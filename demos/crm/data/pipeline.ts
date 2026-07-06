export interface Deal {
  id: string;
  title: string;
  company: string;
  companySlug: string;
  value: number;
  owner: { name: string; avatarId: string };
  age: number;
  lastActivity: string;
  stage: string;
  isHot: boolean;
  isStalled: boolean;
}

export interface Stage {
  id: string;
  name: string;
  icon: string;
  probability: number;
}

export const STAGES: Stage[] = [
  { id: 'lead', name: 'Lead', icon: 'DownloadSimple', probability: 10 },
  { id: 'qualified', name: 'Qualified', icon: 'Target', probability: 30 },
  { id: 'proposal', name: 'Proposal', icon: 'FileText', probability: 50 },
  { id: 'negotiation', name: 'Negotiation', icon: 'ChatsTeardrop', probability: 70 },
  { id: 'won', name: 'Won', icon: 'CheckCircle', probability: 100 }
];

export const SAMPLE_DEALS: Deal[] = [
  {
    id: 'd1',
    title: 'Phần mềm CRM 50 users',
    company: 'FPT Software',
    companySlug: 'fpt',
    value: 1200000000,
    owner: { name: 'Minh', avatarId: '1507003211169-0a1dd7228f2d' },
    age: 2,
    lastActivity: '2 giờ trước',
    stage: 'lead',
    isHot: true,
    isStalled: false
  },
  {
    id: 'd2',
    title: 'Enterprise License 200 users',
    company: 'VNG Corporation',
    companySlug: 'vng',
    value: 4500000000,
    owner: { name: 'Lan', avatarId: '1494790108377-be9c29b29330' },
    age: 15,
    lastActivity: '1 ngày trước',
    stage: 'qualified',
    isHot: false,
    isStalled: true
  },
  {
    id: 'd3',
    title: 'Migration project Q4',
    company: 'TMA Solutions',
    companySlug: 'tma',
    value: 2800000000,
    owner: { name: 'Bảo', avatarId: '1472099645785-5658abf4ff4e' },
    age: 7,
    lastActivity: '4 giờ trước',
    stage: 'proposal',
    isHot: true,
    isStalled: false
  },
  {
    id: 'd4',
    title: 'CRM cho 30 sales reps',
    company: 'Vingroup',
    companySlug: 'vingroup',
    value: 800000000,
    owner: { name: 'Mai', avatarId: '1438761681033-6461ffad8d80' },
    age: 10,
    lastActivity: '3 ngày trước',
    stage: 'qualified',
    isHot: false,
    isStalled: false
  },
  {
    id: 'd5',
    title: 'Government license 100 users',
    company: 'VNPT',
    companySlug: 'vnpt',
    value: 3200000000,
    owner: { name: 'Tuấn', avatarId: '1500648767791-00dcc994a43e' },
    age: 5,
    lastActivity: '6 giờ trước',
    stage: 'negotiation',
    isHot: true,
    isStalled: false
  }
];