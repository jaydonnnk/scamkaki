# Status: Scamkaki

Updated: 2026-10-22 (Asia/Singapore).

- Gate 1 - Product: **APPROVED 2026-10-22** ([01-product.md](01-product.md), [mockups](mockups/)).
- Gate 2 - Architecture: **APPROVED 2026-10-22** ([02-architecture.md](02-architecture.md)).
- Gate 3 - Program Design: **APPROVED 2026-10-22** ([03-program-design.md](03-program-design.md)).
- Gate 4 - Slice plan: **APPROVED 2026-10-22** ([04-slices.md](04-slices.md)).

The user asked for compact versions of all four gates in one pass because of hackathon time (2026-10-22: "draft compact versions of all four in one pass as we dont have much time").
No slice is authorized or started.
No implementation, install, provisioning, deployment, spending or phone call is authorized.

## Slices

- [ ] S1 - Tracer: Guardian stub end to end
- [ ] S2 - Hokkien voice spike
- [ ] S3 - Guardian verdict and family transfer
- [ ] S4 - Ah Ma Bait with extraction and leak guard
- [ ] S5 - The loop: Guardian uses Bait's scripts
- [ ] S6 - Dashboard, report review and demo

## Notes for a fresh session

- Language: Python (user decision 2026-10-22).
- Stack: Bolna only as organiser tech; FastAPI on Render; Neon Postgres; Modal for Hokkien TTS. Structured script matching, no embeddings.
- Superseded: the Next.js and pgvector build plan in `PROGRESS.md` is replaced by these gate drafts.
- Git: `main` pushed to private `https://github.com/jaydonnnk/no-scamkaki` at `7e41056` on 2026-10-22; `outputs/` and `work/` are ignored as local research.

## Approval history

- 2026-10-22: Gates 1-4 approved together by the user ("Yea i approve all four gates.").
  Approval accepts the compact drafts as written, including the least confident decisions in Gate 3, as a proposal; it establishes no runtime, account or model evidence.
  It starts no slice and authorizes no install, provisioning, deployment, spending or phone call.
- 2026-10-22 amendment (user: "Im not using blueprint it costs money"): no `render.yaml`; the Render web service is created by hand in a per-project environment with variables entered manually. Removed `render.yaml` from Gate 3's file list; no behaviour, test or slice change, so no gate reopens.
- 2026-10-22 rename (user: "its wording only so leave the gate approved"): product renamed from Scam Ah Ma to Scamkaki; package `src/scamkaki/`, gate folder `docs/plans/scamkaki/`, branch prefix `scamkaki/`. Persona names Ah Ma Bait and Ah Ma Guardian unchanged. Wording only; no gate reopens.
