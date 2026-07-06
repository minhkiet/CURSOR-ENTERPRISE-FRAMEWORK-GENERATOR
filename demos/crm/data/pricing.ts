export interface PricingTier {
  id: string;
  name: string;
  description: string;
  priceMonthly: number | 'contact';
  priceAnnual: number | 'contact';
  features: Array<{ text: string; included: boolean }>;
  cta: { label: string; href: string };
  recommended: boolean;
}

export const TIERS: PricingTier[] = [
  {
    id: 'starter',
    name: 'Starter',
    description: 'Cho team nhỏ 1-5 người bắt đầu quản lý pipeline',
    priceMonthly: 199000,
    priceAnnual: 158000,
    features: [
      { text: 'Tối đa 5 người dùng', included: true },
      { text: 'Pipeline + Contacts + Deals', included: true },
      { text: 'Email + chat support', included: true },
      { text: 'Báo cáo cơ bản', included: true },
      { text: 'Không giới hạn deals', included: true },
      { text: 'Mobile app', included: true },
      { text: 'Workflow automation', included: false },
      { text: 'API + Webhook', included: false }
    ],
    cta: { label: 'Bắt đầu miễn phí', href: '/signup?plan=starter' },
    recommended: false
  },
  {
    id: 'pro',
    name: 'Pro',
    description: 'Cho team 5-50 người cần automation và báo cáo nâng cao',
    priceMonthly: 599000,
    priceAnnual: 479000,
    features: [
      { text: 'Tối đa 50 người dùng', included: true },
      { text: 'Mọi thứ ở Starter +', included: true },
      { text: 'Workflow automation', included: true },
      { text: 'API + Webhook không giới hạn', included: true },
      { text: 'Báo cáo nâng cao + Forecast', included: true },
      { text: 'Email + chat + phone support', included: true },
      { text: 'Slack + Gmail integration', included: true },
      { text: 'Custom SSO / SAML', included: false }
    ],
    cta: { label: 'Dùng thử 14 ngày', href: '/signup?plan=pro' },
    recommended: true
  },
  {
    id: 'enterprise',
    name: 'Enterprise',
    description: 'Cho tổ chức 50+ người với yêu cầu security cao',
    priceMonthly: 'contact',
    priceAnnual: 'contact',
    features: [
      { text: 'Không giới hạn người dùng', included: true },
      { text: 'Mọi thứ ở Pro +', included: true },
      { text: 'Custom SSO / SAML / SCIM', included: true },
      { text: 'Dedicated CSM 24/7', included: true },
      { text: 'Custom SLA 99.99%', included: true },
      { text: 'Audit log + Compliance', included: true },
      { text: 'On-premise deployment', included: true },
      { text: 'Hợp đồng pháp lý tùy chỉnh', included: true }
    ],
    cta: { label: 'Liên hệ sales', href: '/contact?plan=enterprise' },
    recommended: false
  }
];