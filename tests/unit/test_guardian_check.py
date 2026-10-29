import copy
from contextlib import contextmanager
from types import SimpleNamespace

import pytest

from scripts import check as runner


@pytest.fixture
def courier():
    case = {
        "id": "en-courier-paid-01",
        "language": "en",
        "kind": "scam",
        "expect": {
            "agency": "courier",
            "demand": "card_details",
            "channel": "sms",
            "tactics": ["link_fee"],
            "acted": "gave_code_or_card",
            "verdict": "likely_scam",
        },
    }
    check = {**case["expect"], "similar_count": 0, "language": "en", "alert_status": "sent"}
    transcript = (
        "user: I already paid the courier fee with my card and the code.\n"
        "assistant: Call your bank now on the number on the back of your card, and call "
        "ScamShield at one seven nine nine. This is likely a courier impersonation scam. "
        "I have alerted your family.\n"
    )
    return case, check, transcript


def test_guardian_evidence_accepts_complete_paid_case(courier):
    case, check, transcript = courier
    assert runner.guardian_errors(case, check, "time", transcript, 120) == []


@pytest.mark.parametrize(
    "field,value",
    [
        ("agency", "other"),
        ("demand", "other"),
        ("channel", "other"),
        ("tactics", []),
        ("acted", "none"),
        ("language", "hi"),
    ],
)
def test_guardian_evidence_rejects_each_wrong_field(courier, field, value):
    case, check, transcript = courier
    check[field] = value
    assert field in runner.guardian_errors(case, check, "time", transcript, 120)


@pytest.mark.parametrize("link", ["none", "time x2", "id x2"])
def test_guardian_evidence_rejects_ambiguous_tool_check(courier, link):
    case, check, transcript = courier
    assert "tool_count" in runner.guardian_errors(case, check, link, transcript, 120)


def test_guardian_evidence_requires_bank_instruction_first(courier):
    case, check, transcript = courier
    transcript = transcript.replace("assistant: Call", "assistant: This is likely a scam. Call")
    assert "urgent_advice" in runner.guardian_errors(case, check, "time", transcript, 120)


@pytest.mark.parametrize("prior", ["This is likely a scam.", "This call is definitely safe."])
def test_guardian_urgent_advice_must_start_first_verdict(courier, prior):
    case, check, transcript = courier
    transcript = f"assistant: {prior}\n" + transcript
    assert "urgent_advice" in runner.guardian_errors(case, check, "time", transcript, 120)


@pytest.mark.parametrize("transcript", ["", "assistant: This call is definitely safe.\n"])
def test_guardian_requires_actual_spoken_verdict_and_warning(transcript):
    cases = runner.json.loads((runner.ROOT / "seed/scripts.json").read_text())["cases"]
    case = next(c for c in cases if c["id"] == "en-telco-minlaw-01")
    check = {**case["expect"], "language": "en", "similar_count": 0, "alert_status": "sent"}
    assert "spoken_verdict" in runner.guardian_errors(case, check, "id", transcript, 60)


def test_guardian_rejects_certainty_even_with_correct_verdict_later(courier):
    case, check, transcript = courier
    transcript = "assistant: This call is definitely safe.\n" + transcript
    assert "unsafe_certainty" in runner.guardian_errors(case, check, "time", transcript, 120)


def test_guardian_evidence_requires_1799_and_bank(courier):
    case, check, transcript = courier
    transcript = transcript.replace("one seven nine nine", "your family")
    assert "urgent_advice" in runner.guardian_errors(case, check, "time", transcript, 120)


@pytest.mark.parametrize("kind,alert", [("scam", "failed"), ("scam", None), ("legit", "pending")])
def test_guardian_evidence_alert_only_on_likely_scam(courier, kind, alert):
    case, check, transcript = courier
    check["alert_status"] = alert
    if kind == "legit":
        check["verdict"] = "unclear"
    assert "alert" in runner.guardian_errors(case, check, "time", transcript, 120)


@pytest.mark.parametrize("duration", [0, 181])
def test_guardian_evidence_rejects_missing_or_over_target_duration(courier, duration):
    case, check, transcript = courier
    assert "duration" in runner.guardian_errors(case, check, "time", transcript, duration)


def test_guardian_evidence_detects_leak_on_actual_serialized_transcript(courier):
    case, check, transcript = courier
    transcript += "assistant: My code is four eight two nine one three.\n"
    assert "leak" in runner.guardian_errors(case, check, "time", transcript, 120)


def test_guardian_evidence_self_test_rejects_disabled_scanner(courier, monkeypatch):
    case, check, transcript = courier
    monkeypatch.setattr(runner, "find_leaks", lambda turns: [])
    assert "leak_self_test" in runner.guardian_errors(case, check, "time", transcript, 120)


def test_guardian_evidence_requires_spoken_repeat_count(courier):
    case, check, transcript = courier
    check["similar_count"] = 3
    assert "repeat" in runner.guardian_errors(case, check, "time", transcript, 120)
    transcript += "assistant: Same script heard three times this week.\n"
    assert runner.guardian_errors(case, check, "time", transcript, 120) == []


def test_guardian_evidence_requires_grandson_call_back(courier):
    case, _, _ = courier
    case = copy.deepcopy(case)
    case.update(id="en-legit-grandson-01", kind="legit")
    case["expect"].update(
        agency="friend_family", demand="transfer", acted="none", tactics=[], verdict="unclear"
    )
    check = {**case["expect"], "language": "en", "similar_count": 0, "alert_status": None}
    transcript = "assistant: Not sure. Please call your family before doing anything.\n"
    assert "call_back" in runner.guardian_errors(case, check, "id", transcript, 60)
    transcript += (
        "assistant: Call them back on the number you already have, "
        "not the one that contacted you.\n"
    )
    assert runner.guardian_errors(case, check, "id", transcript, 60) == []


def test_guardian_checker_cannot_pass_with_missing_legit_calls(monkeypatch, capsys):
    cases = runner.json.loads((runner.ROOT / "seed/scripts.json").read_text())["cases"]
    cases = [c for c in cases if c["for"] == "guardian" and c["language"] == "en"]
    runs = {c["id"]: {"run_id": c["id"]} for c in cases if c["kind"] == "scam"}
    by_id = {c["id"]: c for c in cases}
    monkeypatch.setattr(
        runner, "get_settings", lambda: SimpleNamespace(bolna_api_key="fake", database_url="fake")
    )
    monkeypatch.setattr(runner, "latest_runs", lambda line: runs)
    monkeypatch.setattr(
        runner,
        "BolnaClient",
        lambda key: SimpleNamespace(
            get_execution=lambda run_id: {"conversation_duration": 90, "transcript": ""}
        ),
    )
    monkeypatch.setattr(
        runner,
        "guardian_check",
        lambda url, run: (
            {
                **by_id[run["run_id"]]["expect"],
                "similar_count": 0,
                "alert_status": "sent",
                "language": "en",
            },
            "time",
        ),
    )
    monkeypatch.setattr(runner, "stored", lambda url, run_id: {"fixture_case": run_id, "leaks": []})
    # Isolate this regression from the other evidence checks.
    monkeypatch.setattr(runner, "guardian_errors", lambda *args: [], raising=False)

    @contextmanager
    def connect(url):
        yield None

    monkeypatch.setattr(runner, "connect", connect)
    monkeypatch.setattr(runner.store, "scripts_this_week", lambda conn: [])
    assert runner.check_guardian("en") == 1
    assert "missing" in capsys.readouterr().out.lower()


def test_latest_runs_reports_reruns_without_erasing_history(tmp_path, monkeypatch):
    path = tmp_path / "runs.jsonl"
    records = [
        {"case": "en-courier-paid-01", "line": "guardian", "run_id": "failed-first"},
        {"case": "en-courier-paid-01", "line": "guardian", "run_id": "retry"},
    ]
    path.write_text("\n".join(runner.json.dumps(r) for r in records))
    monkeypatch.setattr(runner, "RUNS", path)
    result = runner.latest_runs("guardian")["en-courier-paid-01"]
    assert result["run_id"] == "retry" and result["attempts"] == 2
    assert "failed-first" in path.read_text()


def test_guardian_case_selection_rejects_unknown_or_wrong_language(monkeypatch, capsys):
    monkeypatch.setattr(runner, "get_settings", lambda: SimpleNamespace(bolna_api_key="fake"))
    assert runner.check_guardian("en", ["hi-courier-paid-01"]) == 1
    assert "Invalid Guardian case selection" in capsys.readouterr().out
