# PURGE_RESULTS — Legacy Froggy Demo Pipeline

**Date:** 2026-06-18
**Verification tool:** real ripgrep binary `/home/user/.factory/bin/rg` (v13.0.0). *Note: the shell-aliased `rg` is rewritten by the RTK proxy hook and returned unreliable output; all evidence below used the real binary.*

---

## Definition of Done

| Check | Status | Evidence |
|-------|--------|----------|
| Four legacy plugin files deleted | ✅ | `plugins/` no longer contains `alpha-scout-ingest`, `signal-structurer`, `validator-decision-evaluator`, `execution-agent-sim` |
| `_deprecated_ingest/` absent | ✅ | `find` returns nothing monorepo-wide |
| `dag.codex.json` has no purged node IDs | ✅ | 15 → 8 nodes; sweep = 0 legacy IDs |
| `ops.codex.json` demo pipeline gone / `reference_only` | ✅ | `froggy-trend-pullback-v1` → `status: "reference_only"`, canonical flow, no legacy names |
| `schema.codex.json` no purged `linkedDAGNode` | ✅ | 15 → 10 entries |
| `froggyPipeline.test.ts` legacy chain gone | ✅ | deleted |
| `no-legacy-ingest` guardrail passes | ✅ | rewritten to assert purged state; **wired into jest**; passes |
| `afi-reactor npm test` passes | ✅ | **10 suites / 425 tests passed** |
| Gateway smoke script + actions updated | ✅ | `SUBMIT_SIGNAL_DRAFT` / `EXPLAIN_LAST_DECISION` |
| `PURGE_MANIFEST.md` + `PURGE_RESULTS.md` written | ✅ | this directory |
| `afi-core/ValidatorDecision.ts` untouched | ✅ | 0 legacy refs; not modified |

---

## Search-pattern results (mission patterns)

Scope rule: **zero hits required in code/config** (everything except the audit archive and intentionally-retained historical docs). Run from repo root, excluding `node_modules`/`.git`.

```
# 1  alpha-scout-ingest|alpha-scout|alphaScout
# 2  signal-structurer|pixelrick-structurer|pixelrick|Pixel Rick
# 3  validator-decision-evaluator|validator-decision-node|validator-decision[^/]
# 4  execution-agent-sim|execution-sim-node|execution-sim
# 5  Val Dook|Alpha Scout|SUBMIT_FROGGY_DRAFT|EXPLAIN_LAST_FROGGY
# 6  _deprecated_ingest
```

### CODE / CONFIG (excludes `*.md`, `specs/audit/**`) — only intentional self-references remain

```
afi-reactor/src/config/froggyPipeline.ts            : 4   (REMOVED STAGES doc comment — mission says keep)
afi-reactor/test/guardrails/no-legacy-ingest.test.ts: 16  (guardrail's own assertion constants/comments)
```

Both are **intentional and self-documenting**:
- `froggyPipeline.ts` lines 90-94 are the `REMOVED STAGES:` comment the mission explicitly asks to keep ("verify REMOVED STAGES comment still accurate").
- `no-legacy-ingest.test.ts` must name the legacy IDs as the very strings it asserts are absent.

Every other runtime/config file that previously matched is now clean, including the active rewrites that dropped to **0**: `afi-gateway/plugins/afi-reactor-actions/README.md`, `afi-gateway/docs/AFI_REACTOR_INTEGRATION.md`, `afi-docs/AFI_Docs_Inventory.md`, `afi-docs/AFI_System_Atlas.md`, `afi-docs/AFI_Full_Architecture.md`, `afi-core/docs/MATH_INDEX.md`, `afi-reactor/docs/HTTP_WEBHOOK_SERVER.md`, `afi-reactor/AGENTS.md`, `afi-infra/schemas/enrichment_common.ts`, and the gateway code (`afiCli.ts`, `afiClient.ts`, `afi-reactor-actions-smoke.ts`).

### DOCS still carrying references — all intentional (historical), none active/misleading

| File | Hits | Disposition |
|------|------|-------------|
| `afi-core/docs/ENRICHMENT_PROFILE_SPEC.v0.1.md` | 11 | Illustrative-persona note banner added; `EnrichmentProfile` is a durable protocol type |
| `afi-docs/AFI_PIPELINE_AUDIT_REPORT.md` | 18 | Historical banner |
| `afi-docs/agentic_legos_architecture_analysis.md` | 3 | Historical banner |
| `afi-gateway/docs/INTEGRATION_COMPLETE_SUMMARY.md` | 7 | Historical banner |
| `afi-gateway/docs/MODEL_PROVIDER_FIX.md` | 3 | Historical banner |
| `afi-reactor/AGENTS_AUDIT_REPORT.md` | 6 | Historical banner |
| `afi-reactor/AGENTS_AUDIT_VALIDATION_REPORT.md` | 2 | Historical banner |
| `afi-docs/AFI_CORE_BRANCH_ANALYSIS_REPORT.md` | 1 | Dated branch analysis — left intact |
| `afi-docs/AFI_REACTOR_AUGMENTCODE_AUDIT_REPORT.md` | 4 | Dated audit report — left intact |
| `afi-docs/AFI_REACTOR_BRANCH_ANALYSIS_REPORT.md` | 1 | Dated branch analysis — left intact |
| `afi-docs/AFI_REACTOR_BRANCH_CLEANUP_ANALYSIS.md` | 2 | Dated branch analysis — left intact |
| `afi-docs/AFI_REACTOR_MAIN_VS_DEMO_LIVE_ANALYSIS.md` | 2 | Dated branch comparison — left intact |
| `afi-docs/AFI_REACTOR_MERGE_DEMO_LIVE_INTO_MAIN_PLAN.md` | 1 | Dated merge plan — left intact |

### AUDIT CORPUS (`afi-docs/specs/audit/**`) — 9 files, left intact by design

The forensic recon corpus, `themes/*.json`, `AFI_RECON_CORPUS.json`, the `AFI_FROGGY_MAGE_MIGRATION_MAP.md` DROP rows, and `AFI_LEGACY_PIPELINE_PURGE_PROMPT.md` (the purge prompt itself) intentionally retain the legacy names as the investigation record. Per mission: do not mass-edit the audit corpus.

---

## Test evidence

```
$ cd afi-reactor && npx jest
Test Suites: 10 passed, 10 total
Tests:       425 passed, 425 total
```

Suites run by `npm test` (`testMatch`): `dagConfigShape`, `froggyWebhookService`, **`guardrails/no-legacy-ingest` (newly wired in)**, `state-management`, `integration/state-lifecycle`, and `src/dag/__tests__/*`.

- `dagConfigShape.test.ts` validates the rewritten `dag.codex.json` (8 well-formed nodes).
- `froggyWebhookService.test.ts` asserts the scored-only contract (`validatorDecision`/`execution` are `undefined`) — the canonical replacement for the deleted `froggyPipeline.test.ts`.
- `no-legacy-ingest.test.ts` actively fails if any legacy plugin/node/persona is reintroduced.

### Environment note (pre-existing, out of scope)

`afi-core` does not build (`tsc` errors in `ValidatorDecision.ts` and `froggy.trend_pullback_v1.ts`) and ships an incomplete `dist/`, which blocks `npm install` through afi-reactor's `file:../afi-core` `prepare` hook. Installed with `--ignore-scripts` (afi-core `prepare` temporarily neutralized for the install, then **restored** — afi-core net-zero diff). These afi-core errors are unrelated to the purge and were not fixed.

---

## Not committed

No commits were made (repository is not a git repo; the mission says do not commit unless asked).
