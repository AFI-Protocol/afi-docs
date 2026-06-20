# AFI Normative Register

**Phase 4 synthesis report — AFI Portable Protocol Audit**
**Inputs:** themes A (normative surface), C (on-chain anchor), D (evidence vault), G (emissions/mint), H (governance) + `themes/verified.json`
**Status:** Staged in `afi-docs/specs/audit/final/`. Read-only forensic synthesis; no protocol code modified.

This register is the catalogue the North Star calls for: **"a single doc listing normative schemas, invariants, and on-chain/off-chain division of responsibility"** ([`AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md`](../../AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md) §5.1, §6). It enumerates every artifact the audit found to be **protocol law (normative)** — schemas, doc-stated invariants, and on-chain contracts — each with a `file:line` path, and it explicitly separates the **stated-but-unenforced** invariants (rules asserted in docs but with no code backing).

All paths are relative to `/home/user/AFI-Protocol/`. P0/P1 items carry a **Verified** status drawn from `themes/verified.json` (Phase 3 adversarial re-confirmation).

---

## Related reports (siblings)

This register is one of six cross-linked Phase-4 reports. All link back to [`AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md`](../../AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md):

- `AFI_PROTOCOL_SURFACE_AUDIT.md` — master report (exec summary, 31-repo table, findings by severity, roadmap).
- `AFI_REFERENCE_IMPL_MAP.md` — per-repo classification (normative vs reference vs research vs stale) and reference-spine segments.
- `AFI_CONTRADICTION_REGISTER.md` — all six doc/code tensions with verified status.
- `AFI_REPLAY_READINESS_MATRIX.md` — per-lifecycle-stage replay readiness (RAW→…→REPLAYED).
- `AFI_ONCHAIN_ANCHOR_GAP_ANALYSIS.md` — every relevant Solidity event/struct/field/role; current vs intended anchor.

---

## 1. Scope & method

The portable spec designates the normative surface as **"owned primarily by `afi-config` and cross-repo schema contracts"** (`AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md` §4.1). This register confirms and extends that table against live source: the normative law is owned chiefly by `afi-config` (the self-declared source of truth: `afi-config/docs/AFI_CONFIG_OVERVIEW.md:13-22` — "schemas and invariants here are normative (protocol law)"), with the canonical **evidence record** in `afi-infra`, the **replay invariants** bundled in the reference repo `afi-reactor`, and the **on-chain commitment semantics** in `afi-token/src/*.sol`.

Two of the protocol's five planes — **Commitment** and **Market/analytics** — have **no normative schema** in the canonical library (see §5). This is the headline structural gap and is the reason this register draws on Theme C (on-chain) and Theme G (emissions) to document the commitment-plane law that exists only in Solidity, not in `afi-config`.

---

## 2. Normative schemas (protocol law)

Canonical schemas owned by `afi-config` (JSON Schema Draft 2020-12), plus the cross-repo evidence-record type that the portable spec treats as normative.

| # | Normative schema / type | Path (`file:line`) | Notes |
|---|--------------------------|--------------------|-------|
| S1 | USS v1.1 ingest dialect (index + core) | `afi-config/schemas/usignal/v1_1/index.schema.json:7-31`; required keys `:235-239` (`source`/`providerId`/`signalId`) | The canonical "valid entry dialect". `ingestHash` field at `:258`; replay-canonical `facts` block at `:31`. |
| S2 | USS v1 (legacy) + 4 lenses | `afi-config/schemas/usignal/v1/index.schema.json:207-209` (provenance requires only `[timestamp]`); lenses `afi-config/schemas/usignal/v1/lenses/{equity,strategy,macro,onchain}.lens.schema.json` | `lens` field is **optional** (`v1_1/index.schema.json:14-30`), so lens/payload coherence is not schema-enforced. |
| S3 | CPJ v0.1 dialect | `afi-config/schemas/cpj/v0_1/index.schema.json:4-5` | "First normalization stage before USS v1.1 mapping." |
| S4 | Vault configuration | `afi-config/schemas/vault.schema.json:1-7`; engine enum `:14-23` | Engine enum `[mongodb,postgresql,timescaledb,influxdb]`; only `mongodb` implemented (see §4 contract C-EV). |
| S5 | Pipeline contract | `afi-config/schemas/pipeline.schema.json:5` | Hard-binds description to `afi-reactor`; default `signalSchema` is the weaker `afi.usignal.v1` at `:70-71`. |
| S6 | Blueprint / construct-graph contract | `afi-config/schemas/blueprint.schema.json:3-9` | Normative graph schema; **unused by reactor** (0 hits) per Theme E. |
| S7 | Plugin manifest | `afi-config/schemas/plugin-manifest.schema.json` | Description references the `afi-plugins` registry. |
| S8 | Validator config | `afi-config/schemas/validatorConfig.schema.json:6-46`; on-chain refs `:79-103` | Pins determinism-relevant thresholds (`mintApprovalThreshold` default 0.66, `snapshotSpaceId`); references coordinator `coordinatorAddress`/`chainId` (`:82-87`) but is an **internal** mint-daemon config, not a third-party interop schema. |
| S9 | Analyst config | `afi-config/schemas/analyst-config.schema.json` | Per-analyst scoring config. |
| S10 | Enrichment-node definition | `afi-config/schemas/definitions/enrichment-node.schema.json` | Node-level contract. |
| S11 | **Canonical evidence record** `VaultedSignalRecord` (+ stage snapshots) | `afi-infra/src/tssd/types.ts:331`; stages map `:336-351`; snapshots `:45/60/81/167/187/249`; public/proprietary split `:206-234` | Treated as normative by the portable spec (§4.1) but **defined only in a reference repo** (`afi-infra`), not in the canonical `afi-config` library. |
| S12 | Lifecycle stage enum `SignalLifecycleStage` | `afi-infra/src/tssd/types.ts:10-16` (`RAW\|ENRICHED\|ANALYZED\|SCORED\|MINTED\|REPLAYED`) | The only enumerated lifecycle; **not present in the `afi-config` schema library** (see invariant I1 / finding below). |

**Off-chain receipt schema (mint plane, `afi-mint`).** `afi-mint/codex/mint_receipt_schema.json:6-13` requires `['signal_id','score','mint_amount','validator_id','challenge_status','timestamp']`. It is published as the audit/replay anchor but **diverges from the on-chain `MintRequest` shape** (see §4 contract C-MC and §6).

---

## 3. Normative invariants (stated as protocol law)

Invariants asserted as binding rules in the canonical docs. Enforcement status is summarised here and detailed in §4 (contracts) and §5 (stated-but-unenforced).

| # | Invariant (as stated) | Source (`file:line`) | Enforced? |
|---|-----------------------|----------------------|-----------|
| I1 | Canonical lifecycle `RAW→ENRICHED→ANALYZED→SCORED→MINTED→REPLAYED` | `afi-infra/src/tssd/types.ts:10-16`; North Star `AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md` §5 | **No** — no enumerated `stage` field in canonical schema; only a boolean index hint `afi-config/schemas/vault.schema.json:95-98`. See §5-U1. |
| I2 | Vault finality / immutability is **absolute** | `afi-config/docs/REGISTRIES_AND_REPUTATION.v0.1.md:111` | **No** — only canonical writer overwrites (deleteOne+insertOne). See §5-U2. |
| I3 | Determinism: same codex version + same config + same data snapshot ⇒ same validator outputs | `afi-reactor/docs/VALIDATOR_REPLAY_SPEC.v0.1.md:37`; spec normative-grade `:67` | **No** — record pins no version/topology/content-hash. See §5-U3. |
| I4 | Replay isolation: replay must not mutate production state; traceability required | `afi-reactor/docs/VALIDATOR_REPLAY_SPEC.v0.1.md:35-41` | Partial / design-only — replay runner is a read-only stub `afi-infra/src/tssd/TSSDReplayRunner.ts:40-103`. |
| I5 | Reputation MUST NOT modify UWR scoring, override vault/Codex finality, or change DMV logic | `afi-config/docs/REGISTRIES_AND_REPUTATION.v0.1.md:104-115`; echoed `afi-core/validators/UniversalWeightingRule.ts:22-24`, `afi-core/validators/ValidatorDecision.ts:5` | **No runtime guard** (honor system); and an allocation path scales mint amount by reputation. See §5-U4. |
| I6 | All signals must include `provenance.timestamp` | `afi-config/docs/AFI_CONFIG_OVERVIEW.md:122` | **Stale** — USS v1.1 demotes `timestamp` to legacy/optional `afi-config/schemas/usignal/v1_1/index.schema.json:235-239`. See §5-U5. |
| I7 | Ingest boundary is the USS v1.1 / CPJ v0.1 dialect | `AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md` §3.2; dialect `afi-config/schemas/usignal/v1_1/index.schema.json:7-14` | **Split / inconsistent** — reactor enforces via AJV `afi-reactor/src/server.ts:211`; gateway bypasses it `afi-gateway/src/http/app.ts:26-27,134`. See §5-U6. |
| I8 | 86B total supply cap is an immutable on-chain ceiling | `afi-token/src/AFIToken.sol:35`, enforced `:97-98` | **Yes** — the one strong, independently verifiable on-chain guarantee. |
| I9 | Schema layer is advisory: "Nothing is network-enforced at the schema level" | `afi-config/docs/AFI_CONFIG_OVERVIEW.md:121` | Self-declared — confirms most invariants above are honor-system. |
| I10 | Commitment linkage: on-chain artifacts link to off-chain evidence via `signalId`, epoch, and (where specified) content hashes | `AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md` §3.4 rule 4 | **Partial** — `signalId`/epoch are emitted in logs only; **no content hash** anchored. See §4 C-MC and §5-U3. |

---

## 4. Normative contracts (on-chain commitment plane)

The commitment-plane law lives **only** in `afi-token/src/*.sol` (Foundry/OZ). `afi-mint/contracts/*.sol` are empty stubs (`afi-mint/contracts/MintManager.sol:4-5`) and `afi-xerc20` is an out-of-scope vendored bridge fork (`afi-xerc20/package.json:6`). Full enumeration belongs to `AFI_ONCHAIN_ANCHOR_GAP_ANALYSIS.md`; the normative essentials are:

| # | Contract artifact | Path (`file:line`) | Normative content |
|---|-------------------|--------------------|-------------------|
| C-TK | `AFIToken.mintEmissions(beneficiary, amount)` | `afi-token/src/AFIToken.sol:92`; cap check `:97-98`; cap const `:35` | Sole emissions entrypoint; gated `onlyRole(EMISSIONS_ROLE)`; enforces only the 86B `TOTAL_SUPPLY_CAP`. |
| C-TK-EV | Event `EmissionsMinted(address indexed beneficiary, uint256 amount)` | `afi-token/src/AFIToken.sol:40` | On-chain emissions breadcrumb. |
| C-MC | `AFIMintCoordinator.MintRequest` struct + `mintForSignal` | struct `afi-token/src/AFIMintCoordinator.sol:19-26`; mint `:68-76` | `{beneficiary, tokenAmount, receiptId, receiptAmount, signalId, epoch, extraData}` — **calldata only**; **no `contentHash`/`payloadHash`/`rulesetVersion` field**. |
| C-MC-EV | Event `MintCoordinated(bytes32 signalId, uint256 epochId, address beneficiary, uint256 tokenAmount, uint256 receiptAmount)` | `afi-token/src/AFIMintCoordinator.sol:38-44`; emit `:85` | `signalId`/`epoch` are **emitted in logs only**, never persisted to storage. |
| C-RC | `AFISignalReceipt` ERC-1155 + event `ReceiptMinted(address to, uint256 id, uint256 amount, bytes data)` | `afi-token/src/AFISignalReceipt.sol:15` | Opaque `id` + raw `data`; URI is a placeholder `afi-token/script/DeployAFITokenMainnet.s.sol:103`. |
| C-RL | Roles `DEFAULT_ADMIN_ROLE`, `EMISSIONS_ROLE`, `MINT_COORDINATOR_ROLE` | `afi-token/src/AFIToken.sol:32,35`; coordinator `EMISSIONS_ROLE` `afi-token/src/AFIMintCoordinator.sol:14`; receipt role `afi-token/src/AFISignalReceipt.sol:13` | Mainnet Pattern A grants **both** admin + emissions to one Treasury Safe `afi-token/script/DeployAFITokenMainnet.s.sol:62-63`. |
| C-EV | Evidence-plane storage contract `ITSSDVaultClient` | `afi-infra/src/tssd/TSSDVaultClient.ts:36-68` | Engine-neutral seam; only the `mongodb` binding exists (`afi-infra/src/tssd/MongoTSSDVaultClient.ts:220-221`) vs the 4-engine schema enum (S4). |
| C-SCH | Off-chain emissions schedule (canonical) | `afi-math/src/emissions/emissionsSchedule.ts:4,59-60` | 86B three-phase float schedule; **not on-chain authoritative** — afi-token enforces only the cap. |

---

## 5. Stated-but-unenforced invariants (the critical section)

These are normative rules asserted in docs/specs with **no code backing**. Each carries its **Verified** status from `themes/verified.json` (all listed here were re-opened in Phase 3 and **confirmed**; severities held at P1).

### U1 — Lifecycle is normative law but has no machine-enforceable stage field
- **Stated:** `RAW→…→REPLAYED` is the canonical lifecycle (`afi-infra/src/tssd/types.ts:10-16`; North Star §5).
- **Reality:** the canonical `afi-config` library carries **no enumerated `stage` field** — only a boolean index hint: `afi-config/schemas/vault.schema.json:95-98` ("Create index on signal stage (RAW, ENRICHED, etc.)"). The only enum lives in a reference repo (`afi-infra`), so an external stack cannot machine-validate lifecycle conformance from the source of truth.
- **Severity P1 — Verified: CONFIRMED** (`verified.json` `theme:A-normative-surface#0`, independently `draft:13`; revised severity P1).

### U2 — Vault immutability/finality is "absolute" but the only writer overwrites
- **Stated:** `afi-config/docs/REGISTRIES_AND_REPUTATION.v0.1.md:111` — "Vault finality (T.S.S.D. Vault immutability) is absolute; reputation cannot rewrite history."
- **Reality:** `MongoTSSDVaultClient.upsert` sets `updatedAt=now` (`afi-infra/src/tssd/MongoTSSDVaultClient.ts:150`) then, when a record exists, `deleteOne(filter)` (`:157`) + `insertOne(doc)` (`:160`) — destructive overwrite-in-place; nothing prevents re-writing a finalized signal.
- **Severity P1 — Verified: CONFIRMED** (`theme:A-normative-surface#2`).

### U3 — Determinism/replay is normative but nothing is pinned at the record level
- **Stated:** `afi-reactor/docs/VALIDATOR_REPLAY_SPEC.v0.1.md:37` — "Same codex version + same config + same data snapshot → same validator outputs" (spec declares itself normative for invariants at `:67`).
- **Reality:** `VaultedSignalRecord` pins no codex/DAG-topology/plugin/scorer version or content hash (`afi-infra/src/tssd/types.ts:331-367`; only optional `strategyVersion?` at `:112`); the reference DAG generates execution IDs with `Date.now()+Math.random()` (`afi-reactor/src/dag/DAGExecutor.ts:1002-1003`). A stored record cannot be bound to the exact transforms that produced it.
- **Severity P1 — Verified: CONFIRMED.** Same root cause verified independently three ways: `theme:A-normative-surface#3` = `theme:D-evidence-vault#0` = `draft:53`.

### U4 — "Reputation must not override scoring/finality" is honor-system, and an allocation path violates it
- **Stated:** `afi-config/docs/REGISTRIES_AND_REPUTATION.v0.1.md:104-115` — reputation must not modify UWR, override finality, or change DMV logic; echoed only as code comments `afi-core/validators/UniversalWeightingRule.ts:22-24`, `afi-core/validators/ValidatorDecision.ts:5`.
- **Reality:** no runtime guard exists. Moreover the emissions amount is scaled by an **unpinned** `reputationWeight` and a governance-controlled `epochPulseFactor` (`afi-mint/src/adapters/EmissionsMintDataProvider.ts:272-273,281`), and a successful Snapshot challenge overturns the deterministic mint/reject decision (`afi-mint/src/orchestrator/SignalStateManager.ts:284-286`). Neither factor is anchored in the on-chain receipt (`afi-token/src/AFISignalReceipt.sol:15`; `afi-token/src/AFIMintCoordinator.sol:19-26`), so the reputation/governance influence on allocation is neither deterministic nor auditable.
- **Severity P1 (allocation non-replayability) — Verified: CONFIRMED.** `theme:H-governance#1` = `theme:G-emissions-mint#2` = `draft:66`. (The pure honor-system observation `theme:H-governance#0` is P2.)

### U5 — Overview mandates `provenance.timestamp` but the runtime canon makes it optional
- **Stated:** `afi-config/docs/AFI_CONFIG_OVERVIEW.md:122` — "All signals must include `provenance.timestamp`."
- **Reality:** USS v1.1 requires `source/providerId/signalId` and labels `timestamp` a legacy field (`afi-config/schemas/usignal/v1_1/index.schema.json:235-239`).
- **Severity P2 / Info (doc-drift; full catalogue in `AFI_CONTRADICTION_REGISTER.md` / Theme J).**

### U6 — Normative ingest dialect is unenforced on the production path
- **Stated:** the ingest boundary is the USS v1.1 / CPJ v0.1 dialect (North Star §3.2; dialect schema S1).
- **Reality:** the production gateway validates only 4 identity fields (`afi-gateway/src/http/app.ts:26-27`) and upserts straight to the vault (`:134`) with **no** USS/CPJ validation, while the reactor server enforces the dialect via AJV (`afi-reactor/src/server.ts:211`). Two divergent ingest contracts.
- **Severity P1 — Verified: CONFIRMED.** `theme:A-normative-surface#1` = `theme:I-sdks-gateway#0` = `draft:43`.

### U7 — Commitment linkage promises content-hash binding that does not exist on-chain
- **Stated:** North Star §3.4 rule 4 — on-chain artifacts link to off-chain evidence via `signalId`, epoch, and content hashes; §3.5 frames BASE as a replayable/auditable commitment ledger.
- **Reality:** the `MintRequest`/`MintCoordinated` anchor carries **no content/payload hash, score, validator id, UWR axes, or ruleset version** (`afi-token/src/AFIMintCoordinator.sol:19-26`; reproducible negative search `rg -nwi -c "contentHash|payloadHash|merkle|rulesetVersion" afi-token/src` → 0 hits). A third party can confirm a mint happened under the cap but cannot verify it was legitimately scored or bound to real evidence. Detailed in `AFI_ONCHAIN_ANCHOR_GAP_ANALYSIS.md`.
- **Severity P1 — Verified: CONFIRMED.** `theme:C-onchain-anchor#0` (no on-chain hash) and `theme:C-onchain-anchor#1` (mint gated only by `EMISSIONS_ROLE`).

---

## 6. Coverage gap: 2 of 5 protocol planes have no normative schema

The portable spec defines five planes — Commitment, Evidence, Scoring DAG, Market/analytics, Ingest boundary (`AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md` §3.2). The canonical `afi-config` schema library covers **Evidence (S4/S11), Scoring DAG (S5/S6/S7), and Ingest (S1–S3)** but contains **no Commitment-plane schema** (no on-chain receipt/anchor schema) and **no Market/analytics-plane schema**:

- Reproducible negative searches (from `/home/user/AFI-Protocol/`): `rg -nc "EmissionsMinted|mintForSignal|AFISignalReceipt|contentHash" afi-config/schemas` → 0 hits; `rg -nwi -c "kafka|warehouse|snowflake|redshift|datalake" afi-config/schemas` → 0 hits. The only on-chain reference is a coordinator address/chainId field at `afi-config/schemas/validatorConfig.schema.json:82-87`, not a commitment-plane schema.
- **Severity P1 — Verified: CONFIRMED.** `theme:A-normative-surface#4` = `draft:14`.

Consequence: external validators cannot validate on-chain↔off-chain linkage (North Star rule 4) from the schema library alone. This is the structural reason the commitment-plane law in §4 lives in Solidity rather than in `afi-config`.

---

## 7. Verified-status summary (P0/P1 items cited by this register)

All entries below were adversarially re-confirmed in Phase 3 (`themes/verified.json`); the harness reports 33/33 P0/P1 coverage, all `confirmed=true`, **zero refutations and zero severity changes**.

| Register item | Source ID(s) in `verified.json` | Original → Revised | Verified |
|---------------|----------------------------------|--------------------|----------|
| U1 lifecycle has no canonical stage field | `theme:A-normative-surface#0`; `draft:13` | P1 → P1 | CONFIRMED |
| U6 gateway bypasses USS/CPJ | `theme:A-normative-surface#1`; `theme:I-sdks-gateway#0`; `draft:43` | P1 → P1 | CONFIRMED |
| U2 vault immutability unenforced | `theme:A-normative-surface#2` | P1 → P1 | CONFIRMED |
| U3 record-level determinism unpinned | `theme:A-normative-surface#3`; `theme:D-evidence-vault#0`; `draft:53` | P1 → P1 | CONFIRMED |
| §6 two planes have no normative schema | `theme:A-normative-surface#4`; `draft:14` | P1 → P1 | CONFIRMED |
| U7 no content/ruleset hash on-chain | `theme:C-onchain-anchor#0` | P1 → P1 | CONFIRMED |
| U7 mint gated only by `EMISSIONS_ROLE` | `theme:C-onchain-anchor#1` | P1 → P1 | CONFIRMED |
| Reactor scoring bypasses canonical vault (SCORED never written) | `theme:D-evidence-vault#1` | P1 → P1 | CONFIRMED |
| Public/proprietary split structural only | `theme:D-evidence-vault#2` | P1 → P1 | CONFIRMED |
| Emissions schedule inlined (drift risk) | `theme:G-emissions-mint#0` | P1 → P1 | CONFIRMED |
| Goldpaper mint formula ≠ implemented formula | `theme:G-emissions-mint#1` | P1 → P1 | CONFIRMED |
| Governance/reputation can override deterministic mint | `theme:G-emissions-mint#2`; `theme:H-governance#1`; `draft:66` | P1 → P1 | CONFIRMED |
| On-chain enforces no schedule/score (only cap) | `theme:G-emissions-mint#3` | P1 → P1 | CONFIRMED |
| Single-beneficiary vs research splits | `theme:G-emissions-mint#4` | P1 → P1 | CONFIRMED |
| Mongo-only vs multi-engine schema | `draft:52`; `draft:84` | P1 → P1 | CONFIRMED |

---

## 8. Recommendations (carry-forward)

1. **Promote the lifecycle and replay law into `afi-config`.** Add a normative enumerated `stage` field and a concrete `ValidatorReplaySession` schema (today bundled in the reference repo `afi-reactor`), so external validators can validate lifecycle/replay conformance from the source of truth.
2. **Make replay-pinning normative.** Require record-level `codexVersion`/`configSnapshotId`/`dagTopologyHash`/`payloadHash` on `VaultedSignalRecord` and a deterministic execution ID/ordering in the reference DAG (U3).
3. **Add the missing-plane schemas.** Define a normative Commitment-plane receipt schema (`signalId`/epoch/amounts/beneficiary/`contentHash`/`rulesetVersion`) and at least an interface schema for the analytics plane (§6, U7).
4. **Back the stated invariants with code.** Enforce vault append-only/immutability (U2), route gateway ingest through USS/CPJ validation or document it as pre-canonicalized only (U6), and convert the reputation-non-interference rule into a testable guard with pinned receipt fields (U4).
5. **Reconcile the receipt dialects.** Align the off-chain `mint_receipt_schema.json` with the on-chain `MintRequest` and add the determinism-anchoring fields to both (§2, §4 C-MC).

---

*Backlink:* [`AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md`](../../AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md) · *Generated by the report-synthesizer worker from themes A, C, D, G, H and `themes/verified.json`.*
