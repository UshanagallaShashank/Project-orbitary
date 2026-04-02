// VoicePanel — waveform, last transcript, Gemini Live latency

import { useEffect, useRef } from 'react'

function Waveform({ active }) {
  const bars = Array.from({ length: 24 }, (_, i) => i)

  return (
    <div className="flex items-center gap-px h-8 mb-3">
      {bars.map(i => (
        <div
          key={i}
          className={`w-1 rounded-sm ${active ? 'bg-green-400' : 'bg-zinc-700'}`}
          style={{
            height: active ? `${8 + Math.sin(i * 0.8) * 12 + Math.random() * 8}px` : '4px',
            transition: active ? 'height 0.1s ease' : 'height 0.3s ease',
          }}
        />
      ))}
    </div>
  )
}

export default function VoicePanel({ voice }) {
  return (
    <div data-testid="voice-panel" className="border border-zinc-800 bg-zinc-950 p-4">
      <p className="text-zinc-500 text-xs uppercase tracking-widest mb-3">Voice</p>

      <Waveform active={voice.listening} />

      <p className="text-zinc-500 text-xs uppercase tracking-widest mb-1">Last Transcript</p>

      <p className="font-mono text-zinc-300 text-sm mb-4 break-words">{voice.transcript}</p>

      <div className="flex items-center justify-between">
        <p className="text-zinc-500 text-xs uppercase tracking-widest">Gemini Live Latency</p>

        <p className="font-mono text-green-400 text-sm" data-testid="voice-latency">
          {voice.latency_ms}ms
        </p>
      </div>
    </div>
  )
}
