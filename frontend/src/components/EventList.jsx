import React from 'react'

function formatLocal(iso){
  try{
    const d = new Date(iso)
    return d.toLocaleString(undefined, {weekday:'short', month:'short', day:'numeric', hour:'numeric', minute:'2-digit'})
  }catch(e){return iso}
}

export default function EventList({events=[]}){
  if(!events.length) return <div className="empty">No upcoming events found.</div>
  return (
    <div className="events">
      {events.map((e, idx)=> (
        <article className="event" key={idx}>
          <div className="event-time">{formatLocal(e.start_utc)}</div>
          <div className="event-body">
            <h3 className="event-title">{e.title}</h3>
            <div className="event-venue">{e.venue_name} {e.city?`· ${e.city}`:''} {e.state?`· ${e.state}`:''}</div>
            <div className="event-links">
              {e.ticket_url && <a href={e.ticket_url} target="_blank" rel="noreferrer">🎟 Tickets</a>}
              {e.url && <a href={e.url} target="_blank" rel="noreferrer">Details</a>}
            </div>
          </div>
        </article>
      ))}
    </div>
  )
}
