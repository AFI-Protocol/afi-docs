# AFI Contradiction Register

**Phase 4 synthesis report — AFI Portable Protocol Audit**
**Inputs:** all 10 themes (A–J) + `themes/verified.json` (Phase 3 adversarial re-confirmation) + `drafts/AFI_CONTRADICTION_REGISTER.draft.md` (103-row Phase-1 baseline, promoted here)
**Status:** Staged in `afi-docs/specs/audit/final/`. Read-only forensic synthesis; no protocol code modified.

This register is the verified successor to the Phase-1 draft. It catalogues the **doc/code contradictions** the audit found across the AFI corpus, organised by the **six canonical tensions**, and — for every **P0/P1** entry — carries the **Verified** status drawn from `themes/verified.json`. It is the contradiction half of the catalogue the North Star calls for ([`AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md`](../../AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md) §5, §6).

All paths are relative to `/home/user/AFI-Protocol/`. The full unverified 103-row baseline lives in `drafts/AFI_CONTRADICTION_REGISTER.draft.md`; row IDs of the form `draft:NN` below reference that table.

---

## Related reports (siblings)

This register is one of six cross-linked Phase-4 reports. All link back to [`AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md`](../../AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md):

- `AFI_PROTOCOL_SURFACE_AUDIT.md` — master report (exec summary, 31-repo table, findings by severity, roadmap).
- `AFI_NORMATIVE_REGISTER.md` — normative schemas/invariants/contracts and stated-but-unenforced invariants.
- `AFI_REFERENCE_IMPL_MAP.md` — per-repo classification (normative vs reference vs research vs stale) and reference-spine segments.
- `AFI_REPLAY_READINESS_MATRIX.md` — per-lifecycle-stage replay readiness (RAW→…→REPLAYED).
- `AFI_ONCHAIN_ANCHOR_GAP_ANALYSIS.md` — every relevant Solidity event/struct/field/role; current vs intended anchor.

---

## 1. Scope & method

The portable spec frames the AFI surface as **normative law vs reference implementation vs pluggable choice**, across five planes (Commitment, Evidence, Scoring DAG, Market/analytics, Ingest boundary) (`AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md` §3.2). Most contradictions in the corpus are a single failure mode in different repos: **a reference implementation (or one storage/orchestration choice) is presented as protocol law.** The audit normalises these into six tensions:

| Tension | One-line definition |
|---------|---------------------|
| **Mongo-only** | Evidence/persistence plane (and the ingest path that feeds it) is hard-bound to MongoDB, contradicting the multi-engine `vault.schema.json` and the engine-neutral `ITSSDVaultClient` contract. |
| **reactor-only** | `afi-reactor` (and SDKs/docs pointing at it) is presented as THE only orchestrator / "the DAG is law", contradicting the pluggable scoring-DAG plane. |
| **BASE-ledger** | The on-chain commitment plane anchors no content/score/ruleset hash and enforces only role+cap, contradicting the "replayable, third-party-verifiable commitment ledger" framing. |
| **econ-splits** | On-chain mint is single-beneficiary; the multi-role gauge/split model exists only in research (`afi-econ`), contradicting whitepaper-grade split language. |
| **mint-model** | The implemented emissions/mint path (inlined schedule, proportional allocation, governance/reputation multipliers, divergent state machines) diverges from the documented mint model. |
| **stale-arch-docs** | Docs/metadata reference removed repos, wrong toolchains, and non-existent files; reference docs self-declare authority without naming the portable spec as canonical. |

**Verified status.** Every P0/P1 row carries its status from `themes/verified.json`. The Phase-3 verifier re-opened all 33 P0/P1 sources (22 theme findings + 11 draft rows); the gate reports **33/33 covered, all `confirmed=true`, zero refutations, zero severity changes** — so every P0/P1 below is **CONFIRMED (P1→P1)**.

**Deduplication (collapsed rows).** The verifier flagged five facts that were verified independently from multiple sources and are the **same underlying issue**; each is collapsed here into a single register row carrying the strongest `file:line` set and **all** corroborating source IDs (see §8):

- replay-pinning absent: `theme:A-normative-surface#3` = `theme:D-evidence-vault#0` = `draft:53`
- governance/reputation override: `theme:G-emissions-mint#2` = `theme:H-governance#1` = `draft:66`
- gateway bypasses USS/CPJ: `theme:A-normative-surface#1` = `theme:I-sdks-gateway#0` = `draft:43`
- reactor-only orchestrator: `theme:E-scoring-dag#1` = `draft:83`
- Mongo-only multi-engine gap: `draft:52` = `draft:84`

---

## 2. Tension coverage summary

| Tension | Entries (this register) | Highest severity | P0/P1 verified? |
|---------|------------------------|------------------|-----------------|
| Mongo-only | C-MO-1 … C-MO-9 (+draft P2/P3) | P1 | Yes — all CONFIRMED |
| reactor-only | C-RO-1 … C-RO-2 (+draft P2/P3) | P1 | Yes — all CONFIRMED |
| BASE-ledger | C-BL-1 … C-BL-3 (+draft P2/P3) | P1 | Yes — all CONFIRMED |
| econ-splits | C-ES-1 (+draft Info) | P1 | Yes — CONFIRMED |
| mint-model | C-MM-1 … C-MM-4 (+draft P2/P3) | P1 | Yes — all CONFIRMED |
| stale-arch-docs | C-SD-1 … C-SD-3 (+draft P3) | P2 | n/a (no P0/P1) |
| _Other (cross-cutting)_ | C-OT-1 … C-OT-2 | P1 | Yes — CONFIRMED |

Every required tension has **≥1 entry**. The draft register confirmed all six tensions are present in recon; this register verifies and elevates the high-severity rows.

---

## 3. Mongo-only tension

The evidence plane and the production ingest path are hard-bound to MongoDB and bypass the canonical, engine-neutral contracts.

| ID | Doc says / intent | Code does | Evidence (`file:line`) | Severity | Source ID(s) | Verified |
|----|-------------------|-----------|------------------------|----------|--------------|----------|
| **C-MO-1** | Vault is engine-neutral; schema advertises 4 engines `[mongodb,postgresql,timescaledb,influxdb]` | Production hard-fails to Mongo and forbids fallback; only the Mongo client implements `ITSSDVaultClient` | `afi-config/schemas/vault.schema.json:13-22` (engine enum) vs `afi-infra/src/tssd/TSSDVaultClient.ts:200` ("AFI_TSSD_MONGODB_URI is required in production. Falling back to in-memory is not allowed."); reactor side `afi-reactor/src/services/tssdVaultService.ts:4-17` (Mongo-only, `AFI_MONGO_URI` required) | P1 | `draft:52`, `draft:84` | **CONFIRMED (P1→P1)** |
| **C-MO-2** | "Same codex+config+data ⇒ same outputs" — replay/determinism is normative | Canonical `VaultedSignalRecord` pins no codex/DAG-topology/scorer version or content hash; exec IDs are random | `afi-reactor/docs/VALIDATOR_REPLAY_SPEC.v0.1.md:37` vs `afi-infra/src/tssd/types.ts:331-367` (only optional `strategyVersion?` `:112`); `afi-reactor/src/dag/DAGExecutor.ts:1003` (`exec-${Date.now()}-${Math.random()...}`) | P1 | `theme:A-normative-surface#3`, `theme:D-evidence-vault#0`, `draft:53` | **CONFIRMED (P1→P1)** |
| **C-MO-3** | Canonical lifecycle `RAW→…→REPLAYED` is normative law | The `afi-config` schema library has no enumerated `stage` field — only a boolean index hint; the enum lives only in a reference repo | `afi-config/schemas/vault.schema.json:95-98` (boolean `stageIndex` hint) vs `afi-infra/src/tssd/types.ts:8-15` (the only enum) | P1 | `theme:A-normative-surface#0`, `draft:13` | **CONFIRMED (P1→P1)** |
| **C-MO-4** | Five planes must not be collapsed; commitment + analytics planes are protocol surface | Canonical schema library contains no on-chain commitment schema and no analytics schema (2 of 5 planes unrepresented) | only `afi-config/schemas/validatorConfig.schema.json:82-87` (`coordinatorAddress`/`chainId`); `rg -nwi -c "kafka\|warehouse\|snowflake\|redshift\|datalake" afi-config/schemas` → 0; `rg -nc "EmissionsMinted\|mintForSignal\|AFISignalReceipt\|contentHash" afi-config/schemas` → 0 | P1 | `theme:A-normative-surface#4`, `draft:14` | **CONFIRMED (P1→P1)** |
| **C-MO-5** | Gateway is client-only: "No direct DB access — all AFI data access via AFI HTTP/WS APIs" | Production ingest constructs a Mongo-backed vault client and upserts directly | `afi-gateway/AGENTS.md:89` vs `afi-gateway/src/http/app.ts:133-134` (`const vault = vaultFactory(tenantId); await vault.upsert(parsed.record);`) | P1 | `draft:42` | **CONFIRMED (P1→P1)** |
| **C-MO-6** | Ingest boundary is the canonical USS v1.1 / CPJ v0.1 dialect | Gateway validates only 4 identity fields and upserts a `VaultedSignalRecord` shape — no USS/CPJ validation; reactor enforces AJV separately | `afi-gateway/src/http/app.ts:26-27` (`required = ["signalId","epochId","market","timeframe"]`), `:44`/`:51` pass-through, `:134` upsert vs `afi-reactor/src/server.ts:211` (`validateUsignalV11`) | P1 | `theme:A-normative-surface#1`, `theme:I-sdks-gateway#0`, `draft:43` | **CONFIRMED (P1→P1)** |
| **C-MO-7** | Two disjoint public ingest surfaces; no single canonical public protocol API | Gateway `/api/v1/signals` (presence-check + Mongo write) vs reactor `/api/webhooks/tradingview` + `/api/ingest/cpj` (AJV USS/CPJ) | `afi-gateway/src/http/app.ts:123,134` vs `afi-reactor/src/server.ts:159,290` (validation `:211,:314,:356`) | P1 | `theme:I-sdks-gateway#1` | **CONFIRMED (P1→P1)** |
| **C-MO-8** | Vault finality / immutability is **absolute**; history cannot be rewritten | The only canonical writer's upsert does `deleteOne`+`insertOne` (destructive overwrite-in-place) | `afi-config/docs/REGISTRIES_AND_REPUTATION.v0.1.md:111` vs `afi-infra/src/tssd/MongoTSSDVaultClient.ts:150` (`updatedAt`), `:157` (`deleteOne`), `:160` (`insertOne`) | P1 | `theme:A-normative-surface#2` | **CONFIRMED (P1→P1)** |
| **C-MO-9** | Reactor scoring output is part of the canonical evidence record (`stages.scored`) | Reactor writes a divergent `ReactorScoredSignalDocument` to a separate collection (`reactor_scored_signals_v1`); canonical `stages.scored` never populated | `afi-reactor/src/services/tssdVaultService.ts:6,59` + `afi-reactor/src/types/ReactorScoredSignalV1.ts:67` vs `afi-infra/src/tssd/types.ts:331` | P1 | `theme:D-evidence-vault#1` | **CONFIRMED (P1→P1)** |
| **C-MO-10** | Public/proprietary surfaces are separated (publicSurface vs proprietaryDetail) | Separation is structural only — `proprietaryDetail` is stored plaintext in the same doc and returned by every read (no projection, no access control) | `afi-infra/src/tssd/MongoTSSDVaultClient.ts:278-281` (spreads whole record), `:163-191` (reads, no projection), `afi-infra/src/tssd/TSSDVaultClient.ts:88` ("No persistence, encryption, or access control") | P1 | `theme:D-evidence-vault#2` | **CONFIRMED (P1→P1)** |

**Lower-severity Mongo-only rows (from draft, P2/P3):** schema descriptions hard-bind generic schemas to org repos (`draft:16`); dual USS canon v1 vs v1.1 without supersession (`draft:19`, `afi-config/schemas/usignal/v1/index.schema.json:207-209` vs `.../v1_1/index.schema.json:235-239`); gateway vault hardcoded to Mongo (`draft:44`); tenant scope mutates signal identity (`draft:45`, `afi-infra/src/tssd/TenantScopedTSSDVaultClient.ts:30-37`); ops declares Mongo a REQUIRED dependency (`draft:71`/`draft:72`); labs models TSSD as Mongo-only timeseries (`draft:58`).

---

## 4. reactor-only tension

`afi-reactor` is the reference orchestrator, but it (and the docs pointing at it) is presented as protocol law.

| ID | Doc says / intent | Code does | Evidence (`file:line`) | Severity | Source ID(s) | Verified |
|----|-------------------|-----------|------------------------|----------|--------------|----------|
| **C-RO-1** | Scoring-DAG plane is pluggable: "any conforming orchestrator" (afi-reactor, custom DAG) | Reactor self-declares as THE "ONLY orchestrator" and "the DAG is law"; ad-hoc flows are "anti-patterns" | `afi-reactor/README.md:137`, `afi-reactor/AGENTS.md:3`, `afi-reactor/docs/AFI_ORCHESTRATOR_DOCTRINE.md:38-40` vs `AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md:53,68` | P1 | `theme:E-scoring-dag#1`, `draft:83` | **CONFIRMED (P1→P1)** |
| **C-RO-2** | `dag.codex.json` is the "canonical orchestrator config" | The "canonical" codex DAG still lists nodes the runtime Froggy pipeline explicitly marks REMOVED | `afi-reactor/config/dag.codex.json:100,113,156,173` + `afi-reactor/README.md:122` vs `afi-reactor/src/config/froggyPipeline.ts:90-94` ("REMOVED STAGES") | P1 | `theme:E-scoring-dag#0` | **CONFIRMED (P1→P1)** |

**Lower-severity reactor-only rows (from draft, P2/P3):** charter hard-pins reactor as THE orchestrator (`draft:15`); afi-core runtime overview calls reactor "the canonical orchestrator" (`draft:23`); docs Orchestrator Doctrine "Status: Authoritative" (`draft:29`); internal doc-hierarchy conflict, no doc names the portable spec canonical (`draft:34`); plugins hardcode reactor/core/eliza as runtime targets (`draft:74`); ops/tiny-brains present reactor as THE engine (`draft:73`/`draft:97`).

---

## 5. BASE-ledger tension

The on-chain commitment plane records a breadcrumb, not a verifiable commitment.

| ID | Doc says / intent | Code does | Evidence (`file:line`) | Severity | Source ID(s) | Verified |
|----|-------------------|-----------|------------------------|----------|--------------|----------|
| **C-BL-1** | On-chain artifacts link to off-chain evidence via `signalId`, epoch, and content hashes (North Star rule 4); BASE is a replayable commitment ledger | The only on-chain mint payload (`MintRequest`) carries no content/payload hash or ruleset version; `signalId`/`epoch` are emitted in logs only | `afi-token/src/AFIMintCoordinator.sol:19-26` (struct) + `:85` (emit) vs `AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md` §3.4; `rg -nwi -c "contentHash\|payloadHash\|merkle\|rulesetVersion" afi-token/src` → 0 | P1 | `theme:C-onchain-anchor#0` | **CONFIRMED (P1→P1)** |
| **C-BL-2** | A third party can verify mint legitimacy from chain data | Mint is gated only by `onlyRole(EMISSIONS_ROLE)` + the 86B cap; no scoring/finality is enforced on-chain, and Pattern A grants admin+emissions to one Treasury Safe | `afi-token/src/AFIToken.sol:92` (+ cap `:97`); `afi-token/script/DeployAFITokenMainnet.s.sol:62-63` | P1 | `theme:C-onchain-anchor#1` | **CONFIRMED (P1→P1)** |
| **C-BL-3** | Emissions schedule/epoch caps/scores govern minting | On-chain enforces no per-epoch schedule, cap, or score — only `EMISSIONS_ROLE` + the 86B `TOTAL_SUPPLY_CAP` | `afi-token/src/AFIToken.sol:92`, `:97`; `afi-token/script/DeployAFITokenMainnet.s.sol:62-63` | P1 | `theme:G-emissions-mint#3` | **CONFIRMED (P1→P1)** |

**Lower-severity BASE-ledger rows (from draft, P2/P3/Info):** afi-mint contracts are empty stubs presented as a mint engine (`draft:68`, `afi-mint/contracts/MintManager.sol:4-5`); governance repo described as "on-chain governance contracts" but contains none (`draft:47`); off-chain emissions schedule presented as "canonical" vs on-chain cap-only (`draft:62`/`draft:63`); ElizaOS framed as runtime target (`draft:24`); mint exists only as mock in labs (`draft:61`).

---

## 6. econ-splits tension

| ID | Doc says / intent | Code does | Evidence (`file:line`) | Severity | Source ID(s) | Verified |
|----|-------------------|-----------|------------------------|----------|--------------|----------|
| **C-ES-1** | Emissions are split across roles (producers 0.55 / enrichment 0.25 / validators 0.10 / public_goods 0.10) | On-chain mint is single-beneficiary per signal; the multi-role gauge/split model exists only in the `afi-econ` research kit, which itself disclaims production/contract use | `afi-token/src/AFIMintCoordinator.sol:19-26`, `:76` (`token.mintEmissions(req.beneficiary, req.tokenAmount)`) vs `afi-econ/params/gauge_v0.yaml:5-8`; `afi-econ/README.md:24-26` ("Do NOT use for … Smart contract configuration") | P1 | `theme:G-emissions-mint#4` | **CONFIRMED (P1→P1)** |

**Lower-severity econ-splits rows (from draft, Info):** reputation/merit (BenchKit) blended directly into allocation weights (`draft:36`, `afi-econ/src/afi_econ_kit/gauge.py:159-175`); single-beneficiary mint model, no econ splits (`draft:69`).

---

## 7. mint-model tension

The implemented emissions/mint path diverges from the documented mint model.

| ID | Doc says / intent | Code does | Evidence (`file:line`) | Severity | Source ID(s) | Verified |
|----|-------------------|-----------|------------------------|----------|--------------|----------|
| **C-MM-1** | Emissions schedule is the single canonical `afi-math` module | `afi-mint` inlines (copy-pastes) the schedule "to avoid circular dependency", duplicating the 86B cap constant — silent drift in the replay-critical path | `afi-mint/src/adapters/EmissionsMintDataProvider.ts:19` (comment), `:51` (`cap: 86_000_000_000n`) vs `afi-math/src/emissions/emissionsSchedule.ts:60` | P1 | `theme:G-emissions-mint#0` | **CONFIRMED (P1→P1)** |
| **C-MM-2** | Mint amount follows the goldpaper formula `ΔAFI = clamp(B(t)·Q·N·R·E_epoch, …)` | Implemented path is proportional epoch-budget allocation; the documented `B(t)=8` constant is set but unused in the amount path | `afi-mint/src/adapters/EmissionsMintDataProvider.ts:11` (docstring) vs `:277-281` (proportional), `:202` (`baseMultiplier: 8.0`, unused) | P1 | `theme:G-emissions-mint#1` | **CONFIRMED (P1→P1)** |
| **C-MM-3** | Mint is deterministic; reputation/governance "must not override" scoring or finality | A successful Snapshot challenge flips the mint/reject decision, and the amount is scaled by an unpinned `reputationWeight` R and a governance `epochPulseFactor` — neither anchored in the receipt | `afi-mint/src/orchestrator/SignalStateManager.ts:284-286` + `afi-mint/src/adapters/EmissionsMintDataProvider.ts:272-273,281`; receipt surfaces `afi-token/src/AFISignalReceipt.sol:15`, `afi-token/src/AFIMintCoordinator.sol:19-26` carry no such field | P1 | `theme:G-emissions-mint#2`, `theme:H-governance#1`, `draft:66` | **CONFIRMED (P1→P1)** |
| **C-MM-4** | A single canonical signal-validator state machine | Two divergent state machines: the Zod schema and the TS `VALID_TRANSITIONS` map enumerate disjoint state sets | `afi-mint/schemas/SignalValidatorState.schema.ts:13-20` vs `afi-mint/src/orchestrator/SignalStateManager.ts:42-52` | P1 | `draft:65` | **CONFIRMED (P1→P1)** |

**Lower-severity mint-model rows (from draft, P2/P3):** non-deterministic constructs in the mint path (`draft:67`, `afi-mint/src/adapters/EmissionsMintDataProvider.ts:284`); local SignalSchema diverges from USS v1.1 (`draft:25`/`draft:101`); off-chain `mint_receipt_schema.json` diverges from on-chain `MintRequest` (`afi-mint/codex/mint_receipt_schema.json:6-13`); decentralization claims vs single-Safe role concentration (`draft:100`).

---

## 8. stale-arch-docs tension

| ID | Doc says / intent | Code does / reality | Evidence (`file:line`) | Severity | Verified |
|----|-------------------|---------------------|------------------------|----------|----------|
| **C-SD-1** | afi-token is a Hardhat/Sepolia repo whose coordinator is `src/AFICoordinator.sol` | Repo is Foundry/Base; the coordinator is `src/AFIMintCoordinator.sol`; `AFICoordinator.sol` does not exist | `afi-token/.droid.json:3-4` + `afi-token/.afi-codex.json:8` vs `afi-token/src/AFIMintCoordinator.sol:1`; `rg AFICoordinator afi-token/src` → 0 | P3 | n/a (P3) |
| **C-SD-2** | Core topology wires `afi-pipeline` (DAG engine) | Those repos do not exist locally (workspace = 28 `afi-*` + `.github` + `afi-xerc20`); names persist in current docs | `afi-docs/AFI_Repository_Map.md:24,54,168`; archived in `.github/profile/README.md:73-74`; flagged by North Star `AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md:181` | P3 | n/a (P3) |
| **C-SD-3** | afi-docs hub presents a single authoritative architecture | README/AGENTS/ARCHITECTURE_STATUS/Doctrine each self-declare authority; none names the portable spec as canonical top; reference docs are un-bannered | `afi-docs/ARCHITECTURE_STATUS.md:4`, `afi-docs/AFI_ORCHESTRATOR_DOCTRINE.md:5,290`, `afi-docs/AGENTS.md:4,25` vs `afi-docs/specs/AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md:7` | P2 | n/a (P2) |

**Additional stale-arch-docs rows (from draft, P3):** org map labels reactor as THE orchestrator (`draft:1`); stale/archived repo names in org map (`draft:2`); stale .aider config impersonating afi-core (`draft:10`); stale consumer repo names in afi-math codex (`draft:64`); onboarding mis-tags archived repos as live (`draft:79`). No P0/P1 sits under this tension, so no verified-status column applies.

---

## 9. Other (cross-cutting P0/P1)

Two verified P0/P1 contradictions do not map to a single tension; they are recorded here so every P0/P1 source carries a verified status.

| ID | Doc says / intent | Code does | Evidence (`file:line`) | Severity | Source ID(s) | Verified |
|----|-------------------|-----------|------------------------|----------|--------------|----------|
| **C-OT-1** | CI validates the source-of-truth schemas on every PR ("Validate configs" step) | The step runs `npm run validate:config --if-present`, but the package defines `validate` (not `validate:config`); `--if-present` silently skips it — schema validation never runs in CI | `afi-config/.github/workflows/ci.yml:21-22` vs `afi-config/package.json:13` | P1 | `draft:18` | **CONFIRMED (P1→P1)** |
| **C-OT-2** | "Validator certification moved to an external certification layer" (not the reactor's job) | No external-validator service, endpoint, or interop schema exists; only doc comments reference the moved-away layer and an INTERNAL `validatorConfig.schema.json`; the portable spec's promised third-party Replay Contract is undelivered | `afi-gateway/src/afiClient.ts:46`, `afi-reactor/src/config/froggyPipeline.ts:93`, `afi-reactor/src/types/ReactorScoredSignalV1.ts:8`; `rg -ni "external certification layer\|certification service\|certificationEndpoint" afi-gateway/src afi-reactor/src afi-config/schemas` → 4 doc-comment hits, 0 services | P1 | `theme:I-sdks-gateway#2` | **CONFIRMED (P1→P1)** |

---

## 10. Consolidated P0/P1 verified-status ledger

All P0/P1 contradictions cited in this register, mapped to their `themes/verified.json` source IDs. The Phase-3 gate reports **33/33 covered, all `confirmed=true`, zero severity changes**. Collapsed rows (§1) list every corroborating source ID.

| Register ID | Tension | Source ID(s) in `verified.json` | Original → Revised | Verified |
|-------------|---------|----------------------------------|--------------------|----------|
| C-MO-1 | Mongo-only | `draft:52`; `draft:84` | P1 → P1 | CONFIRMED |
| C-MO-2 | Mongo-only | `theme:A-normative-surface#3`; `theme:D-evidence-vault#0`; `draft:53` | P1 → P1 | CONFIRMED |
| C-MO-3 | Mongo-only | `theme:A-normative-surface#0`; `draft:13` | P1 → P1 | CONFIRMED |
| C-MO-4 | Mongo-only | `theme:A-normative-surface#4`; `draft:14` | P1 → P1 | CONFIRMED |
| C-MO-5 | Mongo-only | `draft:42` | P1 → P1 | CONFIRMED |
| C-MO-6 | Mongo-only | `theme:A-normative-surface#1`; `theme:I-sdks-gateway#0`; `draft:43` | P1 → P1 | CONFIRMED |
| C-MO-7 | Mongo-only | `theme:I-sdks-gateway#1` | P1 → P1 | CONFIRMED |
| C-MO-8 | Mongo-only | `theme:A-normative-surface#2` | P1 → P1 | CONFIRMED |
| C-MO-9 | Mongo-only | `theme:D-evidence-vault#1` | P1 → P1 | CONFIRMED |
| C-MO-10 | Mongo-only | `theme:D-evidence-vault#2` | P1 → P1 | CONFIRMED |
| C-RO-1 | reactor-only | `theme:E-scoring-dag#1`; `draft:83` | P1 → P1 | CONFIRMED |
| C-RO-2 | reactor-only | `theme:E-scoring-dag#0` | P1 → P1 | CONFIRMED |
| C-BL-1 | BASE-ledger | `theme:C-onchain-anchor#0` | P1 → P1 | CONFIRMED |
| C-BL-2 | BASE-ledger | `theme:C-onchain-anchor#1` | P1 → P1 | CONFIRMED |
| C-BL-3 | BASE-ledger | `theme:G-emissions-mint#3` | P1 → P1 | CONFIRMED |
| C-ES-1 | econ-splits | `theme:G-emissions-mint#4` | P1 → P1 | CONFIRMED |
| C-MM-1 | mint-model | `theme:G-emissions-mint#0` | P1 → P1 | CONFIRMED |
| C-MM-2 | mint-model | `theme:G-emissions-mint#1` | P1 → P1 | CONFIRMED |
| C-MM-3 | mint-model | `theme:G-emissions-mint#2`; `theme:H-governance#1`; `draft:66` | P1 → P1 | CONFIRMED |
| C-MM-4 | mint-model | `draft:65` | P1 → P1 | CONFIRMED |
| C-OT-1 | other | `draft:18` | P1 → P1 | CONFIRMED |
| C-OT-2 | other | `theme:I-sdks-gateway#2` | P1 → P1 | CONFIRMED |

**Source-coverage check:** the 23 rows above collapse the 33 verified P0/P1 sources. Theme sources (22): `A#0–#4`, `C#0–#1`, `D#0–#2`, `E#0–#1`, `G#0–#4`, `H#1`, `I#0–#3`. Draft sources (11): `draft:13,14,18,42,43,52,53,65,66,83,84`. Every source appears exactly once across the register (collapsed rows carry the duplicates per §1).

---

## 11. Recommendations (carry-forward)

1. **Decouple the evidence plane from Mongo (Mongo-only).** Document `ITSSDVaultClient` as the normative contract with Mongo as one reference adapter; add a non-Mongo adapter stub or an explicit "Postgres/Timescale/Influx are protocol-valid" note (C-MO-1). Route gateway ingest through USS/CPJ validation and the engine selector, and reconcile the two public ingest surfaces into one canonical API (C-MO-6, C-MO-7).
2. **Make replay-pinning and lifecycle normative (Mongo-only / mint-model).** Add record-level `codexVersion`/`configSnapshotId`/`dagTopologyHash`/`payloadHash` to `VaultedSignalRecord`, an enumerated `stage` field to `afi-config`, and deterministic execution IDs in the reference DAG (C-MO-2, C-MO-3). Enforce vault append-only immutability (C-MO-8).
3. **Reframe reactor as the reference orchestrator (reactor-only).** Change README/Doctrine language from "ONLY orchestrator / DAG is law" to "reference orchestrator for the reference spine"; reconcile `dag.codex.json` with the runtime pipeline (C-RO-1, C-RO-2).
4. **Anchor a verifiable commitment (BASE-ledger).** Add `contentHash`/`rulesetVersion`/score axes to the on-chain `MintRequest`/receipt so a third party can verify scoring legitimacy without trusting the role holder (C-BL-1, C-BL-2, C-BL-3).
5. **Reconcile the mint model and splits (mint-model / econ-splits).** Import the `afi-math` schedule instead of inlining it, align the documented goldpaper formula with the implemented allocation, pin reputation/epochPulse in the receipt, unify the validator-state machines (C-MM-1…C-MM-4), and document whether multi-role gauge splits are intended protocol or research-only (C-ES-1).
6. **Fix the CI gate and define the external-validator surface (other).** Correct `validate:config` → `validate` so schema validation actually runs (C-OT-1); deliver the promised third-party certification/Replay Contract surface or remove the "moved to external layer" claims (C-OT-2).
7. **Sweep stale docs/metadata (stale-arch-docs).** Correct afi-token toolchain/entrypoint metadata, purge `afi-pipeline` from live topology docs, and add a doc-hierarchy banner naming the portable spec as canonical (C-SD-1…C-SD-3).

---

*Backlink:* [`AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md`](../../AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md) · *Generated by the report-synthesizer worker from all 10 themes, `themes/verified.json`, and the promoted `drafts/AFI_CONTRADICTION_REGISTER.draft.md`.*
