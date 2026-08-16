from datetime import datetime, timezone


def is_recently_updated(
    repository: dict,
    max_age_days: int = 180,
) -> bool:
    """Return True if the repository was updated within max_age_days."""

    updated_at = repository.get("updated_at")

    if not updated_at:
        return False

    updated = datetime.fromisoformat(
        updated_at.replace("Z", "+00:00")
    )

    age = datetime.now(timezone.utc) - updated

    return age.days <= max_age_days


def filter_repositories(
    repositories: list[dict],
    min_stars: int = 100,
    max_age_days: int = 180,
    exclude_archived: bool = True,
) -> list[dict]:
    """Filter GitHub repositories according to Dev Radar criteria."""

    filtered = []

    for repository in repositories:
        if repository.get("stargazers_count", 0) < min_stars:
            continue

        if exclude_archived and repository.get("archived", False):
            continue

        if not is_recently_updated(repository, max_age_days):
            continue

        filtered.append(repository)

    return filtered