# CI/CD Workflow

> **Version:** 1.0.0 | **Category:** DevOps | **Triggers:** cicd, github actions, deploy, pipeline

---

## Workflow Structure

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Lint
        run: npm run lint

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Test
        run: npm run test:ci

  build:
    needs: [lint, test]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build
        run: npm run build

  deploy-staging:
    if: github.ref == 'refs/heads/develop'
    needs: [build]
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - name: Deploy to Staging
        run: ./deploy.sh staging

  deploy-production:
    if: github.ref == 'refs/heads/main'
    needs: [build]
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Deploy to Production
        run: ./deploy.sh production
```

## Quality Gates

```
┌────────────────────────────────────────────────────────────┐
│ Quality Gates in Pipeline                                   │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Gate 1: Lint & Format                                  │
│  ├── ESLint                                             │
│  ├── Prettier                                           │
│  └── TypeScript strict                                  │
│                                                            │
│  Gate 2: Unit Tests                                     │
│  ├── All tests pass                                     │
│  ├── Coverage > 80%                                     │
│  └── No console.log                                     │
│                                                            │
│  Gate 3: Integration Tests                              │
│  ├── API tests                                          │
│  ├── Database tests                                     │
│  └── Coverage > 50%                                     │
│                                                            │
│  Gate 4: Security Scan                                 │
│  ├── Dependency audit                                  │
│  ├── SAST scan                                         │
│  └── No critical vulnerabilities                        │
│                                                            │
│  Gate 5: Build                                         │
│  ├── Production build successful                        │
│  ├── Bundle size < limit                                │
│  └── No build warnings                                 │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

## GitHub Actions Examples

### Node.js Pipeline

```yaml
name: Node.js CI

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - run: npm ci
      - run: npm run lint
      - run: npm run type-check

  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - run: npm ci
      - run: npm run test:ci
        env:
          DATABASE_URL: postgresql://postgres:test@localhost:5432/test

  build:
    runs-on: ubuntu-latest
    needs: [lint, test]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/
```

### Docker Deploy

```yaml
name: Docker Deploy

on:
  push:
    tags: ['v*']

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Login to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Build and Push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            ghcr.io/${{ github.repository }}:${{ github.ref_name }}
            ghcr.io/${{ github.repository }}:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy:
    runs-on: ubuntu-latest
    needs: [build]
    steps:
      - name: Deploy to Server
        uses: appleboy/ssh-action@v0.1.0
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SERVER_SSH_KEY }}
          script: |
            docker pull ghcr.io/${{ github.repository }}:${{ github.ref_name }}
            docker-compose down
            docker-compose up -d
            docker image prune -f
```

## Environment Variables

```yaml
# Staging
STAGING_DATABASE_URL: postgresql://user:pass@staging-db:5432/app
STAGING_REDIS_URL: redis://staging-redis:6379
STAGING_API_URL: https://api-staging.example.com

# Production
PRODUCTION_DATABASE_URL: postgresql://user:pass@prod-db:5432/app
PRODUCTION_REDIS_URL: redis://prod-redis:6379
PRODUCTION_API_URL: https://api.example.com
```

## Monitoring

```
┌────────────────────────────────────────────────────────────┐
│ Post-Deploy Monitoring                                    │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Metrics:                                                 │
│  ├── Error rate                                          │
│  ├── Response time (p50, p95, p99)                      │
│  ├── Request throughput                                  │
│  └── CPU/Memory usage                                   │
│                                                            │
│  Logs:                                                   │
│  ├── Application logs                                   │
│  ├── Access logs                                        │
│  └── Error logs                                         │
│                                                            │
│  Alerts:                                                 │
│  ├── Error rate > 1%                                    │
│  ├── Response time > 2s p95                            │
│  └── Memory > 80%                                       │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

## Rollback Strategy

```bash
# Rollback to previous version
kubectl rollout undo deployment/app

# Or with Docker
docker-compose down
docker pull ghcr.io/${{ repo }}:previous
docker-compose up -d
```

## Checklist

```
┌─────────────────────────────────────────────────────────────┐
│ CI/CD Checklist                                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ Lint passes                                            │
│ □ Type check passes                                      │
│ □ Unit tests pass                                        │
│ □ Integration tests pass                                 │
│ □ Security scan clean                                    │
│ □ Build successful                                      │
│ □ Deploy to staging verified                             │
│ □ Smoke tests pass                                      │
│ □ Monitoring active                                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```
