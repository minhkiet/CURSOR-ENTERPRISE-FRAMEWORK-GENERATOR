---
name: frontend-taste
description: Anti-slop frontend skill for landing pages, portfolios, and redesigns. Reads the brief, infers the design direction, sets three dials (VARIANCE/MOTION/DENSITY), and ships interfaces that do not look templated. Includes mandatory pre-review and post-review checkpoints before and after code generation.
---

# Taste Frontend Skill (Anti-Slop Edition)

> For landing pages, portfolios, and redesigns. Not dashboards, not data tables, not multi-step product UI.
> Every rule below is **contextual**. None fires automatically. Read the brief first, then pull only what fits.

---

## 0. REVIEW GATE: PRE-CODE AUDIT (Mandatory)

**Before writing any code, run the pre-review audit. Nothing ships past this gate without passing.**

### 0.A Brief Inference
1. **Page kind** - landing (SaaS / consumer / agency / event), portfolio (dev / designer / creative studio), redesign (preserve vs overhaul), editorial / blog.
2. **Vibe words** - "minimalist", "calm", "Linear-style", "Awwwards", "brutalist", "premium consumer", "Apple-y", "playful", "serious B2B", "editorial", "agency-y", "glassy", "dark tech".
3. **Reference signals** - URLs linked, screenshots pasted, products named, brands competing with.
4. **Audience** - B2B procurement panel vs. design-conscious consumer vs. recruiter scanning a portfolio.
5. **Brand assets that exist** - logo, color, type, photography. For redesigns: starting material, not optional.
6. **Quiet constraints** - accessibility-first, public-sector, regulated industries, trust-first commerce. These OVERRIDE aesthetic preference.

### 0.B Declare Design Read (one line)
Before any code: **"Reading this as: \ for \, with a \ language, leaning toward \."**

Examples:
- *"Reading this as: B2B SaaS landing for technical buyers, with a Linear-style minimalist language, leaning toward Tailwind + Geist + restrained motion."*
- *"Reading this as: solo designer portfolio for hiring managers, with an editorial / kinetic-type language, leaning toward native CSS + scroll-driven animation."*
- *"Reading this as: redesign of a public-sector service site, with a trust-first language, leaning toward GOV.UK Frontend."*

### 0.C Ambiguous Brief Protocol
If the brief genuinely diverges on design direction, ask **one** clarifying question. Do not guess.

### 0.D Anti-Default Discipline (Pre-Code Check)
Explicitly reject these defaults before proceeding:
- AI-purple gradients / centered hero over dark mesh
- Three equal feature cards / generic glassmorphism everywhere
- Inter + slate-900 / infinite-loop micro-animations everywhere
If any of these appear in the draft plan, eliminate them.

### 0.E Design System Check (Pre-Code)
Does the brief match an official design system? If so, use the official package.

| Brief reads as... | Reach for | Why |
|---|---|---|
| Microsoft / enterprise SaaS | `@fluentui/react-components` | Official Fluent UI, accessibility done |
| Google-ish / Material-flavored | `@material/web` | Official, theme-able via Material Theming |
| IBM-style B2B / analytics | `@carbon/react` | Official Carbon |
| Shopify app surfaces | `polaris.js` | Required for Shopify admin UI |
| GitHub-style devtool | `@primer/css` | Official Primer |
| Public-sector UK | `govuk-frontend` | Legally expected |
| US public-sector | `uswds` | Same |
| Modern accessible React | `@radix-ui/themes` | Primitives + polished theme |
| Modern SaaS | `shadcn/ui` (`npx shadcn@latest add ...`) | Own the code |
| Tailwind-based modern SaaS / AI | Tailwind v4 + `dark:` variant | Default for indie builds |

**Honesty rule:** if the brief matches a system above, install and use the **official** package. Do not recreate its CSS by hand.

### 0.F Pre-Code Review Checklist (PASS GATE)
Before touching code, verify ALL of:

- [ ] Design read declared (Section 0.B)
- [ ] No AI-default patterns in draft plan (0.D checked)
- [ ] Design system selected if applicable (0.E)
- [ ] Dial values set: VARIANCE (1-10), MOTION (1-10), DENSITY (1-10)
- [ ] If redesign: audit performed (see redesign-skill)
- [ ] Hero plan fits viewport (headline max 2 lines, subtext max 20 words)
- [ ] Section layout diversity planned (no 3+ consecutive same-layout sections)

---

## 1. THE THREE DIALS

After the design read, set three dials. These gate every decision below.

| Dial | 1 | 5 | 10 |
|------|---|---|-----|
| DESIGN_VARIANCE | Perfect Symmetry | Offset | Artsy Chaos |
| MOTION_INTENSITY | Static | Fluid CSS | Cinematic / Physics |
| VISUAL_DENSITY | Art Gallery | Daily App | Cockpit |

**Baseline:** `VARIANCE: 8 / MOTION: 6 / DENSITY: 4`. Use these unless the design read overrides.

### Dial Inference (signal → value)

| Signal | VARIANCE | MOTION | DENSITY |
|---|---|---|---|
| "minimalist / clean / calm / editorial" | 5-6 | 3-4 | 2-3 |
| "premium consumer / Apple-y / luxury" | 7-8 | 5-7 | 3-4 |
| "playful / wild / Awwwards / experimental" | 9-10 | 8-10 | 3-4 |
| "landing page / marketing (default)" | 7-9 | 6-8 | 3-5 |
| "trust-first / public-sector" | 3-4 | 2-3 | 4-5 |

---

## 2. STACK & CONVENTIONS

### 2.A Framework Defaults
- **React / Next.js** - default to Server Components (RSC)
- **RSC SAFETY:** Global state works ONLY in Client Components
- **Styling:** **Tailwind v4** (default). Use `@tailwindcss/postcss` or Vite plugin (NOT the `tailwindcss` plugin in postcss.config)
- **Animation:** **Motion** from `motion/react`. Legacy alias `framer-motion` still works.
- **Fonts:** Use `next/font` (Next.js) or self-host with `@font-face` + `font-display: swap`. Never link Google Fonts via `<link>` in production.

### 2.B Icons
- **Allowed:** `@phosphor-icons/react`, `hugeicons-react`, `@radix-ui/react-icons`, `@tabler/icons-react`
- **Discouraged:** `lucide-react` (acceptable only if explicitly asked or already in project)
- **NEVER hand-roll SVG icons.** Compose from library glyphs.
- **One family per project.** Never mix Phosphor + Lucide in the same tree.
- **Standardize strokeWidth** globally (e.g. 1.5 or 2.0)

### 2.C State
- Local `useState` / `useReducer` for isolated UI
- Global state: Zustand, Jotai, or React context
- **NEVER use useState for continuous values** (mouse position, scroll progress, magnetic hover). Use Motion's `useMotionValue` / `useTransform` / `useScroll`

### 2.D Dependency Verification
Before importing ANY 3rd-party library, check `package.json`. If missing, output the install command first.

---

## 3. DESIGN ENGINEERING DIRECTIVES

### 3.1 Typography
- **Display:** `text-4xl md:text-6xl tracking-tighter leading-none`
- **Body:** `text-base text-gray-600 leading-relaxed max-w-[65ch]`
- **Sans fonts:** Default away from Inter. Pick `Geist`, `Outfit`, `Cabinet Grotesk`, `Satoshi`
- **SERIF RULE:** Serif is NOT the default. Only acceptable when brand brief names a serif, OR aesthetic is genuinely editorial / luxury / publication. **Banned as default:** Fraunces, Instrument_Serif
- **EMPHASIS:** Use italic/bold of the SAME font family. Do NOT mix serif into sans headlines
- **EM-DASH BAN:** The em-dash character (`—`) is completely banned. Use period, comma, colon, or parentheses. Zero tolerance

### 3.2 Color
- Max 1 accent color. Saturation < 80% by default
- **THE LILA RULE:** No automatic AI-purple/blue glow. Use neutral bases (Zinc/Slate/Stone) with high-contrast singular accents
- **One palette per project.** Do not fluctuate between warm and cool grays within the same project
- **PREMIUM-CONSUMER BAN:** Banned as default: warm beige/cream backgrounds + brass/clay/oxblood accents + espresso text (#f5f1ea, #b08947, #1a1714 families). Default alternatives: Cold Luxury (silver-grey + chrome), Forest (deep green + bone), Pure monochrome + single saturated pop
- **COLOR CONSISTENCY LOCK:** Once an accent color is chosen, use it identically across ALL sections

### 3.3 Layout
- **ANTI-CENTER BIAS:** Avoid centered Hero when `VARIANCE > 4`. Force Split Screen, Left-aligned, or Asymmetric
- **Cards:** Use ONLY when elevation communicates hierarchy. Otherwise group with `border-t`, `divide-y`, or negative space
- **SHAPE CONSISTENCY LOCK:** Pick ONE corner-radius scale per page: all-sharp (0), all-soft (12-16px), or all-pill (full). Do not mix
- **HERO TOP PADDING CAP:** Max `pt-24` at desktop
- **NAVIGATION:** Must render on ONE line at desktop. Height cap: 80px default 64-72px
- **ZIGZAG CAP:** Max 2 consecutive image+text-split sections. The 3rd consecutive is a FAIL
- **BENTO CELL COUNT:** N items → N cells. No empty cells. Grid must interlock mathematically
- **Section-Layout-Repetition:** At least 4 different layout families across 8 sections
- **EYEBROW RESTRAINT:** Max 1 eyebrow per 3 sections. Hero counts as 1
- **SPLIT-HEADER BAN:** "Left big headline + right small explainer paragraph" pattern banned. Stack vertically instead

### 3.4 Interactive States
- **Full state cycles always:** Loading (skeletal loaders), Empty States (composed), Error States (inline)
- **Tactile Feedback:** On `:active` use `scale-[0.98]` or `-translate-y-[1px]`
- **BUTTON CONTRAST CHECK (a11y):** WCAG AA min 4.5:1 for body, 3:1 for large text 18px+. Audit every CTA
- **CTA WRAP BAN:** Button text MUST fit on one line at desktop. Max 3 words for primary CTAs
- **NO DUPLICATE CTA INTENT:** "Get in touch" + "Contact us" + "Let's talk" = same intent. Pick ONE label
- **FORM CONTRAST CHECK:** All inputs, placeholders, focus rings, labels pass WCAG AA

### 3.5 Content
- **NO generic names** (John Doe, Sarah Chan, Jack Su)
- **NO fake round numbers** (99.99%, 50%, 1234567). Use organic messy data (47.2%, 31)
- **NO startup-slop names** (Acme, Nexus, SmartFlow)
- **NO filler verbs** (Elevate, Seamless, Unleash, Next-Gen, Game-changer)
- **COPY SELF-AUDIT:** Every visible string re-read for grammar, unclear referents, AI-hallucination, fake precision
- **Quotes max 3 lines.** Attribution: name + role (+ company). Use typographic quotes (" "), not ASCII

### 3.6 Images
- **Priority 1:** Image-generation tool (use it to create section assets at correct aspect ratio)
- **Priority 2:** Real photography. Use `https://picsum.photos/seed/{descriptive-seed}/{w}/{h}` with descriptive seeds
- **Priority 3:** Tell the user clearly which placeholder slots need real images
- **Real logos for social proof:** Use Simple Icons (`https://cdn.simpleicons.org/{slug}/ffffff`). Never plain text wordmarks
- **Fake screenshots:** BANNED. Use real images, generated images, real component previews, or skip the preview
- **Hand-rolled SVG icons:** Allowed from library. Strongly discouraged as custom illustration/logo

### 3.7 Data & Forms
- Label ABOVE input. Error text BELOW. Standard `gap-2`
- No placeholder-as-label. Ever
- For long lists (> 5 items): tabs, accordion, horizontal scroll-snap pills, or carousel — not default `<ul>`

---

## 4. ANIMATION & MOTION

### 4.1 Motion Intensity Rules
- **1-3 (Static):** CSS `:hover` and `:active` only. No auto-animations
- **4-7 (Fluid CSS):** `transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1)`. Staggered load-ins
- **8-10 (Advanced):** GSAP ScrollTrigger, Motion hooks, parallax, scroll-driven. NEVER `window.addEventListener('scroll')`

### 4.2 GSAP Canonical Patterns
**Sticky-Stack** (`start: "top top"`, `pin: true`, `pinSpacing: false`):
```tsx
"use client";
import { useRef, useEffect } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useReducedMotion } from "motion/react";

gsap.registerPlugin(ScrollTrigger);

export function StickyStack({ cards }: { cards: React.ReactNode[] }) {
  const ref = useRef<HTMLDivElement>(null);
  const reduce = useReducedMotion();
  useEffect(() => {
    if (reduce || !ref.current) return;
    const ctx = gsap.context(() => {
      const cardEls = gsap.utils.toArray<HTMLElement>(".stack-card");
      cardEls.forEach((card, i) => {
        if (i === cardEls.length - 1) return;
        ScrollTrigger.create({
          trigger: card,
          start: "top top",
          endTrigger: cardEls[cardEls.length - 1],
          end: "top top",
          pin: true,
          pinSpacing: false,
        });
        gsap.to(card, {
          scale: 0.92,
          opacity: 0.55,
          ease: "none",
          scrollTrigger: {
            trigger: cardEls[i + 1],
            start: "top bottom",
            end: "top top",
            scrub: true,
          },
        });
      });
    }, ref);
    return () => ctx.revert();
  }, [reduce]);
  return (
    <div ref={ref} className="relative">
      {cards.map((card, i) => (
        <div key={i} className="stack-card sticky top-0 min-h-[100dvh] flex items-center justify-center">
          {card}
        </div>
      ))}
    </div>
  );
}
```

**Horizontal-Pan** (`start: "top top"`, `end: "+=${distance}"`):
```tsx
"use client";
import { useRef, useEffect } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useReducedMotion } from "motion/react";

gsap.registerPlugin(ScrollTrigger);

export function HorizontalPan({ children }: { children: React.ReactNode }) {
  const wrap = useRef<HTMLDivElement>(null);
  const track = useRef<HTMLDivElement>(null);
  const reduce = useReducedMotion();
  useEffect(() => {
    if (reduce || !wrap.current || !track.current) return;
    const ctx = gsap.context(() => {
      const distance = track.current!.scrollWidth - window.innerWidth;
      gsap.to(track.current, {
        x: -distance,
        ease: "none",
        scrollTrigger: {
          trigger: wrap.current,
          start: "top top",
          end: () => `+=${distance}`,
          pin: true,
          scrub: 1,
          invalidateOnRefresh: true,
        },
      });
    }, wrap);
    return () => ctx.revert();
  }, [reduce]);
  return (
    <section ref={wrap} className="relative overflow-hidden">
      <div ref={track} className="flex h-[100dvh] items-center">
        {children}
      </div>
    </section>
  );
}
```

**Scroll-Reveal Stagger** (lighter alternative, prefer this over GSAP for simple reveals):
```tsx
"use client";
import { motion, useReducedMotion } from "motion/react";

export function RevealStagger({ items }: { items: string[] }) {
  const reduce = useReducedMotion();
  return (
    <ul className="grid gap-6">
      {items.map((item, i) => (
        <motion.li
          key={item}
          initial={reduce ? false : { opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.3 }}
          transition={{ duration: 0.6, delay: i * 0.06, ease: [0.16, 1, 0.3, 1] }}
        >
          {item}
        </motion.li>
      ))}
    </ul>
  );
}
```

### 4.3 Forbidden Animation Patterns
- `window.addEventListener("scroll", ...)` — HARD BAN. Use Motion `useScroll()`, GSAP ScrollTrigger, IntersectionObserver, or CSS scroll-driven animations
- Custom scroll progress using `window.scrollY` in React state — same reason
- `requestAnimationFrame` loops that touch React state — use motion values instead
- GSAP + Motion in the same component tree — they fight over frames

### 4.4 Motion Motivation Rule
Before adding any animation, ask: "what does this communicate?" Valid: hierarchy, storytelling, feedback, state transition. Invalid: "it looked cool". GSAP everywhere because GSAP is available is amateur.

### 4.5 Marquee Rule
Max ONE marquee per page.

---

## 5. PERFORMANCE & ACCESSIBILITY

### 5.A Hardware Acceleration
- Animate ONLY `transform` and `opacity`. Never `top`, `left`, `width`, `height`
- `will-change: transform` sparingly — only on actively animating elements

### 5.B Reduced Motion (Non-Negotiable)
Any motion `MOTION > 3` MUST honor `prefers-reduced-motion`. Wrap with `useReducedMotion()` and degrade to static. Infinite loops, parallax, scroll-hijack must collapse to static under reduced motion.

### 5.C Dark Mode
- Design for BOTH modes from the start. Never ship light-only or dark-only without explicit instruction
- Use Tailwind `dark:` variant OR CSS variables. Pick one strategy
- No pure `#000000` or `#ffffff` — use off-black (zinc-950) and off-white
- Respect `prefers-color-scheme` unless brand insists
- Test in BOTH modes before declaring done

### 5.D Core Web Vitals
- LCP < 2.5s. Hero image must be `next/image priority` or preloaded
- INP < 200ms. Heavy work off main thread
- CLS < 0.1. Reserve space for images, fonts, embeds
- Run Lighthouse before declaring done

### 5.E DOM Cost
- Grain/noise filters: ONLY on fixed `pointer-events-none` elements. Never on scrolling containers
- Be aware of bundle size. Lazy-load above-the-fold-only content

### 5.F Z-Index Restraint
Never spam `z-50` or `z-10`. Use z-index strictly for: sticky nav, modals, overlays, grain. Document the scale.

---

## 6. REVIEW GATE: POST-CODE AUDIT (Mandatory)

**After writing code and before delivering, run every box. If any box fails, fix it first.**

### 6.A Layout & Structure
- [ ] Design read declared at start of response?
- [ ] Dial values (VARIANCE/MOTION/DENSITY) explicit and reasoned?
- [ ] Design system selected if applicable?
- [ ] Hero fits viewport (headline max 2 lines, subtext max 20 words AND max 4 lines)?
- [ ] Hero top padding max `pt-24` at desktop?
- [ ] Hero stack discipline: max 4 text elements (eyebrow OR brand strip, headline, subtext, CTAs)?
- [ ] Navigation on ONE line at desktop, height 64-80px?
- [ ] Section layout diversity: at least 4 different layout families across 8 sections?
- [ ] Zigzag alternation cap: no 3+ consecutive same image+text-split sections?
- [ ] Bento grid: N items → N cells, no empty cells, uses `grid-flow-dense`?
- [ ] No split-header pattern ("left big headline + right small explainer paragraph")?
- [ ] Eyebrow count: `uppercase tracking` labels ≤ ceil(sectionCount / 3)?
- [ ] Mobile collapse explicit for every multi-column layout (`w-full px-4 max-w-7xl mx-auto`)?
- [ ] Viewport stability: `min-h-[100dvh]`, never `h-screen`?

### 6.B Design System & Consistency
- [ ] ZERO em-dashes (`—`) anywhere on the page. Headlines, eyebrows, pills, body, quotes, attribution, buttons, alt text. Zero
- [ ] Page theme lock: ONE theme for whole page, no mid-page inversion?
- [ ] Color consistency lock: one accent color used identically across all sections?
- [ ] Shape consistency lock: one corner-radius system applied consistently?
- [ ] No Inter as default (unless brief is public-sector / Linear-style)?
- [ ] No Fraunces / Instrument_Serif as default serif?
- [ ] Premium-consumer brief: NOT using beige+brass+oxblood+espresso palette family?
- [ ] Different serif from the previous project (if serif is used)?
- [ ] Premium-consumer: different palette family from previous premium-consumer project?

### 6.C Typography & Content
- [ ] Italic descender clearance: every italic word with y/g/j/p/q has `leading-[1.1]` min + `pb-1` reserve?
- [ ] Copy self-audit: no grammatically broken, AI-hallucinated, or filler-verb strings shipped?
- [ ] No fake-precise numbers without justification?
- [ ] No generic names (John Doe, Acme Corp, Lorem Ipsum)?
- [ ] No startup-slop brand names?
- [ ] No section-numbering eyebrows ("00 / INDEX", "001 · Capabilities", "06 · how it works")?
- [ ] No version labels in hero (V0.6, BETA, INVITE-ONLY) unless brief is a launch?
- [ ] No decoration text strip at hero bottom ("BRAND. MOTION. SPATIAL.")?
- [ ] No floating top-right sub-text in section headings?
- [ ] No scroll cues ("Scroll", "↓ scroll", "Scroll to explore")?
- [ ] No locale / city-name / weather strips unless brief is genuinely place-focused?
- [ ] No version footers on marketing pages?
- [ ] No photo-credit captions as decoration?
- [ ] No pills/labels overlaid on images?
- [ ] No decorative colored status dots (only for real semantic state)?

### 6.D CTA & Form
- [ ] Button contrast: every CTA text readable against background (WCAG AA 4.5:1)?
- [ ] CTA wrap: no label wraps to 2+ lines at desktop?
- [ ] No duplicate CTA intent on the page?
- [ ] Form contrast: all inputs, placeholders, focus rings, labels pass WCAG AA?
- [ ] Label above input, error below input?
- [ ] No placeholder-as-label?

### 6.E Assets & Images
- [ ] Real images used (gen-tool first, then Picsum-seed with descriptive seeds)?
- [ ] No div-based fake screenshots?
- [ ] No hand-rolled decorative SVG illustrations?
- [ ] Logo wall = logos only (no industry labels below logos)?
- [ ] "Trusted by / Used by" logo wall lives UNDER hero, not inside it?
- [ ] Bento background diversity: at least 2-3 cells have real visual variation (image, gradient, pattern)?

### 6.F Animation & Motion
- [ ] Motion claimed = motion shown (if MOTION > 4, page actually animates)?
- [ ] GSAP patterns use canonical skeleton (Section 4.2) with `start: "top top"`, `pin: true`?
- [ ] No `window.addEventListener('scroll')` — using Motion `useScroll()`, GSAP ScrollTrigger, or IntersectionObserver only?
- [ ] Reduced motion wrapped for all MOTION > 3?
- [ ] Dark mode tokens defined and tested in both modes?
- [ ] All animations use only `transform` and `opacity`?
- [ ] `useEffect` animations have strict cleanup functions?

### 6.G States & Polish
- [ ] Empty / loading / error states provided?
- [ ] Cards omitted in favor of spacing where elevation doesn't communicate hierarchy?
- [ ] Icons from allowed library only (no hand-rolled paths)?
- [ ] Motion isolated in client-leaf components with `'use client'` at top?
- [ ] No AI Tells from Section 9 (AI-purple, three-equal cards, Jane Doe, Acme, "Quietly in use at")?
- [ ] Dark mode: both modes designed, tokens consistent, no pure black/white?

### 6.H Performance
- [ ] Core Web Vitals plausibly hit (LCP < 2.5s, INP < 200ms, CLS < 0.1)?
- [ ] One design system per project (no Material + shadcn mixed)?
- [ ] No arbitrary z-index spam?
- [ ] Grain/noise only on fixed `pointer-events-none` layers?

---

## 7. OUT OF SCOPE

NOT for:
- Dashboards / dense product UI / admin panels (use Fluent, Carbon, Atlassian, Polaris)
- Data tables (use TanStack Table or AG Grid)
- Multi-step forms / wizards
- Code editors (use Monaco / CodeMirror)
- Native mobile (use Apple HIG / Material)
- Realtime collab UIs

If brief is one of the above, say so explicitly and apply this skill only to the surfaces where it applies.

---

## 8. DIAL TECHNICAL REFERENCE

### VARIANCE (Level 1-10)
- **1-3 (Predictable):** Symmetrical 12-col CSS Grid, centered alignment
- **4-7 (Offset):** Negative margin overlaps, varied aspect ratios, left-aligned headers
- **8-10 (Asymmetric):** Masonry, fractional units, massive empty zones
- **Mobile:** For levels 4-10, collapse to strict single-column on < 768px

### MOTION (Level 1-10)
- **1-3 (Static):** CSS hover/active only
- **4-7 (Fluid CSS):** Custom cubic-bezier transitions, stagger cascades
- **8-10 (Advanced):** GSAP ScrollTrigger, Motion hooks. HARD BAN on `window.addEventListener('scroll')`

### DENSITY (Level 1-10)
- **1-3 (Art Gallery):** Huge gaps (`py-32` to `py-48`), minimal content
- **4-7 (Daily App):** Standard spacing (`py-16` to `py-24`)
- **8-10 (Cockpit):** Tight paddings, no card boxes, 1px line separators, `font-mono` for numbers

---

## APPENDIX: INSTALL COMMANDS

```bash
# Material Web
npm install @material/web

# Fluent UI React v9
npm install @fluentui/react-components

# IBM Carbon
npm install @carbon/react @carbon/styles

# Radix Themes
npm install @radix-ui/themes

# shadcn/ui
npx shadcn@latest init
npx shadcn@latest add button card badge separator input

# Primer CSS
npm install --save @primer/css

# GOV.UK Frontend
npm install govuk-frontend

# USWDS
npm install uswds

# Motion (GSAP)
npm install motion gsap
```


---

## Liens

- [[../rules/skill-integration]] - Skill Integration Rules
- [[../rules/frontend-architecture]] - Frontend Architecture
- [[../skills/frontend-review]] - Frontend Review Skill
- [[../skills/full-output]] - Full Output Skill
