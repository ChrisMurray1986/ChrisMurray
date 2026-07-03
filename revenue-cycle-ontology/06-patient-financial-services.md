# RC-10 Patient Financial Services (Patient Billing & Collections)

Manages the patient-pay portion of the receivable after (or in absence of) insurance: statements,
customer service, payment plans, financial assistance, self-pay strategy, agency management, and
patient-protection compliance.

Roles: Patient Account Rep, Customer Service Rep, Financial Assistance Counselor, Self-Pay
Strategy Analyst, Agency Liaison, PFS Director. Systems: statement engine/print vendor, patient
portal & payment tools, propensity-to-pay scoring, FA screening tools, agency interfaces,
call center platform (telephony, QA recording).

---

## 10.1 Patient Statement & Communication Management
- **A1.** Qualify balances for statementing: insurance fully adjudicated (or valid self-pay), no
  active dispute/FA application hold, correct guarantor
- **A2.** Generate statements on cycle (e.g., 30-day) with plain-language design: services, insurance
  paid, patient owes, due date, contact and assistance options
- **A3.** Deliver via preferred channel (paper, e-statement, portal/text push); manage undeliverables
  (returned mail → address hygiene → skip trace)
- **A4.** Sequence dunning series (statement 1..N, pre-collect letter/call) with required
  501(r) plain-language FA notification on statements
- **A5.** Suppress statements appropriately: pending Medicaid/FA application, active insurance
  correction, bankruptcy, deceased-pending-estate
- **D1.** Balance truly patient-owed before first statement?
  - Inputs: remit patient-liability coding, COB completeness, denial state
  - ├─ Yes → statement cycle
  - ├─ Insurance issue outstanding → hold; resolve payer first (never dun patients for payer defects)
  - └─ NSA-protected OON amount → limit to in-network cost-share (10.7)
- **D2.** Statement cycle exhausted without payment/contact?
  - ├─ FA presumptive score high → presumptive charity (10.4)
  - ├─ Collectible score → pre-collect intensification → bad debt eligibility (9.7.A3)
  - └─ Uncollectible/small → administrative disposition

## 10.2 Patient Customer Service & Dispute Resolution
- **A1.** Handle inbound channels (phone, portal messages, chat, walk-in) within service levels
- **A2.** Authenticate caller; resolve inquiry types: itemized bill requests, insurance
  re-verification ("my insurance should have paid"), balance explanation, estimate-vs-final
  questions, payment/receipt issues, refund requests
- **A3.** Execute account actions in-call: update coverage → rebill (8.3 pattern), take payment,
  set plan, initiate FA screening, correct demographics
- **A4.** Log all contacts with disposition codes; escalate unresolved cases to research team with SLA
- **A5.** Run QA scoring on interactions; capture complaint taxonomy {feeds-back-to 8.5/1.x}
- **D1.** Patient disputes charge validity?
  - ├─ Billing error confirmed → correct, adjust, apologize; root-cause log
  - ├─ Charges valid → provide itemized bill + explanation; offer audit walkthrough
  - ├─ Estimate variance ≥ threshold (self-pay GFE >$400) → dispute-resolution rights (10.7)
  - └─ Unresolvable disagreement → formal grievance path; hold collections during review

## 10.3 Payment Plans & Financing
- **A1.** Offer standardized plan terms by balance band (duration, minimum payment, interest-free
  policy); document agreement
- **A2.** Enroll with autopay tokenization where consented; schedule installments
- **A3.** Monitor plan compliance; dunning for missed installments; re-age or default per terms
- **A4.** Manage third-party patient financing partnerships (recourse vs non-recourse terms,
  patient-protection guardrails); reconcile funded amounts
- **A5.** Consolidate new visits into existing plans per policy
- **D1.** Requested terms exceed standard matrix?
  - ├─ Within supervisor authority → approve exception; document
  - ├─ Hardship indicators → route to FA screening instead (10.4)
  - └─ Beyond authority → manager review

## 10.4 Financial Assistance / Charity Care (501(r))
- **A1.** Maintain FA policy artifacts: FAP, plain-language summary, application, provider list;
  publish and translate per regulation
- **A2.** Screen proactively (POS, counseling, statements, agency return files) and on request
- **A3.** Process applications: income/household documentation, FPL calculation, sliding scale
  determination
- **A4.** Run presumptive eligibility scoring (credit-data models, Medicaid proxy) for
  non-responders before bad debt
- **A5.** Apply determinations: full/partial write-off with FA transaction codes; refund amounts
  collected beyond AGB where applicable; notify patient
- **A6.** Enforce 501(r) mechanics: AGB calculation method maintained, ECA restrictions during
  application periods, 240-day application window handling
- **D1.** FA determination?
  - ├─ Approved full → close balance to charity; cease collections
  - ├─ Approved partial/sliding → bill residual with plan offer
  - ├─ Incomplete application → notice with cure period; hold ECAs
  - └─ Denied → document; resume standard cycle with appeal option

## 10.5 Self-Pay Segmentation & Early-Out Programs
- **A1.** Score accounts (propensity to pay, balance, FA likelihood) at self-pay inception
- **A2.** Assign treatment tracks: digital-first self-service, standard cycle, high-touch outreach,
  presumptive charity
- **A3.** Manage early-out vendor (pre-bad-debt outsourcing): placement files, brand/script
  standards, remittance reconciliation, recall rules
- **A4.** Monitor vendor compliance (call recordings, complaint rates, FDCPA-adjacent standards)

## 10.6 Bad Debt & Collection Agency Management
- **A1.** Certify placement eligibility (9.7.A3 gate: cycle complete, FA screened, no disputes/stays)
- **A2.** Transmit placements with data file standards; record agency, date, amount
- **A3.** Reconcile agency activity monthly: collections, remittances, commissions, inventory,
  cancel/recall list
- **A4.** Process agency-returned accounts (uncollectible closure, FA discovery, disputes back to PFS)
- **A5.** Govern ECAs (extraordinary collection actions): credit reporting, litigation, liens —
  board-approved policy, 501(r) timing rules, prohibited-action list
- **A6.** Audit agencies (licensure, complaint handling, data security); manage secondary placement
- **D1.** Agency requests legal action on an account?
  - ├─ Meets policy criteria (balance, asset verification, no hardship flags) + leadership approval → authorize
  - └─ Otherwise → decline; continue standard efforts or close
- **D2.** Payment received in-house on placed account?
  - ├─ Report to agency per contract (commission handling) → adjust inventories both sides

## 10.7 No Surprises Act Patient Protections
- **A1.** Identify NSA-protected scenarios: OON emergency, OON ancillary at in-network facility,
  OON where consent not obtained/invalid
- **A2.** Limit patient liability to in-network cost-share; route provider-payer difference to
  NSA payment dispute/IDR (8.4.5.A5)
- **A3.** Administer notice-and-consent artifacts where balance billing is permitted (1.9.3.A3)
- **A4.** Operate GFE patient-provider dispute resolution: respond to initiated disputes with
  documentation; process SDR (selected dispute resolution) outcomes; adjust balances per determination
- **A5.** Monitor state balance-billing laws layering over federal rules

**Failure modes:** dunning patients for payer-owed balances, FA-eligible accounts sent to bad
debt, statement suppression leaks, plan payment application errors, ECA taken during protected
window, NSA balance-billing violation.
**Metrics:** self-pay cash yield, statement-to-payment conversion, plan default rate, FA
approval turnaround, charity vs bad-debt classification accuracy, agency net-back %, complaint
rate per 1,000 statements.

## Relationships
- 10.1.D1 `consumes` remit liability coding (7.1.3) — posting accuracy gates fair patient billing
- 10.4 `gates` 10.6 (FA screen precedes placement); 9.7.A3 `gates` 10.6.A1
- 10.2 defect taxonomy `feeds-back-to` 8.5 and 1.6 (estimate accuracy)
- 10.7 `governed-by` NSA/state law; interacts with 8.4.5 IDR
