# S1 evidence: Guardian tracer

Date: 2026-10-22 (Asia/Singapore). Labeled test calls by the team, not real scam calls.

- Deploy: `https://scamkaki.onrender.com/healthz` returned `{"ok":true}` from branch `scamkaki/slice-1-guardian-tracer`.
- Agent: `a2cf7af2-1902-4abd-8bac-71b5a4d75d2a`; `GET /v2/agent` confirmed `webhook_url`, `match_script` tool (POST, bearer token), `gpt-5.4-mini`.
- Channel: Bolna dashboard web call (`telephony_data.provider = web-call`). Trial plan only dials +1 and +91, so no phone call was possible.
- Call `4fbe6e50-e283-44a6-86bb-879ea36d73f8`: completed, 31.3 s, 5.5 cents. Transcript: the user said police asked them to transfer money; agent said "Okay, let me check for you." then "Not sure. Please call your family before doing anything." plus a reminder not to transfer money or share codes.
- Call `00664724-8825-44df-b16c-ce1abcc3fb49`: completed, 11.1 s, 2.75 cents, greeting only.
- Database: both calls stored with line `guardian`, status `completed`; one `guardian_checks` row `spf` / `transfer` / `unclear`.
- Execution JSON shape: `context_details` has only `recipient_data` (empty for dashboard web calls); call-variable round-trip is not yet proven and is retested in S4 with `fixture_case`.
- Tests: 5 passed (`uv run pytest -q`); each token guard mutated alone fails one test.
- Spend so far: 8.25 cents of $5.00.
