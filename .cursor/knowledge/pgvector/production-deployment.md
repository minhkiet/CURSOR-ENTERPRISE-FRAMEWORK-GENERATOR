---
title: "pgvector Production Deployment"
description: "Hướng dẫn triển khai pgvector trong production: connection pooling, index warm-up, monitoring và backup strategies"
tags: ["production", "pgvector", "deployment", "monitoring", "backup", "connection-pooling"]
created: "2026-06-23"
version: "1.0.0"
framework: "Cursor Enterprise Framework"
---

# pgvector Production Deployment

## Tổng Quan

Việc triển khai pgvector trong production environment đòi hỏi nhiều hơn việc chỉ cài đặt extension và tạo indexes. Để đảm bảo hệ thống hoạt động ổn định với hiệu suất cao, chúng ta cần quan tâm đến các khía cạnh như connection pooling, index warm-up, monitoring, backup, và capacity planning.

pgvector có thể xử lý hàng triệu vectors với latency thấp, nhưng điều đó chỉ đạt được khi được configure đúng cách cho production workloads. Connection pooling đặc biệt quan trọng vì mỗi vector search operation có thể tốn nhiều memory và CPU.

Tài liệu này cung cấp comprehensive guide cho production deployment, từ initial setup đến ongoing operations và maintenance.

## Mục Đích

Tài liệu này nhằm cung cấp kiến thức toàn diện về production deployment của pgvector:

Đầu tiên, chúng ta sẽ tìm hiểu về connection pooling với PgBouncer và các configurations tối ưu cho vector workloads.

Thứ hai, tài liệu hướng dẫn các chiến lược index warm-up để đạt được consistent latency ngay sau deployment hoặc restart.

Thứ ba, chúng ta sẽ đề cập đến vacuum và ANALYZE operations để maintain index health.

Cuối cùng, tài liệu cung cấp monitoring setup và backup strategies cho production environment.

## Key Concepts

### 1. Connection Pooling với PgBouncer

PgBouncer là connection pooler phổ biến nhất cho PostgreSQL, giúp reduce connection overhead và improve throughput.

```ini
; pgbouncer.ini
[databases]
; Database configuration
production = host=localhost dbname=vector_db port=5432

; PgBouncer admin database
pgbouncer = host=localhost dbname=pgbouncer port=6432

[pgbouncer]
; Connection pool mode
pool_mode = transaction  ; Transaction mode is best for vector workloads
max_client_conn = 1000
default_pool_size = 50   ; Adjust based on PostgreSQL max_connections
min_pool_size = 10
reserve_pool_size = 10
reserve_pool_timeout = 3

; Timeouts
query_timeout = 60
idle_transaction_timeout = 300

; Performance
server_lifetime = 3600
server_idle_timeout = 600
```

```sql
-- PostgreSQL configuration for PgBouncer
ALTER SYSTEM SET max_connections = 200;
ALTER SYSTEM SET shared_buffers = '8GB';
ALTER SYSTEM SET effective_cache_size = '24GB';
ALTER SYSTEM SET work_mem = '256MB';
ALTER SYSTEM SET maintenance_work_mem = '2GB';
```

### 2. Index Warm-up

Vector indexes (đặc biệt là HNSW) cần được "warm up" sau restart để đạt được performance tối ưu.

```sql
-- Warm-up function cho vector indexes
CREATE OR REPLACE FUNCTION warmup_vector_indexes()
RETURNS TABLE(
    index_name TEXT,
    rows_scanned BIGINT,
    duration_ms FLOAT
) AS $$
DECLARE
    v_start_time TIMESTAMP;
    v_index_name TEXT;
    v_rows_scanned BIGINT;
    v_duration INTERVAL;
BEGIN
    FOR v_index_name IN (
        SELECT indexname 
        FROM pg_indexes 
        WHERE tablename = 'document_chunks'
          AND (indexname LIKE '%hnsw%' OR indexname LIKE '%ivfflat%')
    )
    LOOP
        v_start_time := clock_timestamp();
        
        -- Force index scan và cache loading
        EXECUTE format(
            'SELECT COUNT(*) FROM document_chunks WHERE embedding <=> $1::vector < 2',
            array_to_string(array(
                SELECT random()::text FROM generate_series(1, 768)
            ), ',')
        ) INTO v_rows_scanned;
        
        v_duration := clock_timestamp() - v_start_time;
        
        RETURN QUERY
        SELECT 
            v_index_name::TEXT,
            v_rows_scanned::BIGINT,
            EXTRACT(MILLISECONDS FROM v_duration)::FLOAT;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Scheduled warmup (via pg_cron or external scheduler)
SELECT cron.schedule(
    'warmup-vector-indexes',
    '0 6 * * *',  -- Daily at 6 AM
    'SELECT warmup_vector_indexes()'
);
```

### 3. Vacuum và ANALYZE

Regular vacuum và analyze operations là essential cho maintain performance.

```sql
-- Configure autovacuum for vector tables
ALTER TABLE document_chunks SET (
    autovacuum_vacuum_threshold = 50,
    autovacuum_analyze_threshold = 50,
    autovacuum_vacuum_cost_delay = 2,
    autovacuum_vacuum_cost_limit = 1000
);

-- Manual vacuum với index maintenance
CREATE OR REPLACE FUNCTION maintain_vector_tables(
    p_vacuum BOOLEAN DEFAULT TRUE,
    p_analyze BOOLEAN DEFAULT TRUE,
    p_reindex BOOLEAN DEFAULT FALSE
) RETURNS TABLE(
    operation TEXT,
    table_name TEXT,
    duration_ms FLOAT
) AS $$
DECLARE
    v_start_time TIMESTAMP;
    v_tables TEXT[] := ARRAY['documents', 'document_chunks', 'embedding_jobs'];
    v_table TEXT;
BEGIN
    FOREACH v_table IN ARRAY v_tables LOOP
        v_start_time := clock_timestamp();
        
        IF p_vacuum THEN
            EXECUTE format('VACUUM (VERBOSE, ANALYZE) %I', v_table);
        END IF;
        
        RETURN QUERY
        SELECT 
            'vacuum'::TEXT,
            v_table::TEXT,
            EXTRACT(MILLISECONDS FROM (clock_timestamp() - v_start_time))::FLOAT;
        
        IF p_reindex THEN
            v_start_time := clock_timestamp();
            
            IF v_table = 'document_chunks' THEN
                EXECUTE format('REINDEX INDEX CONCURRENTLY %I', 'idx_chunks_embedding');
            END IF;
            
            RETURN QUERY
            SELECT 
                'reindex'::TEXT,
                v_table::TEXT,
                EXTRACT(MILLISECONDS FROM (clock_timestamp() - v_start_time))::FLOAT;
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Schedule maintenance
SELECT cron.schedule(
    'vector-maintenance',
    '0 3 * * *',  -- Daily at 3 AM
    'SELECT maintain_vector_tables(true, true, false)'
);
```

## Connection Pooling Configuration

### 1. Application-side Pooling

```python
# Python example với connection pooling
import psycopg2
from psycopg2 import pool
from contextlib import contextmanager

class VectorDBPool:
    def __init__(self, min_conn=5, max_conn=20):
        self.pool = psycopg2.pool.ThreadedConnectionPool(
            min_conn, max_conn,
            host="localhost",
            database="vector_db",
            user="postgres",
            password="password",
            port=5432
        )
    
    @contextmanager
    def get_connection(self):
        conn = self.pool.getconn()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            self.pool.putconn(conn)
    
    def execute_query(self, query, params=None):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return cur.fetchall()

# Usage
db_pool = VectorDBPool(min_conn=10, max_conn=50)
results = db_pool.execute_query(
    "SELECT * FROM items ORDER BY embedding <=> %s LIMIT 10",
    ([0.1, 0.2] + [0.0] * 1534,)  # 1536 dimensions
)
```

### 2. Transaction vs Session Pooling

```ini
; Transaction mode (recommended for most vector workloads)
; Each query gets its own connection within a transaction
pool_mode = transaction

; Session mode (use for stored procedures that need session state)
pool_mode = session
```

```sql
-- Test pooling efficiency
SELECT 
    datname,
    numbackends,
    xact_commit,
    xact_rollback,
    blks_read,
    blks_hit,
    ROUND(100.0 * blks_hit / NULLIF(blks_hit + blks_read, 0), 2) AS cache_hit_ratio
FROM pg_stat_database
WHERE datname = 'vector_db';
```

## Monitoring Setup

### 1. Performance Metrics Collection

```sql
-- Create metrics table
CREATE TABLE vector_metrics (
    id BIGSERIAL PRIMARY KEY,
    collected_at TIMESTAMPTZ DEFAULT NOW(),
    metric_category VARCHAR(50),
    metric_name VARCHAR(100),
    metric_value FLOAT,
    metadata JSONB DEFAULT '{}'
);

-- Index for efficient querying
CREATE INDEX idx_vector_metrics_time ON vector_metrics (collected_at DESC);
CREATE INDEX idx_vector_metrics_name ON vector_metrics (metric_category, metric_name);

-- Collect metrics function
CREATE OR REPLACE FUNCTION collect_vector_metrics()
RETURNS VOID AS $$
BEGIN
    -- Query performance metrics
    INSERT INTO vector_metrics (metric_category, metric_name, metric_value, metadata)
    SELECT 
        'query',
        'avg_latency_ms',
        AVG(mean_exec_time * 1000),
        jsonb_build_object('backend_type', 'client backend')
    FROM pg_stat_statements s
    JOIN pg_database d ON d.oid = s.dbid
    WHERE d.datname = current_database()
      AND query LIKE '%<=>%';
    
    -- Index size metrics
    INSERT INTO vector_metrics (metric_category, metric_name, metric_value)
    SELECT 
        'storage',
        'index_size_mb',
        SUM(pg_relation_size(indexrelid)) / 1024 / 1024
    FROM pg_stat_user_indexes
    WHERE indexname LIKE '%hnsw%' OR indexname LIKE '%ivfflat%';
    
    -- Table size metrics
    INSERT INTO vector_metrics (metric_category, metric_name, metric_value)
    SELECT 
        'storage',
        'table_size_mb',
        pg_total_relation_size('document_chunks') / 1024 / 1024
    FROM pg_class
    WHERE relname = 'document_chunks';
    
    -- Row count metrics
    INSERT INTO vector_metrics (metric_category, metric_name, metric_value)
    SELECT 
        'data',
        'row_count',
        COUNT(*)
    FROM document_chunks;
    
    -- Pending jobs metrics
    INSERT INTO vector_metrics (metric_category, metric_name, metric_value)
    SELECT 
        'jobs',
        'pending_embeddings',
        COUNT(*)
    FROM embedding_jobs
    WHERE status = 'pending';
END;
$$ LANGUAGE plpgsql;

-- Schedule metrics collection
SELECT cron.schedule(
    'collect-vector-metrics',
    '*/5 * * * *',
    'SELECT collect_vector_metrics()'
);
```

### 2. Dashboard Queries

```sql
-- Latency distribution
CREATE OR REPLACE FUNCTION get_latency_distribution(
    p_hours INTEGER DEFAULT 24
) RETURNS TABLE(
    percentile FLOAT,
    latency_ms FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        50.0 as percentile,
        PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY latency_ms) as latency_ms
    FROM query_logs
    WHERE created_at > NOW() - (p_hours || ' hours')::interval
    
    UNION ALL
    
    SELECT 
        95.0 as percentile,
        PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY latency_ms) as latency_ms
    FROM query_logs
    WHERE created_at > NOW() - (p_hours || ' hours')::interval
    
    UNION ALL
    
    SELECT 
        99.0 as percentile,
        PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY latency_ms) as latency_ms
    FROM query_logs
    WHERE created_at > NOW() - (p_hours || ' hours')::interval;
END;
$$ LANGUAGE plpgsql;

-- QPS over time
CREATE OR REPLACE FUNCTION get_qps_trend(
    p_hours INTEGER DEFAULT 24
) RETURNS TABLE(
    time_bucket TIMESTAMPTZ,
    queries_per_second FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        date_trunc('minute', created_at) as time_bucket,
        COUNT(*)::float / 60 as qps
    FROM query_logs
    WHERE created_at > NOW() - (p_hours || ' hours')::interval
    GROUP BY date_trunc('minute', created_at)
    ORDER BY time_bucket;
END;
$$ LANGUAGE plpgsql;
```

### 3. Alerting Configuration

```sql
-- Alert thresholds
CREATE TABLE alert_thresholds (
    id SERIAL PRIMARY KEY,
    metric_name VARCHAR(100),
    warning_threshold FLOAT,
    critical_threshold FLOAT,
    comparison VARCHAR(10) DEFAULT '>',  -- > or <
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Default thresholds
INSERT INTO alert_thresholds (metric_name, warning_threshold, critical_threshold)
VALUES 
    ('avg_latency_ms', 100, 500),
    ('p99_latency_ms', 200, 1000),
    ('cache_hit_ratio', 95, 90),
    ('pending_embeddings', 1000, 5000),
    ('failed_jobs', 10, 100);

-- Check thresholds
CREATE OR REPLACE FUNCTION check_alerts()
RETURNS TABLE(
    alert_level TEXT,
    metric_name TEXT,
    current_value FLOAT,
    threshold FLOAT
) AS $$
BEGIN
    RETURN QUERY
    -- High latency alert
    SELECT 
        CASE 
            WHEN AVG(mean_exec_time * 1000) > c.critical_threshold THEN 'critical'
            WHEN AVG(mean_exec_time * 1000) > c.warning_threshold THEN 'warning'
        END as alert_level,
        'avg_latency_ms' as metric_name,
        AVG(mean_exec_time * 1000) as current_value,
        c.warning_threshold as threshold
    FROM pg_stat_statements s
    CROSS JOIN alert_thresholds c
    WHERE c.metric_name = 'avg_latency_ms'
      AND query LIKE '%<=>%'
    GROUP BY c.warning_threshold, c.critical_threshold
    HAVING AVG(mean_exec_time * 1000) > c.warning_threshold;
    
    -- Similar checks for other metrics...
END;
$$ LANGUAGE plpgsql;
```

## Backup Strategies

### 1. pg_dump Configuration

```bash
#!/bin/bash
# backup-vector-db.sh

# Configuration
BACKUP_DIR="/backups/vector-db"
RETENTION_DAYS=30
DB_NAME="vector_db"
DB_USER="postgres"

# Create backup
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/vector_db_${TIMESTAMP}.sql.gz"

# Full dump including vectors
pg_dump -U $DB_USER -d $DB_NAME \
    --format=custom \
    --compress=9 \
    --file=${BACKUP_FILE} \
    --schema=public

# Create symbolic link to latest
ln -sf ${BACKUP_FILE} ${BACKUP_DIR}/latest.dump

# Clean old backups
find $BACKUP_DIR -name "*.dump" -mtime +$RETENTION_DAYS -delete

# Verify backup
pg_restore --list ${BACKUP_FILE} | head -20

echo "Backup completed: $BACKUP_FILE"
```

### 2. Incremental Backup với WAL

```ini
# postgresql.conf

# WAL configuration for point-in-time recovery
wal_level = replica
max_wal_senders = 5
max_replication_slots = 5
wal_keep_size = 1GB

# Archive configuration
archive_mode = on
archive_command = 'cp %p /archive/wal/%f'
archive_timeout = 300  -- 5 minutes
```

```bash
#!/bin/bash
# restore-point-in-time.sh

TARGET_TIME="2024-01-15 14:30:00"
BACKUP_DIR="/backups/vector-db"
ARCHIVE_DIR="/archive/wal"

# Stop PostgreSQL
pg_ctl stop -D /var/lib/postgresql/data

# Restore base backup
rm -rf /var/lib/postgresql/data/*
tar -xzf ${BACKUP_DIR}/latest.tar.gz -C /var/lib/postgresql/data/

# Create recovery configuration
cat > /var/lib/postgresql/data/recovery.conf <<EOF
restore_command = 'cp ${ARCHIVE_DIR}/%f %p'
recovery_target_time = '${TARGET_TIME}'
recovery_target_action = 'promote'
EOF

# Start PostgreSQL
pg_ctl start -D /var/lib/postgresql/data
```

### 3. Selective Backup cho Large Datasets

```sql
-- Backup chỉ metadata, rebuild vectors from source
CREATE OR REPLACE FUNCTION export_vector_metadata()
RETURNS TABLE(
    document_id UUID,
    chunk_id UUID,
    chunk_text TEXT,
    metadata JSONB,
    original_source TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        d.id as document_id,
        dc.id as chunk_id,
        dc.chunk_text,
        dc.metadata,
        d.source_url
    FROM document_chunks dc
    JOIN documents d ON dc.document_id = d.id
    WHERE d.status = 'indexed';
END;
$$ LANGUAGE plpgsql;

-- Export to file
\copy (SELECT * FROM export_vector_metadata()) TO '/backup/metadata.csv' WITH CSV HEADER

-- Import và regenerate embeddings
CREATE OR REPLACE FUNCTION import_from_backup(
    p_csv_path TEXT
) RETURNS INTEGER AS $$
DECLARE
    v_count INTEGER := 0;
BEGIN
    -- Create temp table
    CREATE TEMP TABLE temp_backup (
        document_id UUID,
        chunk_text TEXT,
        metadata JSONB,
        source_url TEXT
    );
    
    -- Copy from file
    EXECUTE format('COPY temp_backup FROM %L WITH CSV HEADER', p_csv_path);
    
    -- Insert documents
    INSERT INTO documents (id, content, source_url, status)
    SELECT DISTINCT document_id, chunk_text, source_url, 'processing'
    FROM temp_backup
    ON CONFLICT DO NOTHING;
    
    -- Count chunks
    SELECT COUNT(*) INTO v_count FROM temp_backup;
    
    -- Queue re-embedding jobs
    INSERT INTO embedding_jobs (chunk_id)
    SELECT id FROM document_chunks dc
    JOIN temp_backup tb ON dc.document_id = tb.document_id
    WHERE dc.embedding IS NULL;
    
    DROP TEMP TABLE temp_backup;
    
    RETURN v_count;
END;
$$ LANGUAGE plpgsql;
```

## High Availability Setup

### 1. Streaming Replication

```ini
# postgresql.conf (primary)
wal_level = replica
max_wal_senders = 3
max_replication_slots = 3
wal_keep_size = 1GB

# Create replication user
-- CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD 'secret';

# pg_hba.conf (primary)
host replication replicator 192.168.1.0/24 scram-sha-256
```

```ini
# postgresql.conf (replica)
primary_conninfo = 'host=primary.example.com port=5432 user=replicator'
recovery_target_timeline = 'latest'
hot_standby = on
```

```bash
# Create base backup on replica
pg_basebackup -h primary.example.com -U replicator \
    -D /var/lib/postgresql/15/main \
    -R -P -Xs -Fast
```

### 2. Failover Configuration

```sql
-- pgpool-II or patroni for automatic failover
-- Example: Patroni configuration

{
  "name": "vector-pg-1",
  "scope": "vector-cluster",
  "api": {
    "port": 8008
  },
  "postgresql": {
    "data_dir": "/var/lib/postgresql/data",
    "parameters": {
      "max_connections": 200,
      "shared_buffers": "8GB",
      "effective_cache_size": "24GB",
      "work_mem": "256MB",
      "maintenance_work_mem": "2GB"
    },
    "pg_hba": [
      "host all all 0.0.0.0/0 scram-sha-256"
    ]
  },
  "consul": {
    "host": "consul.example.com:8500",
    "register_service": true,
    "service_port": 5432
  }
}
```

## Capacity Planning

### 1. Resource Estimation

```sql
-- Estimate index size trước khi tạo
CREATE OR REPLACE FUNCTION estimate_vector_index_size(
    p_row_count BIGINT,
    p_dimension INTEGER,
    p_index_type VARCHAR DEFAULT 'hnsw'
) RETURNS TABLE(
    metric_name TEXT,
    estimate_mb FLOAT
) AS $$
DECLARE
    v_vector_size_bytes INTEGER := p_dimension * 4;  -- float32
    v_m INTEGER := 16;
    v_ef_construction INTEGER := 200;
    v_base_index_size_mb FLOAT;
    v_per_vector_overhead_mb FLOAT;
BEGIN
    IF p_index_type = 'hnsw' THEN
        -- Rough HNSW size estimation
        -- Base index: ~3x raw vector data
        v_base_index_size_mb := (p_row_count * v_vector_size_bytes::bigint) / 1024 / 1024 * 3;
        -- Per-vector overhead
        v_per_vector_overhead_mb := (v_m * v_vector_size_bytes::bigint) / 1024 / 1024 * 2;
        
        RETURN QUERY
        SELECT 'base_index_mb'::TEXT, v_base_index_size_mb
        UNION ALL
        SELECT 'overhead_mb'::TEXT, v_per_vector_overhead_mb
        UNION ALL
        SELECT 'total_estimate_mb'::TEXT, v_base_index_size_mb + v_per_vector_overhead_mb
        UNION ALL
        SELECT 'total_estimate_gb'::TEXT, (v_base_index_size_mb + v_per_vector_overhead_mb) / 1024;
    ELSE
        -- IVFFlat estimation
        v_base_index_size_mb := (p_row_count * v_vector_size_bytes::bigint) / 1024 / 1024 * 1.2;
        
        RETURN QUERY
        SELECT 'base_index_mb'::TEXT, v_base_index_size_mb
        UNION ALL
        SELECT 'total_estimate_gb'::TEXT, v_base_index_size_mb / 1024;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Example: Estimate for 10M vectors, 1536 dimensions
SELECT * FROM estimate_vector_index_size(10000000, 1536, 'hnsw');
```

### 2. Scaling Guidelines

```sql
-- Guidelines table
CREATE TABLE scaling_recommendations (
    dataset_size VARCHAR(50),
    recommended_config JSONB,
    expected_qps INTEGER,
    notes TEXT
);

INSERT INTO scaling_recommendations VALUES
('100K vectors', '{"memory": "8GB", "connections": 25, "index_type": "hnsw"}', 1000, 'Small dataset, single instance sufficient'),
('1M vectors', '{"memory": "32GB", "connections": 50, "index_type": "hnsw"}', 500, 'Medium dataset, consider read replicas'),
('10M vectors', '{"memory": "128GB", "connections": 100, "index_type": "hnsw"}', 200, 'Large dataset, partitioning recommended'),
('100M vectors', '{"memory": "512GB", "connections": 200, "index_type": "hnsw+pq"}', 50, 'Very large, consider sharding or dedicated vector DB');
```

## Examples

### Example 1: Complete Production Setup Script

```sql
-- Production setup script
DO $$
BEGIN
    -- Create extensions
    CREATE EXTENSION IF NOT EXISTS vector;
    CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
    CREATE EXTENSION IF NOT EXISTS pg_cron;
    
    -- Configure PostgreSQL parameters
    ALTER SYSTEM SET max_connections = 200;
    ALTER SYSTEM SET shared_buffers = '8GB';
    ALTER SYSTEM SET effective_cache_size = '24GB';
    ALTER SYSTEM SET work_mem = '256MB';
    ALTER SYSTEM SET maintenance_work_mem = '2GB';
    ALTER SYSTEM SET random_page_cost = 1.1;
    ALTER SYSTEM SET effective_io_concurrency = 200;
    ALTER SYSTEM SET max_parallel_workers_per_gather = 4;
    ALTER SYSTEM SET max_parallel_workers = 4;
    
    -- Create optimized tables
    CREATE TABLE IF NOT EXISTS production_embeddings (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        entity_id UUID NOT NULL,
        entity_type VARCHAR(50) NOT NULL,
        embedding VECTOR(1536) NOT NULL,
        metadata JSONB DEFAULT '{}',
        created_at TIMESTAMPTZ DEFAULT NOW(),
        
        CONSTRAINT unique_entity_embedding UNIQUE (entity_id, entity_type)
    ) WITH (
        fillfactor = 90,
        autovacuum_vacuum_threshold = 100,
        autovacuum_analyze_threshold = 100
    );
    
    -- Create indexes
    CREATE INDEX IF NOT EXISTS idx_embeddings_hnsw ON production_embeddings 
        USING hnsw (embedding vector_cosine_ops) 
        WITH (m = 16, ef_construction = 200);
    
    CREATE INDEX IF NOT EXISTS idx_embeddings_entity ON production_embeddings (entity_id, entity_type);
    CREATE INDEX IF NOT EXISTS idx_embeddings_created ON production_embeddings (created_at DESC);
    
    -- Create metrics table
    CREATE TABLE IF NOT EXISTS production_metrics (
        id BIGSERIAL PRIMARY KEY,
        collected_at TIMESTAMPTZ DEFAULT NOW(),
        metric_name VARCHAR(100),
        metric_value FLOAT,
        metadata JSONB DEFAULT '{}'
    );
    
    -- Create indexes for metrics
    CREATE INDEX IF NOT EXISTS idx_metrics_time ON production_metrics (collected_at DESC);
    
    -- Grant permissions
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO app_user;
    GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO app_user;
    
    RAISE NOTICE 'Production setup completed successfully';
END $$;

-- Configure pg_cron
SELECT cron.schedule('collect-metrics', '*/5 * * * *', 
    'INSERT INTO production_metrics (metric_name, metric_value) SELECT ''vector_count'', COUNT(*) FROM production_embeddings');
```

### Example 2: Health Check và Auto-recovery

```sql
-- Health check function
CREATE OR REPLACE FUNCTION production_health_check()
RETURNS TABLE(
    check_name TEXT,
    status TEXT,
    details JSONB
) AS $$
BEGIN
    RETURN QUERY
    -- Check 1: Vector index exists and is healthy
    SELECT 
        'vector_index'::TEXT,
        CASE WHEN EXISTS (
            SELECT 1 FROM pg_indexes WHERE indexname = 'idx_embeddings_hnsw'
        ) THEN 'ok' ELSE 'error' END as status,
        '{}'::jsonb as details;
    
    -- Check 2: Recent embeddings exist
    SELECT 
        'recent_data'::TEXT,
        CASE 
            WHEN COUNT(*) > 0 THEN 'ok'
            ELSE 'warning'
        END as status,
        jsonb_build_object('total_vectors', COUNT(*)) as details
    FROM production_embeddings;
    
    -- Check 3: Metrics collection working
    SELECT 
        'metrics_collection'::TEXT,
        CASE 
            WHEN MAX(collected_at) > NOW() - '10 minutes'::interval THEN 'ok'
            ELSE 'warning'
        END as status,
        jsonb_build_object('last_collection', MAX(collected_at)) as details
    FROM production_metrics;
    
    -- Check 4: No blocking queries
    SELECT 
        'no_blocking'::TEXT,
        CASE 
            WHEN COUNT(*) = 0 THEN 'ok'
            ELSE 'warning'
        END as status,
        jsonb_build_object('blocking_count', COUNT(*)) as details
    FROM pg_locks
    WHERE granted = false;
    
    -- Check 5: Sufficient disk space
    SELECT 
        'disk_space'::TEXT,
        CASE 
            WHEN available > 10 * 1024 * 1024 * 1024 THEN 'ok'
            WHEN available > 1 * 1024 * 1024 * 1024 THEN 'warning'
            ELSE 'error'
        END as status,
        jsonb_build_object('available_bytes', available) as details
    FROM pg tablespace_size('pg_default');
END;
$$ LANGUAGE plpgsql;

-- Auto-recovery trigger
CREATE OR REPLACE FUNCTION auto_recovery()
RETURNS VOID AS $$
BEGIN
    -- Warm up indexes if they haven been cold
    PERFORM warmup_vector_indexes();
    
    -- Cancel long-running queries
    SELECT pg_cancel_backend(pid)
    FROM pg_stat_activity
    WHERE state = 'active'
      AND now() - state_change > interval '5 minutes'
      AND query LIKE '%<=>%';
    
    -- Vacuum if needed
    IF (SELECT COUNT(*) FROM pg_stat_user_tables 
        WHERE relname = 'production_embeddings' 
          AND n_dead_tup > 10000) > 0 THEN
        VACUUM ANALYZE production_embeddings;
    END IF;
END;
$$ LANGUAGE plpgsql;
```

### Example 3: Performance Regression Testing

```sql
-- Baseline performance test
CREATE TABLE performance_baseline (
    id SERIAL PRIMARY KEY,
    test_name VARCHAR(100),
    test_timestamp TIMESTAMPTZ DEFAULT NOW(),
    metric_name VARCHAR(100),
    metric_value FLOAT,
    is_baseline BOOLEAN DEFAULT FALSE
);

-- Record baseline
CREATE OR REPLACE FUNCTION record_baseline(
    p_test_name VARCHAR
) RETURNS VOID AS $$
BEGIN
    -- Run benchmark và record
    INSERT INTO performance_baseline (test_name, metric_name, metric_value, is_baseline)
    SELECT 
        p_test_name,
        'qps',
        1000.0,  -- Placeholder
        true
    FROM generate_series(1, 1);
END;
$$ LANGUAGE plpgsql;

-- Compare against baseline
CREATE OR REPLACE FUNCTION check_performance_regression(
    p_threshold_percent FLOAT DEFAULT 10.0
) RETURNS TABLE(
    metric_name TEXT,
    baseline_value FLOAT,
    current_value FLOAT,
    regression_percent FLOAT,
    is_regression BOOLEAN
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        pb.metric_name,
        pb.metric_value as baseline_value,
        COALESCE((
            SELECT metric_value 
            FROM performance_baseline 
            WHERE test_name = 'current' 
              AND metric_name = pb.metric_name
        ), pb.metric_value) as current_value,
        ((COALESCE((
            SELECT metric_value 
            FROM performance_baseline 
            WHERE test_name = 'current' 
              AND metric_name = pb.metric_name
        ), pb.metric_value) - pb.metric_value) / NULLIF(pb.metric_value, 0) * 100) as regression,
        ((COALESCE((
            SELECT metric_value 
            FROM performance_baseline 
            WHERE test_name = 'current' 
              AND metric_name = pb.metric_name
        ), pb.metric_value) - pb.metric_value) / NULLIF(pb.metric_value, 0) * 100) < -p_threshold_percent as is_regression
    FROM performance_baseline pb
    WHERE pb.is_baseline = true
      AND pb.test_name = 'initial';
END;
$$ LANGUAGE plpgsql;
```

## References

1. **pgvector Production**: https://github.com/pgvector/pgvector#production
2. **PgBouncer**: https://www.pgbouncer.org/
3. **PostgreSQL Monitoring**: https://www.postgresql.org/docs/current/monitoring.html
4. **PgCron**: https://docs.vaultdb.com/pg_cron/
5. **Cursor Enterprise Framework - Deployment Rules**: `.cursor/rules/deployment.mdc`
