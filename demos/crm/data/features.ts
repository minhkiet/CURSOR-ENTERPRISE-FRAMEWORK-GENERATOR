export interface Feature {
  id: string;
  icon: string;
  title: string;
  description: string;
  metric: string;
  metricLabel: string;
  cellSize: '2x2' | '1x1' | '2x1';
  variant: 'large' | 'small';
}

export const FEATURES: Feature[] = [
  {
    id: 'pipeline',
    icon: 'Kanban',
    title: 'Pipeline 5-stage',
    description: 'Kéo deal giữa các stages. Xem tổng giá trị từng stage. Forecast dựa trên win-rate từng stage.',
    metric: '47,8 tỷ',
    metricLabel: 'pipeline value',
    cellSize: '2x2',
    variant: 'large'
  },
  {
    id: 'contacts',
    icon: 'UsersThree',
    title: 'Quản lý contacts',
    description: 'Bulk import từ CSV/Excel. Tự động enrich từ email. Segment theo industry, deal value.',
    metric: '10.247',
    metricLabel: 'contacts',
    cellSize: '1x1',
    variant: 'small'
  },
  {
    id: 'automation',
    icon: 'Lightning',
    title: 'Workflow automation',
    description: 'Trigger tự động khi deal thay đổi stage. Slack notification. Email reminder.',
    metric: '247',
    metricLabel: 'auto triggers/ngày',
    cellSize: '1x1',
    variant: 'small'
  },
  {
    id: 'forecast',
    icon: 'ChartLineUp',
    title: 'AI-driven forecast',
    description: 'Dựa trên historical win rate, deal velocity, rep activity. Không đoán mò.',
    metric: '92%',
    metricLabel: 'forecast accuracy',
    cellSize: '1x1',
    variant: 'small'
  },
  {
    id: 'reports',
    icon: 'ChartBar',
    title: 'Reports tùy chỉnh',
    description: '30+ templates có sẵn. Custom dashboard cho sales rep / manager / executive. Export PDF/CSV.',
    metric: '30+',
    metricLabel: 'templates',
    cellSize: '2x1',
    variant: 'small'
  },
  {
    id: 'integrations',
    icon: 'Plugs',
    title: 'Tích hợp native',
    description: 'Gmail · Slack · Outlook · Zoom · Google Calendar · MISA · ERP. Webhook cho custom integration.',
    metric: '47+',
    metricLabel: 'tích hợp',
    cellSize: '1x1',
    variant: 'small'
  }
];