import json
from pathlib import Path


HISTORY_FILE = Path("data/history.json")


def load_history() -> dict:
    """Load previous radar results."""

    if not HISTORY_FILE.exists():
        return {}

    with HISTORY_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_history(repositories: list[dict]) -> None:
    """Save the current radar results."""

    HISTORY_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    history = {}

    for repository in repositories:
        full_name = repository.get("full_name")

        if not full_name:
            continue

        history[full_name] = {
            "radar_score": repository.get(
                "radar_score",
                0,
            ),
            "stars": repository.get(
                "stargazers_count",
                0,
            ),
            "forks": repository.get(
                "forks_count",
                0,
            ),
        }

    with HISTORY_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            history,
            file,
            indent=2,
        )