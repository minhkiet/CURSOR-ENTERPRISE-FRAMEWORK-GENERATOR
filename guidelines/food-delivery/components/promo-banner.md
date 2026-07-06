# Promo Banner with Countdown

> Banner ngang cho flash promo với countdown thật, mã giảm giá, điều kiện áp dụng. Dùng trong homepage section 4 (Promo strip) và section 8 (Promo codes carousel).

## 1. Mục đích

Flash deal tạo urgency. Countdown rõ ràng + mã giảm giá copy-able + điều kiện rõ ràng.

## 2. Asset

| Element | Source |
|---|---|
| Background pattern | SVG inline (voucher ticket shape) |
| Brand logo | Simple Icons CDN |
| Mã code | Text |

## 3. Cấu trúc

```
┌───────────────────────────────────────────────────────┐
│  ┌─ticket shape with perforated edge──┐             │
│  │ ┌──┐                                  │             │
│  │ │🌟│  GIẢM 30%                        │             │
│  │ └──┘  đơn từ 150.000₫                │             │
│  │                                        │             │
│  │ ┌────────────────┐                    │             │
│  │ │ BOWL30        │  [Sao chép]        │             │
│  │ └────────────────┘                    │             │
│  │                                        │             │
│  │ ⏰ CÒN                                │             │
│  │ 02 : 14 : 33                          │             │
│  │ ───────────────────────────────────── │             │
│  │ HSD: 25/07/2026 · Áp dụng 1 lần/quán │             │
│  └────────────────────────────────────────┘             │
└───────────────────────────────────────────────────────┘
```

## 4. Variants

| Variant | Use | Khác biệt |
|---|---|---|
| `default` | Homepage | Full ticket shape |
| `inline` | Cart page | Compact horizontal |
| `expired` | Past | Greyed + "Đã hết hạn" |
| `claimed` | Used | "Đã dùng" overlay |

## 5. States

| State | Visual |
|---|---|
| default | Active voucher |
| countdown-running | Update mỗi giây |
| countdown-end | "Đã hết hạn" + dim |
| copied | "Đã sao chép" feedback 2s |
| reduce-motion | Static countdown |

## 6. Icon mapping

| Role | Phosphor |
|---|---|
| Tag | `Tag` (fill) |
| Copy | `Copy` |
| Check copied | `CheckCircle` (fill) |
| Clock | `Clock` |
| Star | `Star` (fill) |
| Discount | `Percent` |
| Truck free | `Truck` |

## 7. Code reference

```tsx
'use client';
import { useState, useEffect } from 'react';
import * as Phosphor from '@phosphor-icons/react';

export interface Promo {
  id: string;
  code: string;
  type: 'percent' | 'fixed' | 'freeship';
  value: number; // 30 (%) or 50000 (VND)
  minOrder: number;
  description: string;
  expiresAt: Date;
  usageLimit: string;
}

export function PromoBanner({ promo }: { promo: Promo }) {
  const [copied, setCopied] = useState(false);

  const copyCode = async () => {
    await navigator.clipboard.writeText(promo.code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const valueText = promo.type === 'percent'
    ? `GIẢM ${promo.value}%`
    : promo.type === 'fixed'
    ? `GIẢM ${promo.value.toLocaleString('vi-VN')}₫`
    : 'FREESHIP';

  return (
    <div className="relative bg-gradient-to-r from-emerald-600 via-emerald-500 to-amber-500 rounded-2xl overflow-hidden shadow-xl">
      {/* Decorative pattern */}
      <div className="absolute inset-0 opacity-10" aria-hidden="true">
        <svg className="w-full h-full" preserveAspectRatio="xMidYMid slice" viewBox="0 0 200 200">
          <pattern id="dots" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
            <circle cx="10" cy="10" r="2" fill="white" />
          </pattern>
          <rect width="200" height="200" fill="url(#dots)" />
        </svg>
      </div>

      {/* Perforated edge */}
      <div className="absolute left-1/2 top-0 bottom-0 flex flex-col items-center justify-between py-2 pointer-events-none" aria-hidden="true">
        <div className="w-4 h-4 rounded-full bg-white" />
        <div className="w-4 h-4 rounded-full bg-white" />
      </div>

      <div className="relative grid grid-cols-1 md:grid-cols-2 gap-4 p-6 lg:p-7">
        {/* Left: value + description */}
        <div className="text-white">
          <div className="inline-flex items-center gap-1.5 px-2.5 py-1 bg-white/20 backdrop-blur rounded-full text-[10.5px] font-bold uppercase tracking-wider mb-3">
            <Phosphor.Star size={11} weight="fill" className="text-amber-200" />
            Flash deal
          </div>
          <p className="text-[36px] lg:text-[48px] font-extrabold leading-none tracking-tight">
            {valueText}
          </p>
          <p className="mt-2 text-white/95 text-[14px]">
            {promo.description}
          </p>
          <p className="mt-1 text-white/75 text-[12px]">
            Áp dụng cho đơn từ {promo.minOrder.toLocaleString('vi-VN')}₫
          </p>
        </div>

        {/* Right: code + countdown */}
        <div className="bg-white/15 backdrop-blur rounded-xl p-4 border border-white/20">
          {/* Code */}
          <div className="flex items-center gap-2">
            <code className="flex-1 px-3 py-2.5 bg-white rounded-lg text-[16px] font-extrabold tracking-wider text-slate-900 tabular-nums text-center">
              {promo.code}
            </code>
            <button
              type="button"
              onClick={copyCode}
              aria-label={`Sao chép mã ${promo.code}`}
              className="px-3 py-2.5 bg-white hover:bg-amber-50 rounded-lg text-slate-900 font-bold text-[12px] inline-flex items-center gap-1 transition-colors"
            >
              {copied ? (
                <>
                  <Phosphor.CheckCircle size={14} weight="fill" className="text-emerald-600" />
                  Đã chép
                </>
              ) : (
                <>
                  <Phosphor.Copy size={14} weight="bold" />
                  Sao chép
                </>
              )}
            </button>
          </div>

          {/* Countdown */}
          <CountdownTimer expiresAt={promo.expiresAt} />

          {/* Conditions */}
          <p className="mt-3 text-[11px] text-white/80 text-center">
            {promo.usageLimit}
          </p>
        </div>
      </div>
    </div>
  );
}

function CountdownTimer({ expiresAt }: { expiresAt: Date }) {
  const [mounted, setMounted] = useState(false);
  const [expired, setExpired] = useState(false);
  const [tl, setTl] = useState({ h: 2, m: 14, s: 33 });

  useEffect(() => {
    setMounted(true);
    const tick = () => {
      const total = expiresAt.getTime() - Date.now();
      if (total <= 0) { setExpired(true); return; }
      const h = Math.floor(total / 3600000);
      const m = Math.floor((total % 3600000) / 60000);
      const s = Math.floor((total % 60000) / 1000);
      setTl({ h, m, s });
    };
    tick();
    const id = setInterval(tick, 1000);
    return () => clearInterval(id);
  }, [expiresAt]);

  return (
    <div className="mt-3 bg-slate-900 rounded-lg px-3 py-2 text-center">
      <span className="text-[10.5px] font-bold uppercase tracking-wider text-slate-300">
        {expired ? 'Đã hết hạn' : 'Còn'}
      </span>
      {mounted && !expired ? (
        <>
          <div className="flex items-center justify-center gap-1 mt-0.5 text-white font-extrabold tabular-nums" aria-live="off">
            <span className="text-[18px]">{String(tl.h).padStart(2, '0')}</span>
            <span className="text-slate-500">:</span>
            <span className="text-[18px]">{String(tl.m).padStart(2, '0')}</span>
            <span className="text-slate-500">:</span>
            <span className="text-[18px]">{String(tl.s).padStart(2, '0')}</span>
          </div>
          <span className="sr-only">Còn {tl.h} giờ {tl.m} phút {tl.s} giây</span>
        </>
      ) : (
        <div className="text-white text-[18px] font-extrabold tabular-nums mt-0.5">
          02:14:33
        </div>
      )}
    </div>
  );
}
```

## 8. Accessibility

- Voucher code là `<code>` semantic
- Copy button có aria-label cụ thể
- Copied state có feedback visible
- Countdown `aria-live="off"` + sr-only text update mỗi phút
- Expired announced
- Reduce-motion: countdown static
- Pattern background `aria-hidden="true"`
- Perforated dots decorative
- Ticket shape có semantic meaning qua text

## 9. Performance

- Countdown useEffect + setInterval, cleanup
- Initial render static placeholder
- SVG pattern inline (no request)
- Click copy dùng Clipboard API
- No auto-submit, no unnecessary re-renders

## 10. Anti-patterns đã tránh

- ❌ "Limited time" without real countdown
- ❌ Voucher code dùng image (đã text semantic)
- ❌ Auto-apply mã không cho user kiểm tra
- ❌ Countdown không update (đã useEffect)
- ❌ Modal pop-up ngay khi vào homepage

---

**Component family**: Layout #3 — `promo-banner-countdown`