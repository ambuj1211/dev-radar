import math
from datetime import datetime, timezone


def freshness_score(
    updated_at: str,
    max_age_days: int = 180,
) -> float:
    """Calculate a 0-100 freshness score."""

    if not updated_at:
        return 0.0

    updated = datetime.fromisoformat(
        updated_at.replace("Z", "+00:00")
    )

    age_days = (
        datetime.now(timezone.utc) - updated
    ).total_seconds() / 86400

    if age_days <= 0:
        return 100.0

    score = 100 * (
        1 - age_days / max_age_days
    )

    return max(
        0.0,
        min(100.0, score),
    )


def popularity_score(
    stars: int,
    forks: int,
) -> float:
    """Calculate popularity based on stars and forks."""

    stars_score = min(
        math.log10(max(stars, 1)) / 5 * 100,
        100,
    )

    forks_score = min(
        math.log10(max(forks, 1)) / 4 * 100,
        100,
    )

    return (
        stars_score * 0.7
        + forks_score * 0.3
    )


def community_score(
    open_issues: int,
    contributors: int,
) -> float:
    """Calculate community activity score."""

    issues_score = min(
        math.log10(max(open_issues, 1)) / 4 * 100,
        100,
    )

    contributor_score = min(
        math.log10(max(contributors, 1)) / 3 * 100,
        100,
    )

    return (
        issues_score * 0.3
        + contributor_score * 0.7
    )


def calculate_score_breakdown(
    repository: dict,
) -> dict:
    """Return the individual components of the radar score."""

    popularity = popularity_score(
        repository.get("stargazers_count", 0),
        repository.get("forks_count", 0),
    )

    freshness = freshness_score(
        repository.get("updated_at", ""),
    )

    community = community_score(
        repository.get("open_issues_count", 0),
        repository.get("contributors_count", 0),
    )

    return {
        "popularity": round(popularity, 2),
        "freshness": round(freshness, 2),
        "community": round(community, 2),
    }


def calculate_radar_score(
    repository: dict,
) -> float:
    """Calculate the final Dev Radar score from 0-100."""

    breakdown = calculate_score_breakdown(
        repository
    )

    score = (
        breakdown["popularity"] * 0.40
        + breakdown["freshness"] * 0.35
        + breakdown["community"] * 0.25
    )

    return round(score, 2)


def rank_repositories(
    repositories: list[dict],
) -> list[dict]:
    """Add radar score and score breakdown."""

    ranked = []

    for repository in repositories:

        repository = repository.copy()

        breakdown = calculate_score_breakdown(
            repository
        )

        repository["score_breakdown"] = breakdown

        repository["radar_score"] = round(
            breakdown["popularity"] * 0.40
            + breakdown["freshness"] * 0.35
            + breakdown["community"] * 0.25,
            2,
        )

        ranked.append(repository)

    ranked.sort(
        key=lambda repo: repo["radar_score"],
        reverse=True,
    )

    return ranked