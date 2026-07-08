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
  },
  {
    id: 'food-delivery',
    slug: 'food-delivery',
    name: 'Lẩu Đêm',
    category: 'Food & Beverage',
    tagline: 'Đặt đồ ăn 30 phút, nóng hổi',
    description:
      'Landing page app giao đồ ăn tối Việt Nam. Tracking thời gian thực, đa nhà hàng, thanh toán MoMo/ZaloPay. Phù hợp F&B startup, chuỗi quán ăn, dark kitchen.',
    industry: 'F&B',
    accent: '#ef4444',
    accentSecondary: '#fb923c',
    bgGradient: 'linear-gradient(135deg, #7c2d12 0%, #991b1b 50%, #b91c1c 100%)',
    icon: 'fork-knife',
    features: [
      'GPS tracking shipper realtime',
      'Menu đa nhà hàng, filter theo món',
      'Thanh toán MoMo, ZaloPay, tiền mặt',
      'Đánh giá & review sau giao',
      'Mã giảm giá & loyalty program'
    ],
    highlights: [
      { label: 'Đơn/ngày', value: '12K+' },
      { label: 'Đúng giờ', value: '94%' },
      { label: 'Nhà hàng', value: '2,400+' }
    ],
    tags: ['Food', 'Delivery', 'Mobile-first', 'Realtime'],
    fileSize: '256 KB',
    pages: 6,
    techStack: ['HTML5', 'CSS3', 'Vanilla JS', 'Mapbox GL']
  },
  {
    id: 'edu-tutor',
    slug: 'edu-tutor',
    name: 'Gia Sư Việt',
    category: 'Education & Tutor',
    tagline: 'Gia sư 1-1, lộ trình cá nhân hoá',
    description:
      'Landing page nền tảng kết nối gia sư Việt Nam. Lộ trình học riêng cho từng học sinh, lớp thử miễn phí, công cụ luyện tập. Phù hợp trung tâm, gia sư tự do, edtech startup.',
    industry: 'EDUCATION',
    accent: '#3b82f6',
    accentSecondary: '#06b6d4',
    bgGradient: 'linear-gradient(135deg, #1e3a8a 0%, #1d4ed8 50%, #2563eb 100%)',
    icon: 'graduation-cap',
    features: [
      'Matching AI theo trình độ & mục tiêu',
      'Lớp thử 30 phút miễn phí',
      'Bảng điểm & báo cáo phụ huynh',
      'Luyện tập tương tác, chấm tự động',
      'Thanh toán theo buổi hoặc gói tháng'
    ],
    highlights: [
      { label: 'Gia sư', value: '4,800+' },
      { label: 'Học sinh', value: '38K' },
      { label: 'Đậu ĐH', value: '92%' }
    ],
    tags: ['Education', '1-on-1', 'AI-matching', 'Parent-dashboard'],
    fileSize: '273 KB',
    pages: 7,
    techStack: ['HTML5', 'CSS3', 'Vanilla JS', 'Chart.js']
  },
  {
    id: 'beauty-spa',
    slug: 'beauty-spa',
    name: 'Sen Spa',
    category: 'Beauty & Wellness',
    tagline: 'Spa cao cấp, đặt lịch 60 giây',
    description:
      'Landing page cho spa & salon làm đẹp cao cấp. Đặt lịch trực tuyến, chọn therapist, gallery trước-sau. Phù hợp spa, beauty clinic, nail salon, hair studio.',
    industry: 'BEAUTY',
    accent: '#ec4899',
    accentSecondary: '#a78bfa',
    bgGradient: 'linear-gradient(135deg, #4c1d95 0%, #6b21a8 50%, #831843 100%)',
    icon: 'flower-lotus',
    features: [
      'Booking realtime với calendar widget',
      'Chọn therapist yêu thích',
      'Gallery before/after (consent-based)',
      'Gói membership & loyalty',
      'Nhắc lịch tự động qua Zalo'
    ],
    highlights: [
      { label: 'Chi nhánh', value: '24' },
      { label: 'Khách quay lại', value: '78%' },
      { label: 'Đánh giá', value: '4.9★' }
    ],
    tags: ['Spa', 'Booking', 'Membership', 'Wellness'],
    fileSize: '241 KB',
    pages: 5,
    techStack: ['HTML5', 'CSS3', 'Vanilla JS']
  },
  {
    id: 'fitness',
    slug: 'fitness',
    name: 'GymZone',
    category: 'Fitness & Yoga',
    tagline: 'Tập luyện thông minh, kết quả thật',
    description:
      'Landing page cho phòng gym, yoga studio, boxing club. Đặt lớp realtime, theo dõi tiến độ, coach 1-1 video call. Phù hợp chuỗi fitness, boutique studio, personal trainer.',
    industry: 'FITNESS',
    accent: '#22c55e',
    accentSecondary: '#eab308',
    bgGradient: 'linear-gradient(135deg, #14532d 0%, #166534 50%, #15803d 100%)',
    icon: 'dumbbell',
    features: [
      'Class booking với waitlist tự động',
      'Workout plan cá nhân hoá theo goal',
      'Progress tracking: weight, reps, PR',
      'Video call 1-1 với coach',
      'Cộng đồng & thử thách hàng tuần'
    ],
    highlights: [
      { label: 'Hội viên', value: '18K+' },
      { label: 'Lớp/tuần', value: '420' },
      { label: 'Coach', value: '120' }
    ],
    tags: ['Gym', 'Yoga', 'Booking', 'Tracking'],
    fileSize: '228 KB',
    pages: 6,
    techStack: ['HTML5', 'CSS3', 'Vanilla JS', 'GSAP']
  },
  {
    id: 'realestate',
    slug: 'realestate',
    name: 'Nhà Tốt',
    category: 'Real Estate',
    tagline: 'Mua bán & cho thuê BĐS minh bạch',
    description:
      'Landing page nền tảng BĐS Việt Nam. Listing chi tiết, bản đồ giá, lịch xem nhà online, AI gợi ý theo ngân sách. Phù hợp sàn BĐS, môi giới, chủ nhà.',
    industry: 'REAL ESTATE',
    accent: '#f59e0b',
    accentSecondary: '#10b981',
    bgGradient: 'linear-gradient(135deg, #78350f 0%, #92400e 50%, #b45309 100%)',
    icon: 'house',
    features: [
      'Bản đồ giá BĐS theo quận/huyện',
      'Virtual tour 3D & ảnh 360°',
      'AI matching theo ngân sách + nhu cầu',
      'Đặt lịch xem nhà online',
      'Pháp lý check tự động (sổ đỏ, quy hoạch)'
    ],
    highlights: [
      { label: 'Tin đăng', value: '124K' },
      { label: 'Thành phố', value: '63' },
      { label: 'Verified', value: '100%' }
    ],
    tags: ['Real Estate', 'Map', 'AI-match', 'Virtual Tour'],
    fileSize: '298 KB',
    pages: 7,
    techStack: ['HTML5', 'CSS3', 'Vanilla JS', 'Mapbox GL']
  },
  {
    id: 'travel',
    slug: 'travel',
    name: 'Viet Travel',
    category: 'Travel & Tour',
    tagline: 'Tour Đông Nam Á, đặt nhanh 2 phút',
    description:
      'Landing page công ty du lịch & tour Đông Nam Á. Itinerary chi tiết, review thật từ khách, thanh toán linh hoạt. Phù hợp công ty tour, OTA nhỏ, homestay network.',
    industry: 'TRAVEL',
    accent: '#06b6d4',
    accentSecondary: '#f59e0b',
    bgGradient: 'linear-gradient(135deg, #0c4a6e 0%, #075985 50%, #0369a1 100%)',
    icon: 'airplane-tilt',
    features: [
      'Itinerary từng ngày với map chi tiết',
      'Review thật từ khách đã đi (có ảnh)',
      'Thanh toán trả góp 0% qua thẻ tín dụng',
      'So sánh giá 50+ hãng bay khác nhau',
      'Hỗ trợ 24/7 qua Zalo & hotline'
    ],
    highlights: [
      { label: 'Tour/năm', value: '8,400+' },
      { label: 'Điểm đến', value: '120' },
      { label: 'Quay lại', value: '64%' }
    ],
    tags: ['Travel', 'Tour', 'Booking', 'Southeast Asia'],
    fileSize: '262 KB',
    pages: 6,
    techStack: ['HTML5', 'CSS3', 'Vanilla JS', 'Mapbox GL']
  },
  {
    id: 'farm',
    slug: 'farm',
    name: 'GreenFarm',
    category: 'Nong Trai & Nong San',
    tagline: 'Nong san hieu organic, giao tan cong',
    description:
      'Landing page cho trang trai organic, shop nong san sach. San pham tuoi song, giao hang trong ngay, farm-to-table. Phu hop trai organic, cuu nong trai, san pham dac san vung mien.',
    industry: 'FARM',
    accent: '#16a34a',
    accentSecondary: '#eab308',
    bgGradient: 'linear-gradient(135deg, #14532d 0%, #166534 50%, #22c55e 100%)',
    icon: 'plant',
    features: [
      'Danh muc san pham theo mua vu',
      'Dat hang & giao hang trong ngay',
      'Trai nghiem thu hoach',
      'Gia ca minh bac hon chplay',
      'Trai cay tuoi song'
    ],
    highlights: [
      { label: 'San pham', value: '200+' },
      { label: 'Khach hang', value: '15K' },
      { label: 'Giao hang', value: '2h' }
    ],
    tags: ['Nong trai', 'Organic', 'Farm-to-table', 'Giao hang'],
    fileSize: '245 KB',
    pages: 6,
    techStack: ['HTML5', 'CSS3', 'Vanilla JS']
  },
  {
    id: 'orchard',
    slug: 'orchard',
    name: 'TropicFruit',
    category: 'Vuon Trai Cay',
    tagline: 'Trai cay dac san Mien Dong',
    description:
      'Landing page cho vuon trai cay Mien Dong. Trai cay theo mua vu, tour thu hoach, goi qua tang. Phu hop vuon trai, tien luong, nong dan gia dinh.',
    industry: 'ORCHARD',
    accent: '#ea580c',
    accentSecondary: '#fbbf24',
    bgGradient: 'linear-gradient(135deg, #7c2d12 0%, #9a3412 50%, #ea580c 100%)',
    icon: 'tree',
    features: [
      'Lich trai cay theo mua vu',
      'Tour thu hoach & nha hang trai cay',
      'Goi qua tang & hanh trinh',
      'Ban si trai cay dac san',
      'Trai nghiem thu hoach that'
    ],
    highlights: [
      { label: 'Loai trai cay', value: '45+' },
      { label: 'Dien tich', value: '50 ha' },
      { label: 'Nam thanh lap', value: '1985' }
    ],
    tags: ['Vuon trai cay', 'Mien Dong', 'Du lich', 'Trai nghiem'],
    fileSize: '238 KB',
    pages: 5,
    techStack: ['HTML5', 'CSS3', 'Vanilla JS']
  },
  {
    id: 'agritech',
    slug: 'agritech',
    name: 'AgriTech Pro',
    category: 'Thiet Bi Nong San',
    tagline: 'Cong nghe nong nghiep hien dai',
    description:
      'Landing page cho cong ty thiet bi nong nghiep. May gap hoa, UAV drone, he thong tuoi tu dong. Phu hop nha phan phoi, trai nong, doanh nghiep nong nghiep.',
    industry: 'AGRITECH',
    accent: '#0891b2',
    accentSecondary: '#06b6d4',
    bgGradient: 'linear-gradient(135deg, #164e63 0%, #0e7490 50%, #0891b2 100%)',
    icon: 'tractor',
    features: [
      'May gap hoa hieu suat cao',
      'Drone phun thuoc tu dong',
      'He thong tuoi thong minh IoT',
      'Giao hang & bao hanh toan quoc',
      'Ky thuat hieu chinh'
    ],
    highlights: [
      { label: 'Thiet bi', value: '150+' },
      { label: 'Khach hang', value: '3,200+' },
      { label: 'Bao hanh', value: '2 nam' }
    ],
    tags: ['Thiet bi nong nghiep', 'Drone', 'IoT', 'Co khi'],
    fileSize: '256 KB',
    pages: 6,
    techStack: ['HTML5', 'CSS3', 'Vanilla JS', 'IoT']
  },
  {
    id: 'aitech',
    slug: 'aitech',
    name: 'NeuralAI',
    category: 'Cong Nghe AI',
    tagline: 'Giai phap AI cho doanh nghiep',
    description:
      'Landing page cho startup AI. Chatbot, phan tich du lieu, nhan dien hinh anh, NLP. Phu hop SaaS AI, tu van AI, startup cong nghe.',
    industry: 'AI TECH',
    accent: '#7c3aed',
    accentSecondary: '#a78bfa',
    bgGradient: 'linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #4c1d95 100%)',
    icon: 'brain',
    features: [
      'Chatbot AI tuyet ky',
      'Phan tich du lieu thong minh',
      'Nhan dien hinh anh chinh xac',
      'Xu ly ngon ngu tu nhien',
      'Giai phap theo ngach'
    ],
    highlights: [
      { label: 'Model', value: 'GPT-4' },
      { label: 'Do chinh xac', value: '97.8%' },
      { label: 'API calls', value: '1M+/thang' }
    ],
    tags: ['AI', 'Chatbot', 'Machine Learning', 'SaaS'],
    fileSize: '278 KB',
    pages: 7,
    techStack: ['HTML5', 'CSS3', 'Vanilla JS', 'AI APIs']
  },
  {
    id: 'computech',
    slug: 'computech',
    name: 'TechHub',
    category: 'Cong Nghe May Tinh',
    tagline: 'Laptop, PC gaming, linh kien chinh hang',
    description:
      'Landing page cho cua hang may tinh. Laptop gaming, PC build, linh kien, phu kien. Phu hop cua hang laptop, gaming gear, linh kien may tinh.',
    industry: 'COMPUTER',
    accent: '#dc2626',
    accentSecondary: '#f59e0b',
    bgGradient: 'linear-gradient(135deg, #450a0a 0%, #7f1d1d 50%, #991b1b 100%)',
    icon: 'laptop',
    features: [
      'Laptop gaming & van phong',
      'PC build theo yeu cau',
      'Linh kien chinh hang',
      'Trai nghiem thuc te',
      'Bao hanh & tra gop'
    ],
    highlights: [
      { label: 'San pham', value: '2,000+' },
      { label: 'Thuong hieu', value: '50+' },
      { label: 'Tra gop', value: '0%' }
    ],
    tags: ['Laptop', 'Gaming PC', 'Linh kien', 'Cong nghe'],
    fileSize: '264 KB',
    pages: 6,
    techStack: ['HTML5', 'CSS3', 'Vanilla JS']
  },
  {
    id: 'preschool',
    slug: 'preschool',
    name: 'Little Stars',
    category: 'Giao Duc Mam Non',
    tagline: 'Nuoi day tre trong tinh yeu',
    description:
      'Landing page cho truong mam non. Chuong trinh hoc theo doi tuong, co so vat chat hien dai, giao vien nhiet tinh. Phu hop truong mam non, nha tre, mam non chuyen biet.',
    industry: 'EDUCATION',
    accent: '#f97316',
    accentSecondary: '#84cc16',
    bgGradient: 'linear-gradient(135deg, #7c2d12 0%, #9a3412 50%, #f97316 100%)',
    icon: 'baby',
    features: [
      'Chuong trinh hoc theo nhom tuoi',
      'Co so vat chat hien dai',
      'Giao vien chuyen nghiep',
      'Bao cao hap nhan hang ngay',
      'An toan & giam sat 24/7'
    ],
    highlights: [
      { label: 'Tre em', value: '300+' },
      { label: 'Giao vien', value: '25' },
      { label: 'Nam kinh nghiem', value: '15' }
    ],
    tags: ['Mam non', 'Giao duc tre', 'Nuoi day', 'Phat trien'],
    fileSize: '229 KB',
    pages: 5,
    techStack: ['HTML5', 'CSS3', 'Vanilla JS']
  },
  {
    id: 'church',
    slug: 'church',
    name: 'Holy Light Parish',
    category: 'Giao Xu Cong Giao',
    tagline: 'Noi anh sang Chua soi vao long',
    description:
      'Landing page cho giao xu Cong giao. Lich than le, thong tin bi tich, hoat dong giao xu. Phu hop giao xu, giao phan, cong dong tin nguoi.',
    industry: 'CHURCH',
    accent: '#b91c1c',
    accentSecondary: '#fcd34d',
    bgGradient: 'linear-gradient(135deg, #450a0a 0%, #7f1d1d 50%, #b91c1c 100%)',
    icon: 'cross',
    features: [
      'Lich than le chi tiet',
      'Thong tin bi tich',
      'Hoat dong giao xu',
      'Doi ngu linh muc',
      'Lien he & ban do'
    ],
    highlights: [
      { label: 'Giao dan', value: '3,000+' },
      { label: 'Nam thanh lap', value: '1995' },
      { label: 'Linh muc', value: '2' }
    ],
    tags: ['Cong giao', 'Giao xu', 'Than le', 'Giao dan'],
    fileSize: '198 KB',
    pages: 4,
    techStack: ['HTML5', 'CSS3', 'Vanilla JS']
  }
]

export function getTemplateById(id: string): Template | undefined {
  return templates.find((t) => t.id === id || t.slug === id)
}