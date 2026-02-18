"""Tests for Twitter/X content generation agent."""

import pytest
from unittest.mock import MagicMock

from src.agents.twitter_agent import TwitterAgent
from src.db.models import ContentTask


SAMPLE_TWEET = "Houston multifamily occupancy: 90.4%. Supply pipeline at lowest since 2011. The math is starting to work for workforce housing buyers."

SAMPLE_THREAD = """1/ Houston's multifamily market just hit a key inflection point. Here's what the Q4 2025 data tells us:

2/ Absorption: 26,510 units absorbed in 2025. That's significant demand against a rapidly declining supply pipeline.

3/ Supply: Only 9,087 units under construction — the lowest since 2011. New starts have slowed dramatically as construction costs remain elevated.

4/ Occupancy: 90.4% across the metro. Class B and C workforce housing is leading the recovery, outperforming Class A.

5/ What this means: Operators with low-basis positions in workforce housing are positioned to benefit from tightening fundamentals.

6/ At RC Investment Properties, we've been underwriting for this moment. Conservative leverage + durable cash flow + declining supply = opportunity."""


class TestTwitterAgent:

    @pytest.fixture
    def agent(self, seeded_kb):
        claude = MagicMock()
        claude.generate.return_value = SAMPLE_TWEET
        return TwitterAgent(claude, seeded_kb)

    @pytest.fixture
    def thread_agent(self, seeded_kb):
        claude = MagicMock()
        claude.generate.return_value = SAMPLE_THREAD
        return TwitterAgent(claude, seeded_kb)

    def test_generate_tweet(self, agent):
        task = ContentTask(
            content_type="tweet",
            platform="twitter",
            topic="Houston occupancy data",
            principal="michael",
        )
        draft = agent.generate(task)
        assert draft.content_type == "tweet"
        assert draft.platform == "twitter"
        assert len(draft.body) > 0

    def test_generate_thread(self, thread_agent):
        task = ContentTask(
            content_type="tweet_thread",
            platform="twitter",
            topic="Houston Q4 2025 market analysis",
            principal="michael",
        )
        draft = thread_agent.generate(task)
        assert draft.content_type == "tweet_thread"
        assert "tweets" in draft.metadata
        assert draft.metadata["tweet_count"] >= 3

    def test_parse_thread_numbered_format(self, thread_agent):
        tweets = thread_agent._parse_thread(SAMPLE_THREAD)
        assert len(tweets) == 6
        assert tweets[0].startswith("1/")
        assert tweets[-1].startswith("6/")

    def test_parse_thread_empty(self, thread_agent):
        tweets = thread_agent._parse_thread("")
        assert len(tweets) == 1  # Falls back to single tweet

    def test_system_prompt_includes_twitter_specifics(self, agent):
        assert "280 characters" in agent.system_prompt
        assert "Twitter" in agent.system_prompt or "tweet" in agent.system_prompt.lower()

    def test_validate_compliant_tweet(self, agent):
        result = agent.validate(SAMPLE_TWEET)
        assert result.is_compliant is True

    def test_validate_forbidden_term_in_tweet(self, agent):
        result = agent.validate("We're flipping houses for passive income!")
        assert result.is_compliant is False
