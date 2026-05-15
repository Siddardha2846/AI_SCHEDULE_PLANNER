import json
import os
from typing import List

from .models import ScheduleItem, UserProfile

SYSTEM_PROMPT = """You are an AI study schedule enhancer.
The user has a strictly planned deterministic schedule.
Your ONLY job is to improve the 'topic' and 'notes' fields of the study slots.
- Do NOT change the start_time, end_time, subject, or slot_type.
- Do NOT add or remove any slots.
- Make the 'topic' specific, realistic, and tailored to the subject.
- Make the 'notes' brief, encouraging, and tailored to the subject.
- Return the EXACT SAME array of objects, just with updated 'topic' and 'notes'.

Return the result strictly as a JSON array matching the input structure.
"""

def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        return None, None

    try:
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=api_key)
        return client, types
    except Exception as exc:
        print(f"Gemini setup failed: {exc}")
        return None, None


def enrich_schedule(schedule: List[ScheduleItem], profile: UserProfile) -> List[ScheduleItem]:
    client, genai_types = get_gemini_client()
    if client is None or genai_types is None:
        # If no API key or setup failed, return the deterministic schedule as is
        return schedule

    # Prepare input for Gemini
    schedule_dicts = [item.model_dump() for item in schedule]
    prompt = f"Enhance this schedule for a student.\nSubjects and proficiencies:\n"
    for sub in profile.subjects:
        prompt += f"- {sub.name} (Proficiency: {sub.proficiency}/5)\n"
    
    prompt += "\nDeterministic Schedule:\n"
    prompt += json.dumps(schedule_dicts, indent=2)

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=genai_types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                response_mime_type="application/json",
            ),
        )

        content = response.text or ""
        content = content.strip().replace("```json", "").replace("```", "").strip()
        
        enriched_data = json.loads(content)
        
        # Validate and return
        enriched_schedule = []
        for i, original_item in enumerate(schedule):
            if i < len(enriched_data):
                # Only trust topic and notes from AI
                ai_item = enriched_data[i]
                topic = ai_item.get("topic", original_item.topic)
                notes = ai_item.get("notes", original_item.notes)
                
                enriched_schedule.append(ScheduleItem(
                    start_time=original_item.start_time,
                    end_time=original_item.end_time,
                    subject=original_item.subject,
                    topic=topic,
                    notes=notes,
                    slot_type=original_item.slot_type
                ))
            else:
                enriched_schedule.append(original_item)
                
        return enriched_schedule

    except Exception as exc:
        print(f"AI enrichment failed, using deterministic schedule: {exc}")
        return schedule
