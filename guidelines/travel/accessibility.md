# Travel. Accessibility (WCAG 2.2 AA)

> Tiêu chí acceptance cho mọi giao diện Skylark travel platform. Áp dụng cho cả homepage marketing và booking flow.

## 1. Universal requirements

| Hạng mục | Tiêu chí | Test |
|---|---|---|
| Color contrast | Body text ≥ 4.5:1. Large text ≥ 3:1. UI components ≥ 3:1 | axe-core |
| Keyboard | Mọi tương tác accessible bằng Tab + Enter + Arrow + Esc | Manual |
| Focus visible | Ring navy 2px outline-offset 2px | Visible always |
| Touch target | ≥ 44x44px cho mobile controls | DevTools |
| Alt text | Mọi ảnh Unsplash có alt mô tả location | HTML scan |
| Language | `<html lang="vi">` với content | HTML |
| Motion | Respect `prefers-reduced-motion` | Toggle test |
| Video autoplay | Muted + paused on reduce-motion. Không loop quá 3 lần | Manual |
| Form labels | Mọi input có `<label>` không chỉ placeholder | HTML scan |
| Error messages | Liên kết với input bằng `aria-describedby`. Màu + icon, không chỉ màu | Manual |
| Live regions | Search results count = `aria-live="polite"` | Manual |
| Skip link | "Bỏ qua đến nội dung" ở header | Tab from start |

## 2. Component-specific

### 2.1 Hotel card

- Heart button `aria-pressed="true|false"`, label "Lưu khách sạn [tên]"
- Rating badge có text ẩn cho screen reader ("Xuất sắc, 4.8/5 từ 2.847 đánh giá")
- Gallery strip "+24 ảnh" button accessible
- Video overlay button có aria-label "Phát video walkthrough"
- Sold out overlay có role="status"

### 2.2 Flight search widget

- Trip type radio group với `role="radiogroup"`, mỗi option có label
- Date picker keyboard accessible (Arrow keys, Enter để chọn)
- Passenger stepper `aria-valuemin/max/now`
- From/To inputs với autocomplete `aria-expanded`, `aria-controls`
- Recent searches là `<button>` thật, focusable

### 2.3 Deal countdown

- Countdown không chỉ visual mà có text "Còn 2 giờ 14 phút 33 giây" sr-only cho screen reader
- Khi hết hạn: cập nhật thành "Đã hết hạn" + `aria-live="polite"`
- CTA button focus rõ

### 2.4 Destination bento card

- Card là `<a>` thật với text mô tả destination
- Hover state có transition 240ms, không nhấp nháy
- Image alt mô tả địa điểm: "Bãi biển Phú Quốc lúc hoàng hôn"
- Price badge có label "từ 1.290.000₫ một khách"

### 2.5 Mega footer

- 6 cột links với headings semantic `<h3>`
- Newsletter form có label rõ
- Social icons có aria-label ("Theo dõi Skylark trên Facebook")
- Payment icons có alt text ("Thanh toán qua Visa")
- Hotline link `tel:` accessible

## 3. Vietnamese language considerations

- Vietnamese diacritics bắt buộc (Phở, Hội An, Đà Lạt, Đà Nẵng)
- Currency format `2.500.000₫` tabular-nums cho price
- Distance "2,3 km" với dấu phẩy thập phân Việt Nam
- Date format "25 tháng 7, 2026" hoặc ISO "25/07/2026"

## 4. Booking flow specific

- Stepper có `aria-current="step"` cho bước hiện tại
- Total price được announce khi thay đổi: `aria-live="polite"` cho summary
- Cancellation policy text bắt buộc visible (không chỉ tooltip)
- Passenger info form có autocomplete cho tên, CMND
- Payment fields có PCI-compliant aria-label (tránh số thẻ công khai cho screen reader khi không cần)

## 5. Acceptance criteria

### 5.1 Testable

- [ ] axe-core: 0 violations
- [ ] Lighthouse accessibility: ≥ 95
- [ ] Manual keyboard tab từ header đến footer, không bị trap
- [ ] Screen reader (NVDA / VoiceOver): đọc được mọi phần quan trọng
- [ ] Color contrast: tất cả text passes WCAG AA
- [ ] Touch target: ≥ 44px
- [ ] Form errors có icon + text + màu

### 5.2 Common violations to avoid

- ❌ Placeholder thay label
- ❌ Icon không có aria-label
- ❌ Modal không trap focus / không restore focus
- ❌ Color-only state indication
- ❌ Auto-play video có âm thanh
- ❌ Countdown timer cập nhật liên tục không có debounce
- ❌ Map không có text alternative
- ❌ Date picker chỉ có mouse interaction
- ❌ Phone number trong image thay vì `<a href="tel:">`
- ❌ Carousel không có pause button

## 6. Recommended test tools

- axe-core (CLI + browser extension)
- Lighthouse CI
- NVDA + Firefox (Windows)
- VoiceOver + Safari (macOS / iOS)
- TalkBack + Chrome (Android)
- WAVE (visual overlay)
- Pa11y CI

## 7. Performance interplay

A11y thường gắn với performance:

- `aria-live` regions update có thể trigger reflow — debounce
- Focus rings tốn 2px render, OK
- Skip link giảm tab count
- Reduced-motion video: dùng poster image thay

---

**Version**: 2026.1 · WCAG 2.2 AA baseline