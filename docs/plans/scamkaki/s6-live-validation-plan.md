# S6 live-validation plan

Historical validation plan and cost estimates. The 2026-10-30 continuation request grants a
fresh total ceiling of 100 US cents and names the user as English role-play operator, as
recorded in 00-status.md. Old wallet readings, remaining allowances and option reserves below
are historical evidence, not current account state or an additional budget. The next S6
handoff follows S12 publication. No live action is performed while preparing it.

User answers, 2026-10-28: Option A first, then B; total cap 150 cents; operators to be found by the user (Hindi not needed unless D is chosen later); a passing probe counts as `en-ica-video-01` if it passes `check.py`; `call_terminate` unanswered, so not set. Within 150 cents: A (25) plus B's four calls (100) is 125, leaving 25 for one rerun. Calls remain unauthorized until the user says so by name.

Prepared 2026-10-28 after S7's local build. **This is a plan, not authority.** It authorizes no session mint, call, agent update, top-up, deployment or other charge. S6 stays open until its evidence contract is met or the user changes it.
Fixture targets only: never performance against real scammers, and synthetic speech is never a human result.

## 1. What is known and unknown today

| Item | State |
|---|---|
| Render service answers | [verified 2026-10-28, this session] `GET https://scamkaki.onrender.com/healthz` returned HTTP 200. It returns only `{"ok": true}`, so it shows nothing about the deployed revision |
| Deployed revision | [unknown] `main` was published at `d74f56a`; whether Render has deployed it is not checked. S6 does not need S7 deployed, only the S5 verdict code, which the deployed S5 run already exercised (15 of 15, 2026-10-28) |
| Guardian agents on Bolna | [verified 2026-10-28, earlier] both updated and read back: gpt-5.4-mini, temperature 1, max_tokens 300, explicit yes before the tool call. Not re-read in this session |
| Wallet | [unknown now]. Last reading 277.25 US cents after the failed probe; no call since. Read the wallet again before any call |
| Account access, plan, limits | [unknown now]. Not re-checked in this session; no Bolna API call was made while preparing this plan |
| Operators | [unknown]. The user declined role-play for now because of credits ("theres too little credits to test the role play"). Pravesh's Hindi text review is pending and Pravesh has not been contacted |

## 2. Billing: what the sources say and what our receipts show

[vendor claim] Bolna's pricing page (fetched 2026-10-28) lists pay-as-you-go from 6.00 US cents per minute with speech-to-text, LLM and text-to-speech bundled for preferred models, telephony and a platform fee added per minute, and lower rates for larger top-ups. Its docs say the voice components are billed by duration, the LLM by tokens generated, telephony "rounded to minutes", and that `conversation_duration` is the figure billing uses. The Pilot plan is billed in 30-second pulses. Which of these applies to our wallet is not stated.

[verified on our account] Eight earlier Bolna web calls, cost against duration:

| Call | Duration | Cost (US cents) |
|---|---|---|
| S1 greeting | 11.1 s | 2.75 |
| S3 legit, first try | 8.6 s | 2.75 |
| S1 stub | 31.3 s | 5.5 |
| S3 legit | 48 s | 5.5 |
| S3 probe 1 | 52 s | 5.5 |
| S3 English scam | 58 s | 5.5 |
| S3 Hindi scam | 60 s | 8.25 |
| S6 probe | 135.6 s | 13.75 |

[hypothesis] Every row fits `2.75 cents x ceil(duration / 30 s)`, which would be about 5.5 cents per minute. That is a fit to eight points, not a documented rule: the 60 s Hindi row only fits if the true duration was just over 60 s, durations in the older notes are rounded, and Hindi calls use different speech providers. The 13.75 cents for 135.6 s is not used alone to derive a rate. The mismatch with the docs' "rounded to minutes" wording is unexplained. Treat the hypothesis as an estimate and cap by reserve, not by prediction.
Before the first call, read the agent's "cost per minute" breakdown in Agent Studio and the `cost_breakdown` of one earlier execution, and write down the real components. If they disagree with the fit, replace the numbers below first.

## 3. Cost model used below

- Expected per English Guardian call: 11 to 17 cents [hypothesis], from 4 to 6 started 30-second units (120 s to 180 s). The agent now asks five things and a repeat-back, so calls are likely longer than the 52 s to 58 s S3 calls; the S6 probe ran 135.6 s with a fixed-clip caller.
- **Conservative reserve per call: 25 cents.** It covers the 180-second caller cap with up to 3 s of hang-up delay at 30-second units (7 units, 19.25 cents), and also a 6-cent-per-minute worst case rounded up to 4 minutes (24 cents). The failed S6 plan used the same 25-cent reserve.
- Hindi per call: reserve 30 cents [hypothesis]; the one Hindi data point (8.25 cents at 60 s) suggests a higher rate than English, and only one point.
- The caller caps Guardian calls at 180 seconds client side. A server-side `call_terminate` limit in the agent's Call tab would be a second cap, but setting it is an agent update that needs its own named permission.
- A cap is the user's number. The table gives reserves; the expected column is only to show likely spend.

## 4. Options, cheapest first

Every option starts with Option A. Later options run only after A passes.

| Option | Calls | Expected spend | Reserve and suggested cap | Needs |
|---|---|---|---|---|
| **A. Single confirmation-first probe** | 1 English: `en-ica-video-01` (the repaired fixture, same case as the failed probe, so the change is the only difference) | 11 to 17 cents | 25 cents | an English role-play operator (the user, if willing) |
| **B. Essential reduced English** (the original cut-order floor) | A plus 4: `en-telco-minlaw-01`, `en-courier-paid-01`, `en-legit-grandson-01`, `en-legit-bank-app-01` | 55 to 85 cents | 125 cents (5 x 25) | same operator; no rerun in the cap; one rerun adds 25 cents |
| **C. Full English** | the 12 English fixtures, with A counting as `en-ica-video-01` only if it passed `check.py` for that case under the same conditions | 132 to 204 cents | 300 cents (12 x 25) | same operator for about 12 calls of up to 3 minutes |
| **D. Hindi** | 3: `hi-mom-handoff-01`, `hi-courier-paid-01`, `hi-legit-bank-app-01` | about 25 to 60 cents [hypothesis] | 90 cents (3 x 30) | a Hindi-speaking operator [unknown who]; Pravesh's text review recorded first |
| Whole contract (C plus D) | 15 | about 160 to 265 cents | 390 cents | all of the above |

Reduced samples cannot establish the full target. B is reported as "4 plus probe, reduced", never as 7 of 8. The thresholds do not change:

- English: at least 7 of 8 scams `likely_scam`, at most 1 of 4 legit look-alikes flagged, `en-courier-paid-01` urgent with the bank and 1799 advice first.
- Hindi: 2 of 2 scams, 0 of 1 legit, `hi-courier-paid-01` urgent.
- Every `likely_scam` alerts and no other verdict does; zero secret-looking identifier leaks; call length recorded against the 3-minute target.
- Option A passing proves only the five stored values and exactly one confirmed tool call on one call.

If the 277.25-cent reading still holds, A and B fit with a margin and C does not fit with its full reserve. Whole-contract spend would need a top-up, which only the user can make. Run in stages and re-read the wallet between them rather than topping up in advance.

## 5. Stop conditions

Stop immediately, keep the evidence and report; do not retry automatically:

1. Option A fails any of: all five values stored and plausible, exactly one `match_script` call after an explicit yes, full verdict spoken, no refusal to help, repeat count spoken when `similar_count` is at least 1. No sample follows a failed probe.
2. A leak of an NRIC, OTP, card number, password or bank/PayNow-looking identifier by an agent in any transcript, or an agent claiming to be a government officer, police or a bank. This is a hard failure.
3. A call above the 180-second cap, or cumulative reserve reached, or the wallet below the next call's reserve.
4. Two consecutive calls with a tool-call count other than one.
5. A cost per call above the reserve, or a charge with no call. Stop and reconcile before anything else.
6. Operator unavailable, a mic or transport fault, or any ambiguity about which case was spoken. A call with an unclear case is recorded as invalid, not as a pass.
7. Render not answering `/healthz` after a warm-up. Cold starts may exceed Bolna's tool timeout [unknown]; hit `/healthz` once before each batch and note any slow first tool response.

## 6. Evidence and reruns

- Per call: execution id, case, `caller_mode=live`, `human_roleplay`, duration, cost and wallet before and after, the stored check row, tool-event count, transcript, alert status, and `check.py` output. `scripts/caller/runs.jsonl` and `work/scamkaki-s6/` receipts are kept; nothing is deleted, including failed calls.
- A rerun is labeled a rerun with its attempt number (`check.py` already counts attempts) and its cost is added to the total. A fail followed by a pass is reported as flaky, not as a clean pass.
- "Telegram sent" means Telegram accepted the message. Arrival on the family phone is claimed only if the user confirms it.
- Report pass rates with their sample sizes. Hindi stays "offline-checked only" until a named listener's review is recorded.

## 7. Deployment and agent changes, and who must permit them

| Change | Needed? | Permission to request by name |
|---|---|---|
| Deploy S7 to Render | No, S6 does not depend on it. Without it the live dashboard stays the old one, so results are read through `check.py` and the Neon rows | pushing and fast-forwarding `main`, separate from this plan |
| Guardian agent update | No; both agents already carry the tested configuration | any new PUT |
| `call_terminate` limit on the agents | Optional extra cost cap | an agent update |
| Session mint and each call | Yes | calls and a total cap, in US cents, stated by the user |
| Wallet top-up | Only if the chosen option's reserve exceeds the wallet | the user performs it |
| Reading the wallet and an earlier execution's cost fields | Read-only, to replace the unknowns in section 1 | an explicit go-ahead before the API key is used |
| Contact with Pravesh | Only for Option D | the user's decision; no outreach was made |

## 8. Decisions needed from the user

1. Which option: A only, A then B, A then C, or A then C and D.
2. A total cap in US cents (the table gives reserves; a rerun is extra).
3. Who plays the senior (English), and who for Hindi. Confirm they are available; the user earlier declined role-play for credit reasons.
4. Whether a passing A counts as the `en-ica-video-01` result inside C.
5. Whether to set `call_terminate` as a second cap.

No part of this plan has been run. Nothing was minted, called, updated or paid for while preparing it.
