# Voucher Card + Coupon Code

> Card voucher có mã copy-able, value, min order, expiry. Dùng trong homepage section 4 (Voucher carousel) và cart page (Available coupons).

## 1. Mục đích

Voucher code rõ ràng, copy 1-click, điều kiện visible (min order, expiry), CTA "Dùng ngay". Khách không cần rời trang để lấy code.

## 2. Asset

| Element | Source |
|---|---|
| Brand logo | Simple Icons CDN |
| Voucher shape | SVG inline (perforated edges) |

## 3. Cấu trúc

```
┌──────────────────────────────────────────────────┐
│  ╭──────╮                                ╭──────╮ │
│  │ SHOP │  Giảm 50.000₫                  │ COPY │ │
│  ╰──────╯  đơn từ 150.000₫                ╰──────╯ │
│                                                  │
│  ┌────────────────┐                             │
│  │ SALE50K        │  HSD: 30/07/2026           │
│  └────────────────┘  Còn 1.247 lượt             │
└──────────────────────────────────────────────────┘
```

## 4. Variants

| Variant | Use | Khác biệt |
|---|---|---|
| `default` | Voucher grid | Standard horizontal |
| `platform` | Shopee/Lazada | Brand logo prominent |
| `shop` | Quán specific | Shop logo |
| `shipping` | Freeship | Truck icon |
| `expired` | Past | Greyed + disabled |

## 5. States

| State | Visual |
|---|---|
| default | Active voucher |
| copied | "Đã chép" feedback 2s |
| expired | Greyed + "Đã hết hạn" |
| applied | Green check + "Đã dùng" |
| reduce-motion | No transition |

## 6. Icon mapping

| Role | Phosphor |
|---|---|
| Copy | `Copy` |
| Copied | `CheckCircle` (fill) |
| Store | `Storefront` |
| Truck | `Truck` |
| Tag | `Tag` |
| Percent | `Percent` |
| Calendar | `CalendarBlank` |
| Clock | `Clock` |
| Users | `UsersThree` |

## 7. Code reference

```tsx
'use client';
import { useState } from 'react';
import * as Phosphor from '@phosphor-icons/react';

export interface Voucher {
  id: string;
  code: string;
  type: 'fixed' | 'percent' | 'shipping';
  value: number;
  minOrder: number;
  maxDiscount?: number;
  expiresAt: Date;
  remaining: number;
  brandSlug?: string;
  shopName?: string;
  shopLogo?: string;
}

export function VoucherCard({ voucher }: { voucher: Voucher }) {
  const [copied, setCopied] = useState(false);
  const [applied, setApplied] = useState(false);

  const copyCode = async () => {
    await navigator.clipboard.writeText(voucher.code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const applyVoucher = () => {
    setApplied(true);
  };

  const valueText = voucher.type === 'percent'
    ? `Giảm ${voucher.value}%`
    : voucher.type === 'fixed'
    ? `Giảm ${voucher.value.toLocaleString('vi-VN')}₫`
    : 'Freeship';

  return (
    <div className={`relative bg-white rounded-xl border-2 ${applied ? 'border-emerald-500' : 'border-dashed border-orange-300'} overflow-hidden transition-all`}>
      {/* Perforated edge */}
      <div className="absolute left-1/2 top-0 bottom-0 flex flex-col items-center justify-between py-2 pointer-events-none" aria-hidden="true">
        <div className="w-3 h-3 rounded-full bg-orange-50" />
        <div className="w-3 h-3 rounded-full bg-orange-50" />
      </div>

      <div className="grid grid-cols-[1fr_auto]">
        {/* Left: brand + value + conditions */}
        <div className="p-4">
          <div className="flex items-center gap-2 mb-2">
            {voucher.brandSlug ? (
              <img
                src={`https://cdn.simpleicons.org/${voucher.brandSlug}/ea580c`}
                alt={voucher.shopName || voucher.brandSlug}
                className="h-5 w-5"
                loading="lazy"
              />
            ) : (
              <div className="w-5 h-5 bg-orange-100 rounded flex items-center justify-center">
                <Phosphor.Storefront size={12} weight="fill" className="text-orange-600" />
              </div>
            )}
            <span className="text-[11px] font-bold text-slate-700 uppercase tracking-wide truncate">
              {voucher.shopName || 'Strikeout'}
            </span>
          </div>

          <p className="text-[20px] lg:text-[24px] font-extrabold text-slate-900 leading-none">
            {valueText}
            {voucher.maxDiscount && voucher.type === 'percent' && (
              <span className="text-[11px] font-medium text-slate-500 ml-1">
                tối đa {voucher.maxDiscount.toLocaleString('vi-VN')}₫
              </span>
            )}
          </p>

          <p className="mt-1 text-[12px] text-slate-500">
            Đơn từ {voucher.minOrder.toLocaleString('vi-VN')}₫
          </p>

          <div className="mt-2 flex items-center gap-3 text-[10.5px] text-slate-500">
            <span className="inline-flex items-center gap-1">
              <Phosphor.CalendarBlank size={10} weight="bold" />
              HSD: {new Date(voucher.expiresAt).toLocaleDateString('vi-VN')}
            </span>
            <span className="inline-flex items-center gap-1">
              <Phosphor.UsersThree size={10} weight="bold" />
              Còn {voucher.remaining.toLocaleString('vi-VN')}
            </span>
          </div>
        </div>

        {/* Right: code + CTA */}
        <div className="bg-orange-50 p-3 flex flex-col items-center justify-center gap-2 min-w-[140px] border-l border-dashed border-orange-200">
          <code className="px-2 py-1.5 bg-white border-2 border-dashed border-orange-400 rounded text-[12px] font-extrabold tracking-wider text-slate-900 tabular-nums">
            {voucher.code}
          </code>

          {applied ? (
            <span className="inline-flex items-center gap-1 px-3 py-1.5 bg-emerald-600 text-white text-[11px] font-bold rounded">
              <Phosphor.CheckCircle size={12} weight="fill" />
              Đã dùng
            </span>
          ) : (
            <>
              <button
                type="button"
                onClick={copyCode}
                className="w-full px-2 py-1.5 bg-white hover:bg-orange-100 border border-orange-300 text-orange-700 text-[11px] font-bold rounded inline-flex items-center justify-center gap-1"
              >
                {copied ? (
                  <>
                    <Phosphor.CheckCircle size={11} weight="fill" />
                    Đã chép
                  </>
                ) : (
                  <>
                    <Phosphor.Copy size={11} weight="bold" />
                    Sao chép
                  </>
                )}
              </button>
              <button
                type="button"
                onClick={applyVoucher}
                className="w-full px-2 py-1.5 bg-gradient-to-r from-orange-500 to-rose-500 hover:from-orange-600 hover:to-rose-600 text-white text-[11px] font-extrabold rounded"
              >
                Dùng ngay
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
```

## 8. Accessibility

- Voucher code là `<code>` semantic
- Copy button có icon + text
- "Đã chép" feedback visible
- Applied state có icon + text
- Perforated dots decorative `aria-hidden="true"`
- Brand logo có alt
- Date format Vietnamese

## 9. Performance

- Clipboard API cho copy
- Brand logo qua Simple Icons CDN
- Inline SVG perforated edge
- Hover transition subtle
- No auto-submit

## 10. Anti-patterns đã tránh

- ❌ Voucher code dùng image (đã text semantic)
- ❌ Auto-apply mã không cho user kiểm tra
- ❌ Hidden conditions (đã visible minOrder, expiry)
- ❌ No feedback khi copy
- ❌ Generic code display

---

**Component family**: Layout #3 — `voucher-card`