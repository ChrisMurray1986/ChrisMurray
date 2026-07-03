# AD-04 Enabling Technology (non-AI)

The conventional technology estate the AI stack stands on: EHR optimization, workqueues,
bolt-ons, legacy RPA, telephony, patient-facing tech, and integration hygiene. Most "AI
readiness" gaps found by the facet assessment have their root cause here.

---

## Failure modes

### OFM-ET-01 — The unoptimized EHR
Workqueues, edits, and routing still carry install-era defaults; hundreds of workqueues, many
ownerless, overlapping, or empty-by-miracle; optimization stopped at go-live.
**Signals:** workqueue count nobody can state; "we've always routed it that way"; paid-for
functionality unused; accounts touched by five queues before resolution.
**Damages:** every queue-based process; touch counts; staff trust in the system.
**Degrades:** `queue_api` value (APIs over chaos automate chaos); the workflow dimension's
sufficiency floors are missed for configuration reasons, not capability ones.

### OFM-ET-02 — Bolt-on sprawl
Point solutions accreted per pain-point: three eligibility tools, two estimators, overlapping
claim scrubbers — with contradictory data and double fees.
**Signals:** vendor inventory nobody owns; two systems disagreeing on the same account; renewal
dates discovered by invoice.
**Damages:** KPI-CTC; data consistency; staff context-switching.
**Degrades:** `system_copy_extracts` drift becomes structural; masters diverge by design;
the cost model's platform allocation math meets a zoo.

### OFM-ET-03 — Upgrade and adoption debt
Versions behind; features licensed but never turned on; every upgrade a trauma so upgrades are
deferred, deepening the trauma.
**Signals:** release notes unread; "we're two versions behind" as ambient fact; vendor
features re-bought from third parties because nobody knew.
**Damages:** capability currency; security posture; total cost.
**Degrades:** implementation-pattern scores (file 14) — gates that current versions satisfy
natively score 0 for staleness reasons.

### OFM-ET-04 — The RPA graveyard
Pre-AI bots built by a departed contractor, unmonitored, breaking silently on portal changes;
work vanishes without a hand-back.
**Signals:** "there's a bot for that... I think"; no bot registry; discovery of failure via
downstream complaints weeks later.
**Damages:** whatever the bots touched; institutional trust in automation.
**Degrades:** `handback_queues`, fleet-observability adoption (UC-14-04 inherits distrust);
FM-BOTSILENT already happened here at small scale.

### OFM-ET-05 — Telephony/CRM disconnect
PFS agents answer patient calls without integrated account context: separate phone system,
billing screens, and notes; every call starts with archaeology.
**Signals:** handle times dominated by lookup; patients repeating their story; call notes in a
system billing never reads.
**Damages:** 10.2 service quality; KPI-COMPLAINTS; agent burnout.
**Degrades:** `account_360` (the human version is missing, so the API version has no
requirements owner); conversational-AI use cases inherit an unmapped escalation surface.

### OFM-ET-06 — Patient-facing tech without adoption operations
Portal billing, estimates, e-statements, payment plans exist — with single-digit adoption and
nobody accountable for changing that.
**Signals:** adoption metrics unreported; "patients don't use it" as conclusion rather than
problem; enrollment friction never walked by a leader.
**Damages:** VS-4 patient-cash value pool; statement cost; call volume.
**Degrades:** `statement_history`/digital-channel data too thin to train on; the
patient-experience automation family starves.

### OFM-ET-07 — Interface spaghetti
Point-to-point interfaces accreted over years, undocumented, resilient only in the memory of
one engineer; changes are feared.
**Signals:** interface inventory absent; "don't touch that feed"; outage post-mortems
rediscovering topology.
**Damages:** every cross-system flow; downtime recovery (14.6).
**Degrades:** `fabric` cost balloons (the event backbone must first excavate the spaghetti);
`edi_telemetry` has no clean tap points.

### OFM-ET-08 — The spreadsheet empire
Critical operations run on Excel/Access built by staff: the underpayment tracker, the credit
log, the crosswalk that prices drug charges.
**Signals:** files named FINAL_v7; macros nobody can edit; audit requests answered from a
laptop.
**Damages:** control environment; continuity; audit defense.
**Degrades:** `masterdata_governance` and half the data facets score partial solely because the
real system-of-record is a spreadsheet — the audit's "govern the table first" findings live here.

## Best practices

### BP-ET-01 — Annual EHR optimization cycle
A standing optimization program: workqueue rationalization with named owners per queue, edit
tuning against hit/change rates, adoption of unused licensed features; measured in touches
removed.
**Markers:** workqueue inventory with owners and purpose; queue count trending down; a
feature-harvest review after every upgrade. **Prevents:** OFM-ET-01, -03. **Enables:** the
workflow and integration gates at their configuration floors.

### BP-ET-02 — Capability-based application portfolio
One inventory mapping applications to capabilities; overlaps flagged; every capability has one
system-of-record and one owner; rationalization roadmap with retirement dates.
**Markers:** portfolio reviewed annually; duplicate-capability spend quantified and falling.
**Prevents:** OFM-ET-02. **Enables:** master-data drift monitoring has a defined truth topology.

### BP-ET-03 — Stay-current policy with feature harvest
Version currency as policy (N or N−1); upgrades scheduled, rehearsed, and followed by a
feature-adoption sprint.
**Markers:** version dashboard green; features adopted per upgrade counted. **Prevents:**
OFM-ET-03.

### BP-ET-04 — Bot lifecycle management
Registry of every bot with owner, purpose, and monitoring; failure hand-back to named human
queues; retirement dates; portal-change alerting.
**Markers:** zero unregistered bots on credential audit; failures surface in hours.
**Prevents:** OFM-ET-04. **Enables:** GOV-05/UC-14-04 arrive as an upgrade to an existing
discipline instead of a new religion.

### BP-ET-05 — Integrated agent desktop
CTI screen-pop with unified account context (HB+PB), knowledge at point of use, and call notes
written into the account record.
**Markers:** lookup time <15s; first-call resolution measured. **Prevents:** OFM-ET-05.
**Enables:** `account_360` requirements exist and are tested by humans daily before the
conversational agent needs them.

### BP-ET-06 — Digital adoption operations
Adoption of patient-facing tech run as an operation: targets, enrollment-at-touchpoint scripts,
friction walks, A/B'd prompts; reported beside cash metrics.
**Markers:** portal-billing adoption, e-statement rate, self-service payment share all
targeted and trending. **Prevents:** OFM-ET-06. **Enables:** VS-4 value pools; channel data
for statement optimization.

### BP-ET-07 — Integration architecture standards
Interface inventory and topology documentation; engine-based patterns over point-to-point;
resilience tested; no single-engineer dependencies.
**Markers:** any feed's owner, path, and failure mode answerable in minutes; DR test annual.
**Prevents:** OFM-ET-07. **Enables:** the fabric lands on a mapped estate.

### BP-ET-08 — Spreadsheet amnesty and migration
A no-blame inventory of shadow tools, ranked by criticality; migration into governed tables
with the original builders as design authorities.
**Markers:** critical-process spreadsheet count falling to zero; builders promoted into data
stewardship, not routed around. **Prevents:** OFM-ET-08. **Enables:**
`masterdata_governance`, the crosswalk and register facets, audit-grade control.

## Maturity anchors (AD-04)

| Level | Anchor |
|---|---|
| 0 | Install-default EHR; unmanaged bots; spreadsheet-critical operations |
| 1 | Inventories exist (queues, apps, interfaces, bots); optimization ad hoc |
| 2 | Annual optimization cycle; bot registry; agent desktop integrated |
| 3 | Capability-based portfolio governed; stay-current policy; digital adoption operation running |
| 4 | Technology estate metrics in the investment packet; configuration-class changes ship in days; zero shadow systems-of-record |
