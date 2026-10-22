import pytest
from fastapi.testclient import TestClient

from scamkaki.app.main import app, get_bolna
from scamkaki.lib.db import connect, migrate
from scamkaki.lib.env import get_settings
from tests.support.fakes import FakeBolna


@pytest.fixture
def db(test_settings):
    migrate(test_settings.database_url)
    with connect(test_settings.database_url) as conn:
        conn.execute("truncate calls, guardian_checks restart identity")
    return test_settings.database_url


@pytest.fixture
def bolna() -> FakeBolna:
    return FakeBolna()


@pytest.fixture
def client(test_settings, db, bolna):
    app.dependency_overrides[get_settings] = lambda: test_settings
    app.dependency_overrides[get_bolna] = lambda: bolna
    yield TestClient(app)
    app.dependency_overrides.clear()
