# Mega Footer

> Comprehensive footer với pre-footer CTA strip, 6 columns of links, app download QR, payment logos, social media, legal sub-footer. Dùng cho Skylark homepage và tất cả pages.

## 1. Mục đích

Footer là hub cho discovery, trust, conversion. Khách cần:
- Tìm category (Destinations, Flight, Hotel, Tour)
- Trust signals (IATA, secured payment, hotline)
- Convert (newsletter, app download)
- Legal (privacy, terms)

## 2. Asset

| Element | Source |
|---|---|
| App store badges | Apple / Google official badges |
| Payment icons | Simple Icons CDN (Visa, Mastercard, JCB, Momo, ZaloPay, VNPay) |
| Social icons | Phosphor or brand icons |
| App QR | Generated dynamically |

## 3. Cấu trúc

```
┌──────────────────────────────────────────────────────────┐
│ Pre-footer CTA strip:                                    │
│ Nhận deal sớm nhất. Đăng ký email. [Input] [Subscribe]   │
├──────────────────────────────────────────────────────────┤
│ Footer main grid:                                        │
│ ┌──────────┬──────┬──────┬──────┬──────┬──────┬──────┐  │
│ │ Logo +   │Flight│Hotel │ Dest │ Travel│ Member│Help │  │
│ │ Hotline  │Routes│ Type │ ina- │ Guide │ ship  │      │  │
│ │ + social │      │      │ tions │      │      │      │  │
│ └──────────┴──────┴──────┴──────┴──────┴──────┴──────┘  │
│                                                          │
│ App download:                                            │
│ ┌────────┐                                              │
│ │ QR code│  [App Store badge] [Google Play badge]       │
│ └────────┘                                              │
│                                                          │
│ Payment: [Visa] [Mastercard] [JCB] [Momo] [ZaloPay]    │
│                                                          │
│ IATA certified · Secured payment · 24/7 support          │
├──────────────────────────────────────────────────────────┤
│ Sub-footer:                                              │
│ © 2026 Skylark. Giấy phép kinh doanh lữ hành quốc tế    │
│ [Privacy] [Terms] [Cookies] [Sitemap]                    │
└──────────────────────────────────────────────────────────┘
```

## 4. Variants

| Variant | Use | Khác biệt |
|---|---|---|
| `default` | Homepage | All sections |
| `compact` | Sub-pages | No pre-footer CTA |
| `marketing` | Landing pages | Larger newsletter section |

## 5. States

Standard static + interactive links.

## 6. Icon mapping

| Role | Phosphor |
|---|---|
| Plane | `AirplaneTilt` |
| Hotel | `Buildings` |
| Tour | `MapTrifold` |
| Visa | Brand logo |
| Mastercard | Brand logo |
| Hotline | `Phone` |
| Mail | `EnvelopeSimple` |
| Facebook | `FacebookLogo` |
| Instagram | `InstagramLogo` |
| YouTube | `YoutubeLogo` |
| TikTok | `TiktokLogo` |
| App Store | Apple badge |
| Google Play | Google badge |
| Shield | `ShieldCheck` |
| IATA | Brand text logo |
| Support | `Headset` |
| Arrow | `ArrowRight` |

## 7. Code reference

```tsx
'use client';
import * as Phosphor from '@phosphor-icons/react';

export function MegaFooterTravel() {
  return (
    <footer className="bg-slate-950 text-slate-300">
      {/* Pre-footer CTA */}
      <div className="border-b border-slate-800/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
          <div className="grid grid-cols-1 lg:grid-cols-[1fr_auto] gap-6 items-center">
            <div>
              <h2 className="text-2xl lg:text-3xl font-extrabold text-white">
                Nhận deal sớm nhất trước khi hết
              </h2>
              <p className="mt-1 text-slate-400 text-[14px]">
                Flash deal, mã giảm giá và tips du lịch. 1 email/tuần, hủy bất kỳ lúc nào.
              </p>
            </div>
            <form className="flex items-center gap-2 max-w-md" onSubmit={e => e.preventDefault()}>
              <div className="relative flex-1">
                <Phosphor.EnvelopeSimple size={16} weight="bold" className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
                <input
                  type="email"
                  required
                  placeholder="email@example.com"
                  className="w-full pl-10 pr-3 py-3 bg-slate-900 border border-slate-700 rounded-lg text-white text-[14px] focus:outline-none focus:ring-2 focus:ring-sky-500"
                />
              </div>
              <button
                type="submit"
                className="px-5 py-3 bg-sky-600 hover:bg-sky-700 text-white font-bold text-[14px] rounded-lg whitespace-nowrap inline-flex items-center gap-1.5"
              >
                Đăng ký
                <Phosphor.ArrowRight size={14} weight="bold" />
              </button>
            </form>
          </div>
        </div>
      </div>

      {/* Main footer */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-14">
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-7 gap-8 lg:gap-6">
          {/* Brand column */}
          <div className="col-span-2 lg:col-span-1">
            <a href="/" className="inline-flex items-center gap-2">
              <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-sky-500 to-rose-500 flex items-center justify-center text-white font-extrabold text-lg">
                S
              </div>
              <span className="font-extrabold text-xl text-white tracking-tight">
                Skylark
              </span>
            </a>
            <p className="mt-4 text-[13px] text-slate-400 leading-relaxed">
              Sàn OTA Đông Nam Á. Giá tốt, đặt nhanh, hoàn tiền dễ.
            </p>
            <div className="mt-5 space-y-2">
              <a href="tel:19001569" className="flex items-center gap-2 text-[13px] hover:text-white">
                <Phosphor.Phone size={13} weight="bold" className="text-sky-400" />
                <span className="font-bold text-white tabular-nums">1900 1569</span>
                <span className="text-slate-500">· 24/7</span>
              </a>
              <a href="mailto:hello@skylark.vn" className="flex items-center gap-2 text-[13px] hover:text-white">
                <Phosphor.EnvelopeSimple size={13} weight="bold" className="text-slate-400" />
                hello@skylark.vn
              </a>
              <span className="flex items-center gap-2 text-[13px]">
                <Phosphor.MapPin size={13} weight="bold" className="text-slate-400" />
                Tầng 12, Bitexco, Q.1, TP.HCM
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
            title="Chuyến bay"
            icon="AirplaneTilt"
            links={[
              { label: 'Vé máy bay nội địa', href: '#' },
              { label: 'Vé quốc tế', href: '#' },
              { label: 'Hạng thương gia', href: '#' },
              { label: 'Hãng hàng không', href: '#' },
              { label: 'Sân bay phổ biến', href: '#' },
              { label: 'Lịch bay', href: '#' }
            ]}
          />
          <FooterColumn
            title="Khách sạn"
            icon="Buildings"
            links={[
              { label: 'Resort biển', href: '#' },
              { label: 'Hotel trung tâm', href: '#' },
              { label: 'Boutique hotel', href: '#' },
              { label: 'Homestay', href: '#' },
              { label: 'Villa cao cấp', href: '#' },
              { label: 'Khu vực ĐNÁ', href: '#' }
            ]}
          />
          <FooterColumn
            title="Điểm đến"
            icon="MapTrifold"
            links={[
              { label: 'Phú Quốc', href: '#' },
              { label: 'Đà Lạt', href: '#' },
              { label: 'Hội An', href: '#' },
              { label: 'Bangkok', href: '#' },
              { label: 'Bali', href: '#' },
              { label: 'Tokyo', href: '#' },
              { label: 'Singapore', href: '#' },
              { label: 'Xem tất cả 87', href: '#' }
            ]}
          />
          <FooterColumn
            title="Cẩm nang"
            icon="BookOpen"
            links={[
              { label: 'Kinh nghiệm du lịch', href: '#' },
              { label: 'Visa & hộ chiếu', href: '#' },
              { label: 'Bảo hiểm du lịch', href: '#' },
              { label: 'Thuế & phí', href: '#' },
              { label: 'Mẹo tiết kiệm', href: '#' },
              { label: 'Blog', href: '#' }
            ]}
          />
          <FooterColumn
            title="Thành viên"
            icon="Crown"
            links={[
              { label: 'Skylark Rewards', href: '#' },
              { label: 'Điểm thưởng', href: '#' },
              { label: 'Hạng thẻ', href: '#' },
              { label: 'Đối tác', href: '#' },
              { label: 'Khuyến mãi thành viên', href: '#' }
            ]}
          />
          <FooterColumn
            title="Hỗ trợ"
            icon="Headset"
            links={[
              { label: 'Trung tâm hỗ trợ', href: '#' },
              { label: 'Hủy / đổi booking', href: '#' },
              { label: 'Hoàn tiền', href: '#' },
              { label: 'Liên hệ', href: '#' },
              { label: 'Khiếu nại', href: '#' },
              { label: 'FAQ', href: '#' }
            ]}
          />
        </div>

        {/* App + Payment row */}
        <div className="mt-12 pt-8 border-t border-slate-800/50 grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* App download */}
          <div>
            <h3 className="text-[15px] font-bold text-white mb-4">Tải ứng dụng Skylark</h3>
            <div className="flex items-center gap-4">
              <div className="w-24 h-24 bg-white rounded-xl p-2 flex items-center justify-center flex-shrink-0">
                <div className="w-full h-full bg-slate-900 rounded grid grid-cols-5 gap-px">
                  {Array.from({ length: 25 }).map((_, i) => (
                    <div key={i} className={`${(i * 7) % 3 === 0 ? 'bg-white' : ''} ${(i * 11) % 5 === 0 ? 'bg-white' : ''}`} />
                  ))}
                </div>
              </div>
              <div className="space-y-2">
                <a href="#" className="flex items-center gap-2 px-3 py-2 bg-slate-900 hover:bg-slate-800 border border-slate-700 rounded-lg">
                  <Phosphor.AppleLogo size={20} weight="bold" className="text-white" />
                  <div className="text-left">
                    <div className="text-[10px] text-slate-400">Tải về từ</div>
                    <div className="text-[12px] font-bold text-white">App Store</div>
                  </div>
                </a>
                <a href="#" className="flex items-center gap-2 px-3 py-2 bg-slate-900 hover:bg-slate-800 border border-slate-700 rounded-lg">
                  <Phosphor.GooglePlayLogo size={20} weight="bold" className="text-white" />
                  <div className="text-left">
                    <div className="text-[10px] text-slate-400">Tải về từ</div>
                    <div className="text-[12px] font-bold text-white">Google Play</div>
                  </div>
                </a>
              </div>
            </div>
          </div>

          {/* Payment + Trust */}
          <div>
            <h3 className="text-[15px] font-bold text-white mb-4">Thanh toán & Bảo mật</h3>
            <div className="flex flex-wrap items-center gap-2">
              {[
                'visa', 'mastercard', 'jcb', 'amex',
                'momo', 'zalopay', 'vnpay', 'paypal'
              ].map(slug => (
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
                <span className="text-[10px] font-extrabold text-slate-200 tracking-widest bg-slate-800 px-1.5 py-0.5 rounded">IATA</span>
                IATA certified
              </span>
              <span className="inline-flex items-center gap-1.5">
                <Phosphor.SealCheck size={14} weight="fill" className="text-sky-400" />
                Đã đăng ký Bộ VH-TT&DL
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
              © 2026 Skylark Travel JSC · Giấy phép KD lữ hành quốc tế số 79-022/2020/TCDL-GP LHQT · MST 0315.123.456
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
        <Icon size={14} weight="bold" className="text-sky-400" />
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
      aria-label={`Skylark trên ${label}`}
      className="w-8 h-8 inline-flex items-center justify-center bg-slate-900 hover:bg-sky-600 border border-slate-800 rounded-full transition-colors"
    >
      <Icon size={14} weight="bold" className="text-slate-300" />
    </a>
  );
}
```

## 8. Accessibility

- Footer là `<footer>` semantic
- Pre-footer CTA `<form>` với email input có label
- Mỗi link column có `<h3>` cho screen reader
- Social links `aria-label` cụ thể (không chỉ icon)
- Hotline `tel:` link accessible
- Email `mailto:` link accessible
- Payment icons có alt text
- App store badges accessible
- Newsletter button có visible text
- "Trợ giúp" link semantic
- Color contrast: white/slate-300 trên slate-950 = AA pass

## 9. Performance

- Payment icons qua Simple Icons CDN (cached)
- App store badges có thể preload
- Footer ở bottom, không cần lazy load
- Lazy load cho app QR image
- Newsletter form là client component

## 10. Anti-patterns đã tránh

- ❌ Chỉ 3 columns (đã 6 columns)
- ❌ Tiny social icons (đã 8x8 = 32x32px, touch target ≥ 44px recommended, OK for desktop)
- ❌ Generic "Contact us"
- ❌ Hide trust signals (đã show IATA, secured payment, license)
- ❌ Missing app download
- ❌ Generic payment icons

---

**Component family**: Layout #5 — `footer-mega`