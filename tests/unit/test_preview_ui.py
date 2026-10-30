from types import SimpleNamespace

import pytest

from scripts import preview_ui


def test_preview_refuses_reset_without_explicit_flag(monkeypatch):
    def forbidden():
        raise AssertionError("Settings must not be read before reset confirmation")

    monkeypatch.setattr(preview_ui, "Settings", forbidden)
    with pytest.raises(SystemExit, match="reset-test-db"):
        preview_ui.preview("populated", False)


def test_preview_refuses_missing_test_url(monkeypatch):
    monkeypatch.setattr(preview_ui, "_test_database_url", lambda: None)
    with pytest.raises(SystemExit, match="TEST_DATABASE_URL is required"):
        preview_ui.preview("populated", True)


def test_preview_refuses_production_endpoint_even_with_different_role(monkeypatch):
    monkeypatch.setattr(
        preview_ui, "_test_database_url", lambda: "postgresql://test@same-pooler.invalid/db"
    )
    monkeypatch.setattr(
        preview_ui,
        "Settings",
        lambda: SimpleNamespace(database_url="postgresql://prod@same.invalid/db"),
    )
    with pytest.raises(SystemExit, match="distinct test database endpoint"):
        preview_ui.preview("populated", True)


def test_preview_refuses_missing_family_anchor_before_migrations(monkeypatch):
    from pathlib import Path

    original = Path.read_text

    def missing_anchor(path, *args, **kwargs):
        text = original(path, *args, **kwargs)
        return (
            text.replace("const AGENCIES", "const MISSING_AGENCIES")
            if path.name == "family.html"
            else text
        )

    def forbidden(*args):
        raise AssertionError("Must refuse Family preview before database access")

    monkeypatch.setattr(Path, "read_text", missing_anchor)
    monkeypatch.setattr(preview_ui, "_test_database_url", forbidden)
    with pytest.raises(RuntimeError, match="Family preview replacement"):
        preview_ui.preview("populated", True)
