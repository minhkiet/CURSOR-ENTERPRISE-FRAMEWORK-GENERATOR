# PostgreSQL Decision Tree - Cây Quyết Định

## Mục lục
1. [Data Type Selection](#1-data-type-selection)
2. [Index Creation](#2-index-creation)
3. [Query Optimization](#3-query-optimization)
4. [Performance Troubleshooting](#4-performance-troubleshooting)
5. [Security Implementation](#5-security-implementation)

---

## 1. Data Type Selection

```
BẮT ĐẦU: Chọn data type cho column
              │
              ▼
┌─────────────────────────────────────────┐
│  Dữ liệu là numeric có decimal?         │
└─────────────────────────────────────────┘
              │
        ┌─────┴─────┐
       YES          NO
        │            │
        ▼            ▼
┌───────────────┐  ┌─────────────────────────────────┐
│  DECIMAL hoặc │  │  Dữ liệu là date/time?          │
│  NUMERIC      │  └─────────────────────────────────┘
│  (exact)      │              │
│  • money      │        ┌─────┴─────┐
│  • amounts    │       YES          NO
│               │        │            │
└───────────────┘        ▼            ▼
                   ┌──────────────┐  Tiếp tục ↓
                   │ TIMESTAMP    │
                   │ WITH TIME   │
                   │ ZONE        │
                   │ (recommend) │
                   └──────────────┘
                         │
                         ▼
┌─────────────────────────────────────────┐
│  Dữ liệu là boolean?                   │
└─────────────────────────────────────────┘
              │
        ┌─────┴─────┐
       YES          NO
        │            │
        ▼            ▼
┌───────────────┐  Tiếp tục ↓
│   BOOLEAN     │
│   (not INT)   │
└───────────────┘
```

```
TIẾP TỤC: Chọn data type cho column
              │
              ▼
┌─────────────────────────────────────────┐
│  Dữ liệu là text có giới hạn length?    │
└─────────────────────────────────────────┘
              │
        ┌─────┴─────┐
       YES          NO
        │            │
        ▼            ▼
┌───────────────┐  ┌─────────────────────────────────┐
│  VARCHAR(n)   │  │  Cần lưu trữ structured data?   │
│  hoặc TEXT   │  └─────────────────────────────────┘
│  nếu không    │              │
│  có limit    │        ┌─────┴─────┐
└───────────────┘       YES          NO
        │                 │            │
        ▼                 ▼            ▼
    KẾT THÚC        ┌────────────┐  Tiếp tục ↓
                    │  JSONB     │
                    │ (preferred │
                    │  over     │
                    │  JSON)     │
                    └────────────┘
                          │
                          ▼
                    ┌────────────┐
                    │  ARRAY     │
                    │ (cho list  │
                    │  đơn       │
                    │  giản)     │
                    └────────────┘
                          │
                          ▼
                    ┌────────────┐
                    │  Cần unique│
                    │  identifier│
                    │  ?         │
                    └────────────┘
                          │
                    ┌─────┴─────┐
                   YES          NO
                    │            │
                    ▼            ▼
            ┌────────────┐  KẾT THÚC
            │ SERIAL     │
            │ (local)    │
            │ hoặc       │
            │ UUID v4/v7 │
            │ (global)   │
            └────────────┘
```

---

## 2. Index Creation

```
BẮT ĐẦU: Tạo index cho query này?
              │
              ▼
┌─────────────────────────────────────────┐
│  Query có WHERE clause?                 │
└─────────────────────────────────────────┘
              │
        ┌─────┴─────┐
       YES          NO
        │            │
        ▼            ▼
┌───────────────┐  ┌─────────────────────────────────┐
│  WHERE clause │  │  Cần ORDER BY optimization?      │
│  có nhiều     │  └─────────────────────────────────┘
│  columns?    │              │
└───────────────┘        ┌─────┴─────┐
        │                YES          NO
        ▼                 │            │
    Tiếp tục ↓           ▼            ▼
                   ┌────────────┐  KẾT THÚC
                   │ Tạo index  │
                   │ trên       │
                   │ ORDER BY   │
                   │ columns    │
                   └────────────┘
```

```
TIẾP TỤC: Tạo index nào?
              │
              ▼
┌─────────────────────────────────────────┐
│  WHERE clause filter rows?              │
│  (e.g., status = 'pending')            │
└─────────────────────────────────────────┘
              │
        ┌─────┴─────┐
       YES          NO
        │            │
        ▼            ▼
┌───────────────┐  Tiếp tục ↓
│  PARTIAL     │
│  INDEX       │
│  (chỉ index  │
│  filtered    │
│  rows)       │
└───────────────┘
        │
        ▼
┌─────────────────────────────────────────┐
│  Cần index multiple columns?           │
└─────────────────────────────────────────┘
              │
        ┌─────┴─────┐
       YES          NO
        │            │
        ▼            ▼
┌───────────────┐  Tiếp tục ↓
│  COMPOSITE   │
│  INDEX       │
│              │
│ Column order │
│ 1. Equality  │
│    (=) first │
│ 2. Range     │
│    last      │
└───────────────┘
        │
        ▼
┌─────────────────────────────────────────┐
│  Query SELECT chỉ specific columns?    │
└─────────────────────────────────────────┘
              │
        ┌─────┴─────┐
       YES          NO
        │            │
        ▼            ▼
┌───────────────┐  KẾT THÚC
│  COVERING    │
│  INDEX       │
│              │
│ INCLUDE      │
│ (extra cols) │
└───────────────┘
```

```
INDEX TYPE SELECTION:
              │
              ▼
┌─────────────────────────────────────────┐
│  Data type của column?                  │
└─────────────────────────────────────────┘
              │
    ┌────┬────┬────┬────┬────┐
    ▼    ▼    ▼    ▼    ▼
  TEXT  NUM  DATE JSON ARRAY
    │    │    │    │    │
    ▼    ▼    ▼    ▼    ▼
┌──────┐ ┌───┐ ┌───┐ ┌────┐ ┌────┐
│B-Tree│ │GIN│ │BRIN│ │GIN │ │GIN │
│(def) │ └───┘ └───┘ └────┘ └────┘
└──────┘
    │
    ▼
┌─────────────────────────────────────────┐
│  Cần full-text search?                  │
└─────────────────────────────────────────┘
              │
        ┌─────┴─────┐
       YES          NO
        │            │
        ▼            ▼
┌───────────────┐  KẾT THÚC
│  GIN với     │
│  tsvector    │
│  (search)    │
└───────────────┘
```

---

## 3. Query Optimization

```
BẮT ĐẦU: Tối ưu query chậm
              │
              ▼
┌─────────────────────────────────────────┐
│  Query có slow subquery?                │
└─────────────────────────────────────────┘
              │
        ┌─────┴─────┐
       YES          NO
        │            │
        ▼            ▼
┌───────────────┐  Tiếp tục ↓
│  Chuyển       │
│  subquery     │
│  thành JOIN   │
│  hoặc CTE     │
└───────────────┘
        │
        ▼
┌─────────────────────────────────────────┐
│  Query có multiple OR?                 │
└─────────────────────────────────────────┘
              │
        ┌─────┴─────┐
       YES          NO
        │            │
        ▼            ▼
┌───────────────┐  Tiếp tục ↓
│  Thay OR     │
│  bằng IN    │
│  hoặc UNION │
└───────────────┘
        │
        ▼
┌─────────────────────────────────────────┐
│  Query có JOIN?                         │
└─────────────────────────────────────────┘
              │
        ┌─────┴─────┐
       YES          NO
        │            │
        ▼            ▼
┌───────────────┐  Tiếp tục ↓
│  JOIN có     │
│  index trên  │
│  join cols?  │
└───────────────┘
        │
        ▼
    ┌─────┴─────┐
   YES          NO
    │            │
    ▼            ▼
┌────────┐  ┌───────────────┐
│KẾT THÚC│  │  Tạo index    │
│ (OK)   │  │  trên JOIN    │
└────────┘  │  columns      │
            └───────────────┘
```

```
QUERY PATTERN OPTIMIZATION:
              │
              ▼
┌─────────────────────────────────────────┐
│  Pattern của query?                     │
└─────────────────────────────────────────┘
              │
    ┌────┬────┬────┬────┬────┐
    ▼    ▼    ▼    ▼    ▼
  AGG  RANK PAGING SEARCH COMPLEX
    │    │    │    │    │
    ▼    ▼    ▼    ▼    ▼
┌──────┐ ┌───┐ ┌───┐ ┌────┐ ┌─────────┐
│Group  │ │Win-│ │OFF-│ │GIN │ │CTE với  │
│by     │ │dow │ │SET │ │idx │ │RECUR-   │
│Index  │ │Func│ │    │ │    │ │SIVE     │
└──────┘ └───┘ └───┘ └────┘ └─────────┘
    │    │    │    │    │
    ▼    ▼    ▼    ▼    ▼
┌─────────────────────────────────────────┐
│  Sử dụng EXPLAIN ANALYZE để verify     │
└─────────────────────────────────────────┘
```

---

## 4. Performance Troubleshooting

```
BẮT ĐẦU: Query chậm - làm sao?
              │
              ▼
┌─────────────────────────────────────────┐
│  1. Chạy EXPLAIN ANALYZE                │
│     - Kiểm tra execution plan          │
│     - So sánh estimated vs actual rows │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│  Plan có Seq Scan trên large table?    │
└─────────────────────────────────────────┘
              │
        ┌─────┴─────┐
       YES          NO
        │            │
        ▼            ▼
┌───────────────┐  Tiếp tục ↓
│  Index có    │
│  trên WHERE  │
│  columns?    │
└───────────────┘
        │
        ▼
    ┌─────┴─────┐
   YES          NO
    │            │
    ▼            ▼
┌────────┐  ┌───────────────┐
│Đã có  │  │  Tạo index    │
│index  │  │  trên WHERE   │
│nhưng  │  │  columns      │
│không  │  └───────────────┘
│được   │         │
│dùng?  │         ▼
└────────┘  ┌─────────────────┐
    │        │ Chạy ANALYZE    │
    ▼        │ để update       │
┌─────────────────┐ statistics  │
│  - Check cost   │              │
│    estimates     │              │
│  - Force index  │              │
│    if needed    │              │
└─────────────────┘              │
```

```
TIẾP TỤC: Performance troubleshooting
              │
              ▼
┌─────────────────────────────────────────┐
│  Estimated rows >> Actual rows?         │
│  (Statistics stale)                     │
└─────────────────────────────────────────┘
              │
        ┌─────┴─────┐
       YES          NO
        │            │
        ▼            ▼
┌───────────────┐  Tiếp tục ↓
│  Chạy        │
│  ANALYZE     │
│  trên table  │
└───────────────┘
        │
        ▼
┌─────────────────────────────────────────┐
│  Query có implicit type conversion?     │
│  (string vs int)                        │
└─────────────────────────────────────────┘
        │
        ┌─────┴─────┐
       YES          NO
        │            │
        ▼            ▼
┌───────────────┐  Tiếp tục ↓
│  CAST đúng   │
│  type trong  │
│  query       │
└───────────────┘
        │
        ▼
┌─────────────────────────────────────────┐
│  Query có function trên indexed column? │
└─────────────────────────────────────────┘
        │
        ┌─────┴─────┐
       YES          NO
        │            │
        ▼            ▼
┌───────────────┐  Tiếp tục ↓
│  Tạo expr    │
│  index với   │
│  function    │
└───────────────┘
```

```
ADVANCED PERFORMANCE:
              │
              ▼
┌─────────────────────────────────────────┐
│  Query vẫn chậm sau khi optimize?       │
└─────────────────────────────────────────┘
              │
        ┌─────┴─────┐
       YES          NO
        │            │
        ▼            ▼
┌───────────────┐  KẾT THÚC
│  Table có    │
│  N+1 query?  │
└───────────────┘
        │
        ▼
    ┌─────┴─────┐
   YES          NO
    │            │
    ▼            ▼
┌───────────────┐  ┌───────────────┐
│  Sử dụng     │  │  Xem xét      │
│  JOIN thay   │  │  materialized │
│  vì multi    │  │  view         │
│  queries     │  │               │
└───────────────┘  │  hoặc         │
        │          │  denormalize  │
        ▼          └───────────────┘
┌───────────────┐
│  Batch load   │
│  nếu bulk     │
│  operations   │
└───────────────┘
```

---

## 5. Security Implementation

```
BẮT ĐẦU: Implement security
              │
              ▼
┌─────────────────────────────────────────┐
│  Cần protect row-level access?          │
└─────────────────────────────────────────┘
              │
        ┌─────┴─────┐
       YES          NO
        │            │
        ▼            ▼
┌───────────────┐  Tiếp tục ↓
│  Enable RLS   │
│  ALTER TABLE  │
│  ENABLE ROW   │
│  LEVEL        │
│  SECURITY     │
└───────────────┘
        │
        ▼
┌─────────────────────────────────────────┐
│  Tạo policies cho từng access pattern    │
│  • User chỉ thấy data của mình          │
│  • Admin thấy tất cả                    │
│  • Read-only role chỉ SELECT            │
└─────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────┐
│  Cần protect sensitive columns?         │
└─────────────────────────────────────────┘
        │
        ┌─────┴─────┐
       YES          NO
        │            │
        ▼            ▼
┌───────────────┐  KẾT THÚC
│  Sử dụng     │
│  Column-level │
│  security     │
│  hoặc view   │
│  filtering   │
└───────────────┘
```

```
AUTHENTICATION & AUTHORIZATION:
              │
              ▼
┌─────────────────────────────────────────┐
│  Chọn authentication method?             │
└─────────────────────────────────────────┘
              │
    ┌────┬────┬────┬────┐
    ▼    ▼    ▼    ▼    ▼
 LOCAL MD5 SCRAM LDAP SSO
    │    │    │    │    │
    ▼    ▼    ▼    ▼    ▼
┌──────┐ ┌───┐ ┌───┐ ┌────┐ ┌─────────┐
│trust │ │pass│ │pass│ │LDAP│ │SAML/   │
│local │ │word│ │word│ │Auth│ │OAuth2  │
│conn  │ │enc │ │enc │ │    │ │        │
└──────┘ └───┘ └───┘ └────┘ └─────────┘
```

```
PRIVILEGE MANAGEMENT:
              │
              ▼
┌─────────────────────────────────────────┐
│  Tạo application user role              │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│  Grant permissions theo principle:      │
│  • CONNECT on database                  │
│  • USAGE on schema                      │
│  • SELECT/INSERT/UPDATE/DELETE on      │
│    specific tables                      │
│  • USAGE, SELECT on sequences          │
│  • NO superuser privileges              │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│  Separate roles cho different needs:    │
│  • app_readwrite                        │
│  • app_readonly                         │
│  • app_migration                        │
└─────────────────────────────────────────┘
```

---

## Summary Decision Tree

```
POSTGRESQL DECISION FLOW:
              │
              ▼
┌─────────────────────────────────────────┐
│           START HERE                     │
└─────────────────────────────────────────┘
              │
              ▼
    ┌─────────────────┐
    │  Thiết kế mới: │
    │  Schema/Data    │
    │  Types          │
    └────────┬────────┘
              │
              ▼
    ┌─────────────────┐
    │  Tối ưu:        │
    │  Indexes        │
    └────────┬────────┘
              │
              ▼
    ┌─────────────────┐
    │  Debug:         │
    │  EXPLAIN        │
    └────────┬────────┘
              │
              ▼
    ┌─────────────────┐
    │  Production:    │
    │  Security       │
    └────────┬────────┘
              │
              ▼
    ┌─────────────────┐
    │  Operations:    │
    │  Backup/HA      │
    └─────────────────┘
```

---

## Liên kết liên quan
- [PostgreSQL Glossary](./glossary.md)
- [PostgreSQL Architecture](./architecture.md)
- [PostgreSQL Best Practices](./best-practice.md)
- [PostgreSQL Anti-Patterns](./anti-pattern.md)
- [PostgreSQL Checklist](./checklist.md)
- [PostgreSQL FAQ](./faq.md)
