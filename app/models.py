# app/models.py
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Load .env file
load_dotenv()

# Get DATABASE_URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL is not set. Check your .env file.")

# Create async engine
engine = create_async_engine(DATABASE_URL, future=True, echo=True)

# Create session factory
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

# Example function to fetch events (adjust to your schema)
async def fetch_events():
    async with async_session() as session:
        result = await session.execute("SELECT * FROM events")
        return result.fetchall()


    # TODO: Replace with real DB queries when DB is wired up
    return []

