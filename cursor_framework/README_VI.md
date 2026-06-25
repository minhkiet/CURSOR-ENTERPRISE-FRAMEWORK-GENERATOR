# Cursor Enterprise Framework - Python Library

Thư viện Python toàn diện hỗ trợ các rules và skills của Cursor Enterprise Framework.

## Tính năng

- **Context Router**: Phân loại intent và định tuyến skill thông minh
- **Memory Manager**: Quản lý context theo nguyên tắc Memory First
- **Token Optimizer**: Tối ưu hóa sử dụng token cho LLM
- **Skill Discovery**: Tự động phát hiện và tải skills
- **Code Review**: Tiện ích review code cho frontend
- **Rules/Skills Parser**: Parse và validate các file .mdc

## Cài đặt

```bash
pip install -r requirements.txt
```

## Sử dụng nhanh

```python
from cursor_framework import ContextRouter, MemoryManager, SkillDiscovery

# Định tuyến request đến skill phù hợp
router = ContextRouter()
route = router.route("Tạo landing page cho sản phẩm SaaS")
print(f"Skill: {route.skill.value}, Độ tin cậy: {route.confidence}")

# Quản lý context với memory
memory = MemoryManager()
memory.store("project_info", {"name": "myapp"}, tier=MemoryTier.SESSION)
context = memory.retrieve("project_info")

# Phát hiện skills áp dụng
discovery = SkillDiscovery()
skills = discovery.detect_skills("Build landing page với full implementation")
print(f"Skills phát hiện: {[s.skill for s in skills]}")
```

## Cấu trúc Module

### Module Cốt lõi

| Module | Mô tả |
|--------|--------|
| `context_router` | Phân loại intent và định tuyến skill |
| `memory_manager` | Quản lý context theo nguyên tắc Memory First |
| `token_optimizer` | Tối ưu hóa sử dụng token |
| `skill_discovery` | Phát hiện và tải skills tự động |

### Module Tiện ích

| Module | Mô tả |
|--------|--------|
| `utils/text_utils` | Xử lý văn bản |
| `utils/file_utils` | Thao tác file |
| `utils/code_utils` | Phân tích code |
| `utils/http_utils` | HTTP request helpers |
| `utils/security_utils` | Bảo mật |

## Tích hợp Framework

Thư viện này được thiết kế để làm việc với các rules và skills của Cursor Enterprise Framework:

- **133 files rules** bao gồm các patterns kiến trúc enterprise
- **Skills** cho frontend, security, testing, và nhiều hơn nữa
- **Pre-review và post-review gates** để đảm bảo chất lượng

## License

MIT
