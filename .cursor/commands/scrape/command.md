# Command: /scrape - Web Content Extraction

## Mô tả
Duyệt web và trích xuất nội dung kỹ thuật từ documentation sites sử dụng Playwright.

## Trigger Keywords
- `/scrape` - Bắt đầu scrape
- `/extract` - Trích xuất nội dung
- `/docs` - Lấy documentation

## Categories có thể extract

| Category | Mô tả | Nội dung |
|----------|--------|----------|
| `sdk` | SDK Requirements | Installation, config, dependencies, authentication |
| `api` | API Documentation | Endpoints, schemas, request/response formats |
| `ui` | UI Specifications | Components, layouts, color schemes, responsive |
| `test` | Testing Documentation | Test cases, strategies, benchmarks |
| `qc` | QC Specifications | Acceptance criteria, bug severity, release criteria |

## Usage Examples

```
/scrape https://docs.example.com/sdk sdk,api
/scrape https://api.example.com docs sdk,api,test
/extract https://github.com/org/repo/wiki sdk
/docs https://stripe.com/docs sdk,api,test
```

## Command Prompt

```
# Task: Web Content Extraction

Hãy sử dụng Playwright để duyệt và trích xuất nội dung kỹ thuật từ URLs được cung cấp.

## URLs cần scrape:
{urls}

## Categories cần extract:
{categories}

## Workflow thực hiện:

### 1. Setup Playwright CLI
\`\`\`bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export PWCLI="$CODEX_HOME/skills/playwright/scripts/playwright_cli.sh"
\`\`\`

### 2. Navigate và Survey
- Mở từng URL
- Lấy table of contents
- Identify sections cần extract

### 3. Extract theo Category

**SDK Requirements:**
- Installation commands
- Dependencies
- Environment variables
- Configuration options

**API Documentation:**
- Endpoints và methods
- Request/Response schemas
- Authentication flows
- Error codes

**UI Specifications:**
- Component specs
- Color/typography
- Responsive breakpoints

**Testing Documentation:**
- Test cases
- Setup requirements
- Benchmarks

**QC Specifications:**
- Acceptance criteria
- Bug severity
- Release criteria

### 4. Save Output
Lưu vào `.cursor/knowledge/{domain}/` theo cấu trúc phù hợp.

## Deliverables:
- Tất cả extracted content dưới dạng markdown
- Screenshots nếu cần verify
- Structured data (JSON) nếu có
```

## Related
- [[../workflows/web-content-extraction]] - Web Content Extraction Workflow
- [[../skills/playwright-web-scraper]] - Playwright Web Scraper Skill
- [[../skills/sdk-technical-extraction]] - SDK Technical Extraction Skill
