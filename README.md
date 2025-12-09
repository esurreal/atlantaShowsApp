# Atlanta Concerts — Scaffold (Light Mode)

This repository scaffold provides a minimal, runnable FastAPI backend + React (Vite) frontend (light-mode UI)
and Docker compose so you can run the full stack locally. It starts with Bandsintown + Eventbrite connectors
and exposes `/events` (chronological). The scaffold intentionally keeps things small so you can iterate.

## Quick start (Docker)
1. Copy `.env.example` to `.env` and fill in your keys.
2. `docker compose up --build`
3. Backend API: `http://localhost:8000/events?lat=33.7490&lon=-84.3880`
4. Frontend UI: `http://localhost:5173` (light-mode UI)

## Local dev (without Docker)
- Backend: `cd backend && pip install -r app/requirements.txt && uvicorn app.main:app --reload`
- Frontend: `cd frontend && npm install && npm run dev`

## Notes
- This scaffold is intentionally minimal: no production auth, simple dedupe, no search index.
- Extend `backend/app/ingest.py` to add more connectors (Songkick, Ticketmaster) or scraping if needed.
