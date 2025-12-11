import os
import httpx
from datetime import datetime, timezone
from rapidfuzz import fuzz

BANDSINTOWN_APP_ID = os.getenv("BANDSINTOWN_APP_ID")
EVENTBRITE_TOKEN = os.getenv("EVENTBRITE_TOKEN")

async def fetch_bandsintown_for_artist(artist_name: str):
    url = f"https://rest.bandsintown.com/artists/{artist_name}/events"
    params = {"app_id": BANDSINTOWN_APP_ID, "date": "upcoming"}
    async with httpx.AsyncClient() as client:
        r = await client.get(url, params=params, timeout=20)
        r.raise_for_status()
        return r.json()

async def fetch_eventbrite_by_location(lat: float, lon: float, within_miles: int = 25):
    url = "https://www.eventbriteapi.com/v3/events/search/"
    params = {
        "location.latitude": lat,
        "location.longitude": lon,
        "location.within": f"{within_miles}mi",
        "expand": "venue",
    }
    headers = {"Authorization": f"Bearer {EVENTBRITE_TOKEN}"}  # <-- token goes here, not in params
    async with httpx.AsyncClient() as client:
        r = await client.get(url, params=params, headers=headers, timeout=20)
        r.raise_for_status()
        return r.json().get("events", [])

def normalize_bandsintown(ev):
    venue = ev.get("venue", {})
    start = ev.get("datetime")
    start_dt = datetime.fromisoformat(start).astimezone(timezone.utc)
    artists = ev.get("artists") or []
    title = ev.get("title") or (', '.join(a.get('name') for a in artists) if artists else ev.get('title'))
    return {
        "title": title,
        "start_utc": start_dt.isoformat(),
        "end_utc": None,
        "venue_name": venue.get("name"),
        "city": venue.get("city"),
        "state": venue.get("region"),
        "url": ev.get("url"),
        "ticket_url": (ev.get("offers") or [None])[0].get("url") if ev.get("offers") else None
    }

def normalize_eventbrite(ev):
    v = ev.get("venue", {})
    start = ev.get("start", {}).get("utc")
    start_dt = datetime.fromisoformat(start).replace(tzinfo=timezone.utc)
    end = ev.get("end", {}).get("utc")
    end_dt = datetime.fromisoformat(end).replace(tzinfo=timezone.utc) if end else None
    return {
        "title": ev.get("name", {}).get("text"),
        "start_utc": start_dt.isoformat(),
        "end_utc": end_dt.isoformat() if end_dt else None,
        "venue_name": v.get("name"),
        "city": v.get("address", {}).get("city"),
        "state": v.get("address", {}).get("region"),
        "url": ev.get("url"),
        "ticket_url": ev.get("url")
    }

def probable_duplicate_score(ev_a, ev_b):
    # ev_a and ev_b are dicts with title, start_utc (iso), venue_name
    title_score = fuzz.token_sort_ratio(ev_a.get("title",""), ev_b.get("title","")) / 100.0
    try:
        from datetime import datetime
        a = datetime.fromisoformat(ev_a.get("start_utc"))
        b = datetime.fromisoformat(ev_b.get("start_utc"))
        time_delta = abs((a - b).total_seconds())
    except Exception:
        time_delta = 999999
    time_score = 1.0 if time_delta < 7200 else 0.0
    venue_score = 1.0 if (ev_a.get("venue_name") and ev_b.get("venue_name") and ev_a.get("venue_name").lower()==ev_b.get("venue_name").lower()) else 0.0
    score = (0.45*title_score) + (0.35*time_score) + (0.20*venue_score)
    return score
