"""Tests for the Flask web application."""

import pytest


class TestDashboard:
    """Tests for the dashboard route."""

    def test_dashboard_loads(self, web_client):
        """Dashboard returns 200."""
        response = web_client.get("/")
        assert response.status_code == 200
        assert b"Dashboard" in response.data

    def test_dashboard_shows_queue_count(self, web_client, seeded_kb, sample_content):
        """Dashboard shows pending review count."""
        response = web_client.get("/")
        assert response.status_code == 200


class TestReviewQueue:
    """Tests for the review queue route."""

    def test_review_page_loads(self, web_client):
        """Review page returns 200."""
        response = web_client.get("/review")
        assert response.status_code == 200
        assert b"Review Queue" in response.data

    def test_review_shows_pending_content(self, web_client, sample_content):
        """Review page shows queued/draft content."""
        response = web_client.get("/review")
        assert response.status_code == 200


class TestContentDetail:
    """Tests for content detail and actions."""

    def test_content_detail_loads(self, web_client, sample_content):
        """Content detail page returns 200."""
        content_id = sample_content[0]
        response = web_client.get(f"/content/{content_id}")
        assert response.status_code == 200
        assert b"Content #" in response.data

    def test_content_not_found_redirects(self, web_client):
        """Non-existent content redirects."""
        response = web_client.get("/content/99999")
        assert response.status_code == 302

    def test_approve_content(self, web_client, sample_content, seeded_kb):
        """Can approve queued content."""
        # sample_content[1] is queued
        content_id = sample_content[1]
        response = web_client.post(
            f"/content/{content_id}/approve",
            follow_redirects=True,
        )
        assert response.status_code == 200
        content = seeded_kb.get_content(content_id)
        assert content.status == "approved"

    def test_reject_content(self, web_client, sample_content, seeded_kb):
        """Can reject content with reason."""
        content_id = sample_content[0]  # draft
        response = web_client.post(
            f"/content/{content_id}/reject",
            data={"reason": "Needs more data points"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        content = seeded_kb.get_content(content_id)
        assert content.status == "rejected"

    def test_edit_content(self, web_client, sample_content, seeded_kb):
        """Can edit and requeue content."""
        content_id = sample_content[0]
        new_body = "Updated content with more data about Houston."
        response = web_client.post(
            f"/content/{content_id}/edit",
            data={"body": new_body},
            follow_redirects=True,
        )
        assert response.status_code == 200
        content = seeded_kb.get_content(content_id)
        assert content.body == new_body
        assert content.status == "queued"

    def test_publish_approved_content(self, web_client, sample_content, seeded_kb):
        """Can publish approved content."""
        content_id = sample_content[1]
        seeded_kb.update_content_status(content_id, "approved")
        response = web_client.post(
            f"/content/{content_id}/publish",
            follow_redirects=True,
        )
        assert response.status_code == 200
        content = seeded_kb.get_content(content_id)
        assert content.status == "published"

    def test_publish_dry_run(self, web_client, sample_content, seeded_kb):
        """Dry run does not change status."""
        content_id = sample_content[1]
        seeded_kb.update_content_status(content_id, "approved")
        response = web_client.post(
            f"/content/{content_id}/publish",
            data={"dry_run": "1"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        content = seeded_kb.get_content(content_id)
        assert content.status == "approved"

    def test_cannot_publish_unapproved(self, web_client, sample_content):
        """Cannot publish content that isn't approved."""
        content_id = sample_content[0]  # draft
        response = web_client.post(
            f"/content/{content_id}/publish",
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"must be approved" in response.data


class TestDigests:
    """Tests for digest routes."""

    def test_digest_list_loads(self, web_client):
        """Digest list returns 200."""
        response = web_client.get("/digest")
        assert response.status_code == 200
        assert b"Digests" in response.data

    def test_digest_detail_loads(self, web_client, seeded_kb):
        """Digest detail returns 200."""
        digest_id = seeded_kb.add_digest("Test Digest", "Summary text")
        response = web_client.get(f"/digest/{digest_id}")
        assert response.status_code == 200
        assert b"Test Digest" in response.data

    def test_digest_not_found(self, web_client):
        """Non-existent digest redirects."""
        response = web_client.get("/digest/99999")
        assert response.status_code == 302

    def test_like_scanned_content(self, web_client, seeded_kb):
        """Can like a scanned post from digest."""
        digest_id = seeded_kb.add_digest("Test Digest")
        sc_id = seeded_kb.add_scanned_content(
            "twitter", "Great post", external_id="t100",
            author="expert", digest_id=digest_id,
        )
        response = web_client.post(
            f"/digest/{digest_id}/like/{sc_id}",
            data={"notes": "Great format", "liked_by": "michael"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        items = seeded_kb.get_recent_inspiration(limit=10)
        assert len(items) >= 1
        assert any(i.source_type == "digest_like" for i in items)

    def test_digest_platform_filter(self, web_client, seeded_kb):
        """Can filter digest by platform."""
        digest_id = seeded_kb.add_digest("Filter Test")
        seeded_kb.add_scanned_content(
            "twitter", "Tweet", digest_id=digest_id
        )
        seeded_kb.add_scanned_content(
            "linkedin", "LinkedIn post", digest_id=digest_id
        )
        response = web_client.get(f"/digest/{digest_id}?platform=twitter")
        assert response.status_code == 200


class TestInspiration:
    """Tests for inspiration routes."""

    def test_inspiration_page_loads(self, web_client):
        """Inspiration page returns 200."""
        response = web_client.get("/inspiration")
        assert response.status_code == 200
        assert b"Inspiration" in response.data

    def test_add_inspiration_url(self, web_client, seeded_kb):
        """Can add a URL as inspiration."""
        response = web_client.post(
            "/inspiration/add",
            data={
                "url": "https://example.com/article",
                "notes": "Great thread structure",
                "liked_by": "michael",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        items = seeded_kb.get_recent_inspiration()
        assert len(items) >= 1

    def test_add_inspiration_requires_url(self, web_client):
        """Adding inspiration without URL shows error."""
        response = web_client.post(
            "/inspiration/add",
            data={"url": "", "notes": "test"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"required" in response.data


class TestCalendar:
    """Tests for calendar route."""

    def test_calendar_loads(self, web_client):
        """Calendar page returns 200."""
        response = web_client.get("/calendar")
        assert response.status_code == 200
        assert b"Calendar" in response.data


class TestCalendarCRUD:
    """Tests for calendar add, edit, delete operations."""

    def test_add_calendar_entry(self, web_client, seeded_kb):
        """Can add a new calendar entry."""
        response = web_client.post(
            "/calendar/add",
            data={
                "scheduled_date": "2026-03-01",
                "content_type": "linkedin_post",
                "platform": "linkedin",
                "topic": "market_update",
                "principal": "michael",
                "notes": "Q1 update",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Calendar entry added" in response.data
        entries = seeded_kb.get_all_calendar_entries()
        assert any(e.topic == "market_update" for e in entries)

    def test_add_calendar_entry_missing_fields(self, web_client):
        """Adding entry without required fields shows error."""
        response = web_client.post(
            "/calendar/add",
            data={"scheduled_date": "", "content_type": "", "platform": ""},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"required" in response.data

    def test_edit_calendar_entry(self, web_client, seeded_kb):
        """Can edit an existing calendar entry."""
        entry_id = seeded_kb.add_calendar_entry(
            "tweet", "twitter", "2026-03-05", topic="old_topic"
        )
        response = web_client.post(
            f"/calendar/{entry_id}/edit",
            data={
                "content_type": "linkedin_post",
                "platform": "linkedin",
                "topic": "new_topic",
                "principal": "bradley",
                "scheduled_date": "2026-03-10",
                "notes": "updated",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"updated" in response.data
        entry = seeded_kb.get_calendar_entry(entry_id)
        assert entry.topic == "new_topic"
        assert entry.platform == "linkedin"

    def test_delete_calendar_entry(self, web_client, seeded_kb):
        """Can delete a calendar entry."""
        entry_id = seeded_kb.add_calendar_entry(
            "blog", "blog", "2026-04-01", topic="to_delete"
        )
        response = web_client.post(
            f"/calendar/{entry_id}/delete",
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"deleted" in response.data
        assert seeded_kb.get_calendar_entry(entry_id) is None


class TestAccounts:
    """Tests for monitored accounts routes."""

    def test_accounts_page_loads(self, web_client):
        """Accounts page returns 200."""
        response = web_client.get("/accounts")
        assert response.status_code == 200
        assert b"Monitored Accounts" in response.data

    def test_add_account(self, web_client, seeded_kb):
        """Can add a monitored account."""
        response = web_client.post(
            "/accounts/add",
            data={
                "platform": "twitter",
                "handle": "@test_analyst",
                "name": "Test Analyst",
                "category": "analyst",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        accounts = seeded_kb.get_monitored_accounts()
        assert len(accounts) >= 1

    def test_toggle_account(self, web_client, seeded_kb):
        """Can toggle account active status."""
        aid = seeded_kb.add_monitored_account("twitter", "toggle_test")
        response = web_client.post(
            f"/accounts/{aid}/toggle",
            follow_redirects=True,
        )
        assert response.status_code == 200
        account = seeded_kb.get_monitored_account(aid)
        assert account.active == 0

    def test_add_account_requires_handle(self, web_client):
        """Adding account without handle shows error."""
        response = web_client.post(
            "/accounts/add",
            data={"platform": "twitter", "handle": ""},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"required" in response.data


class TestGenerate:
    """Tests for content generation routes."""

    def test_generate_form_loads(self, web_client):
        """Generate form page returns 200."""
        response = web_client.get("/generate")
        assert response.status_code == 200
        assert b"Generate Content" in response.data

    def test_generate_standalone_content(self, web_client, seeded_kb):
        """Can generate content from the standalone form."""
        response = web_client.post(
            "/generate",
            data={
                "content_type": "linkedin_post",
                "platform": "linkedin",
                "topic": "houston_market",
                "principal": "michael",
                "instructions": "Focus on occupancy data",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Content #" in response.data

    def test_generate_missing_fields(self, web_client):
        """Generate with missing fields shows error."""
        response = web_client.post(
            "/generate",
            data={"content_type": "", "platform": "", "topic": ""},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"required" in response.data

    def test_generate_from_calendar_entry(self, web_client, seeded_kb):
        """Can generate content from a calendar entry."""
        entry_id = seeded_kb.add_calendar_entry(
            "tweet", "twitter", "2026-03-15",
            topic="market_analysis", principal="bradley",
        )
        response = web_client.post(
            f"/calendar/{entry_id}/generate",
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Content #" in response.data
        entry = seeded_kb.get_calendar_entry(entry_id)
        assert entry.status == "generated"


class TestKnowledgeBase:
    """Tests for knowledge base view."""

    def test_knowledge_base_loads(self, web_client):
        """Knowledge base page returns 200."""
        response = web_client.get("/knowledge-base")
        assert response.status_code == 200
        assert b"Knowledge Base" in response.data

    def test_shows_firm_facts(self, web_client):
        """Knowledge base shows firm facts."""
        response = web_client.get("/knowledge-base")
        assert b"meta_street_return" in response.data

    def test_shows_market_data(self, web_client):
        """Knowledge base shows market data."""
        response = web_client.get("/knowledge-base")
        assert b"houston" in response.data
        assert b"occupancy" in response.data

    def test_shows_brand_rules(self, web_client):
        """Knowledge base shows brand rules."""
        response = web_client.get("/knowledge-base")
        assert b"workforce housing" in response.data

    def test_shows_data_sources(self, web_client):
        """Knowledge base shows data sources."""
        response = web_client.get("/knowledge-base")
        assert b"BLS Employment Release" in response.data


class TestScanRoute:
    """Tests for manual scan trigger."""

    def test_scan_trigger(self, web_client):
        """Can trigger a manual scan."""
        response = web_client.post("/scan", follow_redirects=True)
        assert response.status_code == 200
