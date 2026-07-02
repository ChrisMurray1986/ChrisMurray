# RC-13 Analytics, Reporting & Performance Management / RC-14 Master Data, Technology & Vendor Operations

RC-13 measures the cycle and closes the books; RC-14 keeps the data, systems, automation, EDI,
and vendors that every other domain runs on.

---

# RC-13 Analytics, Reporting & Performance Management

Roles: RC Analytics Manager, Data Analyst, Decision Support, Finance/Reimbursement Analyst.
Systems: EDW/data platform, BI tools, cost accounting, contract engine outputs, benchmarking
services (HFMA MAP, peer data).

## 13.1 KPI Definition & Data Governance
- **A1.** Maintain KPI dictionary with exact formulas and source-of-truth mappings (e.g., HFMA MAP
  keys: net days in AR, aged AR %, POS cash, DNFB/DNFC days, clean claim rate, initial denial
  rate, cost to collect, net collection %)
- **A2.** Govern definitions across systems (one definition of "denial", "touch", "clean claim")
- **A3.** Certify data feeds and reconcile analytics totals to patient accounting system of record
- **D1.** Metric moved — real or definitional?
  - ├─ Data/definition artifact → correct pipeline; annotate history
  - └─ Real change → operational drill-down (13.2)

## 13.2 Operational Reporting & Work-Driver Analytics
- **A1.** Produce daily operational packs: cash, DNFB, candidate-for-bill, edit/rejection inventory,
  denial intake, queue aging by team
- **A2.** Produce weekly/monthly management packs: KPI trends, payer scorecards, root-cause Pareto,
  productivity & quality by team/individual
- **A3.** Run drill-down analyses on demand (denial spikes, cash shortfalls, AR growth by cohort)
- **A4.** Support work-driver tuning: queue rule effectiveness, touch-yield analysis, automation
  candidate identification {feeds: 14.4}

## 13.3 Month-End Close & Revenue Recognition Support
- **A1.** Calculate contractual allowance and reserve estimates (payer/aging cohort realization
  models); support net revenue estimation
- **A2.** Reconcile: gross revenue, adjustments, payments, AR rollforward tie-out to GL
- **A3.** Estimate reserves for denials, audits (12.x exposure), settlements (11.7), bad debt
- **A4.** Produce close package with variance narratives (volume, rate, mix, collection performance)
- **A5.** Support external audit of net AR valuation (hindsight/lookback testing of estimates)
- **D1.** Hindsight testing shows estimation bias?
  - ├─ Yes → recalibrate reserve model; disclose per materiality
  - └─ No → maintain model

## 13.4 Predictive & AI-Enabled Analytics
- **A1.** Operate predictive models: denial risk at claim release, propensity to pay, missing-charge
  detection, auth-requirement prediction, expected-payment anomaly detection
- **A2.** Govern models: performance monitoring, drift detection, bias review (esp. patient-facing
  collection/FA models), human-override paths
- **A3.** Integrate model scores into work-queue prioritization (9.1.A2, 10.5.A1) with feedback capture
- **D1.** Model performance degrades?
  - ├─ Retrain/recalibrate → validate before redeploy
  - └─ Structural change (payer behavior shift) → rebuild features; interim rule fallback

## 13.5 Benchmarking & Executive Performance Review
- **A1.** Benchmark KPIs against peers (HFMA/vendor cohorts); normalize for payer mix and service mix
- **A2.** Run monthly revenue cycle executive review: KPI scorecard, initiative tracking, escalations
- **A3.** Quantify improvement-initiative ROI (before/after with control for mix)

---

# RC-14 Master Data, Technology & Vendor Operations

Roles: RC Systems Analyst, EDI Analyst, Automation Engineer, MDM Analyst, Vendor Manager,
IT Application Teams. Systems: HIS/EHR admin config, integration engine, RPA platform,
clearinghouse admin, dictionaries/masters.

## 14.1 Master Data Management
- **A1.** Maintain payer/plan master: payer entities, plan codes, financial class mapping, address
  and EDI routing, eligibility payer IDs — with governance on adds/changes (wrong mapping is a
  first-order denial cause {links: 1.2.2.A3})
- **A2.** Maintain provider master: NPIs, taxonomies, specialties, billing group linkages, enrollment
  status flags synchronized with 11.5
- **A3.** Maintain dictionaries: departments/cost centers, locations (incl. provider-based
  designations), service codes, transaction/adjustment code sets (with 7.4.1/8.6 governance),
  denial reason taxonomy (8.5.A1)
- **A4.** Run MPI hygiene support with HIM (duplicate detection/merge effects on billing)
- **D1.** Master data change requested?
  - ├─ Standard → governed change with effective date, testing, downstream sync (estimator, contract
    engine, MRF, statements)
  - └─ Emergency (payer route broken) → expedited change with post-hoc review

## 14.2 Revenue Cycle System Configuration & Maintenance
- **A1.** Maintain work-queue/edit/routing rules in patient accounting (build, test, version, deploy)
- **A2.** Maintain claim form configuration (837 mappings, payer overrides), statement config,
  auto-adjustment rules
- **A3.** Manage upgrades/patches with revenue-critical regression testing (claims, remit posting,
  estimates)
- **A4.** Intake/prioritize system change requests from operations; maintain build backlog
- **A5.** Support system conversions/migrations: legacy AR strategy (9.7.A4), parallel testing,
  cutover command center

## 14.3 EDI & Trading Partner Management
- **A1.** Manage clearinghouse relationship: connectivity, transaction routing tables, edit package
  versions, SLAs
- **A2.** Enroll transactions per payer: 837, 835, 270/271, 276/277, 278, EFT (CCD+) enrollments
  and re-enrollments on TIN/NPI/bank changes
- **A3.** Monitor transaction flows end-to-end (sent = acknowledged = adjudicated pipeline
  integrity); alarm on volume anomalies (silent file failures are catastrophic)
- **A4.** Resolve EDI incidents with payers/clearinghouse; maintain incident log and prevention

## 14.4 Bot/Automation Fleet Operations
- **A1.** Identify automation candidates from touch-yield analytics (13.2.A4): status checks,
  eligibility reruns, portal data pulls, simple edit fixes, remit retrieval
- **A2.** Build/test bots with credential governance and audit logging
- **A3.** Operate fleet: schedule, monitor success rates, exception routing to humans
- **A4.** Maintain against portal/UI changes (bot fragility management); measure net labor yield
- **D1.** Bot failure rate exceeds threshold?
  - ├─ Transient (portal change) → repair; replay failures
  - └─ Structural → retire/rebuild; return work to human queues explicitly (never silent drop)

## 14.5 Vendor Management & Outsourcing Oversight
- **A1.** Manage RC vendor portfolio: clearinghouse, coding vendors, early-out/agency (10.5/10.6),
  coverage discovery, estimation, denial/underpayment contingency firms, offshore/global BPO
- **A2.** Contract with performance SLAs, data security terms (BAAs — 12.7.A2), audit rights
- **A3.** Run vendor governance: scorecards, invoice validation against contingency terms,
  quality sampling of vendor-worked accounts
- **A4.** Manage transitions (vendor start/stop) with inventory reconciliation — no stranded accounts
- **D1.** Vendor underperformance?
  - ├─ Remediable → corrective action plan with milestones
  - └─ Persistent → transition plan; insource/replace; recover per contract

## 14.6 Business Continuity & Downtime Billing Procedures
- **A1.** Maintain downtime procedures: paper registration/charge capture kits, downtime forms,
  reconstruction workflows
- **A2.** Execute recovery after outages: backfill registrations/charges, reconcile completeness
  (census vs accounts vs charges), extended-outage claim strategies
- **A3.** Test downtime readiness periodically; maintain cyber-incident revenue playbook
  (payer notification, advance-payment programs, manual claim routes)

**Metrics:** master-data defect rate, EDI pipeline integrity (unacknowledged claim count),
bot success rate & net yield, vendor SLA attainment, change-request cycle time, downtime
recovery completeness.

## Relationships
- 14.1 masters `consumed-by` every domain; payer/plan master quality `gates` 1.2/1.3 accuracy
- 14.3 `gates` 6.3/7.1 transaction flow; 13.2 `feeds` 14.4 automation pipeline
- 13.3 `consumes` 7.3/9.7 outputs; 13.1 definitions `govern` all domain metrics
- 14.5 oversight `governs` outsourced execution of 5.x, 9.x, 10.5, 10.6 work
