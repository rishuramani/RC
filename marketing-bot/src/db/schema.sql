-- RC Marketing Bot - Knowledge Base Schema

CREATE TABLE IF NOT EXISTS firm_facts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    key TEXT NOT NULL,
    value TEXT NOT NULL,
    source TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS market_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    market TEXT NOT NULL,
    metric TEXT NOT NULL,
    value TEXT NOT NULL,
    period TEXT,
    source TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS brand_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_type TEXT NOT NULL,
    rule TEXT NOT NULL,
    example TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS content (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content_type TEXT NOT NULL,
    platform TEXT NOT NULL,
    principal TEXT,
    title TEXT,
    body TEXT NOT NULL,
    topic TEXT,
    status TEXT DEFAULT 'draft',
    scheduled_for TIMESTAMP,
    published_at TIMESTAMP,
    platform_post_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS content_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content_id INTEGER NOT NULL REFERENCES content(id),
    impressions INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    clicks INTEGER DEFAULT 0,
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS content_calendar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content_type TEXT NOT NULL,
    platform TEXT NOT NULL,
    topic TEXT,
    principal TEXT,
    scheduled_date DATE NOT NULL,
    status TEXT DEFAULT 'planned',
    content_id INTEGER REFERENCES content(id),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS data_sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    url TEXT,
    frequency TEXT,
    last_checked TIMESTAMP,
    next_check TIMESTAMP,
    notes TEXT
);

-- Scanned external content from Twitter/LinkedIn
CREATE TABLE IF NOT EXISTS scanned_content (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    platform TEXT NOT NULL,
    external_id TEXT,
    author TEXT,
    author_url TEXT,
    body TEXT NOT NULL,
    url TEXT,
    engagement_score INTEGER DEFAULT 0,
    topic_tags TEXT,
    scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    digest_id INTEGER REFERENCES digests(id)
);

-- Digests (batched scanner runs)
CREATE TABLE IF NOT EXISTS digests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    summary TEXT,
    scan_type TEXT DEFAULT 'scheduled',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inspiration (liked content + pasted URLs)
CREATE TABLE IF NOT EXISTS inspiration (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_type TEXT NOT NULL,
    scanned_content_id INTEGER REFERENCES scanned_content(id),
    url TEXT,
    body TEXT,
    author TEXT,
    notes TEXT,
    liked_by TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Monitored accounts
CREATE TABLE IF NOT EXISTS monitored_accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    platform TEXT NOT NULL,
    handle TEXT NOT NULL,
    name TEXT,
    category TEXT,
    active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_firm_facts_category ON firm_facts(category);
CREATE INDEX IF NOT EXISTS idx_market_data_market ON market_data(market);
CREATE INDEX IF NOT EXISTS idx_market_data_metric ON market_data(metric);
CREATE INDEX IF NOT EXISTS idx_brand_rules_type ON brand_rules(rule_type);
CREATE INDEX IF NOT EXISTS idx_content_status ON content(status);
CREATE INDEX IF NOT EXISTS idx_content_platform ON content(platform);
CREATE INDEX IF NOT EXISTS idx_content_type ON content(content_type);
CREATE INDEX IF NOT EXISTS idx_content_calendar_date ON content_calendar(scheduled_date);
CREATE INDEX IF NOT EXISTS idx_content_metrics_content ON content_metrics(content_id);
CREATE INDEX IF NOT EXISTS idx_scanned_platform ON scanned_content(platform);
CREATE INDEX IF NOT EXISTS idx_scanned_digest ON scanned_content(digest_id);
CREATE INDEX IF NOT EXISTS idx_inspiration_source ON inspiration(source_type);
CREATE INDEX IF NOT EXISTS idx_monitored_platform ON monitored_accounts(platform);
