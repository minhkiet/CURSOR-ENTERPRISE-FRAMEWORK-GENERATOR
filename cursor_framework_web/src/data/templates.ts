export type Template = {
  id: string
  slug: string
  name: string
  category: string
  tagline: string
  description: string
  industry: string
  accent: string
  accentSecondary: string
  bgGradient: string
  icon: string
  features: string[]
  highlights: { label: string; value: string }[]
  tags: string[]
  fileSize: string
  pages: number
  techStack: string[]
}

export const templates: Template[] = [
  {
    id: 'crm',
    slug: 'crm',
    name: 'CRM Dashboard',
    category: 'Customer Relationship',
    tagline: 'Quản lý khách hàng thông minh',
    description:
      'Landing page cho phần mềm CRM với dashboard trực quan, quản lý pipeline, contact segmentation và tự động hóa quy trình bán hàng. Phù hợp SaaS B2B, sales teams, agencies.',
    industry: 'CRM',
    accent: '#6366f1',
    accentSecondary: '#a78bfa',
    bgGradient: 'linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #4338ca 100%)',
    icon: 'users',
    features: [
      'Pipeline visualization với drag-drop',
      'Contact segmentation thông minh',
      'Email automation & templates',
      'Real-time analytics dashboard',
      'Multi-tenant architecture ready'
    ],
    highlights: [
      { label: 'Conversion Rate', value: '+47%' },
      { label: 'Customer Retention', value: '92%' },
      { label: 'Avg Deal Size', value: '$8.4K' }
    ],
    tags: ['Dashboard', 'Pipeline', 'Analytics', 'Automation'],
    fileSize: '248 KB',
    pages: 6,
    techStack: ['HTML5', 'CSS3', 'Vanilla JS', 'Chart.js']
  },
  {
    id: 'sale',
    slug: 'sale',
    name: 'Sale Pro',
    category: 'Sales & E-commerce',
    tagline: 'Trang bán hàng chuyển đổi cao',
    description:
      'Landing page tối ưu conversion cho e-commerce, flash sale, product launch. Tập trung vào urgency, social proof và checkout flow mượt mà. A/B tested.',
    industry: 'E-COMMERCE',
    accent: '#f97316',
    accentSecondary: '#fbbf24',
    bgGradient: 'linear-gradient(135deg, #7c2d12 0%, #9a3412 50%, #c2410c 100%)',
    icon: 'cart',
    features: [
      'Hero với countdown timer',
      'Product gallery + variants',
      'Customer reviews carousel',
      'Sticky checkout bar',
      'Mobile-first responsive'
    ],
    highlights: [
      { label: 'Add-to-Cart Rate', value: '24%' },
      { label: 'Avg Order Value', value: '$127' },
      { label: 'Page Load', value: '0.8s' }
    ],
    tags: ['E-commerce', 'High-converting', 'Mobile-first'],
    fileSize: '215 KB',
    pages: 5,
    techStack: ['HTML5', 'CSS3', 'Vanilla JS']
  },
  {
    id: 'bazi',
    slug: 'bazi',
    name: 'Bazi Tử Vi',
    category: 'Tử Vi & Phong Thủy',
    tagline: 'Xem vận mệnh theo Tứ Trụ',
    description:
      'Landing page huyền bí, uy tín cho dịch vụ xem Bazi, Tử Vi, phong thủy. Thiết kế Á Đông hiện đại với hiệu ứng cổ điển, mang lại cảm giác tâm linh và chuyên nghiệp.',
    industry: 'BAZI',
    accent: '#dc2626',
    accentSecondary: '#fbbf24',
    bgGradient: 'linear-gradient(135deg, #450a0a 0%, #7c2d12 50%, #991b1b 100%)',
    icon: 'yin-yang',
    features: [
      'Tứ Trụ interactive demo',
      'Form nhập ngày giờ sinh',
      'Luận giải can chi chi tiết',
      'Bảng hợp màu, hợp hướng',
      'Tích hợp thanh toán QR'
    ],
    highlights: [
      { label: 'Khách hàng tin tưởng', value: '15K+' },
      { label: 'Đánh giá 5 sao', value: '4.9/5' },
      { label: 'Thời gian giao', value: '24h' }
    ],
    tags: ['Tử Vi', 'Phong Thủy', 'Tâm Linh'],
    fileSize: '289 KB',
    pages: 7,
    techStack: ['HTML5', 'CSS3', 'Vanilla JS', 'SVG Animations']
  },
  {
    id: 'numerology',
    slug: 'numerology',
    name: 'Numerology Life',
    category: 'Thần Số Học',
    tagline: 'Khám phá sức mạnh con số',
    description:
      'Landing page hiện đại, tối giản cho dịch vụ Thần Số Học Pythagoras. Tính toán Life Path, Expression, Soul Urge numbers. Giao diện thiên hà, huyền ảo, cuốn hút.',
    industry: 'NUMEROLOGY',
    accent: '#06b6d4',
    accentSecondary: '#a855f7',
    bgGradient: 'linear-gradient(135deg, #0c0a4d 0%, #1e1b4b 50%, #312e81 100%)',
    icon: 'star',
    features: [
      'Calculator 6 chỉ số chính',
      'Biểu đồ trực quan sinh động',
      'Báo cáo PDF tự động',
      'Personalized insights AI',
      'Cosmic animations'
    ],
    highlights: [
      { label: 'Độ chính xác', value: '99.2%' },
      { label: 'Reports/ngày', value: '500+' },
      { label: 'Languages', value: '3 (VI/EN)' }
    ],
    tags: ['Thần Số Học', 'Pythagoras', 'Self-discovery'],
    fileSize: '267 KB',
    pages: 6,
    techStack: ['HTML5', 'CSS3', 'Vanilla JS', 'Canvas API']
  },
  {
    id: 'blog',
    slug: 'blog',
    name: 'Blog Editorial',
    category: 'Magazine & Editorial',
    tagline: 'Trải nghiệm đọc tuyệt vời',
    description:
      'Template blog/magazine cao cấp với typography đẳng cấp, reading time, dark mode. Tối ưu SEO, Core Web Vitals, accessibility AA. Phù hợp tech blog, lifestyle, news.',
    industry: 'EDITORIAL',
    accent: '#10b981',
    accentSecondary: '#34d399',
    bgGradient: 'linear-gradient(135deg, #064e3b 0%, #065f46 50%, #047857 100%)',
    icon: 'book',
    features: [
      'Editorial typography (Serif + Sans)',
      'Reading time + progress bar',
      'Dark mode auto switch',
      'Newsletter subscription widget',
      'Related posts algorithm'
    ],
    highlights: [
      { label: 'Lighthouse Score', value: '100/100' },
      { label: 'Avg Read Time', value: '6m 24s' },
      { label: 'Bounce Rate', value: '12%' }
    ],
    tags: ['Blog', 'Magazine', 'SEO-ready', 'Accessibility'],
    fileSize: '192 KB',
    pages: 8,
    techStack: ['HTML5', 'CSS3', 'Vanilla JS']
  },
  {
    id: 'portfolio',
    slug: 'portfolio',
    name: 'Portfolio Studio',
    category: 'Creative Showcase',
    tagline: 'Portfolio cho designer & dev',
    description:
      'Landing page portfolio tối giản, tinh tế cho designer, developer, photographer. Showcase projects với hiệu ứng parallax, masonry layout, smooth animations.',
    industry: 'PORTFOLIO',
    accent: '#ec4899',
    accentSecondary: '#f472b6',
    bgGradient: 'linear-gradient(135deg, #500724 0%, #831843 50%, #9d174d 100%)',
    icon: 'sparkles',
    features: [
      'Masonry project gallery',
      'Case study templates',
      'Skills visualization',
      'Contact form với validation',
      'Smooth scroll animations'
    ],
    highlights: [
      { label: 'Awwwards', value: 'Site of Day' },
      { label: 'CSS Design Awards', value: 'Best UI' },
      { label: 'Load Time', value: '< 1s' }
    ],
    tags: ['Portfolio', 'Designer', 'Creative', 'Minimal'],
    fileSize: '234 KB',
    pages: 5,
    techStack: ['HTML5', 'CSS3', 'Vanilla JS', 'GSAP']
  }
]

export function getTemplateById(id: string): Template | undefined {
  return templates.find((t) => t.id === id || t.slug === id)
}