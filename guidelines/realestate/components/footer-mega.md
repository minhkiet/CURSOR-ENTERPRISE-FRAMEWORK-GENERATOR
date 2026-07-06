# Mega Footer

> Footer 6-col dày đặc với links + app download QR + payment logos + social + hotline. Là chuẩn footer của web thương mại VN 2026.

## 1. Cấu trúc

```
┌──────────────────────────────────────────────────────────────┐
│ Pre-footer CTA strip (dark navy bg)                         │
│ ┌────────────────────────┬────────────────────────────────┐ │
│ │ Tải app Anchor Pro     │ [QR code]                       │ │
│ │ Mua bán, thuê BĐS      │ [App Store] [Google Play]      │ │
│ │ mọi lúc mọi nơi        │                                 │ │
│ └────────────────────────┴────────────────────────────────┘ │
├──────────────────────────────────────────────────────────────┤
│ Main footer (slate-900 bg)                                   │
│ ┌──────────┬──────────┬──────────┬──────────┬─────────────┐│
│ │ Logo     │ Mua bán  │ Cho thuê │ Dự án    │ Hỗ trợ     ││
│ │ Hotline  │ • Căn hộ │ • Căn hộ │ • HCM    │ • Trung    ││
│ │ 1900-... │ • Nhà    │ • Nhà    │ • Hà Nội │   tâm KH   ││
│ │ Email    │ • Đất    │ • P. thuê│ • Đà Nẵng│ • Câu hỏi  ││
│ │ Địa chỉ │ • Biệt   │ ...      │ ...      │ • Pháp lý   ││
│ │          │   thự   │          │          │ • Điều khoản││
│ ├──────────┴──────────┴──────────┴──────────┴─────────────┤│
│ │ Về Anchor Pro  ·  Tin tức  ·  Tuyển dụng  ·  Blog      ││
│ ├──────────────────────────────────────────────────────────┤│
│ │ [Facebook] [YouTube] [Zalo] [TikTok] [LinkedIn]        ││
│ │ [Payment: Visa · Master · Momo · ZaloPay · VNPay · QR] ││
│ │ [Bộ Công Thương logo + Đã đăng ký BCT]                  ││
│ └──────────────────────────────────────────────────────────┘│
├──────────────────────────────────────────────────────────────┤
│ Sub-footer (slate-950 bg)                                    │
│ © 2026 Anchor Pro. Giấy phép số .../GP-XYZ. MST ...         │
│ Đã đăng ký Bộ Công Thương theo Nghị định ...                │
└──────────────────────────────────────────────────────────────┘
```

## 2. Sections chi tiết

### 2.1 Pre-footer CTA (dark navy)

```
┌─ Anchor Pro · App ─────────────────────────────────────────┐
│ [logo Anchor Pro]               ┌─────────┐                │
│                                  │  █▀▀ ▀█ │                │
│ Tải app Anchor Pro               │  ▀  █ █ │  ← QR code   │
│ Mua bán, cho thuê BĐS            │  █▀▀ ▀█ │                │
│ ngay trên điện thoại             └─────────┘                │
│                                                           │
│ Quét QR hoặc tải từ:                                      │
│ [App Store badge] [Google Play badge]                      │
└──────────────────────────────────────────────────────────┘
```

### 2.2 Main footer (5 cột + Logo cột)

#### Cột 1 — Brand

- Logo Anchor Pro (light version)
- Hotline: **1900 1569** (8h-22h)
- Email: support@anchorpro.vn
- Địa chỉ: Tầng 12, Tòa Bitexco Financial, Q.1, TP.HCM

#### Cột 2 — Mua bán

- Căn hộ chung cư
- Nhà phố, nhà riêng
- Đất nền
- Biệt thự, liền kề
- Shophouse
- Officetel, văn phòng
- Dự án sắp mở bán

#### Cột 3 — Cho thuê

- Cho thuê căn hộ
- Cho thuê nhà nguyên căn
- Cho thuê phòng trọ
- Cho thuê mặt bằng
- Thuê ngắn hạn (theo ngày)

#### Cột 4 — Khu vực

- TP. Hồ Chí Minh
- Hà Nội
- Đà Nẵng
- Nha Trang
- Bình Dương
- Long An
- Đồng Nai
- Toàn quốc

#### Cột 5 — Hỗ trợ

- Trung tâm hỗ trợ
- Hỏi đáp thường gặp
- Pháp lý BĐS
- Cẩm nang mua nhà
- Điều khoản sử dụng
- Chính sách bảo mật
- Quy chế hoạt động

### 2.3 Footer sub-row

- Về Anchor Pro · Tin tức · Tuyển dụng · Blog · Báo chí · Sitemap
- Social: Facebook · YouTube · Zalo · TikTok · LinkedIn · Instagram
- Payment: Visa · Master · JCB · Momo · ZaloPay · VNPay · QR Banking

### 2.4 Sub-footer (legal)

- © 2026 Anchor Pro. All rights reserved.
- Giấy phép mạng xã hội số .../GP-XYZ do Sở TT&TT TP.HCM cấp ngày ...
- MST: 0316xxx
- Đã đăng ký với Bộ Công Thương theo Nghị định 17/2020/NĐ-CP
- Logo Bộ Công Thương (verified badge)

## 3. Asset

| Element | Source |
|---|---|
| QR code | Generated SVG component (placeholder) |
| App Store badge | `https://developer.apple.com/assets/elements/badges/download-on-the-app-store.svg` |
| Google Play badge | `https://play.google.com/intl/en_us/badges/static/images/badges/en_badge_web_generic.png` |
| Social icons | Phosphor / Simple Icons |
| Payment logos | Simple Icons: `visa`, `mastercard`, `jcb`, plus custom for Momo/ZaloPay/VNPay |
| Bộ Công Thương logo | Local SVG (gov emblem) |

## 4. Code reference

```tsx
<footer className="bg-slate-900 text-slate-300 mt-16">
  {/* Pre-footer CTA */}
  <div className="bg-gradient-to-br from-teal-600 to-teal-800 text-white">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
        <div>
          <h3 className="text-3xl lg:text-4xl font-extrabold tracking-tight">
            Tải app Anchor Pro
          </h3>
          <p className="mt-2 text-teal-100">
            Mua bán, cho thuê BĐS ngay trên điện thoại. Đăng tin miễn phí, nhận khách trong 24h.
          </p>
          <div className="mt-6 flex items-center gap-3">
            <a href="#" aria-label="Tải từ App Store">
              <img src="https://developer.apple.com/assets/elements/badges/download-on-the-app-store.svg" alt="" className="h-12" />
            </a>
            <a href="#" aria-label="Tải từ Google Play">
              <img src="https://play.google.com/intl/en_us/badges/static/images/badges/en_badge_web_generic.png" alt="" className="h-12" />
            </a>
          </div>
        </div>
        <div className="flex items-center justify-center lg:justify-end gap-6">
          <div className="bg-white p-3 rounded-2xl shadow-2xl">
            <QRCodeSVG value="https://anchorpro.vn/app" size={140} />
          </div>
          <div className="text-[13px] text-teal-100">
            <p className="font-bold text-white">Quét QR</p>
            <p>Tự động mở link tải app phù hợp với thiết bị của bạn</p>
          </div>
        </div>
      </div>
    </div>
  </div>

  {/* Main footer */}
  <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-8 mb-10">
      {/* Brand col */}
      <div className="col-span-2 md:col-span-3 lg:col-span-1">
        <img src="/logo-anchor-light.svg" alt="Anchor Pro" className="h-8 mb-4" />
        <div className="space-y-2 text-[13px]">
          <a href="tel:19001569" className="flex items-center gap-2 hover:text-white">
            <Phosphor.Phone size={14} weight="bold" className="text-teal-400" />
            <span className="font-bold tabular-nums">1900 1569</span>
            <span className="text-slate-400">(8h-22h)</span>
          </a>
          <a href="mailto:support@anchorpro.vn" className="flex items-center gap-2 hover:text-white">
            <Phosphor.Envelope size={14} weight="bold" className="text-teal-400" />
            support@anchorpro.vn
          </a>
          <p className="flex items-start gap-2 text-slate-400">
            <Phosphor.MapPin size={14} weight="fill" className="text-teal-400 mt-0.5 flex-shrink-0" />
            Tầng 12, Tòa Bitexco Financial, Q.1, TP.HCM
          </p>
        </div>
      </div>

      {/* Link cols */}
      <FooterCol title="Mua bán" items={[
        'Căn hộ chung cư', 'Nhà phố, nhà riêng', 'Đất nền',
        'Biệt thự, liền kề', 'Shophouse', 'Officetel, văn phòng'
      ]} />

      <FooterCol title="Cho thuê" items={[
        'Cho thuê căn hộ', 'Cho thuê nhà', 'Cho thuê phòng trọ',
        'Cho thuê mặt bằng', 'Thuê ngắn hạn'
      ]} />

      <FooterCol title="Khu vực" items={[
        'TP. Hồ Chí Minh', 'Hà Nội', 'Đà Nẵng', 'Nha Trang',
        'Bình Dương', 'Long An', 'Đồng Nai'
      ]} />

      <FooterCol title="Hỗ trợ" items={[
        'Trung tâm hỗ trợ', 'Hỏi đáp', 'Pháp lý BĐS',
        'Cẩm nang mua nhà', 'Điều khoản', 'Bảo mật'
      ]} />

      {/* App + Social col */}
      <div className="col-span-2 md:col-span-3 lg:col-span-1">
        <h4 className="text-white font-bold text-[13px] uppercase tracking-wider mb-4">Kết nối</h4>
        <div className="flex items-center gap-3 mb-4">
          <SocialIcon icon="FacebookLogo" href="#" />
          <SocialIcon icon="YoutubeLogo" href="#" />
          <SocialIcon icon="TiktokLogo" href="#" />
          <SocialIcon icon="LinkedinLogo" href="#" />
          <SocialIcon icon="InstagramLogo" href="#" />
        </div>
        <h4 className="text-white font-bold text-[13px] uppercase tracking-wider mb-3 mt-6">Thanh toán</h4>
        <div className="flex items-center gap-2 flex-wrap">
          {['visa', 'mastercard', 'momo', 'vnpay', 'zalopay'].map(p => (
            <div key={p} className="h-7 w-10 bg-white rounded flex items-center justify-center p-1">
              <img src={`https://cdn.simpleicons.org/${p}`} alt={p} className="h-full w-full object-contain" />
            </div>
          ))}
        </div>
      </div>
    </div>

    {/* Sub-row */}
    <div className="pt-8 border-t border-slate-800 flex flex-col md:flex-row items-center justify-between gap-4 text-[12px] text-slate-400">
      <div className="flex items-center gap-4 flex-wrap">
        <a href="/about" className="hover:text-white">Về Anchor Pro</a>
        <a href="/news" className="hover:text-white">Tin tức</a>
        <a href="/careers" className="hover:text-white">Tuyển dụng</a>
        <a href="/blog" className="hover:text-white">Blog</a>
        <a href="/press" className="hover:text-white">Báo chí</a>
        <a href="/sitemap" className="hover:text-white">Sitemap</a>
      </div>
      <div className="flex items-center gap-2 text-[11px]">
        <span>Đã đăng ký Bộ Công Thương</span>
        <img src="/bo-cong-thuong.svg" alt="" className="h-8" />
      </div>
    </div>
  </div>

  {/* Sub-footer legal */}
  <div className="bg-slate-950 text-slate-500 text-[11px] py-4">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
      © 2026 Anchor Pro. Giấy phép số 123/GP-XYZ do Sở TT&TT TP.HCM cấp ngày 15/3/2026.
      MST: 0316123456.
    </div>
  </div>
</footer>
```

## 5. Accessibility

- `<footer>` semantic
- Mỗi column có `<h3>` heading
- Phone/email là `<a href="tel:">` / `<a href="mailto:">`
- QR code có `aria-label="Quét QR để tải app"`
- Social icons có `aria-label` cho mỗi link
- Color contrast: slate-300 trên slate-900 đạt 8:1

## 6. Performance

- Footer lazy load nếu dưới fold
- QR code component import dynamic
- Logo SVG inline (không HTTP request)