# Status: Scamkaki

Updated: 2026-10-27 (Asia/Singapore).

- Gate 1 - Product: **APPROVED 2026-10-27** (re-approved after the sophisticated-scam revision) ([01-product.md](01-product.md), [mockups](mockups/)).
- Gate 2 - Architecture: **APPROVED 2026-10-27** (re-approved after the sophisticated-scam revision) ([02-architecture.md](02-architecture.md)).
- Gate 3 - Program Design: **APPROVED 2026-10-27** (re-approved after the sophisticated-scam revision) ([03-program-design.md](03-program-design.md)).
- Gate 4 - Slice plan: **APPROVED 2026-10-28** (re-approved after the S5 split) ([04-slices.md](04-slices.md)).

The revision lives on branch `scamkaki/gates-sophisticated-scams`, cut from `main`; not yet committed or merged.

The gate revision branch `scamkaki/gates-english-mandarin` was fast-forwarded into `main` (with S1) and deleted on 2026-10-22.

The user asked for compact versions of all four gates in one pass because of hackathon time (2026-10-22: "draft compact versions of all four in one pass as we dont have much time").
S1 authorized 2026-10-22 by the user ("You have my authorization to start slice 1"), with the installs ("I give authroizeation for 7") and a Bolna budget of $5 for today and tomorrow.
S2 was authorized and closed 2026-10-22 (see approval history). S3 authorized 2026-10-23 and closed 2026-10-24; S4 authorized 2026-10-24 and closed 2026-10-26; S5 authorized 2026-10-27, paused the same day by the gate reopening, and re-authorized 2026-10-28 under the new contract; S6 and S7 are not yet authorized.

## Slices

- [x] S1 - Tracer: Guardian stub end to end, branch `scamkaki/slice-1-guardian-tracer`, done 2026-10-22; [evidence](evidence/s1-tracer.md). Deviation: tested by Bolna dashboard web call because the trial plan dials only +1/+91.
- [x] S2 - Hindi voice, branch `scamkaki/slice-2-hindi-voice`, done 2026-10-22, **go**; [evidence](evidence/s2-hindi.md). Guardian HI (Sarvam `saaras:v4` + `bulbul:v3` `ritu`) extracted agency and demand in 2 of 3 post-fix synthetic calls; Hindi listener Pravesh: understandable, warnings clear, pace OK. Open for S3: repeat-back gets clipped when the caller keeps talking; English Guardian lacks the confirm-first steps.
- [x] S3 - Guardian verdict and family alert, branch `scamkaki/slice-3-guardian-verdict`, done 2026-10-24; [evidence](evidence/s3-guardian-verdict.md). Bolna call transfer was blocked on our account, so the app alerts the family by Telegram and a family page (gates re-approved 2026-10-24). Live: English scam and Hindi scam alerted (`sent`), English legit did not; 6 calls (one over plan, a cut-off attempt), 33 cents. Limits: smoke test only, alert seconds not measured, Hindi likely-scam ending awaiting Pravesh's re-check.
- [x] S4 - Ah Ma Bait with extraction and leak guard, branch `scamkaki/slice-4-bait`, done 2026-10-26; [evidence](evidence/s4-bait.md). Synthetic caller, web calls. English: payees 5 of 5, zero leaks (pass). Hindi: 2 of 4 payees over two runs (first run 0 of 2, retry with Lekha at default speed and reworded payee questions 2 of 2), zero leaks: **flaky**, recorded as such by the user's decision. 9 calls, 74.25 cents. Limits: one scripted call per case; the caller does not react to Ah Ma; Hindi speech-to-text garbles digit words; not real scammers.
- [ ] S5 - Sophisticated verdict behind the tool, no calls, branch `scamkaki/slice-5-guardian-loop`, in progress (re-authorized 2026-10-28, no calls); [evidence](evidence/s5-sophisticated-verdict.md). Code and tests done 2026-10-28: unit 138 passed, integration 60 passed on the Neon test branch with migration 0005, every Guardian fixture 15 of 15 through the real route, 14 of 14 mutations caught. Open: push and fast-forward `main` for Render, migration 0005 on production, then the Render `curl` run, deployed family page and Telegram evidence; the urgent-first ordering keeps an old urgent alert on top (Gate 3 wording decision). Earlier on this branch: 7-day count, Guardian caller mode, `check.py guardian`; probe call `47a10fcb` showed Bolna did not call the tool with an execution id in the param template, so checks link to calls by time.
- [ ] S6 - Guardian asks the new questions, live
- [ ] S7 - Dashboard, report review and demo

## Notes for a fresh session

- Language: Python (user decision 2026-10-22).
- Stack: Bolna only as organiser tech, with stock speech providers; FastAPI on Render; Neon Postgres. Structured script matching, no embeddings.
- Languages: English and Hindi, one Bolna agent per persona and language; Mandarin is a stretch after S7, blocked until Bolna accepts `zh` speech-to-text; Hokkien is dropped (2026-10-22).
- Superseded: the Next.js and pgvector build plan in `PROGRESS.md` is replaced by these gate drafts.
- Git: `main` pushed to private `https://github.com/jaydonnnk/scamkaki` at `7e41056` on 2026-10-22; `outputs/` and `work/` are ignored as local research.

## Approval history

- 2026-10-22: Gates 1-4 approved together by the user ("Yea i approve all four gates.").
  Approval accepts the compact drafts as written, including the least confident decisions in Gate 3, as a proposal; it establishes no runtime, account or model evidence.
  It starts no slice and authorizes no install, provisioning, deployment, spending or phone call.
- 2026-10-22 amendment (user: "Im not using blueprint it costs money"): no `render.yaml`; the Render web service is created by hand in a per-project environment with variables entered manually. Removed `render.yaml` from Gate 3's file list; no behaviour, test or slice change, so no gate reopens.
- 2026-10-22 rename (user: "its wording only so leave the gate approved"): product renamed from Scam Ah Ma to Scamkaki; package `src/scamkaki/`, gate folder `docs/plans/scamkaki/`, branch prefix `scamkaki/`. Persona names Ah Ma Bait and Ah Ma Guardian unchanged. Wording only; no gate reopens.
- 2026-10-22 amendment (user: "Add the Talk to Guardian button to our dashboard"): new route `POST /web-call/session` mints a Bolna Web Call SDK session for the Guardian agent, and the dashboard gets a Talk to Guardian button. Reason: the trial plan dials only +1/+91. Known risk: the dashboard has no auth, so anyone with the URL can start calls on the wallet. Added test `test_web_call_session_mints_for_guardian_agent`. No gate reopens.
- 2026-10-22 amendment (user: "add a simple authentication system. So that only me(admin) can access scamkaki"): HTTP Basic sign-in (`ADMIN_USERNAME`, default `admin`, and `ADMIN_PASSWORD`) guards `/` and `/web-call/session`; locked when no password is set. Webhook, tool and `/healthz` keep their own checks. Four tests added; each guard mutated alone fails a test. No gate reopens.
- 2026-10-22 language change (user: "It should only be english and chinese(hindi is an add on for if we 're done with all the slices)"): Hokkien and the Modal custom TTS are dropped; languages are English and Mandarin; Hindi is a stretch after S6.
  User choices the same day: both Guardian and Bait get Mandarin; one Bolna agent per language, not one multilingual agent; S2 becomes the Mandarin voice slice in the same build and cut position.
  Model check done before the change, kept as context: MERaLiON-OmniVoice-Hokkien-TTS has public ungated weights under the MERaLiON Public Licence v3, which asks for an A*STAR acknowledgment; not used now.
  This changes approved decisions in all four gates, so Gates 1-4 are reopened and need re-approval. S2 is not authorized.
- 2026-10-22: Gates 1-4 re-approved after the language change (user: "Approve all four gates, but before we continue with slice 2, lets check whether bolna's speech to text handles mandarin"). S2 is not yet authorized; a Mandarin STT check comes first.
- 2026-10-22 Mandarin pre-check: Bolna refuses `zh` speech-to-text on every transcriber at agent creation; `hi` is accepted ([evidence](evidence/s2-mandarin-stt-precheck.md)). No call placed, no spend.
- 2026-10-22 language swap (user: "Okay then lets swap hind and chinese. So we do both english and hindi, chinese if all slices are done."): languages are English and Hindi; Mandarin becomes the stretch after S6. Gates 1-4 reopened for re-approval. S2 is not authorized.
- 2026-10-22 Gate 1 re-approved (user: "Sure") after the Hindi line was framed for Hindi-speaking minorities in Singapore facing Singapore scams (MOM added to the claimed agencies), and the Hindi Bait persona named "Mrs Sharma". Gates 2-4 still need re-approval.
- 2026-10-22 Gates 2-4 re-approved (user: "apprive all gates and commit and pusj to main thanks"). S2 is not yet authorized.
- 2026-10-22 S2 authorized (user: "Yea i authorize s2. Plese start on a new branch and i authroize the creation o the guardian agent, and up to 3 web calls."), then 3 more calls ("Yep i authorize go ahead"). S2 code fast-forwarded to `main` at `1fdfa21` on the user's instruction so Render could deploy it ("Yep u can push to main").
- 2026-10-22 S2 extra calls authorized ("okay sure", "sure make that one call"); `main` pushed to `ea020a9` on the user's instruction. S2 recorded as go after the listener verdict.
- 2026-10-23 S3 authorized (user, answering "Do you authorize S3 ...": "Yes, authorize S3"), covering the branch, the code and Bolna updates to both Guardian agents including a transfer tool; calls and pushes are asked separately.
  The user chose one probe call first to learn whether a web call can transfer, and the family number lives only in settings (`FAMILY_TRANSFER_NUMBER`), with a placeholder in `agents/*.json`.
- 2026-10-23 Gate 3 wording amendment (user: "Approve amendment"): `sentence_for(verdict, similar_count, language)` and a `language` field on `POST /tools/match-script`, recording what S2 already built for the Hindi line. No gate reopens.
- 2026-10-23 S3 push authorized (user: "Okay i authoruize pushing thus branch and fast forwarding to main so tht render deploys this new logic").
- 2026-10-24 S3 transfer probes: Bolna blocked the transfer to the family phone ("request blocked by outbound URL policy"); 2 calls, 11 cents ([evidence](evidence/s3-guardian-verdict.md)).
  Change (user: "Yes A+C is really good", then "Secret link. Start the gate drafts as well"): on "likely scam" the app alerts the family on a family alert page reached by a secret link and by Telegram, instead of transferring the call.
  This changes approved decisions in all four gates, so Gates 1-4 are reopened and need re-approval before the S3 alert work continues.
- 2026-10-24 Gates 1-4 re-approved after the family alert change (user: "yes i approve all four gates"). S3 continues under its 2026-10-23 authorization; calls beyond the 5 and pushes are still asked separately.
- 2026-10-24 S3 deploy and calls authorized (user: "I approve A B and C"): migration 0003 on production, push and fast-forward `main`, Bolna Guardian agent updates, and the 3 remaining S3 calls (2 English, 1 Hindi).
- 2026-10-24 S4 authorized (user, answering "Do you authorize S4 ...": "Yes, authorize S4"), covering the branch `scamkaki/slice-4-bait`, the code, migration 0004 on the Neon test branch and Bait EN and Bait HI agent creation on Bolna; calls, pushes, the production migration and Render settings are asked separately.
  Same answers: push and fast-forward the S3 close-out `c8658ff` into `main` ("Yes, push and ff main"), and an S4 Bolna budget of $0.75 ("Up to $0.75").
- 2026-10-24 amendment, Gates 1-4 test method (user chose "Synthetic caller (Recommended)"): Bolna documents no agent-to-agent test feature, its test calls need a phone number a person answers, the trial plan dials only +1/+91, and Bait has no number, so the planned test Scammer and Senior agents cannot call our agents.
  Live fixture calls instead use a synthetic caller: a local page plays each case's scripted caller lines (macOS `say`) into a Bolna web call and passes the case id as web call `user_data`; `scripts/check.py` reads the stored results.
  `agents/test_scammer.json`, `agents/test_senior.json` and `BolnaClient.start_call` are dropped; S4 runs 7 calls (5 English, 2 Hindi) within $0.75.
  Limit: the scripted caller cannot react to Ah Ma's replies. S5 inherits this method. Decision wording only in Gates 1-3; no gate reopens.
- 2026-10-26 S4 deploy authorized (user: "Yes, all three"): push `scamkaki/slice-4-bait`, fast-forward `main` so Render deploys, and migration 0004 on production (applied 2026-10-26). The user set `BOLNA_BAIT_AGENT_ID` and `BOLNA_BAIT_HI_AGENT_ID` on Render ("Done, both set").
- 2026-10-26 S4 closed (user: "Push the slice branch, fast-forward main, run the architect-reviewer cleanup and close S4, recording Hindi as 2 of 4 flaky."). Post-slice cleanup found no orphan, stale or redundant files.
  Amendment recorded at close, no gate reopens: `POST /web-call/session` takes `line` (`guardian` or `bait`) and forwards web call `user_data`; the dashboard has Bait call buttons and shows Bait scripts with draft reports.
- 2026-10-27 S5 authorized (user: "Yes, authorize S5: branch scamkaki/slice-5-guardian-loop, the code, Guardian EN/HI agent updates if needed, no fresh Bait calls, budget $1.50, up to 18 live Guardian calls. Use your recommended case linking (A, then B). Pushes, ff main and any migration asked separately.").
  Case linking: A passes the Bolna execution id in the Guardian tool call; B, the fallback, matches each check to its call by time. Pushes, fast-forward of `main` and any migration are asked separately.
- 2026-10-27 steer (user: "I want scamkaki guardian to be tailored such that even sophisticated scams via voice can be noticed as a scam"; then "Yes, reopen Gates 1-4 and draft the sophisticated-scam revision. Pause S5."): the seeded scripts were too easy to recognise.
  Due diligence against the SPF mid-year brief 2026: 80.8% of scams are self-effected transfers; 65+ are 40.8% of government impersonation victims; new telco-to-official handoffs; cash and valuables handover; courier fee phishing that adds cards to mobile wallets; phone calls 9.7% of contact methods and falling.
  Draft revision: Guardian asks contact channel, three warning-sign questions and whether the senior already acted; `decide` adds harmful-act, red-tactic and friend-money branches; already-acted calls get bank and 1799 advice and an urgent family alert; Guardian fixtures rewritten (12 English, 3 Hindi); Bait unchanged; S5 contract grows.
  This changes approved decisions in all four gates, so Gates 1-4 are reopened. S5 is paused; no calls, pushes or agent updates are authorized by this reopening.
- 2026-10-27 Gates 1-4 re-approved after the sophisticated-scam revision (user: "I approve Gates 1-4 as drafted.").
  Approval accepts the drafts as written, including Bait unchanged and the least confident decisions 8-12 in Gate 3, as a proposal; it establishes no runtime or model evidence.
  S5 stays paused until re-authorized under the revised contract. No commit, push, merge, migration, Bolna agent update or call is authorized by this approval.
- 2026-10-28 revision commit `023d97c` fast-forwarded into `main` and pushed (user: "Commit, ff main, push to main, then draft the plan for the reminaing slices accordingly. Add more slices / modify remaining slices if neede"); `git ls-remote` shows `main` at `023d97c`.
  Slice replan drafted on branch `scamkaki/gates-slice-replan`: S5 becomes the sophisticated verdict behind the tool with no calls; new S6 updates the Guardian agents and runs the live fixture calls; the dashboard and demo slice becomes S7. Gate 4 is reopened; Gates 1-3 change wording only (slice references), not decisions.
- 2026-10-28 Gate 4 re-approved after the S5 split (user: "I approve Gate 4 as drafted."). S5 stays paused until re-authorized under the new S5 contract; S6 and S7 are not authorized. No commit, push or merge of the replan branch is authorized by this approval.
- 2026-10-28 S5 re-authorized under the new contract (user: "Commit the replan, ff main and push. I authorize S5 under the new contract: continue on scamkaki/slice-5-guardian-loop merged with main, migration 0005 on the Neon test branch. Production migration and pushes for Render asked separately. No calls.").
  Covers: the replan commit, fast-forward and push of `main`; merging `main` into `scamkaki/slice-5-guardian-loop`; the S5 code; migration 0005 on the Neon test branch. Not covered: production migration, pushes for Render, Bolna agent updates, any call.
