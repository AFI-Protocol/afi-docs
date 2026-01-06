# AFI LangGraphNode to Pipehead Refactoring Plan

**Date:** 2025-12-28
**Status:** Planning Phase
**Scope:** afi-reactor repository (21 files affected)

---

## Executive Summary

This plan outlines the comprehensive refactoring of the `LangGraphNode` interface to `Pipehead` across the AFI Reactor codebase. This refactoring removes misleading "LangGraph" branding, establishes a unique AFI brand identity with playful naming, and improves code clarity and maintainability.

**Key Changes:**
- Rename `LangGraphNode` → `Pipehead`
- Rename `LangGraphState` → `PipelineState`
- Rename `DAGPluginConfig` → `PipeheadConfig`
- Create `BasePipehead` abstract base class
- Introduce `PipeheadMetadata` interface

**Migration Strategy:** Global rename operation (no backward compatibility constraints - solo MVP)

---

## 1. Refactoring Overview

### 1.1 Naming Convention Changes

| Old Term | New Term | Rationale |
|----------|----------|-----------|
| `LangGraphNode` | `Pipehead` | Memorable, playful, evokes pipeline leadership |
| `LangGraphState` | `PipelineState` | Removes LangGraph branding, describes pipeline execution context |
| `DAGPluginConfig` | `PipeheadConfig` | Consistent naming with playful touch |
| `isLangGraphNode` | `isPipehead` | Type guard follows new naming |
| `isLangGraphState` | `isPipelineState` | Type guard follows new naming |

### 1.2 New Interfaces and Classes

#### BasePipehead Abstract Class
Provides common implementation for trace entry creation and error handling across all pipehead implementations.

#### PipeheadMetadata Interface
Separates pipehead metadata from execution logic, enabling better plugin discovery and documentation.

#### PipeheadConfig Interface
Defines static configuration of a pipehead without execution logic, enabling configuration validation before execution.

---

## 2. File-by-File Changes

### 2.1 Type Definition File

**File:** `afi-reactor/src/types/langgraph.ts`

**Changes:**
1. Rename `LangGraphNode` interface to `Pipehead` (lines 33-51)
2. Rename `LangGraphState` interface to `PipelineState` (lines 59-86)
3. Rename `isLangGraphNode` function to `isPipehead` (lines 248-261)
4. Rename `isLangGraphState` function to `isPipelineState` (lines 266-285)
5. Update all references to `LangGraphNode` in type annotations
6. Update all references to `LangGraphState` in type annotations
7. Update JSDoc comments to reflect new naming
8. Add `BasePipehead` abstract class definition
9. Add `PipeheadMetadata` interface definition
10. Add `PipeheadConfig` interface definition

**New Code to Add:**

```typescript
/**
 * Pipehead metadata interface
 *
 * Provides additional information about a pipehead.
 */
export interface PipeheadMetadata {
  /** Pipehead ID */
  id: string;

  /** Pipehead type */
  type: 'required' | 'enrichment' | 'ingress';

  /** Pipehead version */
  version: string;

  /** Pipehead name */
  name: string;

  /** Pipehead description */
  description: string;

  /** Pipehead author */
  author?: string;

  /** Pipehead tags for categorization */
  tags?: string[];

  /** Whether the pipehead is deprecated */
  deprecated?: boolean;

  /** Minimum required AFI version */
  minAfiVersion?: string;

  /** Maximum compatible AFI version */
  maxAfiVersion?: string;
}

/**
 * Pipehead configuration interface
 *
 * Defines the static configuration of a pipehead without execution logic.
 *
 * Why "PipeheadConfig"? Because even pipeheads need to know how to configure themselves!
 */
export interface PipeheadConfig {
  /** Pipehead ID */
  id: string;

  /** Pipehead type */
  type: 'required' | 'enrichment' | 'ingress';

  /** Pipehead identifier */
  plugin: string;

  /** Whether this pipehead can run in parallel */
  parallel?: boolean;

  /** Pipehead dependencies */
  dependencies?: string[];

  /** Pipehead-specific configuration */
  config?: Record<string, unknown>;
}

/**
 * Abstract base class for pipeheads.
 *
 * Provides common functionality for all pipehead implementations including:
 * - Trace entry creation
 * - Error handling
 * - State management utilities
 *
 * Why "BasePipehead"? Because every pipehead needs a good foundation!
 */
export abstract class BasePipehead implements Pipehead {
  abstract id: string;
  abstract type: 'required' | 'enrichment' | 'ingress';
  abstract plugin: string;
  abstract parallel?: boolean;
  abstract dependencies?: string[];

  /**
   * Executes the pipehead with automatic trace entry management.
   *
   * @param state - The current pipeline state
   * @returns Promise<PipelineState> - The updated state
   */
  async execute(state: PipelineState): Promise<PipelineState> {
    const startTime = Date.now();
    const startTimeIso = new Date(startTime).toISOString();

    // Create a trace entry for the start of execution
    const traceEntry: ExecutionTraceEntry = {
      nodeId: this.id,
      nodeType: this.type,
      startTime: startTimeIso,
      status: 'running',
    };

    try {
      // Execute the pipehead logic
      const result = await this.executeInternal(state);

      // Update trace entry with completion status
      const endTime = Date.now();
      const endTimeIso = new Date(endTime).toISOString();
      const duration = endTime - startTime;

      const completedTraceEntry: ExecutionTraceEntry = {
        ...traceEntry,
        endTime: endTimeIso,
        duration,
        status: 'completed',
      };

      result.metadata.trace.push(completedTraceEntry);

      return result;
    } catch (error) {
      // Update trace entry with failure status
      const endTime = Date.now();
      const endTimeIso = new Date(endTime).toISOString();
      const duration = endTime - startTime;

      const failedTraceEntry: ExecutionTraceEntry = {
        ...traceEntry,
        endTime: endTimeIso,
        duration,
        status: 'failed',
        error: error instanceof Error ? error.message : String(error),
      };

      state.metadata.trace.push(failedTraceEntry);

      throw error;
    }
  }

  /**
   * Internal execution method to be implemented by subclasses.
   *
   * @param state - The current pipeline state
   * @returns Promise<PipelineState> - The updated state
   * @protected
   */
  protected abstract executeInternal(state: PipelineState): Promise<PipelineState>;
}
```

---

### 2.2 Core Infrastructure Files

#### PluginRegistry.ts

**File:** `afi-reactor/src/langgraph/PluginRegistry.ts`

**Changes:**
1. Update import statement (line 14): `LangGraphNode` → `Pipehead`
2. Update import statement (line 15): `isLangGraphNode` → `isPipehead`
3. Update type annotation (line 102): `Map<string, LangGraphNode>` → `Map<string, Pipehead>`
4. Update method signature (line 218): `registerPlugin(plugin: LangGraphNode)` → `registerPlugin(plugin: Pipehead)`
5. Update method signature (line 304): `getPlugin(name: string): LangGraphNode | undefined` → `getPlugin(name: string): Pipehead | undefined`
6. Update method signature (line 314): `getPluginsByType(type: PluginType): LangGraphNode[]` → `getPluginsByType(type: PluginType): Pipehead[]`
7. Update method signature (line 333): `getAllPlugins(): LangGraphNode[]` → `getAllPlugins(): Pipehead[]`
8. Update method signature (line 369): `validatePlugin(plugin: unknown): boolean` - update internal call to `isPipehead`
9. Update method signature (line 380): `determinePluginType(plugin: LangGraphNode)` → `determinePluginType(plugin: Pipehead)`
10. Update method signature (line 508): `getEnabledPlugins(): LangGraphNode[]` → `getEnabledPlugins(): Pipehead[]`
11. Update method signature (line 527): `getEnabledPluginsByType(type: PluginType): LangGraphNode[]` → `getEnabledPluginsByType(type: PluginType): Pipehead[]`
12. Update error message (line 224): "Plugin does not implement LangGraphNode interface" → "Plugin does not implement Pipehead interface"
13. Update JSDoc comments to reflect new naming

#### DAGBuilder.ts

**File:** `afi-reactor/src/langgraph/DAGBuilder.ts`

**Changes:**
1. Update import statement: `LangGraphNode` → `Pipehead`
2. Update type annotation: `node?: LangGraphNode` → `node?: Pipehead`
3. Update all references to `LangGraphNode` in type annotations
4. Update JSDoc comments to reflect new naming

#### DAGExecutor.ts

**File:** `afi-reactor/src/langgraph/DAGExecutor.ts`

**Changes:**
1. Update import statement: `LangGraphNode` → `Pipehead`
2. Update all references to `LangGraphNode` in type annotations
3. Update JSDoc comments to reflect new naming

---

### 2.3 Required Node Implementations

#### AnalystNode.ts

**File:** `afi-reactor/src/langgraph/nodes/AnalystNode.ts`

**Changes:**
1. Update import statement (line 16): `LangGraphNode, LangGraphState` → `Pipehead, PipelineState`
2. Update class declaration (line 32): `implements LangGraphNode` → `implements Pipehead`
3. Update method signature (line 66): `execute(state: LangGraphState): Promise<LangGraphState>` → `execute(state: PipelineState): Promise<PipelineState>`
4. Update all references to `LangGraphState` in type annotations
5. Update JSDoc comments to reflect new naming

#### ExecutionNode.ts

**File:** `afi-reactor/src/langgraph/nodes/ExecutionNode.ts`

**Changes:**
1. Update import statement: `LangGraphNode, LangGraphState` → `Pipehead, PipelineState`
2. Update class declaration: `implements LangGraphNode` → `implements Pipehead`
3. Update method signature: `execute(state: LangGraphState): Promise<LangGraphState>` → `execute(state: PipelineState): Promise<PipelineState>`
4. Update all references to `LangGraphState` in type annotations
5. Update JSDoc comments to reflect new naming

#### ObserverNode.ts

**File:** `afi-reactor/src/langgraph/nodes/ObserverNode.ts`

**Changes:**
1. Update import statement: `LangGraphNode, LangGraphState` → `Pipehead, PipelineState`
2. Update class declaration: `implements LangGraphNode` → `implements Pipehead`
3. Update method signature: `execute(state: LangGraphState): Promise<LangGraphState>` → `execute(state: PipelineState): Promise<PipelineState>`
4. Update all references to `LangGraphState` in type annotations
5. Update JSDoc comments to reflect new naming

---

### 2.4 Enrichment Node Implementations

#### TechnicalIndicatorsNode.ts

**File:** `afi-reactor/src/langgraph/plugins/TechnicalIndicatorsNode.ts`

**Changes:**
1. Update import statement: `LangGraphNode, LangGraphState` → `Pipehead, PipelineState`
2. Update class declaration: `implements LangGraphNode` → `implements Pipehead`
3. Update method signature: `execute(state: LangGraphState): Promise<LangGraphState>` → `execute(state: PipelineState): Promise<PipelineState>`
4. Update all references to `LangGraphState` in type annotations
5. Update JSDoc comments to reflect new naming

#### PatternRecognitionNode.ts

**File:** `afi-reactor/src/langgraph/plugins/PatternRecognitionNode.ts`

**Changes:**
1. Update import statement: `LangGraphNode, LangGraphState` → `Pipehead, PipelineState`
2. Update class declaration: `implements LangGraphNode` → `implements Pipehead`
3. Update method signature: `execute(state: LangGraphState): Promise<LangGraphState>` → `execute(state: PipelineState): Promise<PipelineState>`
4. Update all references to `LangGraphState` in type annotations
5. Update JSDoc comments to reflect new naming

#### SentimentNode.ts

**File:** `afi-reactor/src/langgraph/plugins/SentimentNode.ts`

**Changes:**
1. Update import statement: `LangGraphNode, LangGraphState` → `Pipehead, PipelineState`
2. Update class declaration: `implements LangGraphNode` → `implements Pipehead`
3. Update method signature: `execute(state: LangGraphState): Promise<LangGraphState>` → `execute(state: PipelineState): Promise<PipelineState>`
4. Update all references to `LangGraphState` in type annotations
5. Update JSDoc comments to reflect new naming

#### NewsNode.ts

**File:** `afi-reactor/src/langgraph/plugins/NewsNode.ts`

**Changes:**
1. Update import statement: `LangGraphNode, LangGraphState` → `Pipehead, PipelineState`
2. Update class declaration: `implements LangGraphNode` → `implements Pipehead`
3. Update method signature: `execute(state: LangGraphState): Promise<LangGraphState>` → `execute(state: PipelineState): Promise<PipelineState>`
4. Update all references to `LangGraphState` in type annotations
5. Update JSDoc comments to reflect new naming

#### AiMlNode.ts

**File:** `afi-reactor/src/langgraph/plugins/AiMlNode.ts`

**Changes:**
1. Update import statement: `LangGraphNode, LangGraphState` → `Pipehead, PipelineState`
2. Update class declaration: `implements LangGraphNode` → `implements Pipehead`
3. Update method signature: `execute(state: LangGraphState): Promise<LangGraphState>` → `execute(state: PipelineState): Promise<PipelineState>`
4. Update all references to `LangGraphState` in type annotations
5. Update JSDoc comments to reflect new naming

---

### 2.5 Ingress Node Implementations

#### ScoutNode.ts

**File:** `afi-reactor/src/langgraph/plugins/ScoutNode.ts`

**Changes:**
1. Update import statement: `LangGraphNode, LangGraphState` → `Pipehead, PipelineState`
2. Update class declaration: `implements LangGraphNode` → `implements Pipehead`
3. Update method signature: `execute(state: LangGraphState): Promise<LangGraphState>` → `execute(state: PipelineState): Promise<PipelineState>`
4. Update all references to `LangGraphState` in type annotations
5. Update JSDoc comments to reflect new naming

#### SignalIngressNode.ts

**File:** `afi-reactor/src/langgraph/plugins/SignalIngressNode.ts`

**Changes:**
1. Update import statement: `LangGraphNode, LangGraphState` → `Pipehead, PipelineState`
2. Update class declaration: `implements LangGraphNode` → `implements Pipehead`
3. Update method signature: `execute(state: LangGraphState): Promise<LangGraphState>` → `execute(state: PipelineState): Promise<PipelineState>`
4. Update all references to `LangGraphState` in type annotations
5. Update JSDoc comments to reflect new naming

---

### 2.6 Test Files

#### langgraph.test.ts

**File:** `afi-reactor/src/types/__tests__/langgraph.test.ts`

**Changes:**
1. Update import statements: `LangGraphNode, LangGraphState, isLangGraphNode, isLangGraphState` → `Pipehead, PipelineState, isPipehead, isPipelineState`
2. Update all variable declarations: `LangGraphNode` → `Pipehead`
3. Update all variable declarations: `LangGraphState` → `PipelineState`
4. Update all function calls: `isLangGraphNode` → `isPipehead`
5. Update all function calls: `isLangGraphState` → `isPipelineState`
6. Update all type annotations
7. Update test descriptions to reflect new naming

#### integration.test.ts

**File:** `afi-reactor/src/langgraph/__tests__/integration.test.ts`

**Changes:**
1. Update import statement: `LangGraphNode` → `Pipehead`
2. Update all references to `LangGraphNode` in type annotations
3. Update test descriptions to reflect new naming

#### PluginRegistry.test.ts

**File:** `afi-reactor/src/langgraph/__tests__/PluginRegistry.test.ts`

**Changes:**
1. Update import statement: `LangGraphNode` → `Pipehead`
2. Update all mock class declarations: `implements LangGraphNode` → `implements Pipehead`
3. Update all type annotations: `LangGraphNode` → `Pipehead`
4. Update test descriptions to reflect new naming

#### DAGBuilder.test.ts

**File:** `afi-reactor/src/langgraph/__tests__/DAGBuilder.test.ts`

**Changes:**
1. Update import statement: `LangGraphNode` → `Pipehead`
2. Update all mock class declarations: `implements LangGraphNode` → `implements Pipehead`
3. Update all type annotations: `LangGraphNode` → `Pipehead`
4. Update test descriptions to reflect new naming

#### DAGExecutor.test.ts

**File:** `afi-reactor/src/langgraph/__tests__/DAGExecutor.test.ts`

**Changes:**
1. Update import statement: `LangGraphNode` → `Pipehead`
2. Update all mock class declarations: `implements LangGraphNode` → `implements Pipehead`
3. Update all type annotations: `LangGraphNode` → `Pipehead`
4. Update test descriptions to reflect new naming

#### test-utils.ts

**File:** `afi-reactor/src/langgraph/__tests__/test-utils.ts`

**Changes:**
1. Update import statement: `LangGraphNode` → `Pipehead`
2. Update all mock class declarations: `implements LangGraphNode` → `implements Pipehead`
3. Update all type annotations: `LangGraphNode` → `Pipehead`

---

### 2.7 Documentation Files

#### INTEGRATION_TEST_ANALYSIS_AND_PLAN.md

**File:** `afi-reactor/INTEGRATION_TEST_ANALYSIS_AND_PLAN.md`

**Changes:**
1. Update all references to `LangGraphNode` → `Pipehead`
2. Update all references to `LangGraphState` → `PipelineState`
3. Update all references to `isLangGraphNode` → `isPipehead`
4. Update all references to `isLangGraphState` → `isPipelineState`
5. Update code examples to reflect new naming
6. Update documentation text to reflect new naming

---

## 3. Execution Order

### Phase 1: Type Definitions (Foundation)
1. Update `afi-reactor/src/types/langgraph.ts`
   - Rename interfaces
   - Add new interfaces and classes
   - Update type guards

### Phase 2: Core Infrastructure
2. Update `afi-reactor/src/langgraph/PluginRegistry.ts`
3. Update `afi-reactor/src/langgraph/DAGBuilder.ts`
4. Update `afi-reactor/src/langgraph/DAGExecutor.ts`

### Phase 3: Required Node Implementations
5. Update `afi-reactor/src/langgraph/nodes/AnalystNode.ts`
6. Update `afi-reactor/src/langgraph/nodes/ExecutionNode.ts`
7. Update `afi-reactor/src/langgraph/nodes/ObserverNode.ts`

### Phase 4: Enrichment Node Implementations
8. Update `afi-reactor/src/langgraph/plugins/TechnicalIndicatorsNode.ts`
9. Update `afi-reactor/src/langgraph/plugins/PatternRecognitionNode.ts`
10. Update `afi-reactor/src/langgraph/plugins/SentimentNode.ts`
11. Update `afi-reactor/src/langgraph/plugins/NewsNode.ts`
12. Update `afi-reactor/src/langgraph/plugins/AiMlNode.ts`

### Phase 5: Ingress Node Implementations
13. Update `afi-reactor/src/langgraph/plugins/ScoutNode.ts`
14. Update `afi-reactor/src/langgraph/plugins/SignalIngressNode.ts`

### Phase 6: Test Files
15. Update `afi-reactor/src/types/__tests__/langgraph.test.ts`
16. Update `afi-reactor/src/langgraph/__tests__/integration.test.ts`
17. Update `afi-reactor/src/langgraph/__tests__/PluginRegistry.test.ts`
18. Update `afi-reactor/src/langgraph/__tests__/DAGBuilder.test.ts`
19. Update `afi-reactor/src/langgraph/__tests__/DAGExecutor.test.ts`
20. Update `afi-reactor/src/langgraph/__tests__/test-utils.ts`

### Phase 7: Documentation
21. Update `afi-reactor/INTEGRATION_TEST_ANALYSIS_AND_PLAN.md`

### Phase 8: Verification
22. Verify all imports and exports are updated
23. Run TypeScript compilation to verify no errors
24. Run tests to ensure functionality is preserved

---

## 4. Risk Assessment

| Risk | Level | Mitigation |
|------|-------|------------|
| Breaking changes to external consumers | **Low** | No external consumers - solo MVP |
| Test failures | Low | Update tests during migration |
| Documentation inconsistency | Low | Update documentation in parallel |
| Runtime errors | Low | TypeScript compilation will catch issues |
| Developer confusion during transition | Medium | Clear communication of naming change |

---

## 5. Benefits

| Benefit | Impact |
|---------|--------|
| Improved code clarity | High |
| Reduced confusion about dependencies | High |
| Better alignment with system design goals | High |
| Enhanced maintainability | Medium |
| Improved developer experience | Medium |
| Added memorability and personality | High |
| Playful, approachable codebase | High |

---

## 6. Post-Refactoring Tasks

1. Update README.md files to reflect new naming
2. Update any additional documentation that references LangGraphNode
3. Consider creating a migration guide for future reference
4. Update any CI/CD pipelines that may reference old naming
5. Update any configuration files that may reference old naming

---

## 7. Success Criteria

- [ ] All 21 files updated with new naming
- [ ] TypeScript compilation succeeds with no errors
- [ ] All tests pass
- [ ] No references to `LangGraphNode` remain in the codebase
- [ ] No references to `LangGraphState` remain in the codebase
- [ ] Documentation is consistent with new naming
- [ ] Codebase is fully functional after refactoring

---

## 8. Notes

- This is a global rename operation without backward compatibility constraints
- The "Pipehead" naming convention is intentionally playful and memorable
- All JSDoc comments should be updated to reflect the new terminology
- The `BasePipehead` abstract class provides common functionality for all pipehead implementations
- The `PipeheadMetadata` interface enables better plugin discovery and documentation
- The `PipeheadConfig` interface enables configuration validation before execution

---

**End of Plan**
