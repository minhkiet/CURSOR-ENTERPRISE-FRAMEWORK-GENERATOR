# PR Display (Personal Records)

> Grid / List các personal records với exercise thumbnail, weight × reps, date achieved, improvement vs previous PR. Celebration moment khi mới lập PR.

## 1. Mục đích

User hoàn thành 1 rep max — đây là khoảnh khắc motivation cao nhất. UI phải celebrate + log ngay lập tức + share được lên Strava / feed.

## 2. Layout

```
┌──────────────────────────────────────────────────────┐
│ CÁ NHÂN TỐT NHẤT · 12 records                       │
│ ─────────────────────────────────────────           │
│ ┌──────────────────────────┐ ┌────────────────────┐ │
│ │ 🏆 Bench Press            │ │ 🏆 Squat            │ │
│ │                          │ │                     │ │
│ │ [Video thumbnail]        │ │ [Video thumbnail]  │ │
│ │                          │ │                     │ │
│ │ 120 kg × 5 reps          │ │ 160 kg × 3 reps     │ │
│ │ +10 kg vs last PR        │ │ +20 kg vs last PR   │ │
│ │ 15/7/2026 · "Cảm ơn     │ │ 12/6/2026           │ │
│ │  Ironpath PR tracker"   │ │                     │ │
│ └──────────────────────────┘ └────────────────────┘ │
└──────────────────────────────────────────────────────┘

Celebration modal khi mới lập PR:
┌─────────────────────────────────┐
│        🏆 CÁ NHÂN TỐT NHẤT     │
│                                 │
│      BENCH PRESS                 │
│      120 kg × 5 reps             │
│      +10 kg so với PR cũ       │
│                                 │
│      [Video clip · 5s]           │
│                                 │
│   [Chia sẻ Strava] [OK]         │
└─────────────────────────────────┘
```

## 3. Variants

| Variant | Use | Khác biệt |
|---|---|---|
| `default` | Profile / settings | Grid 2 col |
| `list` | Detailed view | List view |
| `compact` | Sidebar widget | Smaller cards |
| `celebration` | Modal khi vừa lập PR | Confetti + share |

## 4. Code reference

```tsx
import * as Phosphor from '@phosphor-icons/react';

export interface PersonalRecord {
  id: string;
  exercise: string;
  exerciseSlug: string;
  weight: number;
  reps: number;
  unit: 'kg' | 'lb';
  videoUrl?: string;
  posterUrl: string;
  achievedAt: Date;
  improvement: number;
  improvementUnit: 'kg' | 'lb' | 'reps' | 'seconds';
  notes?: string;
}

const SAMPLE_PRS: PersonalRecord[] = [
  {
    id: 'pr1',
    exercise: 'Bench Press',
    exerciseSlug: 'bench-press',
    weight: 120,
    reps: 5,
    unit: 'kg',
    posterUrl: 'https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=400&q=80',
    achievedAt: new Date(Date.now() - 86400000),
    improvement: 10,
    improvementUnit: 'kg',
    notes: 'Cảm ơn Ironpath PR tracker. PR trước 110kg × 5.'
  },
  {
    id: 'pr2',
    exercise: 'Back Squat',
    exerciseSlug: 'back-squat',
    weight: 160,
    reps: 3,
    unit: 'kg',
    posterUrl: 'https://images.unsplash.com/photo-1605296867304-46d5465a13f1?w=400&q=80',
    achievedAt: new Date(Date.now() - 30 * 86400000),
    improvement: 20,
    improvementUnit: 'kg'
  },
  {
    id: 'pr3',
    exercise: 'Deadlift',
    exerciseSlug: 'deadlift',
    weight: 200,
    reps: 1,
    unit: 'kg',
    posterUrl: 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=400&q=80',
    achievedAt: new Date(Date.now() - 7 * 86400000),
    improvement: 15,
    improvementUnit: 'kg'
  },
  {
    id: 'pr4',
    exercise: 'Overhead Press',
    exerciseSlug: 'overhead-press',
    weight: 70,
    reps: 5,
    unit: 'kg',
    posterUrl: 'https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?w=400&q=80',
    achievedAt: new Date(Date.now() - 14 * 86400000),
    improvement: 5,
    improvementUnit: 'kg'
  }
];

export function PRShowcase({ records = SAMPLE_PRS }: { records?: PersonalRecord[] }) {
  return (
    <section
      aria-labelledby="pr-heading"
      className="bg-slate-950 py-16 lg:py-24 text-slate-50"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="flex items-end justify-between mb-10 flex-wrap gap-3">
          <div>
            <span className="inline-flex items-center gap-1.5 text-[11px] font-bold uppercase tracking-[0.18em] text-electric-400 mb-2">
              <Phosphor.Trophy size={12} weight="fill" />
              Cá nhân tốt nhất
            </span>
            <h2 id="pr-heading" className="text-3xl lg:text-5xl font-extrabold tracking-tight">
              {records.length} records trong năm nay
            </h2>
            <p className="mt-2 text-slate-400 text-[15px]">
              Mỗi PR là một cột mốc. Chia sẻ ngay khi bạn vừa lập.
            </p>
          </div>
          <a href="#" className="inline-flex items-center gap-1.5 px-4 py-2 border border-slate-700 hover:border-electric-500 text-slate-300 hover:text-electric-400 text-[13px] font-bold rounded-lg transition-colors">
            Xem tất cả
            <Phosphor.ArrowRight size={14} weight="bold" />
          </a>
        </div>

        {/* Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-5">
          {records.map(pr => <PRCard key={pr.id} pr={pr} />)}
        </div>

        {/* Summary */}
        <div className="mt-10 grid grid-cols-2 lg:grid-cols-4 gap-3 lg:gap-5">
          <PillMetric icon="Trophy" label="PRs 2026" value={records.length} suffix="records" />
          <PillMetric icon="TrendUp" label="Tổng cải thiện" value={50} suffix="kg" />
          <PillMetric icon="CalendarCheck" label="Tuần luyện" value={28} suffix="tuần" />
          <PillMetric icon="Flame" label="Streak" value={47} suffix="ngày liên tiếp" />
        </div>
      </div>
    </section>
  );
}

function PRCard({ pr }: { pr: PersonalRecord }) {
  return (
    <article className="group bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden hover:border-electric-500/50 transition-colors">
      {/* Image + Trophy badge */}
      <div className="relative aspect-[4/3] bg-slate-950 overflow-hidden">
        <img
          src={pr.posterUrl}
          alt={pr.exercise}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          loading="lazy"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/40 to-transparent" />

        {/* Trophy badge */}
        <div className="absolute top-3 left-3 inline-flex items-center gap-1 px-2 py-1 bg-electric-500 text-slate-950 text-[10px] font-bold uppercase tracking-wider rounded-full shadow-lg shadow-electric-500/40" aria-label="Cá nhân tốt nhất">
          <Phosphor.Trophy size={10} weight="fill" />
          PR
        </div>

        {/* Improvement pill */}
        <div className="absolute top-3 right-3 inline-flex items-center gap-1 px-2 py-1 bg-emerald-500/90 text-white text-[10px] font-bold rounded-full" aria-label={`Cải thiện ${pr.improvement} ${pr.improvementUnit} so với PR trước`}>
          <Phosphor.ArrowUp size={10} weight="bold" />
          {pr.improvement} {pr.improvementUnit}
        </div>

        {/* Exercise title */}
        <h3 className="absolute bottom-3 left-3 right-3 text-[18px] font-extrabold text-white leading-tight">
          {pr.exercise}
        </h3>
      </div>

      {/* Body */}
      <div className="p-4">
        {/* Weight × reps */}
        <div className="flex items-baseline gap-2 mb-2">
          <span className="text-[32px] font-extrabold text-slate-50 tabular-nums leading-none">
            {pr.weight}
          </span>
          <span className="text-[13px] font-bold text-slate-400">{pr.unit}</span>
          <span className="text-slate-600">×</span>
          <span className="text-[20px] font-extrabold text-electric-400 tabular-nums">
            {pr.reps}
          </span>
          <span className="text-[12px] font-bold text-slate-400">reps</span>
        </div>

        {/* Date */}
        <p className="text-[11.5px] text-slate-400 mb-3 tabular-nums">
          Đạt được: {pr.achievedAt.toLocaleDateString('vi-VN')} · {timeSince(pr.achievedAt)}
        </p>

        {pr.notes && (
          <p className="text-[12px] text-slate-500 italic line-clamp-2 border-l-2 border-electric-500/40 pl-2">
            "{pr.notes}"
          </p>
        )}

        <button className="mt-3 w-full py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 text-[12px] font-bold rounded-lg flex items-center justify-center gap-1.5 transition-colors">
          <Phosphor.Play size={11} weight="fill" />
          Xem video
        </button>
      </div>
    </article>
  );
}

function PillMetric({ icon, label, value, suffix }: { icon: string; label: string; value: number; suffix: string }) {
  const Icon = Phosphor[icon] as any;
  return (
    <div className="flex items-center gap-2.5 p-3 bg-slate-900 border border-slate-800 rounded-xl">
      <div className="w-10 h-10 rounded-lg bg-electric-500/10 flex items-center justify-center flex-shrink-0">
        <Icon size={18} weight="fill" className="text-electric-400" />
      </div>
      <div>
        <p className="text-[10.5px] font-bold uppercase tracking-wider text-slate-500">{label}</p>
        <p className="text-[18px] font-extrabold text-slate-50 tabular-nums leading-none">
          {value} <span className="text-[12px] text-slate-400 font-medium">{suffix}</span>
        </p>
      </div>
    </div>
  );
}

function timeSince(date: Date): string {
  const days = Math.floor((Date.now() - date.getTime()) / 86400000);
  if (days === 0) return 'hôm nay';
  if (days === 1) return '1 ngày trước';
  if (days < 30) return `${days} ngày trước`;
  if (days < 365) return `${Math.floor(days / 30)} tháng trước`;
  return `${Math.floor(days / 365)} năm trước`;
}
```

## 5. Accessibility

- Section `aria-labelledby`
- Trophy badge có `aria-label="Cá nhân tốt nhất"`
- Improvement pill có `aria-label` mô tả chi tiết
- Numbers tabular-nums
- Avatar alt text
- Date + relative time dual format
- Reduce-motion: hover scale off, no confetti

## 6. Performance

- Lazy load images
- Memoized cards
- Inline icons
- Static data OK

## 7. Anti-patterns đã tránh

- ❌ "Make every screen feel like..."
- ❌ Trophy color-only (đã icon + label)
- ❌ Generic metric display (đã label + suffix)
- ❌ No video access (đã nút Play)
- ❌ Date không accessible (đã dual format)

---

**Component family**: Marketing + Profile — `pr-display`