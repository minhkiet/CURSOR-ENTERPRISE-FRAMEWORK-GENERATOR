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
    id: 'pipeline',
    icon: 'Kanban',
    title: 'Pipeline visualization 5-stage',
    description: 'Kéo deal giữa các stages. Xem tổng giá trị từng stage. Forecast dựa trên win-rate từng stage.',
    metric: '+47% pipeline value',
    variant: 'large'
  },
  {
    id: 'contacts',
    icon: 'UsersThree',
    title: 'Quản lý 10.000+ contacts',
    description: 'Bulk import từ CSV/Excel. Tự động enrich từ email. Segment theo industry, deal value.',
    metric: '10.247 contacts',
    variant: 'small'
  },
  {
    id: 'automation',
    icon: 'Lightning',
    title: 'Workflow automation',
    description: 'Trigger tự động khi deal thay đổi stage. Slack notification. Email reminder. Sync ERP.',
    metric: '247 deals auto',
    variant: 'small'
  },
  {
    id: 'forecast',
    icon: 'ChartLineUp',
    title: 'Forecast chính xác 92%',
    description: 'AI-driven forecast dựa trên historical win rate, deal velocity, rep activity. Không đoán mò.',
    metric: '92% accuracy',
    variant: 'small'
  },
  {
    id: 'reports',
    icon: 'ChartBar',
    title: 'Reports tùy chỉnh',
    description: '30+ templates có sẵn. Custom dashboard cho sales rep / manager / executive. Export PDF/CSV.',
    metric: '30+ templates',
    variant: 'small'
  },
  {
    id: 'integrations',
    icon: 'Plugs',
    title: 'Tích hợp native',
    description: 'Gmail · Slack · Outlook · Zoom · Google Calendar · MISA · ERP. Webhook cho custom integration.',
    metric: '47+ tích hợp',
    variant: 'small'
  }
];