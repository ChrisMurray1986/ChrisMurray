# Vendor Crosswalks — Native Capability Bindings

The ontology's facets, processes, and gate vectors are deliberately **vendor-neutral**; vendor
packaging churns on marketing cycles while operational reality churns on years. This layer is
where the two meet without contaminating each other: **machine-readable, versioned, deliberately
disposable** bindings from neutral IDs (facets, processes, PFMs, UCs) to the named modules,
build surfaces, and first-party AI capabilities of a specific EHR vendor.

It exists to answer three assessment questions that file 14 (`ai-automation/
14-implementation-patterns.md`) poses but cannot carry per-module detail for:

1. **Score, don't build** — which facets is this shop likely already passing natively? (Rule 0)
2. **Configured-to-depth** — the module is licensed and lit; is it producing the output the
   dependent process needs? (`depth_markers`: two-minute field demos, each bound to the PFM
   symptom it explains)
3. **Native-first sourcing** — before pricing `vendor`/build options, does a native module
   cover the gate? (feeds the cost model's `native_module` option and BP-ET-09)

## Files

| File | Vendor scope |
|---|---|
| `epic.yaml` | Single-instance Epic (Chronicles, Clarity/Caboodle, Resolute HB/PB, Prelude/Cadence, Interconnect/FHIR) |
| `oracle-health.yaml` | Oracle Health / Cerner Millennium (+ RevElate patient accounting) |

## Schema

```yaml
meta:
  vendor: ""            # display name
  as_of: "YYYY-MM"      # knowledge date — entries decay; verify before committing a plan
  confidence_legend: {high: ..., medium: ..., needs-sme-validation: ...}

facets:                 # keyed by facet id from gate-vectors.yaml facet_catalog
  <facet_id>:
    module: ""          # where the capability lives in this vendor's stack
    states:             # the three-state ladder (file 14 Rule 0)
      licensed: ""      # what owning it means here
      lit: ""           # what enabled/enrolled looks like
      configured_to_depth: ""   # what a passing (score-2) configuration produces
    depth_markers:      # field-checkable pathologies; empty list = depth == lit
      - id: ""          # slug
        check: ""       # the two-minute demo
        symptom_binding: PFM-*    # the process failure this depth defect explains
        facet_binding: <facet_id> # the facet the marker scores (defaults to parent)
    confidence: high|medium|needs-sme-validation
    note: ""            # overbuild/licensing/scope caveats

stack_agnostic:         # facets whose floor is policy/committee/contract, not modules
  see: ""               # pointer to file 14 §6
  facets: []

build_surfaces:         # upstream build whose defects propagate into revenue processes (C6)
  <surface_id>:
    module: ""
    feeds: []           # process/UC ids that consume this build's outputs
    depth_markers: []   # same shape as above
    symptom_binding: [] # PFMs explained by defects here
    confidence: ...

native_catalog:         # first-party automation/AI capability (OFM-ET-09 / BP-ET-09 inventory seed)
  - capability: ""
    module: ""
    gates_addressed: [] # facets/UCs a lit+deep deployment can satisfy or substitute for
    sourcing_note: ""   # what native coverage means for the option set
    confidence: ...
```

## Rules of use

- **The neutral layer governs.** A crosswalk entry never *defines* a gate; it locates and
  demos the neutral floor on a named stack. Where this file and `gate-vectors.yaml`/file 14
  disagree, they govern.
- **`as_of` is load-bearing.** Module names, packaging, and licensing change; entries carry
  the stamp so staleness is visible instead of silently wrong. Refresh triggers are file 14
  §8's (major upgrades, clearinghouse changes, annual audit sweep).
- **Confidence is per-entry.** `needs-sme-validation` entries are structured hypotheses for
  the field team to confirm on site — never plan-committing facts.
- **Native AI passes no governance for free.** A native predictive/generative capability
  still crosses every GOV-* gate (bias program, decision logging, citation harness) exactly
  like a bolt-on or build — `native_module` changes the cost row, not the risk tier.
- **Adding a vendor** = one new YAML in this schema; the neutral ontology does not change.
