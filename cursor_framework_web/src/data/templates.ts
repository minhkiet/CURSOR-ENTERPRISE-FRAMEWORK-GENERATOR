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
    category: 'Công Nghệ Máy Tính',
    tagline: 'Laptop, PC Gaming, linh kiện chính hãng',
    description:
      'Landing page cho cửa hàng công nghệ & máy tính. Laptop gaming, PC custom, linh kiện chính hãng, bảo hành 24 tháng, hỗ trợ trả góp 0% và giao hàng tốc hành.',
    industry: 'COMPUTER',
    accent: '#dc2626',
    accentSecondary: '#f59e0b',
    bgGradient: 'linear-gradient(135deg, #450a0a 0%, #7f1d1d 50%, #991b1b 100%)',
    icon: 'laptop',
    features: [
      'Bento grid laptop gaming & văn phòng',
      'Cấu hình PC build theo yêu cầu realtime',
      'Linh kiện phân phối chính hãng 100%',
      'Bảo hành 24 tháng tận nơi',
      'Trả góp 0% qua thẻ tín dụng'
    ],
    highlights: [
      { label: 'Sản phẩm', value: '2,000+' },
      { label: 'Thương hiệu', value: '50+' },
      { label: 'Trả góp', value: '0%' }
    ],
    tags: ['Laptop', 'Gaming PC', 'Linh kiện', 'Công nghệ'],
    fileSize: '264 KB',
    pages: 6,
    techStack: ['HTML5', 'CSS3', 'Vanilla JS']
  },
  {
    id: 'preschool',
    slug: 'preschool',
    name: 'Little Stars',
    category: 'Giáo Dục Mầm Non',
    tagline: 'Nuôi dạy trẻ trong tình yêu thương & sáng tạo',
    description:
      'Landing page cho trường mầm non chuẩn quốc tế. Phương pháp STEAM tiên tiến, cơ sở vật chất hiện đại, dinh dưỡng hữu cơ và báo cáo học tập số cho phụ huynh.',
    industry: 'EDUCATION',
    accent: '#f97316',
    accentSecondary: '#84cc16',
    bgGradient: 'linear-gradient(135deg, #7c2d12 0%, #9a3412 50%, #f97316 100%)',
    icon: 'baby',
    features: [
      'Chương trình học STEAM theo lứa tuổi',
      'Cơ sở vật chất chuẩn quốc tế',
      'Đội ngũ giáo viên bản ngữ & chuyên môn cao',
      'Báo cáo sinh hoạt & dinh dưỡng hàng ngày',
      'Camera an ninh giám sát 24/7'
    ],
    highlights: [
      { label: 'Học sinh', value: '300+' },
      { label: 'Giáo viên', value: '25' },
      { label: 'Năm kinh nghiệm', value: '15' }
    ],
    tags: ['Mầm non', 'STEAM', 'Giáo dục sớm', 'Trẻ em'],
    fileSize: '229 KB',
    pages: 5,
    techStack: ['HTML5', 'CSS3', 'Vanilla JS']
  },
  {
    id: 'church',
    slug: 'church',
    name: 'Thánh Quang Parish',
    category: 'Giáo Xứ & Tôn Giáo',
    tagline: 'Nơi ánh sáng Chúa soi rọi tâm hồn',
    description:
      'Landing page trang nghiêm, thanh thoát cho giáo xứ Công giáo. Tra cứu lịch Thánh lễ trực tuyến, hướng dẫn bí tích, tin tức cộng đoàn và suy niệm Lời Chúa mỗi ngày.',
    industry: 'CHURCH',
    accent: '#b91c1c',
    accentSecondary: '#fcd34d',
    bgGradient: 'linear-gradient(135deg, #450a0a 0%, #7f1d1d 50%, #b91c1c 100%)',
    icon: 'cross',
    features: [
      'Lịch Thánh lễ trong tuần & Chúa Nhật chi tiết',
      'Thủ tục chuẩn bị các Bí tích (Rửa tội, Hôn phối...)',
      'Tin tức hoạt động & hội đoàn giáo xứ',
      'Suy niệm Lời Chúa hàng ngày',
      'Thư viện hình ảnh & bản đồ chỉ đường'
    ],
    highlights: [
      { label: 'Giáo dân', value: '3,000+' },
      { label: 'Năm thành lập', value: '1995' },
      { label: 'Linh mục', value: '2' }
    ],
    tags: ['Công giáo', 'Giáo xứ', 'Thánh lễ', 'Tôn giáo'],
    fileSize: '198 KB',
    pages: 4,
    techStack: ['HTML5', 'CSS3', 'Vanilla JS']
  },
  {
    id: 'insurance',
    slug: 'insurance',
    name: 'Aegis Bảo An',
    category: 'Bảo Hiểm Toàn Diện',
    tagline: 'An tâm tương lai, vững bước hiện tại',
    description:
      'Landing page doanh nghiệp bảo hiểm chuẩn quốc tế. Đầy đủ các dòng sản phẩm: Sức khỏe CarePlus, Nhân thọ An Thịnh, Xe cơ giới AutoCare, Du lịch quốc tế GlobeSecure & Tài sản doanh nghiệp BizShield. Tích hợp công cụ tính phí trực tuyến, tra cứu 680+ bệnh viện bảo lãnh, đánh giá khách hàng & bồi thường e-Claim 24h.',
    industry: 'INSURANCE',
    accent: '#0284c7',
    accentSecondary: '#f59e0b',
    bgGradient: 'linear-gradient(135deg, #07192f 0%, #0c3366 50%, #0369a1 100%)',
    icon: 'shield-check',
    features: [
      'Công cụ ước tính phí bảo hiểm động theo độ tuổi & hạn mức',
      'Mạng lưới 680+ bệnh viện bảo lãnh viện phí trực tiếp',
      'Quy trình nộp hồ sơ e-Claim bồi thường trực tuyến 24h',
      'Bảng so sánh 3 gói quyền lợi chi tiết (Cơ bản/Vàng/Kim cương)',
      'Hệ thống thu thập yêu cầu tư vấn 1-1 chuyên sâu'
    ],
    highlights: [
      { label: 'Khách hàng tin chọn', value: '4.8M+' },
      { label: 'Chi trả bồi thường', value: '1.850 Tỷ' },
      { label: 'Bệnh viện liên kết', value: '680+' }
    ],
    tags: ['Bảo Hiểm', 'Sức Khỏe', 'Nhân Thọ', 'Ô Tô', 'E-Claim', 'Tài Chính'],
    fileSize: '312 KB',
    pages: 6,
    techStack: ['HTML5', 'CSS3', 'Vanilla JS', 'Phosphor Icons']
  },
  {
    id: 'auto-showroom',
    slug: 'auto-showroom',
    name: 'AutoPrime Motors',
    category: 'Showroom Ô Tô Đa Thương Hiệu',
    tagline: 'Sở hữu xe mơ ước — Trải nghiệm mua sắm 5 sao',
    description:
      'Siêu thị ô tô phân phối đa thương hiệu chính hãng & xe lướt chuẩn 176 hạng mục: Toyota, Mercedes-Benz, BMW, Porsche, Ford, Hyundai, VinFast. Tích hợp công cụ tính chi phí lăn bánh & trả góp ngân hàng lãi suất 6.8%, lái thử tại nhà, thu cũ đổi mới Trade-in và giao xe 24h tận nơi.',
    industry: 'AUTOMOTIVE',
    accent: '#f59e0b',
    accentSecondary: '#38bdf8',
    bgGradient: 'linear-gradient(135deg, #090d16 0%, #0f172a 50%, #1e293b 100%)',
    icon: 'car-profile',
    features: [
      'Bộ lọc tìm xe thông minh theo hãng, kiểu dáng, tầm giá và nhiên liệu',
      'Công cụ dự toán chi phí lăn bánh & bảng tính trả góp ngân hàng 85%',
      'Quy trình lái thử xe tận nhà (Home Test-Drive) miễn phí',
      'Hệ thống thu cũ đổi mới (Trade-In) định giá minh bạch trong 15 phút',
      'Chính sách bảo hành vàng 3 năm & cứu hộ khẩn cấp 24/7 toàn quốc'
    ],
    highlights: [
      { label: 'Xe đã giao', value: '5,800+' },
      { label: 'Hạng mục kiểm định', value: '176' },
      { label: 'Showroom toàn quốc', value: '5' }
    ],
    tags: ['Ô tô', 'Showroom', 'Xe lướt', 'Xe điện', 'Trả góp', 'Lái thử'],
    fileSize: '340 KB',
    pages: 6,
    techStack: ['HTML5', 'CSS3', 'Vanilla JS', 'Phosphor Icons']
  },
  {
    id: 'viet-restaurant',
    slug: 'viet-restaurant',
    name: 'Vị Xưa Quán',
    category: 'Nhà Hàng Ẩm Thực Truyền Thống Việt',
    tagline: 'Vị xưa tinh hoa — Trọn vẹn phong vị mâm cơm gia đình Việt',
    description:
      'Chuỗi nhà hàng ẩm thực di sản 3 miền Bắc - Trung - Nam đạt chứng nhận Michelin Selected. Chuyên cơm niêu cháy giòn 2 mặt, cá bống kho tộ, bún chả nướng than hoa, phở bát đá và bánh xèo miền Tây. Tích hợp hệ thống đặt bàn giữ chỗ đẹp, phòng VIP máy lạnh, E-Voucher giảm 15%-25% và chỉ dẫn đường tới 4 chi nhánh toàn quốc.',
    industry: 'RESTAURANT',
    accent: '#d97706',
    accentSecondary: '#16a34a',
    bgGradient: 'linear-gradient(135deg, #120b07 0%, #281910 50%, #451a03 100%)',
    icon: 'bowl-food',
    features: [
      'Thực đơn di sản 120+ món ăn truyền thống 3 miền Bắc - Trung - Nam',
      'Hệ thống đặt bàn trực tuyến chọn chi nhánh, phòng VIP & số lượng khách',
      'Bộ sưu tập E-Voucher giảm 15% - 25% kèm form nhận mã SMS/Zalo tức thì',
      'Không gian văn hóa nhà cổ Bắc Bộ, mộc mạc thư thái & âm nhạc truyền thống',
      'Bãi đỗ xe ô tô miễn phí có bảo vệ trông giữ tại tất cả 4 chi nhánh'
    ],
    highlights: [
      { label: 'Năm gia truyền', value: '38+' },
      { label: 'Món ăn di sản', value: '120+' },
      { label: 'Thực khách đánh giá', value: '4.9 ★' }
    ],
    tags: ['Nhà Hàng', 'Cơm Niêu', 'Ẩm Thực Việt', 'Michelin Selected', 'Voucher', 'Đặt Bàn'],
    fileSize: '325 KB',
    pages: 5,
    techStack: ['HTML5', 'CSS3', 'Vanilla JS', 'Phosphor Icons']
  }
]

export function getTemplateById(id: string): Template | undefined {
  return templates.find((t) => t.id === id || t.slug === id)
}