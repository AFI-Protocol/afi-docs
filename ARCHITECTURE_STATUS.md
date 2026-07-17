# AFI Protocol — Architecture Status

**Last updated:** 2026-07-17  
**Purpose:** Single source of truth for how AFI orchestration is implemented today.

---

## Orchestration model

**AFI Reactor** (`afi-reactor`) is a **manifest-driven, analyst-configurable graph executor**
(accepted decision: afi-governance `decisions/factory-configurable-pipelines-v1.md`).

- Pipelines are **registered, never hardcoded**: at boot the runtime validates the
  governed registries in `afi-config` (`registries/analysis-plugins`,
  `registries/pipelines`, `registries/analyst-strategies`,
  `registries/provider-bindings`) and refuses to start on any invalid active
  entry — honest failure, no demo/mock/fallback path.
- A pipeline graph is an **`afi.pipeline.v1` manifest** (governed contract home:
  `afi-config/schemas/pipeline/v1/`) composing **registered strategy nodes**
  across the five canonical analysis categories — `technical`, `pattern`,
  `sentiment`, `news`, `aiMl` — with explicit dependencies, deterministic joins,
  bounded declarative conditionals, and **exactly one scorer terminal** (the sole
  `VALIDATED → SCORED` transition).
- **Authoring lives in `afi-factory`**: pipeline/template authoring, template
  instantiation, manifest validation, and canonical (timestamp-free) hashing.
  Nothing the Factory emits is canonical until validated against the delegated
  `afi-config` contracts.
- **Evidence**: the Reactor constructs `afi.scored-signal-evidence.v2` records
  carrying a thin `afi.composition-ref.v1` composition reference (pipeline
  identity, analyst-config hash, scorer and plugin-set references, hash-addressed
  execution summaries); `afi-infra` validates and persists them at the sole
  canonical persistence interface.

Implementation lives under:

- `afi-reactor/src/pipeline/` — graph executor, plugin registry, registry loader,
  the five category nodes and scorer terminal, canonical hashing, execution summaries
- `afi-reactor/src/config/runtimeComposition.ts` — the boot-validated composition root

---

## Related source of truth

| Concern | Repo / path |
|---------|-------------|
| Graph orchestration | `afi-reactor/src/pipeline/` |
| Pipeline authoring (templates, validation, hashing) | `afi-factory` |
| Validators, scoring, decay | `afi-core` |
| Schemas & registries (USS, `afi.pipeline.v1` family, evidence v2) | `afi-config/schemas/`, `afi-config/registries/` |
| Canonical evidence store | `afi-infra` |
| On-chain mint | `afi-token` |
| Off-chain mint coordination | `afi-mint` |
| Validator benchmarks | `afi-benchkit` |

---

## Optional gateway (not orchestration)

**`afi-gateway`** is an optional **Eliza-based client** for character UX. It calls AFI HTTP APIs (`afi-reactor`, `afi-core`) and does **not** own signal scoring, validation, or minting logic. Its upstream ElizaOS dependency tree resolves third-party packages into the gateway's lockfile that AFI does not import or build on; see the gateway README's *Dependency provenance* note.

---

## Terminology (current)

| Term | Meaning |
|------|---------|
| AFI Reactor pipeline | A registered `afi.pipeline.v1` manifest executed by the Reactor's graph executor (`afi-reactor/src/pipeline/`) |
| Registered strategy | An analyst-strategy registry entry binding a pipeline, scorer, UWR profile, and decay configuration (`afi-config/registries/analyst-strategies/`) |
| Analysis category | One of the five canonical categories: `technical`, `pattern`, `sentiment`, `news`, `aiMl` |
| Scorer terminal | The exactly-one scoring node terminating a valid pipeline; performs the sole `VALIDATED → SCORED` transition |
| Composition reference | The thin `afi.composition-ref.v1` object carried on `afi.scored-signal-evidence.v2`, binding evidence to the executed composition by canonical hashes |
| Pipehead | A District-1 / District-2 M2 fenced reference surface (`afi-reactor/src/pipeheads/`) — non-production, not wired into the live executor |
