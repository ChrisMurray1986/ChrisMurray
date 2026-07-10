# The Investment Loop Playbook

How to operate the full stack — process ontology → use-case catalog → feasibility (07/08) →
value (09) → cost (10) — as a continuous investment process rather than a one-time study. The
stack's outputs are only as good as the loop that refreshes them: assessments go stale, value
drivers drift from actuals, cost crossovers get crossed, and autonomy promotions re-price
everything. This playbook defines the roles, cadence, plays, and decision rules that keep the
loop turning.

**The loop:**

```
        ┌─────────────────────────────────────────────────────────────┐
        ▼                                                             │
  ASSESS readiness ──► SCORE feasibility ──► PRICE value & cost ──► DECIDE
  (facts, quarterly)   (score.py)            (value.py, cost.py)   (invest / remediate /
        ▲                                                            launch / kill)
        │                                                             │
  TRUE-UP drivers ◄── MEASURE realized ◄── BUILD & operate ◄──────────┘
  (recalibrate yaml)   (benefit ledger,      (pilot A1 → earn autonomy,
                        cost actuals)         baseline BEFORE go-live)
```

One command produces the quarterly decision packet:
`python3 scoring/packet.py my-org.yaml my-profile.yaml --outdir packets/2026-Q3`

---

## 1. Operating model — who runs the loop

| Role | Held by | Owns |
|---|---|---|
| **Executive sponsor** | CFO or VP Revenue Cycle | Funding authority; unblocks O0 gaps (no-owner kills); accepts portfolio risk |
| **Automation council** | Sponsor + domain VPs + Finance + Compliance + IT/Eng lead (6–8 people, no more) | The quarterly investment decision; autonomy promotions above A2; kill decisions |
| **Loop operator** | One named person (RCM automation program lead) | Runs the tools, maintains the YAML files, produces the packet, chases assessment inputs. **The loop dies without this role.** |
| **Facet owners** | The operators of each area (per 08 discipline: "scored by the person who operates it") | Their facet scores + evidence, refreshed quarterly |
| **Benefit owners** | Operational owner of each live use case | Quarterly realized-value sign-off (09 §4); the automation team never certifies its own benefits |
| **Governance body** | Per GOV-01 (may be a council subcommittee) | Risk tiering, autonomy ceilings, promotion evidence, demotions |
| **Finance partner** | Assigned analyst | Org profile actuals, cost true-up vs invoices/time capture, benefit ledger integrity |

RACI shorthand: council **decides**, loop operator **runs**, facet/benefit owners **attest**,
governance body **constrains**, sponsor **funds and unblocks**.

## 2. Cadence

| Rhythm | What happens |
|---|---|
| **Weekly** | Delivery standup per active build; exception-queue and bot-fleet health (UC-14-04 telemetry) |
| **Monthly** | Run-rate review: HITL hours, token/vendor invoices, model telemetry (UC-13-04); anything drifting >20% from packet assumptions flags early |
| **Quarterly** | **The investment cycle** (§3) — re-assess, true-up, regenerate packet, council decision |
| **Annually** | Strategy refresh: re-baseline value pools against the year's actuals; revisit KILL register; refresh org profile rates from audited financials; re-run vendor market scan |

### The quarterly cycle (13 weeks)

- **Wks 1–2 — Refresh the facts.** Facet owners update their scores with evidence; finance
  updates the org profile (rates from actuals, volumes); loop operator updates driver YAMLs
  from true-up findings (§ Play 6).
- **Wk 3 — Regenerate.** Run `packet.py`. Diff against last quarter's packet — the diff *is*
  the readiness-velocity and value-drift report.
- **Wk 4 — Council meeting.** One 2-hour session, packet pre-read mandatory (§ Play 2 agenda).
- **Wks 5–12 — Execute.** Funded remediations and builds proceed; measurement baselines
  captured before every go-live (non-negotiable).
- **Wk 13 — Pre-close.** Benefit owners sign the quarter's ledger; cost actuals reconciled;
  true-up notes queued for next cycle's week 1.

## 3. The plays

### Play 0 — Stand up the loop (first 90 days, once)

1. Name the loop operator and convene the council (half-day charter session).
2. Baseline: fill the assessment (facet owners, 2–3 weeks of interviews) and the org profile
   (finance, 1 week — NPR, denial write-offs, cost-to-collect are in monthly reporting).
3. Generate packet #1. Expect `GO: 0` — read it as sequencing, not failure (08 guidance).
4. First council: fund **Wave-0 from the locked-value ranking** (the packet prices it — e.g.,
   "governance≥2 locks $27M/yr"), approve the A0/A1-available list for immediate launch, and
   adopt the decision rules (§4) so future meetings argue about facts, not process.
5. Stand up the benefit ledger (09 §4) and the crossover register (10 §5) — empty is fine;
   existing is mandatory.

### Play 1 — Quarterly re-assessment

- Facet owners re-score **with evidence** ("demo it this week" = 2; vendor promise = 1).
- Rule: a score may only *rise* with a named artifact (working feed, signed BAA, published
  matrix). Scores fall freely — pessimism is self-correcting, optimism is not.
- The loop operator commits the new assessment file; the git diff vs last quarter is reviewed
  at council as the **readiness velocity** slide. Zero diff for two quarters = the remediation
  budget is not working; escalate.

### Play 2 — The investment decision meeting (the council's 2 hours)

Packet pre-read is mandatory; the meeting decides, it does not discover. Agenda:

1. **True-up (20 min)** — realized vs estimated value and cost for everything live; benefit
   owners' signatures; driver recalibrations applied.
2. **Readiness velocity (10 min)** — assessment diff; remediation projects on/off track.
3. **Operational improvements (15 min)** — the operations assessment's improvement plan
   (reconcile.py ENG-07, bound into the packet as `operations.md`): process and operating-model
   fixes prescribed by the paired best practices, typed by layer (structure/incentives,
   standard work, coaching). These carry value with or without automation and are the root
   cause of most weak facets — fund them ahead of, or alongside, technical gate remediation.
   Same decision discipline as track two: owner, budget, proving metric per funded fix.
4. **Remediation funding (15 min)** — locked-value ranking: fund the top technical items until
   marginal locked-value-per-remediation-dollar drops below the best direct use-case ROI.
   Where item 3 already funds a gate's operational root cause, the technical remediation rides
   that project rather than duplicating it.
5. **Launch decisions (30 min)** — GO and CONDITIONAL-with-plan use cases, ranked by
   net-value × payback from the cost model's ROI join; approve builds with named benefit owner,
   measurement baseline plan, and sourcing option (the cost model's recommendation is the
   default; overrides are documented in the packet).
6. **Autonomy promotions (10 min)** — governance body presents evidence per candidate (§ Play 5).
7. **Kills & descopes (10 min)** — net-negative UCs, crossed crossovers, KILL-register re-looks.
8. **Decisions logged (10 min)** — every decision gets: owner, budget, expected value (from the
   packet, not re-negotiated in the room), and the metric that will prove it.

### Play 3 — Remediation projects (unlocking gates)

Remediations are projects with the same discipline as use cases: owner, duration from the
playbook table (07 §remediation), and **expected unlocked value** from the locked-value
ranking as their business case. On completion, the facet score changes *in the assessment
file* — that is the definition of done. A remediation that finishes without moving a facet
score did not finish.

### Play 4 — Use-case launch

1. Verify gates at launch (not at approval — a quarter may have passed).
2. **Capture the measurement baseline first** (09 §4 design for its streams). No baseline, no
   go-live: the benefit becomes unprovable and the ledger inherits a hole.
3. Launch at A1 regardless of target autonomy (07 lifecycle); register run-rate in the ratchet.
4. Stamp every work item the UC produces with its UC id (case-level tagging enables VS-2/VS-3
   attribution later).
5. First 90 days: agreement-rate and exception-queue metrics weekly; value claims start only
   after the first true-up, not at launch.

### Play 5 — Autonomy promotion (the hidden value lever)

A2→A3 promotion is where HITL cost collapses (the cost model prices review burden at mature
autonomy — promotion is how you reach it). Evidence per GOV-01/07: agreement rate vs human
decisions over a defined window, exception-rate stability, audit-sample quality, rollback
tested. On promotion, the loop operator updates the UC's `hitl_share` in `cost-drivers.yaml`
— the next packet shows the run-rate drop automatically. Demotions (auto, via UC-13-04) flow
back the same way. **Every promotion/demotion is a cost-model event, not just a governance
event.**

### Play 6 — True-up (what makes the model honest)

Quarterly, per live use case:
- **Value**: realized (ledger, owner-signed) vs estimated (packet). Persistent >30% over-estimate
  → cut the UC's draw shares in `value-drivers.yaml`; >30% under-estimate → raise them (rare,
  pleasant). Pool sizings re-baseline annually from actuals.
- **Cost**: invoices + time capture vs packet. Token bills, vendor fees, HITL hours map
  directly onto the cost categories; recalibrate `cost-drivers.yaml` rates when a category
  drifts >20% for two quarters.
- **Crossovers**: volumes vs the crossover register; any decision whose volume moved ±30%
  reopens at the next council.
- All recalibrations are YAML commits with a note — the git history is the audit trail of the
  model learning.

### Play 7 — Kill discipline

Kill without ceremony: net-negative for two consecutive true-ups with no credible fix (cost
model flags these — e.g., an LLM assist whose review cost exceeds its pool draw), a facet gone
`blocked`, or a vendor/product change that erases the case. Killing a live UC returns its run
rate to the ratchet as savings and its pool draws to the portfolio. Re-look KILLs annually —
regulations, license terms, and volumes change.

### Play 8 — Vendor renewals

Renewal = decision reopened, not auto-renew: re-run the UC's option comparison at current
volumes (the crossover register predicts most of these), price the exit honestly (already in
TCO), and negotiate with the build-option TCO on the table — the model's number is your BATNA.

## 4. Decision rules quick reference (consolidated)

| Decision | Rule | Source |
|---|---|---|
| Standardize before automating | Never automate W0/W1 | 07 cardinal rule |
| Launch autonomy | Always A1, earn upward | 07 lifecycle |
| Autonomy ceiling | Risk tier caps autonomy, no exceptions for performance | GOV-01 |
| Remediation vs direct build | Fund remediations while marginal locked-$/remediation-$ > best direct ROI | 09 locked-value |
| Sourcing option | Min 3-yr TCO after constraint filter; differentiator override <15%; portfolio-reuse override | 10 §3 |
| SLM | Only when family savings/yr > adapt/3 + hosting (packet table says) | 10 §2 |
| Fine-tune | Format/latency/unit-cost at volume — never for knowledge | 10 §2 |
| Vendor | Wins at low volume + undifferentiated; exit priced in TCO; renewal reopens decision | 10 §2, Play 8 |
| Value claims | Baseline first; owner-signed; net of run cost; one ledger entry per dollar | 09 §4 |
| Kill | 2 consecutive net-negative true-ups, or `blocked` facet, or dead crossover | Play 7 |
| Re-score | Quarterly; facet rises only with evidence | Play 1 |

## 5. Failure modes of the loop itself

| Failure | Symptom | Countermeasure |
|---|---|---|
| No loop operator | Packet #2 never ships | Name the role in Play 0; it's a job, not a hobby |
| Assessment theater | Facets drift up without artifacts | Evidence rule (Play 1); spot-audit two facets per quarter |
| Packet re-litigated in the room | 2-hour meeting becomes 4 | Pre-read mandatory; meeting decides only |
| Benefits certified by the builder | Ledger inflation | Benefit-owner signature rule (09 §4) |
| Baselines skipped under schedule pressure | Unprovable value forever | No-baseline-no-go-live (Play 4) — sponsor enforces |
| Remediation without a facet change | "Done" platform work, same DEFERs | Definition of done = facet score moves (Play 3) |
| Autonomy promotions stall | HITL cost never falls; ROI stuck at A2 | Promotions on every council agenda (Play 5) |
| Drivers never recalibrated | Model credibility decays; finance disengages | True-up is agenda item #1, not an appendix (Play 2) |
| Everything CONDITIONAL forever | Remediation budget spread too thin | Fund fewer gates fully (top of locked-value list) rather than all gates slightly |

## 6. Artifacts & conventions

- **Version-control everything**: assessment, org profile, all driver YAMLs, and each quarter's
  packet directory. Diffs between quarters are the loop's primary management reports.
- **Packet directory** (`packets/<year>-Q<n>/`): feasibility + value + cost reports (md/html/csv)
  plus `index.md` — headline numbers, quarter-over-quarter deltas, and the council agenda
  pre-filled. Generated by `scoring/packet.py`; never hand-edited (edit the inputs, regenerate).
- **Ledgers** (benefit ledger, run-rate ratchet, crossover register, KILL register, decision
  log): simple committed files beside the packets; the packet references them.
- **One source of truth per number**: a figure appears in the YAML inputs or in generated
  output — never retyped into slides. If the council needs a slide, it links the packet.
