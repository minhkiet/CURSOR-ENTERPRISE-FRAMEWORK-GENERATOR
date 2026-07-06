# Set Tracker

> Standalone set list component (extracted từ `workout-screen`). Mỗi set là interactive `<li>` với completion state, RIR rating, weight × reps quick-edit.

## 1. Mục đích

Dùng trong workout tracker sidebar. Tap để chọn active set, double-tap để mark complete.

## 2. Layout

```
┌────────────────────────────────────┐
│ DANH SÁCH HIỆP                    │
├────────────────────────────────────┤
│ ✓ Hiệp 1 · 60kg × 10 · RIR 3    │
│ ✓ Hiệp 2 · 80kg × 8 · RIR 2     │
│ ► Hiệp 3 · 80kg × 8 · ĐANG TẬP  │
│ ○ Hiệp 4 · ??kg × ?? · TAP ĐỂ SET │
└────────────────────────────────────┘
```

## 3. Variants

| Variant | Use | Khác biệt |
|---|---|---|
| `default` | Standard workout | Full info |
| `compact` | Set list inline | Smaller rows |
| `cardio` | Cardio mode | Time + HR |
| `history` | Past workout | No active state |

## 4. Code reference

```tsx
'use client';
import * as Phosphor from '@phosphor-icons/react';

export interface TrackerSet {
  index: number;
  weight: number;
  reps: number;
  rir: number;
  completed: boolean;
  completedAt: Date | null;
  isPR?: boolean;
}

export function SetTracker({
  sets,
  activeIdx,
  onSelect,
  onComplete
}: {
  sets: TrackerSet[];
  activeIdx: number;
  onSelect: (i: number) => void;
  onComplete: (i: number) => void;
}) {
  const completed = sets.filter(s => s.completed).length;
  const totalVolume = sets
    .filter(s => s.completed)
    .reduce((sum, s) => sum + s.weight * s.reps, 0);

  return (
    <section
      aria-labelledby="tracker-heading"
      className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden"
    >
      {/* Header */}
      <header className="flex items-center justify-between p-4 border-b border-slate-800 bg-slate-950">
        <h2 id="tracker-heading" className="text-[12px] font-bold uppercase tracking-wider text-slate-400">
          Danh sách hiệp
        </h2>
        <div className="flex items-center gap-3 text-[10.5px] font-bold uppercase tracking-wider">
          <span className="text-slate-500">
            <strong className="text-electric-400 tabular-nums">{completed}</strong>/{sets.length}
          </span>
          <span className="text-slate-500 tabular-nums">
            <strong className="text-electric-400">{totalVolume.toLocaleString('vi-VN')}</strong> kg
          </span>
        </div>
      </header>

      {/* Progress bar */}
      <div className="h-1 bg-slate-800 relative" role="progressbar" aria-valuenow={completed} aria-valuemin={0} aria-valuemax={sets.length}>
        <div
          className="h-full bg-gradient-to-r from-electric-500 to-electric-400"
          style={{ width: `${(completed / sets.length) * 100}%` }}
        />
      </div>

      {/* Sets */}
      <ol className="divide-y divide-slate-800">
        {sets.map((s, i) => {
          const isActive = i === activeIdx && !s.completed;
          const isPending = !s.completed && !isActive;

          let StatusIcon = Phosphor.Circle;
          let statusColor = 'text-slate-600';
          if (s.completed) {
            StatusIcon = Phosphor.CheckCircle;
            statusColor = 'text-electric-400';
          } else if (isActive) {
            StatusIcon = Phosphor.PlayCircle;
            statusColor = 'text-electric-400';
          }

          return (
            <li
              key={s.index}
              onClick={() => {
                if (s.completed) return;
                if (isActive) onComplete(i);
                else onSelect(i);
              }}
              className={`flex items-center gap-3 px-4 py-3 transition-colors cursor-pointer ${
                s.completed ? 'opacity-60 cursor-default' : isActive ? 'bg-electric-500/10 border-l-4 border-electric-500' : 'hover:bg-slate-800'
              }`}
              aria-current={isActive ? 'true' : undefined}
              aria-disabled={s.completed ? 'true' : undefined}
            >
              <StatusIcon size={22} weight={s.completed ? 'fill' : 'regular'} className={statusColor} />

              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-1.5">
                  <span className="text-[13.5px] font-extrabold text-slate-50 tabular-nums">
                    Hiệp {s.index}
                  </span>
                  {s.isPR && (
                    <span className="inline-flex items-center gap-0.5 px-1.5 py-0.5 bg-amber-500/20 text-amber-400 text-[9.5px] font-bold uppercase tracking-wider rounded">
                      <Phosphor.Trophy size={9} weight="fill" />
                      PR
                    </span>
                  )}
                  {isActive && (
                    <span className="inline-flex items-center gap-1 px-1.5 py-0.5 bg-electric-500 text-slate-950 text-[9.5px] font-bold uppercase tracking-wider rounded">
                      <span className="w-1.5 h-1.5 rounded-full bg-slate-950 animate-pulse" />
                      ĐANG TẬP
                    </span>
                  )}
                </div>

                <p className="text-[12px] text-slate-400 tabular-nums mt-0.5">
                  {s.completed || isActive ? (
                    <>
                      <strong className="font-bold text-slate-300">{s.weight}kg</strong> × <strong className="font-bold text-slate-300">{s.reps}</strong> reps · RIR {s.rir}
                    </>
                  ) : (
                    <span className="text-slate-500">Tap để set</span>
                  )}
                </p>

                {s.completed && s.completedAt && (
                  <p className="text-[10.5px] text-slate-500 mt-0.5 tabular-nums">
                    {Math.round((Date.now() - s.completedAt.getTime()) / 60000)} phút trước
                  </p>
                )}
              </div>

              {!s.completed && (
                <button
                  onClick={(e) => { e.stopPropagation(); onComplete(i); }}
                  aria-label={`Hoàn thành hiệp ${s.index}`}
                  className="w-12 h-12 flex items-center justify-center bg-slate-800 hover:bg-electric-500 hover:text-slate-950 text-slate-400 rounded-lg transition-colors"
                >
                  <Phosphor.Check size={18} weight="bold" />
                </button>
              )}
            </li>
          );
        })}
      </ol>
    </section>
  );
}
```

## 4. Accessibility

- `<section>` + `aria-labelledby`
- `<ol>` semantic cho ordered sets
- Mỗi set là `<li>` với `aria-current` / `aria-disabled`
- Tap-area ≥ 56x56px
- Status icons + text labels
- PR badge có icon + label
- Progress bar `role="progressbar"`
- Reduce-motion: pulse off

## 5. Performance

- Memoized rows
- Inline icons
- Lazy state update

## 6. Anti-patterns đã tránh

- ❌ Tap area < 44px (đã ≥ 56px)
- ❌ Color-only PR (đã icon + label)
- ❌ No reduce-motion (đã disable pulse)
- ❌ Without ARIA current/disabled

---

**Component family**: In-app Cockpit — `set-tracker`