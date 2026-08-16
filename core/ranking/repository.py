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

def growth_score(
    star_change: int,
    stars: int,
) -> float:
    """Calculate repository growth score from star growth."""

    if stars <= 0:
        return 0.0

    if star_change <= 0:
        return 0.0

    growth_ratio = star_change / stars

    score = min(
        growth_ratio * 10000,
        100,
    )

    return round(score, 2)


def developer_usefulness_score(
    repository: dict,
) -> float:
    """
    Estimate how useful a repository is to developers.

    Signals:
    - Forks
    - Contributors
    - Documentation
    - Issues/community
    - Repository type
    """

    forks = repository.get(
        "forks_count",
        0,
    )

    contributors = repository.get(
        "contributors_count",
        0,
    )

    open_issues = repository.get(
        "open_issues_count",
        0,
    )

    description = repository.get(
        "description",
        "",
    )

    homepage = repository.get(
        "homepage",
        "",
    )

    forks_score = min(
        math.log10(max(forks, 1)) / 4 * 100,
        100,
    )

    contributors_score = min(
        math.log10(
            max(contributors, 1)
        ) / 3 * 100,
        100,
    )

    community_score_value = min(
        math.log10(
            max(open_issues, 1)
        ) / 4 * 100,
        100,
    )

    documentation_score = 0.0

    if description:
        documentation_score += 60

    if homepage:
        documentation_score += 40

    score = (
        forks_score * 0.30
        + contributors_score * 0.30
        + community_score_value * 0.20
        + documentation_score * 0.20
    )

    return round(
        min(score, 100),
        2,
    )

def calculate_usefulness_score(
    repository: dict,
) -> dict:
    """Calculate the developer usefulness score."""

    popularity = popularity_score(
        repository.get(
            "stargazers_count",
            0,
        ),
        repository.get(
            "forks_count",
            0,
        ),
    )

    freshness = freshness_score(
        repository.get(
            "updated_at",
            "",
        )
    )

    community = community_score(
        repository.get(
            "open_issues_count",
            0,
        ),
        repository.get(
            "contributors_count",
            0,
        ),
    )

    growth = growth_score(
        repository.get(
            "star_change",
            0,
        ),
        repository.get(
            "stargazers_count",
            0,
        ),
    )

    usefulness = developer_usefulness_score(
        repository
    )

    score = (
        popularity * 0.25
        + freshness * 0.20
        + community * 0.15
        + growth * 0.15
        + usefulness * 0.25
    )

    return {
        "popularity": round(popularity, 2),
        "freshness": round(freshness, 2),
        "community": round(community, 2),
        "growth": round(growth, 2),
        "developer_usefulness": round(
            usefulness,
            2,
        ),
        "usefulness_score": round(
            score,
            2,
        ),
    }

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
    """Rank repositories using quality and developer usefulness."""

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

        usefulness = calculate_usefulness_score(
            repository
        )

        repository[
            "usefulness_breakdown"
        ] = usefulness

        repository[
            "developer_usefulness_score"
        ] = usefulness[
            "usefulness_score"
        ]

        ranked.append(repository)

    ranked.sort(
        key=lambda repository: (
            repository[
                "developer_usefulness_score"
            ],
            repository["radar_score"],
        ),
        reverse=True,
    )

    return ranked