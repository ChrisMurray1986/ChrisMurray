# Use Case Gate Profiles

Application of the feasibility gating framework (`07-feasibility-gating.md`) to every use case
in the catalog. Each profile was derived by: (1) taking the max of the UC's patterns' baseline
vectors, (2) applying autonomy and risk-tier modifiers for the UC's mature state, (3) overriding
with UC-specific requirements.

**Vector notation** — minimum required maturity per dimension:
`D`ata · `I`ntegration · `C`onnectivity · `W`orkflow · `O`rganization · `V`(governance) ·
`E`conomics · `L`egal. Dash (–) = not a binding constraint for this UC.
Vectors state requirements for the UC's **target autonomy**; every UC can pilot at A0/A1 with
one level less on I, V, and W (the "insight-only downgrade" — see note at end).

**Decisive gates** = the one or two dimensions that genuinely decide feasibility at most sites.
**Kill / defer conditions** = the specific finding that stops this UC.

---

## UC-01-* Patient Access

| UC | Vector | Decisive gates | Kill / defer conditions |
|---|---|---|---|
| 01-01 Order intake IDP | D2·I3·C–·W2·O2·V3·E2·L1 | **D**: orders digitized at intake (e-fax, scan-at-receipt); ground-truth set per order type | DEFER if orders remain physical paper with no imaging step; KILL if order volume immaterial |
| 01-02 Identity resolution | D3·I2·C–·W2·O1·V2·E1·L1 | **D**: MPI accessible with match-history; **O**: HIM MPI review capacity | DEFER if no HIM owner for merge review (GOV-09 requires human merge) |
| 01-03 Card OCR & plan mapping | D4·I3·C–·W2·O2·V3·E2·L1 | **W/D**: payer/plan master governed (14.1) with denial-labeled mapping history | DEFER if payer master itself is ungoverned — fix the table before training a model to map into it |
| 01-04 Eligibility orchestration | D3·I3·C2·W3·O1·V2·E2·L2 | **C**: RTE (270/271) live for payers ≥80% of volume; portal ToS for fallback bots | CONDITIONAL: RTE enrollment campaign per payer; SCOPE-CUT payers with no electronic eligibility |
| 01-05 Coverage discovery | D3·I3·C2·W2·O2·V3·E2·L1 | **C**: batch 270/271 + state Medicaid file access | DEFER if state offers no eligibility file/API; monitor false-attach rate from day one |
| 01-06 COB/MSP inference | D3·I2·C2·W2·O2·V2·E1·L1 | **D**: MSPQ answers captured structured (not scanned paper) | DEFER if MSPQ is paper-only → capture-first project |
| 01-07 Auth requirement engine | D3·I3·C3·W3·O2·V3·E2·L2 | **C**: bulletin/portal access for grid maintenance (needs UC-11-03); proof-evidence storage | DEFER without policy-monitoring feed — a stale grid is worse than none (false "no auth required") |
| 01-08 Auth submission agent | D3·I4·C3·W3·O2·V2·E2·L2 | **I**: orchestration fabric (CAP-05); **C**: portal/278 submission rights; clinical-note access approved | DEFER until Wave-0 fabric + GOV-03 harness live; SCOPE-CUT payers whose portals prohibit automation |
| 01-09 Auth tracking bots | D2·I3·C3·W3·O1·V2·E2·L2 | **C**: portal ToS/credential management; UC-14-04 fleet ops live (A4 rule) | KILL for payer segment if ToS prohibits and no 278/API alternative |
| 01-10 Auth-service reconciliation | D3·I3·C–·W3·O2·V3·E2·L1 | **D**: auth details stored structured (number, CPTs, units, span) — not free text | DEFER if auth data lives in notes/comments → structure the capture first (change 1.4.3.A3 practice) |
| 01-11 Necessity screening assist | D3·I3·C–·W2·O2·V2·E2·L2 | **I**: CDS hook at ordering; **O**: ordering-provider adoption path | DEFER if no ordering-workflow integration point (post-hoc screening loses most of the value) |
| 01-12 Estimate engine | D4·I3·C2·W2·O2·V3·E2·L2 | **Dependency**: contract terms loaded (11.2/UC-11-01); **C**: real-time accumulators | DEFER if expected-pay engine unloaded — estimates without contract terms are fiction; GFE content rules (L2) mandatory |
| 01-13 Clearance risk scoring | D4·I3·C–·W3·O2·V3·E2·L1 | **D**: clearance-outcome labels; **O**: counselor capacity for routed accounts | Deferral recommendations stay A1 forever (GOV-09); KILL scoring-for-deferral if V4 absent |
| 01-14 Conversational intake | D3·I3·C–·W3·O2·V2·E2·L3 | **L**: TCPA/consent + recording laws; **O**: live-human escalation staffed across operating hours | KILL if no human escalation coverage plan — HITL-ESCAPE is not optional for R3 |
| 01-15 POS next-best-action | D3·I2·C–·W2·O1·V2·E1·L2 | **W**: single collection policy/discount matrix across sites | DEFER if each site collects differently → standardize policy first (60–90 days) |
| 01-16 Registration QA | D4·I3·C–·W2·O2·V3·E2·L1 | **D**: CAP-02 labels linking denials back to registration fields | CONDITIONAL: build denial→field attribution first (4–8 wks); rules-only version can start at D3 |
| 01-17 No-show revenue protection | D4·I3·C–·W2·O1·V2·E1·L3 | **E**: materiality by service line; **L**: outreach consent | KILL for low-volume/low-no-show lines; POOL with UC-01-14 outreach infrastructure |

## UC-02-* Utilization Review

| UC | Vector | Decisive gates | Kill / defer conditions |
|---|---|---|---|
| 02-01 Status prediction | D4·I2·C–·W2·O2·V3·E2·L1 | **D**: structured clinical features (labs/vitals/orders) + status-outcome labels | DEFER if clinical data locked in text only → NLP feature extraction is the prerequisite project |
| 02-02 Criteria auto-abstraction | D3·I2·C–·W2·O2·V2·E2·L2 | **L**: MCG/InterQual license permits programmatic criteria use | KILL if licensor prohibits automated mapping and won't negotiate — this is a contractual, not technical, gate |
| 02-03 Notification/submission bots | D3·I3·C3·W3·O2·V3·E2·L2 | **C**: per-payer portal/fax/278N channel inventory | SCOPE-CUT to payers with viable channels; manual residual quantified in E |
| 02-04 Auth-days runway monitor | D3·I3·C–·W3·O1·V2·E1·L1 | **D**: authorized days/level stored structured (same gate as UC-01-10) | DEFER until auth capture structured |
| 02-05 Avoidable-day classification | D3·I2·C–·W2·O1·V2·E1·L1 | **W**: avoidable-day reason taxonomy exists and is used | DEFER if no taxonomy → define it (part of 2.3.A1 standardization), then classify |

## UC-03-* Charge Capture & Revenue Integrity

| UC | Vector | Decisive gates | Kill / defer conditions |
|---|---|---|---|
| 03-01 Missing charge detection | D4·I2·C–·W2·O2·V2·E2·L1 | **D**: orders/eMAR/schedule/charge linkage across systems; **O**: department owners committed to work the lists | DEFER if source systems can't be joined at encounter level; KILL-per-dept if no owner accepts the queue |
| 03-02 Dup/anomaly charge screen | D3·I3·C–·W3·O2·V3·E2·L1 | **I**: pre-bill hold hook in billing system | Downgrade to post-bill detection (A0 lists) if no pre-bill hold capability |
| 03-03 Drug units validator | D3·I3·C–·W3·O2·V3·E2·L1 | **D/W**: NDC→HCPCS crosswalk under 14.1 governance; pharmacy system feed | DEFER if crosswalk is an unowned spreadsheet — govern the table first |
| 03-04 Charge trigger surveillance | D3·I2·C–·W2·O1·V2·E1·L1 | **D**: ≥12 mo charge history for baselines; named alert owner | Low bar — Wave-1 candidate almost everywhere |
| 03-05 CDM update automation | D3·I3·C–·W3·O2·V2·E1·L1 | **W**: governed CDM change workflow (3.3.1) exists to receive proposals | DEFER if CDM changes happen by direct edit — automation would bypass governance that doesn't exist |
| 03-06 Autonomous charging | D4·I3·C–·W4·O2·V3·E2·L1 | **W**: documentation practice stable per domain (start/stop times, criteria fields actually documented) | Enable domain-by-domain; DEFER any domain where source documentation is incomplete (capture-first) |
| 03-07 Device/implant reconciliation | D3·I2·C–·W2·O1·V2·E2·L1 | **D**: supply-chain system feed with item-master↔CDM linkage + invoice data | DEFER if OR supply documentation is paper stickers → point-of-use capture project first |
| 03-08 MRF pipeline | D3·I3·C–·W2·O1·V2·E1·L2 | **Dependency**: contract engine load quality (11.2) | Publishing automation on bad terms data automates noncompliance — gate on load verification (UC-11-01) |

## UC-04-* CDI

| UC | Vector | Decisive gates | Kill / defer conditions |
|---|---|---|---|
| 04-01 CDI prioritization | D4·I2·C–·W2·O2·V2·E2·L1 | **D**: note corpus access + DRG/query outcome labels | CONDITIONAL: label backfill from encoder + query tool history |
| 04-02 Evidence surfacing | D3·I2·C–·W2·O1·V2·E1·L1 | **I**: real-time chart read inside CDI workflow tool | Low risk (A0); feasible early at most sites |
| 04-03 Query drafting | D3·I3·C–·W3·O2·V2·E2·L1 | **W**: query practice standardized to AHIMA/ACDIS brief; GOV-03 template validation harness | DEFER if query practice is freeform/noncompliant today — standardize the human process first |
| 04-04 HCC suspecting | D4·I2·C–·W2·O2·V3·E2·L2 | **O**: provider workflow adoption; **V**: RA-compliance guardrails (evidence-backed only) | KILL if no VBC/MA population (E structurally zero); DEFER without compliance guardrail build |
| 04-05 DRG recon triage | D3·I3·C–·W2·O1·V2·E1·L1 | CDI and coding on interoperable platforms (working-DRG + final-DRG both extractable) | Trivial where both live in one suite; DEFER if working DRG isn't recorded |

## UC-05-* Coding

| UC | Vector | Decisive gates | Kill / defer conditions |
|---|---|---|---|
| 05-01 Autonomous/assisted coding | D4·I3·C–·W3·O2·V3·E2·L2 | **V**: audit-sampling + golden sets per case type (GOV-07/CAP-09); documentation-quality floor per enabled type | Never KILL wholesale — scope by case type; DEFER any type failing precision floor on golden set |
| 05-02 DRG risk scoring | D4·I2·C–·W2·O2·V3·E2·L1 | **D**: audit/denial outcome labels tied to coded claims; **O**: second-review capacity | DEFER if historical audit outcomes weren't recorded → instrument 12.x/5.7 first |
| 05-03 Disposition validator | D3·I2·C–·W2·O1·V2·E2·L1 | **D**: post-acute signals (ADT feeds, HIE, payer claims) available to cross-check | Rules-only version (internal documentation cross-check) feasible everywhere; external-signal version needs HIE access |
| 05-04 Deficiency chase | D3·I3·C–·W2·O1·V2·E1·L1 | **D**: HIM deficiency tracking structured (not email) | Low bar; DEFER only if deficiency management is ad hoc → W2 first |
| 05-05 Work distribution optimizer | D3·I3·C–·W3·O2·V2·E1·L1 | **I**: queue assignment APIs; credential/skill matrix data current | DEFER if queues are manually cherry-picked with no API — workflow platform gap |
| 05-06 QA sampling optimizer | D4·I2·C–·W2·O1·V2·E1·L1 | **D**: QA results history in analyzable form | CONDITIONAL: 1–2 quarters of structured QA capture if history is in spreadsheets |
| 05-07 Edit/denial coding assist | D3·I2·C–·W2·O2·V2·E2·L2 | **L**: licensed reference corpus (Coding Clinic, NCCI manuals) usable in retrieval system | DEFER until license rights for programmatic use secured; GOV-03 harness required |

## UC-06-* Claims

| UC | Vector | Decisive gates | Kill / defer conditions |
|---|---|---|---|
| 06-01 Denial risk scoring | D4·I3·C–·W3·O2·V3·E2·L1 | **D**: CAP-02 denial labels ≥12 mo with defect attribution; **W**: leadership-owned hold-vs-release policy | DEFER without label pipeline (Wave-0); pilot A0 (score display) while hold policy is negotiated |
| 06-02 Edit resolution agent | D3·I4·C–·W3·O2·V3·E2·L1 | **I**: fabric; **W**: governed auto-resolution class list with compliance sign-off | Start A1 (recommend) on top-10 edit types; A3 only per governed class |
| 06-03 Edit rule mining | D4·I2·C–·W3·O1·V2·E2·L1 | **D**: denial/rejection history linked to claim data; **W**: 6.2.4 rule-governance process | DEFER if edit rules are vendor-locked with no custom-rule capability |
| 06-04 Submission integrity | D3·I3·C1·W3·O1·V2·E1·L1 | **D**: 999/277CA retained and parsed (many shops discard acks) | CONDITIONAL: turn on ack retention (weeks); then straightforward — Wave-1 |
| 06-05 Rejection auto-repair | D3·I4·C1·W3·O2·V3·E2·L1 | **I**: fabric; **W**: governed repair-class list | Same pattern as 06-02; A1 first |
| 06-06 Timely filing sentinel | D3·I3·C–·W3·O1·V2·E1·L1 | **Dependency**: filing-limit matrix codified per payer/contract (11.2.A4) | DEFER if limits live in analysts' heads → contract-matrix load is the prerequisite |
| 06-07 Attachment prediction | D4·I3·C2·W2·O2·V2·E2·L1 | **C**: attachment channels (275/portal) per payer; ADR/RFI history as labels | SCOPE-CUT fax-only payers; L1 minimum-necessary review of auto-assembled packets |
| 06-08 COB/secondary automation | D3·I3·C1·W3·O1·V3·E2·L1 | **D**: primary 835 data quality (adjustment detail complete) | DEFER for payers whose remits lack required COB detail → paper-EOB IDP (UC-07-03) feeds this |

## UC-07-* Payments

| UC | Vector | Decisive gates | Kill / defer conditions |
|---|---|---|---|
| 07-01 Intelligent auto-posting | D3·I3·C1·W3·O2·V3·E2·L1 | **C**: ERA penetration ≥80% of remit volume; **W**: posting rules standardized (one adjustment-code scheme) | CONDITIONAL: ERA/EFT enrollment campaign first; if paper-heavy, UC-07-03 precedes this |
| 07-02 CARC mapping intelligence | D4·I2·C–·W2·O2·V2·E1·L1 | **W**: internal action taxonomy (7.1.3) defined and owned | DEFER if no taxonomy — the model would learn today's mis-mappings (FM-AI-07) |
| 07-03 Paper EOB/correspondence IDP | D2·I3·C–·W2·O2·V3·E2·L1 | **D**: lockbox imaging service (bank-provided) or in-house scan-at-receipt | CONDITIONAL: switch lockbox to imaging service (contract change, 4–8 wks); ground truth ≥500 docs |
| 07-04 Treasury matching | D3·I3·C–·W2·O1·V2·E2·L1 | **I**: daily bank feed (BAI2/API) + TRN retention | Straightforward Wave-1/2 where bank feeds exist |
| 07-05 Variance detection coverage | D3·I3·C–·W3·O2·V2·E2·L1 | **Dependency**: expected-pay engine loaded and covering the payer mix (11.2) | DEFER if no contract engine — building/loading it IS the project; unpriced-rate alarm from day one |
| 07-06 Recoupment validation | D3·I2·C–·W2·O1·V2·E2·L2 | **D**: takeback transactions linked to original claims; **L**: state recoupment-law matrix maintained | CONDITIONAL: linkage repair in posting rules; legal matrix is a maintainable artifact, not a blocker |

## UC-08-* Denials & Appeals

| UC | Vector | Decisive gates | Kill / defer conditions |
|---|---|---|---|
| 08-01 Denial classification | D3·I3·C–·W2·O2·V3·E2·L1 | **W**: governed denial taxonomy; **D**: all denial channels feeding (835 + letters via UC-07-03) | DEFER taxonomy-first if none exists (2–4 wks); paper-denial capture gap = silent coverage hole |
| 08-02 Overturn/priority scoring | D4·I3·C–·W3·O2·V3·E2·L1 | **D**: appeal outcomes historically recorded (win/loss/dollars by level) | DEFER if outcomes weren't tracked → instrument 8.4.6 and accumulate 2+ quarters; interim: rules-based prioritization (deadline × dollars) |
| 08-03 Appeal generation | D3·I3·C–·W3·O2·V2·E2·L2 | **Dependency**: CAP-04 payer-policy library + GOV-03 citation harness; **O**: reviewer throughput sized; clinical variant adds **L**: criteria license (programmatic rights), **D**: chart-corpus access + recorded appeal outcomes (golden set) | DEFER without policy library (an LLM citing policies it can't retrieve is FM-AI-02 by design); pilot on one denial class. Full engineering deep-dive: `12-clinical-appeals-engineering.md` |
| 08-04 Rebill-loop breaker | D3·I2·C–·W3·O1·V2·E1·L1 | **D**: touch/action history logged (W4 instrumentation) | DEFER where follow-up actions aren't logged — instrumentation-first |
| 08-05 Prevention insight miner | D4·I2·C–·W3·O2·V2·E2·L1 | **O**: cross-functional routing authority (owners obligated to accept prevention actions) | KILL-as-designed if governance won't assign ownership — insight without routing authority is a report nobody reads |
| 08-06 Appeal outcome verification | D3·I3·C–·W2·O1·V2·E2·L1 | **D**: appeal decisions structured + payment linkage | Low bar once 08-01/02 exist |

## UC-09-* AR Management

| UC | Vector | Decisive gates | Kill / defer conditions |
|---|---|---|---|
| 09-01 AR prioritization | D4·I3·C–·W3·O3·V3·E2·L1 | **O**: management adopts ranked worklists over aging buckets (change management, O3); touch history for yield models | The model is rarely the problem; adoption is. DEFER if supervisors won't retire cherry-picking |
| 09-02 Status bot fleet | D3·I3·C2·W3·O1·V2·E2·L2 | **C**: 276/277 enrollment + portal ToS per payer; UC-14-04 fleet ops (A4 rule) | SCOPE-CUT prohibited portals; DEFER A4 until fleet observability live |
| 09-03 Underpayment recovery | D3·I2·C–·W3·O2·V2·E2·L1 | **Dependency**: contract engine (same gate as 07-05); demand process (9.4) standardized | DEFER without loaded terms — you cannot recover variances you cannot compute |
| 09-04 Credit balance automation | D4·I3·C–·W3·O2·V3·E2·L2 | **I**: refund execution path into AP/check systems; **W**: refund approval matrix | Classification (A0/A1) feasible early; execution (A2/A3) gated on AP integration + GOV-08 thresholds |
| 09-05 Special-account monitoring | D3·I3·C3·W3·O1·V2·E2·L2 | **C/L**: external feeds licensed (bankruptcy/PACER, death registries) | CONDITIONAL: data subscriptions; auto-stop on bankruptcy is the first (compliance-safe) release |
| 09-06 Aged-AR disposition | D4·I2·C–·W3·O2·V2·E2·L2 | **W**: 9.7 gate policy (statements/FA/dispute checks) codified; **L**: 501(r) counsel review | DEFER if placement gates are informal → codify, then automate verification |

## UC-10-* Patient Financial Services

| UC | Vector | Decisive gates | Kill / defer conditions |
|---|---|---|---|
| 10-01 Liability verification gate | D3·I3·C–·W3·O2·V3·E2·L2 | **I**: statement-vendor suppression hook (can we actually stop a statement?) | DEFER if statement vendor can't take per-account suppression — vendor/contract change first |
| 10-02 Statement optimization | D4·I3·C–·W2·O2·V3·E2·L3 | **I**: vendor supports channel/timing variation; **L**: required content invariant (GOV-13) | SCOPE to what vendor supports; GOV-06 review (treatment differences must not track protected classes) |
| 10-03 Conversational billing agent | D3·I3·C–·W3·O2·V3·E2·L3 | **I**: unified account-360 API (balance provenance across HB/PB); **W**: one plan/discount matrix; **O**: escalation staffing | DEFER if policies vary by site (standardize first) or if account data can't be assembled for a coherent answer — a billing bot that can't explain the bill is a complaint generator |
| 10-04 Plan default rescue | D4·I3·C–·W2·O2·V3·E2·L3 | **D**: plan payment histories; **L**: TCPA consent for outreach channel | CONDITIONAL on consent capture in plan enrollment flow |
| 10-05 Presumptive FA scoring | D4·I3·C–·W3·O2·V4·E2·L3 | **V**: GOV-06 bias program operational (hard gate); **L/D**: external socioeconomic data licensed + permissible | Cap at A0 (screening lists) until V4; KILL auto-denial variants permanently (GOV-09) |
| 10-06 NSA protection classifier | D3·I3·C–·W3·O2·V3·E2·L3 | **D**: consent artifacts + network status + claim context linkable | DEFER if NSA consents are unindexed paper → capture/indexing first; err-protective default lowers risk of early launch |
| 10-07 Agency oversight analytics | D3·I2·C3·W2·O1·V2·E2·L2 | **C/L**: contractual rights to call recordings + activity data from agencies (GOV-14) | DEFER per vendor until contracts grant data/audit rights — renegotiate at renewal |
| 10-08 GFE variance monitor | D3·I2·C–·W2·O1·V2·E1·L2 | **D**: GFEs stored structured and linkable to final bills (1.6 discipline) | CONDITIONAL: fix GFE storage practice; then trivial rules |

## UC-11-* Contracting, Credentialing & Enrollment

| UC | Vector | Decisive gates | Kill / defer conditions |
|---|---|---|---|
| 11-01 Contract extraction & load verification | D2·I2·C–·W2·O2·V2·E2·L1 | **D**: complete contract repository (all executed contracts + amendments located and digitized) | DEFER if contracts are scattered/missing — repository assembly is the prerequisite project (and valuable alone) |
| 11-02 Amendment watchdog | D3·I2·C–·W2·O1·V2·E1·L1 | **Dependency**: correspondence digitization (UC-07-03) + contract calendar data | Cheap once 07-03 and 11-01 exist |
| 11-03 Policy monitoring & routing | D3·I2·C3·W3·O2·V2·E2·L2 | **O/W**: named implementation owners per change type with routing paths | KILL-as-designed without routing ownership — unrouted intelligence is shelfware; GOV-03 for summaries |
| 11-04 Credentialing/enrollment lifecycle | D3·I3·C3·W3·O2·V2·E2·L2 | **D**: provider master as governed single source (14.1) | DEFER if provider data lives in spreadsheets → provider-master project first; exclusion monitoring can start immediately (low bar, high stakes) |
| 11-05 Payer scorecards | D4·I2·C–·W2·O1·V2·E1·L1 | **D**: cross-domain cost attribution (denial/auth/appeal labor by payer — needs touch instrumentation) | Start with claims-data-only version (yield, denial rates); labor attribution matures with W4 coverage |
| 11-06 VBC settlement validation | D4·I2·C2·W2·O2·V2·E2·L2 | **C/L**: contractual data-sharing (claims extracts, attribution rosters) actually flowing | DEFER per contract until data rights exercised; KILL if no VBC book |

## UC-12-* Compliance & Audit

| UC | Vector | Decisive gates | Kill / defer conditions |
|---|---|---|---|
| 12-01 Audit intake & deadlines | D2·I3·C–·W3·O2·V3·E1·L2 | **D**: every audit channel digitized (mail imaging, portal polling, fax) — one missed channel defeats the purpose | CONDITIONAL: channel inventory + capture completeness before go-live; GOV-10 routing locks wired |
| 12-02 Audit packet assembly | D3·I4·C–·W3·O2·V2·E2·L2 | **I**: HIM/EHR retrieval APIs; release-approval workflow | DEFER until record retrieval is programmatic; manual-pull residual quantified |
| 12-03 Billing pattern surveillance | D3·I2·C–·W2·O2·V2·E1·L2 | **D**: peer benchmark data licensed; **O**: compliance charter covers surveillance use | L2: provider-relations/legal review of how findings are used (GOV-09 — leads, not verdicts) |
| 12-04 Overpayment register | D3·I3·C–·W3·O2·V3·E1·L2 | **D/W**: every identification source (7.4.2, 9.5, 5.7, 12.1–12.3) feeding the register — completeness is the whole point | DEFER partial launches only with explicit registry-scope disclosure; counsel owns scope decisions (GOV-10) |
| 12-05 Regulatory intelligence | D3·I2·C–·W3·O2·V2·E1·L1 | **O/W**: implementation routing owners (same gate as 11-03) | Same kill condition as 11-03 |
| 12-06 Extrapolation modeling | D3·I1·C–·W2·O1·V2·E1·L2 | **L**: privilege protocol for work product (counsel-directed analysis) | DEFER until privilege handling defined — a discoverable exposure model is a self-inflicted wound |

## UC-13-* Analytics & Performance

| UC | Vector | Decisive gates | Kill / defer conditions |
|---|---|---|---|
| 13-01 KPI anomaly narratives | D3·I2·C–·W2·O1·V2·E1·L1 | **W**: KPI definitions governed (13.1) — anomaly detection on ungoverned metrics is noise | DEFER until KPI dictionary exists; then Wave-1 easy |
| 13-02 Reserve/net-revenue models | D4·I2·C–·W2·O2·V3·E2·L2 | **V**: full lineage/auditability — external financial auditors must accept the methodology | DEFER without lineage tooling; run in shadow against current method ≥2 closes before reliance |
| 13-03 Cash forecasting | D4·I2·C–·W2·O1·V2·E1·L1 | **D**: payment-timing history by payer ≥24 mo | Low risk (A0); Wave-2 |
| 13-04 Governance telemetry | D3·I4·C–·W3·O2·V2·E1·L1 | **O**: governance body operating (someone consumes the telemetry and can demote autonomy) | Wave-0: every A3+ UC in this catalog depends on it; build before scaling anything past A1 |

## UC-14-* Master Data, Technology & Vendors

| UC | Vector | Decisive gates | Kill / defer conditions |
|---|---|---|---|
| 14-01 Payer/plan master intelligence | D4·I3·C–·W3·O2·V2·E1·L1 | **W**: 14.1 master-data governance workflow to receive corrections | DEFER if master changes are direct edits — same logic as 03-05 |
| 14-02 Drift & sync monitoring | D3·I2·C–·W2·O1·V2·E1·L1 | **I**: extract access to every system copy (estimator, MRF, contract engine, billing) | CONDITIONAL per system; partial coverage disclosed, not silent |
| 14-03 EDI observability | D3·I2·C1·W3·O1·V2·E1·L1 | **D**: transaction telemetry retained (volumes, acks, timestamps); incident process (W3) | Wave-0; trivial data, high leverage |
| 14-04 Bot fleet observability | D3·I4·C–·W3·O2·V2·E1·L1 | **W**: quarantine/hand-back queues defined (GOV-05 wiring); telemetry standard adopted by every bot | Wave-0; a hard prerequisite for any A4 RPA in this catalog — sequencing rule, not preference |
| 14-05 Candidate mining | D3·I1·C–·W2·O1·V2·E1·L1 | **D**: touch/action logging coverage (W4 breadth across teams) | Value scales with instrumentation coverage; start where logging exists |
| 14-06 Downtime orchestration | D3·I4·C–·W3·O2·V2·E1·L1 | **W**: downtime procedures documented (14.6) — you cannot orchestrate a checklist that doesn't exist | DEFER until downtime procedures written and drilled manually at least once |
| 14-07 Vendor analytics | D3·I2·C3·W2·O1·V2·E1·L2 | **C/L**: contractual data/telemetry rights per vendor (GOV-14) | DEFER per vendor to contract renewal if rights absent |

---

## Reading the portfolio through the gates

**The five gates that decide most of the portfolio** (recurring decisive gates):

1. **CAP-02 label pipeline (D4)** — gates every PAT-PRED use case (06-01, 08-02, 09-01, 05-02,
   01-16, 13-02…). One investment unlocks a dozen use cases; its absence quietly downgrades
   them all to rules-based versions.
2. **Contract engine load quality (11.2 / UC-11-01)** — gates 01-12, 03-08, 06-06, 07-05,
   09-03. Estimates, variance detection, underpayment recovery, and filing sentinels all
   compute against loaded terms. Load verification is the highest-leverage single remediation.
3. **Payer connectivity & ToS (C2/C3)** — gates all RPA/transaction use cases (01-04, 01-09,
   02-03, 09-02…). Managed by enrollment campaigns and per-payer scope-cuts, not all-or-nothing.
4. **Workflow standardization (W2/W3)** — gates conversational and policy-driven use cases
   (10-03, 01-15, 08-01 taxonomy…). The 60–90-day standardization sprint is the most commonly
   needed — and most commonly skipped — prerequisite.
5. **Wave-0 fabric (I4 + V3: CAP-05/06, UC-13-04, UC-14-04)** — gates every agent and every
   A3+ deployment. Build once, amortize across the catalog.

**Insight-only downgrade rule:** any use case blocked on I (write-back), V (governance), or W
(exception paths) can usually launch as an A0/A1 worklist/recommendation with one level less on
those gates, capturing partial value while remediation proceeds — at the cost of adding human
review labor into E. The downgrade is never available for D gaps (no data is no data) or hard
L prohibitions.
