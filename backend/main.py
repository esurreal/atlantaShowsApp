from fastapi import FastAPI
from datetime import datetime
import os
import uvicorn
from app.models import fetch_events
from app.ingest import fetch_eventbrite_by_location, normalize_eventbrite

app = FastAPI(title="Atlanta Concerts API")

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
