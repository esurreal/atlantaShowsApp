from dotenv import load_dotenv
load_dotenv()  # Loads .env when running local

import os

from fastapi import FastAPI
from datetime import datetime

from .models import fetch_events
from .ingest import (
    fetch_eventbrite_by_location,
    normalize_eventbrite,
    fetch_bandsintown_for_artist,
)

app = FastAPI()


@app.get("/events")
async def get_events():
    return fetch_events()


@app.get("/health")
async def health():
    return {"status": "ok", "time": datetime.utcnow().isoformat()}


# --------------------------
# TEST ENDPOINTS
# --------------------------

@app.get("/test-bandsintown")
async def test_bandsintown():
    """Test to confirm Bandsintown token works"""
    try:
        data = await fetch_bandsintown_for_artist("Metallica")
        return {"success": True, "count": len(data)}
    except Exception as e:
        return {"error": str(e)}


@app.get("/test-eventbrite")
async def test_eventbrite():
    """Test to confirm Eventbrite token works"""
    try:
        events = await fetch_eventbrite_by_location(
            lat=33.749, lon=-84.388, within_miles=25
        )
        return {"success": True, "count": len(events)}
    except Exception as e:
        return {"error": str(e)}




