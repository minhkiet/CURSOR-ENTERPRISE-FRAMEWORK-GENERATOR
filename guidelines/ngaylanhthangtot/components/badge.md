# Badge

> Nhãn inline để nhấn mạnh, đánh dấu trạng thái, hoặc hiển thị metadata. Hệ thống badge đọc như dấu triện trên trang lịch cổ: nhỏ, sắc, có chủ đích.

## 1. Mục đích

Dùng cho ribbon ("HÔM NAY"), nhãn tiết kiệm ("TIẾT KIỆM 298.000₫"), nhãn thời hạn ("3 tháng"), và đánh dấu ngày ("NGÀY KHÔ"). Badge nâng cao độ tin cậy của nội dung mà không chiếm dụng layout.

## 2. Hệ thống icon

Một số badge có icon dẫn đầu. Tất cả dùng **Phosphor Regular** (`@phosphor-icons/react`), `weight="bold"` cho badge ribbon.

| Vai trò | Icon Phosphor | Ghi chú |
|---|---|---|
| Ribbon "khuyến nghị" | `Star` (fill) | Màu `#1d3129` trên nền gold |
| Badge "hôm nay" | `Sun` (fill) | 12px, gold |
| Tiết kiệm | `PiggyBank` | 12px, màu `#a3201f` |
| Thời hạn (3/6/12 tháng) | `Clock` | 11px, tertiary |
| Ngày khô | `Sparkle` (fill) | 11px, gold |
| Đã hết hạn | `Prohibit` | 12px, đỏ |
| Mới phát hành | `Crown` (fill) | 11px, ink |
| Đang tải | `CircleNotch` (spin) | 12px, tertiary |

## 3. Cấu trúc

```
[ icon-left? ] [ label ]
```

| Slot | Bắt buộc | Ghi chú |
|---|---|---|
| icon-left | không | 11–14px. Phosphor bold hoặc fill tùy tone. |
| label | có | Mono font, uppercase, `tracking-[0.18–0.22em]`. Tiếng Việt giữ nguyên dấu. |
| value-pair | không | Mẫu "LABEL  VALUE" cho kiểu "NGÀY KHÔ 76/100". |

## 4. Biến thể

| Biến thể | Nền | Chữ | Viền | Cách dùng |
|---|---|---|---|---|
| `ribbon-gold` | `#c5a55a` | `#1d3129` | không | Tag "HÔM NAY", ribbon pricing hero, badge tiết kiệm |
| `ribbon-dark` | `#18150e` | `#c5a55a` | không | "365 TRANG · CẢ NĂM" ở hero stack |
| `inline-muted` | `#ede7d3` | `#7a7050` | không | Nhãn thời hạn ("3 tháng"), metadata trung tính |
| `inline-savings` | `rgba(163, 32, 31, 0.06)` | `#a3201f` | không | Badge giảm giá, tiết kiệm |
| `inline-gold-tint` | `rgba(197, 165, 90, 0.12)` | `#c5a55a` | không | Tiết kiệm trên bề mặt tối |
| `seal-red` | `#a3201f` | `#ede7d3` | không | Con dấu đỏ cho sự kiện đặc biệt (Tết, Trung Thu) |
| `seal-jade` | `#7a9a80` | `#1d3129` | không | Con dấu xanh ngọc cho ngày kỷ niệm cá nhân |

## 5. Kích thước

| Token | Padding (x / y) | Font | Cách dùng |
|---|---|---|---|
| `xs` | 8px × 2px | 9px mono black | Nhãn siêu nhỏ (tiết kiệm trên card compact) |
| `sm` | 10px × 2px | 9.5px mono extrabold | "HÔM NAY", "365 TRANG" |
| `md` | 14px × 4px | 10.5px mono extrabold | "KHUYẾN NGHỊ", pricing ribbon |
| `lg` | 12px × 4px | 10.5px mono bold | Section eyebrow tags |

Mặc định là `sm`. Size lớn hơn chỉ dành cho ribbon cần trọng lượng thị giác.

## 6. Typography

- Font: mono `var(--mono)` hoặc `font-family: ui-monospace, "SF Mono", Menlo, monospace`.
- Tracking `letter-spacing: 0.18–0.22em` (uppercase tracking).
- Weight extrabold (800) cho ribbon, bold (700) cho inline metadata.
- Có dấu tiếng Việt: mono fallback phải có dấu (`Menlo`, `DejaVu Sans Mono` đều OK).

## 7. Radius

| Biến thể | Radius |
|---|---|
| Mặc định | `radius.sm` (2px) |
| `seal-red`, `seal-jade` | `radius.md` (6px) cho cảm giác con dấu |
| `ribbon-gold` "HÔM NAY" | `radius.lg` (6px) |
| Legend swatches | `radius.sharp` (1px) |

## 8. Trạng thái

Badge v1 không tương tác. Nếu cần filter dạng chip, dùng component `filter-chip` thay thế.

| Trạng thái | Thay đổi thị giác |
|---|---|
| default | base |
| hover (nếu tương tác) | nền sáng hơn 4%, cursor pointer |
| focus-visible (nếu tương tác) | outline 2px gold offset 2px |
| active (nếu tương tác) | nền tối hơn 4% |
| disabled (nếu tương tác) | opacity 0.45 |

## 9. Hình ảnh và minh họa

Badge không dùng ảnh. Tuy nhiên có thể kết hợp với **con dấu wax seal** (ảnh PNG) cho dịp đặc biệt:

| Dịp | Hình seal | Cách dùng |
|---|---|---|
| Tết Nguyên Đán | Con dấu đỏ "TẾT" với viền vàng | `https://picsum.photos/seed/wax-seal-tet/96/96` |
| Trung Thu | Con dấu vàng "TRUNG THU" | `https://picsum.photos/seed/wax-seal-trung-thu/96/96` |
| Sinh nhật cá nhân | Con dấu đỏ theo can chi năm sinh | Generated per user |

Seal dùng thay cho ribbon `seal-red` khi dịp đặc biệt, đặt góc trên-trái của calendar page, xoay -8°.

## 10. Pattern sử dụng

| Cách dùng | Biến thể | Size | Ví dụ thực |
|---|---|---|---|
| "Hôm nay" trên calendar page | `ribbon-gold` | `lg` | "HÔM NAY" + `Sun` icon |
| Ribbon pricing hero | `ribbon-gold` | `md` | "★ KHUYẾN NGHỊ - TRỌN VẸN NHẤT" + `Star` fill |
| Hero stack badge | `ribbon-dark` | `sm` | "365 TRANG · CẢ NĂM" |
| Duration label | `inline-muted` | `sm` | "3 tháng" + `Clock` icon |
| Savings 6-month | `inline-savings` | `xs` | "TIẾT KIỆM -51.000₫" + `PiggyBank` icon |
| Savings 12-month (dark) | `inline-gold-tint` | `sm` | "TIẾT KIỆM 298.000₫" + `PiggyBank` icon |
| Section eyebrows | `inline-muted` hoặc `inline-gold-tint` (dark) | `sm` | "TỪNG TUẦN BẢN MỆNH" |
| Calendar page auspicious | inline in card, không dùng badge | n/a | "NGÀY KHÔ" + `Sparkle` icon |
| Lễ hội đặc biệt | `seal-red` | `lg` | Con dấu "TẾT" |

## 11. Responsive

- Tất cả biến thể scale tuyến tính theo container.
- Trên mobile, ribbon có thể rút xuống 1 size (`md` → `sm`) nếu sẽ wrap.
- Không bao giờ dùng `xs` một mình, ghép với `sm` tối thiểu.

## 12. Edge cases

- Tiếng Việt dài: badge phải fit 1 dòng. Truncate bằng ellipsis nếu quá dài. Tránh `white-space: nowrap` nếu gây tràn.
- Nhãn rỗng: không render. Skip hoàn toàn.
- Nhiều badge cùng hàng: cách nhau `gap: 6px` (space.1.5). Không xếp dọc trong cùng context.
- Dấu tiếng Việt trong mono font: test "Tiết", "Bính", "Mậu", "Kỷ".
- Số + tiền tệ ("298.000₫"): dùng `font-variant-numeric: tabular-nums` để căn chỉnh chữ số.
- Ribbon absolute: nếu `-top-3`, đảm bảo parent có `position: relative` và padding tránh đè lên nội dung anh em.

## 13. Accessibility (WCAG 2.2 AA)

- Badge trang trí: thêm `aria-hidden="true"`. Không trùng nhãn với văn bản khác trong cùng card.
- Badge thông tin (status, count): cung cấp `aria-label` với nghĩa đầy đủ. Ví dụ: badge "12" với `aria-label="12 trang lịch chưa đọc"`.
- Badge tương tác: phải là `<button>` hoặc `<a>` với accessible name. Kế thừa accessibility của `filter-chip` nếu dùng làm filter.
- Tương phản:
  - `ribbon-gold` (`#1d3129` trên `#c5a55a`): 6.4:1 ✓ AA
  - `ribbon-dark` (`#c5a55a` trên `#18150e`): 6.4:1 ✓ AA
  - `inline-muted` (`#7a7050` trên `#ede7d3`): 3.0:1 ⚠ chỉ UI component, không dùng cho body text
  - `inline-savings` (`#a3201f` trên `rgba(163, 32, 31, 0.06)` over white): 5.9:1 ✓ AA
  - `inline-gold-tint` (`#c5a55a` trên `rgba(197, 165, 90, 0.12)` over `#1d3129`): xác minh ≥4.5:1
  - `seal-red` (`#ede7d3` trên `#a3201f`): 7.5:1 ✓ AA
  - `seal-jade` (`#1d3129` trên `#7a9a80`): 9.2:1 ✓ AAA
- Touch target: không áp dụng v1 (non-interactive). Nếu tương tác, ≥44×44px.

## 14. Checklist QA

- [ ] Đúng biến thể theo bảng cách dùng
- [ ] Tất cả badge dùng mono font + uppercase + tracking
- [ ] Size khớp token (xs/sm/md/lg)
- [ ] Radius theo quy tắc biến thể
- [ ] Dấu tiếng Việt render đúng
- [ ] Badge trang trí có `aria-hidden`
- [ ] Badge thông tin có `aria-label`
- [ ] Không có badge rỗng
- [ ] Không có badge tương tác (dùng `filter-chip` thay)
- [ ] Nhãn tiếng Việt giữ nguyên dấu
- [ ] axe-core scan: 0 vi phạm
- [ ] Không có em-dash (`,`) trong chuỗi hiển thị

## 15. Code reference

```tsx
{/* Ribbon pricing hero với icon Star */}
<div class="absolute -top-3 left-8 inline-flex items-center gap-2 px-3.5 py-1 bg-[#c5a55a] text-[#1d3129] rounded-[2px] shadow-[0_4px_12px_rgba(197,165,90,0.25)]">
  <Phosphor.Star size={11} weight="fill" aria-hidden="true" />
  <span class="font-mono text-[10.5px] font-extrabold tracking-[0.22em]">KHUYẾN NGHỊ · TRỌN VẸN NHẤT</span>
</div>

{/* "Hôm nay" tag với icon Sun */}
<div class="absolute -top-2.5 left-3.5 inline-flex items-center gap-1.5 px-2.5 py-0.5 bg-[#c5a55a] text-[#1d3129] rounded-[6px]">
  <Phosphor.Sun size={10} weight="fill" aria-hidden="true" />
  <span class="font-mono text-[9.5px] font-extrabold tracking-[0.18em]">HÔM NAY</span>
</div>

{/* Duration label với icon Clock */}
<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-[2px] bg-[#ede7d3] text-[#7a7050]">
  <Phosphor.Clock size={10} weight="bold" aria-hidden="true" />
  <span class="font-mono text-[10px] font-extrabold uppercase tracking-wider">3 tháng</span>
</span>

{/* Savings badge với icon PiggyBank */}
<span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-[2px] bg-[rgba(163,32,31,0.06)] text-[#a3201f]">
  <Phosphor.PiggyBank size={11} weight="bold" aria-hidden="true" />
  <span class="font-mono text-[9px] font-black uppercase tracking-wider">Tiết kiệm 51.000₫</span>
</span>

{/* Decorative hero stack */}
<span aria-hidden="true" class="inline-flex items-center gap-2 px-3 py-1.5 bg-[#18150e] text-[#c5a55a] rounded-[2px]">
  <Phosphor.BookOpen size={11} weight="bold" />
  <span class="font-mono text-[9.5px] font-extrabold uppercase tracking-[0.22em]">365 TRANG · CẢ NĂM</span>
</span>

{/* Con dấu lễ hội với hình ảnh */}
<div class="absolute -top-4 -left-4 rotate-[-8deg] w-16 h-16 drop-shadow-[0_4px_8px_rgba(163,32,31,0.3)]">
  <img src="https://picsum.photos/seed/wax-seal-tet/96/96" alt="" aria-hidden="true" class="w-full h-full rounded-full" />
</div>
```