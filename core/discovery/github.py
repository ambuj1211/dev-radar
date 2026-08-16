import os

import requests
from dotenv import load_dotenv


load_dotenv()

GITHUB_API_URL = "https://api.github.com/search/repositories"


def search_repositories(
    topic: str,
    language: str | None = None,
    min_stars: int = 0,
    per_page: int = 10,
) -> list[dict]:
    """Search GitHub repositories matching the given criteria."""

    query_parts = [topic]

    if language:
        query_parts.append(f"language:{language}")

    if min_stars > 0:
        query_parts.append(f"stars:>={min_stars}")

    headers = {
        "Accept": "application/vnd.github+json",
    }

    token = os.getenv("GITHUB_TOKEN")

    if token:
        headers["Authorization"] = f"Bearer {token}"

    params = {
        "q": " ".join(query_parts),
        "sort": "stars",
        "order": "desc",
        "per_page": per_page,
    }

    response = requests.get(
        GITHUB_API_URL,
        headers=headers,
        params=params,
        timeout=15,
    )

    response.raise_for_status()

    data = response.json()

    return data.get("items", [])