# AFI Protocol Surface Investigation — Full Organization Audit

> **Phase 1 recon already complete?** Use [`audit/AFI_AUDIT_RESUME_PROMPT.md`](./audit/AFI_AUDIT_RESUME_PROMPT.md) instead. Checkpoint: [`audit/AFI_AUDIT_CHECKPOINT.md`](./audit/AFI_AUDIT_CHECKPOINT.md).

**Status:** Active — copy-paste prompt for in-house coding agent team  
**Version:** 0.1  
**Date:** 2026-06-03  
**Companion doc:** [`AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md`](./AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md)

---

## How to Use This Document

1. Read the companion spec first: [`AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md`](./AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md) (Sections 1–7).
2. Grant the agent team **read access** to all AFI-Protocol org repos (public and private).
3. Copy **everything below the horizontal rule** into the agent system or task prompt.
4. This is a **read-only forensic investigation** unless explicitly authorized otherwise.

---

# AFI Protocol Surface Investigation — Full Organization Audit

## Mission

Conduct a thorough, read-only forensic investigation across **every repository** in the AFI-Protocol organization (public and private). No stone left unturned. The goal is to **solidify the portable AFI protocol** along the direction captured in `afi-docs/specs/AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md`.

AFI is **not** Mongo-only, reactor-only, or monorepo-only. It is a portable protocol (HTTP-like): normative schemas and invariants at the top, pluggable implementations below. Your job is to map what is **normative**, what is **reference implementation**, what is **aspirational**, what is **stale**, and what **contradicts** the portable-protocol direction.

## Authority & Constraints

- **Read-only:** Do not modify code, configs, or docs unless explicitly instructed in a follow-up task.
- **Evidence-based:** Every finding must cite file paths and line ranges (or commit SHAs for remote-only repos).
- **Complete org coverage:** Enumerate all org repos via GitHub (`gh repo list`) or internal registry. Clone or sparse-checkout as needed. Private repos are in scope.
- **Cross-repo:** Trace concepts (USS, TSSD, mint, replay, emissions, vault, DAG) across repo boundaries.
- **No assumptions:** Verify claims in docs against executable code and schemas.

## Core Questions (Answer All)

### A. Normative Protocol Surface

1. What schemas, types, and docs are **normative** (protocol law)?
2. What invariants are stated but **not enforced** in code?
3. What is the **complete ingest boundary** (USS, CPJ, lenses, webhooks)?
4. What is the **canonical lifecycle** (RAW → ENRICHED → ANALYZED → SCORED → MINTED → REPLAYED) and where is each stage defined vs implemented?
5. What **determinism/replay** rules exist (`VALIDATOR_REPLAY_SPEC`, codex pins, config snapshots)?

### B. Reference Implementation Map

For each repo, classify as: `NORMATIVE` | `REFERENCE_IMPL` | `SUPPORTING` | `RESEARCH` | `DOCS` | `STALE` | `OUT_OF_SCOPE`.

6. Which repos implement the **reference spine** (ingest → DAG → vault → mint)?
7. Where does code **imply** Mongo, reactor, or org infra is mandatory?
8. Which vault engines are **actually implemented** vs only listed in `vault.schema.json`?

### C. Commitment Layer (BASE / On-Chain)

9. What exactly is stored on-chain today (events, receipt fields, roles, caps)?
10. What is **claimed** in docs vs **encoded** in contracts?
11. What would be required for a third party to verify a mint using only chain data + published rules?
12. Gap analysis: current breadcrumbs vs intended immutable commitment layer.

### D. Evidence Layer (Off-Chain Vault)

13. Where are `VaultedSignalRecord` and stage snapshots defined, written, read?
14. What is public surface vs proprietary detail in practice (not just spec)?
15. Replay readiness: can each stage be reconstructed from stored artifacts?

### E. Scoring & DAG Plane

16. Map all pipeline/DAG definitions (froggy, codex, blueprints, plugins).
17. Which nodes are replay-critical vs operational-only?
18. Where are analyst/validator/scoring formulas defined (`afi-core`, plugins, reactor)?
19. Does any doc claim reactor is **the only** orchestrator? Quote and classify.

### F. Market / Analytics Plane

20. Any BigQuery, Kafka, warehouse, or stream integrations?
21. Where would Mage-style pipelines fit without violating orchestration doctrine?
22. Separate **per-signal operational stores** from **analytics/feature planes** in findings.

### G. Emissions, Mint, Settlement

23. Trace emissions schedule: `afi-math` → `afi-mint` → `afi-token` contracts.
24. Per-signal mint vs epoch batch: what is implemented vs documented?
25. Beneficiary model: single payee vs split docs (`afi-econ`, token docs, whitepaper).
26. Treasury Safe roles vs mint recipient—what is production truth?

### H. Governance, Registries, Reputation

27. How do registries and reputation interact with scoring (must not override scores)?
28. What is wired vs simulation-only?

### I. SDKs, Gateway, External Validators

29. What **public protocol API** (SDKs/clients) is exposed for external builders?
30. Can an external validator integrate without org-private infra? What's missing?

### J. Documentation & Drift

31. Inventory architecture docs; flag stale repo names (`afi-pipeline`, etc.).
32. Build a **contradiction register**: doc A says X, code B does Y.
33. List docs that should be **normative**, **reference**, or **archived**.

## Per-Repo Investigation Checklist

For **each** org repo, produce a subsection with:

| Field | Content |
|-------|---------|
| Repo name | visibility (public/private) |
| Primary purpose | one sentence |
| Classification | NORMATIVE / REFERENCE_IMPL / etc. |
| Protocol touchpoints | USS, TSSD, mint, DAG, schemas, contracts, … |
| Normative artifacts | paths |
| Reference-only assumptions | paths + quotes |
| Contradictions | vs portable protocol surface |
| Replay relevance | none / partial / critical |
| Dependencies | upstream/downstream repos |
| Recommended action | none / tag stale / extract to spec / fix in follow-up |

## Search Patterns (Non-Exhaustive)

Run targeted searches across all repos for:

- `mongodb`, `MongoTSSD`, `vault`, `TSSD`, `VaultedSignalRecord`
- `usignal`, `USS`, `cpj`, `CPJ`
- `mintForSignal`, `coordinateMint`, `beneficiary`, `epoch`
- `replay`, `ReplaySession`, `determinism`, `codex`
- `publicSurface`, `proprietaryDetail`
- `AFIMintCoordinator`, `AFISignalReceipt`, `EmissionsMinted`
- `pipeline`, `DAG`, `froggy`, `orchestrator`, `doctrine`
- `BigQuery`, `kafka`, `warehouse`
- `normative`, `canonical`, `reference implementation`
- `postgresql`, `timescaledb`, `influxdb` (vault engines)

## Deliverables (Required Format)

### 1. Executive Summary (≤ 2 pages)

- Portable protocol alignment score (qualitative: strong / partial / fragmented)
- Top 10 blockers to solidification
- Top 10 quick wins (doc tags, clarifications, no code)

### 2. Master Reports (Markdown in `afi-docs/specs/`)

- `AFI_PROTOCOL_SURFACE_AUDIT.md`
- `AFI_NORMATIVE_REGISTER.md`
- `AFI_REFERENCE_IMPL_MAP.md`
- `AFI_CONTRADICTION_REGISTER.md`
- `AFI_REPLAY_READINESS_MATRIX.md`
- `AFI_ONCHAIN_ANCHOR_GAP_ANALYSIS.md`

### 3. Per-Repo Tables

One consolidated table + per-repo subsections as defined above.

### 4. Solidification Roadmap

Phased proposal (no implementation unless authorized):

| Phase | Focus | Outputs |
|-------|-------|---------|
| 0 — Discovery | This audit | Reports |
| 1 — Classify | Tag normative vs reference in docs | PRs to afi-docs, afi-config |
| 2 — Anchor spec | On-chain/off-chain minimum commitments | New spec in afi-config or afi-docs |
| 3 — Replay contract | External validator checklist | afi-config + sdk docs |
| 4 — Reconcile code | Remove mandatory-impl implications | Targeted issues per repo |

### 5. Open Questions for Human Review

List decisions that **cannot** be resolved by audit alone (e.g. how much signal payload hashes on-chain).

## Severity Rubric

| Severity | Definition |
|----------|------------|
| **P0** | External validator cannot interoperate; normative rule violated in production path |
| **P1** | Doc/code contradiction causes wrong architectural decisions |
| **P2** | Reference impl presented as protocol law; fixable by documentation |
| **P3** | Stale naming, typos, archived repo references |
| **Info** | Observation only |

## Definition of Done

- [ ] All org repos enumerated (count matches `gh repo list` or internal registry)
- [ ] Every repo has a classification row
- [ ] All six master reports exist with cross-links
- [ ] Contradiction register has ≥ 1 entry per major tension (Mongo-only, reactor-only, BASE ledger, econ splits, mint model)
- [ ] Replay readiness matrix covers all six lifecycle stages
- [ ] On-chain anchor gap analysis cites every relevant Solidity event/field
- [ ] Solidification roadmap approved-ready for human review

## Reference Document

Read first: `afi-docs/specs/AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md`

Canonical starting paths:

- `afi-config/docs/AFI_CONFIG_OVERVIEW.md`
- `afi-config/docs/REGISTRIES_AND_REPUTATION.v0.1.md`
- `afi-infra/docs/TSSD_VAULT_SPEC.md`
- `afi-reactor/docs/AFI_ORCHESTRATOR_DOCTRINE.md`
- `afi-reactor/docs/VALIDATOR_REPLAY_SPEC.v0.1.md`
- `afi-token/src/AFIMintCoordinator.sol`, `AFISignalReceipt.sol`
- `afi-mint/src/orchestrator/`
- `afi-math/src/emissions/emissionsSchedule.ts`

Begin investigation. Be exhaustive. Cite evidence. Do not skip private repos.
