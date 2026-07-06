# Mega Hero + Flight Search Widget

> Hero với video destination background + tabbed search widget (Flight / Hotel / Tour / Combo). Đây là first-screen focus của Skylark homepage.

## 1. Mục đích

Khách truy cập homepage trong 3 giây phải hiểu: đây là gì, có thể làm gì, bắt đầu từ đâu. Hero đáp ứng cả 3 bằng:
- Headline rõ ràng ("Du lịch Đông Nam Á")
- Video destination bg tạo cảm xúc
- Search widget tabbed 4-in-1 ngay trong hero

## 2. Asset

| Element | Source |
|---|---|
| Hero video | Coverr aerial Phú Quốc / Đà Lạt / Bali |
| Hero poster | Unsplash fallback `1582719508461-905c673771fd` |
| Destination thumbnails | Unsplash curated 6 điểm |

## 3. Cấu trúc

```
┌─────────────────────────────────────────────────────────┐
│  [VIDEO BG: aerial Phú Quốc 16s loop]                  │
│                                                         │
│  Eyebrow: "Sàn OTA #1 Đông Nam Á · 4.8★ từ 248K review"│
│                                                         │
│  Du lịch Đông Nam Á                                    │
│  Giá tốt. Đặt nhanh. Hoàn tiền dễ.                    │
│                                                         │
│  ┌───────────────────────────────────────────────┐     │
│  │ ✈ Flight │ 🏨 Hotel │ 🗺 Tour │ ⚡ Combo      │     │
│  ├───────────────────────────────────────────────┤     │
│  │ [From]  →  [To]    [Depart]  [Return]  [Pax]  │     │
│  │ Hà Nội    Đà Lạt    25/07     28/07    1 người│     │
│  │                                               │     │
│  │ [    Tìm chuyến bay    ]  [Recently searched] │     │
│  └───────────────────────────────────────────────┘     │
│                                                         │
│  Trust: ✓ Giá rẻ nhất ✓ Hoàn tiền 200% ✓ IATA certified│
└─────────────────────────────────────────────────────────┘
```

## 4. Variants

| Variant | Use | Khác biệt |
|---|---|---|
| `default` | Homepage hero | Video + 4-tab search |
| `compact` | Section header | Không video, 1 search type |
| `seasonal` | Peak season | Countdown + flash deal badge |
| `loyalty` | Returning user | Lời chào cá nhân + recent |

## 5. States

| State | Visual |
|---|---|
| default | Video playing, search interactive |
| focused-tab | Tab navy underline + bold |
| reduce-motion | Poster image thay video |
| loading-search | Skeleton overlay |
| mobile | Stack fields vertical, video 60% height |

## 6. Icon mapping

| Tab | Phosphor |
|---|---|
| Flight | `AirplaneTilt` |
| Hotel | `Buildings` |
| Tour | `MapTrifold` |
| Combo | `Lightning` |
| From swap | `ArrowsLeftRight` |
| Depart | `CalendarBlank` |
| Pax | `Users` |
| Search | `MagnifyingGlass` |
| Recent | `ClockCounterClockwise` |
| Trust | `SealCheck` (fill) |

## 7. Code reference

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

export function MegaHeroTravel() {
  const [tab, setTab] = useState<typeof TABS[number]['id']>('flight');

  return (
    <section className="relative bg-slate-900 overflow-hidden" aria-label="Tìm kiếm chuyến bay và khách sạn">
      {/* Video bg */}
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

      {/* Content */}
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-24 pb-40 lg:pt-32 lg:pb-52">
        {/* Eyebrow */}
        <div className="inline-flex items-center gap-2 px-3 py-1.5 bg-sky-500/20 backdrop-blur border border-sky-400/30 rounded-full text-sky-200 text-[11px] font-bold uppercase tracking-wider mb-6">
          <Phosphor.SealCheck size={14} weight="fill" />
          Sàn OTA #1 Đông Nam Á · 4.8★ từ 248.000 đánh giá
        </div>

        {/* Headline */}
        <h1 className="text-white text-[40px] sm:text-[56px] lg:text-[88px] font-extrabold leading-[1.05] tracking-tight max-w-4xl">
          Du lịch Đông Nam Á<br />
          <span className="text-rose-400">không lo về giá</span>
        </h1>

        {/* Subtitle */}
        <p className="mt-6 text-white/85 text-[16px] lg:text-[18px] leading-relaxed max-w-2xl">
          2.500+ chuyến bay · 50.000+ khách sạn · 800+ tour mỗi ngày. Hoàn tiền 200% nếu giá cao hơn.
        </p>

        {/* Trust strip */}
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

      {/* Floating Search */}
      <div className="relative max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 -mt-32 lg:-mt-40 mb-12 z-10">
        <SearchWidget active={tab} onChange={setTab} />
      </div>
    </section>
  );
}

function SearchWidget({ active, onChange }: { active: string; onChange: (v: any) => void }) {
  return (
    <div className="bg-white rounded-2xl shadow-2xl border border-slate-200 p-4 lg:p-5">
      {/* Tabs */}
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

      {/* Flight tab content */}
      {active === 'flight' && (
        <div>
          <div className="grid grid-cols-1 lg:grid-cols-[1fr_auto_1fr_1fr_1fr_auto] gap-3 mb-3">
            <SearchField label="Từ" placeholder="Hà Nội (HAN)" icon="AirplaneTakeoff" />
            <button className="self-end mb-2.5 w-9 h-9 inline-flex items-center justify-center bg-slate-100 hover:bg-slate-200 rounded-full transition-colors" aria-label="Đổi chiều">
              <Phosphor.ArrowsLeftRight size={14} weight="bold" className="text-slate-700" />
            </button>
            <SearchField label="Đến" placeholder="Đà Lạt (DLI)" icon="AirplaneLanding" />
            <SearchField label="Khởi hành" placeholder="25/07/2026" icon="CalendarBlank" />
            <SearchField label="Khách" placeholder="1 người lớn" icon="Users" />
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

      {/* Hotel tab content */}
      {active === 'hotel' && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3 mb-3">
          <SearchField label="Điểm đến" placeholder="Phú Quốc, Hội An..." icon="MapPin" />
          <SearchField label="Nhận phòng" placeholder="25/07/2026" icon="CalendarBlank" />
          <SearchField label="Trả phòng" placeholder="28/07/2026" icon="CalendarBlank" />
          <SearchField label="Khách & phòng" placeholder="2 người lớn, 1 phòng" icon="Users" />
        </div>
      )}

      {/* Tour / Combo: simple placeholder */}
      {(active === 'tour' || active === 'combo') && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-3">
          <SearchField label="Điểm đến" placeholder="Bali, Singapore..." icon="MapPin" />
          <SearchField label="Ngày khởi hành" placeholder="25/07/2026" icon="CalendarBlank" />
          <SearchField label="Số khách" placeholder="2 người" icon="Users" />
        </div>
      )}

      <div className="flex items-center justify-end gap-2 pt-2">
        <button className="text-[13px] font-semibold text-slate-600 hover:text-sky-600 px-3 py-2 inline-flex items-center gap-1.5">
          <Phosphor.ClockCounterClockwise size={14} weight="bold" />
          Tìm gần đây
        </button>
        <button className="text-[13px] font-semibold text-slate-600 hover:text-sky-600 px-3 py-2 inline-flex items-center gap-1.5">
          <Phosphor.Funnel size={14} weight="bold" />
          Bộ lọc nâng cao
        </button>
      </div>
    </div>
  );
}

function SearchField({ label, placeholder, icon }: { label: string; placeholder: string; icon: any }) {
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

## 8. Accessibility

- Tab list `role="tablist"`, each tab `role="tab"` + `aria-selected`
- Search fields có `<label>` thật
- Swap button `aria-label`
- Video `aria-hidden="true"` (decorative)
- Headline là `<h1>` (page title)
- Trust strip badges có icon + text, không chỉ màu
- "Gợi ý" links có hover rõ + focus visible
- Reduce-motion: poster image thay video

## 9. Performance

- Video poster image dùng `<link rel="preload">` cho LCP
- Video `preload="metadata"` không tải full
- Search fields sử dụng native `<input>` để tận dụng autocomplete browser
- Tabs là client component để tránh flash
- Trust strip có icon Phosphor (SVG inline, no extra request)

---

**Component family**: Layout #1 — `mega-hero-with-search`