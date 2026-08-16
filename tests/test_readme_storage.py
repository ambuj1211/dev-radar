from core.ai.readme_storage import (
    cleanup_old_readmes,
    repository_filename,
    save_readme,
)


def test_repository_filename():

    path = repository_filename(
        "owner/my-repo",
        "2026-08-16",
    )

    assert (
        path.name
        == "2026-08-16_owner_my-repo_readme.md"
    )


def test_save_readme(tmp_path, monkeypatch):

    import core.ai.readme_storage as storage

    monkeypatch.setattr(
        storage,
        "README_DIRECTORY",
        tmp_path,
    )

    path = save_readme(
        "owner/test-repo",
        "# Test Repository",
        "2026-08-16",
    )

    assert path.exists()

    assert (
        path.read_text(
            encoding="utf-8"
        )
        == "# Test Repository"
    )


def test_cleanup_old_readmes(
    tmp_path,
    monkeypatch,
):

    import core.ai.readme_storage as storage

    monkeypatch.setattr(
        storage,
        "README_DIRECTORY",
        tmp_path,
    )

    old_file = (
        tmp_path
        / "2026-08-14_old_repo_readme.md"
    )

    recent_file = (
        tmp_path
        / "2026-08-16_new_repo_readme.md"
    )

    old_file.write_text(
        "old",
        encoding="utf-8",
    )

    recent_file.write_text(
        "recent",
        encoding="utf-8",
    )

    deleted = cleanup_old_readmes(
        keep_days=2
    )

    assert old_file in deleted
    assert not old_file.exists()
    assert recent_file.exists()