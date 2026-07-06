# Customer Testimonial (Marketing Landing)

> Customer testimonial grid 3 col cho marketing landing. Mỗi testimonial có company logo, avatar, quote, KPI metric (revenue tăng X%, deals tăng Y%, etc), industry tag.

## 1. Mục đích

Visitor cần social proof trong 10s: ai đã dùng, kết quả thật. Bento 3-card giúp không bị generic và showcase cả B2B SaaS verticals.

## 2. Layout

```
┌──────────────────┬──────────────────┐
│ FPT Software     │ VNG Corp         │
│ "..."            │ "..."            │
│ ⬆ +47% pipeline │ ⬆ +82% close    │
│ ⬆ 32% win rate  │ ⬆ -28% cycle time│
│ Trần Minh       │ Lê Lan          │
├──────────────────┴──────────────────┤
│ TMA Solutions                        │
│ "..."                                 │
│ ⬆ Revenue 4.8 tỷ / Q               │
│ ⬆ 247 deals/quarter                │
│ Nguyễn Quân                        │
└────────────────────────────────────┘
```

## 3. Code reference

```tsx
import * as Phosphor from '@phosphor-icons/react';

const TESTIMONIALS = [
  {
    id: 'fpt',
    company: 'FPT Software',
    companySlug: 'fpt',
    industry: 'IT Services',
    avatarId: '1507003211169-0a1dd7228f2d',
    name: 'Trần Minh',
    title: 'VP Sales, FPT Software',
    quote: 'Pipeline visibility tốt hơn 4 lần. Sales rep xử lý 247 deals/quarter thay vì 32 như trước. Forecast chính xác 92%.',
    metrics: [
      { label: 'Pipeline value', value: '+47%', icon: 'TrendUp' },
      { label: 'Win rate', value: '32% → 47%', icon: 'Trophy' }
    ],
    cellSize: 'small' as const
  },
  {
    id: 'vng',
    company: 'VNG Corporation',
    companySlug: 'vng',
    industry: 'Tech',
    avatarId: '1494790108377-be9c29b29330',
    name: 'Lê Lan',
    title: 'CRO, VNG',
    quote: '5 đội sales phối hợp 1 pipeline. Cycle time rút ngắn từ 89 ngày còn 64 ngày. ROI dương sau 4 tháng.',
    metrics: [
      { label: 'Close rate', value: '+82%', icon: 'TrendUp' },
      { label: 'Sales cycle', value: '-28%', icon: 'Clock' }
    ],
    cellSize: 'small' as const
  },
  {
    id: 'tma',
    company: 'TMA Solutions',
    companySlug: 'tma',
    industry: 'Outsourcing',
    avatarId: '1472099645785-5658abf4ff4e',
    name: 'Nguyễn Quốc Quân',
    title: 'Sales Director, TMA',
    quote: 'Migrate từ Salesforce sang Northwind tiết kiệm 2.4 tỷ/năm license. Custom workflow cho 6 loại hợp đồng enterprise. API webhook giúp tự động sync với ERP nội bộ.',
    metrics: [
      { label: 'License savings', value: '2.4 tỷ/năm', icon: 'CurrencyDollar' },
      { label: 'Deals/quarter', value: '247', icon: 'Briefcase' }
    ],
    cellSize: 'wide' as const
  }
];

const SIZE_MAP = {
  small: 'lg:col-span-1 lg:row-span-1',
  wide: 'lg:col-span-2 lg:row-span-1'
} as const;

export function CustomerTestimonial() {
  return (
    <section className="bg-slate-50 py-16 lg:py-24" aria-labelledby="testimonial-heading">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-12">
          <span className="inline-block text-[11px] font-bold uppercase tracking-[0.18em] text-indigo-600 mb-2">
            Được tin dùng bởi
          </span>
          <h2 id="testimonial-heading" className="text-3xl lg:text-5xl font-extrabold text-slate-900 tracking-tight">
            247 teams Việt Nam đang chốt deal nhanh hơn
          </h2>
        </div>

        {/* Bento grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 lg:auto-rows-[280px]">
          {TESTIMONIALS.map(t => (
            <article key={t.id} className={`group bg-white rounded-2xl border border-slate-200 p-6 lg:p-7 hover:shadow-xl transition-shadow flex flex-col ${SIZE_MAP[t.cellSize]}`}>
              {/* Logo + Industry */}
              <div className="flex items-center justify-between mb-4">
                <img
                  src={`https://cdn.simpleicons.org/${t.companySlug}/0f172a`}
                  alt={t.company}
                  className="h-6"
                  loading="lazy"
                />
                <span className="text-[10.5px] font-bold uppercase tracking-wider text-slate-500">{t.industry}</span>
              </div>

              {/* Quote */}
              <blockquote className="relative flex-1">
                <Phosphor.Quotes size={20} weight="fill" className="absolute -left-1 -top-1 text-indigo-100" />
                <p className={`text-slate-800 leading-relaxed pl-6 ${t.cellSize === 'wide' ? 'text-[15px]' : 'text-[13.5px] line-clamp-4'}`}>
                  "{t.quote}"
                </p>
              </blockquote>

              {/* Metrics */}
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

              {/* Author */}
              <div className="mt-4 pt-4 border-t border-slate-100 flex items-center gap-2.5">
                <img
                  src={`https://images.unsplash.com/photo-${t.avatarId}?w=80&h=80&fit=crop&q=80`}
                  alt={t.name}
                  className="w-10 h-10 rounded-full object-cover ring-2 ring-slate-100"
                  loading="lazy"
                />
                <div>
                  <p className="text-[13px] font-bold text-slate-900">{t.name}</p>
                  <p className="text-[11px] text-slate-500">{t.title}</p>
                </div>
              </div>
            </article>
          ))}
        </div>

        {/* Logo wall */}
        <div className="mt-12 pt-8 border-t border-slate-200">
          <p className="text-center text-[11px] font-bold uppercase tracking-wider text-slate-500 mb-6">
            Được tin dùng bởi 247+ doanh nghiệp Việt Nam
          </p>
          <div className="grid grid-cols-3 md:grid-cols-6 lg:grid-cols-12 gap-6 items-center justify-items-center opacity-60 grayscale">
            {['fpt', 'vng', 'vingroup', 'vnpt', 'viettel', 'momo', 'tiki', 'shopee', 'lazada', 'sendo', 'tma', 'kms'].map(slug => (
              <img
                key={slug}
                src={`https://cdn.simpleicons.org/${slug}/64748b`}
                alt={slug}
                className="h-6 w-auto object-contain"
                loading="lazy"
              />
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
```

## 4. Accessibility

- Section `aria-labelledby`
- Mỗi card là `<article>`
- Quote là `<blockquote>`
- Avatar có alt text
- Logo có alt
- Metric values accessible với tabular-nums
- Reduce-motion: hover transitions off

## 5. Performance

- Unsplash avatars lazy load
- Simple Icons CDN cached
- Bento dùng CSS Grid auto-rows
- Quote line-clamp cho small cells

---

**Component family**: Marketing Landing — `customer-testimonial`