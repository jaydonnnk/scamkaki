# Product: Scamkaki

Compact gate draft, 2026-10-22.
Revised 2026-10-22: languages are English and Hindi; Hokkien dropped; Mandarin is a stretch after all slices, blocked until Bolna accepts `zh` speech-to-text.
Revised 2026-10-24: on "likely scam" Guardian alerts the family on a family alert page and by Telegram instead of transferring the call, because Bolna blocked the transfer on our account ([evidence](evidence/s3-guardian-verdict.md)).

## Problem

Senior (in their words): "Got one man call me, say he police, say my bank account got problem. I don't know real or not. My grandson working, I don't want to disturb him."
Family member: "By the time Ah Ma tells me, the money is gone. I can't be on the phone with her all day."
Today the ScamShield Helpline (1799) serves the official languages through operators when available, and its four-language phone menu was only planned for 2026 [verified, MHA reply Sep 2025].
Government-impersonation scams remain a top-five scam type in Singapore [verified, SPF mid-year brief 2026].

## Who

- **Senior:** lives in Singapore and gets a suspicious call. Most speak English (including Singlish). A Hindi-speaking minority, for example elderly parents of Indian professionals living here on a Long-Term Visit Pass, may not follow English well; they get the Hindi line. The number of Hindi-speaking seniors in Singapore is [unknown].
- **Family member:** wants to be pulled in only when it matters, and is reachable on Telegram or a bookmarked family alert page on their phone.
- **Scammer:** calls in English or Hindi with a Singapore script (fake SPF, ICA, MOM, MOH, China official, bank, courier) and wants money, an OTP, an app installed or personal details.
- **Reviewer:** a human on our side who reads report drafts before anything leaves the system.

## Journeys

1. **Ah Ma Guardian.** A senior calls the English or the Hindi Guardian line after a strange call. A friendly auntie voice, in that line's language, asks who called, what they said, and whether they asked for money, a code or an app. Guardian answers "likely scam", "not sure, talk to family" or "no scam signs found", and says if the same script was heard recently. On "likely scam" it tells the senior not to transfer anything, says it has alerted the family, and the family member gets a Telegram message and a flashing alert on the family page with who the caller claimed to be, what they wanted, the line and the time.
   The family member then calls the senior back.
2. **Ah Ma Bait.** A scam call reaches the English or the Hindi Bait line. "Mdm Tan" (English) or "Mrs Sharma" (Hindi) plays a confused auntie, stalls, and gets the scammer to say which agency they claim, what they want, and where the money should go. She never gives out an NRIC, OTP, card or account number.
3. **Dashboard.** The reviewer sees each call with its language, the scam scripts heard this week grouped by agency and demand, and a draft report per Bait call. Marking a report reviewed records the review; nothing is sent anywhere by the system.

## Success metric

Real-world target [hypothesis]: when a senior who calls Guardian about a scam call hears "likely scam", the family is alerted within 1 minute and calls the senior back before any money moves.
Hackathon measure, on labeled fixtures only, tested by agent-vs-agent calls:

- Guardian flags at least 4 of 5 scam fixtures as "likely scam" and at most 1 of 3 legit look-alike fixtures.
- Every "likely scam" verdict in a test call produces a family alert, and no other verdict does.
- Bait captures the planted payee detail in at least 4 of 5 scam fixtures.
- Zero NRIC, OTP, card or account-number leaks by Ah Ma across all test calls.
- Hindi agents run a reduced fixture set, reported separately: Guardian flags at least 2 of 2 scam cases and 0 of 1 legit case; Bait captures the payee in at least 1 of 2 scam cases with zero leaks.

These are fixture results, never performance against real scammers.

## Announcement

Ah Ma doesn't need to know if it's a scam. She just needs one number to call.
Scamkaki gives seniors in Singapore a phone line that listens in English, and in Hindi for those who don't follow English well, checks what they heard against scam scripts caught this week, and alerts family before money moves.
Behind it, Ah Ma Bait picks up scam calls herself, plays along, and learns the newest scripts so Guardian is never a week behind.
Every report is a draft that a person checks; nothing is filed automatically.

## Screens

- [`mockups/dashboard.html`](mockups/dashboard.html): live call feed and "scripts this week".
- [`mockups/report.html`](mockups/report.html): one Bait call's report draft with a "Mark reviewed" action.
- [`mockups/family.html`](mockups/family.html): the family alert page, opened from a secret link the family member bookmarks.
- Guardian and Bait are phone-only; no screen.

## Out of scope

Hokkien and other dialects; Mandarin until every slice is done (stretch); one agent that switches language mid-call; transferring the senior's call to a family phone (blocked on our Bolna account, see S3 evidence); automatic filing to ScamShield, SPF or banks; blocking or intercepting calls on a senior's phone; real scam-number seeding; multi-family accounts; Singapore number provisioning beyond what Bolna offers.
