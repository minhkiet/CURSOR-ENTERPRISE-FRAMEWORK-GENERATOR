---
name: frontend-review
description: Comprehensive frontend code review skill with mandatory pre-review scope analysis and post-review quality gates. Reviews for correctness, design quality, accessibility, performance, and taste. Use before and after every frontend implementation task.
---

# Frontend Code Review Skill

> A mandatory dual-gate review system: pre-review before writing code, post-review before delivering.
> This skill applies to all frontend tasks (landing pages, redesigns, components, full-stack UI).
> It integrates taste-skill anti-slop rules and full-output enforcement.

---

## PART A: PRE-REVIEW — BEFORE WRITING CODE (Scope & Plan Gate)

**Run this before any code is written. Results feed into the implementation.**

### A.1 Scope Analysis
1. **Read the full request** — understand every requirement, constraint, and deliverable
2. **List all files to touch** — component files, style files, config files, test files
3. **Identify dependencies** — packages to install, environment setup, API contracts
4. **Check existing codebase** — existing components, design tokens, patterns to follow

### A.2 Quality Plan
Based on scope, plan the quality approach:

| If the task involves... | Apply these checks |
|---|---|
| Landing page / marketing site | taste-skill pre-flight + post-flight (Sections 0, 6) |
| Redesign of existing site | frontend-redesign pre-audit + post-audit |
| Full implementation (multiple files) | full-output pre-generation + post-generation |
| API + UI | correctness, error handling, loading states |
| Animation / motion | reduced motion, GSAP canonical patterns, no jank |
| Forms | validation, WCAG AA contrast, accessibility |
| Dark mode | both modes, prefers-color-scheme, token strategy |

### A.3 Pre-Review Checklist (PASS GATE)
Before writing code:

**Scope**
- [ ] All deliverables listed and counted
- [ ] All file paths confirmed
- [ ] All dependencies identified (packages, env vars, API contracts)
- [ ] Framework/stack confirmed

**Design (if UI task)**
- [ ] Design read declared (brief → language → aesthetic direction)
- [ ] Dial values set: VARIANCE / MOTION / DENSITY
- [ ] Design system selected if applicable
- [ ] Anti-default discipline applied (no AI-purple, no Inter default, no centered hero)

**Architecture**
- [ ] State management strategy defined (local vs global)
- [ ] Component hierarchy planned (atomic design or feature-based)
- [ ] API integration strategy (REST, GraphQL, or local state)
- [ ] Error handling strategy defined
- [ ] Loading/empty/error states planned

**Quality**
- [ ] Testing strategy defined (unit tests, component tests, E2E)
- [ ] Accessibility requirements identified (WCAG level, keyboard nav, screen reader)
- [ ] Performance budget identified (bundle size, LCP target)

---

## PART B: POST-REVIEW — AFTER WRITING CODE (Quality Gate)

**Run this after all code is written, before delivering. Every box must be ticked.**

### B.1 Correctness Review
- [ ] Code compiles / builds without errors
- [ ] No TypeScript errors (or all non-null assertions are justified)
- [ ] All imports resolve (packages exist in package.json)
- [ ] No hardcoded values that should be environment variables
- [ ] No console.log, debugger, or console.warn left in production code
- [ ] Error boundaries / try-catch for all async operations
- [ ] API calls have proper error handling and retry logic
- [ ] No race conditions in async code
- [ ] No security vulnerabilities (XSS, injection, exposed secrets)

### B.2 Design & Taste Review
- [ ] Design read declared at the start of the response?
- [ ] Dial values (VARIANCE/MOTION/DENSITY) declared?
- [ ] ZERO em-dashes (`—`) anywhere in the code or visible text
- [ ] Page theme lock: ONE theme for whole page, no mid-page inversion
- [ ] Color consistency: one accent color used identically across all sections
- [ ] Shape consistency: one corner-radius system applied consistently
- [ ] No Inter as default (unless explicitly asked or Linear-style brief)
- [ ] No Fraunces/Instrument_Serif as default serif
- [ ] Premium-consumer brief: NOT using beige+brass+oxblood+espresso palette family
- [ ] No AI Tells (three-equal cards, Jane Doe, Acme Corp, AI-purple, "Quietly in use at")
- [ ] Hero fits viewport (headline max 2 lines, subtext max 20 words)
- [ ] Navigation on ONE line at desktop, height 64-80px
- [ ] Eyebrow count ≤ ceil(sectionCount / 3)
- [ ] No split-header pattern (left big headline + right small explainer)
- [ ] No 3+ consecutive same-layout sections
- [ ] Bento grid: N items → N cells, no empty cells
- [ ] Copy self-audit: no grammatically broken or AI-hallucinated strings shipped
- [ ] No fake-precise numbers without justification
- [ ] No generic names (John Doe, Lorem Ipsum, Acme Corp)
- [ ] No filler verbs (Elevate, Seamless, Unleash, Next-Gen, Game-changer)
- [ ] No section-numbering eyebrows ("00 / INDEX", "001 · Capabilities")
- [ ] No scroll cues ("Scroll", "↓ scroll")
- [ ] No locale/city/weather strips
- [ ] No version footers on marketing pages
- [ ] Logo wall = logos only (no industry labels below logos)
- [ ] "Trusted by" lives UNDER hero, not inside hero
- [ ] Bento background diversity: real visual variation in cells (not all white-on-white)

### B.3 Accessibility Review
- [ ] All images have meaningful alt text (no `alt=""` on meaningful images, no `alt="image"`)
- [ ] Color contrast passes WCAG AA: 4.5:1 for body text, 3:1 for large text
- [ ] Form labels associated with inputs (htmlFor/id or aria-label)
- [ ] Focus indicators visible for keyboard navigation
- [ ] Skip-to-content link present for keyboard users
- [ ] No positive `tabindex` values (natural DOM order preserved)
- [ ] ARIA attributes used correctly (no `role` conflicts, proper `aria-expanded`, etc.)
- [ ] Button contrast: every CTA text readable against background (WCAG AA)
- [ ] Form contrast: inputs, placeholders, focus rings pass WCAG AA
- [ ] Motion respects `prefers-reduced-motion` (wrap animations for MOTION > 3)
- [ ] Semantic HTML used (`<button>` for buttons, `<a>` for links, `<nav>` for nav, etc.)

### B.4 Performance Review
- [ ] LCP < 2.5s (hero image priority / preloaded)
- [ ] Images have width/height to prevent CLS
- [ ] No layout-triggering animations (transform/opacity only, not top/left/width/height)
- [ ] No `window.addEventListener('scroll')` — using Motion/ScrollTrigger/IntersectionObserver
- [ ] Bundle size reasonable (no unnecessary large dependencies imported)
- [ ] Lazy loading for below-the-fold content (dynamic imports, loading="lazy")
- [ ] No grain/noise on scrolling containers (only on fixed pointer-events-none layers)
- [ ] Google Fonts loaded via `next/font` or `@font-face` with `font-display: swap` (not `<link>` tag)
- [ ] Icons from allowed library only (not hand-rolled SVG paths)
- [ ] Motion isolated in client-leaf components with `'use client'` at top

### B.5 State & Interaction Review
- [ ] Loading state: skeletal loaders matching final layout shape (no generic spinners)
- [ ] Empty state: composed view with clear "how to populate" guidance
- [ ] Error state: clear inline messages (no `window.alert()`)
- [ ] Button hover states: background shift, scale, or translate
- [ ] Button active/pressed feedback: `scale(0.98)` or `-translate-y-[1px]`
- [ ] Smooth transitions on all interactive elements (200-300ms, not instant)
- [ ] Active nav link styled differently (current page indication)
- [ ] CTA wrap: no label wraps to 2+ lines at desktop
- [ ] No duplicate CTA intent on the page ("Get in touch" + "Contact us" = same intent)
- [ ] Form: label above input, error below input, no placeholder-as-label
- [ ] Dark mode: tokens defined, both modes designed, `prefers-color-scheme` respected

### B.6 Testing Review
- [ ] Unit tests for utility functions and hooks
- [ ] Component tests for complex UI components
- [ ] Test coverage for error paths (not just happy path)
- [ ] No commented-out tests left behind
- [ ] Mock setup for external dependencies (API, auth, etc.)

### B.7 Full-Output Verification (if multi-file task)
- [ ] All planned files delivered
- [ ] All planned functions fully implemented
- [ ] No `// ...`, `// TODO`, `/* ... */`, `// implement here` patterns
- [ ] No skeleton when full implementation was requested
- [ ] No "continue later", "you can extend this", or "for brevity" patterns

---

## PART C: REVIEW OUTPUT FORMAT

### C.1 Pre-Review Output
When starting a task, output the pre-review summary:

```
[PRE-REVIEW] Scope: N deliverables
- file1.tsx
- file2.tsx
- ...

Design Direction: [design read declared]
Dial Values: VARIANCE / MOTION / DENSITY
Quality Gates: [list applicable review sections from B above]
```

### C.2 Post-Review Output
When delivering, output the review summary:

```
[POST-REVIEW] All gates passed:
- Correctness: PASS
- Design & Taste: PASS  
- Accessibility: PASS
- Performance: PASS
- State & Interaction: PASS
- Testing: PASS (N tests written)
- Full-Output: PASS (N/N files delivered)

Reviewer Notes:
[If any items failed and were fixed, note them here]
```

### C.3 Review Failures
If any post-review item fails:
1. **Do not deliver** until the item is fixed
2. Fix the item immediately
3. Re-run the review gate
4. Only deliver when ALL boxes pass

---

## PART D: REVIEW TRIGGERS

This skill activates in these scenarios:

| Trigger | Pre-review required | Post-review required |
|---|---|---|
| Landing page build | Yes (taste-skill Section 0) | Yes (taste-skill Section 6) |
| Redesign existing site | Yes (frontend-redesign Section 0) | Yes (frontend-redesign Section 4) |
| Multi-file implementation | Yes (full-output Section 0) | Yes (full-output Section 5) |
| Any frontend UI task | Yes (Part A) | Yes (Part B) |
| API + frontend task | Yes (Part A + API correctness) | Yes (Part B + correctness) |

When the user asks for a review, a code review, quality check, or "is this ready to ship", run the applicable post-review gates.
