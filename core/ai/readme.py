import re


MAX_README_LENGTH = 30000


def preprocess_readme(
    readme: str,
    max_length: int = MAX_README_LENGTH,
) -> str:
    """
    Clean and preprocess a GitHub README before
    sending it to an LLM.
    """

    if not readme:
        return ""

    text = readme

    # --------------------------------------------------
    # Remove HTML comments
    # --------------------------------------------------

    text = re.sub(
        r"<!--.*?-->",
        "",
        text,
        flags=re.DOTALL,
    )

    # --------------------------------------------------
    # Remove HTML tags
    # --------------------------------------------------

    text = re.sub(
        r"<[^>]+>",
        " ",
        text,
    )

    # --------------------------------------------------
    # Remove Markdown images
    # Example:
    # ![logo](https://...)
    # --------------------------------------------------

    text = re.sub(
        r"!\[[^\]]*\]\([^)]+\)",
        "",
        text,
    )

    # --------------------------------------------------
    # Remove image/reference links
    # --------------------------------------------------

    text = re.sub(
        r"\[([^\]]*)\]\([^)]+\)",
        r"\1",
        text,
    )

    # --------------------------------------------------
    # Remove badges
    # --------------------------------------------------

    text = re.sub(
        r"\[!\[[^\]]*\]\([^)]+\)\]\([^)]+\)",
        "",
        text,
    )

    # --------------------------------------------------
    # Remove excessive horizontal separators
    # --------------------------------------------------

    text = re.sub(
        r"[-_*]{3,}",
        "\n",
        text,
    )

    # --------------------------------------------------
    # Normalize whitespace
    # --------------------------------------------------

    text = re.sub(
        r"[ \t]+",
        " ",
        text,
    )

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text,
    )

    text = text.strip()

    # --------------------------------------------------
    # Limit input size
    # --------------------------------------------------

    if len(text) > max_length:
        text = text[:max_length]

        # Avoid cutting in the middle of a word.
        last_space = text.rfind(" ")

        if last_space > 0:
            text = text[:last_space]

        text += "\n\n[README truncated]"

    return text