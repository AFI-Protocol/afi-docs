# AFI Protocol — Full Architecture

AFI is an open protocol for turning trading **signals** into **scored, auditable, replayable evidence**. A submission is authenticated at a boundary, validated against a canonical schema, scored by an analyst-configured pipeline of deterministic components, and written once to a canonical evidence store keyed by a stable signal identifier. Authority over what is canonical lives in a small set of governance, contract, and mathematics repositories; everything that executes is a replaceable implementation that must conform to those contracts.

This document describes AFI **as it exists now** — its authority boundaries, its implemented runtime, its authoring and research surfaces, and its known gaps. It is documentation: it explains authority and does not hold it. Where this document and a governed artifact disagree, the governed artifact wins.

---

## Status vocabulary

Every capability below carries one of these tags. They are not synonyms.

| Tag | Meaning |
|---|---|
| **Governed** | An accepted decision in `afi-governance` establishes it as a protocol requirement. |
| **Implemented** | Code exists on a current default branch and tests support the claim. |
| **Deployed** | A running environment or on-chain deployment is proven. |
| **Research** | An experimental or benchmark surface, not runtime law. |
| **Reference** | A governed or technical reference surface not used in the production path. |
| **Reserved** | Named future scope with no current implementation. |
| **Not implemented** | Absent from the current live architecture. |

A governed requirement is not automatically implemented; implemented code is not automatically deployed; documentation is never authority.

---

## The organization

The AFI organization is exactly **18 repositories** — 17 public and 1 private. They fall into five roles.

| Repository | Current role | Authority status | Runtime status |
|---|---|---|---|
| **afi-governance** | Accepted protocol decisions (`decisions/`) | Normative — protocol law | Not runtime |
| **afi-config** | Canonical schemas, registries, conventions, KATs | Normative — canonical contracts | Not runtime |
| **afi-math** | Canonical deterministic math kernels + golden vectors | Normative — mathematical law | Consumed as a pinned library |
| **afi-core** | Scoring library: UWR engine, profile loader, decay surfaces | Governed implementation | Library (in-process) |
| **afi-reactor** | Scoring runtime: validation → configured graph execution → scoring → evidence construction → submission | Governed implementation | Runtime executor (implemented) |
| **afi-infra** | Canonical evidence store on MongoDB (sole writer) | Governed implementation | Persistence service (implemented) |
| **afi-gateway** | Submission boundary: authenticates, authorizes, routes | Governed implementation | Ingress service (implemented) |
| **afi-mint** | Mint/reward orchestration home (off-chain implemented; on-chain not wired) | Governed implementation | Off-chain orchestration (partial) |
| **afi-token** | On-chain token: 86B hard-cap xERC20 | Governed implementation | Deployed on Base Sepolia testnet |
| **afi-factory** | Pipeline **authoring** system + agent capability layer | Support — replaceable authoring | Authoring tool (not the executor) |
| **afi-xerc20** | Vendored xERC20 standard (dependency of afi-token) | Reference | Compiled dependency |
| **afi-docs** | Documentation hub | Reference | Not runtime |
| **afi-tiny-brains** *(private)* | Bounded first-party aiMl orchestration service: one internal orchestrator runs the ProviderInstance-selected profile of approved experts through a deterministic resolver, fail-closed (does not affect UWR scoring); also hosts the deterministic pattern kernel | Support | Bounded, fenced enrichment |
| **afi-econ** | Economic research kit (non-canonical) | Research | Not runtime |
| **afi-benchkit** | PoI / PoInsight benchmark + reproducibility harness | Research | Standalone benchmark tool |
| **afi-artifacts** | Frozen, DOI-minted paper reproducibility bundle | Reference | Frozen snapshot |
| **afi-protocol** | Public flagship repository map ("start here") | Reference | Not runtime |
| **.github** | Organization profile and defaults | Reference | Not runtime |

Grouped by role: **3** normative + **6** governed implementation + **4** support/reference (`afi-factory`, `afi-xerc20`, `afi-docs`, `afi-tiny-brains`) + **3** research/records (`afi-econ`, `afi-benchkit`, `afi-artifacts`) + **2** organization surfaces (`afi-protocol`, `.github`) = **18**.

---

## Authority model

Authority is exactly what accepted decisions expressly delegate. Self-labeling confers nothing.

```mermaid
flowchart TD
    subgraph Normative["Normative authority"]
        G["afi-governance<br/>accepted decisions — protocol law"]
        C["afi-config<br/>canonical schemas, registries, KATs"]
        M["afi-math<br/>math kernels + golden vectors"]
    end
    subgraph Impl["Governed implementation — replaceable via the same contracts"]
        CO["afi-core"]
        R["afi-reactor"]
        I["afi-infra"]
        GW["afi-gateway"]
        MI["afi-mint"]
        T["afi-token"]
    end
    G --> C --> M
    Normative -->|"contracts, kernels, KATs"| Impl
```

**Normative authority.**
- **afi-governance** holds the accepted decisions — object identity, lifecycle, persistence, scoring pins, math authority, districts, and economic law. Eighteen decision records sit on the current default branch (the newest is the District / API Atlas foundation, **ATLAS-GOV**).
- **afi-config** holds the canonical schemas, registries, conventions, and known-answer tests (KATs) that a decision delegates to it.
- **afi-math** holds canonical deterministic kernels (the 86-billion emissions schedule, decay/Greeks surfaces) with golden vectors.

The precedence order is governance → config → math → implementation → tests → public maps → documentation. A conforming implementation honors the accepted decisions, validates against the afi-config contracts and KATs, and matches the afi-math golden vectors; anything else may be replaced.

**Governed implementation** is carried by six repositories — `afi-core`, `afi-reactor`, `afi-infra`, `afi-gateway`, `afi-mint`, `afi-token` — each replaceable by any implementation honoring the same contracts and handoffs.

**Support, research, and reference** repositories (`afi-factory`, `afi-xerc20`, `afi-docs`, `afi-tiny-brains`, `afi-econ`, `afi-benchkit`, `afi-artifacts`, `afi-protocol`, `.github`) never hold normative authority.

### Canonical objects and identity **(Governed)**

- **`signalId`** is the canonical end-to-end join key. Every artifact about a signal — canonical form, score, evidence record — joins on it.
- **Canonical inbound form** is the Universal Signal Schema **USS v1.1** (`afi.usignal.v1.1`).
- **Strategy identity** is the triple `analystId + strategyId + strategyVersion`.
- **The five analysis categories** are exactly `technical`, `pattern`, `sentiment`, `news`, `aiMl` — a governed namespace (aliases such as `social` or `ai-ml` are disallowed).

These are fixed by the `object-identity-v0.1` and `factory-configurable-pipelines-v1` decisions.

---

## System planes

AFI is organized by responsibility, not by repository alone. The planes below describe what runs today and where each responsibility lives.

### 1. Governance and policy plane **(Governed)**

`afi-governance/decisions/` carries the accepted decisions. The load-bearing ones today:

- **object-identity-v0.1** — canonical Signal (USS v1.1), a thin Scored Signal projection, the strategy triple, `signalId` as the join key.
- **factory-configurable-pipelines-v1** — the analyst-configurable pipeline model: the five-category namespace, the composition and executor boundary, delegation of the contract family to afi-config, and the composition reference carried on canonical scored evidence.
- **provider-byok-foundations-v0.1** — the provider-neutral adapter socket and the secure bring-your-own-key (BYOK) credential boundary: the five categories as open capability lanes, one resolved result per category, the three non-secret objects (Provider, CredentialRef, ProviderInstance), trusted registered adapters, the credential-never-in-artifact and least-privilege runtime-resolution invariants, canonical category-output validation before scoring, and the provider-invocation provenance reservation that `evidence-v3-provider-provenance-v0.1` fills (see [`specs/AFI_PROVIDER_BYOK_FOUNDATIONS.v0.1.md`](specs/AFI_PROVIDER_BYOK_FOUNDATIONS.v0.1.md)).
- **lifecycle-v0.1** — the settlement lifecycle up to the off-chain finality writer; it explicitly reserves on-chain settlement, epochs, rewards, claims, and mint to a future chain-governance track.
- **persistence-v0.1** and **persistence-impl-v0.1** — the canonical evidence store and its staged implementation.
- **uwr-profile-pin-v0.1** and **uwr-runtime-consumption-v0.1** — the pinned (testnet-provisional) UWR profile and the rules for consuming it at runtime.
- **math-authority-v0.1** and **mint-formula-bt-86b-alignment-v0.1** — math ownership and the v1 mint-formula interpretation (epoch budget `E_t = B(t) · AIM_t`, with `AIM_t = 1` for v1).
- **authority-districts-v0.1** and **district-2-m2-ratification-v0.1** — the two-District topology and the prospective ratification of District 2's runtime surface.
- **district-surface-consolidation-v0.1** — the clean-cut District surface record (DSC-GOV): one live `GraphExecutor` as the sole signal-evaluation executor, the District-1 implementation record pointing at the live pipeline, the District-2 provenance law homed in `afi-reactor/src/evidence/provenance/`, exactly one provider framework (`afi-reactor/src/providers/`), and the five-category terminology rule.
- **district-one-signal-evaluation-capability-v0.1** — the District One capability record (D1CAP-GOV): District 1 is the **active Signal Evaluation capability and authority domain** (implementation-independent — a conforming future implementation may replace the current one through accepted authority without retiring the district), with its durable responsibility boundary, its exclusions, the descriptive current-implementation mapping, and the ruling that Mission A's clean cut was an implementation retirement only — the district endures.
- **five-lane-provider-runtime-v0.1** — the Five-Lane Provider Runtime Activation record (FLPR-GOV): the PBF-GOV provider framework is the **sole live enrichment-execution seam** for all five categories; every enabled lane node carries exactly one explicit `providerInstanceRef` (fail-closed, no silent fallback, no env-var vendor selection); the sentiment/aiMl/candlestick-pattern/SEC-EDGAR adapters and the bounded additive `candlestick` block on `afi.enrichment.pattern.v1`; the byte-level scoring-invariance obligations; and the forward-only removal of every classic direct-call category path.
- **evidence-v3-provider-provenance-v0.1** — the Evidence V3 and provider-invocation provenance record (EV3-GOV): `afi.scored-signal-evidence.v3` as the **sole current canonical scored-signal evidence contract** (the prior record shape carried forward plus exactly three required additions — `providerInvocations`, `recordHash`, `replayHash`); exactly five closed, credential-safe, deterministically ordered per-lane provider invocation proofs (`afi.provider-invocation-proof.v1`, carried, never consumed) with the nested Tiny Brains aiMl invocation proof (`afi.aiml-invocation-proof.v1`); the registered `afi.d2.*` hash-domain assignments with an explicit canonical/replay projection separation; the all-five evaluation-completeness law (every category lane fail-fast — a failed lane yields no scored evaluation and no evidence record); capture in the one live graph pass with a fail-closed sole evidence builder in District 2 that never invokes a provider; V3-only hash-verified admission at the sole canonical writer; and the forward-only replacement of the prior evidence surfaces.
- **district-api-atlas-foundation-v0.1** — the District / API Atlas foundation record (ATLAS-GOV): designates AFI's **canonical discoverability and relationship layer** (`afi.protocol-atlas.v1`, delegated to afi-config) over Districts, structures, capabilities, interfaces, typed routes, contracts, repositories, participant roles, and onboarding descriptors; separates maturity from visibility; forbids invented APIs and secret-capable fields; and establishes that the Atlas **describes** protocol truth and does not replace runtime, schema, contract, or governance authority (it fills the reserved ATLAS-GOV slot). It creates no District, changes no District scope, and builds no endpoint or Protocol City surface.

The lifecycle state machine is governed as `INGESTED → VALIDATED → SCORED → CERTIFIED → QUALIFIED → CHALLENGE_OPEN → [CONTESTED →] FINALIZED → EPOCH_ELIGIBLE`. **The implemented lifecycle currently reaches `SCORED`.**

### 2. Contract and registry plane **(Governed)**

`afi-config` is the canonical home for the schemas and registries the runtime consumes:

- the **USS v1.1** signal schema (`schemas/usignal/`);
- the **scored-signal-evidence v3** schema (`afi.scored-signal-evidence.v3`) with its per-lane provider invocation proof contracts (`afi.provider-invocation-proof.v1`, `afi.aiml-invocation-proof.v1`) and its published valid/invalid vectors;
- the pipeline-composition, analysis-plugin, analyst-strategy, and provider-binding registries;
- the **provider / BYOK contract family** — the non-secret `afi.provider.v1`, `afi.credential-ref.v1` (an opaque pointer that never holds a secret), and `afi.provider-instance.v1` (tenant-scoped) schemas, the `registries/providers/` reference records, and the canonical per-category output contracts `afi.enrichment.{technical,pattern,sentiment,news,aiml}.v1` — all five categories have governed contracts (PBF-GOV foundations; the full contract family completed with the enrichment-contract mission);
- the **CPJ v0.1** community-provider-journal schema (`schemas/cpj/v0_1`) and the active oracle provider bindings that consume it;
- the **UWR profile registry** (`registries/uwr-profiles/`), whose pinned profile `uwr-weighted-lifts-v0.1` is testnet-provisional;
- the **provenance (District 2 M1)** schema family (`schemas/provenance/v1`);
- KAT vectors for scoring and time decay;
- a **draft, read-only** vault-address registry (descriptive metadata; not an instruction to move funds).

Analysts may configure and run conforming UWR profiles, decay surfaces, and strategy pipelines without bespoke permission; a profile becomes *protocol-recognized* only when registered and version-pinned in afi-config — a governed registry change.

### 3. Factory authoring plane **(Implemented)**

`afi-factory` is the pipeline **authoring** system. It **produces artifacts; it does not execute the live graph**, load plugin code, or run pipelines.

- An **operation registry** exposes exactly **14** agent-operable authoring operations: `factory.capabilities.list`, `factory.plugins.list`, `factory.official.list`, `factory.template.create`, `factory.template.validate`, `factory.template.inspect`, `factory.template.instantiate`, `factory.pipeline.validate`, `factory.pipeline.inspect`, `factory.analystConfig.create`, `factory.analystConfig.validate`, `factory.plugin.scaffold`, `factory.artifact.hash`, `factory.artifact.package` (twelve read-only, two mutating).
- **Five surfaces project over the same handlers** through one dispatch path: the TypeScript **SDK**, the **`afi-factory` CLI**, a deterministic **capability catalog**, framework-neutral **tool definitions**, and an **MCP-compatible stdio adapter** (JSON-RPC 2.0, transport-only).
- It implements templates (which parameterize values, never topology), plugin/component and official-composition discovery, analyst-strategy configuration, the governed composition model (plugin-subset selection, repeated same-category nodes, sequential/concurrent ordering via explicit dependencies, bounded declarative conditional branches, deterministic multi-parent joins), **canonical hashing** (`canonical-json-hashing.v1` with domain-tagged manifest/analyst-config/plugin-set hashes, KAT-pinned), and fail-closed artifact packaging.
- It consumes byte-pinned copies of the afi-config schema closure; nothing it emits is canonical until validated against those contracts. Its suite is 207 tests.

Factory is **not** the API Atlas, **not** the Gateway, **not** the Reactor runtime, and **not** the source of scoring law or finality. It is a library and CLI that produces artifacts; it is **not deployed** as a service.

### 4. Gateway ingress plane **(Implemented)**

`afi-gateway` is the external submission boundary and **routes; it never writes canonical evidence**.

- `POST /api/v1/signals` authenticates the API key, resolves the tenant, and rate-limits; the handler performs a presence-only field check and forwards the payload to the Reactor.
- It stamps provenance (`providerId = gateway:<tenantId>` from the authenticated key) and returns the Reactor's answer verbatim. It never validates payload semantics, scores, resolves UWR, constructs evidence, or writes a store.
- It **fails closed**: without a configured Reactor URL it refuses to start; an unreachable Reactor yields `503 persisted:false`, never a queued/accepted response.
- The routes-not-writes boundary is enforced by executable guardrail tests (no import of the persistence layer, no canonical-evidence tokens, only operational collections).
- **AFI Research Institute is designated to operate the official hosted Gateway reference instance (Reference).** This designation is **non-exclusive**: the MIT-licensed implementation stays usable by independent conforming operators, and any Institute instance policies (quotas, onboarding, tenant isolation) apply only to that hosted instance, not to protocol law. No Institute-hosted deployment is claimed (none exists). The Gateway's endpoint authority is reserved to `ATLAS-GOV`. See `research-institute-reference-services-v0.1` (INST-GOV) and [`specs/AFI_RESEARCH_INSTITUTE_REFERENCE_SERVICES.v0.1.md`](specs/AFI_RESEARCH_INSTITUTE_REFERENCE_SERVICES.v0.1.md).

### 5. Reactor execution plane **(Implemented)**

`afi-reactor` is the **one production graph executor**.

- **Boot is a fail-closed gate**: it loads the afi-config registries (analysis plugins, pipelines, analyst strategies, provider bindings), schema-validates every active entry, recomputes and verifies the manifest / analyst-config / plugin-set hashes, and refuses to start on any invalid entry. There is no lazy request-time discovery.
- **Two live ingress paths reach the executor.** Most submissions arrive routed from the Gateway (`POST /api/v1/signals` → the Reactor webhook). The Reactor also exposes **`POST /api/ingest/cpj`**, a direct community-provider-journal ingest (`afi.cpj.v0.1`, for Telegram/Discord oracle providers) that bypasses the Gateway under an optional shared secret, validates CPJ v0.1, and deduplicates by ingest hash (`409` on a duplicate). Both paths **resolve the provider → strategy binding** against the boot-validated provider-binding registry — an unbound provider is rejected with an honest `403`, never a silent default composition — then map to USS v1.1 and run the identical scoring path.
- **The direct CPJ route is an internal trusted service boundary, not a public API (Reference/Reserved).** Its authentication is optional (a single shared secret) and provider identity is self-asserted, so any future public or partner CPJ access is designated to be mediated by a separate authenticated **Institute oracle-ingress reference service** — designated, **not implemented or deployed** — or another conforming external trust boundary; the route is neither renamed, moved, nor exposed. Provider binding, CPJ validation, and provenance stay mandatory regardless of exposure (ingest dedupe is opt-in, `AFI_INGEST_DEDUPE=1`) (INST-GOV; see [`specs/AFI_RESEARCH_INSTITUTE_REFERENCE_SERVICES.v0.1.md`](specs/AFI_RESEARCH_INSTITUTE_REFERENCE_SERVICES.v0.1.md)).
- The **graph is manifest-driven**, not a hardcoded DAG. The executor runs topological waves (Kahn's algorithm) with bounded concurrency, deterministic ready-sets, per-node timeout and retry, conditional edges, and joins keyed by node id. Graph validation enforces unique ids, acyclicity, reachability, exactly one non-bypassable scorer sink, and declared joins.
- The **five analysis categories** are vendor-neutral, provider-instance-backed lane plugins bound at build time, alongside the five-category join plugin and the scorer. Any registered strategy (for example the "Froggy trend-pullback" scorer) is an ordinary registry entry, not a special path. The `aiMl` lane joins the sibling lanes' outputs and invokes the self-hosted `afi-tiny-brains` service through its governed adapter, naming the ProviderInstance-selected orchestration profile (the governed `model` field) and carrying the technical lane's real close-price series; Tiny Brains runs that profile's approved internal experts (Chronos-Bolt forecaster + deterministic trend baseline behind `froggy-reference-v1`) through a deterministic resolver into exactly one result. Its result is read-only context and **does not affect UWR scoring** (a failed lane, unknown profile, unready model, or invalid expert output fails the run under the all-five evaluation-completeness law — no scored evaluation, no scored signal, no evidence record; bounded operational diagnostics only, nothing fabricated).
- The **bounded provider-adapter runtime** inside the Reactor, below the category node (not a second executor), is the **sole live enrichment-execution seam** (FLPR-GOV). Boot loads the governed `registries/{providers,provider-instances,credential-refs}` records fail-closed; every lane node carries a non-secret `providerInstanceRef`; the runtime resolves the tenant-scoped provider instance, resolves **only** the authorized credential through an injected least-privilege `SecretResolver` (the adapter receives a bounded credential bundle, never a resolver), invokes the trusted statically registered adapter, and validates the canonical `afi.enrichment.<category>.v1` output before it reaches the scorer — one resolved result per category, fail-closed at every boundary, no silent provider fallback. Eight adapters are registered: keyless local technical, first-party candlestick pattern (local kernels), Tiny-Brains pattern (self-hosted STUMPY/ruptures/find_peaks), keyless CFTC-COT sentiment (public domain), credentialed Coinalyze sentiment (BYOK header), credentialed NewsData news (BYOK header), keyless SEC-EDGAR news, and first-party Tiny-Brains aiMl (internal orchestration selected per instance via the governed `model` field, validated against the provider record's `supportedModels`). The committed reference profile selects an all-five keyless/self-hosted instance set; selecting a different supported provider is a registry/record change, never category-node code. Credentials are resolved only at invocation and appear in no artifact, log, hash, or evidence; the current resolver backend is the env-backed development backend, and deployment-specific secret backends are pending a later staging wave (PBF-GOV + FLPR-GOV; see [`specs/AFI_PROVIDER_BYOK_FOUNDATIONS.v0.1.md`](specs/AFI_PROVIDER_BYOK_FOUNDATIONS.v0.1.md)).
- The scorer node wraps afi-core's analyst, resolves the UWR configuration fail-closed, and emits scores and their resolved source verbatim.
- **A scored evaluation requires all five lanes to succeed** (EV3-GOV): every category lane node in the registered manifest is fail-fast, so a failed lane yields no scored evaluation, no scored signal, and no evidence record — bounded operational diagnostics only. **Provider invocation provenance is captured inside the same single graph pass** at the provider-runtime seam, where the identity chain is already resolved, and travels with execution state to District 2 — evidence describes the invocation that occurred and never re-calls a provider. Each lane's proof binds non-secret facts only: the Provider identity (id, record version, record fingerprint, execution class, deterministic/probabilistic posture), the ProviderInstance identity (id, record version, configuration fingerprint, and the governed `model` where the instance declares one), the adapter identity (id, version, transport kind), the credential binding — an explicit keyless posture or an opaque CredentialRef (id, record version, kind, governed status; never a secret, secret-derived hash, header, token, or credentialed URL) — and the normalized invocation-input, provider-result, and category-result hashes. The `aiMl` proof additionally nests the Tiny Brains invocation proof: orchestration profile, resolver, and per-expert identities and versions, per-expert output hashes, model artifact fingerprints, and the service's verified input/output hashes — hashes and identifiers only, no raw payloads, prompts, paths, or weights.
- The Reactor **constructs Evidence V3** (`afi.scored-signal-evidence.v3`) — the sole current canonical scored-signal evidence contract — with `lifecycleState = SCORED`, `finalized = false`, the registry-backed UWR-profile stamp, a required all-or-nothing composition reference, exactly **five** provider invocation proofs (one per category, unique, deterministically ordered, carried, never consumed), and record-level `recordHash` / `replayHash` commitments. District 2's sole evidence builder validates the five bound proofs and cross-checks every identity and hash against the boot-verified registries and the results the analyst path actually consumed, fail-closed on any mismatch. The canonical record separates immutable invocation facts and the deterministic replay projection from operational diagnostics: wall-clock timings, attempt counts, and transport noise stay in runtime logs and never enter the record or any hashed preimage; `replayHash` commits to the replay projection, so two evaluations of the same canonical inputs through the same composition produce identical `replayHash` values. Scores are read verbatim from afi-core and never recomputed.
- The **submitter rejects any non-`SCORED` record**, proves the wrapper, schema, sub-artifact schemas, and identifier continuity before submitting, and surfaces every failure as a typed non-2xx. The Reactor **never touches MongoDB directly**; it consumes afi-infra's store as a typed dependency, and persistence is a required step of the run.

### 6. Core and mathematical computation plane **(Implemented)**

```text
afi-factory  → authors the configured pipeline and composition (authoring)
afi-reactor  → orchestrates execution                          (runtime)
afi-core     → performs canonical deterministic computation    (domain library)
afi-math     → defines canonical mathematical law              (kernel)
```

- **afi-core** performs deterministic domain computation: the UWR aggregator (a weighted combination of structure, execution, risk, and insight axes, clamped to `[0,1]`), the fail-closed UWR profile loader (pinned to `uwr-weighted-lifts-v0.1`), and decay/Greeks templates. Its runtime UWR resolution is registry-backed in the Reactor.
- **afi-math** owns the numeric kernels; afi-core delegates the numeric decay computation to afi-math (consumed as a version-pinned dependency). Core is the domain wrapper; math is the law.

UWR (the Universal Weighting Rule) is the governed scoring mechanism. There is no separate per-signal "PoI" or "PoInsight" score in the runtime — those names belong to the research benchmark plane below.

### 7. Persistence and evidence plane **(Implemented)**

`afi-infra` owns the **sole canonical write path**.

- The store's `submit` is the only first-write path: it requires the record schema to be `afi.scored-signal-evidence.v3` (the only admissible evidence contract), validates the governed schema and identifier continuity, verifies the record's `recordHash` and `replayHash` by recomputation (an invalid or mis-hashed record is rejected, never persisted), then inserts into a collection with a **unique `signalId` index**. The default database is `afi_scored_signal_evidence` and the current collection is `scored_signal_evidence` (with a history collection), overridable by environment.
- Persistence is **append-once and idempotent**: an identical re-submission returns an idempotent-duplicate outcome; a differing submission for the same `signalId` is a conflict (`409`). A governed correction must go through `supersede()`, which archives the existing version and installs the new one inside a single transaction with version pinning and refuses to alter a finalized record.
- The Gateway routes and never writes here; the Reactor submits and never writes here; afi-infra is the writer.

Every record persisted today carries `lifecycleState = SCORED` and `finalized = false`. **The correction/versioning path (`supersede`) is implemented and tested but has no live caller** — nothing in the production flow supersedes a record yet.

### 8. Benchmarking and research plane **(Research)**

`afi-benchkit` is a standalone public benchmark and reproducibility harness with no private-repository dependency (a guardrail test enforces this).

- It provides two seeded suites: **PoI** (capability — coverage, vitality, determinism, latency) and **PoInsight** (usefulness — information coefficient, hit rate, Sharpe over 1h/4h horizons).
- It is deterministic and reproducible: fixed seeds, stamped artifacts (data hash + git SHA + timestamp), golden-hash-locked plots, an `afi-bench` CLI, and a hash-locked container **published by CI to `ghcr.io/afi-protocol/afi-benchkit`**.
- Its input is **static CSV fixtures**; it has **no live finalized-receipt feed and no production reputation or incentive integration**. Its composite reputation number (a weighted combination of PoI and PoInsight) is a local research computation over benchmark outputs, **not** the protocol's reputation or incentive law. Fixture-backed PoInsight is not PoInsight computed from finalized live receipts.
- Current test state: outside the pinned container, exactly **two** golden-image plot tests fail (`test_calibration_plot_golden`, `test_poi_capability_golden`) as SHA-256 mismatches from a matplotlib version difference; the remaining benchmark tests pass.

`afi-econ` is a non-canonical economic research kit (its models are self-declared placeholder/toy and are not protocol law unless promoted by governance). `afi-artifacts` is a frozen, DOI-minted paper reproducibility bundle (Zenodo). **AFI Research Institute** is AFI's sole research and legal identity — the copyright holder across the organization's licenses — reflecting an open-protocol, auditable, replayable research posture. Committed to open research, it is **designated to operate AFI's official open reference services (Reference)**: a hosted **Gateway reference service** (§4) and a designated **oracle-ingress / CPJ-normalization reference service** (§5), governed by `research-institute-reference-services-v0.1` (INST-GOV) and specified in [`specs/AFI_RESEARCH_INSTITUTE_REFERENCE_SERVICES.v0.1.md`](specs/AFI_RESEARCH_INSTITUTE_REFERENCE_SERVICES.v0.1.md). These are **non-exclusive** reference instances — operating them confers no protocol authority, no economic or validator privilege, and no exclusive network role; independent conforming operators remain free to run their own ingress and collectors. No Institute-hosted deployment is claimed (none exists).

### 9. On-chain and economic plane

The economic plane separates governed design from implementation from deployment.

- **afi-token (Implemented; Deployed on testnet).** `AFIToken` is an xERC20-based ERC-20 with an on-chain hard cap of **86,000,000,000 AFI**, enforced in its sole mint entrypoint (`mintEmissions`, gated by an emissions role granted to explicit addresses, never the deployer). The contract suite passes its Foundry tests. It is deployed on **Base Sepolia testnet** (chain 84532, symbol `tAFI`), with roles held by a Treasury Safe. **There is no Base mainnet deployment.**
- **afi-xerc20 (Reference).** The vendored defi-wonderland xERC20 standard (`XERC20`, `XERC20Lockbox`, `XERC20Factory`), consumed by afi-token as a pinned submodule. Its multichain deploy artifacts are inherited upstream boilerplate, not AFI deployments.
- **afi-mint (Implemented off-chain; on-chain not wired).** The off-chain orchestration is implemented in TypeScript — signal-state management, a challenge-window/appeal model, dispute resolution, a mint executor, a validator daemon, and a governance client — and the per-signal emission math is implemented and parity-tested against the afi-math 86B schedule. The link to a live on-chain mint is **not wired**: the mint executor targets an abstract contract interface with no concrete binding, the Solidity contracts are stubs, and reputation-weighted emission logic is a placeholder awaiting governed values.
- **Settlement (Governed doctrine; not implemented).** AFI Settlement v1 is accepted doctrine — epoch-settled rewards through a custodial rewards vault with Merkle claims, funded from an epoch settlement manifest, with provenance decoupled from payout and concrete address+chainId as source of truth. It **implements no contracts**: no rewards-vault, receipt, Merkle-claim, or settlement-manifest contract exists in any repository.
- **Participant claim roles (Governed doctrine; closure in draft).** Accepted Settlement v1 doctrine mandates at least three participant reward tracks — **Provider**, **Analyst/Scorer**, and **Validator** — as distinct allocation tracks. The tighter closure to *exactly* these three (barring public goods and governance as claimants) currently lives in draft specs and schema and is not yet accepted governance. Operational overhead and the DAO operations vault are treasury policy administered by governance, not a claim role.
- **Live mint is governance-blocked.** The v1 mint-settlement skeleton is governed (epoch budget → role pools → pro-rata verified credits), but the numeric baseline role weights are not yet governed and are a required decision before any live mint. Mainnet settlement is not yet governed.

### 10. Discovery and documentation plane **(Reference)**

- **`.github`** is the concise public organization front door (profile), routing readers to the map and the docs; it holds no authority.
- **afi-protocol** is the flagship "start here" repository map — deliberately thin, no authority of its own.
- **afi-docs** is the detailed documentation hub (this document). Documentation explains authority; it does not replace it.
- The **API Atlas** now has a **canonical foundation** (`afi.protocol-atlas.v1`, ATLAS-GOV): a machine-readable discoverability and relationship registry in afi-config, described in "District / API Atlas foundation" below. The foundation **describes** current capabilities, interfaces, routes, contracts, and maturity; it is not a runtime read/API surface and exposes no endpoint. Factory's capability catalog remains authoring metadata, not the Atlas.

---

## The current end-to-end flow

The implemented path from submission through persistence, proven by CI against real infrastructure:

```mermaid
flowchart TD
    RG["Institute Gateway reference service<br/>(designated · not deployed)"] -. "structured submissions" .-> A
    IND["independent conforming ingress<br/>(architectural right)"] -. "conforming submissions" .-> A
    RO["Institute oracle-ingress reference service<br/>(designated · not deployed)"] -. "authenticated collector CPJ" .-> A2
    A["Signal submission<br/>POST /api/v1/signals"] --> B["afi-gateway<br/>authenticate • resolve tenant • rate-limit • stamp provenance"]
    B -->|"route, never write"| C["afi-reactor webhook<br/>resolve provider → strategy binding (honest 403)"]
    A2["Community provider journal<br/>POST /api/ingest/cpj (internal trusted boundary)"] --> C2["afi-reactor CPJ ingest<br/>validate CPJ v0.1 • dedupe • resolve binding (honest 403)"]
    C --> D["map to USS v1.1<br/>validate canonical signal"]
    C2 --> D
    D --> E["GraphExecutor<br/>manifest-driven topological waves"]
    E --> F["five analysis categories<br/>technical • pattern • sentiment • news • aiMl"]
    F --> G["deterministic join → scorer sink<br/>afi-core UWR scoring"]
    G --> H["Evidence V3 construction<br/>afi.scored-signal-evidence.v3 • five invocation proofs • composition ref • SCORED"]
    H --> I["afi-infra store.submit<br/>unique signalId • append-once • transactional"]
    I --> J(["Canonical record persisted<br/>lifecycleState = SCORED"])
    style RG stroke-dasharray: 5 5
    style RO stroke-dasharray: 5 5
    style IND stroke-dasharray: 5 5
```

The dotted entry lanes are the **designated** ways to reach the two implemented ingress points: the Institute Gateway and oracle-ingress reference services (designated, not deployed) and independent conforming ingress (an architectural right — independent operators submit to the same implemented boundaries directly). The solid path from the ingress points through persistence is the implemented runtime (INST-GOV; §4–§5).

```text
ingest → USS v1.1 validation → scoring (governed UWR engine, pinned profile)
       → Evidence V3 construction (composition reference • five provider invocation proofs • recordHash/replayHash)
       → canonical store (unique signalId, append-once, transactional supersession)
       → lifecycleState = SCORED
```

### Not implemented in the current live path

The lifecycle is governed beyond `SCORED`, but the following are **not** implemented today. They are listed as gaps, not designed here.

```mermaid
flowchart LR
    S(["SCORED<br/>implemented"]) -. "not implemented" .-> X["CERTIFIED · QUALIFIED · CHALLENGE · FINALIZED"]
    X -. "not implemented" .-> Y["epoch accounting · rewards · claims"]
    Y -. "not implemented" .-> Z["live mint · mainnet settlement"]
    style S fill:#1f6f43,stroke:#0d3b24,color:#ffffff
    style X fill:#5b3a00,stroke:#3a2500,color:#ffffff
    style Y fill:#5b3a00,stroke:#3a2500,color:#ffffff
    style Z fill:#5b3a00,stroke:#3a2500,color:#ffffff
```

- **Post-`SCORED` transitions** (`CERTIFIED`, `QUALIFIED`, challenge, `FINALIZED`) — the single finality writer is defined in law but intentionally unimplemented pending new authorization.
- **Market-outcome observation and challenge windows** in the live path.
- **Live PoInsight from finalized receipts** — the benchmark computes PoInsight from fixtures only.
- **Participant reputation updates** in the protocol.
- **Epoch accounting, incentive allocation, reward claims, and claim-root production** — no implemented owner.
- **Live token minting** tied to the settlement design — governance-blocked on ungoverned role weights.
- **Base mainnet settlement** — not yet governed.
- **A read/replay/verify API surface over the Atlas or evidence** — reserved to ATLAS-GOV and not built. The Atlas foundation is discoverability metadata, not a runtime endpoint.
- **The AFI Protocol City** (the visual navigation projection of Atlas truth) and the **AFI Participant Gateway** (a registration/conformance control plane) — **not started**; the Atlas foundation is the groundwork they will later build on.
- **The Institute Gateway hosted reference deployment** — designated for operation by AFI Research Institute (INST-GOV), not deployed.
- **The Institute oracle-ingress reference service** and any public or partner CPJ API — designated as the authenticated external trust boundary in front of the internal Reactor CPJ route, not implemented or deployed. Reference source collectors beyond an in-repo, undeployed Telegram client are not implemented.
- **A production or staging deployment** — the runtime is implemented and CI-proven against real infrastructure, but no deployment target (container, cloud, or Kubernetes manifest) exists in the runtime repositories, and there is no GCP staging or production deployment.

---

## Districts

Exactly **two** Districts are formally registered (`authority-districts-v0.1`, Part D, as amended by `district-surface-consolidation-v0.1` (DSC-GOV) and `district-one-signal-evaluation-capability-v0.1` (D1CAP-GOV)). Both are **active capability domains**, and both remain **non-production** (nothing is deployed). No other District is created or implied. Districts represent durable capability and authority boundaries: implementations may be replaced through accepted authority without retiring the district they implement.

- **District 1 — Signal Evaluation** — the **active** Signal Evaluation capability and authority domain (D1CAP-GOV). It owns evaluation from canonical signal input through the scorer/UWR seam: evaluation-time validation, execution of the five enrichment categories, explicit provider-instance resolution for provider-backed categories, category-result validation against the governed `afi.enrichment.*.v1` contracts, deterministic fan-out and join (exactly one validated result per category), analyst invocation under accepted authority, canonical scorer/UWR invocation (invoked, never re-implemented), and creation of the scored evaluation result handed to District 2. Its current implementation is the live flow described in "The current end-to-end flow" below: the two ingress paths → the one manifest-driven `GraphExecutor` (`afi-reactor/src/pipeline/`) → category nodes → enrichment join → analyst/scorer/UWR → the District-2 handoff. The district is not any directory, class, manifest, analyst, or provider — the mapping is descriptive, and a conforming future implementation may replace it through accepted authority. The five-lane provider runtime is **active** for all five categories (FLPR-GOV; see the category table below). Git history preserves the earlier proof-of-concept implementation record; that record's retirement under DSC-GOV was an implementation retirement only — the district is active.
- **District 2 — Canonical Data & Provenance Boundary.** Active. Its M1 schema family is implemented in `afi-config/schemas/provenance/v1` with validation tests, authorized for **M1 only** ("no runtime wiring") by the D-17 instrument homed in afi-docs. Its live provenance law — CanonicalHash v1 (`afi.hash.v1`), the ScoredSignal v1 projection builders, and the D2 schema validators — is implemented in `afi-reactor/src/evidence/provenance/` and runs as a required step of every scoring run; the prospective, bounded, non-production ratification of `district-2-m2-ratification-v0.1` is recorded at that location by DSC-GOV D-DSC-3 (no canonical-object declaration is made). **It receives the scored evaluation result and the five bound provider invocation proofs from District 1 at the scorer/UWR seam** and owns evidence construction, validation, and the canonical handoff to persistence from there: its sole evidence builder validates the five proofs (exactly five, unique by category, deterministically ordered), cross-checks every identity and hash fail-closed, and constructs the one canonical Evidence V3 artifact (`afi.scored-signal-evidence.v3`) that afi-infra persists as sole writer. **District 2 never invokes a provider** — evidence describes the invocation that occurred (EV3-GOV).

**Five-category state (District 1, current truth):**

| Category | Governed contract | Reference ProviderInstance (keyless/self-hosted) | Additional supported provider | Affects the analyst score today |
|---|---|---|---|---|
| `technical` | `afi.enrichment.technical.v1` | `afi-instance-reference-technical-local` (local kernels over the configured keyless exchange feed) | — | **yes** (EMA distance, value-zone) |
| `pattern` | `afi.enrichment.pattern.v1` | `afi-instance-reference-pattern-candlestick` (first-party local kernels; the D-FLPR-3 candlestick block) | `afi-instance-reference-pattern-tiny-brains` (self-hosted kernel service) | **yes** (pattern confidence) |
| `sentiment` | `afi.enrichment.sentiment.v1` | `afi-instance-reference-sentiment-cftc-cot` (public-domain COT positioning) | `afi-instance-byok-sentiment-coinalyze` (BYOK header) | wired into the scorer input but inert under the live value domains |
| `news` | `afi.enrichment.news.v1` | `afi-instance-reference-news-sec-edgar` (public filings) | `afi-instance-byok-news-newsdata` (BYOK header) | no (evidence/lenses only) |
| `aiMl` | `afi.enrichment.aiml.v1` | `afi-instance-reference-aiml-tiny-brains` (self-hosted service; `model: froggy-reference-v1` selects the internal orchestration profile) | — | no (read-only context; evidence/lenses only) |

All five categories execute live through the provider runtime: the registered `froggy-trend-pullback v1.3.0` manifest binds an explicit `providerInstanceRef` on every lane node (the committed all-five keyless/self-hosted reference profile) and declares every category lane fail-fast — a scored evaluation requires all five lanes to succeed, and a failed lane yields no scored evaluation, no scored signal, and no evidence record (EV3-GOV D-EV3-5). Provider selection is a registry/record change under FLPR-GOV D-FLPR-4 — never category-node code, never an environment switch, never a silent fallback.

**District map authority.** The canonical **District / API Atlas** now has a machine-readable foundation (`afi.protocol-atlas.v1`, ATLAS-GOV; see "District / API Atlas foundation" below). Governance remains the authority: accepted decisions define District boundaries and the Atlas **describes** them; it defines no District and executes nothing. The Atlas records District One and District Two exactly as this chain establishes them, and the human-readable summary below is mechanically drift-checked against the registry.

---

## District / API Atlas foundation

The **District / API Atlas** is AFI's canonical **discoverability and relationship layer**: a machine-readable record of what the protocol *is* — its capability/authority domains (Districts), the concrete systems that implement them (structures), the governed I/O boundaries (interfaces), the typed movement between them (routes), the contracts that govern them, the repositories that implement them, and the participant roles that use or supply them. It is authorized by **`district-api-atlas-foundation-v0.1`** (ATLAS-GOV) and its canonical machine-readable form is **`afi.protocol-atlas.v1`**, delegated to afi-config:

- **Schema:** `afi-config/schemas/atlas/v1/afi-protocol-atlas.schema.json`
- **Registry:** `afi-config/registries/afi-protocol-atlas.v1.json`
- A byte-pinned copy is vendored here at `atlas/afi-protocol-atlas.v1.json`; `scripts/check_atlas_summary.py` mechanically drift-checks this document against it.

**The Atlas describes; it does not decide or execute.** It replaces no runtime, schema, contract, or governance authority (ATLAS-GOV D-ATLAS-1). Where the Atlas and a higher authority disagree, the higher authority wins and the Atlas is the surface to correct. It runs no graph, calls no provider, scores nothing, builds no evidence, routes no live traffic, resolves no secret, activates no participant, and transfers no value.

The registry records **2 active Districts** (plus **1 reserved** capability-domain), **6 capabilities**, **13 structures**, **16 interfaces**, **9 typed routes**, **21 referenced contracts**, **18 repositories**, and **7 participant roles** with onboarding descriptors.

### Districts (from the registry)

| districtId | Name | Maturity | Owned capabilities | Serving structures |
|---|---|---|---|---|
| `district-one` | **Signal Evaluation** | operational | signal ingest & normalization, five-category enrichment, deterministic scoring/UWR, pipeline composition authoring | Reactor runtime, afi-core, afi-math, Factory, Gateway, Tiny Brains, afi-config |
| `district-two` | **Evidence and Provenance** *(registry long-form: Canonical Data & Provenance Boundary)* | operational | Evidence V3 construction, canonical evidence persistence | Reactor runtime (evidence law), afi-infra store, afi-config |
| `chain-settlement` | Settlement, Rewards, Reputation & On-Chain Value | **reserved** *(active: false)* | — (none; **CHAIN-GOV** reserved) | afi-token, afi-mint, afi-math (emissions) |

District Two **spans three repositories** (afi-reactor for Evidence V3 construction, afi-infra for persistence, afi-config for the contract) — a District is a capability/authority domain, never a repository. The reserved `chain-settlement` domain is **not** an active or numbered District: it records, exactly as `authority-districts-v0.1` Part D.2 already does, the uncreated future settlement/rewards/on-chain candidate, which requires its own CHAIN-GOV decision before it becomes a District.

### Structures, interfaces, routes, and maturity

Structures are concrete systems — a runtime, a shared library, a math kernel, an authoring system, a gateway, a service, a registry, a persistence store, the governance ledger, an on-chain token — and a structure is **not automatically a District**: the Reactor runtime serves both District One (execution) and District Two (Evidence V3 construction); the Gateway serves District One by **routing** its signal-submission boundary (`POST /api/v1/signals`) **without owning** that capability. The Atlas records `exposingStructure` and `routingStructure` separately from the owning capability/District (ATLAS-GOV D-ATLAS-4).

The Atlas keeps **maturity** (`operational` / `partial` / `underConstruction` / `planned` / `reserved`) **separate from visibility** (`public` / `restricted` / `internal`): an entity is `operational` only with cited implementation + test evidence, and the org-wide posture stays non-production regardless. A non-`operational` interface carries **no** address or operation identifier (no invented APIs, D-ATLAS-7). Routes are typed by flow — `data`, `control`, `identityTrust`, `evidence`, `buildArtifact`, `value` — and never imply a network hop for an in-process handoff (the District One → District Two evidence handoff is an in-process typed submit, not a network route). Interfaces span HTTP APIs, governed schema boundaries, the persistence admission boundary, the Factory SDK/CLI/MCP operation surface (including the current operation `factory.official.list`), and the self-hosted Tiny Brains endpoints — the API Atlas is not an HTTP-endpoint inventory. Contracts are **referenced, never duplicated**: the Atlas points at `afi.scored-signal-evidence.v3`, `afi.usignal.v1.1`, the five `afi.enrichment.{technical,pattern,sentiment,news,aiMl}.v1` category contracts, and the rest, without copying their schema content.

### Participant roles and onboarding

The Atlas is **onboarding-ready without implementing onboarding** (D-ATLAS-10): it describes roles, the contracts they use, and honest onboarding maturity, but performs no onboarding, identity verification, credential issuance, or activation, and holds no secret. The current participant roles are: **Signal provider**, **Analyst / scorer**, **Data / enrichment provider**, **Validator**, **Operator**, **Builder / developer**, and **Application integrator**. Validator role authority is honestly **reserved** (role weights are unfiled, CHAIN-GOV); a self-serve onboarding control plane does not yet exist, so onboarding descriptors are `planned`/`underConstruction`. "Investor" is **not** a protocol-conformance role — it appears only as a non-conformance audience descriptor.

**AFI-operated onboarding is a reference entrance, not the only entrance** (D-ATLAS-11): third parties may build competing conformant onboarding, education, developer, validator, provider, analyst, or operator experiences against AFI's canonical conformance requirements, and compete on experience and services — but may not redefine or bypass the canonical conformance and activation requirements set by governance and the governed contracts.

### Atlas vs. runtime vs. Protocol City

The Atlas is not the runtime (it describes the runtime, and the runtime authority is the code + governed contracts) and not the Protocol City. The future **AFI Protocol City** is a visualization/navigation projection of Atlas truth — a City landmark has exactly the authority its underlying Atlas entity has, and the visual metaphor creates no architectural authority (D-ATLAS-13). Mission Atlas-0 builds only this foundation: the **AFI Protocol City** and the **AFI Participant Gateway** control plane are **not started**.

---

## Deployment and treasury status

- **No deployment target exists** for the runtime services (`afi-gateway`, `afi-reactor`, `afi-core`, `afi-infra`): there is no container, cloud-build, or Kubernetes/Fly/Render manifest in those repositories; the only workflows are CI and validation. The pipeline is implemented and CI-proven, **not deployed** to a hosted environment. There is no GCP staging or production deployment.
- **The DAO operations vault is a treasury concept, not a repository or a live vault.** The afi-config vault-address registry (a draft, read-only descriptive artifact) records `ops.afidao.eth` (`AFI_OPS_VAULT_PLACEHOLDER`) as a **placeholder**: an empty 1-of-1 Safe on Ethereum mainnet with no balance and no executed transactions — not funded, not DAO-controlled, and not a runtime authority. It names an intended future operations-funding vault; it does not route funds today and is not a participant claim role.

---

## How to read AFI today

| You are a… | Start with |
|---|---|
| **Developer** | `afi-reactor` (runtime) and `afi-core` (scoring library), then the contracts in `afi-config`. |
| **Analyst / strategy author** | the UWR profile registry and KATs in `afi-config`; author pipelines and configs with `afi-factory`. |
| **Validator** | the `scored-signal-evidence` v3 schema and vectors in `afi-config`; store semantics in `afi-infra`. |
| **Operator** | `afi-gateway` (submission boundary) and `afi-infra` (canonical store). |
| **Researcher** | `afi-docs`, `afi-econ`, `afi-benchkit`, and the frozen record in `afi-artifacts`. |

Conformance is defined by the contracts, registries, and KATs — a conforming analyst pipeline needs no permission. Authority lives in `afi-governance`, `afi-config`, and `afi-math`; everything else is a replaceable implementation of those contracts.
