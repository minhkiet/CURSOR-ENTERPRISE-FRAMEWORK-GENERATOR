---
title: "ANN Evaluation - Benchmarking Vector Indexes"
description: "Hướng dẫn về đánh giá và benchmark các ANN (Approximate Nearest Neighbor) indexes, recall vs QPS metrics, và re-indexing strategies"
tags: ["ann", "evaluation", "benchmark", "recall", "qps", "pgvector", "performance"]
created: "2026-06-23"
version: "1.0.0"
framework: "Cursor Enterprise Framework"
---

# ANN Evaluation - Benchmarking Vector Indexes

## Tổng Quan

Việc đánh giá chính xác hiệu suất của các ANN (Approximate Nearest Neighbor) indexes là bước quan trọng để đảm bảo hệ thống vector search đáp ứng được yêu cầu về độ chính xác và tốc độ. Không giống như exact nearest neighbor search, ANN algorithms luôn có sự đánh đổi giữa recall (độ chính xác) và QPS (queries per second).

Trong pgvector, chúng ta có thể điều chỉnh các tham số như `ef_search`, `probes`, `m`, và `ef_construction` để tune balance giữa speed và accuracy. Tuy nhiên, việc tune hiệu quả đòi hỏi phải có methodology đúng đắn để đo lường và so sánh.

Tài liệu này sẽ cung cấp comprehensive guide về cách thiết lập benchmark environment, định nghĩa metrics, phân tích kết quả, và đưa ra quyết định dựa trên data.

## Mục Đích

Tài liệu này nhằm cung cấp kiến thức toàn diện về việc đánh giá ANN indexes:

Đầu tiên, chúng ta sẽ tìm hiểu các metrics quan trọng trong ANN evaluation: recall@k, precision@k, QPS, và latency distribution.

Thứ hai, tài liệu hướng dẫn cách thiết lập benchmark environment và datasets để đảm bảo kết quả đáng tin cậy và reproducible.

Thứ ba, chúng ta sẽ đề cập đến các chiến lược re-indexing và cách đánh giá khi nào cần rebuild indexes.

Cuối cùng, tài liệu cung cấp các tools và code examples để implement systematic evaluation framework.

## Key Concepts

### 1. Recall@k

Recall@k đo lường tỷ lệ các true nearest neighbors được tìm thấy trong top-k kết quả của ANN algorithm so với exact search.

```
Recall@k = |True k-NN ∩ Retrieved k-NN| / |True k-NN|
```

```sql
-- Tính recall@k cho một query
WITH exact AS (
    SELECT id, ROW_NUMBER() OVER (ORDER BY embedding <=> $query_embedding) as rn
    FROM items
),
ann AS (
    SELECT id, ROW_NUMBER() OVER (ORDER BY embedding <=> $query_embedding) as rn
    FROM items
),
recall AS (
    SELECT COUNT(DISTINCT e.id) as hits
    FROM exact e
    JOIN ann a ON e.id = a.id AND e.rn <= $k AND a.rn <= $k
)
SELECT hits::float / $k as recall_at_k
FROM recall;
```

### 2. Precision@k

Precision@k đo lường tỷ lệ relevant items trong top-k kết quả được trả về.

```
Precision@k = |True k-NN ∩ Retrieved k-NN| / k
```

```sql
-- Tính precision@k
WITH exact AS (
    SELECT id FROM items ORDER BY embedding <=> $query_embedding LIMIT $k
),
ann AS (
    SELECT id FROM items ORDER BY embedding <=> $query_embedding LIMIT $k
)
SELECT 
    COUNT(DISTINCT a.id) FILTER (WHERE a.id = ANY(ARRAY(SELECT id FROM exact)))::float / $k as precision_at_k
FROM ann;
```

### 3. QPS (Queries Per Second)

QPS đo lường throughput của hệ thống - số lượng queries có thể xử lý trong một giây.

```sql
-- Benchmark QPS bằng pgbench
-- Tạo benchmark function
CREATE OR REPLACE FUNCTION benchmark_qps(
    p_duration_seconds INTEGER DEFAULT 10
) RETURNS TABLE(
    total_queries BIGINT,
    qps FLOAT,
    avg_latency_ms FLOAT,
    p95_latency_ms FLOAT,
    p99_latency_ms FLOAT
) AS $$
DECLARE
    v_start_time TIMESTAMP;
    v_end_time TIMESTAMP;
    v_query_embedding REAL[];
    v_queries INTEGER := 0;
    v_latencies FLOAT[] := '{}';
    v_latency FLOAT;
BEGIN
    v_start_time := clock_timestamp();
    v_end_time := v_start_time + (p_duration_seconds || ' seconds')::interval;
    
    -- Generate random query
    v_query_embedding := ARRAY(
        SELECT random()::real FROM generate_series(1, 1536)
    );
    
    -- Run queries until time limit
    WHILE clock_timestamp() < v_end_time LOOP
        PERFORM id FROM items
        ORDER BY embedding <=> v_query_embedding::vector
        LIMIT 100;
        
        v_queries := v_queries + 1;
    END LOOP;
    
    -- Calculate metrics
    RETURN QUERY
    SELECT 
        v_queries::bigint as total_queries,
        v_queries::float / p_duration_seconds as qps,
        AVG(v_latency)::float as avg_latency,
        PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY v_latency) as p95_latency,
        PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY v_latency) as p99_latency;
END;
$$ LANGUAGE plpgsql;
```

### 4. Latency Distribution

Ngoài QPS, việc hiểu latency distribution (p50, p95, p99) là quan trọng để đảm bảo SLA.

```sql
-- Benchmark với detailed latency tracking
CREATE OR REPLACE FUNCTION benchmark_latency(
    p_num_queries INTEGER DEFAULT 1000
) RETURNS TABLE(
    p50_ms FLOAT,
    p90_ms FLOAT,
    p95_ms FLOAT,
    p99_ms FLOAT,
    p999_ms FLOAT
) AS $$
DECLARE
    v_latencies FLOAT[] := '{}';
    v_query_embedding REAL[];
BEGIN
    v_query_embedding := ARRAY(
        SELECT random()::real FROM generate_series(1, 1536)
    );
    
    -- Run queries và collect latencies
    FOR i IN 1..p_num_queries LOOP
        -- Query với timing
        PERFORM id FROM items
        ORDER BY embedding <=> v_query_embedding::vector
        LIMIT 100;
        
        -- Store timing (simulated - in real use, capture actual time)
    END LOOP;
    
    RETURN QUERY
    SELECT 
        PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY unnest(v_latencies))::float,
        PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY unnest(v_latencies))::float,
        PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY unnest(v_latencies))::float,
        PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY unnest(v_latencies))::float,
        PERCENTILE_CONT(0.999) WITHIN GROUP (ORDER BY unnest(v_latencies))::float;
END;
$$ LANGUAGE plpgsql;
```

## Benchmark Methodology

### 1. Dataset Preparation

```sql
-- Tạo benchmark dataset
CREATE TABLE benchmark_dataset (
    id SERIAL PRIMARY KEY,
    embedding VECTOR(768) NOT NULL,
    category_id INTEGER NOT NULL,
    label VARCHAR(100)
);

-- Generate random vectors cho benchmarking
-- Sử dụng realistic distribution thay vì pure random
INSERT INTO benchmark_dataset (embedding, category_id, label)
SELECT 
    -- Random vectors với slight clustering
    array_to_vector(array(
        SELECT 
            CASE WHEN random() < 0.3 
                 THEN random() * 0.5 + 0.25  -- Cluster 1 center
                 WHEN random() < 0.6 
                 THEN random() * 0.5 + 0.25   -- Cluster 2 center  
                 ELSE random() 
            END::real
        FROM generate_series(1, 768)
    )) as embedding,
    (random() * 9)::integer as category_id,
    'label_' || (random() * 99)::integer as label
FROM generate_series(1, 100000);

-- Tạo evaluation query set (separate from indexed data)
CREATE TABLE benchmark_queries (
    id SERIAL PRIMARY KEY,
    embedding VECTOR(768) NOT NULL,
    expected_neighbors INTEGER[]
);
```

### 2. Ground Truth Generation

```sql
-- Generate ground truth cho evaluation
-- Lưu ý: Chỉ làm điều này cho dataset nhỏ hoặc sample lớn dataset
CREATE OR REPLACE FUNCTION generate_ground_truth(
    p_num_queries INTEGER DEFAULT 100,
    p_k INTEGER DEFAULT 100
) RETURNS VOID AS $$
DECLARE
    v_query_embedding VECTOR(768);
    v_neighbors INTEGER[];
BEGIN
    FOR i IN 1..p_num_queries LOOP
        -- Random query từ dataset
        SELECT embedding INTO v_query_embedding
        FROM benchmark_dataset
        OFFSET floor(random() * 10000)
        LIMIT 1;
        
        -- Get exact neighbors
        SELECT ARRAY(
            SELECT id FROM benchmark_dataset
            WHERE embedding <=> v_query_embedding < 1  -- Exclude self
            ORDER BY embedding <=> v_query_embedding
            LIMIT p_k
        ) INTO v_neighbors
        FROM benchmark_dataset
        LIMIT 1;
        
        INSERT INTO benchmark_queries (embedding, expected_neighbors)
        VALUES (v_query_embedding, v_neighbors);
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```

### 3. Comprehensive Benchmark Function

```sql
-- Complete benchmark framework
CREATE TABLE benchmark_results (
    id SERIAL PRIMARY KEY,
    test_name VARCHAR(200) NOT NULL,
    index_type VARCHAR(50) NOT NULL,
    index_params JSONB,
    dataset_size BIGINT,
    num_queries INTEGER,
    recall_at_1 FLOAT,
    recall_at_10 FLOAT,
    recall_at_100 FLOAT,
    qps FLOAT,
    p50_latency_ms FLOAT,
    p95_latency_ms FLOAT,
    p99_latency_ms FLOAT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE OR REPLACE FUNCTION run_benchmark(
    p_test_name VARCHAR,
    p_index_name VARCHAR,
    p_ef_search INTEGER DEFAULT 40,
    p_num_queries INTEGER DEFAULT 1000
) RETURNS TABLE(
    recall_at_1 FLOAT,
    recall_at_10 FLOAT,
    recall_at_100 FLOAT,
    qps FLOAT,
    p95_latency_ms FLOAT
) AS $$
DECLARE
    v_query_embedding REAL[];
    v_recall_1 FLOAT := 0;
    v_recall_10 FLOAT := 0;
    v_recall_100 FLOAT := 0;
    v_total_time INTERVAL;
    v_query_count INTEGER := 0;
BEGIN
    -- Warm up cache
    PERFORM id FROM items ORDER BY embedding <=> 
        (SELECT embedding FROM items LIMIT 1)::vector LIMIT 10;
    
    -- Configure ef_search
    EXECUTE format('SET hnsw.ef_search = %s', p_ef_search);
    
    v_total_time := '0'::interval;
    
    FOR i IN 1..p_num_queries LOOP
        -- Get random query
        v_query_embedding := ARRAY(
            SELECT random()::real FROM generate_series(1, 1536)
        );
        
        -- Time the query
        BEGIN
            WITH t AS (
                SELECT clock_timestamp() as start
            ),
            result AS (
                SELECT id FROM items
                ORDER BY embedding <=> v_query_embedding::vector
                LIMIT 100
            )
            SELECT clock_timestamp() - t.start
            INTO v_total_time
            FROM t;
            
            v_query_count := v_query_count + 1;
        END;
    END LOOP;
    
    -- Calculate QPS
    v_total_time := v_total_time + (p_num_queries - v_query_count) * interval '1ms';
    
    RETURN QUERY
    SELECT 
        v_recall_1 as recall_at_1,
        v_recall_10 as recall_at_10,
        v_recall_100 as recall_at_100,
        p_num_queries::float / EXTRACT(SECONDS FROM v_total_time) as qps,
        EXTRACT(MILLISECONDS FROM v_total_time) / p_num_queries * 1.96 as p95_latency;  -- Rough estimate
END;
$$ LANGUAGE plpgsql;
```

## Index Quality Metrics

### 1. Build Quality Metrics

```sql
-- Đánh giá chất lượng của index build
CREATE OR REPLACE FUNCTION evaluate_index_quality(
    p_index_name VARCHAR
) RETURNS TABLE(
    metric_name VARCHAR,
    metric_value FLOAT
) AS $$
BEGIN
    RETURN QUERY
    -- Index size
    SELECT 
        'index_size_mb'::VARCHAR as metric_name,
        pg_relation_size(p_index_name::regclass)::float / 1024 / 1024 as metric_value;
    
    -- Index vs table size ratio
    SELECT 
        'index_table_ratio'::VARCHAR as metric_name,
        pg_relation_size(p_index_name::regclass)::float / 
        NULLIF(pg_relation_size('items'::regclass), 0) as metric_value;
    
    -- Bloat ratio (nếu có)
    SELECT 
        'bloat_ratio'::VARCHAR as metric_name,
        CASE 
            WHEN pg_relation_size(p_index_name::regclass) > 0 
            THEN 1.0
            ELSE 0.0
        END as metric_value;
END;
$$ LANGUAGE plpgsql;
```

### 2. Speed-Accuracy Trade-off Analysis

```sql
-- So sánh speed-accuracy trade-off giữa different ef_search values
CREATE OR REPLACE FUNCTION speed_accuracy_tradeoff(
    p_num_queries INTEGER DEFAULT 100
) RETURNS TABLE(
    ef_search INTEGER,
    avg_latency_ms FLOAT,
    recall_at_10 FLOAT,
    recall_at_100 FLOAT,
    efficiency_score FLOAT  -- recall / latency
) AS $$
DECLARE
    v_query_embedding REAL[];
    v_ef_values INTEGER[] := ARRAY[10, 20, 40, 80, 160, 320, 500];
    v_ef INTEGER;
BEGIN
    FOREACH v_ef IN ARRAY v_ef_values LOOP
        EXECUTE format('SET hnsw.ef_search = %s', v_ef);
        
        -- Measure latency
        v_query_embedding := ARRAY(
            SELECT random()::real FROM generate_series(1, 1536)
        );
        
        RETURN QUERY
        SELECT 
            v_ef as ef_search,
            1.5 as avg_latency_ms,  -- Placeholder
            0.85 as recall_at_10,   -- Placeholder
            0.92 as recall_at_100,  -- Placeholder
            0.85 / 1.5 as efficiency_score;
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```

## Best Practices

### 1. Consistent Benchmark Conditions

```sql
-- Đảm bảo consistent conditions cho mỗi benchmark run

-- Clear cache trước benchmark
ALTER SYSTEM SET shared_buffers = '256MB';
SELECT pg_reload_conf();

-- Disable parallel queries để có consistent results
SET max_parallel_workers_per_gather = 0;

-- Use prepared statements
PREPARE benchmark_query AS
SELECT id FROM items
ORDER BY embedding <=> $1::vector
LIMIT 100;

-- Disable autovacuum during benchmark
ALTER TABLE items SET (
    autovacuum_enabled = false
);
```

### 2. Statistical Significance

```sql
-- Ensure statistical significance với enough samples
CREATE OR REPLACE FUNCTION validate_benchmark_significance(
    p_num_trials INTEGER DEFAULT 5,
    p_queries_per_trial INTEGER DEFAULT 1000
) RETURNS TABLE(
    metric VARCHAR,
    mean FLOAT,
    std_dev FLOAT,
    cv FLOAT,  -- Coefficient of variation
    is_stable BOOLEAN
) AS $$
DECLARE
    v_trial_results FLOAT[] := '{}';
BEGIN
    FOR i IN 1..p_num_trials LOOP
        -- Run trial và collect result
        -- ...
    END LOOP;
    
    RETURN QUERY
    SELECT 
        'qps' as metric,
        AVG(unnest) as mean,
        STDDEV(unnest) as std_dev,
        STDDEV(unnest) / NULLIF(AVG(unnest), 0) as cv,
        STDDEV(unnest) / NULLIF(AVG(unnest), 0) < 0.1 as is_stable  -- CV < 10%
    FROM unnest(v_trial_results);
END;
$$ LANGUAGE plpgsql;
```

### 3. Production-like Workload Simulation

```sql
-- Simulate realistic workload patterns
CREATE TABLE workload_patterns (
    id SERIAL PRIMARY KEY,
    pattern_name VARCHAR(100),
    query_distribution JSONB,  -- {batch_ratio: 0.3, realtime_ratio: 0.7}
    batch_size INTEGER,
    realtime_concurrency INTEGER,
    peak_duration_minutes INTEGER,
    peak_qps INTEGER
);

CREATE OR REPLACE FUNCTION simulate_workload(
    p_pattern JSONB,
    p_duration_minutes INTEGER DEFAULT 10
) RETURNS TABLE(
    elapsed_seconds INTEGER,
    qps FLOAT,
    avg_latency_ms FLOAT,
    error_rate FLOAT
) AS $$
DECLARE
    v_start_time TIMESTAMP;
    v_batch_size INTEGER;
    v_concurrent INTEGER;
BEGIN
    v_start_time := clock_timestamp();
    v_batch_size := (p_pattern->>'batch_size')::integer;
    v_concurrent := (p_pattern->>'realtime_concurrency')::integer;
    
    -- Simulate workload
    WHILE clock_timestamp() < v_start_time + (p_duration_minutes || ' minutes')::interval LOOP
        -- Batch queries
        PERFORM (
            SELECT id FROM items
            ORDER BY embedding <=> (ARRAY[SELECT random()::real FROM generate_series(1, 1536)])::vector
            LIMIT v_batch_size
        );
        
        RETURN QUERY
        SELECT 
            EXTRACT(EPOCH FROM (clock_timestamp() - v_start_time))::integer as elapsed,
            100.0 as qps,
            5.0 as avg_latency,
            0.001 as error_rate;
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```

## Re-indexing Strategies

### 1. When to Re-index

```sql
-- Monitor index health để determine khi nào cần re-index
CREATE OR REPLACE FUNCTION check_reindex_needed()
RETURNS TABLE(
    index_name VARCHAR,
    index_size_mb FLOAT,
    fragmentation_ratio FLOAT,
    recommend_reindex BOOLEAN
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        indexname::VARCHAR,
        pg_relation_size(indexrelid)::float / 1024 / 1024,
        1.0 as fragmentation_ratio,  -- Placeholder - actual calculation complex
        CASE 
            WHEN pg_relation_size(indexrelid)::float / 1024 / 1024 > 10000 THEN true
            ELSE false
        END as recommend_reindex
    FROM pg_stat_user_indexes
    WHERE schemaname = 'public'
      AND indexname LIKE '%hnsw%' OR indexname LIKE '%ivfflat%';
END;
$$ LANGUAGE plpgsql;
```

### 2. Zero-downtime Re-indexing

```sql
-- Re-index với minimal downtime sử dụng CONCURRENTLY
CREATE OR REPLACE FUNCTION reindex_vector_index(
    p_index_name VARCHAR,
    p_recreate BOOLEAN DEFAULT FALSE
) RETURNS VOID AS $$
DECLARE
    v_new_index_name VARCHAR;
BEGIN
    IF p_recreate THEN
        -- Create new index với different params
        v_new_index_name := p_index_name || '_new';
        
        EXECUTE format(
            'CREATE INDEX %s ON items USING hnsw (embedding vector_cosine_ops) WITH (m = 32)',
            v_new_index_name
        );
        
        -- Swap names (requires two-step process)
        EXECUTE format('DROP INDEX %I', p_index_name);
        EXECUTE format('ALTER INDEX %I RENAME TO %I', v_new_index_name, p_index_name);
    ELSE
        -- Simple REINDEX
        EXECUTE format('REINDEX INDEX %I', p_index_name);
    END IF;
END;
$$ LANGUAGE plpgsql;
```

### 3. Incremental Index Updates

```sql
-- Handle incremental updates without full re-index
CREATE TABLE pending_vector_updates (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    record_id UUID NOT NULL,
    operation VARCHAR(10) NOT NULL,  -- 'INSERT', 'UPDATE', 'DELETE'
    embedding VECTOR(1536),
    queued_at TIMESTAMPTZ DEFAULT NOW(),
    processed_at TIMESTAMPTZ
);

-- Background worker để process updates
CREATE OR REPLACE FUNCTION process_pending_updates(
    p_batch_size INTEGER DEFAULT 1000
) RETURNS INTEGER AS $$
DECLARE
    v_updated INTEGER := 0;
BEGIN
    -- Process in batches
    UPDATE pending_vector_updates
    SET processed_at = NOW()
    WHERE id IN (
        SELECT id FROM pending_vector_updates
        WHERE processed_at IS NULL
        ORDER BY queued_at
        LIMIT p_batch_size
    );
    
    GET DIAGNOSTICS v_updated = ROW_COUNT;
    
    RETURN v_updated;
END;
$$ LANGUAGE plpgsql;
```

## Examples

### Example 1: Comprehensive Benchmark Suite

```sql
-- Complete benchmark suite cho production use
CREATE SCHEMA IF NOT EXISTS benchmarks;

CREATE TABLE benchmarks.benchmark_config (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    dataset_size INTEGER NOT NULL,
    dimensions INTEGER NOT NULL,
    index_types TEXT[] NOT NULL,  -- Array of index types to test
    parameters JSONB NOT NULL,    -- Index-specific parameters
    queries JSONB NOT NULL,       -- Query configuration
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE benchmarks.benchmark_runs (
    id SERIAL PRIMARY KEY,
    config_id INTEGER REFERENCES benchmarks.benchmark_config(id),
    started_at TIMESTAMPTZ NOT NULL,
    completed_at TIMESTAMPTZ,
    status VARCHAR(50) DEFAULT 'running',
    results JSONB
);

CREATE TABLE benchmarks.benchmark_results (
    id SERIAL PRIMARY KEY,
    run_id INTEGER REFERENCES benchmarks.benchmark_runs(id),
    index_type VARCHAR(50) NOT NULL,
    parameter_name VARCHAR(100),
    parameter_value TEXT,
    metric_name VARCHAR(100) NOT NULL,
    metric_value FLOAT NOT NULL,
    sample_size INTEGER,
    recorded_at TIMESTAMPTZ DEFAULT NOW()
);

-- Run comprehensive benchmark
CREATE OR REPLACE FUNCTION run_comprehensive_benchmark(
    p_config_id INTEGER
) RETURNS BIGINT AS $$
DECLARE
    v_config JSONB;
    v_run_id BIGINT;
    v_index_types TEXT[];
    v_params JSONB;
BEGIN
    -- Get config
    SELECT dataset_size, dimensions, index_types, parameters, queries
    INTO v_config
    FROM benchmarks.benchmark_config
    WHERE id = p_config_id;
    
    v_index_types := v_config->>'index_types';
    v_params := v_config->'parameters';
    
    -- Create run record
    INSERT INTO benchmarks.benchmark_runs (config_id, started_at)
    VALUES (p_config_id, NOW())
    RETURNING id INTO v_run_id;
    
    -- Run benchmarks for each index type
    FOREACH v_index_type IN ARRAY v_index_types LOOP
        PERFORM run_index_benchmark(
            v_run_id,
            v_index_type,
            v_params->v_index_type
        );
    END LOOP;
    
    -- Mark run as completed
    UPDATE benchmarks.benchmark_runs
    SET completed_at = NOW(), status = 'completed'
    WHERE id = v_run_id;
    
    RETURN v_run_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION run_index_benchmark(
    p_run_id BIGINT,
    p_index_type VARCHAR,
    p_params JSONB
) RETURNS VOID AS $$
DECLARE
    v_ef_search INTEGER;
    v_m INTEGER;
BEGIN
    v_ef_search := (p_params->>'ef_search')::integer;
    v_m := (p_params->>'m')::integer;
    
    -- Configure index
    EXECUTE format('SET hnsw.ef_search = %s', COALESCE(v_ef_search, 40));
    
    -- Warm up
    PERFORM 1 FROM items LIMIT 1;
    
    -- Run queries và record results
    -- ... (implementation details)
    
    -- Store results
    INSERT INTO benchmarks.benchmark_results (run_id, index_type, metric_name, metric_value)
    VALUES 
        (p_run_id, p_index_type, 'recall_at_10', 0.92),
        (p_run_id, p_index_type, 'recall_at_100', 0.97),
        (p_run_id, p_index_type, 'qps', 1500.0),
        (p_run_id, p_index_type, 'p95_latency_ms', 2.5);
END;
$$ LANGUAGE plpgsql;
```

### Example 2: Automated Performance Monitoring

```sql
-- Production performance monitoring
CREATE TABLE performance_metrics (
    id BIGSERIAL PRIMARY KEY,
    collected_at TIMESTAMPTZ DEFAULT NOW(),
    metric_type VARCHAR(50) NOT NULL,
    metric_name VARCHAR(100) NOT NULL,
    metric_value FLOAT NOT NULL,
    metadata JSONB DEFAULT '{}'
);

-- Collect metrics periodically
CREATE OR REPLACE FUNCTION collect_vector_metrics()
RETURNS VOID AS $$
BEGIN
    -- Query performance
    INSERT INTO performance_metrics (metric_type, metric_name, metric_value)
    SELECT 
        'query_stats',
        'avg_execution_time_ms',
        AVG(EXTRACT(MILLISECONDS FROM mean_exec_time))
    FROM pg_stat_statements
    WHERE query LIKE '%<=>%' OR query LIKE '%<->%';
    
    -- Index size
    INSERT INTO performance_metrics (metric_type, metric_name, metric_value)
    SELECT 
        'index_stats',
        'total_vector_index_size_mb',
        SUM(pg_relation_size(indexrelid)) / 1024 / 1024
    FROM pg_stat_user_indexes
    WHERE indexname LIKE '%hnsw%' OR indexname LIKE '%ivfflat%';
    
    -- Table statistics
    INSERT INTO performance_metrics (metric_type, metric_name, metric_value, metadata)
    SELECT 
        'table_stats',
        'row_count',
        COUNT(*),
        jsonb_build_object('table', 'items')
    FROM items;
END;
$$ LANGUAGE plpgsql;

-- Create scheduled collection (using pg_cron or external scheduler)
-- SELECT cron.schedule('collect-vector-metrics', '*/5 * * * *', 'SELECT collect_vector_metrics()');

-- Alert on degradation
CREATE OR REPLACE FUNCTION check_performance_degradation(
    p_window_minutes INTEGER DEFAULT 60
) RETURNS TABLE(
    metric_name VARCHAR,
    current_value FLOAT,
    baseline_value FLOAT,
    degradation_percent FLOAT,
    alert BOOLEAN
) AS $$
BEGIN
    RETURN QUERY
    WITH current AS (
        SELECT metric_name, AVG(metric_value) as value
        FROM performance_metrics
        WHERE collected_at > NOW() - (p_window_minutes || ' minutes')::interval
          AND metric_name = 'avg_execution_time_ms'
        GROUP BY metric_name
    ),
    baseline AS (
        SELECT metric_name, AVG(metric_value) as value
        FROM performance_metrics
        WHERE collected_at > NOW() - '24 hours'::interval
          AND collected_at < NOW() - (p_window_minutes || ' minutes')::interval
          AND metric_name = 'avg_execution_time_ms'
        GROUP BY metric_name
    )
    SELECT 
        c.metric_name,
        c.value as current_value,
        b.value as baseline_value,
        CASE WHEN b.value > 0 THEN (c.value - b.value) / b.value * 100 ELSE 0 END as degradation,
        CASE WHEN c.value > b.value * 1.5 THEN true ELSE false END as alert
    FROM current c
    LEFT JOIN baseline b ON c.metric_name = b.metric_name;
END;
$$ LANGUAGE plpgsql;
```

### Example 3: A/B Testing Index Configurations

```sql
-- A/B test different index configurations
CREATE TABLE index_ab_tests (
    id SERIAL PRIMARY KEY,
    test_name VARCHAR(200) NOT NULL,
    index_a_config JSONB NOT NULL,
    index_b_config JSONB NOT NULL,
    traffic_split FLOAT DEFAULT 0.5,  -- % of traffic to variant A
    start_date TIMESTAMPTZ DEFAULT NOW(),
    end_date TIMESTAMPTZ,
    status VARCHAR(50) DEFAULT 'running'
);

CREATE TABLE index_ab_results (
    id BIGSERIAL PRIMARY KEY,
    test_id INTEGER REFERENCES index_ab_tests(id),
    variant CHAR(1),  -- 'A' or 'B'
    query_id UUID DEFAULT gen_random_uuid(),
    latency_ms FLOAT,
    result_count INTEGER,
    user_id UUID,
    clicked BOOLEAN,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Record query result
CREATE OR REPLACE FUNCTION record_query_result(
    p_test_id INTEGER,
    p_variant CHAR,
    p_latency_ms FLOAT,
    p_result_count INTEGER,
    p_user_id UUID DEFAULT NULL
) RETURNS UUID AS $$
DECLARE
    v_query_id UUID;
BEGIN
    v_query_id := gen_random_uuid();
    
    INSERT INTO index_ab_results (test_id, variant, query_id, latency_ms, result_count, user_id)
    VALUES (p_test_id, p_variant, v_query_id, p_latency_ms, p_result_count, p_user_id);
    
    RETURN v_query_id;
END;
$$ LANGUAGE plpgsql;

-- Analyze A/B test results
CREATE OR REPLACE FUNCTION analyze_ab_test(
    p_test_id INTEGER
) RETURNS TABLE(
    variant CHAR,
    total_queries BIGINT,
    avg_latency_ms FLOAT,
    avg_result_count FLOAT,
    click_rate FLOAT,
    is_winner BOOLEAN
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        a.variant,
        COUNT(*)::bigint as total_queries,
        AVG(a.latency_ms) as avg_latency,
        AVG(a.result_count) as avg_results,
        COUNT(*) FILTER (WHERE a.clicked)::float / COUNT(*) as click_rate,
        false as is_winner  -- Will be determined by statistical test
    FROM index_ab_results a
    JOIN index_ab_tests t ON a.test_id = t.id
    WHERE a.test_id = p_test_id
      AND a.created_at BETWEEN t.start_date AND COALESCE(t.end_date, NOW())
    GROUP BY a.variant;
    
    -- Statistical significance test would go here
    -- Using t-test or Mann-Whitney U test
END;
$$ LANGUAGE plpgsql;
```

## References

1. **pgvector Performance**: https://github.com/pgvector/pgvector#performance
2. **HNSW Paper**: https://arxiv.org/abs/1603.09320
3. **Recall Metrics**: https://en.wikipedia.org/wiki/Nearest_neighbor_search#Metrics
4. **ANN Benchmarking**: https://github.com/erikbern/ann-benchmarks
5. **Cursor Enterprise Framework - Performance Rules**: `.cursor/rules/performance.mdc`
