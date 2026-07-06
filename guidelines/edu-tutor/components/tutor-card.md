# Tutor Card

> Card cho một tutor trong marketplace grid. Photo thật phía trên, verified badge, subject, rating, hourly rate.

## 1. Mục đích

Hiển thị tutor trong filter-able grid. Phải đọc nhanh: ai dạy, dạy gì, giá bao nhiêu, có verified không.

## 2. Icon system

| Role | Icon Phosphor | Size |
|---|---|---|
| Verified | `SealCheck` (fill) | 14px, cobalt |
| Math | `MathOperations` | 14px |
| Physics | `Atom` | 14px |
| English | `BookOpen` | 14px |
| Chemistry | `Flask` | 14px |
| Music | `MusicNote` | 14px |
| Vietnamese | `BookmarkSimple` | 14px |
| Star rating | `Star` (fill) | 11px, amber |
| Hourly rate | `CurrencyCircleDollar` | 14px |
| Schedule | `CalendarBlank` | 14px |
| Trial lesson | `Gift` | 12px |
| Favorite | `Heart` | 16px |

## 3. Hình ảnh

| Section | Source |
|---|---|
| Tutor portrait | `https://picsum.photos/seed/tutor-vn-portrait-{id}/400/400` |
| Subject hero | `https://picsum.photos/seed/subject-{slug}/800/500` |
| Student avatars | `https://picsum.photos/seed/student-avatar-{n}/64/64` |

## 4. Cấu trúc

```
┌──────────────────────────────────┐
│  [tutor portrait]               │
│  ★ 4.9 (123)                    │
├──────────────────────────────────┤
│  Trần Văn Minh                  │ ← name (18px bold)
│  Math · Physics                 │ ← subjects (14px)
│                                  │
│  "5 năm kinh nghiệm luyện thi   │
│   THPT chuyên Toán."            │ ← bio (14px)
│                                  │
│  350.000₫/giờ    [Đặt buổi học]│
└──────────────────────────────────┘
```

## 5. Variants

| Variant | Padding | Use |
|---|---|---|
| `default` | 16 | Marketplace grid |
| `featured` | 24 | Top picks |
| `compact` | 12 | Sidebar widget |

## 6. States

| State | Visual |
|---|---|
| default | base |
| hover | `translateY(-2px)`, shadow lift |
| focus-within | outline 2px cobalt on card |
| loading | skeleton with shimmer |
| unavailable | overlay "Bận đến 15/7", CTA disabled |

## 7. Code reference

```tsx
<article class="group bg-white rounded-xl shadow-[0_1px_2px_rgba(15,23,42,0.04),0_4px_12px_rgba(15,23,42,0.06)] hover:shadow-[0_4px_8px_rgba(15,23,42,0.08),0_12px_24px_rgba(15,23,42,0.10)] hover:-translate-y-0.5 transition-all duration-280 overflow-hidden">
  <div class="relative aspect-square overflow-hidden bg-[#fef3c7]">
    <img
      src={`https://picsum.photos/seed/tutor-vn-portrait-${id}/400/400`}
      alt={`Portrait of ${name}`}
      class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-[1.03]"
      loading="lazy"
    />
    <div class="absolute top-3 left-3 inline-flex items-center gap-1 px-2 py-1 bg-[#1e3a8a] text-white rounded-full text-[10px] font-medium uppercase tracking-wider shadow-md">
      <Phosphor.SealCheck size={11} weight="fill" aria-hidden="true" />
      Verified
    </div>
    <button
      type="button"
      aria-label="Yêu thích gia sư"
      aria-pressed={isFavorited}
      class="absolute top-3 right-3 inline-flex items-center justify-center w-9 h-9 bg-white/90 backdrop-blur rounded-full hover:bg-white transition-colors"
    >
      <Phosphor.Heart size={16} weight={isFavorited ? 'fill' : 'regular'} class="text-[#b45309]" aria-hidden="true" />
    </button>
    <div class="absolute bottom-3 left-3 inline-flex items-center gap-1 px-2 py-1 bg-white/95 backdrop-blur rounded-full text-[11px] font-medium text-[#0f172a]">
      <Phosphor.Star size={11} weight="fill" class="text-[#f59e0b]" aria-hidden="true" />
      <span>{rating.toFixed(1)}</span>
      <span class="text-[#94a3b8]">({reviewCount})</span>
    </div>
  </div>

  <div class="p-4">
    <div class="flex items-start justify-between gap-2">
      <div class="min-w-0 flex-1">
        <h3 class="text-[18px] font-bold text-[#0f172a] truncate">{name}</h3>
        <div class="mt-1 flex items-center gap-2 text-[12px] text-[#475569]">
          <Phosphor.MathOperations size={13} weight="bold" class="text-[#1e3a8a]" aria-hidden="true" />
          <span>{subjects.join(' · ')}</span>
        </div>
      </div>
    </div>

    <p class="mt-3 text-[13px] text-[#475569] leading-relaxed line-clamp-2 min-h-[40px]">
      {bio}
    </p>

    <div class="mt-4 flex items-end justify-between gap-2">
      <div>
        <div class="text-[18px] font-bold text-[#1e3a8a] tabular-nums">
          {formatCurrency(hourlyRate)}<span class="text-[12px] font-medium text-[#475569]">/giờ</span>
        </div>
        <div class="inline-flex items-center gap-1 mt-1 font-mono text-[10px] uppercase tracking-wider text-[#f59e0b]">
          <Phosphor.Gift size={11} weight="bold" aria-hidden="true" />
          Buổi thử miễn phí
        </div>
      </div>
      <button
        type="button"
        class="inline-flex items-center gap-1.5 px-3.5 py-2 bg-[#1e3a8a] text-[#fdf8ec] text-[12.5px] font-medium rounded-md hover:bg-[#172554] hover:-translate-y-px transition-all duration-180"
      >
        <Phosphor.CalendarBlank size={13} weight="bold" aria-hidden="true" />
        Đặt buổi học
      </button>
    </div>
  </div>
</article>
```