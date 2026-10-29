# Progress

Current goal: S7 (dashboard, report review, demo) built and checked locally on `scamkaki/slice-7-dashboard-demo`, uncommitted; open items: backup video unavailable, full live demo not run. S6 live validation plan drafted in docs/plans/scamkaki/s6-live-validation-plan.md (not authority). Evidence: docs/plans/scamkaki/evidence/s7-dashboard-demo.md. Scratch (ignored): work/scamkaki-s7/.
Historical research and the superseded build plan below are context only; current authority is in docs/plans/scamkaki/00-status.md.

- [x] Read AGENTS.md and the user-authored Evidence check - Claude.md; preserve the source report.
- [x] Verify TRAI amendment text, commencement dates, complaint thresholds and enforcement statistics. Verified 30/60/90-day phases; actual commencement date remains uncertified.
- [x] Verify CNAP and DPDP timelines and separate the obligations they create. CNAP order dated 13 October; DPDP framework commencement is not proof that an application portal opens then.
- [x] Check incumbent coverage and accessible carrier interfaces; challenge repeatability, monitoring and buyer claims. Plivo UCC and CallMissed declaration gates are already documented; carrier filing and universal flag access remain unverified.
- [x] Synthesize verified facts, corrections and remaining evidence gates without implementing a product. Saved `outputs/Evidence audit - Codex.md`; preserved the user-authored source.

## Run log

2026-10-18: Research-only review. `git status --short --branch` returned `fatal: not a git repository (or any of the parent directories): .git`. No branch or worktree can be created here; no Git repository initialized. Workers use separate notes files. No code, build system, lint configuration or test suite exists in this research folder, so software checks are not applicable. Verification uses primary regulatory texts, published carrier interfaces and source cross-checks. No live calls, carrier-account actions or messages to others are authorized by this review.

Primary evidence checked directly: rendered TRAI notification pages 1 and 3 and DoT CNAP order page 1 with `view_image`; Plivo UCC API and CallMissed Campaigns API with `web.open`/`web.find`; Plivo 140-series provisioning documentation. Retained scans and PDFs in `work/trai-audit-assets/` and the identity notes evidence folder. These checks verify published contracts and text, not authenticated API behavior or production effectiveness.

Also visually inspected TRAI notification page 9 for complaint thresholds and staged sanctions, and checked PIB release 2261823 directly for the government's May 2027 DPDP timeline. Read the completed audit against those sources and corrected the CallMissed citation to the exact campaign-readiness page.

## Result

Completed a primary-source audit and a separate report without editing `outputs/Evidence check - Claude.md`. The regulatory trigger is stronger than the earlier technical lead, but existing products cover several proposed capabilities. Carrier-confirmed filing interfaces, universal flag visibility, cross-carrier repeatability and buyer willingness to pay remain unverified. Actual TRAI commencement dates are not certified. No code, account changes, live calls, outreach or authenticated API tests were performed; these were outside this research review.

## Shazam integration check, 2026-10-18

- [x] Verify current direct integrations and ShazamKit capabilities using primary sources. Apple confirms Siri uses Shazam; SoundHound documents recognition with spoken requests; Apple documents custom reference catalogs dating to WWDC21.
- [x] Explain what is already served and what a broader sound-recognition interpretation would change; preserve the early/platform criteria.

Research only. No new report or implementation is planned for this focused question. Clarification requested about actual Shazam music recognition versus Shazam-style recognition of other sounds.

Verification: Apple Support `https://support.apple.com/en-nz/118570`, SoundHound's identifying/playing and hands-free support pages, Apple ShazamKit overview and WWDC21 material, opened with `web.open`/`web.search`. Search-indexed ChatGPT directory extracts and March 2026 news reports mention Shazam, but direct directory pages redirect to the current plugins catalog, where `web.find` finds no Shazam; current ChatGPT or live Voice Mode availability is not verified. Do not present the indexed listing as confirmed-current. No live app test performed.

## Organiser and sponsor tools, 2026-10-18

- [x] Confirm the event and six sponsors from the official Buildathon page; explain Bolna, Plivo, Exotel, Sarvam, Cartesia, Deepgram and Kalpa from current official documentation.

Assumption: the question concerns the Bolna Buildathon described in this folder. Verification used `web.open`, `web.click` and `web.find` on `https://www.bolna.ai/symphony/buildathon`, Bolna's agent overview and Plivo/Exotel integration pages, and the Sarvam, Cartesia, Deepgram and Kalpa documentation. `git status --short --branch` again returned `fatal: not a git repository (or any of the parent directories): .git`. This remains a research folder with no software test/build/lint suite.

Result: prepared a plain-language explanation of provider roles, Bolna's agent/graph/workflow tools and the call-processing sequence. Verified published capabilities only; no live API or account tests. Native Bolna support for Kalpa was not established.

## Singapore India voice opportunities, 2026-10-18

- [x] Verify recent technical changes and public Buildathon requirements.
- [x] Research Singapore and Singapore-India problems, including Reddit/X signals.
- [x] Check prior art, filter weak ideas and explain the surviving concepts plainly.
- [x] Deliver a concise shortlist and linked HTML comparison with sources.

Research-only run. Strict freshness window: after 18 September through 18 October 2026. Assumptions: prefer one sponsor company per idea in addition to organiser Bolna; no product implementation, live calls or outreach. Existing research remains background and will not be overwritten. Isolated research notes are under `work/research_notes/Singapore India voice opportunities/`; this folder is not a Git repository, so worker worktrees and software checks do not apply. Distinguish exact Bolna-artifact dependence from universal vendor exclusivity; the latter has not been established.

Evidence: root independently opened Bolna September changelog and graph import/export, Sarvam 22 Sep/4 Oct, Deepgram 2/8 Oct, MOM KET language FAQ, Netic's correction failure account, Due Chain's revision-bound workflow and the prospective SG-India exporter's Reddit body. `web.open` failed twice for Bolna October HTML/Markdown; `curl --fail --silent --show-error --location --max-time 25 https://www.bolna.ai/docs/changelog/october-2026.md` succeeded. Root renovation-thread fetch returned 429; researcher had inspected its body earlier. Hammer PDF direct fetch failed, with official indexed text available via `web.search`. X produced no usable original posts; no X sentiment is claimed.

Corrections/decisions: Cartesia September marketing does not establish new underlying capabilities; Bolna Oct15 is new SIP management, with legacy SIP already working. Sarvam Sep22 streaming keyterms supersede older REST/batch-only notes; Bolna keywords remain fixed per call. Deepgram Oct8 corrects Oct2's over-limit behavior to transcription stopping without an Error. Voice testing/minimization, procurement calls, safety acknowledgments, care teach-back and voice change orders all have prior art. Prefer reviewed correction/action consistency over adding graph edges everywhere; Netic's report warns graph complexity can worsen failures. All proposed gaps remain hypotheses.

Verification: a `python3` standard-library `HTMLParser` check compared the two Markdown files byte-for-byte, checked four HTML idea sections, the expandable evidence section, unique IDs, every local anchor target, expected source-link protocols and no external assets. All passed. CUA `reviewTab.goto("file:///Users/jayd0/Desktop/bolna/outputs/singapore-india-voice-ideas.html")` was rejected by the browser URL policy, which permits only HTTP/HTTPS; no alternate route was attempted. Browser rendering remains unverified. Corrected the illustrative shipping scene to use dispatch/arrival-plan revisions instead of implying same-day road travel across India/Singapore; clarified that graph compilation is our proposed custom work, not a verified Bolna built-in.

Result: saved `outputs/Singapore India voice opportunities.md`, identical working report in `work/reports/`, and `outputs/singapore-india-voice-ideas.html`. Shortlist: Undo Compiler, RevisionRelay, AgreementDiff as a domain application, and Trunk Doctor. Strongest native target is reviewed Bolna graph/tool-policy repair; customer-facing coordination remains a demand hypothesis. Exact vendor exclusivity and newly-possible-this-month status are not established. No product implementation, calls, account actions, outreach, installs or publication performed.

## Singapore infrastructure voice ideas, 2026-10-18

- [x] Verify Singapore-specific infrastructure, developer access and existing products.
- [x] Generate and reality-check ideas where the Singapore infrastructure is essential.
- [x] Explain the strongest ideas with one sponsor, freshness limits and honest access gates.

User correction: geography alone does not satisfy the request. Envoi/SGQR is the reference for structural dependence; no forced India narrative. New idea schema requires the named SG system, concrete data/action it enables, removal test, actual API/access boundary and existing overlap before an idea enters the shortlist. Research only; preserve older reports. Reuse current-day verified voice releases but do not call mature SG infrastructure newly released. New notes are isolated under `work/research_notes/Singapore infrastructure voice ideas/`.

Evidence: root `web.open` verified RedeemSG CFHP FAQ, physical-store eligibility, retry/idempotency contract and EPOS's existing voucher support; SG Peppol Invoice Response and PINT credit-note schemas; TradeTrust SDK owner/holder/surrender operations and reference UI Sepolia support; ServiceNow quantity-dispute voice agent. OneMap BFA direct read returned zero extracted lines; official indexed text through `web.search` confirmed approved-user access and selected coverage. LTA PDF `web.open`/`web.find` confirmed MRT lift maintenance is not HDB-wide, GTFS launch was 3 Aug 2026, and 1 Oct added faulty-traffic-light coordinates, not train GTFS. Public docs are not account access or executed API proof.

Decision: shortlist ClimateTill/RedeemSG, InvoiceNow Rescue/SG PINT, AccessTrip/OneMap+LTA (approval-dependent), TradeTrust Instruction Guard (Singapore-developed, globally usable). Reject generic Singpass wrappers, gated SGFinDex promises, plain OpenCerts readers and voice municipal reports already supplied by OneService. All four are upgrade hypotheses with named prior art; no under-month SG infrastructure unlock was established. Plain-language report and HTML comparison are being prepared. Prior local-file browser block remains in force; no preview workaround will be attempted.

Verification/result: saved `outputs/Singapore infrastructure voice ideas.md`, byte-identical working report under `work/reports/`, and `outputs/singapore-infrastructure-voice-ideas.html`. Root read the full report and ran a standard-library `python3`/`HTMLParser` check: four concept sections, four evidence disclosures, unique IDs, valid local anchors, expected link protocols and no scripts/external resources; all passed. No browser preview was attempted under the existing local-file policy block. No live SG API, retailer/provider account, government access, field usability, model accuracy or buyer demand was verified; no transactions, calls, product implementation, outreach or installs occurred. Research is complete with these explicit limits; original geographic framing is superseded by actual SG protocol/data dependence.

## Voice-first Singapore ideas, 2026-10-22

- [x] Re-check Bolna Oct changelog for fresh unlocks (custom TTS 12 Oct, SIP trunks 15 Oct, SIP headers 18 Oct, debug API 21 Oct, Sarvam keywords 2 Oct).
- [x] Find SG speech tech: MERaLiON-3-3B-ASR (Hokkien/Cantonese/Singlish, OpenAI-compatible serve), MERaLiON-OmniVoice-Hokkien-TTS (Reddit claim, ATxSummit 2026, card not opened), SEA-LION v4.8 (~mid Sep, date inferred).
- [x] Shortlist voice-first ideas: Ah Ma Line (Hokkien calls), Scamkaki (forwarded scam-call honeypot), Singlish Stress Test (Bolna agent QA).

Limits: Bolna has no custom STT, so Hokkien listening relies on listed STT providers plus post-call MERaLiON re-transcription. Custom TTS is whole-clip MP3, 20 s timeout, refused on multilingual agents. Carrier passing of `Diversion` on SG forwarded calls unverified. Hokkien TTS weights/licence unverified. O2 Daisy (2024) is prior art for the honeypot. No calls, installs or account actions.

### Ah Ma Line deep dive, 2026-10-22

- [x] Hokkien TTS card opened: exists, MERaLiON-3 Public Licence (terms unread), Han-character input, 0.8B, CUDA, 24 kHz, voice cloning, no streaming/OpenAI server, small LLM-judged eval only.
- [x] Bolna STT: no Hokkien anywhere; AssemblyAI has `zh`/`yue`; Gemini on Bolna has no Chinese. Custom TTS refused on multilingual agents.
- [x] Prior art: Lions Befrienders + Seasalt.ai NANA (30 Apr 2026, companion check-ins, Singlish/Mandarin/Malay/Tamil/Cantonese, no Hokkien, 1,000+ seniors). Pivot: critical-message delivery with proof of understanding, Hokkien first.
- Plivo SG numbers need Enterprise plan; SG blocks non-local caller ID on domestic calls.

## Scamkaki deep dive, 2026-10-22

- [x] Prior art: Apate.ai (TechCrunch 14 Oct 2026) runs AI victim personas at scale for TPG/CBA; no SG/Asia customer named. Honeypot alone is not novel.
- [x] SG context: SPF H1 2026 16,821 cases, S$410.6M losses; 1799 ScamShield Helpline has no dialect support, 4-language IVR only planned for 2026; Protection from Scams Act ROs (12 issued by 15 Feb 2026); Bill 16 of 2026 adds account disabling orders (passage unconfirmed).
- [x] Reframed: honeypot (Ah Ma answers scammers) feeds a victim-side Hokkien Guardian line. Guardian is the differentiator.

Unverified: Diversion header on SG conditional forwarding, Plivo SG number KYC, Hokkien TTS Mandarin ability, legal review of recording/reporting.
- 2026-10-22 decision: Bolna-only stack. Deepgram/Plivo/Exotel dropped as named sponsors; STT/telephony via Bolna defaults. Forwarding-detection (Diversion header) becomes stretch since it needs own carrier trunk.
- 2026-10-22 test corpus: no public Singapore scam-call audio found. Usable: BothBosu/scam-dialogue (EN text, synthetic, 1,600 rows, Apache-2.0); TeleAntiFraud-28k (ZH audio, 12.7 GB, gated, Apache-2.0); MultiFraudAlign (synthetic multilingual, licence unchecked). SG scripts must be built from SPF advisories/scamalert.sg stories, then generated as synthetic dialogues and Bolna-vs-Bolna test calls.

## Build: Scamkaki (Bolna-only), plan 2026-10-22

Goal: demo-ready Ah Ma Bait + Guardian on Bolna, with minimal sample testing gating each step.
Stack: Bolna graph agents (gpt-5.4-mini), Next.js on Vercel (webhook, `match_script` tool, dashboard, Web Call SDK), Neon Postgres + pgvector, Modal GPU for Hokkien TTS behind `/v1/audio/speech`.
Test set `seed/scripts.json`: 8 hand-written cases from SPF advisories, 5 scam (SPF, ICA/China official, MOH, bank, courier) and 3 legit look-alikes (polyclinic reminder, bank callback, delivery), each with a planted payee value. Paraphrased, no victim details.
Test runner `scripts/check.mjs`: pulls executions over the Bolna API and prints pass/fail per case.

- [ ] 0. Accounts (Bolna, Modal, Neon, Vercel), Bolna number, repo skeleton, write `seed/scripts.json`. Done: stock agent answers a test call.
- [ ] 1. Hokkien TTS spike on Modal + Bolna custom TTS. Done: preview plays Hokkien, <2 s per reply over 5 sample lines. No-go after a few hours: stock voice + Singlish auntie prompt.
- [ ] 2. Guardian agent + `match_script` stub + transfer to a teammate phone. Test: 2 role-play calls (1 scam, 1 legit), transfer fires only on scam.
- [ ] 3. Ah Ma Bait agent + extraction + webhook into Neon. Test: Bolna "Scammer" agent calls Bait for the 5 scam cases; `check.mjs` asserts planted payee extracted (>=4/5) and zero NRIC/OTP/account leaks (hard fail).
- [ ] 4. Real `match_script` (embeddings + pgvector, keyword fallback). Test: Bolna "Senior" agent calls Guardian for all 8 cases; >=4/5 scams flagged, <=1/3 legit flagged.
- [ ] 5. Dashboard: live feed, script clusters, report drafts, Web Call "play scammer" button.
- [ ] 6. Rehearse 3-min demo x3, record backup video.
- [ ] Stretch: BothBosu offline check of `match_script`; MERaLiON ASR post-call re-check; SIP trunk Diversion detection.
- 2026-10-22 repo structured after Envoi: new `AGENTS.md` (Envoi rules adapted to Python/macOS/Bolna, plus product hard rules), old workflow preserved at `docs/agentic-workflow.md`, gate folder `docs/plans/scamkaki/` with `00-status.md` (all gates NOT STARTED), `src/scamkaki/{app,domain,integrations,lib}`, `agents/`, `tts_modal/`, `migrations/`, `seed/`, `scripts/`, `tests/{unit,integration,e2e,support}`, `config/`, `README.md`, `.env.example`, `.gitignore`. Assumption: Python. Not a git repo yet.
- 2026-10-22 git init on `main` (no commits; `outputs/`, `work/` ignored). Compact Gates 1-4 drafted in `docs/plans/scamkaki/` with two HTML mockups; awaiting approval. Next.js/pgvector plan above is superseded by the gate drafts (FastAPI, structured matching).
- 2026-10-22 Gates 1-4 APPROVED by user; no slice authorized yet.
- 2026-10-22 skeleton committed (7e41056) and pushed to private origin jaydonnnk/no-scamkaki main, verified with git ls-remote.
- 2026-10-22 S1: Render live at https://scamkaki.onrender.com (/healthz ok). Guardian agent created a2cf7af2-1902-4abd-8bac-71b5a4d75d2a; GET /v2/agent confirms webhook_url, match_script tool (POST, bearer set), gpt-5.4-mini.


## S6 execution, 2026-10-28

Authority/spec: docs/plans/scamkaki/00-status.md and 04-slices.md.
S6 branch scamkaki/slice-6-guardian-live, from original main 59b918d; offline code/evidence committed as b5eb2b3 under the later publication request.
Inherited .claude/, 33 obsolete clips and all original S6 audio remain untouched.
Spent US$0.1375; remaining S6 cap US$0.8625, user deferred all further calls.

- [x] First five-field implementation and checker; original failed probe retained.
- [x] Caller live microphone mode, fixture id/mode labeling, no clip-timed turns, 180 s cap.
- [x] Approved three fixture corrections applied; verdict rules/expectations unchanged.
- [x] Guardian clip cache uses text digests; 91 current WAVs valid, old audio preserved.
- [x] Both Guardian updates PUT/read back: gpt-5.4-mini, temperature 1, max_tokens 300,
      stronger help and explicit yes. Wallet before/after 277.25 cents, delta zero.
- [x] Fresh full suite 244 passed (183 unit, 61 integration), one existing warning.
- [x] Ruff lint/format, Node offline caller check and diff whitespace pass.
- [!] S6 live exit checks unmet. User declined role-play/testing for credit reasons.
- [ ] Pravesh text review pending; packet ready, no outreach or Hindi live call.

Probe cd987c05-777a-48df-bfed-59381f9ea8cd: 135.6 s, rows 46-48, three successful tool calls
and alert_status=sent; arrival unverified. Timing/fixture ambiguity confound the other failures.
No sample, follow-up or retry ran. Preserve the first call, transcript and frozen fixture hash.
Safe receipts: work/scamkaki-s6/. Canonical evidence: evidence/s6-guardian-live.md in gate folder.
Scoped fault receipts: original checker/params 23; caller 8; config literals 8; fixtures/cache 4.
Initial scanner mutation targeted Bait by mistake; retained invalid receipt, corrected proof caught.
Whole-object read-back initially rejected backend defaults; supplied values matched recursively.
Temperature 0.3 was rejected by documentation, not by a paid attempt; supported 1 approved by user.

No tool-withholding feature verified. Call-end alert fallback needs separate approval because it
changes urgent timing and "I have alerted your family". No Bait, dashboard or domain-code edits.
No installs, migrations or clip deletion. Current-tree publication was later authorized; S7 implementation remains unauthorized.
Offline preview on 8766, PID 9291, and real caller on 8765 are stopped.


## S7 handoff, 2026-10-28

- [x] Read user-supplied Envoi S22 reference and re-verify main/HEAD 59b918d, dirty S6 tree.
- [x] Record Claude design-skill/palette direction in Gates 1/3 and status; no UI implementation.
- [x] Record S7-before-S6-validation-planning exception in Gate 4; no live-proof waiver.
- [x] Write s7-handoff.md and the independent s7-handoff-review.md prompt.
- [!] S7 implementation remains unauthorized. The user later authorized current-tree main publication.
After S7, only a priced S6 validation plan is requested. No calls, spend or S7 code came from
the handoff. Its later Git publication is covered by the user's separate request. PROGRESS grants no approval.


## Main publication, 2026-10-28

User requested the current working tree be pushed to main. Prior no-publication notes above
are historical. S6 remains incomplete live; S7 implementation remains unauthorized.
- [x] Verify branch/main/remote at 59b918d and empty index before staging.
- [x] Source hashes match, lint/format/Node caller checks pass, value-free pattern scan passes.
- [x] Fresh full pytest: 244 passed, one existing warning. Source commit b5eb2b3; launcher ac34285.
Final gate/handoff records are the publication's documentation concern. Main is fast-forwarded
and pushed only under this request; the task reports exact final HEAD and ls-remote verification
in chat after publishing. A fresh session resolves current Git state directly, not from old SHAs.
Reviewed .claude/launch.json: only uv caller-server launch settings, no credentials; preserved
it unchanged in configuration commit ac34285. No ignored clips, logs, work receipts or env files staged.

## Website redesign preview, 2026-10-30

Current UI request only; earlier S6/S7 notes above are historical. Authority remains in
`docs/plans/scamkaki/00-status.md`, never this progress record.
- [x] Verified clean main at 154d1d72fc1518b1f5f29ec53024207cdf141a28; created scamkaki/gates-ui-redesign.
- [x] Built eight standalone HTML screen proposals, preserving existing application code.
- [x] Browser checks at 1280 and 375 px; search, filter, empty/error, review and mock voice controls.
- [x] Mirrored pending amendment in Gates 1-4 and status; checks/ui-redesign-preview.md records limits.
- [x] Reconcile subsequent user direction with status authority and draft the three remaining gate amendments together.
- [x] Synchronize the later user decision in the authority documents; no implementation started.
Preview on 127.0.0.1:8782, server session 75911; Ctrl-C stops it. Retained browser tab is the output.
Generator and screenshots are scratch in work/ui-redesign/. No application tests, calls,
provider access, database actions, installs, commits, pushes or deployments occurred.


## Website redesign gate drafting, 2026-10-30

- [x] Re-verified branch/HEAD and retained all prior in-scope dirty files/previews.
- [x] Read current routes, queries, schema and tests; drafted route/data, signature/test and S8-S12 contracts.
- [x] Preserved known evidence limits: recorded time, no inferred call/check link, sent vs received.
- [ ] S8 implementation remains unstarted; its separate authority is pending in 00-status.md.
Local drafting only. No credentials, database, providers, installs or Git publication used.


## S8 handoff preparation, 2026-10-30

- [x] Read the user-supplied Envoi reference as a structural example only.
- [x] Synchronize the current authority state across gate/status mirrors.
- [x] Re-verify local main/HEAD and remote main at 154d1d7, empty index, no S8 branch.
- [x] Inventory installed tools and known local files without reading credential values.
- [ ] S8 code and destructive test-branch checks remain unstarted pending named authority.
Authority is only in 00-status.md. Handoff and review prompt are in the gate folder.
- [x] Wrote s8-handoff.md and the independent read-only s8-handoff-review.md prompt.
- [x] Documentary checks: approval mirrors, exact copied contract, eight-section order, source boundary and whitespace pass.
No S8 branch/code, test-database mutation, installation or Git publication occurred.


## Redesign publication preparation, 2026-10-30

Current request covers committing this session's documentation/preview/handoff package and
fast-forwarding/pushing main. Scope and exact user words are recorded only in 00-status.md.
- [x] Re-verify branch, empty index, local/remote source baseline 154d1d7 and known file inventory.
- [x] Update handoff/review/Gate 4 mirrors so the old uncommitted snapshot is clearly historical.
Final publication completion is evidenced by Git refs and the task's reported remote SHA;
no hash or successful push is predicted within the commit being published.
S8 code and destructive test-branch work remain unstarted; ignored scratch/audio/env stay local.
- [x] Fresh documentary/HTML/contract/whitespace checks passed for the 17-file package.
- [x] Bounded credential-pattern scan found no matches; no application suite/database reset run.
