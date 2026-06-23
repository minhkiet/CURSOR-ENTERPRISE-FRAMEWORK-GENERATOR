---
title: MySQL 8.0 Features
description: Các tính năng mới trong MySQL 8.0 - CTEs, Window Functions, JSON Table, Descending Indexes, Role Management, InnoDB Cluster
tags: [mysql, mysql-8, cte, window-functions, json-table, roles, innodb-cluster]
created: 2026-06-23
version: 1.0.0
framework: cursor-enterprise-framework
---

# MySQL 8.0 Features

## Tổng quan

MySQL 8.0 là phiên bản major release đánh dấu bước tiến quan trọng trong lịch sử phát triển của MySQL. Phiên bản này mang đến nhiều tính năng mới được mong đợi từ lâu, cải thiện đáng kể về hiệu suất, bảo mật, và khả năng phát triển ứng dụng.

MySQL 8.0 không chỉ đơn thuần là một bản nâng cấp - nó đại diện cho một nền tảng database hiện đại với các tính năng enterprise-grade như atomic DDL, role-based access control, window functions, và cải thiện JSON support. Performance improvements trong MySQL 8.0 đến từ nhiều optimizations bao gồm improved optimizer, better parallel query execution, và enhanced InnoDB capabilities.

Tài liệu này cung cấp hướng dẫn chi tiết về các tính năng mới quan trọng nhất trong MySQL 8.0, cách sử dụng chúng hiệu quả, và best practices để migrate từ MySQL 5.7.

## Mục đích của tài liệu

Tài liệu này được viết nhằm giúp các developers và database administrators:

- Hiểu và tận dụng các tính năng mới của MySQL 8.0
- Migrate applications từ MySQL 5.7 một cách an toàn
- Sử dụng advanced SQL features như CTEs và window functions
- Implement improved security với role-based access control
- Tận dụng enhanced JSON support và các tính năng khác

## Các Khái niệm Cốt lõi

### 1. Common Table Expressions (CTEs)

Common Table Expressions (CTEs) cho phép bạn định nghĩa named temporary result sets có thể được reference trong main query. CTEs cải thiện readability và maintainability của complex queries.

#### Non-Recursive CTEs

```sql
-- Basic CTE syntax
WITH cte_name AS (
    SELECT column_list
    FROM table_name
    WHERE condition
)
SELECT * FROM cte_name;

-- Ví dụ: Sales analysis với CTE
WITH monthly_sales AS (
    SELECT 
        YEAR(order_date) AS year,
        MONTH(order_date) AS month,
        customer_id,
        SUM(total) AS total_sales
    FROM orders
    WHERE order_date >= '2025-01-01'
    GROUP BY YEAR(order_date), MONTH(order_date), customer_id
),
customer_monthly AS (
    SELECT 
        year,
        month,
        customer_id,
        total_sales,
        AVG(total_sales) OVER (
            PARTITION BY customer_id 
            ORDER BY year, month 
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ) AS moving_avg_3m
    FROM monthly_sales
)
SELECT 
    year,
    month,
    COUNT(DISTINCT customer_id) AS active_customers,
    SUM(total_sales) AS total_sales,
    AVG(moving_avg_3m) AS avg_moving_avg
FROM customer_monthly
GROUP BY year, month
ORDER BY year, month;
```

```sql
-- Multiple CTEs in one query
WITH 
    active_customers AS (
        SELECT customer_id
        FROM orders
        WHERE order_date >= DATE_SUB(CURDATE(), INTERVAL 90 DAY)
        GROUP BY customer_id
        HAVING COUNT(*) >= 3
    ),
    customer_orders AS (
        SELECT 
            o.customer_id,
            o.order_id,
            o.order_date,
            o.total,
            ROW_NUMBER() OVER (PARTITION BY o.customer_id ORDER BY o.order_date DESC) AS order_num
        FROM orders o
        INNER JOIN active_customers ac ON o.customer_id = ac.customer_id
    )
SELECT 
    co.customer_id,
    co.order_id,
    co.order_date,
    co.total,
    p.product_name,
    p.category
FROM customer_orders co
JOIN order_items oi ON co.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE co.order_num <= 5
ORDER BY co.customer_id, co.order_date DESC;
```

#### Recursive CTEs

Recursive CTEs cho phép bạn traverse hierarchical data structures như organizational trees, category hierarchies, và graph relationships.

```sql
-- Recursive CTE syntax
WITH RECURSIVE cte_name AS (
    -- Base case (initial row)
    SELECT column_list
    FROM table_name
    WHERE base_condition
    
    UNION ALL
    
    -- Recursive case
    SELECT column_list
    FROM table_name
    JOIN cte_name ON join_condition
    WHERE termination_condition
)
SELECT * FROM cte_name;

-- Ví dụ: Organizational hierarchy
WITH RECURSIVE org_tree AS (
    -- Base case: CEO
    SELECT 
        employee_id,
        name,
        manager_id,
        title,
        1 AS level,
        name AS path
    FROM employees
    WHERE manager_id IS NULL
    
    UNION ALL
    
    -- Recursive case: Employees reporting to manager
    SELECT 
        e.employee_id,
        e.name,
        e.manager_id,
        e.title,
        ot.level + 1,
        CONCAT(ot.path, ' > ', e.name)
    FROM employees e
    INNER JOIN org_tree ot ON e.manager_id = ot.employee_id
)
SELECT * FROM org_tree ORDER BY level, name;
```

```sql
-- Ví dụ: Bill of Materials (BOM) explosion
WITH RECURSIVE bom AS (
    -- Base components (no children)
    SELECT 
        component_id,
        component_name,
        parent_id,
        product_id,
        quantity,
        component_id AS root_id,
        component_name AS root_name,
        1 AS level,
        CAST(component_name AS CHAR(1000)) AS path
    FROM bom_components
    WHERE parent_id IS NULL
    
    UNION ALL
    
    -- Sub-components
    SELECT 
        bc.component_id,
        bc.component_name,
        bc.parent_id,
        bc.product_id,
        bc.quantity,
        bom.root_id,
        bom.root_name,
        bom.level + 1,
        CONCAT(bom.path, ' > ', bc.component_name)
    FROM bom_components bc
    INNER JOIN bom ON bc.parent_id = bom.component_id
    WHERE bom.level < 10  -- Prevent infinite recursion
)
SELECT 
    root_name AS product,
    component_name,
    level,
    quantity,
    path
FROM bom
ORDER BY root_name, level, component_name;
```

```sql
-- Ví dụ: Graph traversal (friend recommendations)
WITH RECURSIVE friends AS (
    -- Base case: Direct friends
    SELECT 
        user_id,
        friend_id,
        1 AS degree,
        CAST(CONCAT(user_id, '-', friend_id) AS CHAR(1000)) AS path
    FROM friendships
    WHERE user_id = 1
    
    UNION ALL
    
    -- Friends of friends
    SELECT 
        f.user_id,
        f.friend_id,
        fr.degree + 1,
        CONCAT(fr.path, '-', f.friend_id)
    FROM friendships f
    INNER JOIN friends fr ON f.user_id = fr.friend_id
    WHERE fr.degree < 3  -- Max 3 degrees
    AND CHAR_LENGTH(REPLACE(fr.path, '-', '')) < 50  -- Prevent cycles
)
SELECT 
    friend_id,
    MIN(degree) AS degree,
    COUNT(*) AS paths
FROM friends
WHERE friend_id != 1  -- Exclude self
AND friend_id NOT IN (
    SELECT friend_id FROM friendships WHERE user_id = 1
)
GROUP BY friend_id
HAVING MIN(degree) <= 2
ORDER BY degree, paths DESC;
```

### 2. Window Functions

Window functions thực hiện calculations across a set of rows related to the current row, tương tự như aggregate functions nhưng không group rows thành một output row duy nhất.

#### Window Function Types

```sql
-- Ranking functions
ROW_NUMBER() OVER (PARTITION BY col ORDER BY col)
RANK() OVER (PARTITION BY col ORDER BY col)
DENSE_RANK() OVER (PARTITION BY col ORDER BY col)
PERCENT_RANK() OVER (PARTITION BY col ORDER BY col)
CUME_DIST() OVER (PARTITION BY col ORDER BY col)

-- Aggregate functions as window functions
COUNT(*) OVER (PARTITION BY col)
SUM(col) OVER (PARTITION BY col ORDER BY col)
AVG(col) OVER (PARTITION BY col ORDER BY col)
MIN(col) OVER (PARTITION BY col ORDER BY col)
MAX(col) OVER (PARTITION BY col ORDER BY col)

-- Value functions
LAG(col) OVER (PARTITION BY col ORDER BY col)
LEAD(col) OVER (PARTITION BY col ORDER BY col)
FIRST_VALUE(col) OVER (PARTITION BY col ORDER BY col)
LAST_VALUE(col) OVER (PARTITION BY col ORDER BY col)
NTH_VALUE(col, n) OVER (PARTITION BY col ORDER BY col)
```

#### Practical Examples

```sql
-- Sales leaderboard
SELECT 
    employee_id,
    employee_name,
    department,
    sales_amount,
    ROW_NUMBER() OVER (
        PARTITION BY department 
        ORDER BY sales_amount DESC
    ) AS department_rank,
    RANK() OVER (
        ORDER BY sales_amount DESC
    ) AS overall_rank,
    PERCENT_RANK() OVER (
        ORDER BY sales_amount DESC
    ) AS percentile
FROM employee_sales
WHERE period = 'Q1-2026';
```

```sql
-- Time-series analysis với LAG/LEAD
SELECT 
    order_date,
    daily_sales,
    LAG(daily_sales, 1) OVER (ORDER BY order_date) AS prev_day_sales,
    LEAD(daily_sales, 1) OVER (ORDER BY order_date) AS next_day_sales,
    daily_sales - LAG(daily_sales, 1) OVER (ORDER BY order_date) AS day_over_day_change,
    ROUND(
        (daily_sales - LAG(daily_sales, 1) OVER (ORDER BY order_date)) /
        LAG(daily_sales, 1) OVER (ORDER BY order_date) * 100, 
        2
    ) AS change_pct
FROM (
    SELECT 
        order_date,
        SUM(total) AS daily_sales
    FROM orders
    GROUP BY order_date
) daily;
```

```sql
-- Running totals và moving averages
SELECT 
    order_date,
    daily_sales,
    SUM(daily_sales) OVER (
        ORDER BY order_date 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total,
    AVG(daily_sales) OVER (
        ORDER BY order_date 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS moving_avg_7d,
    MAX(daily_sales) OVER (
        ORDER BY order_date 
        ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) AS rolling_max_30d
FROM (
    SELECT 
        order_date,
        SUM(total) AS daily_sales
    FROM orders
    GROUP BY order_date
) daily
ORDER BY order_date;
```

```sql
-- Nth value in partition
SELECT 
    product_name,
    category,
    price,
    FIRST_VALUE(price) OVER (
        PARTITION BY category 
        ORDER BY price
    ) AS cheapest_in_category,
    LAST_VALUE(price) OVER (
        PARTITION BY category 
        ORDER BY price
        RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS most_expensive_in_category,
    NTH_VALUE(price, 2) OVER (
        PARTITION BY category 
        ORDER BY price
    ) AS second_cheapest
FROM products
ORDER BY category, price;
```

```sql
-- Churn analysis
SELECT 
    customer_id,
    order_date,
    LAG(order_date) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
    ) AS prev_order_date,
    DATEDIFF(
        order_date,
        LAG(order_date) OVER (
            PARTITION BY customer_id 
            ORDER BY order_date
        )
    ) AS days_since_last_order,
    CASE 
        WHEN DATEDIFF(
            CURDATE(),
            order_date
        ) > 60 THEN 'CHURNED'
        WHEN DATEDIFF(
            CURDATE(),
            order_date
        ) > 30 THEN 'AT_RISK'
        ELSE 'ACTIVE'
    END AS customer_status
FROM orders
ORDER BY customer_id, order_date;
```

### 3. JSON Table Functions

MySQL 8.0 cung cấp khả năng extract và transform JSON data thành relational format sử dụng JSON_TABLE() function.

```sql
-- JSON_TABLE syntax
JSON_TABLE(
    json_data,
    path_columns
    [COLUMNS (column_definition,...)]
) AS table_alias

-- Column definitions
column_name data_type PATH '$.json_path' [ERROR_ON_EMPTY | NULL_ON_EMPTY | DEFAULT value ON EMPTY],
NESTED PATH '$.nested_array[*]' COLUMNS (column definitions)
```

```sql
-- Basic JSON_TABLE example
SELECT *
FROM JSON_TABLE(
    '[{"name":"John","age":30},{"name":"Jane","age":25}]',
    '$[*]'
    COLUMNS (
        name VARCHAR(100) PATH '$.name',
        age INT PATH '$.age'
    )
) AS people;

-- Output:
-- name | age
-- -----|-----
-- John | 30
-- Jane | 25
```

```sql
-- Extract order items từ JSON column
SELECT 
    o.order_id,
    o.customer_id,
    jt.sku,
    jt.quantity,
    jt.price,
    jt.quantity * jt.price AS line_total
FROM orders o,
JSON_TABLE(
    o.items_json,
    '$[*]'
    COLUMNS (
        sku VARCHAR(50) PATH '$.sku',
        quantity INT PATH '$.quantity',
        price DECIMAL(10,2) PATH '$.price'
    )
) AS jt
WHERE o.order_date >= '2026-01-01';
```

```sql
-- Nested JSON extraction
SELECT 
    o.order_id,
    jt.customer_name,
    jt.address_city,
    jt.items_sku,
    jt.items_qty
FROM orders o,
JSON_TABLE(
    o.order_data,
    '$'
    COLUMNS (
        customer_name VARCHAR(100) PATH '$.customer.name',
        NESTED PATH '$.customer.address[*]' COLUMNS (
            address_city VARCHAR(100) PATH '$.city'
        ),
        NESTED PATH '$.items[*]' COLUMNS (
            items_sku VARCHAR(50) PATH '$.sku',
            items_qty INT PATH '$.quantity'
        )
    )
) AS jt
WHERE o.order_date >= '2026-01-01';
```

```sql
-- Advanced JSON aggregation
WITH RECOMMENDATIONS AS (
    SELECT 
        user_id,
        jt.product_id,
        jt.score
    FROM user_preferences up,
    JSON_TABLE(
        up.preferences_json,
        '$.recommendations[*]'
        COLUMNS (
            product_id INT PATH '$.product_id',
            score DECIMAL(3,2) PATH '$.score'
        )
    ) AS jt
)
SELECT 
    user_id,
    COUNT(*) AS num_recommendations,
    AVG(score) AS avg_confidence,
    SUM(CASE WHEN score >= 0.8 THEN 1 ELSE 0 END) AS high_confidence_count
FROM RECOMMENDATIONS
GROUP BY user_id
HAVING AVG(score) >= 0.5;
```

### 4. Descending Indexes

MySQL 8.0 cho phép indexes với descending order (DESC), thay vì luôn ascending như trước. Điều này cải thiện performance cho queries với ORDER BY DESC.

```sql
-- Create descending index
CREATE INDEX idx_order_date_desc ON orders (order_date DESC);
CREATE INDEX idx_name_desc ON customers (name DESC);

-- Composite index với mixed order
CREATE INDEX idx_status_date ON orders (
    order_status ASC,      -- ASC for equality predicate
    order_date DESC        -- DESC for ORDER BY
);

-- Queries that benefit
SELECT * FROM orders 
WHERE order_status = 'completed'
ORDER BY order_date DESC
LIMIT 10;
-- Sử dụng idx_status_date efficiently

-- Verify index usage
EXPLAIN SELECT * FROM orders 
WHERE order_status = 'pending'
ORDER BY order_date DESC;

-- Output includes:
-- key: idx_status_date
-- key_len: ...
-- rows: ...
-- Extra: Backward index scan  <-- Uses DESC index efficiently
```

```sql
-- Performance comparison
-- Without descending index (uses index, then filesort for DESC)
CREATE INDEX idx_date_asc ON orders (order_date);

EXPLAIN SELECT * FROM orders 
WHERE order_status = 'pending'
ORDER BY order_date DESC;

-- With descending index (uses index directly)
CREATE INDEX idx_date_desc ON orders (order_date DESC);

EXPLAIN SELECT * FROM orders 
WHERE order_status = 'pending'
ORDER BY order_date DESC;
```

### 5. Role-based Access Control

MySQL 8.0 giới thiệu role-based access control, cho phép tạo roles với specific privileges và gán roles cho users.

```sql
-- Create roles
CREATE ROLE 'app_read';
CREATE ROLE 'app_write';
CREATE ROLE 'app_admin';
CREATE ROLE 'dba';
CREATE ROLE 'developer';

-- Grant privileges to roles
GRANT SELECT ON ecommerce.* TO 'app_read';
GRANT SELECT, INSERT, UPDATE, DELETE ON ecommerce.* TO 'app_write';
GRANT ALL ON ecommerce.* TO 'app_admin';
GRANT ALL ON *.* TO 'dba';
GRANT SELECT ON production_db.* TO 'developer';
GRANT SELECT ON analytics_db.* TO 'developer';

-- Create users và assign roles
CREATE USER 'app_service'@'%' IDENTIFIED BY 'StrongP@ss!';
CREATE USER 'etl_service'@'%' IDENTIFIED BY 'StrongP@ss!';
CREATE USER 'admin_user'@'%' IDENTIFIED BY 'StrongP@ss!';
CREATE USER 'data_scientist'@'%' IDENTIFIED BY 'StrongP@ss!';

GRANT 'app_read' TO 'app_service'@'%';
GRANT 'app_write' TO 'app_service'@'%';
GRANT 'app_admin' TO 'admin_user'@'%';
GRANT 'app_read' TO 'etl_service'@'%';
GRANT 'app_write' TO 'etl_service'@'%';
GRANT 'app_read' TO 'data_scientist'@'%';
```

```sql
-- Role hierarchy
CREATE ROLE 'senior_developer';
CREATE ROLE 'junior_developer';

-- Senior developer inherits junior developer privileges
GRANT 'junior_developer' TO 'senior_developer';
GRANT EXECUTE ON PROCEDURE production_db.backup_* TO 'senior_developer';
GRANT CREATE USER ON *.* TO 'senior_developer';

-- Assign hierarchical role
GRANT 'senior_developer' TO 'senior_dev_user'@'%';
```

```sql
-- Set default roles for users
ALTER USER 'app_service'@'%' DEFAULT ROLE 'app_read', 'app_write';
ALTER USER 'admin_user'@'%' DEFAULT ROLE 'app_admin';

-- Activate roles (for current session)
SET ROLE 'app_read', 'app_write';
SET ROLE ALL;

-- Check current roles
SELECT CURRENT_ROLE();
SHOW GRANTS FOR CURRENT_USER();
```

```sql
-- Role management
-- Revoke role from user
REVOKE 'app_write' FROM 'app_service'@'%';

-- Revoke privilege from role
REVOKE DELETE ON ecommerce.* FROM 'app_write';

-- Drop role
DROP ROLE 'deprecated_role';

-- View role privileges
SHOW GRANTS FOR 'app_read';
-- +-------------------------------------------+
-- | Grants for app_read@%                      |
-- +-------------------------------------------+
-- | GRANT USAGE ON *.* TO 'app_read'@'%'      |
-- | GRANT SELECT ON ecommerce.* TO 'app_read'@'%' |
-- +-------------------------------------------+
```

```sql
-- Mandatory roles (MySQL 8.0.18+)
-- Set mandatory roles that are always active
SET PERSIST mandatory_roles = 'r1, r2, r3@host';

-- Or in my.cnf
[mysqld]
mandatory_roles = 'r1,r2,r3@host'
```

### 6. Atomic DDL

MySQL 8.0 thực hiện DDL operations một cách atomic - either complete successfully hoặc roll back completely. Điều này ngăn chặn inconsistent states khi DDL fails.

```sql
-- Before MySQL 8.0: Partial DDL could leave inconsistent state
-- CREATE TABLE t (a INT) ENGINE=InnoDB;
-- ALTER TABLE t ADD COLUMN b INT;  -- Fails mid-way

-- MySQL 8.0: Atomic DDL ensures consistency
-- If ALTER TABLE fails, table reverts to original state
```

```sql
-- DDL rollback demonstration
-- Tạo table
CREATE TABLE test_atomic (
    id INT PRIMARY KEY,
    name VARCHAR(100)
) ENGINE=InnoDB;

-- Attempt failed operation (will rollback)
-- RENAME TABLE test_atomic TO nonexistent.test_atomic;  -- Fails

-- Table remains in original state
SHOW CREATE TABLE test_atomic;

-- Atomic rename
RENAME TABLE test_atomic TO test_atomic_renamed;
SHOW CREATE TABLE test_atomic_renamed;
```

### 7. Enhanced Unicode Support

MySQL 8.0 mặc định sử dụng utf8mb4 (full UTF-8 support) thay vì latin1.

```sql
-- Default character set là utf8mb4 trong MySQL 8.0
SHOW VARIABLES LIKE 'character_set%';

-- utf8mb4_0900_ai_ci (MySQL 8.0) vs utf8mb4_unicode_ci (MySQL 5.7)
-- utf8mb4_0900_ai_ci hỗ trợ:
-- - Accent insensitive (ai)
-- - Case insensitive (ci)
-- - Better performance
-- - Emojis và supplementary characters

CREATE TABLE unicode_test (
    id INT PRIMARY KEY,
    text_default VARCHAR(100),           -- utf8mb4_0900_ai_ci
    text_explicit VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
) ENGINE=InnoDB;

-- Insert various Unicode content
INSERT INTO unicode_test VALUES 
(1, 'Hello', 'Hello'),
(2, 'こんにちは', 'Japanese'),
(3, '🎉🎊', 'Emojis'),
(4, 'café', 'Cafe'),
(5, 'naïve', 'Accents');
```

## InnoDB Enhancements

### 1. InnoDB Cluster

InnoDB Cluster cung cấp high availability solution tích hợp với MySQL Group Replication và MySQL Router.

```sql
-- Setup InnoDB Cluster (via MySQL Shell)
-- mysqlsh
// javascript
// dba.createCluster('myCluster')
// cluster.addInstance('mysql-2:3306')
// cluster.addInstance('mysql-3:3306')

-- Check cluster status
// cluster.status()
```

```bash
# MySQL Router configuration
mysqlrouter --bootstrap root@localhost:3306 \
    --directory /etc/mysqlrouter \
    --conf-use-sockets \
    --conf-bind-address 127.0.0.1

# Start MySQL Router
systemctl start mysqlrouter
```

### 2. Instant ADD COLUMN

MySQL 8.0.12+ hỗ trợ instant ADD COLUMN - không cần copy table data khi thêm column vào cuối.

```sql
-- Instant ADD COLUMN (column thêm vào cuối, nullable hoặc có default)
ALTER TABLE orders 
ADD COLUMN tracking_number VARCHAR(100) NULL AFTER total;

-- Verify: không rebuild table
-- Check data_leng th không tăng đáng kể

-- NOT instant: 
-- - ADD COLUMN ở giữa
-- - ADD COLUMN có DATA_TYPE thay đổi
ALTER TABLE orders 
ADD COLUMN new_column VARCHAR(50) NOT NULL AFTER order_date;  -- Instant
```

### 3. Enhanced Information Schema

```sql
-- Better performance for INFORMATION_SCHEMA queries
-- Parallel query execution for I_S tables

-- New columns trong InnoDB tables
SELECT * FROM information_schema.INNODB_TABLESPACES_BRIEF;
SELECT * FROM information_schema.INNODB_TABLES;
SELECT * FROM information_schema.INNODB_COLUMNS;
```

### 4. Resource Groups

Resource groups cho phép bạn phân bổ threads vào groups và set CPU affinity.

```sql
-- Create resource groups
CREATE RESOURCE GROUP admin_rg 
    TYPE = SYSTEM 
    VCPU = 0-3
    THREAD_PRIORITY = -20;

CREATE RESOURCE GROUP batch_rg 
    TYPE = USER 
    VCPU = 4-7
    THREAD_PRIORITY = 5;

-- Assign thread to resource group
SET RESOURCE GROUP admin_rg FOR thread_id;

-- Assign thread by name
SET RESOURCE GROUP batch_rg FOR some_thread;

-- View resource groups
SELECT * FROM information_schema.RESOURCE_GROUPS;
```

## Các Best Practices

### 1. Migration từ MySQL 5.7

```bash
# Step 1: Upgrade MySQL 5.7 to 8.0
# 1. Backup all databases
mysqldump --all-databases --routines --triggers --events > backup_57.sql

# 2. Install MySQL 8.0
# 3. Initialize new data directory
# mysqld --initialize-insecure --user=mysql

# 4. Start MySQL 8.0
# 5. Load backup
# mysql < backup_57.sql
```

```sql
-- Step 2: Post-migration checks

-- Check for deprecated features
SELECT * FROM information_schema.COLUMNS 
WHERE TABLE_SCHEMA = 'your_db'
AND COLUMN_DEFAULT IS NULL
AND IS_NULLABLE = 'NO'
AND COLUMN_TYPE LIKE '%timestamp%';

-- Check for non-standard reserved words
-- MySQL 8.0 has additional reserved words

-- Check for FULLTEXT indexes
-- Verify innodb_ft_* system tables exist

-- Check for SET GLOBAL changes needed
SELECT @@character_set_server;
SET GLOBAL character_set_server = 'utf8mb4';
```

```sql
-- Step 3: Optimizer improvements

-- MySQL 8.0 has improved optimizer
-- Consider updating statistics
ANALYZE TABLE your_table;

-- Histograms (MySQL 8.0)
ANALYZE TABLE your_table UPDATE HISTOGRAM ON column_name;
SELECT * FROM information_schema.COLUMN_STATISTICS;

-- Check invisible indexes (can be useful during migration)
ALTER TABLE your_table ALTER INDEX idx_name INVISIBLE;
```

### 2. Performance Tuning for MySQL 8.0

```ini
# my.cnf - MySQL 8.0 specific tuning
[mysqld]
# Character set
character_set_server = utf8mb4
collation_server = utf8mb4_0900_ai_ci

# New performance features
optimizer_switch = 'index_merge=on,index_merge_union=on,index_merge_sort_union=on,index_merge_intersection=on'

# New default values
default_authentication_plugin = caching_sha2_password

# InnoDB enhancements
innodb_buffer_pool_in_core_file = OFF  # MySQL 8.0.14+
innodb_log_writer_threads = ON           # MySQL 8.0.22+
innodb_dedicated_server = AUTO          # Auto-tune based on server resources
```

### 3. Security Best Practices

```sql
-- Use strong authentication
ALTER USER 'root'@'localhost' IDENTIFIED BY 'NewStrongP@ss!';

-- Password validation
SET GLOBAL validate_password.policy = 'STRONG';

-- Create users with caching_sha2_password
CREATE USER 'app'@'%' IDENTIFIED WITH caching_sha2_password BY 'StrongP@ss!';

-- Enable SSL/TLS
SET GLOBAL require_secure_transport = ON;

-- Audit logging (MySQL Enterprise)
-- SET GLOBAL general_log = 'ON';
-- SET GLOBAL general_log_file = '/var/log/mysql/audit.log';
```

## Các Common Patterns

### Pattern 1: Complex Analytics với CTEs

```sql
-- Customer lifetime value calculation
WITH RECURRIVE customer_periods AS (
    -- First purchase
    SELECT 
        customer_id,
        MIN(order_date) AS first_purchase,
        DATE_ADD(MIN(order_date), INTERVAL 1 YEAR) AS next_period_start
    FROM orders
    GROUP BY customer_id
    
    UNION ALL
    
    -- Subsequent periods
    SELECT 
        cp.customer_id,
        cp.next_period_start AS first_purchase,
        DATE_ADD(cp.next_period_start, INTERVAL 1 YEAR)
    FROM customer_periods cp
    JOIN orders o ON cp.customer_id = o.customer_id
        AND o.order_date >= cp.next_period_start
        AND o.order_date < DATE_ADD(cp.next_period_start, INTERVAL 1 YEAR)
    WHERE cp.next_period_start < CURDATE()
),
period_revenue AS (
    SELECT 
        cp.customer_id,
        cp.first_purchase AS period_start,
        SUM(o.total) AS period_revenue,
        COUNT(DISTINCT o.order_id) AS order_count
    FROM customer_periods cp
    JOIN orders o ON cp.customer_id = o.customer_id
        AND o.order_date >= cp.first_purchase
        AND o.order_date < DATE_ADD(cp.first_purchase, INTERVAL 1 YEAR)
    GROUP BY cp.customer_id, cp.first_purchase
)
SELECT 
    customer_id,
    SUM(period_revenue) AS lifetime_value,
    SUM(order_count) AS lifetime_orders,
    COUNT(DISTINCT YEAR(period_start)) AS periods_active
FROM period_revenue
GROUP BY customer_id
ORDER BY lifetime_value DESC;
```

### Pattern 2: Real-time Analytics Dashboard

```sql
-- Dashboard metrics với window functions
WITH daily_metrics AS (
    SELECT 
        DATE(order_date) AS date,
        COUNT(DISTINCT customer_id) AS dau,
        COUNT(*) AS orders,
        SUM(total) AS revenue,
        SUM(total) / COUNT(*) AS avg_order_value
    FROM orders
    WHERE order_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
    GROUP BY DATE(order_date)
),
metrics_with_trend AS (
    SELECT 
        date,
        dau,
        orders,
        revenue,
        avg_order_value,
        AVG(dau) OVER (
            ORDER BY date 
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS dau_7d_avg,
        AVG(orders) OVER (
            ORDER BY date 
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS orders_7d_avg,
        AVG(revenue) OVER (
            ORDER BY date 
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS revenue_7d_avg,
        dau - LAG(dau) OVER (ORDER BY date) AS dau_delta,
        revenue - LAG(revenue) OVER (ORDER BY date) AS revenue_delta,
        ROUND(
            (revenue - LAG(revenue) OVER (ORDER BY date)) /
            NULLIF(LAG(revenue) OVER (ORDER BY date), 0) * 100, 
            2
        ) AS revenue_growth_pct
    FROM daily_metrics
)
SELECT 
    date,
    dau,
    dau_7d_avg AS dau_7d_ma,
    dau_delta,
    orders,
    revenue,
    revenue_7d_avg AS revenue_7d_ma,
    revenue_growth_pct,
    avg_order_value
FROM metrics_with_trend
ORDER BY date DESC;
```

### Pattern 3: Flexible JSON Reporting

```sql
-- Generate JSON report từ relational data
SELECT JSON_OBJECT(
    'report_date', CURDATE(),
    'total_orders', COUNT(*),
    'total_revenue', SUM(total),
    'top_products', (
        SELECT JSON_ARRAYAGG(JSON_OBJECT(
            'product_id', product_id,
            'product_name', name,
            'revenue', revenue
        ))
        FROM (
            SELECT 
                oi.product_id,
                p.name,
                SUM(oi.quantity * oi.price) AS revenue
            FROM order_items oi
            JOIN products p ON oi.product_id = p.product_id
            JOIN orders o ON oi.order_id = o.order_id
            WHERE o.order_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
            GROUP BY oi.product_id, p.name
            ORDER BY revenue DESC
            LIMIT 10
        ) top_products
    ),
    'orders_by_status', (
        SELECT JSON_OBJECTAGG(status, count)
        FROM (
            SELECT order_status AS status, COUNT(*) AS count
            FROM orders
            GROUP BY order_status
        ) status_counts
    )
) AS report_json
FROM orders
WHERE order_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY);
```

## Troubleshooting

### Vấn đề 1: cachel_sha2_password Authentication

**Symptom**: Clients không thể connect với error về authentication plugin.

**Diagnosis**:
```bash
mysql -u app_user -p
# Error: Authentication plugin 'caching_sha2_password' is not supported
```

**Solutions**:

1. **Update MySQL client**
```bash
mysql --version  # Update nếu cũ
```

2. **Use compatible authentication for user**
```sql
-- Create user with native password
ALTER USER 'app_user'@'%' IDENTIFIED WITH mysql_native_password BY 'password';
```

3. **Force sha2_password với SSL**
```sql
-- User must connect via SSL
ALTER USER 'app_user'@'%' REQUIRE SSL;
```

### Vấn đề 2: Reserved Words Conflicts

**Symptom**: Queries fail với unexpected syntax errors.

**Diagnosis**:
```sql
-- Check if column name is reserved
SELECT * FROM information_schema.COLUMNS
WHERE COLUMN_NAME IN ('groups', 'roles', 'window');
```

**Solution**:
```sql
-- Rename column hoặc quote identifier
SELECT `groups`, `roles`, `window`
FROM my_table;

-- Or rename column
ALTER TABLE my_table CHANGE COLUMN `groups` group_name VARCHAR(50);
```

### Vấn đề 3: Index Size Changes

**Symptom**: Index size tăng sau migration.

**Cause**: utf8mb4 sử dụng 4 bytes per character thay vì 3 bytes.

**Solution**:
```sql
-- Consider prefix indexes
CREATE INDEX idx_name_prefix ON users (name(50));

-- Or assess if index can be shortened
-- 255 chars utf8mb4 = 1020 bytes (vs 767 max for InnoDB)
```

## Ví dụ Thực tế

### Ví dụ 1: Complete Analytics Query

```sql
-- E-commerce analytics dashboard query
WITH base_data AS (
    SELECT 
        o.order_id,
        o.customer_id,
        o.order_date,
        o.total AS order_total,
        oi.product_id,
        oi.quantity,
        oi.price AS unit_price,
        c.category_id,
        c.category_name,
        p.brand_id,
        b.brand_name,
        CASE 
            WHEN o.order_date <= DATE_ADD(o.order_date, INTERVAL 30 DAY)
            THEN 'NORMAL'
            ELSE 'CHURNED'
        END AS customer_status
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_id
    JOIN categories c ON p.category_id = c.category_id
    JOIN brands b ON p.brand_id = b.brand_id
    WHERE o.order_date >= '2025-01-01'
),
customer_metrics AS (
    SELECT 
        customer_id,
        MIN(order_date) AS first_purchase_date,
        MAX(order_date) AS last_purchase_date,
        COUNT(DISTINCT order_id) AS total_orders,
        SUM(order_total) AS lifetime_value,
        AVG(order_total) AS avg_order_value,
        DATEDIFF(CURDATE(), MAX(order_date)) AS days_since_last_order
    FROM base_data
    GROUP BY customer_id
),
category_metrics AS (
    SELECT 
        category_id,
        category_name,
        COUNT(DISTINCT order_id) AS order_count,
        SUM(quantity * unit_price) AS category_revenue,
        AVG(quantity * unit_price) AS avg_item_value,
        RANK() OVER (ORDER BY SUM(quantity * unit_price) DESC) AS category_rank
    FROM base_data
    GROUP BY category_id, category_name
)
SELECT 
    cm.customer_id,
    cm.first_purchase_date,
    cm.last_purchase_date,
    cm.total_orders,
    cm.lifetime_value,
    cm.avg_order_value,
    cm.days_since_last_order,
    cat.category_name AS top_category,
    cat.category_revenue AS top_category_revenue,
    RANK() OVER (ORDER BY cm.lifetime_value DESC) AS customer_tier
FROM customer_metrics cm
LEFT JOIN (
    SELECT DISTINCT FIRST_VALUE(customer_id) OVER (PARTITION BY customer_id ORDER BY quantity * unit_price DESC) AS customer_id,
           FIRST_VALUE(category_name) OVER (PARTITION BY customer_id ORDER BY quantity * unit_price DESC) AS category_name,
           FIRST_VALUE(category_revenue) OVER (PARTITION BY customer_id ORDER BY quantity * unit_price DESC) AS category_revenue
    FROM category_metrics
) cat ON cm.customer_id = cat.customer_id
ORDER BY cm.lifetime_value DESC
LIMIT 100;
```

### Ví dụ 2: Session Analysis

```sql
-- Analyze user sessions from event data
WITH user_events AS (
    SELECT 
        user_id,
        session_id,
        event_timestamp,
        event_type,
        page_url,
        LAG(event_timestamp) OVER (
            PARTITION BY user_id, session_id 
            ORDER BY event_timestamp
        ) AS prev_event_time,
        LEAD(event_timestamp) OVER (
            PARTITION BY user_id, session_id 
            ORDER BY event_timestamp
        ) AS next_event_time
    FROM user_activity_log
    WHERE DATE(event_timestamp) >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
),
session_metrics AS (
    SELECT 
        user_id,
        session_id,
        MIN(event_timestamp) AS session_start,
        MAX(event_timestamp) AS session_end,
        TIMESTAMPDIFF(SECOND, MIN(event_timestamp), MAX(event_timestamp)) AS session_duration_sec,
        COUNT(*) AS event_count,
        COUNT(DISTINCT page_url) AS pages_visited,
        MAX(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS has_purchase
    FROM user_events
    GROUP BY user_id, session_id
),
session_with_metrics AS (
    SELECT 
        *,
        AVG(session_duration_sec) OVER (
            PARTITION BY user_id 
            ORDER BY session_start
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ) AS rolling_avg_session_duration,
        SUM(event_count) OVER (
            PARTITION BY user_id 
            ORDER BY session_start
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS rolling_7d_events,
        ROW_NUMBER() OVER (
            PARTITION BY user_id 
            ORDER BY session_end DESC
        ) AS recency_rank
    FROM session_metrics
)
SELECT 
    user_id,
    COUNT(*) AS total_sessions,
    AVG(session_duration_sec) AS avg_session_duration,
    SUM(event_count) AS total_events,
    SUM(CASE WHEN has_purchase = 1 THEN 1 ELSE 0 END) AS purchase_sessions,
    MAX(session_end) AS last_session,
    DATEDIFF(CURDATE(), MAX(session_end)) AS days_inactive
FROM session_with_metrics
GROUP BY user_id
HAVING days_inactive <= 7
ORDER BY total_events DESC;
```

## Tham khảo

### Official Documentation

- [MySQL 8.0 Reference Manual](https://dev.mysql.com/doc/refman/8.0/en/)
- [What's New in MySQL 8.0](https://dev.mysql.com/doc/refman/8.0/en/mysql-nutshell.html)
- [Common Table Expressions](https://dev.mysql.com/doc/refman/8.0/en/with.html)
- [Window Functions](https://dev.mysql.com/doc/refman/8.0/en/window-functions.html)
- [JSON Table Functions](https://dev.mysql.com/doc/refman/8.0/en/json-table-functions.html)
- [Roles](https://dev.mysql.com/doc/refman/8.0/en/roles.html)

### MySQL Shell Commands

```bash
# MySQL Shell commands for InnoDB Cluster
mysqlsh ---js
// dba.createCluster()
// cluster.addInstance()
// cluster.status()

# Upgrade checker
mysqlsh -- util checkForServerUpgrade()
```

### Books

- "MySQL 8.0 Reference Manual" - Official documentation
- "MySQL 8.0: New Features" - Oreilly publications

---

*Document version: 1.0.0*
*Last updated: 2026-06-23*
*Framework: Cursor Enterprise Framework*
