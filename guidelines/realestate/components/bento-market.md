# Bento Market Insights

> Section thống kê thị trường BĐS. Bento grid 5 cells không đều: 1 lớn + 4 nhỏ. Mỗi cell có mini-chart, số liệu, link. Khác với 3-equal-card cliché.

## 1. Mục đích

Truyền tải dữ liệu thị trường BĐS Việt Nam 2026 một cách trực quan. Bento style asymmetric, mỗi cell là 1 insight riêng biệt. Có chart, có % tăng trưởng, có map mini, có danh sách top.

## 2. Asset

| Element | Source | Notes |
|---|---|---|
| Mini chart bars | Generated SVG (pure component) | No image, pure code |
| Map thumbnail | `https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=600&h=400&fit=crop&q=80` (modern district aerial) | 3:2 |
| Up/down arrows | Phosphor | 16px |
| Icon theo chủ đề | Phosphor | 20px |

## 3. Cấu trúc bento grid (12 col, gap 16px)

```
┌──────────────┬──────────────┬──────────────┐
│              │              │              │
│  Cell 1      │  Cell 2      │  Cell 3      │
│  (col 1-4)   │  (col 5-8)   │  (col 9-12)  │
│  HERO        │  TREND       │  TOP         │
│  Average     │  Forecast    │  Areas       │
│  price       │  2026        │  investment  │
│  big chart   │  sparkline   │  mini list   │
│              │              │              │
├──────────────┴──────────────┴──────────────┘
│                                              │
│  Cell 4 (col 1-6)        Cell 5 (col 7-12)  │
│  Rental yield             Map hotspots       │
│  horizontal bars          aerial + pins      │
│                                              │
└──────────────────────────────────────────────┘
```

## 4. Cell anatomy

### Cell 1 — Average price (HERO)

```
┌────────────────────────────────────┐
│ GIÁ TRUNG BÌNH TOÀN QUỐC         │ ← eyebrow
│                                    │
│ 32,5 triệu/m²                     │ ← big number 56px
│                                    │
│ ↑ 12,4% YoY                        │ ← trend indicator
│                                    │
│ [▮▮▮▮▮▮▮▮▮▯] 12 tháng             │ ← mini bar chart
│                                    │
│ 4 quý qua · Cập nhật 5/7/2026     │ ← timestamp
└────────────────────────────────────┘
```

### Cell 2 — Forecast 2026

```
┌────────────────────────────────────┐
│ DỰ BÁO TĂNG GIÁ 2026              │
│                                    │
│ Q1   Q2   Q3   Q4                  │
│ ╱╲   ╱╲                          │ ← sparkline SVG
│   ╲_╱   ╲╱╲                       │
│                                    │
│ +8,2% đến +15,7%                  │
│ theo khu vực                       │
└────────────────────────────────────┘
```

### Cell 3 — Top đầu tư

```
┌────────────────────────────────────┐
│ TOP KHU VỰC ĐẦU TƯ                │
│                                    │
│ 1. Thủ Đức  ROI 6,8%              │
│ 2. Bình Thạnh ROI 6,2%             │
│ 3. Quận 7    ROI 5,9%             │
│ 4. Long Biên ROI 5,7%             │
│ 5. Gò Vấp   ROI 5,4%             │
│                                    │
│ [Xem tất cả →]                    │
└────────────────────────────────────┘
```

### Cell 4 — Rental yield

```
┌────────────────────────────────────┐
│ TỶ SUẤT CHO THUÊ TRUNG BÌNH       │
│                                    │
│ Căn hộ     ▮▮▮▮▮▮▮▯ 5,8%        │
│ Nhà phố    ▮▮▮▮▮▮▮▮ 6,4%        │
│ Biệt thự   ▮▮▮▮▮▯     4,9%        │
│ Shophouse  ▮▮▮▮▮▮▮▮▮ 7,2%        │
│ Đất nền    ▮▮▮▮▮▮▮    5,5%        │
└────────────────────────────────────┘
```

### Cell 5 — Map hotspots

```
┌────────────────────────────────────┐
│ ĐIỂM NÓNG THANH KHOẢN             │
│                                    │
│ [aerial map with 8 red pins]      │
│  ● HCM: 12.480 tin                 │
│  ● HN: 8.920 tin                   │
│  ● ĐN: 3.640 tin                   │
│  ● NT: 2.180 tin                   │
└────────────────────────────────────┘
```

## 5. Variants

| Variant | Use |
|---|---|
| `default` | Homepage section 5 |
| `compact` | Sidebar widget trong listing detail (3 cells) |
| `expanded` | Dedicated `/insights` page (10+ cells) |

## 6. Code reference (default)

```tsx
<section className="bg-slate-50 py-16 lg:py-24" aria-labelledby="insights-heading">
  <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    {/* Header */}
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

    {/* Bento grid */}
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-12 gap-4">
      {/* Cell 1 — Average price (hero, col 1-4) */}
      <article className="lg:col-span-4 bg-white rounded-2xl border border-slate-200 p-6 hover:shadow-lg transition-shadow">
        <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500">
          Giá trung bình toàn quốc
        </span>
        <p className="mt-3 text-[44px] lg:text-[56px] font-extrabold text-slate-900 leading-none tabular-nums tracking-tight">
          32,5<span className="text-[24px] text-slate-500 font-bold"> triệu/m²</span>
        </p>
        <div className="mt-3 inline-flex items-center gap-1 px-2 py-0.5 bg-emerald-50 text-emerald-700 rounded-full text-[12px] font-bold">
          <Phosphor.TrendUp size={12} weight="bold" />
          +12,4% YoY
        </div>
        <BarChart data={monthlyPrices} className="mt-6" />
        <p className="mt-3 text-[11px] text-slate-500">
          4 quý qua · Cập nhật 5/7/2026 · Nguồn Anchor Pro Index
        </p>
      </article>

      {/* Cell 2 — Forecast (col 5-8) */}
      <article className="lg:col-span-4 bg-slate-900 text-white rounded-2xl p-6 hover:shadow-lg transition-shadow">
        <span className="text-[11px] font-bold uppercase tracking-wider text-teal-300">
          Dự báo tăng giá 2026
        </span>
        <p className="mt-3 text-[28px] font-extrabold leading-tight">
          +8,2% đến +15,7%<br />
          <span className="text-[14px] font-normal text-slate-300">theo khu vực và phân khúc</span>
        </p>
        <Sparkline data={forecastData} className="mt-6" color="#2dd4bf" />
        <div className="mt-6 grid grid-cols-4 gap-2 text-center text-[11px]">
          {['Q1', 'Q2', 'Q3', 'Q4'].map(q => (
            <div key={q} className="text-slate-400">{q}</div>
          ))}
        </div>
      </article>

      {/* Cell 3 — Top areas (col 9-12) */}
      <article className="lg:col-span-4 bg-white rounded-2xl border border-slate-200 p-6 hover:shadow-lg transition-shadow">
        <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500">
          Top khu vực đầu tư
        </span>
        <ul className="mt-4 space-y-2.5">
          {topAreas.map((area, i) => (
            <li key={area.name} className="flex items-center gap-3 text-[13px]">
              <span className="w-6 h-6 rounded-full bg-slate-100 text-slate-700 font-bold text-[11px] flex items-center justify-center tabular-nums">
                {i + 1}
              </span>
              <span className="flex-1 font-semibold text-slate-900">{area.name}</span>
              <span className="text-emerald-600 font-bold tabular-nums">{area.roi}%</span>
            </li>
          ))}
        </ul>
        <a href="/insights/top-areas" className="mt-5 inline-flex items-center gap-1 text-[12px] font-semibold text-teal-600 hover:text-teal-700">
          Xem 50 khu vực
          <Phosphor.ArrowRight size={12} weight="bold" />
        </a>
      </article>

      {/* Cell 4 — Rental yield (col 1-6) */}
      <article className="lg:col-span-6 bg-white rounded-2xl border border-slate-200 p-6 hover:shadow-lg transition-shadow">
        <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500">
          Tỷ suất cho thuê trung bình
        </span>
        <div className="mt-5 space-y-3">
          {rentalYields.map(item => (
            <div key={item.type} className="flex items-center gap-3">
              <span className="w-24 text-[13px] font-medium text-slate-700">{item.type}</span>
              <div className="flex-1 h-2 bg-slate-100 rounded-full overflow-hidden">
                <div className="h-full bg-teal-500 rounded-full" style={{ width: `${item.percent}%` }} />
              </div>
              <span className="w-14 text-right text-[13px] font-bold text-slate-900 tabular-nums">
                {item.yield}%
              </span>
            </div>
          ))}
        </div>
      </article>

      {/* Cell 5 — Map hotspots (col 7-12) */}
      <article className="lg:col-span-6 bg-white rounded-2xl border border-slate-200 overflow-hidden hover:shadow-lg transition-shadow">
        <div className="p-6 pb-3">
          <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500">
            Điểm nóng thanh khoản
          </span>
          <p className="mt-2 text-[15px] text-slate-700">
            Hơn 24.000 giao dịch thành công trong quý này
          </p>
        </div>
        <div className="relative aspect-[16/9] bg-slate-100">
          <img
            src="https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=800&h=450&fit=crop&q=80"
            alt="Bản đồ Việt Nam"
            className="w-full h-full object-cover"
          />
          {/* Pin overlays */}
          <div className="absolute top-[40%] left-[45%] -translate-x-1/2 -translate-y-full">
            <MapPinCard city="TP.HCM" count="12.480" />
          </div>
          <div className="absolute top-[20%] left-[55%] -translate-x-1/2 -translate-y-full">
            <MapPinCard city="Hà Nội" count="8.920" />
          </div>
          {/* ...more pins */}
        </div>
      </article>
    </div>
  </div>
</section>
```

## 7. Chart components

`BarChart`, `Sparkline`, `MapPinCard` là pure SVG/HTML components, không third-party. Implementation:

- `BarChart`: array of `{month: string, value: number}`, render rect elements với fill teal gradient
- `Sparkline`: array of numbers, render polyline với stroke teal, area fill gradient
- `MapPinCard`: absolute positioned div với pulse animation

## 8. Accessibility

- Mỗi cell là `<article>` với heading (sr-only hoặc visible eyebrow)
- Số liệu tabular-nums để screen reader đọc đúng
- Charts có text alternative ngay trong cell (không cần hover)
- Reduced motion: disable pulse/pulse animation trên pins
- Color contrast: dark cell (slate-900) với white text 18:1

## 9. Performance

- Tất cả chart inline SVG, không load chart library
- Map image lazy load
- Bento grid dùng CSS Grid (không tính toán JS)
- Re-render tối đa khi data thay đổi (memo)