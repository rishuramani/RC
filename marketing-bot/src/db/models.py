"""Data models for the RC Marketing Bot knowledge base."""

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional


@dataclass
class FirmFact:
    id: Optional[int] = None
    category: str = ""
    key: str = ""
    value: str = ""
    source: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class MarketData:
    id: Optional[int] = None
    market: str = ""
    metric: str = ""
    value: str = ""
    period: Optional[str] = None
    source: Optional[str] = None
    created_at: Optional[datetime] = None


@dataclass
class BrandRule:
    id: Optional[int] = None
    rule_type: str = ""
    rule: str = ""
    example: Optional[str] = None
    created_at: Optional[datetime] = None


@dataclass
class Content:
    id: Optional[int] = None
    content_type: str = ""
    platform: str = ""
    principal: Optional[str] = None
    title: Optional[str] = None
    body: str = ""
    topic: Optional[str] = None
    status: str = "draft"
    scheduled_for: Optional[datetime] = None
    published_at: Optional[datetime] = None
    platform_post_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class ContentMetrics:
    id: Optional[int] = None
    content_id: int = 0
    impressions: int = 0
    likes: int = 0
    comments: int = 0
    shares: int = 0
    clicks: int = 0
    fetched_at: Optional[datetime] = None


@dataclass
class ContentCalendarEntry:
    id: Optional[int] = None
    content_type: str = ""
    platform: str = ""
    topic: Optional[str] = None
    principal: Optional[str] = None
    scheduled_date: Optional[date] = None
    status: str = "planned"
    content_id: Optional[int] = None
    notes: Optional[str] = None
    created_at: Optional[datetime] = None


@dataclass
class DataSource:
    id: Optional[int] = None
    name: str = ""
    url: Optional[str] = None
    frequency: Optional[str] = None
    last_checked: Optional[datetime] = None
    next_check: Optional[datetime] = None
    notes: Optional[str] = None


@dataclass
class ScannedContent:
    id: Optional[int] = None
    platform: str = ""
    external_id: Optional[str] = None
    author: Optional[str] = None
    author_url: Optional[str] = None
    body: str = ""
    url: Optional[str] = None
    engagement_score: int = 0
    topic_tags: Optional[str] = None
    scanned_at: Optional[datetime] = None
    digest_id: Optional[int] = None


@dataclass
class Digest:
    id: Optional[int] = None
    title: Optional[str] = None
    summary: Optional[str] = None
    scan_type: str = "scheduled"
    created_at: Optional[datetime] = None


@dataclass
class Inspiration:
    id: Optional[int] = None
    source_type: str = ""
    scanned_content_id: Optional[int] = None
    url: Optional[str] = None
    body: Optional[str] = None
    author: Optional[str] = None
    notes: Optional[str] = None
    liked_by: Optional[str] = None
    created_at: Optional[datetime] = None


@dataclass
class MonitoredAccount:
    id: Optional[int] = None
    platform: str = ""
    handle: str = ""
    name: Optional[str] = None
    category: Optional[str] = None
    active: int = 1
    created_at: Optional[datetime] = None


@dataclass
class ContentTask:
    """A task assigned by the orchestrator to a sub-agent."""
    content_type: str = ""
    platform: str = ""
    topic: str = ""
    principal: Optional[str] = None
    context: str = ""
    instructions: Optional[str] = None
    calendar_entry_id: Optional[int] = None


@dataclass
class ContentDraft:
    """Output from a sub-agent."""
    content_type: str = ""
    platform: str = ""
    principal: Optional[str] = None
    title: Optional[str] = None
    body: str = ""
    topic: str = ""
    hashtags: list = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


@dataclass
class BrandCheckResult:
    """Result of a brand compliance check."""
    is_compliant: bool = True
    issues: list = field(default_factory=list)
    suggestions: list = field(default_factory=list)
