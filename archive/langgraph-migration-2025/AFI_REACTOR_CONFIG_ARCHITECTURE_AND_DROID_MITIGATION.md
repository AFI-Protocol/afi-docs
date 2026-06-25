> **Historical note:** This document describes a superseded LangGraph-era architecture plan. AFI Reactor now uses a custom deterministic TypeScript DAG under `afi-reactor/src/dag/`. This file is retained only for historical context and should not be treated as current implementation guidance.
>

# AFI-Reactor: Configuration Architecture & Droid Mitigation Strategy

## Executive Summary

This document clarifies the architectural distinction between [`afi-factory`](afi-factory/) and [`afi-config`](afi-config/) regarding configuration management in the proposed LangGraph-based flexible DAG system, and provides a detailed assessment of how Droids could be deployed as a proactive mitigation strategy for each specific risk identified in the LangGraph flexible DAG analysis.

---

## Part 1: Configuration Architecture - afi-factory vs. afi-config

### 1.1 Architectural Distinction

#### **afi-config: The Canonical Schema Library**

**Role**: [`afi-config`](afi-config/) is the **single source of truth** for all AFI Protocol configuration schemas, templates, and validation utilities.

**Responsibilities**:
- **JSON Schema Definitions**: Defines the structure and validation rules for all configuration formats
- **Canonical Schemas**: Provides the authoritative schema definitions that all other repos consume
- **Validation Utilities**: Provides tools for validating configurations against schemas
- **Governance Artifacts**: Hosts Codex governance documents including the Droid Charter and Playbook
- **Cross-Repo Standardization**: Ensures consistency across the entire AFI ecosystem

**Key Schemas**:
- [`character.schema.json`](afi-config/schemas/character.schema.json) - Agent/character configs (afi-core)
- [`pipeline.schema.json`](afi-config/schemas/pipeline.schema.json) - Pipeline configs (afi-reactor)
- [`blueprint.schema.json`](afi-config/schemas/blueprint.schema.json) - DAG/construct blueprints (afi-reactor)
- [`plugin-manifest.schema.json`](afi-config/schemas/plugin-manifest.schema.json) - Plugin manifests (afi-plugins)
- [`vault.schema.json`](afi-config/schemas/vault.schema.json) - T.S.S.D. Vault configs (afi-infra)
- [`.afi-codex.schema.json`](afi-config/.afi-codex.schema.json) - Codex metadata schema (all repos)

**Relationship to Other Repos**:
```
afi-config (foundational)
    ↓
    ├── afi-core (consumes character.schema.json)
    ├── afi-reactor (consumes pipeline.schema.json, blueprint.schema.json)
    ├── afi-infra (consumes vault.schema.json)
    ├── afi-plugins (consumes plugin-manifest.schema.json)
    ├── afi-ops (consumes ops-config.schema.json)
    └── afi-token (consumes token-config.schema.json)
```

**Key Principle**: **afi-config defines WHAT configurations look like** (schemas, structure, validation rules).

---

#### **afi-factory: Agent Template and Spawning Registry**

**Role**: [`afi-factory`](afi-factory/) is where **agent templates are registered, versioned, and spawned** across the AFI Protocol.

**Responsibilities**:
- **Agent Templates**: Base templates for AFI agents
- **Template Registry**: Programmatic interface for loading and versioning templates
- **Agent Manifest**: Registry of agent templates and logic modules
- **Spawning Logic**: Agent instantiation and lifecycle management
- **Template Validation**: Ensures templates conform to schemas from afi-config

**Key Components**:
- [`agent_manifest.json`](afi-factory/agent_manifest.json) - Registry of agent templates and logic modules
- [`template_registry.ts`](afi-factory/template_registry.ts) - Programmatic interface for loading templates
- [`schemas/`](afi-factory/schemas/) - Agent-specific schema extensions (currently empty, ready for use)
- [`agent-prompts/`](afi-factory/agent-prompts/) - Agent prompt templates

**Relationship to Other Repos**:
```
afi-factory (template layer)
    ↓
    ├── afi-core (agent runtime)
    ├── afi-reactor (agent orchestration)
    └── afi-skills (agent skills)
```

**Key Principle**: **afi-factory defines HOW agents are instantiated and configured** (templates, spawning logic, runtime configuration).

---

### 1.2 Why afi-factory for Analyst Configuration?

In the LangGraph flexible DAG proposal, analyst configuration is stored in [`afi-factory`](afi-factory/) rather than [`afi-config`](afi-config/) for the following reasons:

#### **1. Analyst Configuration is Runtime Configuration, Not Schema**

- **afi-config** defines **schemas** (structure, validation rules)
- **afi-factory** stores **runtime configurations** (actual analyst preferences, enrichment node selections)

Analyst configuration is **instance-specific data** (which enrichment nodes this analyst uses), not a **schema definition** (what fields an analyst config must have).

#### **2. Analyst Configuration is Template-Based**

Analyst configurations follow a **template pattern**:
- Each analyst has a configuration file
- Configuration files are **instantiated from templates**
- Templates are **versioned and managed** in afi-factory

This aligns with afi-factory's core responsibility: **template management and spawning**.

#### **3. Analyst Configuration is Agent-Specific**

Analyst configurations are **tied to specific agents** (analysts):
- Each analyst has their own enrichment strategy
- Configuration is **agent runtime data**, not a system-wide schema
- afi-factory is the **natural home for agent-specific runtime data**

#### **4. Separation of Concerns**

```
afi-config (Schema Layer)
    ↓ Defines schemas for analyst configuration
    ↓ Example: analyst-config.schema.json

afi-factory (Template Layer)
    ↓ Stores actual analyst configurations
    ↓ Example: analyst-configs/froggy-trend-pullback-v1.json

afi-reactor (Orchestration Layer)
    ↓ Reads analyst configurations from afi-factory
    ↓ Builds appropriate DAGs based on configuration
```

This separation ensures:
- **afi-config** remains schema-focused (WHAT configurations look like)
- **afi-factory** remains template-focused (HOW agents are configured)
- **afi-reactor** remains orchestration-focused (HOW DAGs are executed)

---

### 1.3 Proposed Configuration Architecture for LangGraph Flexible DAG

#### **Schema Layer (afi-config)**

**New Schema**: [`analyst-config.schema.json`](afi-config/schemas/analyst-config.schema.json)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://afi-protocol.org/schemas/analyst-config.schema.json",
  "title": "Analyst Configuration Schema",
  "type": "object",
  "properties": {
    "analystId": {
      "type": "string",
      "description": "Unique identifier for the analyst"
    },
    "enrichmentNodes": {
      "type": "array",
      "description": "Array of enrichment node configurations",
      "items": {
        "$ref": "#/definitions/enrichment-node.json"
      }
    }
  }
}
```

**New Schema**: [`enrichment-node.schema.json`](afi-config/schemas/definitions/enrichment-node.schema.json)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://afi-protocol.org/schemas/definitions/enrichment-node.schema.json",
  "title": "Enrichment Node Definition",
  "type": "object",
  "properties": {
    "id": {
      "type": "string",
      "description": "Unique identifier for the enrichment node"
    },
    "type": {
      "type": "string",
      "enum": ["enrichment", "ingress"],
      "description": "Type of node"
    },
    "plugin": {
      "type": "string",
      "description": "LangGraph plugin ID"
    },
    "optional": {
      "type": "boolean",
      "description": "Whether this node is optional"
    },
    "parallel": {
      "type": "boolean",
      "description": "Whether this node can run in parallel with others"
    },
    "dependencies": {
      "type": "array",
      "items": {
        "type": "string",
        "description": "IDs of nodes this node depends on"
      }
    }
  }
}
```

**Updated Schema**: [`pipeline.schema.json`](afi-config/schemas/pipeline.schema.json)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://afi-protocol.org/schemas/pipeline.schema.json",
  "title": "Pipeline Configuration Schema",
  "type": "object",
  "properties": {
    "requiredNodes": {
      "type": "array",
      "description": "Required nodes that are always present",
      "items": {
        "type": "string"
      }
    },
    "enrichmentNodes": {
      "type": "object",
      "description": "Available enrichment nodes (analyst-configurable)",
      "additionalProperties": {
        "$ref": "#/definitions/enrichment-node.json"
      }
    }
  }
}
```

---

#### **Template Layer (afi-factory)**

**Directory Structure**:
```
afi-factory/
├── analyst-configs/
│   ├── froggy-trend-pullback-v1.json
│   ├── froggy-trend-pullback-v2.json
│   ├── another-analyst-v1.json
│   └── templates/
│       ├── analyst-config.template.json
│       └── enrichment-node.template.json
├── schemas/
│   └── index.ts (TypeScript types for analyst configs)
└── template_registry.ts (updated to load analyst configs)
```

**Example Analyst Configuration**: [`afi-factory/analyst-configs/froggy-trend-pullback-v1.json`](afi-factory/analyst-configs/froggy-trend-pullback-v1.json)

```json
{
  "analystId": "froggy-trend-pullback-v1",
  "enrichmentNodes": [
    {
      "id": "technical-indicators",
      "enabled": true,
      "parallel": true
    },
    {
      "id": "pattern-recognition",
      "enabled": true,
      "parallel": false,
      "dependencies": ["technical-indicators"]
    },
    {
      "id": "sentiment",
      "enabled": true,
      "parallel": true
    },
    {
      "id": "news",
      "enabled": false,
      "parallel": false,
      "dependencies": ["sentiment"]
    }
  ]
}
```

**Updated Template Registry**: [`afi-factory/template_registry.ts`](afi-factory/template_registry.ts)

```typescript
// Load analyst configuration
export const loadAnalystConfig = (analystId: string) => {
  const configPath = `./analyst-configs/${analystId}.json`;
  // Load and validate against schema from afi-config
  return loadAndValidate(configPath, 'analyst-config.schema.json');
};

// Load enrichment node template
export const loadEnrichmentNodeTemplate = (nodeId: string) => {
  const templatePath = `./analyst-configs/templates/enrichment-node.template.json`;
  // Load and validate against schema from afi-config
  return loadAndValidate(templatePath, 'enrichment-node.schema.json');
};
```

---

#### **Orchestration Layer (afi-reactor)**

**LangGraph Orchestrator**: [`afi-reactor/src/langgraph/LangGraphOrchestrator.ts`](afi-reactor/src/langgraph/LangGraphOrchestrator.ts)

```typescript
import { Graph } from '@langchain/langgraph';
import { loadAnalystConfig } from 'afi-factory/template_registry';

export class LangGraphOrchestrator {
  async buildDAG(analystId: string): Promise<Graph> {
    // Load analyst configuration from afi-factory
    const analystConfig = await loadAnalystConfig(analystId);
    
    const graph = new Graph();
    
    // Add required nodes
    graph.addNode('analyst', AnalystNode);
    graph.addNode('execution', ExecutionNode);
    graph.addNode('observer', ObserverNode);
    
    // Add enrichment nodes based on analyst config
    for (const nodeConfig of analystConfig.enrichmentNodes) {
      if (nodeConfig.enabled) {
        const plugin = await this.loadPlugin(nodeConfig.plugin);
        graph.addNode(nodeConfig.id, plugin);
        
        // Connect to analyst
        graph.addEdge('analyst', nodeConfig.id);
        
        // Handle dependencies
        for (const dep of nodeConfig.dependencies) {
          graph.addEdge(dep, nodeConfig.id);
        }
      }
    }
    
    // Connect to execution
    for (const nodeConfig of analystConfig.enrichmentNodes) {
      if (nodeConfig.enabled) {
        graph.addEdge(nodeConfig.id, 'execution');
      }
    }
    
    // Connect to observer
    graph.addEdge('execution', 'observer');
    
    return graph;
  }
  
  private async loadPlugin(pluginId: string): Promise<LangGraphNode> {
    // Load plugin from afi-reactor/plugins/langgraph/
    const plugin = await import(`./plugins/langgraph/${pluginId}.ts`);
    return plugin.default;
  }
}
```

---

### 1.4 Summary: afi-config vs. afi-factory

| Aspect | afi-config | afi-factory |
|--------|-----------|-------------|
| **Primary Role** | Schema library | Template registry |
| **What it Defines** | WHAT configurations look like | HOW agents are configured |
| **Content** | JSON schemas, validation rules | Agent templates, runtime configs |
| **Consumers** | All AFI repos | afi-core, afi-reactor, afi-skills |
| **Analyst Config Role** | Defines schema for analyst config | Stores actual analyst configs |
| **Example** | `analyst-config.schema.json` | `froggy-trend-pullback-v1.json` |
| **Validation** | Provides validation utilities | Validates configs against schemas |
| **Versioning** | Schema versioning | Template versioning |

---

## Part 2: Droid Mitigation Strategy

### 2.1 Overview

The AFI Droid Charter ([`AFI_DROID_CHARTER.v0.1.md`](afi-config/codex/governance/droids/AFI_DROID_CHARTER.v0.1.md)) and Playbook ([`AFI_DROID_PLAYBOOK.v0.1.md`](afi-config/codex/governance/droids/AFI_DROID_PLAYBOOK.v0.1.md)) provide a framework for deploying automated coding agents (droids) to maintain and evolve the AFI codebase.

This section analyzes how Droids could be deployed as a **proactive mitigation strategy** for each specific risk identified in the LangGraph flexible DAG analysis.

---

### 2.2 Risk Analysis and Droid Mitigation

#### **Risk 1: Complexity Increase**

**Risk Description**: LangGraph integration adds complexity to the codebase, making it harder to understand and maintain.

**Droid Mitigation Strategy**:

**Droid Class**: **Documentation Droid**

**Mission**: Maintain comprehensive documentation and code clarity as complexity increases.

**Allowed Actions** (per Droid Charter):
- ✅ Add or refine documentation to clarify existing behavior and architecture
- ✅ Add new modules or files that are clearly scoped and documented
- ✅ Propose non-breaking code improvements (readability, type safety)

**Specific Tasks**:

1. **Automated Documentation Generation**:
   - Generate API documentation from TypeScript types
   - Create architecture diagrams from code structure
   - Document LangGraph node interfaces and contracts

2. **Code Clarity Enforcement**:
   - Add inline comments for complex LangGraph logic
   - Ensure all new code has clear documentation
   - Generate README files for new modules

3. **Architecture Visualization**:
   - Generate Mermaid diagrams from DAG configurations
   - Create visual representations of analyst configurations
   - Document data flow through LangGraph nodes

**Implementation**:

```typescript
// Droid task: Generate LangGraph documentation
export async function generateLangGraphDocs() {
  // 1. Scan all LangGraph plugins
  const plugins = await scanPlugins('./src/plugins/langgraph/');
  
  // 2. Extract interfaces and contracts
  const interfaces = await extractInterfaces(plugins);
  
  // 3. Generate documentation
  const docs = await generateDocs(interfaces);
  
  // 4. Write to docs/
  await writeDocs('./docs/langgraph/', docs);
}
```

**Success Metrics**:
- Documentation coverage > 90%
- All LangGraph nodes have clear documentation
- Architecture diagrams are up-to-date

---

#### **Risk 2: Learning Curve**

**Risk Description**: New paradigm for analysts and reactor developers requires significant learning investment.

**Droid Mitigation Strategy**:

**Droid Class**: **Training Droid**

**Mission**: Create comprehensive training materials and interactive examples to reduce learning curve.

**Allowed Actions** (per Droid Charter):
- ✅ Add or refine documentation to clarify existing behavior and architecture
- ✅ Suggest configurations, schemas, or starters that are aligned with existing patterns
- ✅ Add new modules or files that are clearly scoped and documented

**Specific Tasks**:

1. **Interactive Tutorial Generation**:
   - Create step-by-step tutorials for creating analyst configurations
   - Generate example configurations for common use cases
   - Create interactive playgrounds for testing DAG configurations

2. **Example Library**:
   - Generate example analyst configurations for different strategies
   - Create example LangGraph plugins for common enrichment patterns
   - Provide before/after examples showing migration from fixed to flexible DAG

3. **Validation Tools**:
   - Create CLI tools for validating analyst configurations
   - Generate configuration templates with validation
   - Provide real-time feedback on configuration errors

**Implementation**:

```typescript
// Droid task: Generate training materials
export async function generateTrainingMaterials() {
  // 1. Scan existing analyst configurations
  const configs = await scanAnalystConfigs('./afi-factory/analyst-configs/');
  
  // 2. Extract common patterns
  const patterns = await extractPatterns(configs);
  
  // 3. Generate tutorials
  const tutorials = await generateTutorials(patterns);
  
  // 4. Write to docs/training/
  await writeTutorials('./docs/training/', tutorials);
}
```

**Success Metrics**:
- New analysts can create configurations in < 1 hour
- Tutorial completion rate > 80%
- Example library covers > 90% of use cases

---

#### **Risk 3: Performance**

**Risk Description**: Dynamic DAG construction may have overhead, impacting system performance.

**Droid Mitigation Strategy**:

**Droid Class**: **Performance Droid**

**Mission**: Monitor, analyze, and optimize performance of LangGraph-based DAG execution.

**Allowed Actions** (per Droid Charter):
- ✅ Propose non-breaking code improvements (performance, readability, type safety)
- ✅ Add or update tests that improve coverage, without changing semantics
- ✅ Add new modules or files that are clearly scoped and documented

**Specific Tasks**:

1. **Performance Monitoring**:
   - Add instrumentation to track DAG construction time
   - Monitor execution time for each enrichment node
   - Track memory usage during DAG execution

2. **Optimization Suggestions**:
   - Analyze analyst configurations for optimization opportunities
   - Suggest parallelization opportunities
   - Identify bottlenecks in enrichment nodes

3. **Caching Strategies**:
   - Implement caching for analyst configurations
   - Cache DAG construction results
   - Implement memoization for expensive operations

**Implementation**:

```typescript
// Droid task: Analyze performance
export async function analyzePerformance() {
  // 1. Collect performance metrics
  const metrics = await collectMetrics();
  
  // 2. Analyze bottlenecks
  const bottlenecks = await analyzeBottlenecks(metrics);
  
  // 3. Generate optimization suggestions
  const suggestions = await generateSuggestions(bottlenecks);
  
  // 4. Write report
  await writeReport('./reports/performance/', suggestions);
}
```

**Success Metrics**:
- DAG construction time < 100ms
- Enrichment node execution time within SLA
- Performance regression detection < 24 hours

---

#### **Risk 4: Configuration Errors**

**Risk Description**: Analysts may misconfigure enrichment nodes, leading to incorrect behavior.

**Droid Mitigation Strategy**:

**Droid Class**: **Validation Droid**

**Mission**: Provide comprehensive validation tools and guardrails to prevent configuration errors.

**Allowed Actions** (per Droid Charter):
- ✅ Add or update tests that improve coverage, without changing semantics
- ✅ Suggest configurations, schemas, or starters that are aligned with existing patterns
- ✅ Add new modules or files that are clearly scoped and documented

**Specific Tasks**:

1. **Schema Validation**:
   - Validate analyst configurations against schemas from afi-config
   - Provide clear error messages for validation failures
   - Suggest fixes for common configuration errors

2. **Configuration Templates**:
   - Generate validated configuration templates
   - Provide pre-configured templates for common use cases
   - Ensure templates follow best practices

3. **Runtime Validation**:
   - Add runtime validation for analyst configurations
   - Validate enrichment node dependencies
   - Check for circular dependencies

**Implementation**:

```typescript
// Droid task: Validate configurations
export async function validateConfigurations() {
  // 1. Scan all analyst configurations
  const configs = await scanAnalystConfigs('./afi-factory/analyst-configs/');
  
  // 2. Validate against schemas
  const results = await validateAgainstSchemas(configs);
  
  // 3. Generate validation reports
  const reports = await generateReports(results);
  
  // 4. Write reports
  await writeReports('./reports/validation/', reports);
}
```

**Success Metrics**:
- Configuration validation coverage > 95%
- Error messages are clear and actionable
- Configuration error rate < 5%

---

### 2.3 Droid Deployment Strategy

#### **Phase 1: Foundation (Week 1-2)**

**Droid Class**: **Schema Droid**

**Mission**: Create and validate schemas for analyst configuration and enrichment nodes.

**Tasks**:
- Create `analyst-config.schema.json` in afi-config
- Create `enrichment-node.schema.json` in afi-config
- Update `pipeline.schema.json` in afi-config
- Add validation tests for all schemas
- Generate example configurations

**Success Criteria**:
- All schemas are valid JSON Schema Draft 7+
- All schemas have comprehensive documentation
- All schemas have validation tests
- Example configurations validate successfully

---

#### **Phase 2: Plugin System (Week 3-4)**

**Droid Class**: **Plugin Droid**

**Mission**: Implement LangGraph plugins for enrichment nodes.

**Tasks**:
- Implement technical indicators plugin
- Implement pattern recognition plugin
- Implement sentiment plugin
- Implement news plugin
- Implement scout plugin
- Implement signal ingress plugin
- Create plugin registry system
- Add tests for all plugins

**Success Criteria**:
- All plugins implement LangGraphNode interface
- All plugins have comprehensive tests
- All plugins have clear documentation
- Plugin registry loads all plugins successfully

---

#### **Phase 3: Orchestrator (Week 5-6)**

**Droid Class**: **Orchestrator Droid**

**Mission**: Implement LangGraph orchestrator and integration.

**Tasks**:
- Install @langchain/langgraph dependency
- Create LangGraph orchestrator service
- Implement DAG builder from analyst config
- Implement DAG executor with LangGraph
- Add observer node integration
- Update server to use LangGraph orchestrator
- Add integration tests

**Success Criteria**:
- LangGraph orchestrator builds DAGs from analyst configs
- DAGs execute successfully
- Observer node receives results
- Integration tests pass

---

#### **Phase 4: Configuration and Testing (Week 7-8)**

**Droid Class**: **Configuration Droid**

**Mission**: Create sample analyst configurations and test with existing analysts.

**Tasks**:
- Create sample analyst configurations
- Test with existing analysts
- Test parallel enrichment
- Test conditional enrichment
- Update documentation
- Create migration guide

**Success Criteria**:
- Sample configurations work with all analysts
- Parallel enrichment works correctly
- Conditional enrichment works correctly
- Documentation is comprehensive
- Migration guide is clear

---

#### **Phase 5: Migration (Week 9-10)**

**Droid Class**: **Migration Droid**

**Mission**: Ensure backward compatibility and provide migration tools.

**Tasks**:
- Ensure existing analysts work with new system
- Provide migration guide for analysts
- Support both DAG modes (fixed and flexible)
- Add deprecation warnings for old fixed DAG
- Create migration tools
- Test migration process

**Success Criteria**:
- Existing analysts work with new system
- Migration guide is clear and comprehensive
- Both DAG modes work correctly
- Migration tools work correctly
- Migration process is tested

---

#### **Phase 6: Production Rollout (Week 11-12)**

**Droid Class**: **Production Droid**

**Mission**: Gradual rollout to production with monitoring and feedback.

**Tasks**:
- Gradual rollout to select analysts
- Monitor performance and costs
- Gather feedback and iterate
- Update documentation and training
- Create monitoring dashboards
- Set up alerts for performance issues

**Success Criteria**:
- Gradual rollout is successful
- Performance is acceptable
- Costs are within budget
- Feedback is positive
- Documentation is up-to-date
- Monitoring dashboards are functional

---

### 2.4 Droid Governance and Safety

#### **Droid Charter Compliance**

All droids must comply with the AFI Droid Charter ([`AFI_DROID_CHARTER.v0.1.md`](afi-config/codex/governance/droids/AFI_DROID_CHARTER.v0.1.md)):

**Global Operating Principles**:
1. **Propose, Don't Decide**: Droids propose changes via branches and PRs; humans make final decisions
2. **Least Surprise**: Preserve existing behavior unless explicitly instructed to change
3. **Small, Reversible Deltas**: Keep changes small, focused, and atomic
4. **Safety First**: Never touch secrets, credentials, or deployment keys
5. **Respect Boundaries**: Each repo's AGENTS.md is a fence line
6. **Traceability & Clarity**: Use clear commit messages and PR descriptions
7. **No Naming Drift**: Respect established names and architecture

**Repo-Class Boundaries**:

**afi-config (Config Layer)**:
- ✅ May: Add new JSON Schemas, templates, and examples
- ✅ May: Extend existing schemas in an additive, backward-compatible way
- ✅ May: Add or update tests and validation utilities
- ❌ May not: Change the meaning of existing fields without human design and version bump
- ❌ May not: Remove schemas in active use without explicit deprecation plan

**afi-factory (Factory & Starters)**:
- ✅ May: Add or refine droid manifests, tasks, recipes, and starter templates
- ✅ May: Propose new starter projects for AFI-compatible apps, agents, or bots
- ✅ Must: Keep manifests honest about what each droid is allowed to touch
- ✅ Must: Align droid roles with this Charter and per-repo AGENTS.md files
- ❌ May not: Declare droids as allowed to operate outside the boundaries defined by this Charter

**afi-reactor (Orchestrator Layer)**:
- ✅ May: Add new DAG nodes, simulations, or tests that are clearly additive
- ✅ May: Improve logging, observability, and Codex replay artifacts
- ✅ Must: Respect the AFI Orchestrator Doctrine
- ✅ Must: Treat the DAG as the canonical expression of orchestration
- ❌ May not: Rename or remove existing DAG nodes or edges without explicit instruction
- ❌ May not: Introduce tokenomics logic; emissions and rewards belong in token repos

---

#### **Droid Playbook Compliance**

All droids must follow the AFI Droid Playbook ([`AFI_DROID_PLAYBOOK.v0.1.md`](afi-config/codex/governance/droids/AFI_DROID_PLAYBOOK.v0.1.md)):

**Standard Droid Workflow**:
1. **Read instructions**: Load the Droid Charter and the repo's AGENTS.md
2. **Restate the mission**: Summarize the requested change in its own words
3. **Scan before editing**: Identify relevant directories and existing patterns
4. **Plan a minimal diff**: Prefer small, focused changes
5. **Edit with guardrails**: Follow repo conventions for file layout, naming, imports
6. **Run local checks**: Use commands defined in AGENTS.md
7. **Summarize changes**: Explain what was changed and why
8. **Prepare commits/PRs**: Follow the repo's commit style guidelines

**Multi-Repo Missions**:
1. **Declare all repos up front**: Explicitly list the repos involved and their roles
2. **Read AGENTS.md for each repo**: Confirm that each repo allows multi-repo changes
3. **Respect dependency direction**: Never invert established relationships
4. **Keep diffs localized**: Each repo's changes should make sense in isolation

---

### 2.5 Droid Success Metrics

**Overall Success Metrics**:
- All droids comply with Droid Charter and Playbook
- All droid changes are proposed via branches and PRs
- All droid changes are small, focused, and atomic
- All droid changes have clear documentation
- All droid changes have comprehensive tests
- All droid changes are reversible

**Phase-Specific Success Metrics**:

**Phase 1: Foundation**:
- All schemas are valid JSON Schema Draft 7+
- All schemas have comprehensive documentation
- All schemas have validation tests
- Example configurations validate successfully

**Phase 2: Plugin System**:
- All plugins implement LangGraphNode interface
- All plugins have comprehensive tests
- All plugins have clear documentation
- Plugin registry loads all plugins successfully

**Phase 3: Orchestrator**:
- LangGraph orchestrator builds DAGs from analyst configs
- DAGs execute successfully
- Observer node receives results
- Integration tests pass

**Phase 4: Configuration and Testing**:
- Sample configurations work with all analysts
- Parallel enrichment works correctly
- Conditional enrichment works correctly
- Documentation is comprehensive
- Migration guide is clear

**Phase 5: Migration**:
- Existing analysts work with new system
- Migration guide is clear and comprehensive
- Both DAG modes work correctly
- Migration tools work correctly
- Migration process is tested

**Phase 6: Production Rollout**:
- Gradual rollout is successful
- Performance is acceptable
- Costs are within budget
- Feedback is positive
- Documentation is up-to-date
- Monitoring dashboards are functional

---

## Conclusion

### Configuration Architecture Summary

The proposed configuration architecture maintains a clear separation of concerns:

- **afi-config** defines **schemas** (WHAT configurations look like)
- **afi-factory** stores **runtime configurations** (HOW agents are configured)
- **afi-reactor** reads configurations and builds DAGs (HOW DAGs are executed)

This separation ensures:
- **afi-config** remains schema-focused and foundational
- **afi-factory** remains template-focused and agent-specific
- **afi-reactor** remains orchestration-focused and execution-oriented

### Droid Mitigation Summary

Droids can be deployed as a **proactive mitigation strategy** for each risk identified in the LangGraph flexible DAG analysis:

1. **Complexity Increase**: Documentation Droid maintains comprehensive documentation
2. **Learning Curve**: Training Droid creates comprehensive training materials
3. **Performance**: Performance Droid monitors and optimizes performance
4. **Configuration Errors**: Validation Droid provides comprehensive validation tools

All droids must comply with the AFI Droid Charter and Playbook, ensuring:
- Changes are proposed, not decided
- Changes are small, focused, and atomic
- Changes respect repo boundaries
- Changes are traceable and clear

This approach provides a **systematic, automated way** to mitigate risks while maintaining architectural integrity and governance. 🎯