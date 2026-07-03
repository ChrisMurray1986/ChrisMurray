# Governance, Assurance & Enabling Capabilities

The controls (GOV-*) that make the use case catalog safe to run, the enabling capabilities
(CAP-*) it depends on, and the lifecycle/HITL patterns that apply across all UC-*.

---

## Governance controls (GOV-*)

| ID | Control | Applies to |
|---|---|---|
| GOV-01 | **Autonomy ceiling enforcement** — risk tier caps autonomy (README table); autonomy changes require governance approval; automatic demotion on performance-floor breach (via UC-13-04) | all UC |
| GOV-02 | **Decision logging** — every automated determination logs inputs, model version, output, confidence, and human overrides; retained per record-retention policy; reconstructable for audit/appeal defense | all UC ≥ A2; all R1 |
| GOV-03 | **Citation verification** — generative outputs that cite sources (policies, contracts, chart evidence) pass hard validation that cited text exists in the referenced source before human review | all PAT-LLM (UC-01-08, UC-04-03, UC-05-07, UC-08-03, UC-11-01, UC-12-05…) |
| GOV-04 | **No-fabrication rule for claim content** — nothing that changes what is billed (codes, modifiers, units, dx) may be generated without traceable source evidence; edits never applied "to force a claim through" | UC-05-01, UC-06-02, UC-03-06, UC-01-11 |
| GOV-05 | **Explicit exception hand-back** — any automated worker that cannot complete must place the work in a named human queue with context; silent drops are a severity-1 defect | all PAT-RPA/PAT-AGENT (enforced by UC-14-04) |
| GOV-06 | **Bias & adverse-impact testing** — patient-affecting models (propensity-to-pay, FA scoring, collection treatment, plan offers) tested for demographic adverse impact pre-deployment and quarterly; presumptive *denials* of benefit never automated | UC-10-05, UC-10-02, UC-10-04, UC-01-13, UC-09-06 |
| GOV-07 | **Audit sampling mandates** — R1 use cases at A3 carry defined human audit sampling rates with statistical quality floors; sample sizes scale up on any regression | UC-05-01, UC-03-06, UC-01-01, UC-08-01… |
| GOV-08 | **Dollar-threshold gates** — R2 financial executions above configured thresholds drop from A3 to A2 (human approval); thresholds owned by finance with periodic review | UC-07-01, UC-09-04, UC-06-08 |
| GOV-09 | **Adverse-action human rule** — decisions adverse to patients (service deferral, collection escalation, FA denial) or providers (discipline-relevant findings) are never automated above A1 | UC-01-13, UC-10-x, UC-12-03 |
| GOV-10 | **Compliance-critical routing locks** — fraud-unit correspondence, exclusion-list hits, potential FCA/Stark matters route to compliance/counsel by hard rule; AI may flag, never disposition | UC-12-01, UC-11-04, UC-12-04 |
| GOV-11 | **Model change management** — models/prompts/rules version-controlled; material changes tested against golden datasets and shadow-run before production; rollback paths required | all UC |
| GOV-12 | **Automation disclosure** — patient-facing conversational agents disclose automation and provide human escape at any point | UC-01-14, UC-10-03, UC-10-04 |
| GOV-13 | **Regulatory content is rules, not generation** — mandated language (ABN text, 501(r) notices, consent language, GFE elements) comes from controlled templates; generative systems may explain but not author it | UC-01-11, UC-01-14, UC-10-02, UC-10-03 |
| GOV-14 | **Third-party AI vendor diligence** — vendor AI tools meet the same tiering, logging, and testing requirements; BAAs + data-use limits per 12.7 | all vendor-delivered UC |

## Enabling capabilities (CAP-*)

| ID | Capability | Consumed by |
|---|---|---|
| CAP-01 | **Unified data foundation** — cleansed longitudinal account/event data joining clinical, financial, and payer transactions with the base ontology's IDs as schema | every PAT-PRED/PAT-ANOM |
| CAP-02 | **Denial/defect label pipeline** — the 8.1 taxonomy, audit findings, and QA results flowing as training labels with owner attribution (the prevention circuit as data loop) | UC-06-01, UC-08-01/02/05, UC-01-16 |
| CAP-03 | **Document AI platform** — shared OCR/extraction with confidence scoring and human-verify UI | all PAT-IDP |
| CAP-04 | **Payer knowledge base** — versioned, citation-linked store of payer policies, auth grids, contract matrices, bulletins | UC-01-07, UC-08-03, UC-11-03, UC-06-07 |
| CAP-05 | **Orchestration & queue fabric** — event bus on EVT-*, work-queue APIs, and hand-back interfaces every agent uses (GOV-05 depends on this) | all PAT-AGENT/PAT-RPA |
| CAP-06 | **Model observability stack** — telemetry, drift detection, override tracking, demographic metrics | UC-13-04, GOV-01/06/07 |
| CAP-07 | **Human-review workbenches** — confidence-ranked review UIs with one-click accept/correct that feed corrections back as labels | all A1/A2 UC |
| CAP-08 | **Identity & access for non-human workers** — credentialed, least-privilege, auditable bot/agent identities | all PAT-RPA/PAT-AGENT |
| CAP-09 | **Golden test datasets** — curated evaluation sets per use case (claims, denials, documents) for release gating | GOV-11 |
| CAP-10 | **Prompt/rule/policy registry** — versioned store of prompts, rules, and guardrail configs with approval workflow | all PAT-LLM/PAT-RULES |

## Use case lifecycle (applies to every UC-*)

```
Propose (UC-14-05 mining or domain request)
  → Tier (assign risk R1–R4 → autonomy ceiling)
  → Design (bind to process IDs, FM-*, KPI-*; define guardrails, exceptions, HITL points)
  → Validate (golden dataset performance + shadow run in production traffic)
  → Deploy at A1 (recommend-only, measure agreement rates)
  → Earn autonomy (A1→A2→A3 per evidence, never past ceiling; each step governance-approved)
  → Operate (UC-13-04 telemetry; GOV-07 sampling; drift response)
  → Demote/retire (auto-demotion on floor breach; explicit hand-back of work to humans on retirement)
```

## HITL design patterns (referenced by autonomy levels)

| Pattern | Description | Typical use |
|---|---|---|
| HITL-CONF | Confidence-threshold split: high-confidence auto, rest to human | IDP, matching, classification (A3) |
| HITL-APPROVE | Full human approval of staged work product | appeal letters, auth packets, refunds (A2) |
| HITL-SAMPLE | Post-hoc statistical audit of autonomous output | autonomous coding, auto-posting (A3 + GOV-07) |
| HITL-ESCAPE | In-flow escalation triggers (distress, dispute, ambiguity) | conversational agents (R3) |
| HITL-OVERRIDE | Human can override any determination; overrides captured as labels | all scoring/routing |
| HITL-DUAL | Second-human review above dollar/risk thresholds | write-offs, large refunds (GOV-08) |

## Failure modes OF the automation layer (FM-AI-*)

The automation portfolio introduces its own failure modes; each has a named countermeasure:

| ID | Failure mode | Countermeasure |
|---|---|---|
| FM-AI-01 | Model drift degrading silently | UC-13-04 monitoring + auto-demotion (GOV-01) |
| FM-AI-02 | Hallucinated citations/policy text in generated documents | GOV-03 hard citation verification |
| FM-AI-03 | Automation bias (humans rubber-stamping A1/A2 recommendations) | agreement-rate monitoring; deliberate seeded-error QA; UI friction on high-risk approvals |
| FM-AI-04 | Systematic upcoding/leveling drift from AI coding | E/M and DRG distribution surveillance (UC-12-03 watches the machines too) |
| FM-AI-05 | Bot/agent silent failure dropping work | GOV-05 + UC-14-04 quarantine-and-return |
| FM-AI-06 | Discriminatory treatment from patient-facing models | GOV-06 adverse-impact testing; presumptive-approval-only design |
| FM-AI-07 | Training-label contamination (denial taxonomy errors propagate into models) | UC-08-01 classification audits; CAP-02 label QA |
| FM-AI-08 | Cascade failure (upstream model error amplified by downstream automation) | inter-UC dependency registry (`depends-on` edges); circuit-breakers on anomalous volume between stages |
| FM-AI-09 | Unauditable decisions in appeal/audit defense | GOV-02 decision logging with reconstruction capability |
| FM-AI-10 | Vendor AI opacity | GOV-14 diligence; contractual telemetry access |
| FM-AI-11 | Over-automation of judgment work (wrong work assigned to machines) | UC-14-05 mis-assignment detection; lifecycle tiering discipline |
| FM-AI-12 | Prompt/config drift outside change control | CAP-10 registry + GOV-11 change management |
