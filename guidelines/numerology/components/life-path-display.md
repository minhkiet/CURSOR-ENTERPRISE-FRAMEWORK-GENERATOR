# Life Path Number Display

> Component hiển thị Life Path Number. Đây là hero của numerology report, phải đọc ấn tượng ngay.

## 1. Mục đích

Hiển thị con số Life Path (1–9, 11, 22, 33) làm trung tâm. Phải thể hiện ceremonial importance, không phải calculator.

## 2. Icon system

| Role | Icon Phosphor | Size |
|---|---|---|
| Compass (life path) | `Compass` (fill) | 32px, gold |
| Sparkle (insight) | `Sparkle` (fill) | 16px, goldBright |
| Star burst | `StarFour` (fill) | 96px, goldBright |
| Eye (preview) | `Eye` | 14px |
| Share | `ShareNetwork` | 16px |
| Save | `BookmarkSimple` | 16px |

## 3. Hình ảnh

| Element | Source |
|---|---|
| Constellation backdrop | `https://picsum.photos/seed/constellation-{n}-night-sky/1200/800` |
| Mystic seal | `https://picsum.photos/seed/mystic-seal-purple/200/200` |
| Decorative mandala | `https://picsum.photos/seed/mandala-purple-gold/400/400` |

## 4. Cấu trúc

```
┌──────────────────────────────────────┐
│   [constellation backdrop blurred]   │
│                                      │
│      ✦  LIFE PATH  ✦                 │ ← eyebrow
│                                      │
│            7                         │ ← HUGE number (156px Cormorant)
│                                      │
│      The Seeker                      │ ← archetype name
│                                      │
│  "Bạn sinh ra để khám phá chiều sâu  │
│   của sự tồn tại..."                │ ← one-line intro
└──────────────────────────────────────┘
```

## 5. Variants

| Variant | Use |
|---|---|
| `hero` | Full-screen reveal moment, 156px numeral |
| `inline` | Reading body, 76.5px numeral |
| `compact` | Sidebar widget, 56.5px numeral |

## 6. States

| State | Visual |
|---|---|
| loading | Pulse shimmer on gold numeral |
| revealed | Star burst behind numeral on entry |
| focus | goldBright halo |

## 7. Tokens

| Token | Value |
|---|---|
| Numeral font | Cormorant Garamond 700 |
| Numeral color | `#d4af37` gold |
| Numeral size (hero) | 156px |
| Numeral size (inline) | 76.5px |
| Glow | `0 0 24px rgba(212, 175, 55, 0.40)` |
| Eyebrow spacing | tracking 0.20em uppercase |

## 8. Code reference

```tsx
"use client";
import { motion, useReducedMotion } from "motion/react";

export function LifePathDisplay({ number, archetype, intro, seed }: {
  number: number;
  archetype: string;
  intro: string;
  seed: string;
}) {
  const reduce = useReducedMotion();
  return (
    <section class="relative overflow-hidden bg-[#0f0a1f] py-32 px-6 text-center">
      <div class="absolute inset-0 opacity-30 pointer-events-none">
        <img
          src={`https://picsum.photos/seed/constellation-${seed}-night-sky/1200/800`}
          alt=""
          aria-hidden="true"
          class="w-full h-full object-cover"
          style={{ filter: 'hue-rotate(280deg) saturate(0.85) brightness(0.50) blur(2px)' }}
        />
      </div>

      <div class="relative max-w-3xl mx-auto">
        <motion.div
          initial={reduce ? false : { opacity: 0, scale: 0.6 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
          class="flex items-center justify-center gap-3 mb-8"
        >
          <Phosphor.Sparkle size={14} weight="fill" class="text-[#fbbf24]" aria-hidden="true" />
          <span class="font-mono text-[11px] uppercase tracking-[0.20em] text-[#d4af37]">
            Life Path
          </span>
          <Phosphor.Sparkle size={14} weight="fill" class="text-[#fbbf24]" aria-hidden="true" />
        </motion.div>

        <motion.div
          initial={reduce ? false : { opacity: 0, scale: 0.4 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 1.2, ease: [0.16, 1, 0.3, 1], delay: 0.2 }}
          class="relative inline-block"
        >
          <div class="absolute inset-0 flex items-center justify-center pointer-events-none">
            <Phosphor.StarFour size={240} weight="fill" class="text-[#d4af37] opacity-20" aria-hidden="true" />
          </div>
          <span
            class="relative block font-display font-bold text-[#d4af37] leading-none tabular-nums"
            style={{ fontSize: 'clamp(120px, 22vw, 156px)', textShadow: '0 0 24px rgba(212, 175, 55, 0.40)' }}
            aria-label={`Life Path ${number}`}
          >
            {number}
          </span>
        </motion.div>

        <motion.h2
          initial={reduce ? false : { opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
          class="mt-6 font-display text-[42.5px] text-[#f5e9d0]"
        >
          The {archetype}
        </motion.h2>

        <motion.p
          initial={reduce ? false : { opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.8 }}
          class="mt-6 font-display italic text-[18px] text-[#b8b3cf] leading-relaxed max-w-2xl mx-auto"
        >
          &ldquo;{intro}&rdquo;
        </motion.p>

        <motion.div
          initial={reduce ? false : { opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.6, delay: 1.0 }}
          class="mt-10 flex items-center justify-center gap-6"
        >
          <button
            type="button"
            class="inline-flex items-center gap-2 px-4 py-2 bg-[#1c1635] border border-[rgba(212,175,55,0.30)] rounded-md text-[12.5px] font-medium text-[#f5e9d0] hover:bg-[#2a1f47] hover:border-[#fbbf24] transition-all"
          >
            <Phosphor.BookmarkSimple size={14} weight="bold" aria-hidden="true" />
            Lưu lại
          </button>
          <button
            type="button"
            class="inline-flex items-center gap-2 px-4 py-2 bg-[#d4af37] text-[#0f0a1f] rounded-md text-[12.5px] font-bold hover:bg-[#fbbf24] active:scale-[0.98] transition-all"
          >
            <Phosphor.ShareNetwork size={14} weight="bold" aria-hidden="true" />
            Chia sẻ
          </button>
        </motion.div>
      </div>
    </section>
  );
}
```