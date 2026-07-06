# Numerology Reading. Design System Guidelines (Market Pro 2026 — Mystical Hybrid)

> **Redesign ngày 2026-07-05.** Giữ mystical vibe (deep purple + gold + ink) cho numerology ceremony, thêm market density: video reveal, comparison table, pricing, testimonials với avatar.

## 1. Context

Starpath generates personal numerology readings. Bốn bề mặt:

- **Input** (`/`). birth date + full name → reading
- **Reading** (`/readings/[id]`). life path, expression, soul urge numbers + interpretations
- **Compatibility** (`/compatibility`). two people comparison
- **Daily forecast** (`/today`). daily energy + lucky numbers

### 1.2 Brand-locked

| Hạng mục | Quyết định |
|---|---|
| Wordmark | "Starpath" · Cormorant Garamond 600 |
| Palette | Ink purple + gold + parchment |
| Numerology systems | Pythagorean, Chaldean, Vedic |
| Number sets | 1-9, 11, 22, 33 (master numbers) |

### 1.3 Design intent

**Velvet fortune-teller's tent at midnight + market density**. Giữ mystical premium, thêm video reveal, comparison tables, testimonials.

### 1.4 Anti-patterns

- ❌ Inter cho mystical
- ❌ Bright colors
- ❌ "Feel like..."
- ❌ Em-dash
- ❌ Clickbait predictions

---

## 2. Tokens

Xem `tokens.json`. Dark theme, gold numbers primary visual.

---

## 3. Section anatomy (Homepage)

1. **Sticky header dark**. Logo gold · Input · Compatibility · Daily · Reading store · Login
2. **Hero với input widget**. Constellation video bg · gold overlay · "Discover your life path" · input form
3. **Numbers bento**. 9 numbers (1-9) + master numbers (11, 22, 33) bento grid
4. **Reading sample**. Screenshot reading thật (cover image)
5. **Compatibility showcase**. 2 chart side by side preview
6. **Daily forecast video**. Video daily
7. **Pricing**. 3 tiers
8. **Testimonials**. 3 portraits + readings
9. **Footer dark**

---

## 4. Voice

- Second person. "Your Life Path is 7"
- Numbers in words: "Your Soul Urge is Eleven"
- No absolute predictions. Use "tendencies", "energy"
- Em-dash cấm

---

## 5. Components

- `life-path-display.md`
- `numbers-bento.md`
- `reading-card.md`
- `compatibility-split.md`
- `pricing-tier.md`
- `testimonial-portrait.md`
- `footer-mega.md`

---

## 6. Checklist

- [ ] Tokens semantic
- [ ] Cormorant for numerals, Plus Jakarta for body
- [ ] Deep purple bg + gold numerals
- [ ] No absolute predictions
- [ ] Numbers in gold serif
- [ ] axe-core 0
- [ ] WCAG AA (high contrast in dark)
- [ ] Reduced motion
- [ ] No em-dash