# AFI Docs Readiness Report

Template applied uniformly across all detected repositories in `/Users/secretservice/AFI_Modular_Repos`. Identity/purpose pulled from README first line when available; otherwise inferred from structure. Confidence reflects inspection depth (mostly surface-level due to breadth).

---

## ElizaOS_Ext_Ref
- Identity: External reference assets (no README found).
- Documentable today: Directory listing only.
- Existing docs: none detected.
- Entry points: unknown.
- Public surfaces: none identified.
- Missing pieces: README and purpose description.
- Doc confidence: Low.
- Best Mintlify placement: Appendix > External References.

## Spartan_reference
- Identity: Reference materials (no README found).
- Documentable today: Directory listing only.
- Existing docs: none detected.
- Entry points: unknown.
- Public surfaces: none identified.
- Missing pieces: README/purpose.
- Doc confidence: Low.
- Best Mintlify placement: Appendix > Reference Packs.

## _archived
- Identity: Archived content (no README found).
- Documentable today: Folder exists; contents need review.
- Existing docs: none detected.
- Entry points: n/a.
- Public surfaces: n/a.
- Missing pieces: Index of archived items.
- Doc confidence: Low.
- Best Mintlify placement: Appendix > Archives.

## afi-artifacts
- Identity: AFI Artifacts — paper reproducibility bundle (`afi-artifacts/README.md`).
- Documentable today: Repro bundles, likely scripts/config for papers.
- Existing docs: README present.
- Entry points: check package scripts if present (package.json exists).
- Public surfaces: artifacts bundle definitions.
- Missing pieces: Explicit how-to-reproduce guide.
- Doc confidence: Medium.
- Best Mintlify placement: Research > Artifacts & Repro Bundles.

## afi-assets
- Identity: Asset pack (`afi-assets/README.md`).
- Documentable today: Node/TS project structure.
- Existing docs: README present.
- Entry points: package scripts (package.json).
- Public surfaces: asset manifests.
- Missing pieces: API/usage guide.
- Doc confidence: Medium.
- Best Mintlify placement: Platform > Asset Pipeline.

## afi-benchkit
- Identity: AFI BenchKit (`afi-benchkit/README.md`).
- Documentable today: Python bench/eval toolkit.
- Existing docs: README present.
- Entry points: python modules/scripts.
- Public surfaces: eval harnesses, datasets (needs deep pass).
- Missing pieces: CLI/API reference.
- Doc confidence: Medium.
- Best Mintlify placement: Evaluation > BenchKit.

## afi-config
- Identity: AFI config and schemas (`afi-config/README.md`).
- Documentable today: USS schemas (`schemas/`), examples (`examples/`), templates.
- Existing docs: README, docs/, codex content.
- Entry points: schema files, possibly CLI utils.
- Public surfaces: USS v1.1 schemas, examples.
- Missing pieces: cross-repo linkage notes.
- Doc confidence: High.
- Best Mintlify placement: Specs > Schemas & Config.

## afi-core
- Identity: AFI Core (`afi-core/README.md`).
- Documentable today: Core validators/analysis libs (Node/TS).
- Existing docs: README, docs/.
- Entry points: package exports, scripts.
- Public surfaces: core APIs, scoring modules.
- Missing pieces: Up-to-date module reference.
- Doc confidence: Medium.
- Best Mintlify placement: Core > Engine & Validators.

## afi-docs
- Identity: AFI Protocol Documentation (`afi-docs/README.md`).
- Documentable today: Primary docs repository.
- Existing docs: docs/ expected; README present.
- Entry points: build scripts if present.
- Public surfaces: published docs.
- Missing pieces: Sync plan with other repos.
- Doc confidence: Medium.
- Best Mintlify placement: Docs Ops > Site Source.

## afi-econ
- Identity: afi-econ-kit (`afi-econ/README.md`).
- Documentable today: Mixed Node/Python econ tooling.
- Existing docs: README present.
- Entry points: package scripts / python modules.
- Public surfaces: econ models, notebooks (needs review).
- Missing pieces: Integration guidance with scoring.
- Doc confidence: Medium.
- Best Mintlify placement: Research > Econ Models.

## afi-gateway
- Identity: AFI ↔ Eliza gateway (`afi-gateway/README.md`).
- Documentable today: Eliza agent runtime, AFI reactor actions plugin, OpenAI models plugin.
- Existing docs: README, docs/ (multiple guides), .env.example.
- Entry points: `src/server-full.ts`, `src/index.ts`, package scripts.
- Public surfaces: HTTP endpoints (health/ping), Eliza actions, AFI reactor client.
- Missing pieces: Production hardening notes.
- Doc confidence: High.
- Best Mintlify placement: Agents > Eliza Gateway.

## afi-factory
- Identity: AFI-Factory (`afi-factory/README.md`).
- Documentable today: Node/TS structure.
- Existing docs: README present.
- Entry points: package scripts.
- Public surfaces: factory modules (needs review).
- Missing pieces: API reference.
- Doc confidence: Medium.
- Best Mintlify placement: Platform > Factory.

## afi-governance
- Identity: AFI Governance (`afi-governance/README.md`).
- Documentable today: Governance flows, likely contracts/config.
- Existing docs: README present.
- Entry points: package scripts.
- Public surfaces: governance specs (needs deeper pass).
- Missing pieces: Proposal lifecycle docs.
- Doc confidence: Medium.
- Best Mintlify placement: Governance > Protocol Governance.

## afi-infra
- Identity: afi-infra (`afi-infra/README.md`).
- Documentable today: Infra tooling/services (Node/TS).
- Existing docs: README present.
- Entry points: package scripts.
- Public surfaces: infra services/components.
- Missing pieces: Deployment runbooks.
- Doc confidence: Medium.
- Best Mintlify placement: Infrastructure > Services & Ops.

## afi-labs
- Identity: AFI Labs (`afi-labs/README.md`).
- Documentable today: Solidity-focused experiments.
- Existing docs: README present.
- Entry points: solidity build/test scripts (check package if present).
- Public surfaces: contracts (needs review).
- Missing pieces: Network/deployment details.
- Doc confidence: Medium.
- Best Mintlify placement: Labs > Experimental Contracts.

## afi-math
- Identity: AFI Math (`afi-math/README.md`).
- Documentable today: Math primitives in Node/TS.
- Existing docs: README present.
- Entry points: package scripts.
- Public surfaces: math libs/functions.
- Missing pieces: Formula references and usage examples.
- Doc confidence: Medium.
- Best Mintlify placement: Research > Math Primitives.

## afi-mint
- Identity: AFI Mint – Signal-Driven Token Minting Pipeline (`afi-mint/README.md`).
- Documentable today: Node/TS + Solidity minting flow.
- Existing docs: README present.
- Entry points: package scripts.
- Public surfaces: contracts, mint pipeline modules.
- Missing pieces: End-to-end flow docs.
- Doc confidence: Medium.
- Best Mintlify placement: Tokenomics > Minting Pipeline.

## afi-ops
- Identity: AFI Ops (`afi-ops/README.md`).
- Documentable today: Operational tooling (Node/TS).
- Existing docs: README present.
- Entry points: package scripts.
- Public surfaces: ops scripts.
- Missing pieces: Runbooks per environment.
- Doc confidence: Medium.
- Best Mintlify placement: Operations > Tooling.

## afi-plugins
- Identity: afi-plugins (`afi-plugins/README.md`).
- Documentable today: Plugin packages.
- Existing docs: README present.
- Entry points: package scripts.
- Public surfaces: plugin exports.
- Missing pieces: Catalog with compatibility matrix.
- Doc confidence: Medium.
- Best Mintlify placement: Developers > Plugin SDK.

## afi-protocol
- Identity: AFI Protocol meta-repo (`afi-protocol/README.md`).
- Documentable today: Meta coordination assets.
- Existing docs: README present.
- Entry points: package scripts (if any).
- Public surfaces: overarching specs.
- Missing pieces: Cross-repo linkage map.
- Doc confidence: Medium.
- Best Mintlify placement: Overview > Protocol Meta.

## afi-reactor
- Identity: AFI-Reactor (`afi-reactor/README.md`).
- Documentable today: TradingView→USS v1.1→DAG pipeline; HTTP server; vault persistence.
- Existing docs: README, docs/ (many), server docs.
- Entry points: `src/server.ts`, pipeline config `src/config/froggyPipeline.ts`, service `src/services/froggyDemoService.ts`.
- Public surfaces: endpoints (/api/webhooks/tradingview, /api/ingest/cpj, /demo/afi-eliza-demo), schemas via afi-config, plugins.
- Missing pieces: Production hardening vs demo defaults.
- Doc confidence: High.
- Best Mintlify placement: Pipeline > Reactor.

## afi-research-site
- Identity: AFI Research Site (`afi-research-site/README.md`).
- Documentable today: Web site code (Node/TS).
- Existing docs: README present.
- Entry points: package scripts.
- Public surfaces: site content.
- Missing pieces: Deploy instructions.
- Doc confidence: Medium.
- Best Mintlify placement: Research > Site.

## afi-sdk-python
- Identity: afi-sdk-python (`afi-sdk-python/README.md`).
- Documentable today: Python SDK.
- Existing docs: README present.
- Entry points: python modules/CLI (if any).
- Public surfaces: SDK APIs.
- Missing pieces: API reference and examples.
- Doc confidence: Medium.
- Best Mintlify placement: SDKs > Python.

## afi-sdk-ts
- Identity: afi-sdk-ts (`afi-sdk-ts/README.md`).
- Documentable today: TypeScript SDK.
- Existing docs: README present.
- Entry points: package scripts.
- Public surfaces: SDK exports.
- Missing pieces: Usage guides.
- Doc confidence: Medium.
- Best Mintlify placement: SDKs > TypeScript.

## afi-skills
- Identity: AFI Skills Library (`afi-skills/README.md`).
- Documentable today: Skills modules.
- Existing docs: README present.
- Entry points: package scripts.
- Public surfaces: skill exports.
- Missing pieces: Skill catalog and examples.
- Doc confidence: Medium.
- Best Mintlify placement: Developers > Skills Library.

## afi-starters
- Identity: afi-starters (`afi-starters/README.md`).
- Documentable today: Starter templates.
- Existing docs: README present.
- Entry points: package scripts.
- Public surfaces: template projects.
- Missing pieces: Updated starter matrix.
- Doc confidence: Medium.
- Best Mintlify placement: Getting Started > Starters.

## afi-tiny-brains
- Identity: Tiny Brains Service (`afi-tiny-brains/README.md`).
- Documentable today: Python service for AI/ML.
- Existing docs: README present.
- Entry points: python modules/scripts.
- Public surfaces: service APIs (needs review).
- Missing pieces: Deployment + API reference.
- Doc confidence: Medium.
- Best Mintlify placement: AI/ML > Tiny Brains Service.

## afi-token
- Identity: AFI Token Protocol (`afi-token/README.md`).
- Documentable today: Node/TS + Solidity token mechanics.
- Existing docs: README present.
- Entry points: package scripts.
- Public surfaces: contracts, token flows.
- Missing pieces: Emissions/receipt linkage docs.
- Doc confidence: Medium.
- Best Mintlify placement: Tokenomics > Token Protocol.

## augmentcode_rules
- Identity: Augment code rules/config (no README found).
- Documentable today: Config files.
- Existing docs: none detected.
- Entry points: n/a.
- Public surfaces: n/a.
- Missing pieces: README and usage.
- Doc confidence: Low.
- Best Mintlify placement: Dev Tools > Coding Rules.

## scripts
- Identity: Shared scripts folder (no README found).
- Documentable today: Script files (needs review).
- Existing docs: none detected.
- Entry points: script files themselves.
- Public surfaces: n/a.
- Missing pieces: Index of scripts and purpose.
- Doc confidence: Low.
- Best Mintlify placement: Dev Tools > Scripts.
