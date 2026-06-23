-- ============================================================
-- DECISIONS.SQLITE - Lưu trữ Architecture Decision Records
-- ============================================================
-- Schema Version: 1.0.0
-- Created: 2026-06-23
-- Purpose: Ghi lại tất cả ADR decisions
-- ============================================================

PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

-- ============================================================
-- TABLES
-- ============================================================

-- decisions: Bảng chính lưu ADR
CREATE TABLE IF NOT EXISTS decisions (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'proposed'
        CHECK(status IN ('proposed', 'accepted', 'deprecated', 'superseded')),
    context TEXT NOT NULL,
    decision TEXT NOT NULL,
    consequences TEXT,
    decision_date TEXT NOT NULL DEFAULT (date('now')),
    review_date TEXT,
    domain TEXT NOT NULL,
    priority TEXT DEFAULT 'medium'
        CHECK(priority IN ('low', 'medium', 'high', 'critical')),
    tags TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    created_by TEXT,
    superseded_by TEXT REFERENCES decisions(id),
    deprecated_by TEXT REFERENCES decisions(id)
);

-- decision_links: Liên kết giữa các decisions
CREATE TABLE IF NOT EXISTS decision_links (
    id TEXT PRIMARY KEY,
    source_decision_id TEXT NOT NULL REFERENCES decisions(id) ON DELETE CASCADE,
    target_decision_id TEXT NOT NULL REFERENCES decisions(id) ON DELETE CASCADE,
    link_type TEXT NOT NULL CHECK(link_type IN ('relates', 'supersedes', 'depends', 'conflicts')),
    description TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    UNIQUE(source_decision_id, target_decision_id, link_type)
);

-- decision_risks: Rủi ro liên quan đến decision
CREATE TABLE IF NOT EXISTS decision_risks (
    id TEXT PRIMARY KEY,
    decision_id TEXT NOT NULL REFERENCES decisions(id) ON DELETE CASCADE,
    risk_description TEXT NOT NULL,
    severity TEXT NOT NULL CHECK(severity IN ('low', 'medium', 'high', 'critical')),
    mitigation TEXT,
    probability TEXT CHECK(probability IN ('low', 'medium', 'high')),
    impact TEXT CHECK(impact IN ('low', 'medium', 'high')),
    status TEXT DEFAULT 'identified'
        CHECK(status IN ('identified', 'mitigated', 'accepted', 'transferred')),
    created_at TEXT DEFAULT (datetime('now')),
    resolved_at TEXT
);

-- decision_options: Các options đã được xem xét
CREATE TABLE IF NOT EXISTS decision_options (
    id TEXT PRIMARY KEY,
    decision_id TEXT NOT NULL REFERENCES decisions(id) ON DELETE CASCADE,
    option_title TEXT NOT NULL,
    description TEXT NOT NULL,
    pros TEXT,
    cons TEXT,
    estimated_cost TEXT,
    estimated_effort TEXT,
    selected INTEGER DEFAULT 0,
    rank INTEGER,
    created_at TEXT DEFAULT (datetime('now'))
);

-- decision_reviews: Lịch sử review decisions
CREATE TABLE IF NOT EXISTS decision_reviews (
    id TEXT PRIMARY KEY,
    decision_id TEXT NOT NULL REFERENCES decisions(id) ON DELETE CASCADE,
    review_date TEXT NOT NULL,
    reviewer TEXT NOT NULL,
    verdict TEXT NOT NULL CHECK(verdict IN ('uphold', 'supersede', 'deprecate')),
    notes TEXT,
    next_review_date TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

-- decision_tags: Tags cho decisions
CREATE TABLE IF NOT EXISTS decision_tags (
    decision_id TEXT NOT NULL REFERENCES decisions(id) ON DELETE CASCADE,
    tag TEXT NOT NULL,
    PRIMARY KEY (decision_id, tag)
);

-- ============================================================
-- INDEXES
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_decisions_domain ON decisions(domain);
CREATE INDEX IF NOT EXISTS idx_decisions_status ON decisions(status);
CREATE INDEX IF NOT EXISTS idx_decisions_priority ON decisions(priority);
CREATE INDEX IF NOT EXISTS idx_decisions_date ON decisions(decision_date);
CREATE INDEX IF NOT EXISTS idx_decisions_review_date ON decisions(review_date);
CREATE INDEX IF NOT EXISTS idx_decision_links_source ON decision_links(source_decision_id);
CREATE INDEX IF NOT EXISTS idx_decision_links_target ON decision_links(target_decision_id);
CREATE INDEX IF NOT EXISTS idx_decision_risks_decision ON decision_risks(decision_id);
CREATE INDEX IF NOT EXISTS idx_decision_options_decision ON decision_options(decision_id);
CREATE INDEX IF NOT EXISTS idx_decision_reviews_decision ON decision_reviews(decision_id);

-- ============================================================
-- TRIGGERS
-- ============================================================

CREATE TRIGGER IF NOT EXISTS trg_decisions_updated
AFTER UPDATE ON decisions
BEGIN
    UPDATE decisions SET updated_at = datetime('now') WHERE id = NEW.id;
END;

-- ============================================================
-- VIEWS
-- ============================================================

-- Active decisions view
CREATE VIEW IF NOT EXISTS v_active_decisions AS
SELECT d.*, GROUP_CONCAT(dt.tag) as tags
FROM decisions d
LEFT JOIN decision_tags dt ON d.id = dt.decision_id
WHERE d.status IN ('proposed', 'accepted')
GROUP BY d.id
ORDER BY d.decision_date DESC;

-- Decisions by domain
CREATE VIEW IF NOT EXISTS v_decisions_by_domain AS
SELECT domain, COUNT(*) as count, 
       SUM(CASE WHEN status = 'accepted' THEN 1 ELSE 0 END) as accepted_count
FROM decisions
GROUP BY domain
ORDER BY count DESC;

-- Decisions pending review
CREATE VIEW IF NOT EXISTS v_pending_reviews AS
SELECT d.*, dr.next_review_date, dr.reviewer
FROM decisions d
JOIN decision_reviews dr ON d.id = dr.decision_id
WHERE d.status = 'accepted' 
  AND dr.next_review_date <= date('now')
ORDER BY dr.next_review_date ASC;

-- High priority decisions
CREATE VIEW IF NOT EXISTS v_high_priority_decisions AS
SELECT d.*, GROUP_CONCAT(dt.tag) as tags
FROM decisions d
LEFT JOIN decision_tags dt ON d.id = dt.decision_id
WHERE d.priority IN ('high', 'critical')
  AND d.status IN ('proposed', 'accepted')
GROUP BY d.id
ORDER BY 
    CASE d.priority 
        WHEN 'critical' THEN 1 
        WHEN 'high' THEN 2 
        ELSE 3 
    END,
    d.decision_date DESC;

-- ============================================================
-- SEED DATA
-- ============================================================

INSERT OR IGNORE INTO decisions (id, title, status, context, decision, consequences, domain, priority, tags)
VALUES 
    ('ADR-001', 'Chọn PostgreSQL làm database chính', 'accepted', 
     'Cần chọn một relational database cho enterprise SaaS', 
     'Sử dụng PostgreSQL 16 với Supabase như managed service, hỗ trợ RLS, PGVector, JSONB',
     'PostgreSQL cung cấp rich features, scalability, và excellent performance cho SaaS applications',
     'infrastructure', 'critical', 'database,postgres,supabase'),
     
    ('ADR-002', 'Chọn Next.js 15 làm frontend framework', 'accepted',
     'Cần chọn React framework cho CRM SaaS',
     'Sử dụng Next.js 15 với App Router, Server Components, và TypeScript',
     'Next.js 15 provides excellent DX, performance, và SEO capabilities',
     'frontend', 'high', 'nextjs,react,typescript'),
     
    ('ADR-003', 'Multi-tenant với Row Level Security', 'accepted',
     'Cần chọn strategy cho tenant isolation',
     'Sử dụng PostgreSQL RLS với discriminator column (tenant_id)',
     'RLS cung cấp security ở database level, đơn giản hơn schema isolation',
     'architecture', 'critical', 'multi-tenant,rls,security'),

    ('ADR-004', 'RAG Pipeline với PGVector', 'accepted',
     'Cần chọn vector database cho AI RAG',
     'Sử dụng PGVector extension của PostgreSQL để store và search embeddings',
     'Đơn giản hóa stack, tận dụng existing PostgreSQL infrastructure',
     'ai', 'high', 'rag,pgvector,vector-search'),

    ('ADR-005', 'Clean Architecture cho backend', 'accepted',
     'Cần chọn architecture pattern cho ASP.NET Core backend',
     'Implement Clean Architecture với layers: Domain, Application, Infrastructure, Presentation',
     'Separation of concerns rõ ràng, dễ test, dễ maintain',
     'architecture', 'high', 'clean-architecture,ddd,cqrs');
