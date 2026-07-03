# Revenue Cycle Operations Ontology

An exhaustive, machine-parseable ontology of healthcare revenue cycle operations. It maps every
domain, process, sub-process, decision, and action that occurs across the revenue cycle — from
the first patient contact through final account resolution — plus the cross-cutting entities
(roles, systems, artifacts, events, metrics, failure modes) needed to model real operations.

## Scope

Covers hospital (facility/institutional), professional (physician/profee), and hybrid settings;
governmental payers (Medicare, Medicaid, TRICARE, VA), commercial payers, managed care
(MA/managed Medicaid), workers' compensation, auto/liability, and self-pay; fee-for-service and
value-based arrangements.

## Ontology structure (meta-model)

### Entity classes

| Class | Definition | ID pattern |
|---|---|---|
| **Domain** | Top-level functional area of the revenue cycle | `RC-<nn>` |
| **Process** | A named operational process within a domain | `<domain>.<n>` (e.g., `1.4`) |
| **Sub-process** | A bounded stage or workflow within a process | `<process>.<n>` (e.g., `1.4.2`) |
| **Decision** | A branch point with defined inputs and outcomes | `<subprocess>.D<n>` (e.g., `1.4.2.D1`) |
| **Action** | An atomic unit of work performed by a role or system | `<subprocess>.A<n>` (e.g., `1.4.2.A3`) |
| **Event** | An occurrence that triggers or gates work | `EVT-*` (defined in context) |
| **Role** | A human or automated actor | `ROLE-*` (see `10-cross-cutting-entities.md`) |
| **System** | A technology component | `SYS-*` (see `10-cross-cutting-entities.md`) |
| **Artifact** | A document, transaction, or data object | `ART-*` (see `10-cross-cutting-entities.md`) |
| **Metric** | A KPI measuring a process | `KPI-*` (see `10-cross-cutting-entities.md`) |
| **FailureMode** | A known defect/denial/leakage pattern | `FM-*` (see `10-cross-cutting-entities.md`) |

### Relationship types

- `precedes` / `follows` — temporal ordering between processes or sub-processes
- `triggers` — an event or decision outcome initiating a process/action
- `gates` — a decision or event that must resolve before downstream work proceeds
- `performs` — a Role executes an Action
- `automates` — a System executes or supports an Action
- `produces` / `consumes` — Artifact flows in/out of a process
- `measured-by` — Process → Metric
- `fails-as` — Process → FailureMode
- `escalates-to` — hand-off to a higher-authority role or process
- `feeds-back-to` — downstream learning routed upstream (e.g., denial root cause → registration QA)
- `governed-by` — regulation/policy constraining a process

### Decision notation

Each decision is written as:

```
D<n>. <Question>?
  Inputs: <data needed to decide>
  ├─ <outcome 1> → <resulting action/path>
  ├─ <outcome 2> → <resulting action/path>
  └─ <outcome n> → <resulting action/path>
```

### Action notation

Actions are atomic, verb-first, and attributable to a role and/or system:

```
A<n>. <Verb phrase> [role] [system] {produces: artifact}
```

Role/system/artifact tags are included where they disambiguate; otherwise inherited from the
sub-process header.

## Domain map (top level)

| ID | Domain | Cycle phase | File |
|---|---|---|---|
| RC-01 | Patient Access & Financial Clearance | Front end | `01-patient-access.md` |
| RC-02 | Utilization Review & Case Management | Mid cycle | `02-mid-cycle.md` |
| RC-03 | Charge Capture & Revenue Integrity | Mid cycle | `02-mid-cycle.md` |
| RC-04 | Clinical Documentation Integrity (CDI) | Mid cycle | `02-mid-cycle.md` |
| RC-05 | Coding | Mid cycle | `02-mid-cycle.md` |
| RC-06 | Claims Production & Submission | Back end | `03-claims.md` |
| RC-07 | Remittance Processing & Payment Posting | Back end | `04-payments.md` |
| RC-08 | Denials Management & Appeals | Back end | `05-denials-ar.md` |
| RC-09 | Accounts Receivable Management & Follow-Up | Back end | `05-denials-ar.md` |
| RC-10 | Patient Financial Services (Billing & Collections) | Back end | `06-patient-financial-services.md` |
| RC-11 | Payer Contracting, Credentialing & Enrollment | Cross-cutting | `07-payer-contracting.md` |
| RC-12 | Compliance, Audit & Program Integrity | Cross-cutting | `08-compliance-audit.md` |
| RC-13 | Analytics, Reporting & Performance Management | Cross-cutting | `09-analytics-support.md` |
| RC-14 | Master Data, Technology & Vendor Operations | Cross-cutting | `09-analytics-support.md` |

Cross-cutting entity registries (roles, systems, artifacts, metrics, failure modes, events,
regulations) live in `10-cross-cutting-entities.md`. The complete hierarchical index is in
`00-master-taxonomy.md`.

A companion **AI & Automation use case ontology** (`ai-automation/`) maps every AI/automation
use case onto this process ontology — each use case binds to the process IDs it targets, the
`FM-*` failure modes it prevents, and the `KPI-*` metrics it improves, under a governance
meta-model (pattern taxonomy, autonomy levels, risk tiers).

A second companion, the **Operations Assessment ontology** (`operations-assessment/`), covers
the dimensions a full revenue cycle assessment examines alongside AI: operating model, process
improvement, workforce, enabling technology, vendor management, and performance governance —
structured as named failure modes (`OFM-*`, with field-observable signals) and the best
practices (`BP-*`) that prevent them, each coupled to the AI-stack gates it degrades or enables.

## Canonical end-to-end flow

```
Scheduling → Pre-registration → Eligibility/Benefits → Prior Auth → Estimate/GFE →
Financial Counseling → POS Collection → Registration/Arrival → [Service Delivery] →
UR/Status Determination ∥ Charge Capture ∥ CDI → Coding → Claim Edit/Scrub →
Claim Submission → Payer Adjudication → Remittance/Posting → {Paid | Denied | Underpaid} →
Denials/Appeals ∥ Underpayment Recovery ∥ AR Follow-Up → Patient Balance Billing →
Payment Plans / Financial Assistance / Collections → Account Resolution (zero balance) →
Credit Balance/Refund handling → Close
```

Feedback loops (denial root causes → front-end QA; audit findings → coding education; contract
variance → payer negotiation) are modeled with `feeds-back-to` relationships in each domain file.
