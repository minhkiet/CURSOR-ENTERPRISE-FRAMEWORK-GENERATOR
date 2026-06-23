-- ============================================================
-- KNOWLEDGE.SQLITE - Lưu trữ Knowledge Base
-- ============================================================
PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS knowledge_docs (
    id TEXT PRIMARY KEY,
    doc_hash TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    domain TEXT NOT NULL,
    subdomain TEXT,
    category TEXT NOT NULL,
    content TEXT NOT NULL,
    content_summary TEXT,
    keywords TEXT,
    tags TEXT,
    version INTEGER DEFAULT 1,
    author TEXT,
    status TEXT DEFAULT 'active'
        CHECK(status IN ('active', 'archived', 'deprecated', 'draft')),
    source_file TEXT,
    file_path TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS knowledge_chunks (
    id TEXT PRIMARY KEY,
    doc_id TEXT NOT NULL REFERENCES knowledge_docs(id) ON DELETE CASCADE,
    chunk_hash TEXT NOT NULL,
    chunk_text TEXT NOT NULL,
    chunk_index INTEGER,
    start_pos INTEGER,
    end_pos INTEGER,
    tokens INTEGER,
    embedding_id TEXT REFERENCES embeddings(id),
    relevance_score REAL,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS embeddings (
    id TEXT PRIMARY KEY,
    chunk_id TEXT REFERENCES knowledge_chunks(id) ON DELETE CASCADE,
    doc_id TEXT REFERENCES knowledge_docs(id) ON DELETE CASCADE,
    embedding_vector BLOB NOT NULL,
    model TEXT NOT NULL,
    dimensions INTEGER NOT NULL,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS knowledge_links (
    id TEXT PRIMARY KEY,
    source_doc_id TEXT NOT NULL REFERENCES knowledge_docs(id) ON DELETE CASCADE,
    target_doc_id TEXT REFERENCES knowledge_docs(id) ON DELETE SET NULL,
    target_url TEXT,
    link_type TEXT NOT NULL CHECK(link_type IN ('related', 'prerequisite', 'references', 'supplements', 'supersedes')),
    description TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS knowledge_tags (
    doc_id TEXT NOT NULL REFERENCES knowledge_docs(id) ON DELETE CASCADE,
    tag TEXT NOT NULL,
    PRIMARY KEY (doc_id, tag)
);

CREATE TABLE IF NOT EXISTS knowledge_search_history (
    id TEXT PRIMARY KEY,
    query TEXT NOT NULL,
    domain TEXT,
    results_count INTEGER,
    selected_doc_ids TEXT,
    feedback INTEGER CHECK(feedback IN (-1, 0, 1)),
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_knowledge_domain ON knowledge_docs(domain);
CREATE INDEX IF NOT EXISTS idx_knowledge_category ON knowledge_docs(category);
CREATE INDEX IF NOT EXISTS idx_knowledge_chunks_doc ON knowledge_chunks(doc_id);
CREATE INDEX IF NOT EXISTS idx_embeddings_doc ON embeddings(doc_id);
CREATE INDEX IF NOT EXISTS idx_search_history_date ON knowledge_search_history(created_at);

CREATE VIEW IF NOT EXISTS v_knowledge_stats AS
SELECT domain, COUNT(*) as doc_count,
       SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) as active_count,
       COUNT(DISTINCT category) as category_count
FROM knowledge_docs
GROUP BY domain
ORDER BY doc_count DESC;

-- ============================================================
-- EMBEDDINGS.SQLITE - Vector Embeddings Store
-- ============================================================
PRAGMA journal_mode = WAL;

CREATE TABLE IF NOT EXISTS vector_embeddings (
    id TEXT PRIMARY KEY,
    content_hash TEXT NOT NULL UNIQUE,
    content_text TEXT NOT NULL,
    content_type TEXT CHECK(content_type IN ('rule', 'skill', 'knowledge', 'prompt', 'code', 'doc')),
    source_path TEXT,
    domain TEXT,
    metadata TEXT,
    embedding_model TEXT NOT NULL,
    embedding_vector BLOB NOT NULL,
    dimensions INTEGER NOT NULL,
    token_count INTEGER,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS vector_collections (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    model TEXT NOT NULL,
    dimensions INTEGER NOT NULL,
    embedding_count INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS vector_search_results (
    id TEXT PRIMARY KEY,
    query_vector_id TEXT,
    result_vector_id TEXT NOT NULL,
    similarity_score REAL NOT NULL,
    rank INTEGER,
    search_time_ms INTEGER,
    searched_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_vector_content_hash ON vector_embeddings(content_hash);
CREATE INDEX IF NOT EXISTS idx_vector_domain ON vector_embeddings(domain);
CREATE INDEX IF NOT EXISTS idx_vector_content_type ON vector_embeddings(content_type);
CREATE INDEX IF NOT EXISTS idx_vector_collections_name ON vector_collections(name);

-- ============================================================
-- SESSIONS.SQLITE - Session History
-- ============================================================
PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY,
    session_hash TEXT NOT NULL UNIQUE,
    title TEXT,
    summary TEXT,
    domain TEXT,
    tool_count INTEGER DEFAULT 0,
    total_tokens INTEGER DEFAULT 0,
    input_tokens INTEGER DEFAULT 0,
    output_tokens INTEGER DEFAULT 0,
    cost_usd REAL DEFAULT 0.0,
    start_time TEXT NOT NULL,
    end_time TEXT,
    status TEXT CHECK(status IN ('active', 'completed', 'interrupted')),
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS session_messages (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    role TEXT CHECK(role IN ('user', 'assistant', 'system', 'tool')),
    content TEXT NOT NULL,
    tokens INTEGER,
    message_order INTEGER,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS session_context (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    context_type TEXT NOT NULL,
    context_data TEXT NOT NULL,
    loaded_at TEXT DEFAULT (datetime('now')),
    accessed_at TEXT
);

CREATE TABLE IF NOT EXISTS session_rules (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    rule_path TEXT NOT NULL,
    loaded_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS session_skills (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    skill_path TEXT NOT NULL,
    loaded_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_sessions_domain ON sessions(domain);
CREATE INDEX IF NOT EXISTS idx_sessions_status ON sessions(status);
CREATE INDEX IF NOT EXISTS idx_session_messages_session ON session_messages(session_id);
CREATE INDEX IF NOT EXISTS idx_session_context_session ON session_context(session_id);

CREATE VIEW IF NOT EXISTS v_session_stats AS
SELECT domain, COUNT(*) as session_count,
       SUM(total_tokens) as total_tokens,
       SUM(cost_usd) as total_cost,
       AVG(total_tokens) as avg_tokens,
       AVG(tool_count) as avg_tools
FROM sessions
GROUP BY domain
ORDER BY session_count DESC;
