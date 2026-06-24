---
description: On-Failure Hook - Analyze error và suggest fix khi CI/CD fail
trigger: CI/CD failure, build fail, deploy fail, test fail
framework: Cursor Enterprise Framework V4
version: 1.0.0
---

# Hook: on-failure

## Mục tiêu
Analyze CI/CD failure và provide actionable fix suggestions.

## Trigger
Tự động trigger khi CI/CD pipeline fail.

## Workflow

### Bước 1: Error Collection
- [ ] Collect error logs
- [ ] Collect CI/CD output
- [ ] Identify failure stage
- [ ] Extract error messages

### Bước 2: Error Analysis
- [ ] Parse error type
- [ ] Identify root cause
- [ ] Check for known error patterns
- [ ] Categorize error

### Bước 3: Fix Suggestions
- [ ] Look up fix in knowledge base
- [ ] Check for similar past failures
- [ ] Generate fix suggestions
- [ ] Prioritize fixes

### Bước 4: Notification
- [ ] Send failure notification
- [ ] Include error summary
- [ ] Include fix suggestions
- [ ] Include runbook link

### Bước 5: Auto-Retry (optional)
- [ ] Check if retryable
- [ ] Apply potential fixes
- [ ] Retry if appropriate
- [ ] Report retry status

## Error Categories
| Category | Common Causes | Fix Approach |
|----------|--------------|--------------|
| Build | Dependency issue, config error | Fix dependencies, config |
| Test | Code bug, test flakiness | Fix code, fix tests |
| Deploy | Network, permissions | Check permissions, retry |
| Security | Vulnerability, secrets | Fix security issues |
| Config | Missing env, wrong config | Set env vars, fix config |

## Exit Codes
- `0`: Analysis complete
- `1`: Critical failure - escalate

## Liên kết
- [[../rules/ci-cd]] - CI/CD Rules
- [[../rules/incident-response]] - Incident Response Rules
- [[../skills/root-cause-analysis]] - Root Cause Analysis Skill
