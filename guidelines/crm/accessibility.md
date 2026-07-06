# CRM Platform. Accessibility (WCAG 2.2 AA + Keyboard-First)

> Northwind CRM là data-dense SaaS. Accessibility cực kỳ quan trọng cho productivity tools. Áp dụng cho cả marketing landing page và in-app cockpit.

## 1. Universal requirements

| Hạng mục | Tiêu chí | Test |
|---|---|---|
| Color contrast | Body text ≥ 4.5:1. UI components ≥ 3:1. Slate-900 trên white = 15.7:1 ✓ | axe-core |
| Keyboard | Tab + Enter + Arrow + Esc + shortcuts đầy đủ | Manual |
| Focus visible | Ring indigo 2px | Visible always |
| Touch target | ≥ 32x32px cho data-dense UI, ≥ 44px cho primary actions | DevTools |
| Alt text | Charts có text alternative. Avatar có alt text | HTML scan |
| Language | `<html lang="vi">` | HTML |
| Motion | Reduce-motion cho pulse / hover transitions | Toggle test |
| Money format | `$1,250` tabular-nums | Visible |
| Time format | Relative + absolute: "2h ago (15:30 5/7)" | Screen reader |

## 2. Keyboard shortcuts (in-app)

CRM phải keyboard-first. Tất cả shortcut phải có aria-keyshortcuts.

| Shortcut | Action | Context |
|---|---|---|
| `c` | Create new deal | Pipeline |
| `j` / `k` | Next / previous deal | Pipeline |
| `enter` | Open deal detail | Pipeline |
| `esc` | Close drawer / modal | Anywhere |
| `/` | Focus search | Anywhere |
| `g` then `p` | Go to Pipeline | Global |
| `g` then `c` | Go to Contacts | Global |
| `g` then `r` | Go to Reports | Global |
| `?` | Show shortcuts | Anywhere |

## 3. Component-specific

### 3.1 Pipeline kanban

- Columns là `<section>` với `aria-labelledby="stage-xxx"`
- Deal cards là `<article>` với title + owner + value + age
- Drag handle accessible: dùng `aria-roledescription="draggable"` + aria-describedby cho instructions
- Drop zones announce "Moved deal X from Stage A to Stage B" qua `aria-live="polite"`
- Total column value là `<output>` với aria-live update
- Empty state có icon + heading + CTA

### 3.2 Contact table

- `<table>` semantic với `<caption>` cho title
- `<th scope="col">` cho column headers, `aria-sort` cho sortable
- Sortable headers: button inside, keyboard accessible (`aria-sort`, `Enter` to sort)
- Row focus: full row clickable, announce row content khi focused
- Checkbox cho multi-select có label "Select [contact name]"
- Pagination có aria-label + jump-to-page input
- Bulk actions toolbar có aria-live update số items selected

### 3.3 Drawer

- Modal trap focus, restore on close
- `<dialog>` hoặc `role="dialog"` + `aria-modal="true"`
- `aria-labelledby` cho title
- `aria-describedby` cho description
- Escape closes
- Click outside closes
- Body scroll locked while open

### 3.4 Dashboard widget

- Charts có text alternative summary
- Sparklines có `aria-label="Revenue trend up 12% in 30 days"`
- KPI delta có icon + color + value + comparison context
- Live updating data có `aria-live="polite"` (không quá thường xuyên)

### 3.5 Pricing tier

- Tier name là heading level 3
- Price có aria-label "Giá 199.000₫ mỗi người dùng mỗi tháng"
- Feature list là `<ul>` semantic
- CTA là button accessible
- "Most popular" badge có aria-label "Tier được đề xuất"

### 3.6 Mega footer

- 6 columns semantic headings
- Hotline `tel:` accessible
- Social `aria-label` cụ thể

## 4. Data formatting accessibility

### 4.1 Numbers

- Currency `$1,250.00` hoặc `1.250.000₫` tabular-nums
- Phần trăm `12.5%` có sr-only context ("tăng trưởng")
- Large numbers `12,500,000` không aria-label thêm (screen reader đọc "twelve million five hundred thousand")

### 4.2 Dates

- Relative: "2 giờ trước"
- Absolute on hover: "15:30, 5/7/2026"
- Date inputs accessible

### 4.3 Status

- Status badge có icon + text + color, KHÔNG color-only
- "Active deal" + dot green + label
- "Stalled" + warning icon + label

## 5. Vietnamese language considerations

- "Hợp đồng", "Liên hệ", "Doanh nghiệp" đúng chuyên ngành
- Vietnamese có dấu đầy đủ
- Currency format `1.250.000₫`
- Date format `5/7/2026` (DD/MM/YYYY) hoặc `5 tháng 7, 2026`
- "Tỷ" cho 100 triệu VND+ phổ biến cho revenue

## 6. In-app keyboard navigation

### 6.1 Pipeline view

- `Tab` qua cards in column order
- `Enter` mở drawer
- `Space` toggle select
- `J`/`K` next/previous deal
- `Cmd/Ctrl + Enter` advance stage
- `Cmd/Ctrl + Backspace` archive

### 6.2 Contact list

- `Tab` qua rows
- `Enter` mở drawer
- `Cmd/Ctrl + A` select all visible
- `Cmd/Ctrl + D` duplicate
- `Cmd/Ctrl + Delete` archive

### 6.3 Drawer

- `Esc` close
- `Tab` qua fields
- `Cmd/Ctrl + S` save
- `Cmd/Ctrl + Enter` submit

## 7. Performance + A11y interplay

- Large data tables: virtualization với focus preservation
- Live search debounce 200ms, aria-busy state
- Real-time updates: aria-live polite, debounce 5s
- Charts: render SVG với text alternative (sr-only description)

## 8. Acceptance criteria

### 8.1 Testable

- [ ] axe-core: 0 violations
- [ ] Lighthouse accessibility: ≥ 95
- [ ] Manual keyboard: hoàn thành 1 deal flow không dùng chuột
- [ ] Screen reader (NVDA + Firefox): đọc được table + drawer state
- [ ] Color contrast: tất cả text passes WCAG AA
- [ ] Focus order: logical
- [ ] Skip link "Bỏ qua đến nội dung" hoạt động
- [ ] Keyboard shortcuts accessible via `aria-keyshortcuts`
- [ ] Drag-drop có keyboard alternative
- [ ] Charts có text alternative

### 8.2 Common violations to avoid

- ❌ Div soup thay vì semantic HTML
- ❌ Click handler trên `<div>` thay vì `<button>`
- ❌ Modal không trap focus
- ❌ Color-only state indication
- ❌ Table cho layout thay vì data
- ❌ Icon-only buttons không aria-label
- ❌ Skeleton loading accessible
- ❌ Real-time updates spam screen reader

## 9. Recommended test tools

- axe-core CLI + extension
- Lighthouse CI
- NVDA + Firefox (Windows)
- VoiceOver + Safari (macOS)
- Chrome DevTools Accessibility tab
- WAVE
- Pa11y CI

---

**Version**: 2026.1 · WCAG 2.2 AA + Keyboard-First