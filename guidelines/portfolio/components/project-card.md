# Project Card

> Card cho một case study trong work index. Asymmetric grid, large photo, minimal chrome.

## 1. Mục đích

Hiển thị case study trong asymmetric masonry grid. Phải cho phép ảnh thật của work tỏa sáng, không cạnh tranh với typography.

## 2. Icon system

Phosphor Regular, minimal.

| Role | Icon | Size |
|---|---|---|
| External | `ArrowUpRight` | 16px |
| Year label | (mono, no icon) | 11px |
| Client label | (mono, no icon) | 11px |
| View case | `ArrowRight` | 14px |

## 3. Hình ảnh

| Element | Source |
|---|---|
| Project hero | `https://picsum.photos/seed/portfolio-{slug}/1200/750` |
| Client logo | Simple Icons (slack, figma, linear, stripe, etc.) |

## 4. Cấu trúc

```
┌──────────────────────────────────────┐
│                                      │
│  [project hero photo, varied aspect] │
│                                      │
│                                      │
├──────────────────────────────────────┤
│  2024                                │ ← year (mono)
│  Stripe                              │ ← client (mono, gray)
│  Dashboard redesign                  │ ← title (Instrument Serif 28.5)
│  Role · Lead Designer                │ ← role (12px)
│                  → Read case study   │ ← CTA arrow
└──────────────────────────────────────┘
```

## 5. Variants

| Variant | Aspect | Use |
|---|---|---|
| `wide` | 16:9 | Top feature |
| `standard` | 4:3 | Mid-grid |
| `tall` | 3:4 | Side column |
| `square` | 1:1 | Small accent |

Asymmetric grid: `grid-cols-12` with cells spanning `col-span-6` (wide) or `col-span-4` (standard).

## 6. States

| State | Visual |
|---|---|
| default | base |
| hover | image scale 1.03, title underline reveal |
| focus-within | outline 1px accent red on title link |

## 7. Code reference

```tsx
<article class="group">
  <a href={`/work/${slug}`} class="block focus:outline-none">
    <div class="relative overflow-hidden bg-[#fafafa]">
      <div class="aspect-[16/9]">
        <img
          src={`https://picsum.photos/seed/portfolio-${slug}/1200/675`}
          alt={`${title} hero`}
          class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-[1.03]"
          loading="lazy"
        />
      </div>
    </div>
    <div class="mt-6 flex items-start justify-between gap-4">
      <div class="min-w-0 flex-1">
        <div class="flex items-center gap-3 font-mono text-[11px] uppercase tracking-wider text-[#a3a3a3]">
          <span>{year}</span>
          <span class="text-[#0a0a0a]/20">·</span>
          <span>{client}</span>
        </div>
        <h3 class="mt-2 font-display text-[28.5px] leading-[1.1] text-[#0a0a0a]">
          {title}
        </h3>
        <p class="mt-1 text-[13px] text-[#525252]">{role}</p>
      </div>
      <span class="shrink-0 inline-flex items-center gap-1 text-[12px] text-[#0a0a0a] group-hover:text-[#dc2626] transition-colors">
        Read case
        <Phosphor.ArrowUpRight size={14} weight="regular" class="transition-transform duration-300 group-hover:translate-x-0.5 group-hover:-translate-y-0.5" aria-hidden="true" />
      </span>
    </div>
  </a>
</article>
```