import json
from pathlib import Path


HISTORY_FILE = Path("core/history/seen_repositories.json")
CHANGE_HISTORY_FILE = Path(
    "core/history/repository_history.json"
)

def load_history() -> set[str]:
    """Load previously sent repository names."""

    if not HISTORY_FILE.exists():
        return set()

    with HISTORY_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        data = json.load(file)

    return set(
        data.get("repositories", [])
    )


def save_history(
    repositories: list[dict],
) -> None:
    """Save repositories that have already been sent."""

    HISTORY_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    existing = load_history()

    for repository in repositories:
        full_name = repository.get(
            "full_name"
        )

        if full_name:
            existing.add(full_name)

    data = {
        "repositories": sorted(existing)
    }

    with HISTORY_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
            indent=2,
        )


def remove_seen_repositories(
    repositories: list[dict],
) -> list[dict]:
    """Remove repositories that were already sent."""

    seen = load_history()

    return [
        repository
        for repository in repositories
        if repository.get("full_name")
        not in seen
    ]


def select_top_new_repositories(
    repositories: list[dict],
    count: int = 3,
) -> list[dict]:
    """Select the top unique repositories that have not been sent."""

    new_repositories = remove_seen_repositories(
        repositories
    )

    unique_repositories = []
    selected_names = set()

    for repository in new_repositories:
        full_name = repository.get("full_name")

        if not full_name:
            continue

        if full_name in selected_names:
            continue

        selected_names.add(full_name)
        unique_repositories.append(repository)

        if len(unique_repositories) >= count:
            break

    return unique_repositories


def load_repository_history() -> dict:
    """Load previous repository metrics."""

    if not CHANGE_HISTORY_FILE.exists():
        return {}

    with CHANGE_HISTORY_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:

        data = json.load(file)

    return data.get(
        "repositories",
        {},
    )