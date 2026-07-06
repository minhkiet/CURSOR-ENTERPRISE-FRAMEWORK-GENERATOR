# Bowl & Bite. Landing Page Demo (Food Delivery Vertical)

> Single-page React/Next.js demo for Bowl & Bite food delivery. Showcases mega hero with search + categories, restaurant collections, bento cuisines, promo banner, mega footer.

## File structure

```
demos/food-delivery/
├── package.json
├── next.config.js
├── tailwind.config.ts
├── tsconfig.json
├── postcss.config.js
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   ├── globals.css
│   └── components/
│       ├── StickyHeader.tsx
│       ├── MegaHero.tsx        # Hero + search + categories strip
│       ├── PromoBanner.tsx     # Flash deal countdown
│       ├── RestaurantList.tsx  # Nearby + trending
│       ├── BentoCuisines.tsx
│       ├── PromoCarousel.tsx   # Voucher stack
│       ├── AppDownload.tsx
│       └── MegaFooter.tsx
└── data/
    └── restaurants.ts
```

## 1. package.json

```json
{
  "name": "bowl-bite-demo",
  "version": "2026.1",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  },
  "dependencies": {
    "next": "14.2.5",
    "react": "18.3.1",
    "react-dom": "18.3.1",
    "@phosphor-icons/react": "2.1.7",
    "tailwindcss": "3.4.10"
  },
  "devDependencies": {
    "typescript": "5.5.4",
    "@types/react": "18.3.3",
    "@types/react-dom": "18.3.0",
    "autoprefixer": "10.4.20",
    "postcss": "8.4.41"
  }
}
```

## 2. tailwind.config.ts

```ts
import type { Config } from 'tailwindcss';

export default {
  content: ['./app/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        brand: { 50: '#f0fdf4', 100: '#dcfce7', 500: '#22c55e', 600: '#16a34a', 700: '#15803d' },
        coral: { 50: '#fff7ed', 500: '#f97316', 600: '#ea580c' }
      },
      fontFamily: {
        display: ['Plus Jakarta Sans', 'Be Vietnam Pro', 'system-ui', 'sans-serif'],
        body: ['Plus Jakarta Sans', 'Be Vietnam Pro', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'ui-monospace', 'monospace']
      }
    }
  },
  plugins: []
} satisfies Config;
```

## 3. app/globals.css

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --color-brand: #16a34a;
  --color-brand-hover: #15803d;
  --color-accent: #ea580c;
}

html { scroll-behavior: smooth; }
body {
  font-family: 'Plus Jakarta Sans', 'Be Vietnam Pro', system-ui, sans-serif;
  color: #0f172a;
  background: #fff;
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
}

*:focus-visible {
  outline: 2px solid var(--color-brand);
  outline-offset: 2px;
  border-radius: 4px;
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}

.tabular-nums { font-variant-numeric: tabular-nums; }
.scrollbar-hide { scrollbar-width: none; }
.scrollbar-hide::-webkit-scrollbar { display: none; }
```

## 4. app/layout.tsx

```tsx
import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Bowl & Bite. Ăn ngon giao 25 phút | Hà Nội & TP.HCM',
  description: '3.200+ quán verified. Phở, bún, cơm tấm, bánh mì, lẩu, trà sữa. Freeship đơn từ 99.000₫.',
  openGraph: {
    title: 'Bowl & Bite. Ăn ngon giao 25 phút',
    description: '3.200+ quán verified · Freeship 24/7',
    type: 'website',
    locale: 'vi_VN'
  }
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="vi">
      <body>{children}</body>
    </html>
  );
}
```

## 5. app/page.tsx

```tsx
import { StickyHeader } from './components/StickyHeader';
import { MegaHero } from './components/MegaHero';
import { PromoBanner } from './components/PromoBanner';
import { RestaurantList } from './components/RestaurantList';
import { BentoCuisines } from './components/BentoCuisines';
import { PromoCarousel } from './components/PromoCarousel';
import { AppDownload } from './components/AppDownload';
import { MegaFooter } from './components/MegaFooter';

export default function HomePage() {
  return (
    <>
      <StickyHeader />
      <main>
        <MegaHero />
        <PromoBanner />
        <RestaurantList />
        <BentoCuisines />
        <PromoCarousel />
        <AppDownload />
      </main>
      <MegaFooter />
    </>
  );
}
```

## 6. app/components/StickyHeader.tsx

```tsx
'use client';
import { useState, useEffect } from 'react';
import * as Phosphor from '@phosphor-icons/react';

export function StickyHeader() {
  const [scrolled, setScrolled] = useState(false);
  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 50);
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  return (
    <header className={`fixed top-0 inset-x-0 z-50 transition-all duration-300 ${
      scrolled ? 'bg-white shadow-md' : 'bg-white/95 backdrop-blur'
    }`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <a href="/" className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-emerald-500 to-amber-500 flex items-center justify-center text-white font-extrabold text-lg">
              B
            </div>
            <span className="font-extrabold text-lg text-slate-900 tracking-tight">
              Bowl & Bite
            </span>
          </a>

          <nav className="hidden lg:flex items-center gap-7 text-[14px] font-semibold text-slate-700">
            <a href="/pho" className="hover:text-emerald-600">Phở</a>
            <a href="/bun" className="hover:text-emerald-600">Bún</a>
            <a href="/com-tam" className="hover:text-emerald-600">Cơm tấm</a>
            <a href="/banh-mi" className="hover:text-emerald-600">Bánh mì</a>
            <a href="/lau" className="hover:text-emerald-600">Lẩu</a>
            <a href="/tra-sua" className="hover:text-emerald-600">Trà sữa</a>
          </nav>

          <div className="flex items-center gap-3">
            <button className="hidden md:flex items-center gap-1.5 text-[13px] font-semibold text-slate-700 hover:text-emerald-600 px-2 py-2">
              <Phosphor.MagnifyingGlass size={14} weight="bold" />
              Tìm món
            </button>
            <a href="tel:19001515" className="hidden md:flex items-center gap-1.5 text-[13px] font-semibold text-slate-700 hover:text-emerald-600">
              <Phosphor.Phone size={14} weight="bold" />
              1900 1515
            </a>
            <a href="/login" className="hidden sm:inline-flex text-[13px] font-semibold text-slate-700 hover:text-emerald-600 px-3 py-2">
              Đăng nhập
            </a>
            <a href="/cart" className="relative inline-flex items-center gap-1.5 px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white text-[13px] font-bold rounded-lg">
              <Phosphor.ShoppingBag size={16} weight="bold" />
              Giỏ
              <span className="absolute -top-1 -right-1 w-4 h-4 bg-rose-500 text-white text-[10px] font-bold rounded-full flex items-center justify-center">
                2
              </span>
            </a>
          </div>
        </div>
      </div>
    </header>
  );
}
```

## 7. app/components/MegaHero.tsx

```tsx
'use client';
import { useState } from 'react';
import * as Phosphor from '@phosphor-icons/react';

const CATEGORIES = [
  { id: 'pho', name: 'Phở', image: '1576577445504-6af96477db52', count: 247 },
  { id: 'com', name: 'Cơm tấm', image: '1565299624946-b28f40a0ae38', count: 189 },
  { id: 'banhmi', name: 'Bánh mì', image: '1559054663-e8d23213f55c', count: 156 },
  { id: 'bun', name: 'Bún', image: '1569718212165-3a8278d5f624', count: 213 },
  { id: 'lau', name: 'Lẩu', image: '1547573854-74d2a71d0826', count: 78 },
  { id: 'trasua', name: 'Trà sữa', image: '1556679343-c7306c1976bc', count: 312 },
  { id: 'che', name: 'Chè', image: '1551024506-0bccd828d307', count: 134 },
  { id: 'caphe', name: 'Cà phê', image: '1495474472287-4d71bcdd2085', count: 287 },
  { id: 'vegan', name: 'Đồ chay', image: '1546069901-ba9599a7e63c', count: 95 },
  { id: 'dessert', name: 'Tráng miệng', image: '1551024506-0bccd828d307', count: 167 }
];

export function MegaHero() {
  const [location, setLocation] = useState('Quận 1, TP.HCM');

  return (
    <>
      <section className="relative bg-slate-900 overflow-hidden pt-16" aria-label="Tìm đồ ăn">
        <div className="absolute inset-0 h-[680px] lg:h-[720px]" aria-hidden="true">
          <img
            src="https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=1920&h=1080&fit=crop&q=80"
            alt=""
            className="w-full h-full object-cover"
            style={{ filter: 'saturate(1.10) brightness(0.7) contrast(1.05)' }}
          />
          <div className="absolute inset-0 bg-gradient-to-b from-slate-900/60 via-slate-900/30 to-slate-900/80" />
        </div>

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-16 pb-32 lg:pt-20 lg:pb-40">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 bg-emerald-500/20 backdrop-blur border border-emerald-400/30 rounded-full text-emerald-300 text-[11px] font-bold uppercase tracking-wider mb-6">
            <Phosphor.SealCheck size={14} weight="fill" />
            3.200+ quán đã verify · 4.8★ từ 487.000 đánh giá
          </div>

          <h1 className="text-white text-[40px] sm:text-[56px] lg:text-[80px] font-extrabold leading-[1.05] tracking-tight max-w-3xl">
            Ăn ngon.<br />
            <span className="text-emerald-400">Giao 25 phút.</span>
          </h1>

          <p className="mt-6 text-white/85 text-[16px] lg:text-[18px] leading-relaxed max-w-xl">
            Từ phở bò tái đến bún chả Hà Nội. Đặt trước tích điểm, đổi free ship.
          </p>

          {/* Search widget */}
          <div className="mt-8 bg-white rounded-2xl shadow-2xl p-3 lg:p-4 max-w-3xl">
            <button
              type="button"
              className="flex items-center gap-2 px-3 py-2 hover:bg-slate-50 rounded-lg transition-colors w-full text-left"
            >
              <Phosphor.MapPin size={16} weight="fill" className="text-emerald-600" />
              <span className="text-[11px] text-slate-500 font-bold uppercase tracking-wider">Giao đến</span>
              <span className="text-[14px] font-bold text-slate-900">{location}</span>
              <Phosphor.CaretDown size={14} weight="bold" className="text-slate-400 ml-auto" />
            </button>

            <div className="mt-2 flex items-stretch gap-2">
              <div className="relative flex-1">
                <Phosphor.MagnifyingGlass size={16} weight="bold" className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                <input
                  type="text"
                  placeholder="Phở, bún chả, cơm tấm..."
                  className="w-full pl-10 pr-3 py-3 bg-slate-50 hover:bg-slate-100 border border-slate-200 rounded-lg text-[14px] focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:bg-white"
                />
              </div>
              <button className="px-6 py-3 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-lg inline-flex items-center gap-2 whitespace-nowrap">
                <Phosphor.MagnifyingGlass size={16} weight="bold" />
                Tìm đồ ăn
              </button>
            </div>
          </div>

          <div className="mt-8 flex flex-wrap items-center gap-x-6 gap-y-2 text-white/85 text-[13px]">
            <span className="inline-flex items-center gap-1.5">
              <Phosphor.Motorcycle size={14} weight="fill" className="text-emerald-400" />
              <strong className="font-bold">Freeship</strong> 24/7 đơn từ 99.000₫
            </span>
            <span className="inline-flex items-center gap-1.5">
              <Phosphor.Clock size={14} weight="fill" className="text-emerald-400" />
              Trung bình <strong className="font-bold">25 phút</strong>
            </span>
            <span className="inline-flex items-center gap-1.5">
              <Phosphor.SealCheck size={14} weight="fill" className="text-emerald-400" />
              <strong className="font-bold">3.200+</strong> quán verified
            </span>
          </div>
        </div>
      </section>

      {/* Categories strip */}
      <section className="bg-white -mt-12 relative z-10 border-b border-slate-100" aria-label="Danh mục món">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center gap-4 overflow-x-auto pb-2 -mx-2 px-2 scrollbar-hide">
            {CATEGORIES.map(cat => (
              <a
                key={cat.id}
                href={`/c/${cat.id}`}
                className="group flex-shrink-0 flex flex-col items-center gap-2 w-20"
              >
                <div className="w-16 h-16 rounded-full overflow-hidden bg-slate-100 ring-2 ring-slate-100 group-hover:ring-emerald-500 transition-all">
                  <img
                    src={`https://images.unsplash.com/photo-${cat.image}?w=128&h=128&fit=crop&q=80`}
                    alt={cat.name}
                    className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                    style={{ filter: 'saturate(1.10) brightness(1.03)' }}
                    loading="lazy"
                  />
                </div>
                <div className="text-center">
                  <p className="text-[12.5px] font-bold text-slate-900 group-hover:text-emerald-600 transition-colors">{cat.name}</p>
                  <p className="text-[10px] text-slate-500 tabular-nums">{cat.count} quán</p>
                </div>
              </a>
            ))}
          </div>
        </div>
      </section>
    </>
  );
}
```

## 8. app/components/PromoBanner.tsx

```tsx
'use client';
import { useState, useEffect } from 'react';
import * as Phosphor from '@phosphor-icons/react';

export function PromoBanner() {
  const [copied, setCopied] = useState(false);
  const [mounted, setMounted] = useState(false);
  const [tl, setTl] = useState({ h: 2, m: 14, s: 33 });
  const expiresAt = new Date(Date.now() + 2.2 * 3600000);

  useEffect(() => {
    setMounted(true);
    const tick = () => {
      const total = expiresAt.getTime() - Date.now();
      const h = Math.floor(total / 3600000);
      const m = Math.floor((total % 3600000) / 60000);
      const s = Math.floor((total % 60000) / 1000);
      setTl({ h, m, s });
    };
    tick();
    const id = setInterval(tick, 1000);
    return () => clearInterval(id);
  }, []);

  const copyCode = async () => {
    await navigator.clipboard.writeText('BOWL30');
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 lg:py-12">
      <div className="relative bg-gradient-to-r from-emerald-600 via-emerald-500 to-amber-500 rounded-2xl overflow-hidden shadow-xl">
        <div className="absolute inset-0 opacity-10" aria-hidden="true">
          <svg className="w-full h-full" preserveAspectRatio="xMidYMid slice" viewBox="0 0 200 200">
            <pattern id="dots" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
              <circle cx="10" cy="10" r="2" fill="white" />
            </pattern>
            <rect width="200" height="200" fill="url(#dots)" />
          </svg>
        </div>

        <div className="absolute left-1/2 top-0 bottom-0 flex flex-col items-center justify-between py-2 pointer-events-none" aria-hidden="true">
          <div className="w-4 h-4 rounded-full bg-white" />
          <div className="w-4 h-4 rounded-full bg-white" />
        </div>

        <div className="relative grid grid-cols-1 md:grid-cols-2 gap-4 p-6 lg:p-7">
          <div className="text-white">
            <div className="inline-flex items-center gap-1.5 px-2.5 py-1 bg-white/20 backdrop-blur rounded-full text-[10.5px] font-bold uppercase tracking-wider mb-3">
              <Phosphor.Star size={11} weight="fill" className="text-amber-200" />
              Flash deal
            </div>
            <p className="text-[36px] lg:text-[48px] font-extrabold leading-none tracking-tight">
              GIẢM 30%
            </p>
            <p className="mt-2 text-white/95 text-[14px]">Cho đơn đầu tiên qua app, đơn từ 150.000₫</p>
          </div>

          <div className="bg-white/15 backdrop-blur rounded-xl p-4 border border-white/20">
            <div className="flex items-center gap-2">
              <code className="flex-1 px-3 py-2.5 bg-white rounded-lg text-[16px] font-extrabold tracking-wider text-slate-900 tabular-nums text-center">
                BOWL30
              </code>
              <button
                type="button"
                onClick={copyCode}
                aria-label="Sao chép mã BOWL30"
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

            <div className="mt-3 bg-slate-900 rounded-lg px-3 py-2 text-center">
              <span className="text-[10.5px] font-bold uppercase tracking-wider text-slate-300">Còn</span>
              {mounted ? (
                <div className="flex items-center justify-center gap-1 mt-0.5 text-white font-extrabold tabular-nums">
                  <span className="text-[18px]">{String(tl.h).padStart(2, '0')}</span>
                  <span className="text-slate-500">:</span>
                  <span className="text-[18px]">{String(tl.m).padStart(2, '0')}</span>
                  <span className="text-slate-500">:</span>
                  <span className="text-[18px]">{String(tl.s).padStart(2, '0')}</span>
                </div>
              ) : (
                <div className="text-white text-[18px] font-extrabold tabular-nums mt-0.5">02:14:33</div>
              )}
            </div>

            <p className="mt-3 text-[11px] text-white/80 text-center">
              HSD: 25/07/2026 · Áp dụng 1 lần
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
```

## 9. app/components/RestaurantList.tsx

```tsx
import * as Phosphor from '@phosphor-icons/react';
import { RESTAURANTS } from '@/data/restaurants';

export function RestaurantList() {
  return (
    <section className="bg-white py-12 lg:py-20" aria-labelledby="restaurants-heading">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-end justify-between mb-10 flex-wrap gap-4">
          <div>
            <span className="inline-flex items-center gap-2 text-[11px] font-bold uppercase tracking-[0.18em] text-emerald-600 mb-2">
              <Phosphor.MapPin size={14} weight="fill" />
              Gần bạn · 1,2 km
            </span>
            <h2 id="restaurants-heading" className="text-3xl lg:text-5xl font-extrabold text-slate-900 tracking-tight">
              6 quán đang hot gần đây
            </h2>
          </div>
          <a href="/restaurants" className="inline-flex items-center gap-1.5 text-[13px] font-semibold text-emerald-600 hover:text-emerald-700">
            Xem 3.200+ quán
            <Phosphor.ArrowRight size={14} weight="bold" />
          </a>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {RESTAURANTS.slice(0, 6).map(r => (
            <RestaurantCard key={r.slug} restaurant={r} />
          ))}
        </div>
      </div>
    </section>
  );
}

function RestaurantCard({ restaurant }: { restaurant: any }) {
  const busyMap = {
    low: { color: 'text-emerald-600', text: 'Nhận đơn ngay' },
    normal: { color: 'text-amber-600', text: 'Đang nhận đơn' },
    busy: { color: 'text-rose-600', text: `Chờ ~${restaurant.etaMinutes + 10} phút` }
  };
  const busy = busyMap[restaurant.busyLevel as keyof typeof busyMap];

  return (
    <article className="group bg-white rounded-xl border border-slate-200 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300 overflow-hidden">
      <a href={`/restaurants/${restaurant.slug}`} className="block relative aspect-[16/9] overflow-hidden bg-slate-100">
        <img
          src={`https://images.unsplash.com/photo-${restaurant.heroImage}?w=800&h=450&fit=crop&q=80`}
          alt={`${restaurant.name} - ${restaurant.cuisineTypes.join(', ')}`}
          className={`w-full h-full object-cover transition-transform duration-500 group-hover:scale-[1.04] ${restaurant.isOpen ? '' : 'grayscale'}`}
          style={{ filter: 'saturate(1.08) brightness(1.03) contrast(1.02)' }}
          loading="lazy"
        />

        <div className="absolute top-3 left-3 flex items-center gap-1.5 flex-wrap">
          {restaurant.badges.includes('discount') && (
            <span className="inline-flex items-center gap-1 px-2.5 py-1 bg-rose-500 text-white text-[10.5px] font-bold uppercase tracking-wider rounded-md shadow-md">
              <Phosphor.Tag size={11} weight="fill" />
              {restaurant.discountText}
            </span>
          )}
          {restaurant.badges.includes('freeship') && (
            <span className="inline-flex items-center gap-1 px-2.5 py-1 bg-emerald-600 text-white text-[10.5px] font-bold uppercase tracking-wider rounded-md shadow-md">
              <Phosphor.Truck size={11} weight="fill" />
              Free ship
            </span>
          )}
        </div>

        <button
          aria-label={`Lưu quán ${restaurant.name}`}
          className="absolute top-3 right-3 w-9 h-9 bg-white/95 backdrop-blur rounded-full flex items-center justify-center shadow-md"
        >
          <Phosphor.Heart size={16} weight="regular" className="text-slate-700" />
        </button>

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
      </a>

      <div className="p-4 space-y-3">
        <div>
          <h3 className="text-[16px] font-bold text-slate-900 leading-tight hover:text-emerald-600">{restaurant.name}</h3>
          <div className="mt-1.5 flex items-center gap-1.5 text-[12px]">
            <span className="inline-flex items-center gap-0.5 px-1.5 py-0.5 bg-amber-500 text-white rounded font-bold tabular-nums">
              <Phosphor.Star size={10} weight="fill" />
              {restaurant.rating}
            </span>
            <span className="text-slate-700 font-semibold tabular-nums">{restaurant.reviewCount.toLocaleString('vi-VN')}</span>
            <span className="text-slate-500">đánh giá</span>
          </div>
          <p className="mt-1 text-[12px] text-slate-500">{restaurant.cuisineTypes.join(' · ')}</p>
        </div>

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

        {restaurant.discountText && (
          <div className="bg-emerald-50 border border-emerald-200 rounded-lg p-2.5 flex items-center gap-1.5 text-[12px] text-emerald-800">
            <Phosphor.Tag size={12} weight="fill" className="text-emerald-600" />
            <span className="font-semibold">{restaurant.discountText}</span>
          </div>
        )}

        <div className="flex items-center gap-1.5 text-[12px]">
          <Phosphor.Dot size={14} weight="fill" className={restaurant.isOpen ? 'text-emerald-500' : 'text-rose-500'} />
          <span className={`font-semibold ${restaurant.isOpen ? busy.color : 'text-rose-600'}`}>
            {restaurant.isOpen ? busy.text : 'Đã đóng'}
          </span>
        </div>

        <div className="grid grid-cols-2 gap-2 pt-2 border-t border-slate-100">
          <button className="flex items-center justify-center gap-1 py-2.5 text-[12.5px] font-semibold rounded-lg bg-slate-50 hover:bg-slate-100 text-slate-700">
            <Phosphor.Eye size={13} weight="bold" />
            Xem quán
          </button>
          <button
            disabled={!restaurant.isOpen}
            className="flex items-center justify-center gap-1 py-2.5 text-[12.5px] font-bold rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white disabled:opacity-50"
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

## 10. app/components/BentoCuisines.tsx

```tsx
import * as Phosphor from '@phosphor-icons/react';

const CUISINES = [
  { slug: 'pho', name: 'Phở Hà Nội', description: 'Nước dùng ninh xương 12 tiếng, bò tái chín tới', imageId: '1576577445504-6af96477db52', restaurantCount: 247, topDishes: ['Phở bò tái', 'Phở gà', 'Phở bò viên'], cellSize: 'hero' as const },
  { slug: 'bun', name: 'Bún', description: 'Bún chả, bún bò Huế, bún riêu', imageId: '1552611052-33e04de081de', restaurantCount: 213, topDishes: ['Bún chả Hà Nội', 'Bún bò Huế'], cellSize: 'tall' as const },
  { slug: 'com-tam', name: 'Cơm tấm', description: 'Sườn nướng, bì, chả, trứng ốp la', imageId: '1565299624946-b28f40a0ae38', restaurantCount: 189, topDishes: ['Cơm tấm sườn', 'Cơm tấm bì'], cellSize: 'wide' as const },
  { slug: 'banh-mi', name: 'Bánh mì', description: 'Ổ bánh mì giòn với pate, thịt nguội, rau thơm', imageId: '1559054663-e8d23213f55c', restaurantCount: 156, topDishes: ['Bánh mì thịt'], cellSize: 'tall' as const },
  { slug: 'lau', name: 'Lẩu', description: 'Lẩu Thái, lẩu bò, lẩu hải sản cho nhóm', imageId: '1547573854-74d2a71d0826', restaurantCount: 78, topDishes: ['Lẩu Thái'], cellSize: 'small' as const },
  { slug: 'tra-sua', name: 'Trà sữa', description: 'Trân châu đường đen, matcha, fruit tea', imageId: '1556679343-c7306c1976bc', restaurantCount: 312, topDishes: ['Trà sữa trân châu'], cellSize: 'wide' as const },
  { slug: 'ca-phe', name: 'Cà phê', description: 'Cà phê sữa đá, cốt dừa, robusta Đà Lạt', imageId: '1495474472287-4d71bcdd2085', restaurantCount: 287, topDishes: ['Cà phê sữa đá'], cellSize: 'small' as const }
];

const SIZE_MAP = {
  hero: 'lg:col-span-2 lg:row-span-2',
  tall: 'lg:col-span-2 lg:row-span-1',
  wide: 'lg:col-span-2 lg:row-span-1',
  small: 'lg:col-span-1 lg:row-span-1'
} as const;

export function BentoCuisines() {
  return (
    <section className="bg-slate-50 py-12 lg:py-20" aria-labelledby="cuisines-heading">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-end justify-between mb-10 flex-wrap gap-4">
          <div>
            <span className="inline-block text-[11px] font-bold uppercase tracking-[0.18em] text-emerald-600 mb-2">
              Khám phá ẩm thực
            </span>
            <h2 id="cuisines-heading" className="text-3xl lg:text-5xl font-extrabold text-slate-900 tracking-tight">
              7 cuisine hàng đầu
            </h2>
          </div>
          <a href="/cuisines" className="inline-flex items-center gap-1.5 text-[13px] font-semibold text-emerald-600 hover:text-emerald-700">
            Xem tất cả 18 cuisine
            <Phosphor.ArrowRight size={14} weight="bold" />
          </a>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 lg:gap-4 lg:auto-rows-[140px]">
          {CUISINES.map(c => {
            const isLarge = c.cellSize === 'hero' || c.cellSize === 'tall';
            return (
              <a
                key={c.slug}
                href={`/cuisines/${c.slug}`}
                className={`group relative overflow-hidden rounded-2xl bg-slate-100 hover:shadow-xl transition-all duration-300 ${SIZE_MAP[c.cellSize]}`}
              >
                <img
                  src={`https://images.unsplash.com/photo-${c.imageId}?w=${isLarge ? '800' : '500'}&h=${isLarge ? '500' : '300'}&fit=crop&q=80`}
                  alt={`${c.name} - ${c.description}`}
                  className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
                  style={{ filter: 'saturate(1.10) brightness(1.04) contrast(1.03)' }}
                  loading="lazy"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-slate-900/85 via-slate-900/30 to-transparent" />
                <div className="absolute inset-0 p-4 lg:p-5 flex flex-col justify-between text-white">
                  <div className="flex items-start justify-between">
                    <span className="inline-flex items-center gap-1 px-2 py-0.5 bg-white/20 backdrop-blur rounded-md text-[10.5px] font-bold uppercase tracking-wider">
                      <Phosphor.Storefront size={10} weight="bold" />
                      {c.restaurantCount} quán
                    </span>
                  </div>
                  <div>
                    <h3 className={`font-extrabold leading-tight ${isLarge ? 'text-3xl lg:text-4xl' : 'text-xl'}`}>
                      {c.name}
                    </h3>
                    {isLarge && <p className="text-[12px] text-white/80 mt-1 line-clamp-2 max-w-xs">{c.description}</p>}
                    {c.cellSize === 'hero' && (
                      <div className="mt-2 flex flex-wrap gap-1.5">
                        {c.topDishes.slice(0, 2).map(dish => (
                          <span key={dish} className="px-2 py-0.5 bg-white/20 backdrop-blur rounded text-[10.5px] font-semibold">
                            {dish}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              </a>
            );
          })}
        </div>
      </div>
    </section>
  );
}
```

## 11. app/components/PromoCarousel.tsx

```tsx
'use client';
import { useState } from 'react';
import * as Phosphor from '@phosphor-icons/react';

const VOUCHERS = [
  { id: 'v1', code: 'BOWL30', value: 30, type: 'percent' as const, minOrder: 150000, maxDiscount: 50000, expiresAt: new Date(Date.now() + 7 * 86400000), remaining: 1247, shopName: 'Bowl & Bite' },
  { id: 'v2', code: 'FREESHIP', value: 30000, type: 'fixed' as const, minOrder: 99000, expiresAt: new Date(Date.now() + 14 * 86400000), remaining: 3456, shopName: 'Strikeout' },
  { id: 'v3', code: 'NEWUSER50', value: 50, type: 'percent' as const, minOrder: 100000, maxDiscount: 80000, expiresAt: new Date(Date.now() + 30 * 86400000), remaining: 892, shopName: 'Bowl & Bite' }
];

export function PromoCarousel() {
  return (
    <section className="bg-white py-12 lg:py-20" aria-labelledby="vouchers-heading">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-end justify-between mb-10 flex-wrap gap-4">
          <div>
            <span className="inline-flex items-center gap-2 text-[11px] font-bold uppercase tracking-[0.18em] text-emerald-600 mb-2">
              <Phosphor.Ticket size={14} weight="fill" />
              Mã giảm giá hot
            </span>
            <h2 id="vouchers-heading" className="text-3xl lg:text-5xl font-extrabold text-slate-900 tracking-tight">
              Săn voucher mỗi ngày
            </h2>
          </div>
          <a href="/vouchers" className="inline-flex items-center gap-1.5 text-[13px] font-semibold text-emerald-600 hover:text-emerald-700">
            Xem tất cả 247 voucher
            <Phosphor.ArrowRight size={14} weight="bold" />
          </a>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          {VOUCHERS.map(v => (
            <VoucherCard key={v.id} voucher={v} />
          ))}
        </div>
      </div>
    </section>
  );
}

function VoucherCard({ voucher }: { voucher: any }) {
  const [copied, setCopied] = useState(false);

  const copyCode = async () => {
    await navigator.clipboard.writeText(voucher.code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const valueText = voucher.type === 'percent' ? `Giảm ${voucher.value}%` : `Giảm ${voucher.value.toLocaleString('vi-VN')}₫`;

  return (
    <div className="relative bg-white rounded-xl border-2 border-dashed border-emerald-300 overflow-hidden hover:shadow-lg transition-shadow">
      <div className="absolute left-1/2 top-0 bottom-0 flex flex-col items-center justify-between py-2 pointer-events-none" aria-hidden="true">
        <div className="w-3 h-3 rounded-full bg-slate-50" />
        <div className="w-3 h-3 rounded-full bg-slate-50" />
      </div>

      <div className="grid grid-cols-[1fr_auto]">
        <div className="p-4">
          <div className="flex items-center gap-2 mb-2">
            <div className="w-5 h-5 bg-emerald-100 rounded flex items-center justify-center">
              <Phosphor.Storefront size={12} weight="fill" className="text-emerald-600" />
            </div>
            <span className="text-[11px] font-bold text-slate-700 uppercase tracking-wide truncate">
              {voucher.shopName}
            </span>
          </div>

          <p className="text-[22px] font-extrabold text-slate-900 leading-none">
            {valueText}
            {voucher.maxDiscount && (
              <span className="text-[11px] font-medium text-slate-500 ml-1">
                tối đa {voucher.maxDiscount.toLocaleString('vi-VN')}₫
              </span>
            )}
          </p>

          <p className="mt-1 text-[12px] text-slate-500">Đơn từ {voucher.minOrder.toLocaleString('vi-VN')}₫</p>

          <div className="mt-2 flex items-center gap-3 text-[10.5px] text-slate-500">
            <span className="inline-flex items-center gap-1">
              <Phosphor.CalendarBlank size={10} weight="bold" />
              HSD: {voucher.expiresAt.toLocaleDateString('vi-VN')}
            </span>
            <span className="inline-flex items-center gap-1">
              <Phosphor.UsersThree size={10} weight="bold" />
              Còn {voucher.remaining.toLocaleString('vi-VN')}
            </span>
          </div>
        </div>

        <div className="bg-emerald-50 p-3 flex flex-col items-center justify-center gap-2 min-w-[140px] border-l border-dashed border-emerald-200">
          <code className="px-2 py-1.5 bg-white border-2 border-dashed border-emerald-400 rounded text-[12px] font-extrabold tracking-wider text-slate-900 tabular-nums">
            {voucher.code}
          </code>
          <button
            type="button"
            onClick={copyCode}
            className="w-full px-2 py-1.5 bg-white hover:bg-emerald-100 border border-emerald-300 text-emerald-700 text-[11px] font-bold rounded inline-flex items-center justify-center gap-1"
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
          <button className="w-full px-2 py-1.5 bg-gradient-to-r from-emerald-500 to-emerald-600 hover:from-emerald-600 hover:to-emerald-700 text-white text-[11px] font-extrabold rounded">
            Dùng ngay
          </button>
        </div>
      </div>
    </div>
  );
}
```

## 12. app/components/AppDownload.tsx

```tsx
import * as Phosphor from '@phosphor-icons/react';

export function AppDownload() {
  return (
    <section className="bg-gradient-to-br from-emerald-700 via-emerald-800 to-slate-900 text-white py-16 lg:py-24" aria-labelledby="app-heading">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div>
            <span className="inline-block text-[11px] font-bold uppercase tracking-[0.18em] text-emerald-300 mb-3">
              App Bowl & Bite
            </span>
            <h2 id="app-heading" className="text-3xl lg:text-5xl font-extrabold tracking-tight leading-tight">
              Đặt 1 món free.<br />
              <span className="text-emerald-300">Lần đầu qua app.</span>
            </h2>
            <p className="mt-4 text-white/85 text-[15px] lg:text-[17px] max-w-xl leading-relaxed">
              Mã BOWLFREE cho đơn đầu tiên. Freeship đơn từ 99.000₫. Push notification deal mới mỗi giờ.
            </p>

            <div className="mt-8 flex flex-wrap items-center gap-3">
              <a href="#" className="flex items-center gap-2 px-4 py-3 bg-slate-900 hover:bg-slate-800 border border-slate-700 rounded-lg">
                <Phosphor.AppleLogo size={22} weight="bold" />
                <div className="text-left">
                  <div className="text-[10px] text-slate-400">Tải từ</div>
                  <div className="text-[13px] font-bold">App Store</div>
                </div>
              </a>
              <a href="#" className="flex items-center gap-2 px-4 py-3 bg-slate-900 hover:bg-slate-800 border border-slate-700 rounded-lg">
                <Phosphor.GooglePlayLogo size={22} weight="bold" />
                <div className="text-left">
                  <div className="text-[10px] text-slate-400">Tải từ</div>
                  <div className="text-[13px] font-bold">Google Play</div>
                </div>
              </a>
            </div>

            <div className="mt-8 flex items-center gap-6 text-[13px] text-white/80">
              <span className="inline-flex items-center gap-2">
                <Phosphor.Star size={14} weight="fill" className="text-amber-300" />
                <strong className="font-bold tabular-nums">4.8</strong> · 124.580 đánh giá
              </span>
              <span className="inline-flex items-center gap-2">
                <Phosphor.DownloadSimple size={14} weight="bold" />
                8M+ lượt tải
              </span>
            </div>
          </div>

          <div className="relative">
            <div className="aspect-[9/16] max-w-xs mx-auto bg-slate-900 rounded-[3rem] border-[10px] border-slate-950 shadow-2xl overflow-hidden">
              <img
                src="https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400&h=711&fit=crop&q=80"
                alt="App Bowl & Bite trên điện thoại"
                className="w-full h-full object-cover"
              />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
```

## 13. app/components/MegaFooter.tsx

```tsx
import * as Phosphor from '@phosphor-icons/react';

export function MegaFooter() {
  return (
    <footer className="bg-slate-950 text-slate-300">
      <div className="border-b border-slate-800/50 bg-gradient-to-r from-emerald-900/50 to-amber-900/30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
          <div className="grid grid-cols-1 lg:grid-cols-[1fr_auto] gap-6 items-center">
            <div>
              <h2 className="text-2xl lg:text-3xl font-extrabold text-white">
                Tải app. Đặt 1 món free ngay.
              </h2>
              <p className="mt-1 text-slate-300 text-[14px]">
                Ưu đãi cho đơn đầu tiên qua app. Freeship đơn từ 99.000₫, mã BOWLFREE.
              </p>
            </div>
            <div className="flex flex-wrap items-center gap-3">
              <a href="#" className="flex items-center gap-2 px-4 py-3 bg-slate-900 hover:bg-slate-800 border border-slate-700 rounded-lg">
                <Phosphor.AppleLogo size={22} weight="bold" className="text-white" />
                <div className="text-left">
                  <div className="text-[10px] text-slate-400">Tải từ</div>
                  <div className="text-[13px] font-bold text-white">App Store</div>
                </div>
              </a>
              <a href="#" className="flex items-center gap-2 px-4 py-3 bg-slate-900 hover:bg-slate-800 border border-slate-700 rounded-lg">
                <Phosphor.GooglePlayLogo size={22} weight="bold" className="text-white" />
                <div className="text-left">
                  <div className="text-[10px] text-slate-400">Tải từ</div>
                  <div className="text-[13px] font-bold text-white">Google Play</div>
                </div>
              </a>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-14">
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-7 gap-8 lg:gap-6">
          <div className="col-span-2 lg:col-span-1">
            <a href="/" className="inline-flex items-center gap-2">
              <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-emerald-500 to-amber-500 flex items-center justify-center text-white font-extrabold text-lg">B</div>
              <span className="font-extrabold text-xl text-white tracking-tight">Bowl & Bite</span>
            </a>
            <p className="mt-4 text-[13px] text-slate-400 leading-relaxed">
              Ăn ngon, giao nhanh. 3.200+ quán verified tại Hà Nội, TP.HCM, Đà Nẵng.
            </p>
            <div className="mt-5 space-y-2">
              <a href="tel:19001515" className="flex items-center gap-2 text-[13px] hover:text-white">
                <Phosphor.Phone size={13} weight="bold" className="text-emerald-400" />
                <span className="font-bold text-white tabular-nums">1900 1515</span>
                <span className="text-slate-500">· 24/7</span>
              </a>
              <a href="mailto:hello@bowl.vn" className="flex items-center gap-2 text-[13px] hover:text-white">
                <Phosphor.EnvelopeSimple size={13} weight="bold" className="text-slate-400" />
                hello@bowl.vn
              </a>
            </div>
            <div className="mt-5 flex items-center gap-2">
              <SocialLink icon="FacebookLogo" label="Facebook" />
              <SocialLink icon="InstagramLogo" label="Instagram" />
              <SocialLink icon="YoutubeLogo" label="YouTube" />
              <SocialLink icon="TiktokLogo" label="TikTok" />
            </div>
          </div>

          <FooterColumn title="Ẩm thực" icon="BowlFood" links={[
            { label: 'Phở Hà Nội', href: '#' },
            { label: 'Bún', href: '#' },
            { label: 'Cơm tấm', href: '#' },
            { label: 'Bánh mì', href: '#' },
            { label: 'Lẩu', href: '#' },
            { label: 'Trà sữa', href: '#' },
            { label: 'Cà phê', href: '#' },
            { label: 'Đồ chay', href: '#' }
          ]} />
          <FooterColumn title="Thành phố" icon="MapPin" links={[
            { label: 'TP.HCM (1.482 quán)', href: '#' },
            { label: 'Hà Nội (1.247 quán)', href: '#' },
            { label: 'Đà Nẵng (456 quán)', href: '#' },
            { label: 'Hải Phòng', href: '#' },
            { label: 'Cần Thơ', href: '#' },
            { label: 'Biên Hoà', href: '#' }
          ]} />
          <FooterColumn title="Quán nổi bật" icon="Storefront" links={[
            { label: 'Phở Hà Nội - Q.1', href: '#' },
            { label: 'Bún chả Hàng Mành', href: '#' },
            { label: 'Cơm tấm Cali', href: '#' },
            { label: 'Bánh mì Huỳnh Hoa', href: '#' },
            { label: 'Lẩu Thái Tomyum', href: '#' }
          ]} />
          <FooterColumn title="Đối tác" icon="Handshake" links={[
            { label: 'Đăng ký quán', href: '#' },
            { label: 'Bảng giá', href: '#' },
            { label: 'Dashboard', href: '#' },
            { label: 'Marketing', href: '#' },
            { label: 'Hỗ trợ đối tác', href: '#' }
          ]} />
          <FooterColumn title="Tài xế" icon="Motorcycle" links={[
            { label: 'Đăng ký tài xế', href: '#' },
            { label: 'Yêu cầu tài xế', href: '#' },
            { label: 'Bảng lương', href: '#' },
            { label: 'Bảo hiểm', href: '#' },
            { label: 'Hỗ trợ tài xế', href: '#' }
          ]} />
          <FooterColumn title="Hỗ trợ" icon="Headset" links={[
            { label: 'Trung tâm hỗ trợ', href: '#' },
            { label: 'Đơn hàng của tôi', href: '#' },
            { label: 'Hoàn tiền', href: '#' },
            { label: 'Liên hệ', href: '#' },
            { label: 'FAQ', href: '#' }
          ]} />
        </div>

        <div className="mt-12 pt-8 border-t border-slate-800/50 flex flex-wrap items-center justify-between gap-6">
          <div className="flex flex-wrap items-center gap-2">
            {['visa', 'mastercard', 'jcb', 'amex', 'momo', 'zalopay', 'vnpay', 'shopeepay'].map(slug => (
              <img key={slug} src={`https://cdn.simpleicons.org/${slug}/cbd5e1`} alt={slug} className="h-7 w-12 object-contain bg-white rounded px-1.5 py-1" loading="lazy" />
            ))}
          </div>
          <div className="flex flex-wrap items-center gap-4 text-[11.5px] text-slate-400">
            <span className="inline-flex items-center gap-1.5">
              <Phosphor.ShieldCheck size={14} weight="fill" className="text-emerald-400" />
              Secured payment
            </span>
            <span className="inline-flex items-center gap-1.5">
              <Phosphor.SealCheck size={14} weight="fill" className="text-emerald-400" />
              Quán verified 100%
            </span>
            <span className="inline-flex items-center gap-1.5">
              <Phosphor.Clock size={14} weight="fill" className="text-emerald-400" />
              Hoàn tiền 200% nếu trễ
            </span>
          </div>
        </div>
      </div>

      <div className="border-t border-slate-800/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-5">
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-3 text-[11.5px] text-slate-500">
            <div>© 2026 Bowl & Bite JSC · MST 0315.654.321 · Hotline 1900 1515 · 78 Pasteur, Q.1, TP.HCM</div>
            <div className="flex items-center gap-4">
              <a href="#" className="hover:text-slate-300">Privacy</a>
              <a href="#" className="hover:text-slate-300">Terms</a>
              <a href="#" className="hover:text-slate-300">Cookies</a>
              <a href="#" className="hover:text-slate-300">Sitemap</a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}

function FooterColumn({ title, icon, links }: { title: string; icon: any; links: Array<{ label: string; href: string }> }) {
  const Icon = Phosphor[icon] as any;
  return (
    <div>
      <h3 className="flex items-center gap-1.5 text-[12px] font-bold uppercase tracking-wider text-white mb-4">
        <Icon size={14} weight="bold" className="text-emerald-400" />
        {title}
      </h3>
      <ul className="space-y-2">
        {links.map(link => (
          <li key={link.label}>
            <a href={link.href} className="text-[12.5px] text-slate-400 hover:text-white transition-colors">{link.label}</a>
          </li>
        ))}
      </ul>
    </div>
  );
}

function SocialLink({ icon, label }: { icon: any; label: string }) {
  const Icon = Phosphor[icon] as any;
  return (
    <a href="#" aria-label={`Bowl & Bite trên ${label}`} className="w-8 h-8 inline-flex items-center justify-center bg-slate-900 hover:bg-emerald-600 border border-slate-800 rounded-full transition-colors">
      <Icon size={14} weight="bold" className="text-slate-300" />
    </a>
  );
}
```

## 14. data/restaurants.ts

```ts
export const RESTAURANTS = [
  {
    slug: 'pho-ha-noi-q1',
    name: 'Phở Hà Nội - Quán Cô Lan',
    cuisineTypes: ['Phở', 'Bún'],
    rating: 4.8,
    reviewCount: 2847,
    distance: 1.2,
    etaMinutes: 25,
    priceFloor: 49000,
    heroImage: '1576577445504-6af96477db52',
    logoImage: '1576577445504-6af96477db52',
    ordersThisWeek: 1847,
    badges: ['discount' as const, 'freeship' as const],
    discountText: 'Giảm 30% đơn từ 150.000₫',
    isOpen: true,
    busyLevel: 'normal' as const,
    tags: ['Phở bò tái', 'Bún chả', 'Cơm tấm']
  },
  {
    slug: 'bun-cha-hang-manh',
    name: 'Bún Chả Hàng Mành',
    cuisineTypes: ['Bún', 'Phở'],
    rating: 4.7,
    reviewCount: 1923,
    distance: 2.5,
    etaMinutes: 30,
    priceFloor: 45000,
    heroImage: '1552611052-33e04de081de',
    logoImage: '1552611052-33e04de081de',
    ordersThisWeek: 1234,
    badges: ['freeship' as const],
    discountText: '',
    isOpen: true,
    busyLevel: 'low' as const,
    tags: ['Bún chả', 'Nem rán', 'Phở cuốn']
  },
  {
    slug: 'com-tam-cali',
    name: 'Cơm Tấm Cali',
    cuisineTypes: ['Cơm tấm'],
    rating: 4.6,
    reviewCount: 1456,
    distance: 1.8,
    etaMinutes: 22,
    priceFloor: 55000,
    heroImage: '1565299624946-b28f40a0ae38',
    logoImage: '1565299624946-b28f40a0ae38',
    ordersThisWeek: 987,
    badges: ['discount' as const, 'freeship' as const],
    discountText: 'Giảm 25% đơn từ 100.000₫',
    isOpen: true,
    busyLevel: 'busy' as const,
    tags: ['Cơm tấm sườn', 'Sườn nướng']
  },
  {
    slug: 'banh-mi-huynh-hoa',
    name: 'Bánh Mì Huỳnh Hoa',
    cuisineTypes: ['Bánh mì'],
    rating: 4.9,
    reviewCount: 4521,
    distance: 0.8,
    etaMinutes: 15,
    priceFloor: 35000,
    heroImage: '1559054663-e8d23213f55c',
    logoImage: '1559054663-e8d23213f55c',
    ordersThisWeek: 2456,
    badges: ['freeship' as const],
    discountText: '',
    isOpen: true,
    busyLevel: 'busy' as const,
    tags: ['Bánh mì thịt', 'Pate']
  },
  {
    slug: 'lau-thai-tomyum',
    name: 'Lẩu Thái Tomyum Quán',
    cuisineTypes: ['Lẩu', 'Thái'],
    rating: 4.5,
    reviewCount: 678,
    distance: 3.2,
    etaMinutes: 35,
    priceFloor: 199000,
    heroImage: '1547573854-74d2a71d0826',
    logoImage: '1547573854-74d2a71d0826',
    ordersThisWeek: 234,
    badges: ['discount' as const],
    discountText: 'Giảm 40% set lẩu 2 người',
    isOpen: true,
    busyLevel: 'normal' as const,
    tags: ['Lẩu Thái', 'Lẩu hải sản']
  },
  {
    slug: 'tra-sua-tocotoco',
    name: 'Trà Sữa Tocotoco',
    cuisineTypes: ['Trà sữa', 'Đồ uống'],
    rating: 4.4,
    reviewCount: 2156,
    distance: 1.5,
    etaMinutes: 20,
    priceFloor: 35000,
    heroImage: '1556679343-c7306c1976bc',
    logoImage: '1556679343-c7306c1976bc',
    ordersThisWeek: 1342,
    badges: ['freeship' as const],
    discountText: '',
    isOpen: true,
    busyLevel: 'low' as const,
    tags: ['Trà sữa trân châu', 'Matcha']
  }
];
```

## 15. Run

```bash
cd demos/food-delivery
npm install
npm run dev
# Open http://localhost:3000
```

## 16. Anti-pattern checklist

- [x] Plus Jakarta Sans primary, không Cormorant/Fraunces
- [x] Green + coral, không cream
- [x] Real Unsplash dish photos, không Picsum random
- [x] Bento cuisines grid asymmetric
- [x] Promo countdown prominent
- [x] Restaurant card với logo + sold count + deals + ETA
- [x] Mega footer 6 col + app + payment
- [x] Trust strip với Freeship / 25 min / verified
- [x] Categories horizontal scroll
- [x] Không "make every screen feel like..."
- [x] Không em-dash
- [x] Vietnamese diacritics đầy đủ (Phở, Bún, Cơm tấm)
- [x] tabular-nums cho giá
- [x] WCAG AA contrast
- [x] Reduced-motion respected
- [x] aria-label cho icon buttons
- [x] Lazy load dưới fold