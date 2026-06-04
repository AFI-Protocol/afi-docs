> **Historical note:** This document describes a superseded LangGraph-era architecture plan. AFI Reactor now uses a custom deterministic TypeScript DAG under `afi-reactor/src/dag/`. This file is retained only for historical context and should not be treated as current implementation guidance.
>

# AFI LangGraph Terminology Elimination - Phase 2 Execution Plan

**Date:** 2025-12-28  
**Status:** Ready for Execution  
**Phase:** 2 (Source Code Updates)

---

## Executive Summary

This document provides a comprehensive, safe execution plan for **Phase 2** of the LangGraph terminology elimination in the afi-reactor codebase. Phase 1 (directory and file renaming) is **PARTIALLY COMPLETE** with critical issues that need resolution before Phase 2 can proceed safely.

### Current Status Assessment

**✅ Completed in Phase 1:**
- [`afi-core/src/dag/SignalEnvelope.ts`](afi-core/src/dag/SignalEnvelope.ts) created with proper naming (SignalEnvelope interface)
- [`afi-reactor/src/types/pipeline.ts`](afi-reactor/src/types/pipeline.ts) created (visible in open tabs)

**❌ CRITICAL ISSUES - Not Completed in Phase 1:**
1. **Duplicate File:** [`afi-core/src/langgraph/LangGraphSignalEnvelope.ts`](afi-core/src/langgraph/LangGraphSignalEnvelope.ts) still exists (identical to dag/SignalEnvelope.ts)
2. **Directory Not Renamed:** [`afi-reactor/src/langgraph/`](afi-reactor/src/langgraph/) directory still exists (should be renamed to `dag/`)
3. **Old Import Paths:** Multiple files still import from `types/langgraph.js` instead of `types/pipeline.js`
4. **Test File References:** Test files still reference `LangGraphState` instead of `PipelineState`

### Risk Assessment

**Current Risk Level:** 🔴 HIGH

**Why High Risk:**
- Duplicate files create ambiguity about which is the source of truth
- Mixed import paths will cause build failures when old files are removed
- Test failures likely if Phase 2 proceeds without Phase 1 completion

---

## Phase 1 Completion Requirements

**BEFORE** proceeding with Phase 2, Phase 1 must be properly completed:

### Step P1.1: Rename afi-reactor Directory
```bash
cd afi-reactor/src
mv langgraph dag
```

**Files Affected:** All files in [`afi-reactor/src/langgraph/`](afi-reactor/src/langgraph/)

### Step P1.2: Cleanup afi-core Duplicates
```bash
cd afi-core/src
rm -rf langgraph/  # After verifying dag/SignalEnvelope.ts is correct
```

**Verification Required:**
- Confirm [`afi-core/src/dag/SignalEnvelope.ts`](afi-core/src/dag/SignalEnvelope.ts) exports `SignalEnvelope` interface
- Confirm no other code imports from `afi-core/src/langgraph/*`

### Step P1.3: Update Build Configuration
- Update [`afi-reactor/jest.config.js`](afi-reactor/jest.config.js) line 29:
  - From: `"**/src/langgraph/__tests__/*.test.ts"`
  - To: `"**/src/dag/__tests__/*.test.ts"`

---

## Phase 2 Execution Plan

Phase 2 focuses on **source code content** updates, NOT file/directory renaming.

### Terminology Replacements
| Old Term | New Term | Usage Context |
|----------|----------|---------------|
| `LangGraph` | `DAG` | Comments, JSDoc, descriptions |
| `LangGraphNode` | `DAGNode` | Class/interface names (**Note:** Already changed to `Pipehead` in types) |
| `LangGraphState` | `PipelineState` | Type references |
| `LangGraphSignalEnvelope` | `SignalEnvelope` | Interface name |
| `from '../types/langgraph'` | `from '../types/pipeline'` | Import statements |
| `from '../../types/langgraph'` | `from '../../types/pipeline'` | Import statements (nested) |
| `@module .../langgraph/...` | `@module .../dag/...` | JSDoc module paths |

### Phase 2 Breakdown

#### 2.1: Import Statement Updates

**Scope:** All TypeScript files importing from old paths

**Files to Update:**

1. **afi-reactor Test Files:**
   - [`afi-reactor/src/langgraph/__tests__/test-utils.ts`](afi-reactor/src/langgraph/__tests__/test-utils.ts:11)
   - [`afi-reactor/src/langgraph/__tests__/integration.test.ts`](afi-reactor/src/langgraph/__tests__/integration.test.ts:11)
   - [`afi-reactor/src/langgraph/__tests__/PluginRegistry.test.ts`](afi-reactor/src/langgraph/__tests__/PluginRegistry.test.ts:10)
   - [`afi-reactor/src/langgraph/__tests__/DAGBuilder.test.ts`](afi-reactor/src/langgraph/__tests__/DAGBuilder.test.ts:10)
   - [`afi-reactor/src/langgraph/__tests__/DAGExecutor.test.ts`](afi-reactor/src/langgraph/__tests__/DAGExecutor.test.ts:10)
   - [`afi-reactor/src/langgraph/__tests__/AiMlNode.test.ts`](afi-reactor/src/langgraph/__tests__/AiMlNode.test.ts:10)

2. **afi-reactor Plugin Test Files:**
   - [`afi-reactor/src/langgraph/plugins/__tests__/ScoutNode.test.ts`](afi-reactor/src/langgraph/plugins/__tests__/ScoutNode.test.ts:9)
   - [`afi-reactor/src/langgraph/plugins/__tests__/SentimentNode.test.ts`](afi-reactor/src/langgraph/plugins/__tests__/SentimentNode.test.ts:9)
   - [`afi-reactor/src/langgraph/plugins/__tests__/PatternRecognitionNode.test.ts`](afi-reactor/src/langgraph/plugins/__tests__/PatternRecognitionNode.test.ts:9)
   - [`afi-reactor/src/langgraph/plugins/__tests__/SignalIngressNode.test.ts`](afi-reactor/src/langgraph/plugins/__tests__/SignalIngressNode.test.ts:9)
   - [`afi-reactor/src/langgraph/plugins/__tests__/NewsNode.test.ts`](afi-reactor/src/langgraph/plugins/__tests__/NewsNode.test.ts:9)
   - [`afi-reactor/src/langgraph/plugins/__tests__/TechnicalIndicatorsNode.test.ts`](afi-reactor/src/langgraph/plugins/__tests__/TechnicalIndicatorsNode.test.ts:9)

3. **afi-reactor Node Test Files:**
   - [`afi-reactor/src/langgraph/nodes/__tests__/AnalystNode.test.ts`](afi-reactor/src/langgraph/nodes/__tests__/AnalystNode.test.ts:9)
   - [`afi-reactor/src/langgraph/nodes/__tests__/ObserverNode.test.ts`](afi-reactor/src/langgraph/nodes/__tests__/ObserverNode.test.ts:9)
   - [`afi-reactor/src/langgraph/nodes/__tests__/ExecutionNode.test.ts`](afi-reactor/src/langgraph/nodes/__tests__/ExecutionNode.test.ts:9)
   - [`afi-reactor/src/langgraph/nodes/__tests__/nodes-integration.test.ts`](afi-reactor/src/langgraph/nodes/__tests__/nodes-integration.test.ts:11)

4. **afi-reactor State Management:**
   - [`afi-reactor/src/state/StateSerializer.ts`](afi-reactor/src/state/StateSerializer.ts:13)
   - [`afi-reactor/src/state/StateManager.ts`](afi-reactor/src/state/StateManager.ts:13)
   - [`afi-reactor/src/state/StateValidator.ts`](afi-reactor/src/state/StateValidator.ts:13)

5. **afi-reactor Test Integration:**
   - [`afi-reactor/test/integration/state-lifecycle.test.ts`](afi-reactor/test/integration/state-lifecycle.test.ts:12)
   - [`afi-reactor/test/state-management.test.ts`](afi-reactor/test/state-management.test.ts:11)

6. **afi-reactor Type Tests:**
   - [`afi-reactor/src/types/__tests__/langgraph.test.ts`](afi-reactor/src/types/__tests__/langgraph.test.ts:21) - 2 import statements

**Pattern to Find:**
```regex
from ['"].*types/langgraph['"']
```

**Replacement Pattern:**
```typescript
// OLD:
import type { PipelineState } from '../types/langgraph.js';
import type { PipelineState } from '../../types/langgraph.js';

// NEW:
import type { PipelineState } from '../types/pipeline.js';
import type { PipelineState } from '../../types/pipeline.js';
```

#### 2.2: Type Name Updates

**Scope:** Variable declarations, function parameters, type annotations

**Type Replacements:**

| Old Type Name | New Type Name | Files Affected |
|---------------|---------------|----------------|
| `LangGraphState` | `PipelineState` | ~15 test files |
| `langGraphStateTest1` | `pipelineStateTest1` | Type test file |
| `validLangGraphState` | `validPipelineState` | Type test file |
| `minimalLangGraphState` | `minimalPipelineState` | Type test file |

**Example from [`afi-reactor/src/langgraph/nodes/__tests__/ObserverNode.test.ts`](afi-reactor/src/langgraph/nodes/__tests__/ObserverNode.test.ts):**
```typescript
// OLD:
let mockState: LangGraphState;

// NEW:
let mockState: PipelineState;
```

#### 2.3: JSDoc Module Path Updates

**Scope:** All `@module` annotations in source files

**Pattern to Find:**
```regex
@module afi-reactor/src/langgraph/
@module afi-core/src/langgraph/
```

**Replacement:**
```typescript
// OLD:
 * @module afi-reactor/src/langgraph/PluginRegistry

// NEW:
 * @module afi-reactor/src/dag/PluginRegistry
```

**Files Affected:** All source files in langgraph/ directories (~35 files)

#### 2.4: JSDoc Comment Updates

**Scope:** Parameter descriptions, class descriptions, comments

**Patterns to Replace:**

1. **"LangGraph state" → "pipeline state"**
   ```typescript
   // OLD:
    * @param state - The current LangGraph state
   
   // NEW:
    * @param state - The current pipeline state
   ```

2. **"LangGraph DAG" → "DAG"**
   ```typescript
   // OLD:
    * The Observer node is the third and final required node in the LangGraph DAG.
   
   // NEW:
    * The Observer node is the third and final required node in the DAG.
   ```

3. **"LangGraph plugins" → "DAG plugins"**
   ```typescript
   // OLD:
    * Centralized registry for managing all LangGraph plugins.
   
   // NEW:
    * Centralized registry for managing all DAG plugins.
   ```

**Files Affected:** All node and plugin implementation files (~20 files)

#### 2.5: Test Description Updates

**Scope:** Test suite names, test descriptions

**Pattern:**
```typescript
// OLD:
describe('LangGraph Integration Tests', () => {

// NEW:
describe('DAG Integration Tests', () => {
```

**Files Affected:**
- [`afi-reactor/src/langgraph/__tests__/integration.test.ts`](afi-reactor/src/langgraph/__tests__/integration.test.ts:45)
- Other integration test files

#### 2.6: File Comment Headers

**Scope:** File header comments

**Example from [`afi-reactor/src/langgraph/__tests__/test-utils.ts`](afi-reactor/src/langgraph/__tests__/test-utils.ts):**
```typescript
// OLD:
/**
 * AFI Reactor - LangGraph Test Utilities
 *
 * Comprehensive test utilities and fixtures for LangGraph integration tests.
 */

// NEW:
/**
 * AFI Reactor - DAG Test Utilities
 *
 * Comprehensive test utilities and fixtures for DAG integration tests.
 */
```

---

## Safety Measures

### Pre-Execution Checklist

- [ ] Verify Phase 1 directory renaming is complete
- [ ] Verify no duplicate files exist
- [ ] Create git branch for Phase 2: `feature/phase-2-code-updates`
- [ ] Run full test suite to establish baseline
- [ ] Back up current codebase state

### Execution Safety Protocol

1. **Incremental Updates:** Update files in batches, not all at once
2. **Test After Each Batch:** Run relevant tests after each file group
3. **Git Commits:** Commit after each successful batch
4. **Rollback Plan:** Keep git history clean for easy rollback

### Batch Execution Order

**Batch 1: Import Statements (Low Risk)**
- Update all import statements from `langgraph` to `pipeline`
- Run: `npm run type-check`
- Commit: "refactor: update import paths from langgraph to pipeline"

**Batch 2: Type Name Updates (Medium Risk)**  
- Update `LangGraphState` → `PipelineState` in test files
- Run: `npm run test`
- Commit: "refactor: rename LangGraphState to PipelineState in tests"

**Batch 3: JSDoc Updates (Low Risk)**
- Update `@module` paths
- Update parameter descriptions
- Run: `npm run build`
- Commit: "docs: update JSDoc paths and descriptions"

**Batch 4: Comments & Descriptions (Low Risk)**
- Update class descriptions
- Update test descriptions
- Update file headers
- Run: `npm run test`
- Commit: "docs: update comments to remove LangGraph references"

### Post-Execution Verification

- [ ] Full test suite passes: `npm run test`
- [ ] Type checking passes: `npm run type-check`
- [ ] Build succeeds: `npm run build`
- [ ] No references to `LangGraph` remain (except in documentation)
- [ ] Search for remaining "langgraph" in filenames and paths

### Verification Commands

```bash
# Find remaining LangGraph references
grep -r "LangGraph" afi-reactor/src --include="*.ts" --exclude-dir=node_modules

# Find remaining langgraph imports
grep -r "from.*langgraph" afi-reactor/src --include="*.ts" --exclude-dir=node_modules

# Find remaining @module paths
grep -r "@module.*langgraph" afi-reactor/src --include="*.ts" --exclude-dir=node_modules
```

---

## Potential Issues & Mitigations

### Issue 1: Import Path Confusion

**Problem:** Files might have mixed import paths during transition

**Mitigation:**
- Use regex search to find ALL import statements before starting
- Update all imports in a single atomic commit
- Use TypeScript compiler to verify no broken imports

### Issue 2: Test Failures

**Problem:** Tests might fail if type names don't match

**Mitigation:**
- Run tests after each batch
- Keep test updates separate from source updates
- Use git bisect if failures occur

### Issue 3: Build Cache Issues

**Problem:** TypeScript/Jest might cache old paths

**Mitigation:**
```bash
# Clear build artifacts
rm -rf afi-reactor/dist
rm -rf afi-reactor/.jest-cache

# Rebuild
cd afi-reactor && npm run build
```

### Issue 4: Circular Dependencies

**Problem:** Renaming might expose circular dependencies

**Mitigation:**
- Review import graph before starting
- Fix any circular dependencies immediately
- Use `madge` tool to detect cycles

---

## File-by-File Change Summary

### High Priority Files (Must Update)

1. **afi-reactor/src/types/__tests__/langgraph.test.ts**
   - 2 import statements
   - ~30 variable name references
   - File header comments

2. **afi-reactor/src/state/StateManager.ts**
   - 1 import statement
   - Critical for runtime

3. **afi-reactor/src/state/StateSerializer.ts**
   - 1 import statement
   - Critical for runtime

4. **afi-reactor/src/state/StateValidator.ts**
   - 1 import statement
   - Critical for runtime

### Medium Priority Files (Test Files)

- All test files in [`afi-reactor/src/langgraph/__tests__/`](afi-reactor/src/langgraph/__tests__/)
- All test files in [`afi-reactor/src/langgraph/plugins/__tests__/`](afi-reactor/src/langgraph/plugins/__tests__/)
- All test files in [`afi-reactor/src/langgraph/nodes/__tests__/`](afi-reactor/src/langgraph/nodes/__tests__/)

### Low Priority Files (Documentation)

- JSDoc comments in implementation files
- Test descriptions
- File headers

---

## Estimated Effort

### Time Estimates

- **Phase 1 Completion:** 30-60 minutes
- **Phase 2 Execution:**
  - Batch 1 (Imports): 45-60 minutes
  - Batch 2 (Types): 30-45 minutes
  - Batch 3 (JSDoc): 60-90 minutes
  - Batch 4 (Comments): 30-45 minutes
- **Testing & Verification:** 60-90 minutes

**Total Estimated Time:** 4-6 hours

### File Counts

- **Import statements to update:** ~20 files
- **Type references to update:** ~15 files
- **JSDoc modules to update:** ~35 files
- **Comments to update:** ~50 locations
- **Test descriptions to update:** ~10 files

---

## Success Criteria

Phase 2 is complete when:

1. ✅ Zero references to `LangGraph` in source code (except proper nouns in docs)
2. ✅ All imports use `types/pipeline` instead of `types/langgraph`
3. ✅ All JSDoc `@module` paths use `dag/` instead of `langgraph/`
4. ✅ All type names use `PipelineState` instead of `LangGraphState`
5. ✅ All tests pass
6. ✅ Build succeeds without errors
7. ✅ Type checking passes

---

## Next Steps After Phase 2

1. **Documentation Updates:** Update root-level markdown files
2. **Configuration Updates:** Update any remaining config files
3. **Git Cleanup:** Squash commits if needed
4. **PR Creation:** Create pull request with detailed changelog
5. **Team Review:** Get code review from team members
6. **Merge & Deploy:** Merge to main branch after approval

---

## Troubleshooting Guide

### Problem: TypeScript errors after import updates

**Solution:**
```bash
# Clear TypeScript cache
rm -rf afi-reactor/node_modules/.cache
cd afi-reactor && npm run type-check
```

### Problem: Jest can't find modules

**Solution:**
```bash
# Clear Jest cache
npx jest --clearCache
cd afi-reactor && npm run test
```

### Problem: Circular dependency detected

**Solution:**
1. Run: `npx madge --circular afi-reactor/src`
2. Identify circular imports
3. Refactor to break cycles
4. Re-run Phase 2

### Problem: Git conflicts during batch commits

**Solution:**
1. Use `git rebase -i` to squash commits
2. Resolve conflicts manually
3. Continue with next batch

---

## Appendix A: Complete File List

### Files Requiring Import Updates (20 files)

```
afi-reactor/src/langgraph/__tests__/test-utils.ts
afi-reactor/src/langgraph/__tests__/integration.test.ts
afi-reactor/src/langgraph/__tests__/PluginRegistry.test.ts
afi-reactor/src/langgraph/__tests__/DAGBuilder.test.ts
afi-reactor/src/langgraph/__tests__/DAGExecutor.test.ts
afi-reactor/src/langgraph/__tests__/AiMlNode.test.ts
afi-reactor/src/langgraph/plugins/__tests__/ScoutNode.test.ts
afi-reactor/src/langgraph/plugins/__tests__/SentimentNode.test.ts
afi-reactor/src/langgraph/plugins/__tests__/PatternRecognitionNode.test.ts
afi-reactor/src/langgraph/plugins/__tests__/SignalIngressNode.test.ts
afi-reactor/src/langgraph/plugins/__tests__/NewsNode.test.ts
afi-reactor/src/langgraph/plugins/__tests__/TechnicalIndicatorsNode.test.ts
afi-reactor/src/langgraph/nodes/__tests__/AnalystNode.test.ts
afi-reactor/src/langgraph/nodes/__tests__/ObserverNode.test.ts
afi-reactor/src/langgraph/nodes/__tests__/ExecutionNode.test.ts
afi-reactor/src/langgraph/nodes/__tests__/nodes-integration.test.ts
afi-reactor/src/state/StateSerializer.ts
afi-reactor/src/state/StateManager.ts
afi-reactor/src/state/StateValidator.ts
afi-reactor/test/integration/state-lifecycle.test.ts
afi-reactor/test/state-management.test.ts
afi-reactor/src/types/__tests__/langgraph.test.ts
```

### Files Requiring JSDoc Module Updates (~35 files)

All source files in:
- `afi-reactor/src/langgraph/**/*.ts` (excluding test files)
- After Phase 1 completion, will be in `afi-reactor/src/dag/**/*.ts`

---

## Appendix B: Regex Patterns

### Find All Import Statements
```regex
import\s+.*\s+from\s+['"](\.\.\/)*types\/langgraph['"]
```

### Find All LangGraphState References
```regex
:\s*LangGraphState\b
```

### Find All @module References
```regex
@module\s+afi-reactor\/src\/langgraph\/
```

### Find All JSDoc "LangGraph state" References
```regex
@param\s+\w+\s+-\s+.*LangGraph\s+state
```

---

**Report Generated:** 2025-12-28  
**Author:** Architecture Analysis  
**Version:** 1.0  
**Status:** Ready for Review & Execution
