#!/usr/bin/env python3
"""Feasibility scoring for the AI/automation use case catalog.

Computes a GO / CONDITIONAL / DEFER / KILL disposition for every use case in
gate-vectors.yaml given an organization's filled-in assessment, applying the
rules of 07-feasibility-gating.md:

  - weakest-link gating: a UC is only as ready as its least ready mandatory gate
  - KILL        any required facet scored "blocked" (legal/contractual prohibition)
  - DEFER       structural gap: a dimension >=2 levels short, a dimension at 0-1
                where >=3 is required, or a required facet scored 0 (absent)
  - CONDITIONAL remaining gaps are small (dimension 1 short, facet partial)
  - GO          all gates met
  - insight-only downgrade: a CONDITIONAL/DEFER use case with no data gap and no
                blocked facet can usually launch at A0/A1 (worklist output) while
                remediation proceeds

Usage:
  score.py --init assessment.yaml          write a blank assessment template
  score.py assessment.yaml                 print markdown report to stdout
  score.py assessment.yaml -o report.md    write markdown report
  score.py assessment.yaml --csv out.csv   also write per-UC CSV
"""

import argparse
import csv
import sys
from collections import Counter
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required: pip install pyyaml")

DIM_KEYS = {
    "D": "data", "I": "integration", "C": "connectivity", "W": "workflow",
    "O": "org", "V": "governance", "E": "economics", "L": "legal",
}
DIM_ORDER = ["data", "integration", "connectivity", "workflow", "org",
             "governance", "economics", "legal"]
VALID_FACET = {0, 1, 2}


def load_vectors(path):
    with open(path) as f:
        doc = yaml.safe_load(f)
    return doc["facet_catalog"], doc["use_cases"]


def write_template(path, catalog):
    lines = [
        "# Organization readiness assessment — fill in and run score.py against it.",
        "#",
        "# dimensions: overall maturity 0-4 per gate dimension",
        "#   (level anchors: 07-feasibility-gating.md; economics/legal top out at 3)",
        "# facets: 0 = absent, 1 = partial/in progress, 2 = ready.",
        "#   Facets marked (blockable) may instead be the string: blocked",
        "#   meaning legally/contractually prohibited, which KILLs dependent use cases.",
        "",
        "org:",
        "  name: \"<organization>\"",
        "  assessed_by: \"<assessor>\"",
        "  date: \"<yyyy-mm-dd>\"",
        "",
        "dimensions:",
    ]
    for dim in DIM_ORDER:
        lines.append(f"  {dim}: 0")
    lines += ["", "facets:"]
    cur = None
    for fid, meta in catalog.items():
        if meta["dim"] != cur:
            cur = meta["dim"]
            lines.append(f"  # ---- {cur} ----")
        tag = " (blockable)" if meta.get("blockable") else ""
        lines.append(f"  {fid}: 0  # {meta['prompt']}{tag}")
    Path(path).write_text("\n".join(lines) + "\n")
    print(f"Template written to {path}")


def validate(assessment, catalog):
    problems = []
    dims = assessment.get("dimensions") or {}
    for dim in DIM_ORDER:
        v = dims.get(dim)
        if not isinstance(v, int) or not 0 <= v <= 4:
            problems.append(f"dimensions.{dim}: expected integer 0-4, got {v!r}")
    facets = assessment.get("facets") or {}
    for fid, val in facets.items():
        if fid not in catalog:
            problems.append(f"facets.{fid}: unknown facet (not in gate-vectors catalog)")
        elif val == "blocked":
            if not catalog[fid].get("blockable"):
                problems.append(f"facets.{fid}: 'blocked' only valid for blockable facets")
        elif val not in VALID_FACET:
            problems.append(f"facets.{fid}: expected 0/1/2 or 'blocked', got {val!r}")
    missing = [fid for fid in catalog if fid not in facets]
    return problems, missing


def score_uc(uc, dims, facets, catalog):
    """Return (disposition, gap list, downgrade_available)."""
    blocked, structural, conditional = [], [], []

    for letter, req in uc["vector"].items():
        if req is None:
            continue
        dim = DIM_KEYS[letter]
        have = dims.get(dim, 0)
        if have >= req:
            continue
        desc, key = f"{dim} {have}->{req}", f"dimension {dim}>={req}"
        if req - have >= 2 or (have <= 1 and req >= 3):
            structural.append((desc, dim, key))
        else:
            conditional.append((desc, dim, key))

    for fid in uc.get("facets", []):
        val = facets.get(fid, 0)
        fdim = catalog[fid]["dim"]
        if val == "blocked":
            blocked.append((f"{fid} [BLOCKED]", fdim, f"facet {fid}"))
        elif val == 0:
            structural.append((f"{fid} (absent)", fdim, f"facet {fid}"))
        elif val == 1:
            conditional.append((f"{fid} (partial)", fdim, f"facet {fid}"))

    if blocked:
        dispo = "KILL"
    elif structural:
        dispo = "DEFER"
    elif conditional:
        dispo = "CONDITIONAL"
    else:
        dispo = "GO"

    gaps = blocked + structural + conditional
    data_gap = any(dim == "data" for _, dim, _ in gaps)
    downgrade = dispo in ("CONDITIONAL", "DEFER") and not data_gap and not blocked
    return dispo, gaps, downgrade


def build_report(assessment, catalog, use_cases):
    dims = assessment.get("dimensions") or {}
    facets = assessment.get("facets") or {}
    org = assessment.get("org") or {}

    rows = []
    gap_counter = Counter()   # blocking item -> # UCs it appears in
    sole_gap_counter = Counter()
    for uc_id, uc in use_cases.items():
        dispo, gaps, downgrade = score_uc(uc, dims, facets, catalog)
        rows.append({
            "id": uc_id, "name": uc["name"], "disposition": dispo,
            "gaps": [g for g, _, _ in gaps], "downgrade": downgrade,
            "note": uc.get("note", ""),
        })
        for _, _, key in gaps:
            gap_counter[key] += 1
        if len(gaps) == 1:
            sole_gap_counter[gaps[0][2]] += 1

    counts = Counter(r["disposition"] for r in rows)
    order = {"GO": 0, "CONDITIONAL": 1, "DEFER": 2, "KILL": 3}
    rows.sort(key=lambda r: (order[r["disposition"]], r["id"]))

    lines = []
    name = org.get("name", "<unnamed>")
    lines.append(f"# Feasibility scoring report — {name}")
    lines.append(f"\nAssessed by {org.get('assessed_by', '?')} on {org.get('date', '?')}. "
                 f"{len(rows)} use cases scored.\n")
    lines.append("## Portfolio summary\n")
    lines.append("| Disposition | Count |")
    lines.append("|---|---|")
    for d in ["GO", "CONDITIONAL", "DEFER", "KILL"]:
        lines.append(f"| {d} | {counts.get(d, 0)} |")
    dg = sum(1 for r in rows if r["downgrade"])
    lines.append(f"\nInsight-only (A0/A1) downgrade available for **{dg}** of the "
                 f"blocked/conditional use cases.\n")

    lines.append("## Dimension scores\n")
    lines.append("| " + " | ".join(DIM_ORDER) + " |")
    lines.append("|" + "---|" * len(DIM_ORDER))
    lines.append("| " + " | ".join(str(dims.get(d, 0)) for d in DIM_ORDER) + " |")

    lines.append("\n## Highest-leverage remediations\n")
    lines.append("Blocking items ranked by number of use cases they hold back "
                 "(sole-blocker count in parentheses):\n")
    for item, n in gap_counter.most_common(15):
        lines.append(f"- **{item}** — blocks {n} use case(s) ({sole_gap_counter.get(item, 0)} solely)")

    lines.append("\n## Per-use-case results\n")
    lines.append("| UC | Name | Disposition | Gaps | A0/A1 start | Note |")
    lines.append("|---|---|---|---|---|---|")
    for r in rows:
        gaps = "; ".join(r["gaps"]) if r["gaps"] else "—"
        lines.append(f"| {r['id']} | {r['name']} | {r['disposition']} | {gaps} | "
                     f"{'yes' if r['downgrade'] else ''} | {r['note']} |")
    return "\n".join(lines) + "\n", rows


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("assessment", nargs="?", help="filled-in assessment YAML")
    ap.add_argument("--vectors", default=str(Path(__file__).parent / "gate-vectors.yaml"))
    ap.add_argument("--init", metavar="PATH", help="write a blank assessment template and exit")
    ap.add_argument("-o", "--output", help="write markdown report to file (default stdout)")
    ap.add_argument("--csv", help="also write per-UC results as CSV")
    args = ap.parse_args()

    catalog, use_cases = load_vectors(args.vectors)

    if args.init:
        write_template(args.init, catalog)
        return
    if not args.assessment:
        ap.error("provide an assessment file, or --init to create one")

    with open(args.assessment) as f:
        assessment = yaml.safe_load(f)

    problems, missing = validate(assessment, catalog)
    if problems:
        sys.exit("Assessment invalid:\n  " + "\n  ".join(problems))
    if missing:
        print(f"warning: {len(missing)} facet(s) not scored, treated as 0 (absent): "
              + ", ".join(missing[:8]) + ("..." if len(missing) > 8 else ""),
              file=sys.stderr)

    report, rows = build_report(assessment, catalog, use_cases)

    if args.output:
        Path(args.output).write_text(report)
        print(f"Report written to {args.output}")
    else:
        print(report)

    if args.csv:
        with open(args.csv, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["uc_id", "name", "disposition", "gaps", "a0_a1_start", "note"])
            for r in rows:
                w.writerow([r["id"], r["name"], r["disposition"],
                            "; ".join(r["gaps"]), "yes" if r["downgrade"] else "no",
                            r["note"]])
        print(f"CSV written to {args.csv}")


if __name__ == "__main__":
    main()
