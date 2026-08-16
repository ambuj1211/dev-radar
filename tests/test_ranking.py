from core.ranking.repository import (
    calculate_radar_score,
    freshness_score,
    rank_repositories,
    developer_usefulness_score,
    growth_score,
)

def test_growth_score():

    score = growth_score(
        star_change=1000,
        stars=10000,
    )

    assert score > 0
    assert score <= 100


def test_zero_growth():

    score = growth_score(
        star_change=0,
        stars=10000,
    )

    assert score == 0


def test_developer_usefulness():

    repository = {
        "forks_count": 5000,
        "contributors_count": 200,
        "open_issues_count": 100,
        "description": "Developer tool",
        "homepage": "https://example.com",
    }

    score = developer_usefulness_score(
        repository
    )

    assert score > 0
    assert score <= 100

def test_freshness_score():
    score = freshness_score(
        "2026-08-15T12:00:00Z",
        max_age_days=180,
    )

    assert 0 <= score <= 100


def test_radar_score():
    repository = {
        "stargazers_count": 10000,
        "forks_count": 1000,
        "open_issues_count": 100,
        "contributors_count": 50,
        "updated_at": "2026-08-15T12:00:00Z",
    }

    score = calculate_radar_score(repository)

    assert 0 <= score <= 100


def test_rank_repositories():
    repositories = [
        {
            "full_name": "repo/low",
            "stargazers_count": 100,
            "forks_count": 10,
            "open_issues_count": 5,
            "contributors_count": 2,
            "updated_at": "2026-08-15T12:00:00Z",
        },
        {
            "full_name": "repo/high",
            "stargazers_count": 100000,
            "forks_count": 10000,
            "open_issues_count": 500,
            "contributors_count": 100,
            "updated_at": "2026-08-15T12:00:00Z",
        },
    ]

    result = rank_repositories(repositories)

    assert result[0]["full_name"] == "repo/high"
    assert result[0]["radar_score"] >= result[1]["radar_score"]