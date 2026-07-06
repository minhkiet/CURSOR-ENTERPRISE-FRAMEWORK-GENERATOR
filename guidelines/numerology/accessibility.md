# Accessibility. Starpath Numerology

> WCAG 2.2 AA rules for the Starpath numerology platform.

## 1. Language

- Default `<html lang="en">` for numerology terms (international).
- Vietnamese toggle: `lang="vi"`.
- Numbers always rendered numerically, with `<span aria-label="Eleven">11</span>` for screen readers (master numbers announced in words).

## 2. Color contrast on ink

Starpath runs almost entirely on `#0f0a1f` deep purple. Critical pairs:

- `#f5e9d0` parchment on `#0f0a1f`: 13.0:1 AAA
- `#b8b3cf` mist on `#0f0a1f`: 8.0:1 AAA
- `#7d7894` tertiary on `#0f0a1f`: 4.6:1 AA (UI components only)
- `#d4af37` gold on `#0f0a1f`: 7.0:1 AAA
- `#fbbf24` goldBright on `#0f0a1f`: 11.0:1 AAA

## 3. Numerals + screen readers

- `<span aria-label="Life Path Seven">7</span>` for screen readers (numbers announced as words).
- Master numbers: `<span aria-label="Master number Eleven">11</span>`.
- Avoid ordinal confusion: "the number 11" never just "11".

## 4. Reveal animations

- Reveal animation of Life Path number: `MOTION_INTENSITY=7`, requires `prefers-reduced-motion` fallback.
- Reduced-motion: number appears instantly without scale-up.
- Star burst behind number is decorative; `aria-hidden="true"`.

## 5. Reading flow

- Reading report is single-column scroll, semantic `<article>`.
- Each section has `<h2>` heading.
- Section anchor links for deep linking.
- Reading time estimate displayed in metadata.

## 6. Forms

- Date input for birth date: `inputmode="numeric"` for mobile.
- Name input normalizes Unicode (Vietnamese diacritics supported).
- Error text below input, color `#fbbf24` for warnings.
- Required field marked `aria-required="true"`.

## 7. Mystical content

- No absolute predictions, no medical/financial claims.
- All interpretations framed as "tendencies", "energies", "under current".
- Disclaimer visible at reading start.

## 8. Touch + mobile

- Buttons minimum 48×48px.
- Constellation backdrop sized as `next/image priority` for hero LCP.

## 9. Testing

- axe-core: 0 violations.
- Screen reader: NVDA / VoiceOver reads numbers in words.
- Reduced-motion verified.
- em-dash forbidden.