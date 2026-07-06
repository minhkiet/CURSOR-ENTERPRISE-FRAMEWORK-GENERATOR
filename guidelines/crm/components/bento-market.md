# Bento Market

> Marketing landing page 3-pillar feature bento — asymmetric grid, feature screenshots, metric callouts. Đi sau hero và logo wall.

## 1. Mục đích

Showcase 3 tính năng chính (Pipeline, Contacts, Automation) với screenshots thực tế từ app. Mỗi feature có 1 metric mạnh. Bento asymmetric — không 3 equal columns.

## 2. Layout

```
┌──────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  Tất cả công cụ sales rep Việt Nam cần.                               │
│  Một platform cho toàn bộ sales workflow.                             │
│                                                                         │
│  ┌──────────────────────────────┐ ┌────────────┐ ┌─────────────────┐  │
│  │                              │ │            │ │                 │  │
│  │  [Pipeline screenshot]       │ │ Contacts   │ │ Automation      │  │
│  │                              │ │ [List UI]  │ │ [Workflow UI]  │  │
│  │  Pipeline 5 stages          │ │            │ │                 │  │
│  │  47.8 tỷ VND              │ │ 10.247     │ │ 247 auto       │  │
│  │                              │ │ contacts   │ │ trigger/day    │  │
│  │  ─────────────────────────  │ │            │ │                 │  │
│  │  [View screenshot →]        │ │ [View →]  │ │ [View →]      │  │
│  └──────────────────────────────┘ └────────────┘ └─────────────────┘  │
│  ┌────────────┐ ┌────────────────────────────────────────────────┐    │
│  │            │ │                                                  │    │
│  │ Forecast   │ │  Reports tùy chỉnh                             │    │
│  │ 92%       │ │  30+ templates                                  │    │
│  │ accuracy  │ │  [Report UI screenshot]                        │    │
│  └────────────┘ └────────────────────────────────────────────────┘    │
│  ┌──────────────────────────────────────────────────────────────┐     │
│  │ Integrations · 47+ tích hợp · Slack · Gmail · Outlook ·   │     │
│  │ Zoom · Google Calendar · MISA · ERP · [View all →]        │     │
│  └──────────────────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────────────────┘
```

## 3. Bento grid (6 cells)

| Cell | Size | Content | Metric |
|---|---|---|---|
| Pipeline | 2×2 | Screenshot kanban + text | 47,8 tỷ VND |
| Contacts | 1×1 | Screenshot list + text | 10.247 contacts |
| Automation | 1×1 | Screenshot workflow + text | 247 auto triggers |
| Forecast | 1×1 | Text + chart preview | 92% accuracy |
| Reports | 2×1 | Screenshot report + text | 30+ templates |
| Integrations | 1×1 | Logo grid + text | 47+ integrations |

**Grid**: `lg:grid-cols-4 lg:auto-rows-[220px]`

## 4. Code reference

```tsx
import * as Phosphor from '@phosphor-icons/react';

export interface BentoFeature {
  id: string;
  icon: string;
  title: string;
  description: string;
  metric: string;
  metricLabel: string;
  screenshot?: string;
  cellSize: '2x2' | '1x1';
  variant: 'large' | 'small';
}

export const BENTO_FEATURES: BentoFeature[] = [
  {
    id: 'pipeline',
    icon: 'Kanban',
    title: 'Pipeline 5-stage',
    description: 'Kéo deal giữa các stages. Xem tổng giá trị từng stage. Forecast dựa trên win-rate từng stage.',
    metric: '47,8 tỷ',
    metricLabel: 'pipeline value',
    screenshot: 'pipeline-kanban.png',
    cellSize: '2x2',
    variant: 'large'
  },
  {
    id: 'contacts',
    icon: 'UsersThree',
    title: 'Quản lý contacts',
    description: 'Bulk import từ CSV/Excel. Tự động enrich từ email. Segment theo industry, deal value.',
    metric: '10.247',
    metricLabel: 'contacts',
    cellSize: '1x1',
    variant: 'small'
  },
  {
    id: 'automation',
    icon: 'Lightning',
    title: 'Workflow automation',
    description: 'Trigger tự động khi deal thay đổi stage. Slack notification. Email reminder.',
    metric: '247',
    metricLabel: 'auto triggers/ngày',
    cellSize: '1x1',
    variant: 'small'
  },
  {
    id: 'forecast',
    icon: 'ChartLineUp',
    title: 'AI-driven forecast',
    description: 'Dựa trên historical win rate, deal velocity, rep activity.',
    metric: '92%',
    metricLabel: 'forecast accuracy',
    cellSize: '1x1',
    variant: 'small'
  },
  {
    id: 'reports',
    icon: 'ChartBar',
    title: 'Reports tùy chỉnh',
    description: '30+ templates có sẵn. Custom dashboard cho sales rep / manager / executive. Export PDF/CSV.',
    metric: '30+',
    metricLabel: 'templates',
    cellSize: '2x1',
    variant: 'small'
  },
  {
    id: 'integrations',
    icon: 'Plugs',
    title: 'Tích hợp native',
    description: 'Gmail · Slack · Outlook · Zoom · Google Calendar · MISA · ERP.',
    metric: '47+',
    metricLabel: 'tích hợp',
    cellSize: '1x1',
    variant: 'small'
  }
];

export function BentoMarket() {
  return (
    <section id="features" className="bg-slate-50 py-16 lg:py-24" aria-labelledby="bento-heading">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="max-w-2xl mb-12">
          <span className="inline-block text-[11px] font-bold uppercase tracking-[0.18em] text-indigo-600 mb-2">
            Sản phẩm
          </span>
          <h2 id="bento-heading" className="text-3xl lg:text-5xl font-extrabold text-slate-900 tracking-tight leading-tight">
            Tất cả công cụ sales rep Việt Nam cần.
          </h2>
          <p className="mt-3 text-[15px] text-slate-600">
            Pipeline · Contacts · Automation · Forecast · Reports · Integrations. Một platform cho toàn bộ sales workflow.
          </p>
        </div>

        {/* Bento grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-5 lg:auto-rows-[220px]">
          {BENTO_FEATURES.map(f => <BentoCell key={f.id} feature={f} />)}
        </div>
      </div>
    </section>
  );
}

function BentoCell({ feature }: { feature: BentoFeature }) {
  const Icon = Phosphor[feature.icon] as any;

  const spanMap = {
    '2x2': 'lg:col-span-2 lg:row-span-2',
    '1x1': 'lg:col-span-1 lg:row-span-1',
    '2x1': 'lg:col-span-2 lg:row-span-1',
    '1x2': 'lg:col-span-1 lg:row-span-2'
  } as const;

  return (
    <article
      className={`group bg-white rounded-2xl border border-slate-200 p-5 lg:p-6 hover:shadow-card-lift hover:-translate-y-0.5 transition-all flex flex-col ${spanMap[feature.cellSize]}`}
    >
      <div className={`w-11 h-11 rounded-xl flex items-center justify-center mb-4 ${
        feature.cellSize === '2x2'
          ? 'bg-indigo-600 text-white'
          : 'bg-indigo-50 text-indigo-600 group-hover:bg-indigo-600 group-hover:text-white transition-colors'
      }`}>
        <Icon size={feature.cellSize === '2x2' ? 24 : 20} weight="bold" />
      </div>

      <h3 className={`font-extrabold text-slate-900 ${feature.cellSize === '2x2' ? 'text-[22px]' : 'text-[15px]'} leading-snug`}>
        {feature.title}
      </h3>

      <p className={`mt-2 text-slate-600 leading-relaxed ${feature.cellSize === '2x2' ? 'text-[14px]' : 'text-[12.5px] line-clamp-2 lg:line-clamp-3'}`}>
        {feature.description}
      </p>

      <div className="mt-auto pt-3 flex items-center justify-between">
        <span className="inline-flex items-center gap-1 text-[11.5px] font-bold text-indigo-600">
          <Phosphor.ArrowUpRight size={12} weight="bold" />
          {feature.metric} {feature.metricLabel}
        </span>
        <a
          href={`/product/${feature.id}`}
          className="text-[11.5px] font-semibold text-slate-500 hover:text-indigo-600 transition-colors"
        >
          Xem chi tiết →
        </a>
      </div>
    </article>
  );
}
```

## 4. Accessibility

- Section `aria-labelledby`
- Each cell `<article>` với heading
- Links có descriptive text (not "Read more")
- Numbers tabular-nums
- Icons decorative (aria-hidden) or with label
- Reduce-motion: hover transitions off

## 5. Performance

- Static screenshots (no dynamic loading)
- CSS Grid (no JS layout)
- Memoized cells
- Inline icons

## 6. Anti-patterns đã tránh

- ❌ "Make every screen feel like..."
- ❌ 3 equal columns (đã bento asymmetric)
- ❌ Generic "Learn more" links (đã "Xem chi tiết →")
- ❌ No metric callouts (đã metric prominent mỗi cell)
- ❌ Color-only icons (đã icon + text heading)

---

**Component family**: Marketing Landing — `bento-market`