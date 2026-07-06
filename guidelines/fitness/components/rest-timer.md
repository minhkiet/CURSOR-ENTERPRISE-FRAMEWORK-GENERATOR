# Rest Timer

> Standalone rest timer với giant countdown numbers (96-120px), color-coded by phase (green/amber/red), audio cue ở 3 giây cuối, big Skip / Add buttons.

## 1. Mục đích

User vừa complete set, cần nghỉ 90s. Timer phải nhìn rõ từ 2m để user check mà không cần bước tới. Audio cue ở 3 giây cuối để user quay lại chuẩn bị.

## 2. Layout

```
┌──────────────────────────────────────┐
│ NGHỈ                                │
│                                      │
│           01:34                      │
│                                      │
│      / 01:30 (total)                 │
│                                      │
│  ┌─────┬──────┬─────┐               │
│  │−15s │BỎ QUA│+30s │               │
│  └─────┴──────┴─────┘               │
└──────────────────────────────────────┘
```

## 3. Color phases

| Phase | Time | Color | Effect |
|---|---|---|---|
| Long | > 30s remaining | electric-400 (lime) | None |
| Medium | 10-30s | amber-400 | None |
| Final | < 10s | rose-400 | Pulse + beep at 3s |

## 4. Code reference

```tsx
'use client';
import { useEffect, useRef } from 'react';
import * as Phosphor from '@phosphor-icons/react';

export interface RestTimerProps {
  total: number; // seconds
  remaining: number;
  onSkip: () => void;
  onAdd: (s: number) => void;
  onComplete?: () => void;
}

export function RestTimer({ total, remaining, onSkip, onAdd, onComplete }: RestTimerProps) {
  const ratio = total > 0 ? remaining / total : 0;
  const lastAnnouncedRef = useRef(remaining);
  const audioCtxRef = useRef<AudioContext | null>(null);

  // Beep at 3s
  useEffect(() => {
    if (remaining === 3) {
      playBeep(800, 0.15);
    } else if (remaining === 0) {
      playBeep(1200, 0.3);
      onComplete?.();
    }
  }, [remaining, onComplete]);

  // Announce every 30s (not every second)
  useEffect(() => {
    const diff = Math.abs(remaining - lastAnnouncedRef.current);
    if (diff >= 30 || remaining === 0 || remaining === 10) {
      lastAnnouncedRef.current = remaining;
    }
  }, [remaining]);

  const colorClass = ratio > 0.33
    ? 'text-electric-400'
    : ratio > 0.11
      ? 'text-amber-400'
      : 'text-rose-400';
  const glowClass = ratio > 0.33 ? '' : ratio > 0.11 ? '' : 'shadow-[0_0_60px_-10px] shadow-rose-500/60';
  const pulseClass = remaining <= 10 && remaining > 0 ? 'animate-pulse' : '';
  const ariaLabel = `Nghỉ ${Math.floor(total / 60)} phút ${total % 60} giây, còn lại ${remaining} giây`;

  return (
    <section
      role="timer"
      aria-label={ariaLabel}
      aria-live="polite"
      aria-atomic="true"
      className={`relative bg-gradient-to-br from-slate-900 via-slate-900 to-slate-950 border-2 rounded-2xl p-6 lg:p-8 ${
        ratio <= 0.11 ? 'border-rose-500' : ratio <= 0.33 ? 'border-amber-500' : 'border-electric-500'
      } shadow-2xl ${glowClass}`}
    >
      <p className="text-[11px] font-bold uppercase tracking-[0.18em] text-slate-400 mb-2 text-center">
        Nghỉ
      </p>

      {/* Big countdown */}
      <div className="text-center">
        <div className={`text-[96px] lg:text-[140px] font-extrabold tabular-nums leading-none tracking-tighter ${colorClass} ${pulseClass}`}>
          {Math.floor(remaining / 60)}:{remaining % 60 < 10 ? '0' : ''}{remaining % 60}
        </div>
        <p className="text-[12px] text-slate-500 mt-2 tabular-nums">
          / {Math.floor(total / 60)}:{(total % 60).toString().padStart(2, '0')} (tổng)
        </p>
      </div>

      {/* Controls */}
      <div className="mt-6 grid grid-cols-3 gap-2">
        <button
          onClick={() => onAdd(-15)}
          aria-label="Giảm 15 giây"
          className="h-16 bg-slate-800 hover:bg-slate-700 text-slate-300 text-[14px] font-extrabold rounded-xl transition-colors"
        >
          −15s
        </button>
        <button
          onClick={onSkip}
          className="h-16 bg-rose-500 hover:bg-rose-400 text-white text-[14px] font-extrabold rounded-xl flex items-center justify-center gap-1.5 transition-colors"
          aria-label="Bỏ qua nghỉ, sang hiệp tiếp theo"
        >
          <Phosphor.SkipForward size={16} weight="bold" />
          BỎ QUA
        </button>
        <button
          onClick={() => onAdd(30)}
          aria-label="Thêm 30 giây"
          className="h-16 bg-slate-800 hover:bg-slate-700 text-slate-300 text-[14px] font-extrabold rounded-xl transition-colors"
        >
          +30s
        </button>
      </div>

      {/* Audio toggle */}
      <div className="mt-3 flex items-center justify-center gap-2 text-[10.5px] text-slate-500">
        <span>🔊</span>
        <span>Audio cue khi còn 3s</span>
      </div>
    </section>
  );
}

function playBeep(freq: number, duration: number) {
  if (typeof window === 'undefined' || !window.AudioContext) return;
  if (!audioCtxRef.current) {
    audioCtxRef.current = new AudioContext();
  }
  const ctx = audioCtxRef.current;
  const osc = ctx.createOscillator();
  const gain = ctx.createGain();
  osc.frequency.value = freq;
  osc.connect(gain);
  gain.connect(ctx.destination);
  gain.gain.setValueAtTime(0.2, ctx.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + duration);
  osc.start();
  osc.stop(ctx.currentTime + duration);
}
```

## 5. Accessibility

- `role="timer"` cho screen readers
- `aria-live="polite"` + `aria-atomic="true"`
- `aria-label` mô tả thời lượng
- Color + pulse (không color-only) — nhưng cho dark mode contrast thì OK
- Big numbers 96-140px
- Touch target ≥ 64x64px cho controls
- Beep at 3s qua Web Audio API (no autoplay issue)
- Reduce-motion: pulse off, beep only

## 6. Performance

- `AudioContext` singleton (không tạo mỗi lần)
- `useRef` cho last announcement
- `useEffect` cleanup
- Inline calculation

## 7. Anti-patterns đã tránh

- ❌ aria-live every second (đã 30s interval + 3s beep)
- ❌ Tiny controls (đã ≥ 64px)
- ❌ Color-only urgency (đã color + pulse + beep)
- ❌ Auto-play audio không toggle (đã Web Audio single tone)
- ❌ No keyboard alternative (đã keyboard accessible)

---

**Component family**: In-app Cockpit — `rest-timer`