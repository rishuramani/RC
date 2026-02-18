"""Tests for the Inspiration system and monitored accounts."""

import pytest

from src.db.models import Inspiration, MonitoredAccount, ScannedContent


class TestInspiration:
    """Tests for inspiration CRUD operations."""

    def test_add_inspiration_pasted_url(self, seeded_kb):
        """Can add a pasted URL as inspiration."""
        insp_id = seeded_kb.add_inspiration(
            source_type="pasted_url",
            body="Great article on Houston multifamily trends",
            url="https://example.com/article",
            notes="Love the data visualization",
            liked_by="michael",
        )
        assert insp_id is not None

        insp = seeded_kb.get_inspiration(insp_id)
        assert insp.source_type == "pasted_url"
        assert insp.url == "https://example.com/article"
        assert insp.liked_by == "michael"
        assert insp.notes == "Love the data visualization"

    def test_add_inspiration_digest_like(self, seeded_kb):
        """Can add a liked scanned post as inspiration."""
        # First add a scanned content item
        sc_id = seeded_kb.add_scanned_content(
            platform="twitter",
            body="Houston occupancy breaking records",
            external_id="tweet_999",
            author="market_guru",
        )

        insp_id = seeded_kb.add_inspiration(
            source_type="digest_like",
            body="Houston occupancy breaking records",
            author="market_guru",
            liked_by="bradley",
            scanned_content_id=sc_id,
        )

        insp = seeded_kb.get_inspiration(insp_id)
        assert insp.source_type == "digest_like"
        assert insp.scanned_content_id == sc_id
        assert insp.liked_by == "bradley"

    def test_get_recent_inspiration(self, seeded_kb):
        """get_recent_inspiration returns items in reverse chronological order."""
        seeded_kb.add_inspiration("pasted_url", body="First", liked_by="michael")
        seeded_kb.add_inspiration("pasted_url", body="Second", liked_by="michael")
        seeded_kb.add_inspiration("pasted_url", body="Third", liked_by="bradley")

        items = seeded_kb.get_recent_inspiration(limit=10)
        assert len(items) == 3
        assert all(isinstance(i, Inspiration) for i in items)

    def test_get_inspiration_by_user(self, seeded_kb):
        """Can filter inspiration by user."""
        seeded_kb.add_inspiration("pasted_url", body="Michael's pick", liked_by="michael")
        seeded_kb.add_inspiration("pasted_url", body="Bradley's pick", liked_by="bradley")
        seeded_kb.add_inspiration("pasted_url", body="Michael's second", liked_by="michael")

        michael_items = seeded_kb.get_inspiration_by_user("michael")
        assert len(michael_items) == 2
        assert all(i.liked_by == "michael" for i in michael_items)

        bradley_items = seeded_kb.get_inspiration_by_user("bradley")
        assert len(bradley_items) == 1

    def test_delete_inspiration(self, seeded_kb):
        """Can delete an inspiration entry."""
        insp_id = seeded_kb.add_inspiration("pasted_url", body="Temporary")
        assert seeded_kb.get_inspiration(insp_id) is not None
        seeded_kb.delete_inspiration(insp_id)
        assert seeded_kb.get_inspiration(insp_id) is None

    def test_inspiration_in_context(self, seeded_kb):
        """Inspiration appears in get_context_for_topic output."""
        seeded_kb.add_inspiration(
            "pasted_url",
            body="Sunbelt multifamily insight",
            author="Expert",
            liked_by="michael",
        )

        context = seeded_kb.get_context_for_topic("multifamily")
        assert "inspiration" in context
        assert len(context["inspiration"]) >= 1
        assert any("Sunbelt" in (i.get("body") or "") for i in context["inspiration"])

    def test_inspiration_limit(self, seeded_kb):
        """get_recent_inspiration respects limit parameter."""
        for i in range(10):
            seeded_kb.add_inspiration("pasted_url", body=f"Item {i}")
        items = seeded_kb.get_recent_inspiration(limit=3)
        assert len(items) == 3


class TestMonitoredAccounts:
    """Tests for monitored accounts CRUD."""

    def test_add_monitored_account(self, seeded_kb):
        """Can add a monitored account."""
        aid = seeded_kb.add_monitored_account(
            platform="twitter",
            handle="houston_cre",
            name="Houston CRE",
            category="analyst",
        )
        assert aid is not None

        account = seeded_kb.get_monitored_account(aid)
        assert account.platform == "twitter"
        assert account.handle == "houston_cre"
        assert account.name == "Houston CRE"
        assert account.category == "analyst"
        assert account.active == 1

    def test_get_monitored_accounts_by_platform(self, seeded_kb):
        """Can filter accounts by platform."""
        seeded_kb.add_monitored_account("twitter", "tw_user1", category="analyst")
        seeded_kb.add_monitored_account("twitter", "tw_user2", category="competitor")
        seeded_kb.add_monitored_account("linkedin", "li_user1", category="media")

        twitter = seeded_kb.get_monitored_accounts(platform="twitter")
        assert len(twitter) == 2
        assert all(a.platform == "twitter" for a in twitter)

        linkedin = seeded_kb.get_monitored_accounts(platform="linkedin")
        assert len(linkedin) == 1

    def test_get_all_monitored_accounts(self, seeded_kb):
        """get_all_monitored_accounts includes inactive accounts."""
        a1 = seeded_kb.add_monitored_account("twitter", "active_user")
        a2 = seeded_kb.add_monitored_account("twitter", "inactive_user")
        seeded_kb.toggle_monitored_account(a2, active=False)

        all_accounts = seeded_kb.get_all_monitored_accounts()
        assert len(all_accounts) == 2

        active_only = seeded_kb.get_monitored_accounts()
        assert len(active_only) == 1
        assert active_only[0].handle == "active_user"

    def test_toggle_monitored_account(self, seeded_kb):
        """Can toggle account active status."""
        aid = seeded_kb.add_monitored_account("twitter", "toggle_user")
        account = seeded_kb.get_monitored_account(aid)
        assert account.active == 1

        seeded_kb.toggle_monitored_account(aid, active=False)
        account = seeded_kb.get_monitored_account(aid)
        assert account.active == 0

        seeded_kb.toggle_monitored_account(aid, active=True)
        account = seeded_kb.get_monitored_account(aid)
        assert account.active == 1

    def test_delete_monitored_account(self, seeded_kb):
        """Can delete a monitored account."""
        aid = seeded_kb.add_monitored_account("twitter", "delete_me")
        assert seeded_kb.get_monitored_account(aid) is not None
        seeded_kb.delete_monitored_account(aid)
        assert seeded_kb.get_monitored_account(aid) is None


class TestScannedContent:
    """Tests for scanned content CRUD."""

    def test_add_scanned_content(self, seeded_kb):
        """Can add scanned content."""
        sc_id = seeded_kb.add_scanned_content(
            platform="twitter",
            body="Houston market update",
            external_id="tweet_001",
            author="analyst_1",
            engagement_score=150,
            topic_tags="houston,multifamily",
        )
        assert sc_id is not None

        item = seeded_kb.get_scanned_content(sc_id)
        assert item.platform == "twitter"
        assert item.body == "Houston market update"
        assert item.engagement_score == 150
        assert item.topic_tags == "houston,multifamily"

    def test_get_scanned_content_by_digest(self, seeded_kb):
        """Can get scanned content by digest ID."""
        digest_id = seeded_kb.add_digest("Test Digest", "Summary", "manual")
        seeded_kb.add_scanned_content(
            "twitter", "Post 1", digest_id=digest_id, engagement_score=100
        )
        seeded_kb.add_scanned_content(
            "linkedin", "Post 2", digest_id=digest_id, engagement_score=200
        )

        items = seeded_kb.get_scanned_content_by_digest(digest_id)
        assert len(items) == 2
        # Should be ordered by engagement_score DESC
        assert items[0].engagement_score >= items[1].engagement_score

    def test_search_scanned_content(self, seeded_kb):
        """Can search scanned content by body, author, or tags."""
        seeded_kb.add_scanned_content(
            "twitter", "Houston occupancy data", author="houston_expert",
            topic_tags="houston,occupancy"
        )
        seeded_kb.add_scanned_content(
            "linkedin", "Phoenix market update", author="phoenix_analyst",
            topic_tags="phoenix,multifamily"
        )

        results = seeded_kb.search_scanned_content("houston")
        assert len(results) >= 1
        assert any("Houston" in r.body or "houston" in (r.topic_tags or "") for r in results)


class TestDigests:
    """Tests for digest CRUD."""

    def test_add_and_get_digest(self, seeded_kb):
        """Can create and retrieve a digest."""
        digest_id = seeded_kb.add_digest(
            title="Industry Digest — Feb 17, 2026",
            summary="- Theme 1\n- Theme 2",
            scan_type="scheduled",
        )

        digest = seeded_kb.get_digest(digest_id)
        assert digest.title == "Industry Digest — Feb 17, 2026"
        assert "Theme 1" in digest.summary
        assert digest.scan_type == "scheduled"

    def test_get_recent_digests(self, seeded_kb):
        """get_recent_digests returns digests in reverse chronological order."""
        seeded_kb.add_digest("Digest 1")
        seeded_kb.add_digest("Digest 2")
        seeded_kb.add_digest("Digest 3")

        digests = seeded_kb.get_recent_digests(limit=2)
        assert len(digests) == 2

    def test_update_digest(self, seeded_kb):
        """Can update a digest."""
        digest_id = seeded_kb.add_digest("Original Title")
        seeded_kb.update_digest(digest_id, title="Updated Title", summary="New summary")

        digest = seeded_kb.get_digest(digest_id)
        assert digest.title == "Updated Title"
        assert digest.summary == "New summary"
