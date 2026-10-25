# UI/UX Pro Max

> **Source:** [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) (117k stars)
> **Version:** 2.13.0 | **License:** MIT

AI-powered design intelligence for building professional UI/UX across multiple platforms.

## Features

| Category | Count | Description |
|----------|------:|-------------|
| **UI Styles** | 79 | Glassmorphism, Claymorphism, Minimalism, Brutalism, Neumorphism, Bento Grid, Dark Mode, AI-Native UI |
| **Color Palettes** | 192 | Industry-specific palettes aligned 1:1 with product types |
| **Font Pairings** | 74 | Curated typography combinations with Google Fonts imports |
| **Chart Types** | 25 | Dashboard and analytics recommendations |
| **UX Guidelines** | 119 | Best practices, anti-patterns, accessibility rules |
| **Reasoning Rules** | 192 | Industry-specific design system generation |

## Design System Generator

Automatically generates a complete, tailored design system for your project:

```bash
python .cursor/skills/ui-ux-pro-max/scripts/search.py "beauty spa wellness" --design-system -p "Serenity Spa"
```

Output includes:
- **Pattern** - Landing page structure (e.g., Hero-Centric + Social Proof)
- **Style** - Visual direction (e.g., Soft UI Evolution)
- **Colors** - Primary, secondary, CTA, background, text with hex codes
- **Typography** - Font pairing with Google Fonts link
- **Key Effects** - Animations and interactions
- **Anti-Patterns** - What NOT to do for the industry
- **Pre-Delivery Checklist** - Validation before delivery

## Supported Stacks

| Category | Stacks |
|----------|--------|
| **Web (HTML)** | HTML + Tailwind (default) |
| **React Ecosystem** | React, Next.js, shadcn/ui |
| **Vue Ecosystem** | Vue, Nuxt.js, Nuxt UI |
| **Angular** | Angular |
| **PHP** | Laravel (Blade, Livewire, Inertia.js) |
| **Other Web** | Svelte, Astro, Three.js |
| **Desktop** | JavaFX, WPF, WinUI 3, Avalonia, Uno Platform, UWP |
| **iOS** | SwiftUI |
| **Android** | Jetpack Compose |
| **Cross-Platform** | React Native, Flutter |

## Usage

### Natural Language

```
Build a landing page for my SaaS product
Create a dashboard for healthcare analytics
Design a portfolio website with dark mode
Make a mobile app UI for e-commerce
```

### Design System with Project Name

```bash
python .cursor/skills/ui-ux-pro-max/scripts/search.py "fintech banking" --design-system -p "MyBank" --persist
```

### Stack-Specific Search

```bash
python .cursor/skills/ui-ux-pro-max/scripts/search.py "form validation" --stack react
python .cursor/skills/ui-ux-pro-max/scripts/search.py "responsive layout" --stack html-tailwind
python .cursor/skills/ui-ux-pro-max/scripts/search.py "glassmorphism" --domain style
python .cursor/skills/ui-ux-pro-max/scripts/search.py "elegant serif" --domain typography
```

### Domain Search

| Domain | Description |
|--------|-------------|
| `style` | UI visual styles |
| `color` | Color palettes |
| `chart` | Chart types |
| `landing` | Landing page patterns |
| `product` | Product types (192 categories) |
| `ux` | UX guidelines |
| `typography` | Typography |
| `google-fonts` | Google Fonts |
| `icons` | Icon recommendations |
| `gsap` | GSAP animations |
| `react` | React-specific |
| `web` | General web |

## Design Dials (1-10)

Customize design output:

```bash
python .cursor/skills/ui-ux-pro-max/scripts/search.py "SaaS dashboard" \
  --design-system \
  --variance 8 \
  --motion 9 \
  --density 7
```

| Dial | Range | Description |
|------|-------|-------------|
| `variance` | 1-10 | 1=centered/minimal, 10=bold/asymmetric |
| `motion` | 1-10 | 1=subtle, 10=complex |
| `density` | 1-10 | 1=spacious, 10=dense/dashboard |

## Persistence (Master + Overrides)

Save design system for hierarchical retrieval across sessions:

```bash
# Generate and persist to design-system/MASTER.md
python .cursor/skills/ui-ux-pro-max/scripts/search.py "SaaS dashboard" --design-system --persist -p "MyApp"

# Also create page-specific override
python .cursor/skills/ui-ux-pro-max/scripts/search.py "checkout page" --design-system --persist -p "MyApp" --page "checkout"
```

This creates:

```
design-system/
├── MASTER.md           # Global Source of Truth
└── pages/
    └── checkout.md     # Page-specific overrides
```

## Resilient Text & Compact UI

- Balanced heading wrapping is progressive enhancement, not guarantee
- Essential text must reflow without clipping at narrow widths, browser zoom, text scaling
- Chip/tag collections should wrap or use `+n` disclosure
- Badge meaning cannot rely on color alone
- Rapid interactions must respect reduced-motion preferences

## Anti-Patterns to Avoid

Industry-specific anti-patterns are included in design system output:

| Industry | Avoid |
|----------|-------|
| Banking | AI purple/pink gradients, playful animations |
| Healthcare | Bright neon, harsh contrasts |
| Luxury | Flat design, stock imagery |
| Tech/SaaS | Excessive decoration, outdated patterns |

## Related Skills

| Skill | Path | Description |
|-------|------|-------------|
| `frontend-taste` | `skills/ui_frontend-taste/` | Anti-slop frontend (pre/post gates) |
| `hallmark` | `skills/ui_hallmark/` | 57 slop-test gates |
| `dashboard-ui` | `skills/ui_dashboard-ui/` | Dashboard components |
| `frontend-redesign` | `skills/ui_frontend-redesign/` | Redesign existing UI |

## References

- Repository: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
- Homepage: https://uupm.cc
- CLI: `npm install -g ui-ux-pro-max-cli`

---

*Integrated from upstream repository - data files in `data/`, scripts in `scripts/`*
