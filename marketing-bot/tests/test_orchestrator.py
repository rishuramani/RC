"""Tests for the orchestrator (senior marketing agent)."""

import json
import pytest
from unittest.mock import MagicMock

from src.agents.orchestrator import Orchestrator
from src.db.models import ContentTask


SAMPLE_PLAN_RESPONSE = json.dumps([
    {
        "content_type": "linkedin_post",
        "platform": "linkedin",
        "topic": "Houston Q4 2025 occupancy hits 90.4%",
        "principal": "michael",
        "instructions": "Focus on the supply-demand dynamic and what it means for workforce housing investors."
    },
    {
        "content_type": "tweet",
        "platform": "twitter",
        "topic": "Supply pipeline at lowest since 2011",
        "principal": "bradley",
        "instructions": "Quick data drop with brief context."
    },
    {
        "content_type": "blog",
        "platform": "blog",
        "topic": "Why declining supply signals opportunity in workforce housing",
        "principal": None,
        "instructions": "Data-heavy piece using Q4 2025 metrics."
    },
])


class TestOrchestrator:

    @pytest.fixture
    def orchestrator(self, seeded_kb, mock_claude_response):
        claude = MagicMock()
        claude.generate.return_value = SAMPLE_PLAN_RESPONSE
        return Orchestrator(claude, seeded_kb)

    def test_has_all_sub_agents(self, orchestrator):
        assert "linkedin_post" in orchestrator.agents
        assert "tweet" in orchestrator.agents
        assert "tweet_thread" in orchestrator.agents
        assert "blog" in orchestrator.agents
        assert "market_report" in orchestrator.agents

    def test_plan_content_returns_tasks(self, orchestrator):
        tasks = orchestrator.plan_content(days_ahead=7)
        assert len(tasks) == 3
        assert tasks[0].content_type == "linkedin_post"
        assert tasks[0].topic == "Houston Q4 2025 occupancy hits 90.4%"
        assert tasks[1].content_type == "tweet"
        assert tasks[2].content_type == "blog"

    def test_plan_content_passes_instructions(self, orchestrator):
        tasks = orchestrator.plan_content(
            days_ahead=7,
            instructions="Focus on Phoenix market this week"
        )
        # Verify Claude was called with instructions in the prompt
        call_args = orchestrator.claude.generate.call_args
        assert "Phoenix" in call_args.kwargs.get("user_prompt", "") or \
               "Phoenix" in (call_args.args[1] if len(call_args.args) > 1 else "")

    def test_generate_content_delegates_to_linkedin(self, orchestrator):
        task = ContentTask(
            content_type="linkedin_post",
            platform="linkedin",
            topic="Houston market",
            principal="michael",
        )
        # Mock the LinkedIn agent's generate
        orchestrator.agents["linkedin_post"].claude.generate.return_value = \
            "Test LinkedIn post about Houston market."
        draft = orchestrator.generate_content(task)
        assert draft.content_type == "linkedin_post"

    def test_generate_content_unknown_type_raises(self, orchestrator):
        task = ContentTask(content_type="unknown", platform="test", topic="test")
        with pytest.raises(ValueError, match="Unknown content type"):
            orchestrator.generate_content(task)

    def test_validate_content(self, orchestrator):
        from src.db.models import ContentDraft
        draft = ContentDraft(
            content_type="linkedin_post",
            platform="linkedin",
            body="Houston workforce housing is showing resilience.",
            topic="market",
        )
        result = orchestrator.validate_content(draft)
        assert result["is_compliant"] is True

    def test_validate_content_unknown_type_raises(self, orchestrator):
        from src.db.models import ContentDraft
        draft = ContentDraft(
            content_type="unknown",
            platform="test",
            body="test",
            topic="test",
        )
        with pytest.raises(ValueError):
            orchestrator.validate_content(draft)

    def test_suggest_topics(self, orchestrator):
        suggestions = orchestrator.suggest_topics()
        assert len(suggestions) > 0
        assert all("topic" in s for s in suggestions)
        assert all("reason" in s for s in suggestions)

    def test_cross_promote_blog(self, orchestrator):
        kb = orchestrator.kb
        cid = kb.add_content(
            "blog", "blog",
            "<h1>Test Article</h1><p>Content about Houston market...</p>",
            title="Test Article",
            topic="market_analysis",
            principal="michael",
        )
        tasks = orchestrator.cross_promote(cid)
        assert len(tasks) == 2
        types = {t.content_type for t in tasks}
        assert "linkedin_post" in types
        assert "tweet_thread" in types

    def test_cross_promote_linkedin(self, orchestrator):
        kb = orchestrator.kb
        cid = kb.add_content(
            "linkedin_post", "linkedin",
            "Houston absorption data shows strong demand...",
            topic="market_analysis",
            principal="michael",
        )
        tasks = orchestrator.cross_promote(cid)
        assert len(tasks) == 1
        assert tasks[0].content_type == "tweet"

    def test_cross_promote_nonexistent_raises(self, orchestrator):
        with pytest.raises(ValueError, match="not found"):
            orchestrator.cross_promote(9999)

    def test_review_calendar(self, orchestrator):
        kb = orchestrator.kb
        kb.add_calendar_entry("linkedin_post", "linkedin", "2026-02-16",
                              topic="test")
        status = orchestrator.review_calendar()
        assert "total_pending" in status
        assert "upcoming_7_days" in status
        assert "overdue" in status

    def test_parse_plan_invalid_json(self, orchestrator):
        tasks = orchestrator._parse_plan("This is not JSON at all")
        assert tasks == []

    def test_parse_plan_no_array(self, orchestrator):
        tasks = orchestrator._parse_plan('{"key": "value"}')
        assert tasks == []
