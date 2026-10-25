---
name: image-finder
description: Tìm ảnh stock miễn phí và tạo ảnh/video bằng AI (Google Flow, Unsplash, Pexels, Pravatar). Keywords: tìm ảnh, stock image, free image, find image, tạo ảnh AI, generate image, Google Flow, video AI.
---

# Image Finder Skill

Tìm và tải ảnh stock miễn phí cho website clone và web design.

## Khi nào dùng

- Tìm ảnh thay thế cho website clone
- Cần ảnh stock cho landing page
- Tìm ảnh theo chủ đề cụ thể
- Tìm ảnh có độ phân giải cao

## Nguồn ảnh được hỗ trợ

| Nguồn | Loại | URL Pattern | Lưu ý |
|--------|------|-------------|--------|
| **Google Flow** | Image + Video (4s) | `labs.google/fx/tools/flow` | **Miễn phí** - AI tạo ảnh/video |
| **Unsplash** | Photos | `images.unsplash.com/photo-{ID}` | Free, no attribution |
| **Pexels** | Photos + Videos | `images.pexels.com/photos/` | Free commercial use |
| **Pixabay** | Photos + Videos | `pixabay.com/photos/` | Free, attribution appreciated |
| **Lorem Picsum** | Random/Placeholder | `picsum.photos/` | Seed-based for consistency |
| **Pravatar** | Avatars | `i.pravatar.cc/` | Real person avatars |
| **DiceBear** | Avatars | `api.dicebear.com/` | Generated avatars |

---

## Google Flow (AI Free - Image + Video)

**Flow** by Google AI - tạo ảnh và video ngắn miễn phí.

### Truy cập
```
https://labs.google/fx/tools/flow
```

### Features
- **Image Mode**: Tạo ảnh từ text prompt
- **Video Mode**: Tạo video ngắn 4 giây
- **Flow Mode**: Tạo video từ 2 ảnh đầu/cuối

### Prompt Examples

```bash
# Ảnh tĩnh - Hero image
"minimalist workspace, dark theme #0C0C0C, orange accent lights,
professional photography, 8k"

# Video ngắn - Background loop
"slow pan across modern office, golden hour, dark theme, cinematic, seamless loop"

# Video transition - Flow mode
# Upload: start-image.png + end-image.png
# Output: smooth animated transition
```

### Browser Automation (Optional)

```bash
# Nếu cần automate qua browser
# Sử dụng Playwright để screenshot Flow output

npx playwright screenshot \
  --browser chromium \
  "https://labs.google/fx/tools/flow" \
  --output ./assets/flow-result.png
```

---

## Cách tìm ảnh

### 1. Unsplash

```bash
# Tìm ảnh theo keyword
# Truy cập: unsplash.com/s/photos/keyword

# URL pattern cho direct link:
https://images.unsplash.com/photo-{PHOTO_ID}?w=1600&q=80&auto=format&fit=crop
```

**Thumbnails:**
```bash
# Small (400px)
https://images.unsplash.com/photo-{ID}?w=400&q=80

# Medium (1080px)  
https://images.unsplash.com/photo-{ID}?w=1080&q=80

# Large (1920px)
https://images.unsplash.com/photo-{ID}?w=1920&q=80
```

### 2. Pexels

```bash
# Tìm ảnh: pexels.com/search/keyword/

# Direct download URL:
https://images.pexels.com/photos/{PHOTO_ID}/pexels-photo-{PHOTO_ID}.jpeg?auto=compress&cs=tinysrgb&fit=crop&w=1600&h=900
```

### 3. Pixabay

```bash
# Tìm ảnh: pixabay.com/photos/search/keyword/

# CDN URL:
https://cdn.pixabay.com/photo/{YEAR}/{MONTH}/{DAY}/{PHOTO_ID}/...
```

### 4. Lorem Picsum (Placeholder)

```bash
# Random image (different each time)
https://picsum.photos/1920/1080

# Fixed seed (same image every time)
https://picsum.photos/seed/myseed/1920/1080

# Grayscale
https://picsum.photos/1920/1080?grayscale
```

### 5. DiceBear (Avatars)

```bash
# Adventurer style
https://api.dicebear.com/10.x/adventurer/svg?seed={NAME}

# Avataaars style
https://api.dicebear.com/10.x/avataaars/svg?seed={NAME}

# Bottts style
https://api.dicebear.com/10.x/bottts/svg?seed={NAME}

# Initials
https://api.dicebear.com/10.x/initials/svg?seed={NAME}&backgroundColor={HEX}
```

### 6. Pravatar (Real Avatars)

```bash
# Random avatar
https://i.pravatar.cc/150

# Specific avatar (1-70)
https://i.pravatar.cc/150?img=1
```

---

## Video Stock

| Nguồn | Pattern | Notes |
|--------|---------|--------|
| **Pexels Videos** | `videos.pexels.com/video-files/{ID}/...mp4` | Free, HD quality |
| **Coverr** | API requires key | Free, no attribution |

```bash
# Pexels Video URL pattern
https://videos.pexels.com/video-files/{ID}/{ID}-hd_1920_1080_30fps.mp4
```

---

## Lưu ý quan trọng

### ⚠️ Không dùng `source.unsplash.com`
```
# DEPRECATED - Returns 404
https://source.unsplash.com/1600x900/?keyword

# Thay bằng direct Unsplash URL
https://images.unsplash.com/photo-{ID}?w=1600
```

### ⚠️ Chỉ dùng CDN cho hotlinking
- Unsplash, Pexels cho phép hotlink
- Tốt nhất nên download về project

### ⚠️ Attribution
- Unsplash: Không bắt buộc nhưng nên ghi credit
- Pexels: Free commercial use
- Pixabay: Link back appreciated

---

## Common Image Types

### Hero/Landing Page
```bash
# Unsplash - nature/landscape
https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920&q=80

# Unsplash - business/tech
https://images.unsplash.com/photo-1497215728101-856f4ea42174?w=1920&q=80
```

### Team/About Page
```bash
# Pravatar avatars
https://i.pravatar.cc/400?img=1
https://i.pravatar.cc/400?img=2
https://i.pravatar.cc/400?img=3
```

### Placeholder Images
```bash
# With text overlay
https://picsum.photos/seed/placeholder/800/600

# Grayscale
https://picsum.photos/800/600?grayscale
```

---

## Workflow Integration

Trong web-cloner workflow, dùng image-finder khi:

1. **Screenshot mode**: Tạo generation brief → Tìm stock thay thế
2. **URL mode**: Thay thế ảnh không stable
3. **Fallback**: Khi không tạo được ảnh từ AI

### Ví dụ

```markdown
# Trong asset-sourcing.md của web-cloner:

HERO_IMAGE [IMG, 16:9]:
  Medium: modern office workspace
  Palette: match page tokens #0C0C0C / #E1E0CC
  Source: Unsplash
  URL: https://images.unsplash.com/photo-1497366216548-37526070297c?w=1920&q=80
```
