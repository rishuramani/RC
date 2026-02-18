"""LinkedIn content generation agent."""

from src.agents.base_agent import BaseAgent
from src.db.models import ContentTask, ContentDraft
from src.prompts.system_prompts import LINKEDIN_AGENT_PROMPT
from src.prompts.templates import build_linkedin_prompt


class LinkedInAgent(BaseAgent):
    """Generates LinkedIn posts for Michael and Bradley's profiles."""

    @property
    def system_prompt(self) -> str:
        return LINKEDIN_AGENT_PROMPT

    def _build_user_prompt(self, task: ContentTask) -> str:
        context = self._get_context_dict(task)
        return build_linkedin_prompt(
            topic=task.topic,
            principal=task.principal or "company",
            context=context,
            instructions=task.instructions or "",
        )

    def _parse_response(self, response: str, task: ContentTask) -> ContentDraft:
        # Extract hashtags if present
        lines = response.strip().split("\n")
        hashtags = []
        body_lines = []

        for line in lines:
            stripped = line.strip()
            # Check if line is primarily hashtags
            if stripped and all(
                word.startswith("#") or word == ""
                for word in stripped.split()
                if word
            ):
                hashtags.extend(
                    word for word in stripped.split() if word.startswith("#")
                )
            else:
                body_lines.append(line)

        body = "\n".join(body_lines).strip()
        if hashtags:
            body = body + "\n\n" + " ".join(hashtags)

        return ContentDraft(
            content_type="linkedin_post",
            platform="linkedin",
            principal=task.principal,
            body=body,
            topic=task.topic,
            hashtags=hashtags,
        )
