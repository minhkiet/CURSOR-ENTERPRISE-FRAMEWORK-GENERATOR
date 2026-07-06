# Accessibility Guidelines. Beauty Spa (Lumen)

> WCAG 2.2 AA rules for the Lumen Beauty Spa platform. Universal rules apply; the rules below address product-specific cases.

## 1. Language

- Primary `<html lang="vi">` (Vietnamese market). English toggle adds `lang="en"`.
- Mixed-language treatment names (e.g. "HydraFacial") keep brand spelling, but the description translates fully.

## 2. Color and contrast

Pairs verified in tokens.json. Critical rules:

- Body text always uses `color.text.primary` (walnut) on `color.surface.paper` (sand). Contrast 14.2:1.
- CTAs use walnut-on-rose-gold (`#2c2620` on `#d4a574`) → 5.2:1 AA.
- Sage (`#8fa896`) is for icons and decorative. never for body text.
- Terracotta (`#c47a5b`) used sparingly for festival accents (Tết, 8/3) and is decorative-only.

## 3. Photos and people

- All testimonial and therapist portraits are real photos, not generated faces. Placeholders via Picsum with descriptive seed.
- Avatar alt text describes the person by visible attributes only (no assumptions about identity).
- Decorative photos (hero backgrounds) get `alt=""` and `aria-hidden="true"`.

## 4. Booking flow

- Date picker: `<input type="date" lang="vi">` for primary; custom Vietnamese calendar widget for lunar dates if applicable.
- Time slot picker: 30-minute increments, keyboard navigable with arrow keys.
- Each slot has visible duration (60 min) and price (480.000₫). Screen reader announces "14:00, 60 phút, 480.000 đồng".
- Therapist selection announced with name + specialty + rating.
- Submit button has `aria-disabled="true"` while validating; do not native `disabled`.

## 5. Forms

- Label above input, always visible. Placeholder never replaces label.
- Required indicator: `*` plus `aria-required="true"`.
- Phone format: `0xxx xxx xxx` (10 digits). Auto-format on blur.
- Email validation: contains `@` and valid TLD.
- Error message specific, e.g. "Email phải chứa @" not "Invalid".
- `aria-invalid="true"` + `aria-describedby` to error message.
- `role="alert"` on error message.

## 6. Pricing

- Currency format: `480.000₫` (period separator, no decimals).
- `font-variant-numeric: tabular-nums` on all prices.
- Prices announced in full: "480.000 đồng".

## 7. Animation and motion

- All transitions ≤ 480ms.
- Hero photo parallax: 12% max, no more.
- Hover lifts max `-2px` translateY.
- Reduced-motion: disable parallax, fade only.

## 8. Touch targets

- Minimum 44×44px hit area.
- Mobile booking calendar cells minimum 56×56px (above 44 because of fat-finger risk).
- All buttons in form rows at least 48px tall on mobile.

## 9. Member dashboard

- Treatment history timeline uses `<ol>` semantic structure.
- Each treatment card is a `<article>` with date in `<time datetime>`.
- "Cancel booking" is a real button (action), not a link.
- Subscription billing info uses `<dl>` (definition list).

## 10. Testing

- axe-core: 0 violations.
- NVDA + VoiceOver in Vietnamese and English.
- Color contrast verified per pair.
- Keyboard-only booking flow.
- Touch device verified on iOS Safari, Android Chrome.
- em-dash (`,`) never appears in any visible string.