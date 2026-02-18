"""Tests for the content pipeline (generate → queue → approve → publish)."""

import pytest
from unittest.mock import MagicMock, patch

from src.pipeline.content_pipeline import ContentPipeline
from src.db.models import ContentTask


@pytest.fixture
def pipeline(seeded_kb):
    claude = MagicMock()
    claude.generate.return_value = "Houston's workforce housing market shows strength."
    return ContentPipeline(claude, seeded_kb)


class TestGenerateAndQueue:

    def test_generates_and_saves_content(self, pipeline):
        task = ContentTask(
            content_type="linkedin_post",
            platform="linkedin",
            topic="Houston market",
            principal="michael",
        )
        content_id = pipeline.generate_and_queue(task)
        assert content_id > 0

        content = pipeline.kb.get_content(content_id)
        assert content is not None
        assert content.content_type == "linkedin_post"
        assert content.platform == "linkedin"
        assert content.principal == "michael"

    def test_compliant_content_is_queued(self, pipeline):
        task = ContentTask(
            content_type="linkedin_post",
            platform="linkedin",
            topic="Houston market",
            principal="michael",
        )
        content_id = pipeline.generate_and_queue(task)
        content = pipeline.kb.get_content(content_id)
        assert content.status == "queued"

    def test_noncompliant_content_stays_draft(self, pipeline):
        pipeline.orchestrator.claude.generate.return_value = \
            "We guarantee returns by flipping affordable housing!"
        task = ContentTask(
            content_type="linkedin_post",
            platform="linkedin",
            topic="Houston market",
            principal="michael",
        )
        content_id = pipeline.generate_and_queue(task)
        content = pipeline.kb.get_content(content_id)
        assert content.status == "draft"

    def test_updates_calendar_entry(self, pipeline):
        eid = pipeline.kb.add_calendar_entry(
            "linkedin_post", "linkedin", "2026-02-20", topic="Houston market"
        )
        task = ContentTask(
            content_type="linkedin_post",
            platform="linkedin",
            topic="Houston market",
            calendar_entry_id=eid,
        )
        content_id = pipeline.generate_and_queue(task)
        entry = pipeline.kb.get_calendar_entry(eid)
        assert entry.status == "generated"
        assert entry.content_id == content_id


class TestApproveReject:

    def test_approve_queued_content(self, pipeline):
        cid = pipeline.kb.add_content(
            "tweet", "twitter", "Test tweet", status="queued"
        )
        result = pipeline.approve(cid)
        assert result is True
        content = pipeline.kb.get_content(cid)
        assert content.status == "approved"

    def test_approve_draft_content(self, pipeline):
        cid = pipeline.kb.add_content(
            "tweet", "twitter", "Test tweet", status="draft"
        )
        result = pipeline.approve(cid)
        assert result is True

    def test_approve_nonexistent_raises(self, pipeline):
        with pytest.raises(ValueError, match="not found"):
            pipeline.approve(9999)

    def test_approve_published_raises(self, pipeline):
        cid = pipeline.kb.add_content(
            "tweet", "twitter", "Test", status="published"
        )
        with pytest.raises(ValueError, match="Cannot approve"):
            pipeline.approve(cid)

    def test_reject_content(self, pipeline):
        cid = pipeline.kb.add_content(
            "tweet", "twitter", "Test tweet", status="queued"
        )
        result = pipeline.reject(cid, reason="Too aggressive")
        assert result is True
        content = pipeline.kb.get_content(cid)
        assert content.status == "rejected"

    def test_reject_nonexistent_raises(self, pipeline):
        with pytest.raises(ValueError, match="not found"):
            pipeline.reject(9999)


class TestPublish:

    def test_publish_dry_run(self, pipeline):
        cid = pipeline.kb.add_content(
            "tweet", "twitter", "Test tweet content", status="approved"
        )
        result = pipeline.publish(cid, dry_run=True)
        assert result["status"] == "dry_run"
        assert result["content_id"] == cid
        # Status should remain approved (not published)
        content = pipeline.kb.get_content(cid)
        assert content.status == "approved"

    def test_publish_requires_approved_status(self, pipeline):
        cid = pipeline.kb.add_content(
            "tweet", "twitter", "Test", status="queued"
        )
        with pytest.raises(ValueError, match="must be approved"):
            pipeline.publish(cid)

    def test_publish_requires_publisher(self, pipeline):
        cid = pipeline.kb.add_content(
            "tweet", "twitter", "Test", status="approved"
        )
        with pytest.raises(ValueError, match="Publisher required"):
            pipeline.publish(cid)

    def test_publish_with_mock_publisher(self, pipeline):
        cid = pipeline.kb.add_content(
            "tweet", "twitter", "Test tweet", status="approved"
        )
        mock_publisher = MagicMock()
        mock_publisher.publish.return_value = {
            "success": True,
            "post_id": "tweet_12345",
            "platform": "twitter",
        }

        result = pipeline.publish(cid, publisher=mock_publisher)
        assert result["success"] is True

        content = pipeline.kb.get_content(cid)
        assert content.status == "published"
        assert content.platform_post_id == "tweet_12345"

    def test_publish_nonexistent_raises(self, pipeline):
        with pytest.raises(ValueError, match="not found"):
            pipeline.publish(9999)


class TestEditAndRequeue:

    def test_edit_and_requeue(self, pipeline):
        cid = pipeline.kb.add_content(
            "tweet", "twitter", "Original tweet", status="rejected"
        )
        result = pipeline.edit_and_requeue(cid, "Updated tweet", "New Title")
        assert result is True

        content = pipeline.kb.get_content(cid)
        assert content.body == "Updated tweet"
        assert content.title == "New Title"
        assert content.status == "queued"

    def test_edit_nonexistent_raises(self, pipeline):
        with pytest.raises(ValueError, match="not found"):
            pipeline.edit_and_requeue(9999, "new body")


class TestReviewQueue:

    def test_get_review_queue(self, pipeline):
        pipeline.kb.add_content(
            "tweet", "twitter", "Queued tweet", status="queued"
        )
        pipeline.kb.add_content(
            "linkedin_post", "linkedin", "Draft post", status="draft"
        )
        pipeline.kb.add_content(
            "tweet", "twitter", "Published tweet", status="published"
        )

        queue = pipeline.get_review_queue()
        assert len(queue) == 2  # Only queued + draft
        statuses = {item["status"] for item in queue}
        assert "queued" in statuses
        assert "draft" in statuses
        assert "published" not in statuses

    def test_review_queue_includes_compliance(self, pipeline):
        pipeline.kb.add_content(
            "tweet", "twitter", "Clean workforce housing tweet.", status="queued"
        )
        queue = pipeline.get_review_queue()
        assert len(queue) == 1
        assert "is_compliant" in queue[0]


class TestPlanAndGenerate:

    def test_plan_and_generate_all(self, pipeline):
        import json
        pipeline.orchestrator.claude.generate.side_effect = [
            # First call: orchestrator plan
            json.dumps([
                {"content_type": "linkedin_post", "platform": "linkedin",
                 "topic": "Houston market", "principal": "michael"},
                {"content_type": "tweet", "platform": "twitter",
                 "topic": "Supply data", "principal": "bradley"},
            ]),
            # Second call: LinkedIn agent
            "Houston's workforce housing market...",
            # Third call: Twitter agent
            "Houston supply pipeline at lowest since 2011.",
        ]

        content_ids = pipeline.plan_and_generate(days_ahead=7)
        assert len(content_ids) == 2
        for cid in content_ids:
            content = pipeline.kb.get_content(cid)
            assert content is not None
