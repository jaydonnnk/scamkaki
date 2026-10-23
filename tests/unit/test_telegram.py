import logging

import httpx

from scamkaki.integrations import telegram

TOKEN = "123456:secret-bot-token"


def test_send_message_never_raises_or_logs_the_token(monkeypatch, caplog):
    def unreachable(url, **kwargs):
        raise httpx.ConnectError(f"cannot reach {url}")

    monkeypatch.setattr(httpx, "post", unreachable)
    with caplog.at_level(logging.DEBUG):
        assert telegram.send_message(TOKEN, "42", "hello") is False

    assert "ConnectError" in caplog.text
    assert TOKEN not in caplog.text


def test_send_message_is_true_only_when_telegram_says_ok(monkeypatch):
    def reply(status, body):
        request = httpx.Request("POST", "https://api.telegram.org")
        return lambda url, **kwargs: httpx.Response(status, json=body, request=request)

    monkeypatch.setattr(httpx, "post", reply(200, {"ok": True}))
    assert telegram.send_message(TOKEN, "42", "hello") is True
    monkeypatch.setattr(httpx, "post", reply(200, {"ok": False}))
    assert telegram.send_message(TOKEN, "42", "hello") is False
    monkeypatch.setattr(httpx, "post", reply(401, {"ok": False}))
    assert telegram.send_message(TOKEN, "42", "hello") is False
