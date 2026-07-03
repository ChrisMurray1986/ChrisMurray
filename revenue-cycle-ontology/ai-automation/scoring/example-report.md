# Feasibility scoring report — Example Regional Health (fictional)

Assessed by RCM automation working group on 2026-07-03. 99 use cases scored.

## Portfolio summary

| Disposition | Count |
|---|---|
| GO | 0 |
| CONDITIONAL | 43 |
| DEFER | 56 |
| KILL | 0 |

Insight-only (A0/A1) downgrade available for **44** of the blocked/conditional use cases.

## Dimension scores

| data | integration | connectivity | workflow | org | governance | economics | legal |
|---|---|---|---|---|---|---|---|
| 3 | 3 | 2 | 2 | 2 | 1 | 2 | 1 |

## Highest-leverage remediations

Blocking items ranked by number of use cases they hold back (sole-blocker count in parentheses):

- **dimension governance>=2** — blocks 64 use case(s) (7 solely)
- **dimension workflow>=3** — blocks 49 use case(s) (0 solely)
- **dimension governance>=3** — blocks 34 use case(s) (1 solely)
- **dimension legal>=2** — blocks 32 use case(s) (0 solely)
- **dimension data>=4** — blocks 30 use case(s) (0 solely)
- **dimension connectivity>=3** — blocks 9 use case(s) (0 solely)
- **facet fabric** — blocks 9 use case(s) (0 solely)
- **facet portal_automation_permitted** — blocks 7 use case(s) (0 solely)
- **facet citation_harness** — blocks 7 use case(s) (0 solely)
- **dimension integration>=4** — blocks 7 use case(s) (0 solely)
- **facet notes_access** — blocks 7 use case(s) (0 solely)
- **dimension legal>=3** — blocks 7 use case(s) (0 solely)
- **facet denial_labels** — blocks 6 use case(s) (0 solely)
- **facet contract_engine_loaded** — blocks 4 use case(s) (0 solely)
- **facet touch_logging** — blocks 4 use case(s) (0 solely)

## Per-use-case results

| UC | Name | Disposition | Gaps | A0/A1 start | Note |
|---|---|---|---|---|---|
| UC-01-02 | Identity resolution / dup MRN | CONDITIONAL | governance 1->2 | yes | Merge is always human (GOV-09) |
| UC-01-04 | Eligibility orchestration | CONDITIONAL | workflow 2->3; governance 1->2; legal 1->2; portal_automation_permitted (partial) | yes | RTE enrollment campaign; scope-cut payers with no electronic path |
| UC-01-06 | COB/MSP primacy inference | CONDITIONAL | governance 1->2 | yes | Capture-first if MSPQ is paper-only |
| UC-01-11 | Necessity screening & dx assist | CONDITIONAL | governance 1->2; legal 1->2; cds_ordering_hook (partial); provider_adoption (partial) | yes | Post-hoc screening loses most value — needs ordering-workflow hook |
| UC-01-15 | POS next-best-action | CONDITIONAL | governance 1->2; legal 1->2; collection_policy_unified (partial) | yes | Standardize collection policy across sites first |
| UC-02-02 | Criteria auto-abstraction | CONDITIONAL | governance 1->2; legal 1->2; notes_access (partial); criteria_license (partial) |  | Contractual gate: licensor must permit programmatic use |
| UC-02-04 | Auth-days runway monitor | CONDITIONAL | workflow 2->3; governance 1->2; auth_structured (partial) |  | Same structured-auth gate as UC-01-10 |
| UC-03-01 | Missing charge detection | CONDITIONAL | data 3->4; governance 1->2; charge_linkage (partial); dept_charge_owners (partial) |  | Kill per dept if no owner accepts the queue |
| UC-03-04 | Charge trigger surveillance | CONDITIONAL | governance 1->2 | yes | Low bar — Wave-1 candidate almost everywhere |
| UC-03-05 | CDM update automation | CONDITIONAL | workflow 2->3; governance 1->2 | yes | Defer if CDM changes happen by direct edit |
| UC-03-07 | Device/implant reconciliation | CONDITIONAL | governance 1->2; supply_chain_feed (partial) |  | Point-of-use capture project first if OR supplies are paper stickers |
| UC-03-08 | MRF/transparency pipeline | CONDITIONAL | governance 1->2; legal 1->2; contract_engine_loaded (partial) |  | Bad terms data automates noncompliance |
| UC-04-01 | CDI case prioritization | CONDITIONAL | data 3->4; governance 1->2; notes_access (partial) |  | Label backfill from encoder + query tool history |
| UC-04-02 | Evidence surfacing | CONDITIONAL | governance 1->2; notes_access (partial) |  | A0, low risk, feasible early |
| UC-04-05 | DRG reconciliation triage | CONDITIONAL | governance 1->2 | yes | Trivial where CDI+coding share a platform |
| UC-05-03 | Disposition validator | CONDITIONAL | governance 1->2 | yes | Rules-only version feasible everywhere; external signals need HIE |
| UC-05-04 | Deficiency chase automation | CONDITIONAL | governance 1->2 | yes | W2 the deficiency process first if ad hoc |
| UC-05-05 | Work distribution optimizer | CONDITIONAL | workflow 2->3; governance 1->2 | yes | Workflow-platform gap if queues are manual |
| UC-05-06 | QA sampling optimizer | CONDITIONAL | data 3->4; governance 1->2; qa_history (partial) |  | 1-2 quarters of structured QA capture if history is spreadsheets |
| UC-06-03 | Edit rule mining | CONDITIONAL | data 3->4; workflow 2->3; governance 1->2; denial_labels (partial) |  | Defer if edit rules are vendor-locked |
| UC-06-04 | Submission integrity reconciler | CONDITIONAL | workflow 2->3; governance 1->2 | yes | Turn on ack retention, then straightforward — Wave-1 |
| UC-06-06 | Timely filing sentinel | CONDITIONAL | workflow 2->3; governance 1->2; filing_matrix (partial) | yes | Contract-matrix load is the prerequisite |
| UC-06-07 | Attachment prediction/assembly | CONDITIONAL | data 3->4; governance 1->2; attachment_channels (partial) |  | Scope-cut fax-only payers |
| UC-07-02 | CARC mapping intelligence | CONDITIONAL | data 3->4; governance 1->2; denial_taxonomy (partial) |  | Without a taxonomy the model learns today's mis-mappings |
| UC-07-04 | Treasury matching | CONDITIONAL | governance 1->2 | yes | Straightforward where bank feeds exist |
| UC-07-05 | Variance detection coverage | CONDITIONAL | workflow 2->3; governance 1->2; contract_engine_loaded (partial) |  | No engine = that IS the project |
| UC-08-04 | Rebill-loop breaker | CONDITIONAL | workflow 2->3; governance 1->2; touch_logging (partial) |  | Instrumentation-first where touches aren't logged |
| UC-08-05 | Prevention insight miner | CONDITIONAL | data 3->4; workflow 2->3; governance 1->2; routing_authority (partial); denial_labels (partial) |  | Kill-as-designed without routing ownership |
| UC-09-03 | Underpayment pattern recovery | CONDITIONAL | workflow 2->3; governance 1->2; contract_engine_loaded (partial) |  | Cannot recover variances you cannot compute |
| UC-09-06 | Aged-AR disposition modeling | CONDITIONAL | data 3->4; workflow 2->3; governance 1->2; legal 1->2; placement_gates (partial) |  | Codify placement gates, then automate verification |
| UC-10-07 | Agency oversight analytics | CONDITIONAL | connectivity 2->3; governance 1->2; legal 1->2; agency_data_rights (partial) | yes | Renegotiate data/audit rights at vendor renewal |
| UC-10-08 | GFE variance monitor | CONDITIONAL | governance 1->2; legal 1->2; gfe_stored (partial) |  | Fix GFE storage discipline, then trivial rules |
| UC-11-02 | Amendment watchdog | CONDITIONAL | governance 1->2; contract_repository (partial) |  | Cheap once 07-03 and 11-01 exist |
| UC-11-04 | Credentialing/enrollment lifecycle | CONDITIONAL | connectivity 2->3; workflow 2->3; governance 1->2; legal 1->2; provider_master (partial); portal_automation_permitted (partial) |  | Exclusion monitoring can start immediately regardless |
| UC-11-05 | Payer scorecards & negotiation | CONDITIONAL | data 3->4; governance 1->2; touch_logging (partial) |  | Start claims-only; labor attribution matures with instrumentation |
| UC-12-06 | Extrapolation/exposure modeling | CONDITIONAL | governance 1->2; legal 1->2; privilege_protocol (partial); audit_outcomes (partial) |  | A discoverable exposure model is a self-inflicted wound |
| UC-13-01 | KPI anomaly narratives | CONDITIONAL | governance 1->2; kpi_dictionary (partial) | yes | Anomaly detection on ungoverned metrics is noise |
| UC-13-03 | Cash forecasting | CONDITIONAL | data 3->4; governance 1->2 |  | A0, low risk — Wave-2 |
| UC-14-01 | Payer/plan master intelligence | CONDITIONAL | data 3->4; workflow 2->3; governance 1->2; denial_labels (partial); masterdata_governance (partial) |  | Same governance logic as 03-05 |
| UC-14-02 | Master data drift monitoring | CONDITIONAL | governance 1->2; system_copy_extracts (partial) |  | Partial coverage disclosed, not silent |
| UC-14-03 | EDI pipeline observability (Wave-0) | CONDITIONAL | workflow 2->3; governance 1->2; edi_telemetry (partial) |  | Trivial data, high leverage |
| UC-14-05 | Automation candidate mining | CONDITIONAL | governance 1->2; touch_logging (partial) |  | Value scales with instrumentation coverage |
| UC-14-07 | Vendor performance analytics | CONDITIONAL | connectivity 2->3; governance 1->2; legal 1->2; agency_data_rights (partial) | yes | Defer per vendor to contract renewal if rights absent |
| UC-01-01 | Order intake document AI | DEFER | governance 1->3; golden_sets (absent) | yes | Defer if orders remain physical paper; kill if volume immaterial |
| UC-01-03 | Card OCR & plan mapping | DEFER | governance 1->3; data 3->4; denial_labels (partial); masterdata_governance (partial) |  | Fix payer master governance before training a mapper into it |
| UC-01-05 | Coverage discovery sweep | DEFER | governance 1->3 | yes | Monitor false-attach rate from day one |
| UC-01-07 | Auth requirement engine | DEFER | governance 1->3; connectivity 2->3; workflow 2->3; legal 1->2; bulletin_access (partial); portal_automation_permitted (partial) | yes | Stale grid worse than none — needs policy-monitoring feed |
| UC-01-08 | Auth submission agent | DEFER | fabric (absent); citation_harness (absent); integration 3->4; connectivity 2->3; workflow 2->3; governance 1->2; legal 1->2; auth_transactions (partial); notes_access (partial); portal_automation_permitted (partial) |  | Wave-0 fabric + GOV-03 harness prerequisites |
| UC-01-09 | Auth status tracking bots | DEFER | fabric (absent); connectivity 2->3; workflow 2->3; governance 1->2; legal 1->2; portal_automation_permitted (partial) | yes | Kill per payer segment if ToS prohibits with no 278/API alternative |
| UC-01-10 | Auth-to-service reconciliation | DEFER | governance 1->3; workflow 2->3; auth_structured (partial) |  | Structure auth capture first if details live in notes |
| UC-01-12 | Estimate accuracy engine | DEFER | governance 1->3; data 3->4; legal 1->2; contract_engine_loaded (partial) |  | Estimates without loaded contract terms are fiction |
| UC-01-13 | Clearance risk scoring | DEFER | governance 1->3; clearance_outcomes (absent); data 3->4; workflow 2->3; hitl_capacity (partial) |  | Deferral recommendations stay A1 forever (GOV-09) |
| UC-01-14 | Conversational pre-registration | DEFER | legal 1->3; workflow 2->3; governance 1->2; outreach_consent (partial); escalation_staffed (partial) | yes | Kill without staffed human escalation coverage |
| UC-01-16 | Real-time registration QA | DEFER | governance 1->3; data 3->4; denial_labels (partial) |  | Rules-only version can start at D3 |
| UC-01-17 | No-show revenue protection | DEFER | legal 1->3; data 3->4; governance 1->2; outreach_consent (partial) |  | Kill for low-volume lines; pool with UC-01-14 infrastructure |
| UC-02-01 | Admission status prediction | DEFER | governance 1->3; data 3->4 |  | Defer if clinical data is text-only |
| UC-02-03 | Payer notification/submission bots | DEFER | governance 1->3; connectivity 2->3; workflow 2->3; legal 1->2; portal_automation_permitted (partial) | yes | Scope-cut to payers with viable channels |
| UC-02-05 | Avoidable-day classification | DEFER | avoidable_day_taxonomy (absent); governance 1->2; notes_access (partial) |  | Define the taxonomy first |
| UC-03-02 | Dup/anomaly charge screening | DEFER | governance 1->3; workflow 2->3 | yes | Downgrade to post-bill lists without pre-bill hold |
| UC-03-03 | Drug units validator | DEFER | governance 1->3; workflow 2->3; masterdata_governance (partial) | yes | Govern the NDC crosswalk table first |
| UC-03-06 | Autonomous charging | DEFER | workflow 2->4; governance 1->3; data 3->4; documentation_stability (partial) |  | Enable domain-by-domain; capture-first where documentation incomplete |
| UC-04-03 | Compliant query drafting | DEFER | citation_harness (absent); workflow 2->3; governance 1->2 | yes | Standardize the human query process first |
| UC-04-04 | HCC suspecting & recapture | DEFER | governance 1->3; data 3->4; legal 1->2; notes_access (partial); provider_adoption (partial) |  | Kill if no VBC/MA population |
| UC-05-01 | Autonomous/assisted coding | DEFER | governance 1->3; golden_sets (absent); model_monitoring (absent); data 3->4; workflow 2->3; legal 1->2; notes_access (partial) |  | Scope by case type; never kill wholesale |
| UC-05-02 | DRG risk scoring | DEFER | governance 1->3; data 3->4; audit_outcomes (partial); hitl_capacity (partial) |  | Instrument audit outcomes first if unrecorded |
| UC-05-07 | Edit/denial coding assist | DEFER | citation_harness (absent); governance 1->2; legal 1->2; reference_license (partial) | yes | License rights for programmatic reference use |
| UC-06-01 | Denial risk scoring | DEFER | governance 1->3; data 3->4; workflow 2->3; denial_labels (partial) |  | Pilot A0 score display while hold policy is negotiated |
| UC-06-02 | Edit resolution agent | DEFER | governance 1->3; fabric (absent); integration 3->4; workflow 2->3 | yes | A3 only per governed class |
| UC-06-05 | Rejection auto-repair | DEFER | governance 1->3; fabric (absent); integration 3->4; workflow 2->3 | yes | A1 first, same pattern as 06-02 |
| UC-06-08 | COB/secondary automation | DEFER | governance 1->3; workflow 2->3 | yes | UC-07-03 feeds this for paper-remit payers |
| UC-07-01 | Intelligent auto-posting | DEFER | governance 1->3; workflow 2->3 | yes | ERA/EFT enrollment campaign first if paper-heavy |
| UC-07-03 | Paper EOB/correspondence IDP | DEFER | governance 1->3; golden_sets (absent) | yes | Switch lockbox to imaging service (contract change) |
| UC-07-06 | Recoupment validation | DEFER | recoupment_law_matrix (absent); governance 1->2; legal 1->2; takeback_linkage (partial) |  | Linkage repair in posting rules |
| UC-08-01 | Denial classification & attribution | DEFER | governance 1->3; denial_taxonomy (partial) | yes | Paper-denial capture gap = silent coverage hole |
| UC-08-02 | Overturn/priority scoring | DEFER | governance 1->3; appeal_outcomes (absent); data 3->4; workflow 2->3 |  | Interim: rules-based deadline x dollars prioritization |
| UC-08-03 | Appeal letter/packet generation | DEFER | policy_library (absent); citation_harness (absent); workflow 2->3; governance 1->2; legal 1->2; hitl_capacity (partial); appeal_process (partial) |  | LLM citing policies it can't retrieve is FM-AI-02 by design |
| UC-08-06 | Appeal outcome verification | DEFER | appeal_outcomes (absent); governance 1->2 |  | Low bar once 08-01/02 exist |
| UC-09-01 | Expected-value AR prioritization | DEFER | governance 1->3; ranked_list_adoption (absent); data 3->4; workflow 2->3; org 2->3; touch_logging (partial) |  | Adoption, not the model, is the usual blocker |
| UC-09-02 | Claim status bot fleet | DEFER | fabric (absent); workflow 2->3; governance 1->2; legal 1->2; claim_status_edi (partial); portal_automation_permitted (partial) | yes | A4 gated on fleet observability |
| UC-09-04 | Credit balance & refund automation | DEFER | governance 1->3; data 3->4; workflow 2->3; legal 1->2; ap_refund_path (partial) |  | Classification early; execution gated on AP integration |
| UC-09-05 | Special-account monitoring | DEFER | external_registries (absent); connectivity 2->3; workflow 2->3; governance 1->2; legal 1->2 | yes | Auto-stop on bankruptcy is the first release |
| UC-10-01 | Liability verification gate | DEFER | governance 1->3; workflow 2->3; legal 1->2; statement_suppression (partial) | yes | Vendor/contract change first if no suppression hook |
| UC-10-02 | Statement optimization | DEFER | governance 1->3; legal 1->3; bias_program (absent); data 3->4; statement_vendor_flex (partial); statement_history (partial) |  | Treatment differences must not track protected classes |
| UC-10-03 | Conversational billing agent | DEFER | governance 1->3; legal 1->3; account_360 (absent); workflow 2->3; plan_matrix_unified (partial); escalation_staffed (partial) | yes | A bot that can't explain the bill is a complaint generator |
| UC-10-04 | Plan default prediction & rescue | DEFER | governance 1->3; legal 1->3; bias_program (absent); data 3->4; outreach_consent (partial) |  | Consent capture in plan enrollment flow |
| UC-10-05 | Presumptive FA scoring | DEFER | governance 1->4; legal 1->3; bias_program (absent); socio_data_license (absent); data 3->4; workflow 2->3 |  | Cap at A0 lists until bias program; auto-denial killed permanently |
| UC-10-06 | NSA protection classifier | DEFER | governance 1->3; legal 1->3; consents_indexed (absent); workflow 2->3 |  | Index NSA consents first; err-protective default |
| UC-11-01 | Contract extraction & load verify | DEFER | citation_harness (absent); governance 1->2; contract_repository (partial) |  | Repository assembly is the prerequisite (valuable alone) |
| UC-11-03 | Policy monitoring & routing | DEFER | citation_harness (absent); connectivity 2->3; workflow 2->3; governance 1->2; legal 1->2; routing_authority (partial); bulletin_access (partial) | yes | Unrouted intelligence is shelfware |
| UC-11-06 | VBC settlement validation | DEFER | vbc_data_sharing (absent); data 3->4; governance 1->2; legal 1->2 |  | Kill if no VBC book |
| UC-12-01 | Audit intake & deadline mgmt | DEFER | governance 1->3; workflow 2->3; legal 1->2; audit_channels_digitized (partial); audit_workflow (partial) |  | One missed channel defeats the purpose |
| UC-12-02 | Audit packet assembly | DEFER | fabric (absent); integration 3->4; workflow 2->3; governance 1->2; legal 1->2; him_retrieval (partial) | yes | Manual-pull residual quantified |
| UC-12-03 | Billing pattern surveillance | DEFER | peer_benchmarks (absent); governance 1->2; legal 1->2; compliance_charter (partial) |  | Leads, not verdicts (GOV-09) |
| UC-12-04 | Overpayment register & 60-day | DEFER | governance 1->3; workflow 2->3; legal 1->2; ap_refund_path (partial); audit_workflow (partial) | yes | Source-feed completeness is the whole point |
| UC-12-05 | Regulatory change intelligence | DEFER | citation_harness (absent); workflow 2->3; governance 1->2; routing_authority (partial) | yes | Same kill condition as 11-03 |
| UC-13-02 | Reserve/net-revenue models | DEFER | governance 1->3; lineage (absent); data 3->4; legal 1->2 |  | Shadow-run >=2 closes before reliance |
| UC-13-04 | Governance telemetry (Wave-0) | DEFER | fabric (absent); integration 3->4; workflow 2->3; governance 1->2; gov_body (partial) | yes | Every A3+ UC depends on it — build before scaling past A1 |
| UC-14-04 | Bot fleet observability (Wave-0) | DEFER | fabric (absent); handback_queues (absent); integration 3->4; workflow 2->3; governance 1->2 | yes | Hard prerequisite for any A4 RPA |
| UC-14-06 | Downtime orchestration | DEFER | fabric (absent); integration 3->4; workflow 2->3; governance 1->2; downtime_procedures (partial) | yes | Write and drill the checklist before orchestrating it |
