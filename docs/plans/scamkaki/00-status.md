# Status: Scamkaki

Updated: 2026-10-22 (Asia/Singapore).

- Gate 1 - Product: **APPROVED 2026-10-24** (re-approved after the family alert change) ([01-product.md](01-product.md), [mockups](mockups/)).
- Gate 2 - Architecture: **APPROVED 2026-10-24** (re-approved after the family alert change) ([02-architecture.md](02-architecture.md)).
- Gate 3 - Program Design: **APPROVED 2026-10-24** (re-approved after the family alert change) ([03-program-design.md](03-program-design.md)).
- Gate 4 - Slice plan: **APPROVED 2026-10-24** (re-approved after the family alert change) ([04-slices.md](04-slices.md)).

The gate revision branch `scamkaki/gates-english-mandarin` was fast-forwarded into `main` (with S1) and deleted on 2026-10-22.

The user asked for compact versions of all four gates in one pass because of hackathon time (2026-10-22: "draft compact versions of all four in one pass as we dont have much time").
S1 authorized 2026-10-22 by the user ("You have my authorization to start slice 1"), with the installs ("I give authroizeation for 7") and a Bolna budget of $5 for today and tomorrow.
S2 was authorized and closed 2026-10-22 (see approval history). S3 authorized 2026-10-23; S4 to S6 are not yet authorized.

## Slices

- [x] S1 - Tracer: Guardian stub end to end, branch `scamkaki/slice-1-guardian-tracer`, done 2026-10-22; [evidence](evidence/s1-tracer.md). Deviation: tested by Bolna dashboard web call because the trial plan dials only +1/+91.
- [x] S2 - Hindi voice, branch `scamkaki/slice-2-hindi-voice`, done 2026-10-22, **go**; [evidence](evidence/s2-hindi.md). Guardian HI (Sarvam `saaras:v4` + `bulbul:v3` `ritu`) extracted agency and demand in 2 of 3 post-fix synthetic calls; Hindi listener Pravesh: understandable, warnings clear, pace OK. Open for S3: repeat-back gets clipped when the caller keeps talking; English Guardian lacks the confirm-first steps.
- [ ] S3 - Guardian verdict and family alert, branch `scamkaki/slice-3-guardian-verdict`, in progress; resumed after the Gates 1-4 re-approval on 2026-10-24. Verdict code is built and deployed; 2 of 5 calls used ([evidence](evidence/s3-guardian-verdict.md)).
- [ ] S4 - Ah Ma Bait with extraction and leak guard
- [ ] S5 - The loop: Guardian uses Bait's scripts
- [ ] S6 - Dashboard, report review and demo

## Notes for a fresh session

- Language: Python (user decision 2026-10-22).
- Stack: Bolna only as organiser tech, with stock speech providers; FastAPI on Render; Neon Postgres. Structured script matching, no embeddings.
- Languages: English and Hindi, one Bolna agent per persona and language; Mandarin is a stretch after S6, blocked until Bolna accepts `zh` speech-to-text; Hokkien is dropped (2026-10-22).
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
