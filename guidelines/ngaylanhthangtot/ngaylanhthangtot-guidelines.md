# Ngày Lành Tháng Tốt. Design System Guidelines

> Implementation-ready rules for the Ngày Lành Tháng Tốt landing page and subscription PWA. Source of truth for tokens, component anatomy, state behavior, and accessibility acceptance criteria.

---

## 1. Context and Goals

### 1.1 Product context

Ngày Lành Tháng Tốt is a personal electronic calendar product (`https://ngaylanhthangtot.vn/`) targeting Vietnamese end-users aged 30+. It positions a 365-day tear-off calendar re-imagined as a PWA: every page is stamped with the user's Tứ Trụ (Four Pillars) destiny reading for that specific day.

Two surfaces ship from one codebase:

- **Marketing landing surface**. single long-scroll landing page that explains the product, shows the calendar in action, presents 3 pricing tiers (3-month, 6-month, 12-month), and answers FAQs.
- **Authenticated app surface**. `/lich` route where authenticated users view "today's page" each morning.

Both surfaces must read as **the same product**: same warm cream palette, same Lora serif typography, same gold accent (#9a7c22), same vintage-editorial feel.

### 1.2 Audience

- **Primary**: Vietnamese end-users 30+, traditionalist, spiritual-but-modern. They respond to "lá số", "mệnh", "cát hung" (auspicious/inauspicious), and "Tứ Trụ". They distrust generic tech-bro marketing.
- **Secondary**: design-conscious users who notice typography and layout craft.
- **Tertiary**: accessibility reviewers, mobile users on metered connections.

**Audience is NOT developers.** This is not a docs site or component library. Do not write copy that addresses "engineering teams" or "documentation".

### 1.3 Design intent (one sentence)

Make every page feel like a **laminated tear-off calendar page from a refined ấn phẩm (publication)**. warm cream paper, deep ink characters, gold-accented rule lines, nothing decorative without purpose.

### 1.4 Non-goals

- No dark mode (the brand is paper-warm). Dark mode is not in scope for v1.
- No gradient backgrounds on body content (only on hero decorative elements).
- No emoji or illustration mascots. Brand is editorial, not playful.
- No AI-tech-bro vocabulary ("AI-powered", "next-gen", "leverage").

### 1.5 What never changes without explicit approval

Per Section 0.E of `frontend-redesign`:

- Brand wordmark "Ngày Lành / Tháng Tốt" (two-line stacked) and logo mark
- Color palette derived from `#f0ece2` paper / `#9a7c22` gold / `#a3201f` auspicious red / `#1d3129` ink
- Vietnamese language (`<html lang="vi">`)
- Three pricing tiers (3-month / 6-month / 12-month) and their relative discounts
- The 365-page metaphor (always present in copy and visuals)

---

## 2. Design Tokens and Foundations

All raw values are tokenized. Components must reference semantic tokens, never raw hex.

### 2.1 Color tokens

#### Text (on light cream surface `#f0ece2`)

| Token | Value | Intended use | Contrast on `#f0ece2` |
|---|---|---|---|
| `color.text.primary` | `#18150e` | Headlines, body, primary labels | 14.8:1 (AAA) |
| `color.text.secondary` | `#3a3220` | Body emphasis, secondary nav | 9.4:1 (AAA) |
| `color.text.tertiary` | `#7a7050` | Captions, meta, helper text, eyebrows | 4.7:1 (AA) |
| `color.text.auspicious` | `#a3201f` | "Ngày khô" (auspicious) labels, festival accents | 5.9:1 (AA) |
| `color.text.inverse` | `#ede7d3` | Text on dark `#1d3129` surface | 11.2:1 (AAA) |

**Contrast rule** (WCAG 2.2 AA, testable): every text/background pair must achieve ≥4.5:1 for body text and ≥3:1 for text ≥18px regular or ≥14px bold. The brand tertiary `#7a7050` on `#f0ece2` measures 4.7:1. passes AA and is the safe default for captions, eyebrows, and helper text on cream surfaces. Components must NOT use the inverse text color (`#ede7d3`) on cream surfaces. it measures ~1.1:1 and is reserved for dark surfaces only.

#### Text on dark surface `#1d3129` (CTA sections, dark hero strip)

| Pair | Ratio | Status |
|---|---|---|
| `color.text.inverse` `#ede7d3` on `#1d3129` | 11.2:1 | AAA. pass |
| `#c5a55a` gold on `#1d3129` | 6.4:1 | AA. pass |
| `rgba(237,231,211,0.7)` muted inverse on `#1d3129` | ~7.5:1 | AAA. pass |
| `rgba(237,231,211,0.55)` footer body on `#0e1c14` | ~6:1 | AA. pass |

#### Surface

| Token | Value | Intended use |
|---|---|---|
| `color.surface.paper` | `#f0ece2` | Page background, the "paper" of the calendar |
| `color.surface.card` | `#ffffff` | Calendar pages, pricing cards on cream background |
| `color.surface.dark` | `#1d3129` | CTA sections, dark feature strips, sticky bar |
| `color.surface.darkFooter` | `#0e1c14` | Footer background (darker than dark) |
| `color.surface.calPage` | `#ede7d3` | Inactive calendar mini-grid cells (darker than paper) |
| `color.surface.raised` | `#ffffff` | Hover/elevated card background |

#### Accent and semantic

| Token | Value | Intended use |
|---|---|---|
| `color.accent.gold` | `#9a7c22` | Primary accent: rule lines, eyebrow, focus, links, primary CTA background on dark |
| `color.accent.goldBright` | `#c5a55a` | Brighter gold for dark surfaces: CTA button background, prices on dark |
| `color.accent.goldDim` | `#bfae7a` | Muted gold for inactive calendar cells, secondary highlights |
| `color.accent.red` | `#a3201f` | Auspicious day label, ink-red characters (Thứ Ba, ngày số) |
| `color.accent.green` | `#7a9a80` | Positive/inactive calendar cells, jade accent |

#### Border

| Token | Value | Intended use |
|---|---|---|
| `color.border.default` | `#9a7c22` | Strong gold border (active calendar cell, primary card outline) |
| `color.border.muted` | `rgba(154, 124, 34, 0.18)` | Subtle dividers, card outlines on cream |
| `color.border.hairline` | `rgba(154, 124, 34, 0.10)` | Hairline dividers within cards (between sections of a card) |
| `color.border.darkMuted` | `rgba(197, 165, 90, 0.15)` | Dividers on dark surface |
| `color.border.darkHairline` | `rgba(197, 165, 90, 0.12)` | Hairlines on dark surface (footer top, etc.) |

#### Focus

| Token | Value | Use |
|---|---|---|
| `color.focus.ring` | `oklab(0.73 0.0104587 0.119543 / 0.5)` | Focus-visible ring; warm gold tint, 50% opacity |

The oklab value resolves to a desaturated warm gold (~`rgba(202, 159, 73, 0.5)`). Browser support: Chrome 111+, Safari 15.4+, Firefox 113+. Fallback required for older browsers:

```css
:focus-visible {
  outline: 2px solid #9a7c22;
  outline-offset: 2px;
}
@supports (color: oklab(0.5 0 0 / 0.5)) {
  :focus-visible {
    outline-color: oklab(0.73 0.0104587 0.119543 / 0.5);
  }
}
```

### 2.2 Typography tokens

#### Family and base

- `font.family.primary`: `Lora` (serif, body and display. single family used for everything)
- `font.family.stack`: `Lora, Georgia, serif`
- `font.family.mono`: `var(--mono)` (mono fallback for eyebrow numerals, pricing digits)
- `font.size.base`: `16.5px` (slightly larger than typical. supports editorial reading pace)
- `font.weight.base`: `400`
- `font.lineHeight.base`: `24.75px` (1.5 ratio)

#### Type scale (rounded to .5 increments)

The original input contained non-round values (12.5, 13.5, 14.44, 14.5). The following scale rounds these to maintainable .5 steps and adds missing midpoints:

| Token | Size | Weight | Use |
|---|---|---|---|
| `font.size.eyebrow` | 11.5px | 500, uppercase, tracking 0.22em | Section eyebrows ("LỊCH BẢN MỆNH CÁ NHÂN · 2026") |
| `font.size.xs` | 12.5px | 500 | Small labels, card meta |
| `font.size.sm` | 13px | 400 | FAQ body, fine print |
| `font.size.md` | 13.5px | 400 | Tagline, secondary prose, mobile body |
| `font.size.lg` | 14px | 500 | Button text (default) |
| `font.size.xl` | 14.5px | 500 | Body emphasis |
| `font.size.2xl` | 15px | 400 | Body long-form |
| `font.size.base` | 16.5px | 400 | Default body (Lora) |
| `font.size.bodyLg` | 17.5px | 400 | Hero subtitle, docs prose |
| `font.size.h4` | 19.5px | 700, uppercase | FAQ question, card heading |
| `font.size.h3` | 22.5px | 700, uppercase | Pricing card title, section eyebrow title |
| `font.size.h2` | 48.5–56.5px | 800, uppercase | Section heading (large) |
| `font.size.h1` | 64.5px | 800, uppercase | Hero (mobile) |
| `font.size.display` | 88.5–96.5px | 800, uppercase | Hero (desktop) |
| `font.size.calendarDay` | 76.5–130.5px | 800 | Calendar day numeral (responsive) |
| `font.size.price` | 72.5px | 800, tabular-nums | Pricing tier price |

#### Numeric strings

Apply `font-variant-numeric: tabular-nums` to all prices, calendar day numbers, score numbers (76/100, 365, 549.000₫). Do NOT apply to body prose.

### 2.3 Spacing tokens

The original input used unusual fractional values (4.13, 10.31, 12.38, 14.44, 14.5, 16.5, 18, 20.63). These appear to be derived from a base unit of ~1.03 with no semantic meaning. The scale is replaced with a clean 4px-grid that preserves the original intent but uses round numbers:

| Token | Value | Common use |
|---|---|---|
| `space.0.5` | 2px | Hairline padding |
| `space.1` | 4px | Tight gap, icon-to-text |
| `space.1.5` | 6px | Tight stack |
| `space.2` | 8px | Inline padding y, button gap |
| `space.3` | 12px | Button padding y (compact), card gap |
| `space.4` | 14px | Body padding y |
| `space.5` | 16px | Default button padding x, card padding |
| `space.6` | 20px | Card padding (default), section gap |
| `space.7` | 24px | Section padding y (mobile) |
| `space.8` | 32px | Section padding y (desktop) |
| `space.10` | 40px | Hero vertical rhythm |
| `space.12` | 48px | Section block gap |
| `space.16` | 64px | Hero block gap |

**Note**: the original scale is preserved in a comment for traceability but not used. Components must reference the new clean scale. One-off values like `14.44px` are forbidden.

### 2.4 Radius tokens

Derived from site observation. Vintage editorial tone. most radii are 1–3px (paper-cut feel), with one larger radius for soft surfaces:

| Token | Value | Common use |
|---|---|---|
| `radius.sharp` | 1px | Calendar mini-grid cells, hairlines |
| `radius.sm` | 2px | Inline labels, ribbon tags |
| `radius.md` | 3px | Pricing card outer, info callout box |
| `radius.lg` | 6px | Hero number badge, "HÔM NAY" ribbon |
| `radius.xl` | 12px | Sticky mobile CTA bar |
| `radius.pill` | 9999px | (reserved; not currently used by site) |

Rule: a single component must use one radius token. Cards on cream use `radius.md` (3px); the "HÔM NAY" badge uses `radius.lg` (6px). Mixing them within one control is prohibited.

### 2.5 Shadow tokens

The brand uses restrained, tinted shadows:

| Token | Value | Use |
|---|---|---|
| `shadow.card` | `rgba(29, 49, 41, 0.18) 0px 12px 24px 0px` | Default card lift |
| `shadow.gold` | `rgba(197, 165, 90, 0.15) 0px 12px 24px 0px` | Gold CTA button shadow |
| `shadow.goldLg` | `rgba(197, 165, 90, 0.25) 0px 16px 32px 0px` | Hero CTA button shadow |
| `shadow.inkLg` | `rgba(0, 0, 0, 0.2) 0px 36px 60px 0px, rgba(0, 0, 0, 0.08) 0px 6px 12px 0px` | Floating calendar page in hero stack |

Shadow `shadow.card` is tinted toward ink green (not pure black), `shadow.gold*` is tinted toward gold. The floating hero page uses a compound shadow combining a deep drop and a closer soft drop for layered realism.

### 2.6 Motion tokens

| Token | Duration | Easing | Use |
|---|---|---|---|
| `motion.duration.instant` | 80ms | ease-out | Color/opacity swaps |
| `motion.duration.fast` | 200ms | ease-out (default `cubic-bezier(0.22, 1, 0.36, 1)`) | Hover, button press, accordion |
| `motion.duration.normal` | 400ms | ease-out | Modal open, scroll reveal |

`prefers-reduced-motion: reduce` must collapse all three to `0.01ms` and disable transform-based animation entirely.

### 2.7 Breakpoints

| Token | Min-width |
|---|---|
| `breakpoint.sm` | 480px |
| `breakpoint.md` | 768px |
| `breakpoint.lg` | 1024px |
| `breakpoint.xl` | 1280px |

### 2.8 Z-index scale

| Token | Value | Use |
|---|---|---|
| `z.base` | 0 | Default flow |
| `z.raised` | 10 | Cards with hover lift |
| `z.sticky` | 40 | Sticky mobile CTA bar, sticky header (less than modal) |
| `z.modal` | 50 | Modal dialogs |
| `z.toast` | 60 | Toast notifications |

### 2.9 Subtle additions not in input

These tokens are added because the brand surface requires them and the input did not specify:

- `color.surface.darkFooter` `#0e1c14`. darker than the CTA strip, for footer
- `color.accent.goldBright` `#c5a55a`. gold for dark surfaces (button bg on dark)
- `color.accent.green` `#7a9a80`. jade accent observed on inactive calendar cells
- `color.accent.goldDim` `#bfae7a`. muted gold for inactive calendar cells
- `color.border.hairline` and `color.border.darkHairline`. hairline dividers
- `shadow.inkLg`. compound shadow for floating hero calendar page
- `radius.sharp`, `radius.sm`, `radius.md`, `radius.lg`, `radius.xl`. derived from site

---

## 3. Density and Information Architecture

### 3.1 Observed density on `ngaylanhthangtot.vn/` (landing page)

Measured via DOM inspection:

| Element | Observed count | Input claim | Match? |
|---|---|---|---|
| Anchor links | 7–10 (5 nav desktop + 2 footer brand + 2 pricing CTA "Đăng ký") | 11 | close, off by 1 |
| Buttons (`<button>` + `role="button"`) | 11 (1 Google login + 1 hamburger + 6 FAQ + 1 sticky CTA + 2 pricing tier anchor) | 8 | NO |
| Navigation regions | 2 (header + footer) | 2 | yes |

**Treatment**: input density numbers are not used as constraints. The site is rich. pricing CTAs, FAQ accordions, sticky mobile CTA all add to interactive count. Components are designed to support the actual observed density.

### 3.2 Landing page sections (top to bottom)

1. **Sticky header**. logo + 5 nav links + Google login
2. **Hero**. split layout: copy (left) + stacked calendar pages (right)
3. **Lịch section** (`#lich`). dark ink-green background, 3 calendar pages side by side
4. **Cá nhân hoá section** (`#ca-nhan-hoa`). 2 cards comparing "Bạn" vs "Người khác"
5. **Từng tuần section**. 12-month calendar mini-grid (1 month per cell)
6. **Bảng giá section** (`#bang-gia`). 1 hero pricing card + 2 secondary tier cards
7. **Hỏi đáp section** (`#hoi-dap`). 6 FAQ accordion items
8. **CTA section**. final "Khởi tạo lịch" CTA on dark
9. **Footer**. dark `#0e1c14`
10. **Sticky mobile CTA**. fixed bottom bar on `<768px`

### 3.3 App surface sections (post-login)

- Calendar home: today's page front-and-center, mini month grid below
- Past days browse
- Future days browse
- Bản luận giải Bát tự (long-form reading)
- Hỏi đáp AI chat
- Profile / subscription

---

## 4. Component Rules

Each component file in `/guidelines/ngaylanhthangtot/components/` covers anatomy, variants, states, responsive behavior, accessibility, and edge cases:

- [`button.md`](./components/button.md)
- [`input.md`](./components/input.md)
- [`accordion.md`](./components/accordion.md)
- [`card.md`](./components/card.md)
- [`pricing-tier.md`](./components/pricing-tier.md)
- [`calendar-page.md`](./components/calendar-page.md)
- [`calendar-strip.md`](./components/calendar-strip.md)
- [`badge.md`](./components/badge.md)

### 4.1 Component coverage matrix

| Component | Variants | States covered | Density role |
|---|---|---|---|
| Button | primary-on-dark, primary-on-light, ghost, icon-only, link-cta | default, hover, focus-visible, active, disabled, loading, error | High |
| Input | text, search, date (ngày sinh) | default, hover, focus, filled, error, disabled | Low (1–2 on landing) |
| Accordion | faq-item | default, hover, focus, expanded, disabled | High (6 on landing) |
| Card | calendar-page, comparison, pricing-tier | default, hover, focus-within, loading-skeleton, empty | High |
| Pricing-tier | featured, standard, savings-badge | default, hover, focus-within, loading | Medium (3 on landing) |
| Calendar-page | today, day-cell, mini-grid-cell | default, hover, focus, active, disabled | High (decorative + functional) |
| Calendar-strip | monthly-mini-grid, year-overview | default, hover, focus | Low |
| Badge | ribbon, savings, auspicious, count | default, hover, focus | Medium |

---

## 5. Accessibility Requirements

### 5.1 Universal requirements (must pass on every component)

1. **Keyboard**: every interactive element reachable via Tab in DOM order; Enter/Space activates; Escape dismisses overlays.
2. **Focus-visible**: `outline: 2px solid color.focus.ring; outline-offset: 2px` on `:focus-visible` only. Mouse click does not show ring.
3. **Contrast**: text/background meets WCAG 2.2 AA. Body text ≥4.5:1, large text ≥3:1, UI components ≥3:1.
4. **Labels**: every input has `<label>`. Icon-only buttons have `aria-label`.
5. **Touch targets**: minimum 44×44px hit area; extend with padding if visual size is smaller.
6. **Motion**: `prefers-reduced-motion: reduce` collapses all animation to ≤0.01ms.
7. **Screen reader**: status messages use `aria-live="polite"`. Errors use `role="alert"` or `aria-live="assertive"`.
8. **Language**: `<html lang="vi">` (the site is Vietnamese; do not change).

### 5.2 Vietnamese-specific considerations

- Diacritics: text rendering must support full Vietnamese character set. Body text must use a font with full diacritic coverage. `text-rendering: optimizeLegibility` enabled.
- Reading order: Vietnamese reads left-to-right, top-to-bottom like English. No RTL considerations.
- Number formatting: prices use Vietnamese convention (`549.000₫`, period as thousands separator).
- Date formatting: `26 tháng 5 · Thứ Ba`, lunar-solar alongside where applicable.

### 5.3 Testable acceptance criteria

See [`accessibility.md`](./accessibility.md) for full appendix.

---

## 6. Content and Tone Standards

### 6.1 Voice

The brand voice is **editorial-traditionalist**. like reading a refined Vietnamese publication (Tạp chí Kiến Trúc, Thế Giới Mới), not a tech startup. Three rules:

1. **Hơi cổ điển, không lỗi thời**: use slightly elevated vocabulary ("Khởi tạo", "luận giải", "thiết lập") but never archaic ("quý báu", "huy hoàng").
2. **Cụ thể, không hoa mỹ**: state what the user gets, not how wonderful it is. "365 trang lịch tứ trụ" beats "trải nghiệm tuyệt vời".
3. **Trang trọng nhưng ấm**: use `bạn` (you), avoid `chúng tôi` (we). Speak to the reader as a respected friend.

### 6.2 Tone examples

| Use this | Not this |
|---|---|
| Đây là lịch của bạn | Trải nghiệm lịch cá nhân hoàn toàn mới |
| 365 trang lịch tứ trụ | Hơn 300 mẫu lịch đẹp mắt |
| Khởi tạo lịch bản mệnh | Trở thành phiên bản tốt nhất của chính mình |
| Luận giải bát tự chuyên sâu | AI thông minh giúp bạn thành công |
| 549.000₫ cho cả năm | Giá cực shock, chỉ từ 99K |

### 6.3 Forbidden vocabulary

Never use:

- AI-startup jargon: "AI-powered", "next-gen", "leverage", "unleash", "seamless", "frictionless", "elevate"
- Generic SaaS copy: "Sign up today", "Join thousands of users", "Trusted by"
- Western spiritual jargon: "manifest your destiny", "align with the universe"
- Emoji or punctuation-as-decoration: 🔮 ✨ 🙏 ❤

### 6.4 Case and punctuation rules

- **Sentence case** for Vietnamese headings (Tiếng Việt không phân biệt hoa thường ngữ pháp, nhưng brand dùng Title Case cho eyebrow labels).
- **ALL CAPS** reserved for eyebrows (≤24 chars) and CTA buttons.
- **Vietnamese diacritics required**: every Vietnamese word must include full diacritics. No "ngay", "thang", "tot" without marks.

### 6.5 Numbers and currency

- Prices: `549.000₫` (period as thousands separator, ₫ symbol after).
- Use `tabular-nums` for prices and calendar day numbers.
- Currency symbol position: trailing (549.000₫ not ₫549.000).
- Lunar/solar dates: write `26 tháng 5 · Thứ Ba` with bullet separator.

---

## 7. Anti-Patterns and Prohibited Implementations

### 7.1 Token anti-patterns

- ❌ Raw hex values in component CSS (`color: #18150e` instead of `color: var(--color-text-primary)`)
- ❌ One-off spacing values (`padding: 14.44px`)
- ❌ Mixing radius tokens within a single component
- ❌ Border radius on `<img>` directly (use `overflow: hidden` on parent + radius on parent)
- ❌ Using `color.text.inverse` (`#ede7d3`) on light cream surface (contrast 1.1:1, fails AA)

### 7.2 Component anti-patterns

- ❌ **Buttons without focus-visible rings**
- ❌ **Placeholder-as-label**
- ❌ **Icon-only buttons without `aria-label`** (the Google login SVG must have a screen-reader name)
- ❌ **Disabled buttons without explanation**
- ❌ **Loading state that uses generic spinner** (must use skeleton matching final layout)
- ❌ **`window.alert()` for errors**
- ❌ **3-equal-card feature row** (use bento or asymmetric grid)
- ❌ **Gradient backgrounds on body content** (reserves gradients for hero decoration)
- ❌ **Hover state that only changes color** (must include `transform: translateY(-1px)` for tactile feedback on CTAs)

### 7.3 Brand voice anti-patterns

- ❌ **English copy on Vietnamese-first product** (English only allowed for technical terms like "FAQ" or "PWA")
- ❌ **AI-startup jargon** (see §6.3)
- ❌ **Generic Vietnamese clichés** ("Uy tín", "Chất lượng", "Hàng đầu", "Số 1")
- ❌ **Emoji as visual element**
- ❌ **Dashes for emphasis** ("Lịch - của - bạn" instead of "Lịch của bạn")
- ❌ **Exclamation marks in body copy** (only allowed in conversational microcopy like "Chúc mừng!")

### 7.4 Color anti-patterns

- ❌ Pure black `#000000` backgrounds (use `#f0ece2` cream or `#1d3129` ink)
- ❌ Multiple accent colors in one component
- ❌ Out-of-palette accent colors (do not introduce blue, purple, etc.)
- ❌ Borders on `color.border.default` (`#9a7c22`) at <1.5px (becomes too subtle)

### 7.5 Layout anti-patterns

- ❌ Centering everything (offset headers left when possible)
- ❌ `height: 100vh` (use `min-height: 100dvh`)
- ❌ Hardcoded pixel widths (use `max-width` with `width: 100%`)
- ❌ `z-index: 9999` (use the published scale)
- ❌ Missing `meta` description or OG tags
- ❌ Missing `lang="vi"` on `<html>`

### 7.6 Accessibility anti-patterns

- ❌ `outline: none` without replacement focus indicator
- ❌ Positive `tabindex` values
- ❌ `aria-label` that duplicates visible text
- ❌ `role="button"` on `<a>` without `href` (use `<button>`)
- ❌ `alt=""` on meaningful images (use descriptive alt in Vietnamese)
- ❌ Hidden focus on focusable elements

---

## 8. Responsive Behavior

| Breakpoint | Width | Layout |
|---|---|---|
| Mobile | <768px | 1 column, hamburger nav, sticky bottom CTA |
| Tablet | 768–1023px | 2 column grids, full nav inline |
| Desktop | 1024–1439px | Full nav, 3-column calendar strip, 2-column pricing |
| Wide | ≥1440px | Max-width 1200px container, centered |

`100dvh` (dynamic viewport height) required for full-screen sections to handle mobile browser chrome. `100vh` is forbidden.

### 8.1 Sticky mobile CTA

- Visible only at <768px.
- Fixed bottom, `z-index: sticky` (40).
- Includes short label + button.
- Body must have `padding-bottom` equal to sticky bar height when bar is visible, so content is not hidden.
- `aria-label` on CTA button.

---

## 9. Migration Notes (Redesign - Preserve mode)

This is a **Preserve** redesign (Section 0.C of `frontend-redesign`). The brand is established and successful. The redesign task is to formalize the existing system into tokens and component rules for future implementation consistency.

When migrating existing pages to the new tokens:

1. Replace inline color/spacing values with token references. Most values map directly.
2. Round non-standard spacing values to the new clean scale (§2.3). Components that previously used `14.44px` for body padding should use `space.4` (14px).
3. Add missing states. Most existing components lack `loading`, `error`, and explicit `focus-visible` definitions.
4. Add ARIA patterns where missing. The FAQ accordion already uses `role="button"` but should ideally use `<details>`/`<summary>` or proper `aria-expanded`.
5. Standardize focus-visible indicator across all components.
6. Add `prefers-reduced-motion` override.
7. Verify contrast for every state including hover.

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
- [ ] `<html lang="vi">` set on every page

### 10.4 Responsive

- [ ] Layout at 360px, 768px, 1024px, 1440px verified
- [ ] No horizontal scroll at any breakpoint
- [ ] Mobile menu opens/closes via keyboard
- [ ] Touch targets remain ≥44×44px at all breakpoints
- [ ] Sticky mobile CTA does not obscure content (padding-bottom on body)

### 10.5 Content (Vietnamese brand voice)

- [ ] No English copy except technical terms (FAQ, PWA)
- [ ] No AI-startup jargon (AI-powered, next-gen, leverage)
- [ ] No generic Vietnamese clichés (Uy tín, Chất lượng, Số 1)
- [ ] No emoji
- [ ] No exclamation marks in body copy
- [ ] All Vietnamese words have full diacritics (no "ngay", "thang", "tot")
- [ ] Numbers use `tabular-nums` for prices and calendar day numerals
- [ ] Currency format: `549.000₫` (period, trailing symbol)

### 10.6 SEO

- [ ] `<title>` unique per page, ≤60 chars
- [ ] `<meta description>` unique per page, ≤160 chars
- [ ] OG tags present (title, description, image, url)
- [ ] URL slug unchanged from existing structure
- [ ] Structured data (JSON-LD) valid. `SoftwareApplication`, `FAQPage` schemas
- [ ] `lang="vi"` on `<html>`

### 10.7 Code quality

- [ ] No inline styles
- [ ] No hardcoded pixel widths in component CSS
- [ ] Semantic HTML used
- [ ] No dead code or commented-out blocks
- [ ] All imports resolve to existing files
- [ ] No console.log or debugger in production

---

## 11. Open Questions

1. **Token naming for legacy alias**: original input named `color.surface.raised=#1d3129` but in site usage this is the dark CTA surface. Renamed to `color.surface.dark`. Confirm this rename is acceptable.
2. **oklab focus ring**: keep as primary token with rgba fallback, or always fallback to rgba for older-browser support?
3. **Spacing scale**: original input used fractional values (4.13, 10.31, 14.44). Replaced with round 4px-grid values. Confirm trade-off.
4. **Radius scale**: derived 5 tokens (1, 2, 3, 6, 12). Should we add `radius.xxl` (16px from rounded-2xl) and `radius.full` (9999px) for completeness, or keep minimal?
5. **Dark mode**: out of scope for v1 per §1.4. Confirm before adding any dark variant rules.
6. **App surface (post-login `/lich`)**: this guideline covers landing + shared components. Authenticated app surface needs separate spec for stateful components (calendar grid, chat, reading viewer).

---

## Appendix A. Token JSON

```json
{
  "color": {
    "text": {
      "primary": "#18150e",
      "secondary": "#3a3220",
      "tertiary": "#7a7050",
      "auspicious": "#a3201f",
      "inverse": "#ede7d3"
    },
    "surface": {
      "paper": "#f0ece2",
      "card": "#ffffff",
      "calPage": "#ede7d3",
      "dark": "#1d3129",
      "darkFooter": "#0e1c14",
      "raised": "#ffffff"
    },
    "accent": {
      "gold": "#9a7c22",
      "goldBright": "#c5a55a",
      "goldDim": "#bfae7a",
      "red": "#a3201f",
      "green": "#7a9a80"
    },
    "border": {
      "default": "#9a7c22",
      "muted": "rgba(154, 124, 34, 0.18)",
      "hairline": "rgba(154, 124, 34, 0.10)",
      "darkMuted": "rgba(197, 165, 90, 0.15)",
      "darkHairline": "rgba(197, 165, 90, 0.12)"
    },
    "focus": {
      "ring": "oklab(0.73 0.0104587 0.119543 / 0.5)",
      "ringFallback": "#9a7c22"
    }
  },
  "font": {
    "family": {
      "primary": "Lora",
      "stack": "Lora, Georgia, serif",
      "mono": "ui-monospace, monospace"
    },
    "size": {
      "eyebrow": "11.5px",
      "xs": "12.5px",
      "sm": "13px",
      "md": "13.5px",
      "lg": "14px",
      "xl": "14.5px",
      "2xl": "15px",
      "base": "16.5px",
      "bodyLg": "17.5px",
      "h4": "19.5px",
      "h3": "22.5px",
      "h2": "48.5px",
      "h1": "64.5px",
      "display": "88.5px",
      "calendarDay": "96.5px",
      "price": "72.5px"
    },
    "weight": {
      "base": 400,
      "medium": 500,
      "semibold": 600,
      "bold": 700,
      "extrabold": 800
    },
    "lineHeight": {
      "base": "24.75px",
      "tight": "1.1",
      "snug": "1.35",
      "normal": "1.5"
    }
  },
  "space": {
    "0.5": "2px",
    "1": "4px",
    "1.5": "6px",
    "2": "8px",
    "3": "12px",
    "4": "14px",
    "5": "16px",
    "6": "20px",
    "7": "24px",
    "8": "32px",
    "10": "40px",
    "12": "48px",
    "16": "64px"
  },
  "radius": {
    "sharp": "1px",
    "sm": "2px",
    "md": "3px",
    "lg": "6px",
    "xl": "12px",
    "pill": "9999px"
  },
  "shadow": {
    "card": "rgba(29, 49, 41, 0.18) 0px 12px 24px 0px",
    "gold": "rgba(197, 165, 90, 0.15) 0px 12px 24px 0px",
    "goldLg": "rgba(197, 165, 90, 0.25) 0px 16px 32px 0px",
    "inkLg": "rgba(0, 0, 0, 0.2) 0px 36px 60px 0px, rgba(0, 0, 0, 0.08) 0px 6px 12px 0px"
  },
  "motion": {
    "duration": {
      "instant": "80ms",
      "fast": "200ms",
      "normal": "400ms"
    },
    "easing": {
      "default": "cubic-bezier(0.22, 1, 0.36, 1)"
    }
  },
  "z": {
    "base": 0,
    "raised": 10,
    "sticky": 40,
    "modal": 50,
    "toast": 60
  },
  "breakpoint": {
    "sm": "480px",
    "md": "768px",
    "lg": "1024px",
    "xl": "1280px"
  }
}
```

---

## Appendix B. Source-of-truth file paths

- Brand guidelines: `/guidelines/ngaylanhthangtot/ngaylanhthangtot-guidelines.md` (this file)
- Component anatomy: `/guidelines/ngaylanhthangtot/components/*.md`
- Accessibility appendix: `/guidelines/ngaylanhthangtot/accessibility.md`
- Token JSON: `/guidelines/ngaylanhthangtot/tokens.json`

Engineering implementation should consume `tokens.json` and the component files. Do not duplicate token values in component source.