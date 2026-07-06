export interface TrackerSet {
  index: number;
  weight: number;
  reps: number;
  rir: number;
  completed: boolean;
  completedAt: Date | null;
  isPR?: boolean;
}

export const SAMPLE_SETS: TrackerSet[] = [
  { index: 1, weight: 60, reps: 10, rir: 3, completed: true, completedAt: new Date(Date.now() - 360000) },
  { index: 2, weight: 80, reps: 8, rir: 2, completed: true, completedAt: new Date(Date.now() - 180000) },
  { index: 3, weight: 100, reps: 6, rir: 2, completed: false, completedAt: null, isPR: true },
  { index: 4, weight: 100, reps: 6, rir: 1, completed: false, completedAt: null }
];

export const EXERCISE_INFO = {
  name: 'Bench Press',
  cues: [
    'Giữ lưng thẳng trên ghế',
    'Thở vào khi hạ xuống ngực',
    'Thở ra khi đẩy lên',
    'Không bật tay khỏi xà khi ở dưới'
  ]
};