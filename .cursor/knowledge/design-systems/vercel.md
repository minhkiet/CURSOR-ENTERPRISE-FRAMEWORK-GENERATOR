# Vercel Design System

## 1. Colors

```css
:root {
  /* Primary - Black */
  --color-primary: #000000;
  --color-primary-hover: #171717;
  
  /* Background */
  --color-bg-primary: #FFFFFF;
  --color-bg-secondary: #F4F4F5;
  --color-bg-elevated: #FFFFFF;
  
  /* Text */
  --color-text-primary: #000000;
  --color-text-secondary: #52525B;
  --color-text-muted: #A1A1AA;
  
  /* Border */
  --color-border: #E4E4E7;
  --color-border-strong: #D4D4D8;
  
  /* Semantic */
  --color-success: #10B981;
  --color-warning: #F59E0B;
  --color-error: #EF4444;
  --color-info: #3B82F6;
}
```

## 2. Typography

```css
:root {
  /* Display - Inter */
  --font-display: 'Inter', system-ui, -apple-system, sans-serif;
  
  /* Sans - Inter */
  --font-sans: 'Inter', system-ui, -apple-system, sans-serif;
  --font-sans-weight-normal: 400;
  --font-sans-weight-medium: 500;
  --font-sans-weight-semibold: 600;
  
  /* Mono */
  --font-mono: 'JetBrains Mono', 'SF Mono', monospace;
  
  /* Scale */
  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.25rem;
  --text-2xl: 1.5rem;
  --text-3xl: 1.875rem;
  --text-4xl: 2.25rem;
  
  /* Line Heights */
  --leading-tight: 1.25;
  --leading-normal: 1.5;
  
  /* Letter Spacing */
  --tracking-tight: -0.02em;
  --tracking-normal: 0;
  --tracking-wide: 0.02em;
}
```

## 3. Spacing

```css
:root {
  --space-0: 0;
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-5: 1.25rem;
  --space-6: 1.5rem;
  --space-8: 2rem;
  --space-10: 2.5rem;
  --space-12: 3rem;
  --space-16: 4rem;
  --space-20: 5rem;
  --space-24: 6rem;
}
```

## 4. Layout

```css
:root {
  --grid-columns: 12;
  --grid-gap: 1.5rem;
  --container-max: 1280px;
  --container-padding: 1rem;
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;
}
```

## 5. Components

### Button

```css
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.625rem 1.25rem;
  font-size: 0.875rem;
  font-weight: 500;
  border-radius: 0.375rem;
  transition: all 0.2s ease;
}

.btn-primary {
  background: var(--color-primary);
  color: white;
}

.btn-primary:hover {
  background: var(--color-primary-hover);
}

.btn-secondary {
  background: transparent;
  color: var(--color-text-primary);
  border: 1px solid var(--color-border);
}

.btn-secondary:hover {
  border-color: var(--color-border-strong);
  background: var(--color-bg-secondary);
}
```

## 6. Motion

```css
:root {
  --duration-fast: 0.1s;
  --duration-normal: 0.2s;
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
}
```

## 7-9. Voice, Brand, Anti-Patterns

```css
:root {
  --voice-tone: professional;
}

.anti-pattern {
  /* Avoid heavy shadows */
  /* Avoid large border-radius */
  /* Avoid decorative patterns */
  /* Keep it minimal and functional */
}
```
