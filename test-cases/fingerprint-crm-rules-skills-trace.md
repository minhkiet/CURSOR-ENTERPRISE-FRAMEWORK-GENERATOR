# Test Case: CRM Fingerprint Scanner - Rules/Skills Reasoning Trace

## Requirement
> "Xây dựng hoàn chỉnh một Web Application Progressive Web App (PWA) chạy trên điện thoại, tối ưu giao diện Mobile First, dùng để chụp hình vân tay bằng camera điện thoại, quản lý khách hàng và xử lý hình ảnh vân tay chuyên nghiệp."

---

## Phase 1: Intent Detection & Task Analysis

### Step 1.1: Intent Detection (intent-detection.mdc)
```
Input: "Xây dựng hoàn chỉnh một Web Application Progressive Web App (PWA) chạy trên điện thoại, tối ưu giao diện Mobile First, dùng để chụp hình vân tay bằng camera điện thoại, quản lý khách hàng và xử lý hình ảnh vân tay chuyên nghiệp."

Intent Classification:
├── Primary Intent: IMPLEMENT_FULL_STACK_APPLICATION
├── Domain: BIOMETRIC_CRM / FINGERPRINT_ANALYSIS
├── Complexity: ENTERPRISE (full-stack, PWA, AI, Camera, CRM)
├── Urgency: HIGH
└── Language: Vietnamese (auto-translate via multi-language-processing.mdc)

Detected Keywords:
- "PWA" → Progressive Web App patterns
- "Mobile First" → frontend-frameworks.mdc (Vue 3 mobile)
- "Camera" → MediaPipe/TensorFlow.js integration
- "AI xử lý hình ảnh" → OpenCV.js, TensorFlow.js, AI patterns
- "CRM" → crm-saas.mdc patterns
- "ASP.NET Core 9" → backend-frameworks.mdc
- "Vue 3" → frontend-frameworks.mdc
- "SQLite" → databases.mdc
- "JWT" → auth.mdc
- "Dashboard" → observability patterns
- "Đồng bộ Cloud" → Supabase, cloud-infra patterns
```

### Step 1.2: Task Analyzer (task-analyzer.mdc)
```
Task Manifest Generation:
Task: CRM Fingerprint Scanner - Full PWA Implementation

Subtasks:
[1] Project Setup & Architecture
    - Initialize Vue 3 + Vite + TypeScript + PWA
    - Initialize ASP.NET Core 9 Web API
    - Setup SQLite database
    - Configure Supabase Storage
    - Setup JWT Authentication
    - Configure Tailwind CSS
    - Setup Pinia + Vue Router
    - Project folder structure

[2] Authentication Module
    - Login page
    - Register page
    - Forgot password flow
    - OTP verification
    - JWT + Refresh Token implementation
    - Role-based access control
    - Permission system

[3] Dashboard Module
    - Dashboard layout (mobile-first)
    - Statistics cards (customers, profiles, captures)
    - Monthly report chart
    - Activity timeline
    - Quick actions FAB
    - Dark/Light mode toggle

[4] CRM Customer Management
    - Customer list with search/filter
    - Customer detail page
    - Add/Edit customer form
    - Avatar upload
    - Customer history timeline
    - QR Code generation per customer

[5] Fingerprint Profile Management
    - Profile list per customer
    - Profile detail page
    - 10-finger capture wizard
    - Capture progress indicator
    - Quality check per finger
    - Batch upload support

[6] Camera Capture Module
    - Camera access & initialization
    - Auto-focus, HDR, Flash controls
    - Finger placement guide overlay
    - Real-time quality indicators
    - AI guidance (position feedback)
    - Capture trigger
    - Multiple angle capture
    - Low-light mode

[7] AI Image Processing Pipeline
    - Finger cropping
    - Background removal
    - White balance adjustment
    - Contrast enhancement
    - Sharpening (unsharp mask)
    - CLAHE (Contrast Limited Adaptive Histogram Equalization)
    - Noise reduction
    - Ridge enhancement
    - Ridge frequency analysis
    - Ridge orientation map
    - Ridge skeletonization
    - Ridge highlighting
    - Standard resize (500x500)
    - DPI normalization (500 DPI)
    - PNG/TIFF export
    - Original vs processed storage

[8] Image Editor
    - Brightness/Contrast/Exposure controls
    - Gamma correction
    - Hue/Saturation adjustment
    - Temperature/Tint controls
    - Sharpness/Clarity/Texture
    - Noise reduction (denoise)
    - Blur (median, gaussian)
    - Threshold/Binary operations
    - Invert/Grayscale
    - Morphology operations
    - Crop/Rotate/Flip/Perspective
    - Undo/Redo/History
    - Before/After comparison slider
    - Reset to original

[9] AI Enhance (One-click)
    - Auto finger detection
    - Background removal
    - Lighting normalization
    - Noise reduction
    - Contrast enhancement
    - Ridge clarity improvement
    - Standardization pipeline

[10] AI Segmentation
    - Finger mask visualization
    - Ridge map display
    - Valley map display
    - Overlay controls

[11] File Management
    - Original image storage
    - Processed image storage
    - Thumbnail generation
    - Version history
    - Backup system
    - Cloud sync (Supabase)

[12] Reports Module
    - PDF report generation
    - Word document export
    - ZIP archive download
    - Print direct
    - Report templates

[13] Search & Filter
    - Search by name
    - Search by phone
    - Search by DOB
    - Search by profile ID
    - Search by capture date
    - Search by operator
    - Advanced filters

[14] System Administration
    - Role management
    - User management
    - Permission matrix
    - Audit log viewer
    - System settings
    - Database backup/restore

[15] Notifications
    - Push notifications
    - Toast messages
    - SMS integration (placeholder)
    - Email integration (placeholder)
    - Zalo webhook (placeholder)
    - Telegram webhook (placeholder)

[16] Sync & Offline
    - Offline detection
    - Service Worker setup
    - PWA caching strategy
    - Auto-sync when online
    - Conflict resolution

[17] Data Import/Export
    - Excel import
    - Excel export
    - CSV import
    - CSV export
    - Barcode scanning
    - QR code scanning

[18] UI Components
    - Bottom navigation
    - Floating action button
    - Card components
    - Timeline component
    - Image comparison slider
    - Carousel component
    - Wizard/Stepper
    - Modal/Drawer/Bottom sheet
    - Mobile-optimized controls

[19] Security Features
    - HTTPS enforcement
    - JWT token security
    - Role permission checks
    - Watermark on exports
    - File checksum
    - Audit logging
    - XSS/CSRF protection

[20] Performance Optimization
    - Lazy loading routes
    - Image compression (WebP)
    - Virtual scrolling
    - Infinite scroll
    - PWA offline-first
    - Service Worker caching
    - IndexedDB for offline storage

Estimated Complexity: 80-120 hours (Enterprise-level)
Framework: Vue 3 (Frontend) + ASP.NET Core 9 (Backend)
Database: SQLite + Supabase Storage
AI: OpenCV.js, TensorFlow.js, MediaPipe
```

---

## Phase 2: Rules Auto-Discovery

### Step 2.1: Primary Rules Selection

| Rule | Trigger Reason | Load Order |
|------|---------------|------------|
| `task-analyzer.mdc` | Universal task analysis | 1st |
| `frontend-frameworks.mdc` | Vue 3 + Vite + PWA project | 2nd |
| `backend-frameworks.mdc` | ASP.NET Core 9 Web API | 3rd |
| `architecture-patterns.mdc` | Clean Architecture + SOLID | 4th |
| `api-patterns.mdc` | REST API + JWT + Swagger | 5th |
| `ui-visual-design.mdc` | Apple/Material 3/Luxury style | 6th |
| `coding-standards.mdc` | Code consistency across stack | 7th |
| `auth.mdc` | JWT + OTP + RBAC | 8th |
| `databases.mdc` | SQLite + Repository Pattern | 9th |
| `crm-saas.mdc` | CRM patterns (customers, profiles) | 10th |
| `multi-tenant.mdc` | Multi-user with roles | 11th |
| `security.mdc` | JWT, Watermark, Audit | 12th |
| `cloudflare.mdc` | PWA + CDN deployment | 13th |
| `serverless.mdc` | PWA offline capabilities | 14th |
| `performance.mdc` | Image optimization, lazy loading | 15th |
| `observability.mdc` | Dashboard metrics, audit logs | 16th |
| `deployment.mdc` | PWA deployment | 17th |
| `testing.mdc` | Unit tests, integration tests | 18th |

### Step 2.2: Domain-Specific Rules

| Rule | Trigger Reason |
|------|---------------|
| `ai-knowledge.mdc` | OpenCV.js, TensorFlow.js, MediaPipe integration |
| `supabase.mdc` | Supabase Storage for file management |
| `llm-providers.mdc` | AI image processing pipeline |
| `redis.mdc` | Session caching for JWT refresh tokens |
| `container-orchestration.mdc` | If containerized deployment needed |
| `cloud-infra.mdc` | Cloud storage architecture |

### Step 2.3: Platform-Specific Rules

| Rule | Trigger Reason |
|------|---------------|
| `mobile-first.mdc` | Explicit "Mobile First" requirement |
| `pwa-patterns.mdc` | PWA implementation |
| `camera-api.mdc` | Camera access for fingerprint capture |
| `offline-first.mdc` | Offline + sync requirements |

---

## Phase 3: Skills Auto-Discovery

### Step 3.1: Pre-Implementation Skills (skill-registry.mdc)

| Skill | Confidence | Trigger |
|-------|------------|---------|
| `karpathy-coding` | 90% | Large implementation, senior dev approach |
| `ponytail` | 60% | Minimal code, YAGNI for MVP |
| `full-output` | 95% | Explicitly requested "hoàn chỉnh" |
| `frontend-frameworks` | 95% | Vue 3 + Vite project |
| `backend-review` | 85% | ASP.NET Core 9 implementation |
| `code-review` | 80% | Full-stack implementation quality |

### Step 3.2: Quality Gate Skills

| Skill | Gate Type | Purpose |
|-------|-----------|---------|
| `frontend-taste` | PRE-GATE | Ensure Apple/Material 3/Luxury design aesthetic |
| `frontend-review` | POST-GATE | Review Vue 3 + PWA implementation |
| `security-review` | POST-GATE | JWT, RBAC, watermark security |
| `web-performance-auditor` | POST-GATE | PWA performance, image optimization |
| `database-reviewer` | POST-GATE | SQLite schema, Repository pattern |

### Step 3.3: Specialized Skills

| Skill | Purpose |
|-------|---------|
| `canvas-design` | Dashboard charts, image editor |
| `image-enhancer` | AI image processing pipeline |
| `document-ocr` | Fingerprint analysis patterns |

---

## Phase 4: Execution Flow

### Step 4.1: Pre-Implementation Gates

```
[GATE 1] frontend-taste (pre-review)
├── Check: Design system (Apple/Material 3/Luxury)
├── Check: Mobile-first responsive layout
├── Check: Dark/Light mode consistency
├── Check: Touch-optimized interactions
├── Check: Bottom navigation design
└── Decision: APPROVE or REQUEST_CHANGES

[GATE 2] Architecture Review
├── Check: Clean Architecture separation
├── Check: Frontend/backend layer separation
├── Check: Repository Pattern implementation
├── Check: AI pipeline architecture
└── Decision: PROCEED

[GATE 3] AI Integration Plan
├── Check: OpenCV.js/TensorFlow.js strategy
├── Check: MediaPipe finger detection
├── Check: Browser-based vs server processing
└── Decision: PROCEED
```

### Step 4.2: Implementation Phase

```
[PHASE A] Project Foundation
├── Initialize Vue 3 + Vite + TypeScript + PWA
├── Initialize ASP.NET Core 9 Web API
├── Setup folder structure (Clean Architecture)
├── Configure Tailwind CSS + mobile-first
├── Setup Pinia + Vue Router
├── Setup Dapper + SQLite
├── Setup JWT authentication
├── Configure Supabase Storage client
└── Setup Service Worker

[PHASE B] Backend API Layer
├── Database schema (SQLite)
│   ├── Users, Roles, Permissions
│   ├── Customers, FingerprintProfiles
│   ├── FingerImages, CaptureSessions
│   ├── EnhancementHistory, AnalysisResults
│   ├── Reports, AuditLogs
│   └── Notifications
├── Repository implementations
├── Unit of Work pattern
├── JWT authentication endpoints
├── Customer CRUD endpoints
├── Profile management endpoints
├── Fingerprint capture endpoints
├── Image processing endpoints
├── Report generation endpoints
├── Search/filter endpoints
├── Audit log endpoints
├── Swagger documentation
└── Middleware (auth, error handling, logging)

[PHASE C] Authentication Module (Frontend)
├── LoginPage.vue
├── RegisterPage.vue
├── ForgotPasswordPage.vue
├── OTPVerificationPage.vue
├── AuthStore.ts (Pinia)
├── AuthService.ts (API calls)
├── useAuth composable
├── Permission directive
├── Route guards
└── Token refresh interceptor

[PHASE D] Dashboard Module
├── DashboardPage.vue
├── StatsCards.vue
├── MonthlyChart.vue
├── ActivityTimeline.vue
├── QuickActionsFAB.vue
├── ThemeToggle.vue
├── DashboardStore.ts
└── DashboardService.ts

[PHASE E] CRM Customer Module
├── CustomerListPage.vue
├── CustomerDetailPage.vue
├── CustomerForm.vue
├── CustomerSearch.vue
├── CustomerFilters.vue
├── AvatarUpload.vue
├── QRCodeGenerator.vue
├── CustomerHistoryTimeline.vue
├── CustomerStore.ts
└── CustomerService.ts

[PHASE F] Fingerprint Profile Module
├── ProfileListPage.vue
├── ProfileDetailPage.vue
├── FingerprintWizard.vue
├── FingerCaptureFlow.vue
├── CaptureProgressIndicator.vue
├── QualityIndicator.vue
├── ProfileStore.ts
└── ProfileService.ts

[PHASE G] Camera Capture Module
├── CameraCapturePage.vue
├── CameraControls.vue (focus, HDR, flash, zoom)
├── FingerGuideOverlay.vue
├── QualityFeedback.vue
├── AIGuidanceOverlay.vue
├── CaptureButton.vue
├── CameraService.ts
├── useCamera composable
├── useAIFingerDetection composable
└── MediaPipe integration

[PHASE H] AI Image Processing
├── ImageProcessingPipeline.ts
├── FingerCropProcessor.ts
├── BackgroundRemovalProcessor.ts
├── WhiteBalanceProcessor.ts
├── ContrastProcessor.ts
├── SharpeningProcessor.ts
├── CLAHEProcessor.ts
├── NoiseReductionProcessor.ts
├── RidgeEnhancementProcessor.ts
├── RidgeAnalysisProcessor.ts
├── SkeletonizationProcessor.ts
├── ImageStandardizer.ts
├── ImageExportService.ts
└── AIStore.ts (processing state)

[PHASE I] Image Editor
├── ImageEditorPage.vue
├── EditorToolbar.vue
├── BrightnessContrastPanel.vue
├── ColorAdjustmentPanel.vue
├── FilterPanel.vue
├── TransformPanel.vue
├── BeforeAfterSlider.vue
├── HistoryPanel.vue
├── EditorCanvas.vue
├── useImageEditor composable
├── EditorStore.ts
└── ExportOptions.vue

[PHASE J] AI Enhance & Segmentation
├── AIEnhancePanel.vue
├── OneClickEnhanceButton.vue
├── SegmentationViewer.vue
├── FingerMaskDisplay.vue
├── RidgeMapDisplay.vue
├── ValleyMapDisplay.vue
└── AIDetectionService.ts

[PHASE K] File Management
├── FileManager.vue
├── ImageGallery.vue
├── VersionHistory.vue
├── BackupManager.vue
├── CloudSyncStatus.vue
├── FileService.ts
├── StorageService.ts (Supabase)
└── OfflineStorageService.ts (IndexedDB)

[PHASE L] Reports Module
├── ReportsPage.vue
├── ReportPreview.vue
├── PDFGenerator.ts
├── WordExporter.ts
├── ZIPArchiver.ts
├── ReportTemplates/
├── WatermarkService.ts
└── PrintService.ts

[PHASE M] Search & Filters
├── GlobalSearch.vue
├── AdvancedSearchPanel.vue
├── FilterBuilder.vue
├── SearchService.ts
└── SearchStore.ts

[PHASE N] Admin Module
├── AdminDashboard.vue
├── UserManagementPage.vue
├── RoleManagementPage.vue
├── PermissionMatrix.vue
├── AuditLogViewer.vue
├── SystemSettings.vue
├── DatabaseBackup.vue
└── AdminStore.ts

[PHASE O] Notifications & Sync
├── NotificationCenter.vue
├── ToastContainer.vue
├── SyncStatusIndicator.vue
├── OfflineBanner.vue
├── NotificationService.ts
├── SyncService.ts
└── PWAUpdateNotification.vue

[PHASE P] UI Components Library
├── BottomNavigation.vue
├── FloatingActionButton.vue
├── Card.vue
├── Timeline.vue
├── ImageCompare.vue
├── Carousel.vue
├── Wizard.vue
├── Stepper.vue
├── Modal.vue
├── Drawer.vue
├── BottomSheet.vue
└── MobileButton.vue

[PHASE Q] PWA Configuration
├── manifest.json
├── Service Worker (Workbox)
├── PWAInstallPrompt.vue
├── OfflinePage.vue
├── Cache strategies
└── Push notification setup

[PHASE R] Testing
├── Unit tests (Vitest)
├── Integration tests
├── E2E tests (Playwright)
├── Camera API mocks
├── Image processing tests
└── PWA offline tests
```

### Step 4.3: Post-Implementation Gates

```
[GATE 4] frontend-review (post-review)
├── Check: All pages/components implemented
├── Check: No TODO comments remain
├── Check: Mobile-first responsive design
├── Check: Touch interactions working
├── Check: PWA installable
├── Check: Offline functionality
└── Decision: APPROVE or REQUEST_CHANGES

[GATE 5] security-review (post-review)
├── Check: JWT token security
├── Check: RBAC enforcement
├── Check: XSS/CSRF protection
├── Check: Watermark on exports
├── Check: File checksum
├── Check: Audit logging complete
└── Decision: APPROVE

[GATE 6] web-performance-auditor (post-review)
├── Check: First Contentful Paint < 2s
├── Check: Image compression working
├── Check: Lazy loading implemented
├── Check: Service Worker caching
├── Check: PWA Lighthouse score > 80
└── Decision: APPROVE

[GATE 7] database-reviewer (post-review)
├── Check: Repository pattern implemented
├── Check: Unit of Work pattern
├── Check: Indexes on search columns
├── Check: Data integrity constraints
└── Decision: APPROVE
```

---

## Phase 5: Skill Execution Matrix

| Step | Skills Loaded | Rules Loaded | Output |
|------|--------------|--------------|--------|
| Analysis | `intent-detection` | `task-analyzer`, `skill-registry` | Task Manifest (20+ subtasks) |
| Design | `frontend-taste` | `ui-visual-design`, `frontend-frameworks`, `mobile-first.mdc` | Design Approval |
| Backend | `backend-review` | `backend-frameworks`, `databases`, `auth`, `api-patterns` | API Implementation |
| Frontend Core | `karpathy-coding`, `full-output` | `coding-standards`, `architecture-patterns` | Vue 3 + PWA Core |
| Camera Module | `image-enhancer` | `camera-api.mdc`, `pwa-patterns.mdc` | Camera capture |
| AI Processing | `image-enhancer`, `document-ocr` | `ai-knowledge.mdc`, `llm-providers.mdc` | AI pipeline |
| Editor | `canvas-design` | `ui-visual-design`, `performance.mdc` | Image editor |
| Security | `security-review` | `security.mdc`, `auth.mdc` | Security audit pass |
| Performance | `web-performance-auditor` | `performance.mdc`, `serverless.mdc` | Performance audit pass |
| Database | `database-reviewer` | `databases.mdc`, `multi-tenant.mdc` | DB review pass |
| Final | `code-review` | `testing.mdc`, `deployment.mdc` | Quality Gate Pass |

---

## Phase 6: Technology Stack Mapping

### Frontend Stack
```
Vue 3 + Composition API
├── Vite (build tool)
├── TypeScript (type safety)
├── Tailwind CSS (styling)
│   └── Apple/Material 3/Luxury theme
├── Pinia (state management)
├── Vue Router (navigation)
├── Axios (HTTP client)
├── VueUse (composables)
└── PWA Plugin (vite-plugin-pwa)
```

### Frontend Libraries
```
AI & Image Processing:
├── OpenCV.js (wasm) - fingerprint processing
├── TensorFlow.js - ML inference
├── MediaPipe - finger detection
└── Canvas API - image manipulation

UI Components:
├── Vue transition group
├── Vue window (virtual scroll)
└── Custom components

Storage & Sync:
├── IndexedDB (Dexie.js)
├── Supabase JS Client
└── Workbox (Service Worker)
```

### Backend Stack
```
ASP.NET Core 9 Web API
├── Dapper (micro ORM)
├── SQLite (database)
├── JWT Bearer (authentication)
├── Swagger (API documentation)
├── FluentValidation (DTO validation)
├── Serilog (structured logging)
└── Repository Pattern + Unit of Work
```

### Backend Libraries
```
Image Processing:
├── SkiaSharp (image manipulation)
├── ImageSharp (ASP.NET imaging)
└── PDF generation (QuestPDF)

Security:
├── BCrypt (password hashing)
├── JWT libraries
└── Rate limiting
```

---

## Expected Test Criteria

### Must Pass
- [ ] Task manifest generated with all 20+ subtasks
- [ ] Minimum 18 rules auto-discovered
- [ ] Minimum 10 skills triggered
- [ ] Pre-gate `frontend-taste` executed
- [ ] Pre-gate `Architecture Review` executed
- [ ] Post-gate `frontend-review` executed
- [ ] Post-gate `security-review` executed
- [ ] Post-gate `web-performance-auditor` executed
- [ ] Zero TODO comments in output
- [ ] Zero skeleton placeholders
- [ ] Complete JWT authentication flow
- [ ] Complete 10-finger capture wizard
- [ ] AI image processing pipeline implemented
- [ ] Image editor with all controls
- [ ] PWA installable and offline-capable
- [ ] Dashboard with charts
- [ ] Customer CRUD complete
- [ ] Report generation (PDF/ZIP)
- [ ] Mobile-first responsive design
- [ ] Dark/Light mode toggle
- [ ] Bottom navigation
- [ ] FAB quick actions

### Verification Commands
```bash
# Check TODO count (should be 0)
grep -r "TODO" src/ client/ server/

# Check skeleton count (should be 0)
grep -r "skeleton\|Skeleton" src/

# Verify Vue components
ls -la src/components/ | wc -l
# Expected: > 50 components

# Verify backend controllers
ls -la server/Controllers/
# Expected: > 10 controllers

# Verify services
ls src/services/ | wc -l
# Expected: > 15 services

# Verify stores
ls src/stores/
# Expected: > 10 stores

# PWA verification
npx Lighthouse http://localhost:3000
# Expected PWA score: > 80

# API test
curl http://localhost:5000/swagger
# Expected: Swagger UI loaded

# SQLite database check
sqlite3 app.db ".tables"
# Expected: 12+ tables

# TypeScript check
npx tsc --noEmit
# Expected: 0 errors

# Build test
npm run build
# Expected: Build successful
```

---

## Trace Log Template

```
[TIMESTAMP] INTENT_DETECTED: IMPLEMENT_FULL_STACK_APPLICATION, BIOMETRIC_CRM
[TIMESTAMP] TASK_ANALYZER: Generating manifest...
[TIMESTAMP] MANIFEST_COMPLETE: 20+ subtasks, complexity=ENTERPRISE
[TIMESTAMP] RULES_DISCOVERY: 18+ rules loaded
[TIMESTAMP] SKILLS_DISCOVERY: 10+ skills matched
[TIMESTAMP] PRE_GATE: frontend-taste [EXECUTING]
[TIMESTAMP] PRE_GATE: frontend-taste [APPROVED]
[TIMESTAMP] PRE_GATE: Architecture Review [EXECUTING]
[TIMESTAMP] PRE_GATE: Architecture Review [APPROVED]
[TIMESTAMP] PRE_GATE: AI Integration Plan [EXECUTING]
[TIMESTAMP] PRE_GATE: AI Integration Plan [APPROVED]
[TIMESTAMP] SKILL_LOADED: karpathy-coding
[TIMESTAMP] SKILL_LOADED: full-output
[TIMESTAMP] SKILL_LOADED: frontend-frameworks
[TIMESTAMP] SKILL_LOADED: backend-review
[TIMESTAMP] IMPLEMENTATION_STARTED: Project Foundation
[TIMESTAMP] IMPLEMENTATION_STARTED: Backend API Layer
[TIMESTAMP] IMPLEMENTATION_STARTED: Authentication Module
[TIMESTAMP] IMPLEMENTATION_STARTED: Dashboard Module
[TIMESTAMP] IMPLEMENTATION_STARTED: CRM Customer Module
[TIMESTAMP] IMPLEMENTATION_STARTED: Fingerprint Profile Module
[TIMESTAMP] IMPLEMENTATION_STARTED: Camera Capture Module
[TIMESTAMP] IMPLEMENTATION_STARTED: AI Image Processing
[TIMESTAMP] IMPLEMENTATION_STARTED: Image Editor
[TIMESTAMP] IMPLEMENTATION_STARTED: AI Enhance & Segmentation
[TIMESTAMP] IMPLEMENTATION_STARTED: File Management
[TIMESTAMP] IMPLEMENTATION_STARTED: Reports Module
[TIMESTAMP] IMPLEMENTATION_STARTED: Search & Filters
[TIMESTAMP] IMPLEMENTATION_STARTED: Admin Module
[TIMESTAMP] IMPLEMENTATION_STARTED: Notifications & Sync
[TIMESTAMP] IMPLEMENTATION_STARTED: UI Components Library
[TIMESTAMP] IMPLEMENTATION_STARTED: PWA Configuration
[TIMESTAMP] IMPLEMENTATION_STARTED: Testing
[TIMESTAMP] POST_GATE: frontend-review [EXECUTING]
[TIMESTAMP] POST_GATE: frontend-review [APPROVED]
[TIMESTAMP] POST_GATE: security-review [EXECUTING]
[TIMESTAMP] POST_GATE: security-review [APPROVED]
[TIMESTAMP] POST_GATE: web-performance-auditor [EXECUTING]
[TIMESTAMP] POST_GATE: web-performance-auditor [APPROVED]
[TIMESTAMP] POST_GATE: database-reviewer [EXECUTING]
[TIMESTAMP] POST_GATE: database-reviewer [APPROVED]
[TIMESTAMP] POST_GATE: code-review [EXECUTING]
[TIMESTAMP] POST_GATE: code-review [APPROVED]
[TIMESTAMP] TASK_COMPLETE: All gates passed, 20+ modules implemented
```

---

## Folder Structure Reference

```
/
├── client/                          # Vue 3 Frontend (PWA)
│   ├── src/
│   │   ├── assets/                  # Static assets
│   │   ├── components/               # Reusable components
│   │   │   ├── common/             # Generic UI components
│   │   │   ├── camera/             # Camera capture components
│   │   │   ├── editor/             # Image editor components
│   │   │   ├── crm/               # CRM components
│   │   │   └── dashboard/          # Dashboard components
│   │   ├── composables/            # Vue composables
│   │   ├── layouts/                 # Page layouts
│   │   ├── pages/                  # Route pages
│   │   ├── router/                 # Vue Router config
│   │   ├── services/               # API services
│   │   ├── stores/                 # Pinia stores
│   │   ├── types/                  # TypeScript types
│   │   ├── utils/                  # Utilities
│   │   ├── AI/                     # AI processing modules
│   │   │   ├── opencv/            # OpenCV.js integration
│   │   │   ├── tensorflow/        # TensorFlow.js models
│   │   │   └── mediapipe/         # MediaPipe solutions
│   │   ├── App.vue
│   │   └── main.ts
│   ├── public/
│   ├── index.html
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   └── package.json
│
├── server/                          # ASP.NET Core Backend
│   ├── src/
│   │   └── Api/
│   │       ├── Controllers/        # API Controllers
│   │       ├── Services/           # Business logic
│   │       ├── Repositories/       # Data access
│   │       ├── Entities/          # Domain entities
│   │       ├── DTOs/              # Data transfer objects
│   │       ├── Middleware/        # Custom middleware
│   │       ├── Configuration/     # App settings
│   │       └── Extensions/        # Service extensions
│   ├── tests/                      # Unit tests
│   ├── appsettings.json
│   ├── Program.cs
│   └── Api.csproj
│
├── database/                        # Database scripts
│   ├── migrations/
│   └── seeds/
│
├── docs/                            # Documentation
│   ├── api/
│   ├── deployment/
│   └── guides/
│
├── docker/                          # Docker configuration
├── docker-compose.yml
└── README.md
```

---

## Notes

- **Language**: Vietnamese request → auto-translate to English for processing (multi-language-processing.mdc)
- **Framework**: Auto-detect from requirement - Vue 3 (Frontend) + ASP.NET Core 9 (Backend)
- **Style**: Apple/Material 3/Luxury design via `ui-visual-design.mdc`
- **Mobile First**: All components designed mobile-first, tested on mobile viewport
- **PWA**: Service Worker + Workbox for offline-first experience
- **AI Processing**: Browser-based (OpenCV.js, TensorFlow.js) with optional server fallback
- **Storage**: Local SQLite + Supabase Cloud Storage hybrid
- **Authentication**: JWT with refresh tokens + OTP verification
- **Performance Target**: Lighthouse PWA score > 80, FCP < 2s
