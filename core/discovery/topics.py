from core.config_loader import load_topics


def get_topics(
    categories: list[str] | None = None,
) -> list[str]:
    """
    Return all topics from the requested categories.

    If categories is None, return topics from all
    configured categories.
    """

    topic_config = load_topics()

    # Support both:
    #
    # {
    #     "categories": {
    #         ...
    #     }
    # }
    #
    # and:
    #
    # {
    #     "AI": [...],
    #     ...
    #     }
    #
    if "categories" in topic_config:
        topic_config = topic_config["categories"]

    if categories is None:
        categories = list(
            topic_config.keys()
        )

    topics = []

    for category in categories:

        category_topics = topic_config.get(
            category,
            [],
        )

        for topic in category_topics:

            if topic not in topics:
                topics.append(topic)

    return topics


def get_category_topics(
    category: str,
) -> list[str]:
    """
    Return all topics belonging to one category.
    """

    topic_config = load_topics()

    if "categories" in topic_config:
        topic_config = topic_config["categories"]

    return topic_config.get(
        category,
        [],
    )


def get_categories() -> list[str]:
    """
    Return all configured category names.
    """

    topic_config = load_topics()

    if "categories" in topic_config:
        topic_config = topic_config["categories"]

    return list(
        topic_config.keys()
    )