# Vue Anti-Patterns - Các Mẫu Cần Tránh

## Giới thiệu

Tài liệu này liệt kê các anti-patterns phổ biến trong Vue.js development.

## Anti-Patterns

### 1. Mutating Props

**Mô tả**: Thay đổi props trực tiếp trong child component.

**Giải pháp**: Emit events để update parent state.

### 2. Overusing Vuex/Pinia

**Mô tả**: Lưu trữ mọi thứ vào global store.

**Giải pháp**: Chỉ dùng store cho cross-component state.

### 3. Not Using Key with v-for

**Mô tả**: Sử dụng v-for mà không có key.

**Giải phól**: Luôn sử dụng unique :key.

### 4. Side Effects in Computed

**Mô tả**: Side effects trong computed properties.

**Giải pháp**: Computed chỉ cho derived state, dùng watch cho side effects.

### 5. Too Many Watchers

**Mô tả**: Overusing watchers thay vì computed.

**Giải pháp**: Prefer computed properties.

## Kết luận

Tránh các anti-patterns này giúp code Vue sạch hơn.
