"""Tests for database layer and knowledge base CRUD operations."""

import pytest
from src.db.database import Database
from src.db.knowledge_base import KnowledgeBase
from src.db.models import FirmFact, MarketData, BrandRule, Content


class TestDatabase:
    """Test the Database connection manager."""

    def test_connect_memory(self, db):
        conn = db.connect()
        assert conn is not None

    def test_initialize_creates_tables(self, db):
        tables = db.fetchall(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        table_names = [t["name"] for t in tables]
        assert "firm_facts" in table_names
        assert "market_data" in table_names
        assert "brand_rules" in table_names
        assert "content" in table_names
        assert "content_metrics" in table_names
        assert "content_calendar" in table_names
        assert "data_sources" in table_names

    def test_transaction_commit(self, db):
        with db.transaction():
            db.execute(
                "INSERT INTO firm_facts (category, key, value) VALUES (?, ?, ?)",
                ("test", "k", "v"),
            )
        row = db.fetchone("SELECT * FROM firm_facts WHERE key = 'k'")
        assert row is not None
        assert row["value"] == "v"

    def test_transaction_rollback(self, db):
        with pytest.raises(ValueError):
            with db.transaction():
                db.execute(
                    "INSERT INTO firm_facts (category, key, value) "
                    "VALUES (?, ?, ?)",
                    ("test", "rollback_key", "v"),
                )
                raise ValueError("force rollback")
        row = db.fetchone("SELECT * FROM firm_facts WHERE key = 'rollback_key'")
        assert row is None

    def test_double_initialize_is_safe(self, db):
        db.initialize()  # second call should not error
        tables = db.fetchall(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
        assert len(tables) > 0


class TestFirmFacts:
    """Test firm_facts CRUD."""

    def test_add_and_get(self, kb):
        fid = kb.add_firm_fact("track_record", "irr", "43%", "deck")
        fact = kb.get_firm_fact(fid)
        assert fact is not None
        assert fact.category == "track_record"
        assert fact.key == "irr"
        assert fact.value == "43%"
        assert fact.source == "deck"

    def test_get_nonexistent(self, kb):
        assert kb.get_firm_fact(9999) is None

    def test_get_by_category(self, seeded_kb):
        facts = seeded_kb.get_firm_facts_by_category("track_record")
        assert len(facts) == 2
        keys = [f.key for f in facts]
        assert "meta_street_return" in keys
        assert "meta_street_hold" in keys

    def test_search(self, seeded_kb):
        results = seeded_kb.search_firm_facts("meta_street")
        assert len(results) >= 2

    def test_search_by_value(self, seeded_kb):
        results = seeded_kb.search_firm_facts("43.4%")
        assert len(results) >= 1

    def test_update(self, kb):
        fid = kb.add_firm_fact("portfolio", "units", "100")
        kb.update_firm_fact(fid, value="143")
        fact = kb.get_firm_fact(fid)
        assert fact.value == "143"

    def test_update_no_args(self, kb):
        fid = kb.add_firm_fact("portfolio", "units", "100")
        assert kb.update_firm_fact(fid) is False

    def test_delete(self, kb):
        fid = kb.add_firm_fact("test", "key", "val")
        kb.delete_firm_fact(fid)
        assert kb.get_firm_fact(fid) is None


class TestMarketData:
    """Test market_data CRUD."""

    def test_add_and_get(self, kb):
        mid = kb.add_market_data("houston", "occupancy", "90.4%", "Q4 2025",
                                 "CoStar")
        data = kb.get_market_data(mid)
        assert data.market == "houston"
        assert data.metric == "occupancy"
        assert data.value == "90.4%"
        assert data.period == "Q4 2025"

    def test_get_by_market(self, seeded_kb):
        results = seeded_kb.get_market_data_by_market("houston")
        assert len(results) >= 5

    def test_get_by_metric(self, seeded_kb):
        results = seeded_kb.get_market_data_by_metric("occupancy")
        assert len(results) >= 1
        assert results[0].value == "90.4%"

    def test_get_by_metric_and_market(self, seeded_kb):
        results = seeded_kb.get_market_data_by_metric("occupancy", "houston")
        assert len(results) == 1

    def test_search(self, seeded_kb):
        results = seeded_kb.search_market_data("rent")
        assert len(results) >= 1

    def test_delete(self, kb):
        mid = kb.add_market_data("houston", "test", "val")
        kb.delete_market_data(mid)
        assert kb.get_market_data(mid) is None


class TestBrandRules:
    """Test brand_rules CRUD."""

    def test_add_and_get(self, kb):
        rid = kb.add_brand_rule("terminology", "Use 'workforce housing'",
                                "The workforce housing segment...")
        rule = kb.get_brand_rule(rid)
        assert rule.rule_type == "terminology"
        assert "workforce housing" in rule.rule

    def test_get_by_type(self, seeded_kb):
        rules = seeded_kb.get_brand_rules_by_type("compliance")
        assert len(rules) == 2

    def test_get_all(self, seeded_kb):
        rules = seeded_kb.get_all_brand_rules()
        assert len(rules) == 7

    def test_delete(self, kb):
        rid = kb.add_brand_rule("test", "test rule")
        kb.delete_brand_rule(rid)
        assert kb.get_brand_rule(rid) is None


class TestContent:
    """Test content CRUD."""

    def test_add_and_get(self, kb):
        cid = kb.add_content("linkedin_post", "linkedin",
                             "Test post about Houston",
                             principal="michael", topic="market_analysis")
        content = kb.get_content(cid)
        assert content.content_type == "linkedin_post"
        assert content.platform == "linkedin"
        assert content.status == "draft"
        assert content.principal == "michael"

    def test_get_by_status(self, kb, sample_content):
        drafts = kb.get_content_by_status("draft")
        assert len(drafts) == 1
        queued = kb.get_content_by_status("queued")
        assert len(queued) == 1

    def test_get_by_platform(self, kb, sample_content):
        linkedin = kb.get_content_by_platform("linkedin")
        assert len(linkedin) == 1
        twitter = kb.get_content_by_platform("twitter")
        assert len(twitter) == 1

    def test_get_recent(self, kb, sample_content):
        recent = kb.get_recent_content(limit=2)
        assert len(recent) == 2

    def test_update_status(self, kb):
        cid = kb.add_content("tweet", "twitter", "Test tweet")
        kb.update_content_status(cid, "queued")
        content = kb.get_content(cid)
        assert content.status == "queued"

    def test_update_status_published(self, kb):
        cid = kb.add_content("tweet", "twitter", "Test tweet")
        kb.update_content_status(cid, "published")
        content = kb.get_content(cid)
        assert content.status == "published"
        assert content.published_at is not None

    def test_update_body(self, kb):
        cid = kb.add_content("tweet", "twitter", "Original body")
        kb.update_content_body(cid, "Updated body", title="New title")
        content = kb.get_content(cid)
        assert content.body == "Updated body"
        assert content.title == "New title"

    def test_set_platform_post_id(self, kb):
        cid = kb.add_content("tweet", "twitter", "Test")
        kb.set_platform_post_id(cid, "twitter_12345")
        content = kb.get_content(cid)
        assert content.platform_post_id == "twitter_12345"

    def test_search(self, kb, sample_content):
        results = kb.search_content("Houston")
        assert len(results) >= 1

    def test_delete_with_metrics(self, kb):
        cid = kb.add_content("tweet", "twitter", "Test")
        kb.add_content_metrics(cid, impressions=100)
        kb.delete_content(cid)
        assert kb.get_content(cid) is None
        assert kb.get_content_metrics(cid) == []


class TestContentMetrics:
    """Test content_metrics CRUD."""

    def test_add_and_get(self, kb):
        cid = kb.add_content("tweet", "twitter", "Test")
        mid = kb.add_content_metrics(cid, impressions=500, likes=25,
                                     comments=3, shares=10, clicks=50)
        metrics = kb.get_content_metrics(cid)
        assert len(metrics) == 1
        assert metrics[0].impressions == 500
        assert metrics[0].likes == 25

    def test_get_latest(self, kb):
        cid = kb.add_content("tweet", "twitter", "Test")
        kb.add_content_metrics(cid, impressions=100)
        kb.add_content_metrics(cid, impressions=200)
        latest = kb.get_latest_metrics(cid)
        assert latest.impressions == 200

    def test_no_metrics(self, kb):
        cid = kb.add_content("tweet", "twitter", "Test")
        assert kb.get_latest_metrics(cid) is None


class TestContentCalendar:
    """Test content_calendar CRUD."""

    def test_add_and_get(self, kb):
        eid = kb.add_calendar_entry("linkedin_post", "linkedin", "2026-02-20",
                                    topic="market_analysis", principal="michael")
        entry = kb.get_calendar_entry(eid)
        assert entry.content_type == "linkedin_post"
        assert entry.scheduled_date == "2026-02-20"
        assert entry.status == "planned"

    def test_get_by_date_range(self, kb):
        kb.add_calendar_entry("linkedin_post", "linkedin", "2026-02-18")
        kb.add_calendar_entry("tweet", "twitter", "2026-02-20")
        kb.add_calendar_entry("blog", "blog", "2026-02-25")

        entries = kb.get_calendar_entries_by_date_range("2026-02-17", "2026-02-21")
        assert len(entries) == 2

    def test_get_pending(self, kb):
        kb.add_calendar_entry("linkedin_post", "linkedin", "2026-02-18")
        kb.add_calendar_entry("tweet", "twitter", "2026-02-20")
        pending = kb.get_pending_calendar_entries()
        assert len(pending) == 2

    def test_update_status(self, kb):
        eid = kb.add_calendar_entry("tweet", "twitter", "2026-02-20")
        cid = kb.add_content("tweet", "twitter", "Generated tweet")
        kb.update_calendar_entry_status(eid, "generated", content_id=cid)
        entry = kb.get_calendar_entry(eid)
        assert entry.status == "generated"
        assert entry.content_id == cid

    def test_delete(self, kb):
        eid = kb.add_calendar_entry("tweet", "twitter", "2026-02-20")
        kb.delete_calendar_entry(eid)
        assert kb.get_calendar_entry(eid) is None


class TestDataSources:
    """Test data_sources CRUD."""

    def test_add_and_get(self, kb):
        sid = kb.add_data_source("BLS Employment", "https://bls.gov",
                                 "monthly", "Key employment data")
        source = kb.get_data_source(sid)
        assert source.name == "BLS Employment"
        assert source.frequency == "monthly"

    def test_get_all(self, seeded_kb):
        sources = seeded_kb.get_all_data_sources()
        assert len(sources) == 3

    def test_update_checked(self, kb):
        sid = kb.add_data_source("Test Source")
        kb.update_data_source_checked(sid, next_check="2026-03-01")
        source = kb.get_data_source(sid)
        assert source.last_checked is not None
        assert source.next_check == "2026-03-01"

    def test_delete(self, kb):
        sid = kb.add_data_source("Test Source")
        kb.delete_data_source(sid)
        assert kb.get_data_source(sid) is None


class TestAggregateQueries:
    """Test aggregate knowledge base operations."""

    def test_get_context_for_topic(self, seeded_kb):
        context = seeded_kb.get_context_for_topic("houston")
        assert "firm_facts" in context
        assert "market_data" in context
        assert "brand_rules" in context
        assert len(context["market_data"]) > 0

    def test_get_content_stats(self, kb, sample_content):
        stats = kb.get_content_stats()
        assert stats["total"] == 3
        assert "draft" in stats["by_status"]
        assert "linkedin" in stats["by_platform"]
