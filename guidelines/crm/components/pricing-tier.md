# Pricing Tier

> Card pricing 3 tier (Starter · Pro · Enterprise) cho marketing landing. Highlight tier "đề xuất", feature list so sánh, CTA rõ ràng, annual/monthly toggle.

## 1. Mục đích

Visitor cần so sánh 3 tiers trong < 10s, thấy tier phù hợp với team size, click CTA mua.

## 2. Asset

| Element | Source |
|---|---|
| Brand logos (customers) | Simple Icons CDN |
| Avatar | Unsplash curated |

## 3. Layout

```
┌──────────────────┬──────────────────┬──────────────────┐
│ Starter          │ ⭐ Pro           │ Enterprise       │
│ Cho team nhỏ     │ Đề xuất cho bạn  │ Cho 50+ users     │
│                  │                  │                  │
│ 199.000₫         │ 599.000₫         │ Liên hệ          │
│ /user/tháng      │ /user/tháng      │                  │
│                  │                  │                  │
│ ✓ Up to 5 users  │ ✓ Unlimited users│ ✓ Custom SSO     │
│ ✓ Pipeline       │ ✓ Pipeline + Auto │ ✓ Custom SLA     │
│ ✓ Email support  │ ✓ 24/7 chat sup. │ ✓ Dedicated CSM  │
│ ✗ Reporting      │ ✓ Advanced rep.  │ ✓ Custom report  │
│                  │                  │                  │
│ [   Bắt đầu   ]  │ [   Dùng thử   ] │ [   Liên hệ   ]  │
└──────────────────┴──────────────────┴──────────────────┘
```

## 4. Variants

| Variant | Use | Khác biệt |
|---|---|---|
| `default` | Marketing landing | 3 cards horizontal |
| `comparison` | Pricing page | Plus comparison table |
| `compact` | In-app upsell | Smaller |

## 5. States

| State | Visual |
|---|---|
| default | Standard |
| recommended | Border indigo + badge |
| current | Tier người dùng đang dùng |
| reduce-motion | No transitions |

## 6. Icon mapping

| Role | Phosphor |
|---|---|
| Star (recommended) | `Star` (fill) |
| Check | `CheckCircle` (fill) |
| Cross | `X` |
| Sparkle | `Sparkle` (fill) |
| Crown | `Crown` |

## 7. Code reference

```tsx
'use client';
import { useState } from 'react';
import * as Phosphor from '@phosphor-icons/react';

export interface PricingTier {
  id: string;
  name: string;
  description: string;
  priceMonthly: number | 'contact';
  priceAnnual: number | 'contact';
  features: Array<{ text: string; included: boolean; tooltip?: string }>;
  cta: { label: string; href: string };
  recommended: boolean;
}

const TIERS: PricingTier[] = [
  {
    id: 'starter',
    name: 'Starter',
    description: 'Cho team nhỏ 1-5 người bắt đầu quản lý pipeline',
    priceMonthly: 199000,
    priceAnnual: 158000,
    features: [
      { text: 'Tối đa 5 người dùng', included: true },
      { text: 'Pipeline + Contacts + Deals', included: true },
      { text: 'Email + chat support', included: true },
      { text: 'Báo cáo cơ bản', included: true },
      { text: 'Không giới hạn deals', included: true },
      { text: 'Mobile app', included: true },
      { text: 'Tự động hóa workflow', included: false },
      { text: 'API + Webhook', included: false },
      { text: 'Custom SSO / SAML', included: false },
      { text: 'Dedicated CSM', included: false }
    ],
    cta: { label: 'Bắt đầu miễn phí', href: '/signup?plan=starter' },
    recommended: false
  },
  {
    id: 'pro',
    name: 'Pro',
    description: 'Cho team 5-50 người cần automation và báo cáo nâng cao',
    priceMonthly: 599000,
    priceAnnual: 479000,
    features: [
      { text: 'Tối đa 50 người dùng', included: true },
      { text: 'Mọi thứ ở Starter + ', included: true },
      { text: 'Workflow automation', included: true },
      { text: 'API + Webhook không giới hạn', included: true },
      { text: 'Báo cáo nâng cao + Forecast', included: true },
      { text: 'Email + chat + phone support', included: true },
      { text: 'Slack + Gmail integration', included: true },
      { text: 'Custom fields', included: true },
      { text: 'Custom SSO / SAML', included: false },
      { text: 'Dedicated CSM', included: false }
    ],
    cta: { label: 'Dùng thử 14 ngày', href: '/signup?plan=pro' },
    recommended: true
  },
  {
    id: 'enterprise',
    name: 'Enterprise',
    description: 'Cho tổ chức 50+ người với yêu cầu security cao',
    priceMonthly: 'contact',
    priceAnnual: 'contact',
    features: [
      { text: 'Không giới hạn người dùng', included: true },
      { text: 'Mọi thứ ở Pro + ', included: true },
      { text: 'Custom SSO / SAML / SCIM', included: true },
      { text: 'Dedicated CSM 24/7', included: true },
      { text: 'Custom SLA 99.99%', included: true },
      { text: 'Audit log + Compliance', included: true },
      { text: 'On-premise deployment', included: true },
      { text: 'Custom training cho team', included: true },
      { text: 'Hợp đồng pháp lý tùy chỉnh', included: true },
      { text: 'Báo cáo tùy chỉnh', included: true }
    ],
    cta: { label: 'Liên hệ sales', href: '/contact?plan=enterprise' },
    recommended: false
  }
];

export function PricingTierSection() {
  const [billing, setBilling] = useState<'monthly' | 'annual'>('annual');

  return (
    <section className="bg-white py-16 lg:py-24" aria-labelledby="pricing-heading">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-12">
          <span className="inline-block text-[11px] font-bold uppercase tracking-[0.18em] text-indigo-600 mb-2">
            Pricing
          </span>
          <h2 id="pricing-heading" className="text-3xl lg:text-5xl font-extrabold text-slate-900 tracking-tight">
            Chọn gói phù hợp với team
          </h2>
          <p className="mt-3 text-slate-600 max-w-2xl mx-auto">
            14 ngày dùng thử miễn phí, không cần thẻ tín dụng. Hủy bất kỳ lúc nào.
          </p>

          {/* Monthly / Annual toggle */}
          <div className="mt-6 inline-flex items-center gap-1 p-1 bg-slate-100 rounded-lg" role="tablist" aria-label="Chu kỳ thanh toán">
            <button
              role="tab"
              aria-selected={billing === 'monthly'}
              onClick={() => setBilling('monthly')}
              className={`px-4 py-2 text-[13px] font-semibold rounded-md transition-colors ${
                billing === 'monthly' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500 hover:text-slate-700'
              }`}
            >
              Monthly
            </button>
            <button
              role="tab"
              aria-selected={billing === 'annual'}
              onClick={() => setBilling('annual')}
              className={`px-4 py-2 text-[13px] font-semibold rounded-md transition-colors inline-flex items-center gap-1.5 ${
                billing === 'annual' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500 hover:text-slate-700'
              }`}
            >
              Annual
              <span className="inline-flex items-center gap-0.5 px-1.5 py-0.5 bg-emerald-100 text-emerald-700 text-[10.5px] font-bold rounded">
                -20%
              </span>
            </button>
          </div>
        </div>

        {/* Tiers */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-5 lg:gap-6 max-w-6xl mx-auto">
          {TIERS.map(tier => (
            <PricingCard key={tier.id} tier={tier} billing={billing} />
          ))}
        </div>

        {/* Footer note */}
        <p className="mt-10 text-center text-[13px] text-slate-500">
          Tất cả gói bao gồm: SSL · GDPR-compliant · Backups hàng ngày · 99.9% uptime
        </p>
      </div>
    </section>
  );
}

function PricingCard({ tier, billing }: { tier: PricingTier; billing: 'monthly' | 'annual' }) {
  const price = billing === 'annual' ? tier.priceAnnual : tier.priceMonthly;

  return (
    <article
      aria-label={`Gói ${tier.name}`}
      className={`relative bg-white rounded-2xl border-2 ${
        tier.recommended ? 'border-indigo-500 shadow-2xl' : 'border-slate-200 shadow-sm'
      } p-6 lg:p-7 hover:shadow-lg transition-shadow`}
    >
      {tier.recommended && (
        <div className="absolute -top-3 left-1/2 -translate-x-1/2 px-3 py-1 bg-gradient-to-r from-indigo-600 to-indigo-700 text-white text-[11px] font-bold uppercase tracking-wider rounded-full shadow-lg inline-flex items-center gap-1" aria-label="Gói được đề xuất">
          <Phosphor.Sparkle size={11} weight="fill" />
          Đề xuất
        </div>
      )}

      {/* Header */}
      <div>
        <h3 className="text-[20px] font-extrabold text-slate-900 flex items-center gap-2">
          {tier.recommended && <Phosphor.Crown size={20} weight="fill" className="text-indigo-600" />}
          {tier.name}
        </h3>
        <p className="mt-2 text-[13px] text-slate-600 leading-relaxed">
          {tier.description}
        </p>
      </div>

      {/* Price */}
      <div className="mt-6 mb-6">
        {price === 'contact' ? (
          <p className="text-[28px] font-extrabold text-slate-900">Liên hệ</p>
        ) : (
          <div className="flex items-baseline gap-1.5">
            <span className="text-[10px] font-bold text-indigo-600">₫</span>
            <span aria-label={`Giá ${price.toLocaleString('vi-VN')} đồng mỗi người dùng mỗi tháng`} className="text-[44px] font-extrabold text-slate-900 tabular-nums leading-none">
              {price.toLocaleString('vi-VN')}
            </span>
            <span className="text-[13px] text-slate-500 font-medium">/user/tháng</span>
          </div>
        )}
        {billing === 'annual' && price !== 'contact' && (
          <p className="mt-1 text-[11.5px] text-emerald-600 font-semibold">
            Tiết kiệm 20% khi thanh toán annual
          </p>
        )}
      </div>

      {/* Features */}
      <ul className="space-y-2.5 mb-6">
        {tier.features.map((f, i) => (
          <li key={i} className="flex items-start gap-2 text-[13px]">
            {f.included ? (
              <Phosphor.CheckCircle size={16} weight="fill" className="text-emerald-500 flex-shrink-0 mt-0.5" />
            ) : (
              <Phosphor.X size={16} weight="bold" className="text-slate-300 flex-shrink-0 mt-0.5" />
            )}
            <span className={f.included ? 'text-slate-700' : 'text-slate-400 line-through'}>{f.text}</span>
          </li>
        ))}
      </ul>

      {/* CTA */}
      <a
        href={tier.cta.href}
        className={`flex items-center justify-center gap-1.5 w-full py-3 text-[13.5px] font-bold rounded-xl transition-colors ${
          tier.recommended
            ? 'bg-gradient-to-r from-indigo-600 to-indigo-700 hover:from-indigo-700 hover:to-indigo-800 text-white shadow-lg shadow-indigo-200'
            : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
        }`}
      >
        {tier.cta.label}
        <Phosphor.ArrowRight size={14} weight="bold" />
      </a>
    </article>
  );
}
```

## 8. Accessibility

- Pricing section `aria-labelledby`
- Monthly/Annual tabs `role="tablist"` + `aria-selected`
- Tier name là `<h3>`
- Recommended badge có `aria-label`
- Price có `aria-label` mô tả đầy đủ
- Feature list là `<ul>` semantic
- CTA accessible
- Reduce-motion: toggle transitions off

## 9. Performance

- Tabs state local
- No re-mount khi toggle billing
- Hover transition subtle

## 10. Anti-patterns đã tránh

- ❌ 4-equal cards (đã 3 tiers)
- ❌ Featured icon không label (đã aria-label)
- ❌ No price context (đã có /user/tháng)
- ❌ Hidden feature differences (đã list đầy đủ)

---

**Component family**: Marketing Landing — `pricing-tier`