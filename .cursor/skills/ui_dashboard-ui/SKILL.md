---
name: dashboard-ui
description: "Dashboard & Form UI optimization skill. Professional component design với synchronized icons, consistent images, clear colors. Không AI-slop, không generic. Tối ưu cho dashboard, admin panel, forms, inputs, pickers, buttons, labels, notices."
---

# Dashboard UI Optimization Skill

Build professional dashboard interfaces that look custom-built, not templated.

## 1. Component Categories

### 1.1 Form Components

```
┌─────────────────────────────────────────────────────────────────┐
│ INPUT TYPES                                                       │
├─────────────────────────────────────────────────────────────────┤
│ Text Input    │ Textarea     │ Number Input   │ Email Input  │
│ Password      │ Search       │ URL Input      │ Phone Input  │
│ Currency      │ Percentage   │ IP Address     │ Slug/Key     │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ SELECT COMPONENTS                                                 │
├─────────────────────────────────────────────────────────────────┤
│ Dropdown      │ Multi-Select  │ Combobox     │ Tag Input     │
│ Checkbox      │ Radio Group   │ Toggle       │ Switch       │
│ Select Tree   │ Country Picker│ Time Zone    │ Currency      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ DATE/TIME COMPONENTS                                              │
├─────────────────────────────────────────────────────────────────┤
│ Date Picker  │ Time Picker  │ DateTime     │ Range Picker  │
│ Week Picker  │ Month Picker │ Quarter      │ Year Picker   │
│ Range Slider │ Date Range   │ Schedule     │ Recurring     │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ ACTION COMPONENTS                                                 │
├─────────────────────────────────────────────────────────────────┤
│ Button       │ Icon Button  │ Button Group │ Split Button  │
│ Menu        │ Dropdown     │ Action Bar   │ Command Bar  │
│ FAB         │ Tooltip      │ Context Menu │ Keyboard     │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Display Components

```
┌─────────────────────────────────────────────────────────────────┐
│ DATA DISPLAY                                                     │
├─────────────────────────────────────────────────────────────────┤
│ Table         │ Data Grid    │ List View   │ Card Grid    │
│ Stat Card     │ Progress     │ Timeline    │ Avatar       │
│ Badge         │ Tag/Chip     │ Tooltip     │ Empty State  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ TASK VIEWS                                                       │
├─────────────────────────────────────────────────────────────────┤
│ Calendar Bar   │ Calendar Month │ Calendar Week │ Calendar List │
│ Kanban Board   │ List View      │ Grid View    │ Table View   │
│ Gantt Chart    │ Heatmap View   │ Mobile Views │ View Switcher │
└─────────────────────────────────────────────────────────────────┘
```

For complete task view specifications, see [TASK-VIEWS.md](./TASK-VIEWS.md)
For complete table specifications, see [TABLE-DESIGNS.md](./TABLE-DESIGNS.md)
For complete tree table specifications, see [TREE-TABLE.md](./TREE-TABLE.md)
For complete card view specifications, see [CARD-VIEWS.md](./CARD-VIEWS.md)
For complete flow to image/video specifications, see [FLOW-IMAGE-VIDEO.md](./FLOW-IMAGE-VIDEO.md)

```tsx
// Quick reference: View Switcher
const ViewSwitcher = ({ value, onChange }) => (
  <div className="inline-flex bg-gray-100 rounded-xl p-1">
    {views.map(view => (
      <button
        key={view.id}
        onClick={() => onChange(view.id)}
        className={`px-3 py-1.5 rounded-lg text-sm ${value === view.id ? 'bg-white' : ''}`}
      >
        <view.icon className="w-4 h-4" />
      </button>
    ))}
  </div>
)
```

### 1.3 Feedback & Notice

```
┌─────────────────────────────────────────────────────────────────┐
│ FEEDBACK & NOTICE                                                │
├─────────────────────────────────────────────────────────────────┤
│ Alert         │ Toast/Notify │ Modal       │ Drawer        │
│ Side Sheet   │ Banner       │ Callout     │ Inline Msg   │
│ Status Bar   │ Loading      │ Skeleton    │ Progress     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Icon System

### 2.1 Icon Library (Pick ONE)

| Library | Best For | Import |
|---------|----------|--------|
| **Phosphor Icons** | Modern, consistent stroke | `@phosphor-icons/react` |
| **Hugeicons** | Unique, modern | `hugeicons-react` |
| **Tabler Icons** | Dashboard, admin | `@tabler/icons-react` |
| **Lucide** | Simple, clean | `lucide-react` |
| **Radix** | Shadcn/ui compatible | `@radix-ui/react-icons` |

### 2.2 Icon Rules

```tsx
// ❌ NEVER: Mix icon libraries
import { Check } from 'lucide-react'
import { Edit } from '@tabler/icons-react'  // WRONG

// ✅ ALWAYS: Pick ONE library
import { Check, Edit, Trash, Plus } from '@phosphor-icons/react'

// ❌ NEVER: Different stroke widths
<Icon size={16} strokeWidth={1} />
<Icon size={16} strokeWidth={2} />  // WRONG

// ✅ ALWAYS: Consistent stroke globally
// Set in tailwind.config.js or CSS variables
```

### 2.3 Icon Sizing Scale

```css
/* Icon sizes match text sizes */
--icon-xs: 12px;   /* xs text */
--icon-sm: 14px;   /* sm text */
--icon-md: 16px;   /* base text, default */
--icon-lg: 20px;   /* lg text */
--icon-xl: 24px;   /* xl text */
--icon-2xl: 32px; /* 2xl text */

/* Consistent stroke */
--icon-stroke: 1.5;
```

### 2.4 Icon Color Mapping

```tsx
// Match icon color to text color
<Text size="sm" color="muted">
  <Icon name="info" />  {/* Same color as text */}
</Text>

// Status icons use status colors
<Icon name="check" color="green" />   {/* Success */}
<Icon name="warning" color="amber" />  {/* Warning */}
<Icon name="error" color="red" />      {/* Error */}
<Icon name="info" color="blue" />     {/* Info */}
```

---

## 3. Color System

### 3.1 Dashboard Color Palette

```css
/* Neutrals - Primary grays */
--gray-50: #f9fafb;
--gray-100: #f3f4f6;
--gray-200: #e5e7eb;
--gray-300: #d1d5db;
--gray-400: #9ca3af;
--gray-500: #6b7280;
--gray-600: #4b5563;
--gray-700: #374151;
--gray-800: #1f2937;
--gray-900: #111827;

/* Semantic Colors - Dashboard */
--primary-50: #eff6ff;
--primary-100: #dbeafe;
--primary-500: #3b82f6;  /* Default blue */
--primary-600: #2563eb;
--primary-700: #1d4ed8;

--success-50: #f0fdf4;
--success-500: #22c55e;
--success-600: #16a34a;

--warning-50: #fffbeb;
--warning-500: #f59e0b;
--warning-600: #d97706;

--error-50: #fef2f2;
--error-500: #ef4444;
--error-600: #dc2626;

--info-50: #f0f9ff;
--info-500: #0ea5e9;
--info-600: #0284c7;
```

### 3.2 Surface Colors

```css
/* Card surfaces */
--card: #ffffff;
--card-hover: #f9fafb;
--card-border: #e5e7eb;

/* Dashboard backgrounds */
--sidebar: #1f2937;
--sidebar-hover: #374151;
--sidebar-active: #3b82f6;

/* Input surfaces */
--input-bg: #ffffff;
--input-border: #d1d5db;
--input-focus: #3b82f6;
--input-disabled: #f3f4f6;
```

### 3.3 Status Colors (Semantic)

```tsx
// Use these consistently across ALL status indicators
const statusColors = {
  success: { bg: '#f0fdf4', border: '#22c55e', text: '#16a34a' },
  warning: { bg: '#fffbeb', border: '#f59e0b', text: '#d97706' },
  error:   { bg: '#fef2f2', border: '#ef4444', text: '#dc2626' },
  info:    { bg: '#f0f9ff', border: '#0ea5e9', text: '#0284c7' },
  neutral: { bg: '#f3f4f6', border: '#6b7280', text: '#374151' },
}

// NEVER use these generic colors:
// ❌ 'purple', 'pink', 'indigo' for status
// ❌ Gradient backgrounds
// ❌ Multiple accent colors on same page
```

---

## 4. Component Specifications

### 4.1 Text Input

```tsx
// ✅ STANDARD INPUT SPECIFICATION
const Input = ({ label, error, hint, ...props }) => (
  <div className="space-y-1.5">
    {/* Label - always above */}
    {label && (
      <label className="text-sm font-medium text-gray-700">
        {label}
        {required && <span className="text-red-500 ml-1">*</span>}
      </label>
    )}
    
    {/* Input */}
    <input
      className={cn(
        "w-full h-10 px-3 rounded-lg border text-sm",
        "bg-white border-gray-300",
        "placeholder:text-gray-400",
        "focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500",
        "disabled:bg-gray-100 disabled:cursor-not-allowed",
        error && "border-red-500 focus:ring-red-500"
      )}
      {...props}
    />
    
    {/* Error message - below */}
    {error && (
      <p className="text-sm text-red-600">{error}</p>
    )}
    
    {/* Hint - below, muted */}
    {hint && !error && (
      <p className="text-sm text-gray-500">{hint}</p>
    )}
  </div>
)
```

### 4.2 Select/Dropdown

```tsx
// ✅ SELECT SPECIFICATION
const Select = ({ label, options, placeholder, ...props }) => (
  <div className="space-y-1.5">
    {label && (
      <label className="text-sm font-medium text-gray-700">
        {label}
      </label>
    )}
    
    <div className="relative">
      <select
        className={cn(
          "w-full h-10 pl-3 pr-10 rounded-lg border text-sm appearance-none",
          "bg-white border-gray-300",
          "focus:outline-none focus:ring-2 focus:ring-primary-500",
          "disabled:bg-gray-100"
        )}
        {...props}
      >
        {placeholder && (
          <option value="" disabled className="text-gray-400">
            {placeholder}
          </option>
        )}
        {options.map(opt => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>
      
      {/* Chevron icon - right aligned */}
      <ChevronDownIcon 
        className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 pointer-events-none" 
      />
    </div>
  </div>
)
```

### 4.3 Date Picker

```tsx
// ✅ DATE PICKER SPECIFICATION
const DatePicker = ({ label, value, onChange, ...props }) => (
  <div className="space-y-1.5">
    {label && (
      <label className="text-sm font-medium text-gray-700">
        {label}
      </label>
    )}
    
    <Popover>
      <Popover.Trigger asChild>
        <button
          type="button"
          className={cn(
            "w-full h-10 px-3 rounded-lg border text-sm text-left",
            "bg-white border-gray-300",
            "focus:outline-none focus:ring-2 focus:ring-primary-500",
            "flex items-center justify-between",
            !value && "text-gray-400"
          )}
        >
          <span>{value ? format(value, 'PP') : 'Select date'}</span>
          <CalendarIcon className="w-4 h-4 text-gray-400" />
        </button>
      </Popover.Trigger>
      
      <Popover.Content className="w-auto p-3 bg-white rounded-xl shadow-lg border">
        {/* Calendar grid */}
        <Calendar
          mode="single"
          selected={value}
          onSelect={onChange}
          className="rounded-lg"
        />
      </Popover.Content>
    </Popover>
  </div>
)
```

### 4.4 Button Variants

```tsx
// ✅ BUTTON SPECIFICATION
const Button = ({ variant = 'primary', size = 'md', ...props }) => {
  const variants = {
    primary: "bg-primary-600 text-white hover:bg-primary-700",
    secondary: "bg-gray-100 text-gray-900 hover:bg-gray-200",
    outline: "border border-gray-300 bg-white hover:bg-gray-50",
    ghost: "hover:bg-gray-100 text-gray-700",
    destructive: "bg-red-600 text-white hover:bg-red-700",
    link: "text-primary-600 hover:underline p-0 h-auto",
  }
  
  const sizes = {
    sm: "h-8 px-3 text-xs gap-1.5",
    md: "h-10 px-4 text-sm gap-2",
    lg: "h-12 px-6 text-base gap-2.5",
    icon: "h-10 w-10",
  }
  
  return (
    <button
      className={cn(
        "inline-flex items-center justify-center rounded-lg font-medium",
        "transition-colors duration-150",
        "focus:outline-none focus:ring-2 focus:ring-offset-2",
        "disabled:opacity-50 disabled:cursor-not-allowed",
        variants[variant],
        sizes[size]
      )}
      {...props}
    />
  )
}

// Usage
<Button variant="primary" size="md">
  <PlusIcon className="w-4 h-4" />
  Add New
</Button>

<Button variant="ghost" size="icon">
  <SettingsIcon className="w-4 h-4" />
</Button>
```

### 4.5 Badge/Tag

```tsx
// ✅ BADGE SPECIFICATION
const Badge = ({ variant = 'default', children, ...props }) => {
  const variants = {
    default: "bg-gray-100 text-gray-700 border-gray-200",
    primary: "bg-primary-100 text-primary-700 border-primary-200",
    success: "bg-green-100 text-green-700 border-green-200",
    warning: "bg-amber-100 text-amber-700 border-amber-200",
    error: "bg-red-100 text-red-700 border-red-200",
    info: "bg-blue-100 text-blue-700 border-blue-200",
  }
  
  return (
    <span
      className={cn(
        "inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium border",
        variants[variant]
      )}
      {...props}
    >
      {children}
    </span>
  )
}

// Usage examples
<Badge variant="success">Active</Badge>
<Badge variant="warning">Pending</Badge>
<Badge variant="error">Failed</Badge>
```

### 4.6 Alert/Notice

```tsx
// ✅ ALERT SPECIFICATION
const Alert = ({ variant = 'info', title, children, ...props }) => {
  const variants = {
    info: {
      bg: 'bg-blue-50 border-blue-200',
      icon: <InfoIcon className="w-5 h-5 text-blue-500" />,
      title: 'text-blue-800',
      body: 'text-blue-700',
    },
    success: {
      bg: 'bg-green-50 border-green-200',
      icon: <CheckIcon className="w-5 h-5 text-green-500" />,
      title: 'text-green-800',
      body: 'text-green-700',
    },
    warning: {
      bg: 'bg-amber-50 border-amber-200',
      icon: <WarningIcon className="w-5 h-5 text-amber-500" />,
      title: 'text-amber-800',
      body: 'text-amber-700',
    },
    error: {
      bg: 'bg-red-50 border-red-200',
      icon: <ErrorIcon className="w-5 h-5 text-red-500" />,
      title: 'text-red-800',
      body: 'text-red-700',
    },
  }
  
  return (
    <div
      className={cn(
        "p-4 rounded-lg border flex gap-3",
        variants[variant].bg
      )}
      {...props}
    >
      <div className="flex-shrink-0 mt-0.5">
        {variants[variant].icon}
      </div>
      <div className="flex-1 min-w-0">
        {title && (
          <h4 className={cn("font-medium text-sm", variants[variant].title)}>
            {title}
          </h4>
        )}
        <div className={cn("text-sm mt-1", variants[variant].body)}>
          {children}
        </div>
      </div>
    </div>
  )
}
```

---

## 5. Typography Scale

### 5.1 Text Sizes

```css
/* Dashboard Typography */
--text-xs: 0.75rem;    /* 12px - Badges, captions */
--text-sm: 0.875rem;   /* 14px - Table text, secondary */
--text-base: 1rem;      /* 16px - Body text */
--text-lg: 1.125rem;    /* 18px - Subheadings */
--text-xl: 1.25rem;     /* 20px - Section titles */
--text-2xl: 1.5rem;     /* 24px - Page titles */
--text-3xl: 1.875rem;   /* 30px - Dashboard headers */
```

### 5.2 Font Weights

```css
/* Dashboard Font Weights */
--font-normal: 400;
--font-medium: 500;    /* Labels, navigation */
--font-semibold: 600;   /* Headings, titles */
--font-bold: 700;       /* Stats, numbers */

/* Usage */
.stat-value { font-weight: 700; font-size: 2xl; }
.card-title { font-weight: 600; font-size: lg; }
.table-header { font-weight: 500; font-size: sm; }
.body-text { font-weight: 400; font-size: base; }
```

---

## 6. Spacing System

### 6.1 Dashboard Spacing

```css
/* 4px base grid */
--space-0: 0;
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-5: 1.25rem;   /* 20px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-10: 2.5rem;   /* 40px */
--space-12: 3rem;     /* 48px */
```

### 6.2 Component Spacing

```css
/* Form spacing */
--input-height: 2.5rem;     /* 40px */
--input-padding-x: 0.75rem;  /* 12px */
--input-gap: 0.5rem;        /* 8px - between label and input */
--form-gap: 1rem;           /* 16px - between form groups */

/* Card spacing */
--card-padding: 1.5rem;     /* 24px */
--card-gap: 1rem;           /* 16px - between cards */
--card-radius: 0.75rem;     /* 12px */

/* Table spacing */
--cell-padding: 0.75rem;    /* 12px */
--row-gap: 0;               /* Table rows are tight */
```

---

## 7. Dashboard Layout

### 7.1 Grid System

```tsx
// Dashboard grid: 12 columns, 24px gap
const DashboardGrid = ({ children }) => (
  <div className="grid grid-cols-12 gap-6">
    {children}
  </div>
)

// Common spans:
// Full width: col-span-12
// Two columns: col-span-6
// Three columns: col-span-4
// Sidebar + content: col-span-3 + col-span-9
// Stats cards: col-span-3 (4 cards on desktop)
```

### 7.2 Card Specifications

```tsx
// ✅ DASHBOARD CARD SPECIFICATION
const Card = ({ title, action, children, className }) => (
  <div className={cn(
    "bg-white rounded-xl border border-gray-200",
    "p-6",  // 24px padding
    className
  )}>
    {/* Header */}
    <div className="flex items-center justify-between mb-4">
      <h3 className="text-lg font-semibold text-gray-900">
        {title}
      </h3>
      {action && (
        <Button variant="ghost" size="sm">
          {action}
        </Button>
      )}
    </div>
    
    {/* Content */}
    {children}
  </div>
)

// ✅ STAT CARD SPECIFICATION
const StatCard = ({ label, value, trend, icon }) => (
  <Card>
    <div className="flex items-start justify-between">
      <div>
        <p className="text-sm text-gray-500 mb-1">{label}</p>
        <p className="text-3xl font-bold text-gray-900">{value}</p>
        {trend && (
          <p className={cn(
            "text-sm mt-2 flex items-center gap-1",
            trend.positive ? "text-green-600" : "text-red-600"
          )}>
            {trend.positive ? <TrendUpIcon /> : <TrendDownIcon />}
            {trend.value}
          </p>
        )}
      </div>
      {icon && (
        <div className="p-3 bg-gray-50 rounded-lg">
          {icon}
        </div>
      )}
    </div>
  </Card>
)
```

### 7.3 Table Specifications

```tsx
// ✅ DATA TABLE SPECIFICATION
const DataTable = ({ columns, data, onRowClick }) => (
  <div className="overflow-x-auto rounded-lg border">
    <table className="w-full">
      {/* Header */}
      <thead className="bg-gray-50 border-b border-gray-200">
        <tr>
          {columns.map(col => (
            <th
              key={col.key}
              className={cn(
                "px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                col.align === 'right' && "text-right",
                col.align === 'center' && "text-center"
              )}
            >
              {col.label}
            </th>
          ))}
        </tr>
      </thead>
      
      {/* Body */}
      <tbody className="bg-white divide-y divide-gray-200">
        {data.map((row, i) => (
          <tr 
            key={i}
            onClick={() => onRowClick?.(row)}
            className={cn(
              "hover:bg-gray-50 transition-colors",
              onRowClick && "cursor-pointer"
            )}
          >
            {columns.map(col => (
              <td
                key={col.key}
                className={cn(
                  "px-4 py-3 text-sm text-gray-700",
                  col.align === 'right' && "text-right",
                  col.align === 'center' && "text-center"
                )}
              >
                {col.render ? col.render(row[col.key], row) : row[col.key]}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  </div>
)
```

---

## 8. Responsive Breakpoints

```css
/* Dashboard breakpoints */
--breakpoint-sm: 640px;   /* Mobile landscape */
--breakpoint-md: 768px;   /* Tablet */
--breakpoint-lg: 1024px;  /* Desktop */
--breakpoint-xl: 1280px;  /* Large desktop */
--breakpoint-2xl: 1536px; /* Extra large */

/* Common responsive patterns */
.grid-cols-1           /* Mobile */
.md\:grid-cols-2        /* Tablet */
.lg\:grid-cols-4        /* Desktop */

/* Sidebar behavior */
.sidebar-collapsed      /* Mobile: hidden */
.md\:sidebar-open        /* Tablet: visible */
```

---

## 9. Checklist - Dashboard Quality

### Pre-Implementation
- [ ] Icon library selected (one family only)
- [ ] Color palette defined (max 2 accent colors)
- [ ] Typography scale defined
- [ ] Spacing system defined (4px grid)

### Component Audit
- [ ] All inputs have labels above
- [ ] Error messages below inputs
- [ ] Buttons have consistent sizing (sm/md/lg)
- [ ] Icons match text color
- [ ] Badges use semantic colors
- [ ] Alerts use semantic colors
- [ ] Hover states on all interactive elements
- [ ] Focus states visible (not removed)
- [ ] Disabled states styled
- [ ] Loading states implemented

### Layout Audit
- [ ] Consistent card padding (24px)
- [ ] Consistent gap between cards (16-24px)
- [ ] Table rows have hover state
- [ ] Mobile responsive (stack on small)
- [ ] No horizontal scroll on mobile

### Anti-Slop Check
- [ ] No gradient backgrounds
- [ ] No purple/rainbow accents
- [ ] No glassmorphism
- [ ] No floating elements
- [ ] No excessive shadows
- [ ] No centered everything
- [ ] No generic names ("John Doe")
- [ ] No filler text ("Lorem ipsum")

---

## 10. Component Library Reference

### Tailwind + shadcn/ui
Best for: Custom dashboard with full control
- Install: `npx shadcn@latest init`
- Components: `npx shadcn@latest add button input select card table badge alert`

### Radix UI + Tailwind
Best for: Headless, accessible components
- Install: Individual packages from `@radix-ui/react-*`
- Theme with CSS variables

### Headless UI
Best for: Vue/React with Tailwind
- Install: `@headlessui/react` or `@headlessui/vue`

### Chakra UI
Best for: Fast prototyping, React
- Install: `@chakra-ui/react`
- Theme with `extendTheme()`

### Mantine
Best for: React with rich features
- Install: `@mantine/core`
- Components: 100+ included

---

## 11. Integration with Frontend Taste

This skill complements `frontend-taste` for dashboard/admin UI:

```
frontend-taste → Landing pages, marketing
dashboard-ui → Admin panels, data-heavy interfaces
hallmark → Anti-slop design validation
```

Use `hallmark` gates to validate:
- Typography Gates (10 rules)
- Color Gates (10 rules)  
- Component Gates (10 rules)
