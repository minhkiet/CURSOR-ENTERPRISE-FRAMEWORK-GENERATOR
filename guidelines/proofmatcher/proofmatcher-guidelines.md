# ProofMatcher Design System. Implementation Guidelines

> Implementation-ready rules for the ProofMatcher template marketplace and component documentation site. Source of truth for tokens, component anatomy, state behavior, and accessibility acceptance criteria.

---

## 1. Context and Goals

### 1.1 Product context

ProofMatcher is a two-surface product:

- **Marketplace surface** (`/`). a curated template gallery where visitors filter templates by category (SaaS, Agency, Health, Education, Travel, etc.), preview, and purchase.
- **Documentation surface** (`/components/*` and component detail pages). reference documentation for the UI components embedded in ProofMatcher's own templates.

Both surfaces must read as **the same product**: same tokens, same spacing scale, same component anatomy. Diverging between the two creates cognitive cost for users who browse templates and then read component docs.

### 1.2 Audience

- **Primary**: founders, designers, and small-team builders who evaluate templates and copy-paste code into their own projects. They are time-pressed and skim.
- **Secondary**: developers reading component docs to understand which classes/HTML patterns to use in their own work.
- **Tertiary**: accessibility reviewers and procurement teams auditing the templates before purchase.

### 1.3 Design intent (one sentence)

Make every component feel **structured, tokenized, and content-first**. content carries the page, chrome recedes.

### 1.4 Non-goals

- We do not introduce new visual styles per page. Visual variance comes from content, not chrome.
- We do not add decorative elements that do not serve hierarchy or action.

### 1.5 What never changes without explicit approval

Per Section 0.E of `frontend-redesign`:

- URL structure and route slugs (`/`, `/components`, `/about`, `/contact`, etc.)
- Primary nav labels (Home, Components, About, Contact)
- Category filter labels in the marketplace (the 18 verticals in the filter bar)
- Brand wordmark ("PROOF MATCHER") and logo treatment
- Legal copy (Privacy Policy, Terms of Use, Disclaimer, Refund, Cookies)
- Email support address (`support@proofmatcher.com`)

---

## 2. Design Tokens and Foundations

All raw values are tokenized. Components must reference semantic tokens, never raw hex or pixel values.

### 2.1 Color tokens

#### Text

| Token | Value | Intended use |
|---|---|---|
| `color.text.primary` | `#ffffff` | Headlines, primary body, active nav label |
| `color.text.secondary` | `#a1a1aa` | Body, descriptions, secondary nav |
| `color.text.tertiary` | `#737373` | Captions, meta labels, helper text, count badges |
| `color.text.inverse` | `#525252` | Reserved for text on light/inverted surfaces (≥4.5:1 contrast on `#fafafa`+) |

**Contrast rule** (WCAG 2.2 AA, testable): every text/background pairing must achieve ≥4.5:1 for body text and ≥3:1 for text ≥18px or bold ≥14px. `color.text.tertiary` (`#737373`) on `color.surface.base` (`#000000`) measures 4.65:1, which passes AA only when the rendered text is **≥18px regular or ≥14px bold** OR non-essential (decorative captions, status counts). Components must enforce this rule and add automated contrast assertion in tests.

#### Surface

| Token | Value | Intended use |
|---|---|---|
| `color.surface.base` | `#000000` | Page background |
| `color.surface.raised` | `#050505` | Cards, modals, sticky bars |
| `color.surface.strong` | `#0d0d0d` | Hover state on raised surfaces, code blocks |

Surfaces are intentionally close in value. Hierarchy comes from `border-default` (1px) and `shadow.1` (lift), not from surface color contrast.

#### Border

| Token | Value | Intended use |
|---|---|---|
| `color.border.default` | `#e5e7eb` | Card and input borders (high contrast on black surface) |
| `color.border.strong` | `#fafafa` | Focus-visible rings, active state emphasis |

**Note on `border.default`**: `#e5e7eb` on `#000000` measures 17.5:1. This is intentional for borders that must be visible at all times against the dark base. Subtle borders (≤2px decorative dividers) should use `rgba(255,255,255,0.08)` instead. see `2.5 Subtle border extension` below.

### 2.2 Typography tokens

#### Family and base

- `font.family.primary`: `Inter`
- `font.family.stack`: `Inter, sans-serif`
- `font.size.base`: `16px`
- `font.weight.base`: `400`
- `font.lineHeight.base`: `24px`

#### Type scale (extended)

The original scale jumped from 16px to 26px. The extended scale adds intermediate steps that the marketplace and docs both need.

| Token | Size | Weight | Use |
|---|---|---|---|
| `font.size.xs` | 8px | 600, uppercase, tracking 0.08em | Eyebrow labels |
| `font.size.sm` | 11px | 500, uppercase, tracking 0.06em | Section labels, tag pills |
| `font.size.md` | 12px | 500 | Filter chip labels |
| `font.size.lg` | 13px | 400 | Card meta, button text (compact) |
| `font.size.xl` | 14px | 500 | Body emphasis, button text (default) |
| `font.size.2xl` | 15px | 400 | Default body |
| `font.size.3xl` | 16px | 400 | Card title, body long-form |
| `font.size.body-lg` | 18px | 400 | Long-form prose (docs) |
| `font.size.h4` | 20px | 600 | Section heading |
| `font.size.h3` | 22px | 600 | Card hero |
| `font.size.h2` | 24px | 600 | Page section heading |
| `font.size.h1` | 26px | 700 | Page hero (current `font.size.4xl`) |
| `font.size.display` | 36px | 800 | Marketplace hero only |

`tabular-nums` (`font-variant-numeric: tabular-nums`) must be applied to all price, count, and version strings to prevent width shifts.

### 2.3 Spacing tokens

| Token | Value | Common use |
|---|---|---|
| `space.1` | 4px | Icon-to-text gap, inline padding |
| `space.2` | 8px | Tight stack, badge padding y |
| `space.3` | 10px | Button padding y (compact) |
| `space.4` | 12px | Button padding x (compact), input padding y |
| `space.5` | 16px | Default button padding x, card padding (compact) |
| `space.6` | 20px | Card padding (default) |
| `space.7` | 24px | Section padding y (mobile) |
| `space.8` | 32px | Section padding y (desktop), card padding (spacious) |

Components must never introduce one-off values like `14px` or `22px`. If a layout seems to need a value not in the scale, the correct response is to combine existing tokens (`space.7 + space.1` = 28px via `28 = space.7 + space.1` or use flex/grid gap). not to add a new token.

### 2.4 Radius tokens

| Token | Value | Common use |
|---|---|---|
| `radius.sm` | 9999px | Pills, filter chips, avatars, badge |
| `radius.xs` | 12px | Cards, inputs, buttons (default) |
| `radius.md` | 6px | Code blocks, small badges (new) |
| `radius.lg` | 20px | Modals, hero panels (new) |
| `radius.none` | 0 | Decorative dividers, full-bleed surfaces |

Rule: a single component must use **one radius token**. Mixing `radius.xs` button with `radius.sm` badge inside the same control is prohibited.

### 2.5 Shadow tokens

| Token | Value | Use |
|---|---|---|
| `shadow.1` | `rgba(0,0,0,0.28) 0 10px 30px 0` | Card hover lift |
| `shadow.2` | `rgba(127,29,29,0.18) 0 12px 34px 0` | Error/validation emphasis (tinted toward `#7f1d1d`) |
| `shadow.3` | `rgba(0,0,0,0.4) 0 6px 20px 0` | Sticky bar, dropdown |

Shadows are tinted toward the background hue, not pure black. exception `shadow.2` carries the error red for validation states.

### 2.6 Motion tokens

| Token | Duration | Easing (default `cubic-bezier(0.22, 1, 0.36, 1)`) | Use |
|---|---|---|---|
| `motion.duration.instant` | 150ms | ease-out | Color/opacity swaps |
| `motion.duration.fast` | 300ms | ease-out | Hover lift, button press |
| `motion.duration.normal` | 500ms | ease-out | Modal open, drawer slide |

`prefers-reduced-motion: reduce` must collapse all three to `0.01ms`.

### 2.7 Subtle border extension (recommended, not in input)

Components that need a decorative divider (≤2px, non-functional) must use `rgba(255, 255, 255, 0.08)` rather than `color.border.default`, because the latter is too high-contrast for a divider. Add `color.border.subtle` to the token table when promoting to design system:

```
color.border.subtle: rgba(255, 255, 255, 0.08)
```

---

## 3. Density and Information Architecture

### 3.1 Observed density on `proofmatcher.com/` (homepage snapshot)

Measured via accessibility tree at viewport width ~1440px:

| Element | Observed count |
|---|---|
| Links (anchor tags) | ~17 distinct roles (5 nav + 1 footer logo + 11 footer links + cookie link) |
| Buttons | ~21 (1 cart + 2 sort/dropdown + 18 category filters) |
| Inputs | 1 (search) |
| Navigation regions | 2 (top nav, footer) |

The input value `links=68, buttons=25, inputs=1, navigation=1` does not match the current homepage. Treat the observed numbers as baseline. If the brief's larger numbers are a target for a future page (e.g. a fully-populated template grid showing 68 cards), use them as a **planning target**, not a constraint to invent components to hit.

### 3.2 Marketplace page density targets

For a marketplace grid page rendering ~60 templates:

- 60–80 link roles (1 per card + pagination + filters + footer)
- 20–30 button roles (filter chips, sort, view, purchase, pagination)
- 1 input (search)
- 2 navigation regions (top, footer)

Card density per row at desktop ≥1280px: **3 columns**, gap `space.6`. Tablet (768–1279px): 2 columns. Mobile (<768px): 1 column.

### 3.3 Docs page density targets

For a single component documentation page:

- 15–30 links (sidebar nav + footer + external links)
- 5–10 buttons (theme toggle, copy code, expand)
- 1 input (search)
- 2 navigation regions (top, footer)

Docs use a **left sidebar (240px) + main content + right "on this page" (200px)** layout at desktop. Sidebar collapses to a top dropdown below 1024px.

---

## 4. Component Rules

Each component file in `/guidelines/proofmatcher/components/` covers anatomy, variants, states, responsive behavior, accessibility, and edge cases. See:

- [`button.md`](./components/button.md)
- [`input.md`](./components/input.md)
- [`link.md`](./components/link.md)
- [`navigation.md`](./components/navigation.md)
- [`card.md`](./components/card.md)
- [`badge.md`](./components/badge.md)
- [`filter-chip.md`](./components/filter-chip.md)

### 4.1 Component coverage matrix

| Component | Variants | States covered | Density role |
|---|---|---|---|
| Button | primary, secondary, ghost, icon-only | default, hover, focus-visible, active, disabled, loading | High (25/page target) |
| Input | text, search, password | default, hover, focus, filled, error, disabled | Low (1–2/page) |
| Link | inline, standalone, nav | default, hover, focus-visible, active, visited | High (68/page target) |
| Navigation | top bar, footer, breadcrumb | default, scrolled (sticky), mobile-collapsed | Low (1–2/page) |
| Card | template, docs-feature, code-example | default, hover, focus-within, loading-skeleton, empty | Medium |
| Badge | count, status, category | default, hover, focus | Medium |
| Filter-chip | pill, count-suffix | default, hover, focus-visible, active (selected), disabled | Medium |

---

## 5. Accessibility Requirements

### 5.1 Universal requirements (must pass on every component)

1. **Keyboard**: every interactive element must be reachable via Tab in DOM order and operable via Enter/Space. Custom widgets (filter chips, dropdowns) must implement ARIA pattern (`role="tab"`, `aria-selected`, `aria-expanded`).
2. **Focus-visible**: every interactive element must show `outline: 2px solid color.border.strong; outline-offset: 2px` on `:focus-visible`. `:focus` alone must not show the ring (mouse click on button should not display ring).
3. **Contrast**: text/background pairs meet WCAG 2.2 AA (4.5:1 body, 3:1 large text). When using `color.text.tertiary` (`#737373` on `#000000`, 4.65:1), text must be ≥18px regular OR ≥14px bold OR clearly marked decorative.
4. **Labels**: every input must have an associated `<label>`. Icon-only buttons must have `aria-label`.
5. **Touch targets**: minimum 44×44px hit area for any clickable element, even if visual size is smaller (use `padding` or `::before` pseudo-element hit box).
6. **Motion**: respect `prefers-reduced-motion: reduce`. All animation collapses to ≤0.01ms.
7. **Screen reader**: status messages use `aria-live="polite"`. Errors use `aria-live="assertive"` or `role="alert"`.

### 5.2 Testable acceptance criteria

Each component ships with a checklist that QA can run as automated tests:

- `[ ]` axe-core scan shows 0 violations
- `[ ]` Keyboard-only walkthrough completes all primary actions
- `[ ]` Manual contrast check passes for every state (default, hover, focus, active, disabled, error)
- `[ ]` Reduced-motion test: all transitions complete in <50ms
- `[ ]` Touch target ≥44px verified via DevTools
- `[ ]` Screen reader announces component name, state, and value changes

See [`accessibility.md`](./accessibility.md) for the full appendix.

---

## 6. Content and Tone Standards

### 6.1 Voice

- **Concise**: prefer 8 words over 14.
- **Confident**: state the action, not the hedging. "Copy snippet" beats "If you'd like, you can copy the snippet".
- **Implementation-focused**: avoid marketing flourishes. Component docs read like API references.

### 6.2 Examples

| Use this | Not this |
|---|---|
| Copy code | Easily copy our code in seconds |
| 6 categories | We've hand-curated six amazing categories for you |
| View template | See this gorgeous template in action |
| Templates per page | Showing templates like you've never seen before |

### 6.3 Case rules

- **Sentence case** for all headings, buttons, and labels. No Title Case.
- **ALL CAPS** only for eyebrow labels (≤12 chars) and category filter chips (which already follow site convention).
- **lowercase** reserved for nav emphasis patterns and stylistic accents only.

### 6.4 Numbers

- Use organic data when possible: "47 templates" not "50 templates".
- Prices: include currency and locale (`$49 USD`, not `$49`).
- Counts in tables/lists use `tabular-nums`.

---

## 7. Anti-Patterns and Prohibited Implementations

### 7.1 Token anti-patterns

- ❌ Raw hex values in component CSS (`color: #ffffff` instead of `color: var(--color-text-primary)`)
- ❌ One-off spacing values (`margin-top: 14px`)
- ❌ Mixing radius tokens within a single component (`button: 12px, badge: 9999px` inside same control)
- ❌ Border radius on images with `<img>` (use `overflow: hidden` on parent + radius on parent)

### 7.2 Component anti-patterns

- ❌ **Buttons without focus-visible rings**
- ❌ **Placeholder-as-label** (`placeholder="Email"` with no `<label>`)
- ❌ **Icon-only buttons without `aria-label`**
- ❌ **Disabled buttons without explanation** (must include tooltip or `aria-describedby`)
- ❌ **Loading state that uses generic spinner** (must use skeleton matching final layout)
- ❌ **`window.alert()` for errors** (use inline error with `role="alert"`)
- ❌ **3-equal-card feature row** (use bento, asymmetric grid, or 2-column zig-zag)
- ❌ **All-caps subheaders everywhere** (sentence case + 1 ALL CAPS eyebrow per section max)
- ❌ **Hover state that only changes color** (must also include `transform: translateY(-1px)` or `scale(1.01)` for tactile feedback)
- ❌ **Carousel for testimonials** (use masonry wall or single rotating quote instead)

### 7.3 Color anti-patterns

- ❌ Using `color.text.tertiary` for body text <18px regular or <14px bold
- ❌ Multiple accent colors in one component
- ❌ Gradients on text (reserves gradients for hero atmosphere only)
- ❌ Random mid-page theme inversion (page commits to one theme)

### 7.4 Layout anti-patterns

- ❌ Centering everything (offset margins, left-aligned headers)
- ❌ `height: 100vh` (use `min-height: 100dvh`)
- ❌ Hardcoded pixel widths (use `max-width` with `width: 100%`)
- ❌ `z-index: 9999` (use a published scale: `--z-base`, `--z-raised`, `--z-sticky`, `--z-modal`, `--z-toast`)
- ❌ Missing `meta` description or OG tags on docs pages

### 7.5 Accessibility anti-patterns

- ❌ `outline: none` without replacement focus indicator
- ❌ Positive `tabindex` values
- ❌ `aria-label` that duplicates visible text
- ❌ `role="button"` on `<a>` without `href` (use `<button>`)
- ❌ `alt=""` on meaningful images (use descriptive alt)
- ❌ Hidden focus on focusable elements

---

## 8. Responsive Behavior

| Breakpoint | Width | Marketplace grid | Docs layout | Nav |
|---|---|---|---|---|
| Mobile | <768px | 1 column | Sidebar → top dropdown | Hamburger menu |
| Tablet | 768–1023px | 2 columns | Sidebar visible | Top nav |
| Desktop | 1024–1439px | 3 columns | Sidebar + content + ToC | Top nav |
| Wide | ≥1440px | 4 columns | Sidebar + content + ToC | Top nav, max-width 1440px |

`100dvh` (dynamic viewport height) is required for full-screen sections to handle mobile browser chrome. `100vh` is forbidden.

---

## 9. Migration Notes (Redesign - Preserve mode)

This is a **Preserve** redesign (Section 0.C of `frontend-redesign`). Brand identity, URL structure, nav labels, and category taxonomy are preserved. The change is modernization of component implementation.

When migrating existing components to the new tokens:

1. Replace raw hex values with token references. Use a codemod where possible.
2. Update spacing values to the scale. Common offsets: `14px → space.4 (12px) + space.1 (4px) = 16px` or recompose layout.
3. Add missing states. Most existing components lack `loading`, `error`, `disabled`, and `focus-visible` defined explicitly.
4. Add ARIA patterns to interactive widgets that are currently `<div role="button">`.
5. Add `:focus-visible` rules if missing.
6. Add reduced-motion override.
7. Verify contrast for every state, including hover and disabled (disabled must still meet 3:1 for non-text UI).

---

## 10. QA Checklist (run before merge)

### 10.1 Token compliance

- [ ] No raw hex values in component source
- [ ] All spacing values map to `space.*` tokens
- [ ] All radius values map to `radius.*` tokens
- [ ] All shadows map to `shadow.*` tokens
- [ ] All motion durations map to `motion.duration.*` tokens

### 10.2 Component compliance

- [ ] Every interactive component has all required states defined
- [ ] Every state has a visible difference from every other state
- [ ] Disabled state has tooltip or `aria-describedby` explaining why disabled
- [ ] Loading state uses skeleton matching final shape
- [ ] Error state uses `role="alert"` and is reachable by screen reader

### 10.3 Accessibility

- [ ] axe-core scan: 0 violations on every page
- [ ] Keyboard-only walkthrough: every action completable
- [ ] Contrast verified for all 7 states (default, hover, focus, active, disabled, loading, error)
- [ ] Touch targets ≥44×44px
- [ ] Reduced-motion: all transitions ≤50ms
- [ ] Screen reader (NVDA/VoiceOver): announces name, role, state, value

### 10.4 Responsive

- [ ] Layout at 360px, 768px, 1024px, 1440px, 1920px verified
- [ ] No horizontal scroll at any breakpoint
- [ ] Mobile menu opens/closes via keyboard
- [ ] Touch targets remain ≥44×44px at all breakpoints

### 10.5 Content

- [ ] No Lorem Ipsum anywhere
- [ ] No placeholder company names (Acme, Test Co)
- [ ] No AI copywriting clichés (Elevate, Seamless, Unleash, Next-Gen)
- [ ] All headings sentence case
- [ ] Numbers use `tabular-nums` where applicable
- [ ] Emoji absent (unless explicitly requested)

### 10.6 SEO (docs pages)

- [ ] `<title>` unique per page, ≤60 chars
- [ ] `<meta description>` unique per page, ≤160 chars
- [ ] OG tags present (title, description, image, url)
- [ ] URL slug unchanged from existing structure
- [ ] Structured data (JSON-LD) valid

### 10.7 Code quality

- [ ] No inline styles
- [ ] No hardcoded pixel widths in component CSS
- [ ] Semantic HTML used (`<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`)
- [ ] No dead code or commented-out blocks
- [ ] All imports resolve to existing files
- [ ] No console.log or debugger in production

---

## 11. Open Questions

1. **Token table approval**: are the extended type scale and radius additions acceptable, or should we keep the original 8 type sizes and 2 radii?
2. **Subtle border**: confirm we add `color.border.subtle` (`rgba(255,255,255,0.08)`) for decorative dividers, distinct from `border.default`.
3. **Reduced motion strategy**: should `motion.duration.normal` (500ms) keep a fade but remove translate, or collapse fully to 0.01ms?
4. **Component library scope**: do we ship only marketplace components or also the templates' internal components (hero, pricing, FAQ)? The latter expands scope significantly.
5. **Doc layout**: docs currently use the same components as marketplace. Confirm left-sidebar + content + ToC layout is approved for docs pages.

---

## Appendix A. Token JSON (for handoff to engineering)

```json
{
  "color": {
    "text": {
      "primary": "#ffffff",
      "secondary": "#a1a1aa",
      "tertiary": "#737373",
      "inverse": "#525252"
    },
    "surface": {
      "base": "#000000",
      "raised": "#050505",
      "strong": "#0d0d0d"
    },
    "border": {
      "default": "#e5e7eb",
      "strong": "#fafafa",
      "subtle": "rgba(255, 255, 255, 0.08)"
    }
  },
  "font": {
    "family": { "primary": "Inter", "stack": "Inter, sans-serif" },
    "size": {
      "xs": "8px", "sm": "11px", "md": "12px", "lg": "13px",
      "xl": "14px", "2xl": "15px", "3xl": "16px", "base": "16px",
      "body-lg": "18px", "h4": "20px", "h3": "22px",
      "h2": "24px", "h1": "26px", "4xl": "26px", "display": "36px"
    },
    "weight": { "base": 400, "medium": 500, "semibold": 600, "bold": 700, "extrabold": 800 },
    "lineHeight": { "base": "24px" }
  },
  "space": {
    "1": "4px", "2": "8px", "3": "10px", "4": "12px",
    "5": "16px", "6": "20px", "7": "24px", "8": "32px"
  },
  "radius": {
    "none": "0", "xs": "12px", "md": "6px", "lg": "20px", "sm": "9999px"
  },
  "shadow": {
    "1": "rgba(0, 0, 0, 0.28) 0px 10px 30px 0px",
    "2": "rgba(127, 29, 29, 0.18) 0px 12px 34px 0px",
    "3": "rgba(0, 0, 0, 0.4) 0px 6px 20px 0px"
  },
  "motion": {
    "duration": {
      "instant": "150ms",
      "fast": "300ms",
      "normal": "500ms"
    },
    "easing": {
      "default": "cubic-bezier(0.22, 1, 0.36, 1)"
    }
  }
}
```

---

## Appendix B. Source-of-truth file paths

- Brand guidelines: `/guidelines/proofmatcher/proofmatcher-guidelines.md` (this file)
- Component anatomy: `/guidelines/proofmatcher/components/*.md`
- Accessibility appendix: `/guidelines/proofmatcher/accessibility.md`
- Token JSON: `/guidelines/proofmatcher/tokens.json`

Engineering implementation should consume `tokens.json` and the component files. Do not duplicate token values in component source.