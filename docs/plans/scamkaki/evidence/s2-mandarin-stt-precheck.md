# S2 pre-check: Mandarin speech-to-text on Bolna

Date: 2026-10-22.
Authorized by the user ("Yes, create the threowaway agent and run th test calls").
Result: **no-go for Mandarin**; the user then swapped Mandarin for Hindi.

## Method

A throwaway agent body (echo-back prompt, no webhook, no tools, ElevenLabs `eleven_turbo_v2_5` voice) was sent to `POST /v2/agent` with each transcriber and a Chinese language code.
Bolna validates `model` and `language` as a pair at creation, so a refusal means no call can be made.
The probe script lived in the session scratchpad, not the repository.

## Results [verified 2026-10-22, our account]

Every request below returned `400 Provided language: <language> is not available for the model: <model>`.

| Provider | Model | Languages tried |
|---|---|---|
| `assembly` | `universal-3-6-pro` | `zh`, `multi` |
| `deepgram` | `nova-2` | `zh`, `zh-CN`, `zh-Hans`, `zh-TW` |
| `deepgram` | `nova-3` | `multi` |
| `deepgram` | `flux-general-multi` | `zh` |
| `openai` | `gpt-realtime-whisper` | `zh`, `multi` |
| `elevenlabs` | `scribe_v2_realtime` | `zh`, `multi` |
| `gladia` | `solaria-1` | `zh`, `multi` |
| `azure` | `azure` | `zh` |
| `google` | `chirp_3` | `zh` |
| `soniox` | `stt-rt-v5` | `zh` |
| `gemini` | `gemini-3.5-transcribe-live` | `zh` |
| `smallest` | `pulse` | `zh` |
| `sarvam` | `saaras:v4` | `zh` |

Control: the same body with `assembly` / `universal-3-6-pro` / `hi` returned `201` (agent `64a3bab7-22c7-42d3-9ac9-0a8427bb7092`), which was deleted at once (`200`).

## Interpretation

- Bolna's docs list `zh` for AssemblyAI, Deepgram `nova-2` and OpenAI [vendor claim], but the API refuses it; whether this is account, region or platform-wide is [unknown].
- `hi` passing creation proves only that the configuration is accepted, not Hindi transcription quality.
- No call was placed and nothing was spent.
