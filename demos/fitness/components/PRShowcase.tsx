import { Trophy, TrendingUp, CalendarCheck, Flame, ArrowUp, Play } from 'lucide-react';
import { SAMPLE_PRS } from '@/data/pr';

export function PRShowcase() {
  return (
    <section id="stats" className="bg-ink-950 py-16 lg:py-24 text-ink-50" aria-labelledby="pr-heading">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-end justify-between mb-10 flex-wrap gap-3">
          <div>
            <span className="inline-flex items-center gap-1.5 text-[11px] font-bold uppercase tracking-[0.18em] text-electric-400 mb-2">
              <Trophy size={12} strokeWidth={2.5} fill="currentColor" />
              Personal records
            </span>
            <h2 id="pr-heading" className="text-3xl lg:text-5xl font-display tracking-tight">
              892K PRs đã smash.<br />
              <span className="text-electric-400">Bạn tiếp theo?</span>
            </h2>
          </div>
          <a href="#" className="inline-flex items-center gap-1.5 px-4 py-2 border border-ink-700 hover:border-electric-500 text-slate-300 hover:text-electric-400 text-[13px] font-bold rounded-lg transition-colors">
            Xem tất cả 247 PRs
            <ArrowRightInline />
          </a>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-5">
          {SAMPLE_PRS.map(pr => <PRCard key={pr.id} pr={pr} />)}
        </div>

        <div className="mt-10 grid grid-cols-2 lg:grid-cols-4 gap-3 lg:gap-5">
          <PillMetric icon="trophy" label="PRs 2026" value="247" suffix="records" />
          <PillMetric icon="trend" label="Tổng cải thiện" value="50" suffix="kg" />
          <PillMetric icon="calendar" label="Tuần luyện" value="28" suffix="tuần" />
          <PillMetric icon="flame" label="Streak" value="47" suffix="ngày liên tiếp" />
        </div>
      </div>
    </section>
  );
}

function ArrowRightInline() {
  return (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M5 12h14M12 5l7 7-7 7" />
    </svg>
  );
}

function PRCard({ pr }: { pr: typeof SAMPLE_PRS[number] }) {
  return (
    <article className="group bg-ink-900 border border-ink-800 rounded-2xl overflow-hidden hover:border-electric-500/50 transition-colors">
      <div className="relative aspect-[4/3] bg-ink-950 overflow-hidden">
        <img src={pr.posterUrl} alt={pr.exercise} className="w-full h-full object-cover opacity-90 group-hover:opacity-100 group-hover:scale-105 transition-all duration-300" loading="lazy" />
        <div className="absolute inset-0 bg-gradient-to-t from-ink-950 via-ink-950/40 to-transparent" />

        <div className="absolute top-3 left-3 inline-flex items-center gap-1 px-2 py-1 bg-electric-500 text-ink-950 text-[10px] font-extrabold uppercase tracking-wider rounded-full shadow-lg shadow-electric-500/40" aria-label="Cá nhân tốt nhất">
          <Trophy size={10} strokeWidth={2.5} fill="currentColor" />
          PR
        </div>

        <div className="absolute top-3 right-3 inline-flex items-center gap-1 px-2 py-1 bg-emerald-500/90 text-white text-[10px] font-extrabold rounded-full" aria-label={`Cải thiện ${pr.improvement} ${pr.improvementUnit} so với PR trước`}>
          <ArrowUp size={10} strokeWidth={3} />
          {pr.improvement} {pr.improvementUnit}
        </div>

        <h3 className="absolute bottom-3 left-3 right-3 text-[18px] font-display text-ink-50 leading-tight">
          {pr.exercise}
        </h3>
      </div>

      <div className="p-4">
        <div className="flex items-baseline gap-2 mb-2">
          <span className="text-[32px] font-display text-ink-50 tabular-nums leading-none">{pr.weight}</span>
          <span className="text-[13px] font-bold text-slate-400">{pr.unit}</span>
          <span className="text-slate-600">×</span>
          <span className="text-[20px] font-display text-electric-400 tabular-nums">{pr.reps}</span>
          <span className="text-[12px] font-bold text-slate-400">reps</span>
        </div>

        <p className="text-[11.5px] text-slate-400 mb-3 tabular-nums">
          {pr.achievedDaysAgo === 0 ? 'Hôm nay' : pr.achievedDaysAgo === 1 ? '1 ngày trước' : `${pr.achievedDaysAgo} ngày trước`}
        </p>

        {pr.notes && (
          <p className="text-[12px] text-slate-500 italic line-clamp-2 border-l-2 border-electric-500/40 pl-2">
            "{pr.notes}"
          </p>
        )}

        <button className="mt-3 w-full py-2 bg-ink-800 hover:bg-ink-700 text-slate-300 text-[12px] font-bold rounded-lg flex items-center justify-center gap-1.5 transition-colors">
          <Play size={11} strokeWidth={2.5} fill="currentColor" />
          Xem video
        </button>
      </div>
    </article>
  );
}

const ICON_MAP: Record<string, any> = {
  trophy: Trophy,
  trend: TrendingUp,
  calendar: CalendarCheck,
  flame: Flame
};

function PillMetric({ icon, label, value, suffix }: { icon: string; label: string; value: string; suffix: string }) {
  const Icon = ICON_MAP[icon] ?? Trophy;
  return (
    <div className="flex items-center gap-2.5 p-3.5 bg-ink-900 border border-ink-800 rounded-xl">
      <div className="w-10 h-10 rounded-lg bg-electric-500/10 flex items-center justify-center flex-shrink-0">
        <Icon size={18} strokeWidth={2.5} fill="currentColor" className="text-electric-400" />
      </div>
      <div>
        <p className="text-[10px] font-bold uppercase tracking-wider text-slate-500">{label}</p>
        <p className="text-[18px] font-display text-ink-50 tabular-nums leading-none">
          {value} <span className="text-[11px] text-slate-400 font-bold">{suffix}</span>
        </p>
      </div>
    </div>
  );
}