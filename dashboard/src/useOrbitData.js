// useOrbitData — polls the Orbit API and keeps dashboard state in sync

import { useState, useEffect, useCallback } from 'react'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8080'

const INITIAL = {
  intent: { label: '—', text: '—' },
  agents: [],
  memory: { redis: [], pgvector: { query: '—', results: [] } },
  voice: { transcript: '—', latency_ms: 0, listening: false },
  log: [],
  connected: false,
  latency: 0,
}

export function useOrbitData() {
  const [data, setData] = useState(INITIAL)

  const check = useCallback(async () => {
    const start = Date.now()

    try {
      const res = await fetch(`${API}/health`)

      const latency = Date.now() - start

      const json = await res.json()

      setData(d => ({ ...d, connected: json.status === 'ok', latency }))

    } catch {
      setData(d => ({ ...d, connected: false }))
    }
  }, [])

  useEffect(() => {
    check()
    const id = setInterval(check, 3000)
    return () => clearInterval(id)
  }, [check])

  const sendRequest = useCallback(async (text, sessionId = 'dash-session') => {
    const start = Date.now()

    try {
      const res = await fetch(`${API}/intent`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId, text }),
      })

      const json = await res.json()

      const latency = Date.now() - start

      const ts = new Date().toISOString().slice(11, 19)

      const agentList = (json.agents || []).map(a => ({
        name: a.split('.').pop(),
        status: 'DONE',
        latency_ms: latency,
      }))

      const logEntry = {
        ts,
        intent: json.intent || 'UNKNOWN',
        agent: agentList.map(a => a.name).join(', ') || '—',
        latency,
        status: 'DONE',
      }

      setData(d => ({
        ...d,
        intent: { label: json.intent || 'UNKNOWN', text },
        agents: agentList,
        voice: { transcript: text, latency_ms: latency, listening: false },
        log: [logEntry, ...d.log].slice(0, 5),
      }))

    } catch (e) {
      const ts = new Date().toISOString().slice(11, 19)

      setData(d => ({
        ...d,
        log: [{ ts, intent: 'ERROR', agent: '—', latency: 0, status: 'FAILED' }, ...d.log].slice(0, 5),
      }))
    }
  }, [])

  return { data, sendRequest }
}
