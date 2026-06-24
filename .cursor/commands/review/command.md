---
description: Review Code - Review code quality, correctness, performance
trigger: review code, code review, review, kiểm tra code, review pr, pull request review
category: Quality
framework: Cursor Enterprise Framework V4
version: 1.0.0
---

# Command: /review

## Mục tiêu
Review code quality, correctness, performance, và security.

## Trigger Keywords
- review code
- code review
- review
- kiểm tra code
- review pr
- pull request review
- xem lại code
- check code

## Workflow

### Bước 1: Pre-Review
- [ ] Load code-review skill
- [ ] Identify files to review
- [ ] Load relevant rules (coding-standards, architecture)
- [ ] Load relevant knowledge

### Bước 2: Code Review
Apply frontend-review skill nếu là frontend:
- [ ] Correctness: syntax, types, imports
- [ ] Design: design patterns, component structure
- [ ] Accessibility: WCAG AA, ARIA
- [ ] Performance: bundle size, lazy loading
- [ ] State: loading, empty, error states

Apply backend/database rules nếu là backend:
- [ ] API design: REST/GraphQL conventions
- [ ] Data handling: validation, serialization
- [ ] Error handling: proper error types
- [ ] Performance: query optimization, caching
- [ ] Security: input validation, auth, secrets

### Bước 3: Multi-Layer Review
- [ ] Correctness review
- [ ] Design & architecture review
- [ ] Security review
- [ ] Performance review
- [ ] Testing review

### Bước 4: Report
- [ ] Summarize findings
- [ ] Prioritize issues (critical/major/minor)
- [ ] Provide recommendations
- [ ] Provide fix suggestions

## Liên kết
- [[../workflows/review-code]] - Review Code Workflow
- [[../prompts/code-review]] - Code Review Prompt
- [[../skills/code-review]] - Code Review Skill
- [[../rules/coding-standards]] - Coding Standards
