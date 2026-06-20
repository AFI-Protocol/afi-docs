# AFI Protocol Surface Audit — Master Report

**Phase 4 synthesis report (master) — AFI Portable Protocol Audit**
**Inputs:** all 10 themes (A–J) + `themes/verified.json` (Phase 3 adversarial re-confirmation) + the persisted recon corpus (`audit/recon/AFI_RECON_CORPUS.json`, 31 records) + `drafts/AFI_CONTRADICTION_REGISTER.draft.md` + the five sibling Phase-4 reports.
**Status:** Staged in `afi-docs/specs/audit/final/`. Read-only forensic synthesis; no protocol code, schema, or contract was modified.

This is the master deliverable the North Star calls for — *"a master report with executive summary, findings, and severity"* ([`AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md`](../../AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md) §6). It consolidates the other five reports into a single decision surface: an alignment scorecard, the top-10 solidification blockers, the top-10 quick wins, the consolidated repo classification, per-repo subsections, all P0/P1 findings by severity with their Phase-3 verified status, a Phase 0–4 solidification roadmap, open questions for human review, and a Definition-of-Done checklist with cross-links.

All paths are relative to `/home/user/AFI-Protocol/`. Every P0/P1 item carries the **Verified** status drawn from `themes/verified.json` (Phase 3 re-opened all 33 P0/P1 sources; the gate reports **33/33 covered, all `confirmed=true`, zero refutations, zero severity changes**).

---

## Related reports (siblings)

This master report is one of six cross-linked Phase-4 reports. All link back to [`AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md`](../../AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md):

- [`AFI_NORMATIVE_REGISTER.md`](./AFI_NORMATIVE_REGISTER.md) — every normative schema/invariant/contract with `file:line`; stated-but-unenforced invariants.
- [`AFI_REFERENCE_IMPL_MAP.md`](./AFI_REFERENCE_IMPL_MAP.md) — all 31 repos classified; reference-spine segments.
- [`AFI_CONTRADICTION_REGISTER.md`](./AFI_CONTRADICTION_REGISTER.md) — all six doc/code tensions with verified status.
- [`AFI_REPLAY_READINESS_MATRIX.md`](./AFI_REPLAY_READINESS_MATRIX.md) — per-lifecycle-stage replay readiness (RAW→ENRICHED→ANALYZED→SCORED→MINTED→REPLAYED).
- [`AFI_ONCHAIN_ANCHOR_GAP_ANALYSIS.md`](./AFI_ONCHAIN_ANCHOR_GAP_ANALYSIS.md) — every relevant Solidity event/struct/field/role; current vs intended anchor.

---

## 1. Executive summary

AFI's stated direction is a **portable protocol** — HTTP-like, with a thin normative surface (schemas, lifecycle semantics, determinism, on-chain anchors) above pluggable implementations (any database, any DAG framework, any analytics warehouse) ([`AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md`](../../AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md) §1, §3). The audit's headline conclusion: **the protocol surface is real and partly encoded, but across the corpus reference implementations (MongoDB, `afi-reactor`) are wired and documented as protocol law, two of the five planes have no normative schema at all, no lifecycle stage is deterministically replayable today, and the on-chain commitment plus third-party-validator interoperability promise is essentially undelivered.** The single most common failure mode — verified across nine repos — is *one storage/orchestration choice presented as the protocol*.

### 1.1 Alignment scorecard

Portable-protocol alignment is **Partial / fragmented** — an overall **≈32/100**, computed as the mean of five per-plane scores (0–10) against the North Star's five-plane model (§3.2) and §3.4 conformance rules. The corpus is honest where it is concrete (the 86B supply cap, the canonical record shape, deterministic UWR math) and weakest exactly where third parties need it (commitment anchoring, replay pinning, an external-validator surface).

| Plane (North Star §3.2) | Score /10 | One-line basis (evidence) |
|-------------------------|-----------|---------------------------|
| **Ingest boundary** | 4 | USS v1.1 / CPJ dialect defined (`afi-config/schemas/usignal/v1_1/index.schema.json:235-239`) and AJV-enforced in reactor (`afi-reactor/src/server.ts:211`), but the production gateway bypasses it with a 4-field presence check (`afi-gateway/src/http/app.ts:26-27,134`) → two divergent ingest contracts. |
| **Scoring DAG** | 4 | Reference Froggy DAG + deterministic UWR exist (`afi-core/validators/UniversalWeightingRule.ts:78-106`), but reactor is documented as the "ONLY orchestrator / DAG is law" (`afi-reactor/README.md:137`), the "canonical" `dag.codex.json` lists REMOVED nodes (`afi-reactor/src/config/froggyPipeline.ts:90-94`), and exec IDs are random (`afi-reactor/src/dag/DAGExecutor.ts:1002-1003`). |
| **Evidence** | 4 | Canonical `VaultedSignalRecord` defined (`afi-infra/src/tssd/types.ts:331`) but Mongo-only in production (`afi-infra/src/tssd/TSSDVaultClient.ts:200`), pins no replay metadata, and scoring is diverted to a parallel store (`afi-reactor/src/services/tssdVaultService.ts:6`). |
| **Commitment (BASE)** | 3 | Contracts exist and the 86B cap is strongly enforced (`afi-token/src/AFIToken.sol:35,97`), but no content/score/ruleset hash is anchored (`afi-token/src/AFIMintCoordinator.sol:19-26`) and mint is gated only by `EMISSIONS_ROLE` held by one Treasury Safe (`afi-token/script/DeployAFITokenMainnet.s.sol:62-63`). |
| **Market / analytics** | 1 | No analytics-plane schema anywhere in the canonical library; `rg -nwi -c "kafka\|warehouse\|snowflake\|redshift\|datalake" afi-config/schemas` → 0 hits. The evidence store is Mongo TSSD; no warehouse plane is planned for the reference implementation. |
| **Overall** | **≈3.2/10 (≈32/100)** | 2 of 5 planes lack any normative schema; **0 of 6** lifecycle stages are deterministically replayable; reference choices documented as law. |

**Severity ledger (verified):** 33 P0/P1 sources verified in Phase 3 — **22 theme findings + 11 draft rows**, all `confirmed=true`, all retained at **P1**, zero refutations. No finding was assigned P0 at the artifact-evidence level. This master report **escalates two P1 items to P0/blocker rank for solidification prioritization** (see §1.4) under the hard-requirement reading of the protocol's third-party-validator promise; the Phase-3 *evidence* severity in `themes/verified.json` is immutable and remains P1/CONFIRMED for both.

### 1.2 What works (keep)

- The immutable **86B `TOTAL_SUPPLY_CAP`** is the one strong, independently chain-verifiable guarantee (`afi-token/src/AFIToken.sol:35,97-98`).
- A complete, replay-*shaped* canonical record exists with one typed snapshot per lifecycle stage (`afi-infra/src/tssd/types.ts:336-351`).
- The scoring math (UWR) is a pure deterministic weighted average (`afi-core/validators/UniversalWeightingRule.ts:78-106`), and an engine-neutral vault seam (`ITSSDVaultClient`) is the correct extension point (`afi-infra/src/tssd/TSSDVaultClient.ts:36-68`).

### 1.3 Top-10 solidification blockers

Ranked by impact on the portable-protocol promise. Each carries its Phase-3 verified evidence severity; **B1 and B2 are escalated to P0/blocker rank** (§1.4). Full enumeration in [`AFI_CONTRADICTION_REGISTER.md`](./AFI_CONTRADICTION_REGISTER.md) §10 (register IDs in brackets).

| # | Blocker | Evidence (`file:line`) | Source ID(s) | Verified (evidence sev.) | Blocker rank |
|---|---------|------------------------|--------------|--------------------------|--------------|
| **B1** | **No external-validator surface** — "validator certification moved to an external layer" but no service, endpoint, or interop schema exists; the North Star's promised third-party Replay Contract is undelivered. [C-OT-2] | `afi-gateway/src/afiClient.ts:46`; `afi-reactor/src/config/froggyPipeline.ts:93`; `rg -ni "external certification layer\|certification service\|certificationEndpoint" afi-gateway/src afi-reactor/src afi-config/schemas` → 4 doc-comments, 0 services | `theme:I-sdks-gateway#2` | CONFIRMED P1 | **P0 (escalated)** |
| **B2** | **No third-party on-chain verifiability** — no content/payload/ruleset hash on `MintRequest`, and mint legitimacy is gated only by `EMISSIONS_ROLE`; a third party must fully trust the role holder. [C-BL-1, C-BL-2] | `afi-token/src/AFIMintCoordinator.sol:19-26`; `afi-token/src/AFIToken.sol:92`; `afi-token/script/DeployAFITokenMainnet.s.sol:62-63` | `theme:C-onchain-anchor#0`, `theme:C-onchain-anchor#1` | CONFIRMED P1 | **P0 (escalated)** |
| **B3** | **2 of 5 planes have no normative schema** — Commitment and Market/analytics planes are unrepresented in `afi-config`. [C-MO-4] | `afi-config/schemas/validatorConfig.schema.json:82-87` (only on-chain ref); `rg -nc "EmissionsMinted\|mintForSignal\|AFISignalReceipt\|contentHash" afi-config/schemas` → 0 | `theme:A-normative-surface#4`, `draft:14` | CONFIRMED P1 | P1 |
| **B4** | **No record-level replay pinning** — `VaultedSignalRecord` pins no codex/DAG-topology/scorer version or content hash → 0 of 6 stages deterministically replayable. [C-MO-2] | `afi-infra/src/tssd/types.ts:331-367` (only optional `strategyVersion?` `:112`); `afi-reactor/src/dag/DAGExecutor.ts:1003` | `theme:A-normative-surface#3`, `theme:D-evidence-vault#0`, `draft:53` | CONFIRMED P1 | P1 |
| **B5** | **Lifecycle is normative law but has no machine-enforceable stage field** in `afi-config` — the enum lives only in a reference repo. [C-MO-3] | `afi-config/schemas/vault.schema.json:95-98` (boolean hint) vs `afi-infra/src/tssd/types.ts:8-15` | `theme:A-normative-surface#0`, `draft:13` | CONFIRMED P1 | P1 |
| **B6** | **Production ingest bypasses the canonical USS/CPJ dialect** — gateway validates 4 identity fields then upserts; reactor enforces AJV separately. [C-MO-6] | `afi-gateway/src/http/app.ts:26-27,134` vs `afi-reactor/src/server.ts:211` | `theme:A-normative-surface#1`, `theme:I-sdks-gateway#0`, `draft:43` | CONFIRMED P1 | P1 |
| **B7** | **Evidence plane is Mongo-only** — schema advertises 4 engines but only `mongodb` is implemented and production hard-fails without it. [C-MO-1] | `afi-config/schemas/vault.schema.json:13-22` vs `afi-infra/src/tssd/TSSDVaultClient.ts:200`; `afi-reactor/src/services/tssdVaultService.ts:4-17` | `draft:52`, `draft:84` | CONFIRMED P1 | P1 |
| **B8** | **Scoring bypasses the canonical vault** — reactor writes a divergent `ReactorScoredSignalDocument` to `reactor_scored_signals_v1`; `stages.scored` is never populated. [C-MO-9] | `afi-reactor/src/services/tssdVaultService.ts:6,59` + `afi-reactor/src/types/ReactorScoredSignalV1.ts:67` vs `afi-infra/src/tssd/types.ts:331` | `theme:D-evidence-vault#1` | CONFIRMED P1 | P1 |
| **B9** | **Governance/reputation can override the deterministic mint** — a successful Snapshot challenge flips mint/reject and the amount is scaled by an unpinned `reputationWeight`/`epochPulseFactor`, none anchored in the receipt. [C-MM-3] | `afi-mint/src/orchestrator/SignalStateManager.ts:284-286`; `afi-mint/src/adapters/EmissionsMintDataProvider.ts:272-273,281` | `theme:G-emissions-mint#2`, `theme:H-governance#1`, `draft:66` | CONFIRMED P1 | P1 |
| **B10** | **Vault immutability is asserted "absolute" but unenforced** — the only canonical writer does `deleteOne`+`insertOne` (destructive overwrite). [C-MO-8] | `afi-config/docs/REGISTRIES_AND_REPUTATION.v0.1.md:111` vs `afi-infra/src/tssd/MongoTSSDVaultClient.ts:150,157,160` | `theme:A-normative-surface#2` | CONFIRMED P1 | P1 |

*Runners-up (also P1/CONFIRMED, just outside the top 10):* reactor self-declared as the only orchestrator [C-RO-1, `theme:E-scoring-dag#1`]; canonical emissions schedule inlined/copy-pasted into `afi-mint` [C-MM-1, `theme:G-emissions-mint#0`]; documented goldpaper mint formula ≠ implemented allocation [C-MM-2, `theme:G-emissions-mint#1`]; CI schema gate is a silent no-op [C-OT-1, `draft:18`].

### 1.4 Escalation decision — third-party-validator promise treated as a hard requirement

The North Star is unambiguous that third-party interoperability is the *defining* promise of the portable protocol, not an optional extra: the HTTP analogy frames "any conforming orchestrator" as a client (§3.3); §3.4 enumerates the rules under which "any validator or operator may erect their own database and DAG pipeline"; and §5.5 lists a **"Replay Contract — cross-repo checklist: what a third-party validator needs to reproduce a mint decision without org infra"** as an explicit solidification goal. The severity rubric defines **P0** as *"external validator cannot interoperate; normative rule violated in production path"* (`architecture.md` §9 / `AGENTS.md`).

Reading that promise as a **hard requirement**, this master report **escalates the following two confirmed-P1 findings to P0/blocker rank** for solidification prioritization:

- **B1 — `theme:I-sdks-gateway#2` (external-validator interoperability is unbuilt).** Three sites declare validator certification "moved to an external certification layer", yet no external-validator service, endpoint, or interop schema exists. The promised third-party Replay Contract is undelivered. Under the hard-requirement reading this is a textbook P0: an external validator literally *cannot interoperate* because there is no surface to integrate against. The Phase-3 verifier kept it at P1 only because, at the artifact level, it is a *missing-feature/contradiction gap* rather than a live production-path rule violation (`verified.json` note on `theme:I-sdks-gateway#2`: *"borderline P0 for third-party interop, but kept at P1"*). The master honours that evidence severity (P1/CONFIRMED is recorded unchanged) but ranks it **P0/blocker #1** because it negates the protocol's defining interoperability promise. *(If a reviewer instead treats third-party validation as aspirational for v1.0, B1 stays P1 — see Open Question Q1, §7.)*

- **B2 — `theme:C-onchain-anchor#1` (third-party on-chain verifiability).** From chain data a third party can confirm only that *an authorized role minted within the cap*; they cannot verify the mint was legitimately scored or bound to real evidence, because no content/ruleset hash is anchored (`theme:C-onchain-anchor#0`) and mint is gated solely by `EMISSIONS_ROLE`. The verifier likewise considered and declined a P0 at the evidence level (*"a conforming external validator can still interoperate; it merely cannot independently attest scoring legitimacy"*). The master escalates it to **P0/blocker rank** because third-party verifiability is the entire point of the Commitment plane (§3.5); the evidence severity remains **P1/CONFIRMED**.

This is the only place the master's *blocker rank* diverges from the *verified evidence severity*; every other item's rank equals its verified P1. No entry in `themes/verified.json` was altered.

### 1.5 Top-10 quick wins

Low-effort, high-clarity fixes — mostly documentation, metadata, or one-line config — that immediately reduce drift without touching the production data path. None resolve a structural blocker by itself, but together they restore honest labeling and re-arm the CI gate.

| # | Quick win | Type | Evidence (`file:line`) | Closes |
|---|-----------|------|------------------------|--------|
| Q1 | Fix CI schema gate: `validate:config` → `validate` (the `--if-present` step is a silent no-op today). | 1-line CI | `afi-config/.github/workflows/ci.yml:21-22` vs `afi-config/package.json:13` | C-OT-1 (`draft:18`) |
| Q2 | Annotate the vault engine enum to state only `mongodb` is implemented today, and reframe the prod guard as "a persistent `ITSSDVaultClient` is required" (engine-agnostic). | Doc/schema note | `afi-config/schemas/vault.schema.json:14-23`; `afi-infra/src/tssd/TSSDVaultClient.ts:197-201` | C-MO-1 |
| Q3 | Add a banner to `afi-reactor` README/Doctrine: "reference orchestrator, not the only one; any conforming version-pinned DAG output is valid." | Doc | `afi-reactor/README.md:137`; `afi-reactor/docs/AFI_ORCHESTRATOR_DOCTRINE.md:38-40` | C-RO-1 |
| Q4 | Reconcile `dag.codex.json` with the runtime pipeline — delete or mark the four REMOVED nodes. | Config | `afi-reactor/config/dag.codex.json:100,113,156,173` vs `afi-reactor/src/config/froggyPipeline.ts:90-94` | C-RO-2 |
| Q6 | Add an enumerated `stage` field (`RAW…REPLAYED`) to `afi-config` vault schema instead of only a boolean index hint. | Small schema | `afi-config/schemas/vault.schema.json:95-98`; enum source `afi-infra/src/tssd/types.ts:8-15` | C-MO-3 (partial) |
| Q7 | Correct `afi-token` stale metadata: coordinator is `AFIMintCoordinator.sol` (not `AFICoordinator.sol`); toolchain is Foundry/Base (not Hardhat/Sepolia). | Metadata | `afi-token/.droid.json:3-4`; `afi-token/.afi-codex.json:8` vs `afi-token/src/AFIMintCoordinator.sol:1` | C-SD-1 |
| Q8 | Purge `afi-pipeline` from live topology docs and add a doc-hierarchy banner naming the portable spec as canonical. | Doc | `afi-docs/AFI_Repository_Map.md:24,54,168`; `afi-docs/ARCHITECTURE_STATUS.md:4` | C-SD-2, C-SD-3 |
| Q9 | Reconcile the `provenance.timestamp` mandate with USS v1.1 (which demotes it to legacy/optional). | Doc | `afi-config/docs/AFI_CONFIG_OVERVIEW.md:122` vs `afi-config/schemas/usignal/v1_1/index.schema.json:235-239` | U5 (Normative Register) |
| Q10 | Resolve the placeholder receipt URI and document the log-only provenance assumption (or persist a minimal anchor mapping). | Metadata/doc | `afi-token/script/DeployAFITokenMainnet.s.sol:103`; `afi-token/src/AFIMintCoordinator.sol:85` | C-anchor-P2a/b |

---

## 2. Scope & method

**Charter.** Solidify the portable AFI protocol along [`AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md`](../../AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md): map what is *normative* (protocol law), *reference implementation*, *aspirational*, *stale*, and what *contradicts* the portable direction, across the **28 repositories** of the AFI-Protocol org (local `afi-*`/`.github` checkouts).

**Phases.** This is a read-only forensic audit executed in four phases (Phase 1 recon was completed and persisted before this mission):

1. **Phase 1 — Recon (pre-existing).** 31 per-repo structured audits → `audit/recon/AFI_RECON_CORPUS.json` (classification, normative artifacts, 103 contradictions, all `file:line`). Not re-run; reused as a *map, not gospel* (`architecture.md` §1).
2. **Phase 2 — Themes.** 10 cross-cutting deep-dives (A–J), one per core-question group, each answering its sub-questions against live source with `file:line` evidence → `audit/themes/<key>.json`.
3. **Phase 3 — Verify.** Every P0/P1 finding (themes + draft register) adversarially re-opened and confirmed/refuted → `audit/themes/verified.json` (**33/33 covered, all confirmed**).
4. **Phase 4 — Synthesize.** Six cross-linked reports staged in `audit/final/`, then promoted to `afi-docs/specs/` (this master is one).

**Verification approach.** Findings are evidence-based: every factual claim carries a `relpath/file.ext:LINE` citation relative to `/home/user/AFI-Protocol/` (or a reproducible negative grep where the finding is an *absence*). The deterministic gate `afi-docs/specs/audit/scripts/validate_audit.py` enforces report/theme/citation integrity and resolves a random sample of citations against live files. Phase 3 re-opened each P0/P1 citation, corrected line drift, and recorded `confirmed`, `corrected_evidence`, and `revised_severity` per source. The **severity rubric** (P0 = external validator cannot interoperate / normative rule violated in production; P1 = doc/code contradiction drives wrong architecture; P2 = reference-as-law fixable by docs; P3 = stale naming; Info = observation) governs all severities below.

**Read-only boundary.** The only writable tree was `afi-docs/specs/`. No `afi-*` implementation code, schema, Solidity, config, or the recon corpus was modified.

---

## 3. Consolidated repo classification table

Reconciled against the recon corpus (`audit/recon/AFI_RECON_CORPUS.json:1`, `init.sh` reports `corpus records: 31`) and theme B; identical to the detailed table in [`AFI_REFERENCE_IMPL_MAP.md`](./AFI_REFERENCE_IMPL_MAP.md) §3. "Spine?" marks repos on the reference spine **ingest → scoring DAG → evidence vault → mint coordination → on-chain commitment**.

| # | Repo | Visibility | Classification | Spine? | Basis (`file:line` where applicable) |
|---|------|------------|----------------|--------|--------------------------------------|
| 1 | `.github` | PRIVATE | SUPPORTING | no | Org config + repo-map README only. |
| 2 | `afi-artifacts` | PUBLIC | SUPPORTING | no | Zenodo reproducibility bundle; schema *snapshots*, not canonical. |
| 3 | `afi-assets` | PRIVATE | SUPPORTING | no | Brand assets; empty `.gitkeep` placeholders. |
| 4 | `afi-benchkit` | PUBLIC | SUPPORTING | no | Validator benchmark toolkit; "Does NOT contain DAG/engine/scoring runtime". |
| 5 | `afi-cli-framework` | PRIVATE | SUPPORTING | no | Commander.js CLI scaffold; zero protocol surface. |
| 6 | `afi-config` | PUBLIC | **NORMATIVE** | anchor | Canonical schema/spec library; engine enum `afi-config/schemas/vault.schema.json:14-23`. |
| 7 | `afi-core` | PUBLIC | REFERENCE_IMPL | yes | UWR scorer / decay / novelty `afi-core/validators/UniversalWeightingRule.ts`. |
| 8 | `afi-docs` | PRIVATE | DOCS | no | Documentation hub (hosts the North Star); "NOT for code". |
| 9 | `afi-econ` | PRIVATE | RESEARCH | no | "Research-Grade / Placeholder"; gauge splits `afi-econ/README.md:24-26`. |
| 10 | `afi-factory` | PUBLIC | SUPPORTING | no | Agent-template registry; mirrors afi-config schemas. |
| 11 | `afi-gateway` | PUBLIC | REFERENCE_IMPL | **yes (ingest)** | Ingest endpoint `afi-gateway/src/http/app.ts:123`. |
| 12 | `afi-governance` | PRIVATE | REFERENCE_IMPL | no (governance plane) | Universal Proposal Signal + Snapshot/Safe execution. |
| 13 | `afi-infra` | PRIVATE | **NORMATIVE** | anchor + vault | Canonical TSSD types `afi-infra/src/tssd/types.ts:331`; `ITSSDVaultClient` `:36-68`. |
| 14 | `afi-labs` | PRIVATE | RESEARCH | no | "experimental playground… prototypes, PoCs"; Mongo-only MVP scaffolds. |
| 15 | `afi-math` | PUBLIC | SUPPORTING | no (consumed) | Deterministic math; emissions schedule `afi-math/src/emissions/emissionsSchedule.ts:60`. |
| 16 | `afi-mint` | PRIVATE | REFERENCE_IMPL | **yes (off-chain mint)** | FSM `afi-mint/src/orchestrator/MintExecutor.ts:33`. |
| 17 | `afi-ops` | PRIVATE | SUPPORTING | no | Ops/devops scaffold; bakes Mongo as required infra. |
| 18 | `afi-plugins` | PUBLIC | REFERENCE_IMPL | **yes (DAG nodes)** | Plugin registry `afi-plugins/src/types/plugin.ts:22-26`; "NOT production logic". |
| 19 | `afi-protocol` | PRIVATE | DOCS | no | Governance/onboarding meta-repo; zero code. |
| 20 | `afi-reactor` | PUBLIC | REFERENCE_IMPL | **yes (orchestrator)** | Reference Froggy DAG `afi-reactor/src/services/pipelineRunner.ts:161`; "ONLY orchestrator" `afi-reactor/README.md:137`. |
| 21 | `afi-research-site` | PRIVATE | OUT_OF_SCOPE | no | Next.js marketing site (Axleo template); "explicitly separate from the protocol stack". |
| 22 | `afi-skills` | PUBLIC | SUPPORTING | no | Versioned agent-skill library; scoped skill contract only. |
| 23 | `afi-tiny-brains` | PRIVATE | REFERENCE_IMPL | **yes (ML enrich)** | FastAPI ML microservice `afi-tiny-brains/README.md:11`. |
| 24 | `afi-token` | PRIVATE | REFERENCE_IMPL | **yes (on-chain)** | BASE contracts `afi-token/src/AFIMintCoordinator.sol:68`, `afi-token/src/AFIToken.sol:92`. |
| 25 | `afi-xerc20` | PUBLIC | OUT_OF_SCOPE | no | Vendored defi-wonderland/xERC20 fork `afi-xerc20/package.json:6`. |

**Class tallies (25 total):** NORMATIVE = 2; REFERENCE_IMPL = 8; SUPPORTING = 9; RESEARCH = 2; DOCS = 2; OUT_OF_SCOPE = 2. `2 + 8 + 9 + 2 + 2 + 2 = 25`.

---

## 4. Per-repo subsections

One subsection per repo: classification, role on/off the reference spine, and the most salient audit observation (with `file:line` where one applies). Detailed spine mapping is in [`AFI_REFERENCE_IMPL_MAP.md`](./AFI_REFERENCE_IMPL_MAP.md).

### 4.1 `afi-config` — NORMATIVE (schema anchor)
The protocol law library: USS/CPJ/vault/pipeline/plugin schemas, self-declared source of truth (`afi-config/docs/AFI_CONFIG_OVERVIEW.md:13-22`). Gaps: no enumerated lifecycle `stage` field (`afi-config/schemas/vault.schema.json:95-98`), no Commitment or analytics plane schema (B3), and the CI validation step is a silent no-op (Q1).

### 4.2 `afi-infra` — NORMATIVE (type anchor + evidence vault)
Owns the canonical `VaultedSignalRecord` and lifecycle enum (`afi-infra/src/tssd/types.ts:331`, `:8-15`) and the engine-neutral `ITSSDVaultClient` seam (`:36-68`). But production hard-fails to Mongo (`afi-infra/src/tssd/TSSDVaultClient.ts:200`), the record pins no replay metadata (B4), and `upsert` overwrites destructively (B10).

### 4.3 `afi-gateway` — REFERENCE_IMPL (ingest spine)
Production ingest `POST /api/v1/signals` (`afi-gateway/src/http/app.ts:123`). Performs only a 4-field presence check then upserts straight to Mongo (`:26-27,134`), bypassing the canonical USS/CPJ dialect (B6) and its own "no direct DB access" principle (`afi-gateway/AGENTS.md:89`).

### 4.4 `afi-reactor` — REFERENCE_IMPL (orchestrator spine)
Reference Froggy DAG (`afi-reactor/src/services/pipelineRunner.ts:161`). Self-declares as the "ONLY orchestrator / DAG is law" (`afi-reactor/README.md:137`), the "canonical" `dag.codex.json` lists REMOVED nodes (`afi-reactor/src/config/froggyPipeline.ts:90-94`), and scored output is diverted to a parallel store (B8). Exec IDs are non-deterministic (`afi-reactor/src/dag/DAGExecutor.ts:1002-1003`).

### 4.5 `afi-core` — REFERENCE_IMPL (scoring primitives)
Canonical UWR scorer, decay/novelty templates (`afi-core/validators/UniversalWeightingRule.ts:78-106`). Deterministic math, but the default weights are an unpinned `uwr-default-stub` (`:42-52`), and the reputation-non-interference rule survives only as a code comment (`:22-24`).

### 4.6 `afi-plugins` — REFERENCE_IMPL (DAG nodes)
Thin plugin/node registry consumed by reactor (`afi-plugins/src/types/plugin.ts:22-26`); self-described as "NOT production logic". Hardcodes reactor/core/eliza as runtime targets (reactor-only tension).

### 4.7 `afi-tiny-brains` — REFERENCE_IMPL (ML enrichment)
FastAPI ML microservice called by reactor for Froggy predictions (`afi-tiny-brains/README.md:11`). Operational enrichment; off the replay-critical deterministic path.

### 4.8 `afi-mint` — REFERENCE_IMPL (off-chain mint coordination)
FSM + `MintExecutor.mintForSignal` (`afi-mint/src/orchestrator/MintExecutor.ts:33,108`). Inlines the afi-math schedule (drift risk, `afi-mint/src/adapters/EmissionsMintDataProvider.ts:19,51`), implements a proportional allocation that diverges from the documented goldpaper formula (`:11` vs `:277-281`), lets governance/reputation override the mint (B9), and ships two divergent validator-state machines (`afi-mint/schemas/SignalValidatorState.schema.ts:13-20` vs `afi-mint/src/orchestrator/SignalStateManager.ts:42-52`). On-chain `contracts/*.sol` are empty stubs (`afi-mint/contracts/MintManager.sol:4-5`).

### 4.9 `afi-token` — REFERENCE_IMPL (on-chain commitment)
The entire commitment plane: `AFIToken` + `AFIMintCoordinator` + `AFISignalReceipt` (`afi-token/src/AFIToken.sol:92`, `afi-token/src/AFIMintCoordinator.sol:68`). The 86B cap is strongly enforced (`:35,97`), but `MintRequest` anchors no content/score/ruleset hash (B2) and Pattern A centralizes admin+emissions in one Treasury Safe (`afi-token/script/DeployAFITokenMainnet.s.sol:62-63`). Full enumeration in [`AFI_ONCHAIN_ANCHOR_GAP_ANALYSIS.md`](./AFI_ONCHAIN_ANCHOR_GAP_ANALYSIS.md).

### 4.10 `afi-governance` — REFERENCE_IMPL (governance plane)
Universal Proposal Signal + Snapshot/Safe execution; off the signal-data spine. Described as "on-chain governance contracts" but contains none (draft contradiction). Successful challenges feed back into the mint decision (B9).

### 4.11 `afi-math` — SUPPORTING (consumed by spine)
Pure deterministic emissions schedule, the canonical 86B three-phase model (`afi-math/src/emissions/emissionsSchedule.ts:60`). Not on-chain authoritative; copied (not imported) by afi-mint.

### 4.12 `afi-econ` — RESEARCH
Multi-role gauge/split model (`afi-econ/params/gauge_v0.yaml:5-8`) that the repo itself disclaims for production/contract use (`afi-econ/README.md:24-26`). Source of the econ-splits tension vs the single-beneficiary on-chain mint.

### 4.13 `afi-labs` — RESEARCH
Experimental playground; Mongo-only MVP scaffolds and a mock-only mint. Not protocol law.

### 4.14 `afi-benchkit` — SUPPORTING
Validator benchmark toolkit; explicitly contains no DAG/engine/scoring runtime. Merit/reputation weights here are blended into allocation in research (`afi-econ`), an Info-level coupling.

### 4.15 `afi-ops` — SUPPORTING
Ops/devops scaffold; declares Mongo a REQUIRED dependency and reactor as THE engine (reactor-only / Mongo-only tensions).

### 4.16 `afi-factory` — SUPPORTING
Phase-1 agent-template registry; mirrors afi-config schemas without defining protocol law.

### 4.17 `afi-skills` — SUPPORTING
Versioned agent-skill library + tooling; scoped skill contract only.

### 4.18 `afi-cli-framework` — SUPPORTING
Generic Commander.js CLI scaffold; zero protocol surface.

### 4.19 `afi-artifacts` — SUPPORTING
Zenodo paper reproducibility bundle; schema snapshots are point-in-time copies, not canonical.

### 4.20 `afi-assets` — SUPPORTING
Brand/design assets; directories are empty `.gitkeep` placeholders.

### 4.21 `.github` — SUPPORTING
Org-level config and the org-profile README (which still labels reactor as THE orchestrator and lists archived repos — stale-arch-docs).

### 4.22 `afi-docs` — DOCS
Documentation hub hosting the North Star itself; "NOT for code implementation" (`afi-docs/AGENTS.md`). Several docs self-declare authority without naming the portable spec as canonical (C-SD-3).

### 4.23 `afi-protocol` — DOCS
Governance/onboarding meta-repo; zero code or schemas.

### 4.24 `afi-research-site` — OUT_OF_SCOPE
Next.js marketing site (Axleo template); "explicitly separate from the AFI Network protocol stack".

### 4.25 `afi-xerc20` — OUT_OF_SCOPE
Vendored defi-wonderland/xERC20 bridge fork (`afi-xerc20/package.json:6`); not an AFI mint/receipt artifact and must not be read as the commitment layer.

---

## 5. Findings by severity with verified status

All P0/P1 findings collapse to **23 register rows over 33 verified sources** (some sources verified independently are deduplicated). Phase 3 reports **33/33 covered, all `confirmed=true`, zero refutations, zero severity changes**. Detailed evidence per row is in [`AFI_CONTRADICTION_REGISTER.md`](./AFI_CONTRADICTION_REGISTER.md) §10 and [`AFI_NORMATIVE_REGISTER.md`](./AFI_NORMATIVE_REGISTER.md) §7.

### 5.1 P0 (master blocker rank — escalated from verified P1)

| Register ID | Title | Source ID(s) | Evidence severity (verified) | Master rank |
|-------------|-------|--------------|------------------------------|-------------|
| C-OT-2 | No external-validator service/endpoint/interop schema; third-party Replay Contract undelivered | `theme:I-sdks-gateway#2` | **P1 — CONFIRMED** | **P0 / blocker** |
| C-BL-2 | Mint legitimacy gated only by `EMISSIONS_ROLE`; no third-party on-chain verifiability | `theme:C-onchain-anchor#1` | **P1 — CONFIRMED** | **P0 / blocker** |

*(Escalation rationale and the immutability of the verified P1 severity are documented in §1.4.)*

### 5.2 P1 (verified, retained at P1)

| Register ID | Tension | Source ID(s) | Original → Revised | Verified |
|-------------|---------|--------------|--------------------|----------|
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
| C-BL-3 | BASE-ledger | `theme:G-emissions-mint#3` | P1 → P1 | CONFIRMED |
| C-ES-1 | econ-splits | `theme:G-emissions-mint#4` | P1 → P1 | CONFIRMED |
| C-MM-1 | mint-model | `theme:G-emissions-mint#0` | P1 → P1 | CONFIRMED |
| C-MM-2 | mint-model | `theme:G-emissions-mint#1` | P1 → P1 | CONFIRMED |
| C-MM-3 | mint-model | `theme:G-emissions-mint#2`; `theme:H-governance#1`; `draft:66` | P1 → P1 | CONFIRMED |
| C-MM-4 | mint-model | `draft:65` | P1 → P1 | CONFIRMED |
| C-OT-1 | other | `draft:18` | P1 → P1 | CONFIRMED |

*(C-BL-1 and C-OT-2 also appear above as escalated blockers; their verified evidence severity remains P1.)*

### 5.3 P2 / P3 / Info (representative — full catalogue in the contradiction register)

- **P2 (reference-as-law, doc-fixable):** theme-B framing of Mongo-only and reactor-only as reference-as-law (`themes/B-reference-impl.json` #0–#2); honor-system reputation rule (`theme:H-governance#0`); `TSSDReplayRunner` v0.1 stub (`theme:D-evidence-vault#4`); doc-hierarchy authority conflict (C-SD-3); `signalId`/epoch log-only persistence (C-anchor-P2a).
- **P3 (stale naming):** `afi-token` toolchain/entrypoint metadata (C-SD-1); `afi-pipeline` in live topology docs (C-SD-2); theme-B stale-naming finding (`#3`).
- **Info:** 86B cap is the one strong verifiable on-chain guarantee; merit/reputation blended into research allocation weights (`draft:36`).

---

## 6. Solidification roadmap (Phases 0–4)

A staged path from the current ≈32/100 alignment to a third-party-verifiable portable protocol. Phases are ordered by dependency and risk: Phase 0 is pure hygiene (no data-path change); Phases 1–2 complete and enforce the normative surface; Phase 3 closes the on-chain anchor (escalated blocker B2); Phase 4 delivers the external-validator interoperability surface (escalated blocker B1). Maps to the North Star's six solidification goals (§5).

### Phase 0 — Doc hygiene & honest labeling *(the top-10 quick wins; days)*
Re-arm the CI schema gate (Q1), annotate the vault engine enum and prod guard (Q2), reframe reactor as the reference orchestrator (Q3), reconcile `dag.codex.json` with the runtime (Q4), correct `afi-token` metadata (Q7), purge stale repo names and add a doc-hierarchy banner naming the portable spec as canonical (Q8), reconcile the `provenance.timestamp` doc (Q9), resolve the receipt URI (Q10). **Exit:** docs no longer assert reference impls as protocol law; CI actually validates schemas.

### Phase 1 — Complete the normative surface *(weeks)*
Promote the lifecycle law into `afi-config`: add the enumerated `stage` field (Q6) and a normative `ValidatorReplaySession` schema; add the **missing-plane schemas** — a Commitment-plane receipt schema (`signalId`/epoch/amounts/beneficiary/`contentHash`/`rulesetVersion`) and at least an analytics-plane interface schema (closes B3); move the canonical `VaultedSignalRecord` shape into the normative library rather than a reference repo. **Exit:** all five planes have a normative schema; external stacks can machine-validate lifecycle/linkage from the source of truth. *(North Star goals 1, 4.)*

### Phase 2 — Determinism, replay pinning & evidence integrity *(weeks)*
Add record-level `codexVersion`/`configSnapshotId`/`dagTopologyHash`/`payloadHash` to `VaultedSignalRecord` and deterministic execution IDs/ordering in the reference DAG (closes B4); make the reactor write the canonical `stages.scored` (or declare the parallel store normative) (B8); enforce vault append-only immutability (B10); route gateway ingest through USS/CPJ validation and reconcile the two public ingest surfaces into one canonical API (B6, C-MO-7); pin reputation/`epochPulseFactor` and convert the reputation-non-interference rule into a testable guard (B9). **Exit:** every lifecycle stage is deterministically replayable from canonical artifacts. *(North Star goals 1, 5; replay readiness matrix.)*

### Phase 3 — Anchor a verifiable commitment (closes B2) *(weeks)*
Add `bytes32 contentHash` + `rulesetVersion` to `MintRequest`/receipt so each mint is cryptographically bound to its off-chain evidence and the exact emissions ruleset; persist a minimal anchor mapping (`signalId → {epoch, contentHash}`) or document log-only provenance; replace the inlined afi-math schedule with a versioned import pinned on-chain/in-receipt (C-MM-1); reconcile on-chain vs off-chain receipt dialects; decide splits-vs-single-beneficiary in the normative spec (C-ES-1). **Exit:** a third party can verify a mint's legitimacy from chain data + published rules. *(North Star goal 4; on-chain anchor gap analysis §8.)*

### Phase 4 — External-validator interoperability & the Replay Contract (closes B1) *(quarter)*
Define and publish the **third-party Replay Contract** (the cross-repo checklist of what a validator needs to reproduce a mint without org infra), deliver an external-validator service/endpoint and interop schema (the layer the code claims certification "moved to" but never built), and ship working SDKs against it. Add a conformance test kit so a stranger's stack can self-certify. **Exit:** an external validator can interoperate end-to-end — the portable-protocol promise is met. *(North Star goals 2, 5.)*

---

## 7. Open questions for human review

These require a human/architect decision before v0.1 → v1.0 promotion; several are the pivots on which severities and the roadmap depend.

- **Q1 — Is the third-party-validator promise a hard requirement for v1.0?** If yes, B1 (`theme:I-sdks-gateway#2`) and B2 (`theme:C-onchain-anchor#1`) are P0/blockers as ranked in §1.4; if it is aspirational for a later version, both stay P1. This is the single most consequential decision in the audit. *(North Star §3.4, §5.5.)*
- **Q2 — Anchor specification:** What MUST be on-chain vs hash-anchored vs off-chain? The on-chain anchor gap analysis (§4.3) proposes a three-way partition; this needs sign-off before contract changes. *(North Star §5.4 — explicitly an open question.)*
- **Q3 — Splits vs single beneficiary:** Are the `afi-econ` multi-role gauge splits intended normative protocol, or research-only? Today the contract mints to a single beneficiary (C-ES-1).
- **Q4 — Governance/reputation influence on allocation:** Should a Snapshot challenge be allowed to flip a deterministic mint/reject, and should `reputationWeight`/`epochPulseFactor` scale the amount at all? If retained, they must be pinned/anchored (B9).
- **Q5 — Persistence portability:** Is MongoDB a permanent reference default, or is a second engine adapter (Postgres/Timescale/Influx) required for v1.0 to honor the multi-engine schema (B7)?
- **Q6 — Canonical scored store:** Is the normative scored record `afi-infra`'s `stages.scored` or reactor's `reactor_scored_signals_v1`? One must be declared canonical (B8).
- **Q7 — USS versioning:** Is USS v1 deprecated/superseded by v1.1, and should the `provenance.timestamp` mandate be retired (Q9)?

---

## 8. Definition-of-Done checklist + cross-links

DoD items from `AFI_PROTOCOL_INVESTIGATION_PROMPT.md` / `AFI_AUDIT_CHECKPOINT.md`, with the report that satisfies each. *(Ticking the checkpoint's own DoD tracker is performed by the `promote-and-close` feature, not this report.)*

| DoD item | Status | Where satisfied |
|----------|--------|-----------------|
| All org repos enumerated (31) | ✅ | §3 here; [`AFI_REFERENCE_IMPL_MAP.md`](./AFI_REFERENCE_IMPL_MAP.md) §3; corpus `audit/recon/AFI_RECON_CORPUS.json:1` |
| Every repo has a classification row | ✅ | §3 + §4 (per-repo subsections); [`AFI_REFERENCE_IMPL_MAP.md`](./AFI_REFERENCE_IMPL_MAP.md) |
| All six master reports exist with cross-links | ✅ (this completes the set) | This report + the five siblings linked above |
| Contradiction register has ≥1 entry per major tension | ✅ | [`AFI_CONTRADICTION_REGISTER.md`](./AFI_CONTRADICTION_REGISTER.md) §2–§9 (all six tensions) |
| Replay readiness matrix covers all six lifecycle stages | ✅ | [`AFI_REPLAY_READINESS_MATRIX.md`](./AFI_REPLAY_READINESS_MATRIX.md) §2 (RAW→…→REPLAYED) |
| On-chain anchor gap cites every relevant Solidity event/field | ✅ | [`AFI_ONCHAIN_ANCHOR_GAP_ANALYSIS.md`](./AFI_ONCHAIN_ANCHOR_GAP_ANALYSIS.md) §2 |
| Normative register lists schemas/invariants/contracts w/ stated-but-unenforced | ✅ | [`AFI_NORMATIVE_REGISTER.md`](./AFI_NORMATIVE_REGISTER.md) §2–§5 |
| Solidification roadmap ready for human review | ✅ | §6 here (Phases 0–4) |
| Theme answers A1–J33 completed | ✅ | `audit/themes/{A..J}.json` (10 themes) |
| P0/P1 claims adversarially verified | ✅ | `audit/themes/verified.json` (33/33 confirmed) |
| Open questions surfaced for human review | ✅ | §7 here |

**Cross-links:** [`AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md`](../../AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md) (North Star) · [`AFI_NORMATIVE_REGISTER.md`](./AFI_NORMATIVE_REGISTER.md) · [`AFI_REFERENCE_IMPL_MAP.md`](./AFI_REFERENCE_IMPL_MAP.md) · [`AFI_CONTRADICTION_REGISTER.md`](./AFI_CONTRADICTION_REGISTER.md) · [`AFI_REPLAY_READINESS_MATRIX.md`](./AFI_REPLAY_READINESS_MATRIX.md) · [`AFI_ONCHAIN_ANCHOR_GAP_ANALYSIS.md`](./AFI_ONCHAIN_ANCHOR_GAP_ANALYSIS.md).

---

*Backlink:* [`AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md`](../../AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md) · *Generated by the report-synthesizer worker (master) from all 10 themes, `themes/verified.json`, the recon corpus, and the five sibling Phase-4 reports. Read-only forensic synthesis; no protocol code modified.*
