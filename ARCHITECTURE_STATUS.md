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

AFI does **not** use **LangChain**, **LangGraph**, **LangSmith**, or **LangServe** for protocol orchestration. There is no `@langchain/langgraph` dependency in the reactor or core runtime.

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

**`afi-gateway`** is an optional **Eliza-based client** for character UX. It calls AFI HTTP APIs (`afi-reactor`, `afi-core`) and does **not** own signal scoring, validation, or minting logic.

Installing gateway dependencies may pull **transitive** `langchain` / `langsmith` packages via `@elizaos/core`. Those are **gateway-only** and are not used by AFI Reactor DAG execution.

---

## Historical LangGraph documentation

Planning documents that reference `src/langgraph/`, `LangGraphOrchestrator`, `@langchain/langgraph`, `LangGraphNode`, or `LangGraphState` are **archived** and superseded:

- [`afi-docs/archive/langgraph-migration-2025/`](archive/langgraph-migration-2025/)

Do not treat archived files as current implementation guidance.

---

## Terminology (current)

| Use | Avoid (legacy) |
|-----|----------------|
| AFI Reactor pipeline / DAG | LangGraph integration |
| Pipehead | LangGraphNode |
| PipelineState | LangGraphState |
| DAG orchestrator / `DAGExecutor` | LangGraph orchestrator |
| `src/dag/` | `src/langgraph/` |
