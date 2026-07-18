# Decision Log — 2026-07 Digital Twin Layer

Added a fifth layer, `digital-twin/`: a deterministic monthly flow simulation of the
whole revenue cycle operation for scenario analysis (workflow redesign, AI/automation
deployment, staffing change → financial, productivity, and patient/caregiver
experience impact). Shipped baseline: a ~$10B NPR archetype IDN on single-instance
Epic hosted on AWS with Snowflake + Databricks analytics, per the commissioning
request. Scope decisions below; the layer's own README carries the meta-model.

## Structural decisions

| Decision | Choice | Why |
|---|---|---|
| Simulation form | Deterministic monthly fluid-flow over a 22-stage pipeline, not discrete-event/stochastic | Runs are diffable records (repo invariant 5); calibration targets are monthly-reporting quantities; DES micro-realism would demand data no site has and break replayability |
| Grounding | Stages bind process IDs, pools bind `ROLE-*`, denial causes bind `FM-*` + owner stage, outputs bind `KPI-*`, scenario AI interventions bind `UC-*` | Same ID discipline as every other layer; the twin adds **dynamics**, not new semantics |
| Relationship to the value model | Complementary, not a replacement: `value.py` sizes steady-state pools per UC; the twin simulates trajectories, capacity coupling, and experience | The two answer different questions; twin scenarios should stay consistent with pool sizes but are not derived from them |
| Denial mechanics | Initial denial rate decomposed into 10 causes, each scaled by its owner stage's `quality_index`; denied counts drive downstream labor | This is the load-bearing feedback loop (prevention feedback circuit, file 10 §master relationship): upstream quality shrinks back-end work — emergent, not asserted |
| Revenue accounting | Leakage-inclusive envelope: baseline reproduces stated NPR exactly; scenario impact = Δ leakage vs baseline run | Prevents double-counting value already embedded in NPR — same discipline as the value model's finite pools |
| Experience | Two composite indices (PXI patient, CXI caregiver) computed from operational state (capacity, backlog, automation share, rework, provider burden, change load) with explicit worst/best bounds in config | Experience becomes a simulated output that can *fall* (e.g., an under-staffed redesign) rather than a promised benefit |
| Vendor stack | `data-bindings-epic-aws.yaml` (as_of-stamped, confidence-flagged) maps config parameters to Clarity/Caboodle → Snowflake marts → Databricks calibration jobs | Invariant 1: neutral core governs; Epic/AWS/Snowflake/Databricks live only in the disposable binding layer |
| Governance | Scenario `ai_automation` interventions declare autonomy/risk; engine validates UC IDs against `gate-vectors.yaml` and warns on autonomy-ceiling violations | The ceiling rule is the central governance constraint (invariant 2) and must survive into simulation |

## Added

- `digital-twin/twin.py` — engine (Python 3 + PyYAML; ~700 lines).
- `digital-twin/twin-config.yaml` — archetype baseline: 3 segments (~13.9M
  accounts/yr ≈ $10.06B NPR), 19 staffing pools (2,510 FTE incl. overhead), 22
  stages, 10 denial causes, 14 levers, PXI/CXI component model. Calibrated so all
  pools land at 73–96% utilization, AR ≈ 50 days, IDR 11.5%, denial write-off ≈ 2.4%
  NPR, cost-to-collect ≈ 2.7%.
- `digital-twin/data-bindings-epic-aws.yaml` — stack bindings + calibration loop.
- `digital-twin/scenarios/` — SCN-01 (AI wave, 8 governed UC deployments), SCN-02
  (pure staffing rebalance), SCN-03 (pure workflow redesign), SCN-04 (sequenced
  transformation program).
- `digital-twin/examples/` — generated baseline/scenario reports, comparison, monthly
  CSVs (records; regenerate rather than edit).

## Calibration notes (what the shipped baseline asserts)

Baseline appeal rates were rebalanced during calibration (weighted ≈ 9.6% of denied
claims) so the appeals pool sits at ~88% utilization rather than structurally
underwater; cause-level recovery rates were set so weighted recovery ≈ 0.80 → denial
write-off ≈ 2.4% NPR (deliberately worse than the example-org profile's 2.0% —
this archetype carries improvement headroom, which is the point of a twin). The
SCN-03 build surfaced the intended behavior that redeploys must be sized to the
work shift: an under-staffed single-pass-clearance redesign drives pre-registration
to ~144% utilization and *drops* both experience indices below baseline.

## Addendum (same month) — payer response dynamics (config v1.0 → v1.1)

Payer behavior made endogenous. `payer_dynamics:` in `twin-config.yaml` defines five
counter-move rules (PR-01…PR-05: discretionary-category denial re-tightening, appeal
slow-walk/documentation friction, auth-surface expansion, payment/records-request
friction, downcode-and-underpay pressure), each a deterministic intensity state
machine: trigger threshold on a provider-behavior metric, activation lag, ramp,
decay, capped magnitude.

Key design decisions:

- **Triggers watch provider-intent parameters** (baseline + scenario effects, before
  payer response), not net outcomes — the baseline run never self-triggers, and the
  loop cannot oscillate. Payers respond to observable provider posture (submission
  quality, appeal success, automation velocity), which is what the intent parameters
  encode.
- **Grounding**: rules, lags (4–6 months), and boundedness taken from the wargame
  instruments (`whats-right-conference-2026/wargame-2/`): payers deploy decision
  automation 2–3 years ahead of providers at near-zero marginal denial cost; PI
  escalation targets discretionary clinical categories and is a fee-revenue growth
  business on ASO books; aggression is bounded by MLR floors, Stars/CTM exposure,
  prompt-pay statutes, and employer abrasion — hence capped multipliers with decay,
  not unbounded escalation.
- **Gross vs net reporting**: with dynamics active the engine runs each scenario
  twice; every report carries the erosion table and all headline figures are net.
  Regenerated examples: SCN-01 NPV $234M → $110M net (53% erosion); SCN-04 $296M →
  $170M (43%); SCN-02/SCN-03 stay below all thresholds and provoke nothing. The
  emergent strategic result — a quiet workflow redesign's unprovoked NPV (~$98M)
  rivals the aggressive AI wave's post-erosion NPV — is the intended payoff of
  modeling the adversary.
- Scenario schema is backward-compatible (dynamics live in the config; scenarios may
  opt out with `payer_dynamics: false`; CLI `--no-payer-dynamics`). Effect grammar
  gained the `segments` root (payment-lag responses) for both scenarios and rules.

## Not done (deliberate)

- No seasonality or payer-behavior response (exogenous lags/denial rates).
- No HTML app for the twin yet; if added, it follows the build-script pattern
  (`build_*.py` → self-contained generated HTML, never hand-edited).
- Counts elsewhere in the repo are unchanged (no facet/UC/PFM edits); `reconcile.py`
  untouched by this layer.
