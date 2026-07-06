import * as Phosphor from '@phosphor-icons/react';
import { HERO_HEADLINE, HERO_SUBHEAD, TRUST_LOGOS, STATS } from '@/data/hero';

export function Hero() {
  return (
    <section className="relative bg-ink-950 overflow-hidden">
      <div className="absolute inset-0 bg-grid opacity-30" aria-hidden="true" />
      <div className="absolute top-1/2 -translate-y-1/2 -left-40 w-96 h-96 bg-electric-500/10 rounded-full blur-3xl" aria-hidden="true" />
      <div className="absolute bottom-0 right-0 w-96 h-96 bg-electric-500/5 rounded-full blur-3xl" aria-hidden="true" />

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-12 lg:pt-20 pb-16 lg:pb-20">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 lg:gap-16 items-center">
          {/* Copy */}
          <div className="lg:col-span-6">
            <span className="inline-flex items-center gap-1.5 px-3 py-1 bg-electric-500/10 border border-electric-500/30 text-electric-400 text-[11px] font-bold uppercase tracking-wider rounded-full mb-5">
              <Phosphor.Sparkle size={11} weight="fill" />
              App #1 cho gymer Việt · 2026
            </span>

            <h1 className="text-5xl lg:text-7xl font-display text-ink-50 leading-[0.95] tracking-tight">
              {HERO_HEADLINE.split('.').map((part, i) => (
                <span key={i} className="block">
                  {part.trim()}
                  {i === 0 && <span className="text-electric-400">.</span>}
                </span>
              ))}
            </h1>

            <p className="mt-5 text-[16px] lg:text-[18px] text-slate-300 leading-relaxed max-w-xl">
              {HERO_SUBHEAD}
            </p>

            <div className="mt-7 flex flex-wrap items-center gap-3">
              <a href="/download" className="inline-flex items-center gap-2 px-6 py-3.5 bg-electric-500 hover:bg-electric-400 text-ink-950 text-[14px] font-extrabold rounded-lg shadow-lg shadow-electric-500/30">
                <Phosphor.AppleLogo size={16} weight="bold" />
                Tải cho iPhone
                <span className="text-[11px] font-bold opacity-70">v6.2 · 89MB</span>
              </a>
              <a href="/download/android" className="inline-flex items-center gap-2 px-6 py-3.5 bg-ink-800 hover:bg-ink-700 text-ink-50 text-[14px] font-bold border border-ink-700 rounded-lg">
                <Phosphor.Download size={14} weight="bold" />
                Android
              </a>
              <a href="/demo" className="px-6 py-3.5 text-[14px] font-bold text-slate-300 hover:text-electric-400">
                Xem demo →
              </a>
            </div>

            <ul className="mt-7 flex flex-wrap items-center gap-x-5 gap-y-2 text-[12.5px] text-slate-400">
              <li className="inline-flex items-center gap-1.5">
                <Phosphor.CheckCircle size={13} weight="fill" className="text-electric-400" />
                Free 14-day Pro
              </li>
              <li className="inline-flex items-center gap-1.5">
                <Phosphor.CheckCircle size={13} weight="fill" className="text-electric-400" />
                Sync Apple Watch + Strava
              </li>
              <li className="inline-flex items-center gap-1.5">
                <Phosphor.CheckCircle size={13} weight="fill" className="text-electric-400" />
                Privacy-first
              </li>
            </ul>

            {/* Stats */}
            <div className="mt-10 grid grid-cols-4 gap-4">
              {STATS.map(s => (
                <div key={s.label}>
                  <p className="text-[26px] lg:text-[32px] font-display text-electric-400 leading-none tabular-nums">{s.value}</p>
                  <p className="mt-1 text-[11px] font-bold text-slate-500 uppercase tracking-wider">{s.label}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Watch mock */}
          <div className="lg:col-span-6">
            <WatchMock />
          </div>
        </div>
      </div>

      <TrustStrip />
    </section>
  );
}

function WatchMock() {
  return (
    <div className="relative flex items-center justify-center">
      <div className="absolute inset-0 bg-electric-500/20 blur-3xl rounded-full" aria-hidden="true" />

      {/* Watch */}
      <div className="relative">
        {/* Watch body */}
        <div className="relative w-72 lg:w-80 h-80 lg:h-96 bg-gradient-to-br from-ink-800 to-ink-900 rounded-[3rem] p-3 shadow-2xl shadow-black/50 border border-ink-700">
          <div className="relative w-full h-full bg-black rounded-[2.5rem] overflow-hidden flex flex-col p-5">
            <p className="text-[10px] font-bold uppercase tracking-wider text-electric-400">Bench Press · Set 3</p>

            <div className="flex-1 flex flex-col items-center justify-center">
              <p className="text-[12px] font-bold text-slate-400">Trọng lượng</p>
              <p className="text-[80px] font-display text-ink-50 leading-none tabular-nums">100</p>
              <p className="text-[14px] font-bold text-slate-400 uppercase tracking-wider">kg × 6 reps</p>

              <div className="mt-4 flex items-center gap-1.5">
                <div className="w-2 h-2 rounded-full bg-rose-500 animate-pulse" aria-hidden="true" />
                <span className="text-[11px] font-bold text-electric-400 tabular-nums">RIR 2</span>
              </div>
            </div>

            <div className="grid grid-cols-3 gap-2">
              <button className="h-12 bg-ink-800 rounded-lg text-ink-50 text-[18px] font-extrabold">−</button>
              <button className="h-12 bg-electric-500 rounded-lg text-ink-950 text-[12px] font-extrabold flex items-center justify-center">
                <Phosphor.Check size={20} weight="bold" />
              </button>
              <button className="h-12 bg-ink-800 rounded-lg text-ink-50 text-[18px] font-extrabold">+</button>
            </div>
          </div>

          {/* Crown */}
          <div className="absolute right-[-6px] top-1/3 w-3 h-16 bg-ink-700 rounded-r-md" />
          <div className="absolute right-[-4px] bottom-1/3 w-3 h-10 bg-ink-700 rounded-r-md" />
        </div>

        {/* Floating badge */}
        <div className="absolute -left-8 top-1/4 bg-electric-500 text-ink-950 px-4 py-2.5 rounded-2xl shadow-xl shadow-electric-500/30 flex items-center gap-2 animate-pulse">
          <Phosphor.Trophy size={16} weight="fill" />
          <span className="text-[12px] font-extrabold uppercase tracking-wider">PR mới!</span>
        </div>

        {/* Heart rate badge */}
        <div className="absolute -right-6 bottom-1/4 bg-ink-800 border border-ink-700 px-3 py-2.5 rounded-xl shadow-xl">
          <p className="text-[9px] font-bold uppercase tracking-wider text-slate-400">Heart rate</p>
          <p className="text-[18px] font-display text-rose-500 tabular-nums flex items-center gap-1">
            <Phosphor.Heart size={14} weight="fill" />
            142
          </p>
        </div>
      </div>
    </div>
  );
}

function TrustStrip() {
  return (
    <div className="relative border-t border-ink-800 py-8 bg-ink-950">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <p className="text-center text-[11px] font-bold uppercase tracking-[0.18em] text-slate-500 mb-5">
          Đồng bộ với thiết bị bạn đang dùng
        </p>
        <div className="grid grid-cols-3 md:grid-cols-6 gap-6 items-center justify-items-center opacity-60 grayscale">
          {TRUST_LOGOS.map(l => (
            <img
              key={l.slug}
              src={`https://cdn.simpleicons.org/${l.slug}/94a3b8`}
              alt={l.name}
              className="h-6 w-auto object-contain"
              loading="lazy"
            />
          ))}
        </div>
      </div>
    </div>
  );
}