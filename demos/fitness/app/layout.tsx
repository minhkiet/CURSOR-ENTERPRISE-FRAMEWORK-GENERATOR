import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Ironpath — Workout Tracker cho người Việt tập gym nghiêm túc',
  description: 'Log workouts, theo dõi PR, đồng bộ Apple Watch + Strava + Garmin. Đồng hành cùng 247+ gymer Việt Nam.',
  keywords: ['fitness', 'gym', 'workout tracker', 'tập gym', 'PR', 'cá nhân tốt nhất', 'Apple Watch'],
  openGraph: {
    title: 'Ironpath — Log workouts, smash PRs',
    description: 'Workout tracker cho gymer Việt. Đồng bộ Apple Watch + Strava.',
    type: 'website',
    locale: 'vi_VN'
  }
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="vi">
      <body className="bg-ink-950 antialiased">{children}</body>
    </html>
  );
}