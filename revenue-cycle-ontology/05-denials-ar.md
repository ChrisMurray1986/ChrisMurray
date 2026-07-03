# RC-08 Denials Management & Appeals / RC-09 AR Management & Follow-Up

RC-08 recovers and prevents payer denials. RC-09 manages the total receivable inventory —
status determination, no-response follow-up, underpayments, credits, and aged-account
disposition. They share work-queue infrastructure and the defect taxonomy.

Roles: Denials Analyst, Appeals Nurse/Clinician, Appeals Writer, AR Follow-Up Rep, Underpayment
Analyst, Credit Balance Analyst, Denial Prevention Manager. Systems: denial workflow platform,
work-queue engine, payer portals, 276/277, contract engine, appeal letter library.

---

# RC-08 Denials Management & Appeals

## 8.1 Denial Identification & Classification
- **A1.** Ingest denials from every channel: 835 CARC/RARC (incl. zero-pay and line-level partial
  denials), paper EOBs, payer letters, portal messages, take-backs (7.4.3)
- **A2.** Classify each denial into internal taxonomy: category (eligibility, auth, medical
  necessity, coding, timely filing, COB, duplicate, request-for-information, contractual dispute),
  clinical vs technical/administrative, line vs claim level, hard (unrecoverable-if-final) vs soft
  (correctable)
- **A3.** Attribute preliminary root-cause owner (access, UR, coding, billing, payer behavior)
- **A4.** Stamp appeal deadline from payer/contract matrix at intake (clock discipline)
- **D1.** Is this a true denial vs an RFI/development request?
  - ├─ RFI/ADR → documentation response workflow (6.3.5) — respond, don't appeal
  - └─ True denial → triage (8.2)

## 8.2 Denial Triage & Routing
- **A1.** Score denials: recoverable value × overturn probability × deadline urgency
- **A2.** Route by skill: clinical denials → nurse/clinician queues; coding → coding (5.8);
  technical → billing/access queues
- **A3.** Batch systemic denials (same payer/reason/date-range) for project-level handling
- **D1.** Disposition path?
  - Inputs: denial category, correctability, value, deadline
  - ├─ Correctable defect → fix-and-rebill path (8.3)
  - ├─ Payer error, claim correct → reconsideration/appeal path (8.4)
  - ├─ Wrong payer billed → redirect billing (COB fix → bill correct payer; watch both filing clocks)
  - ├─ Patient responsibility per benefits → transfer to patient liability with clear coding (10.1)
  - └─ Not recoverable/not worth pursuit → write-off governance (8.6)

## 8.3 Denial Resolution — Non-Appeal Paths
- **A1.** Correct defect (registration field, code, modifier, auth number, COB order) with the owning team
- **A2.** Rebill or submit corrected claim (6.5.1) referencing original
- **A3.** For retro-actionable items: retro authorization request, retro eligibility (Medicaid) attachment
- **A4.** Verify resolution: track corrected claim to payment (do not close at resubmission)
- **D1.** Corrected claim denies again?
  - ├─ Same reason → escalate to appeal or payer rep (11.6); stop rebill loops
  - └─ New reason → classify new denial (8.1); investigate compound defect

## 8.4 Appeals Management

### 8.4.1 Appeal decision & prioritization
- **A1.** Evaluate merit: policy citations, clinical evidence, contract terms vs denial rationale
- **A2.** Estimate expected value (balance × overturn likelihood) vs appeal cost; apply thresholds
- **D1.** Pursue appeal?
  - ├─ Strong merit → full appeal (8.4.2+)
  - ├─ Marginal, high dollar → obtain records review/external clinical opinion first
  - ├─ Weak merit → write-off with root cause (8.6) — feed prevention
  - └─ Systemic payer behavior → also escalate to payer relations/JOC (11.6) and track dollars

### 8.4.2 Appeal letter/packet construction
- **A1.** Draft argument citing: payer's own medical policy, contract clauses, regulatory
  requirements, clinical facts with record pinpoints
- **A2.** Assemble packet: appeal letter, claim, remit, records excerpts, auth proof, filing proof,
  policy excerpts
- **A3.** Submit via required channel (portal upload, certified mail, fax); log submission + deadline met
- **A4.** Calendar payer response SLA; auto-follow-up at expiry

### 8.4.3 Clinical appeals
- **A1.** Medical necessity/level-of-care: nurse/physician-advisor authored argument mapped to
  criteria (MCG/InterQual) and clinical course
- **A2.** DRG downgrade/clinical validation: defend coded diagnoses with clinical indicators,
  coding guidelines (Coding Clinic), and documentation
- **A3.** Readmission/never-event denials: contract definition analysis and case-specific defense
- **D1.** Payer used correct criteria set (per contract/regulation, e.g., MA two-midnight parity)?
  - ├─ No → procedural argument: wrong standard applied — often the strongest appeal ground
  - └─ Yes → argue within the criteria on clinical facts

### 8.4.4 Administrative/technical appeals
- **A1.** Timely filing: submit proof (277CA acceptance, submission logs, mail receipts)
- **A2.** No-auth: submit "no auth required" evidence (1.4.1.A3), retro-auth grants, or emergent
  exception arguments
- **A3.** Eligibility/COB: submit verification records and payer-of-record evidence
- **A4.** Bundling/edit disputes: cite NCCI/CPT guidance and payer edit policy

### 8.4.5 Appeal levels & escalation
- **A1.** Track appeal level per payer scheme: reconsideration → level 1 → level 2 → external review
- **A2.** Medicare path: redetermination (MAC) → reconsideration (QIC) → ALJ hearing → Medicare
  Appeals Council → federal court; manage AIC thresholds and timelines
- **A3.** MA/commercial: internal appeals → independent external review (state/federal); expedited
  paths where health-endangering
- **A4.** Marketplace/ERISA nuances: exhaust plan remedies; document for potential litigation referral
- **A5.** NSA out-of-network payment disputes: open negotiation window → federal IDR arbitration
  (offer strategy, batching rules, fee management)
- **D1.** Level-N appeal upheld — escalate?
  - Inputs: remaining levels, value, precedent value, cost
  - ├─ Escalate → next level with strengthened evidence
  - ├─ Aggregate → hold for batch escalation/legal or JOC leverage (11.6)
  - └─ Exhaust/stop → final write-off with taxonomy (8.6)

### 8.4.6 Appeal outcome processing
- **A1.** Post overturn payments; verify payment matches overturn decision (payers underpay wins)
- **A2.** Record outcome (overturned/partial/upheld) against denial record for analytics
- **A3.** Release related held balances (patient portion after payer resolution)

## 8.5 Denial Prevention Program
- **A1.** Maintain root-cause taxonomy shared across access/mid-cycle/back-end
- **A2.** Run weekly denial-trend review: new codes, payer spikes, top defect owners
- **A3.** Commission prevention actions: new pre-bill edits (6.2.4), registration QA targets (1.9.5),
  auth grid updates (1.4.1), CDI/coding education (4.5/5.7), payer escalations (11.6)
- **A4.** Measure prevention: initial denial rate trend by category — close the loop on each action
- **A5.** Quantify total denial economics: initial denied dollars, overturn recovery, final write-offs,
  cost-to-collect on appeals

## 8.6 Write-Off Governance & Adjustment Approval
- **A1.** Enforce write-off reason taxonomy (every avoidable write-off has an owner + root cause)
- **A2.** Apply approval matrix by dollar threshold (rep → supervisor → manager → director → CFO)
- **A3.** Review write-off trends monthly; audit for miscoded adjustments (7.4.1.A3)
- **D1.** Write-off request valid?
  - ├─ Appropriate (true contractual, exhausted, uncollectible) → approve at proper level
  - ├─ Premature (recovery paths remain) → reject; route back with direction
  - └─ Pattern detected → escalate systemic fix, not just this account

**Metrics:** initial denial rate (% claims, % dollars), denial overturn rate, appeal success by
level/category, denial write-off %, appeal turnaround, preventable-denial dollars by owner.

---

# RC-09 AR Management & Follow-Up

## 9.1 Work Prioritization & Inventory Management
- **A1.** Segment AR inventory: payer/financial class, age, balance band, claim status, next-action type
- **A2.** Score and rank accounts (expected collectible value × urgency (filing/appeal clocks) ×
  actionability); feed prioritized queues
- **A3.** Set follow-up cadence rules by payer (first touch at expected-adjudication + grace; then cycle)
- **A4.** Manage inventory hygiene: no-touch aging alarms, duplicate-work suppression, closed-loop
  next-action stamping on every touch
- **D1.** Account worked N times without progress?
  - ├─ Yes → break-the-pattern review: escalate channel (rep call → provider rep → JOC), reassign, or disposition decision
  - └─ No → continue cadence

## 9.2 Claim Status Determination
- **A1.** Run automated status sweeps: 276/277 batches, portal-scraping bots, IVR bots
- **A2.** Map status responses to actions (in-process → recheck date; finalized-paid → trace remit;
  finalized-denied → 8.1; pended-RFI → 6.3.5; no claim on file → 6.3.3 trace)
- **A3.** Call payer for statuses automation can't resolve; document call reference/rep/quote
- **D1.** Status response?
  - ├─ Paid, no remit posted → remittance trace (7.3.1)
  - ├─ Denied, not in denial system → intake to 8.1 (channel gap — fix feed)
  - ├─ Pended → supply requested item; set recheck
  - ├─ No claim on file → confirm submission proof; resubmit; check EDI route (14.3)
  - └─ In process within norm → set recheck at payer-average adjudication time

## 9.3 No-Response / Unadjudicated Claim Follow-Up
- **A1.** Detect claims past expected adjudication with no 835/277 activity
- **A2.** Execute escalation ladder: resubmit → provider rep inquiry → prompt-pay complaint
- **A3.** Apply state prompt-pay statutes/contract late-payment interest; bill interest where applicable
- **D1.** Payer systematically slow on a claim population?
  - ├─ Yes → project-level escalation with claim inventory list (11.6); consider regulatory complaint
  - └─ No → account-level handling

## 9.4 Underpayment Recovery
- **A1.** Work variance queue from 7.4.2: validate expected-pay calc against contract terms manually
- **A2.** Classify variance cause: payer misapplication (fee schedule, DRG weight, outlier, carve-out,
  lesser-of logic), contract-load error, stacked-discount/silent-PPO issue
- **A3.** Demand corrected payment with calculation exhibit; track as payer project when systemic
- **A4.** Escalate unresolved underpayments to dispute/appeal or contract remedy (11.6)
- **A5.** Reconcile recovered dollars; report net realization impact
- **D1.** Variance cause?
  - ├─ Contract-load error → fix engine (11.2); recalc population; no payer demand
  - ├─ Payer error, isolated → per-claim demand
  - └─ Payer error, systemic → batch demand + JOC + interest claim

## 9.5 Credit Balance & Refund Management
- **A1.** Work credit balance inventory daily; classify cause (duplicate payment, over-posting, both
  payers paid primary, POS overcollection, adjustment error)
- **A2.** Validate true credit vs posting error (many credits are misposts — correct, don't refund)
- **A3.** Process payer refunds/retractions per payer process; Medicare credit balance reporting (CMS-838 quarterly)
- **A4.** Process patient refunds with approval controls and fraud checks
- **A5.** Escheat unclaimable refunds per state unclaimed-property law
- **D1.** Credit involves government payer overpayment?
  - ├─ Yes → 60-day rule clock (12.4): quantify, refund, document — compliance priority
  - └─ No → standard refund workflow
- **D2.** Patient refund undeliverable?
  - ├─ Locate via skip trace → reissue
  - └─ Exhausted → escheatment pipeline with dormancy tracking

## 9.6 Small Balance & Administrative Resolution
- **A1.** Auto-adjust balances under de-minimis threshold with dedicated reason codes
- **A2.** Balance-forward small residuals to next statement where policy allows
- **A3.** Review small-balance write-off aggregate for hidden systemic defects

## 9.7 Aged AR, Reserves & Bad Debt Transfer
- **A1.** Run aged trial balance reviews (90/180/360 buckets) with disposition decisions per account cohort
- **A2.** Support reserve estimation: historical realization by payer/age cohort {feeds: 13.3}
- **A3.** Execute bad-debt transfer criteria (statement cycle complete, FA screening done, no active
  dispute) {gates: 10.6}
- **A4.** Run legacy/conversion AR wind-down projects (system migrations) with dedicated inventory control

## 9.8 Special Account Resolution
- **A1. WC/liability:** manage lien filings/perfection deadlines, settlement negotiations,
  attorney communication, letters of protection
- **A2. Bankruptcy:** stop collection on notice (automatic stay), file proof of claim, classify
  pre/post-petition balances, track discharge outcomes
- **A3. Deceased/estate:** probate claim filing deadlines, estate representative billing, survivor
  liability rules by state
- **A4. Hospice/VA/IHS interactions:** payer-of-record rules for overlapping benefits
- **A5. Interfacility/transplant/global arrangements:** bill per case-rate agreement terms

**Metrics:** days in AR (net/gross), AR > 90 days %, cash collections vs goal/expected, follow-up
touch productivity & yield, underpayment recovery $, credit balance days-to-resolve, bad debt %.

## Relationships
- 7.1.2/7.4.3 `trigger` 8.1; 7.4.2 `triggers` 9.4; 8.3/8.4 outcomes `feed` 8.5 taxonomy
- 8.5 `feeds-back-to` 1.x, 2.x, 5.x, 6.2.4 (prevention loop — the defining cross-domain circuit)
- 9.7 `gates` 10.6 (no bad-debt placement before required patient-cycle completion)
- 8.6 approval matrix `governs` adjustment transactions in 7.4.1
