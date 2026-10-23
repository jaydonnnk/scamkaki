# S3 evidence: Guardian verdict and family alert

Branch `scamkaki/slice-3-guardian-verdict`.
All calls are web calls by the user role-playing a senior; they are fixture results, not real scam calls.

## Verdict code

- `decide` and `sentence_for(verdict, similar_count, language)` built in `src/scamkaki/domain/verdict.py`; `match_script` uses them with `similar_count` 0 until S5 and answers `unclear` on any internal error.
- Suite at `f861d88`: 53 passed; ruff check and format clean.
- Guard coverage, each mutation applied alone in memory and restored (suite back to 51, then 53, after each):

| Mutation | Failing tests |
|---|---|
| Drop the hard-demand rule | `test_decide_hard_demand_is_likely_scam` (and two integration tests) |
| Drop the government plus personal-info rule | `test_decide_gov_personal_info_is_likely_scam` |
| Drop the repeat-script rule | `test_decide_repeat_script_is_unclear` |
| Default verdict `unclear` | `test_decide_no_signals_is_no_scam_signs` (and others) |
| English sentence says "safe" | `test_sentence_never_says_safe` |
| Hindi likely-scam warnings dropped | `test_sentence_never_says_safe`, `test_match_script_answers_in_hindi_for_hindi_line` |
| Error fallback removed | `test_match_script_error_returns_unclear` |
| Literal number in `guardian_hi.json` | `test_guardian_transfers_to_family_number_from_settings[guardian_hi]` |
| English transfer tool renamed | `test_guardian_transfers_to_family_number_from_settings[guardian]`, `test_hi_agents_match_english_twins` |
| Hindi `match_script` language `en` | `test_hi_agents_send_language_hi_to_tools` |
| Hindi transfer message differs from the approved sentence | `test_transfer_speaks_the_approved_likely_scam_sentence[guardian_hi-hi]` |

- Sentence review: the user accepted the English sentences; Hindi listener Pravesh accepted the Hindi sentences (reported by the user, 2026-10-24).
- Live check after the Render deploy of `c79a427`: `match_script` with `courier` and `none` answered `no_scam_signs`, which the stub could not; the probe `guardian_checks` row was deleted.

## Transfer probes (Guardian EN, transfer target a +65 number)

| Call | Execution | Cost | Result |
|---|---|---|---|
| Probe 1 | `15d788a1-4098-431d-9761-39d2ad179141` | 5.5 cents, 52 s | Repeat-back and confirmation worked; `match_script` got `spf` and `transfer` and answered `likely_scam`; Ah Ma spoke the sentence, then the LLM ended its turn and never called `transfer_to_family`. The repeat-back was spoken twice. |
| Probe 2 | `213b79c1-759a-4e9a-9ad7-ae42199e0b92` | 5.5 cents | After the fix (transfer at once, the tool's pre-call message speaks the sentence), `transfer_to_family` fired and Bolna returned `ERROR CALLING API: request blocked by outbound URL policy`. The phone did not ring. |

Conclusion [verified for this account and web calls, 2026-10-24]: Bolna call transfer does not reach a phone from our web calls; whether a paid plan or real phone calls would allow it is [unknown].
Gate 3's least confident decision 4 (transfer relies on the LLM) also showed in probe 1.
The user chose a family alert page plus Telegram instead (2026-10-24), which reopened Gates 1-4.

Probe spend: 11 cents.

## Family alert build (after the 2026-10-24 gate re-approval)

- Built at `570c15d`, deployed at `8f81828`: migration `0003_family_alerts.sql` (applied to production 2026-10-24), `telegram.send_message`, `alert_text`, the family page `/family/{link_token}` and its alert list, and no transfer tool on either Guardian agent.
- Suite: 62 passed; ruff check and format clean.
- Local preview on the Neon test branch, phone and desktop widths, light and dark: a new alert appeared within one 5-second check, flashed and changed the tab title.
- Guard coverage, each mutation applied alone and restored (suite back to 62 after each):

| Mutation | Failing tests |
|---|---|
| Alert on every verdict | `test_match_script_other_verdicts_send_no_alert`, `test_match_script_error_sends_no_alert` |
| Never alert | `test_match_script_likely_scam_alerts_family` and three more |
| Family link not checked | `test_family_page_rejects_wrong_link`, `test_family_page_is_closed_without_a_link_token` |
| Empty link token opens the page | `test_family_page_is_closed_without_a_link_token` |
| Telegram failure recorded as sent | `test_match_script_telegram_failure_still_answers` |
| Missing Telegram recorded as sent | `test_match_script_without_telegram_records_alert_off` |
| Telegram logs the exception text (can carry the token) | `test_send_message_never_raises_or_logs_the_token` |
| Telegram ignores the `ok` flag | `test_send_message_is_true_only_when_telegram_says_ok` |
| Alert text loses the fixture label | `test_alert_text_is_labeled_fixture_and_names_claim` |
| Family list includes every verdict | `test_family_alerts_lists_likely_scam_only` |
| Alert text drops the repeat count | `test_alert_text_mentions_repeat_script_when_seen` |

## Live calls (web calls, user role-playing a senior; fixture results)

| Call | Execution | Cost | Agency, demand | Verdict | Alert |
|---|---|---|---|---|---|
| English scam | `d080aaff-a80c-4845-81b1-d4b1c1ff25e5`, 58 s | 5.5 cents | ica, otp | `likely_scam` | `sent` |
| English legit, first try | `b99a2158-efab-4a1e-a2c9-10b7ec32cca3`, 8.6 s | 2.75 cents | none (ended after "my bank") | none | none |
| English legit | `f0d0cd91-620b-40a9-8d54-f030acafdd86`, 48 s | 5.5 cents | bank, none | `no_scam_signs` | none |
| Hindi scam | `a3e2f201-ae0c-40cb-aaec-afb9cad85191`, 60 s | 8.25 cents | spf, transfer | `likely_scam` | `sent` |

- English scam excerpt: "So they said they are from ICA and asked for your OTP code. Is that right?" then "This is likely a scam. Do not transfer money or share any code. I have alerted your family. Please wait for their call."
  The LLM then added "Don't answer or call back the caller. Then wait for your family's call.", which repeats the sentence; a prompt polish for S6.
- English legit excerpt: "No scam signs found in what you told me. Still, never move money or share a code because a caller asked. If anything feels wrong, call your family."
- Hindi excerpt: Sarvam split the caller's speech into fragments and misheard one word ("मुनि"), but Guardian HI repeated back "पुलिस" and "पैसे ट्रांसफर", waited for "हाँ", and said the full Hindi likely-scam sentence with both warnings.
- The user reported that the Telegram message arrived and the family page flashed for both scam calls, and nothing arrived for the legit call.
  Seconds from verdict to alert were not measured.
- Pravesh accepted the earlier Hindi sentences; the changed likely-scam ending ("मैंने आपके परिवार को खबर कर दी है") was sent to him for a re-check, with no reply recorded here.

## Totals and limits

- S3 calls: 6 (2 transfer probes, 4 alert calls including one cut-off attempt), against the plan's 5; the extra was the 8.6 s cut-off call.
- S3 spend: 33 cents; Bolna wallet 447.75 before S3 and 414.75 after, matching.
- One English scam, one English legit and one Hindi scam call: a smoke test, not a pass rate. Fixture pass rates come in S5.
- `similar_count` is always 0 until S5.
- The family is reached only through Telegram or an open family page; nobody is phoned.
- Post-slice cleanup: no stale or redundant files; the dashboard does not yet show the alert status (S6).
