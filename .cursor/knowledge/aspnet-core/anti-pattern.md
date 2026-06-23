# ASP.NET Core Anti-Patterns - Các Mẫu Cần Tránh

## Giới thiệu

Tài liệu này liệt kê các anti-patterns phổ biến trong ASP.NET Core development.

## Anti-Patterns

### 1. Synchronous I/O

**Mô tả**: Sử dụng synchronous methods.

**Giải pháp**: Use async/await throughout.

### 2. Large Controllers

**Mô tả**: Logic quá nhiều trong controllers.

**Giải pháp**: Move logic vào Services.

### 3. Ignoring Health Checks

**Mô tả**: Không implement health checks.

**Giải phól**: Implement proper health checks.

### 4. Hard-coded Values

**Mô tả**: Hard-coded connection strings, secrets.

**Giải pháp**: Use configuration, secrets.

## Kết luận

Tránh các anti-patterns này giúp code tốt hơn.
