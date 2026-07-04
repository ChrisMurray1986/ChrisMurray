# Staleness note — 2026-07 depth/lineage expansion

This simulation (assessment, field scores, feasibility, packet, roadmap) was produced against
the **pre-2026-07** registries: facet catalog of 98 (now 103), original floor semantics for
`rte_eligibility`-class facets, 278-item field instrument (now 286), and no `native_module`
sourcing option.

Consequences, per the revise-in-place decision recorded in
`../../../../decision-log-2026-07-depth-lineage.md`:

- `score.py` runs against `meridian-assessment.yaml` now warn that 5 facets are unscored and
  treat them as 0 (absent) — which can only *worsen* dispositions for UC-01-04, 01-07, 01-08,
  01-12, 03-06, and 07-02. The recorded dispositions here reflect the old gates.
- `meridian-field-scores.yaml` carries a pre-expansion `source_version`; `reconcile.py`
  refuses it against the regenerated instrument (ENG-06) unless `--allow-version-mismatch`.
- These artifacts are retained as a worked example of the *method*, not as a current scoring
  reference. Re-score the five new facets and re-run the pipeline before reusing any figure.
