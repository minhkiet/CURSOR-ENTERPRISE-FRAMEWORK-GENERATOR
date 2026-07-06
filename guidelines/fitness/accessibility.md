# Fitness Platform. Accessibility (WCAG 2.2 AA + Gym-Floor Friendly)

> Ironpath Fitness — dark utilitarian design với high-contrast, large touch targets (gloves + mồ hôi). Áp dụng cho cả marketing landing và in-app workout tracker.

## 1. Universal requirements

| Hạng mục | Tiêu chí | Test |
|---|---|---|
| Color contrast | Body text ≥ 4.5:1. Trên dark `slate-950` (`#0a0f1a`), text phải ≥ 7:1 (AAA nếu được) | axe-core |
| Touch target | ≥ 56x56px cho workout controls (gloves+perspiration context). WCAG min 44px không đủ cho gym | DevTools |
| Keyboard | Tab + Enter + Esc + Space. Rest timer cần Space (pause) | Manual |
| Focus visible | Ring electric-green 3px (high-contrast cho dark theme) | Visible |
| Alt text | Workout videos có time-stamped transcripts | HTML scan |
| Language | `<html lang="vi">` | HTML |
| Motion | Reduce-motion: pulse / hover / glow transitions off. Bar-chart animations off | Toggle test |
| Numbers | Weight `kg` · Reps `reps` · Volume `kg` · Distance `km` — all tabular-nums | Visible |
| Time | Rest timer relative: "01:23" remaining + absolute end time | Screen reader |

## 2. Touch & Glove Considerations

Gym environment: user đeo gloves, tay ướt mồ hôi. Touch targets PHẢI rất lớn và visible.

| Element | Min touch target | Why |
|---|---|---|
| Primary CTA "Bắt đầu workout" | 64x64px | Quick tap mid-set |
| Rest timer big numbers | 96px+ | Visible while standing 2m away |
| Set complete check | 56x56px | Hit without looking down |
| Plate calculator +/- | 48x48px | Quick adjust |
| Video play/pause | 64x64px | Sticky with sweat |

> **Rule of thumb**: Nếu bạn không thể tap nó khi đang ở giữa rep thì nó quá nhỏ.

## 3. Color contrast cho dark theme

`#0a0f1a` (slate-950) là base. Tất cả text phải vượt 7:1:

| Foreground | Background | Ratio | Status |
|---|---|---|---|
| `slate-50` (`#f1f5f9`) | `slate-950` (`#0a0f1a`) | 17.8:1 | AAA ✓ |
| `slate-300` (`#cbd5e1`) | `slate-950` | 13.2:1 | AAA ✓ |
| `slate-400` (`#94a3b8`) | `slate-950` | 8.5:1 | AAA ✓ |
| `electric-400` (`#a3e635`) | `slate-950` | 14.1:1 | AAA ✓ |
| `electric-500` (`#84cc16`) | `slate-950` | 11.9:1 | AAA ✓ |
| `red-400` (`#f87171`) | `slate-950` | 7.2:1 | AAA ✓ |
| `amber-400` (`#fbbf24`) | `slate-950` | 11.4:1 | AAA ✓ |

> **Rule of thumb cho dark**: Không bao giờ dùng `slate-500` trở xuống cho body text trên `slate-950`. Minimum là `slate-400`.

## 4. Component-specific

### 4.1 Workout screen

- Rest timer dùng `aria-live="polite"` (announce mỗi 30s), NOT every second
- Big rest timer có aria-label "Nghỉ 1 phút 30 giây, còn lại 30 giây"
- Set counter là `<output>` accessible
- Buttons có `aria-keyshortcuts="Space"`
- Weight + reps input có steppers (±) rõ ràng
- Plate calculator announces "20kg mỗi bên, tổng 60kg"
- Reduce-motion: pulse off khi rest timer < 10s

### 4.2 Set tracker

- Mỗi set là `<li>` trong `<ol>` semantic
- Set có states: pending · active · completed
- Active set có focus + ring
- Tap complete set — tự động advance sau 2s (hoặc manual)
- Touch target ≥ 56x56px cho checkbox
- aria-current="true" cho active set
- aria-disabled khi set locked

### 4.3 Rest timer

- Big numbers ≥ 96px cho timer
- Color-coded: green (>30s) · amber (10-30s) · red (<10s, pulsing)
- Pause/Resume button ≥ 64x64px
- Skip button để next exercise
- Audio cue: 3s cuối có beep, rung trên mobile (toggle)
- Reduce-motion: pulse off at <10s
- Screen reader: announce mỗi 30s (không spam)

### 4.4 PR display

- "CÁ NHÂN TỐT NHẤT" có icon + label, không color-only
- Numbers tabular-nums
- Video thumbnail có alt text mô tả exercise
- Date hiển thị absolute (15/7/2026) và relative ("3 ngày trước")
- Celebration animations có respect reduced-motion

### 4.5 Volume chart

- Bar chart có text alternative summary
- Each bar accessible `<button>` với tooltip chi tiết
- Period selector (7d · 30d · 90d · 1y) là `role="tablist"` + `aria-selected`
- Y-axis có grid lines + labels accessible
- Sparkline có `aria-label="Volume tăng 24% trong 30 ngày"`

### 4.6 Program card

- Program name là heading level 3
- Difficulty có icon + label (Beginner / Intermediate / Advanced)
- Duration có icon + label
- Equipment list accessible
- CTA accessible
- Reduce-motion: hover transitions off

### 4.7 Mega footer

- Brand + link columns semantic
- App download có alt text trên badges
- Hotline `tel:` accessible
- Trust signals có icon + label

## 5. Rest timer audio cue rules

| Time remaining | Audio | Haptic | Visual |
|---|---|---|---|
| > 30s | none | none | green |
| 10-30s | none | none | amber |
| 5-10s | none | short pulse | red |
| 3s | short beep | haptic | red bold |
| 0s (done!) | strong beep (200ms) | strong haptic | green flash |

> Reduce-motion: chỉ beep audio + text change, không flash/pulse.

## 6. Vietnamese language considerations

- "Tập", "Nghỉ", "Hiệp" thay vì "Set" khi nói chuyện, nhưng UI label dùng "Hiệp" để consistent
- "CÁ NHÂN TỐT NHÂN THÀNH TÍCH" / "PR" cho personal record
- "Khối lượng" cho volume
- Weight `80kg` cho kg, `175lb` cho lb
- "Không bao gồm tạ" cho bodyweight
- Date format `15/7/2026` (DD/MM/YYYY)
- Time format `5 phút` cho duration

## 7. Performance + A11y interplay

- Video `preload="metadata"` only — không load full video before play
- Audio cue: small base64 audio (≤ 5KB) inline
- Plate calculator: instant calculation, không async
- Volume chart data: pre-computed, không query trên mỗi render
- Real-time: aria-live chỉ 30s intervals (không spam)
- Workout save: optimistic update, retry on failure

## 8. Acceptance criteria

### 8.1 Testable

- [ ] axe-core: 0 violations
- [ ] Lighthouse accessibility: ≥ 95
- [ ] Touch targets ≥ 56px cho workout controls
- [ ] Manual keyboard: complete 1 workout set không dùng chuột
- [ ] Screen reader (NVDA): đọc được rest timer state + set progression
- [ ] Reduce-motion: pulse off + transitions instant
- [ ] Audio cue off khi reduce-motion + đúng giờ
- [ ] Weight/reps khi tăng/giảm stepper announce value
- [ ] All form fields có label + error
- [ ] Charts có text alternative
- [ ] "Cá nhân tốt nhất" không color-only

### 8.2 Common violations to avoid

- ❌ Touch target < 44px (đặc biệt cho gym)
- ❌ Color-only "Hot" / "New" (đã icon + label)
- ❌ Rest timer spam aria-live (đã 30s interval)
- ❌ Without `prefers-reduced-motion` overrides
- ❌ Animated bar chart on load (đã off reduce-motion)
- ❌ Audio auto-play không toggle (đã có audio toggle)
- ❌ Video autoplay without mute
- ❌ Form không có label (đã có label + error)

## 9. Recommended test tools

- axe-core CLI + extension
- Lighthouse CI
- NVDA + Firefox (Windows)
- VoiceOver + Safari (macOS)
- TalkBack + Chrome (Android)
- Chrome DevTools Accessibility tab
- WAVE
- Pa11y CI

---

**Version**: 2026.1 · WCAG 2.2 AA + Gym-Floor Friendly