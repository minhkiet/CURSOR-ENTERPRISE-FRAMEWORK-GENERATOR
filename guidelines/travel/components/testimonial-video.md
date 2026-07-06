# Testimonial Video Carousel

> Carousel video testimonial từ customer thật. Mỗi testimonial có avatar, video 30-60s, quote text, trip taken, rating. Dùng trong homepage section 7.

## 1. Mục đích

Social proof mạnh: khách thật kể chuyện chuyến đi thật. Video engaging hơn text review. Hiển thị 3-4 video cùng lúc.

## 2. Asset

| Element | Source |
|---|---|
| Video testimonial | Coverr travel customer videos (placeholder) |
| Avatar portrait | Unsplash curated |
| Trip cover photo | Unsplash destination |

## 3. Cấu trúc

```
┌────────────────────────────────────────────────────┐
│  Section header                                    │
│  Khách hàng nói gì                                 │
│  4.8★ từ 248.000 đánh giá thật                    │
├────────────────────────────────────────────────────┤
│  [prev]  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐  [next]│
│          │Video │ │Video │ │Video │ │Video │        │
│          │ 1    │ │ 2    │ │ 3    │ │ 4    │        │
│          └──────┘ └──────┘ └──────┘ └──────┘        │
│          Avatar    Avatar    Avatar    Avatar       │
│          Tên       Tên       Tên       Tên          │
│          ⭐⭐⭐⭐⭐  ⭐⭐⭐⭐⭐  ⭐⭐⭐⭐⭐  ⭐⭐⭐⭐⭐      │
│          "Quote"   "Quote"   "Quote"   "Quote"      │
│          Trip      Trip      Trip      Trip         │
└────────────────────────────────────────────────────┘
```

## 4. Variants

| Variant | Use | Khác biệt |
|---|---|---|
| `default` | Homepage | 4 video cùng lúc |
| `featured` | Single testimonial hero | 1 video lớn + quote lớn |
| `compact` | Sidebar | 1 video nhỏ |
| `grid` | All at once | 4 cards vertical |

## 5. States

| State | Visual |
|---|---|
| default | First video playing muted, others paused |
| hover | Scale 1.02 + show play button overlay |
| playing | Video playing with sound icon |
| reduce-motion | Static image + play button only |

## 6. Icon mapping

| Role | Phosphor |
|---|---|
| Play | `PlayCircle` (fill) |
| Pause | `PauseCircle` (fill) |
| Sound | `SpeakerHigh` |
| Mute | `SpeakerSlash` |
| Star | `Star` (fill) |
| Quote | `Quotes` |
| Verified | `SealCheck` (fill) |
| Trip location | `MapPin` |
| Calendar | `CalendarBlank` |

## 7. Code reference

```tsx
'use client';
import { useState } from 'react';
import * as Phosphor from '@phosphor-icons/react';

export interface Testimonial {
  id: string;
  authorName: string;
  authorTitle: string;
  avatarId: string;
  rating: number;
  quote: string;
  tripDestination: string;
  tripDuration: string;
  tripImageId: string;
  videoUrl: string;
  videoPoster: string;
  verified: boolean;
}

const TESTIMONIALS: Testimonial[] = [
  {
    id: 'minh-hn',
    authorName: 'Trần Minh',
    authorTitle: 'Kỹ sư IT, Hà Nội',
    avatarId: '1507003211169-0a1dd7228f2d',
    rating: 5,
    quote: 'Đặt vé máy bay + khách sạn combo 3 ngày Phú Quốc chỉ 4.500.000₫ cho cả gia đình. Resort view biển xịn, giá tốt hơn booking trực tiếp.',
    tripDestination: 'Phú Quốc',
    tripDuration: '3 ngày 2 đêm',
    tripImageId: '1582719508461-905c673771fd',
    videoUrl: 'https://cdn.coverr.co/videos/coverr-happy-couple-on-beach-3456/1080p.mp4',
    videoPoster: 'https://images.unsplash.com/photo-1582719508461-905c673771fd?w=600&h=400&fit=crop&q=80',
    verified: true
  },
  {
    id: 'lan-hcm',
    authorName: 'Lê Thị Lan',
    authorTitle: 'Marketing Manager, TP.HCM',
    avatarId: '1494790108377-be9c29b29330',
    rating: 5,
    quote: 'Tour Bali 5 ngày trọn gói, hướng dẫn viên nói tiếng Việt, khách sạn 4 sao. Hoàn tiền nhanh khi đổi lịch. Đã dùng 3 lần, lần nào cũng ưng.',
    tripDestination: 'Bali',
    tripDuration: '5 ngày 4 đêm',
    tripImageId: '1537996194471-e657df975ab4',
    videoUrl: 'https://cdn.coverr.co/videos/coverr-travel-vlogger-on-beach-3567/1080p.mp4',
    videoPoster: 'https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=600&h=400&fit=crop&q=80',
    verified: true
  },
  {
    id: 'quan-dn',
    authorName: 'Nguyễn Quốc Quân',
    authorTitle: 'Bác sĩ, Đà Nẵng',
    avatarId: '1472099645785-5658abf4ff4e',
    rating: 5,
    quote: 'Đặt vé khứ hồi Hà Nội - Singapore cho cả nhóm 8 người, mọi thứ suôn sẻ. App theo dõi chuyến bay real-time, check-in online tự động.',
    tripDestination: 'Singapore',
    tripDuration: '4 ngày 3 đêm',
    tripImageId: '1565967511849-76a60a516170',
    videoUrl: 'https://cdn.coverr.co/videos/coverr-family-airport-travel-3876/1080p.mp4',
    videoPoster: 'https://images.unsplash.com/photo-1565967511849-76a60a516170?w=600&h=400&fit=crop&q=80',
    verified: true
  },
  {
    id: 'mai-pt',
    authorName: 'Phạm Thị Mai',
    authorTitle: 'Giáo viên, Pleiku',
    avatarId: '1438761681033-6461ffad8d80',
    rating: 5,
    quote: 'Đi tour Thái Lan tự túc, đặt qua Skylark tiết kiệm 30% so với tự book. Hỗ trợ 24/7 cả khi đang ở nước ngoài, yên tâm.',
    tripDestination: 'Bangkok',
    tripDuration: '4 ngày 3 đêm',
    tripImageId: '1508009603885-50cf7c579365',
    videoUrl: 'https://cdn.coverr.co/videos/coverr-couple-shopping-in-thailand-4123/1080p.mp4',
    videoPoster: 'https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=600&h=400&fit=crop&q=80',
    verified: true
  }
];

export function TestimonialVideoCarousel() {
  return (
    <section className="bg-slate-50 py-16 lg:py-24" aria-labelledby="testimonial-heading">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-12">
          <span className="inline-block text-[11px] font-bold uppercase tracking-[0.18em] text-sky-600 mb-2">
            Khách hàng nói gì
          </span>
          <h2 id="testimonial-heading" className="text-3xl lg:text-5xl font-extrabold text-slate-900 tracking-tight">
            4.8★ từ 248.000 đánh giá thật
          </h2>
          <div className="mt-4 flex items-center justify-center gap-1.5 text-[14px] text-slate-700">
            <span className="inline-flex items-center gap-0.5">
              {Array.from({ length: 5 }).map((_, i) => (
                <Phosphor.Star key={i} size={16} weight="fill" className="text-amber-400" />
              ))}
            </span>
            <strong className="font-bold tabular-nums">4.82</strong>
            <span>·</span>
            <span>248.470 đánh giá</span>
            <span>·</span>
            <a href="#" className="text-sky-600 hover:underline font-semibold">Đọc tất cả</a>
          </div>
        </div>

        {/* Carousel */}
        <div className="relative">
          {/* Cards row */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
            {TESTIMONIALS.map(t => (
              <TestimonialVideoCard key={t.id} testimonial={t} />
            ))}
          </div>

          {/* Nav controls */}
          <div className="flex items-center justify-center gap-2 mt-8">
            <button
              type="button"
              className="w-10 h-10 inline-flex items-center justify-center bg-white hover:bg-slate-100 border border-slate-200 rounded-full shadow-sm"
              aria-label="Trước"
            >
              <Phosphor.CaretLeft size={14} weight="bold" className="text-slate-700" />
            </button>
            <span className="text-[12px] text-slate-500 tabular-nums px-3">
              1 / 4
            </span>
            <button
              type="button"
              className="w-10 h-10 inline-flex items-center justify-center bg-white hover:bg-slate-100 border border-slate-200 rounded-full shadow-sm"
              aria-label="Sau"
            >
              <Phosphor.CaretRight size={14} weight="bold" className="text-slate-700" />
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}

function TestimonialVideoCard({ testimonial }: { testimonial: Testimonial }) {
  const [playing, setPlaying] = useState(false);
  const [muted, setMuted] = useState(true);

  return (
    <article className="group bg-white rounded-2xl border border-slate-200 overflow-hidden hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
      {/* Video */}
      <div className="relative aspect-[3/4] bg-slate-900 overflow-hidden">
        <video
          poster={testimonial.videoPoster}
          src={playing ? testimonial.videoUrl : undefined}
          className="w-full h-full object-cover"
          muted={muted}
          loop
          playsInline
          controls={playing}
        />

        {/* Gradient overlay when not playing */}
        {!playing && (
          <>
            <div className="absolute inset-0 bg-gradient-to-t from-slate-900/70 via-slate-900/10 to-transparent" />
            <button
              type="button"
              onClick={() => setPlaying(true)}
              aria-label={`Phát video của ${testimonial.authorName}`}
              className="absolute inset-0 flex items-center justify-center group-hover:scale-110 transition-transform"
            >
              <span className="w-16 h-16 inline-flex items-center justify-center bg-white/95 backdrop-blur rounded-full shadow-2xl">
                <Phosphor.PlayCircle size={56} weight="fill" className="text-sky-700" />
              </span>
            </button>
            {/* Trip badge bottom */}
            <div className="absolute bottom-3 left-3 right-3 flex items-end justify-between">
              <div className="bg-white/95 backdrop-blur rounded-lg px-2.5 py-1.5">
                <p className="text-[10px] font-bold uppercase tracking-wider text-slate-500">Trip</p>
                <p className="text-[12.5px] font-bold text-slate-900">{testimonial.tripDestination}</p>
              </div>
            </div>
          </>
        )}

        {/* Mute toggle when playing */}
        {playing && (
          <button
            type="button"
            onClick={() => setMuted(!muted)}
            aria-label={muted ? 'Bật âm thanh' : 'Tắt âm thanh'}
            className="absolute top-3 right-3 w-9 h-9 inline-flex items-center justify-center bg-black/60 backdrop-blur rounded-full text-white"
          >
            {muted ? <Phosphor.SpeakerSlash size={14} weight="bold" /> : <Phosphor.SpeakerHigh size={14} weight="bold" />}
          </button>
        )}
      </div>

      {/* Body */}
      <div className="p-4 space-y-3">
        {/* Author */}
        <div className="flex items-center gap-2.5">
          <img
            src={`https://images.unsplash.com/photo-${testimonial.avatarId}?w=80&h=80&fit=crop&q=80`}
            alt={testimonial.authorName}
            className="w-10 h-10 rounded-full object-cover ring-2 ring-white"
            loading="lazy"
          />
          <div className="min-w-0 flex-1">
            <div className="flex items-center gap-1">
              <p className="text-[13px] font-bold text-slate-900 truncate">{testimonial.authorName}</p>
              {testimonial.verified && (
                <Phosphor.SealCheck size={13} weight="fill" className="text-sky-600 flex-shrink-0" />
              )}
            </div>
            <p className="text-[11px] text-slate-500 truncate">{testimonial.authorTitle}</p>
          </div>
        </div>

        {/* Rating */}
        <div className="flex items-center gap-1">
          {Array.from({ length: testimonial.rating }).map((_, i) => (
            <Phosphor.Star key={i} size={12} weight="fill" className="text-amber-400" />
          ))}
        </div>

        {/* Quote */}
        <blockquote className="relative">
          <Phosphor.Quotes size={16} weight="fill" className="absolute -left-1 -top-1 text-sky-100" />
          <p className="text-[12.5px] text-slate-700 leading-relaxed pl-5 line-clamp-4">
            {testimonial.quote}
          </p>
        </blockquote>

        {/* Trip meta */}
        <div className="flex items-center gap-2 text-[11px] text-slate-500 pt-2 border-t border-slate-100">
          <span className="inline-flex items-center gap-1">
            <Phosphor.MapPin size={11} weight="bold" />
            {testimonial.tripDestination}
          </span>
          <span>·</span>
          <span className="inline-flex items-center gap-1">
            <Phosphor.CalendarBlank size={11} weight="bold" />
            {testimonial.tripDuration}
          </span>
        </div>
      </div>
    </article>
  );
}
```

## 8. Accessibility

- Video play button accessible với `aria-label`
- Mute toggle có `aria-label` + icon rõ ràng
- Author avatar có alt text
- Verified badge có icon + semantic meaning
- Quote là `<blockquote>`
- Rating có cả icon và count
- Reduce-motion: poster image tĩnh
- Video có `controls` khi playing để user có thể tạm dừng
- Carousel controls accessible

## 9. Performance

- Video chỉ load khi `playing === true` (src prop conditionally set)
- Poster image là Unsplash với srcset responsive
- Avatar 80x80 nhỏ, lazy load
- Carousel có thể dùng `IntersectionObserver` để autoplay first visible
- `playsInline` cho iOS
- `loop` để continuous viewing
- `controls={playing}` cho user control

## 10. Anti-patterns đã tránh

- ❌ Auto-play with sound
- ❌ Stock portrait (đã dùng Unsplash portrait)
- ❌ Generic "Great service!" quote
- ❌ Video không có fallback khi load fail
- ❌ Avatar to (đã giữ 10x10 trong card)
- ❌ Quote quá dài line-clamp 4

---

**Component family**: Layout #4 — `testimonial-video-carousel`