from core.filtering.repository import (
    filter_repositories,
    is_recently_updated,
)


def test_recent_repository():
    repository = {
        "updated_at": "2026-08-15T12:00:00Z",
    }

    assert is_recently_updated(repository, max_age_days=180)


def test_old_repository():
    repository = {
        "updated_at": "2020-01-01T12:00:00Z",
    }

    assert not is_recently_updated(repository, max_age_days=180)


def test_filter_repositories():
    repositories = [
        {
            "full_name": "good/repo",
            "stargazers_count": 500,
            "archived": False,
            "updated_at": "2026-08-15T12:00:00Z",
        },
        {
            "full_name": "low-stars/repo",
            "stargazers_count": 10,
            "archived": False,
            "updated_at": "2026-08-15T12:00:00Z",
        },
        {
            "full_name": "archived/repo",
            "stargazers_count": 500,
            "archived": True,
            "updated_at": "2026-08-15T12:00:00Z",
        },
    ]

    result = filter_repositories(
        repositories,
        min_stars=100,
        max_age_days=180,
    )

    assert len(result) == 1
    assert result[0]["full_name"] == "good/repo"