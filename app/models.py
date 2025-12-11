from dotenv import load_dotenv
load_dotenv()

import os

DATABASE_URL = os.getenv("DATABASE_URL")
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

print("DEBUG — DATABASE_URL:", os.getenv("DATABASE_URL"))
print("DEBUG — BANDSINTOWN_APP_ID:", os.getenv("BANDSINTOWN_APP_ID"))

engine = create_async_engine(DATABASE_URL, future=True)
# Load DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")

# Flag for local mode (no DB)
NO_DB = DATABASE_URL is None or DATABASE_URL.strip() == ""

if NO_DB:
    print("⚠️ No DATABASE_URL found — running in NO-DB mode (local dev).")
    engine = None
    AsyncSessionLocal = None
else:
    # Convert to async format if needed
    async_db_url = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
    engine = create_async_engine(async_db_url, future=True)
    AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_session():
    """Yields a database session — but disabled in no-DB mode."""
    if NO_DB:
        raise RuntimeError("Database session requested but no DATABASE_URL is set.")
    async with AsyncSessionLocal() as session:
        yield session


# -------------------------------------------------------
# MOCK EVENT DATA FOR LOCAL DEVELOPMENT
# -------------------------------------------------------
def fetch_events():
    """Returns real DB events in production OR mock events locally."""
    if NO_DB:
        # Mocked events so your API works in local dev mode
        return [
            {
                "title": "Mock Concert",
                "start_utc": datetime.now(timezone.utc).isoformat(),
                "venue_name": "Local Test Venue",
                "city": "Atlanta",
                "state": "GA",
                "url": "https://example.com",
                "ticket_url": None,
            }
        ]

    # TODO: Replace with real DB queries when DB is wired up
    return []

