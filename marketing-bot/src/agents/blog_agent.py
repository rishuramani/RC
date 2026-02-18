"""Blog article generation agent."""

import re

from src.agents.base_agent import BaseAgent
from src.db.models import ContentTask, ContentDraft
from src.prompts.system_prompts import BLOG_AGENT_PROMPT
from src.prompts.templates import build_blog_prompt


class BlogAgent(BaseAgent):
    """Generates long-form blog articles for the RC website."""

    @property
    def system_prompt(self) -> str:
        return BLOG_AGENT_PROMPT

    def _build_user_prompt(self, task: ContentTask) -> str:
        context = self._get_context_dict(task)
        return build_blog_prompt(
            topic=task.topic,
            context=context,
            instructions=task.instructions or "",
        )

    def _parse_response(self, response: str, task: ContentTask) -> ContentDraft:
        body = response.strip()
        title = self._extract_title(body)
        meta_desc = self._extract_meta_description(body)

        word_count = len(re.findall(r'\b\w+\b', re.sub(r'<[^>]+>', '', body)))

        return ContentDraft(
            content_type="blog",
            platform="blog",
            title=title,
            body=body,
            topic=task.topic,
            metadata={
                "meta_description": meta_desc,
                "word_count": word_count,
            },
        )

    def _extract_title(self, html: str) -> str:
        """Extract the title from an H1 tag."""
        match = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.IGNORECASE | re.DOTALL)
        if match:
            return re.sub(r'<[^>]+>', '', match.group(1)).strip()
        # Fallback: first non-empty line
        for line in html.split("\n"):
            stripped = line.strip()
            if stripped and not stripped.startswith("<"):
                return stripped
        return "Untitled"

    def _extract_meta_description(self, html: str) -> str:
        """Extract or generate a meta description."""
        match = re.search(
            r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']',
            html, re.IGNORECASE
        )
        if match:
            return match.group(1)
        # Fallback: first paragraph text
        p_match = re.search(r'<p[^>]*>(.*?)</p>', html,
                            re.IGNORECASE | re.DOTALL)
        if p_match:
            text = re.sub(r'<[^>]+>', '', p_match.group(1)).strip()
            return text[:160]
        return ""
