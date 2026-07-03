# Cost Model — Predicting Cost and Deciding Between Cost Options

Companion to the value model (09): where value asks *"what is it worth?"*, this model asks
*"what will it cost, under which delivery option, and which option should we pick?"* Cost in
this portfolio is hard for a specific reason: **most of the money is not in the use case** — it
is in shared platforms, payer connectivity, model engineering choices (prompt vs fine-tune vs
small-language-model), and the run-rate consequences of those choices at revenue-cycle volumes.

Implementation: `scoring/cost-drivers.yaml` (rates, volumes, platform assets, per-UC bindings),
`scoring/cost.py` (engine). The engine joins `value.py` for ROI/payback and the feasibility
assessment for disposition-aware phasing.

---

## 1. The three cost layers

| Layer | What it contains | Behavior |
|---|---|---|
| **L1 Platform** (shared) | Data foundation (CAP-01), label pipeline (CAP-02), orchestration fabric (CAP-05), model/bot observability (CAP-06), document-AI platform, payer knowledge base, review workbenches, non-human identity, prompt registry, governance program, **SLM families** | Built once, amortized across every use case that depends on it. This is where "the first use case costs $2M and the tenth costs $150k" comes from. |
| **L2 Build** (per use case) | Design, integration, model/prompt/rules development, validation against golden sets, change management | One-time, sized by complexity tier (S/M/L/XL eng-weeks) × sourcing-option multiplier |
| **L3 Run** (per unit × volume) | Inference/compute, vendor per-transaction fees, licenses, HITL review labor, maintenance & retraining, payer transaction fees, portal-bot upkeep, platform hosting share | Recurring; scales with the use case's **volume driver** (claims, denials, appeals, statements…) |

**Allocation rule**: platform costs are reported unallocated (the honest view for funding
decisions) *and* allocated equally across the active use cases that depend on each asset (the
view for per-UC ROI). Never fund platforms out of a single use case's business case — that kills
the first mover and subsidizes everyone after.

## 2. Sourcing options — the decision space

Each use case has a set of viable delivery options determined by its workload type. The costs
differ in *shape*, not just size: vendors trade build for per-transaction fees; SLMs trade heavy
upfront engineering for near-zero marginal inference.

| Option | Build | Run structure | When it wins |
|---|---|---|---|
| `vendor` | Low (config + integration, ~0.3×) | Per-transaction/subscription fees forever + your HITL | Low volume, undifferentiated capability, speed-to-value; loses at scale and cedes data/control |
| `build_rules` / `build_rpa` | Low-medium | Maintenance-heavy (rules 25%/yr of build — brittle) | Deterministic work; always the interim while ML gates mature |
| `build_ml` (classical predictive) | Medium (needs CAP-02 labels) | Negligible inference + annual retraining | Scoring/prioritization at any volume — tokens aren't the cost, labels are |
| `api` (frontier LLM + orchestration/RAG) | Medium | Token costs at frontier rates + prompt maintenance | Complex generation/reasoning, fast iteration, low-to-mid volume; **the default LLM starting point** |
| `finetune` (adapt a hosted mid-tier model) | Medium + tuning fixed cost + eval harness | Mid-tier token rates + periodic re-tune | Stable, format-heavy tasks at mid volume; fine-tune for *format, latency, and unit cost* — never for knowledge (that's retrieval's job) |
| `slm` (small language model, self-hosted) | High: continued-pretraining/distillation of open weights + eval + hosting | GPU hosting (mostly fixed) + tiny marginal cost | Very high volume, narrow domain, PHI-locality or latency demands. **Family-level asset**: one SLM serves all use cases in its workload family |

**On "pre-training SLMs"**: from-scratch pretraining is almost never justified in revenue cycle
— the realistic path is domain-adaptive continued pretraining or distillation of open weights
onto your corpus (claims, denials, notes), modeled here as a per-family fixed cost. The engine
prices the honest question instead: *at what annual token volume does a family-level SLM beat
frontier API rates?* — `volume × tokens × (api_rate − slm_rate) > amortized family cost + hosting`.
Below that line, the SLM is an engineering vanity project; above it, it is the single biggest
run-cost lever in the portfolio.

## 3. The decision procedure (per use case)

```
1. CONSTRAINTS — filter the option set:
   ├─ PHI/BAA: every option must be BAA-grade (hosted APIs with BAA, or self-hosted)
   ├─ Latency: real-time flows (POS, conversational, RTE) exclude slow paths
   ├─ Data rights: vendor options require your data stays yours (training-use prohibited)
   └─ Feasibility gates: an option needing capabilities you scored 0 inherits that DEFER
2. TCO — compute 3-year total cost per surviving option:
   build×option-multiplier + Σ run(volume-driven) + platform allocation (option-independent)
3. DECIDE — minimum TCO wins, with two documented overrides:
   ├─ Differentiator override: if the UC is flagged strategic (your denial-prevention loop,
   │    your payer knowledge base) and vendor wins by <15%, build anyway — the data flywheel
   │    and control are worth more than the spread
   └─ Portfolio override: prefer the option that reuses an asset you're already paying for
        (an SLM family funded by two use cases makes the third nearly free)
4. RECORD the crossover: the volume at which the runner-up becomes cheaper — so the decision
   auto-flags for revisit when volumes change
```

## 4. Cost estimation math (what the engine computes)

- **Build**: `tier_weeks(S=6, M=14, L=28, XL=52) × eng_week_rate × option_multiplier
  + integrations × per_integration + golden-set validation (tiered)`
- **Inference**: `annual_volume × tokens_per_txn × $/Mtok` (frontier / mid / SLM rates);
  classical ML priced per-prediction (effectively zero); RPA/rules zero marginal
- **HITL labor**: `volume × review_share × minutes × loaded_rate` — review share defaults by
  workload and falls with autonomy earned (A1→A3 re-prices it); this is routinely the largest
  hidden run cost in "automated" business cases
- **Maintenance**: % of build per year by option (rules/RPA highest — brittleness is a cost,
  not a surprise); predictive models add annual retraining; fine-tunes add re-tune cadence
- **Payer connectivity**: per-payer EDI enrollment (one-time) + per-transaction clearinghouse
  fees for EDI-volume use cases; per-payer-per-year portal-bot upkeep for portal automation
  (priced by payer count — this is why portal bots quietly cost more than their licenses)
- **Platform assets**: build + annual run each; SLM families: fixed adaptation cost + annual
  hosting, shared across member use cases
- **Uncertainty**: build ±(cone multipliers 0.8/1.5), run ±20%; reported as ranges, same
  philosophy as the value model — prioritization, not forecasting

## 5. Cost governance (keeping the model honest)

- **TCO or nothing**: no option comparison on build cost alone; 3-year minimum horizon,
  5-year for SLM decisions (the payoff is in the tail).
- **Run-rate ratchet**: every approved UC registers its steady-state run cost; the portfolio
  run-rate total is reviewed quarterly against the value ledger's realized net (09 §4) — value
  is reported *net of run cost*, so the two models close the loop.
- **Crossover register**: each decision stores its volume crossover; volume drift beyond ±30%
  reopens the decision.
- **Platform double-funding ban**: an asset appears once in the plan; use cases reference it.
- **Vendor exit priced in**: vendor options carry a switching-cost line (data migration,
  retraining, parallel run) in year-3 TCO so lock-in is visible at decision time, not renewal.
- **Estimate → actual true-up**: like the value drivers, cost coefficients recalibrate
  quarterly against actuals (engineering time capture, invoice data, token bills).

## 6. Using it

```bash
cd scoring
python3 cost.py example-org-profile.yaml                                  # cost plan, option decisions
python3 cost.py example-org-profile.yaml --assessment example-assessment.yaml   # phased by disposition
python3 cost.py example-org-profile.yaml --assessment example-assessment.yaml --roi   # joins value.py: ROI, payback, net portfolio curve
python3 cost.py ... --html cost-report.html --csv cost.csv -o cost.md
```

Outputs: platform investment plan (L1), per-UC recommended option with TCO range and the
options it beat (with crossover volumes), portfolio cost curve (build + run by year), cost by
category (inference, HITL, vendor fees, payer connectivity, maintenance, platform), SLM
family break-even analysis, and — with `--roi` — value-vs-cost per UC (net value, ROI,
payback months) and the portfolio net curve.
