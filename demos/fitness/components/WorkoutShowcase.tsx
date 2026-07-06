'use client';
import { useState } from 'react';
import { Heart, CheckCircle2, Circle, PlayCircle, Trophy, SkipForward, Volume2 } from 'lucide-react';
import { SAMPLE_SETS, EXERCISE_INFO } from '@/data/workout';

export function WorkoutShowcase() {
  const [sets] = useState(SAMPLE_SETS);
  const [isResting] = useState(true);
  const [restRemaining] = useState(87);
  const activeIdx = 2;

  const totalVolume = sets.filter(s => s.completed).reduce((sum, s) => sum + s.weight * s.reps, 0);

  return (
    <section id="workout" className="bg-ink-900 py-16 lg:py-24 text-ink-50 border-y border-ink-800" aria-labelledby="workout-heading">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-end justify-between mb-10 flex-wrap gap-3">
          <div>
            <span className="text-[11px] font-bold uppercase tracking-[0.18em] text-electric-400 mb-2 block">
              In-app workout tracker
            </span>
            <h2 id="workout-heading" className="text-3xl lg:text-5xl font-display tracking-tight leading-[1.05]">
              Mid-set 1-tap.<br />
              <span className="text-electric-400">Không cần 2 tay.</span>
            </h2>
            <p className="mt-3 text-slate-400 text-[15px] max-w-2xl">
              Touch targets 56px+ cho găng tay. Rest timer auto. Auto PR detect. Space shortcut complete set.
            </p>
          </div>
          <div className="text-right">
            <p className="text-[10.5px] font-bold uppercase tracking-wider text-slate-400">Workout volume</p>
            <p className="text-[32px] font-display text-electric-400 tabular-nums">{totalVolume.toLocaleString('vi-VN')}<span className="text-[16px] text-slate-400 ml-1">kg</span></p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 lg:gap-6">
          {/* Video + cues */}
          <div className="lg:col-span-7 space-y-3">
            <div className="relative aspect-video bg-black rounded-2xl overflow-hidden border border-ink-800">
              <img
                src="https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=1200&q=80"
                alt={`${EXERCISE_INFO.name} demo`}
                className="w-full h-full object-cover opacity-80"
                loading="lazy"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-ink-950 via-ink-950/40 to-transparent" />

              <div className="absolute top-3 left-3 inline-flex items-center gap-1.5 px-2.5 py-1 bg-rose-500/90 backdrop-blur rounded-full text-[10.5px] font-bold text-white">
                <div className="w-2 h-2 rounded-full bg-white animate-pulse" />
                REC
              </div>

              <div className="absolute bottom-3 right-3 inline-flex items-center gap-1.5 px-2.5 py-1 bg-black/70 backdrop-blur rounded-full text-[11px] font-bold text-ink-50">
                <Heart size={11} strokeWidth={2.5} fill="currentColor" className="text-rose-500" />
                <span className="tabular-nums">142</span> BPM
              </div>

              <div className="absolute bottom-3 left-3 right-20">
                <p className="text-[11px] font-bold uppercase tracking-wider text-electric-400 mb-1">Bài {activeIdx + 1} / 8</p>
                <h3 className="text-[20px] font-display text-ink-50">{EXERCISE_INFO.name}</h3>
              </div>
            </div>

            <ul className="grid grid-cols-1 md:grid-cols-2 gap-2" aria-label="Form cues">
              {EXERCISE_INFO.cues.map((cue, i) => (
                <li key={i} className="flex items-start gap-2 p-3 bg-ink-800/50 border border-ink-800 rounded-lg text-[12.5px] text-slate-300">
                  <CheckCircle2 size={14} strokeWidth={2.5} className="text-electric-400 flex-shrink-0 mt-0.5" />
                  <span>{cue}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Right: Rest timer + Set list */}
          <div className="lg:col-span-5 space-y-4">
            {isResting && <RestTimerDisplay remaining={restRemaining} total={90} />}

            <section aria-labelledby="sets-heading" className="bg-ink-950 border border-ink-800 rounded-2xl overflow-hidden">
              <header className="flex items-center justify-between p-4 border-b border-ink-800">
                <h3 id="sets-heading" className="text-[11px] font-bold uppercase tracking-wider text-slate-400">
                  Danh sách hiệp
                </h3>
                <span className="text-[11px] font-bold text-electric-400 tabular-nums">
                  {sets.filter(s => s.completed).length}/{sets.length} done
                </span>
              </header>
              <ol className="divide-y divide-ink-800">
                {sets.map((s, i) => {
                  const isActive = i === activeIdx && !s.completed;
                  let StatusIcon: any = Circle;
                  let statusColor = 'text-slate-600';
                  if (s.completed) {
                    StatusIcon = CheckCircle2;
                    statusColor = 'text-electric-400';
                  } else if (isActive) {
                    StatusIcon = PlayCircle;
                    statusColor = 'text-electric-400';
                  }

                  return (
                    <li
                      key={s.index}
                      className={`flex items-center gap-3 px-4 py-3 ${
                        isActive ? 'bg-electric-500/10 border-l-4 border-electric-500' : ''
                      }`}
                      aria-current={isActive ? 'true' : undefined}
                    >
                      <StatusIcon size={20} className={statusColor} />
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-1.5">
                          <span className="text-[13px] font-extrabold text-ink-50 tabular-nums">Hiệp {s.index}</span>
                          {s.isPR && (
                            <span className="inline-flex items-center gap-0.5 px-1.5 py-0.5 bg-amber-500/20 text-amber-400 text-[9.5px] font-bold uppercase tracking-wider rounded">
                              <Trophy size={9} strokeWidth={2.5} fill="currentColor" />
                              PR
                            </span>
                          )}
                          {isActive && (
                            <span className="inline-flex items-center gap-1 px-1.5 py-0.5 bg-electric-500 text-ink-950 text-[9.5px] font-bold uppercase tracking-wider rounded">
                              ĐANG TẬP
                            </span>
                          )}
                        </div>
                        <p className="text-[11.5px] text-slate-400 tabular-nums mt-0.5">
                          <strong className="font-bold text-slate-300">{s.weight}kg</strong> × <strong className="font-bold text-slate-300">{s.reps}</strong> reps · RIR {s.rir}
                        </p>
                      </div>
                    </li>
                  );
                })}
              </ol>
            </section>
          </div>
        </div>
      </div>
    </section>
  );
}

function RestTimerDisplay({ remaining, total }: { remaining: number; total: number }) {
  const ratio = remaining / total;
  const colorClass = ratio > 0.33 ? 'text-electric-400' : ratio > 0.11 ? 'text-amber-400' : 'text-rose-400';
  const pulseClass = remaining <= 10 && remaining > 0 ? 'animate-pulse' : '';
  const borderClass = ratio > 0.33 ? 'border-electric-500' : ratio > 0.11 ? 'border-amber-500' : 'border-rose-500';

  return (
    <section
      role="timer"
      aria-label={`Nghỉ ${Math.floor(total / 60)} phút ${total % 60} giây, còn lại ${remaining} giây`}
      aria-live="polite"
      aria-atomic="true"
      className={`bg-gradient-to-br from-ink-900 to-ink-950 border-2 rounded-2xl p-6 lg:p-8 shadow-2xl ${borderClass}`}
    >
      <p className="text-[10.5px] font-bold uppercase tracking-[0.18em] text-slate-400 mb-2 text-center">
        Nghỉ
      </p>

      <div className="text-center">
        <div className={`text-[96px] lg:text-[120px] font-display tabular-nums leading-none tracking-tighter ${colorClass} ${pulseClass}`}>
          {Math.floor(remaining / 60)}:{(remaining % 60).toString().padStart(2, '0')}
        </div>
        <p className="text-[11px] text-slate-500 mt-2 tabular-nums">
          / 1:30 (tổng)
        </p>
      </div>

      <div className="mt-6 grid grid-cols-3 gap-2">
        <button className="h-14 bg-ink-800 hover:bg-ink-700 text-slate-300 text-[13px] font-extrabold rounded-xl">
          −15s
        </button>
        <button className="h-14 bg-rose-500 hover:bg-rose-400 text-white text-[13px] font-extrabold rounded-xl flex items-center justify-center gap-1.5">
          <SkipForward size={13} strokeWidth={2.5} />
          BỎ QUA
        </button>
        <button className="h-14 bg-ink-800 hover:bg-ink-700 text-slate-300 text-[13px] font-extrabold rounded-xl">
          +30s
        </button>
      </div>

      <p className="mt-3 text-center text-[10.5px] text-slate-500 inline-flex items-center gap-1 justify-center w-full">
        <Volume2 size={11} strokeWidth={2.5} />
        Audio cue khi còn 3 giây
      </p>
    </section>
  );
}