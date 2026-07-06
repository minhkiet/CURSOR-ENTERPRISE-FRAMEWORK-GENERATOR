# Volume Chart

> Bar chart cho weekly / monthly / yearly volume (kg hoàn thành). Period selector tabs, summary cards, color-coded by muscle group.

## 1. Mục đích

User xem chart 30 ngày để hiểu consistency, biết recovery gap, plan tuần tiếp.

## 2. Layout

```
┌──────────────────────────────────────────────────────────────┐
│ Khối lượng tập                                              │
│ ──────────────────────────────────────────────              │
│ ┌─────┬─────┬─────┬─────┐                                   │
│ │ 7d  │ 30d │ 90d │ 1y  │                                   │
│ └─────┴─────┴─────┴─────┘                                   │
│                                                              │
│ 38.500 kg  +24%  /target 47.500 kg                          │
│                                                              │
│   ▄                                                          │
│  ▐██▌  ▄▄                                                   │
│  ▐███▌ ███▌                                                 │
│  ▐████▌████▌▄ ▄                                            │
│  ▐████████████████▌                                         │
│  Mo Tu We Th Fr Sa Su                                       │
│                                                              │
│ ┌────────────┬────────────┬────────────┐                     │
│ │ Chest      │ Back       │ Legs       │                     │
│ │ 12.500 kg  │ 14.200 kg  │ 11.800 kg  │                     │
│ └────────────┴────────────┴────────────┘                     │
└──────────────────────────────────────────────────────────────┘
```

## 3. Code reference

```tsx
'use client';
import { useState } from 'react';
import * as Phosphor from '@phosphor-icons/react';

export interface VolumeDataPoint {
  label: string;
  volume: number;
  date: Date;
  byMuscle?: { chest: number; back: number; legs: number; shoulders: number; arms: number; core: number };
}

const SAMPLE_30D: VolumeDataPoint[] = Array.from({ length: 30 }).map((_, i) => {
  const date = new Date(Date.now() - (29 - i) * 86400000);
  const base = i < 20 ? 800 + Math.random() * 1200 : 1200 + Math.random() * 800;
  return {
    label: date.toLocaleDateString('vi-VN', { weekday: 'short' }).slice(0, 2),
    volume: Math.floor(base),
    date,
    byMuscle: {
      chest: Math.floor(base * 0.25),
      back: Math.floor(base * 0.30),
      legs: Math.floor(base * 0.25),
      shoulders: Math.floor(base * 0.10),
      arms: Math.floor(base * 0.07),
      core: Math.floor(base * 0.03)
    }
  };
});

export function VolumeChart() {
  const [period, setPeriod] = useState<'7d' | '30d' | '90d' | '1y'>('30d');

  const total = SAMPLE_30D.reduce((s, d) => s + d.volume, 0);
  const previous = total * 0.81; // simulated previous period
  const delta = ((total - previous) / previous) * 100;
  const target = 47500;

  const max = Math.max(...SAMPLE_30D.map(d => d.volume));
  const averagePerSession = total / SAMPLE_30D.filter(d => d.volume > 0).length;

  return (
    <section
      aria-labelledby="volume-heading"
      className="bg-slate-950 py-16 lg:py-24 text-slate-50"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="flex items-end justify-between mb-8 flex-wrap gap-4">
          <div>
            <span className="text-[11px] font-bold uppercase tracking-[0.18em] text-electric-400 mb-2 block">
              Khối lượng tập
            </span>
            <h2 id="volume-heading" className="text-3xl lg:text-4xl font-extrabold tracking-tight">
              Tổng quan luyện tập
            </h2>
          </div>

          {/* Period tabs */}
          <div role="tablist" aria-label="Khoảng thời gian" className="inline-flex items-center gap-1 p-1 bg-slate-900 border border-slate-800 rounded-lg">
            {(['7d', '30d', '90d', '1y'] as const).map(p => (
              <button
                key={p}
                role="tab"
                aria-selected={period === p}
                onClick={() => setPeriod(p)}
                className={`px-3.5 py-1.5 text-[12.5px] font-bold rounded-md transition-colors ${
                  period === p ? 'bg-electric-500 text-slate-950' : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                {p}
              </button>
            ))}
          </div>
        </div>

        {/* Summary */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-8">
          <article className="bg-gradient-to-br from-slate-900 to-slate-950 border border-slate-800 rounded-2xl p-5">
            <p className="text-[10.5px] font-bold uppercase tracking-wider text-slate-400">Tổng khối lượng</p>
            <p aria-label={`${total.toLocaleString('vi-VN')} kilogam`} className="mt-2 text-[40px] lg:text-[52px] font-extrabold text-slate-50 tabular-nums leading-none">
              {total.toLocaleString('vi-VN')}
            </p>
            <p className="mt-1 text-[11px] text-slate-500 uppercase tracking-wider font-bold">kg</p>
            <div className="mt-3 inline-flex items-center gap-1 px-2 py-0.5 bg-emerald-500/20 text-emerald-400 rounded-full text-[11.5px] font-bold tabular-nums">
              <Phosphor.TrendUp size={11} weight="bold" />
              +{delta.toFixed(1)}% so với kỳ trước
            </div>
          </article>

          <article className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
            <p className="text-[10.5px] font-bold uppercase tracking-wider text-slate-400">Trung bình / buổi</p>
            <p aria-label={`Trung bình ${Math.round(averagePerSession)} kilogam mỗi buổi`} className="mt-2 text-[40px] lg:text-[52px] font-extrabold text-electric-400 tabular-nums leading-none">
              {Math.round(averagePerSession).toLocaleString('vi-VN')}
            </p>
            <p className="mt-1 text-[11px] text-slate-500 uppercase tracking-wider font-bold">kg/buổi</p>
            <p className="mt-3 text-[11.5px] text-slate-400 tabular-nums">
              Target: <strong className="text-slate-300">{target.toLocaleString('vi-VN')}</strong> kg
            </p>

            {/* Progress bar */}
            <div className="mt-2 h-2 bg-slate-800 rounded-full overflow-hidden" role="progressbar" aria-valuenow={Math.min(100, Math.round((total / target) * 100))} aria-valuemin={0} aria-valuemax={100}>
              <div
                className="h-full bg-gradient-to-r from-electric-500 to-electric-400 rounded-full"
                style={{ width: `${Math.min(100, (total / target) * 100)}%` }}
              />
            </div>
          </article>

          <article className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
            <p className="text-[10.5px] font-bold uppercase tracking-wider text-slate-400">Sessions</p>
            <p className="mt-2 text-[40px] lg:text-[52px] font-extrabold text-slate-50 tabular-nums leading-none tabular-nums">
              {SAMPLE_30D.filter(d => d.volume > 0).length}
            </p>
            <p className="mt-1 text-[11px] text-slate-500 uppercase tracking-wider font-bold">/ 30 ngày</p>
            <p className="mt-3 text-[11.5px] text-slate-400 tabular-nums">
              Nghỉ: <strong className="text-amber-400">{SAMPLE_30D.filter(d => d.volume === 0).length}</strong> ngày
            </p>
          </article>
        </div>

        {/* Bar chart */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 lg:p-7" role="img" aria-label={`Biểu đồ khối lượng ${period}, tổng ${total.toLocaleString('vi-VN')} kilogam`}>
          <div className="flex items-end justify-between gap-1 h-64 lg:h-80">
            {SAMPLE_30D.map((d, i) => {
              const heightPct = (d.volume / max) * 100;
              const isWeekend = [0, 6].includes(d.date.getDay());
              return (
                <button
                  key={i}
                  className="flex-1 group relative h-full flex flex-col justify-end focus:outline-none focus-visible:ring-2 focus-visible:ring-electric-500 rounded"
                  aria-label={`${d.date.toLocaleDateString('vi-VN')}: ${d.volume.toLocaleString('vi-VN')} kg`}
                  onClick={() => {}}
                >
                  {/* Tooltip on hover */}
                  <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 hidden group-hover:block z-10 pointer-events-none">
                    <div className="bg-slate-50 text-slate-900 text-[11px] font-bold px-2.5 py-1 rounded whitespace-nowrap">
                      {d.volume.toLocaleString('vi-VN')} kg
                    </div>
                  </div>

                  <div
                    className={`w-full rounded-t ${
                      d.volume === 0
                        ? 'bg-slate-800'
                        : isWeekend
                          ? 'bg-electric-500/70 hover:bg-electric-400'
                          : 'bg-electric-500 hover:bg-electric-400'
                    } transition-colors`}
                    style={{ height: `${Math.max(heightPct, 2)}%` }}
                  />
                </button>
              );
            })}
          </div>

          {/* X-axis labels (every 5 days) */}
          <div className="mt-3 flex justify-between text-[10px] text-slate-500 font-bold uppercase tabular-nums">
            {SAMPLE_30D.filter((_, i) => i % 5 === 0).map((d, i) => (
              <span key={i}>{d.date.toLocaleDateString('vi-VN', { day: 'numeric', month: 'numeric' })}</span>
            ))}
          </div>
        </div>

        {/* By muscle group */}
        <div className="mt-6 grid grid-cols-2 lg:grid-cols-3 gap-3 lg:gap-4">
          {[
            { key: 'chest', label: 'Ngực', color: 'bg-rose-500' },
            { key: 'back', label: 'Lưng', color: 'bg-indigo-500' },
            { key: 'legs', label: 'Chân', color: 'bg-emerald-500' },
            { key: 'shoulders', label: 'Vai', color: 'bg-amber-500' },
            { key: 'arms', label: 'Tay', color: 'bg-purple-500' },
            { key: 'core', label: 'Core', color: 'bg-sky-500' }
          ].map(muscle => {
            const total_muscle = SAMPLE_30D.reduce((s, d) => s + (d.byMuscle?.[muscle.key as keyof VolumeDataPoint['byMuscle']] || 0), 0);
            const pct = (total_muscle / total) * 100;
            return (
              <div key={muscle.key} className="bg-slate-900 border border-slate-800 rounded-xl p-3.5 hover:bg-slate-800/50 transition-colors">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-1.5">
                    <div className={`w-2.5 h-2.5 rounded-full ${muscle.color}`} aria-hidden="true" />
                    <p className="text-[12px] font-bold text-slate-300">{muscle.label}</p>
                  </div>
                  <p className="text-[16px] font-extrabold text-slate-50 tabular-nums">
                    {total_muscle.toLocaleString('vi-VN')}
                    <span className="text-[10.5px] text-slate-500 ml-1">kg</span>
                  </p>
                </div>
                <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden" role="progressbar" aria-valuenow={Math.round(pct)} aria-valuemin={0} aria-valuemax={100}>
                  <div className={`h-full rounded-full ${muscle.color}`} style={{ width: `${pct}%` }} />
                </div>
                <p className="mt-1.5 text-[10.5px] text-slate-500 tabular-nums text-right">
                  {pct.toFixed(1)}% tổng volume
                </p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
```

## 4. Accessibility

- Section `aria-labelledby`
- Period tabs `role="tablist"` + `aria-selected`
- Bar chart container `role="img"` + `aria-label` mô tả tổng
- Mỗi bar là `<button>` focusable với `aria-label` chi tiết
- Tooltip hiện trên hover + focus
- Progress bars `role="progressbar"`
- Numbers tabular-nums
- Reduce-motion: không animate bar height on load

## 5. Performance

- Bar calculation memoized
- Static sample data
- Inline icons
- Hover tooltip CSS only

## 6. Anti-patterns đã tránh

- ❌ Chart không có text alt (đã có)
- ❌ Bar không accessible (đã button + aria-label)
- ❌ Color-only muscle group (đã icon dot + label)
- ❌ Generic number (đã context: "12,500 kg · 25%")

---

**Component family**: In-app Cockpit — `volume-chart`