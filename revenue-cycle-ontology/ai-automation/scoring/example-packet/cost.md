# Cost model — Example Regional Health (fictional)

NPR $1.00B; 99 active use cases priced over 3 years. Build ranges ±(0.8/1.5), run ±20% — see 10-cost-model.md.

## Portfolio totals

| Measure | Value |
|---|---|
| Platform build (L1, one-time) | **$1.69M** |
| Platform run (L1, annual) | $755k |
| Use-case build (L2, one-time, recommended options) | **$15.14M** ($12.11M – $22.71M) |
| Use-case run (L3, annual) | **$10.60M** ($8.48M – $12.72M) |
| 3-year portfolio TCO | **$51.25M** |
| Steady-state net value (value − run), annual | **$30.87M** |

## Annual run cost by category

| Category | Annual $ |
|---|---|
| HITL review labor | $5.93M |
| Maintenance, payer & hosting | $3.85M |
| Vendor fees | $707k |
| Inference/compute | $112k |
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
| UC-03-02 | build_rules | $123k | $433k | $1.43M | $300k | $-135k | — | -67% |  |
| UC-10-03 | api | $472k | $295k | $1.38M | $628k | $328k | 18 mo | -30% | beat vendor; revisit at 0.2x volume |
| UC-01-14 | api | $283k | $311k | $1.24M | $584k | $268k | 13 mo | -27% | beat vendor; revisit at 0.1x volume |
| UC-08-03 | api | $447k | $217k | $1.17M | $1.08M | $853k | 7 mo | +30% | beat slm |
| UC-06-01 | build_ml | $310k | $242k | $1.07M | $917k | $668k | 6 mo | +20% | differentiator: built in-house despite vendor price within threshold; beat vendor; revisit at 1.4x volume |
| UC-03-06 | api | $258k | $243k | $1.02M | $1.55M | $1.30M | 2 mo | +113% | beat slm |
| UC-06-02 | api | $258k | $207k | $987k | $341k | $115k | 32 mo | -46% | beat vendor |
| UC-01-01 | api | $258k | $195k | $985k | $191k | $-32k | — | -70% | beat slm |
| UC-09-02 | build_rpa | $252k | $206k | $959k | $754k | $533k | 7 mo | +22% | beat vendor |
| UC-03-01 | build_ml | $310k | $205k | $959k | $2.50M | $2.29M | 2 mo | +408% | beat vendor; revisit at 0.5x volume |
| UC-01-11 | api | $154k | $228k | $910k | $229k | $-13k | — | -65% | beat slm; revisit at 9.0x volume |
| UC-09-01 | vendor | $77k | $247k | $899k | $718k | $464k | 2 mo | +12% | beat build_ml; revisit at 1.8x volume |
| UC-10-02 | vendor | $46k | $257k | $882k | $460k | $196k | 4 mo | -27% | beat build_ml; revisit at 1.6x volume |
| UC-04-04 | api | $258k | $192k | $864k | $500k | $302k | 11 mo | -19% | beat slm |
| UC-01-12 | build_ml | $340k | $154k | $836k | $450k | $289k | 15 mo | -25% | beat vendor; revisit at 1.1x volume |
| UC-01-03 | api | $154k | $173k | $815k | $382k | $181k | 14 mo | -34% | beat vendor; revisit at 1.1x volume |
| UC-07-01 | vendor | $77k | $222k | $808k | $436k | $208k | 5 mo | -16% | beat build_ml; revisit at 2.7x volume |
| UC-02-02 | api | $258k | $167k | $788k | $314k | $142k | 23 mo | -22% | beat slm |
| UC-01-04 | build_rules | $143k | $212k | $785k | $738k | $525k | 3 mo | +83% | beat vendor; revisit at 0.3x volume |
| UC-01-16 | build_ml | $185k | $175k | $744k | $650k | $468k | 5 mo | +22% |  |
| UC-05-05 | build_ml | $185k | $134k | $621k | $115k | $-25k | — | -64% |  |
| UC-01-02 | vendor | $46k | $169k | $609k | $96k | $-79k | — | -69% | beat build_ml; revisit at 2.1x volume |
| UC-02-03 | build_rpa | $139k | $123k | $595k | $383k | $245k | 9 mo | -10% | beat vendor; revisit at 0.3x volume |
| UC-02-05 | api | $96k | $142k | $553k | $46k | $-102k | — | -88% | beat slm |
| UC-01-09 | build_rpa | $139k | $107k | $547k | $192k | $70k | 31 mo | -46% | beat vendor; revisit at 0.4x volume |
| UC-04-03 | api | $154k | $118k | $537k | $546k | $423k | 5 mo | +42% | beat vendor |
| UC-07-04 | build_ml | $185k | $103k | $526k | $92k | $-17k | — | -66% |  |
| UC-07-03 | vendor | $77k | $93k | $525k | $206k | $84k | 19 mo | -39% | beat api; revisit at 1.9x volume |
| UC-01-13 | build_ml | $185k | $100k | $520k | $315k | $208k | 11 mo | -15% |  |
| UC-12-02 | api | $258k | $51k | $517k | $48k | $-22k | — | -86% | beat slm |
| UC-06-07 | build_ml | $205k | $89k | $506k | $295k | $199k | 13 mo | +14% |  |
| UC-06-04 | build_rules | $143k | $116k | $497k | $279k | $161k | 11 mo | +9% |  |
| UC-13-02 | build_ml | $185k | $87k | $479k | $77k | $-16k | — | -78% |  |
| UC-14-05 | build_ml | $115k | $109k | $477k | $48k | $-68k | — | -80% |  |
| UC-02-01 | build_ml | $185k | $83k | $469k | $344k | $254k | 9 mo | +3% |  |
| UC-14-04 | build_ml | $185k | $56k | $462k | $29k | $-46k | — | -90% |  |
| UC-01-07 | build_rules | $123k | $96k | $461k | $688k | $581k | 3 mo | +131% |  |
| UC-05-02 | build_ml | $185k | $79k | $456k | $229k | $144k | 17 mo | -30% |  |
| UC-06-05 | api | $174k | $55k | $445k | $367k | $294k | 9 mo | +28% | beat slm |
| UC-08-01 | vendor | $77k | $106k | $443k | $332k | $220k | 5 mo | +16% | beat api; revisit at 2.8x volume |
| UC-11-04 | vendor | $77k | $88k | $442k | $537k | $434k | 3 mo | +137% | beat build_rpa; revisit at 4.4x volume |
| UC-05-03 | api | $96k | $104k | $438k | $240k | $130k | 10 mo | +7% | beat slm |
| UC-08-05 | api | $154k | $84k | $435k | $1.15M | $1.06M | 2 mo | +414% | beat slm |
| UC-06-03 | build_ml | $185k | $70k | $430k | $458k | $382k | 6 mo | +108% |  |
| UC-08-02 | build_ml | $185k | $70k | $430k | $434k | $357k | 7 mo | +41% |  |
| UC-09-06 | build_ml | $185k | $70k | $430k | $231k | $154k | 16 mo | +5% |  |
| UC-01-05 | vendor | $66k | $99k | $426k | $1.70M | $1.59M | 1 mo | +518% | beat build_ml; revisit at 1.8x volume |
| UC-10-05 | vendor | $46k | $100k | $424k | $180k | $73k | 10 mo | -41% | beat build_ml; revisit at 1.2x volume |
| UC-09-03 | build_ml | $185k | $61k | $403k | $1.60M | $1.53M | 2 mo | +674% |  |
| UC-03-03 | build_rules | $123k | $91k | $403k | $500k | $407k | 4 mo | +92% |  |
| UC-10-01 | build_rules | $123k | $89k | $396k | $256k | $165k | 9 mo | +0% |  |
| UC-10-04 | build_ml | $185k | $58k | $394k | $340k | $275k | 9 mo | +21% |  |
| UC-03-07 | build_ml | $185k | $57k | $389k | $800k | $737k | 3 mo | +301% |  |
| UC-12-03 | build_ml | $185k | $56k | $385k | $0k | $-62k | — | -100% |  |
| UC-13-04 | build_ml | $185k | $56k | $385k | $29k | $-33k | — | -88% |  |
| UC-11-05 | build_ml | $185k | $55k | $385k | $900k | $838k | 3 mo | +356% |  |
| UC-11-06 | build_ml | $185k | $55k | $385k | $690k | $628k | 4 mo | +151% |  |
| UC-07-05 | build_rules | $123k | $78k | $362k | $2.00M | $1.92M | 1 mo | +976% |  |
| UC-06-06 | build_rules | $123k | $76k | $356k | $344k | $267k | 6 mo | +88% |  |
| UC-10-07 | vendor | $46k | $85k | $352k | $480k | $389k | 2 mo | +166% | beat api; revisit at 1.4x volume |
| UC-04-01 | api | $154k | $54k | $345k | $1.00M | $940k | 2 mo | +465% | beat slm |
| UC-04-02 | api | $154k | $54k | $345k | $577k | $517k | 4 mo | +226% | beat slm |
| UC-08-04 | build_ml | $115k | $64k | $342k | $103k | $32k | 48 mo | -41% |  |
| UC-01-17 | vendor | $29k | $80k | $322k | $60k | $-26k | — | -74% | beat build_ml; revisit at 1.5x volume |
| UC-06-08 | build_rules | $143k | $56k | $317k | $169k | $111k | 16 mo | -17% |  |
| UC-07-02 | api | $154k | $44k | $314k | $84k | $35k | 58 mo | -48% | beat slm |
| UC-12-05 | api | $154k | $29k | $314k | $115k | $71k | 31 mo | -43% | beat slm |
| UC-14-06 | build_rules | $123k | $31k | $299k | $216k | $171k | 11 mo | +12% |  |
| UC-05-06 | build_ml | $115k | $42k | $276k | $69k | $20k | 77 mo | -51% |  |
| UC-14-01 | build_ml | $115k | $39k | $266k | $229k | $184k | 8 mo | +68% |  |
| UC-14-07 | build_ml | $115k | $39k | $266k | $300k | $255k | 6 mo | +120% |  |
| UC-12-01 | vendor | $46k | $22k | $263k | $0k | $-50k | — | -100% | beat api; revisit at 3.0x volume |
| UC-08-06 | build_rules | $143k | $38k | $263k | $140k | $101k | 17 mo | -25% |  |
| UC-12-06 | build_ml | $115k | $35k | $253k | $0k | $-41k | — | -100% |  |
| UC-03-04 | build_ml | $115k | $35k | $253k | $1.00M | $959k | 2 mo | +671% |  |
| UC-13-03 | build_ml | $115k | $35k | $253k | $29k | $-12k | — | -78% |  |
| UC-14-03 | build_ml | $115k | $35k | $253k | $262k | $221k | 7 mo | +102% |  |
| UC-05-04 | build_rules | $123k | $35k | $236k | $128k | $91k | 16 mo | +6% |  |
| UC-10-06 | build_rules | $123k | $34k | $232k | $0k | $-36k | — | -100% |  |
| UC-01-10 | build_rules | $123k | $34k | $230k | $458k | $423k | 4 mo | +179% |  |
| UC-07-06 | build_rules | $123k | $32k | $225k | $400k | $367k | 4 mo | +149% |  |
| UC-11-01 | vendor | $77k | $34k | $225k | $1.31M | $1.27M | 1 mo | +719% | beat api; revisit at 3.2x volume |
| UC-12-04 | build_rules | $123k | $32k | $224k | $0k | $-33k | — | -100% |  |
| UC-03-05 | build_rules | $123k | $31k | $222k | $220k | $187k | 8 mo | +93% |  |
| UC-03-08 | build_rules | $123k | $31k | $222k | $0k | $-32k | — | -100% |  |
| UC-01-15 | build_rules | $77k | $37k | $194k | $300k | $261k | 4 mo | +201% |  |
| UC-11-03 | vendor | $46k | $22k | $187k | $573k | $537k | 2 mo | +374% | beat api; revisit at 8.0x volume |
| UC-13-01 | api | $96k | $17k | $177k | $96k | $73k | 18 mo | +6% | beat slm |
| UC-11-02 | api | $96k | $15k | $170k | $400k | $379k | 3 mo | +358% | beat slm |
| UC-09-05 | vendor | $46k | $34k | $169k | $90k | $55k | 11 mo | -17% | beat build_rules; revisit at 1.8x volume |
| UC-02-04 | build_rules | $77k | $28k | $166k | $229k | $200k | 5 mo | +170% |  |
| UC-04-05 | build_rules | $77k | $26k | $162k | $46k | $18k | 51 mo | -44% |  |
| UC-01-06 | build_rules | $77k | $25k | $157k | $344k | $318k | 3 mo | +328% |  |
| UC-09-04 | vendor | $46k | $22k | $155k | $115k | $87k | 8 mo | +4% | beat build_ml; revisit at 5.6x volume |
| UC-10-08 | build_rules | $77k | $24k | $155k | $40k | $15k | 64 mo | -50% |  |
| UC-14-02 | build_rules | $77k | $19k | $141k | $115k | $94k | 10 mo | +59% |  |

Decision rules, math, and governance: 10-cost-model.md. Coefficients recalibrate quarterly against actuals (true-up rule).
