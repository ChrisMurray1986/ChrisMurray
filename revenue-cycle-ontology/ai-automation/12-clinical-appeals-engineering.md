# Engineering Deep-Dive: Clinical Appeals (UC-08-03, clinical variant)

A worked engineering design for one use case, taken all the way down: what it actually takes to
build clinical appeal generation (medical necessity, level of care, DRG downgrade — base
ontology 8.4.3) to **efficacy at or above an experienced UM physician advisor performing the
task manually**, with the *minimally viable* resource set. The exercise doubles as a
verification pass on the ontology's declared dependencies for UC-08-03 — and it found gaps
(§9): the gate profile has been amended.

---

## 1. Define the bar precisely

"As good as an experienced physician advisor (PA)" is two different claims. Engineer both:

| Claim | Metric | Bar |
|---|---|---|
| **Per-appeal parity** | Overturn rate on comparable case mix; blinded expert rubric score | Non-inferiority (margin −3pp overturn) vs PA-authored appeals |
| **Per-portfolio superiority** | Net dollars recovered across *all* appeal-worthy denials | Strictly above the manual baseline |

The second claim is where the system wins even at mere per-letter parity, because the manual
process loses in three places a machine doesn't:

1. **Coverage** — PAs triage; a meaningful share of winnable clinical denials are never
   appealed (capacity), or get a template letter (deadline pressure). The system drafts every
   appeal-worthy case.
2. **Consistency** — a PA at 4pm on the eighth chart skips criteria elements; the system checks
   every element of the applicable criteria set, every time.
3. **Procedural sweep** — a systematic screen for procedural kill-shots humans rarely check:
   wrong criteria set applied per the contract, untimely determination, no peer-to-peer
   offered, notification defects, Medicare Advantage two-midnight obligations (CMS-4201-F era),
   inpatient-only-list status. Procedural wins don't require winning the clinical argument at all.

What deliberately **stays human**: the peer-to-peer call, final strategy on marginal cases,
external-review testimony, and sign-off on every letter (A2 forever — R1 risk tier; the cost
model already prices 100% human review for this use case, and the efficacy design does not
depend on removing it).

## 2. Decompose the task

The PA's manual workflow, made explicit — each stage becomes a pipeline component with a typed
artifact:

```
DenialRecord ──► CaseFile ──► CriteriaMap ──► ArgumentPlan ──► DraftAppeal ──► VerifiedPacket
   (intake)      (assembly)    (evidence↔criteria)  (strategy)     (generation)     (verification + PA)
```

1. **Intake** — parse the denial (835 CARC/RARC + denial letter): denial type, payer/plan,
   claim/auth linkage, cited rationale and criteria set, appeal level, deadline. Letters via
   the correspondence IDP path (UC-07-03); deadline stamped at intake (UC-08-01).
2. **Case assembly** — retrieve the clinical record for the stay: H&P, ED notes, progress
   notes, discharge summary, labs/vitals time series, medication administrations, orders,
   imaging reports; plus the UM trail (criteria worksheets from 2.1/2.2, notification
   timestamps, P2P notes) and the payer contract's appeal clauses.
3. **Criteria mapping** — determine the *applicable* criteria set (what the contract or
   regulation obligates — often not what the payer used: that mismatch is 8.4.3.D1's
   procedural argument). Represent the criteria as a structured checklist; map chart evidence
   to each element with timestamps, provenance pointers, and per-element confidence:
   `met / partially supported / not supported`.
4. **Argument planning** — rank strategies: procedural defects first (cheap, decisive), then
   clinical necessity element-by-element, then regulatory overlays. Output an ArgumentPlan the
   PA can read in two minutes: claims to make, evidence per claim, weaknesses acknowledged.
5. **Generation** — compose the letter from the ArgumentPlan: payer-level-specific format,
   criteria-element structure, every clinical assertion carrying a record citation
   (document + timestamp), every policy assertion quoting the versioned source; assemble the
   packet (records excerpts, remit, auth proof, timeline exhibit).
6. **Verification** — the non-negotiable layer (§4), then PA review and submission (8.4.2
   mechanics), then outcome capture at adjudication (the label loop).

## 3. Architecture — and what you do NOT build

**Model strategy (applies the cost model's own verdict):** frontier LLM through a BAA-covered
API, wrapped in retrieval and deterministic orchestration. **No pretraining. No SLM. No
fine-tuning in the MVP.** The cost model already showed token spend is trivial at this volume
(~30–60k tokens/appeal ≈ $0.15–0.40 even with multi-pass verification, against an average
appeal value in the thousands); the hard problems are *retrieval, grounding, and verification* —
engineering problems, not model-training problems. Fine-tuning enters later only for format
stability at scale, never for clinical knowledge (knowledge lives in retrieval, where it can be
versioned and audited).

**Three retrieval corpora** (build quality here, not model cleverness):

| Corpus | Content | Notes |
|---|---|---|
| Chart | FHIR/CDA export or EHR read API for the encounter; chunked with document type + timestamp metadata | Labs/vitals/meds ingested as *structured series*, not prose — criteria arguments are quantitative ("3L O2 at 02:14") |
| Policy & criteria | Versioned payer medical policies (CAP-04) + licensed MCG/InterQual criteria in structured element form + CMS rules (two-midnight, IPO list) | Effective-dated: appeals argue the version in force on the date of service |
| Contract & regulatory | Appeal rights, obligated criteria sets, determination timelines, P2P obligations per payer contract (from 11.2/UC-11-01) | This corpus powers the procedural sweep |

**Pipeline over mega-prompt:** each stage is a separate, testable call with a typed schema;
deterministic code routes between stages. Stage-level evals localize failures (a bad letter
traces to a bad CriteriaMap, not to a mystery). Criteria mapping runs per-element (one
element, its candidate evidence, one judgment) — not one pass over the whole chart — because
per-element calls are independently verifiable and cache-friendly.

## 4. The verification layer (what makes the efficacy claim honest)

Every draft passes hard gates before a human sees it:

1. **Citation verification (GOV-03, mechanical)** — every quoted policy/criteria passage is
   string-aligned against the versioned source; every clinical assertion's pointer is resolved
   and the span checked for semantic match (a second, independent model call in verify-only
   mode). Unverifiable → the claim is stripped and flagged, never silently kept. Target: ≥99%
   citation accuracy measured continuously; a hallucinated citation in an appeal to a payer is
   a program-ending credibility event (FM-AI-02).
2. **Clinical-logic checks (deterministic)** — timestamps within the stay window; negation and
   temporality audit on extracted facts (a documented "denies chest pain" must never become
   evidence *for* chest pain); units/values sanity on quantitative claims.
3. **Honesty gate** — elements scored `not supported` may not appear as met in the letter; if
   the case can't clear the criteria threshold and has no procedural angle, the system's output
   is a *recommendation not to appeal* with the gap analysis. Refusing weak cases is part of
   beating the PA baseline (portfolio efficacy is net of wasted appeals), and it protects
   overturn-rate credibility.
4. **PA review (A2)** — the PA sees the ArgumentPlan + verified letter with per-claim evidence
   links; typical review is minutes, not the 60–120 minutes of manual authorship. Every PA
   edit is captured as a labeled correction (CAP-07) — the improvement loop.

## 5. Evaluation design — proving "at or above a PA"

Ground-truth outcomes arrive 30–120 days after submission and are confounded by payer and case
mix, so efficacy is proven in three tiers with explicit exit criteria:

**Tier 1 — Offline golden set (weeks 1–10).**
250–300 historical clinical appeals with known outcomes (stratified: payer × denial type ×
won/lost), each with its full chart. The system drafts blind; a panel of 2–3 PAs + appeals
nurses scores system letters vs the original human letters, blinded, on a rubric: criteria-set
selection, element coverage, evidence accuracy, procedural-defect detection, argument quality,
format compliance. *Exit:* rubric non-inferiority; ≥99% citation accuracy; 100% detection of
the procedural defects known to exist in the set; zero unsupported-claims incidents.

**Tier 2 — Shadow mode (weeks 8–16, overlapping).**
Live cases; PAs work normally; the system drafts in parallel. PAs grade both and pick per case.
*Exit:* system draft preferred or equal in ≥60% of cases; median PA edit turns from rewrite to
touch-up; PA-reported time-per-appeal ≤15 min.

**Tier 3 — Live randomized comparison (quarters 2–3).**
Eligible clinical denials randomized: system-drafted (PA-reviewed) vs manual. At the reference
volume (~10k clinical appeals/yr ≈ 800/mo) a −3pp non-inferiority margin on overturn rate
resolves within a quarter; case-mix-adjusted, sequentially monitored with a pre-registered
stopping rule. *Exit:* non-inferiority on overturn per appeal **and** superiority on net
recovered dollars per appeal-worthy denial (the coverage effect). Then scale coverage and
retire the randomization.

Continuous after launch: overturn by strata, citation accuracy, PA edit rate, refusal quality
(sampled), drift telemetry (UC-13-04) with auto-demotion to draft-only on any floor breach.

## 6. Minimally viable resource set

| Resource | Minimum | Why it's the minimum |
|---|---|---|
| **People** | 1 PA/clinical informaticist (0.4 FTE — the domain oracle and rubric anchor); 1 LLM/ML engineer (1.0); 1 data engineer (1.0); 0.5 integration engineer; 0.25 PM; ~120 hrs appeals-nurse SME time | One pizza team; the PA is non-negotiable — without the oracle you tune against your own guesses |
| **Data** | 250–300 historical appeal packets **with outcomes** + their charts; 12 mo of denial letters; UM criteria worksheets | The golden set is the single most valuable asset in the build; if outcomes weren't recorded (8.4.6), assembling this is the first two weeks of work |
| **Corpora** | Policy library scoped to **top 5 payers × top 20 clinical denial categories** (not everything); criteria license amended for programmatic use; contract appeal-clause matrix for those payers | Scope discipline: 5×20 covers the bulk of clinical-denial dollars; breadth comes after efficacy |
| **Systems** | EHR read access (FHIR export acceptable; real-time API not required for MVP); denial work-queue integration for intake/writeback (I3); document store; BAA-covered frontier LLM API | No new platforms: the fabric (CAP-05) is *not* required at A2 — a queue integration suffices |
| **Compute** | API tokens only (~$0.15–0.40/appeal); zero GPUs | The cost model's SLM break-even said stay on API; the MVP obeys it |
| **Timeline** | ~2 quarters to Tier-2 exit; Tier 3 runs quarters 2–3 | |
| **Budget** | ≈ 2.5 FTE × 2 quarters ≈ $310–350k + criteria-license amendment + eval panel + legal review ≈ **$400–450k** | Independently converges with the cost model's UC-08-03 build estimate ($447k, XL tier) — the two models agree from opposite directions |

Explicitly **not** in the MVP: SLM pretraining/fine-tuning, agentic portal submission
(UC-01-08-style bots — submission stays manual/existing process), auto-selection of appeal
level escalation, non-clinical appeal types (technical appeals are a different, easier build),
real-time EHR integration, and any autonomy above A2.

## 7. Build-specific failure modes → mitigations

| Failure | Mitigation |
|---|---|
| Hallucinated policy/criteria text | §4 gate 1; hard block, not a warning |
| Negation/temporality inversion ("denies pain" → evidence of pain) | Deterministic negation audit + a dedicated eval slice for it in the golden set |
| Over-claiming marginal criteria elements | Per-element confidence + honesty gate; PA sees `partially supported` labels, not prose confidence |
| Payer letter format variance breaks intake | IDP confidence gating → manual intake fallback (never guess a deadline) |
| Stale policy/criteria version argued | Effective-dated corpus; version id cited in the letter; library refresh via UC-11-03 |
| Weak cases appealed anyway (overturn rate dilution) | Refusal path is a first-class output with its own quality sampling |
| Golden set leakage into prompts/retrieval | Eval cases quarantined from every runtime corpus |
| PHI exposure | BAA on every hop; minimum-necessary assembly (encounter-scoped retrieval); GOV-02 logging |
| PA rubber-stamping (FM-AI-03) | Seeded-error QA: known-flawed drafts injected monthly; PA catch-rate tracked |

## 8. Where the >PA efficacy actually comes from (summary of the mechanism)

Parity per letter is achieved by grounding + verification + the PA's own sign-off. The *above*
comes from portfolio mechanics the manual process cannot match: 100% coverage of appeal-worthy
denials, 100% procedural sweep, element-complete criteria mapping on every case, principled
refusal of unwinnable cases, and a correction loop that converts every PA edit and every
adjudicated outcome into next-quarter improvement. None of these require the model to be a
better clinician than the PA — they require the system to never be tired, never skip a step,
and never forget an outcome.

## 9. Dependency verification — what this exercise changed in the ontology

The build plan was checked line-by-line against UC-08-03's gate profile. Result:

**Confirmed as load-bearing** (all four existing facets earn their place):
`policy_library` (the retrieval corpus is the product), `citation_harness` (§4 gate 1),
`hitl_capacity` (PA review time is the run-rate), `appeal_process` (standardized 8.4.x
process to automate).

**Gaps found — profile amended** (gate-vectors.yaml + file 08 updated):

| Added dependency | Why the engineering surfaced it |
|---|---|
| `criteria_license` | Clinical appeals argue *against criteria*; structured programmatic use of MCG/InterQual requires amended license rights — same contractual gate as UC-02-02, previously missing here. Blockable: licensor refusal caps the clinical variant. |
| `notes_access` | The chart corpus is half the build; "D3" alone under-specified it — the concrete facet gate was absent. |
| `appeal_outcomes` | The golden set and Tier-3 evaluation are impossible without recorded outcomes (8.4.6). Without this facet the efficacy claim is unfalsifiable — which is a DEFER, not a nice-to-have. |

One cross-model verification also fell out: the bottom-up budget (§6) and the parametric cost
model's UC-08-03 build estimate agree within ~10% — evidence the cost coefficients are sane at
least for this tier. The true-up loop (Play 6) would have found this eventually; a deep-dive
finds it before the money is spent. **Recommended practice: run this exercise (a one-week desk
version) for every XL-tier use case before council approval — the ontology's profiles are the
checklist, and the deep-dive is how the checklist stays honest.**
