# Slice plan: Scamkaki

Compact gate draft, 2026-10-22.
Revised 2026-10-22: S2 is the Hindi voice slice; Hokkien is dropped; Mandarin is a stretch after S7 (was S6 before the 2026-10-28 split).
Revised 2026-10-24: S3 alerts the family by Telegram and a family alert page instead of transferring the call.
Revised 2026-10-27 (reopened): S5 grows to cover sophisticated scams: warning signs, already-acted handling and the rewritten Guardian fixtures, on top of the 7-day loop already built on its branch.
Revised 2026-10-28 (reopened): that S5 is split. S5 builds the sophisticated verdict behind the tool with no calls; S6 updates the Guardian agents and runs the live fixture calls; the dashboard and demo slice becomes S7.
Riskiest first.
Each slice ends with a visible, working result and evidence in `evidence/`.
Branch per slice: `scamkaki/slice-<N>-<slug>`.

## Build order

| ID | Slice | Visible result | Tests and evidence | Authorizations to request |
|---|---|---|---|---|
| S1 | Tracer: Guardian stub end to end | A phone call to Guardian hears the stub "Not sure, please call your family"; the call appears on the dashboard | Unit: env example test. Integration: webhook token, webhook stores call, match-script token. Evidence: call id, dashboard screenshot, execution JSON shape, whether call variables round-trip | `uv` install of pinned deps; Neon project + test branch; Render deploy; Bolna agent create; up to 3 test calls |
| S2 | Hindi voice | A Hindi web call to Guardian HI hears a Hindi auntie voice, Guardian HI extracts agency and demand and calls `match_script`; the call shows on the dashboard as `hi`. Builds `agents/guardian_hi.json`, `calls.language`, `agent_line`, a Talk to Guardian button per language, and removes the Hokkien TTS leftovers (`tts_modal/`, `TTS_*` settings) | Unit: `test_agent_line_maps_all_four_agents`, `test_hi_agents_match_english_twins`, env example test. Integration: webhook stores `language`. Live: 3 Hindi web calls under 1 minute each, STT provider and voice recorded; go/no-go: agency and demand extracted correctly in at least 2 of 3, reply latency recorded, and a Hindi speaker the user names says the voice is understandable, else English only | Bolna Guardian HI agent create; up to 3 web calls; Hindi listener |
| S3 | Guardian verdict and family alert | A scam description gets "likely scam" and, within a minute, a Telegram message on the family member's phone and a flashing alert on the family page; a legit description sends no alert; Guardian HI says the same verdicts in Hindi. Builds `decide`, `sentence_for`, `alert_text`, migration 0003, the Telegram sender and the family page; removes the transfer tool from both Guardian agents | Unit: all `decide`, `sentence_for`, `alert_text` tests with branch mutations. Integration: alert on likely scam only, Telegram failure still answers, family link check. Live: 2 English role-play calls (1 scam, 1 legit) and 1 Hindi scam call, with alert timing recorded | Up to 5 test calls (2 transfer probes used); the user creates the Telegram bot; `FAMILY_LINK_TOKEN`, `TELEGRAM_*` set on Render; listener check of the changed likely-scam sentences |
| S4 | Ah Ma Bait with extraction and leak guard | A teammate scammer call, in English or Hindi, produces a script row and a draft report on the dashboard | Unit: extraction and all leak tests, including Hindi digit words, with self-test and mutations. Integration: stores script and draft, idempotent, flags leak. Live: `scripts/check.py bait` over 5 English scam fixtures, at least 4 payees and zero leaks; `scripts/check.py bait --language hi` over 2 Hindi fixtures, at least 1 payee and zero leaks | Bait EN and Bait HI agent create; 7 synthetic-caller web calls (5 English, 2 Hindi) within a $0.75 budget |
| S5 | Sophisticated verdict behind the tool, no calls | `curl` to the deployed `/tools/match-script` with each Guardian fixture's expected report returns its expected verdict; the paid courier report returns `urgent` with the bank and 1799 sentence, the family page shows the urgent alert and a Telegram message arrives; a friend-money report returns the call-back sentence. Builds `GuardianReport`, `parse_guardian_report`, the new `decide` branches, sentences in English and Hindi, `alert_text`, migration 0005, the new `match-script` fields with defaults, the family page's urgent state and warning signs, and the 15 Guardian fixtures in `seed/scripts.json`; keeps the 7-day count already built. Continues on `scamkaki/slice-5-guardian-loop`, brought up to date by merging `main` | Unit: every new `decide` branch with a mutation per branch, `test_decide_matches_every_guardian_fixture`, `test_guardian_fixtures_avoid_giveaway_words`, `test_parse_guardian_report_drops_unknown_tactics_and_defaults_acted`, act-now and call-back sentences in both languages, urgent alert text. Integration: new fields stored, missing fields default, urgent alerts first, 7-day count across languages, error returns unclear. Evidence: `curl` outputs for all 15 reports against Render, family page screenshot at phone width, Telegram screenshot | Re-authorization of S5 under this contract; migration 0005 on the Neon test branch, then production; push and fast-forward `main` so Render deploys. No Bolna calls and no agent updates |
| S6 | Guardian asks the new questions, live | A synthetic senior who trusts a telco caller that handed her to a MinLaw officer hears "likely scam" on a Guardian web call; the senior who already paid the courier fee hears the bank and 1799 instruction first and the family gets an urgent alert; the grandson case hears "call him back on the number you already have"; a fixture whose agency and demand Bait collected hears "same script heard N times this week". Builds both Guardian agent prompts (channel, three warning-sign questions, already-acted question, repeat-back) and tool params (`channel`, `tactics`, `acted`), synthetic-caller `senior_lines` clips for the 15 fixtures, and `check.py guardian` reading the new fields | Unit: `test_hi_agents_match_english_twins` with the new params. Probe first: 1 English call to show all five values reach the app; falsifier: values missing or garbled in the stored check, then stop and re-plan before the full run. Live: `scripts/check.py guardian` over 12 English fixtures, at least 7 of 8 scams and at most 1 of 4 legit flagged, the paid courier case urgent; `--language hi` over 3 Hindi fixtures, 2 of 2 scams, 0 of 1 legit, the paid case urgent; call length per case recorded against the 3-minute target; reruns reported as reruns | Guardian EN and HI agent updates on Bolna; 1 probe plus up to 15 calls and a budget, asked when S5 is done; Hindi listener check of the new sentences |
| S7 | Dashboard, report review and demo | Dashboard matches the Gate 1 mockups at phone and desktop widths, including the warning-signs column and the urgent result; "Mark reviewed" works on a report page; demo rehearsed 3 times; backup video recorded | Integration: review marks reviewed and sends nothing; dashboard lists warning signs. Evidence: screenshots, demo run log | Render warm-up or paid instance if cold starts break calls |

S2 needs S1; S3 needs S1; S4 needs S1, and its Hindi half needs S2's provider choice; S5 needs S3 and S4; S6 needs S5; S7 needs S6.
If S2 is no-go, the Hindi parts of S3, S4, S5 and S6 drop and those slices run English only.

## Never cut

S1, S3, S4's leak guard, S5's already-acted path and offline fixture check, and the fixture labels on every screen.

## Cut order (first cut first)

1. S7 polish beyond the mockups (keep "Mark reviewed" and fixture labels).
2. S6 Hindi live run: run English only and report Hindi as offline-checked only.
3. S6 English live run: reduce to 4 cases (2 scam including the paid courier case, 2 legit), reported as such.

## Stretch, not planned

Bait extracts warning signs so the 7-day count can match on tactics; Mandarin Guardian and Bait agents, only after S7 is done and once Bolna accepts `zh` speech-to-text; BothBosu offline check of `decide`; SIP trunk `Diversion` detection.

## Plan-wide rules

- No slice starts without your authorization by ID.
- Every pass rate is reported with its sample size, as fixture results.
- A failed live run keeps its evidence; reruns are reported as reruns.
