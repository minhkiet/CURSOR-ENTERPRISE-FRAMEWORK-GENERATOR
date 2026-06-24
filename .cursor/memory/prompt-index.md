# Prompt Index - Chỉ mục Prompt

## Mô tả
Danh mục tất cả prompt templates trong framework, giúp AI agent nhanh chóng tìm và reuse prompt phù hợp.

## Prompt Categories

### Development Prompts
| ID | Tên file | Mục đích | Last Used |
|----|----------|----------|-----------|
| DEV-001 | bug-fix | Sửa lỗi bug | - |
| DEV-002 | feature-build | Xây dựng feature mới | - |
| DEV-003 | refactor | Refactor code | - |
| DEV-004 | code-review | Review code | - |
| DEV-005 | test-build | Viết unit test | - |

### Architecture Prompts
| ID | Tên file | Mục đích | Last Used |
|----|----------|----------|-----------|
| ARCH-001 | architecture-review | Review kiến trúc | - |
| ARCH-002 | ddd-design | Thiết kế DDD | - |
| ARCH-003 | cqrs-implementation | Implement CQRS | - |
| ARCH-004 | api-design | Thiết kế API | - |
| ARCH-005 | database-design | Thiết kế database | - |

### Security Prompts
| ID | Tên file | Mục đích | Last Used |
|----|----------|----------|-----------|
| SEC-001 | security-audit | Audit bảo mật | - |
| SEC-002 | vulnerability-scan | Scan lỗ hổng | - |
| SEC-003 | penetration-test | Penetration test | - |

### Performance Prompts
| ID | Tên file | Mục đích | Last Used |
|----|----------|----------|-----------|
| PERF-001 | performance-audit | Audit hiệu năng | - |
| PERF-002 | database-optimization | Tối ưu database | - |
| PERF-003 | cache-strategy | Chiến lược cache | - |
| PERF-004 | frontend-optimization | Tối ưu frontend | - |

### AI/RAG Prompts
| ID | Tên file | Mục đích | Last Used |
|----|----------|----------|-----------|
| AI-001 | rag-design | Thiết kế RAG | - |
| AI-002 | vector-search | Vector search | - |
| AI-003 | embedding-strategy | Chiến lược embedding | - |

### Domain Prompts
| ID | Tên file | Mục đích | Last Used |
|----|----------|----------|-----------|
| DOM-001 | bazi-calculation | Tính Bát Tự | - |
| DOM-002 | tuvi-calculation | Tính Tử Vi | - |
| DOM-003 | numerology-calculation | Tính Thần Số | - |
| DOM-004 | pdf-generation | Generate PDF | - |
| DOM-005 | crm-setup | Setup CRM | - |
| DOM-006 | billing-setup | Setup Billing | - |

### Infrastructure Prompts
| ID | Tên file | Mục đích | Last Used |
|----|----------|----------|-----------|
| INF-001 | deployment | Deployment | - |
| INF-002 | docker-build | Docker build | - |
| INF-003 | kubernetes-deploy | K8s deploy | - |
| INF-004 | monitoring-setup | Setup monitoring | - |

## Prompt Hash Index
```
hash(prompt_content) → prompt_id → usage_count → last_used
```

## Usage Statistics
- **Total prompts**: 30
- **Most used**: (none yet)
- **Cache hit rate target**: > 80%
