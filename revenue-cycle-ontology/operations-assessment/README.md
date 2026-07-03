# Operations Assessment Ontology — Failure Modes & Best Practices

Companion ontology for the dimensions a full revenue cycle assessment examines *alongside* AI
and automation: **operating model, process improvement, workforce, enabling technology, vendor
management, and performance/financial governance**. It is structured the way assessors actually
work: for each domain, the named **failure modes** (what broken looks like in the field, with
observable signals) and the **best practices** that prevent them (what good looks like, with
maturity markers).

It couples deliberately to the rest of the repository: every failure mode states which base
processes it damages (`RC-*`), which KPIs it moves (`KPI-*`), and — critically — **which AI
readiness gates it degrades** (`facets`, `GOV-*`, playbook plays). A traditional assessment and
the AI feasibility assessment are two lenses on one organization; findings in this ontology are
usually the *root cause* of low facet scores in the other.

## Meta-model

| Class | ID pattern | Definition |
|---|---|---|
| **Assessment domain** | `AD-0n` | A dimension of the operations assessment |
| **Failure mode** | `OFM-<dom>-<nn>` | A recurring organizational/process defect, with field-observable signals |
| **Best practice** | `BP-<dom>-<nn>` | The practice that prevents specific failure modes, with maturity markers |

Relationships: `signals` (what an assessor sees/hears), `damages` (RC-* processes, KPI-*),
`degrades` (AI-stack gates), `prevented-by` (OFM → BP), `enables` (BP → AI-stack synergy).

## Domain map

| ID | Domain | File | Failure modes / practices |
|---|---|---|---|
| AD-01 | Operating Model & Organization | `01-operating-model.md` | 8 / 8 |
| AD-02 | Process Improvement & Performance Management | `02-process-improvement.md` | 7 / 7 |
| AD-03 | Workforce | `03-workforce.md` | 8 / 8 |
| AD-04 | Enabling Technology (non-AI) | `04-enabling-technology.md` | 8 / 8 |
| AD-05 | Vendor & Outsourcing Management | `05-vendor-outsourcing.md` | 6 / 6 |
| AD-06 | Performance & Financial Governance | `06-performance-governance.md` | 5 / 5 |

A field checklist (`checklist.yaml`) lists every enterprise failure mode with its signal prompt
for structured capture during interviews and observation, scored `0 = not observed / 1 =
partial / 2 = clearly present`, mirroring the facet-scoring discipline (evidence, not
impressions).

## Process- and role-level layer

The enterprise domains above assess the organization; a second layer takes the same
failure-mode/best-practice structure down the **master ontology's spine** — function → process
→ sub-process → decision → action → role — binding every finding to master-ontology IDs
(`PFM-1.4-01 corrupts 1.4.3.D2`, `performed-by ROLE-AUTH`, `hardened-by UC-01-09`):

| File | Contents |
|---|---|
| `10-process-assessment-model.md` | Meta-model: PFM/PBP/RFM/RBP classes, binding verbs, the OFM→PFM→FM causal stack, altitude rules |
| `11-fn-patient-access.md` … `16-fn-enterprise.md` | Process-level failure modes and paired practices for **all 88 processes** of the master taxonomy (1.1–14.6), each bound to the sub-processes/decisions/actions it corrupts, the `FM-*` defects it produces, and the `UC-*` automation that hardens it |
| `17-role-assessment.md` | Role-level failure patterns and practices for every `ROLE-*` family (including ROLE-BOT — automated agents as workforce), with judgment surfaces mapped to decision IDs |
| `build_field_instrument.py` | Generator: parses all three layers from their sources and emits the full field instrument — rerun after any edit |
| `field-instrument.yaml` | Machine-readable instrument: all 278 items (42 OFM + 162 PFM + 74 RFM) with prompts, signals, and score/notes fields |
| `field-instrument.html` | **Self-contained interactive scoring instrument** — layer tabs, search, 0/1/2 scoring with evidence notes, paired practice revealed on flagged items, per-layer progress, save/open state, scored-YAML export. Works offline on a tablet in the field |

The three layers compose into complete findings: **OFM** (systemic cause, files 01–06) enables
**PFM** (local process failure, files 11–16) executed through **RFM** (role behavior, file 17),
producing **FM-\*** (defect artifact, master ontology), costing **KPI-\*/value-pool dollars**,
and — where a `hardened-by UC-*` binding exists — preventable by a priced automation. The fix
prescription differs by layer: structure/incentives (OFM), standard work/tooling (PFM),
coaching/competency (RFM); assessments that prescribe only one layer relapse.

## How this couples to the AI investment stack

The single most useful assessment finding is a **causal chain**: an operational failure mode →
a degraded AI gate → locked automation value. The recurring chains:

| Operational failure (this ontology) | Degrades (AI stack) | Consequence |
|---|---|---|
| OFM-OM-01 fragmented accountability | `routing_authority`, Play 3 remediation ownership | Prevention insights unrouted; UC-08-05 "kill-as-designed" |
| OFM-OM-02 site-based policy variation | workflow dimension, `collection_policy_unified`, `plan_matrix_unified` | Conversational and POS use cases DEFER on W0/W1 |
| OFM-PI-02 no standard work | W-dimension broadly | "Never automate chaos" — half the catalog waits |
| OFM-PI-03/FG-02 ungoverned metrics | `kpi_dictionary` | Anomaly detection on noise; benefits unprovable |
| OFM-PI-04 root-cause theater | `denial_labels` (CAP-02) | The label pipeline inherits garbage attribution |
| OFM-WF-01 vacancy spiral | `hitl_capacity`, `escalation_staffed` | A2/A3 launches stall; review queues rot |
| OFM-WF-08 AI-anxiety unmanaged | HITL quality, FM-AI-03 rubber-stamping, labeler quality | The experts the AI needs most leave first |
| OFM-ET-01 unoptimized EHR workqueues | `queue_api`, workflow gates | Optimizer schedules against queues nobody owns |
| OFM-ET-04 RPA graveyard | `handback_queues`, FM-BOTSILENT precedent | Fleet observability inherits distrust |
| OFM-VN-03 black-box vendors | `agency_data_rights`, GOV-14 | Oversight analytics and telemetry impossible |
| OFM-FG-01 cost-center myopia | Economics gate (E), investment loop funding | The whole portfolio starves regardless of readiness |

**Assessment sequencing implication:** run the two assessments together and reconcile — every
facet scored 0/1 should have a named OFM as its cause (or the facet score is unexplained), and
every OFM observed should be traced to the facets it degrades (or its remediation is
under-motivated). The joint finding — "this $X/yr of automation value is locked behind this
operating-model fix" — is what moves executive action; either finding alone rarely does.

## Assessment method

Same discipline as the facet worksheet: **evidence over impressions**. A failure mode is
"clearly present" only with a named artifact or repeated observation (two independent
interviews, a walked process, a report shown). Each domain also takes a 0–4 maturity score
(anchors in each file's closing table) for executive summary purposes — but the failure-mode
detail, not the maturity number, drives the remediation plan.
