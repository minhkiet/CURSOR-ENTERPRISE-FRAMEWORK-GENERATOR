# Conventions & Precision Rules

*The shared "house style" that makes site-clone prompts reproduce a target 1:1.*

---

## 1. The Opening Sentence

Open with **one imperative sentence that front-loads the global invariants**:

```
BUILD VERB → PAGE TYPE → PRODUCT NAME (quoted) → SECTION COUNT → TECH STACK → KEY LIBS → DOMINANT AESTHETIC → [precision oath]
```

**Examples:**
- `Create a React + Vite + TypeScript + Tailwind CSS landing page for a creative studio called "Prisma". The page has 3 sections: Hero, About, and Features. Use framer-motion for animations and lucide-react for icons. The design is dark, moody, and cinematic.`
- `Build a full-screen, dark-themed hero section for a geology brand called "Lithos" using React 18 + TypeScript + Vite + Tailwind CSS. The signature feature is a cursor-following spotlight that reveals a second image.`

---

## 2. Default Tech Stack

```
React 18 + TypeScript + Vite + Tailwind CSS + Framer Motion + lucide-react
```

**Variations:**
| Variation | When | Changes |
|-----------|------|---------|
| CDN/no-bundler | In-browser demos | React UMD + Tailwind CDN + SRI hashes |
| No framer-motion | Light SaaS | Hand-written CSS @keyframes |
| No icon lib | Byte-exact glyphs | Inline SVG path data |

---

## 3. Exact-Value Rules

### 3.1 Colors — always exact, always role-attached

- **Exact hex everywhere**: `#0C0C0C` (global bg), `#101010` (About card)
- **rgba for translucency**: `rgba(255,255,255,0.01)` (glass fill)
- **Tailwind opacity slashes**: `text-white/70`, `border-white/10`

### 3.2 Tailwind strings — verbatim with full responsive ladders

```tsx
// Good
className="text-[26vw] sm:text-[24vw] md:text-[22vw] lg:text-[20vw]"

// Bad
className="text-large heading"
```

### 3.3 framer-motion — every number specified

```tsx
// Good
initial={{ filter: 'blur(10px)', opacity: 0, y: 20 }}
transition={{ duration: 0.7, delay: 0.5, ease: [0.16, 1, 0.3, 1] }}

// Bad
transition="smooth fade-in"
```

---

## 4. Asset Rules

**Never leave an asset vague.** In screenshot mode, write generation briefs. In URL mode, pin stable original URLs.

### Generation Brief Template
```
Medium: [photoreal photo / cinematic still / 3D render]
Camera: [viewpoint]
Composition: [subject placement, focal area]
Palette lock: match page tokens #HEX / #HEX / #HEX
Lighting: [description]
Negative: no visible text, no watermark, no logo.
Delivery: object-cover, object-position X% Y%
```

### Stock Fallback Sources
| Source | URL Pattern |
|--------|-------------|
| Unsplash | `https://images.unsplash.com/photo-ID?w=1600&q=80` |
| Pexels | `https://videos.pexels.com/video-files/ID/...mp4` |
| DiceBear | `https://api.dicebear.com/10.x/persona/svg?seed=NAME` |

---

## 5. Document Structure

```
1. Opening lock sentence
2. GLOBAL TOKENS — Fonts → Colors → Custom CSS
3. ASSET MANIFEST
4. SHARED COMPONENTS
5. SECTIONS (in render order)
6. RESPONSIVE BREAKPOINTS
7. KEY DESIGN PRINCIPLES (guardrail)
```

---

## 6. Negative Constraints

Suppress plausible-but-wrong defaults:
- `No overlay. The video plays raw.`
- `No purple, no indigo.`
- `No other UI libraries.`
- `loop attribute is OFF.`
- `All text white.`

---

## 7. Do's and Don'ts

**DO:**
- Front-load stack + product + section map in sentence one
- Give exact hex with the surface it paints
- Paste complete Tailwind className strings
- Specify motion numerically
- Quote all copy verbatim
- State z-index numerically
- Add negative constraints

**DON'T:**
- Use named colors ("orange", "dark gray")
- Describe layout in prose ("large rounded corners")
- Say "a nice fade-in" — give y/delay/ease/duration
- Say "a background video" — give generation brief or URL
- Paraphrase or invent copy
- Let the implementer pick the framework
