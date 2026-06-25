# Claude Code Prompt — Fix `afi-core` Build (P0)

**Mission:** Make `afi-core` compile cleanly so `npm run prepare` succeeds and `file:../afi-core` consumers (`afi-reactor`, `afi-infra`) can `npm install` without `--ignore-scripts`.

**Context:** Legacy pipeline purge is done. Reactor tests pass only when install skips `afi-core` prepare. Root cause is **2 TypeScript errors** in `afi-core` (verified 2026-06-19).

**Parent:** Post-purge follow-up · unblocks downstream `file:` consumers

---

## Copy-paste prompt

```
# MISSION: Fix afi-core TypeScript build (P0)

Workspace: /home/user/AFI-Protocol/afi-core

## Current failures (reproduce first)

cd /home/user/AFI-Protocol/afi-core && npm run build

Expected errors today (fix these; if more appear, fix all until clean):

1. validators/ValidatorDecision.ts(12,43): error TS2307
   Cannot find module '../analyst/AnalystScoreTemplate.js'
   → File actually lives at: src/analyst/AnalystScoreTemplate.ts
   → froggy.trend_pullback_v1.ts already imports correctly:
     from "../src/analyst/AnalystScoreTemplate.js"

2. analysts/froggy.trend_pullback_v1.ts(222,9): error TS2741
   Property 'scoredAt' is missing in type '...' but required in type 'AnalystScoreTemplate'
   → buildAnalystScoreTemplate() must set scoredAt (ISO 8601)
   → AnalystScoreTemplate requires scoredAt per src/analyst/AnalystScoreTemplate.ts:68

## Hard rules

1. Minimal diff — fix build only; no refactors, no feature work
2. Do NOT change ValidatorDecision semantics or UWR math
3. Do NOT delete or weaken AnalystScoreTemplate.scoredAt (required for decay)
4. Do NOT touch legacy purge artifacts unless a test breaks
5. Do NOT commit unless user asks
6. Do NOT use --ignore-scripts as the "fix"

## Fix guidance

### Error 1 — import path

In validators/ValidatorDecision.ts line 12, change:

  import type { AnalystScoreTemplate } from "../analyst/AnalystScoreTemplate.js";

To:

  import type { AnalystScoreTemplate } from "../src/analyst/AnalystScoreTemplate.js";

Ripgrep after fix — no remaining broken imports from validators/:

  rg -n 'from \"\\.\\./analyst/AnalystScoreTemplate' afi-core/validators

### Error 2 — scoredAt

In analysts/froggy.trend_pullback_v1.ts, function buildAnalystScoreTemplate(),
add to the analystScore object (under Time / horizon section):

  scoredAt: new Date().toISOString(),

Place alongside signalTimeframe / holdingHorizon. This matches the template contract
used by ValidatorDecision.computeValidatorScore() for decay (uses scoredAt).

If buildAnalystScoreTemplate is called in tests with deterministic time needs,
prefer optional `now?: Date` parameter only if tests require it — default to
new Date().toISOString() for minimal fix.

Ensure AnalystScoreTemplateSchema.safeParse still passes after the change.

## Verification (run in order; all must pass)

### 1. afi-core build
cd /home/user/AFI-Protocol/afi-core
rm -rf dist
npm run build
# Expect: exit 0, dist/ populated including dist/validators/ and dist/src/analyst/

### 2. afi-core tests
npm run test:run
# Expect: all vitest tests pass

### 3. Downstream install WITHOUT ignore-scripts
cd /home/user/AFI-Protocol/afi-reactor
rm -rf node_modules
npm install
# Must NOT require --ignore-scripts; afi-core prepare must run via file: link

### 4. afi-reactor regression
cd /home/user/AFI-Protocol/afi-reactor
npm test
# Expect: 10 suites / 425 tests pass (same as post-purge baseline)

### 5. Optional second consumer
cd /home/user/AFI-Protocol/afi-infra
npm run build 2>/dev/null || npm run typecheck 2>/dev/null || true
# Report result; fix only if your afi-core change broke it

## Deliverable

Write: afi-docs/specs/audit/AFI_CORE_BUILD_FIX_RESULTS.md

| Check | Pass/Fail | Evidence |
|-------|-----------|----------|
| afi-core tsc clean | | npm run build output |
| dist/ complete | | ls dist/validators dist/src/analyst |
| afi-core vitest | | test:run summary |
| afi-reactor npm install (no ignore-scripts) | | install log |
| afi-reactor jest 425/425 | | npm test tail |

## Optional (only if trivial, same PR mindset)

Gateway uwrAxes drift (NOT required for this mission):
- afi-gateway/src/afiClient.ts uses { utility, workQuality, rarity }
- Canonical axes: { structure, execution, risk, insight }
- Skip unless fix is <10 lines and tests exist; otherwise note in RESULTS as follow-up

## Out of scope

- Mongo removal
- afi-mint changes
- Moving AnalystScoreTemplate file location (path fix only)
- Gateway ingest work
```

---

## Why this blocks everything

`afi-core/package.json` runs `"prepare": "npm run build"` on install. `afi-reactor` depends on `"afi-core": "file:../afi-core"`. Broken `tsc` → broken `dist/` → install fails → Froggy/UWR imports break in any fresh workspace.

## Expected fix size

**2 lines changed** (1 import path + 1 `scoredAt` field). If build reveals more errors, fix them — but do not expand scope beyond compile/test green.

---

*After green: afi-core is installable; proceed with downstream `afi-reactor` + Mongo TSSD reference-implementation work.*
