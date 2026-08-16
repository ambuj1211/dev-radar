from datetime import datetime, timezone
from pathlib import Path

from core.reports.intelligence import (
    get_developer_value,
    get_problem_statement,
    get_repository_purpose,
    get_selection_reason,
    get_use_cases,
)


REPORT_DIRECTORY = Path("reports")


def generate_daily_report(
    repositories: list[dict],
    topic: str,
) -> Path:
    """Generate the detailed Markdown report."""

    REPORT_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    today = datetime.now(
        timezone.utc
    ).strftime(
        "%Y-%m-%d"
    )

    report_path = (
        REPORT_DIRECTORY
        / f"{today}.md"
    )

    lines = [
        "# 🚀 Dev Radar — Daily Developer Report",
        "",
        f"**Date:** {today}",
        "",
        f"**Topic:** {topic}",
        "",
        f"**Repositories selected:** {len(repositories)}",
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

        description = (
            repository.get(
                "description"
            )
            or "No description available."
        )

        url = repository.get(
            "html_url",
            "",
        )

        stars = repository.get(
            "stargazers_count",
            0,
        )

        forks = repository.get(
            "forks_count",
            0,
        )

        contributors = repository.get(
            "contributors_count",
            0,
        )

        language = (
            repository.get(
                "language"
            )
            or "Unknown"
        )

        radar_score = repository.get(
            "radar_score",
            0,
        )

        usefulness_score = repository.get(
            "developer_usefulness_score",
            0,
        )

        star_change = repository.get(
            "star_change",
            0,
        )

        score_change = repository.get(
            "score_change",
            0,
        )

        change_type = repository.get(
            "change_type",
            "new",
        )

        license_name = (
            repository.get(
                "license"
            )
            or "Not specified"
        )

        homepage = (
            repository.get(
                "homepage"
            )
            or "Not specified"
        )

        purpose = get_repository_purpose(
            repository
        )

        problem = get_problem_statement(
            repository
        )

        developer_value = get_developer_value(
            repository
        )

        use_cases = get_use_cases(
            repository
        )

        selection_reason = get_selection_reason(
            repository
        )

        lines.extend(
            [
                f"# {index}. {name}",
                "",
                f"> {description}",
                "",
                "## 💡 What is it?",
                "",
                purpose,
                "",
                "## 🎯 Purpose",
                "",
                purpose,
                "",
                "## 🧩 What problem does it solve?",
                "",
                problem,
                "",
                "## 👨‍💻 Why is it important for developers?",
                "",
                developer_value,
                "",
                "## 🛠️ Potential use cases",
                "",
            ]
        )

        for use_case in use_cases:
            lines.append(
                f"- {use_case}"
            )

        lines.extend(
            [
                "",
                "## 📊 GitHub adoption",
                "",
                "| Metric | Value |",
                "|---|---:|",
                f"| ⭐ Stars | {stars:,} |",
                f"| ⭐ Star Change | {star_change:+,} |",
                f"| 🍴 Forks | {forks:,} |",
                f"| 👥 Contributors | {contributors:,} |",
                f"| 📝 Language | {language} |",
                f"| 📜 License | {license_name} |",
                f"| Status | {change_type} |",
                "",
                "## 🏆 Dev Radar scores",
                "",
                "| Score | Value |",
                "|---|---:|",
                f"| Radar Score | **{radar_score:.2f}** |",
                (
                    "| Developer Usefulness Score | "
                    f"**{usefulness_score:.2f}** |"
                ),
                f"| Score Change | {score_change:+.2f} |",
                "",
                "## 🔥 Why Dev Radar selected it",
                "",
                selection_reason,
                "",
                "## 🔗 Repository",
                "",
                f"[Open on GitHub]({url})",
                "",
            ]
        )

        if homepage != "Not specified":
            lines.extend(
                [
                    f"**Homepage:** {homepage}",
                    "",
                ]
            )

        lines.extend(
            [
                "---",
                "",
            ]
        )

    report_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    return report_path