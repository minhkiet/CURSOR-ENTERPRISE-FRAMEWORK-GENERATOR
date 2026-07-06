export interface PersonalRecord {
  id: string;
  exercise: string;
  weight: number;
  reps: number;
  unit: 'kg' | 'lb';
  posterUrl: string;
  achievedDaysAgo: number;
  improvement: number;
  improvementUnit: 'kg' | 'lb' | 'reps' | 'seconds';
  notes?: string;
}

export const SAMPLE_PRS: PersonalRecord[] = [
  {
    id: 'pr1',
    exercise: 'Bench Press',
    weight: 120,
    reps: 5,
    unit: 'kg',
    posterUrl: 'https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=600&q=80',
    achievedDaysAgo: 1,
    improvement: 10,
    improvementUnit: 'kg',
    notes: 'Cảm ơn Ironpath PR tracker. PR trước 110kg × 5.'
  },
  {
    id: 'pr2',
    exercise: 'Back Squat',
    weight: 160,
    reps: 3,
    unit: 'kg',
    posterUrl: 'https://images.unsplash.com/photo-1605296867304-46d5465a13f1?w=600&q=80',
    achievedDaysAgo: 30,
    improvement: 20,
    improvementUnit: 'kg'
  },
  {
    id: 'pr3',
    exercise: 'Deadlift',
    weight: 200,
    reps: 1,
    unit: 'kg',
    posterUrl: 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=600&q=80',
    achievedDaysAgo: 7,
    improvement: 15,
    improvementUnit: 'kg'
  },
  {
    id: 'pr4',
    exercise: 'Overhead Press',
    weight: 70,
    reps: 5,
    unit: 'kg',
    posterUrl: 'https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?w=600&q=80',
    achievedDaysAgo: 14,
    improvement: 5,
    improvementUnit: 'kg'
  }
];

export const VOLUME_DATA_30D = Array.from({ length: 30 }).map((_, i) => {
  const date = new Date(Date.now() - (29 - i) * 86400000);
  const base = i < 20 ? 800 + Math.random() * 1200 : 1200 + Math.random() * 800;
  return {
    label: date.toLocaleDateString('vi-VN', { weekday: 'short' }).slice(0, 2),
    volume: Math.floor(base),
    date,
    byMuscle: {
      chest: Math.floor(base * 0.25),
      back: Math.floor(base * 0.30),
      legs: Math.floor(base * 0.25),
      shoulders: Math.floor(base * 0.10),
      arms: Math.floor(base * 0.07),
      core: Math.floor(base * 0.03)
    }
  };
});