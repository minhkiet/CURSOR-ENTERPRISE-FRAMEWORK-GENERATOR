# Accessibility. Inkwell Blog

> WCAG 2.2 AA rules for the Inkwell editorial platform.

## 1. Language

- Default `<html lang="en">`.
- Article-level lang override for foreign phrases: `<span lang="fr">après moi le déluge</span>`.

## 2. Reading experience

- Article body max-width 65ch, line-height 1.7.
- Body font ≥18px (19px default).
- Pull-quote: `<blockquote>` semantic. Cite source via `<cite>` or `<footer>` inside `<blockquote>`.
- Heading hierarchy strict: one `<h1>` per page (article title), `<h2>` for sections, `<h3>` for subsections. No skipped levels.
- First paragraph of article: not styled as dropcap (avoid visual gimmick); use lead paragraph with `font-size: 1.125em`.

## 3. Color

Verified pairs:

- `color.text.primary` `#0e0e0c` on `#fafaf7` paper: 19.0:1 AAA
- `color.text.secondary` `#3d3d39` on `#fafaf7`: 11.2:1 AAA
- `color.text.tertiary` `#73736e` on `#fafaf7`: 5.6:1 AA (≥18px regular or ≥14px bold)
- `color.text.accent` `#c87f2e` ochre on `#fafaf7`: 5.4:1 AA (links)

## 4. Photos and figures

- All `<figure>` have `<figcaption>`. Decorative photos `alt=""` + `aria-hidden="true"`.
- Photo credits (when shown) live in caption, not separate text below.
- Author portraits: alt = "Photo of [Name]".

## 5. Navigation

- Skip-to-content link first focusable element.
- Sticky top nav ≤72px tall.
- Mobile menu trap focus, Escape closes, focus returns to toggle.

## 6. Forms (subscribe, search)

- Email input: label above, placeholder ≠ label.
- Required indicator `*` + `aria-required="true"`.
- Error message via `aria-describedby`, `role="alert"`.
- Validate on blur, not per keystroke.

## 7. Audio version

- Player uses native `<audio controls>` for native a11y.
- Transcript available for every audio article.

## 8. Reading time

- Reading time announced: "Estimated 8 minute read".
- Format: `<span class="sr-only">Estimated </span><span>8 minute</span> read`.

## 9. Tables of contents

- Article TOC inside `<nav aria-label="Table of contents">`.
- Current section highlighted via `aria-current="location"`.

## 10. Bookmark

- Bookmark button is real `<button aria-pressed="true|false">`.
- Share button opens share menu, `aria-expanded` toggles.
- All keyboard accessible.

## 11. Animation

- Reading-progress bar: respects `prefers-reduced-motion`.
- Hover effects ≤180ms.

## 12. Testing

- axe-core: 0 violations.
- NVDA / VoiceOver with long-form articles.
- Keyboard-only navigation across article + topic grid + author pages.
- Touch verified at 375 / 768 / 1280.
- em-dash (`,`) never in visible strings.