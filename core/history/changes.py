def detect_changes(
    repositories: list[dict],
    previous_history: dict,
) -> list[dict]:
    """Calculate changes compared with the previous radar run."""

    results = []

    for repository in repositories:
        name = repository.get("full_name")

        previous = previous_history.get(name)

        current_stars = repository.get(
            "stargazers_count",
            0,
        )

        current_score = repository.get(
            "radar_score",
            0,
        )

        if previous is None:
            repository["change_type"] = "new"
            repository["star_change"] = 0
            repository["score_change"] = 0

        else:
            repository["change_type"] = "existing"

            repository["star_change"] = (
                current_stars
                - previous.get("stars", 0)
            )

            repository["score_change"] = round(
                current_score
                - previous.get("radar_score", 0),
                2,
            )

        results.append(repository)

    return results