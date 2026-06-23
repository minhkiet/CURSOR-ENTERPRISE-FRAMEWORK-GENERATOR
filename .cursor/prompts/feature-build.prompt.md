# Prompt: Feature Build - Xây dựng Feature

## Mô tả
Prompt template chuẩn để xây dựng feature mới trong Cursor Enterprise Framework.

## Trigger Keywords
- "tạo feature"
- "build feature"
- "implement feature"
- "xây dựng"
- "phát triển"

## Prompt Template

```markdown
# Feature Build Workflow

## 1. FEATURE INFORMATION
- **Feature ID**: [FEATURE-ID]
- **Tên feature**: [Tên feature]
- **Mô tả**: [Mô tả ngắn gọn]
- **Domain**: [Xác định domain]
- **Priority**: [Critical / High / Medium / Low]

## 2. REQUIREMENTS ANALYSIS
```
Đọc knowledge domain liên quan:
- knowledge/[domain]/*
- rules/[domain]/*
Load business-rules.json cho domain
Skip: Tất cả domain không liên quan
```

### Functional Requirements
1. [FR-001]: [Mô tả]
2. [FR-002]: [Mô tả]
3. [FR-003]: [Mô tả]

### Non-Functional Requirements
- Performance: [Yêu cầu]
- Security: [Yêu cầu]
- Scalability: [Yêu cầu]

## 3. ARCHITECTURE DESIGN

### Bước 1: Check ADR
- [ ] Check decisions.sqlite cho existing decisions
- [ ] Check architecture-history/
- [ ] Tạo ADR mới nếu cần

### Bước 2: Design
- [ ] Thiết kế data model
- [ ] Thiết kế API endpoints
- [ ] Thiết kế component structure
- [ ] Xác định dependencies

### Bước 3: Architecture Pattern
- [ ] Clean Architecture
- [ ] DDD approach
- [ ] CQRS nếu cần
- [ ] Event-driven nếu cần

## 4. IMPLEMENTATION WORKFLOW

### Step 1: Setup
```
- Clone repository
- Install dependencies
- Setup development environment
- Run existing tests
```

### Step 2: Database (nếu cần)
- [ ] Tạo migration
- [ ] Run migration
- [ ] Verify schema

### Step 3: Backend
- [ ] Implement domain layer
- [ ] Implement application layer
- [ ] Implement infrastructure layer
- [ ] Implement API endpoints
- [ ] Write unit tests

### Step 4: Frontend (nếu cần)
- [ ] Create components
- [ ] Implement state management
- [ ] Connect to API
- [ ] Write tests

## 5. IMPLEMENTATION CHECKLIST

### Code Quality
- [ ] TypeScript strict mode
- [ ] ESLint passed
- [ ] Prettier formatted
- [ ] Unit tests > 80% coverage

### Security
- [ ] Input validation
- [ ] Output sanitization
- [ ] Authentication check
- [ ] Authorization check
- [ ] Rate limiting

### Performance
- [ ] Database indexes
- [ ] Caching strategy
- [ ] Lazy loading
- [ ] Code splitting

## 6. OUTPUT FORMAT

### Feature Summary
```
Feature: [Tên]
Status: [In Progress / Completed]
Domain: [Domain]
Stack: [Tech stack]
```

### Files Created/Modified
```
Created:
  - [file1]
  - [file2]

Modified:
  - [file3]
  - [file4]
```

### API Endpoints
```
POST   /api/[resource]     - Create
GET    /api/[resource]     - List
GET    /api/[resource]/:id - Get
PUT    /api/[resource]/:id - Update
DELETE /api/[resource]/:id - Delete
```

## 7. LIÊN KẾT
- [[../skills/feature-builder]] - Feature Builder
- [[../skills/code-review]] - Code Review
- [[../rules/ddd]] - DDD Rules
- [[../rules/cqrs]] - CQRS Rules
- [[../rules/clean-architecture]] - Clean Architecture
