# Decision Log — 2026-07 Dual-Track Outputs

Framing correction surfaced in review: the system's terminal outputs (reconcile report, quarterly
packet, council agenda) were AI-portfolio-shaped only. The operations assessment fed the pipeline
solely as *cause of weak facets* and *priced locked automation value* — its own prescriptions
(the paired `BP-*`/PBP/RBP practices, typed by fix layer) never appeared in any generated output,
even though the source ontology carries them and the README states the fix differs by layer.
Result: an assessment consumer would reasonably conclude the system's end product is automations
and AI, when process and operating-model improvements should be an equal or larger share.

## Decision

The pipeline's terminal outputs are **dual-track by construction**: an operational improvement
plan and an AI investment portfolio, in one packet, decided at one council. The operational track
is priced standalone (FM→pool bindings hold whether the cure is procedural or automated); AI-gate
unlock is reported as the secondary benefit, never the justification.

## Changes (ENG-07)

| Where | Change |
|---|---|
| `operations-assessment/reconcile.py` | New reconciliation-mode section **"Operational improvement plan (ENG-07)"**: every flagged finding with its paired-practice prescription (OFM → `BP-*` via the 1:1 numbered pairing; PFM/RFM → captured practice text), fix layer (structure/incentives · standard work/tooling · coaching/competency), standalone $ at stake (with `--profile`), and degraded AI gates as the secondary-benefit column. Sorted score-2-first, then by $ |
| `ai-automation/scoring/packet.py` | New `--ops-report` flag binds the reconcile report into the packet as `operations.md`; council agenda restructured to two tracks with **Operational improvements** as item 3, ahead of technical remediation funding |
| `ai-automation/11-investment-loop-playbook.md` | Play 2 agenda: new item 3 **Operational improvements (15 min)**; remediation funding trimmed to 15 min, autonomy promotions and kills to 10 min each (total stays 120); technical remediations ride the operational root-cause project where one is funded |
| `operations-assessment/README.md` | New section **"Two output tracks, one packet"** stating the co-equal contract; `reconcile.py` table row documents ENG-07 |
| `ai-automation/scoring/README.md` | `packet.py` row documents `--ops-report` and the dual-track packet |

## Invariants

- No ontology content changed: no new IDs, facets, findings, or bindings; counts (103 facets,
  103 UCs, 286 items, 168 PFMs) unchanged. This is an output-layer and operating-cadence fix.
- The OFM→BP prescription lookup relies on the 1:1 numbered pairing per enterprise domain file
  (verified 8/8, 7/7, 8/8, 10/10, 6/6, 5/5). A future OFM/BP whose numbers diverge must update
  `bp_titles()` in `reconcile.py` to parse explicit `Prevents:` bindings instead.
- `field-instrument.yaml`/`couplings.yaml` regeneration unaffected (`source_version` unchanged —
  instrument sources were not edited).
