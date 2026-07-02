# Cross-Cutting Entity Registries

Reference registries for entities used across all domains: roles, systems, artifacts, events,
metrics, failure modes, and governing regulations.

---

## Roles (ROLE-*)

### Front end
| ID | Role | Primary domains |
|---|---|---|
| ROLE-SCHED | Scheduler / Order Intake Rep | 1.1 |
| ROLE-PREREG | Pre-Registration Representative | 1.2 |
| ROLE-VERIF | Insurance Verification Specialist | 1.3 |
| ROLE-AUTH | Authorization/Referral Specialist | 1.4 |
| ROLE-ESTIM | Estimate Analyst | 1.6 |
| ROLE-FINCOUNS | Financial Counselor | 1.7, 10.4 |
| ROLE-REGISTRAR | Registrar / Patient Access Rep | 1.8, 1.9 |
| ROLE-PA-QA | Patient Access QA Auditor | 1.9.5 |
| ROLE-PA-SUP | Patient Access Supervisor/Manager/Director | RC-01 |

### Mid cycle
| ID | Role | Primary domains |
|---|---|---|
| ROLE-URN | Utilization Review Nurse | 2.1–2.4 |
| ROLE-CM | Case Manager | 2.2, 2.3 |
| ROLE-PHYSADV | Physician Advisor | 2.1.4, 2.2.4, 4.2, 8.4.3 |
| ROLE-CHGANALYST | Charge Capture Analyst | 3.1, 3.2 |
| ROLE-DEPTCHG | Department Charge Owner | 3.1, 3.2 |
| ROLE-CDMANALYST | CDM Analyst | 3.3 |
| ROLE-REVINT | Revenue Integrity Analyst/Auditor | 3.4, 3.5 |
| ROLE-CDIS | CDI Specialist | 4.1–4.5 |
| ROLE-CODER-IP | Inpatient Coder | 5.2 |
| ROLE-CODER-OP | Outpatient Coder | 5.3 |
| ROLE-CODER-PRO | Professional Fee Coder | 5.4, 5.5 |
| ROLE-CODEAUD | Coding Auditor/Educator | 5.7 |
| ROLE-HIM | HIM Analyst / ROI Specialist / MPI Analyst | 5.1, 12.1, 1.2.1 |

### Back end
| ID | Role | Primary domains |
|---|---|---|
| ROLE-BILLER | Biller / Claims Specialist | 6.x |
| ROLE-EDITANALYST | Claims Edit Analyst | 6.2 |
| ROLE-POSTER | Payment Poster / Cash Applications Analyst | 7.1, 7.2 |
| ROLE-RECON | Treasury/Reconciliation Analyst | 7.3, 7.6 |
| ROLE-DENIAL | Denials Analyst | 8.1–8.3 |
| ROLE-APPEALRN | Appeals Nurse / Clinical Appeals Writer | 8.4.3 |
| ROLE-APPEALW | Appeals Specialist (administrative) | 8.4 |
| ROLE-ARFU | AR Follow-Up Representative | 9.1–9.3 |
| ROLE-UNDERPAY | Underpayment Analyst | 9.4 |
| ROLE-CREDIT | Credit Balance Analyst | 9.5 |
| ROLE-PFSREP | Patient Account / Customer Service Rep | 10.1, 10.2 |
| ROLE-FACOUNS | Financial Assistance Counselor | 10.4 |
| ROLE-AGCYLIAISON | Agency/Vendor Liaison | 10.5, 10.6, 14.5 |

### Cross-cutting & leadership
| ID | Role | Primary domains |
|---|---|---|
| ROLE-CONTRACT | Managed Care Contracting Analyst/Director | 11.1–11.3 |
| ROLE-CRED | Credentialing Specialist | 11.4 |
| ROLE-ENROLL | Payer Enrollment Specialist | 11.5 |
| ROLE-PAYERREL | Payer Relations Manager | 11.6 |
| ROLE-VBC | VBC/Population Health Program Manager | 11.7 |
| ROLE-COMPLIANCE | Compliance Officer / Billing Compliance Auditor | 12.x |
| ROLE-AUDITCOORD | Audit Response Coordinator | 12.1, 12.2 |
| ROLE-ANALYTICS | RC Analytics Manager / Data Analyst | 13.x |
| ROLE-SYSANALYST | RC Systems Analyst / Application Analyst | 14.1, 14.2 |
| ROLE-EDI | EDI Analyst | 14.3 |
| ROLE-AUTOENG | Automation Engineer (RPA) | 14.4 |
| ROLE-VENDORMGR | Vendor Manager | 14.5 |
| ROLE-CFO | CFO / VP Revenue Cycle / Executive Sponsor | governance, 8.6, 13.5 |
| ROLE-PROVIDER | Physician/Practitioner (documentation, orders, queries, P2P) | 1.1, 4.2, 2.x |
| ROLE-BOT | Automated agent (RPA bot, auto-poster, autonomous coder) | pervasive |

---

## Systems (SYS-*)

| ID | System | Functions supported |
|---|---|---|
| SYS-EHR | EHR/HIS (clinical + ADT) | orders, documentation, ADT, charge triggers |
| SYS-SCHED | Scheduling module | 1.1 |
| SYS-REG | Registration/patient access module | 1.2, 1.9 |
| SYS-PB-HB | Patient accounting (hospital & professional billing) | 6, 7, 8, 9, 10 |
| SYS-RTE | Real-time eligibility engine (270/271) | 1.3 |
| SYS-AUTHTOOL | Authorization management platform / 278 | 1.4 |
| SYS-ESTIMATOR | Price estimation engine | 1.6 |
| SYS-MEDNEC | Medical necessity/ABN screening (NCD/LCD edits) | 1.5 |
| SYS-URTOOL | UR criteria platform (MCG/InterQual) + CM module | 2.x |
| SYS-CDM | Charge description master | 3.3 |
| SYS-CHGCAP | Charge capture/reconciliation tools | 3.1, 3.2 |
| SYS-CDI | CDI workflow/prioritization (incl. NLP) | 4.x |
| SYS-ENCODER | Encoder/grouper (DRG/APC) | 5.x |
| SYS-CAC | Computer-assisted/autonomous coding | 5.6 |
| SYS-SCRUBBER | Claim scrubber/editor | 6.2 |
| SYS-CLRHOUSE | Clearinghouse | 6.3, 7.1, 14.3 |
| SYS-CONTRACT | Contract management + expected-pay engine | 11.2, 7.4.2, 9.4 |
| SYS-DENIALWF | Denial/appeal workflow platform | 8.x |
| SYS-WQ | Work-queue/workflow engine | 9.1 and pervasive |
| SYS-835ENGINE | Remittance processing/auto-posting | 7.1 |
| SYS-LOCKBOX | Bank lockbox & treasury feeds | 7.2, 7.3 |
| SYS-PATIENTPAY | Patient payment portal/IVR/kiosk/merchant processing | 7.5, 10.3 |
| SYS-STATEMENT | Statement engine/print-mail vendor | 10.1 |
| SYS-P2P-SCORE | Propensity-to-pay & FA presumptive scoring | 10.4, 10.5, 13.4 |
| SYS-CREDPLAT | Credentialing platform / CAQH / PECOS | 11.4, 11.5 |
| SYS-POLICYMON | Payer policy/bulletin monitoring service | 11.3, 12.5 |
| SYS-AUDITTRACK | Audit tracking system | 12.1, 12.2 |
| SYS-EDW | Data warehouse/BI stack | 13.x |
| SYS-RPA | RPA/bot platform | 14.4 |
| SYS-MRF | Price transparency MRF tooling | 3.5 |
| SYS-PAYERPORTAL | Payer web portals (per payer) | 1.3, 1.4, 8.4, 9.2 |

---

## Artifacts (ART-*)

### Transactions (X12/standard)
| ID | Artifact |
|---|---|
| ART-270/271 | Eligibility inquiry/response |
| ART-276/277 | Claim status inquiry/response |
| ART-277CA | Claim acknowledgment |
| ART-278 | Authorization request/response |
| ART-275 | Claim attachment |
| ART-837I/837P | Institutional/professional claim |
| ART-835 | Electronic remittance advice |
| ART-999 | Functional acknowledgment |
| ART-CCD+ | EFT with TRN trace |
| ART-UB04 | CMS-1450 paper institutional claim |
| ART-CMS1500 | Paper professional claim |

### Clinical/administrative documents
| ID | Artifact |
|---|---|
| ART-ORDER | Order/referral document |
| ART-AUTH | Authorization approval (number, span, CPTs, units) |
| ART-NOAUTHPROOF | "No auth required" evidence |
| ART-ABN | Advance Beneficiary Notice / noncoverage waiver |
| ART-IMM / ART-MOON | Medicare discharge/observation notices |
| ART-NSA-CONSENT | NSA notice-and-consent form |
| ART-ESTIMATE / ART-GFE | Patient estimate / Good Faith Estimate |
| ART-MSPQ | MSP questionnaire result |
| ART-CONSENTS | Treatment/financial/AOB/HIPAA consent set |
| ART-QUERY | Physician query (CDI/coding) |
| ART-CODESET | Final coded abstract (dx/px/POA/DRG/modifiers) |
| ART-EOB | Explanation of benefits (paper remit) |
| ART-DENIALLTR | Denial letter |
| ART-APPEAL | Appeal letter/packet |
| ART-STATEMENT | Patient statement |
| ART-FAP | Financial assistance policy/application/determination |
| ART-CONTRACT | Payer contract + amendments + abstracted term matrix |
| ART-CMS838 | Medicare quarterly credit balance report |
| ART-ADR | Additional documentation request + response package |
| ART-WQITEM | Work-queue item with next-action stamp (universal work token) |

---

## Events (EVT-*)

| ID | Event | Triggers |
|---|---|---|
| EVT-ORDER | Order/referral received | 1.1.1 |
| EVT-SCHED | Appointment booked/changed/cancelled | 1.1.2, 1.1.4, clearance re-checks |
| EVT-ARRIVAL | Patient arrival/check-in | 1.9, day-of-service eligibility |
| EVT-ADT | Admit/transfer/discharge/status change | 2.x, bill-hold clocks |
| EVT-DOCCOMPLETE | Documentation completion/signature | 5.1.1 release |
| EVT-CHARGE | Charge posted/late charge | 3.x, 6.5.1 |
| EVT-CODED | Coding finalized | claim generation eligibility |
| EVT-CLAIMOUT | Claim submitted | ack tracking, follow-up clocks |
| EVT-ACK | 999/277CA received | 6.3.2 |
| EVT-REMIT | 835/EOB received | 7.1, denial intake |
| EVT-DENIAL | Denial identified (any channel) | 8.1 |
| EVT-PAYMENT | Payment posted (payer/patient) | variance check, statement qualification |
| EVT-TAKEBACK | Recoupment/reversal | 7.4.3 |
| EVT-DEADLINE | Filing/appeal/audit deadline approaching | 6.5.3, 8.4, 12.1 escalations |
| EVT-STATEMENT | Statement cycle milestone | 10.1 dunning progression |
| EVT-FAAPP | FA application submitted/decided | 10.4 holds/releases |
| EVT-PLACEMENT | Agency placement/recall | 10.6 |
| EVT-CONTRACT | Contract effective/amended/terminated | 11.2 loads, matrices refresh |
| EVT-ENROLLCHANGE | Provider enrollment status change | claim hold/release (11.5) |
| EVT-AUDITREQ | External audit request received | 12.1, 12.2 |
| EVT-REGCHANGE | Regulation/payer policy change effective | 12.5, 11.3 |
| EVT-DOWNTIME | System outage begins/ends | 14.6 |

---

## Metrics (KPI-*) — canonical set

### Front end
- KPI-PREREG-RATE — % encounters pre-registered before service
- KPI-VERIF-RATE — % verified (eligibility/benefits) before service
- KPI-AUTH-RATE — % auth-required services authorized before service
- KPI-ESTIMATE-ACC — estimate vs final patient liability accuracy
- KPI-POS-CASH — point-of-service collections ($, % of collectible)
- KPI-REGQA — registration accuracy rate
- KPI-CLEARANCE — % financially cleared at service

### Mid cycle
- KPI-OBSRATE — observation rate; status-change rate; CC44 volume
- KPI-AVOIDDAYS — avoidable days
- KPI-CHGLAG — charge lag days; KPI-LATECHG — late charge %
- KPI-CAPTURE-ACC — charge audit accuracy (over/under)
- KPI-QUERYRATE / KPI-QUERYAGREE — CDI query rate & agreement rate
- KPI-CMI — case mix index trend
- KPI-CODEACC — coding accuracy %; KPI-DNFB / KPI-DNFC — unbilled days ($ and days)

### Claims → cash
- KPI-CLEANCLAIM — clean claim rate; KPI-FPY — first-pass yield
- KPI-CLAIMLAG — service/discharge-to-bill days
- KPI-REJRATE — front-end rejection rate
- KPI-AUTOPOST — 835 auto-post rate; KPI-POSTLAG — deposit-to-post days
- KPI-SUSPENSE — unapplied cash $ and age

### Denials & AR
- KPI-IDR — initial denial rate (% claims, % dollars) by category
- KPI-OVERTURN — denial overturn/appeal success rate by level
- KPI-DENWO — denial write-off % of net revenue
- KPI-DAR — net days in AR; KPI-AR90 — % AR > 90 days
- KPI-UNDERPAY — underpayment identified/recovered $
- KPI-CREDITDAYS — credit balance days-to-resolution
- KPI-CASHGOAL — cash collections vs expected/goal

### Patient financial
- KPI-SELFPAYYIELD — self-pay net collection rate
- KPI-PLANDEFAULT — payment plan default rate
- KPI-FA-TAT — financial assistance turnaround
- KPI-AGENCYNETBACK — agency net-back %
- KPI-COMPLAINTS — billing complaints per 1,000 statements

### Enterprise
- KPI-NCR — net collection rate (net revenue realized vs expected)
- KPI-CTC — cost to collect (% of cash)
- KPI-CONTRACTYIELD — actual vs modeled contract yield by payer
- KPI-AUDITWIN — external audit win rate; takeback net of appeal
- KPI-60DAY — overpayment refund timeliness compliance

---

## Failure modes (FM-*) — leakage & defect taxonomy

| ID | Failure mode | Origin | Detection | Primary prevention |
|---|---|---|---|---|
| FM-DUPMRN | Duplicate/wrong patient record | 1.1/1.2 | MPI audits, claim rejects | search discipline, biometric/ID verify |
| FM-PLANMAP | Wrong plan-code mapping | 1.2.2 | eligibility denials | payer master governance (14.1) |
| FM-ELIGLAPSE | Coverage inactive at service | 1.3 | CO-27 denials | day-of-service re-verification |
| FM-COB | Wrong payer order | 1.2/1.3 | CO-22 denials | MSPQ discipline, COB tooling |
| FM-NOAUTH | Missing/mismatched authorization | 1.4 | CO-197 denials | auth grid currency, auth-to-service reconciliation |
| FM-MEDNEC | Medical necessity unsupported | 1.5/5.x | payer denials, ABN gaps | necessity screening, dx capture |
| FM-NOTICEMISS | Missed IMM/MOON/NSA notice | 1.9.3 | compliance audits | arrival checklists, delivery tracking |
| FM-STATUSWRONG | Wrong patient status (IP/OBS) | 2.1 | payer downgrades, audits | early UR review, PA program |
| FM-CHGMISS | Missed charges (leakage) | 3.1/3.2 | revenue-usage analytics | reconciliation attestation, trend surveillance |
| FM-CHGDUP | Duplicate charges | 3.1 | edits, audits | trigger governance |
| FM-UNITERR | Drug/service unit errors | 3.1.3 | MUE edits, audits | NDC crosswalk maintenance |
| FM-CDMSTALE | Stale CDM (deleted codes, bad pairs) | 3.3 | edit spikes | annual update discipline, CDM audit |
| FM-DOCGAP | Documentation insufficient for acuity/necessity | 4.x | queries, clinical-validation denials | CDI coverage, provider education |
| FM-CODEERR | Coding error (over/under) | 5.x | audits, DRG denials | QA program, education loop |
| FM-DISPO | Wrong discharge disposition | 5.2 | transfer-rule under/overpay | disposition validation |
| FM-CLAIMDROP | Claim never reached payer | 6.3 | ack reconciliation | submission integrity loop |
| FM-REJECTUNWORKED | Front-end rejection unworked | 6.3.3 | rejection aging | daily queue discipline |
| FM-TFL | Timely filing missed | 6.5.3 | CO-29 denials | filing alarms, proof retention |
| FM-MISPOST | Payment misposted | 7.x | recon variances | batch balancing, QA |
| FM-DENIALHIDDEN | Denial posted as contractual adjustment | 7.1.3 | adjustment audits | CARC mapping governance |
| FM-VARIANCEMISS | Underpayment never flagged | 7.4.2 | contract audits | expected-pay engine coverage |
| FM-APPEALMISS | Appeal deadline missed | 8.4 | deadline reports | intake deadline stamping |
| FM-REBILLLOOP | Endless rebill without escalation | 8.3 | touch analytics | break-the-pattern review |
| FM-CREDITAGE | Credit balances aged | 9.5 | CMS-838, audits | daily credit work, root-cause fix |
| FM-PATIENTWRONGBILL | Patient billed for payer-owed/NSA-protected amount | 10.1/10.7 | complaints, audits | liability verification gate |
| FM-FA-MISS | FA-eligible patient sent to collections | 10.4/10.6 | presumptive screens, complaints | pre-placement FA screening gate |
| FM-ENROLLGAP | Provider enrollment lapse | 11.5 | enrollment denials | expirables tracking, claim holds |
| FM-TERMSUNLOADED | Contract terms not loaded/misloaded | 11.2 | variance analysis | load testing, parallel calc |
| FM-AMENDMISS | Adverse amendment unobjected | 11.1 | yield erosion | amendment intake calendar |
| FM-AUDITDEADLINE | ADR/audit response late | 12.1 | auto-denials | centralized audit intake |
| FM-60DAY | Overpayment held past deadline | 12.4 | compliance audit | central overpayment log |
| FM-EDISILENT | Silent EDI file failure | 14.3 | volume anomaly alarms | pipeline monitoring |
| FM-BOTSILENT | Bot failure silently dropping work | 14.4 | success-rate monitors | exception routing mandate |

---

## Governing regulations & standards (REG-*)

| ID | Regulation/standard | Constrains |
|---|---|---|
| REG-EMTALA | Emergency screening before financial activity | 1.1.5, 1.8 |
| REG-HIPAA | Privacy/security, transaction standards (X12) | all data movement, 12.7, 14.3 |
| REG-NSA | No Surprises Act: GFE, balance-billing limits, IDR | 1.6.2, 10.7, 8.4.5 |
| REG-PRICETRANS | Hospital price transparency (MRF, shoppables) | 3.5 |
| REG-2MIDNIGHT | Two-midnight rule / inpatient-only list | 2.1 |
| REG-CC44 | Condition Code 44 / Part B rebilling | 2.1.3 |
| REG-IMM-MOON | Medicare beneficiary notices | 1.9.3, 2.3 |
| REG-ABN | ABN/liability notice rules | 1.5.2 |
| REG-MSP | Medicare Secondary Payer | 1.2.4, 6.4 |
| REG-NCCI | NCCI/MUE edit policy | 5.x, 6.2 |
| REG-60DAY | ACA 60-day overpayment rule | 12.4, 9.5 |
| REG-FCA | False Claims Act exposure | 12.x (governs everything billed) |
| REG-STARK-AKS | Stark/Anti-kickback (financial arrangements touching billing) | 12.4.A4 |
| REG-501R | IRS 501(r): FAP, AGB, ECA limits | 10.4, 10.6 |
| REG-FDCPA-REGF | Debt collection practices (agency conduct) | 10.5, 10.6 |
| REG-TCPA | Contact/dialer consent rules | 10.1, 10.2 outreach |
| REG-PROMPTPAY | State prompt-pay statutes | 9.3 |
| REG-ESCHEAT | State unclaimed property | 9.5 |
| REG-BANKRUPTCY | Automatic stay, proof of claim | 9.8.A2 |
| REG-WCJURIS | State workers' comp fee schedules/dispute processes | 6.4.3, 9.8 |
| REG-PCI | Payment card industry standards | 7.5, 7.6, 10.3 |
| REG-MA-PARITY | MA utilization criteria parity rules | 2.1, 8.4.3 |
| REG-QIO | QIO discharge appeal process | 2.3 |
| REG-AUDITPROG | RAC/MAC/TPE/CERT/UPIC program rules | 12.1 |

---

## The prevention feedback circuit (master relationship)

Every downstream defect signal routes to an upstream owner:

```
Denials (8.1 taxonomy) ─┬→ Access defects → 1.9.5 QA + 1.2–1.4 training
                        ├→ Status defects → 2.1 education
                        ├→ Charge defects → 3.4 edits + department feedback
                        ├→ Documentation defects → 4.5 provider education
                        ├→ Coding defects → 5.7 audits/education
                        ├→ Billing defects → 6.2.4 new pre-bill edits
                        ├→ Posting defects → 7.1.3 mapping fixes
                        └→ Payer behavior → 11.6 JOC → 11.1 negotiation
Audit findings (12.x) ──→ same routing + 12.6 corrective actions
Underpayments (9.4) ────→ 11.2 load fixes / 11.6 payer projects
Patient complaints (10.2) → 1.6 estimates, 10.1 statement clarity, 8.5
```
