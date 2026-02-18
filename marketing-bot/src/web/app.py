"""Flask application factory and routes for the RC Marketing Bot GUI."""

from flask import Flask, render_template, request, redirect, url_for, flash

from src.config import DB_PATH, WEB_SECRET_KEY
from src.db.database import Database
from src.db.knowledge_base import KnowledgeBase
from src.db.models import ContentDraft


def create_app(db_path=None):
    """Create and configure the Flask application."""
    app = Flask(__name__,
                template_folder="templates",
                static_folder="static")
    app.secret_key = WEB_SECRET_KEY

    # Store db_path for use in routes
    app.config["DB_PATH"] = str(db_path or DB_PATH)

    def get_kb():
        db = Database(app.config["DB_PATH"])
        db.initialize()
        return KnowledgeBase(db)

    def get_pipeline():
        from src.integrations.claude_client import ClaudeClient
        from src.pipeline.content_pipeline import ContentPipeline
        kb = get_kb()
        claude = ClaudeClient()
        return ContentPipeline(claude, kb)

    # ── Dashboard ──────────────────────────────────────────────

    @app.route("/")
    def dashboard():
        kb = get_kb()
        # Queue count
        queued = kb.get_content_by_status("queued")
        drafts = kb.get_content_by_status("draft")
        queue_count = len(queued) + len(drafts)

        # Recent published
        published = kb.get_content_by_status("published")[:5]

        # Upcoming calendar (next 7 days)
        from datetime import datetime, timedelta
        today = datetime.now().strftime("%Y-%m-%d")
        week_later = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        upcoming = kb.get_calendar_entries_by_date_range(today, week_later)

        # Latest digest
        digests = kb.get_recent_digests(limit=1)
        latest_digest = digests[0] if digests else None

        return render_template("dashboard.html",
                               queue_count=queue_count,
                               published=published,
                               upcoming=upcoming,
                               latest_digest=latest_digest)

    # ── Review Queue ───────────────────────────────────────────

    @app.route("/review")
    def review():
        kb = get_kb()
        queued = kb.get_content_by_status("queued")
        drafts = kb.get_content_by_status("draft")
        items = queued + drafts

        # Add basic compliance check
        from src.agents.base_agent import BaseAgent
        from src.agents.linkedin_agent import LinkedInAgent
        review_items = []
        for content in items:
            draft = ContentDraft(
                content_type=content.content_type,
                platform=content.platform,
                body=content.body,
                topic=content.topic or "",
            )
            # Use a lightweight validation
            check = LinkedInAgent.__new__(LinkedInAgent)
            validation = BaseAgent.validate(check, content.body, content.content_type)
            review_items.append({
                "content": content,
                "is_compliant": validation.is_compliant,
                "issues": validation.issues,
            })

        return render_template("review.html", items=review_items)

    # ── Content Detail ─────────────────────────────────────────

    @app.route("/content/<int:content_id>")
    def content_detail(content_id):
        kb = get_kb()
        content = kb.get_content(content_id)
        if content is None:
            flash("Content not found.", "error")
            return redirect(url_for("review"))

        # Compliance check
        from src.agents.base_agent import BaseAgent
        from src.agents.linkedin_agent import LinkedInAgent
        check = LinkedInAgent.__new__(LinkedInAgent)
        validation = BaseAgent.validate(check, content.body, content.content_type)

        return render_template("content.html",
                               content=content,
                               validation=validation)

    @app.route("/content/<int:content_id>/approve", methods=["POST"])
    def approve_content(content_id):
        kb = get_kb()
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
        kb = get_kb()
        content = kb.get_content(content_id)
        if content is None:
            flash("Content not found.", "error")
            return redirect(url_for("review"))
        reason = request.form.get("reason", "")
        kb.update_content_status(content_id, "rejected")
        flash(f"Content #{content_id} rejected.", "warning")
        return redirect(url_for("review"))

    @app.route("/content/<int:content_id>/edit", methods=["POST"])
    def edit_content(content_id):
        kb = get_kb()
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
        kb = get_kb()
        content = kb.get_content(content_id)
        if content is None:
            flash("Content not found.", "error")
            return redirect(url_for("review"))
        if content.status != "approved":
            flash("Content must be approved before publishing.", "error")
            return redirect(url_for("content_detail", content_id=content_id))

        dry_run = request.form.get("dry_run") == "1"
        if dry_run:
            flash(f"Dry run: Content #{content_id} would be published to {content.platform}.", "info")
            return redirect(url_for("content_detail", content_id=content_id))

        # Mock publish
        kb.update_content_status(content_id, "published")
        flash(f"Content #{content_id} published.", "success")
        return redirect(url_for("review"))

    # ── Digests ────────────────────────────────────────────────

    @app.route("/digest")
    def digest_list():
        kb = get_kb()
        digests = kb.get_recent_digests(limit=20)
        return render_template("digests.html", digests=digests)

    @app.route("/digest/<int:digest_id>")
    def digest_detail(digest_id):
        kb = get_kb()
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

        return render_template("digest.html",
                               digest=digest, items=items,
                               platform_filter=platform_filter,
                               sort_by=sort_by)

    @app.route("/digest/<int:digest_id>/like/<int:scanned_id>", methods=["POST"])
    def like_scanned(digest_id, scanned_id):
        kb = get_kb()
        scanned = kb.get_scanned_content(scanned_id)
        if scanned is None:
            flash("Scanned content not found.", "error")
            return redirect(url_for("digest_detail", digest_id=digest_id))

        notes = request.form.get("notes", "")
        liked_by = request.form.get("liked_by", "user")
        kb.add_inspiration(
            source_type="digest_like",
            body=scanned.body,
            url=scanned.url,
            author=scanned.author,
            notes=notes or None,
            liked_by=liked_by,
            scanned_content_id=scanned_id,
        )
        flash("Saved to inspiration.", "success")
        return redirect(url_for("digest_detail", digest_id=digest_id))

    # ── Inspiration ────────────────────────────────────────────

    @app.route("/inspiration")
    def inspiration():
        kb = get_kb()
        items = kb.get_recent_inspiration(limit=50)
        digest_likes = [i for i in items if i.source_type == "digest_like"]
        pasted_urls = [i for i in items if i.source_type == "pasted_url"]
        return render_template("inspiration.html",
                               digest_likes=digest_likes,
                               pasted_urls=pasted_urls)

    @app.route("/inspiration/add", methods=["POST"])
    def add_inspiration():
        kb = get_kb()
        url = request.form.get("url", "").strip()
        notes = request.form.get("notes", "").strip()
        liked_by = request.form.get("liked_by", "user")

        if not url:
            flash("URL is required.", "error")
            return redirect(url_for("inspiration"))

        # Fetch content from URL
        body = ""
        try:
            import requests as req
            from bs4 import BeautifulSoup
            resp = req.get(url, timeout=10, headers={
                "User-Agent": "Mozilla/5.0 (compatible; RCBot/1.0)"
            })
            if resp.ok:
                soup = BeautifulSoup(resp.text, "html.parser")
                title = soup.title.string if soup.title else ""
                for tag in soup.find_all(["script", "style", "nav", "footer", "header"]):
                    tag.decompose()
                body = soup.get_text(separator=" ", strip=True)[:500]
                if title:
                    body = f"{title}\n\n{body}"
        except Exception:
            body = url

        kb.add_inspiration(
            source_type="pasted_url",
            body=body,
            url=url,
            notes=notes or None,
            liked_by=liked_by,
        )
        flash("Inspiration saved.", "success")
        return redirect(url_for("inspiration"))

    # ── Calendar ───────────────────────────────────────────────

    @app.route("/calendar")
    def calendar():
        kb = get_kb()
        entries = kb.get_all_calendar_entries()
        return render_template("calendar.html", entries=entries)

    @app.route("/calendar/add", methods=["POST"])
    def calendar_add():
        kb = get_kb()
        scheduled_date = request.form.get("scheduled_date", "").strip()
        content_type = request.form.get("content_type", "").strip()
        platform = request.form.get("platform", "").strip()
        topic = request.form.get("topic", "").strip()
        principal = request.form.get("principal", "").strip()
        notes = request.form.get("notes", "").strip()

        if not scheduled_date or not content_type or not platform:
            flash("Date, content type, and platform are required.", "error")
            return redirect(url_for("calendar"))

        kb.add_calendar_entry(
            content_type=content_type,
            platform=platform,
            scheduled_date=scheduled_date,
            topic=topic or None,
            principal=principal or None,
            notes=notes or None,
        )
        flash("Calendar entry added.", "success")
        return redirect(url_for("calendar"))

    @app.route("/calendar/<int:entry_id>/edit", methods=["POST"])
    def calendar_edit(entry_id):
        kb = get_kb()
        entry = kb.get_calendar_entry(entry_id)
        if entry is None:
            flash("Calendar entry not found.", "error")
            return redirect(url_for("calendar"))

        updates = {}
        for field in ("content_type", "platform", "topic", "principal",
                      "scheduled_date", "notes"):
            val = request.form.get(field)
            if val is not None:
                updates[field] = val.strip() if val.strip() else None

        if updates:
            kb.update_calendar_entry(entry_id, **updates)
            flash(f"Calendar entry #{entry_id} updated.", "success")
        return redirect(url_for("calendar"))

    @app.route("/calendar/<int:entry_id>/delete", methods=["POST"])
    def calendar_delete(entry_id):
        kb = get_kb()
        entry = kb.get_calendar_entry(entry_id)
        if entry is None:
            flash("Calendar entry not found.", "error")
            return redirect(url_for("calendar"))
        kb.delete_calendar_entry(entry_id)
        flash(f"Calendar entry #{entry_id} deleted.", "success")
        return redirect(url_for("calendar"))

    @app.route("/calendar/<int:entry_id>/generate", methods=["POST"])
    def calendar_generate(entry_id):
        kb = get_kb()
        entry = kb.get_calendar_entry(entry_id)
        if entry is None:
            flash("Calendar entry not found.", "error")
            return redirect(url_for("calendar"))

        from src.db.models import ContentTask
        task = ContentTask(
            content_type=entry.content_type,
            platform=entry.platform,
            topic=entry.topic or "",
            principal=entry.principal,
            calendar_entry_id=entry.id,
        )
        pipeline = get_pipeline()
        content_id = pipeline.generate_and_queue(task)
        flash(f"Content generated from calendar entry #{entry_id}.", "success")
        return redirect(url_for("content_detail", content_id=content_id))

    # ── Generate Content ────────────────────────────────────────

    @app.route("/generate", methods=["GET"])
    def generate_form():
        return render_template("generate.html")

    @app.route("/generate", methods=["POST"])
    def generate_content_action():
        from src.db.models import ContentTask
        kb = get_kb()

        content_type = request.form.get("content_type", "").strip()
        platform = request.form.get("platform", "").strip()
        topic = request.form.get("topic", "").strip()
        principal = request.form.get("principal", "").strip()
        instructions = request.form.get("instructions", "").strip()

        if not content_type or not platform or not topic:
            flash("Content type, platform, and topic are required.", "error")
            return redirect(url_for("generate_form"))

        task = ContentTask(
            content_type=content_type,
            platform=platform,
            topic=topic,
            principal=principal or None,
            instructions=instructions or None,
        )
        pipeline = get_pipeline()
        content_id = pipeline.generate_and_queue(task)
        flash("Content generated successfully.", "success")
        return redirect(url_for("content_detail", content_id=content_id))

    # ── Knowledge Base ────────────────────────────────────────

    @app.route("/knowledge-base")
    def knowledge_base():
        kb = get_kb()
        firm_facts = kb.get_all_firm_facts()
        market_data = kb.get_all_market_data()
        data_sources = kb.get_all_data_sources()
        brand_rules = kb.get_all_brand_rules()
        return render_template("knowledge_base.html",
                               firm_facts=firm_facts,
                               market_data=market_data,
                               data_sources=data_sources,
                               brand_rules=brand_rules)

    # ── Monitored Accounts ─────────────────────────────────────

    @app.route("/accounts")
    def accounts_page():
        kb = get_kb()
        accounts = kb.get_all_monitored_accounts()
        return render_template("accounts.html", accounts=accounts)

    @app.route("/accounts/add", methods=["POST"])
    def add_account():
        kb = get_kb()
        platform = request.form.get("platform", "twitter")
        handle = request.form.get("handle", "").strip().lstrip("@")
        name = request.form.get("name", "").strip()
        category = request.form.get("category", "").strip()

        if not handle:
            flash("Handle is required.", "error")
            return redirect(url_for("accounts_page"))

        kb.add_monitored_account(
            platform=platform,
            handle=handle,
            name=name or None,
            category=category or None,
        )
        flash(f"Added @{handle} ({platform}).", "success")
        return redirect(url_for("accounts_page"))

    @app.route("/accounts/<int:account_id>/toggle", methods=["POST"])
    def toggle_account(account_id):
        kb = get_kb()
        account = kb.get_monitored_account(account_id)
        if account:
            kb.toggle_monitored_account(account_id, not account.active)
            status = "activated" if not account.active else "deactivated"
            flash(f"Account @{account.handle} {status}.", "success")
        return redirect(url_for("accounts_page"))

    # ── Manual Scan ────────────────────────────────────────────

    @app.route("/scan", methods=["POST"])
    def trigger_scan():
        from src.agents.scanner_agent import ContentScanner
        from src.integrations.claude_client import ClaudeClient

        kb = get_kb()
        claude = ClaudeClient()
        from src.integrations.twitter_api import TwitterAPI
        from src.integrations.linkedin_api import LinkedInAPI
        scanner = ContentScanner(claude, kb,
                                 TwitterAPI(mock_mode=True),
                                 LinkedInAPI(mock_mode=True))
        digest = scanner.run_scan(scan_type="manual")
        flash(f"Scan complete. Digest: {digest.title}", "success")
        return redirect(url_for("digest_detail", digest_id=digest.id))

    return app
