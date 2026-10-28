"""Each Hindi agent must wire the same tools, enums, extractions and webhook as its English twin."""

import json

import pytest

from tests.conftest import ROOT

HI_AGENTS = sorted((ROOT / "agents").glob("*_hi.json"))


def wiring(path):
    agent = json.loads(path.read_text())
    config = agent["agent_config"]
    tools = config["tasks"][0]["tools_config"].get("api_tools") or {"tools": [], "tools_params": {}}
    params = {
        name: {key: value for key, value in spec.items() if key != "param"}
        for name, spec in tools["tools_params"].items()
    }
    schemas = {tool["name"]: tool["parameters"]["properties"] for tool in tools["tools"]}
    enums = {
        name: {field: spec.get("enum") for field, spec in props.items()}
        for name, props in schemas.items()
    }
    # Extraction keys and the options each objective one may return.
    extractions = {
        spec["name"]: [option["value"] for option in spec.get("objective_options", [])]
        for spec in agent.get("dispositions", [])
    }
    return config["webhook_url"], params, enums, extractions


@pytest.mark.parametrize("name", ["guardian_hi.json", "bait_hi.json"])
def test_there_is_a_hindi_twin(name):
    assert ROOT / "agents" / name in HI_AGENTS


@pytest.mark.parametrize("hi_path", HI_AGENTS, ids=lambda p: p.name)
def test_hi_agents_match_english_twins(hi_path):
    english = hi_path.with_name(hi_path.name.removesuffix("_hi.json") + ".json")
    assert wiring(hi_path) == wiring(english)


@pytest.mark.parametrize("hi_path", HI_AGENTS, ids=lambda p: p.name)
def test_hi_agents_send_language_hi_to_tools(hi_path):
    tools = json.loads(hi_path.read_text())["agent_config"]["tasks"][0]["tools_config"]
    for spec in (tools.get("api_tools") or {"tools_params": {}})["tools_params"].values():
        if spec["url"]:  # Our endpoints; Bolna's own transfer tool has no url.
            assert json.loads(spec["param"])["language"] == "hi"


BAIT_AGENCIES = (
    "spf", "ica", "china_official", "moh", "cpf", "mom", "iras", "bank", "courier", "other"
)  # fmt: skip
BAIT_DEMANDS = ("transfer", "otp", "app_install", "personal_info", "gift_card", "none", "other")


@pytest.mark.parametrize("name", ["bait.json", "bait_hi.json"])
def test_bait_extracts_every_field_and_valid_enums(name):
    from scamkaki.domain.extraction import TEXT_FIELDS
    from scamkaki.domain.types import AGENCIES, DEMANDS

    _, _, _, extractions = wiring(ROOT / "agents" / name)

    assert set(extractions) == {"agency", "demand", *TEXT_FIELDS}
    # Bait keeps its S4 options (Gate 3, 2026-10-27: Bait unchanged); each must still be a value
    # the app knows, so Bait scripts keep matching Guardian checks on agency and demand.
    assert tuple(extractions["agency"]) == BAIT_AGENCIES
    assert tuple(extractions["demand"]) == BAIT_DEMANDS
    assert set(BAIT_AGENCIES) <= set(AGENCIES) and set(BAIT_DEMANDS) <= set(DEMANDS)


@pytest.mark.parametrize("name", ["guardian.json", "guardian_hi.json"])
def test_guardian_sends_all_five_values_with_domain_enums(name):
    from scamkaki.domain.types import ACTED, AGENCIES, CHANNELS, DEMANDS, TACTICS

    agent = json.loads((ROOT / "agents" / name).read_text())
    tools = agent["agent_config"]["tasks"][0]["tools_config"]["api_tools"]
    schema = tools["tools"][0]["parameters"]
    assert set(schema["required"]) == {"agency", "demand", "channel", "tactics", "acted"}
    for field, values in {
        "agency": AGENCIES,
        "demand": DEMANDS,
        "channel": CHANNELS,
        "acted": ACTED,
    }.items():
        assert schema["properties"][field]["enum"] == list(values)
    assert schema["properties"]["tactics"]["type"] == "string"
    for tactic in TACTICS:
        assert tactic in schema["properties"]["tactics"]["description"]
    payload = json.loads(tools["tools_params"]["match_script"]["param"])
    for field in ("agency", "demand", "channel", "tactics", "acted"):
        assert payload[field] == f"%({field})s"


@pytest.mark.parametrize("name", ["guardian.json", "guardian_hi.json"])
def test_guardian_prompt_covers_new_questions_and_confirmation(name):
    agent = json.loads((ROOT / "agents" / name).read_text())
    prompt = agent["agent_prompts"]["task_1"]["system_prompt"]
    for instruction in ("channel", "warning-sign", "already", "repeat", "confirm", "once"):
        assert instruction in prompt.lower()


@pytest.mark.parametrize("name", ["guardian.json", "guardian_hi.json"])
def test_guardian_interview_settings_and_confirmation_rule(name):
    agent = json.loads((ROOT / "agents" / name).read_text())
    config = agent["agent_config"]["tasks"][0]["tools_config"]["llm_agent"]["llm_config"]
    assert config["max_tokens"] == 300
    assert config["temperature"] == 1
    prompt = agent["agent_prompts"]["task_1"]["system_prompt"]
    assert "NO TOOL CALL BEFORE AN EXPLICIT YES" in prompt
    assert "Never refuse to help" in prompt
