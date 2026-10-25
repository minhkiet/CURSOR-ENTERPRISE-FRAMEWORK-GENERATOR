---
name: "source-command-clone-command"
description: "Migrated source command `clone-command`"
---

# source-command-clone-command

Use this skill when the user asks to run the migrated source command `clone-command`.

## Command Template

# Command: /clone - Website Cloning

## Mô tả
Clone một website hoàn chỉnh về cả giao diện và chức năng sử dụng Playwright. Tạo bản sao pixel-perfect với tất cả interactive elements, responsive behavior, và functionality được preserved.

## Trigger Keywords
- `/clone` - Bắt đầu clone website
- `/copy` - Copy website
- `/mirror` - Mirror website

## Usage Examples

```
/clone https://example.com
/clone https://stripe.com --full
/clone https://github.com --test
```

## Command Options

| Option | Description | Example |
|--------|-------------|---------|
| URL | Website URL cần clone | `https://example.com` |
| `--full` | Clone toàn bộ pages | Clone tất cả linked pages |
| `--test` | Test sau khi clone | Run verification tests |
| `--ui` | UI only (no JS) | Static HTML/CSS only |
| `--interactive` | Preserve all JS | Full functionality clone |

## Clone Workflow

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│  Discovery  │───▶│  Extraction  │───▶│  Analysis   │
│  Phase      │    │  Phase       │    │  Phase      │
└─────────────┘    └──────────────┘    └─────────────┘
                                                │
                                                ▼
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│  Verify     │◀───│  Fix Issues  │◀───│  Testing    │
│  Phase      │    │  Phase       │    │  Phase      │
└─────────────┘    └──────────────┘    └─────────────┘
```

## Command Prompt

```
# Task: Website Cloning

Clone website {url} thành bản sao hoàn chỉnh với:
1. UI/Visual giống bản gốc
2. Functionality hoạt động đầy đủ
3. Responsive behavior đúng
4. Assets (images, fonts) được download

## Target URL
{url}

## Clone Options
{options}

## Workflow:

### 1. Discovery Phase
- Open URL in Playwright
- Detect technology stack (React, Vue, Angular, etc.)
- Identify CSS framework (Tailwind, Bootstrap, etc.)
- Map navigation structure
- Inventory all resources

### 2. Extraction Phase
- Extract full HTML structure
- Extract CSS (inline + external)
- Extract JavaScript (inline + external)
- Download images/assets
- Identify interactive elements
- Capture screenshots at multiple viewports

### 3. Analysis Phase
- Analyze component structure
- Identify breakpoints
- Map API endpoints (if any)
- Document form behaviors
- Identify animation/interaction patterns

### 4. Cloning Phase
- Create project structure
- Generate HTML with preserved structure
- Generate CSS with all styles
- Generate JavaScript for functionality
- Download and organize assets
- Ensure responsive breakpoints work

### 5. Testing Phase (if --test)
- Visual comparison with original
- Test all navigation links
- Test all forms
- Test interactive elements
- Test responsive at all breakpoints
- Generate test report

## Deliverables:
- Clone project tại `.cursor/clones/{domain}/`
- Full HTML/CSS/JS implementation
- All assets downloaded
- Test report (if --test)
- Screenshots comparison
```

## Output Structure

```
.cursor/clones/{domain}/
├── index.html
├── css/
│   ├── main.css
│   ├── components.css
│   └── responsive.css
├── js/
│   ├── main.js
│   └── utils.js
├── assets/
│   ├── images/
│   ├── fonts/
│   └── icons/
├── test-report.md
└── README.md
```

## Clone Quality Levels

| Level | Description | Use Case |
|-------|-------------|----------|
| **UI Only** | Static HTML/CSS, no JS | Landing pages, blogs |
| **Basic** | HTML/CSS + basic JS | Simple interactions |
| **Interactive** | Full JS preserved | Forms, modals, animations |
| **Full Clone** | Everything + testing | Complete web apps |

## Known Limitations

- **Authentication-gated content**: Cannot clone behind login
- **Server-rendered content**: May need API simulation
- **WebGL/Canvas**: Complex graphics may not clone perfectly
- **Third-party embeds**: External widgets may not work
- **Dynamic content**: Real-time data may not be captured

## Related

- [[../skills/web-cloner]] - Web Cloner Skill
- [[../skills/web-clone-tester]] - Web Clone Tester Skill
- [[../skills/playwright-web-scraper]] - Web Scraper Skill
