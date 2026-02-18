"""Market report generation agent."""

from src.agents.base_agent import BaseAgent
from src.db.models import ContentTask, ContentDraft
from src.prompts.system_prompts import MARKET_REPORT_PROMPT
from src.prompts.templates import build_market_report_prompt


class MarketReportAgent(BaseAgent):
    """Generates structured market analysis reports."""

    @property
    def system_prompt(self) -> str:
        return MARKET_REPORT_PROMPT

    def _build_user_prompt(self, task: ContentTask) -> str:
        context = self._get_context_dict(task)

        # Extract market and period from topic if possible
        parts = task.topic.split(" - ", 1)
        market = parts[0] if parts else "houston"
        period = parts[1] if len(parts) > 1 else "Latest"

        return build_market_report_prompt(
            market=market,
            period=period,
            context=context,
            instructions=task.instructions or "",
        )

    def _parse_response(self, response: str, task: ContentTask) -> ContentDraft:
        body = response.strip()
        title = self._extract_title(body)

        return ContentDraft(
            content_type="market_report",
            platform="report",
            title=title,
            body=body,
            topic=task.topic,
        )

    def _extract_title(self, markdown: str) -> str:
        """Extract title from first H1 in markdown."""
        for line in markdown.split("\n"):
            stripped = line.strip()
            if stripped.startswith("# ") and not stripped.startswith("## "):
                return stripped[2:].strip()
        return "Market Update Report"
