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

Usage:
  python3 reconcile.py
  python3 reconcile.py --scores <scores.yaml> --facets <assessment.yaml> [-o report.md]
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

import build_field_instrument as bfi  # noqa: E402  (sibling module)

DOMAIN_FILES = ["01-patient-access.md", "02-mid-cycle.md", "03-claims.md", "04-payments.md",
                "05-denials-ar.md", "06-patient-financial-services.md", "07-payer-contracting.md",
                "08-compliance-audit.md", "09-analytics-support.md"]


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
    return fms, set(gv["facet_catalog"]), set(gv["use_cases"])


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


def reconcile(couplings, scores, facet_scores, facets):
    flagged = {i: s for i, s in scores.items() if s.get("score", 0) > 0}
    weak_facets = {f for f in facets if facet_scores.get(f, 0) in (0, 1)}
    facet_to_findings = defaultdict(list)
    for iid in flagged:
        for f in couplings.get(iid, {}).get("facets", []):
            facet_to_findings[f].append(iid)
    explained = {f: v for f, v in facet_to_findings.items() if f in weak_facets}
    unexplained = sorted(weak_facets - set(facet_to_findings))
    unmotivated = sorted(i for i in flagged
                         if not couplings.get(i, {}).get("facets")
                         and not couplings.get(i, {}).get("produces"))
    return {"n_flagged": len(flagged), "n_weak_facets": len(weak_facets),
            "explained": {f: v for f, v in sorted(explained.items())},
            "unexplained_weak_facets": unexplained,
            "findings_without_bindings": unmotivated}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--scores", help="scored field-instrument YAML")
    ap.add_argument("--facets", help="AI facet assessment YAML (score.py format)")
    ap.add_argument("-o", "--output", help="write markdown report")
    args = ap.parse_args()

    items = bfi.parse_ofm() + bfi.parse_pfm() + bfi.parse_rfm()
    fms, facets, ucs = registries()
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
    L.append(f"- **UCs unreferenced (no operational anchor):** "
             f"{', '.join(cov['ucs_unreferenced']) or 'none'}")
    L.append(f"- **Facets unmentioned (reconciliation blind spots):** "
             f"{', '.join(cov['facets_unmentioned']) or 'none'}")

    if args.scores and args.facets:
        scores = load_scores(args.scores)
        fa = yaml.safe_load(Path(args.facets).read_text())
        rec = reconcile(couplings, scores, fa.get("facets", {}), facets)
        L.append("\n## Reconciliation with the facet assessment\n")
        L.append(f"- Flagged findings: {rec['n_flagged']} | weak facets (0/1): {rec['n_weak_facets']}")
        L.append(f"- Weak facets **explained** by ≥1 flagged finding: {len(rec['explained'])}")
        L.append(f"- Weak facets **unexplained** (contract violation — no linked finding): "
                 f"{len(rec['unexplained_weak_facets'])}")
        if rec["unexplained_weak_facets"]:
            L.append(f"  - {', '.join(rec['unexplained_weak_facets'])}")
        L.append(f"- Flagged findings with **no machine-readable binding at all**: "
                 f"{len(rec['findings_without_bindings'])}")
        if rec["findings_without_bindings"]:
            L.append(f"  - {', '.join(rec['findings_without_bindings'][:30])}"
                     + (" …" if len(rec["findings_without_bindings"]) > 30 else ""))

    report = "\n".join(L) + "\n"
    if args.output:
        Path(args.output).write_text(report)
        print(f"report written to {args.output}; couplings.yaml emitted "
              f"({len(couplings)} items)")
    else:
        print(report)


if __name__ == "__main__":
    main()
