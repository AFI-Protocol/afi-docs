# PURGE_MANIFEST — Legacy Froggy Demo Pipeline

**Date:** 2026-06-18
**Mission:** Remove the deprecated Froggy *demo chain* (Alpha Scout → Pixel Rick → Val Dook → Execution Sim) from the AFI monorepo. The canonical spine is the **scored-only** USS v1.1 pipeline: `uss-telemetry-deriver → (tech-pattern ∥ sentiment-news) → enrichment-adapter → froggy-analyst (UWR) → tssd-vault-write`. Validator certification and execution are **not** the reactor's responsibility.

Classification legend: **DELETE** (removed) · **REWRITE** (edited to scored-only) · **KEEP** (left intact, with reason).

---

## DELETE — plugin files (afi-reactor/plugins/)

| File | Reason |
|------|--------|
| `alpha-scout-ingest.plugin.ts` | Dev/demo ingest (Alpha Scout); replaced by webhook-level USS validation. No runtime importer. |
| `signal-structurer.plugin.ts` | Dev/demo structurer (Pixel Rick); replaced by canonical USS v1.1 schema. No runtime importer. |
| `validator-decision-evaluator.plugin.ts` | Dev/demo validator (Val Dook); moved to external certification layer. No runtime importer. |
| `execution-agent-sim.plugin.ts` | Dev/demo execution sim; moved to consumer/adapter layer. No runtime importer. |
| `plugins/_deprecated_ingest/` | **Did not exist** — confirmed absent monorepo-wide. |

## DELETE — tests

| File | Reason |
|------|--------|
| `afi-reactor/test/froggyPipeline.test.ts` | Tested the full dead chain and `import`ed non-existent `../plugins/_deprecated_ingest/*` (already broken). Was unmatched by jest. Scored-only contract is already covered by `froggyWebhookService.test.ts` (asserts `validatorDecision`/`execution` are `undefined`). |

## REWRITE — codex config (afi-reactor/config/)

| File | Change |
|------|--------|
| `dag.codex.json` | Removed the 7-node Froggy demo subgraph (`alpha-scout-ingest`, `pixelrick-structurer`, `froggy-enrichment-adapter`, `froggy-analyst-node`, `froggy-ensemble-scorer`, `execution-sim-node`, `froggy-vault-echo`). 15 → 8 nodes. The 8 retained nodes are non-demo analyzers/governance/persistence. |
| `ops.codex.json` | Replaced the `froggy-trend-pullback-v1` demo pipeline (Alpha Scout → … → Execution Sim → Vault) with a `reference_only` entry citing the canonical stage IDs from `src/config/froggyPipeline.ts`. The two active pipelines are unchanged. |
| `schema.codex.json` | Removed the 5 schema entries whose `linkedDAGNode` was a purged node (`reactor-signal-envelope`, `base-signal`, `froggy-enriched-view`, `froggy-trend-pullback-score`, `execution-result`). 15 → 10 entries. (No test asserts schema count.) |

## REWRITE — reactor tests

| File | Change |
|------|--------|
| `test/guardrails/no-legacy-ingest.test.ts` | Inverted: now asserts the legacy plugins/nodes/personas are **gone** (not quarantined), that no `_deprecated_ingest/` exists, and that the codex configs contain no purged IDs. **Wired into jest** (`testMatch` + removed from `testPathIgnorePatterns`) so it now runs and guards against regression. |
| `test/novelty/noveltyScoring.test.ts` | Removed the dependency on the deleted `validator-decision-evaluator` plugin; reduced to a deferred scored-only placeholder (novelty belongs to the external certification layer). |
| `test/vaultReplayService.test.ts` | Refactored to scored-only replay semantics over `ReactorScoredSignalV1`; removed the broken `TssdSignalDocument` import and all `validator-decision-evaluator@vX` version strings. |
| `jest.config.js` | Added the guardrail to `testMatch`; removed `test/guardrails/` from `testPathIgnorePatterns`. |

## REWRITE — gateway (afi-gateway/)

| File | Type | Change |
|------|------|--------|
| `plugins/afi-reactor-actions/index.ts` | code | **KEEP** — runtime already migrated to `SUBMIT_SIGNAL_DRAFT` / `EXPLAIN_LAST_DECISION`. |
| `src/afiClient.ts` | code | Scored-only types already correct; neutralized an "Alpha Scout" / "simulated execution" header comment. |
| `src/afiCli.ts` | code | `SUBMIT_FROGGY_DRAFT` → `SUBMIT_SIGNAL_DRAFT`; removed "(via Alpha Scout)". |
| `scripts/afi-reactor-actions-smoke.ts` | script | Action-name references updated to match runtime. |
| `plugins/afi-reactor-actions/README.md` | doc (active) | Rewritten to scored-only contract (`ReactorScoredSignalV1`); removed `validatorDecision`/`execution` blocks and dead personas. |
| `docs/AFI_REACTOR_INTEGRATION.md` | doc (active) | Rewritten: action names, scored-only response, canonical 6-stage pipeline; validator/execution marked downstream. |
| `docs/INTEGRATION_COMPLETE_SUMMARY.md` | doc (historical) | One-line historical banner added; body preserved. |
| `docs/MODEL_PROVIDER_FIX.md` | doc (historical) | One-line historical banner added; body preserved. |

## REWRITE — active docs (afi-reactor, afi-docs, afi-core)

| File | Change |
|------|--------|
| `afi-reactor/AGENTS.md` | Removed the Alpha Scout → … → Execution Sim agent chain as the current flow; documents the canonical scored-only pipeline + `ReactorScoredSignalV1`. |
| `afi-reactor/docs/HTTP_WEBHOOK_SERVER.md` | Response body and pipeline-flow sections rewritten to the scored-only contract. |
| `afi-docs/AFI_Docs_Inventory.md` | Fixed the `FROGGY_TREND_PULLBACK_PIPELINE` stage list (removed `validator-decision`, `execution-sim`); now the canonical 6 stages. |
| `afi-docs/AFI_System_Atlas.md` | Removed `validator-decision-evaluator.plugin.ts` as a current plugin; trimmed dead personas from the character list. |
| `afi-docs/AFI_Full_Architecture.md` | Prose/agent lists + ASCII box updated: Phoenix active; Alpha Scout / Pixel Rick / Val Dook / Execution Sim marked removed. |
| `afi-core/docs/MATH_INDEX.md` | Rewrote the "Signal Flow (Prize Demo)" diagram + "Prize Demo" mentions to the canonical scored-only flow. UWR/Decay/Novelty math preserved. |
| `afi-infra/schemas/enrichment_common.ts` | Neutralized one illustrative "Pixel Rick" doc-comment word. Schema/type untouched. |

## REWRITE — comment/example cleanups (kept files)

| File | Change |
|------|--------|
| `afi-reactor/plugins/froggy-enrichment-adapter.plugin.ts` | Stale `Part of: … (Alpha → Pixel Rick → … → Execution Sim)` comment → canonical scored-only description; `@param` "from Pixel Rick" neutralized. Plugin logic untouched. |
| `afi-reactor/plugins/froggy.trend_pullback_v1.plugin.ts` | Same stale "Part of:" comment → canonical. Logic untouched. |
| `afi-core/analysts/froggy.enrichment_adapter.ts` | "Pixel Rick" illustrative comment word neutralized. Type untouched. |
| `afi-core/validators/UniversalWeightingRule.ts` | "(e.g., Val Dook)" comment → "(e.g., certification validators)". UWR logic/types untouched. |
| `afi-config/examples/usignal/v1_1/minimal-runtime.example.json` | Example `providerId` `"alpha-scout-001"` → `"example-provider-001"` (not referenced by any test). |

## KEEP — historical docs (banner added, body preserved)

`afi-docs/AFI_PIPELINE_AUDIT_REPORT.md`, `afi-docs/agentic_legos_architecture_analysis.md`, `afi-reactor/AGENTS_AUDIT_REPORT.md`, `afi-reactor/AGENTS_AUDIT_VALIDATION_REPORT.md`, `afi-core/docs/ENRICHMENT_PROFILE_SPEC.v0.1.md` (illustrative-persona note).

## KEEP — historical analyses (intentionally untouched, obviously dated reports)

`AFI_CORE_BRANCH_ANALYSIS_REPORT.md`, `AFI_REACTOR_AUGMENTCODE_AUDIT_REPORT.md`, `AFI_REACTOR_BRANCH_ANALYSIS_REPORT.md`, `AFI_REACTOR_BRANCH_CLEANUP_ANALYSIS.md`, `AFI_REACTOR_MAIN_VS_DEMO_LIVE_ANALYSIS.md`, `AFI_REACTOR_MERGE_DEMO_LIVE_INTO_MAIN_PLAN.md` — dated branch/merge analysis artifacts; not current docs.

## KEEP — protocol / canonical (untouched logic; hard rules honored)

| File | Reason |
|------|--------|
| `afi-core/validators/ValidatorDecision.ts` | Protocol type for the future certification layer. **Untouched.** |
| `afi-core/docs/VALIDATOR_DECISION_SPEC.v0.1.md` | Normative-adjacent spec. |
| `afi-mint` `state.validatorDecision` / `SignalStateManager` | Mint orchestration FSM, not a reactor plugin. |
| `afi-reactor` canonical Froggy plugins (`froggy-enrichment-{tech-pattern,sentiment-news,adapter}.plugin.ts`, `froggy.trend_pullback_v1.plugin.ts`) | Active scoring path (comments-only cleanup above). |
| `afi-reactor/src/config/froggyPipeline.ts` | Already canonical; REMOVED STAGES comment verified accurate; no imports of purged plugins. |
| `afi-reactor/src/services/froggyDemoService.ts` | Already canonical; no dead imports. |
| `afi-docs/specs/audit/**` (recon, themes, transcripts, `AFI_LEGACY_PIPELINE_PURGE_PROMPT.md`) | Forensic audit corpus — left intact by design. |

## OUT OF SCOPE (observed, not changed)

- **Pre-existing afi-core build break:** `afi-core` fails `tsc` (`ValidatorDecision.ts` missing `../analyst/AnalystScoreTemplate.js`; `froggy.trend_pullback_v1.ts` missing `scoredAt`) and ships an incomplete `dist/`. This blocks `npm install` via the `file:` dep's `prepare` hook. Worked around for testing with `--ignore-scripts` (afi-core `prepare` temporarily neutralized, then restored — net-zero diff). Not fixed (afi-core is out of scope).
- **uwrAxes naming drift:** `afi-gateway/src/afiClient.ts` declares `uwrAxes { utility, workQuality, rarity }`, while the reactor's canonical axes are `{ structure, execution, risk, insight }`. Pre-existing inconsistency, unrelated to the demo-chain purge.
