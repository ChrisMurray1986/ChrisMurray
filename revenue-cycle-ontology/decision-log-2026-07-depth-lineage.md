# Decision Log — 2026-07 Depth & Lineage Expansion

Structural engineering pass applying four field-surfaced gap classes to the entire ontology.
The specimens that exposed the classes: RTE prompt-chaining (config depth inside an owned
module), Epic ASA build (auth-requirement grid accuracy), order sets (lookup-key lineage for
the prior-auth family), scheduling trees/visit types (same class, access side). Scope decisions
confirmed with the owner: **both vendors at full depth** (confidence-flagged), **floors revised
in place** (staleness notes, no simulation rerun), **decide-and-log** for judgment calls.

## The four gap classes and their class-level fixes

| Class | Specimen | Fix applied ontology-wide |
|---|---|---|
| Configured-to-depth | RTE chaining | Three-state ladder (licensed/lit/configured-to-depth) as file 14 Rule 0; floors deepened; depth markers per module in vendor crosswalks |
| Input lineage (C6) | ASA, order-set CPTs | New dependency-audit class C6; 5 new facets; 6 UC vectors amended; spine actions for key derivation/governance |
| Causal misattribution | PFM-1.3-01 blaming verifiers for config debt | 6 config-root-cause sibling PFMs so reconcile.py chains prescribe build fixes vs coaching |
| Native sourcing blindness | "EHR already does this" absent from option set | `native_module` cost option; OFM/BP-ET-09; `native_capability_inventory`; vendor crosswalk native catalogs |

## Added

**Facets (catalog 98 → 103)** — `gate-vectors.yaml`:
`rte_benefit_depth` (connectivity), `auth_grid_accuracy` (data), `intended_cpt_accuracy`
(data), `clinical_build_governance` (workflow), `native_capability_inventory` (workflow).
All class `failure-explained` — each is causally explained by a named OFM/PFM, unlike the
new-capability facets whose weakness needs no operational explanation.

**UC vector amendments (C6)** — 01-04 (+rte_benefit_depth), 01-07 (+intended_cpt_accuracy),
01-08 (+auth_grid_accuracy, intended_cpt_accuracy), 01-12 (+rte_benefit_depth,
intended_cpt_accuracy), 03-06 (+clinical_build_governance), 07-02 (+masterdata_governance).
Round-2 table in `13-dependency-audit.md`; header note in file 08.

**Spine actions** — `1.1.2.A9` intended-CPT derivation ({produces: intended CPT set});
`1.3.1.A4` payer-specific eligibility query configuration; `1.4.1.A4` auth-grid governance;
`14.2.A6 + D1` revenue review of clinical build changes (the boundary process — a deliberate,
minimal scope extension so build-blindside findings have a binding anchor; the spine still
does not absorb CPOE/clinical ontology).

**PFMs (162 → 168)** — config-root-cause siblings of behavioral PFMs:
- `PFM-1.1-05` scheduling-tree/visit-type build defects (sibling of 1.1-02's behavioral slot)
- `PFM-1.3-05` benefit detail structurally absent from 271s (sibling of 1.3-01)
- `PFM-1.4-05` auth grid ungoverned as build (sibling of 1.4-01)
- `PFM-3.1-05` clinical build unreviewed into the charge surface (sibling of 3.1-01)
- `PFM-5.5-02` specialty billing build unvalidated (sibling of 5.5-01 — coaching cannot fix
  system arithmetic)
- `PFM-14.2-02` clinical build with no RC seat (enterprise-process anchor; 1.1-05/3.1-05 are
  its local instances)

**OFM/BP (AD-04: 8 → 10)** — `OFM-ET-09` native capability licensed-but-unlit / `BP-ET-09`
native-first sourcing with capability inventory; `OFM-ET-10` clinical build blindside /
`BP-ET-10` revenue-embedded clinical build governance. Maturity anchors L0–L4 extended.
Checklist + couplings wired.

**Sourcing option** — `native_module` (build_mult 0.15, maintenance 8%) added to
`option_build_mult`, `maintenance_pct`, and the rules/rpa/ml workload option sets; cost-model
§2 row + decision-procedure step 0 (native check).

**Vendor crosswalks** — `vendor-crosswalks/{README,epic,oracle-health}.yaml`: full facet
coverage (stack-agnostic facets grouped honestly rather than given fake vendor content),
build_surfaces (ASA/auth grids, order sets/PowerPlans, scheduling trees/appointment types,
preference cards, documentation templates, anesthesia build, eligibility query config, charge
triggers, claim edits, statement config, estimator config), native AI catalogs, per-entry
confidence + `as_of: 2026-07`.

## Changed

- **Floors revised in place** (file 14): `era_coverage`/`claim_status_edi` gained a
  consumed-as-data clause; `auth_transactions` gained structured-response capture;
  `cds_ordering_hook` gained the alert-burden-governance clause (a hook nobody may add rules
  to scores 1). Version note in file 14 §8; scoring README carries the re-score warning;
  Meridian simulation carries `STALENESS-NOTE.md`.
- `rte_eligibility` floor **kept** at volume and depth split into `rte_benefit_depth` — see
  judgment calls below.
- Counts and descriptions across the four READMEs; root README documents the crosswalk layer.

## Judgment calls (decide-and-log)

| Decision | Call | Rationale |
|---|---|---|
| RTE depth: revise floor vs new facet | **New facet** (`rte_benefit_depth`), floor kept volume-only | Causality classes differ: enrollment coverage is `new-capability` (weakness needs no OFM explanation), query-depth debt is `failure-explained` (PFM-1.3-05 explains it). Folding both into one facet breaks reconcile.py's ENG-01 class logic. The false-positive is still eliminated — depth gates the same UCs. Spirit of "revise in place" honored: no false floor survives. |
| `auth_grid_accuracy` on UC-01-07 | **Not added** (01-08 only) | Circular: 01-07's product *is* grid accuracy; gating the builder on its own output would DEFER the remediation of the very gap it fixes. 01-07 got `intended_cpt_accuracy` instead (its lookup key). |
| Lineage facets on detector UCs (01-10 auth-to-service, 14-02 drift monitor) | **Not added** | Their purpose is *catching* key drift; presupposing measured keys would gate the detector on the detected. |
| `contract_engine_loaded` on UC-09-01 | **Not added** | Round-1 audit confirmed RC-09 as-is; expected-value can bootstrap from payment history; not month-one decisive. Anti-inflation bias governs. |
| Notification-window grids (UC-02-03) | **Not added** | Real but folded into payer-requirement masters (`masterdata_governance` altitude); a dedicated facet would be inflation. |
| `native_module` in idp/nlp/llm/conv workloads | **Not added** | Native document/generative AI coverage is too shop- and release-specific as of the stamp; crosswalk native_catalog carries it with confidence flags, and the cost doc says to price it via overrides when shipping-today evidence exists. Revisit at next true-up. |
| PFM-7.1-03 / UC-07-02 alignment | **Vector amended only** | The PFM already coupled `masterdata_governance`; the UC vector lacked it — a pre-existing asymmetry the C6 sweep caught. |
| Role layer (file 17) | **Untouched** | The four classes are build/config-layer by definition; role-level judgment surfaces are unaffected. ROLE-SYSANALYST failure patterns already exist (RFM-SYS-*). |
| Where the clinical-build OFM lives | **AD-04** (not AD-01) | The failure is an estate/boundary property (what ships into revenue surfaces), not an accountability-structure property; OFM-OM-08 remains the *capacity* failure, ET-10 the *governance-boundary* failure. Cross-coupled through `clinical_build_governance`. |
| Oracle Health confidence | **Full depth, flagged** | Owner accepted lower-confidence entries; `needs-sme-validation` marks the auth-grid location and RevElate-transition surfaces as field hypotheses, not facts. |
| Meridian / example artifacts | **Staleness notes, no rerun** | Per owner decision; `score.py` degrades gracefully (warns, treats new facets as 0). |

## Validation

`build_field_instrument.py` and `reconcile.py` rerun after the change (couplings.yaml is
generated — never hand-edited); planner app and explorer rebuilt from the amended drivers.
See commit for the regenerated artifacts and validation output.
