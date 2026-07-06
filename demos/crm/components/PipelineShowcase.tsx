import * as Phosphor from '@phosphor-icons/react';
import { STAGES, SAMPLE_DEALS } from '@/data/pipeline';

export function PipelineShowcase() {
  return (
    <section className="bg-white py-16 lg:py-24" aria-labelledby="pipeline-heading">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="flex flex-wrap items-end justify-between gap-4 mb-10">
          <div>
            <span className="inline-block text-[11px] font-bold uppercase tracking-[0.18em] text-indigo-600 mb-2">
              Pipeline kanban
            </span>
            <h2 id="pipeline-heading" className="text-3xl lg:text-4xl font-extrabold text-slate-900 tracking-tight">
              Kéo deal giữa các stage
            </h2>
            <p className="mt-2 text-slate-600 text-[15px]">
              5-stage pipeline với visual deal cards. Drag-drop accessible, keyboard shortcuts, total value từng stage.
            </p>
          </div>
          <div className="flex items-center gap-3 text-[13px]">
            <div className="text-right">
              <p className="text-[10.5px] font-bold uppercase tracking-wider text-slate-500">Tổng pipeline</p>
              <p className="text-[22px] font-extrabold text-slate-900 tabular-nums">14,8 tỷ</p>
            </div>
            <div className="text-right">
              <p className="text-[10.5px] font-bold uppercase tracking-wider text-slate-500">Deals active</p>
              <p className="text-[22px] font-extrabold text-slate-900 tabular-nums">247</p>
            </div>
          </div>
        </div>

        {/* Pipeline */}
        <div className="overflow-x-auto hide-scrollbar -mx-4 px-4">
          <div className="flex gap-3 min-w-max pb-4">
            {STAGES.map(stage => {
              const stageDeals = SAMPLE_DEALS.filter(d => d.stage === stage.id);
              const stageValue = stageDeals.reduce((sum, d) => sum + d.value, 0);
              const Icon = Phosphor[stage.icon] as any;
              return (
                <section
                  key={stage.id}
                  aria-labelledby={`stage-${stage.id}`}
                  className="w-72 flex-shrink-0 bg-slate-50 rounded-xl border border-slate-200"
                >
                  {/* Header */}
                  <header className="p-3.5 border-b border-slate-200 bg-white rounded-t-xl">
                    <div className="flex items-center justify-between">
                      <h3 id={`stage-${stage.id}`} className="flex items-center gap-1.5 text-[12.5px] font-bold uppercase tracking-wide text-slate-700">
                        <Icon size={14} weight="bold" className="text-slate-500" />
                        {stage.name}
                      </h3>
                      <span className="px-2 py-0.5 bg-slate-100 text-slate-700 text-[10.5px] font-bold rounded-full tabular-nums">
                        {stageDeals.length}
                      </span>
                    </div>
                    <div className="mt-1.5 flex items-baseline gap-2">
                      <output className="text-[16px] font-extrabold text-slate-900 tabular-nums">
                        {formatVND(stageValue)}
                      </output>
                      <span className="text-[10px] text-slate-500 font-medium uppercase tracking-wider">
                        {stage.probability}%
                      </span>
                    </div>
                  </header>

                  {/* Cards */}
                  <div className="p-2.5 space-y-2 min-h-[140px]">
                    {stageDeals.map(deal => (
                      <article
                        key={deal.id}
                        className="group cursor-pointer p-3 rounded-lg border border-slate-200 bg-white hover:shadow-card-lift hover:-translate-y-0.5 transition-all"
                        tabIndex={0}
                      >
                        {/* Top row */}
                        <div className="flex items-center gap-1 mb-1.5">
                          {deal.isHot && (
                            <span className="inline-flex items-center gap-0.5 px-1.5 py-0.5 bg-rose-100 text-rose-700 text-[9.5px] font-bold uppercase tracking-wider rounded">
                              <Phosphor.Fire size={9} weight="fill" />
                              Hot
                            </span>
                          )}
                          {deal.isStalled && (
                            <span className="inline-flex items-center gap-0.5 px-1.5 py-0.5 bg-amber-100 text-amber-700 text-[9.5px] font-bold uppercase tracking-wider rounded">
                              <Phosphor.WarningCircle size={9} weight="fill" />
                              Stalled
                            </span>
                          )}
                        </div>

                        {/* Title */}
                        <h4 className="text-[13px] font-bold text-slate-900 leading-snug line-clamp-2">
                          {deal.title}
                        </h4>
                        <div className="mt-1 flex items-center gap-1.5 text-[11px] text-slate-600">
                          <img
                            src={`https://cdn.simpleicons.org/${deal.companySlug}/64748b`}
                            alt={deal.company}
                            className="w-3 h-3"
                            loading="lazy"
                          />
                          {deal.company}
                        </div>

                        {/* Value */}
                        <div className="mt-2 text-[15px] font-extrabold text-slate-900 tabular-nums leading-none">
                          {formatVND(deal.value)}
                        </div>

                        {/* Bottom */}
                        <div className="mt-2 pt-2 border-t border-slate-100 flex items-center justify-between">
                          <div className="flex items-center gap-1.5">
                            <img
                              src={`https://images.unsplash.com/photo-${deal.owner.avatarId}?w=40&h=40&fit=crop&q=80`}
                              alt={deal.owner.name}
                              className="w-5 h-5 rounded-full object-cover ring-1 ring-slate-200"
                              loading="lazy"
                            />
                            <span className="text-[11px] font-semibold text-slate-700">{deal.owner.name}</span>
                          </div>
                          <span className="inline-flex items-center gap-0.5 text-[10.5px] text-slate-500 tabular-nums">
                            <Phosphor.Clock size={10} weight="regular" />
                            {deal.age}d
                          </span>
                        </div>
                      </article>
                    ))}
                  </div>
                </section>
              );
            })}
          </div>
        </div>

        <p className="mt-4 text-center text-[12px] text-slate-500">
          ← Cuộn ngang để xem 5 stages · Click deal để mở detail drawer →
        </p>
      </div>
    </section>
  );
}

function formatVND(v: number): string {
  if (v >= 1_000_000_000) return `${(v / 1_000_000_000).toFixed(1)} tỷ`;
  if (v >= 1_000_000) return `${Math.round(v / 1_000_000)} tr`;
  return v.toLocaleString('vi-VN');
}