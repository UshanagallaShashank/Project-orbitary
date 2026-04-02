// MemoryPanel — Redis session keys + pgvector last query and top-3 results

import { useState } from 'react'

function RedisRow({ k, v }) {
  const [open, setOpen] = useState(false)

  return (
    <div className="border-b border-zinc-800 last:border-0" data-testid="redis-key">
      <button
        onClick={() => setOpen(o => !o)}
        className="w-full flex items-center justify-between py-2 text-left hover:bg-zinc-900 px-1 transition-colors"
      >
        <span className="font-mono text-zinc-300 text-xs">{k}</span>

        <span className="font-mono text-zinc-600 text-xs">{open ? '▲' : '▼'}</span>
      </button>

      {open && (
        <p className="font-mono text-zinc-500 text-xs px-2 pb-2 break-all">{JSON.stringify(v)}</p>
      )}
    </div>
  )
}

export default function MemoryPanel({ memory }) {
  return (
    <div data-testid="memory-panel" className="border border-zinc-800 bg-zinc-950 p-4">
      <p className="text-zinc-500 text-xs uppercase tracking-widest mb-3">Memory</p>

      <p className="text-zinc-600 text-xs uppercase tracking-widest mb-2">Redis Session</p>

      {memory.redis.map((r, i) => (
        <RedisRow key={i} k={r.key} v={r.value} />
      ))}

      <p className="text-zinc-600 text-xs uppercase tracking-widest mt-4 mb-2">pgvector — last query</p>

      <p className="font-mono text-zinc-400 text-xs mb-2">{memory.pgvector.query}</p>

      {memory.pgvector.results.map((r, i) => (
        <div key={i} className="flex justify-between py-1">
          <span className="font-mono text-zinc-500 text-xs truncate w-4/5">{r.content}</span>

          <span className="font-mono text-green-400 text-xs">{r.score?.toFixed(3)}</span>
        </div>
      ))}
    </div>
  )
}
