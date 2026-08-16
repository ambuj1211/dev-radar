from core.history.repository import (
    remove_seen_repositories,
    select_top_new_repositories,
)


def test_remove_seen_repositories():

    repositories = [
        {"full_name": "owner/repo1"},
        {"full_name": "owner/repo2"},
        {"full_name": "owner/repo3"},
    ]

    result = remove_seen_repositories(
        repositories
    )

    assert isinstance(result, list)


def test_select_top_three():

    repositories = [
        {
            "full_name": f"owner/repo{i}",
            "radar_score": 100 - i,
        }
        for i in range(10)
    ]

    result = select_top_new_repositories(
        repositories,
        count=3,
    )

    assert len(result) <= 3


def test_no_duplicate_repositories():

    repositories = [
        {"full_name": "owner/repo1"},
        {"full_name": "owner/repo1"},
        {"full_name": "owner/repo2"},
    ]

    result = select_top_new_repositories(
        repositories,
        count=3,
    )

    names = [
        repository["full_name"]
        for repository in result
    ]

    assert len(names) == len(set(names))