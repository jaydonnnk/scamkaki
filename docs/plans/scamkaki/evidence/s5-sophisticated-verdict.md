# S5 evidence: sophisticated verdict behind the tool, no calls

Branch `scamkaki/slice-5-guardian-loop`, merged with `main` at `9be72d1` on 2026-10-28.
Demo fixtures only: scripted senior stories paraphrasing public SPF advisories, never real seniors or real scam calls.
No Bolna call was placed and no Bolna agent was changed in this slice.

## What was built

- `GuardianReport` (agency, demand, channel, warning signs, acted) and `parse_guardian_report`; unknown warning signs are dropped and a missing `acted` is `none`.
- New agency values (`mas`, `minlaw`, `telco`, `investment`, `employer`, `friend_family`) and demands (`cash_handover`, `card_details`).
- `decide` branches, in order: harmful act, any red warning sign, friend or family money with no red sign (`unclear`), hard demand, government plus personal info, weak sign or `acted` unsure or a repeat script (`unclear`).
- Sentences in English and Hindi: the bank and 1799 instruction first when the senior already acted; the call-back sentence for a friend's money request; `MatchResult.urgent`.
- Telegram text and family page: urgent line, contact channel and warning signs in a fixed order.
- Migration `0005_guardian_signs.sql`: `guardian_checks.channel`, `tactics`, `acted` with defaults.
- `/tools/match-script` takes `channel`, `tactics` (comma-separated) and `acted`; an agent still sending only agency and demand gets the defaults.
- `seed/scripts.json`: 7 Bait cases unchanged except `for: bait` and their `senior_lines` removed; the 4 old easy Guardian cases removed; 15 new Guardian cases (12 English, 3 Hindi).
- `scripts/check.py`: filters by `for`; English Guardian threshold 7 of 8 scams, at most 1 of 4 legit.
- Bait's agent options are pinned to their S4 values in `test_agent_twins.py`, because Bait is unchanged by approval.

## Checks (2026-10-28)

| Check | Result |
|---|---|
| `uv run ruff check .` and `ruff format --check .` | pass |
| `uv run pytest tests/unit -q` | 138 passed |
| `uv run pytest tests/integration -q` (Neon test branch, migration 0005 applied by the suite's migrate step) | 60 passed |
| `test_decide_matches_every_guardian_fixture` (rule only, offline) | 15 of 15 |
| `test_match_script_answers_every_guardian_fixture` (each fixture's expected report through the real route, Neon test branch, fake Telegram) | 15 of 15; urgent exactly on the 2 already-acted cases; one alert per `likely_scam`, none otherwise |
| `test_guardian_fixtures_avoid_giveaway_words` | no senior line says "scam", "safety account", "safe account" or "money laundering" |

These prove the rule and the route on the expected reports.
They do not prove that Bolna's LLM fills those five values from a real conversation; that is S6's probe.

## Guard coverage: one mutation per new branch

Each mutation was applied alone, the named tests run, and the file restored.

| Mutation | Caught by |
|---|---|
| Harmful act no longer gives likely scam | `test_decide_harmful_act_is_likely_scam[paid]` |
| Red warning sign no longer gives likely scam | `test_decide_red_tactic_alone_is_likely_scam[channel_move]` |
| Friend money rule removed | `test_decide_friend_money_without_red_tactic_is_unclear` |
| Weak sign dropped from the unclear rule | `test_decide_weak_tactic_or_unsure_act_is_unclear[senior0]` |
| `acted` unsure dropped from the unclear rule | `test_decide_weak_tactic_or_unsure_act_is_unclear[senior2]` |
| Bank and 1799 sentence removed | `test_sentence_for_harmful_act_says_bank_and_1799_first[en-...]` |
| Call-back sentence removed | `test_sentence_for_friend_money_says_call_back_on_known_number[en-...]` |
| `urgent` always false | `test_sentence_for_harmful_act_says_bank_and_1799_first[en-...]` |
| Urgent line removed from the Telegram text | `test_alert_text_marks_urgent_when_acted` |
| Unknown warning signs kept | `test_parse_guardian_report_drops_unknown_tactics_and_defaults_acted` |
| Unknown `acted` becomes `unsure` | `test_parse_guardian_report_drops_unknown_tactics_and_defaults_acted` |
| Family alerts not urgent first | `test_family_alerts_list_urgent_first` |
| Warning signs stored in another order | `test_family_alerts_list_urgent_first` |
| `acted` not stored | `test_match_script_stores_channel_tactics_and_acted` |

14 of 14 caught.

## Family page

The real `family.html` template, rendered with two sample alerts (one urgent courier case, one MinLaw handoff) and a stubbed fetch, checked at 375 px: the urgent alert is on top with the "Urgent: Ah Ma already acted" tag, card details and code, SMS, warning sign and the bank instruction; no horizontal scroll.
This was a local render, not the deployed page.

## Not done yet (needs separate authorization)

- Push the branch and fast-forward `main` so Render deploys, and migration 0005 on production.
- `curl` of the 15 reports against Render, the deployed family page at phone width and one Telegram message, as the S5 contract asks.
- A local server against the test database was tried for the `curl` run; reading the test database URL from `.env.local` was blocked by permissions, so the same reports were sent through the real route in-process instead.

## Open points

- The family page lists urgent alerts first, as Gate 3 says. An old urgent alert stays on top and keeps flashing when a newer, non-urgent alert arrives. [hypothesis: worth limiting "urgent first" to recent alerts; needs a Gate 3 wording decision]
- The Hindi act-now and call-back sentences need the Hindi listener check planned for S6.
