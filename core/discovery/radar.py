from core.discovery.github import (
    search_repositories,
)


def discover_candidates(
    topics: list[str],
    min_stars: int = 100,
    per_topic: int = 10,
) -> list[dict]:
    """
    Search GitHub across multiple topics and build
    one unique candidate pool.
    """

    candidates = []
    seen = set()

    for topic in topics:

        print(
            f"\n🔎 Searching topic: {topic}"
        )

        try:

            repositories = search_repositories(
                topic=topic,
                min_stars=min_stars,
                per_page=per_topic,
            )

        except Exception as exc:

            print(
                f"⚠️ Search failed for "
                f"{topic}: {exc}"
            )

            continue

        print(
            f"   Found: {len(repositories)}"
        )

        for repository in repositories:

            full_name = repository.get(
                "full_name"
            )

            if not full_name:
                continue

            if full_name in seen:
                continue

            seen.add(full_name)

            repository = repository.copy()

            repository["radar_topic"] = topic

            candidates.append(
                repository
            )

    print(
        f"\n📦 Total unique candidates: "
        f"{len(candidates)}"
    )

    return candidates