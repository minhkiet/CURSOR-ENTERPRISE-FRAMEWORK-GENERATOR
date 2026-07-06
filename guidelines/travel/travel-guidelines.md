# Travel Booking. Design System Guidelines (Market Pro 2026)

> **Redesign ngày 2026-07-05.** Phiên bản Market Pro thay thế bản editorial cũ. Giống Traveloka, Booking.com, Agoda — giàu ảnh thật, giàu deals, bố cục chuyên nghiệp.

## 1. Context

Skylark là nền tảng đặt vé máy bay + khách sạn + tour Đông Nam Á. Bốn bề mặt:

- **Trang chủ** (`/`). mega-search + deals countdown + destination showcase + hotel cards + reviews + flight map
- **Search results** (`/search`). filter sidebar + listing list + map + sort
- **Hotel detail** (`/hotels/[id]`). gallery ảnh thật + room selector + amenities + reviews + map + booking widget
- **Booking surface** (`/booking/[id]`). stepper + passenger info + payment + confirmation

### 1.2 Brand-locked

| Hạng mục | Quyết định |
|---|---|
| Wordmark | "Skylark" · Plus Jakarta Sans 800, tracking -0.04em |
| Logo mark | Chim én stylized, gradient brand navy → sky |
| Palette | Trắng + navy + xanh dương + hồng coral + amber |
| Destinations | Đà Lạt, Phú Quốc, Hội An, Sapa, Bangkok, Bali, Singapore, Tokyo, Seoul |
| Travel classes | Economy · Premium Economy · Business |
| Currency | VND. Format `2.500.000₫` |

### 1.3 Design intent

Mỗi màn hình đọc như **sàn OTA chuyên nghiệp Đông Nam Á**. Dày thông tin (giá, rating, amenities, cancellation, deals), ảnh thật 100%, video walkthrough cho hotel, interactive map, countdown deals, sticky search widget.

### 1.4 Anti-patterns

- ❌ Cormorant Garamond, Fraunces, Instrument Serif
- ❌ "Make every screen feel like..." cliché
- ❌ Cream/sky-blue pastel overload (cũ: `#e0f2fe`, `#fef3c7`)
- ❌ 3-equal-card feature row
- ❌ Picsum random
- ❌ Em-dash
- ❌ Generic names

---

## 2. Tokens

Xem `tokens.json`.

### 2.1 Color strategy

| Token | Value | Use |
|---|---|---|
| `text.brand` | `#0c4a6e` | CTA chính, link, nav active |
| `text.accent` | `#f43f5e` | Coral. Discount badge, urgent deals |
| `text.verified` | `#0284c7` | Verified property badge |
| `text.success` | `#16a34a` | Available, instant confirm |

**Rule**: navy là primary, coral chỉ xuất hiện ở badges/deals/urgency.

### 2.2 Typography

| Slot | Family | Weight | Size |
|---|---|---|---|
| Hero | Plus Jakarta Sans | 800 | 72–96px |
| H1 | Plus Jakarta Sans | 700 | 56px |
| H2 | Plus Jakarta Sans | 700 | 40px |
| Body | Plus Jakarta Sans | 400 | 16px |
| Price | Plus Jakarta Sans | 800 tabular-nums | 24-32px |
| Label | Plus Jakarta Sans | 600 | 11px uppercase |
| Mono (time, code) | JetBrains Mono | 500 | 12px |

### 2.3 Spacing & Radius

4 / 8 / 12 / 16 / 20 / 24 / 32 / 40 / 48 / 64 / 80 / 96 / 128 px.

`radius.md` (8px) cards, `radius.lg` (12px) inputs, `radius.xl` (16px) hero CTAs, `radius.pill` cho badges.

---

## 3. Icon system

Phosphor (`@phosphor-icons/react`).

| Role | Phosphor |
|---|---|
| Flight | `AirplaneTilt` |
| Hotel | `Buildings` |
| Tour | `MapTrifold` |
| Beach | `SunHorizon` |
| Mountain | `Mountains` |
| City | `City` |
| Star | `Star` (fill) |
| Heart | `Heart` |
| Calendar | `CalendarBlank` |
| Guest | `Users` |
| Duration | `Hourglass` |
| Free cancellation | `CalendarCheck` |
| Breakfast | `Coffee` |
| Pool | `SwimmingPool` |
| WiFi | `WifiHigh` |
| Parking | `Car` |
| Pet | `PawPrint` |
| Beach access | `Umbrella` |
| Spa | `Flower` |
| Gym | `Barbell` |
| Restaurant | `ForkKnife` |
| Airport transfer | `CarProfile` |
| Search | `MagnifyingGlass` |
| Filter | `Funnel` |
| Sort | `ArrowsDownUp` |
| Compare | `Scales` |
| Map pin | `MapPin` (fill) |
| Photo count | `Images` |
| Video | `PlayCircle` (fill) |
| Verified | `SealCheck` (fill) |
| Rating | `StarFour` (fill) |

---

## 4. Imagery & Video

### 4.1 Image sources

| Element | Source pattern | Aspect |
|---|---|---|
| Destination hero | Unsplash curated ID | 16:9 |
| Hotel exterior | Unsplash curated | 16:9 |
| Hotel room | Unsplash curated | 4:3 |
| Hotel pool/amenity | Unsplash curated | 16:9 |
| Traveler portrait | Unsplash curated | 1:1 |
| Map preview | Unsplash aerial | 16:9 |
| Deal banner | Unsplash curated | 21:9 |
| Airline logo | Simple Icons CDN | 1:1 |

### 4.2 Video

| Element | Source |
|---|---|
| Hero background | Coverr curated beach/destination video |
| Hotel walkthrough | Coverr 30-60s vertical |
| Destination aerial | Coverr drone footage |

### 4.3 Curated Unsplash IDs

```
destinations:
  da_lat: "1573279107032-d3e88dc7d12a"
  phu_quoc: "1582719508461-905c673771fd"
  hoi_an: "1528127269322-539801943592"
  sapa: "1528127269322-539801943592"
  bangkok: "1508009603885-50cf7c579365"
  bali: "1537996194471-e657df975ab4"
  singapore: "1565967511849-76a60a516170"
  tokyo: "1540959733332-eab4deabeeaf"
hotels:
  resort: "1566073771259-6a8506099945"
  boutique: "1551882547-ff40c63fe5fa"
  business: "1564501049412-61c2a3083791"
  luxury: "1582719508461-905c673771fd"
  pool_view: "1571896349842-33c89424de2d"
  room_interior: "1631049307264-da0ec9d70304"
  spa: "1540555700478-4be289fbecef"
travelers:
  female_1: "1494790108377-be9c29b29330"
  male_1: "1507003211169-0a1dd7228f2d"
  female_2: "1438761681033-6461ffad8d80"
  male_2: "1472099645785-5658abf4ff4e"
```

---

## 5. Layout families

| Family | Use |
|---|---|
| Mega-search hero | Homepage. Video bg + tabbed search (Flight/Hotel/Tour/Combo) |
| Deal countdown strip | Homepage section 2. Horizontal scroll cards with countdown |
| Destination showcase | Bento grid: 1 hero + 6 destinations |
| Hotel listing | Search results. List + map + filter sidebar |
| Hotel detail gallery | Hero slider + thumbnail strip + 360 + video |
| Booking widget | Sticky right column: room selector + price + book button |
| Flight route map | Search results. Map with route visualization |
| Testimonial carousel | Homepage section. Customer photos + reviews |
| Insurance upsell | Booking page. Banner with toggle |
| Confirmation hero | Booking done. Hero with booking code + countdown to flight |

---

## 6. Section anatomy (Homepage)

1. **Sticky header**. Logo · Search bar (mini) · Flight/Hotel/Tour tabs · Login · Deals · Hotline
2. **Mega-hero + search**. Video bg destination · overlay · 4-tab search widget (Flight / Hotel / Tour / Combo) với autocomplete
3. **Flash deal countdown strip**. Horizontal cards với countdown: "Còn 02:14:33", "Hot deal Hà Nội - Bali 1.290.000₫"
4. **Featured destinations bento**. 1 hero Phú Quốc + 6 destinations khác (Hội An, Đà Lạt, Bangkok, Bali, Singapore, Tokyo)
5. **Hotel collections**. "Khách sạn view biển 2026", "Resort trung tâm", "Hotel boutique". Mỗi collection 4-6 cards
6. **Deals by category**. Tab "Bay / Ở / Tour" với deal cards
7. **Customer reviews video**. 3 video testimonials
8. **Trust strip**. 6 trust badges: Giá tốt nhất · Hoàn tiền dễ · 24/7 support · Đặt cọc thấp · Chứng nhận IATA · Bảo hiểm du lịch
9. **App download CTA**. QR code + 2 store badges
10. **Mega footer**. 6-col links + destinations + airlines + payment + social

**Density**: VARIANCE 6 · MOTION 5 · DENSITY 7 (market-dense)

---

## 7. Components

Xem `components/`:
- `hotel-card.md`
- `flight-search-widget.md`
- `deal-countdown-card.md`
- `destination-bento.md`
- `testimonial-video.md`
- `footer-mega.md`

---

## 8. Voice

- **Optimistic, exploratory.** "Khám phá Hội An theo cách của bạn", "Bay trong 3 giờ tới Đà Lạt"
- **Số liệu cụ thể.** "Giá rẻ nhất 2.500.000₫" not "Great deals"
- **Cancellation policy rõ ràng.** "Hoàn 100% trước 48h" / "Không hoàn"
- **Địa danh chuẩn.** "Hội An" not "Hoi An"
- **CTA ngắn.** "Đặt ngay", "Xem phòng", "Chọn"
- **Em-dash cấm hoàn toàn.**

---

## 9. Checklist

- [ ] Tokens semantic
- [ ] Plus Jakarta Sans primary, không Inter default, không serif
- [ ] Navy + coral, không cream/sky pastel
- [ ] Real Unsplash + Coverr, không Picsum random
- [ ] Mega-search widget là first screen focus
- [ ] Bento destination grid asymmetric
- [ ] Deal countdown prominent
- [ ] Testimonial video có play button
- [ ] Mega footer 6-col
- [ ] axe-core 0 violations
- [ ] WCAG AA
- [ ] Reduced motion respected
- [ ] Em-dash 0 occurrences