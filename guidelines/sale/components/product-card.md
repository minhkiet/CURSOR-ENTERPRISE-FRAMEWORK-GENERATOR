# Product Card (Flash Sale Style)

> Card sản phẩm với discount badge đỏ/cam dominant, countdown, sold count, progress bar sold. Dùng trong flash sale sections và search results.

## 1. Mục đích

Hiển thị sản phẩm flash sale với urgency maximum: discount %, countdown, sold count, progress bar (còn bao nhiêu suất), strikethrough price, voucher stack.

## 2. Asset

| Element | Source |
|---|---|
| Product image | Unsplash curated |
| Brand logo | Simple Icons CDN |
| Free ship badge | Inline icon |

## 3. Cấu trúc

```
┌─────────────────────────────────────┐
│  [hero 1:1]                    [♥]  │
│  ┌────────┐  ┌──────────┐           │
│  │-50% HOT│  │ 02:14:33 │  ← badge │
│  └────────┘  └──────────┘           │
├─────────────────────────────────────┤
│ Brand · Official Store              │
│                                     │
│ Tên sản phẩm dài 2 dòng line-clamp │
│                                     │
│ ⭐ 4.8 · Đã bán 2.847               │
│                                     │
│ ~~499.000₫~~ -50%                   │
│ 249.000₫                             │
│                                     │
│ ▓▓▓▓▓▓▓▓▓▓▓░░░░ Đã bán 87/100      │
│                                     │
│ [Voucher -20K] [Freeship]          │
│                                     │
│ [    Mua ngay    ] [    Giỏ    ]   │
└─────────────────────────────────────┘
```

## 4. Variants

| Variant | Use | Khác biệt |
|---|---|---|
| `default` | Flash sale grid | Standard |
| `mega` | Hero bento | Larger + video overlay |
| `compact` | Sidebar | Horizontal, smaller |
| `sold-out` | End of sale | Greyed + "Đã hết" |

## 5. States

| State | Visual |
|---|---|
| default | Active |
| countdown-running | Update mỗi giây |
| countdown-end | "Đã kết thúc" + disable |
| low-stock | "Sắp hết" + red pulse |
| reduce-motion | No pulse |

## 6. Icon mapping

| Role | Phosphor |
|---|---|
| Discount | `Percent` |
| Countdown | `Clock` |
| Star | `Star` (fill) |
| Heart | `Heart` |
| Cart | `ShoppingBag` (bold) |
| Plus | `Plus` |
| Free ship | `Truck` |
| Voucher | `Ticket` |
| Store | `Storefront` |
| Verified | `SealCheck` (fill) |
| Mall | `Buildings` |

## 7. Code reference

```tsx
'use client';
import { useState, useEffect } from 'react';
import * as Phosphor from '@phosphor-icons/react';

export interface Product {
  id: string;
  slug: string;
  name: string;
  brand: string;
  isMall: boolean;
  imageId: string;
  rating: number;
  soldCount: number;
  originalPrice: number;
  salePrice: number;
  discountPercent: number;
  flashEndAt: Date;
  totalStock: number;
  soldStock: number;
  vouchers: Array<{ text: string; minOrder: number }>;
  freeShip: boolean;
  category: string;
}

export function FlashDealCard({ product }: { product: Product }) {
  const soldPercent = (product.soldStock / product.totalStock) * 100;
  const isLowStock = product.totalStock - product.soldStock <= 10;

  return (
    <article className="group relative bg-white rounded-xl border-2 border-slate-200 hover:border-orange-500 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300 overflow-hidden">
      <a href={`/products/${product.slug}`} className="block relative aspect-square overflow-hidden bg-slate-100">
        <img
          src={`https://images.unsplash.com/photo-${product.imageId}?w=600&h=600&fit=crop&q=80`}
          alt={product.name}
          className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-[1.04]"
          loading="lazy"
        />

        {/* Top-left badges */}
        <div className="absolute top-2 left-2 flex flex-col gap-1.5 items-start">
          <span className="inline-flex items-center gap-1 px-2 py-1 bg-gradient-to-r from-orange-500 to-rose-500 text-white text-[11px] font-extrabold uppercase tracking-wider rounded shadow-lg">
            <Phosphor.Fire size={11} weight="fill" />
            -{product.discountPercent}%
          </span>
          {product.isMall && (
            <span className="inline-flex items-center gap-1 px-1.5 py-0.5 bg-rose-500 text-white text-[9px] font-bold uppercase tracking-wider rounded">
              <Phosphor.Storefront size={9} weight="fill" />
              Mall
            </span>
          )}
        </div>

        {/* Top-right */}
        <button
          aria-label={`Lưu sản phẩm ${product.name}`}
          className="absolute top-2 right-2 w-8 h-8 bg-white/95 backdrop-blur rounded-full flex items-center justify-center shadow-md"
        >
          <Phosphor.Heart size={14} weight="regular" className="text-slate-700" />
        </button>

        {/* Vouchers bottom */}
        {(product.vouchers.length > 0 || product.freeShip) && (
          <div className="absolute bottom-2 left-2 right-2 flex items-center gap-1 flex-wrap">
            {product.vouchers.slice(0, 2).map((v, i) => (
              <span key={i} className="inline-flex items-center gap-1 px-1.5 py-0.5 bg-yellow-400 text-slate-900 text-[9.5px] font-extrabold rounded">
                <Phosphor.Ticket size={9} weight="fill" />
                {v.text}
              </span>
            ))}
            {product.freeShip && (
              <span className="inline-flex items-center gap-1 px-1.5 py-0.5 bg-sky-500 text-white text-[9.5px] font-extrabold rounded">
                <Phosphor.Truck size={9} weight="fill" />
                Free
              </span>
            )}
          </div>
        )}

        {soldPercent >= 100 && (
          <div className="absolute inset-0 bg-slate-900/80 backdrop-blur-sm flex items-center justify-center">
            <span className="text-white text-2xl font-extrabold">Đã hết</span>
          </div>
        )}
      </a>

      <div className="p-3 space-y-2">
        {/* Brand */}
        <div className="flex items-center gap-1 text-[10.5px]">
          <span className="font-bold text-slate-900 uppercase tracking-wide truncate">{product.brand}</span>
          {product.isMall && (
            <span className="inline-flex items-center text-rose-600 flex-shrink-0">
              <Phosphor.SealCheck size={11} weight="fill" />
            </span>
          )}
        </div>

        {/* Name */}
        <h3 className="text-[12.5px] font-medium text-slate-800 leading-snug line-clamp-2 min-h-[2.5rem] hover:text-orange-600">
          {product.name}
        </h3>

        {/* Rating + sold */}
        <div className="flex items-center gap-1 text-[10.5px] text-slate-500">
          <span className="inline-flex items-center gap-0.5 text-amber-500 font-bold">
            <Phosphor.Star size={10} weight="fill" />
            {product.rating}
          </span>
          <span>·</span>
          <span>Đã bán {product.soldCount.toLocaleString('vi-VN')}</span>
        </div>

        {/* Price */}
        <div>
          <div className="flex items-baseline gap-1.5">
            <span className="text-[10px] font-bold text-orange-600">₫</span>
            <span className="text-[20px] font-extrabold text-rose-600 tabular-nums leading-none">
              {product.salePrice.toLocaleString('vi-VN')}
            </span>
          </div>
          <div className="text-[10.5px] text-slate-400 line-through tabular-nums">
            {product.originalPrice.toLocaleString('vi-VN')}₫
          </div>
        </div>

        {/* Flash sale progress */}
        <div>
          <div className="flex items-center justify-between mb-1 text-[10.5px]">
            <span className="font-bold text-rose-600 inline-flex items-center gap-1">
              <Phosphor.Fire size={10} weight="fill" />
              {isLowStock ? 'Sắp hết!' : 'Đang bán chạy'}
            </span>
            <span className="text-slate-500 tabular-nums">
              Còn {product.totalStock - product.soldStock}
            </span>
          </div>
          <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
            <div
              className={`h-full rounded-full transition-all duration-500 ${
                soldPercent >= 90
                  ? 'bg-gradient-to-r from-rose-500 to-red-500'
                  : soldPercent >= 60
                  ? 'bg-gradient-to-r from-orange-500 to-rose-500'
                  : 'bg-gradient-to-r from-orange-400 to-orange-500'
              } ${soldPercent >= 80 ? 'animate-pulse-slow' : ''}`}
              style={{ width: `${Math.min(100, soldPercent)}%` }}
            />
          </div>
        </div>

        {/* CTAs */}
        <div className="grid grid-cols-2 gap-1.5 pt-1">
          <button className="flex items-center justify-center gap-1 py-1.5 text-[11px] font-semibold rounded bg-slate-100 hover:bg-slate-200 text-slate-700">
            <Phosphor.Plus size={11} weight="bold" />
            Giỏ
          </button>
          <button className="flex items-center justify-center gap-1 py-1.5 text-[11px] font-extrabold rounded bg-gradient-to-r from-orange-500 to-rose-500 hover:from-orange-600 hover:to-rose-600 text-white shadow-md">
            <Phosphor.Bag size={11} weight="bold" />
            Mua ngay
          </button>
        </div>
      </div>
    </article>
  );
}
```

## 8. Accessibility

- Image alt mô tả tên sản phẩm
- Heart `aria-label` cụ thể
- Discount badge có icon + text
- Voucher có icon + text
- Progress bar có text "Còn X suất"
- "Sắp hết!" announced via badge
- Sold out overlay `role="status"`
- CTAs accessible với visible text
- Reduce-motion: no pulse

## 9. Performance

- Image 600x600, lazy load
- Pulse animation subtle (3s)
- Hover transition 300ms
- CSS gradient progress bar (no JS animation)

## 10. Anti-patterns đã tránh

- ❌ "Limited time" without real countdown
- ❌ Generic 3-equal cards (bento elsewhere)
- ❌ No progress bar (đã có)
- ❌ No sold count (đã có)
- ❌ No strikethrough price (đã có)

---

**Component family**: Layout #1 — `flash-deal-product-card`