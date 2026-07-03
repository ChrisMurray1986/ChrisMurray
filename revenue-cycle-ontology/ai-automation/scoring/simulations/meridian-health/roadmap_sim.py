#!/usr/bin/env python3
"""Meridian Health roadmap simulation.

Python port of the planner app's greedy budget-constrained scheduler, extended
for the simulation's installed-vendor footprint:
  - Fathom autonomous coding (ED + Radiology) -> UC-05-01 treated as live at
    ~50% of its value; the remaining share is an EXPANSION candidate (inpatient/
    profee scope) at reduced build cost.
  - Humata prior auth -> UC-01-08/UC-01-09 live at ~70%; remainder = payer-
    coverage expansion candidates.

Outputs roadmap.json (quarters, launches, remediations, curves, backlog) and a
console summary. Run from the scoring/ directory:
  python3 simulations/meridian-health/roadmap_sim.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2]))
import yaml

import cost as cm
import score as sc
import value as vm

HERE = Path(__file__).parent
SCORING = Path(__file__).parents[2]

BUDGET_Q = 2_500_000
HORIZON = 8
LIVE = {  # vendor-covered UCs: coverage share, expansion build multiplier
    "UC-05-01": {"coverage": 0.5, "exp_build_mult": 0.30, "label": "Expand Fathom scope (inpatient/profee coding)"},
    "UC-01-08": {"coverage": 0.7, "exp_build_mult": 0.20, "label": "Expand Humata payer coverage (auth submission)"},
    "UC-01-09": {"coverage": 0.7, "exp_build_mult": 0.20, "label": "Expand Humata payer coverage (auth tracking)"},
}
REMED = {
    "facet_cost": {"data": 120e3, "integration": 150e3, "connectivity": 60e3,
                   "workflow": 60e3, "org": 40e3, "governance": 120e3, "legal": 30e3},
    "facet_dur": {"data": 2, "integration": 2, "connectivity": 1, "workflow": 1,
                  "org": 1, "governance": 2, "legal": 1},
    "dim_cost": {"data": 300e3, "integration": 250e3, "connectivity": 150e3,
                 "workflow": 120e3, "org": 80e3, "governance": 200e3, "legal": 60e3,
                 "economics": 40e3},
    "dim_dur": {"data": 2, "integration": 2, "governance": 2, "connectivity": 1,
                "workflow": 1, "org": 1, "legal": 1, "economics": 1},
    "ramp": [0.25, 0.5, 0.75, 1.0],
}
DIM_KEYS = sc.DIM_KEYS


def structured_gaps(uc, dims, facets, catalog):
    out = []
    for letter, req in uc["vector"].items():
        if req is None:
            continue
        dim = DIM_KEYS[letter]
        have = dims.get(dim, 0)
        if have < req:
            out.append({"kind": "dim", "dim": dim, "req": req,
                        "structural": req - have >= 2 or (have <= 1 and req >= 3)})
    for fid in uc.get("facets", []):
        v = facets.get(fid, 0)
        if v == "blocked":
            out.append({"kind": "blocked", "fid": fid})
        elif v in (0, 1):
            out.append({"kind": "facet", "fid": fid, "dim": catalog[fid]["dim"],
                        "structural": v == 0})
    return out


def main():
    assessment = yaml.safe_load((HERE / "meridian-assessment.yaml").read_text())
    profile = yaml.safe_load((HERE / "meridian-org-profile.yaml").read_text())
    catalog, use_cases = sc.load_vectors(SCORING / "gate-vectors.yaml")
    cdrivers = yaml.safe_load((SCORING / "cost-drivers.yaml").read_text())

    ccomp = cm.compute(profile, cdrivers)
    ccomp = cm.join_value(profile, ccomp, None, None)
    by = {r["id"]: r for r in ccomp["rows"]}

    dims = dict(assessment["dimensions"])
    facets = dict(assessment["facets"])
    in_prog, live, quarters = [], {}, []
    baseline_net = sum(by[uc]["net_yr"] * v["coverage"] for uc, v in LIVE.items())
    cum_spend = cum_value = 0.0

    for q in range(1, HORIZON + 1):
        for p in [p for p in in_prog if p["done"] == q]:
            if p["kind"] == "facet":
                facets[p["fid"]] = 2
            else:
                dims[p["dim"]] = max(dims[p["dim"]], p["level"])
        acts, cands, gap_unlock = [], [], {}
        for uc_id, uc in use_cases.items():
            if uc_id in live or uc_id not in by:
                continue
            gaps = structured_gaps(uc, dims, facets, catalog)
            if any(g["kind"] == "blocked" for g in gaps):
                continue
            struct = [g for g in gaps if g["kind"] == "dim" or g.get("structural")]
            base = by[uc_id]
            cov = LIVE.get(uc_id)
            net = base["net_yr"] * (1 - cov["coverage"]) if cov else base["net_yr"]
            build = (base["build"] * cov["exp_build_mult"] + base["plat_build"] * 0.2) if cov \
                else base["build"] + base["plat_build"]
            if not struct:
                partials = [g for g in gaps if g["kind"] == "facet"]
                cost = build + sum(REMED["facet_cost"][g["dim"]] / 2 for g in partials)
                if net > 0:
                    label = cov["label"] if cov else f"Launch {uc_id} — {uc['name']}"
                    cands.append({"type": "launch", "uc": uc_id, "cost": cost, "net": net,
                                  "score": net / cost, "partials": partials, "label": label})
            else:
                for g in struct:
                    key = f"facet:{g['fid']}" if g["kind"] == "facet" else f"dim:{g['dim']}:{g['req']}"
                    e = gap_unlock.setdefault(key, {"net": 0.0, "n": 0, "g": g})
                    e["net"] += max(0.0, base["net_yr"])
                    e["n"] += 1
        for key, e in gap_unlock.items():
            if any(p["key"] == key and p["done"] > q for p in in_prog):
                continue
            g = e["g"]
            if g["kind"] == "facet":
                cur = facets[g["fid"]]
                cost = REMED["facet_cost"][g["dim"]] * (0.5 if cur == 1 else 1.0)
                dur, label = REMED["facet_dur"][g["dim"]], f"Remediate {g['fid']}"
            else:
                lift = g["req"] - dims[g["dim"]]
                if lift <= 0:
                    continue
                cost = REMED["dim_cost"][g["dim"]] * lift
                dur, label = REMED["dim_dur"][g["dim"]], f"Raise {g['dim']} maturity to {g['req']}"
            cands.append({"type": "rem", "key": key, "cost": cost, "dur": dur, "label": label,
                          "score": 0.5 * e["net"] / max(cost, 1), "g": g,
                          "why": f"unlocks {e['n']} UCs ({e['net']/1e6:.1f}M/yr held)"})
        cands.sort(key=lambda c: -c["score"])
        spend = 0.0
        for c in cands:
            if spend + c["cost"] > BUDGET_Q:
                continue
            spend += c["cost"]
            if c["type"] == "launch":
                live[c["uc"]] = {"q": q, "net": c["net"]}
                for g in c["partials"]:
                    facets[g["fid"]] = 2
                acts.append({"kind": "launch", "label": c["label"], "cost": c["cost"],
                             "net": c["net"], "uc": c["uc"]})
            else:
                in_prog.append({"key": c["key"], "done": q + c["dur"], "kind": c["g"]["kind"],
                                "fid": c["g"].get("fid"), "dim": c["g"].get("dim"),
                                "level": c["g"].get("req")})
                acts.append({"kind": "rem", "label": c["label"], "cost": c["cost"],
                             "why": c["why"], "ready": q + c["dur"]})
        q_val = sum(l["net"] / 4 * REMED["ramp"][min(q - l["q"], 3)] for l in live.values())
        cum_spend += spend
        cum_value += q_val
        quarters.append({"q": q, "acts": acts, "spend": spend, "q_value": q_val,
                         "cum_spend": cum_spend, "cum_value": cum_value,
                         "live_n": len(live), "exit_runrate": q_val * 4})

    backlog = sorted(({"uc": u, "net": by[u]["net_yr"]} for u in use_cases
                      if u not in live and u in by and by[u]["net_yr"] > 0),
                     key=lambda x: -x["net"])
    out = {"org": "Meridian Health (simulated)", "budget_q": BUDGET_Q, "horizon": HORIZON,
           "baseline_vendor_net": baseline_net, "quarters": quarters,
           "launched": {u: {"q": l["q"], "net": l["net"], "name": use_cases[u]["name"]}
                        for u, l in live.items()},
           "backlog": backlog[:25]}
    (HERE / "roadmap.json").write_text(json.dumps(out, indent=1))
    last = quarters[-1]
    print(f"launched {len(live)} | invested ${last['cum_spend']/1e6:.1f}M | "
          f"cum net value ${last['cum_value']/1e6:.1f}M | exit run-rate ${last['exit_runrate']/1e6:.1f}M/yr | "
          f"vendor baseline ${baseline_net/1e6:.1f}M/yr | backlog {len(backlog)}")
    for qq in quarters:
        top = "; ".join(a["label"] for a in qq["acts"][:4])
        print(f"Q{qq['q']}: spend ${qq['spend']/1e6:.2f}M, live {qq['live_n']}, "
              f"runrate ${qq['exit_runrate']/1e6:.1f}M/yr — {top}" + (" …" if len(qq['acts']) > 4 else ""))


if __name__ == "__main__":
    main()
