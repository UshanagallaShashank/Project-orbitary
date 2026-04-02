// AgentPanel — which agents were called, status badge, response time

const STATUS_COLOR = {
  RUNNING: 'text-amber-400',
  DONE:    'text-green-400',
  FAILED:  'text-red-400',
}

export default function AgentPanel({ agents }) {
  return (
    <div data-testid="agent-panel" className="border border-zinc-800 bg-zinc-950 p-4">
      <p className="text-zinc-500 text-xs uppercase tracking-widest mb-3">Agents</p>

      {agents.length === 0 && (
        <p className="font-mono text-zinc-600 text-sm">no agents called yet</p>
      )}

      {agents.map((a, i) => (
        <div key={i} className="flex items-center justify-between py-2 border-b border-zinc-800 last:border-0">
          <span className="font-mono text-zinc-100 text-sm">{a.name}</span>

          <div className="flex items-center gap-4">
            <span className="font-mono text-zinc-500 text-xs">{a.latency_ms}ms</span>

            <span className={`font-mono text-xs font-bold ${STATUS_COLOR[a.status] || 'text-zinc-400'}`}
                  data-testid="agent-status">
              {a.status}
            </span>
          </div>
        </div>
      ))}
    </div>
  )
}
