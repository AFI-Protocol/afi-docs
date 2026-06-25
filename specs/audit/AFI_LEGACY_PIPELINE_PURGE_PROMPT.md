# Claude Code Prompt — Legacy Demo Pipeline Purge

**Mission:** Remove the deprecated Froggy **demo chain** from the AFI monorepo. We are AFI — ingest → score → evidence → (later) mint. Not Alpha Scout → Pixel Rick → Val Dook → execution sim.

**Canonical spine (keep):** USS v1.1 ingest → `uss-telemetry-deriver` → Froggy enrichment → `froggy-analyst` (UWR) → Mongo TSSD vault write. See [`froggyPipeline.ts`](../../../afi-reactor/src/config/froggyPipeline.ts) REMOVED STAGES comment.

**Copy-paste prompt below.**

---

```
# MISSION: Purge legacy demo pipeline (seek & destroy)

Remove all runtime, config, test, and **active** documentation references to the deprecated Froggy demo chain:

| Legacy ID | Plugin / alias | Persona (dead) |
|-----------|----------------|----------------|
| alpha-scout-ingest | alpha-scout-ingest.plugin.ts | Alpha Scout |
| signal-structurer | signal-structurer.plugin.ts | Pixel Rick |
| validator-decision | validator-decision-evaluator.plugin.ts | Val Dook |
| execution-sim | execution-agent-sim.plugin.ts | Execution Agent Sim |

Related codex node IDs to remove or rewrite:
- alpha-scout-ingest, pixelrick-structurer, execution-sim-node
- ops.codex.json flow: validator-decision-node (referenced but may be missing from dag.codex.json — remove from flow)
- froggy-trend-pullback-v1 demo pipeline in ops.codex.json (entire entry or rewrite to match canonical 6-stage pipeline)

## HARD RULES — DO NOT DELETE OR BREAK

These share names but are NOT the legacy reactor plugins:

| Keep | Why |
|------|-----|
| `afi-core/validators/ValidatorDecision.ts` | Protocol type for future certification layer |
| `afi-core/docs/VALIDATOR_DECISION_SPEC.v0.1.md` | Normative-adjacent spec |
| `afi-mint` `state.validatorDecision` / `SignalStateManager` qualified/reject FSM | Mint orchestration, not reactor plugin |
| `afi-reactor` canonical Froggy plugins (enrichment, analyst, UWR) | Active scoring path |
| `afi-reactor/src/uss/*`, `cpj/*`, `froggyDemoService.ts` canonical USS path | Production ingest |
| `afi-docs/specs/audit/**` historical audit JSON/transcripts | Forensic record — update only if they falsely claim legacy is current; do not delete audit corpus |
| Purge-record DROP rows in the audit corpus | Intentional documentation of what was removed |

When `validatorDecision` appears in **replay/vault tests**, refactor fixtures to scored-only semantics — do not delete replay infrastructure blindly.

## SEARCH PATTERNS (run all; zero hits required in code/config except audit archive)

rg -n "alpha-scout-ingest|alpha-scout|alphaScout" --glob '!**/node_modules/**' --glob '!**/.git/**'
rg -n "signal-structurer|pixelrick-structurer|pixelrick|Pixel Rick" --glob '!**/node_modules/**'
rg -n "validator-decision-evaluator|validator-decision-node|validator-decision[^/]" --glob '!**/node_modules/**'
rg -n "execution-agent-sim|execution-sim-node|execution-sim" --glob '!**/node_modules/**'
rg -n "Val Dook|Alpha Scout|SUBMIT_FROGGY_DRAFT|EXPLAIN_LAST_FROGGY" --glob '!**/node_modules/**'
rg -n "_deprecated_ingest" --glob '!**/node_modules/**'

## KNOWN HIT LIST (start here; expand via ripgrep)

### Delete plugin files
- afi-reactor/plugins/alpha-scout-ingest.plugin.ts
- afi-reactor/plugins/signal-structurer.plugin.ts
- afi-reactor/plugins/validator-decision-evaluator.plugin.ts
- afi-reactor/plugins/execution-agent-sim.plugin.ts
- plugins/_deprecated_ingest/ (entire folder if exists)

### Rewrite config
- afi-reactor/config/dag.codex.json — remove nodes: alpha-scout-ingest, pixelrick-structurer, execution-sim-node; rewire froggy-enrichment-adapter input to USS-native entry (document new entry node or remove froggy demo subgraph)
- afi-reactor/config/ops.codex.json — remove or replace `froggy-trend-pullback-v1` demo pipeline (lines ~19-36); remove validator-decision-node, execution-sim-node, alpha-scout-ingest, pixelrick-structurer from flows
- afi-reactor/config/schema.codex.json — remove linkedDAGNode refs to purged nodes

### Tests — delete or rewrite
- afi-reactor/test/froggyPipeline.test.ts — **DELETE** or replace with USS v1.1 + canonical pipeline test (enrichment → analyst only; no scout/structurer/validator/execution)
- afi-reactor/test/guardrails/no-legacy-ingest.test.ts — **UPDATE**: assert plugins are **gone** (not quarantined in _deprecated_ingest); assert codex has **no** deprecated nodes at all
- afi-reactor/test/novelty/noveltyScoring.test.ts — remove validator-decision-evaluator dependency
- afi-reactor/test/vaultReplayService.test.ts — refactor fixtures using `validator-decision-evaluator@v0.1` strings to scored-only replay comparisons

### Gateway / Eliza demo layer
- afi-gateway/plugins/afi-reactor-actions/ — remove SUBMIT_FROGGY_DRAFT, EXPLAIN_LAST_FROGGY_DECISION if tied to validator/execution response shape; update to scored-only ReactorScoredSignalV1
- afi-gateway/src/afiClient.ts — remove TradingViewLikeDraft / validatorDecision / execution from response types if present
- afi-gateway/docs/AFI_REACTOR_INTEGRATION.md — rewrite to USS webhook + scored response only
- afi-gateway/plugins/afi-reactor-actions/README.md
- afi-gateway/scripts/afi-reactor-actions-smoke.ts

### Docs to update (active misleading — not audit archive)
- afi-reactor/AGENTS.md — remove Alpha Scout / Val Dook / execution sim agent chain
- afi-reactor/AGENTS_AUDIT_REPORT.md — add deprecation note or trim stale sections
- afi-docs/AFI_Docs_Inventory.md — fix froggyPipeline stage list (remove validator-decision, execution-sim)
- afi-docs/AFI_System_Atlas.md — remove validator-decision plugin reference as current
- afi-docs/AFI_PIPELINE_AUDIT_REPORT.md — add banner "historical" or update pipeline stages section

Do NOT mass-edit afi-docs/specs/audit/themes/*.json or recon corpus — those are investigation artifacts.

### Keep aligned with canonical pipeline
- afi-reactor/src/config/froggyPipeline.ts — verify REMOVED STAGES comment still accurate; no imports of purged plugins
- afi-reactor/src/services/froggyDemoService.ts — already canonical; ensure no dead imports

## EXECUTION ORDER

1. Ripgrep full monorepo; produce PURGE_MANIFEST.md listing every hit classified: DELETE | REWRITE | KEEP (with reason)
2. Delete plugin files
3. Rewrite dag.codex.json + ops.codex.json + schema.codex.json
4. Fix/delete tests; run `cd afi-reactor && npm test` until green
5. Clean gateway actions + docs
6. Update active afi-docs (not audit corpus)
7. Final ripgrep — paste zero-hit evidence for each search pattern in PURGE_RESULTS.md
8. Do NOT commit unless user asks

## REWRITE GUIDANCE

**ops.codex.json `froggy-trend-pullback-v1` replacement (suggested):**
- status: "deprecated" OR delete entry
- If kept for codex replay tool only: point to canonical stage IDs from froggyPipeline.ts (uss-telemetry-deriver → … → tssd-vault-write) with status "reference_only"

**Gateway actions replacement:**
- Single action: submit USS or TradingView webhook → returns ReactorScoredSignalV1 (signalId, analystScore, scoredAt, rawUss) — no validatorDecision, no execution block

**froggyPipeline.test.ts replacement sketch:**
- POST canonical USS fixture → runPipelineDag(FROGGY_TREND_PULLBACK_PIPELINE) → assert uwrScore bounds
- Or integration test against /api/webhooks/tradingview with mocked enrichment APIs

## DEFINITION OF DONE

| Check | Evidence |
|-------|----------|
| Four plugin files deleted | ls plugins/ — absent |
| dag.codex.json has no purged node IDs | rg on file |
| ops.codex.json demo pipeline gone or reference_only | file diff |
| froggyPipeline.test.ts legacy chain gone | test file |
| no-legacy-ingest guardrail passes | npm test |
| afi-reactor npm test passes | CI output |
| Gateway smoke scripts updated | manual or script run |
| PURGE_RESULTS.md written | afi-docs/specs/audit/PURGE_RESULTS.md |
| afi-core ValidatorDecision.ts untouched | git diff |

## OUT OF SCOPE

- Mongo removal (separate track)
- afi-mint Snapshot challenge logic
- Deleting afi-core ValidatorDecision types
```

---

## After the purge

Update the purge-record DROP section in the audit corpus if paths changed.

Link from [`AFI_TESTNET_E2E_CHECKLIST.md`](./AFI_TESTNET_E2E_CHECKLIST.md) optional housekeeping row if desired.
