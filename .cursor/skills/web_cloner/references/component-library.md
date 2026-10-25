# Component Library · Signature Effects from motionsites.ai

> Extracted from 11 real clone prompts. When a screenshot shows these effects, **copy the exact code into the prompt** rather than re-describing.

---

## 1. Liquid Glass ★★ Highest Frequency

```css
.liquid-glass {
  background: rgba(255, 255, 255, 0.01);
  background-blend-mode: luminosity;
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  border: none;
  box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1);
  position: relative;
  overflow: hidden;
}

.liquid-glass::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  padding: 1.4px;
  background: linear-gradient(
    180deg,
    rgba(255,255,255,0.45) 0%,
    rgba(255,255,255,0.15) 20%,
    rgba(255,255,255,0)   40%,
    rgba(255,255,255,0)   60%,
    rgba(255,255,255,0.15) 80%,
    rgba(255,255,255,0.45) 100%
  );
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}

.liquid-glass:hover {
  background: rgba(255, 255, 255, 0.04);
  box-shadow: inset 0 1px 2px rgba(255, 255, 255, 0.15);
}

.liquid-glass:active {
  transform: scale(0.98);
}

/* Strong variant */
.liquid-glass-strong {
  backdrop-filter: blur(50px);
  -webkit-backdrop-filter: blur(50px);
  box-shadow: 4px 4px 4px rgba(0,0,0,0.05), inset 0 1px 1px rgba(255,255,255,0.15);
}
```

### Tailwind Utility Classes
```html
<!-- Glass card -->
<div class="bg-white/5 backdrop-blur-md rounded-2xl border border-white/10">
  <!-- content -->
</div>

<!-- Glass button -->
<button class="bg-white/10 hover:bg-white/20 backdrop-blur-sm rounded-full px-6 py-3">
  <!-- content -->
</button>
```

---

## 2. FadingVideo · rAF Crossfade

```tsx
const FADE_MS = 500;
const FADE_OUT_LEAD = 0.55;

function FadingVideo({ src, className }: { src: string | string[], className?: string }) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const rafRef = useRef<number>(0);
  const fadeRef = useRef({ from: 0, to: 1, startTime: 0 });

  const fadeTo = (target: number) => {
    const video = videoRef.current;
    if (!video) return;
    cancelAnimationFrame(rafRef.current);
    fadeRef.current = { from: parseFloat(video.style.opacity || '0'), to: target, startTime: performance.now() };
    const step = (now: number) => {
      const progress = Math.min((now - fadeRef.current.startTime) / FADE_MS, 1);
      video.style.opacity = String(fadeRef.current.from + (fadeRef.current.to - fadeRef.current.from) * progress);
      if (progress < 1) rafRef.current = requestAnimationFrame(step);
    };
    rafRef.current = requestAnimationFrame(step);
  };

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;
    video.style.opacity = '0';
    video.addEventListener('loadeddata', () => { video.play(); fadeTo(1); });
    video.addEventListener('timeupdate', () => {
      if (!video.paused && video.duration - video.currentTime <= FADE_OUT_LEAD && video.duration - video.currentTime > 0) {
        fadeTo(0);
      }
    });
    video.addEventListener('ended', () => {
      fadeTo(0);
      setTimeout(() => { if (video) { video.currentTime = 0; video.play(); fadeTo(1); } }, 100);
    });
    return () => { cancelAnimationFrame(rafRef.current); video.pause(); };
  }, [src]);

  return <video ref={videoRef} src={src} autoPlay muted loop playsInline className={className} />;
}
```

---

## 3. BlurText · Word-by-Word Blur-In

```tsx
import { motion } from 'framer-motion';

function BlurText({ text, className = '' }: { text: string; className?: string }) {
  const words = text.split(' ');
  return (
    <div className={`flex flex-wrap justify-center ${className}`}>
      {words.map((word, i) => (
        <motion.span
          key={i}
          initial={{ filter: 'blur(10px)', opacity: 0, y: 50 }}
          whileInView={{ filter: 'blur(0px)', opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: i * 0.1, ease: 'easeOut' }}
          viewport={{ once: true, amount: 0.1 }}
          className="inline-block mr-2"
        >
          {word}
        </motion.span>
      ))}
    </div>
  );
}
```

---

## 4. FadeIn · Generic Delayed Fade

```tsx
import { motion } from 'framer-motion';

function FadeIn({ children, delay = 0, duration = 0.7, y = 30, className = '' }: any) {
  return (
    <motion.div
      initial={{ opacity: 0, y }}
      whileInView={{ opacity: 1, y: 0 }}
      transition={{ duration, delay, ease: [0.25, 0.1, 0.25, 1] }}
      viewport={{ once: true, margin: '50px' }}
      className={className}
    >
      {children}
    </motion.div>
  );
}
```

---

## 5. Gradient Text

```css
.gradient-text {
  background: linear-gradient(180deg, #646973 0%, #BBCCD7 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

---

## 6. Noise Overlay

```css
.noise-overlay {
  position: absolute;
  inset: 0;
  opacity: 0.15;
  pointer-events: none;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
  mix-blend-overlay: overlay;
}
```

---

## 7. Ken Burns / Hero Pseudo-Video

```css
@keyframes ken-burns {
  0% { transform: scale(1.04) rotate(-1.8deg) translate3d(-3%, -1.6%, 0); }
  100% { transform: scale(1.18) rotate(1.8deg) translate3d(3%, 1.6%, 0); }
}

.hero-bg {
  animation: ken-burns 18s ease-in-out infinite alternate;
  will-change: transform;
  transform-origin: center center;
}
```

---

## 8. CSS Keyframe Library

```css
@keyframes fade-up {
  from { opacity: 0; transform: translateY(24px); filter: blur(6px); }
  to { opacity: 1; transform: translateY(0); filter: blur(0); }
}

@keyframes fade-down {
  from { opacity: 0; transform: translateY(-16px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes hero-rise {
  from { opacity: 0; transform: translateY(64px) scale(0.97); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}

.animate-fade-up { animation: fade-up 0.9s cubic-bezier(0.22, 1, 0.36, 1) both; }
.animate-fade-down { animation: fade-down 0.7s cubic-bezier(0.22, 1, 0.36, 1) both; }
.animate-hero-rise { animation: hero-rise 1.1s cubic-bezier(0.22, 1, 0.36, 1) both; }

/* Stagger via inline style: animation-delay: 100ms, 220ms, 340ms, 460ms */

@media (prefers-reduced-motion: reduce) {
  .animate-fade-up, .animate-fade-down, .animate-hero-rise {
    animation: none;
    opacity: 1;
    transform: none;
  }
}
```

---

## 9. Dot Grid Pattern

```css
.dot-grid {
  background-image: radial-gradient(circle, rgba(255,255,255,0.5) 1px, transparent 1px);
  background-size: 24px 24px;
  opacity: 0.05;
}
```

---

## Quick Reference

| Effect | Tailwind | CSS |
|--------|----------|-----|
| Glass card | `bg-white/5 backdrop-blur-md rounded-2xl border border-white/10` | `.liquid-glass` |
| Glass button | `bg-white/10 hover:bg-white/20 backdrop-blur-sm rounded-full` | — |
| Gradient text | — | `.gradient-text` |
| Noise | — | `.noise-overlay` |
| Ken Burns | — | `@keyframes ken-burns` |
| Dot grid | — | `.dot-grid` |
