# Git Workflow

> **Version:** 1.0.0 | **Category:** Version Control

---

## Tổng quan

Quy ước Git workflow đảm bảo team làm việc nhất quán, dễ theo dõi và review.

---

## 1. Branch Strategy

### 1.1 Branch Naming

```
┌────────────────────────────────────────────────────────────┐
│ Branch Naming Convention                                     │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  feature/{ticket-id}-short-description                     │
│  ├── feature/ABC-123-add-user-auth                        │
│  ├── feature/ABC-456-fix-login-bug                        │
│  └── feature/ABC-789-improve-performance                  │
│                                                            │
│  fix/{ticket-id}-short-description                        │
│  ├── fix/ABC-100-fix-memory-leak                         │
│  └── fix/ABC-101-correct-tax-calculation                  │
│                                                            │
│  chore/{description}                                      │
│  ├── chore/update-dependencies                            │
│  └── chore/refactor-user-service                          │
│                                                            │
│  docs/{description}                                       │
│  ├── docs/update-api-documentation                        │
│  └── docs/add-deployment-guide                            │
│                                                            │
│  refactor/{description}                                    │
│  ├── refactor/extract-payment-service                     │
│  └── refactor/cleanup-database-queries                    │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### 1.2 Branch Types

| Type | Purpose | Lifespan |
|------|---------|----------|
| `main`/`master` | Production-ready code | Forever |
| `develop` | Integration branch (optional) | Forever |
| `feature/*` | New features | Until PR merged |
| `fix/*` | Bug fixes | Until PR merged |
| `hotfix/*` | Urgent production fixes | Until PR merged |
| `release/*` | Release preparation | Until released |

---

## 2. Commit Messages

### 2.1 Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### 2.2 Types

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code change, no feature/fix |
| `test` | Adding/updating tests |
| `chore` | Maintenance tasks |
| `perf` | Performance improvement |
| `ci` | CI/CD changes |
| `revert` | Revert previous commit |

### 2.3 Examples

```
# Good commit messages
feat(auth): add JWT refresh token rotation

Implement refresh token rotation for improved security.
- Rotate refresh token on each use
- Store token hash in database
- Invalidate old tokens after rotation

Closes ABC-123
```

```
fix(payment): correct tax calculation for EU countries

The previous implementation was using the wrong tax rate
for B2B transactions in Germany. This fix applies the
correct reverse charge mechanism.

Fixes ABC-456
```

```
chore(deps): upgrade express from 4.17.1 to 4.18.0

Changelog: https://github.com/expressjs/express/blob/master/History.md
```

### 2.4 Rules

```
┌────────────────────────────────────────────────────────────┐
│ Commit Message Rules                                        │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ✓ Use imperative mood ("add" not "added")                │
│  ✓ First line under 72 characters                          │
│  ✓ Reference ticket numbers in footer                     │
│  ✓ Explain "why" not "what" in body                       │
│  ✓ Separate subject from body with blank line             │
│  ✗ Don't end subject with period                          │
│  ✗ Don't use vague messages like "fix stuff"              │
│  ✗ Don't submit without testing                            │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## 3. Pull Request Workflow

### 3.1 Before Opening PR

```
□ Code follows style guidelines
□ Tests added/updated
□ Documentation updated
□ Branch is up-to-date with target
□ No merge conflicts
□ Self-review done
```

### 3.2 PR Description Template

```markdown
## Summary
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How was this tested?

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code where needed
- [ ] I have updated documentation
- [ ] My changes generate no new warnings
- [ ] Tests pass locally
- [ ] Related ticket is linked

## Screenshots (if applicable)
```

### 3.3 PR Size Guidelines

| Size | Lines Changed | Recommendation |
|------|---------------|----------------|
| XS | 1-10 | ✅ Ideal |
| S | 11-50 | ✅ Good |
| M | 51-200 | ⚠️ Consider splitting |
| L | 201-500 | ⚠️ Needs justification |
| XL | 500+ | ❌ Split required |

---

## 4. Merging Strategy

### 4.1 Merge Options

| Strategy | When to Use |
|----------|-------------|
| **Merge commit** | Regular feature branches |
| **Squash merge** | Small fix PRs, maintain clean history |
| **Rebase** | Keeping linear history, cleaning up commits |

### 4.2 Decision Tree

```
┌────────────────────────────────────────────────────────────┐
│ When to use which merge strategy?                          │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Feature branch with messy commits?                        │
│  └── Squash merge                                          │
│                                                            │
│  Multiple logical commits that should be separate?         │
│  └── Rebase + Merge commit                                │
│                                                            │
│  Small fix with single logical change?                      │
│  └── Squash merge                                          │
│                                                            │
│  Long-running branch with multiple contributors?           │
│  └── Merge commit                                          │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### 4.3 Merge Checklist

```
□ PR approved by required reviewers
□ All CI checks pass
□ No merge conflicts (or conflicts resolved)
□ Commits are clean and meaningful
□ Tags/releases updated if needed
□ CHANGELOG updated if needed
```

---

## 5. Tagging & Releases

### 5.1 Semantic Versioning

```
v{major}.{minor}.{patch}
 │      │     │
 │      │     └── Patch: Bug fixes, no API changes
 │      └────────── Minor: New features, backward compatible
 └───────────────── Major: Breaking changes
```

### 5.2 Tag Format

```bash
# Annotated tag (recommended)
git tag -a v1.2.3 -m "Release v1.2.3: Add user authentication"

# Lightweight tag
git tag v1.2.3

# Push tag
git push origin v1.2.3
```

### 5.3 Release Process

```bash
# 1. Update version in code
# 2. Update CHANGELOG.md
# 3. Commit changes
git add -A && git commit -m "chore: prepare v1.2.3 release"

# 4. Create and push tag
git tag -a v1.2.3 -m "Release v1.2.3: Add user authentication"
git push origin v1.2.3

# 5. GitHub Actions will:
#    - Create GitHub Release
#    - Build and publish artifacts
#    - Update package registry if applicable
```

---

## 6. .gitignore Template

```gitignore
# Dependencies
node_modules/
vendor/
.venv/

# Build outputs
dist/
build/
*.tsbuildinfo

# Environment
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
npm-debug.log*

# Test coverage
coverage/

# Secrets
*.pem
*.key
credentials.json
secrets.yaml
```

---

## 7. Git Hooks

### 7.1 Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Run lint
npm run lint
if [ $? -ne 0 ]; then
  echo "Lint failed"
  exit 1
fi

# Run tests
npm run test
if [ $? -ne 0 ]; then
  echo "Tests failed"
  exit 1
fi
```

### 7.2 Commit-msg Hook

```bash
#!/bin/bash
# .git/hooks/commit-msg

commit_msg=$(cat "$1")
pattern="^(feat|fix|docs|style|refactor|test|chore|perf|ci|revert)(\(.+\))?: .{1,72}"

if ! [[ $commit_msg =~ $pattern ]]; then
  echo "Invalid commit message format"
  echo "Expected: type(scope): subject"
  echo "Types: feat, fix, docs, style, refactor, test, chore, perf, ci, revert"
  exit 1
fi
```

---

## Nguồn tham khảo

- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Semantic Versioning](https://semver.org/)
