from types import SimpleNamespace

from scamkaki.app.main import family_url


def settings(**values):
    return SimpleNamespace(**values)


def test_family_url_joins_base_and_token():
    url = family_url(settings(app_base_url="https://a.test/", family_link_token="tok"))

    assert url == "https://a.test/family/tok"


def test_family_url_is_empty_until_both_parts_are_set():
    assert family_url(settings(app_base_url="https://a.test", family_link_token="")) == ""
    assert family_url(settings(app_base_url="", family_link_token="tok")) == ""
