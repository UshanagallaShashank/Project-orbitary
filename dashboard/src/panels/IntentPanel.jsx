// IntentPanel — shows last classified intent label + raw input text

const LABEL_COLOR = {
  DSA:      'text-green-400',
  CALENDAR: 'text-amber-400',
  MENTOR:   'text-green-400',
  TRACKER:  'text-amber-400',
  MEMORY:   'text-zinc-400',
  COMMS:    'text-amber-400',
  UNKNOWN:  'text-red-400',
  '—':      'text-zinc-600',
}

export default function IntentPanel({ intent }) {
  const color = LABEL_COLOR[intent.label] || 'text-zinc-400'

  return (
    <div data-testid="intent-panel" className="border border-zinc-800 bg-zinc-950 p-4">
      <p className="text-zinc-500 text-xs uppercase tracking-widest mb-3">Intent</p>

      <p className={`font-mono text-2xl font-bold tracking-wider mb-3 ${color}`}>
        {intent.label}
      </p>

      <p className="text-zinc-500 text-xs uppercase tracking-widest mb-1">Input</p>

      <p className="font-mono text-zinc-300 text-sm break-words">{intent.text}</p>
    </div>
  )
}
