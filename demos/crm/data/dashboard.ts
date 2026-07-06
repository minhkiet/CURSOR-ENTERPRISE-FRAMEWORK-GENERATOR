export const KPI_MAIN = {
  revenue: '47,8',
  revenueUnit: 'tỷ VND',
  delta: '+18,2%',
  deltaLabel: 'vs Q2 2026',
  subtitle: 'Revenue Q3 2026'
};

export const KPIS_SECONDARY = [
  { label: 'Win rate', value: '68%', delta: '+5pp', trend: 'up' as const },
  { label: 'Avg deal size', value: '195M', unit: 'VND', delta: '-8%', trend: 'down' as const },
  { label: 'Sales cycle', value: '64', unit: 'ngày', delta: '-12 ngày', trend: 'up' as const },
  { label: 'Reps active', value: '247', delta: '+38 mới', trend: 'up' as const }
];

export const SPARKLINE_POINTS = '0,52 17,48 34,45 51,40 68,38 85,32 102,30 119,25 136,22 153,18 170,12 187,8';

export const ACTIVITY_FEED = [
  { icon: 'Phone', color: 'indigo', text: 'Minh gọi với Trần Minh · FPT Software', time: '2 giờ trước' },
  { icon: 'TrendUp', color: 'emerald', text: 'Lan advance deal VNG Migration → Negotiation', time: '4 giờ trước' },
  { icon: 'EnvelopeSimple', color: 'sky', text: 'Bảo gửi email cho TMA Solutions', time: '6 giờ trước' },
  { icon: 'CalendarCheck', color: 'amber', text: 'Lan họp với CTO VNG', time: '1 ngày trước' },
  { icon: 'Trophy', color: 'emerald', text: 'Minh close deal FPT License · 1,2 tỷ', time: '2 ngày trước' }
];

export const STUCK_DEALS = [
  { name: 'Acme Corp', days: 5, value: '450M' },
  { name: 'BetaCo', days: 12, value: '1.2 tỷ' },
  { name: 'GammaTech', days: 8, value: '680M' },
  { name: 'Delta Ltd', days: 4, value: '230M' }
];