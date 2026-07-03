# UC-01-* — Patient Access & Financial Clearance (RC-01)

Format per use case: pattern | autonomy (at maturity) | risk tier, then bindings to the base ontology.

---

### UC-01-01 Order Intake Document AI
- PAT-IDP + PAT-NLP | A3 | R1
- Targets: 1.1.1 | Trigger: EVT-ORDER | Runs-in: SYS-EHR fax/intake
- Function: extract patient, provider, NPI, service, diagnosis, laterality, signature presence from
  faxed/scanned orders; auto-index to correct MRN candidate; auto-populate order record; flag
  incomplete orders with the specific missing element (drives 1.1.1.D1)
- Prevents: unlinked/illegible orders, FM-DUPMRN (via match-confidence gating)
- Improves: order-to-appointment lag, scheduling accuracy
- Guardrails: MRN attach below confidence threshold → human queue; signature/completeness
  determinations audited via sampling

### UC-01-02 Identity Resolution & Duplicate MRN Prevention
- PAT-MATCH + PAT-PRED | A1 (merge always human) | R1
- Targets: 1.1.2.A1, 1.2.1.A3 | Trigger: EVT-SCHED, EVT-ARRIVAL
- Function: probabilistic record linkage at every create/search; real-time "likely duplicate" warning
  with match evidence; nightly MPI duplicate-candidate feed to HIM
- Prevents: FM-DUPMRN | Improves: KPI-REGQA
- Guardrails: never auto-merge; merge recommendations reviewed by HIM MPI analyst (1.2.1.D1)

### UC-01-03 Insurance Card Capture & Plan Mapping AI
- PAT-IDP + PAT-PRED | A3 | R2
- Targets: 1.2.2 | Trigger: card image received
- Function: OCR card front/back; extract payer, member ID, group; predict correct internal plan code
  from card text + payer master history (the plan-mapping step humans get wrong most)
- Prevents: FM-PLANMAP | Improves: KPI-VERIF-RATE, eligibility denial rate
- Guardrails: low-confidence mappings → verifier queue; mapping-accuracy audit vs downstream denials

### UC-01-04 Eligibility Orchestration Engine
- PAT-RULES + PAT-RPA | A4 | R4
- Targets: 1.3.1 | Trigger: EVT-SCHED, T-3 days, EVT-ARRIVAL
- Function: schedule and run 270/271 at all required checkpoints; parse 271 into structured
  benefits; detect plan-product changes (1.3.1.D2) and auto-retrigger auth determination; fall
  back to portal-scraping bots when RTE unavailable (1.3.2)
- Prevents: FM-ELIGLAPSE, FM-PLANMAP (change detection) | Improves: KPI-VERIF-RATE
- Guardrails: unparseable/conflicting 271 → verifier queue with structured discrepancy summary

### UC-01-05 Coverage Discovery Sweep
- PAT-MATCH + PAT-PRED | A3 | R2
- Targets: 1.3.5 | Trigger: self-pay classification, inactive-coverage result
- Function: batch-probe payer eligibility (demographic permutations), Medicaid files incl.
  retroactive spans; validate hits via 270/271 before attaching; rank by billability
- Prevents: missed billable coverage (self-pay leakage) | Improves: KPI-SELFPAYYIELD, KPI-NCR
- Guardrails: coverage attach requires validated 271; false-attach rate monitored (mis-attach
  creates FM-COB)

### UC-01-06 COB/MSP Primacy Inference
- PAT-RULES + PAT-PRED | A1 | R1
- Targets: 1.2.4, 1.3.4 | Trigger: multiple active coverages detected
- Function: infer probable primacy from MSPQ answers, employment data, 271 other-coverage flags,
  accident indicators; present recommended coverage order with rationale; draft payer COB
  update requests
- Prevents: FM-COB | Improves: COB denial rate, KPI-CLEANCLAIM
- Guardrails: primacy set by human on recommendation; MSP determinations logged for audit

### UC-01-07 Auth Requirement Determination Engine
- PAT-RULES + PAT-PRED + PAT-RPA | A3 | R1
- Targets: 1.4.1 | Trigger: EVT-SCHED, plan change (1.3.1.D2)
- Function: maintain payer auth-requirement grid by continuously mining payer bulletins/portal
  rules (with UC-11-03); answer required/not-required per CPT+payer+site in real time; when
  "not required," auto-capture and store dated proof evidence (1.4.1.A3)
- Prevents: FM-NOAUTH | Improves: KPI-AUTH-RATE, auth denial rate
- Guardrails: ambiguous/conflicting rule → verify via portal/278 before clearing; grid changes
  versioned with source citation

### UC-01-08 Auth Submission Agent
- PAT-AGENT + PAT-LLM + PAT-RPA | A2 | R1
- Targets: 1.4.2 | Trigger: auth-required determination
- Function: assemble clinical packet (pull order, notes, prior treatment via NLP), pre-answer payer
  questionnaire from chart evidence, stage submission via portal/278; submit on human approval;
  auto-capture tracking number
- Prevents: FM-NOAUTH, submission delay | Improves: auth turnaround, KPI-AUTH-RATE
- Guardrails: clinical assertions cite chart source; human reviews packet before submission (A2);
  questionnaire answers never fabricated — unanswerable items flagged

### UC-01-09 Auth Status Tracking Bots
- PAT-RPA | A4 | R4
- Targets: 1.4.3 | Trigger: pending-auth inventory, T-48h escalation clock
- Function: poll portals/278 on cadence; post statuses; auto-escalate pending-at-T-48h to human
  with payer expedite script; capture approval details structured (number, CPTs, units, span)
- Improves: auth turnaround, % cleared before service
- Guardrails: portal-change failures alarm to fleet ops (UC-14-04); no silent drops

### UC-01-10 Auth-to-Service Reconciliation Matcher
- PAT-RULES + PAT-MATCH | A3 | R1
- Targets: 1.4.6 | Trigger: coding finalized (EVT-CODED), schedule change (1.1.4)
- Function: compare performed CPT/units/date/site to authorization; auto-clear exact matches;
  generate payer auth-update request drafts for deviations; hold claim release on mismatch
- Prevents: FM-NOAUTH (mismatch variant) | Improves: auth-related denial rate, KPI-CLEANCLAIM
- Guardrails: claim-hold release on unresolved mismatch requires human decision (1.4.6.D1)

### UC-01-11 Medical Necessity Screening & Dx Gap Assist
- PAT-RULES + PAT-NLP | A1 | R1
- Targets: 1.5.1 | Trigger: order + scheduling
- Function: run NCD/LCD/payer-policy necessity edits pre-service; when failing, surface
  chart-supported candidate diagnoses to the ordering provider for confirmation (never auto-add
  a diagnosis); auto-generate ABN with correct reason/cost when provider confirms none apply
- Prevents: FM-MEDNEC | Improves: necessity denial rate, ABN compliance
- Guardrails: diagnosis addition is a provider act only; candidate dx must cite chart evidence

### UC-01-12 Estimate Accuracy Engine
- PAT-PRED | A3 | R3
- Targets: 1.6.1 | Trigger: EVT-SCHED, benefits verified
- Function: predict expected charges from service history models (not just CDM), apply contract
  allowables and live accumulators; produce confidence-scored estimate; monitor estimate-vs-final
  variance and retrain
- Prevents: FM-PATIENTWRONGBILL precursors, GFE dispute exposure | Improves: KPI-ESTIMATE-ACC, KPI-POS-CASH
- Guardrails: low-confidence → range disclosure per 1.6.1.D1; GFE regulatory content validated by rules

### UC-01-13 Financial Clearance Risk Scoring & Routing
- PAT-PRED + PAT-OPT | A3 | R2
- Targets: 1.7.1 | Trigger: clearance checkpoint dates
- Function: score accounts on clearance completeness × financial risk × service value; auto-clear
  complete/low-risk; route high-risk to counselors ranked by intervention value; forecast
  day-of-service uncleared volume
- Improves: KPI-CLEARANCE, counselor yield
- Guardrails: defer/reschedule recommendations (1.7.1.D1) always human-decided

### UC-01-14 Conversational Pre-Registration & Intake
- PAT-CONV | A3 | R3
- Targets: 1.2.3, 1.2.1 | Trigger: T-N outreach window, incomplete pre-check-in
- Function: two-way SMS/voice/portal agent completes demographics, card capture, MSPQ prompts,
  estimate delivery, POS pre-payment; hands off to human on confusion/distress/complex COB
- Improves: KPI-PREREG-RATE, KPI-POS-CASH
- Guardrails: automation disclosed; language access supported; consent/regulatory scripts
  rules-controlled, not generated

### UC-01-15 POS Next-Best-Action Prompting
- PAT-PRED + PAT-RULES | A0 | R3
- Targets: 1.8.1 | Trigger: EVT-ARRIVAL
- Function: present registrar with amount-to-request, discount/plan options the patient qualifies
  for, and compliant scripting; suppress requests where prohibited (EMTALA context)
- Improves: KPI-POS-CASH | Prevents: noncompliant collection conduct
- Guardrails: EMTALA suppression is hard-coded rules, not model-discretionary

### UC-01-16 Real-Time Registration QA
- PAT-RULES + PAT-ANOM | A3 (flagging) / A1 (correction) | R1
- Targets: 1.9.5, 1.9.2 | Trigger: registration save events
- Function: field-level validation at entry (kills defects before they exist); post-save anomaly
  scoring against denial-labeled history; auto-generate registrar-specific error feedback and
  QA scorecards; verify notice checklist completion (IMM/MOON/NSA) before encounter close
- Prevents: FM-NOTICEMISS, FM-PLANMAP, FM-COB (entry-time) | Improves: KPI-REGQA
- Guardrails: notice-delivery attestations remain human acts; QA scoring transparent to staff

### UC-01-17 No-Show & Reschedule Revenue Protection
- PAT-PRED + PAT-CONV | A3 | R3
- Targets: 1.1.4 | Trigger: no-show risk score, cancellation events
- Function: predict no-show risk; targeted confirmation outreach; on reschedule, auto-revalidate
  auth/referral date spans (feeds UC-01-10); work missed-without-reschedule list via outreach agent
- Improves: no-show rate, KPI-AUTH-RATE (date-span mismatches)
