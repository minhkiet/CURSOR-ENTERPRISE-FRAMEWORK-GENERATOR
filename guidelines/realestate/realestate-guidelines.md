# Real Estate. Design System Guidelines (Market Pro 2026)

> **Redesign ngày 2026-07-05.** Phiên bản "Market Pro" thay thế bản editorial cũ. Mục tiêu: giống các web BDS hàng đầu VN (Batdongsan.vn, Meeyland, Rever, OneHousing) — giàu thông tin, giàu ảnh thật, giàu video, bố cục chuyên nghiệp.

---

## 1. Context

Anchor Pro là nền tảng BĐS Việt Nam cho thuê, mua bán, đầu tư. Bốn bề mặt:

- **Trang chủ** (`/`). mega-hero + search overlay + listing grid + market insights + map widget + dự án nổi bật.
- **Search results** (`/search`). map + list + filter sidebar + sort.
- **Listing detail** (`/listings/[id]`). gallery thật + video walkthrough + floor plan + mortgage calculator + agent + 360 tour.
- **Project detail** (`/projects/[slug]`). master plan + tiến độ + mặt bằng + pháp lý + bảng giá + lịch mở bán.

### 1.2 Brand-locked

| Hạng mục | Quyết định |
|---|---|
| Wordmark | "Anchor Pro" · Plus Jakarta Sans 800, tracking -0.04em |
| Logo mark | Chữ "A" tam giác cách điệu, fill brand teal |
| Palette | Trắng + xanh navy + teal brand + cam accent. KHÔNG dùng cream/serif |
| Property types | Căn hộ, Nhà phố, Biệt thự, Đất nền, Shophouse, Văn phòng, Officetel |
| Areas | m² |
| Prices | tỷ / triệu VNĐ. Format `8.5 tỷ` hoặc `45.2 triệu/m²` |
| Trust signals | Pháp lý minh bạch, đã xác minh, video thật, ảnh thật 100% |

### 1.3 Design intent

Mỗi màn hình đọc như một **sàn giao dịch BĐS trực tuyến chuyên nghiệp**. Dày thông tin (giá, diện tích, phòng, pháp lý, vị trí), nhiều ảnh/video thật, CTA rõ ràng, có dữ liệu thị trường kèm theo. Không hoa mỹ, không "feel like" gì cả.

### 1.4 Anti-patterns (BẮT BUỘC loại bỏ)

- ❌ Cormorant Garamond, Fraunces, Instrument Serif (banned theo frontend-taste §3.1)
- ❌ "Make every screen feel like..." cliché
- ❌ Cream/sepia background (chỉ dùng trắng / xám / navy / brand tint)
- ❌ 3-equal-card feature row (dùng bento asymmetric hoặc split)
- ❌ Picsum random ảnh (dùng Unsplash với semantic query + video Coverr)
- ❌ Lucide-react primary (chỉ Phosphor)
- ❌ Em-dash `—` trong visible copy
- ❌ Generic names "Nguyễn Văn A"
- ❌ AI-purple glow / centered hero / Inter default

---

## 2. Design Tokens

Xem `tokens.json`. Tokens semantic, dùng `--color-*`, `--font-*`, `--space-*`, `--radius-*`, `--shadow-*`.

### 2.1 Color strategy (5-color palette)

| Token | Value | Use |
|---|---|---|
| `surface.page` | `#ffffff` | Page bg chính |
| `surface.dark` | `#0a1628` | Hero dark strip, CTA sections, footer |
| `surface.subtle` | `#f8fafc` | Section ngăn cách |
| `text.brand` | `#0d9488` | CTA chính, link active, accent |
| `text.accent` | `#ea580c` | Badge "Mới", sale, urgent |
| `text.verified` | `#0284c7` | Badge xác minh, trust |
| `text.success` | `#16a34a` | Available, completed |

**Rule**: 1 trang chỉ 1 accent. Teal brand primary, cam chỉ xuất hiện ở badge/urgency.

### 2.2 Typography

| Slot | Family | Weight | Size |
|---|---|---|---|
| Hero display | Plus Jakarta Sans | 800 | 72–96px |
| H1 | Plus Jakarta Sans | 700 | 56px |
| H2 | Plus Jakarta Sans | 700 | 40px |
| H3 | Plus Jakarta Sans | 600 | 32px |
| H4 | Plus Jakarta Sans | 600 | 22px |
| Body | Plus Jakarta Sans | 400 | 16px |
| Body small | Plus Jakarta Sans | 400 | 14px |
| Label / eyebrow | Plus Jakarta Sans | 600 | 11px, uppercase, tracking 0.08em |
| Price | Plus Jakarta Sans | 800 tabular-nums | 36px |
| Address / meta | Plus Jakarta Sans | 400 | 13px |
| Mono (ID, area) | JetBrains Mono | 500 | 12px |

**Be Vietnam Pro** là fallback cho tiếng Việt có dấu.

### 2.3 Spacing & Radius

4 / 8 / 12 / 16 / 20 / 24 / 32 / 40 / 48 / 64 / 80 / 96 / 128 px grid.

`radius.md` (8px) cho cards. `radius.lg` (12px) cho inputs/modals. `radius.pill` cho badges.

### 2.4 Shadow

`shadow.md` (4+12) cho card mặc định. `shadow.lg` (8+24) cho hover. `shadow.brand` (teal-tinted) cho CTA focus.

---

## 3. Icon system

Phosphor (`@phosphor-icons/react`). Allowed secondary: Lucide nếu cần icon cụ thể không có trong Phosphor.

| Role | Phosphor | Size |
|---|---|---|
| Bedroom | `Bed` | 16px |
| Bathroom | `Bathtub` | 16px |
| Area | `Ruler` | 16px |
| Floor | `StackSimple` | 16px |
| Pin | `MapPin` (fill) | 14px |
| Heart | `Heart` | 18px |
| Compare | `Scales` | 16px |
| Verified | `SealCheck` (fill) | 14px |
| 360 tour | `Cube` | 16px |
| Video | `PlayCircle` (fill) | 18px |
| Phone | `Phone` | 16px |
| Schedule tour | `CalendarPlus` | 16px |
| Direction | `NavigationArrow` | 16px |
| Pool | `SwimmingPool` | 14px |
| Parking | `Car` | 14px |
| Garden | `Tree` | 14px |
| Elevator | `ArrowsOutCardinal` | 14px |
| Balcony | `Rectangle` | 14px |
| Direction facing | `Compass` | 14px |
| Furnished | `Armchair` | 14px |
| Legal | `FileText` | 14px |
| ROI | `TrendUp` | 14px |
| Chat | `ChatCircleDots` | 16px |

---

## 4. Imagery & Video

### 4.1 Image source

| Element | Source pattern | Aspect |
|---|---|---|
| Listing hero (exterior) | `https://images.unsplash.com/photo-{id}?w=1200&h=750&fit=crop&q=80` (curated ID list) | 8:5 |
| Listing interior | `https://images.unsplash.com/photo-{id}?w=1000&h=700&fit=crop&q=80` | 10:7 |
| Floor plan | Generated SVG component, NOT photo | 4:3 |
| Agent portrait | `https://images.unsplash.com/photo-{id}?w=400&h=400&fit=crop&q=80` | 1:1 |
| Neighborhood aerial | `https://images.unsplash.com/photo-{id}?w=1200&h=600&fit=crop&q=80` | 2:1 |
| Project rendering | `https://images.unsplash.com/photo-{id}?w=1600&h=900&fit=crop&q=80` | 16:9 |
| 360 thumbnail | Static fallback + Play icon overlay | 16:9 |

**Real curated Unsplash IDs** (xem `assets/unsplash-curated.json` đính kèm). KHÔNG dùng Picsum random.

### 4.2 Video source

| Element | Source |
|---|---|
| Hero background | `https://cdn.coverr.co/videos/coverr-{slug}/1080p.mp4` (curated) hoặc `<video>` MP4 local |
| Listing walkthrough | 1 video per featured listing, 30-60s, MP4 + poster image |
| Project intro | 1 video per project, 60-90s, có subtitle |
| Drone aerial | Curated cho dự án cao cấp |

### 4.3 Photo treatment

- Default: no filter, slight saturation +3% cho ảnh trong nhà.
- `filter: brightness(1.02) saturate(1.05) contrast(1.02)` cho interior.
- KHÔNG dùng sepia, grayscale, vintage filter (anti-pattern).

---

## 5. Layout families

| Family | Use | Examples |
|---|---|---|
| Mega-hero with search overlay | Homepage | Hero image/video + filter widget floating top |
| Map split | Search results | Map 60% left, list 40% right |
| Gallery showcase | Listing detail | Hero image slider + thumbnail strip + 360/video toggle |
| Bento market insights | Homepage section | 5-cell bento: ROI / area / project / forecast |
| Comparison table | Project detail | 3-column compare 3 dự án cùng khu |
| Timeline legal | Listing detail | Vertical timeline: sổ đỏ, quy hoạch, xây dựng |
| Video testimonial | Project detail | Video cards với play overlay |
| Mega footer | All pages | 6-col link grid + app download QR + payment + social |

**Layout diversity rule**: 1 landing page cần ≥ 4 layout families khác nhau trong 8 sections.

---

## 6. Section anatomy (Homepage)

1. **Sticky header** · Logo · 5 nav · Hotline · Login · Đăng tin (CTA brand)
2. **Mega-hero** · Video bg 16:9 · overlay gradient · search widget (Loại BĐS · Khu vực · Giá · Diện tích · Tìm)
3. **Trust strip** · 5 trust badges inline: Pháp lý minh bạch · 50.000+ tin · 4.8★ rating · 1.200+ môi giới · Video 100% thật
4. **Featured listings** · 1 mega card bên trái (image lớn, video overlay) + 6 listing cards bên phải (3-col grid)
5. **Market insights bento** · 5 cells: "Giá trung bình Quận 2", "Dự đoán tăng giá 2026", "Top khu vực đầu tư", "Tỷ suất cho thuê", "So sánh Quận"
6. **Projects showcase** · Horizontal scroll 4 cards · video card ở giữa
7. **Map widget** · Full-width split: bản đồ + quick links theo khu vực (Quận 1, 2, Bình Thạnh, Thủ Đức...)
8. **Testimonial video** · 3 video cards + 1 video nổi bật
9. **Agent spotlight** · Avatar grid 8 môi giới + ratings
10. **Blog teaser** · 3 bài viết pháp lý/đầu tư
11. **CTA strip** · Dark navy · "Đăng tin miễn phí" + "Tải app"
12. **Mega footer** · 6-col links + app QR + hotline + payment

**Density**: VARIANCE 7 · MOTION 5 · DENSITY 7 (market-dense)

---

## 7. Voice

- **Direct, data-first.** "Căn hộ 4PN, 156m², 8.5 tỷ, sổ đỏ chính chủ" not "Spacious luxury apartment".
- **Số liệu thật, có nguồn.** "Giá trung bình Q2 tăng 12% YoY (nguồn: batdongsan.com.vn)".
- **Tiếng Việt có dấu đầy đủ.** Không "can ho", "nha pho".
- **CTA ngắn, imperative.** "Đặt lịch xem", "Gọi môi giới", "Lưu tin".
- **Tên địa danh chuẩn.** "Quận Hai Bà Trưng" không "Q.HBT".
- **Em-dash cấm hoàn toàn.**

---

## 8. Checklist

- [ ] Tokens semantic, không raw hex trong component
- [ ] Plus Jakarta Sans primary, không Inter, không serif
- [ ] Teal brand + cam accent + xanh verified. Không cream
- [ ] Unsplash curated IDs, có video thật
- [ ] 5+ layout families khác nhau trên 1 trang
- [ ] Mega-footer 6-col với QR + payment
- [ ] Search widget luôn trong hero
- [ ] Trust strip 4-5 badges inline
- [ ] Bento asymmetric, không 3-equal cards
- [ ] axe-core 0 violations
- [ ] Em-dash 0 occurrences
- [ ] WCAG AA 4.5:1 body, 3:1 large text
- [ ] Reduced-motion respected
- [ ] Keyboard nav cho filter, gallery, modal