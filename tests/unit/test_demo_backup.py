from scamkaki.domain.extraction import parse_guardian_report
from scripts.demo_backup import guardian_cases, tool_body


def test_courier_paid_bodies_parse_back_to_the_fixture_report():
    cases = guardian_cases()
    for case_id in ["en-courier-paid-01", "hi-courier-paid-01"]:
        case = cases[case_id]
        body = tool_body(case)
        report = parse_guardian_report(body)

        assert body["language"] == case["language"]
        assert report.agency == case["expect"]["agency"]
        assert report.demand == case["expect"]["demand"]
        assert report.channel == case["expect"]["channel"]
        assert report.tactics == frozenset(case["expect"]["tactics"])
        assert report.acted == case["expect"]["acted"]


def test_only_guardian_cases_are_offered():
    assert all(case["for"] == "guardian" for case in guardian_cases().values())
