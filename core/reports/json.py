import json
from pathlib import Path


def generate_json_report(
    repositories: list[dict],
    topic: str,
) -> Path:
    """Generate JSON data for the web dashboard."""

    output_directory = Path("web/public/data")
    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = output_directory / "radar.json"

    data = {
        "topic": topic,
        "repositories": repositories,
    }

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False,
        )

    return output_path