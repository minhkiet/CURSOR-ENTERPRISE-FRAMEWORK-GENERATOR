# Bento Cuisines Showcase

> Bento grid asymmetric hiển thị 6 cuisine types Việt Nam + quốc tế: 1 hero lớn + 5 cell nhỏ. Bento shape khác travel (vì food grid ưu tiên dish photo + cuisine type + restaurant count).

## 1. Mục đích

Browse by cuisine. Bento grid cho phép visual diversity và showcase 6 loại ẩm thực trong viewport.

## 2. Asset

| Element | Source |
|---|---|
| Cuisine photos | Unsplash curated 6 cuisines |
| Restaurant count | Mock data |

## 3. Layout grid (desktop)

```
┌────────────────────────┬─────────────┐
│                        │             │
│   HERO (big)           │  Cell 2     │
│   Phở Hà Nội           │  Bún       │
│   16:9                 │  1:1        │
│                        │             │
├────────────────────────┼─────────────┤
│                        │             │
│   Cell 3               │  Cell 4     │
│   Cơm tấm              │  Bánh mì    │
│   16:9                 │  1:1        │
│                        │             │
├─────────────┬──────────┼─────────────┤
│             │          │             │
│ Cell 5      │  Cell 6  │  Cell 7     │
│ Lẩu        │  Trà sữa │  Cà phê     │
│ 1:1         │  16:9    │  16:9       │
│             │          │             │
└─────────────┴──────────┴─────────────┘
```

Grid: 4 columns × 6 rows
- Hero: col-span-2, row-span-2 (big card top-left)
- Cell 2: col-span-2, row-span-1 (tall right)
- Cell 3: col-span-2, row-span-1 (wide middle)
- Cell 4: col-span-2, row-span-1 (tall right)
- Cell 5: col-span-1, row-span-1 (small)
- Cell 6: col-span-2, row-span-1 (wide)
- Cell 7: col-span-1, row-span-1 (small)

## 4. Variants

| Variant | Use | Khác biệt |
|---|---|---|
| `default` | Homepage | 7-cell bento |
| `seasonal` | Tết / Mid-Autumn | Special seasonal cuisines |
| `compact` | Sub-page | 4-cell simple grid |

## 5. States

| State | Visual |
|---|---|
| default | Static |
| hover | translateY(-3px) + image scale 1.05 |
| focused | Ring green 2px |
| reduce-motion | No scale |

## 6. Icon mapping

| Role | Phosphor |
|---|---|
| Phở | `BowlFood` |
| Bún | `Noodles` |
| Cơm | `RiceBowl` |
| Bánh mì | `Bread` |
| Lẩu | `CookingPot` |
| Trà sữa | `Coffee` |
| Cà phê | `Coffee` |
| Pin | `MapPin` |
| Restaurant | `Storefront` |
| Arrow | `ArrowRight` |

## 7. Code reference

```tsx
import * as Phosphor from '@phosphor-icons/react';

export interface Cuisine {
  slug: string;
  name: string;
  description: string;
  imageId: string;
  restaurantCount: number;
  topDishes: string[];
  cellSize: 'hero' | 'tall' | 'wide' | 'small';
  icon: string;
}

const CUISINES: Cuisine[] = [
  {
    slug: 'pho',
    name: 'Phở Hà Nội',
    description: 'Nước dùng ninh xương 12 tiếng, bò tái chín tới',
    imageId: '1576577445504-6af96477db52',
    restaurantCount: 247,
    topDishes: ['Phở bò tái', 'Phở gà', 'Phở bò viên'],
    cellSize: 'hero',
    icon: 'BowlFood'
  },
  {
    slug: 'bun',
    name: 'Bún',
    description: 'Bún chả, bún bò Huế, bún riêu',
    imageId: '1552611052-33e04de081de',
    restaurantCount: 213,
    topDishes: ['Bún chả Hà Nội', 'Bún bò Huế', 'Bún riêu cua'],
    cellSize: 'tall',
    icon: 'Noodles'
  },
  {
    slug: 'com-tam',
    name: 'Cơm tấm',
    description: 'Sườn nướng, bì, chả, trứng ốp la',
    imageId: '1565299624946-b28f40a0ae38',
    restaurantCount: 189,
    topDishes: ['Cơm tấm sườn', 'Cơm tấm bì', 'Cơm tấm chả'],
    cellSize: 'wide',
    icon: 'RiceBowl'
  },
  {
    slug: 'banh-mi',
    name: 'Bánh mì',
    description: 'Ổ bánh mì giòn với pate, thịt nguội, rau thơm',
    imageId: '1559054663-e8d23213f55c',
    restaurantCount: 156,
    topDishes: ['Bánh mì thịt', 'Bánh mì chả cá', 'Bánh mì pate'],
    cellSize: 'tall',
    icon: 'Bread'
  },
  {
    slug: 'lau',
    name: 'Lẩu',
    description: 'Lẩu Thái, lẩu bò, lẩu hải sản cho nhóm',
    imageId: '1547573854-74d2a71d0826',
    restaurantCount: 78,
    topDishes: ['Lẩu Thái', 'Lẩu bò', 'Lẩu hải sản'],
    cellSize: 'small',
    icon: 'CookingPot'
  },
  {
    slug: 'tra-sua',
    name: 'Trà sữa',
    description: 'Trân châu đường đen, matcha, fruit tea',
    imageId: '1556679343-c7306c1976bc',
    restaurantCount: 312,
    topDishes: ['Trà sữa trân châu', 'Matcha latte', 'Fruit tea'],
    cellSize: 'wide',
    icon: 'Coffee'
  },
  {
    slug: 'ca-phe',
    name: 'Cà phê',
    description: 'Cà phê sữa đá, cốt dừa, robusta Đà Lạt',
    imageId: '1495474472287-4d71bcdd2085',
    restaurantCount: 287,
    topDishes: ['Cà phê sữa đá', 'Bạc xỉu', 'Cà phê cốt dừa'],
    cellSize: 'small',
    icon: 'Coffee'
  }
];

export function BentoCuisines() {
  return (
    <section className="bg-white py-16 lg:py-24" aria-labelledby="cuisines-heading">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="flex items-end justify-between mb-10 flex-wrap gap-4">
          <div>
            <span className="inline-block text-[11px] font-bold uppercase tracking-[0.18em] text-emerald-600 mb-2">
              Khám phá ẩm thực
            </span>
            <h2 id="cuisines-heading" className="text-3xl lg:text-5xl font-extrabold text-slate-900 tracking-tight">
              7 cuisine hàng đầu
            </h2>
            <p className="mt-2 text-slate-600 max-w-2xl">
              Từ phở Hà Nội đến cà phê sữa đá Sài Gòn. 1.482 quán verified, giao trong 25 phút.
            </p>
          </div>
          <a href="/cuisines" className="inline-flex items-center gap-1.5 text-[13px] font-semibold text-emerald-600 hover:text-emerald-700">
            Xem tất cả 18 cuisine
            <Phosphor.ArrowRight size={14} weight="bold" />
          </a>
        </div>

        {/* Bento grid */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 lg:gap-4 lg:auto-rows-[140px]">
          {CUISINES.map(c => (
            <CuisineCard key={c.slug} cuisine={c} />
          ))}
        </div>
      </div>
    </section>
  );
}

function CuisineCard({ cuisine }: { cuisine: Cuisine }) {
  const sizeMap = {
    hero: 'lg:col-span-2 lg:row-span-2',
    tall: 'lg:col-span-2 lg:row-span-1',
    wide: 'lg:col-span-2 lg:row-span-1',
    small: 'lg:col-span-1 lg:row-span-1'
  } as const;

  const isLarge = cuisine.cellSize === 'hero' || cuisine.cellSize === 'tall';

  return (
    <a
      href={`/cuisines/${cuisine.slug}`}
      className={`group relative overflow-hidden rounded-2xl bg-slate-100 hover:shadow-xl transition-all duration-300 ${sizeMap[cuisine.cellSize]}`}
    >
      <img
        src={`https://images.unsplash.com/photo-${cuisine.imageId}?w=${isLarge ? '800' : '500'}&h=${isLarge ? '500' : '300'}&fit=crop&q=80`}
        alt={`${cuisine.name} - ${cuisine.description}`}
        className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
        style={{ filter: 'saturate(1.10) brightness(1.04) contrast(1.03)' }}
        loading="lazy"
      />
      <div className="absolute inset-0 bg-gradient-to-t from-slate-900/85 via-slate-900/30 to-transparent" />

      <div className="absolute inset-0 p-4 lg:p-5 flex flex-col justify-between text-white">
        {/* Top */}
        <div className="flex items-start justify-between">
          <span className="inline-flex items-center gap-1 px-2 py-0.5 bg-white/20 backdrop-blur rounded-md text-[10.5px] font-bold uppercase tracking-wider">
            <Phosphor.Storefront size={10} weight="bold" />
            {cuisine.restaurantCount} quán
          </span>
        </div>

        {/* Bottom */}
        <div>
          <div className="flex items-center gap-1.5">
            <h3 className={`font-extrabold leading-tight ${isLarge ? 'text-3xl lg:text-4xl' : 'text-xl'}`}>
              {cuisine.name}
            </h3>
          </div>
          {isLarge && (
            <p className="text-[12px] text-white/80 mt-1 line-clamp-2 max-w-xs">
              {cuisine.description}
            </p>
          )}
          {cuisine.cellSize === 'hero' && (
            <div className="mt-2 flex flex-wrap gap-1.5">
              {cuisine.topDishes.slice(0, 2).map(dish => (
                <span key={dish} className="px-2 py-0.5 bg-white/20 backdrop-blur rounded text-[10.5px] font-semibold">
                  {dish}
                </span>
              ))}
            </div>
          )}
          <div className="mt-2 opacity-0 group-hover:opacity-100 transition-opacity">
            <span className="inline-flex items-center gap-1 text-[11.5px] font-bold text-emerald-300">
              Khám phá
              <Phosphor.ArrowRight size={11} weight="bold" />
            </span>
          </div>
        </div>
      </div>
    </a>
  );
}
```

## 8. Accessibility

- Mỗi card là `<a>` với text mô tả cuisine
- Image alt mô tả cuisine + description
- Restaurant count badge có icon + text
- Hover CTA chỉ show khi hover
- Focus visible ring green
- Reduce-motion: hover scale off

## 9. Performance

- Bento grid auto-rows cho responsive
- Images responsive theo cell size
- Hero cell image 800x500, small cells 500x300
- All images `loading="lazy"`
- Filter subtle saturation + brightness cho appetite

## 10. Anti-patterns đã tránh

- ❌ 7 cells bằng nhau (đã 4 size khác nhau)
- ❌ Picsum random
- ❌ Generic "Asian food"
- ❌ Stock "person eating"
- ❌ Chỉ image không text

---

**Component family**: Layout #4 — `bento-cuisines`