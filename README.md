# AI Schedule Planner - Fixed Version

This version serves the frontend directly from the FastAPI backend.

## Run

```powershell
cd C:\ANTIGRAVITY
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python -m backend.app
```

Open:

```text
http://127.0.0.1:8080
```

## Gemini API Key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_real_key_here
```

Without the key, the app still runs and shows mock schedule data.

## Test API

```text
http://127.0.0.1:8080/health
http://127.0.0.1:8080/docs
```
