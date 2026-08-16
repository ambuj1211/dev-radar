import json
from pathlib import Path


TOPICS_FILE = Path("config/topics.json")


def load_topics() -> dict[str, list[str]]:
    """Load topic categories and topics from configuration."""

    if not TOPICS_FILE.exists():
        raise FileNotFoundError(
            f"Topics configuration not found: {TOPICS_FILE}"
        )

    with TOPICS_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        data = json.load(file)

    categories = data.get("categories", {})

    if not isinstance(categories, dict):
        raise ValueError(
            "topics.json must contain a 'categories' object."
        )

    return categories


def get_all_topics() -> list[str]:
    """Return all configured topics."""

    categories = load_topics()

    topics = []

    for category_topics in categories.values():
        topics.extend(category_topics)

    return topics


def get_category_topics(
    category: str,
) -> list[str]:
    """Return topics belonging to a category."""

    categories = load_topics()

    return categories.get(category, [])