# Calendar Page

> Thành phần thị giác chủ đạo của brand. Mỗi "trang lịch tờ" là một thẻ dọc hiển thị lá số Tứ Trụ của một ngày. Luôn đọc `card.md` trước để nắm quy tắc card chung.

## 1. Mục đích

Hiển thị lá số một ngày theo định dạng trang lịch tear-off cổ điển. Trang có 5 phần: header (dải ngày tháng), hero (số ngày + thứ), subtitle (ngày âm), status (điểm cát hung), footer (câu tục ngữ).

## 2. Hệ thống icon

| Vai trò | Icon Phosphor | Kích thước |
|---|---|---|
| Can chi năm (header) | `YinYang` | 14px, gold |
| Tiết khí (lunar term) | `Leaf` | 12px, jade `#7a9a80` |
| Giờ hoàng đạo | `Clock` | 12px, gold |
| Ngày tốt (auspicious) | `Sparkle` (fill) | 14px, gold |
| Ngày trung bình (neutral) | `Circle` (stroke) | 12px, tertiary |
| Ngày xấu (inauspicious) | `Prohibit` | 14px, đỏ `#a3201f` |
| Hướng xuất hành | `Compass` | 16px, gold |
| Sao tốt | `Star` (fill) | 10px, gold |
| Sao xấu | `MinusCircle` (fill) | 10px, đỏ |
| Bookmark (lưu ngày quan trọng) | `BookmarkSimple` | 16px |
| Chia sẻ | `ShareNetwork` | 14px |

Header dùng `YinYang` để thay thế dấu chấm giữa "Tháng 5 · 2026 · Bính Ngọ", tạo cảm giác nghi lễ mà không phải emoji.

## 3. Hình ảnh và minh họa

Calendar page chính là "ảnh" của brand. Mỗi biến thể có hình nền riêng:

| Biến thể | Hình nền | Nguồn |
|---|---|---|
| `hero` | Giấy dó texture, có vết ố vintage nhẹ | `https://picsum.photos/seed/paper-do-vintage/600/800` |
| `hero` (dịp lễ) | Họa tiết hoa đào / hoa mai nhạt | `https://picsum.photos/seed/hoa-dao-tet/600/800` |
| `strip` | Giấy trắng ngà với họa tiết viền mảnh | `https://picsum.photos/seed/paper-trang-nga/400/300` |
| `detail` (app) | Giấy kraft nhẹ, có góc gấp | `https://picsum.photos/seed/paper-kraft-detail/800/1200` |

Ảnh dùng làm `background-image` với `opacity: 0.06` overlay. Lớp text và border đặt trên, giữ độ tương phản WCAG AA.

Hình minh họa nhỏ (icon trang trí) cho các phần:
- **Hướng xuất hành**: la bàn mini 24×24px dùng `<Phosphor.Compass />` ở góc trên-phải status row.
- **Sao tốt/xấu**: 8 ô vuông nhỏ (12×12px) đặt cạnh status label. Dùng Phosphor icons thay vì chữ "Tốt/Xấu".

## 4. Cấu trúc

```
┌────────────────────────────────────┐
│ THÁNG 5 · 2026 · Bính Ngọ        │ ← eyebrow (11.5px serif + YinYang icon)
├────────────────────────────────────┤
│                                    │
│  26           THỨ BA              │ ← day + weekday (96.5px extrabold đỏ)
│                                    │
├────────────────────────────────────┤
│  Mùng 10 tháng Tư · ngày Mậu Tuất│ ← lunar date (13px serif)
│  Tiết: Lập Hạ · Giờ: Thìn (7-9h) │
├────────────────────────────────────┤
│  ✦ NGÀY KHÔ              76/100   │ ← status row (gold tint bg)
│  ⌖ Hướng xuất hành: Đông Nam     │
├────────────────────────────────────┤
│  "Mặc khô vuông dần trưa,        │ ← proverb (italic serif)
│   hợp kỵ kết và mở việc."        │
└────────────────────────────────────┘
```

| Slot | Kích thước | Căn chỉnh |
|---|---|---|
| Eyebrow row | full-width, 1px bottom border (hairline gold) | trái, padding-bottom 6px |
| Day + weekday row | 2-col, số ngày trái (96.5px), thứ phải (22.5px) | bottom-aligned |
| Lunar date row | full-width | trái, 2 dòng (ngày âm + tiết khí) |
| Status row | 2-col, label trái + score phải | baseline-aligned, gold tint bg |
| Direction row | full-width | trái, dùng icon Compass |
| Proverb row | full-width | trái, italic, quote marks |

Vertical padding giữa các row: 14px.

## 5. Biến thể

| Biến thể | Kích thước | Cách dùng |
|---|---|---|
| `hero` (full) | 320px × 440px | Hero stack (đầu landing) |
| `strip` (compact) | 280px × 240px | Calendar strip (3-up "Lịch" section) |
| `mini-grid` | 1px cell | Mini overview 12 tháng |
| `detail` (in-app) | full-width card | App surface, drill-down view |

File này cover `hero` và `strip`. `mini-grid` ở `calendar-strip.md`. `detail` dành cho app authenticated.

## 6. Sizes. token usage

| Element | Token | Giá trị |
|---|---|---|
| Card outer padding | `space.6` (custom 22px) | 22px |
| Card border | `1px solid rgba(154, 124, 34, 0.18)` | hairline gold |
| Card border (today) | `1.5px solid #9a7c22` | active gold |
| Eyebrow font | `font.size.xs` (12.5px serif, `#7a7050`) | tertiary |
| Day number | `font.size.calendarDay` (96.5px hero / 76.5px strip extrabold đỏ `#a3201f`) | đỏ mực |
| Weekday | `font.size.h3` (22.5px display extrabold uppercase đỏ `#a3201f`) | đỏ mực |
| Lunar date | `font.size.sm` (13px serif, `#7a7050`) | tertiary |
| Status label | `font.size.lg` (13.5px display extrabold uppercase, màu theo status) | status-color |
| Score | `font.size.h3` (22.5px display extrabold, màu theo status) | status-color |
| Direction icon | Phosphor Compass 16px | gold |
| Proverb | `font.size.md` (13px italic serif, `#3a3220`) | secondary |

## 7. Status color rules

| Status | Label color | Score color | Background tint | Icon Phosphor |
|---|---|---|---|---|
| Ngày tốt (auspicious, score ≥75) | `#9a7c22` | `#9a7c22` | `rgba(154, 124, 34, 0.05)` | `Sparkle` (fill) |
| Ngày thường (neutral, 50–74) | `#7a7050` | `#bfae7a` | none | `Circle` |
| Ngày không thuận (inauspicious, <50) | `#a3201f` | `#a3201f` | `rgba(163, 32, 31, 0.04)` | `Prohibit` (fill) |

Chỉ 3 status. Thêm status mới cần brand approval.

## 8. Hero stack. trang trí

Section hero hiển thị xấp 5–6 trang lịch xếp chồng, xoay các góc khác nhau, một trang đầu ở opacity 100%, các trang sau ở opacity giảm dần.

```
   ╱╱╱╱╱ Trang 1 (sau) ╱╱╱╱╱
  ╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱
 ╱╱╱ Trang 2 (xoay nhẹ) ╱╱╱
 ╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱
 ╱╱ Trang 3 (đầu, full opacity) ╱╱
  ╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱
```

| Layer | Transform | Opacity | Shadow |
|---|---|---|---|
| Trang 1 (xa nhất) | `rotate(10deg) translateX(20px)` | 0.7 | `0 8px 18px rgba(0,0,0,0.1)` |
| Trang 2 | `rotate(-6deg) translateY(-4px)` | 0.85 | `0 8px 18px rgba(0,0,0,0.1)` |
| Trang 3 | `rotate(-3deg) translateY(-2px)` | 0.95 | `0 12px 24px rgba(0,0,0,0.12)` |
| Trang 4 | `rotate(5deg)` | 1 | `0 16px 32px rgba(0,0,0,0.14)` |
| Trang 5 | `rotate(8deg) translateX(-8px)` | 1 | `0 20px 40px rgba(0,0,0,0.16)` |
| Trang 6 (đầu) | `rotate(-2deg) scale(1.0)` | 1 | `shadow.inkLg` |

Trang đầu có badge "365 TRANG · CẢ NĂM" ở góc trên-phải với icon `BookOpen`.

Stack này **chỉ trang trí**. không tương tác, không có ý nghĩa accessibility ngoài `aria-label="Minh họa lịch tờ 365 ngày"` trên wrapper.

## 9. Trạng thái

| Trạng thái | Thay đổi thị giác |
|---|---|
| default | base |
| hover | `translateY(-2px) rotate(0)` (cân bằng), shadow sâu hơn |
| focus-within | outline 2px gold trên card |
| active (today) | border `1.5px solid #9a7c22`, shadow sâu hơn, "HÔM NAY" ribbon |
| loading | skeleton với placeholder lines cho mỗi row |
| empty (không có reading) | text căn giữa "Chưa có lá số. Tạo ngay." |

## 10. Active cell

Trong calendar strip, cell "active" (hôm nay) có:

1. Border `1.5px solid #9a7c22`
2. Scale `scale(1.03)` nhẹ để thu hút mắt
3. Shadow `0 24px 48px rgba(0,0,0,0.3)` sâu hơn
4. "HÔM NAY" ribbon với `Sun` icon top-left
5. Nền `#ffffff` (vs muted `#ede7d3` cho inactive)
6. "Bookmark" icon nhỏ ở góc trên-phải

## 11. Responsive

| Breakpoint | Hero | Strip |
|---|---|---|
| <768px | 1 cột, không fan stack (chỉ trang đầu) | horizontal scroll, snap |
| 768–1023px | hero stack đơn giản (3 trang, 1 đầu) | 3-col grid |
| ≥1024px | full fan stack (6 trang, 1 đầu) | 3-col grid |

## 12. Edge cases

- Dấu tiếng Việt dài ("Khánh Hòa", "Bính Ngọ"): giữ nguyên Unicode. Test font rendering.
- Lunar-solar mismatch: hiển thị cả hai. Format `Dương: 26/5 · Âm: 10/4`.
- Score tràn: scores là 0–100, hiển thị `76/100`. Nếu decimal (76.5), hiển thị `76` (round down).
- Cross-day rollover: khi user mở lúc 00:00, page refresh tự động.
- Empty data: nếu lá số chưa có, hiển thị "Chưa có lá số" thay vì broken cells.
- Out-of-range dates: "Ngày ngoài phạm vi" với status greyed out.
- Festival đặc biệt (Tết, Trung Thu): nếu áp dụng, thay status row bằng tên lễ + ribbon. Luôn giữ layout số ngày.

## 13. Accessibility (WCAG 2.2 AA)

- **Single calendar page** (interactive): wrap trong `<button>` hoặc `<a>` nếu clickable. Cung cấp `aria-label="Ngày {day} tháng {month}, {status}, điểm {score}/100"`.
- **Static display**: wrap trong `<article>` với cùng `aria-label`.
- **Decorative hero stack**: wrapper `role="presentation"` hoặc `aria-hidden="true"`. Không đưa vào screen-reader navigation.
- **Status truyền đạt bằng màu + text + icon**: không bao giờ chỉ màu. Status text ("Ngày khô", "Không thuận") và icon Phosphor kèm theo màu.
- Tương phản:
  - Số ngày đỏ `#a3201f` trên trắng: 5.9:1 ✓ AA
  - Score gold trên trắng `#9a7c22`: 5.1:1 ✓ AA
  - Tertiary `#7a7050` trên trắng: 5.4:1 ✓ AA
  - Status row bg `rgba(154, 124, 34, 0.05)` là trang trí, không cần contrast
- Touch target: khi interactive, card ≥44px.
- Bàn phím: focusable chỉ khi interactive. Tab di chuyển giữa các page interactive.
- Screen reader: thông báo ngày, ngày âm, status, score trong một announcement.

## 14. Checklist QA

- [ ] Số ngày dùng `tabular-nums`
- [ ] Ngày âm và dương cùng hiển thị
- [ ] Status màu + text + icon luôn đi cùng
- [ ] Active cell border 1.5px
- [ ] Hero stack wrapper `role="presentation"` hoặc `aria-hidden`
- [ ] Single page interactive có `aria-label`
- [ ] Dấu tiếng Việt render đúng
- [ ] Score 0–100, hiển thị số nguyên
- [ ] Reduced-motion: không animation xoay
- [ ] axe-core scan: 0 vi phạm
- [ ] Có icon Phosphor ở status row và direction row

## 15. Code reference (strip variant)

```tsx
<article
  class="relative bg-white text-left border border-[rgba(154,124,34,0.10)] shadow-[0_8px_18px_rgba(0,0,0,0.1)] hover:shadow-[0_16px_32px_rgba(0,0,0,0.14)] hover:-translate-y-0.5 transition-all duration-200 overflow-hidden"
  aria-label={`Ngày ${day} tháng ${month}, ${statusLabel}, điểm ${score}/100`}
  style={{ backgroundImage: 'url(https://picsum.photos/seed/paper-trang-nga/400/300)', backgroundBlendMode: 'multiply' }}
>
  {isToday && (
    <div class="absolute -top-2.5 left-3.5 z-10 inline-flex items-center gap-1.5 px-2.5 py-0.5 bg-[#c5a55a] text-[#1d3129] rounded-[6px] shadow-[0_4px_10px_rgba(197,165,90,0.3)]">
      <Phosphor.Sun size={10} weight="fill" aria-hidden="true" />
      <span class="font-mono text-[9.5px] font-extrabold tracking-[0.18em]">HÔM NAY</span>
    </div>
  )}
  {isToday && (
    <button class="absolute top-2.5 right-2.5 text-[#9a7c22] hover:text-[#1d3129] transition-colors duration-150" aria-label="Lưu ngày này">
      <Phosphor.BookmarkSimple size={16} weight="bold" />
    </button>
  )}
  <div class="relative px-[18px] pt-3.5 pb-1.5 border-b border-[rgba(154,124,34,0.10)]">
    <span class="inline-flex items-center gap-1.5 font-serif text-[11.5px] text-[#7a7050]">
      <Phosphor.YinYang size={12} weight="bold" aria-hidden="true" />
      Tháng {month} · {year} · {canChiYear}
    </span>
  </div>
  <div class="px-[18px] py-3.5 flex items-end gap-3">
    <div class="font-display font-extrabold text-[96.5px] leading-[0.85] tabular-nums text-[#a3201f] tracking-[-0.045em]">
      {day}
    </div>
    <div class="pb-3 font-display font-extrabold text-[22.5px] uppercase leading-[0.95] text-[#a3201f]">
      {weekday}
    </div>
  </div>
  <div class="px-[18px] py-3.5 border-t border-[rgba(154,124,34,0.10)]">
    <span class="font-serif text-[12.5px] text-[#7a7050] block">
      Mùng {lunarDay} tháng {lunarMonth} · ngày {lunarCanChiDay}
    </span>
    <span class="font-serif text-[11.5px] text-[#7a7050] inline-flex items-center gap-1 mt-1">
      <Phosphor.Leaf size={11} weight="bold" class="text-[#7a9a80]" aria-hidden="true" />
      Tiết: {tietKhi} · Giờ: {gioiHoangDao}
    </span>
  </div>
  <div class="px-[18px] py-3 flex justify-between items-baseline border-t border-[rgba(154,124,34,0.10)] bg-[rgba(154,124,34,0.05)]">
    <div class="flex items-center gap-2">
      {status === 'tot' && <Phosphor.Sparkle size={14} weight="fill" class="text-[#9a7c22]" aria-hidden="true" />}
      {status === 'thuong' && <Phosphor.Circle size={12} weight="bold" class="text-[#7a7050]" aria-hidden="true" />}
      {status === 'xau' && <Phosphor.Prohibit size={14} weight="fill" class="text-[#a3201f]" aria-hidden="true" />}
      <span class="font-display font-extrabold text-[13.5px] uppercase text-[#9a7c22]">{statusLabel}</span>
    </div>
    <span class="font-display font-extrabold text-[22.5px] tabular-nums text-[#9a7c22]">{score}</span>
  </div>
  <div class="px-[18px] py-2.5 border-t border-[rgba(154,124,34,0.10)] inline-flex items-center gap-1.5">
    <Phosphor.Compass size={13} weight="bold" class="text-[#9a7c22]" aria-hidden="true" />
    <span class="font-serif text-[11.5px] text-[#3a3220]">Hướng xuất hành: <strong class="text-[#9a7c22]">{huongXuatHanh}</strong></span>
  </div>
  <div class="px-[18px] pt-3 pb-4 border-t border-[rgba(154,124,34,0.10)]">
    <p class="font-serif italic text-[12.5px] leading-[1.55] text-[#3a3220] m-0">
      <span class="text-[#9a7c22] not-italic font-display mr-1">"</span>
      {proverb}
      <span class="text-[#9a7c22] not-italic font-display ml-1">"</span>
    </p>
  </div>
</article>
```