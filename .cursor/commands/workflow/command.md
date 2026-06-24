---
description: Workflow - Execute standard workflows
trigger: workflow, quy trình, execute workflow, standard workflow, process
category: Workflow
framework: Cursor Enterprise Framework V4
version: 1.0.0
---

# Command: /workflow

## Mục tiêu
Execute các standard workflows được định nghĩa trong framework.

## Trigger Keywords
- workflow
- quy trình
- execute workflow
- standard workflow
- process
- theo quy trình
- follow workflow

## Available Workflows

| Workflow | File | Mô tả |
|----------|------|--------|
| build-feature | [[../workflows/build-feature]] | Xây dựng feature mới |
| fix-bug | [[../workflows/fix-bug]] | Sửa lỗi bug |
| review-code | [[../workflows/review-code]] | Review code |
| review-security | [[../workflows/review-security]] | Security review |
| optimize-performance | [[../workflows/optimize-performance]] | Performance optimization |
| deployment | [[../workflows/deployment]] | Deployment workflow |
| build-rag | [[../workflows/build-rag]] | Xây dựng RAG system |
| generate-pdf | [[../workflows/generate-pdf]] | Generate PDF |
| create-tenant | [[../workflows/create-tenant]] | Create new tenant |
| create-report | [[../workflows/create-report]] | Create report |

## Usage
```
/workflow <workflow-name>

Examples:
/workflow build-feature
/workflow fix-bug
/workflow review-security
```

## Liên kết
- [[../workflows/]] - Workflows Directory
- [[../prompts/]] - Prompts Directory
