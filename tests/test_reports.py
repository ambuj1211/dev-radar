from core.reports.intelligence import (
    get_developer_value,
    get_problem_statement,
    get_repository_purpose,
    get_selection_reason,
    get_use_cases,
)


def sample_repository():
    return {
        "full_name": "owner/example",
        "description": "A developer productivity tool.",
        "language": "Python",
        "topics": [
            "developer-tools",
            "automation",
        ],
        "stargazers_count": 10000,
        "forks_count": 1500,
        "contributors_count": 120,
        "radar_score": 88.5,
        "developer_usefulness_score": 91.2,
    }


def test_repository_purpose():
    repository = sample_repository()

    result = get_repository_purpose(
        repository
    )

    assert "developer productivity" in result


def test_problem_statement():
    repository = sample_repository()

    result = get_problem_statement(
        repository
    )

    assert "developer productivity" in result


def test_developer_value():
    repository = sample_repository()

    result = get_developer_value(
        repository
    )

    assert "10,000" in result
    assert "1,500" in result


def test_use_cases():
    repository = sample_repository()

    result = get_use_cases(
        repository
    )

    assert len(result) > 0


def test_selection_reason():
    repository = sample_repository()

    result = get_selection_reason(
        repository
    )

    assert "88.50" in result
    assert "91.20" in result