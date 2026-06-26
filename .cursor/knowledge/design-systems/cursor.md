# Cursor Design System

## 1. Colors

```css
:root {
  /* Primary - Deep Purple */
  --color-primary: #7C3AED;
  --color-primary-hover: #6D28D9;
  --color-primary-active: #5B21B6;
  
  /* Secondary - Warm Gray */
  --color-secondary: #78716C;
  --color-secondary-hover: #57534E;
  
  /* Accent - Cyan */
  --color-accent: #22D3EE;
  --color-accent-hover: #06B6D4;
  
  /* Background */
  --color-bg-primary: #09090B;
  --color-bg-secondary: #18181B;
  --color-bg-elevated: #27272A;
  --color-bg-overlay: rgba(0, 0, 0, 0.8);
  
  /* Text */
  --color-text-primary: #FAFAFA;
  --color-text-secondary: #A1A1AA;
  --color-text-muted: #71717A;
  
  /* Border */
  --color-border: #3F3F46;
  --color-border-strong: #52525B;
  
  /* Semantic */
  --color-success: #22C55E;
  --color-warning: #F59E0B;
  --color-error: #EF4444;
  --color-info: #3B82F6;
}
```

## 2. Typography

```css
:root {
  /* Display - Geist Display */
  --font-display: 'Geist', system-ui, -apple-system, sans-serif;
  --font-display-weight: 700;
  
  /* Sans - Geist */
  --font-sans: 'Geist', system-ui, -apple-system, sans-serif;
  --font-sans-weight-normal: 400;
  --font-sans-weight-medium: 500;
  --font-sans-weight-semibold: 600;
  
  /* Mono - Geist Mono */
  --font-mono: 'Geist Mono', 'SF Mono', 'Fira Code', monospace;
  --font-mono-weight: 400;
  
  /* Scale */
  --text-xs: 0.75rem;      /* 12px */
  --text-sm: 0.875rem;     /* 14px */
  --text-base: 1rem;       /* 16px */
  --text-lg: 1.125rem;     /* 18px */
  --text-xl: 1.25rem;      /* 20px */
  --text-2xl: 1.5rem;     /* 24px */
  --text-3xl: 1.875rem;    /* 30px */
  --text-4xl: 2.25rem;    /* 36px */
  
  /* Line Heights */
  --leading-tight: 1.25;
  --leading-normal: 1.5;
  --leading-relaxed: 1.625;
  
  /* Letter Spacing */
  --tracking-tight: -0.02em;
  --tracking-normal: 0;
  --tracking-wide: 0.02em;
}
```

## 3. Spacing

```css
:root {
  /* 4px Base Scale */
  --space-0: 0;
  --space-1: 0.25rem;    /* 4px */
  --space-2: 0.5rem;     /* 8px */
  --space-3: 0.75rem;    /* 12px */
  --space-4: 1rem;       /* 16px */
  --space-5: 1.25rem;    /* 20px */
  --space-6: 1.5rem;     /* 24px */
  --space-8: 2rem;       /* 32px */
  --space-10: 2.5rem;    /* 40px */
  --space-12: 3rem;      /* 48px */
  --space-16: 4rem;      /* 64px */
  --space-20: 5rem;      /* 80px */
  --space-24: 6rem;      /* 96px */
}
```

## 4. Layout

```css
:root {
  /* Grid */
  --grid-columns: 12;
  --grid-gap: 1.5rem;
  
  /* Container */
  --container-max: 1280px;
  --container-padding: 1rem;
  
  /* Breakpoints */
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;
  --breakpoint-2xl: 1536px;
  
  /* Section */
  --section-padding-y: 5rem;
  --section-padding-x: 1rem;
}
```

## 5. Components

### Button

```css
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.625rem 1rem;
  font-size: 0.875rem;
  font-weight: 500;
  border-radius: 0.5rem;
  transition: all 0.15s ease;
}

.btn-primary {
  background: var(--color-primary);
  color: white;
}

.btn-primary:hover {
  background: var(--color-primary-hover);
}

.btn-secondary {
  background: var(--color-bg-elevated);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border);
}

.btn-ghost {
  background: transparent;
  color: var(--color-text-secondary);
}

.btn-ghost:hover {
  background: var(--color-bg-elevated);
  color: var(--color-text-primary);
}
```

### Input

```css
.input {
  display: block;
  width: 100%;
  padding: 0.625rem 0.875rem;
  font-size: 0.875rem;
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  border-radius: 0.5rem;
  color: var(--color-text-primary);
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
}

.input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.15);
}

.input::placeholder {
  color: var(--color-text-muted);
}
```

### Card

```css
.card {
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: 0.75rem;
  padding: 1.5rem;
}

.card-hover:hover {
  border-color: var(--color-border-strong);
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
}
```

### Navigation

```css
.nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 4rem;
  padding: 0 1rem;
  background: var(--color-bg-primary);
  border-bottom: 1px solid var(--color-border);
}
```

## 6. Motion

```css
:root {
  /* Durations */
  --duration-fast: 0.1s;
  --duration-normal: 0.15s;
  --duration-slow: 0.3s;
  
  /* Easings */
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
  
  /* Animation Patterns */
  --animation-fade-in: fadeIn 0.3s var(--ease-out);
  --animation-slide-up: slideUp 0.3s var(--ease-out);
  --animation-scale-in: scaleIn 0.2s var(--ease-spring);
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes scaleIn {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}
```

## 7. Voice & Tone

```css
:root {
  /* Writing Style */
  --voice-tone: professional;
  --voice-formality: moderate;
  
  /* Error Messages */
  --error-heading: "Something went wrong";
  --error-body: "Please try again or contact support.";
  
  /* Success Messages */
  --success-heading: "Success";
  --success-body: "Your changes have been saved.";
  
  /* Loading */
  --loading-text: "Loading...";
  --empty-heading: "No items";
  --empty-body: "There are no items to display.";
}
```

## 8. Brand

```css
:root {
  /* Logo */
  --logo-url: url('/logo.svg');
  --logo-width: 2rem;
  --logo-height: 2rem;
  
  /* Imagery */
  --image-radius: 0.75rem;
  --image-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  
  /* Iconography */
  --icon-size-sm: 1rem;
  --icon-size-md: 1.25rem;
  --icon-size-lg: 1.5rem;
  --icon-stroke: 1.5px;
}
```

## 9. Anti-Patterns

```css
/* AVOID */

/* 1. Generic gradients */
.avoid-gradient {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* 2. Excessive shadows */
.avoid-shadow {
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}

/* 3. Large border-radius everywhere */
.avoid-radius {
  border-radius: 9999px;
}

/* 4. Inconsistent spacing */
.avoid-spacing {
  padding: 1rem 2rem 0.5rem 1.5rem;
}

/* 5. Too many colors */
.avoid-colors {
  background: #FF6B6B;
  color: #4ECDC4;
  border: 2px solid #FFE66D;
}
```

## Usage Example

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Cursor-style App</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    /* Copy CSS variables above */
  </style>
</head>
<body>
  <nav class="nav">
    <div class="nav-logo">Logo</div>
    <div class="nav-links">
      <a href="#" class="btn btn-ghost">Features</a>
      <a href="#" class="btn btn-ghost">Pricing</a>
      <a href="#" class="btn btn-primary">Get Started</a>
    </div>
  </nav>
  
  <main>
    <section class="hero">
      <h1 class="display">Build faster with AI</h1>
      <p class="body">Cursor is the AI-powered code editor for professionals.</p>
      <button class="btn btn-primary">Download</button>
    </section>
  </main>
</body>
</html>
```
