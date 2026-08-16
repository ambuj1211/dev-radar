from datetime import datetime, timedelta, timezone
from pathlib import Path
import re


README_DIRECTORY = Path("readmes")


def repository_filename(
    repository_name: str,
    date: str | None = None,
) -> Path:
    """Create a safe dated README filename."""

    if date is None:
        date = datetime.now(
            timezone.utc
        ).strftime("%Y-%m-%d")

    safe_name = re.sub(
        r"[^A-Za-z0-9._-]+",
        "_",
        repository_name,
    )

    return (
        README_DIRECTORY
        / f"{date}_{safe_name}_readme.md"
    )


def save_readme(
    repository_name: str,
    content: str,
    date: str | None = None,
) -> Path:
    """Save a processed README temporarily."""

    README_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    path = repository_filename(
        repository_name,
        date,
    )

    path.write_text(
        content,
        encoding="utf-8",
    )

    return path


def cleanup_old_readmes(
    keep_days: int = 2,
) -> list[Path]:
    """
    Delete README files whose filename date is older
    than the allowed retention period.
    """

    if not README_DIRECTORY.exists():
        return []

    today = datetime.now(
        timezone.utc
    ).date()

    cutoff_date = (
        today - timedelta(
            days=keep_days - 1
        )
    )

    deleted = []

    pattern = re.compile(
        r"^(\d{4}-\d{2}-\d{2})_.+_readme\.md$"
    )

    for path in README_DIRECTORY.glob(
        "*_readme.md"
    ):

        match = pattern.match(
            path.name
        )

        if not match:
            continue

        try:
            file_date = datetime.strptime(
                match.group(1),
                "%Y-%m-%d",
            ).date()

        except ValueError:
            continue

        if file_date < cutoff_date:

            path.unlink()

            deleted.append(path)

    return deleted