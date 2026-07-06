# Pricing Tier

> Quy tắc giải phẫu riêng cho pricing section. Component này là chuyên biệt của `card.md` với quy tắc cấu trúc mở rộng. Luôn đọc cả hai file khi triển khai.

## 1. Mục đích

Hiển thị gói đăng ký trong section "Bảng giá". Brand có đúng **3 tier**:

1. **Gói Trải Nghiệm**. 3 tháng, 99.000₫
2. **Gói Bán Niên**. 6 tháng, 249.000₫
3. **Lịch bản mệnh (cả năm)**. 12 tháng, 549.000₫ (featured, hero tier)

Thêm tier mới hoặc xóa tier hiện tại là **brand-locked** (§1.5 của root guidelines).

## 2. Hệ thống icon

| Vai trò | Icon Phosphor | Kích thước |
|---|---|---|
| Ribbon "khuyến nghị" | `Star` (fill) | 12px, ink trên gold |
| Feature check (bao gồm) | `Check` (bold) hoặc `CheckCircle` (fill) | 18px, gold |
| Feature excluded | `X` (bold) | 18px, tertiary |
| Tiết kiệm | `PiggyBank` (bold) | 14px, đỏ `#a3201f` |
| Crown (gói premium) | `Crown` (fill) | 24px, gold |
| Verified | `SealCheck` (fill) | 14px, gold |
| Thời hạn | `Clock` | 14px |
| Đồng bộ PWA | `DeviceMobile` + `Laptop` | 14px mỗi cái |
| Hỏi đáp AI | `ChatCircleDots` | 14px |
| Lá số Tứ Trụ | `BookOpen` | 14px |
| Hoàn tiền | `ArrowUUpLeft` | 14px |
| Không auto-renew | `Prohibit` (fill) | 14px, đỏ |
| Đặc quyền Premium | `Crown`, `Sparkle`, `Heart` | 16-24px |
| External link | `ArrowUpRight` | 14px |

## 3. Hình ảnh và minh họa

Pricing section là "ảnh" chính của conversion. Mỗi tier có hình ảnh riêng:

| Tier | Hình ảnh | Nguồn |
|---|---|---|
| Hero (12 tháng) | Cuốn lịch cổ trên bàn gỗ + nến | `https://picsum.photos/seed/cuon-lich-co-ban-go/1200/600` |
| Hero thumbnail | Lịch tờ tear-off 96×96 | `https://picsum.photos/seed/lich-to-tear-off/96/96` |
| Standard 6 tháng | Lịch bìa da nâu | `https://picsum.photos/seed/lich-bia-da-nau/600/400` |
| Standard 3 tháng | Lịch mini để bàn | `https://picsum.photos/seed/lich-mini-de-ban/600/400` |
| Background pattern | Gold-leaf vein pattern, opacity 0.04 | `https://picsum.photos/seed/gold-vein-pattern/200/200` |
| Testimonial avatars | 5 portraits khách 30+ Việt Nam | Picsum seed per name |

Hero tier nên có **ảnh thumbnail cuốn lịch** (96×96px) góc trên-phải và **ảnh testimonial avatar** nhỏ (48×48) ở footer.

## 4. Hệ thống tier visual

Tier 12 tháng chiếm ưu thế thị giác. Nó chiếm full container width dưới dạng 2-col hero card (features trái, giá phải), với tier 3 tháng và 6 tháng là card nhỏ hơn bên dưới.

```
┌─────────────────────────────────────────────────┐
│        HERO: 12-MONTH TIER (full width)         │
├──────────────────────┬──────────────────────────┤
│ Features column      │  Price column            │
│ (1.4fr)              │  (1fr)                   │
└──────────────────────┴──────────────────────────┘
┌──────────────────┐ ┌──────────────────┐
│ 3-MONTH (1fr)    │ │ 6-MONTH (1fr)    │
└──────────────────┘ └──────────────────┘
```

## 5. Hero tier. full anatomy

### Layout

Two-column grid: `grid-template-columns: 1.4fr 1fr` với `gap: 48px` (space.12).

### Features column

| Element | Token | Ghi chú |
|---|---|---|
| Eyebrow | `font.size.eyebrow` (11.5px) mono uppercase, `color.accent.goldBright` | "LỊCH ĐỊNH MÙI 2027 · TRỌN NĂM" |
| Title | `font.size.h3` (56.5px display extrabold uppercase) | "Lịch bản mệnh" + italic gold accent "cho cả năm" |
| Features list | `font.size.lg` (14.5px serif), 4 mục | Mỗi mục: `CheckCircle` (gold) + bold label + description |
| CTA | Button `primary-on-light`, full-width, `lg` size | "ĐĂNG KÝ LỊCH NĂM" + `Crown` icon |

### Price column

| Element | Token | Ghi chú |
|---|---|---|
| Eyebrow | mono uppercase 10.5px, `color.accent.goldBright` | "CHI PHÍ ĐỒNG HÀNH" |
| Price | 72.5px display extrabold tabular-nums, `color.accent.goldBright` | "549.000₫" |
| Savings badge | inline mono pill 10.5px, `bg: rgba(197,165,90,0.12)`, text gold + `PiggyBank` icon | "TIẾT KIỆM 298.000₫ · TỐI ƯU TRỌN VẸN" |
| Quote note | 13px serif, `rgba(237,231,211,0.7)` | "Gói dịch vụ được nhiều quý anh chị trên 30 tuổi tin dùng nhất..." |
| Testimonial mini | Avatar 48×48 + quote 1 dòng | Optional |

### Decorative ribbon

Top-left, absolute positioned, gold background, ink text:

```
- KHUYẾN NGHỊ - TRỌN VẸN NHẤT
```

| Token | Giá trị |
|---|---|
| Background | `#c5a55a` |
| Text | `#1d3129` |
| Font | mono 10.5px extrabold |
| Padding | 14px × 4px |
| Position | absolute, top: -12px, left: 32px |
| Letter-spacing | 0.22em |
| Icon | `Star` (fill) 12px ink |

## 6. Standard tier. full anatomy

Single column card:

| Element | Token | Ghi chú |
|---|---|---|
| Header | Title (22.5px display extrabold) + Duration badge (10px mono, `bg: #ede7d3`, text `#7a7050`, `Clock` icon) | "Gói Trải Nghiệm" + "3 tháng" |
| Description | 13.5px serif, `color.text.secondary` | "Phù hợp cho quý anh chị bước đầu trải nghiệm..." |
| Features list | 13.5px serif, 3 active + 1 struck-through | `CheckCircle` (gold) cho active, `X` (tertiary grey) cho not included |
| Footer | Price label + Price (26.5px display gold tabular-nums) + duration | "Chi phí đăng ký:" + "99.000₫" + "(3 tháng)" |

### Savings badge (chỉ 6-month tier)

```
┌─────────────────────────┐
│ 🐷 TIẾT KIỆM -51.000₫       │ ← inline mono pill 9px black uppercase
└─────────────────────────┘
```

| Token | Giá trị |
|---|---|
| Background | `rgba(163, 32, 31, 0.06)` |
| Text | `#a3201f` (đỏ mực) |
| Font | mono 9px black uppercase |
| Padding | 10px × 2px |
| Radius | 2px |
| Icon | `PiggyBank` 11px đỏ |

## 7. Trạng thái

### Hero tier

| Trạng thái | Thay đổi |
|---|---|
| default | ribbon hiển thị, CTA enabled |
| hover | ribbon chuyển gold sáng hơn (`#d4b366`), CTA shadow sâu, card translate -2px |
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

## 8. Hover transition

| Thuộc tính | Thời gian | Easing |
|---|---|---|
| `transform: translateY(-2px)` | 200ms | `cubic-bezier(0.16, 1, 0.3, 1)` |
| `box-shadow` | 200ms | ease-out |
| `border-color` | 200ms | ease-out |

`prefers-reduced-motion: reduce`: xóa transform transition, giữ color/shadow ở 80ms.

## 9. Responsive

| Breakpoint | Hero tier | Standard tiers |
|---|---|---|
| <768px | features + price stack 1-col, price dưới features | stack 1-col |
| 768–1023px | 1.4fr / 1fr (giống desktop) | 1-col stack |
| ≥1024px | 1.4fr / 1fr | 2-col row |

Trên mobile, savings badge và ribbon vẫn hiển thị nhưng compact. Savings badge của price column có thể wrap nếu container quá hẹp.

## 10. Edge cases

- **Currency formatting**: luôn hiển thị "₫" sau số với dấu chấm phân cách. Không dấu phẩy. Không decimal. Ví dụ: `549.000₫`.
- **Tabular-nums**: giá luôn dùng `font-variant-numeric: tabular-nums` để tránh digit jitter khi đổi locale.
- **Multiple prices**: không bao giờ hiển thị "từ X" (from X) mà không có "đến Y" (to Y) rõ ràng. Mỗi tier hiển thị một giá chính xác.
- **Discount math**: savings 6 tháng là `2 × 99.000 - 249.000 = -51.000₫` (tiết kiệm 51K so với mua 2 lần gói 3 tháng). Savings 12 tháng là `4 × 99.000 - 549.000 = -153.000₫`, nhưng brand hiển thị `298.000₫` (tính trên anchor 12 × 99.000 = 1.188.000₫ - 549.000₫ = 639.000₫). Dùng số brand-locked, không tính lại.
- **Future price changes**: giá chỉ đổi qua brand approval. Cập nhật cả root guidelines và `tokens.json` `price.*` khi đổi.
- **Empty tier (deprecated)**: không hiển thị. Nếu tạm hết, hiển thị "Tạm hết hàng" với CTA disabled và lý do.
- **Subscription auto-renew**: brand KHÔNG auto-renew. Hero tier copy phải bao gồm "tuyệt đối không tự động gia hạn trừ tiền thẻ". Thiếu câu này là vi phạm brand.
- **Refund policy**: hero tier copy phải bao gồm "hoàn trả 100% chi phí trong vòng 7 ngày nếu không hài lòng".

## 11. Copy hero tier bắt buộc (brand-locked)

Hero tier PHẢI bao gồm 4 features:

1. **365 ngày Lịch bản mệnh Tứ Trụ** (icon `BookOpen`). điểm số cát hung + thời khắc hành sự đại sự theo chuẩn cổ thư Đông Phương
2. **Bản Luận giải Bát tự chuyên sâu** (icon `Scroll`). giải mã ngũ hành bản mệnh, hộ đồng thần, phương án bổ khuyết
3. **Hỏi đáp AI không giới hạn** (icon `ChatCircleDots`). độc quyền gửi tới 10 câu hỏi chuyên sâu mỗi ngày
4. **An tâm đồng hành** (icon `ShieldCheck`). đồng bộ PWA, không auto-renew, hoàn tiền 100% trong 7 ngày

## 12. Trust signals (bắt buộc trên hero)

Dưới features list, 3 trust badges ngang hàng:

```
[ 🛡️ Không auto-renew ]  [ ↩️ Hoàn tiền 7 ngày ]  [ 🔒 PWA bảo mật ]
```

Mỗi badge 12px mono uppercase, ink text trên gold-tint bg, kèm Phosphor icon.

## 13. Accessibility (WCAG 2.2 AA)

- **Hero tier như link**: wrap toàn card trong `<a href="/dat-lich?plan=goi_12thang">`. CTA button bên trong KHÔNG có `<a>` riêng (không nested anchors).
- **Standard tier như link**: cùng pattern, plan parameter khác (`goi_3thang`, `goi_6thang`).
- **Feature list**: dùng `<ul>` với `<li>` con. Mỗi mục là đơn vị semantic.
- **Savings badge**: phải có visible text, không icon-only. Cung cấp `aria-label` với đầy đủ số tiền cho screen reader.
- **Decorative ribbon**: có thể là `<div aria-hidden="true">` nếu text trùng với title của card.
- Tương phản:
  - Hero tier text `#ede7d3` trên `#1d3129`: 11.2:1 ✓ AAA
  - Price `#c5a55a` trên `#1d3129`: 6.4:1 ✓ AA
  - Ribbon text `#1d3129` trên `#c5a55a`: 6.4:1 ✓ AA
  - Standard tier text trên trắng: 14.8:1 ✓ AAA
  - Struck-through feature `#7a7050` trên trắng: 4.7:1 ✓ AA (vẫn đọc được)
- Hit area: toàn card clickable. Touch target ≥44px height (cards vượt ngưỡng này).
- Bàn phím: tab di chuyển giữa các tier card; Enter kích hoạt tier link.
- Screen reader: announce tier name, duration, giá, số feature. Ví dụ: "Gói Trải Nghiệm, 3 tháng, 99.000 đồng, 4 tính năng".

## 14. Checklist QA

- [ ] Đúng 3 tier theo thứ tự (3-month, 6-month, 12-month)
- [ ] Tier 12 tháng dùng hero layout (2-col)
- [ ] Tier 3 và 6 tháng dùng compact layout
- [ ] Ribbon hiển thị trên tier 12 tháng (có `Star` icon)
- [ ] Savings badge chỉ trên tier 6 tháng (có `PiggyBank` icon)
- [ ] Đủ 4 hero features trong copy (mỗi feature có Phosphor icon)
- [ ] Không auto-renew và refund copy hiển thị
- [ ] Trust signals 3 badge dưới features list
- [ ] Giá dùng `tabular-nums`
- [ ] Currency format `549.000₫` (dấu chấm, trailing)
- [ ] Hover lifts với `translateY(-2px)`, không margin
- [ ] Tất cả trạng thái định nghĩa
- [ ] Reduced-motion tôn trọng transform duration
- [ ] axe-core scan: 0 vi phạm
- [ ] Link wrap toàn card (không nested anchors)
- [ ] Có ảnh thumbnail cuốn lịch 96×96 ở hero tier

## 15. Code reference

```tsx
<a
  href="/dat-lich?plan=goi_12thang"
  class="group relative block bg-[#1d3129] text-[#ede7d3] p-[52px_56px] border-[1.5px] border-[#c5a55a] shadow-[0_24px_48px_rgba(29,49,41,0.25)] hover:shadow-[0_32px_64px_rgba(29,49,41,0.35)] hover:-translate-y-0.5 transition-all duration-200 no-underline overflow-hidden"
  aria-label="Gói Lịch bản mệnh cả năm, 549.000 đồng, 4 tính năng"
>
  {/* Background pattern */}
  <img src="https://picsum.photos/seed/gold-vein-pattern/200/200" alt="" aria-hidden="true" class="absolute inset-0 w-full h-full object-cover opacity-[0.04] pointer-events-none" />

  {/* Thumbnail top-right */}
  <div class="absolute top-6 right-6 w-24 h-24 rounded-[4px] overflow-hidden ring-2 ring-[#c5a55a] ring-offset-2 ring-offset-[#1d3129] shadow-[0_8px_18px_rgba(0,0,0,0.4)]">
    <img src="https://picsum.photos/seed/lich-to-tear-off/96/96" alt="Cuốn lịch bản mệnh 365 trang" class="w-full h-full object-cover" />
  </div>

  {/* Ribbon */}
  <div class="absolute -top-3 left-8 z-10 inline-flex items-center gap-2 px-3.5 py-1 bg-[#c5a55a] text-[#1d3129] rounded-[2px] shadow-[0_4px_12px_rgba(197,165,90,0.25)]">
    <Phosphor.Star size={11} weight="fill" aria-hidden="true" />
    <span class="font-mono text-[10.5px] font-extrabold tracking-[0.22em]">KHUYẾN NGHỊ · TRỌN VẸN NHẤT</span>
  </div>

  <div class="relative grid items-start gap-12 grid-cols-1 md:grid-cols-[1.4fr_1fr]">
    <div>
      <span class="inline-flex items-center gap-1.5 font-mono text-[11.5px] tracking-[0.22em] uppercase text-[#c5a55a]">
        <Phosphor.Calendar size={12} weight="bold" aria-hidden="true" />
        LỊCH ĐỊNH MÙI 2027 · TRỌN NĂM
      </span>
      <h3 class="font-display font-extrabold uppercase leading-[0.96] mt-2.5 text-[56.5px] tracking-[-0.02em]">
        Lịch bản mệnh<br />
        <span class="font-serif italic font-bold normal-case text-[#c5a55a]">cho cả năm</span>
      </h3>
      <ul class="mt-8 space-y-3.5 font-serif text-[14.5px] leading-relaxed text-[rgba(237,231,211,0.9)]">
        <li class="flex items-start gap-3">
          <Phosphor.BookOpen size={18} weight="fill" class="text-[#c5a55a] mt-0.5 shrink-0" aria-hidden="true" />
          <span><strong>365 ngày Lịch bản mệnh Tứ Trụ:</strong> Điểm số cát hung và thời khắc hành sự đại sự được cá nhân hóa trọn vẹn hằng ngày theo chuẩn cổ thư Đông Phương.</span>
        </li>
        <li class="flex items-start gap-3">
          <Phosphor.Scroll size={18} weight="fill" class="text-[#c5a55a] mt-0.5 shrink-0" aria-hidden="true" />
          <span><strong>Bản Luận giải Bát tự chuyên sâu:</strong> Giải mã ngũ hành bản mệnh, hộ đồng thần, phương án bổ khuyết cho từng giai đoạn cuộc đời.</span>
        </li>
        <li class="flex items-start gap-3">
          <Phosphor.ChatCircleDots size={18} weight="fill" class="text-[#c5a55a] mt-0.5 shrink-0" aria-hidden="true" />
          <span><strong>Hỏi đáp AI không giới hạn:</strong> Độc quyền gửi tới 10 câu hỏi chuyên sâu mỗi ngày về vận hạn, sự nghiệp, gia đạo.</span>
        </li>
        <li class="flex items-start gap-3">
          <Phosphor.ShieldCheck size={18} weight="fill" class="text-[#c5a55a] mt-0.5 shrink-0" aria-hidden="true" />
          <span><strong>An tâm đồng hành:</strong> Đồng bộ PWA, không auto-renew, hoàn tiền 100% trong 7 ngày nếu không hài lòng.</span>
        </li>
      </ul>

      {/* Trust signals */}
      <div class="mt-7 flex flex-wrap items-center gap-2.5">
        <span class="inline-flex items-center gap-1.5 px-2.5 py-1 bg-[rgba(197,165,90,0.12)] text-[#c5a55a] rounded-[2px] font-mono text-[10px] uppercase tracking-wider">
          <Phosphor.Prohibit size={11} weight="fill" aria-hidden="true" />
          Không auto-renew
        </span>
        <span class="inline-flex items-center gap-1.5 px-2.5 py-1 bg-[rgba(197,165,90,0.12)] text-[#c5a55a] rounded-[2px] font-mono text-[10px] uppercase tracking-wider">
          <Phosphor.ArrowUUpLeft size={11} weight="bold" aria-hidden="true" />
          Hoàn tiền 7 ngày
        </span>
        <span class="inline-flex items-center gap-1.5 px-2.5 py-1 bg-[rgba(197,165,90,0.12)] text-[#c5a55a] rounded-[2px] font-mono text-[10px] uppercase tracking-wider">
          <Phosphor.Lock size={11} weight="fill" aria-hidden="true" />
          PWA bảo mật
        </span>
      </div>

      <span class="mt-8 inline-flex items-center justify-center gap-2.5 w-full max-w-md py-[18px] font-display font-extrabold text-sm uppercase bg-[#c5a55a] text-[#1d3129] tracking-[0.1em] shadow-[0_12px_24px_rgba(197,165,90,0.15)] group-hover:shadow-[0_16px_32px_rgba(197,165,90,0.25)] group-hover:-translate-y-px transition-all duration-200">
        <Phosphor.Crown size={16} weight="fill" aria-hidden="true" />
        Đăng ký lịch năm
        <Phosphor.ArrowRight size={16} weight="bold" class="transition-transform duration-200 group-hover:translate-x-1" aria-hidden="true" />
      </span>
    </div>

    <div class="flex flex-col h-full justify-between">
      <div>
        <span class="inline-flex items-center gap-1.5 font-mono text-[10.5px] tracking-[0.18em] uppercase text-[#c5a55a]">
          <Phosphor.CurrencyCircleDollar size={12} weight="bold" aria-hidden="true" />
          CHI PHÍ ĐỒNG HÀNH
        </span>
        <div class="flex items-baseline gap-1.5 mt-2">
          <span class="font-display font-extrabold leading-[0.85] tabular-nums text-[72.5px] text-[#c5a55a] tracking-[-0.03em]">
            549.000
          </span>
          <span class="font-display font-bold text-[24.5px] text-[#c5a55a]">₫</span>
        </div>
        <div class="mt-3 inline-flex items-center gap-1.5 px-3 py-1 font-mono text-[10.5px] font-bold uppercase rounded-[2px] bg-[rgba(197,165,90,0.18)] text-[#c5a55a]">
          <Phosphor.PiggyBank size={11} weight="bold" aria-hidden="true" />
          Tiết kiệm 298.000₫ · Tối ưu trọn vẹn
        </div>
      </div>
      <div class="mt-8 p-4 font-serif text-[13px] leading-relaxed rounded-[3px] bg-[rgba(255,255,255,0.03)] border border-dashed border-[rgba(197,165,90,0.25)]">
        <p class="m-0 text-[rgba(237,231,211,0.7)] inline-flex gap-2">
          <Phosphor.Quotes size={16} weight="fill" class="text-[#c5a55a] opacity-50 shrink-0 mt-0.5" aria-hidden="true" />
          <span>Gói dịch vụ được nhiều quý anh chị trên 30 tuổi tin dùng nhất. Đã bao gồm trọn gói Luận giải Bát tự (tiết kiệm hơn 40% so với mua lẻ).</span>
        </p>
      </div>
    </div>
  </div>
</a>
```