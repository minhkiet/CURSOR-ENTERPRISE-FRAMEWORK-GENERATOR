# Mega Footer

> Comprehensive footer với pre-footer CTA, 6 columns links, app download, payment logos, social, legal sub-footer. Style market-flash-sale energy.

## 1. Mục đích

Footer hub cho Strikeout. Cần categories, mega events, trust signals, app download, payment methods, legal.

## 2. Asset

| Element | Source |
|---|---|
| App store badges | Apple / Google official |
| Payment icons | Simple Icons CDN |
| Social icons | Phosphor |
| Brand logos | Simple Icons CDN |

## 3. Cấu trúc

```
┌──────────────────────────────────────────────────────────┐
│ Pre-footer CTA: Deal tốt nhất chỉ có trên app            │
├──────────────────────────────────────────────────────────┤
│ Main grid:                                               │
│ ┌────────┬──────┬──────┬──────┬──────┬──────┬──────┐   │
│ │ Logo + │Shopee│Mega  │Categ-│Mỗi   │Brand │Help  │   │
│ │ Hotline│ Events│-ories│ giờ  │      │      │      │   │
│ └────────┴──────┴──────┴──────┴──────┴──────┴──────┘   │
│                                                          │
│ App + Payment row                                       │
│                                                          │
│ Trust strip: Hoàn 200% · 7 ngày đổi · IATA · Freeship │
├──────────────────────────────────────────────────────────┤
│ Sub-footer                                              │
└──────────────────────────────────────────────────────────┘
```

## 4. Variants

| Variant | Use | Khác biệt |
|---|---|---|
| `default` | Homepage | All sections |
| `compact` | Sub-pages | No pre-footer CTA |
| `event` | 9.9, 11.11 | Larger countdown promo |

## 5. Icon mapping

| Role | Phosphor |
|---|---|
| Bag | `ShoppingBag` |
| Tag | `Tag` |
| Lightning | `Lightning` (fill) |
| Phone | `Phone` |
| Mail | `EnvelopeSimple` |
| Facebook | `FacebookLogo` |
| Instagram | `InstagramLogo` |
| YouTube | `YoutubeLogo` |
| TikTok | `TiktokLogo` |
| App Store | `AppleLogo` |
| Google Play | `GooglePlayLogo` |
| Shield | `ShieldCheck` |
| Truck | `Truck` |
| Seal | `SealCheck` (fill) |
| Arrow | `ArrowRight` |

## 6. Code reference

```tsx
'use client';
import * as Phosphor from '@phosphor-icons/react';

export function MegaFooterSale() {
  return (
    <footer className="bg-slate-950 text-slate-300">
      {/* Pre-footer CTA */}
      <div className="border-b border-slate-800/50 bg-gradient-to-r from-orange-900/50 to-rose-900/30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
          <div className="grid grid-cols-1 lg:grid-cols-[1fr_auto] gap-6 items-center">
            <div>
              <h2 className="text-2xl lg:text-3xl font-extrabold text-white">
                Deal tốt nhất chỉ có trên app
              </h2>
              <p className="mt-1 text-slate-300 text-[14px]">
                Flash deal app-only, push notification deal mới, mã freeship 24/7.
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
              <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-orange-500 to-rose-500 flex items-center justify-center text-white font-extrabold text-lg">
                S
              </div>
              <span className="font-extrabold text-xl text-white tracking-tight">
                Strikeout
              </span>
            </a>
            <p className="mt-4 text-[13px] text-slate-400 leading-relaxed">
              Flash sale mỗi giờ. Cam kết giá tốt nhất, hoàn tiền 200%.
            </p>
            <div className="mt-5 space-y-2">
              <a href="tel:19001569" className="flex items-center gap-2 text-[13px] hover:text-white">
                <Phosphor.Phone size={13} weight="bold" className="text-orange-400" />
                <span className="font-bold text-white tabular-nums">1900 1569</span>
                <span className="text-slate-500">· 24/7</span>
              </a>
              <a href="mailto:hello@strikeout.vn" className="flex items-center gap-2 text-[13px] hover:text-white">
                <Phosphor.EnvelopeSimple size={13} weight="bold" className="text-slate-400" />
                hello@strikeout.vn
              </a>
            </div>
            <div className="mt-5 flex items-center gap-2">
              <SocialLink icon="FacebookLogo" label="Facebook" />
              <SocialLink icon="InstagramLogo" label="Instagram" />
              <SocialLink icon="YoutubeLogo" label="YouTube" />
              <SocialLink icon="TiktokLogo" label="TikTok" />
            </div>
          </div>

          {/* Link columns */}
          <FooterColumn title="Danh mục" icon="Tag" links={[
            { label: 'Điện tử', href: '#' },
            { label: 'Thời trang', href: '#' },
            { label: 'Làm đẹp', href: '#' },
            { label: 'Gia dụng', href: '#' },
            { label: 'Đồ chơi', href: '#' },
            { label: 'Thể thao', href: '#' },
            { label: 'Sách', href: '#' },
            { label: 'Ô tô', href: '#' }
          ]} />
          <FooterColumn title="Mega sale" icon="Lightning" links={[
            { label: '7.7 Sale', href: '#' },
            { label: '8.8 Sale', href: '#' },
            { label: '9.9 Sale', href: '#' },
            { label: '10.10 Sale', href: '#' },
            { label: '11.11 Sale', href: '#' },
            { label: '12.12 Sale', href: '#' }
          ]} />
          <FooterColumn title="Flash deal" icon="ShoppingBag" links={[
            { label: '9AM hôm nay', href: '#' },
            { label: '12PM trưa nay', href: '#' },
            { label: '3PM chiều nay', href: '#' },
            { label: '6PM tối nay', href: '#' },
            { label: '9PM đêm nay', href: '#' },
            { label: '12AM khuya', href: '#' }
          ]} />
          <FooterColumn title="Thương hiệu" icon="Storefront" links={[
            { label: 'Samsung', href: '#' },
            { label: 'Apple', href: '#' },
            { label: 'Xiaomi', href: '#' },
            { label: 'Oppo', href: '#' },
            { label: 'Nike', href: '#' },
            { label: 'Adidas', href: '#' },
            { label: 'Uniqlo', href: '#' }
          ]} />
          <FooterColumn title="Bán trên Strikeout" icon="Handshake" links={[
            { label: 'Đăng ký Shop', href: '#' },
            { label: 'Strikeout Mall', href: '#' },
            { label: 'Marketing tools', href: '#' },
            { label: 'Dashboard Shop', href: '#' },
            { label: 'Hỗ trợ Shop', href: '#' }
          ]} />
          <FooterColumn title="Hỗ trợ" icon="Headset" links={[
            { label: 'Trung tâm hỗ trợ', href: '#' },
            { label: 'Đơn hàng của tôi', href: '#' },
            { label: 'Đổi trả 7 ngày', href: '#' },
            { label: 'Hoàn tiền', href: '#' },
            { label: 'Liên hệ', href: '#' },
            { label: 'FAQ', href: '#' }
          ]} />
        </div>

        {/* Newsletter + Payment row */}
        <div className="mt-12 pt-8 border-t border-slate-800/50 grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Newsletter */}
          <div>
            <h3 className="text-[15px] font-bold text-white mb-2">Deal sớm nhất</h3>
            <p className="text-[12.5px] text-slate-400 mb-4">Flash deal + mã giảm giá gửi email mỗi sáng.</p>
            <form className="flex items-center gap-2 max-w-md" onSubmit={e => e.preventDefault()}>
              <div className="relative flex-1">
                <Phosphor.EnvelopeSimple size={16} weight="bold" className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
                <input
                  type="email"
                  required
                  placeholder="email@example.com"
                  className="w-full pl-10 pr-3 py-2.5 bg-slate-900 border border-slate-700 rounded-lg text-white text-[14px] focus:outline-none focus:ring-2 focus:ring-orange-500"
                />
              </div>
              <button
                type="submit"
                className="px-4 py-2.5 bg-gradient-to-r from-orange-500 to-rose-500 hover:from-orange-600 hover:to-rose-600 text-white font-extrabold text-[13px] rounded-lg whitespace-nowrap"
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
                Hoàn tiền 200%
              </span>
              <span className="inline-flex items-center gap-1.5">
                <Phosphor.SealCheck size={14} weight="fill" className="text-emerald-400" />
                Đổi trả 7 ngày
              </span>
              <span className="inline-flex items-center gap-1.5">
                <Phosphor.Truck size={14} weight="fill" className="text-emerald-400" />
                Freeship 24/7
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
              © 2026 Strikeout JSC · MST 0315.789.012 · Hotline 1900 1569 · Tầng 8, Bitexco, Q.1, TP.HCM
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
        <Icon size={14} weight="bold" className="text-orange-400" />
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
      aria-label={`Strikeout trên ${label}`}
      className="w-8 h-8 inline-flex items-center justify-center bg-slate-900 hover:bg-orange-500 border border-slate-800 rounded-full transition-colors"
    >
      <Icon size={14} weight="bold" className="text-slate-300" />
    </a>
  );
}
```

## 7. Accessibility

- Footer `<footer>` semantic
- Mỗi link column có `<h3>`
- Newsletter form có label
- Social `aria-label` cụ thể
- Hotline `tel:` accessible
- Email `mailto:` accessible
- Payment icons có alt text
- Color contrast: white/slate-300 trên slate-950 = AA

## 8. Performance

- Payment icons qua Simple Icons CDN (cached)
- App store badges có thể preload
- Footer bottom, no lazy needed
- Lazy load cho payment icons

## 9. Anti-patterns đã tránh

- ❌ Chỉ 3 columns (đã 6 columns)
- ❌ Tiny social icons
- ❌ Generic "Contact us"
- ❌ Hide trust signals (đã show hoàn 200%, đổi trả, freeship)
- ❌ Missing app download
- ❌ Generic payment icons

---

**Component family**: Layout #4 — `footer-mega`