import os
import httpx
from dotenv import load_dotenv

# Load .env
load_dotenv()

EVENTBRITE_TOKEN = os.getenv("EVENTBRITE_TOKEN")
if not EVENTBRITE_TOKEN:
    raise RuntimeError("EVENTBRITE_TOKEN not set in .env")

# Example location: Atlanta, GA
lat, lon = 33.7490, -84.3880

url = "https://www.eventbriteapi.com/v3/events/search/"
params = {
    "location.latitude": lat,
    "location.longitude": lon,
    "location.within": "25mi",
    "expand": "venue"
}
headers = {"Authorization": f"Bearer {EVENTBRITE_TOKEN}"}

# Make request
with httpx.Client() as client:
    r = client.get(url, params=params, headers=headers)
    print(f"Status code: {r.status_code}")
    if r.status_code == 200:
        events = r.json().get("events", [])
        print(f"Found {len(events)} events")
        if events:
            print("First event:", events[0]["name"]["text"])
    else:
        print("Error:", r.text)
