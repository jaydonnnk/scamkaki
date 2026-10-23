"""Telegram Bot API: one message to the family chat. Never raises."""

import logging

import httpx

API_URL = "https://api.telegram.org"

log = logging.getLogger("scamkaki")
# httpx logs request URLs, and the bot token is part of the URL.
logging.getLogger("httpx").setLevel(logging.WARNING)


def send_message(bot_token: str, chat_id: str, text: str) -> bool:
    try:
        response = httpx.post(
            f"{API_URL}/bot{bot_token}/sendMessage",
            json={"chat_id": chat_id, "text": text},
            timeout=5,
        )
        ok = response.status_code == 200 and response.json().get("ok") is True
    except Exception as error:
        # The exception text can carry the URL, so log only its type.
        log.warning("telegram send failed: %s", type(error).__name__)
        return False
    if not ok:
        log.warning("telegram send rejected: HTTP %s", response.status_code)
    return ok
