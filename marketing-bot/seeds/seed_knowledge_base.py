"""Seed the knowledge base from existing RC content and JSON data files."""

import json
from pathlib import Path

from src.db.knowledge_base import KnowledgeBase


SEEDS_DIR = Path(__file__).parent


def seed_all(kb: KnowledgeBase):
    """Run all seed operations."""
    print("Seeding firm facts...")
    count = seed_firm_facts(kb)
    print(f"  Added {count} firm facts")

    print("Seeding brand rules...")
    count = seed_brand_rules(kb)
    print(f"  Added {count} brand rules")

    print("Seeding market data...")
    count = seed_market_data(kb)
    print(f"  Added {count} market data points")

    print("Seeding data sources...")
    count = seed_data_sources(kb)
    print(f"  Added {count} data sources")

    print("Seeding content calendar...")
    count = seed_content_calendar(kb)
    print(f"  Added {count} calendar entries")

    print("\nKnowledge base seeding complete!")


def seed_firm_facts(kb: KnowledgeBase) -> int:
    """Seed firm facts from firm_data.json."""
    data = _load_json("firm_data.json")
    count = 0

    for category, items in data.items():
        if isinstance(items, dict):
            for key, value in items.items():
                if isinstance(value, list):
                    # Handle lists (e.g., properties)
                    for i, item in enumerate(value):
                        kb.add_firm_fact(category, f"{key}_{i}", str(item),
                                         source="seed_data")
                        count += 1
                else:
                    kb.add_firm_fact(category, key, str(value),
                                     source="seed_data")
                    count += 1

    return count


def seed_brand_rules(kb: KnowledgeBase) -> int:
    """Seed brand rules from brand_guidelines.json."""
    data = _load_json("brand_guidelines.json")
    count = 0

    for rule_type, rules in data.items():
        for rule_item in rules:
            kb.add_brand_rule(
                rule_type=rule_type,
                rule=rule_item["rule"],
                example=rule_item.get("example"),
            )
            count += 1

    return count


def seed_market_data(kb: KnowledgeBase) -> int:
    """Seed market data from market_data.json."""
    data = _load_json("market_data.json")
    count = 0

    for market, periods in data.items():
        if market == "data_sources":
            continue  # Handled separately

        for period, metrics in periods.items():
            for metric, info in metrics.items():
                if isinstance(info, dict):
                    kb.add_market_data(
                        market=market,
                        metric=metric,
                        value=info["value"],
                        period=period,
                        source=info.get("source"),
                    )
                    count += 1

    return count


def seed_data_sources(kb: KnowledgeBase) -> int:
    """Seed data sources from market_data.json."""
    data = _load_json("market_data.json")
    sources = data.get("data_sources", [])
    count = 0

    for source in sources:
        kb.add_data_source(
            name=source["name"],
            url=source.get("url"),
            frequency=source.get("frequency"),
            notes=source.get("notes"),
        )
        count += 1

    return count


def seed_content_calendar(kb: KnowledgeBase) -> int:
    """Seed a basic content calendar for the upcoming weeks."""
    from datetime import date, timedelta

    today = date.today()
    entries = []

    # Weekly LinkedIn posts for the next 4 weeks
    for week in range(4):
        post_date = today + timedelta(days=(week * 7) + 1)  # Tuesdays
        entries.append({
            "content_type": "linkedin_post",
            "platform": "linkedin",
            "scheduled_date": post_date.isoformat(),
            "topic": None,  # To be filled by orchestrator
            "principal": "michael" if week % 2 == 0 else "bradley",
            "notes": f"Week {week + 1} LinkedIn post",
        })

    # Bi-weekly Twitter threads
    for week in range(0, 4, 2):
        post_date = today + timedelta(days=(week * 7) + 3)  # Thursdays
        entries.append({
            "content_type": "tweet_thread",
            "platform": "twitter",
            "scheduled_date": post_date.isoformat(),
            "topic": None,
            "principal": "michael" if week == 0 else "bradley",
            "notes": f"Bi-weekly Twitter thread",
        })

    # Monthly blog post
    entries.append({
        "content_type": "blog",
        "platform": "blog",
        "scheduled_date": (today + timedelta(days=14)).isoformat(),
        "topic": None,
        "principal": None,
        "notes": "Monthly blog article",
    })

    # Monthly market report
    entries.append({
        "content_type": "market_report",
        "platform": "report",
        "scheduled_date": (today + timedelta(days=21)).isoformat(),
        "topic": "houston",
        "principal": None,
        "notes": "Monthly Houston market update",
    })

    count = 0
    for entry in entries:
        kb.add_calendar_entry(**entry)
        count += 1

    return count


def _load_json(filename: str) -> dict:
    """Load a JSON file from the seeds directory."""
    path = SEEDS_DIR / filename
    with open(path, "r") as f:
        return json.load(f)


if __name__ == "__main__":
    from src.db.database import Database
    from src.config import DB_PATH

    db = Database(str(DB_PATH))
    db.initialize()
    kb = KnowledgeBase(db)
    seed_all(kb)
    db.close()
