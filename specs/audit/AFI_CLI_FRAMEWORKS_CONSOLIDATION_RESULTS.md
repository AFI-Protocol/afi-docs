# CLI Framework Consolidation Results

**Date:** 2026-06-19
**Charter:** [`AFI_CLI_FRAMEWORKS_DECISIONS.md`](./AFI_CLI_FRAMEWORKS_DECISIONS.md) (binding) · [`AFI_CLI_FRAMEWORKS_INVESTIGATION.md`](./AFI_CLI_FRAMEWORKS_INVESTIGATION.md) (evidence)
**Status:** ✅ Executed and pushed (6 repos). Verification gate passed (pre-existing unrelated issues noted).

---

## Summary (what changed, per repo)

| Repo | Change |
|------|--------|
| **afi-docs** | `AFI_Repository_Map.md`: removed phantom `afi-cli-framework → afi-cli-shared` edge + corrected stale `afi-pipeline`/`afi-agents` (neither repo exists) → canonical `afi-gateway → afi-reactor` spine. Added **RETIRED** banner to the 6 CLI-governance docs. Linked investigation/decisions/results from `specs/audit/README.md`. Added this results doc + the consolidation prompt. |
| **afi-cli-framework** | Added `"prepare": "npm run build"` so consumers' `npm ci` always produces `dist/`. README install section now states **monorepo-sibling `file:` link only** (removed false `npm install @afi/cli-framework`). |
| **afi-ops** | **Rehomed** `scripts/lib/afi-shared.sh` here (canonical cross-repo bash-ops home). README documents it + the `AFI_SHARED_SH` override env var. |
| **afi-benchkit** | All 4 scripts now source `${AFI_SHARED_SH:-$REPO_ROOT/../afi-ops/scripts/lib/afi-shared.sh}`. This fixes the `lock/{compile,refresh}.sh` **off-by-one `../../`** bug (was escaping above the monorepo) and repoints `generate_benchmarks.sh`/`capsule_run.sh` to the new afi-ops home. |
| **afi-cli-shared** | **Deprecated.** Deleted the Python package (`src/afi_cli_shared/`, `tests/`, `pyproject.toml`, `egg-info/`) + committed artifacts (`.coverage`, `__pycache__`) + the rehomed bash lib. Repo reduced to `DEPRECATED.md` (tombstone → afi-ops) + `.gitignore`. Python `pip install` **not** fixed (per decision). |
| **afi-gateway** | **Removed** the `eliza-demo` and `validator <subcommand>` CLI verbs from `src/cli.ts` + `src/afiCli.ts` (incl. `runAfiElizaDemoFlow` + `getLastValidatorDecisionSummary` + the disabled-message paths). Rewrote `getAfiCliHelp()` to a scored-only surface (`reactor status` + USS webhook + testnet-checklist pointer). Renamed `SUBMIT_SIGNAL_DRAFT → SUBMIT_TRADINGVIEW_SIGNAL` and `TradingViewLikeDraft → TradingViewWebhookPayload` (28 replacements across 7 files). Kept `reactor status` (on-spine `/health`). |

---

## Verification table (command → pass/fail)

| Check | Command | Result |
|-------|---------|--------|
| Framework install builds dist (prepare) | `afi-cli-framework: rm -rf node_modules && npm ci` | ✅ exit 0 — `prepare`/`tsc` ran |
| Framework tests | `afi-cli-framework: npm test` | ✅ **53/53** (6 suites) |
| Gateway install + typecheck | `afi-gateway: npm ci && npm run typecheck` | ⚠️ **my edits clean**; 2 **pre-existing unrelated** errors only¹ |
| Gateway action tests (renamed) | `afi-gateway: npx vitest run afi-reactor-actions` | ✅ **10/10 PASS** |
| Benchkit script syntax | `bash -n` ×4 (`generate_benchmarks`, `capsule_run`, `lock/compile`, `lock/refresh`) | ✅ **4/4 OK** |
| Rehomed lib resolves + sources | `source afi-ops/scripts/lib/afi-shared.sh; type log_info` | ✅ resolves + `log_info` defined |
| Legacy CLI surface (active) | `rg "eliza-demo\|validator explain-last\|explain-last\|SUBMIT_SIGNAL_DRAFT" afi-gateway/src afi-gateway/plugins/afi-reactor-actions` | ✅ **ZERO** |
| Phantom dependency edge | `rg "afi-cli-framework.*afi-cli-shared\|uses utilities from afi-cli-shared" afi-docs` | ✅ removed from `AFI_Repository_Map.md`; residual hits are benign (see below) |

¹ Gateway `tsc --noEmit` reports exactly two errors, **neither in a file this change touched**: `src/server-full.ts:44` `Cannot find module '@elizaos/server'` (missing optional dep) and `../afi-infra/schemas/enrichment_common.ts:1` `Cannot find module 'zod'` (afi-infra's own node_modules). Both pre-date this work and are out of scope. The full-project typecheck reported **no** errors in `cli.ts`, `afiCli.ts`, `afiClient.ts`, or the plugin.

---

## Commits pushed (repo → SHA)

| Repo | SHA | Branch | Push |
|------|-----|--------|------|
| afi-cli-framework | `59cadf1` | main | ✅ `5b46ed4..59cadf1` |
| afi-ops | `35594a5` | main | ✅ `b9c6ea7..35594a5` |
| afi-benchkit | `de3da7c` | main | ✅ `e3bb1b8..de3da7c` |
| afi-cli-shared | `49649b0` | main | ✅ `fc9d0f0..49649b0` |
| afi-gateway | `262fa30` | main | ✅ `6f7fa8f..262fa30` |
| afi-docs | _(this commit)_ | main | pushed with this doc |

No branch protection blocked any push (all direct to `main`, per charter). Auth: `gh`/SSH as `Gio2050`.

---

## Remaining hits (with justification)

The phantom-dependency `rg` sweep over `afi-docs` still returns matches, **all benign** — the actual false edge (`AFI_Repository_Map.md:172,188` "afi-cli-framework uses utilities from afi-cli-shared") is **gone**:

- **Alphabetical 31-repo enumerations** — `AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md:179`, `AFI_REFERENCE_IMPL_MAP.md:112` (+ `final/` copy), `themes/B-reference-impl.json` (audit corpus). The two names are adjacent in a sorted repo list; no dependency asserted.
- **Investigation/decisions records** — `AFI_CLI_FRAMEWORKS_INVESTIGATION.md` / `AFI_CLI_FRAMEWORKS_DECISIONS.md` quote the phantom string precisely to **document that it was false**. Intentional.
- **RETIRED-bannered governance docs** — `AFI_CLI_MAINTENANCE_SCHEDULE.md:53`, `AFI_CLI_GOVERNANCE_COMMITTEE_CHARTER.md:31` list both repos in now-retired enumerations (each carries the RETIRED banner).

Gateway typecheck residuals: the two pre-existing unrelated module-resolution errors above (out of scope).

---

## Deferred items

- **Archive the `afi-cli-shared` GitHub repo** — left as a `DEPRECATED.md` tombstone; archiving deferred pending an external-link check (DECISIONS open item).
- **`afi-ops` CI** — no `bash -n` workflow added for `afi-shared.sh` consumers (DECISIONS open item).
- **Rename blast radius** — `SUBMIT_TRADINGVIEW_SIGNAL`/`TradingViewWebhookPayload` were confirmed **gateway-only** (8 files; no external Eliza action registry). No follow-up issue needed.
- **Cosmetic** — the `draft` parameter name in `afiClient.ts runFroggyTrendPullback(draft)` and the "TradingView-like signal draft" docstring were left as-is (the verb/type identifiers were the binding rename targets).
- **Repository_Map repo-description sections** — only the dependency diagram + integration points were corrected (binding scope). The standalone `### afi-pipeline` / `### afi-agents` description sections (for non-existent repos) remain as a minor doc-hygiene follow-up.
- **Pre-existing build gaps (not introduced here)** — gateway `@elizaos/server` missing dep; `afi-infra` missing `zod`.

---

## Recommended next action

Archive the `afi-cli-shared` GitHub repo (after a quick external-link check), then proceed to **Phase A1 (Mage/GCP)** per [`AFI_FROGGY_MAGE_MIGRATION_MAP.md`](./AFI_FROGGY_MAGE_MIGRATION_MAP.md) — neither CLI library is on the testnet critical path, so this consolidation unblocks doc/ops hygiene without touching the A1 spine.
