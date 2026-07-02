# RC-06 Claims Production & Submission

Converts finalized clinical/financial data into compliant claims and delivers them to payers,
managing edits, rejections, attachments, corrections, and filing deadlines.

Roles: Biller/Claims Specialist, Claims Edit Analyst, EDI Analyst, Billing Supervisor.
Systems: Patient accounting/billing system (HB/PB), claim scrubber, clearinghouse, payer portals,
DDE/FISS (Medicare), attachment platforms.

---

## 6.1 Claim Generation

### 6.1.1 Bill-hold / suspense management
- **A1.** Apply bill-hold days by patient type (e.g., 3–5 days OP, longer IP) to let charges/coding complete
- **A2.** Monitor DNFB (discharged not final billed) and candidate-for-bill lists daily
- **A3.** Manage hold reasons: coding incomplete (5.1.1), charge review (3.4.1), auth reconciliation
  (1.4.6), COB unresolved (1.3.4), status under review (2.4)
- **D1.** Account clean at bill-hold expiry?
  - ├─ Yes → generate claim (6.1.2)
  - ├─ No, fixable → route to owning queue with aging escalation
  - └─ No, blocked long-term → escalate via DNFB huddle; leadership decision (bill partial, hold, or resolve)

### 6.1.2 Claim assembly
- **A1.** Compile claim dataset: patient/subscriber, payer, provider (billing/rendering/attending NPIs,
  taxonomy), diagnoses, procedures/charges, occurrence/value/condition codes, admission data
- **A2.** Generate 837I (institutional/UB-04) or 837P (professional/CMS-1500) per payer setup
- **A3.** Apply payer-specific formatting rules (loops/segments, local requirements)
- **A4.** Attach claim-level identifiers: patient control number, medical record number, auth number
- **D1.** Which claim form/route applies?
  - Inputs: provider type, service type, payer requirements
  - ├─ Institutional → 837I
  - ├─ Professional → 837P
  - ├─ Both (hospital + profee) → parallel claims with consistent data
  - └─ Non-standard payer (some WC/liability) → payer-specific form/paper (6.3.4)

### 6.1.3 Claim splitting/combining rules
- **A1.** Apply 72-hour/3-day window rule (bundle related outpatient into IP claim)
- **A2.** Generate interim claims for long stays per payer rules (bill types 112/113/114)
- **A3.** Split recurring/series accounts into billing cycles (monthly series claims)
- **A4.** Handle benefit-period and payer-change mid-stay splits
- **D1.** Outpatient service within payment window of related inpatient admission?
  - ├─ Yes, related/same entity rules met → combine into IP claim; cancel separate OP claim
  - └─ No → bill separately with appropriate condition code if needed

## 6.2 Claim Editing & Scrubbing

### 6.2.1 System edits (billing system)
- **A1.** Run HIS/PB edits: required-field, code-validity, financial class/payer consistency, bridge
  routines
- **A2.** Auto-fix rule-safe defects (formatting, known mappings); queue the rest

### 6.2.2 Scrubber/clearinghouse edits
- **A1.** Run national edit sets: NCCI PTP pairs, MUE units, OCE/IOCE, medical necessity (NCD/LCD), CCI modifiers
- **A2.** Run payer-specific custom edits (documented payer bulletins → edit rules)
- **A3.** Classify edit failures by owner (coding, registration, charging, billing)
- **D1.** Edit failure category?
  - ├─ Registration/eligibility → patient access correction queue → re-edit
  - ├─ Coding (NCCI, dx) → coding queue (5.8) → re-edit
  - ├─ Charge issue → revenue integrity queue (3.4.1)
  - ├─ Billing-fixable (modifier per policy, format) → biller corrects with compliance guardrails
  - └─ Conflicting/invalid edit → edit-rule review (6.2.4)

### 6.2.3 Edit resolution workflow
- **A1.** Work edit queues by dollar/age priority to SLA
- **A2.** Document resolution action; re-scrub until clean
- **A3.** Track repeat-edit patterns {feeds-back-to 6.2.4 and upstream owners}

### 6.2.4 Edit rule maintenance
- **A1.** Add/modify custom edits from denial root causes (turn recurring denial into pre-bill stop)
- **A2.** Retire/refine false-positive edits (measure edit hit → change rate)
- **A3.** Version and test edit changes before production

## 6.3 Claim Submission & Acknowledgment

### 6.3.1 Electronic submission & batching
- **A1.** Batch and transmit 837s to clearinghouse/direct payers on schedule
- **A2.** Verify batch counts/dollars transmitted vs generated (no dropped claims)
- **A3.** Log submission timestamps (timely filing evidence)

### 6.3.2 Acknowledgment processing
- **A1.** Process 999 (syntax accept/reject) per batch; re-transmit rejected batches after repair
- **A2.** Process 277CA claim-level acknowledgments; post accept/reject status to each account
- **A3.** Reconcile: every submitted claim must reach payer-accepted status (submission integrity loop)
- **D1.** Claim missing acknowledgment after N days?
  - ├─ Yes → trace with clearinghouse/payer; resubmit if never received
  - └─ No → follow-up clock starts (9.2)

### 6.3.3 Rejection management (front-end rejects)
- **A1.** Work clearinghouse/payer rejection queues daily (these never entered adjudication —
  invisible to denial reports if unmanaged)
- **A2.** Correct and resubmit; track rejection reasons to prevention {feeds-back-to 6.2.4}
- **D1.** Rejection reason?
  - ├─ Member/eligibility mismatch → verify coverage (1.3) → correct → resubmit
  - ├─ Provider enrollment/NPI issue → enrollment team (11.5) → hold claims for that payer/provider
  - ├─ Format/payer rule → fix mapping/edit; resubmit
  - └─ Duplicate → confirm original status; do not resubmit blindly

### 6.3.4 Paper claim production
- **A1.** Print UB-04/CMS-1500 for paper-only payers; include required attachments
- **A2.** Log mail date; use certified/trackable mail for high-dollar or deadline-critical claims

### 6.3.5 Claim attachments
- **A1.** Identify attachment-required claims (payer rules: op notes, invoices, EOBs, consent forms)
- **A2.** Submit via 275/portal/fax with control numbers linking to claim
- **A3.** Track attachment receipt; respond to solicited documentation requests (277 RFI) by deadline
- **D1.** Additional documentation request (ADR) received?
  - ├─ Respond within deadline → track adjudication
  - └─ Missed deadline risk → escalate; late response denial requires appeal (8.4.4)

## 6.4 Secondary, Tertiary & Special Claims

### 6.4.1 COB claim generation
- **A1.** Generate secondary claim carrying primary payer adjudication (paid amount, adjustments,
  CARC detail) in required loops or with EOB attachment
- **A2.** Validate balance math: primary payment + adjustments + patient liability = billed
- **D1.** Did primary adjudicate correctly before secondary billing?
  - ├─ Yes → submit secondary
  - ├─ No (primary error) → resolve primary first (8.x/9.4); hold secondary
  - └─ Primary paid as secondary in error → COB correction with both payers (1.3.4 pattern)

### 6.4.2 Medicare crossover management
- **A1.** Confirm crossover indicator on Medicare remittance (claim forwarded to Medigap/secondary)
- **A2.** Suppress duplicate secondary billing when crossover confirmed; bill directly when not

### 6.4.3 WC / auto / liability claim packaging
- **A1.** Bill carrier per jurisdiction rules (state WC fee schedules, required forms, attachments)
- **A2.** Include claim number/adjuster; coordinate with employer authorization
- **A3.** Track jurisdiction-specific dispute processes; file liens where applicable (9.8)

## 6.5 Corrected, Late & Void Claims

### 6.5.1 Corrected/replacement claim processing
- **A1.** Generate frequency-7 replacement referencing original claim number (ICN/DCN)
- **A2.** Document correction reason; ensure replacement supersedes cleanly (avoid duplicate denials)
- **D1.** Payer supports electronic corrected claims?
  - ├─ Yes → submit 7-frequency electronically
  - └─ No → payer-specific correction form/portal/paper process

### 6.5.2 Void/cancel processing
- **A1.** Submit frequency-8 void when claim billed in error (wrong payer/patient/provider)
- **A2.** Confirm void processed and money recouped/returned properly before rebilling correctly

### 6.5.3 Timely filing management
- **A1.** Maintain filing-limit matrix by payer/contract (initial, corrected, secondary, appeal limits)
- **A2.** Run at-risk aging alarms (e.g., 75% of limit consumed and unbilled/unresolved)
- **A3.** Preserve proof-of-timely-filing artifacts (277CA, submission logs)
- **D1.** Claim approaching filing limit unresolved?
  - ├─ Billable now → force priority release/submission
  - ├─ Blocked (e.g., COB pending) → file protective claim per payer guidance; document
  - └─ Limit passed → timely-filing appeal with proof (8.4.4) or write-off with root cause (8.6)

**Failure modes:** dropped claims (batch loss), unworked rejections, missing acknowledgments,
duplicate claims, filing-limit write-offs, attachment deadline misses.
**Metrics:** clean claim rate, first-pass yield, edit rework rate, days from discharge/service to
bill (claim lag), rejection rate, timely-filing write-offs.

## Relationships
- 6.1.1 `consumes` outputs of RC-03/04/05; DNFB is the shared inventory metric
- 6.3.2 `produces` filing-proof artifacts `consumed-by` 8.4.4
- 6.3.3/6.2.x `feed-back-to` upstream defect owners (8.5 taxonomy shared)
- 6.5.3 `gates` all resolution paths (every downstream fix must respect filing/appeal clocks)
