# Release Workflow

> **Version:** 1.0.0 | **Category:** Workflow | **Steps:** 7

---

## Purpose

Workflow chuẩn để release phiên bản mới.

## Prerequisites

```
□ Tất cả features đã merged
□ Tất cả tests passed
□ Tất cả bugs đã fix
□ Stakeholders đã approve
```

## Steps

### Step 1: Prepare Release

```
┌────────────────────────────────────────────────────────────┐
│ Step 1: Prepare Release                                  │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  1. Update version                                       │
│     - Semantic versioning (major.minor.patch)            │
│     - Update CHANGELOG.md                               │
│     - Update package.json / build.gradle                 │
│                                                            │
│  2. Freeze code                                          │
│     - Không merge features mới                          │
│     - Chỉ merge hotfixes                                │
│                                                            │
│  Gate: Code freeze approved?                             │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Step 2: QA Testing

```
┌────────────────────────────────────────────────────────────┐
│ Step 2: QA Testing                                        │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  1. Regression testing                                   │
│     - Chạy full test suite                              │
│     - Manual testing key flows                           │
│                                                            │
│  2. Performance testing                                   │
│     - Load testing                                       │
│     - Security testing                                   │
│                                                            │
│  Gate: QA sign-off?                                     │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Step 3: Build Artifacts

```
┌────────────────────────────────────────────────────────────┐
│ Step 3: Build Artifacts                                   │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  1. Build production artifacts                           │
│     - Frontend bundle                                   │
│     - Backend binaries / containers                       │
│     - Database migrations                                │
│                                                            │
│  2. Sign artifacts                                       │
│     - Code signing                                       │
│     - Checksum verification                              │
│                                                            │
│  Gate: Build successful?                                 │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Step 4: Deploy to Staging

```
┌────────────────────────────────────────────────────────────┐
│ Step 4: Deploy to Staging                               │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  1. Deploy to staging environment                        │
│     - Blue-green deployment                             │
│     - Feature flags ready                               │
│                                                            │
│  2. Smoke testing                                       │
│     - Verify deployment works                           │
│     - Check critical paths                              │
│                                                            │
│  Gate: Staging verified?                                 │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Step 5: Deploy to Production

```
┌────────────────────────────────────────────────────────────┐
│ Step 5: Deploy to Production                            │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  1. Schedule deployment                                 │
│     - Low traffic window                               │
│     - Team available for support                        │
│                                                            │
│  2. Execute deployment                                 │
│     - Blue-green or canary                             │
│     - Monitor closely                                  │
│                                                            │
│  Gate: Production verified?                             │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Step 6: Post-Release Monitoring

```
┌────────────────────────────────────────────────────────────┐
│ Step 6: Post-Release Monitoring                         │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  1. Monitor metrics                                    │
│     - Error rates                                      │
│     - Latency                                         │
│     - User complaints                                  │
│                                                            │
│  2. Rollback if needed                                 │
│     - Criteria for rollback                            │
│     - Rollback procedure                                │
│                                                            │
│  Gate: No critical issues after 24h?                    │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Step 7: Communicate

```
┌────────────────────────────────────────────────────────────┐
│ Step 7: Communicate                                       │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  1. Release notes                                        │
│     - What changed                                      │
│     - How to use new features                           │
│     - Known issues                                      │
│                                                            │
│  2. Notify stakeholders                                  │
│     - Team                                              │
│     - Users                                            │
│     - Support team                                     │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

## Checklist

```
Pre-Release:
□ Version updated
□ CHANGELOG updated
□ Code frozen
□ QA sign-off obtained

Build:
□ Production build successful
□ Artifacts signed
□ Deployment to staging verified

Deploy:
□ Production deployment successful
□ Smoke tests passed
□ Monitoring active

Post-Release:
□ No critical issues after 24h
□ Release notes published
□ Stakeholders notified
□ Documentation updated
```

## Rollback Criteria

```
□ Error rate > 5% (10x normal)
□ Latency > 2s p99
□ Critical feature broken
□ Security vulnerability introduced
□ Data corruption detected
```

## Deployment Options

| Strategy | Use Case | Risk |
|----------|----------|------|
| **Blue-Green** | Zero downtime | Medium |
| **Canary** | Gradual rollout | Low |
| **Rolling** | Incremental | Medium |
| **Big Bang** | Fast, risky | High |
