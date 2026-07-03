# Implementation Patterns — What Actually Satisfies Each Gate

The gating framework's facets are deliberately technology-agnostic capability contracts. This
layer is the translation table: for each facet, **what a passing demo looks like** (the
sufficiency floor), the **reference pattern at common stack archetypes**, and an explicit
**overbuild flag** where vendors routinely sell more platform than the gate requires. Use it
two ways: assessors read the "passing demo" column to score honestly (the Play-1 evidence rule
made concrete); architects read the pattern columns to buy or build *minimally*.

**Stack archetypes**

| Archetype | Meaning |
|---|---|
| **Epic shop** | Single-instance Epic: Chronicles operational, Clarity (nightly relational) + Caboodle (dimensional) analytics, Interconnect/FHIR/CDS Hooks interfaces, Resolute HB/PB billing |
| **Oracle Health shop** | Cerner Millennium operational, CCL/Discern + Oracle Health data platforms for analytics; same principles, different module names |
| **Multi-EHR / best-of-breed** | Multiple EHRs or heavy bolt-ons; integration engine (Mirth/Rhapsody/Cloverleaf) + an enterprise warehouse become load-bearing much earlier |

*Module names are indicative as of this document's writing; Epic/Oracle packaging and licensing
change — verify current product scope before committing a plan to a named module.*

---

## 0. The two rules that prevent most overbuying

**Rule 1 — Latency decoder.** Sort every facet you're remediating into one of two lanes before
choosing any technology:

- **Analytical lane** (training data, labels, history, reconciliation): T+1 batch is the
  sufficiency floor. Clarity/Caboodle-class nightly extracts satisfy D3 here. *No streaming, no
  lakehouse required.* This lane covers the largest cluster of use cases in the catalog
  (denial/AR/charge scoring, reserve models, QA optimization, mining).
- **Operational lane** (registration QA at save, CDS at ordering, POS prompts, eligibility at
  arrival, conversational account view): served by the EHR's *operational* surfaces — CDS
  Hooks, FHIR/Interconnect APIs, workqueue rules, RTE. An analytics platform contributes
  nothing in this lane, however AI-ready it is.

**Rule 2 — The lakehouse trigger list.** A dedicated AI data platform (Snowflake / Databricks /
Fabric class) is justified when — and only when — one or more of these is true:

1. Material **non-EHR data** must be joined at scale: clearinghouse 835/999/277CA archives,
   bank/lockbox feeds, bot telemetry, vendor/agency files, call recordings, contract documents.
2. **CAP-02 label pipeline** needs lineage/time-travel at auditor grade (the `lineage` facet).
3. **Multi-EHR / multi-instance** consolidation (the third archetype).
4. Embedding/feature stores for **unstructured corpora at scale** beyond what a document store
   + vector index covers.

Absent a trigger, the floor for a mid-size single-Epic shop is: Clarity/Caboodle + a modest
augmentation layer (a schema for non-Epic feeds, dbt-style transforms, an orchestrator).
**D4 is never a platform property**: no warehouse purchase creates denial labels, appeal
outcomes, or UM worksheets. The scarce asset is recorded operational truth.

---

## 1. Data facets — transactional & financial history

| Facet | Passing demo (floor) | Epic shop | Multi-EHR / Oracle Health | Overbuild flag |
|---|---|---|---|---|
| `denial_labels` | Query returns 12 mo of denials joined to accounts with defect/owner attribution | Clarity remit tables + denial workqueue history; attribution usually needs a built mapping table (CARC×context→owner) | Same shape from clearinghouse data if EHR remit detail is thin | ⚠ This is modeling work, not platform work — no purchase substitutes for the attribution table |
| `appeal_outcomes` | Pull win/loss/$ by level for last year's appeals | Appeal tracking in workqueues/extension or bolt-on; if outcomes live in letter PDFs, capture is the project | Bolt-on appeal trackers common; harvest their DB | Start *recording* today; backfill is impossible |
| `touch_logging` | Show who touched an account, when, action taken, for any account | HB/PB account activity/history tables (largely native); gaps are in bolt-on/vendor activity | Integration-engine event capture per system | Don't build a "workforce analytics platform" to get this — the billing system already logs most of it |
| `takeback_linkage` | Any recoupment traces to its original claim in one query | Posting-rule discipline in Resolute (link on reversal transactions) | Same — posting convention, not technology | Pure configuration/process fix |
| `acks_retained` | Produce the 999/277CA for any claim from last quarter | Clearinghouse portal retention → nightly file archive into the warehouse | Same (clearinghouse-side) | Weeks of work; never a platform project |
| `edi_telemetry` | Chart daily 837/835/270 volumes by payer for 12 mo | Same archive + simple aggregates | Same | A dashboard, not a data product |
| `bank_feeds` | Yesterday's BAI2/API feed with TRN visible | Treasury feed → warehouse table; match to 835 TRN | Same | — |
| `payment_timing_history` / `realization_history` | 24-mo lag curves by payer render | Clarity remit + transaction history; standard Cogito content covers much of it | Warehouse from remit archives | — |
| `plan_payment_history` / `statement_history` | Installment/statement response history per guarantor | HB guarantor/statement tables; statement-vendor return files ingested | Statement vendor files are the usual gap | — |
| `clearance_outcomes` | Clearance status at service + downstream payment outcome, joined | Prelude/registration items + remit join; usually a small build | Same | Turn on capture now (prospective-label rule) |
| `audit_outcomes` | Findings + dollars by audit, linked to claims | Audit tracking module/bolt-on or structured log; often spreadsheets → move to a table | Same | A governed table suffices — not a GRC platform purchase |

## 2. Data facets — clinical corpus & mid-cycle labels

| Facet | Passing demo (floor) | Epic shop | Multi-EHR / Oracle Health | Overbuild flag |
|---|---|---|---|---|
| `notes_access` | Programmatically fetch all notes for a specified encounter, with approval on file | Bulk FHIR / Clarity note text (HNO) extract into a document store; governance sign-off is half the gate | Millennium clinical events export; multi-EHR needs per-source pipes | ⚠ The blocker is almost always *approval and governance*, not extraction tech |
| `clinical_structured` | Labs/vitals/meds for an encounter as timestamped rows | Clarity/Caboodle flowsheet, lab, MAR tables — native | HL7v2 feeds → warehouse in multi-EHR | Already satisfied at most EHR shops; score it, don't build it |
| `um_worksheets` | Criteria worksheets + final status determinations queryable | UM/CM module documentation if used structurally; if worksheets are scanned or in a criteria vendor's silo, negotiate the export | Criteria vendor (MCG/InterQual) platform export — contract question | Data-rights conversation, not an ETL project |
| `working_drg_recorded` | Working DRG and final DRG side-by-side per case | CDI module fields (native where CDI documents in-system) | CDI bolt-on DB export | — |
| `deficiency_structured` / `qa_history` | Deficiency/QA results as rows, not emails/spreadsheets | HIM deficiency tracking (native); QA → a simple governed table | Same | — |

## 3. Data facets — documents, images & reference masters

| Facet | Passing demo (floor) | Epic shop | Multi-EHR / Oracle Health | Overbuild flag |
|---|---|---|---|---|
| `orders_digitized` | Any inbound order retrievable as an image/text within minutes of receipt | e-fax → document management (OnBase/ECM class) indexed to patient | Same | Intake process change + imaging service; not an AI platform |
| `card_images` | Front/back card images for yesterday's registrations | Prelude/Welcome kiosk + MyChart pre-check-in capture; front-desk scanner compliance is the real gap | Same | Process compliance beats technology here |
| `lockbox_imaging` | Yesterday's lockbox correspondence as images | Bank imaging service (contract change) or scan-at-receipt | Same | A banking-services amendment, ~weeks |
| `audit_channels_digitized` | Every audit letter from any channel lands in one queue | Mail imaging + payer-portal polling + fax-to-image → one intake queue | Same | — |
| `consents_indexed` | Pull the NSA consent for a given OON claim | eSignature/consent module indexed to encounter; paper → scan+index backlog | Same | — |
| `contract_repository` | Every executed contract + amendment retrievable by payer | Contract mgmt system or governed document library; completeness is the work | Same | Repository ≠ CLM suite; a governed library passes |
| `contract_engine_loaded` | Expected pay computes for 80% of volume; parallel-priced sample matches | Resolute expected-reimbursement contracts (native) loaded + verified; or contract-mgmt bolt-on | Bolt-on engines common | ⚠ Verification (UC-11-01) is the gate — "loaded" without parallel-pricing proof scores 1, not 2 |
| `policy_library` | Retrieve the policy version in force on a date, with citation | Built corpus: payer portals/bulletins scraped into versioned store (CAP-04); no EHR module does this | Same | Scope to top payers × top categories first (per deep-dive) |
| `provider_master` | One governed source answers NPI/credential/enrollment status | Epic SER records + credentialing system reconciled; governance process is the gate | Credentialing bolt-on as source of truth | — |
| `charge_linkage` | Orders↔eMAR↔schedule↔charges join for one encounter | Native in Clarity (order, MAR, charge tables share encounter keys) | Multi-system: this is where the integration warehouse earns its keep | Single-EHR shops: score before building — you likely already pass |
| `supply_chain_feed` | Implant case: item, invoice cost, charge in one view | ERP (Workday/Oracle/Infor) item master + invoice feed joined to CDM | Same | — |
| `mspq_structured` / `auth_structured` / `gfe_stored` | The artifact (MSPQ answers / auth CPT-units-span / estimate) as fields, not scans | Registration items, auth/cert records, estimate module output retained | Same | Configuration + practice discipline; zero new platforms |
| `system_copy_extracts` / `peer_benchmarks` | Diff two system copies of a master; benchmark table queryable | Nightly extracts of each copy; benchmark data licensed (e.g., specialty societies, CMS PUFs) | Same | — |

## 4. Integration facets

| Facet | Passing demo (floor) | Epic shop | Multi-EHR / Oracle Health | Overbuild flag |
|---|---|---|---|---|
| `writeback` | Create a flag/queue item/transaction via API in test | Interconnect web services, FHIR write scopes, workqueue APIs | Millennium ops APIs / integration engine | — |
| `fabric` | An event triggers an agent that writes back and is observable, with a non-human identity | Event feeds (HL7v2/FHIR subscriptions) + queue/API layer + service accounts + telemetry — a build, not a purchase | Same; integration engine as backbone | ⚠ This is Wave-0 by design — but it's plumbing + identity + telemetry, not a $2M "agent platform" license |
| `prebill_hold` | Programmatically hold one claim pre-drop in test | Resolute billing indicators/workqueue routing (native config) | RevElate/bolt-on equivalent | Configuration |
| `statement_suppression` / `statement_vendor_flex` | Suppress/vary one account's statement via file or API | Statement vendor interface spec; often a contract amendment | Same | Vendor negotiation, not integration heroics |
| `ap_refund_path` | Issue one test refund end-to-end programmatically | Refund file/API to ERP AP | Same | — |
| `cds_ordering_hook` | A rule fires in the ordering workflow in test | **CDS Hooks / BPA framework — native Epic**; the gate is governance to add rules | Discern rules | Do not stand up an external CDS platform for this |
| `account_360` | One API call assembles HB+PB balance provenance for a guarantor | Composite service over billing APIs; MyChart billing views prove the data exists | Harder multi-system — this is a real build | — |
| `queue_api` | Reassign work items programmatically in test | Workqueue APIs / RPA-free routing config | Same | — |
| `him_retrieval` | Fetch a defined record set for an encounter programmatically | Release-of-information module APIs / Bulk FHIR document references | Same | — |

## 5. Connectivity facets

Mostly clearinghouse and payer-side; the EHR archetype matters less than the trading-partner
work.

| Facet | Passing demo (floor) | Pattern | Overbuild flag |
|---|---|---|---|
| `rte_eligibility` / `era_coverage` / `claim_status_edi` | Transaction volumes ≥80% coverage on last month's data | Clearinghouse enrollment campaigns (14.3); Epic RTE/remit modules consume natively | Enrollment project management — never a platform |
| `auth_transactions` | Submit/inquire an auth electronically for top payers | 278 via clearinghouse, payer APIs (FHIR prior-auth era), Epic Payer Platform where both sides participate | Payer-by-payer; scope-cut the rest |
| `portal_automation_permitted` | ToS review memo + managed credentials for named portals | Legal review + credential vault + MFA handling | ⚠ Legal gate; no RPA tool purchase makes an unpermitted portal permitted |
| `attachment_channels` | Send a 275/portal attachment for top payers | Clearinghouse attachment services | — |
| `medicaid_files` | Pull the state file incl. retro spans on schedule | State-specific batch/API | — |
| `external_registries` / `agency_data_rights` / `vbc_data_sharing` / `bulletin_access` | The feed lands on schedule with rights documented | Data subscriptions / vendor-contract amendments / payer data-sharing exhibits | Contract work in every case |

## 6. Workflow, org, governance & legal facets

**Workflow and org facets are stack-agnostic by nature** — they live in policy documents,
committee charters, and configuration discipline, not in any platform. The Epic-shop note is
simply *where* the artifact lives: adjustment-code schemes and write-off matrices in Resolute
configuration; queue/reason-code standardization in workqueue design; the denial taxonomy in
the mapping tables of §1. Score them on the artifact's existence and enforcement.

Governance facets have concrete reference patterns worth naming:

| Facet | Passing demo (floor) | Reference pattern | Overbuild flag |
|---|---|---|---|
| `decision_logging` | Reconstruct one automated decision end-to-end (inputs, version, output, override) | Structured logs + model/prompt registry (MLflow/registry class, CAP-10) | — |
| `model_monitoring` | A drift alert fired (or test-fired) and a demotion path exists | Telemetry + thresholds + the UC-13-04 review loop; cloud-native monitors suffice | ⚠ An "AI observability suite" is not required to start; dashboards + paging + a demotion runbook pass |
| `bias_program` | Last adverse-impact test report for a patient-affecting model | Quarterly test harness + review sign-off (GOV-06) | Process + statistics, not software |
| `citation_harness` | A seeded fake citation is caught automatically in test | String-alignment verifier + verify-mode second model call (file 12 §4) | A few engineer-weeks; build it once, reuse portfolio-wide |
| `golden_sets` | A versioned, quarantined eval set exists for the use case with a scoring rubric | Case curation + blinded rubric tooling (CAP-09); spreadsheet-grade tooling passes at MVP | The discipline (quarantine, versioning) is the gate, not the tooling |
| `lineage` | Trace a reserve figure to its inputs for an external auditor | Warehouse-native lineage (dbt docs / platform lineage) | This one IS a legitimate lakehouse-trigger (Rule 2) |
| Legal facets (`criteria_license`, `reference_license`, `socio_data_license`, `outreach_consent`, `privilege_protocol`, `recoupment_law_matrix`, `fa_501r_review`, `baa_program`) | The signed artifact exists and covers programmatic use | Contract amendments, counsel memos, consent-capture flows | Entirely contractual — budget negotiation time, not software |

---

## 7. Worked example — the Epic-shop shortcut map

For a single-instance Epic organization, the honest starting position before buying anything:

- **Likely already at 2 (score, don't build):** `clinical_structured`, `charge_linkage`,
  `prebill_hold`, `cds_ordering_hook`, `queue_api`, `writeback` (with Interconnect licensed),
  much of `touch_logging`, `mspq_structured`/`auth_structured` (if configured), RTE/ERA
  connectivity for major payers.
- **Configuration/process projects (weeks):** `acks_retained`, `posting_standardized`,
  `takeback_linkage`, `card_images` compliance, `gfe_stored`, `bank_feeds`, `filing_matrix`.
- **Governance/contract projects (weeks–months, zero platform):** `notes_access` approval,
  `portal_automation_permitted`, all license facets, `um_worksheets` export rights,
  `statement_suppression` amendment.
- **True builds:** `denial_labels` attribution, `policy_library`, `citation_harness`,
  `golden_sets`, `fabric`, `account_360`, `contract_engine_loaded` *verification*.
- **Lakehouse-trigger check (Rule 2):** usually fires only for the label pipeline at auditor
  grade + the non-EHR archives — a *scoped* platform footprint, adopted for those workloads,
  not as a prerequisite for the portfolio.

The pattern to notice: **most of the portfolio's readiness gap at an Epic shop is approvals,
contracts, capture discipline, and a handful of genuine builds — not data-platform
procurement.** Vendors selling the reverse order are selling their margin, not your roadmap.

## 8. Maintenance

This layer decays fastest of any document in the stack (product names, packaging, payer APIs).
Refresh triggers: EHR major-version upgrades, clearinghouse changes, any Rule-2 trigger firing,
and the annual audit sweep (file 13). Corrections follow the same true-up discipline as every
driver file: commit with a note, and record which facet score the correction changed.
