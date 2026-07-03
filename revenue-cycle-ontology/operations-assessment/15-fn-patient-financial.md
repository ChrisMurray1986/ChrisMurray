# Function Assessment — RC-10 Patient Financial Services

Roles: ROLE-PFSREP, ROLE-FACOUNS, ROLE-AGCYLIAISON, ROLE-FINCOUNS.

### 10.1 Statements & Communication — ROLE-PFSREP

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-10.1-01 | Statements fire on cycle regardless of payer-work state (10.1.D1) → FM-PATIENTWRONGBILL | Patients billed for balances under active appeal/COB work; complaint themes match | PBP-10.1-01 Statement-qualification gate: no dunning while a payer defect is open; hardened-by UC-10-01 |
| PFM-10.1-02 | Returned mail piles unworked; address hygiene absent (10.1.A3) | Statement cost with zero-response segments; skip-trace never run | PBP-10.1-02 Returned-mail → hygiene → channel-switch pipeline with measured recovery; hardened-by UC-10-02 |
| PFM-10.1-03 | 501(r) FA notice content drifts across statement versions (10.1.A4) | Template edits bypass compliance review | PBP-10.1-03 Regulatory content blocks locked (GOV-13's manual form); version control on templates |

### 10.2 Customer Service & Disputes — ROLE-PFSREP

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-10.2-01 | Reps can't see the whole account (HB/PB split) — answers guessed, calls repeat (10.2.A1–A2) | "Let me transfer you"; contradictory answers on the same balance | PBP-10.2-01 Unified account view at the desktop (BP-ET-05); answer accuracy sampled in QA; hardened-by UC-10-03 |
| PFM-10.2-02 | Disputes handled as complaints, not investigations (10.2.D1); itemized-bill requests slow | Dispute outcomes unrecorded; same dispute re-raised | PBP-10.2-02 Dispute protocol with investigation standard, resolution codes, and root-cause feed to 8.5 |
| PFM-10.2-03 | Improvised discounts/plans per rep sympathy (10.2.A4) — policy variance at the phone | Plan terms differ by rep; discount authority informal | PBP-10.2-03 Policy matrix enforced in tooling; empathy through options offered, not invented |

### 10.3 Payment Plans & Financing — ROLE-PFSREP

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-10.3-01 | Plans set to whatever the patient proposes; default handling passive (10.3.A1–A3) | Plan default >40%; broken plans quietly restart | PBP-10.3-01 Plan matrix (term × balance) with affordability check; default rescue protocol; hardened-by UC-10-04 |

### 10.4 Financial Assistance / Charity (501(r)) — ROLE-FACOUNS

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-10.4-01 | FA reached only by those who ask and persist; application friction high (10.4.A1–A3) → FM-FA-MISS | FA volume low vs demographics; applications abandoned mid-way | PBP-10.4-01 Proactive screening at counseling/statement/pre-placement; application assistance; hardened-by UC-10-05 |
| PFM-10.4-02 | Presumptive charity absent; bad debt carries charity-eligible accounts (10.4.A4) | Agency returns accounts as "clearly indigent"; community-benefit understated | PBP-10.4-02 Presumptive-approval scoring pre-placement (approval only — never presumptive denial) |
| PFM-10.4-03 | ECA timing rules (501(r)) tracked informally (10.4.A5) | Collections started inside notice windows on sampled accounts | PBP-10.4-03 ECA-clock automation on every account path |

### 10.5 Self-Pay Segmentation & Early-Out — ROLE-AGCYLIAISON

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-10.5-01 | One treatment path for all self-pay (10.5.A1) — same cadence for $80 and $8,000, for able and unable | Uniform statement cycles; propensity unused | PBP-10.5-01 Segmented pathways (balance × propensity × FA-likelihood) with distinct treatments |
| PFM-10.5-02 | Early-out vendor works unmonitored; conduct QA absent (10.5.A3–A4) | Vendor scripts never reviewed; complaints reach the CFO cold | PBP-10.5-02 Vendor QA sampling + complaint-theme review under BP-VN-03 data rights; hardened-by UC-10-07 |

### 10.6 Bad Debt & Agency Management — ROLE-AGCYLIAISON

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-10.6-01 | Placements untracked post-transfer; recalls and adjustments drift (10.6.A2, A5) | Agency inventory ≠ hospital records; dual collection incidents | PBP-10.6-01 Placement reconciliation monthly; recall triggers automated (FA found, dispute, bankruptcy) |
| PFM-10.6-02 | Net-back never computed; commissions accepted as quoted (10.6.A3–A4) | Agency compared on fee %, not net recovery; no champion/challenger | PBP-10.6-02 Net-back scorecards with challenger splits; hardened-by UC-14-07 |

### 10.7 No Surprises Act Protections — ROLE-PFSREP

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-10.7-01 | NSA-protected scenarios billed as ordinary OON (10.7.A1–A2) → FM-PATIENTWRONGBILL, penalties | OON ED balances at full liability; consent artifacts unfindable | PBP-10.7-01 Protection screen before any OON patient billing; err-protective default; hardened-by UC-10-06 |
| PFM-10.7-02 | GFE-vs-final never compared; SDR disputes land unprepared (10.7.A4) | $400-threshold breaches unnoticed until dispute notice | PBP-10.7-02 Variance monitor with proactive outreach; hardened-by UC-10-08 |
