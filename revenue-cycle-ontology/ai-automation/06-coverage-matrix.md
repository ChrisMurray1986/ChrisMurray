# Coverage Matrix & Portfolio View

Proof of coverage: every failure mode in the base ontology (`../10-cross-cutting-entities.md`)
mapped to its preventing/detecting use cases, a KPI improvement index, and portfolio sequencing.

---

## FM-* → UC-* coverage (all 33 base failure modes countered)

| Failure mode | Prevented / detected by | Mechanism |
|---|---|---|
| FM-DUPMRN | UC-01-02, UC-01-01 | probabilistic identity resolution at create/search; confidence-gated order indexing |
| FM-PLANMAP | UC-01-03, UC-14-01, UC-01-16 | card-to-plan-code AI; master-table defect detection; entry-time validation |
| FM-ELIGLAPSE | UC-01-04 | orchestrated re-verification at every checkpoint incl. day-of-service |
| FM-COB | UC-01-06, UC-01-16, UC-06-08 | primacy inference; entry QA; secondary-claim balance validation |
| FM-NOAUTH | UC-01-07, UC-01-08, UC-01-09, UC-01-10, UC-11-03 | live auth grid; submission agent; tracking bots; auth-to-service reconciliation; policy-change feeds |
| FM-MEDNEC | UC-01-11, UC-06-01 | pre-service necessity screening with dx-gap assist; last-gate denial risk scoring |
| FM-NOTICEMISS | UC-01-16 | notice checklist verification before encounter close |
| FM-STATUSWRONG | UC-02-01, UC-02-02 | admission status prediction & criteria auto-abstraction |
| FM-CHGMISS | UC-03-01, UC-03-04, UC-03-06 | expected-vs-posted modeling; trigger surveillance; documentation-derived charging |
| FM-CHGDUP | UC-03-02 | real-time duplicate screening |
| FM-UNITERR | UC-03-03, UC-03-02 | NDC/unit conversion validation; units anomaly screens |
| FM-CDMSTALE | UC-03-05, UC-14-02 | code-release diffing; cross-system drift monitoring |
| FM-DOCGAP | UC-04-01, UC-04-02, UC-04-03 | query-opportunity prioritization; evidence surfacing; compliant query drafting |
| FM-CODEERR | UC-05-01, UC-05-02, UC-05-06, UC-12-03 | consistent autonomous coding; pre-bill DRG risk scoring; risk-weighted QA; pattern surveillance |
| FM-DISPO | UC-05-03, UC-05-02 | disposition cross-validation pre-bill |
| FM-CLAIMDROP | UC-06-04, UC-14-03 | submission integrity reconciliation; EDI pipeline observability |
| FM-REJECTUNWORKED | UC-06-05 | rejection auto-triage/repair with aging enforcement |
| FM-TFL | UC-06-06 | filing-clock sentinel across all queues |
| FM-MISPOST | UC-07-01, UC-07-03 | probabilistic matching; EOB IDP with balancing |
| FM-DENIALHIDDEN | UC-07-02 | CARC mapping intelligence + adjustment-pattern audit |
| FM-VARIANCEMISS | UC-07-05, UC-09-03 | 100% variance-check coverage; pattern clustering |
| FM-APPEALMISS | UC-08-01, UC-07-03 | deadline stamping at intake; letter-routing with deadlines |
| FM-REBILLLOOP | UC-08-04 | stuck-account pattern detection with forced review |
| FM-CREDITAGE | UC-09-04 | credit classification & staged refund automation |
| FM-PATIENTWRONGBILL | UC-10-01, UC-10-06 | statement-qualification hard gate; NSA protection classifier |
| FM-FA-MISS | UC-10-05, UC-09-06, UC-10-07 | presumptive FA scoring pre-placement; transfer-gate verification; placed-inventory recall |
| FM-ENROLLGAP | UC-11-04 | expirables lifecycle automation with claim hold/release |
| FM-TERMSUNLOADED | UC-11-01, UC-09-03 | independent extraction-vs-load verification; variance-cause clustering |
| FM-AMENDMISS | UC-11-02 | amendment watchdog with objection-window calendaring |
| FM-AUDITDEADLINE | UC-12-01 | audit intake classification with deadline workflow |
| FM-60DAY | UC-12-04, UC-09-04 | central overpayment register with clock automation |
| FM-EDISILENT | UC-14-03, UC-13-03 | transaction-flow anomaly detection; cash-forecast divergence alerting |
| FM-BOTSILENT | UC-14-04, GOV-05 | fleet observability with quarantine-and-return; mandatory hand-back |

Residual-risk note: coverage means *mitigated*, not eliminated. Each UC's guardrails and the
FM-AI-* table (`05-governance-assurance.md`) define the new risks introduced and their controls.

---

## KPI improvement index (primary movers)

| KPI | Primary use cases |
|---|---|
| KPI-PREREG-RATE / KPI-VERIF-RATE | UC-01-14, UC-01-04, UC-01-03 |
| KPI-AUTH-RATE | UC-01-07/08/09/10 |
| KPI-ESTIMATE-ACC | UC-01-12, UC-10-08 |
| KPI-POS-CASH | UC-01-15, UC-01-12, UC-01-14 |
| KPI-REGQA / KPI-CLEARANCE | UC-01-16, UC-01-13 |
| KPI-OBSRATE / KPI-AVOIDDAYS | UC-02-01/02/04/05 |
| KPI-CHGLAG / KPI-LATECHG / KPI-CAPTURE-ACC | UC-03-01/02/03/04/06/07 |
| KPI-QUERYRATE / KPI-CMI | UC-04-01/02/03/04 |
| KPI-CODEACC / KPI-DNFB / KPI-DNFC | UC-05-01…07 |
| KPI-CLEANCLAIM / KPI-FPY / KPI-CLAIMLAG / KPI-REJRATE | UC-06-01…08 |
| KPI-AUTOPOST / KPI-POSTLAG / KPI-SUSPENSE | UC-07-01/03/04 |
| KPI-IDR / KPI-OVERTURN / KPI-DENWO | UC-08-01…06, UC-06-01/03 |
| KPI-DAR / KPI-AR90 / KPI-CASHGOAL | UC-09-01/02, UC-08-04, UC-13-03 |
| KPI-UNDERPAY | UC-07-05, UC-09-03 |
| KPI-CREDITDAYS / KPI-60DAY | UC-09-04, UC-12-04 |
| KPI-SELFPAYYIELD / KPI-PLANDEFAULT / KPI-COMPLAINTS | UC-10-01…08, UC-01-05 |
| KPI-FA-TAT / KPI-AGENCYNETBACK | UC-10-05, UC-10-07 |
| KPI-CONTRACTYIELD | UC-11-01/02/05/06 |
| KPI-AUDITWIN | UC-12-01/02/06, UC-05-02 |
| KPI-NCR / KPI-CTC | entire portfolio (composite) |

---

## Portfolio sequencing (dependency-aware)

**Wave 0 — Foundations (everything depends on these)**
CAP-01 data foundation, CAP-02 label pipeline, CAP-05 orchestration/queue fabric, CAP-06
observability, UC-13-04 governance telemetry, UC-14-03/04 pipeline & fleet observability.

**Wave 1 — Deterministic protection (rules/RPA; fast, low-risk, immediate leakage stops)**
UC-01-04 eligibility orchestration, UC-06-04 submission integrity, UC-06-06 filing sentinel,
UC-03-03 drug units validator, UC-10-01 liability gate, UC-12-04 overpayment register,
UC-11-04 enrollment lifecycle, UC-09-02 status bots, UC-12-01 audit intake.

**Wave 2 — Prediction & prioritization (needs Wave 0 labels)**
UC-06-01 denial risk scoring, UC-08-01/02 denial classification & prioritization, UC-09-01 AR
prioritization, UC-04-01 CDI prioritization, UC-05-02 DRG risk, UC-02-01 status prediction,
UC-03-01 missing charge detection, UC-07-05 variance coverage, UC-10-05 FA scoring.

**Wave 3 — Generative & document AI (needs CAP-03/04/10 + GOV-03 verification)**
UC-07-03 EOB IDP, UC-01-01 order intake, UC-08-03 appeal generation, UC-04-03 query drafting,
UC-11-01 contract extraction, UC-11-03 policy monitoring, UC-12-02 audit packets.

**Wave 4 — Agentic & conversational (needs everything above proven)**
UC-01-08 auth submission agent, UC-06-02 edit resolution agent, UC-10-03 conversational billing,
UC-01-14 conversational intake, UC-06-05 rejection repair, UC-05-01 autonomous coding expansion.

**Continuous — the learning loop**
UC-08-05 prevention insight miner + UC-06-03 edit mining + UC-14-05 candidate mining: each
denial, audit finding, and complaint makes the upstream models and rules better. The base
ontology's prevention feedback circuit, run by machines, audited by humans.
