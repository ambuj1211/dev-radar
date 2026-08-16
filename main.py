from core.discovery.github import (
    enrich_repository,
    search_repositories,
)
from core.filtering.repository import filter_repositories
from core.ranking.repository import rank_repositories
from core.history.changes import detect_changes
from core.history.store import (
    load_history,
    save_history,
)
from core.reports.daily import generate_daily_report
from core.reports.json import generate_json_report


def run_radar(
    topic: str,
    language: str | None = None,
    min_stars: int = 100,
    max_age_days: int = 180,
    limit: int = 10,
) -> list[dict]:
    """Run the complete Dev Radar pipeline."""

    print(f"\n🔎 Searching GitHub for: {topic}")

    repositories = search_repositories(
        topic=topic,
        language=language,
        min_stars=min_stars,
        per_page=limit,
    )

    print(f"📦 Discovered: {len(repositories)} repositories")

    repositories = filter_repositories(
        repositories,
        min_stars=min_stars,
        max_age_days=max_age_days,
    )

    print(f"🔍 After filtering: {len(repositories)} repositories")

    enriched_repositories = []

    for repository in repositories:
        try:
            enriched = enrich_repository(repository)
            enriched_repositories.append(enriched)
        except Exception as exc:
            print(
                f"⚠️ Could not enrich "
                f"{repository.get('full_name')}: {exc}"
            )

    repositories = enriched_repositories

    print(
        f"📊 Enriched: "
        f"{len(repositories)} repositories"
    )

    repositories = rank_repositories(repositories)

    previous_history = load_history()

    repositories = detect_changes(
        repositories,
        previous_history,
    )

    save_history(repositories)

    return repositories


def print_report(repositories: list[dict]) -> None:
    """Print ranked repositories to the terminal."""

    print("\n" + "=" * 70)
    print("🚀 DEV RADAR")
    print("=" * 70)

    if not repositories:
        print("No repositories found.")
        return

    for index, repository in enumerate(repositories, start=1):
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
            f"   Change      : "
            f"{repository.get('change_type', 'unknown')}"
        )

        print(
            f"   ⭐ Change    : "
            f"{repository.get('star_change', 0):+,}"
        )

        print(
            f"   Score Δ     : "
            f"{repository.get('score_change', 0):+.2f}"
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
            f"   🔗 URL       : "
            f"{repository.get('html_url', '')}"
        )
        


if __name__ == "__main__":
    topic = "artificial intelligence"

    results = run_radar(
        topic=topic,
        language="Python",
        min_stars=1000,
        max_age_days=180,
        limit=10,
    )

    print_report(results)

    report_path = generate_daily_report(
        results,
        topic,
    )

    json_path = generate_json_report(
        results,
        topic,
    )
    
    print(
        f"🌐 Web data generated: {json_path}"
    )
    print(
        f"\n📄 Report generated: {report_path}"
    )