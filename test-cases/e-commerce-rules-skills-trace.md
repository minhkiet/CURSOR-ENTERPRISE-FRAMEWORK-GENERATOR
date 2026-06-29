# Test Case: E-commerce Implementation - Rules/Skills Reasoning Trace

## Requirement
> "Implement đầy đủ một trang e-commerce với product listing, cart, checkout. Không skeleton, không TODO, full code."

---

## Phase 1: Intent Detection & Task Analysis

### Step 1.1: Intent Detection (intent-detection.mdc)
```
Input: "Implement đầy đủ một trang e-commerce với product listing, cart, checkout..."

Intent Classification:
├── Primary Intent: IMPLEMENT_FEATURE
├── Domain: E-COMMERCE
├── Complexity: HIGH (multi-page, stateful, transactional)
└── Urgency: STANDARD

Detected Keywords:
- "e-commerce" → maps to crm-saas.mdc, enterprise-patterns.mdc
- "product listing" → frontend requirements
- "cart, checkout" → state management, transaction flow
- "full code, no skeleton" → triggers full-output skill
```

### Step 1.2: Task Analyzer (task-analyzer.mdc)
```
Task Manifest Generation:
Task: E-Commerce Full Implementation

Subtasks:
[1] Product Listing Page
    - Grid/List view product cards
    - Filtering & sorting
    - Search functionality
    - Pagination or infinite scroll

[2] Shopping Cart
    - Add/remove/update quantities
    - Price calculation
    - Persistent cart state
    - Cart summary sidebar

[3] Checkout Flow
    - Cart review
    - Shipping address form
    - Payment integration placeholder
    - Order confirmation

[4] Supporting Components
    - Header with cart badge
    - Product detail modal/page
    - Toast notifications
    - Loading states (non-skeleton)

Estimated Complexity: 8-12 hours
Framework: Vue 3 / Nuxt 3 (based on existing ArchitectureSection.vue)
```

---

## Phase 2: Rules Auto-Discovery

### Step 2.1: Primary Rules Selection

| Rule | Trigger Reason | Load Order |
|------|---------------|------------|
| `task-analyzer.mdc` | Universal task analysis | 1st |
| `frontend-frameworks.mdc` | Vue/Nuxt project detected | 2nd |
| `architecture-patterns.mdc` | E-commerce needs clean separation | 3rd |
| `api-patterns.mdc` | Product/cart APIs needed | 4th |
| `ui-visual-design.mdc` | UI implementation required | 5th |
| `coding-standards.mdc` | Code consistency | 6th |
| `testing.mdc` | Post-implementation testing | 7th |

### Step 2.2: Domain-Specific Rules

| Rule | Trigger Reason |
|------|---------------|
| `crm-saas.mdc` | E-commerce patterns (orders, customers) |
| `auth.mdc` | User authentication for checkout |
| `databases.mdc` | Product/Cart data storage |
| `multi-tenant.mdc` | If multi-vendor platform |

---

## Phase 3: Skills Auto-Discovery

### Step 3.1: Pre-Implementation Skills (skill-registry.mdc)

| Skill | Confidence | Trigger |
|-------|------------|---------|
| `karpathy-coding` | 95% | "full code, no skeleton" - vibe coding approach |
| `ponytail` | 70% | Senior dev minimal approach, YAGNI |
| `full-output` | 99% | Explicitly requested "không TODO, full code" |
| `frontend-frameworks` | 90% | Vue 3 project detected |

### Step 3.2: Quality Gate Skills

| Skill | Gate Type | Purpose |
|-------|-----------|---------|
| `frontend-review` | POST-GATE | Review UI implementation quality |
| `frontend-taste` | PRE-GATE | Ensure design aesthetic |
| `security-review` | POST-GATE | Payment/checkout security |

---

## Phase 4: Execution Flow

### Step 4.1: Pre-Implementation Gates

```
[GATE 1] frontend-taste (pre-review)
├── Check: Design system consistency
├── Check: Component library usage
└── Decision: APPROVE or REQUEST_CHANGES

[GATE 2] Architecture Review
├── Check: Clean Architecture applied
├── Check: Component structure
└── Decision: PROCEED
```

### Step 4.2: Implementation Phase

```
[PHASE A] Core Data Layer
├── Database schema (Supabase/postgres)
├── Product API endpoints
├── Cart state management (Pinia/localStorage)
└── Type definitions

[PHASE B] Product Listing
├── ProductCard.vue
├── ProductGrid.vue
├── ProductFilters.vue
├── ProductSearch.vue
└── ProductService.ts

[PHASE C] Shopping Cart
├── CartStore.ts (Pinia)
├── CartSidebar.vue
├── CartItem.vue
├── CartSummary.vue
└── Cart persistence (localStorage/API)

[PHASE D] Checkout Flow
├── CheckoutPage.vue
├── AddressForm.vue
├── PaymentStep.vue
├── OrderConfirmation.vue
└── OrderService.ts

[PHASE E] Integration
├── Header with cart badge
├── Toast notifications
├── Error handling
└── Loading states
```

### Step 4.3: Post-Implementation Gates

```
[GATE 3] frontend-review (post-review)
├── Check: All components implemented
├── Check: No TODO comments remain
├── Check: Responsive design
├── Check: Accessibility
└── Decision: APPROVE or REQUEST_CHANGES

[GATE 4] security-review (post-review)
├── Check: Payment form XSS protection
├── Check: CSRF tokens
└── Decision: APPROVE
```

---

## Phase 5: Skill Execution Matrix

| Step | Skills Loaded | Rules Loaded | Output |
|------|--------------|--------------|--------|
| Analysis | `intent-detection` | `task-analyzer`, `skill-registry` | Task Manifest |
| Design | `frontend-taste` | `ui-visual-design`, `frontend-frameworks` | Design Approval |
| Code | `karpathy-coding`, `full-output`, `ponytail` | `coding-standards`, `architecture-patterns` | Full Implementation |
| Review | `frontend-review` | `testing`, `security` | Quality Gate Pass |

---

## Expected Test Criteria

### Must Pass
- [ ] Task manifest generated with all 4 subtasks
- [ ] Minimum 6 rules auto-discovered
- [ ] Minimum 4 skills triggered
- [ ] Pre-gate `frontend-taste` executed
- [ ] Post-gate `frontend-review` executed
- [ ] Zero TODO comments in output
- [ ] Zero skeleton placeholders
- [ ] Full CRUD for cart operations
- [ ] Complete checkout flow

### Verification Commands
```bash
# Check TODO count (should be 0)
grep -r "TODO" src/

# Check skeleton count (should be 0)  
grep -r "skeleton" src/

# Verify component count
ls -la src/components/ | wc -l
# Expected: > 10 components

# Verify store files
ls src/stores/
# Expected: cart.ts, product.ts
```

---

## Trace Log Template

```
[10:53:00] INTENT_DETECTED: IMPLEMENT_FEATURE, E-COMMERCE
[10:53:01] TASK_ANALYZER: Generating manifest...
[10:53:02] MANIFEST_COMPLETE: 4 subtasks, complexity=HIGH
[10:53:02] RULES_DISCOVERY: 7 rules loaded
[10:53:03] SKILLS_DISCOVERY: 4 skills matched
[10:53:03] PRE_GATE: frontend-taste [EXECUTING]
[10:53:05] PRE_GATE: frontend-taste [APPROVED]
[10:53:05] SKILL_LOADED: karpathy-coding
[10:53:05] SKILL_LOADED: full-output
[10:53:06] IMPLEMENTATION_STARTED: Product Listing
[10:53:XX] IMPLEMENTATION_STARTED: Shopping Cart
[10:53:XX] IMPLEMENTATION_STARTED: Checkout Flow
[10:53:XX] IMPLEMENTATION_STARTED: Supporting Components
[10:54:XX] POST_GATE: frontend-review [EXECUTING]
[10:54:XX] POST_GATE: frontend-review [APPROVED]
[10:54:XX] TASK_COMPLETE: All gates passed
```

---

## Notes

- Language: Vietnamese request → auto-translate to English for processing (multi-language-processing.mdc)
- Framework: Auto-detect from existing file `ArchitectureSection.vue` (Vue 3)
- Style: Use existing design system from `ui-visual-design.mdc`
- Persistence: Cart should persist (localStorage + API sync)
