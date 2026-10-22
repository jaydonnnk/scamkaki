"""Each Hindi agent must wire the same tools, enums and webhook as its English twin."""

import json

import pytest

from tests.conftest import ROOT

HI_AGENTS = sorted((ROOT / "agents").glob("*_hi.json"))


def wiring(path):
    config = json.loads(path.read_text())["agent_config"]
    tools = config["tasks"][0]["tools_config"]["api_tools"]
    params = {
        name: {key: value for key, value in spec.items() if key != "param"}
        for name, spec in tools["tools_params"].items()
    }
    schemas = {tool["name"]: tool["parameters"]["properties"] for tool in tools["tools"]}
    enums = {
        name: {field: spec.get("enum") for field, spec in props.items()}
        for name, props in schemas.items()
    }
    return config["webhook_url"], params, enums


def test_there_is_a_hindi_guardian():
    assert ROOT / "agents" / "guardian_hi.json" in HI_AGENTS


@pytest.mark.parametrize("hi_path", HI_AGENTS, ids=lambda p: p.name)
def test_hi_agents_match_english_twins(hi_path):
    english = hi_path.with_name(hi_path.name.removesuffix("_hi.json") + ".json")
    assert wiring(hi_path) == wiring(english)


@pytest.mark.parametrize("hi_path", HI_AGENTS, ids=lambda p: p.name)
def test_hi_agents_send_language_hi_to_tools(hi_path):
    tools = json.loads(hi_path.read_text())["agent_config"]["tasks"][0]["tools_config"]
    for spec in tools["api_tools"]["tools_params"].values():
        if spec["url"]:  # Our endpoints; Bolna's own transfer tool has no url.
            assert json.loads(spec["param"])["language"] == "hi"


@pytest.mark.parametrize("name", ["guardian", "guardian_hi"])
def test_guardian_transfers_to_family_number_from_settings(name):
    tools = json.loads((ROOT / "agents" / f"{name}.json").read_text())["agent_config"]
    api = tools["tasks"][0]["tools_config"]["api_tools"]
    transfer = [tool for tool in api["tools"] if tool["key"] == "transfer_call"]

    assert [tool["name"] for tool in transfer] == ["transfer_to_family"]
    param = json.loads(api["tools_params"]["transfer_to_family"]["param"])
    # The real number lives in settings only, never in the committed file.
    assert param["call_transfer_number"] == "${FAMILY_TRANSFER_NUMBER}"
