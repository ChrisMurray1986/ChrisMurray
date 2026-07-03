# Function Assessment — RC-06 Claims Production · RC-07 Remittance & Posting

Roles: ROLE-BILLER, ROLE-EDITANALYST, ROLE-POSTER, ROLE-RECON, ROLE-EDI.

## RC-06 Claims Production & Submission

### 6.1 Claim Generation — ROLE-BILLER

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-6.1-01 | Bill-hold expiry ships dirty claims (6.1.1.D1); hold reasons unworked, just waited-out | Claims release at day N regardless; DNFB huddle reviews totals, not blockers | PBP-6.1-01 Hold-reason queues with owners and SLAs; release-on-expiry requires clean status, not calendar |
| PFM-6.1-02 | Payment-window/series rules hand-applied (6.1.3.A1–A3, D1) — 72-hour combines missed or wrong | Window-rule denials and duplicate-billing rejections both present | PBP-6.1-02 Window/series logic automated in billing config; exceptions queue for judgment cases |

### 6.2 Claim Editing & Scrubbing — ROLE-EDITANALYST

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-6.2-01 | Edits resolved to *pass the edit*, not fix the claim (6.2.3.A2) — modifiers/data forced → FM-CODEERR, audit exposure | Edit clearance fast, denial rate flat; "make it go through" culture | PBP-6.2-01 Resolution standards per edit class; content changes route to owning function (6.2.2.D1 discipline); hardened-by UC-06-02 |
| PFM-6.2-02 | Same defects re-edited forever; rule feedback loop (6.2.4.A1–A2) dead | Top-10 edits unchanged for a year; no custom-edit pipeline from denials | PBP-6.2-02 Monthly edit-mining cycle: recurring denial → new pre-bill edit; false-positive retirement; hardened-by UC-06-03 |
| PFM-6.2-03 | Edit queues worked FIFO regardless of dollars/filing clocks (6.2.3.A1) | High-dollar claims age behind trivia; TFL near-misses | PBP-6.2-03 Value/urgency-ranked edit queues (deadline-aware) |

### 6.3 Submission & Acknowledgment — ROLE-EDI, ROLE-BILLER

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-6.3-01 | Batch counts unverified; 999/277CA worked partially (6.3.1.A2, 6.3.2.A1–A3, D1) → FM-CLAIMDROP | "Submitted" claims payers never received, found at day 60 | PBP-6.3-01 Submission-integrity reconciliation to accepted-status per claim; hardened-by UC-06-04 |
| PFM-6.3-02 | Front-end rejections parked in a side queue (6.3.3.A1) → FM-REJECTUNWORKED | Rejection queue aged >14 days; excluded from denial reporting | PBP-6.3-02 Rejections worked same-day with reason-code prevention loop; hardened-by UC-06-05 |
| PFM-6.3-03 | ADR/attachment deadlines tracked in memory (6.3.5.A3, D1) | RFI denials for "documentation not received" on documentation that exists | PBP-6.3-03 Attachment/ADR deadline register with escalation; hardened-by UC-06-07 |

### 6.4 Secondary & Special Claims — ROLE-BILLER

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-6.4-01 | Secondaries billed before primary resolution verified (6.4.1.D1); crossovers double-billed (6.4.2.A2) | Secondary denials for primary-pending; crossover duplicates | PBP-6.4-01 Secondary release gated on primary adjudication state; crossover indicator honored; hardened-by UC-06-08 |
| PFM-6.4-02 | WC/liability claims billed like commercial (6.4.3.A1–A2) — jurisdiction forms/attachments missing | State-form rejections; adjuster info absent from claims | PBP-6.4-02 Jurisdiction playbooks with required-element checklists (feeds from PFM-1.9-04 capture) |

### 6.5 Corrected, Late & Void Claims — ROLE-BILLER

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-6.5-01 | Corrections resubmitted as new claims, not frequency-7 (6.5.1.A1, D1) — duplicate denials loop | Duplicate-denial volume high; original ICNs not referenced | PBP-6.5-01 Correction protocol by payer with ICN linkage; duplicate-denial rate as control metric |
| PFM-6.5-02 | Filing limits tracked by folklore (6.5.3.A1–A2, D1) → FM-TFL | TFL write-offs material; protective-claim option unknown to staff | PBP-6.5-02 Filing matrix codified with at-risk alarms; proof artifacts auto-preserved; hardened-by UC-06-06 |

## RC-07 Remittance Processing & Payment Posting

### 7.1 Electronic Remittance — ROLE-POSTER

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-7.1-01 | Exception queue triaged by ease; unmatched remits sit (7.1.2.A3, D1) | Suspense aging up; posters judged on lines/day | PBP-7.1-01 Exception aging SLAs; match-rate improvement fed back to rules; hardened-by UC-07-01 |
| PFM-7.1-02 | Zero-pay remits auto-adjusted without denial routing (7.1.2.A4, 7.1.3.A2) → FM-DENIALHIDDEN | Denial volumes understate 835 reality; adjustment codes hide denials | PBP-7.1-02 CARC-mapping governance with mis-map audit (adjustment-vs-denial); hardened-by UC-07-02 |
| PFM-7.1-03 | New CARC/RARC combos mapped ad hoc by whoever hits them (7.1.3.D1) | Mapping table has no owner or history | PBP-7.1-03 Mapping change control with denial-team review |

### 7.2 Manual & Paper Posting — ROLE-POSTER

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-7.2-01 | Paper EOB detail keyed as lump sums; denial codes dropped (7.2.A2) | Paper-payer denials invisible; line detail absent | PBP-7.2-01 Line-level keying standard (or IDP conversion, UC-07-03); paper payers pushed to ERA (7.2.A4) |

### 7.3 Reconciliation & Treasury — ROLE-RECON

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-7.3-01 | EFT-835 matching manual; missing remits chased when someone notices (7.3.1.A1–A2, D1) | Money-without-remit aged weeks; posted-from-portal workarounds | PBP-7.3-01 Daily TRN matching with unmatched alarms; hardened-by UC-07-04 |
| PFM-7.3-02 | Suspense as dumping ground (7.3.3.A1–A3, D1) — research happens at year-end | Suspense balance grows monotonically | PBP-7.3-02 Suspense aging SLA with weekly burn-down and escheatment discipline |

### 7.4 Adjustments & Variance — ROLE-POSTER, ROLE-UNDERPAY

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-7.4-01 | Balance forced to zero with generic adjustment codes (7.4.1.A2–A3) — variance signal destroyed → FM-VARIANCEMISS | "Contractual—other" among top codes; posting audits absent | PBP-7.4-01 Restricted adjustment codes with authority matrix; force-balance audit; hardened-by UC-07-05 |
| PFM-7.4-02 | Recoupments absorbed unvalidated (7.4.3.A2, D1) | Take-backs posted same-day, never disputed | PBP-7.4-02 Recoupment validation protocol (notice, timeliness, linkage) before acceptance; hardened-by UC-07-06 |

### 7.5 Patient Payments — ROLE-POSTER

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-7.5-01 | Allocation rules inconsistent (7.5.A2) — payments land on wrong visits; refunds spawn | Patient calls about "paid" bills; credit churn | PBP-7.5-01 Documented allocation hierarchy applied by system, not poster judgment |

### 7.6 Cash Controls — ROLE-RECON

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-7.6-01 | Batch balancing self-attested; segregation of duties thin (7.6.A1–A2) | Same person posts, adjusts, refunds; variances unexplained | PBP-7.6-01 Dual-control balancing, SoD matrix enforced in system security, override monitoring (7.6.A3) |
