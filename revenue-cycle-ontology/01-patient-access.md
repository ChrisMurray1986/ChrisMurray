# RC-01 Patient Access & Financial Clearance

Front-end domain: all work from first patient contact through arrival that establishes *who* the
patient is, *who pays*, *whether the service is covered and authorized*, *what the patient owes*,
and *whether the account is financially cleared* before (or at) service.

Primary roles: Scheduler, Pre-Registration Rep, Financial Clearance Specialist, Insurance
Verifier, Authorization Specialist, Financial Counselor, Registrar, Patient Access Supervisor.
Primary systems: EHR/HIS scheduling & registration modules, eligibility engine (270/271), auth
management tool, estimation engine, payment processing, RTE clearinghouse, payer portals.

---

## 1.1 Scheduling & Appointment Management

### 1.1.1 Order intake & triage
- **A1.** Receive order/referral (fax, e-fax, EHR order, portal, phone) {produces: pending order}
- **A2.** Index order to correct patient (match/create medical record number)
- **A3.** Validate order completeness (ordering provider, NPI, diagnosis, exact service, laterality, signature, date)
- **A4.** Verify ordering provider is credentialed/enrolled and not on exclusion list (OIG/SAM)
- **A5.** Triage order by urgency (STAT, urgent, routine) and route to scheduling queue
- **D1.** Is the order complete and valid?
  - Inputs: order fields, payer requirements, protocol library
  - ├─ Complete → proceed to scheduling (1.1.2)
  - ├─ Incomplete/illegible → contact ordering office for correction; hold order
  - └─ Clinically inappropriate for setting → route to clinical review / redirect service
- **D2.** Does the service require pre-service clinical protocol review (e.g., imaging appropriateness, CDSM/AUC)?
  - ├─ Yes → run clinical decision support; capture consultation identifier → then schedule
  - └─ No → schedule directly

### 1.1.2 Appointment scheduling
- **A1.** Identify or create patient record (search by name/DOB/SSN fragment; avoid duplicate MRN)
- **A2.** Select service, location, resource, provider per scheduling protocol
- **A3.** Check payer network/site-of-care rules before offering slots (steerage, site-of-service policies)
- **A4.** Offer and book slot; set visit type, duration, prep instructions
- **A5.** Capture minimum demographic + insurance data set at booking
- **A6.** Link order/referral to appointment
- **A7.** Send confirmation and prep instructions (SMS/email/portal/letter)
- **A8.** Flag account for downstream financial clearance queue {triggers: 1.7.1}
- **A9.** Derive intended procedure code(s) (CPT/HCPCS) from the order, order set, or visit-type
  build {produces: intended CPT set} — the lookup key for auth requirement determination (1.4.1),
  necessity screening (1.5.1), and estimation (1.6.1); intended-vs-performed mismatch is measured
  (reconciled at 1.4.6)
- **D1.** Is the requested provider in-network for the patient's plan?
  - ├─ In-network → book
  - ├─ Out-of-network → advise patient of OON implications; offer in-network alternative; if patient
    proceeds → capture NSA notice-and-consent where permitted (1.9.3)
  - └─ Unknown plan → book provisionally; flag for verification (1.3)
- **D2.** Does lead time allow financial clearance before service date?
  - ├─ Yes → standard clearance track
  - ├─ No (short lead) → expedited clearance track; consider rescheduling high-risk services
  - └─ Emergent → bypass clearance; post-service clearance track

### 1.1.3 Referral capture at scheduling
- **A1.** Determine if plan is gatekeeper/HMO type requiring PCP referral
- **A2.** Obtain referral number, valid dates, visit count from PCP or payer portal
- **A3.** Record referral on account and decrement visit counts per visit
- **D1.** Is a required referral on file and valid for the date of service?
  - ├─ Yes → clear referral requirement
  - ├─ No → request referral from PCP; hold or reschedule if not obtained
  - └─ Expired/exhausted → request extension/new referral

### 1.1.4 Reschedule / cancellation / no-show management
- **A1.** Process reschedule; re-validate auth/referral date spans against new date {triggers: 1.4.6}
- **A2.** Process cancellation; release auth if not reusable; notify ordering provider
- **A3.** Record no-show; apply no-show policy (fee where permitted, outreach, re-book)
- **A4.** Work "missed without reschedule" list for revenue recapture and care continuity
- **D1.** Does the changed date invalidate the existing authorization?
  - ├─ Within auth span → keep auth; update appointment
  - └─ Outside span → request auth date change from payer before service

### 1.1.5 Direct/emergency arrivals (unscheduled)
- **A1.** Perform quick registration (ED quick-reg: name, DOB, complaint) per EMTALA — no payment discussion before medical screening exam
- **A2.** Complete full registration at bedside/after stabilization
- **A3.** Initiate notification-of-admission clock if admitted {triggers: 2.2.1}

**Failure modes:** wrong-patient booking (duplicate MRN), unlinked order, missed referral,
OON booking without disclosure, insufficient clearance lead time.
**Key metrics:** scheduling accuracy, order-to-appointment lag, no-show rate, % appointments
financially cleared before service.

---

## 1.2 Pre-Registration

### 1.2.1 Demographic capture & verification
- **A1.** Contact patient (call/portal/text link) ahead of service
- **A2.** Verify/collect legal name, DOB, sex/gender, address, phone, email, SSN (per policy), emergency contact
- **A3.** Verify identity against prior records; resolve near-duplicate records via MPI review
- **A4.** Run address validation (USPS) and update returned-mail flags
- **A5.** Capture guarantor (responsible party) and relationship; handle minor/guardian rules
- **D1.** Do submitted demographics conflict with existing MPI record?
  - ├─ Minor variance → update with audit trail
  - └─ Identity conflict (possible fraud/duplicate) → escalate to HIM MPI team; do not merge without review

### 1.2.2 Insurance capture
- **A1.** Collect payer, plan, member ID, group, subscriber, subscriber DOB/relationship
- **A2.** Capture card images (front/back) via portal or at arrival
- **A3.** Map payer/plan to correct plan code in payer master (critical: wrong plan mapping is a top denial driver)
- **A4.** Order coverages (primary/secondary/tertiary) per COB rules (birthday rule for dependents; Medicare Secondary Payer rules; retiree vs active)
- **D1.** Which coverage is primary?
  - Inputs: employment status, MSP questionnaire, dependents' plans, accident indicators, ESRD/entitlement facts
  - ├─ Commercial primary → sequence commercial first
  - ├─ Medicare primary → sequence Medicare first
  - ├─ Accident/TPL involved → set WC/auto/liability primary; capture claim number, adjuster, carrier (1.9.6)
  - └─ Undetermined → flag for COB resolution before billing (1.3.4)

### 1.2.3 Pre-registration outreach & self-service
- **A1.** Run auto-dialer/text campaigns for upcoming visits not yet pre-registered
- **A2.** Monitor portal pre-check-in completion; work incomplete list
- **A3.** Prioritize outreach by service value and clearance risk

### 1.2.4 Medicare Secondary Payer (MSP) questionnaire
- **A1.** Administer MSP questionnaire (required cadence: each admission; every 90 days for recurring outpatient)
- **A2.** Record MSP responses; set value codes/condition codes for claim
- **D1.** Do MSP answers indicate another payer is primary to Medicare?
  - ├─ Yes (working aged, WC, no-fault, liability, ESRD coordination) → sequence accordingly; document
  - └─ No → Medicare primary

**Failure modes:** eligibility denial from plan-mapping error, COB denial, returned mail,
duplicate MRN.
**Metrics:** pre-registration rate, demographic accuracy rate, MSP completion compliance.

---

## 1.3 Eligibility & Benefits Verification

### 1.3.1 Automated eligibility inquiry (270/271)
- **A1.** Trigger real-time 270 eligibility request at scheduling, T-3 days, and day-of-service
- **A2.** Parse 271 response: active/inactive, plan name, effective dates, service-type benefits
- **A3.** Auto-post verified coverage details to account; set verification status/timestamp
- **A4.** Maintain payer-specific eligibility query configuration: service-type codes requested,
  benefit-detail prompts, and follow-up query chains per payer — reviewed against payer companion
  guides and eligibility-denial patterns (a generic STC-30 query cannot return the benefit detail
  1.3.3 needs, no matter how diligent the verifier)
- **D1.** What did the 271 return?
  - ├─ Active coverage → proceed to benefits detailing (1.3.3)
  - ├─ Inactive/terminated → coverage discovery (1.3.5) + patient outreach for updated insurance
  - ├─ Patient not found → correct ID/demographics and re-run; if still not found → treat as unverified
  - └─ Payer system unavailable → retry per schedule; fall back to portal/phone (1.3.2)
- **D2.** Does the 271 show a different plan/product than registered (e.g., MA plan replacing traditional Medicare, managed Medicaid assignment)?
  - ├─ Yes → re-map plan code; re-check network status and auth requirements {feeds-back-to 1.4.1}
  - └─ No → continue

### 1.3.2 Manual verification & discrepancy resolution
- **A1.** Verify via payer portal or IVR/phone when RTE is unavailable or ambiguous
- **A2.** Document reference number, representative, date/time of verification
- **A3.** Resolve subscriber/dependent mismatches, name spelling, ID format errors

### 1.3.3 Benefits detailing
- **A1.** Capture: deductible (total/met), OOP max (total/met), copay, coinsurance by service type
- **A2.** Capture: in/out-of-network differentials, carve-outs (behavioral, lab, imaging vendors)
- **A3.** Capture: benefit limits (visit counts, lifetime/annual max), exclusions, waiting periods
- **A4.** Identify auth/referral requirements flagged in benefits {triggers: 1.4.1}
- **A5.** Identify plan-specific billing requirements (site-of-care policy, network lab steerage)
- **D1.** Is the scheduled service a covered benefit?
  - ├─ Covered → continue clearance
  - ├─ Not covered / exclusion → financial counseling for self-pay pricing or alternative coverage (1.7)
  - └─ Coverage unclear → request written benefit confirmation / predetermination from payer

### 1.3.4 Coordination of benefits determination
- **A1.** Query all reported payers for other-coverage flags in 271
- **A2.** Ask patient to update COB with payer when payer shows stale COB (common denial cause)
- **A3.** Document primacy decision and rationale on account
- **D1.** Do payers disagree about primacy?
  - ├─ Yes → obtain COB questionnaire results; escalate to payer COB units; hold claim release if needed
  - └─ No → finalize coverage order

### 1.3.5 Coverage discovery / insurance finding
- **A1.** Run coverage discovery vendor/tool sweep on self-pay and inactive-coverage accounts
- **A2.** Check state Medicaid eligibility files including retroactive eligibility
- **A3.** Validate discovered coverage with 270/271 before attaching
- **D1.** Was billable coverage found?
  - ├─ Yes → attach coverage; reclass from self-pay; verify timely filing feasibility
  - └─ No → continue self-pay pathway (1.7 / RC-10)

**Failure modes:** eligibility (CO-27/26) denials, COB denials (CO-22), benefit-max denials,
site-of-care redirection denials.
**Metrics:** verification rate before service, RTE hit rate, eligibility-related denial rate.

---

## 1.4 Prior Authorization, Pre-Certification & Referral Management

### 1.4.1 Auth requirement determination
- **A1.** Look up CPT/HCPCS + payer + plan + site in auth-requirements rules engine/payer grid
- **A2.** Confirm requirement via payer portal/278 inquiry when rules are stale or ambiguous
- **A3.** Document "no auth required" evidence (screenshot/reference number) — defensible proof for appeals
- **A4.** Maintain the auth-requirements grid as governed master data: versioned changes with
  source citations, sampled accuracy audits against current payer policy, staleness alarms
  (a wrong grid mass-produces false "no auth required" — the most expensive wrong answer)
- **D1.** Is authorization required for this service/payer/site?
  - ├─ Required → initiate auth (1.4.2)
  - ├─ Not required → document proof; clear requirement
  - ├─ Notification-only → send notification; document
  - └─ Delegated to medical group/IPA → route request to delegated entity

### 1.4.2 Auth initiation & clinical submission
- **A1.** Compile clinical package: order, notes, prior treatment/conservative therapy, imaging results
- **A2.** Submit via payer portal / 278 transaction / fax / phone; record submission timestamp
- **A3.** Answer payer medical-policy questionnaires (e.g., criteria-based instant approval paths)
- **A4.** Record auth request tracking number
- **D1.** Does the case meet the payer's published medical policy criteria?
  - ├─ Meets → submit standard
  - ├─ Marginal → strengthen documentation with provider before submitting; consider peer-to-peer readiness
  - └─ Does not meet → provider discussion: alternative service, criteria completion, or patient
    self-pay election with waiver

### 1.4.3 Auth status tracking & follow-up
- **A1.** Work pending-auth queue by date-of-service proximity
- **A2.** Poll payer portal/278 for status; call when aged beyond SLA
- **A3.** Record approval: auth number, approved CPTs, units, sites, valid date span
- **A4.** Verify approved details exactly match scheduled service {triggers: 1.4.6 if mismatch}
- **D1.** Auth still pending at T-48h before service?
  - ├─ Yes → escalate (payer expedite request, supervisor, provider office)
  - └─ Approved → clear
- **D2.** Service date arriving with no auth decision?
  - ├─ Reschedule → move service until auth obtained
  - ├─ Proceed at risk → document leadership approval; flag account for potential denial
  - └─ Urgent/emergent clinical need → proceed; use expedited/retro auth provisions

### 1.4.4 Peer-to-peer & pre-service auth denial handling
- **A1.** Schedule peer-to-peer between treating physician and payer medical director within payer window
- **A2.** Prepare physician with criteria gaps and talking points
- **A3.** Record P2P outcome; if overturned, capture new auth number
- **D1.** P2P outcome?
  - ├─ Approved → proceed to service
  - ├─ Upheld → pre-service appeal, alternative covered service, or patient self-pay election
  - └─ Partially approved (fewer units/different level) → provider decision: accept, appeal, or modify plan

### 1.4.5 Referral validation
- (See 1.1.3 for capture) — validate active referral covers the specific specialty/date/visit count
  and matches the rendering provider

### 1.4.6 Auth-to-service reconciliation
- **A1.** Compare performed service (post-service coding/CPT) to authorized CPT/units/date/site
- **A2.** Request auth updates for intraoperative changes, add-on procedures, date moves
- **A3.** For inpatient: reconcile authorized LOS/level-of-care to actual {links: 2.2.3}
- **D1.** Did the performed service deviate from what was authorized?
  - ├─ No → release for billing
  - ├─ Yes, payer allows post-service modification → request updated auth before claim release; hold claim
  - └─ Yes, payer refuses update → bill authorized portion / prepare denial defense; document clinical rationale

**Failure modes:** no-auth denial (CO-197), auth mismatch (CPT/date/units), expired auth, delegated-entity confusion.
**Metrics:** auth turnaround, % services with auth secured before service, auth-related denial rate & overturn rate.

---

## 1.5 Medical Necessity & Coverage Screening

### 1.5.1 NCD/LCD medical necessity check
- **A1.** Screen ordered CPT/HCPCS against diagnosis using NCD/LCD (Medicare) or payer policy edits
- **A2.** Request additional/corrected diagnosis from ordering provider when check fails
- **D1.** Does the diagnosis support medical necessity per policy?
  - ├─ Supported → clear
  - ├─ Not supported, provider adds valid dx → re-run; clear
  - └─ Not supported, no additional dx → issue ABN path (1.5.2)

### 1.5.2 ABN / notice-of-noncoverage issuance
- **A1.** Generate Advance Beneficiary Notice (Medicare) or payer-equivalent noncoverage waiver with
  specific service, reason, and cost estimate
- **A2.** Explain notice to patient; capture signed election (Option 1/2/3 on ABN)
- **A3.** Apply GA/GX/GY/GZ modifiers downstream per election {feeds: RC-05, RC-06}
- **D1.** Patient election?
  - ├─ Receive service & accept liability (bill Medicare) → proceed; append GA
  - ├─ Receive service, don't bill payer → self-pay; append GX/GY as applicable
  - └─ Decline service → cancel; notify ordering provider

### 1.5.3 Experimental/investigational & benefit-exclusion screening
- **A1.** Screen high-cost/novel services against payer investigational lists
- **A2.** Request predetermination in writing for gray-zone services
- **A3.** Route trial-related services to research billing review (coverage analysis; Qualifying
  Clinical Trial rules; route research-paid items to study account) {links: 1.9.6}

---

## 1.6 Price Estimation & Good Faith Estimates

### 1.6.1 Insured patient estimate generation
- **A1.** Assemble expected charges from scheduled service (CPT/DRG history-based models or CDM)
- **A2.** Apply contract terms (expected allowable) and real-time benefit accumulators (remaining deductible/OOP)
- **A3.** Produce patient responsibility estimate {produces: ART-Estimate}
- **A4.** Version and store estimate for later variance analysis and dispute defense
- **D1.** Is estimate confidence adequate (complete benefits + contract data)?
  - ├─ Yes → deliver estimate
  - └─ No → widen range/disclose assumptions; or complete verification first

### 1.6.2 Good Faith Estimate (uninsured/self-pay — No Surprises Act)
- **A1.** Identify GFE-eligible patients (uninsured or electing not to use insurance)
- **A2.** Generate GFE with itemized expected charges, provider/facility identifiers, disclaimers
- **A3.** Include co-provider/co-facility items as required; deliver within mandated timeframes
  (e.g., 3 business days after scheduling ≥10 days out)
- **A4.** Retain GFE; monitor final charges vs GFE for $400 dispute threshold {links: 10.7}

### 1.6.3 Estimate delivery & documentation
- **A1.** Deliver via portal/email/mail/verbal-with-documentation per patient preference
- **A2.** Record patient acknowledgment; answer estimate questions or route to counseling (1.7.2)

**Metrics:** estimate accuracy (estimate vs final liability), estimate coverage rate (% of
scheduled services with estimate), GFE timeliness compliance.

---

## 1.7 Financial Counseling & Financial Clearance

### 1.7.1 Financial clearance workflow & risk scoring
- **A1.** Aggregate clearance status: demographics verified, eligibility verified, auth secured,
  necessity cleared, estimate produced
- **A2.** Score financial risk (propensity to pay, balance size, coverage adequacy)
- **A3.** Route high-risk accounts to financial counselor; auto-clear low-risk complete accounts
- **D1.** Clearance disposition at review point?
  - ├─ Fully cleared → mark cleared; ready for arrival
  - ├─ Conditionally cleared (minor items open) → allow service; task remaining items
  - ├─ Not cleared, elective service → defer/reschedule per policy with leadership signoff
  - └─ Not cleared, urgent/emergent → proceed; route to post-service clearance

### 1.7.2 Financial counseling session
- **A1.** Review estimate, benefits, and out-of-pocket with patient
- **A2.** Present payment options: pay in full (prompt-pay discount), deposit, payment plan, financing
- **A3.** Screen for financial assistance eligibility (presumptive scoring, income/household size) {links: 10.4}
- **A4.** Document counseling outcome and commitments on account

### 1.7.3 Coverage enrollment assistance
- **A1.** Screen uninsured/underinsured for Medicaid, CHIP, exchange subsidies, COBRA, crime victims,
  county programs
- **A2.** Assist application submission; track application status through determination
- **A3.** Set account hold/self-pay-pending-Medicaid class while application pends
- **D1.** Application outcome?
  - ├─ Approved (incl. retroactive) → attach coverage; rebill window check
  - ├─ Denied → financial assistance screening / self-pay pathway
  - └─ Pending past service → manage under pending-Medicaid hold rules

### 1.7.4 Pre-service deposit & payment arrangement
- **A1.** Request deposit per policy for high-dollar elective services
- **A2.** Establish payment plan pre-service where allowed {links: 10.3}
- **D1.** Patient unable/unwilling to meet pre-service financial requirement (elective)?
  - ├─ FA-eligible → process assistance; proceed
  - ├─ Alternative arrangement approved → proceed with documented plan
  - └─ None → defer service per policy (never for emergent care)

### 1.7.5 Clearance disposition
- **A1.** Set final clearance status flag consumed by arrival workflow and revenue reporting
- **A2.** Publish daily uncleared-upcoming-service report; escalate exceptions

---

## 1.8 Point-of-Service (POS) Collections

### 1.8.1 POS collection workflow
- **A1.** Present amount due at check-in: copay + estimated deductible/coinsurance + prior balances
- **A2.** Use compliant scripting (ask for payment; offer options; never deny emergent care for nonpayment)
- **A3.** Record outcome (paid full/partial/declined) and reason codes
- **D1.** Patient offers partial payment?
  - ├─ Accept partial → receipt; set plan or bill remainder
  - └─ Declines → document; route to statement cycle; flag counseling if high balance

### 1.8.2 POS payment processing & receipting
- **A1.** Process card/cash/check/HSA-FSA; tokenize card-on-file with consent
- **A2.** Issue receipt; post payment to correct account/visit in real time
- **A3.** Apply prompt-pay/self-pay discount rules automatically

### 1.8.3 POS cash controls & reconciliation
- **A1.** Open/close cash drawer with counts; dual verification
- **A2.** Reconcile daily POS receipts to posting system and bank {links: 7.6}
- **A3.** Investigate overs/shorts; escalate per threshold

**Metrics:** POS collection rate, POS yield vs estimated collectible, drawer variance incidents.

---

## 1.9 Registration / Arrival / Admission

### 1.9.1 Check-in & identity verification
- **A1.** Verify identity with photo ID + two identifiers; photograph per policy
- **A2.** Match to correct MRN; guard against identity theft (red-flag rules)
- **A3.** Scan insurance card updates; re-run day-of-service eligibility (1.3.1)

### 1.9.2 Full registration & consent capture
- **A1.** Confirm/complete all demographic, guarantor, employer, accident fields
- **A2.** Capture consents: treatment, financial responsibility, assignment of benefits, HIPAA NPP
  acknowledgment, release of information
- **A3.** Collect advance directive information where required
- **A4.** Assign visit/account: patient type, service code, financial class, admit source
- **D1.** Correct patient type/financial class assigned for the service?
  - ├─ Yes → continue
  - └─ No/uncertain → correct now (wrong patient type drives billing rework and denials)

### 1.9.3 Regulatory notices
- **A1.** Deliver Important Message from Medicare (IMM) within required windows (admission & pre-discharge)
- **A2.** Deliver MOON (observation >24h notice) with required timing
- **A3.** Deliver NSA disclosures; process notice-and-consent for permitted OON balance billing
- **A4.** Deliver state-specific notices; document delivery, signatures, refusals

### 1.9.4 Admission / bed management events (ADT)
- **A1.** Process admit/transfer/discharge events; keep patient class synchronized with orders
- **A2.** Trigger payer notification requirements on admit {triggers: 2.2.1}
- **A3.** Process status change orders (OBS→IP, IP→OBS via CC44 path) {links: 2.1.3}

### 1.9.5 Registration quality assurance
- **A1.** Run daily registration QA edits (missing/invalid fields, plan-mapping checks)
- **A2.** Score registrar accuracy; deliver feedback and targeted training
- **A3.** Correct errors pre-bill {feeds-back-to: denial prevention 8.5}

### 1.9.6 Special account types
- **A1. Workers' comp:** capture employer, injury date, claim number, adjuster, WC carrier;
  obtain employer/carrier authorization; set WC financial class
- **A2. Auto/liability:** capture accident details, auto carrier, med-pay limits, attorney; evaluate
  lien filing rights {links: 9.8}
- **A3. Research:** apply coverage analysis grid — route study-paid items to sponsor account,
  standard-of-care to insurance with QCT indicators (Q0/Q1 modifiers, condition code 30)
- **A4. Occupational/employer-billed:** attach employer account and pricing agreement
- **A5. Confidential/VIP/safe-haven:** apply privacy flags without breaking billing linkage

**Failure modes:** wrong patient type, missed IMM/MOON (compliance + payment risk), missed
accident info (COB denials), unsigned consents.
**Metrics:** registration accuracy rate, day-of-service eligibility re-check rate, notice
compliance rate.

---

## Domain-level relationships

- 1.1 `precedes` 1.2 `precedes` 1.3 `precedes` 1.4/1.5 `precedes` 1.6 `precedes` 1.7 `precedes` 1.8/1.9
- 1.3.1.D2 `feeds-back-to` 1.4.1 (plan change re-triggers auth determination)
- 1.9.5 `feeds-back-to` denial prevention (8.5); 8.5 root causes `feed-back-to` 1.2/1.3/1.4 training
- 1.4.6 `gates` claim release (6.1.1)
- Emergency arrivals (1.1.5) `governed-by` EMTALA — financial activities deferred until screening/stabilization
