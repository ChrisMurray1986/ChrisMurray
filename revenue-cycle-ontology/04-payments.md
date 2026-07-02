# RC-07 Remittance Processing & Payment Posting

Receives payer and patient payments, applies them to the correct accounts and lines, records
adjustments accurately, reconciles to bank, and flags every variance for downstream action.
Posting accuracy is the data foundation for denials, underpayments, and AR truth.

Roles: Payment Poster, Cash Applications Analyst, Treasury/Reconciliation Analyst, PFS Supervisor.
Systems: 835 processing engine, lockbox, bank feeds, patient accounting, payment portals,
merchant processor, contract/expected-pay engine.

---

## 7.1 Electronic Remittance (835) Processing

### 7.1.1 835 receipt, validation & loading
- **A1.** Retrieve 835 files from clearinghouse/payers on schedule; verify file integrity
- **A2.** Balance file header totals to claim-level detail; log control numbers
- **A3.** Match 835 to corresponding EFT/check (TRN trace number) {links: 7.3.1}
- **D1.** 835 fails validation/balancing?
  - ├─ Yes → quarantine file; request retransmission; do not partially post
  - └─ No → load for posting

### 7.1.2 Auto-posting & exception queue
- **A1.** Auto-match remit claims to open accounts (claim number, patient control number, member, dates)
- **A2.** Auto-post payments, contractual adjustments, patient responsibility per mapped rules
- **A3.** Route non-matching/ambiguous remit lines to manual exception queue
- **A4.** Post zero-pay remits (full denials) so denial workflows trigger {triggers: 8.1}
- **D1.** Remit line matches an open account?
  - ├─ Exact match → auto-post
  - ├─ Partial match (payment plan claim, split claim) → analyst applies with line mapping
  - └─ No match → unidentified cash process (7.3.3)
- **D2.** Remit amount differs from expected reimbursement?
  - ├─ Within tolerance → post; close if resolved
  - └─ Outside tolerance → post + flag variance {triggers: 7.4.2}

### 7.1.3 CARC/RARC mapping & action coding
- **A1.** Maintain mapping of CARC/RARC/group codes → internal transaction codes and next actions
  (adjust, deny-route, patient-liability, review)
- **A2.** Review payer-new codes and remap; audit mapping quality (mis-mapped denial-as-adjustment
  silently writes off recoverable revenue — high-severity failure mode)
- **D1.** New/unmapped CARC-RARC combination encountered?
  - ├─ Yes → hold lines; classify with denial team; add mapping
  - └─ No → standard flow

## 7.2 Manual & Paper Remittance Posting
- **A1.** Process lockbox correspondence/EOB images; index to accounts
- **A2.** Key payments/adjustments line-by-line from paper EOBs with denial codes captured
- **A3.** Batch-balance manual posting (keyed totals = check totals) before commit
- **A4.** Convert repeat paper payers to ERA/EFT enrollment {links: 14.3}

## 7.3 Payment Reconciliation & Treasury

### 7.3.1 EFT-to-835 matching
- **A1.** Match bank EFT credits to 835 files via TRN; work unmatched-EFT and unmatched-835 lists
- **A2.** Chase missing remits for received funds (payer/clearinghouse retrieval)
- **D1.** Money received without remittance detail after N days?
  - ├─ Obtain remit → post normally
  - └─ Cannot obtain → post from payer portal detail/EOB copy; escalate payer EDI issue

### 7.3.2 Bank deposit / lockbox reconciliation
- **A1.** Reconcile daily: bank deposits = posted cash + unposted-in-transit, by source (EFT, lockbox,
  POS, portal, agency remits)
- **A2.** Investigate and clear reconciling items within close calendar
- **A3.** Certify monthly cash reconciliation with GL {links: 13.3}

### 7.3.3 Unapplied & unidentified cash resolution
- **A1.** Log unidentified receipts to suspense with source detail
- **A2.** Research (payer contact, remit trace, patient inquiry) and apply to correct account
- **A3.** Age suspense with escalation; resolve to zero on cadence
- **D1.** Unidentifiable after exhaustive research?
  - ├─ Payer money → return to payer with documentation
  - └─ Patient money → refund attempt → unclaimed property/escheatment path (9.5)

## 7.4 Adjustment Posting & Variance Detection

### 7.4.1 Contractual adjustment posting
- **A1.** Post contractual allowances per remit and contract terms with correct transaction codes
- **A2.** Restrict non-standard adjustment codes to authorized users (write-off governance 8.6)
- **A3.** Audit adjustment usage for miscoding (denial hidden as contractual)

### 7.4.2 Expected-vs-actual variance flagging
- **A1.** Compute expected reimbursement per contract engine at claim level
- **A2.** Compare posted payment+patient-liability to expected; flag over/under outside tolerance
- **D1.** Variance direction?
  - ├─ Underpaid → underpayment recovery queue (9.4)
  - ├─ Overpaid → overpayment review (12.4) — do not silently absorb
  - └─ Expected-pay model wrong → contract-load correction (11.2) and recalc

### 7.4.3 Take-back / recoupment / reversal processing
- **A1.** Post payer reversals/negative remits; link recoupment to original claim and reason
- **A2.** Validate recoupment legitimacy (was there notice? is it timely under state/contract rules?)
- **A3.** Rebalance account after take-back; re-open for appropriate follow-up (appeal, rebill,
  patient transfer)
- **D1.** Recoupment disputed?
  - ├─ Yes → dispute/appeal recoupment per payer process (8.4); track offset against future remits
  - └─ No → accept; adjust account; refund interaction check (9.5)

## 7.5 Patient Payment Processing
- **A1.** Ingest payments from portal, IVR, mail, POS, kiosks, payment plans, financing partners
- **A2.** Apply per allocation rules (oldest visit, patient-directed, plan installment schedule)
- **A3.** Process card declines/dunning for stored-card plan payments {links: 10.3}
- **A4.** Handle disputes/chargebacks with evidence packets; track chargeback outcomes
- **A5.** Process patient refund requests intake {links: 9.5}

## 7.6 Cash Application Controls & Balancing
- **A1.** Enforce daily batch balancing per poster; supervisor review of exceptions
- **A2.** Maintain segregation of duties (posting vs refund approval vs reconciliation)
- **A3.** Audit posting accuracy samples; monitor auto-post override patterns
- **A4.** Maintain PCI-compliant handling of card data across all channels

**Failure modes:** misposted cash, denial-as-adjustment miscoding, unposted 835s, suspense
aging, recoupment posted without validation, plan payments unapplied.
**Metrics:** auto-post rate, posting lag (deposit-to-post days), suspense balance & age,
posting accuracy %, unmatched EFT count, cost per posted transaction.

## Relationships
- 7.1.2 zero-pay/denial lines `trigger` 8.1 (denial intake)
- 7.4.2 `triggers` 9.4 (underpayments) and 12.4 (overpayments)
- 7.3 `feeds` 13.3 (month-end close); posting accuracy `gates` all AR analytics validity
- 7.1.3 mapping quality `gates` denial program completeness (8.x)
