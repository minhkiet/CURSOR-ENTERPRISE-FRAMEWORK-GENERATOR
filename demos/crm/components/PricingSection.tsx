'use client';
import { useState } from 'react';
import * as Phosphor from '@phosphor-icons/react';
import { TIERS } from '@/data/pricing';

export function PricingSection() {
  const [billing, setBilling] = useState<'monthly' | 'annual'>('annual');

  return (
    <section id="pricing" className="bg-slate-50 py-16 lg:py-24" aria-labelledby="pricing-heading">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-12">
          <span className="inline-block text-[11px] font-bold uppercase tracking-[0.18em] text-indigo-600 mb-2">
            Bảng giá
          </span>
          <h2 id="pricing-heading" className="text-3xl lg:text-5xl font-extrabold text-slate-900 tracking-tight">
            Chọn gói phù hợp với team
          </h2>
          <p className="mt-3 text-slate-600 max-w-2xl mx-auto">
            14 ngày dùng thử miễn phí, không cần thẻ tín dụng. Hủy bất kỳ lúc nào.
          </p>

          <div className="mt-6 inline-flex items-center gap-1 p-1 bg-slate-100 rounded-lg" role="tablist" aria-label="Chu kỳ thanh toán">
            <button
              role="tab"
              aria-selected={billing === 'monthly'}
              onClick={() => setBilling('monthly')}
              className={`px-4 py-2 text-[13px] font-semibold rounded-md transition-colors ${
                billing === 'monthly' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500 hover:text-slate-700'
              }`}
            >
              Monthly
            </button>
            <button
              role="tab"
              aria-selected={billing === 'annual'}
              onClick={() => setBilling('annual')}
              className={`px-4 py-2 text-[13px] font-semibold rounded-md transition-colors inline-flex items-center gap-1.5 ${
                billing === 'annual' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500 hover:text-slate-700'
              }`}
            >
              Annual
              <span className="inline-flex items-center gap-0.5 px-1.5 py-0.5 bg-emerald-100 text-emerald-700 text-[10.5px] font-bold rounded">
                -20%
              </span>
            </button>
          </div>
        </div>

        {/* Tiers */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-5 lg:gap-6 max-w-6xl mx-auto">
          {TIERS.map(tier => (
            <PricingCard key={tier.id} tier={tier} billing={billing} />
          ))}
        </div>

        <p className="mt-10 text-center text-[13px] text-slate-500">
          Tất cả gói bao gồm: SSL · GDPR-compliant · Backups hàng ngày · 99.9% uptime
        </p>
      </div>
    </section>
  );
}

function PricingCard({ tier, billing }: { tier: typeof TIERS[number]; billing: 'monthly' | 'annual' }) {
  const price = billing === 'annual' ? tier.priceAnnual : tier.priceMonthly;

  return (
    <article
      aria-label={`Gói ${tier.name}`}
      className={`relative bg-white rounded-2xl border-2 ${
        tier.recommended ? 'border-indigo-500 shadow-2xl' : 'border-slate-200 shadow-sm'
      } p-6 lg:p-7 hover:shadow-lg transition-shadow`}
    >
      {tier.recommended && (
        <div className="absolute -top-3 left-1/2 -translate-x-1/2 px-3 py-1 bg-gradient-to-r from-indigo-600 to-indigo-700 text-white text-[11px] font-bold uppercase tracking-wider rounded-full shadow-lg inline-flex items-center gap-1" aria-label="Gói được đề xuất">
          <Phosphor.Sparkle size={11} weight="fill" />
          Đề xuất
        </div>
      )}

      <div>
        <h3 className="text-[20px] font-extrabold text-slate-900 flex items-center gap-2">
          {tier.recommended && <Phosphor.Crown size={20} weight="fill" className="text-indigo-600" />}
          {tier.name}
        </h3>
        <p className="mt-2 text-[13px] text-slate-600 leading-relaxed">
          {tier.description}
        </p>
      </div>

      <div className="mt-6 mb-6">
        {price === 'contact' ? (
          <p className="text-[28px] font-extrabold text-slate-900">Liên hệ</p>
        ) : (
          <div className="flex items-baseline gap-1.5">
            <span className="text-[10px] font-bold text-indigo-600">₫</span>
            <span aria-label={`Giá ${price.toLocaleString('vi-VN')} đồng mỗi người dùng mỗi tháng`} className="text-[44px] font-extrabold text-slate-900 tabular-nums leading-none">
              {price.toLocaleString('vi-VN')}
            </span>
            <span className="text-[13px] text-slate-500 font-medium">/user/tháng</span>
          </div>
        )}
        {billing === 'annual' && price !== 'contact' && (
          <p className="mt-1 text-[11.5px] text-emerald-600 font-semibold">
            Tiết kiệm 20% khi thanh toán annual
          </p>
        )}
      </div>

      <ul className="space-y-2.5 mb-6">
        {tier.features.map((f, i) => (
          <li key={i} className="flex items-start gap-2 text-[13px]">
            {f.included ? (
              <Phosphor.CheckCircle size={16} weight="fill" className="text-emerald-500 flex-shrink-0 mt-0.5" />
            ) : (
              <Phosphor.X size={16} weight="bold" className="text-slate-300 flex-shrink-0 mt-0.5" />
            )}
            <span className={f.included ? 'text-slate-700' : 'text-slate-400 line-through'}>{f.text}</span>
          </li>
        ))}
      </ul>

      <a
        href={tier.cta.href}
        className={`flex items-center justify-center gap-1.5 w-full py-3 text-[13.5px] font-bold rounded-xl transition-colors ${
          tier.recommended
            ? 'bg-gradient-to-r from-indigo-600 to-indigo-700 hover:from-indigo-700 hover:to-indigo-800 text-white shadow-lg shadow-indigo-200'
            : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
        }`}
      >
        {tier.cta.label}
        <Phosphor.ArrowRight size={14} weight="bold" />
      </a>
    </article>
  );
}