# Cursor Enterprise Framework - Hooks
# Tự động trigger khi xảy ra sự kiện trong Git, CI/CD, hoặc development workflow

## Giới thiệu

Hooks là các script tự động trigger khi xảy ra sự kiện trong:
- **Git hooks** (pre-commit, pre-push, etc.)
- **CI/CD hooks** (GitHub Actions, GitLab CI, etc.)
- **Development hooks** (pre-build, post-deploy, etc.)
- **Cursor hooks** (before-task, after-task, etc.)

## Danh sách Hooks

### Git Hooks
| Hook | Trigger | Mô tả |
|------|---------|--------|
| [[git-hooks/pre-commit]] | Trước commit | Lint, format, type check |
| [[git-hooks/commit-msg]] | Sau khi viết message | Validate commit message format |
| [[git-hooks/pre-push]] | Trước push | Chạy tests, security scan |
| [[git-hooks/post-commit]] | Sau commit | Update session summary |
| [[git-hooks/post-checkout]] | Sau checkout | Update workspace context |
| [[git-hooks/pre-rebase]] | Trước rebase | Kiểm tra conflicts |

### CI/CD Hooks
| Hook | Trigger | Mô tả |
|------|---------|--------|
| [[ci-cd-hooks/pre-build]] | Trước build | Verify dependencies |
| [[ci-cd-hooks/post-build]] | Sau build | Verify artifacts |
| [[ci-cd-hooks/pre-deploy]] | Trước deploy | Final checks |
| [[ci-cd-hooks/post-deploy]] | Sau deploy | Health check, notify |
| [[ci-cd-hooks/on-failure]] | Khi CI/CD fail | Analyze error, suggest fix |

### Development Hooks
| Hook | Trigger | Mô tả |
|------|---------|--------|
| [[dev-hooks/before-task]] | Trước task | Load context, check memory |
| [[dev-hooks/after-task]] | Sau task | Update memory, summarize |
| [[dev-hooks/on-error]] | Khi có error | Analyze, suggest fix |

## Cách cài đặt

1. Copy hook files vào thư mục `.git/hooks/`
2. Hoặc sử dụng `command-registry.ps1` để tự động setup

## Thêm Hook mới

1. Tạo file hook trong thư mục phù hợp
2. Cập nhật README này
3. Update `command-registry.ps1`
