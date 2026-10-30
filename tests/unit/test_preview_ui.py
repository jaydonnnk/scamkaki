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
