# Feasibility Gating Framework

Defines when a use case from this catalog is *feasible to implement*. Two parts working together:

1. **This file** — the readiness model: eight gate dimensions with 0–4 maturity scales, a
   universal feasibility decision tree, pattern-based gate templates, and autonomy/risk
   modifiers.
2. **`08-use-case-gate-profiles.md`** — the per-use-case application: every UC's minimum gate
   vector, its decisive gates, and its kill/defer conditions.

The core mechanic: each use case requires a **minimum maturity level in each gate dimension**
(its *gate vector*). Feasibility is weakest-link: the use case is only as ready as its least
ready mandatory gate. A brilliant model with no payer connectivity is infeasible; so is perfect
connectivity feeding an unstandardized workflow.

---

## Gate dimensions and maturity scales

### D — Data Readiness
| Level | Criteria |
|---|---|
| D0 | Required inputs not captured digitally (paper, phone notes, tribal knowledge) |
| D1 | Captured but siloed/unstructured; no reliable extract; IDs don't link across systems |
| D2 | Accessible via warehouse/extract; known quality gaps; linkable with effort |
| D3 | Reliable structured feed at required latency; account/event IDs link across systems (CAP-01); quality measured |
| D4 | Outcome-labeled history ≥12 months (CAP-02), feature-ready, quality monitored continuously; sufficient volume for training/validation splits |

### I — Integration & Infrastructure Readiness
| Level | Criteria |
|---|---|
| I0 | Target systems reachable only through human UI |
| I1 | Read-only batch extracts (daily files) |
| I2 | Read APIs / HL7 / event feeds at the latency the use case needs |
| I3 | **Write-back path** exists: can post transactions, set flags, route queues programmatically; test environment available |
| I4 | Event-driven orchestration fabric (CAP-05), observability (CAP-06), non-human identity & least-privilege access (CAP-08) in place |

### C — Payer / External Connectivity Readiness
| Level | Criteria |
|---|---|
| C0 | Paper/phone only for the transaction in question |
| C1 | Batch EDI via clearinghouse (837/835) established for payers covering the target volume |
| C2 | Real-time transactions live (270/271, 276/277, 278 as required) for payers covering ≥80% of target volume |
| C3 | Portal automation viable: credentials managed, payer terms-of-use reviewed, MFA handled, portal stability acceptable — or payer APIs available |
| C4 | Modern payer APIs (FHIR-based eligibility/auth, e.g., PARDD-era prior-auth APIs), near-universal ERA/EFT enrollment |

*Connectivity is measured against the use case's payer mix, not the whole book: "C2 for the top
10 payers by target-transaction volume" is the working standard.*

### W — Process & Workflow Standardization
| Level | Criteria |
|---|---|
| W0 | Process undocumented; practice varies by individual |
| W1 | Documented but inconsistently followed; exceptions handled ad hoc |
| W2 | Standardized: defined queues, reason/action codes, single owner, consistent policy (e.g., one write-off matrix, one plan matrix) |
| W3 | Exception paths and **hand-back queues** defined (GOV-05 pre-requisite); SLAs defined and measured |
| W4 | Instrumented (touch/action logging) and stable ≥2 quarters — safe to train on and automate against |

**Cardinal rule: never automate a W0/W1 process. Automation hard-codes whatever it finds.**
Standardize first (typically 60–90 days), then automate.

### O — Organizational & Operating-Model Readiness
| Level | Criteria |
|---|---|
| O0 | No accountable business owner |
| O1 | Named owner + SME availability committed for design/validation |
| O2 | Human-in-the-loop capacity sized and staffed (review workbench users, exception workers, escalation-path staffing for conversational agents) |
| O3 | Change management done: affected roles redesigned, training delivered, performance baseline captured for benefit measurement |
| O4 | Feedback labeling is part of the job (corrections captured as training data); continuous improvement cadence running |

### V — Governance & Assurance Readiness
| Level | Criteria |
|---|---|
| V0 | No AI governance function |
| V1 | Risk-tiering body exists; use case tiered and approved at intended autonomy (GOV-01) |
| V2 | Decision logging + version control operational (GOV-02, GOV-11, CAP-10); rollback path defined |
| V3 | Monitoring & audit sampling live (CAP-06, UC-13-04, GOV-07); auto-demotion wired |
| V4 | Bias/adverse-impact testing program (GOV-06) operational for patient-affecting models |

### E — Economic Readiness
| Level | Criteria |
|---|---|
| E0 | Problem not quantified (no baseline metric, unknown volume) |
| E1 | Baseline measured: volume, error/denial rate, labor cost, leakage dollars |
| E2 | Volume clears the materiality threshold and ROI model is positive including build + run + HITL + remediation costs |
| E3 | Benefit-tracking mechanism defined (which KPI-*, measured how) so realization is provable post-launch |

### L — Legal, Regulatory & Contractual Clearance
| Level | Criteria |
|---|---|
| L0 | Not assessed |
| L1 | Privacy/security review done: PHI flows mapped, minimum-necessary applied, BAAs in place for any vendor (GOV-14, 12.7) |
| L2 | External constraints cleared: payer portal terms-of-use for bots, state law (collection conduct, recording consent, balance-billing overlays), CMS rules for the touched process |
| L3 | Counsel sign-off for patient-facing/adverse-action-adjacent automation (FDCPA/TCPA/UDAP exposure for outreach, 501(r) for FA/collections, NSA for billing) |

---

## Universal feasibility decision tree

Run every candidate UC through this tree. Levels required at each gate come from the UC's gate
vector in `08-use-case-gate-profiles.md`.

```
START: candidate use case (UC-XX-NN), target autonomy level, risk tier
│
├─ G0 VALUE GATE — Is E at required level?
│   ├─ E0 → STOP: measure baseline first (2–4 wks). Re-enter.
│   ├─ E1 but volume below materiality → KILL or POOL (combine with adjacent UC; revisit at scale change)
│   └─ E≥2 → continue
│
├─ G1 LEGAL/REGULATORY GATE — Is L at required level? Any hard prohibition?
│   ├─ Hard prohibition at target autonomy (e.g., payer ToS bans bots; state bars automated
│   │   collection act; adverse-action rule GOV-09) →
│   │     ├─ Redesignable at lower autonomy / different pattern? → re-enter with new design
│   │     └─ No → KILL (record reason; watch for rule change)
│   └─ Clearable within plan → continue with L-remediation on the critical path
│
├─ G2 DATA GATE — Is D at required level for every required input?
│   ├─ D0 on any required input → DEFER: capture-first project (change the process to capture
│   │     the data digitally; typically a quarter+). This is a prerequisite project, not a blocker note.
│   ├─ D1–D2 vs D3 required → CONDITIONAL: data engineering remediation (4–12 wks) on critical path
│   ├─ D3 but D4 required (PAT-PRED needing labels) →
│   │     ├─ Label pipeline (CAP-02) can backfill from history → CONDITIONAL (build labels, 4–8 wks)
│   │     ├─ No usable history → DEFER: run the process instrumented (W4) for 2+ quarters to
│   │     │     accumulate labels; OR start with rules-based interim (PAT-RULES version of the UC)
│   │     └─ Vendor pre-trained model viable → CONDITIONAL on validation against local golden set (CAP-09)
│   └─ Met → continue
│
├─ G3 INTEGRATION GATE — Is I at required level?
│   ├─ I0–I1 vs I3 required → is write-back achievable?
│   │     ├─ Vendor/EHR API exists but unlicensed/unbuilt → CONDITIONAL (interface project; cost into ROI)
│   │     ├─ No write-back possible → REDESIGN as A0/A1 insight-only (worklist output), or
│   │     │     RPA-as-integration stopgap (accept fragility; require UC-14-04 fleet ops first)
│   │     └─ Nothing viable → DEFER until platform change
│   ├─ I3 but I4 required (agentic/A4) → CONDITIONAL on Wave-0 fabric (CAP-05/06/08)
│   └─ Met → continue
│
├─ G4 CONNECTIVITY GATE — Is C at required level for payers covering ≥80% of target volume?
│   ├─ Below level →
│   │     ├─ Enrollable (ERA/EFT, RTE, 276/277 enrollment gap) → CONDITIONAL: enrollment
│   │     │     campaign (14.3 work, 4–12 wks/payer)
│   │     ├─ Payer offers no electronic path (niche WC/liability) → SCOPE-CUT: implement for
│   │     │     connected payers only; manual residual; recompute E with reduced scope
│   │     └─ Portal-only + ToS prohibits automation → SCOPE-CUT or KILL for that payer segment
│   └─ Met → continue
│
├─ G5 WORKFLOW GATE — Is W at required level?
│   ├─ W0–W1 → STOP: standardization-first project (document, unify policy matrices, define
│   │     queues/reason codes; 60–90 days). NEVER proceed. Re-enter after.
│   ├─ W2 vs W3 required → CONDITIONAL: define exception/hand-back paths (2–4 wks) before go-live
│   ├─ W3 vs W4 required (training on touch history) → instrument now, train later; interim rules version
│   └─ Met → continue
│
├─ G6 ORGANIZATIONAL GATE — Is O at required level?
│   ├─ O0 → STOP: no owner, no project (this kills more automations than technology does)
│   ├─ O1 vs O2 required → CONDITIONAL: size and staff HITL/exception capacity before pilot
│   │     (rule of thumb: exception volume = (1 − automation rate) × current volume + net-new
│   │     review load; if HITL staffing exceeds labor saved → recompute E, possibly KILL)
│   └─ Met → continue
│
├─ G7 GOVERNANCE GATE — Is V at the level demanded by (risk tier × target autonomy)?
│   ├─ R1 or A≥3 without V3 → cap launch autonomy at A1 (recommend-only) until V3 lands, OR defer
│   ├─ Patient-affecting model without V4 → cap at A0/A1; GOV-06 program is critical path
│   └─ Met → continue
│
└─ DISPOSITION
    ├─ GO           — all gates met → pilot at A1 (per lifecycle), scale per evidence
    ├─ CONDITIONAL  — ≤2 gaps, each remediable ≤90 days → approve with remediation plan; gaps on critical path
    ├─ DEFER        — structural gap (D0 capture, I0 no path, W0/W1 chaos, O0 no owner) → prerequisite
    │                  project first; re-enter tree on completion
    └─ KILL         — legal prohibition with no redesign; volume permanently immaterial; HITL cost
                       exceeds benefit at any achievable automation rate. Record rationale + re-look trigger.
```

**Sequencing note:** gates are ordered by cheapness of killing. Value and legal kill a bad idea
in days; discovering a data gap after building integration wastes a quarter. Always run G0–G1
as a desk exercise before any technical assessment.

---

## Pattern-based gate templates (baseline vectors)

Each automation pattern implies a baseline gate vector. A use case inherits the **maximum** of
its patterns' baselines, then applies autonomy/risk modifiers, then its own specifics (file 08).

| Pattern | D | I | C | W | O | V | E | L | Pattern-specific gating notes |
|---|---|---|---|---|---|---|---|---|---|
| PAT-RULES | 2 | 3 | – | 2 | 1 | 2 | 1 | 1 | Rule source-of-truth must be governed (who owns the logic) |
| PAT-RPA | 2 | 3 | 3 | 3 | 2 | 2 | 2 | 2 | Portal ToS review mandatory; UC-14-04 fleet ops before >3 bots; credential mgmt (CAP-08) |
| PAT-IDP | 2 | 3 | 1 | 2 | 2 | 2 | 2 | 1 | Docs digitized at source (D0 if paper stays paper); ground-truth set ≥500 docs/type for validation |
| PAT-PRED | 4 | 2 | – | 2 | 2 | 3 | 2 | 1 | Labeled outcomes ≥12 mo; label quality audited (FM-AI-07); class balance checked |
| PAT-ANOM | 3 | 2 | – | 2 | 1 | 2 | 1 | 1 | Baseline history ≥12 mo incl. seasonality; alert-fatigue budget (precision floor) defined |
| PAT-NLP | 3 | 2 | – | 2 | 2 | 2 | 2 | 1 | Text corpus accessible (notes access approved); clinical NLP needs domain validation set |
| PAT-LLM | 3 | 3 | – | 2 | 2 | 2 | 2 | 2 | GOV-03 citation-verification harness REQUIRED pre-launch; CAP-04/CAP-10 in place; golden eval set (CAP-09) |
| PAT-AGENT | 3 | 4 | – | 3 | 2 | 3 | 2 | 2 | CAP-05 orchestration + GOV-05 hand-back wiring are hard prerequisites; blast-radius limits defined |
| PAT-CONV | 3 | 3 | – | 3 | 2 | 2 | 2 | 3 | Telephony/chat integration; human escalation staffed for live hand-off (O2 literal); recording-consent laws (L) |
| PAT-OPT | 3 | 3 | – | 3 | 2 | 2 | 2 | 1 | Objective function signed off by business owner; constraint completeness validated |
| PAT-MATCH | 3 | 3 | – | 2 | 2 | 2 | 2 | 1 | Match-confidence thresholds tuned on local data; false-match cost quantified |

*C is dash where connectivity isn't intrinsic to the pattern — the use case's own profile sets it.*

## Autonomy modifiers (added on top of pattern baseline)

| Target autonomy | Additional requirements |
|---|---|
| A0–A1 | Baseline only. This is why every UC launches here. |
| A2 | W≥3 (approval/hand-back paths), V≥2 (logging live), I≥3 (execution path) |
| A3 | V≥3 (sampling + monitoring + auto-demotion), O≥2 (audit capacity staffed), rollback tested |
| A4 | V≥3, I=4, W=4, and UC-14-03/04 observability live — A4 without fleet observability is FM-BOTSILENT by design |

## Risk-tier modifiers

| Risk tier | Additional requirements |
|---|---|
| R1 | V≥3 before exceeding A1; L≥2; GOV-02 reconstruction capability demonstrated |
| R2 | Dollar-threshold gates configured (GOV-08); finance owner named |
| R3 | L=3; GOV-12 disclosure implemented; escalation staffing verified under load |
| R4 | Baseline |

## Remediation playbook (gap → standard fix → typical duration)

| Gap | Standard remediation | Typical duration |
|---|---|---|
| D1→D3 | Interface/warehouse feed + ID-linkage build (CAP-01 increment) | 4–12 wks |
| D3→D4 | Label backfill via CAP-02 from denial/QA/audit history | 4–8 wks |
| No history at all | Instrument process (W4) and accumulate; interim rules-based version | 2+ quarters |
| I1→I3 | EHR/vendor API licensing + interface build | 6–16 wks |
| No write-back | Redesign as worklist (A0/A1) or RPA stopgap with fleet ops | 2–6 wks |
| C1→C2 | RTE/claim-status enrollment per payer via clearinghouse | 4–12 wks/payer |
| Portal ToS blocks bots | Negotiate payer data access / use payer API / scope-cut segment | varies; often KILL for segment |
| W0→W2 | Process standardization sprint: document, unify policy, define queues & codes | 60–90 days |
| W2→W3 | Exception-path & hand-back design | 2–4 wks |
| O0→O1 | Executive sponsorship assignment — governance escalation, not a project | days (or never — then KILL) |
| O1→O2 | HITL capacity model + staffing/backfill plan | 4–8 wks |
| V1→V3 | Stand up CAP-06/CAP-10 + UC-13-04 telemetry (Wave-0 investment, amortized across portfolio) | 8–16 wks once |
| L gaps | Privacy review, ToS review, counsel opinion | 2–8 wks |

---

## How to read a gate profile (file 08)

Each UC row gives:
- **Vector** — minimum levels, e.g. `D3 I3 C2 W3 O2 V3 E2 L2` (dash = not a binding constraint)
- **Decisive gates** — the one or two dimensions that actually decide feasibility for this UC
  (everything else is usually inherited from Wave-0 foundations)
- **Kill/defer conditions** — the specific finding that should stop this UC at this site
