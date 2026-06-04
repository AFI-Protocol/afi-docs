# Phase 3: Template Registry - Status & Resumption Plan

**Project:** AFI-Reactor pipeline / DAG integration
**Phase:** Phase 3 - Template Registry in afi-factory
**Status:** In Progress - Initial Information Gathering Complete
**Last Updated:** 2025-12-26T16:13:00Z

---

## Executive Summary

Phase 3 focuses on updating the afi-factory template registry to load and validate analyst configurations, bridging afi-config schemas with afi-reactor orchestration. Initial information gathering has been completed, but no code has been written yet.

---

## Current Progress

### ✅ Completed (Phase 1 & 2)
- **Phase 1 (Schema Foundation):** JSON schemas created in afi-config
  - [`analyst-config.schema.json`](../afi-config/schemas/analyst-config.schema.json)
  - [`enrichment-node.schema.json`](../afi-config/schemas/definitions/enrichment-node.schema.json)
  - Example configurations provided

- **Phase 2 (TypeScript Interfaces):** Type definitions created in afi-factory
  - [`schemas/index.ts`](../afi-factory/schemas/index.ts) with complete interfaces
  - Type guards for runtime validation
  - Supporting interfaces (ValidatedAnalystConfig, TemplateRegistryEntry, LoadAnalystConfigOptions)

### 🔄 In Progress (Phase 3)
- **Information Gathering:** ✅ Complete
  - Read existing template_registry.ts (minimal implementation)
  - Reviewed all schemas and examples
  - Understood TypeScript interfaces from Phase 2

- **Implementation:** ⏳ Not Started
  - No code written yet for Phase 3

### ⏳ Pending (Phase 3)
- Update afi-factory/template_registry.ts
- Create afi-factory/validators/analyst-config-validator.ts
- Create example analyst configurations
- Add unit tests
- Add integration tests

---

## Phase 3 Objectives

### 1. Update afi-factory/template_registry.ts
**Current State:** Minimal implementation with only `loadTemplate()` function

**Required Functions:**
- `loadAnalystConfig(analystId, options)` - Load analyst configuration from file
- `loadEnrichmentNodeTemplate(nodeId)` - Load enrichment node template
- `listAnalystConfigs(configDir)` - List all analyst configurations
- `validateAnalystConfig(config)` - Validate analyst configuration
- `checkForCircularDependencies(nodeId, dependencies, allNodes, visited)` - Check for circular dependencies

**Key Requirements:**
- Maintain backward compatibility with existing `loadTemplate()` function
- Use schemas from afi-config for validation
- Use TypeScript interfaces from afi-factory/schemas/index.ts
- Comprehensive error handling
- JSDoc comments

### 2. Create afi-factory/validators/analyst-config-validator.ts
**Required Functions:**
- `validateAnalystConfig(config)` - Validate analyst configuration against schema
- `validateEnrichmentNode(node)` - Validate enrichment node
- `isValidISODate(dateString)` - Check if string is valid ISO date

**Key Requirements:**
- Use JSON schemas from afi-config
- Return validation results with errors/warnings
- Support schema validation using ajv or similar library

### 3. Create Example Analyst Configurations
**Required Files:**
- `afi-factory/analyst-configs/froggy-trend-pullback-v1.json`
- `afi-factory/analyst-configs/crypto-analyst-v1.json`
- `afi-factory/analyst-configs/templates/analyst-config.template.json`
- `afi-factory/analyst-configs/templates/enrichment-node.template.json`

**Key Requirements:**
- Demonstrate different use cases
- Validate successfully against schemas
- Include comprehensive metadata

### 4. Add Unit Tests
**Required Tests:**
- Template registry functions
- Validation functions
- Error handling
- Edge cases

### 5. Add Integration Tests
**Required Tests:**
- End-to-end configuration loading
- Schema validation integration
- Circular dependency detection

---

## Technical Context

### Existing Code Structure

**afi-factory/template_registry.ts** (Current):
```typescript
export const loadTemplate = (templateId: string) => {
  switch (templateId) {
    case 'validator-v1':
      return { type: 'validator', entry: './templates/validator.ts' };
    case 'signal-emitter-basic':
      return { type: 'signal', entry: './templates/emitter.ts' };
    default:
      throw new Error('Template not found: ' + templateId);
  }
};
```

**afi-factory/schemas/index.ts** (Phase 2 - Complete):
- `EnrichmentNodeConfig` interface
- `AnalystConfig` interface
- `ValidatedAnalystConfig` interface
- `TemplateRegistryEntry` interface
- `LoadAnalystConfigOptions` interface
- Type guards: `isEnrichmentNodeConfig()`, `isAnalystConfig()`, `isValidatedAnalystConfig()`

**afi-config/schemas/** (Phase 1 - Complete):
- `analyst-config.schema.json` - Full schema with validation rules
- `definitions/enrichment-node.schema.json` - Enrichment node schema
- Examples provided for reference

### Dependencies Analysis

**afi-factory/package.json** - Current State:
```json
{
  "name": "afi-factory",
  "version": "1.0.0",
  "description": "AFI agent factory and templates",
  "type": "module",
  "scripts": {
    "build": "tsc",
    "test": "echo 'No tests yet' && exit 0",
    "typecheck": "tsc --noEmit"
  },
  "keywords": ["afi", "factory", "agents", "templates"],
  "license": "MIT"
}
```

**Dependencies Required:**
- **ajv** (^8.12.0) - JSON schema validation (used in afi-config)
- **ajv-formats** (^3.0.1) - Additional format validators for ajv
- **vitest** (^4.0.14) - Testing framework (used in afi-config)
- **@types/node** (^20.11.0) - Node.js type definitions

**Note:** afi-config already has these dependencies. afi-factory needs to add them.

---

## Implementation Plan

### Step 1: Check Dependencies
- Review afi-factory/package.json for existing dependencies
- Add ajv or similar JSON schema validator if not present
- Ensure testing framework is configured

### Step 2: Create Validator Module
- Create `afi-factory/validators/analyst-config-validator.ts`
- Implement `validateAnalystConfig()` using JSON schemas
- Implement `validateEnrichmentNode()` 
- Implement `isValidISODate()`
- Add comprehensive error messages

### Step 3: Update Template Registry
- Extend `afi-factory/template_registry.ts`
- Add new functions while preserving backward compatibility
- Implement file loading with proper error handling
- Add caching support
- Implement circular dependency detection

### Step 4: Create Example Configurations
- Create `afi-factory/analyst-configs/` directory
- Create example configurations based on afi-config/examples
- Create template files for reference
- Ensure all examples validate successfully

### Step 5: Add Unit Tests
- Create `afi-factory/__tests__/template-registry.test.ts`
- Test all new functions
- Test error cases
- Test edge cases

### Step 6: Add Integration Tests
- Create `afi-factory/__tests__/integration/analyst-config-loading.test.ts`
- Test end-to-end workflows
- Test schema validation integration

### Step 7: Verify and Document
- Run all tests
- Update README if needed
- Ensure backward compatibility

---

## File Structure After Implementation

```
afi-factory/
├── template_registry.ts              # Updated with new functions
├── validators/
│   └── analyst-config-validator.ts   # New validation module
├── analyst-configs/
│   ├── froggy-trend-pullback-v1.json # Example config
│   ├── crypto-analyst-v1.json        # Example config
│   └── templates/
│       ├── analyst-config.template.json
│       └── enrichment-node.template.json
├── __tests__/
│   ├── template-registry.test.ts     # Unit tests
│   └── integration/
│       └── analyst-config-loading.test.ts  # Integration tests
└── schemas/
    └── index.ts                      # Phase 2 - already complete
```

---

## Success Criteria

- [ ] Template registry loads analyst configurations from files
- [ ] Template registry validates configurations against schemas
- [ ] Example configurations validate successfully
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] Backward compatibility maintained with existing `loadTemplate()` function
- [ ] Comprehensive error handling implemented
- [ ] JSDoc comments added to all functions

---

## Resuming This Work

### Quick Start Instructions

To resume Phase 3 implementation in a new task:

1. **Read this status document** (`plans/phase3-template-registry-status.md`)
2. **Review the implementation plan** above (Steps 1-7)
3. **Add dependencies** to afi-factory/package.json:
   ```bash
   cd afi-factory
   npm install --save-dev ajv@^8.12.0 ajv-formats@^3.0.1 vitest@^4.0.14 @types/node@^20.11.0
   ```
4. **Update package.json scripts** to use vitest:
   ```json
   "scripts": {
     "build": "tsc",
     "test": "vitest",
     "test:run": "vitest run",
     "typecheck": "tsc --noEmit"
   }
   ```
5. **Create vitest.config.ts** (if not present)
6. **Start with Step 2** of the implementation plan (Create Validator Module)

### Key Files to Reference:

- **Schemas:** [`afi-config/schemas/analyst-config.schema.json`](../afi-config/schemas/analyst-config.schema.json)
- **Definitions:** [`afi-config/schemas/definitions/enrichment-node.schema.json`](../afi-config/schemas/definitions/enrichment-node.schema.json)
- **Examples:** [`afi-config/examples/analyst-config.example.json`](../afi-config/examples/analyst-config.example.json)
- **Types:** [`afi-factory/schemas/index.ts`](../afi-factory/schemas/index.ts)
- **Current Registry:** [`afi-factory/template_registry.ts`](../afi-factory/template_registry.ts)

### Recommended Mode for Implementation:

Use **Code mode** for implementing the changes, as this involves writing and modifying code files.

---

## Important Notes

### Dependencies Status
- **afi-factory currently has NO dependencies** - needs ajv, ajv-formats, vitest, @types/node
- **afi-config already has these dependencies** - can reference their implementation
- **Testing framework**: afi-config uses vitest, afi-factory should follow the same pattern

### Implementation References
- **Schema validation pattern**: See [`afi-config/tests/schema-validation.test.ts`](../afi-config/tests/schema-validation.test.ts) for ajv usage examples
- **TypeScript interfaces**: Already complete in [`afi-factory/schemas/index.ts`](../afi-factory/schemas/index.ts)
- **JSON schemas**: Complete in [`afi-config/schemas/`](../afi-config/schemas/)

### Known Issues
- The LangGraph-era implementation plan is archived at `archive/langgraph-migration-2025/AFI_REACTOR_LANGGRAPH_IMPLEMENTATION_PLAN.md` (superseded; reactor uses `src/dag/`)
- afi-factory currently has no test infrastructure - needs to be set up

### Success Criteria Verification
- [ ] Template registry loads analyst configurations from files
- [ ] Template registry validates configurations against schemas
- [ ] Example configurations validate successfully
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] Backward compatibility maintained with existing `loadTemplate()` function
- [ ] Comprehensive error handling implemented
- [ ] JSDoc comments added to all functions

---

## Next Steps

1. Review afi-factory/package.json to check dependencies
2. Install ajv or similar JSON schema validator if needed
3. Create the validator module
4. Update the template registry
5. Create example configurations
6. Add tests
7. Verify all success criteria are met
