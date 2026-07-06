export interface Feature {
  id: string;
  icon: string;
  title: string;
  description: string;
  metric: string;
  variant: 'large' | 'small';
}

export const FEATURES: Feature[] = [
  {
    id: 'tracker',
    icon: 'Barbell',
    title: 'Workout tracker 1-tap',
    description: 'Log weight × reps × RIR bằng 1 ngón cái ngay giữa set. Rest timer tự động. Touch targets 56px cho tay đeo găng và ướt mồ hôi.',
    metric: '30s per set',
    variant: 'large'
  },
  {
    id: 'pr',
    icon: 'Trophy',
    title: 'Auto-detect PRs',
    description: 'Tự động phát hiện 1RM mới. Confetti + share Strava 1-tap.',
    metric: '892K PRs',
    variant: 'small'
  },
  {
    id: 'rest',
    icon: 'Timer',
    title: 'Rest timer giant',
    description: 'Countdown 96-140px. Audio cue ở 3 giây cuối. Haptic trên Apple Watch.',
    metric: '94% start next set on time',
    variant: 'small'
  },
  {
    id: 'volume',
    icon: 'ChartBar',
    title: 'Volume analytics',
    description: 'Volume 7d/30d/90d/1y. Breakdown theo 6 muscle groups. Sparkline trend.',
    metric: '+24% volume YoY',
    variant: 'small'
  },
  {
    id: 'watch',
    icon: 'AppleLogo',
    title: 'Apple Watch native',
    description: 'Không cần iPhone. Start workout từ cổ tay. Heart rate live + haptic cues.',
    metric: '47ms latency',
    variant: 'small'
  },
  {
    id: 'strava',
    icon: 'StravaLogo',
    title: 'Strava + Garmin sync',
    description: 'Sync activities 2 chiều. Tự động import cardio runs + rides. Strava club Ironpath.',
    metric: '12+ integrations',
    variant: 'small'
  }
];