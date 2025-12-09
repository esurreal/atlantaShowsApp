from fastapi import FastAPI
from datetime import datetime
import os
from backend.app.models import fetch_events
from backend.app.ingest import fetch_eventbrite_by_location, normalize_eventbrite

app = FastAPI(title="Atlanta Concerts API")

@app.get("/events")
async def events(lat: float = None, lon: float = None, limit: int = 200):
    # For MVP: if lat/lon provided, call Eventbrite and return normalized results
    if lat and lon:
        try:
            evs = await fetch_eventbrite_by_location(lat, lon)
            normalized = [normalize_eventbrite(e) for e in evs]
            normalized_sorted = sorted(normalized, key=lambda x: x["start_utc"])[:limit]
            return normalized_sorted
        except Exception as e:
            return {"error": str(e)}
    # otherwise, return events fetched from DB
    rows = await fetch_events(limit=limit)
    return rows

@app.get("/health")
async def health():
    return {"status": "ok", "time": datetime.utcnow().isoformat()}
