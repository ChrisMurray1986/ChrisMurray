# AD-01 Operating Model & Organization

How the revenue cycle is structured, governed, and connected to clinical operations and IT.
Operating-model failures are the most expensive in this ontology because they are *upstream of
everything*: they turn process fixes into turf wars and automation programs into orphans.

---

## Failure modes

### OFM-OM-01 — Fragmented accountability
No single executive owns the revenue cycle end-to-end; access reports to operations, HIM to
compliance, billing to finance, the medical group bills separately.
**Signals:** denial root causes bounce between departments for months; "that's a front-end
problem" heard in the back end and vice versa; no one can state total cost-to-collect.
**Damages:** the entire prevention feedback circuit (base ontology 8.5); KPI-IDR, KPI-NCR.
**Degrades (AI):** `routing_authority` — prevention insights have no obligated owner; Play 3
remediations die in matrix limbo.

### OFM-OM-02 — Site-based policy variation
Each facility/practice runs its own collection policy, discount practice, write-off habits, and
workqueue conventions — usually a merger integration that never finished.
**Signals:** "it depends on the site" answers; three different financial-assistance forms; the
same CARC worked three different ways.
**Damages:** 1.8/10.x consistency; patient-experience equity; audit exposure.
**Degrades:** workflow dimension W0/W1; `collection_policy_unified`, `plan_matrix_unified` —
conversational/POS automation DEFERs indefinitely.

### OFM-OM-03 — The front/back wall
Patient access and the business office operate as separate worlds with no feedback contract;
registration defects are discovered — and paid for — 45 days later as denials.
**Signals:** back-end staff maintain private "fix lists" of front-end errors; access QA measures
courtesy, not denial-linked accuracy; no shared metrics.
**Damages:** 1.9.5↔8.5 feedback loop; KPI-REGQA, eligibility/auth denial rates.
**Degrades:** `denial_labels` attribution quality (defects never attributed to origin).

### OFM-OM-04 — Clinical–revenue cycle disconnect
No physician advisor structure with real authority; CDI and UM report into silos; provider
documentation and status decisions have no revenue-cycle voice.
**Signals:** unanswered queries with no escalation; peer-to-peers declined for clinic schedule;
status changes litigated after discharge.
**Damages:** RC-02, RC-04; KPI-CMI, concurrent denial overturn, KPI-QUERYRATE.
**Degrades:** `provider_adoption`, `um_worksheets` quality; clinical-appeals efficacy ceiling.

### OFM-OM-05 — Governance theater
Committees exist, meet, and review dashboards — but hold no decision rights, no budget, and no
follow-through mechanism.
**Signals:** the same agenda item three months running; decisions "taken offline" and lost;
minutes without owners or dates.
**Damages:** every cross-functional fix; write-off governance (8.6).
**Degrades:** `gov_body` becomes a paper facet; the investment loop's council (Play 2) inherits
a theater culture.

### OFM-OM-06 — Span and layer distortion
Supervisors with 25+ direct reports doing pure firefighting, or three management layers each
"reviewing" the same work; no one coaches.
**Signals:** supervisors can't name their team's top error patterns; QA exists but feedback
loops don't close; promotion = escape from the work.
**Damages:** quality programs across all domains; KPI variance between teams.
**Degrades:** `hitl_capacity` credibility (review capacity exists on paper, not in practice).

### OFM-OM-07 — Shared service without service
Functions were centralized for scale but never adopted service commitments; sites experience a
black hole and quietly rebuild shadow staff.
**Signals:** sites keep "billing liaisons" off-book; central turnaround times unmeasured;
escalation = knowing someone personally.
**Damages:** the economics of centralization; duplicate effort; KPI-CTC.
**Degrades:** trust required for `ranked_list_adoption` and central automation ownership.

### OFM-OM-08 — The IT–RCM divide
Revenue cycle competes in a general IT queue for every workqueue change; simple edits take a
quarter; nobody in IT owns revenue-cycle outcomes.
**Signals:** "it's with IT" as a status; 200-item enhancement backlog with no ranking by
dollars; analysts hoarding access as power.
**Damages:** every configuration-dependent fix; edit governance (6.2.4).
**Degrades:** the entire integration dimension in practice — `writeback`, `queue_api`, `fabric`
scores decay because build capacity is theoretical.

## Best practices

### BP-OM-01 — Single accountable executive, end-to-end
One leader owns cost-to-collect *and* net realization jointly, front door to zero balance,
hospital and professional. **Maturity markers:** one P&L view exists; denial dollars carry a
single owner map; access and billing share incentive metrics. **Prevents:** OFM-OM-01, -03.
**Enables:** `routing_authority`; makes the AI council (Play 2) decision-capable.

### BP-OM-02 — Enterprise standards, local execution
One policy library (collections, discounts, write-offs, FA) with documented, regulation-driven
local exceptions only. **Markers:** policy variance inventory exists and shrinks quarterly;
new-site integration playbook standardizes in 90 days. **Prevents:** OFM-OM-02. **Enables:**
W2+ across the board; unblocks conversational/POS automation.

### BP-OM-03 — Feedback contracts across the wall
Formal defect-attribution flow: every denial taxonomy category has an owning function; origin
functions receive weekly defect feeds with named accounts; access QA is denial-linked.
**Markers:** access leaders can quote their denial-linked error rate; defect trend reviewed in
joint huddle. **Prevents:** OFM-OM-03. **Enables:** `denial_labels` (this practice *is* CAP-02's
organizational half).

### BP-OM-04 — Clinical revenue integrity structure
Physician advisors with medical-staff authority; CDI/UM/coding aligned under one clinical
revenue leader or a tight compact; documentation performance visible to service chiefs.
**Markers:** query response SLA enforced by chiefs; P2P coverage roster exists; advisor time
protected. **Prevents:** OFM-OM-04. **Enables:** clinical NLP/appeals efficacy; `provider_adoption`.

### BP-OM-05 — Decision-rights charter
A one-page RACI for the decisions that matter: write-off authority levels, policy changes,
vendor selection/renewal, edit changes, automation autonomy promotions. **Markers:** charter
exists, is cited in meetings, and decision logs reference it. **Prevents:** OFM-OM-05.
**Enables:** GOV-01 governance body lands on existing rails.

### BP-OM-06 — Spans, layers, and working supervision
Span standards by work type (transactional 12–15, judgment 8–10); supervisors spend ≥40% on
QA/coaching with calendars audited to it. **Markers:** coaching logs exist; team-level variance
narrows. **Prevents:** OFM-OM-06. **Enables:** real `hitl_capacity`; HITL-SAMPLE audit quality.

### BP-OM-07 — Service-level operating agreements
Shared services publish turnaround/quality SLAs to sites, measured and reviewed jointly; a
named service manager per site relationship. **Markers:** SLA dashboard public; shadow staff
absorbed or chartered. **Prevents:** OFM-OM-07.

### BP-OM-08 — Dedicated revenue-cycle build capacity
A ring-fenced EHR build team for revenue cycle with an intake process ranked by dollars, joint
IT/RCM governance, and a 2-week SLA for configuration-class changes. **Markers:** enhancement
backlog carries $ estimates and burns down; workqueue changes ship in days. **Prevents:**
OFM-OM-08. **Enables:** integration-dimension scores that survive an audit; the remediation
playbook's 2–6 week timelines become real.

## Maturity anchors (AD-01)

| Level | Anchor |
|---|---|
| 0 | No single owner; sites autonomous; governance absent |
| 1 | Owner named but matrix-blocked; standards drafted, unenforced |
| 2 | End-to-end owner with budget; standards enforced at most sites; feedback contracts piloted |
| 3 | Decision-rights charter operating; clinical structure seated; IT capacity dedicated |
| 4 | Operating model reviewed annually against outcomes; new-site integration <90 days; governance decisions traceable to results |
