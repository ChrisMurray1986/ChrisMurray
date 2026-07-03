# Dynamic Value Model

The economic companion to the feasibility gating framework. Where files 07/08 answer *"can we
build it?"*, this model answers *"what is it worth, and how will we prove it?"* — for every use
case, before (estimation) and after (measurement) deployment.

Implementation: `scoring/value-drivers.yaml` (pools + per-UC bindings), `scoring/value.py`
(engine), `scoring/org-profile.template.yaml` (your financial inputs). The engine joins the
feasibility assessment, so dispositions and gaps price the portfolio: blocked value is
attributed to the specific gate that blocks it.

---

## 1. Value stream taxonomy (VS-*)

Every dollar a use case creates flows through one of eight streams. Streams differ in *kind* —
protected vs recovered vs captured vs accelerated — because each kind has different estimation
math, different measurement designs, and different credibility discount.

| ID | Stream | Nature | Hardness |
|---|---|---|---|
| VS-1 | **Revenue protected** — denials/write-offs prevented (auth, eligibility, TFL, enrollment) | Recurring net revenue | Hard, measurable |
| VS-2 | **Revenue recovered** — appeals won, underpayments collected, hidden denials surfaced | Recurring net revenue | Hard, directly countable |
| VS-3 | **Revenue captured** — charges found, documentation/CMI yield, coverage discovered, contract yield | Recurring net revenue | Hard-to-medium |
| VS-4 | **Patient cash yield** — POS/self-pay conversion, plan retention, bad-debt reduction | Recurring cash | Medium |
| VS-5 | **Cash acceleration** — AR days down: one-time working-capital release + recurring carrying-cost savings | One-time + recurring | Hard but often misclaimed (see §5) |
| VS-6 | **Labor productivity** — touches automated, capacity redeployed or backfill avoided | Recurring cost | Medium; needs harvest rule |
| VS-7 | **External cost reduction** — statement, agency commission, vendor spend avoided | Recurring cost | Hard |
| VS-8 | **Risk & compliance** — expected-value reduction in audit takebacks, penalties, FCA exposure | Expected value | Soft; report separately, never blend into cash totals |

## 2. Value pools — the anti-double-counting mechanism

Use cases do not have independent value; they draw from **shared, finite pools**. Three use
cases that each "prevent 30% of denials" do not prevent 90% of denials. The model therefore:

1. Sizes each pool once, from the org profile (e.g., preventable denial write-offs =
   NPR × final-denial-write-off % × preventable share).
2. Lets each use case claim a **share** of specific pools (its steady-state draw).
3. **Caps** total extraction per pool (default 85%) and scales all draws proportionally when
   the portfolio over-claims — so the portfolio total is structurally honest even if individual
   estimates are optimistic.

Pool catalog (annual $, formulas in `value-drivers.yaml`):

| Pool | Stream | Default sizing ($1B NPR example) |
|---|---|---|
| `denial_prevention` | VS-1 | NPR × 2.0% write-off × 60% preventable = $12.0M |
| `denial_recovery` | VS-2 | NPR × 2.0% × 40% × 35% recoverable headroom = $2.8M |
| `underpayment` | VS-2 | NPR × 1.0% × 80% detectable = $8.0M |
| `charge_capture` | VS-3 | NPR × 1.0% leakage = $10.0M |
| `doc_yield` | VS-3 | NPR × 0.5% CC/MCC-CMI headroom = $5.0M |
| `coverage_conversion` | VS-3 | NPR × 0.4% = $4.0M |
| `contract_yield` | VS-3 | NPR × 0.3% = $3.0M |
| `pos_yield` | VS-4 | NPR × 0.2% = $2.0M |
| `bad_debt_reduction` | VS-4 | NPR × 2.0% bad debt × 15% addressable = $3.0M |
| `ar_days` | VS-5 | per-day: one-time NPR/365 = $2.74M; recurring NPR/365 × WACC = $164k/yr; max 8 reducible days |
| `labor_<function>` (10 pools) | VS-6 | NPR × 3.2% cost-to-collect × 60% labor, split by function |
| `cost_external` | VS-7 | NPR × 0.6% addressable external spend = $6.0M |
| `audit_risk` | VS-8 | NPR × 0.3% exposure × 50% mitigable = $1.5M |

Every default is a parameter in the org profile — replace with your actuals (your denial
write-off rate is in your own data; the defaults are industry-plausible starting points, not
benchmarks to defend).

## 3. Per-use-case estimation

Each UC's binding in `value-drivers.yaml` lists its pool draws:

```yaml
UC-08-03:  # appeal generation
  draws:
    - {pool: denial_recovery, share: 0.25}
    - {pool: labor_denials,  share: 0.20}
```

Steady-state value = Σ (pool × share). Uncertainty band: low = 0.5×, high = 1.6× (global
multipliers, overridable per draw with explicit `low:`/`high:`). The bands are deliberately
wide — this is a prioritization model, not a forecast; precision theater helps no one.

**Disposition-adjusted value** (requires `--assessment`): the feasibility result gates the ramp.

| Disposition | Year-1 factor | Year-2 factor | Steady state |
|---|---|---|---|
| GO | 0.50 | 0.85 | 1.00 from year 3 |
| CONDITIONAL | 0.25 | 0.70 | 1.00 |
| DEFER | 0.00 (0.15 if A0/A1 start available) | 0.40 | 1.00 after remediation |
| KILL | 0 | 0 | structurally unavailable |

**Value locked by gates**: for every blocking item from the scoring run, the engine sums the
steady-state value of the use cases it blocks. This upgrades the readiness report's leverage
chart from "governance≥2 blocks 64 use cases" to "**governance≥2 locks $XXM of annual value**"
— the Wave-0 business case in dollars. (Attribution overlaps by design: a UC with three gaps
appears under all three; the ranking prices gates, it does not sum to the portfolio.)

## 4. Measurement designs — proving it after launch

Estimation gets funding; measurement keeps it. Each stream has one canonical design, defined
*before* go-live (baseline first, or the benefit is unprovable):

| Stream | Baseline | Measured as | Attribution method | Counting rule |
|---|---|---|---|---|
| VS-1 protected | denial write-off rate by taxonomy segment (12-mo) | (baseline rate − actual rate) × volume × net realization | diff-in-diff vs untouched segment/payer control; phased rollout as natural experiment | count *net* dollars at final resolution, not first-pass avoidance; re-baseline annually |
| VS-2 recovered | appeal win rate & $, variance recovery $ | directly counted: dollars posted from appeals/demands the UC produced | case-level tagging (UC id stamped on the work item) | net of recoupments/reversals within 12 mo; never count gross demand letters |
| VS-3 captured | charge/CMI/coverage baseline by cohort | incremental posted (and *paid*) dollars from UC-generated finds | case-level tagging + paid-claim follow-through | count at payment, not charge entry; CMI gains require documentation-audit sign-off |
| VS-4 patient cash | POS $/visit, plan default rate, net bad debt % | cohort deltas | matched-cohort comparison (propensity-scored) | exclude payer-mix drift via mix-adjusted rates |
| VS-5 acceleration | AR days, DNFB days (13-week trailing) | day-delta × NPR/365 | interrupted time-series on the specific inventory the UC touches | **one-time** release counted once; only carrying cost recurs; a day re-lost is clawed back |
| VS-6 labor | touches/FTE, cost/touch, queue volumes | automated touches × standard time × loaded rate | activity logs (the W4 instrumentation) | **harvest rule**: counts only when capacity is redeployed, backfill avoided, or volume absorbed without hiring — "freed minutes" alone are zero |
| VS-7 external cost | vendor invoices, unit costs | invoice deltas | direct — contract/invoice comparison | net of the automation's own run cost |
| VS-8 risk | takeback/penalty history, audit findings rate | expected-value delta (exposure × probability) | scenario model reviewed by compliance | reported in a separate column, never summed with cash streams |

**Benefit ledger governance** (the rules that keep the numbers honest):

- **Single-counting ledger**: every claimed dollar is registered once, to one UC, in one stream.
  Two UCs touching the same denial split by documented rule, not double-claim.
- **Benefit owner sign-off**: the operational owner (not the automation team) certifies each
  quarter's realized value.
- **Net of run cost**: realized value is reported net of license, infra, and HITL labor.
- **Quarterly true-up**: estimated → realized variance reviewed; persistent over-estimation
  triggers driver recalibration in `value-drivers.yaml` (the model is meant to *learn*).
- **Decay & re-baseline**: baselines refresh annually; value against a stale baseline inflates.
- **The measurement infrastructure is itself gated**: most designs need the same CAP-01/CAP-02
  data foundations as the models — if you can't measure the baseline, the UC isn't ready
  (economics gate E1 in file 07).

## 5. Classic value-model failure modes (and where this model blocks them)

| Failure | Control |
|---|---|
| Double-counting across use cases | shared pools + extraction cap (§2) |
| Claiming one-time cash acceleration as recurring | ar_days pool splits one-time vs carrying (§4 VS-5) |
| "Soft savings" inflation (freed minutes ≠ dollars) | VS-6 harvest rule |
| Risk value laundered into cash totals | VS-8 segregated column |
| Gross recovery claimed, net ignored | VS-2 netting rule |
| Value claimed for infeasible use cases | disposition-adjusted view; KILL zeroed, DEFER delayed |
| Enabler use cases (Wave-0) look worthless | locked-value attribution prices the gates they open |
| Estimates never reconciled | quarterly true-up + driver recalibration |

## 6. Using it

```bash
cd scoring
cp org-profile.template.yaml my-profile.yaml   # fill in NPR + your actual rates
python3 value.py my-profile.yaml                              # unconstrained + capped estimates
python3 value.py my-profile.yaml --assessment my-org.yaml     # disposition-adjusted + locked-value-by-gate
python3 value.py my-profile.yaml --assessment my-org.yaml --html value-report.html
```

Outputs: portfolio totals by value stream (capped), per-UC value ranges, year-1
disposition-adjusted value, dollar-ranked remediation list, pool utilization (which pools the
portfolio over-claims), and the measurement plan per use case (stream designs from §4).
