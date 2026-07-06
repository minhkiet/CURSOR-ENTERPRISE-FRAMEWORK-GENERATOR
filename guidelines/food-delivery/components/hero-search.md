# Mega Hero + Search + Categories Strip

> Homepage hero với search bar (location picker + restaurant/dish input), trust strip ngay dưới, và category circles strip 8-10 cuisine types.

## 1. Mục đích

First-screen focus: tìm món/quán nhanh. Location selector prominent vì Bowl & Bite là local delivery. Categories cho phép browse by mood.

## 2. Asset

| Element | Source |
|---|---|
| Hero bg photo | Unsplash curated Vietnamese street food / restaurant interior |
| Category icons | Phosphor + Unsplash curated dish photo |
| Trust badges | Phosphor icons + text |

## 3. Cấu trúc

```
┌────────────────────────────────────────────────────────┐
│ [hero photo: vibrant Vietnamese street food market]   │
│                                                        │
│ Eat good. Get it fast.                                 │
│ 3.200+ quán · Giao 25 phút · Hà Nội & TP.HCM         │
│                                                        │
│ ┌──────────────────────────────────────────────────┐  │
│ │ 📍 Giao đến: Quận 1, TP.HCM          ▼           │  │
│ │ ┌──────────────────┬─────────┬────────────────┐  │  │
│ │ │ Tìm món, quán... │ 🍜 Phở │ [Tìm đồ ăn]    │  │  │
│ │ └──────────────────┴─────────┴────────────────┘  │  │
│ └──────────────────────────────────────────────────┘  │
│                                                        │
│ [Free ship 24/7] [3.200+ quán] [25 min avg] [4.8★]   │
└────────────────────────────────────────────────────────┘

[Categories strip - dưới hero]
┌────────────────────────────────────────────────────────┐
│ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐              │
│ │🍜│ │🍚│ │🥖│ │🍲│ │🥤│ │🍰│ │☕│ │🥗│              │
│ │Phở│ │Cơm│ │Bánh│ │Lẩu│ │Trà│ │Chè│ │Cà │ │Vegan│   │
│ └──┘ └──┘ └──┘ └──┘ └──┘ └──┘ └──┘ └──┘              │
└────────────────────────────────────────────────────────┘
```

## 4. Variants

| Variant | Use | Khác biệt |
|---|---|---|
| `default` | Homepage | Hero + search + categories |
| `compact` | Sub-page | Search bar only |
| `authed` | Returning user | Greeting + recent orders |

## 5. States

| State | Visual |
|---|---|
| default | Hero + categories interactive |
| location-picker-open | Dropdown với saved + current |
| search-focused | Border green + suggestions |
| reduce-motion | Static hero image |

## 6. Icon mapping

| Role | Phosphor |
|---|---|
| Pin | `MapPin` (fill) |
| Search | `MagnifyingGlass` |
| Dropdown | `CaretDown` |
| Phở | `BowlFood` |
| Cơm | `RiceBowl` |
| Bánh mì | `Bread` |
| Lẩu | `CookingPot` |
| Trà sữa | `Coffee` |
| Chè | `IceCream` |
| Cà phê | `Coffee` (alt) |
| Vegan | `Leaf` |
| Bún | `Noodles` |
| Bún bò | `Noodles` + spicy overlay |
| Ship | `Motorcycle` |
| Time | `Clock` |
| Star | `Star` (fill) |
| Trust | `SealCheck` (fill) |

## 7. Code reference

```tsx
'use client';
import { useState } from 'react';
import * as Phosphor from '@phosphor-icons/react';

const CATEGORIES = [
  { id: 'pho', name: 'Phở', image: '1576577445504-6af96477db52', count: 247 },
  { id: 'com', name: 'Cơm tấm', image: '1565299624946-b28f40a0ae38', count: 189 },
  { id: 'banhmi', name: 'Bánh mì', image: '1559054663-e8d23213f55c', count: 156 },
  { id: 'bun', name: 'Bún', image: '1569718212165-3a8278d5f624', count: 213 },
  { id: 'lau', name: 'Lẩu', image: '1547573854-74d2a71d0826', count: 78 },
  { id: 'trasua', name: 'Trà sữa', image: '1556679343-c7306c1976bc', count: 312 },
  { id: 'che', name: 'Chè', image: '1551024506-0bccd828d307', count: 134 },
  { id: 'caphe', name: 'Cà phê', image: '1495474472287-4d71bcdd2085', count: 287 },
  { id: 'vegan', name: 'Đồ chay', image: '1546069901-ba9599a7e63c', count: 95 },
  { id: 'dessert', name: 'Tráng miệng', image: '1551024506-0bccd828d307', count: 167 }
];

export function MegaHeroFood() {
  const [location, setLocation] = useState('Quận 1, TP.HCM');

  return (
    <>
      <section className="relative bg-slate-900 overflow-hidden" aria-label="Tìm đồ ăn">
        {/* Hero photo bg */}
        <div className="absolute inset-0 h-[680px] lg:h-[720px]" aria-hidden="true">
          <img
            src="https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=1920&h=1080&fit=crop&q=80"
            alt=""
            className="w-full h-full object-cover"
            style={{ filter: 'saturate(1.10) brightness(0.7) contrast(1.05)' }}
          />
          <div className="absolute inset-0 bg-gradient-to-b from-slate-900/60 via-slate-900/30 to-slate-900/80" />
        </div>

        {/* Content */}
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-16 pb-32 lg:pt-20 lg:pb-40">
          {/* Eyebrow */}
          <div className="inline-flex items-center gap-2 px-3 py-1.5 bg-emerald-500/20 backdrop-blur border border-emerald-400/30 rounded-full text-emerald-300 text-[11px] font-bold uppercase tracking-wider mb-6">
            <Phosphor.SealCheck size={14} weight="fill" />
            3.200+ quán đã verify · 4.8★ từ 487.000 đánh giá
          </div>

          {/* Headline */}
          <h1 className="text-white text-[40px] sm:text-[56px] lg:text-[80px] font-extrabold leading-[1.05] tracking-tight max-w-3xl">
            Ăn ngon.<br />
            <span className="text-emerald-400">Giao 25 phút.</span>
          </h1>

          {/* Subtitle */}
          <p className="mt-6 text-white/85 text-[16px] lg:text-[18px] leading-relaxed max-w-xl">
            Từ phở bò tái đến bún chả Hà Nội. Đặt trước tích điểm, đổi free ship.
          </p>

          {/* Search widget */}
          <div className="mt-8 bg-white rounded-2xl shadow-2xl p-3 lg:p-4 max-w-3xl">
            {/* Location row */}
            <button
              type="button"
              className="flex items-center gap-2 px-3 py-2 hover:bg-slate-50 rounded-lg transition-colors w-full text-left"
            >
              <Phosphor.MapPin size={16} weight="fill" className="text-emerald-600" />
              <span className="text-[11px] text-slate-500 font-bold uppercase tracking-wider">Giao đến</span>
              <span className="text-[14px] font-bold text-slate-900">{location}</span>
              <Phosphor.CaretDown size={14} weight="bold" className="text-slate-400 ml-auto" />
            </button>

            {/* Search row */}
            <div className="mt-2 flex items-stretch gap-2">
              <div className="relative flex-1">
                <Phosphor.MagnifyingGlass size={16} weight="bold" className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                <input
                  type="text"
                  placeholder="Phở, bún chả, cơm tấm..."
                  className="w-full pl-10 pr-3 py-3 bg-slate-50 hover:bg-slate-100 border border-slate-200 rounded-lg text-[14px] focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:bg-white"
                />
              </div>
              <button className="px-6 py-3 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-lg inline-flex items-center gap-2 whitespace-nowrap">
                <Phosphor.MagnifyingGlass size={16} weight="bold" />
                Tìm đồ ăn
              </button>
            </div>
          </div>

          {/* Trust strip */}
          <div className="mt-8 flex flex-wrap items-center gap-x-6 gap-y-2 text-white/85 text-[13px]">
            <span className="inline-flex items-center gap-1.5">
              <Phosphor.Motorcycle size={14} weight="fill" className="text-emerald-400" />
              <strong className="font-bold">Freeship</strong> 24/7 đơn từ 99.000₫
            </span>
            <span className="inline-flex items-center gap-1.5">
              <Phosphor.Clock size={14} weight="fill" className="text-emerald-400" />
              Trung bình <strong className="font-bold">25 phút</strong>
            </span>
            <span className="inline-flex items-center gap-1.5">
              <Phosphor.SealCheck size={14} weight="fill" className="text-emerald-400" />
              <strong className="font-bold">3.200+</strong> quán verified
            </span>
          </div>
        </div>
      </section>

      {/* Categories strip */}
      <section className="bg-white -mt-12 relative z-10" aria-label="Danh mục món">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center gap-4 overflow-x-auto pb-2 -mx-2 px-2 scrollbar-hide">
            {CATEGORIES.map(cat => (
              <a
                key={cat.id}
                href={`/c/${cat.id}`}
                className="group flex-shrink-0 flex flex-col items-center gap-2 w-20"
              >
                <div className="w-16 h-16 rounded-full overflow-hidden bg-slate-100 ring-2 ring-slate-100 group-hover:ring-emerald-500 transition-all">
                  <img
                    src={`https://images.unsplash.com/photo-${cat.image}?w=128&h=128&fit=crop&q=80`}
                    alt={cat.name}
                    className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                    style={{ filter: 'saturate(1.10) brightness(1.03)' }}
                    loading="lazy"
                  />
                </div>
                <div className="text-center">
                  <p className="text-[12.5px] font-bold text-slate-900 group-hover:text-emerald-600 transition-colors">
                    {cat.name}
                  </p>
                  <p className="text-[10px] text-slate-500 tabular-nums">{cat.count} quán</p>
                </div>
              </a>
            ))}
          </div>
        </div>
      </section>
    </>
  );
}
```

## 8. Accessibility

- Hero section `aria-label`
- Hero photo bg `aria-hidden="true"` (decorative)
- Eyebrow badge có icon + text
- Location button accessible, focus rõ
- Search input có placeholder + label sr-only
- CTA button có visible text
- Trust strip có icon + text, không chỉ màu
- Categories là `<a>` thật, focus visible
- Image alt mô tả tên món
- Reduce-motion: hero photo tĩnh
- Category strip là horizontal scroll với scroll-snap

## 9. Performance

- Hero image LCP candidate, preload
- Hero photo có filter subtle để appetite
- Categories scroll horizontal dùng scroll-snap native
- Images 128x128 cho categories, lazy load
- Search input native HTML, browser autocomplete

## 10. Anti-patterns đã tránh

- ❌ 3-equal feature card
- ❌ Generic cream
- ❌ Stock "person eating"
- ❌ Picsum random
- ❌ Emoji-only category (đã image thật)
- ❌ Generic category names

---

**Component family**: Layout #1 — `mega-hero-with-search-categories`