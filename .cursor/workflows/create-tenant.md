# Workflow: Create Tenant - Tạo Tenant

## Mục tiêu
Workflow chuẩn để tạo tenant mới trong multi-tenant SaaS.

## Trigger
Khi user yêu cầu tạo tenant mới.

## Workflow Steps

### Bước 1: Provision
- [ ] Create tenant record
- [ ] Setup tenant config
- [ ] Initialize default data

### Bước 2: Configure
- [ ] Setup RLS policies
- [ ] Configure SSO (if needed)
- [ ] Setup billing

### Bước 3: Verify
- [ ] Test tenant isolation
- [ ] Test authentication
- [ ] Verify data access

## Liên kết
- [[../skills/tenant-isolation-review]] - Tenant Isolation
- [[../rules/multi-tenant]] - Multi-Tenant Rules
