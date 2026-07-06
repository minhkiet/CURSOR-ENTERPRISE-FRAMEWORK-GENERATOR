# Mega Footer

> Footer đầy đủ cho CRM SaaS marketing landing: pre-footer CTA, 5 columns links, app download, payment logos, social media, legal + copyright. Hỗ trợ tiếng Việt + EN.

## 1. Mục đích

Visitor cần trust signals + quick links + contact. Footer là last chance để giữ người dùng ở lại.

## 2. Layout

```
┌────────────────────────────────────────────────────────────────────────┐
│  PRE-FOOTER CTA                                                        │
│  Sẵn sàng tăng revenue 47%? [Dùng thử 14 ngày →] [Xem demo →]         │
├────────────────────────────────────────────────────────────────────────┤
│  Logo Northwind   | Product  | Solutions  | Resources | Company  | Legal│
│  Mô tả ngắn     | Pipeline | IT Services| Blog      | Về chúng tôi| Privacy│
│  Hotline         | Contacts | Bất động   | Customer  | Tuyển dụng | Terms │
│  1900 6868      | Reports  | sản        | stories   | Press     | Cookie│
│  email@co       | Workflow | Marketing  | Docs      | Contact   | GDPR │
│                  | API      | Finance    | Webinars  | Partner  |       │
│                  | Pricing  | Edu        | Templates | Investors|      │
│                  |          | Healthcare | Case stud.│          │       │
├────────────────────────────────────────────────────────────────────────┤
│  Tải app: [App Store] [Google Play] | Thanh toán: Visa MC PayPal VietQR│
├────────────────────────────────────────────────────────────────────────┤
│  © 2026 Northwind CRM · Mã số doanh nghiệp 0123456789 · SOC2 Type II │
│  Mạng xã hội: FB · YT · LinkedIn · X                                  │
└────────────────────────────────────────────────────────────────────────┘
```

## 3. Code reference

```tsx
import * as Phosphor from '@phosphor-icons/react';

const COLUMNS = [
  {
    title: 'Sản phẩm',
    links: [
      { label: 'Pipeline bán hàng', href: '/product/pipeline' },
      { label: 'Quản lý liên hệ', href: '/product/contacts' },
      { label: 'Báo cáo doanh thu', href: '/product/reports' },
      { label: 'Workflow tự động', href: '/product/automation' },
      { label: 'API & Webhook', href: '/product/api' },
      { label: 'Bảng giá', href: '/pricing' },
      { label: 'Mobile app', href: '/mobile' }
    ]
  },
  {
    title: 'Giải pháp',
    links: [
      { label: 'IT Services', href: '/solutions/it-services' },
      { label: 'Bất động sản', href: '/solutions/real-estate' },
      { label: 'Marketing Agency', href: '/solutions/marketing' },
      { label: 'Tài chính', href: '/solutions/finance' },
      { label: 'Giáo dục', href: '/solutions/education' },
      { label: 'Y tế', href: '/solutions/healthcare' },
      { label: 'Sản xuất', href: '/solutions/manufacturing' }
    ]
  },
  {
    title: 'Tài nguyên',
    links: [
      { label: 'Blog', href: '/blog' },
      { label: 'Case studies', href: '/case-studies' },
      { label: 'Hướng dẫn', href: '/docs' },
      { label: 'Webinars', href: '/webinars' },
      { label: 'Templates', href: '/templates' },
      { label: 'API documentation', href: '/docs/api' },
      { label: 'Cộng đồng', href: '/community' }
    ]
  },
  {
    title: 'Công ty',
    links: [
      { label: 'Về chúng tôi', href: '/about' },
      { label: 'Tuyển dụng', href: '/careers' },
      { label: 'Báo chí', href: '/press' },
      { label: 'Đối tác', href: '/partners' },
      { label: 'Liên hệ sales', href: '/contact' },
      { label: 'Đầu tư', href: '/investors' },
      { label: 'Trạng thái dịch vụ', href: 'https://status.northwind.vn' }
    ]
  },
  {
    title: 'Pháp lý',
    links: [
      { label: 'Điều khoản dịch vụ', href: '/terms' },
      { label: 'Chính sách bảo mật', href: '/privacy' },
      { label: 'Cookie', href: '/cookies' },
      { label: 'GDPR', href: '/gdpr' },
      { label: 'Bảo mật', href: '/security' },
      { label: 'SOC2 report', href: '/soc2' },
      { label: 'DPA', href: '/dpa' }
    ]
  }
];

export function MegaFooter() {
  return (
    <footer className="bg-slate-950 text-slate-300">
      {/* Pre-footer CTA */}
      <div className="bg-gradient-to-r from-indigo-600 via-indigo-700 to-indigo-800 border-b border-indigo-500">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 lg:py-12">
          <div className="flex flex-wrap items-center justify-between gap-6">
            <div>
              <h2 className="text-2xl lg:text-3xl font-extrabold text-white tracking-tight">
                Sẵn sàng tăng revenue 47%?
              </h2>
              <p className="mt-1 text-indigo-100 text-[14px]">
                Dùng thử miễn phí 14 ngày · Không cần thẻ tín dụng · Setup trong 5 phút
              </p>
            </div>
            <div className="flex items-center gap-2">
              <a href="/signup" className="inline-flex items-center gap-1.5 px-5 py-3 bg-white hover:bg-indigo-50 text-indigo-700 text-[13.5px] font-bold rounded-lg">
                Dùng thử miễn phí
                <Phosphor.ArrowRight size={14} weight="bold" />
              </a>
              <a href="/demo" className="inline-flex items-center gap-1.5 px-5 py-3 bg-indigo-500/30 hover:bg-indigo-500/50 backdrop-blur text-white border border-white/30 text-[13.5px] font-bold rounded-lg">
                Xem demo
              </a>
            </div>
          </div>
        </div>
      </div>

      {/* Main footer */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 lg:py-16">
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-8 lg:gap-12">
          {/* Brand column */}
          <div className="col-span-2 md:col-span-3 lg:col-span-1">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-9 h-9 bg-gradient-to-br from-indigo-500 to-indigo-700 rounded-lg flex items-center justify-center">
                <Phosphor.Compass size={20} weight="fill" className="text-white" />
              </div>
              <span className="text-[18px] font-extrabold text-white">Northwind</span>
            </div>
            <p className="text-[12.5px] text-slate-400 leading-relaxed mb-4">
              CRM platform giúp sales rep Việt Nam chốt deal nhanh hơn 47%. Được tin dùng bởi 247+ doanh nghiệp.
            </p>
            <div className="space-y-1.5 text-[12.5px]">
              <a href="tel:19006868" className="flex items-center gap-1.5 hover:text-white">
                <Phosphor.Phone size={12} weight="bold" />
                Hotline: 1900 6868
              </a>
              <a href="mailto:sales@northwind.vn" className="flex items-center gap-1.5 hover:text-white">
                <Phosphor.EnvelopeSimple size={12} weight="bold" />
                sales@northwind.vn
              </a>
              <p className="flex items-center gap-1.5 text-slate-400">
                <Phosphor.MapPin size={12} weight="bold" />
                Tầng 12, Vincom Đồng Khởi, Quận 1, TP.HCM
              </p>
            </div>
          </div>

          {/* Link columns */}
          {COLUMNS.map(col => (
            <div key={col.title}>
              <h3 className="text-[12px] font-bold uppercase tracking-wider text-white mb-4">
                {col.title}
              </h3>
              <ul className="space-y-2">
                {col.links.map(link => (
                  <li key={link.label}>
                    <a href={link.href} className="text-[12.5px] text-slate-400 hover:text-white transition-colors">
                      {link.label}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* App download + payments */}
        <div className="mt-12 pt-8 border-t border-slate-800 flex flex-wrap items-center justify-between gap-6">
          <div>
            <p className="text-[11px] font-bold uppercase tracking-wider text-slate-500 mb-3">
              Tải ứng dụng
            </p>
            <div className="flex items-center gap-2">
              <a href="#" className="block h-10" aria-label="Tải trên App Store">
                <img src="https://developer.apple.com/assets/elements/badges/download-on-the-app-store.svg" alt="App Store" className="h-10" loading="lazy" />
              </a>
              <a href="#" className="block h-10" aria-label="Tải trên Google Play">
                <img src="https://upload.wikimedia.org/wikipedia/commons/7/78/Google_Play_Store_badge_EN.svg" alt="Google Play" className="h-10" loading="lazy" />
              </a>
            </div>
          </div>

          <div>
            <p className="text-[11px] font-bold uppercase tracking-wider text-slate-500 mb-3">
              Thanh toán
            </p>
            <div className="flex items-center gap-2">
              {['visa', 'mastercard', 'amex', 'paypal', 'applepay'].map(p => (
                <img
                  key={p}
                  src={`https://cdn.simpleicons.org/${p}/cbd5e1`}
                  alt={p}
                  className="h-6 w-auto opacity-70"
                  loading="lazy"
                />
              ))}
            </div>
          </div>

          <div>
            <p className="text-[11px] font-bold uppercase tracking-wider text-slate-500 mb-3">
              Mạng xã hội
            </p>
            <div className="flex items-center gap-2">
              {[
                { icon: 'FacebookLogo', label: 'Facebook' },
                { icon: 'YoutubeLogo', label: 'YouTube' },
                { icon: 'LinkedinLogo', label: 'LinkedIn' },
                { icon: 'XLogo', label: 'X (Twitter)' }
              ].map(s => {
                const Icon = Phosphor[s.icon] as any;
                return (
                  <a key={s.label} href="#" aria-label={s.label} className="w-9 h-9 inline-flex items-center justify-center bg-slate-800 hover:bg-indigo-600 rounded-lg transition-colors">
                    <Icon size={16} weight="bold" />
                  </a>
                );
              })}
            </div>
          </div>
        </div>

        {/* Bottom legal */}
        <div className="mt-8 pt-6 border-t border-slate-800 flex flex-wrap items-center justify-between gap-3 text-[11.5px] text-slate-500">
          <p>
            © 2026 Northwind CRM Vietnam. Mã số doanh nghiệp: <strong className="text-slate-400">0123456789</strong> cấp tại TP.HCM. Tầng 12, Vincom Đồng Khởi.
          </p>
          <div className="flex items-center gap-4">
            <span className="inline-flex items-center gap-1.5">
              <Phosphor.ShieldCheck size={12} weight="fill" className="text-emerald-500" />
              SOC 2 Type II
            </span>
            <span className="inline-flex items-center gap-1.5">
              <Phosphor.Lock size={12} weight="fill" className="text-emerald-500" />
              ISO 27001
            </span>
            <span className="inline-flex items-center gap-1.5">
              <Phosphor.Globe size={12} weight="fill" className="text-emerald-500" />
              GDPR Compliant
            </span>
            <span>Tiếng Việt ↓</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
```

## 4. Accessibility

- `<footer>` semantic
- Pre-footer CTA có heading + actions
- Link columns với `<h3>` + `<ul>` semantic
- Hotline `tel:` link accessible
- Email `mailto:` link accessible
- Social `aria-label` cụ thể
- App Store / Google Play badges có alt text
- Trust signals có icons + labels
- Reduce-motion: hover transitions off

## 5. Performance

- App store badges lazy load
- Simple Icons CDN cached
- No auto-play video
- Inline SVG icons (Phosphor)
- Static content

## 6. Anti-patterns đã tránh

- ❌ 3-column only footer (đã 6 cols + brand)
- ❌ No app download (đã có)
- ❌ No payment trust (đã có)
- ❌ No security badges (đã SOC2 + ISO + GDPR)
- ❌ Social icons no label (đã aria-label)
- ❌ Generic hotline (đã 1900 6868 format VN)

---

**Component family**: Marketing Landing — `footer-mega`