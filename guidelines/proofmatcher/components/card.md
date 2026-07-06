# Card Component

> Container cho nội dung nhóm. Bốn biến thể: template (marketplace), docs-feature, code-example, testimonial. Linear-style dark theme, hierarchy qua border và shadow chứ không phải surface contrast.

## 1. Mục đích

Container chính cho marketplace grid, docs feature lists, code blocks, và testimonials. Card phải recede để content chiếm ưu thế.

## 2. Hệ thống icon

| Vai trò | Icon Phosphor | Kích thước |
|---|---|---|
| Icon đầu feature card | `Star`, `Compass`, `BookOpen`, `Lightning`, `Shield`, `Rocket`, `Code`, `Stack` (tùy loại) | 24×24px trong vòng tròn 40×40 nền surface.strong |
| Category icon (template) | `Browser`, `ShoppingBag`, `Briefcase`, `Heartbeat`, `GraduationCap`, `AirplaneTilt` | 14px trên eyebrow |
| Preview indicator | `Eye` | 14px trên preview overlay |
| Source code link | `Code` | 14px |
| Bookmark template | `BookmarkSimple` | 16px |
| Download template | `DownloadSimple` | 14px |
| Verified | `SealCheck` (fill) | 12px, mint |
| New | `Sparkle` (fill) | 11px, mint |
| Featured | `Star` (fill) | 12px |
| Loading | `CircleNotch` | 16px |

## 3. Hình ảnh và minh họa

Đây là nơi template marketplace khoe hình ảnh thật. Mỗi template card có preview image thật:

### Template card previews

| Category | Preview type | Nguồn |
|---|---|---|
| SaaS Landing | Dashboard screenshot | `https://picsum.photos/seed/saas-dashboard-1/640/400` |
| Agency | Hero portfolio | `https://picsum.photos/seed/agency-portfolio/640/400` |
| Health | Clinic interface | `https://picsum.photos/seed/health-clinic-ui/640/400` |
| Education | LMS dashboard | `https://picsum.photos/seed/edu-lms-dashboard/640/400` |
| Travel | Travel booking | `https://picsum.photos/seed/travel-booking-ui/640/400` |
| Restaurant | Menu showcase | `https://picsum.photos/seed/restaurant-menu-ui/640/400` |
| Real Estate | Listings grid | `https://picsum.photos/seed/real-estate-listings/640/400` |
| Portfolio | Designer portfolio | `https://picsum.photos/seed/designer-portfolio/640/400` |

Preview dùng `loading="lazy"`, `aspect-ratio: 16/10`, placeholder background `color.surface.strong` với skeleton shimmer khi loading.

### Docs-feature card icons

Mỗi docs feature có một Phosphor icon trong vòng tròn nền:

```tsx
<div class="w-10 h-10 rounded-full bg-[#0d0d0d] border border-[rgba(255,255,255,0.08)] flex items-center justify-center">
  <Phosphor.Lightning size={20} weight="bold" class="text-white" aria-hidden="true" />
</div>
```

### Testimonial avatars

Avatar 40×40px bo tròn, dùng Picsum: `https://picsum.photos/seed/portrait-founder-1/80/80`.

## 4. Cấu trúc

### Template card

```
┌────────────────────────────────┐
│  [preview image / iframe]      │
│                                │
├────────────────────────────────┤
│  CATEGORY · 6 pages · 248KB    │
│                                │
│  Template Title                │
│  Short tagline                  │
│                                │
│  [tag] [tag] [tag]             │
│                                │
│  [Preview] [Source]            │
└────────────────────────────────┘
```

### Docs-feature card

```
┌────────────────────────────────┐
│  [icon]                        │
│  Title                         │
│  Description prose             │
└────────────────────────────────┘
```

### Code-example card

```
┌────────────────────────────────┐
│  [filename]      [Copy]        │
├────────────────────────────────┤
│  <pre><code>...</code></pre>   │
└────────────────────────────────┘
```

### Testimonial card

```
┌────────────────────────────────┐
│  [ portrait 40×40 ]            │
│                                │
│  ★★★★★                          │
│  "Quote text..."                │
│                                │
│  Name · Role · Company         │
└────────────────────────────────┘
```

## 5. Biến thể

| Variant | Padding | Radius | Background | Cách dùng |
|---|---|---|---|---|
| `template` | `space.5` (20) | `radius.xs` (12) | `color.surface.raised` | Marketplace grid |
| `docs-feature` | `space.6` (20) | `radius.xs` (12) | `color.surface.raised` | Docs feature lists |
| `code-example` | none | `radius.md` (6) | `color.surface.strong` | Code blocks |
| `inline` (compact) | `space.4` (12) | `radius.xs` (12) | `color.surface.raised` | Inline references, sidebar items |
| `testimonial` | `space.6` (24) | `radius.xs` (12) | `color.surface.raised` | Quote cards |

## 6. Sizes

Card sizes xác định bởi grid column width, không phải fixed size token. Dùng responsive grid rules:

- Desktop ≥1280px: 3 columns, gap `space.6`
- Tablet 768–1279px: 2 columns, gap `space.6`
- Mobile <768px: 1 column, gap `space.5`

## 7. Trạng thái

| Trạng thái | Background | Border | Transform | Shadow |
|---|---|---|---|---|
| `default` | `color.surface.raised` | 1px `rgba(255,255,255,0.08)` | none | none |
| `hover` | `color.surface.strong` | 1px `color.border.default` | `translateY(-2px)` | `shadow.1` |
| `focus-within` | `color.surface.strong` | 1px `color.border.default` | none | none |
| `selected` | `color.surface.strong` | 2px `color.border.strong` | none | none |
| `disabled` | `color.surface.raised` | 1px `rgba(255,255,255,0.04)` | none | none, opacity 0.6 |
| `loading` | `color.surface.raised` | 1px `rgba(255,255,255,0.08)` | none | skeleton shimmer bên trong |

## 8. Template card specifics

- Preview area: aspect-ratio 16/10. Image lazy-loaded với `loading="lazy"`. Hiển thị overlay hover với `Eye` icon + "Preview" text.
- Categories displayed như `font.size.sm` (11px) uppercase eyebrow với category icon Phosphor.
- Title `font.size.h3` (22px) hoặc `font.size.h2` (24px) cho hero card.
- Tagline `font.size.2xl` (15px).
- Tags: max 3 hiển thị, ellipsis nếu nhiều hơn. Mỗi tag dùng Phosphor icon nhỏ (12px) + text.
- Actions: 2 buttons cạnh nhau (`Preview` primary, `Source` ghost) hoặc CTA lớn khi card là featured.
- Click anywhere trên card navigate tới template detail (ngoại trừ khi click buttons hoặc links bên trong).

## 9. Docs-feature card specifics

- Icon 24×24px trong vòng tròn 40×40 nền `color.surface.strong`, viền `rgba(255,255,255,0.08)`.
- Title `font.size.h4` (20px).
- Description `font.size.xl` (14px), `color.text.secondary`.
- Optional link dưới: `font.size.lg` (13px) arrow link với `ArrowUpRight` icon.

## 10. Code-example card specifics

- Filename bar: `font.size.sm` (11px) monospace, copy button bên phải với `Copy` icon.
- Code block: `<pre><code>` với monospace font, syntax highlighting qua Shiki hoặc Prism.
- Copy button: ghost variant, 32px height.
- Long code: horizontal scroll bên trong `<pre>`, không phải card.
- Line numbers: optional, trong `color.text.tertiary`, `font-variant-numeric: tabular-nums`.

## 11. Testimonial card specifics

- Avatar 40×40px bo tròn (Picsum).
- Star rating: 5 Phosphor `Star` (fill) icons màu vàng `#fbbf24`, hoặc partial star cho rating không tròn.
- Quote: `font.size.lg` (15px) italic.
- Attribution: name + role + company, monospace 11px uppercase tracking.
- Verified badge: `SealCheck` (fill) mint nếu có.

## 12. Empty state

Khi grid không có items, show composed empty state trong section, không trong card:

- Centered icon (40×40px) `color.text.tertiary`. dùng Phosphor `FunnelX` hoặc `MagnifyingGlass` với `Slash`.
- Title `font.size.h3` (22px).
- Description `font.size.2xl` (15px), `color.text.secondary`.
- Optional action button.

## 13. Loading skeleton

- Cùng dimensions với final card.
- Shimmer animation ở `motion.duration.normal`.
- `aria-busy="true"` trên card.
- Stop animation khi content load.

## 14. Responsive

- Mọi breakpoint, card padding scale theo grid gap.
- <480px: card padding giảm xuống `space.4` (12px).
- ≥1280px: cards giữ 3-column grid với consistent height (dùng `display: grid; grid-template-rows: 1fr auto` cho equal action row alignment).

## 15. Edge cases

- **Long title**: truncate ở 2 dòng với `text-overflow: ellipsis`. Title max-height: 2 dòng.
- **Long description**: truncate ở 3 dòng.
- **Missing preview image**: show placeholder block với category icon Phosphor lớn (32×32) ở giữa, màu tertiary.
- **No tags**: ẩn tag row, giảm card padding bottom.
- **Filter mismatch**: cards animate out (`opacity` + `transform: scale(0.95)`) ở `motion.duration.fast`, rồi `display: none` sau animation.

## 16. Accessibility

- Card tự nó không interactive trừ khi `link-whole-card` variant. Khi đó toàn card wrap trong `<a>`, mọi inner interactive elements bị xóa (không nested buttons hoặc links).
- Buttons bên trong card (Preview, Source) giữ individually focusable.
- Card có `<article>` hoặc `<section>` semantic role.
- Loading state: `aria-busy="true"`.
- Focus order: title → tags → Preview → Source.
- Color contrast cho mọi text đạt WCAG AA.

## 17. QA acceptance criteria

```
[ ] Padding matches variant token
[ ] Radius matches variant token
[ ] Hover lifts -2px với shadow
[ ] Focus-within state visible (whole-card link variant)
[ ] Empty state renders khi filter không có results
[ ] Loading skeleton matches final dimensions
[ ] Long titles truncate ở 2 dòng
[ ] Long descriptions truncate ở 3 dòng
[ ] Click area consistent qua card body (không buttons)
[ ] Tag row ẩn khi không có tags
[ ] Code block scroll horizontal bên trong, không card
[ ] Touch target ≥44×44px trên mọi buttons
[ ] Template card có preview image thật (Picsum seed), không div giả
[ ] Testimonial card có avatar thật
[ ] axe-core: 0 violations
```

## 18. Code reference

```tsx
{/* Template card với preview image thật */}
<article
  class="group bg-[#050505] border border-[rgba(255,255,255,0.08)] rounded-xl overflow-hidden hover:border-[#e5e7eb] hover:-translate-y-0.5 hover:shadow-[0_8px_24px_rgba(0,0,0,0.4)] focus-within:border-[#e5e7eb] transition-all duration-200"
  aria-busy={isLoading}
>
  <div class="relative aspect-[16/10] overflow-hidden bg-[#0d0d0d]">
    <img
      src="https://picsum.photos/seed/saas-dashboard-1/640/400"
      alt="SaaS dashboard template preview"
      class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
      loading="lazy"
    />
    {/* Hover overlay */}
    <div class="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity duration-200 flex items-center justify-center">
      <button class="inline-flex items-center gap-2 px-4 py-2 bg-white text-black rounded-md font-medium text-sm">
        <Phosphor.Eye size={14} weight="bold" aria-hidden="true" />
        Preview
      </button>
    </div>
    {/* Badges */}
    {isNew && (
      <div class="absolute top-3 left-3 inline-flex items-center gap-1 px-2 py-1 bg-black/70 backdrop-blur rounded-full">
        <Phosphor.Sparkle size={10} weight="fill" class="text-[#34d399]" aria-hidden="true" />
        <span class="font-mono text-[10px] uppercase tracking-wider text-[#34d399]">New</span>
      </div>
    )}
    {isFeatured && (
      <div class="absolute top-3 right-3 inline-flex items-center gap-1 px-2 py-1 bg-black/70 backdrop-blur rounded-full">
        <Phosphor.Star size={10} weight="fill" class="text-white" aria-hidden="true" />
        <span class="font-mono text-[10px] uppercase tracking-wider text-white">Featured</span>
      </div>
    )}
  </div>

  <div class="p-5">
    <div class="flex items-center gap-2 font-mono text-[11px] uppercase tracking-[0.06em] text-[#737373]">
      <Phosphor.Browser size={12} weight="bold" aria-hidden="true" />
      <span>SaaS</span>
      <span aria-hidden="true">·</span>
      <span>6 pages</span>
      <span aria-hidden="true">·</span>
      <span>248KB</span>
    </div>
    <h3 class="mt-2 text-[20px] font-semibold text-white leading-tight">
      Aurora Dashboard Kit
    </h3>
    <p class="mt-1.5 text-[14px] text-[#a1a1aa] leading-relaxed line-clamp-2">
      A complete dashboard system with 6 pages, dark mode, and 40+ components.
    </p>
    <div class="mt-4 flex flex-wrap items-center gap-1.5">
      <span class="inline-flex items-center gap-1 px-2 py-0.5 bg-[#0d0d0d] border border-[rgba(255,255,255,0.08)] rounded-full font-mono text-[10.5px] text-[#a1a1aa]">
        <Phosphor.Lightning size={10} weight="bold" aria-hidden="true" />
        React
      </span>
      <span class="inline-flex items-center gap-1 px-2 py-0.5 bg-[#0d0d0d] border border-[rgba(255,255,255,0.08)] rounded-full font-mono text-[10.5px] text-[#a1a1aa]">
        <Phosphor.Palette size={10} weight="bold" aria-hidden="true" />
        Tailwind
      </span>
      <span class="inline-flex items-center gap-1 px-2 py-0.5 bg-[#0d0d0d] border border-[rgba(255,255,255,0.08)] rounded-full font-mono text-[10.5px] text-[#a1a1aa]">
        <Phosphor.Moon size={10} weight="bold" aria-hidden="true" />
        Dark mode
      </span>
    </div>
    <div class="mt-5 flex items-center gap-2">
      <button class="flex-1 inline-flex items-center justify-center gap-1.5 px-3 py-2 bg-white text-black rounded-md text-[13px] font-medium hover:-translate-y-px transition-transform duration-150">
        <Phosphor.Eye size={13} weight="bold" aria-hidden="true" />
        Preview
      </button>
      <button class="flex-1 inline-flex items-center justify-center gap-1.5 px-3 py-2 bg-transparent text-white border border-[#e5e7eb] rounded-md text-[13px] font-medium hover:border-[#fafafa] transition-colors duration-150">
        <Phosphor.Code size={13} weight="bold" aria-hidden="true" />
        Source
      </button>
    </div>
  </div>
</article>

{/* Docs-feature card với icon trong vòng tròn */}
<article class="bg-[#050505] border border-[rgba(255,255,255,0.08)] rounded-xl p-6 hover:border-[#e5e7eb] transition-colors duration-200">
  <div class="w-10 h-10 rounded-full bg-[#0d0d0d] border border-[rgba(255,255,255,0.08)] flex items-center justify-center mb-4">
    <Phosphor.Lightning size={20} weight="bold" class="text-white" aria-hidden="true" />
  </div>
  <h3 class="text-[18px] font-semibold text-white">Zero-config setup</h3>
  <p class="mt-2 text-[14px] text-[#a1a1aa] leading-relaxed">
    Drop in the snippet, paste your tokens, ship in 5 minutes. No build pipeline required.
  </p>
  <a href="/docs/setup" class="mt-4 inline-flex items-center gap-1 text-[13px] text-white hover:underline">
    Read the setup guide
    <Phosphor.ArrowUpRight size={12} weight="bold" aria-hidden="true" />
  </a>
</article>

{/* Testimonial card với avatar thật */}
<article class="bg-[#050505] border border-[rgba(255,255,255,0.08)] rounded-xl p-6">
  <div class="flex items-start gap-3">
    <img src="https://picsum.photos/seed/portrait-founder-1/80/80" alt="" aria-hidden="true" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(255,255,255,0.1)]" />
    <div class="flex-1 min-w-0">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-0.5 text-[#fbbf24]" aria-label="Đánh giá 5 trên 5 sao">
          {[1, 2, 3, 4, 5].map(i => <Phosphor.Star key={i} size={13} weight="fill" aria-hidden="true" />)}
        </div>
        <span class="inline-flex items-center gap-1 font-mono text-[10px] uppercase tracking-wider text-[#34d399]">
          <Phosphor.SealCheck size={10} weight="fill" aria-hidden="true" />
          Verified
        </span>
      </div>
      <Phosphor.Quotes size={20} weight="fill" class="text-[#737373] opacity-40 mt-3 mb-1" aria-hidden="true" />
      <blockquote class="text-[14px] text-[#a1a1aa] italic leading-relaxed">
        "Cut our landing-page timeline from 3 days to 4 hours. The token system alone is worth the price."
      </blockquote>
      <footer class="mt-4 pt-3 border-t border-[rgba(255,255,255,0.06)] flex items-center justify-between">
        <span class="font-mono text-[10.5px] uppercase tracking-wider text-[#737373]">
          Mira K. · Founder, Linear-like Co
        </span>
      </footer>
    </div>
  </div>
</article>
```