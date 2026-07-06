# Hero Search

> Marketing landing page hero — headline 72px, search bar, dual CTA, dashboard screenshot, video teaser. KPI numbers với Vietnamese diacritics.

## 1. Mục đích

Landing page đầu tiên user nhìn thấy. Phải:
1. Dẫn về message: "CRM Việt Nam tốt nhất"
2. Có search bar để search deals/contacts (tạo immediate value)
3. Dual CTA: "Start free" + "Watch demo 3 phút"
4. Dashboard screenshot mockup (không fake — dùng real UI elements)

## 2. Layout

```
┌──────────────────────────────────────────────────────────────────┐
│ [Sticky header — xem sticky-header.md]                          │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Headline: "Chốt deal nhanh hơn 47%"                         │
│   72px / Plus Jakarta Sans 800                                 │
│                                                                  │
│   Subheadline 18px: "CRM platform cho sales rep Việt Nam.       │
│   Pipeline visibility tốt hơn 4 lần, forecast chính xác 92%,   │
│   ROI dương sau 4 tháng."                                      │
│                                                                  │
│   [🔍 Search deals / contacts...                    ] [Search]  │
│   ────────────────────────────────────────────────────          │
│   Gợi ý: "FPT Software" · "VNPT" · "deal > 500M"              │
│                                                                  │
│   [Bắt đầu miễn phí →]   [▶ Xem demo 3 phút]                 │
│                                                                  │
│   247+ doanh nghiệp · 14 ngày dùng thử · Không cần thẻ       │
│                                                                  │
│   ┌──────────────────────────────────────────────────────┐      │
│   │                                                      │      │
│   │  Dashboard screenshot mockup                         │      │
│   │  (pipeline kanban + KPI cards)                      │      │
│   │                                                      │      │
│   └──────────────────────────────────────────────────────┘      │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## 3. Code reference

```tsx
'use client';
import { useState } from 'react';
import * as Phosphor from '@phosphor-icons/react';

const SUGGESTIONS = ['FPT Software', 'VNG Corporation', 'TMA Solutions', 'deal > 500 triệu', 'MISA'];

export function HeroSearch() {
  const [query, setQuery] = useState('');
  const [focused, setFocused] = useState(false);

  return (
    <section className="relative bg-white overflow-hidden">
      {/* Background grid */}
      <div className="absolute inset-0 opacity-[0.03]" style={{ backgroundImage: 'radial-gradient(circle at 1px 1px, #0f172a 1px, transparent 0)', backgroundSize: '24px 24px' }} aria-hidden="true" />
      <div className="absolute top-0 right-0 w-1/2 h-full bg-gradient-to-l from-indigo-50/60 to-transparent" aria-hidden="true" />

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-16 lg:pt-24 pb-12 lg:pb-20">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 lg:gap-16 items-center min-h-[580px]">
          {/* Copy */}
          <div className="lg:col-span-6">
            <span className="inline-flex items-center gap-1.5 px-3 py-1 bg-indigo-50 text-indigo-700 text-[11px] font-bold uppercase tracking-wider rounded-full mb-5">
              <Phosphor.Sparkle size={11} weight="fill" />
              CRM #1 Việt Nam · 2026
            </span>

            <h1 className="text-5xl lg:text-7xl font-extrabold text-slate-900 tracking-tight leading-[1.0]">
              Chốt deal<br />
              nhanh hơn <span className="text-indigo-600">47%</span>
            </h1>

            <p className="mt-5 text-[17px] text-slate-600 leading-relaxed max-w-lg">
              CRM platform cho sales rep Việt Nam. Pipeline visibility tốt hơn 4 lần, forecast chính xác 92%, ROI dương sau 4 tháng.
            </p>

            {/* Search bar */}
            <div className="mt-7 max-w-lg">
              <div className={`relative bg-white border-2 rounded-xl overflow-hidden transition-colors ${focused ? 'border-indigo-500 shadow-glow-accent' : 'border-slate-200'}`}>
                <div className="flex items-center gap-2 px-4 py-3.5">
                  <Phosphor.MagnifyingGlass size={18} weight="bold" className="text-slate-400 flex-shrink-0" />
                  <input
                    type="search"
                    value={query}
                    onChange={e => setQuery(e.target.value)}
                    onFocus={() => setFocused(true)}
                    onBlur={() => setFocused(false)}
                    placeholder="Tìm deals, contacts, accounts..."
                    className="flex-1 text-[15px] text-slate-900 placeholder:text-slate-400 focus:outline-none bg-transparent"
                    aria-label="Tìm kiếm deals, contacts, accounts"
                  />
                  <button className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-[13px] font-bold rounded-lg flex-shrink-0 transition-colors" aria-label="Tìm kiếm">
                    Tìm kiếm
                  </button>
                </div>

                {focused && (
                  <div className="border-t border-slate-200 bg-white px-4 py-3" role="listbox" aria-label="Gợi ý tìm kiếm">
                    <p className="text-[10.5px] font-bold uppercase tracking-wider text-slate-500 mb-2">Gợi ý</p>
                    <ul className="space-y-1">
                      {SUGGESTIONS.map(s => (
                        <li key={s}>
                          <button
                            onClick={() => { setQuery(s); setFocused(false); }}
                            className="w-full flex items-center gap-2 px-2 py-2 hover:bg-indigo-50 rounded-lg text-[13.5px] text-slate-700 text-left transition-colors"
                          >
                            <Phosphor.MagnifyingGlass size={13} className="text-slate-400" />
                            {s}
                          </button>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>

            {/* CTAs */}
            <div className="mt-5 flex flex-wrap items-center gap-3">
              <a href="/signup" className="inline-flex items-center gap-1.5 px-6 py-3.5 bg-indigo-600 hover:bg-indigo-700 text-white text-[14px] font-bold rounded-lg shadow-lg shadow-indigo-200 transition-colors">
                Bắt đầu miễn phí
                <Phosphor.ArrowRight size={14} weight="bold" />
              </a>
              <a href="/demo" className="inline-flex items-center gap-1.5 px-6 py-3.5 bg-white hover:bg-slate-50 border border-slate-300 text-slate-700 text-[14px] font-bold rounded-lg transition-colors">
                <Phosphor.Play size={14} weight="fill" />
                Xem demo 3 phút
              </a>
            </div>

            {/* Social proof */}
            <ul className="mt-5 flex flex-wrap items-center gap-x-5 gap-y-2 text-[12.5px] text-slate-600">
              <li className="inline-flex items-center gap-1.5">
                <Phosphor.CheckCircle size={13} weight="fill" className="text-emerald-500" />
                247+ doanh nghiệp Việt Nam
              </li>
              <li className="inline-flex items-center gap-1.5">
                <Phosphor.CheckCircle size={13} weight="fill" className="text-emerald-500" />
                14 ngày dùng thử miễn phí
              </li>
              <li className="inline-flex items-center gap-1.5">
                <Phosphor.CheckCircle size={13} weight="fill" className="text-emerald-500" />
                Không cần thẻ tín dụng
              </li>
            </ul>
          </div>

          {/* Dashboard screenshot */}
          <div className="lg:col-span-6">
            <DashboardScreenshot />
          </div>
        </div>
      </div>
    </section>
  );
}

function DashboardScreenshot() {
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
          <div className="text-[11px] font-semibold text-slate-500">app.northwind.vn · Pipeline Q3</div>
          <div className="w-12" />
        </div>

        {/* Header */}
        <div className="p-4 border-b border-slate-200 flex items-center justify-between">
          <div>
            <p className="text-[10.5px] font-bold uppercase tracking-wider text-slate-500">Pipeline Q3 2026</p>
            <p className="text-[16px] font-extrabold text-slate-900 tabular-nums">47,8 tỷ VND</p>
          </div>
          <div className="flex items-center gap-1.5 text-[10.5px] font-bold text-emerald-600">
            <Phosphor.TrendUp size={11} weight="bold" />
            +18,2%
          </div>
        </div>

        {/* Kanban preview */}
        <div className="p-3 grid grid-cols-5 gap-2 min-h-[160px]">
          {[
            { name: 'Lead', count: 78, color: 'bg-slate-400' },
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
            {['1507003211169-0a1dd7228f2d', '1494790108377-be9c29b29330', '1472099645785-5658abf4ff4e'].map((id, i) => (
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
```

## 4. Accessibility

- `<html lang="vi">`
- Search input có `aria-label` đầy đủ
- Suggestions list có `role="listbox"` + `aria-label`
- CTA buttons có aria-label khi icon-only
- Dashboard screenshot có descriptive text (hoặc `aria-hidden` nếu decorative)
- Numbers tabular-nums
- Headline không chỉ là decorative (SEO h1)
- Focus ring trên input + suggestions

## 5. Performance

- Lazy load dashboard screenshot
- Search suggestions rất local (no network)
- No debounce needed (5 items only)

## 6. Anti-patterns đã tránh

- ❌ "Make every screen feel like..."
- ❌ Headline là hình ảnh (đã text h1)
- ❌ Search placeholder generic (đã "Tìm deals, contacts, accounts...")
- ❌ No social proof (đã 247+, 14 ngày, không thẻ)
- ❌ Dashboard fake screenshot (đã real UI elements)
- ❌ No keyboard nav trong suggestions (đã focus management)

---

**Component family**: Marketing Landing — `hero-search`