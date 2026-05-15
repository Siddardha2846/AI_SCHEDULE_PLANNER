# AI Personalized Study Scheduler

This version uses a deterministic FastAPI scheduler for a strict daily time window. Gemini is optional and only refines topic and notes text after the backend has finished allocating time blocks.

## Run

```powershell
cd D:\coding\projects\AI_SCHEDULE_PLANNER
.\.venv\Scripts\activate
pip install -r requirements.txt
python -m backend.main
```

Open:

```text
http://127.0.0.1:8080
```

## API

`POST /generate-schedule`

Example request:

```json
{
	"start_time": "09:00",
	"end_time": "16:00",
	"break_duration": 10,
	"preferred_subject_order": ["DBMS", "OS"],
	"subjects": [
		{ "name": "DBMS", "proficiency": 2 },
		{ "name": "OS", "proficiency": 4 }
	]
}
```

The endpoint returns a plain array of cards with `start_time`, `end_time`, `subject`, `topic`, `notes`, and `slot_type`.

## Gemini API Key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_real_key_here
```

If the key is missing or rejected, the deterministic schedule still works.
