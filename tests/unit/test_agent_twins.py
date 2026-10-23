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


@pytest.mark.parametrize("name", ["bait.json", "bait_hi.json"])
def test_bait_extracts_every_field_and_valid_enums(name):
    from scamkaki.domain.extraction import TEXT_FIELDS
    from scamkaki.domain.types import AGENCIES, DEMANDS

    _, _, _, extractions = wiring(ROOT / "agents" / name)

    assert set(extractions) == {"agency", "demand", *TEXT_FIELDS}
    assert tuple(extractions["agency"]) == AGENCIES
    assert tuple(extractions["demand"]) == DEMANDS
