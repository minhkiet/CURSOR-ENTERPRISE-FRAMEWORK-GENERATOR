# Bazi. Design System Guidelines (Market Pro 2026 — Editorial Hybrid)

> **Redesign ngày 2026-07-05.** Phiên bản Market Pro hybrid giữ editorial cốt lõi của di sản văn hóa (giấy dó, mực tàu, ấn triện đỏ son) nhưng thêm market density: video demo, infographics, testimonials với avatar thật, interactive chart, pricing rõ ràng.

## 1. Context

Bazi (八字) là personal destiny reading app. Bốn bề mặt:

- **Reading app** (`/`). birth input → chart generation → interpretation
- **Marketplace** (`/charts`). famous historical figures charts
- **Daily reading** (`/today`). today's reading for user
- **Comparison** (`/compare`). compare two charts

### 1.2 Brand-locked (giữ nguyên)

- Wordmark: 八字 · Bazi
- Palette: rice paper, cinnabar, bronze, sumi ink
- 五行 palette: 木 fire 火 earth 土 metal 金 water 水
- Reading structure: 年柱 / 月柱 / 日柱 / 时柱

### 1.3 Design intent

**Bound silk-thread book (线装书) + rich media**. Vẫn giữ cảm giác sách cổ điển, nhưng thêm video giải thích, infographic, testimonials, để người dùng hiểu sâu hơn.

### 1.4 Anti-patterns

- ❌ Cormorant Garamond (đang dùng - OK giữ Lora)
- ❌ Cream quá đậm (giảm xuống nhẹ)
- ❌ "Feel like..." copy
- ❌ Em-dash
- ❌ Fortune-cookie English

---

## 2. Tokens

Xem `tokens.json`. Giữ nguyên palette cốt lõi, thêm density mới.

---

## 3. Section anatomy (Homepage)

1. **Sticky header**. Logo 八字 · Bazi · 5 nav · "Đọc lá số" CTA
2. **Mega-hero**. Background ink-wash painting (Unsplash) · overlay · birth input widget
3. **Trust strip**. 5 trust: "100.000+ lá số đã đọc", "Chuyên gia 30 năm", "Bảo mật tuyệt đối", "Khuyến nghị ĐH Bắc Kinh", "Đã xuất hiện trên Forbes VN"
4. **5 elements bento**. 五行 snapshot bento: mỗi element 1 cell với icon, mô tả, %
5. **Sample chart showcase**. Ảnh chart thật (Unsplash) + 4 pillars + interpretation
6. **Marketplace famous charts**. Bento: Khổng Tử · Lý Bạch · Võ Tắc Thiên · Napoleon
7. **Video demo**. Video giải thích cách đọc lá số (Coverr hoặc embedded YouTube)
8. **Testimonial**. 3 testimonials với portrait thật
9. **Pricing tiers**. 3 gói: Cơ bản · Premium · Master
10. **Blog teaser**. 3 bài: "大运 là gì?", "用神 chọn sao?", "流年 2026"
11. **FAQ**. 6 câu hỏi thường gặp
12. **Footer**

**Density**: VARIANCE 7 · MOTION 4 · DENSITY 5 (rich hơn bản cũ)

---

## 4. Voice

- **命理 vocabulary.** 五行, 十神, 用神, 喜神, 忌神, 大运, 流年, 流月, 流日
- **English translations in parentheses.** "用神 (useful god)"
- **Second-person.** "Lá số của bạn" not "User's chart"
- **Em-dash cấm**

---

## 5. Imagery & Video

### 5.1 Image sources

| Element | Unsplash curated ID |
|---|---|
| Ink-wash hero | `1528127269322-539801943592` |
| Rice paper texture | `1578926375605-eaf7559b1458` |
| Seal stamp | `1547036967-23d11aacaee0` |
| Chinese landscape | `1547981609-4b6bfe67ca0b` |
| Famous portrait | `1539571696357-5a69c17a67c6` |
| Wuxing pattern | `1551184451-76b762941ad6` |

### 5.2 Video

- Hero: ink-wash animation (Coverr)
- Chart demo: chart generation walkthrough
- Expert intro: chuyên gia giải thích

---

## 6. Components

- `birth-input.md`
- `four-pillars-chart.md`
- `wuxing-snapshot.md`
- `marketplace-chart-card.md`
- `seal-stamp-disc.md`
- `pricing-tier.md`
- `testimonial-portrait.md`
- `footer-mega.md`

---

## 7. Checklist

- [ ] Tokens semantic
- [ ] Noto Serif SC + Lora only, no Cormorant, no Fraunces
- [ ] Paper warm bg
- [ ] 五行 palette visible only in chart
- [ ] Cinnabar dùng sparingly
- [ ] Real portrait ảnh
- [ ] No emoji
- [ ] Em-dash cấm
- [ ] axe-core 0
- [ ] WCAG AA
- [ ] Reduced motion