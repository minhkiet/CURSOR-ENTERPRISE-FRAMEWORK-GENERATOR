# Badge Component

> Inline status, count, hoặc category indicator. Pill nhỏ, non-interactive mặc định. Trong dark theme, badge phải có độ tương phản vừa đủ để đọc nhanh trong 0.3s nhưng không phá nhịp thị giác.

## 1. Mục đích

Đánh dấu trạng thái (new, featured, deprecated), đếm (12 items), category tag. Mọi badge đọc như một tín hiệu nhỏ giữa dòng chảy nội dung.

## 2. Hệ thống icon

Một số badge có icon dẫn đầu hoặc icon-only. Tất cả dùng **Phosphor Regular** (`@phosphor-icons/react`), `weight="bold"` cho badge status, `weight="regular"` cho icon-only.

| Vai trò | Icon Phosphor | Kích thước |
|---|---|---|
| Status "new" | `Sparkle` (fill) | 12px, mint `#34d399` |
| Status "featured" | `Star` (fill) | 12px, primary |
| Status "deprecated" | `Archive` | 12px, tertiary |
| Status "draft" | `PencilSimple` | 12px, tertiary |
| Status "error" | `WarningCircle` (fill) | 12px, đỏ nhạt `#fca5a5` |
| Status "warning" | `Warning` (fill) | 12px, vàng `#fbbf24` |
| Status "verified" | `SealCheck` (fill) | 12px, mint |
| Loading state | `CircleNotch` (spin) | 12px, tertiary |
| External link | `ArrowUpRight` | 12px |
| Code example | `Code` | 12px |
| Documentation | `BookOpen` | 12px |
| Free tier | `Gift` | 12px |

## 3. Hình ảnh và minh họa

Badge tiêu chuẩn không dùng ảnh. Tuy nhiên có thể thay status "verified" bằng **ảnh seal verified** 16×16px (Picsum): `https://picsum.photos/seed/verified-seal-vintage/64/64` với `grayscale(100%) + brightness(1.2)` cho phù hợp dark theme.

## 4. Cấu trúc

```
┌─────────────────┐
│  [icon?]  Label │
└─────────────────┘
```

| Slot | Bắt buộc | Ghi chú |
|---|---|---|
| Container | có | Pill hoặc rectangle, padding `space.1 space.3` (4/10) cho compact, `space.2 space.4` (8/12) cho default |
| Label | có | `font.size.sm` (11px) hoặc `font.size.md` (12px), uppercase, `letter-spacing: 0.06em` |
| Leading icon | không | 12×12px Phosphor |

## 5. Biến thể

| Variant | Background | Text | Border | Cách dùng |
|---|---|---|---|---|
| `default` | `color.surface.raised` | `color.text.secondary` | 1px `rgba(255,255,255,0.08)` | Category tags, generic status |
| `count` | `color.surface.raised` | `color.text.tertiary` | none | Count items ("12") |
| `status-new` | `color.surface.raised` | `#34d399` (mint) | 1px `rgba(52,211,153,0.4)` | Template mới thêm gần đây |
| `status-featured` | `color.surface.raised` | `color.text.primary` | 1px `color.border.strong` | Featured, đề xuất |
| `status-warning` | `color.surface.raised` | `#fbbf24` | 1px `rgba(251,191,36,0.4)` | Deprecated, draft |
| `status-error` | `color.surface.raised` | `#fca5a5` | 1px `#7f1d1d` | Failed, removed |
| `status-verified` | `color.surface.raised` | `#34d399` | 1px `rgba(52,211,153,0.4)` | Verified template |
| `interactive` | `color.surface.raised` | `color.text.primary` | 1px `color.border.default` | Filter chip (xem `filter-chip.md`) |

## 6. Sizes

| Size | Padding (y/x) | Font size | Cách dùng |
|---|---|---|---|
| `compact` | `space.1` / `space.3` (4/10) | `font.size.sm` (11px) | Inline tags |
| `default` | `space.2` / `space.4` (8/12) | `font.size.md` (12px) | Status indicators |
| `large` | `space.2` / `space.5` (8/14) | `font.size.lg` (13px) | Hero status, prominent badges |

## 7. Trạng thái (interactive variant only)

| Trạng thái | Background | Text | Border | Khác |
|---|---|---|---|---|
| `default` | `color.surface.raised` | `color.text.primary` | 1px `color.border.default` |. |
| `hover` | `color.surface.strong` | `color.text.primary` | 1px `color.border.strong` |. |
| `focus-visible` | unchanged | unchanged | 2px outline `color.border.strong`, 2px offset | ring bắt buộc |
| `active` (pressed) | `color.surface.strong` | `color.text.primary` | 1px `color.border.strong` | `scale(0.98)` |
| `disabled` | `color.surface.raised` | `color.text.tertiary` | 1px `rgba(255,255,255,0.04)` | `cursor: not-allowed` |

## 8. Non-interactive variant

- `<span>` element.
- Không focusable.
- Không có hover/focus state change.
- Dùng cho status indicators trên card.

## 9. Interactive variant

- `<button>` element.
- Tab-focusable.
- Dùng cho filter chips, removable tags.
- Cho removable tags: trailing `×` icon Phosphor (`X` weight="bold" 12px), click xóa item, `aria-label="Remove [tag name]"`.

## 10. Radius

| Variant | Radius |
|---|---|
| `default`, `count`, tất cả status | `radius.sm` (9999px, pill) |
| Code example, documentation | `radius.md` (6px) cho cảm giác code block |

## 11. Responsive

- Badges không đổi size qua các breakpoint.
- Badge label dài truncate ở 200px với ellipsis.

## 12. Edge cases

- **Empty label**: ẩn badge hoàn toàn (không render empty `<span>`).
- **Long label**: truncate. Tốt hơn nên dùng 2–3 từ max trong copy.
- **No count value**: ẩn count badge.
- **Negative count**: render 0, không bao giờ âm.
- **Pill overflow**: badge dài không được phép tràn container. Dùng ellipsis.

## 13. Accessibility

- Non-interactive: `aria-hidden="true"` nếu label trùng với adjacent text. Ngược lại expose bình thường.
- Interactive: `<button>` với descriptive `aria-label` nếu icon-only.
- Focus-visible bắt buộc cho interactive.
- Color contrast: variant text trên `color.surface.raised` phải đạt 4.5:1 (count badge `color.text.tertiary` trên `color.surface.raised` là 4.65:1, pass AA).
- Status color không phải tín hiệu duy nhất. pair với text hoặc icon.
- Touch target ≥44×44px cho interactive variant.

## 14. QA acceptance criteria

```
[ ] Padding matches size token
[ ] Border-radius đúng theo variant
[ ] Interactive variant focusable qua Tab
[ ] Non-interactive variant không focusable
[ ] Removable tag × button có aria-label
[ ] Empty badge không render
[ ] Status color pair với text hoặc icon (không màu đơn thuần)
[ ] Touch target ≥44×44px cho interactive variant
[ ] axe-core: 0 violations
[ ] Không em-dash (,) trong label
```

## 15. Code reference

```tsx
{/* Default category tag */}
<span class="inline-flex items-center gap-1.5 px-2.5 py-1 bg-[#050505] border border-[rgba(255,255,255,0.08)] rounded-full">
  <span class="font-mono text-[11px] uppercase tracking-[0.06em] text-[#a1a1aa]">SaaS</span>
</span>

{/* Status new với Sparkle icon */}
<span class="inline-flex items-center gap-1.5 px-2.5 py-1 bg-[#050505] border border-[rgba(52,211,153,0.4)] rounded-full">
  <Phosphor.Sparkle size={12} weight="fill" class="text-[#34d399]" aria-hidden="true" />
  <span class="font-mono text-[11px] uppercase tracking-[0.06em] text-[#34d399]">New</span>
</span>

{/* Status featured với Star */}
<span class="inline-flex items-center gap-1.5 px-2.5 py-1 bg-[#050505] border border-[#fafafa] rounded-full">
  <Phosphor.Star size={12} weight="fill" class="text-white" aria-hidden="true" />
  <span class="font-mono text-[11px] uppercase tracking-[0.06em] text-white">Featured</span>
</span>

{/* Status deprecated với Archive */}
<span class="inline-flex items-center gap-1.5 px-2.5 py-1 bg-[#050505] border border-[rgba(251,191,36,0.4)] rounded-full">
  <Phosphor.Archive size={12} weight="bold" class="text-[#fbbf24]" aria-hidden="true" />
  <span class="font-mono text-[11px] uppercase tracking-[0.06em] text-[#fbbf24]">Deprecated</span>
</span>

{/* Status verified với seal ảnh */}
<span class="inline-flex items-center gap-1.5 px-2.5 py-1 bg-[#050505] border border-[rgba(52,211,153,0.4)] rounded-full">
  <img src="https://picsum.photos/seed/verified-seal-vintage/64/64" alt="" aria-hidden="true" class="w-3 h-3 rounded-full grayscale brightness-125" />
  <span class="font-mono text-[11px] uppercase tracking-[0.06em] text-[#34d399]">Verified</span>
</span>

{/* Count badge */}
<span aria-label="12 templates" class="inline-flex items-center px-2 py-0.5 bg-[#050505] rounded-full">
  <span class="font-mono text-[11px] tabular-nums text-[#737373]">12</span>
</span>

{/* Interactive filter-style badge (xem thêm filter-chip.md) */}
<button
  type="button"
  class="inline-flex items-center gap-1.5 px-3 py-1 bg-[#050505] border border-[#e5e7eb] text-white font-mono text-[12px] uppercase tracking-[0.06em] rounded-full hover:bg-[#0d0d0d] hover:border-[#fafafa] focus-visible:outline-2 focus-visible:outline-[#fafafa] focus-visible:outline-offset-2 transition-all duration-150"
  aria-pressed="false"
>
  React
  <Phosphor.X size={11} weight="bold" aria-hidden="true" />
</button>
```