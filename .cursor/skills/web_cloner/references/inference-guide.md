# Reverse-Engineering & Inference Guide

**Purpose:** The user gives you only a **screenshot (one or several)** or a **webpage URL** — never source code. Your job is to *visually analyze* the input, *infer* every slot the master clone-prompt template needs, and *emit a finished, deterministic clone prompt* in the house style learned from the 11 reference prompts.

The reference prompts achieve 1:1 fidelity by pinning: exact stack → identity sentence → design tokens (fonts/colors/CSS utilities) → sections in DOM order with per-element Tailwind strings + verbatim copy + numeric motion params → shared components → responsive → recap. **You must reproduce that shape even though you are inferring, not transcribing.** When you can't know a value exactly, you still emit an *exact-looking* value (a specific hex, a specific ms delay) plus a quiet `[inferred]` marker — never vague prose like "large rounded corners." Keep the authorization boundary explicit: third-party original assets/copy are internal reference material unless the user owns or has permission to publish them.

---

## 0. The slot inventory you must fill

Every emitted clone prompt targets these slots (derived from the 11 anatomies). Each row says **where the value comes from** in screenshot vs URL mode.

| Slot | Screenshot source | URL source |
|---|---|---|
| Build sentence (stack + product name + section map + key libs + aesthetic) | Inferred wholesale | Inferred + DOM-confirmed section count |
| Product name / brand | Read the wordmark text; else invent + flag | Read `<title>`, logo `alt`, nav |
| Tech stack | Default policy (§2) | Sniff framework (§3.1); still emit a clean target stack |
| Fonts → **concrete loadable font + real load URL** | Shape-match to a real font, source it (§1.3 / font-matching.md) — **never a placeholder** | `getComputedStyle` / `<link>` / `@font-face` (§3.2) |
| Color tokens (bg/text/accent/border, by role + exact hex) | Eyedropper-estimate (§1.4) | Computed colors → exact hex (§3.3) |
| Custom CSS utilities (glass/noise/gradient-text) | Detect visually (§1.6) | Inspect CSS, else detect visually |
| Assets → **zero-user-work media specs** | Write generation briefs by default (§4 / asset-sourcing.md) — **never `REPLACE-ME`** | Pin stable public original URLs first for authorized/internal use; for third-party public release mark originals as replace-before-production, otherwise generation brief + optional fetch-only fallback |
| Section inventory & order | Count visual bands top→bottom (§1.1) | DOM `<main>/<section>/<article>` landmark walk (§3.5) |
| Per-element Tailwind class strings | Infer from measured proportions (§1.2) | Infer; optionally cross-check computed box |
| Verbatim copy | **Transcribe exactly** (§1.7) | **Transcribe exactly** from DOM text |
| Motion (entrance/scroll/hover/mouse/canvas) | Assume by archetype (§1.5) | Inspect scripts/styles/rendered state for custom elements, canvas/WebGL, GSAP/Lenis, `pointermove`, `requestAnimationFrame`, `fontVariationSettings`, scroll timelines (§3.6–3.7) |
| Responsive behavior | Infer breakpoint ladder (§1.8) | Resize-inspect if possible, else infer |
| Page title | Brand + tagline | `<title>` verbatim |

---

## 1. Visual-Analysis Checklist (screenshot → slots)

Work **top-to-bottom, outside-in**: page-level globals first, then each section, then each element inside it. Narrate in DOM order so the emitted prompt is assemblable in one pass.

### 1.0 Screenshot frame registry — the screenshot is the source of truth

Screenshot mode cannot read source code, but it still requires evidence-based comparison. Before inference, register every uploaded image as a reference frame:

```
REFERENCE_FRAME_01: filename, viewport/aspect, visible section(s), scroll position if inferable, exact visible crop boundaries.
REFERENCE_FRAME_02: ...
```

**Rules:**
- If one screenshot is a full viewport, treat it as the exact target for that visible screen; do not "improve" it with plausible layout changes.
- If multiple screenshots are same page sections, preserve order and compare each screen after implementation.
- If a screenshot is truncated, visible pixels remain exact; below-fold completion is inferred separately and labeled.
- If the screenshot contains hover/open/modal/menu states, record that state explicitly and require a matching clone screenshot for it.
- In prompt output, include a **Reference Frames / Visual Regression Targets** block so the consuming AI knows which screenshots it must match.
- In implementation-confirmed runs, capture clone screenshots at matching viewport/aspect and compare against every `REFERENCE_FRAME_N`, not only the hero.

### 1.1 Section count & order

- Scan for horizontal "bands" separated by background-color change, full-width media, or large vertical whitespace. Each band = one `### SECTION N`.
- A single tall screenshot that fills the viewport with one composition (nav + headline + CTA over one background) can mean two different scopes:
  - User asks for **hero / first screen / only what is shown** → emit a one-section hero prompt. Do not invent below-the-fold content.
  - User asks for **page / site / landing page / website** → treat the screenshot as a truncated capture of a longer page. Recreate the visible hero exactly, then infer the rest of the landing page from nav labels, industry, visible visual system, and common landing-page information architecture. Mark inferred sections as `[inferred from visible design system]`, but still specify exact class strings, copy, media briefs, and motion.
- If the screenshot shows a **site inside a centered frame/mockup with visible outer backdrop** (e.g. rounded page shell, browser/device frame, blurred lifestyle background around the page), treat that outer presentation context as part of the clone unless the user explicitly asks for the raw website only. Emit a `GLOBAL PAGE FRAME` block before sections: body backdrop, shell width, shell radius, shadows, top/bottom spacing, and whether section corners are clipped by the frame.
- Name each section by its job: `Hero`, `Capabilities`/`Features`, `About`, `Marquee`, `Services`, `Projects`, `Footer`. Emit a `SECTION ORDER` manifest before detailing.
- **Fixed/sticky nav** is its own block layered over section 1 (note `z-50`), not a section.

### 1.1b Truncated screenshot → full landing-page extrapolation

When scope is a full landing page but the screenshot is cut off, infer a complete structure instead of stopping at the visible crop.

**Use this priority order:**
1. **Visible nav labels** become the section map.
2. **Visible sections** keep exact placement and copy; inferred sections reuse their typography, spacing, radii, icon style, media treatment, and color rhythm.
3. **Industry conventions** fill content type, not visual style.
4. **Copy policy:** visible copy is verbatim; inferred copy may be generated but must be marked `[inferred copy]`.
5. **Asset policy:** every inferred image still gets a full generation brief derived from the visible asset grammar.
6. **Layout balance policy:** inferred sections must pass a visual-balance sanity check before emission.

### 1.2 Layout grid & containers

- Estimate the column structure of each section: single centered column (`text-center`, `max-w-*`), 2-column split (`lg:grid lg:grid-cols-2`), 8/4 asymmetric grid, or a card row (`grid-cols-3`). Express as the explicit column count.
- Read content **anchor**: top-aligned hero vs **bottom-aligned** hero (content pushed down via `flex-1 ... justify-end`).
- Note inset/padding rhythm: full-bleed vs an "inset" rounded container (`p-4 md:p-6`, `rounded-[2rem]`).
- Convert proportions to a responsive padding ladder: `px-6 md:px-12 lg:px-16` is the safe default.
- For floating side labels, dates, `EST.`, section numbers, and similar microcopy, anchor them to the exact element they visually align with.
- If a photographic/mockup image overlaps or blocks a title, wordmark, CTA, or section boundary, treat that as a **state in motion**.
- If the hero uses **layered landscape occlusion**, map it as a depth stack.
- Run a **layout QA line** for every inferred section.

### 1.3 Fonts — match to a CONCRETE, LOADABLE font (never a placeholder)

| Font Type | Suggested Fonts |
|---|---|
| High-contrast didone / fashion serif | Playfair Display, Cormorant |
| Swash/script | Great Vibes, Pinyon Script |
| Geometric/condensed heavy uppercase | Oswald, Anton, Bebas Neue |
| Clean geometric UI | Inter, Manrope, Geist |
| Monospace technical | JetBrains Mono, Space Mono |
| Old-style serif body | Lora, Source Serif, Merriweather |

Emit each as `family + weights + real load URL + role`. **Never write `[inferred, swap]`.**

### 1.4 Color palette — read approximate hex

Identify **background**, **primary text**, **secondary text**, **accent/CTA**, **border/glass tint** — each as an exact hex *with the surface it paints*.

- Dark cinematic pages: emit `#000000`, `#010101`, or `#0C0C0C`
- Cream/off-white text: `#E1E0CC` / `#DEDBC8`
- The **one saturated accent** is the highest-value pin

### 1.5 Motion — what to assume from a STATIC frame

A screenshot has no motion, so **infer by archetype** and emit concrete numbers:

- **Background media moving?** If the bg is photographic/cinematic and full-bleed, infer **motion language**: drone push, slow orbit, parallax pan, Ken Burns.
- **Entrance animations (always assume for hero content):**
  - Word/line **blur-rise**: `initial {filter: blur(10px), opacity:0, y:20} → easeOut`
  - **Fade-up**: `y:20→0, opacity 0→1`, duration `0.8s`
  - **Staggered cascade** down the hero
- **Scroll-driven**: progressive text opacity reveal (`useScroll`)
- **Hover micro-interactions**: CTA `hover:scale-105 active:scale-95`
- **Shared easing default:** `cubic-bezier(0.22, 1, 0.36, 1)` or `[0.16, 1, 0.3, 1]`

### 1.6 Backgrounds & signature visual effects

- **Glassmorphism / "liquid glass"**: frosted translucent panels with a faint bright top-edge. Emit the full recipe.
- **Gradient-clipped metallic text:** via `background-clip:text`
- **Film grain:** SVG `feTurbulence` noise overlay

### 1.7 Copy — transcribe verbatim (non-negotiable)

Transcribe **every visible string exactly**, character-for-character. Preserve casing quirks, punctuation, em-dashes, separators.

### 1.8 Responsive behavior

Emit a mobile-first ladder even from one desktop frame: typography `text-4xl md:text-5xl lg:text-6xl xl:text-7xl`; padding `px-5 sm:px-8 lg:px-12`.

---

## 2. Tech-stack default policy

Emit a clean, modern target stack rather than guessing the original's build:
- **Default:** `React 18 + TypeScript + Vite + Tailwind CSS`, `lucide-react` for icons.
- **Add Framer Motion** if you inferred any non-trivial entrance/scroll motion.
- **Hand-rolled CSS `@keyframes`** instead, if the page is animation-light.

---

## 3. URL case — what to fetch & inspect

### 3.1 Framework sniff

Look for `__NEXT_DATA__`, `/_next/`, `data-reactroot`, `wp-content`, Webflow classes.

### 3.2 Fonts (exact)

`getComputedStyle(el).fontFamily` → real family names + roles. Read `<link>` Google Fonts hrefs verbatim.

### 3.3 Colors (exact)

`getComputedStyle` for `backgroundColor`, `color`, `borderColor` on key nodes; convert rgb→hex.

### 3.4 Assets (URL mode: stable originals first, briefs for gaps)

Extract `<img>`/`video`/`source` src, `srcset`, and CSS `background-image: url(...)`. Keep **full URLs including query params**.

### 3.5 DOM section structure

Walk `<header>/<main>/<section>/<article>/<footer>` and obvious top-level wrapper divs.

### 3.6 URL motion source audit

Search HTML/CSS/JS for:
```
canvas, webgl, ogl, three, shader, customElements.define,
pointermove, mousemove, requestAnimationFrame, gsap, ScrollTrigger, lenis,
fontVariationSettings, useScroll, scrollYProgress
```

### 3.7 Complexity triage — ask before promising impossible 100%

Classify the original:
```
complexity: simple DOM/CSS | DOM+GSAP/smooth-scroll | canvas/WebGL shader | full 3D engine | video/physics
success_target: 100% replica | high-fidelity reimplementation | static/partial approximation
risk_items: exact engine unavailable, private shader, inaccessible assets
```

---

## 4. Assets — the consuming AI MATERIALIZES them, never `REPLACE-ME`

**Priority order:**

1. **URL MODE DEFAULT → pin stable original URLs.** Public same-origin/CDN images, videos, fonts become primary assets.
2. **SCREENSHOT MODE DEFAULT / URL GAP FALLBACK → write a generation brief.**
3. **OPTIONAL fallback → one real free-stock URL per generated asset** for fetch-only tools.
4. **Only for screenshot pixel-exact 1:1 → crop from the screenshot** (last resort).
5. **Icons:** prefer `lucide-react` named icons.

Emit a **"素材清单 / Asset manifest"** at the top of the prompt.

---

## 5. Ask vs. infer — the decision rule

**Infer/resolve it yourself (don't ask)** for: exact motion timings, hex within a readable family, responsive breakpoint ladder, font weights, the concrete font, all assets.

**Ask a short clarifying question (max 2–3, batched) only when:**
- Scope/section count is ambiguous
- Multiple screenshots — confirm if sequential or alternatives
- Real brand vs. fictional

---

## 6. Emission rules (so the inferred prompt stays deterministic)

- **Lead with the one-sentence identity line:** STACK → PRODUCT NAME → SECTION MAP → KEY LIBS → AESTHETIC
- **Tokens before sections:** Fonts block, Color-system block, Custom-CSS-utility blocks
- **Assets are zero-user-work** (§4)
- **Sections in DOM order**
- **Hoist repeated behavior into named components**
- **Every value is a literal**
- **Add negative constraints**
- **Close with a guardrail block**
- **Flag inferred-vs-known**

---

## 7. Quick Reference

### Screenshot → slots checklist:
1. [ ] Register every screenshot as REFERENCE_FRAME_N
2. [ ] Count sections (visible + inferred)
3. [ ] Estimate grid/columns
4. [ ] Match fonts to concrete names + URLs
5. [ ] Read approximate hex values with roles
6. [ ] Detect liquid-glass/noise/gradient effects
7. [ ] Write generation briefs for all assets
8. [ ] Transcribe copy verbatim
9. [ ] Infer motion from archetype
10. [ ] Define responsive breakpoint ladder

### URL → slots checklist:
1. [ ] Sniff framework
2. [ ] Read computed fonts verbatim
3. [ ] Read computed colors verbatim
4. [ ] Extract stable asset URLs
5. [ ] Walk DOM for section structure
6. [ ] Audit motion primitives
7. [ ] Capture opening sequence
8. [ ] Complexity triage if needed
