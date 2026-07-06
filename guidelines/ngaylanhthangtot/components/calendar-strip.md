# Calendar Strip

> Lưới mini 12 tháng trong section "Từng tuần bản mệnh". Mỗi cell là chỉ báo trạng thái nhỏ cho một ngày. Luôn đọc `calendar-page.md` và `card.md` cho quy tắc liên quan.

## 1. Mục đích

Hiển thị cả năm ở một cái nhìn. Strip có 12 thẻ tháng xếp lưới 6×2 (desktop) hoặc stack dọc (mobile). Mỗi tháng chứa 28–31 ô ngày tô màu theo trạng thái.

## 2. Hệ thống icon

| Vai trò | Icon Phosphor | Kích thước |
|---|---|---|
| Eyebrow tháng | `Calendar` | 10px |
| Tháng hiện tại | `Dot` (fill gold) | 8px đặt cạnh tên tháng |
| Filter mở rộng | `DotsThreeVertical` | 14px |
| Sao tốt (chú thích) | `Sparkle` (fill) | 11px, gold |
| Sao trung bình | `Circle` | 11px, gold-dim |
| Sao xấu | `Prohibit` | 11px, đỏ |
| Click để drill-down | `ArrowUpRight` | 12px |

Không dùng emoji đánh số tháng (`1️⃣`, `🈷️`). Phosphor `Calendar` + dot indicator cho tháng hiện tại.

## 3. Hình ảnh và minh họa

Mỗi tháng có thể có **ảnh nền rất nhẹ** (pattern họa tiết tháng):

| Tháng | Pattern | Nguồn |
|---|---|---|
| Tháng 1 (Tết) | Hoa mai vàng rơi nhẹ | `https://picsum.photos/seed/hoa-mai-vang/120/120` |
| Tháng 2 | Lá vàng | `https://picsum.photos/seed/la-vang-thu/120/120` |
| Tháng 3 | Hoa đào hồng | `https://picsum.photos/seed/hoa-dao-hong/120/120` |
| Tháng 4 | Cỏ xanh mùa hạ | `https://picsum.photos/seed/co-xuan/120/120` |
| Tháng 5 | Nắng vàng | `https://picsum.photos/seed/nang-vang/120/120` |
| Tháng 6 | Sen hồng | `https://picsum.photos/seed/ sen-trang/120/120` |
| Tháng 7 | Sấm sét mùa mưa | `https://picsum.photos/seed/mua-he/120/120` |
| Tháng 8 | Trăng rằm | `https://picsum.photos/seed/trang-ram/120/120` |
| Tháng 9 | Lá phong đỏ | `https://picsum.photos/seed/la-phong-do/120/120` |
| Tháng 10 | Dã quỳ | `https://picsum.photos/seed/da-quy-vang/120/120` |
| Tháng 11 | Sương mù buổi sáng | `https://picsum.photos/seed/suong-mu/120/120` |
| Tháng 12 | Tuyết đầu mùa | `https://picsum.photos/seed/tuyet-dau-mua/120/120` |

Pattern dùng làm `background-image` với `opacity: 0.04` overlay. Tăng nhận diện tháng mà không phá hệ thống màu status.

## 4. Cấu trúc

```
┌──────────────────┐
│ THÁNG 5 •         │ ← month eyebrow (9.5px mono + Calendar icon)
│ Giêng             │ ← month name (14px display extrabold uppercase)
├──────────────────┤
│ ■ ■ ■ ■ ■ ■ ■    │
│ ■ ■ ■ ■ ■ ■ ■    │ ← 28–31 day cells (1px squares)
│ ■ ■ ■ ■ ■ ■ ■    │
│ ■ ■ ■ ■          │
└──────────────────┘
```

| Slot | Bắt buộc | Ghi chú |
|---|---|---|
| month-eyebrow | có | "THÁNG {n}" mono 9.5px + `Calendar` icon Phosphor 10px |
| month-name | có | Tên tháng âm lịch (Giêng, Hai, Ba...) 14px display extrabold uppercase |
| status-dot | không | `Dot` (fill gold) cạnh tháng hiện tại |
| day-grid | có | 28–31 ô vuông 1px bo 1px, màu theo score |
| legend | có | 3 ô màu + text dưới grid |

## 5. Biến thể

| Biến thể | Container | Cell | Cách dùng |
|---|---|---|---|
| `inactive` | 100% | 1px squares, `bg: #ede7d3`, `opacity: 0.55` cho non-today | Standard month display |
| `active` (current month) | 100%, `scale(1.0)` highlight | 1px squares, full opacity, white bg, gold border | Current month |

Tháng hiện tại (tháng 5 trong ví dụ 2026) được highlight với `border-[1.5px] border-[#9a7c22]` + `Dot` gold indicator cạnh tên tháng.

## 6. Day cell. color rules

Mỗi ô ngày là hình vuông 1px (`aspect-ratio: 1/1`, `border-radius: 1px`) tô màu theo score:

| Score range | Màu | Opacity (inactive months) | Icon Phosphor tương ứng |
|---|---|---|---|
| 0–30 (rất xấu) | `#a3201f` (đỏ) | 0.55 | `Prohibit` (fill) |
| 31–50 (xấu) | `#7a7050` (tertiary grey) | 0.55 | `XCircle` |
| 51–74 (trung bình) | `#bfae7a` (gold-dim) | 0.55 | `Circle` |
| 75–89 (tốt) | `#7a9a80` (jade) | 0.55 | `Sparkle` |
| 90–100 (rất tốt) | `#9a7c22` (gold) | 0.55 | `Sparkle` (fill) |

Tháng active dùng `opacity: 1` cho tất cả cells.

## 7. Sizes

| Token | Giá trị |
|---|---|
| Month card padding | 12px |
| Month eyebrow font | 9.5px mono uppercase, `#7a7050` |
| Month title font | 14px display extrabold uppercase, `#3a3220` (inactive) / `#18150e` (active) |
| Cell size | aspect-square, 1px radius |
| Cell gap | 2px |

## 8. Grid layout

| Breakpoint | Layout | Columns |
|---|---|---|
| <768px | horizontal scroll, snap to each month | 1-col stack, scroll ngang |
| 768–1023px | 3-col grid | 3 cols × 4 rows |
| ≥1024px | 6-col grid | 6 cols × 2 rows |

## 9. Trạng thái

| Trạng thái | Thay đổi thị giác |
|---|---|
| default | inactive months: muted cells, current month highlighted |
| hover (month card) | `translateY(-2px)`, shadow xuất hiện |
| focus-within (interactive) | outline 2px gold trên month card |
| loading | skeleton với placeholder cell grid (mỗi cell `#ede7d3`) |

V1 month cards KHÔNG tương tác (chỉ hiển thị). Nếu interactive v2, wrap mỗi month trong `<a>` dẫn tới monthly detail.

## 10. Edge cases

- Leap year February: 29 cells (không phải 28).
- Lunar new year overlap: nếu tháng bắt đầu giữa tuần, leading cells của row đầu là empty (`bg: transparent`). Implement empty cells trong grid.
- Tất cả tốt / tất cả xấu: khối màu đơn điệu. Để tránh gây hiểu nhầm, thêm tooltip hoặc label giải thích.
- Empty data (user chưa có lá số): grid màu `#ede7d3` với overlay text "Tạo lá số để xem lịch năm" + `Sparkle` icon.
- Current day highlight (active month only): cell tương ứng ngày hôm nay dùng `border: 1.5px solid #18150e` để nổi bật.
- Year boundary: strip hiển thị năm hiện tại. Năm cũ cần query riêng (ngoài scope v1).

## 11. Accessibility (WCAG 2.2 AA)

- **Wrapper structure**: `<section>` với `aria-labelledby="year-overview-title"`. Title đầu section: "Từng tuần bản mệnh".
- **Month card**: `<div role="group" aria-label="Tháng 5, 30 ngày, 18 ngày tốt, 8 ngày thường, 4 ngày không thuận">`.
- **Day cells**: không focusable riêng. Status truyền đạt bằng màu, summary text qua `aria-label` của month card.
- **Màu không đứng một mình**: thêm legend text dưới grid (xem section 12).
- Tương phản:
  - Inactive card border (none) trên `#f0ece2` paper
  - Active card border `#9a7c22` trên trắng: 5.1:1 ✓ AA (UI component)
  - Month title `#18150e` trên trắng: 14.8:1 ✓ AAA
  - Eyebrow `#7a7050` trên trắng: 5.4:1 ✓ AA
  - Cell màu là trang trí; không cần đạt contrast
- Bàn phím: không focusable mỗi tháng v1. Nếu v2, mỗi month card cần keyboard support đầy đủ.
- Screen reader: thông báo section title, rồi month summary. Legend cũng được thông báo.

## 12. Legend bắt buộc

Dưới grid, render legend inline nhỏ:

```tsx
<div class="flex items-center gap-5 mt-6 font-mono text-[11px] text-[#7a7050]">
  <span class="flex items-center gap-1.5">
    <Phosphor.Sparkle size={11} weight="fill" class="text-[#9a7c22]" aria-hidden="true" />
    <span>Ngày tốt (75–100)</span>
  </span>
  <span class="flex items-center gap-1.5">
    <Phosphor.Circle size={11} weight="bold" class="text-[#bfae7a]" aria-hidden="true" />
    <span>Trung bình (51–74)</span>
  </span>
  <span class="flex items-center gap-1.5">
    <Phosphor.Prohibit size={11} weight="fill" class="text-[#a3201f]" aria-hidden="true" />
    <span>Không thuận (≤50)</span>
  </span>
</div>
```

Đơn giản hóa còn 3 bucket cho screen-reader clarity, nhưng cell màu thực tế dùng 5 bucket. Legend dùng 3 để rõ thị giác.

## 13. Checklist QA

- [ ] Đúng 12 tháng hiển thị
- [ ] Current month highlight border 1.5px gold + Dot indicator
- [ ] Cell màu theo 5-bucket rules
- [ ] Inactive months dùng opacity 0.55
- [ ] Mobile horizontal scroll với snap
- [ ] Legend hiển thị dưới grid
- [ ] aria-label mỗi tháng có summary stats
- [ ] Wrapper section có aria-labelledby
- [ ] Empty state cho user chưa có lá số
- [ ] Leap year February có 29 cells
- [ ] axe-core scan: 0 vi phạm
- [ ] Legend dùng Phosphor icons, không phải ô vuông đơn điệu

## 14. Code reference

```tsx
<section
  aria-labelledby="year-overview-title"
  class="bg-[#f0ece2] py-24 px-[6vw] border-t border-[rgba(154,124,34,0.18)] relative overflow-hidden"
>
  {/* Decorative pattern background */}
  <div class="absolute inset-0 opacity-[0.025] pointer-events-none" aria-hidden="true">
    <img src="https://picsum.photos/seed/grid-pattern-vintage/200/200" alt="" class="w-full h-full object-cover" />
  </div>

  <div class="relative max-w-[1200px] mx-auto">
    <div class="flex items-baseline gap-3.5 mb-8">
      <span class="inline-flex items-center gap-2 font-mono text-[11.5px] tracking-[0.22em] uppercase text-[#9a7c22]">
        <Phosphor.YinYang size={14} weight="bold" aria-hidden="true" />
        TỪNG TUẦN BẢN MỆNH
      </span>
      <span class="flex-1 h-px bg-[rgba(154,124,34,0.18)]"></span>
    </div>
    <h2 id="year-overview-title" class="font-display font-extrabold uppercase leading-[1.02] max-w-[880px] text-[56.5px] tracking-[-0.02em] text-[#18150e]">
      365 ngày cát hung, <span class="font-serif italic font-bold normal-case text-[#9a7c22]">định vị tứ trụ</span> cho riêng bạn.
    </h2>

    <div class="mt-12 grid gap-4 grid-cols-2 md:grid-cols-3 lg:grid-cols-6">
      {months.map(month => (
        <div
          role="group"
          aria-label={`Tháng ${month.num}, ${month.days} ngày, ${month.goodDays} ngày tốt, ${month.neutralDays} ngày thường, ${month.badDays} ngày không thuận`}
          class={cn(
            'relative p-3 transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_12px_24px_rgba(0,0,0,0.1)] overflow-hidden',
            month.isCurrent
              ? 'bg-white border-[1.5px] border-[#9a7c22] shadow-[0_8px_18px_rgba(154,124,34,0.15)]'
              : 'bg-[#ede7d3] border border-[rgba(154,124,34,0.10)]',
          )}
          style={!month.isCurrent && month.pattern ? { backgroundImage: `url(https://picsum.photos/seed/${month.pattern}/120/120)`, backgroundBlendMode: 'multiply' } : undefined}
        >
          {month.isCurrent && (
            <img src="https://picsum.photos/seed/current-month-bg/200/200" alt="" aria-hidden="true" class="absolute inset-0 w-full h-full object-cover opacity-[0.04] pointer-events-none" />
          )}
          <div class="relative inline-flex items-center gap-1.5">
            <Phosphor.Calendar size={10} weight="bold" class="text-[#7a7050]" aria-hidden="true" />
            <span class="font-mono text-[9.5px] tracking-[0.12em] uppercase text-[#7a7050]">
              Tháng {month.num}
            </span>
            {month.isCurrent && <Phosphor.Dot size={8} weight="fill" class="text-[#9a7c22]" aria-label="Tháng hiện tại" />}
          </div>
          <div class={cn(
            'mt-1 font-display font-extrabold text-sm uppercase tracking-tight',
            month.isCurrent ? 'text-[#18150e]' : 'text-[#3a3220]',
          )}>
            {month.name}
          </div>
          <div class="mt-2 grid gap-0.5 grid-cols-7">
            {month.daysArray.map(day => (
              <span
                class="aspect-square rounded-[1px] transition-opacity duration-200"
                style={`background: ${day.color}; opacity: ${month.isCurrent ? 1 : 0.55}`}
                aria-hidden="true"
              />
            ))}
          </div>
          <div class="relative mt-2 flex items-center justify-between text-[9.5px] font-mono uppercase tracking-wider">
            <span class="text-[#9a7c22]">{month.goodDays} tốt</span>
            <span class="text-[#7a7050]">{month.neutralDays} tb</span>
            <span class="text-[#a3201f]">{month.badDays} xấu</span>
          </div>
        </div>
      ))}
    </div>

    {/* Legend */}
    <div class="mt-8 flex items-center gap-5 font-mono text-[11px] text-[#7a7050]">
      <span class="inline-flex items-center gap-1.5">
        <Phosphor.Sparkle size={11} weight="fill" class="text-[#9a7c22]" aria-hidden="true" />
        Ngày tốt (75–100)
      </span>
      <span class="inline-flex items-center gap-1.5">
        <Phosphor.Circle size={11} weight="bold" class="text-[#bfae7a]" aria-hidden="true" />
        Trung bình (51–74)
      </span>
      <span class="inline-flex items-center gap-1.5">
        <Phosphor.Prohibit size={11} weight="fill" class="text-[#a3201f]" aria-hidden="true" />
        Không thuận (≤50)
      </span>
    </div>
  </div>
</section>
```