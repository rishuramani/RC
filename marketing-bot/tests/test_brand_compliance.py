"""Tests for brand compliance checking across all agents."""

import pytest
from unittest.mock import MagicMock

from src.agents.base_agent import BaseAgent
from src.agents.linkedin_agent import LinkedInAgent
from src.db.models import BrandCheckResult
from src.prompts.brand_voice import FORBIDDEN_TERMS, REQUIRED_DISCLAIMERS


@pytest.fixture
def checker(seeded_kb):
    """Create a LinkedIn agent for validation testing."""
    claude = MagicMock()
    return LinkedInAgent(claude, seeded_kb)


class TestForbiddenTerms:
    """Verify all forbidden terms are caught."""

    @pytest.mark.parametrize("term", FORBIDDEN_TERMS)
    def test_catches_forbidden_term(self, checker, term):
        content = f"We are focused on {term} in the Houston market."
        result = checker.validate(content)
        assert result.is_compliant is False, \
            f"Failed to catch forbidden term: '{term}'"
        assert any(term.lower() in issue.lower() for issue in result.issues)

    def test_clean_content_passes(self, checker):
        content = (
            "Houston's workforce housing market showed strong absorption "
            "in Q4 2025. Occupancy reached 90.4% with a declining supply pipeline."
        )
        result = checker.validate(content)
        assert result.is_compliant is True
        assert len(result.issues) == 0


class TestTrackRecordDisclaimer:
    """Verify track record mentions require disclaimers."""

    def test_track_record_without_disclaimer(self, checker):
        content = "Our track record speaks for itself with consistent returns."
        result = checker.validate(content)
        assert result.is_compliant is False
        assert any("disclaimer" in i.lower() for i in result.issues)

    def test_historical_without_disclaimer(self, checker):
        content = "Historical performance shows 19.7% annualized returns."
        result = checker.validate(content)
        assert result.is_compliant is False

    def test_specific_return_without_disclaimer(self, checker):
        content = "The Meta Street deal generated a 43.4% value increase."
        result = checker.validate(content)
        assert result.is_compliant is False

    def test_track_record_with_disclaimer(self, checker):
        content = (
            "Our track record includes a 43.4% value increase on the Meta Street exit. "
            "Past performance is not indicative of future results."
        )
        result = checker.validate(content)
        assert result.is_compliant is True

    def test_no_track_record_no_disclaimer_needed(self, checker):
        content = "Houston absorbed 26,510 units in 2025. Supply is declining."
        result = checker.validate(content)
        assert result.is_compliant is True


class TestBlogAndReportDisclaimers:
    """Verify long-form content gets disclaimer suggestions."""

    def test_blog_without_disclaimer_gets_suggestion(self, checker):
        result = checker.validate(
            "Houston's market is strengthening with 90.4% occupancy.",
            content_type="blog"
        )
        assert any("disclaimer" in s.lower() for s in result.suggestions)

    def test_market_report_without_disclaimer_gets_suggestion(self, checker):
        result = checker.validate(
            "Q4 2025 shows strong absorption in Houston.",
            content_type="market_report"
        )
        assert any("disclaimer" in s.lower() for s in result.suggestions)

    def test_blog_with_disclaimer_no_suggestion(self, checker):
        result = checker.validate(
            "Houston's market is strengthening. "
            "For informational purposes only. This does not constitute investment advice.",
            content_type="blog"
        )
        disclaimer_suggestions = [
            s for s in result.suggestions if "disclaimer" in s.lower()
        ]
        assert len(disclaimer_suggestions) == 0


class TestEdgeCases:

    def test_empty_content(self, checker):
        result = checker.validate("")
        assert result.is_compliant is True

    def test_case_insensitive_forbidden_terms(self, checker):
        result = checker.validate("GUARANTEED RETURNS on every deal!")
        assert result.is_compliant is False

    def test_partial_match_not_caught(self, checker):
        # "flip" is forbidden but "flipchart" should be caught (substring match)
        # This is a known limitation - we accept it for safety
        result = checker.validate("We used a flipchart in the meeting.")
        # The word "flip" will match inside "flipchart" — this is the conservative approach
        assert result.is_compliant is False

    def test_multiple_violations(self, checker):
        content = (
            "We guarantee returns by flipping affordable housing "
            "for passive income. This is a risk-free investment!"
        )
        result = checker.validate(content)
        assert result.is_compliant is False
        assert len(result.issues) >= 4
