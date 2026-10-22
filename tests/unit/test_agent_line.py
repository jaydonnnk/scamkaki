from tests.conftest import BAIT_AGENT, BAIT_HI_AGENT, GUARDIAN_AGENT, GUARDIAN_HI_AGENT


def test_agent_line_maps_all_four_agents(test_settings):
    assert test_settings.agent_line(GUARDIAN_AGENT) == ("guardian", "en")
    assert test_settings.agent_line(GUARDIAN_HI_AGENT) == ("guardian", "hi")
    assert test_settings.agent_line(BAIT_AGENT) == ("bait", "en")
    assert test_settings.agent_line(BAIT_HI_AGENT) == ("bait", "hi")


def test_agent_line_ignores_unknown_and_missing_ids(test_settings):
    assert test_settings.agent_line("someone-else") is None
    assert test_settings.agent_line(None) is None
    # An unset agent id is "" in settings; an empty id must not match it.
    assert test_settings.model_copy(update={"bolna_bait_hi_agent_id": ""}).agent_line("") is None
