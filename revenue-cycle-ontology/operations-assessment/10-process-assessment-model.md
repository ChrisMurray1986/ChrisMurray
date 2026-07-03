# Process-Level Assessment Model

Files 01–06 assess the *enterprise* (operating model, PI, workforce, technology, vendors,
governance). This layer takes the assessment down the master ontology's spine — **function →
process → sub-process → decision → action → role** — so findings bind to the exact place in
the work where value leaks, using the master ontology's own IDs.

## Entity classes (extends the README meta-model)

| Class | ID pattern | Bound to | Definition |
|---|---|---|---|
| **Process failure mode** | `PFM-<process>-<nn>` (e.g., `PFM-1.3-01`) | The process, plus the specific sub-processes (`1.3.3`), decisions (`1.4.3.D2`), and actions (`1.9.3.A1`) it corrupts; the `FM-*` defects it produces; the `ROLE-*` that performs the work | How this process goes wrong *operationally* — observable in the field |
| **Process best practice** | `PBP-<process>-<nn>` | Same bindings; the `UC-*` automation that hardens it where one exists | The paired practice, with what-good-looks-like |
| **Role failure mode** | `RFM-<role>-<nn>` | `ROLE-*`; the decisions/actions where the role's judgment lives | Competency/behavioral failure patterns of the role itself |
| **Role best practice** | `RBP-<role>-<nn>` | Same | Competency model, decision support, and coaching practices |

**Binding verbs:** `corrupts <sub-process/action>` (work done wrong), `skips <action>` (work not
done), `biases <decision>` (branch taken for the wrong reason), `produces <FM-*>` (the defect
artifact), `performed-by <ROLE-*>`, `hardened-by <UC-*>`.

## The causal stack — how the three failure layers compose

```
OFM-*  (systemic cause: files 01–06)        "training is shadowing" (OFM-WF-02)
  └─ enables ─► PFM-*  (local process failure)   "MSPQ read as script, answers defaulted" (PFM-1.2-03)
                  └─ produces ─► FM-*  (defect artifact, master ontology)   FM-COB
                                   └─ costs ─► KPI-* / value pool           CO-22 denials → denial_prevention pool
```

An assessment finding is complete when the chain is walked in both directions: every observed
PFM should name its plausible systemic OFM cause(s), and every PFM should trace to the defect
and dollars it produces. This is also the reconciliation contract with the AI stack: a PFM at a
decision/action is simultaneously (a) a coaching/standard-work finding, (b) an explanation for
a facet score, and (c) an automation candidate — the `hardened-by UC-*` binding says which.

## Altitude rules (how "exhaustive" stays usable)

1. **Coverage is exhaustive at the process level**: every process in the master taxonomy
   (1.1–14.6, 88 processes) carries at least two failure modes and paired practices.
2. **Precision is at the decision/action level**: entries bind to the specific `D`/`A` IDs
   where the failure actually occurs, rather than multiplying entries per action. One PFM
   binding five actions beats five near-duplicate PFMs.
3. **Roles are assessed once, as roles** (file 17), then referenced — role failures recur
   across every process the role touches; duplicating them per process would triple the
   ontology without adding information.
4. **The tables are the checklist**: score each PFM in the field 0/1/2 (not observed /
   partial / clearly present) with the same evidence rule as everything else. The `ID` column
   is the scoring key.

## File map for this layer

| File | Covers |
|---|---|
| `11-fn-patient-access.md` | RC-01 (processes 1.1–1.9) |
| `12-fn-mid-cycle.md` | RC-02 UR, RC-03 Charge, RC-04 CDI, RC-05 Coding (2.1–5.8) |
| `13-fn-claims-payments.md` | RC-06 Claims, RC-07 Payments (6.1–7.6) |
| `14-fn-denials-ar.md` | RC-08 Denials, RC-09 AR (8.1–9.8) |
| `15-fn-patient-financial.md` | RC-10 PFS (10.1–10.7) |
| `16-fn-enterprise.md` | RC-11 Contracting, RC-12 Compliance, RC-13 Analytics, RC-14 Data/Tech (11.1–14.6) |
| `17-role-assessment.md` | RFM/RBP per ROLE-* family |
