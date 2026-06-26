# Linear Design System

## 1. Colors

```css
:root {
  /* Primary - Indigo */
  --color-primary: #5E6AD2;
  --color-primary-hover: #4F56C1;
  --color-primary-subtle: rgba(94, 106, 210, 0.1);
  
  /* Accent - Amber */
  --color-accent: #FF9F1C;
  --color-accent-hover: #E8930A;
  
  /* Background - Gray */
  --color-bg-base: #F7F7F8;
  --color-bg-surface: #FFFFFF;
  --color-bg-overlay: rgba(0, 0, 0, 0.5);
  --color-bg-hover: #EFEFEF;
  
  /* Text */
  --color-text-primary: #1A1A1A;
  --color-text-secondary: #6B6B6B;
  --color-text-tertiary: #ABABAB;
  --color-text-inverse: #FFFFFF;
  
  /* Border */
  --color-border: #E5E5E5;
  --color-border-strong: #D4D4D4;
  --color-border-subtle: #F0F0F0;
  
  /* Semantic */
  --color-success: #26D367;
  --color-success-subtle: rgba(38, 211, 103, 0.1);
  --color-warning: #FF9F1C;
  --color-warning-subtle: rgba(255, 159, 28, 0.1);
  --color-error: #EF4444;
  --color-error-subtle: rgba(239, 68, 68, 0.1);
  --color-info: #5E6AD2;
  --color-info-subtle: rgba(94, 106, 210, 0.1);
}
```

## 2. Typography

```css
:root {
  /* Display - Inter Tight */
  --font-display: 'Inter Tight', 'Inter', system-ui, sans-serif;
  --font-display-weight: 600;
  
  /* Sans - Inter */
  --font-sans: 'Inter', system-ui, -apple-system, sans-serif;
  --font-sans-weight-normal: 400;
  --font-sans-weight-medium: 500;
  --font-sans-weight-semibold: 600;
  
  /* Mono - JetBrains Mono */
  --font-mono: 'JetBrains Mono', 'SF Mono', monospace;
  
  /* Scale */
  --text-2xs: 0.625rem;   /* 10px */
  --text-xs: 0.6875rem;   /* 11px */
  --text-sm: 0.8125rem;   /* 13px */
  --text-base: 0.9375rem; /* 15px */
  --text-lg: 1.0625rem;   /* 17px */
  --text-xl: 1.25rem;     /* 20px */
  --text-2xl: 1.5rem;     /* 24px */
  --text-3xl: 1.875rem;   /* 30px */
  
  /* Line Heights */
  --leading-tight: 1.2;
  --leading-normal: 1.5;
  
  /* Letter Spacing */
  --tracking-tight: -0.01em;
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
}
```

## 4. Layout

```css
:root {
  /* Grid */
  --grid-columns: 12;
  --grid-gap: 1.5rem;
  
  /* Container */
  --container-max: 1200px;
  --container-padding: 1rem;
  
  /* Sidebar */
  --sidebar-width: 240px;
  --sidebar-collapsed: 56px;
  
  /* Breakpoints */
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
  gap: 0.375rem;
  padding: 0.5rem 0.875rem;
  font-size: 0.8125rem;
  font-weight: 500;
  border-radius: 0.375rem;
  transition: all 0.1s ease;
}

.btn-primary {
  background: var(--color-primary);
  color: white;
}

.btn-primary:hover {
  background: var(--color-primary-hover);
}

.btn-secondary {
  background: var(--color-bg-surface);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border);
}

.btn-secondary:hover {
  background: var(--color-bg-hover);
  border-color: var(--color-border-strong);
}

.btn-ghost {
  background: transparent;
  color: var(--color-text-secondary);
}

.btn-ghost:hover {
  background: var(--color-bg-hover);
  color: var(--color-text-primary);
}
```

### Input

```css
.input {
  display: block;
  width: 100%;
  padding: 0.5rem 0.75rem;
  font-size: 0.8125rem;
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: 0.375rem;
  color: var(--color-text-primary);
  transition: border-color 0.1s ease;
}

.input:focus {
  outline: none;
  border-color: var(--color-primary);
}

.input::placeholder {
  color: var(--color-text-tertiary);
}
```

### Card

```css
.card {
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: 0.5rem;
  padding: 1rem;
}

.card-interactive {
  cursor: pointer;
}

.card-interactive:hover {
  border-color: var(--color-border-strong);
  background: var(--color-bg-hover);
}
```

## 6. Motion

```css
:root {
  /* Durations */
  --duration-fast: 0.1s;
  --duration-normal: 0.15s;
  --duration-slow: 0.25s;
  
  /* Easings */
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
  
  /* Animation */
  --animation-fade: opacity 0.15s ease;
  --animation-slide: transform 0.15s ease;
}
```

## 7. Voice & Tone

```css
:root {
  /* Professional & Direct */
  --voice-tone: professional;
  
  /* Messages */
  --error-message: "Something went wrong. Please try again.";
  --success-message: "Changes saved.";
  --empty-state: "No items yet.";
}
```

## 8. Brand

```css
:root {
  /* Logo */
  --logo-url: url('/linear-logo.svg');
  --logo-width: 1.5rem;
  --logo-height: 1.5rem;
  
  /* Icons */
  --icon-size-xs: 0.75rem;
  --icon-size-sm: 1rem;
  --icon-size-md: 1.25rem;
  --icon-size-lg: 1.5rem;
}
```

## 9. Anti-Patterns

```css
/* AVOID */

/* 1. Large border-radius */
.bad { border-radius: 1rem; }

/* 2. Heavy shadows */
.bad { box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2); }

/* 3. Bold colors everywhere */
.bad { background: #FF0000; color: #00FF00; }

/* 4. Large padding */
.bad { padding: 2rem 3rem; }

/* 5. Decorative elements */
.bad { background-image: url('/pattern.svg'); }
```

## Usage Example

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Linear-style App</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    /* Copy CSS variables above */
  </style>
</head>
<body>
  <div class="app">
    <aside class="sidebar">...</aside>
    <main class="content">
      <div class="card">
        <h2>Project Name</h2>
        <p>Description</p>
      </div>
    </main>
  </div>
</body>
</html>
```
