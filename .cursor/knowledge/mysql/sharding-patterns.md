---
title: Sharding Patterns
description: Chiến lược Sharding - Horizontal Sharding, Sharding Keys, Consistent Hashing, Application-level Sharding, ProxySQL Sharding, Vitess
tags: [mysql, sharding, scalability, distributed-database, consistent-hashing]
created: 2026-06-23
version: 1.0.0
framework: cursor-enterprise-framework
---

# Sharding Patterns

## Tổng quan

Sharding là kỹ thuật phân chia data của một database table lớn thành nhiều smaller tables (shards) được lưu trữ trên các servers khác nhau. Mỗi shard chứa một phần của data và có thể được truy cập độc lập. Sharding là giải pháp quan trọng khi một single database server không thể handle tải hoặc storage requirements của ứng dụng.

Trong môi trường enterprise, khi data volume đạt đến hàng tỷ rows hoặc khi transaction throughput vượt quá khả năng của một single server, sharding trở thành lựa chọn cần thiết. Tuy nhiên, sharding cũng mang đến những complexity mới về data distribution, cross-shard queries, và distributed transactions.

Tài liệu này cung cấp hướng dẫn chi tiết về các chiến lược sharding khác nhau, cách chọn sharding keys, implementation patterns, và các tools để implement và quản lý sharded databases.

## Mục đích của tài liệu

Tài liệu này được viết nhằm giúp các database architects và developers:

- Hiểu các loại sharding strategies và trade-offs
- Chọn và evaluate sharding keys phù hợp
- Implement application-level sharding
- Sử dụng middleware như ProxySQL cho sharding
- Hiểu các concepts từ Vitess và cách apply vào MySQL
- Thiết kế schema và queries tương thích với sharding

## Các Khái niệm Cốt lõi

### 1. Horizontal Sharding (Data Partitioning)

Horizontal sharding (còn gọi là data partitioning hoặc zone sharding) phân chia rows của một table thành nhiều physical tables, mỗi table chứa một subset của rows dựa trên một shard key.

#### Sharding vs Partitioning

| Aspect | Table Partitioning | Sharding |
|--------|-------------------|----------|
| Storage | Single server | Multiple servers |
| Operation | Same database | Distributed databases |
| Complexity | Low | High |
| Cross-partition queries | Supported | Limited |
| Cross-shard queries | N/A | Very limited |
| Scaling | Vertical | Horizontal |

```sql
-- Ví dụ: Partitioning trên single server
CREATE TABLE orders (
    order_id BIGINT,
    customer_id INT,
    order_date DATE,
    total DECIMAL(10,2),
    PRIMARY KEY (order_id, order_date)
) ENGINE=InnoDB
PARTITION BY RANGE (YEAR(order_date)) (
    PARTITION p_2024 VALUES LESS THAN (2025),
    PARTITION p_2025 VALUES LESS THAN (2026),
    PARTITION p_2026 VALUES LESS THAN (2027),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);

-- Sharding: Data thực sự nằm trên các servers khác nhau
-- Shard 1 (shard_0): orders_0
-- Shard 2 (shard_1): orders_1
-- Shard 3 (shard_2): orders_2
```

#### Khi nào cần Sharding

**Indicators**:

1. **Database size gần đạt disk capacity**
2. **Replication lag không thể giải quyết được**
3. **Backup/restore times quá lâu**
4. **Single primary bottleneck cho writes**
5. **Cost của single large server vượt budget**

**Pre-sharding considerations**:

1. **Data growth projection**: Đủ 12-24 months growth?
2. **Query patterns**: % cross-shard queries có thể chấp nhận được?
3. **Operational complexity**: Có đủ resources để quản lý sharded environment?

### 2. Sharding Keys

Sharding key là column(s) được sử dụng để determine data sẽ được lưu trên shard nào. Việc chọn sharding key là quan trọng nhất trong sharding design.

#### Các loại Sharding Keys

**1. User ID / Customer ID**
- Pros: Natural access pattern cho user-centric apps
- Cons: Hot spots nếu có power users

```sql
-- Shard by user_id modulo N
shard_id = user_id % num_shards

-- Hoặc range-based
shard_id = user_id / 1000  -- Mỗi shard chứa 1000 users
```

**2. Time-based / Date-based**
- Pros: Dễ implement, align với retention policies
- Cons: Hot spot ở current period

```sql
-- Shard by date
shard_id = YEAR(order_date) * 12 + MONTH(order_date)

-- Hoặc range
shard_2024: orders WHERE order_date < '2025-01-01'
shard_2025: orders WHERE order_date >= '2025-01-01' AND order_date < '2026-01-01'
shard_2026: orders WHERE order_date >= '2026-01-01'
```

**3. Geographic-based**
- Pros: Tốt cho latency-sensitive apps (multi-region)
- Cons: Rebalancing phức tạp

```sql
-- Shard by region
shard_us: customers WHERE region = 'US'
shard_eu: customers WHERE region = 'EU'
shard_asia: customers WHERE region = 'APAC'
```

**4. Hash-based**
- Pros: Even distribution
- Cons: No locality, cross-shard queries khó

```sql
-- Consistent hashing
shard_id = CRC32(sharding_key) % num_shards

-- Hoặc MD5/SHA
shard_id = CONV(SUBSTRING(MD5(sharding_key), 1, 8), 16, 10) % num_shards
```

#### Các tính chất của Good Sharding Key

```sql
-- 1. High Cardinality: Có nhiều distinct values
-- BAD: gender (2 values), country (~200 values)
-- GOOD: user_id (hàng triệu values)

-- 2. Even Distribution: Mỗi shard chứa roughly equal data
-- Kiểm tra distribution:
SELECT 
    COUNT(*) / (SELECT COUNT(*) FROM orders) AS pct_rows,
    SUM(total) / (SELECT SUM(total) FROM orders) AS pct_volume
FROM orders
GROUP BY shard_id;

-- 3. Access Pattern Alignment: Queries thường filter theo shard key
-- Tốt:
SELECT * FROM orders WHERE customer_id = ?;
-- Không tốt (requires all shards):
SELECT * FROM orders WHERE order_date BETWEEN ? AND ?;
```

### 3. Consistent Hashing

Consistent hashing là thuật toán giúp minimize data movement khi thêm hoặc bớt shards, khác với modulo-based sharding cần remap đa số data.

#### How Consistent Hashing Works

```
                    Hash Ring (0 to 2^32)
                    
            0                              2^32
            |--------------------------------|
                   ^
                   |
            [Node A: 1000]
                       ^
                       |
            [Node B: 3000]
                       ^
                       |
            [Node C: 6000]
                       ^
                       |
            [Node D: 9000]

Data với hash value X được assigned đến node có hash lớn hơn gần nhất
```

#### Implementation

```python
# Python implementation của consistent hashing
import hashlib
from bisect import bisect

class ConsistentHash:
    def __init__(self, nodes=None, virtual_nodes=100):
        self.virtual_nodes = virtual_nodes
        self.ring = {}
        self.sorted_keys = []
        
        if nodes:
            for node in nodes:
                self.add_node(node)
    
    def _hash(self, key):
        """Hash function - có thể thay đổi"""
        return int(hashlib.md5(str(key).encode()).hexdigest(), 16)
    
    def add_node(self, node):
        """Thêm node vào ring"""
        for i in range(self.virtual_nodes):
            hash_key = self._hash(f"{node}_{i}")
            self.ring[hash_key] = node
        self.sorted_keys = sorted(self.ring.keys())
    
    def remove_node(self, node):
        """Remove node khỏi ring"""
        for i in range(self.virtual_nodes):
            hash_key = self._hash(f"{node}_{i}")
            del self.ring[hash_key]
        self.sorted_keys = sorted(self.ring.keys())
    
    def get_node(self, key):
        """Lấy node cho một key"""
        if not self.ring:
            return None
        
        hash_key = self._hash(key)
        # Tìm node có hash lớn hơn gần nhất
        pos = bisect(self.sorted_keys, hash_key)
        if pos == len(self.sorted_keys):
            pos = 0
        return self.ring[self.sorted_keys[pos]]

# Usage
ch = ConsistentHash(['shard1', 'shard2', 'shard3'], virtual_nodes=150)

# Get shard cho user_id
user_id = 12345
shard = ch.get_node(user_id)
print(f"User {user_id} -> Shard {shard}")

# Add new shard (minimize data movement)
ch.add_node('shard4')
```

```sql
-- MySQL UDF cho consistent hashing
-- Cần compile và install mysql-udf-consistent-hash
CREATE FUNCTION consistent_hash RETURNS INT
    SONAME 'consistent_hash.so';

-- Usage
SELECT consistent_hash(user_id, 4) AS shard_id;
```

### 4. Application-level Sharding

Trong application-level sharding, application logic xác định shard nào chứa data và kết nối trực tiếp đến shard đó. Cách này linh hoạt nhưng đòi hỏi code changes.

#### Shard Router Pattern

```python
# Python example: Shard Router
import hashlib
from typing import Optional, List

class ShardRouter:
    def __init__(self, shard_config: List[dict]):
        """
        shard_config = [
            {'id': 0, 'host': 'shard0.db.internal', 'port': 3306},
            {'id': 1, 'host': 'shard1.db.internal', 'port': 3306},
            {'id': 2, 'host': 'shard2.db.internal', 'port': 3306},
        ]
        """
        self.shards = {s['id']: s for s in shard_config}
        self.num_shards = len(shard_config)
    
    def get_shard_id(self, key_value: any, strategy: str = 'mod') -> int:
        """Determine shard ID dựa trên strategy"""
        if strategy == 'mod':
            key_hash = int(hashlib.md5(str(key_value).encode()).hexdigest(), 16)
            return key_hash % self.num_shards
        elif strategy == 'range':
            # Range-based sharding
            if key_value < 1000000:
                return 0
            elif key_value < 5000000:
                return 1
            else:
                return 2
        elif strategy == 'consistent':
            # Consistent hashing
            return self._consistent_hash(key_value)
    
    def get_connection(self, shard_id: int):
        """Get database connection cho shard"""
        import mysql.connector
        shard = self.shards.get(shard_id)
        return mysql.connector.connect(
            host=shard['host'],
            port=shard['port'],
            database='app_db',
            user='app_user',
            password='password'
        )
    
    def get_shard_for_user(self, user_id: int) -> dict:
        """Get shard configuration cho user"""
        shard_id = self.get_shard_id(user_id)
        return self.shards[shard_id]
    
    def execute_on_shard(self, shard_id: int, query: str, params: tuple = None):
        """Execute query trên specific shard"""
        conn = self.get_connection(shard_id)
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

# Usage
router = ShardRouter(shard_config)

def get_user_orders(user_id: int, limit: int = 10):
    shard = router.get_shard_for_user(user_id)
    query = """
        SELECT order_id, order_date, total 
        FROM orders 
        WHERE customer_id = %s 
        ORDER BY order_date DESC 
        LIMIT %s
    """
    return router.execute_on_shard(shard['id'], query, (user_id, limit))
```

#### Global Lookup Table

```sql
-- Tạo bảng để track shard assignments
CREATE TABLE shard_map (
    entity_type VARCHAR(50) NOT NULL,
    entity_id BIGINT NOT NULL,
    shard_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (entity_type, entity_id),
    INDEX idx_shard (shard_id)
) ENGINE=InnoDB;

-- Các entities cần lookup table
-- - User details (khi cần query không có user_id)
-- - Product catalog (khi cần search across shards)
-- - Locations/addresses

-- Khi user tạo account
INSERT INTO shard_map (entity_type, entity_id, shard_id)
VALUES ('user', NEW.user_id, router.get_shard_id(NEW.user_id));

-- Lookup user shard
SELECT shard_id FROM shard_map WHERE entity_type = 'user' AND entity_id = ?
```

### 5. ProxySQL Sharding

ProxySQL là advanced SQL proxy hỗ trợ sharding thông qua query rules và redirect logic.

#### ProxySQL Installation và Configuration

```bash
# Install ProxySQL
wget https://github.com/sysown/proxysql/releases/download/v2.5.1/proxysql_2.5.1_amd64.deb
dpkg -i proxysql_2.5.1_amd64.deb

# Start ProxySQL
systemctl start proxysql
```

```sql
-- Connect to ProxySQL admin interface
mysql -h 127.0.0.1 -u admin -padmin -P 6032

-- Configure main mysql servers (shards)
INSERT INTO mysql_servers (hostgroup_id, hostname, port, status) VALUES
(10, 'shard0.db.internal', 3306, 'ONLINE'),
(11, 'shard0.db.internal', 3306, 'ONLINE'),  -- Write group
(20, 'shard1.db.internal', 3306, 'ONLINE'),
(21, 'shard1.db.internal', 3306, 'ONLINE'),  -- Write group
(30, 'shard2.db.internal', 3306, 'ONLINE'),
(31, 'shard2.db.internal', 3306, 'ONLINE');  -- Write group

LOAD MYSQL SERVERS TO RUNTIME;
SAVE MYSQL SERVERS TO DISK;
```

```sql
-- Configure users
INSERT INTO mysql_users (username, password, default_hostgroup) VALUES
('app_user', 'password_hash', 10);

LOAD MYSQL USERS TO RUNTIME;
SAVE MYSQL USERS TO DISK;
```

#### Query Rules cho Sharding

```sql
-- Route queries dựa trên shard key (user_id)
-- Pattern: SELECT ... WHERE user_id = 12345
INSERT INTO mysql_query_rules (
    rule_id, active, match_pattern, 
    destination_hostgroup, apply
) VALUES
(1, 1, '^SELECT.*FROM users WHERE user_id\\s*=\\s*([0-9]+)', 
    10, 1),  -- Route based on user_id to appropriate shard
(2, 1, '^SELECT.*FROM orders WHERE customer_id\\s*=\\s*([0-9]+)', 
    10, 1),  -- Route based on customer_id
(3, 1, '^SELECT.*FROM products WHERE product_id\\s*=\\s*([0-9]+)', 
    20, 1);  -- Products shard

-- Route all writes to primary hostgroup (10)
INSERT INTO mysql_query_rules (
    rule_id, active, match_digest, 
    destination_hostgroup, apply
) VALUES
(100, 1, '^(INSERT|UPDATE|DELETE)', 
    10, 1);

-- Default fallback
INSERT INTO mysql_query_rules (
    rule_id, active, match_digest,
    destination_hostgroup, apply
) VALUES
(1000, 1, '.*', 
    10, 1);

LOAD MYSQL QUERY RULES TO RUNTIME;
SAVE MYSQL QUERY RULES TO DISK;
```

#### Custom Sharding với ProxySQL Scheduler

```bash
# ProxySQL scheduler for custom routing
# /etc/proxysql/scheduler.json
cat > /etc/proxysql/scheduler.json <<'EOF'
[
    {
        "id": 1,
        "active": 1,
        "interval_ms": 10000,
        "filename": "/usr/bin/proxysql_shard_router",
        "arg1": "/etc/proxysql/shard_config.json",
        "arg2": "/var/lib/proxysql/shard_routes.db"
    }
]
EOF
```

```python
#!/usr/bin/env python3
# /usr/bin/proxysql_shard_router

import sys
import json
import sqlite3
import hashlib

def calculate_shard(user_id, num_shards):
    return int(hashlib.md5(str(user_id).encode()).hexdigest(), 16) % num_shards

def main():
    config_path = sys.argv[1]
    db_path = sys.argv[2]
    
    with open(config_path) as f:
        config = json.load(f)
    
    # Update routing table
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Clear old routes
    cursor.execute("DELETE FROM shard_routes")
    
    # Calculate routes
    for i, shard in enumerate(config['shards']):
        for user_range in shard.get('user_ranges', []):
            for user_id in range(user_range[0], user_range[1] + 1):
                shard_id = calculate_shard(user_id, len(config['shards']))
                cursor.execute(
                    "INSERT INTO shard_routes (entity_type, entity_id, shard_id) VALUES (?, ?, ?)",
                    ('user', user_id, shard_id)
                )
    
    conn.commit()
    conn.close()
    
    # Reload ProxySQL
    # In practice, you'd use ProxySQL admin interface

if __name__ == '__main__':
    main()
```

### 6. Vitess Concepts

Vitess là database clustering system ban đầu được phát triển bởi YouTube, giờ là open-source project. Nó cung cấp many của các concepts và tooling hữu ích cho MySQL sharding.

#### Key Vitess Concepts

**1. Keyspace**: Logical database tương đương với MySQL database, có thể span multiple shards.

**2. Shard**: Subset của data, thường được identify bằng range của shard keys.

**3. VTTablet**: Proxy server chạy bên cạnh MySQL, handle routing, connection pooling.

**4. VTGate**: Frontend proxy, nhận queries từ application, route đến appropriate VTTablets.

**5. Topology Service**: Stores cluster metadata (shard map, tablet locations).

```
┌─────────────────────────────────────────────────────────┐
│                      Application                         │
└───────────────────────────┬─────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                        VTGate                           │
│  ┌─────────────────────────────────────────────────┐    │
│  │              Query Router                        │    │
│  │  - Parse queries                                 │    │
│  │  - Determine target shards                       │    │
│  │  - Merge results                                 │    │
│  └─────────────────────────────────────────────────┘    │
└───────────────────────────┬─────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│   VTTablet    │   │   VTTablet    │   │   VTTablet    │
│   (Shard 0)   │   │   (Shard 1)   │   │   (Shard 2)   │
│ ┌───────────┐ │   │ ┌───────────┐ │   │ ┌───────────┐ │
│ │   MySQL   │ │   │ │   MySQL   │ │   │ │   MySQL   │ │
│ └───────────┘ │   └───────────┘ │   └───────────┘ │
└───────────────┘   └───────────────┘   └───────────────┘
```

#### Applying Vitess Patterns to MySQL

Dù không dùng Vitess, bạn có thể apply các patterns của nó:

```sql
-- 1. VSchema-like metadata table
CREATE TABLE vschema (
    table_name VARCHAR(255) PRIMARY KEY,
    shard_key VARCHAR(255),
    shard_algorithm ENUM('hash', 'range', 'consistent_hash'),
    num_shards INT,
    indexed_columns JSON,
    FOREIGN_KEY (shard_key) REFERENCES columns(table_name)
) ENGINE=InnoDB;

INSERT INTO vschema VALUES 
('orders', 'customer_id', 'hash', 4, '["customer_id", "order_id", "order_date"]'),
('products', 'product_id', 'hash', 2, '["product_id", "category_id"]');
```

```python
# 2. VTGate-like query router
class VitessQueryRouter:
    """Inspired by Vitess VTGate"""
    
    def __init__(self, shards):
        self.shards = shards
        self.keyspace = Keyspace(shards)
    
    def parse_and_route(self, query, params):
        """Parse query, find shard keys, route"""
        parsed = self.parse_query(query)
        
        if parsed.is_scatter_query():
            # Query touches all shards - needs special handling
            return self.execute_scatter(parsed, params)
        elif parsed.shard_key:
            # Route to specific shard
            shard = self.keyspace.get_shard(parsed.shard_key)
            return self.execute_on_shard(shard, parsed, params)
    
    def execute_scatter(self, query, params):
        """Execute on all shards, merge results"""
        results = []
        for shard in self.shards:
            result = self.execute_on_shard(shard, query, params)
            results.extend(result)
        return self.merge_results(query, results)
    
    def merge_results(self, query, results):
        """Merge sorted results from multiple shards"""
        if query.is_aggregate():
            return self.merge_aggregates(results)
        else:
            return self.sort_and_dedupe(results)
```

## Các Best Practices

### 1. Sharding Key Selection

```sql
-- Checklist cho good sharding key:

-- 1. High cardinality
SELECT COUNT(DISTINCT customer_id) AS cardinality FROM orders;
-- Nên có ít nhất 10x số shards

-- 2. Even distribution
SELECT 
    FLOOR(customer_id / 1000000) AS bucket,
    COUNT(*) AS cnt,
    AVG(total) AS avg_total
FROM orders
GROUP BY bucket
ORDER BY bucket;

-- 3. Query pattern alignment
-- % queries filter theo sharding key?
SELECT 
    'Filtered by customer_id' AS pattern,
    COUNT(*) AS count
FROM query_log
WHERE query LIKE '%WHERE customer_id%'

UNION ALL

SELECT 
    'Filtered by order_date' AS pattern,
    COUNT(*) AS count
FROM query_log
WHERE query LIKE '%WHERE order_date%';
```

### 2. Cross-shard Query Handling

```python
# Pattern: Scatter-gather cho cross-shard queries
class CrossShardQueryExecutor:
    def __init__(self, router):
        self.router = router
    
    def execute_scatter_gather(self, query_template, params=None):
        """
        Execute query trên all shards và merge results
        """
        futures = []
        
        # Submit to all shards
        for shard_id, shard in self.router.shards.items():
            future = self.submit_query(shard, query_template, params)
            futures.append((shard_id, future))
        
        # Gather results
        results = []
        for shard_id, future in futures:
            try:
                shard_results = future.result(timeout=30)
                results.extend(shard_results)
            except Exception as e:
                logger.error(f"Shard {shard_id} failed: {e}")
        
        return results
    
    def get_top_products_by_revenue(self, start_date, end_date, limit=10):
        """Example: Top products across all shards"""
        query = """
            SELECT 
                product_id,
                SUM(quantity * unit_price) AS revenue
            FROM order_items
            WHERE created_at BETWEEN %s AND %s
            GROUP BY product_id
        """
        
        # Execute on all shards
        all_results = self.execute_scatter_gather(query, (start_date, end_date))
        
        # Aggregate and sort
        aggregated = {}
        for row in all_results:
            pid, revenue = row
            aggregated[pid] = aggregated.get(pid, 0) + revenue
        
        # Top N
        return sorted(aggregated.items(), key=lambda x: -x[1])[:limit]
```

### 3. Distributed Transactions

```python
# Two-phase commit cho cross-shard transactions
class DistributedTransaction:
    def __init__(self, router):
        self.router = router
        self.coordinator = coordinator
    
    def begin(self):
        self.transaction_id = self.coordinator.create_transaction()
        self.shard_connections = {}
        self.participants = []
    
    def prepare(self, shard_id, operations):
        """Phase 1: Prepare trên all involved shards"""
        if shard_id not in self.shard_connections:
            conn = self.router.get_connection(shard_id)
            self.shard_connections[shard_id] = conn
            conn.begin()
        
        for op in operations:
            self.execute_operation(shard_id, op)
        
        # Prepare (xaact)
        conn = self.shard_connections[shard_id]
        conn.query("XA PREPARE xid_{}".format(self.transaction_id))
        self.participants.append(shard_id)
    
    def commit(self):
        """Phase 2: Commit trên all participants"""
        success = True
        for shard_id in self.participants:
            try:
                conn = self.shard_connections[shard_id]
                conn.query("XA COMMIT xid_{}".format(self.transaction_id))
            except Exception as e:
                logger.error(f"Commit failed on shard {shard_id}: {e}")
                success = False
        
        return success
    
    def rollback(self):
        """Rollback all participants"""
        for shard_id, conn in self.shard_connections.items():
            try:
                conn.rollback()
            except Exception as e:
                logger.error(f"Rollback failed on shard {shard_id}: {e}")
```

### 4. Rebalancing Shards

```python
# Rebalance data khi thêm shard mới
def rebalance_shards(router, source_shard, target_shard, batch_size=1000):
    """
    Move data từ source shard sang target shard
    """
    source_conn = router.get_connection(source_shard)
    target_conn = router.get_connection(target_shard)
    
    # Calculate new shard assignment
    num_shards = router.num_shards + 1
    
    # Batch move để minimize lock contention
    offset = 0
    while True:
        # Read batch from source
        query = """
            SELECT * FROM orders 
            WHERE customer_id % {} = {}  -- New shard assignment
            LIMIT {} OFFSET {}
        """.format(num_shards, target_shard, batch_size, offset)
        
        rows = source_conn.query(query)
        if not rows:
            break
        
        # Insert into target
        for row in rows:
            target_conn.insert('orders', row)
        
        # Delete from source
        ids = [row['order_id'] for row in rows]
        source_conn.query(
            "DELETE FROM orders WHERE order_id IN ({})".format(ids),
            ids
        )
        
        # Commit batch
        source_conn.commit()
        target_conn.commit()
        
        offset += batch_size
        print(f"Moved {offset} rows...")
```

## Các Common Patterns

### Pattern 1: Tenant-based Sharding (Multi-tenant SaaS)

```sql
-- Mỗi tenant có shard riêng
-- Shard naming: tenant_{tenant_id}

CREATE TABLE global_tenant_map (
    tenant_id INT PRIMARY KEY,
    shard_name VARCHAR(100),
    created_at TIMESTAMP,
    status ENUM('active', 'suspended', 'deleted')
);

-- Application routing
class TenantRouter:
    def get_shard_for_tenant(self, tenant_id):
        result = db.query(
            "SELECT shard_name FROM global_tenant_map WHERE tenant_id = ?",
            tenant_id
        )
        if result:
            return result[0]['shard_name']
        return self._default_shard(tenant_id)
    
    def _default_shard(self, tenant_id):
        # Hash-based fallback
        shard_num = tenant_id % 10
        return f'tenant_shard_{shard_num}'
```

### Pattern 2: Time-series Sharding

```sql
-- Shard theo tháng hoặc quý
CREATE TABLE time_shard_config (
    shard_name VARCHAR(100) PRIMARY KEY,
    start_date DATE,
    end_date DATE,
    status ENUM('active', 'readonly', 'archived')
);

-- Config for orders
INSERT INTO time_shard_config VALUES
('orders_2024_q1', '2024-01-01', '2024-03-31', 'readonly'),
('orders_2024_q2', '2024-04-01', '2024-06-30', 'readonly'),
('orders_2024_q3', '2024-07-01', '2024-09-30', 'active'),
('orders_2024_q4', '2024-10-01', '2024-12-31', 'active');

-- Routing function
def get_order_shard(order_date):
    if order_date < '2024-04-01':
        return 'orders_2024_q1'
    elif order_date < '2024-07-01':
        return 'orders_2024_q2'
    # ... etc
```

### Pattern 3: Hierarchical Sharding

```sql
-- Shard by region, then by user range
-- Region: US, EU, APAC
-- Within region: User ranges

CREATE TABLE hierarchical_shard_map (
    region VARCHAR(10),
    user_range_start BIGINT,
    user_range_end BIGINT,
    shard_name VARCHAR(100),
    PRIMARY KEY (region, user_range_start)
);

INSERT INTO hierarchical_shard_map VALUES
('US', 1, 1000000, 'us_users_0'),
('US', 1000001, 2000000, 'us_users_1'),
('EU', 1, 500000, 'eu_users_0'),
('EU', 500001, 1000000, 'eu_users_1'),
('APAC', 1, 2000000, 'apac_users_0');

-- Query routing
def get_user_shard(region, user_id):
    result = db.query("""
        SELECT shard_name FROM hierarchical_shard_map 
        WHERE region = ? AND user_range_start <= ? AND user_range_end >= ?
    """, region, user_id, user_id)
    return result[0]['shard_name'] if result else 'default_shard'
```

## Troubleshooting

### Vấn đề 1: Data Skew (Hot Shards)

**Symptom**: Một shard có quá nhiều data hoặc queries, trong khi shards khác underutilized.

**Diagnosis**:
```sql
-- Kiểm tra data distribution
SELECT 
    shard_id,
    COUNT(*) AS row_count,
    AVG(row_size) AS avg_size,
    MAX(row_size) AS max_size
FROM information_schema.tables
GROUP BY shard_id;

-- Kiểm tra query distribution
SELECT 
    shard_id,
    COUNT(*) AS query_count,
    AVG(execution_time_ms) AS avg_time
FROM query_log
GROUP BY shard_id;
```

**Solutions**:

1. **Choose better shard key** với higher cardinality
2. **Virtual shards**: Partition large physical shards
3. **Move hot data to dedicated shard**
4. **Implement caching cho hot data**

### Vấn đề 2: Cross-shard Deadlocks

**Symptom**: Transactions timeout khi cần lock resources trên multiple shards.

**Diagnosis**:
```python
# Log cross-shard transactions
def detect_cross_shard_txn(operations):
    affected_shards = set(op.shard_id for op in operations)
    if len(affected_shards) > 1:
        logger.warning(f"Cross-shard transaction: {affected_shards}")
    return affected_shards
```

**Solutions**:

1. **Reduce cross-shard transactions** bằng cách redesign schema
2. **Use eventually consistent** patterns thay vì distributed transactions
3. **Implement retry logic** với exponential backoff
4. **Consider Saga pattern** cho distributed workflows

### Vấn đề 3: Rebalancing Complexity

**Symptom**: Thêm shard mới gây ra inconsistent data hoặc application errors.

**Solutions**:

1. **Use consistent hashing** để minimize remapping
2. **Follow proper rebalancing steps**:
   - Add new shard (read-only initially)
   - Migrate data in batches
   - Verify data integrity
   - Switchover traffic
   - Decommission old shard
3. **Test thoroughly** trong staging environment
4. **Have rollback plan** sẵn sàng

## Ví dụ Thực tế

### Ví dụ 1: Complete Sharding Implementation

```python
# Complete application with sharding
# file: app/sharding/__init__.py

from app.sharding.router import ShardRouter
from app.sharding.manager import ShardManager
from app.sharding.query_builder import ShardQueryBuilder

__all__ = ['ShardRouter', 'ShardManager', 'ShardQueryBuilder']
```

```python
# app/sharding/router.py
import hashlib
from typing import Optional, List, Dict
from contextlib import contextmanager

class ShardRouter:
    """Central shard routing logic"""
    
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.shards: Dict[int, Dict] = {
            s['id']: s for s in self.config['shards']
        }
        self.num_shards = len(self.shards)
    
    def _load_config(self, path: str) -> dict:
        import yaml
        with open(path) as f:
            return yaml.safe_load(f)
    
    def get_shard_id(self, key_value: any, key_type: str = 'hash') -> int:
        """Determine shard ID for a key value"""
        if key_type == 'hash':
            key_hash = int(hashlib.md5(str(key_value).encode()).hexdigest(), 16)
            return key_hash % self.num_shards
        elif key_type == 'range':
            return self._range_shard_id(key_value)
        return 0
    
    def get_shard_connection(self, shard_id: int):
        """Get database connection for shard"""
        import mysql.connector
        shard = self.shards.get(shard_id)
        return mysql.connector.connect(
            host=shard['host'],
            port=shard['port'],
            database=shard['database'],
            user=self.config['db_user'],
            password=self.config['db_password'],
            pool_name=f"pool_shard_{shard_id}",
            pool_size=10
        )
    
    @contextmanager
    def connection(self, shard_id: int):
        """Context manager for shard connection"""
        conn = self.get_shard_connection(shard_id)
        try:
            yield conn
        finally:
            conn.close()
    
    def execute_on_shard(self, shard_id: int, query: str, params: tuple = None):
        """Execute query on specific shard"""
        with self.connection(shard_id) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            return cursor.fetchall()
```

```python
# app/sharding/manager.py
class ShardManager:
    """Manage shard lifecycle operations"""
    
    def __init__(self, router: ShardRouter):
        self.router = router
    
    def add_shard(self, config: dict):
        """Add new shard to cluster"""
        shard_id = config['id']
        
        # 1. Create database on new server
        self._create_database(shard_id, config)
        
        # 2. Create schema
        self._create_schema(shard_id)
        
        # 3. Add to router
        self.router.shards[shard_id] = config
        self.router.num_shards += 1
        
        # 4. Update config file
        self._save_config()
    
    def move_data(self, source_shard: int, target_shard: int, 
                  batch_size: int = 1000):
        """Move data between shards for rebalancing"""
        query = """
            SELECT * FROM {} 
            WHERE {} % {} = {}
            LIMIT {}
        """
        
        offset = 0
        while True:
            rows = self.router.execute_on_shard(
                source_shard,
                query.format(
                    'orders',
                    'customer_id',
                    self.router.num_shards + 1,
                    target_shard
                ) + f' OFFSET {offset}'
            )
            
            if not rows:
                break
            
            # Insert to target
            self._batch_insert(target_shard, 'orders', rows)
            
            # Delete from source
            ids = [r[0] for r in rows]
            self.router.execute_on_shard(
                source_shard,
                f"DELETE FROM orders WHERE order_id IN ({ids})"
            )
            
            offset += batch_size
    
    def health_check(self):
        """Check health of all shards"""
        results = {}
        for shard_id in self.router.shards:
            try:
                result = self.router.execute_on_shard(
                    shard_id,
                    "SELECT 1 AS health"
                )
                results[shard_id] = {
                    'status': 'healthy',
                    'latency_ms': result[0][0]
                }
            except Exception as e:
                results[shard_id] = {
                    'status': 'unhealthy',
                    'error': str(e)
                }
        return results
```

### Ví dụ 2: Migration Script

```bash
#!/bin/bash
# migrate_to_sharded.sh

set -e

NUM_SHARDS=4
SOURCE_DB="legacy_db"
SOURCE_TABLE="orders"

echo "=== Migration to Sharded Schema ==="

# Step 1: Create sharded tables
for i in $(seq 0 $((NUM_SHARDS-1))); do
    echo "Creating shard_${i}.${SOURCE_TABLE}..."
    mysql -e "
        CREATE DATABASE IF NOT EXISTS shard_${i};
        USE shard_${i};
        CREATE TABLE ${SOURCE_TABLE} (
            order_id BIGINT PRIMARY KEY,
            customer_id INT NOT NULL,
            order_date DATE,
            total DECIMAL(10,2),
            INDEX idx_customer (customer_id),
            INDEX idx_date (order_date)
        ) ENGINE=InnoDB;
    "
done

# Step 2: Migrate data in batches
BATCH_SIZE=10000
OFFSET=0

while true; do
    echo "Migrating batch starting at offset $OFFSET..."
    
    mysql -N -e "
        SELECT CONCAT(
            order_id, '|',
            customer_id, '|',
            order_date, '|',
            total
        ) FROM ${SOURCE_DB}.${SOURCE_TABLE}
        LIMIT ${BATCH_SIZE} OFFSET ${OFFSET}
    " | while IFS='|' read -r order_id customer_id order_date total; do
        shard_id=$((customer_id % NUM_SHARDS))
        mysql -e "
            INSERT INTO shard_${shard_id}.${SOURCE_TABLE}
            (order_id, customer_id, order_date, total)
            VALUES (${order_id}, ${customer_id}, '${order_date}', ${total})
            ON DUPLICATE KEY UPDATE total=${total};
        "
    done
    
    OFFSET=$((OFFSET + BATCH_SIZE))
    
    if [ $OFFSET -ge $(mysql -N -e "SELECT COUNT(*) FROM ${SOURCE_DB}.${SOURCE_TABLE}") ]; then
        break
    fi
done

# Step 3: Verify
echo "=== Verification ==="
for i in $(seq 0 $((NUM_SHARDS-1))); do
    count=$(mysql -N -e "SELECT COUNT(*) FROM shard_${i}.${SOURCE_TABLE}")
    echo "Shard ${i}: ${count} rows"
done
```

## Tham khảo

### Official Documentation

- [MySQL Partitioning](https://dev.mysql.com/doc/refman/8.0/en/partitioning.html)
- [ProxySQL Documentation](https://proxysql.com/documentation/)
- [Vitess Documentation](https://vitess.io/docs/)

### Tools

- **MySQL Fabric**: MySQL's official sharding solution (deprecated in MySQL 8.0)
- **ProxySQL**: Advanced SQL proxy với query routing
- **Vitess**: YouTube's database clustering system
- **Citus**: PostgreSQL sharding extension (inspiration for patterns)
- **ScaleArc**: Commercial SQL routing and sharding

### Libraries

- **PyMySQL**: Pure Python MySQL client
- **mysql-connector-python**: Official MySQL connector
- **SQLAlchemy**: ORM với sharding support

### Books

- "Designing Data-Intensive Applications" - Chapter on partitioning
- "Scalable Web Architecture" - Sharding patterns

---

*Document version: 1.0.0*
*Last updated: 2026-06-23*
*Framework: Cursor Enterprise Framework*
