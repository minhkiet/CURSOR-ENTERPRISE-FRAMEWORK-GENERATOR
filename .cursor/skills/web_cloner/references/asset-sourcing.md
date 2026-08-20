# Asset Sourcing · Zero-User-Work Media Specs

> **🔴 Hard Rule 2:** The deliverable is a **portable, single text prompt**. Goal: the AI that consumes it completes every asset with **zero work handed back to the user**.
>
> `REPLACE-ME` / `placehold.co` is **banned**.

---

## Decision Priority

```
① URL抽取 [URL mode default] → stable public assets as primary
② 生成简报 [Screenshot mode default] → generation briefs
③ image-workflow [integrated] → image-finder (stock) → image-generator (AI)
④ stock直链兜底 [fetch-only only] → one verified free URL
⑤ 截图裁切 [pixel-exact 1:1 only] → last resort
```

---

## Integrated Image Workflow

### Phase 1: Asset Analysis
1. Identify images from screenshot/URL
2. Classify by type (hero, avatar, icon, etc.)
3. Note colors, style, mood

### Phase 2: Asset Strategy

```
Is asset available in URL?
├── YES: Is it stable/public CDN?
│   ├── YES → Use original URL
│   └── NO → Use as reference, generate replacement
└── NO (Screenshot mode)
    ├── Is it generic stock image?
    │   ├── YES → Search via image-finder
    │   └── NO → Generate via image-generator
    └── Is it specific/unique?
        └── YES → Generate via image-generator
```

### Phase 3: Image Finder (Stock First)

For generic images (office, nature, people, technology):

| Source | Type | URL Pattern |
|--------|------|-------------|
| **Unsplash** | Photos | `images.unsplash.com/photo-{ID}` |
| **Pexels** | Photos | `images.pexels.com/photos/` |
| **Pravatar** | Avatars | `i.pravatar.cc/` |
| **DiceBear** | Avatars | `api.dicebear.com/` |

```bash
# Download stock image
curl -L -o public/assets/image.webp "https://images.unsplash.com/photo-{ID}?w=1920&q=80"
```

### Phase 4: Image Generator (Custom)

For specific images matching palette/style:

**Providers:**
| Provider | Best For | API |
|----------|----------|-----|
| **DALL-E 3** | Quality, consistency | OpenAI |
| **Flux** | Speed, realism | Replicate |
| **Stable Diffusion** | Custom, local | Various |

**Prompt Template:**
```
Modern [subject], [lighting style], [color palette: #HEX #HEX #HEX],
[composition], [mood], professional photography, 8k
```

**Example:**
```
Modern minimalist workspace, soft natural lighting, #0C0C0C and #E1E0CC color scheme,
centered composition, professional corporate photography, 8k resolution
```

---

## 1. URL Extraction (URL Mode Default)

Extract and verify:
- `<img>` / `<video>` / `<source>` src
- CSS `background-image: url(...)`
- `@font-face` URLs
- Inline SVG paths

**Keep full URLs with query params:**
```
https://images.unsplash.com/photo-ID?w=1280&q=85&auto=format&fit=crop
```

**Verification:** HEAD/GET returns 200, not login page/403/signed URL.

---

## 2. Generation Briefs (Screenshot Mode Default)

Write **production-level briefs** for each image/video:

### Image Brief Template

**Using image-workflow skills:**
```
Asset Type: [hero/avatar/product/bg]
Medium: [photoreal editorial photo / cinematic still / clean 3D render]
Camera: [top-down drone / high oblique / eye-level / macro close-up]
Composition: [subject placement, focal area, safe area for text]
Palette lock: match page tokens exactly #HEX / #HEX / #HEX
  - Desaturated tones only, avoid off-palette hues
Lighting: [golden hour / overcast / soft studio / rim light]
Subject: [specific details, not generic]
Negative constraints: no visible text, no watermark, no logo, no UI
Delivery: object-cover, object-position X% Y%, save as [ASSET_NAME]
Source Strategy: [image-finder (stock) / image-generator (AI)]
```

**Complete Example (Hero):**
```markdown
HERO_BG [IMG, 16:9]:
  Asset Type: Hero background
  Medium: cinematic aerial workspace
  Camera: high angle, centered
  Palette: match #0C0C0C / #E1E0CC / #e8702a
  Lighting: soft ambient, subtle orange accent lights
  Subject: modern minimalist office, 3-4 people working, glass walls
  Negative: no text, no watermark, no logo
  Source Strategy: image-generator (DALL-E 3)
  Local path: public/assets/hero-bg.webp
```

**Complete Example (Avatar):**
```markdown
TEAM_PHOTO_1 [IMG, 1:1]:
  Asset Type: Team member avatar
  Medium: professional headshot
  Camera: eye-level, centered
  Palette: match #1a1a1a background
  Subject: friendly professional, business attire, diverse ethnicity
  Negative: no text, no watermark
  Source Strategy: image-generator (DALL-E 3)
  Local path: public/assets/avatar-1.webp
```

**Complete Example (Stock Fallback):**
```markdown
TESTIMONIAL_BG [IMG, 4:3]:
  Asset Type: testimonial section background
  Medium: abstract gradient
  Palette: match #0C0C0C → #1a1a1a gradient
  Source Strategy: image-finder (Unsplash)
  Unsplash URL: https://images.unsplash.com/photo-{ID}?w=1200&q=80
  Local path: public/assets/testimonial-bg.webp
```

### Video Brief Template
```
Medium: [seamless looping drone clip / cinematic footage]
Duration: 6-10s seamless loop
Palette: match #HEX / #HEX / #HEX
Lighting: [description]
Negative: no text, no watermark
Delivery: autoplay muted loop playsinline object-cover
Fallback: generate still image + CSS motion
```

### Mockup/Device Screens
```
For device mockups: describe the SCREEN UI layout in the brief.
NOT blank screen — unless the reference is genuinely blank.
```

---

## 3. Stock Fallback Sources

| Source | Type | URL Pattern | Notes |
|--------|------|-------------|-------|
| **Unsplash** | Images | `https://images.unsplash.com/photo-ID?w=1600&q=80` | Free, no attribution |
| **Pexels Videos** | Video | `https://videos.pexels.com/video-files/ID/...mp4` | Free commercial use |
| **DiceBear** | Avatars | `https://api.dicebear.com/10.x/persona/svg?seed=NAME` | Generated avatars |

> ⚠️ `source.unsplash.com` is **deprecated** (June 2024) — returns 404.

---

## 4. Screenshot Cropping (Last Resort)

Only when screenshot pixel-exact is required:

```bash
# macOS sips
sips -c HEIGHT WIDTH --cropOffset Y X screenshot.png --out output.png

# ImageMagick
magick screenshot.png -crop WxH+X+Y +repage output.png
```

---

## 5. Icons

- **Preferred:** `lucide-react` named icons (`ArrowRight`, `Menu`, `X`, `Check`, `Play`)
- **Fallback:** Inline SVG path data for exact geometry

---

## 6. Asset Manifest Format

```markdown
ASSET MANIFEST
target_asset_mode: image-gen-capable

HERO_BG [IMG, 16:9]:
  Medium: cinematic aerial of [subject]
  Palette: match #0C0C0C / #E1E0CC / #e8702a
  No text, no watermark
  object-cover, object-position center

CARD_IMG_1 [IMG, 4:5]:
  Medium: [description]
  Palette: match page tokens
  No text, no logo

LOGO [SVG]:
  Inline SVG — see Custom Components block
```

---

## 7. Common Mistakes

| Mistake | Why It's Wrong |
|---------|----------------|
| `REPLACE-ME` | Leaves work for the user |
| `placehold.co` | Unprofessional, breaks design |
| `source.unsplash.com` | Deprecated, returns 404 |
| Blank screen for device mockup | Wrong when reference shows UI |
| Generic "hero image" | Not specific enough to match style |
