# Function Assessment — RC-02 UR · RC-03 Charge Capture · RC-04 CDI · RC-05 Coding

Process-level failure modes and practices for the mid cycle. Roles: ROLE-URN, ROLE-CM,
ROLE-PHYSADV, ROLE-CHGANALYST, ROLE-DEPTCHG, ROLE-CDMANALYST, ROLE-REVINT, ROLE-CDIS,
ROLE-CODER-IP/OP/PRO, ROLE-CODEAUD, ROLE-HIM, ROLE-PROVIDER.

## RC-02 Utilization Review & Case Management

### 2.1 Admission Status Determination — ROLE-URN, ROLE-PHYSADV

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-2.1-01 | First status review hours late (2.1.1.A1); status set by bed placement, not criteria → FM-STATUSWRONG | OBS-to-IP flips after midnight; CC44 volume high or (worse) zero | PBP-2.1-01 Status review within admission-decision window, staffed to arrival pattern; hardened-by UC-02-01 |
| PFM-2.1-02 | Criteria worksheets completed as after-the-fact paperwork (2.1.1.A2) — determinations don't match documentation | Worksheets identical across cases; criteria cited absent from chart | PBP-2.1-02 Worksheet = the working document, evidence-linked (feeds `um_worksheets`); hardened-by UC-02-02 |
| PFM-2.1-03 | Physician advisor referrals late/rubber-stamped (2.1.4.A1–A3, D1) | Advisor agrees with requestor >95%; referrals post-discharge | PBP-2.1-03 Referral SLA + advisor rationale audit; disagreement rate monitored as signal (see RFM-PHYSADV) |

### 2.2 Concurrent Review & Payer Notification — ROLE-URN, ROLE-CM

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-2.2-01 | Notification windows missed on weekends/holidays (2.2.1.A1, D1) | Late-notification denials cluster Mon/Tue admissions | PBP-2.2-01 Seven-day notification coverage or automation; hardened-by UC-02-03 |
| PFM-2.2-02 | Reviews submitted on payer cadence but content-thin (2.2.2.A1); auth days run out unnoticed (2.2.3.A1, D1) | Concurrent denials for "insufficient clinical"; unauthorized days at discharge | PBP-2.2-02 Criteria-mapped review content + auth-days runway visible on census; hardened-by UC-02-04 |
| PFM-2.2-03 | P2P offers missed or unprepped (2.2.4.A1–A2) | P2P conversion low; attendings learn of P2P after window | PBP-2.2-03 P2P roster + prep brief protocol with the physician advisor |

### 2.3 Discharge & Transitions — ROLE-CM

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-2.3-01 | Avoidable days untracked or blamed uniformly on payers (2.3.A1) | No taxonomy; "payer delay" = 90% of entries | PBP-2.3-01 Avoidable-day taxonomy with internal categories honestly used; payer-caused days → JOC ledger (hardened-by UC-02-05) |
| PFM-2.3-02 | Discharge-appeal notices (IMM second copy) missed (2.3.A3, D1) → FM-NOTICEMISS | QIO appeals reveal notice gaps | PBP-2.3-02 Notice delivery bound to discharge-planning milestones |

### 2.4 Retrospective UR — ROLE-URN

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-2.4-01 | Held accounts reviewed for billability, not defensibility (2.4.A1) — bill-and-hope | Status-related denials on held accounts; self-denial/rebill (2.1.3.D1) never used | PBP-2.4-01 Retro review with explicit defend/self-deny decision and documented rationale |

## RC-03 Charge Capture & Revenue Integrity

### 3.1 Charge Generation & Entry — ROLE-DEPTCHG, ROLE-CHGANALYST

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-3.1-01 | Interface/trigger failures repaired silently, root cause never fixed (3.1.1.A3, D1) → FM-CHGMISS | Same interface queue cleared weekly; orphan charges recurring | PBP-3.1-01 Trigger-failure taxonomy with fix-forward rule; queue clearance ≠ closure; hardened-by UC-03-04 |
| PFM-3.1-02 | High-complexity areas run folk charging: infusion hierarchy, ED leveling inconsistent (3.1.3.A2, A4) | Leveling distribution differs by shift; infusion charges flat regardless of documentation | PBP-3.1-02 Department charging standards with criteria sheets and audit; hardened-by UC-03-06 |
| PFM-3.1-03 | Drug units converted by habit (3.1.3.A3) → FM-UNITERR; waste undocumented | MUE hits; JW/JZ absent; pharmacist never in the loop | PBP-3.1-03 NDC→HCPCS crosswalk governed; unit edits at entry; hardened-by UC-03-03 |
| PFM-3.1-04 | Provider encounters closed without charges; missing-encounter list unworked (3.1.4.A2–A3, D1) | Profee charge lag >5 days; "the doctors will get to it" | PBP-3.1-04 Encounter-close SLA with chair-level escalation and mobile capture |
| PFM-3.1-05 | Clinical build ships unreviewed into the charge surface: new/changed order sets and documentation templates break charge-trigger mappings (3.1.1.A2, 14.2.A6) → FM-CHGMISS, FM-CDMSTALE | Orphan-charge and interface-queue spikes correlate with clinical release dates; order-set changes reach revenue integrity as edit/denial clusters weeks later | PBP-3.1-05 Revenue regression on clinical build releases: trigger fire-tests against the CDM, order-set→charge mapping sampled (clinical_build_governance); hardened-by UC-03-04 |

### 3.2 Charge Reconciliation — ROLE-DEPTCHG

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-3.2-01 | Daily reconciliation attested, not performed (3.2.1.A1–A2) | Attestations 100%, late charges anyway; no source-log comparison evident | PBP-3.2-01 Reconciliation = schedule/log-to-charge match with exceptions listed, sampled by revenue integrity; hardened-by UC-03-01 |
| PFM-3.2-02 | Late charges written off silently below threshold (3.2.3.D1) — threshold nobody set | Late-charge write-off code among top adjustments | PBP-3.2-02 Late-charge policy with materiality set by finance; corrected-claim path exercised |

### 3.3 CDM Management — ROLE-CDMANALYST

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-3.3-01 | CDM changes by direct edit; review workflow (3.3.1.A2) bypassed → FM-CDMSTALE | No change log; downstream systems out of sync (3.3.4.A2) | PBP-3.3-01 Governed change workflow, effective-dated, synchronized push; hardened-by UC-03-05 |
| PFM-3.3-02 | Annual code update = find-and-replace under deadline (3.3.2.A1–A2); no claim testing | Q1 edit spikes every year | PBP-3.3-02 Update runbook with test claims before effective date |

### 3.4 Revenue Integrity Auditing — ROLE-REVINT

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-3.4-01 | Pre-bill review queues staffed as overflow; DNFB pressure empties them unread (3.4.1.A2) → FM-CHGDUP and unit errors escape | Review bypass rate unmeasured; "we release at day 5 regardless" | PBP-3.4-01 Review capacity sized to hit-rate; bypass requires sign-off and is tracked; hardened-by UC-03-02 |
| PFM-3.4-02 | Retro audits find overcharges, refund path unclear (3.4.2.A2) → FM-60DAY exposure | Findings sit in spreadsheets; compliance learns late | PBP-3.4-02 Audit findings flow to the overpayment register (12.4) by rule |

### 3.5 Price Transparency — ROLE-REVINT

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-3.5-01 | MRF published from stale extracts (3.5.A1); nobody owns refresh | File dates months old; estimator and MRF disagree | PBP-3.5-01 MRF regeneration bound to CDM/contract change events; hardened-by UC-03-08 |

## RC-04 Clinical Documentation Integrity

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-4.1-01 | Review prioritization by payer/LOS habit (4.1.A1); high-opportunity charts unseen → FM-DOCGAP | Review rate high, query yield low | PBP-4.1-01 Opportunity-scored worklists; coverage vs yield both tracked; hardened-by UC-04-01 |
| PFM-4.2-01 | Leading or drive-by queries (4.2.A1); answers not documented in record (4.2.A3) | Query templates suggest diagnoses; coded dx present only in query threads | PBP-4.2-01 AHIMA/ACDIS-compliant templates, response-in-record rule enforced; hardened-by UC-04-03 |
| PFM-4.2-02 | Query non-response tolerated (4.2.A2, D1) — escalation path exists on paper | Response rate <70%; same providers forever | PBP-4.2-02 Escalation through physician advisor to service chief with visible metrics (needs BP-OM-04) |
| PFM-4.3-01 | DRG mismatches resolved by seniority, not evidence (4.3.A2, D1) | Reconciliation log shows one side always wins | PBP-4.3-01 Evidence-based reconciliation with tie-break protocol and education loop; hardened-by UC-04-05 |
| PFM-4.4-01 | HCC capture pursued without MEAT support (4.4.A2–A3) — compliance risk masquerading as performance | Suspect lists coded wholesale; RAF up, audit exposure up | PBP-4.4-01 Evidence-backed suspecting only; validation audit before submission; hardened-by UC-04-04 |
| PFM-4.5-01 | CDI metrics = activity counts (4.5.A1); impact never tied to outcomes | Query rate celebrated; CMI flat | PBP-4.5-01 Outcome-linked CDI scorecard (capture rate, validation-denial rate, CMI decomposition) |

## RC-05 Coding

### 5.1 Record Preparation & Distribution — ROLE-HIM

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-5.1-01 | DNFC managed by exhortation; deficiency chase manual (5.1.1.A2, D1) | Coders idle while charts incomplete; deficiency emails | PBP-5.1-01 Deficiency SLA with structured tracking and auto-escalation; hardened-by UC-05-04 |
| PFM-5.1-02 | Queue assignment by grabbing (5.1.2.A1); aging and credentials mismatched | Hard cases age; simple cases cherry-picked | PBP-5.1-02 Skill/priority-routed assignment; hardened-by UC-05-05 |

### 5.2–5.5 Coding Production — ROLE-CODER-IP/OP/PRO

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-5.2-01 | Defensive undercoding: CCs/MCCs left uncoded to avoid audit anxiety (5.2.A1, A3) → FM-CODEERR (under), CMI leakage | CC/MCC capture below peers; coders cite "playing it safe" | PBP-5.2-01 Code-what's-documented standard; audit fear addressed with education, not omission (see RFM-CODER) |
| PFM-5.2-02 | Disposition defaulted (5.2.A4, D2) → FM-DISPO transfer-rule errors | Disposition corrections post-payment; home-health dispositions rare vs reality | PBP-5.2-02 Disposition verified against discharge documentation pre-finalize; hardened-by UC-05-03 |
| PFM-5.2-03 | Retrospective queries bypassed under productivity pressure (5.2.D1) | Codeable-as-documented used to close ambiguous charts | PBP-5.2-03 Query-opportunity criteria in coder standard work; query time credited in productivity |
| PFM-5.3-01 | Modifier reflexes: 59/25 appended to clear edits (5.3.A2, 5.4.D1) → FM-CODEERR (over), audit exposure | Modifier rates outliers vs peers; edit-clearance correlates with modifier use | PBP-5.3-01 Modifier decision support with documentation prompts; pattern surveillance (UC-12-03) as guardrail |
| PFM-5.4-01 | E/M leveled by habit/template, not MDM (5.4.A1) | Level distribution near-uniform per provider; cloned notes | PBP-5.4-01 MDM-based leveling education + distribution monitoring per provider |
| PFM-5.5-01 | Specialty coding by generalists: anesthesia units, interventional bundling, PDPM/OASIS rules applied from memory (5.5.A1–A4) | Specialty denial/audit rates outliers; no credentialed specialty coverage or backup | PBP-5.5-01 Specialty coding assignments credential-matched with documented backup coverage (BP-WF-05); specialty reference sets licensed and current |
| PFM-5.5-02 | Specialty billing *build* unvalidated: anesthesia base-unit/time-unit math, concurrency/medical-direction modifier logic, and specialty fee-schedule build configured once and never recalculated against payer rules (5.5.A1–A4) — coder diligence cannot fix system arithmetic | Hand-recalculated anesthesia claims disagree with system math; base-unit table version unknown; concurrency modifiers suspiciously uniform across cases | PBP-5.5-02 Specialty-build validation: sampled claims recomputed from source (base units × time ÷ increments + modifiers) at every fee-schedule load and annual code update (3.3.2.A1); clinical_build_governance |

### 5.6–5.8 CAC Oversight, QA, Support — ROLE-CODEAUD

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-5.6-01 | CAC suggestions accepted wholesale (5.6.A1); autonomous eligibility never revisited (5.6.A2–A3) | Acceptance rate ≈100%; no per-doc-type precision tracking | PBP-5.6-01 Suggestion QA with acceptance-rate norms; eligibility rules reviewed quarterly (FM-AI-03 guard) |
| PFM-5.7-01 | QA samples randomly, findings die in spreadsheets (5.7.A2–A3, D1) | Same error types quarter after quarter | PBP-5.7-01 Risk-weighted sampling, education plans with re-audit, billed-error correction path exercised; hardened-by UC-05-06 |
| PFM-5.8-01 | Coding-denial support ad hoc; edit resolutions undocumented (5.8.A1–A2) | Coding edits resolved differently per coder; appeal rationales thin | PBP-5.8-01 Coding-determination log with citation library; hardened-by UC-05-07 |
