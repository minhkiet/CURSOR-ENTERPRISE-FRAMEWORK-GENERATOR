import * as Phosphor from '@phosphor-icons/react';
import { FEATURES } from '@/data/features';

const SIZE_MAP = {
  large: 'lg:col-span-2 lg:row-span-2',
  small: 'lg:col-span-1 lg:row-span-1'
} as const;

export function FeatureBento() {
  return (
    <section id="features" className="bg-ink-950 py-16 lg:py-24 text-ink-50" aria-labelledby="features-heading">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="max-w-2xl mb-12">
          <span className="text-[11px] font-bold uppercase tracking-[0.18em] text-electric-400 mb-2 block">
            Built for serious lifters
          </span>
          <h2 id="features-heading" className="text-3xl lg:text-5xl font-display tracking-tight leading-[1.05]">
            Mọi thứ bạn cần.<br />
            <span className="text-electric-400">Không có clutter.</span>
          </h2>
          <p className="mt-3 text-slate-400 text-[15px]">
            Touch targets 56px+ cho tay đeo găng. Dark theme AAA contrast. Apple Watch native. Strava + Garmin sync.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-5 lg:auto-rows-[180px]">
          {FEATURES.map(f => {
            const Icon = Phosphor[f.icon] as any;
            return (
              <article
                key={f.id}
                className={`group bg-ink-900 border border-ink-800 rounded-2xl p-5 lg:p-6 hover:border-electric-500/50 hover:shadow-glow-electric transition-all flex flex-col ${SIZE_MAP[f.variant]}`}
              >
                <div className={`w-11 h-11 rounded-xl flex items-center justify-center mb-4 ${
                  f.variant === 'large'
                    ? 'bg-electric-500 text-ink-950 shadow-lg shadow-electric-500/30'
                    : 'bg-electric-500/10 text-electric-400 group-hover:bg-electric-500 group-hover:text-ink-950 transition-colors'
                }`}>
                  <Icon size={f.variant === 'large' ? 24 : 20} weight="bold" />
                </div>

                <h3 className={`font-display text-ink-50 ${f.variant === 'large' ? 'text-[24px]' : 'text-[16px]'} leading-tight`}>
                  {f.title}
                </h3>

                <p className={`mt-2 text-slate-400 leading-relaxed ${f.variant === 'large' ? 'text-[14px]' : 'text-[12.5px] line-clamp-3'}`}>
                  {f.description}
                </p>

                <div className="mt-auto pt-3 flex items-center gap-2">
                  <span className="inline-flex items-center gap-1 text-[11.5px] font-extrabold text-electric-400 tabular-nums">
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