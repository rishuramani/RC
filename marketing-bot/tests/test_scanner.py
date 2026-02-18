"""Tests for the Content Scanner Agent."""

import json
import pytest

from src.agents.scanner_agent import ContentScanner
from src.db.models import ScannedContent, Digest


class TestContentScanner:
    """Tests for ContentScanner."""

    def test_scan_twitter_mock(self, scanner):
        """Scanner returns mock tweets from search queries."""
        items = scanner.scan_twitter(queries=["multifamily houston"], limit=10)
        assert len(items) > 0
        assert all(isinstance(i, ScannedContent) for i in items)
        assert all(i.platform == "twitter" for i in items)

    def test_scan_twitter_with_accounts(self, scanner):
        """Scanner also fetches tweets from monitored accounts."""
        items = scanner.scan_twitter(
            queries=["multifamily"],
            accounts=["@test_analyst"],
            limit=20,
        )
        assert len(items) > 0
        # Should have items from both search and account
        authors = {i.author for i in items}
        assert "test_analyst" in authors

    def test_scan_twitter_deduplicates_by_id(self, scanner):
        """Scanner does not include duplicate tweet IDs."""
        items = scanner.scan_twitter(queries=["multifamily houston"], limit=20)
        ids = [i.external_id for i in items]
        assert len(ids) == len(set(ids))

    def test_scan_linkedin_mock(self, scanner):
        """Scanner returns mock LinkedIn posts."""
        items = scanner.scan_linkedin(queries=["multifamily real estate"], limit=5)
        assert len(items) > 0
        assert all(i.platform == "linkedin" for i in items)

    def test_engagement_score_calculated(self, scanner):
        """Engagement score is computed from metrics."""
        items = scanner.scan_twitter(queries=["CRE investment"], limit=5)
        for item in items:
            assert item.engagement_score > 0

    def test_create_digest(self, scanner, mock_claude_response):
        """create_digest saves items and returns a digest."""
        items = [
            ScannedContent(
                platform="twitter", external_id="t1",
                author="analyst_1", body="Houston multifamily occupancy hits 90%",
                engagement_score=100,
            ),
            ScannedContent(
                platform="linkedin", external_id="li1",
                author="expert_2", body="Workforce housing demand surging in Sunbelt",
                engagement_score=200,
            ),
        ]

        digest = scanner.create_digest(items, scan_type="manual")
        assert digest is not None
        assert isinstance(digest, Digest)
        assert digest.id is not None
        assert digest.scan_type == "manual"

        # Items should be saved to DB
        saved = scanner.kb.get_scanned_content_by_digest(digest.id)
        assert len(saved) == 2

    def test_run_scan_full_pipeline(self, scanner, mock_claude_response):
        """run_scan executes the full pipeline."""
        digest = scanner.run_scan(scan_type="manual")
        assert digest is not None
        assert digest.id is not None

        # Should have scanned content linked to digest
        items = scanner.kb.get_scanned_content_by_digest(digest.id)
        assert len(items) > 0

    def test_run_scan_twitter_only(self, scanner, mock_claude_response):
        """run_scan with twitter_only skips LinkedIn."""
        digest = scanner.run_scan(scan_type="manual", twitter_only=True)
        items = scanner.kb.get_scanned_content_by_digest(digest.id)
        platforms = {i.platform for i in items}
        assert "linkedin" not in platforms

    def test_deduplication_on_second_scan(self, scanner, mock_claude_response):
        """Second scan should not re-add existing items."""
        digest1 = scanner.run_scan(scan_type="manual")
        count1 = len(scanner.kb.get_scanned_content_by_digest(digest1.id))

        digest2 = scanner.run_scan(scan_type="manual")
        # Second scan should find all items already exist
        items2 = scanner.kb.get_scanned_content_by_digest(digest2.id)
        # The second digest exists but should have 0 new items (all deduped)
        assert len(items2) == 0

    def test_monitored_accounts_integrated(self, scanner, seeded_kb, mock_claude_response):
        """Scanner uses monitored accounts from DB."""
        seeded_kb.add_monitored_account("twitter", "houston_cre", "Houston CRE", "analyst")
        digest = scanner.run_scan(scan_type="scheduled")
        items = scanner.kb.get_scanned_content_by_digest(digest.id)
        authors = {i.author for i in items}
        assert "houston_cre" in authors


class TestScannerEdgeCases:
    """Edge case tests for scanner."""

    def test_empty_scan(self, seeded_kb):
        """Scanner handles case with no results."""
        from src.integrations.twitter_api import TwitterAPI
        from src.integrations.linkedin_api import LinkedInAPI

        class EmptyTwitter(TwitterAPI):
            def search_recent(self, *a, **kw):
                return []
            def get_user_tweets(self, *a, **kw):
                return []

        class EmptyLinkedIn(LinkedInAPI):
            pass

        scanner = ContentScanner(
            claude_client=None,
            knowledge_base=seeded_kb,
            twitter_api=EmptyTwitter(mock_mode=True),
            linkedin_api=EmptyLinkedIn(mock_mode=True),
        )
        # Override scan methods to return empty
        scanner.scan_twitter = lambda **kw: []
        scanner.scan_linkedin = lambda **kw: []

        digest = scanner.run_scan()
        assert digest is not None
        assert "Empty" in (digest.title or "") or "No" in (digest.summary or "")

    def test_scanned_content_exists_check(self, seeded_kb):
        """scanned_content_exists correctly identifies existing items."""
        seeded_kb.add_scanned_content(
            platform="twitter", body="test", external_id="exists_123"
        )
        assert seeded_kb.scanned_content_exists("exists_123", "twitter")
        assert not seeded_kb.scanned_content_exists("not_exists", "twitter")
        assert not seeded_kb.scanned_content_exists("exists_123", "linkedin")
