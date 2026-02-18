"""Tests for market report generation agent."""

import pytest
from unittest.mock import MagicMock

from src.agents.market_report_agent import MarketReportAgent
from src.db.models import ContentTask


SAMPLE_REPORT = """# Houston Multifamily Market Update — Q4 2025

## Executive Summary

- **Occupancy** recovered to 90.4%, strongest level in 18 months
- **Absorption** of 26,510 units outpaced new deliveries by a wide margin
- **Supply pipeline** dropped to 9,087 units under construction (lowest since 2011)
- **Rent growth** projected at 2.1% annualized heading into 2026
- **Investment sales** activity increasing as pricing stabilizes in the $5-20M range

## Market Overview

Houston's multifamily market demonstrated meaningful recovery in Q4 2025. The confluence of slowing supply and sustained demand is creating favorable conditions for operators, particularly in the workforce housing segment.

The metro added approximately 200,000 residents in 2024 (U.S. Census Bureau), with net migration accounting for 75% of growth. Employment diversification across healthcare, energy, technology, and manufacturing continues to support housing demand.

## Supply & Demand

**Absorption:** 26,510 units absorbed in 2025 (CoStar), reflecting durable demand driven by population growth and employment gains.

**Construction Pipeline:**
- 9,087 units under construction (Q4 2025)
- Down from 30,000+ units at peak
- New starts have slowed significantly due to elevated construction costs and tighter lending

**Deliveries:** New supply continues to moderate, with 2026 projected to see further declines.

## Rent & Occupancy Trends

| Metric | Q4 2025 | Prior Year |
|--------|---------|------------|
| Metro Occupancy | 90.4% | 88.1% |
| Average Effective Rent | $1,277/mo | $1,250/mo |
| Projected Rent Growth | 2.1% | 0.8% |

Workforce housing (Class B/C) outperformed Class A in occupancy gains, benefiting from limited direct competition from new construction.

## Investment Sales Activity

Transaction volume in the $5-20M range has increased as pricing recalibrates. Key trends:
- Cap rate compression beginning in well-located workforce housing assets
- Buyer-seller gap narrowing as rate environment stabilizes
- Distress remains limited but select opportunities emerging

## Outlook & Investment Implications

The fundamental setup for Houston workforce housing is increasingly constructive:
1. Supply discipline reduces oversaturation risk
2. Population growth supports sustained demand
3. Low-basis acquisitions offer meaningful replacement cost protection
4. Conservative leverage positions operators for both cash flow and eventual exit

For informational purposes only. This does not constitute investment advice.
"""


class TestMarketReportAgent:

    @pytest.fixture
    def agent(self, seeded_kb):
        claude = MagicMock()
        claude.generate.return_value = SAMPLE_REPORT
        return MarketReportAgent(claude, seeded_kb)

    def test_generate_produces_draft(self, agent):
        task = ContentTask(
            content_type="market_report",
            platform="report",
            topic="houston - Q4 2025",
        )
        draft = agent.generate(task)
        assert draft.content_type == "market_report"
        assert draft.platform == "report"
        assert "Houston" in draft.title
        assert len(draft.body) > 0

    def test_extracts_title_from_h1(self, agent):
        task = ContentTask(
            content_type="market_report",
            platform="report",
            topic="houston - Q4 2025",
        )
        draft = agent.generate(task)
        assert "Q4 2025" in draft.title

    def test_system_prompt_includes_report_specifics(self, agent):
        assert "Executive Summary" in agent.system_prompt
        assert "Markdown" in agent.system_prompt

    def test_validate_report_with_disclaimer(self, agent):
        result = agent.validate(SAMPLE_REPORT, "market_report")
        assert result.is_compliant is True

    def test_topic_parsing_with_dash(self, agent):
        task = ContentTask(
            content_type="market_report",
            platform="report",
            topic="houston - Q4 2025",
        )
        prompt = agent._build_user_prompt(task)
        assert "Houston" in prompt
        assert "Q4 2025" in prompt

    def test_topic_parsing_without_dash(self, agent):
        task = ContentTask(
            content_type="market_report",
            platform="report",
            topic="phoenix market conditions",
        )
        prompt = agent._build_user_prompt(task)
        assert "Phoenix Market Conditions" in prompt
