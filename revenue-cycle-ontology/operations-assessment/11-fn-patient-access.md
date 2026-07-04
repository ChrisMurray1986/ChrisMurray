# Function Assessment — RC-01 Patient Access & Financial Clearance

Process-level failure modes and practices, bound to master-ontology IDs. Score each PFM 0/1/2
in the field. Primary roles: ROLE-SCHED, ROLE-PREREG, ROLE-VERIF, ROLE-AUTH, ROLE-ESTIM,
ROLE-FINCOUNS, ROLE-REGISTRAR, ROLE-PA-QA, ROLE-PA-SUP (role-level patterns: file 17).

### 1.1 Scheduling & Appointment Management — ROLE-SCHED

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-1.1-01 | Orders accepted incomplete; validation (1.1.1.A3–A4) skipped under queue pressure → downstream FM-MEDNEC, FM-NOAUTH | "We schedule it and sort it out later"; ordering-office callbacks post-service; unsigned orders found at coding | PBP-1.1-01 Completeness gate at intake with same-day ordering-office callback loop; hardened-by UC-01-01 |
| PFM-1.1-02 | Slot-first scheduling: network/site rules (1.1.2.A3, D1) checked after booking or never | OON surprises at check-in; site-of-care denials; schedulers unaware plan networks differ | PBP-1.1-02 Network check in the booking script before offering slots; plan-network cheat sheets retired in favor of system prompts |
| PFM-1.1-03 | Reschedules break auth linkage (1.1.4.A1, D1) — date moved, auth span not re-checked | Auth-date-mismatch denials cluster on rescheduled cases | PBP-1.1-03 Reschedule triggers auth revalidation task automatically; hardened-by UC-01-17/UC-01-10 |
| PFM-1.1-04 | Unscheduled/ED arrivals bypass quick-reg discipline (1.1.5.A1–A2); EMTALA fear suppresses *all* data capture | Bedside registration never completed; "ED accounts are always a mess" | PBP-1.1-04 Two-stage ED protocol: compliant quick-reg, then structured bedside completion with checklist |
| PFM-1.1-05 | Scheduling decision trees / visit-type build wrong or stale (1.1.2.A2, A4, A9): visit types map to wrong auth, network, or duration rules — schedulers following the tree faithfully still mis-key every downstream lookup | Auth/site-of-care denials cluster on specific visit types; tree and visit-type list maintained outside revenue-cycle change control; nobody can say when a branch was last validated | PBP-1.1-05 Visit-type/decision-tree change control with auth-grid and network-rule sync (14.2.A6); tree-attributed denials sampled quarterly; intended-CPT fidelity measured (1.1.2.A9, intended_cpt_accuracy) |

### 1.2 Pre-Registration — ROLE-PREREG

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-1.2-01 | Search-then-create discipline absent; duplicate MRNs created at 1.2.1.A3 → FM-DUPMRN | MPI duplicate queue growing; "easier to make a new record" | PBP-1.2-01 Mandatory match-review step; duplicate-creation rate on individual scorecards; hardened-by UC-01-02 |
| PFM-1.2-02 | Plan mapping guessed at 1.2.2.A3; card images not captured (A2) → FM-PLANMAP | Top eligibility-denial cause is wrong plan code; mapping folklore ("BCBS PPO usually means…") | PBP-1.2-02 Card capture required to complete pre-reg; plan-mapping decision support; hardened-by UC-01-03 |
| PFM-1.2-03 | MSPQ administered as a read-aloud script; answers defaulted (1.2.4.A1, D1) → FM-COB | Identical MSPQ answers across accounts; MSP denials on working-aged patients | PBP-1.2-03 MSPQ as structured interview with branch logic; sampled audio QA; hardened-by UC-01-06 |
| PFM-1.2-04 | Coverage order set by card order, not COB rules (1.2.2.D1) → FM-COB | Birthday-rule errors on dependents; secondary billed as primary | PBP-1.2-04 COB determination worksheet embedded in workflow; primacy rationale documented on account |

### 1.3 Eligibility & Benefits Verification — ROLE-VERIF

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-1.3-01 | 271 read as active/inactive only; benefits detailing (1.3.3.A1–A5) skipped → benefit-max and site-of-care denials | Benefit fields defaulted; carve-outs discovered at denial | PBP-1.3-01 Service-type benefit-detail standard with completeness edit; hardened-by UC-01-04 |
| PFM-1.3-02 | Day-of-service re-verification (1.3.1.A1 cadence) not run; T-3 result trusted at arrival → FM-ELIGLAPSE | Term-date denials on month-boundary services | PBP-1.3-02 Automated re-run at arrival with discrepancy alert to registrar |
| PFM-1.3-03 | Plan-change signals in 271 ignored (1.3.1.D2) — MA replacement, managed Medicaid assignment missed → FM-NOAUTH downstream | "Medicare" billed while 271 showed MA plan; auth denials citing wrong payer | PBP-1.3-03 Plan-change diff surfaced as a task, not a footnote; auth re-determination auto-triggered |
| PFM-1.3-04 | Coverage discovery (1.3.5) run only at write-off, not at self-pay classification → FM-FA-MISS, lost conversion | Retro Medicaid found by collection agency, not by access | PBP-1.3-04 Discovery sweep at self-pay classification + pre-statement; hardened-by UC-01-05 |
| PFM-1.3-05 | Benefit detail structurally absent from 271s — eligibility query configuration (1.3.1.A4) never built to request service-type detail or chain follow-up queries; verifiers blamed for skipping detailing the response cannot contain | 271s show generic active/inactive only across *all* verifiers; portal lookups dominate verification time; benefit fields defaulted org-wide regardless of who works the queue | PBP-1.3-05 Payer-specific query configuration governed and reviewed against companion guides and eligibility-denial patterns; response depth sampled quarterly (rte_benefit_depth); hardened-by UC-01-04 |

### 1.4 Prior Authorization & Referral — ROLE-AUTH

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-1.4-01 | "No auth required" concluded from stale grid; proof not captured (1.4.1.A3, D1) → FM-NOAUTH | Auth denials on services the grid said were exempt; no evidence trail for appeals | PBP-1.4-01 Dated proof capture mandatory to clear the requirement; grid fed by policy monitoring; hardened-by UC-01-07 |
| PFM-1.4-02 | Clinical packets under-built (1.4.2.A1, D1); submit-and-pray, then P2P scramble | High auth-denial→P2P rate; criteria gaps discovered by the payer | PBP-1.4-02 Criteria-mapped packet checklist before submission; marginal cases flagged to provider first; hardened-by UC-01-08 |
| PFM-1.4-03 | Pending auths unworked until day-of-service (1.4.3.A1, D1–D2); escalation ad hoc | Day-of-service scrambles; reschedule-vs-proceed decisions undocumented | PBP-1.4-03 T-48h escalation protocol with leadership sign-off for proceed-at-risk; hardened-by UC-01-09 |
| PFM-1.4-04 | Performed ≠ authorized never reconciled (1.4.6.A1–A3, D1) — intraop changes, date moves → FM-NOAUTH (mismatch) | CPT-mismatch denials on surgical cases; claims released on hold-expiry autopilot | PBP-1.4-04 Post-coding auth reconciliation gate before release; hardened-by UC-01-10 |
| PFM-1.4-05 | Auth-requirements grid ungoverned as build (1.4.1.A4): ad-hoc edits without versioning, source citations, or accuracy sampling — false "no auth required" ships at volume regardless of ROLE-AUTH diligence → FM-NOAUTH | Grid (e.g., Epic ASA) edits untracked; no accuracy sample ever run; grid owner unknown; auth denials on "exempt" services persist after staff coaching | PBP-1.4-05 Grid as governed master data (1.4.1.A4): change control, source-cited versions, quarterly accuracy sample against payer policy (auth_grid_accuracy); hardened-by UC-01-07 |

### 1.5 Medical Necessity & Coverage Screening — ROLE-VERIF/ROLE-SCHED

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-1.5-01 | Necessity check post-hoc, not at ordering (1.5.1.A1); provider never sees the failure → FM-MEDNEC | ABN volume near zero at a Medicare-heavy site; necessity denials instead | PBP-1.5-01 Check fires in the ordering workflow with dx-gap prompt to provider; hardened-by UC-01-11 |
| PFM-1.5-02 | ABNs issued blank/late/en-masse (1.5.2.A1–A2, D1) — invalid when needed | Signed ABNs missing estimates or reasons; "everyone gets one" practice | PBP-1.5-02 ABN issued only on triggered failure, complete, explained; election drives modifiers automatically |
| PFM-1.5-03 | Research/trial services billed to payer (1.5.3.A3) — QCT rules unapplied | Study items on commercial claims; sponsor-billable charges written off | PBP-1.5-03 Coverage-analysis grid drives account routing at registration (1.9.6.A3) |

### 1.6 Price Estimation & GFE — ROLE-ESTIM

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-1.6-01 | Estimates from chargemaster only; contract terms and accumulators ignored (1.6.1.A2) | Estimate-vs-final variance >30%; staff apologize for estimates | PBP-1.6-01 Contract-based estimation with live accumulators; variance tracked per 1.6.1.A4; hardened-by UC-01-12 |
| PFM-1.6-02 | GFE issued only on request; timing/content rules missed (1.6.2.A1–A3) | GFE compliance sampled: late or absent for self-pay schedulings | PBP-1.6-02 GFE auto-triggered by self-pay scheduling event; content rules-templated |
| PFM-1.6-03 | Estimates not stored/versioned (1.6.1.A4, 1.6.3.A2) — dispute defense and accuracy loop impossible | "We don't keep them"; NSA disputes lost by default | PBP-1.6-03 Estimate repository linked to final bill; feeds accuracy retraining and 10.7 defense |

### 1.7 Financial Counseling & Clearance — ROLE-FINCOUNS

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-1.7-01 | Clearance = checklist theater; disposition (1.7.1.D1, 1.7.5) not enforced — uncleared electives proceed silently | "Cleared" accounts missing auth/benefits; defer policy exists, never invoked | PBP-1.7-01 Clearance status gates the arrival workflow; exceptions require named sign-off; hardened-by UC-01-13 |
| PFM-1.7-02 | Counseling = payment demand; assistance screening (1.7.2.A3) skipped → FM-FA-MISS | FA applications originate in collections, not counseling; POS scripts purely collective | PBP-1.7-02 Counseling protocol pairs payment options with FA screening every time |
| PFM-1.7-03 | Medicaid/exchange applications started, never tracked (1.7.3.A2, D1) | Pending-app accounts age into bad debt; approval windows missed | PBP-1.7-03 Application pipeline with status tracking and retro-window alarms |

### 1.8 POS Collections — ROLE-REGISTRAR

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-1.8-01 | The ask never happens (1.8.1.A1–A2) — discomfort, no scripting, no expectation | POS yield <30% of estimated collectible; "we don't really ask" | PBP-1.8-01 Compliant scripting + expectation-setting at scheduling; yield on team scorecards; hardened-by UC-01-15 |
| PFM-1.8-02 | Cash controls informal (1.8.3.A1–A3) — shared drawers, unreconciled days | Overs/shorts unexplained; single-signature counts | PBP-1.8-02 Drawer discipline: individual accountability, dual verification, daily reconciliation to posting |

### 1.9 Registration / Arrival / Admission — ROLE-REGISTRAR, ROLE-PA-QA

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-1.9-01 | Identity check compressed to name+DOB confirmation (1.9.1.A1–A2) → FM-DUPMRN, wrong-patient risk | ID scan rate low; overlays discovered by HIM | PBP-1.9-01 Two-identifier + photo-ID standard enforced by workflow, exceptions logged |
| PFM-1.9-02 | Patient type/financial class guessed (1.9.2.A4, D1) — rework cascades to billing | Patient-type corrections post-discharge; recurring/series accounts built wrong | PBP-1.9-02 Type/class decision support with the taxonomy on-screen; corrections feed registrar coaching |
| PFM-1.9-03 | Regulatory notices missed or batch-signed (1.9.3.A1–A4) → FM-NOTICEMISS | IMM second copies absent; MOON delivered at hour 30; signature piles | PBP-1.9-03 Notice checklist bound to encounter close; delivery windows alarmed; hardened-by UC-01-16 |
| PFM-1.9-04 | Accident/TPL details not captured at the desk (1.9.6.A1–A2) → FM-COB, lost liens | WC claims missing employer/claim number; liability discovered at denial | PBP-1.9-04 Accident-indicator branch script with required fields; TPL specialist referral path |
| PFM-1.9-05 | Registration QA samples courtesy, not denial-linked accuracy (1.9.5.A1–A3) | QA scores 98% while eligibility denials climb | PBP-1.9-05 QA rebuilt on denial-linked field accuracy with individual feedback loops (BP-PI-07) |
