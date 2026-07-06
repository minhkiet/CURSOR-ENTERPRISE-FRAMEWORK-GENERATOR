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
}

export const SAMPLE_PROGRAMS: Program[] = [
  {
    id: 'p1',
    name: 'PPL — Push Pull Legs',
    slug: 'ppl-push-pull-legs',
    description: 'Chương trình 6 buổi/tuần cho hypertrophy cổ điển. Volume cao, recovery đầy đủ.',
    coverUrl: 'https://images.unsplash.com/photo-1581009146145-b7e9c0a3b8c5?w=800&q=80',
    weeks: 8,
    daysPerWeek: 6,
    difficulty: 'intermediate',
    equipment: ['barbell', 'dumbbell', 'pull-up bar', 'cable', 'bench', 'squat-rack'],
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
    equipment: ['barbell', 'squat-rack', 'bench'],
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
    equipment: ['barbell', 'dumbbell', 'cable', 'squat-rack'],
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
    coverUrl: 'https://images.unsplash.com/photo-1598971639058-fab3c3109a00?w=800&q=80',
    weeks: 6,
    daysPerWeek: 4,
    difficulty: 'beginner',
    equipment: ['pull-up bar', 'parallettes'],
    muscles: ['Toàn thân'],
    rating: 4.6,
    enrolled: 1893
  }
];

export const TESTIMONIALS = [
  {
    id: 't1',
    name: 'Minh Trần',
    title: 'VP, FPT · Powerlifter',
    avatarId: '1507003211169-0a1dd7228f2d',
    quote: 'Squat từ 100 lên 160kg trong 8 tháng nhờ log volume chính xác + RIR tracking. Ironpath là 1 app duy nhất tôi mở trong gym.',
    metrics: [
      { label: 'Squat 1RM', value: '+60kg', icon: 'TrendUp' },
      { label: 'Total volume', value: '12,5 tấn/tháng', icon: 'ChartBar' }
    ]
  },
  {
    id: 't2',
    name: 'Lan Lê',
    title: 'Founder, BeautyBox · Bodybuilder',
    avatarId: '1494790108377-be9c29b29330',
    quote: 'Apple Watch sync ngon. Tôi log set ngay cổ tay giữa hiệp, không cần lấy iPhone. Trainer của tôi follow progress realtime.',
    metrics: [
      { label: 'Workouts', value: '247/yr', icon: 'Barbell' },
      { label: 'PRs', value: '34', icon: 'Trophy' }
    ]
  },
  {
    id: 't3',
    name: 'Quân Nguyễn',
    title: 'Coach cá nhân · Crossfit',
    avatarId: '1472099645785-5658abf4ff4e',
    quote: '12 clients của tôi đều dùng Ironpath. Tôi assign program từ xa và xem progress chart. Setup cho client mới chỉ 5 phút.',
    metrics: [
      { label: 'Clients', value: '12', icon: 'UsersThree' },
      { label: 'Programs', value: '47', icon: 'Books' }
    ]
  }
];