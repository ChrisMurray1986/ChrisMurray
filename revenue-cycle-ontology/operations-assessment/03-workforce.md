# AD-03 Workforce

Staffing, skills, careers, incentives, and engagement across the revenue cycle — including the
workforce transition that AI adoption forces. The AI stack's largest run cost is human review;
this domain decides whether that capacity exists, stays, and improves.

---

## Failure modes

### OFM-WF-01 — The vacancy spiral
Turnover creates vacancies → overtime and backlog for the remainers → burnout → more turnover.
Backlogs become permanent; hiring runs perpetually behind attrition.
**Signals:** >25% annual turnover in transactional roles; standing overtime; time-to-fill
>60 days; recruiting treated as an HR problem, not an operating one.
**Damages:** every queue-based process; KPI-DAR, denial timeliness, morale.
**Degrades:** `hitl_capacity`, `escalation_staffed` — A2/A3 launches stall because review
queues rot; automation gets blamed for the chaos it inherited.

### OFM-WF-02 — Training by shadowing
Onboarding is two weeks sitting with whoever is least busy; errors propagate as folklore;
competence is never verified before production.
**Signals:** no curriculum or certification gate; error patterns cluster by trainer lineage;
90-day new-hire error rates unmeasured.
**Damages:** quality baselines; time-to-productivity; OFM-PI-02 reinforcement.
**Degrades:** the human baseline the AI is measured against is itself unstable — efficacy
comparisons (file 12 tier designs) lose their control group.

### OFM-WF-03 — No career architecture
Roles cap out; mastery has no ladder; the best performers leave or promote away from the work
they were best at.
**Signals:** flat job families; supervisor as the only advancement; tenure bimodal (green or
15 years, nothing between).
**Damages:** knowledge retention; QA and coaching bench.
**Degrades:** the AI-era roles (exception specialist, automation QA, labeler, loop operator)
have no rungs to attach to — the stack's staffing plan has nowhere to promote from.

### OFM-WF-04 — Productivity without quality (or neither)
Standards exist only for volume, or not at all; quality consequences are folklore.
**Signals:** quotas without QA weighting; no balanced scorecard; "productivity report" is the
only report staff see.
**Damages:** OFM-PI-06's twin at the individual level; rework rates.
**Degrades:** HITL review quality — reviewers optimized for throughput rubber-stamp
(FM-AI-03's staffing root cause).

### OFM-WF-05 — Knowledge concentration
Single points of failure: the one person who knows payer X's appeals, the analyst who owns the
month-end query. Vacations are risk events.
**Signals:** named individuals in process descriptions; PTO coverage panic; undocumented
"Maria's spreadsheet" dependencies.
**Damages:** continuity; every process that person touches.
**Degrades:** SME availability for design/validation (O1 gate); golden-set curation and
label quality depend on exactly these people.

### OFM-WF-06 — Misaligned incentives
Bonuses on cash collected drive write-off abuse and cherry-picking; team metrics punish the
functions that prevent rather than collect.
**Signals:** write-off spikes at bonus period ends; prevention work "doesn't count"; access
incented on speed while billing eats the denials.
**Damages:** 8.6 write-off governance; front/back alignment; audit exposure.
**Degrades:** `writeoff_matrix` enforcement in practice; corrupts the outcome labels the value
ledger and the models both consume.

### OFM-WF-07 — Uninstrumented remote work
Remote/hybrid adopted without operating discipline: no work visibility, no virtual coaching
rhythm, engagement decays silently.
**Signals:** supervisors "can't see" work; QA sampling collapsed post-remote; new hires remote
from day one with shadow-training over screen share.
**Damages:** all coaching and QA practices; team cohesion; turnover.
**Degrades:** `touch_logging` completeness ironically improves (systems capture more) while
judgment quality drifts unobserved.

### OFM-WF-08 — Unmanaged AI anxiety
Automation announced (or rumored) as headcount reduction; the most experienced staff — exactly
the reviewers, labelers, and exception handlers the AI stack needs — leave first or quietly
undermine adoption.
**Signals:** "the robot is taking our jobs" in interviews; experts declining SME requests;
adoption metrics fine, override rates weird.
**Damages:** every launch's change curve; attrition of the top decile.
**Degrades:** HITL quality, labeling programs, `provider_adoption`, and the harvest rule's
legitimacy — capacity "freed" by force is capacity lost.

## Best practices

### BP-WF-01 — Driver-based capacity model
Staffing modeled from the same volume drivers the cost model uses (claims, denials, calls),
with hiring triggers at lead time, seasonal flex plans, and backlog-burn math.
**Markers:** capacity model reviewed monthly; requisitions trigger from drivers, not pain.
**Prevents:** OFM-WF-01. **Enables:** honest `hitl_capacity` sizing; the optimizer's launch
cadence gets a staffing reality check.

### BP-WF-02 — Academy onboarding with certification
Structured curriculum, simulation cases, competency certification *before* production work,
90-day error tracking with coaching.
**Markers:** time-to-independent-productivity measured and falling; new-hire error curves
converge regardless of trainer. **Prevents:** OFM-WF-02. **Enables:** stable human baselines
for AI efficacy comparisons; curriculum doubles as SOP corpus for retrieval.

### BP-WF-03 — Career lattice including AI-era roles
Dual tracks (mastery and management) with explicit rungs for the new work: exception
specialist, automation quality auditor, denial strategist, knowledge/label curator, loop
operator.
**Markers:** published lattice; internal fill rate for new roles >70%. **Prevents:**
OFM-WF-03, feeds -08. **Enables:** the playbook's roles are careers, not assignments.

### BP-WF-04 — Balanced scorecards
Individual performance = quality × resolution productivity × development, with QA weighting
that makes rubber-stamping expensive.
**Markers:** scorecard visible to the individual weekly; no single-metric bonuses.
**Prevents:** OFM-WF-04, -06 (jointly with BP-WF-06). **Enables:** HITL review quality;
GOV-07 audit sampling lands on people paid to catch errors.

### BP-WF-05 — Knowledge as managed asset
Cross-training matrix with minimum-two coverage on every critical process; payer playbooks and
"Maria's spreadsheet" migrations into governed documentation.
**Markers:** coverage matrix reviewed quarterly; PTO requires no heroics. **Prevents:**
OFM-WF-05. **Enables:** SME availability; the payer knowledge base (CAP-04) has human sources.

### BP-WF-06 — Incentives aligned to net yield and prevention
Team-level incentives on net realization, prevention outcomes, and patient-experience
measures; write-off authority separated from collection incentives.
**Markers:** prevention dollars in the bonus math; write-off pattern audits clean.
**Prevents:** OFM-WF-06. **Enables:** clean outcome labels; 8.6 governance holds under pressure.

### BP-WF-07 — Remote operating standard
Instrumented work (activity + outcome), virtual huddle rhythm, camera-on coaching sessions,
deliberate onboarding pods, engagement pulse with action loops.
**Markers:** QA sampling rates equal to pre-remote; remote/onsite performance gap <5%.
**Prevents:** OFM-WF-07.

### BP-WF-08 — The automation compact
An explicit, kept promise: automation harvests capacity through attrition, redeployment, and
growth absorption — not surprise layoffs; experts get first claim on the new roles (reviewer,
trainer, curator); every launch names its people plan.
**Markers:** compact published; top-decile attrition ≤ org average during launches; SME
volunteering rate rises. **Prevents:** OFM-WF-08. **Enables:** the VS-6 harvest rule becomes
credible; HITL and labeling attract the best rather than the leftover.

## Maturity anchors (AD-03)

| Level | Anchor |
|---|---|
| 0 | Vacancy spiral active; shadow training; no quality standards |
| 1 | Capacity gaps known; curriculum drafted; scorecards volume-only |
| 2 | Driver-based staffing; certification gate live; balanced scorecards |
| 3 | Career lattice with AI-era roles; knowledge coverage matrix; automation compact published |
| 4 | Turnover at/below benchmark; internal fill of AI-era roles; workforce metrics in the investment loop packet |
