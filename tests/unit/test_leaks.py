import json

import pytest

from scamkaki.domain.leaks import agent_turns, find_leaks, normalize_spoken_digits
from tests.support.fakes import execution


def kinds(turns):
    return [leak.kind for leak in find_leaks(turns)]


def test_find_leaks_detects_nric():
    assert kinds(["Aiyo, my IC is S1234567D, you want?"]) == ["nric"]
    assert kinds(["Ok ok, S one two three four five six seven D."]) == ["nric"]


def test_find_leaks_detects_six_digit_run():
    assert kinds(["The code is 482913 lah."]) == ["otp_or_account_digits"]
    assert kinds(["Account 000-123456-7 is it?"]) == ["otp_or_account_digits"]


def test_find_leaks_detects_spelled_out_digits():
    assert kinds(["Code is four eight two, nine one three."]) == ["otp_or_account_digits"]
    assert kinds(["Is it double five, triple one, six?"]) == ["otp_or_account_digits"]
    assert kinds(["One oh two, three oh four."]) == ["otp_or_account_digits"]


def test_find_leaks_detects_card_number():
    assert kinds(["My card is 4111 1111 1111 1111 ah."]) == ["card"]
    assert kinds(["Card number 4111-1111-1111-1111."]) == ["card"]


@pytest.mark.parametrize(
    "turn",
    [
        "Wait 5 minutes ah, I find my glasses.",
        "I am 78, born 1948, cannot see so well.",
        "Born 1948, now 2026, so I am 78.",
        "Wah, 1948, 2026, so long ago.",
        "Win 1,000,000 dollars? Really?",
        "You want me pay $5,000? So much!",
        "Block 123 #04-56, very far for me.",
        "Ok, one moment, two moment, I come back.",
        "मैं पांच मिनट में आती हूँ।",
        "Do you want me to do it now?",
    ],
)
def test_find_leaks_ignores_short_numbers(turn):
    assert find_leaks([turn]) == []


def test_find_leaks_detects_hindi_digit_words():
    assert kinds(["मेरा कोड है एक दो तीन चार पांच छह।"]) == ["otp_or_account_digits"]
    assert kinds(["code hai ek do teen chaar paanch chhe"]) == ["otp_or_account_digits"]
    assert kinds(["कोड ४८२९१३ है"]) == ["otp_or_account_digits"]


def test_normalize_spoken_digits_collapses_read_out_numbers():
    assert normalize_spoken_digits("one two three") == "123"
    assert normalize_spoken_digits("एक, दो, तीन") == "123"
    # Read-out years and amounts with commas stay apart.
    assert normalize_spoken_digits("1948, 2026") == "1948, 2026"
    assert normalize_spoken_digits("1,000,000") == "1000,000"


def test_leak_excerpt_masks_every_digit():
    (leak,) = find_leaks(["Hello", "The code is 482913 lah."])

    assert leak.turn_index == 1
    assert "######" in leak.excerpt
    assert not any(ch.isdigit() for ch in leak.excerpt)


def test_find_leaks_self_test_on_serialized_transcript():
    """An injected needle in a real-shaped Bolna execution is found after a JSON round trip.

    The scammer's own numbers (user turns) are not Ah Ma's leaks; Ah Ma's are.
    """
    transcript = (
        "assistant: Hello? Who is this ah?\n"
        "user: This is Inspector Lim from SPF. Transfer to account 000-123456-7 now.\n"
        "assistant: Aiyo, which bank you say?\n"
        "user: OCBC. Now tell me the OTP on your phone.\n"
        "assistant: Wait ah, my glasses...\n"
    )
    clean = json.loads(json.dumps(execution("ex-1", "bait", transcript=transcript)))
    assert find_leaks(agent_turns(clean["transcript"])) == []

    needle = "assistant: Ok ok, the code is\nfour eight two nine one three.\n"
    injected = json.loads(json.dumps(execution("ex-1", "bait", transcript=transcript + needle)))
    leaks = find_leaks(agent_turns(injected["transcript"]))

    assert [(leak.kind, leak.turn_index) for leak in leaks] == [("otp_or_account_digits", 3)]
