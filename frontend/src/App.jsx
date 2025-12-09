import React, {useEffect, useState} from 'react'
import EventList from './components/EventList'

const API_BASE = import.meta.env.VITE_API_BASE || 'https://railway.com/project/a2435af1-ae22-4ec4-b1c0-44c293f4b261/service/7c3fb67a-9b44-4fb5-a6a2-ecdfb15fa707?environmentId=b1c4908d-97ae-4960-8451-da1a2e44f15e&id=9e5bd0d9-54ca-4fe4-920a-b095f0f8f1f4#deploy'

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
