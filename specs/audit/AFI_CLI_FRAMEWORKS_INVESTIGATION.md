# AFI CLI Frameworks Investigation

## Executive verdict (one paragraph)

`afi-cli-framework` (TypeScript/Commander.js) and `afi-cli-shared` (Python/Click + a bash helper lib) are both **generic, protocol-agnostic CLI scaffolding with zero AFI trading-protocol coupling** — every "AFI"/"afi" hit across both repos is branding-only (package names, the `.afi-cli.json` config filename, the `AFI_CLI_` env prefix, `AFI_*` bash vars, the `afi-cli` logger name, "AFI Team" metadata), and the lone protocol-regex hit (`USS` at `afi-cli-framework/package-lock.json:779`) is a confirmed false positive inside a base64 sha512 integrity hash. **Neither is on the Phase A1 (or A0/A2) testnet critical path** — the entire operator surface is raw bash + Foundry `cast`/`forge` + `gcloud`/`bq`/Terraform + Mage, none of which is built on either framework. The **TS framework builds (exit 0) and passes 53/53 tests** and has exactly one real consumer (`afi-gateway`), so it is load-bearing and a **KEEP**; the **Python package's canonical `pip install -e .` is BROKEN out of the box** (src-layout vs `packages=["afi_cli_shared"]` mismatch), is unpublished (PyPI 404), and has **zero in-tree Python consumers** — so it is a **CONSOLIDATE/DEPRECATE** target whose only genuinely-used artifact is the standalone `scripts/lib/afi-shared.sh` bash lib (sourced by 4 dormant benchkit scripts). Separately, the gateway **consumer** still exposes neutralized **legacy operator semantics** (eliza-demo, validator-decision vocabulary) — a consumer-refactor issue, not a defect in the clean library repos.

## Relevance matrix

| Repo | Testnet critical? | Active consumers | Protocol surface | Recommendation |
|---|---|---|---|---|
| `afi-cli-framework` (TS) | **No** (not on A0/A1/A2) | 1 real, dormant: `afi-gateway/src/cli.ts:10` (`extends CliApp`); declared `afi-gateway/package.json:42` `file:../afi-cli-framework` | **None** (branding only; `USS` lock hit is base64 false positive) | **KEEP** (fix packaging) |
| `afi-cli-shared` (Python + bash) | **No** (not on A0/A1/A2) | 0 Python consumers in-tree; bash lib sourced by 4 **dormant** benchkit scripts | **None** (branding only; "mage" hits = substring of "image" in docker helpers) | **CONSOLIDATE** (deprecate Python pkg; retain `afi-shared.sh`) |

## Consumer graph (with evidence links)

**`afi-cli-framework` — exactly one real consumer (verified complete, all 26 package.json scanned):**
- `afi-gateway/package.json:42` — `"@afi/cli-framework": "file:../afi-cli-framework"` (local file: link, not a registry version; literal-string searches miss it because the dep key is the npm scope).
- `afi-gateway/src/cli.ts:10` — `import { CliApp }`; `afi-gateway/src/cli.ts:16` — `class AfiGatewayCli extends CliApp`.
- **Dormant as a product surface**: `afi-gateway/package.json` has **no `bin` field**; CLI reachable only via npm scripts `start:cli`/`dev` (`package.json:9,17`). Zero GitHub Actions in afi-gateway. Not in any runbook or `AFI_TESTNET_E2E_CHECKLIST.md`. AGENTS.md:3 / README.md:5 frame afi-gateway as an "external client."
- Framework dist is buildable on demand (`afi-cli-framework/dist/base/CliApp.js` present after `tsc`).

**`afi-cli-shared` — zero Python consumers; bash lib has 4 dormant consumers (verified complete, all `*.sh` scanned):**
- `afi-benchkit/scripts/capsule_run.sh:12` — `source "$REPO_ROOT/../afi-cli-shared/scripts/lib/afi-shared.sh"`
- `afi-benchkit/scripts/generate_benchmarks.sh:8` — sources `afi-shared.sh` (invoked only by `afi-benchkit/Makefile:56`)
- `afi-benchkit/scripts/lock/refresh.sh:8` — sources via `$REPO_ROOT/../../afi-cli-shared/...` (**broken in-tree**, see below)
- `afi-benchkit/scripts/lock/compile.sh:8` — sources via `$REPO_ROOT/../../afi-cli-shared/...` (self-declared "maintainers only" at `compile.sh:3`)
- All four are **dormant**: `afi-benchkit/.github/workflows/ci.yml:11-12,50-53` runs `afi-bench run ... ` directly via `docker run`, **never** these shell scripts. Not in any runbook/testnet checklist.
- **Python side has ZERO importers**: `from afi_cli_shared`/`import afi_cli_shared` across all `*.py` (excl. the repo) returns only the package's own `tests/*.py`. No `pyproject`/`requirements`/`setup.cfg`/`tox` declares it as a dep; egg-info has no `entry_points.txt` (no console_scripts), so it exposes no callable bin.

**Phantom dependency correction (verifier):** `afi-docs/AFI_Repository_Map.md:172` and `:188` assert "afi-cli-framework uses utilities from afi-cli-shared" — this is **FALSE/aspirational**; grep of `afi-cli-framework/` for `cli-shared|afi_cli_shared|afi-shared` returns nothing. It is a doc-only phantom relationship, not a real consumer edge.

**Doc-only "AFI CLI Standardization & Governance" initiative:** `afi-docs` mandates ALL Node CLIs extend `CliApp` and ALL Python CLIs extend `BaseCli`, names afi-benchkit as non-compliant (direct Click) and slated to migrate, and frames these two packages as Phase-1 "Foundation" for unifying "6 disparate CLI frameworks across 15 implementations." **Reality: aspirational/doc-only** — the only `CliApp` extender is afi-gateway, the only `BaseCli` "extender" is afi-cli-shared's own test, and afi-benchkit still depends on `click` directly (`pyproject.toml:15`), unmigrated.

## Alignment findings (legacy drift)

**LIBRARY REPOS ARE CLEAN.** Every source file of both repos was read directly (not just grepped) by the protocol verifier: no imports/uses of USS/mint/vault/reactor/Mage/BigQuery/Pub-Sub logic, no DB/network clients, only generic config/extension/validation/logging scaffolding. `anyRealCoupling=false` stands. Neither `afi-cli-framework` nor `afi-cli-shared` exhibits any legacy protocol drift.

**CONSUMER DRIFT — `afi-gateway` CLI (a consumer of `afi-cli-framework`).** **Explicit answer: YES, the afi-gateway CLI still exposes legacy semantics** (verified by independent re-read of `cli.ts`, `afiCli.ts`, the plugin, and `afiClient.ts`; `grep deprecated|legacy` across both CLI files returns **zero** hits, so these legacy verbs are presented as live with no deprecation marker). All code paths are neutralized (disabled/stubbed/on-spine-under-the-hood), so nothing on the purged demo chain actually executes — the exposure is at the command-surface / help-text / vocabulary level. No P0.

| # | File:line | Item | Why legacy | Severity |
|---|---|---|---|---|
| 1 | `afi-gateway/src/cli.ts:43-49` | `eliza-demo` command ("Run AFI Eliza Demo pipeline") | Purged demo-chain entrypoint still registered as a first-class CLI verb | **P1** |
| 2 | `afi-gateway/src/afiCli.ts:44-45,81-98` | `eliza-demo` dispatch -> `runAfiElizaDemoFlow` | Disabled (warns, returns "endpoint has been removed"), but message (`L92`) steers operators to legacy `SUBMIT_SIGNAL_DRAFT` draft-handoff verb | **P1** |
| 3 | `afi-gateway/src/cli.ts:60-67` | `validator <subcommand>` ("Validator operations") | Resurfaces purged validator-decision-evaluator namespace as a primary CLI surface (distinct from `afi-core/validators/ValidatorDecision.ts`, not calling it) | **P1** |
| 4 | `afi-gateway/src/afiCli.ts:53-57,120-126` | `validator explain-last` -> `getLastValidatorDecisionSummary` | Stub returning "Last Validator Decision: Not yet implemented"; exposes purged validator-decision response-shape vocabulary | **P1** |
| 5 | `afi-gateway/src/afiCli.ts:131-142` | `help` text | Advertises `eliza-demo` (`L135`) and `validator explain-last` (`L137`) with no deprecation marker — markets purged semantics as live | **P1** |
| 6 | `afi-gateway/plugins/afi-reactor-actions/index.ts:37-113` | `SUBMIT_SIGNAL_DRAFT` action (registered via `cli.ts:31-32`) | Legacy "draft" handoff verb/shape (`TradingViewLikeDraft`); BUT underlying call (`afiClient.ts:117-155` -> `/api/webhooks/tradingview` -> Froggy ingest->USS->enrich->score->persist) is **on-spine** | **P2** |

**On-spine / NOT legacy:** `afi-gateway/src/cli.ts:51-58` + `afiCli.ts:47-51,104-114` + `afiClient.ts:164` — `reactor status` = read-only `/health` check reporting Froggy pipeline status. Canonical.

**Minor nit (verifier):** the prior `reactor` entry's prose mislabeled its description as "Validator operations"; actual is "AFI Reactor operations" (`cli.ts:53`). Cosmetic; classification (`legacy:false`) is correct.

## State of reality

### afi-cli-framework — build/test/maturity
- **Maturity:** single commit `5b46ed4` "Initial commit" (2026-01-02), branch `main` only, no tags, remote `git@github.com:AFI-Protocol/afi-cli-framework.git`. **No CI** (`.github/workflows` absent).
- **Build:** `npm run build` (`tsc`) -> **exit 0**, no errors (re-verified independently).
- **Tests:** `npm test` (jest/ts-jest) -> **exit 0**: "Test Suites: 6 passed, 6 total / Tests: 53 passed, 53 total." 100% stmts/branch/funcs/lines across all 7 src files.
- **Packaging:** `@afi/cli-framework` v1.0.0, **unpublished** (npm registry 404); sole dep `commander ^14.0.2`. `@types/commander ^2.12.0` is a deprecated stub (commander v14 ships its own types). No committed `dist/` guarantee + no `prepare` script while `main=dist/index.js` — the `file:../` link only works after a manual `npm run build` in the sibling.
- **README vs code:** accurate, no material discrepancies; only overstatement is `npm install @afi/cli-framework` (not registry-resolvable). `ConfigManager.save()` has rambling comments (`lines 109-119`) but works.

### afi-cli-shared — build/test/maturity
- **Maturity:** single commit `fc9d0f05` "Initial commit" (2026-01-02, author machinemonk), branch `main` only, no tags. **No CI of its own.**
- **Build/editable install:** `pip install -e ".[test]"` -> **exit 1 (BROKEN)**. Root cause (verified): `pyproject.toml:35` `packages = ["afi_cli_shared"]` but code lives under `src/afi_cli_shared/` with no `package-dir = {""="src"}` / `[tool.setuptools.packages.find] where=["src"]`; setuptools errors `package directory 'afi_cli_shared' does not exist`. (System pip also blocked by PEP 668 externally-managed-environment, handled via venv — but the failure is a real packaging bug, not network.)
- **Tests:** only via workaround `PYTHONPATH=src .../python -m pytest -q` -> **exit 0**, "28 passed in 0.06s" (click 8.4.1, pytest 9.1.0, Py 3.12.3). Mock-heavy unit tests of the Python modules; **do NOT exercise** `scripts/lib/afi-shared.sh`.
- **Packaging:** `afi-cli-shared` v1.0.0, **unpublished** (PyPI 404), not importable in any live interpreter; committed `egg-info` is a stale top-level-layout artifact.
- **Hygiene issues (committed/git-tracked):** `afi_cli_shared.egg-info/*`, `.coverage`, `__pycache__/*.pyc`.
- **README vs code:** API docs mostly accurate, but "Ready for PyPI" / `pip install afi-cli-shared` / `pip install -e ".[test]" && pytest` are all FALSE/broken; README is silent about `scripts/lib/afi-shared.sh` (the more reusable deliverable); references a nonexistent `docs/` dir; env-var nested keys stay strings (no type coercion), undocumented.

## Testnet workflow fit (A0 / A1 / A2)

**(a) Are these on the Phase A1 testnet critical path? NO** (and not A0/A2 either). The entire operator surface is bash + Foundry `cast`/`forge` + `gcloud`/`bq`/Terraform + Mage; a sweep of both frameworks for `pubsub|bigquery|bq|gcloud|mage|cast|mint|deploy|webhook|grantRole` returned nothing but generic `docker_*` helpers in `afi-shared.sh`. The only genuine framework consumer (gateway CLI) drives ElizaOS demo commands, off the critical path. `frameworkA1Critical=false`, `sharedA1Critical=false`.

| Operator action | Phase | Uses framework? | Should? | Gap |
|---|---|---|---|---|
| Section 0 preflight: `afitoken_testnet_sanity_checks.sh` + `cast call hasRole` role checks | A0 (T1 gate) | neither | no | Raw bash + `cast`; no role-check wrapper exists on either lib |
| Section 0.1 manual mint smoke: `cast send COORDINATOR mintForSignal(...)` | A0 (T1 gate) | neither | maybe | Raw `cast send`, fiddly tuple encoding; a viem/cast mint wrapper would be the missing surface (TS framework a plausible host) |
| Safe role grant `grantRole(EMISSIONS_ROLE)` (Gate 3 HANDOFF) | A0 (T1 gate) | neither | no | Human/Safe multisig calldata; no Safe-calldata generator on either lib |
| Ingest webhook smoke: validate USS/CPJ, publish to Pub/Sub `signal-raw` (§1.2) | A1 | neither | no | Runs inside HTTP services, not a CLI; missing surface is a Pub/Sub publish/curl harness |
| Pub/Sub topic/IAM + publish test (§1.1, §1.7) | A1 | neither | maybe | All `gcloud pubsub`/Terraform; a gcloud/pubsub wrapper could be built but isn't |
| Mage deploy + Froggy scoring DAG + BQ SCORED (§1.0, §1.3) | A1 | neither | no | Mage = Docker/Terraform/Python platform; zero AFI CLI named in migration map |
| BigQuery verify rows in `afi_evidence.signals_lifecycle` (§1.7) | A1 | neither | maybe | `bq query`/DDL; a `bq` verify wrapper is candidate missing surface, not built |
| Mint orchestration (A2): Pub/Sub push -> afi-mint Cloud Run, on-chain mint, BQ write-back (§1.4-§1.7) | A2 | neither | no | afi-mint is a Cloud Run ethers/viem service; does not depend on either lib |
| afi-gateway CLI `eliza-demo`/`reactor`/`validator` (`cli.ts`) | dev/demo (off path) | **afi-cli-framework** | yes | Only real consumer of `@afi/cli-framework`; ElizaOS demo cmds, not testnet ingest/score/mint/BQ/Safe |
| afi-benchkit scripts sourcing `afi-shared.sh` | benchmarking (off path) | **afi-cli-shared** | yes | Only real consumer of `afi-cli-shared`; generic log/docker helpers, off the critical path |

## Duplication analysis

**Feature matrix:**

| Feature | afi-cli-framework (TS) | afi-cli-shared (Python) |
|---|---|---|
| Base app class | `CliApp extends commander.Command` (`base/CliApp.ts:9`); config-driven log level (`L31-43`); `run()` -> `extensionManager.initAll` + `parse()` | `BaseCli(click.Group)` (`base.py:9`); `run()` -> `extension_manager.init_all` + `self()`. No log-level wiring |
| Config hierarchy (`.afi-cli.json` + `AFI_CLI_*`) | YES (`config/ConfigManager.ts:29-65`); `save()` works but comments self-document indecision (`L109-119`) | YES — identical 3-tier merge, identical prefix/key transform (`config.py:17-37`). Functional port |
| Extension manager | `ExtensionManager.register/initAll` (`extensions/ExtensionPoint.ts:11-25`) | `ExtensionManager.register/init_all` (`extensions.py:11-25`). Equivalent |
| Bash helpers | NONE | YES — `scripts/lib/afi-shared.sh` (193 lines). **Only unique surface** |
| Command registration | Inherited from Commander.js | Inherited from Click `Group` |
| Error handling | `CliError`+`handleError`+`wrapAsync` (`utils/errorHandling.ts`) | `CliError`+`handle_error`, no async wrapper (`error_handling.py`) |
| Validation | 6 fns incl. boolean/inRange (`utils/validation.ts`) | 5 fns, no boolean/inRange (`validation.py`) |
| Logging | Real `Logger`+`LogLevel`, level-gated (`utils/logging.ts`) | Delegates to stdlib `logging.getLogger`, no level config |
| Tests / coverage | 53 tests, 6 suites, 100% — `npm test` exit 0 | 28 tests, 100% line — **only via `PYTHONPATH=src`**; `pip install -e .` fails first |

**Two frameworks justified? NO** (`twoFrameworksJustified=false`). Both are thin wrappers over mature upstreams (Commander.js / Click) plus a ~100-line config/extension/validation layer; the TS framework has one real consumer and the Python Click package has **zero** in-tree consumers. The configs/extension systems are near-identical ports.

**Is `afi-shared.sh` the real value? YES** (`sharedShIsRealValue=true`). `scripts/lib/afi-shared.sh` (193 lines) is the most substantive, reusable artifact: structured stderr logging (`log_info/error/warn/debug/success`, debug gated by `AFI_VERBOSE`), `error_exit`, cleanup trap setup, common-arg parsing (`--dry-run/--verbose/--help/--version`), container-runtime abstraction (docker->podman fallback, image exists/pull/build/run honoring `AFI_DRY_RUN`), file ops, `get_repo_root`, `init_script`. Self-contained (`set -euo pipefail` + standard tools), no protocol coupling. Caveat: it has **NO tests** (the 28 pytest tests cover only the Python modules).

**Broken file:/sibling assumptions (verified):** (1) `afi-gateway/package.json:42` `file:../afi-cli-framework` breaks standalone and yields nothing runnable until the sibling is manually built. (2) benchkit `generate_benchmarks.sh:8` / `capsule_run.sh:12` use one `..` (work in-tree, break standalone). (3) **BROKEN IN-TREE**: `lock/compile.sh:8` and `lock/refresh.sh:8` source `$REPO_ROOT/../../afi-cli-shared/...`; since they live in `scripts/lock/`, `REPO_ROOT` = benchkit root and `../../` escapes ABOVE the monorepo to a path that does not exist even in a full checkout (`ls` -> No such file or directory) — an off-by-one-`..` bug; under `set -euo pipefail` a failed source aborts. (4) `afi-cli-shared/pyproject.toml:35` src/packages mismatch breaks `pip install [-e] .` outright.

## Options (ranked)

**1 — KEEP AS-IS.** Applies to **`afi-cli-framework`**: it is generic, self-contained, builds clean (exit 0), passes 53/53, has a live consumer (`afi-gateway`), and carries zero protocol coupling. Keep it as a library. (The only caveats — unpublished/file-link, no CI, deprecated `@types/commander` stub — are low-priority follow-ups, not blockers.)

**2 — CONSOLIDATE.** Applies to **`afi-cli-shared`** (overall repo): single uninstallable commit, never published (PyPI 404), Python package has zero in-tree consumers and a broken canonical install. Fold the trivial Python helpers into whatever single CLI needs them (or fix-then-publish), and **EXTRACT/RETAIN `scripts/lib/afi-shared.sh`** as its own tiny standalone shared-ops artifact (the genuinely-used part), fixing the benchkit `../../` path bug. Net: collapse two frameworks + a bash lib -> one TS framework (properly packaged) + standalone `afi-shared.sh`.

**3 — EXTEND.** Applies to **`afi-cli-framework`** *if and only if* AFI decides operator tooling should be built on a CLI framework: the real testnet gaps are `cast`/viem mint+role wrappers, `gcloud pubsub` publish/verify, and `bq` query/verify wrappers. None exist today; the TS framework is the plausible host. Also applies to the **gateway consumer** as a refactor (remove/hard-gate `eliza-demo`/`validator` registrations and help-text lines; rename `SUBMIT_SIGNAL_DRAFT`/`TradingViewLikeDraft` away from "draft" vocabulary).

**4 — DEPRECATE / ARCHIVE.** Applies to the **Python package portion of `afi-cli-shared`** (`src/afi_cli_shared/*.py`): zero consumers + broken `pyproject` = retiring it removes dead, mis-packaged code at zero cost. (Do NOT archive the whole repo until `afi-shared.sh` is rehomed, since the bash lib is the only used surface.)

## Recommended next action

KEEP `afi-cli-framework` as the single TS CLI library (fix packaging so the `file:../` link is reliable), CONSOLIDATE `afi-cli-shared` by deprecating its unused, broken-to-install Python package while extracting `scripts/lib/afi-shared.sh` as a standalone bash utility (and fixing the benchkit `../../` source-path bug), and separately refactor the `afi-gateway` consumer to remove/gate its legacy `eliza-demo`/`validator` CLI verbs and help text.

## Open questions for human review

1. **Distribution intent:** is `@afi/cli-framework` meant for external/registry distribution (publish to a private registry + add a `prepare` script / commit `dist/`), or is the `file:../` monorepo link sufficient? The README's `npm install @afi/cli-framework` currently overstates availability.
2. **Standardization initiative:** the doc-only "AFI CLI Standardization & Governance" program (committee, quarterly reviews, 90% coverage, migrating afi-econ/tiny-brains/governance/mint/reactor) has zero code adoption — should it be funded/executed or retired so the docs stop asserting a phantom standard (incl. the false `AFI_Repository_Map.md:172/188` claim)?
3. **`afi-shared.sh` ownership:** where should the bash lib live once extracted, and who owns adding tests for it (currently untested)? Fixing the in-tree-broken `../../` source paths in benchkit's `lock/{compile,refresh}.sh` is a prerequisite.
4. **Gateway CLI legacy verbs:** confirm `eliza-demo` and `validator <subcommand>` should be removed/hard-gated (purged pipeline) rather than re-implemented, and whether `SUBMIT_SIGNAL_DRAFT`/`TradingViewLikeDraft` should be renamed to the USS-spine vocabulary even though the underlying call is on-spine.
5. **Python package fate:** deprecate-and-delete `src/afi_cli_shared/*.py`, or fix the `src`-layout packaging and find/justify a real consumer? Today it has none.
