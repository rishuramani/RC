"""Base agent with shared Claude API logic and brand compliance checking."""

from abc import ABC, abstractmethod

from src.db.knowledge_base import KnowledgeBase
from src.db.models import ContentTask, ContentDraft, BrandCheckResult
from src.integrations.claude_client import ClaudeClient
from src.prompts.brand_voice import FORBIDDEN_TERMS, REQUIRED_DISCLAIMERS


class BaseAgent(ABC):
    """Abstract base class for all content generation agents."""

    def __init__(self, claude_client: ClaudeClient, knowledge_base: KnowledgeBase):
        self.claude = claude_client
        self.kb = knowledge_base

    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """Return the system prompt for this agent."""
        ...

    @abstractmethod
    def _build_user_prompt(self, task: ContentTask) -> str:
        """Build the user prompt from a content task."""
        ...

    @abstractmethod
    def _parse_response(self, response: str, task: ContentTask) -> ContentDraft:
        """Parse Claude's response into a ContentDraft."""
        ...

    def generate(self, task: ContentTask) -> ContentDraft:
        """Generate content for the given task."""
        if not task.context:
            context = self.kb.get_context_for_topic(task.topic)
            task.context = str(context)

        user_prompt = self._build_user_prompt(task)
        response = self.claude.generate(
            system_prompt=self.system_prompt,
            user_prompt=user_prompt,
        )

        draft = self._parse_response(response, task)
        return draft

    def validate(self, content: str, content_type: str = "") -> BrandCheckResult:
        """Check content against brand guidelines."""
        issues = []
        suggestions = []
        content_lower = content.lower()

        # Check forbidden terms
        for term in FORBIDDEN_TERMS:
            if term.lower() in content_lower:
                issues.append(f"Contains forbidden term: '{term}'")

        # Check required disclaimers
        if content_type in ("blog", "market_report"):
            disclaimer = REQUIRED_DISCLAIMERS.get("market_analysis", "")
            if disclaimer and disclaimer.lower() not in content_lower:
                suggestions.append(
                    f"Consider adding market analysis disclaimer: '{disclaimer}'"
                )

        # Check if track record is mentioned without disclaimer
        track_record_terms = ["track record", "historical", "past returns",
                              "prior performance", "43.4%", "19.7%"]
        has_track_record = any(t in content_lower for t in track_record_terms)
        if has_track_record:
            disclaimer = REQUIRED_DISCLAIMERS.get("track_record", "")
            if disclaimer.lower() not in content_lower:
                issues.append(
                    f"Track record mentioned without disclaimer: '{disclaimer}'"
                )

        return BrandCheckResult(
            is_compliant=len(issues) == 0,
            issues=issues,
            suggestions=suggestions,
        )

    def _get_context_dict(self, task: ContentTask) -> dict:
        """Get context as a dictionary for prompt building."""
        return self.kb.get_context_for_topic(task.topic)
