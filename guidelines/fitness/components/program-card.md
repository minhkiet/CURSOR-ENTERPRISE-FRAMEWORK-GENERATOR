# Program Card

> Workout program card cho marketing landing và in-app library. Cover image, difficulty, duration, equipment, weekly schedule, CTA.

## 1. Mục đích

User browse programs, cần filter nhanh theo difficulty, equipment, duration. Tap để xem chi tiết + start.

## 2. Layout

```
┌──────────────────────────────────┐
│ [Cover image 4:3]                │
│                                  │
│ BEGINNER  ★ 4.9 (1.247)         │
│                                  │
│ PPL — Push Pull Legs            │
│ 8 tuần · 6 buổi/tuần            │
│                                  │
│ Cơ vai, ngực, lưng, chân, tay    │
│                                  │
│ ┌─────┬─────┬─────┐             │
│ │ Bar │ Dumb│ Pull│ → 7 thiết bị │
│ └─────┴─────┴─────┘             │
│                                  │
│ ┌──────────────────────────┐   │
│ │ BẮT ĐẦU                │   │
│ └──────────────────────────┘   │
└──────────────────────────────────┘
```

## 3. Variants

| Variant | Use | Khác biệt |
|---|---|---|
| `default` | Marketing landing | Full info |
| `compact` | Sidebar widget | Truncated |
| `enrolled` | In-app "Chương trình của tôi" | Progress bar |
| `coach-pick` | Featured | Highlighted |

## 4. Code reference

```tsx
import * as Phosphor from '@phosphor-icons/react';

export interface Program {
  id: string;
  name: string;
  slug: string;
  description: string;
  coverUrl: string;
  weeks: number;
  daysPerWeek: number;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  equipment: string[];
  muscles: string[];
  rating: number;
  enrolled: number;
  enrolledByUser?: boolean;
  progressPercent?: number;
  coachName?: string;
}

const SAMPLE_PROGRAMS: Program[] = [
  {
    id: 'p1',
    name: 'PPL — Push Pull Legs',
    slug: 'ppl-push-pull-legs',
    description: 'Chương trình 6 buổi/tuần cho hypertrophy cổ điển. Volume cao, recovery đầy đủ.',
    coverUrl: 'https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?w=800&q=80',
    weeks: 8,
    daysPerWeek: 6,
    difficulty: 'intermediate',
    equipment: ['barbell', 'dumbbell', 'pull-up bar', 'cable machine', 'bench', 'squat rack', 'leg press'],
    muscles: ['Ngực', 'Lưng', 'Vai', 'Chân', 'Tay'],
    rating: 4.9,
    enrolled: 1247
  },
  {
    id: 'p2',
    name: 'StrongLifts 5×5',
    slug: 'stronglifts-5x5',
    description: 'Classic 5×5 cho người mới. 3 buổi/tuần, 5 reps, tăng tạ mỗi buổi.',
    coverUrl: 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=800&q=80',
    weeks: 12,
    daysPerWeek: 3,
    difficulty: 'beginner',
    equipment: ['barbell', 'squat rack', 'bench'],
    muscles: ['Toàn thân'],
    rating: 4.8,
    enrolled: 3421
  },
  {
    id: 'p3',
    name: 'Powerbuilding 4-day',
    slug: 'powerbuilding-4-day',
    description: 'Hybrid strength + hypertrophy. Bench, Squat, Deadlift + accessory work.',
    coverUrl: 'https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?w=800&q=80',
    weeks: 10,
    daysPerWeek: 4,
    difficulty: 'advanced',
    equipment: ['barbell', 'dumbbell', 'cable machine', 'squat rack'],
    muscles: ['Toàn thân'],
    rating: 4.7,
    enrolled: 856,
    enrolledByUser: true,
    progressPercent: 45
  },
  {
    id: 'p4',
    name: 'Calisthenics Beginner',
    slug: 'calisthenics-beginner',
    description: 'Bodyweight progression. Push-up, pull-up, dip, squat pistol — không cần tạ.',
    coverUrl: 'https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=800&q=80',
    weeks: 6,
    daysPerWeek: 4,
    difficulty: 'beginner',
    equipment: ['pull-up bar', 'parallettes'],
    muscles: ['Toàn thân'],
    rating: 4.6,
    enrolled: 1893
  }
];

const DIFFICULTY_MAP = {
  beginner: { label: 'Mới bắt đầu', color: 'bg-emerald-500/20 text-emerald-400', icon: 'Seedling' },
  intermediate: { label: 'Trung cấp', color: 'bg-amber-500/20 text-amber-400', icon: 'Barbell' },
  advanced: { label: 'Nâng cao', color: 'bg-rose-500/20 text-rose-400', icon: 'Flame' }
} as const;

const EQUIPMENT_LABEL: Record<string, string> = {
  barbell: 'Bar',
  dumbbell: 'Tạ đôi',
  'pull-up bar': 'Xà đơn',
  cable: 'Cáp',
  bodyweight: 'BW',
  bench: 'Ghế',
  'squat rack': 'Squat rack'
};

export function ProgramLibrary() {
  return (
    <section className="bg-slate-50 py-16 lg:py-24" aria-labelledby="programs-heading">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="flex items-end justify-between mb-10 flex-wrap gap-4">
          <div>
            <span className="text-[11px] font-bold uppercase tracking-[0.18em] text-electric-600 mb-2 block">
              Thư viện chương trình
            </span>
            <h2 id="programs-heading" className="text-3xl lg:text-5xl font-extrabold text-slate-900 tracking-tight">
              Chọn chương trình phù hợp với bạn
            </h2>
            <p className="mt-2 text-slate-600 text-[15px] max-w-2xl">
              47 chương trình từ PPL hypertrophy tới Calisthenics. Tất cả có video hướng dẫn + progress tracker.
            </p>
          </div>
          <a href="#" className="inline-flex items-center gap-1.5 px-5 py-3 bg-slate-900 hover:bg-slate-800 text-white text-[13px] font-bold rounded-lg">
            Xem tất cả 47 chương trình
            <Phosphor.ArrowRight size={14} weight="bold" />
          </a>
        </div>

        {/* Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-5">
          {SAMPLE_PROGRAMS.map(p => <ProgramCard key={p.id} program={p} />)}
        </div>
      </div>
    </section>
  );
}

function ProgramCard({ program }: { program: Program }) {
  const diff = DIFFICULTY_MAP[program.difficulty];
  const DiffIcon = Phosphor[diff.icon] as any;

  return (
    <article className="group bg-white rounded-2xl border border-slate-200 overflow-hidden hover:shadow-card-lift hover:-translate-y-0.5 transition-all flex flex-col">
      {/* Cover */}
      <div className="relative aspect-[4/3] overflow-hidden bg-slate-100">
        <img
          src={program.coverUrl}
          alt={program.name}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          loading="lazy"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-transparent" />

        {/* Difficulty badge */}
        <span className={`absolute top-3 left-3 inline-flex items-center gap-1 px-2 py-1 text-[10px] font-bold uppercase tracking-wider rounded-full backdrop-blur ${diff.color}`} aria-label={`Độ khó: ${diff.label}`}>
          <DiffIcon size={10} weight="bold" />
          {diff.label}
        </span>

        {/* Rating */}
        <span className="absolute top-3 right-3 inline-flex items-center gap-1 px-2 py-1 bg-black/60 backdrop-blur text-white text-[10px] font-bold rounded-full tabular-nums">
          <Phosphor.Star size={10} weight="fill" className="text-amber-400" />
          {program.rating}
        </span>

        {/* Enrolled by user badge */}
        {program.enrolledByUser && (
          <div className="absolute bottom-3 left-3 right-3 bg-electric-500/95 text-slate-950 px-3 py-2 rounded-lg backdrop-blur shadow-lg">
            <p className="text-[10.5px] font-bold uppercase tracking-wider leading-none">Đang tập</p>
            {program.progressPercent !== undefined && (
              <>
                <div className="mt-1.5 h-1.5 bg-slate-950/30 rounded-full overflow-hidden" role="progressbar" aria-valuenow={program.progressPercent} aria-valuemin={0} aria-valuemax={100}>
                  <div className="h-full bg-slate-950 rounded-full" style={{ width: `${program.progressPercent}%` }} />
                </div>
                <p className="mt-1 text-[10px] font-bold tabular-nums">{program.progressPercent}% hoàn thành</p>
              </>
            )}
          </div>
        )}
      </div>

      {/* Body */}
      <div className="p-4 flex-1 flex flex-col">
        {/* Meta */}
        <div className="flex items-center gap-2 text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-2 tabular-nums">
          <span>{program.weeks} tuần</span>
          <span className="text-slate-300">·</span>
          <span>{program.daysPerWeek} buổi/tuần</span>
        </div>

        {/* Title */}
        <h3 className="text-[16px] font-extrabold text-slate-900 leading-tight line-clamp-2">
          {program.name}
        </h3>
        <p className="mt-1.5 text-[12.5px] text-slate-600 leading-relaxed line-clamp-2">
          {program.description}
        </p>

        {/* Equipment */}
        <div className="mt-3 flex items-center gap-1.5 flex-wrap">
          {program.equipment.slice(0, 3).map(eq => {
            const slug = eq.toLowerCase().replace(/\s+/g, '-');
            return (
              <span key={eq} className="inline-flex items-center gap-1 px-1.5 py-0.5 bg-slate-100 text-slate-700 text-[10px] font-bold rounded" title={eq}>
                <img src={`https://cdn.simpleicons.org/${slug}/64748b`} alt="" className="w-2.5 h-2.5" loading="lazy" />
                {EQUIPMENT_LABEL[eq] || eq}
              </span>
            );
          })}
          {program.equipment.length > 3 && (
            <span className="text-[10.5px] font-bold text-slate-500">+{program.equipment.length - 3}</span>
          )}
        </div>

        {/* Enrolled */}
        <p className="mt-3 text-[10.5px] text-slate-500 tabular-nums">
          <strong className="font-bold text-slate-700">{program.enrolled.toLocaleString('vi-VN')}</strong> người đang tập chương trình này
        </p>

        {/* Spacer */}
        <div className="flex-1" />

        {/* CTA */}
        <button
          aria-label={`${program.enrolledByUser ? 'Tiếp tục' : 'Bắt đầu'} chương trình ${program.name}`}
          className={`mt-4 w-full py-2.5 text-[12.5px] font-bold rounded-lg flex items-center justify-center gap-1.5 transition-colors ${
            program.enrolledByUser
              ? 'bg-electric-500 hover:bg-electric-400 text-slate-950'
              : 'bg-slate-900 hover:bg-slate-800 text-white'
          }`}
        >
          {program.enrolledByUser ? (
            <>
              <Phosphor.Play size={12} weight="fill" />
              TIẾP TỤC TẬP
            </>
          ) : (
            <>
              BẮT ĐẦU
              <Phosphor.ArrowRight size={12} weight="bold" />
            </>
          )}
        </button>
      </div>
    </article>
  );
}
```

## 5. Accessibility

- Section `aria-labelledby`
- Mỗi card là `<article>`
- Difficulty badge có `aria-label` đầy đủ
- Progress bar `role="progressbar"` + `aria-valuenow`
- CTA buttons có `aria-label` riêng cho mỗi program
- Equipment có `title` + text visible
- Rating có icon + value
- Numbers tabular-nums
- Reduce-motion: hover scale off

## 6. Performance

- Lazy load images
- Memoized cards
- Static data
- Inline icons

## 7. Anti-patterns đã tránh

- ❌ "Make every screen feel like..."
- ❌ Color-only difficulty (đã icon + label)
- ❌ Generic equipment list (đã icon + label)
- ❌ No progress bar cho enrolled (đã có)
- ❌ No aria-label cho CTA

---

**Component family**: Marketing + In-app — `program-card`