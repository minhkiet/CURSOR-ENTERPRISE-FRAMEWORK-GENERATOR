# Workout Screen

> In-app workout tracker. Active exercise video + current set input + set list + rest timer. Designed cho mid-set glove-friendly input.

## 1. Mục đích

User đang squat 100kg, không cầm điện thoại 2 tay, mồ hôi. Phải log set 1-tap nhanh với ngón cái, tự động start rest timer, advance to next set.

## 2. Asset

| Element | Source |
|---|---|
| Exercise video | Coverr.co fitness stock videos |
| Poster image | Unsplash curated gym shots |
| Equipment photos | Unsplash + icon (barbell, dumbbell, kettlebell) |

## 3. Layout

```
┌──────────────────────────────────────────────────────────────────────┐
│ Header: ← Back | Bài 3/8 · Bench Press | ⏱ 28:34 | Share | ⚙         │
├──────────────────────────────────┬───────────────────────────────────┤
│                                  │                                   │
│  Exercise video                  │  CURRENT SET (hiệp 2 / 4)       │
│  (16:9, autoplay muted, loop)    │                                   │
│  ┌──────────────────┐            │  Trọng lượng:  [-] 80 kg [+]    │
│  │                  │            │  Số lần:      [-] 8 reps [+]    │
│  │   Video          │            │  RIR:          ●○●●  (3)        │
│  │                  │            │                                   │
│  └──────────────────┘            │  ┌────────────────────────────┐ │
│  Form cues: "Giữ lưng thẳng"    │  │                            │ │
│                                  │  │   ✓ HOÀN THÀNH HIỆP        │ │
├──────────────────────────────────┤  │                            │ │
│ SET LIST                          │  └────────────────────────────┘ │
│ ✓ Hiệp 1 · 80kg x 8 · 02:30 ago │                                   │
│ ✓ Hiệp 2 · 80kg x 8 · 01:50 ago │                                   │
│ ► Hiệp 3 · 80kg x 8 (active)    │  Rest timer: 01:34               │
│ ○ Hiệp 4 · ??kg x ??            │  [Skip nghỉ]  [+30s]             │
│                                  │                                   │
├──────────────────────────────────┴───────────────────────────────────┤
│ FOOTER: ‹ Bài trước: Incline DB | Bài tiếp: Close-grip bench ›       │
└──────────────────────────────────────────────────────────────────────┘
```

## 4. Variants

| Variant | Use | Khác biệt |
|---|---|---|
| `default` | Strength training | Weight + reps + RIR |
| `cardio` | HIIT / cardio | Time + distance + HR |
| `bodyweight` | Calisthenetics | Reps only |
| `companion` | Side-by-side video | Larger video, smaller inputs |

## 5. States

| State | Visual |
|---|---|
| default | Active set highlighted |
| rest-active | Big countdown |
| set-completed | Check + auto-advance |
| reduce-motion | No pulse/glow |

## 6. Icon mapping

| Role | Phosphor |
|---|---|
| Back | `ArrowLeft` |
| Share | `ShareNetwork` |
| Settings | `GearSix` |
| Check (set done) | `CheckCircle` (fill) |
| Plus | `Plus` |
| Minus | `Minus` |
| Clock | `Clock` |
| Skip | `SkipForward` |
| Play (video) | `PlayCircle` |
| Pause | `PauseCircle` |
| Volume | `SpeakerSimpleHigh` |
| Heart rate | `Heartbeat` |
| Fire | `Fire` (fill) |

## 7. Code reference

```tsx
'use client';
import { useState, useEffect, useRef } from 'react';
import * as Phosphor from '@phosphor-icons/react';

export interface ExerciseSet {
  index: number;
  weight: number;
  reps: number;
  rir: number;
  completed: boolean;
  completedAt: Date | null;
}

export interface WorkoutExercise {
  id: string;
  name: string;
  videoUrl: string;
  posterUrl: string;
  cues: string[];
  sets: ExerciseSet[];
  restSeconds: number;
}

const SAMPLE: WorkoutExercise = {
  id: 'bench',
  name: 'Bench Press',
  videoUrl: 'https://coverr.co/videos/b6b3f6a7-6b4e-4e2e-b6a4-b6b3f6a7/1080p.mp4',
  posterUrl: 'https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=800&q=80',
  cues: ['Giữ lưng thẳng', 'Thở vào khi hạ, thở ra khi đẩy', 'Không bật tay khỏi xà'],
  sets: [
    { index: 1, weight: 60, reps: 10, rir: 3, completed: true, completedAt: new Date(Date.now() - 180000) },
    { index: 2, weight: 80, reps: 8, rir: 2, completed: true, completedAt: new Date(Date.now() - 90000) },
    { index: 3, weight: 100, reps: 6, rir: 2, completed: false, completedAt: null },
    { index: 4, weight: 100, reps: 6, rir: 1, completed: false, completedAt: null }
  ],
  restSeconds: 90
};

export function WorkoutScreen() {
  const [sets, setSets] = useState(SAMPLE.sets);
  const [activeIdx, setActiveIdx] = useState(2);
  const [isResting, setIsResting] = useState(false);
  const [restRemaining, setRestRemaining] = useState(0);

  const activeSet = sets[activeIdx];

  const completeSet = () => {
    setSets(prev => prev.map((s, i) =>
      i === activeIdx ? { ...s, completed: true, completedAt: new Date() } : s
    ));
    setIsResting(true);
    setRestRemaining(SAMPLE.restSeconds);
  };

  useEffect(() => {
    if (!isResting || restRemaining <= 0) return;
    const id = setInterval(() => {
      setRestRemaining(r => {
        if (r <= 1) {
          clearInterval(id);
          if (activeIdx < sets.length - 1) setActiveIdx(activeIdx + 1);
          setIsResting(false);
          return 0;
        }
        return r - 1;
      });
    }, 1000);
    return () => clearInterval(id);
  }, [isResting, restRemaining, activeIdx, sets.length]);

  return (
    <div className="bg-slate-950 min-h-screen text-slate-50 pb-32 lg:pb-8">
      {/* Header */}
      <div className="sticky top-0 z-30 bg-slate-950/95 backdrop-blur border-b border-slate-800">
        <div className="max-w-7xl mx-auto px-4 lg:px-6 py-3 flex items-center justify-between">
          <a href="#" className="w-12 h-12 inline-flex items-center justify-center text-slate-300 hover:bg-slate-800 rounded-lg" aria-label="Quay lại">
            <Phosphor.ArrowLeft size={20} weight="bold" />
          </a>
          <div className="text-center flex-1">
            <p className="text-[10.5px] font-bold uppercase tracking-wider text-electric-400">Bài 3 / 8</p>
            <h1 className="text-[16px] font-extrabold text-slate-50">{SAMPLE.name}</h1>
          </div>
          <div className="flex items-center gap-1">
            <span className="text-[13px] font-bold text-slate-300 tabular-nums px-2">28:34</span>
            <button className="w-10 h-10 inline-flex items-center justify-center text-slate-300 hover:bg-slate-800 rounded-lg" aria-label="Chia sẻ workout">
              <Phosphor.ShareNetwork size={18} weight="bold" />
            </button>
            <button className="w-10 h-10 inline-flex items-center justify-center text-slate-300 hover:bg-slate-800 rounded-lg" aria-label="Cài đặt">
              <Phosphor.GearSix size={18} weight="bold" />
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 lg:px-6 py-5 lg:py-8 grid grid-cols-1 lg:grid-cols-12 gap-5 lg:gap-6">
        {/* Video + cues */}
        <div className="lg:col-span-7 space-y-3">
          <div className="relative aspect-video bg-slate-900 rounded-xl overflow-hidden border border-slate-800">
            <video
              poster={SAMPLE.posterUrl}
              preload="metadata"
              muted
              loop
              playsInline
              autoPlay
              className="w-full h-full object-cover"
            >
              <source src={SAMPLE.videoUrl} type="video/mp4" />
            </video>

            <div className="absolute bottom-3 left-3 right-3 flex items-center justify-between">
              <div className="flex items-center gap-1.5 px-2.5 py-1 bg-black/60 backdrop-blur rounded-full text-[11px] font-bold text-white">
                <div className="w-2 h-2 rounded-full bg-rose-500 animate-pulse" aria-hidden="true" />
                HD · 1080p
              </div>
              <button className="w-10 h-10 inline-flex items-center justify-center bg-black/60 backdrop-blur text-white hover:bg-black/80 rounded-full" aria-label="Bật/tắt âm thanh">
                <Phosphor.SpeakerSimpleHigh size={16} weight="bold" />
              </button>
            </div>
          </div>

          <ul className="space-y-1.5" aria-label="Form cues cho Bench Press">
            {SAMPLE.cues.map((cue, i) => (
              <li key={i} className="flex items-start gap-2 text-[12.5px] text-slate-300">
                <Phosphor.CheckCircle size={14} weight="fill" className="text-electric-400 flex-shrink-0 mt-0.5" />
                <span>{cue}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Set list + active input */}
        <div className="lg:col-span-5 space-y-4">
          {/* Active set panel */}
          {!isResting ? (
            <section
              aria-labelledby="active-set-heading"
              className="bg-gradient-to-br from-slate-900 to-slate-950 border-2 border-electric-500 rounded-2xl p-5 shadow-lg shadow-electric-500/20"
            >
              <p id="active-set-heading" className="text-[11px] font-bold uppercase tracking-wider text-electric-400 mb-3">
                Hiệp {activeSet.index} / {sets.length}
              </p>

              {/* Weight */}
              <div className="mb-4">
                <label htmlFor="weight-input" className="block text-[10.5px] font-bold uppercase tracking-wider text-slate-400 mb-2">
                  Trọng lượng
                </label>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => setSets(prev => prev.map((s, i) => i === activeIdx ? { ...s, weight: Math.max(0, s.weight - 2.5) } : s))}
                    className="w-14 h-14 bg-slate-800 hover:bg-slate-700 text-slate-50 rounded-xl flex items-center justify-center font-extrabold text-[20px] flex-shrink-0"
                    aria-label="Giảm trọng lượng 2,5kg"
                  >
                    <Phosphor.Minus size={20} weight="bold" />
                  </button>
                  <div className="flex-1 bg-slate-900 border border-slate-700 rounded-xl px-4 py-2 text-center">
                    <input
                      id="weight-input"
                      type="number"
                      value={activeSet.weight}
                      onChange={e => setSets(prev => prev.map((s, i) => i === activeIdx ? { ...s, weight: Number(e.target.value) } : s))}
                      className="w-full bg-transparent text-[36px] font-extrabold text-slate-50 tabular-nums text-center focus:outline-none"
                      aria-label={`Trọng lượng ${activeSet.weight} kg`}
                    />
                    <span className="text-[10.5px] font-bold text-slate-400 uppercase tracking-wider">kg</span>
                  </div>
                  <button
                    onClick={() => setSets(prev => prev.map((s, i) => i === activeIdx ? { ...s, weight: s.weight + 2.5 } : s))}
                    className="w-14 h-14 bg-slate-800 hover:bg-slate-700 text-slate-50 rounded-xl flex items-center justify-center font-extrabold text-[20px] flex-shrink-0"
                    aria-label="Tăng trọng lượng 2,5kg"
                  >
                    <Phosphor.Plus size={20} weight="bold" />
                  </button>
                </div>
              </div>

              {/* Reps */}
              <div className="mb-4">
                <label htmlFor="reps-input" className="block text-[10.5px] font-bold uppercase tracking-wider text-slate-400 mb-2">
                  Số lần
                </label>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => setSets(prev => prev.map((s, i) => i === activeIdx ? { ...s, reps: Math.max(0, s.reps - 1) } : s))}
                    className="w-14 h-14 bg-slate-800 hover:bg-slate-700 text-slate-50 rounded-xl flex items-center justify-center font-extrabold text-[20px]"
                    aria-label="Giảm 1 rep"
                  >
                    <Phosphor.Minus size={20} weight="bold" />
                  </button>
                  <div className="flex-1 bg-slate-900 border border-slate-700 rounded-xl px-4 py-2 text-center">
                    <input
                      id="reps-input"
                      type="number"
                      value={activeSet.reps}
                      onChange={e => setSets(prev => prev.map((s, i) => i === activeIdx ? { ...s, reps: Number(e.target.value) } : s))}
                      className="w-full bg-transparent text-[36px] font-extrabold text-slate-50 tabular-nums text-center focus:outline-none"
                      aria-label={`Số lần ${activeSet.reps}`}
                    />
                    <span className="text-[10.5px] font-bold text-slate-400 uppercase tracking-wider">reps</span>
                  </div>
                  <button
                    onClick={() => setSets(prev => prev.map((s, i) => i === activeIdx ? { ...s, reps: s.reps + 1 } : s))}
                    className="w-14 h-14 bg-slate-800 hover:bg-slate-700 text-slate-50 rounded-xl flex items-center justify-center font-extrabold text-[20px]"
                    aria-label="Tăng 1 rep"
                  >
                    <Phosphor.Plus size={20} weight="bold" />
                  </button>
                </div>
              </div>

              {/* RIR slider */}
              <div className="mb-5">
                <label htmlFor="rir-slider" className="block text-[10.5px] font-bold uppercase tracking-wider text-slate-400 mb-2">
                  RIR — Số rep còn lại trong bể
                </label>
                <div className="flex items-center gap-1" role="radiogroup" aria-label="RIR rating">
                  {[0, 1, 2, 3, 4].map(n => (
                    <button
                      key={n}
                      onClick={() => setSets(prev => prev.map((s, i) => i === activeIdx ? { ...s, rir: n } : s))}
                      role="radio"
                      aria-checked={activeSet.rir === n}
                      aria-label={`RIR ${n}`}
                      className={`flex-1 h-12 rounded-lg font-extrabold text-[14px] transition-colors ${
                        activeSet.rir === n ? 'bg-electric-500 text-slate-950 shadow-lg shadow-electric-500/40' : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
                      }`}
                    >
                      {n}
                    </button>
                  ))}
                </div>
              </div>

              {/* Complete set button */}
              <button
                onClick={completeSet}
                aria-keyshortcuts="Space"
                className="w-full h-20 bg-gradient-to-r from-electric-500 to-electric-400 hover:from-electric-400 hover:to-electric-500 text-slate-950 text-[16px] font-extrabold rounded-2xl shadow-xl shadow-electric-500/30 flex items-center justify-center gap-2"
              >
                <Phosphor.CheckCircle size={28} weight="fill" />
                HOÀN THÀNH HIỆP
                <span className="text-[10.5px] font-bold opacity-70 ml-1">(Space)</span>
              </button>
            </section>
          ) : (
            <RestTimer
              total={SAMPLE.restSeconds}
              remaining={restRemaining}
              onSkip={() => {
                if (activeIdx < sets.length - 1) setActiveIdx(activeIdx + 1);
                setIsResting(false);
              }}
              onAdd={s => setRestRemaining(r => r + s)}
            />
          )}

          {/* Set list */}
          <section aria-labelledby="sets-heading" className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
            <h2 id="sets-heading" className="text-[12px] font-bold uppercase tracking-wider text-slate-400 mb-3">
              Danh sách hiệp
            </h2>
            <ol className="space-y-2">
              {sets.map((s, i) => {
                const isActive = i === activeIdx && !s.completed;
                const Icon = s.completed ? (Phosphor.CheckCircle as any) : isActive ? (Phosphor.PlayCircle as any) : (Phosphor.Circle as any);
                return (
                  <li
                    key={s.index}
                    onClick={() => !s.completed && setActiveIdx(i)}
                    className={`flex items-center gap-3 p-3 rounded-lg cursor-pointer transition-colors ${
                      isActive ? 'bg-electric-500/10 border border-electric-500' : s.completed ? 'bg-slate-950/50' : 'bg-slate-950 hover:bg-slate-800'
                    }`}
                    aria-current={isActive ? 'true' : undefined}
                  >
                    <Icon
                      size={20}
                      weight={s.completed ? 'fill' : 'regular'}
                      className={s.completed ? 'text-electric-400' : isActive ? 'text-electric-400' : 'text-slate-500'}
                    />
                    <div className="flex-1">
                      <p className="text-[13.5px] font-extrabold text-slate-50 tabular-nums">
                        Hiệp {s.index}
                        {s.completed ? (
                          <span className="ml-2 text-slate-300"> · {s.weight}kg × {s.reps}</span>
                        ) : isActive ? (
                          <span className="ml-2 text-slate-300"> · {s.weight}kg × {s.reps}</span>
                        ) : (
                          <span className="ml-2 text-slate-500"> · ??</span>
                        )}
                      </p>
                      {s.completed && s.completedAt && (
                        <p className="text-[10.5px] text-slate-500">
                          RIR {s.rir} · {Math.round((Date.now() - s.completedAt.getTime()) / 60000)} phút trước
                        </p>
                      )}
                    </div>
                    {s.completed && (
                      <span className="text-[10.5px] font-bold text-electric-400">✓</span>
                    )}
                  </li>
                );
              })}
            </ol>
          </section>
        </div>
      </div>
    </div>
  );
}

function RestTimer({ total, remaining, onSkip, onAdd }: { total: number; remaining: number; onSkip: () => void; onAdd: (s: number) => void }) {
  const ratio = remaining / total;
  const colorClass = ratio > 0.33 ? 'text-electric-400' : ratio > 0.11 ? 'text-amber-400' : 'text-rose-400';
  const pulseClass = remaining <= 10 && remaining > 0 ? 'animate-pulse' : '';

  return (
    <section
      aria-labelledby="rest-heading"
      aria-live="polite"
      aria-atomic="true"
      className="bg-gradient-to-br from-slate-900 to-slate-950 border-2 border-electric-500 rounded-2xl p-8 shadow-2xl"
    >
      <p id="rest-heading" className="text-[11px] font-bold uppercase tracking-wider text-slate-400 mb-2 text-center">
        Nghỉ
      </p>
      <div className="text-center">
        <div className={`text-[96px] lg:text-[120px] font-extrabold tabular-nums leading-none tracking-tighter ${colorClass} ${pulseClass}`}>
          {Math.floor(remaining / 60)}:{(remaining % 60).toString().padStart(2, '0')}
        </div>
        <p className="text-[12px] text-slate-500 mt-2 tabular-nums">
          / {Math.floor(total / 60)}:{(total % 60).toString().padStart(2, '0')}
        </p>
      </div>

      <div className="mt-6 grid grid-cols-3 gap-2">
        <button
          onClick={() => onAdd(-15)}
          className="h-14 bg-slate-800 hover:bg-slate-700 text-slate-300 text-[12.5px] font-bold rounded-lg"
          aria-label="Giảm 15 giây"
        >
          −15s
        </button>
        <button
          onClick={onSkip}
          className="h-14 bg-rose-500 hover:bg-rose-400 text-white text-[12.5px] font-extrabold rounded-lg flex items-center justify-center gap-1"
          aria-label="Bỏ qua nghỉ và sang hiệp tiếp theo"
        >
          <Phosphor.SkipForward size={14} weight="bold" />
          BỎ QUA
        </button>
        <button
          onClick={() => onAdd(30)}
          className="h-14 bg-slate-800 hover:bg-slate-700 text-slate-300 text-[12.5px] font-bold rounded-lg"
          aria-label="Thêm 30 giây"
        >
          +30s
        </button>
      </div>
    </section>
  );
}
```

## 8. Accessibility

- Section `aria-labelledby`
- Set list `<ol>` semantic với `<li>`
- Active set `aria-current="true"`
- Complete button `aria-keyshortcuts="Space"`
- RIR slider `role="radiogroup"`
- Touch targets ≥ 56px cho controls, ≥ 64px cho primary CTA
- Rest timer color + pulse (không color-only)
- `prefers-reduced-motion` disable pulse
- Inputs có label + aria-label chi tiết
- Video `muted` + `playsInline` + `preload="metadata"`
- Form fields step rõ ràng

## 9. Performance

- Video lazy load qua `<video preload="metadata">`
- Auto-play muted để tiết kiệm bandwidth
- `setInterval` cleanup trong `useEffect`
- Sets immutable update
- No re-mount của set list

## 10. Anti-patterns đã tránh

- ❌ "Make every screen feel like..."
- ❌ Touch target < 44px (đã ≥ 56px)
- ❌ Color-only RIR (đã number + radio group)
- ❌ Rest timer spam aria-live every second (đã 30s interval)
- ❌ Video autoplay with sound (đã muted)
- ❌ No reduce-motion respect (đã disable pulse)
- ❌ Tiny input fields (đã 36px font, 14px touch height)

---

**Component family**: In-app Cockpit — `workout-screen`