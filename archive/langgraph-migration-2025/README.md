# LangGraph-era architecture archive (2025)

Documents in this folder describe **superseded** planning and analysis from when AFI considered or labeled orchestration as "LangGraph integration."

**Current architecture:** AFI Reactor is a **custom, deterministic TypeScript DAG** under `afi-reactor/src/dag/`. Types use **Pipehead** and **PipelineState**. AFI does **not** use LangChain, LangGraph, LangSmith, or LangServe for protocol orchestration.

See [`../../ARCHITECTURE_STATUS.md`](../../ARCHITECTURE_STATUS.md) for the canonical status summary.

## Contents

| File | Summary |
|------|---------|
| `AFI_REACTOR_LANGGRAPH_IMPLEMENTATION_PLAN.md` | Planned `@langchain/langgraph` integration (not implemented) |
| `AFI_REACTOR_CONFIG_ARCHITECTURE_AND_DROID_MITIGATION.md` | Config split + proposed `LangGraphOrchestrator` |
| `AFI_ML_PROVIDER_ABSTRACTION_ARCHITECTURE.md` | ML provider design (stale `src/langgraph/` paths) |
| `AFI_LANGGRAPH_*` | Terminology elimination, Pipehead refactor, DAG analysis, scout/AI-ML plans |

Do not use these files as implementation guidance without cross-checking `afi-reactor`, `afi-core`, and `afi-config`.
