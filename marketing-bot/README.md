# RC Marketing Bot

An AI-powered marketing content engine built for RC Investment Properties. The system uses Claude (Anthropic) to generate brand-consistent content across LinkedIn, Twitter/X, the firm's blog, and investor market reports — all orchestrated by a senior marketing agent that plans, delegates, and coordinates content creation.

## Why This Exists

RC Investment Properties is a boutique multifamily real estate investment firm led by Michael Rosen and Bradley Couch. The firm needs a consistent content presence to position both principals as thought leaders in workforce housing investment. Manually writing LinkedIn posts, tweets, blog articles, and market reports is time-consuming and hard to keep consistent. This bot automates the content creation process while keeping Michael and Bradley in full control of what gets published.

---

## How It Works

### The Agent System

The bot is built around a **multi-agent architecture** where a senior orchestrator delegates work to specialized content agents. Every agent shares the same brand voice, compliance rules, and knowledge base — but each is tuned for its specific platform.

```
                    ┌──────────────────────┐
                    │     Orchestrator      │
                    │ (Senior Marketing     │
                    │  Strategist)          │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │                │
    ┌─────────▼──┐   ┌────────▼───┐   ┌───────▼────┐   ┌──────▼───────┐
    │  LinkedIn   │   │  Twitter   │   │    Blog    │   │   Market     │
    │   Agent     │   │   Agent    │   │   Agent    │   │   Report     │
    │             │   │            │   │            │   │   Agent      │
    └─────────────┘   └────────────┘   └────────────┘   └──────────────┘
```

**All agents share:**
- The same Claude API connection
- The same persistent knowledge base (firm data, market metrics, brand rules)
- The same brand voice definition and compliance checker

### The Orchestrator (Senior Marketing Agent)

The orchestrator is the brain of the system. It does not generate content itself — it plans, delegates, and coordinates.

**What it does:**

1. **Plans content calendars** — Looks at the content calendar, recent market data, and what's already been posted to decide what should be created next. It calls Claude with full context about the firm's state and gets back a structured plan (JSON) of content to produce.

2. **Delegates to sub-agents** — Each planned piece gets assigned to the right agent. A LinkedIn post goes to the LinkedIn Agent, a tweet to the Twitter Agent, etc. The orchestrator constructs a `ContentTask` with the topic, target principal, platform, and any special instructions.

3. **Suggests topics** — Scans the knowledge base for fresh market data that hasn't been turned into content yet. If Houston occupancy data was added but no post about it exists, it surfaces that as a suggestion.

4. **Cross-promotes content** — When a blog article is published, the orchestrator can automatically create tasks to promote it on LinkedIn (summary post) and Twitter (thread breakdown). A LinkedIn post can be condensed into a tweet.

5. **Reviews the calendar** — Shows what's coming up, what's overdue, and what's been published.

### The LinkedIn Agent

Generates posts optimized for LinkedIn's feed algorithm. Every post follows a proven structure:

- **Hook** (first 2 lines) — the most important part; this is what shows before "see more"
- **Value** (body) — short paragraphs with data-backed insights, line breaks for readability
- **Takeaway** — a clear conclusion or insight (never a sales pitch)
- **Hashtags** — 3-5 relevant hashtags at the end

**Post types it can generate:**
- Data Commentary — lead with a specific metric, then contextualize it
- Market Insight — share a non-obvious observation about market dynamics
- Operational Lesson — share a real lesson from managing properties
- Thought Leadership — articulate a nuanced view on the industry

Posts are written in first person ("I" / "we") since they go on Michael's or Bradley's personal profiles, not a company page. Max 3,000 characters.

### The Twitter/X Agent

Generates two formats:

**Single tweets** (max 280 characters):
- Lead with the data point or insight
- Plain language, minimal hashtags
- Designed to be quotable and shareable

**Threads** (3-7 numbered tweets):
- Hook tweet that stands alone
- Each tweet numbered (1/, 2/, etc.)
- Each tweet makes sense independently
- Final tweet summarizes the takeaway

**Post types:** Data drops, thread breakdowns, quick takes on news, contrarian views backed by data.

### The Blog Agent

Generates long-form articles (800-1200 words) in HTML format that matches the existing RC website blog template.

**Article structure:**
1. Title (H1) — clear, specific, SEO-friendly
2. Meta description — 150-160 characters
3. Introduction — 1-2 paragraphs setting context and thesis
4. Body — 3-5 sections with H2 headers, data-backed analysis
5. Conclusion — key takeaway and forward-looking statement
6. Disclaimer — standard market analysis disclaimer

Every claim is supported by data with source citations. Written for sophisticated investors, not the general public.

### The Market Report Agent

Generates structured market analysis reports in Markdown format for investor distribution.

**Report structure:**
1. Executive Summary — 3-5 bullet point takeaways
2. Market Overview — high-level conditions with key metrics
3. Supply & Demand — pipeline, absorption, construction activity
4. Rent & Occupancy Trends — by submarket and class
5. Investment Sales Activity — cap rates, pricing, transaction volume
6. Outlook & Investment Implications — what it means for RC's strategy
7. Disclaimer

Reports pull heavily from the market data table and compare current period to prior period where possible. 600-1000 words.

---

## The Knowledge Base

The persistent knowledge base is an SQLite database that stores everything the agents need to generate accurate, on-brand content. It's the single source of truth.

### What's stored:

| Table | Purpose | Example |
|-------|---------|---------|
| **firm_facts** | Track record, portfolio, thesis, advantages, terms | "Meta Street exit: 43.4% value increase" |
| **market_data** | Houston/Phoenix metrics by period and source | "Houston Q4 2025 occupancy: 90.4% (CoStar)" |
| **brand_rules** | Terminology rules, tone guidelines, compliance requirements | "Use 'workforce housing' not 'affordable housing'" |
| **content** | Every piece of generated content with status tracking | LinkedIn post, status=queued, principal=michael |
| **content_metrics** | Engagement data (impressions, likes, comments, shares) | Post #42: 1,500 impressions, 45 likes |
| **content_calendar** | Scheduled content with dates and assignments | Feb 17: LinkedIn post for Michael (planned) |
| **data_sources** | External data providers and their update frequency | CoStar Houston Report, quarterly |

### How agents use it:

When any agent receives a task (e.g., "write a LinkedIn post about Houston absorption"), it:

1. Queries the knowledge base for relevant firm facts, market data, and brand rules matching the topic
2. Pulls recent content on similar topics (to avoid repetition)
3. Injects all of this as context into the Claude API prompt
4. Generates content grounded in real, firm-specific data

This means the agents never hallucinate market data — they use what's in the KB.

### Pre-seeded data:

The KB comes pre-loaded with:
- **42 firm facts** — track record (7), portfolio (12), thesis (9), advantages (6), terms (8)
- **14 market data points** — Houston Q4 2025 and 2024 metrics from CoStar, Census, BLS
- **25 brand rules** — terminology (7), tone (4), compliance (6), terms to avoid (8)
- **6 data sources** — BLS, CoStar, Census, TWC, GHP, Federal Reserve
- **8 calendar entries** — 4 weeks of planned LinkedIn, Twitter, blog, and report content

---

## Brand Compliance System

Every piece of content is automatically validated before it enters the review queue. The compliance checker runs two types of checks:

### Forbidden Term Detection

The system scans for 11 forbidden terms that violate RC's brand positioning:

| Forbidden | Use Instead |
|-----------|-------------|
| "affordable housing" | "workforce housing" |
| "flipping" / "flip" | "value creation" / "repositioning" |
| "guaranteed returns" / "guaranteed" | "target returns" |
| "risk-free" | "downside protection" |
| "passive income" | "cash flow" / "distributions" |
| "get rich" / "wealth building" | (don't use) |
| "deal of a lifetime" | (don't use) |

If any forbidden term is detected, the content is flagged as non-compliant and saved with status `draft` instead of `queued`. It still goes to the review queue but is marked with compliance issues.

### Disclaimer Enforcement

- **Track record mentions** — If the content references the firm's track record, historical performance, or specific return numbers (43.4%, 19.7%, etc.), a past performance disclaimer is required: *"Past performance is not indicative of future results."*
- **Market analysis** — Blog articles and market reports get a suggestion to include: *"For informational purposes only. This does not constitute investment advice."*

---

## The Content Pipeline

Content flows through a strict lifecycle:

```
  Generate ──→ Validate ──→ Queue ──→ Review ──→ Approve ──→ Publish ──→ Track
                  │                      │           │
                  │                      │           └──→ Reject ──→ Edit ──→ Re-queue
                  │                      │
                  └── Non-compliant?     └── Michael or Bradley
                      Save as "draft"        reviews via CLI
                      (flagged)
```

**Step by step:**

1. **Generate** — The orchestrator delegates to a sub-agent. The agent pulls KB context, calls Claude with a layered prompt (brand voice + agent role + task context), and returns a `ContentDraft`.

2. **Validate** — The draft is run through the brand compliance checker. Forbidden terms? Missing disclaimers? It catches them.

3. **Queue** — Compliant content gets status `queued`. Non-compliant content gets status `draft` with issues flagged.

4. **Review** — Michael or Bradley run `rc-bot review` to see all pending content. Each item shows its compliance status. They can view the full content with `rc-bot review <id>`.

5. **Approve / Reject** — The principal approves (`rc-bot approve <id>`) or rejects (`rc-bot reject <id> --reason "..."`) each piece. Rejected content can be edited and requeued.

6. **Publish** — Approved content is posted via the LinkedIn or Twitter API. The platform post ID is stored in the database. A `--dry-run` flag lets you preview without actually posting.

7. **Track** — Engagement metrics (impressions, likes, comments, shares, clicks) can be fetched and stored for strategy adjustment.

---

## The Prompt Architecture

Each agent's prompt is built from three layers:

### Layer 1: Brand Foundation (shared by all agents)
The complete brand voice definition including:
- Company identity and positioning
- Tone and style rules
- Required and forbidden terminology
- Compliance rules
- Core messaging themes

### Layer 2: Agent Role (specific to each agent)
The agent's specific responsibilities, output format, content types, and platform-specific rules. For example, the Twitter Agent knows about the 280-character limit and thread numbering format, while the Blog Agent knows about HTML structure and 800-1200 word targets.

### Layer 3: Task Context (dynamic, per-task)
For each content generation task, the system injects:
- Relevant firm facts from the KB
- Market data matching the topic
- All brand rules
- Recently created content on similar topics (to avoid repetition)

This layered approach means the agents always write on-brand, always have access to real data, and never repeat themselves.

---

## CLI Reference

The bot is controlled through the `rc-bot` command-line tool.

### Content Generation
```bash
rc-bot generate linkedin --topic "Houston Q4 absorption data" --principal michael
rc-bot generate tweet --topic "Supply pipeline at lowest since 2011" --principal bradley
rc-bot generate thread --topic "Houston workforce housing market update"
rc-bot generate blog --topic "Why declining supply signals opportunity"
rc-bot generate report --topic "houston - Q4 2025"
```

### Orchestrator Planning
```bash
rc-bot plan --days 7                    # Auto-plan next 7 days
rc-bot plan --days 14 -i "Focus on Phoenix this week"
rc-bot suggest                          # Topic suggestions from fresh data
```

### Review & Approval
```bash
rc-bot review                           # List all pending content
rc-bot review 42                        # View full content for item #42
rc-bot approve 42                       # Approve for publishing
rc-bot reject 42 --reason "Too promotional"
```

### Publishing
```bash
rc-bot publish 42 --dry-run             # Preview publish payload
rc-bot publish 42 --mock                # Publish via mock APIs (testing)
rc-bot publish 42                       # Publish to real platform
```

### Knowledge Base Management
```bash
rc-bot kb seed                          # Seed KB from source files
rc-bot kb stats                         # View KB statistics
rc-bot kb search "houston rent growth"  # Search across all tables
rc-bot kb add-market --market houston --metric occupancy --value "91.0%" --period "Q1 2026"
```

### Calendar & Metrics
```bash
rc-bot calendar                         # View upcoming schedule
rc-bot metrics                          # Content performance summary
rc-bot metrics 42                       # Metrics for specific post
```

---

## Setup

```bash
cd marketing-bot

# Create virtual environment and install
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Configure API keys
cp .env.example .env
# Edit .env — add your ANTHROPIC_API_KEY at minimum

# Seed the knowledge base
rc-bot kb seed
```

### Required API Keys

| Key | Required For | How to Get |
|-----|-------------|------------|
| `ANTHROPIC_API_KEY` | All content generation | [console.anthropic.com](https://console.anthropic.com) |
| `LINKEDIN_ACCESS_TOKEN` | Publishing to LinkedIn | LinkedIn Developer Portal, OAuth 2.0 |
| `TWITTER_BEARER_TOKEN` | Publishing to Twitter/X | Twitter Developer Portal, OAuth 2.0 |

LinkedIn and Twitter keys are only needed for actual publishing. You can generate and review content with just the Anthropic key.

---

## Testing

```bash
# Run all 176 tests
pytest tests/ -v

# Run with coverage (86% coverage)
coverage run -m pytest tests/ && coverage report

# Run specific test categories
pytest tests/test_database.py -v          # 47 database CRUD tests
pytest tests/test_brand_compliance.py -v  # 16 brand compliance tests
pytest tests/test_pipeline.py -v          # 15 pipeline workflow tests
pytest tests/test_cli.py -v              # 21 CLI command tests
pytest tests/test_linkedin_agent.py -v    # 9 LinkedIn agent tests
pytest tests/test_twitter_agent.py -v     # 7 Twitter agent tests
pytest tests/test_blog_agent.py -v        # 7 blog agent tests
pytest tests/test_orchestrator.py -v      # 14 orchestrator tests
pytest tests/test_publisher.py -v         # 14 publisher/API tests
pytest tests/test_market_report.py -v     # 6 market report tests
pytest tests/test_data_ingestion.py -v    # 7 data ingestion tests
```

All tests use mocked Claude API responses and in-memory SQLite databases — no API keys or network access needed to run the test suite.

---

## Project Structure

```
marketing-bot/
├── pyproject.toml                     # Dependencies and project config
├── .env.example                       # API key template
├── README.md                          # This file
│
├── src/
│   ├── config.py                      # Environment variables and settings
│   ├── cli.py                         # Click-based CLI (rc-bot command)
│   │
│   ├── db/
│   │   ├── database.py                # SQLite connection manager
│   │   ├── schema.sql                 # 7 tables with indexes
│   │   ├── models.py                  # Dataclasses (FirmFact, Content, etc.)
│   │   └── knowledge_base.py          # Full CRUD for all tables + search
│   │
│   ├── agents/
│   │   ├── base_agent.py              # Abstract base: generate, validate, context
│   │   ├── orchestrator.py            # Plans, delegates, coordinates, cross-promotes
│   │   ├── linkedin_agent.py          # Hook → value → CTA post format
│   │   ├── twitter_agent.py           # Tweets (280 char) and threads (numbered)
│   │   ├── blog_agent.py              # 800-1200 word HTML articles
│   │   └── market_report_agent.py     # Structured markdown reports
│   │
│   ├── prompts/
│   │   ├── brand_voice.py             # Full brand definition + forbidden terms
│   │   ├── system_prompts.py          # Layered prompts for each agent
│   │   └── templates.py               # User prompt builders with KB context
│   │
│   ├── pipeline/
│   │   ├── content_pipeline.py        # Generate → queue → approve → publish
│   │   ├── publisher.py               # Routes content to platform APIs
│   │   └── data_ingestion.py          # Parse HTML/markdown into KB
│   │
│   └── integrations/
│       ├── claude_client.py            # Anthropic SDK wrapper with retry + tracking
│       ├── linkedin_api.py             # LinkedIn API v2 (OAuth 2.0, mock mode)
│       └── twitter_api.py              # Twitter API v2 (OAuth 2.0, mock mode)
│
├── seeds/
│   ├── seed_knowledge_base.py          # Populates KB from JSON files
│   ├── firm_data.json                  # 42 firm facts (track record, portfolio, etc.)
│   ├── brand_guidelines.json           # 25 brand rules (terminology, compliance)
│   └── market_data.json                # 14 market data points + 6 data sources
│
├── data/
│   └── rc_marketing.db                 # SQLite database (created on first run)
│
└── tests/                              # 176 tests, 86% coverage
    ├── conftest.py                     # Fixtures: test DB, seeded KB, mock Claude
    ├── test_database.py                # CRUD for all 7 tables
    ├── test_linkedin_agent.py          # Generation, hashtags, prompts, validation
    ├── test_twitter_agent.py           # Tweets, threads, parsing, validation
    ├── test_blog_agent.py              # HTML output, title/meta extraction, word count
    ├── test_market_report.py           # Markdown output, title extraction, prompts
    ├── test_orchestrator.py            # Planning, delegation, cross-promotion, calendar
    ├── test_brand_compliance.py        # All 11 forbidden terms, disclaimers, edge cases
    ├── test_pipeline.py                # Full lifecycle: generate → approve → publish
    ├── test_publisher.py               # Mock LinkedIn/Twitter APIs
    ├── test_data_ingestion.py          # HTML/markdown parsing, KB population
    └── test_cli.py                     # All CLI commands via Click test runner
```

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.11+ |
| LLM | Claude (Anthropic API) via `anthropic` SDK |
| CLI | Click + Rich (tables, panels, formatting) |
| Database | SQLite (file-based, no server needed) |
| HTTP | Requests (LinkedIn/Twitter APIs) |
| HTML Parsing | BeautifulSoup4 (KB seeding from website) |
| Testing | pytest + pytest-mock + coverage |
| Config | python-dotenv (.env files) |
