# Restaurant Card

> Card quán ăn trong search results và homepage collections. Logo/cover ảnh thật, tên quán, rating + reviews, ETA + distance, deals badges, free ship badge, sold count, CTA add favorite.

## 1. Mục đích

Hiển thị 1 quán với đủ thông tin user cần để quyết định có click vào hay không. Ảnh món prominent, rating + sold count cho trust, ETA + distance cho urgency.

## 2. Asset

| Element | Source |
|---|---|
| Hero photo | Unsplash curated dish / restaurant interior |
| Logo | Unsplash curated (hoặc restaurant self-upload) |
| Cuisine icon | Phosphor (Phở, Bún, Cơm...) |

## 3. Cấu trúc

```
┌──────────────────────────────────────────────┐
│  [hero 16:9]                  [♥]            │
│  ┌────────┐  ┌─────────┐                    │
│  │-30%    │  │FREE SHIP│                    │
│  └────────┘  └─────────┘                    │
│ ┌────────────────────────────────────┐       │
│ │ Logo + "Đã đặt 1.847 lần tuần này" │       │
│ └────────────────────────────────────┘       │
├──────────────────────────────────────────────┤
│ Quán Phở Hà Nội                            │
│ ⭐ 4.8 (2.847) · Phở · Bún chả · Cơm      │
│ 📍 Quận 1 · 1,2 km · 25 phút · 49.000₫+   │
│                                              │
│ 💰 Deals:                                    │
│ • Giảm 30% đơn từ 150.000₫                 │
│ • Freeship đơn từ 99.000₫                  │
│                                              │
│ 🕐 Mở cửa · Đang nhận đơn                  │
│                                              │
│ [    Xem quán    ] [    Đặt ngay    ]      │
└──────────────────────────────────────────────┘
```

## 4. Variants

| Variant | Use | Khác biệt |
|---|---|---|
| `default` | Search results | Standard |
| `featured` | Homepage bento | Larger + video overlay |
| `compact` | Horizontal scroll | Smaller, no deals list |
| `closed` | Outside hours | Greyed out + "Đóng cửa" |
| `new` | New on platform | "Mới" badge prominent |

## 5. States

| State | Visual |
|---|---|
| default | Base |
| hover | translateY(-3px) + shadow-lg |
| closed | Greyscale 0.6 + "Đóng cửa" overlay |
| busy | "Đang bận - chờ 35 phút" + ETA orange |
| reduce-motion | No transition |

## 6. Icon mapping

| Role | Phosphor |
|---|---|
| Star | `Star` (fill) |
| Pin | `MapPin` (fill) |
| Distance | `NavigationArrow` |
| Time ETA | `Clock` |
| Delivery | `Motorcycle` |
| Discount | `Tag` (fill) |
| Free ship | `Truck` |
| Heart | `Heart` |
| Open | `Dot` (green) |
| Closed | `Dot` (red) |
| Verified | `SealCheck` (fill) |
| Logo | Image |

## 7. Code reference

```tsx
import * as Phosphor from '@phosphor-icons/react';

export interface Restaurant {
  slug: string;
  name: string;
  cuisineTypes: string[];
  rating: number;
  reviewCount: number;
  address: string;
  distance: number;
  etaMinutes: number;
  priceFloor: number;
  heroImage: string;
  logoImage: string;
  ordersThisWeek: number;
  badges: Array<'discount' | 'freeship' | 'new' | 'featured' | 'top-rated'>;
  discountText?: string;
  isOpen: boolean;
  busyLevel: 'low' | 'normal' | 'busy';
  tags: string[];
}

export function RestaurantCard({ restaurant }: { restaurant: Restaurant }) {
  const busyMap = {
    low: { color: 'text-emerald-600', text: 'Nhận đơn ngay' },
    normal: { color: 'text-amber-600', text: 'Đang nhận đơn' },
    busy: { color: 'text-rose-600', text: `Chờ ~${restaurant.etaMinutes + 10} phút` }
  };
  const busy = busyMap[restaurant.busyLevel];

  return (
    <article className="group relative bg-white rounded-xl border border-slate-200 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300 overflow-hidden">
      <a href={`/restaurants/${restaurant.slug}`} className="block relative aspect-[16/9] overflow-hidden bg-slate-100">
        <img
          src={`https://images.unsplash.com/photo-${restaurant.heroImage}?w=800&h=450&fit=crop&q=80`}
          alt={`${restaurant.name} - ${restaurant.cuisineTypes.join(', ')}`}
          className={`w-full h-full object-cover transition-transform duration-500 group-hover:scale-[1.04] ${restaurant.isOpen ? '' : 'grayscale'}`}
          style={{ filter: 'saturate(1.08) brightness(1.03) contrast(1.02)' }}
          loading="lazy"
        />

        {/* Top-left badges */}
        <div className="absolute top-3 left-3 flex items-center gap-1.5 flex-wrap">
          {restaurant.badges.includes('discount') && (
            <span className="inline-flex items-center gap-1 px-2.5 py-1 bg-rose-500 text-white text-[10.5px] font-bold uppercase tracking-wider rounded-md shadow-md">
              <Phosphor.Tag size={11} weight="fill" />
              {restaurant.discountText || 'DEAL'}
            </span>
          )}
          {restaurant.badges.includes('freeship') && (
            <span className="inline-flex items-center gap-1 px-2.5 py-1 bg-emerald-600 text-white text-[10.5px] font-bold uppercase tracking-wider rounded-md shadow-md">
              <Phosphor.Truck size={11} weight="fill" />
              Free ship
            </span>
          )}
          {restaurant.badges.includes('new') && (
            <span className="inline-flex items-center gap-1 px-2.5 py-1 bg-sky-500 text-white text-[10.5px] font-bold uppercase tracking-wider rounded-md shadow-md">
              <Phosphor.Sparkle size={11} weight="fill" />
              Mới
            </span>
          )}
          {restaurant.badges.includes('featured') && (
            <span className="inline-flex items-center gap-1 px-2.5 py-1 bg-amber-500 text-white text-[10.5px] font-bold uppercase tracking-wider rounded-md shadow-md">
              <Phosphor.Crown size={11} weight="fill" />
              Featured
            </span>
          )}
        </div>

        {/* Top-right: heart */}
        <button
          type="button"
          aria-label={`Lưu quán ${restaurant.name}`}
          className="absolute top-3 right-3 w-9 h-9 bg-white/95 backdrop-blur rounded-full flex items-center justify-center shadow-md hover:bg-white"
        >
          <Phosphor.Heart size={16} weight="regular" className="text-slate-700" />
        </button>

        {/* Logo + orders overlay */}
        <div className="absolute bottom-3 left-3 right-3 flex items-end gap-2">
          <div className="w-12 h-12 rounded-xl overflow-hidden bg-white ring-2 ring-white shadow-md flex-shrink-0">
            <img
              src={`https://images.unsplash.com/photo-${restaurant.logoImage}?w=100&h=100&fit=crop&q=80`}
              alt={`Logo ${restaurant.name}`}
              className="w-full h-full object-cover"
              loading="lazy"
            />
          </div>
          <div className="bg-white/95 backdrop-blur rounded-lg px-2.5 py-1.5 shadow-md">
            <p className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">Đã đặt</p>
            <p className="text-[11.5px] font-bold text-slate-900 tabular-nums">
              {restaurant.ordersThisWeek.toLocaleString('vi-VN')} lần tuần này
            </p>
          </div>
        </div>

        {!restaurant.isOpen && (
          <div className="absolute inset-0 bg-slate-900/70 backdrop-blur-sm flex items-center justify-center">
            <div className="text-center">
              <p className="text-white text-2xl font-extrabold">Đóng cửa</p>
              <p className="text-white/70 text-[12px] mt-1">Mở lúc 10:00 sáng mai</p>
            </div>
          </div>
        )}
      </a>

      <div className="p-4 space-y-3">
        {/* Name + rating */}
        <div>
          <h3 className="text-[16px] font-bold text-slate-900 leading-tight hover:text-emerald-600">
            {restaurant.name}
          </h3>
          <div className="mt-1.5 flex items-center gap-1.5 text-[12px]">
            <span className="inline-flex items-center gap-0.5 px-1.5 py-0.5 bg-amber-500 text-white rounded font-bold tabular-nums">
              <Phosphor.Star size={10} weight="fill" />
              {restaurant.rating}
            </span>
            <span className="text-slate-700 font-semibold tabular-nums">{restaurant.reviewCount.toLocaleString('vi-VN')}</span>
            <span className="text-slate-500">đánh giá</span>
          </div>
          <p className="mt-1 text-[12px] text-slate-500">
            {restaurant.cuisineTypes.join(' · ')}
          </p>
        </div>

        {/* Location + ETA + price floor */}
        <div className="flex items-center gap-x-3 gap-y-1 flex-wrap text-[12px] text-slate-700">
          <span className="inline-flex items-center gap-1">
            <Phosphor.MapPin size={12} weight="fill" className="text-slate-400" />
            {restaurant.distance} km
          </span>
          <span className="inline-flex items-center gap-1">
            <Phosphor.Clock size={12} weight="bold" className="text-slate-400" />
            {restaurant.etaMinutes} phút
          </span>
          <span className="inline-flex items-center gap-1">
            <span className="text-slate-500">Đặt tối thiểu</span>
            <span className="font-bold tabular-nums">{restaurant.priceFloor.toLocaleString('vi-VN')}₫</span>
          </span>
        </div>

        {/* Deals */}
        {(restaurant.discountText || restaurant.badges.includes('freeship')) && (
          <div className="bg-emerald-50 border border-emerald-200 rounded-lg p-2.5 space-y-1">
            {restaurant.discountText && (
              <div className="flex items-center gap-1.5 text-[12px] text-emerald-800">
                <Phosphor.Tag size={12} weight="fill" className="text-emerald-600" />
                <span className="font-semibold">{restaurant.discountText}</span>
              </div>
            )}
            {restaurant.badges.includes('freeship') && (
              <div className="flex items-center gap-1.5 text-[12px] text-emerald-800">
                <Phosphor.Truck size={12} weight="fill" className="text-emerald-600" />
                <span className="font-semibold">Freeship đơn từ 99.000₫</span>
              </div>
            )}
          </div>
        )}

        {/* Open status */}
        <div className="flex items-center gap-1.5 text-[12px]">
          <Phosphor.Dot size={14} weight="fill" className={restaurant.isOpen ? 'text-emerald-500' : 'text-rose-500'} />
          <span className={`font-semibold ${restaurant.isOpen ? busy.color : 'text-rose-600'}`}>
            {restaurant.isOpen ? busy.text : 'Đã đóng'}
          </span>
        </div>

        {/* CTAs */}
        <div className="grid grid-cols-2 gap-2 pt-2 border-t border-slate-100">
          <button className="flex items-center justify-center gap-1 py-2.5 text-[12.5px] font-semibold rounded-lg bg-slate-50 hover:bg-slate-100 text-slate-700">
            <Phosphor.Eye size={13} weight="bold" />
            Xem quán
          </button>
          <button
            disabled={!restaurant.isOpen}
            className="flex items-center justify-center gap-1 py-2.5 text-[12.5px] font-bold rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Phosphor.Bag size={13} weight="bold" />
            Đặt ngay
          </button>
        </div>
      </div>
    </article>
  );
}
```

## 8. Accessibility

- Image alt mô tả tên quán + cuisine types
- Heart button `aria-label` cụ thể
- Discount / freeship badges có icon + text
- Logo alt
- Busy level có icon + text, không chỉ màu
- "Đã đặt X lần tuần này" dùng tabular-nums
- Closed overlay có text + role="status"
- CTA buttons accessible với disabled state rõ
- Reduce-motion: hover translateY off

## 9. Performance

- Hero image 800x450, lazy load
- Logo 100x100, lazy load
- Hover transition 300ms
- Image filter subtle saturation cho appetite

## 10. Anti-patterns đã tránh

- ❌ Generic 3-equal cards (bento layout elsewhere)
- ❌ Stock photo "smiling chef"
- ❌ Emoji-only category (đã image thật)
- ❌ Picsum random
- ❌ No sold count
- ❌ No ETA

---

**Component family**: Layout #2 — `restaurant-card`