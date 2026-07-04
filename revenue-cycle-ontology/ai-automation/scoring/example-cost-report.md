# Cost model — Example Regional Health (fictional)

NPR $1.00B; 99 active use cases priced over 3 years. Build ranges ±(0.8/1.5), run ±20% — see 10-cost-model.md.

## Portfolio totals

| Measure | Value |
|---|---|
| Platform build (L1, one-time) | **$1.69M** |
| Platform run (L1, annual) | $755k |
| Use-case build (L2, one-time, recommended options) | **$7.45M** ($5.96M – $11.18M) |
| Use-case run (L3, annual) | **$7.70M** ($6.16M – $9.24M) |
| 3-year portfolio TCO | **$34.61M** |
| Steady-state net value (value − run), annual | **$33.77M** |

## Annual run cost by category

| Category | Annual $ |
|---|---|
| HITL review labor | $5.93M |
| Maintenance, payer & hosting | $1.48M |
| Vendor fees | $186k |
| Inference/compute | $108k |
| Platform hosting/run (L1) | $755k |

## Platform assets (L1)

| Asset | Build | Run/yr | Dependent UCs |
|---|---|---|---|
| data_foundation | $350k | $120k | 70 |
| label_pipeline | $150k | $60k | 39 |
| orchestration_fabric | $300k | $100k | 10 |
| observability | $200k | $80k | 74 |
| doc_ai_platform | $180k | $90k | 4 |
| payer_knowledge_base | $120k | $60k | 7 |
| review_workbenches | $100k | $40k | 68 |
| nonhuman_identity | $80k | $30k | 10 |
| prompt_registry | $60k | $25k | 31 |
| governance_program | $150k | $150k | 99 |

## SLM family break-even (vs frontier API rates)

| Family | Member UCs | Annual Mtokens | API-vs-SLM savings/yr | Family cost/yr | Verdict |
|---|---|---|---|---|---|
| doc_extraction | 4 | 3,911 | $15k | $180k | stay on API |
| gen_drafting | 12 | 6,875 | $27k | $233k | stay on API |
| clinical_nlp | 13 | 4,858 | $19k | $197k | stay on API |

## Per-use-case decisions (sorted by allocated TCO)

| UC | Option | Build | Run/yr | TCO (alloc) | Value/yr | Net/yr | Payback | ROI-3yr | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UC-05-01 | api | $422k | $430k | $1.74M | $888k | $452k | 12 mo | -29% | beat slm; revisit at 4.4x volume |
| UC-01-08 | api | $283k | $391k | $1.60M | $651k | $233k | 18 mo | -43% | beat slm |
| UC-05-07 | api | $154k | $419k | $1.48M | $148k | $-285k | — | -85% | beat slm |
| UC-10-03 | api | $472k | $295k | $1.38M | $628k | $328k | 18 mo | -30% | beat vendor; revisit at 0.2x volume |
| UC-01-14 | api | $283k | $311k | $1.24M | $584k | $268k | 13 mo | -27% | beat vendor; revisit at 0.1x volume |
| UC-03-02 | native_module | $23k | $404k | $1.24M | $300k | $-106k | — | -63% | beat build_rules |
| UC-08-03 | api | $447k | $217k | $1.17M | $1.08M | $853k | 7 mo | +30% | beat slm |
| UC-03-06 | api | $258k | $243k | $1.02M | $1.55M | $1.30M | 2 mo | +113% | beat slm |
| UC-06-02 | api | $258k | $207k | $987k | $341k | $115k | 32 mo | -46% | beat vendor |
| UC-01-01 | api | $258k | $195k | $985k | $191k | $-32k | — | -70% | beat slm |
| UC-01-11 | api | $154k | $228k | $910k | $229k | $-13k | — | -65% | beat slm; revisit at 9.0x volume |
| UC-04-04 | api | $258k | $192k | $864k | $500k | $302k | 11 mo | -19% | beat slm |
| UC-01-03 | api | $154k | $173k | $815k | $382k | $181k | 14 mo | -34% | beat vendor; revisit at 1.1x volume |
| UC-02-02 | api | $258k | $167k | $788k | $314k | $142k | 23 mo | -22% | beat slm |
| UC-10-02 | native_module | $23k | $196k | $644k | $460k | $258k | 2 mo | +0% | beat vendor |
| UC-09-02 | native_module | $59k | $148k | $591k | $754k | $591k | 2 mo | +98% | beat build_rpa |
| UC-01-04 | native_module | $43k | $179k | $588k | $738k | $557k | 1 mo | +95% | beat build_rules |
| UC-02-05 | api | $96k | $142k | $553k | $46k | $-102k | — | -88% | beat slm |
| UC-07-01 | native_module | $39k | $160k | $551k | $436k | $270k | 2 mo | +23% | beat vendor |
| UC-04-03 | api | $154k | $118k | $537k | $546k | $423k | 5 mo | +42% | beat vendor |
| UC-06-01 | native_module | $39k | $152k | $529k | $917k | $758k | 1 mo | +143% | beat vendor |
| UC-09-01 | native_module | $39k | $152k | $529k | $718k | $559k | 1 mo | +90% | beat vendor |
| UC-07-03 | vendor | $77k | $93k | $525k | $206k | $84k | 19 mo | -39% | beat api; revisit at 1.9x volume |
| UC-12-02 | api | $258k | $51k | $517k | $48k | $-22k | — | -86% | beat slm |
| UC-06-05 | api | $174k | $55k | $445k | $367k | $294k | 9 mo | +28% | beat slm |
| UC-08-01 | vendor | $77k | $106k | $443k | $332k | $220k | 5 mo | +16% | beat api; revisit at 2.8x volume |
| UC-05-03 | api | $96k | $104k | $438k | $240k | $130k | 10 mo | +7% | beat slm |
| UC-08-05 | api | $154k | $84k | $435k | $1.15M | $1.06M | 2 mo | +414% | beat slm |
| UC-01-02 | native_module | $23k | $121k | $420k | $96k | $-32k | — | -56% | beat vendor |
| UC-01-16 | native_module | $23k | $121k | $420k | $650k | $522k | 1 mo | +117% | beat build_ml |
| UC-03-01 | native_module | $39k | $115k | $417k | $2.50M | $2.38M | 0 mo | +1069% | beat build_ml |
| UC-02-03 | native_module | $23k | $90k | $381k | $383k | $277k | 3 mo | +40% | beat build_rpa |
| UC-10-07 | vendor | $46k | $85k | $352k | $480k | $389k | 2 mo | +166% | beat api; revisit at 1.4x volume |
| UC-04-01 | api | $154k | $54k | $345k | $1.00M | $940k | 2 mo | +465% | beat slm |
| UC-04-02 | api | $154k | $54k | $345k | $577k | $517k | 4 mo | +226% | beat slm |
| UC-01-09 | native_module | $23k | $74k | $333k | $192k | $103k | 8 mo | -11% | beat build_rpa |
| UC-11-04 | native_module | $39k | $63k | $317k | $537k | $458k | 2 mo | +230% | beat vendor |
| UC-07-02 | api | $154k | $44k | $314k | $84k | $35k | 58 mo | -48% | beat slm |
| UC-12-05 | api | $154k | $29k | $314k | $115k | $71k | 31 mo | -43% | beat slm |
| UC-06-04 | native_module | $43k | $83k | $300k | $279k | $194k | 3 mo | +81% | beat build_rules |
| UC-05-05 | native_module | $23k | $80k | $297k | $115k | $29k | 16 mo | -24% | beat build_ml |
| UC-14-05 | native_module | $14k | $76k | $275k | $48k | $-34k | — | -66% | beat build_ml |
| UC-01-07 | native_module | $23k | $67k | $274k | $688k | $610k | 1 mo | +252% | beat build_rules |
| UC-12-01 | vendor | $46k | $22k | $263k | $0k | $-50k | — | -100% | beat api; revisit at 3.0x volume |
| UC-01-12 | native_module | $42k | $56k | $243k | $450k | $388k | 2 mo | +159% | beat build_ml |
| UC-11-01 | vendor | $77k | $34k | $225k | $1.31M | $1.27M | 1 mo | +719% | beat api; revisit at 3.2x volume |
| UC-03-03 | native_module | $23k | $62k | $216k | $500k | $436k | 1 mo | +259% | beat build_rules |
| UC-10-01 | native_module | $23k | $60k | $209k | $256k | $194k | 2 mo | +90% | beat build_rules |
| UC-07-04 | native_module | $23k | $49k | $203k | $92k | $37k | 12 mo | -12% | beat build_ml |
| UC-01-05 | native_module | $43k | $40k | $198k | $1.70M | $1.65M | 0 mo | +1232% | beat vendor |
| UC-01-13 | native_module | $23k | $47k | $197k | $315k | $262k | 2 mo | +124% | beat build_ml |
| UC-11-03 | vendor | $46k | $22k | $187k | $573k | $537k | 2 mo | +374% | beat api; revisit at 8.0x volume |
| UC-13-01 | api | $96k | $17k | $177k | $96k | $73k | 18 mo | +6% | beat slm |
| UC-07-05 | native_module | $23k | $49k | $176k | $2.00M | $1.95M | 0 mo | +2122% | beat build_rules |
| UC-06-07 | native_module | $43k | $31k | $170k | $295k | $257k | 3 mo | +238% | beat build_ml |
| UC-11-02 | api | $96k | $15k | $170k | $400k | $379k | 3 mo | +358% | beat slm |
| UC-06-06 | native_module | $23k | $47k | $169k | $344k | $296k | 1 mo | +297% | beat build_rules |
| UC-01-17 | native_module | $14k | $37k | $159k | $60k | $17k | 21 mo | -47% | beat vendor |
| UC-13-02 | native_module | $23k | $33k | $156k | $77k | $37k | 12 mo | -31% | beat build_ml |
| UC-02-01 | native_module | $23k | $30k | $146k | $344k | $308k | 1 mo | +229% | beat build_ml |
| UC-08-04 | native_module | $14k | $31k | $141k | $103k | $66k | 5 mo | +42% | beat build_ml |
| UC-14-04 | native_module | $23k | $2k | $140k | $29k | $7k | 122 mo | -68% | beat build_ml |
| UC-05-02 | native_module | $23k | $25k | $133k | $229k | $197k | 2 mo | +141% | beat build_ml |
| UC-06-08 | native_module | $43k | $23k | $120k | $169k | $144k | 4 mo | +119% | beat build_rules |
| UC-14-06 | native_module | $23k | $2k | $112k | $216k | $200k | 4 mo | +200% | beat build_rules |
| UC-06-03 | native_module | $23k | $17k | $107k | $458k | $435k | 1 mo | +734% | beat build_ml |
| UC-08-02 | native_module | $23k | $17k | $107k | $434k | $410k | 1 mo | +466% | beat build_ml |
| UC-09-06 | native_module | $23k | $17k | $107k | $231k | $207k | 2 mo | +320% | beat build_ml |
| UC-10-05 | native_module | $23k | $15k | $103k | $180k | $158k | 3 mo | +145% | beat vendor |
| UC-09-03 | native_module | $23k | $8k | $80k | $1.60M | $1.59M | 0 mo | +3782% | beat build_ml |
| UC-01-15 | native_module | $14k | $19k | $78k | $300k | $279k | 1 mo | +654% | beat build_rules |
| UC-05-06 | native_module | $14k | $9k | $75k | $69k | $54k | 6 mo | +79% | beat build_ml |
| UC-10-04 | native_module | $23k | $5k | $71k | $340k | $329k | 1 mo | +566% | beat build_ml |
| UC-09-04 | native_module | $23k | $4k | $69k | $115k | $105k | 4 mo | +133% | beat vendor |
| UC-03-07 | native_module | $23k | $3k | $67k | $800k | $790k | 1 mo | +2230% | beat build_ml |
| UC-08-06 | native_module | $43k | $5k | $66k | $140k | $133k | 4 mo | +199% | beat build_rules |
| UC-14-01 | native_module | $14k | $6k | $65k | $229k | $217k | 2 mo | +586% | beat build_ml |
| UC-14-07 | native_module | $14k | $6k | $65k | $300k | $288k | 1 mo | +798% | beat build_ml |
| UC-12-03 | native_module | $23k | $2k | $63k | $0k | $-8k | — | -100% | beat build_ml |
| UC-13-04 | native_module | $23k | $2k | $63k | $29k | $20k | 22 mo | -29% | beat build_ml |
| UC-11-05 | native_module | $23k | $2k | $63k | $900k | $892k | 1 mo | +2707% | beat build_ml |
| UC-11-06 | native_module | $23k | $2k | $63k | $690k | $682k | 1 mo | +1446% | beat build_ml |
| UC-12-06 | native_module | $14k | $1k | $52k | $0k | $-8k | — | -100% | beat build_ml |
| UC-03-04 | native_module | $14k | $1k | $52k | $1.00M | $992k | 0 mo | +3658% | beat build_ml |
| UC-13-03 | native_module | $14k | $1k | $52k | $29k | $21k | 16 mo | +8% | beat build_ml |
| UC-14-03 | native_module | $14k | $1k | $52k | $262k | $254k | 1 mo | +885% | beat build_ml |
| UC-02-04 | native_module | $14k | $10k | $49k | $229k | $218k | 1 mo | +811% | beat build_rules |
| UC-05-04 | native_module | $23k | $7k | $49k | $128k | $120k | 2 mo | +413% | beat build_rules |
| UC-10-06 | native_module | $23k | $5k | $45k | $0k | $-7k | — | -100% | beat build_rules |
| UC-04-05 | native_module | $14k | $8k | $45k | $46k | $36k | 5 mo | +100% | beat build_rules |
| UC-01-10 | native_module | $23k | $5k | $43k | $458k | $452k | 1 mo | +1383% | beat build_rules |
| UC-09-05 | native_module | $23k | $4k | $41k | $90k | $84k | 3 mo | +237% | beat vendor |
| UC-01-06 | native_module | $14k | $7k | $40k | $344k | $336k | 1 mo | +1576% | beat build_rules |
| UC-07-06 | native_module | $23k | $3k | $38k | $400k | $396k | 1 mo | +1370% | beat build_rules |
| UC-10-08 | native_module | $14k | $6k | $38k | $40k | $33k | 6 mo | +105% | beat build_rules |
| UC-12-04 | native_module | $23k | $3k | $37k | $0k | $-4k | — | -100% | beat build_rules |
| UC-03-05 | native_module | $23k | $2k | $35k | $220k | $216k | 1 mo | +1124% | beat build_rules |
| UC-03-08 | native_module | $23k | $2k | $35k | $0k | $-3k | — | -100% | beat build_rules |
| UC-14-02 | native_module | $14k | $1k | $24k | $115k | $112k | 2 mo | +832% | beat build_rules |

Decision rules, math, and governance: 10-cost-model.md. Coefficients recalibrate quarterly against actuals (true-up rule).
