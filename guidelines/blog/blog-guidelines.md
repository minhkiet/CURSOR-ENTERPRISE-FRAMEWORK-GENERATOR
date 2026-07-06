# Blog Platform. Design System Guidelines (Market Pro 2026 — Editorial Hybrid)

> **Redesign ngày 2026-07-05.** Giữ Newsreader editorial + ink palette cho di sản báo chí, thêm market density: bento articles, video essays, author spotlights, newsletter funnel, podcast embed.

## 1. Context

Inkwell là long-form editorial blog cho tech, culture, design. Bốn bề mặt:

- **Reading** (`/`). featured article + topic grid + author spotlight + newsletter
- **Article** (`/posts/[slug]`). long-form with inline media
- **Author** (`/authors/[handle]`). bio + bibliography + podcast
- **Topic** (`/topics/[slug]`). all articles by topic

### 1.2 Brand-locked

- Wordmark: "Inkwell" · Newsreader Italic
- Palette: paper, ink, ochre
- Topics: Tech, Culture, Design, Science, Long Reads, Business

### 1.3 Design intent

**Printed broadsheet digital twin + modern density**. Vẫn giữ cảm giác báo chí in truyền thống, nhưng thêm video essay, podcast embed, infographic, multi-author.

### 1.4 Anti-patterns

- ❌ Cormorant (giữ Newsreader)
- ❌ Generic cream overload (giữ giấy)
- ❌ Clickbait
- ❌ "Feel like..." 
- ❌ Em-dash

---

## 2. Tokens

Xem `tokens.json`.

---

## 3. Imagery

| Element | Unsplash ID |
|---|---|
| Editorial BW portrait | `1494790108377-be9c29b29330` |
| Article hero | `1499951360447-b19be8fe80f5` |
| Pen-ink drawing | `1455390582262-044cdead277a` |
| Topic Tech | `1518770660439-4636190af475` |
| Topic Culture | `1542038784456-1ea8e935640e` |
| Topic Design | `1561070791-2526d30994b8` |
| Topic Science | `1532187863486-abf9dbad1b69` |

### Photo treatment

`filter: grayscale(0.6) contrast(1.05)` cho editorial feel.

---

## 4. Section anatomy (Homepage)

1. **Sticky header minimal**. Logo · Topics nav · Search · Subscribe · Login
2. **Featured article hero**. Ảnh editorial BW + headline 96.5px + 2-line dek + byline
3. **Today's edition**. 3 bài mới nhất: 1 lớn + 2 nhỏ
4. **Topic bento**. 5 topics với mini grid: Tech, Culture, Design, Science, Long Reads
5. **Author spotlight**. Bento 3 tác giả + featured article của họ
6. **Video essay carousel**. Video essays
7. **Long reads**. Bài dài với reading time > 20 phút
8. **Podcast embed**. Audio player với episode mới
9. **Newsletter signup**. Email + 1-line value prop
10. **Footer minimal**

**Density**: VARIANCE 7 · MOTION 3 · DENSITY 5

---

## 5. Voice

- Editorial third person
- Sentence case
- No clickbait
- Pull-quotes real
- Em-dash cấm

---

## 6. Components

- `article-card.md`
- `author-card.md`
- `topic-bento.md`
- `newsletter-inline.md`
- `podcast-embed.md`
- `video-essay-card.md`
- `pull-quote.md`
- `footer-mega.md`

---

## 7. Checklist

- [ ] Tokens semantic
- [ ] Newsreader only, no Inter
- [ ] Photos BW via filter
- [ ] Articles max-width 65ch
- [ ] Pull-quote ochre
- [ ] No clickbait
- [ ] Em-dash cấm
- [ ] axe-core 0
- [ ] WCAG AA
- [ ] Reduced motion