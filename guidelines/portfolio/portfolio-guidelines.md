# Designer Portfolio. Design System Guidelines (Market Pro 2026 — Editorial Hybrid)

> **Redesign ngày 2026-07-05.** Giữ white-cube gallery aesthetic (giữ Instrument Serif + minimal), thêm case studies phong phú hơn, awards wall, CV download, testimonials từ clients thật, video walkthrough case study.

## 1. Context

Linh Pham product designer portfolio. Bốn bề mặt:

- **Work index** (`/`). featured projects bento
- **Case study** (`/work/[slug]`). long-form process + outcome
- **About** (`/about`). bio + awards + clients
- **Contact** (`/contact`). one CTA

### 1.2 Brand-locked

- Wordmark: "Linh Pham" · Instrument Serif (giữ)
- Palette: white + ink + accent red (giữ)
- 5 featured projects max

### 1.3 Design intent

**White-cube gallery + rich case studies**. Vẫn gallery minimal, nhưng thêm video walkthrough, awards wall, testimonials từ clients thật.

### 1.4 Anti-patterns

- ❌ Generic 3-equal cards
- ❌ "Feel like..."
- ❌ Em-dash
- ❌ Resume-voice

---

## 2. Tokens

Xem `tokens.json`.

---

## 3. Section anatomy (Work index)

1. **Sticky header minimal**. Logo "Linh Pham" · Work · About · Awards · Contact · Resume
2. **Hero statement**. Massive italic Instrument Serif: "I design products that earn trust"
3. **Featured projects bento**. 5 projects asymmetric
4. **Selected clients wall**. 30+ logo via Simple Icons
5. **Awards strip**. Awwwards · FWA · CSS Design Awards
6. **Speaking + writing**. Bento 2 col
7. **Testimonials từ clients**. 3 client quotes
8. **Available for hire CTA**. Big CTA
9. **Footer minimal**

---

## 4. Voice

- First-person, not resume-voice
- "I led the design for..." not "Responsible for..."
- Client names italicized
- Em-dash cấm

---

## 5. Components

- `project-card.md`
- `case-study-hero.md`
- `awards-wall.md`
- `client-testimonial.md`
- `footer-mega.md`

---

## 6. Checklist

- [ ] Tokens semantic
- [ ] Instrument Serif for display, Plus Jakarta for body
- [ ] Whitespace py-32 to py-48
- [ ] No cards except photo containers
- [ ] Sharp corners (radius 0)
- [ ] One accent red sparingly
- [ ] axe-core 0
- [ ] WCAG AA
- [ ] Reduced motion
- [ ] No em-dash