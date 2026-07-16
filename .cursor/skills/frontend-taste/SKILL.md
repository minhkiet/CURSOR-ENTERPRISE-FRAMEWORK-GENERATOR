---
name: frontend-taste
description: Anti-slop frontend skill for landing pages, portfolios, and redesigns. Reads the brief, infers the design direction, sets three dials (VARIANCE/MOTION/DENSITY), and ships interfaces that do not look templated. Includes mandatory pre-review and post-review checkpoints before and after code generation. Synthesizes pbakaus/impeccable, Leonxlnx/taste-skill, anthropics/frontend-design, vercel-labs/web-design-guidelines, nextlevelbuilder/ui-ux-pro-max, emilkowalski/emil-design-eng, and Nutlope/hallmark (9.3k stars) into a single coherent playbook. See §12 for attribution and conflict-resolution rules.
version: 1.8.0
updated: 2026-07-16
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

## 9. DESIGN-LEAD PHILOSOPHY (Two-Pass Build + Hallmark)

> Synthesized from `anthropics/frontend-design` (⭐3), `pbakaus/impeccable` (⭐1), and `Nutlope/hallmark` (⭐9.3k).
> This is the *frame of mind* behind every section above. Apply it whenever §0.B produces a non-trivial design read.

### 9.A Hallmark Integration (v1.8.0)

**Hallmark** (9.3k stars) picks a macrostructure, applies one of 20 themes, runs 57 slop-test gates. Two pages for different briefs feel like different sites.

#### 9.A.1 Hallmark Themes (20 Catalog + Custom)

Select theme based on brand brief:

| Theme | Aesthetic | Color Anchor | Example Use Cases |
|-------|-----------|-------------|------------------|
| **Hum** | Warm minimal | Soft peach + sage | Sourdough app, wellness |
| **Cobalt** | Industrial clean | Deep blue + cream | API tools, dev infra |
| **Carnival** | Vibrant bold | Rich red + gold | Record labels, creative |
| **Lumen** | Bright tech | White + electric blue | AI tools, dashboards |
| **Garden** | Natural earthy | Moss + cream | Honey farms, organic |
| **Riso** | Print-inspired | Bright spots on off-white | Print fairs, art |
| **modern-minimal** | Clean SaaS | Neutral + accent | SaaS products |
| **atmospheric** | Moody, immersive | Dark + glowing | Travel, experience |
| **arctic-frost** | Cool, crisp | Ice blue + white | Tech, fintech |
| **golden-hour** | Warm glow | Amber + cream | Lifestyle, beauty |
| **ocean-depths** | Deep, mysterious | Navy + teal | Maritime, premium |
| **desert-rose** | Earthy warmth | Terracotta + sand | Artisan, craft |
| **sunset-boulevard** | Retro warmth | Orange + purple | Entertainment |
| **dark-luxury** | Premium dark | Charcoal + gold | High-end products |
| **neo-brutalist** | Raw, bold | High contrast | Agencies, portfolios |
| **editorial-serif** | Classic print | Cream + black serif | Publications |
| **swiss-grid** | Geometric | Red + black | Corporate |
| **Custom** | Bespoke | Made-to-measure | No catalog fit |

**Theme Selection Protocol:**
```
1. Analyze brief for brand signals
2. Match to closest catalog theme OR trigger Custom
3. Derive all design tokens from selected theme
4. Run 57 slop-test gates (§9.F)
5. Self-critique before code (§9.H)
```

#### 9.A.2 Hallmark 4 Verbs (Design Actions)

| Verb | Action | When to Use |
|------|--------|-------------|
| *(default)* | Build new UI | New landing pages, portfolios |
| `hallmark audit` | Score existing code | Audit current UI for slop |
| `hallmark redesign` | Rebuild with new theme | Full redesign preserving brand |
| `hallmark study` | Extract design DNA | Study admired designs |

#### 9.A.3 Custom Theme Protocol

When no catalog theme fits:
```
1. Design from scratch (not template)
2. Bespoke palette: 4-5 hex values
3. Custom type pairing
4. Unique layout macrostructure
5. Same 57 slop-test gates apply
6. Document as "Custom" for future reference
```

#### 9.A.4 Hallmark DNA Extraction (Study Mode)

For `hallmark study` requests:
```
1. Extract MACROSTRUCTURE
   └── Layout family, section hierarchy, visual rhythm
   
2. Extract TYPE-PAIRING
   └── Display font + body font combination
   
3. Extract COLOUR ANCHOR
   └── Primary + accent + neutral base
   
4. Refuse pixel-clones
   └── Design DNA, not visual copy
   
5. Optional: Emit portable design.md
   └── For handoff to other AI tools
```

### 9.B Two-Pass Build (mandatory for landing pages and redesigns)

```
PASS 1 — BRAINSTORM (do not write code yet)
  ↓  Pick 4-6 named hex values for the palette
  ↓  Pick display + body + (optional utility) typefaces — DELIBERATE PAIRING, not default
  ↓  One-sentence layout concept
  ↓  ONE signature element the page will be remembered by
  ↓  Self-critique: is any of this the generic default for this category?
     (If yes, revise before moving on.)

PASS 2 — BUILD
  ↓  Implement exactly the revised plan
  ↓  Derive every color/type decision from the tokens — no off-token drift
  ↓  Run §6 post-review audit before declaring done
```

The two-pass discipline is the single highest-leverage rule in this skill. Most "AI-slop" output happens because the agent jumps from brief → code in one pass and never revisits the plan.

### 9.B The Signature Element

Every distinctive page has **one** memorable element that embodies the brief. Examples:
- A kinetic headline that scrubs based on scroll progress
- A real-time data visualization that responds to the cursor
- A bespoke cursor / magnetic interaction reserved for the primary CTA
- A typographic mark used as the brand's identity

The signature gets **one place** of boldness. Everything around it stays quiet and disciplined. Channel Chanel's rule: *before leaving the house, look in the mirror and remove one accessory.*

### 9.C Anti-Cream Default (color)

If the brief calls for "warm / editorial / heritage / magazine" and you reach for `#f5f1ea`, `#faf7f1`, or any OKLCH L 0.84-0.97 + low-chroma warm band — **stop**. That warm-neutral band is the saturated 2026 AI default. Token names like `--paper`, `--cream`, `--sand`, `--bone` are tells in themselves.

Instead, pick one of:
- **(a) Saturated body** — terracotta, oxblood, deep ochre, near-black as the page color
- **(b) True off-white** at chroma 0 (or chroma toward the brand's own hue, not toward warmth)
- **(c) Darker mid-tone tinted neutral** that is clearly the brand's own

The brand's "warmth" lives in accent + typography + imagery, not in body background.

### 9.D Anti-Identical-Card-Grids (layout)

Five-card row with icon-heading-text repeated five times is banned. Vary the grid: 1+2 split, 2+1 asymmetric, hero+4 with mixed cell sizes, masonry. If you have N items, you need N cells with a real composition — not 5 identical siblings.

### 9.E Display Letter-Spacing Floor

`letter-spacing` on display H1 must stay ≥ -0.04em. Anything tighter (`-0.05em` to `-0.085em`) and the letters touch. The right tight range is -0.02 to -0.03em. Use `text-wrap: balance` on h1-h3 and `text-wrap: pretty` on long prose.

### 9.F Heading Overflow Test

Long headline words + large `clamp()` scales + narrow grids cause overflow on tablet/mobile. Test the heading copy at every breakpoint; if it overflows, reduce the clamp max or rewrite the copy. The viewport is part of the design.

### 9.G Heading Ceiling

Display H1 max `clamp()` ≤ 6rem (~96px). Above that the page is shouting, not designing.

### 9.H Side-Stripe Borders (banned)

`border-left` or `border-right` > 1px as a colored accent on cards, list items, callouts, or alerts. Never intentional. Rewrite with full borders, background tints, leading numbers/icons, or nothing.

### 9.I Gradient Text (banned)

`background-clip: text` + gradient background. Decorative, never meaningful. Emphasis via weight or size, single solid color.

### 9.J Hero-Metric Template (banned)

Big number + small label + supporting stats + gradient accent. The SaaS cliché. Reject on sight.

### 9.K Reveal-Safety (motion)

Reveal animations must enhance an *already-visible default*. Do not gate content visibility on a class-triggered transition — transitions pause on hidden tabs and headless renderers, so the section ships blank. The default state must be readable; the reveal is an enhancement.

### 9.L The AI Slop Test

If someone could look at the interface and say "AI made that" without doubt, it has failed.

- **First-order check:** if a viewer could guess the theme + palette from the *category alone* (e.g. "AI workflow tool", "fintech app"), it is the first training-data reflex. Rework the scene sentence and color strategy until the answer is not obvious from the domain.
- **Second-order check:** if the viewer could guess the aesthetic family from category-plus-anti-references (e.g. "fintech that's not navy-and-gold → terminal-native dark mode"), it is the trap one tier deeper. Rework until both answers are not obvious.

### 9.M Hallmark 57 Slop-Test Gates (Automated Anti-Slop Protocol)

> Integrated from `Nutlope/hallmark` (9.3k stars). Hallmark runs 57 automated gates before emitting. These are mapped to framework rules.

#### Color Defaults Gates (12 gates)
| Gate | Check | Fail if... | Rule mapping |
|------|-------|-----------|-------------|
| C.01 | AI-purple gradient | `#667eea`, `#764ba2` gradient | `ui-visual-design §AI_SLOP_PATTERNS` |
| C.02 | Blue mesh background | Radial gradient blue/purple mesh | `ui-visual-design §AI_SLOP_PATTERNS` |
| C.03 | Em-dash overuse | More than 1 em-dash on page | `§3.1 EM-DASH BAN` |
| C.04 | Generic cream | `#f5f1ea`, `#faf7f1`, `--paper` tokens | `§9.C Anti-Cream` |
| C.05 | Warm beige palette | Beige + brass + oxblood + espresso | `§3.2 PREMIUM-CONSUMER BAN` |
| C.06 | Single accent variety | Only one accent, no semantic colors | `ui-visual-design §Color System` |
| C.07 | Neutral base consistency | Mixing warm/cool grays mid-page | `§3.2 One palette per project` |
| C.08 | Pure black/white | `#000000` or `#ffffff` | `§5.C Dark Mode` |
| C.09 | Gradient text | `background-clip: text` | `§9.I Gradient Text banned` |
| C.10 | Saturated >80% accent | Accent saturation >80% | `§3.2 Max 1 accent, <80%` |
| C.11 | Purple/blue glow | `box-shadow` with purple/blue | `§3.2 THE LILA RULE` |
| C.12 | Multiple accent colors | >1 accent color on page | `§3.2 Max 1 accent` |

#### Typography Defaults Gates (10 gates)
| Gate | Check | Fail if... | Rule mapping |
|------|-------|-----------|-------------|
| T.01 | Inter as default | Inter used without brand reason | `§3.1 Sans fonts default away from Inter` |
| T.02 | Serif as default | Fraunces/Instrument Serif without brief | `§3.1 SERIF RULE` |
| T.03 | Em-mix headlines | Serif italic in sans headlines | `§3.1 EM-PHASIS same family` |
| T.04 | Display spacing | H1 `letter-spacing` < -0.04em | `§9.E Letter-Spacing Floor` |
| T.05 | Heading overflow | Long headlines overflow viewport | `§9.F Heading Overflow Test` |
| T.06 | Heading ceiling | H1 `clamp()` > 6rem | `§9.G Heading Ceiling` |
| T.07 | Section numbering | "00 / INDEX", "001 · Capabilities" | `§6.C No section-numbering eyebrows` |
| T.08 | Filler verbs | Elevate, Seamless, Unleash, Next-Gen | `§3.5 NO filler verbs` |
| T.09 | Generic names | John Doe, Sarah Chan, Acme | `§3.5 NO generic names` |
| T.10 | Fake precision | 99.99%, 50%, 1234567 | `§3.5 NO fake round numbers` |

#### Layout Patterns Gates (15 gates)
| Gate | Check | Fail if... | Rule mapping |
|------|-------|-----------|-------------|
| L.01 | Centered hero bias | Centered hero with VARIANCE > 4 | `§3.3 ANTI-CENTER BIAS` |
| L.02 | Three equal cards | 3 cards, same icon, same structure | `§9.D Anti-Identical-Card-Grids` |
| L.03 | Split header pattern | Left big headline + right explainer | `§3.3 SPLIT-HEADER BAN` |
| L.04 | Side-stripe borders | `border-left/right` > 1px colored accent | `§9.H Side-Stripe Borders banned` |
| L.05 | Zigzag overflow | 3+ consecutive same image+text sections | `§3.3 ZIGZAG CAP` |
| L.06 | Hero top padding | `pt-32` or more at desktop | `§3.3 HERO TOP PADDING CAP` |
| L.07 | Nav overflow | Navigation doesn't fit one line | `§3.3 NAVIGATION 1 line` |
| L.08 | Nav height | Height > 80px | `§3.3 NAVIGATION height cap` |
| L.09 | Bento empty cells | Empty cells in bento grid | `§3.3 BENTO CELL COUNT` |
| L.10 | Eyebrow spam | > ceil(sectionCount / 3) eyebrows | `§3.3 EYEBROW RESTRAINT` |
| L.11 | Layout repetition | <4 layout families across 8 sections | `§3.3 Section-Layout-Repetition` |
| L.12 | Version labels | V0.6, BETA, INVITE-ONLY in hero | `§6.C No version labels` |
| L.13 | Decoration strips | "BRAND. MOTION. SPATIAL." at hero | `§6.C No decoration text` |
| L.14 | Floating sub-text | Top-right sub-text in headings | `§6.C No floating text` |
| L.15 | Scroll cues | "Scroll", "↓ scroll" in sections | `§6.C No scroll cues` |

#### Component Patterns Gates (10 gates)
| Gate | Check | Fail if... | Rule mapping |
|------|-------|-----------|-------------|
| P.01 | CTA wrap | Button text wraps to 2+ lines | `§3.4 CTA WRAP BAN` |
| P.02 | Duplicate CTA intent | "Get in touch" + "Contact us" | `§3.4 NO DUPLICATE CTA` |
| P.03 | Fake screenshots | div-based fake screenshots | `§3.6 Fake screenshots BANNED` |
| P.04 | Placeholder-as-label | Placeholder text without label | `§3.7 No placeholder-as-label` |
| P.05 | Hero-metric template | Big number + small label + gradient | `§9.J Hero-Metric Template banned` |
| P.06 | Card overuse | Cards where spacing would suffice | `§3.3 Cards only when elevation needed` |
| P.07 | Logo text wordmarks | Plain text instead of SVG logos | `§3.6 Real logos with Simple Icons` |
| P.08 | Pills on images | Labels/overlays on hero images | `§6.C No pills on images` |
| P.09 | Status dots decoration | Decorative colored status dots | `§6.C Semantic status only` |
| P.10 | Photo-credit captions | Photo credits as decoration | `§6.C No photo-credit captions` |

#### Animation Defaults Gates (10 gates)
| Gate | Check | Fail if... | Rule mapping |
|------|-------|-----------|-------------|
| A.01 | Scroll listener | `window.addEventListener('scroll')` | `§4.3 HARD BAN` |
| A.02 | RAF state loop | `requestAnimationFrame` + React state | `§4.3 Forbidden patterns` |
| A.03 | GSAP + Motion mix | Both in same component tree | `§4.3 GSAP + Motion fight` |
| A.04 | Non-GPU animate | `top`, `left`, `width`, `height` | `§5.A Hardware Acceleration` |
| A.05 | Reduced motion | `MOTION > 3` without reduced motion | `§5.B Reduced Motion non-negotiable` |
| A.06 | Marquee overflow | >1 marquee on page | `§4.5 Marquee Rule` |
| A.07 | Motion mismatch | `MOTION > 4` but page is static | `§6.F Motion claimed ≠ shown` |
| A.08 | GSAP non-canonical | GSAP without `start: "top top"` | `§4.2 GSAP Canonical Patterns` |
| A.09 | Infinite loops | Pulsing glow everywhere | `§4.4 Motion Motivation Rule` |
| A.10 | Reveal gating | Content invisible without animation | `§9.K Reveal-Safety` |

#### Slop Test Execution

Before emitting any frontend code, run the relevant gates:

```
SLOP TEST EXECUTION
    │
    ├── Color Gates (C.01-C.12)
    │   └── If any fail: reject palette, restart from §9.A
    │
    ├── Typography Gates (T.01-T.10)
    │   └── If any fail: correct type selection
    │
    ├── Layout Gates (L.01-L.15)
    │   └── If any fail: restructure layout
    │
    ├── Component Gates (P.01-P.10)
    │   └── If any fail: replace with approved pattern
    │
    └── Animation Gates (A.01-A.10)
        └── If any fail: fix or remove animation
```

**Pass threshold:** 57/57 gates must pass. Any failure = reject and rebuild.

---

## 10. ANIMATION DECISION FRAMEWORK (Emil Kowalski Polish Layer)

> Synthesized from `emilkowalski/emil-design-eng` (⭐6). Augments §4 with the *decision rules* the polish layer requires.
> See also: https://animations.dev/

### 10.A Decision Order (always ask these in order before writing any animation code)

1. **Should this animate at all?** How often will the user see this animation?
   - 100+/day (keyboard shortcuts, command palette) → **No animation. Ever.**
   - Tens/day (hover effects, list navigation) → Remove or drastically reduce
   - Occasional (modals, drawers, toasts) → Standard animation
   - Rare (onboarding, celebrations) → Can add delight

2. **What is the purpose?** Valid answers: spatial consistency, state indication, explanation, feedback, preventing jarring change. Invalid: "it looked cool".

3. **What easing?**
   - Entering the screen → `ease-out` (starts fast, feels responsive)
   - Moving on screen → `ease-in-out`
   - Hover / color change → `ease`
   - Constant motion (marquee, progress) → `linear`
   - **Default → `ease-out`. Never `ease-in` for UI — it makes the interface feel sluggish at the exact moment the user is watching.**

4. **How fast?**
   - Button press feedback: 100-160ms
   - Tooltips, small popovers: 125-200ms
   - Dropdowns, selects: 150-250ms
   - Modals, drawers: 200-500ms
   - Marketing/explanatory: can be longer
   - **Rule: UI animations stay under 300ms.** A 180ms dropdown feels more responsive than a 400ms one.

### 10.B Custom Easing Curves (mandatory for craft feel)

```css
:root {
  --ease-out: cubic-bezier(0.23, 1, 0.32, 1);     /* strong UI interactions */
  --ease-in-out: cubic-bezier(0.77, 0, 0.175, 1); /* on-screen movement */
  --ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);  /* iOS-like drawer (Ionic) */
}
```

Do not create curves from scratch. Use https://easing.dev/ or https://easings.co/.

### 10.C Spring Animations (when to reach for them)

Springs feel natural because they simulate physics. Reach for them for:
- Drag interactions with momentum
- Elements that should feel "alive" (Apple's Dynamic Island, magnetic hovers)
- Gestures that can be interrupted mid-animation
- Decorative mouse-tracking interactions

```js
// Apple-style — easier to reason about
{ type: "spring", duration: 0.5, bounce: 0.2 }

// Traditional physics — more control
{ type: "spring", mass: 1, stiffness: 100, damping: 10 }
```

**Keep bounce subtle (0.1-0.3).** Bounce is for drag-to-dismiss and playful interactions, not for primary UI feedback.

**Interruptibility advantage:** springs maintain velocity when interrupted. CSS animations restart from zero. For any interaction that can be retriggered rapidly (toggling states, queueing toasts), springs produce smoother results.

### 10.D Component Polish Rules

| Element | Rule | Why |
|---|---|---|
| Buttons | `transform: scale(0.97)` on `:active` | Buttons must feel responsive to press |
| Entry animations | Never from `scale(0)` — start at `scale(0.9)` + opacity | Nothing in real world appears from nothing |
| Popovers | `transform-origin: var(--radix-popover-content-transform-origin)` | Popovers scale from trigger; modals stay centered (exception) |
| Tooltips | Skip animation on subsequent hovers (data-instant) | Feels faster without defeating initial delay purpose |
| Crossfades that feel off | Add `filter: blur(2px)` during transition | Blur bridges the visual gap between old and new state |
| Entry | Prefer CSS `@starting-style` over `useEffect`-mounted pattern | Modern, no JS mount race |
| Interruptible UI | Prefer CSS transitions over `@keyframes` | Transitions can be interrupted and retargeted mid-flight |
| Hardware-accel | Animate ONLY `transform` and `opacity` | Never `width`/`height`/`top`/`left` |

### 10.E Imperceptible Details That Compound

- **Spring mouse tracking:** Tying visual change directly to mouse position feels artificial. Use `useSpring` to interpolate value changes with momentum.
- **Translate by percentage:** `translateY(100%)` moves an element by its own height regardless of actual size. Use for drawer/toast positioning.
- **`scale()` scales children too:** unlike `width`/`height`, `scale()` scales font, icons, content proportionally — a feature, not a bug.
- **`transform-origin` matters:** default `center` is wrong for almost every popover. Set to where the trigger lives.
- **Blur mask for imperfect transitions:** when crossfade feels off despite trying different easings, add `filter: blur(2px)` during the transition. Keep blur under 20px (Safari cost).
- **`clip-path: inset()`** for reveals, hold-to-delete patterns, comparison sliders, perfect color transitions on tabs. Hardware-accelerated, no extra DOM.

### 10.F Gesture and Drag (when needed)

- **Momentum-based dismissal:** don't require dragging past a threshold. If velocity > ~0.11 (`Math.abs(dragDistance) / elapsedTime`), dismiss regardless of distance.
- **Boundary damping** instead of hard stops — feels physical.
- **Interruptibility:** any drag/swipe/pinch animation must be retargetable mid-flight.

### 10.G Review Format (mandatory for any animation review)

When reviewing motion code, output a single markdown table — never a "Before:/After:" list:

```
| Before | After | Why |
| --- | --- | --- |
| `transition: all 300ms` | `transition: transform 200ms ease-out` | Specify exact properties; never `all` |
| `ease-in` on dropdown | `ease-out` with custom curve | `ease-in` feels sluggish; `ease-out` gives instant feedback |
```

---

## 11. STYLE & PALETTE REFERENCE (Database Pointer)

> Synthesized from `nextlevelbuilder/ui-ux-pro-max` (⭐5). This section is a **pointer**, not an embedded database. The skill file stays lean; the data lives in the source repo and can be queried at design time.

### 11.A Why a pointer and not the database

`ui-ux-pro-max` ships with ~30MB of CSV data: 50+ styles, 161 palettes, 57 font pairings, 161 product types, 99 UX guidelines, 25 chart types across 10 stacks. Embedding that into `SKILL.md` would:
- Blow past Cursor's skill-loading budget per request
- Go stale instantly when the source repo updates
- Duplicate data that already lives in `.cursor/rules/ui-visual-design.mdc`

### 11.B Reference resolution order

When you need a style, palette, font pairing, or UX rule:

1. **§2.A Design System Map** — if the brief matches an official system (Fluent, Carbon, Material, Polaris, Primer, GOV.UK, USWDS, Radix, shadcn/ui), use that. Stop here.
2. **§0.E Existing project tokens** — check `package.json`, `tailwind.config.*`, `:root` CSS vars. If a committed palette exists, identity-preservation wins.
3. **`.cursor/rules/ui-visual-design.mdc`** — for general visual design principles in this workspace.
4. **`ui-ux-pro-max` CLI (optional, install on demand):**
   ```bash
   # One-time install for the project
   npm install -g ui-ux-pro-max-cli
   uipro init --ai cursor
   ```
   Then query:
   ```bash
   # Style + palette + font pairing for a brief
   uipro search "<keywords>" --design-system

   # Stack-specific guidance
   uipro search "<topic>" --stack react
   ```
   Use `--domain` to scope: `style`, `color`, `typography`, `ux`, `chart`, `product`, `stack`.
5. **Vercel Web Interface Guidelines** (see §11.C) — for a11y/perf/UX compliance rules.

### 11.C Vercel Web Interface Guidelines (⭐4)

The `vercel-labs/web-design-guidelines` skill is **a runtime-fetched audit tool**, not a static rule file. SKILL.md only contains a pointer to `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`. To run an audit:

```
# From any Cursor chat
@web-design-guidelines <file-or-pattern>
```

Or inline-fetch when needed:

```
WebFetch https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
```

**100+ rules covering:** Accessibility (aria, semantic, keyboard), Focus States, Forms (autocomplete, validation), Animation (prefers-reduced-motion, compositor transforms), Typography (curly quotes, tabular-nums), Images (dimensions, lazy, alt), Performance (virtualization, layout thrashing, preconnect), Navigation & State (URL reflects state, deep-linking), Dark Mode & Theming (color-scheme, theme-color), Touch & Interaction (touch-action, tap-highlight), Locale & i18n (Intl.DateTimeFormat, Intl.NumberFormat).

**When to run the audit:** after §6 post-review passes, before declaring done. Output format is terse `file:line` — wire into PR checks via `npx skills add vercel-labs/agent-skills --skill web-design-guidelines` if you want CI enforcement.

### 11.D Rule priority table (from ui-ux-pro-max — reference, not rules)

| Priority | Category | Impact |
|---|---|---|
| 1 | Accessibility | CRITICAL — contrast 4.5:1, alt text, keyboard nav, aria |
| 2 | Touch & Interaction | CRITICAL — 44×44px targets, 8px+ spacing, loading feedback |
| 3 | Performance | HIGH — WebP/AVIF, lazy load, reserve space (CLS < 0.1) |
| 4 | Style Selection | HIGH — match product type, consistency, no emoji-as-icons |
| 5 | Layout & Responsive | HIGH — mobile-first, viewport meta, no horizontal scroll |
| 6 | Typography & Color | MEDIUM — 16px base, 1.5 line-height, semantic tokens |
| 7 | Animation | MEDIUM — 150-300ms, motion conveys meaning |
| 8 | Forms & Feedback | MEDIUM — visible labels, error near field, helper text |
| 9 | Navigation Patterns | HIGH — predictable back, deep linking, max 5 bottom-nav |
| 10 | Charts & Data | LOW — legends, tooltips, accessible colors |

Note: this priority order is **embedded as reference only**. The active rules live in §0-§9 of this skill and in `.cursor/rules/ui-visual-design.mdc`. The database is the *why*, this file is the *what to do*.

---

## 12. SOURCES, ATTRIBUTION & CONFLICT RESOLUTION

### 12.A Source skills (merged into this file)

| # | Skill | Source | Stars | Merged into |
|---|-------|--------|-------|-------------|
| ⭐1 | impeccable | github.com/pbakaus/impeccable | 39k | §9 (philosophy + anti-slop catalog) + §2 (anti-cream) |
| ⭐2 | taste-skill | github.com/Leonxlnx/taste-skill | — | §0-§4 (original source of dials, GSAP skeletons, em-dash ban) |
| ⭐3 | frontend-design | github.com/anthropics/skills | 147k | §9 (two-pass build, signature element, critique) |
| ⭐4 | web-design-guidelines | github.com/vercel-labs/agent-skills | 25k | §11.C (runtime audit pointer; not embedded — stays fresh) |
| ⭐5 | ui-ux-pro-max | github.com/nextlevelbuilder/ui-ux-pro-max-skill | 95k | §11 (database pointer, priority table) |
| ⭐6 | emil-design-eng | github.com/emilkowalski/skill | 2k | §10 (animation decision framework + polish layer) |
| ⭐7 | hallmark | github.com/Nutlope/hallmark | 9.3k | §9.A (4 verbs, 20 themes, 57 slop-test gates) |

### 12.B Merge order

The ⭐ priority (1=highest) defines **conflict resolution** when sources disagree:

- ⭐1 wins on **anti-slop catalog and color strategy** (cream ban, ghost-card ban, signature element framing)
- ⭐2 wins on **structural defaults** (the three dials, GSAP canonical skeletons, em-dash ban — *this is the spine of the skill*)
- ⭐3 wins on **philosophy and intent framing** (two-pass build, design-lead voice)
- ⭐4 wins on **a11y/perf/UX compliance rules** (any conflict with ⭐1-3 on accessibility → ⭐4 wins, no exceptions)
- ⭐5 wins on **style/palette/font pairing lookup** (when the brief needs a database-driven recommendation, not a taste-driven one)
- ⭐6 wins on **micro-interaction polish** (motion decisions, easing curves, button-press feedback)
- ⭐7 wins on **slop-test gates and theme selection** (57 gates, 20 catalog themes, custom theme protocol)

In practice the sources agree on most things. When they disagree, the resolution above is the rule.

### 12.C Active skills in this workspace

| Skill | File | Role | Pre-gate | Post-gate |
|---|---|---|---|---|
| `frontend-taste` (this file) | `.cursor/skills/frontend-taste/SKILL.md` | Build landing pages, portfolios, redesigns | §0 pre-flight | §6 audit + §10 polish review |
| `frontend-review` | `.cursor/skills/frontend-review/SKILL.md` | Quality gate for any frontend task | Part A scope | Part B 7-axis review |
| `frontend-redesign` | `.cursor/skills/frontend-redesign/SKILL.md` | Upgrade existing sites without breaking functionality | §0 pre-audit | §4 post-redesign audit |
| `karpathy-coding` | `.cursor/skills/karpathy-coding/SKILL.md` | Overlay: pre/post reasoning gate for any code task | karpathy-pre | karpathy-post |
| `full-output` | `.cursor/skills/full-output/SKILL.md` | Multi-file implementations | fulloutput-pre | fulloutput-post |
| `ponytail` | `.cursor/skills/ponytail/SKILL.md` | Lazy Senior Dev — minimum viable code | ponytail-pre | ponytail-post |
| `Hallmark` | `.cursor/skills/frontend-taste/SKILL.md §9.A` | Anti-slop themes + 57 gates | theme selection | slop-test gates |

### 12.D Why no new skill files were created

The six source skills overlap heavily with each other and with the three pre-existing skills in this workspace. Creating six parallel skills would:

- Cause direct conflicts on every rule (each skill ships its own opinion on motion duration, color, typography)
- Multiply the per-request context load (Cursor loads each skill's body into context on relevant requests)
- Force the agent to pick between conflicting rules at runtime
- Stale instantly (⭐4 fetches rules dynamically for a reason)

The single-source-of-truth pattern — this file — means one rule per concern, one place to update, zero conflict. The ⭐1→⭐6 merge order encodes the priority without creating files.

### 12.E External pointers (install only when needed)

These are **not installed** by default. Install via `npx skills add` only when the use case demands live data:

- `npx skills add https://github.com/pbakaus/impeccable --skill impeccable` — only if you want the full commands menu (`craft`, `shape`, `audit`, `polish`, ...) and the bundled detector hooks
- `npx skills add https://github.com/Leonxlnx/taste-skill --skill design-taste-frontend-v1` — only if you want the v1 baseline for diff comparison
- `npx skills add vercel-labs/agent-skills --skill web-design-guidelines` — only if you want CI/PR-check integration for the Vercel rules
- `uipro init --ai cursor` (from `ui-ux-pro-max-cli`) — only if you need on-demand palette/style/font queries during a build

In all four cases, the merge into this file is **complete enough that you do not need them for normal use**. Install only when you specifically want live-data access.

---

## Liens

- [[../rules/skill-integration]] - Skill Integration Rules
- [[../rules/frontend-architecture]] - Frontend Architecture
- [[../skills/frontend-review]] - Frontend Review Skill
- [[../skills/frontend-redesign]] - Frontend Redesign Skill
- [[../skills/full-output]] - Full Output Skill
- [[../rules/ui-visual-design]] - Workspace Visual Design Principles

**Synthesized from:** [pbakaus/impeccable](https://github.com/pbakaus/impeccable) ⭐1 · [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) ⭐2 · [anthropics/frontend-design](https://github.com/anthropics/skills) ⭐3 · [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) ⭐4 · [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) ⭐5 · [emilkowalski/skill](https://github.com/emilkowalski/skill) ⭐6 · [Nutlope/hallmark](https://github.com/Nutlope/hallmark) ⭐9.3k. See §12 for merge order and conflict resolution.
