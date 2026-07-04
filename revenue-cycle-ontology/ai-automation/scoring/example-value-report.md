# Value model — Example Regional Health (fictional)

Profile date 2026-07-03; NPR $1.00B. 99 use cases valued. All figures annual steady-state unless noted; pool-capped (extraction limit applied); risk value (VS-8) segregated.

## Portfolio totals

| Measure | Value |
|---|---|
| Recurring value, base case (capped) | **$42.2M** |
| Recurring range (low–high) | $21.1M – $67.6M |
| One-time cash release (AR days) | $15.9M |
| Risk & compliance EV (VS-8, segregated) | $1.3M |
| Year-1 value, disposition-adjusted | $5.9M |

## By value stream (recurring, capped, base case)

| Stream | Annual value |
|---|---|
| VS-1 Revenue protected | $10.2M |
| VS-2 Revenue recovered | $7.6M |
| VS-3 Revenue captured | $12.1M |
| VS-4 Patient cash yield | $2.7M |
| VS-5 Cash acceleration | $953k |
| VS-6 Labor productivity | $7.5M |
| VS-7 External cost reduction | $1.3M |
| VS-8 Risk & compliance (segregated) | $1.3M |

## Value locked by gate (steady-state $ held back per blocking item)

Overlapping attribution — a use case with three gaps appears under all three; this prices gates, it does not sum to the portfolio.

| Blocking item | UCs | Locked value |
|---|---|---|
| governance 1->2 | 64 | $26.7M |
| workflow 2->3 | 49 | $21.5M |
| data 3->4 | 30 | $16.2M |
| governance 1->3 | 34 | $15.3M |
| legal 1->2 | 32 | $11.2M |
| notes_access | 11 | $7.5M |
| citation_harness | 7 | $4.4M |
| golden_sets | 7 | $4.2M |
| contract_engine_loaded | 4 | $4.0M |
| portal_automation_permitted | 7 | $3.9M |
| connectivity 2->3 | 9 | $3.9M |
| denial_labels | 6 | $3.8M |
| fabric | 9 | $2.6M |
| charge_linkage | 1 | $2.5M |
| dept_charge_owners | 1 | $2.5M |

## Pool utilization

| Pool | Sized at | Claimed | Cap | Scaled down |
|---|---|---|---|---|
| denial_prevention | $12.0M | 89% | 85% | yes |
| denial_recovery | $2.8M | 53% | 85% |  |
| underpayment | $8.0M | 76% | 85% |  |
| charge_capture | $10.0M | 68% | 85% |  |
| doc_yield | $5.0M | 50% | 85% |  |
| coverage_conversion | $4.0M | 35% | 85% |  |
| contract_yield | $3.0M | 45% | 85% |  |
| pos_yield | $2.0M | 73% | 85% |  |
| bad_debt_reduction | $3.0M | 41% | 85% |  |
| ar_days | $164k/day-yr + $2.7M/day one-time | 5.8 days | 6.8 days |  |
| labor_access | $3.8M | 38% | 85% |  |
| labor_um_cdi | $1.5M | 39% | 85% |  |
| labor_coding | $2.3M | 44% | 85% |  |
| labor_billing | $1.7M | 31% | 85% |  |
| labor_posting | $1.2M | 68% | 85% |  |
| labor_denials | $1.9M | 38% | 85% |  |
| labor_ar | $2.7M | 45% | 85% |  |
| labor_pfs | $2.1M | 30% | 85% |  |
| labor_analytics | $960k | 42% | 85% |  |
| labor_contracting | $960k | 15% | 85% |  |
| cost_external | $6.0M | 21% | 85% |  |
| audit_risk | $1.5M | 115% | 85% | yes |

## Per-use-case value (sorted by base case)

| UC | Domain | Streams | Low | Base | High | One-time | Risk EV | Dispo | Year-1 |
|---|---|---|---|---|---|---|---|---|---|
| UC-03-01 | Charge Capture | VS-3 | $1.2M | **$2.5M** | $4.0M | — | — | CONDITIONAL | $625k |
| UC-07-05 | Payments | VS-2 | $1.0M | **$2.0M** | $3.2M | — | — | CONDITIONAL | $500k |
| UC-01-05 | Patient Access | VS-3 VS-4 | $850k | **$1.7M** | $2.7M | — | — | DEFER | $255k |
| UC-09-03 | AR Management | VS-2 | $800k | **$1.6M** | $2.6M | — | — | CONDITIONAL | $400k |
| UC-03-06 | Charge Capture | VS-3 VS-6 | $776k | **$1.6M** | $2.5M | — | — | DEFER | $0k |
| UC-11-01 | Contracting | VS-1 VS-2 | $657k | **$1.3M** | $2.1M | — | — | DEFER | $0k |
| UC-08-05 | Denials & Appeals | VS-1 | $573k | **$1.1M** | $1.8M | — | — | CONDITIONAL | $287k |
| UC-08-03 | Denials & Appeals | VS-2 VS-6 | $542k | **$1.1M** | $1.7M | — | — | DEFER | $0k |
| UC-03-04 | Charge Capture | VS-3 | $500k | **$1.0M** | $1.6M | — | — | CONDITIONAL | $250k |
| UC-04-01 | CDI | VS-3 | $500k | **$1.0M** | $1.6M | — | — | CONDITIONAL | $250k |
| UC-06-01 | Claims | VS-1 | $458k | **$917k** | $1.5M | — | — | DEFER | $0k |
| UC-11-05 | Contracting | VS-3 | $450k | **$900k** | $1.4M | — | — | CONDITIONAL | $225k |
| UC-05-01 | Coding | VS-1 VS-5 VS-6 | $444k | **$888k** | $1.4M | $1.4M | — | DEFER | $0k |
| UC-03-07 | Charge Capture | VS-3 | $400k | **$800k** | $1.3M | — | — | CONDITIONAL | $200k |
| UC-09-02 | AR Management | VS-5 VS-6 | $377k | **$754k** | $1.2M | $1.4M | — | DEFER | $113k |
| UC-01-04 | Patient Access | VS-1 VS-5 VS-6 | $369k | **$738k** | $1.2M | $822k | — | DEFER | $111k |
| UC-09-01 | AR Management | VS-4 VS-5 VS-6 | $359k | **$718k** | $1.1M | $2.7M | — | DEFER | $0k |
| UC-11-06 | Contracting | VS-2 VS-3 | $345k | **$690k** | $1.1M | — | — | DEFER | $0k |
| UC-01-07 | Patient Access | VS-1 | $344k | **$688k** | $1.1M | — | — | DEFER | $0k |
| UC-01-08 | Patient Access | VS-1 VS-6 | $326k | **$651k** | $1.0M | — | — | DEFER | $0k |
| UC-01-16 | Patient Access | VS-1 VS-6 | $325k | **$650k** | $1.0M | — | — | DEFER | $0k |
| UC-10-03 | Patient Financial Svcs | VS-4 VS-6 | $314k | **$628k** | $1.0M | — | — | DEFER | $94k |
| UC-01-14 | Patient Access | VS-4 VS-6 | $292k | **$584k** | $934k | — | — | DEFER | $88k |
| UC-04-02 | CDI | VS-3 VS-6 | $288k | **$577k** | $923k | — | — | CONDITIONAL | $144k |
| UC-11-03 | Contracting | VS-1 | $287k | **$573k** | $917k | — | — | DEFER | $86k |
| UC-04-03 | CDI | VS-3 VS-6 | $273k | **$546k** | $874k | — | — | DEFER | $0k |
| UC-11-04 | Contracting | VS-1 VS-5 VS-6 | $269k | **$537k** | $859k | $822k | — | CONDITIONAL | $134k |
| UC-03-03 | Charge Capture | VS-3 VS-8 | $250k | **$500k** | $800k | — | $111k | DEFER | $75k |
| UC-04-04 | CDI | VS-3 | $250k | **$500k** | $800k | — | — | DEFER | $0k |
| UC-10-07 | Patient Financial Svcs | VS-7 VS-8 | $240k | **$480k** | $768k | — | $22k | CONDITIONAL | $120k |
| UC-10-02 | Patient Financial Svcs | VS-4 VS-7 | $230k | **$460k** | $736k | — | — | DEFER | $0k |
| UC-01-10 | Patient Access | VS-1 | $229k | **$458k** | $733k | — | — | DEFER | $0k |
| UC-06-03 | Claims | VS-1 | $229k | **$458k** | $733k | — | — | CONDITIONAL | $115k |
| UC-01-12 | Patient Access | VS-4 | $225k | **$450k** | $720k | — | — | DEFER | $0k |
| UC-07-01 | Payments | VS-5 VS-6 | $218k | **$436k** | $698k | $548k | — | DEFER | $65k |
| UC-08-02 | Denials & Appeals | VS-2 VS-6 | $217k | **$434k** | $694k | — | — | DEFER | $0k |
| UC-07-06 | Payments | VS-2 | $200k | **$400k** | $640k | — | — | DEFER | $0k |
| UC-11-02 | Contracting | VS-2 | $200k | **$400k** | $640k | — | — | CONDITIONAL | $100k |
| UC-02-03 | Utilization Review | VS-1 VS-6 | $191k | **$383k** | $613k | — | — | DEFER | $0k |
| UC-01-03 | Patient Access | VS-1 VS-6 | $191k | **$382k** | $612k | — | — | DEFER | $0k |
| UC-06-05 | Claims | VS-1 VS-6 | $184k | **$367k** | $588k | — | — | DEFER | $55k |
| UC-01-06 | Patient Access | VS-1 | $172k | **$344k** | $550k | — | — | CONDITIONAL | $86k |
| UC-02-01 | Utilization Review | VS-1 | $172k | **$344k** | $550k | — | — | DEFER | $0k |
| UC-06-06 | Claims | VS-1 | $172k | **$344k** | $550k | — | — | CONDITIONAL | $86k |
| UC-06-02 | Claims | VS-5 VS-6 | $171k | **$341k** | $546k | $1.4M | — | DEFER | $51k |
| UC-10-04 | Patient Financial Svcs | VS-4 | $170k | **$340k** | $544k | — | — | DEFER | $0k |
| UC-08-01 | Denials & Appeals | VS-2 VS-6 | $166k | **$332k** | $531k | — | — | DEFER | $50k |
| UC-01-13 | Patient Access | VS-4 VS-6 | $158k | **$315k** | $504k | — | — | DEFER | $0k |
| UC-02-02 | Utilization Review | VS-2 VS-6 | $157k | **$314k** | $503k | — | — | CONDITIONAL | $79k |
| UC-01-15 | Patient Access | VS-4 | $150k | **$300k** | $480k | — | — | CONDITIONAL | $75k |
| UC-03-02 | Charge Capture | VS-3 VS-8 | $150k | **$300k** | $480k | — | $55k | DEFER | $45k |
| UC-14-07 | Master Data & Tech | VS-7 | $150k | **$300k** | $480k | — | — | CONDITIONAL | $75k |
| UC-06-07 | Claims | VS-1 VS-5 | $147k | **$295k** | $472k | $1.1M | — | CONDITIONAL | $74k |
| UC-06-04 | Claims | VS-1 VS-5 | $139k | **$279k** | $446k | $822k | — | CONDITIONAL | $70k |
| UC-14-03 | Master Data & Tech | VS-1 VS-5 | $131k | **$262k** | $419k | $548k | — | CONDITIONAL | $66k |
| UC-10-01 | Patient Financial Svcs | VS-4 VS-6 | $128k | **$256k** | $409k | — | — | DEFER | $38k |
| UC-05-03 | Coding | VS-2 VS-8 | $120k | **$240k** | $384k | — | $22k | CONDITIONAL | $60k |
| UC-09-06 | AR Management | VS-4 VS-6 | $115k | **$231k** | $369k | — | — | CONDITIONAL | $58k |
| UC-01-11 | Patient Access | VS-1 VS-8 | $115k | **$229k** | $367k | — | $22k | DEFER | $0k |
| UC-02-04 | Utilization Review | VS-1 | $115k | **$229k** | $367k | — | — | CONDITIONAL | $57k |
| UC-05-02 | Coding | VS-1 VS-8 | $115k | **$229k** | $367k | — | $89k | DEFER | $0k |
| UC-14-01 | Master Data & Tech | VS-1 | $115k | **$229k** | $367k | — | — | CONDITIONAL | $57k |
| UC-03-05 | Charge Capture | VS-1 VS-6 | $110k | **$220k** | $352k | — | — | CONDITIONAL | $55k |
| UC-14-06 | Master Data & Tech | VS-3 VS-5 | $108k | **$216k** | $346k | $274k | — | DEFER | $32k |
| UC-07-03 | Payments | VS-5 VS-6 | $103k | **$206k** | $329k | $548k | — | DEFER | $31k |
| UC-01-09 | Patient Access | VS-6 | $96k | **$192k** | $307k | — | — | DEFER | $29k |
| UC-01-01 | Patient Access | VS-1 VS-6 | $96k | **$191k** | $306k | — | — | DEFER | $29k |
| UC-10-05 | Patient Financial Svcs | VS-7 VS-8 | $90k | **$180k** | $288k | — | $22k | DEFER | $0k |
| UC-06-08 | Claims | VS-5 VS-6 | $84k | **$169k** | $270k | $1.4M | — | DEFER | $25k |
| UC-05-07 | Coding | VS-2 VS-6 | $74k | **$148k** | $237k | — | — | DEFER | $22k |
| UC-08-06 | Denials & Appeals | VS-2 | $70k | **$140k** | $224k | — | — | DEFER | $0k |
| UC-05-04 | Coding | VS-5 VS-6 | $64k | **$128k** | $205k | $1.4M | — | CONDITIONAL | $32k |
| UC-05-05 | Coding | VS-6 | $58k | **$115k** | $184k | — | — | CONDITIONAL | $29k |
| UC-09-04 | AR Management | VS-6 VS-8 | $58k | **$115k** | $184k | — | $55k | DEFER | $0k |
| UC-12-05 | Compliance | VS-1 VS-8 | $57k | **$115k** | $183k | — | $55k | DEFER | $17k |
| UC-14-02 | Master Data & Tech | VS-1 VS-8 | $57k | **$115k** | $183k | — | $11k | CONDITIONAL | $29k |
| UC-08-04 | Denials & Appeals | VS-5 VS-6 | $52k | **$103k** | $165k | $822k | — | CONDITIONAL | $26k |
| UC-13-01 | Analytics | VS-6 | $48k | **$96k** | $154k | — | — | CONDITIONAL | $24k |
| UC-01-02 | Patient Access | VS-1 VS-6 | $48k | **$96k** | $153k | — | — | CONDITIONAL | $24k |
| UC-07-04 | Payments | VS-6 | $46k | **$92k** | $147k | — | — | CONDITIONAL | $23k |
| UC-09-05 | AR Management | VS-4 VS-8 | $45k | **$90k** | $144k | — | $22k | DEFER | $14k |
| UC-07-02 | Payments | VS-2 | $42k | **$84k** | $134k | — | — | CONDITIONAL | $21k |
| UC-13-02 | Analytics | VS-6 VS-8 | $38k | **$77k** | $123k | — | $11k | DEFER | $0k |
| UC-05-06 | Coding | VS-6 VS-8 | $35k | **$69k** | $111k | — | $33k | CONDITIONAL | $17k |
| UC-01-17 | Patient Access | VS-4 | $30k | **$60k** | $96k | — | — | DEFER | $0k |
| UC-12-02 | Compliance | VS-6 VS-8 | $24k | **$48k** | $77k | — | $111k | DEFER | $7k |
| UC-14-05 | Master Data & Tech | VS-6 | $24k | **$48k** | $77k | — | — | CONDITIONAL | $12k |
| UC-02-05 | Utilization Review | VS-6 | $23k | **$46k** | $74k | — | — | DEFER | $0k |
| UC-04-05 | CDI | VS-6 | $23k | **$46k** | $74k | — | — | CONDITIONAL | $12k |
| UC-10-08 | Patient Financial Svcs | VS-4 VS-8 | $20k | **$40k** | $64k | — | $11k | CONDITIONAL | $10k |
| UC-13-03 | Analytics | VS-6 | $14k | **$29k** | $46k | — | — | CONDITIONAL | $7k |
| UC-13-04 | Analytics | VS-6 VS-8 | $14k | **$29k** | $46k | — | $33k | DEFER | $4k |
| UC-14-04 | Master Data & Tech | VS-6 VS-8 | $14k | **$29k** | $46k | — | $11k | DEFER | $4k |
| UC-03-08 | Charge Capture | VS-8 | $0k | **$0k** | $0k | — | $22k | CONDITIONAL | $0k |
| UC-10-06 | Patient Financial Svcs | VS-8 | $0k | **$0k** | $0k | — | $55k | DEFER | $0k |
| UC-12-01 | Compliance | VS-8 | $0k | **$0k** | $0k | — | $166k | DEFER | $0k |
| UC-12-03 | Compliance | VS-8 | $0k | **$0k** | $0k | — | $111k | DEFER | $0k |
| UC-12-04 | Compliance | VS-8 | $0k | **$0k** | $0k | — | $166k | DEFER | $0k |
| UC-12-06 | Compliance | VS-8 | $0k | **$0k** | $0k | — | $55k | CONDITIONAL | $0k |

Measurement designs per stream: 09-value-model.md §4. Recalibrate draw shares quarterly against realized value (true-up rule).
