# Full Assessment Simulation — Model Strengths, Weaknesses & Hardening Backlog

A complete joint assessment was simulated against Meridian Health (the standing simulated org):
the 278-item field instrument scored across all three layers (58 findings flagged with evidence
notes, authored to be consistent with Meridian's existing AI facet assessment), then run through
a purpose-built mechanical validator/reconciler (`reconcile.py`) that stress-tests every claim
the model makes about itself. This file records what held, what broke, and the engineering
backlog (ENG-*) that falls out. Artifacts: `reconcile.py`, `couplings.yaml`,
`binding-validation.md`, and the scored instrument in
`../ai-automation/scoring/simulations/meridian-health/meridian-field-scores.yaml`.

## What the simulation validated (strengths)

1. **The binding discipline is real and mechanically checkable.** Every structural reference in
   all 278 items resolves against the master ontology's actual sections/actions/decisions —
   after the validator caught **10 dangling references** on first run and the fix loop closed
   them. One was a genuine master-ontology mismatch (exclusion screening cited as `11.4.A6`;
   the master holds it at `11.4.A5`) — the assessment layer audited the master, exactly the
   two-way verification the architecture promises.
2. **Defect coverage closes.** All 33 `FM-*` defect artifacts are now produced by at least one
   process failure mode (the validator found 3 orphans — FM-CHGDUP, FM-DOCGAP, FM-MISPOST —
   which were anchored).
3. **The three-layer scoring works in the field-simulation.** 58 findings across
   enterprise/process/role layers scored cleanly with evidence notes; the layered structure
   naturally captured the same reality at multiple altitudes (e.g., metric anarchy appears as
   OFM-FG-02 + PFM-13.1-01 + RFM-ANL-02 — see weakness W4 for the flip side).
4. **The enterprise coupling increment works.** Adding machine-readable `degrades:` to the 42
   OFMs dropped facets-with-no-explaining-finding from 96 to 67 in one pass — proof the
   annotation approach scales to the other layers.
5. **Consistency across the toolchain held.** The field scores authored for Meridian reconciled
   with its facet file without contradiction — no case where the field instrument and the facet
   worksheet forced opposite conclusions about the same fact.

## What the simulation exposed (weaknesses → engineering requirements)

| # | Weakness (evidence from the run) | Engineering requirement |
|---|---|---|
| W1 | **The reconciliation contract is unenforceable as written.** 43 of Meridian's 58 weak facets had *no* linked finding — but inspection shows most are *new-capability* facets (citation_harness, golden_sets, lineage, policy_library…) where nothing "failed"; the capability simply doesn't exist yet. The README contract ("every weak facet has a named OFM cause") is over-strong. | **ENG-01 — Facet causality classes.** Tag every facet as `failure-explained` (weakness must trace to a finding), `new-capability` (absence is the normal state; no finding required), or `contractual` (weakness = unexecuted paperwork). Reconciler enforces the contract only on the first class. |
| W2 | **Process- and role-layer couplings are prose.** 27 of 58 flagged findings carried no machine-readable binding — including *all ten* role findings. PFM-6.5-02 obviously degrades `filing_matrix`, but the text says "filing limits," not the token. | **ENG-02 — `degrades:` annotations for PFM/RFM layers** (as done for OFMs), emitted through `couplings.yaml`; RFM judgment-surface IDs parsed into bindings. Until then the causal-chain report is hand-work. |
| W3 | **Findings carry no dollars.** 58 findings with no severity weighting or value linkage; the council can't rank them against the AI stack's dollar-ranked gates. | **ENG-03 — FM→value-pool join.** Add explicit `pool:` mapping per FM-* in the master registry; reconciler prices each finding via produces→FM→pool (same math as locked-value). Findings become rankable in the same currency as everything else. |
| W4 | **Cross-layer duplicate counting.** The same reality legitimately appears at 3 altitudes (my own scoring notes say "matches PFM-13.1-01"), but chains exist only in prose — a naive report counts 3 findings where there is 1 problem. | **ENG-04 — Chain objects.** First-class `CHAIN-*` records (OFM ← PFM ← RFM → FM → pool) captured at scoring time; reporting counts chains, layers annotate them. |
| W5 | **Opportunity-class use cases look like coverage gaps.** 8 UCs remain unreferenced by any `hardened-by` — correctly, because they are opportunity-driven (cash forecasting, conversational intake), not failure-driven; the validator can't tell. | **ENG-05 — `anchor: failure\|opportunity` designation** per UC in gate-vectors, so the validator distinguishes real gaps from by-design absences. |
| W6 | **Version skew between instrument and scores was silent.** Scores exported last quarter against a since-edited item set would join wrongly with no warning. | **ENG-06 — source-version stamping** *(implemented this run)*: sha1 of sources embedded in instrument YAML/HTML and score exports; reconciler should refuse mismatched versions (refusal check still to add). |
| W7 | **No assessment protocol metadata.** The instrument says *what* to look for, not *who to ask* or *what artifact to request* — inter-assessor variance is uncontrolled (the facet worksheet has the same gap). | **ENG-07 — Per-item protocol fields:** `ask` (role interviews), `artifact` (evidence to request), `sample` (minimum observation). Doubles as new-assessor training. |
| W8 | **Role-layer findings are HR-sensitive with no handling guidance.** RFM-DEN-01 scored 2 names a team's behavior; in a real engagement that page leaks. | **ENG-08 — Sensitivity handling:** role-layer scores aggregate-only in exports by default; individual attribution requires explicit engagement-lead action; anonymization note in the instrument UI. |
| W9 | **The reconciler's facet-mention extraction is string-matching.** It worked here because tokens were written into some texts deliberately; it will silently miss paraphrase forever. | Superseded by ENG-02 (explicit annotations beat NLP extraction for a governed ontology); string-matching demoted to a *lint* that suggests candidate annotations. |
| W10 | **Instrument fatigue is real.** 278 items is a 2–3 day field effort; nothing sequences it. | **ENG-09 — Adaptive pathing:** enterprise layer first; OFM scores gate which process/role sections are worth deep sampling (e.g., OFM-PI-02 absent → light-touch the standard-work PFMs). Encode as `skip-if` hints, keep override trivial. |

**Status (post-hardening pass):** all nine requirements are now **implemented**:
ENG-01 facet causality classes (59 failure-explained / 23 new-capability / 16 contractual in
gate-vectors); ENG-02 `degrades:` couplings for all 236 PFM/RFM items (`pfm-couplings.yaml`,
token-validated at build); ENG-03 FM→pool pricing (`fm_pools` in value-drivers; `--profile`
prices findings and chains); ENG-04 explicit `chain:` grouping with union-find and chain
pricing; ENG-05 `anchor: opportunity` on the 8 by-design-unreferenced use cases; ENG-06
version stamping **plus refusal** on mismatch; ENG-07 per-item ask/artifact protocol defaults
(role-aware for the process layer); ENG-08 role-layer sensitivity banner + aggregate-only
export default; ENG-09 adaptive priority pathing (flagged OFMs light up their coupled
PFM/RFM items, with a priority-only filter). String-matching demoted to lint per W9.

**Post-hardening Meridian rerun:** facets no finding can explain 96 → 67 → **7** (all exempt
classes); weak facets in contract scope 58 → 30, of which 20 explained and 10 correctly flagged
for assessor follow-up; findings with no machine binding 27 → **0**; 58 findings group into
**50 problem chains** (5 multi-layer); top priced finding: the filing-limits chain
{PFM-11.2-02, PFM-6.5-02} at **$32M/yr at stake** (behavior-only chains price $0 — honest:
they degrade capability rather than produce defects).

## Scoreboard from the Meridian run

| Check | First run | After fix loop |
|---|---|---|
| Dangling references (incl. 1 real master-ontology defect) | 10 | **0** |
| FM-* defects produced by no PFM | 3 | **0** |
| Facets with no explaining finding possible | 96 | **67** (42-OFM annotation only; ENG-01/02 close the rest) |
| Weak facets explained at Meridian | — | 15 of 58 (contract enforceable only after ENG-01/02) |
| Flagged findings with no machine binding | — | 27 of 58 (all RFMs; ENG-02) |
| UCs without failure anchor | 12 | **8**, all argued opportunity-class (ENG-05 formalizes) |

## Standing rule

`reconcile.py` runs in validation mode on **every commit** touching the assessment or master
ontology files (the binding report is cheap); the full scored reconciliation runs with every
real engagement and every quarterly re-assessment. Like the dependency audit before it, this
simulation is now a repeatable harness, not a one-time exercise: the model earned its next
increment of trust by being made to fail in public, and the ENG backlog is the receipt.
