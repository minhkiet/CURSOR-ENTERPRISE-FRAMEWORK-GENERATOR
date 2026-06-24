# Business Rules - Quy tắc nghiệp vụ

## Mô tả
Lưu trữ các quy tắc nghiệp vụ đặc thù của từng domain, giúp AI agent hiểu rõ business logic trước khi implement.

## CRM SaaS Multi Tenant

### Tenant Management
- [ ] Mỗi tenant phải có unique identifier
- [ ] Tenant data phải được isolate hoàn toàn
- [ ] Cross-tenant access phải được authorize rõ ràng
- [ ] Tenant có thể upgrade/downgrade subscription
- [ ] Tenant có thể export toàn bộ data

### User Management
- [ ] User chỉ thuộc về một tenant
- [ ] User có role: owner, admin, manager, member, viewer
- [ ] Permission được define theo role
- [ ] User có thể thuộc nhiều workspace

### Billing Rules
- [ ] Billing theo tenant, không theo user
- [ ] Hỗ trợ monthly và annual billing cycle
- [ ] Automatic retry cho failed payment
- [ ] Prorated upgrade/downgrade
- [ ] Dunning management cho overdue payment

## AI SaaS

### RAG Pipeline
- [ ] Document ingestion → Chunking → Embedding → Vector Store
- [ ] Chunk size: 512-1024 tokens tùy use case
- [ ] Overlap between chunks: 10-20%
- [ ] Hybrid search: vector + keyword
- [ ] Reranking sau retrieval

### AI Model Selection
- [ ] GPT-4o cho complex reasoning tasks
- [ ] GPT-4o-mini cho simple tasks
- [ ] Gemini cho long context
- [ ] Claude cho creative tasks
- [ ] Local Ollama cho privacy-sensitive

## Bát Tự (Four Pillars of Destiny)

### Tứ trụ (Four Pillars)
- [ ] Năm sinh (Year Pillar): Can Chi của năm
- [ ] Tháng sinh (Month Pillar): Can Chi của tháng
- [ ] Ngày sinh (Day Pillar): Can Chi của ngày
- [ ] Giờ sinh (Hour Pillar): Can Chi của giờ

### Ngũ hành (Five Elements)
- [ ] Mộc (Wood): 甲, 乙
- [ ] Hỏa (Fire): 丙, 丁
- [ ] Thổ (Earth): 戊, 己
- [ ] Kim (Metal): 庚, 辛
- [ ] Thủy (Water): 壬, 癸

### Cung mệnh (Fate Palaces)
- [ ] 12 cung mệnh: Mệnh, Phụ Mẫu, Phúc Đức, Quan Tài, Tam Tai, Tài Bạch, Thiên Di, Nạp Âm, Tướng, Tài, Phú
- [ ] Xác định cung an theo ngày sinh
- [ ] Xác định sao chiếu theo năm

### Vận trình (Life Cycles)
- [ ] 10 đại vận, mỗi vận 10 năm
- [ ] Lưu niên vận: 1 năm
- [ ] Xác định vận theo năm sinh

## Tử Vi (Chinese Fortune Telling)

### Lá số (Natal Chart)
- [ ] 12 cung: Mệnh, Phụ Mẫu, Điền Trạch, Quan Lộc, Phúc Đức, Thân, Tài Bạch, Thiên Di, Nạp Âm, Tướng, Tài, Phú
- [ ] 12 điền: Dần, Mão, Thìn, Tỵ, Ngọ, Mùi, Thân, Dậu, Tuất, Hợi, Tý, Sửu
- [ ] Xác định điền an theo giờ sinh

### Sao chiếu (Stars)
- [ ] 14 chính tinh: Thiên Lương, Vũ Khúc, Thái Dương, Thái Âm, Liêm Trinh, Thiên Cơ, Tham Lang, Cự Môn, Văn Xương, Văn Khúc, Lộc Tồn, Khoa Duyệt, Tướng Quân, Hữu Bật
- [ ] 6XQ: Xấu, Kiến, Trung, Đắc, Hưng, Vượng
- [ ] Xác định sao an theo ngày, giờ, cung

## Thần Số Học (Numerology)

### Số chủ đạo (Life Path Number)
- [ ] Tính tổng ngày sinh, rút gọn về 1-9 hoặc 11, 22, 33
- [ ] 1: Leadership, Independence
- [ ] 2: Diplomacy, Cooperation
- [ ] 3: Expression, Creativity
- [ ] 4: Practicality, Foundation
- [ ] 5: Freedom, Change
- [ ] 6: Responsibility, Service
- [ ] 7: Analysis, Spirituality
- [ ] 8: Power, Abundance
- [ ] 9: Completion, Wisdom
- [ ] 11: Master number, Intuition
- [ ] 22: Master number, Master Builder
- [ ] 33: Master number, Master Teacher

### Số linh hồn (Soul Urge Number)
- [ ] Tính từ nguyên âm trong tên
- [ ] Inner desire và motivation

### Số nhân cách (Personality Number)
- [ ] Tính từ phụ âm trong tên
- [ ] Cách người khác nhìn nhận

## PDF Report

### Template System
- [ ] Template được define bằng HTML/CSS hoặc React components
- [ ] Hỗ trợ variable interpolation
- [ ] Hỗ trợ conditional rendering
- [ ] Hỗ trợ loop qua data array

### Generation Pipeline
- [ ] Input: Template ID + Data JSON
- [ ] Process: Render HTML → Convert to PDF
- [ ] Output: PDF binary hoặc file path
- [ ] Storage: Local filesystem hoặc S3/R2

## ERP / HRM

### Employee Management
- [ ] Mỗi employee có unique employee ID
- [ ] Employee có department và position
- [ ] Employee có reporting line (manager)
- [ ] Employee có employment status: active, terminated, on-leave

### Payroll Rules
- [ ] Payroll calculation dựa trên salary + allowances - deductions
- [ ] Tax calculation theo tax brackets
- [ ] Pay frequency: monthly, bi-weekly, weekly
- [ ] Generate payslip PDF

## E-Commerce

### Product Catalog
- [ ] Product có SKU (unique)
- [ ] Product có multiple variants (size, color)
- [ ] Product có inventory quantity
- [ ] Product có pricing tiers

### Order Management
- [ ] Order có unique order number
- [ ] Order status: pending, confirmed, shipped, delivered, cancelled
- [ ] Order có line items
- [ ] Order có shipping address và billing address

## Multi-Tenant Isolation

### Row Level Security (RLS)
- [ ] PostgreSQL RLS cho Supabase
- [ ] tenant_id column trên mọi tenant-scoped table
- [ ] Enable RLS trên tất cả tables
- [ ] Policy: users chỉ thấy data của tenant họ

### Schema Isolation
- [ ] Alternative: Separate schema per tenant
- [ ] Pros: Stronger isolation
- [ ] Cons: Migration complexity

### Discriminator Column
- [ ] Single database, single schema
- [ ] tenant_id discriminator column
- [ ] Application-level filter
- [ ] RLS enforcement

## Liên kết
- [[project-index]] - Project Index
- [[context-router]] - Context Router
- [[../rules/multi-tenant]] - Multi-Tenant Rules
- [[../rules/crm-saas]] - CRM SaaS Rules
- [[../rules/billing]] - Billing Rules
