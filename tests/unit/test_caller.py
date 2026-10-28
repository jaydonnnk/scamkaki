import json
import threading
from copy import deepcopy
from http.server import ThreadingHTTPServer
from types import SimpleNamespace

import httpx
import pytest

from scripts.caller import serve


@pytest.fixture
def caller(monkeypatch, tmp_path):
    requests = []

    class FakeBolna:
        def __init__(self, key):
            assert key == "offline-key"

        def mint_web_call_session(self, agent_id, user_data):
            requests.append((agent_id, user_data))
            return {"offline": True}

    monkeypatch.setattr(serve, "BolnaClient", FakeBolna)
    monkeypatch.setattr(
        serve,
        "get_settings",
        lambda: SimpleNamespace(
            bolna_api_key="offline-key", agent_id=lambda line, language: f"{line}-{language}"
        ),
    )
    monkeypatch.setattr(serve.Handler, "cases", serve.load_cases())
    monkeypatch.setattr(serve.Handler, "log_message", lambda *args: None)
    runs = tmp_path / "runs.jsonl"
    monkeypatch.setattr(serve, "RUNS", runs)
    server = ThreadingHTTPServer(("127.0.0.1", 0), serve.Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    with httpx.Client(base_url=f"http://127.0.0.1:{server.server_port}") as client:
        yield client, requests, runs
    server.shutdown()
    thread.join()
    server.server_close()


def test_caller_exposes_fixture_facts_for_roleplay(caller):
    client, _, _ = caller
    cases = client.get("/cases").json()
    case = next(c for c in cases if c["id"] == "en-ica-video-01")
    assert case["label"].startswith("Demo fixture")
    assert case["senior_lines"][0].startswith("Someone from ICA called.")


def test_live_session_keeps_fixture_id(caller):
    client, requests, _ = caller
    response = client.post("/session?line=guardian&case=en-ica-video-01&mode=live")
    assert response.status_code == 200
    assert requests == [("guardian-en", {"fixture_case": "en-ica-video-01"})]


@pytest.mark.parametrize(
    "query",
    [
        "line=bait&case=en-spf-01&mode=live",
        "line=guardian&case=en-ica-video-01&mode=invalid",
    ],
)
def test_invalid_caller_mode_never_mints_a_session(caller, query):
    client, requests, _ = caller
    assert client.post("/session?" + query).status_code == 400
    assert requests == []


def test_bait_clip_session_is_unchanged(caller):
    client, requests, _ = caller
    assert client.post("/session?line=bait&case=en-spf-01").status_code == 200
    assert requests == [("bait-en", {"fixture_case": "en-spf-01"})]


def test_roleplay_log_records_mode_without_claiming_a_real_senior(caller):
    client, _, runs = caller
    record = {
        "case": "en-ica-video-01",
        "line": "guardian",
        "caller_mode": "live",
        "caller_kind": "human_roleplay",
        "run_id": "offline-test",
        "clips_played": 0,
    }
    assert client.post("/log", json=record).status_code == 200
    assert json.loads(runs.read_text())["caller_kind"] == "human_roleplay"


def test_changed_guardian_story_does_not_reuse_the_old_audio_file():
    case = deepcopy(serve.load_cases()["en-ica-video-01"])
    before = serve.clip_names(case, "guardian")
    case["senior_lines"][-2] += " They did not threaten arrest."
    after = serve.clip_names(case, "guardian")
    assert after[-2] != before[-2]
    assert after[:-2] == before[:-2] and after[-1] == before[-1]


def test_bait_audio_names_stay_at_the_s4_paths():
    case = serve.load_cases()["en-spf-01"]
    assert serve.clip_names(case, "bait") == [f"en-spf-01-{i}.wav" for i in range(4)]
