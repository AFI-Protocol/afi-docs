# AFI_CORE_BUILD_FIX — Results

**Date:** 2026-06-19
**Mission:** Make `afi-core` compile cleanly so `prepare` (`tsc`) succeeds and `file:../afi-core` consumers can `npm install` without `--ignore-scripts`.
**Diff size:** 2 lines (1 import path + 1 `scoredAt` field). No refactors, no semantic/UWR changes.

---

## Fixes applied

### Error 1 — broken import path (TS2307)
`afi-core/validators/ValidatorDecision.ts:12`
```diff
- import type { AnalystScoreTemplate } from "../analyst/AnalystScoreTemplate.js";
+ import type { AnalystScoreTemplate } from "../src/analyst/AnalystScoreTemplate.js";
```
The module lives at `src/analyst/AnalystScoreTemplate.ts`; `analysts/froggy.trend_pullback_v1.ts` already used the correct `../src/analyst/...` path. No file was moved.

### Error 2 — missing required `scoredAt` (TS2741)
`afi-core/analysts/froggy.trend_pullback_v1.ts` — `buildAnalystScoreTemplate()` `analystScore` object, Time / horizon section:
```diff
  signalTimeframe: enriched?.timeframe || "1h", // default to 1h if not available
  holdingHorizon: "swing", // Froggy trend_pullback_v1 is typically swing trading
+ scoredAt: new Date().toISOString(), // ISO 8601 — when scoring completed (required for decay)
```
`AnalystScoreTemplate` requires `scoredAt: string` (contract line 68; Zod `z.string().datetime()` line 156). No optional `now?: Date` param was needed — the existing test passes with the default.

---

## Verification

| Check | Pass/Fail | Evidence |
|-------|-----------|----------|
| afi-core `tsc` clean | ✅ PASS | `rm -rf dist && npm run build` → exit 0, zero errors |
| `dist/` complete | ✅ PASS | `dist/validators/ValidatorDecision.js` + `dist/src/analyst/AnalystScoreTemplate.js` present¹ |
| afi-core vitest | ✅ 59 passed | `npm run test:run` → **6 files / 59 tests pass**, incl. `froggy.trend_pullback_v1.test.ts` (5) which exercises `buildAnalystScoreTemplate` with the new `scoredAt`. 2 suite errors are pre-existing & unrelated² |
| afi-reactor `npm install` (no `--ignore-scripts`) | ✅ PASS | `rm -rf node_modules && npm install` → exit 0, 464 packages; afi-core `prepare`/`tsc` ran via the `file:` link |
| afi-reactor jest 425/425 | ✅ PASS | `npm test` → **10 suites / 425 tests** (same as post-purge baseline) |

¹ `dist/index.js` is **not** produced because there is no root `index.ts` in afi-core — pre-existing (`package.json` `main` points at a path that never existed). Out of scope (mission = compile/test green, no file moves); flagged as a separate follow-up.

² The two failing vitest **suites** are independent of this 2-line change:
- `validators/__tests__/SignalDecay.test.ts` — `Cannot find module '@afi-protocol/afi-math/dist/timeValue/timeValue'`. The **sibling `afi-math` package ships an incomplete `dist/`** (same class of problem afi-core had). Not touched by this fix.
- `src/analyst/__tests__/AnalystScoreTemplate.test.ts` — "No test suite found". The file is a **compile-time type-assertion file with no runtime `test()`/`describe()`** (its own header: "without requiring a test framework"). It registers no suite; pre-existing.

---

## Optional second consumer — afi-infra

`afi-infra` `npm run build` **fails, but for pre-existing reasons unrelated to afi-core** (not caused by this fix — none of the errors reference afi-core):
- `Cannot find name 'console' / 'process'` → afi-infra's own tsconfig is missing `@types/node` / `lib` config.
- `Cannot find module 'vitest'` → afi-infra's `node_modules` is not installed.

Left as-is (out of scope — afi-infra dependency/tsconfig hygiene is its own task).

---

## Optional — gateway uwrAxes drift (NOT fixed; follow-up)

`afi-gateway/src/afiClient.ts` declares `uwrAxes { utility, workQuality, rarity }`; the canonical reactor axes are `{ structure, execution, risk, insight }`. Not addressed here — it is gateway-side, unrelated to the afi-core build, and changing it risks gateway type/consumer breakage that is out of this PR's scope. Recommended as a separate gateway follow-up.

---

## Hard rules honored

- Minimal diff (2 lines); no refactors / no feature work.
- `ValidatorDecision` semantics and UWR math unchanged.
- `AnalystScoreTemplate.scoredAt` kept required (satisfied, not weakened).
- No legacy purge artifacts touched.
- `--ignore-scripts` is no longer needed — it was **not** used as the fix.
- Not committed (repo is not a git repo; no commit requested).

**Next:** afi-core build is green and installable; ready for downstream `afi-reactor` + Mongo TSSD reference-implementation work.
