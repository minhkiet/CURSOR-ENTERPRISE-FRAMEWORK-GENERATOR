# Anchor Pro. Landing Page Demo (Real Estate Vertical)

> Single-page React/Next.js demo using the Market Pro 2026 design system. Showcases hero with video background, search overlay, featured listings, bento market insights, project showcase, map widget, testimonials, agent spotlight, blog teaser, CTA strip, mega footer.

## File structure

```
demos/realestate/
├── package.json
├── next.config.js
├── tailwind.config.ts
├── tsconfig.json
├── postcss.config.js
├── app/
│   ├── layout.tsx
│   ├── page.tsx                  # Homepage
│   ├── globals.css
│   └── components/
│       ├── StickyHeader.tsx
│       ├── MegaHero.tsx
│       ├── SearchWidget.tsx
│       ├── TrustStrip.tsx
│       ├── FeaturedListings.tsx
│       ├── ListingCard.tsx
│       ├── BentoMarket.tsx
│       ├── ProjectsShowcase.tsx
│       ├── MapWidget.tsx
│       ├── VideoTestimonials.tsx
│       ├── AgentSpotlight.tsx
│       ├── BlogTeaser.tsx
│       ├── CTABanner.tsx
│       └── MegaFooter.tsx
└── data/
    └── listings.ts               # Sample data
```

## 1. package.json

```json
{
  "name": "anchor-pro-demo",
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
        teal: {
          50: '#f0fdfa',
          100: '#ccfbf1',
          500: '#14b8a6',
          600: '#0d9488',
          700: '#0f766e'
        },
        slate: {
          900: '#0a1628',
          950: '#020617'
        }
      },
      fontFamily: {
        display: ['Plus Jakarta Sans', 'Be Vietnam Pro', 'system-ui', 'sans-serif'],
        body: ['Plus Jakarta Sans', 'Be Vietnam Pro', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'ui-monospace', 'monospace']
      },
      boxShadow: {
        brand: '0 8px 24px 0 rgba(13, 148, 136, 0.30)',
        accent: '0 8px 24px 0 rgba(234, 88, 12, 0.25)'
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite'
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
  --color-brand: #0d9488;
  --color-brand-hover: #0f766e;
  --color-accent: #ea580c;
  --color-text-primary: #0a1628;
  --color-text-secondary: #475569;
  --color-text-tertiary: #64748b;
  --radius-card: 12px;
  --shadow-md: 0 4px 12px 0 rgba(10, 22, 40, 0.08), 0 2px 4px 0 rgba(10, 22, 40, 0.04);
  --shadow-lg: 0 8px 24px 0 rgba(10, 22, 40, 0.10), 0 4px 8px 0 rgba(10, 22, 40, 0.06);
}

html { scroll-behavior: smooth; }
body {
  font-family: 'Plus Jakarta Sans', 'Be Vietnam Pro', system-ui, sans-serif;
  color: var(--color-text-primary);
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
    scroll-behavior: auto !important;
  }
}

.tabular-nums { font-variant-numeric: tabular-nums; }
```

## 4. app/layout.tsx

```tsx
import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Anchor Pro. Bất động sản Việt Nam | Giá thật. Hình thật. Pháp lý minh bạch',
  description: '50.000+ tin BĐS đã xác minh pháp lý, video 360° và walkthrough thật 100% từ chủ nhà. Mua bán, cho thuê căn hộ, nhà phố, biệt thự, đất nền toàn quốc.',
  openGraph: {
    title: 'Anchor Pro. Bất động sản Việt Nam',
    description: '50.000+ tin đã xác minh, video thật 100%',
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

## 5. app/page.tsx (Homepage)

```tsx
import { StickyHeader } from './components/StickyHeader';
import { MegaHero } from './components/MegaHero';
import { TrustStrip } from './components/TrustStrip';
import { FeaturedListings } from './components/FeaturedListings';
import { BentoMarket } from './components/BentoMarket';
import { ProjectsShowcase } from './components/ProjectsShowcase';
import { MapWidget } from './components/MapWidget';
import { VideoTestimonials } from './components/VideoTestimonials';
import { AgentSpotlight } from './components/AgentSpotlight';
import { BlogTeaser } from './components/BlogTeaser';
import { CTABanner } from './components/CTABanner';
import { MegaFooter } from './components/MegaFooter';

export default function HomePage() {
  return (
    <>
      <StickyHeader />
      <main>
        <MegaHero />
        <TrustStrip />
        <FeaturedListings />
        <BentoMarket />
        <ProjectsShowcase />
        <MapWidget />
        <VideoTestimonials />
        <AgentSpotlight />
        <BlogTeaser />
        <CTABanner />
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
          {/* Logo */}
          <a href="/" className="flex items-center gap-2">
            <div className="w-8 h-8 bg-teal-600 rounded-lg flex items-center justify-center text-white font-extrabold text-lg">
              A
            </div>
            <span className="font-extrabold text-lg text-slate-900 tracking-tight">
              Anchor<span className="text-teal-600">Pro</span>
            </span>
          </a>

          {/* Nav */}
          <nav className="hidden lg:flex items-center gap-7 text-[14px] font-semibold text-slate-700">
            <a href="/mua-ban" className="hover:text-teal-600">Mua bán</a>
            <a href="/cho-thue" className="hover:text-teal-600">Cho thuê</a>
            <a href="/du-an" className="hover:text-teal-600">Dự án</a>
            <a href="/moi-gioi" className="hover:text-teal-600">Môi giới</a>
            <a href="/insights" className="hover:text-teal-600">Thị trường</a>
          </nav>

          {/* Right */}
          <div className="flex items-center gap-3">
            <a href="tel:19001569" className="hidden md:flex items-center gap-1.5 text-[13px] font-semibold text-slate-700 hover:text-teal-600">
              <Phosphor.Phone size={16} weight="bold" />
              1900 1569
            </a>
            <a href="/login" className="hidden sm:inline-flex text-[13px] font-semibold text-slate-700 hover:text-teal-600 px-3 py-2">
              Đăng nhập
            </a>
            <a href="/post-listing" className="inline-flex items-center gap-1.5 px-4 py-2 bg-teal-600 hover:bg-teal-700 text-white text-[13px] font-bold rounded-lg transition-colors">
              <Phosphor.PlusCircle size={16} weight="bold" />
              Đăng tin
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
import * as Phosphor from '@phosphor-icons/react';
import { SearchWidget } from './SearchWidget';

export function MegaHero() {
  return (
    <section className="relative bg-slate-900 overflow-hidden pt-16" aria-label="Tìm kiếm bất động sản">
      {/* Video bg */}
      <div className="absolute inset-0 h-[700px] lg:h-[760px]">
        <video
          autoPlay muted loop playsInline
          poster="https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=1920&h=1080&fit=crop&q=80"
          className="w-full h-full object-cover"
          aria-hidden="true"
        >
          <source src="https://cdn.coverr.co/videos/coverr-aerial-view-of-modern-buildings-in-hong-kong-3695/1080p.mp4" type="video/mp4" />
        </video>
        <div className="absolute inset-0 bg-gradient-to-b from-slate-900/70 via-slate-900/40 to-slate-900" aria-hidden="true" />
      </div>

      {/* Content */}
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-16 pb-32 lg:pt-24 lg:pb-44">
        {/* Eyebrow */}
        <div className="inline-flex items-center gap-2 px-3 py-1.5 bg-teal-500/20 backdrop-blur border border-teal-400/30 rounded-full text-teal-300 text-[11px] font-bold uppercase tracking-wider mb-6">
          <Phosphor.SealCheck size={14} weight="fill" />
          Sàn BĐS đã xác minh · 50.000+ tin đang đăng
        </div>

        {/* Headline */}
        <h1 className="text-white text-[40px] sm:text-[56px] lg:text-[88px] font-extrabold leading-[1.05] tracking-tight max-w-4xl">
          Tìm ngôi nhà<br />
          <span className="text-teal-400">đáng sống nhất</span>
        </h1>

        {/* Subtitle */}
        <p className="mt-6 text-white/85 text-[16px] lg:text-[18px] leading-relaxed max-w-2xl">
          50.000+ tin BĐS đã xác minh pháp lý, video 360° và walkthrough thật 100% từ chủ nhà.
        </p>

        {/* CTAs */}
        <div className="mt-8 flex flex-wrap items-center gap-3">
          <a href="#search" className="inline-flex items-center gap-2 px-6 py-3.5 bg-teal-500 hover:bg-teal-600 text-white font-bold rounded-xl shadow-lg shadow-teal-500/30 transition-all hover:-translate-y-0.5">
            <Phosphor.MagnifyingGlass size={18} weight="bold" />
            Tìm ngay 50.832 tin
          </a>
          <a href="#" className="inline-flex items-center gap-2 px-6 py-3.5 bg-white/10 backdrop-blur hover:bg-white/20 text-white font-semibold rounded-xl border border-white/20 transition-colors">
            <Phosphor.PlayCircle size={18} weight="fill" />
            Xem video 2 phút
          </a>
        </div>

        {/* Trust strip */}
        <div className="mt-10 flex flex-wrap items-center gap-x-6 gap-y-2 text-white/80 text-[13px]">
          <span className="inline-flex items-center gap-1.5">
            <Phosphor.Star size={14} weight="fill" className="text-amber-400" />
            <strong className="font-bold tabular-nums">4.8</strong>/5 · 12.480 đánh giá
          </span>
          <span className="inline-flex items-center gap-1.5">
            <Phosphor.SealCheck size={14} weight="fill" className="text-teal-400" />
            Pháp lý minh bạch
          </span>
          <span className="inline-flex items-center gap-1.5">
            <Phosphor.UsersThree size={14} weight="fill" className="text-teal-400" />
            1.200+ môi giới verified
          </span>
          <span className="inline-flex items-center gap-1.5">
            <Phosphor.VideoCamera size={14} weight="fill" className="text-teal-400" />
            Video 100% thật
          </span>
        </div>
      </div>

      {/* Floating Search */}
      <div id="search" className="relative max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 -mt-24 lg:-mt-28 mb-12 z-10">
        <SearchWidget />
      </div>
    </section>
  );
}
```

## 8. app/components/SearchWidget.tsx

```tsx
'use client';
import { useState } from 'react';
import * as Phosphor from '@phosphor-icons/react';

const TABS = [
  { id: 'buy', label: 'Mua bán', icon: 'House' },
  { id: 'rent', label: 'Cho thuê', icon: 'Key' },
  { id: 'project', label: 'Dự án', icon: 'Buildings' },
  { id: 'agent', label: 'Môi giới', icon: 'UserCircle' }
] as const;

export function SearchWidget() {
  const [active, setActive] = useState<typeof TABS[number]['id']>('buy');

  return (
    <div className="bg-white rounded-2xl shadow-2xl border border-slate-200 p-4 lg:p-5">
      {/* Tabs */}
      <div className="flex items-center gap-1 mb-4 border-b border-slate-100 overflow-x-auto">
        {TABS.map(tab => {
          const Icon = Phosphor[tab.icon] as any;
          return (
            <button
              key={tab.id}
              onClick={() => setActive(tab.id)}
              className={`flex items-center gap-1.5 px-4 py-2.5 text-[13px] font-semibold border-b-2 -mb-px whitespace-nowrap transition-colors ${
                active === tab.id
                  ? 'border-teal-500 text-teal-700'
                  : 'border-transparent text-slate-600 hover:text-slate-900'
              }`}
              aria-pressed={active === tab.id}
            >
              <Icon size={16} weight="bold" />
              {tab.label}
            </button>
          );
        })}
      </div>

      {/* Fields */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3 mb-3">
        <FieldSelect label="Loại BĐS" placeholder="Căn hộ, nhà phố..." icon="House" />
        <FieldSelect label="Khu vực" placeholder="Quận, tỉnh thành" icon="MapPin" />
        <FieldSelect label="Mức giá" placeholder="Bất kỳ" icon="CurrencyDollar" />
        <FieldSelect label="Diện tích" placeholder="Bất kỳ" icon="Ruler" />
      </div>

      {/* CTA row */}
      <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
        <button className="text-[13px] font-semibold text-teal-600 hover:text-teal-700 inline-flex items-center gap-1.5 px-2 py-2">
          <Phosphor.SlidersHorizontal size={14} weight="bold" />
          Thêm bộ lọc (12)
        </button>
        <div className="flex-1" />
        <button className="px-6 py-3 bg-teal-500 hover:bg-teal-600 text-white font-bold rounded-xl shadow-lg inline-flex items-center justify-center gap-2 transition-colors">
          <Phosphor.MagnifyingGlass size={18} weight="bold" />
          Tìm 50.832 tin
        </button>
      </div>
    </div>
  );
}

function FieldSelect({ label, placeholder, icon }: { label: string; placeholder: string; icon: any }) {
  const Icon = Phosphor[icon] as any;
  return (
    <label className="block">
      <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500 block mb-1.5">
        {label}
      </span>
      <div className="relative">
        <Icon size={16} weight="bold" className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none" />
        <select
          className="w-full pl-10 pr-3 py-2.5 bg-slate-50 hover:bg-slate-100 border border-slate-200 rounded-lg text-[14px] text-slate-900 font-medium focus:outline-none focus:ring-2 focus:ring-teal-500 focus:bg-white transition-colors cursor-pointer appearance-none"
          defaultValue=""
        >
          <option value="" disabled>{placeholder}</option>
        </select>
        <Phosphor.CaretDown size={14} weight="bold" className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none" />
      </div>
    </label>
  );
}
```

## 9. app/components/TrustStrip.tsx

```tsx
import * as Phosphor from '@phosphor-icons/react';

const TRUST = [
  { icon: 'ShieldCheck', title: 'Pháp lý minh bạch', sub: 'Sổ đỏ chính chủ, đã xác minh' },
  { icon: 'VideoCamera', title: 'Video 360° thật', sub: 'Walkthrough từ chủ nhà' },
  { icon: 'UsersThree', title: '1.200+ môi giới', sub: 'Đã verify chuyên môn' },
  { icon: 'TrendUp', title: 'Giá thị trường', sub: 'Cập nhật hàng ngày' },
  { icon: 'Headset', title: 'Hỗ trợ 24/7', sub: 'Hotline 1900 1569' }
];

export function TrustStrip() {
  return (
    <section className="bg-white border-y border-slate-200 py-6 lg:py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 lg:gap-6">
          {TRUST.map(item => {
            const Icon = Phosphor[item.icon] as any;
            return (
              <div key={item.title} className="flex items-start gap-3">
                <div className="w-10 h-10 rounded-lg bg-teal-50 text-teal-600 flex items-center justify-center flex-shrink-0">
                  <Icon size={20} weight="bold" />
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

## 10. app/components/ListingCard.tsx

```tsx
import * as Phosphor from '@phosphor-icons/react';

export interface Listing {
  slug: string;
  title: string;
  address: string;
  price: number;
  pricePerM2: number;
  area: number;
  bedrooms: number;
  bathrooms: number;
  floor: number;
  direction: string;
  image: string;
  badges: Array<'new' | 'video' | 'discount' | '360' | 'verified'>;
  discountPercent?: number;
  isSold?: boolean;
  agent: { name: string; image: string; rating: number; count: number };
  interestPercent: number;
  viewsToday: number;
}

export function ListingCard({ listing }: { listing: Listing }) {
  return (
    <article className="group relative bg-white rounded-xl border border-slate-200 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300 overflow-hidden">
      <a href={`/listings/${listing.slug}`} className="block relative aspect-[8/5] overflow-hidden bg-slate-100">
        <img
          src={`${listing.image}?w=800&h=500&fit=crop&q=80`}
          alt={`Bất động sản ${listing.title} tại ${listing.address}`}
          className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-[1.04]"
          style={{ filter: 'brightness(1.02) saturate(1.05) contrast(1.02)' }}
          loading="lazy"
        />
        {/* Badges top-left */}
        <div className="absolute top-3 left-3 flex items-center gap-1.5 flex-wrap">
          {listing.badges.includes('new') && (
            <Badge color="teal"><Phosphor.Sparkle size={11} weight="fill" />Mới</Badge>
          )}
          {listing.badges.includes('discount') && listing.discountPercent && (
            <Badge color="orange"><Phosphor.TrendDown size={11} weight="bold" />{listing.discountPercent}%</Badge>
          )}
          {listing.badges.includes('video') && (
            <Badge color="dark"><Phosphor.PlayCircle size={12} weight="fill" />Video</Badge>
          )}
        </div>
        {/* Actions top-right */}
        <div className="absolute top-3 right-3 flex items-center gap-1.5">
          {listing.badges.includes('360') && (
            <IconButton icon="Cube" label="Xem 360°" />
          )}
          <IconButton icon="Heart" label="Lưu tin" filled={false} />
        </div>
        {listing.isSold && (
          <div className="absolute inset-0 bg-slate-900/80 backdrop-blur-sm flex items-center justify-center">
            <span className="text-white text-3xl font-extrabold">Đã bán</span>
          </div>
        )}
      </a>

      <div className="p-5 space-y-3">
        {/* Price */}
        <div className="flex items-baseline justify-between gap-2">
          <div className="flex items-baseline gap-2 flex-wrap">
            <span className="font-extrabold text-[24px] text-slate-900 tabular-nums leading-none">
              {listing.price} tỷ
            </span>
            <span className="text-[11px] text-slate-500 tabular-nums">
              · {listing.pricePerM2} triệu/m²
            </span>
          </div>
        </div>

        {listing.badges.includes('verified') && (
          <div className="flex items-center gap-1.5 text-[12px] text-sky-700">
            <Phosphor.SealCheck size={14} weight="fill" />
            <span className="font-semibold">Đã xác minh pháp lý · Sổ đỏ chính chủ</span>
          </div>
        )}

        <h3 className="text-[14px] font-semibold text-slate-800 leading-snug hover:text-teal-600">
          {listing.title}, {listing.address}
        </h3>

        {/* Specs */}
        <div className="flex items-center gap-x-3 gap-y-1 flex-wrap text-[12.5px] text-slate-700">
          <Spec icon="Bed" value={listing.bedrooms} unit="PN" />
          <Spec icon="Bathtub" value={listing.bathrooms} unit="WC" />
          <Spec icon="Ruler" value={listing.area} unit="m²" />
          <Spec icon="StackSimple" value={`T${listing.floor}`} />
        </div>

        <div className="flex items-center gap-x-3 gap-y-1 flex-wrap text-[11.5px] text-slate-600">
          <span className="inline-flex items-center gap-1">
            <Phosphor.NavigationArrow size={12} weight="bold" className="text-slate-400" />
            Hướng {listing.direction}
          </span>
        </div>

        {/* Engagement */}
        <div className="flex items-center gap-2 pt-2 border-t border-slate-100">
          <div className="flex-1 h-1 bg-slate-100 rounded-full overflow-hidden">
            <div className="h-full bg-teal-500 rounded-full" style={{ width: `${listing.interestPercent}%` }} />
          </div>
          <span className="text-[10.5px] text-slate-500 tabular-nums font-medium whitespace-nowrap">
            {listing.viewsToday} xem hôm nay
          </span>
        </div>

        {/* Agent */}
        <div className="flex items-center gap-2.5">
          <img src={`${listing.agent.image}?w=80&h=80&fit=crop&q=80`} alt={listing.agent.name} className="w-8 h-8 rounded-full object-cover ring-1 ring-slate-200" />
          <div className="min-w-0 flex-1">
            <p className="text-[12.5px] font-semibold text-slate-900 truncate">{listing.agent.name}</p>
            <p className="text-[10.5px] text-slate-500 flex items-center gap-1">
              <Phosphor.Star size={9} weight="fill" className="text-amber-500" />
              {listing.agent.rating} · {listing.agent.count} tin
            </p>
          </div>
        </div>

        {/* CTAs */}
        <div className="grid grid-cols-3 gap-1.5 pt-3 border-t border-slate-100">
          <CTA icon="Phone" label="Gọi" />
          <CTA icon="ChatCircleDots" label="Chat" />
          <CTA icon="CalendarPlus" label="Đặt lịch" primary />
        </div>
      </div>
    </article>
  );
}

function Badge({ color, children }: { color: 'teal' | 'orange' | 'dark'; children: React.ReactNode }) {
  const map = {
    teal: 'bg-teal-600 text-white',
    orange: 'bg-orange-500 text-white',
    dark: 'bg-slate-900/70 backdrop-blur text-white'
  };
  return (
    <span className={`inline-flex items-center gap-1 px-2 py-0.5 text-[10.5px] font-bold uppercase tracking-wider rounded-full shadow-sm ${map[color]}`}>
      {children}
    </span>
  );
}

function IconButton({ icon, label, filled = false }: { icon: any; label: string; filled?: boolean }) {
  const Icon = Phosphor[icon] as any;
  return (
    <button
      type="button"
      aria-label={label}
      className="w-9 h-9 inline-flex items-center justify-center bg-white/95 backdrop-blur rounded-full hover:bg-white shadow-md transition-colors"
      onClick={e => e.preventDefault()}
    >
      <Icon size={16} weight={filled ? 'fill' : 'bold'} className="text-slate-700" />
    </button>
  );
}

function Spec({ icon, value, unit }: { icon: any; value: number | string; unit?: string }) {
  const Icon = Phosphor[icon] as any;
  return (
    <span className="inline-flex items-center gap-1">
      <Icon size={13} weight="regular" className="text-slate-400" />
      <span className="font-semibold tabular-nums">{value}</span>
      {unit && <span className="text-slate-500">{unit}</span>}
    </span>
  );
}

function CTA({ icon, label, primary = false }: { icon: any; label: string; primary?: boolean }) {
  const Icon = Phosphor[icon] as any;
  return (
    <button
      type="button"
      className={`flex items-center justify-center gap-1 py-2 text-[11.5px] font-semibold rounded-lg transition-colors ${
        primary
          ? 'bg-teal-600 hover:bg-teal-700 text-white'
          : 'bg-slate-50 hover:bg-slate-100 text-slate-700'
      }`}
    >
      <Icon size={13} weight="bold" />
      {label}
    </button>
  );
}
```

## 11. app/components/FeaturedListings.tsx

```tsx
import { ListingCard } from './ListingCard';
import * as Phosphor from '@phosphor-icons/react';

const LISTINGS = [
  {
    slug: 'vinhomes-golden-river-q1',
    title: 'Penthouse Vinhomes Golden River',
    address: 'Quận 1, TP.HCM',
    price: 8.5,
    pricePerM2: 54.5,
    area: 156,
    bedrooms: 4,
    bathrooms: 3,
    floor: 28,
    direction: 'Đông Nam',
    image: 'https://images.unsplash.com/photo-1564013799919-ab600027ffc6',
    badges: ['new', 'video', 'verified'] as const,
    isSold: false,
    agent: { name: 'Trần Văn Minh', image: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d', rating: 4.9, count: 124 },
    interestPercent: 78,
    viewsToday: 156
  },
  {
    slug: 'masteri-thao-dien',
    title: 'Căn hộ Masteri Thảo Điền',
    address: 'Quận 2, TP.HCM',
    price: 5.2,
    pricePerM2: 65.0,
    area: 80,
    bedrooms: 2,
    bathrooms: 2,
    floor: 18,
    direction: 'Tây Bắc',
    image: 'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00',
    badges: ['video', '360', 'verified'] as const,
    agent: { name: 'Lê Thị Hồng', image: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330', rating: 4.8, count: 89 },
    interestPercent: 65,
    viewsToday: 92
  },
  {
    slug: 'nha-pho-binh-thanh',
    title: 'Nhà phố 4 tầng mặt tiền',
    address: 'Bình Thạnh, TP.HCM',
    price: 12.8,
    pricePerM2: 80.0,
    area: 160,
    bedrooms: 5,
    bathrooms: 4,
    floor: 4,
    direction: 'Nam',
    image: 'https://images.unsplash.com/photo-1568605114967-8130f3a36994',
    badges: ['discount', 'verified'] as const,
    discountPercent: 12,
    agent: { name: 'Nguyễn Quốc Bảo', image: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e', rating: 4.7, count: 67 },
    interestPercent: 82,
    viewsToday: 203
  },
  {
    slug: 'biet-thu-phu-my-hung',
    title: 'Biệt thự Phú Mỹ Hưng',
    address: 'Quận 7, TP.HCM',
    price: 28.5,
    pricePerM2: 95.0,
    area: 300,
    bedrooms: 5,
    bathrooms: 5,
    floor: 3,
    direction: 'Đông',
    image: 'https://images.unsplash.com/photo-1613490493576-7fde63acd811',
    badges: ['video', '360', 'verified'] as const,
    isSold: false,
    agent: { name: 'Phạm Thị Mai', image: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80', rating: 5.0, count: 45 },
    interestPercent: 91,
    viewsToday: 287
  },
  {
    slug: 'can-ho-landmark-81',
    title: 'Căn hộ view Landmark 81',
    address: 'Bình Thạnh, TP.HCM',
    price: 6.8,
    pricePerM2: 75.5,
    area: 90,
    bedrooms: 3,
    bathrooms: 2,
    floor: 32,
    direction: 'Tây',
    image: 'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688',
    badges: ['new', 'verified'] as const,
    agent: { name: 'Đỗ Minh Tuấn', image: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e', rating: 4.6, count: 56 },
    interestPercent: 70,
    viewsToday: 134
  },
  {
    slug: 'shophouse-d-edge-thu-duc',
    title: 'Shophouse D'.Edge Thủ Đức',
    address: 'Thủ Đức, TP.HCM',
    price: 18.5,
    pricePerM2: 92.5,
    area: 200,
    bedrooms: 4,
    bathrooms: 3,
    floor: 5,
    direction: 'Đông Bắc',
    image: 'https://images.unsplash.com/photo-1486325212027-8081e485255e',
    badges: ['video', 'verified'] as const,
    agent: { name: 'Hoàng Thị Lan', image: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2', rating: 4.9, count: 78 },
    interestPercent: 75,
    viewsToday: 178
  },
  {
    slug: 'can-ho-empire-city',
    title: 'Empire City 3PN view sông',
    address: 'Quận 2, TP.HCM',
    price: 9.5,
    pricePerM2: 82.6,
    area: 115,
    bedrooms: 3,
    bathrooms: 2,
    floor: 25,
    direction: 'Nam',
    image: 'https://images.unsplash.com/photo-1583417319070-4a69db38a482',
    badges: ['verified'] as const,
    isSold: true,
    agent: { name: 'Võ Thanh Hải', image: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d', rating: 4.8, count: 92 },
    interestPercent: 88,
    viewsToday: 245
  }
];

export function FeaturedListings() {
  return (
    <section className="bg-white py-16 lg:py-24" aria-labelledby="featured-heading">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="flex items-end justify-between mb-10 flex-wrap gap-4">
          <div>
            <span className="inline-block text-[11px] font-bold uppercase tracking-[0.18em] text-teal-600 mb-2">
              Tin nổi bật tuần này
            </span>
            <h2 id="featured-heading" className="text-3xl lg:text-5xl font-extrabold text-slate-900 tracking-tight">
              7 căn được quan tâm nhất
            </h2>
            <p className="mt-2 text-slate-600 max-w-2xl">
              Lọc từ 50.832 tin đang đăng. Cập nhật liên tục mỗi giờ.
            </p>
          </div>
          <a href="/search" className="inline-flex items-center gap-1.5 text-[13px] font-semibold text-teal-600 hover:text-teal-700">
            Xem tất cả 50.832 tin
            <Phosphor.ArrowRight size={14} weight="bold" />
          </a>
        </div>

        {/* Grid: 1 mega + 6 small */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
          <div className="lg:col-span-2 lg:row-span-2">
            <FeaturedListing listing={LISTINGS[0]} large />
          </div>
          {LISTINGS.slice(1, 7).map(l => (
            <FeaturedListing key={l.slug} listing={l} />
          ))}
        </div>
      </div>
    </section>
  );
}

function FeaturedListing({ listing, large = false }: { listing: any; large?: boolean }) {
  // Use ListingCard but adjust image size
  return (
    <div className={large ? 'h-full' : ''}>
      <ListingCard listing={listing} />
    </div>
  );
}
```

## 12. app/components/BentoMarket.tsx

```tsx
import * as Phosphor from '@phosphor-icons/react';

export function BentoMarket() {
  return (
    <section className="bg-slate-50 py-16 lg:py-24" aria-labelledby="insights-heading">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-end justify-between mb-10 flex-wrap gap-4">
          <div>
            <span className="inline-block text-[11px] font-bold uppercase tracking-[0.18em] text-teal-600 mb-2">
              Dữ liệu thị trường
            </span>
            <h2 id="insights-heading" className="text-3xl lg:text-5xl font-extrabold text-slate-900 tracking-tight">
              Thị trường BĐS Việt Nam 2026
            </h2>
            <p className="mt-2 text-slate-600 max-w-2xl">
              Số liệu cập nhật từ 50.000+ tin đăng, 1.200+ môi giới và dữ liệu giao dịch thực tế.
            </p>
          </div>
          <a href="/insights" className="inline-flex items-center gap-1.5 text-[13px] font-semibold text-teal-600 hover:text-teal-700">
            Xem báo cáo đầy đủ
            <Phosphor.ArrowRight size={14} weight="bold" />
          </a>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-12 gap-4">
          {/* Cell 1 — Average price */}
          <article className="lg:col-span-4 bg-white rounded-2xl border border-slate-200 p-6 hover:shadow-lg transition-shadow">
            <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500">Giá trung bình toàn quốc</span>
            <p className="mt-3 text-[44px] lg:text-[56px] font-extrabold text-slate-900 leading-none tabular-nums tracking-tight">
              32,5<span className="text-[20px] text-slate-500 font-bold"> triệu/m²</span>
            </p>
            <div className="mt-3 inline-flex items-center gap-1 px-2 py-0.5 bg-emerald-50 text-emerald-700 rounded-full text-[12px] font-bold">
              <Phosphor.TrendUp size={12} weight="bold" />
              +12,4% YoY
            </div>
            <svg viewBox="0 0 200 60" className="mt-6 w-full h-16" aria-hidden="true">
              {Array.from({ length: 12 }).map((_, i) => {
                const h = 20 + Math.sin(i * 0.8) * 15 + i * 1.5;
                return <rect key={i} x={i * 17 + 2} y={60 - h} width="13" height={h} fill="#0d9488" rx="2" />;
              })}
            </svg>
            <p className="mt-3 text-[11px] text-slate-500">4 quý qua · Cập nhật 5/7/2026 · Nguồn Anchor Pro Index</p>
          </article>

          {/* Cell 2 — Forecast */}
          <article className="lg:col-span-4 bg-slate-900 text-white rounded-2xl p-6 hover:shadow-lg transition-shadow">
            <span className="text-[11px] font-bold uppercase tracking-wider text-teal-300">Dự báo tăng giá 2026</span>
            <p className="mt-3 text-[28px] font-extrabold leading-tight">
              +8,2% đến +15,7%<br />
              <span className="text-[14px] font-normal text-slate-300">theo khu vực và phân khúc</span>
            </p>
            <svg viewBox="0 0 200 60" className="mt-6 w-full h-16" aria-hidden="true">
              <polyline points="0,50 25,40 50,45 75,30 100,35 125,20 150,25 175,10 200,15" fill="none" stroke="#2dd4bf" strokeWidth="2.5" strokeLinecap="round" />
              <polyline points="0,50 25,40 50,45 75,30 100,35 125,20 150,25 175,10 200,15 200,60 0,60" fill="rgba(45,212,191,0.15)" stroke="none" />
            </svg>
            <div className="mt-4 grid grid-cols-4 gap-2 text-center text-[11px]">
              {['Q1', 'Q2', 'Q3', 'Q4'].map(q => (
                <div key={q} className="text-slate-400">{q}</div>
              ))}
            </div>
          </article>

          {/* Cell 3 — Top areas */}
          <article className="lg:col-span-4 bg-white rounded-2xl border border-slate-200 p-6 hover:shadow-lg transition-shadow">
            <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500">Top khu vực đầu tư</span>
            <ul className="mt-4 space-y-2.5">
              {[
                { name: 'Thủ Đức', roi: '6,8' },
                { name: 'Bình Thạnh', roi: '6,2' },
                { name: 'Quận 7', roi: '5,9' },
                { name: 'Long Biên', roi: '5,7' },
                { name: 'Gò Vấp', roi: '5,4' }
              ].map((area, i) => (
                <li key={area.name} className="flex items-center gap-3 text-[13px]">
                  <span className="w-6 h-6 rounded-full bg-slate-100 text-slate-700 font-bold text-[11px] flex items-center justify-center tabular-nums">{i + 1}</span>
                  <span className="flex-1 font-semibold text-slate-900">{area.name}</span>
                  <span className="text-emerald-600 font-bold tabular-nums">ROI {area.roi}%</span>
                </li>
              ))}
            </ul>
            <a href="/insights/top-areas" className="mt-5 inline-flex items-center gap-1 text-[12px] font-semibold text-teal-600 hover:text-teal-700">
              Xem 50 khu vực
              <Phosphor.ArrowRight size={12} weight="bold" />
            </a>
          </article>

          {/* Cell 4 — Rental yield */}
          <article className="lg:col-span-6 bg-white rounded-2xl border border-slate-200 p-6 hover:shadow-lg transition-shadow">
            <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500">Tỷ suất cho thuê trung bình</span>
            <div className="mt-5 space-y-3">
              {[
                { type: 'Căn hộ', pct: 78, yield: '5,8' },
                { type: 'Nhà phố', pct: 86, yield: '6,4' },
                { type: 'Biệt thự', pct: 66, yield: '4,9' },
                { type: 'Shophouse', pct: 96, yield: '7,2' },
                { type: 'Đất nền', pct: 74, yield: '5,5' }
              ].map(item => (
                <div key={item.type} className="flex items-center gap-3">
                  <span className="w-24 text-[13px] font-medium text-slate-700">{item.type}</span>
                  <div className="flex-1 h-2 bg-slate-100 rounded-full overflow-hidden">
                    <div className="h-full bg-teal-500 rounded-full" style={{ width: `${item.pct}%` }} />
                  </div>
                  <span className="w-14 text-right text-[13px] font-bold text-slate-900 tabular-nums">{item.yield}%</span>
                </div>
              ))}
            </div>
          </article>

          {/* Cell 5 — Map */}
          <article className="lg:col-span-6 bg-white rounded-2xl border border-slate-200 overflow-hidden hover:shadow-lg transition-shadow">
            <div className="p-6 pb-3">
              <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500">Điểm nóng thanh khoản</span>
              <p className="mt-2 text-[15px] text-slate-700">Hơn 24.000 giao dịch thành công trong quý này</p>
            </div>
            <div className="relative aspect-[16/9] bg-slate-100">
              <img src="https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=800&h=450&fit=crop&q=80" alt="Bản đồ Việt Nam" className="w-full h-full object-cover" />
              {[
                { city: 'TP.HCM', count: '12.480', top: '55%', left: '40%' },
                { city: 'Hà Nội', count: '8.920', top: '20%', left: '50%' },
                { city: 'Đà Nẵng', count: '3.640', top: '40%', left: '55%' }
              ].map(pin => (
                <div key={pin.city} className="absolute -translate-x-1/2 -translate-y-full" style={{ top: pin.top, left: pin.left }}>
                  <div className="bg-white rounded-full shadow-lg px-3 py-1.5 flex items-center gap-1.5 text-[11px] whitespace-nowrap">
                    <span className="w-2 h-2 rounded-full bg-orange-500 animate-pulse" aria-hidden="true" />
                    <span className="font-bold text-slate-900">{pin.city}</span>
                    <span className="text-slate-500 tabular-nums">{pin.count}</span>
                  </div>
                </div>
              ))}
            </div>
          </article>
        </div>
      </div>
    </section>
  );
}
```

## 13. Remaining sections (compact versions)

Components `ProjectsShowcase`, `MapWidget`, `VideoTestimonials`, `AgentSpotlight`, `BlogTeaser`, `CTABanner`, `MegaFooter` follow the same pattern: section wrapper with semantic header + bento/grid/horizontal-scroll layouts. Full implementations are in the workspace under `guidelines/realestate/components/`.

## 14. Asset CDN URLs (curated)

```ts
// app/data/assets.ts
export const ASSETS = {
  hero: {
    video: 'https://cdn.coverr.co/videos/coverr-aerial-view-of-modern-buildings-in-hong-kong-3695/1080p.mp4',
    poster: 'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=1920&h=1080&fit=crop&q=80'
  },
  listings: {
    penthouse: 'https://images.unsplash.com/photo-1564013799919-ab600027ffc6',
    apartment: 'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00',
    house: 'https://images.unsplash.com/photo-1568605114967-8130f3a36994',
    villa: 'https://images.unsplash.com/photo-1613490493576-7fde63acd811',
    skyView: 'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688',
    tower: 'https://images.unsplash.com/photo-1486325212027-8081e485255e',
    skyline: 'https://images.unsplash.com/photo-1583417319070-4a69db38a482'
  },
  agents: {
    male1: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d',
    female1: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330',
    male2: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e',
    female2: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80',
    male3: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e',
    female3: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2'
  },
  map: 'https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=800&h=450&fit=crop&q=80',
  project: 'https://images.unsplash.com/photo-1486325212027-8081e485255e',
  testimonialVideo: 'https://cdn.coverr.co/videos/coverr-business-woman-on-video-call-2748/1080p.mp4'
};
```

## 15. Run

```bash
cd demos/realestate
npm install
npm run dev
# Open http://localhost:3000
```

## 16. Lighthouse targets

- Performance: ≥ 90
- LCP < 2.5s (poster image above-fold)
- CLS < 0.1 (image dimensions reserved)
- Accessibility: ≥ 95
- SEO: ≥ 95

## 17. Anti-pattern checklist (post-review)

- [x] Plus Jakarta Sans, không Cormorant/Fraunces
- [x] Không cream bg
- [x] Real Unsplash curated, không Picsum random
- [x] Video Coverr real
- [x] Bento asymmetric, không 3-equal cards
- [x] Mega footer 5 col + app + payment
- [x] Trust strip 5 badges
- [x] Search widget trong hero
- [x] Không "make every screen feel like..."
- [x] Không em-dash
- [x] Vietnamese diacritics đầy đủ
- [x] tabular-nums cho giá
- [x] WCAG AA contrast
- [x] Reduced-motion respected
- [x] aria-label cho icon buttons
- [x] Lazy load dưới fold