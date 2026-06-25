# CEF Landing Vue 3 App

Enterprise-grade Vue 3 landing page cho Cursor Enterprise Framework.

## Tech Stack

- **Vue 3** với Composition API và `<script setup>`
- **TypeScript** cho type safety
- **Vite** cho fast development và building
- **CSS Variables** cho design tokens

## Features

- Responsive design với mobile-first approach
- Dark theme với premium SaaS aesthetic
- Intersection Observer animations
- Interactive components showcase
- Rules & Skills explorer với search và filtering
- Token optimization visualization
- Copy-to-clipboard functionality
- Smooth scroll navigation

## Project Structure

```
vue-app/
├── src/
│   ├── components/
│   │   ├── NavBar.vue
│   │   ├── HeroSection.vue
│   │   ├── StatsBar.vue
│   │   ├── ExplorerSection.vue
│   │   ├── PrinciplesSection.vue
│   │   ├── ArchitectureSection.vue
│   │   ├── ComponentsSection.vue
│   │   ├── DomainsSection.vue
│   │   ├── OptimizationSection.vue
│   │   ├── GettingStartedSection.vue
│   │   └── FooterSection.vue
│   ├── composables/
│   │   └── useIntersectionObserver.ts
│   ├── styles/
│   │   └── main.css
│   ├── App.vue
│   ├── main.ts
│   └── env.d.ts
├── public/
│   └── favicon.svg
├── index.html
├── package.json
├── vite.config.ts
├── tsconfig.json
└── tsconfig.node.json
```

## Quick Start

Double-click these batch files to get started:

```bash
start.bat    # Install dependencies & setup
upweb.bat   # Build & deploy to Vercel
```

Or use commands manually:

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Deployment

The app is configured for Vercel deployment via `vercel.json`:
- Framework: Vite
- Build command: `npm run build`
- Output directory: `dist`

Run `upweb.bat` or manually:
1. `npm run build`
2. `vercel --prod`

## Design System

Sử dụng CSS custom properties cho design tokens:

- **Colors**: Violet/Cyan accent palette
- **Typography**: Inter + JetBrains Mono
- **Spacing**: Consistent spacing scale
- **Radius**: Border radius tokens
- **Shadows**: Elevation system

## Components

### NavBar
- Fixed position với blur backdrop
- Responsive mobile menu
- Smooth scroll navigation

### HeroSection
- Animated badge pill
- Gradient title
- Terminal mockup với typing animation
- Stats cards với hover effects

### StatsBar
- Animated counter numbers
- Staggered reveal animation

### ExplorerSection
- Category filtering
- Real-time search
- Rules/Skills toggle
- Empty state handling

### PrinciplesSection
- Card hover animations
- Staggered reveal

### ArchitectureSection
- File tree visualization
- Tech stack grid
- Fade-in animations

### ComponentsSection
- Full UI component showcase
- Buttons, badges, inputs, cards, alerts, progress, tabs

### DomainsSection
- Domain cards grid
- Spotlight badge cho special domains
- Staggered animations

### OptimizationSection
- Token savings chart
- Animated bar visualization
- Feature list

### GettingStartedSection
- Step cards
- Copy-to-clipboard functionality
- Scripts reference table

### FooterSection
- Multi-column layout
- External links với proper rel attributes

## Best Practices

- Composition API với `<script setup>`
- TypeScript strict mode
- CSS scoped styles trong components
- Reusable composables
- Semantic HTML
- Accessibility considerations
- Performance optimized animations

## License

MIT
