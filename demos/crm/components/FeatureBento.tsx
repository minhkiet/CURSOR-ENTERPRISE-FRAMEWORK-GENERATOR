import * as Phosphor from '@phosphor-icons/react';
import { FEATURES } from '@/data/features';

const SIZE_MAP = {
  large: 'lg:col-span-2 lg:row-span-2',
  small: 'lg:col-span-1 lg:row-span-1'
} as const;

export function FeatureBento() {
  return (
    <section id="features" className="bg-slate-50 py-16 lg:py-24" aria-labelledby="features-heading">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="max-w-2xl mb-12">
          <span className="inline-block text-[11px] font-bold uppercase tracking-[0.18em] text-indigo-600 mb-2">
            Sản phẩm
          </span>
          <h2 id="features-heading" className="text-3xl lg:text-5xl font-extrabold text-slate-900 tracking-tight leading-tight">
            Tất cả công cụ sales rep Việt Nam cần.
          </h2>
          <p className="mt-3 text-[15px] text-slate-600">
            Pipeline · Contacts · Automation · Forecast · Reports · Integrations. Một platform cho toàn bộ sales workflow.
          </p>
        </div>

        {/* Bento grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-5 lg:auto-rows-[180px]">
          {FEATURES.map(f => {
            const Icon = Phosphor[f.icon] as any;
            return (
              <article
                key={f.id}
                className={`group bg-white rounded-2xl border border-slate-200 p-5 lg:p-6 hover:shadow-card-lift hover:-translate-y-0.5 transition-all flex flex-col ${SIZE_MAP[f.variant]}`}
              >
                <div className={`w-11 h-11 rounded-xl flex items-center justify-center mb-4 ${f.variant === 'large' ? 'bg-indigo-600 text-white' : 'bg-indigo-50 text-indigo-600 group-hover:bg-indigo-600 group-hover:text-white transition-colors'}`}>
                  <Icon size={f.variant === 'large' ? 24 : 20} weight="bold" />
                </div>

                <h3 className={`font-extrabold text-slate-900 ${f.variant === 'large' ? 'text-[22px]' : 'text-[15px]'} leading-snug`}>
                  {f.title}
                </h3>

                <p className={`mt-2 text-slate-600 leading-relaxed ${f.variant === 'large' ? 'text-[14px]' : 'text-[12.5px] line-clamp-3'}`}>
                  {f.description}
                </p>

                <div className="mt-auto pt-3 flex items-center gap-2">
                  <span className="inline-flex items-center gap-1 text-[11.5px] font-bold text-indigo-600">
                    <Phosphor.ArrowUpRight size={12} weight="bold" />
                    {f.metric}
                  </span>
                </div>
              </article>
            );
          })}
        </div>
      </div>
    </section>
  );
}