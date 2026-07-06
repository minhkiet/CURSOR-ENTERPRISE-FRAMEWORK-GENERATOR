# Food Delivery. Accessibility (WCAG 2.2 AA)

> Tiêu chí acceptance cho Bowl & Bite food delivery platform. Marketing site + customer ordering flow + driver tracking.

## 1. Universal requirements

| Hạng mục | Tiêu chí | Test |
|---|---|---|
| Color contrast | Body text ≥ 4.5:1. UI components ≥ 3:1. Brand green #16a34a trên white = 3.39:1 large text only | axe-core |
| Keyboard | Tab + Enter + Arrow + Esc đầy đủ | Manual |
| Focus visible | Ring brand green 2px | Visible always |
| Touch target | ≥ 44x44px cho mọi button | DevTools |
| Alt text | Ảnh món Unsplash có alt mô tả tên món + ingredients | HTML scan |
| Language | `<html lang="vi">` | HTML |
| Motion | Reduce-motion cho pulse / countdown | Toggle test |
| Currency | `49.000₫` tabular-nums | Visible |
| Time ETA | Cả relative ("25 phút") + absolute ("15:30") | Screen reader |

## 2. Component-specific

### 2.1 Restaurant card

- Ảnh có alt "Phở bò tái tại Quán Phở Hà Nội - Hà Nội"
- Heart button `aria-pressed`
- "Free ship" badge có icon + text
- Sold count có sr-only text ("Đã bán 847 phần tuần này")
- Price + discount badge có text "Giá gốc 80.000₫, giảm 30% còn 49.000₫"
- ETA "25 phút" có aria-label "Thời gian giao hàng ước tính 25 phút"
- Distance "1.2km" có text mô tả "cách bạn 1.2 km"

### 2.2 Dish card

- Add button `aria-label="Thêm [tên món] vào giỏ, [giá]"`
- Spicy / vegan badges có icon + text
- "Bán chạy" badge có rank
- Sold count visible
- Quantity stepper `aria-valuemin/max/now`

### 2.3 Category circle

- Icon + label visible
- 8 categories là `<button>` thật
- Focus visible ring
- Active state có visual change

### 2.4 Promo banner

- Countdown "Còn 02:14:33" có sr-only "Còn 2 giờ 14 phút 33 giây"
- Code "BOWL50K" có aria-label "Mã giảm giá BOWL50K, giảm 50.000₫ cho đơn từ 150.000₫"
- "Sao chép mã" button có feedback

### 2.5 Live tracking

- Map có text alternative ("Tài xế Nguyễn Văn A đang cách bạn 200m")
- ETA updates `aria-live="polite"`
- Driver avatar + name visible
- Status timeline có semantic markers
- "Gọi tài xế" là `<a href="tel:">` accessible

## 3. Vietnamese language considerations

- Món ăn có dấu: Phở, Bún chả, Cơm tấm (không "Pho", "Bun cha")
- Currency: `49.000₫` (dấu chấm phân cách hàng nghìn)
- Distance: `1,2 km` (dấu phẩy thập phân VN)
- ETA: "25 phút" not "25 min"
- "Miễn phí vận chuyển" not "Free shipping"
- "Đã bán 847 phần" not "847 sold"

## 4. Appetite-driven design considerations

- Màu sắc tươi, sạch, appetite
- Photo saturation cao để thu hút
- Không dùng red cho "mua" (red = warning, không appetite)
- Coral #ea580c cho CTA accent
- Green #16a34a cho success / fresh

## 5. Customer ordering flow

### 5.1 Cart

- Item list có remove button accessible
- Quantity stepper keyboard accessible
- Total price `aria-live="polite"` khi thay đổi
- Coupon input có label + error message

### 5.2 Checkout

- Address selector keyboard accessible
- Payment methods là radio group
- Order summary `aria-label="Tóm tắt đơn hàng"`
- Place order button loading state announced

### 5.3 Order tracking

- Status updates với toast + `aria-live`
- Map có alternative text view
- Driver info accessible
- "Gặp vấn đề?" help link accessible

## 6. Acceptance criteria

### 6.1 Testable

- [ ] axe-core: 0 violations
- [ ] Lighthouse accessibility: ≥ 95
- [ ] Manual keyboard flow: chọn món → add → checkout → track
- [ ] Screen reader: đọc được tất cả thông tin món, giá, ETA
- [ ] Color contrast: green/white text passes WCAG AA for large text
- [ ] Touch target: ≥ 44px cho mọi button
- [ ] Form errors có icon + text + màu
- [ ] Map có alt text view

### 6.2 Common violations to avoid

- ❌ Placeholder thay label
- ❌ Icon không có aria-label
- ❌ Modal không trap focus
- ❌ Color-only state (chỉ đổi màu khi hết hàng)
- ❌ Auto-play video có âm thanh
- ❌ Distance chỉ icon, không text
- ❌ ETA chỉ relative ("25 phút") không có absolute cho accessible time
- ❌ Carousel không có pause button

## 7. Performance + A11y interplay

- Auto-loading lazy images kèm alt
- Map tile lazy load
- Countdown debounce khi update để tránh spam aria-live
- Pre-render static placeholder cho countdown để tránh hydration mismatch

## 8. Recommended test tools

- axe-core CLI + browser extension
- Lighthouse CI
- NVDA + Firefox (Windows)
- VoiceOver + Safari (iOS)
- TalkBack + Chrome (Android)
- WAVE
- Pa11y CI

---

**Version**: 2026.1 · WCAG 2.2 AA baseline