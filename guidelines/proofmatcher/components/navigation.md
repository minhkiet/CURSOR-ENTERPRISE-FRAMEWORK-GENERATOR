# Navigation Component

> Primary site navigation. Ba biến thể: top bar (always visible), footer (always visible at bottom), breadcrumb (docs only).

## 1. Mục đích

Dẫn hướng toàn site. Linear-style: dark base, monospace nav items, blur on scroll, hairline border. Đủ minimal để content là trung tâm, đủ distinct để user luôn biết họ đang ở đâu.

## 2. Hệ thống icon

| Vai trò | Icon Phosphor | Kích thước |
|---|---|---|
| Logo | Brand wordmark, không icon | 24×24px mark + wordmark |
| Hamburger mobile | `List` | 20px |
| Close menu | `X` | 20px |
| Caret (dropdown) | `CaretDown` | 12px |
| Cart | `ShoppingBag` | 18px |
| User / account | `UserCircle` | 20px |
| Search trigger | `MagnifyingGlass` | 18px |
| Theme toggle | `Moon` / `Sun` | 18px |
| GitHub social | `GithubLogo` hoặc Simple Icons | 18px |
| Twitter / X social | `TwitterLogo` hoặc Simple Icons | 18px |
| Discord social | `DiscordLogo` hoặc Simple Icons | 18px |
| RSS | `Rss` | 16px |
| External link (footer) | `ArrowUpRight` | 12px |
| Back (breadcrumb mobile) | `ArrowLeft` | 16px |
| Breadcrumb separator | `CaretRight` | 12px, tertiary |
| Cookie icon | `Cookie` | 18px |

## 3. Hình ảnh và minh họa

Navigation không dùng ảnh nền. Logo là exception:

- **Logo mark** 24×24px, dùng inline SVG (không Picsum). Lưu trong `/public/logo.svg`.
- **Logo wordmark** "PROOF MATCHER" kèm mark. Mono font, uppercase, `letter-spacing: 0.18em`.
- **Social icons** dùng Simple Icons CDN: `https://cdn.simpleicons.org/github/ffffff`, `https://cdn.simpleicons.org/twitter/ffffff`, `https://cdn.simpleicons.org/discord/ffffff`.

## 4. Cấu trúc

### Top bar

```
┌──────────────────────────────────────────────────────┐
│ [LOGO]   Home  Components  About  Contact   [Cart] │
└──────────────────────────────────────────────────────┘
```

| Slot | Ghi chú |
|---|---|
| Container | sticky top, `color.surface.base` background, 1px bottom border `rgba(255,255,255,0.08)` |
| Height | 60px (compact) hoặc 72px (default) |
| Logo | trái, 24×24px mark + wordmark |
| Nav items | center hoặc right, 4 items max trong primary nav |
| Cart/utility | phải |

### Footer

```
┌──────────────────────────────────────────────────────┐
│  [LOGO + tagline]    Main Pages   Social   Legal    │
│  ─────────────────────────────────────────────────── │
│  © 2026 ProofMatcher · Privacy · Terms · Cookies     │
└──────────────────────────────────────────────────────┘
```

- 4-column grid ở desktop, 2-column ở tablet, 1-column ở mobile.
- Bottom row: copyright + legal links.

### Breadcrumb (docs)

```
Home / Components / Button
```

- Truncate tới 3 levels với "..." middle item nếu deeper.

## 5. Biến thể

| Variant | Sticky | Background | Cách dùng |
|---|---|---|---|
| `top` | có | `color.surface.base` với `backdrop-filter: blur(12px)` khi scrolled | All marketplace pages |
| `footer` | không | `color.surface.base` với 1px top border `rgba(255,255,255,0.08)` | All pages |
| `breadcrumb` | không | transparent | Docs pages only |

## 6. Sizes

| Size | Height | Logo size |
|---|---|---|
| `compact` | 56px | 24×24px |
| `default` | 64px | 32×32px |
| `large` | 80px | 40×40px |

## 7. Trạng thái

### Top bar

| Trạng thái | Background | Border | Logo | Items |
|---|---|---|---|---|
| `default` | transparent (over hero) hoặc `color.surface.base` | none hoặc 1px `rgba(255,255,255,0.08)` | `color.text.primary` | `color.text.secondary` |
| `scrolled` | `color.surface.base` + `backdrop-filter: blur(12px) saturate(160%)` | 1px `rgba(255,255,255,0.08)` | unchanged | unchanged |
| `mobile-open` | `color.surface.base` | 1px `rgba(255,255,255,0.08)` | unchanged | hamburger → X |

### Nav item states

| Trạng thái | Color | Underline / Border | Khác |
|---|---|---|---|
| `default` | `color.text.secondary` | none |. |
| `hover` | `color.text.primary` | none | `transition: 150ms` |
| `focus-visible` | `color.text.primary` | none | 2px outline ring |
| `active` (current page) | `color.text.primary` | 2px bottom border `color.border.strong` | `aria-current="page"`, font-weight 600 |

## 8. Mobile menu (top bar variant)

- Hamburger button ở <768px (`aria-expanded`, `aria-controls`).
- Open menu: full-screen overlay với nav list và CTA. Closes on Escape, on outside click, on link click.
- Trap focus bên trong menu khi open. Restore focus tới hamburger khi close.
- `aria-modal="true"` trên overlay.
- Body scroll lock khi open.
- Close button: `Phosphor.X` weight="bold" 20px.

## 9. Footer link states

- Default: `color.text.tertiary`.
- Hover: `color.text.primary`.
- Focus-visible: 2px outline ring.
- External links: `ArrowUpRight` icon + `rel="noopener noreferrer"`.

## 10. Sticky behavior

- Top bar stick on scroll. Dùng `position: sticky; top: 0`.
- Khi scrolled past 16px, thêm `.scrolled` class để apply background + blur.
- Không animate height change. class swap instant để tránh layout shift.

## 11. Skip-to-content link

- First focusable element trong DOM, trước nav.
- Ẩn mặc định (off-screen), visible on focus.
- "Skip to main content" text với `ArrowDown` icon.
- Bắt buộc cho keyboard accessibility.

## 12. Responsive

| Breakpoint | Top bar | Footer |
|---|---|---|
| <768px | Hamburger menu | 1 column |
| 768–1023px | Full nav inline | 2 columns |
| ≥1024px | Full nav inline | 4 columns |

## 13. Edge cases

- **Active link missing**: nếu không có nav item match current route, không có item nào nhận `aria-current` (không fake active state).
- **Long nav label**: truncate với ellipsis ở 200px max width.
- **Logo missing alt**: logo PHẢI có `alt="ProofMatcher home"`. descriptive, không "logo".
- **Footer overflow**: column count giảm trước khi text wrap.
- **iOS Safari 100vh bug**: không liên quan cho nav (nav fixed height, không viewport-based).
- **Cookie banner**: xuất hiện dưới nav, fixed bottom. `role="region"`, `aria-label="Cookie preferences"`. Có `Cookie` icon + Accept/Reject buttons.

## 14. Accessibility

- `<nav>` element với `aria-label="Primary"` hoặc `aria-label="Footer"`.
- Tất cả interactive items keyboard accessible.
- Skip-to-content link đầu tiên.
- Focus trap bên trong mobile menu.
- Escape đóng mobile menu.
- `aria-current="page"` trên active link.
- Touch target ≥44×44px trên mọi nav items.

## 15. QA acceptance criteria

```
[ ] <nav> element với aria-label
[ ] Skip-to-content link đầu tiên focusable
[ ] Sticky top bar với scrolled state
[ ] Mobile menu mở/đóng qua keyboard
[ ] Mobile menu traps focus
[ ] Escape đóng mobile menu
[ ] Focus restored to hamburger khi menu close
[ ] Active nav link có aria-current="page"
[ ] Body scroll locked khi menu open
[ ] Footer columns responsive ở mọi breakpoints
[ ] Logo alt là "ProofMatcher home"
[ ] Touch targets ≥44×44px
[ ] Hamburger/close icons Phosphor (X, List)
[ ] Social icons dùng Simple Icons CDN
[ ] axe-core: 0 violations
```

## 16. Code reference

```tsx
{/* Skip link */}
<a
  href="#main-content"
  class="sr-only focus:not-sr-only focus:absolute focus:top-2 focus:left-2 focus:z-50 focus:px-4 focus:py-2 focus:bg-white focus:text-black focus:rounded-md focus:font-medium"
>
  Skip to main content
</a>

{/* Top bar */}
<nav aria-label="Primary" class="sticky top-0 z-40 backdrop-blur-md bg-black/80 border-b border-[rgba(255,255,255,0.08)]">
  <div class="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
    {/* Logo */}
    <a href="/" aria-label="ProofMatcher home" class="inline-flex items-center gap-2.5">
      <img src="/logo.svg" alt="" aria-hidden="true" class="w-6 h-6" />
      <span class="font-mono text-[12px] uppercase tracking-[0.18em] text-white font-bold">Proof Matcher</span>
    </a>

    {/* Desktop nav */}
    <div class="hidden md:flex items-center gap-6">
      <a
        href="/"
        aria-current="page"
        class="relative text-white font-semibold text-[14px] py-2 after:absolute after:left-0 after:right-0 after:bottom-0 after:h-[2px] after:bg-white"
      >
        Home
      </a>
      <a href="/components" class="text-[#a1a1aa] hover:text-white text-[14px] py-2 transition-colors duration-150">
        Components
      </a>
      <a href="/about" class="text-[#a1a1aa] hover:text-white text-[14px] py-2 transition-colors duration-150">
        About
      </a>
      <a href="/contact" class="text-[#a1a1aa] hover:text-white text-[14px] py-2 transition-colors duration-150">
        Contact
      </a>
    </div>

    {/* Right utilities */}
    <div class="flex items-center gap-3">
      <button
        type="button"
        aria-label="Search templates"
        class="hidden md:inline-flex items-center justify-center w-10 h-10 text-[#a1a1aa] hover:text-white transition-colors duration-150 rounded-md"
      >
        <Phosphor.MagnifyingGlass size={18} weight="bold" aria-hidden="true" />
      </button>
      <a
        href="/cart"
        aria-label="Cart (0 items)"
        class="hidden md:inline-flex items-center justify-center w-10 h-10 text-[#a1a1aa] hover:text-white transition-colors duration-150 rounded-md relative"
      >
        <Phosphor.ShoppingBag size={18} weight="bold" aria-hidden="true" />
        <span class="absolute -top-0.5 -right-0.5 w-4 h-4 bg-white text-black font-mono text-[10px] font-bold rounded-full flex items-center justify-center">0</span>
      </a>

      {/* Mobile hamburger */}
      <button
        type="button"
        class="md:hidden inline-flex items-center justify-center w-10 h-10 text-white rounded-md"
        aria-expanded={mobileMenuOpen}
        aria-controls="mobile-menu"
        aria-label={mobileMenuOpen ? 'Close menu' : 'Open menu'}
      >
        {mobileMenuOpen ? <Phosphor.X size={20} weight="bold" aria-hidden="true" /> : <Phosphor.List size={20} weight="bold" aria-hidden="true" />}
      </button>
    </div>
  </div>

  {/* Mobile menu overlay */}
  {mobileMenuOpen && (
    <div id="mobile-menu" role="dialog" aria-modal="true" aria-label="Mobile navigation" class="md:hidden border-t border-[rgba(255,255,255,0.08)] bg-black">
      <div class="px-6 py-6 space-y-1">
        {navItems.map(item => (
          <a
            key={item.href}
            href={item.href}
            aria-current={isCurrent(item.href) ? 'page' : undefined}
            class={cn(
              'block px-4 py-3 text-[16px] rounded-md transition-colors duration-150',
              isCurrent(item.href) ? 'bg-[#0d0d0d] text-white font-semibold' : 'text-[#a1a1aa] hover:bg-[#0d0d0d] hover:text-white'
            )}
            onClick={() => setMobileMenuOpen(false)}
          >
            {item.label}
          </a>
        ))}
      </div>
    </div>
  )}
</nav>

{/* Footer */}
<footer aria-label="Footer" class="bg-black border-t border-[rgba(255,255,255,0.08)] mt-32">
  <div class="max-w-7xl mx-auto px-6 py-16">
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12">
      {/* Brand */}
      <div>
        <a href="/" aria-label="ProofMatcher home" class="inline-flex items-center gap-2.5">
          <img src="/logo.svg" alt="" aria-hidden="true" class="w-7 h-7" />
          <span class="font-mono text-[12px] uppercase tracking-[0.18em] text-white font-bold">Proof Matcher</span>
        </a>
        <p class="mt-4 text-[13px] text-[#737373] leading-relaxed max-w-xs">
          Tokenized templates for founders and small teams. Ship faster, look sharper.
        </p>
      </div>

      {/* Main pages */}
      <div>
        <h4 class="font-mono text-[11px] uppercase tracking-[0.18em] text-white font-bold mb-4">Product</h4>
        <ul class="space-y-2">
          <li><a href="/components" class="text-[#a1a1aa] hover:text-white text-[13px] transition-colors duration-150">Components</a></li>
          <li><a href="/pricing" class="text-[#a1a1aa] hover:text-white text-[13px] transition-colors duration-150">Pricing</a></li>
          <li><a href="/changelog" class="text-[#a1a1aa] hover:text-white text-[13px] transition-colors duration-150">Changelog</a></li>
          <li><a href="/roadmap" class="text-[#a1a1aa] hover:text-white text-[13px] transition-colors duration-150">Roadmap</a></li>
        </ul>
      </div>

      {/* Social */}
      <div>
        <h4 class="font-mono text-[11px] uppercase tracking-[0.18em] text-white font-bold mb-4">Social</h4>
        <ul class="space-y-2">
          <li>
            <a
              href="https://github.com/proofmatcher"
              target="_blank"
              rel="noopener noreferrer"
              aria-label="GitHub (opens in new tab)"
              class="inline-flex items-center gap-2 text-[#a1a1aa] hover:text-white text-[13px] transition-colors duration-150"
            >
              <img src="https://cdn.simpleicons.org/github/ffffff" alt="" aria-hidden="true" class="w-4 h-4" />
              GitHub
              <Phosphor.ArrowUpRight size={11} weight="bold" aria-hidden="true" />
            </a>
          </li>
          <li>
            <a
              href="https://twitter.com/proofmatcher"
              target="_blank"
              rel="noopener noreferrer"
              aria-label="Twitter (opens in new tab)"
              class="inline-flex items-center gap-2 text-[#a1a1aa] hover:text-white text-[13px] transition-colors duration-150"
            >
              <img src="https://cdn.simpleicons.org/twitter/ffffff" alt="" aria-hidden="true" class="w-4 h-4" />
              Twitter
              <Phosphor.ArrowUpRight size={11} weight="bold" aria-hidden="true" />
            </a>
          </li>
          <li>
            <a
              href="https://discord.gg/proofmatcher"
              target="_blank"
              rel="noopener noreferrer"
              aria-label="Discord (opens in new tab)"
              class="inline-flex items-center gap-2 text-[#a1a1aa] hover:text-white text-[13px] transition-colors duration-150"
            >
              <img src="https://cdn.simpleicons.org/discord/ffffff" alt="" aria-hidden="true" class="w-4 h-4" />
              Discord
              <Phosphor.ArrowUpRight size={11} weight="bold" aria-hidden="true" />
            </a>
          </li>
        </ul>
      </div>

      {/* Legal */}
      <div>
        <h4 class="font-mono text-[11px] uppercase tracking-[0.18em] text-white font-bold mb-4">Legal</h4>
        <ul class="space-y-2">
          <li><a href="/privacy" class="text-[#a1a1aa] hover:text-white text-[13px] transition-colors duration-150">Privacy Policy</a></li>
          <li><a href="/terms" class="text-[#a1a1aa] hover:text-white text-[13px] transition-colors duration-150">Terms of Use</a></li>
          <li><a href="/refund" class="text-[#a1a1aa] hover:text-white text-[13px] transition-colors duration-150">Refund Policy</a></li>
          <li><a href="/cookies" class="text-[#a1a1aa] hover:text-white text-[13px] transition-colors duration-150">Cookies</a></li>
        </ul>
      </div>
    </div>

    <div class="mt-12 pt-8 border-t border-[rgba(255,255,255,0.08)] flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
      <p class="text-[12px] text-[#737373]">
        © 2026 ProofMatcher. All rights reserved.
      </p>
      <a
        href="mailto:support@proofmatcher.com"
        class="inline-flex items-center gap-1.5 text-[12px] text-[#a1a1aa] hover:text-white transition-colors duration-150"
      >
        <Phosphor.Envelope size={13} weight="bold" aria-hidden="true" />
        support@proofmatcher.com
      </a>
    </div>
  </div>
</footer>
```