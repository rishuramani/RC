"""Configuration management for RC Marketing Bot."""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root
_PROJECT_ROOT = Path(__file__).parent.parent
load_dotenv(_PROJECT_ROOT / ".env")


# Paths
PROJECT_ROOT = _PROJECT_ROOT
DATA_DIR = _PROJECT_ROOT / "data"
DB_PATH = Path(os.getenv("DB_PATH", str(DATA_DIR / "rc_marketing.db")))
SEEDS_DIR = _PROJECT_ROOT / "seeds"

# Anthropic
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5-20250929")

# LinkedIn
LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID", "")
LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET", "")
LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN", "")

# Twitter/X
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY", "")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET", "")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN", "")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET", "")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN", "")

# Environment
ENV = os.getenv("ENV", "development")
IS_DEV = ENV == "development"

# Content defaults
MAX_TWEET_LENGTH = 280
MAX_LINKEDIN_LENGTH = 3000
BLOG_MIN_WORDS = 800
BLOG_MAX_WORDS = 1200

# Scanner configuration
SCANNER_TWITTER_QUERIES = [
    "multifamily houston",
    "workforce housing",
    "multifamily investment sunbelt",
    "houston real estate market",
    "phoenix multifamily",
    "CRE investment",
    "apartment investment",
]

SCANNER_LINKEDIN_QUERIES = [
    "multifamily real estate",
    "workforce housing investment",
    "houston apartment market",
]

# Web server
WEB_HOST = os.getenv("WEB_HOST", "127.0.0.1")
WEB_PORT = int(os.getenv("WEB_PORT", "5000"))
WEB_SECRET_KEY = os.getenv("WEB_SECRET_KEY", "rc-marketing-bot-dev-key")
