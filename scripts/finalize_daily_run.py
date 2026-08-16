import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from core.history.store import save_history


INPUT_FILE = Path(
    "kaggle-worker/input/daily_input.json"
)

AI_OUTPUT_FILE = Path(
    "kaggle-worker/output/ai_analysis.json"
)

README_DIRECTORY = Path(
    "readmes"
)


def load_json(path: Path) -> dict:
    """Load a JSON file."""

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {path}"
        )

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def validate_ai_output(
    ai_data: dict,
) -> list[dict]:
    """Validate that every repository was analyzed successfully."""

    if ai_data.get("status") != "success":
        raise RuntimeError(
            "AI analysis status is not success."
        )

    repositories = ai_data.get(
        "repositories",
        [],
    )

    if not repositories:
        raise RuntimeError(
            "AI analysis contains no repositories."
        )

    failed = [
        repository
        for repository in repositories
        if repository.get("status") != "success"
    ]

    if failed:
        names = ", ".join(
            repository.get(
                "full_name",
                "Unknown",
            )
            for repository in failed
        )

        raise RuntimeError(
            f"AI analysis failed for: {names}"
        )

    return repositories


def save_successful_history(
    input_data: dict,
    ai_data: dict,
) -> None:
    """
    Save repositories to history only after
    successful AI analysis and email delivery.
    """

    input_repositories = {
        repository.get("full_name"): repository
        for repository in input_data.get(
            "repositories",
            [],
        )
        if repository.get("full_name")
    }

    successful_repositories = []

    for ai_repository in ai_data.get(
        "repositories",
        [],
    ):
        full_name = ai_repository.get(
            "full_name"
        )

        if not full_name:
            continue

        repository = input_repositories.get(
            full_name
        )

        if repository:
            successful_repositories.append(
                repository
            )

    if not successful_repositories:
        raise RuntimeError(
            "No successful repositories found "
            "for history."
        )

    save_history(
        successful_repositories
    )

    print(
        f"✅ Saved "
        f"{len(successful_repositories)} "
        f"repositories to history."
    )


def cleanup_old_readmes() -> None:
    """
    Delete README files older than two days.

    README filenames are expected to follow:

        YYYY-MM-DD_reponame_readme.md
    """

    if not README_DIRECTORY.exists():
        print(
            "ℹ️ README directory does not exist."
        )
        return

    today = datetime.now(
        timezone.utc
    ).date()

    cutoff_date = today - timedelta(
        days=2
    )

    deleted = 0
    kept = 0

    for path in README_DIRECTORY.glob(
        "*_readme.md"
    ):
        try:
            date_text = path.name[:10]

            file_date = datetime.strptime(
                date_text,
                "%Y-%m-%d",
            ).date()

        except ValueError:
            print(
                f"⚠️ Skipping README with "
                f"invalid date: {path.name}"
            )
            continue

        if file_date < cutoff_date:

            path.unlink()

            deleted += 1

            print(
                f"🗑️ Deleted old README: "
                f"{path.name}"
            )

        else:
            kept += 1

    print(
        f"🧹 README cleanup complete. "
        f"Deleted: {deleted}, "
        f"Kept: {kept}"
    )


def main() -> None:
    print(
        "🏁 Finalizing Dev Radar run"
    )

    input_data = load_json(
        INPUT_FILE
    )

    ai_data = load_json(
        AI_OUTPUT_FILE
    )

    # This validates the AI result again.
    # This script should only be reached after
    # the email has already been sent successfully.
    validate_ai_output(
        ai_data
    )

    # Save history.
    save_successful_history(
        input_data,
        ai_data,
    )

    # Remove README files older than two days.
    cleanup_old_readmes()

    print(
        "✅ Daily Dev Radar run finalized."
    )


if __name__ == "__main__":
    main()