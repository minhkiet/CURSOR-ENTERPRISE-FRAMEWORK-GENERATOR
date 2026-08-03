---
description: AI Video Generation Skill - Auto-generate short videos (9:16) from URLs or text using HyperFrames rendering, OmniVoice TTS, and FFmpeg. Integrated from AI-auto-generate-video (huytranvan2010).
created: 2026-07-01
version: 1.0.0
updated: 2026-07-01
tags: [video, hyperframes, omnivoice, tts, short-video, tiktok, youtube-shorts, vietnamese, ffmpeg]
source: https://github.com/huytranvan2010/AI-auto-generate-video (118 stars, MIT License)
see_also: .cursor/rules/ref_frontend-frameworks.mdc (template system)
dependencies: [node>=22, ffmpeg, chromium, omnivoice-server]
---

# AI Video Generation Skill

## Tổng quan

Skill này tích hợp [AI-auto-generate-video](https://github.com/huytranvan2010/AI-auto-generate-video) - auto-generate video từ URL/article/text với HyperFrames rendering, OmniVoice TTS tiếng Việt, và FFmpeg.

**Source:** 118 stars · 70 forks · MIT License

```
┌─────────────────────────────────────────────────────────────────────┐
│                    VIDEO GENERATION PIPELINE                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  URL/Text → Claude Code → script.json → Template Pipeline           │
│                                        │                            │
│           ┌────────────────────────────┼────────────────────────┐   │
│           ▼                            ▼                        ▼   │
│    ┌─────────────┐            ┌─────────────┐          ┌──────────┐│
│    │  OmniVoice  │            │ HyperFrames │          │  FFmpeg  ││
│    │  (TTS)     │            │ (Render)    │          │  (Mux)   ││
│    └─────────────┘            └─────────────┘          └──────────┘│
│           │                            │                        │    │
│           └────────────────────────────┼────────────────────────┘    │
│                                        ▼                             │
│                              ┌──────────────────┐                   │
│                              │  video.mp4       │                   │
│                              │  voice.mp3       │                   │
│                              │  script.txt      │                   │
│                              └──────────────────┘                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Core Workflow

### Step 1: Content Input

```bash
# Via Claude Code (recommended)
/create-template-video https://example.com/article
/create-template-video path/to/article.txt
/create-template-video "Nội dung bài viết trực tiếp..."
```

### Step 2: Script Generation

Claude Code tạo `script.json` với cấu trúc:

```json
{
  "version": "1.0",
  "renderer": "hyperframes",
  "aspect": "9:16",
  "metadata": {
    "title": "Article Title",
    "source": { "url": "https://...", "domain": "example.com" }
  },
  "voice": { "provider": "omnivoice", "speed": 1.0 },
  "scenes": [
    {
      "id": "hook",
      "type": "hook",
      "voiceText": "Opening hook text...",
      "templateId": "frame-liquid-bg-hero",
      "inputs": { "headline": "...", "subheadline": "..." }
    }
  ]
}
```

### Step 3: Pipeline Execution

```bash
npm run pipeline -- output/<slug>/script.json
```

8 deterministic steps:
1. **Validate** - Zod schema check
2. **Caption text** - Generate script.txt
3. **TTS/scene** - OmniVoice per scene
4. **Concat voice** - Merge with gaps
5. **SFX mix** - Sound effects layer
6. **Render clips** - HyperFrames → MP4
7. **Concat + mux** - Final video
8. **Done** - Output paths

### Step 4: Output

```
output/<slug>-<timestamp>/
├── video.mp4          # Final 1080×1920 + audio + SFX
├── voice.mp3          # Narration track
├── script.txt         # Plain text for captions
├── clips/             # Per-scene clips
└── voice/             # Per-scene TTS
```

## Pre-Review Gate

### V.1 Prerequisites Check

- [ ] Node.js >= 22 installed
- [ ] FFmpeg + ffprobe in PATH
- [ ] Chromium available (HyperFrames)
- [ ] OmniVoice server running (default: http://127.0.0.1:8123)
- [ ] `.env.local` configured

### V.2 Input Validation

- [ ] URL accessible hoặc text content provided
- [ ] Content length: 3-12 scenes recommended
- [ ] Vietnamese TTS number handling (200MP = "hai trăm megapixel")

### V.3 Template Selection

- [ ] Scene type: hook → body (n) → outro
- [ ] Template exists in `templates/<id>/`
- [ ] Inputs match template slots

## Post-Review Gate

### V.4 Output Verification

- [ ] video.mp4 generated (1080×1920)
- [ ] voice.mp3 synced with video
- [ ] No encoding errors
- [ ] Idempotent: re-run produces same output

### V.5 Quality Check

- [ ] TTS audio clear, no truncation
- [ ] Scene transitions smooth
- [ ] SFX appropriately layered
- [ ] Text readable in 9:16 format

## Templates Reference

### Hook Templates (scenes[0])

| Template | Use Case |
|----------|----------|
| `frame-liquid-bg-hero` | Aurora hero + headline + CTA |

### Body Templates (scenes[1..n-1])

| Template | Use Case |
|----------|----------|
| `frame-vignelli` | Single stat, dark + red accent |
| `frame-pentagram-stat` | Hero number + bar chart |
| `frame-bold-poster` | Multi-line statement + giant figure |
| `frame-build-minimal` | Bold word, letter-by-letter |
| `frame-creative-voltage` | Slogan, electric-blue split |
| `frame-glitch-title` | Breaking/tech news, cyberpunk |
| `frame-aicoding-list` | List 2-5 items |
| `frame-aicoding-comparison` | Head-to-head comparison |

### Outro Templates (scenes[last])

| Template | Use Case |
|----------|----------|
| `frame-logo-outro` | Logo glow + name + tagline |
| `frame-statement-outro` | Red statement card |

## SFX System

SFX được chọn theo 3-tier system:

```
1. scene.sfx override   → exact file hoặc { "name": "none" }
2. semantic match       → voiceText keywords (cảnh báo→alert, kỷ lục→success)
3. scene-type default   → hook→hook, body→callout, outro→outro
```

**Lệnh quản lý SFX:**
```bash
npm run sfx:download   # Download SFX library
npm run sfx:filter     # Prune library
```

## Configuration

### Environment (.env.local)

```env
TTS_PROVIDER=omnivoice
OMNIVOICE_ENDPOINT=http://127.0.0.1:8123
```

### OmniVoice Server

Server phải accept:
- `POST /tts` với `{ text: string }`
- Return: `audio/mpeg`

## Tech Stack

| Layer | Technology |
|-------|------------|
| Runtime | Node ≥22, TypeScript 6, ESM, tsx |
| Render | HyperFrames 0.6.94 (HTML→MP4) |
| TTS | OmniVoice (local Vietnamese TTS) |
| Schema | Zod ^4 |
| A/V | FFmpeg + ffprobe |
| Tests | Vitest ^4 |

## Integration Points

### Với karpathy-coding

Video generation tasks cũng cần karpathy overlay:

```
User Request → karpathy-pre → [V.1-V.3 gates] → IMPLEMENT → [V.4-V.5 gates] → karpathy-post
```

### Với full-output

Complex video tasks (multi-template, custom SFX) nên combine với full-output skill.

## Vietnamese Content Best Practices

1. **Số**: "200" → "hai trăm" (OmniVoice không đọc số tiếng Anh)
2. **Độ dài scene**: 5-15 giây mỗi scene
3. **Hook**: Dưới 3 giây, gây tò mò
4. **Outro**: Logo + CTA + URL

## Troubleshooting

| Issue | Solution |
|-------|----------|
| TTS timeout | Check OmniVoice server, increase timeout |
| Render fail | Verify Chromium available, check template HTML |
| Mux error | Verify FFmpeg version, check audio codec |
| Font missing | Use Vietnamese-capable font stack |

## Links

- [AI-auto-generate-video](https://github.com/huytranvan2010/AI-auto-generate-video)
- [HyperFrames](https://www.npmjs.com/package/hyperframes)
- [[ref_frontend-frameworks]] - Template system reference
