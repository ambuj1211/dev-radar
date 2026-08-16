from unittest.mock import patch

from core.ai.pipeline import (
    prepare_repository_readme,
)


def test_prepare_repository_readme():

    repository = {
        "full_name": "owner/test-repo",
    }

    fake_readme = """
# Test Repository

![Badge](https://example.com/badge.png)

This is a developer tool.

[Documentation](https://example.com/docs)
"""

    with patch(
        "core.ai.pipeline.get_repository_readme",
        return_value=fake_readme,
    ), patch(
        "core.ai.pipeline.save_readme",
    ) as save_mock:

        result = prepare_repository_readme(
            repository
        )

    assert result

    assert "badge.png" not in result

    assert "https://example.com/docs" not in result

    assert "This is a developer tool." in result

    save_mock.assert_called_once()