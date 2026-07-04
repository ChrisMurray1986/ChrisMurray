# Portfolio Dependency Audit

The clinical-appeals engineering deep-dive (file 12) proved that gate profiles written at
catalog altitude can miss dependencies that only surface at engineering depth. This audit ran
the same analysis — a desk-version deep-dive — across **all 99 use cases**, to verify that the
declared dependencies are accurate at the depth needed to guide portfolio recommendations and
gate sequencing. Result: **80 profiles confirmed as-is; 19 amended** (plus UC-08-03's earlier
amendment); **2 new facets** added to the catalog (now 98). All driver files, example reports,
the packet, the planner app, and the explorer have been regenerated from the amended vectors.

## Method — the five dependency classes engineering surfaces

The deep-dive's misses generalize into five recurring classes. Each use case was re-examined
against all five, with a bias against facet inflation (a dependency was added only if it is
*decisive* — something a build team would hit in month one and the dimension vector alone
under-specifies):

| Class | The question | Example miss it catches |
|---|---|---|
| **C1 Corpus** | What retrieval/input corpus does the pipeline actually run on, and does it exist digitally? | Appeals need the chart corpus (`notes_access`); card mapping needs card images |
| **C2 License/contract** | Does any input or reasoning target carry usage rights (criteria, code sets, references, external data)? | Arguing against MCG/InterQual needs `criteria_license`; CDM automation touches AMA-licensed CPT |
| **C3 Outcome labels** | Can the efficacy claim be trained and *falsified* — are the outcome labels recorded? | No `appeal_outcomes` → no golden set → unfalsifiable efficacy |
| **C4 Execution hook** | Is there a concrete integration point where the output lands (not just generic write-back)? | Attachment auto-assembly needs programmatic record retrieval (`him_retrieval`) |
| **C5 Release gating** | Does an A3-target system have the evaluation asset that earns the autonomy (CAP-09)? | Autonomous charging / edit agents without `golden_sets` |
| **C6 Input lineage** *(added round 2)* | What upstream build or master supplies the decision keys (lookup values, routing keys) the automation runs on — and is their fidelity scored? | The auth engine's CPT key comes from order-set/visit-type build (`intended_cpt_accuracy`); the submission agent consumes grid verdicts (`auth_grid_accuracy`) |

## Findings by domain

**Confirmed without change (80 use cases).** Notably: all of RC-07 Payments, RC-09 AR,
RC-12 Compliance, RC-13 Analytics, and RC-14 Master Data — domains whose use cases run on
transactional data the facet catalog already named precisely (remits, acks, bank feeds,
registers, telemetry). The original profiles were strongest where the data is most structured.

**Amended (19 use cases):**

| UC | Added | Class | Rationale |
|---|---|---|---|
| 01-03 Card OCR & plan mapping | `card_images` *(new facet)* | C1 | The OCR corpus: if card images aren't captured digitally at registration, there is nothing to extract from |
| 01-07 Auth requirement engine | `masterdata_governance` | C4 | The auth grid is a governed master table; ungoverned edits create false "no auth required" — the most expensive wrong answer |
| 01-08 Auth submission agent | `policy_library` | C1 | Payer questionnaire pre-answering retrieves from medical policies — same corpus as appeals |
| 01-11 Necessity screening | `policy_library` | C1 | Payer-policy necessity edits (beyond public NCD/LCD) need the versioned policy corpus |
| 01-12 Estimate engine | `gfe_stored` | C3 | Estimate-vs-final variance is the training and measurement loop; unstored estimates make accuracy unfalsifiable |
| 02-01 Status prediction | `um_worksheets` *(new facet)* | C3 | Status-determination outcomes are the labels; they live in UR criteria worksheets |
| 02-02 Criteria auto-abstraction | `um_worksheets` | C3 | Nurse-completed worksheets are the ground truth for criteria-element mapping |
| 02-03 Notification/submission bots | `notes_access` | C1 | Clinical review packets are assembled from the chart |
| 03-05 CDM update automation | `reference_license` | C2 | CPT is AMA-licensed content; programmatic diffing/mapping requires rights |
| 03-06 Autonomous charging | `notes_access`, `golden_sets` | C1, C5 | Charges derive from documentation text; A3 charging needs per-domain release gating |
| 04-01 CDI prioritization | `working_drg_recorded` | C3 | Documentation-DRG gap labels require the working DRG to be recorded |
| 04-03 Query drafting | `notes_access` | C1 | Clinical indicators auto-inserted into queries come from the chart corpus |
| 05-01 Autonomous coding | `reference_license` | C2 | Retrieval-grounded coding and audit defense cite licensed references (Coding Clinic, CPT) |
| 06-02 Edit resolution agent | `golden_sets` | C5 | Governed auto-resolution classes are earned per class via evaluation sets |
| 06-05 Rejection auto-repair | `golden_sets` | C5 | Same logic as 06-02 |
| 06-07 Attachment prediction | `him_retrieval` | C4 | Auto-assembly must pull records programmatically — the same hook audit packets need |
| 08-03 Appeal generation | `um_worksheets` (adds to file-12 amendments) | C1 | Case assembly uses the UM trail: worksheets, notifications, P2P notes |
| 10-01 Liability verification gate | `posting_standardized` | C1 | The gate reads remit liability coding; an inconsistent adjustment-code scheme makes it misfire |
| 10-03 Conversational billing | `golden_sets` | C5 | Patient-facing launch requires a conversation evaluation set, not just live QA sampling |

**New facets (catalog 96 → 98):**
- `card_images` — insurance card images captured digitally, front and back
- `um_worksheets` — UR criteria worksheets and determinations stored structured

## Sequencing implications — what the audit changes in portfolio recommendations

The amendments shift the remediation-leverage ranking, which is the input to Play 3 funding
decisions. Three gates gained material weight:

1. **`notes_access` (clinical corpus) now gates 10 use cases** (was 7) — spanning CDI, coding,
   UR, charging, and appeals. At the example org it holds ~$6M/yr. Implication: **chart-corpus
   access + its approval/licensing should be treated as a Wave-0-adjacent asset**, funded once
   with governance, not negotiated use-case-by-use-case. It was previously priced as a
   mid-cycle nicety; it is actually the front door to the entire clinical-NLP family.
2. **`golden_sets` (CAP-09 evaluation infrastructure) now gates 8 use cases** (was 3) — every
   A3-target generative/autonomous build. Implication: a shared evaluation harness (case
   curation, blinded rubric tooling, quarantine discipline) is portfolio infrastructure and
   belongs in Wave 0 alongside observability — confirming what the lifecycle already implied
   but the gate vectors under-priced.
3. **`policy_library` (CAP-04) now gates 4 use cases** (was 1) — appeals, auth submission,
   necessity screening, plus its builder (11-03). Implication: the payer policy corpus should
   be scoped and funded as one asset with one owner; the auth and appeals teams must not build
   parallel policy stores.

Second-order effects: license gates (`criteria_license`, `reference_license`) now appear on
five use cases across three domains — worth consolidating into **one vendor-negotiation
motion** (criteria licensor + AMA + references) rather than three surprise procurement cycles.
And two label gates (`um_worksheets`, `gfe_stored`) are cheap to satisfy *prospectively* (store
what the process already produces) but impossible to backfill — organizations should turn on
that capture now even for use cases they won't build for a year. The playbook's Play 1
evidence rule applies to these immediately.

What did **not** change: no dimension vectors moved, no dispositions flipped at the example
org (the amended use cases were already CONDITIONAL/DEFER on shared gaps), and the Wave-0
core (governance stack, label pipeline, orchestration fabric, contract engine) keeps its rank.
The audit sharpened the middle of the leverage table, not its head — which is itself a useful
validation that the original sequencing guidance was sound.

## Audit round 2 (2026-07) — the input-lineage sweep (C6)

Field use of the ontology surfaced a dependency class the five-class checklist missed:
**automations whose decision keys are supplied by upstream build** — the auth-requirements
grid (Epic ASA class), order-set/visit-type-derived CPTs, eligibility query configuration.
A gate vector can pass on every existing class while the automation runs on unmeasured keys;
the failure is silent because the mis-keyed cases never enter the automation's own queues.
The class was formalized as **C6** and swept across all 99 use cases with the same
anti-inflation bias (decisive-only).

**Amended (6 use cases):**

| UC | Added | Class | Rationale |
|---|---|---|---|
| 01-04 Eligibility orchestration | `rte_benefit_depth` *(new facet)* | C6 | Volume coverage without payer-specific query chaining automates the portal-lookup workaround; the 271 cannot contain what the 270 never asked (PFM-1.3-05) |
| 01-07 Auth requirement engine | `intended_cpt_accuracy` *(new facet)* | C6 | The engine answers per CPT+payer+site — a correct grid answers the wrong question when the order-set/visit-type-derived key is unmeasured |
| 01-08 Auth submission agent | `auth_grid_accuracy` *(new facet)*, `intended_cpt_accuracy` | C6 | Consumes grid verdicts: a false "no auth required" upstream means the case never reaches the agent — the silent branch |
| 01-12 Estimate engine | `rte_benefit_depth`, `intended_cpt_accuracy` | C6 | Cost-share math needs benefit depth; the estimate is keyed on the intended CPT |
| 03-06 Autonomous charging | `clinical_build_governance` *(new facet)* | C6 | Charges fire from order/documentation build; ungoverned clinical releases silently shift the trigger surface |
| 07-02 CARC mapping intelligence | `masterdata_governance` | C6 | The CARC→category mapping table is ungoverned master data at most shops (PFM-7.1-03) — the model trains on its drift |

**New facets (catalog 98 → 103):** `rte_benefit_depth`, `auth_grid_accuracy`,
`intended_cpt_accuracy`, `clinical_build_governance`, `native_capability_inventory` (the fifth
supports the `native_module` sourcing option and OFM-ET-09 rather than a UC gate).

**Sequencing implications:** the prior-auth family (01-07/08/09/10) is where C6 bites hardest —
its keys and verdicts are all upstream build. Grid governance (1.4.1.A4) and intended-CPT
measurement (1.1.2.A9) are cheap, prospective, and impossible to backfill — the same
turn-on-capture-now logic as `um_worksheets`/`gfe_stored` in round 1. Considered and rejected
(anti-inflation): notification-window grids for 02-03 (folded into payer-requirement masters),
`contract_engine_loaded` on 09-01 (round 1 confirmed RC-09 as-is), lineage facets on detector
UCs (01-10, 14-02) whose *purpose* is catching key drift.

## Standing rule (adopted into the loop)

- **Depth-on-demand**: every XL-tier use case gets the full file-12-style deep-dive before
  council approval; every L-tier gets the one-week desk version; S/M tiers rely on this audit's
  five-class checklist at design time.
- **Audit cadence**: re-run the (now six-class) sweep annually, and whenever a deep-dive or a
  failed build surfaces a dependency class the checklist missed — the checklist, like everything
  else in this stack, is a living artifact under true-up. Round 2 (C6) is itself the precedent:
  the class was found by field questioning, not by the annual sweep.
