"""Twitter/X content generation agent."""

from src.agents.base_agent import BaseAgent
from src.db.models import ContentTask, ContentDraft
from src.prompts.system_prompts import TWITTER_AGENT_PROMPT
from src.prompts.templates import build_twitter_prompt


class TwitterAgent(BaseAgent):
    """Generates tweets and threads for Twitter/X."""

    @property
    def system_prompt(self) -> str:
        return TWITTER_AGENT_PROMPT

    def _build_user_prompt(self, task: ContentTask) -> str:
        context = self._get_context_dict(task)
        is_thread = task.content_type == "tweet_thread"
        return build_twitter_prompt(
            topic=task.topic,
            principal=task.principal or "company",
            context=context,
            thread=is_thread,
            instructions=task.instructions or "",
        )

    def _parse_response(self, response: str, task: ContentTask) -> ContentDraft:
        is_thread = task.content_type == "tweet_thread"

        if is_thread:
            tweets = self._parse_thread(response)
            metadata = {"tweets": tweets, "tweet_count": len(tweets)}
        else:
            metadata = {}

        return ContentDraft(
            content_type=task.content_type or "tweet",
            platform="twitter",
            principal=task.principal,
            body=response.strip(),
            topic=task.topic,
            metadata=metadata,
        )

    def _parse_thread(self, response: str) -> list[str]:
        """Parse a thread response into individual tweets."""
        tweets = []
        current_tweet = []

        for line in response.strip().split("\n"):
            stripped = line.strip()
            # Check if this line starts a new numbered tweet
            if stripped and (
                stripped[0].isdigit() and "/" in stripped[:4]
            ):
                if current_tweet:
                    tweets.append("\n".join(current_tweet).strip())
                current_tweet = [stripped]
            elif stripped:
                current_tweet.append(stripped)

        if current_tweet:
            tweets.append("\n".join(current_tweet).strip())

        # If no numbered format detected, treat the whole response as one tweet
        if not tweets:
            tweets = [response.strip()]

        return tweets
