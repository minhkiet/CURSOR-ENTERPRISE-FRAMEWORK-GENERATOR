# Create UI Skill

> **Version:** 1.0.0 | **Category:** Development | **Triggers:** tạo ui, create ui, build component, thiết kế giao diện

---

## Goal

Thiết kế và implement UI components hoàn chỉnh:
- Responsive design
- Accessible markup
- Performant rendering
- Consistent styling

## Trigger Conditions

- User yêu cầu tạo UI component
- User cần thiết kế một màn hình
- User muốn implement một layout

## Pre-Check Gates

```
┌─────────────────────────────────────────────────────────────┐
│ P.1: Design Review                                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ Design đã có (Figma, Sketch)?                          │
│ □ Responsive breakpoints đã define?                        │
│ □ Color palette & typography đã có?                        │
│ □ Component states đã mô tả?                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ P.2: Technology Stack                                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ Framework: Vue, React, Angular?                        │
│ □ Styling: Tailwind, CSS Modules, Styled?                │
│ □ Component library: shadcn/ui, Vuetify?                  │
│ □ Icons: Lucide, Heroicons?                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Process Steps

### Step 1: Analyze Design

```
┌────────────────────────────────────────────────────────────┐
│ Component Analysis                                          │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Structure:                                                 │
│  ├── Header                                                │
│  ├── Content                                               │
│  └── Footer                                                │
│                                                            │
│  Components:                                               │
│  ├── Button (states: default, hover, active, disabled)  │
│  ├── Input (states: default, focus, error, disabled)    │
│  └── Card (variants: elevated, flat, outlined)           │
│                                                            │
│  Responsive:                                               │
│  ├── Mobile (< 640px)                                    │
│  ├── Tablet (640px - 1024px)                             │
│  └── Desktop (> 1024px)                                   │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Step 2: Create Component Structure

```
src/
├── components/
│   ├── ui/                    # Base components
│   │   ├── Button/
│   │   │   ├── Button.tsx
│   │   │   ├── Button.css
│   │   │   └── Button.stories.tsx
│   │   └── Input/
│   │       ├── Input.tsx
│   │       ├── Input.css
│   │       └── Input.stories.tsx
│   │
│   └── features/              # Feature components
│       ├── UserCard/
│       └── ProductList/
```

### Step 3: Implement with Accessibility

```tsx
// ✅ Accessible component
interface ButtonProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary';
  disabled?: boolean;
  onClick?: () => void;
}

export function Button({ 
  children, 
  variant = 'primary', 
  disabled = false,
  onClick 
}: ButtonProps) {
  return (
    <button
      type="button"
      className={`btn btn--${variant}`}
      disabled={disabled}
      onClick={onClick}
      aria-disabled={disabled}
    >
      {children}
    </button>
  );
}
```

### Step 4: Implement Responsive Styles

```css
/* Tailwind */
<button className="
  px-4 py-2           /* Default: mobile */
  text-base
  rounded-lg
  bg-blue-600
  text-white
  hover:bg-blue-700
  disabled:opacity-50
  disabled:cursor-not-allowed
  
  md:px-6 md:py-3    /* Tablet */
  lg:px-8 lg:text-lg  /* Desktop */
">
  {children}
</button>
```

### Step 5: Add Component Stories

```tsx
// Component Story for testing
const meta: Meta<typeof Button> = {
  component: Button,
  tags: ['autodocs'],
  argTypes: {
    variant: { control: 'select', options: ['primary', 'secondary'] },
  },
};

export const Primary = {
  args: {
    children: 'Primary Button',
    variant: 'primary',
  },
};

export const Secondary = {
  args: {
    children: 'Secondary Button',
    variant: 'secondary',
  },
};

export const Disabled = {
  args: {
    children: 'Disabled Button',
    disabled: true,
  },
};
```

## Post-Check Gates

```
┌─────────────────────────────────────────────────────────────┐
│ C.1: Accessibility                                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ Semantic HTML used?                                      │
│ □ ARIA labels provided?                                    │
│ □ Keyboard navigation works?                               │
│ □ Focus states visible?                                    │
│ □ Color contrast sufficient?                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ C.2: Responsiveness                                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ Mobile view correct?                                     │
│ □ Tablet view correct?                                     │
│ □ Desktop view correct?                                    │
│ □ Touch targets ≥ 44px?                                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ C.3: Performance                                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ No unnecessary re-renders?                               │
│ □ Images optimized?                                        │
│ □ CSS not bloated?                                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Output

```
✅ UI Component hoàn chỉnh
├── Component file (TSX/Vue)
├── Styles (CSS/Tailwind)
├── Stories (for testing)
├── Types (TypeScript)
└── Tests (optional)
```
