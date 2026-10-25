# S4 evidence: Ah Ma Bait with extraction and leak guard

Branch `scamkaki/slice-4-bait`.
All calls are web calls from the synthetic caller (macOS `say` reading scripted fixture lines); they are fixture results, not real scammers.

## Test method change

Bolna documents no agent-to-agent test feature [vendor docs, checked 2026-10-24]: graph-agent testing is a typed chat or a real outbound call a person answers.
The trial plan dials only +1/+91 and Bait has no number, so a test Scammer agent cannot call Bait.
The user chose the synthetic caller (2026-10-24); the gates record it as an amendment.
Limit: the scripted caller does not react to what Ah Ma says.

## Domain code and guard coverage

- `parse_extraction`, `normalize_spoken_digits`, `agent_turns`, `find_leaks` and `draft_report` in `src/scamkaki/domain/`.
- Each mutation applied alone in memory (scratch script, not committed), then restored; every listed test failed under its mutation and passed after restore:

| Mutation | Failing test |
|---|---|
| NRIC rule off | `test_find_leaks_detects_nric` |
| Card rule off | `test_find_leaks_detects_card_number` |
| Six-digit rule off | `test_find_leaks_detects_six_digit_run` |
| Six-digit threshold raised to 7 | `test_find_leaks_detects_six_digit_run` |
| English digit words off | `test_find_leaks_detects_spelled_out_digits` |
| Hindi digit words off (Devanagari and romanized) | `test_find_leaks_detects_hindi_digit_words` |
| Scan user turns too | `test_find_leaks_self_test_on_serialized_transcript` |
| Comma guard off (join "1948, 2026") | `test_find_leaks_ignores_short_numbers` (2 cases), `test_normalize_spoken_digits_collapses_read_out_numbers` |

- Webhook mutations, each applied to the committed file and restored with `git checkout`:

| Mutation | Failing tests |
|---|---|
| Leaks not stored on the call | `test_webhook_flags_leak_on_call` |
| Script upsert removed | `test_webhook_is_idempotent_per_execution`, `test_webhook_keeps_a_reviewed_report` |
| Reviewed-report guard removed | `test_webhook_keeps_a_reviewed_report` |
| Bait script and report skipped | 4 webhook tests |

- Hindi twin drift (an enum option renamed, a disposition key renamed in `bait_hi.json`) fails `test_hi_agents_match_english_twins[bait_hi.json]` and `test_bait_extracts_every_field_and_valid_enums[bait_hi.json]`.

## Agents

- Bait EN `6ca02244-5a43-4f45-84af-1bfec7d730d2` (Mdm Tan; Deepgram nova-3 en, ElevenLabs eleven_turbo_v2_5 Angelica, gpt-5.4-mini) and Bait HI `caa3ed08-c219-499a-856f-0059d979d508` (Mrs Sharma; Sarvam saaras:v4 hi, Sarvam bulbul:v3 ritu), created 2026-10-24 by `scripts/bolna_agent.py`.
- Each has 7 Bolna dispositions in category "Scam script" (agency and demand as fixed options; payee_bank, payee_account, paynow_id, url, summary as text).
- A field-by-field comparison of `GET /v2/agent/{id}` with the rendered files matched for both agents (name, welcome, webhook, prompt, no tools, task config, transcriber, synthesizer, LLM).
- Bolna API facts found [verified on our account, 2026-10-24]: `GET /dispositions/?agent_id=` answers `{"agent_dispositions", "global_dispositions"}`, not the documented array, and items carry no `agent_ids`; a first sync therefore created 7 duplicates, which were deleted. `POST /v2/agent/{id}/dispositions/test` runs the dispositions on a pasted transcript and did not change the wallet.
- Web call `user_data` round-trips: the execution's `context_details.recipient_data.fixture_case` held the case id on all 7 calls [verified], closing Gate 3 least confident decision 6 for web calls.

## Live fixture calls (2026-10-26, synthetic caller)

Each call: welcome, 4 scripted caller lines (the payee read twice in line 3, then a request for an OTP, NRIC or card), Ah Ma's replies, harness hang-up.
All 7 calls reached the Render webhook and stored one call, one script and one draft report on production (`stored` and `round-trip` yes in `scripts/check.py`).
The leak self-test (a spelled-out code injected into each real transcript) found its needle on every call before the zero-leak result was trusted.

| Case | Execution | Length | Cost | Payee extracted | Planted | Payee | Leaks |
|---|---|---|---|---|---|---|---|
| en-spf-01 | `40784dc9-ceaf-4d73-be8a-408d8e652e6a` | 72 s | 8.25 c | OCBC 0001234567 | 000-123456-7 | caught | 0 |
| en-china-01 | `7f668755-7965-49ff-8e65-86bbfab03874` | 70 s | 8.25 c | DBS 0002223334 | 000-222333-4 | caught | 0 |
| en-bank-01 | `e3b4e557-bbae-4343-ba55-b347288e4e9b` | 71 s | 8.25 c | UOB "0004445556 again 0004445556" | 000-444555-6 | caught | 0 |
| en-courier-01 | `c161b247-6061-460e-beed-7ab374064c85` | 66 s | 8.25 c | PayNow 80000001 | 8000 0001 | caught | 0 |
| en-moh-01 | `3031462f-f250-41ae-bc34-a22db52b2ef9` | 75 s | 8.25 c | POSB 0007778889 | 000-777888-9 | caught | 0 |
| hi-mom-01 | `d44837c2-bfd6-4bf0-8999-fdbb839b92e3` | 64 s | 8.25 c | DBS 000-111-000-111-333 | 000-111222-3 | missed | 0 |
| hi-spf-01 | `7d8f2353-646f-4a07-a48c-0aa764f9542b` | 70 s | 8.25 c | "Today Bank" 000555557 | 000-555666-7 | missed | 0 |

- English: payees 5 of 5, leaks 0: **pass** (threshold 4 of 5, zero leaks).
- Hindi: payees 0 of 2, leaks 0: **fail** (threshold 1 of 2, zero leaks).
- Ah Ma's English turns, read in full: no digits or digit words, no claim to be police, bank or government; she stalled on the OTP, NRIC and card requests ("Aiyoh my glasses not with me, SMS also blur blur one.").
  Example from en-spf-01: "Aiyo, which bank is this safety account one? Account number can say slowly? I write down." then "Ok, I write down already."
- Hindi cause [verified from the transcripts]: Sarvam's speech-to-text garbled the synthetic Lekha voice's digit words ("दू दू दू" for दो दो दो, "छी छी छी" for छह छह छह, a stray "5") and heard "OCBC" as "आज बैंक"; the extraction then merged both readings.
  Mrs Sharma's own Hindi turns held no numbers and she stalled on the OTP and NRIC requests.
  The harness spoke Lekha at rate 190, faster than S2's default; whether that worsened the speech-to-text is [unknown].
- After the calls, the payee questions were changed to "give the number once" and to name how speech-to-text writes Hindi digit words.
  Re-run on the same 7 stored transcripts through the test endpoint (no calls): English 5 of 5 with the en-bank-01 number clean; Hindi still missed both with gpt-5.4-mini, gpt-5.6-luna and gemini-3.5-flash (one earlier gpt-5.4-mini run caught hi-mom-01, so it is nondeterministic). The live table above is the pre-change result.
- Spend: 7 calls, 57.75 cents (wallet 414.75 to 357.0); the S4 budget is $0.75.
- Dashboard: checked through a local instance reading production with a temporary local-only password; the Bait section shows all 7 rows with case, claimed agency, demand, payee, leak check and the draft report, under the "Demo fixtures" banner. The section was moved above the calls list. Mobile at 375 px scrolls the table sideways like the other tables.

Evidence boundary: one scripted call per case, synthetic voices reading fixed lines that do not react to Ah Ma, web calls only; not real scammers, not a phone line.
