# MASTER PROMPT TEMPLATE — "1:1 Website Clone Prompt"

> **What this is.** A fill-in skeleton for writing a *website clone prompt* — the kind an AI coding agent reads to reproduce a landing page pixel-for-pixel.
>
> **How to use.** Walk the blocks top-to-bottom. Fill every slot with **literal values, not vague descriptions**.
>
> **Authorization boundary.** Exact clone prompts are for user-owned pages, authorized work, internal research, or local visual regression.

---

## BLOCK 0 — OPENING BRIEF (the one-sentence lock)

**Format:**
```
Create a React + Vite + TypeScript + Tailwind CSS landing page for "PRODUCT_NAME".
The page has N sections: Section1, Section2, Section3.
Use Framer Motion for animations and lucide-react for icons.
The design is [aesthetic description with concrete invariants].
Match every detail below exactly.
```

---

## BLOCK 1 — TECH STACK

```
- React 18 (react, react-dom ^18.3.1)
- TypeScript
- Vite
- Tailwind CSS ^3.4.1
- Framer Motion ^12.40.0
- lucide-react ^0.344.0
- No other UI libraries.
```

---

## BLOCK 2 — FONTS

```
Load in index.html:
<link href="https://fonts.googleapis.com/css2?family=FONT_NAME:wght@WEIGHTS&display=swap" rel="stylesheet">

- Heading/Display: "FONT_NAME" (weights) — role.
- Body/UI: "FONT_NAME" (weights) — role.

tailwind.config → fontFamily: { serif:['"FONT_NAME"', 'serif'], sans:['FONT_NAME','system-ui',sans-serif] }
```

---

## BLOCK 3 — COLOR SYSTEM

```
- Background: #HEX — globally / for [element]
- Primary text: #HEX
- Secondary text: #HEX
- Accent/CTA: #HEX
- Border: #HEX or white/OPACITY
- No purple, no indigo.
```

---

## BLOCK 4 — ASSET MANIFEST

```
target_asset_mode: image-gen-capable

ASSET_ALIAS [TYPE, aspect ratio]:
  Medium: [description]
  Camera: [angle/viewpoint]
  Composition: [subject placement, focal area]
  Palette lock: match page tokens #HEX / #HEX / #HEX
  Lighting: [description]
  Negative constraints: no visible text, no watermark, no logo.
  Delivery: object-cover, object-position X% Y%
```

---

## BLOCK 4B — REFERENCE FRAMES

```
REFERENCE_FRAMES / VISUAL REGRESSION TARGETS
- REFERENCE_FRAME_01: [screenshot file], viewport [WxH], visible section [name], pass criteria: [exact match requirements]
```

---

## BLOCK 5 — CUSTOM CSS UTILITIES

### Liquid Glass
```css
.liquid-glass {
  background: rgba(255,255,255,0.01);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  box-shadow: inset 0 1px 1px rgba(255,255,255,0.1);
}
.liquid-glass::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  padding: 1.4px;
  background: linear-gradient(180deg, rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.15) 20%, rgba(255,255,255,0) 40%, rgba(255,255,255,0) 60%, rgba(255,255,255,0.15) 80%, rgba(255,255,255,0.45) 100%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0));
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}
.liquid-glass:hover { background: rgba(255,255,255,0.04); }
```

### Gradient Text
```css
.gradient-text {
  background: linear-gradient(180deg, #HEX 0%, #HEX 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
```

### Noise Overlay
```css
.noise-overlay {
  position: absolute;
  inset: 0;
  opacity: 0.15;
  pointer-events: none;
  background-image: url("data:image/svg+xml,...");
  mix-blend-overlay: overlay;
}
```

---

## BLOCK 6 — CUSTOM COMPONENTS

### BlurText Component
```tsx
function BlurText({ text, className }) {
  const words = text.split(' ');
  return (
    <div className="flex flex-wrap justify-center gap-x-3">
      {words.map((word, i) => (
        <motion.span
          key={i}
          initial={{ filter: 'blur(10px)', opacity: 0, y: 20 }}
          whileInView={{ filter: 'blur(0px)', opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: i * 0.1, ease: 'easeOut' }}
          className="inline-block mr-2"
        >
          {word}
        </motion.span>
      ))}
    </div>
  );
}
```

### FadeIn Component
```tsx
function FadeIn({ children, delay = 0, className }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.7, delay, ease: [0.25, 0.1, 0.25, 1] }}
      viewport={{ once: true, margin: '50px' }}
      className={className}
    >
      {children}
    </motion.div>
  );
}
```

---

## BLOCK 7 — SECTION TEMPLATE

```
#### SECTION N: [Name]
- Container: [flex/grid spec + overflow + padding]
- Background: [asset constant + playback mode] OR [exact bg color]
- Z-order: [layer order]

[Sub-element]:
  - Classes: [exact Tailwind class string with responsive ladder]
  - Copy: "[verbatim text]"
  - Typography: text-[SIZE] [weight] leading-[LINEHEIGHT] tracking-[TRACKING] [color]
  - Animation: [from] → [to], duration [X]s, delay [X]s, ease [EASING], stagger [X]s

Responsive: [hide/show rules for mobile/tablet]
```

---

## BLOCK 8 — SHARED ANIMATION COMPONENTS

```
BlurText: split on spaces, each word a motion.span,
  initial {filter:'blur(10px)', opacity:0, y:20} → {filter:'blur(0px)', opacity:1, y:0},
  duration 0.7s, stagger i*100ms, IntersectionObserver threshold 0.1.

FadeIn: whileInView + viewport={{ once:true, margin:'50px' }},
  delay/duration props, ease [0.25,0.1,0.25,1].

CSS variant:
  @keyframes fade-up { from{opacity:0;transform:translateY(24px)} to{opacity:1;transform:translateY(0)} }
  .animate-fade-up { animation: fade-up 0.9s cubic-bezier(0.22,1,0.36,1) both; }
  @media (prefers-reduced-motion: reduce){ .animate-fade-up { animation:none; opacity:1; } }
```

---

## BLOCK 9 — RESPONSIVE

```
Mobile-first; breakpoints sm/md/lg/xl.
- Headline: text-5xl → sm:text-7xl → md:text-8xl
- Features grid: 1-col → md:2-col → lg:4-col
- Center nav: hidden below md; hamburger: md:hidden
- All h-screen elements also carry h-[100dvh].
```

---

## BLOCK 10 — KEY DESIGN PRINCIPLES

```
- App wrapper: fontFamily matching the specified font stack
- Liquid glass recipe: backdrop-blur + gradient-stroke border
- Heading font: always italic with tight tracking
- Body font: light weight
- No dark overlay on video unless source has it
- rounded-full for buttons, rounded-2xl for containers
- prefers-reduced-motion support required
```

---

## BLOCK 11 — TECH STACK RECAP

```
TECH STACK
Vite + React 18 + TypeScript
Tailwind CSS 3
Framer Motion (all animations)
lucide-react (icons)

Dependencies: react, react-dom, framer-motion, tailwindcss, postcss, autoprefixer, vite, @vitejs/plugin-react, typescript

The detailed prompt above captures every element, style, animation, asset brief/URL, and font to recreate the page exactly.
```

---

## QUICK CHECKLIST BEFORE YOU SHIP THE PROMPT

- [ ] Opening sentence carries **stack + product + section map + aesthetic**
- [ ] Usage scope is explicit
- [ ] **Every** color is exact hex with a role
- [ ] Screenshot mode: every screenshot registered as REFERENCE_FRAME_N
- [ ] Screenshot mode: truncated pages completed with INFERRED PAGE COMPLETION
- [ ] URL mode: opening/loader frames captured if present
- [ ] **Every** asset has a generation brief with palette lock
- [ ] **Every** visible string is quoted VERBATIM
- [ ] **Every** element has VERBATIM Tailwind class string
- [ ] **Every** animation has exact from→to states, duration, delay, easing
- [ ] Signature CSS effects pasted as full CSS
- [ ] Negative constraints suppress wrong defaults
- [ ] After delivering the clone prompt, ask user whether to continue building locally
