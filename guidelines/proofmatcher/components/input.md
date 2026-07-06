# Input Component

> Text input cho search, email, password, và form fields. Lower density hơn buttons (1 mỗi page typically) nhưng high importance. single source of user intent capture.

## 1. Mục đích

Capture user intent: search templates, enter email để subscribe, password cho account. Mỗi input phải đọc nhanh và phản hồi rõ ràng về state.

## 2. Hệ thống icon

| Vai trò | Icon Phosphor | Kích thước |
|---|---|---|
| Search | `MagnifyingGlass` | 16px |
| Email | `Envelope` | 16px |
| Password (locked) | `Lock` | 16px |
| Password toggle visible | `Eye` / `EyeSlash` | 16px |
| User | `User` | 16px |
| Clear (khi có value) | `XCircle` (fill) | 14px |
| Required indicator | `Asterisk` | 10px, đỏ `#fca5a5` |
| Error | `WarningCircle` (fill) | 14px, đỏ nhạt `#fca5a5` |
| Success | `CheckCircle` (fill) | 14px, mint `#34d399` |
| Loading | `CircleNotch` (spin) | 14px, tertiary |
| URL | `Link` | 16px |
| Phone | `Phone` | 16px |
| Dropdown chevron (select) | `CaretDown` | 14px |

## 3. Hình ảnh và minh họa

Input tiêu chuẩn không dùng ảnh. Một số case đặc biệt:

- **Search hero** trên marketplace có thể dùng **ảnh background mờ** (Picsum landscape, opacity 0.1) để tạo mood. `https://picsum.photos/seed/code-editor-night/1920/600`.
- **404 form / auth page** có thể đặt **ảnh minh họa** 96×96 cạnh form. `https://picsum.photos/seed/auth-illustration/192/192`.

## 4. Cấu trúc

```
┌─────────────────────────────────────────┐
│ [icon]  Placeholder or value            │
└─────────────────────────────────────────┘
   Helper text or error message (optional)
```

| Slot | Bắt buộc | Ghi chú |
|---|---|---|
| Container | có | `<input>` wrap trong label-element div, padding `space.4 space.5` (12/16) |
| Label | có | Bắt buộc, luôn hiển thị phía trên. `font.size.lg` (13px, 500). Không dùng placeholder thay label. |
| Leading icon | không | 16×16px, decorative (`aria-hidden="true"`). Functional icons (clear, password toggle) sống như buttons bên trong input. |
| Helper text | không | Dưới input, `font.size.md` (12px), `color.text.tertiary`. |
| Error message | có khi lỗi | Thay helper text khi invalid, `role="alert"`, liên kết qua `aria-describedby`. |

## 5. Biến thể

| Variant | Border | Background | Cách dùng |
|---|---|---|---|
| `default` | 1px `color.border.default` | `color.surface.base` | Mọi inputs |
| `filled` | 1px `color.border.default` | `color.surface.raised` | Search field trên hero |
| `inline` | none | transparent | Inline editing, filter chips với text |
| `search-hero` | 1px `rgba(255,255,255,0.12)` | `rgba(255,255,255,0.04)` + backdrop-blur | Hero search, large search bars |

Search field là variant riêng cho visual prominence. Password field dùng cùng anatomy nhưng có toggle visibility button.

## 6. Sizes

| Size | Padding (y/x) | Font size | Height |
|---|---|---|---|
| `compact` | `space.3` / `space.4` (10/12) | `font.size.lg` (13px) | 32px |
| `default` | `space.4` / `space.5` (12/16) | `font.size.xl` (14px) | 40px |
| `large` | `space.5` / `space.6` (16/20) | `font.size.2xl` (15px) | 48px |

## 7. Trạng thái

| Trạng thái | Border | Background | Khác |
|---|---|---|---|
| `default` | 1px `color.border.default` | `color.surface.base` |. |
| `hover` | 1px `color.border.strong` | unchanged | `cursor: text` |
| `focus` (mouse click, no ring) | 1px `color.border.strong` | unchanged | `caret-color: color.text.primary` |
| `focus-visible` (keyboard nav) | 1px `color.border.strong` + 2px outline `color.border.strong`, 2px offset | unchanged | ring bắt buộc |
| `filled` | 1px `color.border.default` | `color.surface.raised` | khi value present |
| `error` | 1px `#7f1d1d` | `color.surface.base` | `shadow.2`, `aria-invalid="true"`, error message visible |
| `disabled` | 1px `rgba(255,255,255,0.08)` | `color.surface.raised` | `cursor: not-allowed`, `aria-disabled="true"` |
| `loading` | 1px `color.border.default` | `color.surface.base` | spinner thay leading icon, `aria-busy="true"` |

## 8. Label rules (bắt buộc)

- Luôn render `<label>` phía trên input. `<label for="input-id">` khớp `id` trên input.
- Placeholder không bao giờ là label. Placeholder biến mất khi gõ; label phải persist.
- Helper text dưới input riêng biệt với label. Error message thay helper khi invalid.
- Required field indicator: `*` sau label text, với `aria-required="true"` trên input.

## 9. Validation rules

- Validate on blur, không trên mỗi keystroke.
- Hiển thị error sau first blur nếu invalid; clear error trên first valid keystroke sau error.
- Error message phải specific: "Email must include @" không "Invalid input".
- `aria-invalid="true"` + `aria-describedby="error-id"` link tới error message.
- `role="alert"` trên error message để screen readers announce khi xuất hiện.
- Dùng `aria-live="polite"` nếu error xuất hiện mà không có focus change.

## 10. Search input specifics

- Leading search icon (decorative).
- Trailing clear button (`aria-label="Clear search"`) chỉ xuất hiện khi value không rỗng.
- Submit on Enter triggers search; không yêu cầu button click.
- `type="search"` cho native UX (browsers có thể thêm clear riêng).

## 11. Password input specifics

- Trailing toggle visibility button (`aria-label="Show password"` / `aria-label="Hide password"`).
- `aria-pressed="true|false"` trên toggle phản ánh state.
- Không bao giờ disable password paste.

## 12. Responsive

- <768px: full-width mặc định.
- ≥768px: max-width 400px trừ khi inline form.
- Font size phải ≥16px trên iOS để tránh zoom-on-focus. Dùng `font-size: max(16px, 1rem)`.

## 13. Edge cases

- **Empty value on submit**: hiển thị error "Required" chỉ nếu field required.
- **Autofill**: respect `autocomplete` attribute values. Không override với custom UI.
- **Long content**: max-width applies; horizontal scroll bên trong input cấm. overflow phải xử lý bằng truncation.
- **Copy/paste**: không block.
- **RTL**: dùng logical properties (`padding-inline-start` không `padding-left`).

## 14. Accessibility

- `<label>` luôn liên kết qua `for`/`id`.
- Required: `aria-required="true"` (visible `*` cộng).
- Invalid: `aria-invalid="true"` cộng visible error.
- Disabled: `aria-disabled="true"` (không native `disabled` nếu re-enable expected).
- Focus-visible ring bắt buộc.
- Color contrast: text trên background đạt 4.5:1. Border trên background đạt 3:1.
- Touch target ≥44×44px (toàn bộ input là hit area).

## 15. QA acceptance criteria

```
[ ] Label persists khi typing
[ ] Placeholder không act as label
[ ] Focus-visible ring xuất hiện trên Tab
[ ] Mouse click không hiện focus ring
[ ] Error message link qua aria-describedby
[ ] Error có role="alert" và được announce
[ ] Clear button (search) có aria-label
[ ] Password toggle có aria-label và aria-pressed
[ ] Disabled state có tooltip/aria-describedby giải thích lý do
[ ] Long content không gây horizontal scroll
[ ] iOS font size ≥16px để tránh zoom
[ ] Touch target ≥44×44px
[ ] prefers-reduced-motion: không transition animation
[ ] axe-core: 0 violations
[ ] Không em-dash trong label hoặc helper text
```

## 16. Code reference

```tsx
{/* Search input với MagnifyingGlass + clear button */}
<div class="flex flex-col gap-1.5">
  <label for="search-templates" class="text-[13px] font-medium text-white">
    Search templates
  </label>
  <div class="relative">
    <Phosphor.MagnifyingGlass size={16} weight="bold" class="absolute left-3.5 top-1/2 -translate-y-1/2 text-[#737373] pointer-events-none" aria-hidden="true" />
    <input
      id="search-templates"
      type="search"
      value={searchValue}
      onChange={e => setSearchValue(e.target.value)}
      placeholder="Try &quot;SaaS dashboard&quot; or &quot;agency&quot;..."
      class="w-full pl-11 pr-11 py-3 bg-[#050505] text-white font-mono text-[14px] border border-[#e5e7eb] rounded-md placeholder:text-[#737373] hover:border-[#fafafa] focus:outline-2 focus:outline-[#fafafa] focus:outline-offset-2 focus:border-[#fafafa] transition-colors duration-150"
    />
    {searchValue && (
      <button
        type="button"
        aria-label="Clear search"
        onClick={() => setSearchValue('')}
        class="absolute right-3 top-1/2 -translate-y-1/2 text-[#737373] hover:text-white transition-colors duration-150"
      >
        <Phosphor.XCircle size={14} weight="fill" aria-hidden="true" />
      </button>
    )}
  </div>
  <span class="text-[12px] text-[#737373]">
    247 templates indexed
  </span>
</div>

{/* Email input với error state */}
<div class="flex flex-col gap-1.5">
  <label for="email" class="text-[13px] font-medium text-white flex items-center gap-1">
    Email
    <Phosphor.Asterisk size={9} weight="bold" class="text-[#fca5a5]" aria-label="bắt buộc" />
  </label>
  <div class="relative">
    <Phosphor.Envelope size={16} weight="bold" class="absolute left-3.5 top-1/2 -translate-y-1/2 text-[#737373] pointer-events-none" aria-hidden="true" />
    <input
      id="email"
      type="email"
      required
      aria-required="true"
      aria-invalid={hasError}
      aria-describedby={hasError ? 'email-error' : 'email-helper'}
      class={cn(
        'w-full pl-11 pr-11 py-3 bg-black text-white font-mono text-[14px] border rounded-md placeholder:text-[#737373] focus:outline-2 focus:outline-[#fafafa] focus:outline-offset-2 transition-colors duration-150',
        hasError ? 'border-[#7f1d1d] shadow-[0_2px_8px_rgba(127,29,29,0.3)]' : 'border-[#e5e7eb] hover:border-[#fafafa] focus:border-[#fafafa]'
      )}
      placeholder="founder@startup.io"
    />
    {hasError && (
      <Phosphor.WarningCircle size={16} weight="fill" class="absolute right-3.5 top-1/2 -translate-y-1/2 text-[#fca5a5]" aria-hidden="true" />
    )}
  </div>
  {hasError ? (
    <span id="email-error" role="alert" class="flex items-center gap-1 text-[12px] text-[#fca5a5]">
      <Phosphor.WarningCircle size={12} weight="fill" aria-hidden="true" />
      Email must include @ and a valid domain.
    </span>
  ) : (
    <span id="email-helper" class="text-[12px] text-[#737373]">
      We'll send your subscription receipt here.
    </span>
  )}
</div>

{/* Password input với toggle visibility */}
<div class="flex flex-col gap-1.5">
  <label for="password" class="text-[13px] font-medium text-white">
    Password
  </label>
  <div class="relative">
    <Phosphor.Lock size={16} weight="bold" class="absolute left-3.5 top-1/2 -translate-y-1/2 text-[#737373] pointer-events-none" aria-hidden="true" />
    <input
      id="password"
      type={showPassword ? 'text' : 'password'}
      autoComplete="current-password"
      class="w-full pl-11 pr-11 py-3 bg-black text-white font-mono text-[14px] border border-[#e5e7eb] rounded-md hover:border-[#fafafa] focus:outline-2 focus:outline-[#fafafa] focus:outline-offset-2 focus:border-[#fafafa] transition-colors duration-150"
    />
    <button
      type="button"
      aria-label={showPassword ? 'Hide password' : 'Show password'}
      aria-pressed={showPassword}
      onClick={() => setShowPassword(s => !s)}
      class="absolute right-3 top-1/2 -translate-y-1/2 text-[#737373] hover:text-white transition-colors duration-150"
    >
      {showPassword ? <Phosphor.EyeSlash size={16} weight="bold" aria-hidden="true" /> : <Phosphor.Eye size={16} weight="bold" aria-hidden="true" />}
    </button>
  </div>
</div>
```