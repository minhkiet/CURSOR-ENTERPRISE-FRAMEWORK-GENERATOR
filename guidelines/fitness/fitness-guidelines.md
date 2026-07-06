# Fitness App. Design System Guidelines (Market Pro 2026)

> **Redesign ngày 2026-07-05.** Phiên bản Market Pro giữ phong cách gym-floor (dark + electric green + chrome) nhưng giàu ảnh thật, video demo bài tập, giống Strong, Hevy, FitNotes.

## 1. Context

Ironpath là strength-training app. Bốn bề mặt:

- **Homepage** (`/`). Hero với workout video · Programs showcase · Stats demo · Pricing
- **Active workout** (`/workout`). Set tracker · Rest timer · Plate calculator · RPE
- **Programs** (`/programs`). 5/3/1 · Westside · Conjugate · Linear Progression · Bro Split
- **Stats** (`/stats`). 1RM history · Volume graphs · Personal records

### 1.2 Brand-locked

| Hạng mục | Quyết định |
|---|---|
| Wordmark | "Ironpath" · Plus Jakarta Sans 800 (giữ Space Grotesk OK) |
| Palette | Đen + electric green + chrome silver |
| Units | kg primary · lb toggle |
| Programs | 5/3/1, Westside, Conjugate, Linear Progression, Bro Split, PPL, GZCLP |

### 1.3 Design intent

**Gym-floor utilitarian**. Contrast cao, big mono numbers cho PRs, instant feedback, zero fluff. Ảnh gym low-light treatment.

### 1.4 Anti-patterns

- ❌ Cormorant/Fraunces
- ❌ Wellness framing ("you're doing great!")
- ❌ Pastel/cream
- ❌ Em-dash

---

## 2. Tokens

Xem `tokens.json`. Dark theme primary, electric green `#00ff88` cho CTA và success.

---

## 3. Section anatomy (Homepage)

1. **Sticky header dark**. Logo · Workout · Programs · Stats · Pricing · Login
2. **Hero workout video**. Background video squat/deadlift overlay · big metric "Build strength that lasts" · CTA "Start workout"
3. **Programs showcase**. 8 programs với ảnh + duration + difficulty
4. **Stats demo**. Big numbers với chart: total volume, sessions, PRs
5. **Workout in action**. Video gallery bài tập
6. **Testimonial**. Lifters với avatar + stats
7. **Pricing**. 3 tiers
8. **Footer**

---

## 4. Voice

- **Gym-floor terse.** "Locked in" not "You're doing great"
- **Numbers always with units.** "100kg x 5"
- **Failure is normal.** "Failed at rep 6. Drop 10% next set."
- **Em-dash cấm**

---

## 5. Components

- `workout-screen.md`
- `set-tracker.md`
- `rest-timer.md`
- `program-card.md`
- `pr-display.md`
- `volume-chart.md`
- `footer-mega.md`

---

## 6. Checklist

- [ ] Tokens semantic
- [ ] Plus Jakarta Sans + JetBrains Mono
- [ ] Dark primary
- [ ] Big mono numbers
- [ ] Real gym photos / videos
- [ ] axe-core 0
- [ ] WCAG AA (high contrast in dark mode)
- [ ] No em-dash