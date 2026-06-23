---
title: "RAG with pgvector"
description: "Hướng dẫn triển khai RAG (Retrieval Augmented Generation) với pgvector, embedding pipeline, query processing và answer synthesis"
tags: ["rag", "pgvector", "retrieval", "llm", "embedding", "chunking"]
created: "2026-06-23"
version: "1.0.0"
framework: "Cursor Enterprise Framework"
---

# RAG with pgvector

## Tổng Quan

Retrieval Augmented Generation (RAG) là pattern kết hợp khả năng tìm kiếm thông tin từ vector database với sức mạnh của Large Language Models (LLMs) để tạo ra câu trả lời chính xác và có context. pgvector cung cấp native vector search capabilities trong PostgreSQL, cho phép xây dựng RAG systems với kiến trúc đơn giản nhưng hiệu quả cao.

RAG giải quyết nhiều limitations của LLMs như: knowledge cutoff, hallucination, và lack of up-to-date information. Thay vì rely hoàn toàn vào internal knowledge, RAG cho phép LLM access relevant documents từ external knowledge base trong thời gian thực.

pgvector đặc biệt phù hợp cho RAG vì:
- Tích hợp trực tiếp với PostgreSQL, không cần separate vector database
- Hỗ trợ ACID transactions và complex SQL queries
- Dễ dàng combine vector search với structured data filtering
- Mature backup và replication support

## Mục Đích

Tài liệu này nhằm cung cấp comprehensive guide để implement RAG với pgvector:

Đầu tiên, chúng ta sẽ tìm hiểu các chunking strategies để prepare documents cho RAG indexing, bao gồm fixed-size, semantic, và recursive splitting.

Thứ hai, tài liệu hướng dẫn cách build complete embedding pipeline từ document ingestion đến storage.

Thứ ba, chúng ta sẽ đề cập đến query processing flow và các techniques để improve retrieval quality.

Cuối cùng, tài liệu cung cấp patterns cho answer synthesis và complete RAG system implementation.

## Key Concepts

### 1. RAG Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         RAG System                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────┐  │
│  │   Document   │───▶│   Chunker    │───▶│  Embedding      │  │
│  │   Ingestion  │    │              │    │  Model          │  │
│  └──────────────┘    └──────────────┘    └────────┬─────────┘  │
│                                                   │             │
│                                                   ▼             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────┐  │
│  │    LLM       │◀───│   Synthesize │    │    pgvector     │  │
│  │   Response   │    │              │◀───│    Retrieval    │  │
│  └──────────────┘    └──────────────┘    └────────┬─────────┘  │
│                                                    │             │
│  ┌──────────────┐    ┌──────────────┐             │             │
│  │  User Query  │───▶│  Embedding   │─────────────┘             │
│  └──────────────┘    │  Query       │                          │
│                      └──────────────┘                          │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Document Processing Pipeline

```sql
-- Table cho storing documents
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    source_url TEXT,
    source_type VARCHAR(50),  -- 'pdf', 'web', 'api', 'file'
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    status VARCHAR(20) DEFAULT 'pending'  -- pending, processing, indexed, error
);

-- Table cho document chunks
CREATE TABLE document_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    chunk_text TEXT NOT NULL,
    chunk_hash VARCHAR(64) NOT NULL,  -- For deduplication
    embedding VECTOR(1536),  -- NULL until indexed
    token_count INTEGER,
    start_char INTEGER,  -- Position in original document
    end_char INTEGER,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    UNIQUE (document_id, chunk_index)
);

-- Index for vector search
CREATE INDEX idx_chunks_embedding ON document_chunks 
    USING hnsw (embedding vector_cosine_ops) 
    WITH (m = 16, ef_construction = 200);

-- Index for metadata filtering
CREATE INDEX idx_chunks_document ON document_chunks (document_id);
CREATE INDEX idx_chunks_hash ON document_chunks (chunk_hash);
```

### 3. Chunking Strategies

#### Fixed-size Chunking

```sql
-- Fixed-size chunking với configurable size và overlap
CREATE OR REPLACE FUNCTION chunk_document_fixed_size(
    p_document_id UUID,
    p_text TEXT,
    p_chunk_size INTEGER DEFAULT 500,  -- characters
    p_overlap INTEGER DEFAULT 50      -- overlap characters
) RETURNS INTEGER AS $$
DECLARE
    v_text_length INTEGER;
    v_start_pos INTEGER := 1;
    v_chunk_index INTEGER := 0;
    v_chunk_text TEXT;
    v_chunk_hash VARCHAR(64);
BEGIN
    v_text_length := length(p_text);
    
    WHILE v_start_pos <= v_text_length LOOP
        -- Extract chunk
        v_chunk_text := substring(
            p_text, 
            v_start_pos, 
            LEAST(p_chunk_size, v_text_length - v_start_pos + 1)
        );
        
        -- Calculate hash for deduplication
        v_chunk_hash := encode(sha256(v_chunk_text::bytea), 'hex');
        
        -- Insert chunk
        INSERT INTO document_chunks (
            id, document_id, chunk_index, chunk_text, chunk_hash,
            start_char, end_char, token_count
        )
        VALUES (
            gen_random_uuid(),
            p_document_id,
            v_chunk_index,
            v_chunk_text,
            v_chunk_hash,
            v_start_pos - 1,
            v_start_pos + length(v_chunk_text) - 1,
            length(v_chunk_text) / 4  -- Rough token estimate
        )
        ON CONFLICT (document_id, chunk_index) DO UPDATE SET
            chunk_text = EXCLUDED.chunk_text,
            chunk_hash = EXCLUDED.chunk_hash;
        
        v_start_pos := v_start_pos + p_chunk_size - p_overlap;
        v_chunk_index := v_chunk_index + 1;
    END LOOP;
    
    RETURN v_chunk_index;
END;
$$ LANGUAGE plpgsql;
```

#### Semantic Chunking

```sql
-- Semantic chunking dựa trên sentence boundaries
CREATE OR REPLACE FUNCTION chunk_document_semantic(
    p_document_id UUID,
    p_text TEXT,
    p_max_sentences INTEGER DEFAULT 5,
    p_min_sentences INTEGER DEFAULT 2
) RETURNS INTEGER AS $$
DECLARE
    v_sentences TEXT[] := '{}';
    v_chunks TEXT[] := '{}';
    v_current_chunk TEXT := '';
    v_sentence_count INTEGER := 0;
    v_chunk_index INTEGER := 0;
    v_chunk_hash VARCHAR(64);
BEGIN
    -- Split into sentences (basic regex - use more sophisticated NLP in production)
    v_sentences := regexp_matches(p_text, '[^\.!?]+[\.!?]+', 'g');
    
    -- Group sentences into chunks
    FOR i IN 1..array_length(v_sentences, 1) LOOP
        v_current_chunk := v_current_chunk || ' ' || v_sentences[i];
        v_sentence_count := v_sentence_count + 1;
        
        -- Create chunk when reaching max sentences
        IF v_sentence_count >= p_max_sentences THEN
            v_chunks := array_append(v_chunks, trim(v_current_chunk));
            v_current_chunk := '';
            v_sentence_count := 0;
        END IF;
    END LOOP;
    
    -- Add remaining sentences as final chunk (if enough sentences)
    IF v_sentence_count >= p_min_sentences THEN
        v_chunks := array_append(v_chunks, trim(v_current_chunk));
    ELSIF array_length(v_chunks, 1) > 0 AND v_sentence_count > 0 THEN
        -- Merge with previous chunk
        v_chunks[array_length(v_chunks, 1)] := 
            v_chunks[array_length(v_chunks, 1)] || ' ' || trim(v_current_chunk);
    END IF;
    
    -- Insert chunks
    FOREACH v_current_chunk IN ARRAY v_chunks LOOP
        v_chunk_hash := encode(sha256(v_current_chunk::bytea), 'hex');
        
        INSERT INTO document_chunks (
            id, document_id, chunk_index, chunk_text, chunk_hash, token_count
        )
        VALUES (
            gen_random_uuid(),
            p_document_id,
            v_chunk_index,
            v_current_chunk,
            v_chunk_hash,
            length(v_current_chunk) / 4
        )
        ON CONFLICT (document_id, chunk_index) DO UPDATE SET
            chunk_text = EXCLUDED.chunk_text,
            chunk_hash = EXCLUDED.chunk_hash;
        
        v_chunk_index := v_chunk_index + 1;
    END LOOP;
    
    RETURN v_chunk_index;
END;
$$ LANGUAGE plpgsql;
```

## Embedding Pipeline

### 1. Embedding Generation

```sql
-- Table cho embedding jobs queue
CREATE TABLE embedding_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chunk_id UUID NOT NULL REFERENCES document_chunks(id),
    status VARCHAR(20) DEFAULT 'pending',  -- pending, processing, completed, failed
    attempts INTEGER DEFAULT 0,
    error_message TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ
);

-- Index for job processing
CREATE INDEX idx_embedding_jobs_status ON embedding_jobs (status) WHERE status = 'pending';

-- Queue embedding job
CREATE OR REPLACE FUNCTION queue_embedding_job(
    p_chunk_id UUID
) RETURNS VOID AS $$
BEGIN
    INSERT INTO embedding_jobs (chunk_id)
    VALUES (p_chunk_id)
    ON CONFLICT DO NOTHING;
END;
$$ LANGUAGE plpgsql;

-- Process embedding jobs (to be called by background worker)
CREATE OR REPLACE FUNCTION process_embedding_jobs(
    p_batch_size INTEGER DEFAULT 100,
    p_embedding_model VARCHAR DEFAULT 'text-embedding-3-small'
) RETURNS INTEGER AS $$
DECLARE
    v_job_record RECORD;
    v_embedding VECTOR(1536);
    v_job_ids UUID[] := '{}';
BEGIN
    -- Get pending jobs
    FOR v_job_record IN (
        SELECT id, chunk_id 
        FROM embedding_jobs 
        WHERE status = 'pending' 
        ORDER BY created_at 
        LIMIT p_batch_size
    )
    LOOP
        v_job_ids := array_append(v_job_ids, v_job_record.id);
    END LOOP;
    
    -- Mark as processing
    UPDATE embedding_jobs
    SET status = 'processing', started_at = NOW(), attempts = attempts + 1
    WHERE id = ANY(v_job_ids);
    
    -- Process each job (placeholder - integrate with actual embedding API)
    FOR v_job_record IN (
        SELECT id, chunk_id 
        FROM embedding_jobs 
        WHERE status = 'processing'
    )
    LOOP
        BEGIN
            -- Get chunk text
            SELECT chunk_text INTO v_job_record
            FROM document_chunks
            WHERE id = v_job_record.chunk_id;
            
            -- Generate embedding (mock - replace with actual API call)
            -- v_embedding := generate_embedding(v_job_record.chunk_text, p_embedding_model);
            v_embedding := array_to_vector(array(
                SELECT random()::real FROM generate_series(1, 1536)
            ))::vector;
            
            -- Update chunk with embedding
            UPDATE document_chunks
            SET embedding = v_embedding
            WHERE id = v_job_record.chunk_id;
            
            -- Mark job as completed
            UPDATE embedding_jobs
            SET status = 'completed', completed_at = NOW()
            WHERE id = v_job_record.id;
            
        EXCEPTION WHEN OTHERS THEN
            UPDATE embedding_jobs
            SET status = 'failed', error_message = SQLERRM
            WHERE id = v_job_record.id;
        END;
    END LOOP;
    
    RETURN array_length(v_job_ids, 1);
END;
$$ LANGUAGE plpgsql;
```

### 2. Batch Embedding for Efficiency

```sql
-- Batch processing để improve throughput
CREATE OR REPLACE FUNCTION batch_embed_documents(
    p_document_ids UUID[],
    p_batch_size INTEGER DEFAULT 100
) RETURNS TABLE(
    document_id UUID,
    chunks_processed INTEGER,
    embeddings_generated INTEGER,
    failed_chunks INTEGER
) AS $$
DECLARE
    v_document_id UUID;
    v_chunks_processed INTEGER := 0;
    v_embeddings INTEGER := 0;
    v_failures INTEGER := 0;
BEGIN
    FOREACH v_document_id IN ARRAY p_document_ids LOOP
        -- Queue all chunks for document
        INSERT INTO embedding_jobs (chunk_id)
        SELECT id FROM document_chunks
        WHERE document_id = v_document_id
          AND embedding IS NULL;
        
        -- Process batch
        v_chunks_processed := process_embedding_jobs(p_batch_size);
        
        -- Count results
        SELECT COUNT(*) INTO v_embeddings
        FROM document_chunks
        WHERE document_id = v_document_id
          AND embedding IS NOT NULL;
        
        SELECT COUNT(*) INTO v_failures
        FROM embedding_jobs ej
        JOIN document_chunks dc ON ej.chunk_id = dc.id
        WHERE dc.document_id = v_document_id
          AND ej.status = 'failed';
        
        RETURN QUERY SELECT v_document_id, v_chunks_processed, v_embeddings, v_failures;
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```

## Query Processing

### 1. Query Embedding

```sql
-- Store user queries for analysis
CREATE TABLE query_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    query_text TEXT NOT NULL,
    query_embedding VECTOR(1536),
    filters JSONB DEFAULT '{}',
    results_count INTEGER,
    latency_ms FLOAT,
    user_id UUID,
    session_id UUID,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Log query với embedding
CREATE OR REPLACE FUNCTION log_query(
    p_query_text TEXT,
    p_filters JSONB DEFAULT '{}',
    p_results_count INTEGER,
    p_latency_ms FLOAT,
    p_user_id UUID DEFAULT NULL
) RETURNS UUID AS $$
DECLARE
    v_query_embedding VECTOR(1536);
    v_log_id UUID;
BEGIN
    -- Generate query embedding (mock - replace with actual API)
    v_query_embedding := array_to_vector(array(
        SELECT random()::real FROM generate_series(1, 1536)
    ))::vector;
    
    INSERT INTO query_logs (
        id, query_text, query_embedding, filters, 
        results_count, latency_ms, user_id
    )
    VALUES (
        gen_random_uuid(),
        p_query_text,
        v_query_embedding,
        p_filters,
        p_results_count,
        p_latency_ms,
        p_user_id
    )
    RETURNING id INTO v_log_id;
    
    RETURN v_log_id;
END;
$$ LANGUAGE plpgsql;
```

### 2. Retrieval with Filtering

```sql
-- Advanced retrieval function với multiple filters
CREATE OR REPLACE FUNCTION retrieve_chunks(
    p_query_embedding REAL[],
    p_filters JSONB DEFAULT '{}',
    p_limit INTEGER DEFAULT 10,
    p_min_similarity FLOAT DEFAULT 0.5,
    p_include_vector_rank BOOLEAN DEFAULT TRUE
) RETURNS TABLE(
    chunk_id UUID,
    document_id UUID,
    chunk_text TEXT,
    document_title TEXT,
    similarity FLOAT,
    vector_rank BIGINT,
    metadata JSONB
) AS $$
DECLARE
    v_source_types TEXT[] := COALESCE((p_filters->>'source_types')::text[], '{pdf,web,api}');
    v_date_from TIMESTAMPTZ := (p_filters->>'date_from')::timestamptz;
    v_date_to TIMESTAMPTZ := (p_filters->>'date_to')::timestamptz;
BEGIN
    RETURN QUERY
    WITH filtered_chunks AS (
        SELECT 
            dc.id as chunk_id,
            dc.document_id,
            dc.chunk_text,
            dc.metadata,
            1 - (dc.embedding <=> p_query_embedding::vector) as similarity,
            ROW_NUMBER() OVER (ORDER BY dc.embedding <=> p_query_embedding::vector) as rn
        FROM document_chunks dc
        JOIN documents d ON dc.document_id = d.id
        WHERE 
            -- Similarity threshold
            1 - (dc.embedding <=> p_query_embedding::vector) >= p_min_similarity
            -- Source type filter
            AND (v_source_types IS NULL OR v_source_types = '{}'::text[]
                 OR d.source_type = ANY(v_source_types))
            -- Date range filter
            AND (v_date_from IS NULL OR d.created_at >= v_date_from)
            AND (v_date_to IS NULL OR d.created_at <= v_date_to)
            -- Document status filter
            AND d.status = 'indexed'
    )
    SELECT 
        fc.chunk_id,
        fc.document_id,
        fc.chunk_text,
        d.title as document_title,
        fc.similarity,
        fc.rn as vector_rank,
        fc.metadata
    FROM filtered_chunks fc
    JOIN documents d ON fc.document_id = d.id
    ORDER BY fc.rn
    LIMIT p_limit;
END;
$$ LANGUAGE plpgsql;
```

### 3. RAG Prompt Construction

```sql
-- Construct prompt cho LLM
CREATE OR REPLACE FUNCTION construct_rag_prompt(
    p_query TEXT,
    p_retrieved_chunks TEXT[],
    p_system_prompt TEXT DEFAULT NULL,
    p_max_context_tokens INTEGER DEFAULT 4000
) RETURNS TEXT AS $$
DECLARE
    v_system TEXT := COALESCE(p_system_prompt,
        'You are a helpful AI assistant. Use the provided context to answer the user question. ' ||
        'If the context does not contain relevant information, say so.');
    v_context TEXT := '';
    v_chunk TEXT;
    v_token_count INTEGER := 0;
BEGIN
    -- Build context from retrieved chunks
    FOREACH v_chunk IN ARRAY p_retrieved_chunks LOOP
        -- Rough token estimation
        IF v_token_count + length(v_chunk) / 4 > p_max_context_tokens THEN
            EXIT;
        END IF;
        
        v_context := v_context || E'\n\n---\n\n' || v_chunk;
        v_token_count := v_token_count + length(v_chunk) / 4;
    END LOOP;
    
    RETURN format(
        'System: %s
        
Context:
%s

User Question: %s
        
Answer:',
        v_system,
        v_context,
        p_query
    );
END;
$$ LANGUAGE plpgsql;
```

## Complete RAG Implementation

### 1. Main RAG Function

```sql
-- Complete RAG function
CREATE OR REPLACE FUNCTION rag_query(
    p_query TEXT,
    p_filters JSONB DEFAULT '{}',
    p_limit INTEGER DEFAULT 5,
    p_min_similarity FLOAT DEFAULT 0.6,
    p_max_context_chunks INTEGER DEFAULT 5,
    p_llm_model VARCHAR DEFAULT 'gpt-4'
) RETURNS TABLE(
    answer TEXT,
    sources JSONB,
    retrieved_chunks JSONB,
    metadata JSONB
) AS $$
DECLARE
    v_query_embedding REAL[];
    v_retrieved_chunks RECORD;
    v_chunk_texts TEXT[] := '{}';
    v_sources JSONB := '[]'::jsonb;
    v_context_size INTEGER := 0;
    v_llm_response TEXT;
    v_start_time TIMESTAMPTZ := clock_timestamp();
    v_latency_ms FLOAT;
BEGIN
    -- Step 1: Generate query embedding
    v_query_embedding := ARRAY(
        SELECT random()::real FROM generate_series(1, 1536)
    );  -- Placeholder - integrate with actual embedding API
    
    -- Step 2: Retrieve relevant chunks
    FOR v_retrieved_chunks IN (
        SELECT 
            chunk_id,
            chunk_text,
            document_title,
            similarity,
            metadata
        FROM retrieve_chunks(
            v_query_embedding,
            p_filters,
            p_limit * 2,  -- Retrieve more for filtering
            p_min_similarity
        )
        ORDER BY similarity DESC
        LIMIT p_limit
    )
    LOOP
        -- Check if chunk fits in context
        IF v_context_size + length(v_retrieved_chunks.chunk_text) > 4000 * 4 THEN
            EXIT;
        END IF;
        
        v_chunk_texts := array_append(v_chunk_texts, v_retrieved_chunks.chunk_text);
        v_sources := v_sources || jsonb_build_array(
            jsonb_build_object(
                'chunk_id', v_retrieved_chunks.chunk_id,
                'title', v_retrieved_chunks.document_title,
                'similarity', v_retrieved_chunks.similarity,
                'metadata', v_retrieved_chunks.metadata
            )
        );
        v_context_size := v_context_size + length(v_retrieved_chunks.chunk_text);
    END LOOP;
    
    -- Step 3: Construct prompt
    -- (In production, this would call actual LLM API)
    v_llm_response := format(
        'Based on the context provided, here is the answer to your question about "%s"...',
        p_query
    );
    
    -- Step 4: Calculate latency
    v_latency_ms := EXTRACT(MILLISECONDS FROM (clock_timestamp() - v_start_time));
    
    -- Return results
    RETURN QUERY
    SELECT 
        v_llm_response as answer,
        v_sources as sources,
        array_to_jsonb(v_chunk_texts) as retrieved_chunks,
        jsonb_build_object(
            'query', p_query,
            'model', p_llm_model,
            'chunks_retrieved', array_length(v_chunk_texts, 1),
            'latency_ms', v_latency_ms
        ) as metadata;
END;
$$ LANGUAGE plpgsql;
```

### 2. Query Analysis and Optimization

```sql
-- Analyze query patterns
CREATE OR REPLACE FUNCTION analyze_query_patterns(
    p_days INTEGER DEFAULT 7
) RETURNS TABLE(
    metric_name TEXT,
    metric_value FLOAT,
    details JSONB
) AS $$
BEGIN
    RETURN QUERY
    -- Most common queries
    SELECT 
        'top_queries'::TEXT,
        COUNT(*)::float,
        (SELECT jsonb_agg(jsonb_build_object(
            'query', query_text,
            'count', cnt
        ))
        FROM (
            SELECT query_text, COUNT(*) as cnt
            FROM query_logs
            WHERE created_at > NOW() - (p_days || ' days')::interval
            GROUP BY query_text
            ORDER BY cnt DESC
            LIMIT 10
        ) t)::jsonb as details
    FROM query_logs
    WHERE created_at > NOW() - (p_days || ' days')::interval;
    
    -- Average results count
    SELECT 
        'avg_results'::TEXT,
        AVG(results_count)::float,
        NULL::jsonb
    FROM query_logs
    WHERE created_at > NOW() - (p_days || ' days')::interval;
    
    -- Average latency
    SELECT 
        'avg_latency_ms'::TEXT,
        AVG(latency_ms)::float,
        jsonb_build_object(
            'p50', PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY latency_ms),
            'p95', PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY latency_ms),
            'p99', PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY latency_ms)
        ) as details
    FROM query_logs
    WHERE created_at > NOW() - (p_days || ' days')::interval;
    
    -- Low-similarity queries (potential index issues)
    SELECT 
        'low_similarity_queries'::TEXT,
        COUNT(*)::float,
        (SELECT jsonb_agg(jsonb_build_object(
            'query', query_text,
            'max_similarity', max_similarity
        ))
        FROM (
            SELECT query_text, MAX(results_count) as max_similarity
            FROM query_logs
            WHERE created_at > NOW() - (p_days || ' days')::interval
            GROUP BY query_text
            HAVING MAX(results_count) < 3
            ORDER BY MAX(results_count)
            LIMIT 20
        ) t)::jsonb as details
    FROM query_logs
    WHERE created_at > NOW() - (p_days || ' days')::interval;
END;
$$ LANGUAGE plpgsql;
```

## Best Practices

### 1. Chunking Best Practices

```sql
-- Dynamic chunk sizing based on content type
CREATE OR REPLACE FUNCTION chunk_by_content_type(
    p_document_id UUID,
    p_text TEXT,
    p_content_type VARCHAR(50)
) RETURNS INTEGER AS $$
DECLARE
    v_chunk_size INTEGER;
    v_overlap INTEGER;
BEGIN
    -- Adjust chunk parameters based on content type
    CASE p_content_type
        WHEN 'code' THEN
            v_chunk_size := 1000;  -- Larger chunks for code
            v_overlap := 100;
        WHEN 'technical' THEN
            v_chunk_size := 600;
            v_overlap := 100;
        WHEN 'conversational' THEN
            v_chunk_size := 300;
            v_overlap := 50;
        ELSE
            v_chunk_size := 500;
            v_overlap := 50;
    END CASE;
    
    RETURN chunk_document_fixed_size(p_document_id, p_text, v_chunk_size, v_overlap);
END;
$$ LANGUAGE plpgsql;
```

### 2. Index Optimization

```sql
-- Optimize HNSW index for RAG workloads
CREATE INDEX idx_chunks_hnsw_optimized ON document_chunks 
    USING hnsw (embedding vector_cosine_ops) 
    WITH (
        m = 16, 
        ef_construction = 200,
        maintenance_work_mem = '4GB'
    );

-- Partial index cho active documents
CREATE INDEX idx_chunks_active ON document_chunks 
    USING hnsw (embedding vector_cosine_ops) 
    WHERE status = 'indexed';
```

### 3. Monitoring RAG Health

```sql
-- RAG system health check
CREATE OR REPLACE FUNCTION rag_health_check()
RETURNS TABLE(
    check_name TEXT,
    status TEXT,
    details JSONB
) AS $$
BEGIN
    RETURN QUERY
    -- Check pending embedding jobs
    SELECT 
        'pending_embeddings'::TEXT,
        CASE 
            WHEN COUNT(*) > 1000 THEN 'warning'
            ELSE 'ok'
        END as status,
        jsonb_build_object('count', COUNT(*)) as details
    FROM embedding_jobs
    WHERE status = 'pending';
    
    -- Check failed jobs
    SELECT 
        'failed_embeddings'::TEXT,
        CASE 
            WHEN COUNT(*) > 100 THEN 'error'
            WHEN COUNT(*) > 10 THEN 'warning'
            ELSE 'ok'
        END as status,
        jsonb_build_object('count', COUNT(*)) as details
    FROM embedding_jobs
    WHERE status = 'failed';
    
    -- Check index health
    SELECT 
        'index_health'::TEXT,
        'ok' as status,
        jsonb_build_object(
            'size_mb', pg_relation_size('idx_chunks_embedding') / 1024 / 1024
        ) as details
    FROM pg_indexes
    WHERE indexname = 'idx_chunks_embedding';
    
    -- Check recent query performance
    SELECT 
        'query_performance'::TEXT,
        CASE 
            WHEN AVG(latency_ms) > 500 THEN 'warning'
            ELSE 'ok'
        END as status,
        jsonb_build_object(
            'avg_latency_ms', AVG(latency_ms),
            'queries_last_hour', COUNT(*)
        ) as details
    FROM query_logs
    WHERE created_at > NOW() - '1 hour'::interval;
END;
$$ LANGUAGE plpgsql;
```

## Examples

### Example 1: Complete Document Ingestion Flow

```sql
-- Complete document ingestion với error handling
CREATE OR REPLACE FUNCTION ingest_document(
    p_title TEXT,
    p_content TEXT,
    p_source_url TEXT DEFAULT NULL,
    p_source_type VARCHAR DEFAULT 'web',
    p_metadata JSONB DEFAULT '{}'
) RETURNS UUID AS $$
DECLARE
    v_document_id UUID;
    v_chunks_created INTEGER;
BEGIN
    -- Create document record
    INSERT INTO documents (title, content, source_url, source_type, metadata, status)
    VALUES (p_title, p_content, p_source_url, p_source_type, p_metadata, 'processing')
    RETURNING id INTO v_document_id;
    
    -- Chunk the document
    BEGIN
        v_chunks_created := chunk_document_semantic(
            v_document_id,
            p_content,
            5,  -- max sentences per chunk
            2   -- min sentences per chunk
        );
        
        -- Queue embedding jobs
        INSERT INTO embedding_jobs (chunk_id)
        SELECT id FROM document_chunks
        WHERE document_id = v_document_id
          AND embedding IS NULL;
        
        -- Update status
        UPDATE documents
        SET status = 'indexed', updated_at = NOW()
        WHERE id = v_document_id;
        
    EXCEPTION WHEN OTHERS THEN
        UPDATE documents
        SET status = 'error', updated_at = NOW()
        WHERE id = v_document_id;
        RAISE;
    END;
    
    RETURN v_document_id;
END;
$$ LANGUAGE plpgsql;

-- Batch ingestion
CREATE OR REPLACE FUNCTION batch_ingest_documents(
    p_documents JSONB  -- Array of {title, content, source_url, source_type}
) RETURNS TABLE(
    document_id UUID,
    status TEXT,
    chunks_created INTEGER
) AS $$
DECLARE
    v_doc JSONB;
BEGIN
    FOR v_doc IN SELECT * FROM jsonb_array_elements(p_documents)
    LOOP
        BEGIN
            INSERT INTO documents (title, content, source_url, source_type, metadata, status)
            VALUES (
                v_doc->>'title',
                v_doc->>'content',
                v_doc->>'source_url',
                COALESCE(v_doc->>'source_type', 'web'),
                COALESCE(v_doc->'metadata', '{}'),
                'processing'
            )
            RETURNING id INTO v_doc;
            
            -- Chunking would happen asynchronously in production
            -- This is synchronous for demonstration
            UPDATE documents SET status = 'indexed' WHERE id = v_doc;
            
            RETURN QUERY SELECT v_doc, 'success'::TEXT, 5::INTEGER;
            
        EXCEPTION WHEN OTHERS THEN
            RETURN QUERY SELECT v_doc, 'failed: ' || SQLERRM::TEXT, 0::INTEGER;
        END;
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```

### Example 2: Conversational RAG

```sql
-- Store conversation history
CREATE TABLE rag_conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    message_count INTEGER DEFAULT 0
);

CREATE TABLE rag_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES rag_conversations(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL,  -- 'user', 'assistant', 'system'
    content TEXT NOT NULL,
    context_chunks JSONB,  -- Retrieved chunks used
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Conversational RAG
CREATE OR REPLACE FUNCTION conversational_rag(
    p_conversation_id UUID,
    p_query TEXT,
    p_filters JSONB DEFAULT '{}',
    p_max_history INTEGER DEFAULT 10
) RETURNS TABLE(
    answer TEXT,
    sources JSONB,
    conversation_id UUID
) AS $$
DECLARE
    v_conversation_id UUID;
    v_history TEXT[] := '{}';
    v_message RECORD;
    v_context_chunks TEXT[] := '{}';
    v_prompt TEXT;
    v_sources JSONB := '[]'::jsonb;
BEGIN
    -- Create conversation if not exists
    IF p_conversation_id IS NULL THEN
        INSERT INTO rag_conversations (user_id)
        VALUES (NULL)
        RETURNING id INTO v_conversation_id;
    ELSE
        v_conversation_id := p_conversation_id;
    END IF;
    
    -- Get conversation history
    FOR v_message IN (
        SELECT role, content 
        FROM rag_messages
        WHERE conversation_id = v_conversation_id
        ORDER BY created_at DESC
        LIMIT p_max_history
    )
    LOOP
        v_history := array_append(v_history, 
            v_message.role || ': ' || v_message.content);
    END LOOP;
    
    -- Add retrieved context (simplified)
    v_context_chunks := ARRAY[
        'Context from document: ...',
        'Another relevant passage: ...'
    ];
    
    v_sources := jsonb_build_array(
        jsonb_build_object('title', 'Sample Doc', 'similarity', 0.85)
    );
    
    -- Construct prompt
    v_prompt := 'Previous conversation:\n' || 
                array_to_string(ARRAY_REVERSE(v_history), '\n') ||
                '\n\nContext:\n' ||
                array_to_string(v_context_chunks, '\n\n') ||
                '\n\nUser: ' || p_query;
    
    -- Store user message
    INSERT INTO rag_messages (conversation_id, role, content, context_chunks)
    VALUES (v_conversation_id, 'user', p_query, v_sources);
    
    -- Generate response (mock - integrate with LLM)
    RETURN QUERY
    SELECT 
        'Generated response based on context...' as answer,
        v_sources as sources,
        v_conversation_id as conversation_id;
    
    -- Store assistant response
    INSERT INTO rag_messages (conversation_id, role, content)
    VALUES (v_conversation_id, 'assistant', 'Generated response based on context...');
    
    -- Update conversation
    UPDATE rag_conversations
    SET message_count = message_count + 2, updated_at = NOW()
    WHERE id = v_conversation_id;
END;
$$ LANGUAGE plpgsql;
```

## References

1. **pgvector RAG**: https://github.com/pgvector/pgvector#rag
2. **RAG Architecture**: https://arxiv.org/abs/2005.11401
3. **Chunking Strategies**: https://python.langchain.com/docs/modules/data_connection/document_transformers/
4. **Cursor Enterprise Framework - RAG Rules**: `.cursor/rules/rag.mdc`
5. **Embedding Models**: OpenAI, Cohere, HuggingFace documentation
