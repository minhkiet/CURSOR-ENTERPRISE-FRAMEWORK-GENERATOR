import { StickyHeader } from '@/components/StickyHeader';
import { Hero, TrustStrip } from '@/components/Hero';
import { FeatureBento } from '@/components/FeatureBento';
import { IntegrationsSection } from '@/components/IntegrationsSection';
import { DashboardShowcase } from '@/components/DashboardShowcase';
import { PipelineShowcase } from '@/components/PipelineShowcase';
import { PricingSection } from '@/components/PricingSection';
import { TestimonialSection } from '@/components/TestimonialSection';
import { MegaFooter } from '@/components/MegaFooter';

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-50">
      <StickyHeader />
      <Hero />
      <TrustStrip />
      <FeatureBento />
      <IntegrationsSection />
      <DashboardShowcase />
      <PipelineShowcase />
      <PricingSection />
      <TestimonialSection />
      <MegaFooter />
    </main>
  );
}