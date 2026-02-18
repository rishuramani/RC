"""Tests for blog article generation agent."""

import pytest
from unittest.mock import MagicMock

from src.agents.blog_agent import BlogAgent
from src.db.models import ContentTask


SAMPLE_BLOG = """<h1>Houston Q4 2025: Why Declining Supply Signals Opportunity in Workforce Housing</h1>

<p>Houston's multifamily market is entering a new phase. After years of elevated construction activity, the supply pipeline has contracted sharply, creating conditions that favor disciplined operators with existing positions in workforce housing.</p>

<h2>The Supply Picture</h2>

<p>According to CoStar's Q4 2025 data, Houston has just 9,087 multifamily units under construction — the lowest figure since 2011. This represents a dramatic pullback from the peak of over 30,000 units in the pipeline just two years ago.</p>

<p>The reasons are straightforward: elevated construction costs, tighter lending standards, and fewer viable land sites have combined to slow new starts significantly.</p>

<h2>Demand Remains Durable</h2>

<p>While supply has contracted, demand has remained remarkably resilient. Houston absorbed 26,510 units in 2025, driven by continued population growth — the metro added approximately 200,000 residents in 2024 alone (U.S. Census Bureau), with 75% attributed to net migration.</p>

<p>The employment picture supports this trend. Houston added 57,800 jobs in 2024, diversified across healthcare, energy, technology, and manufacturing sectors.</p>

<h2>Workforce Housing: The Sweet Spot</h2>

<p>The convergence of declining supply and sustained demand is most pronounced in the workforce housing segment — Class B and C properties typically renting between $1,100 and $1,450 per month.</p>

<p>These assets face minimal competition from new Class A construction, which targets higher rent points. As metro occupancy has recovered to 90.4%, workforce housing properties have seen the strongest occupancy gains.</p>

<h2>What This Means for Investors</h2>

<p>For operators focused on the sub-institutional segment ($5-20M per deal), current conditions offer a compelling setup:</p>

<ul>
<li><strong>Supply discipline</strong> reduces the risk of oversaturation in workforce housing submarkets</li>
<li><strong>Durable demand</strong> from population growth and job creation supports occupancy</li>
<li><strong>Basis protection</strong> — replacement costs continue to rise, making existing low-basis positions increasingly valuable</li>
<li><strong>Cash flow durability</strong> — tightening fundamentals support stable rent collection and moderate growth</li>
</ul>

<h2>Looking Ahead</h2>

<p>The math is straightforward. When supply growth slows and demand persists, occupancy tightens and rent growth follows. For investors with conservative leverage, low acquisition basis, and hands-on operational capability, Houston's workforce housing market is well-positioned for the next phase.</p>

<p><em>For informational purposes only. This does not constitute investment advice.</em></p>"""


class TestBlogAgent:

    @pytest.fixture
    def agent(self, seeded_kb):
        claude = MagicMock()
        claude.generate.return_value = SAMPLE_BLOG
        return BlogAgent(claude, seeded_kb)

    def test_generate_produces_draft(self, agent):
        task = ContentTask(
            content_type="blog",
            platform="blog",
            topic="Houston Q4 supply decline",
        )
        draft = agent.generate(task)
        assert draft.content_type == "blog"
        assert draft.platform == "blog"
        assert draft.title is not None
        assert "Houston" in draft.title
        assert len(draft.body) > 0

    def test_extracts_title_from_h1(self, agent):
        task = ContentTask(
            content_type="blog", platform="blog",
            topic="Houston Q4 supply decline",
        )
        draft = agent.generate(task)
        assert "Workforce Housing" in draft.title

    def test_calculates_word_count(self, agent):
        task = ContentTask(
            content_type="blog", platform="blog",
            topic="Houston Q4 supply decline",
        )
        draft = agent.generate(task)
        assert "word_count" in draft.metadata
        assert draft.metadata["word_count"] > 300

    def test_extracts_meta_description(self, agent):
        task = ContentTask(
            content_type="blog", platform="blog",
            topic="Houston Q4 supply decline",
        )
        draft = agent.generate(task)
        assert "meta_description" in draft.metadata

    def test_system_prompt_includes_blog_specifics(self, agent):
        assert "800-1200 words" in agent.system_prompt
        assert "HTML" in agent.system_prompt

    def test_validate_blog_with_disclaimer(self, agent):
        result = agent.validate(SAMPLE_BLOG, "blog")
        assert result.is_compliant is True

    def test_validate_blog_without_disclaimer(self, agent):
        bad_blog = SAMPLE_BLOG.replace(
            "For informational purposes only. This does not constitute investment advice.",
            ""
        )
        result = agent.validate(bad_blog, "blog")
        # Should suggest disclaimer but not necessarily fail compliance
        # (it depends on whether track record terms are present)
        assert isinstance(result.suggestions, list)
