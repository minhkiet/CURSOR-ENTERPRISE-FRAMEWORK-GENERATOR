# Numerology Decision Tree - Cây Quyết Định

## Giới thiệu

Cây quyết định này hướng dẫn developers và system designers trong việc đưa ra các quyết định kiến trúc và triển khai cho hệ thống Thần Số Học.

## Quyết định về Calculation Method

### Câu hỏi: Nên sử dụng phương pháp tính nào?

- **Pythagorean Method**
  - Pros: Phổ biến nhất, dễ hiểu
  - Cons: Ít chính xác hơn cho một số cases
  - Khi nào: Users mới, Western-focused app

- **Chaldean Method**
  - Pros: Cổ xưa hơn, được coi là chính xác hơn
  - Cons: Ít phổ biến, ít tài liệu
  - Khi nào: Advanced users, Eastern-focused app

- **Support Both**
  - Approach: Cho phép users chọn
  - Pros: Flexibility, comprehensive
  - Cons: More complex
  - Khi nào: Most applications

## Quyết định về Data Model

### Câu hỏi: Nên lưu trữ readings như thế nào?

- **Relational (PostgreSQL)**
  - Phù hợp khi: ACID compliance, complex queries
  - Khi nào: Enterprise applications

- **Document (MongoDB)**
  - Phù hợp khi: Flexible schema
  - Khi nào: Agile development

## Quyết định về Name Processing

### Câu hỏi: Làm thế nào để xử lý tên tiếng Việt?

- **Normalize to Latin**
  - Approach: Chuyển đổi sang alphabet không dấu
  - Pros: Đơn giản
  - Cons: Mất thông tin
  - Khi nào: Simple implementation

- **Preserve Diacritics**
  - Approach: Xử lý trực tiếp các ký tự tiếng Việt
  - Pros: Chính xác hơn
  - Cons: Complex
  - Khi nào: Vietnamese-focused app

## Quyết định về Visualization

### Câu hỏi: Nên visualize numbers như thế nào?

- **Number Wheel**
  - Approach: Bánh xe số với connections
  - Khi nào: Most applications

- **Cards**
  - Approach: Cards cho mỗi number
  - Khi nào: Mobile apps

## Summary

Sử dụng cây quyết định này như starting point và document các decisions trong ADRs.
