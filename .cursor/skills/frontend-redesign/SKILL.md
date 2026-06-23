---
name: frontend-redesign
description: Upgrades existing websites and apps to premium quality. Audits current design, identifies generic AI patterns, and applies high-end design standards without breaking functionality. Includes mandatory pre-redesign audit and post-redesign validation. Works with any CSS framework or vanilla CSS.
---

# Frontend Redesign Skill

> For upgrading existing websites and apps. Not greenfield builds (use frontend-taste for that).
> Includes mandatory pre-audit before touching code, and post-audit before delivering.

---

## 0. REVIEW GATE: PRE-REDESIGN AUDIT (Mandatory)

**Before touching any code, read the existing codebase and run the full audit below.**

### 0.A Scan the Codebase
1. Identify the framework (React, Vue, Next.js, Nuxt, vanilla, etc.)
2. Identify the styling method (Tailwind, CSS modules, styled-components, vanilla CSS, etc.)
3. Identify current design patterns and component structure
4. Check `package.json` for existing dependencies
5. Check Tailwind version (v3 vs v4) before modifying config

### 0.B Audit the Current State
Document the following before proposing changes:

| Category | What to document |
|---|---|
| **Brand tokens** | Primary/accent colors, type stack, logo treatment, radii |
| **Information architecture** | Page tree, primary nav, key conversion paths |
| **Content blocks** | What exists, what's working, what's filler |
| **Patterns to preserve** | Signature interactions, recognizable hero, copy voice |
| **Patterns to retire** | AI-slop tells, broken layouts, dead links, generic stock imagery |
| **Dial reading** | Infer current VARIANCE / MOTION / DENSITY of the existing site |
| **SEO baseline** | Current ranking pages, meta titles, structured data, OG cards |

### 0.C Classify the Redesign Mode
- **Greenfield** — no existing site, or full overhaul approved → use frontend-taste instead
- **Redesign - Preserve** — modernize without breaking brand → extract tokens first, evolve gradually
- **Redesign - Overhaul** — new visual language on top of existing content → treat visuals as greenfield, preserve content/IA

If ambiguous, ask once: *"Should this redesign preserve the existing brand, or are we starting visually from scratch?"*

### 0.D Pre-Redesign Review Checklist (PASS GATE)
Before touching code:
- [ ] Framework and styling method identified
- [ ] Existing brand tokens extracted
- [ ] Redesign mode classified (preserve vs overhaul)
- [ ] SEO baseline documented (URLs, meta, structured data)
- [ ] Accessibility baseline noted (focus states, alt text, keyboard nav)
- [ ] Analytics dependencies identified (button names, form field names, section IDs)
- [ ] Dial reading performed on existing site

### 0.E What Never Changes Without Explicit Approval
- URL structure / route slugs
- Primary nav labels
- Form field names or order
- Brand logo or wordmark
- Existing legal / consent / cookie copy

---

## 1. DESIGN AUDIT (Full Checklist)

### 1.A Typography
- [ ] Browser defaults or Inter everywhere? Replace with font that has character
- [ ] Headlines lack presence? Increase size, tighten tracking, reduce leading
- [ ] Body text too wide? Limit to ~65 characters, increase line-height
- [ ] Only Regular (400) and Bold (700)? Introduce Medium (500) and SemiBold (600)
- [ ] Numbers in proportional font? Use `font-variant-numeric: tabular-nums` or monospace
- [ ] All-caps subheaders everywhere? Try lowercase italics or sentence case
- [ ] Orphaned words on last line? Apply `text-wrap: balance` or `text-wrap: pretty`

### 1.B Color and Surfaces
- [ ] Pure `#000000` background? Replace with off-black (#0a0a0a, #121212, tinted dark)
- [ ] Oversaturated accent colors? Desaturate below 80%
- [ ] More than one accent color? Pick ONE
- [ ] Mixing warm and cool grays? Stick to one family
- [ ] AI-purple/blue gradient aesthetic? Replace with neutral bases + single accent
- [ ] Generic box-shadow? Tint shadows to match background hue
- [ ] Flat design with zero texture? Add subtle noise, grain, or micro-patterns
- [ ] Perfectly even gradients? Use radial gradients or mesh instead
- [ ] Random dark sections in light mode page (or vice versa)? Commit to one theme
- [ ] Empty flat sections with no visual depth? Add background imagery or subtle patterns

### 1.C Layout
- [ ] Everything centered and symmetrical? Break with offset margins or left-aligned headers
- [ ] Three equal card columns as feature row? Replace with 2-column zig-zag, asymmetric grid, or masonry
- [ ] Using `height: 100vh` for full-screen sections? Replace with `min-height: 100dvh`
- [ ] Complex flexbox percentage math? Replace with CSS Grid
- [ ] No max-width container? Add ~1200-1440px container with auto margins
- [ ] Uniform border-radius on everything? Vary radius across elements
- [ ] No overlap or depth? Use negative margins for layering
- [ ] Missing whitespace? Double the spacing
- [ ] Dashboard always has a left sidebar? Try top navigation or floating command menu
- [ ] Buttons not bottom-aligned in card groups? Pin CTAs to card bottom

### 1.D Interactivity and States
- [ ] No hover states on buttons? Add background shift, scale, or translate
- [ ] No active/pressed feedback? Add `scale(0.98)` or `translateY(1px)` on press
- [ ] Instant transitions with zero duration? Add 200-300ms transitions
- [ ] Missing focus ring? Add visible focus indicators for keyboard nav
- [ ] No loading states? Replace spinners with skeleton loaders matching layout shape
- [ ] No empty states? Design composed "getting started" views
- [ ] No error states? Add clear inline error messages (no `window.alert()`)
- [ ] Dead links? Link to real destinations or visually disable
- [ ] No current-page indication in navigation? Style active nav link differently
- [ ] Scroll jumping? Add `scroll-behavior: smooth`

### 1.E Content
- [ ] Generic names (John Doe, Jane Smith)? Use diverse, realistic names
- [ ] Fake round numbers (99.99%, 50%, $100.00)? Use organic data (47.2%, $99.00)
- [ ] Placeholder company names (Acme, Nexus, SmartFlow)? Invent contextual names
- [ ] AI copywriting clichés (Elevate, Seamless, Unleash, Next-Gen, Game-changer)? Replace with plain language
- [ ] Exclamation marks in success messages? Remove them
- [ ] "Oops!" error messages? Be direct
- [ ] All blog post dates identical? Randomize dates
- [ ] Same avatar for multiple users? Use unique assets
- [ ] Lorem Ipsum? Write real draft copy
- [ ] Title Case on every header? Use sentence case

### 1.F Component Patterns
- [ ] Generic card look (border + shadow + white)? Remove border, or use only spacing
- [ ] Always one filled + one ghost button? Add text links or tertiary styles
- [ ] Pill-shaped "New" and "Beta" badges? Try square badges or plain text labels
- [ ] Accordion FAQ sections? Use side-by-side list or inline progressive disclosure
- [ ] 3-card carousel testimonials with dots? Replace with masonry wall or single rotating quote
- [ ] Pricing table with 3 towers? Highlight recommended tier with color, not extra height
- [ ] Modals for everything? Use inline editing or slide-over panels
- [ ] Avatar circles exclusively? Try squircles or rounded squares
- [ ] Footer link farm with 4 columns? Simplify to main paths + legal links

### 1.G Iconography
- [ ] Lucide or Feather icons exclusively? Use Phosphor, HugeIcons, or Radix
- [ ] Cliché metaphors (rocketship = Launch, shield = Security)? Use less obvious icons
- [ ] Inconsistent stroke widths? Standardize to one stroke weight
- [ ] Missing favicon? Add branded favicon
- [ ] Stock "diverse team" photos? Use real team photos or consistent illustration style

### 1.H Code Quality
- [ ] Div soup? Use semantic HTML (`<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`)
- [ ] Inline styles mixed with CSS classes? Consolidate to project styling system
- [ ] Hardcoded pixel widths? Use relative units (`%`, `rem`, `em`, `max-width`)
- [ ] Missing alt text on images? Describe content for screen readers
- [ ] Arbitrary z-index values (`9999`)? Establish clean z-index scale
- [ ] Missing meta tags? Add `<title>`, `description`, `og:image`, social sharing tags

### 1.I Strategic Omissions (What Gets Forgotten)
- [ ] No legal links (privacy policy, terms of service)?
- [ ] No "back" navigation (dead ends in user flows)?
- [ ] No custom 404 page?
- [ ] No form validation (client-side)?
- [ ] No "skip to content" link (keyboard accessibility)?
- [ ] No cookie consent (if required by jurisdiction)?

---

## 2. UPGRADE TECHNIQUES

### 2.A Typography Upgrades
- **Variable font animation** — Interpolate weight/width on scroll or hover
- **Outlined-to-fill transitions** — Text starts as stroke outline, fills on scroll entry or interaction
- **Text mask reveals** — Large type as window to video or animated imagery behind it

### 2.B Layout Upgrades
- **Broken grid / asymmetry** — Elements deliberately ignoring column structure (overlapping, bleeding off-screen)
- **Whitespace maximization** — Aggressive negative space to force focus on a single element
- **Parallax card stacks** — Sections that stick and physically stack during scroll
- **Split-screen scroll** — Two halves sliding in opposite directions

### 2.C Motion Upgrades
- **Smooth scroll with inertia** — Decouple scrolling from browser defaults for cinematic feel
- **Staggered entry** — Elements cascade in with slight delays combining Y-translation + opacity fade
- **Spring physics** — Replace linear easing with spring-based motion
- **Scroll-driven reveals** — Content entering through expanding masks, wipes, or SVG paths tied to scroll

### 2.D Surface Upgrades
- **True glassmorphism** — `backdrop-filter: blur` + 1px inner border + subtle inner shadow
- **Spotlight borders** — Card borders that illuminate under cursor
- **Grain and noise overlays** — Fixed `pointer-events-none` overlay with subtle noise
- **Colored tinted shadows** — Shadows carry the hue of the background, not pure black

---

## 3. FIX PRIORITY

Apply in this order for maximum visual impact with minimum risk:

1. **Font swap** — biggest instant improvement, lowest risk
2. **Color palette cleanup** — remove clashing or oversaturated colors
3. **Hover and active states** — makes the interface feel alive
4. **Layout and spacing** — proper grid, max-width, consistent padding
5. **Replace generic components** — swap cliché patterns for modern alternatives
6. **Add loading, empty, and error states** — makes it feel finished
7. **Polish typography scale and spacing** — the premium final touch

---

## 4. REVIEW GATE: POST-REDESIGN AUDIT (Mandatory)

**After applying changes and before delivering, verify ALL of the following:**

### 4.A Functionality Preserved
- [ ] Existing navigation works correctly (all links functional)
- [ ] Forms submit and validate correctly
- [ ] No broken links introduced
- [ ] Analytics events still firing correctly (no renamed buttons/fields/IDs)
- [ ] Focus states, alt text, keyboard nav not regressed
- [ ] Mobile layout functions correctly

### 4.B Design Quality
- [ ] No new AI-default patterns introduced during upgrade
- [ ] Font has character (not browser default or generic Inter)
- [ ] Color palette unified (one accent, consistent gray family)
- [ ] Spacing doubled (sections breathe, not cramped)
- [ ] Hover states on all interactive elements
- [ ] Active/pressed feedback on buttons
- [ ] Smooth transitions on interactive elements (not instant)
- [ ] Visible focus rings for keyboard navigation
- [ ] Loading, empty, and error states designed

### 4.C Accessibility
- [ ] Alt text on all meaningful images
- [ ] Color contrast passes WCAG AA (4.5:1 body, 3:1 large text)
- [ ] Focus order logical
- [ ] Skip-to-content link present
- [ ] No `alt=""` or `alt="image"` on meaningful images

### 4.D SEO Preserved
- [ ] Meta titles unchanged
- [ ] Meta descriptions unchanged
- [ ] OG tags unchanged
- [ ] URL structure unchanged
- [ ] Structured data intact

### 4.E Code Quality
- [ ] No inline styles introduced
- [ ] No hardcoded pixel widths introduced
- [ ] Semantic HTML used
- [ ] No dead/commented-out code left behind
- [ ] All imports actually exist in package.json

---

## 5. RULES

- Work with the existing tech stack. Do not migrate frameworks or styling libraries
- Do not break existing functionality. Test after every change
- Before importing any new library, check package.json first
- Keep changes reviewable and focused. Small, targeted improvements over big rewrites
- Honor accessibility wins already in place. Do not regress focus states, alt text, keyboard nav
