# AD-02 Process Improvement & Performance Management

Whether the organization can see its own performance truthfully and improve it durably. This
domain determines if fixes stick — including every fix the AI stack proposes.

---

## Failure modes

### OFM-PI-01 — Firefighting culture
All capacity is consumed working the backlog; prevention is perpetually next quarter. The same
denials are worked, appealed, and re-caused forever.
**Signals:** overtime as steady state; "we can't spare anyone for root cause"; backlog age
charts that saw-tooth but never trend down.
**Damages:** 8.5 prevention circuit; KPI-IDR never improves; FM-REBILLLOOP at org scale.
**Degrades:** every `feeds-back-to` edge in the base ontology; the label pipeline's purpose.

### OFM-PI-02 — No standard work
Outcomes depend on who touches the account. Ten reps, ten methods, tribal knowledge as
infrastructure.
**Signals:** "ask Maria, she knows payer X"; onboarding = shadowing; identical accounts
resolved differently on sampled review.
**Damages:** quality variance everywhere; training cost; audit defense.
**Degrades:** the W-dimension wholesale — the cardinal rule ("never automate W0/W1") parks half
the automation catalog behind this single failure mode.

### OFM-PI-03 — Watermelon metrics
Dashboards green, reality red. Definitions drift by author; exclusions accumulate until the
metric measures nothing.
**Signals:** three AR-days figures in one meeting; "that number excludes…" explanations;
frontline disbelief of official reports.
**Damages:** every management decision made on the numbers; KPI-* integrity.
**Degrades:** `kpi_dictionary`; UC-13-01 anomaly detection amplifies noise; benefits ledger
credibility (09 §4) is stillborn.

### OFM-PI-04 — Root-cause theater
"Root cause analysis" stops at *payer behavior* or *user error*; five-whys never crosses an
internal process boundary; the corrective action is always re-education.
**Signals:** RCA documents blaming payers; identical denials recurring after "closure";
retraining as the universal fix.
**Damages:** denial prevention (8.5); repeat-defect rates.
**Degrades:** `denial_labels` attribution — the ML label pipeline inherits garbage causality and
models learn to predict the wrong owner (FM-AI-07's organizational twin).

### OFM-PI-05 — Improvement without control
Projects succeed and decay: the fix works for 90 days, the control plan doesn't exist, and next
year the same project runs again with a new name.
**Signals:** "we fixed that in 2023" about a current problem; no re-audit calendar; benefits
claimed at go-live, never at month 12.
**Damages:** improvement ROI; organizational faith in projects.
**Degrades:** the true-up loop's premise — realized-value tracking (Play 6) needs controls that
hold.

### OFM-PI-06 — Volume worship
Productivity measured in touches, not resolutions. Reps optimize for activity: quick notes,
status checks, re-bills — the account ages anyway.
**Signals:** high touches/FTE with flat liquidation; "worked" accounts with no state change;
cherry-picking easy accounts.
**Damages:** 9.1 touch-yield economics; KPI-DAR; FM-REBILLLOOP.
**Degrades:** `touch_logging` data quality (touches recorded, outcomes not); poisons the
AR-prioritization training signal (UC-09-01).

### OFM-PI-07 — Inspection at the end
QA samples the final output — the claim, the letter — long after the defect was injected;
feedback reaches the source weeks later or never.
**Signals:** QA results reported monthly in aggregate; front-line staff unaware of their error
patterns; QA team seen as police, not coaches.
**Damages:** all QA programs; error-correction latency.
**Degrades:** source-point automation cases (UC-01-16 registration QA) lack the labeled
defect-at-origin data they train on.

## Best practices

### BP-PI-01 — Ring-fenced prevention capacity
A fixed share of operational capacity (commonly ~10%) permanently assigned to prevention squads
working the denial/defect taxonomy, protected from backlog raids by executive rule.
**Markers:** prevention squad staffing survives busy season; prevented-dollar runrate reported
beside worked-dollar. **Prevents:** OFM-PI-01. **Enables:** 8.5 circuit; gives UC-08-05's routed
actions a receiving team.

### BP-PI-02 — Standard work as infrastructure
Documented current-best-method per process, versioned, trained-to, and audited-to; deviations
treated as signals to investigate, not sins to punish.
**Markers:** standard-work library with owners and review dates; sampled work matches the
standard ≥90%. **Prevents:** OFM-PI-02. **Enables:** W2→W3; the single highest-leverage
enabler of the automation catalog.

### BP-PI-03 — Governed metrics and tiered huddles
One KPI dictionary under change control; daily team huddles → weekly domain reviews → monthly
executive review, each tier with defined escalation and decision rights.
**Markers:** metric definitions cited by ID; huddle boards show problems, owners, dates;
escalations resolve. **Prevents:** OFM-PI-03. **Enables:** `kpi_dictionary`; 13.1; honest
benefits measurement.

### BP-PI-04 — Root cause with owner attribution
Defect taxonomy with named owning functions (the same taxonomy as CAP-02); five-whys required
to cross at least one internal boundary; corrective actions beyond retraining mandatory.
**Markers:** repeat-defect rate tracked and falling; RCA library searchable; payer-fault RCAs
require evidence. **Prevents:** OFM-PI-04. **Enables:** trustworthy `denial_labels`; model
training data with true causality.

### BP-PI-05 — Control plans and 12-month benefit verification
Every improvement ships with a control metric, an owner, and a re-audit date; benefits are
claimed at month 12 against the baseline, not at go-live.
**Markers:** control-plan registry; decayed fixes trigger andon, not amnesia. **Prevents:**
OFM-PI-05. **Enables:** the benefit ledger and Play-6 true-up land on existing habit.

### BP-PI-06 — Resolution-based productivity
Productivity = accounts *resolved* or state-advanced, quality-gated; touch counts demoted to a
diagnostic. Work distribution prevents cherry-picking.
**Markers:** yield-per-touch tracked; account-state model defined ("what counts as progress").
**Prevents:** OFM-PI-06. **Enables:** clean `touch_logging` outcomes; UC-09-01's training
signal and its adoption case.

### BP-PI-07 — Source-point quality
QA moved to the point of defect injection: registration edits at save, coding checks pre-bill,
same-day feedback to the individual, coaching loops closed weekly.
**Markers:** defect-to-feedback latency <48h; individual error trends visible to the
individual. **Prevents:** OFM-PI-07. **Enables:** UC-01-16-class automation lands as an
amplifier of an existing habit instead of a foreign intrusion.

## Maturity anchors (AD-02)

| Level | Anchor |
|---|---|
| 0 | Pure firefighting; no standard work; metrics contested |
| 1 | Standards drafted; QA exists end-of-line; RCA blames externals |
| 2 | KPI dictionary governed; huddle tiers running; prevention squad piloted |
| 3 | Standard-work audits routine; owner-attributed defect taxonomy; control plans standard |
| 4 | Repeat-defect rate structurally declining; benefits verified at month 12 as habit; improvement capacity self-funding |
