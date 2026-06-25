# Workflow: Web Content Extraction - Trích xuất Nội dung Web

## Mục tiêu
Workflow chuẩn để duyệt web và trích xuất nội dung kỹ thuật (SDK, API, UI, Testing, QC) sử dụng Playwright.

## Trigger
Khi user yêu cầu:
- Scrape nội dung từ một hoặc nhiều URLs
- Thu thập documentation về SDK/API
- Lấy specifications về UI/Giao diện
- Trích xuất tài liệu testing/QC

## Prerequisites

1. **Kiểm tra Playwright CLI available:**
   ```bash
   command -v npx >/dev/null 2>&1
   ```

2. **Setup wrapper script:**
   ```bash
   export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
   export PWCLI="$CODEX_HOME/skills/playwright/scripts/playwright_cli.sh"
   ```

## Workflow Steps

### Bước 1: Analyze Request Scope

Xác định scope của extraction:

| Category | Mô tả | Examples |
|----------|-------|----------|
| **SDK Requirements** | Thông tin cài đặt, dependencies, config | Installation, env vars, version requirements |
| **API Documentation** | Endpoints, schemas, authentication | REST APIs, GraphQL, SDK methods |
| **UI Specifications** | Giao diện, components, layouts | Color schemes, responsive, accessibility |
| **Testing Documentation** | Test cases, strategies, benchmarks | Unit tests, E2E, performance |
| **QC Specifications** | Quality control, acceptance criteria | Bug severity, release criteria, SLA |

**Ghi nhận deliverables count:** __ items

### Bước 2: Setup Output Structure

Tạo thư mục output:
```
.cursor/knowledge/{domain}/
├── sdk-requirements.md
├── api-documentation.md
├── ui-specifications.md
├── testing-documentation.md
└── qc-specifications.md
```

### Bước 3: Navigate và Survey Pages

```bash
# Mở trang chính
"$PWCLI" open https://target-docs-site.com

# Snapshot để có refs
"$PWCLI" snapshot

# Lấy page metadata
"$PWCLI" eval "document.title"
"$PWCLI" eval "window.location.href"

# Lấy tất cả navigation links
"$PWCLI" eval "Array.from(document.querySelectorAll('a[href]')).map(a => ({text: a.textContent.trim(), href: a.href})).filter(l => l.href.startsWith('http'))"
```

### Bước 4: Extract Content theo Category

#### SDK Requirements Extraction

```bash
# Tìm và extract SDK section
"$PWCLI" click e5  # Navigate to SDK section
"$PWCLI" snapshot

# Lấy installation instructions
"$PWCLI" eval "document.querySelector('main').textContent"

# Lấy code examples
"$PWCLI" eval "Array.from(document.querySelectorAll('pre code')).map(c => c.textContent)"

# Extract configuration options
"$PWCLI" eval "JSON.stringify(Array.from(document.querySelectorAll('table')).map(t => ({headers: Array.from(t.querySelectorAll('th')).map(h => h.textContent), rows: Array.from(t.querySelectorAll('tr')).map(r => Array.from(r.querySelectorAll('td')).map(d => d.textContent))}))))"
```

#### API Documentation Extraction

```bash
# Navigate to API section
"$PWCLI" click e7
"$PWCLI" snapshot

# Extract endpoints
"$PWCLI" eval "JSON.stringify(Array.from(document.querySelectorAll('[class*=endpoint], [class*=path]')).map(el => ({method: el.textContent.split(' ')[0], path: el.textContent.split(' ').slice(1).join(' ')})))"

# Extract request/response schemas
"$PWCLI" eval "Array.from(document.querySelectorAll('pre')).map(p => p.textContent)"

# Screenshot để verify
"$PWCLI" screenshot
```

#### UI Specifications Extraction

```bash
# Navigate to UI/Guidelines section
"$PWCLI" click e10
"$PWCLI" snapshot

# Extract color/text specs
"$PWCLI" eval "Array.from(document.querySelectorAll('[class*=color], [class*=palette]')).map(el => el.textContent)"

# Extract spacing/layout specs
"$PWCLI" eval "Array.from(document.querySelectorAll('[class*=spacing], [class*=grid]')).map(el => el.textContent)"

# Screenshot for visual reference
"$PWCLI" screenshot
```

#### Testing Documentation Extraction

```bash
# Navigate to Testing/QA section
"$PWCLI" click e12
"$PWCLI" snapshot

# Extract test cases
"$PWCLI" eval "Array.from(document.querySelectorAll('li, tr')).map(el => el.textContent)"

# Extract setup instructions
"$PWCLI" eval "document.querySelector('main').innerText"

# Screenshot
"$PWCLI" screenshot
```

#### QC Specifications Extraction

```bash
# Navigate to QC/Release section
"$PWCLI" click e14
"$PWCLI" snapshot

# Extract acceptance criteria
"$PWCLI" eval "Array.from(document.querySelectorAll('[class*=criterion], [class*=requirement]')).map(el => el.textContent)"

# Extract bug severity definitions
"$PWCLI" eval "document.querySelector('main').innerText"
```

### Bước 5: Multi-Page Traversal (Optional)

```bash
# Lấy tất cả sub-page links
LINKS=$("$PWCLI" eval "Array.from(document.querySelectorAll('nav a')).map(a => a.href)")
echo "$LINKS"

# Duyệt từng link
for link in $LINKS; do
    "$PWCLI" tab-new "$link"
    "$PWCLI" snapshot
    "$PWCLI" screenshot
    # Extract content
    "$PWCLI" eval "document.body.innerText"
    "$PWCLI" tab-close
done
```

### Bước 6: Save và Format Output

```bash
# Tạo markdown output
cat > ".cursor/knowledge/{domain}/sdk-requirements.md" << 'EOF'
# SDK Requirements

## Installation

## Configuration

## Dependencies

## Authentication
EOF

# Tương tự cho các category khác...
```

### Bước 7: Verification

- [ ] Tất cả URLs đã được duyệt
- [ ] Nội dung đã được extract đầy đủ
- [ ] Screenshots đã được capture
- [ ] Output files đã được format đúng
- [ ] Không có placeholder content

## Output Templates

### SDK Requirements Template

```markdown
# SDK Requirements - {SDK Name}

## Overview
{Mô tả tổng quan về SDK}

## Installation

### Package Manager
```bash
{npm/yarn/pnpm install commands}
```

### Peer Dependencies
{List các dependencies cần thiết}

## Configuration

### Environment Variables
| Variable | Description | Required |
|----------|-------------|----------|
| VAR_NAME | Description | Yes/No |

### Config Options
{Configuration code examples}

## Version Requirements
{Versions compatibility matrix}

## Authentication
{Authentication setup instructions}
```

### API Documentation Template

```markdown
# API Documentation - {API Name}

## Base URL
`{base_url}`

## Authentication
{Auth method và headers}

## Endpoints

### GET /resource
**Description:** {Mô tả endpoint}

**Parameters:**
| Name | Type | Location | Description |
|------|------|----------|-------------|
| param | string | query | Description |

**Response:**
```json
{
  "field": "description"
}
```

**Errors:**
| Code | Message | Description |
|------|---------|-------------|
| 400 | Bad Request | Invalid parameters |
```

### Testing Documentation Template

```markdown
# Testing Documentation - {Feature}

## Test Strategy
{Mô tả chiến lược testing}

## Test Types
- Unit Tests
- Integration Tests
- E2E Tests

## Test Cases

### TC-001: {Test Case Name}
- **Preconditions:** {Conditions trước khi test}
- **Steps:** {Các bước thực hiện}
- **Expected:** {Kết quả mong đợi}

## Setup Requirements
{Environment setup cho testing}
```

## Error Handling

| Issue | Solution |
|-------|----------|
| Page không load | Reload và snapshot lại |
| Element not found | Snapshot để refresh refs |
| Content truncated | Scroll và eval lại |
| Navigation fail | Dùng direct URL với tab-new |

## Related

- [[../skills/playwright-web-scraper]] - Playwright Web Scraper Skill
- [[../skills/knowledge-compiler]] - Knowledge Compiler Skill
- [[../rules/coding-standards]] - Coding Standards
