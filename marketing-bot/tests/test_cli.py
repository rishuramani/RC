"""Tests for the CLI interface."""

import pytest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner

from src.cli import main


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def mock_pipeline(seeded_kb):
    """Mock the pipeline initialization."""
    with patch("src.cli._get_pipeline") as mock_get:
        from src.pipeline.content_pipeline import ContentPipeline
        claude = MagicMock()
        claude.generate.return_value = "Houston workforce housing market update."
        pipeline = ContentPipeline(claude, seeded_kb)
        mock_get.return_value = pipeline
        yield pipeline


@pytest.fixture
def mock_kb(seeded_kb):
    """Mock the KB initialization."""
    with patch("src.cli._get_kb") as mock_get:
        mock_get.return_value = seeded_kb
        yield seeded_kb


class TestGenerateCommand:

    def test_generate_linkedin(self, runner, mock_pipeline):
        result = runner.invoke(main, [
            "generate", "linkedin", "--topic", "Houston market", "--principal", "michael"
        ])
        assert result.exit_code == 0
        assert "Content #" in result.output

    def test_generate_tweet(self, runner, mock_pipeline):
        result = runner.invoke(main, [
            "generate", "tweet", "--topic", "Supply data"
        ])
        assert result.exit_code == 0

    def test_generate_invalid_type(self, runner, mock_pipeline):
        result = runner.invoke(main, ["generate", "invalid", "--topic", "test"])
        assert result.exit_code != 0

    def test_generate_requires_topic(self, runner, mock_pipeline):
        result = runner.invoke(main, ["generate", "linkedin"])
        assert result.exit_code != 0


class TestReviewCommand:

    def test_review_empty_queue(self, runner, mock_pipeline):
        result = runner.invoke(main, ["review"])
        assert result.exit_code == 0
        assert "empty" in result.output.lower() or "Review Queue" in result.output

    def test_review_with_content(self, runner, mock_pipeline):
        mock_pipeline.kb.add_content(
            "tweet", "twitter", "Test tweet", status="queued"
        )
        result = runner.invoke(main, ["review"])
        assert result.exit_code == 0

    def test_review_specific_id(self, runner, mock_pipeline):
        cid = mock_pipeline.kb.add_content(
            "tweet", "twitter", "Test tweet body", status="queued"
        )
        result = runner.invoke(main, ["review", str(cid)])
        assert result.exit_code == 0
        assert "Test tweet body" in result.output

    def test_review_nonexistent(self, runner, mock_pipeline):
        result = runner.invoke(main, ["review", "9999"])
        assert result.exit_code == 0
        assert "not found" in result.output.lower()


class TestApproveRejectCommands:

    def test_approve(self, runner, mock_pipeline):
        cid = mock_pipeline.kb.add_content(
            "tweet", "twitter", "Test", status="queued"
        )
        result = runner.invoke(main, ["approve", str(cid)])
        assert result.exit_code == 0
        assert "approved" in result.output.lower()

    def test_approve_invalid(self, runner, mock_pipeline):
        result = runner.invoke(main, ["approve", "9999"])
        assert result.exit_code == 0
        assert "error" in result.output.lower()

    def test_reject(self, runner, mock_pipeline):
        cid = mock_pipeline.kb.add_content(
            "tweet", "twitter", "Test", status="queued"
        )
        result = runner.invoke(main, ["reject", str(cid), "--reason", "Too aggressive"])
        assert result.exit_code == 0
        assert "rejected" in result.output.lower()


class TestPublishCommand:

    def test_publish_dry_run(self, runner, mock_pipeline):
        cid = mock_pipeline.kb.add_content(
            "tweet", "twitter", "Test tweet", status="approved"
        )
        result = runner.invoke(main, ["publish", str(cid), "--dry-run"])
        assert result.exit_code == 0
        assert "DRY RUN" in result.output

    def test_publish_mock(self, runner, mock_pipeline):
        cid = mock_pipeline.kb.add_content(
            "tweet", "twitter", "Test tweet", status="approved"
        )
        result = runner.invoke(main, ["publish", str(cid), "--mock"])
        assert result.exit_code == 0
        assert "Published" in result.output


class TestKBCommands:

    def test_kb_add_market(self, runner, mock_kb):
        result = runner.invoke(main, [
            "kb", "add-market",
            "--market", "houston",
            "--metric", "occupancy",
            "--value", "91.0%",
            "--period", "Q1 2026",
        ])
        assert result.exit_code == 0
        assert "Added" in result.output

    def test_kb_search(self, runner, mock_kb):
        result = runner.invoke(main, ["kb", "search", "houston"])
        assert result.exit_code == 0

    def test_kb_search_no_results(self, runner, mock_kb):
        result = runner.invoke(main, ["kb", "search", "nonexistentxyz"])
        assert result.exit_code == 0
        assert "No results" in result.output

    def test_kb_stats(self, runner, mock_kb):
        result = runner.invoke(main, ["kb", "stats"])
        assert result.exit_code == 0
        assert "Knowledge Base Statistics" in result.output


class TestSuggestCommand:

    def test_suggest(self, runner, mock_pipeline):
        result = runner.invoke(main, ["suggest"])
        assert result.exit_code == 0
        assert "Topic Suggestions" in result.output or "No suggestions" in result.output


class TestCalendarCommand:

    def test_calendar(self, runner, mock_pipeline):
        result = runner.invoke(main, ["calendar"])
        assert result.exit_code == 0
        assert "Content Calendar" in result.output


class TestMetricsCommand:

    def test_metrics_summary(self, runner, mock_kb):
        result = runner.invoke(main, ["metrics"])
        assert result.exit_code == 0
        assert "Content Performance" in result.output

    def test_metrics_no_data(self, runner, mock_kb):
        result = runner.invoke(main, ["metrics", "9999"])
        assert result.exit_code == 0
        assert "No metrics" in result.output
