import * as Phosphor from '@phosphor-icons/react';
import { HERO_HEADLINE, HERO_SUBHEAD, TRUST_LOGOS } from '@/data/hero';

export function Hero() {
  return (
    <section className="relative bg-white overflow-hidden">
      {/* Subtle bg pattern */}
      <div className="absolute inset-0 opacity-[0.03]" style={{ backgroundImage: 'radial-gradient(circle at 1px 1px, #0f172a 1px, transparent 0)', backgroundSize: '24px 24px' }} aria-hidden="true" />

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-16 lg:pt-24 pb-16 lg:pb-20">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 lg:gap-16 items-center">
          {/* Copy */}
          <div className="lg:col-span-6">
            <span className="inline-flex items-center gap-1.5 px-3 py-1 bg-indigo-50 text-indigo-700 text-[11px] font-bold uppercase tracking-wider rounded-full mb-5">
              <Phosphor.Sparkle size={11} weight="fill" />
              CRM #1 Việt Nam · 2026
            </span>
            <h1 className="text-4xl lg:text-6xl font-extrabold text-slate-900 tracking-tight leading-[1.05]">
              {HERO_HEADLINE}
            </h1>
            <p className="mt-5 text-[16px] lg:text-[18px] text-slate-600 leading-relaxed max-w-xl">
              {HERO_SUBHEAD}
            </p>

            <div className="mt-7 flex flex-wrap items-center gap-3">
              <a href="/signup" className="inline-flex items-center gap-1.5 px-6 py-3.5 bg-gradient-to-r from-indigo-600 to-indigo-700 hover:from-indigo-700 hover:to-indigo-800 text-white text-[14px] font-bold rounded-lg shadow-lg shadow-indigo-200">
                Dùng thử 14 ngày miễn phí
                <Phosphor.ArrowRight size={14} weight="bold" />
              </a>
              <a href="/demo" className="inline-flex items-center gap-1.5 px-6 py-3.5 bg-white hover:bg-slate-50 border border-slate-300 text-slate-700 text-[14px] font-bold rounded-lg">
                <Phosphor.Play size={14} weight="fill" />
                Xem demo 2 phút
              </a>
            </div>

            <ul className="mt-7 flex flex-wrap items-center gap-x-5 gap-y-2 text-[12.5px] text-slate-600">
              <li className="inline-flex items-center gap-1.5">
                <Phosphor.CheckCircle size={13} weight="fill" className="text-emerald-500" />
                Không cần thẻ tín dụng
              </li>
              <li className="inline-flex items-center gap-1.5">
                <Phosphor.CheckCircle size={13} weight="fill" className="text-emerald-500" />
                Setup trong 5 phút
              </li>
              <li className="inline-flex items-center gap-1.5">
                <Phosphor.CheckCircle size={13} weight="fill" className="text-emerald-500" />
                24/7 support tiếng Việt
              </li>
            </ul>
          </div>

          {/* Dashboard mock */}
          <div className="lg:col-span-6">
            <DashboardMock />
          </div>
        </div>
      </div>
    </section>
  );
}

function DashboardMock() {
  return (
    <div className="relative">
      {/* Glow */}
      <div className="absolute -inset-4 bg-gradient-to-br from-indigo-100 to-sky-100 rounded-3xl blur-2xl opacity-50" aria-hidden="true" />

      <div className="relative bg-white rounded-2xl shadow-2xl border border-slate-200 overflow-hidden">
        {/* Window chrome */}
        <div className="flex items-center justify-between bg-slate-100 px-4 py-2.5 border-b border-slate-200">
          <div className="flex items-center gap-1.5">
            <div className="w-3 h-3 bg-rose-400 rounded-full" />
            <div className="w-3 h-3 bg-amber-400 rounded-full" />
            <div className="w-3 h-3 bg-emerald-400 rounded-full" />
          </div>
          <div className="text-[11px] font-semibold text-slate-500 tabular-nums">app.northwind.vn · Pipeline Q3</div>
          <div className="w-12" />
        </div>

        {/* Header bar */}
        <div className="p-4 border-b border-slate-200 flex items-center justify-between">
          <div>
            <p className="text-[11px] font-bold uppercase tracking-wider text-slate-500">Pipeline Q3 2026</p>
            <p className="text-[16px] font-extrabold text-slate-900 tabular-nums">47,8 tỷ VND</p>
          </div>
          <div className="flex items-center gap-1.5 text-[10.5px] font-bold text-emerald-600">
            <Phosphor.TrendUp size={11} weight="bold" />
            +18,2%
          </div>
        </div>

        {/* Stages */}
        <div className="p-3 grid grid-cols-5 gap-2 min-h-[180px]">
          {[
            { name: 'Lead', count: 78, color: 'bg-slate-500' },
            { name: 'Qualified', count: 56, color: 'bg-sky-500' },
            { name: 'Proposal', count: 42, color: 'bg-indigo-500' },
            { name: 'Negotiation', count: 18, color: 'bg-amber-500' },
            { name: 'Won', count: 53, color: 'bg-emerald-500' }
          ].map(stage => (
            <div key={stage.name} className="bg-slate-50 rounded-lg p-2">
              <div className="flex items-center justify-between mb-1.5">
                <p className="text-[9.5px] font-bold uppercase tracking-wider text-slate-600 truncate">{stage.name}</p>
                <span className="text-[9px] font-bold text-slate-500 tabular-nums">{stage.count}</span>
              </div>
              <div className={`h-1 ${stage.color} rounded-full mb-2`} />
              <div className="space-y-1">
                {Array.from({ length: Math.min(3, Math.floor(stage.count / 20)) }).map((_, i) => (
                  <div key={i} className="bg-white p-1.5 rounded border border-slate-200">
                    <div className="h-1 bg-slate-200 rounded w-3/4 mb-0.5" />
                    <div className="h-1 bg-slate-100 rounded w-1/2" />
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* Activity bar */}
        <div className="px-4 py-2.5 border-t border-slate-200 bg-slate-50 flex items-center gap-3">
          <div className="flex -space-x-1.5">
            {['1507003211169-0a1dd7228f2d', '1494790108377-be9c29b29330', '1472099645785-5658abf4ff4e'].map(id => (
              <img key={id} src={`https://images.unsplash.com/photo-${id}?w=40&h=40&fit=crop&q=80`} alt="" className="w-5 h-5 rounded-full ring-2 ring-white object-cover" loading="lazy" />
            ))}
          </div>
          <p className="text-[10.5px] text-slate-600">
            <strong className="font-bold text-slate-900 tabular-nums">247</strong> deals · <strong className="font-bold text-slate-900 tabular-nums">38</strong> reps active
          </p>
        </div>
      </div>
    </div>
  );
}

export function TrustStrip() {
  return (
    <section className="bg-white border-y border-slate-200 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <p className="text-center text-[11px] font-bold uppercase tracking-[0.18em] text-slate-500 mb-6">
          Được tin dùng bởi 247+ doanh nghiệp Việt Nam
        </p>
        <div className="grid grid-cols-4 md:grid-cols-8 gap-6 items-center justify-items-center opacity-70 grayscale">
          {TRUST_LOGOS.map(l => (
            <img
              key={l.slug}
              src={`https://cdn.simpleicons.org/${l.slug}/64748b`}
              alt={l.name}
              className="h-6 w-auto object-contain"
              loading="lazy"
            />
          ))}
        </div>
      </div>
    </section>
  );
}