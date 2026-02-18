"""Tests for LinkedIn content generation agent."""

import pytest
from unittest.mock import MagicMock

from src.agents.linkedin_agent import LinkedInAgent
from src.db.models import ContentTask


SAMPLE_LINKEDIN_RESPONSE = """Houston's multifamily market just hit a milestone that deserves attention.

Q4 2025 data shows 90.4% occupancy across the metro — and here's the real story: the supply pipeline has dropped to just 9,087 units under construction, the lowest level since 2011.

For those of us focused on workforce housing in the $5-20M range, this confluence of strong absorption and declining new supply is exactly the environment we underwrite for.

Three things stand out:

1. Absorption of 26,510 units in 2025 outpaced new deliveries by a significant margin
2. Class B and C assets — the workforce housing segment — are seeing the strongest occupancy gains
3. Replacement costs continue to rise, making existing basis positions increasingly attractive

This isn't speculation. It's math.

At RC Investment Properties, we've seen this dynamic play out across our 143-unit Houston portfolio. When supply discipline meets sustained demand, operators with low basis positions benefit disproportionately.

The fundamentals are shifting in favor of disciplined buyers.

#MultifamilyInvesting #HoustonRealEstate #WorkforceHousing #RealEstateInvesting #CRE"""


class TestLinkedInAgent:

    @pytest.fixture
    def agent(self, seeded_kb, mock_claude_response):
        claude = MagicMock()
        claude.generate.return_value = SAMPLE_LINKEDIN_RESPONSE
        return LinkedInAgent(claude, seeded_kb)

    def test_generate_produces_draft(self, agent):
        task = ContentTask(
            content_type="linkedin_post",
            platform="linkedin",
            topic="Houston Q4 2025 absorption data",
            principal="michael",
        )
        draft = agent.generate(task)

        assert draft.content_type == "linkedin_post"
        assert draft.platform == "linkedin"
        assert draft.principal == "michael"
        assert draft.topic == "Houston Q4 2025 absorption data"
        assert len(draft.body) > 0

    def test_extracts_hashtags(self, agent):
        task = ContentTask(
            content_type="linkedin_post",
            platform="linkedin",
            topic="Houston market",
            principal="michael",
        )
        draft = agent.generate(task)
        assert len(draft.hashtags) > 0
        assert all(h.startswith("#") for h in draft.hashtags)

    def test_system_prompt_includes_brand_voice(self, agent):
        assert "RC Investment Properties" in agent.system_prompt
        assert "workforce housing" in agent.system_prompt
        assert "LinkedIn" in agent.system_prompt

    def test_builds_user_prompt_with_context(self, agent):
        task = ContentTask(
            content_type="linkedin_post",
            platform="linkedin",
            topic="houston occupancy",
            principal="michael",
        )
        prompt = agent._build_user_prompt(task)
        assert "houston occupancy" in prompt
        assert "Michael Rosen" in prompt

    def test_builds_prompt_for_bradley(self, agent):
        task = ContentTask(
            content_type="linkedin_post",
            platform="linkedin",
            topic="property operations",
            principal="bradley",
        )
        prompt = agent._build_user_prompt(task)
        assert "Bradley Couch" in prompt

    def test_validate_compliant_content(self, agent):
        result = agent.validate(
            "Houston occupancy hit 90.4% in Q4 2025. Workforce housing continues to show strength."
        )
        assert result.is_compliant is True

    def test_validate_forbidden_term(self, agent):
        result = agent.validate(
            "We're flipping properties in Houston for guaranteed returns!"
        )
        assert result.is_compliant is False
        assert any("flipping" in i.lower() for i in result.issues)
        assert any("guaranteed" in i.lower() for i in result.issues)

    def test_validate_track_record_without_disclaimer(self, agent):
        result = agent.validate(
            "Our track record shows 43.4% value increase on the Meta Street exit."
        )
        assert result.is_compliant is False
        assert any("disclaimer" in i.lower() for i in result.issues)

    def test_validate_track_record_with_disclaimer(self, agent):
        result = agent.validate(
            "Our track record shows 43.4% value increase on the Meta Street exit. "
            "Past performance is not indicative of future results."
        )
        assert result.is_compliant is True
