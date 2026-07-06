# Dashboard Widget Bento

> Bento grid asymmetric cho sales dashboard: KPI card lớn + secondary metrics + chart widget + activity feed + goal progress. Data-dense, keyboard-friendly.

## 1. Mục đích

Sales rep vào dashboard sáng thứ Hai phải hiểu trong 5 giây: tuần trước bao nhiêu revenue, deals nào cần follow-up, mình đang ở đâu trên target.

## 2. Layout (desktop)

```
┌──────────────────────────────────┬───────────────────────┐
│                                  │                       │
│  HERO KPI                        │  Secondary metric     │
│  Revenue Q3                      │  Win rate             │
│  47,8 tỷ VND                     │  68%                  │
│  +18% vs Q2                      │  +5pp vs last         │
│  [sparkline chart]               │                       │
│                                  ├───────────────────────┤
│                                  │                       │
│                                  │  Secondary metric     │
│                                  │  Avg deal size        │
│                                  │  195M VND             │
├──────────────────────────────────┴───────────────────────┤
│                                                          │
│  Activity feed (recent)                                 │
│  • Call logged with Tran Minh - 2h ago                  │
│  • Deal advanced: VNG → Negotiation - 4h ago           │
│                                                          │
├──────────────────────────────┬───────────────────────────┤
│                              │                           │
│  Goal progress               │  Stuck deals              │
│  Q3 target: 60 tỷ VND        │  7 deals need follow-up   │
│  [progress bar]  47,8 / 60   │  • Acme Corp - 5d no...   │
│  79.7%                       │  • BetaCo - 12d no...     │
│                              │                           │
└──────────────────────────────┴───────────────────────────┘
```

## 3. Variants

| Variant | Use | Khác biệt |
|---|---|---|
| `executive` | Sales rep | KPIs focus |
| `manager` | Manager | Team performance |
| `compact` | Home | Smaller cells |

## 4. States

| State | Visual |
|---|---|
| default | Standard |
| loading | Skeleton |
| error | "Không thể load" + retry |
| refresh | Subtle "Cập nhật lúc..." |

## 5. Icon mapping

| Role | Phosphor |
|---|---|
| Revenue | `CurrencyDollar` |
| Win | `Trophy` (fill) |
| Deal | `Briefcase` |
| Activity | `Pulse` |
| Up | `TrendUp` |
| Down | `TrendDown` |
| Goal | `Flag` |
| Stuck | `WarningCircle` (fill) |
| Call | `Phone` |
| Email | `EnvelopeSimple` |
| Meeting | `CalendarCheck` |
| Refresh | `ArrowClockwise` |

## 6. Code reference

```tsx
import * as Phosphor from '@phosphor-icons/react';

export function DashboardWidget() {
  return (
    <section className="bg-slate-50 p-6 lg:p-8 min-h-screen" aria-label="Dashboard doanh số">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex items-end justify-between mb-6 flex-wrap gap-3">
          <div>
            <span className="text-[11px] font-bold uppercase tracking-[0.18em] text-indigo-600 mb-1">Q3 2026 · Tuần 27</span>
            <h1 className="text-3xl lg:text-4xl font-extrabold text-slate-900 tracking-tight">
              Chào buổi sáng, Minh 👋
            </h1>
            <p className="text-[14px] text-slate-600 mt-1">
              3 deals cần follow-up hôm nay. Bạn đang đạt <strong className="text-emerald-600">79,7%</strong> target Q3.
            </p>
          </div>
          <div className="flex items-center gap-2">
            <button className="inline-flex items-center gap-1.5 px-3 py-2 bg-white hover:bg-slate-50 border border-slate-200 rounded-lg text-[12.5px] font-semibold text-slate-700" aria-label="Làm mới dữ liệu">
              <Phosphor.ArrowClockwise size={14} weight="bold" />
              Làm mới
            </button>
            <button className="inline-flex items-center gap-1.5 px-3 py-2 bg-white hover:bg-slate-50 border border-slate-200 rounded-lg text-[12.5px] font-semibold text-slate-700">
              Tuần này ↓
            </button>
          </div>
        </div>

        {/* Bento grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-4 lg:auto-rows-[140px]">
          {/* Hero KPI */}
          <article className="lg:col-span-3 lg:row-span-2 bg-gradient-to-br from-indigo-600 to-indigo-800 text-white rounded-2xl p-6 shadow-xl">
            <div className="flex items-center gap-2 mb-2">
              <Phosphor.CurrencyDollar size={18} weight="bold" className="text-indigo-200" />
              <span className="text-[11px] font-bold uppercase tracking-wider text-indigo-200">Revenue Q3</span>
            </div>
            <p className="text-[44px] lg:text-[56px] font-extrabold tabular-nums leading-none tracking-tight">
              47,8 <span className="text-[24px] text-indigo-200 font-bold">tỷ VND</span>
            </p>
            <div className="mt-2 inline-flex items-center gap-1 px-2 py-0.5 bg-emerald-500/20 text-emerald-300 rounded-full text-[12px] font-bold">
              <Phosphor.TrendUp size={11} weight="bold" />
              +18,2% vs Q2
            </div>

            {/* Sparkline */}
            <div className="mt-6" aria-label="Revenue 12 tuần tăng 18,2%">
              <svg viewBox="0 0 200 60" className="w-full h-16" role="img">
                <polyline points="0,52 17,48 34,45 51,40 68,38 85,32 102,30 119,25 136,22 153,18 170,12 187,8" fill="none" stroke="#a5b4fc" strokeWidth="2.5" strokeLinecap="round" />
                <polyline points="0,52 17,48 34,45 51,40 68,38 85,32 102,30 119,25 136,22 153,18 170,12 187,8 187,60 0,60" fill="rgba(165, 180, 252, 0.20)" stroke="none" />
                <text x="0" y="76" fill="white" fontSize="10" fontWeight="600">Tuần 16</text>
                <text x="180" y="76" fill="white" fontSize="10" fontWeight="600">Tuần 27</text>
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

          {/* Win rate */}
          <article className="lg:col-span-3 lg:row-span-1 bg-white rounded-2xl border border-slate-200 p-5 hover:shadow-lg transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-[11px] font-bold uppercase tracking-wider text-slate-500">Win rate</p>
                <p className="mt-1 text-[32px] font-extrabold text-slate-900 tabular-nums leading-none">
                  68%
                </p>
                <p className="mt-1 text-[11.5px] text-emerald-600 font-bold inline-flex items-center gap-1">
                  <Phosphor.TrendUp size={11} weight="bold" />
                  +5pp vs tháng trước
                </p>
              </div>
              <div className="w-16 h-16 rounded-full bg-emerald-100 flex items-center justify-center">
                <Phosphor.Trophy size={28} weight="fill" className="text-emerald-600" />
              </div>
            </div>
          </article>

          {/* Avg deal size */}
          <article className="lg:col-span-3 lg:row-span-1 bg-white rounded-2xl border border-slate-200 p-5 hover:shadow-lg transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-[11px] font-bold uppercase tracking-wider text-slate-500">Giá trị TB / deal</p>
                <p className="mt-1 text-[28px] font-extrabold text-slate-900 tabular-nums leading-none">
                  195<span className="text-[14px] text-slate-500 font-bold">M VND</span>
                </p>
                <p className="mt-1 text-[11.5px] text-rose-600 font-bold inline-flex items-center gap-1">
                  <Phosphor.TrendDown size={11} weight="bold" />
                  -8% vs tháng trước
                </p>
              </div>
              <div className="w-16 h-16 rounded-full bg-indigo-100 flex items-center justify-center">
                <Phosphor.Briefcase size={28} weight="fill" className="text-indigo-600" />
              </div>
            </div>
          </article>

          {/* Activity feed */}
          <article className="lg:col-span-4 lg:row-span-2 bg-white rounded-2xl border border-slate-200 p-5 hover:shadow-lg transition-shadow">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-[14px] font-bold text-slate-900 flex items-center gap-1.5">
                <Phosphor.Pulse size={16} weight="bold" className="text-indigo-600" />
                Hoạt động gần đây
              </h2>
              <a href="#" className="text-[11.5px] font-semibold text-indigo-600 hover:underline">Xem tất cả</a>
            </div>
            <ul className="space-y-3">
              {[
                { icon: 'Phone', color: 'indigo', text: <><strong>Minh</strong> gọi với <strong>Trần Minh</strong> · FPT Software</>, time: '2 giờ trước' },
                { icon: 'TrendUp', color: 'emerald', text: <><strong>Lan</strong> advance deal <strong>VNG Migration</strong> → Negotiation</>, time: '4 giờ trước' },
                { icon: 'EnvelopeSimple', color: 'sky', text: <><strong>Bảo</strong> gửi email cho <strong>TMA Solutions</strong></>, time: '6 giờ trước' },
                { icon: 'CalendarCheck', color: 'amber', text: <><strong>Lan</strong> họp với <strong>CTO VNG</strong></>, time: '1 ngày trước' },
                { icon: 'Trophy', color: 'emerald', text: <><strong>Minh</strong> close deal <strong>FPT License</strong> · 1,2 tỷ</>, time: '2 ngày trước' }
              ].map((a, i) => {
                const Icon = Phosphor[a.icon] as any;
                return (
                  <li key={i} className="flex items-start gap-3">
                    <div className={`w-8 h-8 rounded-full bg-${a.color}-100 flex items-center justify-center flex-shrink-0`}>
                      <Icon size={14} weight="bold" className={`text-${a.color}-600`} />
                    </div>
                    <div className="min-w-0 flex-1">
                      <p className="text-[12.5px] text-slate-800">{a.text}</p>
                      <p className="text-[11px] text-slate-500 mt-0.5 tabular-nums">{a.time}</p>
                    </div>
                  </li>
                );
              })}
            </ul>
          </article>

          {/* Stuck deals */}
          <article className="lg:col-span-2 lg:row-span-2 bg-rose-50 border border-rose-200 rounded-2xl p-5 hover:shadow-lg transition-shadow">
            <div className="flex items-center gap-2 mb-3">
              <Phosphor.WarningCircle size={18} weight="fill" className="text-rose-600" />
              <h2 className="text-[14px] font-bold text-rose-900">
                7 deals cần follow-up
              </h2>
            </div>
            <ul className="space-y-2">
              {[
                { name: 'Acme Corp', days: 5, value: '450M' },
                { name: 'BetaCo', days: 12, value: '1.2 tỷ' },
                { name: 'GammaTech', days: 8, value: '680M' },
                { name: 'Delta Ltd', days: 4, value: '230M' }
              ].map(d => (
                <li key={d.name} className="flex items-center justify-between p-2 bg-white rounded-lg hover:shadow-sm transition-shadow">
                  <div>
                    <p className="text-[12.5px] font-semibold text-slate-900">{d.name}</p>
                    <p className="text-[11px] text-rose-600 font-medium">{d.days} ngày không hoạt động</p>
                  </div>
                  <div className="text-right">
                    <p className="text-[12.5px] font-bold text-slate-900 tabular-nums">{d.value}</p>
                    <button aria-label={`Follow-up ${d.name}`} className="text-[10.5px] font-bold text-indigo-600 hover:underline">
                      Follow →
                    </button>
                  </div>
                </li>
              ))}
            </ul>
            <button className="mt-3 w-full py-2 bg-white hover:bg-rose-100 border border-rose-300 text-rose-700 text-[12px] font-bold rounded-lg">
              Xem tất cả 7 deals
            </button>
          </article>
        </div>
      </div>
    </section>
  );
}
```

## 7. Accessibility

- Section `aria-label`
- Bento cells là `<article>` semantic
- KPIs accessible với tabular-nums
- Sparkline có `role="img"` + `aria-label` text alternative
- `<dl>` semantic cho definition lists
- Activity feed là `<ul>` semantic
- Stuck deals có icon + text + color
- CTA buttons accessible
- Refresh button `aria-label`
- Reduce-motion: chart transitions off

## 8. Performance

- SVG sparkline inline (no request)
- KPI calculation memoized
- Avatar lazy load
- Chart colors semantic
- Bento grid dùng CSS Grid auto-rows
- Static placeholder OK

## 9. Anti-patterns đã tránh

- ❌ "Make every screen feel like..."
- ❌ 3 equal cards (đã bento asymmetric)
- ❌ Chart không có text alt (đã có)
- ❌ Number without context (đã có context)
- ❌ Emoji overload (1 chào buổi sáng)

---

**Component family**: In-app Cockpit — `dashboard-widget-bento`