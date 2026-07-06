# Accessibility Guidelines. Bazi

> WCAG 2.2 AA conformance rules specific to the Bazi product. Universal rules apply; the rules below cover product-specific cases.

## 1. Language

- Primary `<html lang="zh-Hans">`. English toggle adds `<html lang="en">` to root.
- Mixed-language content uses `<span lang="en">` for English fragments within Chinese copy and vice versa.
- Pinyin terms (e.g. 喜神 xishen) carry `<span lang="zh-Latn">` only when first introduced; subsequent uses can be Chinese-only.

## 2. Cultural and reading order

- Date format: `2026年7月5日` (Chinese) or `5 July 2026` (English). Year first in Chinese, day first in English. Do not invert.
- Time format: 24-hour for precision (`13:45`), with Chinese 时辰 (shi chen) labels when relevant (`未时 13:00–15:00`).
- Numbers: 中文 千分位 uses `,` (U+002C) in some regions, no separator in modern usage. Default: no separator for years, `,` for thousands in modern contexts.

## 3. Wuxing (五行) colors. never alone

Five-element color encoding must always be paired with the character label (木 / 火 / 土 / 金 / 水) and/or an icon (`Tree`, `Flame`, `Mountains`, `Coins`, `Drop`). Never communicate element by color alone. Each element color also meets 4.5:1 against `color.surface.paper` and `color.surface.card`.

| Element | Char | Icon | Hex | Contrast on `#f4ede0` |
|---|---|---|---|---|
| Wood 木 | 木 | `Tree` | `#5e8c5a` | 4.7:1 AA |
| Fire 火 | 火 | `Flame` (fill) | `#c84a2c` | 5.4:1 AA |
| Earth 土 | 土 | `Mountains` | `#a37b3a` | 4.5:1 AA |
| Metal 金 | 金 | `Coins` | `#b09a5a` | 3.6:1 (UI only, not text) |
| Water 水 | 水 | `Drop` | `#3a4f6e` | 8.7:1 AAA |

## 4. Cinnabar (`#a8331f`). restricted use

Cinnabar is auspicious red. Use it for:
- 吉 (auspicious) labels
- Seal 印 stamps
- Festival accents (Spring Festival, Mid-Autumn)
- Active state emphasis

Never use cinnabar for error or destructive (use sumi ink + `#3d2e1f` for those).

## 5. Charts and data tables

- Four-pillar chart (年柱 / 月柱 / 日柱 / 时柱): use a real `<table>` with `<caption>`, `<thead>`, `<tbody>`. Each cell is a `<th scope="row">` for stem/branch character and `<td>` for metadata.
- Header rows repeat on print (`<thead>` markup).
- Cell content limited to 2 lines; complex readings route to detail view.
- Reading text max-width 65ch.

## 6. Calendar and date input

- Date input accepts both Gregorian (`2026-07-05`) and Chinese lunar (e.g. `丙午年 六月初一`).
- Use `<input type="date">` for Gregorian with `lang="zh-Hans"` fallback.
- For lunar input, use a custom picker that announces in zh-Hans: "请选择农历日期".
- Time input supports 24-hour + 时辰 labels.

## 7. Names and identity

- Preserve full Unicode characters. Do not strip diacritics or tone marks.
- Romanized names (e.g. `孔子 Kongzi`) need both Chinese and Roman form. Use `<span lang="zh-Hans">孔子</span> <span lang="en">Kongzi</span>`.

## 8. Ten Gods (十神) terminology

Each ten god role has a glyph and an icon. Both must be present in the UI:

| Role | Glyph | Icon | Meaning |
|---|---|---|---|
| 比肩 | 比 | `User` | Same element peer |
| 劫财 | 劫 | `UsersThree` | Rob wealth |
| 食神 | 食 | `ForkKnife` | Eating god |
| 伤官 | 伤 | `PenNib` | Hurting officer |
| 偏财 | 财偏 | `Coins` | Indirect wealth |
| 正财 | 财 | `Wallet` | Direct wealth |
| 七杀 | 杀 | `Scissors` | Seven killings |
| 偏官 | 官偏 | `Shield` | Indirect officer |
| 正官 | 官 | `Crown` | Direct officer |
| 偏印 | 印偏 | `Stamp` | Indirect seal |
| 正印 | 印 | `SealCheck` | Direct seal |

Each label includes a `title` attribute or `aria-describedby` with the English translation for accessibility.

## 9. Testing

- axe-core: 0 violations.
- NVDA / VoiceOver in Chinese and English.
- Color contrast verified per pair in §3 above.
- Keyboard-only navigation across chart comparison flow.
- Reduced-motion: any chart animation collapses to static.
- All visible strings free of em-dash character.