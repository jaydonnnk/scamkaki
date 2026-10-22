# S2 evidence: Hindi voice

Date: 2026-10-22 (Asia/Singapore).
Branch `scamkaki/slice-2-hindi-voice`.
All calls are labeled fixture test calls with a synthetic caller, not real seniors or real scammers.

## Setup

- Guardian HI agent `f86cc044-3c02-49aa-b1bd-b04b2f3d4e3a`, created from `agents/guardian_hi.json`.
- Transcriber: Sarvam `saaras:v4`, `hi`. Voice: Sarvam `bulbul:v3`, `ritu`. LLM: `gpt-5.4-mini`. All three are on Bolna's flat-rate preferred list [vendor claim, pricing docs].
- Deploy: Render runs `main` at `1fdfa21`; `POST /tools/match-script` with `language: hi` returned the Hindi sentence (four probe requests, each logged an `spf/transfer/unclear` row in `guardian_checks`).
- Migration `0002_calls_language.sql` applied to production.
- Caller: a local test page minted a Bolna web call session server-side and fed a macOS `say -v Lekha` (hi_IN) clip into the call as its microphone, because the in-app browser blocks microphone access.
  The clip (line 1): "हाँ, अभी एक आदमी ने फ़ोन किया। बोला वो सिंगापुर पुलिस से है। उसने कहा मेरे बैंक खाते में गड़बड़ है और मुझे सारा पैसा एक सुरक्षित खाते में ट्रांसफर करना होगा।"
  Expected extraction: `spf` / `transfer`.

## Calls (3 of 3 authorized)

| # | Execution | Length | Cost | Valid | Extracted | Notes |
|---|---|---|---|---|---|---|
| 1 | `d8ededa5-346f-4a7b-a914-90eac2ff6151` | 18 s | 2.75 c | No | none | Harness bug: the Web Call SDK's microphone preflight stops the tracks it gets, and the test page returned the same stream twice, so Bolna heard silence and hung up after 10 s. Fixed by returning a cloned track per request; verified locally (second stream `live`, peak 0.278). |
| 2 | `c5c32a97-69fd-41a9-9a43-7d27f1e9af8d` | 42 s | 5.5 c | Yes | `other/other`, then `other/transfer` | Endpointing 500 ms. STT cut the turn after the first sentence; Guardian called `match_script` at once, and the "police" sentence was lost while it spoke. |
| 3 | `49da0351-7a17-4617-8995-e7a5752f8ebc` | 42 s | 5.5 c | Yes | `other/other` | Endpointing 1000 ms and a prompt rule to ask for the missing half first. Still split ("बोला वो सिंगापुर।"); Guardian called the tool early, then improvised "यह धोखा हो सकता है" instead of a second tool call. |

- Webhook: calls 1-3 stored with `line = guardian`, `language = hi` [verified, production DB].
- Hindi STT: the captured text matches the clip word for word where it was captured (for example "खाते में गड़बड़ है और मुझे सारा पैसा एक सुरक्षित खाते में ट्रांसफर करना होगा।") [verified, transcripts].
- Latency (Bolna `latency_data`): LLM time to first token 526-954 ms per turn; time to first audio 6.0-6.5 s at call start.
- Extraction: 0 of 2 valid calls correct. The exit check needs at least 2 of 3.
- Spend this slice: 13.75 cents (Bolna total 22 cents of the $5.00 budget).

## Open

- Listener verdict: recordings of calls 2 and 3 handed to the user for a Hindi speaker; verdict [unknown].
- Go/no-go: not decided; turn-taking, not transcription, is the failing part.
