# CLAUDE.md

Guidance for Claude Code when working in this repository.

## What this repository is

A machine-parseable **ontology of healthcare revenue cycle operations** plus companion layers
that build on it. Almost everything is structured Markdown and YAML; the only code is a small
Python 3 toolkit (sole dependency: **PyYAML** — `pip install pyyaml`). There is no build system,
package manager, or test runner at the repo root.

Everything lives under `revenue-cycle-ontology/`. The system has four layers, each with its own
README that is the authoritative deep documentation:

| Layer | Location | What it is |
|---|---|---|
| 1. Base process ontology | `revenue-cycle-ontology/` (files `00`–`10`) | 14 domains (`RC-01`–`RC-14`), 88 processes, sub-processes, decisions, actions + cross-cutting registries (roles, systems, artifacts, KPIs, failure modes, events) |
| 2. AI & automation ontology | `ai-automation/` | 103 use cases (`UC-*`) bound to base-ontology IDs, with governance (autonomy ceilings), feasibility gating, value model, cost model, investment playbook |
| 3. Operations assessment | `operations-assessment/` | Failure modes (`OFM-*`/`PFM-*`/`RFM-*`) and best practices (`BP-*`) across 3 layers (enterprise → process → role), coupled to the AI readiness gates they degrade |
| 4. Vendor crosswalks | `vendor-crosswalks/` | Disposable, `as_of`-stamped bindings from neutral IDs to named EHR modules (Epic, Oracle Health) |
| 5. Digital twin | `digital-twin/` | Deterministic monthly flow simulation of the whole operation ($10B-NPR archetype baseline); scenarios (workflow, AI/automation via `UC-*`, staffing) → financial, productivity, and patient/caregiver experience impact |

## Key files

- `revenue-cycle-ontology/README.md` — meta-model: entity classes, ID patterns, relationship
  verbs, decision/action notation. **Read this before editing any ontology file.**
- `00-master-taxonomy.md` — the complete hierarchical index (the "spine"). Domain files
  `01-*.md` … `09-*.md` carry the detail; `10-cross-cutting-entities.md` holds the ID
  registries (`ROLE-*`, `SYS-*`, `ART-*`, `KPI-*`, `FM-*`, `EVT-*`).
- `ai-automation/scoring/gate-vectors.yaml` — authoritative machine-readable encoding of the
  facet catalog (103 facets) and every UC's gate profile.
- `operations-assessment/field-instrument.yaml` — generated instrument (286 items); built by
  `build_field_instrument.py`, do not hand-edit.
- `decision-log-*.md` — structural engineering decisions. Major structural changes get logged
  here (see the 2026-07 depth/lineage log for the format).

## ID scheme (how everything links)

Every entity has a stable ID and layers reference each other only by ID:
processes `1.4.2`, decisions `1.4.2.D1`, actions `1.4.2.A3`, domains `RC-*`, use cases
`UC-<domain>-<nn>`, failure modes `FM-*` (base) / `OFM-*` / `PFM-*` / `RFM-*` (assessment),
best practices `BP-*`, facets are snake_case keys in `gate-vectors.yaml`, controls `GOV-*`,
capabilities `CAP-*`, patterns `PAT-*`, autonomy `A0`–`A4`, risk `R1`–`R4`.

When adding or renaming an ID, find and update every cross-reference — the coupling files
(`operations-assessment/pfm-couplings.yaml`, `couplings.yaml`) and `gate-vectors.yaml` are
validated against the registries by `reconcile.py`, so run it after ontology edits.

## Runnable toolkit

All scripts are Python 3 + PyYAML, run from their own directory.

`ai-automation/scoring/` (feasibility → value → cost → packet pipeline):

```bash
python3 score.py --init my-org.yaml        # blank assessment worksheet
python3 score.py my-org.yaml -o report.md --csv report.csv [--html report.html]
python3 value.py ...                       # value model (joins feasibility)
python3 cost.py ... [--roi]                # cost model / ROI join
python3 packet.py ...                      # quarterly investment packet (runs all three)
python3 build_app.py                       # rebuild rcm-investment-app.html from driver YAMLs
python3 build_explorer.py                  # rebuild use-case-explorer.html
```

`operations-assessment/`:

```bash
python3 build_field_instrument.py          # regenerate field-instrument.yaml/.html from sources
python3 reconcile.py --scores S.yaml --facets A.yaml [--profile P.yaml] [-o report.md]
```

`digital-twin/` (operational simulation; see its README for the meta-model):

```bash
python3 twin.py --diag                     # baseline pool-utilization sanity check
python3 twin.py -o report.md               # baseline run
python3 twin.py --scenario scenarios/SCN-01-ai-automation-wave1.yaml -o r.md [--csv m.csv] [--json r.json]
python3 twin.py --compare scenarios/SCN-0*.yaml -o comparison.md
```

`digital-twin/twin-config.yaml` and `scenarios/*.yaml` are source; `examples/*` are
generated run records (regenerate, don't hand-edit).

The HTML artifacts (`rcm-investment-app.html`, `use-case-explorer.html`,
`field-instrument.html`) are **generated, self-contained files** — never edit them directly;
edit the templates/driver YAMLs/source markdown and rerun the build script.

## Invariants to preserve

1. **The neutral layer governs.** Vendor crosswalks never define a gate — they locate it on a
   named stack. Ontology semantics live in the neutral files; `vendor-crosswalks/*.yaml` is
   deliberately disposable and carries per-entry `as_of` stamps and confidence flags.
2. **Autonomy ceiling.** A use case's autonomy level (`A0`–`A4`) may never exceed its risk
   tier's ceiling (`R1`–`R4`), regardless of performance (`ai-automation/README.md`).
3. **Weakest-link scoring.** Facet/dimension scoring is evidence-based and pessimistic by
   design ("score 2 only if you could demo it this week"); don't soften scoring guidance.
4. **Generated ≠ source.** YAML driver files and markdown are source; HTML apps and
   `field-instrument.yaml` are build outputs.
5. **Assessments are records.** Filled assessment YAMLs are committed, diffed, never
   overwritten — history is the audit trail.
6. **Version stamps matter.** Facet-catalog changes make older assessments non-comparable
   (see the 2026-07 floor note in `scoring/README.md`); `reconcile.py` refuses version
   mismatches by design.

## Editing conventions

- Follow the decision/action notation in `revenue-cycle-ontology/README.md` exactly
  (`D<n>.` question trees with `├─`/`└─` branches; `A<n>.` verb-first actions with
  `[role] [system] {produces: artifact}` tags).
- New failure modes/best practices follow the paired OFM→BP / PFM→PBP structure with
  field-observable `signals`, `damages` (RC-*/KPI-*), and `degrades` (facet) bindings.
- Counts are load-bearing: READMEs cite exact totals (103 facets, 103 UCs, 286 instrument
  items, 168 PFMs…). If an edit changes a count, update every README that states it.
- Log structural changes (new gap classes, facet additions, spine extensions) in a
  `decision-log-YYYY-MM-*.md` file.
