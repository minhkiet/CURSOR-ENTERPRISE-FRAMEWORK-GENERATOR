---
name: image-generator
description: Tạo ảnh và video theo yêu cầu bằng AI (DALL-E, Google Flow, Midjourney, Stable Diffusion, Flux). Keywords: tạo ảnh, generate image, AI art, create image, drawing, illustration, tạo video, generate video, AI video.
---

# Image Generator Skill

Tạo ảnh theo yêu cầu cho website clone và web design.

## Khi nào dùng

- Tạo ảnh hero cho landing page
- Tạo illustrations/iconography theo style
- Tạo mockup images cho website
- Tạo background images theo màu sắc
- Thay thế ảnh stock bằng ảnh custom

## Các nền tảng AI Image & Video

### 1. Google Flow (labs.google/fx/tools/flow)

**Flow** by Google AI - miễn phí, tạo ảnh và video từ prompt. Tích hợp tốt với browser.

```bash
# Flow tại labs.google/fx/tools/flow
# - Miễn phí sử dụng
# - Tạo ảnh từ text prompt
# - Tạo video ngắn từ ảnh hoặc prompt
# - Style: photorealistic, illustrative, cinematic

# Cách sử dụng:
1. Truy cập: https://labs.google/fx/tools/flow
2. Nhập prompt mô tả ảnh/video
3. Chọn style (Image, Video, or Flow Mode)
4. Download kết quả
```

**Flow Modes:**
| Mode | Description | Use Case |
|------|-------------|----------|
| **Image** | Tạo ảnh tĩnh | Hero images, illustrations |
| **Video** | Tạo video ngắn 4s | Backgrounds, animations |
| **Flow** | Tạo video từ 2 ảnh | Smooth transitions |

**Flow API (via Browser Extension):**
```bash
# Sử dụng Flow qua trình duyệt
# Extension: Flow Browser Controller
# Hoặc sử dụng Playwright để automate

# Ví dụ Playwright automation:
npx playwright screenshot https://flow.google.com/generate \
  --prompt "modern workspace with dark theme" \
  --download-path ./assets/flow-output.png
```

**Prompt cho Flow:**
```bash
# Ảnh tĩnh
"minimalist workspace, dark theme #0C0C0C, orange accent lights,
professional photography, 8k"

# Video ngắn (4 giây)
"slow pan across modern office, golden hour lighting,
dark theme, cinematic, seamless loop"

# Flow transition
# Upload 2 ảnh đầu và cuối → Flow tạo video chuyển đổi mượt
```

### 2. OpenAI DALL-E

```bash
# Via API
curl https://api.openai.com/v1/images/generations \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "prompt": "modern office workspace, minimal design, #0C0C0C background, professional photography style",
    "n": 1,
    "size": "1792x1024",
    "model": "dall-e-3"
  }'
```

**Models:**
| Model | Resolution | Quality |
|-------|-------------|---------|
| `dall-e-3` | 1024x1024, 1024x1792, 1792x1024 | Highest, HD |
| `dall-e-2` | 256x256, 512x512, 1024x1024 | Good |

### 2. Flux (via Replicate)

```bash
# Flux Pro API
curl -X POST https://api.replicate.com/v1/predictions \
  -H "Authorization: Token $REPLICATE_API_TOKEN" \
  -d '{
    "version": "stability-ai/sdxl:...",
    "input": {
      "prompt": "modern office workspace, minimal",
      "aspect_ratio": "16:9",
      "guidance_scale": 3.5
    }
  }'
```

### 3. Midjourney (via Discord/API)

```bash
# Via Midjourney API (e.g., Thunderbit)
curl -X POST https://api.thunderbit.com/v1/midjourney \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "prompt": "modern office workspace --ar 16:9 --style raw"
  }'
```

### 4. Stable Diffusion (Local/Cloud)

```bash
# Via ComfyUI API
curl -X POST http://localhost:8188/prompt \
  -d '{"prompt": {"nodes": [...], "workflow": {...}}}'

# Via RunPod/other cloud
curl https://api.runpod.io/v2/stable-diffusion-v1-5/run \
  -H "Authorization: Bearer $API_KEY" \
  -d '{"input": {"prompt": "modern office"}}'
```

---

## Prompt Engineering cho Web Design

### Hero Images

```
Modern [subject] photography, [lighting style], [color palette matching #HEX],
[composition], [mood], ultra realistic, 8k, professional photography
```

**Ví dụ:**
```
Modern minimalist workspace, soft natural lighting, #0C0C0C and #E1E0CC color scheme,
centered composition, professional corporate photography, 8k resolution
```

### Illustrations/Icons

```
[Style] illustration of [subject], [color palette], flat design,
vector style, clean lines, minimal, [format]
```

**Ví dụ:**
```
Minimalist illustration of a cloud server, blue and white color scheme,
flat design, vector style, clean lines, SVG format
```

### Mockups

```
[Type] mockup, [device/context], [angle], [lighting],
realistic, high quality, [background]
```

**Ví dụ:**
```
MacBook Pro displaying dashboard interface, front view, 
soft studio lighting, white background, realistic mockup, 8k
```

---

## Color Palette Integration

**Critical:** Khi tạo ảnh cho clone website, phải match màu:

```bash
# Include palette in prompt
"modern office, color palette: #0C0C0C #E1E0CC #e8702a,
desaturated tones, matching website colors"

# Or reference specific brand
"workspace matching Apple's dark mode aesthetic, 
#1D1D1F background, #F5F5F7 text"
```

---

## Aspect Ratios

| Use Case | Ratio | Common Sizes |
|----------|-------|--------------|
| Hero/Landing | 16:9 | 1920x1080, 1792x1024 |
| Blog Featured | 3:2 | 1200x800 |
| Social (Instagram) | 1:1 | 1080x1080 |
| Social (Twitter) | 16:9 | 1200x675 |
| Portrait/Team | 4:5 | 800x1000 |
| Background | 21:9 | 2560x1080 |

---

## Style References

### Photography Styles
- `professional photography` - Thực tế, chuyên nghiệp
- `editorial photography` - Magazine style
- `cinematic photography` - Movie-like, moody
- `minimalist photography` - Clean, sparse

### Illustration Styles
- `flat design` - 2D, solid colors
- `isometric` - 3D on 2D plane
- `watercolor` - Soft, artistic
- `line art` - Outlines only

### Mood Keywords
- `corporate` / `professional` / `startup`
- `dark mode` / `light mode`
- `minimal` / `complex`
- `playful` / `serious`

---

## Workflow Integration

### Trong web-cloner workflow

1. **Analyze screenshot** → Identify image needs
2. **Write generation brief** → Match palette
3. **Call image generator** → Create image
4. **Download to project** → `public/assets/`
5. **Update asset manifest** → Reference local path

### Example Asset Manifest

```markdown
ASSET MANIFEST
target_asset_mode: image-gen-capable

HERO_BG [IMG, 16:9, generated]:
  Medium: cinematic aerial workspace
  Palette: #0C0C0C / #E1E0CC / #e8702a
  Negative: no text, no watermark, no logo
  Generator: DALL-E 3
  Local path: public/assets/hero-bg.webp

TEAM_AVATAR_1 [IMG, 1:1, generated]:
  Medium: professional headshot
  Style: corporate portrait
  Background: transparent
  Generator: DALL-E 3
  Local path: public/assets/avatar-1.webp
```

---

## Tips

1. **Always include color palette** in prompt
2. **Use negative prompts** to exclude unwanted elements
3. **Match style** to website aesthetic
4. **Generate multiple variants** and choose best
5. **Save as WebP** for better compression
6. **Generate at 2x size** for retina displays

---

## So sánh các nền tảng

| Platform | Image | Video | Giá | API | Best For |
|----------|-------|-------|------|-----|----------|
| **Google Flow** | ✅ | ✅ 4s | Miễn phí | Browser only | Quick prototyping, video backgrounds |
| **DALL-E 3** | ✅ | ❌ | Pay-per-use | ✅ | High quality images, consistency |
| **Flux** | ✅ | ❌ | Pay-per-use | ✅ | Fast, realistic |
| **Midjourney** | ✅ | ❌ | Subscription | ✅ | Artistic, creative |
| **Stable Diffusion** | ✅ | ❌ | Local/Free | ✅ | Custom, privacy |

### Recommendation cho Web Clone

| Use Case | Recommend | Why |
|----------|-----------|-----|
| Hero images | **DALL-E 3** or **Flow** | Consistent quality, color control |
| Video backgrounds | **Flow** | Free, 4s loops |
| Illustrations | **Flow** or **DALL-E 3** | Fast iteration |
| Batch generation | **DALL-E 3 API** | Programmatic control |
