# Linear Design System (DESIGN.md)

> **Source Reference:** [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) — `linear.app` preset
> **Target:** High-fidelity, cinematic dark mode UI for B2B SaaS, developer tools, issue trackers, and productivity software.

---

## 1. Design Philosophy & Atmosphere

- **Theme:** Strict Dark Mode (Cinematic, obsidian-layered, zero pure white glare).
- **Core Aesthetic:** Precision engineering, restrained luxury, high information density without clutter, sharp focus states.
- **Lighting Model:** Backgrounds are deep obsidian (`#08090a`). Surfaces elevate through layered dark charcoals and subtle hairline borders (`1px solid rgba(255,255,255,0.08)`), rather than heavy drop shadows.
- **Accent Restraint:** Linear Lavender/Purple (`#5e6ad2`) is used with high intentionality for active states, primary CTAs, and focus rings—never splashed arbitrarily across cards or backgrounds.

---

## 2. Color System & Semantic Tokens

### Canvas & Surface Hierarchy
```css
--linear-canvas:          #08090a; /* Background chính toàn màn hình */
--linear-surface-1:       #0f1011; /* Panel/Card cấp 1 */
--linear-surface-2:       #141516; /* Hover card, dropdown, popover */
--linear-surface-3:       #1c1d1f; /* Modal, floating dialogs, active items */
--linear-surface-inset:   #050506; /* Code wells, input backgrounds */
```

### Borders & Dividers
```css
--linear-border-hairline: rgba(255, 255, 255, 0.08); /* Viền card, table rows */
--linear-border-subtle:   rgba(255, 255, 255, 0.12); /* Viền divider, header border */
--linear-border-focus:    rgba(94, 106, 210, 0.6);   /* Viền khi input focus */
--linear-border-hover:    rgba(255, 255, 255, 0.18); /* Hover state border */
```

### Text & Iconography Hierarchy
```css
--linear-text-primary:    #f7f8f8; /* Tiêu đề, primary body text */
--linear-text-secondary:  #8a8f98; /* Subtext, labels, metadata */
--linear-text-tertiary:   #62666d; /* Placeholders, timestamps, hints */
--linear-text-muted:      #43474d; /* Disabled text, subtle icon state */
```

### Brand Accent & Status Colors
```css
--linear-accent:          #5e6ad2; /* Signature Linear Lavender */
--linear-accent-hover:    #717de0; /* Hover state for primary buttons */
--linear-accent-active:   #4e5ac0; /* Active / Clicked state */
--linear-accent-subtle:   rgba(94, 106, 210, 0.15); /* Badge, subtle highlight */

--linear-status-success:  #27c281; /* Completed, online, connected */
--linear-status-warning:  #f0a04b; /* In progress, warning, pending */
--linear-status-danger:   #f25555; /* Blocked, error, cancelled */
--linear-status-info:     #5e6ad2; /* Informational notices */
```

---

## 3. Typography & Rhythm

### Font Stacks
- **UI / Sans-Serif:** `Inter, -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, sans-serif`
- **Code / Mono:** `"JetBrains Mono", "SF Mono", Menlo, Consolas, monospace`

### Scale & Tracking (Letter-Spacing)
| Level | Font Size | Line Height | Weight | Tracking | Cách dùng |
|:---|:---|:---|:---|:---|:---|
| **Display / H1** | 32px / 2rem | 1.2 | 600 (Semibold) | `-0.025em` | Hero titles, page headers |
| **Heading / H2** | 24px / 1.5rem | 1.25 | 600 (Semibold) | `-0.02em` | Section headers |
| **Heading / H3** | 18px / 1.125rem | 1.3 | 500 (Medium) | `-0.015em` | Card titles, group names |
| **Body Large** | 15px / 0.9375rem | 1.5 | 400 (Regular) | `-0.01em` | Lead paragraphs |
| **Body Regular** | 13px / 0.8125rem | 1.5 | 400 (Regular) | `0` | Dense data tables, list rows |
| **Caption / Meta**| 12px / 0.75rem | 1.4 | 400 / 500 | `+0.01em` | Timestamps, status pills |
| **Mono / Code** | 12px / 0.75rem | 1.4 | 500 | `0` | Commit hashes, hotkeys, IDs |

---

## 4. Component Patterns & Elevation

### Border Radius Hierarchy
- **`4px` - `6px` (`rounded-md`):** Small buttons, status badges, `<kbd>` keys, form inputs.
- **`8px` (`rounded-lg`):** Cards, dropdown menus, context menus, popovers.
- **`12px` (`rounded-xl`):** Heavy containers, modal dialogs, drawer panels.
- **`9999px` (`rounded-full`):** User avatars, status indicator dots, capsule pills.
- *(Lưu ý: Không dùng radius > 12px cho cards để giữ tính kỹ thuật, sắc nét).*

### Elevation & Shadows
```css
/* Hairline Card Shadow */
box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.08), 
            0 2px 4px rgba(0, 0, 0, 0.4);

/* Modal / Dropdown Floating Shadow */
box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.1), 
            0 8px 24px -4px rgba(0, 0, 0, 0.6),
            0 24px 48px -8px rgba(0, 0, 0, 0.8);

/* Glow Accent (Phía sau Hero hoặc Focus Ring) */
box-shadow: 0 0 0 2px rgba(94, 106, 210, 0.4),
            0 0 20px rgba(94, 106, 210, 0.2);
```

### Button Variants
1. **Primary Button:**
   - Background: `#5e6ad2`
   - Text: `#ffffff`, Font: 13px / 500 weight
   - Border: `1px solid rgba(255, 255, 255, 0.15)` (inner highlight)
   - Hover: Background `#717de0`, subtle glow
2. **Secondary / Subtle Button:**
   - Background: `rgba(255, 255, 255, 0.04)`
   - Text: `#f7f8f8`, Border: `1px solid rgba(255, 255, 255, 0.08)`
   - Hover: Background `rgba(255, 255, 255, 0.08)`, Border `rgba(255, 255, 255, 0.14)`
3. **Ghost Button:**
   - Background: `transparent`
   - Text: `#8a8f98`
   - Hover: Text `#f7f8f8`, Background `rgba(255, 255, 255, 0.05)`

### Keyboard Shortcuts (`<kbd>`)
```css
background: #191b1d;
border: 1px solid rgba(255, 255, 255, 0.1);
border-radius: 4px;
color: #8a8f98;
font-family: var(--font-mono);
font-size: 11px;
padding: 2px 5px;
box-shadow: inset 0 -1px 0 rgba(0, 0, 0, 0.4);
```

---

## 5. Tailwind CSS Configuration Reference

```ts
// tailwind.config.ts
export default {
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        linear: {
          canvas: '#08090a',
          surface: {
            1: '#0f1011',
            2: '#141516',
            3: '#1c1d1f',
            inset: '#050506',
          },
          border: {
            hairline: 'rgba(255, 255, 255, 0.08)',
            subtle: 'rgba(255, 255, 255, 0.12)',
            hover: 'rgba(255, 255, 255, 0.18)',
          },
          text: {
            primary: '#f7f8f8',
            secondary: '#8a8f98',
            tertiary: '#62666d',
            muted: '#43474d',
          },
          accent: {
            DEFAULT: '#5e6ad2',
            hover: '#717de0',
            subtle: 'rgba(94, 106, 210, 0.15)',
          },
        },
      },
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
        mono: ['JetBrains Mono', 'SF Mono', 'monospace'],
      },
    },
  },
};
```

---

## 6. Anti-Patterns & Slop Gates (Những điều TUYỆT ĐỐI TRÁNH)

- ❌ **Không dùng nền xám nhạt hoặc trắng thuần** trong theme Linear; mọi thứ phải bắt đầu từ `#08090a`.
- ❌ **Không lạm dụng bo tròn lớn (`rounded-2xl`, `rounded-3xl`)** cho card, container. Tối đa là `12px`.
- ❌ **Không dùng viền dày hoặc sặc sỡ:** Viền luôn là `1px` với opacity mảnh (`0.06 - 0.12`).
- ❌ **Không dùng màu tím bão hòa 100% làm background diện rộng:** Chỉ dùng `#5e6ad2` làm điểm nhấn (accent).
- ❌ **Không dùng drop shadow mờ màu xám:** Dùng shadow màu đen (`rgba(0,0,0,0.6 - 0.8)`) kết hợp hairline border.
