// useOrbitData — sends requests to Orbit API, uses mock when offline

import { useState, useEffect, useCallback } from 'react'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8080'

// Intent labels for deterministic offline classification
const KEYWORD_MAP = {
  MENTOR:   ['explain', 'what is', 'teach', 'how does', 'define'],
  TRACKER:  ['streak', 'leetcode', 'solved', 'log', 'progress'],
  CALENDAR: ['calendar', 'schedule', 'event', 'meeting', 'today'],
  COMMS:    ['email', 'gmail', 'send', 'read', 'inbox'],
  DSA:      ['array', 'tree', 'graph', 'heap', 'sort', 'binary'],
}

function classifyOffline(text) {
  const lower = text.toLowerCase()

  for (const [label, keywords] of Object.entries(KEYWORD_MAP)) {
    if (keywords.some(k => lower.includes(k))) return label
  }

  return 'MENTOR'
}

function agentFor(intent) {
  const map = {
    MENTOR: 'mentor_agent', TRACKER: 'tracker_agent',
    CALENDAR: 'task_agent', COMMS: 'comms_agent',
    DSA: 'tracker_agent', MEMORY: 'memory_agent',
  }
  return map[intent] || 'mentor_agent'
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

  // Health check every 5s — does not block anything
  useEffect(() => {
    const check = async () => {
      const start = Date.now()
      try {
        const res = await fetch(`${API}/health`, { signal: AbortSignal.timeout(1500) })
        const json = await res.json()
        setData(d => ({ ...d, connected: json.status === 'ok', latency: Date.now() - start }))
      } catch {
        setData(d => ({ ...d, connected: false, latency: 0 }))
      }
    }
    check()
    const id = setInterval(check, 5000)
    return () => clearInterval(id)
  }, [])

  const sendRequest = useCallback(async (text, sessionId = 'dash-session') => {
    const start = Date.now()

    // Apply mock immediately — state updates before any fetch
    const offlineIntent = classifyOffline(text)
    const offlineAgent = agentFor(offlineIntent)
    const ts = new Date().toISOString().slice(11, 19)

    const applyResult = (intent, agentName, latency) => {
      setData(d => ({
        ...d,
        intent: { label: intent, text },
        agents: [{ name: agentName, status: 'DONE', latency_ms: latency }],
        voice: { transcript: text, latency_ms: latency, listening: false },
        log: [{ ts, intent, agent: agentName, latency, status: 'DONE' }, ...d.log].slice(0, 5),
      }))
    }

    // Apply offline result immediately so UI updates right away
    applyResult(offlineIntent, offlineAgent, 0)

    // Then try to hit real API and overwrite if it responds
    try {
      const res = await fetch(`${API}/intent`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId, text }),
        signal: AbortSignal.timeout(3000),
      })

      const json = await res.json()

      const latency = Date.now() - start

      const agentList = (json.agents || []).map(a => ({
        name: typeof a === 'string' ? a.split('.').pop() : a.name,
        status: a.status || 'DONE',
        latency_ms: a.latency_ms || latency,
      }))

      const realIntent = json.intent || offlineIntent

      const realAgent = agentList[0]?.name || offlineAgent

      applyResult(realIntent, realAgent, latency)

    } catch {
      // Offline result already applied above — nothing more to do
    }
  }, [])

  return { data, sendRequest }
}
