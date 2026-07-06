/**
 * Generate real HTML landing page previews for all 12 templates.
 * Outputs to cursor_framework_web/public/templates/{slug}/index.html
 */
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', 'cursor_framework_web', 'public', 'templates');

// ─── Template Data ──────────────────────────────────────────────────────────────
const TEMPLATES = [
  {
    id: 'crm', slug: 'crm', name: 'CRM Dashboard',
    tagline: 'Quản lý khách hàng thông minh', industry: 'CRM',
    accent: '#6366f1', accentSecondary: '#a78bfa',
    bgGradient: 'linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #4338ca 100%)',
    icon: 'users',
    features: ['Pipeline visualization với drag-drop', 'Contact segmentation thông minh', 'Email automation & templates', 'Real-time analytics dashboard'],
    highlights: [{ label: 'Conversion Rate', value: '+47%' }, { label: 'Customer Retention', value: '92%' }, { label: 'Avg Deal Size', value: '$8.4K' }],
    pages: 6, fileSize: '248 KB',
    techStack: ['HTML5', 'CSS3', 'Vanilla JS', 'Chart.js'],
    description: 'Landing page cho phần mềm CRM với dashboard trực quan.',
    bodyBg: '#0f0e30', cardBg: '#1a1a4e', textPrimary: '#f1f5f9', textSecondary: '#cbd5e1',
    nav: { logo: 'FlowCRM', links: ['Features', 'Pricing', 'Blog', 'Login'], cta: 'Start Free' },
    hero: { badge: 'New v3.0 — AI-powered segmentation', headline: 'Close more deals\nwith less effort', sub: 'Pipeline visualization, contact scoring, and automated follow-ups. Built for modern sales teams.' },
    stats: [{ value: '4,200+', label: 'Active Teams' }, { value: '$2.1B', label: 'Revenue Tracked' }, { value: '99.9%', label: 'Uptime SLA' }],
    testimonials: [{ name: 'Minh Tran', role: 'Head of Sales, TechVina', text: '"FlowCRM cut our sales cycle from 45 to 18 days. The pipeline view alone is worth it."' }],
    faqs: [
      { q: 'Does it integrate with Salesforce?', a: 'Yes — native two-way sync with Salesforce, HubSpot, Pipedrive, and 40+ more CRMs.' },
      { q: 'Is there a free trial?', a: '14-day free trial, no credit card required. Team plan starts at $29/seat/month.' },
    ],
  },
  {
    id: 'sale', slug: 'sale', name: 'Sale Pro',
    tagline: 'Trang bán hàng chuyển đổi cao', industry: 'E-Commerce',
    accent: '#f97316', accentSecondary: '#fbbf24',
    bgGradient: 'linear-gradient(135deg, #7c2d12 0%, #9a3412 50%, #c2410c 100%)',
    icon: 'cart',
    features: ['Hero với countdown timer', 'Product gallery + variants', 'Customer reviews carousel', 'Sticky checkout bar', 'Mobile-first responsive'],
    highlights: [{ label: 'Add-to-Cart Rate', value: '24%' }, { label: 'Avg Order Value', value: '$127' }, { label: 'Page Load', value: '0.8s' }],
    pages: 5, fileSize: '215 KB',
    techStack: ['HTML5', 'CSS3', 'Vanilla JS'],
    description: 'Landing page tối ưu conversion cho e-commerce, flash sale, product launch.',
    bodyBg: '#1c0a00', cardBg: '#2d1505', textPrimary: '#fff7ed', textSecondary: '#fed7aa',
    nav: { logo: 'SalePro', links: ['Products', 'About', 'Contact'], cta: 'Shop Now' },
    hero: { badge: 'Flash Sale — 48 Hours Only', headline: 'Premium headphones.\nIrresistible price.', sub: 'Active noise cancelling. 40h battery. Free shipping worldwide.' },
    stats: [{ value: '12,800', label: 'Units Sold' }, { value: '4.9★', label: 'Avg Rating' }, { value: 'Free', label: 'Worldwide Shipping' }],
    testimonials: [{ name: 'Lan Nguyen', role: 'Verified Buyer', text: '"Sound quality is incredible for the price. Arrived in 3 days to Hanoi."' }],
    faqs: [
      { q: 'What about warranty?', a: '24-month international warranty. Free replacement within 30 days.' },
      { q: 'Does it work with iPhone?', a: 'Yes — Bluetooth 5.3, works with iOS, Android, Windows, and macOS.' },
    ],
  },
  {
    id: 'bazi', slug: 'bazi', name: 'Bazi Tử Vi',
    tagline: 'Xem vận mệnh theo Tứ Trụ', industry: 'BAZI',
    accent: '#dc2626', accentSecondary: '#fbbf24',
    bgGradient: 'linear-gradient(135deg, #450a0a 0%, #7c2d12 50%, #991b1b 100%)',
    icon: 'yin-yang',
    features: ['Tứ Trụ interactive demo', 'Form nhập ngày giờ sinh', 'Luận giải can chi chi tiết', 'Bảng hợp màu, hợp hướng', 'Tích hợp thanh toán QR'],
    highlights: [{ label: 'Khách hàng tin tưởng', value: '15K+' }, { label: 'Đánh giá 5 sao', value: '4.9/5' }, { label: 'Thời gian giao', value: '24h' }],
    pages: 7, fileSize: '289 KB',
    techStack: ['HTML5', 'CSS3', 'Vanilla JS', 'SVG Animations'],
    description: 'Landing page huyền bí, uy tín cho dịch vụ xem Bazi, Tử Vi, phong thủy.',
    bodyBg: '#1a0505', cardBg: '#2d0a0a', textPrimary: '#fef2f2', textSecondary: '#fecaca',
    nav: { logo: 'Tử Vi Việt', links: ['Xem Bazi', 'Phong Thủy', 'Tử Vi', 'Đăng nhập'], cta: 'Xem Ngay' },
    hero: { badge: 'Cao nhân Tử Vi hàng đầu', headline: 'Giải mã vận mệnh\nqua Tứ Trụ', sub: 'Xem tử vi chính xác theo ngày giờ âm lịch. Luận giải về tài lộc, tình duyên, sự nghiệp.' },
    stats: [{ value: '15,000+', label: 'Lượt xem' }, { value: '4.9/5', label: 'Đánh giá' }, { value: '24h', label: 'Giao kết quả' }],
    testimonials: [{ name: 'Chị Hương', role: 'Khách hàng tại TP.HCM', text: '"Luận rất chính xác. Đã đặt thêm gói Tử Vi chi tiết cho cả gia đình."' }],
    faqs: [
      { q: 'Cần cung cấp thông tin gì?', a: 'Ngày, tháng, năm, giờ sinh (âm lịch). Càng chính xác giờ sinh, luận càng đúng.' },
      { q: 'Kết quả giao như thế nào?', a: 'PDF chi tiết gửi qua Zalo trong 24h. Có thể book lịch tư vấn 1-1 qua video call.' },
    ],
  },
  {
    id: 'numerology', slug: 'numerology', name: 'Numerology Life',
    tagline: 'Khám phá sức mạnh con số', industry: 'NUMEROLOGY',
    accent: '#06b6d4', accentSecondary: '#a855f7',
    bgGradient: 'linear-gradient(135deg, #0c0a4d 0%, #1e1b4b 50%, #312e81 100%)',
    icon: 'star',
    features: ['Calculator 6 chỉ số chính', 'Biểu đồ trực quan sinh động', 'Báo cáo PDF tự động', 'Personalized insights AI', 'Cosmic animations'],
    highlights: [{ label: 'Độ chính xác', value: '99.2%' }, { label: 'Reports/ngày', value: '500+' }, { label: 'Languages', value: '3' }],
    pages: 6, fileSize: '267 KB',
    techStack: ['HTML5', 'CSS3', 'Vanilla JS', 'Canvas API'],
    description: 'Landing page hiện đại, tối giản cho dịch vụ Thần Số Học Pythagoras.',
    bodyBg: '#080820', cardBg: '#12103d', textPrimary: '#f0f9ff', textSecondary: '#bae6fd',
    nav: { logo: 'Numera', links: ['Calculator', 'How it works', 'Stories', 'Login'], cta: 'Discover Now' },
    hero: { badge: 'Based on Pythagorean Numerology', headline: 'Your numbers\nhold the answers', sub: 'Calculate your Life Path, Expression, and Soul Urge numbers. Get a personalized cosmic report in 60 seconds.' },
    stats: [{ value: '99.2%', label: 'Accuracy Rate' }, { value: '3', label: 'Languages' }, { value: '500+', label: 'Daily Reports' }],
    testimonials: [{ name: 'Khanh Pham', role: 'Startup Founder', text: '"The Life Path reading was surprisingly accurate. It helped me understand why I kept gravitating toward certain careers."' }],
    faqs: [
      { q: 'How is this different from western numerology apps?', a: 'We use the Pythagorean method with an enhanced AI layer that cross-references your chart with 12,000+ historical patterns.' },
      { q: 'Is my birth data safe?', a: 'We never store your personal data. The report is generated and emailed, then discarded.' },
    ],
  },
  {
    id: 'blog', slug: 'blog', name: 'Blog Editorial',
    tagline: 'Trải nghiệm đọc tuyệt vời', industry: 'EDITORIAL',
    accent: '#10b981', accentSecondary: '#34d399',
    bgGradient: 'linear-gradient(135deg, #064e3b 0%, #065f46 50%, #047857 100%)',
    icon: 'book',
    features: ['Editorial typography (Serif + Sans)', 'Reading time + progress bar', 'Dark mode auto switch', 'Newsletter subscription widget', 'Related posts algorithm'],
    highlights: [{ label: 'Lighthouse Score', value: '100/100' }, { label: 'Avg Read Time', value: '6m 24s' }, { label: 'Bounce Rate', value: '12%' }],
    pages: 8, fileSize: '192 KB',
    techStack: ['HTML5', 'CSS3', 'Vanilla JS'],
    description: 'Template blog/magazine cao cấp với typography đẳng cấp, reading time, dark mode.',
    bodyBg: '#022c22', cardBg: '#064e3b', textPrimary: '#ecfdf5', textSecondary: '#a7f3d0',
    nav: { logo: 'BytePaper', links: ['Articles', 'Topics', 'Authors', 'Newsletter'], cta: 'Subscribe' },
    hero: { badge: 'Technology & Design', headline: 'Thinking in\npublic', sub: 'Deep dives on software architecture, UX design, and the craft of building products people love.' },
    stats: [{ value: '100/100', label: 'Lighthouse' }, { value: '50K+', label: 'Monthly Readers' }, { value: '3 posts/week', label: 'Publishing Cadence' }],
    testimonials: [{ name: 'Dat Le', role: 'Senior Engineer, FPT', text: '"Finally a dev blog that respects my time. Short, precise, zero fluff."' }],
    faqs: [
      { q: 'Do you accept guest posts?', a: 'Yes — we publish 2 guest posts per month. Pitch via the contact form with a 200-word outline.' },
      { q: 'Is there a newsletter?', a: 'Weekly digest every Monday. 3 curated articles + 1 tool recommendation. 50,000+ subscribers.' },
    ],
  },
  {
    id: 'portfolio', slug: 'portfolio', name: 'Portfolio Studio',
    tagline: 'Portfolio cho designer & dev', industry: 'PORTFOLIO',
    accent: '#ec4899', accentSecondary: '#f472b6',
    bgGradient: 'linear-gradient(135deg, #500724 0%, #831843 50%, #9d174d 100%)',
    icon: 'sparkles',
    features: ['Masonry project gallery', 'Case study templates', 'Skills visualization', 'Contact form với validation', 'Smooth scroll animations'],
    highlights: [{ label: 'Awwwards', value: 'Site of Day' }, { label: 'CSS Design Awards', value: 'Best UI' }, { label: 'Load Time', value: '< 1s' }],
    pages: 5, fileSize: '234 KB',
    techStack: ['HTML5', 'CSS3', 'Vanilla JS', 'GSAP'],
    description: 'Landing page portfolio tối giản, tinh tế cho designer, developer, photographer.',
    bodyBg: '#1f0a1a', cardBg: '#4a0d28', textPrimary: '#fdf4ff', textSecondary: '#f5d0fe',
    nav: { logo: 'Portfolio', links: ['Work', 'About', 'Process', 'Contact'], cta: 'Hire Me' },
    hero: { badge: 'Available for freelance', headline: 'Design that\nmoves people', sub: 'UI/UX designer and frontend developer crafting digital experiences that convert and delight.' },
    stats: [{ value: '50+', label: 'Projects' }, { value: '3', label: 'Awards' }, { value: '< 1s', label: 'Load Time' }],
    testimonials: [{ name: 'Agency Director', role: 'Creative Studio HCM', text: '"Trang transformed our online presence. The portfolio got us 3 enterprise clients in the first month."' }],
    faqs: [
      { q: 'What does a project cost?', a: 'Brand identity from $1,500. Website from $3,000. Complex apps quoted individually.' },
      { q: 'What is your process?', a: 'Discover → Wireframe → Design → Develop → Launch. 4-week average for a full website.' },
    ],
  },
  {
    id: 'food-delivery', slug: 'food-delivery', name: 'Lẩu Đêm',
    tagline: 'Đặt đồ ăn 30 phút, nóng hổi', industry: 'F&B',
    accent: '#ef4444', accentSecondary: '#fb923c',
    bgGradient: 'linear-gradient(135deg, #7c2d12 0%, #991b1b 50%, #b91c1c 100%)',
    icon: 'fork-knife',
    features: ['GPS tracking shipper realtime', 'Menu đa nhà hàng, filter theo món', 'Thanh toán MoMo, ZaloPay, tiền mặt', 'Đánh giá & review sau giao', 'Mã giảm giá & loyalty program'],
    highlights: [{ label: 'Đơn/ngày', value: '12K+' }, { label: 'Đúng giờ', value: '94%' }, { label: 'Nhà hàng', value: '2,400+' }],
    pages: 6, fileSize: '256 KB',
    techStack: ['HTML5', 'CSS3', 'Vanilla JS', 'Mapbox GL'],
    description: 'Landing page app giao đồ ăn tối Việt Nam. Tracking thời gian thực, đa nhà hàng.',
    bodyBg: '#1c0505', cardBg: '#2d0a0a', textPrimary: '#fff7ed', textSecondary: '#fed7aa',
    nav: { logo: 'Lẩu Đêm', links: ['Menu', 'Restaurants', 'About', 'Login'], cta: 'Order Now' },
    hero: { badge: 'Free delivery on first order', headline: 'Đặt lẩu nóng,\ngiao tận cửa', sub: '2,400+ nhà hàng. Giao trong 30 phút. Thanh toán MoMo, ZaloPay, hoặc tiền mặt.' },
    stats: [{ value: '12K+', label: 'Orders/Day' }, { value: '94%', label: 'On Time' }, { value: '2,400+', label: 'Restaurants' }],
    testimonials: [{ name: 'Thu Hà', role: 'Food Blogger, Hanoi', text: '"Đặt lẩu qua app lúc 11h đêm, giao 11:28. Nóng như vừa nấu xong."' }],
    faqs: [
      { q: 'Delivery time?', a: 'Average 28 minutes within 3km. Real-time GPS tracking from kitchen to your door.' },
      { q: 'Payment options?', a: 'MoMo, ZaloPay, Visa/Mastercard, or cash on delivery. No extra fees.' },
    ],
  },
  {
    id: 'edu-tutor', slug: 'edu-tutor', name: 'Gia Sư Việt',
    tagline: 'Gia sư 1-1, lộ trình cá nhân hoá', industry: 'EDUCATION',
    accent: '#3b82f6', accentSecondary: '#06b6d4',
    bgGradient: 'linear-gradient(135deg, #1e3a8a 0%, #1d4ed8 50%, #2563eb 100%)',
    icon: 'graduation-cap',
    features: ['Matching AI theo trình độ & mục tiêu', 'Lớp thử 30 phút miễn phí', 'Bảng điểm & báo cáo phụ huynh', 'Luyện tập tương tác, chấm tự động', 'Thanh toán theo buổi hoặc gói tháng'],
    highlights: [{ label: 'Gia sư', value: '4,800+' }, { label: 'Học sinh', value: '38K' }, { label: 'Đậu ĐH', value: '92%' }],
    pages: 7, fileSize: '273 KB',
    techStack: ['HTML5', 'CSS3', 'Vanilla JS', 'Chart.js'],
    description: 'Landing page nền tảng kết nối gia sư Việt Nam. Lộ trình học riêng cho từng học sinh.',
    bodyBg: '#0a1628', cardBg: '#1e3a6e', textPrimary: '#eff6ff', textSecondary: '#bfdbfe',
    nav: { logo: 'Gia Sư Việt', links: ['Tìm gia sư', 'Cách hoạt động', 'Giá', 'Đăng ký'], cta: 'Dùng thử' },
    hero: { badge: 'Hơn 4,800 gia sư đã kiểm chứng', headline: 'Con giỏi hơn\nmỗi ngày', sub: 'Gia sư 1-1 phù hợp từng trình độ. Lớp thử miễn phí 30 phút. Báo cáo phụ huynh hàng tuần.' },
    stats: [{ value: '4,800+', label: 'Gia Sư' }, { value: '38,000', label: 'Học Sinh' }, { value: '92%', label: 'Đậu ĐH' }],
    testimonials: [{ name: 'Chị Mai', role: 'Phụ huynh, Q.7 TP.HCM', text: '"Con từ 5.5 lên 8.5 sau 3 tháng. Gia sư dạy rất có hệ thống."' }],
    faqs: [
      { q: 'Gia sư có kiểm tra pháp lý?', a: 'Tất cả gia sư xác minh CMND, bằng cấp, và lý lịch. Chỉ nhận 1/3 hồ sơ đăng ký.' },
      { q: 'Học phí thế nào?', a: 'Thanh toán theo buổi (từ 120K/buổi) hoặc gói tháng tiết kiệm 20%. Không phí setup.' },
    ],
  },
  {
    id: 'beauty-spa', slug: 'beauty-spa', name: 'Sen Spa',
    tagline: 'Spa cao cấp, đặt lịch 60 giây', industry: 'BEAUTY',
    accent: '#ec4899', accentSecondary: '#a78bfa',
    bgGradient: 'linear-gradient(135deg, #4c1d95 0%, #6b21a8 50%, #831843 100%)',
    icon: 'flower-lotus',
    features: ['Booking realtime với calendar widget', 'Chọn therapist yêu thích', 'Gallery before/after (consent-based)', 'Gói membership & loyalty', 'Nhắc lịch tự động qua Zalo'],
    highlights: [{ label: 'Chi nhánh', value: '24' }, { label: 'Khách quay lại', value: '78%' }, { label: 'Đánh giá', value: '4.9★' }],
    pages: 5, fileSize: '241 KB',
    techStack: ['HTML5', 'CSS3', 'Vanilla JS'],
    description: 'Landing page cho spa & salon làm đẹp cao cấp. Đặt lịch trực tuyến, chọn therapist.',
    bodyBg: '#1a0a20', cardBg: '#3d0d38', textPrimary: '#fdf4ff', textSecondary: '#f5d0fe',
    nav: { logo: 'Sen Spa', links: ['Services', 'Gallery', 'Membership', 'Branches', 'Login'], cta: 'Book Now' },
    hero: { badge: '24 branches across Vietnam', headline: 'Relax. Renew.\nRejuvenate.', sub: 'Premium spa treatments with certified therapists. Book your appointment in 60 seconds.' },
    stats: [{ value: '24', label: 'Branches' }, { value: '78%', label: 'Return Rate' }, { value: '4.9★', label: 'Google Rating' }],
    testimonials: [{ name: 'Chị Loan', role: 'Regular Client, Q.3', text: '"Massage signature của Sen Spa là无可挑剔. Da mình cải thiện rõ rệt sau 8 sessions."' }],
    faqs: [
      { q: 'What treatments do you offer?', a: 'Swedish, deep tissue, hot stone, aromatherapy, facial treatments, body wraps. All using organic products.' },
      { q: 'Cancellation policy?', a: 'Free cancellation up to 4 hours before appointment. Late cancellations incur 50% charge.' },
    ],
  },
  {
    id: 'fitness', slug: 'fitness', name: 'GymZone',
    tagline: 'Tập luyện thông minh, kết quả thật', industry: 'FITNESS',
    accent: '#22c55e', accentSecondary: '#eab308',
    bgGradient: 'linear-gradient(135deg, #14532d 0%, #166534 50%, #15803d 100%)',
    icon: 'dumbbell',
    features: ['Class booking với waitlist tự động', 'Workout plan cá nhân hoá theo goal', 'Progress tracking: weight, reps, PR', 'Video call 1-1 với coach', 'Cộng đồng & thử thách hàng tuần'],
    highlights: [{ label: 'Hội viên', value: '18K+' }, { label: 'Lớp/tuần', value: '420' }, { label: 'Coach', value: '120' }],
    pages: 6, fileSize: '228 KB',
    techStack: ['HTML5', 'CSS3', 'Vanilla JS', 'GSAP'],
    description: 'Landing page cho phòng gym, yoga studio, boxing club. Đặt lớp realtime, theo dõi tiến độ.',
    bodyBg: '#0a1f0a', cardBg: '#1a3d1a', textPrimary: '#f0fdf4', textSecondary: '#bbf7d0',
    nav: { logo: 'GymZone', links: ['Classes', 'Coaches', 'Pricing', 'Community'], cta: 'Join Now' },
    hero: { badge: '120 certified coaches, 18,000 members', headline: 'Your transformation\nstarts here', sub: 'Personalized workout plans, certified coaches, and a community that keeps you accountable.' },
    stats: [{ value: '18K+', label: 'Members' }, { value: '420', label: 'Classes/Week' }, { value: '120', label: 'Coaches' }],
    testimonials: [{ name: 'Minh Duc', role: 'Lost 18kg in 6 months', text: '"GymZone coach giúp mình xây dựng kế hoạch tập phù hợp. Kết quả sau 6 tháng: -18kg, 6-pack đầu tiên."' }],
    faqs: [
      { q: 'Do I need to commit to a contract?', a: 'No — month-to-month membership available. No joining fee. Cancel anytime.' },
      { q: 'Is there a trial class?', a: 'Free first class for all new members. Book via the app or website.' },
    ],
  },
  {
    id: 'realestate', slug: 'realestate', name: 'Nhà Tốt',
    tagline: 'Mua bán & cho thuê BĐS minh bạch', industry: 'REAL ESTATE',
    accent: '#f59e0b', accentSecondary: '#10b981',
    bgGradient: 'linear-gradient(135deg, #78350f 0%, #92400e 50%, #b45309 100%)',
    icon: 'house',
    features: ['Bản đồ giá BĐS theo quận/huyện', 'Virtual tour 3D & ảnh 360°', 'AI matching theo ngân sách + nhu cầu', 'Đặt lịch xem nhà online', 'Pháp lý check tự động (sổ đỏ, quy hoạch)'],
    highlights: [{ label: 'Tin đăng', value: '124K' }, { label: 'Thành phố', value: '63' }, { label: 'Verified', value: '100%' }],
    pages: 7, fileSize: '298 KB',
    techStack: ['HTML5', 'CSS3', 'Vanilla JS', 'Mapbox GL'],
    description: 'Landing page nền tảng BĐS Việt Nam. Listingchi tiết, bản đồ giá, lịch xem nhà online.',
    bodyBg: '#1a0f00', cardBg: '#2d1a00', textPrimary: '#fffbeb', textSecondary: '#fde68a',
    nav: { logo: 'Nhà Tốt', links: ['Mua', 'Thuê', 'Dự án', 'Giá đất', 'Đăng tin'], cta: 'Tìm nhà' },
    hero: { badge: '124,000 verified listings', headline: 'Tìm nhà dễ hơn,\ntin tưởng hơn', sub: '124K tin đăng đã xác minh. Bản đồ giá theo quận. AI gợi ý theo ngân sách của bạn.' },
    stats: [{ value: '124K', label: 'Verified Listings' }, { value: '63', label: 'Cities' }, { value: '100%', label: 'Verified Properties' }],
    testimonials: [{ name: 'Anh Tùng', role: 'First-time buyer, Da Nang', text: '"Đặt lịch xem 3 căn trong 1 buổi. Nhà Tốt check pháp lý tự động, yên tâm đặt cọc."' }],
    faqs: [
      { q: 'Is the listing information verified?', a: 'Yes — every listing goes through document verification, physical inspection, and owner confirmation before publishing.' },
      { q: 'Does NhaTot charge buyers?', a: 'No — service is completely free for buyers. Sellers pay a small fee to post.' },
    ],
  },
  {
    id: 'travel', slug: 'travel', name: 'Viet Travel',
    tagline: 'Tour Đông Nam Á, đặt nhanh 2 phút', industry: 'TRAVEL',
    accent: '#06b6d4', accentSecondary: '#f59e0b',
    bgGradient: 'linear-gradient(135deg, #0c4a6e 0%, #075985 50%, #0369a1 100%)',
    icon: 'airplane-tilt',
    features: ['Itinerary từng ngày với map chi tiết', 'Review thật từ khách đã đi (có ảnh)', 'Thanh toán trả góp 0% qua thẻ tín dụng', 'So sánh giá 50+ hãng bay khác nhau', 'Hỗ trợ 24/7 qua Zalo & hotline'],
    highlights: [{ label: 'Tour/năm', value: '8,400+' }, { label: 'Điểm đến', value: '120' }, { label: 'Quay lại', value: '64%' }],
    pages: 6, fileSize: '262 KB',
    techStack: ['HTML5', 'CSS3', 'Vanilla JS', 'Mapbox GL'],
    description: 'Landing page công ty du lịch & tour Đông Nam Á. Itinerary chi tiết, review thật từ khách.',
    bodyBg: '#050f1a', cardBg: '#0c2840', textPrimary: '#f0f9ff', textSecondary: '#bae6fd',
    nav: { logo: 'VietTravel', links: ['Tours', 'Destinations', 'Reviews', 'About'], cta: 'Book Now' },
    hero: { badge: '120 destinations, 64% return rate', headline: 'Discover Vietnam.\nBeyond the guidebooks.', sub: 'Authentic tours designed by locals. Every itinerary verified by travelers who have been there.' },
    stats: [{ value: '8,400+', label: 'Tours/Year' }, { value: '120', label: 'Destinations' }, { value: '64%', label: 'Return Rate' }],
    testimonials: [{ name: 'Jennifer K.', role: 'Solo traveler, Australia', text: '"The Ha Long Bay overnight tour was magical. VietTravel thought of everything — even packed breakfast for the early morning kayak."' }],
    faqs: [
      { q: 'What is included in the tour price?', a: 'Accommodation, meals as listed, transport, guide, and all entrance fees. Flights and travel insurance are optional add-ons.' },
      { q: 'Can I customize an itinerary?', a: 'Yes — contact our team and we will build a custom itinerary for groups of 6 or more. Same pricing as published tours.' },
    ],
  },
];

// ─── HTML Generator ─────────────────────────────────────────────────────────────
function generateHTML(t) {
  const a = t.accent;
  const as = t.accentSecondary;

  return `<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>${t.name} — ${t.tagline}</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --accent: ${a};
      --accent2: ${as};
      --bg: ${t.bodyBg};
      --card: ${t.cardBg};
      --text: ${t.textPrimary};
      --text2: ${t.textSecondary};
    }

    html { font-size: 16px; scroll-behavior: smooth; }

    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.6;
      min-height: 100vh;
    }

    /* ── Nav ── */
    .nav {
      position: sticky; top: 0; z-index: 100;
      background: rgba(0,0,0,0.5);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border-bottom: 1px solid rgba(255,255,255,0.06);
      padding: 0 24px;
    }
    .nav-inner {
      max-width: 1100px; margin: 0 auto;
      display: flex; align-items: center; justify-content: space-between;
      height: 56px;
    }
    .nav-logo {
      font-size: 17px; font-weight: 700; letter-spacing: -0.02em;
      color: var(--text);
      text-decoration: none;
    }
    .nav-logo span { color: var(--accent); }
    .nav-links { display: flex; align-items: center; gap: 28px; list-style: none; }
    .nav-links a {
      color: var(--text2); font-size: 13.5px; font-weight: 500;
      text-decoration: none; transition: color 0.2s;
    }
    .nav-links a:hover { color: var(--text); }
    .nav-cta {
      background: var(--accent); color: #fff; font-size: 13px; font-weight: 600;
      padding: 8px 18px; border-radius: 8px; text-decoration: none;
      transition: opacity 0.2s, transform 0.2s;
    }
    .nav-cta:hover { opacity: 0.88; transform: translateY(-1px); }

    /* ── Hero ── */
    .hero {
      min-height: 520px;
      display: flex; align-items: center; justify-content: center;
      background: var(--bg);
      position: relative; overflow: hidden;
    }
    .hero::before {
      content: '';
      position: absolute; inset: 0;
      background: var(--bgGradient, ${t.bgGradient});
      opacity: 0.6;
    }
    .hero::after {
      content: '';
      position: absolute; inset: 0;
      background: radial-gradient(ellipse 80% 60% at 50% 40%, ${a}22 0%, transparent 70%);
    }
    .hero-inner {
      position: relative; z-index: 1;
      text-align: center; padding: 60px 24px;
      max-width: 700px;
    }
    .hero-badge {
      display: inline-block;
      background: ${a}22; border: 1px solid ${a}55;
      color: var(--accent); font-size: 11.5px; font-weight: 600;
      padding: 5px 14px; border-radius: 999px;
      letter-spacing: 0.05em; text-transform: uppercase;
      margin-bottom: 20px;
    }
    .hero-headline {
      font-size: clamp(36px, 6vw, 64px);
      font-weight: 800; line-height: 1.05; letter-spacing: -0.03em;
      margin-bottom: 18px; color: var(--text);
    }
    .hero-sub {
      font-size: 17px; color: var(--text2); max-width: 480px;
      margin: 0 auto 32px; line-height: 1.65;
    }
    .hero-actions { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; }
    .btn-primary {
      background: var(--accent); color: #fff;
      padding: 12px 28px; border-radius: 10px;
      font-size: 15px; font-weight: 600; text-decoration: none;
      transition: transform 0.2s, box-shadow 0.2s;
      box-shadow: 0 4px 20px ${a}44;
    }
    .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 8px 30px ${a}55; }
    .btn-secondary {
      background: rgba(255,255,255,0.08); color: var(--text);
      border: 1px solid rgba(255,255,255,0.12);
      padding: 12px 28px; border-radius: 10px;
      font-size: 15px; font-weight: 500; text-decoration: none;
      transition: background 0.2s;
    }
    .btn-secondary:hover { background: rgba(255,255,255,0.13); }

    /* ── Stats ── */
    .stats-bar {
      background: var(--card);
      border-top: 1px solid rgba(255,255,255,0.05);
      border-bottom: 1px solid rgba(255,255,255,0.05);
      padding: 24px;
    }
    .stats-inner {
      max-width: 700px; margin: 0 auto;
      display: grid; grid-template-columns: repeat(3, 1fr);
      gap: 16px; text-align: center;
    }
    .stat-value {
      font-size: 28px; font-weight: 800; letter-spacing: -0.03em;
      color: var(--accent); font-variant-numeric: tabular-nums;
    }
    .stat-label { font-size: 12px; color: var(--text2); margin-top: 2px; }

    /* ── Features ── */
    .section { max-width: 900px; margin: 0 auto; padding: 64px 24px; }
    .section-label {
      font-size: 11px; font-weight: 700; letter-spacing: 0.1em;
      text-transform: uppercase; color: var(--accent); margin-bottom: 12px;
    }
    .section-title {
      font-size: clamp(26px, 4vw, 38px); font-weight: 800;
      letter-spacing: -0.03em; margin-bottom: 8px; line-height: 1.15;
    }
    .section-sub { color: var(--text2); font-size: 16px; margin-bottom: 40px; }

    .features-grid {
      display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
      gap: 16px;
    }
    .feature-card {
      background: var(--card); border-radius: 12px; padding: 20px;
      border: 1px solid rgba(255,255,255,0.05);
    }
    .feature-icon {
      width: 36px; height: 36px; border-radius: 8px;
      background: ${a}22; display: flex; align-items: center; justify-content: center;
      margin-bottom: 12px; font-size: 16px;
    }
    .feature-title { font-size: 14px; font-weight: 600; margin-bottom: 6px; }
    .feature-desc { font-size: 12.5px; color: var(--text2); line-height: 1.55; }

    /* ── Testimonial ── */
    .testimonial {
      background: var(--card); border-radius: 16px; padding: 32px;
      border-left: 3px solid var(--accent);
      margin-bottom: 0;
    }
    .testimonial-text {
      font-size: 17px; line-height: 1.7; margin-bottom: 16px;
      font-style: italic; color: var(--text);
    }
    .testimonial-author { font-size: 13px; font-weight: 600; }
    .testimonial-role { color: var(--text2); font-size: 12px; margin-top: 2px; }

    /* ── FAQ ── */
    .faq-item {
      border-bottom: 1px solid rgba(255,255,255,0.05); padding: 18px 0;
    }
    .faq-q { font-size: 14px; font-weight: 600; margin-bottom: 6px; }
    .faq-a { font-size: 13px; color: var(--text2); line-height: 1.65; }

    /* ── CTA Banner ── */
    .cta-banner {
      background: var(--card);
      border-radius: 16px; padding: 48px 32px;
      text-align: center;
      background-image: radial-gradient(ellipse 60% 50% at 50% 100%, ${a}22 0%, transparent 70%);
    }
    .cta-banner h2 {
      font-size: clamp(22px, 4vw, 34px); font-weight: 800;
      letter-spacing: -0.03em; margin-bottom: 12px;
    }
    .cta-banner p { color: var(--text2); font-size: 15px; margin-bottom: 24px; }

    /* ── Footer ── */
    .footer {
      text-align: center; padding: 32px 24px;
      color: var(--text2); font-size: 12px;
      border-top: 1px solid rgba(255,255,255,0.04);
    }

    /* ── Responsive ── */
    @media (max-width: 600px) {
      .nav-links { display: none; }
      .hero-headline { font-size: 36px; }
      .stats-inner { grid-template-columns: repeat(3, 1fr); gap: 8px; }
      .stat-value { font-size: 20px; }
    }
  </style>
</head>
<body>

<!-- NAV -->
<nav class="nav">
  <div class="nav-inner">
    <a href="#" class="nav-logo">${t.nav.logo.replace(/([A-Z])/g, ' $1').trim()}<span>.</span></a>
    <ul class="nav-links">
      ${t.nav.links.map(l => `<li><a href="#">${l}</a></li>`).join('\n      ')}
    </ul>
    <a href="#" class="nav-cta">${t.nav.cta}</a>
  </div>
</nav>

<!-- HERO -->
<section class="hero">
  <div class="hero-inner">
    <span class="hero-badge">${t.hero.badge}</span>
    <h1 class="hero-headline">${t.hero.headline.split('\n').join('<br>')}</h1>
    <p class="hero-sub">${t.hero.sub}</p>
    <div class="hero-actions">
      <a href="#" class="btn-primary">Get Started Free</a>
      <a href="#" class="btn-secondary">View Demo</a>
    </div>
  </div>
</section>

<!-- STATS -->
<div class="stats-bar">
  <div class="stats-inner">
    ${t.stats.map(s => `
    <div>
      <div class="stat-value">${s.value}</div>
      <div class="stat-label">${s.label}</div>
    </div>`).join('')}
  </div>
</div>

<!-- FEATURES -->
<section class="section">
  <div class="section-label">Features</div>
  <h2 class="section-title">Everything you need.</h2>
  <p class="section-sub">Built for real workflows. No bloat.</p>
  <div class="features-grid">
    ${t.features.slice(0, 6).map((f, i) => `
    <div class="feature-card">
      <div class="feature-icon">✦</div>
      <div class="feature-title">${f.split(' với ')[0].split(' theo ')[0]}</div>
      <div class="feature-desc">${f}</div>
    </div>`).join('')}
  </div>
</section>

<!-- HIGHLIGHTS -->
<section class="section" style="padding-top:0;">
  <div class="section-label">By the numbers</div>
  <div class="features-grid">
    ${t.highlights.map(h => `
    <div class="feature-card" style="text-align:center;">
      <div class="stat-value" style="font-size:36px;margin-bottom:4px;">${h.value}</div>
      <div class="stat-label">${h.label}</div>
    </div>`).join('')}
  </div>
</section>

<!-- TESTIMONIAL -->
<section class="section" style="padding-top:0;">
  <div class="testimonial">
    <p class="testimonial-text">${t.testimonials[0].text}</p>
    <div class="testimonial-author">${t.testimonials[0].name}</div>
    <div class="testimonial-role">${t.testimonials[0].role}</div>
  </div>
</section>

<!-- FAQ -->
<section class="section" style="padding-top:0;">
  <div class="section-label">FAQ</div>
  <h2 class="section-title">Common questions.</h2>
  ${t.faqs.map(faq => `
  <div class="faq-item">
    <div class="faq-q">${faq.q}</div>
    <div class="faq-a">${faq.a}</div>
  </div>`).join('')}
</section>

<!-- CTA -->
<section class="section" style="padding-top:0;">
  <div class="cta-banner">
    <h2>Ready to get started?</h2>
    <p>Join thousands of users today. ${t.pages} pages · ${t.fileSize} · ${t.techStack.join(', ')}</p>
    <a href="#" class="btn-primary">Try ${t.name} Free</a>
  </div>
</section>

<!-- FOOTER -->
<footer class="footer">
  <div>${t.name} · ${t.industry} template · Part of Cursor Enterprise Framework</div>
</footer>

</body>
</html>`;
}

// ─── Generate All Files ────────────────────────────────────────────────────────
for (const t of TEMPLATES) {
  const dir = path.join(ROOT, t.slug);
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, 'index.html'), generateHTML(t), 'utf8');
  console.log(`✓ Generated: ${t.slug}/index.html`);
}

console.log(`\nAll ${TEMPLATES.length} templates generated in ${ROOT}`);
