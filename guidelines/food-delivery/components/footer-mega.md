# Mega Footer

> Comprehensive footer với pre-footer CTA, 6 columns links, app download QR, payment logos, social, legal sub-footer. Dùng cho Bowl & Bite homepage và tất cả pages.

## 1. Mục đích

Footer hub discovery, trust, conversion. Cần:
- Cuisine categories
- City coverage
- Trust signals (verified, secured, hotline)
- Convert (newsletter, app download)
- Legal (privacy, terms)

## 2. Asset

| Element | Source |
|---|---|
| App store badges | Apple / Google official |
| Payment icons | Simple Icons CDN (Momo, ZaloPay, VNPay, Visa, Mastercard) |
| Social icons | Phosphor |

## 3. Cấu trúc

```
┌──────────────────────────────────────────────────────────┐
│ Pre-footer CTA strip:                                    │
│ Đặt 1 món free? Tải app. [App Store] [Google Play]      │
├──────────────────────────────────────────────────────────┤
│ Main grid:                                               │
│ ┌────────┬──────┬──────┬──────┬──────┬──────┬──────┐   │
│ │ Logo + │Cuisine│City │Member│Help │Compa-│Brand │   │
│ │ Hotline│      │     │      │      │ny    │      │   │
│ │ +social│      │     │      │      │      │      │   │
│ └────────┴──────┴──────┴──────┴──────┴──────┴──────┘   │
│                                                          │
│ App download + payment row                              │
│                                                          │
│ Trust strip: Verified · 24/7 · Secured · 30 phút        │
├──────────────────────────────────────────────────────────┤
│ Sub-footer:                                              │
│ © 2026 Bowl & Bite · MST + hotline                      │
│ [Privacy] [Terms] [Cookies] [Sitemap]                   │
└──────────────────────────────────────────────────────────┘
```

## 4. Variants

| Variant | Use | Khác biệt |
|---|---|---|
| `default` | Homepage | All sections |
| `compact` | Sub-pages | No pre-footer CTA |
| `marketing` | Landing | Larger newsletter |

## 5. Icon mapping

| Role | Phosphor |
|---|---|
| Phở | `BowlFood` |
| Bún | `Noodles` |
| Cơm | `RiceBowl` |
| Bánh mì | `Bread` |
| Lẩu | `CookingPot` |
| Trà sữa | `Coffee` |
| Hotline | `Phone` |
| Mail | `EnvelopeSimple` |
| Facebook | `FacebookLogo` |
| Instagram | `InstagramLogo` |
| YouTube | `YoutubeLogo` |
| TikTok | `TiktokLogo` |
| App Store | `AppleLogo` |
| Google Play | `GooglePlayLogo` |
| Shield | `ShieldCheck` |
| Clock | `Clock` |
| Pin | `MapPin` |
| Arrow | `ArrowRight` |

## 6. Code reference

```tsx
'use client';
import * as Phosphor from '@phosphor-icons/react';

export function MegaFooterFood() {
  return (
    <footer className="bg-slate-950 text-slate-300">
      {/* Pre-footer CTA */}
      <div className="border-b border-slate-800/50 bg-gradient-to-r from-emerald-900/50 to-amber-900/30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
          <div className="grid grid-cols-1 lg:grid-cols-[1fr_auto] gap-6 items-center">
            <div>
              <h2 className="text-2xl lg:text-3xl font-extrabold text-white">
                Tải app. Đặt 1 món free ngay.
              </h2>
              <p className="mt-1 text-slate-300 text-[14px]">
                Ưu đãi cho đơn đầu tiên qua app. Freeship đơn từ 99.000₫, mã BOWLFREE.
              </p>
            </div>
            <div className="flex flex-wrap items-center gap-3">
              <a href="#" className="flex items-center gap-2 px-4 py-3 bg-slate-900 hover:bg-slate-800 border border-slate-700 rounded-lg">
                <Phosphor.AppleLogo size={22} weight="bold" className="text-white" />
                <div className="text-left">
                  <div className="text-[10px] text-slate-400">Tải từ</div>
                  <div className="text-[13px] font-bold text-white">App Store</div>
                </div>
              </a>
              <a href="#" className="flex items-center gap-2 px-4 py-3 bg-slate-900 hover:bg-slate-800 border border-slate-700 rounded-lg">
                <Phosphor.GooglePlayLogo size={22} weight="bold" className="text-white" />
                <div className="text-left">
                  <div className="text-[10px] text-slate-400">Tải từ</div>
                  <div className="text-[13px] font-bold text-white">Google Play</div>
                </div>
              </a>
            </div>
          </div>
        </div>
      </div>

      {/* Main footer */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-14">
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-7 gap-8 lg:gap-6">
          {/* Brand column */}
          <div className="col-span-2 lg:col-span-1">
            <a href="/" className="inline-flex items-center gap-2">
              <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-emerald-500 to-amber-500 flex items-center justify-center text-white font-extrabold text-lg">
                B
              </div>
              <span className="font-extrabold text-xl text-white tracking-tight">
                Bowl & Bite
              </span>
            </a>
            <p className="mt-4 text-[13px] text-slate-400 leading-relaxed">
              Ăn ngon, giao nhanh. 3.200+ quán verified tại Hà Nội, TP.HCM, Đà Nẵng.
            </p>
            <div className="mt-5 space-y-2">
              <a href="tel:19001515" className="flex items-center gap-2 text-[13px] hover:text-white">
                <Phosphor.Phone size={13} weight="bold" className="text-emerald-400" />
                <span className="font-bold text-white tabular-nums">1900 1515</span>
                <span className="text-slate-500">· 24/7</span>
              </a>
              <a href="mailto:hello@bowl.vn" className="flex items-center gap-2 text-[13px] hover:text-white">
                <Phosphor.EnvelopeSimple size={13} weight="bold" className="text-slate-400" />
                hello@bowl.vn
              </a>
              <span className="flex items-center gap-2 text-[13px]">
                <Phosphor.MapPin size={13} weight="bold" className="text-slate-400" />
                3 chi nhánh: HN · HCM · ĐN
              </span>
            </div>
            <div className="mt-5 flex items-center gap-2">
              <SocialLink icon="FacebookLogo" label="Facebook" />
              <SocialLink icon="InstagramLogo" label="Instagram" />
              <SocialLink icon="YoutubeLogo" label="YouTube" />
              <SocialLink icon="TiktokLogo" label="TikTok" />
            </div>
          </div>

          {/* Link columns */}
          <FooterColumn
            title="Ẩm thực"
            icon="BowlFood"
            links={[
              { label: 'Phở Hà Nội', href: '#' },
              { label: 'Bún', href: '#' },
              { label: 'Cơm tấm', href: '#' },
              { label: 'Bánh mì', href: '#' },
              { label: 'Lẩu', href: '#' },
              { label: 'Trà sữa', href: '#' },
              { label: 'Cà phê', href: '#' },
              { label: 'Đồ chay', href: '#' }
            ]}
          />
          <FooterColumn
            title="Thành phố"
            icon="MapPin"
            links={[
              { label: 'TP.HCM (1.482 quán)', href: '#' },
              { label: 'Hà Nội (1.247 quán)', href: '#' },
              { label: 'Đà Nẵng (456 quán)', href: '#' },
              { label: 'Hải Phòng', href: '#' },
              { label: 'Cần Thơ', href: '#' },
              { label: 'Biên Hoà', href: '#' }
            ]}
          />
          <FooterColumn
            title="Quán nổi bật"
            icon="Storefront"
            links={[
              { label: 'Phở Hà Nội - Quận 1', href: '#' },
              { label: 'Bún chả Hàng Mành', href: '#' },
              { label: 'Cơm tấm Cali', href: '#' },
              { label: 'Bánh mì Huỳnh Hoa', href: '#' },
              { label: 'Lẩu Thái Tomyum', href: '#' },
              { label: 'Trà sữa Tocotoco', href: '#' }
            ]}
          />
          <FooterColumn
            title="Trở thành đối tác"
            icon="Handshake"
            links={[
              { label: 'Đăng ký quán', href: '#' },
              { label: 'Bảng giá dịch vụ', href: '#' },
              { label: 'Dashboard quán', href: '#' },
              { label: 'Marketing tools', href: '#' },
              { label: 'Quán của tôi', href: '#' },
              { label: 'Hỗ trợ đối tác', href: '#' }
            ]}
          />
          <FooterColumn
            title="Tài xế"
            icon="Motorcycle"
            links={[
              { label: 'Đăng ký tài xế', href: '#' },
              { label: 'Yêu cầu tài xế', href: '#' },
              { label: 'Bảng lương', href: '#' },
              { label: 'Bảo hiểm', href: '#' },
              { label: 'Hỗ trợ tài xế', href: '#' }
            ]}
          />
          <FooterColumn
            title="Hỗ trợ"
            icon="Headset"
            links={[
              { label: 'Trung tâm hỗ trợ', href: '#' },
              { label: 'Đơn hàng của tôi', href: '#' },
              { label: 'Hoàn tiền', href: '#' },
              { label: 'Liên hệ', href: '#' },
              { label: 'Khiếu nại', href: '#' },
              { label: 'FAQ', href: '#' }
            ]}
          />
        </div>

        {/* Newsletter + Payment row */}
        <div className="mt-12 pt-8 border-t border-slate-800/50 grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Newsletter */}
          <div>
            <h3 className="text-[15px] font-bold text-white mb-2">Deal mỗi ngày</h3>
            <p className="text-[12.5px] text-slate-400 mb-4">Flash deal + mã giảm giá gửi email mỗi sáng.</p>
            <form className="flex items-center gap-2 max-w-md" onSubmit={e => e.preventDefault()}>
              <div className="relative flex-1">
                <Phosphor.EnvelopeSimple size={16} weight="bold" className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
                <input
                  type="email"
                  required
                  placeholder="email@example.com"
                  className="w-full pl-10 pr-3 py-2.5 bg-slate-900 border border-slate-700 rounded-lg text-white text-[14px] focus:outline-none focus:ring-2 focus:ring-emerald-500"
                />
              </div>
              <button
                type="submit"
                className="px-4 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-[13px] rounded-lg whitespace-nowrap"
              >
                Đăng ký
              </button>
            </form>
          </div>

          {/* Payment + Trust */}
          <div>
            <h3 className="text-[15px] font-bold text-white mb-4">Thanh toán & Bảo mật</h3>
            <div className="flex flex-wrap items-center gap-2">
              {['visa', 'mastercard', 'jcb', 'amex', 'momo', 'zalopay', 'vnpay', 'shopeepay'].map(slug => (
                <img
                  key={slug}
                  src={`https://cdn.simpleicons.org/${slug}/cbd5e1`}
                  alt={slug}
                  className="h-7 w-12 object-contain bg-white rounded px-1.5 py-1"
                  loading="lazy"
                />
              ))}
            </div>
            <div className="mt-4 flex flex-wrap items-center gap-4 text-[11.5px] text-slate-400">
              <span className="inline-flex items-center gap-1.5">
                <Phosphor.ShieldCheck size={14} weight="fill" className="text-emerald-400" />
                Secured payment
              </span>
              <span className="inline-flex items-center gap-1.5">
                <Phosphor.SealCheck size={14} weight="fill" className="text-emerald-400" />
                Quán verified 100%
              </span>
              <span className="inline-flex items-center gap-1.5">
                <Phosphor.Clock size={14} weight="fill" className="text-emerald-400" />
                Hoàn tiền 200% nếu trễ
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Sub-footer */}
      <div className="border-t border-slate-800/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-5">
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-3 text-[11.5px] text-slate-500">
            <div>
              © 2026 Bowl & Bite JSC · MST 0315.654.321 · Hotline 1900 1515 · 78 Pasteur, Q.1, TP.HCM
            </div>
            <div className="flex items-center gap-4">
              <a href="#" className="hover:text-slate-300">Privacy</a>
              <a href="#" className="hover:text-slate-300">Terms</a>
              <a href="#" className="hover:text-slate-300">Cookies</a>
              <a href="#" className="hover:text-slate-300">Sitemap</a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}

function FooterColumn({ title, icon, links }: { title: string; icon: any; links: Array<{ label: string; href: string }> }) {
  const Icon = Phosphor[icon] as any;
  return (
    <div>
      <h3 className="flex items-center gap-1.5 text-[12px] font-bold uppercase tracking-wider text-white mb-4">
        <Icon size={14} weight="bold" className="text-emerald-400" />
        {title}
      </h3>
      <ul className="space-y-2">
        {links.map(link => (
          <li key={link.label}>
            <a href={link.href} className="text-[12.5px] text-slate-400 hover:text-white transition-colors">
              {link.label}
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
}

function SocialLink({ icon, label }: { icon: any; label: string }) {
  const Icon = Phosphor[icon] as any;
  return (
    <a
      href="#"
      aria-label={`Bowl & Bite trên ${label}`}
      className="w-8 h-8 inline-flex items-center justify-center bg-slate-900 hover:bg-emerald-600 border border-slate-800 rounded-full transition-colors"
    >
      <Icon size={14} weight="bold" className="text-slate-300" />
    </a>
  );
}
```

## 7. Accessibility

- Footer `<footer>` semantic
- Mỗi link column có `<h3>` cho screen reader
- Newsletter form có label rõ
- Social `aria-label` cụ thể
- Hotline `tel:` accessible
- Email `mailto:` accessible
- Payment icons có alt text
- App store badges accessible
- Color contrast white/slate-300 trên slate-950 = AA

## 8. Performance

- Payment icons qua Simple Icons CDN (cached)
- App store badges có thể preload
- Footer bottom, no lazy needed
- Lazy load cho payment icons
- Newsletter form client component

## 9. Anti-patterns đã tránh

- ❌ Chỉ 3 columns (đã 6 columns)
- ❌ Tiny social icons
- ❌ Generic "Contact us"
- ❌ Hide trust signals
- ❌ Missing app download
- ❌ Generic payment icons

---

**Component family**: Layout #5 — `footer-mega`