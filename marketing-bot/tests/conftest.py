"""Shared test fixtures for RC Marketing Bot."""

import json
import pytest

from src.db.database import Database
from src.db.knowledge_base import KnowledgeBase
from src.integrations.twitter_api import TwitterAPI
from src.integrations.linkedin_api import LinkedInAPI


@pytest.fixture
def db():
    """In-memory database for testing."""
    database = Database(":memory:")
    database.initialize()
    yield database
    database.close()


@pytest.fixture
def kb(db):
    """Knowledge base backed by in-memory database."""
    return KnowledgeBase(db)


@pytest.fixture
def seeded_kb(kb):
    """Knowledge base pre-populated with test data."""
    # Firm facts
    kb.add_firm_fact("track_record", "meta_street_return", "43.4% value increase",
                     "website")
    kb.add_firm_fact("track_record", "meta_street_hold", "18 months", "website")
    kb.add_firm_fact("portfolio", "total_units", "143", "website")
    kb.add_firm_fact("portfolio", "total_volume", "$20M+", "website")
    kb.add_firm_fact("thesis", "target_irr", "18-25%", "investor_deck")
    kb.add_firm_fact("thesis", "hold_period", "5-7 years", "investor_deck")
    kb.add_firm_fact("thesis", "deal_size", "$5-20M", "website")
    kb.add_firm_fact("advantage", "co_investment", "5-10% personal capital", "website")
    kb.add_firm_fact("terms", "min_investment", "$100,000", "website")

    # Market data
    kb.add_market_data("houston", "occupancy", "90.4%", "Q4 2025", "CoStar")
    kb.add_market_data("houston", "absorption", "26,510 units", "2025", "CoStar")
    kb.add_market_data("houston", "rent_growth", "2.1%", "Q4 2025", "CoStar")
    kb.add_market_data("houston", "supply_pipeline", "9,087 units", "Q4 2025",
                       "CoStar")
    kb.add_market_data("houston", "avg_rent", "$1,277/month", "2024", "CoStar")
    kb.add_market_data("houston", "population_growth", "200,000 residents", "2024",
                       "Census")
    kb.add_market_data("phoenix", "units", "15", "2025", "internal")

    # Brand rules
    kb.add_brand_rule("terminology", "Use 'workforce housing' not 'affordable housing'",
                      "Houston's workforce housing segment...")
    kb.add_brand_rule("terminology",
                      "Use 'value creation' not 'flipping'",
                      "Our value creation strategy...")
    kb.add_brand_rule("tone", "Professional, analytical, data-driven",
                      "Houston occupancy reached 90.4% in Q4 2025...")
    kb.add_brand_rule("compliance",
                      "Never guarantee returns",
                      "Target IRR of 18-25% (not guaranteed)")
    kb.add_brand_rule("compliance",
                      "Include past performance disclaimer on track record mentions")
    kb.add_brand_rule("avoid", "Do not use 'affordable housing'")
    kb.add_brand_rule("avoid", "Do not use 'flipping'")

    # Data sources
    kb.add_data_source("BLS Employment Release",
                       "https://www.bls.gov", "monthly")
    kb.add_data_source("CoStar Houston Report", None, "quarterly")
    kb.add_data_source("Census Population Estimates",
                       "https://www.census.gov", "annual")

    return kb


@pytest.fixture
def sample_content(kb):
    """Create sample content entries."""
    ids = []
    ids.append(kb.add_content(
        "linkedin_post", "linkedin",
        "Houston's multifamily market is showing strength...",
        principal="michael", topic="market_analysis", status="draft",
    ))
    ids.append(kb.add_content(
        "tweet", "twitter",
        "Houston Q4 occupancy: 90.4%. Supply pipeline at lowest since 2011.",
        principal="bradley", topic="market_analysis", status="queued",
    ))
    ids.append(kb.add_content(
        "blog", "blog",
        "<h1>Why Workforce Housing Remains Resilient</h1><p>Long article...</p>",
        title="Why Workforce Housing Remains Resilient",
        topic="investment_strategy", status="published",
    ))
    return ids


@pytest.fixture
def mock_claude_response():
    """Factory for mock Claude API responses."""
    def _make_response(text="Generated content about Houston market."):
        class MockContent:
            def __init__(self, t):
                self.text = t
                self.type = "text"

        class MockUsage:
            input_tokens = 100
            output_tokens = 50

        class MockResponse:
            def __init__(self, t):
                self.content = [MockContent(t)]
                self.usage = MockUsage()
                self.model = "claude-sonnet-4-5-20250929"
                self.stop_reason = "end_turn"

        return MockResponse(text)
    return _make_response


@pytest.fixture
def scanner(seeded_kb, monkeypatch, mock_claude_response):
    """ContentScanner with mock APIs and mock Claude."""
    from src.agents.scanner_agent import ContentScanner

    class MockClaudeClient:
        def generate(self, system_prompt="", user_prompt="", max_tokens=1000,
                     temperature=0.7, max_retries=3):
            return json.dumps({
                "title": "Industry Digest — Test",
                "summary": "- Theme 1: Houston market\n- Theme 2: Workforce housing",
                "highlights": [{"index": 0, "reason": "Key market data"}],
                "topic_tags": [{"index": 0, "tags": "houston,multifamily"}],
                "opportunities": ["Respond to competitor analysis"],
            })

    twitter = TwitterAPI(mock_mode=True)
    linkedin = LinkedInAPI(mock_mode=True)
    claude = MockClaudeClient()

    return ContentScanner(claude, seeded_kb, twitter, linkedin)


@pytest.fixture
def web_client(seeded_kb, sample_content):
    """Flask test client with seeded database."""
    from src.web.app import create_app

    # The seeded_kb and sample_content fixtures share the same in-memory db.
    # We need to pass the db to Flask. We'll use a custom app creation.
    app = create_app(db_path=":memory:")

    # Override get_kb to return our seeded_kb
    @app.before_request
    def _override_kb():
        from flask import g
        g._test_kb = seeded_kb

    # Monkey-patch the routes' get_kb
    original_get_kb = None
    for rule in app.url_map.iter_rules():
        pass  # just iterating

    # Instead, we'll use a simpler approach: override at module level
    import src.web.app as web_module

    # Store reference to the kb's db for the app
    app.config["_TEST_KB"] = seeded_kb
    app.config["TESTING"] = True

    # Patch the get_kb closure in the app
    # We need to replace the create_app's internal get_kb
    # The cleanest way is to modify the app's view functions
    with app.test_client() as client:
        # We need a different approach - let's create the app properly
        pass

    # Recreate with proper DB sharing
    app2 = create_app.__wrapped__(seeded_kb.db) if hasattr(create_app, '__wrapped__') else None

    # Simplest approach: create a fresh app that uses the seeded_kb's database
    from flask import Flask
    from src.db.models import ContentDraft

    app = Flask(__name__,
                template_folder=str(__import__('pathlib').Path(__file__).parent.parent / "src" / "web" / "templates"),
                static_folder=str(__import__('pathlib').Path(__file__).parent.parent / "src" / "web" / "static"))
    app.secret_key = "test-secret"
    app.config["TESTING"] = True

    kb = seeded_kb

    @app.route("/")
    def dashboard():
        queued = kb.get_content_by_status("queued")
        drafts = kb.get_content_by_status("draft")
        queue_count = len(queued) + len(drafts)
        published = kb.get_content_by_status("published")[:5]
        from datetime import datetime, timedelta
        today = datetime.now().strftime("%Y-%m-%d")
        week_later = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        upcoming = kb.get_calendar_entries_by_date_range(today, week_later)
        digests = kb.get_recent_digests(limit=1)
        latest_digest = digests[0] if digests else None
        from flask import render_template
        return render_template("dashboard.html",
                               queue_count=queue_count, published=published,
                               upcoming=upcoming, latest_digest=latest_digest)

    @app.route("/review")
    def review():
        queued = kb.get_content_by_status("queued")
        drafts = kb.get_content_by_status("draft")
        items = queued + drafts
        from src.agents.base_agent import BaseAgent
        from src.agents.linkedin_agent import LinkedInAgent
        review_items = []
        for content in items:
            check = LinkedInAgent.__new__(LinkedInAgent)
            validation = BaseAgent.validate(check, content.body, content.content_type)
            review_items.append({"content": content, "is_compliant": validation.is_compliant, "issues": validation.issues})
        from flask import render_template
        return render_template("review.html", items=review_items)

    @app.route("/content/<int:content_id>")
    def content_detail(content_id):
        from flask import render_template, redirect, url_for, flash
        content = kb.get_content(content_id)
        if content is None:
            flash("Content not found.", "error")
            return redirect(url_for("review"))
        from src.agents.base_agent import BaseAgent
        from src.agents.linkedin_agent import LinkedInAgent
        check = LinkedInAgent.__new__(LinkedInAgent)
        validation = BaseAgent.validate(check, content.body, content.content_type)
        return render_template("content.html", content=content, validation=validation)

    @app.route("/content/<int:content_id>/approve", methods=["POST"])
    def approve_content(content_id):
        from flask import redirect, url_for, flash
        content = kb.get_content(content_id)
        if content is None:
            flash("Content not found.", "error")
            return redirect(url_for("review"))
        if content.status not in ("draft", "queued"):
            flash(f"Cannot approve content with status '{content.status}'.", "error")
            return redirect(url_for("content_detail", content_id=content_id))
        kb.update_content_status(content_id, "approved")
        flash(f"Content #{content_id} approved.", "success")
        return redirect(url_for("review"))

    @app.route("/content/<int:content_id>/reject", methods=["POST"])
    def reject_content(content_id):
        from flask import redirect, url_for, flash
        content = kb.get_content(content_id)
        if content is None:
            flash("Content not found.", "error")
            return redirect(url_for("review"))
        kb.update_content_status(content_id, "rejected")
        flash(f"Content #{content_id} rejected.", "warning")
        return redirect(url_for("review"))

    @app.route("/content/<int:content_id>/edit", methods=["POST"])
    def edit_content(content_id):
        from flask import request, redirect, url_for, flash
        content = kb.get_content(content_id)
        if content is None:
            flash("Content not found.", "error")
            return redirect(url_for("review"))
        new_body = request.form.get("body", "")
        if new_body.strip():
            kb.update_content_body(content_id, new_body)
            kb.update_content_status(content_id, "queued")
            flash(f"Content #{content_id} updated and requeued.", "success")
        return redirect(url_for("content_detail", content_id=content_id))

    @app.route("/content/<int:content_id>/publish", methods=["POST"])
    def publish_content(content_id):
        from flask import request, redirect, url_for, flash
        content = kb.get_content(content_id)
        if content is None:
            flash("Content not found.", "error")
            return redirect(url_for("review"))
        if content.status != "approved":
            flash("Content must be approved before publishing.", "error")
            return redirect(url_for("content_detail", content_id=content_id))
        dry_run = request.form.get("dry_run") == "1"
        if dry_run:
            flash(f"Dry run: Content #{content_id} would be published.", "info")
            return redirect(url_for("content_detail", content_id=content_id))
        kb.update_content_status(content_id, "published")
        flash(f"Content #{content_id} published.", "success")
        return redirect(url_for("review"))

    @app.route("/digest")
    def digest_list():
        from flask import render_template
        digests = kb.get_recent_digests(limit=20)
        return render_template("digests.html", digests=digests)

    @app.route("/digest/<int:digest_id>")
    def digest_detail(digest_id):
        from flask import render_template, redirect, url_for, flash, request
        digest = kb.get_digest(digest_id)
        if digest is None:
            flash("Digest not found.", "error")
            return redirect(url_for("digest_list"))
        items = kb.get_scanned_content_by_digest(digest_id)
        platform_filter = request.args.get("platform", "")
        sort_by = request.args.get("sort", "engagement")
        if platform_filter:
            items = [i for i in items if i.platform == platform_filter]
        if sort_by == "engagement":
            items.sort(key=lambda x: x.engagement_score, reverse=True)
        return render_template("digest.html", digest=digest, items=items,
                               platform_filter=platform_filter, sort_by=sort_by)

    @app.route("/digest/<int:digest_id>/like/<int:scanned_id>", methods=["POST"])
    def like_scanned(digest_id, scanned_id):
        from flask import request, redirect, url_for, flash
        scanned = kb.get_scanned_content(scanned_id)
        if scanned is None:
            flash("Scanned content not found.", "error")
            return redirect(url_for("digest_detail", digest_id=digest_id))
        notes = request.form.get("notes", "")
        liked_by = request.form.get("liked_by", "user")
        kb.add_inspiration(source_type="digest_like", body=scanned.body,
                           url=scanned.url, author=scanned.author,
                           notes=notes or None, liked_by=liked_by,
                           scanned_content_id=scanned_id)
        flash("Saved to inspiration.", "success")
        return redirect(url_for("digest_detail", digest_id=digest_id))

    @app.route("/inspiration")
    def inspiration():
        from flask import render_template
        items = kb.get_recent_inspiration(limit=50)
        digest_likes = [i for i in items if i.source_type == "digest_like"]
        pasted_urls = [i for i in items if i.source_type == "pasted_url"]
        return render_template("inspiration.html", digest_likes=digest_likes, pasted_urls=pasted_urls)

    @app.route("/inspiration/add", methods=["POST"])
    def add_inspiration():
        from flask import request, redirect, url_for, flash
        url = request.form.get("url", "").strip()
        notes = request.form.get("notes", "").strip()
        liked_by = request.form.get("liked_by", "user")
        if not url:
            flash("URL is required.", "error")
            return redirect(url_for("inspiration"))
        kb.add_inspiration(source_type="pasted_url", body=url, url=url,
                           notes=notes or None, liked_by=liked_by)
        flash("Inspiration saved.", "success")
        return redirect(url_for("inspiration"))

    @app.route("/calendar")
    def calendar():
        from flask import render_template
        entries = kb.get_all_calendar_entries()
        return render_template("calendar.html", entries=entries)

    @app.route("/calendar/add", methods=["POST"])
    def calendar_add():
        from flask import request, redirect, url_for, flash
        scheduled_date = request.form.get("scheduled_date", "").strip()
        content_type = request.form.get("content_type", "").strip()
        platform = request.form.get("platform", "").strip()
        topic = request.form.get("topic", "").strip()
        principal = request.form.get("principal", "").strip()
        notes = request.form.get("notes", "").strip()
        if not scheduled_date or not content_type or not platform:
            flash("Date, content type, and platform are required.", "error")
            return redirect(url_for("calendar"))
        kb.add_calendar_entry(content_type=content_type, platform=platform,
                              scheduled_date=scheduled_date,
                              topic=topic or None, principal=principal or None,
                              notes=notes or None)
        flash("Calendar entry added.", "success")
        return redirect(url_for("calendar"))

    @app.route("/calendar/<int:entry_id>/edit", methods=["POST"])
    def calendar_edit(entry_id):
        from flask import request, redirect, url_for, flash
        entry = kb.get_calendar_entry(entry_id)
        if entry is None:
            flash("Calendar entry not found.", "error")
            return redirect(url_for("calendar"))
        updates = {}
        for fld in ("content_type", "platform", "topic", "principal",
                     "scheduled_date", "notes"):
            val = request.form.get(fld)
            if val is not None:
                updates[fld] = val.strip() if val.strip() else None
        if updates:
            kb.update_calendar_entry(entry_id, **updates)
            flash(f"Calendar entry #{entry_id} updated.", "success")
        return redirect(url_for("calendar"))

    @app.route("/calendar/<int:entry_id>/delete", methods=["POST"])
    def calendar_delete(entry_id):
        from flask import redirect, url_for, flash
        entry = kb.get_calendar_entry(entry_id)
        if entry is None:
            flash("Calendar entry not found.", "error")
            return redirect(url_for("calendar"))
        kb.delete_calendar_entry(entry_id)
        flash(f"Calendar entry #{entry_id} deleted.", "success")
        return redirect(url_for("calendar"))

    @app.route("/calendar/<int:entry_id>/generate", methods=["POST"])
    def calendar_generate(entry_id):
        from flask import redirect, url_for, flash
        from src.db.models import ContentTask
        entry = kb.get_calendar_entry(entry_id)
        if entry is None:
            flash("Calendar entry not found.", "error")
            return redirect(url_for("calendar"))
        task = ContentTask(content_type=entry.content_type, platform=entry.platform,
                           topic=entry.topic or "", principal=entry.principal,
                           calendar_entry_id=entry.id)

        from src.pipeline.content_pipeline import ContentPipeline

        class MockClaudeForGen:
            def generate(self, **kw):
                return "Generated content about Houston market."

        pipeline = ContentPipeline(MockClaudeForGen(), kb)
        content_id = pipeline.generate_and_queue(task)
        flash(f"Content generated from calendar entry #{entry_id}.", "success")
        return redirect(url_for("content_detail", content_id=content_id))

    @app.route("/generate", methods=["GET"])
    def generate_form():
        from flask import render_template
        return render_template("generate.html")

    @app.route("/generate", methods=["POST"])
    def generate_content_action():
        from flask import request, redirect, url_for, flash
        from src.db.models import ContentTask
        content_type = request.form.get("content_type", "").strip()
        platform = request.form.get("platform", "").strip()
        topic = request.form.get("topic", "").strip()
        principal = request.form.get("principal", "").strip()
        instructions = request.form.get("instructions", "").strip()
        if not content_type or not platform or not topic:
            flash("Content type, platform, and topic are required.", "error")
            return redirect(url_for("generate_form"))
        task = ContentTask(content_type=content_type, platform=platform,
                           topic=topic, principal=principal or None,
                           instructions=instructions or None)

        from src.pipeline.content_pipeline import ContentPipeline

        class MockClaudeForGen:
            def generate(self, **kw):
                return "Generated content about Houston market."

        pipeline = ContentPipeline(MockClaudeForGen(), kb)
        content_id = pipeline.generate_and_queue(task)
        flash("Content generated successfully.", "success")
        return redirect(url_for("content_detail", content_id=content_id))

    @app.route("/knowledge-base")
    def knowledge_base():
        from flask import render_template
        firm_facts = kb.get_all_firm_facts()
        market_data = kb.get_all_market_data()
        data_sources = kb.get_all_data_sources()
        brand_rules = kb.get_all_brand_rules()
        return render_template("knowledge_base.html",
                               firm_facts=firm_facts, market_data=market_data,
                               data_sources=data_sources, brand_rules=brand_rules)

    @app.route("/accounts")
    def accounts_page():
        from flask import render_template
        accounts = kb.get_all_monitored_accounts()
        return render_template("accounts.html", accounts=accounts)

    @app.route("/accounts/add", methods=["POST"])
    def add_account():
        from flask import request, redirect, url_for, flash
        platform = request.form.get("platform", "twitter")
        handle = request.form.get("handle", "").strip().lstrip("@")
        name = request.form.get("name", "").strip()
        category = request.form.get("category", "").strip()
        if not handle:
            flash("Handle is required.", "error")
            return redirect(url_for("accounts_page"))
        kb.add_monitored_account(platform=platform, handle=handle,
                                 name=name or None, category=category or None)
        flash(f"Added @{handle} ({platform}).", "success")
        return redirect(url_for("accounts_page"))

    @app.route("/accounts/<int:account_id>/toggle", methods=["POST"])
    def toggle_account(account_id):
        from flask import redirect, url_for, flash
        account = kb.get_monitored_account(account_id)
        if account:
            kb.toggle_monitored_account(account_id, not account.active)
            flash(f"Account toggled.", "success")
        return redirect(url_for("accounts_page"))

    @app.route("/scan", methods=["POST"])
    def trigger_scan():
        from flask import redirect, url_for, flash
        from src.agents.scanner_agent import ContentScanner

        class MockClaudeForScan:
            def generate(self, **kw):
                return json.dumps({
                    "title": "Test Scan Digest",
                    "summary": "Test summary",
                    "topic_tags": [], "highlights": [], "opportunities": [],
                })

        scanner = ContentScanner(MockClaudeForScan(), kb,
                                 TwitterAPI(mock_mode=True),
                                 LinkedInAPI(mock_mode=True))
        digest = scanner.run_scan(scan_type="manual")
        flash(f"Scan complete. Digest: {digest.title}", "success")
        return redirect(url_for("digest_detail", digest_id=digest.id))

    with app.test_client() as client:
        yield client
