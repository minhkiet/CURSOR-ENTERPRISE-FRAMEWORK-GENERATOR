# Link Component

> Navigation và inline reference element. Highest density trên site (mục tiêu 68 mỗi page). Phải visually distinct từ button để tránh nhầm lẫn.

## 1. Mục đích

Navigate tới trang khác, download file, hoặc inline reference. Linear-style underline-on-hover với monospace cho nav, color-only cho inline.

## 2. Hệ thống icon

| Vai trò | Icon Phosphor | Kích thước |
|---|---|---|
| External link | `ArrowUpRight` | 12-14px |
| Download | `DownloadSimple` | 12-14px |
| Open in new tab | `ArrowSquareOut` | 12px |
| Anchor (jump to section) | `ArrowDown` hoặc `ArrowLineDown` | 14px |
| Documentation link | `BookOpen` | 12px |
| GitHub link | `GithubLogo` (custom) hoặc dùng Simple Icons | 12px |
| Email | `Envelope` | 12px |
| Phone | `Phone` | 12px |
| Discord | `DiscordLogo` | 12px |

## 3. Hình ảnh và minh họa

Link không dùng ảnh. Ngoại lệ:

- **Inline logo link** (tới GitHub, Twitter): dùng Simple Icons CDN `https://cdn.simpleicons.org/{slug}/ffffff`. Ví dụ: `https://cdn.simpleicons.org/github/ffffff`, `https://cdn.simpleicons.org/twitter/ffffff`, `https://cdn.simpleicons.org/discord/ffffff`.

## 4. Cấu trúc

```
[icon?]  Link text
```

- Anchor: `<a>` element với `href`.
- Label: bắt buộc. Sentence case.
- Leading icon: optional (external link, download, arrow).

## 5. Biến thể

| Variant | Color | Underline | Cách dùng |
|---|---|---|---|
| `inline` (default) | `color.text.primary` | none, hover underline | Body copy references |
| `standalone` | `color.text.primary` | none, hover background tint | Card titles, list items |
| `nav` | `color.text.secondary`, hover `color.text.primary` | none, active: bottom border | Top navigation |
| `muted` | `color.text.tertiary`, hover `color.text.secondary` | none | Footer links, breadcrumbs |
| `danger` | `#fca5a5`, hover `#fecaca` | none | Delete, remove actions (hiếm; prefer button) |
| `external` | `color.text.primary` | underline always | External links (CSS prevent visited confusion) |

## 6. Phân biệt với button

- **Link** navigate hoặc download. Không `onclick` ngoài default browser behavior.
- **Button** trigger action (form submit, modal open, toggle).

Sai lầm phổ biến: `<a href="#" onclick="openModal()">`. Dùng `<button>` cho actions; reserve `<a>` cho navigation.

## 7. Sizes

| Size | Font size | Cách dùng |
|---|---|---|
| `compact` | `font.size.lg` (13px) | Footer, dense lists |
| `default` | `font.size.xl` (14px) | Body, navigation |
| `large` | `font.size.2xl` (15px) | Hero sub-links, prominent CTAs |

## 8. Trạng thái

| Trạng thái | Color | Underline | Khác |
|---|---|---|---|
| `default` | variant base | none |. |
| `hover` | variant base | 1px underline | transition 150ms ease-out |
| `focus-visible` | variant base | none | 2px outline `color.border.strong`, 2px offset |
| `active` | variant base + 8% lighten | 1px underline | cho `nav` variant: bottom border `color.border.strong` |
| `visited` | variant base (không đổi) | none | không style distinct để tránh color confusion |
| `disabled` | `color.text.tertiary` | none | `aria-disabled="true"`, `cursor: not-allowed` |

## 9. External link rules

- Luôn mark external links với `target="_blank"`.
- Thêm `rel="noopener noreferrer"` cho security.
- Thêm trailing icon (12×12px) chỉ external (`ArrowUpRight`) `aria-hidden="true"`.
- `aria-label="(opens in new tab)"` nếu visual cue không đủ (e.g. icon removed cho compact layout).

## 10. Active navigation rules

- Active nav link phải visually distinct từ inactive.
- Dùng bottom border 2px `color.border.strong` HOẶC weight 600 + color `color.text.primary`.
- `aria-current="page"` trên active link.

## 11. Touch and click target

- Inline links inherit line height. Standalone links cần `padding: space.2 space.3` để đạt 44×44px hit area.
- Click target phải ≥44×44px. Nếu text-only inline link quá nhỏ, wrap adjacent text trong parent mở rộng hit area.

## 12. Responsive

- Mọi breakpoint, link color và underline behavior consistent.
- Touch targets expand tự động qua padding trên touch devices (`@media (pointer: coarse)`).

## 13. Edge cases

- **Long link text**: wrap, không truncate. Dùng `text-wrap: balance` cho headings chứa links.
- **Link inside copy**: dùng `inline` variant. Underline xuất hiện on hover only, body copy giữ clean.
- **Empty href**: không bao giờ `<a href="">`. Dùng `<button>` nếu không có destination.
- **JavaScript-only link**: nếu destination cần JS, dùng `<a href="/fallback-url">` và progressively enhance.
- **Disabled link**: prefer xóa link hoàn toàn. Nếu disabled state cần thiết (e.g. trial expired), dùng `<span aria-disabled="true">` styled as link không có `href`.

## 14. Accessibility

- `<a>` với `href` focusable mặc định.
- Focus-visible bắt buộc.
- Color contrast: variant base trên background đạt 4.5:1.
- Underline không bắt buộc nếu non-color cue (bold, weight 600) phân biệt link với body text. Khuyến nghị: giữ underline-on-hover cho inline links.
- External link icon decorative (`aria-hidden`); `aria-label` mang announcement.

## 15. QA acceptance criteria

```
[ ] Tất cả 7 trạng thái định nghĩa
[ ] Active nav link có aria-current="page"
[ ] External links có rel="noopener noreferrer"
[ ] External links có aria-label "(opens in new tab)" nếu icon ẩn
[ ] Focus-visible ring chỉ hiện trên keyboard nav
[ ] Underline-on-hover cho inline variant
[ ] Click target ≥44×44px cho standalone variant
[ ] Không empty href
[ ] Long link text wrap, không truncate
[ ] Disabled links là spans, không anchors
[ ] axe-core: 0 violations
[ ] Không em-dash trong label
```

## 16. Code reference

```tsx
{/* Inline link trong body copy */}
<p class="text-[15px] text-[#a1a1aa] leading-relaxed">
  Browse our marketplace to find the template that fits your stack. For team plans,{' '}
  <a href="/pricing" class="text-white underline-offset-4 hover:underline transition-all duration-150">
    see pricing
  </a>
  .
</p>

{/* External link với icon ArrowUpRight */}
<a
  href="https://github.com/proofmatcher/templates"
  target="_blank"
  rel="noopener noreferrer"
  aria-label="View templates on GitHub (opens in new tab)"
  class="inline-flex items-center gap-1.5 text-white underline-offset-4 hover:underline transition-all duration-150"
>
  View templates on GitHub
  <Phosphor.ArrowUpRight size={12} weight="bold" aria-hidden="true" />
</a>

{/* Active nav link với bottom border */}
<nav aria-label="Primary" class="flex items-center gap-6">
  <a
    href="/"
    aria-current="page"
    class="relative text-white font-semibold text-[14px] py-2 after:absolute after:left-0 after:right-0 after:bottom-0 after:h-[2px] after:bg-white"
  >
    Home
  </a>
  <a
    href="/components"
    class="text-[#a1a1aa] hover:text-white text-[14px] py-2 transition-colors duration-150"
  >
    Components
  </a>
  <a
    href="/about"
    class="text-[#a1a1aa] hover:text-white text-[14px] py-2 transition-colors duration-150"
  >
    About
  </a>
</nav>

{/* Social icon link với Simple Icons */}
<a
  href="https://github.com/proofmatcher"
  target="_blank"
  rel="noopener noreferrer"
  aria-label="ProofMatcher on GitHub (opens in new tab)"
  class="inline-flex items-center justify-center w-9 h-9 text-[#a1a1aa] hover:text-white transition-colors duration-150"
>
  <img src="https://cdn.simpleicons.org/github/ffffff" alt="" aria-hidden="true" class="w-5 h-5" />
</a>

{/* Download link với icon */}
<a
  href="/templates/aurora.zip"
  download
  class="inline-flex items-center gap-1.5 text-[#a1a1aa] hover:text-white text-[13px] transition-colors duration-150"
>
  <Phosphor.DownloadSimple size={14} weight="bold" aria-hidden="true" />
  Download starter (2.4MB)
</a>

{/* Disabled link (trial expired). span, không anchor */}
<span
  aria-disabled="true"
  class="text-[#737373] cursor-not-allowed text-[14px]"
  title="Upgrade to Pro to access this template"
>
  <span class="line-through opacity-60">Pro template</span>
</span>
```