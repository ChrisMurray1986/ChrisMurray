# Value model — Meridian Health (simulated)

Profile date 2026-07-03; NPR $2.40B. 99 use cases valued. All figures annual steady-state unless noted; pool-capped (extraction limit applied); risk value (VS-8) segregated.

## Portfolio totals

| Measure | Value |
|---|---|
| Recurring value, base case (capped) | **$96.9M** |
| Recurring range (low–high) | $48.4M – $155.0M |
| One-time cash release (AR days) | $38.1M |
| Risk & compliance EV (VS-8, segregated) | $3.1M |
| Year-1 value, disposition-adjusted | $15.4M |

## By value stream (recurring, capped, base case)

| Stream | Annual value |
|---|---|
| VS-1 Revenue protected | $22.0M |
| VS-2 Revenue recovered | $17.8M |
| VS-3 Revenue captured | $28.9M |
| VS-4 Patient cash yield | $6.5M |
| VS-5 Cash acceleration | $2.3M |
| VS-6 Labor productivity | $16.3M |
| VS-7 External cost reduction | $3.0M |
| VS-8 Risk & compliance (segregated) | $3.1M |

## Value locked by gate (steady-state $ held back per blocking item)

Overlapping attribution — a use case with three gaps appears under all three; this prices gates, it does not sum to the portfolio.

| Blocking item | UCs | Locked value |
|---|---|---|
| governance 1->2 | 64 | $61.6M |
| workflow 2->3 | 49 | $48.2M |
| data 3->4 | 30 | $37.4M |
| governance 1->3 | 34 | $34.8M |
| notes_access | 11 | $17.3M |
| citation_harness | 7 | $10.0M |
| contract_engine_loaded | 4 | $9.7M |
| golden_sets | 7 | $9.5M |
| portal_automation_permitted | 7 | $8.6M |
| denial_labels | 6 | $8.2M |
| dept_charge_owners | 1 | $6.0M |
| fabric | 9 | $5.8M |
| legal 2->3 | 7 | $5.2M |
| policy_library | 3 | $4.3M |
| contract_repository | 2 | $4.1M |

## Pool utilization

| Pool | Sized at | Claimed | Cap | Scaled down |
|---|---|---|---|---|
| denial_prevention | $25.9M | 89% | 85% | yes |
| denial_recovery | $6.0M | 53% | 85% |  |
| underpayment | $19.2M | 76% | 85% |  |
| charge_capture | $24.0M | 68% | 85% |  |
| doc_yield | $12.0M | 50% | 85% |  |
| coverage_conversion | $9.6M | 35% | 85% |  |
| contract_yield | $7.2M | 45% | 85% |  |
| pos_yield | $4.8M | 73% | 85% |  |
| bad_debt_reduction | $7.2M | 41% | 85% |  |
| ar_days | $395k/day-yr + $6.6M/day one-time | 5.8 days | 6.8 days |  |
| labor_access | $8.4M | 38% | 85% |  |
| labor_um_cdi | $3.3M | 39% | 85% |  |
| labor_coding | $5.0M | 44% | 85% |  |
| labor_billing | $3.8M | 31% | 85% |  |
| labor_posting | $2.5M | 68% | 85% |  |
| labor_denials | $4.2M | 38% | 85% |  |
| labor_ar | $5.8M | 45% | 85% |  |
| labor_pfs | $4.6M | 30% | 85% |  |
| labor_analytics | $2.1M | 42% | 85% |  |
| labor_contracting | $2.1M | 15% | 85% |  |
| cost_external | $14.4M | 21% | 85% |  |
| audit_risk | $3.6M | 115% | 85% | yes |

## Per-use-case value (sorted by base case)

| UC | Domain | Streams | Low | Base | High | One-time | Risk EV | Dispo | Year-1 |
|---|---|---|---|---|---|---|---|---|---|
| UC-03-01 | Charge Capture | VS-3 | $3.0M | **$6.0M** | $9.6M | — | — | CONDITIONAL | $1.5M |
| UC-07-05 | Payments | VS-2 | $2.4M | **$4.8M** | $7.7M | — | — | CONDITIONAL | $1.2M |
| UC-01-05 | Patient Access | VS-3 VS-4 | $2.0M | **$4.1M** | $6.5M | — | — | DEFER | $612k |
| UC-09-03 | AR Management | VS-2 | $1.9M | **$3.8M** | $6.1M | — | — | CONDITIONAL | $960k |
| UC-03-06 | Charge Capture | VS-3 VS-6 | $1.9M | **$3.7M** | $5.9M | — | — | DEFER | $0k |
| UC-11-01 | Contracting | VS-1 VS-2 | $1.6M | **$3.1M** | $5.0M | — | — | DEFER | $0k |
| UC-08-05 | Denials & Appeals | VS-1 | $1.2M | **$2.5M** | $4.0M | — | — | CONDITIONAL | $619k |
| UC-03-04 | Charge Capture | VS-3 | $1.2M | **$2.4M** | $3.8M | — | — | CONDITIONAL | $600k |
| UC-04-01 | CDI | VS-3 | $1.2M | **$2.4M** | $3.8M | — | — | CONDITIONAL | $600k |
| UC-08-03 | Denials & Appeals | VS-2 VS-6 | $1.2M | **$2.3M** | $3.8M | — | — | DEFER | $0k |
| UC-11-05 | Contracting | VS-3 | $1.1M | **$2.2M** | $3.5M | — | — | CONDITIONAL | $540k |
| UC-06-01 | Claims | VS-1 | $990k | **$2.0M** | $3.2M | — | — | DEFER | $0k |
| UC-05-01 | Coding | VS-1 VS-5 VS-6 | $974k | **$1.9M** | $3.1M | $3.3M | — | DEFER | $0k |
| UC-03-07 | Charge Capture | VS-3 | $960k | **$1.9M** | $3.1M | — | — | CONDITIONAL | $480k |
| UC-09-02 | AR Management | VS-5 VS-6 | $829k | **$1.7M** | $2.7M | $3.3M | — | CONDITIONAL | $415k |
| UC-11-06 | Contracting | VS-2 VS-3 | $828k | **$1.7M** | $2.6M | — | — | CONDITIONAL | $414k |
| UC-09-01 | AR Management | VS-4 VS-5 VS-6 | $816k | **$1.6M** | $2.6M | $6.6M | — | DEFER | $0k |
| UC-01-04 | Patient Access | VS-1 VS-5 VS-6 | $805k | **$1.6M** | $2.6M | $2.0M | — | CONDITIONAL | $402k |
| UC-01-07 | Patient Access | VS-1 | $743k | **$1.5M** | $2.4M | — | — | DEFER | $223k |
| UC-01-08 | Patient Access | VS-1 VS-6 | $705k | **$1.4M** | $2.3M | — | — | DEFER | $0k |
| UC-01-16 | Patient Access | VS-1 VS-6 | $702k | **$1.4M** | $2.2M | — | — | DEFER | $0k |
| UC-10-03 | Patient Financial Svcs | VS-4 VS-6 | $694k | **$1.4M** | $2.2M | — | — | DEFER | $208k |
| UC-04-02 | CDI | VS-3 VS-6 | $684k | **$1.4M** | $2.2M | — | — | CONDITIONAL | $342k |
| UC-01-14 | Patient Access | VS-4 VS-6 | $658k | **$1.3M** | $2.1M | — | — | CONDITIONAL | $329k |
| UC-04-03 | CDI | VS-3 VS-6 | $650k | **$1.3M** | $2.1M | — | — | DEFER | $0k |
| UC-11-03 | Contracting | VS-1 | $619k | **$1.2M** | $2.0M | — | — | DEFER | $186k |
| UC-03-03 | Charge Capture | VS-3 VS-8 | $600k | **$1.2M** | $1.9M | — | $266k | DEFER | $180k |
| UC-04-04 | CDI | VS-3 | $600k | **$1.2M** | $1.9M | — | — | DEFER | $0k |
| UC-11-04 | Contracting | VS-1 VS-5 VS-6 | $587k | **$1.2M** | $1.9M | $2.0M | — | CONDITIONAL | $294k |
| UC-10-07 | Patient Financial Svcs | VS-7 VS-8 | $576k | **$1.2M** | $1.8M | — | $53k | CONDITIONAL | $288k |
| UC-10-02 | Patient Financial Svcs | VS-4 VS-7 | $552k | **$1.1M** | $1.8M | — | — | DEFER | $0k |
| UC-01-12 | Patient Access | VS-4 | $540k | **$1.1M** | $1.7M | — | — | DEFER | $0k |
| UC-01-10 | Patient Access | VS-1 | $495k | **$990k** | $1.6M | — | — | DEFER | $149k |
| UC-06-03 | Claims | VS-1 | $495k | **$990k** | $1.6M | — | — | CONDITIONAL | $248k |
| UC-07-06 | Payments | VS-2 | $480k | **$960k** | $1.5M | — | — | CONDITIONAL | $240k |
| UC-11-02 | Contracting | VS-2 | $480k | **$960k** | $1.5M | — | — | CONDITIONAL | $240k |
| UC-07-01 | Payments | VS-5 VS-6 | $478k | **$956k** | $1.5M | $1.3M | — | DEFER | $143k |
| UC-08-02 | Denials & Appeals | VS-2 VS-6 | $469k | **$939k** | $1.5M | — | — | DEFER | $0k |
| UC-02-03 | Utilization Review | VS-1 VS-6 | $415k | **$829k** | $1.3M | — | — | DEFER | $0k |
| UC-01-03 | Patient Access | VS-1 VS-6 | $413k | **$826k** | $1.3M | — | — | DEFER | $0k |
| UC-10-04 | Patient Financial Svcs | VS-4 | $408k | **$816k** | $1.3M | — | — | DEFER | $0k |
| UC-06-05 | Claims | VS-1 VS-6 | $398k | **$796k** | $1.3M | — | — | DEFER | $119k |
| UC-06-02 | Claims | VS-5 VS-6 | $381k | **$761k** | $1.2M | $3.3M | — | DEFER | $114k |
| UC-01-06 | Patient Access | VS-1 | $371k | **$743k** | $1.2M | — | — | CONDITIONAL | $186k |
| UC-02-01 | Utilization Review | VS-1 | $371k | **$743k** | $1.2M | — | — | DEFER | $0k |
| UC-06-06 | Claims | VS-1 | $371k | **$743k** | $1.2M | — | — | CONDITIONAL | $186k |
| UC-01-13 | Patient Access | VS-4 VS-6 | $365k | **$731k** | $1.2M | — | — | DEFER | $0k |
| UC-01-15 | Patient Access | VS-4 | $360k | **$720k** | $1.2M | — | — | CONDITIONAL | $180k |
| UC-03-02 | Charge Capture | VS-3 VS-8 | $360k | **$720k** | $1.2M | — | $133k | DEFER | $108k |
| UC-08-01 | Denials & Appeals | VS-2 VS-6 | $360k | **$720k** | $1.2M | — | — | DEFER | $108k |
| UC-14-07 | Master Data & Tech | VS-7 | $360k | **$720k** | $1.2M | — | — | CONDITIONAL | $180k |
| UC-02-02 | Utilization Review | VS-2 VS-6 | $341k | **$683k** | $1.1M | — | — | CONDITIONAL | $171k |
| UC-06-07 | Claims | VS-1 VS-5 | $326k | **$653k** | $1.0M | $2.6M | — | CONDITIONAL | $163k |
| UC-06-04 | Claims | VS-1 VS-5 | $307k | **$613k** | $982k | $2.0M | — | CONDITIONAL | $153k |
| UC-10-01 | Patient Financial Svcs | VS-4 VS-6 | $295k | **$590k** | $943k | — | — | DEFER | $88k |
| UC-05-03 | Coding | VS-2 VS-8 | $288k | **$576k** | $922k | — | $53k | CONDITIONAL | $144k |
| UC-14-03 | Master Data & Tech | VS-1 VS-5 | $287k | **$574k** | $918k | $1.3M | — | CONDITIONAL | $144k |
| UC-09-06 | AR Management | VS-4 VS-6 | $268k | **$535k** | $857k | — | — | CONDITIONAL | $134k |
| UC-14-06 | Master Data & Tech | VS-3 VS-5 | $260k | **$519k** | $831k | $658k | — | CONDITIONAL | $130k |
| UC-01-11 | Patient Access | VS-1 VS-8 | $248k | **$495k** | $792k | — | $53k | CONDITIONAL | $124k |
| UC-02-04 | Utilization Review | VS-1 | $248k | **$495k** | $792k | — | — | CONDITIONAL | $124k |
| UC-05-02 | Coding | VS-1 VS-8 | $248k | **$495k** | $792k | — | $213k | DEFER | $0k |
| UC-14-01 | Master Data & Tech | VS-1 | $248k | **$495k** | $792k | — | — | CONDITIONAL | $124k |
| UC-03-05 | Charge Capture | VS-1 VS-6 | $238k | **$476k** | $761k | — | — | CONDITIONAL | $119k |
| UC-07-03 | Payments | VS-5 VS-6 | $227k | **$455k** | $728k | $1.3M | — | DEFER | $68k |
| UC-10-05 | Patient Financial Svcs | VS-7 VS-8 | $216k | **$432k** | $691k | — | $53k | DEFER | $0k |
| UC-01-09 | Patient Access | VS-6 | $209k | **$418k** | $668k | — | — | CONDITIONAL | $104k |
| UC-01-01 | Patient Access | VS-1 VS-6 | $207k | **$415k** | $663k | — | — | DEFER | $62k |
| UC-06-08 | Claims | VS-5 VS-6 | $193k | **$385k** | $616k | $3.3M | — | DEFER | $58k |
| UC-05-07 | Coding | VS-2 VS-6 | $161k | **$321k** | $514k | — | — | DEFER | $48k |
| UC-08-06 | Denials & Appeals | VS-2 | $151k | **$302k** | $484k | — | — | CONDITIONAL | $76k |
| UC-05-04 | Coding | VS-5 VS-6 | $149k | **$297k** | $476k | $3.3M | — | CONDITIONAL | $74k |
| UC-05-05 | Coding | VS-6 | $125k | **$251k** | $401k | — | — | CONDITIONAL | $63k |
| UC-09-04 | AR Management | VS-6 VS-8 | $125k | **$251k** | $401k | — | $133k | DEFER | $0k |
| UC-12-05 | Compliance | VS-1 VS-8 | $124k | **$248k** | $396k | — | $133k | DEFER | $37k |
| UC-14-02 | Master Data & Tech | VS-1 VS-8 | $124k | **$248k** | $396k | — | $27k | CONDITIONAL | $62k |
| UC-08-04 | Denials & Appeals | VS-5 VS-6 | $118k | **$235k** | $376k | $2.0M | — | CONDITIONAL | $59k |
| UC-09-05 | AR Management | VS-4 VS-8 | $108k | **$216k** | $346k | — | $53k | DEFER | $32k |
| UC-13-01 | Analytics | VS-6 | $104k | **$209k** | $334k | — | — | CONDITIONAL | $52k |
| UC-01-02 | Patient Access | VS-1 VS-6 | $104k | **$207k** | $332k | — | — | CONDITIONAL | $52k |
| UC-07-04 | Payments | VS-6 | $100k | **$200k** | $321k | — | — | CONDITIONAL | $50k |
| UC-07-02 | Payments | VS-2 | $91k | **$181k** | $290k | — | — | CONDITIONAL | $45k |
| UC-13-02 | Analytics | VS-6 VS-8 | $84k | **$167k** | $267k | — | $27k | DEFER | $0k |
| UC-05-06 | Coding | VS-6 VS-8 | $75k | **$150k** | $241k | — | $80k | CONDITIONAL | $38k |
| UC-01-17 | Patient Access | VS-4 | $72k | **$144k** | $230k | — | — | CONDITIONAL | $36k |
| UC-12-02 | Compliance | VS-6 VS-8 | $52k | **$104k** | $167k | — | $266k | CONDITIONAL | $26k |
| UC-14-05 | Master Data & Tech | VS-6 | $52k | **$104k** | $167k | — | — | CONDITIONAL | $26k |
| UC-02-05 | Utilization Review | VS-6 | $50k | **$100k** | $160k | — | — | CONDITIONAL | $25k |
| UC-04-05 | CDI | VS-6 | $50k | **$100k** | $160k | — | — | CONDITIONAL | $25k |
| UC-10-08 | Patient Financial Svcs | VS-4 VS-8 | $48k | **$96k** | $154k | — | $27k | CONDITIONAL | $24k |
| UC-13-03 | Analytics | VS-6 | $31k | **$63k** | $100k | — | — | CONDITIONAL | $16k |
| UC-13-04 | Analytics | VS-6 VS-8 | $31k | **$63k** | $100k | — | $80k | CONDITIONAL | $16k |
| UC-14-04 | Master Data & Tech | VS-6 VS-8 | $31k | **$63k** | $100k | — | $27k | CONDITIONAL | $16k |
| UC-03-08 | Charge Capture | VS-8 | $0k | **$0k** | $0k | — | $53k | CONDITIONAL | $0k |
| UC-10-06 | Patient Financial Svcs | VS-8 | $0k | **$0k** | $0k | — | $133k | DEFER | $0k |
| UC-12-01 | Compliance | VS-8 | $0k | **$0k** | $0k | — | $399k | DEFER | $0k |
| UC-12-03 | Compliance | VS-8 | $0k | **$0k** | $0k | — | $266k | CONDITIONAL | $0k |
| UC-12-04 | Compliance | VS-8 | $0k | **$0k** | $0k | — | $399k | DEFER | $0k |
| UC-12-06 | Compliance | VS-8 | $0k | **$0k** | $0k | — | $133k | CONDITIONAL | $0k |

Measurement designs per stream: 09-value-model.md §4. Recalibrate draw shares quarterly against realized value (true-up rule).
