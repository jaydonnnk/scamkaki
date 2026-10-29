# Product: Scamkaki

Compact gate draft, 2026-10-22.
Revised 2026-10-22: languages are English and Hindi; Hokkien dropped; Mandarin is a stretch after all slices, blocked until Bolna accepts `zh` speech-to-text.
Revised 2026-10-24: on "likely scam" Guardian alerts the family on a family alert page and by Telegram instead of transferring the call, because Bolna blocked the transfer on our account ([evidence](evidence/s3-guardian-verdict.md)).
Revised 2026-10-27 (reopened): Guardian is redrafted for sophisticated scams. It asks how the senior was contacted, listens for the tricks polished scams use, asks whether the senior already paid or gave a code, and tells a senior who already acted what to do now. The fixtures are rewritten so the senior does not sound suspicious.

## Problem

Senior (in their words): "The Singtel lady was very professional, she knew my IC number. Then she passed me to a Ministry of Law officer. He said must keep it secret, even from my son. I think it's real, but I just want to check."
Senior, after the fact: "The SMS said my parcel cannot deliver. I paid one dollar sixty-four on the website with my card and put in the code. Is that a problem?"
Family member: "By the time Ah Ma tells me, the money is gone. I can't be on the phone with her all day."

Facts that shape this:

- 80.8% of reported scams in the first half of 2026 were transfers the victim made, not account takeovers [verified, SPF mid-year brief 2026].
- Seniors aged 65 and above are 40.8% of government official impersonation victims, reached mainly by phone calls and WhatsApp, and lose the most per victim of any age group (S$42,347 on average) [verified, SPF mid-year brief 2026].
- Scammers now pose as Singtel, YouTrip or Prudential first, then pass the victim to a fake MinLaw, MAS or SPF officer; ATM cash deposits and handing over cash and valuables continue [verified, SPF mid-year brief 2026].
- Courier phishing asks for card details and an OTP to pay a small redelivery fee, after which the card is added to Google Pay or Apple Pay [verified, SPF advisories 15 Jul and 5 Aug 2026].
- A senior who is being deceived well does not feel suspicious, so a line that waits for suspicion misses the best scams [hypothesis].
- Today the ScamShield Helpline (1799) serves the official languages through operators when available, and its four-language phone menu was only planned for 2026 [verified, MHA reply Sep 2025].

## Who

- **Senior:** lives in Singapore and has been contacted by someone who wants them to do something: a call, an SMS, a WhatsApp message or a website. Most speak English (including Singlish). A Hindi-speaking minority, for example elderly parents of Indian professionals living here on a Long-Term Visit Pass, may not follow English well; they get the Hindi line. The number of Hindi-speaking seniors in Singapore is [unknown].
- **Family member:** wants to be pulled in only when it matters, and is reachable on Telegram or a bookmarked family alert page on their phone.
- **Scammer:** speaks fluent, polite English or Hindi and sounds official. Uses Singapore scripts: a telco or bank that hands the senior to a government officer (SPF, MinLaw, MAS, ICA, MOM, China officials); a bank fraud team that already knows card digits; a courier redelivery fee paid on a website; an investment chat group that shows early profits; a job that pays for small tasks first; a friend's hijacked WhatsApp asking for an urgent loan; an officer who asks for cash or gold to be handed over or deposited at an ATM. Wants money, an OTP, card details, an app installed or personal details, and tells the senior to keep it secret and stay on the line.
- **Reviewer:** a human on our side who reads report drafts before anything leaves the system.

## Journeys

1. **Ah Ma Guardian.** A senior calls the English or the Hindi Guardian line before moving money for anyone, or after any strange call or message. A friendly auntie voice, in that line's language, asks:
   - who contacted them and how (call, SMS, WhatsApp, website);
   - what they asked for: money moved, cash or gold handed over, a code, card details, an app, personal details, or nothing;
   - three short warning-sign questions: were you passed to another officer or company; were you told to keep it secret or stay on the line; did they move you to WhatsApp or video, pay you first, or ask for a small fee by link;
   - whether the senior already paid, gave a code or card details, or installed an app.

   Guardian repeats it back, then answers "likely scam", "not sure, talk to family" or "no scam signs found", and says if the same script was heard recently.
   On "likely scam" it tells the senior not to pay or share anything, says it has alerted the family, and the family member gets a Telegram message and a flashing alert on the family page with who the caller claimed to be, what they wanted, the warning signs, the line and the time.
   If the senior already acted, Guardian says that first: call your bank now on the number on the back of your card, and call ScamShield at 1799. The family alert is marked urgent with what the senior already did.
   When a friend or family member asks for money with no warning signs, Guardian says "not sure" and tells the senior to call that person back on the number they already have.
   The family member then calls the senior back.
2. **Ah Ma Bait.** A scam call reaches the English or the Hindi Bait line. "Mdm Tan" (English) or "Mrs Sharma" (Hindi) plays a confused auntie, stalls, and gets the scammer to say which agency they claim, what they want, and where the money should go. She never gives out an NRIC, OTP, card or account number. Bait is unchanged by this revision; phone calls are a shrinking scam channel (9.7% of contact methods, cases down 49.1%) [verified, SPF mid-year brief 2026], so Bait covers the phone part of the picture only.
3. **Dashboard.** The reviewer sees each call with its language, the scam scripts heard this week grouped by agency and demand, the warning signs Guardian heard, and a draft report per Bait call. Marking a report reviewed records the review; nothing is sent anywhere by the system.

## Success metric

Real-world target [hypothesis]: when a senior who calls Guardian about a scam hears "likely scam", the family is alerted within 1 minute and calls the senior back before any money moves; a senior who already acted is told to call their bank in the same call.
Hackathon measure, on labeled fixtures only, tested by synthetic-caller web calls (scripted caller clips, not live people). Guardian fixtures are written so the senior trusts the caller and never uses scam words such as "safety account":

- Guardian flags at least 7 of 8 sophisticated English scam fixtures as "likely scam" and at most 1 of 4 legit look-alike fixtures.
- Both "already acted" fixtures (one English, one Hindi) get the call-your-bank instruction and an urgent family alert.
- Every "likely scam" verdict in a test call produces a family alert, and no other verdict does.
- Bait captures the planted payee detail in at least 4 of 5 scam fixtures.
- Zero NRIC, OTP, card or account-number leaks by Ah Ma across all test calls.
- Hindi agents run a reduced fixture set, reported separately: Guardian flags at least 2 of 2 scam cases and 0 of 1 legit case; Bait captures the payee in at least 1 of 2 scam cases with zero leaks.

These are fixture results, never performance against real scammers.

## Announcement

Before you move money for anyone, call Ah Ma.
Today's scams don't sound like scams: the caller is polite, knows your details, and passes you to an "officer" who says to keep it quiet.
Scamkaki gives seniors in Singapore a phone line, in English and in Hindi, that asks the questions a careful grandchild would ask, spots the tricks behind polished scams, and alerts family before money moves.
If the money or the code is already gone, Ah Ma tells you to call your bank right away.
Behind it, Ah Ma Bait picks up scam calls herself, plays along, and keeps Guardian's list of phone scripts current.
Every report is a draft that a person checks; nothing is filed automatically.

## Previously approved screens

- [`mockups/dashboard.html`](mockups/dashboard.html): live call feed and "scripts this week".
- [`mockups/report.html`](mockups/report.html): one Bait call's report draft with a "Mark reviewed" action.
- [`mockups/family.html`](mockups/family.html): the family alert page, opened from a secret link the family member bookmarks; shows warning signs and an urgent state when the senior already acted.
- Guardian and Bait are phone-only; no screen.

## S7 visual direction, user-selected 2026-10-28

Claude is to use its relevant design skills for S7, with an appropriate combination of
midnight blue, ice blue, electric blue and chartreuse. Exact shades and proportions are design
choices, not approved measurements. Keep the reviewer workflow. The 2026-10-30 screen amendment below supersedes the original three-screen layout scope.
This direction supersedes the mockups' old color treatment, not their functional content.
Use the palette with readable contrast, clear focus and danger/urgent meaning beyond color alone.
Mockups and visualization files stay plain HTML; this adds no framework or new product feature.

## Out of scope

Hokkien and other dialects; Mandarin until every slice is done (stretch); one agent that switches language mid-call; transferring the senior's call to a family phone (blocked on our Bolna account, see S3 evidence); automatic filing to ScamShield, SPF or banks; Guardian contacting a bank or freezing a card for the senior; checking website addresses or reading screenshots, because a link spoken aloud cannot be checked reliably; business email and invoice scams; blocking or intercepting calls on a senior's phone; real scam-number seeding; multi-family accounts; Singapore number provisioning beyond what Bolna offers.

## Website redesign proposal, 2026-10-30

**Gate 1 amendment, APPROVED 2026-10-30.** User: "Looks good. I approve gate 1." The earlier product goals, languages, verdicts,
fixture labels, private family access and human-only report review remain unchanged.

### Problem and intended result

[verified] The current dashboard puts call controls, a live feed, weekly scripts and a second
call-log table on one page (`src/scamkaki/app/templates/dashboard.html`). The user described
it as one dimensional, basic, wordy and too much like a test website.
[hypothesis] A separate screen for each task, clear navigation and visual explanations will
make the product easier to use. More screens alone do not establish usability.

Design target, not a measured user result: from Overview, reach an urgent Guardian check,
a report draft or a call's details in at most two navigation actions. At phone width, each
call reads as a labeled record without horizontal table scrolling. A future human walkthrough
must establish whether people understand the result and next action without explanation.

### Announcement

Scamkaki puts the next useful action first. See urgent checks on Overview, browse conversations
in Calls, and understand repeated requests in Script patterns. Review a report on its own
screen. Family members get a simpler alert page with the immediate next steps.

### Approved screen direction

One self-contained HTML file per screen, under `mockups/redesign/`:

- [Overview](mockups/redesign/overview.html): urgent check, draft queue, recent activity and a Bait-to-Guardian flow diagram.
- [Calls](mockups/redesign/calls.html): search, line filter, aligned status/duration fields and readable phone records; empty and unavailable states.
- [Call details](mockups/redesign/call-detail.html): call facts, conversation record availability and a record trail; no inferred verdict.
- [Guardian check](mockups/redesign/check.html): claimed agency, request, warning signs, already-acted state and alert progress, with a cause-and-result diagram.
- [Script patterns](mockups/redesign/patterns.html): seven-day Bait counts by agency/request as bars, expandable explanations and the matching flow.
- [Reports](mockups/redesign/reports.html): focused report review, source limitations and explicit confirmation before marking reviewed; sends nothing.
- [Voice room](mockups/redesign/voice.html): choose persona and language away from the call history; clearly disclose microphone and credit use before a real connection.
- [Family alerts](mockups/redesign/family.html): separate private-link experience with urgent guidance, compact reasons and no reviewer navigation.

### Visual direction and limits

Retain the user-selected midnight blue, ice blue, electric blue and chartreuse palette.
Use a midnight navigation rail, light reading areas, clear status labels and restrained icons.
Keep chartreuse for fixture labeling, never for a claim that a call is safe. Move secondary
explanations into details disclosures. Do not remove failed calls or uncertainty to look polished.

[verified] S7 evidence records that Guardian checks cannot reliably be tied to calls. The
approved design keeps them separate. A completed call is not a passed check. Telegram sent is not
confirmed receipt. Script counts are not confirmed scams, unique scammers or success rates.

All sample counts, durations, dates and stories in these mockups are illustrative fixtures,
not extracted results. Missing transcripts are explicitly unavailable; none are fabricated.
Only the first sample call has a detail preview. Reports shows one sample draft, not a built
report-list feature. Review confirmation changes this page only and resets on reload. Voice
controls never request a microphone, mint a session or start a call. Family remains a standalone
preview, outside reviewer navigation. No automatic filing, settings, account management,
identity matching, new voice behavior or real-world effectiveness claim is added.

The old mockups remain historical. Gate 1 approval selects this product direction. Gates 2-4
were drafted together and approved 2026-10-30. They resolve routes, access checks,
data availability, transcript handling, real review persistence and tests before implementation.
