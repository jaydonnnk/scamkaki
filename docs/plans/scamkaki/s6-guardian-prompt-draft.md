# Guardian EN prompt draft for the next S6 probe

Drafted 2026-10-29 at the user's request. **A draft only.** Nothing was sent to Bolna; applying it is an agent update that needs its own approval. It changes wording only: no model, temperature, max_tokens, tool, schema or silence-timeout change.
It targets two failures in call `eb4b7e5f` (see `evidence/s6-guardian-live.md`): denied warning signs stored as present, and two `match_script` calls. A prompt line is an instruction, not an enforced guard, so a pass on one probe would not prove the rule holds.

## Edits to `agent_prompts.task_1.system_prompt` (`agents/guardian.json`)

**1. Replace** the sentence "Never infer a warning sign from a question you asked, a denial or the senior trusting the caller." **with:**

> Record a warning sign only if the senior says it happened. A sign the senior denies ("did not", "no", "never", "didn't") is absent: leave it out. Example: "they did not threaten me and did not know my IC" means no urgency_threat and no knew_details. Never infer a sign from your own question or from the senior trusting the caller. If an answer is garbled and you cannot tell whether a sign happened or was denied, ask one short yes or no question about that sign before you repeat back.

**2. Replace** step 6 **with:**

> 6. Repeat back in short phrases: who, channel, what they asked, every warning sign you will send, and what the senior did, or "no warning signs". Never send a sign you did not say in the repeat-back. Example: "So China police, WhatsApp video, move savings. Handoff, moved to video. Nothing done yet." Then ask: Is that right? Only a clear yes to this complete repeat-back counts (yes, yeah, correct, right). A reply that adds, corrects or denies a fact is not a yes: fix the summary and ask again. Do not call match_script before this yes, and not after the senior's denials or any other answer.

**3. Replace** the first sentence of step 7 ("After confirmation, call match_script exactly once with all five values, keeping enum values in English.") **with:**

> 7. After the clear yes, call match_script once with all five values, keeping enum values in English. After it returns, never call it again in this call, even if the senior speaks or adds a fact.

**4. In step 8, replace** "or call the tool again" **with** "or call the tool again. If the senior adds a fact after the verdict, say: Please tell your family that too. Then say goodbye."

Everything else in the prompt is unchanged. Nothing here removes "Say each sentence once" (the prompt still repeated whole sentences in call `eb4b7e5f`; a rule alone has not stopped that).

## How it would be applied and checked

- Apply with `PATCH /v2/agent/{id}` carrying only `agent_prompts`, as on 2026-10-29 (a full PUT failed webhook validation), then read back and compare the prompt; update `agents/guardian.json`; unit test `test_hi_agents_match_english_twins` must still pass.
- The Hindi agent is not changed.
- Then one probe on the reworded `en-ica-video-01`, 25 cents of reserve, inside the 95 cents left. Pass means `check.py guardian --case en-ica-video-01` exits 0. If it fails on `tool_count` again, stop and ask about an enforced guard instead of another prompt edit.
