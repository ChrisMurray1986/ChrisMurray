# Investment packet — Example Regional Health (fictional)

Assessment dated 2026-07-03; generated from committed inputs (never hand-edit this packet — edit the inputs and regenerate).

## Headline

| | |
|---|---|
| Dispositions | GO 0 / COND 42 / DEFER 57 / KILL 0 |
| A0/A1 launchable now | 41 |
| Steady-state value (base, capped) | $42.2M/yr |
| Year-1 value (disposition-adjusted) | $6.0M |
| One-time cash release | $15.9M |
| Total run cost | $11.4M/yr |
| 3-yr portfolio TCO | $51.3M |
| Steady-state net (value − run) | **$30.9M/yr** |

## Top gates by locked value

| Gate | UCs held | Locked $/yr |
|---|---|---|
| governance 1->2 | 64 | $26.7M |
| workflow 2->3 | 49 | $21.5M |
| data 3->4 | 30 | $16.2M |
| governance 1->3 | 34 | $15.3M |
| legal 1->2 | 32 | $11.2M |

## Top use cases by steady-state net value

| UC | Option | Net/yr | Payback | Disposition |
|---|---|---|---|---|
| UC-03-01 | build_ml | $2.3M | 2 mo | CONDITIONAL |
| UC-07-05 | build_rules | $1.9M | 1 mo | CONDITIONAL |
| UC-01-05 | vendor | $1.6M | 1 mo | DEFER |
| UC-09-03 | build_ml | $1.5M | 2 mo | CONDITIONAL |
| UC-03-06 | api | $1.3M | 2 mo | DEFER |

**Net-negative use cases (kill/descope review, Play 7):** UC-05-07, UC-03-02, UC-01-01, UC-01-11*, UC-05-05, UC-01-02, UC-02-05, UC-07-04, UC-12-02*, UC-13-02, UC-14-05, UC-14-04, UC-12-03*, UC-13-04*, UC-01-17, UC-12-01*, UC-12-06*, UC-13-03, UC-10-06*, UC-12-04*, UC-03-08

\* risk-EV-justified: segregated VS-8 expected value covers the cash shortfall — judge on risk grounds, not as an automatic descope.

**SLM verdicts:** doc_extraction: api, gen_drafting: api, clinical_nlp: api

## Council agenda (Play 2)

1. True-up — realized vs estimated; benefit-owner signatures; driver recalibrations
2. Readiness velocity — assessment diff vs prior quarter
3. Remediation funding — work the locked-value table above
4. Launch decisions — GO/CONDITIONAL ranked by net value × payback (portfolio.csv)
5. Autonomy promotions — evidence per candidate; update hitl_share on promotion
6. Kills & descopes — net-negative list above; crossed crossovers; KILL re-looks
7. Log decisions — owner, budget, expected value, proving metric

## Contents

- `feasibility.md` / `.html` — dispositions, gaps, remediation leverage
- `value.md` / `.html` — value streams, pools, locked-value detail
- `cost.md` / `.html` — sourcing decisions, TCO, ROI, SLM break-even
- `portfolio.csv` — one row per use case across all three models
- `packet.json` — headline numbers (machine-readable, for next quarter's deltas)
