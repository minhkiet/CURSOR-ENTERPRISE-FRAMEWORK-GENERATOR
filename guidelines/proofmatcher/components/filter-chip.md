# Filter Chip Component

> Pill-shaped button cho marketplace category filter. Optional count suffix. Nhiều chips có thể active đồng thời (multi-select) hoặc một chip tại một thời điểm (single-select).

## 1. Mục đích

Filter templates theo category (SaaS, Agency, Health, Education...), style (Modern, Minimal, Editorial), framework (React, Vue, Svelte), price tier. Mỗi chip là một quyết định nhỏ. phải đọc được trong 0.2s.

## 2. Hệ thống icon

| Vai trò | Icon Phosphor | Kích thước |
|---|---|---|
| Category icons | `Browser` (SaaS), `Briefcase` (Agency), `Heartbeat` (Health), `GraduationCap` (Education), `AirplaneTilt` (Travel), `ForkKnife` (Restaurant), `House` (Real Estate), `Palette` (Design), `Code` (Developer) | 13px |
| Framework icons | `Atom` (React), `Cube` (Vue), `Stack` (Svelte), `Lightning` (Solid), `Code` (Vanilla) | 13px |
| Style | `Sparkle` (Modern), `Circle` (Minimal), `Newspaper` (Editorial), `Cube` (Geometric) | 13px |
| Clear all | `XCircle` (fill) | 14px |
| Active indicator | `Check` (bold) | 12px |
| Disabled (no items) | `Prohibit` | 11px, tertiary |
| More options | `DotsThreeVertical` | 14px |

## 3. Hình ảnh và minh họa

Filter chip không dùng ảnh. Tuy nhiên **category header banner** trên marketplace có thể hiển thị:

- Banner ngang 1600×160px với pattern họa tiết mỗi category. Lấy từ `https://picsum.photos/seed/{category}-pattern/1600/160`.
- Icon category lớn 64×64px đặt giữa banner.

Banner hiển thị khi filter chỉ còn 1 category active. Khi "All" được chọn, banner ẩn.

## 4. Cấu trúc

```
┌─────────────────────┐
│  [icon?] Label [count]│
└─────────────────────┘
```

- Container: pill, padding `space.2 space.4` (8/12).
- Label: `font.size.md` (12px, 500), uppercase, `letter-spacing: 0.06em`.
- Count suffix: optional, phân cách `space.2` (8px) gap, `font.size.sm` (11px) `color.text.tertiary`, `tabular-nums`.

## 5. Biến thể

| Variant | Selection mode | Cách dùng |
|---|---|---|
| `single-select` | một chip active tại một thời điểm | Filter theo primary category |
| `multi-select` | nhiều chips active | Refine theo secondary attributes |
| `clear-all` | standalone | Reset all filters, visible khi có filter active |

## 6. Sizes

| Size | Padding (y/x) | Font size | Height |
|---|---|---|---|
| `compact` | `space.1` / `space.3` (4/10) | `font.size.sm` (11px) | 28px |
| `default` | `space.2` / `space.4` (8/12) | `font.size.md` (12px) | 32px |
| `large` | `space.3` / `space.5` (10/14) | `font.size.lg` (13px) | 36px (hero filters) |

## 7. Trạng thái

| Trạng thái | Background | Text | Border | Khác |
|---|---|---|---|---|
| `default` | `color.surface.raised` | `color.text.secondary` | 1px `rgba(255,255,255,0.08)` |. |
| `hover` | `color.surface.strong` | `color.text.primary` | 1px `color.border.default` | transition 150ms |
| `focus-visible` | unchanged | unchanged | 2px outline `color.border.strong`, 2px offset | ring bắt buộc |
| `active` (selected) | `color.text.primary` | `color.surface.base` | 1px `color.text.primary` | `aria-pressed="true"`, font-weight 600, `Check` icon |
| `active-hover` | `color.text.primary` + 8% darken | `color.surface.base` | 1px `color.text.primary` | combined selected + hover |
| `disabled` | `color.surface.raised` | `color.text.tertiary` | 1px `rgba(255,255,255,0.04)` | `cursor: not-allowed`, opacity 0.6 |

## 8. Selection model

### Single-select (một active tại một thời điểm)

- Dùng `<button role="radio" aria-checked="...">` bên trong `<div role="radiogroup" aria-label="Filter by category">`.
- Đúng một chip có `aria-checked="true"` tại bất kỳ thời điểm nào (ngoại trừ "All" luôn present và selected khi không có chip nào khác).
- Arrow keys di chuyển selection giữa chips.
- Space/Enter kích hoạt chip focused.

### Multi-select (nhiều active)

- Dùng `<button aria-pressed="true|false">`.
- Không giới hạn count active.
- Toggle behavior: click thêm/xóa.

### Clear-all

- Visible chỉ khi ít nhất một filter đang active.
- Distinct style: ghost variant hoặc underlined link.
- Click xóa tất cả active filters trong group hiện tại.
- `aria-label="Clear all [group name] filters"`.

## 9. Count behavior

- Count dynamic, update khi templates thêm/xóa.
- Khi count = 0, chip disabled (`aria-disabled="true"`, opacity 0.6) + `Prohibit` icon.
- Count hiển thị với `font-variant-numeric: tabular-nums`.
- Count là decorative (`aria-hidden`) khi label đủ. Dùng `aria-label` nếu count có ý nghĩa (e.g. "All templates" + 247).

## 10. Filter group behavior

- Nhiều filter groups (Category, Style, Price) hoạt động độc lập.
- Filter results = intersection của tất cả groups.
- Empty result → hiển thị empty state (xem `card.md` § Empty state).

## 11. Sticky filter bar (optional)

- Ở top marketplace grid, sticky dưới top nav.
- Background `color.surface.base` + `backdrop-filter: blur(12px)` khi scrolled.
- 1px bottom border `rgba(255,255,255,0.08)`.

## 12. Responsive

- <768px: filter chips horizontal scroll, không wrap. Snap to left edge on scroll.
- ≥768px: chips wrap thành multiple rows.
- Container padding `space.5` (16px) trên mobile, `space.6` (20px) ở desktop.

## 13. Edge cases

- **All categories disabled**: ẩn filter bar, hiển thị "No categories available" message.
- **Single category**: ẩn filter bar hoàn toàn (không cần filtering).
- **Long category name**: truncate ở 120px với ellipsis.
- **Count overflow**: cap ở "99+".
- **Empty state**: "No templates match" với "Clear all filters" button.
- **Active filters persistence**: sync tới URL query params cho shareable links. `?category=saas&style=premium`.

## 14. Accessibility

- Group có `role="radiogroup"` (single) hoặc `role="group"` (multi) với `aria-label`.
- Mỗi chip có ARIA role và state phù hợp.
- Bàn phím: Tab vào group, Arrow keys trong group (single-select only), Space/Enter để activate.
- Focus-visible bắt buộc.
- Disabled chips giữ trong tab order nhưng announce là unavailable.
- Color contrast: selected state `color.surface.base` trên `color.text.primary` measures 21:1 (passes AAA). Default `color.text.secondary` trên `color.surface.raised` measures 6.8:1 (passes AA).
- Touch target ≥44×44px (extend padding nếu visual size nhỏ hơn).

## 15. QA acceptance criteria

```
[ ] Group có aria-label
[ ] Single-select dùng role="radio" + aria-checked
[ ] Multi-select dùng aria-pressed
[ ] Arrow key navigation hoạt động trong single-select
[ ] Space/Enter activate chip
[ ] Disabled chip có aria-disabled và opacity
[ ] Count updates dynamic với dataset changes
[ ] Count 0 disables chip
[ ] Clear-all visible chỉ khi filters active
[ ] URL sync với active filters
[ ] Empty state hiển thị khi không có matches
[ ] Sticky filter bar với scrolled background
[ ] Horizontal scroll trên mobile, wrap trên desktop
[ ] Touch target ≥44×44px
[ ] axe-core: 0 violations
[ ] Không em-dash trong label
```

## 16. Code reference

```tsx
{/* Single-select category filter với icon */}
<div role="radiogroup" aria-label="Filter by category" class="flex flex-wrap gap-2">
  {categories.map(category => (
    <button
      key={category.id}
      role="radio"
      aria-checked={activeCategory === category.id}
      onClick={() => setActiveCategory(category.id)}
      class={cn(
        'inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full font-mono text-[12px] uppercase tracking-[0.06em] transition-all duration-150 focus-visible:outline-2 focus-visible:outline-[#fafafa] focus-visible:outline-offset-2',
        activeCategory === category.id
          ? 'bg-white text-black border border-white font-semibold'
          : 'bg-[#050505] text-[#a1a1aa] border border-[rgba(255,255,255,0.08)] hover:bg-[#0d0d0d] hover:text-white hover:border-[#e5e7eb]',
        category.count === 0 && 'opacity-50 cursor-not-allowed'
      )}
      aria-disabled={category.count === 0}
    >
      <span aria-hidden="true">{categoryIcons[category.id]}</span>
      <span>{category.label}</span>
      <span class="font-mono text-[11px] tabular-nums opacity-70" aria-hidden="true">{category.count}</span>
      {activeCategory === category.id && (
        <Phosphor.Check size={11} weight="bold" aria-hidden="true" />
      )}
    </button>
  ))}
</div>

{/* Multi-select framework filter với framework icons */}
<div role="group" aria-label="Filter by framework" class="flex flex-wrap gap-2">
  {frameworks.map(framework => (
    <button
      key={framework.id}
      aria-pressed={activeFrameworks.has(framework.id)}
      onClick={() => toggleFramework(framework.id)}
      class={cn(
        'inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full font-mono text-[12px] uppercase tracking-[0.06em] transition-all duration-150 focus-visible:outline-2 focus-visible:outline-[#fafafa] focus-visible:outline-offset-2',
        activeFrameworks.has(framework.id)
          ? 'bg-white text-black border border-white font-semibold'
          : 'bg-[#050505] text-[#a1a1aa] border border-[rgba(255,255,255,0.08)] hover:bg-[#0d0d0d] hover:text-white hover:border-[#e5e7eb]'
      )}
    >
      <span aria-hidden="true">{frameworkIcons[framework.id]}</span>
      <span>{framework.label}</span>
    </button>
  ))}
</div>

{/* Clear-all button */}
{hasActiveFilters && (
  <button
    type="button"
    onClick={clearAllFilters}
    aria-label="Clear all category filters"
    class="inline-flex items-center gap-1.5 px-3 py-1.5 text-[#a1a1aa] hover:text-white font-mono text-[12px] uppercase tracking-[0.06em] underline-offset-4 hover:underline transition-colors duration-150"
  >
    <Phosphor.XCircle size={13} weight="fill" aria-hidden="true" />
    Clear all
  </button>
)}

{/* Disabled chip khi count = 0 */}
<button
  type="button"
  role="radio"
  aria-checked={false}
  aria-disabled="true"
  disabled
  class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full font-mono text-[12px] uppercase tracking-[0.06em] opacity-50 cursor-not-allowed bg-[#050505] text-[#737373] border border-[rgba(255,255,255,0.04)]"
>
  <Phosphor.Prohibit size={11} weight="bold" aria-hidden="true" />
  <span>Empty category</span>
  <span class="font-mono text-[11px] tabular-nums" aria-hidden="true">0</span>
</button>
```