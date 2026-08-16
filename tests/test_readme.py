from core.ai.readme import (
    preprocess_readme,
)


def test_empty_readme():

    assert preprocess_readme("") == ""


def test_remove_images():

    readme = """
    # Project

    ![Logo](https://example.com/logo.png)

    This is a project.
    """

    result = preprocess_readme(
        readme
    )

    assert "logo.png" not in result
    assert "This is a project." in result


def test_remove_html():

    readme = """
    # Project

    <div>Hello</div>

    Description.
    """

    result = preprocess_readme(
        readme
    )

    assert "<div>" not in result
    assert "Description." in result


def test_remove_markdown_links():

    readme = """
    [Documentation](https://example.com)

    Important information.
    """

    result = preprocess_readme(
        readme
    )

    assert "https://example.com" not in result
    assert "Documentation" in result


def test_length_limit():

    readme = "A" * 50000

    result = preprocess_readme(
        readme,
        max_length=1000,
    )

    assert len(result) <= 1050
    assert "[README truncated]" in result