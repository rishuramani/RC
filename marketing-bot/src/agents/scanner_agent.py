"""Content Scanner Agent — scans industry content and creates digests."""

import json
import logging
from datetime import datetime
from typing import Optional

from src.db.knowledge_base import KnowledgeBase
from src.db.models import ScannedContent, Digest
from src.integrations.claude_client import ClaudeClient
from src.integrations.twitter_api import TwitterAPI
from src.integrations.linkedin_api import LinkedInAPI
from src.prompts.system_prompts import SCANNER_DIGEST_PROMPT
from src.config import SCANNER_TWITTER_QUERIES, SCANNER_LINKEDIN_QUERIES

logger = logging.getLogger(__name__)


class ContentScanner:
    """Scans Twitter and LinkedIn for relevant industry content and creates digests."""

    def __init__(self, claude_client: ClaudeClient,
                 knowledge_base: KnowledgeBase,
                 twitter_api: Optional[TwitterAPI] = None,
                 linkedin_api: Optional[LinkedInAPI] = None):
        self.claude = claude_client
        self.kb = knowledge_base
        self.twitter = twitter_api or TwitterAPI(mock_mode=True)
        self.linkedin = linkedin_api or LinkedInAPI(mock_mode=True)

    def scan_twitter(self, queries: Optional[list[str]] = None,
                     accounts: Optional[list[str]] = None,
                     limit: int = 50) -> list[ScannedContent]:
        """Search Twitter for relevant content using API v2 search."""
        queries = queries or SCANNER_TWITTER_QUERIES
        accounts = accounts or []
        items = []
        seen_ids = set()

        # Search by queries
        per_query = max(1, limit // max(len(queries), 1))
        for query in queries:
            try:
                tweets = self.twitter.search_recent(query, max_results=per_query)
                for tweet in tweets:
                    tid = tweet.get("id", "")
                    if tid and tid not in seen_ids:
                        seen_ids.add(tid)
                        metrics = tweet.get("public_metrics", {})
                        engagement = (
                            metrics.get("like_count", 0) +
                            metrics.get("retweet_count", 0) +
                            metrics.get("reply_count", 0) +
                            metrics.get("quote_count", 0)
                        )
                        items.append(ScannedContent(
                            platform="twitter",
                            external_id=tid,
                            author=tweet.get("author_username", ""),
                            author_url=f"https://twitter.com/{tweet.get('author_username', '')}",
                            body=tweet.get("text", ""),
                            url=f"https://twitter.com/i/status/{tid}",
                            engagement_score=engagement,
                        ))
            except Exception as e:
                logger.warning(f"Twitter search failed for query '{query}': {e}")

        # Search by monitored accounts
        for handle in accounts:
            username = handle.lstrip("@")
            try:
                tweets = self.twitter.get_user_tweets(username, max_results=10)
                for tweet in tweets:
                    tid = tweet.get("id", "")
                    if tid and tid not in seen_ids:
                        seen_ids.add(tid)
                        metrics = tweet.get("public_metrics", {})
                        engagement = (
                            metrics.get("like_count", 0) +
                            metrics.get("retweet_count", 0) +
                            metrics.get("reply_count", 0) +
                            metrics.get("quote_count", 0)
                        )
                        items.append(ScannedContent(
                            platform="twitter",
                            external_id=tid,
                            author=username,
                            author_url=f"https://twitter.com/{username}",
                            body=tweet.get("text", ""),
                            url=f"https://twitter.com/i/status/{tid}",
                            engagement_score=engagement,
                        ))
            except Exception as e:
                logger.warning(f"Failed to get tweets for @{username}: {e}")

        return items

    def scan_linkedin(self, queries: Optional[list[str]] = None,
                      accounts: Optional[list[str]] = None,
                      limit: int = 30) -> list[ScannedContent]:
        """Scan LinkedIn for relevant posts (limited API — focus on mock data)."""
        queries = queries or SCANNER_LINKEDIN_QUERIES
        items = []

        if self.linkedin._mock_mode:
            # Generate mock LinkedIn posts for each query
            for i, query in enumerate(queries[:limit]):
                items.append(ScannedContent(
                    platform="linkedin",
                    external_id=f"li_post_{i}",
                    author=f"Industry Analyst {i + 1}",
                    author_url=f"https://linkedin.com/in/analyst-{i + 1}",
                    body=f"Key insights on {query}: The market continues to show "
                         f"strong fundamentals in Sunbelt markets. Workforce housing "
                         f"demand remains robust with occupancy above 90% in major metros.",
                    url=f"https://linkedin.com/posts/analyst-{i + 1}_post-{i}",
                    engagement_score=120 + i * 30,
                ))

        return items

    def _deduplicate(self, items: list[ScannedContent]) -> list[ScannedContent]:
        """Remove items already in the database."""
        unique = []
        for item in items:
            if item.external_id and self.kb.scanned_content_exists(
                item.external_id, item.platform
            ):
                continue
            unique.append(item)
        return unique

    def create_digest(self, scanned_items: list[ScannedContent],
                      scan_type: str = "scheduled") -> Digest:
        """Use Claude to summarize scanned content into a readable digest."""
        # Build content for Claude
        posts_text = []
        for i, item in enumerate(scanned_items):
            posts_text.append(
                f"[{i}] @{item.author} ({item.platform}) "
                f"[engagement: {item.engagement_score}]\n{item.body}\n"
            )

        user_prompt = (
            f"Analyze these {len(scanned_items)} scanned industry posts and "
            f"create a digest:\n\n" + "\n".join(posts_text)
        )

        try:
            response = self.claude.generate(
                system_prompt=SCANNER_DIGEST_PROMPT,
                user_prompt=user_prompt,
                max_tokens=2000,
            )
            digest_data = json.loads(response)
        except (json.JSONDecodeError, Exception) as e:
            logger.warning(f"Failed to parse Claude digest response: {e}")
            today = datetime.now().strftime("%b %d, %Y")
            digest_data = {
                "title": f"Industry Digest — {today}",
                "summary": f"Scanned {len(scanned_items)} posts across platforms.",
                "topic_tags": [],
                "highlights": [],
                "opportunities": [],
            }

        # Create digest record
        digest_id = self.kb.add_digest(
            title=digest_data.get("title", "Industry Digest"),
            summary=digest_data.get("summary", ""),
            scan_type=scan_type,
        )

        # Apply topic tags from Claude's analysis
        tag_map = {}
        for tag_entry in digest_data.get("topic_tags", []):
            idx = tag_entry.get("index", -1)
            if 0 <= idx < len(scanned_items):
                tag_map[idx] = tag_entry.get("tags", "")

        # Save scanned items to DB
        for i, item in enumerate(scanned_items):
            item.digest_id = digest_id
            if i in tag_map:
                item.topic_tags = tag_map[i]
            self.kb.add_scanned_content(
                platform=item.platform,
                body=item.body,
                external_id=item.external_id,
                author=item.author,
                author_url=item.author_url,
                url=item.url,
                engagement_score=item.engagement_score,
                topic_tags=item.topic_tags,
                digest_id=digest_id,
            )

        return self.kb.get_digest(digest_id)

    def run_scan(self, scan_type: str = "scheduled",
                 twitter_only: bool = False) -> Digest:
        """Full scan pipeline: fetch -> deduplicate -> analyze -> digest."""
        # 1. Get monitored accounts from DB
        twitter_accounts = [
            a.handle for a in self.kb.get_monitored_accounts(platform="twitter")
        ]
        linkedin_accounts = [
            a.handle for a in self.kb.get_monitored_accounts(platform="linkedin")
        ]

        # 2. Scan platforms
        all_items = []

        twitter_items = self.scan_twitter(accounts=twitter_accounts)
        all_items.extend(twitter_items)

        if not twitter_only:
            linkedin_items = self.scan_linkedin(accounts=linkedin_accounts)
            all_items.extend(linkedin_items)

        if not all_items:
            # Create an empty digest
            digest_id = self.kb.add_digest(
                title="Empty Scan", summary="No content found.", scan_type=scan_type,
            )
            return self.kb.get_digest(digest_id)

        # 3. Deduplicate
        unique_items = self._deduplicate(all_items)

        if not unique_items:
            digest_id = self.kb.add_digest(
                title="No New Content",
                summary="All scanned content was already in the database.",
                scan_type=scan_type,
            )
            return self.kb.get_digest(digest_id)

        # 4. Sort by engagement
        unique_items.sort(key=lambda x: x.engagement_score, reverse=True)

        # 5. Create digest with Claude analysis
        return self.create_digest(unique_items, scan_type=scan_type)
