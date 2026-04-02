// useOrbitData — polls Orbit API, falls back to mock data when offline

import { useState, useEffect, useCallback } from 'react'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8080'

const MOCK_RESPONSE = {
  intent: 'MENTOR',
  agents: [{ name: 'mentor_agent', status: 'DONE', latency_ms: 142 }],
}

const INITIAL = {
  intent: { label: '—', text: '—' },
  agents: [],
  memory: { redis: [{ key: 'session:active', value: true }], pgvector: { query: '—', results: [] } },
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
      const res = await fetch(`${API}/health`, { signal: AbortSignal.timeout(2000) })

      const json = await res.json()

      setData(d => ({ ...d, connected: json.status === 'ok', latency: Date.now() - start }))

    } catch {
      setData(d => ({ ...d, connected: false, latency: 0 }))
    }
  }, [])

  useEffect(() => {
    check()
    const id = setInterval(check, 5000)
    return () => clearInterval(id)
  }, [check])

  const sendRequest = useCallback(async (text, sessionId = 'dash-session') => {
    const start = Date.now()

    let json = MOCK_RESPONSE

    try {
      const res = await fetch(`${API}/intent`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId, text }),
        signal: AbortSignal.timeout(4000),
      })

      json = await res.json()

    } catch {
      // API offline — use mock so dashboard stays functional in CI
    }

    const latency = Date.now() - start

    const ts = new Date().toISOString().slice(11, 19)

    const agentList = (json.agents || []).map(a => ({
      name: typeof a === 'string' ? a.split('.').pop() : a.name,
      status: a.status || 'DONE',
      latency_ms: a.latency_ms || latency,
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
  }, [])

  return { data, sendRequest }
}
