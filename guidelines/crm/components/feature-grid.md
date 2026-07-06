# Feature Grid

> Generic asymmetric grid for features, integrations, or any grid-based showcase. Supports 2 sizes (large highlight + small cells), icon + title + description + link pattern.

## 1. Mục đích

Dùng cho:
- **Integrations section**: Logo grid với Slack, Gmail, Outlook, Zoom, Google Calendar, MISA, ERP, Zapier, v.v.
- **Feature grid**: Grid các feature nhỏ
- **Logo wall**: Customer logos với description

## 2. Variants

| Variant | Use | Notes |
|---|---|---|
| `integrations` | Integration logos | Logo + name + short description |
| `feature-small` | Small feature icons | Icon + label grid |
| `logo-wall` | Customer logos | Logos only, no text |

## 3. Layout — Integrations variant

```
┌──────────────────────────────────────────────────────────────────────┐
│ Tích hợp native                                                 │
│ Kết nối với công cụ bạn đang dùng. Không cần code.           │
│                                                                          │
│ ┌────────────────────────────────────────────────────────────────┐ │
│ │ Slack · Gmail · Outlook · Zoom · Google Calendar · MISA · ERP   │ │
│ │ HubSpot · Zapier · Salesforce · QuickBooks · Jira · Zendesk     │ │
│ │ Pipedrive · Zoho · Freshsales · Telegram · Viber               │ │
│ └────────────────────────────────────────────────────────────────┘ │
│                                                                          │
│ 47+ tích hợp     [API Documentation →]    [Request integration →]     │
└──────────────────────────────────────────────────────────────────────┘
```

## 4. Layout — Logo wall variant

```
┌──────────────────────────────────────────────────────────────────────┐
│ Được tin dùng bởi 247+ doanh nghiệp Việt Nam                         │
│                                                                          │
│ FPT · VNG · Vingroup · VNPT · Viettel · TMA · MoMo · Tiki · Shopee │
│ Lazada · Sendo · KMS · Bosch · Canon · HP · Dell · Cisco           │
└──────────────────────────────────────────────────────────────────────┘
```

## 5. Code reference

```tsx
import * as Phosphor from '@phosphor-icons/react';

export interface Integration {
  slug: string;
  name: string;
  description: string;
  category: 'communication' | 'productivity' | 'finance' | 'crm' | 'other';
}

export const INTEGRATIONS: Integration[] = [
  { slug: 'slack', name: 'Slack', description: 'Channel notifications', category: 'communication' },
  { slug: 'gmail', name: 'Gmail', description: 'Email sync + scheduling', category: 'communication' },
  { slug: 'outlook', name: 'Outlook', description: 'Office 365 integration', category: 'communication' },
  { slug: 'zoom', name: 'Zoom', description: 'Meeting links auto-generate', category: 'communication' },
  { slug: 'google-calendar', name: 'Google Calendar', description: 'Event sync 2 chiều', category: 'productivity' },
  { slug: 'misa', name: 'MISA', description: 'Invoice + accounting sync', category: 'finance' },
  { slug: 'erp', name: 'ERP', description: 'Custom ERP webhook', category: 'finance' },
  { slug: 'hubspot', name: 'HubSpot', description: 'CRM data migration', category: 'crm' },
  { slug: 'pipedrive', name: 'Pipedrive', description: 'Import deals + contacts', category: 'crm' },
  { slug: 'zapier', name: 'Zapier', description: '5.000+ app connections', category: 'other' },
  { slug: 'quickbooks', name: 'QuickBooks', description: 'Revenue sync', category: 'finance' },
  { slug: 'jira', name: 'Jira', description: 'Task from deal', category: 'productivity' }
];

export const LOGO_WALL = [
  'fpt', 'vng', 'vingroup', 'vnpt', 'viettel', 'momo', 'tiki', 'shopee',
  'lazada', 'sendo', 'tma', 'kms', 'bosch', 'canon', 'hp', 'dell', 'cisco'
];

export function FeatureGrid() {
  return (
    <>
      <IntegrationsSection />
      <LogoWallSection />
    </>
  );
}

function IntegrationsSection() {
  return (
    <section className="bg-white py-16 lg:py-24" aria-labelledby="integrations-heading">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-10">
          <span className="inline-block text-[11px] font-bold uppercase tracking-[0.18em] text-indigo-600 mb-2">
            Tích hợp
          </span>
          <h2 id="integrations-heading" className="text-3xl lg:text-4xl font-extrabold text-slate-900 tracking-tight">
            Kết nối với công cụ bạn đang dùng
          </h2>
          <p className="mt-3 text-[15px] text-slate-600 max-w-2xl mx-auto">
            Native integration với 47+ công cụ phổ biến. Không cần code. Setup trong 5 phút.
          </p>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3 lg:gap-4 mb-8">
          {INTEGRATIONS.map(integration => (
            <article
              key={integration.slug}
              className="group bg-white border border-slate-200 rounded-xl p-4 hover:shadow-card-lift hover:-translate-y-0.5 transition-all text-center"
            >
              <div className="w-12 h-12 mx-auto mb-3">
                <img
                  src={`https://cdn.simpleicons.org/${integration.slug}/64748b`}
                  alt={integration.name}
                  className="w-full h-full object-contain group-hover:scale-110 transition-transform"
                  loading="lazy"
                />
              </div>
              <p className="text-[13px] font-bold text-slate-900">{integration.name}</p>
              <p className="text-[11px] text-slate-500 mt-0.5 line-clamp-1">{integration.description}</p>
            </article>
          ))}
        </div>

        <div className="flex flex-wrap items-center justify-center gap-3 text-[13px]">
          <div className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-indigo-50 text-indigo-700 rounded-full font-bold">
            <Phosphor.Plugs size={13} weight="bold" />
            47+ tích hợp
          </div>
          <a href="/docs/api" className="inline-flex items-center gap-1.5 px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold rounded-lg transition-colors">
            API Documentation
            <Phosphor.ArrowRight size={12} weight="bold" />
          </a>
          <a href="/request-integration" className="inline-flex items-center gap-1.5 px-4 py-2 border border-slate-300 hover:border-indigo-500 text-slate-700 hover:text-indigo-700 font-semibold rounded-lg transition-colors">
            Request integration
            <Phosphor.Plus size={12} weight="bold" />
          </a>
        </div>
      </div>
    </section>
  );
}

function LogoWallSection() {
  return (
    <section className="bg-white border-y border-slate-200 py-10" aria-labelledby="logo-wall-heading">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <p id="logo-wall-heading" className="text-center text-[11px] font-bold uppercase tracking-[0.18em] text-slate-500 mb-8">
          Được tin dùng bởi 247+ doanh nghiệp Việt Nam
        </p>
        <div className="grid grid-cols-3 md:grid-cols-6 lg:grid-cols-9 gap-6 items-center justify-items-center opacity-60 grayscale hover:opacity-100 hover:grayscale-0 transition-all duration-500">
          {LOGO_WALL.map(slug => (
            <img
              key={slug}
              src={`https://cdn.simpleicons.org/${slug}/64748b`}
              alt={slug}
              className="h-7 w-auto object-contain"
              loading="lazy"
            />
          ))}
        </div>
      </div>
    </section>
  );
}
```

## 5. Accessibility

- Section `aria-labelledby`
- Each integration `<article>` với name visible
- Logos có alt text (name of company)
- Links có descriptive text
- Numbers tabular-nums
- Reduce-motion: hover scale off

## 6. Performance

- Logo lazy load
- CSS grid (no JS)
- Grayscale → color transition CSS only

## 7. Anti-patterns đã tránh

- ❌ "Make every screen feel like..."
- ❌ Logos không alt text
- ❌ Logos không contrast (đã grayscale → color on hover)
- ❌ Logo wall trống không context (đã heading + "247+ doanh nghiệp")
- ❌ Integration list không mô tả

---

**Component family**: Marketing Landing — `feature-grid`