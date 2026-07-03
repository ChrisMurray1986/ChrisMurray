#!/usr/bin/env python3
"""Cost model for the AI/automation use case catalog (10-cost-model.md).

Prices every use case across its viable sourcing options (vendor SaaS, rules/RPA,
classical ML, frontier API, fine-tune, self-hosted SLM), picks the recommended
option by 3-year TCO with documented strategic overrides, prices shared platform
assets and payer connectivity explicitly, and — with --roi — joins the value
model for net value, ROI, and payback per use case.

Usage:
  cost.py my-profile.yaml
  cost.py my-profile.yaml --assessment my-org.yaml --roi
  cost.py my-profile.yaml --roi -o cost.md --csv cost.csv --html cost.html
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

BUILD_OPTIONS = {"build_rules", "build_rpa", "build_ml", "api", "finetune", "slm"}


def money(x):
    if abs(x) >= 1e9:
        return f"${x/1e9:,.2f}B"
    if abs(x) >= 1e6:
        return f"${x/1e6:,.2f}M"
    return f"${x/1e3:,.0f}k"


def resolve_volumes(profile, vol_defs, overrides):
    npr = profile["financials"]["npr"]
    vols, pending = {}, dict(vol_defs)
    for _ in range(10):
        for key, d in list(pending.items()):
            if key in overrides:
                vols[key] = float(overrides[key]); pending.pop(key)
            elif "flat" in d:
                vols[key] = float(d["flat"]); pending.pop(key)
            elif "npr_per_unit" in d:
                vols[key] = npr / d["npr_per_unit"]; pending.pop(key)
            elif "of" in d and d["of"] in vols:
                vols[key] = vols[d["of"]] * d["mult"]; pending.pop(key)
        if not pending:
            break
    if pending:
        sys.exit(f"unresolvable volume drivers: {sorted(pending)}")
    return vols


def family_membership(use_cases, workloads):
    members = defaultdict(list)
    for uc_id, spec in use_cases.items():
        wl = workloads[spec["workload"]]
        fam = wl.get("family")
        if fam and "slm" in wl["options"]:
            members[fam].append(uc_id)
    return members


def option_costs(uc_id, spec, R, workloads, vols, families, fam_members):
    """Return {option: {build, fixed_run, var_run, tco}} plus shared per-txn context."""
    wl = workloads[spec["workload"]]
    volume = vols[spec["vol"]] * spec.get("mult", 1.0)
    tokens = spec.get("tokens", wl["tokens"])
    hitl_share = spec.get("hitl_share", wl["hitl_share"])
    hitl_min = spec.get("hitl_min", wl["hitl_min"])
    integ = spec.get("integ", 2)
    tier = spec["tier"]
    Y = R["tco_years"]

    base_build = (R["tier_weeks"][tier] * R["eng_week_rate"]
                  + integ * R["per_integration"] + R["validation"][tier])
    hitl_yr = volume * hitl_share * hitl_min / 60 * R["hitl_hourly"]

    payer_build = payer_fixed = payer_var = 0.0
    p = R["payer"]
    if spec.get("payer") in ("edi", "both"):
        payer_build += p["n_payers"] * p["edi_enrollment"]
        payer_var += volume * p["edi_per_txn"]
    if spec.get("payer") in ("portal", "both"):
        payer_fixed += p["n_payers"] * p["portal_bot_per_payer_yr"]

    out = {}
    for opt in wl["options"]:
        if opt == "vendor" and "vendor_txn" not in spec:
            continue
        build = base_build * R["option_build_mult"][opt] + payer_build
        fixed = payer_fixed + R["maintenance_pct"][opt] * build
        var = hitl_yr + payer_var
        if opt == "vendor":
            var += volume * spec["vendor_txn"]
        elif opt == "api":
            var += volume * tokens / 1e6 * R["token_price_per_m"]["api"]
        elif opt == "finetune":
            build += R["finetune_fixed"]
            fixed += R["finetune_annual_retune"]
            var += volume * tokens / 1e6 * R["token_price_per_m"]["finetune"]
        elif opt == "slm":
            fam = wl["family"]
            n = max(1, len(fam_members[fam]))
            build += families[fam]["adapt_cost"] / n
            fixed += families[fam]["hosting_yr"] / n
            var += volume * tokens / 1e6 * R["token_price_per_m"]["slm"]
        elif opt == "build_ml":
            fixed += R["ml_retrain_pct"] * build
            var += volume * R["ml_per_prediction"]
        tco = build + Y * (fixed + var)
        if opt == "vendor":
            tco += R["vendor_switching_pct"] * volume * spec["vendor_txn"]  # exit priced in
        out[opt] = {"build": build, "fixed_run": fixed, "var_run": var,
                    "run_yr": fixed + var, "tco": tco}
    return out, volume


def decide(spec, opts, R):
    ranked = sorted(opts.items(), key=lambda kv: kv[1]["tco"])
    rec, rec_c = ranked[0]
    override = None
    if spec.get("diff") and rec == "vendor" and len(ranked) > 1:
        nb = next(((o, c) for o, c in ranked[1:] if o != "vendor"), None)
        if nb and rec_c["tco"] >= (1 - R["differentiator_threshold"]) * nb[1]["tco"]:
            rec, rec_c = nb
            override = "differentiator: built in-house despite vendor price within threshold"
    runner = next(((o, c) for o, c in ranked if o != rec), None)
    crossover = None
    if runner:
        (b1, f1, v1) = (rec_c["build"], rec_c["fixed_run"], rec_c["var_run"])
        (b2, f2, v2) = (runner[1]["build"], runner[1]["fixed_run"], runner[1]["var_run"])
        Y = R["tco_years"]
        if abs(v2 - v1) > 1e-9:
            f = (b1 + Y * f1 - b2 - Y * f2) / (Y * (v2 - v1))
            if 0.1 < f < 10 and abs(f - 1) > 0.05:
                crossover = f
    return rec, rec_c, (runner[0] if runner else None), override, crossover


def allocate_platform(assets, use_cases, active):
    dep = {}
    for name, a in assets.items():
        tags = set(a["tags"])
        dep[name] = [uc for uc in active
                     if use_cases[uc]["workload"] in tags
                     or tags & set(use_cases[uc].get("flags", []))]
    alloc_b, alloc_r = defaultdict(float), defaultdict(float)
    for name, ucs in dep.items():
        if not ucs:
            continue
        for uc in ucs:
            alloc_b[uc] += assets[name]["build"] / len(ucs)
            alloc_r[uc] += assets[name]["run_yr"] / len(ucs)
    return dep, alloc_b, alloc_r


def compute(profile, drivers, dispo_by_uc=None):
    R = dict(drivers["rates"])
    R.update(profile.get("cost_rates", {}))
    workloads, families = drivers["workloads"], drivers["slm_families"]
    use_cases = drivers["use_cases"]
    vols = resolve_volumes(profile, drivers["volumes"], profile.get("volumes", {}))
    fam_members = family_membership(use_cases, workloads)

    active = [uc for uc in use_cases
              if (dispo_by_uc or {}).get(uc, "UNASSESSED") != "KILL"]
    dep, alloc_b, alloc_r = allocate_platform(drivers["platform_assets"], use_cases, active)

    rows, cat = [], defaultdict(float)
    for uc_id, spec in use_cases.items():
        if uc_id not in active:
            continue
        opts, volume = option_costs(uc_id, spec, R, workloads, vols, families, fam_members)
        rec, c, runner, override, crossover = decide(spec, opts, R)
        wl = workloads[spec["workload"]]
        tokens = spec.get("tokens", wl["tokens"])
        hitl_yr = volume * spec.get("hitl_share", wl["hitl_share"]) \
            * spec.get("hitl_min", wl["hitl_min"]) / 60 * R["hitl_hourly"]
        infer = (volume * tokens / 1e6 * R["token_price_per_m"].get(
                 rec if rec in ("api", "finetune", "slm") else "api", 0)
                 if rec in ("api", "finetune", "slm") else
                 volume * R["ml_per_prediction"] if rec == "build_ml" else 0.0)
        vendor_fees = volume * spec.get("vendor_txn", 0) if rec == "vendor" else 0.0
        maint = c["run_yr"] - hitl_yr - infer - vendor_fees
        cat["HITL review labor"] += hitl_yr
        cat["Inference/compute"] += infer
        cat["Vendor fees"] += vendor_fees
        cat["Maintenance, payer & hosting"] += max(0.0, maint)
        rows.append({
            "id": uc_id, "domain": DOMAIN_NAMES.get(uc_id.split("-")[1], "?"),
            "workload": spec["workload"], "tier": spec["tier"], "volume": volume,
            "option": rec, "runner": runner, "override": override, "crossover": crossover,
            "build": c["build"], "run_yr": c["run_yr"], "tco": c["tco"],
            "build_lo": c["build"] * R["build_cone"][0], "build_hi": c["build"] * R["build_cone"][1],
            "run_lo": c["run_yr"] * R["run_cone"][0], "run_hi": c["run_yr"] * R["run_cone"][1],
            "plat_build": alloc_b.get(uc_id, 0.0), "plat_run": alloc_r.get(uc_id, 0.0),
            "tco_alloc": c["tco"] + alloc_b.get(uc_id, 0.0) + R["tco_years"] * alloc_r.get(uc_id, 0.0),
            "options": {o: v["tco"] for o, v in opts.items()},
            "dispo": (dispo_by_uc or {}).get(uc_id, "UNASSESSED"),
        })
    rows.sort(key=lambda r: -r["tco_alloc"])

    plat_build = sum(a["build"] for n, a in drivers["platform_assets"].items() if dep[n])
    plat_run = sum(a["run_yr"] for n, a in drivers["platform_assets"].items() if dep[n])
    # SLM family break-even (vs api rates), counted across members that chose slm-eligible workloads
    fam_rows = []
    for fam, members in fam_members.items():
        tok_vol = 0.0
        for uc in members:
            spec = use_cases[uc]
            wl = workloads[spec["workload"]]
            tok_vol += vols[spec["vol"]] * spec.get("mult", 1.0) * spec.get("tokens", wl["tokens"])
        savings = tok_vol / 1e6 * (R["token_price_per_m"]["api"] - R["token_price_per_m"]["slm"])
        annual_cost = families[fam]["hosting_yr"] + families[fam]["adapt_cost"] / R["tco_years"]
        fam_rows.append({"family": fam, "members": len(members), "mtokens": tok_vol / 1e6,
                         "savings_yr": savings, "cost_yr": annual_cost,
                         "breakeven": savings >= annual_cost})
    return {"rows": rows, "categories": dict(cat), "vols": vols,
            "platform": {"build": plat_build, "run_yr": plat_run,
                         "assets": {n: {**a, "n_dep": len(dep[n])}
                                    for n, a in drivers["platform_assets"].items()}},
            "families": fam_rows, "rates": R}


def join_value(profile, comp, dispo_by_uc, downgrade_by_uc):
    import value as vm
    with open(Path(__file__).parent / "value-drivers.yaml") as f:
        vdrivers = yaml.safe_load(f)
    vcomp = vm.compute(profile, vdrivers, dispo_by_uc, downgrade_by_uc)
    vby = {r["id"]: r for r in vcomp["results"]}
    for r in comp["rows"]:
        v = vby.get(r["id"])
        if not v:
            continue
        run_total = r["run_yr"] + r["plat_run"]
        build_total = r["build"] + r["plat_build"]
        r["value_yr"] = v["base"]
        r["net_yr"] = v["base"] - run_total
        val3 = (v["y1"] + v["y2"] + v["base"]) if dispo_by_uc else v["base"] * 2.1
        r["roi3"] = (val3 - r["tco_alloc"]) / r["tco_alloc"] if r["tco_alloc"] > 0 else 0.0
        r["payback_mo"] = (build_total / r["net_yr"] * 12) if r["net_yr"] > 0 else None
    return comp


def build_md(profile, comp, roi, assessed):
    org = profile.get("org", {})
    rows = comp["rows"]
    Y = comp["rates"]["tco_years"]
    build_uc = sum(r["build"] for r in rows)
    run_uc = sum(r["run_yr"] for r in rows)
    plat = comp["platform"]
    tco_total = plat["build"] + Y * plat["run_yr"] + sum(r["tco"] for r in rows)

    L = [f"# Cost model — {org.get('name', '?')}",
         f"\nNPR {money(profile['financials']['npr'])}; {len(rows)} active use cases priced over "
         f"{Y} years. Build ranges ±(0.8/1.5), run ±20% — see 10-cost-model.md.\n",
         "## Portfolio totals\n", "| Measure | Value |", "|---|---|",
         f"| Platform build (L1, one-time) | **{money(plat['build'])}** |",
         f"| Platform run (L1, annual) | {money(plat['run_yr'])} |",
         f"| Use-case build (L2, one-time, recommended options) | **{money(build_uc)}** "
         f"({money(sum(r['build_lo'] for r in rows))} – {money(sum(r['build_hi'] for r in rows))}) |",
         f"| Use-case run (L3, annual) | **{money(run_uc)}** "
         f"({money(sum(r['run_lo'] for r in rows))} – {money(sum(r['run_hi'] for r in rows))}) |",
         f"| {Y}-year portfolio TCO | **{money(tco_total)}** |"]
    if roi:
        net = sum(r.get("net_yr", 0) for r in rows)
        L.append(f"| Steady-state net value (value − run), annual | **{money(net)}** |")

    L += ["\n## Annual run cost by category\n", "| Category | Annual $ |", "|---|---|"]
    for k, v in sorted(comp["categories"].items(), key=lambda kv: -kv[1]):
        L.append(f"| {k} | {money(v)} |")
    L.append(f"| Platform hosting/run (L1) | {money(plat['run_yr'])} |")

    L += ["\n## Platform assets (L1)\n",
          "| Asset | Build | Run/yr | Dependent UCs |", "|---|---|---|---|"]
    for n, a in comp["platform"]["assets"].items():
        if a["n_dep"]:
            L.append(f"| {n} | {money(a['build'])} | {money(a['run_yr'])} | {a['n_dep']} |")

    L += ["\n## SLM family break-even (vs frontier API rates)\n",
          "| Family | Member UCs | Annual Mtokens | API-vs-SLM savings/yr | Family cost/yr | Verdict |",
          "|---|---|---|---|---|---|"]
    for f in comp["families"]:
        verdict = "**SLM pays**" if f["breakeven"] else "stay on API"
        L.append(f"| {f['family']} | {f['members']} | {f['mtokens']:,.0f} | "
                 f"{money(f['savings_yr'])} | {money(f['cost_yr'])} | {verdict} |")

    hdr = "| UC | Option | Build | Run/yr | TCO (alloc) |"
    sep = "|---|---|---|---|---|"
    if roi:
        hdr += " Value/yr | Net/yr | Payback | ROI-3yr |"
        sep += "---|---|---|---|"
    hdr += " Notes |"
    sep += "---|"
    L += ["\n## Per-use-case decisions (sorted by allocated TCO)\n", hdr, sep]
    for r in rows:
        notes = []
        if r["override"]:
            notes.append(r["override"])
        if r["runner"]:
            notes.append(f"beat {r['runner']}")
        if r["crossover"]:
            notes.append(f"revisit at {r['crossover']:.1f}x volume")
        row = (f"| {r['id']} | {r['option']} | {money(r['build'])} | {money(r['run_yr'])} | "
               f"{money(r['tco_alloc'])} |")
        if roi:
            pb = f"{r['payback_mo']:.0f} mo" if r.get("payback_mo") else "—"
            row += (f" {money(r.get('value_yr', 0))} | {money(r.get('net_yr', 0))} | {pb} | "
                    f"{r.get('roi3', 0):+.0%} |")
        row += f" {'; '.join(notes)} |"
        L.append(row)
    L.append("\nDecision rules, math, and governance: 10-cost-model.md. Coefficients "
             "recalibrate quarterly against actuals (true-up rule).")
    return "\n".join(L) + "\n"


HTML_TEMPLATE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
  :root { --page:#f9f9f7; --surface:#fcfcfb; --ink:#0b0b0b; --ink-2:#52514e; --muted:#898781;
    --grid:#e1e0d9; --baseline:#c3c2b7; --ring:rgba(11,11,11,0.10); --seq:#2a78d6;
    --good-ink:#006300; --critical-ink:#d03b3b; }
  @media (prefers-color-scheme: dark) {
    :root { --page:#0d0d0d; --surface:#1a1a19; --ink:#fff; --ink-2:#c3c2b7; --grid:#2c2c2a;
      --baseline:#383835; --ring:rgba(255,255,255,0.10); --seq:#3987e5;
      --good-ink:#0ca30c; --critical-ink:#d03b3b; } }
  * { box-sizing:border-box; }
  body { margin:0; background:var(--page); color:var(--ink);
         font:14px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif; }
  .wrap { max-width:1100px; margin:0 auto; padding:28px 20px 60px; }
  h1 { font-size:21px; margin:0 0 2px; } h2 { font-size:15px; margin:34px 0 12px; }
  .sub { color:var(--ink-2); margin:0 0 24px; }
  .card { background:var(--surface); border:1px solid var(--ring); border-radius:10px; padding:16px; }
  .tiles { display:grid; grid-template-columns:repeat(auto-fit,minmax(165px,1fr)); gap:10px; }
  .tile { background:var(--surface); border:1px solid var(--ring); border-radius:10px; padding:12px 14px; }
  .tile .v { font-size:22px; font-weight:650; } .tile .l { color:var(--ink-2); font-size:12.5px; }
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
  .opt { font-weight:650; } .pos { color:var(--good-ink); font-weight:650; } .neg { color:var(--critical-ink); font-weight:650; }
  .filters { display:flex; flex-wrap:wrap; gap:8px; margin:0 0 12px; }
  .filters input, .filters select { background:var(--surface); color:var(--ink); border:1px solid var(--ring); border-radius:8px; padding:6px 10px; font:inherit; }
  .note { color:var(--muted); font-size:12px; }
  footer { color:var(--muted); font-size:12px; margin-top:40px; }
</style></head>
<body><div class="wrap">
  <h1>Cost model</h1>
  <p class="sub" id="sub"></p>
  <div class="tiles" id="tiles"></div>
  <h2>Annual run cost by category</h2>
  <div class="card bars" id="cats"></div>
  <h2>SLM family break-even <span class="axis-note">(annual API-vs-SLM savings vs family cost)</span></h2>
  <div class="card tblwrap"><table id="fam"><thead><tr>
    <th>Family</th><th>Member UCs</th><th>Annual Mtokens</th><th>Savings/yr on SLM</th><th>Family cost/yr</th><th>Verdict</th>
  </tr></thead><tbody></tbody></table></div>
  <h2>Top use cases by allocated 3-yr TCO</h2>
  <div class="card bars" id="topuc"></div>
  <h2>All use cases</h2>
  <div class="filters">
    <input type="search" id="q" placeholder="Search&hellip;" aria-label="Search">
    <select id="domain" aria-label="Filter by domain"></select>
    <select id="opt" aria-label="Filter by option"></select>
  </div>
  <div class="card tblwrap"><table id="tbl"><thead><tr id="thead"></tr></thead><tbody></tbody></table></div>
  <footer>Generated by cost.py from cost-drivers.yaml — framework: 10-cost-model.md.
  TCO = build + 3yr run + platform allocation; vendor options carry a priced exit; SLM families
  are shared assets. Build ±(0.8/1.5), run ±20%. Coefficients true-up quarterly.</footer>
</div>
<script>
const DATA = __DATA__;
const fmt = x => Math.abs(x) >= 1e9 ? "$" + (x/1e9).toFixed(2) + "B"
  : Math.abs(x) >= 1e6 ? "$" + (x/1e6).toFixed(2) + "M" : "$" + Math.round(x/1e3) + "k";
const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
document.getElementById("sub").textContent =
  `${DATA.org.name || ""} — NPR ${fmt(DATA.npr)}. ${DATA.rows.length} active use cases priced over ${DATA.years} years` +
  (DATA.roi ? "; ROI joined from the value model." : ".");
const T = DATA.totals;
const tile = (v, l) => `<div class="tile"><div class="v">${v}</div><div class="l">${l}</div></div>`;
document.getElementById("tiles").innerHTML =
  tile(fmt(T.plat_build), "platform build (one-time)") +
  tile(fmt(T.build), "use-case build (one-time)") +
  tile(fmt(T.run + T.plat_run), "total run / yr") +
  tile(fmt(T.tco), DATA.years + "-yr portfolio TCO") +
  (DATA.roi ? tile(fmt(T.net), "steady-state net value / yr") : "");
function bars(el, items, labelKey, valKey) {
  const max = Math.max(1, ...items.map(i => i[valKey]));
  el.innerHTML = items.map(i => {
    const pct = i[valKey] / max * 100;
    return `<div class="row" title="${esc(i[labelKey])}: ${fmt(i[valKey])}">
      <div class="lbl"><code>${esc(i[labelKey])}</code></div>
      <div class="track"><div class="bar" style="width:${pct}%"></div>
      <div class="val" style="left:calc(${pct}% + 6px)">${fmt(i[valKey])}</div></div></div>`;
  }).join("");
}
bars(document.getElementById("cats"), DATA.categories, "name", "value");
document.querySelector("#fam tbody").innerHTML = DATA.families.map(f => `<tr>
  <td>${esc(f.family)}</td><td>${f.members}</td><td>${Math.round(f.mtokens).toLocaleString()}</td>
  <td>${fmt(f.savings_yr)}</td><td>${fmt(f.cost_yr)}</td>
  <td class="${f.breakeven ? "pos" : ""}">${f.breakeven ? "SLM pays" : "stay on API"}</td></tr>`).join("");
bars(document.getElementById("topuc"), DATA.rows.slice(0, 15), "id", "tco_alloc");
const cols = ["UC", "Domain", "Option", "Build", "Run/yr", "TCO (alloc)"]
  .concat(DATA.roi ? ["Value/yr", "Net/yr", "Payback", "ROI-3yr"] : []).concat(["Notes"]);
document.getElementById("thead").innerHTML = cols.map(c => `<th>${c}</th>`).join("");
const state = { q: "", domain: "", opt: "" };
const domSel = document.getElementById("domain"), optSel = document.getElementById("opt");
domSel.innerHTML = `<option value="">All domains</option>` +
  [...new Set(DATA.rows.map(r => r.domain))].map(d => `<option>${esc(d)}</option>`).join("");
optSel.innerHTML = `<option value="">All options</option>` +
  [...new Set(DATA.rows.map(r => r.option))].map(d => `<option>${esc(d)}</option>`).join("");
domSel.addEventListener("change", () => { state.domain = domSel.value; render(); });
optSel.addEventListener("change", () => { state.opt = optSel.value; render(); });
document.getElementById("q").addEventListener("input", e => { state.q = e.target.value.toLowerCase(); render(); });
function render() {
  const rows = DATA.rows.filter(r =>
    (!state.domain || r.domain === state.domain) && (!state.opt || r.option === state.opt) &&
    (!state.q || (r.id + " " + r.domain + " " + r.option + " " + (r.notes || "")).toLowerCase().includes(state.q)));
  document.querySelector("#tbl tbody").innerHTML = rows.map(r => {
    let cells = `<td class="ucid">${r.id}</td><td>${esc(r.domain)}</td><td class="opt">${esc(r.option)}</td>
      <td>${fmt(r.build)}</td><td>${fmt(r.run_yr)}</td><td>${fmt(r.tco_alloc)}</td>`;
    if (DATA.roi) {
      const pb = r.payback_mo ? Math.round(r.payback_mo) + " mo" : "—";
      const roiCls = (r.roi3 || 0) >= 0 ? "pos" : "neg";
      cells += `<td>${fmt(r.value_yr || 0)}</td><td class="${(r.net_yr||0)>=0?"pos":"neg"}">${fmt(r.net_yr || 0)}</td>
        <td>${pb}</td><td class="${roiCls}">${Math.round((r.roi3 || 0) * 100)}%</td>`;
    }
    cells += `<td class="note">${esc(r.notes || "")}</td>`;
    return `<tr>${cells}</tr>`;
  }).join("");
}
render();
</script></body></html>
"""


def build_html(profile, comp, roi):
    org = profile.get("org", {})
    rows = comp["rows"]
    Y = comp["rates"]["tco_years"]
    plat = comp["platform"]
    for r in rows:
        notes = []
        if r["override"]:
            notes.append(r["override"])
        if r["runner"]:
            notes.append(f"beat {r['runner']}")
        if r["crossover"]:
            notes.append(f"revisit at {r['crossover']:.1f}x volume")
        r["notes"] = "; ".join(notes)
    data = {
        "org": org, "npr": profile["financials"]["npr"], "years": Y, "roi": roi,
        "totals": {
            "plat_build": plat["build"], "plat_run": plat["run_yr"],
            "build": sum(r["build"] for r in rows), "run": sum(r["run_yr"] for r in rows),
            "tco": plat["build"] + Y * plat["run_yr"] + sum(r["tco"] for r in rows),
            "net": sum(r.get("net_yr", 0) for r in rows),
        },
        "categories": [{"name": k, "value": v} for k, v in
                       sorted(comp["categories"].items(), key=lambda kv: -kv[1])]
                      + [{"name": "Platform hosting/run (L1)", "value": plat["run_yr"]}],
        "families": comp["families"],
        "rows": [{k: r.get(k) for k in ("id", "domain", "option", "build", "run_yr",
                                        "tco_alloc", "value_yr", "net_yr", "payback_mo",
                                        "roi3", "notes")} for r in rows],
    }
    title = f"Cost model — {org.get('name', '?')}"
    return (HTML_TEMPLATE.replace("__TITLE__", title.replace("<", "&lt;"))
            .replace("__DATA__", json.dumps(data)))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("profile", help="org financial profile YAML (same file the value model uses)")
    ap.add_argument("--drivers", default=str(Path(__file__).parent / "cost-drivers.yaml"))
    ap.add_argument("--assessment", help="feasibility assessment YAML: KILLed UCs drop out; "
                                         "dispositions phase the plan")
    ap.add_argument("--vectors", default=str(Path(__file__).parent / "gate-vectors.yaml"))
    ap.add_argument("--roi", action="store_true", help="join value.py for net value/ROI/payback")
    ap.add_argument("-o", "--output", help="write markdown report (default stdout)")
    ap.add_argument("--csv", help="write per-UC costs as CSV")
    ap.add_argument("--html", help="write self-contained interactive HTML report")
    args = ap.parse_args()

    with open(args.profile) as f:
        profile = yaml.safe_load(f)
    with open(args.drivers) as f:
        drivers = yaml.safe_load(f)

    catalog, use_cases = load_vectors(args.vectors)
    missing = set(use_cases) ^ set(drivers["use_cases"])
    if missing:
        sys.exit(f"cost-drivers.yaml and gate-vectors.yaml disagree on use cases: {sorted(missing)}")

    dispo_by_uc = downgrade_by_uc = None
    if args.assessment:
        with open(args.assessment) as f:
            assessment = yaml.safe_load(f)
        res = analyze(assessment, catalog, use_cases)
        dispo_by_uc = {r["id"]: r["disposition"] for r in res["rows"]}
        downgrade_by_uc = {r["id"]: r["downgrade"] for r in res["rows"]}

    comp = compute(profile, drivers, dispo_by_uc)
    if args.roi:
        comp = join_value(profile, comp, dispo_by_uc, downgrade_by_uc)

    report = build_md(profile, comp, args.roi, bool(args.assessment))
    if args.output:
        Path(args.output).write_text(report)
        print(f"Report written to {args.output}")
    else:
        print(report)

    if args.csv:
        with open(args.csv, "w", newline="") as f:
            w = csv.writer(f)
            hdr = ["uc_id", "domain", "workload", "tier", "annual_volume", "option", "runner_up",
                   "build", "run_yr", "tco_3yr_allocated", "platform_build_alloc",
                   "platform_run_alloc", "crossover_x_volume", "disposition"]
            if args.roi:
                hdr += ["value_yr", "net_yr", "payback_months", "roi_3yr"]
            w.writerow(hdr)
            for r in comp["rows"]:
                row = [r["id"], r["domain"], r["workload"], r["tier"], round(r["volume"]),
                       r["option"], r["runner"], round(r["build"]), round(r["run_yr"]),
                       round(r["tco_alloc"]), round(r["plat_build"]), round(r["plat_run"]),
                       round(r["crossover"], 2) if r["crossover"] else "", r["dispo"]]
                if args.roi:
                    row += [round(r.get("value_yr", 0)), round(r.get("net_yr", 0)),
                            round(r["payback_mo"]) if r.get("payback_mo") else "",
                            round(r.get("roi3", 0), 2)]
                w.writerow(row)
        print(f"CSV written to {args.csv}")

    if args.html:
        Path(args.html).write_text(build_html(profile, comp, args.roi))
        print(f"HTML report written to {args.html}")


if __name__ == "__main__":
    main()
