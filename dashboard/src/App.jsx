// App.jsx — ORBIT debug dashboard, terminal meets mission control

import { useState } from 'react'
import { useOrbitData } from './useOrbitData'
import IntentPanel from './panels/IntentPanel'
import AgentPanel from './panels/AgentPanel'
import MemoryPanel from './panels/MemoryPanel'
import VoicePanel from './panels/VoicePanel'

function TopBar({ connected, latency }) {
  const now = new Date().toLocaleTimeString('en-IN', { timeZone: 'Asia/Kolkata', hour12: false })

  return (
    <div className="flex items-center justify-between px-6 py-3 border-b border-zinc-800 bg-zinc-950">
      <span className="font-mono text-zinc-100 text-sm tracking-[0.3em] uppercase font-bold">Orbit</span>

      <div className="flex items-center gap-6">
        <div className="flex items-center gap-2">
          <div className={`w-2 h-2 rounded-full ${connected ? 'bg-green-400' : 'bg-red-400'}`}
               data-testid="connection-dot" />
          <span className="font-mono text-zinc-400 text-xs">{latency}ms</span>
        </div>

        <span className="font-mono text-zinc-500 text-xs">{now} IST</span>
      </div>
    </div>
  )
}

function RequestLog({ log }) {
  return (
    <div className="border-t border-zinc-800 bg-zinc-950 px-6 py-3">
      <div className="flex items-center justify-between mb-2">
        <p className="text-zinc-600 text-xs uppercase tracking-widest">Request Log</p>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-xs font-mono" data-testid="request-log">
          <thead>
            <tr className="text-zinc-600">
              <th className="text-left pr-6 pb-1">time</th>
              <th className="text-left pr-6 pb-1">intent</th>
              <th className="text-left pr-6 pb-1">agent</th>
              <th className="text-left pr-6 pb-1">latency</th>
              <th className="text-left pb-1">status</th>
            </tr>
          </thead>

          <tbody>
            {log.length === 0 && (
              <tr><td colSpan={5} className="text-zinc-700 py-1">no requests yet</td></tr>
            )}

            {log.map((r, i) => (
              <tr key={i} className="border-t border-zinc-900">
                <td className="text-zinc-500 pr-6 py-1">{r.ts}</td>
                <td className="text-zinc-300 pr-6">{r.intent}</td>
                <td className="text-zinc-400 pr-6">{r.agent}</td>
                <td className="text-zinc-500 pr-6">{r.latency}ms</td>
                <td className={r.status === 'DONE' ? 'text-green-400' : 'text-red-400'}>{r.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

function ExportButton({ log }) {
  const exportLog = () => {
    const lines = log.map(r => JSON.stringify(r)).join('\n')

    const blob = new Blob([lines], { type: 'application/jsonl' })

    const url = URL.createObjectURL(blob)

    const a = document.createElement('a')

    a.href = url
    a.download = `orbit-log-${Date.now()}.jsonl`
    a.click()

    URL.revokeObjectURL(url)
  }

  return (
    <button
      onClick={exportLog}
      data-testid="export-button"
      className="border border-zinc-700 bg-zinc-900 text-zinc-300 font-mono text-xs px-4 py-1.5 hover:border-zinc-500 hover:text-zinc-100 transition-colors"
    >
      export .jsonl
    </button>
  )
}

function InputBar({ onSend }) {
  const [text, setText] = useState('')

  const send = () => {
    if (!text.trim()) return
    onSend(text.trim())
    setText('')
  }

  return (
    <div className="flex gap-2 px-6 py-3 border-t border-zinc-800 bg-black">
      <input
        value={text}
        onChange={e => setText(e.target.value)}
        onKeyDown={e => e.key === 'Enter' && send()}
        placeholder="type a request and press enter..."
        data-testid="input-bar"
        className="flex-1 bg-zinc-950 border border-zinc-800 font-mono text-zinc-200 text-sm px-3 py-2 outline-none focus:border-zinc-600 placeholder:text-zinc-700"
      />

      <button
        onClick={send}
        className="border border-zinc-700 bg-zinc-900 text-zinc-300 font-mono text-xs px-4 hover:border-zinc-500 transition-colors"
      >
        send
      </button>
    </div>
  )
}

export default function App() {
  const { data, sendRequest } = useOrbitData()

  return (
    <div className="grid-bg min-h-screen flex flex-col">
      <TopBar connected={data.connected} latency={data.latency} />

      <div className="flex-1 grid grid-cols-2 gap-px p-px">
        <div className="flex flex-col gap-px">
          <IntentPanel intent={data.intent} />
          <AgentPanel agents={data.agents} />
        </div>

        <div className="flex flex-col gap-px">
          <MemoryPanel memory={data.memory} />
          <VoicePanel voice={data.voice} />
        </div>
      </div>

      <div className="border-t border-zinc-800 bg-zinc-950 px-6 py-2 flex justify-end">
        <ExportButton log={data.log} />
      </div>

      <RequestLog log={data.log} />

      <InputBar onSend={sendRequest} />
    </div>
  )
}
