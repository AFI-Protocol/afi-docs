# AFI Contradiction Register

**Status:** DRAFT — unverified; adversarial verify required in Phase 3
**Date:** 2026-06-15
**Entries:** 103 contradictions from Phase 1 recon

Promote to [`afi-docs/specs/AFI_CONTRADICTION_REGISTER.md`](../../AFI_CONTRADICTION_REGISTER.md) after verification.

---

## Tension Coverage Check

| Tension | Covered in recon? |
|---------|-------------------|
| Mongo-only | yes |
| reactor-only | yes |
| BASE-ledger | yes |
| econ-splits | yes |
| mint-model | yes |
| stale-arch-docs | yes |

## Register

| ID | Repo | Tension | Severity | Title | Evidence | Verified? |
|----|------|---------|----------|-------|----------|-----------|
| 1 | `.github` | reactor-only | P3 | Repo map labels afi-reactor as THE orchestrator (no reference-vs-norma | `profile/README.md:12 '- **afi-reactor** – Signal DAG / orchestrator, Codex integration, replay.'` | no |
| 2 | `.github` | stale-arch-docs | P3 | Stale/archived repo names persist in the org map | `profile/README.md:73-74 '- **afi-agents** – Early CLI entry-points and manifests. / - **afi-construc` | no |
| 3 | `.github` | other | P2 | Root README advertises reusable workflows/templates that do not exist  | `README.md:21-25 lists 'validate-typescript.yml ... validate-solidity.yml ... security-scan.yml'; fin` | no |
| 4 | `afi-artifacts` | other | P3 | Repo self-description (compiled binaries/build artifacts) contradicts  | `package.json:4 "description": "AFI build artifacts and compiled outputs"; AGENTS.md:3 "It contains r` | no |
| 5 | `afi-artifacts` | Mongo-only | P2 | Ships its own snapshot copies of USS/vault/CPJ schemas separate from t | `repro/README.md:8 "schemas/ — minimal JSON Schemas for snapshots shown in Appendix A (A.1/A.2/A.3)";` | no |
| 6 | `afi-artifacts` | mint-model | P2 | Two divergent codex replay manifests; the example one is unchecksummed | `repro/codex/afi-codex.json:2-8 "epoch":"2025-08-10...","scorers":["signal-scorer@v0.3.1"] vs repro/c` | no |
| 7 | `afi-artifacts` | Mongo-only | P2 | Reproducibility/integrity guarantee covers only a subset of the bundle | `repro/SHA256SUMS:1-8 (only codex/, data/examples/{valid-proposal,vault-ready-record}, schemas/{3 jso` | no |
| 8 | `afi-artifacts` | mint-model | P3 | Determinism rule met only by a hash mock, not by pinned-transform scor | `repro/tests/mock_replay.js:17-18 "crypto.createHash('sha256').update(line + String(codex.epoch))... ` | no |
| 9 | `afi-artifacts` | Mongo-only | P3 | Inconsistent score-scale across example records (0-1 vs 0-100) | `repro/data/examples/vault-ready-record.jsonl:1 "score":{"overall":0.78,...} vs repro/data/sample_tss` | no |
| 10 | `afi-assets` | stale-arch-docs | P3 | Stale .aider config impersonates afi-core with non-existent protocol d | `/home/user/AFI-Protocol/afi-assets/.aider.conf.json:31-32 "repo_name": "afi-core", "description": "A` | no |
| 11 | `afi-benchkit` | other | P3 | Benchmark 'reputation' score risks being read as protocol-canonical sc | `src/afi_benchkit/reputation.py:65 "reputation_score = alpha * poi_score + beta * poinsight_score"; R` | no |
| 12 | `afi-benchkit` | other | Info | Hardcoded heuristic N=10 and assumed determinism=1.0/uptime=1.0 weaken | `src/afi_benchkit/reputation.py:119-120 "Could not determine exact sample size for PoInsight, using e` | no |
| 13 | `afi-config` | Mongo-only | P1 | Vault schema lacks canonical lifecycle stage enum despite stages being | `schemas/vault.schema.json:95-98 "stageIndex": {..."description": "Create index on signal stage (RAW,` | no |
| 14 | `afi-config` | Mongo-only | P1 | No analytics/market plane and no on-chain commitment schema in the can | `grep BigQuery/kafka/warehouse across repo: 0 hits; grep mintForSignal/coordinateMint/EmissionsMinted` | no |
| 15 | `afi-config` | reactor-only | P2 | Charter hard-pins afi-reactor as THE orchestrator (reference-impl-as-l | `codex/governance/droids/AFI_DROID_CHARTER.v0.1.md:117 "**`afi-reactor`** is the orchestrator" vs doc` | no |
| 16 | `afi-config` | Mongo-only | P2 | Schema descriptions hard-bind generic schemas to specific org repos | `schemas/pipeline.schema.json:5 "...pipeline configurations in afi-reactor"; schemas/vault.schema.jso` | no |
| 17 | `afi-config` | stale-arch-docs | P2 | Orphaned .afi-codex.schema.json contradicts the actual codex metadata  | `.afi-codex.schema.json:31-34 "required": ["persona","abilities"] vs tests/schema-validation.test.ts:` | no |
| 18 | `afi-config` | other | P1 | CI never runs schema validation (script name mismatch) | `.github/workflows/ci.yml:21-22 "run: npm run validate:config --if-present // echo \"No validation sc` | no |
| 19 | `afi-config` | Mongo-only | P2 | Dual USS canon (v1 vs v1.1) without a normative supersession statement | `schemas/usignal/v1/index.schema.json:207-209 provenance required:[timestamp] vs schemas/usignal/v1_1` | no |
| 20 | `afi-config` | other | P3 | Duplicated, divergent USS schemas in afi-uss-pr-v2p1/ staging director | `afi-uss-pr-v2p1/schema/usignal/v1/core.schema.json:2 "$schema":"https://json-schema.org/draft/2020-1` | no |
| 21 | `afi-construct` | stale-arch-docs | P3 | Divergent local blueprint.schema.json competes with normative afi-conf | `blueprint.schema.json:1-3 "$schema: draft-07 ... title: AFI Construct Blueprint Schema ... required:` | no |
| 22 | `afi-construct` | Mongo-only | P3 | Stale repo-lineage and 'afi-core' production naming | `README.md "afi-labs (private experiments) ➜ afi-construct (public simulation) ➜ afi-core (production` | no |
| 23 | `afi-core` | reactor-only | P2 | Reactor presented as THE canonical orchestrator (reference spine asser | `docs/AFI_CORE_RUNTIME_OVERVIEW.md:39 'AFI-Reactor (already hardened) is the **canonical orchestrator` | no |
| 24 | `afi-core` | BASE-ledger | P3 | ElizaOS framed as the runtime/soft-fork target (specific stack implied | `docs/AFI_CORE_RUNTIME_OVERVIEW.md:10 'runtime layer powered by ElizaOS (or a future soft fork thereo` | no |
| 25 | `afi-core` | mint-model | P2 | Local SignalSchema diverges from normative USS v1.1 surface | `schemas/universal_signal_schema.ts:3-39 (no macro/provenance/epoch fields; content z.string().min(1)` | no |
| 26 | `afi-core` | Mongo-only | P3 | AGENTS.md documents many npm scripts that do not exist (replay/determi | `AGENTS.md:36-63 'npm run validate-all ... npm run simulate-signal ... npm run replay-vault # Replay ` | no |
| 27 | `afi-core` | reactor-only | P3 | Conflicting dependency declarations across the two codex manifests | `.afi-codex:8 'dependsOn: [afi-reactor, afi-token]'; .afi-codex.json:18-21 'dependsOn: [afi-config, a` | no |
| 28 | `afi-core` | mint-model | P3 | Stale entrypoint and module references in metadata/docs | `.afi-codex.json:5-8 'entrypoints: validators/PoIValidator.ts'; droids/00_repo_orientation.md:39-52 l` | no |
| 29 | `afi-docs` | reactor-only | P2 | Orchestrator Doctrine declares reactor THE protocol orchestrator and i | `AFI_ORCHESTRATOR_DOCTRINE.md:5,11,38-40,290 'Status: Authoritative'; '#1 afi-reactor is the orchestr` | no |
| 30 | `afi-docs` | Mongo-only | P2 | Pipeline audit presents MongoDB TSSD vault as the canonical/working ev | `AFI_PIPELINE_AUDIT_REPORT.md:16,41,118 '✅ MongoDB TSSD vault persistence'; 'afi-infra — TSSD vault (` | no |
| 31 | `afi-docs` | stale-arch-docs | P3 | AFI_Repository_Map.md uses stale/nonexistent repo names (afi-pipeline, | `AFI_Repository_Map.md:24-32,54-61,168,170 'afi-pipeline ... DAG execution engine'; 'afi-agents ... a` | no |
| 32 | `afi-docs` | reactor-only | P3 | ARCHITECTURE_STATUS.md claims reactor is the single source of truth fo | `ARCHITECTURE_STATUS.md:4,10 'Single source of truth for how AFI orchestration is implemented today.'` | no |
| 33 | `afi-docs` | Mongo-only | P3 | Market/analytics plane (BigQuery/Kafka/warehouses/Mage) entirely absen | `grep bigquery/kafka/warehouse/mage across *.md = 0 hits outside specs/; AFI_Full_Architecture.md & A` | no |
| 34 | `afi-docs` | reactor-only | P2 | Internal doc-hierarchy conflict: README/AGENTS/Architecture-Status/Doc | `README.md:14 'AGENTS.md wins'; AGENTS.md:25 'Codex + AOS are truth sources'; ARCHITECTURE_STATUS.md:` | no |
| 35 | `afi-econ` | BASE-ledger | Info | Repo models multi-role econ splits (gauge) while reference mint path i | `params/gauge_v0.yaml:4-11 'weights: producers: 0.55 enrichment: 0.25 validators: 0.10 public_goods: ` | no |
| 36 | `afi-econ` | econ-splits | Info | Reputation/merit (BenchKit) blended directly into allocation weights | `src/afi_econ_kit/gauge.py:159-175 'if bench_merit and bench_merit_weights: ... raw_allocation[role] ` | no |
| 37 | `afi-econ` | other | Info | Local determinism/provenance mechanism parallel to VALIDATOR_REPLAY_SP | `src/afi_econ_kit/schemas.py:97-104 'class ProvenanceStamp(BaseModel): version... git_sha... config_h` | no |
| 38 | `afi-econ` | other | P2 | out_audit/AUDIT.md asserts 'WHITEPAPER READY' while README says models | `out_audit/AUDIT.md:29 'WHITEPAPER READY: All critical checks pass...suitable for academic publicatio` | no |
| 39 | `afi-factory` | other | P2 | Duplicated/derived type defs risk drift from canonical afi-config sche | `schemas/index.ts:7-9 'These interfaces are strongly typed and compatible with the JSON schemas defin` | no |
| 40 | `afi-factory` | other | P3 | Analyst topology hardcoded without pinned plugin/validator versions fo | `template_registry.ts:26-74 analystId 'froggy-analyst-node' version '1.0.0' with enrichmentNodes plug` | no |
| 41 | `afi-factory` | stale-arch-docs | P3 | Stale/inconsistent paths between docs, codex, and actual layout | `AGENTS.md:45-48 'templates/ ... agents/ ... factory/'; .afi-codex.json:6 'src/template_registry.ts';` | no |
| 42 | `afi-gateway` | Mongo-only | P1 | Stated client-only / no-direct-DB principle contradicted by direct Mon | `src/http/app.ts:133-136 'const vault = vaultFactory(tenantId); await vault.upsert(parsed.record);' +` | no |
| 43 | `afi-gateway` | Mongo-only | P1 | Ingest boundary does not validate against canonical USS/CPJ dialect | `src/http/app.ts:26-30 'const required = ["signalId","epochId","market","timeframe"]; const missing =` | no |
| 44 | `afi-gateway` | Mongo-only | P2 | Vault layer hardcoded to MongoDB only, ignoring multi-engine vault.sch | `src/services/vaultFactory.ts:19-21 'dbName: process.env.AFI_TSSD_DB_NAME // "afi_tssd", collectionNa` | no |
| 45 | `afi-gateway` | Mongo-only | P2 | Tenant scope mutates canonical signal identity (analystId overwritten) | `afi-infra/src/tssd/TenantScopedTSSDVaultClient.ts:30-37 'identity: { ...record.identity, analystId: ` | no |
| 46 | `afi-gateway` | Mongo-only | P3 | Large cross-repo TSSD readiness report lives in gateway and is dated/M | `TSSD_VAULT_READINESS_REPORT.md:26 'no production MongoDB implementation exists yet' vs afi-infra/src` | no |
| 47 | `afi-governance` | BASE-ledger | P2 | Repo described as 'on-chain governance contracts' but contains zero co | `AGENTS.md:3 'afi-governance contains on-chain governance contracts and Epoch Pulse coordination logi` | no |
| 48 | `afi-governance` | BASE-ledger | P2 | 'Universal Proposal Signal' reuses canonical 'signal' vocabulary for a | `schemas/UniversalProposalSignal.schema.json:5 '"signal_type": "governance_proposal"'; README.md:38-4` | no |
| 49 | `afi-governance` | other | P2 | Canonical schema file is not valid JSON (un-parseable as a schema) | `schemas/UniversalProposalSignal.schema.json:1-2 '// Mirrors specs/... // Used internally'; specs/uni` | no |
| 50 | `afi-governance` | BASE-ledger | P3 | Governance/staking gated on mint supply implies tight coupling to comm | `config/config_staking.ts:4 'export const MIN_SUPPLY_FOR_STAKING = 1_000_000_000;'; README.md:26-31 '` | no |
| 51 | `afi-governance` | stale-arch-docs | P3 | docs/governance_links.md points to files that do not exist at HEAD (st | `docs/governance_links.md:8-31 links to docs/constitution.md, tokenomics/distribution_model.ts, org/b` | no |
| 52 | `afi-infra` | Mongo-only | P1 | TSSD vault production path is Mongo-only; multi-engine vault is absent | `src/tssd/TSSDVaultClient.ts:199 "AFI_TSSD_MONGODB_URI is required in production. Falling back to in-` | no |
| 53 | `afi-infra` | Mongo-only | P1 | Canonical vault type omits pinned-version / determinism replay fields  | `src/tssd/types.ts:331-367 (VaultedSignalRecord has identity/stages/publicSurface/proprietaryDetail/t` | no |
| 54 | `afi-infra` | Mongo-only | P2 | Spec claims on-chain receipt carries baseScore+confidence, richer than | `docs/TSSD_VAULT_SPEC.md:103 "Receipt (on-chain): Minimal public fields (signalId, epochId, baseScore` | no |
| 55 | `afi-infra` | Mongo-only | P2 | .afi-codex.json labels the vault CLIENT entrypoint as the canonical va | `.afi-codex.json:12-15 "module": "afi-infra/tssd-vault", "role": "canonical_signal_vault", "entryPoin` | no |
| 56 | `afi-infra` | reactor-only | P3 | DAG determinism test points to afi-reactor doctrine as 'real' orchestr | `tests/dag.deterministic.test.ts:15 "Real DAG orchestration lives in afi-reactor (see AFI_ORCHESTRATO` | no |
| 57 | `afi-infra` | Mongo-only | P3 | Stale AGENTS.md / codex references to deleted dirs and a non-existent  | `AGENTS.md:3 "This repo is template/stub oriented, not production runtime."; AGENTS.md:58 references ` | no |
| 58 | `afi-labs` | Mongo-only | P3 | TSSD modeled as MongoDB-only timeseries store (collapses evidence plan | `docs/specs/vercel_mongo_scaffold.md:14-23 'MongoDB Timeseries Setup: db.createCollection("tssd", { t` | no |
| 59 | `afi-labs` | Mongo-only | P3 | No canonical USS/CPJ/vault/pipeline schemas; signal schema reduced to  | `docs/sections/section-4-universal-signal-schema.md:1-2 'Section 4: Universal Signal Schema / Formal ` | no |
| 60 | `afi-labs` | other | Info | Replay/determinism advertised as capability but engine is an empty pla | `pipelines/replay/replay_engine.py:1 '# Placeholder content for replay_engine.py'; code-sandbox/core/` | no |
| 61 | `afi-labs` | BASE-ledger | Info | Mint/on-chain commitment exists only as mock/placeholder, no receipt o | `docs/plans/afi_mvp_what_to_stub_vs_build.md:13 '$AFI minting logic -> use mocked console log or toke` | no |
| 62 | `afi-math` | BASE-ledger | P2 | Emissions cap/curve hardcoded despite 'no policy constants' rule | `AGENTS.md:92 'No hardcoded policy constants: AFI-specific parameters (e.g., decay rates, discount ra` | no |
| 63 | `afi-math` | BASE-ledger | P2 | Off-chain emissions schedule presented as 'canonical' vs on-chain emis | `src/emissions/emissionsSchedule.ts:215-217 'export function getRemainingSupply(schedule, alreadyMint` | no |
| 64 | `afi-math` | mint-model | P3 | Stale / inconsistent consumer repo names | `.afi-codex.json:21-28 'consumers: [afi-engine, afi-token-finalized, afi-config, afi-plugins, afi-rea` | no |
| 65 | `afi-mint` | reactor-only | P1 | Two divergent SignalValidatorState state machines (Zod schema vs TS ty | `schemas/SignalValidatorState.schema.ts:13-20 z.enum(['pending','decay_pass','challenge_open','voting` | no |
| 66 | `afi-mint` | mint-model | P1 | Reputation/governance can override deterministic mint outcome and amou | `src/orchestrator/SignalStateManager.ts:284-286 'if (challengeSucceeded) { finalDecision = state.vali` | no |
| 67 | `afi-mint` | mint-model | P2 | Non-deterministic constructs in a replay-critical mint path | `src/adapters/EmissionsMintDataProvider.ts:284 'BigInt(Math.floor(adjustedAmount * 10 ** this.config.` | no |
| 68 | `afi-mint` | BASE-ledger | P2 | On-chain commitment presented as full mint engine but contracts are em | `contracts/MintManager.sol:4-5 'contract MintManager { // Stub for minting logic }'; contracts/Thresh` | no |
| 69 | `afi-mint` | econ-splits | P3 | Single-beneficiary mint model, no econ splits / gauge | `src/orchestrator/MintExecutor.ts:19-27 'interface MintRequest { beneficiary: string; tokenAmount: bi` | no |
| 70 | `afi-mint` | mint-model | P3 | Stale root-level placeholder files and broken CLI references | `cli/simulate-mint.ts:2-3 'import { runMintFlow } from \'../mint/mint\'; runMintFlow();' vs mint/mint` | no |
| 71 | `afi-ops` | Mongo-only | P2 | MongoDB declared REQUIRED external dependency in codex metadata | `.afi-codex.json:95-99 '"name": "mongodb", "description": "MongoDB database", "defaultPort": 27017, "` | no |
| 72 | `afi-ops` | Mongo-only | P2 | TSSD Vault backend restricted to memory/mongodb only | `configs/env.template:40-44 'TSSD_VAULT_BACKEND=memory ... MongoDB collection for T.S.S.D. Vault (if ` | no |
| 73 | `afi-ops` | reactor-only | P3 | afi-reactor presented as THE DAG orchestrator across ops docs | `README.md:41 '- afi-reactor - DAG orchestrator'; scripts/run-local-deploy.sh:126 'Would start afi-re` | no |
| 74 | `afi-plugins` | reactor-only | P2 | Reactor/core/eliza hardcoded as canonical runtime targets (reactor-as- | `src/types/plugin.ts:22-26 'export type RuntimeTarget = / "afi-reactor" / "afi-core" / "eliza-tool" /` | no |
| 75 | `afi-plugins` | Mongo-only | P2 | Validator replay coupled to a specific store (T.S.S.D. Vault / afi-inf | `src/templates/validator/halfDecayReplayTemplate.ts:45 'NOTE: Integrates with T.S.S.D. Vault (afi-inf` | no |
| 76 | `afi-plugins` | other | P2 | Local PluginManifest type is disconnected from the normative plugin-ma | `src/types/plugin.ts:45-81 'export interface PluginManifest { ... configSchemaRef?: string; ... }' ; ` | no |
| 77 | `afi-plugins` | other | Info | Determinism / pinned-version / replay-reproducibility rules absent fro | `src/types/context.ts:108 'mode?: "pre-mint" / "post-mint" / "replay";' ; scorer/README.md:32 'Compos` | no |
| 78 | `afi-protocol` | reactor-only | P2 | Reactor framed as the single 'source of truth' orchestrator, not a ref | `architecture_overview.md:23 '/ **Reactor** / DAG orchestration (source of truth) / `afi-reactor` /';` | no |
| 79 | `afi-protocol` | reactor-only | P3 | Stale repo names referenced in onboarding (afi-agents, afi-labs) and d | `contributor-manifest/onboarding.md:9 '[`afi-agents`](https://github.com/AFI-Protocol/afi-agents) – a` | no |
| 80 | `afi-protocol` | other | P3 | Architecture overview references a non-existent local diagrams/ direct | `architecture_overview.md:11 '├─ diagrams/                  ← high level PNG/SVG diagrams (add as you` | no |
| 81 | `AFI-Protocol/afi-agents` | Mongo-only | P3 | Demo 'signal' shape diverges from normative USS/VaultedSignalRecord | `ui/SignalValidator.tsx:8-15 — "export type SignalData = { id: string; timestamp: string; source: str` | no |
| 82 | `AFI-Protocol/afi-agents` | stale-arch-docs | P3 | Hard-coded sibling-repo paths assume a specific monorepo/org layout | `cli/afi-cli.ts:6-8 — "import { validateCodex } from '../../afi-config/cli_utils/codex_validator'; ..` | no |
| 83 | `afi-reactor` | reactor-only | P1 | Reactor self-declares as THE single orchestrator, contradicting portab | `README.md:137 "afi-reactor is the ONLY orchestrator in AFI Protocol."; docs/AFI_ORCHESTRATOR_DOCTRIN` | no |
| 84 | `afi-reactor` | Mongo-only | P1 | Vault layer hard-bound to MongoDB; no multi-engine seam at the persist | `src/services/tssdVaultService.ts:4-22 "MongoDB persistence... AFI_MONGO_URI: MongoDB connection stri` | no |
| 85 | `afi-reactor` | other | P2 | DAG executor uses non-deterministic ordering/IDs, risking replay deter | `src/dag/DAGExecutor.ts:1002-1004 generateExecutionId uses Date.now()+Math.random; DAGExecutor.ts:716` | no |
| 86 | `afi-reactor` | reactor-only | P2 | DAG spec/codex describe an aspirational 15-node design not matched by  | `config/schema.codex.json:289-291 "additional-schema.schema.json" ... "Additional schema to reach cou` | no |
| 87 | `afi-reactor` | reactor-only | P3 | Doctrine claims 'Configuration is externalized' from afi-config but pi | `docs/AFI_ORCHESTRATOR_DOCTRINE.md:95-104 "Configuration is externalized... no hard-coded magic"; con` | no |
| 88 | `afi-sdk-python` | reactor-only | P2 | SDK targets afi-reactor as the API client surface | `README.md:11 '- Pythonic API clients for afi-reactor'` | no |
| 89 | `afi-sdk-python` | other | P3 | pyproject declares version 1.0.0 for an empty scaffold | `pyproject.toml:3 'version = "1.0.0"' vs README.md:41 '🚧 New repository created during multi-repo reo` | no |
| 90 | `afi-sdk-ts` | reactor-only | P3 | SDK narrative anchored to afi-reactor (reference impl) rather than can | `/home/user/AFI-Protocol/afi-sdk-ts/README.md:11 'Type-safe API clients for afi-reactor'` | no |
| 91 | `afi-skills` | Mongo-only | P3 | TSSD bound to a single named engine ('Time-Series Signal Database') | `skills/README.md:86 '`["tssd:read"]`: Read-only access to TSSD (Time-Series Signal Database)'` | no |
| 92 | `afi-skills` | other | P2 | Determinism declared as protocol-critical but not enforced by tooling  | `scripts/lint-skills.ts:82-84 'if (fm.determinism_required) { // TODO: Add more determinism checks (e` | no |
| 93 | `afi-skills` | other | P3 | Repo self-described as 'canonical source of truth' could be misread as | `README.md:28 '`afi-skills` is the **canonical source of truth** for AFI agent capabilities.' ; docs/` | no |
| 94 | `afi-starters` | Mongo-only | P2 | Self-hosted starter presents Mongo as the only persistence layer (Mong | `self-hosted-pipeline/docker-compose.yml:4-10 'mongo:\n  image: mongo:7'; render.yaml:24-27 'database` | no |
| 95 | `afi-starters` | reactor-only | P2 | Reactor presented as THE pipeline engine in the only starter | `self-hosted-pipeline/Dockerfile:3 'ARG REACTOR_REPO=https://github.com/AFI-Protocol/afi-reactor.git'` | no |
| 96 | `afi-starters` | stale-arch-docs | P3 | README advertises many starters that do not exist (stale/aspirational  | `README.md:11-31 lists starter-signal-generator/.../starter-research-tool and 'cd afi-starters/starte` | no |
| 97 | `afi-tiny-brains` | reactor-only | P2 | I/O contract hand-mirrored from afi-reactor TS types, not validated ag | `tiny_brains_service/models.py:12 "# Input Models (mirror TinyBrainsFroggyInput from src/aiMl/tinyBra` | no |
| 98 | `afi-tiny-brains` | Mongo-only | P2 | Inference is non-deterministic / model versions not pinned in output ( | `tiny_brains_service/brains/chronos_brain.py:146 "num_samples=10,  # Generate multiple samples for un` | no |
| 99 | `afi-token` | BASE-ledger | P2 | On-chain mint is single-beneficiary; no econ split / gauge despite age | `src/AFIMintCoordinator.sol:76 'token.mintEmissions(req.beneficiary, req.tokenAmount);' (single benef` | no |
| 100 | `afi-token` | mint-model | P2 | Decentralization claims contradict single-Safe admin+emissions role co | `README.md:225 '✅ No centralized control' vs script/DeployAFITokenMainnet.s.sol:62-63 'address admin_` | no |
| 101 | `afi-token` | other | P2 | Local SignalSchema.zod.ts is not the canonical USS v1.1 dialect | `models/SignalSchema.zod.ts:3-15 'export const SignalSchema = z.object({ id, provider_id, content, ti` | no |
| 102 | `afi-token` | reactor-only | P2 | Replay/'Codex replayable' claim unbacked on-chain; receipt is breadcru | `src/AFIMintCoordinator.sol:84-85 'emit MintCoordinated(req.signalId, req.epoch, req.beneficiary, req` | no |
| 103 | `afi-token` | BASE-ledger | P3 | Stale toolchain and entrypoint metadata | `.droid.json:4 '"toolchain": "hardhat"'; .afi-codex.json:8 '"src/AFICoordinator.sol"' (file does not ` | no |

## P0/P1 Notable Findings Appendix

High-severity items from `notable_findings[]` (distinct from contradiction register).

### [P1] `afi-config` — CI validation gate is a no-op due to script name mismatch
- Evidence: `.github/workflows/ci.yml:21-22 run: npm run validate:config --if-present (package.json has no validate:config; defines validate at line 13)`
- Recommendation: Fix CI to call `npm run validate` (and `npm test`) so the AJV schema-compile + example-validation suite gates every PR to the source-of-truth repo. Until fixed, malformed normative schemas can merge to main.

### [P1] `afi-config` — No Commitment-plane schema (mint receipt/emissions/epoch/content-hash anchors)
- Evidence: `Only validatorConfig.schema.json:79-103 references mint (coordinatorAddress regex, chainId, gas) and droid docs name AFIMintCoordinator/AFISignalReceipt/EmissionsMinted; no schema defines receipt metadata (signalId/epoch/amounts/beneficiary/contentHash)`
- Recommendation: Add a normative receipt/anchor schema to this library so the on-chain<->off-chain linkage (signalId/epoch/content hash) is validatable by external parties, per decentralization rule 4. Even a breadcrumb-receipt schema would close the gap.

### [P1] `afi-gateway` — Live signal-ingest route writes VaultedSignalRecord directly to Mongo TSSD vault
- Evidence: `src/http/app.ts:122-141 'app.post("/api/v1/signals", auth, ... const vault = vaultFactory(tenantId); await vault.upsert(parsed.record); ... res.status(202).json({ status: "accepted", ... signalId })'; server.ts:76 advertises 'POST /api/v1/signals — Ingest signal into TSSD (tenant scoped)'`
- Recommendation: Clarify whether the gateway is an HTTP client (per README/AGENTS) or a first-class ingest+persistence node. If the latter, update the 'no direct DB access' docs and treat this as a reference ingest implementation that MUST validate USS/CPJ and route through the canonical engine selector, not hardcoded Mongo.

### [P1] `afi-gateway` — Ingest validation is 4-field presence check, no canonical schema validation
- Evidence: `src/http/app.ts:20-57 normalizeSignalPayload: 'const required = ["signalId","epochId","market","timeframe"]; ... stages: payload.stages ?? {}, publicSurface: payload.publicSurface ?? {...}, proprietaryDetail: payload.proprietaryDetail'`
- Recommendation: Validate inbound payloads against the canonical USS v1.1 / CPJ v0.1 / vault.schema.json (afi.usignal.v1) before persisting, to satisfy decentralization rule (1) at the ingest boundary.

### [P1] `afi-infra` — Persistence layer is MongoDB-only across spec, client, factory, replay (Mongo tunnel vision)
- Evidence: `68 mongo grep hits; src/tssd/MongoTSSDVaultClient.ts is the sole persistent client; TSSDVaultClient.ts:218 returns MongoTSSDVaultClient; replay spec line 24 "only talk to TSSD (Mongo)"; grep postgresql|timescaledb|influxdb = 0 hits`
- Recommendation: Document that ITSSDVaultClient is the normative contract and Mongo is ONE reference adapter; add a non-Mongo adapter stub or explicit note that Postgres/Timescale/Influx adapters are protocol-valid to dispel Mongo-as-mandatory.

### [P1] `afi-mint` — Snapshot governance vote determines mint finality (selection vs finality boundary)
- Evidence: `src/orchestrator/DisputeResolver.ts:106-122 evaluateChallengeOutcome + src/orchestrator/SignalStateManager.ts:280-290 'if (challengeSucceeded) { ... overturn original decision }'`
- Recommendation: Document whether governance overturning a deterministic validator decision is intended protocol behavior. Per north-star rule 5 governance must not override deterministic scoring/finality; clarify this as appeal-of-record vs finality override.

### [P1] `afi-reactor` — README and doctrine present reference orchestrator as protocol law ('ONLY orchestrator', 'DAG is law')
- Evidence: `README.md:137 "afi-reactor is the ONLY orchestrator in AFI Protocol."; docs/AFI_ORCHESTRATOR_DOCTRINE.md:290 "This doctrine is authoritative. All afi-reactor code must comply."`
- Recommendation: Reframe doctrine/README as 'reference orchestrator for the AFI reference spine'. The portable-protocol law is conformance to USS/CPJ/scored-signal/vaulted-signal contracts + replay invariants, NOT that this DAG engine is the only legal orchestrator. Extract the genuinely normative pieces (replay invariants, signal envelope) to spec repo.

### [P1] `afi-reactor` — Vault persistence is Mongo-only and canonical contract is BSON-typed; violates multi-engine evidence plane
- Evidence: `src/services/tssdVaultService.ts:22 "import { MongoClient, Db, Collection } from \"mongodb\";"; config/schema.codex.json:49-53 vaulted-signal meta uses bsonType; config/dag.codex.json:196 "persists execution result to MongoDB vault."`
- Recommendation: Define vaulted-signal as an engine-neutral JSON Schema (current vault.schema.json North Star), with Mongo BSON as one binding. Make the reactor write through a storage-agnostic interface so PostgreSQL/Timescale/Influx backends can satisfy the same contract.

### [P1] `afi-token` — EMISSIONS_ROLE concentration is the only gate on minting
- Evidence: `src/AFIToken.sol:92 'function mintEmissions(address beneficiary, uint256 amount) external onlyRole(EMISSIONS_ROLE)' with mainnet Pattern A granting EMISSIONS_ROLE to the Treasury Safe (DeployAFITokenMainnet.s.sol:63)`
- Recommendation: Document that protocol finality / determinism must be enforced off-chain by afi-mint before this role mints; an external validator cannot verify scoring legitimacy from on-chain data alone. Clarify trust assumption in VALIDATOR_REPLAY_SPEC.
