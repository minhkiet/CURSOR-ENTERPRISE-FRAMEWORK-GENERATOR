# Sale / E-commerce. Design System Guidelines (Market Pro 2026)

> **Redesign ngày 2026-07-05.** Phiên bản Market Pro thay thế. Giống Shopee, Tiki, Lazada — flash deal countdown dominant, sold progress bar, voucher, deal stack nhiều tầng.

## 1. Context

Strikeout là flash-sale + outlet marketplace VN. Bốn bề mặt:

- **Homepage** (`/`). Flash deal countdown hero · categories · mega deal · brand showcase · voucher carousel
- **Product detail** (`/products/[id]`). Gallery · specs · variants · reviews · flash badge sticky
- **Cart** (`/cart`). Items list · coupon · checkout sticky
- **Checkout** (`/checkout`). Stepper · address · payment · confirm

### 1.2 Brand-locked

| Hạng mục | Quyết định |
|---|---|
| Wordmark | "Strikeout" · Plus Jakarta Sans 800 (giữ Space Grotesk OK nhưng switch sang Plus Jakarta cho market consistency) |
| Logo mark | Tia sét stylized, fill brand orange |
| Palette | Trắng + đen + cam brand + vàng gold + đỏ danger |
| Discount tiers | -20%, -30%, -50%, -70%, -90% |
| Time format | Countdown HH:MM:SS |

### 1.3 Design intent

Đậm chất **flash-sale warehouse clearance**. Countdown đỏ/cam dominant, sold progress bar đỏ, strikethrough price đậm, urgency khắp nơi.

### 1.4 Anti-patterns

- ❌ Cormorant/Fraunces (Space Grotesk OK nhưng Plus Jakarta tốt hơn cho market-style)
- ❌ Cream background
- ❌ "Feel like..." copy
- ❌ Em-dash

---

## 2. Tokens

Xem `tokens.json`. Orange `#f97316` primary, danger red `#dc2626` chỉ cho sold out / strikethrough.

---

## 3. Section anatomy (Homepage)

1. **Sticky header**. Logo · Categories · Search · Cart (badge count) · User
2. **Flash deal countdown hero**. BIG countdown HH:MM:SS + mega deal card + 4 smaller deals
3. **Categories mega-menu**. Electronics · Fashion · Beauty · Home · Toys · Sports · Books · Auto · Groceries
4. **Voucher carousel**. Stack of voucher cards với code + value + min order + expiry
5. **Top brands showcase**. Brand wall với Simple Icons logos
6. **Flash deals by hour**. Countdown tabs: 9AM · 12PM · 3PM · 6PM · 9PM · 12AM
7. **Mega sale events**. Banner carousel: 7.7, 8.8, 9.9, 11.11, 12.12
8. **Top selling**. Bento grid với sold count
9. **New arrivals**. Horizontal scroll
10. **Footer mega**. 6-col + payment + social

**Density**: VARIANCE 6 · MOTION 6 · DENSITY 8 (very dense)

---

## 4. Voice

- **Urgent.** "Còn 02:14:33", "Sắp hết", "Đã bán 847"
- **Trust.** "Hoàn tiền 200% nếu hàng giả", "Đổi trả 7 ngày miễn phí"
- **Specific discount.** "-50% còn 299.000₫ ~~599.000₫~~"
- **Vietnamese diacritics đầy đủ**
- **Em-dash cấm**

---

## 5. Components

- `flash-deal-card.md`
- `product-card.md`
- `voucher-card.md`
- `countdown-timer.md`
- `category-tile.md`
- `mega-deal-banner.md`
- `cart-summary.md`
- `footer-mega.md`

---

## 6. Checklist

- [ ] Tokens semantic
- [ ] Plus Jakarta Sans + JetBrains Mono
- [ ] Orange + black + white
- [ ] Countdown visible everywhere
- [ ] Sold progress bar prominent
- [ ] Strikethrough original price
- [ ] Mega footer
- [ ] axe-core 0
- [ ] WCAG AA
- [ ] Reduced motion
- [ ] No em-dash