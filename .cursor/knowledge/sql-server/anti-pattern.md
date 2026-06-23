# SQL Server Anti-Patterns - Các Mẫu Cần Tránh

## Anti-Patterns

### 1. No Indexes

**Mô tả**: Table không có indexes.

**Giải pháp**: Index foreign keys, frequently queried columns.

### 2. SELECT *

**Mô tả**: Sử dụng SELECT *.

**Giải pháp**: Select only needed columns.

### 3. Cursors

**Mô tả**: Overusing cursors.

**Giải pháp**: Use set-based operations.

### 4. Implicit Conversions

**Mô tả**: Data type mismatches.

**Giải pháp**: Match data types.

## Kết luận

Tránh các anti-patterns này giúp SQL Server performance tốt hơn.
