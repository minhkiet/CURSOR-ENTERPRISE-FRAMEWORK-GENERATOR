import { StickyHeader } from '@/components/StickyHeader';
import { Hero } from '@/components/Hero';
import { FeatureBento } from '@/components/FeatureBento';
import { WorkoutShowcase } from '@/components/WorkoutShowcase';
import { PRShowcase } from '@/components/PRShowcase';
import { VolumeChart } from '@/components/VolumeChart';
import { ProgramLibrary } from '@/components/ProgramLibrary';
import { MegaFooter } from '@/components/MegaFooter';

export default function Home() {
  return (
    <main className="min-h-screen bg-ink-950">
      <StickyHeader />
      <Hero />
      <FeatureBento />
      <WorkoutShowcase />
      <PRShowcase />
      <VolumeChart />
      <ProgramLibrary />
      <MegaFooter />
    </main>
  );
}