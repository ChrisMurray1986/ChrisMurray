# Master Taxonomy — Revenue Cycle Operations

Complete hierarchical index of domains → processes → sub-processes. Decisions and actions for
each sub-process are detailed in the domain files.

## RC-01 Patient Access & Financial Clearance (`01-patient-access.md`)

- **1.1 Scheduling & Appointment Management**
  - 1.1.1 Order intake & triage
  - 1.1.2 Appointment scheduling
  - 1.1.3 Referral capture at scheduling
  - 1.1.4 Reschedule / cancellation / no-show management
  - 1.1.5 Direct/emergency arrivals (unscheduled)
- **1.2 Pre-Registration**
  - 1.2.1 Demographic capture & verification
  - 1.2.2 Insurance capture
  - 1.2.3 Pre-registration outreach & self-service
  - 1.2.4 Medicare Secondary Payer (MSP) questionnaire
- **1.3 Eligibility & Benefits Verification**
  - 1.3.1 Automated eligibility inquiry (270/271)
  - 1.3.2 Manual verification & discrepancy resolution
  - 1.3.3 Benefits detailing (coverage, cost-share, limits)
  - 1.3.4 Coordination of benefits determination
  - 1.3.5 Coverage discovery / insurance finding
- **1.4 Prior Authorization, Pre-Certification & Referral Management**
  - 1.4.1 Auth requirement determination
  - 1.4.2 Auth initiation & clinical submission
  - 1.4.3 Auth status tracking & follow-up
  - 1.4.4 Peer-to-peer & auth denial handling (pre-service)
  - 1.4.5 Referral validation
  - 1.4.6 Auth-to-service reconciliation (changes in service/date/CPT)
- **1.5 Medical Necessity & Coverage Screening**
  - 1.5.1 NCD/LCD medical necessity check
  - 1.5.2 ABN / notice-of-noncoverage issuance
  - 1.5.3 Experimental/investigational & benefit-exclusion screening
- **1.6 Price Estimation & Good Faith Estimates**
  - 1.6.1 Insured patient estimate generation
  - 1.6.2 Good Faith Estimate (uninsured/self-pay, No Surprises Act)
  - 1.6.3 Estimate delivery & documentation
- **1.7 Financial Counseling & Financial Clearance**
  - 1.7.1 Financial clearance workflow & risk scoring
  - 1.7.2 Financial counseling session
  - 1.7.3 Coverage enrollment assistance (Medicaid, exchange, COBRA)
  - 1.7.4 Pre-service deposit & payment arrangement
  - 1.7.5 Clearance disposition (clear / conditional / defer)
- **1.8 Point-of-Service (POS) Collections**
  - 1.8.1 POS collection workflow
  - 1.8.2 POS payment processing & receipting
  - 1.8.3 POS cash controls & reconciliation
- **1.9 Registration / Arrival / Admission (ADT)**
  - 1.9.1 Check-in & identity verification
  - 1.9.2 Full registration & consent capture
  - 1.9.3 Regulatory notices (IMM, MOON, NSA disclosures)
  - 1.9.4 Admission / bed management events (ADT)
  - 1.9.5 Registration quality assurance
  - 1.9.6 Special account types (WC, auto/liability, research, occupational)

## RC-02 Utilization Review & Case Management (`02-mid-cycle.md`)

- **2.1 Admission Status Determination**
  - 2.1.1 Initial status review (IP vs OBS vs OP)
  - 2.1.2 Two-midnight / criteria application
  - 2.1.3 Condition Code 44 / self-denial process
  - 2.1.4 Physician advisor review
- **2.2 Concurrent Review & Payer Notification**
  - 2.2.1 Admission notification to payer
  - 2.2.2 Concurrent clinical reviews to payer
  - 2.2.3 Continued-stay authorization management
  - 2.2.4 Concurrent denial & peer-to-peer management
- **2.3 Discharge & Level-of-Care Transitions**
  - 2.3.1 Discharge planning coordination (revenue-affecting elements)
  - 2.3.2 Avoidable day tracking
  - 2.3.3 Post-acute authorization coordination
- **2.4 Retrospective Utilization Review**

## RC-03 Charge Capture & Revenue Integrity (`02-mid-cycle.md`)

- **3.1 Charge Generation & Entry**
  - 3.1.1 Order/documentation-driven automated charging
  - 3.1.2 Manual charge entry
  - 3.1.3 Departmental charge capture (OR, ED, pharmacy, supplies, infusion)
  - 3.1.4 Professional charge capture (charge tickets, mobile capture)
- **3.2 Charge Reconciliation**
  - 3.2.1 Daily department reconciliation
  - 3.2.2 Missing charge identification
  - 3.2.3 Late charge processing
- **3.3 Charge Description Master (CDM) Management**
  - 3.3.1 CDM item add/change/inactivate
  - 3.3.2 Annual code update maintenance (CPT/HCPCS/revenue codes)
  - 3.3.3 Pricing updates & strategic pricing review
  - 3.3.4 CDM audit & synchronization across systems
- **3.4 Revenue Integrity Auditing**
  - 3.4.1 Pre-bill charge review edits
  - 3.4.2 Retrospective charge audits
  - 3.4.3 Revenue guardian / charge trend surveillance
  - 3.4.4 Defense audits of itemized bills
- **3.5 Price Transparency Operations**
  - 3.5.1 Machine-readable file production & publication
  - 3.5.2 Shoppable services / consumer display maintenance

## RC-04 Clinical Documentation Integrity (`02-mid-cycle.md`)

- **4.1 Concurrent Documentation Review**
- **4.2 Physician Query Process**
- **4.3 CDI–Coding DRG Reconciliation**
- **4.4 Risk Adjustment / HCC Documentation Programs**
- **4.5 CDI Metrics, Education & Escalation**

## RC-05 Coding (`02-mid-cycle.md`)

- **5.1 Record Preparation & Work Distribution**
  - 5.1.1 Documentation completeness check / DNFB-DNFC management
  - 5.1.2 Coding work queue assignment
- **5.2 Inpatient Facility Coding**
- **5.3 Outpatient Facility Coding** (same-day surgery, ED, ancillary, observation)
- **5.4 Professional Fee Coding** (E/M, procedures, split/shared, teaching rules)
- **5.5 Specialty Coding** (interventional, anesthesia, radiation onc, home health/OASIS, SNF/PDPM)
- **5.6 Computer-Assisted & Autonomous Coding Oversight**
- **5.7 Coding Quality Review & Education**
- **5.8 Coding Support for Edits, Denials & Audits**

## RC-06 Claims Production & Submission (`03-claims.md`)

- **6.1 Claim Generation**
  - 6.1.1 Bill-hold / suspense management
  - 6.1.2 Claim assembly (837I/837P; UB-04/CMS-1500)
  - 6.1.3 Claim splitting/combining rules (interim, series, 72-hour rule)
- **6.2 Claim Editing & Scrubbing**
  - 6.2.1 System edits (HIS/PB billing edits)
  - 6.2.2 Scrubber/clearinghouse edits (NCCI, MUE, OCE, payer-specific)
  - 6.2.3 Edit resolution workflow
  - 6.2.4 Edit rule maintenance & false-positive tuning
- **6.3 Claim Submission & Acknowledgment**
  - 6.3.1 Electronic submission & batching
  - 6.3.2 Acknowledgment processing (999, 277CA)
  - 6.3.3 Rejection management (front-end rejects)
  - 6.3.4 Paper claim production
  - 6.3.5 Claim attachments (275, portal, fax)
- **6.4 Secondary, Tertiary & Special Claims**
  - 6.4.1 COB claim generation with primary remittance data
  - 6.4.2 Medicare crossover management
  - 6.4.3 Workers' comp / auto / liability claim packaging
- **6.5 Corrected, Late & Void Claims**
  - 6.5.1 Corrected/replacement claim (frequency 7) processing
  - 6.5.2 Void/cancel (frequency 8) processing
  - 6.5.3 Timely filing management & exception handling

## RC-07 Remittance Processing & Payment Posting (`04-payments.md`)

- **7.1 Electronic Remittance (835) Processing**
  - 7.1.1 835 receipt, validation & loading
  - 7.1.2 Auto-posting & exception queue
  - 7.1.3 CARC/RARC mapping & action coding
- **7.2 Manual & Paper Remittance Posting**
- **7.3 Payment Reconciliation & Treasury**
  - 7.3.1 EFT-to-835 matching
  - 7.3.2 Bank deposit / lockbox reconciliation
  - 7.3.3 Unapplied & unidentified cash resolution
- **7.4 Adjustment Posting & Variance Detection**
  - 7.4.1 Contractual adjustment posting
  - 7.4.2 Expected-vs-actual variance flagging (over/underpayment)
  - 7.4.3 Take-back / recoupment / reversal processing
- **7.5 Patient Payment Processing** (portal, IVR, mail, POS, plans)
- **7.6 Cash Application Controls & Balancing**

## RC-08 Denials Management & Appeals (`05-denials-ar.md`)

- **8.1 Denial Identification & Classification**
- **8.2 Denial Triage & Routing**
- **8.3 Denial Resolution (non-appeal paths)** — rebill, corrected claim, redirect, W/O
- **8.4 Appeals Management**
  - 8.4.1 Appeal decision & prioritization
  - 8.4.2 Appeal letter/packet construction
  - 8.4.3 Clinical appeals (medical necessity, DRG, level of care)
  - 8.4.4 Administrative/technical appeals
  - 8.4.5 Appeal levels & escalation (incl. Medicare ALJ path, external review, IDR)
  - 8.4.6 Appeal outcome processing
- **8.5 Denial Prevention Program** — root cause, feedback loops, payer trend escalation
- **8.6 Write-Off Governance & Adjustment Approval**

## RC-09 AR Management & Follow-Up (`05-denials-ar.md`)

- **9.1 Work Prioritization & Inventory Management**
- **9.2 Claim Status Determination** (276/277, portals, calls, bots)
- **9.3 No-Response / Unadjudicated Claim Follow-Up**
- **9.4 Underpayment Recovery**
- **9.5 Credit Balance & Refund Management** (payer, patient, escheatment, 60-day rule)
- **9.6 Small Balance & Administrative Resolution**
- **9.7 Aged AR, Reserves & Bad Debt Transfer**
- **9.8 Special Account Resolution** (WC/liability liens, estates, bankruptcy, hospice/VA)

## RC-10 Patient Financial Services (`06-patient-financial-services.md`)

- **10.1 Patient Statement & Communication Management**
- **10.2 Patient Customer Service & Dispute Resolution**
- **10.3 Payment Plans & Financing**
- **10.4 Financial Assistance / Charity Care (501(r))**
- **10.5 Self-Pay Segmentation & Early-Out Programs**
- **10.6 Bad Debt & Collection Agency Management**
- **10.7 No Surprises Act Patient Protections** (balance-billing limits, patient-provider dispute)

## RC-11 Payer Contracting, Credentialing & Enrollment (`07-payer-contracting.md`)

- **11.1 Contract Strategy, Modeling & Negotiation**
- **11.2 Contract Implementation & Maintenance** (terms loading, expected-pay engines)
- **11.3 Payer Policy & Bulletin Monitoring**
- **11.4 Provider Credentialing** (primary source verification, committees)
- **11.5 Payer Enrollment & Revalidation** (855 forms, CAQH, delegated rosters)
- **11.6 Payer Relations & Joint Operating Committees**
- **11.7 Value-Based & Alternative Payment Model Administration**

## RC-12 Compliance, Audit & Program Integrity (`08-compliance-audit.md`)

- **12.1 External Government Audit Response** (RAC, MAC/TPE, CERT, UPIC, OIG, MIC/state)
- **12.2 Commercial Payer Audit Response**
- **12.3 Internal Audit & Monitoring Program**
- **12.4 Overpayment Identification & Refund (60-day rule, self-disclosure)**
- **12.5 Regulatory Change Management**
- **12.6 Billing Compliance Investigations & Education**
- **12.7 Privacy & Security in Billing Operations**

## RC-13 Analytics, Reporting & Performance Management (`09-analytics-support.md`)

- **13.1 KPI Definition & Data Governance**
- **13.2 Operational Reporting & Work-Driver Analytics**
- **13.3 Month-End Close & Revenue Recognition Support**
- **13.4 Predictive & AI-Enabled Analytics**
- **13.5 Benchmarking & Executive Performance Review**

## RC-14 Master Data, Technology & Vendor Operations (`09-analytics-support.md`)

- **14.1 Master Data Management** (payer/plan master, provider master, dictionaries)
- **14.2 Revenue Cycle System Configuration & Maintenance**
- **14.3 EDI & Trading Partner Management**
- **14.4 Bot/Automation Fleet Operations**
- **14.5 Vendor Management & Outsourcing Oversight**
- **14.6 Business Continuity & Downtime Billing Procedures**
