from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .gemini_service import enrich_schedule
from .models import ScheduleItem, StudyScheduleRequest
from .scheduler import build_user_profile, generate_schedule

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"

load_dotenv(PROJECT_ROOT / ".env")
load_dotenv(Path(__file__).resolve().parent / ".env")

app = FastAPI(title="AI Personalized Study Scheduler")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

if FRONTEND_DIR.exists():
    app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend")


@app.get("/")
def serve_frontend():
    index_path = FRONTEND_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=500, detail="frontend/index.html not found")
    return FileResponse(index_path)


@app.get("/health")
def health():
    return {"status": "ok", "message": "AI Personalized Study Scheduler backend is running"}


@app.post("/generate-schedule", response_model=list[ScheduleItem])
def generate_study_schedule(request: StudyScheduleRequest):
    profile = build_user_profile(request)
    deterministic_schedule = generate_schedule(profile)
    enriched_schedule = enrich_schedule(deterministic_schedule, profile)
    return enriched_schedule


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8080, reload=True)
