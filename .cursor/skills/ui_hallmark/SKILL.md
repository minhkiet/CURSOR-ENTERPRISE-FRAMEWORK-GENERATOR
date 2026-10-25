---
name: hallmark
description: "Design taste skill for anti-slop UI. Based on Nutlope/hallmark (9.3k stars), detects AI slop aesthetics and builds distinctive, professional interfaces. Use when building landing pages, portfolios, marketing sites, or any design-intensive UI work. Identifies 57 slop-test gates to ensure work is original and tasteful."
---

# Hallmark: Anti-Slop Design Taste

Build distinctive, professional interfaces that pass the slop test.

## Philosophy

AI-generated UI all looks the same. Hallmark is a design skill that detects and avoids the 57 patterns that make AI slop recognizable, while teaching how to build interfaces with real taste.

**The slop test:** Would a designer recognize this as AI-generated? If yes, it's slop. Hallmark has 57 gates to catch it.

## Core Anti-Slop Principles

### 1. Typography Over Decoration
- Strong typographic hierarchy over illustration
- One powerful typeface over multiple fonts
- Editorial grid over scattered layout
- Text carries weight, images supplement

### 2. Structure Over Ornament
- Clean information architecture
- Breathing room between sections
- Purposeful white space
- Content-first hierarchy

### 3. Distinctive Over Safe
- Unique angle or perspective
- Specific, not generic
- Personal voice in copy
- Brand personality through details

### 4. Coherence Over Variety
- Consistent spacing rhythm
- Unified color language
- Typographic system
- Single visual language

### 5. Tactile Over Flat
- Subtle depth and shadows
- Layered elements
- Realistic interactions
- Physical feel

## The 57 Slop Gates

### Typography Gates (10)
- [ ] Headings use at most 2 weights
- [ ] No gradient text on large text
- [ ] Type scale follows 1.25+ ratio
- [ ] Line height 1.4-1.6 for body
- [ ] Measure 65-75 characters
- [ ] No mixed typefaces without purpose
- [ ] Text contrast 4.5:1 minimum
- [ ] No all-caps for body text
- [ ] Justified text avoided
- [ ] Kerning not increased globally

### Color Gates (10)
- [ ] Max 2 accent colors
- [ ] No pure black (#000) on white
- [ ] Saturation below 80% for accents
- [ ] Grays follow single hue
- [ ] No rainbow palette
- [ ] Shadows use neutral color
- [ ] Borders use gray, not color
- [ ] Hover states are subtle
- [ ] Focus states visible but not garish
- [ ] Dark mode is complete

### Layout Gates (10)
- [ ] 8px base grid
- [ ] Spacing in multiples of 4
- [ ] No perfectly symmetrical layouts
- [ ] Asymmetric balance
- [ ] No centered everything
- [ ] Content max-width 1200px
- [ ] Sidebar max 320px
- [ ] Mobile-first breakpoints
- [ ] No horizontal scroll
- [ ] Visible fold at 768px

### Component Gates (10)
- [ ] Buttons use consistent radius
- [ ] Cards have subtle shadow
- [ ] Inputs have clear states
- [ ] No gradient backgrounds
- [ ] Icons single color or stroke
- [ ] Tables are clean
- [ ] Modals centered with backdrop
- [ ] Tooltips positioned contextually
- [ ] Avatars use initials or real photos
- [ ] Badges are subtle

### Animation Gates (7)
- [ ] Duration 150-300ms
- [ ] Ease-out for entrances
- [ ] Ease-in for exits
- [ ] No bounce animations
- [ ] Stagger 50-100ms
- [ ] Hover transitions visible
- [ ] Loading states are subtle

### Copy Gates (10)
- [ ] No "Welcome to our platform"
- [ ] No "Get started today"
- [ ] No "Seamless experience"
- [ ] No "We make it easy"
- [ ] No "Join thousands of users"
- [ ] No exclamation marks
- [ ] No "Amazing" or "Incredible"
- [ ] Headline is specific, not generic
- [ ] CTA is action not "Submit"
- [ ] Error messages are helpful

## Design Themes

### Editorial
- Serif headlines
- Generous margins
- Pull quotes
- Column layouts
- Ink-on-paper feel

### Brutalist
- Raw typography
- Visible structure
- High contrast
- Bold blocks
- Anti-decoration

### Minimal
- Extreme white space
- Single accent color
- Mono typography
- Grid discipline
- Maximum restraint

### Atelier
- Elegant serifs
- Warm neutrals
- Artful spacing
- Craft feel
- Premium touches

### Neon
- Dark backgrounds
- Glowing accents
- Tech aesthetic
- Gradient trails
- Futuristic mood

### Brutal
- Harsh contrasts
- Industrial feel
- Bold type
- Raw edges
- Maximum impact

## Design Token System

### Spacing Scale
```
--space-1: 4px
--space-2: 8px
--space-3: 12px
--space-4: 16px
--space-6: 24px
--space-8: 32px
--space-12: 48px
--space-16: 64px
--space-24: 96px
```

### Typography Scale
```
--text-xs: 0.75rem    (12px)
--text-sm: 0.875rem   (14px)
--text-base: 1rem     (16px)
--text-lg: 1.125rem   (18px)
--text-xl: 1.25rem    (20px)
--text-2xl: 1.5rem    (24px)
--text-3xl: 1.875rem  (30px)
--text-4xl: 2.25rem   (36px)
--text-5xl: 3rem      (48px)
```

### Color System
```
--bg: #ffffff
--bg-subtle: #f7f7f8
--bg-muted: #e8e8e8
--text: #171717
--text-muted: #6b6b6b
--border: #e5e5e5
--accent: #2563eb
--accent-hover: #1d4ed8
```

## Landing Page Checklist

### Hero
- [ ] Headline is specific, not generic
- [ ] Subhead explains the value
- [ ] CTA is action-oriented
- [ ] Visual is contextual, not stock
- [ ] Social proof is real

### Features
- [ ] 3-4 key benefits
- [ ] Icon style is consistent
- [ ] Description is concise
- [ ] Visual aids comprehension
- [ ] No "feature dump"

### Pricing
- [ ] Clear value proposition
- [ ] Anchor pricing visible
- [ ] FAQ addresses objections
- [ ] CTA consistent
- [ ] No "best value" badges

### Footer
- [ ] Links organized logically
- [ ] Social icons minimal
- [ ] Copyright is accurate
- [ ] No "Made with love"
- [ ] Privacy links visible

## Common Slop Patterns

### Typography Slop
- Gradient text
- Multiple fonts mixed randomly
- Oversized headlines
- All-caps everything
- Centered paragraphs

### Color Slop
- Rainbow palettes
- Gradient backgrounds
- Saturated blues and purples
- Pure black/white contrast
- Random accent colors

### Layout Slop
- Hero with floating elements
- Multi-column grids everywhere
- Horizontal scroll sections
- Perfect symmetry
- Overcrowded information

### Component Slop
- Rounded corners everywhere
- Drop shadows on everything
- Animated gradients
- Stock photo backgrounds
- Icon soup features

## Building Blocks

### Strong Typography
1. Choose one typeface family
2. Define type scale
3. Set line height rules
4. Create heading hierarchy
5. Apply consistently

### Purposeful Color
1. Start with neutrals
2. Add one accent
3. Use for CTAs only
4. Test contrast
5. Keep dark mode complete

### Clean Structure
1. Define grid
2. Set spacing scale
3. Create component rhythm
4. Maintain alignment
5. Respect breathing room

### Natural Motion
1. Keep durations short
2. Use ease-out enters
3. Use ease-in exits
4. Stagger list items
5. Animate only interactive elements

## Integration

Use with:
- `ai-copywriter`: Strong copy + good design
- `frontend-taste`: Landing page specific guidance
- `simple-english`: Accessible copy alongside tasteful design

The slop test passes when design and copy feel intentional, specific, and human-made.
