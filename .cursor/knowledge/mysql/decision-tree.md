# MySQL Decision Tree - Cây Quyết Định

## Mục lục
1. [Data Type Decision](#1-data-type-decision)
2. [Index Decision](#2-index-decision)
3. [Query Optimization Decision](#3-query-optimization-decision)

---

## 1. Data Type Decision

```
Bạn cần chọn data type?
│
├── Data là True/False hoặc Yes/No?
│   ├── YES ────────────────────────────────→ → → TINYINT(1) hoặc BOOLEAN
│   │                                              └── Chỉ 0 và 1
│   │
│   └── NO
│       │
│       └── Data là số nguyên?
│           ├── YES
│           │   └── Giá trị lớn hơn 0?
│           │       ├── YES ────────────────────────────────→ → → INT UNSIGNED
│           │       │                                              └── Tối đa ~4 tỷ
│           │       │
│           │       └── NO ─────────────────────────────────→ → → INT
│           │                                                              └── Có âm và dương
│           │
│           └── NO
│               │
│               └── Data là số thập phân (tiền tệ)?
│                   ├── YES ────────────────────────────────→ → → DECIMAL(p,s)
│                   │                                              └── p: tổng chữ số, s: chữ số thập phân
│                   │
│                   └── NO
│                       │
│                       └── Data là ngày giờ?
│                           ├── YES
│                           │   └── Cần timestamp với timezone?
│                           │       ├── YES ────────────────────────────────→ → → TIMESTAMP
│                           │       │                                              └── Tự động convert timezone
│                           │       │
│                           │       └── NO ─────────────────────────────────→ → → DATETIME
│                           │                                                              └── Ngày giờ cố định
│                           │
│                           └── Data có độ dài cố định?
│                               ├── YES ────────────────────────────────→ → → CHAR(n)
│                               │                                              └── Mã, mã vùng (US, VN)
│                               │
│                               └── NO (độ dài thay đổi)
│                                   │
│                                   └── Có thể > 255 ký tự?
│                                       ├── YES ────────────────────────────────→ → → TEXT
│                                       │                                              └── Bài viết, mô tả dài
│                                       │
│                                       └── NO ────────────────────────────────→ → → VARCHAR(n)
│                                                                      └── Tên, email, địa chỉ
```

---

## 2. Index Decision

```
Bạn cần tạo index?
│
├── Column là PRIMARY KEY?
│   ├── YES ────────────────────────────────→ → → Tự động được index
│   │
│   └── NO
│       │
│       └── Column là FOREIGN KEY?
│           ├── YES ────────────────────────────────→ → → Nên tạo index
│           │                                              └── Cải thiện JOIN performance
│           │
│           └── NO
│               │
│               └── Column được sử dụng trong WHERE?
│                   ├── YES
│                   │   └── Column có cardinality cao?
│                   │       ├── YES (>100 distinct values) ─────────────────────→ → → Tạo index
│                   │       │
│                   │       └── NO (low cardinality) ────────────────────────→ → → Cân nhắc kỹ
│                   │                                                              └── Có thể không cần
│                   │
│                   └── Column được sử dụng trong ORDER BY?
│                       ├── YES ────────────────────────────────→ → → Cân nhắc index
│                       │                                              └── Đặc biệt nếu JOIN với WHERE
│                       │
│                       └── NO ─────────────────────────────────→ → → Có thể không cần
```

---

## 3. Query Optimization Decision

```
Query của bạn chậm?
│
├── EXPLAIN đã được chạy?
│   ├── CHƯA ─────────────────────────────────→ → → CHẠY EXPLAIN TRƯỚC
│   │                                              └── EXPLAIN SELECT ...
│   │
│   └── RỒI
│       │
│       └── type = 'ALL' (full table scan)?
│           ├── YES
│           │   └── WHERE clause có indexed column?
│           │       ├── CÓ ────────────────────────────────→ → → Kiểm tra function trên column
│           │       │                                      └── Column có function wrapping?
│           │       │                                          ├── CÓ ───→ Loại bỏ function
│           │       │                                          └── KHÔNG ───→ Index không được sử dụng
│           │       │                                                     Kiểm tra statistics
│           │       │
│           │       └── KHÔNG ───────────────────────────→ → → Cần thêm index
│           │                                                  └── Index trên WHERE columns
│           │
│           └── NO (có index được sử dụng)
│               │
│               └── Extra có 'Using filesort'?
│                   ├── YES ────────────────────────────────→ → → Thêm index cho ORDER BY
│                   │                                              └── INDEX (col1, col2) cho ORDER BY
│                   │
│                   └── Extra có 'Using temporary'?
│                       ├── YES ────────────────────────────────→ → → GROUP BY / ORDER BY columns
│                       │                                              └── Cần cover bằng index
│                       │
│                       └── Tất cả OK nhưng vẫn chậm
│                           │
│                           └── Kiểm tra:
│                               ├── Kết quả trả về > 15% rows?
│                               │   ├── YES ───→ Query design issue
│                               │   │           └── Thử LIMIT hoặc paginate
│                               │   │
│                               │   └── Table có lớn?
│                               │       ├── YES ───→ Cần partition hoặc archive
│                               │       │
│                               │       └── NO ───→ Server/resource issue
│                               │                   └── Kiểm tra: RAM, disk I/O
│                               │
│                               └── Cache query results
│                                   └── Sử dụng query cache (MySQL < 8.0)
```

---

## Quick Decision Reference

### Data Types
```
Boolean → TINYINT(1) / BOOLEAN
Integer (positive) → INT UNSIGNED
Integer (with negatives) → INT
Decimal (money) → DECIMAL(10,2)
Date only → DATE
Date + Time → DATETIME
Date + Time + Timezone → TIMESTAMP
Fixed-length string → CHAR(n)
Variable string < 255 → VARCHAR(n)
Variable string > 255 → TEXT
JSON data → JSON
```

### Index Priority
```
1. Primary Keys ─── Auto-indexed
2. Foreign Keys ─── Always index
3. WHERE columns ─── High cardinality
4. ORDER BY columns ─── Combined with WHERE
5. JOIN columns ─── Always index
```

### Query Optimization Steps
```
1. EXPLAIN query
2. Check for full table scans
3. Verify index usage
4. Remove functions on columns
5. Add missing indexes
6. Consider query rewrite
7. Check server resources
```

---

## Liên kết liên quan
- [MySQL Glossary](./glossary.md)
- [MySQL Architecture](./architecture.md)
- [MySQL Best Practices](./best-practice.md)
- [MySQL Anti-Patterns](./anti-pattern.md)
- [MySQL Checklist](./checklist.md)
- [MySQL FAQ](./faq.md)
