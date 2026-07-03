# Binding validation & reconciliation report

Items: 278 | dangling references: 0 | FMs never produced by a PFM: 0 | UCs never referenced as hardened-by: 8 | facets never mentioned by any finding: 7


## Coverage gaps

- **FMs unproduced:** none
- **UCs unreferenced, failure-anchored (real gaps):** none
- **UCs opportunity-anchored (by design, ENG-05):** UC-01-14, UC-03-07, UC-04-02, UC-05-01, UC-05-02, UC-06-01, UC-13-03, UC-14-05
- **Facets unmentioned (reconciliation blind spots):** auth_transactions, baa_program, bias_program, citation_harness, outreach_consent, portal_automation_permitted, supply_chain_feed

## Reconciliation with the facet assessment

- Score-file source version: 2c0952099842 (current 2c0952099842)
- Flagged findings: 58 → **50 problem chains** (5 multi-layer, ENG-04)
- Weak facets in scope (class failure-explained): 30 | exempt by causality class (new-capability/contractual, ENG-01): 28
- In-scope weak facets **explained** by ≥1 flagged finding: 20
- Weak facets **unexplained** (contract violation — no linked finding): 10
  - appeal_outcomes, appeal_process, audit_channels_digitized, compliance_charter, consents_indexed, documentation_stability, edi_telemetry, provider_master, ranked_list_adoption, takeback_linkage
- Flagged findings with **no machine-readable binding at all**: 0

### Findings priced via FM→pool (ENG-03; overlapping attribution)

| Finding | Pools at stake | $ at stake/yr |
|---|---|---|
| PFM-11.2-02 | denial_prevention, denial_recovery | $32.0M |
| PFM-6.5-02 | denial_prevention | $25.9M |
| PFM-1.4-04 | denial_prevention | $25.9M |
| PFM-1.4-01 | denial_prevention | $25.9M |
| PFM-7.4-01 | underpayment | $19.2M |
| PFM-11.2-01 | underpayment | $19.2M |
| PFM-9.7-01 | bad_debt_reduction | $7.2M |
| PFM-1.3-04 | bad_debt_reduction | $7.2M |
| PFM-7.1-02 | denial_recovery | $6.0M |
| PFM-6.2-01 | audit_risk | $3.6M |

**Top multi-layer chains:** {PFM-11.2-02, PFM-6.5-02} → $32.0M (denial_prevention, denial_recovery); {OFM-ET-04, PFM-14.4-01} → $2.1M (labor_analytics); {OFM-OM-05, PFM-8.5-01, RFM-EXEC-03} → $0.0M (); {OFM-PI-04, PFM-8.1-02, RFM-DEN-01} → $0.0M (); {OFM-FG-02, PFM-13.1-01, RFM-ANL-02} → $0.0M ()
