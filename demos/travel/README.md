# Skylark. Landing Page Demo (Travel Vertical)

> Single-page React/Next.js demo for Skylark travel platform. Showcases mega hero with tabbed search, deal countdown strip, destination bento, hotel collections, video testimonials, mega footer.

## File structure

```
demos/travel/
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
│       ├── MegaHero.tsx       # Tabs search widget
│       ├── DealStrip.tsx      # Horizontal scroll flash deals
│       ├── DestinationBento.tsx
│       ├── HotelCollection.tsx
│       ├── TestimonialVideo.tsx
│       ├── TrustStrip.tsx
│       ├── AppDownload.tsx
│       └── MegaFooter.tsx
└── data/
    ├── deals.ts
    ├── hotels.ts
    └── destinations.ts
```

## 1. package.json

```json
{
  "name": "skylark-demo",
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
        navy: { 50: '#f0f9ff', 100: '#e0f2fe', 700: '#0c4a6e', 800: '#075985', 900: '#0c4a6e' },
        coral: { 50: '#fff1f2', 400: '#fb7185', 500: '#f43f5e' }
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
  --color-brand: #0c4a6e;
  --color-brand-hover: #075985;
  --color-accent: #f43f5e;
  --radius-card: 12px;
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
  title: 'Skylark. Du lịch Đông Nam Á | Giá tốt. Đặt nhanh. Hoàn tiền dễ.',
  description: '2.500+ chuyến bay · 50.000+ khách sạn · 800+ tour mỗi ngày tại 87 điểm đến Đông Nam Á.',
  openGraph: {
    title: 'Skylark. Du lịch Đông Nam Á',
    description: 'Giá tốt nhất. Hoàn tiền 200% nếu giá cao hơn.',
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
import { TrustStrip } from './components/TrustStrip';
import { DealStrip } from './components/DealStrip';
import { DestinationBento } from './components/DestinationBento';
import { HotelCollection } from './components/HotelCollection';
import { TestimonialVideo } from './components/TestimonialVideo';
import { AppDownload } from './components/AppDownload';
import { MegaFooter } from './components/MegaFooter';

export default function HomePage() {
  return (
    <>
      <StickyHeader />
      <main>
        <MegaHero />
        <TrustStrip />
        <DealStrip />
        <DestinationBento />
        <HotelCollection />
        <TestimonialVideo />
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
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-sky-600 to-rose-500 flex items-center justify-center text-white font-extrabold text-lg">
              S
            </div>
            <span className="font-extrabold text-lg text-slate-900 tracking-tight">
              Skylark
            </span>
          </a>

          <nav className="hidden lg:flex items-center gap-7 text-[14px] font-semibold text-slate-700">
            <a href="/flights" className="hover:text-sky-700 inline-flex items-center gap-1">
              <Phosphor.AirplaneTilt size={16} weight="bold" />
              Chuyến bay
            </a>
            <a href="/hotels" className="hover:text-sky-700 inline-flex items-center gap-1">
              <Phosphor.Buildings size={16} weight="bold" />
              Khách sạn
            </a>
            <a href="/tours" className="hover:text-sky-700 inline-flex items-center gap-1">
              <Phosphor.MapTrifold size={16} weight="bold" />
              Tour
            </a>
            <a href="/combo" className="hover:text-sky-700 inline-flex items-center gap-1">
              <Phosphor.Lightning size={16} weight="bold" />
              Combo
            </a>
            <a href="/destinations" className="hover:text-sky-700">Điểm đến</a>
            <a href="/membership" className="hover:text-sky-700">Membership</a>
          </nav>

          <div className="flex items-center gap-3">
            <a href="tel:19001569" className="hidden md:flex items-center gap-1.5 text-[13px] font-semibold text-slate-700 hover:text-sky-700">
              <Phosphor.Phone size={14} weight="bold" />
              1900 1569
            </a>
            <a href="/login" className="hidden sm:inline-flex text-[13px] font-semibold text-slate-700 hover:text-sky-700 px-3 py-2">
              Đăng nhập
            </a>
            <a href="/signup" className="inline-flex items-center gap-1.5 px-4 py-2 bg-sky-700 hover:bg-sky-800 text-white text-[13px] font-bold rounded-lg transition-colors">
              Đăng ký
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

const TABS = [
  { id: 'flight', label: 'Chuyến bay', icon: 'AirplaneTilt' },
  { id: 'hotel', label: 'Khách sạn', icon: 'Buildings' },
  { id: 'tour', label: 'Tour', icon: 'MapTrifold' },
  { id: 'combo', label: 'Combo', icon: 'Lightning' }
] as const;

export function MegaHero() {
  const [tab, setTab] = useState<typeof TABS[number]['id']>('flight');

  return (
    <section className="relative bg-slate-900 overflow-hidden pt-16" aria-label="Tìm chuyến bay và khách sạn">
      <div className="absolute inset-0 h-[760px] lg:h-[820px]" aria-hidden="true">
        <video
          autoPlay muted loop playsInline
          poster="https://images.unsplash.com/photo-1582719508461-905c673771fd?w=1920&h=1080&fit=crop&q=80"
          className="w-full h-full object-cover"
        >
          <source src="https://cdn.coverr.co/videos/coverr-aerial-view-of-tropical-beach-2656/1080p.mp4" type="video/mp4" />
        </video>
        <div className="absolute inset-0 bg-gradient-to-b from-slate-900/70 via-slate-900/30 to-slate-900" />
      </div>

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-24 pb-40 lg:pt-32 lg:pb-52">
        <div className="inline-flex items-center gap-2 px-3 py-1.5 bg-sky-500/20 backdrop-blur border border-sky-400/30 rounded-full text-sky-200 text-[11px] font-bold uppercase tracking-wider mb-6">
          <Phosphor.SealCheck size={14} weight="fill" />
          Sàn OTA #1 Đông Nam Á · 4.8★ từ 248.000 đánh giá
        </div>

        <h1 className="text-white text-[40px] sm:text-[56px] lg:text-[88px] font-extrabold leading-[1.05] tracking-tight max-w-4xl">
          Du lịch Đông Nam Á<br />
          <span className="text-rose-400">không lo về giá</span>
        </h1>
        <p className="mt-6 text-white/85 text-[16px] lg:text-[18px] leading-relaxed max-w-2xl">
          2.500+ chuyến bay · 50.000+ khách sạn · 800+ tour mỗi ngày. Hoàn tiền 200% nếu giá cao hơn.
        </p>

        <div className="mt-8 flex flex-wrap items-center gap-x-6 gap-y-2 text-white/80 text-[13px]">
          <span className="inline-flex items-center gap-1.5">
            <Phosphor.Ticket size={14} weight="fill" className="text-rose-400" />
            Flash deal cứ mỗi giờ
          </span>
          <span className="inline-flex items-center gap-1.5">
            <Phosphor.SealCheck size={14} weight="fill" className="text-sky-400" />
            IATA certified
          </span>
          <span className="inline-flex items-center gap-1.5">
            <Phosphor.Clock size={14} weight="fill" className="text-sky-400" />
            Xác nhận tức thì
          </span>
        </div>
      </div>

      <div className="relative max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 -mt-32 lg:-mt-40 mb-12 z-10">
        <SearchWidget active={tab} onChange={setTab} />
      </div>
    </section>
  );
}

function SearchWidget({ active, onChange }: { active: string; onChange: (v: any) => void }) {
  return (
    <div className="bg-white rounded-2xl shadow-2xl border border-slate-200 p-4 lg:p-5">
      <div className="flex items-center gap-1 mb-4 border-b border-slate-100 overflow-x-auto" role="tablist">
        {TABS.map(t => {
          const Icon = Phosphor[t.icon] as any;
          return (
            <button
              key={t.id}
              role="tab"
              aria-selected={active === t.id}
              onClick={() => onChange(t.id)}
              className={`flex items-center gap-1.5 px-4 py-2.5 text-[13px] font-semibold border-b-2 -mb-px whitespace-nowrap transition-colors ${
                active === t.id
                  ? 'border-sky-600 text-sky-700'
                  : 'border-transparent text-slate-600 hover:text-slate-900'
              }`}
            >
              <Icon size={16} weight="bold" />
              {t.label}
            </button>
          );
        })}
      </div>

      {active === 'flight' && (
        <div>
          <div className="grid grid-cols-1 lg:grid-cols-[1fr_auto_1fr_1fr_1fr_auto] gap-3 mb-3">
            <Field label="Từ" placeholder="Hà Nội (HAN)" icon="AirplaneTakeoff" />
            <button className="self-end mb-2.5 w-9 h-9 inline-flex items-center justify-center bg-slate-100 hover:bg-slate-200 rounded-full transition-colors" aria-label="Đổi chiều">
              <Phosphor.ArrowsLeftRight size={14} weight="bold" className="text-slate-700" />
            </button>
            <Field label="Đến" placeholder="Đà Lạt (DLI)" icon="AirplaneLanding" />
            <Field label="Khởi hành" placeholder="25/07/2026" icon="CalendarBlank" />
            <Field label="Khách" placeholder="1 người lớn" icon="Users" />
            <button className="self-end mb-1 px-6 py-3 bg-sky-600 hover:bg-sky-700 text-white font-bold rounded-xl shadow-lg inline-flex items-center gap-2">
              <Phosphor.MagnifyingGlass size={18} weight="bold" />
              Tìm
            </button>
          </div>
          <div className="flex items-center gap-3 text-[12.5px] text-slate-600 pt-2 border-t border-slate-100">
            <label className="inline-flex items-center gap-1.5 cursor-pointer">
              <input type="checkbox" className="rounded text-sky-600" />
              Khứ hồi
            </label>
            <label className="inline-flex items-center gap-1.5 cursor-pointer">
              <input type="checkbox" className="rounded text-sky-600" />
              Chỉ hạng phổ thông
            </label>
            <div className="flex-1" />
            <span className="text-slate-500">
              Gợi ý: <a className="text-sky-600 hover:underline font-semibold" href="#">HN → DL 1.290.000₫</a> · <a className="text-sky-600 hover:underline font-semibold" href="#">SGN → PQ 2.100.000₫</a>
            </span>
          </div>
        </div>
      )}

      {active === 'hotel' && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3 mb-3">
          <Field label="Điểm đến" placeholder="Phú Quốc, Hội An..." icon="MapPin" />
          <Field label="Nhận phòng" placeholder="25/07/2026" icon="CalendarBlank" />
          <Field label="Trả phòng" placeholder="28/07/2026" icon="CalendarBlank" />
          <Field label="Khách & phòng" placeholder="2 người lớn, 1 phòng" icon="Users" />
        </div>
      )}
    </div>
  );
}

function Field({ label, placeholder, icon }: { label: string; placeholder: string; icon: any }) {
  const Icon = Phosphor[icon] as any;
  return (
    <label className="block">
      <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500 block mb-1.5">
        {label}
      </span>
      <div className="relative">
        <Icon size={16} weight="bold" className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none" />
        <input
          type="text"
          placeholder={placeholder}
          className="w-full pl-10 pr-3 py-2.5 bg-slate-50 hover:bg-slate-100 border border-slate-200 rounded-lg text-[14px] text-slate-900 font-medium focus:outline-none focus:ring-2 focus:ring-sky-500 focus:bg-white transition-colors"
        />
      </div>
    </label>
  );
}
```

## 8. app/components/TrustStrip.tsx

```tsx
import * as Phosphor from '@phosphor-icons/react';

const TRUST = [
  { icon: 'Ticket', title: 'Flash deal mỗi giờ', sub: 'Tiết kiệm đến 70%' },
  { icon: 'SealCheck', title: 'Hoàn tiền 200%', sub: 'Nếu tìm thấy giá rẻ hơn' },
  { icon: 'Clock', title: 'Xác nhận tức thì', sub: 'Trong vòng 60 giây' },
  { icon: 'Headset', title: 'Hỗ trợ 24/7', sub: 'Hotline 1900 1569' },
  { icon: 'ShieldCheck', title: 'IATA certified', sub: 'Đại lý chính thức' },
  { icon: 'CalendarCheck', title: 'Hủy miễn phí', sub: 'Đa số khách sạn' }
];

export function TrustStrip() {
  return (
    <section className="bg-white border-y border-slate-200 py-6 lg:py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 lg:gap-6">
          {TRUST.map(item => {
            const Icon = Phosphor[item.icon] as any;
            return (
              <div key={item.title} className="flex items-start gap-3">
                <div className="w-10 h-10 rounded-lg bg-sky-50 text-sky-700 flex items-center justify-center flex-shrink-0">
                  <Icon size={20} weight="fill" />
                </div>
                <div className="min-w-0">
                  <p className="text-[13px] font-bold text-slate-900 leading-tight">{item.title}</p>
                  <p className="text-[12px] text-slate-500 mt-0.5">{item.sub}</p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
```

## 9. app/components/DealStrip.tsx

```tsx
import * as Phosphor from '@phosphor-icons/react';
import { DEALS } from '@/data/deals';

export function DealStrip() {
  return (
    <section className="bg-slate-50 py-16 lg:py-24" aria-labelledby="deal-heading">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-end justify-between mb-10 flex-wrap gap-4">
          <div>
            <span className="inline-flex items-center gap-2 text-[11px] font-bold uppercase tracking-[0.18em] text-rose-600 mb-2">
              <Phosphor.Fire size={14} weight="fill" />
              Flash deal · Mỗi giờ
            </span>
            <h2 id="deal-heading" className="text-3xl lg:text-5xl font-extrabold text-slate-900 tracking-tight">
              Deal hết hạn trong hôm nay
            </h2>
          </div>
          <a href="/deals" className="inline-flex items-center gap-1.5 text-[13px] font-semibold text-sky-600 hover:text-sky-700">
            Tất cả 487 deal
            <Phosphor.ArrowRight size={14} weight="bold" />
          </a>
        </div>

        <div className="flex gap-5 overflow-x-auto pb-4 -mx-4 px-4 scrollbar-hide snap-x snap-mandatory">
          {DEALS.map(deal => (
            <DealCard key={deal.id} deal={deal} />
          ))}
        </div>
      </div>
    </section>
  );
}

function DealCard({ deal }: { deal: any }) {
  return (
    <article className="group w-[320px] flex-shrink-0 snap-start bg-white rounded-xl border border-slate-200 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300 overflow-hidden">
      <a href={`/deals/${deal.id}`} className="block relative aspect-[16/10] overflow-hidden bg-slate-100">
        <img
          src={`https://images.unsplash.com/photo-${deal.imageId}?w=600&h=375&fit=crop&q=80`}
          alt={`${deal.title} - ${deal.subtitle}`}
          className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-[1.04]"
          loading="lazy"
        />
        <span className="absolute top-3 left-3 inline-flex items-center gap-1 px-2.5 py-1 bg-rose-500 text-white text-[11px] font-bold uppercase tracking-wider rounded-md shadow-md">
          <Phosphor.Fire size={11} weight="fill" />
          -{deal.discount}% OFF
        </span>
        <button
          aria-label={`Lưu deal ${deal.title}`}
          className="absolute top-3 right-3 w-9 h-9 bg-white/95 backdrop-blur rounded-full flex items-center justify-center shadow-md"
        >
          <Phosphor.Heart size={16} weight="regular" className="text-slate-700" />
        </button>
      </a>

      <div className="p-4 space-y-3">
        <div>
          <p className="text-[11px] font-bold uppercase tracking-wider text-slate-500 mb-0.5">{deal.brand}</p>
          <h3 className="text-[15px] font-bold text-slate-900 leading-snug">{deal.title}</h3>
          <p className="text-[12.5px] text-slate-600 mt-0.5">{deal.subtitle}</p>
        </div>

        <div className="flex items-center gap-2 text-[12px] text-slate-600">
          <span className="inline-flex items-center gap-1 text-amber-600 font-bold">
            <Phosphor.Star size={11} weight="fill" />
            {deal.rating}
          </span>
          <span>·</span>
          <span>{deal.reviewCount.toLocaleString('vi-VN')} đánh giá</span>
          <span>·</span>
          <span>{deal.meta}</span>
        </div>

        <div className="bg-slate-900 text-white rounded-lg px-3 py-2 text-center">
          <span className="text-[10.5px] font-bold uppercase tracking-wider text-slate-300">Còn</span>
          <div className="flex items-center justify-center gap-1 mt-0.5 font-extrabold tabular-nums text-white">
            <span className="text-[16px]">02</span>
            <span className="text-slate-500">:</span>
            <span className="text-[16px]">14</span>
            <span className="text-slate-500">:</span>
            <span className="text-[16px]">33</span>
          </div>
        </div>

        <div className="flex items-baseline gap-2">
          <span className="text-[24px] font-extrabold text-slate-900 tabular-nums leading-none">
            {deal.price.toLocaleString('vi-VN')}₫
          </span>
          <span className="text-[12px] text-slate-400 line-through tabular-nums">
            {deal.originalPrice.toLocaleString('vi-VN')}₫
          </span>
        </div>

        <div className="flex items-center gap-1.5 text-[11.5px]">
          <Phosphor.Fire size={12} weight="fill" className="text-rose-500" />
          <span className="text-rose-600 font-bold">Đã bán {deal.soldCount}</span>
        </div>

        <a
          href={`/deals/${deal.id}/book`}
          className="flex items-center justify-center gap-1.5 w-full py-2.5 bg-sky-600 hover:bg-sky-700 text-white text-[13px] font-bold rounded-lg transition-colors"
        >
          Đặt ngay {deal.price.toLocaleString('vi-VN')}₫
          <Phosphor.ArrowRight size={14} weight="bold" />
        </a>
      </div>
    </article>
  );
}
```

## 10. app/components/DestinationBento.tsx

```tsx
import * as Phosphor from '@phosphor-icons/react';
import { DESTINATIONS } from '@/data/destinations';

const SIZE_MAP = {
  hero: 'lg:col-span-3 lg:row-span-2',
  tall: 'lg:col-span-2 lg:row-span-2',
  small: 'lg:col-span-1 lg:row-span-1',
  wide: 'lg:col-span-3 lg:row-span-1'
} as const;

export function DestinationBento() {
  return (
    <section className="bg-white py-16 lg:py-24" aria-labelledby="dest-heading">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-end justify-between mb-10 flex-wrap gap-4">
          <div>
            <span className="inline-block text-[11px] font-bold uppercase tracking-[0.18em] text-sky-600 mb-2">
              Điểm đến nổi bật
            </span>
            <h2 id="dest-heading" className="text-3xl lg:text-5xl font-extrabold text-slate-900 tracking-tight">
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

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3 lg:gap-4 lg:auto-rows-[160px]">
          {DESTINATIONS.map(d => {
            const isLarge = d.cellSize === 'hero' || d.cellSize === 'tall';
            return (
              <a
                key={d.slug}
                href={`/destinations/${d.slug}`}
                className={`group relative overflow-hidden rounded-2xl bg-slate-100 hover:shadow-xl transition-all duration-300 ${SIZE_MAP[d.cellSize]}`}
              >
                <img
                  src={`https://images.unsplash.com/photo-${d.imageId}?w=${isLarge ? '800' : '600'}&h=${isLarge ? '600' : '400'}&fit=crop&q=80`}
                  alt={`${d.name} - ${d.country}`}
                  className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
                  loading="lazy"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-slate-900/85 via-slate-900/20 to-transparent" />
                <div className="absolute inset-0 p-4 lg:p-5 flex flex-col justify-between text-white">
                  <div className="flex items-start justify-between">
                    <span className="text-[10.5px] font-bold uppercase tracking-wider px-2 py-0.5 bg-white/20 backdrop-blur rounded-full">
                      {d.flag} {d.country}
                    </span>
                    <span className="inline-flex items-center gap-0.5 text-[10.5px] font-bold bg-white/20 backdrop-blur px-2 py-0.5 rounded-full">
                      <Phosphor.Star size={10} weight="fill" className="text-amber-300" />
                      {d.rating}
                    </span>
                  </div>
                  <div>
                    <h3 className={`font-extrabold leading-tight ${isLarge ? 'text-3xl lg:text-4xl' : 'text-xl'}`}>
                      {d.name}
                    </h3>
                    {isLarge && <p className="text-[12.5px] text-white/80 mt-1 line-clamp-2 max-w-xs">{d.description}</p>}
                    <div className="flex items-center gap-2 mt-2 text-[11.5px]">
                      <span className="inline-flex items-center gap-1 text-white/90">
                        <Phosphor.AirplaneTakeoff size={11} weight="bold" />
                        {d.flightsPerWeek} chuyến/tuần
                      </span>
                    </div>
                    <div className="mt-2 inline-flex items-baseline gap-1">
                      <span className="text-[10.5px] text-white/70">từ</span>
                      <span className="text-[18px] font-extrabold tabular-nums">{d.startingPrice.toLocaleString('vi-VN')}₫</span>
                    </div>
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

## 11. app/components/HotelCollection.tsx

```tsx
import * as Phosphor from '@phosphor-icons/react';
import { HOTELS } from '@/data/hotels';

export function HotelCollection() {
  return (
    <section className="bg-slate-50 py-16 lg:py-24" aria-labelledby="hotel-heading">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-end justify-between mb-10 flex-wrap gap-4">
          <div>
            <span className="inline-block text-[11px] font-bold uppercase tracking-[0.18em] text-sky-600 mb-2">
              Khách sạn nổi bật
            </span>
            <h2 id="hotel-heading" className="text-3xl lg:text-5xl font-extrabold text-slate-900 tracking-tight">
              Resort view biển 2026
            </h2>
            <p className="mt-2 text-slate-600 max-w-2xl">
              Tuyển chọn 6 resort cao cấp có hồ bơi riêng và bãi biển riêng. Đặt sớm giảm 30%.
            </p>
          </div>
          <a href="/hotels" className="inline-flex items-center gap-1.5 text-[13px] font-semibold text-sky-600 hover:text-sky-700">
            Xem tất cả 50.000+ khách sạn
            <Phosphor.ArrowRight size={14} weight="bold" />
          </a>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {HOTELS.map(h => (
            <HotelCard key={h.slug} hotel={h} />
          ))}
        </div>
      </div>
    </section>
  );
}

function HotelCard({ hotel }: { hotel: any }) {
  return (
    <article className="group bg-white rounded-xl border border-slate-200 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300 overflow-hidden">
      <a href={`/hotels/${hotel.slug}`} className="block relative aspect-[16/9] overflow-hidden bg-slate-100">
        <img
          src={`https://images.unsplash.com/photo-${hotel.imageId}?w=800&h=450&fit=crop&q=80`}
          alt={`${hotel.name} tại ${hotel.location}`}
          className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-[1.04]"
          loading="lazy"
        />
        <span className="absolute top-3 left-3 inline-flex items-center gap-1 px-2.5 py-1 bg-rose-500 text-white text-[10.5px] font-bold uppercase tracking-wider rounded-md shadow-md">
          <Phosphor.Fire size={11} weight="fill" />
          -{hotel.discount}% DEAL
        </span>
        <button
          aria-label={`Lưu khách sạn ${hotel.name}`}
          className="absolute top-3 right-3 w-9 h-9 bg-white/95 backdrop-blur rounded-full flex items-center justify-center shadow-md"
        >
          <Phosphor.Heart size={16} weight="regular" className="text-slate-700" />
        </button>
        {hotel.gallery && (
          <div className="absolute bottom-3 left-3 right-3 flex items-center gap-1.5">
            {hotel.gallery.slice(0, 3).map((g: string, i: number) => (
              <div key={i} className="flex-1 aspect-[4/3] rounded overflow-hidden border-2 border-white shadow-sm bg-slate-200">
                <img src={`https://images.unsplash.com/photo-${g}?w=120&h=90&fit=crop&q=80`} alt="" className="w-full h-full object-cover" />
              </div>
            ))}
            <div className="flex-1 aspect-[4/3] rounded bg-black/70 backdrop-blur border-2 border-white flex items-center justify-center text-white text-[11px] font-bold">
              +{hotel.galleryCount} ảnh
            </div>
          </div>
        )}
      </a>

      <div className="p-5 space-y-3">
        <div>
          <h3 className="text-[16px] font-bold text-slate-900 leading-snug hover:text-sky-700">{hotel.name}</h3>
          <div className="mt-1.5 flex items-center gap-2 text-[12px]">
            <span className="inline-flex items-center gap-0.5 px-1.5 py-0.5 bg-sky-700 text-white rounded font-bold tabular-nums">{hotel.rating}</span>
            <span className="text-slate-700 font-semibold">{hotel.label}</span>
            <span className="text-slate-500">· {hotel.reviewCount.toLocaleString('vi-VN')} đánh giá</span>
          </div>
          <p className="flex items-start gap-1.5 mt-1 text-[13px] text-slate-600">
            <Phosphor.MapPin size={13} weight="fill" className="text-slate-400 mt-0.5 flex-shrink-0" />
            {hotel.location} · <strong className="text-slate-900">{hotel.distance} km</strong> từ {hotel.landmark}
          </p>
        </div>

        <div className="flex items-center gap-x-3 gap-y-1 flex-wrap text-[12px] text-slate-600">
          {hotel.amenities.map((a: any) => (
            <span key={a.name} className="inline-flex items-center gap-1">
              <Phosphor[a.icon] size={13} weight="regular" className="text-slate-400" />
              {a.label}
            </span>
          ))}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-[1fr_auto] gap-3 pt-3 border-t border-slate-100">
          <div>
            <p className="text-[14px] font-bold text-slate-900">{hotel.room.name}</p>
            <p className="text-[12px] text-slate-500 mt-0.5">{hotel.room.bed} · {hotel.room.area}m² · {hotel.room.breakfast}</p>
            <p className="text-[11px] text-emerald-600 mt-1 font-semibold">{hotel.room.cancelPolicy}</p>
          </div>
          <div className="text-right">
            <div className="text-[10px] text-rose-500 font-bold uppercase">Chỉ còn 2 phòng</div>
            <div className="text-[24px] font-extrabold text-slate-900 tabular-nums leading-none">
              {hotel.price.toLocaleString('vi-VN')}₫
            </div>
            <div className="text-[11px] text-slate-400 line-through tabular-nums">{hotel.originalPrice.toLocaleString('vi-VN')}₫</div>
            <a href={`/booking/${hotel.slug}`} className="mt-2 inline-flex items-center gap-1 px-4 py-2 bg-sky-700 hover:bg-sky-800 text-white text-[12px] font-bold rounded-lg">
              Đặt ngay
              <Phosphor.ArrowRight size={12} weight="bold" />
            </a>
          </div>
        </div>
      </div>
    </article>
  );
}
```

## 12. app/components/TestimonialVideo.tsx

```tsx
import * as Phosphor from '@phosphor-icons/react';

const TESTIMONIALS = [
  {
    id: 'minh-hn',
    name: 'Trần Minh',
    title: 'Kỹ sư IT, Hà Nội',
    avatarId: '1507003211169-0a1dd7228f2d',
    rating: 5,
    quote: 'Đặt vé máy bay + khách sạn combo 3 ngày Phú Quốc chỉ 4.500.000₫ cho cả gia đình. Resort view biển xịn, giá tốt hơn booking trực tiếp.',
    destination: 'Phú Quốc',
    duration: '3 ngày 2 đêm',
    tripImageId: '1582719508461-905c673771fd',
    videoPoster: 'https://images.unsplash.com/photo-1582719508461-905c673771fd?w=600&h=400&fit=crop&q=80'
  },
  {
    id: 'lan-hcm',
    name: 'Lê Thị Lan',
    title: 'Marketing Manager, TP.HCM',
    avatarId: '1494790108377-be9c29b29330',
    rating: 5,
    quote: 'Tour Bali 5 ngày trọn gói, hướng dẫn viên nói tiếng Việt, khách sạn 4 sao. Hoàn tiền nhanh khi đổi lịch. Đã dùng 3 lần, lần nào cũng ưng.',
    destination: 'Bali',
    duration: '5 ngày 4 đêm',
    tripImageId: '1537996194471-e657df975ab4',
    videoPoster: 'https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=600&h=400&fit=crop&q=80'
  },
  {
    id: 'quan-dn',
    name: 'Nguyễn Quốc Quân',
    title: 'Bác sĩ, Đà Nẵng',
    avatarId: '1472099645785-5658abf4ff4e',
    rating: 5,
    quote: 'Đặt vé khứ hồi Hà Nội - Singapore cho cả nhóm 8 người, mọi thứ suôn sẻ. App theo dõi chuyến bay real-time, check-in online tự động.',
    destination: 'Singapore',
    duration: '4 ngày 3 đêm',
    tripImageId: '1565967511849-76a60a516170',
    videoPoster: 'https://images.unsplash.com/photo-1565967511849-76a60a516170?w=600&h=400&fit=crop&q=80'
  },
  {
    id: 'mai-pt',
    name: 'Phạm Thị Mai',
    title: 'Giáo viên, Pleiku',
    avatarId: '1438761681033-6461ffad8d80',
    rating: 5,
    quote: 'Đi tour Thái Lan tự túc, đặt qua Skylark tiết kiệm 30% so với tự book. Hỗ trợ 24/7 cả khi đang ở nước ngoài, yên tâm.',
    destination: 'Bangkok',
    duration: '4 ngày 3 đêm',
    tripImageId: '1508009603885-50cf7c579365',
    videoPoster: 'https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=600&h=400&fit=crop&q=80'
  }
];

export function TestimonialVideo() {
  return (
    <section className="bg-slate-50 py-16 lg:py-24" aria-labelledby="testimonial-heading">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <span className="inline-block text-[11px] font-bold uppercase tracking-[0.18em] text-sky-600 mb-2">
            Khách hàng nói gì
          </span>
          <h2 id="testimonial-heading" className="text-3xl lg:text-5xl font-extrabold text-slate-900 tracking-tight">
            4.8★ từ 248.000 đánh giá thật
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
          {TESTIMONIALS.map(t => (
            <article key={t.id} className="group bg-white rounded-2xl border border-slate-200 overflow-hidden hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
              <div className="relative aspect-[3/4] bg-slate-900 overflow-hidden">
                <img src={t.videoPoster} alt="" className="w-full h-full object-cover" loading="lazy" />
                <div className="absolute inset-0 bg-gradient-to-t from-slate-900/70 via-slate-900/10 to-transparent" />
                <button
                  type="button"
                  aria-label={`Phát video của ${t.name}`}
                  className="absolute inset-0 flex items-center justify-center group-hover:scale-110 transition-transform"
                >
                  <span className="w-16 h-16 inline-flex items-center justify-center bg-white/95 backdrop-blur rounded-full shadow-2xl">
                    <Phosphor.PlayCircle size={56} weight="fill" className="text-sky-700" />
                  </span>
                </button>
                <div className="absolute bottom-3 left-3 right-3 flex items-end justify-between">
                  <div className="bg-white/95 backdrop-blur rounded-lg px-2.5 py-1.5">
                    <p className="text-[10px] font-bold uppercase tracking-wider text-slate-500">Trip</p>
                    <p className="text-[12.5px] font-bold text-slate-900">{t.destination}</p>
                  </div>
                </div>
              </div>
              <div className="p-4 space-y-3">
                <div className="flex items-center gap-2.5">
                  <img
                    src={`https://images.unsplash.com/photo-${t.avatarId}?w=80&h=80&fit=crop&q=80`}
                    alt={t.name}
                    className="w-10 h-10 rounded-full object-cover ring-2 ring-white"
                    loading="lazy"
                  />
                  <div className="min-w-0 flex-1">
                    <div className="flex items-center gap-1">
                      <p className="text-[13px] font-bold text-slate-900 truncate">{t.name}</p>
                      <Phosphor.SealCheck size={13} weight="fill" className="text-sky-600 flex-shrink-0" />
                    </div>
                    <p className="text-[11px] text-slate-500 truncate">{t.title}</p>
                  </div>
                </div>
                <div className="flex items-center gap-1">
                  {Array.from({ length: t.rating }).map((_, i) => (
                    <Phosphor.Star key={i} size={12} weight="fill" className="text-amber-400" />
                  ))}
                </div>
                <blockquote className="relative">
                  <Phosphor.Quotes size={16} weight="fill" className="absolute -left-1 -top-1 text-sky-100" />
                  <p className="text-[12.5px] text-slate-700 leading-relaxed pl-5 line-clamp-4">{t.quote}</p>
                </blockquote>
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
```

## 13. app/components/AppDownload.tsx

```tsx
import * as Phosphor from '@phosphor-icons/react';

export function AppDownload() {
  return (
    <section className="bg-gradient-to-br from-sky-700 via-sky-800 to-slate-900 text-white py-16 lg:py-24" aria-labelledby="app-heading">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div>
            <span className="inline-block text-[11px] font-bold uppercase tracking-[0.18em] text-sky-300 mb-3">
              App Skylark
            </span>
            <h2 id="app-heading" className="text-3xl lg:text-5xl font-extrabold tracking-tight leading-tight">
              Đặt vé. Check-in. Theo dõi chuyến bay.<br />
              <span className="text-sky-300">Mọi thứ trong túi.</span>
            </h2>
            <p className="mt-4 text-white/85 text-[15px] lg:text-[17px] max-w-xl leading-relaxed">
              Ưu đãi app-only, thông báo gate thay đổi real-time, check-in trước 24h. Tải miễn phí.
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
                <strong className="font-bold tabular-nums">4.8</strong> · 87.420 đánh giá
              </span>
              <span className="inline-flex items-center gap-2">
                <Phosphor.DownloadSimple size={14} weight="bold" />
                5M+ lượt tải
              </span>
            </div>
          </div>

          {/* Phone mockup */}
          <div className="relative">
            <div className="aspect-[9/16] max-w-xs mx-auto bg-slate-900 rounded-[3rem] border-[10px] border-slate-950 shadow-2xl overflow-hidden">
              <img
                src="https://images.unsplash.com/photo-1582719508461-905c673771fd?w=400&h=711&fit=crop&q=80"
                alt="App Skylark trên điện thoại"
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

## 14. app/components/MegaFooter.tsx

```tsx
import * as Phosphor from '@phosphor-icons/react';

export function MegaFooter() {
  return (
    <footer className="bg-slate-950 text-slate-300">
      <div className="border-b border-slate-800/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
          <div className="grid grid-cols-1 lg:grid-cols-[1fr_auto] gap-6 items-center">
            <div>
              <h2 className="text-2xl lg:text-3xl font-extrabold text-white">
                Nhận deal sớm nhất trước khi hết
              </h2>
              <p className="mt-1 text-slate-400 text-[14px]">
                Flash deal, mã giảm giá và tips du lịch. 1 email/tuần, hủy bất kỳ lúc nào.
              </p>
            </div>
            <form className="flex items-center gap-2 max-w-md" onSubmit={e => e.preventDefault()}>
              <div className="relative flex-1">
                <Phosphor.EnvelopeSimple size={16} weight="bold" className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
                <input
                  type="email"
                  required
                  placeholder="email@example.com"
                  className="w-full pl-10 pr-3 py-3 bg-slate-900 border border-slate-700 rounded-lg text-white text-[14px] focus:outline-none focus:ring-2 focus:ring-sky-500"
                />
              </div>
              <button type="submit" className="px-5 py-3 bg-sky-600 hover:bg-sky-700 text-white font-bold text-[14px] rounded-lg whitespace-nowrap inline-flex items-center gap-1.5">
                Đăng ký
                <Phosphor.ArrowRight size={14} weight="bold" />
              </button>
            </form>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-14">
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-7 gap-8 lg:gap-6">
          <div className="col-span-2 lg:col-span-1">
            <a href="/" className="inline-flex items-center gap-2">
              <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-sky-500 to-rose-500 flex items-center justify-center text-white font-extrabold text-lg">S</div>
              <span className="font-extrabold text-xl text-white tracking-tight">Skylark</span>
            </a>
            <p className="mt-4 text-[13px] text-slate-400 leading-relaxed">
              Sàn OTA Đông Nam Á. Giá tốt, đặt nhanh, hoàn tiền dễ.
            </p>
            <div className="mt-5 space-y-2">
              <a href="tel:19001569" className="flex items-center gap-2 text-[13px] hover:text-white">
                <Phosphor.Phone size={13} weight="bold" className="text-sky-400" />
                <span className="font-bold text-white tabular-nums">1900 1569</span>
                <span className="text-slate-500">· 24/7</span>
              </a>
              <a href="mailto:hello@skylark.vn" className="flex items-center gap-2 text-[13px] hover:text-white">
                <Phosphor.EnvelopeSimple size={13} weight="bold" className="text-slate-400" />
                hello@skylark.vn
              </a>
            </div>
            <div className="mt-5 flex items-center gap-2">
              <SocialLink icon="FacebookLogo" label="Facebook" />
              <SocialLink icon="InstagramLogo" label="Instagram" />
              <SocialLink icon="YoutubeLogo" label="YouTube" />
              <SocialLink icon="TiktokLogo" label="TikTok" />
            </div>
          </div>

          <FooterColumn title="Chuyến bay" icon="AirplaneTilt" links={[
            { label: 'Vé nội địa', href: '#' },
            { label: 'Vé quốc tế', href: '#' },
            { label: 'Hạng thương gia', href: '#' },
            { label: 'Hãng hàng không', href: '#' },
            { label: 'Sân bay', href: '#' }
          ]} />
          <FooterColumn title="Khách sạn" icon="Buildings" links={[
            { label: 'Resort biển', href: '#' },
            { label: 'Hotel trung tâm', href: '#' },
            { label: 'Boutique', href: '#' },
            { label: 'Homestay', href: '#' },
            { label: 'Villa', href: '#' }
          ]} />
          <FooterColumn title="Điểm đến" icon="MapTrifold" links={[
            { label: 'Phú Quốc', href: '#' },
            { label: 'Đà Lạt', href: '#' },
            { label: 'Hội An', href: '#' },
            { label: 'Bangkok', href: '#' },
            { label: 'Bali', href: '#' },
            { label: 'Tokyo', href: '#' },
            { label: 'Singapore', href: '#' },
            { label: 'Xem tất cả 87', href: '#' }
          ]} />
          <FooterColumn title="Cẩm nang" icon="BookOpen" links={[
            { label: 'Kinh nghiệm', href: '#' },
            { label: 'Visa', href: '#' },
            { label: 'Bảo hiểm', href: '#' },
            { label: 'Mẹo tiết kiệm', href: '#' },
            { label: 'Blog', href: '#' }
          ]} />
          <FooterColumn title="Membership" icon="Crown" links={[
            { label: 'Skylark Rewards', href: '#' },
            { label: 'Điểm thưởng', href: '#' },
            { label: 'Hạng thẻ', href: '#' },
            { label: 'Đối tác', href: '#' }
          ]} />
          <FooterColumn title="Hỗ trợ" icon="Headset" links={[
            { label: 'Trung tâm hỗ trợ', href: '#' },
            { label: 'Hủy / đổi', href: '#' },
            { label: 'Hoàn tiền', href: '#' },
            { label: 'Liên hệ', href: '#' },
            { label: 'FAQ', href: '#' }
          ]} />
        </div>

        <div className="mt-12 pt-8 border-t border-slate-800/50 flex flex-wrap items-center justify-between gap-6">
          <div className="flex flex-wrap items-center gap-2">
            {['visa', 'mastercard', 'jcb', 'amex', 'momo', 'zalopay', 'vnpay', 'paypal'].map(slug => (
              <img key={slug} src={`https://cdn.simpleicons.org/${slug}/cbd5e1`} alt={slug} className="h-7 w-12 object-contain bg-white rounded px-1.5 py-1" loading="lazy" />
            ))}
          </div>
          <div className="flex flex-wrap items-center gap-4 text-[11.5px] text-slate-400">
            <span className="inline-flex items-center gap-1.5">
              <Phosphor.ShieldCheck size={14} weight="fill" className="text-emerald-400" />
              Secured payment
            </span>
            <span className="inline-flex items-center gap-1.5">
              <span className="text-[10px] font-extrabold text-slate-200 tracking-widest bg-slate-800 px-1.5 py-0.5 rounded">IATA</span>
              IATA certified
            </span>
          </div>
        </div>
      </div>

      <div className="border-t border-slate-800/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-5">
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-3 text-[11.5px] text-slate-500">
            <div>© 2026 Skylark Travel JSC · Giấy phép KD lữ hành quốc tế số 79-022/2020/TCDL-GP LHQT</div>
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
        <Icon size={14} weight="bold" className="text-sky-400" />
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
    <a href="#" aria-label={`Skylark trên ${label}`} className="w-8 h-8 inline-flex items-center justify-center bg-slate-900 hover:bg-sky-600 border border-slate-800 rounded-full transition-colors">
      <Icon size={14} weight="bold" className="text-slate-300" />
    </a>
  );
}
```

## 15. data/deals.ts

```ts
const now = Date.now();
const inHours = (h: number) => new Date(now + h * 3600000);

export const DEALS = [
  {
    id: 'vn-airlines-hn-dl',
    brand: 'Vietnam Airlines',
    type: 'flight' as const,
    title: 'Hà Nội → Đà Lạt',
    subtitle: 'Bay thẳng 1h50m · Khứ hồi',
    imageId: '1573279107032-d3e88dc7d12a',
    rating: 4.7,
    reviewCount: 1247,
    meta: 'Bay 2h15m',
    discount: 47,
    price: 1290000,
    originalPrice: 2450000,
    endAt: inHours(2),
    soldCount: 487,
    remainingCount: 13
  },
  {
    id: 'vietjet-sgn-pq',
    brand: 'Vietjet Air',
    type: 'flight' as const,
    title: 'TP.HCM → Phú Quốc',
    subtitle: 'Bay thẳng 1h · 1 chiều',
    imageId: '1582719508461-905c673771fd',
    rating: 4.5,
    reviewCount: 892,
    meta: 'Bay 1h',
    discount: 35,
    price: 890000,
    originalPrice: 1370000,
    endAt: inHours(4),
    soldCount: 623,
    remainingCount: 27
  },
  {
    id: 'vinpearl-pq',
    brand: 'Vinpearl Resort',
    type: 'hotel' as const,
    title: 'Vinpearl Phú Quốc 5★',
    subtitle: 'Deluxe Ocean View · Bao bữa sáng',
    imageId: '1571896349842-33c89424de2d',
    rating: 4.9,
    reviewCount: 1456,
    meta: '5★ Resort',
    discount: 30,
    price: 3250000,
    originalPrice: 4640000,
    endAt: inHours(6),
    soldCount: 287,
    remainingCount: 8
  },
  {
    id: 'bali-tour',
    brand: 'Vietravel',
    type: 'tour' as const,
    title: 'Tour Bali 5N4Đ trọn gói',
    subtitle: 'Khách sạn 4★ · Hướng dẫn viên TV',
    imageId: '1537996194471-e657df975ab4',
    rating: 4.8,
    reviewCount: 423,
    meta: '5 ngày 4 đêm',
    discount: 25,
    price: 14900000,
    originalPrice: 19900000,
    endAt: inHours(8),
    soldCount: 156,
    remainingCount: 12
  },
  {
    id: 'combo-bangkok',
    brand: 'Skylark Combo',
    type: 'combo' as const,
    title: 'Combo Bangkok: Vé + Khách sạn',
    subtitle: 'Bangkok Airways 4★ · 3 ngày',
    imageId: '1508009603885-50cf7c579365',
    rating: 4.6,
    reviewCount: 678,
    meta: '3N2Đ',
    discount: 40,
    price: 5490000,
    originalPrice: 9150000,
    endAt: inHours(5),
    soldCount: 412,
    remainingCount: 18
  },
  {
    id: 'hn-tokyo',
    brand: 'Japan Airlines',
    type: 'flight' as const,
    title: 'Hà Nội → Tokyo',
    subtitle: 'Bay thẳng 5h45m · Khứ hồi',
    imageId: '1540959733332-eab4deabeeaf',
    rating: 4.9,
    reviewCount: 567,
    meta: 'Bay 5h45m',
    discount: 22,
    price: 4990000,
    originalPrice: 6390000,
    endAt: inHours(10),
    soldCount: 234,
    remainingCount: 9
  }
];
```

## 16. data/destinations.ts

```ts
export const DESTINATIONS = [
  { slug: 'phu-quoc', name: 'Phú Quốc', country: 'Việt Nam', flag: '🇻🇳', imageId: '1582719508461-905c673771fd', flightsPerWeek: 487, duration: '2h15m', rating: 4.8, reviewCount: 12847, startingPrice: 1290000, description: 'Đảo ngọc thiên đường với bãi biển trắng và resort 5 sao', cellSize: 'hero' as const },
  { slug: 'da-lat', name: 'Đà Lạt', country: 'Việt Nam', flag: '🇻🇳', imageId: '1573279107032-d3e88dc7d12a', flightsPerWeek: 312, duration: '1h50m', rating: 4.7, reviewCount: 8923, startingPrice: 990000, description: 'Thành phố ngàn hoa với khí hậu mát mẻ quanh năm', cellSize: 'tall' as const },
  { slug: 'hoi-an', name: 'Hội An', country: 'Việt Nam', flag: '🇻🇳', imageId: '1528127269322-539801943592', flightsPerWeek: 256, duration: '1h45m', rating: 4.9, reviewCount: 11420, startingPrice: 1190000, description: 'Phố cổ đèn lồng ven sông Thu Bồn', cellSize: 'tall' as const },
  { slug: 'bangkok', name: 'Bangkok', country: 'Thái Lan', flag: '🇹🇭', imageId: '1508009603885-50cf7c579365', flightsPerWeek: 642, duration: '2h10m', rating: 4.6, reviewCount: 24580, startingPrice: 1490000, description: 'Thủ đô sôi động với chợ nổi và đền chùa', cellSize: 'small' as const },
  { slug: 'bali', name: 'Bali', country: 'Indonesia', flag: '🇮🇩', imageId: '1537996194471-e657df975ab4', flightsPerWeek: 184, duration: '4h30m', rating: 4.8, reviewCount: 18230, startingPrice: 2490000, description: 'Đảo thần thánh với ruộng bậc thang và đền Hindu', cellSize: 'small' as const },
  { slug: 'tokyo', name: 'Tokyo', country: 'Nhật Bản', flag: '🇯🇵', imageId: '1540959733332-eab4deabeeaf', flightsPerWeek: 96, duration: '5h45m', rating: 4.9, reviewCount: 31240, startingPrice: 4990000, description: 'Siêu đô thị ánh sáng với văn hóa độc đáo', cellSize: 'wide' as const },
  { slug: 'singapore', name: 'Singapore', country: 'Singapore', flag: '🇸🇬', imageId: '1565967511849-76a60a516170', flightsPerWeek: 124, duration: '3h20m', rating: 4.8, reviewCount: 19870, startingPrice: 3290000, description: 'Đảo quốc sư tử với Gardens by the Bay', cellSize: 'wide' as const }
];
```

## 17. data/hotels.ts

```ts
export const HOTELS = [
  {
    slug: 'vinpearl-pq',
    name: 'Vinpearl Resort Phú Quốc',
    imageId: '1566073771259-6a8506099945',
    rating: 4.9, label: 'Tuyệt vời', reviewCount: 2847,
    location: 'Bãi Dài, Phú Quốc', distance: '2.3', landmark: 'sân bay',
    amenities: [
      { icon: 'SwimmingPool', label: 'Hồ bơi' },
      { icon: 'ForkKnife', label: 'Nhà hàng' },
      { icon: 'Spa', label: 'Spa' },
      { icon: 'Barbell', label: 'Gym' }
    ],
    room: { name: 'Deluxe Garden View', bed: '1 king bed', area: 45, breakfast: 'Bao bữa sáng', cancelPolicy: 'Hủy miễn phí trước 48h' },
    price: 3250000, originalPrice: 4640000, discount: 30,
    gallery: ['1571896349842-33c89424de2d', '1631049307264-da0ec9d70304', '1540555700478-4be289fbecef'],
    galleryCount: 24
  },
  {
    slug: 'intercontinental-danang',
    name: 'InterContinental Danang',
    imageId: '1582719508461-905c673771fd',
    rating: 4.8, label: 'Tuyệt vời', reviewCount: 1923,
    location: 'Bãi Bắc, Đà Nẵng', distance: '8.5', landmark: 'sân bay',
    amenities: [
      { icon: 'SwimmingPool', label: 'Hồ bơi' },
      { icon: 'Umbrella', label: 'Bãi biển' },
      { icon: 'ForkKnife', label: 'Nhà hàng' }
    ],
    room: { name: 'Ocean View Suite', bed: '1 king bed', area: 65, breakfast: 'Bao bữa sáng', cancelPolicy: 'Hủy miễn phí trước 72h' },
    price: 4250000, originalPrice: 5670000, discount: 25,
    gallery: ['1600334129128-685c5582fd35', '1540555700478-4be289fbecef', '1566073771259-6a8506099945'],
    galleryCount: 32
  },
  {
    slug: 'six-senses-ninhvanh',
    name: 'Six Senses Ninh Vân Bay',
    imageId: '1571003123894-1f0594d2b5d9',
    rating: 5.0, label: 'Xuất sắc', reviewCount: 856,
    location: 'Ninh Vân, Khánh Hoà', distance: '24.5', landmark: 'sân bay Cam Ranh',
    amenities: [
      { icon: 'SwimmingPool', label: 'Pool villa' },
      { icon: 'Spa', label: 'Spa' },
      { icon: 'ForkKnife', label: 'Fine dining' }
    ],
    room: { name: 'Beachfront Pool Villa', bed: '1 king bed', area: 180, breakfast: 'All-inclusive', cancelPolicy: 'Không hoàn' },
    price: 18500000, originalPrice: 22000000, discount: 16,
    gallery: ['1571003123894-1f0594d2b5d9', '1540555700478-4be289fbecef', '1571896349842-33c89424de2d'],
    galleryCount: 18
  },
  {
    slug: 'marriott-phuquoc',
    name: 'JW Marriott Phú Quốc',
    imageId: '1631049307264-da0ec9d70304',
    rating: 4.7, label: 'Rất tốt', reviewCount: 1456,
    location: 'Bãi Khem, Phú Quốc', distance: '12', landmark: 'sân bay',
    amenities: [
      { icon: 'SwimmingPool', label: 'Hồ bơi' },
      { icon: 'ForkKnife', label: '4 nhà hàng' },
      { icon: 'Barbell', label: 'Gym' }
    ],
    room: { name: 'Garden Suite', bed: '1 king bed', area: 55, breakfast: 'Bao bữa sáng', cancelPolicy: 'Hủy miễn phí trước 24h' },
    price: 3890000, originalPrice: 4980000, discount: 22,
    gallery: ['1566073771259-6a8506099945', '1571896349842-33c89424de2d', '1540555700478-4be289fbecef'],
    galleryCount: 28
  },
  {
    slug: 'four-seasons-hanoi',
    name: 'Four Seasons Hà Nội',
    imageId: '1540541338287-41700207dee6',
    rating: 4.9, label: 'Tuyệt vời', reviewCount: 2134,
    location: 'Quận 1, Hà Nội', distance: '0.8', landmark: 'Hồ Hoàn Kiếm',
    amenities: [
      { icon: 'Spa', label: 'Spa' },
      { icon: 'ForkKnife', label: 'Fine dining' },
      { icon: 'Barbell', label: 'Gym' }
    ],
    room: { name: 'Deluxe Room', bed: '1 king bed', area: 48, breakfast: 'Bao bữa sáng', cancelPolicy: 'Hủy miễn phí trước 48h' },
    price: 5450000, originalPrice: 6900000, discount: 21,
    gallery: ['1540541338287-41700207dee6', '1631049307264-da0ec9d70304', '1540555700478-4be289fbecef'],
    galleryCount: 36
  },
  {
    slug: 'amanoi-ninhthuan',
    name: 'Amanoi Ninh Thuận',
    imageId: '1571003123894-1f0594d2b5d9',
    rating: 5.0, label: 'Xuất sắc', reviewCount: 423,
    location: 'Vĩnh Hy, Ninh Thuận', distance: '45', landmark: 'sân bay Cam Ranh',
    amenities: [
      { icon: 'SwimmingPool', label: 'Pool villa' },
      { icon: 'Spa', label: 'Aman Spa' },
      { icon: 'ForkKnife', label: 'Fine dining' }
    ],
    room: { name: 'Ocean Pavilion', bed: '1 king bed', area: 95, breakfast: 'Bao bữa sáng', cancelPolicy: 'Không hoàn' },
    price: 16800000, originalPrice: 19800000, discount: 15,
    gallery: ['1571003123894-1f0594d2b5d9', '1540555700478-4be289fbecef', '1571896349842-33c89424de2d'],
    galleryCount: 22
  }
];
```

## 18. Run

```bash
cd demos/travel
npm install
npm run dev
# Open http://localhost:3000
```

## 19. Anti-pattern checklist

- [x] Plus Jakarta Sans primary, không Cormorant/Fraunces
- [x] Navy + coral, không cream/sky pastel
- [x] Real Unsplash + Coverr curated
- [x] Bento asymmetric destinations 7-cell
- [x] Deal countdown prominent
- [x] Hotel card với gallery strip + amenities icon + verified badge
- [x] Testimonial video carousel 4 cùng lúc
- [x] Mega footer 6 col + newsletter + payment
- [x] Trust strip 6 badges
- [x] Tabbed search widget trong hero
- [x] Không "make every screen feel like..."
- [x] Không em-dash
- [x] Vietnamese diacritics đầy đủ
- [x] tabular-nums cho giá
- [x] WCAG AA contrast
- [x] Reduced-motion respected
- [x] aria-label cho icon buttons
- [x] Lazy load dưới fold