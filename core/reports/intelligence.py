def get_repository_purpose(
    repository: dict,
) -> str:
    """Build a concise purpose statement from repository metadata."""

    description = repository.get(
        "description"
    )

    if description:
        return description.strip()

    topics = repository.get(
        "topics",
        []
    )

    if topics:
        topic_text = ", ".join(
            topics[:5]
        )

        return (
            f"A developer project related to "
            f"{topic_text}."
        )

    return (
        "Purpose information is not available "
        "from the repository metadata."
    )


def get_problem_statement(
    repository: dict,
) -> str:
    """Describe the problem using available repository information."""

    description = repository.get(
        "description"
    )

    topics = repository.get(
        "topics",
        []
    )

    if description:
        return (
            f"It addresses the developer need described "
            f"by the project as: {description.strip()}"
        )

    if topics:
        topic_text = ", ".join(
            topics[:5]
        )

        return (
            f"It targets developer workflows and problems "
            f"related to {topic_text}."
        )

    return (
        "The specific problem statement could not be "
        "determined from the available GitHub metadata."
    )


def get_developer_value(
    repository: dict,
) -> str:
    """Explain why the repository may matter to developers."""

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

    language = repository.get(
        "language"
    ) or "multiple technologies"

    return (
        f"This project may be useful to developers working "
        f"with {language}. It has {stars:,} stars, "
        f"{forks:,} forks, and approximately "
        f"{contributors:,} contributors, providing signals "
        f"of community adoption and practical interest."
    )


def get_use_cases(
    repository: dict,
) -> list[str]:
    """Generate conservative use-case suggestions."""

    topics = [
        topic.lower()
        for topic in repository.get(
            "topics",
            []
        )
    ]

    language = (
        repository.get(
            "language"
        ) or ""
    ).lower()

    use_cases = []

    if any(
        topic in topics
        for topic in [
            "machine-learning",
            "machine learning",
            "artificial-intelligence",
            "ai",
            "llm",
            "generative-ai",
        ]
    ):
        use_cases.append(
            "Building or experimenting with AI/ML applications"
        )

    if any(
        topic in topics
        for topic in [
            "web",
            "web-development",
            "frontend",
            "backend",
            "full-stack",
        ]
    ):
        use_cases.append(
            "Building web applications and developer services"
        )

    if any(
        topic in topics
        for topic in [
            "developer-tools",
            "cli",
            "automation",
            "developer-productivity",
        ]
    ):
        use_cases.append(
            "Improving developer workflows and automation"
        )

    if language:
        use_cases.append(
            f"Developing applications using {language}"
        )

    if not use_cases:
        use_cases.append(
            "Exploring, integrating, or extending the project's capabilities"
        )

    return use_cases[:4]


def get_selection_reason(
    repository: dict,
) -> str:
    """Explain why Dev Radar selected the repository."""

    radar_score = repository.get(
        "radar_score",
        0,
    )

    usefulness_score = repository.get(
        "developer_usefulness_score",
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

    return (
        f"Dev Radar selected this repository because it "
        f"has a Radar Score of {radar_score:.2f} and a "
        f"Developer Usefulness Score of "
        f"{usefulness_score:.2f}, together with "
        f"{stars:,} stars and {forks:,} forks."
    )