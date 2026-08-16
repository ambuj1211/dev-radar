from datetime import datetime, timezone

from core.discovery.github import (
    enrich_repository,
    search_repositories,
)

from core.filtering.repository import (
    filter_repositories,
)

from core.ranking.repository import (
    rank_repositories,
)

from core.history.changes import (
    detect_changes,
)

from core.history.store import (
    load_history as load_metric_history,
)

from core.history.repository import (
    select_top_new_repositories,
)

from core.reports.daily import (
    generate_daily_report,
)

from core.reports.json import (
    generate_json_report,
)

from core.discovery.radar import (
    discover_candidates,
)

from core.discovery.daily_topics import (
    get_daily_topics,
    get_daily_topic_group_name,
)

from core.ai.pipeline import (
    prepare_repository_readme,
    prepare_kaggle_input,
)


def run_radar(
    topic: str,
    language: str | None = None,
    min_stars: int = 100,
    max_age_days: int = 180,
    limit: int = 50,
) -> list[dict]:
    """
    Run the complete Dev Radar pipeline
    for a single topic.
    """

    print(
        f"\n🔎 Searching GitHub for: {topic}"
    )

    # --------------------------------------------------
    # 1. DISCOVERY
    # --------------------------------------------------

    repositories = search_repositories(
        topic=topic,
        language=language,
        min_stars=min_stars,
        per_page=limit,
    )

    print(
        f"📦 Discovered: "
        f"{len(repositories)} repositories"
    )

    # --------------------------------------------------
    # 2. FILTERING
    # --------------------------------------------------

    repositories = filter_repositories(
        repositories,
        min_stars=min_stars,
        max_age_days=max_age_days,
    )

    print(
        f"🔍 After filtering: "
        f"{len(repositories)} repositories"
    )

    # --------------------------------------------------
    # 3. ENRICHMENT
    # --------------------------------------------------

    enriched_repositories = []

    for repository in repositories:

        try:

            enriched = enrich_repository(
                repository
            )

            enriched_repositories.append(
                enriched
            )

        except Exception as exc:

            print(
                f"⚠️ Could not enrich "
                f"{repository.get('full_name')}: "
                f"{exc}"
            )

    repositories = enriched_repositories

    print(
        f"📊 Enriched: "
        f"{len(repositories)} repositories"
    )

    # --------------------------------------------------
    # 4. RANKING
    # --------------------------------------------------

    repositories = rank_repositories(
        repositories
    )

    print(
        f"🏆 Ranked: "
        f"{len(repositories)} repositories"
    )

    # --------------------------------------------------
    # 5. CHANGE DETECTION
    # --------------------------------------------------

    previous_history = load_metric_history()

    repositories = detect_changes(
        repositories,
        previous_history,
    )

    # --------------------------------------------------
    # 6. REMOVE PREVIOUSLY SENT REPOSITORIES
    # --------------------------------------------------

    repositories = select_top_new_repositories(
        repositories,
        count=3,
    )

    print(
        f"🎯 Selected: "
        f"{len(repositories)} new repositories"
    )

    return repositories


def run_daily_radar(
    min_stars: int = 1000,
    max_age_days: int = 180,
    per_topic: int = 10,
) -> list[dict]:
    """
    Discover and rank repositories across
    the configured daily topics.
    """

    # --------------------------------------------------
    # 1. GET DAILY TOPICS
    # --------------------------------------------------

    topics = get_daily_topics()

    print(
        "\n🌐 Daily topics:"
    )

    for topic in topics:

        print(
            f"   • {topic}"
        )

    # --------------------------------------------------
    # 2. DISCOVER CANDIDATES
    # --------------------------------------------------

    repositories = discover_candidates(
        topics=topics,
        min_stars=min_stars,
        per_topic=per_topic,
    )

    print(
        f"\n📦 Candidate pool: "
        f"{len(repositories)}"
    )

    # --------------------------------------------------
    # 3. FILTERING
    # --------------------------------------------------

    repositories = filter_repositories(
        repositories,
        min_stars=min_stars,
        max_age_days=max_age_days,
    )

    print(
        f"🔍 After filtering: "
        f"{len(repositories)}"
    )

    # --------------------------------------------------
    # 4. ENRICHMENT
    # --------------------------------------------------

    enriched = []

    for repository in repositories:

        try:

            enriched.append(
                enrich_repository(
                    repository
                )
            )

        except Exception as exc:

            print(
                f"⚠️ Could not enrich "
                f"{repository.get('full_name')}: "
                f"{exc}"
            )

    repositories = enriched

    print(
        f"📊 Enriched: "
        f"{len(repositories)}"
    )

    # --------------------------------------------------
    # 5. RANKING
    # --------------------------------------------------

    repositories = rank_repositories(
        repositories
    )

    print(
        f"🏆 Ranked: "
        f"{len(repositories)}"
    )

    # --------------------------------------------------
    # 6. CHANGE DETECTION
    # --------------------------------------------------

    previous_history = load_metric_history()

    repositories = detect_changes(
        repositories,
        previous_history,
    )

    # --------------------------------------------------
    # 7. SELECT TOP 3 NEW REPOSITORIES
    # --------------------------------------------------

    repositories = select_top_new_repositories(
        repositories,
        count=3,
    )

    print(
        f"🎯 Final selection: "
        f"{len(repositories)}"
    )

    # --------------------------------------------------
    # 8. PREPARE README FILES
    # --------------------------------------------------

    if not repositories:

        print(
            "\n⚠️ No new repositories available."
        )

        return []

    print(
        "\n📚 Preparing repository READMEs..."
    )

    for repository in repositories:

        prepare_repository_readme(
            repository
        )

    # --------------------------------------------------
    # 9. CREATE KAGGLE INPUT
    # --------------------------------------------------

    today = datetime.now(
        timezone.utc
    ).strftime("%Y-%m-%d")

    prepare_kaggle_input(
        repositories,
        today,
    )

    return repositories


def print_report(
    repositories: list[dict],
) -> None:
    """Print selected repositories to the terminal."""

    print(
        "\n" + "=" * 70
    )

    print(
        "🚀 DEV RADAR"
    )

    print(
        "=" * 70
    )

    if not repositories:

        print(
            "No new repositories found."
        )

        return

    for index, repository in enumerate(
        repositories,
        start=1,
    ):

        print(
            f"\n#{index} "
            f"{repository.get('full_name', 'Unknown')}"
        )

        print(
            f"   Radar Score : "
            f"{repository.get('radar_score', 0):.2f}"
        )

        print(
            f"   ⭐ Stars     : "
            f"{repository.get('stargazers_count', 0):,}"
        )

        print(
            f"   ⭐ Change    : "
            f"{repository.get('star_change', 0):+,}"
        )

        print(
            f"   🍴 Forks     : "
            f"{repository.get('forks_count', 0):,}"
        )

        print(
            f"   📝 Language  : "
            f"{repository.get('language') or 'Unknown'}"
        )

        print(
            f"   Change      : "
            f"{repository.get('change_type', 'unknown')}"
        )

        print(
            f"   Score Δ     : "
            f"{repository.get('score_change', 0):+.2f}"
        )

        print(
            f"   🔗 URL       : "
            f"{repository.get('html_url', '')}"
        )

        # ----------------------------------------------
        # Score breakdown
        # ----------------------------------------------

        breakdown = repository.get(
            "score_breakdown",
            {},
        )

        if breakdown:

            print(
                "\n   Score Breakdown:"
            )

            print(
                f"      Popularity : "
                f"{breakdown.get('popularity', 0):.2f}"
            )

            print(
                f"      Freshness  : "
                f"{breakdown.get('freshness', 0):.2f}"
            )

            print(
                f"      Community  : "
                f"{breakdown.get('community', 0):.2f}"
            )

        # ----------------------------------------------
        # README status
        # ----------------------------------------------

        readme_path = repository.get(
            "readme_path"
        )

        if readme_path:

            print(
                f"   📖 README    : "
                f"{readme_path}"
            )

        else:

            print(
                "   📖 README    : Not available"
            )


def generate_reports(
    repositories: list[dict],
    topic: str,
) -> tuple[str, str]:
    """
    Generate the daily Markdown report
    and web JSON.
    """

    report_path = generate_daily_report(
        repositories,
        topic,
    )

    json_path = generate_json_report(
        repositories,
        topic,
    )

    print(
        f"\n📄 Report generated: "
        f"{report_path}"
    )

    print(
        f"🌐 Web data generated: "
        f"{json_path}"
    )

    return (
        str(report_path),
        str(json_path),
    )


if __name__ == "__main__":

    # --------------------------------------------------
    # DAILY RADAR
    # --------------------------------------------------

    results = run_daily_radar(
        min_stars=1000,
        max_age_days=180,
        per_topic=10,
    )

    # --------------------------------------------------
    # TERMINAL REPORT
    # --------------------------------------------------

    print_report(
        results
    )

    # --------------------------------------------------
    # FILE REPORTS
    # --------------------------------------------------

    if results:

        generate_reports(
            results,
            "Daily Dev Radar",
        )

    else:

        print(
            "\n⚠️ No new repositories available."
        )