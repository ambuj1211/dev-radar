from core.config_loader import load_topics


def get_daily_topics(
    categories: list[str] | None = None,
) -> list[str]:
    """
    Return topics that should be searched during
    the current radar run.
    """

    topic_config = load_topics()

    if categories is None:
        categories = [
            "AI",
            "Programming",
            "Web",
            "DevOps / Cloud",
            "Developer Tools",
        ]

    topics = []

    for category in categories:

        category_topics = topic_config.get(
            category,
            [],
        )

        topics.extend(category_topics)

    return topics