# AFI CLI Frameworks — Consolidation Execution Prompt

**Status:** EXECUTED 2026-06-19 → see [`AFI_CLI_FRAMEWORKS_CONSOLIDATION_RESULTS.md`](./AFI_CLI_FRAMEWORKS_CONSOLIDATION_RESULTS.md)
**Binding decisions:** [`AFI_CLI_FRAMEWORKS_DECISIONS.md`](./AFI_CLI_FRAMEWORKS_DECISIONS.md)
**Investigation:** [`AFI_CLI_FRAMEWORKS_INVESTIGATION.md`](./AFI_CLI_FRAMEWORKS_INVESTIGATION.md) · [`.json`](./AFI_CLI_FRAMEWORKS_INVESTIGATION.json)

Execute the binding decisions from the CLI frameworks investigation — rehome bash
helpers, fix phantom docs, deprecate the dead Python package, align the gateway CLI
with the scored-only spine.

---

## Context (already decided — do not re-investigate)

- `afi-cli-framework` (TS/Commander) = **KEEP** — generic scaffolding, zero protocol coupling, 53/53 tests, one consumer (`afi-gateway`).
- `afi-cli-shared` (Python/Click + bash) = **CONSOLIDATE** — Python package broken (`pip install -e .` fails), zero Python consumers; only `scripts/lib/afi-shared.sh` is used (4 dormant benchkit scripts).
- **Neither repo is on the Phase A0/A1/A2 testnet critical path.**

### Canonical spine (do not reintroduce legacy verbs)
USS v1.1 ingest → Froggy 6-stage score → Pub/Sub `signal-scored` → BigQuery append-only → (later) afi-mint.

**Purged / deprecated (must not appear as live CLI surface):** `eliza-demo`, `validator explain-last`, the `validator-decision-evaluator` namespace, `SUBMIT_SIGNAL_DRAFT`/draft-handoff vocabulary, and the phantom doc claim "afi-cli-framework uses afi-cli-shared".

## Phases

**A — Docs correction (afi-docs)**
1. `AFI_Repository_Map.md`: remove phantom `afi-cli-framework → afi-cli-shared` edge; correct stale `afi-pipeline`/`afi-agents` references (both repos no longer exist) → `afi-gateway → afi-reactor`.
2. Add a `RETIRED (2026-06-19)` banner to the 6 CLI-governance docs (`AFI_CLI_STANDARDS_AND_GOVERNANCE`, `AFI_CLI_STANDARDIZATION_IMPLEMENTATION_PLAN`, `AFI_CLI_GOVERNANCE_COMMITTEE_CHARTER`, `AFI_CLI_REVIEW_PROCESS`, `AFI_CLI_MAINTENANCE_SCHEDULE`, `AFI_CLI_COMMUNICATION_PLAN`).
3. Link investigation/decisions/results from `specs/audit/README.md`.

**B — Mechanical fixes**
1. `afi-cli-framework`: add `"prepare": "npm run build"`; README → monorepo-sibling `file:` only.
2. `afi-ops`: rehome `scripts/lib/afi-shared.sh`; document `AFI_SHARED_SH` override.
3. `afi-benchkit`: repoint all 4 scripts to `${AFI_SHARED_SH:-$REPO_ROOT/../afi-ops/scripts/lib/afi-shared.sh}`; fix `lock/*.sh` off-by-one `../../`.
4. `afi-cli-shared`: delete the Python package + packaging + artifacts; reduce to `DEPRECATED.md` (→ afi-ops). Do **not** fix pip.

**C — Gateway alignment**
1. Remove `eliza-demo` + `validator <subcommand>` from `src/cli.ts` and `src/afiCli.ts` (REMOVE, not stub); keep `reactor status`.
2. Rewrite `getAfiCliHelp()` to a scored-only surface (USS webhook + testnet checklist).
3. Rename `SUBMIT_SIGNAL_DRAFT → SUBMIT_TRADINGVIEW_SIGNAL`, `TradingViewLikeDraft → TradingViewWebhookPayload` (gateway-only).

**D — Verify**
- `afi-cli-framework`: `npm ci && npm test` (expect 53/53).
- `afi-gateway`: `npm ci && npm run typecheck` + `vitest run afi-reactor-actions`.
- `afi-benchkit`: `bash -n` on the 4 scripts.
- `rg "eliza-demo|validator explain-last|SUBMIT_SIGNAL_DRAFT" afi-gateway/src afi-gateway/plugins` → zero.

## Hard rules
- Follow `AFI_CLI_FRAMEWORKS_DECISIONS.md` (binding). Commit per repo; push to GitHub. PR if branch protection blocks main.
- Do **not**: build gcloud/bq/cast operator CLIs on `CliApp`; publish to npm/PyPI; fix the afi-cli-shared Python packaging; migrate afi-benchkit Click → BaseCli; conflate `afi-core/validators/ValidatorDecision.ts` with the purged reactor plugin.

## Deliverable
`afi-docs/specs/audit/AFI_CLI_FRAMEWORKS_CONSOLIDATION_RESULTS.md` (summary, verification table, commits, remaining hits, deferred items, next action). Link it from `specs/audit/README.md`.
