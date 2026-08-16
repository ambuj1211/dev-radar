from core.discovery.github import search_repositories


def test_search_repositories():
    repositories = search_repositories(
        topic="artificial intelligence",
        language="Python",
        min_stars=1000,
        per_page=5,
    )

    assert isinstance(repositories, list)
    assert len(repositories) <= 5

    if repositories:
        assert "full_name" in repositories[0]
        assert "html_url" in repositories[0]