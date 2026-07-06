# Destination Bento Showcase

> Bento grid asymmetric hiển thị 7 destinations: 1 hero lớn + 6 cell nhỏ. Mỗi cell có ảnh thật destination, giá từ, rating, CTA khám phá.

## 1. Mục đích

Showcase 7 destinations nổi bật trong 1 grid nhưng visual diversity cao (asymmetric). Thay thế "3-equal-cards" anti-pattern.

## 2. Asset

| Element | Source |
|---|---|
| Destination photos | Unsplash curated 7 destinations |
| Country flag / icon | Phosphor simple |

## 3. Layout grid (desktop)

```
┌─────────────────────┬───────────────┬───────────────┐
│                     │               │               │
│   HERO (big)        │   Cell 2      │   Cell 3      │
│   Phú Quốc          │   Đà Lạt      │   Hội An      │
│   16:9 + overlays   │   4:5         │   4:5         │
│                     │               │               │
├──────────┬──────────┼───────────────┼───────────────┤
│          │          │               │               │
│ Cell 4   │  Cell 5  │   Cell 6      │   Cell 7      │
│ Bangkok  │  Bali    │   Tokyo       │   Singapore   │
│ 1:1      │  1:1     │   16:9        │   16:9        │
│          │          │               │               │
└──────────┴──────────┴───────────────┴───────────────┘
```

Grid: 6 columns × 4 rows
- Hero: col-span-3, row-span-2 (big card top-left)
- Cell 2, 3: col-span-2 each, row-span-2 (tall cards top-right)
- Cell 4, 5: col-span-1 each, row-span-1 (small cards bottom-left)
- Cell 6, 7: col-span-3 each (wide cards bottom-right)

## 4. Variants

| Variant | Use | Khác biệt |
|---|---|---|
| `default` | Homepage | Asymmetric 7-cell |
| `seasonal` | Peak season | Highlight 1 destination lớn + 5 nhỏ |
| `compact` | Mid-page | 4-cell grid đơn giản |

## 5. States

| State | Visual |
|---|---|
| default | Static |
| hover | translateY(-3px) + image scale 1.04 |
| focused | Sky ring 2px |
| reduce-motion | No scale transition |

## 6. Icon mapping

| Role | Phosphor |
|---|---|
| Star | `Star` (fill) |
| Price | `CurrencyDollar` |
| Duration | `AirplaneTakeoff` |
| Pin | `MapPin` (fill) |
| Explore arrow | `ArrowRight` |
| Country flags | Emoji (Vietnam 🇻🇳 Japan 🇯🇵) OK |

## 7. Code reference

```tsx
import * as Phosphor from '@phosphor-icons/react';

export interface Destination {
  slug: string;
  name: string;
  country: string;
  flag: string;
  imageId: string;
  flightsPerWeek: number;
  duration: string;
  rating: number;
  reviewCount: number;
  startingPrice: number;
  description: string;
  cellSize: 'hero' | 'tall' | 'small' | 'wide';
}

const DESTINATIONS: Destination[] = [
  {
    slug: 'phu-quoc',
    name: 'Phú Quốc',
    country: 'Việt Nam',
    flag: '🇻🇳',
    imageId: '1582719508461-905c673771fd',
    flightsPerWeek: 487,
    duration: '2h15m',
    rating: 4.8,
    reviewCount: 12847,
    startingPrice: 1290000,
    description: 'Đảo ngọc thiên đường với bãi biển trắng và resort 5 sao',
    cellSize: 'hero'
  },
  {
    slug: 'da-lat',
    name: 'Đà Lạt',
    country: 'Việt Nam',
    flag: '🇻🇳',
    imageId: '1573279107032-d3e88dc7d12a',
    flightsPerWeek: 312,
    duration: '1h50m',
    rating: 4.7,
    reviewCount: 8923,
    startingPrice: 990000,
    description: 'Thành phố ngàn hoa với khí hậu mát mẻ quanh năm',
    cellSize: 'tall'
  },
  {
    slug: 'hoi-an',
    name: 'Hội An',
    country: 'Việt Nam',
    flag: '🇻🇳',
    imageId: '1528127269322-539801943592',
    flightsPerWeek: 256,
    duration: '1h45m',
    rating: 4.9,
    reviewCount: 11420,
    startingPrice: 1190000,
    description: 'Phố cổ đèn lồng ven sông Thu Bồn',
    cellSize: 'tall'
  },
  {
    slug: 'bangkok',
    name: 'Bangkok',
    country: 'Thái Lan',
    flag: '🇹🇭',
    imageId: '1508009603885-50cf7c579365',
    flightsPerWeek: 642,
    duration: '2h10m',
    rating: 4.6,
    reviewCount: 24580,
    startingPrice: 1490000,
    description: 'Thủ đô sôi động với chợ nổi và đền chùa',
    cellSize: 'small'
  },
  {
    slug: 'bali',
    name: 'Bali',
    country: 'Indonesia',
    flag: '🇮🇩',
    imageId: '1537996194471-e657df975ab4',
    flightsPerWeek: 184,
    duration: '4h30m',
    rating: 4.8,
    reviewCount: 18230,
    startingPrice: 2490000,
    description: 'Đảo thần thánh với ruộng bậc thang và đền Hindu',
    cellSize: 'small'
  },
  {
    slug: 'tokyo',
    name: 'Tokyo',
    country: 'Nhật Bản',
    flag: '🇯🇵',
    imageId: '1540959733332-eab4deabeeaf',
    flightsPerWeek: 96,
    duration: '5h45m',
    rating: 4.9,
    reviewCount: 31240,
    startingPrice: 4990000,
    description: 'Siêu đô thị ánh sáng với văn hóa độc đáo',
    cellSize: 'wide'
  },
  {
    slug: 'singapore',
    name: 'Singapore',
    country: 'Singapore',
    flag: '🇸🇬',
    imageId: '1565967511849-76a60a516170',
    flightsPerWeek: 124,
    duration: '3h20m',
    rating: 4.8,
    reviewCount: 19870,
    startingPrice: 3290000,
    description: 'Đảo quốc sư tử với Gardens by the Bay',
    cellSize: 'wide'
  }
];

export function DestinationBento() {
  return (
    <section className="bg-white py-16 lg:py-24" aria-labelledby="destinations-heading">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="flex items-end justify-between mb-10 flex-wrap gap-4">
          <div>
            <span className="inline-block text-[11px] font-bold uppercase tracking-[0.18em] text-sky-600 mb-2">
              Điểm đến nổi bật
            </span>
            <h2 id="destinations-heading" className="text-3xl lg:text-5xl font-extrabold text-slate-900 tracking-tight">
              Khám phá Đông Nam Á
            </h2>
            <p className="mt-2 text-slate-600 max-w-2xl">
              7 điểm đến hàng đầu với 2.500+ chuyến bay và 50.000+ khách sạn mỗi tuần.
            </p>
          </div>
          <a href="/destinations" className="inline-flex items-center gap-1.5 text-[13px] font-semibold text-sky-600 hover:text-sky-700">
            Tất cả 87 điểm đến
            <Phosphor.ArrowRight size={14} weight="bold" />
          </a>
        </div>

        {/* Bento grid */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3 lg:gap-4 lg:auto-rows-[160px]">
          {DESTINATIONS.map(dest => (
            <DestinationCard key={dest.slug} destination={dest} />
          ))}
        </div>
      </div>
    </section>
  );
}

function DestinationCard({ destination }: { destination: Destination }) {
  // Cell sizes (lg breakpoint)
  const sizeMap = {
    hero: 'lg:col-span-3 lg:row-span-2',
    tall: 'lg:col-span-2 lg:row-span-2',
    small: 'lg:col-span-1 lg:row-span-1',
    wide: 'lg:col-span-3 lg:row-span-1'
  } as const;

  const isLarge = destination.cellSize === 'hero' || destination.cellSize === 'tall';

  return (
    <a
      href={`/destinations/${destination.slug}`}
      className={`group relative overflow-hidden rounded-2xl bg-slate-100 hover:shadow-xl transition-all duration-300 ${sizeMap[destination.cellSize]}`}
    >
      {/* Image */}
      <img
        src={`https://images.unsplash.com/photo-${destination.imageId}?w=${isLarge ? '800' : '600'}&h=${isLarge ? '600' : '400'}&fit=crop&q=80`}
        alt={`${destination.name} - ${destination.country}`}
        className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
        style={{ filter: 'saturate(1.05) contrast(1.02)' }}
        loading="lazy"
      />

      {/* Gradient overlay */}
      <div className="absolute inset-0 bg-gradient-to-t from-slate-900/85 via-slate-900/20 to-transparent" />

      {/* Content */}
      <div className="absolute inset-0 p-4 lg:p-5 flex flex-col justify-between text-white">
        {/* Top row */}
        <div className="flex items-start justify-between">
          <span className="text-[10.5px] font-bold uppercase tracking-wider px-2 py-0.5 bg-white/20 backdrop-blur rounded-full">
            {destination.flag} {destination.country}
          </span>
          <span className="inline-flex items-center gap-0.5 text-[10.5px] font-bold bg-white/20 backdrop-blur px-2 py-0.5 rounded-full">
            <Phosphor.Star size={10} weight="fill" className="text-amber-300" />
            {destination.rating}
          </span>
        </div>

        {/* Bottom */}
        <div>
          <h3 className={`font-extrabold leading-tight ${isLarge ? 'text-3xl lg:text-4xl' : 'text-xl'}`}>
            {destination.name}
          </h3>
          {isLarge && (
            <p className="text-[12.5px] text-white/80 mt-1 line-clamp-2 max-w-xs">
              {destination.description}
            </p>
          )}
          <div className="flex items-center gap-2 mt-2 text-[11.5px]">
            <span className="inline-flex items-center gap-1 text-white/90">
              <Phosphor.AirplaneTakeoff size={11} weight="bold" />
              {destination.flightsPerWeek} chuyến/tuần
            </span>
            {isLarge && (
              <span className="inline-flex items-center gap-1 text-white/90">
                <Phosphor.MapPin size={11} weight="bold" />
                {destination.duration}
              </span>
            )}
          </div>
          <div className="mt-2 inline-flex items-baseline gap-1">
            <span className="text-[10.5px] text-white/70">từ</span>
            <span className="text-[18px] font-extrabold tabular-nums">
              {destination.startingPrice.toLocaleString('vi-VN')}₫
            </span>
          </div>
        </div>
      </div>

      {/* Hover CTA */}
      <div className="absolute top-3 right-3 opacity-0 group-hover:opacity-100 transition-opacity">
        <span className="inline-flex items-center gap-1 px-3 py-1.5 bg-sky-600 text-white text-[11px] font-bold rounded-full shadow-lg">
          Khám phá
          <Phosphor.ArrowRight size={11} weight="bold" />
        </span>
      </div>
    </a>
  );
}
```

## 8. Accessibility

- Mỗi card là `<a>` với text mô tả destination visible
- Image alt mô tả location + country
- Country flag dùng emoji + text label (`"🇻🇳 Việt Nam"`)
- Rating có cả số + icon
- Price visible text + tabular-nums
- Hover CTA chỉ show khi hover, không che thông tin khi không hover

## 9. Performance

- Bento grid sử dụng CSS Grid với auto-rows, không hardcode rows
- Images responsive theo cell size
- Hero cell image 800x600, small cells 600x400
- All images `loading="lazy"`
- Filter subtle saturate/contrast để appetite

## 10. Anti-patterns đã tránh

- ❌ 7 cells bằng nhau (đã dùng 4 size khác nhau)
- ❌ Picsum random
- ❌ Stock photo "everything sunny"
- ❌ Generic names ("Beach destination")

---

**Component family**: Layout #3 — `destination-bento`