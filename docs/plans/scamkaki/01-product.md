# Product: Scamkaki

Compact gate draft, 2026-10-22.
Revised 2026-10-22: languages are English and Mandarin; Hokkien dropped; Hindi is a stretch after all slices.

## Problem

Senior (in their words): "Got one man call me, say he police, say my bank account got problem. I don't know real or not. My grandson working, I don't want to disturb him."
Family member: "By the time Ah Ma tells me, the money is gone. I can't be on the phone with her all day."
Today the ScamShield Helpline (1799) serves the official languages through operators when available, and its four-language phone menu was only planned for 2026 [verified, MHA reply Sep 2025].
Government-impersonation scams remain a top-five scam type in Singapore [verified, SPF mid-year brief 2026].

## Who

- **Senior:** speaks English (including Singlish) or Mandarin; may not read English; gets a suspicious call.
- **Family member:** wants to be pulled in only when it matters.
- **Scammer:** calls in English or Mandarin with a script (fake SPF, ICA, MOH, China official, bank, courier) and wants money, an OTP, an app installed or personal details.
- **Reviewer:** a human on our side who reads report drafts before anything leaves the system.

## Journeys

1. **Ah Ma Guardian.** A senior calls the English or the Mandarin Guardian line after a strange call. A friendly auntie voice, in that line's language, asks who called, what they said, and whether they asked for money, a code or an app. Guardian answers "likely scam", "not sure, talk to family" or "no scam signs found", and says if the same script was heard recently. On "likely scam" it tells the senior not to transfer anything and connects the call to the family member.
2. **Ah Ma Bait.** A scam call reaches the English or the Mandarin Bait line. "Mdm Tan" plays a confused auntie in that language, stalls, and gets the scammer to say which agency they claim, what they want, and where the money should go. She never gives out an NRIC, OTP, card or account number.
3. **Dashboard.** The reviewer sees each call with its language, the scam scripts heard this week grouped by agency and demand, and a draft report per Bait call. Marking a report reviewed records the review; nothing is sent anywhere by the system.

## Success metric

Real-world target [hypothesis]: a senior who calls Guardian about a scam call reaches a family member within 3 minutes, with no money moved.
Hackathon measure, on labeled fixtures only, tested by agent-vs-agent calls:

- Guardian flags at least 4 of 5 scam fixtures as "likely scam" and at most 1 of 3 legit look-alike fixtures.
- Bait captures the planted payee detail in at least 4 of 5 scam fixtures.
- Zero NRIC, OTP, card or account-number leaks by Ah Ma across all test calls.
- Mandarin agents run a reduced fixture set, reported separately: Guardian flags at least 2 of 2 scam cases and 0 of 1 legit case; Bait captures the payee in at least 1 of 2 scam cases with zero leaks.

These are fixture results, never performance against real scammers.

## Announcement

Ah Ma doesn't need to know if it's a scam. She just needs one number to call.
Scamkaki gives Singapore seniors a phone line that listens in English or Mandarin, checks what they heard against scam scripts caught this week, and brings in family before money moves.
Behind it, Ah Ma Bait picks up scam calls herself, plays along, and learns the newest scripts so Guardian is never a week behind.
Every report is a draft that a person checks; nothing is filed automatically.

## Screens

- [`mockups/dashboard.html`](mockups/dashboard.html): live call feed and "scripts this week".
- [`mockups/report.html`](mockups/report.html): one Bait call's report draft with a "Mark reviewed" action.
- Guardian and Bait are phone-only; no screen.

## Out of scope

Hokkien and other dialects; Hindi until every slice is done (stretch); one agent that switches language mid-call; automatic filing to ScamShield, SPF or banks; blocking or intercepting calls on a senior's phone; real scam-number seeding; multi-family accounts; Singapore number provisioning beyond what Bolna offers.
