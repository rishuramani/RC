"""Data ingestion utilities for pulling market data into the knowledge base."""

from pathlib import Path
from typing import Optional

from bs4 import BeautifulSoup

from src.db.knowledge_base import KnowledgeBase


class DataIngestion:
    """Parses existing content files and ingests data into the knowledge base."""

    def __init__(self, knowledge_base: KnowledgeBase):
        self.kb = knowledge_base

    def ingest_html_file(self, file_path: str, source: str = "") -> int:
        """Parse an HTML file and extract text content."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        html = path.read_text(encoding="utf-8")
        soup = BeautifulSoup(html, "html.parser")

        # Remove script and style elements
        for tag in soup(["script", "style"]):
            tag.decompose()

        text = soup.get_text(separator="\n", strip=True)
        return len(text)

    def ingest_markdown_file(self, file_path: str) -> str:
        """Read a markdown file and return its content."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        return path.read_text(encoding="utf-8")

    def add_market_metric(self, market: str, metric: str, value: str,
                          period: Optional[str] = None,
                          source: Optional[str] = None) -> int:
        """Add a single market data point to the knowledge base."""
        return self.kb.add_market_data(market, metric, value, period, source)

    def add_firm_fact(self, category: str, key: str, value: str,
                      source: Optional[str] = None) -> int:
        """Add a firm fact to the knowledge base."""
        return self.kb.add_firm_fact(category, key, value, source)
