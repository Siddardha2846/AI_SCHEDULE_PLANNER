from datetime import datetime, timedelta
from typing import List

from .models import ScheduleItem, StudyScheduleRequest, UserProfile


def parse_time(time_str: str) -> datetime:
    # Use a dummy date, we only care about hours and minutes
    return datetime.strptime(time_str, "%H:%M")


def build_user_profile(request: StudyScheduleRequest) -> UserProfile:
    start_dt = parse_time(request.start_time)
    end_dt = parse_time(request.end_time)
    
    if end_dt <= start_dt:
        end_dt += timedelta(days=1)
        
    window_minutes = int((end_dt - start_dt).total_seconds() / 60)
    
    return UserProfile(
        start_time=request.start_time,
        end_time=request.end_time,
        subjects=request.subjects,
        window_minutes=window_minutes,
        break_duration=request.break_duration,
        preferred_subject_order=request.preferred_subject_order
    )


def generate_schedule(profile: UserProfile) -> List[ScheduleItem]:
    if not profile.subjects:
        return []

    # Order subjects if preference is given
    ordered_subjects = []
    pref_names = [name.lower() for name in profile.preferred_subject_order]
    
    # Add preferred ones first
    for pref in pref_names:
        for sub in profile.subjects:
            if sub.name.lower() == pref and sub not in ordered_subjects:
                ordered_subjects.append(sub)
                
    # Add the rest
    for sub in profile.subjects:
        if sub not in ordered_subjects:
            ordered_subjects.append(sub)

    # Calculate weights: lower proficiency = higher weight (needs more time)
    # Proficiency is 1-5. Weight = 6 - proficiency (so 1 -> 5, 5 -> 1)
    weights = {sub.name: 6 - sub.proficiency for sub in ordered_subjects}
    total_weight = sum(weights.values())

    # Estimate number of breaks: roughly 1 break per 50 mins of study
    estimated_blocks = max(1, profile.window_minutes // 60)
    total_break_time = (estimated_blocks - 1) * profile.break_duration
    
    total_study_time = max(10, profile.window_minutes - total_break_time)

    # Allocate study time proportionally
    allocated_mins = {
        sub.name: max(10, int((weights[sub.name] / total_weight) * total_study_time))
        for sub in ordered_subjects
    }

    # Ensure total allocated matches exact total_study_time due to rounding
    diff = total_study_time - sum(allocated_mins.values())
    if diff != 0 and ordered_subjects:
        # Give remaining diff to the weakest subject (highest weight)
        weakest = max(ordered_subjects, key=lambda s: weights[s.name])
        allocated_mins[weakest.name] = max(10, allocated_mins[weakest.name] + diff)

    schedule: List[ScheduleItem] = []
    current_dt = parse_time(profile.start_time)
    end_dt = current_dt + timedelta(minutes=profile.window_minutes)

    max_chunk = 50

    for sub in ordered_subjects:
        rem_mins = allocated_mins[sub.name]
        
        while rem_mins > 0:
            chunk = min(rem_mins, max_chunk)
            
            # Check if we exceed the total window
            if current_dt + timedelta(minutes=chunk) > end_dt:
                chunk = int((end_dt - current_dt).total_seconds() / 60)
                if chunk <= 0:
                    break
            
            slot_end = current_dt + timedelta(minutes=chunk)
            
            topic = f"Review {sub.name}" if sub.proficiency >= 4 else f"Study core concepts of {sub.name}"
            notes = "Revision focus" if sub.proficiency >= 4 else "Focus on weak areas"
            
            schedule.append(ScheduleItem(
                start_time=current_dt.strftime("%H:%M"),
                end_time=slot_end.strftime("%H:%M"),
                subject=sub.name,
                topic=topic,
                notes=notes,
                slot_type="study"
            ))
            
            rem_mins -= chunk
            current_dt = slot_end
            
            # Add break if not at the end
            if rem_mins > 0 or sub != ordered_subjects[-1]:
                if current_dt + timedelta(minutes=profile.break_duration) <= end_dt:
                    break_end = current_dt + timedelta(minutes=profile.break_duration)
                    schedule.append(ScheduleItem(
                        start_time=current_dt.strftime("%H:%M"),
                        end_time=break_end.strftime("%H:%M"),
                        subject="Break",
                        topic="Rest & Recharge",
                        notes="Stretch, hydrate, and relax",
                        slot_type="break"
                    ))
                    current_dt = break_end
                else:
                    # Not enough time for a break, maybe just finish early or no break
                    break

    return schedule
