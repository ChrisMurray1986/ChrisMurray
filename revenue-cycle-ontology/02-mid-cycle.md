# RC-02–RC-05 Mid-Cycle Operations

Mid-cycle converts clinical activity into complete, compliant, billable data: correct patient
status (RC-02), complete charges (RC-03), documentation that supports acuity and necessity
(RC-04), and accurate codes (RC-05).

---

# RC-02 Utilization Review & Case Management

Roles: UR Nurse, Case Manager, Physician Advisor, UM Director. Systems: UR criteria platforms
(MCG/InterQual), EHR case management module, payer portals/fax.

## 2.1 Admission Status Determination

### 2.1.1 Initial status review
- **A1.** Review admission order and clinicals within first hours of arrival/decision-to-admit
- **A2.** Apply screening criteria (MCG/InterQual) for inpatient vs observation vs outpatient
- **A3.** Validate order says what the clinical picture supports (order-status congruence)
- **D1.** Does clinical picture support the ordered status?
  - Inputs: severity of illness, intensity of service, expected duration, criteria result
  - ├─ Supports IP → confirm inpatient; document criteria met
  - ├─ Supports OBS only → recommend observation to attending; obtain corrected order
  - ├─ Ambiguous → physician advisor review (2.1.4)
  - └─ Neither (outpatient appropriate) → recommend OP with service orders

### 2.1.2 Two-midnight / criteria application (Medicare & MA nuances)
- **A1.** Assess reasonable expectation of ≥2-midnight stay at admission for Medicare
- **A2.** Document expectation basis; track actuals vs expectation
- **A3.** Apply inpatient-only list check for surgical cases
- **D1.** Procedure on inpatient-only list?
  - ├─ Yes → inpatient status required regardless of duration
  - └─ No → two-midnight/criteria analysis applies

### 2.1.3 Condition Code 44 / self-denial process
- **A1.** When IP status found unsupported *before discharge*: convene UR committee review (physician
  member concurrence), notify attending, obtain change order, notify patient in writing → bill OP with CC44
- **A2.** When found *after discharge* (Medicare): execute self-denial/rebill (Part A no-pay, rebill
  Part B) within rules
- **D1.** Was the patient discharged before status correction?
  - ├─ No → CC44 pathway
  - └─ Yes → self-denial/121-day Part B rebill pathway

### 2.1.4 Physician advisor review
- **A1.** Refer ambiguous/failed-criteria cases with clinical summary
- **A2.** Physician advisor renders status recommendation with documented rationale
- **A3.** Communicate to attending; reconcile disagreements via UM committee escalation

## 2.2 Concurrent Review & Payer Notification

### 2.2.1 Admission notification to payer
- **A1.** Notify payer of admission within contract window (often 24–48h) via portal/278N/fax/phone
- **A2.** Record notification reference; calendar clinical-review due dates
- **D1.** Notification made timely?
  - ├─ Yes → proceed
  - └─ No → document cause; prepare late-notification appeal defense; escalate process gap {feeds-back-to 8.5}

### 2.2.2 Concurrent clinical reviews to payer
- **A1.** Submit clinical reviews at payer-required cadence with criteria-mapped documentation
- **A2.** Track payer determinations by review; log approved days/levels
- **A3.** Respond to payer requests for additional information within deadlines

### 2.2.3 Continued-stay authorization management
- **A1.** Monitor authorized-days runway vs expected LOS; request extensions before expiry
- **A2.** Reconcile approved level of care vs actual (ICU vs floor) and resolve gaps
- **D1.** Payer denies continued stay concurrently?
  - ├─ Peer-to-peer available → schedule immediately (2.2.4)
  - ├─ Discharge clinically appropriate → coordinate discharge; end authorization exposure
  - └─ Patient not dischargeable, denial stands → document; case builds to retrospective appeal (8.4.3)

### 2.2.4 Concurrent denial & peer-to-peer management
- **A1.** Prepare attending/physician advisor with denial rationale and criteria gaps
- **A2.** Conduct P2P within payer window; document outcome and reviewer name
- **A3.** Record overturns with new approved days; log upheld denials for retro appeal

## 2.3 Discharge & Level-of-Care Transitions
- **A1.** Track avoidable days with reason taxonomy (payer delay, placement, internal delay) {measured-by KPI}
- **A2.** Coordinate post-acute authorizations (SNF, IRF, LTACH, home health) before transfer
- **A3.** Issue discharge appeal rights notices (IMM second copy; expedited QIO appeal handling)
- **D1.** Patient appeals discharge to QIO?
  - ├─ Yes → continue stay pending QIO decision per rules; submit records to QIO
  - └─ No → discharge per plan

## 2.4 Retrospective Utilization Review
- **A1.** Review unbilled/held accounts for status defensibility before claim release
- **A2.** Support retrospective authorization requests where payer allows
- **A3.** Feed status-related denial patterns to admission-point education {feeds-back-to 2.1}

**Metrics:** observation rate, status-change rate, concurrent denial overturn rate, avoidable days,
authorized-vs-billed day variance.

---

# RC-03 Charge Capture & Revenue Integrity

Roles: Department charge owners, Charge Capture Analyst, Revenue Integrity Analyst, CDM Analyst.
Systems: EHR charge router, CDM, charge edit engines, pharmacy/OR/ED systems.

## 3.1 Charge Generation & Entry

### 3.1.1 Order/documentation-driven automated charging
- **A1.** Fire charges from order completion, medication administration (eMAR), documentation triggers
- **A2.** Maintain charge trigger rules mapped to CDM items
- **A3.** Monitor interface queues for dropped/suspended charges; repair and repost
- **D1.** Charge trigger fired without matching CDM item (orphan)?
  - ├─ Yes → route to CDM work queue (3.3.1); hold charge
  - └─ No → post charge

### 3.1.2 Manual charge entry
- **A1.** Enter charges from department documentation with service date, quantity, modifiers
- **A2.** Apply department-specific capture rules (units by time, supplies chargeability)
- **A3.** Reconcile entered charges to source logs (3.2.1)

### 3.1.3 Departmental charge capture (high-complexity areas)
- **A1. OR:** capture case time levels, implants (with invoice cost linkage), supplies, anesthesia time units
- **A2. ED:** assign facility E/M level via acuity criteria; capture procedures, infusions/injections hierarchy
- **A3. Pharmacy:** charge on administration; maintain NDC-to-HCPCS crosswalk, billable units conversion (critical: unit-conversion errors are a top overpayment/audit driver); handle waste billing (JW/JZ modifiers)
- **A4. Infusion/oncology:** apply initial/sequential/concurrent hierarchy, time documentation, drug units
- **A5. Cath/IR/Endo:** capture device-intensive procedure charges; device credit handling (condition codes FB/FC-era → value code FD reporting for replaced devices)
- **D1.** Implant/high-cost device used?
  - ├─ Yes → verify device charge + invoice linkage + warranty/credit status → apply device credit reporting if credited
  - └─ No → standard capture

### 3.1.4 Professional charge capture
- **A1.** Capture profee charges via EHR encounter close, mobile charge capture, or coder abstraction
- **A2.** Reconcile provider schedules/census to submitted charges (missing-encounter report)
- **A3.** Route unsigned/uncoded encounters to providers with aging escalation
- **D1.** Encounter closed without charge after N days?
  - ├─ Yes → escalate to provider/department chair; track to resolution
  - └─ No → normal flow

## 3.2 Charge Reconciliation
### 3.2.1 Daily department reconciliation
- **A1.** Compare scheduled/performed activity (schedules, logs, eMAR) to posted charges daily
- **A2.** Certify department reconciliation completion (attestation)
### 3.2.2 Missing charge identification
- **A1.** Run revenue-usage analytics (volume vs charges by cost center) to find capture gaps
- **A2.** Investigate zero-charge encounters and department outliers
### 3.2.3 Late charge processing
- **A1.** Post late charges within late-charge window; evaluate against payer cutoff
- **D1.** Claim already submitted when late charge posts?
  - ├─ Within payer window & material → corrected claim (6.5.1)
  - ├─ Immaterial per policy → write off with reason code
  - └─ Claim not yet out → add to claim before release

## 3.3 CDM Management
### 3.3.1 CDM item add/change/inactivate
- **A1.** Intake request; validate CPT/HCPCS, revenue code, description, price, multiplier logic
- **A2.** Route through review (coding, compliance, finance) and approve; effective-date the change
- **A3.** Synchronize CDM change to downstream systems (billing, contract engine, estimator, MRF)
### 3.3.2 Annual code update maintenance
- **A1.** Apply quarterly/annual CPT/HCPCS additions, deletions, revisions; map deleted codes to replacements
- **A2.** Test claim generation for changed items before effective date
### 3.3.3 Pricing updates & strategic pricing review
- **A1.** Run annual price study (market position, cost, payer fee schedule floors/ceilings)
- **A2.** Apply price changes with board/finance approval; update transparency artifacts (3.5)
### 3.3.4 CDM audit & synchronization
- **A1.** Audit CDM for invalid code/revenue-code pairs, missing HCPCS where required, price anomalies
- **A2.** Reconcile multi-system CDM copies for drift

## 3.4 Revenue Integrity Auditing
### 3.4.1 Pre-bill charge review edits
- **A1.** Run rules that stop claims with charge anomalies (e.g., OR time without anesthesia, delivery
  without newborn charges, implant without device charge)
- **A2.** Work pre-bill review queues within DNFB budget {gates: 6.1.1}
### 3.4.2 Retrospective charge audits
- **A1.** Sample paid claims for charge accuracy (over- and under-charging both corrected)
- **A2.** Quantify findings; rebill/refund per compliance rules {links: 12.4}
### 3.4.3 Charge trend surveillance
- **A1.** Monitor charge volume by CDM item/department for breaks in pattern (trigger: interface failure,
  practice change)
- **A2.** Alert departments; recover missed windows within timely filing
### 3.4.4 Defense audits
- **A1.** Perform line-by-line itemized bill audits when payers/patients contest charges
- **A2.** Produce audit response with documentation support {links: 12.2}

## 3.5 Price Transparency Operations
- **A1.** Produce and publish machine-readable file (all items/services, payer-specific negotiated
  rates) per CMS schema; refresh on schedule
- **A2.** Maintain shoppable-services display/estimator availability
- **A3.** Monitor compliance (completeness/format) and remediate gaps

**Failure modes:** missed charges (leakage), duplicate charges, unit errors (esp. drugs), late
charges past filing, CDM-claim mismatch, orphan charge triggers.
**Metrics:** charge lag days, late charge %, charge capture audit accuracy, gross revenue by
department vs volume, DNFB attributable to charge review.

---

# RC-04 Clinical Documentation Integrity (CDI)

Roles: CDI Specialist (RN/coder hybrid), Physician Advisor, CDI Manager. Systems: CDI workflow
tools, encoder, prioritization/NLP engines.

## 4.1 Concurrent Documentation Review
- **A1.** Prioritize admitted cases for review (payer, LOS, DRG potential, NLP flags)
- **A2.** Review record for specificity gaps: CC/MCC capture, POA status, acuity, clinical validity
- **A3.** Assign working DRG; update as record evolves
- **D1.** Documentation gap identified?
  - ├─ Specificity/acuity gap → issue query (4.2)
  - ├─ Clinical validity concern (dx documented but not clinically supported) → clinical validation query
  - └─ No gap → continue monitoring

## 4.2 Physician Query Process
- **A1.** Compose compliant, non-leading query with clinical indicators and multiple-choice options
  (per AHIMA/ACDIS practice brief)
- **A2.** Deliver query; track response aging; escalate unanswered per policy
- **A3.** Record response; ensure agreed diagnoses are documented in the record itself (not just query)
- **D1.** Provider response?
  - ├─ Agrees & documents → update working DRG
  - ├─ Disagrees with rationale → close; no code assignment from query
  - ├─ No response → escalate (physician advisor → service chief); track noncompliance
  - └─ Ambiguous response → clarify with follow-up query

## 4.3 CDI–Coding DRG Reconciliation
- **A1.** Compare CDI working DRG to final coded DRG post-coding
- **A2.** Route mismatches for coder/CDI discussion; document resolution rationale
- **D1.** Mismatch resolution?
  - ├─ Coder position stands → finalize; log for CDI education
  - ├─ CDI position stands → recode; log for coder education
  - └─ Escalate → coding manager/physician advisor tie-break

## 4.4 Risk Adjustment / HCC Documentation Programs
- **A1.** Run pre-visit chronic condition reviews for VBC/MA populations (suspecting/recapture lists)
- **A2.** Query for MEAT-supported (Monitor/Evaluate/Assess/Treat) chronic condition documentation
- **A3.** Validate RAF-impacting codes are supported annually; never code unsupported suspects
  {governed-by: risk adjustment compliance — see 12.3}

## 4.5 CDI Metrics, Education & Escalation
- **A1.** Track review rate, query rate, agreement rate, CC/MCC capture, CMI trend, query impact
- **A2.** Deliver provider documentation education from query/denial patterns {feeds-back-to providers}
- **A3.** Support clinical-validation denial appeals with documentation evidence {links: 8.4.3}

---

# RC-05 Coding

Roles: Inpatient Coder, Outpatient Coder, Profee Coder, Coding Auditor, Coding Manager, HIM
Analyst. Systems: encoder/grouper, CAC/autonomous coding, abstracting, EHR HIM module.

## 5.1 Record Preparation & Work Distribution
### 5.1.1 Documentation completeness / DNFC management
- **A1.** Identify accounts awaiting documentation (op note, discharge summary, path report, signatures)
- **A2.** Issue physician deficiency notifications; escalate per medical staff rules
- **D1.** Required documentation present by coding SLA?
  - ├─ Yes → route to coding queue
  - ├─ No → hold (DNFC); escalate deficiency; monitor against bill-hold budget
  - └─ Codeable without pending item per policy → code with addendum process defined
### 5.1.2 Coding work queue assignment
- **A1.** Route by case type/credential/specialty; balance workloads; apply aging priority

## 5.2 Inpatient Facility Coding
- **A1.** Assign ICD-10-CM diagnoses with POA indicators; sequence principal diagnosis per UHDDS
- **A2.** Assign ICD-10-PCS procedures
- **A3.** Run grouper → MS-DRG/APR-DRG; validate CC/MCC and SOI/ROM drivers
- **A4.** Abstract required data (discharge disposition — payment-critical for transfer DRG rules,
  attending/operating providers)
- **A5.** Resolve edits (age/sex conflicts, manifestation rules); finalize and release to billing
- **D1.** Documentation conflict or gap found at coding?
  - ├─ Query-able → retrospective physician query (4.2 pattern)
  - └─ Codeable as documented → code; note for CDI feedback
- **D2.** Discharge disposition supports transfer rule payment reduction?
  - ├─ Verify disposition against discharge documentation before finalizing (frequent under/overpayment source)

## 5.3 Outpatient Facility Coding
- **A1.** Code diagnoses (medical necessity linkage) and CPT/HCPCS where not hard-coded via CDM
- **A2.** Apply modifiers (laterality, distinct procedure 59/X{EPSU}, discontinued 73/74)
- **A3.** Resolve OCE/NCCI edits pre-release; validate revenue code/CPT pairing
- **A4.** Observation: validate hours, carve out non-billable window; apply visit level

## 5.4 Professional Fee Coding
- **A1.** Assign E/M levels per MDM/time guidelines; validate split/shared and incident-to rules
- **A2.** Code procedures with global-period awareness (modifiers 24/25/57/58/78/79)
- **A3.** Apply teaching physician rules (GC/GE) where applicable
- **A4.** Link dx-to-procedure for necessity; sequence for claim
- **D1.** Same-day E/M with procedure?
  - ├─ Separately identifiable & documented → append 25
  - └─ Not separately identifiable → E/M not separately billed

## 5.5 Specialty Coding
- **A1.** Anesthesia: time units, base units, physical status, medical direction ratios (AA/QK/QX/QZ)
- **A2.** Interventional/cath: component coding, bundling hierarchies
- **A3.** Radiation oncology: course-based coding, simulation/planning/delivery structure
- **A4.** Home health: OASIS-driven HIPPS; SNF: PDPM components from MDS; IRF: IRF-PAI/CMGs
- **A5.** Behavioral health: time-based codes, licensure-level billing rules

## 5.6 Computer-Assisted & Autonomous Coding Oversight
- **A1.** Review/validate CAC-suggested codes; measure precision/recall by document type
- **A2.** Define autonomous-coding eligibility rules (case types passing without human review)
- **A3.** Audit autonomous output samples; tune/retract eligibility on quality regression
- **D1.** Case meets autonomous confidence threshold?
  - ├─ Yes → auto-finalize; sample-audit
  - └─ No → human coder queue

## 5.7 Coding Quality Review & Education
- **A1.** Perform pre-bill review for high-risk case types (high-weight DRGs, new coders)
- **A2.** Perform retrospective accuracy audits (internal + external); score against standard (e.g., 95%)
- **A3.** Deliver education plans; re-audit focus areas; manage coder QA performance
- **D1.** Audit finds coded claim error?
  - ├─ Not yet billed → correct
  - ├─ Billed, underpaid → rebill/corrected claim
  - └─ Billed, overpaid → refund pathway (12.4) — 60-day rule clock starts at identification

## 5.8 Coding Support for Edits, Denials & Audits
- **A1.** Resolve coding-related claim edits (6.2.3 escalations)
- **A2.** Author coding rationale for DRG downgrade/clinical validation appeals (8.4.3)
- **A3.** Provide coding determinations for external audit responses (12.1/12.2)

**Metrics:** coding accuracy %, DNFB/DNFC days, coder productivity, query rate, CMI,
autonomous coding rate & accuracy, edit rework rate.

## Mid-cycle relationships
- 2.1 `gates` claim status integrity; 2.2 `produces` authorized-days artifact consumed by 8.4.3
- 3.x `precedes` 6.1 (charges must be complete before bill drop; bill-hold window balances lag vs completeness)
- 4.x `precedes/parallels` 5.2 (concurrent CDI during stay; reconciliation post-coding)
- 5.x `produces` coded claim data `consumed-by` 6.1.2
- 5.7/4.5 `feed-back-to` provider & coder education; denial outcomes (8.x) `feed-back-to` 2/3/4/5
