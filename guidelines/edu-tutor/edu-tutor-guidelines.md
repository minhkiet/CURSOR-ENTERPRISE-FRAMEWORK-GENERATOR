# Edu Tutor. Design System Guidelines (Market Pro 2026)

> **Redesign ngày 2026-07-05.** Phiên bản Market Pro. Giống Preply, Italki, VIPKid — giàu tutor portfolio, video intro, rating, hourly rate, lesson packages.

## 1. Context

Mentorly connects students (15-22) với verified tutors. Bốn bề mặt:

- **Marketplace** (`/`). tutor directory với filter + video intro
- **Tutor profile** (`/tutors/[id]`). bio + video + reviews + booking widget
- **Lesson** (`/lessons/[id]`). video room + chat + homework
- **Student dashboard** (`/dashboard`). upcoming lessons + progress

### 1.2 Brand-locked

| Hạng mục | Quyết định |
|---|---|
| Wordmark | "Mentorly" · Plus Jakarta Sans 800 |
| Logo mark | Graduation cap stylized |
| Palette | Cream + cobalt + amber |
| Subjects | Math, Physics, English, Chemistry, Music, Vietnamese |
| Account types | Student, Tutor |

### 1.3 Design intent

**Bright study hall at 3 p.m. + market density**. Vẫn giữ warm friendly, thêm tutor portfolios phong phú.

### 1.4 Anti-patterns

- ❌ Cormorant/Fraunces
- ❌ Cream quá đậm (giữ)
- ❌ "Feel like..."
- ❌ Em-dash

---

## 2. Tokens

Xem `tokens.json`. Caveat cốc cho reward/sticker.

---

## 3. Section anatomy (Homepage)

1. **Sticky header**. Logo · Subjects · Tutors · How it works · Become tutor · Login
2. **Hero với search widget**. Subject picker · Level · Price · "Tìm gia sư"
3. **Trust strip**. "5.000+ gia sư verified", "100.000+ buổi học", "4.9★ average", "Đã đăng ký Bộ GD&ĐT"
4. **Subjects bento**. 6 subjects với icon + tutor count
5. **Top rated tutors**. 8 tutor cards với avatar, video, rating, hourly rate
6. **How it works**. 3 steps với video demo
7. **Student testimonials video**. 3 video
8. **Pricing - hourly rates**. Mini bento: gia sư theo price tier
9. **Become a tutor CTA**. Side strip
10. **FAQ**. 6 câu
11. **Footer**

**Density**: VARIANCE 6 · MOTION 6 · DENSITY 6

---

## 4. Voice

- Friendly but professional. "Đặt buổi học thử miễn phí" not "Free trial lesson"
- Parents speak English: "Verified tutor" not "Certified teacher"
- Caveat ≤3 per page, only for rewards/stickers
- Em-dash cấm

---

## 5. Components

- `tutor-card.md`
- `subject-bento.md`
- `video-intro-player.md`
- `lesson-booking-widget.md`
- `testimonial-video.md`
- `reward-sticker.md`
- `footer-mega.md`

---

## 6. Checklist

- [ ] Tokens semantic
- [ ] Plus Jakarta Sans + Caveat (rare)
- [ ] Cobalt CTAs on cream
- [ ] Caveat ≤ 3 per page
- [ ] Real tutor photos via Unsplash
- [ ] Video intros
- [ ] axe-core 0
- [ ] WCAG AA
- [ ] Reduced motion
- [ ] No em-dash