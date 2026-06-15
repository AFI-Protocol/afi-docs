# AFI Reference Implementation Map

**Status:** DRAFT — Phase 1 recon only; themes unverified
**Date:** 2026-06-15

Promote to [`afi-docs/specs/AFI_REFERENCE_IMPL_MAP.md`](../../AFI_REFERENCE_IMPL_MAP.md) after Phase 3 verification.

Source: [`recon/AFI_RECON_CORPUS.json`](../recon/AFI_RECON_CORPUS.json)

---

## Reference Spine

```
ingest (afi-gateway)
  -> scoring DAG (afi-reactor + afi-core + afi-plugins + afi-tiny-brains)
  -> evidence vault (afi-infra)
  -> mint coordination (afi-mint)
  -> on-chain commitment (afi-token)

normative surface: afi-config + afi-infra (TSSD types/spec)
```

| Segment | Repo(s) | Classification |
|---------|---------|----------------|
| Ingest boundary | `afi-gateway` | REFERENCE_IMPL |
| Scoring DAG | `afi-reactor` | REFERENCE_IMPL |
| Scoring DAG | `afi-core` | REFERENCE_IMPL |
| Scoring DAG | `afi-plugins` | REFERENCE_IMPL |
| Scoring DAG | `afi-tiny-brains` | REFERENCE_IMPL |
| Evidence vault | `afi-infra` | NORMATIVE |
| Mint coordination | `afi-mint` | REFERENCE_IMPL |
| On-chain commitment | `afi-token` | REFERENCE_IMPL |
| Normative schemas/types | `afi-config` | NORMATIVE |
| Normative schemas/types | `afi-infra` | NORMATIVE |

## 31-Repo Classification Table

| Repo | Visibility | Classification | Replay | Recommended action |
|------|------------|----------------|--------|----------------------|
| `.github` | PRIVATE | SUPPORTING | none | tag stale / fix in follow-up: add the missing reusable workf |
| `afi-artifacts` | PUBLIC | SUPPORTING | partial | clarify reference-vs-normative |
| `afi-assets` | PRIVATE | SUPPORTING | none | tag stale |
| `afi-benchkit` | PUBLIC | SUPPORTING | partial | clarify reference-vs-normative |
| `afi-cli-framework` | PRIVATE | SUPPORTING | none | none |
| `afi-cli-shared` | PRIVATE | SUPPORTING | none | none |
| `afi-config` | PUBLIC | NORMATIVE | critical | clarify reference-vs-normative |
| `afi-construct` | PRIVATE | STALE | none | tag stale |
| `afi-core` | PUBLIC | REFERENCE_IMPL | partial | clarify reference-vs-normative |
| `afi-docs` | PRIVATE | DOCS | none | tag stale + clarify reference-vs-normative: (1) Add a banner |
| `afi-econ` | PRIVATE | RESEARCH | none | tag stale (rename internal afi-econ-kit identifiers + remove |
| `afi-factory` | PUBLIC | SUPPORTING | none | clarify reference-vs-normative + tag stale: keep classified  |
| `afi-gateway` | PUBLIC | REFERENCE_IMPL | partial | clarify reference-vs-normative |
| `afi-governance` | PRIVATE | REFERENCE_IMPL | none | clarify reference-vs-normative |
| `afi-infra` | PRIVATE | NORMATIVE | critical | clarify reference-vs-normative |
| `afi-labs` | PRIVATE | RESEARCH | none | tag stale |
| `afi-math` | PUBLIC | SUPPORTING | partial | clarify reference-vs-normative |
| `afi-mint` | PRIVATE | REFERENCE_IMPL | partial | clarify reference-vs-normative |
| `afi-ops` | PRIVATE | SUPPORTING | none | clarify reference-vs-normative |
| `afi-plugins` | PUBLIC | REFERENCE_IMPL | partial | clarify reference-vs-normative |
| `afi-protocol` | PRIVATE | DOCS | none | clarify reference-vs-normative |
| `AFI-Protocol/afi-agents` | PRIVATE | STALE | none | tag stale |
| `afi-reactor` | PUBLIC | REFERENCE_IMPL | critical | clarify reference-vs-normative |
| `afi-research-site` | PRIVATE | OUT_OF_SCOPE | none | none |
| `afi-sdk-python` | PRIVATE | STALE | none | clarify reference-vs-normative |
| `afi-sdk-ts` | PRIVATE | STALE | none | tag stale |
| `afi-skills` | PUBLIC | SUPPORTING | partial | clarify reference-vs-normative |
| `afi-starters` | PRIVATE | SUPPORTING | none | clarify reference-vs-normative |
| `afi-tiny-brains` | PRIVATE | REFERENCE_IMPL | partial | clarify reference-vs-normative |
| `afi-token` | PRIVATE | REFERENCE_IMPL | partial | clarify reference-vs-normative |
| `afi-xerc20` | PUBLIC | OUT_OF_SCOPE | none | clarify reference-vs-normative |

## Per-Repo Blocks

### `.github`

- **Purpose:** Org-wide GitHub configuration repository for the AFI Protocol organization, holding the org profile/repository map plus a README describing intended reusable GitHub Actions workflows and templates (none of which are actually present in the repo yet).
- **Classification:** SUPPORTING
- **Rationale:** Contains only README.md, package.json (private, name '.github', description 'Organization-wide GitHub configuration for AFI Protocol'), and profile/README.md (the org repository map). No schemas, contracts, type defs, code, or specs. It is GitHub org tooling/config plus a documentation index, i.e. S…
- **Touchpoints:** DAG/pipeline (named only, in repo map), mint/receipt (named only, in repo map), contracts (named only: afi-token), schemas (named only: afi-config, afi-artifacts), registries/reputation (named only: validator/mentor registries), SDK/API (named only: afi-sdk-ts, afi-sdk-python), replay/determinism (named only: afi-reactor replay, afi-artifacts replay)
- **Dependencies:** upstream=[]; downstream=['afi-core', 'afi-reactor', 'afi-plugins', 'afi-sdk-ts', 'afi-sdk-python', 'afi-starters', 'afi-protocol', 'afi-governance', 'afi-mint', 'afi-token', 'afi-benchkit', 'afi-infra', 'afi-ops', 'afi-factory', 'afi-docs', 'afi-artifacts', 'afi-research-site', 'afi-config', 'afi-assets', 'afi-labs']

### `afi-artifacts`

- **Purpose:** Versioned, citable (Zenodo DOI 10.5281/zenodo.16857347) reproducibility bundle for the "Agentic Financial Intelligence" paper, packaging snapshot JSON Schemas (USS ingestion, vaulted TSSD, universal proposal), an example codex replay manifest, sample vault-ready records, and a deterministic mock-replay smoke test so reviewers can verify schema compliance and replay wiring without the full AFI engine.
- **Classification:** SUPPORTING
- **Rationale:** This is a static "paper reproducibility bundle" (release tag paper-2025-v2.2) accompanying the AFI paper, not a runtime or a normative spec source. repro/README.md:4-5 "It is a validation pack: schemas, example records, Codex manifest, and a deterministic mock replay. It does not include the AFI run…
- **Touchpoints:** USS ingest (snapshot schema), TSSD/vault (vaulted_tssd snapshot schema + example record), DAG/pipeline (referenced as out-of-scope; pipeline field in schema), schemas (USS, vaulted TSSD, universal proposal snapshots), replay/determinism (codex manifest + mock_replay + canonicalizeSignal), registries/reputation (validators/scorers listed in codex; proposal voting/governance schema), SDK/API (canonicalizeSignal ingestion->validator helper)
- **Normative artifacts:**
  - `/home/user/AFI-Protocol/afi-artifacts/repro/schemas/universal_signal_ingestion.schema.json (snapshot of USS ingestion, NOT the canonical afi-config/schemas/usignal/v1)`
  - `/home/user/AFI-Protocol/afi-artifacts/repro/schemas/vaulted_tssd.schema.json (snapshot of vault.schema.json TSSD shape)`
  - `/home/user/AFI-Protocol/afi-artifacts/repro/schemas/universal_proposal_schema.json (CPJ-like proposal v0.1 snapshot)`
  - `/home/user/AFI-Protocol/afi-artifacts/repro/schemas/universal_signal_schema.mjs`
  - `/home/user/AFI-Protocol/afi-artifacts/repro/schemas/vaulted_signal_schema.mjs`
  - `/home/user/AFI-Protocol/afi-artifacts/repro/schemas/universal_proposal_schema.mjs`
  - `/home/user/AFI-Protocol/afi-artifacts/repro/codex/afi-codex.json (replay manifest: epoch, scorers, validators, seed, deterministic)`
  - `/home/user/AFI-Protocol/afi-artifacts/repro/tools/replay/canonicalizeSignal.js (ingestion->validator canonicalization rules)`
- **Dependencies:** upstream=['afi-config (canonical schemas/codex/governance: AGENTS.md cites afi-config/codex/governance/droids/AFI_DROID_CHARTER.v0.1.md; schemas here are snapshots of afi-config USS/vault/CPJ)', "AFI paper / SSRN-arXiv (source of the snapshots — schemas labeled 'shown in Appendix A')"]; downstream=["External reviewers / Zenodo citers (the bundle's primary consumers)", 'CI (.github/workflows/reproducibility.yml runs npm test)', "AGENTS.md claims consumed by 'CI/CD pipelines, deployment workflows, audit processes'"]

### `afi-assets`

- **Purpose:** Brand and visual-asset scaffold repository intended to store AFI Protocol logos, token icons, and media kits for frontend/docs consumption; all asset directories are currently empty placeholders.
- **Classification:** SUPPORTING
- **Rationale:** README.asset.md:3 states "This repo stores all visual, brand, and identity-related files for the AFI Protocol." package.json:4 description is "AFI brand assets, logos, and design files". The logos/, tokens/, media_kits/ dirs contain only .gitkeep (0 bytes). No schemas, contracts, protocol code, or d…
- **Touchpoints:** none — no USS/CPJ ingest, TSSD/vault, mint/receipt, DAG/pipeline, schemas, contracts, emissions, replay, registries, SDK/API, or analytics surfaces are present; the tokens/ dir is for token ICON imagery, not token contracts
- **Dependencies:** upstream=[]; downstream=['Consumed (read-only) per README.asset.md by: frontend dashboards, agentic UIs, docs/GitBook generators — aspirational; no code dependency edges exist since the repo is empty']

### `afi-benchkit`

- **Purpose:** A standalone, container-packaged Python toolkit that runs deterministic, seeded validator benchmarks (PoI capability and PoInsight usefulness suites) over CSV datasets, emitting hash-stamped canonical artifacts, metrics, calibration/capability plots, and a composite "reputation" score with confidence intervals for reproducible validator verification.
- **Classification:** SUPPORTING
- **Rationale:** A standalone Python package (pyproject.toml:6 name="afi-benchkit", entrypoint afi-bench=afi_benchkit.cli:main) for deterministic validator benchmarking. README.md:22-26 explicitly bounds it: "This is a benchmark and verification toolkit only... Does NOT contain DAG/engine/scoring runtime logic... Do…
- **Touchpoints:** replay/determinism (hash-locked reproducible benchmark outputs, golden-image verification), registries/reputation (computes benchmark-derived validator reputation scores influencing selection/allocation), scoring/metrics (PoI/PoInsight benchmark metrics: IC, hit-rate, Sharpe, coverage, vitality, latency), SDK/CLI (afi-bench CLI)
- **Dependencies:** upstream=['afi-cli-shared (scripts/generate_benchmarks.sh:8, scripts/capsule_run.sh:12, scripts/lock/{compile,refresh}.sh source afi-cli-shared/scripts/lib/afi-shared.sh)', 'ghcr.io/AFI-Protocol/afi-benchkit container registry (README.md:177, ci.yml:80)']; downstream=[]

### `afi-cli-framework`

- **Purpose:** A generic, framework-agnostic Node.js/TypeScript CLI scaffolding library (a Commander.js wrapper providing base CLI app class, hierarchical config, logging, validation, error handling, and an extension/plugin system) intended to be reused by AFI command-line tools.
- **Classification:** SUPPORTING
- **Rationale:** README.md:3 describes it as "A modular CLI framework for AFI Node.js projects, built on Commander.js" and package.json:3 as "Modular CLI framework for AFI projects using Commander.js". The only dependency is commander (package.json:16). Source (src/) contains CliApp, ConfigManager, Logger, validatio…
- **Dependencies:** upstream=['commander (npm, ^14.0.2)']; downstream=[]

### `afi-cli-shared`

- **Purpose:** A reusable, domain-agnostic shared CLI framework for AFI Python projects built on Click — providing BaseCli (a click.Group subclass), a hierarchical ConfigManager (defaults -> .afi-cli.json -> AFI_CLI_* env vars), validation/error-handling helpers, an Extension/ExtensionManager plugin system, plus a Bash utility library (scripts/lib/afi-shared.sh) for logging, docker/podman, and file operations.
- **Classification:** SUPPORTING
- **Rationale:** Generic Click-based CLI framework with zero AFI protocol surface. README.md:3 "A shared CLI framework for AFI Python projects, built on Click." pyproject.toml:13 description "Shared CLI framework for AFI Python projects using Click". Source (src/afi_cli_shared/*.py) contains only BaseCli, ConfigMana…
- **Dependencies:** upstream=['click (PyPI runtime dependency)', 'pytest (optional, test extra)', 'sphinx (optional, docs extra)']; downstream=['AFI Python CLI repos that pip install afi-cli-shared and extend BaseCli, or source scripts/lib/afi-shared.sh (consumers not enumerable from within this repo)']

### `afi-config`

- **Purpose:** afi-config is the canonical configuration and JSON Schema library for AFI Protocol: it provides the normative ingest dialects (USS v1.1, CPJ v0.1), vault/pipeline/plugin/validator/blueprint schemas, agent-registry + reputation invariants, and AJV-based validation utilities consumed by every other AFI module.
- **Classification:** NORMATIVE
- **Rationale:** This repo is the canonical JSON Schema + spec library that defines the AFI interoperability surface. README.md:3-5 declares it the "single source of truth for all AFI Protocol configuration schemas". It physically holds named normative artifacts: USS v1/v1.1 (schemas/usignal/), CPJ v0.1 (schemas/cpj…
- **Touchpoints:** USS/CPJ ingest, TSSD/vault, DAG/pipeline, schemas, replay/determinism, registries/reputation, mint/receipt (config ref only), emissions (validator thresholds)
- **Normative artifacts:**
  - `/home/user/AFI-Protocol/afi-config/schemas/usignal/v1_1/index.schema.json`
  - `/home/user/AFI-Protocol/afi-config/schemas/usignal/v1_1/core.schema.json`
  - `/home/user/AFI-Protocol/afi-config/schemas/usignal/v1/index.schema.json`
  - `/home/user/AFI-Protocol/afi-config/schemas/usignal/v1/core.schema.json`
  - `/home/user/AFI-Protocol/afi-config/schemas/usignal/v1/lenses/equity.lens.schema.json`
  - `/home/user/AFI-Protocol/afi-config/schemas/usignal/v1/lenses/strategy.lens.schema.json`
  - `/home/user/AFI-Protocol/afi-config/schemas/usignal/v1/lenses/macro.lens.schema.json`
  - `/home/user/AFI-Protocol/afi-config/schemas/usignal/v1/lenses/onchain.lens.schema.json`
  - … (+13 more)
- **Dependencies:** upstream=[]; downstream=['afi-core', 'afi-reactor', 'afi-infra', 'afi-plugins', 'afi-ops', 'afi-token', 'afi-skills', 'afi-factory']

### `afi-construct`

- **Purpose:** A minimal archived scaffold for a "public simulation and blueprint layer" — a white-room/dojo environment intended for rehearsing DAG pipelines and modular agent interactions before hardening them in production logic (per README.md @ e7cfd87).
- **Classification:** STALE
- **Rationale:** Repo is GitHub-archived (archived:true, pushed_at 2025-07-15) and consists of only 8 files / 5 commits on a single `main` branch: README, two JSON stubs, an aider config, an init script, a no-op CI workflow, .gitignore, and an empty construct_templates/.gitkeep. README.md self-describes it as "the p…
- **Touchpoints:** DAG/pipeline (blueprint.schema.json id/nodes/edges; pipeline_manifest.json), schemas (a divergent blueprint schema stub), validator/PoI simulation only (mock-validator-flow, mock data agents)
- **Dependencies:** upstream=['afi-labs (named as upstream private-experiments source in README lineage)']; downstream=["afi-core (named as production-logic target where blueprints are 'hardened'; afi-core is a stale/renamed name)"]

### `afi-core`

- **Purpose:** afi-core is a pure-ESM TypeScript runtime library providing the deterministic scoring/validation primitives of AFI Protocol: the canonical UWR (Universal Weighting Rule) scorer, time/Greeks decay integration over afi-math, deterministic novelty scoring, the per-signal AnalystScoreTemplate, the ValidatorDecision/Outcome envelopes, a SignalEnvelope DAG record type, local v0.1 Zod schemas, and stub runtime/ElizaOS adapter types (package.json:3 "Core runtime for agent signal validation in AFI Protocol").
- **Classification:** REFERENCE_IMPL
- **Rationale:** It implements concrete, working scoring/validation logic for the reference spine (UWR aggregator, decay, novelty, Froggy analyst) rather than defining cross-stack interoperability rules, yet it also holds some genuinely normative-adjacent type contracts. It self-describes as "our runtime library, no…
- **Touchpoints:** DAG/pipeline (SignalEnvelope execution trace, AnalystScoreTemplate.afiDAGConfig, PipelineConfigSchema), schemas (local v0.1 Zod: SignalSchema, PipelineConfig, ValidatorMetadata, ValidatorGovernance, SignalFinalizationRequest, AnalystScoreTemplate, GreeksDecayTemplate), replay/determinism (UWR + novelty deterministic; ValidatorDecisionBase.createdAt for audit/replay; replaySessionId), registries/reputation (ValidatorMetadata poiScore/stakeWeight/reputationScore; ValidatorGovernance; explicit rule reputation MUST NOT override UWR/vault finality), mint/receipt (ValidatorOutcome.mintEligible; emitMintInstruction stub; docs reference AFIMintCoordinator/AFISignalReceipt as out-of-repo), TSSD/vault (referenced only as out-of-repo finality target; afiRuntimeAdapter telemetry-to-vault TODOs), USS/CPJ ingest (regimeTag aligns to macro.regimeTag in uSignal schema owned by afi-config; no CPJ), SDK/API (package exports of validators/schemas/analyst/decay/runtime for downstream consumers), emissions (referenced only; off-chain emissions docs note splits/Epoch Pulse unimplemented)
- **Normative artifacts:**
  - `/home/user/AFI-Protocol/afi-core/validators/UniversalWeightingRule.ts (canonical UWR v0.1 implementation + UwrAxesInput/Config type contract)`
  - `/home/user/AFI-Protocol/afi-core/validators/ValidatorDecision.ts (ValidatorDecisionBase/ValidatorOutcome/ValidatorScoreOutput envelopes; reputation-cannot-override rule)`
  - `/home/user/AFI-Protocol/afi-core/validators/NoveltyTypes.ts (NoveltyResult v0.1 deterministic envelope)`
  - `/home/user/AFI-Protocol/afi-core/src/analyst/AnalystScoreTemplate.ts (canonical per-signal analyst scoring template + Zod schema)`
  - `/home/user/AFI-Protocol/afi-core/src/decay/GreeksDecayTemplate.ts (canonical decay template + Zod schema)`
  - `/home/user/AFI-Protocol/afi-core/validators/SignalDecay.ts (decay integration over afi-math)`
  - `/home/user/AFI-Protocol/afi-core/schemas/universal_signal_schema.ts (local v0.1 SignalSchema)`
  - `/home/user/AFI-Protocol/afi-core/schemas/validator_metadata_schema.ts`
  - … (+5 more)
- **Dependencies:** upstream=['@afi-protocol/afi-math (package.json:69, git+ssh pinned #2042ed3 — provides decay models)', 'afi-config (canonical USS/macro schemas, governance-approved UWR weights, REGISTRIES_AND_REPUTATION.v0.1.md — referenced, not a code dep)', 'afi-docs (canonical specs referenced as future home of VALIDATOR_DECISION/NOVELTY specs)', 'afi-infra (TSSD vault + validator_metadata_v1 evolution; referenced only)']; downstream=['afi-reactor (consumer: orchestrates afi-core validators/scoring per AGENTS.md:79)', 'afi-plugins / Eliza gateways (consume shared types/clients per .afi-codex.json:22-24 and AGENTS.md:86-90)', 'afi-token (consumes ValidatorOutcome/mint-instruction shapes downstream; mint logic out-of-repo)']

### `afi-docs`

- **Purpose:** Documentation hub for AFI Protocol: hosts the portable-protocol surface spec and investigation charter, plus developer guides, architecture/status docs, branch/audit reports, droid instructions, and the Signal-Lore narrative series; contains no protocol code.
- **Classification:** DOCS
- **Rationale:** This is the AFI documentation hub. README.md:6 states it is "the official documentation hub for every public facet of AFI: protocol specs, developer guides, governance blueprints, and the illustrative Signal-Lore series." AGENTS.md:13-16 explicitly forbids code ("What this repo is NOT for: Code impl…
- **Touchpoints:** USS/CPJ ingest (described, not defined), TSSD/vault (described, points to afi-infra), mint/receipt (described, points to afi-token/afi-mint), DAG/pipeline (doctrine + status docs), schemas (pointers to afi-config), contracts (architecture description only), emissions (described), replay/determinism (described, points to afi-reactor), registries/reputation (pointer), SDK/API (referenced), analytics (ABSENT)
- **Normative artifacts:**
  - `specs/AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md (direction-setting normative-vs-reference charter; the audit north star itself)`
  - `specs/AFI_PROTOCOL_INVESTIGATION_PROMPT.md (investigation methodology charter)`
- **Dependencies:** upstream=['afi-config (schemas referenced: USS, vault, pipeline, blueprint, plugin-manifest)', 'afi-infra (TSSD vault spec/types referenced)', 'afi-reactor (orchestrator doctrine, replay spec, DAG referenced)', 'afi-token (contract sources referenced)', 'afi-mint (mint orchestrator referenced)', 'afi-core / afi-math / afi-gateway (described as spine components)']; downstream=[]

### `afi-econ`

- **Purpose:** A dual-stack (TypeScript + Python) deterministic, config-driven economic simulation toolkit that models AFI token emissions, epoch-pulse rhythm, role-based reward/gauge allocation, and payouts for research, parameter-sensitivity, and whitepaper-chart purposes -- explicitly placeholder/toy formulas pending afi-math integration.
- **Classification:** RESEARCH
- **Rationale:** Self-declared research/tooling repo for economic simulation, NOT production or protocol logic. README.md:9 "Status: Research-Grade / Placeholder Models"; README.md:14 "Economic models are PLACEHOLDER / toy implementations"; README.md:24-26 "Do NOT use for: Production parameter decisions... Whitepape…
- **Touchpoints:** emissions (simulated epoch-pulse / minting curves), mint/receipt (consumes receipts.json as simulation input, models tokensMinted/cumulativeSupply), DAG/pipeline (econ pipeline stages: gauge->safety->payouts, NOT scoring DAG), replay/determinism (seeded RNG, provenance stamps, econ replay command, determinism tests), registries/reputation (consumes BenchKit merit scores: reputation/poi/poinsight to weight allocation), schemas (local Pydantic + Zod sim-config schemas only, non-normative), SDK/API (CLI tools: TS afi-econ + Python afi-econ-kit)
- **Dependencies:** upstream=["afi-benchkit (scores.json: reputation/poi/poinsight consumed by gauge; scripts/end_to_end_audit.py:147 find_sibling_repo('afi-benchkit'))", 'afi-math (intended future source of real curves/decay; README.md:16,61 - not yet wired)']; downstream=['afi-token (econ models intended to INFORM contract parameters; README.md:58 - advisory only, no code dependency)', 'afi-core / afi-reactor (named as conceptual relations only; README.md:59-60 - no import/runtime dependency)']

### `afi-factory`

- **Purpose:** afi-factory is a Phase-1 scaffolding repo providing AFI agent templates, a TypeScript template/analyst-config registry, and an agent manifest for registering, versioning, and spawning AFI agents (per README.md:7 and package.json description "AFI agent factory and templates").
- **Classification:** SUPPORTING
- **Rationale:** Phase-1 scaffolding repo for AFI agent templates/manifests/spawning, not a protocol-defining or replay-critical component. README.md:7 "where agent templates are registered, versioned, and spawned across the AFI Protocol"; README.md:33 "Phase 1 Scaffolding - Template registry and manifest are establ…
- **Touchpoints:** DAG/pipeline (analyst enrichment-node topology config in schemas/index.ts + template_registry.ts), schemas (TypeScript mirrors of afi-config analyst-config & enrichment-node schemas), SDK/API (exported template_registry loaders and type guards), registries/reputation (template/agent registry only, not reputation)
- **Dependencies:** upstream=['afi-config (schemas: analyst-config.schema.json, definitions/enrichment-node.schema.json)', 'afi-core (per .afi-codex.json dependsOn and README Related Repositories)', 'afi-config/codex/governance/droids/AFI_DROID_CHARTER.v0.1.md (governing charter)']; downstream=['afi-reactor (consumer / orchestration)', 'afi-ops (consumer per .afi-codex.json)', 'afi-core', 'afi-starters (per README Related Repositories)']

### `afi-gateway`

- **Purpose:** An ElizaOS-based universal gateway / framework: it lets community developers build custom characters with skills, provides AFI-specific Eliza plugins and HTTP/WS clients that call AFI services (afi-reactor Froggy pipeline), and exposes a tenant-scoped HTTP API (api-keys, skills discovery, and a /api/v1/signals ingest endpoint that writes into the TSSD vault).
- **Classification:** REFERENCE_IMPL
- **Rationale:** README.md:3-5 and package.json:3 describe this as "AFI's universal gateway framework for custom character development" / "universal gateway for multiple interfaces and integrations" — an ElizaOS-based external client + character framework. It is the ingest-boundary plane in the five-plane model. It …
- **Touchpoints:** USS/CPJ ingest (referenced, not validated), TSSD/vault (direct writes via afi-infra VaultedSignalRecord), DAG/pipeline (HTTP client to afi-reactor Froggy), schemas (consumes VaultedSignalRecord, AfiScoutSignalDraft), epoch/signalId identity, replay/determinism (skills manifest determinism_required flag; Codex referenced as replay service), SDK/API (api-key auth, rate limiting, skills discovery), mint/receipt (only described in TSSD readiness report, no code)
- **Normative artifacts:**
  - `(none authored here) — gateway consumes afi-infra/src/tssd/types.ts (VaultedSignalRecord) imported at /home/user/AFI-Protocol/afi-gateway/src/http/app.ts:8`
  - `/home/user/AFI-Protocol/afi-gateway/src/afiscout/types/afi-scout-signal.ts (AfiScoutSignalDraft — explicitly NON-canonical draft type)`
  - `/home/user/AFI-Protocol/afi-gateway/src/afiClient.ts:50-80 (ReactorScoredSignalV1 response-contract shape, gateway-side mirror of reactor's contract)`
- **Dependencies:** upstream=['afi-infra (file:../afi-infra — TSSD VaultedSignalRecord types, TenantScopedTSSDVaultClient, MongoTSSDVaultClient, InMemoryTSSDVaultClient)', '@afi/cli-framework (file:../afi-cli-framework)', '@elizaos/core 1.6.4 (external SDK)', 'afi-reactor (runtime HTTP dependency — Froggy /api/webhooks/tradingview, /health, /api/ingest/cpj)', 'afi-config (docs reference: Droid Charter, vault.schema.json, codex governance)', 'afi-skills (skills manifest at ../afi-skills/manifest.json consumed by skillsService)', 'MongoDB (mongodb ^6.21.0)', 'openai (^4.77.3)']; downstream=['End users / community character developers', 'Discord/Telegram bots (dev:discord, dev:telegram scripts)', 'web UI via ElizaOS server-full']

### `afi-governance`

- **Purpose:** Defines the AFI governance/DAO layer: a standardized "Universal Proposal Signal" schema for human/agent governance proposals, agent-validator scoring stubs, a deferred-staking activation threshold, and a hybrid off-chain (Snapshot) -> on-chain (Safe + Zodiac Reality) proposal execution model.
- **Classification:** REFERENCE_IMPL
- **Rationale:** This is the AFI governance/DAO plane, NOT one of the five canonical signal-data planes. README.md:13 "AFI Governance is the agentic decision-making layer of the AFI Protocol." It defines a governance "Universal Proposal Signal" schema plus Snapshot/Safe/Zodiac-Reality execution. Under the North Star…
- **Touchpoints:** registries/reputation (validator registry, deferred staking, agent registry schema), governance proposal lifecycle (submit/score/execute), schemas (UniversalProposalSignal, SignalChallengeProposal, proposal_receipt), SDK/API (Snapshot API, Safe SDK stubs), replay/determinism (mentioned aspirationally only: 'Replayable DAG of proposal analysis' - not implemented), mint/emissions (referenced only via MIN_SUPPLY_FOR_STAKING staking-activation gate, no mint logic)
- **Normative artifacts:**
  - `/home/user/AFI-Protocol/afi-governance/schemas/UniversalProposalSignal.schema.json (governance proposal schema - NOTE: not valid JSON, contains JS comments+prose)`
  - `/home/user/AFI-Protocol/afi-governance/specs/universal_proposal_schema.json (duplicate/source-of-truth for the above, Zenodo lineage)`
  - `/home/user/AFI-Protocol/afi-governance/schemas/SignalChallengeProposal.schema.json (valid draft-07 schema for Snapshot signal-challenge proposals)`
  - `/home/user/AFI-Protocol/afi-governance/codex/proposal_receipt_schema.json (proposal scoring receipt schema)`
  - `/home/user/AFI-Protocol/afi-governance/config/config_staking.ts (MIN_SUPPLY_FOR_STAKING = 1_000_000_000)`
- **Dependencies:** upstream=["afi-config (AGENTS.md:7,108 cites afi-config/codex/governance/droids/AFI_DROID_CHARTER.v0.1.md as global authority; AGENTS.md:81 'validated against afi-config schemas')", 'afi-token / afi-mint (staking gated on AFI minted supply, MIN_SUPPLY_FOR_STAKING)', 'Snapshot.org (off-chain voting, SignalChallengeProposal schema + executor agent)', 'Safe / Zodiac Reality module (on-chain execution layer, external SDKs)']; downstream=["afi-token (AGENTS.md:54 'Consumed by: afi-token, afi-reactor, on-chain governance processes')", 'afi-reactor (AGENTS.md:54 consumer)']

### `afi-infra`

- **Purpose:** afi-infra defines AFI's canonical T.S.S.D. Vault types and lifecycle spec (the off-chain per-signal Evidence-plane record) plus signal-stage Zod schemas, agent-role definitions, and a read-only deterministic replay runner; package.json:3 "Infrastructure services, TSSD vault clients, and shared schemas for AFI Protocol".
- **Classification:** NORMATIVE
- **Rationale:** The brief explicitly names "afi-infra/src/tssd/types.ts" and "TSSD spec" as NORMATIVE artifacts. This repo hosts the canonical VaultedSignalRecord type (src/tssd/types.ts:331), the TSSD_VAULT_SPEC (docs/TSSD_VAULT_SPEC.md) and TSSD_REPLAY_CLI_SPEC.v0.1 (docs/TSSD_REPLAY_CLI_SPEC.v0.1.md) which defin…
- **Touchpoints:** TSSD/vault, replay/determinism, schemas, mint/receipt (referenced, no contract code), DAG/pipeline (mock test only), registries/reputation (validator metadata doc only), SDK/API (ITSSDVaultClient interface)
- **Normative artifacts:**
  - `/home/user/AFI-Protocol/afi-infra/src/tssd/types.ts`
  - `/home/user/AFI-Protocol/afi-infra/docs/TSSD_VAULT_SPEC.md`
  - `/home/user/AFI-Protocol/afi-infra/docs/TSSD_REPLAY_CLI_SPEC.v0.1.md`
  - `/home/user/AFI-Protocol/afi-infra/src/tssd/TSSDVaultClient.ts (ITSSDVaultClient interface, lines 36-69)`
  - `/home/user/AFI-Protocol/afi-infra/schemas/enrichment_common.ts (EnrichmentCategory + EnrichedSignalCore)`
  - `/home/user/AFI-Protocol/afi-infra/schemas/signal_scoring_schema.ts`
  - `/home/user/AFI-Protocol/afi-infra/agent-roles/validator_metadata_v1.md (registries/reputation invariants)`
- **Dependencies:** upstream=['afi-core (package.json:26 "afi-core": "file:../afi-core"; AnalystScoreTemplate is canonical source per types.ts:98; validator_metadata Zod schema lives in afi-core per agent-roles/validator_metadata_v1.md:30)', 'afi-config (AGENTS.md:61 "Depends on: afi-config (schemas)"; Charter authority AGENTS.md:5)', 'mongodb (package.json:27)', 'zod (package.json:28)']; downstream=['afi-reactor (.afi-codex.json:35 dependsOn; README.md:67 DAG orchestrator consumer)', 'afi-core (.afi-codex.json:34 dependsOn; AGENTS.md:60 Consumed by)', 'afi-token (.afi-codex.json:36 dependsOn; receipt/mint integration per TSSD_VAULT_SPEC.md:98)', 'afi-ops (README.md:66; AGENTS.md:60)', 'afi-factory (AGENTS.md:60)']

### `afi-labs`

- **Purpose:** afi-labs is the AFI org's explicitly-experimental private R&D sandbox ("junk drawer for experiments") holding prototypes, PoCs, stub scaffolds, and design-note drafts that are meant to graduate into production repos only after proving stable; it ships no normative protocol artifacts and no real implementation.
- **Classification:** RESEARCH
- **Rationale:** Self-described as experimental: README.md:4-5 "AFI Labs is the experimental playground... Anything that isn't production-ready - prototypes, PoCs, research notebooks, speculative integrations - lives here first." .afi-codex.json:3-4 sets role "Experimental playground for prototypes and PoCs" and sta…
- **Touchpoints:** USS/CPJ ingest (name-only, no schema), TSSD/vault (Mongo-only MVP scaffold, prose), mint/receipt (placeholder/mock only), DAG/pipeline (toy pipeline-runner), schemas (agent registry pydantic + agent_spec template; no canonical AFI schemas), replay/determinism (empty placeholder engine + codex replay_endpoint string), registries/reputation (agent registry servers, ghost/omnichain registry configs), SDK/API (FastAPI registry, Next.js frontend stubs)
- **Dependencies:** upstream=['ElizaOS (proposed signal-processing base, roadmap only)', 'MongoDB Atlas (proposed TSSD store)', 'Vercel/Next.js (proposed frontend)', 'Factory.ai droids / augmentcode (codegen tooling)', 'LayerZero/OFT (proposed bridge, mock only)']; downstream=['afi-core (graduation target per README)', 'afi-agents (graduation target per README)']

### `afi-math`

- **Purpose:** Pure, deterministic, dependency-free TypeScript library of financial/scoring math primitives (time value of money, curve shaping, reverse DCF/implied-rate, signal decay/half-life, and a three-phase emissions schedule) shared across AFI Protocol repos for scoring, tokenomics, and pipeline computation.
- **Classification:** SUPPORTING
- **Rationale:** Pure TypeScript math primitives library with zero deps and no I/O: README.md:5 "a pure TypeScript library providing deterministic mathematical functions for time value of money, curve primitives, valuation models, and signal decay"; AGENTS.md:74 "Depends on: NONE (pure math library...)". It is consu…
- **Touchpoints:** emissions (off-chain schedule/cap computation), replay/determinism (pure deterministic transforms underpinning reproducible scoring), DAG/pipeline (curve/decay transforms consumed by reactor scoring), USS ingest (decay/greeks field mapping, docs-only reference)
- **Dependencies:** upstream=[]; downstream=['afi-reactor', 'afi-core', 'afi-mint', 'afi-token', 'afi-engine (legacy name)', 'afi-token-finalized (legacy name)', 'afi-plugins']

### `afi-mint`

- **Purpose:** Off-chain coordination of signal-driven AFI token minting: an appeal-based validator pipeline (auto qualify/reject by decay score, challenge window, Snapshot dispute voting) that finalizes signals and invokes an on-chain AFIMintCoordinator.mintForSignal() to emit a per-signal mint breadcrumb (signalId, epoch, beneficiary, receiptId).
- **Classification:** REFERENCE_IMPL
- **Rationale:** afi-mint is the off-chain minting *coordination* spine of the reference stack, not a protocol-normative source. package.json:3 "AFI signal validation and token minting coordination"; AGENTS.md:3 "coordinates signal-driven token minting... but does NOT contain token contracts or on-chain economics lo…
- **Touchpoints:** mint/receipt, emissions, replay/determinism, schemas, contracts (stubs), registries/reputation (placeholder), TSSD/vault (interface only), DAG/pipeline (consumer of scored signals), SDK/API (Snapshot GraphQL governance)
- **Normative artifacts:**
  - `/home/user/AFI-Protocol/afi-mint/codex/mint_receipt_schema.json`
  - `/home/user/AFI-Protocol/afi-mint/src/orchestrator/MintExecutor.ts (MintRequest / IMintCoordinatorContract.mintForSignal breadcrumb shape, lines 19-47)`
  - `/home/user/AFI-Protocol/afi-mint/schemas/MintTrigger.schema.ts (MintRequestSchema, lines 11-19)`
  - `/home/user/AFI-Protocol/afi-mint/src/orchestrator/types.ts (SignalValidatorState state machine, lines 33-150)`
  - `/home/user/AFI-Protocol/afi-mint/schemas/SignalValidatorState.schema.ts`
  - `/home/user/AFI-Protocol/afi-mint/src/adapters/EmissionsMintDataProvider.ts (goldpaper emissions formula, lines 50-288)`
- **Dependencies:** upstream=['@afi-protocol/afi-core (peerDependency, validators/schemas; reputation_bridge references afi-core/validators/ValidatorDecision.ts)', '@afi-protocol/afi-infra (peerDependency; reputation_bridge references afi-infra/src/tssd/types.ts)', "afi-math (emissions schedule inlined 'to avoid circular dependency', canonical source afi-math/src/emissions/emissionsSchedule.ts)", 'afi-config (validator config + REGISTRIES_AND_REPUTATION.v0.1.md + AFI_DROID_CHARTER governance)', 'afi-reactor (consumes scored signals via IAnalystScoreFetcher)', 'ethers (peerDependency, optional)', 'Snapshot.org hub/sequencer (external governance API)']; downstream=['afi-token (afi-mint invokes IMintCoordinatorContract.mintForSignal on-chain; AGENTS.md dependency afi-mint -> afi-token)', "afi-ops (deployment; AGENTS.md 'Consumed by: afi-ops')"]

### `afi-ops`

- **Purpose:** afi-ops is a Phase-1 scaffolding operations/devops toolkit providing local-deploy stubs, read-only health-check scripts, operational runbooks/SLO docs, and AgentOps utilities (config hashing, agent versioning, Sentry hooks) for the AFI Protocol reference stack.
- **Classification:** SUPPORTING
- **Rationale:** Repo is a Phase-1 scaffolding-only operations/devops toolkit: local deploy stubs, health-check shell scripts, runbooks, SLO docs, and AgentOps helpers (config hashing, agent versioning, Sentry). It defines no protocol schemas, contracts, lifecycle semantics, or deterministic transforms. package.json…
- **Touchpoints:** TSSD/vault (operationally referenced: env TSSD_VAULT_BACKEND, health checks, SLO freshness/replayability), DAG/pipeline (afi-reactor deploy/health stubs, pipeline config paths), replay/determinism (SLO 'Codex Replayability' target only; no replay artifacts), SDK/API (health endpoints /health on ports 3000/3001), observability (Sentry, telemetry env flags)
- **Dependencies:** upstream=['afi-config (schemas; AGENTS.md:68, Charter authority AGENTS.md:5)', '@sentry/node (package.json:18)', 'afi-core', 'afi-reactor', 'afi-infra', 'afi-plugins (.afi-codex.json:60-65 dependsOn)']; downstream=['Production/staging environments', 'CI/CD pipelines (AGENTS.md:67)']

### `afi-plugins`

- **Purpose:** Central plugin registry and template/stub pack that defines the extension surface (types, manifests, and placeholder implementations for signal generators, analyzers, scorers, validators, executors, observers) for the AFI reference stack (afi-reactor DAG orchestrator and afi-core ElizaOS runtime), with all real logic deferred to runtime/infra repos.
- **Classification:** REFERENCE_IMPL
- **Rationale:** A thin TypeScript scaffolding package (README.md:11 "intentionally thin and lightweight... NOT production logic"; package.json:3 "Plugin registry and template pack for AFI Protocol"). It defines local plugin types and a hardcoded in-memory registry of stub plugins (signal/analyzer/scorer/validator/e…
- **Touchpoints:** DAG/pipeline, replay/determinism (validator stub only), scoring (scorer stub only), SDK/API (plugin registry/types), TSSD/vault (referenced, not implemented), epoch lifecycle (optional context fields)
- **Dependencies:** upstream=['afi-core (schemas/validators, runtime)', 'afi-config (plugin config, AFI_DROID_CHARTER governance)', 'afi-infra (T.S.S.D. Vault client, tssd/types.ts, exchange clients)', 'afi-math (referenced for statistical scoring - scorer README)']; downstream=['afi-reactor (consumes plugin defs as DAG nodes)', 'afi-core (binds eliza-tool plugins)', 'afi-skills (consumes plugin definitions per AGENTS.md)']

### `afi-protocol`

- **Purpose:** A governance/onboarding meta-repo that orchestrates the AFI ("Agentic Financial Intelligence") ecosystem by pointing human contributors and Factory.ai/augmentcode droids at the other AFI repos (afi-core, afi-reactor, afi-config, afi-infra, afi-docs, afi-gateway, afi-ops) via README, an architecture overview, a droid registry, and a contributor manifest.
- **Classification:** DOCS
- **Rationale:** This is a thin meta-repo containing ONLY documentation, governance, and agent-orchestration manifests — zero code, schemas, contracts, or canonical type definitions. package.json self-describes it: "description": "AFI Protocol documentation and specifications" with stub scripts ("build": "echo 'Buil…
- **Touchpoints:** DAG/pipeline (described only, in architecture_overview.md — reactor as 'source of truth'), validators/scoring (described only, afi-core), registries/reputation (mentioned in faq/announcement: reputation, DAO votes, mentor registry), schemas (referenced only as 'persona schemas'/'Codex definitions' pointing at afi-config; none present)
- **Dependencies:** upstream=[]; downstream=['afi-reactor (referenced as DAG source of truth)', 'afi-core (validators/mentors/scoring; agent_manifest entries)', 'afi-infra (signal templates/simulators; agent_manifest entry)', 'afi-config (codex/persona schemas)', 'afi-ops (deployment/health)', 'afi-docs (documentation; ARCHITECTURE_STATUS.md, droid_contributor_guide.md, archive/langgraph-migration-2025)', 'afi-gateway (optional Eliza client)', 'afi-agents (stale, onboarding only)', 'afi-labs (private, onboarding only)']

### `AFI-Protocol/afi-agents`

- **Purpose:** A pre-archival scaffold providing agent/persona definitions plus a yargs CLI wrapper that delegates protocol commands (validate-codex, simulate-signal, invoke-validator, invoke-mentor, run-local-deploy) to sibling repos (afi-config, afi-infra, afi-core, afi-ops), with a demo React SignalValidator UI and an in-memory mentor-pairing registry.
- **Classification:** STALE
- **Rationale:** Repo is ARCHIVED (gh api archived:true), 21 KB, last pushed 2025-07-15, and is one of the stale repo names explicitly flagged in the North Star tension list (afi-agents). README is a one-line stub ("This repository contains the afi-agents module for AFI Protocol"). Content is an early scaffold: a ya…
- **Touchpoints:** USS/CPJ ingest (only as demo mock SignalData, NOT canonical USS), DAG/pipeline (CLI invoke-validator -> afi-core PoIValidator, delegated), schemas (stub-only, schemas/index.ts empty), SDK/API (yargs CLI entry-points / cli_manifest.json), registries/reputation (in-memory mentor_registry only, non-canonical)
- **Dependencies:** upstream=['afi-config (cli_utils/codex_validator)', 'afi-core (cli_hooks/validator_invoker, PoIValidator, MentorRegistry)', 'afi-infra (cli_templates/signal_simulator)', 'afi-ops (scripts/deploy_local.sh)']; downstream=[]

### `afi-reactor`

- **Purpose:** afi-reactor is the reference TypeScript orchestrator that runs a flexible, plugin-based DAG pipeline to ingest (USS v1.1 / CPJ v0.1), enrich, deterministically score, and persist financial signals to a Mongo-backed scored-signal vault, exposing replay/simulation entrypoints.
- **Classification:** REFERENCE_IMPL
- **Rationale:** afi-reactor is a concrete TypeScript implementation of ONE scoring/orchestration spine (the "reference spine" gateway->reactor DAG->vault per North Star). package.json declares `"name": "afi-reactor"` with mongodb, express, zod and `file:../afi-core`/`file:../afi-factory` deps (package.json:1-46). I…
- **Touchpoints:** USS/CPJ ingest, TSSD/vault, DAG/pipeline, schemas, replay/determinism, SDK/API
- **Normative artifacts:**
  - `/home/user/AFI-Protocol/afi-reactor/docs/VALIDATOR_REPLAY_SPEC.v0.1.md`
  - `/home/user/AFI-Protocol/afi-reactor/config/schema.codex.json`
  - `/home/user/AFI-Protocol/afi-reactor/config/dag.codex.json`
  - `/home/user/AFI-Protocol/afi-reactor/src/types/ReactorScoredSignalV1.ts`
  - `/home/user/AFI-Protocol/afi-reactor/src/uss/ussValidator.ts`
  - `/home/user/AFI-Protocol/afi-reactor/src/cpj/cpjValidator.ts`
  - `/home/user/AFI-Protocol/afi-reactor/src/uss/cpjMapper.ts`
  - `/home/user/AFI-Protocol/afi-reactor/src/novelty/canonicalNovelty.ts`
  - … (+1 more)
- **Dependencies:** upstream=['afi-core (file:../afi-core; AnalystScoreTemplate, validators, UWR/PoI logic, scoring formulas)', 'afi-config (USS v1.1 schemas loaded at runtime by ussValidator)', 'afi-factory (file:../afi-factory; AnalystConfig/EnrichmentNodeConfig, template_registry)', 'afi-math (declared in .afi-codex.json dependsOn)', 'afi-plugins (declared in .afi-codex.json dependsOn)']; downstream=['afi-infra (owns canonical vaulted-signal schema + real TSSD persistence; consumes reactor as service)', 'afi-ops (deployment, listed as consumer)', 'afi-gateway (ElizaOS actions call reactor Froggy pipeline via HTTP/WS)', 'afi-mint (receives validated/scored outcomes; minting/emissions explicitly moved out of reactor)', 'afi-token (subscribes to reactor events for emissions per doctrine)']

### `afi-research-site`

- **Purpose:** Public-facing marketing/brochure website (Next.js App Router, Axleo template skin) for the AFI Research Institute, presenting research programs, services, team/careers, blog, and a fiat-only Stripe "Adopt-an-Agent" donation flow; explicitly separate from the AFI Network protocol stack.
- **Classification:** OUT_OF_SCOPE
- **Rationale:** This is a Next.js marketing/brochure website built on the purchased "Axleo" ThemeForest template (package.json name "axleo-next", README:3 "AFI Research Institute website (Next.js), adapted from the Axleo template"). It is the public portal for research programs, services, team, blog, and a fiat-onl…

### `afi-sdk-python`

- **Purpose:** Intended official Python SDK for building on AFI Protocol (signal submission/validation helpers, agent integration, ML/AI integration), but currently an empty scaffold with only README and pyproject.toml — no implementation exists.
- **Classification:** STALE
- **Rationale:** Repository contains only README.md and pyproject.toml with no source code, package, schemas, contracts, or tests. The afi_sdk package referenced in README usage examples does not exist. README Status line states "New repository created during multi-repo reorganization (2025-11-14)" and the single gi…
- **Touchpoints:** USS/CPJ ingest (aspirational only: 'Signal submission and validation helpers'), SDK/API (intended client surface, not implemented)
- **Dependencies:** upstream=['afi-reactor (named as API client target in README.md:11; not declared as a code dependency)']; downstream=[]

### `afi-sdk-ts`

- **Purpose:** Intended (currently unimplemented) official TypeScript/JavaScript SDK for building on AFI Protocol (README.md:3 "TypeScript SDK for AFI Protocol"; package.json:3).
- **Classification:** STALE
- **Rationale:** Repo contains only README.md and package.json with a single git commit "chore: initialize new repository" (c770140). No src/, schemas, contracts, or tests. README.md:43 states it is a "New repository created during multi-repo reorganization (2025-11-14)". package.json:6 points main to ./dist/index.j…
- **Touchpoints:** SDK/API (aspirational only, no code), USS/CPJ ingest (implied by README 'Signal submission and validation helpers' but NOT implemented)

### `afi-skills`

- **Purpose:** A canonical, versioned library of AFI agent "skills" -- discrete reusable capabilities defined as markdown + YAML front-matter (typed I/O, risk level, determinism flag, golden evals) with TS tooling (Zod schema, linter, manifest builder) and agent skillsets, consumed by afi-core/afi-reactor/afi-factory.
- **Classification:** SUPPORTING
- **Rationale:** This is a versioned library of agent "skills" (markdown docs with YAML front-matter describing typed I/O, risk levels, determinism flags, and golden eval cases), plus TypeScript tooling (Zod schema, linter, manifest builder) and agent skillsets. README.md:28 calls it "the canonical source of truth f…
- **Touchpoints:** TSSD/vault (tool token tssd:read only; vault-replay-determinism skill), mint/receipt (receipt-verification skill; epoch-pulse-emissions skill), emissions (epoch-pulse-emissions skill describes proportional distribution, supply cap, decay), replay/determinism (vault-replay-determinism skill, codex:replay tool, determinism_required flag, golden cases), DAG/pipeline (referenced only as out-of-scope: orchestration belongs to afi-reactor), schemas (own skill front-matter Zod schema + skill_contract_v1; NOT USS/CPJ/vault/pipeline schemas), registries/reputation (signal-scoring-core describes reputation scoring inputs), SDK/API (skill manifest/index consumed by agent runtimes)
- **Normative artifacts:**
  - `/home/user/AFI-Protocol/afi-skills/docs/skill_contract_v1.md (AFI Skill Contract v1.0, status Locked -- canonical for skill front-matter only, scoped to this repo)`
  - `/home/user/AFI-Protocol/afi-skills/scripts/shared/frontmatter-schema.ts (Zod SkillFrontMatterSchema enforcing the contract)`
  - `/home/user/AFI-Protocol/afi-skills/scripts/shared/risk-patterns.ts (security risk pattern set used in PR gating)`
- **Dependencies:** upstream=['afi-config (declared dependsOn in .afi-codex.json:15; AGENTS.md/Charter authority afi-config/codex/governance/droids/AFI_DROID_CHARTER.v0.1.md)']; downstream=['afi-core (loads skills at runtime)', 'afi-reactor (uses skills in DAG nodes)', 'afi-factory (references skills in agent templates)', 'afi-docs (generates public documentation)', 'afi-evals (runs golden case validation)']

### `afi-starters`

- **Purpose:** Provides clone-and-extend starter templates and a self-hosted deployment kit (Docker/compose + Fly/Render/Railway manifests) so developers and agents can quickly bootstrap AFI-compatible projects, currently containing only a "self-hosted-pipeline" starter that stands up an afi-gateway + afi-reactor + MongoDB stack.
- **Classification:** SUPPORTING
- **Rationale:** This repo is a developer-onboarding scaffold collection, not a protocol authority. README.md:1-3 "Starter templates and boilerplates for AFI Protocol"; package.json:3 description matches; AGENTS.md:28 "This repo contains templates only, not runnable applications" and AGENTS.md:35 "Do not add product…
- **Touchpoints:** DAG/pipeline (reactor enrichmentNodes configs + Pipehead plugin template), TSSD/vault (Mongo persistence env vars only, no schema), SDK/API (gateway server referenced as deploy target; README mentions afi-sdk-ts/afi-sdk-python starters not yet present)
- **Dependencies:** upstream=['afi-gateway (Dockerfile clones GATEWAY_REPO; runs dist/src/server-full.js)', 'afi-reactor (Dockerfile clones REACTOR_REPO; runs dist/src/server.js; plugin template imports afi-reactor/src/types/dag.js)', 'afi-skills (Dockerfile clones SKILLS_REPO for manifest.json)', 'afi-config (AGENTS.md cites afi-config/codex/governance/droids/AFI_DROID_CHARTER.v0.1.md as global authority)']; downstream=['Developers/agents who fork starters', "afi-factory (AGENTS.md:48 'Consumed by: ... afi-factory (for agent instantiation)')"]

### `afi-tiny-brains`

- **Purpose:** A FastAPI microservice exposing POST /predict/froggy that runs a three-brain ensemble (Chronos time-series, HMM regime, LightGBM meta-learner) over Froggy enrichment context and returns a FroggyAiMlV1 prediction (convictionScore/direction/regime/riskFlag/notes), with heuristic fallbacks so it never errors.
- **Classification:** REFERENCE_IMPL
- **Rationale:** A self-contained Python/FastAPI AI/ML microservice ("Tiny Brains") that provides ML enrichment predictions for the Froggy lane and is explicitly invoked by the reference spine (afi-reactor) over HTTP. README.md:3 "AFI's AI/ML microservice for Froggy enrichment pipeline"; README.md:11 "This service i…
- **Touchpoints:** DAG/pipeline (Froggy enrichment scoring transform), SDK/API (HTTP /predict/froggy contract), replay/determinism (model versions/seeds at inference not pinned in outputs)
- **Dependencies:** upstream=['afi-reactor (HTTP caller via src/aiMl/tinyBrainsClient.ts; provides run scripts/.env config)', 'afi-core (source of FroggyAiMlV1 type definition)']; downstream=[]

### `afi-token`

- **Purpose:** afi-token implements the AFI Protocol's on-chain Commitment plane on BASE: an xERC20-based ERC-20 emissions token (AFIToken, 86B hard cap), an ERC-1155 provenance receipt (AFISignalReceipt), and an AFIMintCoordinator orchestrator that links token+receipt mints to off-chain signal/epoch metadata via the MintCoordinated event.
- **Classification:** REFERENCE_IMPL
- **Rationale:** The repo's Solidity contracts (src/*.sol) are listed in the North Star as NORMATIVE commitment-plane artifacts, yet the repo as a whole is a concrete BASE/xERC20/Foundry reference deployment with a SPECIFIC stack (defi-wonderland xERC20, OpenZeppelin AccessControl, single Treasury Safe role pattern)…
- **Touchpoints:** mint/receipt, emissions, contracts, schemas, registries/reputation, replay/determinism, DAG/pipeline
- **Normative artifacts:**
  - `/home/user/AFI-Protocol/afi-token/src/AFIToken.sol`
  - `/home/user/AFI-Protocol/afi-token/src/AFIMintCoordinator.sol`
  - `/home/user/AFI-Protocol/afi-token/src/AFISignalReceipt.sol`
  - `/home/user/AFI-Protocol/afi-token/script/DeployAFITokenMainnet.s.sol`
- **Dependencies:** upstream=['afi-xerc20 (lib/xERC20 submodule, branch afi-oz-v5-compat)', 'openzeppelin-contracts', 'forge-std', 'afi-config (AFI_DROID_CHARTER governance authority)']; downstream=['afi-mint (consumes contracts; .droid.json: integrate with afi-mint mint_trigger.ts; calls EMISSIONS_ROLE on coordinator)', 'afi-governance (Epoch Pulse, role evolution)', 'afi-ops (deployment)']

### `afi-xerc20`

- **Purpose:** A vendored fork of the defi-wonderland/xERC20 (Connext xTokens) Solidity standard providing a cross-chain bridged-token implementation (XERC20, XERC20Lockbox, XERC20Factory) with per-bridge rate-limited mint/burn, patched only for OpenZeppelin v5 Ownable compatibility so it can compile alongside AFI Protocol contracts.
- **Classification:** OUT_OF_SCOPE
- **Rationale:** This is a vendored fork of the third-party defi-wonderland/xERC20 (Connext xTokens) cross-chain bridged-token standard, not an AFI protocol artifact. package.json identifies it: name 'xerc20', homepage 'https://github.com/defi-wonderland/xERC20#readme', repository 'git+https://github.com/defi-wonder…
- **Touchpoints:** contracts (generic XERC20 bridge token, NOT AFI mint/receipt), potentially upstream of mint/commitment plane only by reuse of OZ v5 toolchain (no direct AFI mint logic)
- **Dependencies:** upstream=['@openzeppelin/contracts (lib/openzeppelin-contracts, branch v4.9.3 per .gitmodules but patched for v5 per commit 305922f)', 'isolmate (defi-wonderland, CREATE3)', 'forge-std / ds-test / prb-test (test harness)', 'permit2 (Uniswap)']; downstream=['AFI commitment/mint layer (afi-token / afi-mint) MAY consume this xERC20 standard for a cross-chain bridgeable AFI token; relationship is implied only by the OZ-v5 patch commit message, no code import exists in this repo']

## Mandatory-Stack Implication Catalog

Code/docs implying Mongo, reactor, or org infra is **mandatory** (not merely default).

| Repo | Path | Quote |
|------|------|-------|
| `.github` | `profile/README.md` | afi-reactor – Signal DAG / orchestrator, Codex integration, replay. |
| `afi-config` | `/home/user/AFI-Protocol/afi-config/codex/governance/droids/AFI_DROID_CHARTER.v0.1.md:117` | **`afi-reactor`** is the orchestrator; do not reintroduce or reference `afi-engine`. |
| `afi-config` | `/home/user/AFI-Protocol/afi-config/schemas/pipeline.schema.json:5` | Schema for signal processing pipeline configurations in afi-reactor |
| `afi-config` | `/home/user/AFI-Protocol/afi-config/schemas/analyst-config.schema.json:5` | Schema for analyst configurations in the AFI-Reactor pipeline / DAG integration. |
| `afi-config` | `/home/user/AFI-Protocol/afi-config/schemas/definitions/enrichment-node.schema.json:5` | Enrichment nodes are processing units that transform, analyze, or augment signals within the AFI-Reactor pipeline / DAG. |
| `afi-config` | `/home/user/AFI-Protocol/afi-config/docs/AFI_CONFIG_OVERVIEW.md:33` | ### afi-reactor (DAG Orchestrator) |
| `afi-core` | `/home/user/AFI-Protocol/afi-core/docs/AFI_CORE_RUNTIME_OVERVIEW.md:39` | AFI-Reactor (already hardened) is the **canonical orchestrator** for AFI Protocol. |
| `afi-core` | `/home/user/AFI-Protocol/afi-core/docs/AFI_CORE_RUNTIME_OVERVIEW.md:29` | DAG Topology / Policy - That's afi-reactor (15-node DAG, pipeline definitions, orchestration rules) |
| `afi-core` | `/home/user/AFI-Protocol/afi-core/.factory/droids/schema-validator-droid.md:91` | afi-reactor is the orchestrator of AFI — afi-core is NOT an orchestrator. |
| `afi-core` | `/home/user/AFI-Protocol/afi-core/.afi-codex:3` | ElizaOS-based runtime layer for AFI, bridging AFI-Reactor DAG plans to agents and mint instructions |
| `afi-docs` | `AFI_ORCHESTRATOR_DOCTRINE.md:11` | ### 1. afi-reactor is the orchestrator of AFI All canonical pipelines, DAGs, and routing logic live here—not in afi-core, not in random helpers. |
| `afi-docs` | `AFI_ORCHESTRATOR_DOCTRINE.md:3-5` | Repository: afi-reactor  Purpose: Canonical orchestration principles for AFI Protocol  Status: Authoritative |
| `afi-docs` | `AFI_ORCHESTRATOR_DOCTRINE.md:39` | ### 3. The DAG is law Every signal path (ingest → enrich → score → mint/review) must be expressible as a Reactor DAG; ad-hoc flows are anti-patterns. |
| `afi-docs` | `AFI_PIPELINE_AUDIT_REPORT.md:16` | - ✅ MongoDB TSSD vault persistence (Phase 1 complete) |
| `afi-docs` | `AFI_PIPELINE_AUDIT_REPORT.md:41` | `afi-infra` — TSSD vault (MongoDB), types, schemas |
| `afi-docs` | `AFI_System_Atlas.md:18` | afi-reactor: TSSD vault persistence via src/services/tssdVaultService.ts; writes canonical USS + pipeline outputs when AFI_MONGO_URI configured |
| `afi-factory` | `afi-factory/schemas/index.ts:5` | bridging afi-config schemas with afi-reactor orchestration. |
| `afi-factory` | `afi-factory/README.md:27` | ❌ Agent orchestration (→ `afi-reactor`) |
| `afi-factory` | `afi-factory/.afi-codex.json:20-23` | "consumers": [ "afi-reactor", "afi-ops" ] |
| `afi-gateway` | `src/services/vaultFactory.ts:7-22` | function baseMongoConfig(): MongoTSSDVaultClientConfig { const mongoUri = process.env.AFI_TSSD_MONGODB_URI // ... dbName: ... 'afi_tssd', collectionName: ... 'tssd_signals' } |
| `afi-gateway` | `src/services/vaultFactory.ts:24-33` | export function createVaultFactoryFromEnv(): VaultFactory { const config = baseMongoConfig(); ... new TenantScopedTSSDVaultClient({ tenantId, ...config }) } |
| `afi-gateway` | `src/lib/db/mongo.ts:43-52` | const uri = process.env.MONGODB_URI; if (!uri) { ... throw new Error("MONGODB_URI environment variable is required"); } |
| `afi-infra` | `/home/user/AFI-Protocol/afi-infra/docs/TSSD_VAULT_SPEC.md:98` | The TSSD Vault lives off-chain (e.g. in MongoDB time-series collections), while on-chain receipts ... provide a lightweight, immutable breadcrumb. |
| `afi-infra` | `/home/user/AFI-Protocol/afi-infra/docs/TSSD_VAULT_SPEC.md:133` | ### Future: Mongo-Backed Implementation A production-ready `MongoTSSDVaultClient` will: Leverage MongoDB time-series collections... |
| `afi-infra` | `/home/user/AFI-Protocol/afi-infra/src/tssd/TSSDVaultClient.ts:197` | if (isProd) { throw new Error("[TSSD] AFI_TSSD_MONGODB_URI is required in production. Falling back to in-memory is not allowed."); } |
| `afi-infra` | `/home/user/AFI-Protocol/afi-infra/docs/TSSD_REPLAY_CLI_SPEC.v0.1.md:24` | It should only talk to TSSD (Mongo) for reads, local scoring/analysis code, and optionally dedicated replay/audit collections. |
| `afi-labs` | `docs/specs/vercel_mongo_scaffold.md` | # Vercel + MongoDB MVP Starter (AFI Protocol) ... /lib/tssd.ts — Logic to write to timeseries collection ... db.createCollection("tssd", { timeseries: ... }) |
| `afi-labs` | `docs/plans/afi_mvp_what_to_stub_vs_build.md` | ## Build Now - Signal submission (API) - MongoDB T.S.S.D. write with timeseries schema |
| `afi-labs` | `docs/plans/afi_mvp_roadmap.md` | [ ] Store signal in MongoDB (timeseries with metadata) ... [ ] Create timeseries collections in MongoDB for T.S.S.D. |
| `afi-labs` | `code-sandbox/agents/registry/agent_registry_server_mongo.py` | MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017") ... app = FastAPI(title="AFI Agent Registry API with MongoDB") |
| `afi-mint` | `/home/user/AFI-Protocol/afi-mint/AGENTS.md` | afi-reactor = signal orchestration (DAG pipeline, signal scoring); afi-mint = signal consumption ... Dependency direction: afi-mint -> afi-reactor (never reverse) |
| `afi-ops` | `configs/env.template:40-44` | # Vault backend: "memory" or "mongodb" TSSD_VAULT_BACKEND=memory # MongoDB collection for T.S.S.D. Vault (if backend=mongodb) TSSD_VAULT_COLLECTION=tssd_signals |
| `afi-ops` | `.afi-codex.json:93-100` | "external": [ { "name": "mongodb", "description": "MongoDB database", "defaultPort": 27017, "required": true } ] |
| `afi-ops` | `scripts/run-local-deploy.sh:105` | print_warn "Assumes local MongoDB at mongodb://localhost:27017/afi" |
| `afi-ops` | `configs/env.template:20-24` | # MongoDB connection string MONGODB_URI=mongodb://localhost:27017/afi # MongoDB database name MONGODB_DATABASE=afi |
| `afi-ops` | `configs/docker-compose.local.yml.template:11-19` | services:   # MongoDB Database   mongodb:     image: mongo:7     container_name: afi-mongo ... MONGO_INITDB_DATABASE: afi |
| `afi-ops` | `README.md:41` | - **afi-reactor** - DAG orchestrator |
| `afi-ops` | `README.md:285-288` | - afi-core - ElizaOS runtime layer ... afi-reactor - DAG orchestrator ... afi-infra - Infrastructure services |
| `afi-plugins` | `afi-plugins/README.md:7-9` | It serves as the canonical extension surface for: - afi-reactor (DAG orchestrator) - afi-core (ElizaOS runtime layer) |
| `afi-plugins` | `afi-plugins/docs/AFI_PLUGINS_OVERVIEW.md:5` | the canonical extension surface for afi-reactor (DAG orchestrator) and afi-core (ElizaOS runtime layer). |
| `afi-plugins` | `afi-plugins/src/types/plugin.ts:22-26` | export type RuntimeTarget = / "afi-reactor" / "afi-core" / "eliza-tool" / "hybrid"; |
| `afi-plugins` | `afi-plugins/AGENTS.md:144-145` | afi-plugins MUST NOT modify DAG structure or orchestration logic. Dependency direction: afi-reactor -> afi-plugins (reactor consumes plugins) |
| `afi-protocol` | `architecture_overview.md:23` | / **Reactor**    / DAG orchestration (source of truth)       / `afi-reactor` / |
| `afi-protocol` | `architecture_overview.md:6` | **Canonical orchestration status:** AFI Reactor uses a **custom deterministic TypeScript DAG** (`afi-reactor/src/dag/`), not LangChain/LangGraph. |
| `afi-reactor` | `/home/user/AFI-Protocol/afi-reactor/README.md` | **afi-reactor is the ONLY orchestrator in AFI Protocol.** All canonical pipelines, DAGs, and routing logic live here. |
| `afi-reactor` | `/home/user/AFI-Protocol/afi-reactor/docs/AFI_ORCHESTRATOR_DOCTRINE.md` | ### 3. The DAG is law Every signal path (ingest → enrich → score → mint/review) must be expressible as a Reactor DAG; ad-hoc flows are anti-patterns. |
| `afi-reactor` | `/home/user/AFI-Protocol/afi-reactor/AGENTS.md` | **afi-reactor** is the canonical DAG orchestrator for AFI Protocol... This is the **ONLY orchestrator** in the AFI ecosystem—agents are nodes, not orchestrators. |
| `afi-reactor` | `/home/user/AFI-Protocol/afi-reactor/src/services/tssdVaultService.ts` | Provides MongoDB persistence for scored signals from AFI Reactor. ... AFI_MONGO_URI: MongoDB connection string (required) |
| `afi-reactor` | `/home/user/AFI-Protocol/afi-reactor/config/dag.codex.json` | "description": "Stores approved signals in the MongoDB T.S.S.D. Vault." |
| `afi-reactor` | `/home/user/AFI-Protocol/afi-reactor/config/schema.codex.json` | "meta": { "bsonType": "object", "required": ["signalId", "timestamp", "score"] ...} (vaulted-signal schema expressed only as MongoDB BSON) |
| `afi-sdk-python` | `/home/user/AFI-Protocol/afi-sdk-python/README.md:11` | - Pythonic API clients for afi-reactor |
| `afi-sdk-ts` | `/home/user/AFI-Protocol/afi-sdk-ts/README.md:11` | Type-safe API clients for afi-reactor |
| `afi-skills` | `/home/user/AFI-Protocol/afi-skills/AGENTS.md:55` | Consumed by: afi-core (loads skills at runtime), afi-reactor (uses skills in DAG nodes), afi-factory (references skills in agent templates) |
| `afi-starters` | `self-hosted-pipeline/docker-compose.yml:4-10` | services:   mongo:     image: mongo:7     ... volumes:       - mongo_data:/data/db |
| `afi-starters` | `self-hosted-pipeline/.env.example:1-4` | # Core persistence AFI_TSSD_MONGODB_URI=mongodb://mongo:27017 AFI_TSSD_DB_NAME=afi_tssd AFI_TSSD_COLLECTION=tssd_signals |
| `afi-starters` | `self-hosted-pipeline/render.yaml:24-27` | databases:   - name: afi-mongo     databaseName: afi_tssd     ipAllowList: [] |
| `afi-starters` | `self-hosted-pipeline/Dockerfile:2-3` | ARG GATEWAY_REPO=https://github.com/AFI-Protocol/afi-gateway.git ARG REACTOR_REPO=https://github.com/AFI-Protocol/afi-reactor.git |
| `afi-starters` | `self-hosted-pipeline/plugins/custom.plugin.ts:1-2` | // Custom enrichment plugin template compatible with afi-reactor Pipehead interface import type { Pipehead, PipelineState } from "afi-reactor/src/types/dag.js"; |
| `afi-tiny-brains` | `README.md:11` | This service is called by `afi-reactor` via the Tiny Brains client (`src/aiMl/tinyBrainsClient.ts`) when Froggy enrichment has `aiMl.enabled = true`. |
| `afi-tiny-brains` | `README.md:120` | X-AFI-Client: afi-reactor-froggy-v1 |
