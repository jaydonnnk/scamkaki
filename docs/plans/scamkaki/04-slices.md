# Slice plan: Scamkaki

Compact gate draft, 2026-10-22.
Riskiest first.
Each slice ends with a visible, working result and evidence in `evidence/`.
Branch per slice: `scamkaki/slice-<N>-<slug>`.

## Build order

| ID | Slice | Visible result | Tests and evidence | Authorizations to request |
|---|---|---|---|---|
| S1 | Tracer: Guardian stub end to end | A phone call to Guardian hears the stub "Not sure, please call your family"; the call appears on the dashboard | Unit: env example test. Integration: webhook token, webhook stores call, match-script token. Evidence: call id, dashboard screenshot, execution JSON shape, whether call variables round-trip | `uv` install of pinned deps; Neon project + test branch; Render deploy; Bolna agent create; up to 3 test calls |
| S2 | Hokkien voice spike | Guardian speaks Hokkien through Bolna custom TTS | 5 sample lines, time per reply recorded; go/no-go: under 2 s per reply and intelligible to a Hokkien speaker, else stock voice with a Singlish-auntie prompt | Modal GPU spend; model licence check before deploy |
| S3 | Guardian verdict and family transfer | A scam description gets "likely scam", the call transfers to a teammate's phone; a legit description does not transfer | Unit: all `decide`, `sentence_for` tests with branch mutations. Live: 2 role-play calls (1 scam, 1 legit) | Up to 5 test calls; teammate phone number as transfer target |
| S4 | Ah Ma Bait with extraction and leak guard | A teammate scammer call produces a script row and a draft report on the dashboard | Unit: extraction and all leak tests with self-test and mutations. Integration: stores script and draft, idempotent, flags leak. Live: `scripts/check.py bait` over 5 scam fixtures, at least 4 payees and zero leaks | Up to 15 agent-vs-agent test calls |
| S5 | The loop: Guardian uses Bait's scripts | Guardian says "same script heard N times this week" for a script Bait collected | Integration: 7-day count, error returns unclear. Live: `scripts/check.py guardian` over 8 fixtures, at least 4 of 5 scams and at most 1 of 3 legit flagged | Up to 20 test calls |
| S6 | Dashboard, report review and demo | Dashboard matches the Gate 1 mockups at phone and desktop widths; "Mark reviewed" works; demo rehearsed 3 times; backup video recorded | Integration: review marks reviewed and sends nothing. Evidence: screenshots, demo run log | Render warm-up or paid instance if cold starts break calls |

S1 and S2 are independent and can run in parallel; S3 needs S1; S4 needs S1; S5 needs S3 and S4; S6 needs S5.

## Never cut

S1, S3, S4's leak guard, and the fixture labels on every screen.

## Cut order (first cut first)

1. S6 polish beyond the mockups (keep "Mark reviewed" and fixture labels).
2. S2 Hokkien voice: fall back to a stock Bolna voice and show Hokkien as roadmap.
3. S5 live 8-case run: reduce to 3 cases, reported as such.

## Stretch, not planned

BothBosu offline check of `decide`; MERaLiON post-call re-transcription; SIP trunk `Diversion` detection; Mandarin Guardian agent.

## Plan-wide rules

- No slice starts without your authorization by ID.
- Every pass rate is reported with its sample size, as fixture results.
- A failed live run keeps its evidence; reruns are reported as reruns.
