# Build-Out #4 — "The Pilot Purgatory Autopsy"
## Stall signatures vs. scaler behaviors, with a self-scoring diagnostic

**Role in the block:** FIRST ALTERNATE. Three deployment modes:
- **Mode 1 (default):** 10-minute compressed insert inside the Rev Cycle 2030 keynote (the "why most of you won't get there" passage)
- **Mode 2:** full 30–35 min interactive segment replacing the war game (if the room skews operational, or the war game is judged too high-risk for the group)
- **Mode 3:** the diagnostic scorecard ships as a leave-behind only, with 2 minutes of stage framing

**Theme anchors:** Pilot purgatory (Theme 2), governance (Theme 6), operating-model redesign (Theme 3)

---

## 1. Design logic

This is the block's **"no vendor will ever tell you this"** content. Every attendee has stalled pilots; no vendor autopsy is credible because every vendor claims *their* tool escapes purgatory. The evidence base is unusually strong and unusually honest — including named health system executives on record about their own failures, and two failure modes that point in *opposite* directions (too fast AND too slow), which is exactly the nuance sales decks flatten.

**The core numbers (open with these):**
- 53% of organizations are stuck in pilots; 27% deploy at scale (HFMA Feb 2026 — *adversarially verified*)
- 67% believe AI can improve claims; 14% use it on denials (Experian 2025)
- 73% have automation somewhere; 58% call it fragmented across tools, departments, or suppliers (Black Book 2026)
- The board-deck grenade: MIT — >95% of $30–40B in enterprise GenAI investment shows no measurable ROI
- Only 39% of CFOs expect their AI investments to reduce costs (HFMA C-suite survey)

**Framing line:** *"Purgatory is not a technology state. It's an organizational state. And it has exactly five signatures — you'll recognize yours in about ninety seconds."*

---

## 2. The five stall signatures (the autopsy)

Each signature = named pattern + evidence + the tell (how you know it's you).

### Signature 1 — TOOL-FIRST ("a solution shopping for a problem")
- **Pattern:** the pilot began with an exciting vendor, not a defined problem and outcome metric.
- **Evidence:** Reid Health CIO Muhammad Siddiqui, on record: the biggest early-AI lesson was moving on tools "that sounded interesting" before defining the problem — *"we learned that the hard way."* Early-boom systems accumulated "a surplus of redundant — or ineffective — solutions."
- **The tell:** you cannot state, in one sentence, the metric the pilot was supposed to move — or two of your tools do the same thing.

### Signature 2 — ROI-ON-HOPE (no funding discipline)
- **Pattern:** the business case was directional enthusiasm; nobody defined what "working" meant, so nothing could graduate OR be killed.
- **Evidence:** Baptist Health CIO Aaron Miri's funding rule — AI can't be funded on "hope"; every initiative needs defined ROI: measurable time returned or direct financial impact. Cost/ROI ambiguity is the #1 stated barrier for large systems (52.5%, AKASA/HFMA).
- **The tell:** pilots at your organization end by expiring, not by decision. No pilot has ever been formally killed.

### Signature 3 — FRAGMENT FARM (no orchestration layer)
- **Pattern:** point solutions bought unit-by-unit; automation exists everywhere and connects nowhere; each new tool adds integration debt.
- **Evidence:** 58% report automation fragmented across tools/departments/suppliers (Black Book); integration with fragmented legacy EHR/billing environments is a top stall point (AKASA/HFMA). HFMA's scaler pattern is the opposite: a unified orchestration layer — an "AI fabric" — across EHR, point solutions, and internal models, with explainable, auditable decisions.
- **The tell:** you can't produce a single inventory of your AI/automation footprint — or the count surprises you.

### Signature 4 — TRUST CEILING (the hidden factory)
- **Pattern:** the pilot "works" but everyone double-checks it, so no labor ever comes out; automation that requires constant review isn't automation.
- **Evidence:** 41% of providers find it difficult to fully trust AI results (Experian). Failure mechanics: black-box models trained on claims-only data can't see clinical context, over-flag records, and replicate the historical errors in their training data — creating rework that eats the ROI.
- **The tell:** the pilot's "success" report counts outputs produced, not hours of human review eliminated. Staffing in the piloted area hasn't changed.

### Signature 5 — GOVERNANCE VACUUM or its evil twin, CAUTION LOCK
- **Pattern A (vacuum):** ungoverned pilots sprawl; nobody can explain model behavior when a payer, auditor, or board asks. **Pattern B (lock):** governance became a veto machine and nothing ships.
- **Evidence:** Mass General Brigham CTO Nallan Sriraman — stopped ungoverned pilots, installed an enterprise governance framework. Baptist's Miri — the *opposite* regret: "we overindexed on caution instead of accelerating where we had clear use cases." 63% now say auditability/explainability are mandatory (Black Book).
- **The tell (A):** no standing body with clinical informatics + data science + frontline users reviews AI deployments. **The tell (B):** your governance committee has never approved anything in under 90 days.
- **Stage note:** presenting BOTH regrets — too fast and too slow — is the segment's credibility peak. *"The vendors tell you the risk is moving too slow. The lawyers tell you it's moving too fast. The record says both are real, which is why the differentiator is neither speed — it's discipline."*

## 3. The five scaler behaviors (the counter-list)

1. **Problem-first, metric-gated** — every initiative starts from an operational need and a kill/scale metric defined *before* the pilot (Reid's lesson inverted; Miri's rule).
2. **A 3–4 priority portfolio, not a use-case zoo** — concentrate on a small number of enterprise priorities (BCG); prioritize with opportunity scoring (impact vs. implementation friction).
3. **Orchestration architecture** — build toward one AI fabric with auditable decisions, not another point solution (HFMA); make explainability a contract requirement (the 63%).
4. **Governance that ships** — standing committee (clinical informatics + data science + frontline users) with authority to kill AND a service-level clock, so it accelerates rather than vetoes (MGB × Baptist synthesis).
5. **Fund the 70%** — BCG's 10-20-70: 10% algorithms, 20% technology, 70% people/process. Scalers budget change management, workflow redesign, and training as first-class line items, not contingency. *(Bridge line to keynote thesis: "and the biggest 70% investment of all is redesigning the process — asking why the step exists at all.")*

---

## 4. The self-scoring diagnostic (the Monday artifact)

One page, 10 statements, score each 1–5 (1 = not true of us, 5 = very true). **Deliberately scored so LOW totals = purgatory** — executives remember a bad score.

| # | Statement | Signature tested |
|---|---|---|
| 1 | Every active AI initiative has a one-sentence problem statement and a number it must move | 1, 2 |
| 2 | We have formally killed at least one AI pilot in the past 18 months | 2 |
| 3 | I could produce a complete inventory of our rev-cycle AI/automation footprint within one week | 3 |
| 4 | Our AI initiatives ladder up to 3–4 named enterprise priorities (not a use-case list) | 1, scaler 2 |
| 5 | In at least one deployed use case, humans review exceptions only — not every output | 4 |
| 6 | Our pilot success metrics count human hours eliminated, not just outputs produced | 4 |
| 7 | A standing governance body with clinical, data-science, AND frontline membership reviews every AI deployment | 5A |
| 8 | That body has approved something in under 90 days | 5B |
| 9 | We could explain any AI-influenced decision to a payer auditor or board member within 48 hours | 5A, 6 |
| 10 | Change management, training, and workflow redesign are funded line items in every AI business case | scaler 5 |

**Scoring bands:**
- **10–24: Deep purgatory.** Stop starting pilots. Run the inventory (Q3), kill three things, pick your 3–4 priorities.
- **25–39: The messy middle** (most of the room — say so). Pick your two lowest-scoring statements; they are your next two quarters.
- **40–50: Scaler profile.** Your risk flips to Caution Lock and complacency — re-score quarterly, and go find what Baptist found: the clear use case you're under-accelerating.

## 5. Run of show

**Mode 1 — 10-min keynote insert:** core numbers (2 min) → five signatures at ~75 sec each, evidence quotes on-slide (6 min) → scaler list as a single build slide + "the scorecard is in your packet; score yourself on the flight home" (2 min). No table work.

**Mode 2 — full 30–35 min segment:** open with reserve poll R1 ("what killed your last stalled pilot?" — options map to the five signatures; benchmark: 52.5% cost/ROI, 41% trust) (3 min) → signatures with full storytelling (10 min) → silent individual scoring (4 min) → table discussion: "share your lowest-scoring statement and one thing that would move it" (8 min) → scaler behaviors + report-back of two or three table insights (7 min) → close: *"Purgatory is a choice made by default. Scale is a choice made on purpose. You now know which five defaults to break."*

**Mode 3 — leave-behind only:** scorecard + signatures/scalers on one sheet in the packet; 2-minute stage pointer during the keynote.

## 6. Materials & contingencies

- **Materials:** signature slides with verbatim quotes (Siddiqui, Sriraman, Miri); scorecard one-pager per seat (works standalone — it will be photocopied inside their organizations, which is the goal); poll R1 loaded if Mode 2.
- **"Our stall reason isn't listed" pushback:** invite it — *"tell me the sixth signature"* — and map it live; it almost always decomposes into 2 + 4 (no metric + no trust).
- **Room includes organizations doing this well:** recruit them — ask a high-scorer to say what made Q2 (killing pilots) possible; peer testimony beats any slide.
- **Huron positioning discipline:** the AI Acceleration Council reference belongs here if anywhere — one slide, framed as "we ran this diagnostic on ourselves; here were OUR two lowest scores," which is self-deprecating evidence, not a pitch. Never present Huron client stall stories with identifying detail.
