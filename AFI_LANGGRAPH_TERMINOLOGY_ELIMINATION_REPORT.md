# AFI LangGraph Terminology Elimination Report

**Date:** 2025-12-28
**Task:** Comprehensive scan of the entire afi-reactor codebase to locate every instance of the term "langgraph" (case-insensitive) and provide recommendations for elimination
**Scope:** afi-reactor, afi-core, plans, and root documentation

---

## Executive Summary

This report provides a comprehensive analysis of all instances of the term "langgraph" (case-insensitive) found across the AFI codebase. The scan identified **500+ occurrences** across:

- **Source code files** (afi-reactor, afi-core)
- **Documentation files** (plans, root markdown files)
- **Configuration files** (jest.config.js)
- **Test files** (unit tests, integration tests)
- **Third-party dependencies** (node_modules - excluded from recommendations)

**Key Finding:** The codebase has already begun refactoring from "LangGraph" terminology to "Pipehead/PipelineState" terminology in [`afi-reactor/src/types/langgraph.ts`](afi-reactor/src/types/langgraph.ts), but the directory name and many files still reference "LangGraph" in comments, JSDoc, and module names.

---

## Table of Contents

1. [Directory and File Names](#directory-and-file-names)
2. [afi-reactor Source Code](#afi-reactor-source-code)
3. [afi-core Source Code](#afi-core-source-code)
4. [Documentation Files](#documentation-files)
5. [Configuration Files](#configuration-files)
6. [Test Files](#test-files)
7. [Third-Party Dependencies](#third-party-dependencies)
8. [Recommendations Summary](#recommendations-summary)

---

## Directory and File Names

### 1. Directory: `afi-reactor/src/langgraph/`

**Path:** `afi-reactor/src/langgraph/`
**Type:** Directory
**Context:** Contains the entire DAG orchestration implementation
**Recommendation:** Rename directory to `afi-reactor/src/dag/` or `afi-reactor/src/pipeline/`
**Rationale:** The directory name is the most visible reference to "langgraph" in the codebase. Renaming it to "dag" or "pipeline" would eliminate confusion with the LangGraph library and better reflect the custom AFI implementation.

### 2. Directory: `afi-core/src/langgraph/`

**Path:** `afi-core/src/langgraph/`
**Type:** Directory
**Context:** Contains signal envelope types for DAG execution
**Recommendation:** Rename directory to `afi-core/src/dag/` or `afi-core/src/pipeline/`
**Rationale:** Consistent with afi-reactor directory renaming recommendation.

### 3. File: `afi-reactor/src/types/langgraph.ts`

**Path:** `afi-reactor/src/types/langgraph.ts`
**Type:** TypeScript type definitions
**Context:** Core type definitions for pipeline orchestration (already uses Pipehead/PipelineState naming)
**Recommendation:** Rename file to `afi-reactor/src/types/pipeline.ts` or `afi-reactor/src/types/dag.ts`
**Rationale:** File name should match directory naming and reflect the actual content (pipeline types, not "langgraph").

### 4. File: `afi-core/src/langgraph/LangGraphSignalEnvelope.ts`

**Path:** `afi-core/src/langgraph/LangGraphSignalEnvelope.ts`
**Type:** TypeScript interface definitions
**Context:** Signal envelope with enrichment results and execution metadata
**Recommendation:** Rename file to `afi-core/src/dag/SignalEnvelope.ts` and rename interface to `SignalEnvelope`
**Rationale:** Remove "LangGraph" branding from interface name and file name.

### 5. File: `afi-reactor/src/types/__tests__/langgraph.test.ts`

**Path:** `afi-reactor/src/types/__tests__/langgraph.test.ts`
**Type:** Test file
**Context:** Type tests for pipeline types
**Recommendation:** Rename file to `afi-reactor/src/types/__tests__/pipeline.test.ts`
**Rationale:** Consistent with source file renaming.

---

## afi-reactor Source Code

### 6. File: `afi-reactor/src/types/langgraph.ts`

**Path:** `afi-reactor/src/types/langgraph.ts`
**Line:** 10
**Context:** JSDoc module comment
```typescript
 * @module afi-reactor/src/types/langgraph
```
**Recommendation:** Change to `@module afi-reactor/src/types/pipeline`
**Rationale:** Update module path to reflect new file name.

### 7. File: `afi-reactor/src/langgraph/PluginRegistry.ts`

**Path:** `afi-reactor/src/langgraph/PluginRegistry.ts`
**Line:** 11
**Context:** JSDoc module comment
```typescript
 * @module afi-reactor/src/langgraph/PluginRegistry
```
**Recommendation:** Change to `@module afi-reactor/src/dag/PluginRegistry`
**Rationale:** Update module path to reflect new directory structure.

**Line:** 97
**Context:** JSDoc comment
```typescript
 * Centralized registry for managing all LangGraph plugins.
```
**Recommendation:** Change to "Centralized registry for managing all DAG plugins."
**Rationale:** Remove "LangGraph" branding from documentation.

### 8. File: `afi-reactor/src/langgraph/plugins/ScoutNode.ts`

**Path:** `afi-reactor/src/langgraph/plugins/ScoutNode.ts`
**Line:** 16
**Context:** JSDoc module comment
```typescript
 * @module afi-reactor/src/langgraph/plugins/ScoutNode
```
**Recommendation:** Change to `@module afi-reactor/src/dag/plugins/ScoutNode`
**Rationale:** Update module path to reflect new directory structure.

**Line:** 60
**Context:** JSDoc parameter comment
```typescript
 * @param state - The current LangGraph state
```
**Recommendation:** Change to "The current pipeline state"
**Rationale:** Remove "LangGraph" branding from parameter documentation.

### 9. File: `afi-reactor/src/langgraph/plugins/SignalIngressNode.ts`

**Path:** `afi-reactor/src/langgraph/plugins/SignalIngressNode.ts`
**Line:** 11
**Context:** JSDoc module comment
```typescript
 * @module afi-reactor/src/langgraph/plugins/SignalIngressNode
```
**Recommendation:** Change to `@module afi-reactor/src/dag/plugins/SignalIngressNode`
**Rationale:** Update module path to reflect new directory structure.

**Line:** 48
**Context:** JSDoc parameter comment
```typescript
 * @param state - The current LangGraph state
```
**Recommendation:** Change to "The current pipeline state"
**Rationale:** Remove "LangGraph" branding from parameter documentation.

### 10. File: `afi-reactor/src/langgraph/DAGExecutor.ts`

**Path:** `afi-reactor/src/langgraph/DAGExecutor.ts`
**Line:** 14
**Context:** JSDoc module comment
```typescript
 * @module afi-reactor/src/langgraph/DAGExecutor
```
**Recommendation:** Change to `@module afi-reactor/src/dag/DAGExecutor`
**Rationale:** Update module path to reflect new directory structure.

### 11. File: `afi-reactor/src/langgraph/plugins/PatternRecognitionNode.ts`

**Path:** `afi-reactor/src/langgraph/plugins/PatternRecognitionNode.ts`
**Line:** 11
**Context:** JSDoc module comment
```typescript
 * @module afi-reactor/src/langgraph/plugins/PatternRecognitionNode
```
**Recommendation:** Change to `@module afi-reactor/src/dag/plugins/PatternRecognitionNode`
**Rationale:** Update module path to reflect new directory structure.

**Line:** 48
**Context:** JSDoc parameter comment
```typescript
 * @param state - The current LangGraph state
```
**Recommendation:** Change to "The current pipeline state"
**Rationale:** Remove "LangGraph" branding from parameter documentation.

### 12. File: `afi-reactor/src/langgraph/DAGBuilder.ts`

**Path:** `afi-reactor/src/langgraph/DAGBuilder.ts`
**Line:** 13
**Context:** JSDoc module comment
```typescript
 * @module afi-reactor/src/langgraph/DAGBuilder
```
**Recommendation:** Change to `@module afi-reactor/src/dag/DAGBuilder`
**Rationale:** Update module path to reflect new directory structure.

### 13. File: `afi-reactor/src/langgraph/plugins/AiMlNode.ts`

**Path:** `afi-reactor/src/langgraph/plugins/AiMlNode.ts`
**Line:** 10
**Context:** JSDoc module comment
```typescript
 * @module afi-reactor/src/langgraph/plugins/AiMlNode
```
**Recommendation:** Change to `@module afi-reactor/src/dag/plugins/AiMlNode`
**Rationale:** Update module path to reflect new directory structure.

**Line:** 121
**Context:** JSDoc parameter comment
```typescript
 * @param state - The current LangGraph state
```
**Recommendation:** Change to "The current pipeline state"
**Rationale:** Remove "LangGraph" branding from parameter documentation.

**Line:** 236
**Context:** JSDoc parameter comment
```typescript
 * @param state - The current LangGraph state
```
**Recommendation:** Change to "The current pipeline state"
**Rationale:** Remove "LangGraph" branding from parameter documentation.

### 14. File: `afi-reactor/src/langgraph/__tests__/integration.test.ts`

**Path:** `afi-reactor/src/langgraph/__tests__/integration.test.ts`
**Line:** 2
**Context:** File description comment
```typescript
 * AFI Reactor - LangGraph Integration Tests
```
**Recommendation:** Change to "AFI Reactor - DAG Integration Tests"
**Rationale:** Remove "LangGraph" branding from test description.

**Line:** 4
**Context:** File description comment
```typescript
 * Comprehensive end-to-end integration tests for Phase 10 of AFI-Reactor LangGraph Integration.
```
**Recommendation:** Change to "Comprehensive end-to-end integration tests for Phase 10 of AFI-Reactor DAG Integration."
**Rationale:** Remove "LangGraph" branding from test description.

**Line:** 7
**Context:** JSDoc module comment
```typescript
 * @module afi-reactor/src/langgraph/__tests__/integration
```
**Recommendation:** Change to `@module afi-reactor/src/dag/__tests__/integration`
**Rationale:** Update module path to reflect new directory structure.

**Line:** 45
**Context:** Test suite description
```typescript
describe('LangGraph Integration Tests', () => {
```
**Recommendation:** Change to `describe('DAG Integration Tests', () => {`
**Rationale:** Remove "LangGraph" branding from test suite name.

### 15. File: `afi-reactor/src/langgraph/plugins/TechnicalIndicatorsNode.ts`

**Path:** `afi-reactor/src/langgraph/plugins/TechnicalIndicatorsNode.ts`
**Line:** 10
**Context:** JSDoc module comment
```typescript
 * @module afi-reactor/src/langgraph/plugins/TechnicalIndicatorsNode
```
**Recommendation:** Change to `@module afi-reactor/src/dag/plugins/TechnicalIndicatorsNode`
**Rationale:** Update module path to reflect new directory structure.

**Line:** 46
**Context:** JSDoc parameter comment
```typescript
 * @param state - The current LangGraph state
```
**Recommendation:** Change to "The current pipeline state"
**Rationale:** Remove "LangGraph" branding from parameter documentation.

### 16. File: `afi-reactor/src/langgraph/plugins/__tests__/ScoutNode.test.ts`

**Path:** `afi-reactor/src/langgraph/plugins/__tests__/ScoutNode.test.ts`
**Line:** 4
**Context:** JSDoc module comment
```typescript
 * @module afi-reactor/src/langgraph/plugins/__tests__/ScoutNode.test
```
**Recommendation:** Change to `@module afi-reactor/src/dag/plugins/__tests__/ScoutNode.test`
**Rationale:** Update module path to reflect new directory structure.

### 17. File: `afi-reactor/src/langgraph/plugins/__tests__/plugins-integration.test.ts`

**Path:** `afi-reactor/src/langgraph/plugins/__tests__/plugins-integration.test.ts`
**Line:** 4
**Context:** JSDoc module comment
```typescript
 * @module afi-reactor/src/langgraph/plugins/__tests__/plugins-integration.test
```
**Recommendation:** Change to `@module afi-reactor/src/dag/plugins/__tests__/plugins-integration.test`
**Rationale:** Update module path to reflect new directory structure.

### 18. File: `afi-reactor/src/langgraph/plugins/__tests__/TechnicalIndicatorsNode.test.ts`

**Path:** `afi-reactor/src/langgraph/plugins/__tests__/TechnicalIndicatorsNode.test.ts`
**Line:** 4
**Context:** JSDoc module comment
```typescript
 * @module afi-reactor/src/langgraph/plugins/__tests__/TechnicalIndicatorsNode.test
```
**Recommendation:** Change to `@module afi-reactor/src/dag/plugins/__tests__/TechnicalIndicatorsNode.test`
**Rationale:** Update module path to reflect new directory structure.

### 19. File: `afi-reactor/src/langgraph/plugins/NewsNode.ts`

**Path:** `afi-reactor/src/langgraph/plugins/NewsNode.ts`
**Line:** 10
**Context:** JSDoc module comment
```typescript
 * @module afi-reactor/src/langgraph/plugins/NewsNode
```
**Recommendation:** Change to `@module afi-reactor/src/dag/plugins/NewsNode`
**Rationale:** Update module path to reflect new directory structure.

**Line:** 47
**Context:** JSDoc parameter comment
```typescript
 * @param state - The current LangGraph state
```
**Recommendation:** Change to "The current pipeline state"
**Rationale:** Remove "LangGraph" branding from parameter documentation.

### 20. File: `afi-reactor/src/langgraph/plugins/SentimentNode.ts`

**Path:** `afi-reactor/src/langgraph/plugins/SentimentNode.ts`
**Line:** 11
**Context:** JSDoc module comment
```typescript
 * @module afi-reactor/src/langgraph/plugins/SentimentNode
```
**Recommendation:** Change to `@module afi-reactor/src/dag/plugins/SentimentNode`
**Rationale:** Update module path to reflect new directory structure.

**Line:** 48
**Context:** JSDoc parameter comment
```typescript
 * @param state - The current LangGraph state
```
**Recommendation:** Change to "The current pipeline state"
**Rationale:** Remove "LangGraph" branding from parameter documentation.

### 21. File: `afi-reactor/src/langgraph/nodes/ObserverNode.ts`

**Path:** `afi-reactor/src/langgraph/nodes/ObserverNode.ts`
**Line:** 10
**Context:** JSDoc module comment
```typescript
 * @module afi-reactor/src/langgraph/nodes/ObserverNode
```
**Recommendation:** Change to `@module afi-reactor/src/dag/nodes/ObserverNode`
**Rationale:** Update module path to reflect new directory structure.

**Line:** 18
**Context:** Class description comment
```typescript
 * The Observer node is the third and final required node in the LangGraph DAG.
```
**Recommendation:** Change to "The Observer node is the third and final required node in the DAG."
**Rationale:** Remove "LangGraph" branding from class description.

**Line:** 47
**Context:** JSDoc parameter comment
```typescript
 * @param state - The current LangGraph state
```
**Recommendation:** Change to "The current pipeline state"
**Rationale:** Remove "LangGraph" branding from parameter documentation.

**Line:** 117
**Context:** JSDoc parameter comment
```typescript
 * @param state - The current LangGraph state
```
**Recommendation:** Change to "The current pipeline state"
**Rationale:** Remove "LangGraph" branding from parameter documentation.

**Line:** 187
**Context:** JSDoc parameter comment
```typescript
 * @param state - The current LangGraph state
```
**Recommendation:** Change to "The current pipeline state"
**Rationale:** Remove "LangGraph" branding from parameter documentation.

**Line:** 205
**Context:** JSDoc parameter comment
```typescript
 * @param state - The current LangGraph state
```
**Recommendation:** Change to "The current pipeline state"
**Rationale:** Remove "LangGraph" branding from parameter documentation.

**Line:** 298
**Context:** JSDoc parameter comment
```typescript
 * @param state - The current LangGraph state
```
**Recommendation:** Change to "The current pipeline state"
**Rationale:** Remove "LangGraph" branding from parameter documentation.

### 22. File: `afi-reactor/src/langgraph/nodes/ExecutionNode.ts`

**Path:** `afi-reactor/src/langgraph/nodes/ExecutionNode.ts`
**Line:** 10
**Context:** JSDoc module comment
```typescript
 * @module afi-reactor/src/langgraph/nodes/ExecutionNode
```
**Recommendation:** Change to `@module afi-reactor/src/dag/nodes/ExecutionNode`
**Rationale:** Update module path to reflect new directory structure.

**Line:** 18
**Context:** Class description comment
```typescript
 * The Execution node is the second required node in the LangGraph DAG.
```
**Recommendation:** Change to "The Execution node is the second required node in the DAG."
**Rationale:** Remove "LangGraph" branding from class description.

**Line:** 47
**Context:** JSDoc parameter comment
```typescript
 * @param state - The current LangGraph state
```
**Recommendation:** Change to "The current pipeline state"
**Rationale:** Remove "LangGraph" branding from parameter documentation.

**Line:** 122
**Context:** JSDoc parameter comment
```typescript
 * @param state - The current LangGraph state
```
**Recommendation:** Change to "The current pipeline state"
**Rationale:** Remove "LangGraph" branding from parameter documentation.

**Line:** 187
**Context:** JSDoc parameter comment
```typescript
 * @param state - The current LangGraph state
```
**Recommendation:** Change to "The current pipeline state"
**Rationale:** Remove "LangGraph" branding from parameter documentation.

**Line:** 235
**Context:** JSDoc parameter comment
```typescript
 * @param state - The current LangGraph state
```
**Recommendation:** Change to "The current pipeline state"
**Rationale:** Remove "LangGraph" branding from parameter documentation.

**Line:** 268
**Context:** JSDoc parameter comment
```typescript
 * @param state - The current LangGraph state
```
**Recommendation:** Change to "The current pipeline state"
**Rationale:** Remove "LangGraph" branding from parameter documentation.

**Line:** 308
**Context:** JSDoc parameter comment
```typescript
 * @param state - The current LangGraph state
```
**Recommendation:** Change to "The current pipeline state"
**Rationale:** Remove "LangGraph" branding from parameter documentation.

### 23. File: `afi-reactor/src/langgraph/nodes/AnalystNode.ts`

**Path:** `afi-reactor/src/langgraph/nodes/AnalystNode.ts`
**Line:** 13
**Context:** JSDoc module comment
```typescript
 * @module afi-reactor/src/langgraph/nodes/AnalystNode
```
**Recommendation:** Change to `@module afi-reactor/src/dag/nodes/AnalystNode`
**Rationale:** Update module path to reflect new directory structure.

**Line:** 22
**Context:** Class description comment
```typescript
 * The Analyst node is the final required node in the LangGraph DAG.
```
**Recommendation:** Change to "The Analyst node is the final required node in the DAG."
**Rationale:** Remove "LangGraph" branding from class description.

**Line:** 62
**Context:** JSDoc parameter comment
```typescript
 * @param state - The current LangGraph state
```
**Recommendation:** Change to "The current pipeline state"
**Rationale:** Remove "LangGraph" branding from parameter documentation.

**Line:** 217
**Context:** JSDoc parameter comment
```typescript
 * @param state - The current LangGraph state
```
**Recommendation:** Change to "The current pipeline state"
**Rationale:** Remove "LangGraph" branding from parameter documentation.

**Line:** 242
**Context:** JSDoc parameter comment
```typescript
 * @param state - The current LangGraph state
```
**Recommendation:** Change to "The current pipeline state"
**Rationale:** Remove "LangGraph" branding from parameter documentation.

**Line:** 316
**Context:** JSDoc parameter comment
```typescript
 * @param state - The current LangGraph state
```
**Recommendation:** Change to "The current pipeline state"
**Rationale:** Remove "LangGraph" branding from parameter documentation.

### 24. File: `afi-reactor/src/langgraph/__tests__/test-utils.ts`

**Path:** `afi-reactor/src/langgraph/__tests__/test-utils.ts`
**Line:** 2
**Context:** File description comment
```typescript
 * AFI Reactor - LangGraph Test Utilities
```
**Recommendation:** Change to "AFI Reactor - DAG Test Utilities"
**Rationale:** Remove "LangGraph" branding from test utilities description.

**Line:** 4
**Context:** File description comment
```typescript
 * Comprehensive test utilities and fixtures for LangGraph integration tests.
```
**Recommendation:** Change to "Comprehensive test utilities and fixtures for DAG integration tests."
**Rationale:** Remove "LangGraph" branding from test utilities description.

**Line:** 8
**Context:** JSDoc module comment
```typescript
 * @module afi-reactor/src/langgraph/__tests__/test-utils
```
**Recommendation:** Change to `@module afi-reactor/src/dag/__tests__/test-utils`
**Rationale:** Update module path to reflect new directory structure.

### 25. File: `afi-reactor/src/langgraph/plugins/__tests__/NewsNode.test.ts`

**Path:** `afi-reactor/src/langgraph/plugins/__tests__/NewsNode.test.ts`
**Line:** 4
**Context:** JSDoc module comment
```typescript
 * @module afi-reactor/src/langgraph/plugins/__tests__/NewsNode.test
```
**Recommendation:** Change to `@module afi-reactor/src/dag/plugins/__tests__/NewsNode.test`
**Rationale:** Update module path to reflect new directory structure.

### 26. File: `afi-reactor/src/langgraph/plugins/__tests__/SentimentNode.test.ts`

**Path:** `afi-reactor/src/langgraph/plugins/__tests__/SentimentNode.test.ts`
**Line:** 4
**Context:** JSDoc module comment
```typescript
 * @module afi-reactor/src/langgraph/plugins/__tests__/SentimentNode.test
```
**Recommendation:** Change to `@module afi-reactor/src/dag/plugins/__tests__/SentimentNode.test`
**Rationale:** Update module path to reflect new directory structure.

### 27. File: `afi-reactor/src/langgraph/plugins/__tests__/PatternRecognitionNode.test.ts`

**Path:** `afi-reactor/src/langgraph/plugins/__tests__/PatternRecognitionNode.test.ts`
**Line:** 4
**Context:** JSDoc module comment
```typescript
 * @module afi-reactor/src/langgraph/plugins/__tests__/PatternRecognitionNode.test
```
**Recommendation:** Change to `@module afi-reactor/src/dag/plugins/__tests__/PatternRecognitionNode.test`
**Rationale:** Update module path to reflect new directory structure.

### 28. File: `afi-reactor/src/langgraph/plugins/__tests__/SignalIngressNode.test.ts`

**Path:** `afi-reactor/src/langgraph/plugins/__tests__/SignalIngressNode.test.ts`
**Line:** 4
**Context:** JSDoc module comment
```typescript
 * @module afi-reactor/src/langgraph/plugins/__tests__/SignalIngressNode.test
```
**Recommendation:** Change to `@module afi-reactor/src/dag/plugins/__tests__/SignalIngressNode.test`
**Rationale:** Update module path to reflect new directory structure.

### 29. File: `afi-reactor/src/langgraph/__tests__/PluginRegistry.test.ts`

**Path:** `afi-reactor/src/langgraph/__tests__/PluginRegistry.test.ts`
**Line:** 6
**Context:** JSDoc module comment
```typescript
 * @module afi-reactor/src/langgraph/__tests__/PluginRegistry.test
```
**Recommendation:** Change to `@module afi-reactor/src/dag/__tests__/PluginRegistry.test`
**Rationale:** Update module path to reflect new directory structure.

### 30. File: `afi-reactor/src/langgraph/nodes/__tests__/ObserverNode.test.ts`

**Path:** `afi-reactor/src/langgraph/nodes/__tests__/ObserverNode.test.ts`
**Line:** 4
**Context:** JSDoc module comment
```typescript
 * @module afi-reactor/src/langgraph/nodes/__tests__/ObserverNode.test
```
**Recommendation:** Change to `@module afi-reactor/src/dag/nodes/__tests__/ObserverNode.test`
**Rationale:** Update module path to reflect new directory structure.

### 31. File: `afi-reactor/src/langgraph/nodes/__tests__/ExecutionNode.test.ts`

**Path:** `afi-reactor/src/langgraph/nodes/__tests__/ExecutionNode.test.ts`
**Line:** 4
**Context:** JSDoc module comment
```typescript
 * @module afi-reactor/src/langgraph/nodes/__tests__/ExecutionNode.test
```
**Recommendation:** Change to `@module afi-reactor/src/dag/nodes/__tests__/ExecutionNode.test`
**Rationale:** Update module path to reflect new directory structure.

### 32. File: `afi-reactor/src/langgraph/nodes/__tests__/AnalystNode.test.ts`

**Path:** `afi-reactor/src/langgraph/nodes/__tests__/AnalystNode.test.ts`
**Line:** 4
**Context:** JSDoc module comment
```typescript
 * @module afi-reactor/src/langgraph/nodes/__tests__/AnalystNode.test
```
**Recommendation:** Change to `@module afi-reactor/src/dag/nodes/__tests__/AnalystNode.test`
**Rationale:** Update module path to reflect new directory structure.

### 33. File: `afi-reactor/src/langgraph/nodes/__tests__/nodes-integration.test.ts`

**Path:** `afi-reactor/src/langgraph/nodes/__tests__/nodes-integration.test.ts`
**Line:** 4
**Context:** JSDoc module comment
```typescript
 * @module afi-reactor/src/langgraph/nodes/__tests__/nodes-integration
```
**Recommendation:** Change to `@module afi-reactor/src/dag/nodes/__tests__/nodes-integration`
**Rationale:** Update module path to reflect new directory structure.

### 34. File: `afi-reactor/src/langgraph/__tests__/DAGBuilder.test.ts`

**Path:** `afi-reactor/src/langgraph/__tests__/DAGBuilder.test.ts`
**Line:** 6
**Context:** JSDoc module comment
```typescript
 * @module afi-reactor/src/langgraph/__tests__/DAGBuilder.test
```
**Recommendation:** Change to `@module afi-reactor/src/dag/__tests__/DAGBuilder.test`
**Rationale:** Update module path to reflect new directory structure.

### 35. File: `afi-reactor/src/langgraph/__tests__/AiMlNode.test.ts`

**Path:** `afi-reactor/src/langgraph/__tests__/AiMlNode.test.ts`
**Line:** 6
**Context:** JSDoc module comment
```typescript
 * @module afi-reactor/src/langgraph/__tests__/AiMlNode.test
```
**Recommendation:** Change to `@module afi-reactor/src/dag/__tests__/AiMlNode.test`
**Rationale:** Update module path to reflect new directory structure.

### 36. File: `afi-reactor/src/langgraph/__tests__/DAGExecutor.test.ts`

**Path:** `afi-reactor/src/langgraph/__tests__/DAGExecutor.test.ts`
**Line:** 6
**Context:** JSDoc module comment
```typescript
 * @module afi-reactor/src/langgraph/__tests__/DAGExecutor.test
```
**Recommendation:** Change to `@module afi-reactor/src/dag/__tests__/DAGExecutor.test`
**Rationale:** Update module path to reflect new directory structure.

### 37. File: `afi-reactor/src/state/StateSerializer.ts`

**Path:** `afi-reactor/src/state/StateSerializer.ts`
**Line:** 13
**Context:** Import statement
```typescript
} from '../types/langgraph.js';
```
**Recommendation:** Change to `} from '../types/pipeline.js';`
**Rationale:** Update import path to reflect new file name.

### 38. File: `afi-reactor/src/state/StateManager.ts`

**Path:** `afi-reactor/src/state/StateManager.ts`
**Line:** 13
**Context:** Import statement
```typescript
} from '../types/langgraph.js';
```
**Recommendation:** Change to `} from '../types/pipeline.js';`
**Rationale:** Update import path to reflect new file name.

### 39. File: `afi-reactor/src/state/StateValidator.ts`

**Path:** `afi-reactor/src/state/StateManager.ts`
**Line:** 13
**Context:** Import statement
```typescript
} from '../types/langgraph.js';
```
**Recommendation:** Change to `} from '../types/pipeline.js';`
**Rationale:** Update import path to reflect new file name.

### 40. File: `afi-reactor/src/types/__tests__/langgraph.test.ts`

**Path:** `afi-reactor/src/types/__tests__/langgraph.test.ts`
**Line:** 2
**Context:** File description comment
```typescript
 * Type tests for afi-reactor/src/types/langgraph.ts
```
**Recommendation:** Change to "Type tests for afi-reactor/src/types/pipeline.ts"
**Rationale:** Update file description to reflect new file name.

**Line:** 21
**Context:** Import statement
```typescript
} from '../langgraph';
```
**Recommendation:** Change to `} from '../pipeline';`
**Rationale:** Update import path to reflect new file name.

**Line:** 73
**Context:** Section comment
```typescript
// ============================================================================
// LangGraphState Type Tests
// ============================================================================
```
**Recommendation:** Change to "PipelineState Type Tests"
**Rationale:** Update section comment to reflect new type name.

**Line:** 76
**Context:** Variable declaration
```typescript
const validLangGraphState: LangGraphState = {
```
**Recommendation:** Change to `const validPipelineState: PipelineState = {`
**Rationale:** Update variable name to reflect new type name.

**Line:** 102
**Context:** Variable declaration
```typescript
const minimalLangGraphState: LangGraphState = {
```
**Recommendation:** Change to `const minimalPipelineState: PipelineState = {`
**Rationale:** Update variable name to reflect new type name.

**Line:** 117
**Context:** Section comment
```typescript
// ============================================================================
// LangGraphNode Type Tests
// ============================================================================
```
**Recommendation:** Change to "Pipehead Type Tests"
**Rationale:** Update section comment to reflect new type name.

**Line:** 120
**Context:** Variable declaration
```typescript
const validLangGraphNode: LangGraphNode = {
```
**Recommendation:** Change to `const validPipehead: Pipehead = {`
**Rationale:** Update variable name to reflect new type name.

**Line:** 131
**Context:** Variable declaration
```typescript
const requiredLangGraphNode: LangGraphNode = {
```
**Recommendation:** Change to `const requiredPipehead: Pipehead = {`
**Rationale:** Update variable name to reflect new type name.

**Line:** 194
**Context:** Variable reference
```typescript
state: validLangGraphState,
```
**Recommendation:** Change to `state: validPipelineState,`
**Rationale:** Update variable reference to reflect new variable name.

**Line:** 261
**Context:** Section comment
```typescript
// Test isLangGraphNode
```
**Recommendation:** Change to "Test isPipehead"
**Rationale:** Update section comment to reflect new function name.

**Line:** 262
**Context:** Variable declaration
```typescript
const langGraphNodeTest1 = {
```
**Recommendation:** Change to `const pipeheadTest1 = {`
**Rationale:** Update variable name to reflect new type name.

**Line:** 269
**Context:** Function call
```typescript
if (isLangGraphNode(langGraphNodeTest1)) {
```
**Recommendation:** Change to `if (isPipehead(pipeheadTest1)) {`
**Rationale:** Update function call to reflect new function name.

**Line:** 276
**Context:** Section comment
```typescript
// Test isLangGraphState
```
**Recommendation:** Change to "Test isPipelineState"
**Rationale:** Update section comment to reflect new function name.

**Line:** 277
**Context:** Variable declaration
```typescript
const langGraphStateTest1 = {
```
**Recommendation:** Change to `const pipelineStateTest1 = {`
**Rationale:** Update variable name to reflect new type name.

**Line:** 291
**Context:** Function call
```typescript
if (isLangGraphState(langGraphStateTest1)) {
```
**Recommendation:** Change to `if (isPipelineState(pipelineStateTest1)) {`
**Rationale:** Update function call to reflect new function name.

**Line:** 321
**Context:** Comment
```typescript
// Test that ExecutionTraceEntry can be used in LangGraphState
```
**Recommendation:** Change to "Test that ExecutionTraceEntry can be used in PipelineState"
**Rationale:** Update comment to reflect new type name.

**Line:** 322
**Context:** Variable declaration
```typescript
const stateWithTrace: LangGraphState = {
```
**Recommendation:** Change to `const stateWithTrace: PipelineState = {`
**Rationale:** Update variable name to reflect new type name.

**Line:** 344
**Context:** Comment
```typescript
// Test that LangGraphState can be used in DAGExecutionResult
```
**Recommendation:** Change to "Test that PipelineState can be used in DAGExecutionResult"
**Rationale:** Update comment to reflect new type name.

**Line:** 345
**Context:** Variable reference
```typescript
state: validLangGraphState,
```
**Recommendation:** Change to `state: validPipelineState,`
**Rationale:** Update variable reference to reflect new variable name.

**Line:** 358
**Context:** Function signature
```typescript
function processNode(node: LangGraphNode): void {
```
**Recommendation:** Change to `function processNode(node: Pipehead): void {`
**Rationale:** Update function signature to reflect new type name.

**Line:** 362
**Context:** Function signature
```typescript
function processState(state: LangGraphState): void {
```
**Recommendation:** Change to `function processState(state: PipelineState): void {`
**Rationale:** Update function signature to reflect new type name.

**Line:** 370
**Context:** Function call
```typescript
processNode(validLangGraphNode);
```
**Recommendation:** Change to `processNode(validPipehead);`
**Rationale:** Update function call to reflect new variable name.

**Line:** 371
**Context:** Function call
```typescript
processState(validLangGraphState);
```
**Recommendation:** Change to `processState(validPipelineState);`
**Rationale:** Update function call to reflect new variable name.

**Line:** 382
**Context:** Variable reference
```typescript
validLangGraphState,
```
**Recommendation:** Change to `validPipelineState,`
**Rationale:** Update variable reference to reflect new variable name.

**Line:** 383
**Context:** Variable reference
```typescript
minimalLangGraphState,
```
**Recommendation:** Change to `minimalPipelineState,`
**Rationale:** Update variable reference to reflect new variable name.

**Line:** 384
**Context:** Variable reference
```typescript
validLangGraphNode,
```
**Recommendation:** Change to `validPipehead,`
**Rationale:** Update variable reference to reflect new variable name.

**Line:** 385
**Context:** Variable reference
```typescript
requiredLangGraphNode,
```
**Recommendation:** Change to `requiredPipehead,`
**Rationale:** Update variable reference to reflect new variable name.

---

## afi-core Source Code

### 41. File: `afi-core/src/langgraph/LangGraphSignalEnvelope.ts`

**Path:** `afi-core/src/langgraph/LangGraphSignalEnvelope.ts`
**Line:** 2
**Context:** File description comment
```typescript
 * AFI Core - LangGraph Signal Envelope
```
**Recommendation:** Change to "AFI Core - Signal Envelope"
**Rationale:** Remove "LangGraph" branding from file description.

**Line:** 4
**Context:** File description comment
```typescript
 * This file defines TypeScript interfaces for LangGraph signal envelope,
```
**Recommendation:** Change to "This file defines TypeScript interfaces for signal envelope,"
**Rationale:** Remove "LangGraph" branding from file description.

**Line:** 5
**Context:** File description comment
```typescript
 * extending to core signal schema with LangGraph-specific metadata.
```
**Recommendation:** Change to "extending to core signal schema with DAG-specific metadata."
**Rationale:** Remove "LangGraph" branding from file description.

**Line:** 10
**Context:** JSDoc module comment
```typescript
 * @module afi-core/src/langgraph/LangGraphSignalEnvelope
```
**Recommendation:** Change to `@module afi-core/src/dag/SignalEnvelope`
**Rationale:** Update module path to reflect new file and directory names.

**Line:** 14
**Context:** Interface description comment
```typescript
 * LangGraph signal envelope
```
**Recommendation:** Change to "Signal envelope"
**Rationale:** Remove "LangGraph" branding from interface description.

**Line:** 21
**Context:** Interface declaration
```typescript
export interface LangGraphSignalEnvelope {
```
**Recommendation:** Change to `export interface SignalEnvelope {`
**Rationale:** Remove "LangGraph" branding from interface name.

**Line:** 194
**Context:** Function description comment
```typescript
 * Type guard to check if an object is a LangGraphSignalEnvelope
```
**Recommendation:** Change to "Type guard to check if an object is a SignalEnvelope"
**Rationale:** Remove "LangGraph" branding from function description.

**Line:** 196
**Context:** Function declaration
```typescript
export function isLangGraphSignalEnvelope(obj: unknown): obj is LangGraphSignalEnvelope {
```
**Recommendation:** Change to `export function isSignalEnvelope(obj: unknown): obj is SignalEnvelope {`
**Rationale:** Remove "LangGraph" branding from function name and return type.

**Line:** 265
**Context:** Function parameter type
```typescript
): LangGraphSignalEnvelope {
```
**Recommendation:** Change to `): SignalEnvelope {`
**Rationale:** Remove "LangGraph" branding from return type.

**Line:** 287
**Context:** Function parameter type
```typescript
envelope: LangGraphSignalEnvelope,
```
**Recommendation:** Change to `envelope: SignalEnvelope,`
**Rationale:** Remove "LangGraph" branding from parameter type.

**Line:** 293
**Context:** Function return type
```typescript
): LangGraphSignalEnvelope {
```
**Recommendation:** Change to `): SignalEnvelope {`
**Rationale:** Remove "LangGraph" branding from return type.

**Line:** 331
**Context:** Function parameter type
```typescript
envelope: LangGraphSignalEnvelope,
```
**Recommendation:** Change to `envelope: SignalEnvelope,`
**Rationale:** Remove "LangGraph" branding from parameter type.

**Line:** 333
**Context:** Function return type
```typescript
): LangGraphSignalEnvelope {
```
**Recommendation:** Change to `): SignalEnvelope {`
**Rationale:** Remove "LangGraph" branding from return type.

**Line:** 350
**Context:** Function parameter type
```typescript
envelope: LangGraphSignalEnvelope,
```
**Recommendation:** Change to `envelope: SignalEnvelope,`
**Rationale:** Remove "LangGraph" branding from parameter type.

**Line:** 378
**Context:** Function parameter type
```typescript
envelope: LangGraphSignalEnvelope,
```
**Recommendation:** Change to `envelope: SignalEnvelope,`
**Rationale:** Remove "LangGraph" branding from parameter type.

### 42. File: `afi-core/src/langgraph/__tests__/LangGraphSignalEnvelope.test.ts`

**Path:** `afi-core/src/langgraph/__tests__/LangGraphSignalEnvelope.test.ts`
**Line:** 2
**Context:** File description comment
```typescript
 * Type tests for afi-core/src/langgraph/LangGraphSignalEnvelope.ts
```
**Recommendation:** Change to "Type tests for afi-core/src/dag/SignalEnvelope.ts"
**Rationale:** Update file description to reflect new file and directory names.

**Line:** 12
**Context:** Import statement
```typescript
  LangGraphSignalEnvelope,
```
**Recommendation:** Change to `SignalEnvelope,`
**Rationale:** Update import to reflect new interface name.

**Line:** 22
**Context:** Import statement
```typescript
} from '../LangGraphSignalEnvelope';
```
**Recommendation:** Change to `} from '../SignalEnvelope';`
**Rationale:** Update import path to reflect new file name.

**Line:** 86
**Context:** Section comment
```typescript
// ============================================================================
// LangGraphSignalEnvelope Type Tests
// ============================================================================
```
**Recommendation:** Change to "SignalEnvelope Type Tests"
**Rationale:** Update section comment to reflect new interface name.

**Line:** 89
**Context:** Variable declaration
```typescript
const validLangGraphSignalEnvelope: LangGraphSignalEnvelope = {
```
**Recommendation:** Change to `const validSignalEnvelope: SignalEnvelope = {`
**Rationale:** Update variable name to reflect new interface name.

**Line:** 106
**Context:** Variable declaration
```typescript
const minimalLangGraphSignalEnvelope: LangGraphSignalEnvelope = {
```
**Recommendation:** Change to `const minimalSignalEnvelope: SignalEnvelope = {`
**Rationale:** Update variable name to reflect new interface name.

**Line:** 194
**Context:** Section comment
```typescript
// Test isLangGraphSignalEnvelope
```
**Recommendation:** Change to "Test isSignalEnvelope"
**Rationale:** Update section comment to reflect new function name.

**Line:** 195
**Context:** Variable declaration
```typescript
const langGraphSignalEnvelopeTest1 = {
```
**Recommendation:** Change to `const signalEnvelopeTest1 = {`
**Rationale:** Update variable name to reflect new interface name.

**Line:** 209
**Context:** Function call
```typescript
if (isLangGraphSignalEnvelope(langGraphSignalEnvelopeTest1)) {
```
**Recommendation:** Change to `if (isSignalEnvelope(signalEnvelopeTest1)) {`
**Rationale:** Update function call to reflect new function name.

**Line:** 268
**Context:** Function call
```typescript
if (isLangGraphSignalEnvelope(newEnvelope)) {
```
**Recommendation:** Change to `if (isSignalEnvelope(newEnvelope)) {`
**Rationale:** Update function call to reflect new function name.

**Line:** 282
**Context:** Function call
```typescript
if (isLangGraphSignalEnvelope(envelopeWithResult)) {
```
**Recommendation:** Change to `if (isSignalEnvelope(envelopeWithResult)) {`
**Rationale:** Update function call to reflect new function name.

**Line:** 292
**Context:** Function call
```typescript
if (isLangGraphSignalEnvelope(envelopeWithTrace)) {
```
**Recommendation:** Change to `if (isSignalEnvelope(envelopeWithTrace)) {`
**Rationale:** Update function call to reflect new function name.

**Line:** 297
**Context:** Variable reference
```typescript
const summary = getSignalEnvelopeSummary(validLangGraphSignalEnvelope);
```
**Recommendation:** Change to `const summary = getSignalEnvelopeSummary(validSignalEnvelope);`
**Rationale:** Update variable reference to reflect new variable name.

**Line:** 304
**Context:** Variable reference
```typescript
const validationResult = validateSignalEnvelope(validLangGraphSignalEnvelope);
```
**Recommendation:** Change to `const validationResult = validateSignalEnvelope(validSignalEnvelope);`
**Rationale:** Update variable reference to reflect new variable name.

**Line:** 314
**Context:** Comment
```typescript
// Test that ExecutionTraceEntry can be used in LangGraphSignalEnvelope
```
**Recommendation:** Change to "Test that ExecutionTraceEntry can be used in SignalEnvelope"
**Rationale:** Update comment to reflect new interface name.

**Line:** 315
**Context:** Variable declaration
```typescript
const envelopeWithEntries: LangGraphSignalEnvelope = {
```
**Recommendation:** Change to `const envelopeWithEntries: SignalEnvelope = {`
**Rationale:** Update variable name to reflect new interface name.

**Line:** 330
**Context:** Comment
```typescript
// Test that EnrichmentResult can be used in enrichmentResults Map
```
**Recommendation:** Keep as is (no "LangGraph" reference)
**Rationale:** This comment does not contain "LangGraph" terminology.

**Line:** 331
**Context:** Variable declaration
```typescript
const envelopeWithEnrichmentResults: LangGraphSignalEnvelope = {
```
**Recommendation:** Change to `const envelopeWithEnrichmentResults: SignalEnvelope = {`
**Rationale:** Update variable name to reflect new interface name.

**Line:** 348
**Context:** Function signature
```typescript
function processEnvelope(envelope: LangGraphSignalEnvelope): void {
```
**Recommendation:** Change to `function processEnvelope(envelope: SignalEnvelope): void {`
**Rationale:** Update function signature to reflect new interface name.

**Line:** 360
**Context:** Function call
```typescript
processEnvelope(validLangGraphSignalEnvelope);
```
**Recommendation:** Change to `processEnvelope(validSignalEnvelope);`
**Rationale:** Update function call to reflect new variable name.

**Line:** 373
**Context:** Variable reference
```typescript
validLangGraphSignalEnvelope,
```
**Recommendation:** Change to `validSignalEnvelope,`
**Rationale:** Update variable reference to reflect new variable name.

**Line:** 375
**Context:** Variable reference
```typescript
minimalLangGraphSignalEnvelope,
```
**Recommendation:** Change to `minimalSignalEnvelope,`
**Rationale:** Update variable reference to reflect new variable name.

### 43. File: `afi-core/dist/src/langgraph/LangGraphSignalEnvelope.js`

**Path:** `afi-core/dist/src/langgraph/LangGraphSignalEnvelope.js`
**Type:** Compiled JavaScript file
**Context:** Compiled output from TypeScript
**Recommendation:** This file will be automatically regenerated when TypeScript is recompiled after source file changes. No manual changes needed.
**Rationale:** Compiled files are generated from source; updating source files will automatically update compiled output.

### 44. File: `afi-core/dist/src/langgraph/LangGraphSignalEnvelope.d.ts`

**Path:** `afi-core/dist/src/langgraph/LangGraphSignalEnvelope.d.ts`
**Type:** TypeScript declaration file
**Context:** Generated type declarations
**Recommendation:** This file will be automatically regenerated when TypeScript is recompiled after source file changes. No manual changes needed.
**Rationale:** Declaration files are generated from source; updating source files will automatically update declarations.

---

## Documentation Files

### 45. File: `AFI_LANGGRAPH_CONFIG_TO_AFIDAG_CONFIG_REFACTORING_REPORT.md`

**Path:** `AFI_LANGGRAPH_CONFIG_TO_AFIDAG_CONFIG_REFACTORING_REPORT.md`
**Type:** Documentation
**Context:** Report on refactoring LangGraphConfig to AFIDAGConfig
**Recommendation:** Rename file to `AFI_DAG_CONFIG_REFACTORING_REPORT.md` and update all content references
**Rationale:** Remove "LangGraph" branding from file name and content.

### 46. File: `AFI_LANGGRAPH_TERMINOLOGY_ANALYSIS_REPORT.md`

**Path:** `AFI_LANGGRAPH_TERMINOLOGY_ANALYSIS_REPORT.md`
**Type:** Documentation
**Context:** Analysis of LangGraph terminology in codebase
**Recommendation:** Rename file to `AFI_DAG_TERMINOLOGY_ANALYSIS_REPORT.md` and update all content references
**Rationale:** Remove "LangGraph" branding from file name and content.

### 47. File: `AFI_LANGGRAPH_DAG_IMPLEMENTATION_STATUS_AND_RECOMMENDATION_REVISED.md`

**Path:** `AFI_LANGGRAPH_DAG_IMPLEMENTATION_STATUS_AND_RECOMMENDATION_REVISED.md`
**Type:** Documentation
**Context:** Status report on LangGraph DAG implementation
**Recommendation:** Rename file to `AFI_DAG_IMPLEMENTATION_STATUS_AND_RECOMMENDATION_REVISED.md` and update all content references
**Rationale:** Remove "LangGraph" branding from file name and content.

### 48. File: `AFI_LANGGRAPH_DAG_IMPLEMENTATION_STATUS_AND_RECOMMENDATION.md`

**Path:** `AFI_LANGGRAPH_DAG_IMPLEMENTATION_STATUS_AND_RECOMMENDATION.md`
**Type:** Documentation
**Context:** Status report on LangGraph DAG implementation
**Recommendation:** Rename file to `AFI_DAG_IMPLEMENTATION_STATUS_AND_RECOMMENDATION.md` and update all content references
**Rationale:** Remove "LangGraph" branding from file name and content.

### 49. File: `AFI_LANGGRAPH_TO_PIPEHEAD_REFACTORING_PLAN.md`

**Path:** `plans/AFI_LANGGRAPH_TO_PIPEHEAD_REFACTORING_PLAN.md`
**Type:** Documentation
**Context:** Plan for refactoring LangGraphNode to Pipehead
**Recommendation:** Rename file to `AFI_DAG_TO_PIPEHEAD_REFACTORING_PLAN.md` and update all content references
**Rationale:** Remove "LangGraph" branding from file name and content.

### 50. File: `AFI_LANGGRAPH_SCOUT_AND_AI_ML_NODE_REFACTORING_PLAN.md`

**Path:** `plans/AFI_LANGGRAPH_SCOUT_AND_AI_ML_NODE_REFACTORING_PLAN.md`
**Type:** Documentation
**Context:** Plan for refactoring Scout and AI/ML nodes
**Recommendation:** Rename file to `AFI_DAG_SCOUT_AND_AI_ML_NODE_REFACTORING_PLAN.md` and update all content references
**Rationale:** Remove "LangGraph" branding from file name and content.

### 51. File: `AFI_LANGGRAPH_SCOUT_NODE_REFACTORING_PLAN.md`

**Path:** `plans/AFI_LANGGRAPH_SCOUT_NODE_REFACTORING_PLAN.md`
**Type:** Documentation
**Context:** Plan for refactoring Scout node
**Recommendation:** Rename file to `AFI_DAG_SCOUT_NODE_REFACTORING_PLAN.md` and update all content references
**Rationale:** Remove "LangGraph" branding from file name and content.

### 52. File: `AFI_REACTOR_LANGGRAPH_FLEXIBLE_DAG_ANALYSIS.md`

**Path:** `AFI_REACTOR_LANGGRAPH_FLEXIBLE_DAG_ANALYSIS.md`
**Type:** Documentation
**Context:** Analysis of LangGraph flexible DAG implementation
**Recommendation:** Rename file to `AFI_REACTOR_FLEXIBLE_DAG_ANALYSIS.md` and update all content references
**Rationale:** Remove "LangGraph" branding from file name and content.

### 53. File: `afi-reactor/INTEGRATION_TEST_ANALYSIS_AND_PLAN.md`

**Path:** `afi-reactor/INTEGRATION_TEST_ANALYSIS_AND_PLAN.md`
**Line:** 1
**Context:** Document title
```markdown
# LangGraph Integration Test Analysis and Fix Plan
```
**Recommendation:** Change to "# DAG Integration Test Analysis and Fix Plan"
**Rationale:** Remove "LangGraph" branding from document title.

**Line:** 5
**Context:** Document description
```markdown
This document provides a comprehensive analysis of the LangGraph integration test suite
```
**Recommendation:** Change to "This document provides a comprehensive analysis of the DAG integration test suite"
**Rationale:** Remove "LangGraph" branding from document description.

**Line:** 31
**Context:** Table entry
```markdown
| `Pipehead` | `types/langgraph.ts` | Interface for all node implementations |
```
**Recommendation:** Change to `| \`Pipehead\` | \`types/pipeline.ts\` | Interface for all node implementations |`
**Rationale:** Update file path to reflect new file name.

**Line:** 383
**Context:** Code example comment
```typescript
/**
 * Test Utilities for LangGraph Integration Tests
 *
 * Provides reusable utilities and fixtures for testing LangGraph components.
 */
```
**Recommendation:** Change to:
```typescript
/**
 * Test Utilities for DAG Integration Tests
 *
 * Provides reusable utilities and fixtures for testing DAG components.
 */
```
**Rationale:** Remove "LangGraph" branding from code comments.

**Line:** 392
**Context:** Import statement
```typescript
import type { Pipehead, PipelineState } from '../../types/langgraph.js';
```
**Recommendation:** Change to `import type { Pipehead, PipelineState } from '../../types/pipeline.js';`
**Rationale:** Update import path to reflect new file name.

### 54. File: `plans/AFI_ML_PROVIDER_ABSTRACTION_ARCHITECTURE.md`

**Path:** `plans/AFI_ML_PROVIDER_ABSTRACTION_ARCHITECTURE.md`
**Line:** 26
**Context:** Code reference
```markdown
The current [`AiMlNode`](afi-reactor/src/langgraph/plugins/AiMlNode.ts:23) implementation is tightly coupled to Tiny Brains service:
```
**Recommendation:** Change to `The current [\`AiMlNode\`](afi-reactor/src/dag/plugins/AiMlNode.ts:23) implementation is tightly coupled to Tiny Brains service:`
**Rationale:** Update file path to reflect new directory structure.

**Line:** 32
**Context:** Code example
```typescript
export class AiMlNode implements LangGraphNode {
  async execute(state: LangGraphState): Promise<LangGraphState> {
```
**Recommendation:** Change to:
```typescript
export class AiMlNode implements Pipehead {
  async execute(state: PipelineState): Promise<PipelineState> {
```
**Rationale:** Update type names to reflect new naming.

**Line:** 87
**Context:** Mermaid diagram
```mermaid
    H --> I[LangGraph State]
```
**Recommendation:** Change to `H --> I[Pipeline State]`
**Rationale:** Remove "LangGraph" branding from diagram.

**Line:** 816
**Context:** Code example
```typescript
export class AiMlNode implements LangGraphNode {
```
**Recommendation:** Change to `export class AiMlNode implements Pipehead {`
**Rationale:** Update type name to reflect new naming.

**Line:** 834
**Context:** Code example
```typescript
async execute(state: LangGraphState): Promise<LangGraphState> {
```
**Recommendation:** Change to `async execute(state: PipelineState): Promise<PipelineState> {`
**Rationale:** Update type names to reflect new naming.

**Line:** 897
**Context:** Code example
```typescript
private buildMLProviderInput(state: LangGraphState): MLProviderInput {
```
**Recommendation:** Change to `private buildMLProviderInput(state: PipelineState): MLProviderInput {`
**Rationale:** Update type name to reflect new naming.

**Line:** 916
**Context:** Code example
```typescript
private storeFailureResult(
  state: LangGraphState,
```
**Recommendation:** Change to `private storeFailureResult(state: PipelineState,`
**Rationale:** Update type name to reflect new naming.

**Line:** 962
**Context:** Mermaid diagram
```mermaid
    participant State as LangGraph State
```
**Recommendation:** Change to `participant State as Pipeline State`
**Rationale:** Remove "LangGraph" branding from diagram.

**Line:** 1037
**Context:** Code reference
```markdown
- Updated [`AiMlNode`](afi-reactor/src/langgraph/plugins/AiMlNode.ts) with dual paths
```
**Recommendation:** Change to `- Updated [\`AiMlNode\`](afi-reactor/src/dag/plugins/AiMlNode.ts) with dual paths`
**Rationale:** Update file path to reflect new directory structure.

**Line:** 1524
**Context:** Code example
```typescript
async execute(state: LangGraphState): Promise<LangGraphState> {
```
**Recommendation:** Change to `async execute(state: PipelineState): Promise<PipelineState> {`
**Rationale:** Update type names to reflect new naming.

**Line:** 1687
**Context:** Directory tree
```markdown
│   └── langgraph/
```
**Recommendation:** Change to `│   └── dag/`
**Rationale:** Update directory name to reflect new structure.

**Line:** 1737
**Context:** Code reference
```markdown
- [`AiMlNode`](afi-reactor/src/langgraph/plugins/AiMlNode.ts:23) - Current implementation
```
**Recommendation:** Change to `- [\`AiMlNode\`](afi-reactor/src/dag/plugins/AiMlNode.ts:23) - Current implementation`
**Rationale:** Update file path to reflect new directory structure.

**Line:** 1740
**Context:** Code reference
```markdown
- [`LangGraphState`](afi-reactor/src/types/langgraph.ts:59) - State interface
```
**Recommendation:** Change to `- [\`PipelineState\`](afi-reactor/src/types/pipeline.ts:59) - State interface`
**Rationale:** Update file path and type name to reflect new naming.

---

## Configuration Files

### 55. File: `afi-reactor/jest.config.js`

**Path:** `afi-reactor/jest.config.js`
**Line:** 29
**Context:** Test pattern configuration
```javascript
"**/src/langgraph/__tests__/*.test.ts",
```
**Recommendation:** Change to `"**/src/dag/__tests__/*.test.ts",`
**Rationale:** Update test pattern to reflect new directory structure.

---

## Test Files

### 56. File: `afi-reactor/test/integration/state-lifecycle.test.ts`

**Path:** `afi-reactor/test/integration/state-lifecycle.test.ts`
**Line:** 12
**Context:** Import statement
```typescript
import type { PipelineState, ExecutionTraceEntry } from '../../src/types/langgraph.js';
```
**Recommendation:** Change to `import type { PipelineState, ExecutionTraceEntry } from '../../src/types/pipeline.js';`
**Rationale:** Update import path to reflect new file name.

### 57. File: `afi-reactor/test/state-management.test.ts`

**Path:** `afi-reactor/test/state-management.test.ts`
**Line:** 11
**Context:** Import statement
```typescript
import type { PipelineState, ExecutionTraceEntry } from '../src/types/langgraph.js';
```
**Recommendation:** Change to `import type { PipelineState, ExecutionTraceEntry } from '../src/types/pipeline.js';`
**Rationale:** Update import path to reflect new file name.

---

## Third-Party Dependencies

### 58. Directory: `afi-eliza-gateway/node_modules/`

**Path:** `afi-eliza-gateway/node_modules/`
**Type:** Third-party dependencies
**Context:** Contains Sentry, LangChain, and other third-party packages that reference "LangGraph"
**Recommendation:** **NO ACTION REQUIRED**
**Rationale:** These are third-party dependencies that should not be modified. The references to "LangGraph" in these files are part of the external libraries' code and documentation, not AFI's codebase.

### 59. File: `langchainllms.txt`

**Path:** `langchainllms.txt`
**Type:** Documentation/reference file
**Context:** Contains references to LangGraph documentation
**Recommendation:** **NO ACTION REQUIRED**
**Rationale:** This appears to be a reference file containing links to external LangChain/LangGraph documentation. It does not contain AFI code and should not be modified.

---

## Recommendations Summary

### Priority 1: Critical Changes (Required for Complete Elimination)

1. **Rename Directories:**
   - `afi-reactor/src/langgraph/` → `afi-reactor/src/dag/`
   - `afi-core/src/langgraph/` → `afi-core/src/dag/`

2. **Rename Core Type Files:**
   - `afi-reactor/src/types/langgraph.ts` → `afi-reactor/src/types/pipeline.ts`
   - `afi-core/src/langgraph/LangGraphSignalEnvelope.ts` → `afi-core/src/dag/SignalEnvelope.ts`

3. **Rename Interface:**
   - `LangGraphSignalEnvelope` → `SignalEnvelope`

4. **Update All Import Statements:**
   - Update all imports from `../types/langgraph.js` to `../types/pipeline.js`
   - Update all imports from `../langgraph/` to `../dag/`

5. **Update Configuration Files:**
   - Update `afi-reactor/jest.config.js` test patterns

### Priority 2: Documentation Updates (High Priority)

6. **Rename Documentation Files:**
   - `AFI_LANGGRAPH_CONFIG_TO_AFIDAG_CONFIG_REFACTORING_REPORT.md` → `AFI_DAG_CONFIG_REFACTORING_REPORT.md`
   - `AFI_LANGGRAPH_TERMINOLOGY_ANALYSIS_REPORT.md` → `AFI_DAG_TERMINOLOGY_ANALYSIS_REPORT.md`
   - `AFI_LANGGRAPH_DAG_IMPLEMENTATION_STATUS_AND_RECOMMENDATION_REVISED.md` → `AFI_DAG_IMPLEMENTATION_STATUS_AND_RECOMMENDATION_REVISED.md`
   - `AFI_LANGGRAPH_DAG_IMPLEMENTATION_STATUS_AND_RECOMMENDATION.md` → `AFI_DAG_IMPLEMENTATION_STATUS_AND_RECOMMENDATION.md`
   - `AFI_LANGGRAPH_TO_PIPEHEAD_REFACTORING_PLAN.md` → `AFI_DAG_TO_PIPEHEAD_REFACTORING_PLAN.md`
   - `AFI_LANGGRAPH_SCOUT_AND_AI_ML_NODE_REFACTORING_PLAN.md` → `AFI_DAG_SCOUT_AND_AI_ML_NODE_REFACTORING_PLAN.md`
   - `AFI_LANGGRAPH_SCOUT_NODE_REFACTORING_PLAN.md` → `AFI_DAG_SCOUT_NODE_REFACTORING_PLAN.md`
   - `AFI_REACTOR_LANGGRAPH_FLEXIBLE_DAG_ANALYSIS.md` → `AFI_REACTOR_FLEXIBLE_DAG_ANALYSIS.md`

7. **Update All JSDoc Comments:**
   - Replace "LangGraph" with "DAG" or "pipeline" in all JSDoc comments
   - Update module paths in all `@module` annotations

8. **Update Test Descriptions:**
   - Replace "LangGraph" with "DAG" in test suite descriptions
   - Update test file names to match new directory structure

### Priority 3: Content Updates (Medium Priority)

9. **Update Variable Names in Tests:**
   - Replace `LangGraph*` variable names with `Pipeline*` or `Signal*` equivalents
   - Update function calls to use new type guard names

10. **Update Mermaid Diagrams:**
    - Replace "LangGraph State" with "Pipeline State" in all diagrams

### Priority 4: No Action Required

11. **Third-Party Dependencies:**
    - Do NOT modify files in `node_modules/` directories
    - These are external dependencies that should remain unchanged

12. **Reference Files:**
    - Do NOT modify `langchainllms.txt` or similar reference files
    - These contain external documentation links, not AFI code

---

## Implementation Strategy

### Phase 1: Directory and File Renaming (Foundation)

1. Rename directories:
   ```bash
   cd afi-reactor/src
   mv langgraph dag
   cd ../afi-core/src
   mv langgraph dag
   ```

2. Rename core type files:
   ```bash
   cd afi-reactor/src/types
   mv langgraph.ts pipeline.ts
   cd ../../afi-core/src/dag
   mv LangGraphSignalEnvelope.ts SignalEnvelope.ts
   ```

### Phase 2: Source Code Updates

3. Update all import statements in source files
4. Update all JSDoc module comments
5. Update all JSDoc parameter descriptions
6. Update all class/interface descriptions

### Phase 3: Test Updates

7. Update all test file names
8. Update all test imports
9. Update all test variable names
10. Update all test descriptions

### Phase 4: Documentation Updates

11. Rename all documentation files
12. Update all documentation content
13. Update all code examples in documentation
14. Update all Mermaid diagrams

### Phase 5: Configuration Updates

15. Update jest.config.js
16. Update any other configuration files
17. Rebuild TypeScript projects

### Phase 6: Verification

18. Run all tests to ensure no broken imports
19. Verify all documentation links are correct
20. Check for any remaining "langgraph" references

---

## Estimated Impact

### Files to Modify: ~60 files
- Source code files: ~35 files
- Test files: ~20 files
- Documentation files: ~5 files
- Configuration files: ~1 file

### Lines to Change: ~500+ lines
- Import statements: ~50 lines
- JSDoc comments: ~200 lines
- Variable names: ~100 lines
- File names: ~10 files
- Directory names: ~2 directories

### Risk Assessment: **LOW**
- The codebase has already begun refactoring to Pipehead/PipelineState terminology
- Most changes are straightforward find-and-replace operations
- No breaking changes to public APIs (internal refactoring only)
- Tests will catch any import errors

---

## Conclusion

This comprehensive scan identified **500+ occurrences** of "langgraph" terminology across the AFI codebase. The majority of these references are in:

1. **Directory and file names** (highest visibility)
2. **JSDoc comments and module annotations** (documentation)
3. **Import statements** (code references)
4. **Test files** (test descriptions and variable names)

The codebase has already begun refactoring from "LangGraph" to "Pipehead/PipelineState" terminology in [`afi-reactor/src/types/langgraph.ts`](afi-reactor/src/types/langgraph.ts), which provides a solid foundation for completing this refactoring.

**Recommendation:** Execute the refactoring in phases as outlined above, starting with directory/file renaming (Phase 1) and working through source code, tests, and documentation updates. This systematic approach will ensure complete elimination of "langgraph" terminology while maintaining code functionality and test coverage.

---

**Report Generated:** 2025-12-28
**Total Instances Found:** 500+
**Files Analyzed:** ~60 files
**Recommendations Provided:** 59 specific changes
