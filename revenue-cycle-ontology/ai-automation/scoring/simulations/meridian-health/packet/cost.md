# Cost model — Meridian Health (simulated)

NPR $2.40B; 99 active use cases priced over 3 years. Build ranges ±(0.8/1.5), run ±20% — see 10-cost-model.md.

## Portfolio totals

| Measure | Value |
|---|---|
| Platform build (L1, one-time) | **$1.69M** |
| Platform run (L1, annual) | $755k |
| Use-case build (L2, one-time, recommended options) | **$16.79M** ($13.44M – $25.19M) |
| Use-case run (L3, annual) | **$19.25M** ($15.40M – $23.10M) |
| 3-year portfolio TCO | **$78.58M** |
| Steady-state net value (value − run), annual | **$76.85M** |

## Annual run cost by category

| Category | Annual $ |
|---|---|
| HITL review labor | $14.21M |
| Maintenance, payer & hosting | $4.61M |
| Inference/compute | $284k |
| Vendor fees | $149k |
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
| doc_extraction | 4 | 9,385 | $37k | $180k | stay on API |
| gen_drafting | 12 | 16,416 | $64k | $233k | stay on API |
| clinical_nlp | 13 | 11,658 | $45k | $197k | stay on API |

## Per-use-case decisions (sorted by allocated TCO)

| UC | Option | Build | Run/yr | TCO (alloc) | Value/yr | Net/yr | Payback | ROI-3yr | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UC-05-01 | api | $422k | $944k | $3.28M | $1.95M | $999k | 5 mo | -17% | beat slm; revisit at 1.8x volume |
| UC-05-07 | api | $154k | $974k | $3.15M | $321k | $-667k | — | -84% | beat slm; revisit at 5.4x volume |
| UC-03-02 | build_rules | $123k | $996k | $3.12M | $720k | $-278k | — | -64% |  |
| UC-01-08 | api | $283k | $794k | $2.81M | $1.41M | $590k | 7 mo | -30% | beat slm |
| UC-01-14 | api | $283k | $687k | $2.37M | $1.32M | $623k | 6 mo | +8% | beat vendor |
| UC-10-03 | api | $472k | $608k | $2.32M | $1.39M | $775k | 7 mo | -7% | beat vendor |
| UC-03-06 | api | $258k | $530k | $1.88M | $3.71M | $3.18M | 1 mo | +177% | beat slm; revisit at 5.1x volume |
| UC-08-03 | api | $447k | $427k | $1.80M | $2.35M | $1.91M | 3 mo | +82% | beat slm |
| UC-10-02 | build_ml | $185k | $522k | $1.79M | $1.10M | $575k | 4 mo | -13% | beat vendor; revisit at 0.7x volume |
| UC-01-11 | api | $154k | $514k | $1.77M | $495k | $-34k | — | -45% | beat slm; revisit at 3.8x volume |
| UC-07-01 | build_ml | $310k | $470k | $1.75M | $956k | $480k | 8 mo | -15% | beat vendor; revisit at 1.1x volume |
| UC-06-01 | build_ml | $310k | $452k | $1.70M | $1.98M | $1.52M | 3 mo | +63% | beat vendor; revisit at 0.6x volume |
| UC-09-01 | build_ml | $310k | $452k | $1.70M | $1.63M | $1.17M | 3 mo | +34% | beat vendor; revisit at 0.7x volume |
| UC-06-02 | api | $258k | $443k | $1.69M | $761k | $299k | 12 mo | -30% | beat slm; revisit at 4.2x volume |
| UC-01-01 | api | $258k | $413k | $1.64M | $415k | $-27k | — | -61% | beat slm; revisit at 4.3x volume |
| UC-01-04 | build_rules | $143k | $458k | $1.52M | $1.61M | $1.15M | 2 mo | +106% | beat vendor; revisit at 0.1x volume |
| UC-04-04 | api | $258k | $407k | $1.51M | $1.20M | $787k | 4 mo | +11% | beat slm; revisit at 6.7x volume |
| UC-01-03 | api | $154k | $383k | $1.44M | $826k | $415k | 6 mo | -20% | beat slm; revisit at 3.8x volume |
| UC-03-01 | build_ml | $310k | $362k | $1.43M | $6.00M | $5.63M | 1 mo | +718% | beat vendor; revisit at 0.2x volume |
| UC-02-02 | api | $258k | $346k | $1.33M | $683k | $331k | 10 mo | +0% | beat slm; revisit at 8.1x volume |
| UC-09-02 | build_rpa | $252k | $322k | $1.31M | $1.66M | $1.32M | 3 mo | +147% | beat vendor; revisit at 0.4x volume |
| UC-01-02 | build_ml | $185k | $343k | $1.25M | $207k | $-142k | — | -68% | beat vendor; revisit at 0.9x volume |
| UC-01-16 | build_ml | $185k | $343k | $1.25M | $1.40M | $1.06M | 2 mo | +58% |  |
| UC-02-05 | api | $96k | $321k | $1.09M | $100k | $-227k | — | -82% | beat slm; revisit at 4.9x volume |
| UC-01-12 | build_ml | $340k | $228k | $1.06M | $1.08M | $846k | 5 mo | +43% | beat vendor; revisit at 0.5x volume |
| UC-05-05 | build_ml | $185k | $244k | $950k | $251k | $0k | 13522 mo | -49% |  |
| UC-04-03 | api | $154k | $250k | $934k | $1.30M | $1.04M | 2 mo | +95% | beat slm |
| UC-08-01 | api | $258k | $202k | $895k | $720k | $512k | 6 mo | +25% | beat vendor; revisit at 1.2x volume |
| UC-06-04 | build_rules | $143k | $228k | $833k | $613k | $384k | 5 mo | +44% |  |
| UC-05-03 | api | $96k | $229k | $814k | $576k | $341k | 4 mo | +38% | beat slm; revisit at 6.9x volume |
| UC-07-03 | api | $258k | $133k | $800k | $455k | $293k | 13 mo | -12% | beat vendor; revisit at 0.8x volume |
| UC-14-05 | build_ml | $115k | $214k | $791k | $104k | $-116k | — | -74% |  |
| UC-07-04 | build_ml | $185k | $169k | $724k | $200k | $25k | 94 mo | -46% |  |
| UC-02-03 | build_rpa | $139k | $162k | $713k | $829k | $652k | 3 mo | +63% | beat vendor; revisit at 0.1x volume |
| UC-01-13 | build_ml | $185k | $163k | $708k | $731k | $561k | 4 mo | +44% |  |
| UC-01-05 | build_ml | $205k | $150k | $689k | $4.08M | $3.92M | 1 mo | +818% | beat vendor; revisit at 0.7x volume |
| UC-08-05 | api | $154k | $168k | $689k | $2.48M | $2.30M | 1 mo | +601% | beat slm |
| UC-03-03 | build_rules | $123k | $176k | $656k | $1.20M | $1.02M | 1 mo | +183% |  |
| UC-10-01 | build_rules | $123k | $170k | $640k | $590k | $418k | 4 mo | +43% |  |
| UC-06-07 | build_ml | $205k | $128k | $623k | $653k | $518k | 5 mo | +104% |  |
| UC-13-02 | build_ml | $185k | $131k | $611k | $167k | $30k | 80 mo | -62% |  |
| UC-01-09 | build_rpa | $139k | $123k | $597k | $418k | $279k | 8 mo | +36% | beat vendor; revisit at 0.2x volume |
| UC-02-01 | build_ml | $185k | $123k | $587k | $743k | $613k | 4 mo | +77% |  |
| UC-12-02 | api | $258k | $68k | $569k | $104k | $18k | 209 mo | -64% | beat slm |
| UC-06-05 | api | $174k | $95k | $566k | $796k | $682k | 4 mo | +118% | beat slm |
| UC-07-05 | build_rules | $123k | $143k | $560k | $4.80M | $4.66M | 0 mo | +1573% |  |
| UC-05-02 | build_ml | $185k | $112k | $555k | $495k | $377k | 6 mo | +25% |  |
| UC-10-07 | api | $154k | $121k | $548k | $1.15M | $1.02M | 2 mo | +310% | beat slm |
| UC-06-06 | build_rules | $123k | $138k | $544k | $743k | $603k | 2 mo | +166% |  |
| UC-01-17 | build_ml | $115k | $121k | $511k | $144k | $17k | 93 mo | -45% | beat vendor; revisit at 0.6x volume |
| UC-06-03 | build_ml | $185k | $91k | $493k | $990k | $892k | 3 mo | +292% |  |
| UC-08-02 | build_ml | $185k | $91k | $493k | $939k | $841k | 3 mo | +167% |  |
| UC-09-06 | build_ml | $185k | $91k | $493k | $535k | $438k | 5 mo | +112% |  |
| UC-01-07 | build_rules | $123k | $104k | $483k | $1.49M | $1.37M | 1 mo | +377% |  |
| UC-10-05 | build_ml | $185k | $88k | $482k | $432k | $338k | 7 mo | +26% | beat vendor; revisit at 0.5x volume |
| UC-04-01 | api | $154k | $97k | $474k | $2.40M | $2.30M | 1 mo | +887% | beat slm |
| UC-04-02 | api | $154k | $97k | $474k | $1.37M | $1.26M | 2 mo | +462% | beat slm |
| UC-08-04 | build_ml | $115k | $106k | $468k | $235k | $122k | 13 mo | -2% |  |
| UC-14-04 | build_ml | $185k | $56k | $462k | $63k | $-12k | — | -74% |  |
| UC-11-04 | vendor | $77k | $88k | $442k | $1.17M | $1.07M | 1 mo | +418% | beat build_rpa; revisit at 4.4x volume |
| UC-09-03 | build_ml | $185k | $70k | $428k | $3.84M | $3.76M | 1 mo | +1649% |  |
| UC-10-04 | build_ml | $185k | $63k | $407k | $816k | $747k | 3 mo | +181% |  |
| UC-06-08 | build_rules | $143k | $84k | $401k | $385k | $300k | 6 mo | +49% |  |
| UC-07-02 | api | $154k | $72k | $400k | $181k | $104k | 19 mo | -12% | beat slm |
| UC-03-07 | build_ml | $185k | $59k | $396k | $1.92M | $1.85M | 1 mo | +846% |  |
| UC-12-03 | build_ml | $185k | $56k | $385k | $0k | $-62k | — | -100% |  |
| UC-13-04 | build_ml | $185k | $56k | $385k | $63k | $1k | 3421 mo | -68% |  |
| UC-11-05 | build_ml | $185k | $55k | $385k | $2.16M | $2.10M | 1 mo | +994% |  |
| UC-11-06 | build_ml | $185k | $55k | $385k | $1.66M | $1.59M | 2 mo | +739% |  |
| UC-12-01 | vendor | $46k | $49k | $358k | $0k | $-77k | — | -100% | beat api; revisit at 1.3x volume |
| UC-12-05 | api | $154k | $29k | $314k | $248k | $204k | 11 mo | +22% | beat slm |
| UC-05-06 | build_ml | $115k | $53k | $309k | $150k | $90k | 17 mo | -5% |  |
| UC-14-06 | build_rules | $123k | $31k | $299k | $519k | $474k | 4 mo | +239% |  |
| UC-14-01 | build_ml | $115k | $45k | $285k | $495k | $443k | 4 mo | +239% |  |
| UC-14-07 | build_ml | $115k | $45k | $285k | $720k | $668k | 2 mo | +393% |  |
| UC-08-06 | build_rules | $143k | $41k | $271k | $302k | $260k | 7 mo | +118% |  |
| UC-01-15 | build_rules | $77k | $62k | $269k | $720k | $656k | 1 mo | +422% |  |
| UC-05-04 | build_rules | $123k | $42k | $255k | $297k | $254k | 6 mo | +127% |  |
| UC-12-06 | build_ml | $115k | $35k | $254k | $0k | $-41k | — | -100% |  |
| UC-03-04 | build_ml | $115k | $35k | $253k | $2.40M | $2.36M | 1 mo | +1750% |  |
| UC-13-03 | build_ml | $115k | $35k | $253k | $63k | $22k | 72 mo | -52% |  |
| UC-14-03 | build_ml | $115k | $35k | $253k | $574k | $533k | 3 mo | +343% |  |
| UC-09-04 | vendor | $46k | $50k | $251k | $251k | $194k | 4 mo | +40% | beat build_ml; revisit at 2.3x volume |
| UC-10-06 | build_rules | $123k | $39k | $247k | $0k | $-41k | — | -100% |  |
| UC-01-10 | build_rules | $123k | $38k | $242k | $990k | $951k | 2 mo | +534% |  |
| UC-09-05 | build_rules | $123k | $36k | $238k | $216k | $178k | 8 mo | +41% | beat vendor; revisit at 0.8x volume |
| UC-07-06 | build_rules | $123k | $34k | $230k | $960k | $925k | 2 mo | +715% |  |
| UC-12-04 | build_rules | $123k | $33k | $228k | $0k | $-34k | — | -100% |  |
| UC-11-01 | vendor | $77k | $34k | $225k | $3.13M | $3.09M | 0 mo | +1849% | beat api; revisit at 3.2x volume |
| UC-03-05 | build_rules | $123k | $31k | $222k | $476k | $443k | 3 mo | +318% |  |
| UC-03-08 | build_rules | $123k | $31k | $222k | $0k | $-32k | — | -100% |  |
| UC-02-04 | build_rules | $77k | $39k | $201k | $495k | $454k | 2 mo | +381% |  |
| UC-04-05 | build_rules | $77k | $36k | $191k | $100k | $63k | 15 mo | +2% |  |
| UC-11-03 | vendor | $46k | $22k | $187k | $1.24M | $1.20M | 1 mo | +924% | beat api; revisit at 8.0x volume |
| UC-01-06 | build_rules | $77k | $32k | $179k | $743k | $709k | 1 mo | +709% |  |
| UC-13-01 | api | $96k | $17k | $177k | $209k | $186k | 7 mo | +131% | beat slm |
| UC-10-08 | build_rules | $77k | $30k | $174k | $96k | $64k | 15 mo | +7% |  |
| UC-11-02 | api | $96k | $15k | $170k | $960k | $939k | 1 mo | +1000% | beat slm |
| UC-14-02 | build_rules | $77k | $19k | $141k | $248k | $227k | 4 mo | +244% |  |

Decision rules, math, and governance: 10-cost-model.md. Coefficients recalibrate quarterly against actuals (true-up rule).
