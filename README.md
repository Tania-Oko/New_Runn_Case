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
- After set-up, for Antitrust, Consumer Fraud, Discrimination or Environmental cases, email Chris Pike and Tania Oko (Outlook) with the Runn fields.

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
- Notify the BUH column people (Per Axelson / Robert Chang) and Tania Oko with the Runn fields instead of Chris Pike.
- Setup done checklist: also tick "Added to Runn" (dropdown_mm8qdb8d) once the ID is on the board. The board's Setup status column belongs to the separate setup-new-finsec-case skill, so do not change it.
