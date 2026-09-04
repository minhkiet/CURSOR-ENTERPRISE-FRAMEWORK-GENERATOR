# External Benchmarks · Lessons from Adjacent Tools

**Purpose:** Keep lessons from mature tools without becoming them.

---

## Verdict Matrix

| Reference | Useful for this skill | Do not copy |
|-----------|----------------------|-------------|
| `abi/screenshot-to-code` | Prompt routing, design-system injection, asset extraction | Placeholder policy |
| `alyssaxuu/motionity` | Timeline vocabulary: keyframes, easing, duration | Editor embedding |
| `CopyWeb` | Confirms target user flow | Closed internals |

---

## Adopted Patterns

### 1. Prompt Construction Plan

Before writing the clone prompt, route the task:

```text
input_mode: screenshot | multi-screenshot | url | screenshot+url
target_stage: prompt-only | implementation-confirmed
asset_mode: image-gen-capable | fetch-only | original-src-required
scope: visible-only | full-landing-page
```

**Rules:**
- `prompt-only` is default
- `implementation-confirmed` only after user confirms

### 2. Design System Injection

If the user provides design system, prior prompt, or brand guide:

```
DESIGN SYSTEM CONTEXT
If this conflicts with generic defaults, prioritize this block.
```

**Priority order:**
1. Current URL measured values
2. Current screenshot visible facts
3. User-provided design system
4. Inference from industry

### 3. Asset Strategy: Extract, Generate, Verify

```text
1. URL + stable public asset → pin exact src
2. Screenshot + distinct element → generation brief
3. Missing/low-res → generate with brief
4. Implementation confirmed → copy to public/assets/
```

**Never use:** `placehold.co`, `REPLACE-ME`, vague "hero image"

### 4. Preview Regression Loop

```text
build → run dev server → screenshot desktop → screenshot mobile
→ inspect layout/motion → patch → rebuild
```

**Checks:**
- Screenshot mode: compare every uploaded screenshot
- URL mode: capture original opening, rest, mouse states, scroll
- No horizontal overflow
- Generated images from project-local paths
- Hero background has perceptible motion

---

## Motionity-Inspired Motion Vocabulary

For static screenshots, infer motion:

```text
layer: background media, veil, nav, title, CTA, cards
keyframes: exact from/to transform, opacity, filter
easing: named or cubic-bezier array
order: forward/backward/letters/words
mask: spotlight, crop reveal, liquid-glass borders
```

**Example:**
```
Hero background pseudo-video:
Layer HERO_BG_STILL keyframes:
  0%   transform scale(1.04) rotate(-1.8deg) translate3d(-3%, -1.6%, 0)
  100% transform scale(1.18) rotate(1.8deg) translate3d(3%, 1.6%, 0)
duration 18-24s, easing ease-in-out, direction alternate, repeat infinite
```

---

## Rejection Rules

- Do not switch from prompt-first to code-first
- Do not start implementation without user confirmation
- Do not copy screenshot-to-code's placeholder policy
- Do not make Motionity-style complexity mandatory for simple interactions
