import * as Phosphor from '@phosphor-icons/react';
import { KPI_MAIN, KPIS_SECONDARY, SPARKLINE_POINTS, ACTIVITY_FEED, STUCK_DEALS } from '@/data/dashboard';

export function DashboardShowcase() {
  return (
    <section id="dashboard" className="bg-slate-950 py-16 lg:py-24" aria-labelledby="dashboard-heading">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="max-w-2xl mb-12">
          <span className="inline-block text-[11px] font-bold uppercase tracking-[0.18em] text-indigo-400 mb-2">
            Dashboard cockpit
          </span>
          <h2 id="dashboard-heading" className="text-3xl lg:text-5xl font-extrabold text-white tracking-tight leading-tight">
            Nhìn toàn cảnh pipeline trong 5 giây
          </h2>
          <p className="mt-3 text-slate-300 text-[15px]">
            KPI chính · Sparkline 12 tuần · Activity feed · Stuck deals alert. Một màn hình cho toàn bộ tình hình sales.
          </p>
        </div>

        {/* Bento grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-4 lg:auto-rows-[140px]">
          {/* Hero KPI */}
          <article className="lg:col-span-3 lg:row-span-2 bg-gradient-to-br from-indigo-600 to-indigo-800 text-white rounded-2xl p-6 shadow-xl">
            <div className="flex items-center gap-2 mb-2">
              <Phosphor.CurrencyDollar size={18} weight="bold" className="text-indigo-200" />
              <span className="text-[11px] font-bold uppercase tracking-wider text-indigo-200">{KPI_MAIN.subtitle}</span>
            </div>
            <p className="text-[44px] lg:text-[56px] font-extrabold tabular-nums leading-none tracking-tight">
              {KPI_MAIN.revenue} <span className="text-[24px] text-indigo-200 font-bold">{KPI_MAIN.revenueUnit}</span>
            </p>
            <div className="mt-2 inline-flex items-center gap-1 px-2 py-0.5 bg-emerald-500/20 text-emerald-300 rounded-full text-[12px] font-bold">
              <Phosphor.TrendUp size={11} weight="bold" />
              {KPI_MAIN.delta} {KPI_MAIN.deltaLabel}
            </div>

            {/* Sparkline */}
            <div className="mt-6" aria-label={`Revenue 12 tuần tăng ${KPI_MAIN.delta}`}>
              <svg viewBox="0 0 200 60" className="w-full h-16" role="img">
                <polyline points={SPARKLINE_POINTS} fill="none" stroke="#a5b4fc" strokeWidth="2.5" strokeLinecap="round" />
                <polyline points={`${SPARKLINE_POINTS} 187,60 0,60`} fill="rgba(165, 180, 252, 0.20)" stroke="none" />
                <text x="0" y="76" fill="white" fontSize="10" fontWeight="600">Tuần 16</text>
                <text x="172" y="76" fill="white" fontSize="10" fontWeight="600">Tuần 27</text>
              </svg>
            </div>

            <dl className="mt-6 grid grid-cols-3 gap-4 text-[12px]">
              <div>
                <dt className="text-indigo-200 font-medium">Target</dt>
                <dd className="font-extrabold text-white text-[16px] tabular-nums">60 tỷ</dd>
              </div>
              <div>
                <dt className="text-indigo-200 font-medium">Đạt</dt>
                <dd className="font-extrabold text-white text-[16px] tabular-nums">79,7%</dd>
              </div>
              <div>
                <dt className="text-indigo-200 font-medium">Còn lại</dt>
                <dd className="font-extrabold text-white text-[16px] tabular-nums">12,2 tỷ</dd>
              </div>
            </dl>
          </article>

          {/* Secondary KPIs */}
          {KPIS_SECONDARY.map(kpi => {
            const trendIcon = kpi.trend === 'up' ? 'TrendUp' : 'TrendDown';
            const trendColor = kpi.trend === 'up' ? 'text-emerald-400' : 'text-rose-400';
            const Icon = Phosphor[trendIcon] as any;
            return (
              <article key={kpi.label} className="lg:col-span-3 lg:row-span-1 bg-slate-900 border border-slate-800 rounded-2xl p-5 hover:bg-slate-800 transition-colors">
                <p className="text-[10.5px] font-bold uppercase tracking-wider text-slate-400">{kpi.label}</p>
                <p className="mt-1 text-[28px] font-extrabold text-white tabular-nums leading-none">
                  {kpi.value}
                  {kpi.unit && <span className="text-[14px] text-slate-400 font-bold ml-1">{kpi.unit}</span>}
                </p>
                <p className={`mt-1 text-[11px] font-bold inline-flex items-center gap-1 ${trendColor}`}>
                  <Icon size={11} weight="bold" />
                  {kpi.delta}
                </p>
              </article>
            );
          })}

          {/* Activity feed */}
          <article className="lg:col-span-4 lg:row-span-2 bg-slate-900 border border-slate-800 rounded-2xl p-5">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-[14px] font-bold text-white flex items-center gap-1.5">
                <Phosphor.Pulse size={16} weight="bold" className="text-indigo-400" />
                Hoạt động gần đây
              </h3>
              <a href="#" className="text-[11px] font-semibold text-indigo-400 hover:text-indigo-300">Xem tất cả</a>
            </div>
            <ul className="space-y-3">
              {ACTIVITY_FEED.map((a, i) => {
                const Icon = Phosphor[a.icon] as any;
                return (
                  <li key={i} className="flex items-start gap-3">
                    <div className={`w-8 h-8 rounded-full bg-${a.color}-500/20 flex items-center justify-center flex-shrink-0`}>
                      <Icon size={14} weight="bold" className={`text-${a.color}-400`} />
                    </div>
                    <div className="min-w-0 flex-1">
                      <p className="text-[12.5px] text-slate-200" dangerouslySetInnerHTML={{ __html: a.text.replace(/\*\*(.*?)\*\*/g, '<strong class="font-bold text-white">$1</strong>') }} />
                      <p className="text-[11px] text-slate-500 mt-0.5 tabular-nums">{a.time}</p>
                    </div>
                  </li>
                );
              })}
            </ul>
          </article>

          {/* Stuck deals */}
          <article className="lg:col-span-2 lg:row-span-2 bg-rose-950/50 border border-rose-900/50 rounded-2xl p-5">
            <div className="flex items-center gap-2 mb-3">
              <Phosphor.WarningCircle size={18} weight="fill" className="text-rose-400" />
              <h3 className="text-[14px] font-bold text-rose-200">
                7 deals cần follow-up
              </h3>
            </div>
            <ul className="space-y-2">
              {STUCK_DEALS.map(d => (
                <li key={d.name} className="flex items-center justify-between p-2 bg-slate-900 rounded-lg hover:bg-slate-800 transition-colors">
                  <div>
                    <p className="text-[12.5px] font-semibold text-white">{d.name}</p>
                    <p className="text-[11px] text-rose-400 font-medium">{d.days} ngày không hoạt động</p>
                  </div>
                  <div className="text-right">
                    <p className="text-[12.5px] font-bold text-white tabular-nums">{d.value}</p>
                    <button aria-label={`Follow-up ${d.name}`} className="text-[10.5px] font-bold text-indigo-400 hover:text-indigo-300">
                      Follow →
                    </button>
                  </div>
                </li>
              ))}
            </ul>
            <button className="mt-3 w-full py-2 bg-slate-900 hover:bg-slate-800 border border-rose-900 text-rose-300 text-[12px] font-bold rounded-lg">
              Xem tất cả 7 deals
            </button>
          </article>
        </div>
      </div>
    </section>
  );
}