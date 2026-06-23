# PostgreSQL Architecture - Kiến Trúc Chi Tiết

## Mục lục
1. [Tổng quan Kiến trúc](#1-tổng-quan-kiến-trúc)
2. [Process Architecture](#2-process-architecture)
3. [Memory Architecture](#3-memory-architecture)
4. [Storage Architecture](#4-storage-architecture)
5. [Query Processing](#5-query-processing)

---

## 1. Tổng quan Kiến trúc

### 1.1 PostgreSQL Overview

PostgreSQL là một advanced, enterprise-class object-relational database system. Nó cung cấp ACID compliance, MVCC, extensible architecture, và support cho complex data types.

Core features:
- **MVCC**: Multi-Version Concurrency Control
- **ACID**: Atomicity, Consistency, Isolation, Durability
- **Extensibility**: Custom types, functions, operators
- **Advanced Indexing**: B-tree, Hash, GiST, SP-GiST, GIN, BRIN
- **Full-Text Search**: Native text search
- **JSON Support**: JSON và JSONB data types
- **Partitioning**: Table partitioning
- **Replication**: Streaming, Logical, Synchronous

### 1.2 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                     POSTGRESQL ARCHITECTURE                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                   CLIENT APPLICATIONS                           │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │   │
│  │  │   CLI   │  │  JDBC  │  │   Npgsql │  │  libpq  │       │   │
│  │  │ psql   │  │        │  │         │  │         │       │   │
│  │  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘       │   │
│  └────────┼──────────┼──────────┼──────────┼──────────────┘   │
│           │          │          │          │                     │
│           └──────────┴──────────┴──────────┘                     │
│                              │                                       │
│                              ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                      POSTMASTER                               │   │
│  │  ┌─────────────────────────────────────────────────────┐  │   │
│  │  │                  Connection Listener                   │  │   │
│  │  │              (Port 5432 - default)                   │  │   │
│  │  └─────────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│                              ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                   PROCESS PER CONNECTION                      │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │   │
│  │  │postgres │  │postgres │  │postgres │  │postgres │       │   │
│  │  │proc 1  │  │proc 2  │  │proc 3  │  │proc N  │       │   │
│  │  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘       │   │
│  └────────┼──────────┼──────────┼──────────┼──────────────┘   │
│           │          │          │          │                     │
│           └──────────┴──────────┴──────────┘                     │
│                              │                                       │
│                              ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                     SHARED MEMORY                             │   │
│  │                                                             │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │   │
│  │  │   Buffer   │  │   WAL Buffer │  │  Lock       │       │   │
│  │  │   Pool    │  │              │  │  Manager    │       │   │
│  │  │ (shared_  │  │              │  │             │       │   │
│  │  │  buffers) │  │              │  │             │       │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘       │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│                              ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    LOCAL MEMORY                             │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │   │
│  │  │ Sort Buffer │  │   Temp     │  │  Work Mem   │       │   │
│  │  │             │  │   Tables   │  │             │       │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘       │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│                              ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                     POSTGRESQL PROCESSES                      │   │
│  │                                                             │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │   │
│  │  │ Writer  │  │ WAL     │  │ Archiver│  │ Stats   │       │   │
│  │  │ Process │  │ Writer  │  │         │  │ Collector│      │   │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘       │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│                              ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                        FILE SYSTEM                           │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │   │
│  │  │   Data   │  │    WAL   │  │  System  │  │  Tables  │   │   │
│  │  │  Files  │  │   Files  │  │ Catalogs │  │  Spaces  │   │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 2. Process Architecture

### 2.1 Process Types

```
┌─────────────────────────────────────────────────────────────────────┐
│                      POSTGRESQL PROCESSES                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    POSTMASTER (Main Process)                     │   │
│  │  - Listens for connections (port 5432)                         │   │
│  │  - Forks new processes for each connection                    │   │
│  │  - Manages shared memory and locks                            │   │
│  │  - Handles startup/shutdown                                  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│                              │ Forks                                │
│                              ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              POSTGRESQL (Backend Process)                      │   │
│  │  - One per connection                                      │   │
│  │  - Executes queries                                       │   │
│  │  - Parses, analyzes, optimizes queries                     │   │
│  │  - Own local memory (work_mem, temp_buffers)                │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│                              │                                       │
│          ┌───────────────────┼───────────────────┐                │
│          │                   │                   │                  │
│          ▼                   ▼                   ▼                   │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐          │
│  │    Writer     │  │   WAL Writer  │  │   Autovacuum  │          │
│  │   Process    │  │   Process     │  │   Launcher   │          │
│  │              │  │              │  │              │          │
│  │ - Writes to  │  │ - Writes WAL │  │ - Monitors   │          │
│  │   data files │  │   to disk   │  │   tables    │          │
│  │ - Checkpoint │  │ - Checkpoint │  │ - Vacuum    │          │
│  │   activity  │  │   writes    │  │   workers   │          │
│  └───────────────┘  └───────────────┘  └───────────────┘          │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### 2.2 Query Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                         QUERY FLOW                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Client SQL Query                                                   │
│       │                                                             │
│       ▼                                                             │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    PARSING LAYER                             │   │
│  │  - Lexer/Tokenize                                            │   │
│  │  - Parser (generates parse tree)                             │   │
│  │  - Rewrite rules application                                 │   │
│  └─────────────────────────────────────────────────────────────┘   │
│       │                                                             │
│       ▼                                                             │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                  ANALYZER/TRASFORMER                       │   │
│  │  - Semantic analysis                                         │   │
│  │  - Type checking and coercion                               │   │
│  │  - Bind parameters                                         │   │
│  │  - Generate query tree                                      │   │
│  └─────────────────────────────────────────────────────────────┘   │
│       │                                                             │
│       ▼                                                             │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                     PLANNER/OPTIMIZER                       │   │
│  │  - Generate multiple execution plans                        │   │
│  │  - Cost estimation for each plan                          │   │
│  │  - Select cheapest plan (cost-based)                      │   │
│  │  - Statistics from pg_statistic                           │   │
│  └─────────────────────────────────────────────────────────────┘   │
│       │                                                             │
│       ▼                                                             │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                      EXECUTOR                              │   │
│  │  - Execute plan nodes sequentially                        │   │
│  │  - Access methods (sequential scan, index scan)          │   │
│  │  - Join methods (nested loop, hash join, merge join)     │   │
│  │  - Aggregate and sort operations                          │   │
│  │  - Return results to client                               │   │
│  └─────────────────────────────────────────────────────────────┘   │
│       │                                                             │
│       ▼                                                             │
│  Results to Client                                                  │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 3. Memory Architecture

### 3.1 Memory Components

```
┌─────────────────────────────────────────────────────────────────────┐
│                      POSTGRESQL MEMORY                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    SHARED MEMORY                               │   │
│  │  (Allocated at startup, shared by all backends)              │   │
│  │                                                             │   │
│  │  ┌─────────────────────────────────────────────────────┐  │   │
│  │  │                Shared Buffers                         │  │   │
│  │  │  - Default: 128MB                                   │  │   │
│  │  │  - 8KB pages (same as OS block size)               │  │   │
│  │  │  - Cache for table/index pages                       │  │   │
│  │  │  - Configuration: shared_buffers                    │  │   │
│  │  └─────────────────────────────────────────────────────┘  │   │
│  │                                                             │   │
│  │  ┌─────────────────────────────────────────────────────┐  │   │
│  │  │               WAL Buffers                            │  │   │
│  │  │  - Default: 16MB                                    │  │   │
│  │  │  - Write-Ahead Logging buffer                       │  │   │
│  │  │  - Configuration: wal_buffers                      │  │   │
│  │  └─────────────────────────────────────────────────────┘  │   │
│  │                                                             │   │
│  │  ┌─────────────────────────────────────────────────────┐  │   │
│  │  │              Lock Manager                            │  │   │
│  │  │  - Row-level locks                                  │  │   │
│  │  │  - Page-level locks                                │  │   │
│  │  │  - Relation locks                                  │  │   │
│  │  └─────────────────────────────────────────────────────┘  │   │
│  │                                                             │   │
│  │  ┌─────────────────────────────────────────────────────┐  │   │
│  │  │              Free Space Map                         │  │   │
│  │  │  - Tracks free space in tables                     │  │   │
│  │  │  - Used by VACUUM                                  │  │   │
│  │  └─────────────────────────────────────────────────────┘  │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│                              ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                   LOCAL MEMORY (per backend)                │   │
│  │  (Allocated per connection)                                  │   │
│  │                                                             │   │
│  │  ┌─────────────────────────────────────────────────────┐  │   │
│  │  │               work_mem                                │  │   │
│  │  │  - Default: 4MB                                       │  │   │
│  │  │  - Memory for sorting, hash operations               │  │   │
│  │  │  - Can increase for complex queries                   │  │   │
│  │  └─────────────────────────────────────────────────────┘  │   │
│  │                                                             │   │
│  │  ┌─────────────────────────────────────────────────────┐  │   │
│  │  │             maintenance_work_mem                    │  │   │
│  │  │  - Default: 64MB                                    │  │   │
│  │  │  - For VACUUM, CREATE INDEX, ALTER TABLE           │  │   │
│  │  └─────────────────────────────────────────────────────┘  │   │
│  │                                                             │   │
│  │  ┌─────────────────────────────────────────────────────┐  │   │
│  │  │              temp_buffers                           │  │   │
│  │  │  - Default: 8MB                                    │  │   │
│  │  │  - Temporary tables                                 │  │   │
│  │  └─────────────────────────────────────────────────────┘  │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 4. Storage Architecture

### 4.1 Heap File Structure

```
┌─────────────────────────────────────────────────────────────────────┐
│                      HEAP FILE STRUCTURE                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                  HEAP FILE (per table)                       │   │
│  │                                                             │   │
│  │  ┌─────────────────────────────────────────────────────┐  │   │
│  │  │                  Page 0 (Header)                     │  │   │
│  │  │  ┌───────────────────────────────────────────────┐ │  │   │
│  │  │  │ PageHeaderData (24 bytes)                    │ │  │   │
│  │  │  │ - pd_lsn: Last WAL record pointer            │ │  │   │
│  │  │  │ - pd_checksum: Page checksum                │ │  │   │
│  │  │  │ - pd_lower: Free space start               │ │  │   │
│  │  │  │ - pd_upper: Free space end                 │ │  │   │
│  │  │  │ - pd_special: Special space start          │ │  │   │
│  │  │  └───────────────────────────────────────────────┘ │  │   │
│  │  │                       │                               │  │   │
│  │  │                       ▼                               │  │   │
│  │  │  ┌───────────────────────────────────────────────┐ │  │   │
│  │  │  │              ItemIdData Array                  │ │  │   │
│  │  │  │  ┌─────────┐ ┌─────────┐ ┌─────────┐        │ │  │   │
│  │  │  │  │ offset  │ │ length  │ │ flags   │        │ │  │   │
│  │  │  │  │ (4 bytes)│ │ (2 bytes)│ │ (2 bytes)│       │ │  │   │
│  │  │  │  └─────────┘ └─────────┘ └─────────┘        │ │  │   │
│  │  │  └───────────────────────────────────────────────┘ │  │   │
│  │  │                       │                               │  │   │
│  │  │                       ▼                               │  │   │
│  │  │  ┌───────────────────────────────────────────────┐ │  │   │
│  │  │  │                 Items (Rows)                  │ │  │   │
│  │  │  │  ┌─────────────────────────────────────┐     │ │  │   │
│  │  │  │  │           HeapTupleHeaderData         │     │ │  │   │
│  │  │  │  │  - t_xmin: Insert transaction ID   │     │ │  │   │
│  │  │  │  │  - t_xmax: Delete transaction ID   │     │ │  │   │
│  │  │  │  │  - t_cid: Command ID              │     │ │  │   │
│  │  │  │  │  - t_ctid: Current tuple ID      │     │ │  │   │
│  │  │  │  │  - t_infomask: Status bits       │     │ │  │   │
│  │  │  │  │  - t_infomask2: Status bits     │     │ │  │   │
│  │  │  │  │  - t_len: Tuple length           │     │ │  │   │
│  │  │  │  │  - t_oid: Object ID (if any)     │     │ │  │   │
│  │  │  │  └─────────────────────────────────────┘     │ │  │   │
│  │  │  │              Data Fields                       │ │  │   │
│  │  │  └───────────────────────────────────────────────┘ │  │   │
│  │  │                       │                               │  │   │
│  │  │                       ▼                               │  │   │
│  │  │  ┌───────────────────────────────────────────────┐ │  │   │
│  │  │  │              Special Space                      │ │  │   │
│  │  │  │  (Index-specific data, e.g., B-tree ptrs)   │ │  │   │
│  │  │  └───────────────────────────────────────────────┘ │  │   │
│  │  └─────────────────────────────────────────────────────┘  │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│                              ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                      Page N (8KB)                             │   │
│  │  - Same structure as Page 0                                  │   │
│  │  - Contains rows N through M                                  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### 4.2 Write-Ahead Logging

```
┌─────────────────────────────────────────────────────────────────────┐
│                    WRITE-AHEAD LOGGING (WAL)                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                        TRANSACTION                            │   │
│  │                                                             │   │
│  │  BEGIN;                                                     │   │
│  │       │                                                     │   │
│  │       ▼                                                     │   │
│  │  ┌─────────────────────────────────────────────────────┐ │   │
│  │  │                   WAL RECORD                        │ │   │
│  │  │  - Record type (INSERT/UPDATE/DELETE)              │ │   │
│  │  │  - Transaction ID                                   │ │   │
│  │  │  - Before image (for UPDATE/DELETE)                 │ │   │
│  │  │  - After image (for INSERT/UPDATE)                  │ │   │
│  │  │  - LSN (Log Sequence Number)                        │ │   │
│  │  └─────────────────────────────────────────────────────┘ │   │
│  │       │                                                     │   │
│  │       ▼                                                     │   │
│  │  ┌─────────────────────────────────────────────────────┐ │   │
│  │  │                   WAL BUFFER                        │ │   │
│  │  │  - Size: wal_buffers (default 16MB)                 │ │   │
│  │  │  - In shared memory                                 │ │   │
│  │  └─────────────────────────────────────────────────────┘ │   │
│  │       │                                                     │   │
│  │       ▼                                                     │   │
│  │  ┌─────────────────────────────────────────────────────┐ │   │
│  │  │                   WAL FILES                           │ │   │
│  │  │  - Write to disk before data page                   │ │   │
│  │  │  - File format: 0000000100000000000000001          │ │   │
│  │  │  - Archived if archive_mode = on                     │ │   │
│  │  └─────────────────────────────────────────────────────┘ │   │
│  │       │                                                     │   │
│  │       ▼                                                     │   │
│  │  ┌─────────────────────────────────────────────────────┐ │   │
│  │  │                   DATA FILES                          │ │   │
│  │  │  - Modified pages written to disk                   │ │   │
│  │  │  - Only after checkpoint                           │ │   │
│  │  └─────────────────────────────────────────────────────┘ │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│                              ▼                                       │
│                          COMMIT;                                     │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 5. Query Processing

### 5.1 Index Types

```
┌─────────────────────────────────────────────────────────────────────┐
│                    POSTGRESQL INDEX TYPES                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                         B-Tree (default)                       │   │
│  │  - Most common, default type                                │   │
│  │  - Equality and range queries                             │   │
│  │  - ASC, DESC, NULLS FIRST/LAST                           │   │
│  │  - Use cases: IDs, dates, strings                         │   │
│  │                                                             │   │
│  │  CREATE INDEX idx ON table (column);                      │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                          Hash                               │   │
│  │  - Equality queries only                                 │   │
│  │  - Cannot handle range queries                          │   │
│  │  - Use cases: Simple key lookups                        │   │
│  │                                                             │   │
│  │  CREATE INDEX idx ON table USING hash (column);          │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                        GiST                                 │   │
│  │  - Geometric data types                                   │   │
│  │  - Full-text search                                     │   │
│  │  - Range types                                         │   │
│  │  - Use cases: PostGIS, text search                      │   │
│  │                                                             │   │
│  │  CREATE INDEX idx ON table USING gist (column);           │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                         GIN                                 │   │
│  │  - Inverted index for arrays, JSONB                     │   │
│  │  - Multiple values per row                               │   │
│  │  - Use cases: Search, tags, JSONB                       │   │
│  │                                                             │   │
│  │  CREATE INDEX idx ON table USING gin (column);            │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                        BRIN                                 │   │
│  │  - Block Range Index                                    │   │
│  │  - For naturally ordered data (dates, sequences)         │   │
│  │  - Much smaller than B-tree                           │   │
│  │  - Use cases: Time-series data, logs                     │   │
│  │                                                             │   │
│  │  CREATE INDEX idx ON table USING brin (column);           │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Liên kết liên quan
- [PostgreSQL Glossary](./glossary.md)
- [PostgreSQL Best Practices](./best-practice.md)
- [PostgreSQL Anti-Patterns](./anti-pattern.md)
- [PostgreSQL Checklist](./checklist.md)
- [PostgreSQL FAQ](./faq.md)
- [PostgreSQL Decision Tree](./decision-tree.md)
