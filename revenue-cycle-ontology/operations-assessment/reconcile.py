#!/usr/bin/env python3
"""Validate the assessment ontology's bindings and reconcile field scores with
the AI facet assessment.

Validation mode (always runs):
  - extracts every binding from OFM/PFM/RFM text: FM-* defects, UC-* hardenings,
    facet mentions, and structural references (sub-process/action/decision IDs)
  - resolves them against the authoritative registries (FM registry in the master
    ontology, gate-vectors facet catalog and use-case list, and the master
    ontology's actual section/action/decision structure)
  - reports dangling references, plus coverage gaps (FMs no PFM produces,
    UCs never referenced as hardened-by, facets no finding explains)
  - emits couplings.yaml: the machine-readable binding graph (ENG-01)

Reconciliation mode (--scores + --facets):
  - joins scored field findings with the facet assessment
  - checks the README contract both ways: facets scored 0/1 with no linked
    finding (unexplained gaps) and flagged findings that degrade no facet
    (unmotivated findings)
  - emits the operational improvement plan (ENG-07): every flagged finding
    with its paired best-practice prescription, typed by fix layer
    (structure/incentives, standard work/tooling, coaching/competency) —
    a co-equal output to the AI portfolio, priced standalone when --profile
    is given, with AI-gate unlock listed as the secondary benefit

Usage:
  python3 reconcile.py
  python3 reconcile.py --scores <scores.yaml> --facets <assessment.yaml> \
                       [--profile <org-profile.yaml>] [-o report.md]

Hardening features (18-full-assessment-simulation.md): facet causality classes
(ENG-01), degrades couplings for all layers (ENG-02), FM->pool pricing with
--profile (ENG-03), explicit chain grouping via `chain:` in score entries
(ENG-04), opportunity-anchor awareness (ENG-05), and source-version refusal
(ENG-06; override with --allow-version-mismatch).
"""

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required: pip install pyyaml")

HERE = Path(__file__).parent
ROOT = HERE.parent
SCORING = ROOT / "ai-automation" / "scoring"
PROFILE = None

import build_field_instrument as bfi  # noqa: E402  (sibling module)

DOMAIN_FILES = ["01-patient-access.md", "02-mid-cycle.md", "03-claims.md", "04-payments.md",
                "05-denials-ar.md", "06-patient-financial-services.md", "07-payer-contracting.md",
                "08-compliance-audit.md", "09-analytics-support.md"]

ENTERPRISE_FILES = ["01-operating-model.md", "02-process-improvement.md", "03-workforce.md",
                    "04-enabling-technology.md", "05-vendor-outsourcing.md",
                    "06-performance-governance.md"]

# The fix prescription differs by layer (README): assessments that prescribe
# only one layer relapse.
FIX_TYPES = {"enterprise": "structure & incentives (operating model)",
             "process": "standard work & tooling",
             "role": "coaching & competency"}


def master_structure():
    """Parse the master ontology into {section_id: {'A1','D2',...}} plus the set of ids."""
    sections = {}
    for fname in DOMAIN_FILES:
        text = (ROOT / fname).read_text()
        current = None
        for line in text.splitlines():
            h = re.match(r"#{2,3}\s+(\d{1,2}\.\d(?:\.\d)?)\s", line)
            if h:
                current = h.group(1)
                sections.setdefault(current, set())
                continue
            if current:
                b = re.match(r"-\s+\*\*([AD]\d+)[.\s]", line)
                if b:
                    sections[current].add(b.group(1))
    return sections


def registries():
    cc = (ROOT / "10-cross-cutting-entities.md").read_text()
    fms = set(re.findall(r"(?<![A-Z])FM-[A-Z][A-Z0-9]*(?:-[A-Z]+)?", cc))
    gv = yaml.safe_load((SCORING / "gate-vectors.yaml").read_text())
    classes = {f: m.get("class", "failure-explained") for f, m in gv["facet_catalog"].items()}
    anchors = {u: m.get("anchor", "failure") for u, m in gv["use_cases"].items()}
    return fms, set(gv["facet_catalog"]), set(gv["use_cases"]), classes, anchors


def extract_bindings(items, fms, facets, ucs, sections):
    couplings, problems = {}, []
    facet_pat = re.compile("|".join(sorted((re.escape(f) for f in facets), key=len, reverse=True)))
    for it in items:
        text = " ".join([it["prompt"], it.get("signals", ""), it.get("practice", "")])
        b = {"produces": sorted(set(re.findall(r"(?<![A-Z])FM-[A-Z][A-Z0-9]*(?:-[A-Z]+)?", text)) & fms),
             "hardened_by": sorted(set(re.findall(r"UC-\d\d-\d\d", text)) & ucs),
             "facets": sorted(set(facet_pat.findall(text))
                              | {d for d in it.get("degrades", []) if d in facets}),
             "degrades_dims": sorted(d[4:] for d in it.get("degrades", []) if d.startswith("dim:")),
             "refs": sorted(set(re.findall(r"\d{1,2}\.\d(?:\.\d)?(?:\.[AD]\d+)?", text)))}
        for fm in set(re.findall(r"(?<![A-Z])FM-[A-Z][A-Z0-9]*(?:-[A-Z]+)?", text)) - fms:
            if not fm.startswith(("FM-AI",)):
                problems.append(f"{it['id']}: unknown defect id {fm}")
        for uc in set(re.findall(r"UC-\d\d-\d\d", text)) - ucs:
            problems.append(f"{it['id']}: unknown use case {uc}")
        for ref in b["refs"]:
            parts = ref.split(".")
            if parts[-1][:1] in "AD":
                sec, tok = ".".join(parts[:-1]), parts[-1]
                if sec not in sections:
                    problems.append(f"{it['id']}: reference {ref} — section {sec} not found in master ontology")
                elif tok not in sections[sec]:
                    problems.append(f"{it['id']}: reference {ref} — {tok} not found under {sec}")
            elif len(parts) >= 2 and ref not in sections and not any(
                    s.startswith(ref) for s in sections):
                problems.append(f"{it['id']}: reference {ref} — no such section in master ontology")
        couplings[it["id"]] = {k: v for k, v in b.items() if v}
        couplings[it["id"]]["layer"] = it["layer"]
        couplings[it["id"]]["group"] = it["group"]
    return couplings, problems


def coverage(couplings, fms, facets, ucs):
    produced = {fm for c in couplings.values() for fm in c.get("produces", [])}
    hardened = {uc for c in couplings.values() for uc in c.get("hardened_by", [])}
    mentioned = {f for c in couplings.values() for f in c.get("facets", [])}
    return {"fms_unproduced": sorted(fms - produced),
            "ucs_unreferenced": sorted(ucs - hardened),
            "facets_unmentioned": sorted(facets - mentioned)}


def price_findings(couplings, flagged, chains):
    """ENG-03: finding $ = sizes of the pools its produced FMs feed (overlapping)."""
    import value as vm
    vd = yaml.safe_load((SCORING / "value-drivers.yaml").read_text())
    fm_pools = vd.get("fm_pools", {})
    profile = yaml.safe_load(Path(PROFILE).read_text())
    amounts, day_rec, _ = vm.size_pools(profile, vd["pools"])
    def item_price(iid):
        pools = {fm_pools[fm] for fm in couplings.get(iid, {}).get("produces", []) if fm in fm_pools}
        return sum(amounts.get(p, 0.0) for p in pools), sorted(pools)
    priced = {i: item_price(i) for i in flagged}
    chain_priced = []
    for members in chains:
        pools = set()
        for i in members:
            pools |= {fm_pools[fm] for fm in couplings.get(i, {}).get("produces", []) if fm in fm_pools}
        chain_priced.append((sorted(members), sum(amounts.get(p, 0.0) for p in pools), sorted(pools)))
    return priced, chain_priced


def bp_titles():
    """OFM -> paired BP prescription: 1:1 numbered pairing per enterprise domain file."""
    titles = {}
    for fname in ENTERPRISE_FILES:
        text = (HERE / fname).read_text()
        for m in re.finditer(r"^### (BP-[A-Z]+-\d\d) — (.+)$", text, re.M):
            titles[m.group(1)] = m.group(2).strip()
    return titles


def improvement_plan(items_by_id, flagged, couplings, priced=None):
    """ENG-07: the operational improvement plan — the co-equal output track.

    Every flagged finding gets its paired best-practice prescription, typed by
    fix layer. The $ at stake is standalone (the pools leak whether the cure is
    procedural or automated); AI-gate unlock is the secondary benefit column.
    """
    bps = bp_titles()
    L = ["\n## Operational improvement plan (ENG-07 — co-equal output)\n",
         "Process and operating-model fixes prescribed by the paired best practices. These stand",
         "on their own: the dollars at stake leak through the FM→pool bindings whether or not any",
         "automation is ever funded, and most weak AI facets have a finding below as their root",
         "cause — so this plan is funded alongside, usually ahead of, the AI portfolio. The last",
         "column is the *secondary* benefit, not the justification.\n",
         "| Finding | Score | Fix layer | Prescription (paired practice) | $ at stake/yr | AI gates also unlocked |",
         "|---|---|---|---|---|---|"]

    def row_key(iid):
        val = priced.get(iid, (0.0, []))[0] if priced else 0.0
        return (-flagged[iid].get("score", 0), -val, iid)

    for iid in sorted(flagged, key=row_key):
        it = items_by_id.get(iid)
        if not it:
            continue
        if it["layer"] == "enterprise":
            bpid = "BP-" + iid[len("OFM-"):]
            presc = f"**{bpid}** {bps.get(bpid, '')}".strip()
        else:
            first = (it.get("practice") or "").split(". ")[0].strip()
            presc = (first[:110] + "…") if len(first) > 110 else (first or "see paired practice")
        dollars = "—"
        if priced and priced.get(iid, (0.0,))[0] > 0:
            dollars = f"${priced[iid][0]/1e6:.1f}M"
        gates = ", ".join(couplings.get(iid, {}).get("facets", [])[:4]) or "—"
        L.append(f"| {iid} | {flagged[iid].get('score')} | {FIX_TYPES[it['layer']]} "
                 f"| {presc} | {dollars} | {gates} |")

    n_by_layer = defaultdict(int)
    for iid in flagged:
        if iid in items_by_id:
            n_by_layer[items_by_id[iid]["layer"]] += 1
    L.append(f"\nFindings by fix layer: enterprise {n_by_layer['enterprise']} · "
             f"process {n_by_layer['process']} · role {n_by_layer['role']}. "
             "A complete prescription usually needs all three layers — structure/incentive fixes "
             "(OFM), standard work (PFM), and coaching (RFM) — before or alongside automation; "
             "prescribing only one layer relapses (README).")
    return L


def build_chains(scores, flagged):
    """ENG-04: union explicit chain: links into problem chains."""
    parent = {i: i for i in flagged}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a, b):
        if a in parent and b in parent:
            parent[find(a)] = find(b)
    for iid in flagged:
        for other in (scores[iid].get("chain") or []):
            union(iid, other)
    groups = {}
    for i in flagged:
        groups.setdefault(find(i), []).append(i)
    return sorted(groups.values(), key=len, reverse=True)


def load_scores(path):
    doc = yaml.safe_load(Path(path).read_text())
    out = {}
    for layer in doc.values():
        if not isinstance(layer, dict):
            continue
        for group in layer.values():
            if not isinstance(group, dict):
                continue
            for iid, e in group.items():
                if isinstance(e, dict) and "score" in e:
                    out[iid] = e
    return out


def reconcile(couplings, scores, facet_scores, facets, classes):
    flagged = {i: s for i, s in scores.items() if s.get("score", 0) > 0}
    weak_all = {f for f in facets if facet_scores.get(f, 0) in (0, 1)}
    weak_facets = {f for f in weak_all if classes.get(f) == "failure-explained"}
    weak_other = {f: classes[f] for f in weak_all - weak_facets}
    facet_to_findings = defaultdict(list)
    for iid in flagged:
        for f in couplings.get(iid, {}).get("facets", []):
            facet_to_findings[f].append(iid)
    explained = {f: v for f, v in facet_to_findings.items() if f in weak_facets}
    unexplained = sorted(weak_facets - set(facet_to_findings))
    unmotivated = sorted(i for i in flagged
                         if not couplings.get(i, {}).get("facets")
                         and not couplings.get(i, {}).get("produces")
                         and not couplings.get(i, {}).get("degrades_dims"))
    return {"n_flagged": len(flagged), "n_weak_facets": len(weak_facets),
            "n_weak_exempt": len(weak_other),
            "weak_exempt": weak_other,
            "explained": {f: v for f, v in sorted(explained.items())},
            "unexplained_weak_facets": unexplained,
            "findings_without_bindings": unmotivated, "flagged": flagged}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--scores", help="scored field-instrument YAML")
    ap.add_argument("--facets", help="AI facet assessment YAML (score.py format)")
    ap.add_argument("--profile", help="org financial profile YAML — prices findings via FM->pool (ENG-03)")
    ap.add_argument("--allow-version-mismatch", action="store_true")
    ap.add_argument("-o", "--output", help="write markdown report")
    args = ap.parse_args()

    items = bfi.parse_ofm() + bfi.parse_pfm() + bfi.parse_rfm()
    fms, facets, ucs, classes, anchors = registries()
    sections = master_structure()
    couplings, problems = extract_bindings(items, fms, facets, ucs, sections)
    cov = coverage(couplings, fms, facets, ucs)

    (HERE / "couplings.yaml").write_text(yaml.safe_dump(
        {"generated_by": "reconcile.py — machine-readable binding graph (ENG-01)",
         "items": couplings}, sort_keys=True, allow_unicode=True, width=110))

    L = ["# Binding validation & reconciliation report", ""]
    L.append(f"Items: {len(items)} | dangling references: {len(problems)} | "
             f"FMs never produced by a PFM: {len(cov['fms_unproduced'])} | "
             f"UCs never referenced as hardened-by: {len(cov['ucs_unreferenced'])} | "
             f"facets never mentioned by any finding: {len(cov['facets_unmentioned'])}\n")
    if problems:
        L.append("## Dangling references\n")
        L += [f"- {p}" for p in problems]
    L.append("\n## Coverage gaps\n")
    L.append(f"- **FMs unproduced:** {', '.join(cov['fms_unproduced']) or 'none'}")
    unref_fail = [u for u in cov["ucs_unreferenced"] if anchors.get(u) == "failure"]
    unref_opp = [u for u in cov["ucs_unreferenced"] if anchors.get(u) == "opportunity"]
    L.append(f"- **UCs unreferenced, failure-anchored (real gaps):** {', '.join(unref_fail) or 'none'}")
    L.append(f"- **UCs opportunity-anchored (by design, ENG-05):** {', '.join(unref_opp) or 'none'}")
    L.append(f"- **Facets unmentioned (reconciliation blind spots):** "
             f"{', '.join(cov['facets_unmentioned']) or 'none'}")

    if args.scores and args.facets:
        doc = yaml.safe_load(Path(args.scores).read_text())
        sv = doc.get("source_version")
        cur = bfi.source_version()
        if sv and sv != cur and not args.allow_version_mismatch:
            sys.exit(f"score file source_version {sv} != current {cur} — "
                     f"item sets may differ (ENG-06). Re-score or pass --allow-version-mismatch.")
        scores = load_scores(args.scores)
        fa = yaml.safe_load(Path(args.facets).read_text())
        rec = reconcile(couplings, scores, fa.get("facets", {}), facets, classes)
        chains = build_chains(scores, rec["flagged"])
        multi = [c for c in chains if len(c) > 1]
        L.append("\n## Reconciliation with the facet assessment\n")
        L.append(f"- Score-file source version: {sv or 'unstamped'} (current {cur})")
        L.append(f"- Flagged findings: {rec['n_flagged']} → **{len(chains)} problem chains** "
                 f"({len(multi)} multi-layer, ENG-04)")
        L.append(f"- Weak facets in scope (class failure-explained): {rec['n_weak_facets']} | "
                 f"exempt by causality class (new-capability/contractual, ENG-01): {rec['n_weak_exempt']}")
        L.append(f"- In-scope weak facets **explained** by ≥1 flagged finding: {len(rec['explained'])}")
        L.append(f"- Weak facets **unexplained** (contract violation — no linked finding): "
                 f"{len(rec['unexplained_weak_facets'])}")
        if rec["unexplained_weak_facets"]:
            L.append(f"  - {', '.join(rec['unexplained_weak_facets'])}")
        L.append(f"- Flagged findings with **no machine-readable binding at all**: "
                 f"{len(rec['findings_without_bindings'])}")
        if rec["findings_without_bindings"]:
            L.append(f"  - {', '.join(rec['findings_without_bindings'][:30])}"
                     + (" …" if len(rec["findings_without_bindings"]) > 30 else ""))
        priced = None
        if args.profile:
            global PROFILE
            PROFILE = args.profile
            sys.path.insert(0, str(SCORING))
            priced, chain_priced = price_findings(couplings, rec["flagged"], chains)
            top = sorted(((v, p, i) for i, (v, p) in priced.items() if v > 0), reverse=True)[:10]
            L.append("\n### Findings priced via FM→pool (ENG-03; overlapping attribution)\n")
            L.append("| Finding | Pools at stake | $ at stake/yr |")
            L.append("|---|---|---|")
            for v, p, i in top:
                L.append(f"| {i} | {', '.join(p)} | ${v/1e6:.1f}M |")
            cp = sorted((c for c in chain_priced if len(c[0]) > 1), key=lambda x: -x[1])[:5]
            if cp:
                L.append("\n**Top multi-layer chains:** " + "; ".join(
                    f"{{{', '.join(m)}}} → ${v/1e6:.1f}M ({', '.join(p)})" for m, v, p in cp))

        L += improvement_plan({it["id"]: it for it in items}, rec["flagged"], couplings, priced)

    report = "\n".join(L) + "\n"
    if args.output:
        Path(args.output).write_text(report)
        print(f"report written to {args.output}; couplings.yaml emitted "
              f"({len(couplings)} items)")
    else:
        print(report)


if __name__ == "__main__":
    main()
