from scamkaki.lib.env import Settings
from tests.conftest import ROOT

# Names read only by the test suite, never by the app.
TEST_ONLY_NAMES = {"TEST_DATABASE_URL"}


def test_env_example_lists_exactly_settings_names():
    lines = (ROOT / ".env.example").read_text().splitlines()
    entries = [line for line in lines if line and not line.startswith("#")]

    assert all(line.endswith("=") for line in entries), "values must stay out of .env.example"
    names = {line.removesuffix("=") for line in entries}
    assert names - TEST_ONLY_NAMES == {name.upper() for name in Settings.model_fields}
