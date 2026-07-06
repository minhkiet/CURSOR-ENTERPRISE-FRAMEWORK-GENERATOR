# Real Estate Accessibility Appendix

> WCAG 2.2 AA acceptance criteria for Anchor Pro. Bắt buộc pass axe-core và manual screen reader test.

## 1. Universal requirements

1. **Keyboard**: mọi element tương tác reachable qua Tab theo DOM order. Enter/Space activate. Escape đóng overlay.
2. **Focus visible**: `:focus-visible` ring 2px solid teal-500, offset 2px. Mouse click không show ring.
3. **Contrast**: text/bg đạt WCAG AA. Body ≥4.5:1, large text ≥3:1, UI components ≥3:1.
4. **Labels**: mỗi input có `<label>` hoặc `aria-label`.
5. **Touch target**: ≥44x44px. Visual nhỏ hơn phải extend với padding.
6. **Motion**: `prefers-reduced-motion: reduce` collapse tất cả animation ≤ 50ms, tắt parallax.
7. **Screen reader**: status messages dùng `aria-live="polite"`. Errors dùng `role="alert"`.
8. **Language**: `<html lang="vi">`.

## 2. Component-specific

### 2.1 Listing card
- Mỗi CTA là `<a>` cho navigation, `<button>` cho action (heart, 360 tour).
- Heart có `aria-pressed`.
- Image `alt` mô tả: `Bất động sản ${title} tại ${address}`.
- Sold overlay có `role="status"`.
- Specs dùng icon aria-hidden + visible text.
- Touch target ≥44x44 cho mỗi button.

### 2.2 Search widget
- Form semantic với `<label>` cho mỗi input.
- Select fields có `<label>` + visible label.
- Filter chips có `aria-pressed`.
- Submit button `<button type="submit">`.
- Validation errors dùng `role="alert"`.
- Loading state dùng `aria-busy="true"`.

### 2.3 Hero
- `<h1>` cho headline.
- Video có `aria-hidden="true"`, poster thay thế khi reduced-motion.
- Search widget reachable bằng keyboard.
- CTAs `<a>` semantic.

### 2.4 Bento market
- Mỗi cell là `<article>` với heading.
- Charts có text alternative ngay trong cell.
- Số liệu tabular-nums.
- Map pins có `aria-label` mô tả city + count.

### 2.5 Footer
- `<footer>` semantic.
- Phone `<a href="tel:">`, email `<a href="mailto:">`.
- QR code có `aria-label`.
- Social icons có `aria-label`.
- Payment logos có `alt=""` (decorative) hoặc `alt="Visa"`.

## 3. Vietnamese considerations

- Diacritics: text rendering support đầy đủ dấu tiếng Việt. Plus Jakarta Sans + Be Vietnam Pro fallback đảm bảo.
- Number formatting: `8.5 tỷ` (period as thousands separator).
- Currency: `triệu/m²` cho đơn giá.
- Date: `5/7/2026` (DD/MM/YYYY).
- Reading order: LTR, top-to-bottom.

## 4. Testable acceptance criteria

| Check | Method | Pass criteria |
|---|---|---|
| Keyboard nav | Manual + axe | Tab đi qua mọi control theo DOM order |
| Focus visible | Manual | Ring 2px teal-500 visible trên mọi focus |
| Contrast | axe-core | 0 AA violations |
| Screen reader | NVDA + VoiceOver | Headlines, CTAs, image alts đọc rõ |
| Touch target | Manual | Mỗi interactive element ≥ 44x44px |
| Reduced motion | Manual + media query | Animations collapse, content vẫn readable |
| Language | HTML check | `<html lang="vi">` |
| No autoplay audio | Manual | Video muted, no audio start without click |

## 5. Test tools

- axe DevTools browser extension
- NVDA + Firefox (Windows)
- VoiceOver + Safari (macOS/iOS)
- Chrome DevTools Lighthouse
- Contrast checker (WebAIM)
- Real keyboard test (no mouse)

## 6. Common violations to watch

- ❌ Carousel without pause button
- ❌ Video without captions
- ❌ Form without labels
- ❌ Icon button without `aria-label`
- ❌ Modal without focus trap
- ❌ Image with empty alt when meaningful
- ❌ Decorative SVG without `aria-hidden`
- ❌ Focus order mismatch visual order
- ❌ Auto-playing audio
- ❌ Required form field without indicator