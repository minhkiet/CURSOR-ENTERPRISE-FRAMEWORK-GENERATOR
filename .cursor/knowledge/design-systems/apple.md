# Apple Human Interface Design System

## 1. Colors

```css
:root {
  /* Primary - System Blue */
  --color-primary: #007AFF;
  --color-primary-hover: #0056CC;
  
  /* System Colors */
  --color-blue: #007AFF;
  --color-green: #34C759;
  --color-indigo: #5856D6;
  --color-orange: #FF9500;
  --color-pink: #FF2D55;
  --color-purple: #AF52DE;
  --color-red: #FF3B30;
  --color-teal: #5AC8FA;
  --color-yellow: #FFCC00;
  
  /* Background */
  --color-bg-primary: #FFFFFF;
  --color-bg-secondary: #F2F2F7;
  --color-bg-tertiary: #FFFFFF;
  --color-bg-grouped: #F2F2F7;
  
  /* Text */
  --color-text-primary: #000000;
  --color-text-secondary: rgba(60, 60, 67, 0.6);
  --color-text-tertiary: rgba(60, 60, 67, 0.3);
  --color-text-placeholder: rgba(60, 60, 67, 0.3);
  
  /* Separator */
  --color-separator: rgba(60, 60, 67, 0.12);
  --color-separator-opaque: #C6C6C8;
  
  /* Fill Colors */
  --color-fill: rgba(120, 120, 128, 0.2);
  --color-fill-secondary: rgba(120, 120, 128, 0.16);
  --color-fill-tertiary: rgba(118, 118, 128, 0.12);
}
```

## 2. Typography

```css
:root {
  /* SF Pro Display */
  --font-display: -apple-system, BlinkMacSystemFont, 'SF Pro Display', system-ui, sans-serif;
  
  /* SF Pro Text */
  --font-sans: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif;
  
  /* SF Mono */
  --font-mono: 'SF Mono', 'Menlo', monospace;
  
  /* Scale - iOS */
  --text-2xlarge: 2.375rem;  /* 38px - Large Title */
  --text-xlarge: 1.75rem;     /* 28px - Title 1 */
  --text-large: 1.375rem;     /* 22px - Title 2 */
  --text-title3: 1.25rem;     /* 20px - Title 3 */
  --text-headline: 1rem;       /* 17px - Headline */
  --text-body: 1rem;          /* 17px - Body */
  --text-callout: 0.9375rem;  /* 15px - Callout */
  --text-subhead: 0.875rem;    /* 15px - Subhead */
  --text-footnote: 0.8125rem; /* 13px - Footnote */
  --text-caption1: 0.75rem;    /* 12px - Caption 1 */
  --text-caption2: 0.6875rem;  /* 11px - Caption 2 */
  
  /* Font Weights */
  --font-weight-regular: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  
  /* Line Heights */
  --leading-tight: 1.2;
  --leading-normal: 1.35;
  --leading-relaxed: 1.5;
}
```

## 3. Spacing

```css
:root {
  /* 4pt Grid */
  --space-0: 0;
  --space-1: 0.25rem;    /* 4pt */
  --space-2: 0.5rem;      /* 8pt */
  --space-3: 0.75rem;     /* 12pt */
  --space-4: 1rem;        /* 16pt */
  --space-5: 1.25rem;    /* 20pt */
  --space-6: 1.5rem;     /* 24pt */
  --space-8: 2rem;        /* 32pt */
  --space-10: 2.5rem;     /* 40pt */
  --space-12: 3rem;       /* 48pt */
  --space-16: 4rem;       /* 64pt */
  --space-20: 5rem;       /* 80pt */
  
  /* Corner Radii */
  --radius-small: 0.375rem;  /* 6pt */
  --radius-medium: 0.5rem;   /* 8pt */
  --radius-large: 0.75rem;  /* 12pt */
  --radius-xlarge: 1rem;     /* 16pt */
}
```

## 4. Layout

```css
:root {
  /* iOS Layout */
  --grid-columns: 12;
  --grid-gap: 1rem;
  
  /* Container */
  --container-max: 1024px;
  --container-padding: 1rem;
  
  /* Breakpoints */
  --breakpoint-sm: 320px;
  --breakpoint-md: 375px;
  --breakpoint-lg: 414px;
  --breakpoint-tablet: 768px;
  --breakpoint-desktop: 1024px;
  
  /* Safe Area */
  --safe-area-inset-top: env(safe-area-inset-top);
  --safe-area-inset-bottom: env(safe-area-inset-bottom);
  --safe-area-inset-left: env(safe-area-inset-left);
  --safe-area-inset-right: env(safe-area-inset-right);
}
```

## 5. Components

### Button

```css
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 2.75rem;
  padding: 0.875rem 1.25rem;
  font-size: 1rem;
  font-weight: 500;
  border-radius: var(--radius-medium);
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
  background: var(--color-fill-secondary);
  color: var(--color-primary);
}

.btn-tertiary {
  background: transparent;
  color: var(--color-primary);
}
```

### Input

```css
.input {
  display: block;
  width: 100%;
  height: 2.75rem;
  padding: 0 1rem;
  font-size: 1rem;
  background: var(--color-fill-secondary);
  border: none;
  border-radius: var(--radius-medium);
  color: var(--color-text-primary);
}

.input:focus {
  outline: none;
  background: var(--color-bg-primary);
  box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.3);
}
```

### Card

```css
.card {
  background: var(--color-bg-primary);
  border-radius: var(--radius-large);
  padding: 1.25rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.card-grouped {
  background: var(--color-bg-primary);
  border-radius: var(--radius-large);
  overflow: hidden;
}

.card-grouped-item {
  padding: 1rem 1.25rem;
  border-bottom: 0.5px solid var(--color-separator);
}

.card-grouped-item:last-child {
  border-bottom: none;
}
```

### List

```css
.list {
  background: var(--color-bg-primary);
  border-radius: var(--radius-large);
  overflow: hidden;
}

.list-item {
  display: flex;
  align-items: center;
  min-height: 2.75rem;
  padding: 0.75rem 1.25rem;
  border-bottom: 0.5px solid var(--color-separator);
}

.list-item:last-child {
  border-bottom: none;
}
```

## 6. Motion

```css
:root {
  /* Spring Animations */
  --duration-instant: 0.1s;
  --duration-fast: 0.2s;
  --duration-normal: 0.3s;
  --duration-slow: 0.4s;
  
  /* iOS Spring */
  --ease-spring: cubic-bezier(0.175, 0.885, 0.32, 1.275);
  --ease-smooth: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-dramatic: cubic-bezier(0.3, 0, 0, 1);
  
  /* Animation Types */
  --animation-push: push 0.3s ease-out;
  --animation-pop: pop 0.3s ease-out;
  --animation-fade: fade 0.2s ease-out;
  --animation-slide: slide 0.3s ease-out;
}

@keyframes push {
  0% { transform: translateX(0); }
  100% { transform: translateX(-100%); }
}

@keyframes pop {
  0% { transform: scale(0.95); opacity: 0; }
  100% { transform: scale(1); opacity: 1; }
}

@keyframes fade {
  0% { opacity: 0; }
  100% { opacity: 1; }
}

@keyframes slide {
  0% { transform: translateY(20px); opacity: 0; }
  100% { transform: translateY(0); opacity: 1; }
}
```

## 7. Voice & Tone

```css
:root {
  /* Clear & Direct */
  --voice-tone: conversational;
  
  /* iOS Terminology */
  --term-cancel: "Cancel";
  --term-done: "Done";
  --term-delete: "Delete";
  --term-edit: "Edit";
  
  /* Messages */
  --error-message: "An error occurred.";
  --loading-message: "Loading...";
  --empty-message: "No Content";
}
```

## 8. Brand

```css
:root {
  /* SF Symbols */
  --symbol-font: 'SF Symbols', -apple-system;
  
  /* Icon Sizes */
  --icon-size-small: 1rem;
  --icon-size-medium: 1.5rem;
  --icon-size-large: 2rem;
  
  /* App Icon */
  --app-icon-radius: 1.375rem;
}
```

## 9. Anti-Patterns

```css
/* AVOID in Apple-style design */

/* 1. Hard edges - iOS is smooth */
.bad { border-radius: 0; }

/* 2. Heavy borders */
.bad { border: 2px solid #000; }

/* 3. Drop shadows on cards */
.bad { box-shadow: 0 4px 20px rgba(0,0,0,0.3); }

/* 4. Solid backgrounds for grouped lists */
.bad { background: #F00; }

/* 5. Windows-style buttons */
.bad { border: 1px solid #333; background: #DDD; }

/* 6. Overly decorative elements */
.bad { background: url('/pattern.png'); }
```

## Usage Example

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Apple-style App</title>
  <style>
    /* Apple Design Tokens */
    :root {
      --color-primary: #007AFF;
      --font-sans: -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif;
      --radius-medium: 0.5rem;
    }
    
    body {
      font-family: var(--font-sans);
      background: #F2F2F7;
      color: #000;
    }
    
    .card {
      background: white;
      border-radius: var(--radius-medium);
      padding: 1rem;
    }
    
    .btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-height: 2.75rem;
      padding: 0.875rem 1.25rem;
      font-size: 1rem;
      font-weight: 500;
      background: var(--color-primary);
      color: white;
      border-radius: var(--radius-medium);
    }
  </style>
</head>
<body>
  <main>
    <div class="card">
      <h1>Large Title</h1>
      <p>Body text here</p>
      <button class="btn">Button</button>
    </div>
  </main>
</body>
</html>
```
