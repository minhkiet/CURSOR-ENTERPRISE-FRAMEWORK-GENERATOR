# Test Case: UpNewsFeed Clone - Rules/Skills Reasoning Trace

## Requirement
> "Clone web https://www.upnewsfeed.com/"

**Target Website:** UpNewsFeed - Cộng đồng Maker, Developer và Entrepreneur Việt Nam
**Status:** ✅ Website analyzed from search results

---

## Phase 1: Intent Detection & Task Analysis

### Step 1.1: Intent Detection (intent-detection.mdc)
```
Input: "Clone web https://www.upnewsfeed.com/"

Intent Classification:
├── Primary Intent: CLONE_WEBSITE
├── Secondary Intent: UI_REPLICATION
├── Domain: COMMUNITY_PLATFORM / TECH_NEWS
├── Complexity: MEDIUM (modern UI, responsive, multiple sections)
├── Urgency: STANDARD
└── Language: Vietnamese

Detected Keywords:
- "clone" → website duplication, UI replication
- "upnewsfeed.com" → Vietnamese tech community platform
- Website features detected:
  ├── Bảng xếp hạng (Rankings)
  ├── Trending/Featured sections
  ├── Category browsing (Công cụ Lập trình, Thiết kế UI/UX, etc.)
  ├── User profiles
  ├── Newsletter subscription
  └── Community guidelines

⚠️ ETHICAL NOTE: Website cloning for personal portfolio/demo is acceptable.
   Cloning for phishing/malicious purposes is prohibited.
   Implied intent: Portfolio project, learning, or legitimate demo.
```

### Step 1.2: Website Structure Analysis (from search results)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    UPNEWSFEED.COM - STRUCTURE ANALYSIS                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  HEADER:                                                                 │
│  ├── Logo: "UPNEWSFEED"                                                 │
│  ├── Navigation: Khám phá, Showcase, Bảng xếp hạng, Cách hoạt động    │
│  ├── Auth: Đăng ký, Đăng nhập                                         │
│  └── Language: VN                                                        │
│                                                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  HERO SECTION:                                                           │
│  ├── Tagline: "Khám phá. Chia sẻ. Kiến tạo."                          │
│  ├── Description: Cộng đồng Maker, Developer, Entrepreneur Việt Nam     │
│  ├── CTA: Đăng bài, Cách hoạt động                                    │
│  └── Newsletter signup: "UpNewsWeekly"                                  │
│                                                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  FEATURED SECTIONS:                                                     │
│  ├── Categories Grid:                                                     │
│  │   ├── Case Study & Khởi nghiệp                                      │
│  │   ├── Tài chính số & Đầu tư                                        │
│  │   ├── Kiếm tiền online MMO                                          │
│  │   ├── SaaS & Web App                                                 │
│  │   ├── AI & Tự động hóa                                              │
│  │   ├── Công cụ Lập trình                                             │
│  │   ├── Thiết kế & Đa phương tiện                                     │
│  │   ├── Tăng trưởng & Marketing                                       │
│  │   ├── Ứng dụng Di động                                             │
│  │   └── Co-founder & Tuyển dụng                                       │
│  │                                                                      │
│  ├── Xu hướng (Trending):                                               │
│  │   ├── FlipLab - Học Flashcard thông minh                            │
│  │   ├── Transifyr - Dịch giọng nói real-time                          │
│  │   ├── WinWraper - Quản lý tiến trình Windows                         │
│  │   └── NestProxy - Affiliate platform                                 │
│  │                                                                      │
│  ├── Bảng xếp hạng:                                                     │
│  │   ├── Bài viết                                                       │
│  │   └── Sản phẩm (Coming Soon)                                        │
│  │                                                                      │
│  └── Top Thành viên tuần:                                               │
│      └── Member avatars with activity indicators                         │
│                                                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  CONTENT SECTIONS:                                                       │
│  ├── Mới nhất (Latest):                                                  │
│  │   └── Cards with: Title, Category, Author, Time, Comments            │
│  │                                                                      │
│  ├── Nổi bật tuần (Weekly Highlights):                                  │
│  │   └── Award-style cards with vote counts                             │
│  │                                                                      │
│  └── UpNewsFeed Official:                                                │
│      └── Admin posts, guidelines, announcements                          │
│                                                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  FOOTER:                                                                 │
│  ├── Pháp lý: Chính sách bảo mật, Điều khoản, Quy chuẩn              │
│  ├── Kết nối: Social links                                              │
│  └── Newsletter: Đăng ký nhận tin                                       │
│                                                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  DESIGN LANGUAGE:                                                        │
│  ├── Modern, clean SaaS aesthetic                                        │
│  ├── Card-based layouts                                                  │
│  ├── Vietnamese content focus                                            │
│  ├── Dark/Light mode potential                                           │
│  └── Mobile-first responsive                                             │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Step 1.3: Task Analyzer (task-analyzer.mdc)
```
Task Manifest Generation:
Task: UpNewsFeed Website Clone

Subtasks:
[1] UI/UX Design
    - Modern card-based layout
    - Responsive grid system
    - Category navigation
    - Header with auth buttons
    - Hero section with CTA
    - Content cards with metadata
    - Ranking badges/indicators
    - Newsletter signup form
    - Footer with links

[2] Component Architecture
    - Header.vue (logo, nav, auth)
    - HeroSection.vue (tagline, CTA, newsletter)
    - CategoryGrid.vue (9 categories)
    - TrendingSection.vue (featured projects)
    - LatestPosts.vue (content cards)
    - RankingsWidget.vue (weekly highlights)
    - MemberList.vue (top members)
    - Footer.vue (links, newsletter)

[3] Data Structure (Mock/Static)
    - Categories data
    - Posts/Projects data
    - User profiles
    - Rankings data

[4] Interactions
    - Category filtering
    - Post card hover effects
    - Newsletter form submission
    - Auth modal (login/register)
    - Vote/reaction UI
    - Comment indicators

[5] Responsive Design
    - Mobile navigation
    - Grid collapse patterns
    - Touch-friendly cards
    - Sticky header

Estimated Complexity: 8-12 hours
Framework: Nuxt 3 (recommended for Vue ecosystem)
```

---

## Phase 2: Rules Auto-Discovery

### Step 2.1: Primary Rules Selection

| Rule | Trigger Reason | Load Order |
|------|---------------|------------|
| `task-analyzer.mdc` | Universal task analysis | 1st |
| `frontend-frameworks.mdc` | Nuxt 3 implementation | 2nd |
| `ui-visual-design.mdc` | Modern UI clone | 3rd |
| `coding-standards.mdc` | Code consistency | 4th |
| `architecture-patterns.mdc` | Component structure | 5th |
| `testing.mdc` | Component testing | 6th |

### Step 2.2: Domain-Specific Rules

| Rule | Trigger Reason |
|------|---------------|
| `frontend-frameworks.mdc` | Vue/Nuxt implementation |
| `ui-visual-design.mdc` | Card-based, modern aesthetic |
| `performance.mdc` | Image lazy loading, optimization |

### Step 2.3: Relevant Project Skills (local)

| Skill | Path | Trigger |
|-------|------|---------|
| `frontend-taste` | `.cursor/skills/frontend-taste/SKILL.md` | Modern design quality |
| `frontend-review` | `.cursor/skills/frontend-review/SKILL.md` | UI quality gate |
| `frontend-redesign` | `.cursor/skills/frontend-redesign/SKILL.md` | Design replication |

---

## Phase 3: Skills Auto-Discovery

### Step 3.1: Pre-Implementation Skills (skill-registry.mdc)

| Skill | Confidence | Trigger |
|-------|------------|---------|
| `karpathy-coding` | 90% | "Clone" = implement it |
| `ponytail` | 70% | MVP approach |
| `full-output` | 95% | Full UI replication |

### Step 3.2: Domain-Specific Skills

| Skill | Confidence | Trigger |
|-------|------------|---------|
| `frontend-taste` | 95% | Modern Vietnamese tech aesthetic |
| `frontend-review` | 90% | Quality gate for UI |
| `frontend-redesign` | 85% | Design replication |

### Step 3.3: Quality Gate Skills

| Skill | Gate Type | Purpose |
|-------|-----------|---------|
| `frontend-taste` | PRE-GATE | Design vision alignment |
| `frontend-review` | POST-GATE | UI quality check |

---

## Phase 4: Architecture Decision

### Step 4.1: Tech Stack Selection

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    TECHNOLOGY STACK                                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  FRONTEND:                                                              │
│  ├── Framework: Nuxt 3 (Vue 3 Composition API)                         │
│  ├── Styling: Tailwind CSS or UnoCSS                                   │
│  ├── Icons: Lucide Vue / Heroicons                                      │
│  ├── Fonts: Google Fonts (Inter, Plus Jakarta Sans)                     │
│  └── State: Pinia (for any interactive state)                          │
│                                                                          │
│  DESIGN SYSTEM:                                                          │
│  ├── Color Palette:                                                      │
│  │   ├── Primary: Blue-based tech theme                                │
│  │   ├── Secondary: Purple accent                                      │
│  │   ├── Neutrals: Gray scale                                          │
│  │   └── Category colors: Each category unique                         │
│  │                                                                      │
│  ├── Typography:                                                        │
│  │   ├── Headings: Bold, modern sans-serif                             │
│  │   ├── Body: Clean, readable                                         │
│  │   └── Code: Monospace for tech content                              │
│  │                                                                      │
│  └── Components:                                                        │
│      ├── Cards: Shadow, rounded corners, hover lift                     │
│      ├── Buttons: Filled, outlined, ghost variants                     │
│      ├── Badges: Category tags, ranking indicators                     │
│      └── Forms: Newsletter signup, auth forms                          │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Step 4.2: Component Structure

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    COMPONENT ARCHITECTURE                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  pages/                                                                 │
│  └── index.vue                                                          │
│                                                                          │
│  components/                                                            │
│  ├── layout/                                                            │
│  │   ├── AppHeader.vue                                                 │
│  │   │   ├── Logo.vue                                                  │
│  │   │   ├── NavMenu.vue                                               │
│  │   │   ├── AuthButtons.vue                                           │
│  │   │   └── MobileMenu.vue                                            │
│  │   └── AppFooter.vue                                                 │
│  │                                                                      │
│  ├── sections/                                                         │
│  │   ├── HeroSection.vue                                               │
│  │   │   ├── HeroTagline.vue                                           │
│  │   │   ├── HeroCTA.vue                                               │
│  │   │   └── NewsletterForm.vue                                        │
│  │   ├── CategoryGrid.vue                                              │
│  │   │   └── CategoryCard.vue (x9)                                     │
│  │   ├── TrendingSection.vue                                           │
│  │   │   └── ProjectCard.vue (x4)                                      │
│  │   ├── LatestPosts.vue                                               │
│  │   │   ├── PostCard.vue                                              │
│  │   │   └── LoadMore.vue                                              │
│  │   ├── RankingsSection.vue                                           │
│  │   │   ├── WeeklyWinners.vue                                         │
│  │   │   └── RankingsList.vue                                          │
│  │   └── TopMembers.vue                                                │
│  │                                                                      │
│  └── ui/                                                                │
│      ├── BaseButton.vue                                                 │
│      ├── BaseCard.vue                                                   │
│      ├── BaseBadge.vue                                                  │
│      ├── BaseInput.vue                                                 │
│      └── BaseAvatar.vue                                                 │
│                                                                          │
│  composables/                                                           │
│  ├── useCategories.ts                                                  │
│  ├── usePosts.ts                                                       │
│  └── useNewsletter.ts                                                  │
│                                                                          │
│  data/                                                                  │
│  ├── categories.ts                                                     │
│  ├── posts.ts                                                          │
│  └── mock-data.ts                                                      │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Step 4.3: UI Visual Design

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    UI DESIGN SPECIFICATION                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  LAYOUT:                                                                │
│  ├── Max-width: 1280px                                                 │
│  ├── Section spacing: 64px (py-16)                                     │
│  ├── Grid: 12-column, responsive                                       │
│  └── Card gap: 24px                                                    │
│                                                                          │
│  COLORS:                                                                │
│  ├── Primary: #3B82F6 (Blue-500)                                       │
│  ├── Secondary: #8B5CF6 (Purple-500)                                   │
│  ├── Success: #10B981 (Green-500)                                      │
│  ├── Warning: #F59E0B (Amber-500)                                      │
│  ├── Background: #FFFFFF / #F9FAFB (light mode)                       │
│  └── Text: #111827 / #6B7280 (gray-900/gray-500)                      │
│                                                                          │
│  TYPOGRAPHY:                                                            │
│  ├── H1: 3rem (48px), font-bold, line-height 1.2                      │
│  ├── H2: 2rem (32px), font-bold, line-height 1.3                     │
│  ├── H3: 1.5rem (24px), font-semibold, line-height 1.4               │
│  ├── Body: 1rem (16px), font-normal, line-height 1.6                 │
│  └── Small: 0.875rem (14px), font-normal                              │
│                                                                          │
│  SPACING:                                                               │
│  ├── xs: 4px                                                            │
│  ├── sm: 8px                                                            │
│  ├── md: 16px                                                           │
│  ├── lg: 24px                                                           │
│  ├── xl: 32px                                                           │
│  └── 2xl: 48px                                                          │
│                                                                          │
│  BORDERS:                                                               │
│  ├── Radius-sm: 6px                                                     │
│  ├── Radius-md: 8px                                                     │
│  ├── Radius-lg: 12px                                                    │
│  └── Radius-xl: 16px                                                    │
│                                                                          │
│  SHADOWS:                                                               │
│  ├── sm: 0 1px 2px rgba(0,0,0,0.05)                                   │
│  ├── md: 0 4px 6px rgba(0,0,0,0.1)                                   │
│  ├── lg: 0 10px 15px rgba(0,0,0,0.1)                                 │
│  └── Card hover: translateY(-2px) + shadow-lg                         │
│                                                                          │
│  ANIMATIONS:                                                            │
│  ├── Transition: 150ms ease-in-out                                      │
│  ├── Card hover: transform + shadow                                     │
│  └── Button hover: opacity change                                       │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 5: Execution Flow

### Step 5.1: Pre-Implementation Gates

```
[GATE 1] Design Vision Alignment ✅
├── Check: Understand UpNewsFeed aesthetic
├── Check: Identify target audience (Vietnamese tech community)
├── Check: Confirm MVP scope
└── Decision: APPROVE ✅

[GATE 2] Tech Stack Decision
├── Check: Nuxt 3 + Tailwind CSS
├── Check: Component structure
└── Decision: PROCEED

[GATE 3] Frontend Taste Review
├── Review: Modern SaaS aesthetic matches
├── Review: Vietnamese tech community feel
└── Decision: APPROVE
```

### Step 5.2: Implementation Phase

```
[PHASE A] Project Setup
├── nuxi init upnewsfeed-clone
├── Install: Tailwind CSS, @nuxtjs/google-fonts
├── Configure: nuxt.config.ts
├── Setup: tailwind.config.js
└── Create: directory structure

[PHASE B] Base Components
├── BaseButton.vue (variants: primary, secondary, ghost)
├── BaseCard.vue (with hover effects)
├── BaseBadge.vue (category tags)
├── BaseInput.vue (form inputs)
└── BaseAvatar.vue (user avatars)

[PHASE C] Layout Components
├── AppHeader.vue
│   ├── Logo (UPNEWSFEED)
│   ├── NavMenu (Khám phá, Showcase, BXH, Cách hoạt động)
│   ├── AuthButtons (Đăng ký, Đăng nhập)
│   └── MobileMenu (hamburger)
├── AppFooter.vue
│   ├── Legal links
│   ├── Social links
│   └── Copyright
└── Default layout

[PHASE D] Hero Section
├── HeroSection.vue
│   ├── H1: "Khám phá. Chia sẻ. Kiến tạo."
│   ├── Description text
│   ├── CTA buttons: Đăng bài, Cách hoạt động
│   └── Newsletter form: UpNewsWeekly signup
└── Hero styling (gradient background optional)

[PHASE E] Category Grid
├── CategoryGrid.vue
│   ├── 9 CategoryCard components
│   ├── Grid layout (3x3 on desktop, 2x on tablet, 1x on mobile)
│   └── Category icons
│
├── Categories:
│   ├── Case Study & Khởi nghiệp
│   ├── Tài chính số & Đầu tư
│   ├── Kiếm tiền online MMO
│   ├── SaaS & Web App
│   ├── AI & Tự động hóa
│   ├── Công cụ Lập trình
│   ├── Thiết kế & Đa phương tiện
│   ├── Tăng trưởng & Marketing
│   ├── Ứng dụng Di động
│   └── Co-founder & Tuyển dụng

[PHASE F] Content Sections
├── TrendingSection.vue
│   ├── Section title: "Xu hướng"
│   ├── 4 ProjectCard (featured projects)
│   └── Card: image, title, category, author, time, votes
│
├── LatestPosts.vue
│   ├── Section title: "Mới nhất"
│   ├── PostCard grid
│   └── Card: thumbnail, title, category, author, time, comments
│
├── RankingsSection.vue
│   ├── Section title: "Nổi bật tuần"
│   ├── WeeklyWinners component
│   └── RankingsList with vote counts
│
└── TopMembers.vue
    ├── Section title: "Top Thành viên tuần"
    └── Member avatars with activity

[PHASE G] Responsive Design
├── Mobile: Single column, hamburger menu
├── Tablet: 2-column grid
├── Desktop: 3-4 column grid
└── Large: Max-width container

[PHASE H] Mock Data
├── categories.ts (9 categories with icons)
├── posts.ts (sample posts/projects)
├── users.ts (mock user profiles)
└── rankings.ts (vote counts)
```

### Step 5.3: Post-Implementation Gates

```
[GATE 4] frontend-review (post-review)
├── Check: All sections implemented
├── Check: Responsive on mobile/tablet/desktop
├── Check: Card hover effects working
├── Check: Newsletter form UI present
├── Check: Vietnamese content displayed
├── Check: Zero TODOs
└── Decision: APPROVE or REQUEST_CHANGES

[GATE 5] Design Quality Check
├── Check: Modern SaaS aesthetic
├── Check: Card-based layout consistent
├── Check: Color palette applied
├── Check: Typography hierarchy
└── Decision: APPROVE
```

---

## Phase 6: Skill Execution Matrix

| Step | Skills Loaded | Rules Loaded | Output |
|------|--------------|--------------|--------|
| Analysis | `intent-detection` | `task-analyzer`, `skill-registry` | Task Manifest |
| Design | `frontend-taste` | `ui-visual-design`, `frontend-frameworks` | Design Spec |
| Code | `karpathy-coding`, `full-output` | `coding-standards`, `architecture-patterns` | Full UI |
| Review | `frontend-review` | `testing`, `ui-visual-design` | Quality Gate |

---

## Expected Test Criteria

### UI Components
- [ ] Header with logo, nav, auth buttons
- [ ] Hero section with tagline and CTA
- [ ] Newsletter signup form
- [ ] 9 category cards in grid
- [ ] Trending projects section
- [ ] Latest posts grid
- [ ] Rankings section
- [ ] Top members widget
- [ ] Footer with links

### Interactions
- [ ] Category cards hover effect
- [ ] Post cards hover effect
- [ ] Newsletter form visible
- [ ] Mobile menu toggle
- [ ] Responsive on all breakpoints

### Visual Quality
- [ ] Modern SaaS aesthetic
- [ ] Card-based layout
- [ ] Consistent spacing
- [ ] Vietnamese typography
- [ ] Category badges with colors
- [ ] Vote/comment indicators

### Functional Requirements
- [ ] Zero TODO comments
- [ ] Zero skeleton placeholders
- [ ] Static mock data loaded
- [ ] No console errors

### Verification Commands
```bash
# Check TODO count (should be 0)
grep -r "TODO" pages/ components/

# Check skeleton count (should be 0)
grep -r "skeleton" pages/ components/

# Verify components
ls components/sections/
# Expected: HeroSection, CategoryGrid, TrendingSection, etc.

# Verify responsive
grep -r "sm:|md:|lg:|xl:" components/
```

---

## Trace Log Template

```
[17:05:00] INTENT_DETECTED: CLONE_WEBSITE, UPNEWSFEED
[17:05:01] TARGET_ANALYZED: upnewsfeed.com structure extracted
[17:05:02] TASK_ANALYZER: Generating manifest...
[17:05:03] DOMAIN_IDENTIFIED: Vietnamese Tech Community Platform
[17:05:04] MANIFEST_COMPLETE: 5 subtasks, complexity=MEDIUM
[17:05:05] RULES_DISCOVERY: 6 rules loaded
[17:05:06] SKILLS_DISCOVERY: 5 skills matched
[17:05:07] PRE_GATE: Design Vision [✅ APPROVED]
[17:05:08] TECH_STACK: Nuxt 3 + Tailwind CSS
[17:05:09] PRE_GATE: Frontend Taste [APPROVED]
[17:05:10] IMPLEMENTATION_STARTED: Project Setup
[17:05:XX] IMPLEMENTATION_STARTED: Base Components
[17:05:XX] IMPLEMENTATION_STARTED: Layout (Header, Footer)
[17:05:XX] IMPLEMENTATION_STARTED: Hero Section
[17:05:XX] IMPLEMENTATION_STARTED: Category Grid
[17:06:XX] IMPLEMENTATION_STARTED: Content Sections
[17:06:XX] IMPLEMENTATION_STARTED: Responsive Design
[17:06:XX] POST_GATE: frontend-review [EXECUTING]
[17:06:XX] POST_GATE: Design Quality [EXECUTING]
[17:06:XX] POST_GATE: All gates [APPROVED]
[17:06:XX] TASK_COMPLETE: UpNewsFeed Clone delivered
```

---

## Critical Notes

1. **Ethical Clone Scope:**
   - ✅ OK: Portfolio project, learning, demo
   - ✅ OK: Personal practice with modern UI
   - ❌ NOT OK: Phishing/malicious purposes
   - ❌ NOT OK: Claiming as official website

2. **Content Differences:**
   - Use mock/placeholder content
   - Don't copy exact post titles or descriptions
   - Focus on UI/UX pattern replication
   - Add original touches and improvements

3. **Performance:**
   - Lazy load images
   - Optimize for Core Web Vitals
   - Use appropriate image sizes
   - Implement smooth animations

4. **Accessibility:**
   - Semantic HTML
   - Keyboard navigation
   - ARIA labels where needed
   - Color contrast compliance

---

## Clarification Questions

1. **Features Scope:**
   - Full clone or MVP (header + hero + categories)?
   - Include rankings functionality?
   - Newsletter form functional or just UI?

2. **Content Source:**
   - Use mock data or real content (with credits)?
   - Link to original or standalone?

3. **Additional Features:**
   - Dark mode support?
   - Search functionality?
   - Category filtering?
