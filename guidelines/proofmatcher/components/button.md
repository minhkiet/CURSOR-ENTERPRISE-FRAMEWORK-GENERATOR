# Button Component

> Primary interactive control để trigger actions. Nút mặc định là component được dùng nhiều nhất trên site (mục tiêu 25+ mỗi page). Linear-style: tối giản, phản hồi xúc giác rõ ràng.

## 1. Mục đích

Trigger actions: subscribe, preview template, copy code, login, open modal. Mỗi nút có phản hồi xúc giác rõ ràng (lift -1px, scale 0.98 active), giữ UI đọc nhanh trong 0.3s.

## 2. Hệ thống icon

Tất cả dùng **Phosphor Regular** (`@phosphor-icons/react`), `weight="bold"` cho icon stroke thống nhất.

| Vai trò | Icon Phosphor | Kích thước theo size nút |
|---|---|---|
| Subscribe / Buy | `ShoppingBag` | 14/16/18/20px theo `compact/default/large` |
| Preview | `Eye` | tương tự |
| Get template | `DownloadSimple` | tương tự |
| Copy code | `Copy` | 14px cố định |
| Continue | `ArrowRight` | 14/16/18/20px |
| Back | `ArrowLeft` | tương tự |
| Close | `X` | 16px |
| Menu mobile | `List` | 18px |
| Loading | `CircleNotch` (spin) | 14px, tertiary |
| Success | `CheckCircle` (fill) | 14px, mint `#34d399` |
| Error | `WarningCircle` (fill) | 14px, đỏ nhạt |
| Save / Bookmark | `BookmarkSimple` | 14px |
| Share | `ShareNetwork` | 14px |
| External link | `ArrowUpRight` | 12px |
| Filter | `Funnel` | 14px |
| Search | `MagnifyingGlass` | 14px |
| Chevron (dropdown) | `CaretDown` | 12px |
| Plus (add) | `Plus` | 14px |

Quy tắc: một nút tối đa 1 icon-left và 1 icon-right. Icon-right không bao giờ đứng một mình.

## 3. Hình ảnh và minh họa

Nút thường không dùng ảnh. Một số case đặc biệt:

- **Nút "Get template"** cho template preview có thể đặt **thumbnail 24×24px** (bo vuông 4px) trước label. Lấy từ `https://picsum.photos/seed/template-thumb-1/48/48`.
- **Nút social** (GitHub, Twitter, Discord): dùng **logo Simple Icons** với màu invert cho dark theme: `https://cdn.simpleicons.org/github/ffffff`, `https://cdn.simpleicons.org/twitter/ffffff`, `https://cdn.simpleicons.org/discord/ffffff`.

Không dùng ảnh minh họa khác trên button. Button phải đọc nhanh trong 0.4 giây.

## 4. Cấu trúc

```
┌─────────────────────────────────────────┐
│ [icon]  Label text  [trailing icon]     │
└─────────────────────────────────────────┘
```

| Slot | Bắt buộc | Ghi chú |
|---|---|---|
| Container | có | Bo vuông 6px, padding `space.3 space.5` (compact) hoặc `space.4 space.6` (default) |
| Label | có | Bắt buộc trừ khi icon-only. `font.size.xl` (14px, 500). |
| Leading icon | không | 14×14px, gap `space.2` tới label |
| Trailing icon | không | 14×14px, gap `space.2` tới label |
| Loading spinner | có khi loading | Thay trailing icon slot khi `loading=true`. 14×14px, `motion.duration.instant` rotation. |

## 5. Biến thể

| Variant | Background | Text | Border | Cách dùng |
|---|---|---|---|---|
| `primary` | `color.text.primary` (`#ffffff`) | `color.surface.base` | none | Một primary action duy nhất mỗi page |
| `secondary` | `color.surface.strong` | `color.text.primary` | 1px `color.border.default` | Secondary actions, paired với primary |
| `ghost` | transparent | `color.text.primary` | none | Tertiary actions, "Cancel", "Learn more" |
| `destructive` | `color.surface.strong` | `#fca5a5` | 1px `#7f1d1d` | Delete, remove (dùng `shadow.2` cho emphasis) |
| `icon-only` | transparent (default) | `currentColor` | none | Toolbar buttons; phải có `aria-label` |
| `link-cta` | transparent | `color.text.primary` | underline on hover | Inline CTAs |

## 6. Sizes

| Size | Padding (y/x) | Font size | Height | Cách dùng |
|---|---|---|---|---|
| `compact` | `space.3` / `space.5` (10/16) | `font.size.lg` (13px) | 32px | Inline forms, dense lists |
| `default` | `space.4` / `space.6` (12/20) | `font.size.xl` (14px) | 40px | Default |
| `large` | `space.5` / `space.7` (16/24) | `font.size.2xl` (15px) | 48px | Hero CTAs, modal confirmations |

Touch target minimum: 44×44px. Nếu visual height nhỏ hơn, extend hit area với padding (không đổi visual size).

## 7. Trạng thái

| Trạng thái | Background | Text | Border | Transform | Shadow | Khác |
|---|---|---|---|---|---|---|
| `default` | variant base | variant base | variant base | none | none |. |
| `hover` | +4% lightness (`color.surface.hover`) | unchanged | unchanged | `translateY(-1px)` | `shadow.1` (primary/secondary) | 150ms ease-out |
| `focus-visible` | variant base | variant base | 2px outline `color.border.strong`, 2px offset | none | none | ring only |
| `active` (pressed) | -4% lightness | unchanged | unchanged | `translateY(0)` `scale(0.98)` | `shadow.3` | tactile press |
| `disabled` | `color.surface.strong` | `color.text.tertiary` | 1px `rgba(255,255,255,0.08)` | none | none | `cursor: not-allowed`, `aria-disabled="true"` |
| `loading` | variant base | `color.text.tertiary` | unchanged | none | none | spinner thay icon, `aria-busy="true"`, label có thể ẩn hoặc giữ |
| `error` (destructive only) | `color.surface.strong` | `#fca5a5` | 1px `#7f1d1d` | none | `shadow.2` | `aria-describedby` tới error message |

## 8. Loading state rules

- Spinner phải inherit button text color hoặc dùng `color.text.tertiary`.
- Label có thể giữ (khuyến nghị cho confirmation CTAs như "Save changes") hoặc thay bằng spinner alone (cho actions như "Submit").
- Button phải giữ trong tab order khi loading. Re-click trong loading là idempotent.
- `aria-busy="true"` khi loading.

## 9. Disabled state rules

- Không bao giờ xóa khỏi tab order. `aria-disabled="true"` trên focusable element; không dùng HTML `disabled` trừ khi permanently disabled.
- Cung cấp tooltip hoặc `aria-describedby` giải thích lý do khi không hiển nhiên.
- Disabled phải đạt 3:1 non-text contrast.

## 10. Responsive

- <768px: width = `100%` cho `primary` actions trong stacked forms. `default` và `secondary` buttons giữ inline.
- ≥768px: width = `auto` (content-based).
- Icon-only buttons giữ square aspect ratio ở mọi size (32×32, 40×40, 48×48).

## 11. Edge cases

- **Long label**: nếu label quá 3 từ, prefer split thành pattern "Action + subject". Không wrap. Dùng `text-wrap: balance` cho stacked button groups.
- **No label, icon-only**: phải có `aria-label` matching action ("Add to cart", "Close", "Copy code").
- **Confirmation required**: render `<dialog>` hoặc inline confirm pattern. Không `window.confirm()`.
- **Async with retry**: button hiển thị error state 3s sau failure, rồi trở về default. Retry action là cùng button.
- **Empty href**: không `<a href="">`. Dùng `<button>` nếu không có destination.

## 12. Accessibility

- `<button>` element. Không `<a role="button">` không có `href`.
- Tab order match visual order.
- `:focus-visible` bắt buộc (không `:focus`).
- Touch target ≥44×44px.
- `aria-disabled` thay vì `disabled` khi interactive retry cần.
- `aria-busy` trong loading.
- Color contrast: tất cả trạng thái đạt WCAG AA.

## 13. QA acceptance criteria

```
[ ] Tất cả 7 trạng thái định nghĩa và visually distinct
[ ] Hover lifts -1px và apply shadow
[ ] Focus-visible ring chỉ hiện trên keyboard nav
[ ] Disabled state đạt 3:1 non-text contrast
[ ] Loading spinner inherit text color
[ ] Async button idempotent trên double-click
[ ] Icon-only button có aria-label
[ ] Touch target ≥44×44px verify ở mọi size
[ ] Long labels không wrap (max-width: 24ch)
[ ] Responsive width behavior đúng ở 360/768/1024/1440px
[ ] prefers-reduced-motion: không transform animation
[ ] axe-core: 0 violations
[ ] Không em-dash trong label
```

## 14. Code reference

```tsx
{/* Primary subscribe button với ShoppingBag icon */}
<button
  type="button"
  class="group inline-flex items-center justify-center gap-2 px-5 py-3 bg-white text-black font-medium text-[14px] rounded-md shadow-[0_1px_2px_rgba(0,0,0,0.3)] hover:-translate-y-px hover:shadow-[0_4px_8px_rgba(0,0,0,0.4)] focus-visible:outline-2 focus-visible:outline-[#fafafa] focus-visible:outline-offset-2 active:translate-y-0 active:scale-[0.98] active:shadow-[0_1px_2px_rgba(0,0,0,0.3)] transition-all duration-150 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:translate-y-0"
>
  <Phosphor.ShoppingBag size={16} weight="bold" aria-hidden="true" />
  <span>Subscribe</span>
  <Phosphor.ArrowRight size={16} weight="bold" class="transition-transform duration-150 group-hover:translate-x-0.5" aria-hidden="true" />
</button>

{/* Secondary "Get template" với thumbnail + DownloadSimple */}
<button
  type="button"
  class="inline-flex items-center gap-2 px-5 py-2.5 bg-[#0d0d0d] text-white border border-[#e5e7eb] font-medium text-[14px] rounded-md hover:bg-[#1a1a1a] hover:border-[#fafafa] hover:-translate-y-px transition-all duration-150 focus-visible:outline-2 focus-visible:outline-[#fafafa] focus-visible:outline-offset-2"
>
  <img src="https://picsum.photos/seed/template-thumb-1/48/48" alt="" aria-hidden="true" class="w-6 h-6 rounded" />
  <Phosphor.DownloadSimple size={14} weight="bold" aria-hidden="true" />
  <span>Get template</span>
</button>

{/* Ghost "Cancel" */}
<button
  type="button"
  class="inline-flex items-center justify-center gap-2 px-5 py-2.5 text-white font-medium text-[14px] rounded-md hover:bg-[rgba(255,255,255,0.05)] focus-visible:outline-2 focus-visible:outline-[#fafafa] focus-visible:outline-offset-2 transition-colors duration-150"
>
  Cancel
</button>

{/* Icon-only copy button */}
<button
  type="button"
  aria-label="Copy code"
  class="inline-flex items-center justify-center w-11 h-11 text-[#a1a1aa] hover:text-white hover:bg-[rgba(255,255,255,0.05)] focus-visible:outline-2 focus-visible:outline-[#fafafa] focus-visible:outline-offset-2 transition-colors duration-150 rounded-md"
>
  <Phosphor.Copy size={16} weight="bold" aria-hidden="true" />
</button>

{/* Loading state */}
<button
  type="button"
  aria-busy="true"
  disabled
  class="inline-flex items-center justify-center gap-2 px-5 py-2.5 bg-white text-[#737373] font-medium text-[14px] rounded-md cursor-wait opacity-90"
>
  <Phosphor.CircleNotch size={14} weight="bold" class="animate-spin" aria-hidden="true" />
  <span>Saving...</span>
</button>

{/* GitHub social button với logo */}
<a
  href="https://github.com/proofmatcher"
  rel="noopener noreferrer"
  target="_blank"
  class="inline-flex items-center justify-center gap-2 px-4 py-2 bg-[#0d0d0d] border border-[#e5e7eb] text-white font-medium text-[13px] rounded-md hover:border-[#fafafa] transition-colors duration-150"
>
  <img src="https://cdn.simpleicons.org/github/ffffff" alt="" aria-hidden="true" class="w-4 h-4" />
  <span>Star on GitHub</span>
  <Phosphor.ArrowUpRight size={12} weight="bold" aria-hidden="true" />
</a>
```