# Input

> Trường nhập liệu cho text ngắn, search, và ngày (ngày sinh cho Tứ Trụ). Mỗi input là một "phiếu điền" trên giấy dó: label phía trên, viền chỉ vàng nhạt, error message đỏ mực bên dưới.

## 1. Mục đích

Nhập liệu cho landing (auth/signup) và app (ngày giờ sinh, profile, AI chat). Tứ Trụ yêu cầu lunar-solar accuracy nên date picker là trọng tâm.

## 2. Hệ th系統 icon

| Vai trò | Icon Phosphor | Kích thước |
|---|---|---|
| Search | `MagnifyingGlass` | 16px |
| Calendar / date picker | `CalendarBlank` | 16px |
| Time picker (giờ sinh) | `Clock` | 16px |
| Clear (khi có value) | `XCircle` (fill) | 14px |
| Toggle password visibility | `Eye` / `EyeSlash` | 16px |
| Dropdown chevron (select) | `CaretDown` | 14px |
| Error indicator | `WarningCircle` (fill) | 14px, đỏ `#a3201f` |
| Success indicator | `CheckCircle` (fill) | 14px, jade `#7a9a80` |
| Loading | `CircleNotch` (spin) | 14px, tertiary |
| Required marker | `Asterisk` | 10px, đỏ `#a3201f` |

## 3. Hình ảnh và minh họa

Input tiêu chuẩn không dùng ảnh. Tuy nhiên cho một số flow đặc biệt:

- **Date of birth flow**: hiển thị minh họa **âm lịch Việt Nam** (12 con giáp xếp vòng tròn) cạnh date picker. Lấy từ `https://picsum.photos/seed/12-con-giap/200/200`. Ảnh 120×120px, opacity 0.15, đặt góc trên-phải của form section.
- **Time of birth**: dùng **đồng hồ cát** mini 32×32 cạnh input. `https://picsum.photos/seed/dong-ho-cat-mini/64/64`.
- **Welcome / onboarding screen**: dùng **ảnh nền thư pháp** nhẹ (opacity 0.04). `https://picsum.photos/seed/thu-phap-vintage/800/600`.

## 4. Cấu trúc

```
[ label (above)               ]
[ icon-left  text  icon-right ]
[ helper text / error          ]
```

| Slot | Bắt buộc | Ghi chú |
|---|---|---|
| label | có | Luôn hiển thị phía trên input. Tiếng Việt, sentence case. |
| input | có | Single-line mặc định. Multi-line tùy chọn. |
| icon-left | không | MagnifyingGlass, CalendarBlank. 16px. |
| icon-right | không | Clear (XCircle) khi có value. Toggle (Eye) cho password. |
| helper text | không | Dưới input. `color.text.tertiary` (#7a7050). |
| error message | có khi lỗi | Dưới input, thay helper khi error state. |

## 5. Biến thể

| Biến thể | Background | Border | Cách dùng |
|---|---|---|---|
| `default` | `#ffffff` (trắng trên cream) hoặc `transparent` trên dark | `1px solid rgba(154, 124, 34, 0.18)` | Standard input trên light |
| `on-dark` | `rgba(255, 255, 255, 0.04)` | `1px solid rgba(197, 165, 90, 0.25)` | Trên `#1d3129` CTA sections |
| `inline` | transparent | `none`, gạch chân bottom | Search bar, filter row |
| `date-picker` | `#ffffff` | `1px solid rgba(154, 124, 34, 0.18)` | Date of birth với nút calendar |

## 6. Sizes

| Token | Padding (x / y) | Font | Min height |
|---|---|---|---|
| `sm` | 12 / 8 | 13.5px | 36px |
| `md` | 16 / 12 | 14.5px | 44px (mặc định) |
| `lg` | 18 / 14 | 15.5px | 52px (modal forms) |

## 7. Trạng thái

| Trạng thái | Thay đổi thị giác | Ghi chú a11y |
|---|---|---|
| default | base border |. |
| hover | border chuyển `1px solid #9a7c22` |. |
| focus | `outline: 2px solid color.focus.ring; outline-offset: 2px` + border sẫm gold | bắt buộc |
| focus-visible | giống focus | bắt buộc cho keyboard |
| filled | giống default | value được announce |
| error | border `1.5px solid #a3201f` (đỏ mực), error message dưới đỏ | `aria-invalid="true"`, `aria-describedby="error-id"` |
| success | border `1px solid #7a9a80` (jade), success message dưới jade | `aria-describedby="success-id"` |
| disabled | `bg: rgba(154, 124, 34, 0.05)`, `color: #7a7050`, `cursor: not-allowed` | `aria-disabled="true"` |
| loading | spinner bên phải thay clear button | `aria-busy="true"` |

## 8. Field types

| Type | Cách dùng | Ghi chú |
|---|---|---|
| `text` | Tên, địa điểm | Standard |
| `email` | Email | Validation: phải có `@` và `.` |
| `tel` | Số điện thoại (Việt Nam) | Validation: 10 chữ số, tùy chọn +84 prefix |
| `date` | Ngày sinh | Tứ Trụ yêu cầu lunar-solar accuracy. Cung cấp toggle "Âm lịch" riêng nếu cần. |
| `time` | Giờ sinh | Bắt buộc cho Tứ Trụ. Dùng 12 chi format (Tý 23:00-01:00...). |
| `password` | Mật khẩu | Toggle Eye/EyeSlash. Không cấm paste. |
| `search` | Tìm kiếm | Có clear button, native `type="search"`. |
| `tel-prefix` | Mã vùng +84 | Dropdown chọn mã vùng, kèm CaretDown. |

## 9. Quy tắc đặc thù Việt Nam

- **Ngày sinh**: hiển thị cả Dương lịch và Âm lịch khi liên quan. Mặc định Dương lịch.
- **Giờ sinh**: hiển thị 12 chi (Tý 23:00-01:00, Sửu 01:00-03:00, ..., Hợi 21:00-23:00). Có helper chuyển 24h sang chi hour.
- **Số điện thoại**: format `0xxx xxx xxx` (10 chữ số) hoặc `+84 xxx xxx xxx`.
- **Tên**: không strip dấu. Hiển thị đúng như user nhập.
- **Địa chỉ**: dùng bộ chọn tỉnh/huyện Việt Nam (xem skill `vietnam-address`).
- **Giới tính / năm sinh âm lịch**: select với Can Chi năm (Giáp Tý, Ất Sửu...).

## 10. Responsive

- <768px: full-width inputs trong form rows. Stack label phía trên input (không float inline).
- ≥768px: form rows có thể dùng 2-col layout (ví dụ name + phone cạnh nhau).
- iOS: font ≥16px để tránh zoom-on-focus. Dùng `font-size: max(16px, 1rem)`.

## 11. Edge cases

- Input dài: scroll ngang trong input trên mobile. Set `overflow-x: auto; white-space: nowrap` trên inner element.
- Empty state: hiển thị ghost hint trong input chỉ khi input rỗng VÀ không focus. Khi focus hoặc có value, ẩn hint.
- Date picker (ngày sinh): cần calendar widget. Dùng native `<input type="date">` với `lang="vi"` fallback. Cho UX tốt hơn, cung cấp picker custom với tên ngày/tháng tiếng Việt.
- Auto-formatting (phone, currency): áp dụng on blur, không trên mỗi keystroke.
- Validation timing: validate on blur, không trên mỗi keystroke. Hiển thị error chỉ sau user chỉnh sửa xong.
- Required field: thêm ` *` (với `aria-label="bắt buộc"`) vào label text.
- Paste handling: không transform pasted content. Nếu paste vi phạm format, hiển thị error on blur.
- Copy/paste: không block.
- RTL: dùng logical properties (`padding-inline-start` không `padding-left`).

## 12. Accessibility (WCAG 2.2 AA)

- **Label association**: mọi input phải có `<label for="input-id">` khớp `id="input-id"`. `aria-label` đơn thuần cấm khi có visible label.
- **Required indicator**: visible `*` cộng `aria-required="true"`.
- **Error association**: `aria-invalid="true"` + `aria-describedby="error-id"` trỏ tới error message container.
- **Success association**: `aria-describedby="success-id"` cho success message.
- **Password toggle**: `aria-pressed="true|false"` phản ánh state.
- **Clear button**: `aria-label="Xóa giá trị"` và `aria-pressed="true|false"` nếu dùng toggle.
- Tương phản:
  - Default border `rgba(154, 124, 34, 0.18)` trên trắng: ≥3:1 (UI component) ✓
  - Focus border `#9a7c22` trên trắng: ≥3:1 ✓
  - Text `#18150e` trên `#ffffff`: 14.8:1 ✓ AAA
  - Helper `#7a7050` trên `#ffffff`: 5.4:1 ✓ AA
  - Error `#a3201f` trên `#ffffff`: 5.9:1 ✓ AA
  - Success `#7a9a80` trên `#ffffff`: 4.6:1 ✓ AA
  - On-dark variant: text `#ede7d3` trên `rgba(255, 255, 255, 0.04)` overlaid trên `#1d3129`, verify ≥4.5:1
- Hit area: ≥44×44px.
- Bàn phím: Tab di chuyển focus, typing hoạt động, Shift+Tab back. Date picker phải keyboard-navigable (arrow keys, Enter select).
- Screen reader: announce name (từ label), state (required, invalid, disabled), error.

## 13. Checklist QA

- [ ] Label liên kết chương trình qua `for`/`id`
- [ ] Tất cả 8 trạng thái định nghĩa
- [ ] Error message chỉ hiển thị sau blur
- [ ] Required field có indicator + `aria-required`
- [ ] Tiếng Việt giữ dấu khi nhập và hiển thị
- [ ] Ngày sinh hỗ trợ cả Dương và Âm lịch khi liên quan
- [ ] Giờ sinh dùng chi-hour format
- [ ] `prefers-reduced-motion` xóa focus ring animation
- [ ] Focus ring hiện trên keyboard, ẩn trên mouse
- [ ] Touch target ≥44×44px trên mobile
- [ ] axe-core scan: 0 vi phạm
- [ ] Date picker có hình ảnh minh họa 12 con giáp (nếu flow ngày sinh)
- [ ] Time picker có icon Clock Phosphor

## 14. Code reference

```tsx
{/* Ngày sinh với icon Calendar và toggle Âm/Dương */}
<div class="flex flex-col gap-1.5">
  <label for="ngay-sinh" class="font-serif text-[13.5px] text-[#3a3220] flex items-center gap-1">
    Ngày sinh (Dương lịch)
    <Phosphor.Asterisk size={9} weight="bold" class="text-[#a3201f]" aria-label="bắt buộc" />
  </label>
  <div class="relative">
    <Phosphor.CalendarBlank size={16} weight="regular" class="absolute left-3.5 top-1/2 -translate-y-1/2 text-[#7a7050] pointer-events-none" aria-hidden="true" />
    <input
      id="ngay-sinh"
      type="date"
      lang="vi"
      required
      aria-required="true"
      aria-invalid={hasError}
      aria-describedby={hasError ? 'ngay-sinh-error' : 'ngay-sinh-helper'}
      class={cn(
        'w-full pl-11 pr-4 py-3 font-serif text-[14.5px]',
        'bg-white border',
        hasError ? 'border-[1.5px] border-[#a3201f]' : 'border border-[rgba(154,124,34,0.18)]',
        'hover:border-[#9a7c22]',
        'focus:outline-[2px] focus:outline-[oklab(0.73_0.0104587_0.119543_/_0.5)] focus:outline-offset-2',
      )}
    />
  </div>
  {hasError ? (
    <span id="ngay-sinh-error" role="alert" class="flex items-center gap-1 text-[12.5px] text-[#a3201f]">
      <Phosphor.WarningCircle size={13} weight="fill" aria-hidden="true" />
      Vui lòng nhập ngày sinh hợp lệ.
    </span>
  ) : (
    <span id="ngay-sinh-helper" class="text-[12.5px] text-[#7a7050]">
      Dùng để lập lá số Tứ Trụ của bạn.
    </span>
  )}
</div>

{/* Search input với clear button */}
<div class="relative">
  <Phosphor.MagnifyingGlass size={16} weight="bold" class="absolute left-3.5 top-1/2 -translate-y-1/2 text-[#7a7050] pointer-events-none" aria-hidden="true" />
  <input
    type="search"
    placeholder="Tìm câu tục ngữ, can chi..."
    class="w-full pl-11 pr-11 py-3 font-serif text-[14.5px] bg-white border border-[rgba(154,124,34,0.18)] focus:outline-[2px] focus:outline-[#9a7c22] focus:outline-offset-2"
  />
  {searchValue && (
    <button
      type="button"
      aria-label="Xóa tìm kiếm"
      onClick={() => setSearchValue('')}
      class="absolute right-3 top-1/2 -translate-y-1/2 text-[#7a7050] hover:text-[#1d3129]"
    >
      <Phosphor.XCircle size={16} weight="fill" aria-hidden="true" />
    </button>
  )}
</div>

{/* Password input với toggle visibility */}
<div class="relative">
  <input
    type={showPassword ? 'text' : 'password'}
    class="w-full pl-4 pr-11 py-3 font-serif text-[14.5px] bg-white border border-[rgba(154,124,34,0.18)] focus:outline-[2px] focus:outline-[#9a7c22] focus:outline-offset-2"
    aria-describedby="password-helper"
  />
  <button
    type="button"
    aria-label={showPassword ? 'Ẩn mật khẩu' : 'Hiện mật khẩu'}
    aria-pressed={showPassword}
    onClick={() => setShowPassword(s => !s)}
    class="absolute right-3 top-1/2 -translate-y-1/2 text-[#7a7050] hover:text-[#1d3129]"
  >
    {showPassword ? <Phosphor.EyeSlash size={16} weight="bold" /> : <Phosphor.Eye size={16} weight="bold" />}
  </button>
</div>
```