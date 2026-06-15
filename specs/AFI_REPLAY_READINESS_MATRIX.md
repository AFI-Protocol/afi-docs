# AFI Replay Readiness Matrix

**Phase 4 synthesis report — AFI Portable Protocol Audit**
**Inputs:** themes A (normative surface), D (evidence vault), E (scoring/DAG), C (on-chain anchor) + `themes/verified.json`
**Status:** Staged in `afi-docs/specs/audit/final/`. Read-only forensic synthesis; no protocol code modified.

This report answers Core Question **D15** — *"Replay readiness: can each stage be reconstructed from stored artifacts?"* — against the canonical lifecycle spine defined by the North Star, [`AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md`](../../AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md) §5: **RAW → ENRICHED → ANALYZED → SCORED → MINTED → REPLAYED**. For each lifecycle stage it states **what is stored**, **where it is stored** (which repo/store), and **whether it is replayable** from those stored artifacts.

All paths are relative to `/home/user/AFI-Protocol/`. P0/P1 items carry a **Verified** status drawn from `themes/verified.json` (Phase 3 adversarial re-confirmation); see §5.

---

## Related reports (siblings)

This matrix is one of six cross-linked Phase-4 reports. All link back to [`AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md`](../../AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md):

- `AFI_PROTOCOL_SURFACE_AUDIT.md` — master report (exec summary, 31-repo table, findings by severity, roadmap).
- `AFI_NORMATIVE_REGISTER.md` — every normative schema/invariant/contract with `file:line`, incl. stated-but-unenforced invariants.
- `AFI_REFERENCE_IMPL_MAP.md` — per-repo classification (normative vs reference vs research vs stale) and reference-spine segments.
- `AFI_CONTRADICTION_REGISTER.md` — all six doc/code tensions with verified status.
- `AFI_ONCHAIN_ANCHOR_GAP_ANALYSIS.md` — every relevant Solidity event/struct/field/role; current vs intended anchor.

---

## 1. Scope & method

The lifecycle is a **normative concept** but it is not machine-enforceable from the canonical schema library: the only enumerated `SignalLifecycleStage = RAW|ENRICHED|ANALYZED|SCORED|MINTED|REPLAYED` lives in a *reference* repo (`afi-infra/src/tssd/types.ts:10-16`), and the canonical `afi-config` vault schema exposes only a boolean `stageIndex` hint, not an enumerated `stage` field (`afi-config/schemas/vault.schema.json:93-98`). So an external stack cannot validate lifecycle conformance from the source of truth — this is the framing constraint for every row below (theme A, **VAL-THEME-A**; verified `theme:A-normative-surface#0`, P1, confirmed).

The canonical replayable artifact is the **`VaultedSignalRecord`** (Evidence plane), defined with one optional snapshot per stage at `afi-infra/src/tssd/types.ts:331`, stages map `:336-351`. The matrix evaluates replay against the three normative determinism invariants in `afi-reactor/docs/VALIDATOR_REPLAY_SPEC.v0.1.md:35-41` ("Same codex version + same config + same data snapshot → same validator outputs"; Isolation; Traceability).

**Cross-cutting blocker (applies to every stage).** The canonical record pins **no determinism metadata** — no codex version, DAG-topology hash, plugin/scorer version, or payload/content hash at the record level (only an optional `analystScore.strategyVersion` at `afi-infra/src/tssd/types.ts:112`). A stored record therefore cannot be bound to the exact code that produced it (theme A/D; verified `theme:D-evidence-vault#0` and `theme:A-normative-surface#3`, both P1, confirmed). Compounding this, the reference orchestrator is itself non-deterministic: `DAGExecutor.generateExecutionId` uses `Date.now()+Math.random()` (`afi-reactor/src/dag/DAGExecutor.ts:1002-1003`) and same-level nodes run via `Promise.all` (`afi-reactor/src/services/pipelineRunner.ts:448`).

**Replayable rating legend:**
- **No** — the stage is not written by any production code path, and/or cannot be deterministically reconstructed from stored artifacts.
- **Partial** — some stored artifact exists, but in a divergent/log-only store or without the version-pinning needed for deterministic reproduction.
- **Yes** — the stage is written to the canonical record and is deterministically reproducible from stored artifacts. *(No stage currently meets this bar.)*

---

## 2. Replay readiness matrix (one row per lifecycle stage)

| Stage | Stored — what | Stored — where (repo / store) | Replayable from stored artifacts? |
|-------|---------------|-------------------------------|-----------------------------------|
| **RAW** | `RawSignalSnapshot` (`source`/`triggerSummary`, **optional** `payloadHash`) — `afi-infra/src/tssd/types.ts:45-58`. In production only the `identity` + caller-supplied `stages` (default `{}`) are written, i.e. an effectively RAW-only ingest. | **Mongo `afi_tssd.tssd_signals`** via the `afi-gateway` ingest route `POST /api/v1/signals` (`afi-gateway/src/http/app.ts:134`), wired TenantScoped→Mongo by `afi-gateway/src/services/vaultFactory.ts:18-34`. Record shape defined in `afi-infra`. | **No.** `payloadHash` is optional and uncomputed and the raw payload body is not persisted (`afi-gateway/src/http/app.ts:33-58`), so enrichment cannot be re-derived from RAW. The boundary also performs only a 4-field presence check, never USS/CPJ validation (verified `theme:A-normative-surface#1`, P1, confirmed). |
| **ENRICHED** | `EnrichmentSnapshot` — `indicators`/`patterns`/`sentiment` as free-form `Record<string,…>`, **no enrichment-engine version** — `afi-infra/src/tssd/types.ts:60-79`. | **Defined-but-unwritten** in the canonical record: no code populates `stages.enriched`. The reference transforms live in `afi-reactor` (`afi-reactor/src/enrichment/technicalIndicators.ts:2-5`) but their output is not persisted into `VaultedSignalRecord`. | **No (record unpopulated).** Technical/pattern enrichment is deterministic, but the sentiment/news branch calls live external APIs (Coinalyze, NewsData.io) and is non-deterministic (`afi-reactor/src/config/froggyPipeline.ts:120-126`), and no enrichment-engine version is stored. Not reconstructable from canonical artifacts. |
| **ANALYZED** | `AnalysisSnapshot` — narrative text / regime tags — `afi-infra/src/tssd/types.ts:81-91`. | **Defined-but-unwritten**: no code populates `stages.analyzed`. Type owned by `afi-infra`. | **No.** Narrative/free-form output with no stored input or model version; not deterministically reproducible. |
| **SCORED** | `ScoreSnapshot.analystScore` — the canonical UWR score — `afi-infra/src/tssd/types.ts:167-185`. The scoring math is `afi-core` `computeUwrScore` (`afi-core/validators/UniversalWeightingRule.ts:78-106`). | **Divergent store, not the canonical record.** The reactor writes a different type, `ReactorScoredSignalDocument`, into a separate Reactor-owned collection `reactor_scored_signals_v1` (`afi-reactor/src/services/tssdVaultService.ts:6,59,104`); `VaultedSignalRecord.stages.scored` is never populated. | **Partial.** The UWR transform is a pure deterministic weighted average, **but** its default config is an unpinned placeholder (`uwr-default-stub`, all weights 0.25, `afi-core/validators/UniversalWeightingRule.ts:42-52`), the canonical record pins no scorer/codex/DAG version, and the score lives in a parallel store — so a canonical-history re-score is impossible (verified `theme:D-evidence-vault#1`, P1, confirmed; `theme:A-normative-surface#3`, P1, confirmed). |
| **MINTED** | `MintSnapshot` (`txHash`/`tokenAddress`/`chainId`) — `afi-infra/src/tssd/types.ts:187-204`. On-chain: `MintCoordinated(signalId, epochId, beneficiary, tokenAmount, receiptAmount)` (`afi-token/src/AFIMintCoordinator.sol:38-44`), plus `EmissionsMinted`/`ReceiptMinted`. | **On-chain BASE** (`afi-token` contracts) as **event logs only** — `signalId`/`epoch`/`extraData` are emitted, never written to contract storage (`afi-token/src/AFIMintCoordinator.sol:85`, struct `:19-26`). The minted stage is **not** written back to the canonical `VaultedSignalRecord`. | **Partial (log-only / no evidence binding).** A third party can confirm an authorized role minted within the 86B cap (`afi-token/src/AFIToken.sol:35,97`), but **no content/payload hash binds the receipt to off-chain evidence** (verified `theme:C-onchain-anchor#0`, P1, confirmed) and mint legitimacy is gated only by `EMISSIONS_ROLE` (verified `theme:C-onchain-anchor#1`, P1, confirmed). Provenance is recoverable only via an event indexer, not from contract state or the vault. |
| **REPLAYED** | `OutcomeSnapshot` (the REPLAYED stage) — `afi-infra/src/tssd/types.ts:249-261`. | **Nowhere.** No code populates `stages.replayed`; `replaySignalsFromTssd` is a v0.1 read-only stub (`afi-infra/src/tssd/TSSDReplayRunner.ts:40-103`). The replay invariants/`ReplaySession` are conceptual only (`afi-reactor/docs/VALIDATOR_REPLAY_SPEC.v0.1.md:67`). | **No.** The replay runner does no re-scoring — it only checks presence of `stages.scored` and writes nothing (`afi-infra/src/tssd/TSSDReplayRunner.ts:82-90`); bulk filters and audit writes are TODO (`:51-52`). Deterministic re-execution is design-only. |

---

## 3. Per-stage detail

### RAW — partially written, not replayable
The only production writer of the canonical record is the external `afi-gateway` ingest route, which persists a RAW-only record straight into Mongo (`afi-gateway/src/http/app.ts:134`; theme D answer D2). Because the raw payload body is not stored and `payloadHash` is never computed, downstream enrichment cannot be re-derived — the RAW stage is an anchor in name only (theme D finding #6, Info; theme D answer D5). The same route is also the normative-dialect bypass: it never validates USS v1.1 / CPJ v0.1 (verified `theme:A-normative-surface#1`, P1, confirmed), so even the stored RAW shape is not guaranteed to be a conformant canonical signal.

### ENRICHED / ANALYZED — defined-but-unwritten
Both stages have typed snapshot interfaces on `VaultedSignalRecord` but **no code populates them** (theme A answer A4; theme D answer D5). The replay-critical, deterministic transforms (OHLCV technical indicators, `afi-reactor/src/enrichment/technicalIndicators.ts:2-5`) exist but their output is never serialized into the canonical record, while the sentiment/news enrichment branch is operational-only / non-deterministic (`afi-reactor/src/config/froggyPipeline.ts:120-126`; theme E answer E2). With no stored enrichment artifact and no engine version, neither stage is reconstructable.

### SCORED — written to a parallel store, not the canonical lifecycle
The canonical scorer is `afi-core` `computeUwrScore` (theme E answer E3), but the reactor persists its result as a divergent `ReactorScoredSignalDocument` in `reactor_scored_signals_v1`, explicitly isolated from the afi-infra TSSD vault (`afi-reactor/src/services/tssdVaultService.ts:6`). Thus the Evidence-plane `stages.scored` is never populated (verified `theme:D-evidence-vault#1`, P1, confirmed). Even within the parallel store, the score is not reproducible across stacks because the default UWR weights are an unpinned `uwr-default-stub` placeholder and the record carries no scorer/codex/DAG-topology version (verified `theme:A-normative-surface#3` and `theme:D-evidence-vault#0`, both P1, confirmed). The two divergent DAG definitions (runtime Froggy pipeline vs the "canonical" `dag.codex.json`, which still lists REMOVED nodes) further undermine any claim of a single replayable topology (verified `theme:E-scoring-dag#0`, P1, confirmed).

### MINTED — on-chain breadcrumb, not bound to evidence, not echoed to the vault
The mint emits `MintCoordinated` with `signalId`/`epochId`/`beneficiary`/amounts (`afi-token/src/AFIMintCoordinator.sol:38-44`), but these are log topics only — `signalId`/`epoch`/`extraData` are never persisted to contract storage (`afi-token/src/AFIMintCoordinator.sol:85`; theme C answer C4). No content/payload hash or ruleset version anchors the receipt to off-chain evidence (verified `theme:C-onchain-anchor#0`, P1, confirmed), and mint legitimacy is gated solely by `EMISSIONS_ROLE` held by a single Treasury Safe in the mainnet deploy (verified `theme:C-onchain-anchor#1`, P1, confirmed; `afi-token/script/DeployAFITokenMainnet.s.sol:62-63`). No code writes the minted stage back into `VaultedSignalRecord`, so the canonical lifecycle never records the on-chain outcome. The one strong, independently verifiable guarantee is the immutable 86B `TOTAL_SUPPLY_CAP` (`afi-token/src/AFIToken.sol:35,97-98`). See `AFI_ONCHAIN_ANCHOR_GAP_ANALYSIS.md` for the full enumeration.

### REPLAYED — design-only
`OutcomeSnapshot` is never populated by code; `TSSDReplayRunner` is a v0.1 stub that reads one signal, checks only for the presence of `stages.scored`, performs no actual scoring, and writes no audit record (`afi-infra/src/tssd/TSSDReplayRunner.ts:40-103`, esp. `:51-52`, `:82-90`; theme D finding #4, P2). The normative `ReplaySession` (codexVersion / configSnapshotId / dataSnapshotRef) is described as conceptual and "SHOULD capture" only, with no JSON Schema (`afi-reactor/docs/VALIDATOR_REPLAY_SPEC.v0.1.md:67`; theme A answer A5). Challenge/regression replay over canonical history is therefore not possible today.

---

## 4. End-to-end verdict

| Property | State | Evidence |
|----------|-------|----------|
| Lifecycle stages **defined** | All 6 (typed snapshots on the canonical record) | `afi-infra/src/tssd/types.ts:10-16,336-351` |
| Lifecycle stages **written by production code** | Only RAW (gateway, partial) + SCORED (divergent store) | `afi-gateway/src/http/app.ts:134`; `afi-reactor/src/services/tssdVaultService.ts:104` |
| Stages **deterministically replayable** from canonical artifacts | **0 of 6** | record pins no version/hash — `afi-infra/src/tssd/types.ts:331-362`; replay runner is a stub — `afi-infra/src/tssd/TSSDReplayRunner.ts:40-103` |
| Lifecycle **machine-enforceable** from canonical schema | No (only an `afi-infra` reference enum) | `afi-config/schemas/vault.schema.json:93-98` |

**Bottom line:** the Evidence plane defines a complete, replay-shaped record, but in practice it is write-mostly (RAW ingest) with scoring diverted to a parallel store and minting recorded only as an on-chain log breadcrumb. Because no stage pins the transform set that produced it, **no lifecycle stage is reconstructable as a deterministic, challenge-ready replay from stored artifacts today**. The minimal unlock is record-level determinism pinning (`codexVersion`, `dagTopologyHash`, plugin/scorer/validator versions, `payloadHash`) plus a real replay engine and a canonical `stages.scored` writer — tracked in `AFI_NORMATIVE_REGISTER.md` and `AFI_CONTRADICTION_REGISTER.md`.

---

## 5. P0/P1 items cited — verified status

All statuses are drawn from `themes/verified.json` (Phase 3 adversarial re-confirmation; `revised_severity` shown).

| Source (finding id) | Title (abbrev.) | Sev. | Verified |
|---------------------|-----------------|------|----------|
| `theme:A-normative-surface#0` | Lifecycle normative but no machine-enforceable `stage` field in `afi-config` | P1 | ✅ confirmed |
| `theme:A-normative-surface#1` | Gateway ingest bypasses canonical USS/CPJ dialect | P1 | ✅ confirmed |
| `theme:A-normative-surface#3` | Determinism/replay unenforced at record level (no codex/topology/hash) | P1 | ✅ confirmed |
| `theme:D-evidence-vault#0` | `VaultedSignalRecord` pins no version/content-hash → not deterministic/challenge-ready | P1 | ✅ confirmed |
| `theme:D-evidence-vault#1` | Reactor scoring bypasses canonical vault (divergent `reactor_scored_signals_v1`) | P1 | ✅ confirmed |
| `theme:E-scoring-dag#0` | Two divergent DAG definitions; codex DAG lists REMOVED nodes | P1 | ✅ confirmed |
| `theme:C-onchain-anchor#0` | No content/payload hash anchored on-chain (receipt↔evidence binding absent) | P1 | ✅ confirmed |
| `theme:C-onchain-anchor#1` | Mint gated only by `EMISSIONS_ROLE`; no on-chain scoring/finality | P1 | ✅ confirmed |

Supporting P2/Info observations cited above (RAW `payloadHash` uncomputed — theme D #6; `TSSDReplayRunner` stub — theme D #4; unpinned `uwr-default-stub` — theme E #3; DAG orchestration non-determinism — theme E #5) are not in the P0/P1 verification set but are sourced to live `file:line` evidence in their themes.

---

*Generated for the AFI Portable Protocol Audit (Phases 2–4). Read-only synthesis of `themes/{A-normative-surface,D-evidence-vault,E-scoring-dag,C-onchain-anchor}.json` and `themes/verified.json`. Backlink: [`AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md`](../../AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md).*
