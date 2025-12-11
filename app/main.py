from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from datetime import datetime
import os
import uvicorn
from .models import fetch_events
from .ingest import fetch_eventbrite_by_location, normalize_eventbrite
from .ingest import fetch_bandsintown_for_artist, normalize_bandsintown

app = FastAPI()

import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Get the DATABASE_URL from environment variables
db_url = os.getenv("DATABASE_URL")

if not db_url:
    raise RuntimeError(
        "DATABASE_URL environment variable not set. "
        "Please set it in Railway project variables."
    )

# Convert to async format for SQLAlchemy
async_db_url = db_url.replace("postgresql://", "postgresql+asyncpg://")

# Create the async engine
engine = create_async_engine(async_db_url, future=True)

# Optional: create a session factory for async sessions
AsyncSessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# Example usage function
async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

print("Database engine initialized successfully")


@app.get("/events")
async def get_events():
    events = await fetch_events()
    return fetch_events()

@app.get("/health")
async def health():
    return {"status": "ok", "time": datetime.utcnow().isoformat()}

@app.get("/test-eventbrite")
async def test_eventbrite():
    try:
        events = await fetch_eventbrite_by_location(33.7490, -84.3880)
        return {"count": len(events), "sample": events[:1]}
    except Exception as e:
        return {"error": str(e)}


@app.get("/bandsintown")
async def get_bandsintown_events(artist: str):
    raw_events = await fetch_bandsintown_for_artist(artist)
    return [normalize_bandsintown(e) for e in raw_events]
   




