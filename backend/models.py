from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class SubjectInput(BaseModel):
    name: str = Field(..., min_length=1)
    proficiency: int = Field(..., ge=1, le=5)


class StudyScheduleRequest(BaseModel):
    start_time: str = Field(..., description="HH:MM in 24-hour format")
    end_time: str = Field(..., description="HH:MM in 24-hour format")
    subjects: List[SubjectInput] = Field(..., min_length=1)
    break_duration: int = Field(default=10, ge=0, le=60, description="Duration of break in minutes")
    preferred_subject_order: List[str] = Field(default_factory=list)


class ScheduleItem(BaseModel):
    start_time: str
    end_time: str
    subject: str
    topic: str
    notes: str
    slot_type: Literal["study", "break"] = "study"


class UserProfile(BaseModel):
    start_time: str
    end_time: str
    subjects: List[SubjectInput]
    window_minutes: int
    break_duration: int
    preferred_subject_order: List[str]
