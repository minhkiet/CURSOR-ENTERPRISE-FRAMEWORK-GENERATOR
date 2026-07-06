# Listing Card (Market Pro)

> Card listing BĐS dùng cho search results, featured blocks, market insights. Ảnh thật (Unsplash), video overlay optional, trust badges, price + area + specs + agent + CTA nhanh.

## 1. Mục đích

Hiển thị một listing BĐS với đầy đủ thông tin khách hàng cần để quyết định click. Phải đọc trong 1.5s: ảnh, giá, diện tích, phòng, địa chỉ, pháp lý, agent, CTA.

## 2. Asset

| Element | Source pattern | Notes |
|---|---|---|
| Hero image | `https://images.unsplash.com/photo-{unsplashId}?w=800&h=500&fit=crop&q=80` | 8:5, `curated-realestate-exterior-{1..8}` |
| Gallery strip (4 thumbs) | Cùng Unsplash pattern | Optional, cho `featured` variant |
| Video overlay | MP4 local hoặc Coverr CDN | Có nút Play tròn overlay |
| 360 tour thumbnail | Image tĩnh + Cube icon overlay | Optional |
| Agent portrait | Unsplash curated portrait | 1:1, 80x80 |
| Brand logo (nếu listing từ agency) | `https://cdn.simpleicons.org/{slug}` | Optional |
| QR vcard agent | Generated SVG component | Optional |

## 3. Cấu trúc

```
┌─────────────────────────────────────────────────┐
│  [hero 8:5]              ▶ 360 ♥              │
│  ┌──────┐  ┌─────────┐                          │
│  │ -12% │  │ CÓ VIDEO│                          │
│  └──────┘  └─────────┘                          │
│ ┌──┬──┬──┬──┐                                  │
│ │1 │2 │3 │4 │  thumbnail gallery (4 ảnh)       │
│ └──┴──┴──┴──┘                                  │
├─────────────────────────────────────────────────┤
│  Penthouse · 8.5 tỷ  ·  56.2 triệu/m²         │ ← price + per-m²
│  ✦ Đã xác minh pháp lý                          │ ← verified row
│                                                  │
│  Vinhomes Golden River, Quận 1, TP.HCM         │ ← address
│                                                  │
│  ┌─────────────────────────────────────┐       │
│  │ 🛏 4PN · 🛁 3WC · 📐 156m² · T6     │       │ ← specs row
│  │ ✦ Hướng ĐN · 🅿️ 2 chỗ · 🏊 Hồ bơi │       │
│  └─────────────────────────────────────┘       │
│                                                  │
│  ░░░░░░░░░░ 78% quan tâm · 156 lượt xem hôm nay│
│                                                  │
│  ┌────┐                                          │
│  │ 👤 │ Trần Văn Minh · 4.9★ · 124 tin          │ ← agent
│  └────┘  ↳ Môi giới Anchor Pro Verified         │
│                                                  │
│  [📞 Gọi]  [💬 Chat]  [📅 Đặt lịch xem]          │ ← 3 CTAs
└─────────────────────────────────────────────────┘
```

## 4. Variants

| Variant | Use | Khác biệt |
|---|---|---|
| `default` | Grid search results | Standard 8:5 image, 3 CTAs |
| `featured` | Homepage mega block | Larger image 16:10, gallery strip 4 ảnh, "HOT" badge |
| `compact` | Map drawer list, sidebar | 1:1 image left, info right, 1 CTA chính |
| `video` | Listing có video walkthrough | Play icon overlay lớn, video plays on hover |
| `360` | Listing có virtual tour | Cube icon overlay, "Xem 360°" CTA |

## 5. States

| State | Visual change |
|---|---|
| default | Base |
| hover | `translateY(-4px)`, `shadow.lg`, image scale 1.04 |
| focus-within | `outline: 2px solid var(--color-focus-ring)`, offset 2px |
| loading | Skeleton: gray rectangle image, gray lines for text |
| sold | Opacity 0.6, "Đã bán" overlay navy 80%, "Tương tự" CTA |
| reserved | "Đã đặt cọc" badge cam, image normal |
| new (24h) | "MỚI" badge brand teal pulsing |
| price-drop | "-12%" badge cam + tooltip lịch sử giá |
| urgent | Cam border 2px, "Sắp hết hạn đăng tin" countdown |

## 6. Icon mapping

| Role | Phosphor | Size |
|---|---|---|
| Bedroom | `Bed` | 14px |
| Bathroom | `Bathtub` | 14px |
| Area | `Ruler` | 14px |
| Floor | `StackSimple` | 14px |
| Direction | `NavigationArrow` | 14px |
| Parking | `Car` | 14px |
| Pool | `SwimmingPool` | 14px |
| Garden | `Tree` | 14px |
| Elevator | `ArrowsOutCardinal` | 14px |
| Furnished | `Armchair` | 14px |
| Pet | `PawPrint` | 14px |
| Pin | `MapPin` (fill) | 14px |
| Heart | `Heart` | 18px |
| Phone | `Phone` | 16px |
| Chat | `ChatCircleDots` | 16px |
| Calendar | `CalendarPlus` | 16px |
| Verified | `SealCheck` (fill) | 12px |
| Play video | `PlayCircle` (fill) | 56px white shadow (featured) / 24px (compact) |
| 360 cube | `Cube` | 18px |
| Trend up | `TrendUp` | 12px |
| External | `ArrowSquareOut` | 12px |

## 7. Code reference (default variant)

```tsx
<article className="group relative bg-white rounded-xl border border-slate-200 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300 overflow-hidden">
  {/* Image container */}
  <a href={`/listings/${slug}`} className="block relative aspect-[8/5] overflow-hidden bg-slate-100">
    <img
      src={`https://images.unsplash.com/photo-${unsplashId}?w=800&h=500&fit=crop&q=80`}
      alt={`Bất động sản ${title} tại ${address}`}
      className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-[1.04]"
      style={{ filter: 'brightness(1.02) saturate(1.05) contrast(1.02)' }}
      loading="lazy"
      decoding="async"
    />

    {/* Top-left badges */}
    <div className="absolute top-3 left-3 flex items-center gap-1.5">
      {isNew && (
        <span className="inline-flex items-center gap-1 px-2.5 py-1 bg-teal-600 text-white text-[10.5px] font-bold uppercase tracking-wider rounded-full shadow-md animate-pulse">
          <Phosphor.Sparkle size={11} weight="fill" />
          Mới
        </span>
      )}
      {hasPriceDrop && (
        <span className="inline-flex items-center gap-1 px-2.5 py-1 bg-orange-500 text-white text-[10.5px] font-bold tabular-nums rounded-full shadow-md">
          <Phosphor.TrendDown size={11} weight="bold" />
          {priceDropPercent}%
        </span>
      )}
      {hasVideo && (
        <span className="inline-flex items-center gap-1 px-2.5 py-1 bg-black/70 backdrop-blur text-white text-[10.5px] font-semibold rounded-full">
          <Phosphor.PlayCircle size={12} weight="fill" />
          Video
        </span>
      )}
    </div>

    {/* Top-right actions */}
    <div className="absolute top-3 right-3 flex items-center gap-1.5">
      {has360Tour && (
        <button
          type="button"
          aria-label="Xem 360°"
          className="w-9 h-9 inline-flex items-center justify-center bg-white/95 backdrop-blur rounded-full hover:bg-white shadow-md"
          onClick={e => e.preventDefault()}
        >
          <Phosphor.Cube size={16} weight="bold" className="text-slate-700" />
        </button>
      )}
      <button
        type="button"
        aria-label={`Lưu tin ${title}`}
        aria-pressed={isFavorited}
        className="w-9 h-9 inline-flex items-center justify-center bg-white/95 backdrop-blur rounded-full hover:bg-white shadow-md"
        onClick={e => e.preventDefault()}
      >
        <Phosphor.Heart size={16} weight={isFavorited ? 'fill' : 'regular'} className={isFavorited ? 'text-red-500' : 'text-slate-700'} />
      </button>
    </div>

    {/* Gallery strip */}
    {showGallery && (
      <div className="absolute bottom-3 left-3 right-3 flex items-center gap-1.5">
        {gallery.map((thumb, i) => (
          <div key={i} className="w-12 h-9 rounded overflow-hidden border-2 border-white shadow-sm bg-slate-200">
            <img src={`https://images.unsplash.com/photo-${thumb}?w=80&h=60&fit=crop&q=80`} alt="" className="w-full h-full object-cover" />
          </div>
        ))}
        {remainingCount > 0 && (
          <div className="w-12 h-9 rounded bg-black/70 backdrop-blur border-2 border-white flex items-center justify-center text-white text-[10px] font-bold tabular-nums">
            +{remainingCount}
          </div>
        )}
      </div>
    )}

    {/* Sold overlay */}
    {isSold && (
      <div className="absolute inset-0 bg-navy-900/80 backdrop-blur-sm flex items-center justify-center">
        <div className="text-center">
          <span className="block text-white text-3xl font-extrabold tracking-tight">Đã bán</span>
          <span className="block text-white/70 text-xs mt-1">Xem tin tương tự →</span>
        </div>
      </div>
    )}
  </a>

  {/* Body */}
  <div className="p-5 space-y-3">
    {/* Price row */}
    <div className="flex items-baseline justify-between gap-2">
      <div className="flex items-baseline gap-2 flex-wrap">
        <span className="font-extrabold text-[28px] text-slate-900 tabular-nums leading-none">
          {formatPrice(price)}
        </span>
        <span className="text-[12px] text-slate-500 tabular-nums">· {formatPricePerM2(price, area)}</span>
      </div>
      <span className="text-[11px] font-semibold text-teal-600 uppercase tracking-wider">Penthouse</span>
    </div>

    {/* Verified row */}
    {isVerified && (
      <div className="flex items-center gap-1.5 text-[12px] text-sky-700">
        <Phosphor.SealCheck size={14} weight="fill" />
        <span className="font-semibold">Đã xác minh pháp lý · Sổ đỏ chính chủ</span>
      </div>
    )}

    {/* Address */}
    <a href={`/listings/${slug}`} className="block">
      <h3 className="text-[15px] font-semibold text-slate-800 leading-snug hover:text-teal-600 transition-colors">
        {title}, {address}
      </h3>
    </a>

    {/* Specs grid */}
    <div className="flex items-center gap-x-4 gap-y-1.5 flex-wrap text-[13px] text-slate-700">
      <span className="inline-flex items-center gap-1.5">
        <Phosphor.Bed size={14} weight="regular" className="text-slate-400" />
        <span className="font-semibold tabular-nums">{bedrooms}</span>
        <span className="text-slate-500">PN</span>
      </span>
      <span className="inline-flex items-center gap-1.5">
        <Phosphor.Bathtub size={14} weight="regular" className="text-slate-400" />
        <span className="font-semibold tabular-nums">{bathrooms}</span>
        <span className="text-slate-500">WC</span>
      </span>
      <span className="inline-flex items-center gap-1.5">
        <Phosphor.Ruler size={14} weight="regular" className="text-slate-400" />
        <span className="font-semibold tabular-nums">{area}</span>
        <span className="text-slate-500">m²</span>
      </span>
      <span className="inline-flex items-center gap-1.5">
        <Phosphor.StackSimple size={14} weight="regular" className="text-slate-400" />
        <span className="font-semibold">T{floor}</span>
      </span>
    </div>

    <div className="flex items-center gap-x-4 gap-y-1.5 flex-wrap text-[12px] text-slate-600">
      <span className="inline-flex items-center gap-1">
        <Phosphor.NavigationArrow size={12} weight="bold" className="text-slate-400" />
        Hướng {direction}
      </span>
      {hasParking && (
        <span className="inline-flex items-center gap-1">
          <Phosphor.Car size={12} weight="regular" className="text-slate-400" />
          {parkingSlots} chỗ đậu
        </span>
      )}
      {hasPool && (
        <span className="inline-flex items-center gap-1">
          <Phosphor.SwimmingPool size={12} weight="regular" className="text-slate-400" />
          Hồ bơi
        </span>
      )}
      {hasElevator && (
        <span className="inline-flex items-center gap-1">
          <Phosphor.ArrowsOutCardinal size={12} weight="regular" className="text-slate-400" />
          Thang máy
        </span>
      )}
      {isFurnished && (
        <span className="inline-flex items-center gap-1">
          <Phosphor.Armchair size={12} weight="regular" className="text-slate-400" />
          Nội thất đầy đủ
        </span>
      )}
    </div>

    {/* Engagement */}
    <div className="flex items-center gap-2 pt-2 border-t border-slate-100">
      <div className="flex-1 h-1 bg-slate-100 rounded-full overflow-hidden">
        <div className="h-full bg-teal-500 rounded-full" style={{ width: `${interestPercent}%` }} />
      </div>
      <span className="text-[11px] text-slate-500 tabular-nums font-medium">
        {interestPercent}% quan tâm · {viewsToday} xem hôm nay
      </span>
    </div>

    {/* Agent */}
    <div className="flex items-center gap-3 pt-1">
      <img
        src={`https://images.unsplash.com/photo-${agent.unsplashId}?w=80&h=80&fit=crop&q=80`}
        alt={agent.name}
        className="w-9 h-9 rounded-full object-cover ring-1 ring-slate-200"
      />
      <div className="min-w-0 flex-1">
        <p className="text-[13px] font-semibold text-slate-900 truncate">{agent.name}</p>
        <p className="text-[11px] text-slate-500 flex items-center gap-1">
          <Phosphor.Star size={10} weight="fill" className="text-amber-500" />
          {agent.rating} · {agent.totalListings} tin · Verified
        </p>
      </div>
    </div>

    {/* CTAs */}
    <div className="grid grid-cols-3 gap-2 pt-3 border-t border-slate-100">
      <a href={`tel:${agent.phone}`} className="flex items-center justify-center gap-1 py-2 px-2 text-[12px] font-semibold text-slate-700 bg-slate-50 hover:bg-slate-100 rounded-lg transition-colors">
        <Phosphor.Phone size={14} weight="bold" />
        Gọi
      </a>
      <a href={`/chat/${agent.id}`} className="flex items-center justify-center gap-1 py-2 px-2 text-[12px] font-semibold text-slate-700 bg-slate-50 hover:bg-slate-100 rounded-lg transition-colors">
        <Phosphor.ChatCircleDots size={14} weight="bold" />
        Chat
      </a>
      <a href={`/listings/${slug}/schedule`} className="flex items-center justify-center gap-1 py-2 px-2 text-[12px] font-semibold text-white bg-teal-600 hover:bg-teal-700 rounded-lg transition-colors">
        <Phosphor.CalendarPlus size={14} weight="bold" />
        Đặt lịch
      </a>
    </div>
  </div>
</article>
```

## 8. Edge cases

- **Ảnh lỗi**: fallback `data:image/svg+xml` placeholder với MapPin icon
- **Giá ẩn**: hiển thị "Liên hệ" thay vì giá, CTA chính đổi thành "Gọi để biết giá"
- **Diện tích = 0** (tin chỉ có thông tin chung): ẩn specs PN/WC/m², chỉ hiển thị địa chỉ
- **Listing nước ngoài** (multi-region): thêm country flag icon
- **Long title**: line-clamp 2, height cố định 40px
- **Real-time update** (giá thay đổi): subtle flash animation 200ms trên price
- **New in 24h**: thêm timestamp "Đăng 2 giờ trước" thay vì chỉ "Mới"

## 9. Accessibility

- Mỗi CTA là `<a>` hoặc `<button>` đúng semantic
- Heart favorite có `aria-pressed`
- Image có `alt` mô tả địa điểm cụ thể (không generic)
- Focus visible ring teal brand 2px
- Specs dùng `<dl>` semantic hoặc text thường với icon aria-hidden
- Sold overlay dùng `<div role="status">` cho screen reader
- Touch target ≥ 44x44px cho mọi action

## 10. Performance

- Ảnh 800x500 với `srcset` 400/600/800 cho responsive
- `loading="lazy"` cho tất cả ảnh dưới fold
- `decoding="async"` 
- Image format: Unsplash tự trả WebP với `auto=format&q=80`
- Above-the-fold listing (3-4 đầu) load eagerly với `fetchpriority="high"`
- Gallery thumbnails: 80x60, lazy load