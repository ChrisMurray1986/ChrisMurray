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
import json
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

DOMAIN_NAMES = {
    "01": "Patient Access", "02": "Utilization Review", "03": "Charge Capture",
    "04": "CDI", "05": "Coding", "06": "Claims", "07": "Payments",
    "08": "Denials & Appeals", "09": "AR Management", "10": "Patient Financial Svcs",
    "11": "Contracting", "12": "Compliance", "13": "Analytics", "14": "Master Data & Tech",
}


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


def analyze(assessment, catalog, use_cases):
    """Score every UC; return the structured results both renderers consume."""
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
            "domain": DOMAIN_NAMES.get(uc_id.split("-")[1], "?"),
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
    return {"org": org, "dims": dims, "rows": rows, "counts": counts,
            "gap_counter": gap_counter, "sole_gap_counter": sole_gap_counter}


def build_report(assessment, catalog, use_cases):
    res = analyze(assessment, catalog, use_cases)
    org, dims, rows = res["org"], res["dims"], res["rows"]
    counts = res["counts"]
    gap_counter, sole_gap_counter = res["gap_counter"], res["sole_gap_counter"]

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


HTML_TEMPLATE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
  :root {
    --page: #f9f9f7; --surface: #fcfcfb; --ink: #0b0b0b; --ink-2: #52514e;
    --muted: #898781; --grid: #e1e0d9; --baseline: #c3c2b7;
    --ring: rgba(11,11,11,0.10);
    --seq: #2a78d6; --seq-soft: #9ec5f4;
    --good: #0ca30c; --warning: #fab219; --serious: #ec835a; --critical: #d03b3b;
    --good-ink: #006300; --warning-ink: #7a5200; --serious-ink: #9c3f1d; --critical-ink: #d03b3b;
  }
  @media (prefers-color-scheme: dark) {
    :root {
      --page: #0d0d0d; --surface: #1a1a19; --ink: #ffffff; --ink-2: #c3c2b7;
      --muted: #898781; --grid: #2c2c2a; --baseline: #383835;
      --ring: rgba(255,255,255,0.10);
      --seq: #3987e5; --seq-soft: #1c5cab;
      --good-ink: #0ca30c; --warning-ink: #fab219; --serious-ink: #ec835a; --critical-ink: #d03b3b;
    }
  }
  * { box-sizing: border-box; }
  body { margin: 0; background: var(--page); color: var(--ink);
         font: 14px/1.5 system-ui, -apple-system, "Segoe UI", sans-serif; }
  .wrap { max-width: 1100px; margin: 0 auto; padding: 28px 20px 60px; }
  h1 { font-size: 21px; margin: 0 0 2px; }
  h2 { font-size: 15px; margin: 34px 0 12px; }
  .sub { color: var(--ink-2); margin: 0 0 24px; }
  .card { background: var(--surface); border: 1px solid var(--ring); border-radius: 10px; padding: 16px; }

  .tiles { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; }
  .tile { background: var(--surface); border: 1px solid var(--ring); border-radius: 10px;
          padding: 12px 14px; border-top: 3px solid var(--baseline); }
  .tile .v { font-size: 26px; font-weight: 650; }
  .tile .l { color: var(--ink-2); font-size: 12.5px; }
  .tile .g { font-size: 12.5px; font-weight: 600; }

  .dims { display: grid; grid-template-columns: repeat(auto-fit, minmax(112px, 1fr)); gap: 10px; }
  .dim .name { font-size: 12px; color: var(--ink-2); display: flex; justify-content: space-between; }
  .dim .name b { color: var(--ink); font-variant-numeric: tabular-nums; }
  .meter { display: flex; gap: 2px; margin-top: 4px; }
  .meter span { height: 8px; flex: 1; border-radius: 3px; background: var(--grid); }
  .meter span.on { background: var(--seq); }

  .bars .row { display: grid; grid-template-columns: 300px 1fr; gap: 10px; align-items: center;
               padding: 3px 0; border-radius: 6px; }
  .bars .row:hover { background: var(--grid); }
  .bars .lbl { font-size: 12.5px; color: var(--ink-2); text-align: right;
               white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .bars .lbl code { font-family: inherit; color: var(--ink); }
  .bars .track { position: relative; height: 14px; }
  .bars .bar { position: absolute; inset: 0 auto 0 0; background: var(--seq);
               border-radius: 0 4px 4px 0; min-width: 2px; }
  .bars .val { position: absolute; top: -1px; font-size: 12px; color: var(--ink-2);
               font-variant-numeric: tabular-nums; white-space: nowrap; }
  .axis-note { color: var(--muted); font-size: 12px; margin-top: 8px; }

  .filters { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin: 0 0 12px; }
  .filters input[type=search], .filters select {
    background: var(--surface); color: var(--ink); border: 1px solid var(--ring);
    border-radius: 8px; padding: 6px 10px; font: inherit; }
  .chip { border: 1px solid var(--ring); background: var(--surface); color: var(--ink-2);
          border-radius: 999px; padding: 5px 12px; font: inherit; font-size: 12.5px; cursor: pointer; }
  .chip[aria-pressed="true"] { color: var(--ink); font-weight: 650; border-color: var(--baseline);
          box-shadow: inset 0 0 0 1px var(--baseline); }
  .count-note { color: var(--muted); font-size: 12.5px; margin-left: auto; }

  .tblwrap { overflow-x: auto; }
  table { border-collapse: collapse; width: 100%; font-size: 13px; }
  th { text-align: left; color: var(--muted); font-weight: 600; font-size: 12px;
       border-bottom: 1px solid var(--baseline); padding: 6px 10px; white-space: nowrap; }
  td { border-bottom: 1px solid var(--grid); padding: 7px 10px; vertical-align: top; }
  tr:hover td { background: var(--grid); }
  td.ucid { font-variant-numeric: tabular-nums; white-space: nowrap; color: var(--ink-2); }
  .badge { display: inline-flex; align-items: center; gap: 5px; font-weight: 650; font-size: 12px;
           white-space: nowrap; }
  .badge .dot { width: 9px; height: 9px; border-radius: 3px; }
  .b-GO .dot { background: var(--good); } .b-GO { color: var(--good-ink); }
  .b-CONDITIONAL .dot { background: var(--warning); } .b-CONDITIONAL { color: var(--warning-ink); }
  .b-DEFER .dot { background: var(--serious); } .b-DEFER { color: var(--serious-ink); }
  .b-KILL .dot { background: var(--critical); } .b-KILL { color: var(--critical-ink); }
  .gap { display: inline-block; border: 1px solid var(--ring); border-radius: 6px;
         padding: 1px 6px; margin: 1px 2px 1px 0; font-size: 11.5px; color: var(--ink-2);
         background: var(--surface); }
  .gap.hard { border-color: var(--serious); }
  .gap.blk { border-color: var(--critical); color: var(--critical-ink); }
  .dg { color: var(--good-ink); font-weight: 650; font-size: 12px; white-space: nowrap; }
  .note { color: var(--muted); font-size: 12px; }
  footer { color: var(--muted); font-size: 12px; margin-top: 40px; }
</style></head>
<body>
<div class="wrap">
  <h1>Feasibility scoring report</h1>
  <p class="sub" id="sub"></p>

  <div class="tiles" id="tiles"></div>

  <h2>Dimension maturity <span class="axis-note">(assessed level of 4 — anchors in 07-feasibility-gating.md)</span></h2>
  <div class="card dims" id="dims"></div>

  <h2>Highest-leverage remediations</h2>
  <div class="card bars" id="bars"></div>

  <h2>Use cases</h2>
  <div class="filters" id="filters">
    <input type="search" id="q" placeholder="Search name, gap, note&hellip;" aria-label="Search use cases">
    <select id="domain" aria-label="Filter by domain"></select>
    <span id="chips"></span>
    <span class="count-note" id="shown"></span>
  </div>
  <div class="card tblwrap">
    <table id="tbl">
      <thead><tr>
        <th>UC</th><th>Name</th><th>Domain</th><th>Disposition</th>
        <th>Gaps</th><th>A0/A1 start</th><th>Note</th>
      </tr></thead>
      <tbody></tbody>
    </table>
  </div>

  <footer>Generated by score.py from gate-vectors.yaml — framework: 07-feasibility-gating.md,
  profiles: 08-use-case-gate-profiles.md. Dispositions are weakest-link: KILL = a required
  capability is legally/contractually blocked; DEFER = a structural gap needing a prerequisite
  project; CONDITIONAL = remediable gaps (&le;90 days); GO = all gates met (pilot at A1).</footer>
</div>
<script>
const DATA = __DATA__;
const DISPOS = ["GO","CONDITIONAL","DEFER","KILL"];
const GLYPH = {GO:"✓", CONDITIONAL:"◑", DEFER:"■", KILL:"✕"};
const esc = s => String(s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const badge = d => `<span class="badge b-${d}"><span class="dot"></span>${GLYPH[d]} ${d}</span>`;

document.title = `Feasibility — ${DATA.org.name || "assessment"}`;
document.getElementById("sub").textContent =
  `${DATA.org.name || ""} — assessed by ${DATA.org.assessed_by || "?"} on ${DATA.org.date || "?"}. ` +
  `${DATA.rows.length} use cases scored against ${DATA.n_facets} readiness facets.`;

/* Stat tiles: disposition counts (status color as top accent; glyph+label carry meaning) */
const tiles = document.getElementById("tiles");
const ACCENT = {GO:"var(--good)", CONDITIONAL:"var(--warning)", DEFER:"var(--serious)", KILL:"var(--critical)"};
const INK = {GO:"var(--good-ink)", CONDITIONAL:"var(--warning-ink)", DEFER:"var(--serious-ink)", KILL:"var(--critical-ink)"};
for (const d of DISPOS) {
  tiles.insertAdjacentHTML("beforeend",
    `<div class="tile" style="border-top-color:${ACCENT[d]}">
       <div class="v">${DATA.counts[d] || 0}</div>
       <div class="g" style="color:${INK[d]}">${GLYPH[d]} ${d}</div></div>`);
}
tiles.insertAdjacentHTML("beforeend",
  `<div class="tile"><div class="v">${DATA.downgrade_n}</div>
     <div class="l">can start now at A0/A1<br>(insight-only)</div></div>`);

/* Dimension meters (0-4 segmented, sequential hue) */
const dims = document.getElementById("dims");
for (const [name, val] of DATA.dims) {
  const segs = [1,2,3,4].map(i => `<span class="${i <= val ? "on" : ""}"></span>`).join("");
  dims.insertAdjacentHTML("beforeend",
    `<div class="dim"><div class="name"><span>${esc(name)}</span><b>${val}</b></div>
       <div class="meter" role="img" aria-label="${esc(name)} level ${val} of 4">${segs}</div></div>`);
}

/* Remediation leverage bars (single series, direct-labeled, no legend) */
const bars = document.getElementById("bars");
const maxN = Math.max(1, ...DATA.gaps.map(g => g.n));
for (const g of DATA.gaps) {
  const pct = (g.n / maxN) * 100;
  const sole = g.sole ? ` (${g.sole} solely)` : "";
  bars.insertAdjacentHTML("beforeend",
    `<div class="row" title="${esc(g.item)} blocks ${g.n} use case(s)${sole}">
       <div class="lbl"><code>${esc(g.item)}</code></div>
       <div class="track"><div class="bar" style="width:${pct}%"></div>
         <div class="val" style="left:calc(${pct}% + 6px)">${g.n}${sole}</div></div>
     </div>`);
}
bars.insertAdjacentHTML("beforeend",
  `<div class="axis-note">Use cases held back by each unmet gate (top ${DATA.gaps.length}).
   Fixing the top items unlocks the most portfolio value.</div>`);

/* Filters + table */
const state = { q: "", domain: "", dispo: new Set(DISPOS) };
const chips = document.getElementById("chips");
for (const d of DISPOS) {
  chips.insertAdjacentHTML("beforeend",
    `<button class="chip" data-d="${d}" aria-pressed="true">${GLYPH[d]} ${d} (${DATA.counts[d] || 0})</button>`);
}
chips.addEventListener("click", e => {
  const b = e.target.closest(".chip"); if (!b) return;
  const d = b.dataset.d;
  state.dispo.has(d) && state.dispo.size > 1 ? state.dispo.delete(d) : state.dispo.add(d);
  b.setAttribute("aria-pressed", state.dispo.has(d));
  render();
});
const domSel = document.getElementById("domain");
domSel.innerHTML = `<option value="">All domains</option>` +
  [...new Set(DATA.rows.map(r => r.domain))].map(d => `<option>${esc(d)}</option>`).join("");
domSel.addEventListener("change", () => { state.domain = domSel.value; render(); });
document.getElementById("q").addEventListener("input", e => { state.q = e.target.value.toLowerCase(); render(); });

function gapChip(g) {
  const cls = g.includes("[BLOCKED]") ? "gap blk" : g.includes("(absent)") ? "gap hard" : "gap";
  return `<span class="${cls}">${esc(g)}</span>`;
}
function render() {
  const tb = document.querySelector("#tbl tbody");
  const rows = DATA.rows.filter(r =>
    state.dispo.has(r.disposition) &&
    (!state.domain || r.domain === state.domain) &&
    (!state.q || (r.id + " " + r.name + " " + r.gaps.join(" ") + " " + r.note).toLowerCase().includes(state.q)));
  tb.innerHTML = rows.map(r => `<tr>
      <td class="ucid">${r.id}</td><td>${esc(r.name)}</td><td>${esc(r.domain)}</td>
      <td>${badge(r.disposition)}</td>
      <td>${r.gaps.length ? r.gaps.map(gapChip).join("") : "&mdash;"}</td>
      <td>${r.downgrade ? '<span class="dg">✓ yes</span>' : ""}</td>
      <td class="note">${esc(r.note)}</td></tr>`).join("");
  document.getElementById("shown").textContent = `${rows.length} of ${DATA.rows.length} shown`;
}
render();
</script>
</body></html>
"""


def build_html(assessment, catalog, use_cases):
    res = analyze(assessment, catalog, use_cases)
    gaps = [{"item": item, "n": n, "sole": res["sole_gap_counter"].get(item, 0)}
            for item, n in res["gap_counter"].most_common(15)]
    data = {
        "org": res["org"],
        "dims": [[d, res["dims"].get(d, 0)] for d in DIM_ORDER],
        "counts": dict(res["counts"]),
        "rows": res["rows"],
        "gaps": gaps,
        "downgrade_n": sum(1 for r in res["rows"] if r["downgrade"]),
        "n_facets": len(catalog),
    }
    title = f"Feasibility — {res['org'].get('name', 'assessment')}"
    return (HTML_TEMPLATE
            .replace("__TITLE__", title.replace("<", "&lt;"))
            .replace("__DATA__", json.dumps(data)))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("assessment", nargs="?", help="filled-in assessment YAML")
    ap.add_argument("--vectors", default=str(Path(__file__).parent / "gate-vectors.yaml"))
    ap.add_argument("--init", metavar="PATH", help="write a blank assessment template and exit")
    ap.add_argument("-o", "--output", help="write markdown report to file (default stdout)")
    ap.add_argument("--csv", help="also write per-UC results as CSV")
    ap.add_argument("--html", help="also write a self-contained interactive HTML report")
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

    if args.html:
        Path(args.html).write_text(build_html(assessment, catalog, use_cases))
        print(f"HTML report written to {args.html}")

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
