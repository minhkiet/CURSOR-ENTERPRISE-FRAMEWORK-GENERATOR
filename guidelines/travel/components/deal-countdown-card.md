# Deal Countdown Card

> Card flash deal với countdown timer thật (HH:MM:SS), price gốc vs sale price, sold count, CTA đặt nhanh. Dùng trong homepage section 2 (Flash deal countdown strip) và homepage section 6 (Deals by category).

## 1. Mục đích

Khách thấy deal ngay trong viewport với countdown rõ ràng, sold count cho FOMO, 1-click CTA. Không cần click vào trang detail mới biết giá.

## 2. Asset

| Element | Source |
|---|---|
| Hero image | Unsplash destination |
| Brand logo (airline) | Simple Icons CDN |
| Rating icon | Phosphor `Star` (fill) |

## 3. Cấu trúc

```
┌─────────────────────────────────────┐
│  [hero 16:9]                  [♥]   │
│  ┌──────────┐                       │
│  │ -47% OFF │                       │
│  └──────────┘                       │
├─────────────────────────────────────┤
│ ✈ Vietnam Airlines                  │
│ Hà Nội → Đà Lạt                   │
│ ⭐ 4.7 (1.247) · Bay 2h15m        │
│                                     │
│ ┌──────────────────────────────┐   │
│ │ CÒN                         │   │
│ │ 02 : 14 : 33                 │   │  ← big mono countdown
│ │ GIỜ   PHÚT  GIÂY             │   │
│ └──────────────────────────────┘   │
│                                     │
│ 1.290.000₫   ̶2̶.̶4̶5̶0̶.̶0̶0̶0̶₫̶  │
│                                     │
│ Đã bán 487 vé · Còn 13 vé          │
│                                     │
│ [    Đặt ngay 1.290.000₫    ]     │
└─────────────────────────────────────┘
```

## 4. Variants

| Variant | Use | Khác biệt |
|---|---|---|
| `default` | Horizontal scroll | Standard |
| `featured` | Bento big | Larger countdown 64px |
| `tour` | Tour deal | Multi-day tour code |
| `hotel` | Hotel deal | Night price |
| `combo` | Flight + Hotel | 2 cards fused |
| `last-call` | Còn < 1h | Red urgent border + pulse |

## 5. States

| State | Visual |
|---|---|
| default | Standard |
| countdown-running | Cập nhật mỗi giây |
| countdown-end | "Đã hết hạn" + disable CTA |
| low-stock | Coral pulse + "Sắp hết" |
| hover | translateY(-2px) + shadow-lg |
| reduce-motion | Countdown static, không pulse |

## 6. Icon mapping

| Role | Phosphor |
|---|---|
| Plane | `AirplaneTilt` |
| Discount | `Tag` (fill) hoặc `Percent` |
| Star | `Star` (fill) |
| Duration | `HourglassMedium` |
| Calendar | `CalendarBlank` |
| Sold count | `UsersThree` |
| Remaining | `WarningCircle` |
| Heart | `Heart` |
| Arrow | `ArrowRight` |
| Urgency | `Fire` (fill) |

## 7. Code reference

```tsx
'use client';
import { useState, useEffect } from 'react';
import * as Phosphor from '@phosphor-icons/react';

export interface Deal {
  id: string;
  type: 'flight' | 'hotel' | 'tour' | 'combo';
  brand: string;
  title: string;
  subtitle: string;
  imageId: string;
  rating: number;
  reviewCount: number;
  meta: string;
  endAt: Date;
  price: number;
  originalPrice: number;
  discountPercent: number;
  soldCount: number;
  remainingCount: number;
}

export function DealCountdownCard({ deal }: { deal: Deal }) {
  return (
    <article className="group relative w-[320px] flex-shrink-0 bg-white rounded-xl border border-slate-200 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300 overflow-hidden">
      <a href={`/deals/${deal.id}`} className="block relative aspect-[16/10] overflow-hidden bg-slate-100">
        <img
          src={`https://images.unsplash.com/photo-${deal.imageId}?w=600&h=375&fit=crop&q=80`}
          alt={`${deal.title} - ${deal.subtitle}`}
          className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-[1.04]"
          loading="lazy"
        />
        {/* Discount badge */}
        <div className="absolute top-3 left-3">
          <span className="inline-flex items-center gap-1 px-2.5 py-1 bg-rose-500 text-white text-[11px] font-bold uppercase tracking-wider rounded-md shadow-md">
            <Phosphor.Fire size={11} weight="fill" />
            -{deal.discountPercent}% OFF
          </span>
        </div>
        {/* Heart */}
        <button
          aria-label={`Lưu deal ${deal.title}`}
          className="absolute top-3 right-3 w-9 h-9 bg-white/95 backdrop-blur rounded-full flex items-center justify-center shadow-md hover:bg-white"
        >
          <Phosphor.Heart size={16} weight="regular" className="text-slate-700" />
        </button>
        {/* Type badge */}
        <div className="absolute bottom-3 left-3">
          <span className="inline-flex items-center gap-1 px-2 py-0.5 bg-white/95 backdrop-blur rounded text-[10px] font-bold uppercase tracking-wider text-slate-900">
            {deal.type === 'flight' && <Phosphor.AirplaneTilt size={10} weight="bold" />}
            {deal.type === 'hotel' && <Phosphor.Buildings size={10} weight="bold" />}
            {deal.type === 'tour' && <Phosphor.MapTrifold size={10} weight="bold" />}
            {deal.type === 'combo' && <Phosphor.Lightning size={10} weight="bold" />}
            {deal.type}
          </span>
        </div>
      </a>

      <div className="p-4 space-y-3">
        {/* Brand + Title */}
        <div>
          <p className="text-[11px] font-bold uppercase tracking-wider text-slate-500 mb-0.5">
            {deal.brand}
          </p>
          <h3 className="text-[15px] font-bold text-slate-900 leading-snug line-clamp-1">
            {deal.title}
          </h3>
          <p className="text-[12.5px] text-slate-600 mt-0.5 line-clamp-1">
            {deal.subtitle}
          </p>
        </div>

        {/* Meta */}
        <div className="flex items-center gap-2 text-[12px] text-slate-600">
          <span className="inline-flex items-center gap-1 text-amber-600 font-bold">
            <Phosphor.Star size={11} weight="fill" />
            {deal.rating}
          </span>
          <span>·</span>
          <span>{deal.reviewCount.toLocaleString()} đánh giá</span>
          <span>·</span>
          <span>{deal.meta}</span>
        </div>

        {/* Countdown */}
        <CountdownTimer endAt={deal.endAt} />

        {/* Price */}
        <div className="flex items-baseline gap-2">
          <span className="text-[24px] font-extrabold text-slate-900 tabular-nums leading-none">
            {deal.price.toLocaleString('vi-VN')}₫
          </span>
          <span className="text-[12px] text-slate-400 line-through tabular-nums">
            {deal.originalPrice.toLocaleString('vi-VN')}₫
          </span>
        </div>

        {/* Stock */}
        <div className="flex items-center gap-1.5 text-[11.5px]">
          <Phosphor.Fire size={12} weight="fill" className="text-rose-500" />
          <span className="text-rose-600 font-bold">
            Đã bán {deal.soldCount}
          </span>
          {deal.remainingCount <= 20 && (
            <span className="text-amber-600 font-semibold ml-1">
              · Còn {deal.remainingCount} suất
            </span>
          )}
        </div>

        {/* CTA */}
        <a
          href={`/deals/${deal.id}/book`}
          className="flex items-center justify-center gap-1.5 w-full py-2.5 bg-sky-600 hover:bg-sky-700 text-white text-[13px] font-bold rounded-lg transition-colors"
        >
          Đặt ngay {deal.price.toLocaleString('vi-VN')}₫
          <Phosphor.ArrowRight size={14} weight="bold" />
        </a>
      </div>
    </article>
  );
}

function CountdownTimer({ endAt }: { endAt: Date }) {
  const [timeLeft, setTimeLeft] = useState(() => calcTimeLeft(endAt));
  const [mounted, setMounted] = useState(false);
  const [expired, setExpired] = useState(false);

  useEffect(() => {
    setMounted(true);
    const tick = () => {
      const tl = calcTimeLeft(endAt);
      setTimeLeft(tl);
      if (tl.total <= 0) setExpired(true);
    };
    tick();
    const id = setInterval(tick, 1000);
    return () => clearInterval(id);
  }, [endAt]);

  // Static render trước khi mount (server / SSR)
  if (!mounted || expired) {
    return (
      <div className="bg-slate-900 text-white rounded-lg px-3 py-2 text-center">
        <span className="text-[11px] font-bold uppercase tracking-wider text-slate-300">
          {expired ? 'Đã hết hạn' : 'Còn'}
        </span>
        {!expired && (
          <div className="text-[18px] font-extrabold tabular-nums tracking-wider mt-0.5">
            02:14:33
          </div>
        )}
      </div>
    );
  }

  const { hours, minutes, seconds } = timeLeft;
  const isLowTime = timeLeft.total < 3600000; // < 1h

  return (
    <div className={`rounded-lg px-3 py-2 text-center ${isLowTime ? 'bg-rose-50 border border-rose-200' : 'bg-slate-900'}`}>
      <span className={`text-[10.5px] font-bold uppercase tracking-wider ${isLowTime ? 'text-rose-600' : 'text-slate-300'}`}>
        Còn
      </span>
      <div className={`flex items-center justify-center gap-1 mt-0.5 font-extrabold tabular-nums ${isLowTime ? 'text-rose-700' : 'text-white'}`} aria-live="off">
        <span className="text-[16px]">{String(hours).padStart(2, '0')}</span>
        <span className={isLowTime ? 'text-rose-300' : 'text-slate-500'}>:</span>
        <span className="text-[16px]">{String(minutes).padStart(2, '0')}</span>
        <span className={isLowTime ? 'text-rose-300' : 'text-slate-500'}>:</span>
        <span className="text-[16px]">{String(seconds).padStart(2, '0')}</span>
      </div>
      {/* sr-only text */}
      <span className="sr-only">
        Còn {hours} giờ {minutes} phút {seconds} giây
      </span>
    </div>
  );
}

function calcTimeLeft(endAt: Date) {
  const total = endAt.getTime() - Date.now();
  const hours = Math.max(0, Math.floor(total / 3600000));
  const minutes = Math.max(0, Math.floor((total % 3600000) / 60000));
  const seconds = Math.max(0, Math.floor((total % 60000) / 1000));
  return { total, hours, minutes, seconds };
}
```

## 8. Accessibility

- Countdown `aria-live="off"` (tránh spam screen reader mỗi giây). Có `.sr-only` text tóm tắt "Còn 2 giờ 14 phút 33 giây" update mỗi phút thay vì mỗi giây.
- Heart `aria-label` cụ thể
- CTA link accessible
- "Đã hết hạn" announced khi expired (`aria-live="polite"`)
- Reduce-motion: pulse animation off
- Color contrast: rose/sky đều pass AA

## 9. Performance

- Countdown dùng `useEffect` + `setInterval` 1s, clear khi unmount
- Image 600x375, `loading="lazy"`
- Initial render dùng placeholder static để tránh hydration mismatch (mounted flag)
- Re-render chỉ khi state thay đổi (giây)
- Interval cleanup function quan trọng

## 10. Anti-patterns đã tránh

- ❌ "Limited time" mà không có countdown thật
- ❌ Auto-redirect khi hết
- ❌ Modal chiếm toàn màn khi countdown < 1 phút
- ❌ Countdown nhảy lung tung giữa các tab (giờ server vs client)

---

**Component family**: Layout #2 — `deal-countdown-card`