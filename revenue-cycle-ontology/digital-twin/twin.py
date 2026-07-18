#!/usr/bin/env python3
"""Revenue cycle operations digital twin — deterministic monthly flow simulation.

Simulates the claim lifecycle of a health system (baseline: ~$10B NPR, Epic on
AWS, Snowflake/Databricks data plane) as a staged work-flow network grounded in
the base ontology: stages bind process IDs, staffing pools bind ROLE-* IDs,
denial causes bind FM-* IDs, outputs bind KPI-* IDs. Scenarios (workflow
changes, AI/automation additions bound to UC-* IDs, staffing changes) are
applied as ramped parameter overlays; the engine reports impact on financials,
productivity, and patient/caregiver experience versus the untouched baseline.

Usage (from this directory; sole dependency: PyYAML):
  python3 twin.py                                # baseline run, summary to stdout
  python3 twin.py --scenario scenarios/SCN-01-ai-automation-wave1.yaml \
                  -o examples/SCN-01-report.md [--csv out.csv] [--json out.json]
  python3 twin.py --compare scenarios/*.yaml -o examples/scenario-comparison.md

The model is deterministic and flow-based (no random draws): identical inputs
always reproduce identical outputs, so runs are diffable records.
"""

import argparse
import copy
import csv
import io
import json
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).parent
DAYS_PER_MONTH = 30.44
WORKDAYS_PER_MONTH = 21.7
PATIENT_TAIL_DAYS = 60.0        # collection tail on patient-responsibility dollars
AUTH_WAIT_BASE_DAYS = 3.5       # baseline auth turnaround at baseline manual share
AUTONOMY_CEILING = {"R1": 3, "R2": 3, "R3": 3, "R4": 4}   # ai-automation/README.md ceiling rule


# ----------------------------------------------------------------------------
# Loading & validation
# ----------------------------------------------------------------------------

def load_config(path):
    cfg = yaml.safe_load(Path(path).read_text())
    warnings = []
    # NPR cross-check
    monthly = sum(s["monthly_accounts"] * s["avg_net_rev"] for s in cfg["segments"].values())
    stated = cfg["organization"]["npr_annual"]
    if abs(monthly * 12 - stated) / stated > 0.03:
        warnings.append(f"segment volumes imply NPR ${monthly*12/1e9:.2f}B vs stated ${stated/1e9:.2f}B")
    # denial cause shares
    tot = sum(c["share"] for c in cfg["denials"]["causes"].values())
    if abs(tot - 1.0) > 0.01:
        warnings.append(f"denial cause shares sum to {tot:.3f}, expected 1.0")
    # stage -> pool references
    pools = cfg["staffing"]["pools"]
    for st in cfg["stages"]:
        if st["pool"] not in pools:
            raise SystemExit(f"stage {st['id']} references unknown pool {st['pool']}")
        st.setdefault("quality_index", 1.0)
        st.setdefault("dwell_days", 0.0)
        st.setdefault("lag_chain", "none")
    ids = [st["id"] for st in cfg["stages"]]
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate stage ids")
    for cause in cfg["denials"]["causes"].values():
        if cause["owner_stage"] not in ids:
            raise SystemExit(f"denial cause owner_stage {cause['owner_stage']} not a stage id")
    for rule in (cfg.get("payer_dynamics") or {}).get("rules", []):
        if rule["trigger"]["metric"] not in PAYER_METRICS:
            raise SystemExit(f"payer rule {rule['id']}: unknown metric {rule['trigger']['metric']}")
        for eff in rule.get("responses", []):
            parts = eff["target"].split(".")
            if parts[0] == "stages" and parts[1] not in ids:
                raise SystemExit(f"payer rule {rule['id']}: unknown stage in {eff['target']}")
            if parts[0] not in ("stages", "levers", "denials", "segments"):
                raise SystemExit(f"payer rule {rule['id']}: unknown target root {eff['target']}")
    return cfg, warnings


def load_scenario(path, cfg):
    scn = yaml.safe_load(Path(path).read_text())
    warnings = []
    known_ucs = set()
    gv = HERE.parent / "ai-automation" / "scoring" / "gate-vectors.yaml"
    if gv.exists():
        known_ucs = set(yaml.safe_load(gv.read_text()).get("use_cases", {}))
    stage_ids = {st["id"] for st in cfg["stages"]}
    for iv in scn.get("interventions", []):
        iv.setdefault("start_month", 1)
        iv.setdefault("ramp_months", 1)
        if iv.get("type") == "ai_automation":
            if not iv.get("use_cases"):
                warnings.append(f"{iv['id']}: ai_automation intervention with no use_cases binding")
            for uc in iv.get("use_cases", []):
                if known_ucs and uc not in known_ucs:
                    warnings.append(f"{iv['id']}: {uc} not found in gate-vectors.yaml")
            tier, aut = iv.get("risk_tier"), iv.get("autonomy")
            if tier and aut:
                if int(aut[1]) > AUTONOMY_CEILING.get(tier, 4):
                    warnings.append(f"{iv['id']}: autonomy {aut} exceeds ceiling for {tier} "
                                    f"(A{AUTONOMY_CEILING[tier]}) — governance violation")
        for eff in iv.get("effects", []):
            top = eff["target"].split(".")[0]
            if top == "stages" and eff["target"].split(".")[1] not in stage_ids:
                warnings.append(f"{iv['id']}: effect target {eff['target']} — unknown stage")
            elif top not in ("stages", "levers", "denials", "segments"):
                warnings.append(f"{iv['id']}: effect target {eff['target']} — unknown root")
        for sc in iv.get("staffing", []):
            if sc["pool"] not in cfg["staffing"]["pools"]:
                warnings.append(f"{iv['id']}: staffing change on unknown pool {sc['pool']}")
            sc.setdefault("start_month", iv["start_month"])
            sc.setdefault("glide_months", 1)
    return scn, warnings


# ----------------------------------------------------------------------------
# Scenario overlay
# ----------------------------------------------------------------------------

def ramp_fraction(month, start, ramp):
    if month < start:
        return 0.0
    return min(1.0, (month - start + 1) / max(1, ramp))


def _resolve(root, dotted):
    """Return (container, key) for a dotted path; stages addressed by id."""
    parts = dotted.split(".")
    node = root
    for p in parts[:-1]:
        if p == "stages" and isinstance(node, dict) and isinstance(node.get("stages"), list):
            node = {st["id"]: st for st in node["stages"]}
        else:
            node = node[p]
    return node, parts[-1]


def apply_effect(cfg, eff, frac):
    node, key = _resolve(cfg, eff["target"])
    cur = node[key]
    def blend(base, op_set=None, op_mult=None, op_delta=None):
        if op_set is not None:
            return base + (op_set - base) * frac
        if op_mult is not None:
            return base * (1 + (op_mult - 1) * frac)
        return base + op_delta * frac
    if isinstance(cur, dict):   # per-segment map param, scalar op applies to all
        for k in cur:
            cur[k] = blend(cur[k], eff.get("set"), eff.get("mult"), eff.get("delta"))
    else:
        node[key] = blend(cur, eff.get("set"), eff.get("mult"), eff.get("delta"))


def month_params(cfg, scenario, month):
    """Config with all scenario effects applied at this month's ramp fractions."""
    p = copy.deepcopy(cfg)
    ramping = 0
    if scenario:
        for iv in scenario.get("interventions", []):
            f = ramp_fraction(month, iv["start_month"], iv["ramp_months"])
            if 0.0 < f < 1.0:
                ramping += 1
            if f <= 0.0:
                continue
            for eff in iv.get("effects", []):
                apply_effect(p, eff, f)
    return p, ramping


def pool_fte(cfg, scenario, month):
    fte = {k: float(v["fte"]) for k, v in cfg["staffing"]["pools"].items()}
    if scenario:
        for iv in scenario.get("interventions", []):
            for sc in iv.get("staffing", []):
                f = ramp_fraction(month, sc["start_month"], sc["glide_months"])
                if f <= 0.0:
                    continue
                if "fte_delta" in sc:
                    fte[sc["pool"]] += sc["fte_delta"] * f
                elif "fte_set" in sc:
                    base = cfg["staffing"]["pools"][sc["pool"]]["fte"]
                    fte[sc["pool"]] = base + (sc["fte_set"] - base) * f
    return {k: max(0.0, v) for k, v in fte.items()}


def scenario_costs(scenario, month):
    one_time, run_rate = 0.0, 0.0
    if scenario:
        for iv in scenario.get("interventions", []):
            c = iv.get("costs", {})
            if month == iv["start_month"]:
                one_time += c.get("one_time", 0.0)
            f = ramp_fraction(month, iv["start_month"], iv["ramp_months"])
            run_rate += c.get("run_rate_annual", 0.0) / 12.0 * f
    return one_time, run_rate


# ----------------------------------------------------------------------------
# Payer response dynamics
# ----------------------------------------------------------------------------
# Payer behavior is endogenous: each rule watches a PROVIDER-INTENT metric
# (baseline + scenario effects, before any payer response) so the baseline run
# never self-triggers and the feedback cannot oscillate. Intensity climbs
# 1/ramp_months per month while the lagged metric exceeds threshold, decays
# 1/decay_months otherwise; responses are effect-grammar edits scaled by it.

PAYER_METRICS = ("prevention_gain_pts", "appeal_recovery_gain_pts",
                 "auth_automation_gain_pts", "writeoff_reduction_pts")


def _denial_rates(cfg):
    """(initial-denial dollar rate, write-off dollar rate) as shares of expected net."""
    stage_q = {st["id"]: st.get("quality_index", 1.0) for st in cfg["stages"]}
    idr = cfg["denials"]["initial_denial_rate_dollars"]
    rate = wo = 0.0
    for cause in cfg["denials"]["causes"].values():
        d = idr * cause["share"] * stage_q[cause["owner_stage"]]
        rate += d
        wo += d * (1 - cause["recovery"])
    return rate, wo


def _appeal_recovery(cfg):
    """Weighted recovery over appealable causes (appeal_rate >= 0.10)."""
    num = den = 0.0
    for cause in cfg["denials"]["causes"].values():
        if cause["appeal_rate"] >= 0.10:
            w = cause["share"] * cause["appeal_rate"]
            num += w * cause["recovery"]
            den += w
    return num / den if den else 0.0


def payer_metrics(base_cfg, provider):
    b_rate, b_wo = _denial_rates(base_cfg)
    p_rate, p_wo = _denial_rates(provider)
    return {
        "prevention_gain_pts": b_rate - p_rate,
        "appeal_recovery_gain_pts": _appeal_recovery(provider) - _appeal_recovery(base_cfg),
        "auth_automation_gain_pts": _scalar_mean(provider, "prior_auth", "auto_rate")
                                    - _scalar_mean(base_cfg, "prior_auth", "auto_rate"),
        "writeoff_reduction_pts": b_wo - p_wo,
    }


# ----------------------------------------------------------------------------
# One simulated month
# ----------------------------------------------------------------------------

def seg_value(param, seg):
    return param[seg] if isinstance(param, dict) else param


def simulate(cfg, scenario=None, payer=True):
    horizon = cfg["meta"]["horizon_months"]
    staff = cfg["staffing"]
    prod_hours_fte = staff["hours_month"] * staff["productive_pct"]
    growth = cfg.get("growth_annual_pct", 0.0)
    backlog = {k: 0.0 for k in staff["pools"]}      # carried hours by pool
    months = []
    prev_ar_balance = None

    pd_cfg = cfg.get("payer_dynamics") or {}
    pd_rules = pd_cfg.get("rules", []) if (
        payer and scenario and pd_cfg.get("enabled")
        and scenario.get("payer_dynamics", True) is not False) else []
    intensity, metric_history = {r["id"]: 0.0 for r in pd_rules}, []

    for m in range(1, horizon + 1):
        p, ramping = month_params(cfg, scenario, m)

        # --- payer response overlay (on provider-intent params) -------------
        if pd_rules:
            metric_history.append(payer_metrics(cfg, p))
            for rule in pd_rules:
                idx = m - rule["lag_months"] - 1
                lagged = metric_history[idx] if idx >= 0 else None
                triggered = (lagged is not None and
                             lagged[rule["trigger"]["metric"]] >= rule["trigger"]["threshold"])
                i = intensity[rule["id"]]
                i = min(1.0, i + 1.0 / max(1, rule["ramp_months"])) if triggered \
                    else max(0.0, i - 1.0 / max(1, rule["decay_months"]))
                intensity[rule["id"]] = i
                if i > 0.0:
                    for eff in rule["responses"]:
                        apply_effect(p, eff, i)
        segs = p["segments"]
        seg_ids = list(segs)
        gf = (1 + growth) ** ((m - 1) / 12.0)
        accounts = {s: segs[s]["monthly_accounts"] * gf for s in seg_ids}
        expected = {s: accounts[s] * segs[s]["avg_net_rev"] for s in seg_ids}
        expected_total = sum(expected.values())

        # --- denial model -----------------------------------------------------
        den = p["denials"]
        stage_by_id = {st["id"]: st for st in p["stages"]}
        idr_base = den["initial_denial_rate_dollars"]
        denied_d, writeoff_d, appeal_wt, quality_factor = 0.0, 0.0, 0.0, 0.0
        for cause in den["causes"].values():
            q = stage_by_id[cause["owner_stage"]]["quality_index"]
            quality_factor += cause["share"] * q
            d = expected_total * idr_base * cause["share"] * q
            denied_d += d
            writeoff_d += d * (1 - cause["recovery"])
            appeal_wt += cause["share"] * q * cause["appeal_rate"]
        idr_eff = denied_d / expected_total if expected_total else 0.0
        # denied-claim counts scale with the same quality factor; appeals are the
        # cause-weighted share of denied claims that get a formal appeal
        denied_claims = {s: accounts[s] * segs[s]["denial_count_rate"] * quality_factor
                         for s in seg_ids}
        appeal_share = appeal_wt / quality_factor if quality_factor else 0.0
        appealed_claims = {s: denied_claims[s] * appeal_share for s in seg_ids}

        # --- financial levers & leakage --------------------------------------
        lev = p["levers"]
        patient_resp = expected_total * lev["patient_share_of_npr"]
        bad_debt = patient_resp * (1 - lev["selfpay_yield"])
        up_leak = expected_total * lev["underpayment_pct"] * (1 - lev["underpayment_detect_rate"])
        chg_leak = expected_total * lev["charge_leakage_pct"] * (1 - lev["charge_capture_rate"])

        # --- driver volumes ---------------------------------------------------
        statements = {s: accounts[s] * segs[s]["patient_balance_rate"] for s in seg_ids}
        drivers = {"accounts": accounts, "denied_claims": denied_claims,
                   "appealed_claims": appealed_claims, "patient_statements": statements}

        # --- stage demand -----------------------------------------------------
        pool_demand = {k: 0.0 for k in staff["pools"]}
        stage_rows, total_touches, auto_touches = {}, 0.0, 0.0
        for st in p["stages"]:
            units = drivers[st["driver"]]
            hours = touches = auto = 0.0
            for s in seg_ids:
                u = units[s] * seg_value(st["applies"], s) * seg_value(st["touch_rate"], s)
                a = u * seg_value(st["auto_rate"], s)
                manual = u - a
                touches += u
                auto += a
                hours += manual * seg_value(st["min_per_touch"], s) / 60.0
            pool_demand[st["pool"]] += hours
            stage_rows[st["id"]] = {"pool": st["pool"], "hours": hours,
                                    "touches": touches, "auto": auto,
                                    "dwell": st["dwell_days"], "lag": st["lag_chain"]}
            total_touches += touches
            auto_touches += auto

        # --- capacity, overtime, backlog -------------------------------------
        fte = pool_fte(cfg, scenario, m)
        pool_rows = {}
        labor_cost = ot_cost = 0.0
        for k, pool in staff["pools"].items():
            cap = fte[k] * prod_hours_fte
            need = pool_demand[k] + backlog[k]
            ot_avail = cap * staff["ot_cap_pct"]
            ot_used = min(max(0.0, need - cap), ot_avail) if cap > 0 else 0.0
            served = min(need, cap + ot_used)
            backlog[k] = need - served
            util = need / cap if cap > 0 else float("inf")
            hourly = pool["loaded_cost"] / 12.0 / staff["hours_month"]
            labor_cost += fte[k] * pool["loaded_cost"] / 12.0
            ot_cost += ot_used * hourly * (1 + staff["overtime_premium"])
            pool_rows[k] = {"fte": fte[k], "demand": pool_demand[k], "capacity": cap,
                            "util": util, "ot_hours": ot_used,
                            "backlog_days": backlog[k] / (cap / WORKDAYS_PER_MONTH) if cap > 0 else 0.0}

        # --- lag chain & AR days ---------------------------------------------
        bill_lag = 0.0
        for sid, row in stage_rows.items():
            if row["lag"] != "prebill":
                continue
            pr = pool_rows[row["pool"]]
            share = row["hours"] / pool_demand[row["pool"]] if pool_demand[row["pool"]] > 0 else 0.0
            bill_lag += row["dwell"] + pr["backlog_days"] * share
        w_pay = sum(expected[s] / expected_total * segs[s]["payment_lag_days"] for s in seg_ids)
        patient_tail = PATIENT_TAIL_DAYS * (1 - lev["pos_collection_rate"])
        ar_days = (bill_lag + w_pay + idr_eff * den["denial_cycle_days"]
                   + lev["patient_share_of_npr"] * patient_tail)

        # --- revenue & cash ---------------------------------------------------
        # gross_expected holds the leakage-inclusive envelope so the baseline
        # parameterization reproduces stated NPR exactly (leakage embedded).
        base_leak = _baseline_leakage(cfg, expected_total)
        revenue = expected_total + (base_leak - (writeoff_d + bad_debt + up_leak + chg_leak))
        one_time, run_rate = scenario_costs(scenario, m)
        ext_tech = (p["organization"]["external_spend_annual"]
                    + p["organization"]["tech_run_annual"]) / 12.0
        overhead = p["organization"]["overhead_fte"] * p["organization"]["overhead_loaded_cost"] / 12.0
        total_cost = labor_cost + ot_cost + ext_tech + overhead + run_rate + one_time
        ar_balance = revenue / DAYS_PER_MONTH * ar_days
        cash = revenue - (ar_balance - prev_ar_balance if prev_ar_balance is not None else 0.0)
        prev_ar_balance = ar_balance

        # --- experience -------------------------------------------------------
        pre_pools = ["prereg", "eligibility", "prior_auth", "registration"]
        service_level = min(min(1.0, 1.0 / pool_rows[k]["util"]) if pool_rows[k]["util"] > 0 else 1.0
                            for k in pre_pools)
        auth_st = stage_by_id["prior_auth"]
        auth_manual = 1 - (sum(seg_value(auth_st["auto_rate"], s) for s in seg_ids) / len(seg_ids))
        base_auth_manual = 1 - _scalar_mean(cfg, "prior_auth", "auto_rate")
        auth_wait = (AUTH_WAIT_BASE_DAYS * auth_manual / base_auth_manual
                     + pool_rows["prior_auth"]["backlog_days"])
        pfs_util = pool_rows["pfs"]["util"]
        complaints = (lev["complaints_per_1k"]
                      * (1 + 0.5 * max(0.0, pfs_util - 0.9) / 0.1)
                      * (cfg["levers"]["estimate_accuracy"] / max(0.3, lev["estimate_accuracy"])) ** 0.5)
        px_vals = {
            "financial_clearance": lev["financial_clearance_rate"] * service_level,
            "estimate_accuracy": lev["estimate_accuracy"],
            "auth_wait_days": auth_wait,
            "billing_complaints": complaints,
            "surprise_bills": lev["surprise_bill_per_1k"],
            "self_service": lev["self_service_rate"],
            "first_contact_res": lev["first_contact_resolution"],
        }
        rework_hours = sum(stage_rows[s]["hours"] for s in
                           ("denial_triage", "denial_resolution", "appeals"))
        rework_hours += stage_rows["ar_followup"]["hours"] * 0.5
        total_hours = sum(pool_demand.values())
        utils = [pool_rows[k]["util"] for k in pool_rows if pool_rows[k]["capacity"] > 0]
        cx_vals = {
            "workload_balance": sum(utils) / len(utils),
            "backlog_pressure": sum(pool_rows[k]["backlog_days"] for k in pool_rows) / len(pool_rows),
            "rework_share": rework_hours / total_hours if total_hours else 0.0,
            "automation_relief": auto_touches / total_touches if total_touches else 0.0,
            "provider_burden": 0.5 * lev["queries_per_100_ip"] / cfg["levers"]["queries_per_100_ip"]
                               + 0.5 * lev["clinic_auth_burden"] / cfg["levers"]["clinic_auth_burden"],
            "change_load": float(ramping),
        }
        pxi = _index(px_vals, p["experience"]["patient"]["components"])
        cxi = _index(cx_vals, p["experience"]["caregiver"]["components"])

        months.append({
            "month": m, "expected_net": expected_total, "revenue": revenue,
            "denied_dollars": denied_d, "idr": idr_eff, "denial_writeoff": writeoff_d,
            "bad_debt": bad_debt, "underpayment_leak": up_leak, "charge_leak": chg_leak,
            "labor_cost": labor_cost, "ot_cost": ot_cost, "scenario_run_cost": run_rate,
            "one_time_cost": one_time, "total_cost": total_cost, "cash": cash,
            "ar_days": ar_days, "ar_balance": ar_balance, "bill_lag_days": bill_lag,
            "pxi": pxi, "cxi": cxi, "px_vals": px_vals, "cx_vals": cx_vals,
            "pools": pool_rows, "stages": stage_rows,
            "total_touches": total_touches, "auto_touches": auto_touches,
            "denied_claims": sum(denied_claims.values()),
            "appealed_claims": sum(appealed_claims.values()),
            "patient_resp": patient_resp,
            "payer": dict(intensity),
            "payer_pressure": (sum(intensity.values()) / len(intensity)) if intensity else 0.0,
            "fte_total": sum(fte.values()) + cfg["organization"]["overhead_fte"],
        })
    return months


def _baseline_leakage(cfg, expected_total):
    """Leakage envelope at baseline parameters, scaled to this month's volumes."""
    lev = cfg["levers"]
    den = cfg["denials"]
    wo = sum(expected_total * den["initial_denial_rate_dollars"] * c["share"]
             * (1 - c["recovery"]) for c in den["causes"].values())
    bad = expected_total * lev["patient_share_of_npr"] * (1 - lev["selfpay_yield"])
    up = expected_total * lev["underpayment_pct"] * (1 - lev["underpayment_detect_rate"])
    chg = expected_total * lev["charge_leakage_pct"] * (1 - lev["charge_capture_rate"])
    return wo + bad + up + chg


def _scalar_mean(cfg, stage_id, param):
    st = next(s for s in cfg["stages"] if s["id"] == stage_id)
    v = st[param]
    return sum(v.values()) / len(v) if isinstance(v, dict) else v


def _index(values, components):
    score = wsum = 0.0
    for name, comp in components.items():
        v = values[name]
        lo, hi = comp["worst"], comp["best"]
        x = (v - lo) / (hi - lo) if hi != lo else 0.0
        score += comp["weight"] * max(0.0, min(1.0, x))
        wsum += comp["weight"]
    return 100.0 * score / wsum if wsum else 0.0


# ----------------------------------------------------------------------------
# Reporting
# ----------------------------------------------------------------------------

def annualize(months, year):
    span = [r for r in months if (year - 1) * 12 < r["month"] <= year * 12]
    return span


def _sum(rows, key):
    return sum(r[key] for r in rows)


def money(x):
    if abs(x) >= 1e9:
        return f"${x/1e9:,.2f}B"
    if abs(x) >= 1e6:
        return f"${x/1e6:,.1f}M"
    return f"${x/1e3:,.0f}K"


def delta_money(x):
    sign = "+" if x >= 0 else "−"
    return f"{sign}{money(abs(x))}"


def npv(base, scen, wacc, years):
    total = 0.0
    for b, s in zip(base, scen):
        if b["month"] > years * 12:
            break
        benefit = (s["revenue"] - b["revenue"]) - (s["total_cost"] - b["total_cost"])
        # cash-timing benefit: AR balance released (or absorbed) vs baseline
        benefit -= ((s["ar_balance"] - b["ar_balance"])
                    - (prev_delta(base, scen, b["month"])))
        total += benefit / (1 + wacc) ** (b["month"] / 12.0)
    return total


def prev_delta(base, scen, month):
    if month <= 1:
        return 0.0
    b = base[month - 2]
    s = scen[month - 2]
    return s["ar_balance"] - b["ar_balance"]


def payer_section(cfg, base, scen, gross, wacc, years):
    """Payer response dynamics report block. Empty if dynamics were not simulated."""
    rules = (cfg.get("payer_dynamics") or {}).get("rules", [])
    if gross is None or not rules:
        return []
    L = ["## Payer response dynamics\n"]
    any_triggered = any(r["payer_pressure"] > 0 for r in scen)
    if not any_triggered:
        L.append("*No payer counter-response triggered: the program stays below every "
                 "reaction threshold (see `payer_dynamics` in the config). Gross and "
                 "net-of-payer-response results are identical.*\n")
        return L
    L.append("Payer behavior is endogenous in this run: sustained provider gains trigger "
             "lagged, capped counter-moves. Intensities are 0–1 (1.0 = full response).\n")
    L.append("| Rule | Counter-move | Trigger metric | First active | Peak | End |")
    L.append("|---|---|---|---|---|---|")
    for rule in rules:
        rid = rule["id"]
        series = [(r["month"], r["payer"].get(rid, 0.0)) for r in scen]
        active = [(mo, v) for mo, v in series if v > 0]
        first = f"M{active[0][0]}" if active else "—"
        peak = max((v for _, v in series), default=0.0)
        L.append(f"| {rid} | {rule['name']} | {rule['trigger']['metric']} ≥ "
                 f"{rule['trigger']['threshold']} | {first} | {peak:.2f} | "
                 f"{series[-1][1]:.2f} |")
    last, g_last, b_last = scen[-1], gross[-1], base[-1]
    rev_net = (last["revenue"] - b_last["revenue"]) * 12
    rev_gross = (g_last["revenue"] - b_last["revenue"]) * 12
    npv_net, npv_gross = npv(base, scen, wacc, years), npv(base, gross, wacc, years)
    erosion_pct = (1 - npv_net / npv_gross) * 100 if npv_gross else 0.0
    L.append("")
    L.append("| Measure | Gross (no payer response) | Net (with payer response) | Erosion |")
    L.append("|---|---|---|---|")
    L.append(f"| Steady-state net revenue /yr | {delta_money(rev_gross)} | {delta_money(rev_net)} | "
             f"{delta_money(rev_net - rev_gross)} |")
    L.append(f"| {years}-year NPV | {delta_money(npv_gross)} | {delta_money(npv_net)} | "
             f"{erosion_pct:.0f}% |")
    L.append(f"| Net days in AR (end) | {g_last['ar_days']:.1f} | {last['ar_days']:.1f} | "
             f"+{last['ar_days'] - g_last['ar_days']:.1f} d |")
    L.append(f"| Initial denial rate (end) | {g_last['idr']*100:.1f}% | {last['idr']*100:.1f}% | "
             f"+{(last['idr'] - g_last['idr'])*100:.1f} pt |")
    L.append("")
    L.append("*All headline figures elsewhere in this report are NET of payer response. "
             "Responses are bounded (MLR floors, Stars/CTM exposure, prompt-pay statutes, "
             "employer abrasion) and decay if the provider posture normalizes — see "
             "`payer_dynamics` rationale fields in the config.*\n")
    return L


def kpi_table(cfg, last, base_last):
    rows = [
        ("KPI-IDR", "Initial denial rate ($)", f"{base_last['idr']*100:.1f}%", f"{last['idr']*100:.1f}%"),
        ("KPI-DENWO", "Denial write-off % NPR",
         f"{base_last['denial_writeoff']/base_last['expected_net']*100:.2f}%",
         f"{last['denial_writeoff']/last['expected_net']*100:.2f}%"),
        ("KPI-DAR", "Net days in AR", f"{base_last['ar_days']:.1f}", f"{last['ar_days']:.1f}"),
        ("KPI-DNFB", "Bill lag days (prebill chain)", f"{base_last['bill_lag_days']:.1f}",
         f"{last['bill_lag_days']:.1f}"),
        ("KPI-CTC", "Cost to collect (% cash)",
         f"{base_last['total_cost']/base_last['cash']*100:.2f}%",
         f"{last['total_cost']/last['cash']*100:.2f}%"),
        ("KPI-ESTIMATE-ACC", "Estimate accuracy", f"{base_last['px_vals']['estimate_accuracy']*100:.0f}%",
         f"{last['px_vals']['estimate_accuracy']*100:.0f}%"),
        ("KPI-CLEARANCE", "Financial clearance rate",
         f"{base_last['px_vals']['financial_clearance']*100:.0f}%",
         f"{last['px_vals']['financial_clearance']*100:.0f}%"),
        ("KPI-COMPLAINTS", "Complaints / 1k statements",
         f"{base_last['px_vals']['billing_complaints']:.1f}",
         f"{last['px_vals']['billing_complaints']:.1f}"),
        ("KPI-SELFPAYYIELD", "Self-pay yield",
         f"{(1 - base_last['bad_debt']/base_last['patient_resp'])*100:.0f}%",
         f"{(1 - last['bad_debt']/last['patient_resp'])*100:.0f}%"),
    ]
    return rows


def write_report(cfg, scenario, base, scen, out_path=None, gross=None):
    is_scn = scenario is not None
    last, base_last = scen[-1], base[-1]
    wacc = cfg["organization"]["wacc"]
    years = cfg["reporting"]["npv_years"]
    L = []
    title = scenario["scenario"]["name"] if is_scn else "Baseline (no interventions)"
    L.append(f"# Digital twin run — {title}\n")
    L.append(f"*Model: `{cfg['meta']['id']}` v{cfg['meta']['version']} ({cfg['meta']['as_of']}) — "
             f"{cfg['meta']['name']}. Horizon {cfg['meta']['horizon_months']} months. "
             f"Generated by `twin.py`; do not hand-edit.*\n")
    if is_scn:
        L.append(f"> {scenario['scenario'].get('description','').strip()}\n")
        L.append("## Interventions\n")
        L.append("| ID | Type | Binds | Start | Ramp | One-time | Run-rate/yr |")
        L.append("|---|---|---|---|---|---|---|")
        for iv in scenario.get("interventions", []):
            binds = ", ".join(iv.get("use_cases", [])) or iv.get("type", "")
            c = iv.get("costs", {})
            L.append(f"| {iv['id']} | {iv.get('type','')} | {binds} | M{iv['start_month']} | "
                     f"{iv['ramp_months']}mo | {money(c.get('one_time',0))} | {money(c.get('run_rate_annual',0))} |")
        L.append("")

    # Financial impact
    L.append("## Financial impact\n")
    if is_scn:
        L.append("| Measure | Year 1 | Year 2 | Year 3 | Steady-state /yr |")
        L.append("|---|---|---|---|---|")
        rows = [
            ("Net revenue captured", "revenue"),
            ("Denial write-offs", "denial_writeoff"),
            ("Bad debt", "bad_debt"),
            ("Underpayment leakage", "underpayment_leak"),
            ("Charge capture leakage", "charge_leak"),
            ("Labor cost (incl. OT)", None),
            ("Total operating cost", "total_cost"),
            ("Cash collected", "cash"),
        ]
        for label, key in rows:
            cells = []
            for y in (1, 2, 3):
                bs, ss = annualize(base, y), annualize(scen, y)
                if key is None:
                    d = (_sum(ss, "labor_cost") + _sum(ss, "ot_cost")) - \
                        (_sum(bs, "labor_cost") + _sum(bs, "ot_cost"))
                else:
                    d = _sum(ss, key) - _sum(bs, key)
                cells.append(delta_money(d))
            if key is None:
                steady = ((last["labor_cost"] + last["ot_cost"]) -
                          (base_last["labor_cost"] + base_last["ot_cost"])) * 12
            else:
                steady = (last[key] - base_last[key]) * 12
            L.append(f"| {label} | " + " | ".join(cells) + f" | {delta_money(steady)} |")
        v = npv(base, scen, wacc, years)
        ar_release = -(last["ar_balance"] - base_last["ar_balance"])
        L.append("")
        L.append(f"- **{years}-year NPV of the program (revenue + cost + cash-timing, "
                 f"discounted at {wacc*100:.1f}%): {delta_money(v)}**")
        L.append(f"- One-time cash from AR-days change: {delta_money(ar_release)} "
                 f"(AR days {base_last['ar_days']:.1f} → {last['ar_days']:.1f})")
        onetime = sum(r["one_time_cost"] for r in scen)
        runrate = last["scenario_run_cost"] * 12
        L.append(f"- Program spend: {money(onetime)} one-time + {money(runrate)}/yr run-rate at maturity\n")
        L.extend(payer_section(cfg, base, scen, gross, wacc, years))
    else:
        y1 = annualize(scen, 1)
        L.append(f"- Net revenue captured: {money(_sum(y1,'revenue'))}/yr on expected net {money(_sum(y1,'expected_net'))}")
        L.append(f"- Leakage: denials {money(_sum(y1,'denial_writeoff'))}, bad debt {money(_sum(y1,'bad_debt'))}, "
                 f"underpayment {money(_sum(y1,'underpayment_leak'))}, charge capture {money(_sum(y1,'charge_leak'))}")
        L.append(f"- Operating cost: {money(_sum(y1,'total_cost'))}/yr "
                 f"({_sum(y1,'total_cost')/_sum(y1,'cash')*100:.2f}% cost to collect)")
        L.append(f"- Net AR days: {last['ar_days']:.1f} | workforce: {last['fte_total']:,.0f} FTE\n")

    # KPI table
    L.append("## KPI movement (ontology bindings)\n")
    L.append("| KPI | Definition | Baseline | " + ("Scenario end-state |" if is_scn else "End-state |"))
    L.append("|---|---|---|---|")
    for kid, name, b, s in kpi_table(cfg, last, base_last):
        L.append(f"| `{kid}` | {name} | {b} | {s} |")
    L.append("")

    # Productivity
    L.append("## Productivity & workforce\n")
    L.append("| Pool (ROLE-*) | FTE base→end | Utilization | Backlog days | Touches/FTE/mo | Automated share |")
    L.append("|---|---|---|---|---|---|")
    for k, pr in last["pools"].items():
        roles = ", ".join(cfg["staffing"]["pools"][k]["roles"])
        base_pr = base_last["pools"][k]
        st_touch = sum(s["touches"] for s in last["stages"].values() if s["pool"] == k)
        st_auto = sum(s["auto"] for s in last["stages"].values() if s["pool"] == k)
        tpf = (st_touch - st_auto) / pr["fte"] if pr["fte"] else 0.0
        auto_share = st_auto / st_touch if st_touch else 0.0
        L.append(f"| {k} ({roles}) | {base_pr['fte']:.0f}→{pr['fte']:.0f} | {pr['util']*100:.0f}% | "
                 f"{pr['backlog_days']:.1f} | {tpf:,.0f} | {auto_share*100:.0f}% |")
    auto_delta = (last["auto_touches"] / last["total_touches"] -
                  base_last["auto_touches"] / base_last["total_touches"]) if is_scn else \
        last["auto_touches"] / last["total_touches"]
    L.append("")
    L.append(f"- Manual touches: {base_last['total_touches']-base_last['auto_touches']:,.0f}/mo baseline → "
             f"{last['total_touches']-last['auto_touches']:,.0f}/mo "
             f"({'+' if auto_delta>=0 else ''}{auto_delta*100:.1f} pt automated share)"
             if is_scn else
             f"- Manual touches {last['total_touches']-last['auto_touches']:,.0f}/mo; "
             f"automated share {auto_delta*100:.1f}%")
    L.append(f"- Denied claims worked: {base_last['denied_claims']:,.0f}/mo → {last['denied_claims']:,.0f}/mo; "
             f"appeals {base_last['appealed_claims']:,.0f} → {last['appealed_claims']:,.0f}/mo"
             if is_scn else
             f"- Denied claims worked {last['denied_claims']:,.0f}/mo; appeals {last['appealed_claims']:,.0f}/mo")
    L.append(f"- Total workforce: {base_last['fte_total']:,.0f} → {last['fte_total']:,.0f} FTE\n"
             if is_scn else f"- Total workforce {last['fte_total']:,.0f} FTE\n")

    # Experience
    L.append("## Experience impact\n")
    L.append(f"**Patient financial experience index (PXI): {base_last['pxi']:.1f} → {last['pxi']:.1f}**"
             if is_scn else f"**Patient financial experience index (PXI): {last['pxi']:.1f}/100**")
    L.append("")
    L.append("| Component (KPI binding) | Baseline | End-state |")
    L.append("|---|---|---|")
    fmt = {"auth_wait_days": "{:.1f} d", "billing_complaints": "{:.1f}/1k",
           "surprise_bills": "{:.1f}/1k"}
    for name in last["px_vals"]:
        f = fmt.get(name, "{:.0%}")
        L.append(f"| {name} | {f.format(base_last['px_vals'][name])} | {f.format(last['px_vals'][name])} |")
    L.append("")
    L.append(f"**Caregiver experience index (CXI): {base_last['cxi']:.1f} → {last['cxi']:.1f}**"
             if is_scn else f"**Caregiver experience index (CXI): {last['cxi']:.1f}/100**")
    L.append("")
    L.append("| Component | Baseline | End-state |")
    L.append("|---|---|---|")
    cfmt = {"backlog_pressure": "{:.1f} d", "change_load": "{:.0f} ramping",
            "provider_burden": "{:.2f}×", "workload_balance": "{:.0%}",
            "rework_share": "{:.0%}", "automation_relief": "{:.0%}"}
    for name in last["cx_vals"]:
        f = cfmt.get(name, "{:.2f}")
        L.append(f"| {name} | {f.format(base_last['cx_vals'][name])} | {f.format(last['cx_vals'][name])} |")
    L.append("")

    text = "\n".join(L)
    if out_path:
        Path(out_path).write_text(text)
    return text


def write_csv(months, path):
    keys = ["month", "expected_net", "revenue", "cash", "ar_days", "bill_lag_days",
            "idr", "denial_writeoff", "bad_debt", "underpayment_leak", "charge_leak",
            "labor_cost", "ot_cost", "total_cost", "one_time_cost", "scenario_run_cost",
            "pxi", "cxi", "fte_total", "total_touches", "auto_touches",
            "denied_claims", "appealed_claims", "payer_pressure"]
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(keys)
        for r in months:
            w.writerow([f"{r[k]:.4f}" if isinstance(r[k], float) else r[k] for k in keys])


def write_json(cfg, scenario, base, scen, path):
    out = {
        "model": cfg["meta"]["id"], "version": cfg["meta"]["version"],
        "scenario": scenario["scenario"]["id"] if scenario else None,
        "months": [{k: v for k, v in r.items()
                    if k not in ("pools", "stages", "px_vals", "cx_vals", "payer")}
                   for r in scen],
        "end_state": {"pools": scen[-1]["pools"], "px": scen[-1]["px_vals"],
                      "cx": scen[-1]["cx_vals"], "payer_rules": scen[-1]["payer"]},
        "baseline_end": {"ar_days": base[-1]["ar_days"], "pxi": base[-1]["pxi"],
                         "cxi": base[-1]["cxi"]},
    }
    Path(path).write_text(json.dumps(out, indent=1))


def compare_report(cfg, runs, out_path):
    base = runs[0][2]
    wacc = cfg["organization"]["wacc"]
    years = cfg["reporting"]["npv_years"]
    L = ["# Digital twin — scenario comparison\n",
         f"*Model `{cfg['meta']['id']}` v{cfg['meta']['version']}; {years}-yr NPV at "
         f"{wacc*100:.1f}% WACC. Figures are NET of payer response dynamics; the erosion "
         f"column is gross-NPV minus net-NPV. Generated by `twin.py`.*\n",
         "| Scenario | Net rev Δ/yr (steady) | Op cost Δ/yr | AR days | NPV | Payer erosion | PXI | CXI |",
         "|---|---|---|---|---|---|---|---|"]
    b_last = base[-1]
    L.append(f"| Baseline | — | — | {b_last['ar_days']:.1f} | — | — | "
             f"{b_last['pxi']:.1f} | {b_last['cxi']:.1f} |")
    for scenario, _, scen, gross in runs[1:]:
        last = scen[-1]
        rev = (last["revenue"] - b_last["revenue"]) * 12
        cost = (last["total_cost"] - last["one_time_cost"]
                - (b_last["total_cost"] - b_last["one_time_cost"])) * 12
        v = npv(base, scen, wacc, years)
        if gross is not None and any(r["payer_pressure"] > 0 for r in scen):
            erosion = delta_money(v - npv(base, gross, wacc, years))
        else:
            erosion = "none"
        L.append(f"| {scenario['scenario']['name']} | {delta_money(rev)} | {delta_money(cost)} | "
                 f"{last['ar_days']:.1f} | {delta_money(v)} | {erosion} | "
                 f"{last['pxi']:.1f} | {last['cxi']:.1f} |")
    text = "\n".join(L) + "\n"
    if out_path:
        Path(out_path).write_text(text)
    return text


# ----------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Revenue cycle digital twin simulator")
    ap.add_argument("--config", default=str(HERE / "twin-config.yaml"))
    ap.add_argument("--scenario", help="scenario YAML to simulate against baseline")
    ap.add_argument("--compare", nargs="+", help="multiple scenario YAMLs; comparison table")
    ap.add_argument("-o", "--out", help="write markdown report here")
    ap.add_argument("--csv", help="write monthly time series CSV here")
    ap.add_argument("--json", help="write JSON dump here")
    ap.add_argument("--diag", action="store_true", help="print baseline pool utilization diagnostics")
    ap.add_argument("--no-payer-dynamics", action="store_true",
                    help="disable endogenous payer response (report gross program value)")
    args = ap.parse_args()

    cfg, warns = load_config(args.config)
    for w in warns:
        print(f"WARNING: {w}", file=sys.stderr)

    base = simulate(cfg)

    if args.diag:
        last = base[-1]
        print(f"{'pool':<18}{'fte':>7}{'util':>7}{'backlog_d':>10}")
        for k, pr in last["pools"].items():
            print(f"{k:<18}{pr['fte']:>7.0f}{pr['util']*100:>6.0f}%{pr['backlog_days']:>10.1f}")
        print(f"\nAR days {last['ar_days']:.1f} | bill lag {last['bill_lag_days']:.1f} | "
              f"IDR {last['idr']*100:.1f}% | PXI {last['pxi']:.1f} | CXI {last['cxi']:.1f}")
        y1 = annualize(base, 1)
        print(f"revenue {money(_sum(y1,'revenue'))}/yr | cost {money(_sum(y1,'total_cost'))} | "
              f"CTC {_sum(y1,'total_cost')/_sum(y1,'cash')*100:.2f}%")
        return

    payer_on = not args.no_payer_dynamics and bool(
        (cfg.get("payer_dynamics") or {}).get("enabled"))

    if args.compare:
        runs = [(None, None, base)]
        for spath in args.compare:
            scn, swarns = load_scenario(spath, cfg)
            for w in swarns:
                print(f"WARNING [{spath}]: {w}", file=sys.stderr)
            net = simulate(cfg, scn, payer=payer_on)
            gross = simulate(cfg, scn, payer=False) if payer_on else None
            runs.append((scn, spath, net, gross))
        print(compare_report(cfg, runs, args.out))
        return

    scenario, gross = None, None
    if args.scenario:
        scenario, swarns = load_scenario(args.scenario, cfg)
        for w in swarns:
            print(f"WARNING: {w}", file=sys.stderr)
        scen = simulate(cfg, scenario, payer=payer_on)
        if payer_on:
            gross = simulate(cfg, scenario, payer=False)
    else:
        scen = base

    report = write_report(cfg, scenario, base, scen, args.out, gross=gross)
    if not args.out:
        print(report)
    else:
        print(f"report written to {args.out}")
    if args.csv:
        write_csv(scen, args.csv)
    if args.json:
        write_json(cfg, scenario, base, scen, args.json)


if __name__ == "__main__":
    main()
