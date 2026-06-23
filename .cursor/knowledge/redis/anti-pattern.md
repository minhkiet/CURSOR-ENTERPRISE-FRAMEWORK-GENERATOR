# Redis Anti-Patterns - Các Mẫu Cần Tránh

## Anti-Patterns

### 1. Keys Without TTL

**Mô tả**: Keys không expire.

**Giải pháp**: Always set TTL.

### 2. Large Values

**Mô tả**: Store large values.

**Giải pháp**: Keep values small.

## Kết luận

Tránh các anti-patterns này giúp Redis performance tốt hơn.
