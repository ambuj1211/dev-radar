from datetime import datetime, timezone
from pathlib import Path


REPORT_DIRECTORY = Path("reports")


def generate_daily_report(
    repositories: list[dict],
    topic: str,
) -> Path:
    """Generate a Markdown report for the current radar run."""

    REPORT_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    report_path = REPORT_DIRECTORY / f"{today}.md"

    lines = [
        f"# 🚀 Dev Radar — {today}",
        "",
        f"**Topic:** {topic}",
        "",
        f"**Repositories analyzed:** {len(repositories)}",
        "",
        "---",
        "",
    ]

    for index, repository in enumerate(
        repositories,
        start=1,
    ):
        name = repository.get(
            "full_name",
            "Unknown",
        )

        score = repository.get(
            "radar_score",
            0,
        )

        stars = repository.get(
            "stargazers_count",
            0,
        )

        forks = repository.get(
            "forks_count",
            0,
        )

        language = repository.get(
            "language",
            "Unknown",
        )

        description = repository.get(
            "description",
        ) or "No description available."

        change_type = repository.get(
            "change_type",
            "unknown",
        )

        star_change = repository.get(
            "star_change",
            0,
        )

        score_change = repository.get(
            "score_change",
            0,
        )

        url = repository.get(
            "html_url",
            "",
        )

        lines.extend(
            [
                f"## {index}. [{name}]({url})",
                "",
                f"> {description}",
                "",
                "| Metric | Value |",
                "|---|---:|",
                f"| Radar Score | **{score:.2f}** |",
                f"| Stars | {stars:,} |",
                f"| Star Change | {star_change:+,} |",
                f"| Forks | {forks:,} |",
                f"| Score Change | {score_change:+.2f} |",
                f"| Language | {language} |",
                f"| Status | {change_type} |",
                "",
            ]
        )

    report_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    return report_path