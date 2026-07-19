# AFI Protocol — Architecture Status

**Last updated:** 2026-07-19  
**Purpose:** Orchestration-focused status snapshot of how AFI scoring is implemented today. The organization-wide current-state map is [AFI_Full_Architecture.md](AFI_Full_Architecture.md).

---

## Orchestration model

**AFI Reactor** (`afi-reactor`) is a **manifest-driven, analyst-configurable graph executor**
(accepted decision: afi-governance `decisions/factory-configurable-pipelines-v1.md`).

- Pipelines are **registered, never hardcoded**: at boot the runtime validates the
  governed registries in `afi-config` (`registries/analysis-plugins`,
  `registries/pipelines`, `registries/analyst-strategies`,
  `registries/provider-bindings`, and the FLPR-GOV enrichment-provider
  registries `registries/providers`, `registries/provider-instances`,
  `registries/credential-refs`) and refuses to start on any invalid active
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
- **Evidence**: the Reactor constructs `afi.scored-signal-evidence.v3` records —
  the sole current canonical evidence contract — carrying a thin
  `afi.composition-ref.v1` composition reference (pipeline identity,
  analyst-config hash, scorer and plugin-set references, hash-addressed
  execution summaries), exactly five credential-safe per-lane provider
  invocation proofs (`afi.provider-invocation-proof.v1`, unique by category,
  deterministically ordered; the `aiMl` proof nests the Tiny Brains invocation
  proof `afi.aiml-invocation-proof.v1`), and record-level
  `recordHash`/`replayHash` commitments; `afi-infra` validates, hash-verifies,
  and persists them at the sole canonical persistence interface.
- **Evaluation completeness**: a scored evaluation requires all five category
  lanes to succeed (EV3-GOV) — every lane node in the registered manifest is
  fail-fast, and a failed lane yields no scored evaluation, no scored signal,
  and no evidence record (bounded operational diagnostics only).

Implementation lives under:

- `afi-reactor/src/pipeline/` — graph executor, plugin registry, registry loader,
  the five provider-backed lane bindings, the five-category join and scorer
  terminal, canonical hashing, execution summaries
- `afi-reactor/src/providers/` — the sole enrichment-execution seam (FLPR-GOV):
  the static adapter registry, provider/instance/credential-ref resolution, the
  least-privilege SecretResolver, canonical category-output validation, and the
  trusted service clients
- `afi-reactor/src/config/runtimeComposition.ts` — the boot-validated composition root

---

## Related source of truth

| Concern | Repo / path |
|---------|-------------|
| Graph orchestration | `afi-reactor/src/pipeline/` |
| Pipeline authoring (templates, validation, hashing) | `afi-factory` |
| Validators, scoring, decay | `afi-core` |
| Schemas & registries (USS, `afi.pipeline.v1` family, evidence v3) | `afi-config/schemas/`, `afi-config/registries/` |
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
| Composition reference | The thin `afi.composition-ref.v1` object carried on `afi.scored-signal-evidence.v3`, binding evidence to the executed composition by canonical hashes |
| District 1 — Signal Evaluation | The **active** Signal Evaluation capability and authority domain (`district-one-signal-evaluation-capability-v0.1`, D1CAP-GOV): canonical input → five-category enrichment → deterministic join → analyst/scorer/UWR seam → District-2 handoff. Its current implementation is the live GraphExecutor pipeline (`afi-reactor/src/pipeline/`); implementations may be replaced through accepted authority without retiring the district |
| District 2 — Evidence & Provenance | The active canonical data & provenance boundary: receives the scored evaluation result from District 1 and owns evidence construction, validation, and the canonical persistence handoff. Live law in `afi-reactor/src/evidence/provenance/` |
| Pipehead | The bounded stage discipline of the Pipehead Addendum (one node → one validated category result → merge → one scorer seam), implemented today by the live pipeline nodes. District 1's former non-production Pipehead POC implementation was retired and deleted by Mission A (DSC-GOV) — an implementation retirement only, not a District retirement (D1CAP-GOV); git history preserves the former implementation |
