# Function Assessment — RC-08 Denials & Appeals · RC-09 AR Management

Roles: ROLE-DENIAL, ROLE-APPEALRN, ROLE-APPEALW, ROLE-PHYSADV, ROLE-ARFU, ROLE-UNDERPAY,
ROLE-CREDIT.

## RC-08 Denials Management & Appeals

### 8.1 Denial Identification & Classification — ROLE-DENIAL

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-8.1-01 | Denial universe = 835s only; letter/portal denials uncaptured (8.1.A1) | Appeals discover denials the reports never showed; paper-payer denials absent | PBP-8.1-01 All-channel denial intake (835 + correspondence + portal); hardened-by UC-08-01 |
| PFM-8.1-02 | Classification stops at CARC; root-cause owner never attributed (8.1.A2–A3) — the taxonomy exists, unused | Denial reports by code, never by owning function; prevention meetings argue anecdotes | PBP-8.1-02 Owner-attributed taxonomy applied at intake (BP-PI-04's operational form); feeds `denial_labels` |
| PFM-8.1-03 | Appeal deadlines computed per-analyst from memory (8.1.A4) → FM-APPEALMISS | Deadline-missed write-offs exist at all | PBP-8.1-03 Deadline stamped at intake from the filing matrix; countdown visible in queues |

### 8.2 Triage & Routing — ROLE-DENIAL

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-8.2-01 | Worked oldest-first or smallest-first (8.2.A1) — recoverable dollars age out | High-value denials untouched at day 30; cherry-picking measurable | PBP-8.2-01 Value × overturn-likelihood × deadline routing; hardened-by UC-08-02 |
| PFM-8.2-02 | Systemic denial clusters worked one-by-one (8.2.A3, D1) | Same payer/reason denied 400 times, appealed 400 times separately | PBP-8.2-02 Cluster detection with batch strategy (project appeal or payer escalation, 11.6) |

### 8.3 Non-Appeal Resolution — ROLE-DENIAL

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-8.3-01 | Rebill reflex: resubmit-as-fix without diagnosis (8.3.A1, D1) → FM-REBILLLOOP | Accounts with 3+ identical submissions; touch history shows loops | PBP-8.3-01 Loop-breaker rule: second identical denial forces root-cause path; hardened-by UC-08-04 |
| PFM-8.3-02 | Write-off as path of least resistance (8.3.A4); authority matrix ignored under volume | Small-balance denials auto-adjusted; write-off codes concentrated on a few users | PBP-8.3-02 Write-off governance enforced in system (8.6); reason-coded and sampled |

### 8.4 Appeals — ROLE-APPEALW, ROLE-APPEALRN, ROLE-PHYSADV

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-8.4-01 | Template letters regardless of denial substance (8.4.2.A1) | Overturn rate low and flat; payers pattern-match and deny | PBP-8.4-01 Argument selection per denial class (procedural first, 8.4.3.D1); evidence-cited letters; hardened-by UC-08-03 |
| PFM-8.4-02 | Clinical appeals written without criteria mapping or chart pinpoints (8.4.3.A1) | Letters assert "medically necessary" without evidence citations | PBP-8.4-02 Criteria-element structure with record citations (file 12 §2 as the manual standard) |
| PFM-8.4-03 | Levels burned reflexively: level-1 loss → level-2 same letter (8.4.5.A1, D1) | Multi-level appeals with identical content; external review never reached strategically | PBP-8.4-03 Level strategy per case (strengthen, escalate, or stop); upheld-twice → prevention analysis |
| PFM-8.4-04 | Won appeals unpaid — overturn letter filed, payment never verified (8.4.6.A1–A2) | Wins celebrated, cash unmatched | PBP-8.4-04 Overturn-to-payment reconciliation; hardened-by UC-08-06 |

### 8.5 Denial Prevention — ROLE-DENIAL + owning functions

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-8.5-01 | Prevention meeting = report review; actions unowned, untracked (8.5.A2–A4) | Same top-5 denial categories for 8 quarters | PBP-8.5-01 Routed prevention actions with owners/dates and denial-rate verification per action (needs BP-OM-01/BP-PI-01); hardened-by UC-08-05 |

### 8.6 Write-Off Governance — ROLE-CFO

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-8.6-01 | Authority matrix on paper; system permits anyone anything (8.6.A1–A2) | Write-offs above authority levels found on sampling | PBP-8.6-01 Matrix enforced in system security; monthly pattern review by reason/user (8.6.A3) |

## RC-09 AR Management & Follow-Up

### 9.1 Work Prioritization — ROLE-ARFU

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-9.1-01 | Aging-bucket worklists; cherry-picking endemic (9.1.A2, D1) | 90+ bucket grows while 30-day easy accounts get triple-touched | PBP-9.1-01 Expected-value routing with cherry-pick guardrails; hardened-by UC-09-01 |
| PFM-9.1-02 | Touch ≠ progress: status-check notes count as work (9.1.A3) | "Claim in process" notes recurring monthly per account | PBP-9.1-02 Resolution-based standards (BP-PI-06); next-action-with-date required per touch |

### 9.2 Claim Status Determination — ROLE-ARFU

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-9.2-01 | Reps call payers for statuses available on 276/portal (9.2.A1) | Hold-time hours; status calls >50% of touches | PBP-9.2-01 Status automation with humans on exceptions only; hardened-by UC-09-02 |

### 9.3 No-Response Follow-Up — ROLE-ARFU

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-9.3-01 | No-response claims re-billed blind (9.3.A2, D1) — duplicate denials, TFL burn | Resubmission without receipt-verification; duplicates in denial mix | PBP-9.3-01 Trace-then-act protocol (ack? received? adjudicating?) before any resubmission |

### 9.4 Underpayment Recovery — ROLE-UNDERPAY

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-9.4-01 | Variances chased claim-by-claim; systematic patterns never aggregated (9.4.A2–A3) | Same fee-schedule error recovered 900 times individually | PBP-9.4-01 Pattern clustering with batch demands and JOC escalation; hardened-by UC-09-03 |
| PFM-9.4-02 | Load-vs-payer confusion: engine errors "recovered" from payers, payer errors "fixed" in the engine (9.4.D1) | Demand letters withdrawn; contract engine trust erodes | PBP-9.4-02 Variance-cause triage (load error → 11.2; payer error → demand) before action |

### 9.5 Credit Balances & Refunds — ROLE-CREDIT

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-9.5-01 | Credits worked oldest-first at month-end only (9.5.A1) → FM-CREDITAGE, FM-60DAY | Credit AR aged >90 days; government credits untracked for the clock | PBP-9.5-01 Classification-first workflow (true credit vs mispost) with 60-day clocking; hardened-by UC-09-04 |
| PFM-9.5-02 | Patient refunds slow-walked while payer demands jump the queue (9.5.A3) | Patient refund cycle >30 days; complaints reference credits | PBP-9.5-02 Patient-refund SLA equal to payer-demand SLA |

### 9.6 Small Balance & Administrative — ROLE-ARFU

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-9.6-01 | Small-balance thresholds set once, never revisited; leakage compounding (9.6.A1) | Threshold write-offs material in aggregate; no periodic review | PBP-9.6-01 Threshold economics reviewed annually with volume × recovery-cost math |

### 9.7 Aged AR & Bad Debt Transfer — ROLE-ARFU, ROLE-CFO

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-9.7-01 | Placement gates unchecked: accounts to bad debt with statements incomplete or FA unscreened (9.7.A3) → FM-FA-MISS, 501(r) exposure | Agency kicks back gate failures; charity found post-placement | PBP-9.7-01 Gate verification automated pre-placement; hardened-by UC-09-06 |

### 9.8 Special Accounts — ROLE-ARFU

| ID | Failure mode → bindings | Field signals | Paired practice |
|---|---|---|---|
| PFM-9.8-01 | Bankruptcy/deceased notices actioned late (9.8.A2–A3) — stay violations, estate windows missed | Collection letters post-petition; probate deadlines lapsed | PBP-9.8-01 Registry-feed monitoring with same-day stops; hardened-by UC-09-05 |
| PFM-9.8-02 | Liens unperfected or unmonitored (9.8.A1) | Liability settlements paid out with hospital unpaid | PBP-9.8-02 Lien calendar with perfection checklists per jurisdiction |
