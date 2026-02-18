"""CRUD operations for the RC Marketing Bot knowledge base."""

from datetime import datetime, date
from typing import Optional

from src.db.database import Database
from src.db.models import (
    FirmFact, MarketData, BrandRule, Content,
    ContentMetrics, ContentCalendarEntry, DataSource,
    ScannedContent, Digest, Inspiration, MonitoredAccount,
)


class KnowledgeBase:
    """Interface to all knowledge base tables."""

    def __init__(self, db: Database):
        self.db = db

    # ── Firm Facts ──────────────────────────────────────────────

    def add_firm_fact(self, category: str, key: str, value: str,
                      source: Optional[str] = None) -> int:
        cursor = self.db.execute(
            "INSERT INTO firm_facts (category, key, value, source) VALUES (?, ?, ?, ?)",
            (category, key, value, source),
        )
        self.db.commit()
        return cursor.lastrowid

    def get_firm_fact(self, fact_id: int) -> Optional[FirmFact]:
        row = self.db.fetchone("SELECT * FROM firm_facts WHERE id = ?", (fact_id,))
        return self._row_to_firm_fact(row) if row else None

    def get_firm_facts_by_category(self, category: str) -> list[FirmFact]:
        rows = self.db.fetchall(
            "SELECT * FROM firm_facts WHERE category = ? ORDER BY key", (category,)
        )
        return [self._row_to_firm_fact(r) for r in rows]

    def get_all_firm_facts(self) -> list[FirmFact]:
        rows = self.db.fetchall("SELECT * FROM firm_facts ORDER BY category, key")
        return [self._row_to_firm_fact(r) for r in rows]

    def search_firm_facts(self, query: str) -> list[FirmFact]:
        rows = self.db.fetchall(
            "SELECT * FROM firm_facts WHERE key LIKE ? OR value LIKE ?",
            (f"%{query}%", f"%{query}%"),
        )
        return [self._row_to_firm_fact(r) for r in rows]

    def update_firm_fact(self, fact_id: int, **kwargs) -> bool:
        if not kwargs:
            return False
        kwargs["updated_at"] = datetime.now().isoformat()
        sets = ", ".join(f"{k} = ?" for k in kwargs)
        values = list(kwargs.values()) + [fact_id]
        self.db.execute(f"UPDATE firm_facts SET {sets} WHERE id = ?", tuple(values))
        self.db.commit()
        return True

    def delete_firm_fact(self, fact_id: int) -> bool:
        self.db.execute("DELETE FROM firm_facts WHERE id = ?", (fact_id,))
        self.db.commit()
        return True

    def _row_to_firm_fact(self, row) -> FirmFact:
        return FirmFact(
            id=row["id"], category=row["category"], key=row["key"],
            value=row["value"], source=row["source"],
            created_at=row["created_at"], updated_at=row["updated_at"],
        )

    # ── Market Data ─────────────────────────────────────────────

    def add_market_data(self, market: str, metric: str, value: str,
                        period: Optional[str] = None,
                        source: Optional[str] = None) -> int:
        cursor = self.db.execute(
            "INSERT INTO market_data (market, metric, value, period, source) "
            "VALUES (?, ?, ?, ?, ?)",
            (market, metric, value, period, source),
        )
        self.db.commit()
        return cursor.lastrowid

    def get_market_data(self, data_id: int) -> Optional[MarketData]:
        row = self.db.fetchone("SELECT * FROM market_data WHERE id = ?", (data_id,))
        return self._row_to_market_data(row) if row else None

    def get_market_data_by_market(self, market: str) -> list[MarketData]:
        rows = self.db.fetchall(
            "SELECT * FROM market_data WHERE market = ? ORDER BY period DESC",
            (market,),
        )
        return [self._row_to_market_data(r) for r in rows]

    def get_market_data_by_metric(self, metric: str,
                                   market: Optional[str] = None) -> list[MarketData]:
        if market:
            rows = self.db.fetchall(
                "SELECT * FROM market_data WHERE metric = ? AND market = ? "
                "ORDER BY period DESC",
                (metric, market),
            )
        else:
            rows = self.db.fetchall(
                "SELECT * FROM market_data WHERE metric = ? ORDER BY period DESC",
                (metric,),
            )
        return [self._row_to_market_data(r) for r in rows]

    def get_all_market_data(self) -> list[MarketData]:
        rows = self.db.fetchall("SELECT * FROM market_data ORDER BY market, metric")
        return [self._row_to_market_data(r) for r in rows]

    def search_market_data(self, query: str) -> list[MarketData]:
        rows = self.db.fetchall(
            "SELECT * FROM market_data WHERE metric LIKE ? OR value LIKE ? "
            "OR market LIKE ?",
            (f"%{query}%", f"%{query}%", f"%{query}%"),
        )
        return [self._row_to_market_data(r) for r in rows]

    def delete_market_data(self, data_id: int) -> bool:
        self.db.execute("DELETE FROM market_data WHERE id = ?", (data_id,))
        self.db.commit()
        return True

    def _row_to_market_data(self, row) -> MarketData:
        return MarketData(
            id=row["id"], market=row["market"], metric=row["metric"],
            value=row["value"], period=row["period"], source=row["source"],
            created_at=row["created_at"],
        )

    # ── Brand Rules ─────────────────────────────────────────────

    def add_brand_rule(self, rule_type: str, rule: str,
                       example: Optional[str] = None) -> int:
        cursor = self.db.execute(
            "INSERT INTO brand_rules (rule_type, rule, example) VALUES (?, ?, ?)",
            (rule_type, rule, example),
        )
        self.db.commit()
        return cursor.lastrowid

    def get_brand_rule(self, rule_id: int) -> Optional[BrandRule]:
        row = self.db.fetchone("SELECT * FROM brand_rules WHERE id = ?", (rule_id,))
        return self._row_to_brand_rule(row) if row else None

    def get_brand_rules_by_type(self, rule_type: str) -> list[BrandRule]:
        rows = self.db.fetchall(
            "SELECT * FROM brand_rules WHERE rule_type = ?", (rule_type,)
        )
        return [self._row_to_brand_rule(r) for r in rows]

    def get_all_brand_rules(self) -> list[BrandRule]:
        rows = self.db.fetchall("SELECT * FROM brand_rules ORDER BY rule_type")
        return [self._row_to_brand_rule(r) for r in rows]

    def delete_brand_rule(self, rule_id: int) -> bool:
        self.db.execute("DELETE FROM brand_rules WHERE id = ?", (rule_id,))
        self.db.commit()
        return True

    def _row_to_brand_rule(self, row) -> BrandRule:
        return BrandRule(
            id=row["id"], rule_type=row["rule_type"],
            rule=row["rule"], example=row["example"],
            created_at=row["created_at"],
        )

    # ── Content ─────────────────────────────────────────────────

    def add_content(self, content_type: str, platform: str, body: str,
                    principal: Optional[str] = None, title: Optional[str] = None,
                    topic: Optional[str] = None, status: str = "draft",
                    scheduled_for: Optional[str] = None) -> int:
        cursor = self.db.execute(
            "INSERT INTO content (content_type, platform, principal, title, body, "
            "topic, status, scheduled_for) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (content_type, platform, principal, title, body, topic, status,
             scheduled_for),
        )
        self.db.commit()
        return cursor.lastrowid

    def get_content(self, content_id: int) -> Optional[Content]:
        row = self.db.fetchone("SELECT * FROM content WHERE id = ?", (content_id,))
        return self._row_to_content(row) if row else None

    def get_content_by_status(self, status: str) -> list[Content]:
        rows = self.db.fetchall(
            "SELECT * FROM content WHERE status = ? ORDER BY created_at DESC",
            (status,),
        )
        return [self._row_to_content(r) for r in rows]

    def get_content_by_platform(self, platform: str,
                                 limit: int = 20) -> list[Content]:
        rows = self.db.fetchall(
            "SELECT * FROM content WHERE platform = ? ORDER BY created_at DESC "
            "LIMIT ?",
            (platform, limit),
        )
        return [self._row_to_content(r) for r in rows]

    def get_recent_content(self, limit: int = 20) -> list[Content]:
        rows = self.db.fetchall(
            "SELECT * FROM content ORDER BY created_at DESC LIMIT ?", (limit,)
        )
        return [self._row_to_content(r) for r in rows]

    def update_content_status(self, content_id: int, status: str) -> bool:
        now = datetime.now().isoformat()
        extra = ""
        params = [status, now, content_id]
        if status == "published":
            extra = ", published_at = ?"
            params = [status, now, now, content_id]
        self.db.execute(
            f"UPDATE content SET status = ?, updated_at = ?{extra} WHERE id = ?",
            tuple(params),
        )
        self.db.commit()
        return True

    def update_content_body(self, content_id: int, body: str,
                            title: Optional[str] = None) -> bool:
        now = datetime.now().isoformat()
        if title is not None:
            self.db.execute(
                "UPDATE content SET body = ?, title = ?, updated_at = ? WHERE id = ?",
                (body, title, now, content_id),
            )
        else:
            self.db.execute(
                "UPDATE content SET body = ?, updated_at = ? WHERE id = ?",
                (body, now, content_id),
            )
        self.db.commit()
        return True

    def set_platform_post_id(self, content_id: int, platform_post_id: str) -> bool:
        self.db.execute(
            "UPDATE content SET platform_post_id = ? WHERE id = ?",
            (platform_post_id, content_id),
        )
        self.db.commit()
        return True

    def delete_content(self, content_id: int) -> bool:
        self.db.execute("DELETE FROM content_metrics WHERE content_id = ?",
                        (content_id,))
        self.db.execute("DELETE FROM content WHERE id = ?", (content_id,))
        self.db.commit()
        return True

    def search_content(self, query: str) -> list[Content]:
        rows = self.db.fetchall(
            "SELECT * FROM content WHERE body LIKE ? OR title LIKE ? OR topic LIKE ?",
            (f"%{query}%", f"%{query}%", f"%{query}%"),
        )
        return [self._row_to_content(r) for r in rows]

    def _row_to_content(self, row) -> Content:
        return Content(
            id=row["id"], content_type=row["content_type"],
            platform=row["platform"], principal=row["principal"],
            title=row["title"], body=row["body"], topic=row["topic"],
            status=row["status"], scheduled_for=row["scheduled_for"],
            published_at=row["published_at"],
            platform_post_id=row["platform_post_id"],
            created_at=row["created_at"], updated_at=row["updated_at"],
        )

    # ── Content Metrics ─────────────────────────────────────────

    def add_content_metrics(self, content_id: int, impressions: int = 0,
                            likes: int = 0, comments: int = 0,
                            shares: int = 0, clicks: int = 0) -> int:
        cursor = self.db.execute(
            "INSERT INTO content_metrics (content_id, impressions, likes, "
            "comments, shares, clicks) VALUES (?, ?, ?, ?, ?, ?)",
            (content_id, impressions, likes, comments, shares, clicks),
        )
        self.db.commit()
        return cursor.lastrowid

    def get_content_metrics(self, content_id: int) -> list[ContentMetrics]:
        rows = self.db.fetchall(
            "SELECT * FROM content_metrics WHERE content_id = ? "
            "ORDER BY id DESC",
            (content_id,),
        )
        return [self._row_to_content_metrics(r) for r in rows]

    def get_latest_metrics(self, content_id: int) -> Optional[ContentMetrics]:
        row = self.db.fetchone(
            "SELECT * FROM content_metrics WHERE content_id = ? "
            "ORDER BY id DESC LIMIT 1",
            (content_id,),
        )
        return self._row_to_content_metrics(row) if row else None

    def _row_to_content_metrics(self, row) -> ContentMetrics:
        return ContentMetrics(
            id=row["id"], content_id=row["content_id"],
            impressions=row["impressions"], likes=row["likes"],
            comments=row["comments"], shares=row["shares"],
            clicks=row["clicks"], fetched_at=row["fetched_at"],
        )

    # ── Content Calendar ────────────────────────────────────────

    def add_calendar_entry(self, content_type: str, platform: str,
                           scheduled_date: str, topic: Optional[str] = None,
                           principal: Optional[str] = None,
                           notes: Optional[str] = None) -> int:
        cursor = self.db.execute(
            "INSERT INTO content_calendar (content_type, platform, topic, "
            "principal, scheduled_date, notes) VALUES (?, ?, ?, ?, ?, ?)",
            (content_type, platform, topic, principal, scheduled_date, notes),
        )
        self.db.commit()
        return cursor.lastrowid

    def get_calendar_entry(self, entry_id: int) -> Optional[ContentCalendarEntry]:
        row = self.db.fetchone(
            "SELECT * FROM content_calendar WHERE id = ?", (entry_id,)
        )
        return self._row_to_calendar_entry(row) if row else None

    def get_calendar_entries_by_date_range(
        self, start_date: str, end_date: str
    ) -> list[ContentCalendarEntry]:
        rows = self.db.fetchall(
            "SELECT * FROM content_calendar WHERE scheduled_date BETWEEN ? AND ? "
            "ORDER BY scheduled_date",
            (start_date, end_date),
        )
        return [self._row_to_calendar_entry(r) for r in rows]

    def get_pending_calendar_entries(self) -> list[ContentCalendarEntry]:
        rows = self.db.fetchall(
            "SELECT * FROM content_calendar WHERE status = 'planned' "
            "ORDER BY scheduled_date"
        )
        return [self._row_to_calendar_entry(r) for r in rows]

    def update_calendar_entry_status(self, entry_id: int, status: str,
                                      content_id: Optional[int] = None) -> bool:
        if content_id is not None:
            self.db.execute(
                "UPDATE content_calendar SET status = ?, content_id = ? WHERE id = ?",
                (status, content_id, entry_id),
            )
        else:
            self.db.execute(
                "UPDATE content_calendar SET status = ? WHERE id = ?",
                (status, entry_id),
            )
        self.db.commit()
        return True

    def update_calendar_entry(self, entry_id: int, **kwargs) -> bool:
        if not kwargs:
            return False
        allowed = {"content_type", "platform", "topic", "principal",
                   "scheduled_date", "notes", "status", "content_id"}
        filtered = {k: v for k, v in kwargs.items() if k in allowed}
        if not filtered:
            return False
        sets = ", ".join(f"{k} = ?" for k in filtered)
        values = list(filtered.values()) + [entry_id]
        self.db.execute(
            f"UPDATE content_calendar SET {sets} WHERE id = ?", tuple(values)
        )
        self.db.commit()
        return True

    def delete_calendar_entry(self, entry_id: int) -> bool:
        self.db.execute("DELETE FROM content_calendar WHERE id = ?", (entry_id,))
        self.db.commit()
        return True

    def _row_to_calendar_entry(self, row) -> ContentCalendarEntry:
        return ContentCalendarEntry(
            id=row["id"], content_type=row["content_type"],
            platform=row["platform"], topic=row["topic"],
            principal=row["principal"], scheduled_date=row["scheduled_date"],
            status=row["status"], content_id=row["content_id"],
            notes=row["notes"], created_at=row["created_at"],
        )

    def get_all_calendar_entries(self) -> list[ContentCalendarEntry]:
        rows = self.db.fetchall(
            "SELECT * FROM content_calendar ORDER BY scheduled_date"
        )
        return [self._row_to_calendar_entry(r) for r in rows]

    # ── Data Sources ────────────────────────────────────────────

    def add_data_source(self, name: str, url: Optional[str] = None,
                        frequency: Optional[str] = None,
                        notes: Optional[str] = None) -> int:
        cursor = self.db.execute(
            "INSERT INTO data_sources (name, url, frequency, notes) "
            "VALUES (?, ?, ?, ?)",
            (name, url, frequency, notes),
        )
        self.db.commit()
        return cursor.lastrowid

    def get_data_source(self, source_id: int) -> Optional[DataSource]:
        row = self.db.fetchone(
            "SELECT * FROM data_sources WHERE id = ?", (source_id,)
        )
        return self._row_to_data_source(row) if row else None

    def get_all_data_sources(self) -> list[DataSource]:
        rows = self.db.fetchall("SELECT * FROM data_sources ORDER BY name")
        return [self._row_to_data_source(r) for r in rows]

    def update_data_source_checked(self, source_id: int,
                                    next_check: Optional[str] = None) -> bool:
        now = datetime.now().isoformat()
        self.db.execute(
            "UPDATE data_sources SET last_checked = ?, next_check = ? WHERE id = ?",
            (now, next_check, source_id),
        )
        self.db.commit()
        return True

    def delete_data_source(self, source_id: int) -> bool:
        self.db.execute("DELETE FROM data_sources WHERE id = ?", (source_id,))
        self.db.commit()
        return True

    def _row_to_data_source(self, row) -> DataSource:
        return DataSource(
            id=row["id"], name=row["name"], url=row["url"],
            frequency=row["frequency"], last_checked=row["last_checked"],
            next_check=row["next_check"], notes=row["notes"],
        )

    # ── Scanned Content ──────────────────────────────────────────

    def add_scanned_content(self, platform: str, body: str,
                            external_id: Optional[str] = None,
                            author: Optional[str] = None,
                            author_url: Optional[str] = None,
                            url: Optional[str] = None,
                            engagement_score: int = 0,
                            topic_tags: Optional[str] = None,
                            digest_id: Optional[int] = None) -> int:
        cursor = self.db.execute(
            "INSERT INTO scanned_content (platform, body, external_id, author, "
            "author_url, url, engagement_score, topic_tags, digest_id) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (platform, body, external_id, author, author_url, url,
             engagement_score, topic_tags, digest_id),
        )
        self.db.commit()
        return cursor.lastrowid

    def get_scanned_content(self, content_id: int) -> Optional[ScannedContent]:
        row = self.db.fetchone(
            "SELECT * FROM scanned_content WHERE id = ?", (content_id,)
        )
        return self._row_to_scanned_content(row) if row else None

    def get_scanned_content_by_digest(self, digest_id: int) -> list[ScannedContent]:
        rows = self.db.fetchall(
            "SELECT * FROM scanned_content WHERE digest_id = ? "
            "ORDER BY engagement_score DESC",
            (digest_id,),
        )
        return [self._row_to_scanned_content(r) for r in rows]

    def search_scanned_content(self, query: str) -> list[ScannedContent]:
        rows = self.db.fetchall(
            "SELECT * FROM scanned_content WHERE body LIKE ? OR author LIKE ? "
            "OR topic_tags LIKE ? ORDER BY scanned_at DESC",
            (f"%{query}%", f"%{query}%", f"%{query}%"),
        )
        return [self._row_to_scanned_content(r) for r in rows]

    def scanned_content_exists(self, external_id: str, platform: str) -> bool:
        row = self.db.fetchone(
            "SELECT id FROM scanned_content WHERE external_id = ? AND platform = ?",
            (external_id, platform),
        )
        return row is not None

    def _row_to_scanned_content(self, row) -> ScannedContent:
        return ScannedContent(
            id=row["id"], platform=row["platform"],
            external_id=row["external_id"], author=row["author"],
            author_url=row["author_url"], body=row["body"],
            url=row["url"], engagement_score=row["engagement_score"],
            topic_tags=row["topic_tags"], scanned_at=row["scanned_at"],
            digest_id=row["digest_id"],
        )

    # ── Digests ──────────────────────────────────────────────────

    def add_digest(self, title: Optional[str] = None,
                   summary: Optional[str] = None,
                   scan_type: str = "scheduled") -> int:
        cursor = self.db.execute(
            "INSERT INTO digests (title, summary, scan_type) VALUES (?, ?, ?)",
            (title, summary, scan_type),
        )
        self.db.commit()
        return cursor.lastrowid

    def get_digest(self, digest_id: int) -> Optional[Digest]:
        row = self.db.fetchone(
            "SELECT * FROM digests WHERE id = ?", (digest_id,)
        )
        return self._row_to_digest(row) if row else None

    def get_recent_digests(self, limit: int = 10) -> list[Digest]:
        rows = self.db.fetchall(
            "SELECT * FROM digests ORDER BY created_at DESC LIMIT ?", (limit,)
        )
        return [self._row_to_digest(r) for r in rows]

    def update_digest(self, digest_id: int, **kwargs) -> bool:
        if not kwargs:
            return False
        sets = ", ".join(f"{k} = ?" for k in kwargs)
        values = list(kwargs.values()) + [digest_id]
        self.db.execute(
            f"UPDATE digests SET {sets} WHERE id = ?", tuple(values)
        )
        self.db.commit()
        return True

    def _row_to_digest(self, row) -> Digest:
        return Digest(
            id=row["id"], title=row["title"], summary=row["summary"],
            scan_type=row["scan_type"], created_at=row["created_at"],
        )

    # ── Inspiration ──────────────────────────────────────────────

    def add_inspiration(self, source_type: str, body: Optional[str] = None,
                        url: Optional[str] = None,
                        author: Optional[str] = None,
                        notes: Optional[str] = None,
                        liked_by: Optional[str] = None,
                        scanned_content_id: Optional[int] = None) -> int:
        cursor = self.db.execute(
            "INSERT INTO inspiration (source_type, scanned_content_id, url, "
            "body, author, notes, liked_by) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (source_type, scanned_content_id, url, body, author, notes, liked_by),
        )
        self.db.commit()
        return cursor.lastrowid

    def get_inspiration(self, inspiration_id: int) -> Optional[Inspiration]:
        row = self.db.fetchone(
            "SELECT * FROM inspiration WHERE id = ?", (inspiration_id,)
        )
        return self._row_to_inspiration(row) if row else None

    def get_recent_inspiration(self, limit: int = 20) -> list[Inspiration]:
        rows = self.db.fetchall(
            "SELECT * FROM inspiration ORDER BY created_at DESC LIMIT ?",
            (limit,),
        )
        return [self._row_to_inspiration(r) for r in rows]

    def get_inspiration_by_user(self, liked_by: str) -> list[Inspiration]:
        rows = self.db.fetchall(
            "SELECT * FROM inspiration WHERE liked_by = ? ORDER BY created_at DESC",
            (liked_by,),
        )
        return [self._row_to_inspiration(r) for r in rows]

    def delete_inspiration(self, inspiration_id: int) -> bool:
        self.db.execute(
            "DELETE FROM inspiration WHERE id = ?", (inspiration_id,)
        )
        self.db.commit()
        return True

    def _row_to_inspiration(self, row) -> Inspiration:
        return Inspiration(
            id=row["id"], source_type=row["source_type"],
            scanned_content_id=row["scanned_content_id"],
            url=row["url"], body=row["body"], author=row["author"],
            notes=row["notes"], liked_by=row["liked_by"],
            created_at=row["created_at"],
        )

    # ── Monitored Accounts ───────────────────────────────────────

    def add_monitored_account(self, platform: str, handle: str,
                              name: Optional[str] = None,
                              category: Optional[str] = None) -> int:
        cursor = self.db.execute(
            "INSERT INTO monitored_accounts (platform, handle, name, category) "
            "VALUES (?, ?, ?, ?)",
            (platform, handle, name, category),
        )
        self.db.commit()
        return cursor.lastrowid

    def get_monitored_account(self, account_id: int) -> Optional[MonitoredAccount]:
        row = self.db.fetchone(
            "SELECT * FROM monitored_accounts WHERE id = ?", (account_id,)
        )
        return self._row_to_monitored_account(row) if row else None

    def get_monitored_accounts(self, platform: Optional[str] = None) -> list[MonitoredAccount]:
        if platform:
            rows = self.db.fetchall(
                "SELECT * FROM monitored_accounts WHERE platform = ? AND active = 1 "
                "ORDER BY handle",
                (platform,),
            )
        else:
            rows = self.db.fetchall(
                "SELECT * FROM monitored_accounts WHERE active = 1 ORDER BY handle"
            )
        return [self._row_to_monitored_account(r) for r in rows]

    def get_all_monitored_accounts(self) -> list[MonitoredAccount]:
        rows = self.db.fetchall(
            "SELECT * FROM monitored_accounts ORDER BY handle"
        )
        return [self._row_to_monitored_account(r) for r in rows]

    def toggle_monitored_account(self, account_id: int, active: bool) -> bool:
        self.db.execute(
            "UPDATE monitored_accounts SET active = ? WHERE id = ?",
            (1 if active else 0, account_id),
        )
        self.db.commit()
        return True

    def delete_monitored_account(self, account_id: int) -> bool:
        self.db.execute(
            "DELETE FROM monitored_accounts WHERE id = ?", (account_id,)
        )
        self.db.commit()
        return True

    def _row_to_monitored_account(self, row) -> MonitoredAccount:
        return MonitoredAccount(
            id=row["id"], platform=row["platform"],
            handle=row["handle"], name=row["name"],
            category=row["category"], active=row["active"],
            created_at=row["created_at"],
        )

    # ── Aggregate Queries ───────────────────────────────────────

    def get_context_for_topic(self, topic: str) -> dict:
        """Get all relevant KB data for a content generation task."""
        return {
            "firm_facts": [f.__dict__ for f in self.search_firm_facts(topic)],
            "market_data": [m.__dict__ for m in self.search_market_data(topic)],
            "brand_rules": [r.__dict__ for r in self.get_all_brand_rules()],
            "recent_content": [
                c.__dict__ for c in self.search_content(topic)
            ][:5],
            "inspiration": [
                i.__dict__ for i in self.get_recent_inspiration(limit=5)
            ],
        }

    def get_content_stats(self) -> dict:
        """Get summary statistics about content."""
        total = self.db.fetchone("SELECT COUNT(*) as cnt FROM content")
        by_status = self.db.fetchall(
            "SELECT status, COUNT(*) as cnt FROM content GROUP BY status"
        )
        by_platform = self.db.fetchall(
            "SELECT platform, COUNT(*) as cnt FROM content GROUP BY platform"
        )
        return {
            "total": total["cnt"] if total else 0,
            "by_status": {r["status"]: r["cnt"] for r in by_status},
            "by_platform": {r["platform"]: r["cnt"] for r in by_platform},
        }
