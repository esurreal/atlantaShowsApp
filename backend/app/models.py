# Lightweight DB helpers for async access using SQLAlchemy core
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_async_engine(DATABASE_URL, future=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def fetch_events(limit=200):
    async with async_session() as s:
        q = text("SELECT e.title,e.start_utc,e.end_utc,v.name as venue_name,v.city,v.state,e.url,e.ticket_url FROM events e LEFT JOIN venues v ON e.venue_id = v.id WHERE e.start_utc >= now() ORDER BY e.start_utc LIMIT :limit")
        r = await s.execute(q, {"limit": limit})
        rows = r.fetchall()
        return [dict(row._mapping) for row in rows]

async def find_existing_event(session: AsyncSession, title: str, start_utc, venue_id: int):
    # naive exact/near match lookup
    q = text("""
        SELECT e.id, e.title, e.start_utc FROM events e
        WHERE e.venue_id = :venue_id
          AND ABS(EXTRACT(EPOCH FROM (e.start_utc - :start_utc))) < 7200
        LIMIT 1
    """)
    r = await session.execute(q, {"venue_id": venue_id, "start_utc": start_utc})
    row = r.first()
    return row[0] if row else None

async def upsert_event_with_source(event_obj, source_name, source_event_id, raw_payload):
    async with async_session() as s:
        # insert or find venue
        venue_id = None
        if event_obj.get("venue_name"):
            r = await s.execute(text("SELECT id FROM venues WHERE name = :name LIMIT 1"), {"name": event_obj["venue_name"]})
            row = r.first()
            if row:
                venue_id = row[0]
            else:
                rr = await s.execute(text("INSERT INTO venues(name, city, state, country) VALUES(:n,:c,:s,:co) RETURNING id"), {"n": event_obj["venue_name"],"c": event_obj.get("city"),"s": event_obj.get("state"),"co": event_obj.get("country")})
                venue_id = rr.scalar()
                await s.commit()
        # check for existing
        existing = await find_existing_event(s, event_obj.get("title"), event_obj.get("start_utc"), venue_id)
        if existing:
            # only save source metadata
            await s.execute(text("INSERT INTO event_sources(event_id, source_name, source_event_id, raw_payload) VALUES(:eid,:sn,:seid,:rp)"), {"eid": existing,"sn": source_name,"seid": source_event_id,"rp": json.dumps(raw_payload)})
            await s.commit()
            return existing
        rr = await s.execute(text("INSERT INTO events(title, start_utc, end_utc, venue_id, description, url, ticket_url) VALUES(:t,:st,:en,:v,:d,:u,:tu) RETURNING id"), {
            "t": event_obj.get("title"),
            "st": event_obj.get("start_utc"),
            "en": event_obj.get("end_utc"),
            "v": venue_id,
            "d": event_obj.get("description"),
            "u": event_obj.get("url"),
            "tu": event_obj.get("ticket_url")
        })
        event_id = rr.scalar()
        await s.execute(text("INSERT INTO event_sources(event_id, source_name, source_event_id, raw_payload) VALUES(:eid,:sn,:seid,:rp)"), {"eid": event_id,"sn": source_name,"seid": source_event_id,"rp": json.dumps(raw_payload)})
        await s.commit()
        return event_id
