# Beauty Spa. Design System Guidelines (Market Pro 2026 — Editorial Hybrid)

> **Redesign ngày 2026-07-05.** Giữ editorial cao cấp (Cormorant + DM Sans + sand palette) cho phù hợp ritual cao cấp, thêm market density: video walkthrough treatment room, treatment gallery phong phú, testimonial với avatar, pricing transparent.

## 1. Context

Lumen là luxury day-spa booking. Bốn bề mặt:

- **Booking** (`/`). browse treatments · therapist profiles · book slots
- **Member** (`/account`). subscriptions · treatment history · saved rituals
- **Therapist** (`/admin`). schedules · availability · notes

### 1.2 Brand-locked (giữ nguyên)

- Wordmark: "LUMEN" · Cormorant Garamond 800, tracked
- Logo mark: vertical hairline (rose-gold) crossing circle (sand)
- Palette: paper, rose-gold, walnut ink
- Categories: Facial, Body, Massage, Energy, Couples

### 1.3 Design intent

**Bright treatment room at 9 a.m. + market density**. Vẫn giữ cảm giác thư giãn sang trọng, nhưng nhiều thông tin thực tế hơn (giá rõ, video tour, reviews, therapist portfolio).

### 1.4 Anti-patterns

- ❌ Cormorant Garamond dùng nhiều nơi (chỉ giữ cho display, body chuyển DM Sans)
- ❌ Sand cream quá đậm (giữ)
- ❌ "Feel like..." 
- ❌ Emoji
- ❌ Em-dash

---

## 2. Tokens

Xem `tokens.json`. Giữ palette cốt lõi, giảm bớt dùng Cormorant.

---

## 3. Imagery & Video

### 3.1 Image sources

| Element | Unsplash ID |
|---|---|
| Spa massage hands | `1544161515-4ab6ce6db874` |
| Treatment jar | `1556228720-195a672e8a03` |
| Therapist portrait | `1494790108377-be9c29b29330` |
| Ritual room | `1540555700478-4be289fbecef` |
| Sand wash texture | `1547036967-23d11aacaee0` |
| Eucalyptus | `1547043263-39d7fc7ed1cf` |
| Stone therapy | `1600334129128-685c5582fd35` |
| Aromatherapy | `1596178065887-1198b6148b2b` |

### 3.2 Video

- Hero: spa ambient video (Coverr - candle, water, hands)
- Treatment walkthrough: 30s tour mỗi treatment
- Ritual room: tour 360°

---

## 4. Section anatomy (Homepage)

1. **Sticky header minimal**. Logo · Treatments · Therapists · Membership · Locations · Book
2. **Mega-hero editorial**. Video ambient bg · overlay sand · "A ritual, not a service" · CTA "Đặt lịch ngay"
3. **Featured treatments bento**. 5 treatments bento với photo thật, duration, price, "Add to ritual" CTA
4. **Therapist showcase**. Avatar + name + specialties + rating carousel
5. **Ritual rooms gallery**. Video carousel phòng treatment
6. **Member testimonials**. 3 portrait + review text + treatment taken
7. **Membership tiers**. 3 gói: Essential · Signature · Ritual
8. **Booking widget**. Sticky floating với date picker
9. **FAQ ritual**. 6 câu về ritual cao cấp
10. **Footer elegant**

**Density**: VARIANCE 6 · MOTION 4 · DENSITY 5

---

## 5. Voice

- **Ritual vocabulary.** "ritual", "treatment", "ceremony", "lymphatic", "skin barrier", "restorative"
- **Warm, never breathless.** No urgency tactics.
- **No "AI", "smart", "instant", "revolutionary"**
- **Duration + price trên cùng card.**

---

## 6. Components

- `treatment-card.md`
- `therapist-portrait-card.md`
- `ritual-room-tour.md`
- `membership-tier.md`
- `booking-widget.md`
- `testimonial-portrait.md`
- `footer-mega.md`

---

## 7. Checklist

- [ ] Tokens semantic
- [ ] Cormorant cho display only, DM Sans cho body
- [ ] No Inter, no Helvetica
- [ ] Real spa photos
- [ ] Duration + price pairing
- [ ] No emoji
- [ ] Em-dash cấm
- [ ] axe-core 0
- [ ] WCAG AA
- [ ] Reduced motion