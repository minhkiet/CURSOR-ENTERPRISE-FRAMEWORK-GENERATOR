import * as Phosphor from '@phosphor-icons/react';
import { TESTIMONIALS, LOGO_WALL } from '@/data/testimonials';

const SIZE_MAP = {
  small: 'lg:col-span-1 lg:row-span-1',
  wide: 'lg:col-span-2 lg:row-span-1'
} as const;

export function TestimonialSection() {
  return (
    <section id="testimonials" className="bg-white py-16 lg:py-24" aria-labelledby="testimonial-heading">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <span className="inline-block text-[11px] font-bold uppercase tracking-[0.18em] text-indigo-600 mb-2">
            Được tin dùng bởi
          </span>
          <h2 id="testimonial-heading" className="text-3xl lg:text-5xl font-extrabold text-slate-900 tracking-tight">
            247 teams Việt Nam đang chốt deal nhanh hơn
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 lg:auto-rows-[300px]">
          {TESTIMONIALS.map(t => (
            <article key={t.id} className={`group bg-white rounded-2xl border border-slate-200 p-6 lg:p-7 hover:shadow-xl transition-shadow flex flex-col ${SIZE_MAP[t.cellSize]}`}>
              <div className="flex items-center justify-between mb-4">
                <img src={`https://cdn.simpleicons.org/${t.companySlug}/0f172a`} alt={t.company} className="h-6" loading="lazy" />
                <span className="text-[10.5px] font-bold uppercase tracking-wider text-slate-500">{t.industry}</span>
              </div>

              <blockquote className="relative flex-1">
                <Phosphor.Quotes size={20} weight="fill" className="absolute -left-1 -top-1 text-indigo-100" />
                <p className={`text-slate-800 leading-relaxed pl-6 ${t.cellSize === 'wide' ? 'text-[15px]' : 'text-[13.5px] line-clamp-4'}`}>
                  "{t.quote}"
                </p>
              </blockquote>

              <div className="mt-4 grid grid-cols-2 gap-3">
                {t.metrics.map((m, i) => {
                  const Icon = Phosphor[m.icon] as any;
                  return (
                    <div key={i} className="bg-slate-50 rounded-lg p-2.5">
                      <div className="flex items-center gap-1 text-[10.5px] text-slate-500 uppercase tracking-wider font-bold">
                        <Icon size={11} weight="bold" className="text-indigo-600" />
                        {m.label}
                      </div>
                      <p className="mt-1 text-[16px] font-extrabold text-slate-900 tabular-nums">{m.value}</p>
                    </div>
                  );
                })}
              </div>

              <div className="mt-4 pt-4 border-t border-slate-100 flex items-center gap-2.5">
                <img src={`https://images.unsplash.com/photo-${t.avatarId}?w=80&h=80&fit=crop&q=80`} alt={t.name} className="w-10 h-10 rounded-full object-cover ring-2 ring-slate-100" loading="lazy" />
                <div>
                  <p className="text-[13px] font-bold text-slate-900">{t.name}</p>
                  <p className="text-[11px] text-slate-500">{t.title}</p>
                </div>
              </div>
            </article>
          ))}
        </div>

        <div className="mt-12 pt-8 border-t border-slate-200">
          <p className="text-center text-[11px] font-bold uppercase tracking-wider text-slate-500 mb-6">
            Được tin dùng bởi 247+ doanh nghiệp Việt Nam
          </p>
          <div className="grid grid-cols-3 md:grid-cols-6 lg:grid-cols-12 gap-6 items-center justify-items-center opacity-60 grayscale">
            {LOGO_WALL.map(slug => (
              <img key={slug} src={`https://cdn.simpleicons.org/${slug}/64748b`} alt={slug} className="h-6 w-auto object-contain" loading="lazy" />
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}