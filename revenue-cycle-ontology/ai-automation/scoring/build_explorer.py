#!/usr/bin/env python3
"""Build the use-case explorer (use-case-explorer.html).

Merges three sources per use case and embeds them into explorer-template.html:
  1. Descriptions parsed from the catalog markdown (01..04-use-cases-*.md):
     patterns, autonomy, risk tier, targets, trigger, function, prevents,
     improves, guardrails, and any extra fields.
  2. Driver YAMLs: gate vector + facet dependencies (gate-vectors), value pool
     draws (value-drivers), workload/tier/options/volume bindings (cost-drivers).
  3. Computed $ figures at the reference org profile (example-org-profile.yaml)
     via the value.py and cost.py engines, unassessed (full steady-state view).

Usage: python3 build_explorer.py [-o use-case-explorer.html]
"""

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required: pip install pyyaml")

import cost as cm
import value as vm
from score import DOMAIN_NAMES, load_vectors

HERE = Path(__file__).parent
AI_DIR = HERE.parent
CATALOG_FILES = ["01-use-cases-front-end.md", "02-use-cases-mid-cycle.md",
                 "03-use-cases-back-end.md", "04-use-cases-cross-cutting.md"]
PHASE_BY_DOMAIN = {**{f"{i:02d}": "front" for i in [1]},
                   **{f"{i:02d}": "mid" for i in range(2, 6)},
                   **{f"{i:02d}": "back" for i in range(6, 11)},
                   **{f"{i:02d}": "cross" for i in range(11, 15)}}
RISK_NAMES = {"R1": "compliance-critical", "R2": "financially material",
              "R3": "patient-facing", "R4": "internal/operational"}


def parse_catalog():
    """Parse the four markdown catalog files into {uc_id: fields}."""
    out = {}
    for fname in CATALOG_FILES:
        text = (AI_DIR / fname).read_text()
        for block in re.split(r"^### ", text, flags=re.M)[1:]:
            lines = block.splitlines()
            m = re.match(r"(UC-\d\d-\d\d)\s+(.*)", lines[0])
            if not m:
                continue
            uc_id, name = m.group(1), m.group(2).strip()
            # join bullet continuation lines
            bullets, cur = [], None
            for ln in lines[1:]:
                if ln.startswith("- "):
                    if cur:
                        bullets.append(cur)
                    cur = ln[2:].strip()
                elif ln.startswith("  ") and cur is not None:
                    cur += " " + ln.strip()
                elif not ln.strip() and cur:
                    bullets.append(cur)
                    cur = None
            if cur:
                bullets.append(cur)
            rec = {"name": name, "patterns": [], "autonomy": "", "risk": "",
                   "fields": {}}
            for b in bullets:
                if b.startswith("PAT-"):
                    parts = [p.strip() for p in b.split("|")]
                    rec["patterns"] = re.findall(r"PAT-[A-Z]+", parts[0])
                    rec["autonomy"] = parts[1] if len(parts) > 1 else ""
                    rm = re.search(r"R\d", parts[2]) if len(parts) > 2 else None
                    rec["risk"] = rm.group(0) if rm else ""
                    continue
                # bullets may hold several "Key: value" segments split by " | "
                segs = re.split(r"\s\|\s(?=[A-Z][\w&-]*(?:-in)?:)", b)
                for seg in segs:
                    km = re.match(r"([A-Z][\w &/-]{1,14}):\s*(.*)", seg)
                    if km:
                        rec["fields"][km.group(1)] = km.group(2).strip()
                    elif "Function" in rec["fields"] and not rec["fields"].get("_done"):
                        rec["fields"]["Function"] += " " + seg
            out[uc_id] = rec
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("-o", "--output", default=str(HERE / "use-case-explorer.html"))
    args = ap.parse_args()

    catalog_md = parse_catalog()
    _, gv_ucs = load_vectors(HERE / "gate-vectors.yaml")
    gv = yaml.safe_load((HERE / "gate-vectors.yaml").read_text())
    vd = yaml.safe_load((HERE / "value-drivers.yaml").read_text())
    cd = yaml.safe_load((HERE / "cost-drivers.yaml").read_text())
    profile = yaml.safe_load((HERE / "example-org-profile.yaml").read_text())

    missing = set(gv_ucs) - set(catalog_md)
    if missing:
        sys.exit(f"catalog markdown missing use cases: {sorted(missing)}")

    # engines at reference profile, unassessed
    vcomp = vm.compute(profile, vd)
    ccomp = cm.compute(profile, cd)
    ccomp = cm.join_value(profile, ccomp, None, None)
    vby = {r["id"]: r for r in vcomp["results"]}
    cby = {r["id"]: r for r in ccomp["rows"]}

    # pool $ for per-draw display (recompute amounts like value.size_pools)
    amounts, day_rec, _ = vm.size_pools(profile, vd["pools"])
    facet_cat = gv["facet_catalog"]
    vols = cm.resolve_volumes(profile, cd["volumes"], {})

    ucs = []
    for uc_id in gv_ucs:
        md = catalog_md[uc_id]
        g = gv["use_cases"][uc_id]
        v, c = vby[uc_id], cby[uc_id]
        spec = cd["use_cases"][uc_id]
        wl = cd["workloads"][spec["workload"]]
        fields = md["fields"]
        draws = []
        for d in vd["use_cases"][uc_id]["draws"]:
            if d["pool"] == "ar_days":
                draws.append({"pool": "ar_days (carrying)", "share": f"{d['days']} days",
                              "usd": d["days"] * day_rec})
            else:
                draws.append({"pool": d["pool"], "share": f"{d['share']:.1%}",
                              "usd": amounts[d["pool"]] * d["share"]})
        platform = [n for n, a in cd["platform_assets"].items()
                    if spec["workload"] in a["tags"]
                    or set(a["tags"]) & set(spec.get("flags", []))]
        deps = [{"id": fid, "prompt": facet_cat[fid]["prompt"],
                 "blockable": bool(facet_cat[fid].get("blockable"))}
                for fid in g.get("facets", [])]
        extra = {k: val for k, val in fields.items()
                 if k not in ("Targets", "Trigger", "Function", "Prevents",
                              "Improves", "Guardrails", "Runs-in")}
        rec = {
            "id": uc_id, "name": md["name"],
            "domain": DOMAIN_NAMES[uc_id.split("-")[1]],
            "phase": PHASE_BY_DOMAIN[uc_id.split("-")[1]],
            "patterns": md["patterns"], "autonomy": md["autonomy"],
            "autonomyShort": (re.search(r"A\d(?:/A\d)?", md["autonomy"]) or ["A?"])[0],
            "risk": md["risk"],
            "targets": fields.get("Targets", ""), "trigger": fields.get("Trigger", ""),
            "function": fields.get("Function", ""),
            "prevents": fields.get("Prevents", ""), "improves": fields.get("Improves", ""),
            "guardrails": fields.get("Guardrails", ""), "extra": extra,
            "vector": g["vector"], "deps": deps, "note": g.get("note", ""),
            "draws": draws, "value": v["base"], "valueLow": v["low"], "valueHigh": v["high"],
            "onetime": v["onetime"], "riskEV": v["risk"],
            "options": c["options"], "rec": c["option"],
            "build": c["build"], "run": c["run_yr"],
            "platB": c["plat_build"], "platR": c["plat_run"],
            "tcoAlloc": c["tco_alloc"], "net": c.get("net_yr", 0),
            "payback": c.get("payback_mo"),
            "workload": spec["workload"], "tier": spec["tier"],
            "family": wl.get("family") if "slm" in wl["options"] else None,
            "volume": round(vols[spec["vol"]] * spec.get("mult", 1.0)),
            "volKey": spec["vol"], "platform": platform,
        }
        rec["search"] = " ".join([uc_id, rec["name"], rec["domain"], rec["function"],
                                  rec["targets"], rec["prevents"], rec["improves"],
                                  " ".join(rec["patterns"]),
                                  " ".join(d["id"] for d in deps)]).lower()
        ucs.append(rec)

    meta = {"riskNames": RISK_NAMES}
    html = ((HERE / "explorer-template.html").read_text()
            .replace("__UCS__", json.dumps(ucs))
            .replace("__META__", json.dumps(meta)))
    Path(args.output).write_text(html)
    n_missing_fn = sum(1 for u in ucs if not u["function"])
    print(f"Explorer written to {args.output} ({len(html)//1024} KiB, {len(ucs)} use cases; "
          f"{n_missing_fn} missing Function text)")


if __name__ == "__main__":
    main()
