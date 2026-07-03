# Function Assessment — RC-11 Contracting · RC-12 Compliance · RC-13 Analytics · RC-14 Data/Tech

Roles: ROLE-CONTRACT, ROLE-CRED, ROLE-ENROLL, ROLE-PAYERREL, ROLE-VBC, ROLE-COMPLIANCE,
ROLE-AUDITCOORD, ROLE-ANALYTICS, ROLE-SYSANALYST, ROLE-EDI, ROLE-AUTOENG, ROLE-VENDORMGR.

## RC-11 Payer Contracting, Credentialing & Enrollment

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-11.1-01 | Negotiations run on rate benchmarks alone; denial burden, auth friction, payment behavior unpriced (11.1.A2–A3) | JOC issues never reach the negotiation table; "good rates" from a payer that denies 15% | PBP-11.1-01 Total-cost-of-payer scorecards in every negotiation (hardened-by UC-11-05) |
| PFM-11.1-02 | Amendments and term dates slip by (11.1.D2) → FM-AMENDMISS | Evergreen rollovers unexamined; objection windows found expired | PBP-11.1-02 Contract calendar with notice-period gates; hardened-by UC-11-02 |
| PFM-11.2-01 | Contract loads unverified against source (11.2.A1–A2) → FM-TERMSUNLOADED, false variance | Engine trusted until an analyst proves it wrong; variance queue polluted | PBP-11.2-01 Parallel-price verification on load and amendment; hardened-by UC-11-01 |
| PFM-11.2-02 | Filing/appeal limits per contract never codified (11.2.A4) → feeds FM-TFL, FM-APPEALMISS | Deadlines live in analyst memory (see PFM-6.5-02, PFM-8.1-03) | PBP-11.2-02 Term matrix maintained as master data with change control |
| PFM-11.3-01 | Payer bulletins read by whoever subscribes; changes reach ops after denials do (11.3.A1–A3) | Policy-change denial waves; "since when?" meetings | PBP-11.3-01 Bulletin monitoring with routed implementation tasks and verified adoption; hardened-by UC-11-03 |
| PFM-11.4-01 | Expirables tracked in spreadsheets; lapses discovered by rejection (11.4.A4–A5, 11.5.A2) → FM-ENROLLGAP | Claims held for lapsed enrollment; revalidations missed | PBP-11.4-01 Expirables lifecycle with escalating alerts and claim-hold automation; hardened-by UC-11-04 |
| PFM-11.4-02 | Exclusion screening (OIG/SAM) periodic, not continuous (11.4.A5) | Annual batch checks; hires between checks unscreened | PBP-11.4-02 Continuous exclusion monitoring, compliance-routed hits |
| PFM-11.5-01 | Enrollment applications (855s, CAQH, delegated rosters) worked reactively; effective-date gaps eat revenue (11.5.A1–A3) → FM-ENROLLGAP | New providers seeing patients before enrollment effective; held-claim inventory by provider unknown | PBP-11.5-01 Enrollment pipeline started at signed offer with per-payer lead times; claim holds auto-applied and auto-released by effective date (hardened-by UC-11-04) |
| PFM-11.6-01 | JOCs are grievance sessions without dollarized issues or follow-through (11.6.A1–A3) | Same issues every JOC; no issue ledger | PBP-11.6-01 Dollarized issue inventory with aging and resolution tracking; escalation ladder used |
| PFM-11.7-01 | VBC settlements accepted as issued; attribution/rosters unreconciled (11.7.A2–A3) | Settlement checks deposited unverified; roster churn invisible | PBP-11.7-01 Independent settlement modeling and monthly roster reconciliation; hardened-by UC-11-06 |

## RC-12 Compliance, Audit & Program Integrity

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-12.1-01 | Audit requests enter through many doors; deadlines tracked locally (12.1.A1–A2) → FM-AUDITDEADLINE | ADRs found in department inboxes; technical-denial losses for non-response | PBP-12.1-01 Single audit intake with deadline register; hardened-by UC-12-01 |
| PFM-12.1-02 | Record submissions incomplete — the packet loses what the care earned (12.1.A3) | Findings overturned on appeal *with the same record*, better assembled | PBP-12.1-02 Completeness checklists per audit type with QA before release; hardened-by UC-12-02 |
| PFM-12.1-03 | Findings unappealed by default; extrapolation math unexamined (12.1.A5–A6, D1) | Auto-accepted findings; universe/sample never challenged | PBP-12.1-03 Appeal-vs-accept economics per finding; statistician review of extrapolations (UC-12-06) |
| PFM-12.2-01 | Commercial audits handled like government audits — contract audit clauses (lookback limits, ADR caps, offset rules) never invoked (12.2.A1–A3) | Out-of-scope record pulls fulfilled; recoupments beyond contractual lookback absorbed | PBP-12.2-01 Contract-clause validation on every commercial audit request before fulfillment (terms from 11.2 matrix) |
| PFM-12.3-01 | Monitoring plan = last year's plan; risk-blind sampling (12.3.A1–A2) | Work plan static while services/codes shift | PBP-12.3-01 Risk-ranked annual plan refreshed by surveillance signals (UC-12-03) |
| PFM-12.4-01 | Overpayments identified in silos; no central register or clock (12.4.A1–A2) → FM-60DAY | Refunds ad hoc; identification dates unrecorded | PBP-12.4-01 Central register with 60-day clocking from every source (12.4 as designed); hardened-by UC-12-04 |
| PFM-12.5-01 | Regulatory changes tracked by newsletter forwarding (12.5.A1–A2) | Implementation evidence absent; effective dates missed | PBP-12.5-01 Change register with owners, deadlines, and adoption verification; hardened-by UC-12-05 |
| PFM-12.6-01 | Investigations punish individuals; systemic causes untouched; education generic (12.6.A1–A3) | Repeat findings in the same process with different names attached; annual compliance training as the universal remedy | PBP-12.6-01 Investigation standard requires process-level cause analysis (OFM/PFM layers) before individual attribution; education targeted from findings |
| PFM-12.7-01 | Billing staff access broad by convenience; minimum-necessary unenforced (12.7.A1–A2) | Role-based access reviews stale; ROI releases over-inclusive | PBP-12.7-01 Access recertification cadence; release templates scoped to request |

## RC-13 Analytics, Reporting & Performance

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-13.1-01 | Metrics computed per-report from raw tables; definitions re-derived each time (13.1.A1–A2) | Two analysts, two denial rates; logic in personal SQL | PBP-13.1-01 Certified metric layer (semantic definitions once); reports consume, never re-derive |
| PFM-13.2-01 | Reporting describes, never directs: no work-driver linkage (13.2.A2–A4) | Dashboards admired; queues unchanged | PBP-13.2-01 Every executive metric decomposes to a workable driver list; hardened-by UC-13-01 |
| PFM-13.3-01 | Reserve methodology opaque to operations; hindsight never tested (13.3.A1, D1) | Surprises at year-end audit; operators distrust net numbers | PBP-13.3-01 Documented methodology, hindsight-tested annually, explained to operators; hardened-by UC-13-02 |
| PFM-13.4-01 | Models deployed without owners or refresh plans (13.4.A2) | Propensity scores from 2022 still routing work | PBP-13.4-01 Model inventory with owners, refresh cadence, and performance floors (UC-13-04's manual precursor) |
| PFM-13.5-01 | Benchmarks quoted without definition alignment (13.5.A1–A2) | See OFM-FG-04 — this is its process-level instance | PBP-13.5-01 Definition-mapped benchmarking only (BP-FG-04) |

## RC-14 Master Data, Technology & Vendor Operations

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-14.1-01 | Payer/plan master edited live under pressure (14.1.A1, D1) → FM-PLANMAP at the table | Mapping changes untracked; Friday-afternoon edits precede Monday denial spikes | PBP-14.1-01 Master-data change control with effective dating and rollback; hardened-by UC-14-01 |
| PFM-14.2-01 | Config changes ship without regression checks; work-queue logic drifts (14.2.A1–A3) | Post-change denial/edit spikes correlate with release dates, nobody connects them | PBP-14.2-01 RC-specific change calendar + post-change monitoring windows; hardened-by UC-14-02 |
| PFM-14.3-01 | EDI monitored by absence-of-complaints (14.3.A1–A3) → FM-EDISILENT | File failures discovered by cash dips; trading-partner tickets stale | PBP-14.3-01 Transaction-flow telemetry with volume baselines and alarms; hardened-by UC-14-03 |
| PFM-14.4-01 | Bots owned by their builders; failures return work to no one (14.4.A2–A3) → FM-BOTSILENT | See OFM-ET-04 — process-level instance; exception queues unmapped | PBP-14.4-01 Fleet standards: registry, monitoring, named hand-back queues; hardened-by UC-14-04 |
| PFM-14.5-01 | Vendor SLAs reviewed at renewal only (14.5.A2–A3) | Quarterly reviews skipped when busy — which is always | PBP-14.5-01 Standing vendor scorecards from own-system data (BP-VN-02); hardened-by UC-14-07 |
| PFM-14.6-01 | Downtime procedures exist, drilled never (14.6.A1–A2); reconstruction improvised | Post-outage charge gaps found months later | PBP-14.6-01 Annual downtime drill including revenue reconstruction to census; hardened-by UC-14-06 |
