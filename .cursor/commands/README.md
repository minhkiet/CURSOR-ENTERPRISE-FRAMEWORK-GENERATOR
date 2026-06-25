# Cursor Commands Registry
# Tự động load bởi Cursor IDE
# Framework: Cursor Enterprise Framework V4

## Giới thiệu

Commands là các slash commands cho Cursor IDE. Mỗi command được định nghĩa trong thư mục riêng với:
- `command.md` - Mô tả command và trigger keywords
- `prompt.md` - Prompt template cho command

## Danh sách Commands

| Command | Category | Mô tả |
|---------|----------|--------|
| `/build` | Development | Xây dựng feature mới |
| `/fix` | Development | Sửa lỗi bug |
| `/review` | Quality | Review code |
| `/audit` | Quality | Audit code (security, performance, architecture) |
| `/design` | Architecture | Thiết kế (DDD, CQRS, Database) |
| `/rag` | AI | Xây dựng RAG system |
| `/deploy` | DevOps | Deployment workflow |
| `/test` | Testing | Chiến lược testing |
| `/doc` | Documentation | Tạo tài liệu |
| `/memory` | Memory | Quản lý memory system |
| `/adr` | Architecture | Tạo ADR (Architecture Decision Record) |
| `/payment` | Domain | Review payment integration Việt Nam |
| `/security` | Security | Security review |
| `/frontend` | Frontend | Frontend tasks (build, redesign, review) |
| `/perf` | Performance | Performance audit |
| `/refactor` | Refactoring | Refactor code |
| `/generate` | Generation | Generate code (PDF, API, migration) |
| `/workflow` | Workflow | Execute standard workflow |
| `/report` | Reporting | Tạo report |
| `/bazi` | Domain | Tính Bát Tự |
| `/tuvi` | Domain | Tính Tử Vi |
| `/numerology` | Domain | Thần Số Học |
| `/scrape` | Data | Web scraping và content extraction |

## Cách sử dụng

1. Gõ `/` trong Cursor chat để hiển thị danh sách commands
2. Chọn command phù hợp với task
3. Mô tả chi tiết yêu cầu sau command

## Thêm Command mới

1. Tạo thư mục mới trong `.cursor/commands/<command-name>/`
2. Tạo file `command.md` với mô tả
3. Tạo file `prompt.md` với prompt template
4. Cập nhật registry này
