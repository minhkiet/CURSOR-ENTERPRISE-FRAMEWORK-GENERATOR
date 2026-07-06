# Card

> Container cho nội dung nhóm. Các biến thể đa dạng (calendar page, pricing tier, comparison, feature) chia sẻ ngôn ngữ "giấy in có viền chỉ vàng" và bóng ink-green nhạt.

## 1. Mục đích

Card cho calendar pages, pricing tiers, comparison và feature rows. Cảm giác giấy in rõ ràng: nền trắng hoặc ink, viền chỉ vàng hoặc hairline, bóng ink-green nhẹ.

## 2. Hệ thống icon

| Vai trò | Icon Phosphor | Kích thước |
|---|---|---|
| Action chính (CTA card) | `ArrowUpRight` | 14px |
| Bookmark / lưu | `BookmarkSimple` | 16px |
| Chia sẻ card | `ShareNetwork` | 14px |
| Đóng / xóa | `X` | 14px |
| Verified (đã xác minh) | `SealCheck` (fill) | 14px, gold |
| Loading spinner | `CircleNotch` | 16px |
| Icon đầu feature card | `Star`, `Compass`, `BookOpen`, `Sparkle` (tùy loại) | 28px |

## 3. Hình ảnh và minh họa

Mỗi biến thể card có hình ảnh riêng:

| Variant | Hình nền / thumbnail | Nguồn |
|---|---|---|
| `calendar-page` | Giấy trắng ngà texture | `https://picsum.photos/seed/paper-trang-nga/400/600` |
| `calendar-page-active` | Giấy trắng sáng hơn + vàng nhạt | `https://picsum.photos/seed/paper-do-trang/400/600` |
| `pricing-tier-hero` | Gradient ink + gold-leaf vein pattern | `https://picsum.photos/seed/ink-gold-vein/1200/600` |
| `pricing-tier` | Giấy trắng ngà | `https://picsum.photos/seed/paper-trang-nga/600/400` |
| `comparison` | Side-by-side split background | `https://picsum.photos/seed/comparison-split/800/400` |
| `feature-3up` | Mỗi card icon 64×64 trên nền ivory | icons Phosphor |

Pricing tier hero nên có **ảnh thumbnail cuốn lịch** (96×96px, bo vuông 4px) ở góc trên-phải, lấy từ `https://picsum.photos/seed/lich-to-thumb/96/96`.

Calendar page có thể thêm **ảnh con dấu** (wax seal) cho dịp đặc biệt ở góc trên-trái, xoay -8°.

## 4. Cấu trúc

```
[ eyebrow tag (optional, absolute top-left) ]
[ header section          ]
[ divider (hairline)      ]
[ main content            ]
[ divider (hairline)      ]
[ footer / CTA (optional) ]
```

| Slot | Bắt buộc | Ghi chú |
|---|---|---|
| eyebrow tag | không | Nhãn nhỏ absolute (ví dụ "HÔM NAY"). 9.5px mono, ink text trên gold bg, `radius.lg` (6px). Kèm Phosphor icon (Sun, Star). |
| header | có | Display font, 22.5px (calendar day) hoặc size khác tùy variant. |
| divider | không | `1px solid rgba(154, 124, 34, 0.10)` (hairline). |
| main | có | Body content. |
| footer | không | CTA, giá, status. |

## 5. Biến thể

| Variant | Background | Border | Shadow | Cách dùng |
|---|---|---|---|---|
| `calendar-page` | `#ffffff` | `1px solid rgba(154, 124, 34, 0.10)` | `shadow.card` | Calendar mini-page (today, day cells) |
| `calendar-page-active` | `#ffffff` | `1.5px solid #9a7c22` | `0 24px 48px rgba(0,0,0,0.3)` (sâu hơn) | Today's page trong calendar strip |
| `pricing-tier-hero` | `#1d3129` (ink) | `1.5px solid #c5a55a` | `0 24px 48px rgba(29,49,41,0.25)` | Featured pricing tier |
| `pricing-tier` | `#ffffff` | `1px solid rgba(154, 124, 34, 0.18)` | none (hover: `shadow.card`) | Standard pricing tier |
| `comparison` | `#ffffff` | `1px solid rgba(154, 124, 34, 0.18)` | none | "Bạn vs Người khác" comparison |
| `feature-3up` | `#ffffff` | `1px solid rgba(154, 124, 34, 0.18)` | none | 3-column feature row |
| `testimonial` | `#ffffff` | `1px solid rgba(154, 124, 34, 0.10)` | `shadow.card` nhẹ | Quote từ khách hàng |

## 6. Sizes

| Variant | Padding | Max-width | Min-height |
|---|---|---|---|
| `calendar-page` | 18px × 14px (compact) | 280px (hero), 320px (strip) | 380px (hero), 240px (strip) |
| `calendar-page-active` | 18px × 14px | 280px | 240px |
| `pricing-tier-hero` | 52px × 56px | 1200px container | none |
| `pricing-tier` | 24px | 600px | none |
| `comparison` | 22px | 580px | 380px |
| `feature-3up` | 28px × 24px | 380px | 280px |
| `testimonial` | 32px | 520px | none |

## 7. Trạng thái

| Trạng thái | Thay đổi thị giác |
|---|---|
| default | base |
| hover (calendar-page) | `translateY(-2px)` + shadow sâu hơn |
| hover (pricing-tier) | shadow lift, border `1px solid rgba(154, 124, 34, 0.30)` |
| hover (testimonial) | border `1px solid rgba(154, 124, 34, 0.25)` |
| focus-within (pricing-tier) | outline 2px gold trên container |
| active (today cell) | border `1.5px solid #9a7c22`, shadow sâu hơn |
| loading | skeleton (cùng shape, neutral grey) |
| empty | text căn giữa "Chưa có nội dung", không illustration |

## 8. Calendar page variant. chi tiết

Calendar page là thành phần signature của brand. Luôn giữ cấu trúc:

```
┌─────────────────────────┐
│ Tháng 5 · 2026 · Bính Ngọ │ ← eyebrow (small serif, #7a7050) + YinYang icon
├─────────────────────────┤
│  26      THỨ BA         │ ← day number (96.5px extrabold đỏ) + weekday
├─────────────────────────┤
│  Mùng 10 tháng Tư · ...  │ ← lunar date subtitle (13px serif)
│  ngày Mậu Tuất · tiết... │
├─────────────────────────┤
│  Ngày khô       76/100   │ ← status row (gold tint bg, có icon)
├─────────────────────────┤
│  "Mặc khô vuông dần..."  │ ← proverb quote (italic serif)
└─────────────────────────┘
```

Border: `1px solid rgba(154, 124, 34, 0.18)`. Background: `#ffffff` + paper texture overlay. Padding: 22px (rộng hơn compact calendar page).

### Màu status cho calendar page

| Status | Label color | Score color | Icon |
|---|---|---|---|
| Ngày tốt (auspicious) | `#9a7c22` (gold) | `#9a7c22` | `Sparkle` (fill) |
| Ngày thường (neutral) | `#7a7050` (tertiary) | `#bfae7a` (gold-dim) | `Circle` |
| Ngày không thuận (inauspicious) | `#a3201f` (auspicious đỏ) | `#a3201f` | `Prohibit` (fill) |

## 9. Pricing tier variant. chi tiết

### Hero tier

```
┌─────────────────────────────────────────┐
│ ★ KHUYẾN NGHỊ - TRỌN VẸN NHẤT        │ ← ribbon (gold bg, ink text, top-left)
├─────────────────────────────────────────┤
│ LỊCH ĐỊNH MÙI 2027 · TRỌN NĂM        │ ← eyebrow
│                                          │
│ Lịch bản mệnh                          │ ← title (56.5px display)
│ cho cả năm (italic gold accent)         │
│                                          │
│ ✓ Feature 1                             │
│ ✓ Feature 2                             │
│ ✓ Feature 3                             │
│ ✓ Feature 4                             │
│                                          │
│ [ ĐĂNG KÝ LỊCH NĂM ]                   │ ← CTA button (full-width)
└─────────────────────────────────────────┘
```

Cộng thêm khối giá song song bên phải (column ratio 1.4fr / 1fr):

```
┌──────────────────┐
│ CHI PHÍ ĐỒNG HÀNH│
│                   │
│ 549.000₫          │ ← price (72.5px gold tabular)
│                   │
│ [TIẾT KIỆM 298K] │ ← savings badge với PiggyBank icon
│                   │
│ ─────────────    │
│ Quote: trọn gói...│ ← muted footer note
└──────────────────┘
```

### Standard tier (compact)

```
┌─────────────────────────┐
│ Gói Trải Nghiệm  [3 tháng] │ ← title + duration badge
│                          │
│ Description text...      │ ← 13.5px serif
│                          │
│ ✓ Feature 1              │
│ ✓ Feature 2              │
│ ✓ Feature 3              │
│ ✗ Crossed feature (optional) │
├─────────────────────────┤
│ Chi phí đăng ký:        │
│           99.000₫        │ ← 26.5px gold tabular
│        (3 tháng)         │
└─────────────────────────┘
```

Standard tier là link (`<a href="/dat-lich?plan=goi_3thang">`), styled như card. Cả card clickable.

## 10. Testimonial variant. chi tiết

```
┌───────────────────────────────┐
│ [ portrait 64×64 ]            │
│                              │
│ "Mỗi sáng mở lịch ra đọc    │ ← quote (16px italic serif)
│  câu tục ngữ xong là thấy    │
│  bình tâm hơn hẳn."          │
│                              │
│ ─ Trần Thị M., 47 tuổi, HN │ ← attribution
│ ★★★★★ verified              │
└───────────────────────────────┘
```

Avatar 64×64px bo tròn, dùng ảnh Picsum: `https://picsum.photos/seed/portrait-vn-woman/128/128`.

## 11. Trạng thái (pricing-specific)

### Hero tier

| Trạng thái | Thay đổi |
|---|---|
| default | ribbon hiển thị, CTA enabled |
| hover | ribbon chuyển sang gold sáng hơn (`#d4b366`), CTA shadow sâu hơn, card translate -2px |
| focus-within | outline 2px gold trên card border, offset 4px |
| loading | skeleton: placeholder title, features, price (giữ grid) |
| error | ribbon text "LỖI TẢI", retry button dưới |
| disabled | ribbon muted, CTA disabled với lý do "Đang tạm dừng bán" |

### Standard tier

| Trạng thái | Thay đổi |
|---|---|
| default | border nhạt, không shadow |
| hover | shadow lift, border sẫm `rgba(154, 124, 34, 0.30)`, translate -2px |
| focus-within | outline 2px gold trên card |
| loading | skeleton |
| disabled | text muted, "Hết hàng" overlay |

## 12. Hover transition

| Thuộc tính | Thời gian | Easing |
|---|---|---|
| `transform: translateY(-2px)` | 200ms | `cubic-bezier(0.16, 1, 0.3, 1)` |
| `box-shadow` | 200ms | ease-out |
| `border-color` | 200ms | ease-out |

`prefers-reduced-motion: reduce`: xóa transform transition, giữ color/shadow ở 80ms.

## 13. Responsive

| Breakpoint | Calendar strip | Pricing tiers | Comparison | Testimonial |
|---|---|---|---|---|
| <768px | horizontal scroll | stack 1-col, sticky CTA dưới | stack 1-col | stack 1-col |
| 768–1023px | 3-col grid | 1 hero + 2 standard dưới 2-col | 2-col side by side | 2-col |
| ≥1024px | full 6-col grid | hero full-width trên, 2-col standard dưới | 2-col side by side | 2-col |

## 14. Edge cases

- Content overflow: header truncate ellipsis sau 2 dòng. Body scroll trong card nếu tuyệt đối cần, nhưng tránh bằng sizing đúng.
- Empty calendar page: "Chưa có lá số. [Tạo ngay]" trong page.
- Disabled subscription tier: grey features, "Đã ngừng bán" label, CTA disabled với lý do.
- Ribbon overflow: nếu eyebrow tag quá dài cho card width, truncate bằng ellipsis.
- Pricing tab change: khi user chuyển tab 3/6/12 tháng, không animate giá (dùng opacity fade 200ms thay vì slide).
- Dấu tiếng Việt trong tier title: phải render đúng. Test "Tiết", "Bính", "Mậu".

## 15. Accessibility (WCAG 2.2 AA)

- **Semantic structure**: `<article>` hoặc `<section>` cho cards; không `<div>` đơn thuần.
- **Interactive card** (pricing tier): accessible name. Wrap content trong `<a>` với text mô tả hoặc `aria-label`.
- **Today's calendar page**: announce "Today, day 26, Tuesday, auspicious score 76 out of 100" qua `aria-label`.
- Tương phản:
  - Card bg `#ffffff` với border `rgba(154, 124, 34, 0.10)` trên `#f0ece2`: border ≥3:1 ✓
  - Active cell border `#9a7c22`: ≥3:1 ✓
  - Text trên white card: 14.8:1 ✓ AAA
  - Hero tier text `#ede7d3` trên `#1d3129`: 11.2:1 ✓ AAA
  - Ribbon text `#1d3129` trên `#c5a55a`: 6.4:1 ✓ AA
- Hit area: toàn card interactive ≥44px bất kỳ chiều nào.
- Bàn phím: pricing tier card (link) focusable như một đơn vị. Calendar pages không focusable trừ khi interactive.
- Screen reader: thông báo card content top-bottom. Dùng `aria-labelledby` trỏ tới card title.

## 16. Checklist QA

- [ ] Variant đúng border/shadow tokens
- [ ] Tất cả trạng thái thay đổi thị giác
- [ ] Calendar page status color rules tuân thủ
- [ ] Pricing tier ribbon không tràn card
- [ ] Hover lift dùng `transform: translateY`, không margin-top
- [ ] Dấu tiếng Việt render đúng trong title
- [ ] Active calendar cell border 1.5px
- [ ] Cards stack đúng trên mobile (không scroll ngang ngoài calendar strip)
- [ ] axe-core scan: 0 vi phạm
- [ ] Mỗi testimonial có avatar thật (không div giả)

## 17. Code reference (calendar page)

```tsx
<article
  class={cn(
    'relative bg-white text-left overflow-hidden transition-all duration-200',
    isToday
      ? 'border-[1.5px] border-[#9a7c22] shadow-[0_24px_48px_rgba(0,0,0,0.3)] hover:shadow-[0_32px_64px_rgba(0,0,0,0.35)]'
      : 'border border-[rgba(154,124,34,0.10)] shadow-[0_8px_18px_rgba(0,0,0,0.1)] hover:shadow-[0_16px_32px_rgba(0,0,0,0.14)] hover:-translate-y-0.5',
  )}
  aria-label={isToday ? `Hôm nay, ngày ${day} ${weekday}, điểm ${score}/100` : undefined}
  style={{ backgroundImage: 'url(https://picsum.photos/seed/paper-trang-nga/400/600)', backgroundBlendMode: 'multiply' }}
>
  {isToday && (
    <div class="absolute -top-2.5 left-3.5 z-10 inline-flex items-center gap-1.5 px-2.5 py-0.5 bg-[#c5a55a] text-[#1d3129] rounded-[6px] shadow-[0_4px_10px_rgba(197,165,90,0.3)]">
      <Phosphor.Sun size={10} weight="fill" aria-hidden="true" />
      <span class="font-mono text-[9.5px] font-extrabold tracking-[0.18em]">HÔM NAY</span>
    </div>
  )}
  <div class="px-[18px] pt-3.5 pb-1.5 border-b border-[rgba(154,124,34,0.10)]">
    <span class="inline-flex items-center gap-1.5 font-serif text-[11.5px] text-[#7a7050]">
      <Phosphor.YinYang size={11} weight="bold" class="text-[#9a7c22]" aria-hidden="true" />
      Tháng 5 · 2026 · Bính Ngọ
    </span>
  </div>
  <div class="px-[18px] py-3.5 flex items-end gap-3">
    <div class="font-display font-extrabold text-[96.5px] leading-[0.85] tabular-nums text-[#a3201f]">
      {day}
    </div>
    <div class="pb-3 font-display font-extrabold text-[22.5px] uppercase leading-[0.95] text-[#a3201f]">
      {weekday}
    </div>
  </div>
  <div class="px-[18px] py-3.5 flex justify-between items-baseline border-t border-[rgba(154,124,34,0.10)] bg-[rgba(154,124,34,0.05)]">
    <div class="flex items-center gap-2">
      {status === 'tot' && <Phosphor.Sparkle size={14} weight="fill" class="text-[#9a7c22]" aria-hidden="true" />}
      {status === 'thuong' && <Phosphor.Circle size={12} weight="bold" class="text-[#7a7050]" aria-hidden="true" />}
      {status === 'xau' && <Phosphor.Prohibit size={14} weight="fill" class="text-[#a3201f]" aria-hidden="true" />}
      <span class="font-display font-extrabold text-[13.5px] uppercase text-[#9a7c22]">Ngày khô</span>
    </div>
    <span class="font-display font-extrabold text-[22.5px] tabular-nums text-[#9a7c22]">{score}</span>
  </div>
</article>

{/* Testimonial card với avatar thật */}
<article class="bg-white border border-[rgba(154,124,34,0.10)] p-8 shadow-[0_8px_18px_rgba(0,0,0,0.06)] hover:shadow-[0_16px_32px_rgba(0,0,0,0.1)] hover:-translate-y-0.5 transition-all duration-200">
  <div class="flex items-start gap-4">
    <img src="https://picsum.photos/seed/portrait-vn-woman-47/128/128" alt="" aria-hidden="true" class="w-16 h-16 rounded-full object-cover ring-2 ring-[#9a7c22] ring-offset-2 ring-offset-white" />
    <div class="flex-1">
      <div class="flex items-center gap-1 text-[#9a7c22] mb-2" aria-label="Đánh giá 5 trên 5 sao">
        {[1, 2, 3, 4, 5].map(i => <Phosphor.Star key={i} size={14} weight="fill" aria-hidden="true" />)}
      </div>
      <Phosphor.Quotes size={20} weight="fill" class="text-[#9a7c22] opacity-30 mb-2" aria-hidden="true" />
      <p class="font-serif italic text-[15px] leading-relaxed text-[#3a3220] m-0">
        "Mỗi sáng mở lịch ra đọc câu tục ngữ xong là thấy bình tâm hơn hẳn."
      </p>
      <footer class="mt-4 pt-3 border-t border-[rgba(154,124,34,0.10)] flex items-center justify-between">
        <span class="font-mono text-[10.5px] uppercase tracking-[0.18em] text-[#7a7050]">
          Trần Thị M., 47 tuổi, Hà Nội
        </span>
        <span class="inline-flex items-center gap-1 text-[10.5px] font-mono uppercase tracking-[0.18em] text-[#9a7c22]">
          <Phosphor.SealCheck size={12} weight="fill" aria-hidden="true" />
          Verified
        </span>
      </footer>
    </div>
  </div>
</article>
```