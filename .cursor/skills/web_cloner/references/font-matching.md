# Font Matching · Screenshot → Concrete Loadable Font

> **🔴 Hard Rule 1:** We are **cloning**, not designing from scratch. Fonts **must** be a **real, loadable font** with a **real load URL**. **Never write `[inferred, swap]`.**

---

## 1. Classification — Shape → Candidate Fonts

| Font Characteristic | Primary Fonts | Source | Cyrillic |
|---------------------|---------------|--------|----------|
| **High-contrast didone / fashion serif** (Vogue/香水感) | Playfair Display, Cormorant | Google Fonts | ✅ |
| **Swash/script wordmark** | Great Vibes, Pinyon Script | Google Fonts | Great Vibes ✅ |
| **Clean geometric UI** | Inter, Manrope, Geist | Google Fonts | ✅ |
| **Condensed heavy uppercase** | Oswald, Anton, Bebas Neue | Google Fonts | Oswald ✅ |
| **Monospace technical** | JetBrains Mono, Fira Code | Google Fonts | ✅ |
| **Old-style serif body** | Lora, Source Serif, Merriweather | Google Fonts | ✅ |
| **Elegant serif for headlines** | Instrument Serif (italic) | Google Fonts | ❌ |

---

## 2. Identification — Unknown Font → Exact Name

### URL Mode (has live page)
Skip image recognition — use DevTools directly:
1. `getComputedStyle(el).fontFamily`
2. Read `<link>` Google Fonts hrefs verbatim
3. Find `@font-face` / CDN URLs

### Screenshot Mode → Font Recognition Sites
1. **WhatTheFont** (myfonts.com/pages/whatthefont) — largest library
2. **Fontspring Matcherator** — independent foundry fonts
3. **WhatFontIs** (whatfontis.com) — 1M+ free+commercial fonts

**Cropping tips:** Clean single word, light-on-dark, straight, enlarged.

---

## 3. Load URL Resolution Priority

### a) Google Fonts (preferred)
```
https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400..900;1,400..900&display=swap
```

### b) Fontshare (modern SaaS fonts)
```
https://api.fontshare.com/v2/css?f[]=clash-display@400,500,600,700&display=swap
```

### c) Bunny Fonts (privacy-safe Google alternative)
```
https://fonts.bunny.net/css?family=prata:400
```

### d) Fontsource via jsDelivr
```
https://cdn.jsdelivr.net/npm/@fontsource/montserrat@5.2.8/cyrillic.css
```

### e) OnlineWebFonts (last resort)
```
<link href="https://db.onlinewebfonts.com/c/HASH?family=FONT+NAME" rel="stylesheet">
```
> ⚠️ Requires real hash from the site — do not fabricate.

---

## 4. Font Block Format

```html
<link href="https://fonts.googleapis.com/css2?family=PLAYFAIR+DISPLAY:ital,wght@0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=INTER:wght@300;400;500;600&display=swap" rel="stylesheet">
```

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      fontFamily: {
        serif: ['"Playfair Display"', 'serif'],
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
}
```

---

## 5. Common Mistakes

| Mistake | Fix |
|---------|-----|
| `[inferred, swap]` | Give a real font + URL |
| Cinzel / Italianno for Cyrillic | Use fonts with `cyrillic` subset |
| Fontshare for Russian text | Use Google Fonts instead |
| Fontsource `index.css` as CDN | Use per-subset CSS file |

---

## 6. Quick Reference Table

| Need | Use |
|------|-----|
| Luxury serif heading | Playfair Display |
| Modern UI/body | Inter |
| Heavy uppercase display | Oswald |
| Technical/monospace | JetBrains Mono |
| Elegant italic serif | Instrument Serif |
| Cyrillic body | Inter, Golos Text |
| Any Google Font URL | fonts.googleapis.com/css2?family=... |
