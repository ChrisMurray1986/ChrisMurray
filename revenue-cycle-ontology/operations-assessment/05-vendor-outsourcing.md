# AD-05 Vendor & Outsourcing Management

The extended workforce and capability estate: BPO, collection agencies, coding/CDI vendors,
technology point solutions, and global delivery. The AI stack's vendor decisions (cost model
sourcing options, GOV-14) inherit whatever discipline — or absence of it — this domain shows.

---

## Failure modes

### OFM-VN-01 — Accidental outsourcing
The vendor footprint grew by accretion — a backlog crisis here, a departed team there — with no
sourcing strategy; scopes overlap, gaps hide between contracts.
**Signals:** nobody can produce the full vendor map with scopes and spend; two vendors touching
the same account class; work insourced and outsourced simultaneously at different sites.
**Damages:** KPI-CTC; accountability seams where accounts fall.
**Degrades:** the cost model's vendor-option pricing meets an unmapped baseline; platform
allocation double-counts what vendors already charge for.

### OFM-VN-02 — Set-and-forget contracts
Auto-renewals pass unexamined; SLAs exist in the contract and nowhere else; rates negotiated
years ago under different volumes.
**Signals:** renewal discovered by invoice; SLA reports produced by the vendor, unaudited;
"we've always used them."
**Damages:** external spend pool; performance leverage.
**Degrades:** Play 8 (renewal = decision reopened) has no muscle memory to build on; crossover
register findings die at renewal time.

### OFM-VN-03 — Black-box vendors
No access to vendor activity data, decision logic, call recordings, or outcome detail; oversight
is a monthly slide deck authored by the vendor.
**Signals:** contract grants no data/telemetry rights; QA of vendor work impossible; disputes
resolved by relationship.
**Damages:** 10.5/10.6 oversight duties (regulatory exposure for agency conduct); attribution.
**Degrades:** `agency_data_rights`; GOV-14 vendor diligence; UC-10-07/UC-14-07 are structurally
impossible until contracts change.

### OFM-VN-04 — Attribution wars
Contingency vendors claim credit for dollars that would have arrived anyway; internal teams
dispute it; nobody ran a control group.
**Signals:** vendor-reported "recoveries" exceed plausible pools; fee disputes as ritual;
the same dollar in two success stories.
**Damages:** external spend efficiency; benefit ledger integrity.
**Degrades:** the value model's single-counting rule (09 §4) — vendor claims contaminate the
same ledger the AI benefits report into.

### OFM-VN-05 — Knowledge exodus
The process was outsourced along with the knowledge of how it works; the organization can no
longer evaluate vendor quality, negotiate from competence, or ever insource.
**Signals:** no retained SME for the outsourced function; vendor transitions described as
impossible; internal QA of vendor output discontinued.
**Damages:** strategic flexibility; negotiation position; quality drift undetected.
**Degrades:** golden-set curation and efficacy evaluation for that function (nobody left who
can judge); the build-option BATNA in Play 8 becomes fiction.

### OFM-VN-06 — Unmanaged global delivery
Offshore/nearshore delivery adopted for rate arbitrage without operating investment: quality
variance by team, attrition invisible, SOPs forked from onshore versions years ago.
**Signals:** quality by shift/team unmeasured; vendor attrition rates unknown; escalation
timezone gaps; SOP versions diverged.
**Damages:** quality consistency; rework rates that erase the rate arbitrage.
**Degrades:** any HITL or labeling work placed in that delivery model inherits the variance —
the AI stack's review quality floor (GOV-07) can't be met by an unmeasured team.

## Best practices

### BP-VN-01 — Capability-based sourcing strategy
A deliberate map: which capabilities are core (build/retain), context (candidate to source),
and commodity (source aggressively); overlaps eliminated; every sourcing decision traceable to
the strategy.
**Markers:** vendor map with scopes/spend maintained; overlap spend quantified and falling.
**Prevents:** OFM-VN-01. **Enables:** the cost model's option comparisons start from a mapped
baseline; differentiator flags (10 §3) have an owner.

### BP-VN-02 — Active contract lifecycle management
Renewal calendar with 180-day decision gates; SLA scorecards measured from *your* data;
market-tested rates; termination assistance clauses standard.
**Markers:** zero surprise renewals; SLA credits actually collected. **Prevents:** OFM-VN-02.
**Enables:** Play 8 and the crossover register operate on existing rails.

### BP-VN-03 — Data-rights and telemetry standard clauses
Every vendor contract grants: activity-level data feeds, outcome detail, call recordings where
applicable, decision-logic transparency for automated decisions, and audit rights — as
non-negotiable paper.
**Markers:** clause present in all renewals; feeds actually flowing and used. **Prevents:**
OFM-VN-03. **Enables:** `agency_data_rights`, GOV-14, vendor oversight analytics.

### BP-VN-04 — Pre-agreed attribution with controls
Contingency arrangements define counting rules up front; holdout/control groups for recovery
vendors; one benefit ledger adjudicates all claims — vendor and internal alike.
**Markers:** attribution disputes rare and resolved by rule; control groups documented.
**Prevents:** OFM-VN-04. **Enables:** ledger integrity that the AI value claims also depend on.

### BP-VN-05 — Retained organization by design
Process ownership, QA sampling of vendor output, and at least one deep SME stay in-house for
every outsourced function; insourcing remains a priced option.
**Markers:** retained-org chart per vendor; internal QA of vendor work ≥ monthly; transition
playbooks exist. **Prevents:** OFM-VN-05. **Enables:** golden sets and efficacy evaluation for
vendor-performed functions; credible BATNAs.

### BP-VN-06 — Global delivery operating standard
Unified QA standards across shores; versioned single-source SOPs; vendor attrition and team
tenure reported; overlap-hour coverage designed; engagement investment treated as part of the
rate.
**Markers:** onshore/offshore quality gap <5%; SOP version parity audited. **Prevents:**
OFM-VN-06. **Enables:** globally delivered HITL/labeling that meets GOV-07 floors.

## Maturity anchors (AD-05)

| Level | Anchor |
|---|---|
| 0 | Unmapped vendor estate; auto-renewals; no data rights |
| 1 | Vendor inventory exists; SLAs tracked from vendor reports |
| 2 | Renewal gates with decisions; own-data scorecards; retained SMEs named |
| 3 | Sourcing strategy governs decisions; data-rights clauses standard; attribution rules pre-agreed |
| 4 | Vendor performance in the investment packet beside internal automations; insourcing/outsourcing moves executed from strategy, not crisis |
