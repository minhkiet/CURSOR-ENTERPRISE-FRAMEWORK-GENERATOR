# Prompt: Code Review - Review Code

```markdown
# Code Review Workflow

## 1. REVIEW SCOPE
- **Scope**: [Full PR / Module / File / Component]
- **Language**: [TypeScript / PHP / C# / Python]
- **Focus**: [Quality / Security / Performance / All]

## 2. CONTEXT LOADING
```
Load knowledge:
- knowledge/[language]/*
- knowledge/[framework]/*
Load rules: coding-standards.mdc
```

## 3. REVIEW AREAS

### Code Quality
- [ ] Naming conventions
- [ ] Code structure
- [ ] DRY principle
- [ ] SOLID principles
- [ ] Error handling

### Security
- [ ] Input validation
- [ ] SQL injection
- [ ] XSS prevention
- [ ] Authentication
- [ ] Authorization

### Performance
- [ ] Database queries
- [ ] Memory usage
- [ ] Algorithmic efficiency
- [ ] Caching

### Testing
- [ ] Test coverage
- [ ] Test quality
- [ ] Edge cases

## 4. FINDINGS

### Must Fix
| ID | Issue | File | Line |
|----|-------|------|------|

### Should Fix
| ID | Issue | File | Line |
|----|-------|------|------|

### Consider
| ID | Issue | File | Line |
|----|-------|------|------|

## 5. LIÊN KẾT
- [[../skills/code-review]] - Code Review Skill
- [[../rules/coding-standards]] - Coding Standards
```
