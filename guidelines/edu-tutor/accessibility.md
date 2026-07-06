# Accessibility. Mentorly Edu Tutor

> WCAG 2.2 AA rules for the Mentorly tutor booking platform.

## 1. Language

- Default `<html lang="vi">`.
- Toggle English via `lang="en"`.
- Subject names: Vietnamese primary, English in parens for international terms (`<span lang="en">Mathematics</span>`).

## 2. Color contrast on cream

Mentorly runs on `#fdf8ec` cream. Critical pairs:

- `#0f172a` ink on `#fdf8ec`: 18.6:1 AAA
- `#475569` secondary on `#fdf8ec`: 7.6:1 AAA
- `#1e3a8a` cobalt on `#fdf8ec`: 12.0:1 AAA
- `#b45309` amber on `#fdf8ec`: 5.1:1 AA
- `#f59e0b` amberBright on `#fdf8ec`: 2.1:1 (UI only, never text)
- `#047857` success on `#fdf8ec`: 6.2:1 AA

## 3. Touch targets

Students tap quickly between classes. Minimum 48×48px, primary CTA 56×56px.

## 4. Subject icons + screen readers

- Each subject icon must have `aria-hidden="true"`, subject name announced via `<h3>`.
- Subject selection: `<input type="radio">` with visible label.

## 5. Date + time pickers

- Date input: `inputmode="numeric"` for mobile.
- Time zone explicit: "24h Vietnam (UTC+7)".
- Format: `dd/MM/yyyy` for Vietnamese, `MM/dd/yyyy` for English.

## 6. Video room

- Join button is real `<button>`, not a `<div>`.
- Microphone + camera toggles announced.
- Reduced-motion: no animated mic indicator.

## 7. Forms

- Label above input, error below input.
- Required fields marked `aria-required="true"`.
- Form validation summary at top on error submit.

## 8. Tutor cards

- Photo has descriptive alt: `alt="Portrait of Trần Văn Minh"`.
- Avatar lazy-loaded.
- Hover lift cancelled under reduced-motion.

## 9. Rating display

- `<span aria-label="Rated 4.9 out of 5">★★★★★</span>` for screen readers.

## 10. Reduced motion

- Caveat handwritten font: static, no animation.
- Card hover lift replaced by border color change.
- Confetti / sparkle effects disabled.

## 11. Testing

- axe-core: 0 violations.
- Keyboard-only navigation: Tab through all tutor cards, Open, Book.
- em-dash forbidden.