"""Publishing module — posts content to LinkedIn and Twitter/X APIs."""

from src.db.models import Content
from src.integrations.linkedin_api import LinkedInAPI
from src.integrations.twitter_api import TwitterAPI


class Publisher:
    """Publishes content to the appropriate platform."""

    def __init__(self, linkedin_api: LinkedInAPI = None,
                 twitter_api: TwitterAPI = None):
        self.linkedin = linkedin_api
        self.twitter = twitter_api

    def publish(self, content: Content) -> dict:
        """Publish content to the target platform."""
        if content.platform == "linkedin":
            return self._publish_linkedin(content)
        elif content.platform == "twitter":
            return self._publish_twitter(content)
        else:
            return {
                "success": False,
                "error": f"Publishing not supported for platform: {content.platform}",
            }

    def _publish_linkedin(self, content: Content) -> dict:
        if self.linkedin is None:
            return {"success": False, "error": "LinkedIn API not configured"}
        return self.linkedin.create_post(content.body)

    def _publish_twitter(self, content: Content) -> dict:
        if self.twitter is None:
            return {"success": False, "error": "Twitter API not configured"}

        if content.content_type == "tweet_thread":
            return self.twitter.create_thread(content.body)
        return self.twitter.create_tweet(content.body)
