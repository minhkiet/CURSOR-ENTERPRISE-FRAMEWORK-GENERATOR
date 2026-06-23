-- ============================================================
-- BUGS.SQLITE - Lưu trữ Bug History và Tracking
-- ============================================================
-- Schema Version: 1.0.0
-- Created: 2026-06-23
-- Purpose: Ghi lại tất cả bugs, solutions, và patterns
-- ============================================================

PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

-- ============================================================
-- TABLES
-- ============================================================

-- bugs: Bảng chính lưu bug information
CREATE TABLE IF NOT EXISTS bugs (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    severity TEXT NOT NULL CHECK(severity IN ('critical', 'high', 'medium', 'low')),
    priority TEXT NOT NULL DEFAULT 'medium'
        CHECK(priority IN ('critical', 'high', 'medium', 'low')),
    status TEXT NOT NULL DEFAULT 'open'
        CHECK(status IN ('open', 'investigating', 'identified', 'fixing', 'fixed', 'verified', 'closed', 'wontfix')),
    domain TEXT NOT NULL,
    component TEXT,
    file_path TEXT,
    line_number INTEGER,
    stack_trace TEXT,
    error_code TEXT,
    frequency TEXT CHECK(frequency IN ('once', 'rare', 'intermittent', 'frequent', 'constant')),
    reproducibility TEXT CHECK(reproducibility IN ('not-tried', 'cannot-reproduce', 'hard', 'easy', 'always')),
    first_observed TEXT NOT NULL,
    last_observed TEXT,
    reported_by TEXT,
    assigned_to TEXT,
    tags TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

-- bug_root_causes: Root cause analysis
CREATE TABLE IF NOT EXISTS bug_root_causes (
    id TEXT PRIMARY KEY,
    bug_id TEXT NOT NULL REFERENCES bugs(id) ON DELETE CASCADE,
    root_cause TEXT NOT NULL,
    root_cause_category TEXT NOT NULL
        CHECK(root_cause_category IN ('coding-error', 'design-flaw', 'configuration', 'dependency', 'environment', 'data', 'third-party', 'unknown')),
    root_cause_details TEXT,
    affected_components TEXT,
    similar_bugs_count INTEGER DEFAULT 0,
    confidence TEXT CHECK(confidence IN ('low', 'medium', 'high')),
    identified_at TEXT DEFAULT (datetime('now')),
    identified_by TEXT
);

-- bug_fixes: Solutions và fixes
CREATE TABLE IF NOT EXISTS bug_fixes (
    id TEXT PRIMARY KEY,
    bug_id TEXT NOT NULL REFERENCES bugs(id) ON DELETE CASCADE,
    fix_description TEXT NOT NULL,
    fix_type TEXT CHECK(fix_type IN ('hotfix', 'patch', 'minor', 'major', 'workaround')),
    files_changed TEXT,
    lines_added INTEGER DEFAULT 0,
    lines_removed INTEGER DEFAULT 0,
    fix_approach TEXT,
    rollback_plan TEXT,
    fix_committed_at TEXT,
    merged_at TEXT,
    deployed_at TEXT,
    verified_at TEXT,
    fix_success INTEGER DEFAULT 1,
    notes TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

-- bug_tests: Test cases cho bug fixes
CREATE TABLE IF NOT EXISTS bug_tests (
    id TEXT PRIMARY KEY,
    bug_id TEXT NOT NULL REFERENCES bugs(id) ON DELETE CASCADE,
    test_description TEXT NOT NULL,
    test_type TEXT CHECK(test_type IN ('unit', 'integration', 'e2e', 'manual', 'regression')),
    test_status TEXT CHECK(test_status IN ('pending', 'passed', 'failed', 'skipped')),
    test_code TEXT,
    test_result TEXT,
    regression_risk TEXT CHECK(regression_risk IN ('low', 'medium', 'high')),
    created_at TEXT DEFAULT (datetime('now')),
    executed_at TEXT
);

-- bug_related: Related bugs và similar bugs
CREATE TABLE IF NOT EXISTS bug_related (
    bug_id TEXT NOT NULL REFERENCES bugs(id) ON DELETE CASCADE,
    related_bug_id TEXT NOT NULL REFERENCES bugs(id) ON DELETE CASCADE,
    relationship TEXT CHECK(relationship IN ('duplicates', 'related', 'blocks', 'blocked-by', 'same-root-cause')),
    description TEXT,
    PRIMARY KEY (bug_id, related_bug_id)
);

-- bug_comments: Comments và notes
CREATE TABLE IF NOT EXISTS bug_comments (
    id TEXT PRIMARY KEY,
    bug_id TEXT NOT NULL REFERENCES bugs(id) ON DELETE CASCADE,
    comment TEXT NOT NULL,
    author TEXT NOT NULL,
    comment_type TEXT CHECK(comment_type IN ('note', 'update', 'question', 'answer')),
    created_at TEXT DEFAULT (datetime('now'))
);

-- bug_tags: Tags cho bugs
CREATE TABLE IF NOT EXISTS bug_tags (
    bug_id TEXT NOT NULL REFERENCES bugs(id) ON DELETE CASCADE,
    tag TEXT NOT NULL,
    PRIMARY KEY (bug_id, tag)
);

-- bug_patterns: Common bug patterns
CREATE TABLE IF NOT EXISTS bug_patterns (
    id TEXT PRIMARY KEY,
    pattern_name TEXT NOT NULL UNIQUE,
    pattern_description TEXT NOT NULL,
    pattern_category TEXT NOT NULL,
    occurrence_count INTEGER DEFAULT 1,
    severity TEXT CHECK(severity IN ('critical', 'high', 'medium', 'low')),
    prevention TEXT,
    last_occurrence TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

-- bug_pattern_bugs: Link bugs to patterns
CREATE TABLE IF NOT EXISTS bug_pattern_bugs (
    pattern_id TEXT NOT NULL REFERENCES bug_patterns(id) ON DELETE CASCADE,
    bug_id TEXT NOT NULL REFERENCES bugs(id) ON DELETE CASCADE,
    PRIMARY KEY (pattern_id, bug_id)
);

-- ============================================================
-- INDEXES
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_bugs_domain ON bugs(domain);
CREATE INDEX IF NOT EXISTS idx_bugs_status ON bugs(status);
CREATE INDEX IF NOT EXISTS idx_bugs_severity ON bugs(severity);
CREATE INDEX IF NOT EXISTS idx_bugs_priority ON bugs(priority);
CREATE INDEX IF NOT EXISTS idx_bugs_file ON bugs(file_path);
CREATE INDEX IF NOT EXISTS idx_bugs_first_observed ON bugs(first_observed);
CREATE INDEX IF NOT EXISTS idx_bug_root_causes_bug ON bug_root_causes(bug_id);
CREATE INDEX IF NOT EXISTS idx_bug_fixes_bug ON bug_fixes(bug_id);
CREATE INDEX IF NOT EXISTS idx_bug_tests_bug ON bug_tests(bug_id);

-- ============================================================
-- VIEWS
-- ============================================================

CREATE VIEW IF NOT EXISTS v_open_bugs AS
SELECT b.*, 
       rc.root_cause,
       f.fix_description,
       GROUP_CONCAT(DISTINCT bt.tag) as tags
FROM bugs b
LEFT JOIN bug_root_causes rc ON b.id = rc.bug_id
LEFT JOIN bug_fixes f ON b.id = f.bug_id AND f.fix_success = 1
LEFT JOIN bug_tags bt ON b.id = bt.bug_id
WHERE b.status NOT IN ('fixed', 'verified', 'closed', 'wontfix')
GROUP BY b.id
ORDER BY 
    CASE b.severity 
        WHEN 'critical' THEN 1 
        WHEN 'high' THEN 2 
        WHEN 'medium' THEN 3 
        ELSE 4 
    END,
    b.priority DESC;

CREATE VIEW IF NOT EXISTS v_bugs_by_domain AS
SELECT domain, COUNT(*) as total,
       SUM(CASE WHEN status = 'fixed' THEN 1 ELSE 0 END) as fixed,
       SUM(CASE WHEN status = 'open' THEN 1 ELSE 0 END) as open,
       SUM(CASE WHEN severity = 'critical' THEN 1 ELSE 0 END) as critical
FROM bugs
GROUP BY domain;

CREATE VIEW IF NOT EXISTS v_common_patterns AS
SELECT bp.*, COUNT(bpb.bug_id) as bug_count
FROM bug_patterns bp
JOIN bug_pattern_bugs bpb ON bp.id = bpb.pattern_id
GROUP BY bp.id
ORDER BY occurrence_count DESC;

-- ============================================================
-- TRIGGERS
-- ============================================================

CREATE TRIGGER IF NOT EXISTS trg_bugs_updated
AFTER UPDATE ON bugs
BEGIN
    UPDATE bugs SET updated_at = datetime('now') WHERE id = NEW.id;
END;
