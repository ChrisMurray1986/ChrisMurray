# UC-11-* … UC-14-* — Cross-Cutting (Contracting, Compliance, Analytics, Data/Tech)

---

## UC-11-* Payer Contracting, Credentialing & Enrollment (RC-11)

### UC-11-01 Contract Term Extraction & Load Verification
- PAT-LLM + PAT-IDP | A2 | R2
- Targets: 11.1.A5, 11.2.A1–A2 | Trigger: EVT-CONTRACT (execution/amendment)
- Function: extract rates, methodologies, carve-outs, lesser-of language, timely filing, appeal
  windows, audit lookbacks, escalators from contract documents into the structured term matrix;
  cross-verify loaded engine terms against extracted terms (independent check on the load);
  parallel-price historical claims to validate before go-live
- Prevents: FM-TERMSUNLOADED | Improves: KPI-CONTRACTYIELD, false-variance rate
- Guardrails: contracting analyst approves extraction; engine changes through 11.2 testing

### UC-11-02 Amendment & Term-Date Watchdog
- PAT-RULES + PAT-NLP | A3 (alerting) | R2
- Targets: 11.1.A1, 11.1.D2 | Trigger: payer correspondence, contract calendar
- Function: detect amendment notices in payer correspondence (via UC-07-03 classification);
  calendar objection windows, renewal/termination notice deadlines, evergreen rollovers; alert
  with materiality assessment (modeled dollar impact of proposed changes)
- Prevents: FM-AMENDMISS | Improves: negotiation leverage retention

### UC-11-03 Payer Policy Monitoring & Change Routing
- PAT-NLP + PAT-LLM | A1 | R2
- Targets: 11.3 | Trigger: bulletin/portal/transmittal publication
- Function: continuously ingest payer bulletins, MLN/MAC transmittals, portal announcements;
  classify operational impact (auth list change, edit change, documentation requirement,
  site-of-care policy); route to owning teams with drafted implementation tasks and due dates;
  verify implementation by watching for policy-correlated denial spikes
- Prevents: FM-NOAUTH (grid staleness), policy-change denial waves | Improves: KPI-IDR
- Feeds: UC-01-07 auth grid, UC-06-03 edit candidates, 3.3 CDM changes

### UC-11-04 Credentialing & Enrollment Lifecycle Automation
- PAT-RULES + PAT-RPA + PAT-IDP | A3 | R2
- Targets: 11.4.A4–A5, 11.5 | Trigger: expirable clocks, roster changes, EVT-ENROLLCHANGE
- Function: track every expirable (license, DEA, cert, CAQH attestation, revalidation) with
  escalating alerts; auto-populate enrollment applications (855s, payer forms) from provider
  master; run continuous exclusion monitoring (OIG LEIE, SAM) against all active providers;
  auto-hold claims for not-yet-effective enrollments and auto-release on effective date
- Prevents: FM-ENROLLGAP, exclusion-list billing exposure | Improves: enrollment turnaround,
  enrollment denial rate
- Guardrails: exclusion hits escalate to compliance immediately (never auto-cleared)

### UC-11-05 Payer Scorecard & Negotiation Analytics
- PAT-PRED + PAT-LLM | A0 | R4
- Targets: 11.1.A2–A3, 11.6.A5 | Trigger: negotiation cycles, JOC cadence
- Function: compute per-payer total cost of doing business (yield vs contract, denial burden,
  auth/appeal labor, payment timing); simulate proposed term changes against volume history;
  draft JOC issue inventories with dollar quantification from 8.5/9.4 project data
- Improves: KPI-CONTRACTYIELD, JOC resolution dollars

### UC-11-06 VBC Settlement & Attribution Validation
- PAT-PRED + PAT-RULES | A1 | R2
- Targets: 11.7.A2–A3 | Trigger: settlement statements, roster files
- Function: independently model expected shared-savings/risk settlements (claims runout,
  truncation, risk-adjustment inputs); reconcile payer settlement statements against internal
  model; reconcile capitation rosters/PMPM payments monthly; monitor encounter-submission
  acceptance rates (risk-adjustment data completeness)
- Prevents: settlement acceptance without validation, encounter data leakage
- Improves: VBC settlement accuracy

---

## UC-12-* Compliance, Audit & Program Integrity (RC-12)

### UC-12-01 Audit Correspondence Intake & Deadline Management
- PAT-IDP + PAT-RULES | A3 | R1
- Targets: 12.1.A1–A2, 12.2 | Trigger: EVT-AUDITREQ (any channel)
- Function: classify all inbound audit correspondence (auditor type, request scope, claim list,
  deadline); validate request legitimacy against auditor authority and contract audit clauses
  (lookback limits, ADR caps); stamp deadlines into tracked workflow with escalation
- Prevents: FM-AUDITDEADLINE, out-of-scope compliance | Improves: ADR response timeliness
- Guardrails: legitimacy determinations reviewed by audit coordinator; UPIC/fraud-unit
  correspondence routes directly to compliance/counsel (12.1.D2) — flagged, never auto-processed

### UC-12-02 Audit Response Packet Assembly
- PAT-AGENT + PAT-RULES | A2 | R1
- Targets: 12.1.A3 | Trigger: validated record request
- Function: compile complete record sets per request specification (pull from EHR/HIM),
  completeness-check against a document checklist per audit type, assemble organized submission
  with index; QA report before release
- Improves: audit win rate (complete records win), response labor
- Guardrails: HIM/audit coordinator approves release; minimum-necessary enforced

### UC-12-03 Provider Billing Pattern Surveillance
- PAT-ANOM | A0 | R1
- Targets: 12.3.A3 | Trigger: continuous claims stream
- Function: statistical outlier detection on coding/billing distributions by provider/department
  (E/M levels, modifier 25/59 usage, units, high-weight DRG concentration) against peer and
  historical baselines; feed internal audit work plan with risk-ranked targets
- Prevents: FM-CODEERR patterns maturing into FCA exposure | Improves: internal audit targeting
- Guardrails: surveillance output is investigative lead only — no automated adverse action
  against providers; monitored for the same drift AI coding tools can introduce (UC-05-01)

### UC-12-04 Overpayment Register & 60-Day Clock Automation
- PAT-RULES | A3 (tracking) / A2 (refund execution) | R1
- Targets: 12.4 | Trigger: overpayment identification from any source (7.4.2, 9.5, 5.7, 12.1–12.3)
- Function: centralize every identified overpayment into one register with identification date,
  quantification status, and 60-day clock; drive quantification tasks; stage refunds via correct
  mechanism; produce compliance evidence trail
- Prevents: FM-60DAY | Improves: KPI-60DAY
- Guardrails: pattern-scope determinations (12.4.D1) and disclosure-protocol decisions are
  counsel/compliance calls — the system tracks, humans decide scope

### UC-12-05 Regulatory Change Intelligence
- PAT-NLP + PAT-LLM | A1 | R2
- Targets: 12.5 | Trigger: rulemaking publications, effective-date calendar
- Function: monitor federal/state rulemaking and transmittals; summarize operational impact per
  domain with citation; draft implementation task lists with owners and effective-date deadlines;
  verify implementation evidence collected
- Improves: regulatory implementation timeliness | Feeds: UC-11-03, 3.5, 10.7

### UC-12-06 Extrapolation & Exposure Modeling
- PAT-PRED | A0 | R1
- Targets: 12.1.A6, 12.3.D1 | Trigger: audit findings, internal audit results
- Function: model financial exposure of audit findings if extrapolated (universe size, error rate
  confidence intervals); support appeal-vs-accept economics and lookback-scope decisions with
  counsel
- Improves: audit strategy quality
- Guardrails: decision support only; scope decisions privileged/counsel-directed

---

## UC-13-* Analytics, Reporting & Performance Management (RC-13)

### UC-13-01 KPI Anomaly Detection & Auto-Narrative
- PAT-ANOM + PAT-LLM | A0 | R4
- Targets: 13.1.D1, 13.2.A3 | Trigger: daily/weekly metric refresh
- Function: detect statistically significant KPI movements; auto-distinguish data/definition
  artifacts from real operational change; generate drill-down narratives (which payer, which
  defect, which team drove the move) with linked work-lists
- Improves: time-to-detection of operational breaks; leadership signal quality

### UC-13-02 Reserve & Net Revenue Estimation Models
- PAT-PRED | A1 | R2
- Targets: 13.3.A1, 13.3.A3, 9.7.A2 | Trigger: month-end close
- Function: ML realization models by payer/age/denial-state cohort for contractual allowance and
  reserve estimation; hindsight-test automatically (13.3.D1) and flag estimation bias; reserve
  for denial/audit exposure using live 8.x/12.x inventory
- Improves: net revenue accuracy, close speed
- Guardrails: model outputs reviewed by finance; auditability of estimation methodology (external
  audit consumes this — full lineage required)

### UC-13-03 Cash Forecasting
- PAT-PRED | A0 | R4
- Targets: 13.2, treasury planning | Trigger: daily
- Function: forecast cash by payer/week from claim inventory state, payer payment-timing
  distributions, and denial pipeline; alert on forecast-vs-actual divergence (early warning of
  payer slowdowns or pipeline breaks)
- Improves: KPI-CASHGOAL management, early detection of FM-EDISILENT/payer behavior shifts

### UC-13-04 Model Governance Telemetry (meta-use-case)
- PAT-ANOM | A4 (monitoring) | R4
- Targets: 13.4.A2, every UC in this catalog | Trigger: continuous
- Function: central monitoring of all deployed models/agents — performance vs baseline, drift,
  override rates, exception-queue depths, demographic-impact metrics for patient-affecting
  models; auto-demote autonomy (A3→A1) on breach of performance floor
- Prevents: silent model decay, FM-BOTSILENT (model variant) | Governs: entire portfolio
- Guardrails: this is itself GOV-controlled infrastructure (05-governance-assurance.md)

---

## UC-14-* Master Data, Technology & Vendor Operations (RC-14)

### UC-14-01 Payer/Plan Master Intelligence
- PAT-PRED + PAT-MATCH | A1 | R2
- Targets: 14.1.A1 | Trigger: mapping errors, new plan encounters
- Function: detect payer/plan master defects from downstream signals (eligibility denials
  clustering on a plan code, remit routing failures); recommend mapping corrections; suggest
  mappings for newly encountered plans from card/271 evidence
- Prevents: FM-PLANMAP at the source table | Improves: master-data defect rate
- Guardrails: changes via 14.1.D1 governance with effective-dating

### UC-14-02 Master Data Drift & Sync Monitoring
- PAT-ANOM + PAT-RULES | A4 (alerting) | R4
- Targets: 14.1.D1 sync, 3.3.4 | Trigger: nightly cross-system comparison
- Function: detect divergence across system copies of CDM, payer master, provider master,
  dictionaries (estimator vs billing vs MRF vs contract engine); alarm with diff detail
- Prevents: FM-CDMSTALE, silent cross-system inconsistency

### UC-14-03 EDI Pipeline Observability
- PAT-ANOM | A4 (alerting) | R4
- Targets: 14.3.A3 | Trigger: continuous transaction-flow telemetry
- Function: monitor every transaction type (837/835/270/276/278) for volume anomalies, missing
  files, acknowledgment gaps by payer/route; alarm within hours; auto-open incidents with
  clearinghouse/payer context
- Prevents: FM-EDISILENT (catastrophic silent failure class) | Improves: KPI pipeline integrity

### UC-14-04 Bot Fleet Observability & Self-Healing
- PAT-ANOM + PAT-AGENT | A3 | R4
- Targets: 14.4.A3–A4 | Trigger: continuous fleet telemetry
- Function: monitor success rates per bot; detect portal/UI changes (failure signature
  classification); quarantine failing bots and return their work to named human queues
  explicitly; auto-repair simple selector breaks; replay failed transactions after repair
- Prevents: FM-BOTSILENT | Improves: bot net yield, automation reliability
- Guardrails: quarantine-and-return-to-human is mandatory default on unknown failure

### UC-14-05 Automation Candidate Mining
- PAT-PRED | A0 | R4
- Targets: 14.4.A1, 13.2.A4 | Trigger: quarterly portfolio review
- Function: mine touch/action logs for high-volume, low-variance, rules-expressible work
  (automation candidates) and high-judgment work being done robotically (mis-assigned to
  humans/bots); rank by net labor yield and error-reduction value
- Improves: automation portfolio ROI; feeds this catalog's backlog

### UC-14-06 Downtime Detection & Recovery Orchestration
- PAT-RULES + PAT-AGENT | A2 | R2
- Targets: 14.6 | Trigger: EVT-DOWNTIME
- Function: detect revenue-affecting outages from transaction telemetry (often before formal
  incident); activate downtime procedure checklists; after restoration, drive reconstruction
  reconciliation (census vs accounts vs charges completeness) with gap work-lists
- Prevents: unbilled care from outage windows | Improves: downtime recovery completeness

### UC-14-07 Vendor Performance Analytics
- PAT-ANOM + PAT-PRED | A0/A1 | R4
- Targets: 14.5.A3 | Trigger: vendor activity/remit files, invoice cycles
- Function: score vendor SLA attainment continuously; validate contingency invoices against
  actual collections attribution; quality-sample vendor-worked accounts; detect inventory
  stranding during transitions
- Improves: vendor SLA attainment, invoice accuracy
