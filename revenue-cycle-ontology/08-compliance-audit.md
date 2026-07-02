# RC-12 Compliance, Audit & Program Integrity

Defends against external audits, self-polices billing accuracy, returns overpayments lawfully,
absorbs regulatory change, and investigates/corrects compliance issues in revenue operations.

Roles: Compliance Officer, Billing Compliance Auditor, Audit Response Coordinator, Regulatory
Analyst, Privacy Officer, Legal Counsel. Systems: audit tracking system, release-of-information
workflow, compliance hotline/case management, policy library.

---

## 12.1 External Government Audit Response
Auditor types: RAC (recovery audit), MAC medical review incl. TPE (targeted probe & educate),
CERT, SMRC, UPIC/ZPIC (program integrity/fraud), OIG audits, state Medicaid RAC/MIC, MFCU.

- **A1.** Centralize intake of all audit correspondence (single point — missed letters are
  auto-losses); log record requests with deadlines
- **A2.** Validate request legitimacy and scope (auditor authority, lookback limits, record counts
  vs ADR limits)
- **A3.** Compile complete, organized record submissions; QA before release; submit trackably
  (esMD/portal/certified mail) within deadline
- **A4.** Track determinations; reconcile recoupment notices to specific claims
- **A5.** Appeal adverse findings through applicable path (Medicare 5-level for RAC/MAC denials)
  {links: 8.4.5.A2}; manage recoupment timing elections (rebuttal, redetermination-stage
  recoupment pause rules)
- **A6.** Analyze audit findings for pattern exposure: extrapolation risk, related-claim self-review
  decisions with counsel
- **D1.** Audit finding response?
  - Inputs: clinical/coding merit review, dollars, extrapolation stakes
  - ├─ Defensible → appeal every meritorious finding (high government-audit overturn rates at ALJ)
  - ├─ Valid finding → accept; refund; corrective action (12.6); assess 60-day related-claims duty (12.4)
  - └─ Mixed → line-by-line disposition
- **D2.** UPIC/fraud-unit contact or payment suspension?
  - ├─ Immediately engage counsel and compliance officer → privileged response track (not routine audit handling)

## 12.2 Commercial Payer Audit Response
- **A1.** Manage payer/contracted-vendor audits: DRG validation, itemized bill/charge audits,
  implant invoice audits, short-stay reviews, HEDIS/risk-adjustment chart pulls
- **A2.** Enforce contract audit clauses: lookback limits, notice requirements, audit fees, offset
  restrictions — reject out-of-scope requests in writing
- **A3.** Host on-site/remote audits with controlled record access; rebut findings with documentation
- **A4.** Negotiate audit settlements where appropriate; track audit-firm behavior patterns
  {feeds: 11.6, 11.1}
- **D1.** Audit request exceeds contractual rights?
  - ├─ Yes → formal objection citing contract; comply only to contracted scope
  - └─ No → standard response track

## 12.3 Internal Audit & Monitoring Program
- **A1.** Maintain annual risk-based work plan (OIG Work Plan-informed): E/M distribution, high-risk
  DRGs, inpatient-only, device credits, drug units, modifier usage (25/59), teaching rules, HCC
  support, provider-based billing, 340B modifiers
- **A2.** Execute audits with defined samples; score against standards; report findings with
  corrective action plans
- **A3.** Run continuous monitoring dashboards (statistical outlier detection on coding/billing
  patterns by provider/department)
- **A4.** Verify corrective action effectiveness with re-audits
- **D1.** Internal audit finds systematic overbilling?
  - ├─ Quantify → 12.4 overpayment duty; consider lookback sampling/extrapolation with counsel
  - └─ Isolated → correct claims; education (12.6)

## 12.4 Overpayment Identification & Refund (60-Day Rule)
- **A1.** Intake identified overpayments from all sources (7.4.2, 5.7.D1, 9.5.D1, 12.1–12.3, hotline)
- **A2.** Investigate and quantify with reasonable diligence (proactive quantification duty);
  document identification date — 60-day repayment clock
- **A3.** Refund via correct mechanism: claim adjustment/void, voluntary refund forms, MAC processes
- **A4.** Evaluate disclosure protocols where conduct concerns exist (OIG SDP, CMS SRDP for Stark)
  with counsel
- **A5.** Log all refunds centrally (audit trail of compliance with deadline)
- **D1.** Overpayment scope?
  - ├─ Simple posting/claim error → refund/adjust in normal course
  - ├─ Pattern across claims → structured lookback and batch refund with methodology memo
  - └─ Potential fraud/kickback/Stark implication → counsel-directed self-disclosure evaluation

## 12.5 Regulatory Change Management
- **A1.** Monitor rulemaking and effective dates: IPPS/OPPS/PFS annual rules, transmittals, NSA
  regs, price transparency, state billing/collection laws, telehealth policy changes
- **A2.** Impact-assess each change across domains; assign implementation owners and deadlines
- **A3.** Implement and verify (edits, CDM, forms, notices, workflows updated by effective date)
- **A4.** Train affected staff; retain implementation evidence

## 12.6 Billing Compliance Investigations & Education
- **A1.** Intake concerns (hotline, exit interviews, audit flags, self-reports); triage severity
- **A2.** Investigate under appropriate privilege; interview, sample claims, document findings
- **A3.** Execute corrective actions: repayment (12.4), process fixes, discipline, monitoring
- **A4.** Deliver role-based compliance education (coding, documentation, FA/collections law,
  EMTALA-adjacent financial conduct); track completion
- **A5.** Maintain policies/procedures library for all revenue cycle functions with review cycles

## 12.7 Privacy & Security in Billing Operations
- **A1.** Enforce minimum-necessary in billing disclosures, attachments, and agency data feeds
- **A2.** Manage business associate agreements for all revenue cycle vendors (10.5/10.6/14.5)
- **A3.** Process billing-related privacy events (misdirected statements, wrong-patient claims)
  through breach evaluation
- **A4.** Honor restriction requests affecting billing (e.g., self-pay restriction on disclosure
  to plan when paid in full out-of-pocket)

**Metrics:** audit win rate by auditor type, ADR response timeliness, audit takeback net of
appeals, internal audit accuracy trends, 60-day compliance rate, corrective action closure rate,
policy review currency.

## Relationships
- 12.1/12.2 `consume` records via HIM ROI; findings `feed-back-to` 4.x/5.x education and 8.5
- 12.4 `governed-by` ACA 60-day rule; `consumes` triggers from 7.4.2, 9.5, 5.7, 12.3
- 12.5 `feeds` 11.3 (payer-policy channel) and every operational domain's rule sets
- 12.7 `governs` data movement in 10.5/10.6/14.5 vendor operations
