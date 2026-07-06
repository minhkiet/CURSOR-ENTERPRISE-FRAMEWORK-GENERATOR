'use client';
import { useState } from 'react';
import * as Phosphor from '@phosphor-icons/react';
import { VOLUME_DATA_30D } from '@/data/pr';

export function VolumeChart() {
  const [period, setPeriod] = useState<'7d' | '30d' | '90d' | '1y'>('30d');

  const total = VOLUME_DATA_30D.reduce((s, d) => s + d.volume, 0);
  const previous = total * 0.81;
  const delta = ((total - previous) / previous) * 100;
  const target = 47500;
  const sessions = VOLUME_DATA_30D.filter(d => d.volume > 0).length;
  const restDays = VOLUME_DATA_30D.filter(d => d.volume === 0).length;
  const avgPerSession = total / sessions;

  const max = Math.max(...VOLUME_DATA_30D.map(d => d.volume));

  return (
    <section className="bg-ink-900 py-16 lg:py-24 text-ink-50 border-t border-ink-800" aria-labelledby="volume-heading">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-end justify-between mb-8 flex-wrap gap-4">
          <div>
            <span className="text-[11px] font-bold uppercase tracking-[0.18em] text-electric-400 mb-2 block">
              Volume analytics
            </span>
            <h2 id="volume-heading" className="text-3xl lg:text-4xl font-display tracking-tight">
              Theo dõi khối lượng. <span className="text-electric-400">Tối ưu progression.</span>
            </h2>
          </div>

          <div role="tablist" aria-label="Khoảng thời gian" className="inline-flex items-center gap-1 p-1 bg-ink-950 border border-ink-800 rounded-lg">
            {(['7d', '30d', '90d', '1y'] as const).map(p => (
              <button
                key={p}
                role="tab"
                aria-selected={period === p}
                onClick={() => setPeriod(p)}
                className={`px-3.5 py-1.5 text-[12.5px] font-extrabold rounded-md transition-colors ${
                  period === p ? 'bg-electric-500 text-ink-950' : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                {p}
              </button>
            ))}
          </div>
        </div>

        {/* Summary */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-8">
          <article className="bg-gradient-to-br from-ink-950 to-ink-900 border border-ink-800 rounded-2xl p-5">
            <p className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Tổng khối lượng</p>
            <p className="mt-2 text-[40px] lg:text-[52px] font-display text-ink-50 tabular-nums leading-none">{total.toLocaleString('vi-VN')}</p>
            <p className="mt-1 text-[10px] text-slate-500 uppercase tracking-wider font-bold">kg</p>
            <div className="mt-3 inline-flex items-center gap-1 px-2 py-0.5 bg-emerald-500/20 text-emerald-400 rounded-full text-[11.5px] font-extrabold tabular-nums">
              <Phosphor.TrendUp size={11} weight="bold" />
              +{delta.toFixed(1)}% so với kỳ trước
            </div>
          </article>

          <article className="bg-ink-950 border border-ink-800 rounded-2xl p-5">
            <p className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Trung bình / buổi</p>
            <p className="mt-2 text-[40px] lg:text-[52px] font-display text-electric-400 tabular-nums leading-none">{Math.round(avgPerSession).toLocaleString('vi-VN')}</p>
            <p className="mt-1 text-[10px] text-slate-500 uppercase tracking-wider font-bold">kg/buổi</p>
            <p className="mt-3 text-[11px] text-slate-400 tabular-nums">Target: <strong className="text-slate-300">{target.toLocaleString('vi-VN')}</strong> kg</p>
            <div className="mt-2 h-2 bg-ink-800 rounded-full overflow-hidden" role="progressbar" aria-valuenow={Math.round((total / target) * 100)} aria-valuemin={0} aria-valuemax={100}>
              <div className="h-full bg-gradient-to-r from-electric-500 to-electric-400 rounded-full" style={{ width: `${Math.min(100, (total / target) * 100)}%` }} />
            </div>
          </article>

          <article className="bg-ink-950 border border-ink-800 rounded-2xl p-5">
            <p className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Sessions</p>
            <p className="mt-2 text-[40px] lg:text-[52px] font-display text-ink-50 tabular-nums leading-none">{sessions}</p>
            <p className="mt-1 text-[10px] text-slate-500 uppercase tracking-wider font-bold">/ 30 ngày</p>
            <p className="mt-3 text-[11px] text-slate-400 tabular-nums">Nghỉ: <strong className="text-amber-400">{restDays}</strong> ngày</p>
          </article>
        </div>

        {/* Bar chart */}
        <div className="bg-ink-950 border border-ink-800 rounded-2xl p-5 lg:p-7" role="img" aria-label={`Biểu đồ khối lượng ${period}, tổng ${total.toLocaleString('vi-VN')} kilogam`}>
          <div className="flex items-end justify-between gap-1 h-64 lg:h-80">
            {VOLUME_DATA_30D.map((d, i) => {
              const heightPct = (d.volume / max) * 100;
              const isWeekend = [0, 6].includes(d.date.getDay());
              return (
                <button
                  key={i}
                  className="flex-1 group relative h-full flex flex-col justify-end focus:outline-none focus-visible:ring-2 focus-visible:ring-electric-500 rounded"
                  aria-label={`${d.date.toLocaleDateString('vi-VN')}: ${d.volume.toLocaleString('vi-VN')} kg`}
                >
                  <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 hidden group-hover:block z-10 pointer-events-none">
                    <div className="bg-ink-50 text-ink-950 text-[11px] font-bold px-2.5 py-1 rounded whitespace-nowrap">{d.volume.toLocaleString('vi-VN')} kg</div>
                  </div>
                  <div
                    className={`w-full rounded-t ${
                      d.volume === 0 ? 'bg-ink-800' : isWeekend ? 'bg-electric-500/70 hover:bg-electric-400' : 'bg-electric-500 hover:bg-electric-400'
                    } transition-colors`}
                    style={{ height: `${Math.max(heightPct, 2)}%` }}
                  />
                </button>
              );
            })}
          </div>

          <div className="mt-3 flex justify-between text-[10px] text-slate-500 font-bold uppercase tabular-nums">
            {VOLUME_DATA_30D.filter((_, i) => i % 5 === 0).map((d, i) => (
              <span key={i}>{d.date.toLocaleDateString('vi-VN', { day: 'numeric', month: 'numeric' })}</span>
            ))}
          </div>
        </div>

        {/* By muscle */}
        <div className="mt-6 grid grid-cols-2 lg:grid-cols-3 gap-3 lg:gap-4">
          {[
            { key: 'chest', label: 'Ngực', color: 'bg-rose-500' },
            { key: 'back', label: 'Lưng', color: 'bg-indigo-500' },
            { key: 'legs', label: 'Chân', color: 'bg-emerald-500' },
            { key: 'shoulders', label: 'Vai', color: 'bg-amber-500' },
            { key: 'arms', label: 'Tay', color: 'bg-purple-500' },
            { key: 'core', label: 'Core', color: 'bg-sky-500' }
          ].map(muscle => {
            const total_m = VOLUME_DATA_30D.reduce((s, d) => s + (d.byMuscle?.[muscle.key as keyof typeof d.byMuscle] || 0), 0);
            const pct = (total_m / total) * 100;
            return (
              <div key={muscle.key} className="bg-ink-950 border border-ink-800 rounded-xl p-3.5 hover:bg-ink-800/50 transition-colors">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-1.5">
                    <div className={`w-2.5 h-2.5 rounded-full ${muscle.color}`} aria-hidden="true" />
                    <p className="text-[12px] font-bold text-slate-300">{muscle.label}</p>
                  </div>
                  <p className="text-[16px] font-display text-ink-50 tabular-nums">
                    {total_m.toLocaleString('vi-VN')}<span className="text-[10px] text-slate-500 ml-1">kg</span>
                  </p>
                </div>
                <div className="h-1.5 bg-ink-800 rounded-full overflow-hidden" role="progressbar" aria-valuenow={Math.round(pct)} aria-valuemin={0} aria-valuemax={100}>
                  <div className={`h-full rounded-full ${muscle.color}`} style={{ width: `${pct}%` }} />
                </div>
                <p className="mt-1.5 text-[10px] text-slate-500 tabular-nums text-right">{pct.toFixed(1)}% tổng volume</p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}