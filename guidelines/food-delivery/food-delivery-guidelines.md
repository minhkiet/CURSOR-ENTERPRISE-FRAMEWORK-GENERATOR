# Food Delivery. Design System Guidelines (Market Pro 2026)

> **Redesign ngày 2026-07-05.** Phiên bản Market Pro thay thế bản editorial cũ. Giống Shopee Food, Grab Food, Baemin, GoFood — giàu ảnh món thật, deals countdown, live tracking, nhiều filter.

## 1. Context

Bowl & Bite là food delivery marketplace TP.HCM + Hà Nội + Đà Nẵng. Bốn bề mặt:

- **Discovery** (`/`). Search bar · categories · nearby restaurants · trending dishes · promo banner · cuisine filter
- **Restaurant** (`/restaurants/[id]`). Hero photo · menu categories · dish grid · reviews · info
- **Cart** (`/cart`). Items list · coupon · delivery time · checkout
- **Tracking** (`/orders/[id]`). Live map · driver info · chat · status timeline

### 1.2 Brand-locked

| Hạng mục | Quyết định |
|---|---|
| Wordmark | "Bowl & Bite" · Plus Jakarta Sans 800 |
| Logo mark | Tô bát stylized, fill brand green |
| Palette | Trắng + xanh lá brand + cam coral + xám |
| Cuisines | Phở, Bún chả, Cơm tấm, Bánh mì, Chè, Bánh xèo, Lẩu, Cà phê, Bún bò, Hủ tiếu, Bánh cuốn |
| Delivery tiers | Standard 25 min · Express 15 min · Scheduled |

### 1.3 Design intent

Mỗi màn hình đọc như **app delivery Đông Nam Á chuyên nghiệp**. Ảnh món thật dominant, rating + sold count, ETA chính xác, distance, promo badge, free ship, category icons đầy màu.

### 1.4 Anti-patterns

- ❌ Cormorant/Fraunces (cũ dùng Fraunces cho dish names)
- ❌ Cream background (cũ: `#fff7ed`)
- ❌ Editorial "make every screen feel like..." 
- ❌ Picsum random
- ❌ Em-dash
- ❌ Generic names

---

## 2. Tokens

Xem `tokens.json`. Brand green `#16a34a` thay cho coral cũ.

---

## 3. Icon system

Phosphor.

| Role | Phosphor |
|---|---|
| Star rating | `Star` (fill) |
| Delivery time | `Clock` |
| Distance | `MapPin` |
| Free ship | `Truck` |
| Promo | `Ticket` |
| Add | `Plus` (bold) |
| Cart | `ShoppingBag` |
| Search | `MagnifyingGlass` |
| Filter | `Funnel` |
| Heart | `Heart` |
| Restaurant | `ForkKnife` |
| Vegan | `Leaf` |
| Spicy | `Fire` (fill) |
| Driver | `Motorcycle` |
| Payment | `CreditCard` |
| Cash | `Money` |
| Live tracking | `CrosshairSimple` |
| Category Phở | `BowlFood` |
| Category Cơm | `RiceBowl` |
| Category Bún | `Noodles` |
| Category Bánh mì | `Bread` |
| Category Trà sữa | `Coffee` |
| Category Lẩu | `CookingPot` |
| Category Chè | `IceCream` |
| Category Cà phê | `Coffee` (alt) |

---

## 4. Imagery & Video

### 4.1 Image sources

| Element | Unsplash curated ID |
|---|---|
| Phở | `1576577445504-6af96477db52` |
| Bún chả | `1552611052-33e04de081de` |
| Cơm tấm | `1565299624946-b28f40a0ae38` |
| Bánh mì | `1559054663-e8d23213f55c` |
| Lẩu | `1547573854-74d2a71d0826` |
| Trà sữa | `1556679343-c7306c1976bc` |
| Cà phê | `1495474472287-4d71bcdd2085` |
| Bún bò | `1582878826629-29b7ad1cdc43` |
| Bánh cuốn | `1569718212165-3a8278d5f624` |
| Hủ tiếu | `1569718212165-3a8278d5f624` |

Restaurant hero, dish, interior, chef — all Unsplash curated.

### 4.2 Photo treatment

- `filter: saturate(1.08) brightness(1.03) contrast(1.02)` cho appetite-driven warm vibe.

---

## 5. Section anatomy (Homepage)

1. **Sticky header**. Logo · Search bar (large, với location selector) · Login · Cart (with badge count)
2. **Hero banner carousel**. Auto-rotating banners với CTA (Big promo, Featured restaurant)
3. **Categories grid**. 8-10 category icon circles (Phở, Bún, Cơm, Bánh mì, Lẩu, Trà sữa, Cà phê, Chè) - circular image với label
4. **Featured promo strip**. Banner ngang: "Giảm 50.000₫ đơn từ 150.000₫" với countdown
5. **Nearby restaurants**. "Gần bạn" với map preview thumbnail + restaurant cards
6. **Trending dishes**. Horizontal scroll với rating + sold count + price
7. **Top cuisines bento**. Bento grid: 1 hero + 4 cuisine types
8. **New on Bowl & Bite**. Restaurant mới trong tuần
9. **Promo codes**. Carousel cards với code, value, expiry
10. **App download CTA**. QR + 2 store badges
11. **Mega footer**

**Density**: VARIANCE 7 · MOTION 6 · DENSITY 8 (market-dense)

---

## 6. Voice

- **Appetite-first.** "Phở bò tái với nước dùng ninh 12 tiếng"
- **Urgent for deals.** "Còn 2 tiếng 14 phút"
- **Sold count.** "Đã bán 847 phần tuần này"
- **Free ship CTA.** "Freeship đơn từ 100.000₫"
- **Vietnamese có dấu.** "Phở" không "Pho"
- **Em-dash cấm.**

---

## 7. Components

Xem `components/`:
- `restaurant-card.md`
- `dish-card.md`
- `category-circle.md`
- `promo-banner.md`
- `cart-summary.md`
- `live-tracking.md`
- `footer-mega.md`

---

## 8. Checklist

- [ ] Tokens semantic
- [ ] Plus Jakarta Sans, không Fraunces
- [ ] Green brand + coral accent, không cream
- [ ] Real dish photos, không Picsum
- [ ] Mega-search bar prominent
- [ ] Bento cuisines grid
- [ ] Promotional countdown
- [ ] Mega footer
- [ ] axe-core 0
- [ ] WCAG AA
- [ ] Reduced motion
- [ ] No em-dash