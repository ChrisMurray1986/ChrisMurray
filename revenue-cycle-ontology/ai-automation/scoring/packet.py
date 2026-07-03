#!/usr/bin/env python3
"""Quarterly investment-packet generator (11-investment-loop-playbook.md).

Runs the full stack — feasibility (score.py), value (value.py), cost with ROI
join (cost.py) — from one assessment + one org profile, and writes a packet
directory: all three reports (md + html), a combined per-UC CSV, a
machine-readable packet.json, and index.md with headline numbers, quarter-over-
quarter deltas (via --prev), and the council agenda pre-filled.

Usage:
  packet.py my-org.yaml my-profile.yaml --outdir packets/2026-Q3
  packet.py my-org.yaml my-profile.yaml --outdir packets/2026-Q4 --prev packets/2026-Q3
"""

import argparse
import csv
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required: pip install pyyaml")

import cost as cm
import score as sc
import value as vm

HERE = Path(__file__).parent


def money(x):
    return vm.money(x)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("assessment", help="feasibility assessment YAML")
    ap.add_argument("profile", help="org financial profile YAML")
    ap.add_argument("--outdir", required=True, help="packet directory to create")
    ap.add_argument("--prev", help="previous packet directory (for quarter-over-quarter deltas)")
    args = ap.parse_args()

    out = Path(args.outdir)
    out.mkdir(parents=True, exist_ok=True)

    with open(args.assessment) as f:
        assessment = yaml.safe_load(f)
    with open(args.profile) as f:
        profile = yaml.safe_load(f)
    catalog, use_cases = sc.load_vectors(HERE / "gate-vectors.yaml")
    with open(HERE / "value-drivers.yaml") as f:
        vdrivers = yaml.safe_load(f)
    with open(HERE / "cost-drivers.yaml") as f:
        cdrivers = yaml.safe_load(f)

    # 1. Feasibility
    fres = sc.analyze(assessment, catalog, use_cases)
    report, _ = sc.build_report(assessment, catalog, use_cases)
    (out / "feasibility.md").write_text(report)
    (out / "feasibility.html").write_text(sc.build_html(assessment, catalog, use_cases))
    dispo = {r["id"]: r["disposition"] for r in fres["rows"]}
    downgrade = {r["id"]: r["downgrade"] for r in fres["rows"]}

    # 2. Value
    vcomp = vm.compute(profile, vdrivers, dispo, downgrade)
    locked = vm.locked_value(vcomp["results"], fres["rows"])
    (out / "value.md").write_text(vm.build_md(profile, vcomp, locked, assessed=True))
    (out / "value.html").write_text(vm.build_html(profile, vcomp, locked, assessed=True))

    # 3. Cost with ROI join
    ccomp = cm.compute(profile, cdrivers, dispo)
    ccomp = cm.join_value(profile, ccomp, dispo, downgrade)
    (out / "cost.md").write_text(cm.build_md(profile, ccomp, roi=True, assessed=True))
    (out / "cost.html").write_text(cm.build_html(profile, ccomp, roi=True))

    # 4. Combined per-UC CSV (the one row per UC the council actually reads)
    vby = {r["id"]: r for r in vcomp["results"]}
    with open(out / "portfolio.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["uc_id", "domain", "disposition", "a0_a1_start", "gaps",
                    "value_yr_base", "value_y1", "option", "build", "run_yr",
                    "tco_3yr_alloc", "net_yr", "payback_months", "roi_3yr"])
        crow = {r["id"]: r for r in ccomp["rows"]}
        for r in fres["rows"]:
            v, c = vby.get(r["id"]), crow.get(r["id"])
            w.writerow([r["id"], r["domain"], r["disposition"],
                        "yes" if r["downgrade"] else "", "; ".join(r["gaps"]),
                        round(v["base"]) if v else "", round(v["y1"]) if v else "",
                        c["option"] if c else "", round(c["build"]) if c else "",
                        round(c["run_yr"]) if c else "", round(c["tco_alloc"]) if c else "",
                        round(c.get("net_yr", 0)) if c else "",
                        round(c["payback_mo"]) if c and c.get("payback_mo") else "",
                        round(c.get("roi3", 0), 2) if c else ""])

    # 5. Headline numbers -> packet.json
    Y = ccomp["rates"]["tco_years"]
    counts = {d: sum(1 for r in fres["rows"] if r["disposition"] == d)
              for d in ("GO", "CONDITIONAL", "DEFER", "KILL")}
    headline = {
        "org": profile.get("org", {}).get("name"),
        "assessment_date": (assessment.get("org") or {}).get("date"),
        "dispositions": counts,
        "a0_a1_available": sum(1 for r in fres["rows"] if r["downgrade"]),
        "value_base_yr": round(sum(r["base"] for r in vcomp["results"])),
        "value_y1": round(sum(r["y1"] for r in vcomp["results"])),
        "value_onetime": round(vcomp["onetime_total"]),
        "risk_ev_yr": round(sum(r["risk"] for r in vcomp["results"])),
        "platform_build": round(ccomp["platform"]["build"]),
        "uc_build": round(sum(r["build"] for r in ccomp["rows"])),
        "run_yr": round(sum(r["run_yr"] for r in ccomp["rows"]) + ccomp["platform"]["run_yr"]),
        "tco_3yr": round(ccomp["platform"]["build"] + Y * ccomp["platform"]["run_yr"]
                         + sum(r["tco"] for r in ccomp["rows"])),
        "net_yr_steady": round(sum(r.get("net_yr", 0) for r in ccomp["rows"])),
        "top_locked": [{"item": x["item"], "n": x["n"], "value": round(x["value"])}
                       for x in locked[:5]],
        "net_negative_ucs": [
            # asterisk = segregated risk EV (VS-8) exceeds the cash shortfall — judge on
            # risk grounds (Play 2 item 6), not as an automatic descope
            r["id"] + ("*" if vby.get(r["id"], {}).get("risk", 0) >= -r.get("net_yr", 0) else "")
            for r in ccomp["rows"] if r.get("net_yr", 0) < 0],
        "slm_verdicts": {x["family"]: ("slm" if x["breakeven"] else "api")
                         for x in ccomp["families"]},
    }
    (out / "packet.json").write_text(json.dumps(headline, indent=2))

    prev = None
    if args.prev:
        prev_path = Path(args.prev) / "packet.json"
        if prev_path.exists():
            prev = json.loads(prev_path.read_text())
        else:
            print(f"warning: {prev_path} not found; skipping deltas", file=sys.stderr)

    def delta(key, fmt=money):
        if not prev or key not in prev:
            return ""
        d = headline[key] - prev[key]
        arrow = "▲" if d > 0 else ("▼" if d < 0 else "=")
        return f" ({arrow} {fmt(abs(d))} vs prior)" if d else " (unchanged)"

    top_net = sorted((r for r in ccomp["rows"] if r.get("net_yr") is not None),
                     key=lambda r: -r.get("net_yr", 0))[:5]
    L = [f"# Investment packet — {headline['org']}",
         f"\nAssessment dated {headline['assessment_date']}; generated from committed inputs "
         f"(never hand-edit this packet — edit the inputs and regenerate).\n",
         "## Headline\n", "| | |", "|---|---|",
         f"| Dispositions | GO {counts['GO']} / COND {counts['CONDITIONAL']} / "
         f"DEFER {counts['DEFER']} / KILL {counts['KILL']}"
         + (f" (prior: GO {prev['dispositions']['GO']} / COND {prev['dispositions']['CONDITIONAL']} / "
            f"DEFER {prev['dispositions']['DEFER']} / KILL {prev['dispositions']['KILL']})" if prev else "") + " |",
         f"| A0/A1 launchable now | {headline['a0_a1_available']} |",
         f"| Steady-state value (base, capped) | {money(headline['value_base_yr'])}/yr"
         + delta("value_base_yr") + " |",
         f"| Year-1 value (disposition-adjusted) | {money(headline['value_y1'])}" + delta("value_y1") + " |",
         f"| One-time cash release | {money(headline['value_onetime'])} |",
         f"| Total run cost | {money(headline['run_yr'])}/yr" + delta("run_yr") + " |",
         f"| 3-yr portfolio TCO | {money(headline['tco_3yr'])}" + delta("tco_3yr") + " |",
         f"| Steady-state net (value − run) | **{money(headline['net_yr_steady'])}/yr**"
         + delta("net_yr_steady") + " |",
         "\n## Top gates by locked value\n", "| Gate | UCs held | Locked $/yr |", "|---|---|---|"]
    for x in headline["top_locked"]:
        L.append(f"| {x['item']} | {x['n']} | {money(x['value'])} |")
    L += ["\n## Top use cases by steady-state net value\n",
          "| UC | Option | Net/yr | Payback | Disposition |", "|---|---|---|---|---|"]
    for r in top_net:
        pb = f"{r['payback_mo']:.0f} mo" if r.get("payback_mo") else "—"
        L.append(f"| {r['id']} | {r['option']} | {money(r.get('net_yr', 0))} | {pb} | {r['dispo']} |")
    if headline["net_negative_ucs"]:
        L.append(f"\n**Net-negative use cases (kill/descope review, Play 7):** "
                 + ", ".join(headline["net_negative_ucs"])
                 + "\n\n\\* risk-EV-justified: segregated VS-8 expected value covers the cash "
                   "shortfall — judge on risk grounds, not as an automatic descope.")
    L.append("\n**SLM verdicts:** " + ", ".join(f"{k}: {v}" for k, v in headline["slm_verdicts"].items()))
    L += ["\n## Council agenda (Play 2)\n",
          "1. True-up — realized vs estimated; benefit-owner signatures; driver recalibrations",
          "2. Readiness velocity — assessment diff vs prior quarter",
          "3. Remediation funding — work the locked-value table above",
          "4. Launch decisions — GO/CONDITIONAL ranked by net value × payback (portfolio.csv)",
          "5. Autonomy promotions — evidence per candidate; update hitl_share on promotion",
          "6. Kills & descopes — net-negative list above; crossed crossovers; KILL re-looks",
          "7. Log decisions — owner, budget, expected value, proving metric",
          "\n## Contents\n",
          "- `feasibility.md` / `.html` — dispositions, gaps, remediation leverage",
          "- `value.md` / `.html` — value streams, pools, locked-value detail",
          "- `cost.md` / `.html` — sourcing decisions, TCO, ROI, SLM break-even",
          "- `portfolio.csv` — one row per use case across all three models",
          "- `packet.json` — headline numbers (machine-readable, for next quarter's deltas)"]
    (out / "index.md").write_text("\n".join(L) + "\n")

    print(f"Packet written to {out}/ (index.md, feasibility|value|cost .md/.html, "
          f"portfolio.csv, packet.json)")


if __name__ == "__main__":
    main()
