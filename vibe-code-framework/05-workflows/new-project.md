# New Project Workflow

> **Version:** 1.0.0 | **Category:** Workflow | **Steps:** 8

---

## Purpose

Workflow chuẩn để tạo project mới từ đầu.

## Steps

### Step 1: Define Scope

```
┌────────────────────────────────────────────────────────────┐
│ Step 1: Define Project Scope                             │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  1. Project overview                                     │
│     - Name & description                                 │
│     - Target users                                      │
│     - Success metrics                                   │
│                                                            │
│  2. Non-functional requirements                         │
│     - Performance targets                               │
│     - Scalability requirements                          │
│     - Security requirements                             │
│                                                            │
│  Gate: Scope approved?                                  │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Step 2: Choose Tech Stack

```
┌────────────────────────────────────────────────────────────┐
│ Step 2: Choose Technology Stack                          │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  1. Frontend                                           │
│     - Framework: Vue / React / Angular                   │
│     - Styling: Tailwind / CSS Modules                   │
│     - State: Pinia / Redux / NgRx                       │
│                                                            │
│  2. Backend                                            │
│     - Language: Node / Python / Go / C#                  │
│     - Framework: Express / FastAPI / Gin / ASP.NET       │
│     - ORM: Prisma / Dapper / GORM                       │
│                                                            │
│  3. Database                                           │
│     - Type: PostgreSQL / MySQL / MongoDB                 │
│     - Cache: Redis                                      │
│                                                            │
│  4. Infrastructure                                     │
│     - Deploy: Vercel / AWS / Docker                     │
│     - CI/CD: GitHub Actions / GitLab CI                  │
│                                                            │
│  Gate: Tech stack approved?                             │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Step 3: Design Architecture

```
┌────────────────────────────────────────────────────────────┐
│ Step 3: Design System Architecture                       │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  1. High-level architecture                             │
│     - System diagram                                    │
│     - Component overview                                │
│     - Data flow                                        │
│                                                            │
│  2. API design                                         │
│     - REST/GraphQL contracts                           │
│     - Authentication strategy                          │
│                                                            │
│  3. Database schema                                   │
│     - Entity relationship diagram                       │
│     - Index strategy                                   │
│                                                            │
│  Gate: Architecture approved?                           │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Step 4: Setup Project

```
┌────────────────────────────────────────────────────────────┐
│ Step 4: Project Setup                                    │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  1. Initialize repository                               │
│     - Git init                                         │
│     - .gitignore                                       │
│     - License                                          │
│                                                            │
│  2. Setup frontend                                    │
│     - Scaffold project                                 │
│     - Configure ESLint/Prettier                        │
│     - Setup testing (Vitest/Jest)                      │
│                                                            │
│  3. Setup backend                                     │
│     - Scaffold project                                 │
│     - Configure linting                                │
│     - Setup testing                                   │
│                                                            │
│  4. Setup infrastructure                               │
│     - Docker Compose for local dev                    │
│     - CI/CD pipeline                                  │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Step 5: Implement Foundation

```
┌────────────────────────────────────────────────────────────┐
│ Step 5: Implement Foundation                             │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  1. Authentication                                      │
│     - JWT setup                                        │
│     - Login/Register flows                             │
│     - Password hashing                                 │
│                                                            │
│  2. Database schema                                    │
│     - Initial migrations                               │
│     - Seed data                                       │
│                                                            │
│  3. API foundation                                     │
│     - Base controller/service structure                 │
│     - Error handling                                   │
│     - Logging                                          │
│                                                            │
│  Gate: Foundation verified?                             │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Step 6: Implement Core Features

```
┌────────────────────────────────────────────────────────────┐
│ Step 6: Implement Core Features                         │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  For each feature:                                       │
│                                                            │
│  1. Create feature branch                              │
│  2. Write specification                               │
│  3. Implement domain layer                            │
│  4. Implement application layer                        │
│  5. Implement infrastructure layer                   │
│  6. Implement presentation layer                      │
│  7. Write tests                                       │
│  8. Create PR & review                                │
│                                                            │
│  Gate: All core features done?                         │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Step 7: Polish & Optimize

```
┌────────────────────────────────────────────────────────────┐
│ Step 7: Polish & Optimize                              │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  1. Performance                                        │
│     - Bundle size optimization                         │
│     - Database query optimization                      │
│     - Caching strategy                                 │
│                                                            │
│  2. Security                                           │
│     - Security audit                                  │
│     - Penetration testing                             │
│                                                            │
│  3. UX/UI                                              │
│     - Responsive design                               │
│     - Accessibility                                   │
│     - Error states                                   │
│                                                            │
│  Gate: Quality gates passed?                           │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Step 8: Launch

```
┌────────────────────────────────────────────────────────────┐
│ Step 8: Launch                                          │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  1. Pre-launch checklist                               │
│     - All tests green                                  │
│     - Documentation complete                           │
│     - Monitoring configured                            │
│                                                            │
│  2. Deploy                                            │
│     - Staging verification                            │
│     - Production deployment                            │
│                                                            │
│  3. Post-launch                                       │
│     - Monitor metrics                                 │
│     - Gather feedback                                 │
│     - Plan next iteration                            │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

## Project Structure Template

```
project/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── stores/
│   │   ├── services/
│   │   ├── types/
│   │   └── utils/
│   ├── tests/
│   ├── package.json
│   └── vite.config.ts
│
├── backend/
│   ├── src/
│   │   ├── domain/
│   │   ├── application/
│   │   ├── infrastructure/
│   │   ├── presentation/
│   │   └── config/
│   ├── tests/
│   ├── package.json
│   └── tsconfig.json
│
├── docker-compose.yml
├── .gitignore
├── README.md
└── LICENSE
```

## Timeline Guide

| Phase | Duration | Deliverable |
|-------|----------|------------|
| Scope & Stack | 1-2 days | Tech stack chosen |
| Architecture | 2-3 days | System design doc |
| Foundation | 3-5 days | Auth + DB ready |
| Core Features | 1-2 weeks | MVP ready |
| Polish | 1 week | Production ready |
| Launch | 1-2 days | Live |
