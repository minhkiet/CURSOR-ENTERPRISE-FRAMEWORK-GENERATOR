# Nuxt Anti-Patterns - Các Mẫu Cần Tránh

## Giới thiệu

Tài liệu này liệt kê các anti-patterns phổ biến trong Nuxt.js development.

## Anti-Patterns

### 1. Overusing Client-only

**Mô tả**: Đánh dấu components là client-only khi không cần.

**Giải pháp**: SSR-friendly components by default.

### 2. Improper Data Fetching

**Mô tả**: Fetch data trong onMounted thay vì useFetch.

**Giải pháp**: Use useFetch/useAsyncData.

### 3. Ignoring SEO

**Mô tả**: Không set meta tags.

**Giải pháp**: Use useHead() cho every page.

### 4. Large Bundle

**Mô tả**: Import libraries không cần thiết.

**Giải pháp**: Lazy load, tree-shake.

## Kết luận

Tránh các anti-patterns này giúp Nuxt apps tốt hơn.
