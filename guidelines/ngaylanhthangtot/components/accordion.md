# Accordion

> Thanh điều hướng câu hỏi. Mỗi dòng FAQ dùng `<details>`/`<summary>` để giữ nguyên phím tắt và trình đọc màn hình. Không bao giờ vẽ tay SVG khi `<details>` đã có sẵn ngữ nghĩa.

## 1. Mục đích

Câu hỏi thường gặp của khách 30+ Việt Nam, đặc biệt về Tứ Trụ, ngày giờ sinh, hoàn tiền và đồng bộ PWA. Sáu mục, mục đầu mở sẵn để giảm tải nhận thức ngay khi cuộn tới. Mục tiêu UX: trả lời đúng câu hỏi khách đang nghĩ trong 8 giây.

## 2. Hệ thống icon

Mọi accordion dùng **Phosphor Regular** (`@phosphor-icons/react`). Ngôn ngữ mặc định `weight="regular"`, các nút quan trọng `weight="bold"`.

| Vai trò hiện tại | Icon Phosphor | Kích thước |
|---|---|---|
| Mở rộng (collapsed) | `Plus` | 20px |
| Thu gọn (expanded) | `Minus` | 20px |
| Đánh số câu hỏi | `NumberOne`, `NumberTwo`, ... (theo index) | 14px |
| Bookmark câu hỏi quan trọng | `BookmarkSimple` | 16px |
| Cảnh báo chính sách (câu về hoàn tiền, auto-renew) | `WarningCircle` | 16px, `weight="fill"`, màu `#a3201f` |
| Liên kết ngoài (hướng dẫn chi tiết) | `ArrowUpRight` | 14px |

`Plus` xoay 45 độ khi mở không còn được dùng. Thay bằng morph `Plus → Minus` để tránh cảm giác "loading-spinner".

## 3. Hình ảnh và minh họa

FAQ không dùng ảnh chính. Tuy nhiên mỗi mục có thể đi kèm **một hình minh họa nhỏ** (48×48px) ở đầu dòng khi nội dung cần trực quan hóa:

| Mục FAQ | Hình minh họa | Nguồn |
|---|---|---|
| Ứng dụng hoạt động như thế nào | Bàn tay cầm cuốn lịch cổ | `https://picsum.photos/seed/lich-to-vietnam/96/96` |
| Tứ Trụ có chính xác không | La bàn phong thủy | `https://picsum.photos/seed/la-ban-phong-thuy/96/96` |
| Hoàn tiền 7 ngày | Phong bì đóng dấu sáp đỏ | `https://picsum.photos/seed/phong-bi-hoan-tien/96/96` |
| Có tự động gia hạn không | Ổ khóa đồng | `https://picsum.photos/seed/o-khoa-dong/96/96` |
| Đồng bộ thiết bị | Điện thoại và máy tính bàn cạnh nhau | `https://picsum.photos/seed/dong-bo-thiet-bi/96/96` |
| Tôi sinh không nhớ giờ | Đồng hồ cát gỗ | `https://picsum.photos/seed/dong-ho-cat-vintage/96/96` |

Ảnh minh họa chỉ hiển thị khi accordion mở. Khi thu gọn, slot ảnh để trống (không giữ chỗ) để giữ danh sách gọn.

## 4. Cấu trúc

```
┌──────────────────────────────────────────────┐
│ ①  Ứng dụng hoạt động như thế nào?     [+] │ ← 60px row, 19.5px
│ ─────────────────────────────────────────── │ ← hairline gold
│ Chỉ mất 30 giây để nhập ngày giờ sinh.    │
│ Hệ thống tính ra lá số Tứ Trụ theo can chi │
│ của bạn, sau đó mỗi sáng sẽ gửi một trang  │
│ lịch qua PWA, email và ứng dụng.           │
│                                              │
│ → Đọc hướng dẫn đầy đủ                     │
└──────────────────────────────────────────────┘
```

| Slot | Bắt buộc | Ghi chú |
|---|---|---|
| number | có | `NumberOne` ... `NumberSix` của Phosphor, 14px, `color.text.tertiary`. Khi mở chuyển sang `color.accent.gold` (`#9a7c22`) và `weight="bold"`. |
| question | có | Display `Lora` extrabold, 19.5px (desktop) / 17.5px (mobile), `color.text.primary` (`#18150e`), ALL CAPS. |
| indicator | có | `Plus` (collapsed) → `Minus` (expanded). 20px, `color.accent.gold`. Icon tự xoay 180° với `motion.duration.fast` 150ms. |
| answer | có khi mở | Body `Lora` serif, 15px, `color.text.secondary` (`#3a3220`), `leading-relaxed`. Tối đa 4 dòng, dài hơn thì rút gọn dưới link "Đọc hướng dẫn đầy đủ". |
| illustration | không | 48×48px bo cong 4px, hiển thị khi mở. |

## 5. Biến thể

Chỉ một biến thể cho landing: `faq-row`. Biến thể tương lai cho app (không nằm trong v1):

- `settings-row`. cùng pattern, font nhỏ hơn (16px), dùng trong app
- `reading-expander`. full-width có ảnh nền, dùng cho giải thích dài về Tứ Trụ

## 6. Trạng thái

| Trạng thái | Câu hỏi | Indicator | Câu trả lời |
|---|---|---|---|
| collapsed | base | `Plus` ở 0° | ẩn |
| hover (collapsed) | `color: #1d3129` | `Plus` dịch sang phải 2px | ẩn |
| focus-visible | outline 2px gold offset 2px trên `<summary>` | `Plus` nguyên | ẩn |
| expanded | base, số thứ tự đổi màu gold và bold | `Minus` | hiện, padding 16px trên/dưới |
| hover (expanded) | base | `Minus` nguyên | nguyên |
| disabled | `color: #7a7050`, `cursor: not-allowed` | greyed | ẩn |

## 7. Animation

| Sự kiện | Hiệu ứng | Thời gian | Easing |
|---|---|---|---|
| Mở câu trả lời | `grid-template-rows: 0fr → 1fr` (auto-height) | 240ms | `cubic-bezier(0.16, 1, 0.3, 1)` |
| Đổi icon | `Plus` ↔ `Minus` crossfade + rotate 180° | 150ms | ease-out |
| Hover số thứ tự | translateX 2px sang phải + đổi màu gold | 120ms | ease-out |

`prefers-reduced-motion: reduce` thu gọn mọi animation xuống 0.01ms nhưng vẫn mở/đóng được.

## 8. Pattern triển khai

Dùng `<details>` và `<summary>` cho FAQ. Phím tắt và screen reader có sẵn, không cần viết lại.

```tsx
<details class="group border-t border-b border-[rgba(154,124,34,0.18)] py-5">
  <summary class="flex items-center gap-4 cursor-pointer list-none [&::-webkit-details-marker]:hidden">
    <span class="text-[#7a7050] group-open:text-[#9a7c22] group-open:font-bold transition-colors duration-150">
      <Phosphor.NumberOne size={14} weight="regular" />
    </span>
    <span class="flex-1 font-display font-bold text-[19.5px] uppercase text-[#18150e] tracking-[0.005em]">
      Ứng dụng hoạt động như thế nào?
    </span>
    <span
      class="text-[#9a7c22] transition-transform duration-150 group-open:rotate-180"
      aria-hidden="true"
    >
      {open
        ? <Phosphor.Minus size={20} weight="bold" />
        : <Phosphor.Plus size={20} weight="bold" />}
    </span>
  </summary>
  <div class="mt-4 ml-9 grid grid-rows-[0fr] group-open:grid-rows-[1fr] transition-[grid-template-rows] duration-240">
    <div class="overflow-hidden">
      <p class="font-serif text-[15px] leading-relaxed text-[#3a3220] max-w-[60ch]">
        Chỉ mất 30 giây để nhập ngày giờ sinh. Hệ thống tính ra lá số Tứ Trụ theo can chi của bạn,
        sau đó mỗi sáng sẽ gửi một trang lịch qua PWA, email và ứng dụng.
      </p>
      <a href="/huong-dan" class="inline-flex items-center gap-1 mt-3 font-mono text-[10.5px] uppercase tracking-[0.18em] text-[#9a7c22] hover:text-[#1d3129] transition-colors duration-120">
        Đọc hướng dẫn đầy đủ <Phosphor.ArrowUpRight size={14} weight="bold" />
      </a>
    </div>
  </div>
</details>
```

Khi cần custom (ví dụ hiển thị ảnh minh họa theo trạng thái), dùng button + `aria-expanded` nhưng **phải** giữ đúng ngữ nghĩa ARIA mà `<details>` cung cấp:

- Trigger: `role="button"`, `aria-expanded`, `aria-controls` trỏ tới panel id
- Panel: `role="region"`, `aria-labelledby` trỏ tới trigger id
- Bàn phím: Enter/Space toggle, ArrowDown tới trigger kế tiếp (khi nhiều trigger cùng group)

## 9. Responsive

- ≥768px: padding `20px` dọc, font câu hỏi 19.5px, indent số thứ tự 36px
- <768px: padding `16px` dọc, font câu hỏi 17.5px, indent số thứ tự 32px, ảnh minh họa ẩn (tiết kiệm không gian)

## 10. Edge cases

- Câu trả lời dài: hiển thị tối đa 4 dòng ở collapsed, mở rộng đầy đủ khi mở. Không cắt bằng max-height animation.
- Mục đầu mở sẵn: chỉ mục 01 mặc định `open`. Các mục sau collapsed.
- Accordion lồng nhau: cấm. Chỉ danh sách phẳng.
- Tìm kiếm (tương lai): nếu filter ẩn mục không khớp, dùng `display: none`, không animate chiều cao.
- Nhiều mục mở đồng thời: cho phép. Không giới hạn.
- Câu hỏi dài: wrap 2 dòng. Indicator giữ phải.
- Đánh số: tuần tự 01–06 ngay cả khi ẩn mục. Không đánh lại.

## 11. Nội dung FAQ chuẩn (brand-locked)

Sáu câu hỏi dưới đây là canonical. Không thêm câu mới nếu không có sự chấp thuận của brand:

| # | Câu hỏi | Icon cảnh báo | Ghi chú |
|---|---|---|---|
| 01 | Ứng dụng hoạt động như thế nào? | không | Câu "an toàn" mở đầu |
| 02 | Lá số Tứ Trụ có chính xác không? | `WarningCircle` (fill đỏ) | Câu nhạy cảm về niềm tin |
| 03 | Hoàn tiền trong 7 ngày thế nào? | không | Phải nêu rõ "100% chi phí, không cần lý do" |
| 04 | Có tự động gia hạn không? | `WarningCircle` (fill đỏ) | Phải nêu "tuyệt đối không auto-renew" |
| 05 | Đồng bộ giữa các thiết bị? | không | PWA, iOS, Android |
| 06 | Tôi không nhớ giờ sinh chính xác? | không | Đưa ra sai số ±2 tiếng được chấp nhận |

## 12. Accessibility (WCAG 2.2 AA)

- `<details>`/`<summary>`: phím Enter/Space và ARIA state (`aria-expanded`) mặc định đúng. Ưu tiên dùng.
- Tuỳ chỉnh: trigger `role="button"`, `aria-expanded`, `aria-controls`. Panel `role="region"`, `aria-labelledby`.
- Tương phản:
  - Câu hỏi `#18150e` trên `#f0ece2`: 14.8:1 ✓ AAA
  - Số thứ tự `#7a7050` trên `#f0ece2`: 4.7:1 ✓ AA (chỉ phụ hoạ)
  - Indicator gold `#9a7c22` trên `#f0ece2`: 5.1:1 ✓ AA
  - Câu trả lời `#3a3220` trên `#f0ece2`: 9.4:1 ✓ AAA
- Vùng bấm: toàn dòng (≥44×44px khi collapsed).
- Bàn phím: Tab di chuyển giữa các trigger. Enter/Space toggle panel.
- Screen reader: thông báo "expanded" / "collapsed" cùng với câu hỏi.

## 13. Checklist QA

- [ ] Dùng `<details>`/`<summary>` hoặc custom đúng ARIA
- [ ] Mục 01 mặc định `open`
- [ ] Icon đổi `Plus` ↔ `Minus`, không xoay 45 độ từ `+`
- [ ] Animation tôn trọng `prefers-reduced-motion`
- [ ] Đánh số tuần tự kể cả khi ẩn
- [ ] Đủ 7 trạng thái (collapsed/hover/focus/expanded/hover-expanded/disabled)
- [ ] Điều hướng bàn phím đầy đủ
- [ ] axe-core scan: 0 vi phạm
- [ ] Không có em-dash (`,`) trong bất kỳ chuỗi nào hiển thị