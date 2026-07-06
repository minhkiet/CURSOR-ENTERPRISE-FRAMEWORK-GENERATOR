# Article Card

> Card cho một article trong grid hoặc list. Đọc như một broadsheet clipping: ảnh editorial trên đầu, headline + dek dưới.

## 1. Mục đích

Hiển thị article trong topic grid, related-article list, hoặc author bibliography.

## 2. Icon system

| Role | Icon Phosphor | Size |
|---|---|---|
| Topic tag | `Tag` | 11px |
| Reading time | `Clock` | 11px |
| Bookmark | `BookmarkSimple` | 16px |
| Share | `ShareNetwork` | 14px |
| Author | `UserCircle` | 12px |
| Audio available | `SpeakerHigh` | 11px |
| External link | `ArrowUpRight` | 12px |

## 3. Hình ảnh

| Section | Image | Source |
|---|---|---|
| Article hero | Black-and-white photo | `https://picsum.photos/seed/editorial-bw-{slug}/800/500` |
| Topic card | Topic illustration | `https://picsum.photos/seed/topic-{tech|culture|design|science|longread}/600/400` |
| Author portrait | Editorial headshot | `https://picsum.photos/seed/author-portrait-{n}/200/200` |

Photo treatment: `filter: grayscale(0.6) contrast(1.05)`. Hover desaturates to 0.3.

## 4. Cấu trúc

```
┌────────────────────────────────────┐
│  [article photo 16/10]            │
├────────────────────────────────────┤
│  TECH · 8 MIN READ                 │ ← eyebrow mono uppercase
│                                    │
│  The Last Days of the Slow Web    │ ← headline (24px Newsreader 500)
│  A meditation on patience and the │ ← dek (15px Newsreader 400)
│  architecture of attention.        │
│                                    │
│  ────                              │
│  Author name · Date                │
│  [Bookmark]                        │
└────────────────────────────────────┘
```

## 5. Variants

| Variant | Padding | Use |
|---|---|---|
| `default` | 20 | Topic grid |
| `compact` | 16 | Related articles list |
| `featured` | 28 | Top of page, larger photo |
| `text-only` | 20 | No photo, used in dense lists |

## 6. Sizes

- ≥1280px: 3-col grid, gap 32
- 768–1279px: 2-col grid, gap 24
- <768px: 1-col

## 7. States

| State | Visual |
|---|---|
| default | base |
| hover | `translateY(-2px)`, photo `scale(1.02)`, headline underline ochre |
| focus-within | outline 2px ochre on card |
| reading | small ochre dot cạnh headline |
| loading | skeleton |

## 8. Code reference

```tsx
<article class="group bg-white shadow-[0_1px_0_rgba(14,14,12,0.04)] hover:shadow-[0_8px_24px_rgba(14,14,12,0.10)] hover:-translate-y-0.5 transition-all duration-280">
  <a href={`/posts/${slug}`} class="block">
    <div class="aspect-[16/10] overflow-hidden bg-[#f0eee8]">
      <img
        src={`https://picsum.photos/seed/editorial-bw-${slug}/800/500`}
        alt=""
        aria-hidden="true"
        class="w-full h-full object-cover transition-all duration-500 group-hover:scale-[1.02]"
        style={{ filter: 'grayscale(0.6) contrast(1.05)' }}
        loading="lazy"
      />
    </div>
    <div class="p-5">
      <div class="flex items-center gap-2 font-mono text-[10.5px] uppercase tracking-[0.18em] text-[#73736e]">
        <Phosphor.Tag size={11} weight="bold" aria-hidden="true" />
        <span>{topic}</span>
        <span aria-hidden="true">·</span>
        <Phosphor.Clock size={11} weight="bold" aria-hidden="true" />
        <span>{readTime} min read</span>
        {hasAudio && (
          <>
            <span aria-hidden="true">·</span>
            <Phosphor.SpeakerHigh size={11} weight="bold" aria-hidden="true" />
            <span>Audio</span>
          </>
        )}
      </div>
      <h3 class="mt-3 font-display text-[24px] leading-tight text-[#0e0e0c] group-hover:underline decoration-[#c87f2e] decoration-2 underline-offset-4 transition-all">
        {headline}
      </h3>
      <p class="mt-2 text-[14.5px] text-[#3d3d39] leading-relaxed line-clamp-2">
        {dek}
      </p>
      <div class="mt-4 pt-4 border-t border-[rgba(14,14,12,0.06)] flex items-center justify-between">
        <div class="flex items-center gap-2">
          <img src={`https://picsum.photos/seed/author-portrait-${authorId}/80/80`} alt="" aria-hidden="true" class="w-7 h-7 rounded-full object-cover grayscale" />
          <span class="text-[12.5px] text-[#3d3d39]">{author}</span>
          <span aria-hidden="true" class="text-[#73736e]">·</span>
          <time datetime={publishedAt} class="text-[12.5px] text-[#73736e]">{publishedHuman}</time>
        </div>
        <button
          type="button"
          aria-label="Lưu bài"
          aria-pressed={bookmarked}
          class="text-[#73736e] hover:text-[#c87f2e] transition-colors duration-180"
          onClick={(e) => { e.preventDefault(); toggleBookmark(); }}
        >
          <Phosphor.BookmarkSimple size={16} weight={bookmarked ? 'fill' : 'regular'} aria-hidden="true" />
        </button>
      </div>
    </div>
  </a>
</article>
```