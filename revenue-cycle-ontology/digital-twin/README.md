# Revenue Cycle Operations Digital Twin

A deterministic, ontology-grounded simulation of a health system's revenue cycle
operation. The shipped baseline models a **~$10B NPR integrated delivery network on
single-instance Epic, hosted on AWS, with a Snowflake warehouse and Databricks
lakehouse** — but the twin itself is vendor-neutral; the named stack lives only in
the disposable data-binding layer (invariant #1 of this repository).

The twin exists to answer one question class: *if we change how the operation runs —
redesign a workflow, deploy AI/automation, move staff — what happens to financials,
productivity, and patient/caregiver experience, quarter by quarter?*

## Position in the stack

This is the fifth layer of the ontology system. It **consumes** the other four:

| It takes | From | As |
|---|---|---|
| Process IDs (`1.4`, `8.3`…), `ROLE-*`, `FM-*`, `KPI-*` | Base ontology (files `00`–`10`) | Stage/pool/cause/output bindings |
| `UC-*` use-case IDs, autonomy `A0`–`A4`, risk `R1`–`R4` | AI & automation layer | Scenario intervention bindings (validated against `scoring/gate-vectors.yaml`; the autonomy-ceiling rule is checked and violations are warned) |
| The premise that failure modes degrade operations measurably | Operations assessment layer | `quality_index` semantics (defect-rate multipliers on FM-* denial causes) |
| The neutral-core / disposable-binding discipline | Vendor crosswalks | `data-bindings-epic-aws.yaml` (as_of-stamped, confidence-flagged) |

Where the **value model** (`ai-automation/scoring/value.py`) answers "how big is the
prize for use case X at maturity," the twin answers the *operational dynamics*
question: what the whole system does over time when several things change at once —
capacity freed here, backlog formed there, denials prevented upstream shrinking work
downstream, experience moving with workload.

## Files

| File | Role |
|---|---|
| `twin.py` | Simulation engine (Python 3 + PyYAML only). Deterministic — no random draws; identical inputs reproduce identical outputs. |
| `twin-config.yaml` | **Source.** Baseline parameterization of the archetype system. Calibrate every value to your actuals. |
| `data-bindings-epic-aws.yaml` | **Disposable binding.** Where each twin parameter lives on an Epic + AWS + Snowflake + Databricks stack, with `as_of` and confidence flags. |
| `scenarios/*.yaml` | Scenario library (see grammar below). |
| `examples/*.md`, `examples/*.csv` | **Generated** run outputs (committed as records; regenerate, don't hand-edit). |

Run from this directory:

```bash
python3 twin.py --diag                                   # baseline pool utilization sanity check
python3 twin.py -o examples/baseline-report.md           # baseline report
python3 twin.py --scenario scenarios/SCN-01-ai-automation-wave1.yaml \
                -o report.md --csv monthly.csv --json run.json
python3 twin.py --compare scenarios/SCN-0*.yaml -o comparison.md
```

## Model meta-model

Five entity kinds, all defined in `twin-config.yaml`:

1. **Segments** — billing populations (inpatient, hospital outpatient, professional)
   with monthly account volumes, average net revenue, payment lags, denial count
   rates, patient-balance rates. Their product reproduces stated NPR (checked at load).
2. **Stages** — the claim-lifecycle pipeline (22 stages), each bound to the base
   ontology process IDs it aggregates and to one staffing pool. A stage turns driver
   volumes (accounts, denied claims, appealed claims, patient statements) into
   **manual work hours** via `applies × touch_rate × (1 − auto_rate) × min_per_touch`.
   `touch_rate` may exceed 1.0 (multi-review); `auto_rate` is the primary
   AI/automation lever; parameters may be scalar or per-segment maps.
3. **Pools** — staffing supply bound to `ROLE-*` IDs (FTE, loaded cost, productive
   hours). Demand above capacity is absorbed first by capped overtime (at a premium),
   then becomes **backlog**, which carries forward, adds dwell days to the lag chain,
   and degrades experience.
4. **Denial causes** — the initial denial rate decomposed into ten causes, each bound
   to the `FM-*` failure modes behind it and to the **owner stage** whose
   `quality_index` scales it. Scenario improvements upstream (quality_index < 1.0)
   shrink denied dollars *and* denied-claim counts — which shrinks denial/appeal/AR
   work downstream. Each cause carries `recovery` (share of denied dollars ultimately
   recovered) and `appeal_rate` (drives appeals labor).
5. **Levers** — scalar financial/experience parameters (self-pay yield, POS
   collection, estimate accuracy, underpayment detection, charge capture, complaint
   rates, provider burden…), each annotated with its `KPI-*` binding.

### The monthly loop

For each month over the horizon (default 36):

```
volumes → provider-intent params (scenario effects) → payer response overlay
       → denial cascade → driver volumes → stage demand hours → pool capacity/OT/backlog
       → lag chain (bill lag + payment lag + denial cycle + patient tail) → AR days
       → leakage (denial write-offs, bad debt, underpayment, charge leakage)
       → revenue, cash (AR-delta), operating cost → productivity → PXI / CXI
```

Revenue accounting uses a **leakage-inclusive envelope**: the baseline
parameterization reproduces stated NPR exactly (its leakage is already embedded in
NPR), and scenario impact is the *change* in each leakage component versus baseline —
so the twin never double-counts value that today's performance already includes.

### Experience model

Two composite indices (0–100), each a weighted normalization of engine-derived
components between explicit worst/best bounds (see `experience:` in the config):

- **PXI — patient financial experience**: financial clearance rate (degraded by
  front-end capacity shortfalls), estimate accuracy, auth wait days (driven by the
  manual share of auth work and auth backlog), billing complaints (driven by
  estimate accuracy and PFS overload), surprise-bill rate, digital self-service,
  first-contact resolution.
- **CXI — caregiver experience** (staff and providers): workload balance (mean pool
  utilization), backlog pressure, rework share (denial/appeal/follow-up hours as a
  share of all hours), automation relief (share of rote touches automated), provider
  administrative burden (CDI queries + auth work pushed to clinics), and change load
  (simultaneous ramping interventions — transformation fatigue is modeled).

Experience is therefore **emergent, not asserted**: an automation scenario raises CXI
by removing rote touches and rework; an under-staffed redesign *lowers* PXI/CXI
through backlog even if its intent was patient-friendly.

### Payer response dynamics

Payer behavior is **endogenous**: sustained provider improvement triggers lagged,
capped counter-moves, defined as rules in `payer_dynamics:` in the config. Each rule
is a deterministic intensity state machine (0–1): its trigger metric is computed from
**provider-intent parameters** (baseline + scenario effects, *before* payer response)
versus baseline — so the baseline run never self-triggers and the feedback loop
cannot oscillate — and its responses are ordinary effect-grammar edits scaled by
intensity. Shipped rules, grounded in the wargame instruments
(`whats-right-conference-2026/wargame-2/`: payers run decision automation 2–3 years
ahead of providers and deny at near-zero marginal cost; PI escalation targets
discretionary clinical categories; aggression is bounded by MLR floors, Stars/CTM
exposure, prompt-pay statutes, and employer abrasion):

| Rule | Counter-move | Watches |
|---|---|---|
| PR-01 | Algorithmic denial re-tightening on discretionary categories (clinical validation, level-of-care) | denial-prevention gain |
| PR-02 | Appeal slow-walk, documentation friction, marginal overturn erosion | appeal-recovery gain |
| PR-03 | Auth-required service list expansion | auth automation share |
| PR-04 | Payment friction / records-request escalation (ADR, itemized review) | write-off reduction |
| PR-05 | Downcode & silent underpayment pressure | write-off reduction |

When dynamics are active, scenario runs execute **twice** (gross and net) and the
report carries a "Payer response dynamics" section with per-rule trigger months,
intensities, and the gross→net erosion table. All headline figures are **net of
payer response**. Modest programs that stay below every threshold provoke nothing —
which the comparison table makes visible (see SCN-02/SCN-03 vs SCN-01/SCN-04).
Disable with `--no-payer-dynamics` (CLI), `payer_dynamics: false` at scenario top
level, or `enabled: false` in the config.

## Scenario grammar

```yaml
scenario: {id: SCN-XX, name: "...", description: "..."}
interventions:
  - id: INT-XX
    name: "..."
    type: ai_automation | workflow | staffing
    use_cases: [UC-05-01]        # required for ai_automation; validated vs gate-vectors.yaml
    autonomy: A3                 # declared per the governance meta-model
    risk_tier: R1                # ceiling checked: R1/R2/R3 ≤ A3, R4 ≤ A4 (warning on violation)
    start_month: 4
    ramp_months: 9               # effects interpolate linearly baseline → target over the ramp
    effects:
      - {target: stages.coding.auto_rate.hosp_outpatient, set: 0.55}
      - {target: stages.coding.quality_index, set: 0.85}     # fewer FM-CODEERR denials
      - {target: denials.causes.prior_auth.recovery, set: 0.80}
      - {target: levers.selfpay_yield, mult: 1.05}           # set | mult | delta
    staffing:
      - {pool: coding, fte_delta: -45, start_month: 12, glide_months: 10, mechanism: attrition}
    costs: {one_time: 3200000, run_rate_annual: 2400000}
```

Composition rules: effects from multiple interventions on the same parameter apply
sequentially in file order; staffing deltas are additive; every effect ramps from the
**baseline** value, so sequence phases by `start_month`. Shipped scenarios:

| Scenario | Lever exercised | Steady-state, net of payer response |
|---|---|---|
| `SCN-01` AI & automation wave 1 | Eight governed `UC-*` deployments + attrition capture | +$42M/yr net revenue (gross +$66M before payer counter-moves), −$18M/yr labor, PXI 57→66, CXI 70→86 |
| `SCN-02` Staffing rebalance | Pure staffing: 40 FTE back→front, prevention team | +$17M/yr, near-cost-neutral, no payer reaction |
| `SCN-03` Front-end workflow redesign | Pure process change: single-pass clearance, POS discipline | +$37M/yr, PXI 57→67, no payer reaction |
| `SCN-04` Transformation program | All three, sequenced per the investment-loop playbook | +$66M/yr (gross +$96M), NPV ≈ $170M net, PXI 76, CXI 87 |

(Exact figures regenerate from `twin.py`; see `examples/`. Note the strategic result
the payer dynamics surface: the quiet workflow redesign's NPV (~$98M, unprovoked)
lands close to the aggressive AI wave's post-erosion NPV (~$111M) — visibility to
payers is itself a cost.)

## Calibration on Epic + AWS + Snowflake + Databricks

The shipped numbers are archetype defaults. `data-bindings-epic-aws.yaml` maps every
config section to the place it is measured on the named stack (Clarity/Caboodle →
Snowflake marts; Databricks jobs fit touch times, denial cause shares, and drift).
The intended cadence:

1. **Initial fit** — populate `twin-config.yaml` from the warehouse queries in the
   bindings file (volumes, payer lags, denial CARC roll-ups, activity-log touch
   times, HR roster FTEs).
2. **Baseline acceptance** — `--diag` utilizations should land near observed
   productivity; AR days, IDR, and cost-to-collect should match monthly reporting
   within tolerance. If not, fix the config, not the engine.
3. **Quarterly true-up** — rerun the calibration jobs; committed assessment YAMLs and
   example reports are records (repo invariant #5): add new runs, don't overwrite.

## Invariants

1. The neutral core governs: `twin.py` and `twin-config.yaml` never name vendors
   outside `meta.stack` annotations; everything vendor-specific is in the bindings file.
2. Deterministic replay: no clocks, no randomness — runs are diffable artifacts.
3. `examples/` outputs are **generated**; regenerate rather than edit.
4. Scenario `ai_automation` interventions must bind real `UC-*` IDs and respect the
   autonomy ceiling; the engine warns, and a warned scenario should not be presented
   as a governed plan.
5. Pessimism discipline carries over from the scoring layer: prefer conservative
   effect targets (the shipped scenarios cite ramps of 5–10 months and partial
   automation shares, not vendor-brochure numbers).

## Known simplifications

Monthly (not daily) resolution; queues are fluid-flow, not per-account discrete
events; payer response is modeled as bounded, deterministic counter-move rules —
regulatory shocks, litigation, contract renegotiation cycles, and payer-specific
strategy differences (ASO vs fully-insured vs MA books) are not; no seasonality
(add via `growth_annual_pct` or per-month volume overrides if needed);
patient-experience components are proxies bound to measurable KPIs, not survey
instruments. These are deliberate: the twin optimizes for auditable, calibratable
causality over micro-realism.
