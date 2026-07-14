# Districts / API Atlas Reconciliation Audit

> **This directory is a read-only reconciliation record. It does not establish protocol authority, authorize implementation, ratify proposed doctrine, or supersede accepted governance decisions. Recommendations become authoritative only through an owner-approved AFI governance decision.**

Preserved evidence from the read-only cross-repository Districts / API Atlas reconciliation audit (baseline `origin/main` as of afi-docs `c666224` and the sibling commits listed in the report). This is a **distinct** audit from the older protocol-surface corpus in `../` (normative register, contradiction register, on-chain anchor gap analysis); it is preserved here as a self-contained set.

## Contents

| File | What it is |
|---|---|
| [`AFI_DISTRICTS_API_ATLAS_AUDIT.md`](./AFI_DISTRICTS_API_ATLAS_AUDIT.md) | Complete human-readable audit: all 8 deliverables (executive verdict, current-state map, complete 96-finding register, contract/identifier crosswalk, lifecycle transition table, minimal implementation program, MongoDB/blockchain resumption gates, deferred register). |
| [`AFI_DISTRICTS_API_ATLAS_FINDINGS.json`](./AFI_DISTRICTS_API_ATLAS_FINDINGS.json) | Machine-readable register: metadata header + 96 findings with all fields. |
| [`AFI_DISTRICTS_API_ATLAS_FINDINGS.csv`](./AFI_DISTRICTS_API_ATLAS_FINDINGS.csv) | Same 96 findings, sortable/filterable (banner in leading `#` comment lines). |
| [`AFI_DISTRICTS_API_ATLAS_METHODOLOGY.md`](./AFI_DISTRICTS_API_ATLAS_METHODOLOGY.md) | Methodology, reliability, access limits, and the corrections appendix (two corrected agent errors). |

## Headline

Limited-but-real reconciliation debt, not an architectural crisis. The live ingest → normalize → validate → score → persist path is coherent; the lifecycle tail (validation → qualification → epoch → receipt → reward → claim) is unbuilt; the authority/naming layer is tangled. **96 findings**: 6 blocker, 32 high, 33 medium, 25 low.

The audit recommends a governance-first spine (District/authority registry → API Atlas → object identity → lifecycle → persistence → settlement) with MongoDB behind resumption Gate A and all blockchain work behind Gates B/C. **These are recommendations only; each becomes authoritative solely through an owner-approved governance decision.**
