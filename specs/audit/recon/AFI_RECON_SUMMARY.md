# AFI Recon Summary (Phase 1)

**Status:** DRAFT — Phase 1 recon complete; themes and verification pending
**Extracted:** 2026-06-15T01:18:51Z
**Source workflow:** `wf_854527ef-4aa`
**Repos audited:** 31

Companion: [`AFI_RECON_CORPUS.json`](./AFI_RECON_CORPUS.json) | Checkpoint: [`../AFI_AUDIT_CHECKPOINT.md`](../AFI_AUDIT_CHECKPOINT.md)

---

## Classification Snapshot

| Classification | Count |
|----------------|-------|
| NORMATIVE | 2 |
| REFERENCE_IMPL | 8 |
| SUPPORTING | 11 |
| RESEARCH | 2 |
| DOCS | 2 |
| STALE | 4 |
| OUT_OF_SCOPE | 2 |

## Replay Relevance

| Level | Count |
|-------|-------|
| critical | 3 |
| partial | 10 |
| none | 18 |

## Reference Spine

| Segment | Repo(s) |
|---------|---------|
| Ingest boundary | `afi-gateway` |
| Scoring DAG | `afi-reactor`, `afi-core`, `afi-plugins`, `afi-tiny-brains` |
| Evidence vault | `afi-infra` |
| Mint coordination | `afi-mint` |
| On-chain commitment | `afi-token` |
| Normative schemas/types | `afi-config`, `afi-infra` |

## Full Classification Table

| Repo | Classification | Replay | Purpose (abbrev.) |
|------|----------------|--------|-------------------|
| `.github` | SUPPORTING | none | Org-wide GitHub configuration repository for the AFI Protocol organization, hold… |
| `afi-artifacts` | SUPPORTING | partial | Versioned, citable (Zenodo DOI 10.5281/zenodo.16857347) reproducibility bundle f… |
| `afi-assets` | SUPPORTING | none | Brand and visual-asset scaffold repository intended to store AFI Protocol logos,… |
| `afi-benchkit` | SUPPORTING | partial | A standalone, container-packaged Python toolkit that runs deterministic, seeded … |
| `afi-cli-framework` | SUPPORTING | none | A generic, framework-agnostic Node.js/TypeScript CLI scaffolding library (a Comm… |
| `afi-config` | NORMATIVE | critical | afi-config is the canonical configuration and JSON Schema library for AFI Protoc… |
| `afi-core` | REFERENCE_IMPL | partial | afi-core is a pure-ESM TypeScript runtime library providing the deterministic sc… |
| `afi-docs` | DOCS | none | Documentation hub for AFI Protocol: hosts the portable-protocol surface spec and… |
| `afi-econ` | RESEARCH | none | A dual-stack (TypeScript + Python) deterministic, config-driven economic simulat… |
| `afi-factory` | SUPPORTING | none | afi-factory is a Phase-1 scaffolding repo providing AFI agent templates, a TypeS… |
| `afi-gateway` | REFERENCE_IMPL | partial | An ElizaOS-based universal gateway / framework: it lets community developers bui… |
| `afi-governance` | REFERENCE_IMPL | none | Defines the AFI governance/DAO layer: a standardized "Universal Proposal Signal"… |
| `afi-infra` | NORMATIVE | critical | afi-infra defines AFI's canonical T.S.S.D. Vault types and lifecycle spec (the o… |
| `afi-labs` | RESEARCH | none | afi-labs is the AFI org's explicitly-experimental private R&D sandbox ("junk dra… |
| `afi-math` | SUPPORTING | partial | Pure, deterministic, dependency-free TypeScript library of financial/scoring mat… |
| `afi-mint` | REFERENCE_IMPL | partial | Off-chain coordination of signal-driven AFI token minting: an appeal-based valid… |
| `afi-ops` | SUPPORTING | none | afi-ops is a Phase-1 scaffolding operations/devops toolkit providing local-deplo… |
| `afi-plugins` | REFERENCE_IMPL | partial | Central plugin registry and template/stub pack that defines the extension surfac… |
| `afi-protocol` | DOCS | none | A governance/onboarding meta-repo that orchestrates the AFI ("Agentic Financial … |
| `afi-reactor` | REFERENCE_IMPL | critical | afi-reactor is the reference TypeScript orchestrator that runs a flexible, plugi… |
| `afi-research-site` | OUT_OF_SCOPE | none | Public-facing marketing/brochure website (Next.js App Router, Axleo template ski… |
| `afi-sdk-python` | STALE | none | Intended official Python SDK for building on AFI Protocol (signal submission/val… |
| `afi-sdk-ts` | STALE | none | Intended (currently unimplemented) official TypeScript/JavaScript SDK for buildi… |
| `afi-skills` | SUPPORTING | partial | A canonical, versioned library of AFI agent "skills" -- discrete reusable capabi… |
| `afi-starters` | SUPPORTING | none | Provides clone-and-extend starter templates and a self-hosted deployment kit (Do… |
| `afi-tiny-brains` | REFERENCE_IMPL | partial | A FastAPI microservice exposing POST /predict/froggy that runs a three-brain ens… |
| `afi-token` | REFERENCE_IMPL | partial | afi-token implements the AFI Protocol's on-chain Commitment plane on BASE: an xE… |
| `afi-xerc20` | OUT_OF_SCOPE | none | A vendored fork of the defi-wonderland/xERC20 (Connext xTokens) Solidity standar… |

## P0/P1 Notable Findings (Unverified)

- **[P1] `afi-config`** — CI validation gate is a no-op due to script name mismatch
  - Evidence: `.github/workflows/ci.yml:21-22 run: npm run validate:config --if-present (package.json has no validate:config; defines validate at line 13)`
- **[P1] `afi-config`** — No Commitment-plane schema (mint receipt/emissions/epoch/content-hash anchors)
  - Evidence: `Only validatorConfig.schema.json:79-103 references mint (coordinatorAddress regex, chainId, gas) and droid docs name AFIMintCoordinator/AFISignalReceipt/EmissionsMinted; no schema defines receipt metadata (signalId/epoch/amounts/beneficiary/contentHash)`
- **[P1] `afi-gateway`** — Live signal-ingest route writes VaultedSignalRecord directly to Mongo TSSD vault
  - Evidence: `src/http/app.ts:122-141 'app.post("/api/v1/signals", auth, ... const vault = vaultFactory(tenantId); await vault.upsert(parsed.record); ... res.status(202).json({ status: "accepted", ... signalId })'; server.ts:76 advertises 'POST /api/v1/signals — Ingest signal into TSSD (tenant scoped)'`
- **[P1] `afi-gateway`** — Ingest validation is 4-field presence check, no canonical schema validation
  - Evidence: `src/http/app.ts:20-57 normalizeSignalPayload: 'const required = ["signalId","epochId","market","timeframe"]; ... stages: payload.stages ?? {}, publicSurface: payload.publicSurface ?? {...}, proprietaryDetail: payload.proprietaryDetail'`
- **[P1] `afi-infra`** — Persistence layer is MongoDB-only across spec, client, factory, replay (Mongo tunnel vision)
  - Evidence: `68 mongo grep hits; src/tssd/MongoTSSDVaultClient.ts is the sole persistent client; TSSDVaultClient.ts:218 returns MongoTSSDVaultClient; replay spec line 24 "only talk to TSSD (Mongo)"; grep postgresql|timescaledb|influxdb = 0 hits`
- **[P1] `afi-mint`** — Snapshot governance vote determines mint finality (selection vs finality boundary)
  - Evidence: `src/orchestrator/DisputeResolver.ts:106-122 evaluateChallengeOutcome + src/orchestrator/SignalStateManager.ts:280-290 'if (challengeSucceeded) { ... overturn original decision }'`
- **[P1] `afi-reactor`** — README and doctrine present reference orchestrator as protocol law ('ONLY orchestrator', 'DAG is law')
  - Evidence: `README.md:137 "afi-reactor is the ONLY orchestrator in AFI Protocol."; docs/AFI_ORCHESTRATOR_DOCTRINE.md:290 "This doctrine is authoritative. All afi-reactor code must comply."`
- **[P1] `afi-reactor`** — Vault persistence is Mongo-only and canonical contract is BSON-typed; violates multi-engine evidence plane
  - Evidence: `src/services/tssdVaultService.ts:22 "import { MongoClient, Db, Collection } from \"mongodb\";"; config/schema.codex.json:49-53 vaulted-signal meta uses bsonType; config/dag.codex.json:196 "persists execution result to MongoDB vault."`
- **[P1] `afi-token`** — EMISSIONS_ROLE concentration is the only gate on minting
  - Evidence: `src/AFIToken.sol:92 'function mintEmissions(address beneficiary, uint256 amount) external onlyRole(EMISSIONS_ROLE)' with mainnet Pattern A granting EMISSIONS_ROLE to the Treasury Safe (DeployAFITokenMainnet.s.sol:63)`
