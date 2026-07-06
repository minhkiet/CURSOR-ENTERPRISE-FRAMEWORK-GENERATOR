# Button

> Nút bấm kích hoạt hành động. Tất cả nút trong brand đọc như con dấu ấn lên giấy dó: phản hồi xúc giác rõ ràng, chuyển động tối thiểu, có chủ đích.

## 1. Mục đích

Trigger cho các hành động chính: đăng ký gói, đăng nhập Google, mở FAQ, accordion trigger. Tất cả nút có cảm giác "ấn lên giấy": phản hồi tức thì, không có micro-animation thừa.

## 2. Hệ thống icon

Mọi nút dùng **Phosphor Regular** (`@phosphor-icons/react`). Stroke width thống nhất `weight="bold"` (1.5pt) cho cả icon-left và icon-right.

| Vai trò | Icon Phosphor | Kích thước theo size nút |
|---|---|---|
| Đăng ký / Subscribe | `Crown` (fill) | 16/18/20/22px theo `sm/md/lg/xl` |
| Mở lịch xem hôm nay | `BookOpen` | tương tự |
| Đăng nhập Google | Logo Google SVG chính hãng | 16px cố định |
| Đăng nhập Apple | Logo Apple SVG chính hãng | 16px cố định |
| Tiếp tục / Tiếp theo | `ArrowRight` | tương tự |
| Quay lại | `ArrowLeft` | tương tự |
| Đóng | `X` | 18px |
| Menu mobile | `List` | 20px |
| Đang tải | `CircleNotch` (spin) | 16px, `motion.duration.slow` rotation |
| Thành công | `CheckCircle` (fill) | 16px, màu gold |
| Lỗi | `WarningCircle` (fill) | 16px, màu `#a3201f` |
| FAQ trigger | `Plus` ↔ `Minus` | 18px |
| Chia sẻ | `ShareNetwork` | 16px |
| Tải xuống | `DownloadSimple` | 16px |

**Quy tắc**: một nút có tối đa 1 icon-left và 1 icon-right. Icon-right không bao giờ đứng một mình. Icon trái có thể đứng một mình (icon-only variant).

## 3. Hình ảnh và minh họa

Button không dùng ảnh nền. Tuy nhiên:
- Nút đăng ký gói có thể đặt **ảnh thumbnail cuốn lịch** (32×32px, bo vuông) bên trái label. Ảnh lấy từ `https://picsum.photos/seed/lich-to-thumb/64/64`.
- Nút social (Google, Apple, Facebook) dùng **logo chính hãng** từ Simple Icons: `https://cdn.simpleicons.org/google/1d3129`, `https://cdn.simpleicons.org/apple/1d3129`, `https://cdn.simpleicons.org/facebook/1d3129`.

Không dùng ảnh minh họa khác trên button. Button phải đọc nhanh trong 0.4 giây.

## 4. Cấu trúc

```
[ icon-left? ]  label  [ icon-right? ]
```

| Slot | Bắt buộc | Ghi chú |
|---|---|---|
| icon-left | không | 14–22px tùy size. Phosphor bold. |
| label | có | Tiếng Việt, sentence case cho hành động ("Khởi tạo"), ALL CAPS cho CTA premium ("ĐĂNG KÝ LỊCH NĂM"). |
| icon-right | không | 14–22px. Dành cho mũi tên / chevron. Không bao giờ đứng một mình. |
| focus ring | có | Bao quanh toàn bộ nút. |

## 5. Biến thể

| Biến thể | Nền | Chữ | Viền | Cách dùng |
|---|---|---|---|---|
| `primary-on-dark` | `#1d3129` | `#ede7d3` | không | CTA landing chính |
| `primary-on-light` | `#9a7c22` | `#1d3129` | không | CTA pricing featured, header Google login |
| `ghost` | transparent | `#3a3220` | `1px solid rgba(154, 124, 34, 0.18)` | Nav links dạng nút, FAQ trigger khi không dùng `<details>` |
| `ghost-inverse` | transparent | `#ede7d3` | `1px solid rgba(197, 165, 90, 0.25)` | Bề mặt tối, hành động phụ |
| `link-cta` | transparent | `#9a7c22` | không, gạch chân khi hover | Inline CTA ("Mở lịch" trong nav) |
| `icon-only` | match `ghost` hoặc `ghost-inverse` | không | match | Hamburger, accordion trigger |
| `destructive` | `#a3201f` | `#ede7d3` | không | Hủy đăng ký, xóa lịch sử |

## 6. Kích thước

| Token | Padding (x / y) | Font | Chiều cao tối thiểu |
|---|---|---|---|
| `sm` | 14 / 8 | 13px | 36px |
| `md` | 18 / 14 | 14px | 44px (mặc định) |
| `lg` | 24 / 18 | 15.5px | 52px (hero CTA) |
| `xl` | 32 / 20 | 16.5px | 56px (CTA section cuối) |

Mặc định `md`. `lg` dành cho hero/CTA sections. `sm` chỉ cho inline actions trong body.

## 7. Trạng thái

| Trạng thái | Thay đổi thị giác | Motion | Ghi chú a11y |
|---|---|---|---|
| default | base |. |. |
| hover | bg sẫm 3%, `shadow.gold` lift | 150ms ease-out | phải đạt được qua `:focus-visible` |
| focus-visible | outline 2px `color.focus.ring` offset 2px | không | bắt buộc, mouse click không hiện ring |
| active | bg sẫm 6%, `translateY(1px)` | 80ms ease-out | xúc giác ấn |
| disabled | opacity 0.45, `cursor: not-allowed`, không hover/press | không | `aria-disabled="true"` + tooltip giải thích |
| loading | label thay bằng spinner + text "Đang tải...", giữ chiều rộng | spinner xoay 800ms linear | `aria-live="polite"`, `aria-busy="true"` |
| success | bg chuyển gold sáng, label đổi "Đăng ký thành công", icon `CheckCircle` | 200ms ease-out | `role="status"` |
| error | bg tint đỏ 2%, rung 1 chu kỳ | 200ms ease-out | `role="alert"` trên thông báo lỗi |

Disabled trên landing hiện tại: opacity 0.85, `cursor: wait`, `aria-disabled="true"` vì subscription flow đang triển khai. Dùng tooltip "Tính năng đang được triển khai" (Feature coming soon).

## 8. Hiệu ứng animation

| Thuộc tính | Thời gian | Easing |
|---|---|---|
| `transform: translateY(-1px)` (hover) | 150ms | `cubic-bezier(0.16, 1, 0.3, 1)` |
| `box-shadow` lift | 150ms | ease-out |
| `border-color` | 150ms | ease-out |
| `background-color` | 150ms | ease-out |
| Loading spinner rotate | 800ms | linear infinite |

`prefers-reduced-motion: reduce`: thu gọn `transform` xuống 0.01ms nhưng giữ color/shadow transition ở 80ms.

## 9. Responsive

- ≥768px: size `md` hoặc `lg` theo design
- <768px: nút CTA chính của section stretch full-width (`width: 100%`)
- Icon-only giữ 44×44px hit area
- Font tối thiểu 14px (touch-friendly)

## 10. Edge cases

- Label dài: nếu width <200px có thể wrap. Set `white-space: nowrap` và rely on parent truncation, hoặc cho phép wrap với `text-align: center`. Ưu tiên truncate cho `md` và nhỏ hơn; chỉ wrap ở `xl` pricing tier CTA.
- Icon-only không label: phải có `aria-label`. Icon 18–24px.
- Disabled có lý do: `<button aria-disabled="true" aria-describedby="reason-id">` và `<span id="reason-id">` kế bên. Tooltip qua `title` cấm (không a11y trên touch).
- Loading: không disable nút khi loading; giữ width, swap label.
- CTA nhiều dòng: pricing tier "Đăng ký lịch năm" 1 dòng. Nếu label >24 chars ở size `md`, nâng lên `lg`.
- Emoji và sticker: cấm hoàn toàn. Dùng Phosphor icons.

## 11. Accessibility (WCAG 2.2 AA)

- Hit area: ≥44×44px. Icon-only: 44×44px tối thiểu.
- Tương phản:
  - `primary-on-dark`: `#ede7d3` trên `#1d3129` = 11.2:1 ✓ AAA
  - `primary-on-light`: `#1d3129` trên `#9a7c22` = 6.4:1 ✓ AA
  - `ghost`: `#3a3220` trên `#f0ece2` = 9.4:1 ✓ AAA
  - `ghost-inverse`: `#ede7d3` trên `#1d3129` = 11.2:1 ✓ AAA
  - `destructive`: `#ede7d3` trên `#a3201f` = 7.5:1 ✓ AA
  - `disabled`: text ở opacity 0.45 trên cream, xác minh ≥3:1 cho UI components
- Focus-visible: bắt buộc mọi biến thể. Ring `color.focus.ring`.
- Bàn phím:
  - Tab di chuyển focus vào nút
  - Enter và Space cùng kích hoạt
  - Escape hủy (trong modal/popover)
- Screen reader: name là button text hoặc `aria-label`, state qua `aria-pressed` (toggle), `aria-disabled` (disabled).
- Loading: thông báo "Đang tải" qua `aria-live="polite"` một lần, rồi thông báo kết quả khi xong.

## 12. Checklist QA

- [ ] 7 biến thể đúng token
- [ ] 4 size đúng padding/height
- [ ] 8 trạng thái có khác biệt thị giác
- [ ] `prefers-reduced-motion` xóa transform transition
- [ ] Focus-visible: không ring khi mouse click, có ring khi keyboard tab
- [ ] Hit area ≥44×44px mọi breakpoint
- [ ] Loading giữ width
- [ ] Disabled có accessible explanation
- [ ] Tất cả biến thể verify ở mobile (375px), tablet (768px), desktop (1280px)
- [ ] axe-core scan: 0 vi phạm
- [ ] Không có em-dash (`,`) trong label

## 13. Code reference

```tsx
{/* CTA đăng ký gói với icon Crown */}
<a
  href="/dat-lich?plan=goi_12thang"
  class="group inline-flex items-center justify-center gap-2.5 px-6 py-3.5 bg-[#1d3129] text-[#ede7d3] font-display font-bold uppercase text-[14px] tracking-[0.1em] shadow-[0_8px_18px_rgba(29,49,41,0.18)] hover:-translate-y-px hover:shadow-[0_12px_24px_rgba(29,49,41,0.25)] active:translate-y-0 active:shadow-[0_4px_10px_rgba(29,49,41,0.18)] transition-all duration-150 rounded-[2px]"
>
  <Phosphor.Crown size={16} weight="fill" class="text-[#c5a55a] transition-transform duration-150 group-hover:rotate-[8deg]" aria-hidden="true" />
  <span>Đăng ký lịch năm</span>
  <Phosphor.ArrowRight size={16} weight="bold" class="transition-transform duration-150 group-hover:translate-x-1" aria-hidden="true" />
</a>

{/* Google login với logo chính hãng */}
<button
  type="button"
  class="inline-flex items-center justify-center gap-2.5 px-5 py-2.5 bg-[#9a7c22] text-[#1d3129] font-display font-bold uppercase text-[14px] tracking-[0.1em] hover:-translate-y-px transition-transform duration-150 rounded-[2px]"
>
  <img src="https://cdn.simpleicons.org/google/1d3129" alt="" aria-hidden="true" class="w-4 h-4" />
  <span>Tiếp tục với Google</span>
</button>

{/* Loading state */}
<button
  type="button"
  aria-busy="true"
  aria-live="polite"
  class="inline-flex items-center justify-center gap-2.5 px-6 py-3.5 bg-[#1d3129] text-[#ede7d3] opacity-90 cursor-wait rounded-[2px]"
>
  <Phosphor.CircleNotch size={16} weight="bold" class="animate-spin" aria-hidden="true" />
  <span>Đang tải...</span>
</button>

{/* Icon-only close button */}
<button
  type="button"
  aria-label="Đóng"
  class="inline-flex items-center justify-center w-11 h-11 text-[#ede7d3] hover:bg-[rgba(197,165,90,0.1)] focus-visible:outline-2 focus-visible:outline-[#9a7c22] focus-visible:outline-offset-2 transition-colors duration-150 rounded-[2px]"
>
  <Phosphor.X size={18} weight="bold" aria-hidden="true" />
</button>
```