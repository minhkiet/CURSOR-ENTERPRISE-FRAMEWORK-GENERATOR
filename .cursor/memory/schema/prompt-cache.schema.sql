-- ============================================================
-- PROMPT-CACHE.SQLITE - Lưu trữ Prompt Cache
-- ============================================================
PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS prompts (
    id TEXT PRIMARY KEY,
    hash TEXT NOT NULL UNIQUE,
    summary TEXT NOT NULL,
    full_prompt TEXT NOT NULL,
    category TEXT NOT NULL,
    subcategory TEXT,
    domain TEXT NOT NULL,
    tags TEXT,
    version INTEGER DEFAULT 1,
    created_at TEXT DEFAULT (datetime('now')),
    last_used_at TEXT,
    use_count INTEGER DEFAULT 0,
    avg_response_tokens INTEGER,
    avg_input_tokens INTEGER,
    success_rate REAL DEFAULT 0.0,
    pinned INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS prompt_variants (
    id TEXT PRIMARY KEY,
    prompt_id TEXT NOT NULL REFERENCES prompts(id) ON DELETE CASCADE,
    variant_name TEXT NOT NULL,
    variant_prompt TEXT NOT NULL,
    variant_hash TEXT NOT NULL UNIQUE,
    performance_score REAL DEFAULT 0.0,
    sample_size INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now')),
    last_used_at TEXT,
    use_count INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS prompt_responses (
    id TEXT PRIMARY KEY,
    prompt_id TEXT NOT NULL REFERENCES prompts(id) ON DELETE CASCADE,
    response_hash TEXT NOT NULL,
    response_summary TEXT NOT NULL,
    response_full TEXT NOT NULL,
    input_tokens INTEGER,
    output_tokens INTEGER,
    total_tokens INTEGER,
    latency_ms INTEGER,
    model TEXT,
    quality_score REAL,
    usefulness_score REAL,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS prompt_metrics (
    id TEXT PRIMARY KEY,
    prompt_id TEXT NOT NULL REFERENCES prompts(id) ON DELETE CASCADE,
    date TEXT NOT NULL,
    total_uses INTEGER DEFAULT 0,
    success_count INTEGER DEFAULT 0,
    failure_count INTEGER DEFAULT 0,
    avg_latency_ms INTEGER,
    avg_tokens INTEGER,
    cost_usd REAL DEFAULT 0.0,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_prompts_hash ON prompts(hash);
CREATE INDEX IF NOT EXISTS idx_prompts_domain ON prompts(domain);
CREATE INDEX IF NOT EXISTS idx_prompts_last_used ON prompts(last_used_at);
CREATE INDEX IF NOT EXISTS idx_prompt_responses_prompt ON prompt_responses(prompt_id);
CREATE INDEX IF NOT EXISTS idx_prompt_metrics_prompt_date ON prompt_metrics(prompt_id, date);

CREATE VIEW IF NOT EXISTS v_prompt_stats AS
SELECT 
    p.id, p.summary, p.category, p.domain, p.use_count, p.success_rate,
    p.avg_response_tokens, p.avg_input_tokens,
    pm.avg_latency_ms, pm.cost_usd
FROM prompts p
LEFT JOIN (
    SELECT prompt_id, AVG(avg_latency_ms) as avg_latency_ms, SUM(cost_usd) as cost_usd
    FROM prompt_metrics GROUP BY prompt_id
) pm ON p.id = pm.prompt_id
ORDER BY p.use_count DESC;

CREATE VIEW IF NOT EXISTS v_top_prompts AS
SELECT p.*, pr.avg_quality
FROM prompts p
JOIN (
    SELECT prompt_id, AVG(quality_score) as avg_quality
    FROM prompt_responses GROUP BY prompt_id
) pr ON p.id = pr.prompt_id
ORDER BY pr.avg_quality DESC, p.use_count DESC;
