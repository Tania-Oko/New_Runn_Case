# New_Runn_Case
Creates project in Runn based on trigger in Monday Pipeline Board and returns the Runn project ID to the Monday board. Notifies the BUHs, GB and Oko that the new project has been set up in Runn to review.

## Runn project field rules (from Tania Oko, 5 Nov 2026)

Trigger: Monday Pipeline board item with Runn Instruction = "Set up case in Runn" and an empty Runn ID.
If the case already exists in Runn, link its ID instead of creating a duplicate. Once the ID is on the board, set Runn Instruction to "Done".

- Status: Tentative (isConfirmed = false)
- Rate card: by Monday country. US = "USD Standard" (196335); UK = "GBP Standard" (196337)
- Budget method: Phases (PHASE)
- Primary team: Antitrust (109050), also for Consumer Fraud, Discrimination and Environmental, as it is the only team for those BUs
- Project tag: by Monday country (US = 571874, UK = 567524)
- Contracting entity: US = Fideres USA Inc; Spain/Portugal = Iberia; UK = Partners LLP; other EU = Fideres Europe; anything else = Fideres Partners LLP
- Business line: Monday business unit, fuzzy matched (Consumer Fraud = "Consumer" in Runn)
- Project type: Consumer = US CP Report; EU Antitrust = EU Comp Report; first phase of UK antitrust = UK Comp Pre-filing; early-stage US case (not Financial/Securities) = US Comp Pre-filing
- Probability: 20 (edited later)
- Billing category: "No LoE - Not Billable Yet" (reviewed later)
- Name format: `Case | Country | Business unit | Year | Lead initials | No LoE`
- After set-up, for Antitrust, Consumer Fraud, Discrimination or Environmental cases, email Chris Pike and Tania Oko (Outlook) with the Runn fields.

Runn API notes: send a custom User-Agent (default Python UA gets 403). Custom fields are applied by PATCH /projects/{id}; the Billing Category field does not accept a change via the API and must be set manually.
