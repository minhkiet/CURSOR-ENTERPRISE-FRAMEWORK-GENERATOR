---
title: "Vue Checklist - Danh Sách Kiểm Tra Vue.js"
description: "Danh sách kiểm tra toàn diện cho pre-deployment, code review, và best practices verification trong Vue.js projects"
tags: ["vue", "javascript", "checklist", "deployment", "code-review", "frontend"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Vue Checklist - Danh Sách Kiểm Tra Vue.js

## Tổng Quan

Tài liệu này cung cấp một danh sách kiểm tra toàn diện (comprehensive checklist) cho việc phát triển, code review, và deployment các ứng dụng Vue.js. Checklist được thiết kế để cover mọi aspect của Vue development từ project setup ban đầu cho đến production deployment và monitoring.

Việc sử dụng checklist không chỉ giúp đảm bảo chất lượng code mà còn tạo ra một quy trình standardized cho team, giúp giảm bugs và improve consistency across different developers và projects. Mỗi section trong checklist được phân chia theo functional area và importance level.

Checklist này phù hợp cho cả individual developers muốn ensure quality work và team leads muốn establish quality standards cho entire team. Nó có thể được customize theo specific needs của từng project hoặc organization.

## Mục Đích

Danh sách kiểm tra này được thiết kế với các mục đích chính sau:

1. **Quality Assurance**: Đảm bảo mọi aspects của Vue application đã được properly implemented và tested trước khi release. Quality assurance là một continuous process không chỉ là final step.

2. **Standardization**: Cung cấp một bộ tiêu chuẩn thống nhất cho code review và deployment process. Standardization giúp new team members understand expectations nhanh chóng.

3. **Preventive Check**: Giúp identify potential issues trước khi chúng trở thành production problems. Prevention tốt hơn cure - catching issues early tiết kiệm time và resources.

4. **Knowledge Transfer**: Serving as documentation cho Vue best practices trong team. Checklist có thể được sử dụng như onboarding reference cho new developers.

## Project Setup Checklist

### Environment Configuration

- [ ] **Node.js Version**: Sử dụng Node.js LTS version (18+ for Vue 3 projects). Kiểm tra `.nvmrc` hoặc `engines` field trong `package.json` nếu có team members sử dụng different Node versions.

- [ ] **Package Manager**: Chọn và stick với một package manager (npm, yarn, hoặc pnpm). Document preference trong `CONTRIBUTING.md`. Pnpm được recommend cho Vue projects vì better dependency deduplication và disk space savings.

- [ ] **IDE Setup**: VS Code với Volar extension được cài đặt và configured. Volar provides TypeScript support inside Vue SFCs và là recommended extension cho Vue development.

- [ ] **Git Hooks**: Husky và lint-staged được configured cho pre-commit linting. Git hooks giúp catch issues trước khi code được committed.

- [ ] **Environment Variables**: `.env.example` file được tạo với all required environment variables. Sensitive values không bao giờ được commit vào repository.

### Build Tool Configuration

- [ ] **Vite Configuration**: `vite.config.ts` được properly configured cho project requirements. Bao gồm appropriate aliases, proxy settings cho development, và build optimizations.

- [ ] **TypeScript Configuration**: `tsconfig.json` được set up với strict mode enabled. TypeScript strict mode giúp catch more errors at compile time.

- [ ] **ESLint Configuration**: ESLint với Vue plugin và Prettier được configured. Rules nên align với team conventions và Vue best practices.

- [ ] **Browser Support**: Build target và polyfills được configured cho supported browsers. Kiểm tra `browserslist` configuration.

- [ ] **Path Aliases**: `@/` alias được configured và consistent across all config files (vite, tsconfig, eslint).

### Dependencies Management

- [ ] **Core Dependencies Pinned**: Vue, Vue Router, Pinia versions được pinned trong `package.json`. Sử dụng exact versions hoặc lock files để ensure consistency.

- [ ] **Dev Dependencies Audited**: Regular audit của dev dependencies để identify vulnerabilities. Chạy `npm audit` hoặc equivalent periodically.

- [ ] **Unused Dependencies Removed**: Regular cleanup của unused dependencies. Sử dụng tools như `depcheck` để identify dead weight.

- [ ] **Dependency Versions Compatible**: All dependencies compatible với nhau và Vue version. Kiểm tra peer dependencies requirements.

## Component Development Checklist

### Component Structure

- [ ] **Single-File Component Format**: All components sử dụng SFC format với `<script setup>`, `<template>`, và `<style scoped>`. `<script setup>` là recommended syntax cho Vue 3.

- [ ] **Component Naming Convention**: Components được đặt tên theo PascalCase convention. File names nên match component names (UserCard.vue cho component named UserCard).

- [ ] **Props Type Definition**: All props được defined với proper TypeScript types. Avoid using `any` type - define explicit interfaces.

- [ ] **Emits Type Definition**: All emitted events được properly defined sử dụng `defineEmits` với type syntax. Event names tuân theo kebab-case convention.

- [ ] **Component Documentation**: Complex components có JSDoc comments giải thích purpose và usage. Public component APIs được documented.

### Props Validation

- [ ] **Required Props Marked**: Props that are required được marked với `required: true` trong prop definitions.

- [ ] **Default Values**: Optional props có appropriate default values sử dụng `withDefaults` hoặc `default` property.

- [ ] **Prop Type Validation**: Props có proper type validation for complex objects. Consider using custom validators cho business logic validation.

- [ ] **Props Are Read-Only**: Components không mutate received props directly. Any necessary mutation được handled through emits.

- [ ] **Complex Props Destructured Safely**: Reactive objects được destructured using `toRefs` hoặc accessed directly để preserve reactivity.

### Component Logic

- [ ] **Reactive State Properly Declared**: Sử dụng `ref()` cho primitives và objects được replaced entirely. Sử dụng `reactive()` cho objects được mutated in place.

- [ ] **Computed Properties Used Appropriately**: Derived state được implemented using `computed()` thay vì methods hoặc watchers.

- [ ] **Watchers Have Dependencies**: Watchers chỉ watch specific dependencies và không trigger unnecessary executions.

- [ ] **Lifecycle Hooks Properly Used**: Appropriate lifecycle hooks được used cho side effects và cleanup. `onUnmounted` được used cho cleanup.

- [ ] **No Side Effects in Computed**: Computed properties không contain side effects như API calls hoặc DOM manipulation.

- [ ] **Async Operations Properly Handled**: Async operations được wrapped in try-catch và loading/error states được managed properly.

### Template Best Practices

- [ ] **Keys in v-for**: All `v-for` loops có unique `:key` attributes using stable identifiers. Index không được sử dụng làm key trừ khi absolutely necessary.

- [ ] **Conditional Rendering Optimized**: `v-if` vs `v-show` được chosen appropriately. `v-if` cho content rarely rendered, `v-show` cho content frequently toggled.

- [ ] **Event Handling**: Event handlers được properly bound và cleaned up. Arrow functions không được sử dụng làm event handlers khi `this` context cần thiết.

- [ ] **Dynamic Classes and Styles**: Dynamic classes và styles được properly formatted. Consider extracting to computed properties khi complex.

- [ ] **Template Refs Properly Declared**: Template refs được declared as refs và properly typed. Null checks được performed before accessing refs.

- [ ] **No Inline Functions in Templates**: Complex logic được extracted to methods. Inline functions trong templates có thể cause performance issues.

## State Management Checklist

### Pinia Store Structure

- [ ] **Store Organization**: Stores được organized by domain (user, cart, products) thay vì by type (all state, all getters, all actions). Single responsibility principle được followed.

- [ ] **State Immutability**: Store state không được mutated directly outside of actions. Consider using spread operators hoặc Object.assign for updates.

- [ ] **Getters for Derived State**: Computed derived state được implemented as getters thay vì computed in components accessing raw state.

- [ ] **Actions for Async Operations**: All async operations (API calls) được placed in actions. Actions properly handle loading và error states.

- [ ] **Store Hydration**: Stores properly hydrate from persisted state (localStorage, cookies) on app initialization.

### Store Implementation

- [ ] **TypeScript Types Defined**: Store state, getters, và actions có proper TypeScript types. Avoid `any` types.

- [ ] **State Initialization**: Initial state được properly initialized với appropriate default values.

- [ ] **Error Handling**: Store actions have proper error handling. Error states được exposed for components to handle.

- [ ] **Persistence Strategy**: For persisted stores, appropriate persistence strategy được implemented. Consider encryption cho sensitive data.

- [ ] **Reset Capability**: Stores có ability to reset to initial state. Useful for logout và testing.

### Cross-Component State

- [ ] **Global vs Local State**: Clear distinction giữa state cần global access và state chỉ cần local component scope. Don't over-globalize.

- [ ] **Provide/Inject Usage**: Related state được shared through provide/inject pattern where appropriate, avoiding prop drilling.

- [ ] **Event Bus Not Used**: Components communicate through well-defined patterns (props/emits, provide/inject, store) instead of event buses.

## Vue Router Checklist

### Route Configuration

- [ ] **Lazy Loading**: All routes use dynamic imports for lazy loading. Main routes (landing, login) có thể be eagerly loaded.

- [ ] **Route Meta Types**: Route meta được properly typed. Consider creating a `RouteMeta` interface.

- [ ] **404 Handling**: Catch-all route for 404 được implemented và properly handled.

- [ ] **Route Naming**: All routes có unique names for programmatic navigation.

- [ ] **Route Guards**: Authentication và authorization guards được properly implemented.

### Navigation

- [ ] **Navigation Guards**: Route guards properly redirect unauthorized users và protect sensitive routes.

- [ ] **Query Parameters Handled**: Changes to query parameters được properly handled và don't cause unnecessary reloads.

- [ ] **Route Transitions**: Smooth transitions between routes được implemented. Consider page-level transitions.

- [ ] **Scroll Behavior**: Proper scroll behavior được configured. Scroll to top on navigation hoặc restore scroll position as appropriate.

- [ ] **Breadcrumbs**: Breadcrumb navigation được implemented for nested routes.

## Performance Checklist

### Bundle Optimization

- [ ] **Code Splitting**: Routes được lazy loaded để reduce initial bundle size. Identify và split large dependencies.

- [ ] **Tree Shaking**: Ensure build configuration properly enables tree shaking. Import only what you need.

- [ ] **Bundle Analysis**: Regular bundle size analysis được performed. Use tools like `rollup-plugin-visualizer` hoặc `webpack-bundle-analyzer`.

- [ ] **Chunk Strategy**: Appropriate chunk strategy cho vendor libraries. Consider separating vendor chunks from app chunks.

- [ ] **Dynamic Imports**: Large components được dynamically imported. Use `defineAsyncComponent` where appropriate.

### Rendering Optimization

- [ ] **Component Memoization**: Expensive computations được memoized using `computed()`.

- [ ] **Virtual Scrolling**: Long lists sử dụng virtual scrolling implementation. Libraries như `vue-virtual-scroller` hoặc `@vueuse/core`.

- [ ] **Lazy Components**: Heavy components được lazy loaded và only rendered when needed.

- [ ] **shallowRef Usage**: Large data structures sử dụng `shallowRef` where inner changes don't need deep reactivity.

- [ ] **v-memo Usage**: Repeated elements in `v-for` loops benefit from `v-memo` for conditional memoization.

### Loading Optimization

- [ ] **Skeleton Screens**: Loading states được handled với skeleton screens thay vì spinners where appropriate.

- [ ] **Image Optimization**: Images được lazy loaded, properly sized, và use modern formats (WebP, AVIF). Use `loading="lazy"` attribute.

- [ ] **Preloading**: Critical routes/components được preloaded. Consider resource hints (`<link rel="preload">`).

- [ ] **Service Worker**: Consider implementing service worker for caching và offline support. Nuxt provides built-in PWA module.

## Security Checklist

### Input Handling

- [ ] **XSS Prevention**: User-generated content được sanitized trước khi render. Never use `v-html` với user input without sanitization.

- [ ] **Input Validation**: All form inputs được validated both client-side và server-side. Never trust client-side validation alone.

- [ ] **SQL Injection Prevention**: API calls properly sanitize inputs. Use parameterized queries trong backend.

- [ ] **URL Validation**: Dynamic URLs được validated before use. Prevent open redirect vulnerabilities.

### Authentication & Authorization

- [ ] **Token Storage**: Authentication tokens được stored securely. Consider httpOnly cookies thay vì localStorage for sensitive applications.

- [ ] **Session Expiration**: Sessions properly expire và users được logged out after inactivity.

- [ ] **Permission Checks**: UI elements properly hide based on user permissions. Route guards check permissions before navigation.

- [ ] **Sensitive Data Exposure**: Sensitive data không được logged hoặc exposed in client-side code.

### API Security

- [ ] **HTTPS Only**: All API calls use HTTPS in production.

- [ ] **CORS Configuration**: API properly configured to accept requests only from allowed origins.

- [ ] **Rate Limiting**: API endpoints properly rate limited to prevent abuse.

- [ ] **API Keys Secured**: API keys và secrets được stored as environment variables và not committed to repository.

## Testing Checklist

### Unit Testing

- [ ] **Critical Logic Tested**: Business logic, utilities, và composables có unit tests. Target high coverage cho complex logic.

- [ ] **Test Coverage**: Project has reasonable test coverage (aim for 80%+ for critical paths). Coverage reports được generated và reviewed.

- [ ] **Test Organization**: Tests được organized in parallel structure với source files. Follow consistent naming convention.

- [ ] **Mock Dependencies**: External dependencies (API calls, browser APIs) được properly mocked in tests.

- [ ] **Test Isolation**: Tests are independent và don't rely on execution order. Each test can run in isolation.

### Component Testing

- [ ] **Component Behavior Tested**: Component behavior được tested thay vì implementation details. Test what component does, not how.

- [ ] **User Interactions Tested**: User interactions (clicks, inputs) được tested with proper user simulation.

- [ ] **Edge Cases Covered**: Edge cases và error states được tested. Consider boundary conditions.

- [ ] **Props and Events Tested**: Props validation và event emissions được tested.

- [ ] **Snapshot Tests**: For stable components, snapshot tests help catch unintended changes.

### Integration Testing

- [ ] **Route Integration**: Route navigation được tested. Guards và redirects work correctly.

- [ ] **Store Integration**: Components properly integrate with stores. Store actions trigger expected UI updates.

- [ ] **API Integration**: API calls được mocked và integration tests verify correct data flow.

- [ ] **E2E Tests**: Critical user flows (login, checkout) có E2E tests. Consider Cypress, Playwright, hoặc Vitest.

## Accessibility Checklist

### Semantic HTML

- [ ] **Proper Heading Hierarchy**: Page content uses proper heading hierarchy (h1 → h2 → h3). One h1 per page.

- [ ] **Semantic Elements**: Semantic HTML elements được sử dụng (`<button>`, `<nav>`, `<main>`, `<article>`) thay vì generic `<div>`.

- [ ] **Form Labels**: All form inputs có associated labels. Use `for` attribute hoặc wrap input in label.

- [ ] **Lists**: Lists được marked up as `<ul>`, `<ol>`, hoặc `<dl>` appropriate.

### ARIA Implementation

- [ ] **ARIA Labels**: Interactive elements without visible text có proper `aria-label`.

- [ ] **ARIA Live Regions**: Dynamic content changes được announced using `aria-live` regions where appropriate.

- [ ] **ARIA Roles**: Custom components have appropriate ARIA roles. Don't override native semantics.

- [ ] **Focus Management**: Focus được properly managed for modals, dialogs, và dynamic content.

### Keyboard Navigation

- [ ] **Tab Order**: Tab order is logical và follows visual layout. No positive `tabindex` values.

- [ ] **Focus Indicators**: Keyboard focus is visible. Don't remove default focus outlines without providing alternatives.

- [ ] **Keyboard Operable**: All interactive elements are operable via keyboard. Custom components properly handle keyboard events.

- [ ] **Escape Key**: Modal dialogs và dropdowns close on Escape key press.

### Visual

- [ ] **Color Contrast**: Text có sufficient contrast ratio (4.5:1 for normal text, 3:1 for large text).

- [ ] **Text Resizing**: Content remains readable when text is resized up to 200%.

- [ ] **Motion**: Animations respect `prefers-reduced-motion`. Consider providing reduced motion alternatives.

## Code Quality Checklist

### TypeScript

- [ ] **Strict Mode**: TypeScript strict mode được enabled. All any types được eliminated hoặc justified.

- [ ] **Type Coverage**: High type coverage for component props, emits, và store definitions.

- [ ] **No Type Assertions**: Avoid non-null assertions (`!`) và type assertions (`as any`). Handle types properly.

- [ ] **Interface Naming**: Interfaces được named descriptively (IUser, UserProps) và follow conventions.

- [ ] **Generics Used**: Generic types được used cho reusable components và utilities.

### Code Organization

- [ ] **Composables**: Reusable logic được extracted to composables. Follow `use` naming convention.

- [ ] **Single Responsibility**: Components và functions có single responsibility. Avoid god components.

- [ ] **Import Organization**: Imports được organized (external packages → internal packages → relative imports) và sorted alphabetically within groups.

- [ ] **Constants**: Magic numbers và strings được extracted to constants. Use meaningful names.

- [ ] **Comments**: Code has meaningful comments explaining "why" not "what". Avoid redundant comments.

### Linting

- [ ] **ESLint Passing**: No ESLint errors in project. Warnings được addressed appropriately.

- [ ] **Prettier Formatting**: Code follows Prettier formatting. Pre-commit hooks prevent formatting issues.

- [ ] **Import Order**: Import order follows project conventions. Configure import order in ESLint/Prettier.

- [ ] **Unused Code**: No unused variables, imports, hoặc dead code. Regular cleanup performed.

## Deployment Checklist

### Build Verification

- [ ] **Production Build**: Production build completes successfully without errors. Run `npm run build` và verify output.

- [ ] **Bundle Size**: Bundle size within acceptable limits. Review bundle analyzer output.

- [ ] **Build Warnings**: No significant build warnings. Address any warnings about bundle size hoặc potential issues.

- [ ] **Source Maps**: Source maps được generated for debugging production issues. Consider separate sourcemaps for production.

- [ ] **Environment Variables**: All required environment variables được set in production environment. No hardcoded secrets.

### Deployment Process

- [ ] **Deployment Documentation**: Deployment process được documented. Include rollback procedures.

- [ ] **Zero Downtime**: Deployment strategy supports zero downtime. Consider blue-green deployment hoặc rolling updates.

- [ ] **Health Checks**: Application health endpoints được implemented và monitored.

- [ ] **CDN Configuration**: Static assets được served from CDN. Proper cache headers configured.

- [ ] **Asset Hashing**: Build artifacts có content hashes for cache busting.

### Post-Deployment

- [ ] **Smoke Tests**: Post-deployment smoke tests verify basic functionality. Automated where possible.

- [ ] **Error Monitoring**: Error tracking (Sentry, Datadog) được configured và monitoring active.

- [ ] **Performance Monitoring**: Performance metrics được tracked. Set up alerts for degradation.

- [ ] **Logging**: Application logging properly configured. Logs shipped to centralized logging system.

- [ ] **Rollback Plan**: Rollback procedure được documented và tested. Know how to revert quickly.

## Monitoring Checklist

### Application Monitoring

- [ ] **Error Tracking**: Error tracking service được integrated (Sentry, Bugsnag, hoặc similar). Alerts configured for new errors.

- [ ] **Performance Metrics**: Core Web Vitals và application metrics được tracked. Set baselines và monitor for degradation.

- [ ] **User Analytics**: Analytics tracking implemented for user behavior. Privacy compliance ensured.

- [ ] **Uptime Monitoring**: Uptime monitoring configured. Alerts set for downtime.

### Infrastructure Monitoring

- [ ] **Server Metrics**: CPU, memory, disk usage monitored. Alerts configured for thresholds.

- [ ] **Database Monitoring**: Query performance monitored. Slow queries identified và optimized.

- [ ] **API Monitoring**: API response times and error rates monitored. Third-party API health tracked.

- [ ] **Log Aggregation**: Logs aggregated in centralized system. Structured logging implemented.

## Pre-Release Final Checklist

### Final Quality Gates

- [ ] **All Tests Passing**: 100% of critical tests passing. No known bugs at launch-critical severity.

- [ ] **Security Scan**: Security scan completed. No high/critical vulnerabilities.

- [ ] **Performance Benchmarks**: Performance meets SLAs. Load tested if applicable.

- [ ] **Cross-Browser Testing**: Application tested across supported browsers và devices.

- [ ] **Mobile Testing**: Responsive design verified across device sizes. Touch interactions tested.

### Documentation

- [ ] **README Updated**: Project README current và accurate. Include setup instructions.

- [ ] **API Documentation**: API endpoints documented. Consider OpenAPI/Swagger.

- [ ] **Deployment Runbook**: Runbook documented with common operations và troubleshooting steps.

- [ ] **Changelog**: Changelog prepared for release. Semantic versioning followed.

### Sign-Off

- [ ] **Code Review Complete**: All changes reviewed by at least one other developer.

- [ ] **QA Sign-Off**: QA team has signed off on release candidate.

- [ ] **Product Sign-Off**: Product owner/stakeholder has approved release.

- [ ] **Rollback Plan Ready**: Rollback plan prepared và team knows procedure.

## Daily Development Checklist

### Before Starting Work

- [ ] Pull latest changes from main branch
- [ ] Review any new PRs or changes that might affect your work
- [ ] Run local build to ensure everything compiles
- [ ] Check for any breaking changes in dependencies

### During Development

- [ ] Write tests for new functionality
- [ ] Run linting and fix any issues
- [ ] Verify changes work in development mode
- [ ] Check for any TypeScript errors

### Before Committing

- [ ] Run full test suite
- [ ] Verify no console.log statements left in code
- [ ] Ensure all console.error/warn are intentional
- [ ] Check for any sensitive data accidentally committed
- [ ] Verify build succeeds

### Before Creating PR

- [ ] Rebase on latest main branch
- [ ] Resolve any merge conflicts
- [ ] Update documentation if needed
- [ ] Self-review your changes
- [ ] Ensure PR description is clear and complete

## References

### Vue Official Resources

- Vue 3 Style Guide: https://vuejs.org/style-guide/
- Vue Router Guide: https://router.vuejs.org/
- Pinia Guide: https://pinia.vuejs.org/
- Vue Test Utils Guide: https://test-utils.vuejs.org/

### Tools for Verification

- Vue DevTools: Browser extension for debugging
- Lighthouse: Performance auditing
- axe: Accessibility testing
- ESLint: Code linting
- Vitest: Unit testing

### Further Reading

- Vue.js Security Guide
- Web Performance Guide
- OWASP Top 10

## Kết Luận

Danh sách kiểm tra này cung cấp một comprehensive framework để đảm bảo chất lượng trong Vue development. Tuy nhiên, quan trọng cần nhớ:

1. **Adapt to Your Context**: Không phải item nào cũng applicable cho mọi project. Customize theo your specific needs.

2. **Progressive Application**: Áp dụng checklist progressively. Start với high-impact items và expand over time.

3. **Team Buy-In**: Đảm bảo team members understand và buy-in vào checklist. It works best when everyone follows it.

4. **Continuous Improvement**: Regular review và update checklist based on lessons learned từ projects.

5. **Automation**: Automate wherever possible. CI/CD pipelines nên enforce many of these checks automatically.

Sử dụng checklist này consistently sẽ help maintain high quality standards và reduce bugs trong Vue applications của bạn.
