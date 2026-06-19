# AFI System Atlas

High-level map of AFI components across all repositories in `/Users/secretservice/AFI_Modular_Repos`.

## Pipeline / Ingestion / Normalization
- **afi-reactor**: HTTP ingress (`src/server.ts`) for TradingView `/api/webhooks/tradingview` and CPJ `/api/ingest/cpj`; maps TradingView to USS v1.1 (`src/uss/tradingViewMapper.ts`); AJV validation against `afi-config` schemas (`src/uss/ussValidator.ts`).
- **DAG execution** (scored-only): `src/services/froggyDemoService.ts` + `src/config/froggyPipeline.ts` (uss-telemetry-deriver → parallel enrichment branches → enrichment-adapter → froggy-analyst → tssd-vault-write).
- **Collectors**: Telegram collectors present under `src/collectors/` (not detailed here).
- **Normalization**: USS facts/provenance from mappers; schemas from `afi-config`.

## Scoring / UWR / Validators / Replay
- **afi-core**: Core scoring/validator logic (Node/TS library; needs module-level doc extraction).
- **afi-reactor**: Scores signals via the canonical Froggy DAG and emits `ReactorScoredSignalV1` (scored-only: `analystScore.uwrScore` + `uwrAxes{structure,execution,risk,insight}`); replay endpoints `/replay/signal/:signalId`. Validator certification is an external concern, not a reactor plugin.
- **afi-math / afi-econ**: Math/econ primitives that feed scoring models (Node/TS and Python).
- **afi-benchkit**: Benchmark/eval harnesses (Python) for validating scoring models.

## Vault / Storage / Provenance
- **afi-reactor**: TSSD vault persistence via `src/services/tssdVaultService.ts`; writes canonical USS + pipeline outputs when `AFI_MONGO_URI` configured; provenance enforcement via `_priceFeedMetadata` guard.
- **afi-config**: USS schemas ensure provenance fields; examples in `examples/usignal/v1_1/`.
- **afi-infra**: Infrastructure services (needs deeper pass) likely to host shared storage/ops patterns.

## Plugins / Skills / Enrichment
- **afi-plugins**: Plugin packages (catalog to be extracted).
- **afi-skills**: Skills library for agents/pipelines.
- **afi-reactor**: Enrichment plugins `plugins/froggy-enrichment-*`, enrichment adapter, sentiment/news, AI/ML hooks.
- **afi-gateway**: AFI Reactor Actions plugin for ElizaOS (`plugins/afi-reactor-actions`), telemetry plugin (`plugins/afi-telemetry`).

## Agents / Droids / Factory Orchestration
- **afi-gateway**: ElizaOS runtime with the active Phoenix concierge persona (`src/*.character.ts`), full server in `src/server-full.ts`). Alpha/Froggy may remain as generic character names; the legacy validator and signal-structuring demo personas are deprecated/removed.
- **afi-factory**: Factory orchestration (Node/TS).
- **afi-ops**: Operational tooling for agent/service deployment.
- **afi-protocol / afi-docs**: Meta/governance context for agents/droids.

## Gateway / ElizaOS Lane
- **afi-gateway**: HTTP health/ping and full Eliza API; bridges to AFI Reactor via actions; depends on `OPENAI_API_KEY` and optional Mongo for sessions.

## Token / Minting / Receipts / Metadata
- **afi-mint**: Signal-driven minting pipeline (Node/TS + Solidity).
- **afi-token**: Token protocol (Node/TS + Solidity) with envs for RPC/keys.
- **afi-labs**: Experimental contracts.
- **afi-governance**: Governance assets, likely proposal flow and registries.

## Governance / Epoch Pulse / Registries / Proposal Flow
- **afi-governance**: Governance repo (needs extraction of registries/proposals).
- **afi-protocol**: Meta-repo coordinating governance artifacts.

## Infra / Ops / Deployments / CI
- **afi-infra**: Infrastructure services; scripts for tests/builds.
- **afi-ops**: Ops scripts and deploy helpers; .env.example shows DB/agent keys.
- **scripts**: Shared script folder (needs indexing).

## Research Primitives (Math, Econ, Benchkit, Evals, Datasets)
- **afi-math**: Math library (TS).
- **afi-econ**: Econ models (TS/Python).
- **afi-benchkit**: Benchmark and evaluation toolkit (Python).
- **afi-research-site**: Research site code (Next.js-based).
- **afi-artifacts**: Paper reproducibility bundles.

## Gateway Docs + Documentation Source
- **afi-docs**: Documentation site source.
- **afi-config**: Schemas/specs used across repos.
- **augmentcode_rules**: Coding rule configs.

## Boundary Conflicts / Naming Drift (observations)
- Multiple Mongo/vault implementations noted in afi-reactor vs infra (needs harmonization).
- Token/mint responsibilities split across afi-token, afi-mint, afi-labs (requires clear boundaries).
- Math/econ primitives spread across TS and Python; doc consolidation needed.
