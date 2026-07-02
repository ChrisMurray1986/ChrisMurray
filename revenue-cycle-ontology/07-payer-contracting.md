# RC-11 Payer Contracting, Credentialing & Enrollment

Establishes and maintains the commercial terms under which care is paid, keeps providers
billable with every payer, monitors payer policy behavior, and manages the ongoing payer
relationship including escalation leverage.

Roles: Managed Care Contracting Director/Analyst, Contract Modeling Analyst, Credentialing
Specialist, Enrollment Specialist, Payer Relations Manager, VBC Program Manager.
Systems: contract management system, contract modeling/expected-pay engine, credentialing
platform, CAQH, PECOS/NPPES, payer portals, policy-monitoring services.

---

## 11.1 Contract Strategy, Modeling & Negotiation
- **A1.** Maintain payer portfolio inventory: contracts, amendments, term/renewal dates,
  termination notice windows, evergreen clauses
- **A2.** Model current-state performance by payer: realized yield vs contract, denial/underpayment
  burden, admin cost (auth/appeal load) — payer scorecard
- **A3.** Model proposed terms against historical volumes (rate changes, carve-outs, lesser-of
  language, stop-loss/outlier thresholds, escalators)
- **A4.** Negotiate: rates, payment methodologies (DRG/per-diem/case-rate/fee schedule/percent-of-charge),
  operational terms (auth turnaround SLAs, denial/appeal terms, timely filing, retro-audit
  lookback limits, prompt-pay interest, criteria set designation, notice requirements)
- **A5.** Execute contract; distribute abstracted terms to operations {produces: contract summary/matrix}
- **D1.** Renew, renegotiate, or terminate?
  - Inputs: payer scorecard, market position, volume dependence, alternative networks
  - ├─ Acceptable performance → renew/light renegotiation
  - ├─ Underperforming → full renegotiation with escalation plan and term-notice leverage
  - └─ Irreparable → issue termination notice; patient-transition and continuity-of-care planning
- **D2.** Accept payer-proposed amendment (unilateral policy incorporation)?
  - ├─ Materially adverse → object within contract window; negotiate
  - └─ Acceptable → acknowledge; operationalize (11.2)

## 11.2 Contract Implementation & Maintenance
- **A1.** Load contract terms into expected-pay/contract engine: rate tables, groupers, carve-outs,
  lesser-of logic, effective dates
- **A2.** Test loads against known claims (parallel calculation validation) before go-live
- **A3.** Maintain term changes (fee schedule updates, escalator effective dates, amendment loads)
- **A4.** Publish operational contract matrices: timely filing, auth requirements, appeal windows,
  notification rules — consumed by 1.4.1, 6.5.3, 8.1.A4
- **D1.** Variance analysis (9.4) shows engine-vs-contract discrepancy?
  - ├─ Load error → correct engine; recalc affected claims; notify underpayment team of false variances
  - └─ Interpretation dispute → contracting clarifies with payer; document interpretation

## 11.3 Payer Policy & Bulletin Monitoring
- **A1.** Monitor payer bulletins/newsletters/portal announcements and regulatory transmittals
  (MLN Matters, MAC updates) on a defined cadence
- **A2.** Assess operational impact of each change (new auth list entries, edit changes, site-of-care
  policies, documentation requirements)
- **A3.** Route changes to owners with due dates: auth grids (1.4.1), edits (6.2.4), CDM (3.3),
  coding guidance (5.x), contract objections (11.1.D2)
- **A4.** Verify implementation and track policy-change-driven denial spikes {links: 8.5}

## 11.4 Provider Credentialing
- **A1.** Intake new practitioners; collect application data, licensure, DEA, board certs, work
  history, malpractice history, references
- **A2.** Perform primary source verification (PSV) on all credentials
- **A3.** Run committee review/approval; grant privileges (facility) per medical staff process
- **A4.** Track expirables (licenses, DEA, certs, insurance) with renewal workflows
- **A5.** Re-credential on cycle (typically 2–3 years); monitor sanctions/exclusions continuously
  (OIG LEIE, SAM, state boards)
- **D1.** Adverse finding during credentialing/monitoring?
  - ├─ Disqualifying → deny/suspend; stop billing under that provider; assess claims exposure
  - └─ Reviewable → committee evaluation with conditions

## 11.5 Payer Enrollment & Revalidation
- **A1.** Enroll providers/entities with each payer: Medicare (855A/855B/855I via PECOS), Medicaid
  per state, commercial payer applications, CAQH profile maintenance/attestation
- **A2.** Manage group linkages, reassignment of benefits, locum tenens arrangements
- **A3.** Track effective dates by payer; hold/queue claims until enrollment effective {gates: 6.3}
- **A4.** Process revalidations by deadline (missed revalidation = deactivation = claim rejections)
- **A5.** Maintain delegated credentialing rosters and submissions where delegated agreements exist
- **A6.** Maintain provider directory data accuracy (regulatory requirement; also drives OON denials)
- **D1.** Claims denying for provider-not-enrolled?
  - ├─ Enrollment pending, retro-effective available → hold and release on effective date; rebill
  - ├─ Enrollment defect → cure defect; appeal denials with effective-date evidence
  - └─ True gap (never enrolled) → enrollment initiation; assess write-off exposure & prevention gap

## 11.6 Payer Relations & Joint Operating Committees
- **A1.** Maintain named payer contacts/provider-rep relationships per payer
- **A2.** Run JOC meetings on cadence: aging inventory of disputes, systemic denial/underpayment
  projects (from 8.5/9.4), policy disputes, SLA performance
- **A3.** Track payer commitments to resolution with dollar accountability
- **A4.** Escalate failed commitments: contract remedies, regulatory complaints (DOI, CMS for MA),
  network strategy input (11.1.D1)
- **A5.** Produce internal payer scorecards for negotiation leverage {feeds: 11.1.A2}

## 11.7 Value-Based & Alternative Payment Model Administration
- **A1.** Administer VBC contracts: attribution reconciliation, quality measure tracking/submission,
  care-gap data exchange with payers
- **A2.** Reconcile shared savings/risk settlements: validate payer settlement calculations
  (claims runout, truncation, risk adjustment) before acceptance
- **A3.** Manage capitation operations: membership/roster reconciliation, PMPM payment validation,
  stop-loss tracking, division-of-financial-responsibility (DOFR) adjudication for delegated risk
- **A4.** Manage bundled payment episodes: episode triggering, cost tracking vs target, gainsharing
  distribution, post-acute utilization visibility
- **A5.** Ensure risk-adjustment data completeness (encounter submission acceptance rates,
  RAPS/EDS-equivalent monitoring) {links: 4.4, 12.3}
- **D1.** Settlement statement disagrees with internal model?
  - ├─ Material variance → formal dispute with data exhibits within contract window
  - └─ Within tolerance → accept; book settlement (13.3)

**Failure modes:** unloaded/misloaded contract terms, missed revalidation deactivations,
credentialing lapses stopping billing, unobjected adverse amendments, directory inaccuracy
penalties, settlement acceptance without validation.
**Metrics:** contract yield vs modeled, % claims priced by engine, enrollment turnaround days,
credentialing cycle time, expirable-lapse incidents, JOC issue resolution rate/dollars, VBC
settlement accuracy.

## Relationships
- 11.2.A4 `produces` the operational matrices consumed by 1.4.1, 6.5.3, 8.1.A4, 9.1.A3
- 11.5.A3 `gates` 6.3 for new providers; 11.4 continuous monitoring `governs` billable status
- 8.5/9.4 systemic findings `escalate-to` 11.6 and inform 11.1 negotiations
- 11.7 `consumes` 4.4 documentation programs and `feeds` 13.x performance reporting
