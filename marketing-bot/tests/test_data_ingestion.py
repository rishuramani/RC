"""Tests for data ingestion utilities."""

import pytest
import tempfile
from pathlib import Path

from src.pipeline.data_ingestion import DataIngestion


@pytest.fixture
def ingestion(seeded_kb):
    return DataIngestion(seeded_kb)


class TestDataIngestion:

    def test_ingest_html_file(self, ingestion, tmp_path):
        html_file = tmp_path / "test.html"
        html_file.write_text(
            "<html><body><h1>Test</h1><p>Houston market data</p></body></html>"
        )
        length = ingestion.ingest_html_file(str(html_file), source="test")
        assert length > 0

    def test_ingest_html_strips_scripts(self, ingestion, tmp_path):
        html_file = tmp_path / "test.html"
        html_file.write_text(
            "<html><body><script>alert('x')</script><p>Content</p></body></html>"
        )
        length = ingestion.ingest_html_file(str(html_file))
        assert length > 0

    def test_ingest_html_nonexistent(self, ingestion):
        with pytest.raises(FileNotFoundError):
            ingestion.ingest_html_file("/nonexistent/file.html")

    def test_ingest_markdown_file(self, ingestion, tmp_path):
        md_file = tmp_path / "test.md"
        md_file.write_text("# Houston Market Update\n\nOccupancy: 90.4%")
        content = ingestion.ingest_markdown_file(str(md_file))
        assert "90.4%" in content

    def test_ingest_markdown_nonexistent(self, ingestion):
        with pytest.raises(FileNotFoundError):
            ingestion.ingest_markdown_file("/nonexistent/file.md")

    def test_add_market_metric(self, ingestion):
        mid = ingestion.add_market_metric(
            "houston", "cap_rate", "5.5%", "Q4 2025", "CoStar"
        )
        assert mid > 0

    def test_add_firm_fact(self, ingestion):
        fid = ingestion.add_firm_fact(
            "track_record", "new_deal_irr", "22%", "internal"
        )
        assert fid > 0
