---
name: "source-command-cms-command"
description: "CMS Landing Enterprise v4 - Build complete SaaS CRM/CMS/Landing/Wallet/Affiliate system"
---

# source-command-cms-command

Use this skill when the user asks to run the migrated source command `cms-command`.

## Command Template

# Command: /cms

## Mục tiêu
Build CMS Landing Enterprise v4 - complete SaaS system với CRM, CMS, Landing Builder, Wallet, Affiliate.

## Trigger Keywords
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
- drag drop dashboard
- bottom navigation
- floating action button
- mobile first
- responsive layout
- pipeline view
- kanban board
- calendar view
- real-time chat
- signalr

## Tech Stack

### Frontend
- [ ] Vue 3 + TypeScript + Composition API
- [ ] Vite + TailwindCSS + Preline UI
- [ ] Pinia + Vue Router + VueUse
- [ ] ApexCharts + VueApexCharts
- [ ] Mobile First + Bottom Navigation

### Backend
- [ ] ASP.NET Core 9 + Dapper
- [ ] UnitOfWork + Repository Pattern
- [ ] ASP.NET Core Identity + JWT
- [ ] SignalR + Refresh Token

### Database
- [ ] SQLite (default) / PostgreSQL / MySQL
- [ ] Audit Log on all entities
- [ ] Soft delete pattern

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

## Mobile UX

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

## Workspace Layout

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
│  CONTENT AREA                                                │
└──────────────────────────────────────────────────────────────┘
```

## Liên kết
- [[../skills/cms-landing-enterprise]] - CMS Landing Enterprise Master Skill
- [[../agents/cms-solution-architect]] - Solution Architect Agent
- [[../agents/cms-frontend-engineer]] - Frontend Engineer Agent
- [[../agents/cms-backend-engineer]] - Backend Engineer Agent
- [[../agents/cms-ux-designer]] - UX Designer Agent
- [[../rules/rule_cms-architecture]] - Architecture Rules
- [[../rules/rule_cms-stack]] - Tech Stack Rules
- [[../rules/rule_cms-rbac]] - RBAC Rules
- [[../rules/rule_cms-responsive]] - Responsive Rules
