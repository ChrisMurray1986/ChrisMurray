# UC-02-* … UC-05-* — Mid-Cycle (UR, Charge Capture, CDI, Coding)

---

## UC-02-* Utilization Review & Case Management (RC-02)

### UC-02-01 Admission Status Prediction
- PAT-PRED + PAT-NLP | A0/A1 | R1
- Targets: 2.1.1 | Trigger: EVT-ADT (admission decision)
- Function: score IP-vs-OBS likelihood at admission from vitals, labs, orders, history; rank UR
  queue so nurses review highest-risk status calls first; surface criteria-relevant clinical facts
- Prevents: FM-STATUSWRONG | Improves: KPI-OBSRATE, status-change rate, CC44 volume
- Guardrails: status is always a physician/UR determination; model provides prioritization and
  evidence only

### UC-02-02 Criteria Auto-Abstraction
- PAT-NLP | A1 | R1
- Targets: 2.1.1.A2, 2.2.2 | Trigger: UR review due
- Function: map chart evidence to MCG/InterQual criteria elements automatically; pre-populate
  criteria worksheets with citations; flag unmet criteria needing documentation or P2P prep
- Improves: UR nurse throughput, concurrent denial overturn rate
- Guardrails: nurse validates every criteria determination before payer submission

### UC-02-03 Payer Notification & Clinical Submission Bots
- PAT-RPA + PAT-LLM | A3 (notification) / A2 (clinicals) | R1
- Targets: 2.2.1, 2.2.2 | Trigger: EVT-ADT admit, review cadence clocks
- Function: auto-submit admission notifications within contract windows with reference capture;
  assemble and stage concurrent review packets (LLM summary + criteria mapping from UC-02-02)
- Prevents: late-notification denials (2.2.1.D1) | Improves: concurrent denial rate
- Guardrails: clinical summaries cite record; nurse approves clinical submissions

### UC-02-04 Authorized-Days Runway Monitor
- PAT-RULES | A4 (alerting) | R4
- Targets: 2.2.3 | Trigger: daily census vs auth records
- Function: track approved days/level vs actual and expected LOS; alarm before expiry; auto-draft
  extension requests; reconcile authorized-vs-billed days at discharge for appeal artifacts
- Improves: concurrent denial rate, KPI-AVOIDDAYS
- Prevents: unauthorized-day denials

### UC-02-05 Avoidable Day Classification
- PAT-NLP + PAT-ANOM | A3 | R4
- Targets: 2.3.A1 | Trigger: daily LOS review
- Function: classify delay causes from case management notes into avoidable-day taxonomy
  (payer delay, placement, internal); quantify payer-caused days for JOC escalation (11.6)
- Improves: KPI-AVOIDDAYS; feeds payer accountability dollars

---

## UC-03-* Charge Capture & Revenue Integrity (RC-03)

### UC-03-01 Missing Charge Detection
- PAT-PRED + PAT-ANOM | A1 | R2
- Targets: 3.2.2 | Trigger: daily post-service sweep
- Function: model expected charges from orders/documentation/eMAR/schedules vs posted charges;
  surface probable missing charges with evidence (e.g., administration documented, no charge);
  department-level trend alarms for systemic breaks
- Prevents: FM-CHGMISS | Improves: KPI-CAPTURE-ACC, gross revenue integrity
- Guardrails: charge addition posted by department owner/analyst on recommendation (R2)

### UC-03-02 Duplicate & Anomalous Charge Screening
- PAT-RULES + PAT-ANOM | A3 | R2
- Targets: 3.4.1 | Trigger: EVT-CHARGE
- Function: real-time duplicate detection (same item/date/patient across entry paths); anomaly
  screens (units outliers, incompatible combinations); auto-hold suspects pre-bill
- Prevents: FM-CHGDUP, FM-UNITERR | Improves: KPI-CLEANCLAIM, audit exposure
- Guardrails: auto-removal only for exact-duplicate rule hits; probabilistic flags → human review

### UC-03-03 Drug Units & NDC Crosswalk Validator
- PAT-RULES | A3 | R1
- Targets: 3.1.3.A3 | Trigger: pharmacy charge posting
- Function: validate billable-unit conversion (NDC package → HCPCS units) on every drug charge;
  enforce JW/JZ waste logic; block MUE-exceeding units pre-bill with pharmacist verification path
- Prevents: FM-UNITERR (top overpayment/audit driver) | Improves: KPI-CAPTURE-ACC, audit takeback
- Guardrails: crosswalk table governed under 14.1; blocks are reviewable, never silently dropped

### UC-03-04 Charge Trigger & Interface Surveillance
- PAT-ANOM | A4 (alerting) | R4
- Targets: 3.1.1.A3, 3.4.3 | Trigger: continuous charge-stream monitoring
- Function: monitor charge volume by CDM item/department/interface against seasonal baselines;
  alarm on breaks (dropped interface, trigger misconfiguration) within hours, not month-end
- Prevents: FM-CHGMISS (systemic variant), FM-EDISILENT analog for charges
- Improves: KPI-CHGLAG, KPI-LATECHG

### UC-03-05 CDM Update Automation
- PAT-RULES + PAT-NLP | A2 | R1
- Targets: 3.3.1, 3.3.2, 3.3.4 | Trigger: quarterly/annual code releases, EVT-REGCHANGE
- Function: diff new CPT/HCPCS releases against CDM; auto-propose add/inactivate/remap actions
  with crosswalks; detect invalid code/revenue-code pairs continuously; reconcile multi-system
  CDM drift nightly
- Prevents: FM-CDMSTALE | Improves: edit rates, KPI-CLEANCLAIM
- Guardrails: CDM changes apply through governed approval workflow (3.3.1.A2), never direct

### UC-03-06 Documentation-Derived Autonomous Charging
- PAT-NLP + PAT-RULES | A3 (audited) | R1
- Targets: 3.1.1, 3.1.3 | Trigger: EVT-DOCCOMPLETE
- Function: derive charges from clinical documentation for rule-stable domains (infusion
  start/stop hierarchy, ED facility level criteria, observation hours carve-outs); post with
  full evidence trail; sample-audited
- Prevents: FM-CHGMISS, ED/infusion leveling errors | Improves: KPI-CAPTURE-ACC, KPI-CHGLAG
- Guardrails: domain-by-domain enablement with accuracy proof; audit sampling per R1

### UC-03-07 Device/Implant Charge Reconciliation
- PAT-MATCH + PAT-RULES | A1 | R2
- Targets: 3.1.3.A5, 3.1.3.D1 | Trigger: OR/cath case close
- Function: match supply-chain issue records and invoices to posted implant charges; flag
  unmatched high-cost devices; detect warranty/credit situations requiring device-credit
  reporting (value code FD)
- Prevents: implant leakage, device-credit compliance findings | Improves: KPI-CAPTURE-ACC

### UC-03-08 MRF/Transparency Pipeline Automation
- PAT-RULES | A3 | R1
- Targets: 3.5 | Trigger: CDM/contract changes, publication schedule
- Function: regenerate machine-readable files from CDM + contract engine on change; validate
  schema/completeness pre-publication; monitor for compliance gaps
- Prevents: transparency noncompliance penalties | Improves: publication currency

---

## UC-04-* Clinical Documentation Integrity (RC-04)

### UC-04-01 CDI Case Prioritization
- PAT-NLP + PAT-PRED | A3 (worklist) | R4
- Targets: 4.1.A1 | Trigger: census refresh
- Function: score every admitted case for query opportunity (documentation-DRG gap, missing
  CC/MCC evidence, clinical-validity risk) so CDI reviews the right charts; replaces
  payer/LOS-only heuristics
- Prevents: FM-DOCGAP | Improves: KPI-QUERYRATE quality, KPI-CMI, review coverage

### UC-04-02 Evidence Surfacing & Working-DRG Assist
- PAT-NLP | A0 | R1
- Targets: 4.1.A2–A3 | Trigger: chart open in CDI tool
- Function: highlight clinical indicators supporting/undermining documented diagnoses (labs,
  meds, vitals vs documented condition); compute working DRG deltas for candidate clarifications
- Improves: CDI specialist throughput, clinical-validation denial defense
- Guardrails: evidence display only; no diagnosis suggestion enters the record via this path

### UC-04-03 Compliant Query Drafting
- PAT-LLM + PAT-RULES | A2 | R1
- Targets: 4.2.A1 | Trigger: CDI identifies gap
- Function: draft non-leading, multiple-choice queries per AHIMA/ACDIS brief with auto-inserted
  clinical indicators and citations; rules engine enforces compliant structure (options include
  "unable to determine", no diagnosis suggestion without indicators)
- Improves: query turnaround, query compliance
- Guardrails: CDI specialist reviews/sends every query; template compliance is hard-validated

### UC-04-04 HCC Suspecting & Recapture
- PAT-PRED + PAT-NLP | A1 | R1
- Targets: 4.4 | Trigger: pre-visit planning, annual recapture cycles
- Function: generate chart-evidence-backed chronic condition suspect lists (prior coded, clinical
  indicator-supported); require MEAT-supported provider confirmation; track recapture completion
- Improves: RAF accuracy | Prevents: both under-capture and unsupported-code compliance risk
- Guardrails: suspects without chart evidence are never presented (risk-adjustment integrity —
  12.3.A1); provider attestation required; audit trail per suspect

### UC-04-05 DRG Reconciliation Triage
- PAT-RULES + PAT-PRED | A3 | R4
- Targets: 4.3 | Trigger: EVT-CODED
- Function: auto-compare CDI working DRG vs final coded DRG; auto-close exact matches; route
  true mismatches with pre-built comparison evidence; track resolution patterns for education
- Improves: reconciliation throughput, coder/CDI education targeting

---

## UC-05-* Coding (RC-05)

### UC-05-01 Autonomous/Computer-Assisted Coding
- PAT-NLP + PAT-LLM | A3 (eligible case types) / A1 (assist elsewhere) | R1
- Targets: 5.2, 5.3, 5.4, 5.6 | Trigger: EVT-DOCCOMPLETE
- Function: full code assignment (dx/px/modifiers/POA) for high-confidence case types
  (recurring ancillary, straightforward ED/profee E/M) with auto-finalize; suggestion mode with
  evidence links for complex cases; continuous precision/recall measurement by document type
- Prevents: FM-CODEERR (consistency), coding delay | Improves: KPI-CODEACC, KPI-DNFB, coder productivity
- Guardrails: eligibility rules per 5.6.A2 (governed enablement); mandatory audit sampling with
  auto-retraction of eligibility on quality regression (5.6.A3); E/M level distributions monitored
  for drift (12.3 outlier exposure)

### UC-05-02 Pre-Bill DRG Integrity & Audit-Risk Scoring
- PAT-PRED | A0/A1 | R1
- Targets: 5.7.A1 | Trigger: EVT-CODED, pre-release
- Function: score finalized claims for DRG error likelihood and external-audit selection risk
  (RAC-targeted DRGs, single-CC dependency, disposition-sensitive payments); route high-risk to
  second-level review before release
- Prevents: FM-CODEERR, FM-DISPO, audit takebacks | Improves: KPI-CODEACC, KPI-AUDITWIN

### UC-05-03 Discharge Disposition Validator
- PAT-NLP + PAT-RULES | A1 | R1
- Targets: 5.2.D2 | Trigger: inpatient coding finalization
- Function: cross-check coded disposition against discharge documentation and post-acute
  claims/ADT signals (transfer DRG rule exposure); flag mismatches pre-bill
- Prevents: FM-DISPO | Improves: transfer-rule payment accuracy

### UC-05-04 Documentation Deficiency Chase Automation
- PAT-RULES + PAT-CONV | A3 | R4
- Targets: 5.1.1 | Trigger: DNFC aging
- Function: detect missing documents blocking coding (op note, path, signatures); auto-notify
  responsible providers with escalating cadence and one-tap completion links; forecast DNFC
  impact by provider
- Improves: KPI-DNFC, KPI-CLAIMLAG

### UC-05-05 Coding Work Distribution Optimizer
- PAT-OPT | A4 | R4
- Targets: 5.1.2 | Trigger: continuous queue state
- Function: assign cases by credential/specialty/complexity/aging/filing-deadline priority;
  balance workloads; predict backlog and staffing needs
- Improves: KPI-DNFB, coder productivity

### UC-05-06 Coding QA Sampling & Education Targeting
- PAT-PRED | A3 (sampling) | R4
- Targets: 5.7 | Trigger: audit cycles
- Function: replace random QA samples with risk-weighted selection (new coders, changed
  guidelines, denial-correlated patterns); auto-compile per-coder error taxonomies into
  education plans; verify improvement via focused re-audit
- Improves: KPI-CODEACC, audit efficiency

### UC-05-07 Edit/Denial Coding Resolution Assist
- PAT-LLM + PAT-RULES | A1 | R1
- Targets: 5.8 | Trigger: coding-category edits (6.2.2.D1) and denials (8.2.A2)
- Function: for NCCI/modifier/dx edits and coding denials, retrieve governing guidance (NCCI
  policy, Coding Clinic references, payer policy) and draft resolution recommendation with
  citation; draft coding rationale sections for DRG appeals (8.4.3.A2)
- Improves: edit turnaround, KPI-OVERTURN (coding denials)
- Guardrails: coder approves all code changes; citations verified against source library
