"""Senior Marketing Agent - orchestrates content creation across platforms."""

import json
from datetime import datetime, timedelta
from typing import Optional

from src.db.knowledge_base import KnowledgeBase
from src.db.models import ContentTask, ContentDraft, Content
from src.integrations.claude_client import ClaudeClient
from src.prompts.system_prompts import ORCHESTRATOR_PROMPT
from src.prompts.templates import build_orchestrator_prompt
from src.agents.linkedin_agent import LinkedInAgent
from src.agents.twitter_agent import TwitterAgent
from src.agents.blog_agent import BlogAgent
from src.agents.market_report_agent import MarketReportAgent


class Orchestrator:
    """Senior marketing agent that plans and coordinates content creation."""

    def __init__(self, claude_client: ClaudeClient, knowledge_base: KnowledgeBase):
        self.claude = claude_client
        self.kb = knowledge_base

        # Initialize sub-agents
        self.agents = {
            "linkedin_post": LinkedInAgent(claude_client, knowledge_base),
            "tweet": TwitterAgent(claude_client, knowledge_base),
            "tweet_thread": TwitterAgent(claude_client, knowledge_base),
            "blog": BlogAgent(claude_client, knowledge_base),
            "market_report": MarketReportAgent(claude_client, knowledge_base),
        }

    def plan_content(self, days_ahead: int = 7,
                     instructions: str = "") -> list[ContentTask]:
        """Use Claude to plan upcoming content based on KB state."""
        # Gather context
        calendar_status = self._get_calendar_status(days_ahead)
        recent_content = self._get_recent_content_summary()
        market_data = self._get_market_data_summary()

        prompt = build_orchestrator_prompt(
            calendar_status=calendar_status,
            recent_content=recent_content,
            market_data=market_data,
            instructions=instructions,
        )

        response = self.claude.generate(
            system_prompt=ORCHESTRATOR_PROMPT,
            user_prompt=prompt,
        )

        return self._parse_plan(response)

    def generate_content(self, task: ContentTask) -> ContentDraft:
        """Delegate content generation to the appropriate sub-agent."""
        agent = self.agents.get(task.content_type)
        if agent is None:
            raise ValueError(f"Unknown content type: {task.content_type}")
        return agent.generate(task)

    def validate_content(self, draft: ContentDraft) -> dict:
        """Validate a draft against brand guidelines."""
        agent = self.agents.get(draft.content_type)
        if agent is None:
            raise ValueError(f"Unknown content type: {draft.content_type}")
        result = agent.validate(draft.body, draft.content_type)
        return {
            "is_compliant": result.is_compliant,
            "issues": result.issues,
            "suggestions": result.suggestions,
        }

    def suggest_topics(self) -> list[dict]:
        """Suggest content topics based on recent market data and gaps."""
        market_data = self.kb.get_market_data_by_market("houston")
        recent = self.kb.get_recent_content(limit=10)
        recent_topics = {c.topic for c in recent if c.topic}

        suggestions = []

        # Check for fresh market data not yet covered
        for data in market_data[:10]:
            topic_key = f"{data.metric}_{data.period}"
            if topic_key not in recent_topics:
                suggestions.append({
                    "topic": f"{data.market.title()} {data.metric}: {data.value}"
                             f" ({data.period})",
                    "reason": f"Fresh data from {data.source or 'knowledge base'}"
                              f" not yet covered",
                    "platforms": ["linkedin", "twitter"],
                })

        # Always suggest periodic content types
        suggestions.append({
            "topic": "Weekly market commentary",
            "reason": "Maintain consistent posting cadence",
            "platforms": ["linkedin", "twitter"],
        })

        return suggestions[:5]

    def cross_promote(self, content_id: int) -> list[ContentTask]:
        """Create tasks to adapt existing content across platforms."""
        content = self.kb.get_content(content_id)
        if content is None:
            raise ValueError(f"Content {content_id} not found")

        tasks = []
        existing_platforms = {content.platform}

        # Blog → LinkedIn + Twitter
        if content.content_type == "blog":
            if "linkedin" not in existing_platforms:
                tasks.append(ContentTask(
                    content_type="linkedin_post",
                    platform="linkedin",
                    topic=content.topic or "blog promotion",
                    principal=content.principal,
                    instructions=f"Promote this blog article: {content.title}. "
                                 f"Key points from the article:\n{content.body[:500]}",
                ))
            if "twitter" not in existing_platforms:
                tasks.append(ContentTask(
                    content_type="tweet_thread",
                    platform="twitter",
                    topic=content.topic or "blog promotion",
                    principal=content.principal,
                    instructions=f"Create a thread summarizing this article: "
                                 f"{content.title}.\n{content.body[:500]}",
                ))

        # LinkedIn → Twitter
        elif content.content_type == "linkedin_post":
            if "twitter" not in existing_platforms:
                tasks.append(ContentTask(
                    content_type="tweet",
                    platform="twitter",
                    topic=content.topic or "linkedin adaptation",
                    principal=content.principal,
                    instructions=f"Condense this LinkedIn post into a tweet:\n"
                                 f"{content.body[:500]}",
                ))

        return tasks

    def review_calendar(self) -> dict:
        """Review the current state of the content calendar."""
        today = datetime.now().date().isoformat()
        week_ahead = (datetime.now().date() + timedelta(days=7)).isoformat()

        pending = self.kb.get_pending_calendar_entries()
        upcoming = self.kb.get_calendar_entries_by_date_range(today, week_ahead)

        overdue = [
            e for e in pending
            if e.scheduled_date and e.scheduled_date < today
        ]

        return {
            "total_pending": len(pending),
            "upcoming_7_days": len(upcoming),
            "overdue": len(overdue),
            "entries": [
                {
                    "id": e.id,
                    "type": e.content_type,
                    "platform": e.platform,
                    "topic": e.topic,
                    "date": e.scheduled_date,
                    "status": e.status,
                }
                for e in upcoming
            ],
        }

    def _get_calendar_status(self, days_ahead: int) -> str:
        today = datetime.now().date().isoformat()
        end = (datetime.now().date() + timedelta(days=days_ahead)).isoformat()
        entries = self.kb.get_calendar_entries_by_date_range(today, end)

        if not entries:
            return "No content scheduled for the upcoming period."

        lines = []
        for e in entries:
            lines.append(
                f"- {e.scheduled_date}: {e.content_type} on {e.platform} "
                f"[{e.status}] - {e.topic or 'No topic specified'}"
            )
        return "\n".join(lines)

    def _get_recent_content_summary(self) -> str:
        recent = self.kb.get_recent_content(limit=10)
        if not recent:
            return "No content has been created yet."

        lines = []
        for c in recent:
            preview = c.body[:100].replace("\n", " ")
            lines.append(
                f"- [{c.content_type}] ({c.status}) {preview}..."
            )
        return "\n".join(lines)

    def _get_market_data_summary(self) -> str:
        houston = self.kb.get_market_data_by_market("houston")
        phoenix = self.kb.get_market_data_by_market("phoenix")

        lines = ["### Houston"]
        for d in houston[:10]:
            lines.append(f"- {d.metric}: {d.value} ({d.period or 'latest'})")

        if phoenix:
            lines.append("\n### Phoenix")
            for d in phoenix[:5]:
                lines.append(f"- {d.metric}: {d.value} ({d.period or 'latest'})")

        return "\n".join(lines) if lines else "No market data available."

    def _parse_plan(self, response: str) -> list[ContentTask]:
        """Parse Claude's JSON plan response into ContentTask objects."""
        # Try to extract JSON from the response
        try:
            # Find JSON array in the response
            start = response.find("[")
            end = response.rfind("]") + 1
            if start >= 0 and end > start:
                items = json.loads(response[start:end])
            else:
                return []
        except json.JSONDecodeError:
            return []

        tasks = []
        for item in items:
            tasks.append(ContentTask(
                content_type=item.get("content_type", "linkedin_post"),
                platform=item.get("platform", "linkedin"),
                topic=item.get("topic", ""),
                principal=item.get("principal"),
                instructions=item.get("instructions"),
            ))
        return tasks
