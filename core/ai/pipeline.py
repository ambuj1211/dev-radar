import json
from pathlib import Path

from core.ai.readme import preprocess_readme
from core.ai.readme_storage import save_readme
from core.discovery.github import get_repository_readme


KAGGLE_INPUT_FILE = Path(
    "kaggle-worker/input/daily_input.json"
)


def prepare_repository_readme(
    repository: dict,
) -> str:
    """
    Download, preprocess and temporarily store
    a repository README.
    """

    full_name = repository.get(
        "full_name",
        "",
    )

    if "/" not in full_name:
        return ""

    owner, name = full_name.split(
        "/",
        1,
    )

    print(
        f"📖 Downloading README: {full_name}"
    )

    try:
        raw_readme = get_repository_readme(
            owner,
            name,
        )

    except Exception as exc:

        print(
            f"⚠️ Could not download README "
            f"for {full_name}: {exc}"
        )

        return ""

    if not raw_readme:

        print(
            f"⚠️ README not available: "
            f"{full_name}"
        )

        return ""

    processed_readme = preprocess_readme(
        raw_readme
    )

    if not processed_readme:

        print(
            f"⚠️ README became empty after "
            f"preprocessing: {full_name}"
        )

        return ""

    path = save_readme(
        full_name,
        processed_readme,
    )

    print(
        f"💾 README saved: {path}"
    )

    repository["readme_path"] = str(path)

    repository["readme_content"] = (
        processed_readme
    )

    return processed_readme


def prepare_kaggle_input(
    repositories: list[dict],
    date: str,
) -> Path:
    """
    Create the input JSON consumed by the
    Kaggle Qwen worker.
    """

    KAGGLE_INPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    input_repositories = []

    for repository in repositories:

        full_name = repository.get(
            "full_name"
        )

        if not full_name:
            continue

        readme = repository.get(
            "readme_content",
            "",
        )

        input_repositories.append(
            {
                "full_name": full_name,

                "description": repository.get(
                    "description"
                ),

                "language": repository.get(
                    "language"
                ),

                "stargazers_count": repository.get(
                    "stargazers_count",
                    0,
                ),

                "forks_count": repository.get(
                    "forks_count",
                    0,
                ),

                "radar_score": repository.get(
                    "radar_score",
                    0,
                ),

                "readme": readme,
            }
        )

    data = {
        "date": date,
        "repositories": input_repositories,
    }

    with KAGGLE_INPUT_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print(
        f"📦 Kaggle input created: "
        f"{KAGGLE_INPUT_FILE}"
    )

    print(
        f"📊 Repositories prepared: "
        f"{len(input_repositories)}"
    )

    return KAGGLE_INPUT_FILE