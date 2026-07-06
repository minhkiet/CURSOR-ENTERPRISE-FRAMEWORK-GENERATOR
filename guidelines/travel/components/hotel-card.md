# Hotel Card

> Card khách sạn trong search results và homepage collections. Photo thật, rating, deals, amenities icon, distance, price, badge verified, instant confirm.

## 1. Mục đích

Hiển thị 1 khách sạn với đầy đủ thông tin khách cần: ảnh thật (gallery), tên, rating, số review, vị trí (khoảng cách từ landmark), deals badge, amenities, giá, CTA. Phải đọc trong 1.5s.

## 2. Asset

| Element | Source |
|---|---|
| Hero image | Unsplash curated hotel |
| Gallery strip (3 ảnh) | Cùng Unsplash collection |
| Video overlay (optional) | Coverr hotel tour |
| Traveler avatar | Unsplash curated portrait |
| Airline/brand logo | Simple Icons |

## 3. Cấu trúc

```
┌─────────────────────────────────────────────────┐
│  [hero 16:9]              ▶ ❤                  │
│  ┌──────┐  ┌──────┐  ┌──────┐                  │
│  │-30%  │  │VIDEO │  │FREE  │  ← 3 badges     │
│  │DEAL  │  │      │  │CANCEL│                  │
│  └──────┘  └──────┘  └──────┘                  │
│ ┌──┬──┬──┐                                      │
│ │1 │2 │3 │  gallery 3 ảnh + "+24"             │
│ └──┴──┴──┘                                      │
├─────────────────────────────────────────────────┤
│ Vinpearl Resort Phú Quốc                        │
│ ★ 4.8 (2.847 đánh giá) · Xuất sắc             │ ← rating
│ ✦ Verified · Thanh toán an toàn                │
│                                                  │
│ 📍 Bãi Dài, Phú Quốc · 2.3km từ sân bay        │
│                                                  │
│ 🏊 Hồ bơi · 🍴 Nhà hàng · 🛁 Spa · 🏋️ Gym    │ ← amenities
│ 🅿️ Đỗ xe miễn phí · 🐕 Thú cưng OK · 📶 WiFi  │
│                                                  │
│ ┌──────────────────────────┬──────────────────┐│
│ │ Phòng Deluxe Garden View │  3.250.000₫/đêm ││
│ │ 1 giường king · 45m²     │  ~~4.640.000₫~~  ││
│ │ Bao gồm bữa sáng · Hủy  │  -30% DEAL       ││
│ │ miễn phí trước 48h       │                  ││
│ │                          │  [Đặt ngay →]    ││
│ └──────────────────────────┴──────────────────┘│
└─────────────────────────────────────────────────┘
```

## 4. Variants

| Variant | Use | Khác biệt |
|---|---|---|
| `default` | Search results | Standard card |
| `featured` | Homepage bento | Larger, video overlay |
| `compact` | Sidebar list | Horizontal, 1 ảnh left, info right |
| `mystery` | Deal hot | "Khách sạn bí ẩn - tiết kiệm 50%" |
| `luxury` | Premium collection | Larger image, concierge badge |

## 5. States

| State | Visual |
|---|---|
| default | Base |
| hover | `translateY(-3px)`, shadow lg |
| focus-within | Ring navy 2px |
| sold-out | "Hết phòng" overlay |
| loading | Skeleton |
| instant-book | Coral badge "Xác nhận tức thì" |

## 6. Icon mapping

| Role | Phosphor | Size |
|---|---|---|
| Star rating | `Star` (fill) | 14px amber |
| Excellent | `StarFour` (fill) | 12px |
| Pin | `MapPin` (fill) | 12px |
| Verified | `SealCheck` (fill) | 14px sky |
| Pool | `SwimmingPool` | 14px |
| Restaurant | `ForkKnife` | 14px |
| Spa | `Flower` | 14px |
| Gym | `Barbell` | 14px |
| Parking | `Car` | 14px |
| Pet | `PawPrint` | 14px |
| WiFi | `WifiHigh` | 14px |
| Beach | `Umbrella` | 14px |
| Breakfast | `Coffee` | 14px |
| Heart | `Heart` | 18px |
| Play video | `PlayCircle` (fill) | 32px white shadow |
| Calendar | `CalendarBlank` | 14px |
| Users | `Users` | 14px |
| Distance | `AirplaneTakeoff` | 12px |

## 7. Code reference (default variant)

```tsx
<article className="group relative bg-white rounded-xl border border-slate-200 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300 overflow-hidden">
  {/* Image gallery */}
  <a href={`/hotels/${slug}`} className="block relative aspect-[16/9] overflow-hidden bg-slate-100">
    <img
      src={`https://images.unsplash.com/photo-${imageId}?w=800&h=450&fit=crop&q=80`}
      alt={`${name} tại ${location}`}
      className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-[1.04]"
      loading="lazy"
    />

    {/* Top-left badges */}
    <div className="absolute top-3 left-3 flex items-center gap-1.5">
      {discount && (
        <span className="inline-flex items-center gap-1 px-2.5 py-1 bg-rose-500 text-white text-[10.5px] font-bold rounded-full shadow-md">
          <Phosphor.Fire size={11} weight="fill" />
          -{discount}% DEAL
        </span>
      )}
      {hasVideo && (
        <span className="inline-flex items-center gap-1 px-2.5 py-1 bg-black/70 backdrop-blur text-white text-[10.5px] font-semibold rounded-full">
          <Phosphor.PlayCircle size={12} weight="fill" />
          Video
        </span>
      )}
      {freeCancel && (
        <span className="inline-flex items-center gap-1 px-2.5 py-1 bg-emerald-600 text-white text-[10.5px] font-semibold rounded-full">
          <Phosphor.CalendarCheck size={11} weight="bold" />
          Hủy miễn phí
        </span>
      )}
    </div>

    {/* Top-right */}
    <button aria-label="Lưu" className="absolute top-3 right-3 w-9 h-9 bg-white/95 backdrop-blur rounded-full flex items-center justify-center shadow-md">
      <Phosphor.Heart size={16} weight="regular" className="text-slate-700" />
    </button>

    {/* Gallery strip */}
    <div className="absolute bottom-3 left-3 right-3 flex items-center gap-1.5">
      {gallery.map((g, i) => (
        <div key={i} className="flex-1 aspect-[4/3] rounded overflow-hidden border-2 border-white shadow-sm bg-slate-200">
          <img src={`https://images.unsplash.com/photo-${g}?w=120&h=90&fit=crop&q=80`} alt="" className="w-full h-full object-cover" />
        </div>
      ))}
      <div className="flex-1 aspect-[4/3] rounded bg-black/70 backdrop-blur border-2 border-white flex items-center justify-center text-white text-[11px] font-bold">
        +{remainingCount} ảnh
      </div>
    </div>

    {soldOut && (
      <div className="absolute inset-0 bg-slate-900/85 backdrop-blur-sm flex items-center justify-center">
        <span className="text-white text-2xl font-extrabold">Hết phòng</span>
      </div>
    )}
  </a>

  {/* Body */}
  <div className="p-5 space-y-3">
    {/* Name + rating */}
    <div>
      <h3 className="text-[18px] font-bold text-slate-900 leading-snug hover:text-sky-700">
        {name}
      </h3>
      <div className="mt-1.5 flex items-center gap-2 text-[12px]">
        <span className="inline-flex items-center gap-0.5 px-1.5 py-0.5 bg-sky-700 text-white rounded font-bold tabular-nums">
          {rating}
        </span>
        <span className="text-slate-700 font-semibold">{label}</span>
        <span className="text-slate-500">· {formatCount(reviews)} đánh giá</span>
      </div>
    </div>

    {/* Verified row */}
    <div className="flex items-center gap-1.5 text-[12px] text-sky-700">
      <Phosphor.SealCheck size={14} weight="fill" />
      <span className="font-semibold">Verified · Thanh toán an toàn · Xác nhận tức thì</span>
    </div>

    {/* Location */}
    <p className="flex items-start gap-1.5 text-[13px] text-slate-600">
      <Phosphor.MapPin size={14} weight="fill" className="text-slate-400 mt-0.5 flex-shrink-0" />
      <span>{location} · <strong className="text-slate-900">{distance} km</strong> từ {landmark}</span>
    </p>

    {/* Amenities */}
    <div className="flex items-center gap-x-3 gap-y-1.5 flex-wrap text-[12px] text-slate-600">
      {amenities.map(a => (
        <span key={a.name} className="inline-flex items-center gap-1">
          <Phosphor[a.icon] size={13} weight="regular" className="text-slate-400" />
          {a.label}
        </span>
      ))}
    </div>

    {/* Room + price */}
    <div className="grid grid-cols-1 md:grid-cols-[1fr_auto] gap-3 pt-3 border-t border-slate-100">
      <div>
        <p className="text-[14px] font-bold text-slate-900">{room.name}</p>
        <p className="text-[12px] text-slate-500 mt-0.5">
          {room.bed} · {room.area}m² · {room.breakfast}
        </p>
        <p className="text-[11px] text-emerald-600 mt-1 font-semibold">{room.cancelPolicy}</p>
      </div>
      <div className="text-right">
        <div className="text-[10px] text-rose-500 font-bold uppercase">Chỉ còn 2 phòng</div>
        <div className="text-[24px] font-extrabold text-slate-900 tabular-nums leading-none">
          {formatPrice(price)}
        </div>
        <div className="text-[11px] text-slate-400 line-through tabular-nums">{formatPrice(originalPrice)}</div>
        <div className="text-[10px] text-slate-500 mt-1">/đêm, đã gồm thuế</div>
        <a href={`/booking/${slug}`} className="mt-2 inline-flex items-center gap-1 px-4 py-2 bg-sky-700 hover:bg-sky-800 text-white text-[12px] font-bold rounded-lg">
          Đặt ngay
          <Phosphor.ArrowRight size={12} weight="bold" />
        </a>
      </div>
    </div>
  </div>
</article>
```

## 8. Accessibility

- Image `alt` mô tả địa điểm
- Rating có cả số và label text ("Xuất sắc", "Rất tốt")
- Distance visible text, không chỉ icon
- Heart có `aria-pressed`
- CTA `<a>` semantic
- Touch target ≥ 44px

## 9. Performance

- Image 800x450 + srcset responsive
- Gallery thumbnails 120x90, lazy
- `loading="lazy"` dưới fold