export const TESTIMONIALS = [
  {
    id: 'fpt',
    company: 'FPT Software',
    companySlug: 'fpt',
    industry: 'IT Services',
    avatarId: '1507003211169-0a1dd7228f2d',
    name: 'Trần Minh',
    title: 'VP Sales, FPT Software',
    quote: 'Pipeline visibility tốt hơn 4 lần. Sales rep xử lý 247 deals/quarter thay vì 32 như trước. Forecast chính xác 92%.',
    metrics: [
      { label: 'Pipeline value', value: '+47%', icon: 'TrendUp' },
      { label: 'Win rate', value: '32% → 47%', icon: 'Trophy' }
    ],
    cellSize: 'small' as const
  },
  {
    id: 'vng',
    company: 'VNG Corporation',
    companySlug: 'vng',
    industry: 'Tech',
    avatarId: '1494790108377-be9c29b29330',
    name: 'Lê Lan',
    title: 'CRO, VNG',
    quote: '5 đội sales phối hợp 1 pipeline. Cycle time rút ngắn từ 89 ngày còn 64 ngày. ROI dương sau 4 tháng.',
    metrics: [
      { label: 'Close rate', value: '+82%', icon: 'TrendUp' },
      { label: 'Sales cycle', value: '-28%', icon: 'Clock' }
    ],
    cellSize: 'small' as const
  },
  {
    id: 'tma',
    company: 'TMA Solutions',
    companySlug: 'tma',
    industry: 'Outsourcing',
    avatarId: '1472099645785-5658abf4ff4e',
    name: 'Nguyễn Quốc Quân',
    title: 'Sales Director, TMA',
    quote: 'Migrate từ Salesforce sang Northwind tiết kiệm 2.4 tỷ/năm license. Custom workflow cho 6 loại hợp đồng enterprise. API webhook giúp tự động sync với ERP nội bộ.',
    metrics: [
      { label: 'License savings', value: '2.4 tỷ/năm', icon: 'CurrencyDollar' },
      { label: 'Deals/quarter', value: '247', icon: 'Briefcase' }
    ],
    cellSize: 'wide' as const
  }
];

export const LOGO_WALL = [
  'fpt', 'vng', 'vingroup', 'vnpt', 'viettel', 'momo', 'tiki', 'shopee', 'lazada', 'sendo', 'tma', 'kms'
];