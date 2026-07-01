# Report — AFI Signal Evaluation Pipehead System (non-production POC)

**Date:** 2026-06-30
**Repo (implementation):** `afi-reactor` — branch `mission/afi-signal-evaluation-pipehead-system`
**Repo (this report):** `afi-docs` — branch `mission/afi-signal-evaluation-pipehead-system`
**Type:** Determinism / plumbing proof-of-concept (POC). Demo-only — implements no production surface.
**Governance:** Subordinate to `AFI_DROID_CHARTER.v0.1.md` and `AFI_DROID_PIPEHEAD_ADDENDUM.v0.1.md`. Where this report conflicts with governance, governance wins.
**Merge status (2026-07-01 reconciliation):** afi-reactor PR #33 is **merged** to `main` (merge commit `dd15287`, 2026-06-30); the afi-config Pipehead Addendum is **merged** via PR #12 + #13 (`codex/governance/droids/AFI_DROID_PIPEHEAD_ADDENDUM.v0.1.md`). This afi-docs report (PR #5) is the remaining open reconciliation item. The "no changes to afi-config" note below refers to the reactor implementation footprint only; the governance addendum shipped through its own afi-config PRs.

> **Status: non-production POC / demo.** Nothing in this system is intended for production use, and no output is canonical protocol truth. All scored output, receipts, and audit records are explicitly **demo-only / provisional**. This report describes the code that actually shipped, and records the real gate and demo outcomes captured while writing it.

---

## 1. Executive summary

This mission made AFI's signal-evaluation DAG **Droid-operable** as a self-contained set of "pipeheads" in `afi-reactor`, **without** making Droids the source of financial truth. Droids operate the machinery — schema validation, a five-lane analysis fan-out, fan-in normalization, scoring invocation, a demo receipt, and a content-hashed audit record — while the **deterministic kernel** (the afi-core Froggy trend-pullback UWR scorer) remains the source of truth and is **invoked, never replaced**.

The deliverable is additive and minimal-footprint: all new code lives under `afi-reactor/src/pipeheads/**`, a CLI demo entrypoint, and tests/fixtures under `test/pipeheads/**`, plus a scoped typecheck config and a scoped ESM gate. The only existing file edited is `jest.config.js` (a `testMatch` allowlist addition). No changes were made to `afi-core`, `afi-math`, or `afi-config`, and no scoring/UWR/reputation/token/settlement logic was touched.

The system preserves the five-lane interface (`technical-indicators`, `pattern-recognition`, `news`, `social`, `ai-ml`) at all times. Two lanes are **wired** (real deterministic math over committed fixture OHLCV); three lanes (`news`, `social`, `ai-ml`) are **provisional** committed fixtures, explicitly labeled. Determinism is mandatory and proven: identical input ⇒ identical output ⇒ identical content hash, anchored to a committed golden fixture.

Two trust-relevant afi-reactor modules could not be reused **offline**, so self-contained equivalents were used behind clean seams (recorded as Decision Records DR-001 and DR-002 in the mission `AGENTS.md`, and summarized in §8 below): the canonical USS validator (blocked by `ajv`/`ajv-formats`) and the canonical technical-indicator kernel (blocked by `trading-signals`). Scoring itself stays 100% afi-core. Both have a documented future restoration path.

All three verification gates were run while writing this report and passed: scoped typecheck clean, scoped ESM check clean, and `npm test` green at **644 tests / 25 suites** (425 baseline + new pipehead tests). The CLI demo runs offline, exits `0`, and prints an identical `outputHash` across two runs.

---

## 2. Files changed

All paths are in `afi-reactor` unless noted. Everything below is **new** except `jest.config.js` (modified) and this report + the system doc (new, in their respective repos).

### Pipehead implementation — `src/pipeheads/` (new)

| File | Role |
| --- | --- |
| `src/pipeheads/types.ts` | Mission-local contracts (`Pipehead`, `AnalysisLaneResult`, `AnalysisBundle`, `DemoScoredSignal`, `DemoReputationReceipt`, `AuditRecord`, the five canonical lane ids). |
| `src/pipeheads/clock.ts` | Injectable frozen-clock factory (`createFrozenClock`, `FROZEN_CLOCK_ISO`) — timestamps are human-only and excluded from hashes. |
| `src/pipeheads/canonicalHash.ts` | Recursive key-sorted canonicalizer + sha256 (`canonicalize`, `canonicalHash`, `buildScoringProjection`, `EXCLUDED_TIMESTAMP_KEYS`). |
| `src/pipeheads/schemaValidationPipehead.ts` | Self-contained **OFFLINE structural** USS v1.1 validator (DR-001; NOT canonical `ussValidator`). |
| `src/pipeheads/lanes/technicalLane.ts` | WIRED technical lane (`provisional:false`); self-labels its indicators as non-canonical (DR-002). |
| `src/pipeheads/lanes/technicalIndicators.ts` | Self-contained **OFFLINE** EMA-20/50, RSI-14, ATR-14 + `trendBias`/`emaDistancePct` helper (DR-002). |
| `src/pipeheads/lanes/patternLane.ts` | WIRED pattern lane (`provisional:false`); reuses `src/enrichment/patternRecognition.ts#detectPatterns` (pure, offline). |
| `src/pipeheads/lanes/newsLane.ts` | PROVISIONAL committed news fixture lane (`provisional:true`). |
| `src/pipeheads/lanes/socialLane.ts` | PROVISIONAL committed social/sentiment fixture lane (`provisional:true`; maps to `enrichedView.sentiment`). |
| `src/pipeheads/lanes/aimlLane.ts` | PROVISIONAL committed AI/ML fixture lane (`provisional:true`; no network, no Tiny Brains). |
| `src/pipeheads/fanOut.ts` | Five-lane fan-out coordinator with per-lane error isolation. |
| `src/pipeheads/normalizePipehead.ts` | Fan-in to an `AnalysisBundle` + `FroggyEnrichedView` projection. |
| `src/pipeheads/scoringPipehead.ts` | **Invokes** the afi-core deterministic scorer (`createScoringPipehead`, `buildDemoScoredSignal`); afi-core bound via dynamic ESM import. |
| `src/pipeheads/reputationReceipt.ts` | Demo-only, non-mutating `DemoReputationReceipt`. |
| `src/pipeheads/auditPipehead.ts` | Content-hashed `AuditRecord` (sha256; timestamps excluded). |
| `src/pipeheads/harness.ts` | Composes the full DAG in fixed order and returns one aggregate. |
| `src/pipeheads/index.ts` | Barrel exports. |

### CLI demo (new)

- `src/cli/run-pipehead-demo.ts` — runnable via `node --loader ts-node/esm`; thin wrapper over the harness; prints a five-lane summary + four labeled JSON blocks.

### Tests + fixtures — `test/pipeheads/` (new)

- Test suites: `types.test.ts`, `clock.test.ts`, `canonicalHash.test.ts`, `schemaValidation.test.ts`, `lanes.test.ts`, `fanOut.test.ts`, `provisionalLanes.test.ts`, `normalize.test.ts`, `normalizeIdentity.test.ts`, `scoring.test.ts`, `reputationReceipt.test.ts`, `audit.test.ts`, `harness.test.ts`, `crossArea.test.ts`, `cli.test.ts`.
- Fixtures: `fixtures/signal.uss.json` (canonical USS v1.1), `fixtures/signal.invalid.uss.json` (missing `provenance.signalId`), `fixtures/ohlcv.json`, `fixtures/lanes/{news,social,aiml}.json`, and `fixtures/golden.json` (committed replay anchor: `inputHash`/`bundleHash`/`outputHash` + `uwrScore`/`uwrAxes`).

### Tooling + config

- `tsconfig.pipeheads.json` (new) — scoped typecheck over only the new pipehead/CLI/test code (avoids the pre-existing `AnalystNode → afi-factory` full-build break).
- `scripts/esm-check-pipeheads.sh` (new) — scoped ESM-invariant gate over the new files only.
- `jest.config.js` (**modified** — the only existing file edited) — `testMatch` allowlist addition for `test/pipeheads/**`.

### Documentation

- `afi-reactor/docs/PIPEHEAD_SYSTEM.md` (new) — the system doc this report summarizes.
- `afi-docs/reports/afi-signal-evaluation-pipehead-system-report.md` (new) — this report.

---

## 3. Architecture implemented

The implemented DAG matches the mission `architecture.md` and is composed by `src/pipeheads/harness.ts` in a fixed order:

```
fixture USS v1.1
  → schema-validation pipehead   (self-contained OFFLINE structural validator; DR-001)
  → fan-out across FIVE lanes:
       technical-indicators (WIRED) | pattern-recognition (WIRED)
       news (PROVISIONAL) | social (PROVISIONAL) | ai-ml (PROVISIONAL)
  → normalize pipehead           (fan-in → AnalysisBundle; projects to FroggyEnrichedView)
  → scoring pipehead             (INVOKE afi-core scoreFroggyTrendPullbackFromEnriched; deterministic)
  → reputation receipt           (demo-only, non-mutating)
  → audit pipehead               (canonical sha256: inputHash, bundleHash, outputHash; timestamps excluded)
```

Key contracts (from `src/pipeheads/types.ts`):

- Every pipehead exposes `execute(input, ctx)` returning a typed `PipeheadExecutionResult`, pure given `(input, ctx)` — no network, no DB, no `Date.now`/`Math.random`. All timestamps come from the injectable `ctx.clock()`.
- The `AnalysisBundle.lanes` record **always** contains the five canonical lane keys in stable order; `provisionalLanes` is the explicit `["news","social","ai-ml"]` list; `enrichedView` is a `FroggyEnrichedView` the afi-core scorer consumes directly (social → `sentiment`; technical → `technical`; pattern → `pattern`). The bundle carries a `provenance` block binding it to the validated input (`signalId` + `inputHash`).
- A schema-validation failure is returned as a **structured value** (no uncaught throw) and **short-circuits** the pipeline — no bundle, scored output, receipt, or audit record is produced for invalid input.
- The `outputHash` is computed over an explicit deterministic projection (`{uwrScore, uwrAxes, analystId, strategyId, direction, riskBucket, conviction}`), never the raw timestamped `analystScore` (which carries an afi-core wall-clock `scoredAt`).

---

## 4. Demo flow

**How to run** (from the `afi-reactor` repo root, fully offline):

```bash
node --loader ts-node/esm src/cli/run-pipehead-demo.ts
```

Optional flags: `--uss <path>` / `--ohlcv <path>` (default to the committed canonical fixtures).

**What it prints.** First a short human-readable five-lane summary, each lane tagged `[WIRED]` or `[PROVISIONAL]`:

```
Analysis lanes (5):
  - technical-indicators [WIRED]
  - pattern-recognition [WIRED]
  - news [PROVISIONAL]
  - social [PROVISIONAL]
  - ai-ml [PROVISIONAL]
```

Then **four** labeled, individually `JSON.parse`-able blocks (each delimited by `===== BEGIN <Label> (application/json) =====` / `===== END <Label> =====`):

1. **`AnalysisBundle`** — `signalId`/`symbol`/`market`/`timeframe` (`BTC/USDT`, `perp`, `4h`), all five `lanes`, `provisionalLanes: ["news","social","ai-ml"]`, the `enrichedView` projection, and a `provenance` block (`signalId` + `inputHash`).
2. **`DemoScoredSignal`** — `uwrScore: 0.1875`, `uwrAxes {structure:0.15, execution:0, risk:0.2, insight:0.4}`, the afi-core `analystScore` verbatim (`analystId:"froggy"`, `strategyId:"trend_pullback_v1"`), and `provisional:true`, `demoOnly:true`.
3. **`DemoReputationReceipt`** — `receiptKind:"demo-only"`, `mutatesReputationState:false`, echoed `uwrScore` + `provisionalLanes`, and a non-canonical `note`.
4. **`AuditRecord`** — `algo:"sha256"`, `inputHash`, `bundleHash`, `outputHash`, echoed `uwrScore`/`uwrAxes`/`provisionalLanes`, `scoredAtExcluded:true`, `demoOnly:true`.

**Determinism check (twice-run identical hash).** Running the demo twice yields a byte-identical `outputHash`:

```
outputHash = 4b6dd610cba2b64831b0aa2a9e27707908affdf8134ca77d1083535de78ad8dc
```

The only run-to-run difference in stdout is the embedded afi-core wall-clock `analystScore.scoredAt` (afi-core is read-only, so the injected frozen clock cannot reach it) — and that field is **excluded** from every content hash, so all three hashes (`inputHash`/`bundleHash`/`outputHash`) are stable across runs. These match the committed `golden.json` exactly:

```
inputHash  = 92258c5bea8c613238c1f2f7f746c99084251510195682cbaf4cf39884e2422d
bundleHash = c75a1860df037619f257af024f8b0a3fc3ef057950bf9e36477c3c6a1d1add31
outputHash = 4b6dd610cba2b64831b0aa2a9e27707908affdf8134ca77d1083535de78ad8dc
```

**Exit-code semantics.** Over the committed (valid) fixture the demo exits `0`. Pointed at the deliberately-invalid fixture (`--uss test/pipeheads/fixtures/signal.invalid.uss.json`, missing `provenance.signalId`), it exits `2`, prints a structured `DemoError` block (`{ ok:false, stage:"validation", errors:[{field:"provenance.signalId", message:"..."}] }`) instead of a stack trace, and emits **no** downstream bundle/score/receipt/audit. The run is fully offline: no servers, no listening ports, no network, no DB writes, and it self-terminates leaving no orphaned process.

---

## 5. Test results

All three gates from the mission `services.yaml` were run from the `afi-reactor` repo root while writing this report. The scoped commands are used intentionally because the full `npm run build` and full `npm run esm:check` are RED for **pre-existing, out-of-scope** reasons (see §9).

| Gate | Command | Outcome |
| --- | --- | --- |
| **Unit/integration tests (Jest)** | `npm test -- --maxWorkers=2` | **PASS** — `Test Suites: 25 passed, 25 total`; `Tests: 644 passed, 644 total` (425 baseline + new pipehead tests). Exit code `0`. |
| **Scoped typecheck** | `npx tsc -p tsconfig.pipeheads.json` | **PASS** — clean; exit code `0`. Scoped to the new pipehead/CLI/test code only. |
| **Scoped ESM check** | `bash scripts/esm-check-pipeheads.sh` | **PASS** — no cross-repo relative imports, all relative imports carry `.js` extensions, no `.ts` extensions in imports; exit code `0`. |

Supplementary runtime checks captured for this report:

- **CLI demo (valid fixture):** `node --loader ts-node/esm src/cli/run-pipehead-demo.ts` → exit `0`; four parseable JSON blocks printed.
- **CLI demo determinism:** two consecutive runs → identical `outputHash` (`4b6dd6…d8dc`); only the excluded `analystScore.scoredAt` differs.
- **CLI demo (invalid fixture):** exit `2`; structured `DemoError`; no audit block emitted.

> **Note on a pre-existing Jest warning.** `npm test` ends with "A worker process has failed to exit gracefully." This is PRE-EXISTING and originates from `MLProviderRegistry` timers in the unrelated `src/dag` test suites — **not** from pipehead code (pipehead tests are pure and leak no handles). It is not a mission regression and is documented as do-not-fix in `AGENTS.md`.

---

## 6. What is deterministic (source of truth)

The **deterministic source of truth** is the afi-core kernel, invoked **unchanged**:

- **Scorer:** `scoreFroggyTrendPullbackFromEnriched(enriched)` from `afi-core/analysts/froggy.trend_pullback_v1.js` (`analystId="froggy"`, `strategyId="trend_pullback_v1"`). The scoring pipehead carries its `AnalystScoreTemplate` through **verbatim** and never recomputes or re-weights anything.
- **Universal Weighting Rule (UWR):** `defaultUwrConfig` is used **unchanged** — four equal axis weights of `0.25`, so `uwrScore` equals the equal-weight mean of the four `uwrAxes`. For the canonical fixture this is verifiable: `mean(0.15, 0, 0.2, 0.4) = 0.1875 = uwrScore`.

Determinism is mandatory and enforced end to end: identical input ⇒ identical output ⇒ identical content hash. Runtime timestamps come from an injectable clock and are excluded from every hash; the `outputHash` commits the deterministic scoring projection, never the raw timestamped object. The committed `golden.json` is the replay anchor — a recompute that diverges signals nondeterminism or an unreviewed scoring/canonicalization change. The mission introduced **no** changes to `afi-core`, `afi-math`, or `afi-config`; the scorer and UWR config are referenced read-only via the `afi-core/...` package name.

---

## 7. What is Droid-operated

Droids **operate** the pipeline machinery; they do **not adjudicate** outcomes. Concretely, Droids built/operate only the machinery:

- schema validation (structural pre-check),
- the five-lane analysis fan-out,
- fan-in normalization into the `AnalysisBundle` + `FroggyEnrichedView`,
- **invocation** of the deterministic afi-core scorer (carrying its output through verbatim),
- the demo-only reputation receipt,
- the content-hashed, replayable audit record,
- and the tests, fixtures, CLI demo, and documentation.

Droids never substitute LLM/subjective judgment for a score, a validation decision, or any trust-critical output. **The score is produced solely by the deterministic afi-core kernel (§6); no pipehead authors, re-implements, re-weights, or "adjusts" the score, UWR, or reputation math.** The pipeheads only transport, bind, hash, and present it.

---

## 8. What is demo-only / provisional

Nothing here is canonical protocol truth. Every protocol-shaped output is explicitly labeled:

- `DemoScoredSignal` — `demoOnly: true` and `provisional: true`.
- `DemoReputationReceipt` — `receiptKind: "demo-only"`, `mutatesReputationState: false`, plus a non-canonical `note`. It mutates **no** reputation state and performs no DB/vault writes.
- `AuditRecord` — `demoOnly: true` and `scoredAtExcluded: true`.

**Provisional lanes (committed fixtures, no network, no external adapter, `provisional: true`):**

- **`news`** — committed news fixture; self-labeled provisional in its own payload + note.
- **`social`** — committed sentiment fixture (maps to `enrichedView.sentiment`); self-labeled provisional.
- **`ai-ml`** — committed AI/ML fixture (no Tiny Brains, no model inference, no network); self-labeled provisional.

The **wired** lanes (`technical-indicators`, `pattern-recognition`) are `provisional: false` and compute real deterministic math over committed fixture OHLCV. This is a non-production POC; **no part of this system is production-ready or canonical protocol truth.**

### Offline reuse limitations (Decision Records)

Two trust-relevant afi-reactor modules could not be reused **offline**, so self-contained equivalents were used behind clean seams. These are recorded as DR-001 and DR-002 in the mission `AGENTS.md` and in `docs/PIPEHEAD_SYSTEM.md`.

**DR-001 — Schema validation uses a self-contained OFFLINE structural validator (NOT canonical USS validation).**
- *Limitation.* The canonical USS validator `src/uss/ussValidator.ts` (`validateUsignalV11`) could **not** be reused offline: its module-level `import { Ajv } from "ajv"` throws because `ajv`/`ajv-formats` are not installed/resolvable (absent from `package.json`/lockfile, not installable offline), and the afi-config schemas are absent from `node_modules`.
- *POC decision.* This POC uses a **self-contained STRUCTURAL validator only** (`src/pipeheads/schemaValidationPipehead.ts`) enforcing the same minimum USS v1.1 rules (top-level `schema` + `provenance`; `schema === "afi.usignal.v1.1"`; `provenance.source`/`providerId`/`signalId` present and correctly typed) and returning the same `{ ok, errors:[{field,message}] }` contract, self-labeled structural / POC / demo-only / non-canonical. It is **not** a replacement for canonical USS validation.
- *Recommended future fix.* Restore canonical USS validation by resolving the `ajv`/`ajv-formats` + afi-config schema dependency path, then swap `validateUssV11Structural` for canonical `validateUsignalV11` at the existing clean seam (no caller change).

**DR-002 — WIRED technical lane uses a self-contained OFFLINE EMA/RSI/ATR helper (NOT the canonical indicator kernel).**
- *Limitation.* The canonical technical-indicator kernel (`src/enrichment/technicalIndicators.ts` → `src/indicator/*`) could **not** be reused offline: that import chain hard-imports `trading-signals` (`import { EMA, RSI, ATR } from "trading-signals"`), which is not installed, not cached, not installable offline, and absent from `package.json`/lockfile. (It is a runtime-only break: those files are `@ts-nocheck`, so a scoped typecheck does not catch it.)
- *POC decision.* The WIRED `technical-indicators` lane computes its indicators with a **self-contained OFFLINE EMA/RSI/ATR helper** (`src/pipeheads/lanes/technicalIndicators.ts`: EMA-20/50, RSI-14, ATR-14 + `trendBias`/`emaDistancePct`), mirroring the repo's own deprecated pure formulas, over committed fixture OHLCV. The lane stays genuinely **wired** (`provisional: false`, real deterministic math) and self-labels its indicators as a self-contained / non-canonical offline computation. **Scoring stays 100% afi-core** — only the lane's indicator inputs use the offline helper; the deterministic scorer + UWR are reused offline, unchanged.
- *Recommended future fix.* Restore the canonical indicator kernel by resolving the `trading-signals` dependency, then swap the offline helper for `computeTechnicalEnrichment` / `src/indicator/*` at the existing clean seam (no lane-contract change).

---

## 9. What remains out of scope

The following are explicitly **out of scope** for this mission and were not touched (Charter / Pipehead Addendum exclusions, mission `architecture.md` §8):

- Token logic, minting, treasury, vault/settlement logic, emissions math, reward distribution.
- Live trading, production deploys, production keys/secrets.
- Any change to core **scoring / UWR / reputation math**, and any **mutation of reputation state** (the receipt is non-mutating only).
- Any live external dependency / network / DB / server / port (the demo and tests run fully offline against committed fixtures).
- The pre-existing `src/dag/**` pipeline and the `afi-factory` import it depends on.

**Known pre-existing issues (do-not-fix, unrelated to this mission):**
- `npm run build` (full `tsc`) is RED because `src/dag/nodes/AnalystNode.ts` imports unresolved `afi-factory/*` — outside this footprint; the scoped `tsc -p tsconfig.pipeheads.json` is used instead.
- `npm run esm:check` (full) is RED from pre-existing test-file violations — the scoped `scripts/esm-check-pipeheads.sh` is used instead.
- The Jest "worker process failed to exit gracefully" warning originates from `MLProviderRegistry` timers in the `src/dag` suites, not pipehead code.

---

## 10. Recommended next mission

**Proposed next mission: "Restore canonical USS validation and the canonical indicator kernel (online-enabled)."** With network/registry access available, a focused follow-on should:

1. **Restore canonical USS validation (DR-001).** Resolve the `ajv` / `ajv-formats` + afi-config schema dependency path, then swap `validateUssV11Structural` for canonical `validateUsignalV11` at the existing clean seam; add tests proving the canonical validator accepts/rejects the same fixtures and the structural pre-check can be retired or relegated.
2. **Restore the canonical indicator kernel (DR-002).** Resolve the `trading-signals` dependency, then swap the offline EMA/RSI/ATR helper for `computeTechnicalEnrichment` / `src/indicator/*` at the clean seam; re-pin the golden replay hashes under the canonical indicators (scoring already stays in afi-core).

Further follow-on work (separate missions, all still governance-bound): wire the three provisional lanes (`news`, `social`, `ai-ml`) to real, governed data sources behind the existing lane seams; extend provenance and add a governed, auditable persistence path for audit records; and build operator/replay tooling for drift detection over the content-hashed audit records. Token/mint/treasury/vault/settlement, emissions, reward distribution, live trading, production deploys, and any change to core scoring/UWR/reputation math remain out of scope and governed by the Charter and Pipehead Addendum.

---

*This report describes a non-production POC. It records the actual implemented code and the real gate/demo outcomes captured on 2026-06-30. No part of the system is presented as production-ready or as canonical protocol truth.*
