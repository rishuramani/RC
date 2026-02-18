"""CLI interface for the RC Marketing Bot."""

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from src.config import DB_PATH
from src.db.database import Database
from src.db.knowledge_base import KnowledgeBase
from src.integrations.claude_client import ClaudeClient
from src.pipeline.content_pipeline import ContentPipeline
from src.pipeline.publisher import Publisher
from src.integrations.linkedin_api import LinkedInAPI
from src.integrations.twitter_api import TwitterAPI

console = Console()


def _get_pipeline() -> ContentPipeline:
    """Initialize the full pipeline stack."""
    db = Database(str(DB_PATH))
    db.initialize()
    kb = KnowledgeBase(db)
    claude = ClaudeClient()
    return ContentPipeline(claude, kb)


def _get_kb() -> KnowledgeBase:
    """Get a knowledge base instance."""
    db = Database(str(DB_PATH))
    db.initialize()
    return KnowledgeBase(db)


@click.group()
def main():
    """RC Marketing Bot — AI-powered content for RC Investment Properties."""
    pass


# ── Generate Commands ───────────────────────────────────────────

@main.command()
@click.argument("content_type", type=click.Choice(
    ["linkedin", "tweet", "thread", "blog", "report"]
))
@click.option("--topic", "-t", required=True, help="Content topic")
@click.option("--principal", "-p", type=click.Choice(["michael", "bradley", "company"]),
              default="company", help="Who is this content for?")
@click.option("--instructions", "-i", default="", help="Additional instructions")
def generate(content_type, topic, principal, instructions):
    """Generate content for a specific platform."""
    from src.db.models import ContentTask

    type_map = {
        "linkedin": ("linkedin_post", "linkedin"),
        "tweet": ("tweet", "twitter"),
        "thread": ("tweet_thread", "twitter"),
        "blog": ("blog", "blog"),
        "report": ("market_report", "report"),
    }
    ct, platform = type_map[content_type]

    task = ContentTask(
        content_type=ct,
        platform=platform,
        topic=topic,
        principal=principal,
        instructions=instructions or None,
    )

    console.print(f"\n[bold]Generating {content_type}...[/bold]")

    pipeline = _get_pipeline()
    content_id = pipeline.generate_and_queue(task)
    content = pipeline.kb.get_content(content_id)

    console.print(Panel(
        content.body[:500] + ("..." if len(content.body) > 500 else ""),
        title=f"[green]Content #{content_id}[/green] ({content.status})",
        subtitle=f"{content.content_type} | {content.platform}",
    ))
    console.print(f"\nUse [bold]rc-bot review {content_id}[/bold] to see full content.")


@main.command()
@click.option("--days", "-d", default=7, help="Days ahead to plan")
@click.option("--instructions", "-i", default="", help="Planning instructions")
def plan(days, instructions):
    """Let the orchestrator plan upcoming content."""
    console.print(f"\n[bold]Planning content for the next {days} days...[/bold]")

    pipeline = _get_pipeline()
    content_ids = pipeline.plan_and_generate(days_ahead=days, instructions=instructions)

    console.print(f"\n[green]Generated {len(content_ids)} content pieces:[/green]")
    for cid in content_ids:
        content = pipeline.kb.get_content(cid)
        console.print(f"  #{cid}: {content.content_type} ({content.status}) — "
                      f"{content.body[:80]}...")


@main.command()
def suggest():
    """Get topic suggestions based on market data."""
    pipeline = _get_pipeline()
    suggestions = pipeline.orchestrator.suggest_topics()

    if not suggestions:
        console.print("[yellow]No suggestions available. Add market data first.[/yellow]")
        return

    console.print("\n[bold]Topic Suggestions:[/bold]\n")
    for i, s in enumerate(suggestions, 1):
        console.print(f"  {i}. [bold]{s['topic']}[/bold]")
        console.print(f"     Reason: {s['reason']}")
        console.print(f"     Platforms: {', '.join(s.get('platforms', []))}\n")


# ── Review Commands ─────────────────────────────────────────────

@main.command()
@click.argument("content_id", required=False, type=int)
def review(content_id):
    """Review queued content. Pass an ID to see specific content."""
    pipeline = _get_pipeline()

    if content_id:
        content = pipeline.kb.get_content(content_id)
        if content is None:
            console.print(f"[red]Content #{content_id} not found.[/red]")
            return

        console.print(Panel(
            content.body,
            title=f"[bold]Content #{content.id}[/bold]",
            subtitle=f"{content.content_type} | {content.platform} | "
                     f"{content.principal or 'company'} | {content.status}",
        ))
        if content.title:
            console.print(f"  Title: {content.title}")
        console.print(f"  Topic: {content.topic}")
        console.print(f"  Created: {content.created_at}")
        return

    queue = pipeline.get_review_queue()
    if not queue:
        console.print("[green]Review queue is empty.[/green]")
        return

    table = Table(title="Review Queue")
    table.add_column("ID", style="bold")
    table.add_column("Type")
    table.add_column("Platform")
    table.add_column("Principal")
    table.add_column("Status")
    table.add_column("Compliant")
    table.add_column("Preview", max_width=60)

    for item in queue:
        compliant = "[green]Yes[/green]" if item["is_compliant"] else "[red]No[/red]"
        table.add_row(
            str(item["id"]),
            item["type"],
            item["platform"],
            item["principal"] or "company",
            item["status"],
            compliant,
            item["preview"][:60] + "...",
        )

    console.print(table)


@main.command()
@click.argument("content_id", type=int)
def approve(content_id):
    """Approve content for publishing."""
    pipeline = _get_pipeline()
    try:
        pipeline.approve(content_id)
        console.print(f"[green]Content #{content_id} approved.[/green]")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")


@main.command()
@click.argument("content_id", type=int)
@click.option("--reason", "-r", default="", help="Rejection reason")
def reject(content_id, reason):
    """Reject content."""
    pipeline = _get_pipeline()
    try:
        pipeline.reject(content_id, reason=reason)
        console.print(f"[yellow]Content #{content_id} rejected.[/yellow]")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")


# ── Publish Commands ────────────────────────────────────────────

@main.command()
@click.argument("content_id", type=int)
@click.option("--dry-run", is_flag=True, help="Preview without publishing")
@click.option("--mock", is_flag=True, help="Use mock APIs (for testing)")
def publish(content_id, dry_run, mock):
    """Publish approved content to the target platform."""
    pipeline = _get_pipeline()

    if dry_run:
        try:
            result = pipeline.publish(content_id, dry_run=True)
            console.print(Panel(
                result.get("body_preview", ""),
                title=f"[yellow]DRY RUN — Content #{content_id}[/yellow]",
                subtitle=f"Platform: {result.get('platform', 'unknown')}",
            ))
        except ValueError as e:
            console.print(f"[red]Error: {e}[/red]")
        return

    publisher = Publisher(
        linkedin_api=LinkedInAPI(mock_mode=mock),
        twitter_api=TwitterAPI(mock_mode=mock),
    )

    try:
        result = pipeline.publish(content_id, publisher=publisher)
        if result.get("success"):
            console.print(
                f"[green]Published! Post ID: {result.get('post_id', 'N/A')}[/green]"
            )
        else:
            console.print(f"[red]Failed: {result.get('error', 'Unknown error')}[/red]")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")


# ── Knowledge Base Commands ─────────────────────────────────────

@main.group()
def kb():
    """Knowledge base management commands."""
    pass


@kb.command("add-market")
@click.option("--market", "-m", required=True, help="Market name (houston, phoenix)")
@click.option("--metric", required=True, help="Metric name (occupancy, rent_growth)")
@click.option("--value", "-v", required=True, help="Metric value")
@click.option("--period", "-p", default="", help="Time period (Q4 2025, 2024)")
@click.option("--source", "-s", default="", help="Data source")
def kb_add_market(market, metric, value, period, source):
    """Add market data to the knowledge base."""
    knowledge_base = _get_kb()
    mid = knowledge_base.add_market_data(
        market, metric, value, period or None, source or None
    )
    console.print(f"[green]Added market data #{mid}: {market} {metric} = {value}[/green]")


@kb.command("search")
@click.argument("query")
def kb_search(query):
    """Search the knowledge base."""
    knowledge_base = _get_kb()

    facts = knowledge_base.search_firm_facts(query)
    market = knowledge_base.search_market_data(query)
    content = knowledge_base.search_content(query)

    if facts:
        console.print("\n[bold]Firm Facts:[/bold]")
        for f in facts:
            console.print(f"  [{f.category}] {f.key}: {f.value}")

    if market:
        console.print("\n[bold]Market Data:[/bold]")
        for m in market:
            console.print(f"  {m.market.title()} {m.metric}: {m.value} "
                          f"({m.period or 'N/A'})")

    if content:
        console.print("\n[bold]Content:[/bold]")
        for c in content:
            console.print(f"  #{c.id} [{c.content_type}] {c.body[:80]}...")

    if not facts and not market and not content:
        console.print(f"[yellow]No results for '{query}'[/yellow]")


@kb.command("seed")
def kb_seed():
    """Seed the knowledge base from existing RC content."""
    from seeds.seed_knowledge_base import seed_all
    knowledge_base = _get_kb()
    seed_all(knowledge_base)
    console.print("[green]Knowledge base seeded successfully.[/green]")


@kb.command("stats")
def kb_stats():
    """Show knowledge base statistics."""
    knowledge_base = _get_kb()

    facts = len(knowledge_base.get_firm_facts_by_category("track_record")) + \
            len(knowledge_base.get_firm_facts_by_category("portfolio")) + \
            len(knowledge_base.get_firm_facts_by_category("thesis")) + \
            len(knowledge_base.get_firm_facts_by_category("advantage")) + \
            len(knowledge_base.get_firm_facts_by_category("terms"))
    rules = len(knowledge_base.get_all_brand_rules())
    sources = len(knowledge_base.get_all_data_sources())
    content_stats = knowledge_base.get_content_stats()

    table = Table(title="Knowledge Base Statistics")
    table.add_column("Category", style="bold")
    table.add_column("Count")

    table.add_row("Firm Facts", str(facts))
    table.add_row("Brand Rules", str(rules))
    table.add_row("Data Sources", str(sources))
    table.add_row("Total Content", str(content_stats["total"]))
    for status, count in content_stats.get("by_status", {}).items():
        table.add_row(f"  Content ({status})", str(count))

    console.print(table)


# ── Calendar Commands ───────────────────────────────────────────

@main.command()
@click.option("--week", is_flag=True, help="Show this week only")
def calendar(week):
    """View the content calendar."""
    from datetime import datetime, timedelta

    pipeline = _get_pipeline()
    status = pipeline.orchestrator.review_calendar()

    console.print(f"\n[bold]Content Calendar[/bold]")
    console.print(f"  Pending: {status['total_pending']}")
    console.print(f"  Upcoming (7 days): {status['upcoming_7_days']}")
    console.print(f"  Overdue: {status['overdue']}")

    if status["entries"]:
        table = Table(title="Upcoming Entries")
        table.add_column("ID")
        table.add_column("Date")
        table.add_column("Type")
        table.add_column("Platform")
        table.add_column("Topic")
        table.add_column("Status")

        for e in status["entries"]:
            table.add_row(
                str(e["id"]), str(e["date"]), e["type"],
                e["platform"], e.get("topic", "—"), e["status"],
            )
        console.print(table)


# ── Metrics Commands ────────────────────────────────────────────

@main.command()
@click.argument("content_id", required=False, type=int)
def metrics(content_id):
    """View content performance metrics."""
    knowledge_base = _get_kb()

    if content_id:
        latest = knowledge_base.get_latest_metrics(content_id)
        if latest is None:
            console.print(f"[yellow]No metrics for content #{content_id}.[/yellow]")
            return
        console.print(Panel(
            f"Impressions: {latest.impressions}\n"
            f"Likes: {latest.likes}\n"
            f"Comments: {latest.comments}\n"
            f"Shares: {latest.shares}\n"
            f"Clicks: {latest.clicks}",
            title=f"Metrics for Content #{content_id}",
        ))
        return

    stats = knowledge_base.get_content_stats()
    console.print(f"\n[bold]Content Performance Summary[/bold]")
    console.print(f"  Total content: {stats['total']}")
    for status, count in stats.get("by_status", {}).items():
        console.print(f"  {status.title()}: {count}")


# ── Scanner Commands ───────────────────────────────────────────

@main.command()
@click.option("--twitter-only", is_flag=True, help="Only scan Twitter")
def scan(twitter_only):
    """Run a content scan of industry sources."""
    from src.agents.scanner_agent import ContentScanner
    from src.integrations.claude_client import ClaudeClient

    console.print("\n[bold]Running content scan...[/bold]")

    kb = _get_kb()
    claude = ClaudeClient()
    twitter = TwitterAPI(mock_mode=True)
    linkedin = LinkedInAPI(mock_mode=True)
    scanner = ContentScanner(claude, kb, twitter, linkedin)

    digest = scanner.run_scan(scan_type="manual", twitter_only=twitter_only)

    console.print(Panel(
        digest.summary or "No summary available.",
        title=f"[green]{digest.title}[/green]",
        subtitle=f"Digest #{digest.id} ({digest.scan_type})",
    ))
    console.print(f"\nUse [bold]rc-bot digest {digest.id}[/bold] to browse scanned posts.")


@main.command()
@click.argument("digest_id", required=False, type=int)
def digest(digest_id):
    """View digests. Pass an ID to see a specific digest."""
    kb = _get_kb()

    if digest_id:
        d = kb.get_digest(digest_id)
        if d is None:
            console.print(f"[red]Digest #{digest_id} not found.[/red]")
            return

        console.print(Panel(
            d.summary or "No summary.",
            title=f"[bold]{d.title}[/bold]",
            subtitle=f"Type: {d.scan_type} | Created: {d.created_at}",
        ))

        items = kb.get_scanned_content_by_digest(digest_id)
        if items:
            table = Table(title="Scanned Posts")
            table.add_column("ID")
            table.add_column("Platform")
            table.add_column("Author")
            table.add_column("Engagement")
            table.add_column("Tags")
            table.add_column("Preview", max_width=50)

            for item in items:
                table.add_row(
                    str(item.id), item.platform,
                    item.author or "—",
                    str(item.engagement_score),
                    item.topic_tags or "—",
                    item.body[:50] + "...",
                )
            console.print(table)
        return

    digests = kb.get_recent_digests(limit=10)
    if not digests:
        console.print("[yellow]No digests found. Run 'rc-bot scan' first.[/yellow]")
        return

    table = Table(title="Recent Digests")
    table.add_column("ID", style="bold")
    table.add_column("Title")
    table.add_column("Type")
    table.add_column("Created")

    for d in digests:
        table.add_row(
            str(d.id), d.title or "—", d.scan_type,
            str(d.created_at or "—"),
        )
    console.print(table)


# ── Inspiration Commands ───────────────────────────────────────

@main.command()
@click.option("--url", "-u", default="", help="URL to save as inspiration")
@click.option("--notes", "-n", default="", help="Notes about why you liked it")
@click.option("--list", "list_all", is_flag=True, help="List recent inspiration")
@click.option("--user", default="", help="Filter by user (michael, bradley)")
def inspire(url, notes, list_all, user):
    """Save inspiration or browse liked content."""
    kb = _get_kb()

    if list_all or (not url):
        if user:
            items = kb.get_inspiration_by_user(user)
        else:
            items = kb.get_recent_inspiration(limit=20)

        if not items:
            console.print("[yellow]No inspiration saved yet.[/yellow]")
            return

        table = Table(title="Inspiration")
        table.add_column("ID")
        table.add_column("Type")
        table.add_column("Author")
        table.add_column("By")
        table.add_column("Preview", max_width=50)
        table.add_column("Notes", max_width=30)

        for item in items:
            table.add_row(
                str(item.id), item.source_type,
                item.author or "—", item.liked_by or "—",
                (item.body or "")[:50] + ("..." if item.body and len(item.body) > 50 else ""),
                item.notes or "—",
            )
        console.print(table)
        return

    if url:
        # Fetch content from URL
        body = ""
        try:
            import requests
            from bs4 import BeautifulSoup
            resp = requests.get(url, timeout=10, headers={
                "User-Agent": "Mozilla/5.0 (compatible; RCBot/1.0)"
            })
            if resp.ok:
                soup = BeautifulSoup(resp.text, "html.parser")
                # Get page title and main text
                title = soup.title.string if soup.title else ""
                # Extract text from article or main content
                for tag in soup.find_all(["script", "style", "nav", "footer", "header"]):
                    tag.decompose()
                body = soup.get_text(separator=" ", strip=True)[:500]
                if title:
                    body = f"{title}\n\n{body}"
        except Exception as e:
            console.print(f"[yellow]Could not fetch URL content: {e}[/yellow]")
            body = url

        insp_id = kb.add_inspiration(
            source_type="pasted_url",
            body=body,
            url=url,
            notes=notes or None,
            liked_by="user",
        )
        console.print(f"[green]Saved inspiration #{insp_id} from URL.[/green]")


# ── Monitored Accounts Commands ────────────────────────────────

@main.group()
def accounts():
    """Manage monitored accounts."""
    pass


@accounts.command("list")
@click.option("--all", "show_all", is_flag=True, help="Include inactive accounts")
def accounts_list(show_all):
    """List monitored accounts."""
    kb = _get_kb()
    items = kb.get_all_monitored_accounts() if show_all else kb.get_monitored_accounts()

    if not items:
        console.print("[yellow]No monitored accounts.[/yellow]")
        return

    table = Table(title="Monitored Accounts")
    table.add_column("ID")
    table.add_column("Platform")
    table.add_column("Handle")
    table.add_column("Name")
    table.add_column("Category")
    table.add_column("Active")

    for a in items:
        active = "[green]Yes[/green]" if a.active else "[red]No[/red]"
        table.add_row(
            str(a.id), a.platform, a.handle,
            a.name or "—", a.category or "—", active,
        )
    console.print(table)


@accounts.command("add")
@click.option("--platform", "-p", required=True,
              type=click.Choice(["twitter", "linkedin"]),
              help="Platform")
@click.option("--handle", "-h", required=True, help="Account handle")
@click.option("--name", "-n", default="", help="Display name")
@click.option("--category", "-c", default="",
              type=click.Choice(["competitor", "analyst", "influencer", "media", ""],
                                case_sensitive=False),
              help="Account category")
def accounts_add(platform, handle, name, category):
    """Add a monitored account."""
    kb = _get_kb()
    aid = kb.add_monitored_account(
        platform=platform,
        handle=handle.lstrip("@"),
        name=name or None,
        category=category or None,
    )
    console.print(f"[green]Added monitored account #{aid}: @{handle} ({platform})[/green]")


@accounts.command("remove")
@click.argument("account_id", type=int)
def accounts_remove(account_id):
    """Remove a monitored account."""
    kb = _get_kb()
    account = kb.get_monitored_account(account_id)
    if account is None:
        console.print(f"[red]Account #{account_id} not found.[/red]")
        return
    kb.delete_monitored_account(account_id)
    console.print(f"[yellow]Removed account #{account_id} (@{account.handle}).[/yellow]")


# ── Web GUI Command ────────────────────────────────────────────

@main.command()
@click.option("--port", "-p", default=5000, help="Port number")
@click.option("--host", "-h", default="127.0.0.1", help="Host to bind to")
def web(port, host):
    """Start the Flask web GUI."""
    from src.web.app import create_app
    app = create_app()
    console.print(f"\n[bold]Starting RC Marketing Bot GUI...[/bold]")
    console.print(f"  Open [link=http://{host}:{port}]http://{host}:{port}[/link] in your browser.\n")
    app.run(host=host, port=port, debug=True)


if __name__ == "__main__":
    main()
