# AI & Automation Use Case Ontology — Revenue Cycle Operations

A companion ontology to the revenue cycle process ontology (`../README.md`). It catalogs every
AI and automation use case that improves the performance of, or prevents the failure modes in,
the process ontology. Every use case is bound to the base ontology by ID: the processes it
targets (`1.4.2`), the events that trigger it (`EVT-*`), the failure modes it prevents (`FM-*`),
the KPIs it improves (`KPI-*`), and the systems it runs in (`SYS-*`).

## Meta-model

### Use case entity

| Attribute | Description | Vocabulary |
|---|---|---|
| `id` | Stable identifier | `UC-<domain>-<nn>` (e.g., `UC-01-04`) |
| `pattern` | Automation pattern(s) employed | `PAT-*` (below) |
| `autonomy` | Maximum autonomy level at maturity | `A0`–`A4` (below) |
| `risk` | Governance risk tier | `R1`–`R4` (below) |
| `targets` | Base-ontology process/sub-process IDs | e.g., `1.4.1, 1.4.3` |
| `trigger` | Initiating event(s) | `EVT-*` |
| `prevents` | Failure modes mitigated | `FM-*` |
| `improves` | KPIs moved | `KPI-*` |
| `guardrails` | Required human-in-the-loop points, thresholds, audits | free text bound to GOV-* controls |

### Automation pattern taxonomy (PAT-*)

| ID | Pattern | Description |
|---|---|---|
| PAT-RULES | Deterministic rules/edits | Hard-coded logic, edit engines, validation gates |
| PAT-RPA | Robotic process automation | Scripted UI/portal interaction; deterministic bots |
| PAT-IDP | Intelligent document processing | OCR + extraction from faxes, cards, EOBs, letters |
| PAT-PRED | Predictive ML | Classification/regression scoring (risk, propensity, value) |
| PAT-ANOM | Anomaly detection | Statistical/ML outlier and drift detection on streams |
| PAT-NLP | Clinical/operational NLP | Entity extraction, criteria mapping, text classification |
| PAT-LLM | Generative AI | Drafting, summarization, evidence citation, explanation |
| PAT-AGENT | Agentic automation | Multi-step goal-directed workflows combining tools, with planning and state |
| PAT-CONV | Conversational AI | Patient/staff-facing chat and voice interaction |
| PAT-OPT | Optimization | Scheduling, routing, prioritization, resource allocation |
| PAT-MATCH | Probabilistic matching | Record linkage, remit-to-claim, payment-to-account matching |

### Autonomy levels (A0–A4)

| Level | Name | Human role |
|---|---|---|
| A0 | Insight | Surfaces information/flags; human decides and acts |
| A1 | Recommend | Proposes a specific action; human approves and executes |
| A2 | Prepare & execute on approval | Drafts/stages the work product; human approves; system executes |
| A3 | Autonomous with audit | Executes without pre-approval; sampled human audit; reversible |
| A4 | Fully autonomous | Executes and self-monitors; humans handle exceptions only |

### Risk tiers (R1–R4) and the autonomy ceiling

| Tier | Definition | Autonomy ceiling |
|---|---|---|
| R1 | Compliance-critical: determines claim content, coded data, patient notices, FA/collection or coverage decisions, audit responses | ≤ A3, mandatory audit sampling, full decision logging; adverse patient-affecting decisions never above A1 |
| R2 | Financially material: moves or forgoes dollars (posting, adjustments, write-offs, refunds) | ≤ A3 with dollar-threshold gates; above threshold → A2 |
| R3 | Patient-facing communication | ≤ A3 with content controls, escalation-to-human on distress/dispute, disclosure of automation |
| R4 | Internal/operational (status checks, monitoring, data movement) | A4 permitted with fleet observability |

The ceiling rule is the central governance constraint: **a use case's autonomy may never exceed
its risk tier's ceiling**, regardless of model performance. Details and controls: `05-governance-assurance.md`.

### Relationship types (extends base ontology)

- `targets` — UC → process/sub-process it operates in
- `prevents` — UC → FM-* it mitigates
- `improves` — UC → KPI-* it moves
- `triggered-by` — UC → EVT-*
- `runs-in` — UC → SYS-*
- `supervised-by` — UC → ROLE-* accountable for its output
- `governed-by` — UC → GOV-* control (defined in `05-governance-assurance.md`)
- `depends-on` — UC → enabling capability (CAP-*) or another UC
- `escalates-to` — UC exception path → human queue/role

## File map

| File | Contents |
|---|---|
| `01-use-cases-front-end.md` | UC-01-* (Patient Access, RC-01) |
| `02-use-cases-mid-cycle.md` | UC-02-* … UC-05-* (UR, Charge, CDI, Coding) |
| `03-use-cases-back-end.md` | UC-06-* … UC-10-* (Claims, Payments, Denials/AR, PFS) |
| `04-use-cases-cross-cutting.md` | UC-11-* … UC-14-* (Contracting, Compliance, Analytics, Data/Tech) |
| `05-governance-assurance.md` | GOV-* controls, CAP-* enabling capabilities, lifecycle, HITL patterns |
| `06-coverage-matrix.md` | FM-* → UC-* coverage (every failure mode countered), KPI → UC index, portfolio sequencing |
| `07-feasibility-gating.md` | Feasibility gating framework: 8 readiness dimensions (0–4 scales), universal decision tree, pattern gate templates, autonomy/risk modifiers, remediation playbook |
| `08-use-case-gate-profiles.md` | Per-use-case gate profiles: minimum gate vector, decisive gates, and kill/defer conditions for every UC |
| `09-value-model.md` | Dynamic value model: 8 value streams, shared value pools with double-count capping, disposition-gated ramps, measurement designs and benefit-ledger governance |
| `10-cost-model.md` | Cost model: three cost layers (platform/build/run), sourcing options (vendor, rules/RPA, ML, frontier API, fine-tune, SLM) with TCO-based decision procedure, SLM break-even math, payer-connectivity pricing, cost governance |
| `11-investment-loop-playbook.md` | Operating playbook for the full stack: roles, quarterly cadence, eight plays (stand-up, re-assessment, council meeting, remediation, launch, autonomy promotion, true-up, kills/renewals), consolidated decision rules, loop failure modes |
| `12-clinical-appeals-engineering.md` | Worked engineering deep-dive (UC-08-03 clinical variant): pipeline decomposition, retrieval/verification architecture, three-tier efficacy evaluation vs a UM physician advisor, minimally viable resource set, and the dependency gaps the exercise surfaced (profile amended) |
| `13-dependency-audit.md` | Portfolio-wide dependency audit: the deep-dive's five dependency classes applied to all 99 use cases — 80 confirmed, 19 amended, 2 new facets, and the sequencing implications (chart corpus, evaluation harness, and policy library elevated to shared Wave-0-adjacent assets) |
| `scoring/` | Runnable toolkit: feasibility (`score.py`), value (`value.py`), cost (`cost.py`), quarterly packets (`packet.py`), a self-contained planner app (`rcm-investment-app.html`), and a use-case catalog explorer (`use-case-explorer.html`) |

## Design principles encoded in this ontology

1. **Prevention beats recovery**: use cases are preferentially placed at the upstream origin of a
   failure mode (per the base ontology's prevention feedback circuit), not at the downstream symptom.
2. **Every automated action is reversible or audited**: no silent, unlogged state change (counters
   FM-BOTSILENT by construction).
3. **Exceptions route to named human queues**: a bot that fails must hand work back explicitly.
4. **Autonomy is earned per use case**: each UC states its maturity path (typically A1 → A3 as
   monitored performance proves out), never deployed at ceiling on day one.
5. **The denial taxonomy is the shared training signal**: denial/audit/complaint outcomes label the
   training data for upstream predictive models — the feedback circuit is also the ML data loop.
