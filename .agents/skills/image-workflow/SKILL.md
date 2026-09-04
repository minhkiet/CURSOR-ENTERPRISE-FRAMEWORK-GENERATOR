---
name: image-workflow
description: Workflow kết hợp image-finder + image-generator + web-cloner. Tìm/tạo ảnh phù hợp cho website clone.
triggers:
  - "tìm ảnh"
  - "tạo ảnh"
  - "generate image"
  - "clone website"
  - "clone with images"
---

# Image Workflow - Kết hợp Image Finder + Generator + Web Cloner

## Tổng quan Workflow

```
Screenshot/URL → Web Cloner → Asset Manifest → Image Finder/Generator → Local Assets → Clone Website
```

## Phase 1: Asset Analysis

### Từ Screenshot
1. Identify tất cả images trong screenshot
2. Classify theo type (hero, avatar, icon, etc.)
3. Note colors, style, mood

### Từ URL
1. Extract existing image URLs
2. Check stability (404? CDN? Same-origin?)
3. Identify gaps

---

## Phase 2: Asset Strategy

### Decision Tree

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

---

## Phase 3: Image Finder (Stock First)

### Khi nào dùng

- Ảnh generic (office, nature, people, technology)
- Không cần custom branding
- Cần nhanh, miễn phí

### Sources

| Type | Source | URL |
|------|--------|-----|
| **Photos** | Unsplash | `images.unsplash.com` |
| **Photos** | Pexels | `images.pexels.com` |
| **Videos** | Pexels | `videos.pexels.com` |
| **Avatars** | Pravatar | `i.pravatar.cc` |
| **Avatars** | DiceBear | `api.dicebear.com` |

### Workflow

```bash
# 1. Search Unsplash
# Visit: unsplash.com/s/photos/keyword

# 2. Get direct URL
https://images.unsplash.com/photo-{ID}?w=1920&q=80&auto=format&fit=crop

# 3. Download to project
curl -L -o public/assets/image.webp "URL"

# 4. Verify
ls -la public/assets/image.webp
```

---

## Phase 4: Image Generator (Custom)

### Khi nào dùng

- Cần match specific color palette
- Cần custom composition
- Stock images không phù hợp
- Cần consistent style

### Providers

| Provider | Best For | API | Video |
|----------|----------|-----|-------|
| **Google Flow** | Free, quick | Browser only | ✅ 4s |
| **DALL-E 3** | Quality, consistency | OpenAI | ❌ |
| **Flux** | Speed, realism | Replicate | ❌ |
| **Stable Diffusion** | Custom, local | Various | ❌ |

### Workflow

```bash
# 1. Write prompt
PROMPT="Cinematic dark office, #0C0C0C background, #e8702a accent lights,
minimalist workspace, professional photography, 8k"

# 2. Generate via Google Flow (free)
# Visit: labs.google/fx/tools/flow
# Download result to public/assets/hero.png

# OR generate via DALL-E 3 (paid)
curl -X POST https://api.openai.com/v1/images/generations \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d "{
    \"prompt\": \"$PROMPT\",
    \"n\": 1,
    \"size\": \"1792x1024\",
    \"model\": \"dall-e-3\"
  }"

# 3. Download response
curl -L -o public/assets/hero.webp "RESPONSE_URL"

# 4. Optimize
cwebp -q 80 public/assets/hero.webp -o public/assets/hero.webp
```

---

## Phase 5: Integration

### Update Asset Manifest

```markdown
ASSET MANIFEST

## Stock Images (via image-finder)
HERO_BG [IMG, 16:9]:
  Source: Unsplash
  URL: https://images.unsplash.com/photo-{ID}?w=1920&q=80
  Local: public/assets/hero-bg.webp
  License: Free, no attribution

## Generated Images (via image-generator)
TEAM_PHOTO [IMG, 4:5]:
  Generator: DALL-E 3
  Prompt: Professional headshot, #0C0C0C background, corporate
  Local: public/assets/team-1.webp
```

### Update Clone Prompt

```markdown
## IMAGES
- Hero: ./public/assets/hero-bg.webp (Unsplash, cropped 16:9)
- Team: ./public/assets/team-*.webp (DALL-E 3 generated)
```

---

## Complete Example

### Input: Screenshot của một SaaS landing page

**Step 1:** Identify images
- Hero background (dark gradient)
- Team avatars (3 people)
- Feature icons (5 icons)
- Testimonial photo (1 person)

**Step 2:** Asset decisions
- Hero: Generate (need dark cinematic matching palette)
- Team: Generate (corporate portraits matching style)
- Icons: Use Lucide React (already in stack)
- Testimonial: Find stock (professional headshot)

**Step 3:** Execute

```bash
# Hero image - Google Flow (free)
# Visit: labs.google/fx/tools/flow
PROMPT="Cinematic dark office, #0C0C0C background, #e8702a accent lights,
minimalist workspace, professional photography, 8k"
# Download to public/assets/hero.webp

# Hero video - Google Flow (4s loop)
# Mode: Video
PROMPT="Slow pan across modern office, dark theme, orange lights, cinematic, loop"
# Download to public/assets/hero-loop.mp4

# Team - Google Flow (free)
PROMPT="Professional corporate headshot, neutral background matching #1a1a1a,
friendly smile, business attire, 4:5 portrait"
# Generate 3 variants, download

# Testimonial photo - Google Flow (free)
PROMPT="Professional headshot, warm smile, #2a2a2a background, business casual"
# Download to public/assets/testimonial.webp
```

**Step 4:** Final manifest

```markdown
ASSET MANIFEST
- HERO_IMG: public/assets/hero.webp (Google Flow, 1920x1080)
- HERO_VIDEO: public/assets/hero-loop.mp4 (Google Flow, 4s loop)
- TEAM_1: public/assets/team-1.webp (Google Flow, 800x1000)
- TEAM_2: public/assets/team-2.webp (Google Flow, 800x1000)
- TEAM_3: public/assets/team-3.webp (Google Flow, 800x1000)
- TESTIMONIAL: public/assets/testimonial.webp (Google Flow, 800x1000)
- ICONS: lucide-react (ArrowRight, Check, Star, etc.)
```

---

## Quality Checklist

- [ ] All images match page color palette
- [ ] Images saved in WebP format (or optimized alternative)
- [ ] 2x resolution for retina displays
- [ ] No text/watermarks in images
- [ ] Aspect ratios match usage (16:9 hero, 1:1 avatar, etc.)
- [ ] All images accessible via local paths
- [ ] Alt text added for accessibility

## Common Issues

| Issue | Solution |
|-------|----------|
| Color mismatch | Include exact hex in prompt |
| Generic AI look | Use specific composition reference |
| Text in image | Add "no text, no watermark" to prompt |
| Blurry | Generate at 2x resolution |
| Wrong style | Match photography style keywords |
