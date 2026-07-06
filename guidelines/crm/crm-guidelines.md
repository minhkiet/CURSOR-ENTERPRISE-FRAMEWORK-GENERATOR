# CRM Platform. Design System Guidelines (Market Pro 2026)

> **Redesign ngày 2026-07-05.** Full market-style SaaS. Giống Salesforce, HubSpot, Pipedrive — data-dense, keyboard-first, dashboard heavy.

## 1. Context

Northwind CRM cho sales teams 5-50. Bốn bề mặt:

- **Pipeline** (`/`). kanban board 5 stages
- **Contacts** (`/contacts`). sortable list + detail drawer
- **Reports** (`/reports`). analytics dashboard
- **Marketing landing** (`/marketing`). public-facing site

### 1.2 Brand-locked

- Wordmark: "Northwind" · Plus Jakarta Sans 800, tracking -0.04em
- Palette: slate, indigo, mint, paper
- Inter primary (giữ), Plus Jakarta Sans cho landing

### 1.3 Design intent

**Professional cockpit for revenue teams**. Data-dense, keyboard-first, no decoration.

### 1.4 Anti-patterns

- ❌ Cream / serif
- ❌ "Feel like..." 
- ❌ Em-dash
- ❌ Decorative empty states

---

## 2. Tokens

Xem `tokens.json`.

---

## 3. Imagery & Video

### Marketing landing:
- Hero: dashboard screenshot (real, not fake)
- Customer logos: Simple Icons CDN
- Customer photos: Unsplash curated headshots
- Product demo: video walkthrough dashboard

---

## 4. Section anatomy (Marketing landing)

1. **Sticky header**. Logo · Product · Solutions · Pricing · Resources · Login · "Start free" CTA
2. **Hero**. Headline 72px + 18px subtext + CTA "Bắt đầu miễn phí" + "Xem demo 3 phút" + dashboard screenshot
3. **Logo wall**. 50+ customer logos
4. **3-pillar feature bento**. Bento asymmetric với screenshot từng feature
5. **Pipeline demo video**. Video walkthrough 60s
6. **Customer testimonials**. Bento 3 customer + quote + metric
7. **Integrations**. Logo grid với Slack, Gmail, Outlook, Zapier, etc.
8. **Pricing**. 3 tiers
9. **FAQ**. 8 câu hỏi
10. **Final CTA**. "Đóng deal đầu tiên trong 7 ngày"
11. **Footer**

---

## 5. Voice

- Professional, terse, never playful
- "Deal", "Contact", "Account", "Pipeline" exact terms
- Money: `$1,250` (no decimals unless cents), `tabular-nums`
- Time: relative ("2h ago") + absolute on hover
- Em-dash cấm

---

## 6. Components

- `pipeline-kanban.md`
- `contact-table.md`
- `dashboard-widget.md`
- `drawer.md`
- `data-table.md`
- `pricing-tier.md`
- `testimonial-portrait.md`
- `footer-mega.md`

---

## 7. Checklist

- [ ] Tokens semantic
- [ ] Plus Jakarta Sans / Inter
- [ ] Indigo brand
- [ ] Real dashboard screenshots
- [ ] Real customer logos via Simple Icons
- [ ] Keyboard nav
- [ ] axe-core 0
- [ ] WCAG AA
- [ ] Reduced motion
- [ ] No em-dash