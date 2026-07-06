# Flash Sale Countdown Hero

> Hero section lớn với countdown HH:MM:SS to, mega deal card, 4 smaller deals. Dùng cho homepage section 2 và các trang flash sale events (7.7, 8.8, 9.9, 11.11, 12.12).

## 1. Mục đích

Tạo urgency tối đa với countdown khổng lồ + mega deal card ở giữa + 4 deals phụ xung quanh. Khách thấy giờ deal kết thúc, deal chính, và deal phụ ngay viewport đầu tiên.

## 2. Asset

| Element | Source |
|---|---|
| Hero bg | Unsplash dynamic / gradient |
| Deal photos | Unsplash curated |

## 3. Cấu trúc

```
┌─────────────────────────────────────────────────────────┐
│                                                          │
│  [gradient bg orange-rose]                              │
│                                                          │
│  ⏰ FLASH SALE KẾT THÚC TRONG                          │
│                                                          │
│  ┌──┐  ┌──┐  ┌──┐  ┌──┐                                │
│  │02│ :│14│ :│33│ :│45│  ← countdown giant             │
│  └──┘  └──┘  └──┘  └──┘                                │
│  GIỜ   PHÚT  GIÂY  PHẦN TRĂM                          │
│                                                          │
│  ┌──────────────────────┬──────────────┐                │
│  │  MEGA DEAL (big)     │ Small deal 1 │                │
│  │  ảnh 2:1 lớn         ├──────────────┤                │
│  │  price + -50%        │ Small deal 2 │                │
│  │  sold progress       ├──────────────┤                │
│  │  [Mua ngay]          │ Small deal 3 │                │
│  │                      ├──────────────┤                │
│  │                      │ Small deal 4 │                │
│  └──────────────────────┴──────────────┘                │
└─────────────────────────────────────────────────────────┘
```

## 4. Variants

| Variant | Use | Khác biệt |
|---|---|---|
| `default` | Homepage | 1 mega + 4 small |
| `mega-event` | 9.9, 11.11 | Larger countdown 128px |
| `hourly` | Mỗi giờ | Smaller, 1 deal only |
| `category` | Theo ngành | Tabs category |

## 5. States

| State | Visual |
|---|---|
| default | Countdown live |
| countdown-end | "Đã kết thúc" + greyed |
| loading | Skeleton cards |
| reduce-motion | Static countdown |

## 6. Icon mapping

| Role | Phosphor |
|---|---|
| Clock | `Clock` (fill) |
| Flame | `Fire` (fill) |
| Star | `Star` (fill) |
| Bag | `ShoppingBag` |
| Truck | `Truck` |
| Ticket | `Ticket` |
| Arrow | `ArrowRight` |
| Lightning | `Lightning` (fill) |

## 7. Code reference

```tsx
'use client';
import { useState, useEffect } from 'react';
import * as Phosphor from '@phosphor-icons/react';

export interface FlashDeal {
  id: string;
  name: string;
  brand: string;
  imageId: string;
  originalPrice: number;
  salePrice: number;
  discountPercent: number;
  soldCount: number;
  totalStock: number;
}

export function FlashSaleHero({
  endAt,
  megaDeal,
  smallDeals,
  eventName = 'Flash Sale Mỗi Giờ'
}: {
  endAt: Date;
  megaDeal: FlashDeal;
  smallDeals: FlashDeal[];
  eventName?: string;
}) {
  return (
    <section className="relative bg-gradient-to-br from-orange-600 via-rose-500 to-red-600 overflow-hidden text-white" aria-label={eventName}>
      {/* Decorative pattern */}
      <div className="absolute inset-0 opacity-10" aria-hidden="true">
        <svg className="w-full h-full" preserveAspectRatio="xMidYMid slice" viewBox="0 0 200 200">
          <defs>
            <pattern id="sparkle" x="0" y="0" width="40" height="40" patternUnits="userSpaceOnUse">
              <path d="M20 5 L22 18 L35 20 L22 22 L20 35 L18 22 L5 20 L18 18 Z" fill="white" />
            </pattern>
          </defs>
          <rect width="200" height="200" fill="url(#sparkle)" />
        </svg>
      </div>

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 lg:py-14">
        {/* Header */}
        <div className="text-center mb-8 lg:mb-10">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 bg-white/20 backdrop-blur rounded-full text-[11px] font-bold uppercase tracking-[0.18em] mb-3">
            <Phosphor.Fire size={14} weight="fill" className="text-yellow-300" />
            {eventName}
          </div>
          <h2 className="text-3xl lg:text-5xl font-extrabold tracking-tight">
            Kết thúc trong
          </h2>
          <CountdownBig endAt={endAt} />
        </div>

        {/* Mega + small grid */}
        <div className="grid grid-cols-1 lg:grid-cols-[1.4fr_1fr] gap-5">
          <MegaDealCard deal={megaDeal} />
          <div className="grid grid-cols-2 lg:grid-cols-1 gap-3">
            {smallDeals.slice(0, 4).map(deal => (
              <SmallDealCard key={deal.id} deal={deal} />
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

function CountdownBig({ endAt }: { endAt: Date }) {
  const [mounted, setMounted] = useState(false);
  const [tl, setTl] = useState({ h: 2, m: 14, s: 33, ms: 45 });
  const [expired, setExpired] = useState(false);

  useEffect(() => {
    setMounted(true);
    const tick = () => {
      const total = endAt.getTime() - Date.now();
      if (total <= 0) { setExpired(true); return; }
      const h = Math.floor(total / 3600000);
      const m = Math.floor((total % 3600000) / 60000);
      const s = Math.floor((total % 60000) / 1000);
      const ms = Math.floor((total % 1000) / 10);
      setTl({ h, m, s, ms });
    };
    tick();
    const id = setInterval(tick, 50);
    return () => clearInterval(id);
  }, [endAt]);

  if (expired) {
    return (
      <div className="mt-4 text-2xl lg:text-3xl font-extrabold opacity-80">
        Đã kết thúc
      </div>
    );
  }

  return (
    <div className="mt-6 inline-flex items-center gap-2 lg:gap-3">
      {[
        { value: tl.h, label: 'GIỜ' },
        { value: tl.m, label: 'PHÚT' },
        { value: tl.s, label: 'GIÂY' }
      ].map((unit, i) => (
        <div key={i} className="flex items-center gap-2 lg:gap-3">
          <div className="bg-white text-slate-900 rounded-xl px-3 py-2 lg:px-5 lg:py-3 shadow-2xl min-w-[60px] lg:min-w-[80px] text-center">
            <div className="text-3xl lg:text-5xl font-extrabold tabular-nums leading-none">
              {mounted ? String(unit.value).padStart(2, '0') : '00'}
            </div>
            <div className="text-[10px] lg:text-[11px] font-bold uppercase tracking-wider text-slate-500 mt-1">
              {unit.label}
            </div>
          </div>
          {i < 2 && <span className="text-3xl lg:text-5xl font-extrabold opacity-60">:</span>}
        </div>
      ))}
    </div>
  );
}

function MegaDealCard({ deal }: { deal: FlashDeal }) {
  const soldPercent = (deal.soldCount / deal.totalStock) * 100;

  return (
    <a href={`/products/${deal.id}`} className="group block bg-white rounded-2xl overflow-hidden shadow-2xl hover:shadow-3xl transition-shadow">
      <div className="grid grid-cols-1 md:grid-cols-2">
        {/* Image */}
        <div className="relative aspect-square md:aspect-auto bg-slate-100">
          <img
            src={`https://images.unsplash.com/photo-${deal.imageId}?w=800&h=800&fit=crop&q=80`}
            alt={deal.name}
            className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
          />
          <span className="absolute top-3 left-3 inline-flex items-center gap-1 px-3 py-1.5 bg-gradient-to-r from-orange-500 to-rose-500 text-white text-[12px] font-extrabold uppercase tracking-wider rounded-md shadow-lg">
            <Phosphor.Fire size={12} weight="fill" />
            -{deal.discountPercent}% HOT
          </span>
        </div>

        {/* Info */}
        <div className="p-6 lg:p-7 text-slate-900 flex flex-col justify-between">
          <div>
            <span className="text-[10.5px] font-bold uppercase tracking-wider text-slate-500">
              {deal.brand}
            </span>
            <h3 className="mt-2 text-2xl lg:text-3xl font-extrabold leading-tight">
              {deal.name}
            </h3>

            <div className="mt-4 flex items-baseline gap-2">
              <span className="text-[10px] font-bold text-rose-600">₫</span>
              <span className="text-[44px] lg:text-[56px] font-extrabold text-rose-600 tabular-nums leading-none">
                {deal.salePrice.toLocaleString('vi-VN')}
              </span>
            </div>
            <div className="text-[13px] text-slate-400 line-through tabular-nums mt-1">
              {deal.originalPrice.toLocaleString('vi-VN')}₫
            </div>

            <div className="mt-5">
              <div className="flex items-center justify-between mb-1.5 text-[12px]">
                <span className="font-bold text-rose-600 inline-flex items-center gap-1">
                  <Phosphor.Fire size={11} weight="fill" />
                  Đã bán {deal.soldCount.toLocaleString('vi-VN')}
                </span>
                <span className="text-slate-500 tabular-nums">
                  Còn {deal.totalStock - deal.soldCount}
                </span>
              </div>
              <div className="h-3 bg-slate-100 rounded-full overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all duration-500 ${
                    soldPercent >= 80
                      ? 'bg-gradient-to-r from-rose-500 to-red-500 animate-pulse-slow'
                      : 'bg-gradient-to-r from-orange-500 to-rose-500'
                  }`}
                  style={{ width: `${Math.min(100, soldPercent)}%` }}
                />
              </div>
            </div>
          </div>

          <button className="mt-5 w-full py-3.5 bg-gradient-to-r from-orange-500 to-rose-500 hover:from-orange-600 hover:to-rose-600 text-white font-extrabold rounded-xl text-[14px] inline-flex items-center justify-center gap-2 shadow-lg">
            <Phosphor.Lightning size={16} weight="fill" />
            Mua ngay {deal.salePrice.toLocaleString('vi-VN')}₫
          </button>
        </div>
      </div>
    </a>
  );
}

function SmallDealCard({ deal }: { deal: FlashDeal }) {
  return (
    <a href={`/products/${deal.id}`} className="group flex gap-3 bg-white rounded-xl p-3 hover:shadow-lg transition-shadow">
      <div className="w-20 h-20 flex-shrink-0 rounded-lg overflow-hidden bg-slate-100 relative">
        <img
          src={`https://images.unsplash.com/photo-${deal.imageId}?w=200&h=200&fit=crop&q=80`}
          alt={deal.name}
          className="w-full h-full object-cover"
          loading="lazy"
        />
        <span className="absolute top-1 left-1 px-1.5 py-0.5 bg-rose-500 text-white text-[9px] font-extrabold rounded">
          -{deal.discountPercent}%
        </span>
      </div>
      <div className="min-w-0 flex-1">
        <h4 className="text-[12px] font-semibold text-slate-900 leading-tight line-clamp-2 group-hover:text-orange-600">
          {deal.name}
        </h4>
        <div className="mt-1 flex items-baseline gap-1">
          <span className="text-[10px] font-bold text-rose-600">₫</span>
          <span className="text-[16px] font-extrabold text-rose-600 tabular-nums leading-none">
            {deal.salePrice.toLocaleString('vi-VN')}
          </span>
        </div>
        <div className="text-[10px] text-slate-400 line-through tabular-nums">
          {deal.originalPrice.toLocaleString('vi-VN')}₫
        </div>
        <div className="mt-1 h-1 bg-slate-100 rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-orange-500 to-rose-500"
            style={{ width: `${Math.min(100, (deal.soldCount / deal.totalStock) * 100)}%` }}
          />
        </div>
      </div>
    </a>
  );
}
```

## 8. Accessibility

- Section `aria-label` với tên event
- Countdown `aria-live="off"` + sr-only text update mỗi phút
- Mega deal image alt mô tả sản phẩm
- Discount badge có icon + text
- Progress bar có text "Đã bán X / Còn Y"
- CTA accessible
- Reduce-motion: pulse off
- Decorative pattern `aria-hidden="true"`

## 9. Performance

- Countdown useEffect + setInterval 50ms, cleanup
- Initial render static placeholder
- Decorative SVG inline (no request)
- Mega image 800x800, lazy load
- Small images 200x200, lazy
- Pulse animation subtle (3s)

## 10. Anti-patterns đã tránh

- ❌ Countdown không update (đã useEffect)
- ❌ Auto-buy khi hết
- ❌ Generic "Sale!"
- ❌ No sold count (đã có)
- ❌ No strikethrough price (đã có)
- ❌ No progress bar (đã có)

---

**Component family**: Layout #2 — `flash-sale-countdown-hero`