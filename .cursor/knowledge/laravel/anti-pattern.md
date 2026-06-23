# Laravel Anti-Patterns - Các Mẫu Cần Tránh

## Giới thiệu

Tài liệu này liệt kê các anti-patterns phổ biến trong Laravel development.

## Anti-Patterns

### 1. Fat Controllers

**Mô tả**: Logic quá nhiều trong controllers.

**Giải pháp**: Move logic vào Services/Repositories.

### 2. N+1 Queries

**Mô tả**: Lazy loading gây ra nhiều queries.

**Giải pháp**: Use eager loading (with()).

### 3. Ignoring Mass Assignment

**Mô tả**: Không sử dụng fillable guarded.

**Giải phól**: Define $fillable or $guarded.

### 4. Hard-coded Config

**Mô tả**: Hard-coded values thay vì config.

**Giải pháp**: Use config files và env().

## Kết luận

Tránh các anti-patterns này giúp code Laravel sạch hơn.
