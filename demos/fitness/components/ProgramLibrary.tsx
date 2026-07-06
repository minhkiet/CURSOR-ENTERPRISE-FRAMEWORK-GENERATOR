import * as Phosphor from '@phosphor-icons/react';
import { SAMPLE_PROGRAMS, TESTIMONIALS } from '@/data/programs';

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
  'squat-rack': 'Squat rack',
  parallettes: 'Parallettes'
};

export function ProgramLibrary() {
  return (
    <section id="programs" className="bg-ink-950 py-16 lg:py-24 text-ink-50" aria-labelledby="programs-heading">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="flex items-end justify-between mb-10 flex-wrap gap-4">
          <div>
            <span className="text-[11px] font-bold uppercase tracking-[0.18em] text-electric-400 mb-2 block">
              Thư viện chương trình
            </span>
            <h2 id="programs-heading" className="text-3xl lg:text-5xl font-display tracking-tight">
              47 chương trình tập.<br />
              <span className="text-electric-400">1 người dùng tập.</span>
            </h2>
            <p className="mt-3 text-slate-400 text-[15px]">
              Từ PPL hypertrophy tới Calisthenics. Tất cả có video form guide + progress tracker.
            </p>
          </div>
          <a href="#" className="inline-flex items-center gap-1.5 px-5 py-3 bg-ink-800 hover:bg-ink-700 text-ink-50 text-[13px] font-extrabold rounded-lg transition-colors">
            Xem 47 chương trình
            <Phosphor.ArrowRight size={14} weight="bold" />
          </a>
        </div>

        {/* Programs grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-5 mb-16">
          {SAMPLE_PROGRAMS.map(p => <ProgramCard key={p.id} program={p} />)}
        </div>

        {/* Testimonials */}
        <div className="border-t border-ink-800 pt-12">
          <h3 className="text-2xl lg:text-3xl font-display text-ink-50 mb-8">
            Gymer Việt nói gì?
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
            {TESTIMONIALS.map(t => <TestimonialCard key={t.id} t={t} />)}
          </div>
        </div>
      </div>
    </section>
  );
}

function ProgramCard({ program }: { program: typeof SAMPLE_PROGRAMS[number] }) {
  const diff = DIFFICULTY_MAP[program.difficulty];
  const DiffIcon = Phosphor[diff.icon] as any;

  return (
    <article className="group bg-ink-900 border border-ink-800 rounded-2xl overflow-hidden hover:border-electric-500/50 transition-colors flex flex-col">
      <div className="relative aspect-[4/3] overflow-hidden bg-ink-950">
        <img
          src={program.coverUrl}
          alt={program.name}
          className="w-full h-full object-cover opacity-90 group-hover:opacity-100 group-hover:scale-105 transition-transform duration-300"
          loading="lazy"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-ink-950 via-ink-950/30 to-transparent" />

        <span className={`absolute top-3 left-3 inline-flex items-center gap-1 px-2 py-1 text-[10px] font-bold uppercase tracking-wider rounded-full backdrop-blur ${diff.color}`} aria-label={`Độ khó: ${diff.label}`}>
          <DiffIcon size={10} weight="bold" />
          {diff.label}
        </span>

        <span className="absolute top-3 right-3 inline-flex items-center gap-1 px-2 py-1 bg-black/60 backdrop-blur text-ink-50 text-[10px] font-bold rounded-full tabular-nums">
          <Phosphor.Star size={10} weight="fill" className="text-amber-400" />
          {program.rating}
        </span>

        {program.enrolledByUser && (
          <div className="absolute bottom-3 left-3 right-3 bg-electric-500/95 text-ink-950 px-3 py-2 rounded-lg backdrop-blur shadow-lg">
            <p className="text-[10.5px] font-extrabold uppercase tracking-wider leading-none">Đang tập</p>
            {program.progressPercent !== undefined && (
              <>
                <div className="mt-1.5 h-1.5 bg-ink-950/30 rounded-full overflow-hidden" role="progressbar" aria-valuenow={program.progressPercent} aria-valuemin={0} aria-valuemax={100}>
                  <div className="h-full bg-ink-950 rounded-full" style={{ width: `${program.progressPercent}%` }} />
                </div>
                <p className="mt-1 text-[10px] font-bold tabular-nums">{program.progressPercent}% hoàn thành</p>
              </>
            )}
          </div>
        )}
      </div>

      <div className="p-4 flex-1 flex flex-col">
        <div className="flex items-center gap-2 text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-2 tabular-nums">
          <span>{program.weeks} tuần</span>
          <span className="text-ink-800">·</span>
          <span>{program.daysPerWeek} buổi/tuần</span>
        </div>

        <h3 className="text-[16px] font-display text-ink-50 leading-tight line-clamp-2">
          {program.name}
        </h3>
        <p className="mt-1.5 text-[12.5px] text-slate-400 leading-relaxed line-clamp-2">
          {program.description}
        </p>

        <div className="mt-3 flex items-center gap-1.5 flex-wrap flex-1">
          {program.equipment.slice(0, 3).map(eq => (
            <span key={eq} className="inline-flex items-center gap-1 px-1.5 py-0.5 bg-ink-800 text-slate-300 text-[10px] font-bold rounded">
              {EQUIPMENT_LABEL[eq] || eq}
            </span>
          ))}
          {program.equipment.length > 3 && (
            <span className="text-[10px] font-bold text-slate-500">+{program.equipment.length - 3}</span>
          )}
        </div>

        <p className="mt-3 text-[10.5px] text-slate-500 tabular-nums">
          <strong className="font-extrabold text-slate-300">{program.enrolled.toLocaleString('vi-VN')}</strong> người đang tập
        </p>

        <button
          className={`mt-4 w-full py-2.5 text-[12.5px] font-extrabold rounded-lg flex items-center justify-center gap-1.5 transition-colors ${
            program.enrolledByUser
              ? 'bg-electric-500 hover:bg-electric-400 text-ink-950'
              : 'bg-ink-800 hover:bg-ink-700 text-ink-50'
          }`}
        >
          {program.enrolledByUser ? (
            <><Phosphor.Play size={12} weight="fill" /> TIẾP TỤC</>
          ) : (
            <>BẮT ĐẦU <Phosphor.ArrowRight size={12} weight="bold" /></>
          )}
        </button>
      </div>
    </article>
  );
}

function TestimonialCard({ t }: { t: typeof TESTIMONIALS[number] }) {
  return (
    <article className="bg-ink-900 border border-ink-800 rounded-2xl p-5">
      <p className="text-[13.5px] text-slate-300 leading-relaxed italic">
        "{t.quote}"
      </p>

      <div className="mt-4 grid grid-cols-2 gap-2">
        {t.metrics.map((m, i) => {
          const Icon = Phosphor[m.icon] as any;
          return (
            <div key={i} className="bg-ink-950 rounded-lg p-2.5">
              <div className="flex items-center gap-1 text-[10px] text-slate-500 uppercase tracking-wider font-bold">
                <Icon size={10} weight="bold" className="text-electric-400" />
                {m.label}
              </div>
              <p className="text-[16px] font-display text-ink-50 tabular-nums">{m.value}</p>
            </div>
          );
        })}
      </div>

      <div className="mt-4 flex items-center gap-2.5 pt-3 border-t border-ink-800">
        <img
          src={`https://images.unsplash.com/photo-${t.avatarId}?w=80&h=80&fit=crop&q=80`}
          alt={t.name}
          className="w-10 h-10 rounded-full object-cover ring-2 ring-ink-800"
          loading="lazy"
        />
        <div>
          <p className="text-[13px] font-extrabold text-ink-50">{t.name}</p>
          <p className="text-[11px] text-slate-500">{t.title}</p>
        </div>
      </div>
    </article>
  );
}