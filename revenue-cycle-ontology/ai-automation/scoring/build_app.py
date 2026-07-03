#!/usr/bin/env python3
"""Build the self-contained HTML investment planner (rcm-investment-app.html).

Embeds the driver YAMLs (gate-vectors, value-drivers, cost-drivers) plus the
example assessment/profile into app-template.html so the app runs entirely in
the browser with the YAML files remaining the single source of truth.

Usage: python3 build_app.py [-o rcm-investment-app.html]
"""

import argparse
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required: pip install pyyaml")

from score import DOMAIN_NAMES

HERE = Path(__file__).parent


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("-o", "--output", default=str(HERE / "rcm-investment-app.html"))
    args = ap.parse_args()

    gv = yaml.safe_load((HERE / "gate-vectors.yaml").read_text())
    vd = yaml.safe_load((HERE / "value-drivers.yaml").read_text())
    cd = yaml.safe_load((HERE / "cost-drivers.yaml").read_text())
    profile = yaml.safe_load((HERE / "org-profile.template.yaml").read_text())
    example_assessment = yaml.safe_load((HERE / "example-assessment.yaml").read_text())
    example_profile = yaml.safe_load((HERE / "example-org-profile.yaml").read_text())

    mismatch = set(gv["use_cases"]) ^ set(vd["use_cases"]) | set(gv["use_cases"]) ^ set(cd["use_cases"])
    if mismatch:
        sys.exit(f"driver files disagree on use cases: {sorted(mismatch)}")

    drivers = {
        "facetCatalog": gv["facet_catalog"],
        "useCases": gv["use_cases"],
        "valuePools": vd["pools"],
        "valueUCs": vd["use_cases"],
        "costRates": cd["rates"],
        "workloads": cd["workloads"],
        "slmFamilies": cd["slm_families"],
        "platformAssets": cd["platform_assets"],
        "volumes": cd["volumes"],
        "costUCs": cd["use_cases"],
        "domains": DOMAIN_NAMES,
        "profileDefaults": {
            "rates": profile["rates"], "costs": profile["costs"],
            "labor_function_shares": profile["labor_function_shares"],
            "model": profile["model"],
        },
        "example": {
            "org": example_profile["org"],
            "financials": example_profile["financials"],
            "dimensions": example_assessment["dimensions"],
            "facets": example_assessment["facets"],
        },
    }

    template = (HERE / "app-template.html").read_text()
    html = template.replace("__DRIVERS__", json.dumps(drivers))
    Path(args.output).write_text(html)
    print(f"App written to {args.output} "
          f"({len(html)//1024} KiB, {len(gv['use_cases'])} use cases, "
          f"{len(gv['facet_catalog'])} facets embedded)")


if __name__ == "__main__":
    main()
