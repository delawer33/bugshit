# TaskFlow

Project management API and web client for teams tracking tasks, projects, and internal credits.

## Stack

- **Backend:** Python 3.12, FastAPI, SQLAlchemy, SQLite
- **Frontend:** React 18, TypeScript, Vite

## Quick start

```bash
# Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m app.seed
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

## Default accounts

| User  | Password    |
| ----- | ----------- |
| admin | admin       |
| alice | password123 |
| bob   | password123 |
