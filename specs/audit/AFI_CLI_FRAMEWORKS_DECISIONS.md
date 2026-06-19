# AFI CLI Frameworks — Human Decisions & Execution Charter

**Date:** 2026-06-19  
**Status:** BINDING (post-investigation)  
**Investigation:** [`AFI_CLI_FRAMEWORKS_INVESTIGATION.md`](./AFI_CLI_FRAMEWORKS_INVESTIGATION.md) · [`AFI_CLI_FRAMEWORKS_INVESTIGATION.json`](./AFI_CLI_FRAMEWORKS_INVESTIGATION.json)

---

## Executive summary

Phase 1 audit classified `afi-cli-framework` and `afi-cli-shared` as **SUPPORTING** generic CLI scaffolding with zero protocol surface. A fresh 2026-06-19 investigation **confirms** that verdict with build/test evidence and a full consumer graph.

**Neither repo is on the Phase A0/A1/A2 testnet critical path.** Operator work for testnet remains raw bash + Foundry `cast`/`forge` + `gcloud`/`bq`/Terraform + Mage — not these libraries.

| Repo | Verdict | Rationale |
|------|---------|-----------|
| `afi-cli-framework` (TS) | **KEEP** | One real consumer (`afi-gateway`); builds; 53/53 tests; fix packaging only |
| `afi-cli-shared` (Py + bash) | **CONSOLIDATE** | Python package broken + zero consumers; only `afi-shared.sh` is used (dormant benchkit scripts) |

**Overall action:** CONSOLIDATE — keep the TS framework, rehome bash helpers to `afi-ops`, deprecate the Python package, fix doc phantom edges, align `afi-gateway` CLI surface with scored-only spine.

**Out of scope until Phase A1 gate passes:** building `gcloud`/`bq`/`cast` operator CLIs on `CliApp`; publishing to npm/PyPI; migrating other repos onto BaseCli/CliApp.

---

## Investigation findings adopted

The following conclusions from the investigation report are **accepted as ground truth**:

1. Both library repos are protocol-agnostic; every protocol-regex hit is branding or false positive.
2. `afi-gateway` is the sole `CliApp` extender; `afi-benchkit` sources `afi-shared.sh` only (four dormant scripts).
3. `afi-docs/AFI_Repository_Map.md:172,188` falsely claims `afi-cli-framework → afi-cli-shared` — **phantom dependency**.
4. `afi-benchkit/scripts/lock/{compile,refresh}.sh:8` uses `$REPO_ROOT/../../afi-cli-shared/...` — **off-by-one `..` bug** (fails under `set -euo pipefail` even in full monorepo checkout).
5. `afi-cli-shared` `pip install -e .` is **broken** (`pyproject.toml` packages vs `src/` layout mismatch).
6. Gateway **consumer drift** (not library defect): `eliza-demo`, `validator <subcommand>`, help text, `SUBMIT_SIGNAL_DRAFT` naming — all P1/P2, neutralized but still discoverable.

---

## Human decisions (binding)

### 1. Distribution intent

- `file:../` monorepo sibling links are **sufficient for now**.
- **Do not** publish `@afi/cli-framework` or `afi-cli-shared` to npm/PyPI yet.
- **Do** add `"prepare": "npm run build"` to `afi-cli-framework/package.json` so `npm ci` in `afi-gateway` always produces `dist/` without manual `tsc`.
- Update READMEs to say **monorepo sibling dependency only** — remove false `npm install @afi/cli-framework` / `pip install afi-cli-shared` claims.

### 2. Standardization initiative

- **RETIRE** the aspirational "AFI CLI Standardization & Governance" program as an **active mandate**.
- Docs affected (status → `RETIRED / aspirational only`):
  - `afi-docs/AFI_CLI_STANDARDS_AND_GOVERNANCE.md`
  - `afi-docs/AFI_CLI_STANDARDIZATION_IMPLEMENTATION_PLAN.md`
  - `afi-docs/AFI_CLI_GOVERNANCE_COMMITTEE_CHARTER.md`
  - `afi-docs/AFI_CLI_REVIEW_PROCESS.md`
  - `afi-docs/AFI_CLI_MAINTENANCE_SCHEDULE.md`
  - `afi-docs/AFI_CLI_COMMUNICATION_PLAN.md`
- **Do not** schedule migration of `afi-econ`, `afi-tiny-brains`, `afi-governance`, `afi-mint`, or `afi-reactor` onto these libs before **Phase A1 gate** passes.
- **Fix** `afi-docs/AFI_Repository_Map.md`: remove phantom `afi-cli-framework → afi-cli-shared` edge; correct stale `afi-pipeline` / `afi-agents` references in the dependency diagram where still present.

### 3. `afi-shared.sh` ownership

- **Extract** to `afi-ops/scripts/lib/afi-shared.sh` (cross-repo bash ops home).
- Update `afi-benchkit` scripts to source:
  - `$REPO_ROOT/../afi-ops/scripts/lib/afi-shared.sh`, or
  - `${AFI_SHARED_SH:-$REPO_ROOT/../afi-ops/scripts/lib/afi-shared.sh}` with documented default.
- **Fix immediately:** `lock/compile.sh` and `lock/refresh.sh` off-by-one `../../` → one `..` (or use `afi-ops` path above).
- No dedicated test suite for `afi-shared.sh` in this pass — `bash -n` + script smoke is enough.

### 4. Gateway CLI legacy verbs

- **REMOVE** (not stub/hard-gate):
  - `eliza-demo` command (`cli.ts`, `afiCli.ts`)
  - `validator <subcommand>` command (`cli.ts`, `afiCli.ts`)
  - All help text advertising either (`afiCli.ts`)
- **KEEP:** `reactor status` (on-spine `/health` check).
- **RENAME** (P2, same PR if small):
  - `SUBMIT_SIGNAL_DRAFT` → `SUBMIT_TRADINGVIEW_SIGNAL`
  - `TradingViewLikeDraft` → `TradingViewWebhookPayload` or `UssIngestPayload` (match `afi-config` naming)
- Delete disabled-message paths that steer operators to purged draft/validator vocabulary.

### 5. Python package fate

- **DEPRECATE AND DELETE** `afi-cli-shared/src/afi_cli_shared/*.py`, tests, and broken `pyproject.toml` packaging.
- After `afi-shared.sh` is rehomed, **archive** `afi-cli-shared` repo (or leave a stub README pointing to `afi-ops`).
- **Do not** fix Python `src`-layout packaging — no consumer justifies the work.

---

## Execution charter (copy-paste for Claude Code)

```
# MISSION: Execute CLI framework consolidation (post-investigation)

Read first (binding):
- afi-docs/specs/audit/AFI_CLI_FRAMEWORKS_INVESTIGATION.md
- afi-docs/specs/audit/AFI_CLI_FRAMEWORKS_INVESTIGATION.json
- afi-docs/specs/audit/AFI_CLI_FRAMEWORKS_DECISIONS.md

## Phase A — Docs correction (no code risk)
1. Fix afi-docs/AFI_Repository_Map.md phantom edges and stale pipeline diagram
2. Add RETIRED banner to AFI_CLI_STANDARDS_AND_GOVERNANCE.md and related CLI governance docs
3. Link investigation + decisions from afi-docs/specs/audit/README.md

## Phase B — Low-risk mechanical fixes
1. afi-cli-framework/package.json — add "prepare": "npm run build"; fix README install claims
2. afi-ops/scripts/lib/afi-shared.sh — move from afi-cli-shared (git mv or copy+delete)
3. afi-benchkit — fix all source paths; fix lock/*.sh off-by-one
4. afi-cli-shared — delete Python package; add DEPRECATED.md → afi-ops (or archive repo)

## Phase C — Gateway alignment (PR if branch protection)
1. Remove eliza-demo + validator commands from cli.ts and afiCli.ts
2. Rewrite help to scored-only: reactor status + link to USS webhook / testnet checklist
3. Rename SUBMIT_SIGNAL_DRAFT / TradingViewLikeDraft if scope stays small; else open follow-up issue

## Phase D — Verify
- afi-cli-framework: npm ci && npm test
- afi-gateway: npm ci && npm run build (if applicable)
- afi-benchkit: bash -n on updated scripts
- rg eliza-demo|validator explain-last|SUBMIT_SIGNAL_DRAFT in afi-gateway — zero hits in active CLI surface

## Out of scope (do NOT do now)
- Building gcloud/bq/cast operator CLIs on CliApp
- Publishing @afi/cli-framework to npm
- Migrating afi-benchkit from Click to BaseCli
- Fixing afi-cli-shared pip install

Commit per repo. Push when done.
Write AFI_CLI_FRAMEWORKS_CONSOLIDATION_RESULTS.md under afi-docs/specs/audit/ when complete.
```

---

## Priority relative to testnet

| Work | Blocks Phase A1? | When |
|------|------------------|------|
| Docs phantom-edge fix | No | Now |
| `afi-shared.sh` rehome + benchkit path fix | No | Now |
| `prepare` script on afi-cli-framework | No | Now |
| Gateway CLI verb removal | No (reduces operator confusion) | Before operators run gateway CLI |
| Operator CLIs on CliApp (`gcloud`/`bq`/`cast`) | No | **After** Phase A1 gate |

---

## Open items (defer)

- Whether to archive vs stub `afi-cli-shared` GitHub repo (check for external links first).
- Whether `SUBMIT_TRADINGVIEW_SIGNAL` rename touches Eliza action registry / external docs.
- Whether `afi-ops` gets a minimal CI `bash -n` workflow for `afi-shared.sh` consumers.
