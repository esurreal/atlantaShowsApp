import React, {useEffect, useState} from 'react'
import EventList from './components/EventList'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export default function App(){
  const [events, setEvents] = useState([])
  useEffect(()=>{
    (async ()=>{
      try{
        const r = await fetch(`${API_BASE}/events?lat=33.7490&lon=-84.3880`)
        const j = await r.json()
        setEvents(j)
      }catch(e){
        console.error(e)
      }
    })()
  },[])
  return (
    <div className="app-container">
      <header className="site-header">
        <h1>Atlanta Concerts</h1>
        <p>Upcoming shows — Atlanta, GA</p>
      </header>
      <main>
        <EventList events={events} />
      </main>
    </div>
  )
}
