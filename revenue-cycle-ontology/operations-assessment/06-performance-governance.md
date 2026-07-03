# AD-06 Performance & Financial Governance

How the revenue cycle is funded, measured, and held to account at the enterprise level. This
domain decides whether anything in the other five — or in the AI investment stack — gets
sustained resources and honest scorekeeping.

---

## Failure modes

### OFM-FG-01 — Cost-center myopia
The revenue cycle is budgeted purely as a cost to minimize; yield is invisible in the budget
conversation, so cuts that destroy net revenue look like savings.
**Signals:** budget targets set as % headcount reduction without yield modeling; denial spikes
following "efficiency" cuts; business cases evaluated on cost only.
**Damages:** the entire operation, cyclically; KPI-NCR vs KPI-CTC traded blindly.
**Degrades:** the economics gate (E) portfolio-wide — the investment loop starves regardless of
readiness; Wave-0 assets are unfundable as "overhead."

### OFM-FG-02 — KPI anarchy
Metrics are local dialects: three AR-days definitions, denial rates that differ by report
author, no change control on definitions.
**Signals:** meetings arguing about whose number is right; exclusions accreting silently;
benchmark submissions inconsistent with internal reports.
**Damages:** every decision made on the numbers; trust between finance and operations.
**Degrades:** `kpi_dictionary`; 13.1; anomaly detection, benefits measurement, and the packet's
headline numbers all inherit the noise.

### OFM-FG-03 — Close-driven operations
The month-end close dominates the calendar: reserves opaque and adjusted late, daily operations
distorted by close-week fire drills, analytics staff consumed by manual close production.
**Signals:** "we'll know after close"; reserve movements unexplained to operators; analysts
spending week one rebuilding the same workbooks.
**Damages:** 13.3; decision latency; analyst capacity.
**Degrades:** `realization_history`/`lineage` quality; reserve-model adoption (UC-13-02) has no
methodological baseline to shadow.

### OFM-FG-04 — Benchmark misuse
Benchmarks compared without definition or case-mix alignment; leadership whipsawed between
complacency ("we're top quartile!") and panic, both unfounded.
**Signals:** benchmark source/definition unstated in decks; peer group includes dissimilar
organizations; targets set from benchmarks nobody can reproduce.
**Damages:** target credibility; investment prioritization.
**Degrades:** `peer_benchmarks` facet quality; the surveillance use case (UC-12-03) compares
against the wrong reference class.

### OFM-FG-05 — Investment starvation cycle
No capital-ask discipline: requests are episodic, unquantified, and lose to clinical capital;
tech debt compounds; performance declines; credibility for the next ask declines with it.
**Signals:** last approved RCM capital request years old; asks framed as costs not yields;
"we'll fund it from operations" as default answer.
**Damages:** AD-04 wholesale; long-run performance trajectory.
**Degrades:** the entire investment loop — packets without a funding mechanism are literature.

## Best practices

### BP-FG-01 — Yield-and-cost joint governance
Revenue cycle governed on net realization *and* cost-to-collect together; every budget action
modeled for yield impact before approval; the value/cost models of this repository are the
tooling.
**Markers:** budget decisions carry yield-impact estimates; a cut that raised denials is
reversed with the same rigor it was made. **Prevents:** OFM-FG-01. **Enables:** the economics
gate and the loop's funding envelope.

### BP-FG-02 — One KPI dictionary under change control
Single governed definitions with owners, versioning, and change control; every report cites
definition IDs; exclusions documented and approved.
**Markers:** zero definitional disputes in executive meetings; benchmark submissions match
internal reporting. **Prevents:** OFM-FG-02, -04 (jointly with BP-FG-04). **Enables:**
`kpi_dictionary`; honest anomaly detection and benefits ledgers.

### BP-FG-03 — Continuous-close practices
Reserves estimated on transparent, documented methodology reviewed with operations monthly;
close automation frees analyst capacity; daily flash metrics decouple operations from the
close calendar.
**Markers:** close duration falling; reserve methodology explainable by operators; analysts'
close-week hours reallocated to analysis. **Prevents:** OFM-FG-03. **Enables:** lineage-grade
reserve modeling; UC-13-02's shadow-run baseline.

### BP-FG-04 — Benchmark hygiene
Benchmarks used only with definition mapping and case-mix adjustment; peer sets justified;
internal trend prioritized over external position.
**Markers:** benchmark appendix states source, definition, and adjustments; targets tie to
trend + benchmark, not benchmark alone. **Prevents:** OFM-FG-04.

### BP-FG-05 — Rolling investment roadmap with a credibility loop
A standing, quantified multi-year investment roadmap (the packet *is* the format); every funded
initiative reports realized value against its promise; realized-value track record compounds
into easier future asks.
**Markers:** capital asks reference the benefits ledger's history; approval cycle times
falling. **Prevents:** OFM-FG-05. **Enables:** the investment loop as the organization's
normal operating rhythm rather than a special program.

## Maturity anchors (AD-06)

| Level | Anchor |
|---|---|
| 0 | Cost-only budgeting; contested metrics; episodic asks |
| 1 | Yield discussed but not modeled; KPI dictionary drafted |
| 2 | Joint yield/cost governance; dictionary under change control; transparent reserves |
| 3 | Rolling investment roadmap; benefits ledger informing asks; benchmark hygiene routine |
| 4 | The investment loop is the operating rhythm; funding tracks demonstrated realization; finance and operations argue about actions, never numbers |
