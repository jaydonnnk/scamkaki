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

Calls used: 2 of the 5 S3 allows; spend 11 cents.
