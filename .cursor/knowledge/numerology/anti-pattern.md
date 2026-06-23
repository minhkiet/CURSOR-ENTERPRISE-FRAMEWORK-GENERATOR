# Numerology Anti-Patterns - Các Mẫu Thiết Kế Cần Tránh

## Giới thiệu

Tài liệu này liệt kê các anti-patterns phổ biến trong việc phát triển hệ thống Thần Số Học.

## Anti-Patterns về Calculation

### 1. Ignoring Master Numbers

**Mô tả**: Rút gọn Master Numbers (11, 22, 33) như các số thường.

**Ví dụ xấu**: reduceNumber(11) = 2 thay vì giữ nguyên là 11.

**Hậu quả**: Mất ý nghĩa đặc biệt của Master Numbers.

**Giải pháp**: Check cho Master Numbers trước khi reduce.

### 2. Incorrect Name Processing

**Mô tả**: Không xử lý đúng tiếng Việt trong tên.

**Ví dụ xấu**: Xử lý "Nguyễn" như có chữ Y thay vì chuyển thành "Nguyen".

**Hậu quả**: Số không chính xác.

**Giải pháp**: Implement proper Vietnamese name normalization.

### 3. Wrong Date Parsing

**Mô tả**: Không handle các date formats khác nhau (DD/MM/YYYY vs MM/DD/YYYY).

**Hậu quả**: Sai Số Chủ Đạo.

**Giải pháp**: Explicit date format và validation.

## Anti-Patterns về Business Logic

### 4. Deterministic Pronouncements

**Mô tả**: Đưa ra interpretations như facts thay vì guidance.

**Hậu quả**: Users may make poor decisions.

**Giải pháp**: Sử dụng ngôn ngữ như "có thể", "xu hướng".

### 5. Overloading Information

**Mô tả**: Hiển thị tất cả numbers cùng lúc mà không prioritization.

**Hậu quả**: Users overwhelmed và disengaged.

**Giải pháp**: Progressive disclosure.

### 6. Generic Interpretations

**Mô tả**: Cùng interpretation cho all users với same number.

**Hậu quả**: Poor personalization.

**Giải pháp**: Factor in user's specific context.

## Anti-Patterns về Data Management

### 7. No Version Tracking

**Mô tả**: Không track calculation version.

**Hậu quả**: Khó compare readings across versions.

**Giải pháp**: Include version in reading record.

### 8. Storing Names Without Normalization

**Mô tả**: Lưu tên raw mà không normalize.

**Hậu quả**: Inconsistent calculations.

**Giải pháp**: Normalize và store normalized name.

## Kết luận

Tránh các anti-patterns này giúp xây dựng hệ thống Thần Số Học chất lượng cao.
