import os

import requests
from dotenv import load_dotenv


load_dotenv()

GITHUB_API_BASE = "https://api.github.com"
SEARCH_REPOSITORIES_URL = f"{GITHUB_API_BASE}/search/repositories"


def get_headers() -> dict[str, str]:
    """Return headers used for GitHub API requests."""

    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    token = os.getenv("GITHUB_TOKEN")

    if token:
        headers["Authorization"] = f"Bearer {token}"

    return headers


def search_repositories(
    topic: str,
    language: str | None = None,
    min_stars: int = 0,
    per_page: int = 10,
) -> list[dict]:
    """Search GitHub repositories."""

    query_parts = [topic]

    if language:
        query_parts.append(f"language:{language}")

    if min_stars > 0:
        query_parts.append(f"stars:>={min_stars}")

    params = {
        "q": " ".join(query_parts),
        "sort": "stars",
        "order": "desc",
        "per_page": per_page,
    }

    response = requests.get(
        SEARCH_REPOSITORIES_URL,
        headers=get_headers(),
        params=params,
        timeout=15,
    )

    response.raise_for_status()

    return response.json().get("items", [])


def get_repository(
    owner: str,
    name: str,
) -> dict:
    """Get detailed information about a GitHub repository."""

    url = f"{GITHUB_API_BASE}/repos/{owner}/{name}"

    response = requests.get(
        url,
        headers=get_headers(),
        timeout=15,
    )

    response.raise_for_status()

    return response.json()


def enrich_repository(repository: dict) -> dict:
    """Add detailed GitHub repository information."""

    full_name = repository.get("full_name", "")

    if "/" not in full_name:
        return repository

    owner, name = full_name.split("/", 1)

    details = get_repository(
        owner,
        name,
    )

    enriched = repository.copy()

    enriched.update(
        {
            "description": details.get(
                "description"
            ),

            "forks_count": details.get(
                "forks_count",
                0,
            ),

            "open_issues_count": details.get(
                "open_issues_count",
                0,
            ),

            "watchers_count": details.get(
                "watchers_count",
                0,
            ),

            "language": details.get(
                "language"
            ),

            "created_at": details.get(
                "created_at"
            ),

            "updated_at": details.get(
                "updated_at"
            ),

            "pushed_at": details.get(
                "pushed_at"
            ),

            "archived": details.get(
                "archived",
                False,
            ),

            "license": (
                details.get("license") or {}
            ).get(
                "spdx_id"
            ),

            "homepage": details.get(
                "homepage"
            ),

            "topics": details.get(
                "topics",
                []
            ),

            "default_branch": details.get(
                "default_branch",
                "main",
            ),

            "has_wiki": details.get(
                "has_wiki",
                False,
            ),

            "has_issues": details.get(
                "has_issues",
                False,
            ),

            "has_discussions": details.get(
                "has_discussions",
                False,
            ),
        }
    )

    enriched["contributors_count"] = (
        get_contributor_count(
            owner,
            name,
        )
    )

    return enriched


def get_contributor_count(
    owner: str,
    name: str,
) -> int:
    """Return the approximate number of repository contributors."""

    url = (
        f"{GITHUB_API_BASE}/repos/"
        f"{owner}/{name}/contributors"
    )

    params = {
        "per_page": 1,
        "anon": "true",
    }

    response = requests.get(
        url,
        headers=get_headers(),
        params=params,
        timeout=15,
    )

    response.raise_for_status()

    # GitHub provides the total through the last-page URL
    # when pagination is available.
    link = response.headers.get("Link", "")

    if 'rel="last"' in link:
        for part in link.split(","):
            if 'rel="last"' in part:
                url_part = part.split(";")[0].strip()
                last_url = url_part.strip("<>")

                from urllib.parse import parse_qs, urlparse

                query = parse_qs(
                    urlparse(last_url).query
                )

                return int(query["page"][0])

    data = response.json()

    return len(data)

def get_repository_readme(
    owner: str,
    name: str,
) -> str:
    """Download the repository README as Markdown."""

    url = (
        f"{GITHUB_API_BASE}/repos/"
        f"{owner}/{name}/readme"
    )

    headers = get_headers()
    headers["Accept"] = "application/vnd.github.raw+json"

    response = requests.get(
        url,
        headers=headers,
        timeout=15,
    )

    if response.status_code == 404:
        return ""

    response.raise_for_status()

    return response.text