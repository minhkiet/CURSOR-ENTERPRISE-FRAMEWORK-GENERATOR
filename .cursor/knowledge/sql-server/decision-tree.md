# SQL Server Decision Tree - Cây Quyết Định

## Giới thiệu

Tài liệu này cung cấp cây quyết định để hướng dẫn việc lựa chọn các giải pháp và cấu hình phù hợp cho SQL Server trong các tình huống khác nhau.

---

## 1. Performance Troubleshooting Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│              PERFORMANCE ISSUE DETECTED                          │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ Is the issue on a specific      │
              │ query or overall system?        │
              └─────────────────────────────────┘
                    │                     │
                    ▼                     ▼
               [Specific Query]       [System-wide]
                    │                     │
                    ▼                     ▼
         ┌──────────────────┐    ┌──────────────────────┐
         │ Get execution    │    │ Check wait statistics│
         │ plan             │    └──────────────────────┘
         └──────────────────┘               │
                    │                      ▼
                    ▼              ┌──────────────────────┐
         ┌──────────────────┐      │ What is top wait?   │
         │ Is plan optimal? │      └──────────────────────┘
         └──────────────────┘               │
              │         │                    │
         [Yes]      [No]                    ▼
              │         │         ┌──────────────────────┐
              ▼         ▼         │ Category?            │
    ┌─────────────┐ ┌─────────┐   │ - CXPACKET → Go to A │
    │Check stats  │ │ Analyze │   │ - PAGEIOLATCH → Go to B│
    │and indexes  │ │ operators│  │ - LCK_M_* → Go to C │
    └─────────────┘ └─────────┘   │ - SOS_* → Go to D │
              │         │         │ - Other → Investigate │
              ▼         ▼         └──────────────────────┘
    ┌─────────────────────────────────────────────────────┐
    │  A. PARALLELISM ISSUES (CXPACKET)                   │
    ├─────────────────────────────────────────────────────┤
    │  1. Check MAXDOP setting:                           │
    │     EXEC sp_configure 'max degree of parallelism';  │
    │                                                     │
    │  2. If MAXDOP = 0 or too high:                      │
    │     - OLTP workload: SET to 0 or number of cores   │
    │     - DW workload: Consider 0                       │
    │                                                     │
    │  3. If specific query:                              │
    │     - Add OPTION (MAXDOP 1) hint                   │
    │     - Or tune query to avoid parallelism overhead  │
    │                                                     │
    │  4. Check cost threshold for parallelism:          │
    │     - Default: 5 (often too low)                   │
    │     - Consider: 25-50 for better parallelization   │
    └─────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────┐
    │  B. I/O ISSUES (PAGEIOLATCH)                       │
    ├─────────────────────────────────────────────────────┤
    │  1. Check disk latency:                            │
    │     SELECT * FROM sys.dm_io_virtual_file_stats     │
    │     WHERE num_of_reads > 0;                        │
    │                                                     │
    │  2. If avg_read_latency_ms > 10ms for data files:  │
    │     - Add more memory                              │
    │     - Optimize indexes (reduce reads)              │
    │     - Consider faster storage (SSD)                │
    │                                                     │
    │  3. If tempdb related:                             │
    │     - Increase number of tempdb data files        │
    │     - Move to faster storage                       │
    │                                                     │
    │  4. Check for missing indexes:                     │
    │     SELECT * FROM sys.dm_db_missing_index_details  │
    └─────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────┐
    │  C. LOCKING ISSUES (LCK_M_*)                       │
    ├─────────────────────────────────────────────────────┤
    │  1. Find blocking session:                         │
    │     SELECT * FROM sys.dm_exec_requests             │
    │     WHERE blocking_session_id > 0;                 │
    │                                                     │
    │  2. Check locks held:                              │
    │     SELECT * FROM sys.dm_tran_locks                │
    │     WHERE request_session_id = @blocker_id;       │
    │                                                     │
    │  3. Options:                                       │
    │     a. If long-running query:                      │
    │        - Optimize the blocking query              │
    │        - Break into smaller transactions          │
    │                                                     │
    │     b. If data modification:                       │
    │        - Use optimistic locking                   │
    │        - Reduce transaction scope                  │
    │                                                     │
    │     c. If necessary:                               │
    │        - KILL blocking session (with caution)      │
    │                                                     │
    │  4. Prevention:                                    │
    │     - Index tuning                                 │
    │     - Proper transaction management                │
    │     - Consider RCSI for read-heavy workloads       │
    └─────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────┐
    │  D. MEMORY ISSUES (SOS_SCHEDULER_YIELD, RESOURCE_SEMAPHORE)│
    ├─────────────────────────────────────────────────────┤
    │  1. Check memory configuration:                    │
    │     EXEC sp_configure 'max server memory';         │
    │                                                     │
    │  2. If max memory too high:                        │
    │     - Leave 4GB or 10% for OS (whichever is larger)│
    │     - Set appropriately for SQL Server            │
    │                                                     │
    │  3. Check memory pressure:                         │
    │     SELECT * FROM sys.dm_os_ring_buffers          │
    │     WHERE ring_buffer_type = 'RING_BUFFER_RESOURCE_MONITOR'│
    │                                                     │
    │  4. If query memory issues (RESOURCE_SEMAPHORE):   │
    │     - Optimize large queries                       │
    │     - Add covering indexes                         │
    │     - Reduce memory grants                         │
    │     - Consider query hints                        │
    └─────────────────────────────────────────────────────┘
```

---

## 2. Index Selection Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│              CREATE NEW INDEX                                    │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ What is the table size?         │
              └─────────────────────────────────┘
                    │         │           │
               [Small]    [Medium]     [Large]
                <10K       10K-1M       >1M rows
                rows        rows
                    │         │           │
                    ▼         ▼           ▼
            ┌────────────┐ ┌────────────┐ ┌────────────────────┐
            │ Index may  │ │Proceed with│ │ Thorough analysis │
            │ not be     │ │ analysis   │ │ required           │
            │ needed     │ │            │ └────────────────────┘
            └────────────┘ └────────────┘          │
                                                   ▼
                        ┌───────────────────────────────────────┐
                        │ What is the query pattern?            │
                        └───────────────────────────────────────┘
                                        │
          ┌─────────────────────────────┼─────────────────────────────┐
          │                             │                             │
          ▼                             ▼                             ▼
    ┌───────────────┐          ┌───────────────┐           ┌───────────────┐
    │Point lookup   │          │Range query    │           │JOIN           │
    │(WHERE x = y)  │          │(WHERE x > a)  │           │               │
    └───────────────┘          └───────────────┘           └───────────────┘
          │                             │                             │
          ▼                             ▼                             ▼
    ┌───────────────┐          ┌───────────────┐           ┌───────────────┐
    │ Column = key  │          │ Range column  │           │ Join columns  │
    │ selectivity?  │          │ = first key   │           │ = keys        │
    └───────────────┘          └───────────────┘           └───────────────┘
          │                             │                             │
    ┌─────┴─────┐                 ┌─────┴─────┐                ┌─────┴─────┐
   [High]      [Low]              [High]      [Low]           [Any]
  >95% unique  <95%              >selectivity <selectivity
    │             │                │             │               │
    ▼             ▼                ▼             ▼               ▼
  ┌───────┐  ┌───────────┐    ┌───────────┐ ┌─────────────┐ ┌───────────┐
  │Single │  │Consider   │    │Composite  │ │Consider     │ │Composite  │
  │column │  │filtered   │    │on range   │ │covering     │ │with INCLUDE│
  │index  │  │or don't   │    │column     │ │index        │ │           │
  │       │  │index      │    │first      │ │for large    │ │           │
  └───────┘  └───────────┘    └───────────┘ │tables       │ └───────────┘
                                            └─────────────┘

    ┌─────────────────────────────────────────────────────────────┐
    │ DECISION SUMMARY                                            │
    ├─────────────────────────────────────────────────────────────┤
    │                                                             │
    │  1. CLUSTERED INDEX                                         │
    │     ✓ One per table (usually on PK)                        │
    │     ✓ Best for: Range queries, PK lookups                  │
    │     ✓ Choose columns with:                                 │
    │       - High cardinality                                    │
    │       - Sequential values (IDENTITY)                       │
    │       - Frequently used in ORDER BY                         │
    │                                                             │
    │  2. NONCLUSTERED INDEX                                      │
    │     ✓ Multiple per table                                    │
    │     ✓ Best for: Covering queries, specific column searches │
    │     ✓ Include frequently SELECT columns (INCLUDE)           │
    │                                                             │
    │  3. COVERING INDEX                                          │
    │     ✓ Nonclustered + INCLUDE for all SELECT columns         │
    │     ✓ Eliminates table/index lookups                        │
    │     ✓ Use when: Query runs frequently but is slow           │
    │                                                             │
    │  4. FILTERED INDEX                                          │
    │     ✓ Indexes subset of rows                                │
    │     ✓ Use when: Queries filter on specific value            │
    │     ✓ Examples: IsDeleted=0, Status='Active'               │
    │                                                             │
    │  5. COMPOSITE INDEX                                         │
    │     ✓ Multiple columns                                     │
    │     ✓ Column order: Equality → Range → Sort                 │
    │     ✓ Use when: Queries filter on multiple columns         │
    │                                                             │
    └─────────────────────────────────────────────────────────────┘
```

---

## 3. Backup Strategy Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│              DESIGN BACKUP STRATEGY                              │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ What is the Recovery Point     │
              │ Objective (RPO)?               │
              └─────────────────────────────────┘
                    │         │           │
              [<15 min]  [15-60 min]  [>1 hour]
                    │         │           │
                    ▼         ▼           ▼
         ┌─────────────┐ ┌──────────┐ ┌──────────────┐
         │Log backup   │ │Log backup│ │Differential  │
         │every 5-15min│ │every 1hr │ │backups only  │
         └─────────────┘ └──────────┘ └──────────────┘
                │             │              │
                └─────────────┴──────────────┘
                                 │
                                 ▼
              ┌─────────────────────────────────┐
              │ What is the Recovery Time       │
              │ Objective (RTO)?               │
              └─────────────────────────────────┘
                    │         │           │
               [<1 hour]  [1-4 hours]  [>4 hours]
                    │         │           │
                    ▼         ▼           ▼
         ┌─────────────┐ ┌──────────┐ ┌──────────────┐
         │Full + Diff +│ │Full +   │ │Full backups  │
         │Frequent Logs│ │Diff +   │ │with possible │
         │             │ │Log      │ │data loss     │
         └─────────────┘ └──────────┘ └──────────────┘
                │             │              │
                └─────────────┴──────────────┘
                                 │
                                 ▼
              ┌─────────────────────────────────┐
              │ What is the database size?     │
              └─────────────────────────────────┘
                    │         │           │
              [<100GB]  [100-500GB]  [>500GB]
                    │         │           │
                    ▼         ▼           ▼
         ┌─────────────┐ ┌──────────┐ ┌──────────────┐
         │Full daily   │ │Full +   │ │Consider      │
         │Diff every   │ │Diff +   │ │partial      │
         │4-6 hours   │ │Log +    │ │backup or    │
         │Log 15 min  │ │Stretch  │ │filegroups  │
         └─────────────┘ └──────────┘ └──────────────┘

    ┌─────────────────────────────────────────────────────────────┐
    │ RECOVERY MODEL SELECTION                                    │
    ├─────────────────────────────────────────────────────────────┤
    │                                                             │
    │  ┌──────────────────┐  ┌──────────────────┐               │
    │  │ FULL             │  │ SIMPLE            │               │
    │  ├──────────────────┤  ├──────────────────┤               │
    │  │ • Point-in-time  │  │ • Cannot do      │               │
    │  │   recovery       │  │   point-in-time  │               │
    │  │ • Log backups    │  │ • Auto-truncates │               │
    │  │   required       │  │   transaction log│               │
    │  │ • Full logging    │  │ • Less log space │               │
    │  │                 │  │   needed         │               │
    │  │ USE FOR:         │  │                 │               │
    │  │ • Production     │  │ USE FOR:         │               │
    │  │ • Critical data  │  │ • Dev/Test      │               │
    │  │ • Audit needs    │  │ • Read-only DBs │               │
    │  └──────────────────┘  └──────────────────┘               │
    │                                                             │
    │  ┌──────────────────┐                                      │
    │  │ BULK_LOGGED      │                                      │
    │  ├──────────────────┤                                      │
    │  │ • Minimal logging│                                      │
    │  │   for bulk ops   │                                      │
    │  │ • Point-in-time  │                                      │
    │  │   except bulk    │                                      │
    │  │ • Smaller logs   │                                      │
    │  │                 │                                      │
    │  │ USE FOR:         │                                      │
    │  │ • Periodic ETL   │                                      │
    │  │ • Bulk imports   │                                      │
    │  └──────────────────┘                                      │
    └─────────────────────────────────────────────────────────────┘
```

---

## 4. High Availability Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│              SELECT HA/DR SOLUTION                               │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ What is your SQL Server         │
              │ Edition?                        │
              └─────────────────────────────────┘
                    │         │           │
              [Enterprise] [Standard] [Express/Web]
                    │         │           │
                    ▼         ▼           ▼
         ┌─────────────┐ ┌──────────┐ ┌──────────────┐
         │Full options │ │Limited  │ │Basic options │
         │available    │ │options  │ │only          │
         └─────────────┘ └──────────┘ └──────────────┘
                │             │              │
                └─────────────┴──────────────┘
                                 │
                                 ▼
              ┌─────────────────────────────────┐
              │ What is your RTO/RPO requirement?│
              └─────────────────────────────────┘
                    │         │           │
              [Zero loss] [Minutes]  [Hours/Loss OK]
              Real-time  <30 min
                    │         │           │
                    ▼         ▼           ▼
         ┌─────────────┐ ┌──────────┐ ┌──────────────┐
         │Always On   │ │Log       │ │Basic backup  │
         │AG with     │ │Shipping  │ │restore       │
         │Sync commit │ │          │ │              │
         └─────────────┘ └──────────┘ └──────────────┘

    ┌─────────────────────────────────────────────────────────────┐
    │ SOLUTION COMPARISON                                         │
    ├─────────────────────────────────────────────────────────────┤
    │                                                             │
    │  ┌─────────────────────┐  ┌─────────────────────────────┐   │
    │  │ Always On AG        │  │ Log Shipping               │   │
    │  ├─────────────────────┤  ├─────────────────────────────┤   │
    │  │ RTO: Seconds-Minutes│  │ RTO: Minutes-Hours         │   │
    │  │ RPO: Zero (sync)    │  │ RPO: Minutes-hours         │   │
    │  │ Auto failover: Yes   │  │ Auto failover: No         │   │
    │  │ Read scale-out: Yes  │  │ Read scale-out: No        │   │
    │  │ Cost: Enterprise     │  │ Cost: Standard+           │   │
    │  └─────────────────────┘  └─────────────────────────────┘   │
    │                                                             │
    │  ┌─────────────────────┐  ┌─────────────────────────────┐   │
    │  │ Database Mirroring   │  │ Failover Clustering         │   │
    │  ├─────────────────────┤  ├─────────────────────────────┤   │
    │  │ (Deprecated)         │  │ RTO: Minutes               │   │
    │  │ RTO: Seconds        │  │ RPO: Depends on app        │   │
    │  │ RPO: Zero (sync)    │  │ Single database: No        │   │
    │  │ Auto failover: Yes   │  │ Multiple DBs: Yes         │   │
    │  │ Read scale-out: No  │  │ Read scale-out: No        │   │
    │  └─────────────────────┘  └─────────────────────────────┘   │
    │                                                             │
    └─────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────┐
    │ DECISION FLOWCHART                                          │
    ├─────────────────────────────────────────────────────────────┤
    │                                                             │
    │  START                                                       │
    │   │                                                          │
    │   ▼                                                          │
    │  Can you afford Enterprise Edition?                         │
    │   │                                                          │
    │   ├──[Yes]──→ Need zero RPO?                               │
    │   │                │                                        │
    │   │           [Yes] │ [No]                                  │
    │   │                ▼ ▼                                      │
    │   │         AG Sync or AG Async                            │
    │   │                │                                        │
    │   ├──[No]───→ Need read scale-out?                         │
    │   │                │                                        │
    │   │           [Yes] │ [No]                                  │
    │   │                ▼ ▼                                      │
    │   │         AG Read-only │ Log Shipping                     │
    │   │                │                                        │
    │   ▼                 │                                        │
    │  Need multiple DBs  │                                        │
    │  failover together? │                                        │
    │   │                 │                                        │
    │   ├──[Yes]──→ Failover Cluster + AG                        │
    │   │                │                                        │
    │   ├──[No]───→ AG Basic or Log Shipping                    │
    │   │                │                                        │
    │   └──[Standalone]→ Consider Log Shipping or Backup/Restore │
    │                                                             │
    └─────────────────────────────────────────────────────────────┘
```

---

## 5. Data Type Selection Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│              SELECT DATA TYPE                                    │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ What type of data?              │
              └─────────────────────────────────┘
                    │         │         │         │
              ┌─────┴───┐ ┌───┴───┐ ┌───┴───┐ ┌───┴────┐
              │ Numeric │ │ String│ │ Date  │ │ Other  │
              └─────┬───┘ └───┬───┘ └───┬───┘ └───┬────┘
                    │         │         │         │
                    ▼         ▼         ▼         ▼
              ┌───────────┐ ┌────────┐ ┌────────┐ ┌──────────┐
              │ See Num. │ │See Str.│ │See Date│ │See Other │
              │ Types    │ │ Types │ │ Types  │ │ Types    │
              └───────────┘ └────────┘ └────────┘ └──────────┘

    ┌─────────────────────────────────────────────────────────────┐
    │ NUMERIC TYPES                                              │
    ├─────────────────────────────────────────────────────────────┤
    │                                                             │
    │  ┌────────────────────────────────────────────────────────┐│
    │  │ INTEGER NUMBERS                                        ││
    │  ├────────────────────────────────────────────────────────┤│
    │  │ Value Range              │ Use                        ││
    │  │ TINYINT   (0-255)        │ Flags, small counts        ││
    │  │ SMALLINT  (-32K to 32K)  │ IDs for small tables       ││
    │  │ INT       (-2B to 2B)     │ Default for most IDs       ││
    │  │ BIGINT    (-9Q to 9Q)     │ Large IDs, big counts      ││
    │  └────────────────────────────────────────────────────────┘│
    │                                                             │
    │  ┌────────────────────────────────────────────────────────┐│
    │  │ DECIMAL/FLOAT                                          ││
    │  ├────────────────────────────────────────────────────────┤│
    │  │ Prec.   │ Storage │ Use                              ││
    │  │ DECIMAL(10,2)  │ 5 bytes│ Money, measurements (BEST)  ││
    │  │ DECIMAL(18,2)  │ 9 bytes│ Large monetary values        ││
    │  │ FLOAT(24)      │ 4 bytes│ Scientific calculations      ││
    │  │ FLOAT(53)      │ 8 bytes│ Scientific calculations       ││
    │  │ MONEY (8 bytes)│         │ Monetary (but has issues)   ││
    │  └────────────────────────────────────────────────────────┘│
    │                                                             │
    │  DECISION:                                                  │
    │  • Always use DECIMAL for money, not FLOAT or MONEY        │
    │  • DECIMAL(10,2) for most currency values                  │
    │  • DECIMAL(18,2) for large monetary amounts                │
    │  • DECIMAL(p,s) where p=symbols+sigits, s=decimal places  │
    └─────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────┐
    │ STRING TYPES                                                │
    ├─────────────────────────────────────────────────────────────┤
    │                                                             │
    │  ┌────────────────────────────────────────────────────────┐│
    │  │ FIXED vs VARIABLE                                      ││
    │  ├────────────────────────────────────────────────────────┤│
    │  │ CHAR(n)     │ Fixed n chars │ Pad with spaces          ││
    │  │ VARCHAR(n)  │ Variable, 1-8000 │ Most cases            ││
    │  │ NCHAR(n)    │ Fixed Unicode  │ For multilingual        ││
    │  │ NVARCHAR(n) │ Variable Unicode │ Default for .NET      ││
    │  │ VARCHAR(MAX)│ Large text     │ When n unknown/large   ││
    │  └────────────────────────────────────────────────────────┘│
    │                                                             │
    │  DECISION:                                                  │
    │  • VARCHAR(MAX) replaces TEXT, IMAGE (deprecated)          │
    │  • Use NVARCHAR for Unicode/multilingual data              │
    │  • Size VARCHAR columns appropriately (don't use MAX if not needed)│
    │  • Use VARCHAR(n) not VARCHAR(8000) for known max length  │
    │  • Consider collation for case-sensitive comparisons      │
    └─────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────┐
    │ DATE TYPES                                                  │
    ├─────────────────────────────────────────────────────────────┤
    │                                                             │
    │  ┌────────────────────────────────────────────────────────┐│
    │  │ Type        │ Range                    │ Precision   ││
    │  ├─────────────┼──────────────────────────┼─────────────┤│
    │  │ DATE        │ 0001-01-01 to 9999-12-31 │ 1 day       ││
    │  │ TIME        │ 00:00:00 to 23:59:59     │ 100ns       ││
    │  │ DATETIME    │ 1753-01-01 to 9999-12-31 │ 3.33ms     ││
    │  │ DATETIME2   │ 0001-01-01 to 9999-12-31 │ 100ns      ││
    │  │ SMALLDATETIME│ 1900-01-01 to 2079-06-06│ 1 minute   ││
    │  │ DATETIMEOFFSET│ Same as DATETIME2 + TZ │ 100ns      ││
    │  └────────────────────────────────────────────────────────┘│
    │                                                             │
    │  DECISION:                                                  │
    │  • DATETIME2(0-7) is SQL Server 2008+ best practice        │
    │  • DATETIME2(0) = 1 second precision, good for logs       │
    │  • DATETIME2(3) = 1 millisecond, good for most cases       │
    │  • DATETIMEOFFSET when timezone needed                    │
    │  • Avoid DATETIME (legacy, less precise)                   │
    └─────────────────────────────────────────────────────────────┘
```

---

## 6. Query Optimization Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│              OPTIMIZE SLOW QUERY                                 │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ Step 1: Get actual execution    │
              │ plan and run time               │
              └─────────────────────────────────┘
                    │
                    ▼
              ┌─────────────────────────────────┐
              │ Are there warnings in plan?     │
              │ (Yellow triangle)               │
              └─────────────────────────────────┘
                    │
            ┌───────┴───────┐
           [Yes]          [No]
            │               │
            ▼               ▼
    ┌───────────────┐ ┌─────────────────────┐
    │Analyze warning│ │Check for expensive  │
    │- No statistics│ │operations           │
    │- Memory grant │ │- Table/index scans  │
    │- Spill to temp│ │- Sorts without index│
    └───────────────┘ │- Hash joins large   │
            │         │- Multiple JOINs     │
            │         └─────────────────────┘
            │                    │
            └────────┬───────────┘
                     ▼
    ┌───────────────────────────────────────┐
    │ Step 2: Check operators in plan        │
    ├───────────────────────────────────────┤
    │                                        │
    │   [Table Scan] → Add covering index    │
    │        │                               │
    │   [Index Scan] → Consider index with  │
    │        │        INCLUDE columns        │
    │   [Index Seek] → Good, check I/O cost │
    │        │                               │
    │   [Sort] → Add ORDER BY with index   │
    │        │                               │
    │   [Hash Join] → Consider hint or index │
    │        │                               │
    │   [Nested Loop] → Good if outer small │
    │        │                               │
    │   [Lookup] → Add covering index      │
    │                                        │
    └───────────────────────────────────────┘
                     │
                     ▼
    ┌───────────────────────────────────────┐
    │ Step 3: Check index recommendations    │
    ├───────────────────────────────────────┤
    │                                        │
    │ SELECT * FROM sys.dm_db_missing_index_│
    │ details WHERE database_id = DB_ID();   │
    │                                        │
    │ If recommendations exist:             │
    │ 1. Review column order                 │
    │ 2. Check if INCLUDE columns needed     │
    │ 3. Consider filtered index            │
    │ 4. Test with actual query              │
    │ 5. Monitor impact                      │
    │                                        │
    └───────────────────────────────────────┘
                     │
                     ▼
    ┌───────────────────────────────────────┐
    │ Step 4: Check statistics               │
    ├───────────────────────────────────────┤
    │                                        │
    │ DBCC SHOW_STATISTICS('Table', 'Index');│
    │                                        │
    │ If statistics are stale:               │
    │ UPDATE STATISTICS Table WITH FULLSCAN; │
    │                                        │
    │ If histogram is outdated:              │
    │ Consider trace flag 2371              │
    │ (Auto-update threshold)               │
    │                                        │
    └───────────────────────────────────────┘
                     │
                     ▼
    ┌───────────────────────────────────────┐
    │ Step 5: Query rewrite options          │
    ├───────────────────────────────────────┤
    │                                        │
    │ 1. Replace OR with IN or UNION:       │
    │    WHERE A=1 OR A=2 → WHERE A IN(1,2) │
    │                                        │
    │ 2. Avoid functions on indexed columns │
    │    WHERE YEAR(d)=2024 → WHERE d >=... │
    │                                        │
    │ 3. Use EXISTS instead of IN:           │
    │    WHERE x IN (SELECT y FROM z)       │
    │    → WHERE EXISTS (SELECT 1 FROM z)    │
    │                                        │
    │ 4. Use JOIN instead of subquery:       │
    │    (unless subquery is more efficient)│
    │                                        │
    │ 5. Break complex queries into CTEs:   │
    │    WITH cte AS (...) SELECT FROM cte   │
    │                                        │
    └───────────────────────────────────────┘
                     │
                     ▼
    ┌───────────────────────────────────────┐
    │ Step 6: If still slow, consider hints │
    ├───────────────────────────────────────┤
    │                                        │
    │ OPTION (MAXDOP n) - Limit parallelism │
    │ OPTION (RECOMPILE) - Always recompile │
    │ OPTION (OPTIMIZE FOR @var = val)     │
    │ OPTION (USE HINT ('DISABLE_OPTIMIZER')│
    │                                        │
    │ USE INDEX (index_name)                │
    │ FORCE ORDER - Force join order        │
    │ LOOP/HASH/MERGE JOIN - Force join type│
    │                                        │
    │ WARNING: Test thoroughly before       │
    │ production deployment!                │
    │                                        │
    └───────────────────────────────────────┘
```

---

## 7. Security Hardening Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│              SECURITY HARDENING CHECKLIST                       │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ 1. Authentication               │
              └─────────────────────────────────┘
                    │
                    ▼
         ┌─────────────────────────────────┐
         │ Use Windows Authentication?      │
         └─────────────────────────────────┘
                │                 │
              [Yes]              [No]
                │                 │
                ▼                 ▼
         ┌───────────┐     ┌─────────────────┐
         │Enforce    │     │ Strong passwords │
         │complexity │     │ policy enabled? │
         │policy     │     └─────────────────┘
         └───────────┘            │
                                 ▼
                    ┌─────────────────────────┐
                    │ Disable sa or rename   │
                    │ Implement separate     │
                    │ admin accounts         │
                    └─────────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ 2. Authorization                 │
              └─────────────────────────────────┘
                    │
                    ▼
         ┌─────────────────────────────────┐
         │ Apply principle of least priv?  │
         └─────────────────────────────────┘
                │                 │
              [Yes]              [No]
                │                 │
                ▼                 ▼
         ┌───────────┐     ┌─────────────────┐
         │Review per │     │Start with deny, │
         │missions   │     │grant as needed │
         │regularly  │     │                │
         └───────────┘     └─────────────────┘
                                │
                                ▼
         ┌─────────────────────────────────┐
         │ Use roles instead of direct    │
         │ user permissions?              │
         └─────────────────────────────────┘
                │                 │
              [Yes]              [No]
                │                 │
                ▼                 ▼
         ┌───────────┐     ┌─────────────────┐
         │Good!      │     │Create roles for │
         │Document   │     │each function    │
         │and audit  │     │                │
         └───────────┘     └─────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ 3. Data Protection               │
              └─────────────────────────────────┘
                    │
                    ▼
         ┌─────────────────────────────────┐
         │ Sensitive data to protect?      │
         └─────────────────────────────────┘
                │                 │
           [Yes]              [No]
                │                 │
                ▼                 ▼
         ┌───────────┐     ┌─────────────────┐
         │Enable TDE │     │Enable TDE for  │
         │and Always │     │at-rest encrypt │
         │Encrypted  │     │Audit access    │
         └───────────┘     └─────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ 4. Network Security             │
              └─────────────────────────────────┘
                    │
                    ▼
         ┌─────────────────────────────────┐
         │ Configure:                      │
         │ □ TLS for connections           │
         │ □ Firewall rules                │
         │ □ Named pipes disabled (if not  │
         │   needed)                       │
         │ □ Default port changed?         │
         └─────────────────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ 5. Monitoring & Auditing       │
              └─────────────────────────────────┘
                    │
                    ▼
         ┌─────────────────────────────────┐
         │ □ Enable SQL Server Audit       │
         │ □ Track failed login attempts  │
         │ □ Log all DDL changes          │
         │ □ Regular security reviews     │
         │ □ Set up alerts for suspicious │
         │   activity                     │
         └─────────────────────────────────┘
```

---

## 8. Database Design Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│              DESIGN NEW TABLE                                    │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ 1. Choose Primary Key          │
              └─────────────────────────────────┘
                    │
         ┌──────────┼──────────┐
         │          │          │
         ▼          ▼          ▼
      [INT ID]  [GUID]    [Natural Key]
         │          │          │
         ▼          ▼          ▼
    Use INT      Use GUID   Use natural
    IDENTITY     only if    key only if
    for most     truly      truly unique
    cases        needed     and small
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ 2. Normalize or Denormalize?    │
              └─────────────────────────────────┘
                    │
         ┌──────────┴──────────┐
         │                      │
      [OLTP]                  [OLAP/DW]
         │                      │
         ▼                      ▼
    Normalize to        Consider denorm.
    3NF for data        for read perf.
    integrity           (star schema)
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ 3. Choose Data Types            │
              └─────────────────────────────────┘
                    │
         ┌──────────┼──────────┐
         │          │          │
         ▼          ▼          ▼
    Use most      Use      Use appropriate
    restrictive   NVARCHAR sizes
    type that     for       (not 1000 for
    fits          strings   small values)
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ 4. Handle NULLs appropriately    │
              └─────────────────────────────────┘
                    │
         ┌──────────┴──────────┐
         │                      │
       [Usually NOT NULL]    [NULL needed]
         │                      │
         ▼                      ▼
    Set NOT NULL          Document meaning
    with DEFAULT          of NULL
    if applicable
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ 5. Add audit columns?           │
              └─────────────────────────────────┘
                    │
         ┌──────────┴──────────┐
         │                      │
       [Yes]                  [No]
         │                      │
         ▼                      ▼
    Add standard:          Consider
    - CreatedDate          temporal tables
    - CreatedBy            for full history
    - ModifiedDate
    - ModifiedBy
    - IsDeleted (soft del)
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ 6. Create Initial Indexes       │
              └─────────────────────────────────┘
                    │
         ┌──────────┼──────────┐
         │          │          │
         ▼          ▼          ▼
    Clustered    FK columns   Review if
    on PK        (if many     covering
                 JOINs)       index needed
```

---

## 9. Migration Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│              MIGRATE TO NEW SQL SERVER                          │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ 1. Assess current environment   │
              └─────────────────────────────────┘
                    │
         ┌──────────┼──────────┐
         │          │          │
         ▼          ▼          ▼
    Inventory    Analyze     Check
    databases    workload    dependencies
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ 2. Choose migration method     │
              └─────────────────────────────────┘
                    │
         ┌──────────┼──────────┐
         │          │          │
    [Simple]    [Complex]  [Minimal Downtime]
         │          │          │
         ▼          ▼          ▼
    Backup/     Log          Always On AG
    Restore     Shipping     migration
    + Scripts   Migration    or Backup/
                + Log        Restore +
                Restore      Log Shipping
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ 3. Pre-migration tasks          │
              └─────────────────────────────────┘
                    │
                    ▼
    □ Backup all databases
    □ Test backup restore
    □ Check compatibility
    □ Update connection strings
    □ Plan rollback
    □ Schedule maintenance window
    □ Notify stakeholders
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ 4. Execute migration           │
              └─────────────────────────────────┘
                    │
         ┌──────────┼──────────┐
         │          │          │
         ▼          ▼          ▼
    Phase 1    Phase 2    Phase 3
    Migrate   Migrate   Migrate
    Schema    Data      Users/Permissions
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ 5. Post-migration validation    │
              └─────────────────────────────────┘
                    │
                    ▼
    □ Verify data integrity
    □ Test application functionality
    □ Check performance (baseline comparison)
    □ Monitor errors
    □ Update monitoring
    □ Document changes
```
