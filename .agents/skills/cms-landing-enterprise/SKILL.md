---
name: "cms-landing-enterprise"
description: "CMS Landing Enterprise v4 - Full SaaS CRM/CMS/Landing/Wallet/Affiliate system. Generate complete production-ready code from spec."
version: 4.0.0
author: "OpenAI"
created: 2026-09-29
updated: 2026-09-29
---

# CMS Landing Enterprise v4 Skill

> **Phiên bản:** 4.0.0 | **Author:** OpenAI | **Stack:** Vue 3 + ASP.NET Core 9 + Dapper + SQLite/PostgreSQL

Use this skill when building CMS Landing Enterprise - a complete SaaS system with CRM, CMS, Landing Builder, Wallet, Affiliate, and multi-channel integrations.

## System Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    CMS LANDING ENTERPRISE v4                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │   DASHBOARD │  │     CRM     │  │   LANDING   │  │    CMS      │  │
│  │  Widgets    │  │  Lead/Cust  │  │   Builder   │  │  Page/Menu  │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  │
│                                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │   WALLET    │  │  AFFILIATE  │  │   ORDERS    │  │   PAYMENT    │  │
│  │   Points    │  │   F0-F3     │  │  Invoice    │  │  SePay/Strp │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  │
│                                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │    CHAT     │  │   CALENDAR  │  │    TASK     │  │    BLOG     │  │
│  │  SignalR    │  │  Events     │  │   Kanban    │  │   Content   │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Tech Stack

### Frontend
- Vue 3 + TypeScript + Composition API
- Vite + TailwindCSS + Preline UI
- Pinia + Vue Router + VueUse
- ApexCharts + ApexCharts Vue3
- Mobile First + Bottom Navigation

### Backend
- ASP.NET Core 9 + Dapper
- UnitOfWork + Repository Pattern
- ASP.NET Core Identity + JWT
- SignalR + Refresh Token

### Database
- SQLite (default) / PostgreSQL / MySQL
- Audit Log on all entities
- Soft delete pattern

### Deploy
- Docker + Nginx
- IIS + Windows VPS
- Linux VPS + Vercel

## Trigger Keywords

### Module Keywords
- cms landing enterprise
- saas crm
- landing builder
- menu builder
- wallet system
- affiliate system
- commission engine
- lead workspace
- customer workspace
- product workspace
- invoice workspace

### Feature Keywords
- drag drop dashboard
- bottom navigation
- floating action button
- responsive layout
- mobile first
- workspace layout
- pipeline view
- kanban board
- calendar view
- real-time chat

### Integration Keywords
- sepay payment
- stripe payment
- telegram integration
- zalo integration
- facebook integration
- signalr realtime

### Payment Keywords
- point wallet
- commission wallet
- deposit withdraw
- affiliate referral
- multi-level commission
- idempotent webhook

## Development Phases

### Phase 1: Foundation
- [ ] Project scaffolding (Vue 3 + ASP.NET Core 9)
- [ ] Authentication (JWT + Refresh Token)
- [ ] Database schema (all entities)
- [ ] RBAC system (roles + permissions)
- [ ] Menu builder (dynamic menu)
- [ ] Base layout (sidebar + header)

### Phase 2: Core Modules
- [ ] Dashboard (widget system)
- [ ] CRM (Lead + Customer workspace)
- [ ] Product + Category management
- [ ] Order + Invoice system
- [ ] Wallet (Point + Commission)

### Phase 3: Landing Builder
- [ ] Section library (Hero, Feature, Pricing, etc.)
- [ ] Drag-drop editor
- [ ] Preview (Desktop/Tablet/Mobile)
- [ ] Landing workspace
- [ ] Component library

### Phase 4: Affiliate & Payment
- [ ] Referral system (F0-F3)
- [ ] Commission engine
- [ ] SePay integration
- [ ] Stripe integration
- [ ] Withdrawal workflow

### Phase 5: Collaboration
- [ ] Task (Kanban + List + Calendar)
- [ ] Calendar (Day/Week/Month/Agenda)
- [ ] Internal Chat (SignalR)
- [ ] Notification system
- [ ] Blog + Media

### Phase 6: Advanced
- [ ] Automation engine
- [ ] Reports + Analytics
- [ ] API system
- [ ] Settings (all configurable)
- [ ] Dark mode
- [ ] AI integration

## Mobile UX Rules

### Bottom Navigation (5 items)
```
┌─────┬─────┬─────┬─────┬─────┐
│ 🏠  │ CRM │ ⚡  │ 💬  │ ⋯   │
│Home │     │Quick│Chat │More │
└─────┴─────┴─────┴─────┴─────┘
```

### FAB (Floating Action Button)
```
┌─────────────────────────┐
│     Primary Action      │
│  ┌────┐ ┌────┐ ┌────┐  │
│  │Lead│ │Task│ │Inv │  │
│  └────┘ └────┘ └────┘  │
│  ┌────┐ ┌────┐ ┌────┐  │
│  │Prod│ │Land│ │Cal │  │
│  └────┘ └────┘ └────┘  │
└─────────────────────────┘
```

### Touch Targets
- Minimum: 48x48px
- No hover dependency
- Swipe gestures
- Pull refresh
- Sticky header/bottom nav

## Design System

### Colors
```css
--color-primary: #22C55E;
--color-primary-dark: #16A34A;
--color-primary-light: #DCFCE7;
--color-background: #F8FAF8;
--color-surface: #FFFFFF;
--color-border: #E5E7EB;
--color-text: #1F2937;
--color-success: #22C55E;
--color-warning: #F59E0B;
--color-danger: #EF4444;
--color-info: #3B82F6;
--color-dark: #0F172A;
```

### Typography
```css
--font-family: 'Inter', sans-serif;
--font-h1: 32px;
--font-h2: 24px;
--font-h3: 20px;
--font-body: 16px;
--font-caption: 14px;
```

### Radius
```css
--radius-card: 24px;
--radius-button: 16px;
--radius-input: 14px;
--radius-avatar: 999px;
```

### Spacing
```css
--space-xs: 4px;
--space-sm: 8px;
--space-md: 16px;
--space-lg: 24px;
--space-xl: 32px;
--space-2xl: 48px;
```

## Theme Variables

All themes stored in database, not hardcoded:

| Setting | Default | Type |
|---------|---------|------|
| system_name | "CMS Enterprise" | string |
| logo_url | "/logo.svg" | string |
| primary_color | "#22C55E" | string |
| dark_mode | false | boolean |
| radius_card | 24 | number |
| commission_f0 | 10 | number (%) |
| commission_f1 | 5 | number (%) |
| commission_f2 | 2 | number (%) |
| commission_f3 | 1 | number (%) |

## Entity Architecture

### Core Entities
```
User ─────┬──── Wallet (Point)
          ├──── CommissionWallet
          ├──── Affiliate
          ├──── UserRole
          └──── Notification

Lead ────┬──── Task
         ├──── CalendarEvent
         ├──── LeadChat
         └──── Order

Customer ┬──── Wallet
         ├──── Order
         ├──── Invoice
         └──── Affiliate

Product ─┬──── Category
         ├──── OrderItem
         └──── Landing

Order ───┼──── Invoice
         ├──── Payment
         └──── OrderItem

Affiliate ┬──── Referral (F1-F3)
          ├──── CommissionTransaction
          └──── CommissionWithdrawal
```

## Workspace Layout Pattern

Every entity has a workspace page (`/{entity}/{id}`):

```
┌──────────────────────────────────────────────────────────────┐
│  HEADER                                                     │
│  ┌──────┐ Name │ Phone │ Email │ Status │ Owner    [Actions]│
│  │Avatar│                                               │    │
│  └──────┘                                                   │
├──────────────────────────────────────────────────────────────┤
│  TABS                                                       │
│  [Overview] [Timeline] [Tasks] [Calendar] [Orders] [More...]│
├──────────────────────────────────────────────────────────────┤
│  CONTENT                                                    │
│                                                              │
│  Quick Actions (FAB style):                                 │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐                              │
│  │Call│ │SMS │ │Task│ │Meet│                              │
│  └────┘ └────┘ └────┘ └────┘                              │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Quality Gates

### Pre-Implementation
- [ ] Spec reviewed and understood
- [ ] Entity diagram created
- [ ] API endpoints designed
- [ ] Component structure planned
- [ ] Mobile layout verified

### Post-Implementation
- [ ] Build passes (npm build && dotnet build)
- [ ] Responsive tested (Desktop/Tablet/Mobile)
- [ ] Bottom Navigation functional
- [ ] FAB working
- [ ] Workspace layout complete
- [ ] No TODO/placeholder
- [ ] Audit log on changes
- [ ] RBAC enforced

## File Structure

### Frontend
```
src/
├── assets/           # Static assets
├── components/      # Reusable components
│   ├── ui/          # Base UI (Button, Card, Input)
│   ├── layout/     # Layout (Sidebar, Header, BottomNav)
│   └── workspace/   # Workspace components
├── composables/     # Vue composables
├── layouts/        # Page layouts
├── pages/          # Route pages
│   ├── dashboard/
│   ├── crm/
│   ├── landing/
│   ├── wallet/
│   ├── affiliate/
│   └── ...
├── router/         # Vue Router
├── stores/         # Pinia stores
├── types/          # TypeScript types
└── utils/          # Utilities
```

### Backend
```
backend/
├── src/
│   ├── Controllers/    # API Controllers
│   ├── Services/       # Business logic
│   ├── Repositories/    # Data access (Dapper)
│   ├── Entities/       # Database entities
│   ├── DTOs/           # Data transfer objects
│   ├── Middleware/     # Auth, RBAC, logging
│   └── Extensions/     # Extension methods
├── tests/              # Unit tests
└── Program.cs
```

## API Design

### RESTful Endpoints
```
GET    /api/{resource}          # List with pagination
GET    /api/{resource}/{id}     # Get single
POST   /api/{resource}          # Create
PUT    /api/{resource}/{id}      # Update
DELETE /api/{resource}/{id}      # Soft delete

GET    /api/{resource}/{id}/workspace  # Workspace data
POST   /api/{resource}/{id}/action      # Entity action
```

### Response Format
```json
{
  "success": true,
  "data": { },
  "message": "Success",
  "errors": []
}
```

## Security Checklist

- [ ] JWT with short expiry (15 min)
- [ ] Refresh token rotation
- [ ] RBAC on all endpoints
- [ ] Input validation (FluentValidation)
- [ ] SQL injection prevention (Dapper)
- [ ] XSS prevention
- [ ] CSRF protection
- [ ] Rate limiting
- [ ] Audit logging
- [ ] HTTPS only
- [ ] Secure cookie settings

## Performance Checklist

- [ ] Lazy loading routes
- [ ] Virtual scrolling for lists
- [ ] Image optimization (WEBP)
- [ ] Code splitting
- [ ] Caching strategy
- [ ] Database indexing
- [ ] Query optimization
- [ ] SignalR for realtime

## Related Skills

- [[../skills/code_karpathy]] - Think before coding, minimal code
- [[../skills/full-output]] - Complete implementation, no placeholders
- [[../skills/frontend-review]] - Quality gate for frontend
- [[../skills/security-review]] - Security audit
- [[../skills/dashboard-ui]] - Dashboard & form components
- [[../skills/vietnam-payment-review]] - Vietnam payment (SePay, Stripe)

## Related Agents

- [[../agents/cms-architect]] - Solution architect for CMS
- [[../agents/cms-frontend-engineer]] - Vue 3 specialist
- [[../agents/cms-backend-engineer]] - ASP.NET Core specialist
- [[../agents/cms-ux-designer]] - UX designer for CMS

## Related Rules

- [[../rules/rule_cms-architecture]] - Architecture patterns
- [[../rules/rule_cms-stack]] - Tech stack conventions
- [[../rules/rule_cms-rbac]] - RBAC patterns
- [[../rules/rule_cms-responsive]] - Mobile-first responsive
