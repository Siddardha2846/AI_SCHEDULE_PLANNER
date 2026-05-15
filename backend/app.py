import json
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel


PROJECT_ROOT = Path(__file__).resolve().parent.parent

load_dotenv(PROJECT_ROOT / ".env")
load_dotenv(Path(__file__).resolve().parent / ".env")

app = FastAPI(title="AI Schedule Planner API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ScheduleRequest(BaseModel):
    prompt: str


def get_mock_schedule():
    return {
        "date": "2026-05-15",
        "summary": "A balanced schedule with college, study, gym, and rest. Add your GEMINI_API_KEY in .env to use real AI.",
        "status": "success",
        "warnings": ["Mock data is shown because Gemini is not configured or failed."],
        "schedule": [
            {
                "id": 1,
                "start_time": "06:30",
                "end_time": "07:00",
                "title": "Wake up and freshen up",
                "type": "routine",
                "priority": "medium",
                "reason": "Starts the day clean",
            },
            {
                "id": 2,
                "start_time": "09:00",
                "end_time": "16:00",
                "title": "College",
                "type": "fixed",
                "priority": "high",
                "reason": "Fixed commitment",
            },
            {
                "id": 3,
                "start_time": "16:00",
                "end_time": "17:00",
                "title": "Rest & Snack",
                "type": "break",
                "priority": "low",
                "reason": "Recharge after college",
            },
            {
                "id": 4,
                "start_time": "17:00",
                "end_time": "18:30",
                "title": "DSA Practice",
                "type": "study",
                "priority": "high",
                "reason": "Important skill improvement",
            },
            {
                "id": 5,
                "start_time": "18:30",
                "end_time": "19:30",
                "title": "Gym",
                "type": "health",
                "priority": "medium",
                "reason": "Physical health",
            },
            {
                "id": 6,
                "start_time": "20:00",
                "end_time": "21:30",
                "title": "Revise DBMS",
                "type": "study",
                "priority": "high",
                "reason": "Academic requirement",
            },
            {
                "id": 7,
                "start_time": "21:30",
                "end_time": "22:30",
                "title": "Submit Assignment",
                "type": "study",
                "priority": "high",
                "reason": "Deadline approaching",
            },
            {
                "id": 8,
                "start_time": "23:00",
                "end_time": "06:30",
                "title": "Sleep",
                "type": "routine",
                "priority": "high",
                "reason": "Rest and recovery",
            },
        ],
    }


SYSTEM_PROMPT = """You are an expert AI schedule planner.
Based on the user's prompt, generate a realistic day schedule.

Rules:
- Return JSON ONLY
- No markdown
- No code fences
- No explanation text
- No overlapping tasks
- Include realistic breaks
- Respect fixed timings mentioned by user
- Schedule high-priority work in available slots
- Use 24-hour time format HH:MM
- If all tasks cannot fit, mention it in the warnings array

Exact JSON schema:
{
  "date": "YYYY-MM-DD",
  "summary": "short summary of the day plan",
  "status": "success",
  "warnings": [],
  "schedule": [
    {
      "id": 1,
      "start_time": "07:00",
      "end_time": "08:00",
      "title": "Morning routine",
      "type": "routine",
      "priority": "medium",
      "reason": "Keeps the day organized"
    }
  ]
}

Types allowed: routine, fixed, study, health, break
Priority allowed: high, medium, low"""


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
        print(f"Gemini setup failed, using mock data: {exc}")
        return None, None


@app.get("/")
def serve_frontend():
    index_path = PROJECT_ROOT / "frontend" / "index.html"

    if not index_path.exists():
        raise HTTPException(status_code=500, detail="frontend/index.html not found")

    return FileResponse(index_path)


@app.get("/health")
def health():
    return {"message": "AI Schedule Planner backend is running"}


@app.post("/generate-schedule")
async def generate_schedule(req: ScheduleRequest):
    if not req.prompt or not req.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt is required")

    client, genai_types = get_gemini_client()

    if client is None or genai_types is None:
        return get_mock_schedule()

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=req.prompt,
            config=genai_types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                response_mime_type="application/json",
            ),
        )

        content = response.text or ""
        content = content.strip()
        content = content.replace("```json", "").replace("```", "").strip()

        return json.loads(content)

    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=500, detail=f"AI returned invalid JSON: {exc}")

    except Exception as exc:
        print(f"AI generation failed, using mock data: {exc}")
        fallback = get_mock_schedule()
        fallback["warnings"] = [f"AI generation failed, mock data shown: {exc}"]
        return fallback


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.app:app",
        host="127.0.0.1",
        port=8080,
        reload=True,
    )