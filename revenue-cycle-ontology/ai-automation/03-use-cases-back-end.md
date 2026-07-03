# UC-06-* … UC-10-* — Back End (Claims, Payments, Denials/AR, Patient Financial Services)

---

## UC-06-* Claims Production & Submission (RC-06)

### UC-06-01 Denial Risk Scoring at Claim Release
- PAT-PRED | A1 | R2
- Targets: 6.1.1, 6.2 | Trigger: candidate-for-bill
- Function: score every claim's denial probability by category before release, trained on the
  denial taxonomy (8.1.A2 labels); route high-risk claims to targeted pre-bill fix (the specific
  predicted defect) instead of letting them deny
- Prevents: FM-NOAUTH/FM-COB/FM-MEDNEC escapes at last gate | Improves: KPI-IDR, KPI-FPY
- Guardrails: holds bounded by DNFB budget; hold-vs-release trade-off thresholds owned by leadership

### UC-06-02 Edit Auto-Resolution Agent
- PAT-AGENT + PAT-RULES | A3 (rule-safe classes) / A1 (rest) | R1
- Targets: 6.2.3 | Trigger: edit failure
- Function: resolve deterministic edit classes autonomously (formatting, known payer mappings,
  data lookups from source systems); for judgment edits, assemble evidence and recommend;
  document every resolution action
- Improves: edit rework rate, KPI-CLAIMLAG, KPI-CLEANCLAIM
- Guardrails: auto-resolution class list is governed and versioned; modifier/code-content changes
  route to coding (never auto-applied to force claims through — compliance line)

### UC-06-03 Edit Rule Mining
- PAT-PRED + PAT-ANOM | A1 | R2
- Targets: 6.2.4 | Trigger: denial/rejection pattern detection
- Function: mine denial and rejection history for recurring defects with no corresponding
  pre-bill edit; auto-draft candidate edit rules with projected hit/prevention rates; detect
  false-positive edits (high hit, low change rate) for retirement
- Prevents: recurring preventable denials | Improves: KPI-IDR, edit precision
- Guardrails: rules deploy through 6.2.4 governance with testing

### UC-06-04 Submission Integrity Reconciler
- PAT-RULES | A4 (alerting) | R4
- Targets: 6.3.1.A2, 6.3.2 | Trigger: every batch cycle
- Function: reconcile generated = transmitted = 999-accepted = 277CA-accepted per claim; alarm
  on any claim without acknowledgment within SLA; auto-trace and resubmit never-received claims
- Prevents: FM-CLAIMDROP | Improves: KPI-REJRATE visibility, KPI-DAR
- Guardrails: resubmission duplicate-check before auto-resubmit

### UC-06-05 Rejection Auto-Triage & Repair
- PAT-NLP + PAT-AGENT | A3 (defined classes) | R1
- Targets: 6.3.3 | Trigger: 277CA/clearinghouse rejection
- Function: classify rejection reasons; auto-repair deterministic classes (ID formats, payer
  routing, demographic sync from source) and resubmit; route enrollment/eligibility classes to
  owning queues with context
- Prevents: FM-REJECTUNWORKED | Improves: KPI-REJRATE, KPI-CLAIMLAG
- Guardrails: repair classes governed; repeat-rejection accounts escalate to human

### UC-06-06 Timely Filing Sentinel
- PAT-RULES + PAT-OPT | A4 (alarming) / A3 (prioritization) | R2
- Targets: 6.5.3 | Trigger: continuous inventory scan
- Function: compute filing-clock consumption per claim from the contract matrix (11.2.A4);
  force-prioritize at-risk claims in all queues; preserve submission-proof artifacts
  automatically; protective-claim recommendations for blocked accounts
- Prevents: FM-TFL | Improves: timely-filing write-offs

### UC-06-07 Attachment Prediction & Auto-Assembly
- PAT-PRED + PAT-AGENT | A2 | R1
- Targets: 6.3.5 | Trigger: claim generation, ADR receipt
- Function: predict attachment-required claims from payer history before denial; auto-assemble
  attachment packages (op notes, invoices, EOBs) with claim linkage; track ADR deadlines with
  escalation
- Prevents: RFI denials, ADR deadline misses | Improves: KPI-FPY
- Guardrails: record releases follow minimum-necessary (12.7.A1); human approves packet content

### UC-06-08 COB/Secondary Claim Automation
- PAT-RULES + PAT-MATCH | A3 | R2
- Targets: 6.4.1, 6.4.2 | Trigger: primary EVT-REMIT posted
- Function: auto-generate secondary claims with primary adjudication data; validate balance math;
  detect crossover-confirmed claims and suppress duplicate billing; flag primary-adjudication
  errors for resolution before secondary release
- Improves: secondary lag, KPI-CLEANCLAIM | Prevents: crossover duplicate denials

---

## UC-07-* Remittance & Payment Posting (RC-07)

### UC-07-01 Intelligent Auto-Posting & Exception Resolution
- PAT-MATCH + PAT-PRED | A3 | R2
- Targets: 7.1.2 | Trigger: EVT-REMIT
- Function: raise auto-post match rates via probabilistic matching on imperfect identifiers
  (split claims, plan payments, resubmissions); learn exception-resolution patterns from analyst
  actions and auto-resolve recurring classes
- Prevents: FM-MISPOST | Improves: KPI-AUTOPOST, KPI-POSTLAG
- Guardrails: sub-threshold matches → human; dollar-threshold gates on auto-application (R2)

### UC-07-02 CARC/RARC Mapping Intelligence
- PAT-NLP + PAT-PRED | A1 | R1
- Targets: 7.1.3 | Trigger: new/unmapped code combination
- Function: classify new CARC/RARC/group-code combinations into the internal action taxonomy
  with recommended mapping; audit existing mappings against downstream outcomes (detect
  denial-coded-as-adjustment patterns statistically)
- Prevents: FM-DENIALHIDDEN (silent write-off of recoverable revenue) | Improves: denial capture completeness
- Guardrails: mapping changes human-approved (they redefine what counts as a denial)

### UC-07-03 Paper EOB / Correspondence IDP
- PAT-IDP | A3 | R2
- Targets: 7.2, 8.1.A1 | Trigger: lockbox/mail imaging
- Function: extract claim-level payments, adjustments, denial codes from paper EOBs and payer
  letters into structured postings; classify correspondence type (denial letter, audit request,
  refund demand) and route to owning workflow with deadlines stamped
- Prevents: FM-MISPOST, FM-APPEALMISS/FM-AUDITDEADLINE (letter routing) | Improves: KPI-POSTLAG
- Guardrails: batch balancing still enforced; low-confidence extractions → keying queue

### UC-07-04 Treasury Matching & Suspense Resolution
- PAT-MATCH | A3 | R2
- Targets: 7.3.1, 7.3.3 | Trigger: daily bank feeds
- Function: auto-match EFTs to 835s via TRN and fuzzy fallback; chase missing remits via bots;
  research unidentified cash against open-account universe with candidate ranking
- Prevents: aged suspense | Improves: KPI-SUSPENSE, reconciliation timeliness

### UC-07-05 Payment Variance Detection Coverage
- PAT-RULES + PAT-ANOM | A4 (flagging) | R2
- Targets: 7.4.2 | Trigger: every posting event
- Function: guarantee 100% of postings pass expected-vs-actual comparison (no unpriced claims);
  anomaly-detect variance patterns the contract engine misses (systematic small underpayments,
  new payer behavior); route by cause per 7.4.2.D1
- Prevents: FM-VARIANCEMISS | Improves: KPI-UNDERPAY identified
- Guardrails: unpriced-claim rate is itself an alarmed metric (engine coverage gap)

### UC-07-06 Recoupment Validation
- PAT-RULES + PAT-NLP | A1 | R2
- Targets: 7.4.3 | Trigger: EVT-TAKEBACK
- Function: validate every recoupment against notice requirements, contractual/state timeliness
  limits, and original-claim linkage; flag illegitimate take-backs with dispute recommendation
  and evidence
- Prevents: unlawful recoupments absorbed silently | Improves: recovery of disputed take-backs

---

## UC-08-* Denials Management & Appeals (RC-08)

### UC-08-01 Denial Auto-Classification & Root-Cause Attribution
- PAT-NLP + PAT-PRED | A3 | R4
- Targets: 8.1.A2–A3 | Trigger: EVT-DENIAL (all channels)
- Function: classify every denial into the internal taxonomy (category, clinical/technical,
  hard/soft) and attribute probable root-cause owner from account history (which upstream step
  failed); stamp appeal deadlines from the contract matrix at intake
- Prevents: FM-APPEALMISS (deadline stamping), misrouted denials | Improves: KPI-IDR accuracy,
  prevention-loop signal quality (8.5)
- Guardrails: classification accuracy audited; taxonomy changes governed

### UC-08-02 Overturn Probability & Appeal Prioritization
- PAT-PRED | A3 (ranking) | R2
- Targets: 8.2.A1, 8.4.1 | Trigger: classified denial inventory
- Function: score recoverable value × overturn probability × deadline urgency per denial;
  drive 8.2 routing and 8.4.1 pursue/write-off economics; batch systemic denials automatically
  (same payer/reason/period clustering)
- Improves: KPI-OVERTURN, appeal ROI, KPI-DENWO
- Guardrails: write-off recommendations execute through 8.6 approval matrix, never directly

### UC-08-03 Appeal Letter & Packet Generation
- PAT-LLM + PAT-AGENT | A2 | R1
- Targets: 8.4.2, 8.4.3, 8.4.4 | Trigger: appeal decision
- Function: draft appeal arguments citing the payer's own medical policy, contract clauses, and
  chart evidence with record pinpoints; assemble complete packet (claim, remit, auth proof,
  filing proof, policy excerpts); select strongest argument frame (e.g., wrong-criteria-set
  procedural argument per 8.4.3.D1); track submission and response SLA
- Improves: KPI-OVERTURN, appeal throughput (the highest-leverage LLM use case in the cycle)
- Guardrails: human (nurse/appeals specialist per denial class) approves before submission;
  every citation verified against source (no hallucinated policy text — hard validation);
  clinical assertions must carry record citations

### UC-08-04 Rebill-Loop & Stuck-Account Breaker
- PAT-ANOM | A0 | R4
- Targets: 8.3.D1, 9.1.D1 | Trigger: touch-history analysis
- Function: detect accounts cycling through resubmission/touch patterns without state progress;
  force break-the-pattern review with full history summary and recommended escalation channel
- Prevents: FM-REBILLLOOP | Improves: touch yield, KPI-AR90

### UC-08-05 Prevention Insight Miner
- PAT-PRED + PAT-LLM | A1 | R4
- Targets: 8.5 | Trigger: weekly trend cycle
- Function: surface emerging denial patterns (new codes, payer spikes, defect-owner trends)
  with quantified dollars; auto-draft prevention actions routed to owners (edit candidate →
  UC-06-03, auth grid gap → UC-01-07, registration defect → UC-01-16); track each action's
  denial-rate impact to close the loop (8.5.A4)
- Improves: KPI-IDR trend, preventable-denial dollars
- Guardrails: this is the orchestrator of the prevention feedback circuit — its routing accuracy
  is audited quarterly

### UC-08-06 Appeal Outcome Verification
- PAT-RULES + PAT-MATCH | A3 | R2
- Targets: 8.4.6 | Trigger: appeal decision received
- Function: match overturn decisions to subsequent payments; verify payment equals the overturn
  determination (payers underpay wins); auto-chase unpaid overturns; release held patient
  balances on final resolution
- Improves: realized overturn dollars | Prevents: won-but-unpaid leakage

---

## UC-09-* AR Management & Follow-Up (RC-09)

### UC-09-01 Expected-Value Work Prioritization
- PAT-PRED + PAT-OPT | A3 | R4
- Targets: 9.1.A2–A3 | Trigger: continuous inventory refresh
- Function: rank all AR by expected collectible value × urgency (filing/appeal clocks from
  UC-06-06) × actionability; set payer-specific follow-up cadence from observed adjudication
  timing; suppress zero-yield touches (accounts that will resolve without intervention)
- Improves: KPI-DAR, touch yield, KPI-CASHGOAL
- Guardrails: suppression logic audited against missed-recovery outcomes

### UC-09-02 Claim Status Automation Fleet
- PAT-RPA + PAT-RULES | A4 | R4
- Targets: 9.2 | Trigger: follow-up cadence due
- Function: run 276/277 batches, portal bots, and IVR bots to determine claim status; map
  responses to next actions automatically (9.2.A2 mapping table) and execute the routing
  (paid→remit trace, denied→8.1 intake, pended→RFI supply, no-claim→resubmission trace)
- Improves: touch productivity, KPI-DAR | Prevents: status-check labor consuming analyst time
- Guardrails: unresolvable statuses route to human callers with full bot-gathered context

### UC-09-03 Underpayment Pattern Recovery
- PAT-ANOM + PAT-PRED | A1 | R2
- Targets: 9.4 | Trigger: variance inventory (UC-07-05 feed)
- Function: cluster variances by cause signature (fee schedule misapplication, DRG weight error,
  carve-out miss, lesser-of logic, stacked discounts); distinguish contract-load errors from
  payer errors (9.4.D1); auto-generate batch demand packages with calculation exhibits
- Prevents: FM-VARIANCEMISS downstream, FM-TERMSUNLOADED detection | Improves: KPI-UNDERPAY recovered
- Guardrails: load-error findings route to 11.2 before payer demands (no false demands)

### UC-09-04 Credit Balance Classification & Refund Automation
- PAT-PRED + PAT-RULES | A3 (classification) / A2 (refund execution) | R2/R1
- Targets: 9.5 | Trigger: credit balance creation
- Function: classify each credit as true-credit vs posting-error with cause (duplicate payment,
  dual-primary, over-posting); auto-correct posting errors; stage validated refunds with
  government-payer 60-day clock stamping and CMS-838 reporting feeds
- Prevents: FM-CREDITAGE, FM-60DAY | Improves: KPI-CREDITDAYS
- Guardrails: refund release requires approval per matrix; government overpayments logged to
  central 12.4 register automatically

### UC-09-05 Special-Account Event Monitoring
- PAT-RULES + PAT-MATCH | A3 (flagging) | R2
- Targets: 9.8 | Trigger: external data feeds
- Function: monitor bankruptcy filings, death registries, and estate/probate records against AR
  inventory; auto-apply collection stops on bankruptcy notice (automatic stay compliance);
  calendar proof-of-claim and probate deadlines; track WC/liability lien perfection deadlines
- Prevents: stay violations, missed lien/probate deadlines | Improves: special-account recovery
- Guardrails: collection stop is auto (compliance-safe direction); resumption is human-decided

### UC-09-06 Aged-AR Disposition Modeling
- PAT-PRED | A1 | R2
- Targets: 9.7 | Trigger: aging review cycles
- Function: model residual collectibility per aged cohort; recommend disposition (continue,
  vendor, write-off) with expected-value math; verify bad-debt transfer gate conditions
  (statement cycle, FA screening, no disputes) automatically before placement eligibility
- Prevents: FM-FA-MISS (gate verification), premature write-offs | Improves: KPI-AR90, KPI-NCR

---

## UC-10-* Patient Financial Services (RC-10)

### UC-10-01 Patient Liability Verification Gate
- PAT-RULES | A4 (blocking) | R1
- Targets: 10.1.D1 | Trigger: statement qualification
- Function: hard gate before first statement — verify remit liability coding, COB completeness,
  no active payer defect, NSA protection screen (UC-10-06); block dunning where payer work
  remains
- Prevents: FM-PATIENTWRONGBILL (the most trust-destroying failure mode) | Improves: KPI-COMPLAINTS
- Guardrails: gate rules governed; blocks visible in queue with resolution routing

### UC-10-02 Statement Channel & Timing Optimization
- PAT-PRED + PAT-OPT | A3 | R3
- Targets: 10.1.A2–A4 | Trigger: statement cycle
- Function: optimize channel (paper/e-statement/text), timing, and message framing per patient
  response history; manage returned-mail → address-hygiene → skip-trace pipeline automatically
- Improves: statement-to-payment conversion, statement cost
- Guardrails: required regulatory content (501(r) FA notice) rules-enforced on every variant

### UC-10-03 Conversational Billing Agent
- PAT-CONV + PAT-LLM | A3 | R3
- Targets: 10.2 | Trigger: inbound patient contact (chat/voice/portal), off-hours coverage
- Function: authenticate; explain balances line-by-line in plain language (linking payments,
  insurance actions, estimate history); take payments; set standard-matrix payment plans;
  initiate FA screening; produce itemized bills; escalate disputes, distress, and complex COB
  to humans with full context
- Improves: KPI-COMPLAINTS, service cost, after-hours resolution
- Guardrails: automation disclosed; never negotiates outside policy matrix; dispute/hardship
  triggers immediate human path; conversation QA sampling (10.2.A5)

### UC-10-04 Payment Plan Default Prediction & Rescue
- PAT-PRED + PAT-CONV | A3 | R3
- Targets: 10.3.A3 | Trigger: plan payment events, decline signals
- Function: predict plan default before it happens (decline patterns, payment timing drift);
  proactive outreach with restructure offers within policy matrix; retry/dunning optimization
  for stored-card failures
- Improves: KPI-PLANDEFAULT, self-pay yield

### UC-10-05 Presumptive Financial Assistance Scoring
- PAT-PRED | A2 | R1
- Targets: 10.4.A4, 10.1.D2 | Trigger: pre-bad-debt gate, non-responder cycles
- Function: score FA likelihood from consented credit/socioeconomic data and Medicaid-proxy
  signals; recommend presumptive charity before any placement; verify 501(r) ECA timing
  conditions automatically
- Prevents: FM-FA-MISS | Improves: charity vs bad-debt classification accuracy
- Guardrails: model bias review mandatory (adverse-impact testing across demographics —
  GOV-06); presumptive denial never automated (only presumptive approval); human approves
  write-off application per 8.6 matrix

### UC-10-06 NSA Protection Classifier
- PAT-RULES + PAT-PRED | A3 (flagging + liability capping) | R1
- Targets: 10.7.A1–A2 | Trigger: OON claim adjudication, statement qualification
- Function: detect NSA-protected scenarios (OON emergency, OON ancillary at INN facility,
  absent/invalid consent); cap patient liability at in-network cost-share automatically; route
  provider-payer difference to IDR workflow (8.4.5.A5); track state-law overlays
- Prevents: FM-PATIENTWRONGBILL (NSA variant), balance-billing violations
- Guardrails: protection determination errs toward patient (false-positive-protective); overrides
  require compliance sign-off

### UC-10-07 Agency Oversight Analytics
- PAT-NLP + PAT-ANOM | A0/A1 | R3
- Targets: 10.5.A4, 10.6.A3–A6 | Trigger: agency remit/activity files, call recordings
- Function: QA-score vendor call recordings at scale (script compliance, prohibited practices,
  complaint precursors); reconcile agency inventories/remits automatically; anomaly-detect
  commission and net-back drift; flag FA-eligible accounts discovered in placed inventory for
  recall
- Prevents: vendor conduct violations, FM-FA-MISS (post-placement) | Improves: KPI-AGENCYNETBACK,
  KPI-COMPLAINTS

### UC-10-08 GFE Dispute & Estimate Variance Monitor
- PAT-RULES | A3 (flagging) | R2
- Targets: 10.7.A4, 10.2.D1 | Trigger: final billing vs stored GFE/estimate
- Function: compare every self-pay final bill to its GFE ($400 dispute threshold) and insured
  bills to estimates; pre-flag variance accounts for proactive outreach before dispute; assemble
  documentation packages for initiated SDR disputes
- Prevents: dispute losses, estimate-trust erosion | Improves: KPI-ESTIMATE-ACC feedback loop
