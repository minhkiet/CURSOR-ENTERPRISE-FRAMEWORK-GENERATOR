# Treatment Card

> Card cho một treatment. Đọc như jar trưng bày trên kệ sand: ảnh thật phía trên, thông tin dưới, rose-gold viền nhấn.

## 1. Mục đích

Hiển thị một treatment trong grid. Card phải đọc nhanh trong 0.5s: thumbnail, tên, duration, giá.

## 2. Icon system

| Role | Icon Phosphor | Size |
|---|---|---|
| Facial | `Drop` | 14px trên eyebrow category |
| Massage | `Hand` | 14px |
| Body | `Flower` | 14px |
| Energy | `Lightning` | 14px |
| Couples | `Heart` | 14px |
| Duration | `Clock` | 12px |
| Price | `CurrencyCircleDollar` | 14px |
| Therapist | `UserCircle` | 14px |
| Rating | `Star` (fill) | 11px, gold |
| Verified | `SealCheck` (fill) | 11px, sage |
| Favorite | `Heart` | 16px |
| Book | `CalendarPlus` | 14px |

## 3. Hình ảnh

| Treatment | Image source |
|---|---|
| HydraFacial | `https://picsum.photos/seed/hydrafacial-jar/600/400` |
| Aromatherapy massage | `https://picsum.photos/seed/aromatherapy-massage/600/400` |
| Body scrub ritual | `https://picsum.photos/seed/body-scrub-ritual/600/400` |
| Couples retreat | `https://picsum.photos/seed/couples-retreat/600/400` |
| Energy healing | `https://picsum.photos/seed/energy-healing/600/400` |
| Pregnancy massage | `https://picsum.photos/seed/pregnancy-massage/600/400` |

Photo treatment: `filter: brightness(1.04) saturate(0.92)`.

## 4. Cấu trúc

```
┌────────────────────────────────────┐
│  [treatment photo 16/10]           │
│  ✦ Facial · 60 min                │ ← category + duration badge
├────────────────────────────────────┤
│  HydraFacial Premium               │ ← title (24px Cormorant)
│  Deep cleanse with hyaluronic acid │ ← description (15px DM Sans)
│                                    │
│  ★ 4.9 (124)  · Therapist: Lan    │
│                                    │
│  1.200.000₫         [Heart]       │ ← price + favorite
│                                    │
│  [ Đặt lịch ]                     │ ← CTA full-width
└────────────────────────────────────┘
```

## 5. Variants

| Variant | Padding | Background | Use |
|---|---|---|---|
| `default` | 20 | `#ffffff` | Standard grid |
| `compact` | 16 | `#ffffff` | Dense lists, related treatments |
| `featured` | 24 | `#f5f0e8` paper | Editor's pick, top of page |
| `member` | 20 | `#2c2620` walnut | Member-only treatments |

## 6. Sizes

Card sizes determined by grid column. Responsive grid:

- ≥1280px: 3 columns, gap 24
- 768–1279px: 2 columns, gap 24
- <768px: 1 column, gap 16

## 7. States

| State | Visual |
|---|---|
| default | base |
| hover | `translateY(-2px)`, shadow lifted, photo `scale(1.03)` |
| focus-within | outline 2px rose-gold on card |
| loading | skeleton with shimmer |
| sold-out | overlay "Hết lịch tuần này", CTA disabled |

## 8. Responsive

- Mobile: card 100% width, photo 16:10.
- Tablet: 2-col.
- Desktop: 3-col.

## 9. Edge cases

- Long title: 2-line truncate.
- Missing photo: placeholder with category icon (32×32) on sand bg.
- Out of stock: overlay "Hết lịch" với `Clock` icon, CTA disabled.

## 10. Code reference

```tsx
<article class="group bg-white rounded-2xl overflow-hidden shadow-[0_4px_16px_rgba(44,38,32,0.06)] hover:shadow-[0_12px_32px_rgba(44,38,32,0.10)] hover:-translate-y-0.5 transition-all duration-280">
  <div class="relative aspect-[16/10] overflow-hidden bg-[#ebe2d4]">
    <img
      src="https://picsum.photos/seed/hydrafacial-jar/600/400"
      alt="HydraFacial Premium treatment jar with rose petals"
      class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-[1.04]"
      style={{ filter: 'brightness(1.04) saturate(0.92)' }}
      loading="lazy"
    />
    <div class="absolute top-3 left-3 inline-flex items-center gap-1 px-2.5 py-1 bg-white/90 backdrop-blur rounded-full shadow-sm">
      <Phosphor.Drop size={11} weight="bold" class="text-[#a07749]" aria-hidden="true" />
      <span class="font-mono text-[10px] uppercase tracking-[0.18em] text-[#5a4f43]">Facial · 60 min</span>
    </div>
    <button
      type="button"
      aria-label="Yêu thích HydraFacial Premium"
      aria-pressed={isFavorited}
      class="absolute top-3 right-3 inline-flex items-center justify-center w-9 h-9 bg-white/90 backdrop-blur rounded-full hover:bg-white transition-colors"
    >
      <Phosphor.Heart size={16} weight={isFavorited ? 'fill' : 'regular'} class="text-[#a07749]" aria-hidden="true" />
    </button>
  </div>

  <div class="p-5">
    <div class="flex items-center gap-1 text-[#a07749]">
      {[1, 2, 3, 4, 5].map(i => <Phosphor.Star key={i} size={11} weight="fill" aria-hidden="true" />)}
      <span class="ml-1 font-mono text-[10.5px] text-[#5a4f43]">4.9 · 124 đánh giá</span>
      <span class="ml-auto inline-flex items-center gap-1 font-mono text-[10.5px] text-[#5a4f43]">
        <Phosphor.UserCircle size={11} weight="bold" aria-hidden="true" />
        Therapist Lan
      </span>
    </div>

    <h3 class="mt-3 font-display text-[24px] leading-tight text-[#2c2620]">HydraFacial Premium</h3>
    <p class="mt-1.5 text-[13.5px] text-[#5a4f43] leading-relaxed line-clamp-2">
      Làm sạch sâu với hyaluronic acid và chiết xuất hoa hồng Bulgaria.
    </p>

    <div class="mt-4 flex items-baseline justify-between">
      <div class="flex items-baseline gap-1">
        <span class="font-display text-[26px] tabular-nums text-[#2c2620]">1.200.000</span>
        <span class="font-medium text-[14px] text-[#2c2620]">₫</span>
      </div>
      <span class="font-mono text-[10.5px] uppercase tracking-[0.18em] text-[#8a7e6e]">/ 60 phút</span>
    </div>

    <button
      type="button"
      class="mt-5 w-full inline-flex items-center justify-center gap-2 px-5 py-3 bg-[#a07749] text-[#f8f4ec] font-medium uppercase text-[12.5px] tracking-[0.12em] rounded-full hover:bg-[#8a6239] hover:-translate-y-px transition-all duration-180"
    >
      <Phosphor.CalendarPlus size={14} weight="bold" aria-hidden="true" />
      <span>Đặt lịch</span>
    </button>
  </div>
</article>
```