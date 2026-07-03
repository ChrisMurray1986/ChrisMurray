#!/usr/bin/env python3
"""Dynamic value model for the AI/automation use case catalog.

Estimates every use case's annual value from shared, finite value pools sized by
the organization's financial profile (09-value-model.md), and — when given the
feasibility assessment — gates the ramp by disposition and prices the value
locked behind each blocking gate.

Anti-double-counting: use cases draw *shares* of shared pools; total extraction
per pool is capped (default 85%) and over-claimed pools scale all draws down
proportionally. One-time cash acceleration (AR-days release) is reported
separately from recurring value. Risk/compliance value (VS-8) is reported in
its own column, never blended into cash totals.

Usage:
  value.py my-profile.yaml
  value.py my-profile.yaml --assessment my-org.yaml
  value.py my-profile.yaml --assessment my-org.yaml -o value.md --csv value.csv --html value.html
"""

import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required: pip install pyyaml")

from score import DOMAIN_NAMES, analyze, load_vectors

STREAMS = {
    "VS-1": "Revenue protected", "VS-2": "Revenue recovered", "VS-3": "Revenue captured",
    "VS-4": "Patient cash yield", "VS-5": "Cash acceleration", "VS-6": "Labor productivity",
    "VS-7": "External cost reduction", "VS-8": "Risk & compliance (segregated)",
}


def money(x):
    if abs(x) >= 1e9:
        return f"${x/1e9:,.2f}B"
    if abs(x) >= 1e6:
        return f"${x/1e6:,.1f}M"
    return f"${x/1e3:,.0f}k"


def size_pools(profile, pool_defs):
    """Compute each pool's annual $ (and per-day values for ar_days)."""
    fin, r, c = profile["financials"], profile["rates"], profile["costs"]
    npr = fin["npr"]
    labor_total = npr * c["cost_to_collect_pct"] * c["labor_share_of_ctc"]
    shares = profile["labor_function_shares"]
    if abs(sum(shares.values()) - 1.0) > 0.01:
        sys.exit(f"labor_function_shares must sum to 1.0 (got {sum(shares.values()):.2f})")

    amounts = {
        "denial_prevention": npr * r["denial_writeoff_pct"] * r["denial_preventable_share"],
        "denial_recovery": npr * r["denial_writeoff_pct"] * (1 - r["denial_preventable_share"])
                           * r["denial_recovery_headroom"],
        "underpayment": npr * r["underpayment_pct"] * r["underpayment_detectable"],
        "charge_capture": npr * r["charge_leakage_pct"],
        "doc_yield": npr * r["doc_yield_pct"],
        "coverage_conversion": npr * r["coverage_convertible_pct"],
        "contract_yield": npr * r["contract_yield_pct"],
        "pos_yield": npr * r["pos_upside_pct"],
        "bad_debt_reduction": npr * r["bad_debt_pct"] * r["bad_debt_addressable"],
        "cost_external": npr * c["external_spend_pct"],
        "audit_risk": npr * r["audit_exposure_pct"] * r["audit_mitigable"],
    }
    for fn, sh in shares.items():
        amounts[f"labor_{fn}"] = labor_total * sh

    unknown = set(pool_defs) - set(amounts) - {"ar_days"}
    if unknown:
        sys.exit(f"pools in value-drivers.yaml without sizing logic: {sorted(unknown)}")

    day_recurring = npr / 365 * fin["wacc"]   # carrying cost per AR-day-year
    day_onetime = npr / 365                    # one-time cash release per AR day
    return amounts, day_recurring, day_onetime


def compute(profile, drivers, dispo_by_uc=None, downgrade_by_uc=None):
    model = profile["model"]
    low_m, high_m = model["low_mult"], model["high_mult"]
    cap = model["pool_max_extraction"]
    max_days = model["max_reducible_days"]
    ramp = model["ramp"]
    dg_floor = model["downgrade_y1_floor"]

    pool_defs = drivers["pools"]
    amounts, day_rec, day_one = size_pools(profile, pool_defs)

    # First pass: raw draws
    pool_claims = defaultdict(float)   # pool -> total base share claimed (ar_days in days)
    ucs = {}
    for uc_id, spec in drivers["use_cases"].items():
        rows = []
        for d in spec["draws"]:
            pool = d["pool"]
            if pool == "ar_days":
                units = d["days"]
                pool_claims[pool] += units
                rows.append({"pool": pool, "units": units})
            else:
                share = d["share"]
                pool_claims[pool] += share
                rows.append({"pool": pool, "share": share,
                             "low": d.get("low"), "high": d.get("high")})
        ucs[uc_id] = rows

    # Scaling factors so no pool exceeds its extraction cap
    scale = {}
    for pool, claimed in pool_claims.items():
        limit = max_days * cap if pool == "ar_days" else cap
        scale[pool] = min(1.0, limit / claimed) if claimed > 0 else 1.0

    results = []
    stream_totals = defaultdict(float)          # capped recurring base $ by stream (excl VS-8)
    onetime_total = 0.0
    for uc_id, rows in ucs.items():
        base = risk = one = 0.0
        raw_base = 0.0
        streams = set()
        for r in rows:
            pool = r["pool"]
            stream = pool_defs[pool]["stream"]
            streams.add(stream)
            if pool == "ar_days":
                units = r["units"] * scale[pool]
                v = units * day_rec
                base += v
                one += r["units"] * scale[pool] * day_one
                raw_base += r["units"] * day_rec
                stream_totals[stream] += v
            else:
                v = amounts[pool] * r["share"] * scale[pool]
                raw_base += amounts[pool] * r["share"]
                if stream == "VS-8":
                    risk += v
                else:
                    base += v
                    stream_totals[stream] += v
        dispo = (dispo_by_uc or {}).get(uc_id, "UNASSESSED")
        y1f, y2f = ramp.get(dispo, ramp["UNASSESSED"])
        if dispo == "DEFER" and (downgrade_by_uc or {}).get(uc_id):
            y1f = max(y1f, dg_floor)
        steady = 0.0 if dispo == "KILL" else base
        results.append({
            "id": uc_id, "domain": DOMAIN_NAMES.get(uc_id.split("-")[1], "?"),
            "streams": sorted(streams),
            "low": steady * low_m, "base": steady, "high": steady * high_m,
            "raw_base": raw_base, "risk": 0.0 if dispo == "KILL" else risk,
            "onetime": 0.0 if dispo == "KILL" else one,
            "dispo": dispo, "y1": steady * y1f, "y2": steady * y2f,
        })
        onetime_total += results[-1]["onetime"]

    results.sort(key=lambda r: -r["base"])
    # report claimed vs cap in natural units
    util_rows = []
    for pool in pool_defs:
        claimed = pool_claims.get(pool, 0.0)
        if pool == "ar_days":
            util_rows.append({"pool": pool, "claimed": f"{claimed:.1f} days",
                              "cap": f"{max_days * cap:.1f} days", "scaled": scale.get(pool, 1.0) < 1.0,
                              "amount": f"{money(day_rec)}/day-yr + {money(day_one)}/day one-time"})
        else:
            util_rows.append({"pool": pool, "claimed": f"{claimed:.0%}",
                              "cap": f"{cap:.0%}", "scaled": scale.get(pool, 1.0) < 1.0,
                              "amount": money(amounts[pool])})
    return {"results": results, "stream_totals": dict(stream_totals),
            "onetime_total": onetime_total, "util": util_rows,
            "amounts": amounts, "scale": scale}


def locked_value(results, assessment_rows):
    """Sum steady-state base value of the UCs each blocking gate holds back."""
    by_id = {r["id"]: r for r in results}
    locked = defaultdict(lambda: {"n": 0, "value": 0.0})
    for row in assessment_rows:
        uc = by_id.get(row["id"])
        if not uc or row["disposition"] == "GO":
            continue
        for gap in row["gaps"]:
            key = gap.replace(" (partial)", "").replace(" (absent)", "").replace(" [BLOCKED]", "")
            locked[key]["n"] += 1
            locked[key]["value"] += uc["base"]
    return sorted(({"item": k, **v} for k, v in locked.items()),
                  key=lambda x: -x["value"])


def build_md(profile, comp, locked, assessed):
    org = profile.get("org", {})
    res = comp["results"]
    total_base = sum(r["base"] for r in res)
    total_low = sum(r["low"] for r in res)
    total_high = sum(r["high"] for r in res)
    total_risk = sum(r["risk"] for r in res)
    total_y1 = sum(r["y1"] for r in res)

    L = [f"# Value model — {org.get('name', '?')}",
         f"\nProfile date {org.get('date', '?')}; NPR {money(profile['financials']['npr'])}. "
         f"{len(res)} use cases valued. All figures annual steady-state unless noted; "
         f"pool-capped (extraction limit applied); risk value (VS-8) segregated.\n",
         "## Portfolio totals\n",
         "| Measure | Value |", "|---|---|",
         f"| Recurring value, base case (capped) | **{money(total_base)}** |",
         f"| Recurring range (low–high) | {money(total_low)} – {money(total_high)} |",
         f"| One-time cash release (AR days) | {money(comp['onetime_total'])} |",
         f"| Risk & compliance EV (VS-8, segregated) | {money(total_risk)} |"]
    if assessed:
        L.append(f"| Year-1 value, disposition-adjusted | {money(total_y1)} |")
    L += ["\n## By value stream (recurring, capped, base case)\n",
          "| Stream | Annual value |", "|---|---|"]
    for vs, name in STREAMS.items():
        if vs == "VS-8":
            continue
        L.append(f"| {vs} {name} | {money(comp['stream_totals'].get(vs, 0.0))} |")
    L.append(f"| VS-8 {STREAMS['VS-8']} | {money(total_risk)} |")

    if locked:
        L += ["\n## Value locked by gate (steady-state $ held back per blocking item)\n",
              "Overlapping attribution — a use case with three gaps appears under all three; "
              "this prices gates, it does not sum to the portfolio.\n",
              "| Blocking item | UCs | Locked value |", "|---|---|---|"]
        for row in locked[:15]:
            L.append(f"| {row['item']} | {row['n']} | {money(row['value'])} |")

    L += ["\n## Pool utilization\n",
          "| Pool | Sized at | Claimed | Cap | Scaled down |", "|---|---|---|---|---|"]
    for u in comp["util"]:
        L.append(f"| {u['pool']} | {u['amount']} | {u['claimed']} | {u['cap']} | "
                 f"{'yes' if u['scaled'] else ''} |")

    L += ["\n## Per-use-case value (sorted by base case)\n",
          "| UC | Domain | Streams | Low | Base | High | One-time | Risk EV |"
          + (" Dispo | Year-1 |" if assessed else ""),
          "|---|---|---|---|---|---|---|---|" + ("---|---|" if assessed else "")]
    for r in res:
        row = (f"| {r['id']} | {r['domain']} | {' '.join(r['streams'])} | {money(r['low'])} | "
               f"**{money(r['base'])}** | {money(r['high'])} | "
               f"{money(r['onetime']) if r['onetime'] else '—'} | "
               f"{money(r['risk']) if r['risk'] else '—'} |")
        if assessed:
            row += f" {r['dispo']} | {money(r['y1'])} |"
        L.append(row)
    L.append("\nMeasurement designs per stream: 09-value-model.md §4. Recalibrate draw shares "
             "quarterly against realized value (true-up rule).")
    return "\n".join(L) + "\n"


HTML_TEMPLATE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
  :root {
    --page:#f9f9f7; --surface:#fcfcfb; --ink:#0b0b0b; --ink-2:#52514e; --muted:#898781;
    --grid:#e1e0d9; --baseline:#c3c2b7; --ring:rgba(11,11,11,0.10);
    --seq:#2a78d6; --warning-ink:#7a5200; --serious-ink:#9c3f1d; --critical-ink:#d03b3b;
    --good-ink:#006300;
  }
  @media (prefers-color-scheme: dark) {
    :root { --page:#0d0d0d; --surface:#1a1a19; --ink:#fff; --ink-2:#c3c2b7;
      --grid:#2c2c2a; --baseline:#383835; --ring:rgba(255,255,255,0.10); --seq:#3987e5;
      --warning-ink:#fab219; --serious-ink:#ec835a; --critical-ink:#d03b3b; --good-ink:#0ca30c; }
  }
  * { box-sizing:border-box; }
  body { margin:0; background:var(--page); color:var(--ink);
         font:14px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif; }
  .wrap { max-width:1100px; margin:0 auto; padding:28px 20px 60px; }
  h1 { font-size:21px; margin:0 0 2px; } h2 { font-size:15px; margin:34px 0 12px; }
  .sub { color:var(--ink-2); margin:0 0 24px; }
  .card { background:var(--surface); border:1px solid var(--ring); border-radius:10px; padding:16px; }
  .tiles { display:grid; grid-template-columns:repeat(auto-fit,minmax(170px,1fr)); gap:10px; }
  .tile { background:var(--surface); border:1px solid var(--ring); border-radius:10px; padding:12px 14px; }
  .tile .v { font-size:24px; font-weight:650; } .tile .l { color:var(--ink-2); font-size:12.5px; }
  .bars .row { display:grid; grid-template-columns:280px 1fr; gap:10px; align-items:center; padding:3px 0; border-radius:6px; }
  .bars .row:hover { background:var(--grid); }
  .bars .lbl { font-size:12.5px; color:var(--ink-2); text-align:right; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
  .bars .lbl code { font-family:inherit; color:var(--ink); }
  .bars .track { position:relative; height:14px; }
  .bars .bar { position:absolute; inset:0 auto 0 0; background:var(--seq); border-radius:0 4px 4px 0; min-width:2px; }
  .bars .val { position:absolute; top:-1px; font-size:12px; color:var(--ink-2); font-variant-numeric:tabular-nums; white-space:nowrap; }
  .axis-note { color:var(--muted); font-size:12px; margin-top:8px; }
  .tblwrap { overflow-x:auto; }
  table { border-collapse:collapse; width:100%; font-size:13px; }
  th { text-align:left; color:var(--muted); font-weight:600; font-size:12px; border-bottom:1px solid var(--baseline); padding:6px 10px; white-space:nowrap; }
  td { border-bottom:1px solid var(--grid); padding:7px 10px; vertical-align:top; font-variant-numeric:tabular-nums; }
  tr:hover td { background:var(--grid); }
  td.ucid { white-space:nowrap; color:var(--ink-2); }
  .d-GO { color:var(--good-ink); font-weight:650; } .d-CONDITIONAL { color:var(--warning-ink); font-weight:650; }
  .d-DEFER { color:var(--serious-ink); font-weight:650; } .d-KILL { color:var(--critical-ink); font-weight:650; }
  .d-UNASSESSED { color:var(--muted); }
  .filters { display:flex; flex-wrap:wrap; gap:8px; margin:0 0 12px; }
  .filters input, .filters select { background:var(--surface); color:var(--ink); border:1px solid var(--ring); border-radius:8px; padding:6px 10px; font:inherit; }
  footer { color:var(--muted); font-size:12px; margin-top:40px; }
</style></head>
<body><div class="wrap">
  <h1>Value model</h1>
  <p class="sub" id="sub"></p>
  <div class="tiles" id="tiles"></div>
  <h2>Value by stream <span class="axis-note">(recurring, pool-capped, base case; VS-8 segregated)</span></h2>
  <div class="card bars" id="streams"></div>
  <h2 id="lockedh" hidden>Value locked by gate <span class="axis-note">(overlapping attribution — prices gates, does not sum)</span></h2>
  <div class="card bars" id="locked" hidden></div>
  <h2>Top use cases by value</h2>
  <div class="card bars" id="topuc"></div>
  <h2>All use cases</h2>
  <div class="filters">
    <input type="search" id="q" placeholder="Search&hellip;" aria-label="Search">
    <select id="domain" aria-label="Filter by domain"></select>
  </div>
  <div class="card tblwrap"><table id="tbl"><thead><tr>
    <th>UC</th><th>Domain</th><th>Streams</th><th>Low</th><th>Base</th><th>High</th>
    <th>One-time</th><th>Risk EV</th><th>Disposition</th><th>Year-1</th>
  </tr></thead><tbody></tbody></table></div>
  <footer>Generated by value.py from value-drivers.yaml — framework: 09-value-model.md.
  Shared-pool draws with extraction capping prevent double counting; one-time AR release and
  risk expected-value are never blended into recurring cash totals. Measurement designs per
  stream: 09-value-model.md §4.</footer>
</div>
<script>
const DATA = __DATA__;
const fmt = x => Math.abs(x) >= 1e9 ? "$" + (x/1e9).toFixed(2) + "B"
  : Math.abs(x) >= 1e6 ? "$" + (x/1e6).toFixed(1) + "M" : "$" + Math.round(x/1e3) + "k";
const esc = s => String(s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
document.getElementById("sub").textContent =
  `${DATA.org.name || ""} — profile ${DATA.org.date || "?"}, NPR ${fmt(DATA.npr)}. ` +
  `${DATA.rows.length} use cases valued${DATA.assessed ? ", disposition-adjusted from the feasibility assessment" : ""}.`;
const tiles = document.getElementById("tiles");
const T = DATA.totals;
const tile = (v, l) => `<div class="tile"><div class="v">${v}</div><div class="l">${l}</div></div>`;
tiles.innerHTML =
  tile(fmt(T.base), "recurring value / yr (base, capped)") +
  tile(fmt(T.low) + " – " + fmt(T.high), "uncertainty range") +
  tile(fmt(T.onetime), "one-time cash release (AR days)") +
  tile(fmt(T.risk), "risk &amp; compliance EV (segregated)") +
  (DATA.assessed ? tile(fmt(T.y1), "year-1, disposition-adjusted") : "");
function bars(el, items, labelKey, valKey, extra) {
  const max = Math.max(1, ...items.map(i => i[valKey]));
  el.innerHTML = items.map(i => {
    const pct = i[valKey] / max * 100;
    return `<div class="row" title="${esc(i[labelKey])}: ${fmt(i[valKey])}">
      <div class="lbl"><code>${esc(i[labelKey])}</code></div>
      <div class="track"><div class="bar" style="width:${pct}%"></div>
      <div class="val" style="left:calc(${pct}% + 6px)">${fmt(i[valKey])}${extra ? extra(i) : ""}</div></div></div>`;
  }).join("");
}
bars(document.getElementById("streams"), DATA.streams, "name", "value");
if (DATA.locked.length) {
  document.getElementById("lockedh").hidden = false;
  const el = document.getElementById("locked"); el.hidden = false;
  bars(el, DATA.locked.slice(0, 15), "item", "value", i => ` (${i.n} UCs)`);
}
bars(document.getElementById("topuc"), DATA.rows.slice(0, 15), "id", "base");
const state = { q: "", domain: "" };
const domSel = document.getElementById("domain");
domSel.innerHTML = `<option value="">All domains</option>` +
  [...new Set(DATA.rows.map(r => r.domain))].map(d => `<option>${esc(d)}</option>`).join("");
domSel.addEventListener("change", () => { state.domain = domSel.value; render(); });
document.getElementById("q").addEventListener("input", e => { state.q = e.target.value.toLowerCase(); render(); });
function render() {
  const rows = DATA.rows.filter(r =>
    (!state.domain || r.domain === state.domain) &&
    (!state.q || (r.id + " " + r.domain + " " + r.streams.join(" ")).toLowerCase().includes(state.q)));
  document.querySelector("#tbl tbody").innerHTML = rows.map(r => `<tr>
    <td class="ucid">${r.id}</td><td>${esc(r.domain)}</td><td>${r.streams.join(" ")}</td>
    <td>${fmt(r.low)}</td><td><b>${fmt(r.base)}</b></td><td>${fmt(r.high)}</td>
    <td>${r.onetime ? fmt(r.onetime) : "—"}</td><td>${r.risk ? fmt(r.risk) : "—"}</td>
    <td class="d-${r.dispo}">${r.dispo}</td><td>${DATA.assessed ? fmt(r.y1) : "—"}</td></tr>`).join("");
}
render();
</script></body></html>
"""


def build_html(profile, comp, locked, assessed):
    org = profile.get("org", {})
    res = comp["results"]
    data = {
        "org": org, "npr": profile["financials"]["npr"], "assessed": assessed,
        "totals": {
            "base": sum(r["base"] for r in res), "low": sum(r["low"] for r in res),
            "high": sum(r["high"] for r in res), "onetime": comp["onetime_total"],
            "risk": sum(r["risk"] for r in res), "y1": sum(r["y1"] for r in res),
        },
        "streams": [{"name": f"{vs} {name}", "value": comp["stream_totals"].get(vs, 0.0)}
                    for vs, name in STREAMS.items() if vs != "VS-8"]
                   + [{"name": f"VS-8 {STREAMS['VS-8']}", "value": sum(r["risk"] for r in res)}],
        "locked": locked or [],
        "rows": res,
    }
    title = f"Value model — {org.get('name', '?')}"
    return (HTML_TEMPLATE.replace("__TITLE__", title.replace("<", "&lt;"))
            .replace("__DATA__", json.dumps(data)))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("profile", help="org financial profile YAML (see org-profile.template.yaml)")
    ap.add_argument("--drivers", default=str(Path(__file__).parent / "value-drivers.yaml"))
    ap.add_argument("--assessment", help="feasibility assessment YAML (from score.py) to "
                                         "disposition-adjust value and price locked gates")
    ap.add_argument("--vectors", default=str(Path(__file__).parent / "gate-vectors.yaml"))
    ap.add_argument("-o", "--output", help="write markdown report (default stdout)")
    ap.add_argument("--csv", help="write per-UC values as CSV")
    ap.add_argument("--html", help="write self-contained interactive HTML report")
    args = ap.parse_args()

    with open(args.profile) as f:
        profile = yaml.safe_load(f)
    with open(args.drivers) as f:
        drivers = yaml.safe_load(f)

    # cross-check: every valued UC exists in the gate vectors and vice versa
    catalog, use_cases = load_vectors(args.vectors)
    missing = set(use_cases) ^ set(drivers["use_cases"])
    if missing:
        sys.exit(f"value-drivers.yaml and gate-vectors.yaml disagree on use cases: {sorted(missing)}")

    dispo_by_uc = downgrade_by_uc = None
    assessment_rows = None
    if args.assessment:
        with open(args.assessment) as f:
            assessment = yaml.safe_load(f)
        res = analyze(assessment, catalog, use_cases)
        assessment_rows = res["rows"]
        dispo_by_uc = {r["id"]: r["disposition"] for r in assessment_rows}
        downgrade_by_uc = {r["id"]: r["downgrade"] for r in assessment_rows}

    comp = compute(profile, drivers, dispo_by_uc, downgrade_by_uc)
    locked = locked_value(comp["results"], assessment_rows) if assessment_rows else None

    report = build_md(profile, comp, locked, assessed=bool(args.assessment))
    if args.output:
        Path(args.output).write_text(report)
        print(f"Report written to {args.output}")
    else:
        print(report)

    if args.csv:
        with open(args.csv, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["uc_id", "domain", "streams", "low", "base", "high",
                        "onetime", "risk_ev", "disposition", "year1"])
            for r in comp["results"]:
                w.writerow([r["id"], r["domain"], " ".join(r["streams"]),
                            round(r["low"]), round(r["base"]), round(r["high"]),
                            round(r["onetime"]), round(r["risk"]), r["dispo"], round(r["y1"])])
        print(f"CSV written to {args.csv}")

    if args.html:
        Path(args.html).write_text(build_html(profile, comp, locked, bool(args.assessment)))
        print(f"HTML report written to {args.html}")


if __name__ == "__main__":
    main()
