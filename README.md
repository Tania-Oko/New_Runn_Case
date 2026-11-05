# New_Runn_Case
Creates project in Runn based on trigger in Monday Pipeline Board and returns the Runn project ID to the Monday board. Notifies the BUHs, GB and Oko that the new project has been set up in Runn to review.

## Runn project field defaults for initial set-up (from Tania Oko, 5 Nov 2026)

These are starting defaults only. They are reviewed and edited manually in Runn afterwards, so never overwrite fields on an existing Runn project.

Trigger: Monday Pipeline board item with Runn Instruction = "Set up case in Runn" and an empty Runn ID.
If the case already exists in Runn, link its ID instead of creating a duplicate. Once the ID is on the board, set Runn Instruction to "Done".

- Status: Tentative (isConfirmed = false)
- Rate card: by Monday country. US = "USD Standard" (196335); UK = "GBP Standard" (196337)
- Budget method: Phases (PHASE)
- Primary team: Antitrust (109050), also for Consumer Fraud, Discrimination and Environmental, as it is the only team for those BUs
- Project tag: by Monday country (US = 571874, UK = 567524)
- Contracting entity: US = Fideres USA Inc; Spain/Portugal = Iberia; UK = Partners LLP; other EU = Fideres Europe; anything else = Fideres Partners LLP
- Business line: Monday business unit, fuzzy matched (Consumer Fraud = "Consumer" in Runn)
- Project type: Consumer = US CP Report; EU Antitrust = EU Comp Report; first phase of UK antitrust = UK Comp Pre-filing; early-stage US case (not Financial/Securities) = US Comp Pre-filing; US case already Filed (Monday Stage = Filed, not Financial/Securities) = US Comp Expert Report
- Probability: 20 (edited later)
- Billing category: "No LoE - Not Billable Yet" (reviewed later)
- Name format: `Case | Country | Business unit | Year | Lead initials | No LoE`
- After set-up, send the Teams notification described under "Teams notification" below (no email).

Runn API notes: send a custom User-Agent (default Python UA gets 403). Custom fields are applied by PATCH /projects/{id}; the Billing Category field does not accept a change via the API and must be set manually.

## FinSec Pipeline board (Financial and Securities business lines)

Financial and Securities cases are NOT triggered from the main Pipeline board. Use the FinSec Pipeline board (https://fideres-team.monday.com/boards/2691948641/, board id 2691948641) instead. Items on the main Pipeline board with Business unit Financial or Securities are ignored.

Trigger: FinSec Pipeline item with Runn Instruction (color_mm8ty94b) = "Set up case in Runn" and an empty Runn ID (text_mkygq8yb). Once the ID is on the board, set Runn Instruction to "Done". If the case already exists in Runn, link it and do not edit it. The general rules above apply (tentative, PHASE, probability 20, billing category, apply defaults to new projects only), with these FinSec differences:

- Primary team: FinSec (109049)
- Business line: Securities, or Financial when Type = Financial or Securities&Financial (precedent: Dangdang)
- Project type, from the board's Type column: US Sec Class = US Securities Class Action; US Sec Opt-Out = US Securities Opt-Out; Non-US Sec Group = Non-US Securities Group Action; SEC Case = SEC Case; Financial = Financial; Securities&Financial = Securities&Financial. Other Types (Software, Product, SDM, Others, Canada Sec, Valuation, blank): leave blank and flag in the notification.
- Country: board column Country (country_mm8qmdeh). Rate card, tag and contracting entity follow the country rules above.
- Name format: `Case | Country code | Securities or Financial | Year | PM initials | No LoE`, with PM taken from the PM column (e.g. `Manhattan Associates | US | Securities | 2026 | CH | No LoE`).
- Client: from the board's Client dropdown; match an existing Runn client, create one only if none exists.
- Notification goes to the RUNN Finsec chat (chat id 19:171290e9ddfe47e4b0f759504d60249c@thread.v2; members Tania Oko, Alyse Corcoran, Connor Hurley), not the Pipeline-board chat. No test message has been sent there yet.
- Setup done checklist: also tick "Added to Runn" (dropdown_mm8qdb8d) once the ID is on the board. The board's Setup status column belongs to the separate setup-new-finsec-case skill, so do not change it.

## Existing, archived and missing-country rules (both boards)

- An archived Runn project counts as "already exists". Link its ID; never create a new project and never unarchive or edit it. Match on case name (ignoring year, country and initials in the Runn name) and client.
- In the Teams message, flag a linked archived project under "To check": say it is archived in Runn and ask the team to confirm it is the same case (same client, country and matter) and not a new, similar one.
- If the Monday Country is blank, do not guess for a NEW project: skip creating it, leave Runn Instruction as it is, and flag the item in the Teams message ("Country missing on the Monday item, please fill it in and re-trigger"). For a project that already exists in Runn, link it and flag the missing country under "To check".

## FinSec US Securities: phases, milestones and team (NEW projects only)

Applies when a project is created (not linked) from the FinSec Pipeline board and Type = US Sec Class (US Securities Class Action). Never add or change phases, milestones or assignments on an existing Runn project. Starter template: templates/finsec_us_securities_4phase.json (4 phases: Cert., Cert Reply, Merits Opening, Merits Reply, from Runn test project 2398424). Apply with the logic in templates/apply_template.py, but with named people and Monday dates as below. This is still being tested, so keep to what is listed here.

- Dates come from the Monday item: Case Schedule (US date format, e.g. 9/4/26 = 4 Sep 2026), Next Internal Deadline, Next Court Deadline, Project Start Date, Estimated Project End. Add only the phases for which Monday has dates (e.g. Cert. ends on the cert motion date; Cert Reply runs from the opposition date to the reply date). Do not invent dates for the other phases.
- Milestones: add all dated events (start, motion, opposition, reply, internal deadlines and drafts, estimated end). Historic milestones ARE added, as they are useful case history. Estimated end: the Monday Estimated Project End; if blank, about 2 years after the project start.
- Time: never schedule time historically. Assignments start no earlier than the Monday of the current week (the weekly Toggl historical update covers earlier time) and only for phases ending in the future. A phase in the past is created with no assignments.
- Team: replace the template placeholders with the named people from the Monday columns BUH, PM and Consultant(s), keeping the template's hours per day per slot (Executive Director 4, Director 42, Senior Associate and Associate 105 minutes a day). Use each person's default role in Runn and match to the closest template slot (BUH = Executive Director, PM = Director / Senior Associate by their Runn role, consultant = Associate slot, an Analyst is the closest match). If there are fewer people than slots, leave the empty slots out; do not add placeholders.
- The Runn API ignores phase budgets, so budgets cannot be set. State revenue by phase (not per person) in the Teams message, calculated from the resourcing put in for that phase: working days x minutes per day / 60 x the role's standard rate (Runn roles standardRate, e.g. Analyst 375, Associate 550, Director 800, Senior Associate 625, Executive Director 815; the USD Standard rate card may differ, so say it is an estimate). Phases with no resourcing show no revenue.
- Alongside it, show the typical revenue range for the phase, so PMs can course correct (Tania Oko, 5 Nov 2026):
  - Smaller US Securities case: cert opener $60-80k, cert reply $60-80k, merits opening $200-375k, merits reply $200-300k.
  - Larger US Securities case: cert opener $100-150k, class cert reply $150-275k, merits opening $375-500k, merits reply $375-500k.
  - The starter template ($100k / $200k / $200k / $100k of $600k) is more conservative and is fine for now.
  - Choose smaller or larger from the Monday Total Budget (USD) (about $600k-$900k = smaller, above that = larger); if blank, show the smaller range and say the size is unconfirmed. If Total Budget exists, scale the ranges to it rather than using them unscaled.
- Teams message, per such project, add: (1) team members added with their Runn role and hours per day; (2) each phase with its dates, the revenue from the resourcing and the typical range; (3) milestones added with dates; (4) phases left out because Monday had no dates; (5) a note that the PMs should course correct dates and enter the budgets in Runn. Keep the rest of the layout above.

## Teams notification (replaces the email)

Send one Teams message per run (one section per project set up or linked in that run), as HTML via the Teams chat tool. It is sent without a test or confirmation step. Skip it if no project was set up or linked.

- Pipeline board (Antitrust, Consumer Fraud, Discrimination, Environmental, etc.): chat "Chris, Max, Paul, +2", chat id 19:cae01a63d2134538bcd74463de9a6018@thread.v2 (Chris Pike, Max Theiler, Paul Vella, Russell De Souza, Tania Oko).
- FinSec Pipeline board: RUNN Finsec chat (see above).
- Before posting, check the chat's member list still matches. If it does not, do not post; report it instead.
- Message layout: short intro on the first message only if asked; then a heading "N new Runn projects to review (Pipeline board)" and "Current state in Runn as of <date>". For each project: numbered bold title linked to https://app.runn.io/projects/<Runn ID> with "(Runn ID ...)", a line saying whether it was created (with client) or already existed and was linked, then bullets: "Now set: ..." and "To check: ..." (read the CURRENT values back from Runn, do not report what was originally created, as people edit projects afterwards). For a new project with unset fields use "Action needed, still to complete in Runn:" with a nested bullet per field and its suggested value.
- Flags go under "To check" for the project: archived project linked, missing Country, Project Type left blank, PM or initials mismatch.
- Fields the API cannot set (budget method, Contracting Entity, Business Line, Probability, Billing Category, Project Type) are listed for manual completion unless Runn already shows them set. Always check project managers and budget.
- End with: "This is an automated message from the Runn case set-up routine (Claude), sent on behalf of Tania Oko."
- Do not send test messages to the group chats. Use the notes-to-self chat id 48:notes for tests.
