# Adjudication Doctrine D2: ESCALATION-VIABLE

## Core principle
Escalation contests resolve on **capability differentials and unit economics**, not on symmetry. Two sides escalating simultaneously is not a wash; it is a measurable contest the stronger platform wins on margin.

## 1. Resolving simultaneous escalation

When both sides escalate in the same turn, adjudicate each contested metric independently via a **Capability Differential (CD)** score per side, per domain:

CD = Model/data quality (0-4) + Data access advantage (0-3) + Deployment scale on affected volume (0-2) + Regulatory/contractual position (0-1)

- **CD gap ≥ 3:** stronger side captures 60-80% of the contested metric swing (denial yield, appeal overturn rate, clean-claim leakage). The swing is **durable**: it persists across turns until the loser closes the capability gap, not merely until it counter-escalates.
- **CD gap 1-2:** stronger side captures 25-40% of the swing; loser's counter-move degrades but does not neutralize it.
- **CD gap 0:** stalemate on metrics — but NOT cost-neutral. Each side pays its own run-rate; whoever's P&L supports the run-rate longer holds position (see §2).

**Payer ASO economics rule:** payment-integrity recoveries on self-funded volume are booked as **fee revenue to the payer's services arm** (contingency 10-15% of recoveries). Escalating denial/audit intensity on ASO book is therefore P&L-positive for the payer indefinitely, provided plan sponsors don't churn (see failure conditions). Adjudicators must NOT charge payers a "conflict cost" on ASO escalation; charge only fully-insured MLR exposure and operating cost of the tooling.

**Provider symmetric rule:** provider appeal/documentation escalation that raises overturn rates or clean-claim yield is revenue recovery net of tooling cost — also indefinitely sustainable if net-positive per claim.

## 2. What makes escalation fail

Escalation fails ONLY through these channels — never through an automatic "mutual destruction" tax:

1. **Own-P&L break:** cumulative tooling + admin cost exceeds recovered/defended revenue for that side over a rolling 4-quarter window. Adjudicator tracks a per-side conflict ledger; exhaustion is declared when the ledger goes negative and the side has no capability investment maturing within 2 turns.
2. **Customer defection:** payer ASO escalation fails if adjudicator finds plan-sponsor abrasion (member complaints, provider network friction) crosses a churn threshold — roll only when escalation touches member-visible surfaces (prior auth denials on care, not post-pay recoveries).
3. **Capability leapfrog:** loser acquires/builds superior models or data (e.g., provider coalition pools payer-behavior data); CD recomputes and gains reverse prospectively, not retroactively.
4. **Litigation/regulatory shock — slow and probabilistic:** each turn of aggressive escalation adds 5-10% to a cumulative shock probability; if triggered, effects land 3-7 game-years later (injunction, consent decree, ERISA fiduciary ruling). Expected-value cost is real but small enough that a strong-CD escalator rationally continues.

## 3. Costing cooperative moves

Cooperative moves are no longer free wins. Charge:

- **Formation cost:** multilateral instruments (data-sharing compacts, gold-carding standards, joint clearinghouse rules) cost 1-2 turns of lead time plus explicit legal/antitrust overhead (real dollars off both P&Ls) before any benefit accrues.
- **Governance drag:** ongoing 10-20% haircut on modeled cooperative surplus.
- **Defection option value:** each turn, adjudicator tests whether unilateral defection is individually rational (defector's one-turn gain > discounted compact benefit). If yes, the compact holds only if enforcement teeth exist in the instrument; otherwise it decays. Cooperation is an equilibrium to be earned, not a default reward.
- Cooperative surplus, when it survives, may still be large — D2 removes the thumb on the scale, not the possibility.

## 4. Adjudication examples

**Example A — Simultaneous AI arms race, ASO book.** Payer deploys frontier-model itemized-bill review (CD 8); provider deploys mid-tier appeal-letter generator (CD 5). Gap 3: payer captures 70% of contested swing — denial yield +180bps on ASO volume, booked as services fee revenue. Provider overturn rate rises only 4pts. Payer ledger positive; escalation is a winning strategy this turn and durable next turn.

**Example B — Escalation failure via P&L break.** Regional provider system counter-escalates with a bespoke denial-prediction stack costing $40M/yr; recovered revenue $28M/yr; no capability investment maturing. After 4 quarters, ledger negative → exhaustion declared; provider must sue (slow channel), join a coalition (pay formation costs), or settle on payer terms.

**Example C — Compact defection.** Three payers and two systems form a prior-auth gold-carding compact: 1.5-turn formation, $12M lawyering/antitrust cost each, 15% governance haircut. Turn 3, one payer's new model makes unilateral audit escalation worth more than its compact share; instrument has no clawback teeth. Defection adjudicated rational; compact decays; defector gains durable CD-based advantage. Remaining parties eat sunk formation costs.