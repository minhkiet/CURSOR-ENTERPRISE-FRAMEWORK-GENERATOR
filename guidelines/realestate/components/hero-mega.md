# Mega Hero with Search Overlay

> Hero section trang chủ Anchor Pro. Video background, gradient overlay, search widget floating, trust strip. Đây là section đầu tiên khách thấy và quyết định ở lại hay rời đi.

## 1. Mục đích

Hero 16:9 với video/ảnh chất lượng cao làm nền. Search widget nổi bật phía dưới. Trust signals inline. CTA rõ ràng. Toàn bộ section phải truyền tải "đây là web BDS chuyên nghiệp, có video thật, có pháp lý minh bạch".

## 2. Asset

| Element | Source | Kích thước |
|---|---|---|
| Video background | `https://cdn.coverr.co/videos/coverr-{slug}/1080p.mp4` (xem assets/unsplash-curated.json) | 1920x1080 MP4 |
| Video poster (fallback) | Unsplash `1564013799919-ab600027ffc6` | 1920x1080 |
| Search icons | Phosphor | 16-20px |
| Trust badge icons | Phosphor | 18px |

## 3. Cấu trúc

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│  [video bg 16:9 + dark gradient overlay]                 │
│                                                          │
│  ┌─ Eyebrow ─────────────────────────────────────────┐  │
│  │ ✦ SÀN BĐS ĐÃ XÁC MINH · 50.000+ TIN ĐANG ĐĂNG  │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  Tìm ngôi nhà                                            │
│  đáng sống nhất                                          │ ← 96px hero
│                                                          │
│  50.000+ tin BĐS đã xác minh pháp lý, video 360°         │
│  và walkthrough thật 100% từ chủ nhà.                    │ ← 18px subtitle
│                                                          │
│  [🔍 Tìm ngay]  [▶ Xem video 2 phút]                    │ ← 2 CTAs
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Search Widget (floating)                          │  │
│  │  ┌──────────┬──────────┬──────────┬──────────┐    │  │
│  │  │ Loại BĐS │ Khu vực  │ Giá      │ DT       │    │  │
│  │  │ [select] │ [select] │ [range]  │ [range]  │    │  │
│  │  └──────────┴──────────┴──────────┴──────────┘    │  │
│  │            [🔍 Tìm 50.832 tin]                     │  │
│  └──────────────────────────────────────────────────┘  │
│                                                          │
│  ✓ 4.8★/5 (12.480 đánh giá)  ·  50.000+ tin             │
│  ✓ Pháp lý minh bạch  ·  1.200+ môi giới verified      │
└──────────────────────────────────────────────────────────┘
```

## 4. Variants

| Variant | Use | Khác biệt |
|---|---|---|
| `home` | Homepage | Full video, search widget floating, trust strip |
| `search` | Search results page | Solid image (no video), search widget sticky on top |
| `project` | Project landing | Video project + breadcrumb + CTA "Đăng ký tư vấn" |
| `compact` | Mobile-first focused | Image static, search widget full-width, no trust strip |

## 5. States

| State | Visual |
|---|---|
| default | Video playing muted, search widget visible |
| video-loaded | Video plays in loop, poster hidden |
| video-failed | Falls back to poster image (Unsplash) |
| search-focused | Widget elevates with shadow, fields highlight teal |
| scrolled | Search widget detaches, becomes sticky bar |

## 6. Animation

- Video: autoplay, muted, loop, playsInline. NO controls visible.
- Gradient overlay: dark navy → transparent, opacity 70% top → 90% bottom
- Search widget: fade-in 400ms sau khi hero mount, slide up 20px → 0
- Hero text: stagger fade-up 100ms intervals (eyebrow → headline → subtext → CTA)
- Reduced-motion: video replaced by static poster, no slide-up

## 7. Code reference (default variant)

```tsx
<section className="relative w-full bg-slate-900 overflow-hidden" aria-label="Tìm kiếm bất động sản">
  {/* Video/Image background */}
  <div className="absolute inset-0">
    <video
      autoPlay
      muted
      loop
      playsInline
      poster="https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=1920&h=1080&fit=crop&q=80"
      className="w-full h-full object-cover"
    >
      <source src="https://cdn.coverr.co/videos/coverr-aerial-view-of-modern-buildings-in-hong-kong-3695/1080p.mp4" type="video/mp4" />
    </video>
    {/* Gradient overlay */}
    <div className="absolute inset-0 bg-gradient-to-b from-slate-900/70 via-slate-900/50 to-slate-900/90" aria-hidden="true" />
  </div>

  {/* Content */}
  <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-32 lg:pt-28 lg:pb-40">
    {/* Eyebrow */}
    <div className="inline-flex items-center gap-2 px-3 py-1.5 bg-teal-500/20 backdrop-blur border border-teal-400/30 rounded-full text-teal-300 text-[11px] font-bold uppercase tracking-wider mb-6">
      <Phosphor.SealCheck size={14} weight="fill" />
      Sàn BĐS đã xác minh · 50.000+ tin đang đăng
    </div>

    {/* Headline */}
    <h1 className="text-white text-[44px] sm:text-[64px] lg:text-[88px] font-extrabold leading-[1.05] tracking-tight max-w-4xl">
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
        Tìm ngay
      </a>
      <a href="/about/video" className="inline-flex items-center gap-2 px-6 py-3.5 bg-white/10 backdrop-blur hover:bg-white/20 text-white font-semibold rounded-xl border border-white/20 transition-colors">
        <Phosphor.PlayCircle size={18} weight="fill" />
        Xem video 2 phút
      </a>
    </div>

    {/* Trust strip inline */}
    <div className="mt-10 flex flex-wrap items-center gap-x-6 gap-y-2 text-white/75 text-[13px]">
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

  {/* Floating Search Widget */}
  <div id="search" className="relative max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 -mt-16 lg:-mt-20 mb-12 z-10">
    <SearchWidget />
  </div>
</section>
```

## 8. SearchWidget sub-component

```tsx
function SearchWidget() {
  return (
    <div className="bg-white rounded-2xl shadow-2xl border border-slate-200 p-4 lg:p-5">
      {/* Tabs */}
      <div className="flex items-center gap-1 mb-4 border-b border-slate-100">
        {[
          { id: 'buy', label: 'Mua bán', icon: 'House' },
          { id: 'rent', label: 'Cho thuê', icon: 'Key' },
          { id: 'project', label: 'Dự án', icon: 'Buildings' },
          { id: 'agent', label: 'Môi giới', icon: 'UserCircle' }
        ].map(tab => (
          <button
            key={tab.id}
            className={cx(
              "flex items-center gap-1.5 px-4 py-2.5 text-[13px] font-semibold border-b-2 -mb-px transition-colors",
              activeTab === tab.id
                ? "border-teal-500 text-teal-700"
                : "border-transparent text-slate-600 hover:text-slate-900"
            )}
          >
            <Phosphor[tab.icon] size={16} weight="bold" />
            {tab.label}
          </button>
        ))}
      </div>

      {/* Fields */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3 mb-3">
        <SelectField label="Loại BĐS" placeholder="Căn hộ, nhà phố..." icon="House" />
        <SelectField label="Khu vực" placeholder="Quận, tỉnh thành" icon="MapPin" />
        <RangeField label="Mức giá" placeholder="Bất kỳ" />
        <RangeField label="Diện tích" placeholder="Bất kỳ" />
      </div>

      {/* CTA row */}
      <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
        <button className="text-[13px] font-semibold text-teal-600 hover:text-teal-700 inline-flex items-center gap-1">
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
```

## 9. Accessibility

- Video: `aria-hidden="true"` vì purely decorative; poster image thay thế khi reduced-motion
- Headline: dùng `<h1>`, không span lớn rồi pseudo-heading
- Search widget: form đúng semantic với `<label>` cho mỗi field
- CTAs: `<a>` cho navigation, `<button>` cho action (filter)
- Focus: search fields có `focus:ring-2 focus:ring-teal-500 focus:ring-offset-2`
- Touch targets: tất cả buttons ≥ 44px height
- Screen reader: hero text đọc được, video được bỏ qua
- Color contrast: white text trên dark gradient đạt 8:1+

## 10. Performance

- Video: preload="metadata", không preload="auto"
- Poster image: 1920x1080 max, dùng `srcset` 1280/1920
- Hero text render ngay khi poster load (LCP-friendly)
- Search widget không có third-party JS
- Lazy load video play button overlay (chỉ hover)