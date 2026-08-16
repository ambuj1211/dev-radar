from unittest.mock import patch

from core.discovery.radar import (
    discover_candidates,
)


def test_discover_candidates_removes_duplicates():

    fake_results = [
        {
            "full_name": "owner/repo1",
        },
        {
            "full_name": "owner/repo2",
        },
    ]

    with patch(
        "core.discovery.radar.search_repositories",
        return_value=fake_results,
    ):

        results = discover_candidates(
            topics=[
                "AI",
                "LLM",
            ],
            min_stars=100,
            per_topic=10,
        )

    names = [
        repository["full_name"]
        for repository in results
    ]

    assert len(names) == 2

    assert len(names) == len(
        set(names)
    )


def test_topic_is_recorded():

    fake_results = [
        {
            "full_name": "owner/repo1",
        },
    ]

    with patch(
        "core.discovery.radar.search_repositories",
        return_value=fake_results,
    ):

        results = discover_candidates(
            topics=["AI"],
        )

    assert results[0]["radar_topic"] == "AI"