# AFI Protocol — Architecture Status

**Last updated:** 2026-06-03  
**Purpose:** Single source of truth for how AFI orchestration is implemented today.

---

## Orchestration model

**AFI Reactor** (`afi-reactor`) is a **custom, deterministic TypeScript DAG orchestrator**.

- Signals flow through configured **pipeheads** (required and enrichment nodes).
- Execution uses explicit **pipeline state** (`PipelineState`), dependency ordering, and typed node contracts (`Pipehead`).
- **Codex** configuration and replay support auditability and reproducibility.

Implementation lives under:

- `afi-reactor/src/dag/` — `DAGBuilder`, `DAGExecutor`, `PluginRegistry`, core nodes, plugins
- `afi-reactor/src/types/pipeline.ts`, `afi-reactor/src/types/dag.ts` — pipeline types

---

## Related source of truth

| Concern | Repo / path |
|---------|-------------|
| DAG orchestration | `afi-reactor/src/dag/` |
| Validators, scoring, decay | `afi-core` |
| Schemas (USS, pipeline, analyst config) | `afi-config/schemas/` |
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
| AFI Reactor pipeline / DAG | The deterministic execution graph built and run in `afi-reactor/src/dag/` |
| Pipehead | A typed node contract (`afi-reactor/src/pipeheads/`) |
| PipelineState | Explicit execution state threaded through the DAG (`afi-reactor/src/types/dag.ts`) |
| `DAGBuilder` / `DAGExecutor` / `PluginRegistry` | DAG construction, deterministic execution, and plugin resolution (`afi-reactor/src/dag/`) |
| Core nodes / plugin nodes | The two node categories composing a pipeline (`src/dag/nodes`, `src/dag/plugins`) |
| Codex | Configuration and replay support for auditability and reproducibility |
