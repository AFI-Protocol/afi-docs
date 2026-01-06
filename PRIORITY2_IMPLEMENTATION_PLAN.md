# Priority 2 Implementation Plan for AGENTS.md

**Date**: 2025-12-31
**Status**: Planning Phase
**Scope**: Priority 2 (HIGH) tasks from AGENTS_AUDIT_REPORT.md

---

## Executive Summary

This plan addresses Priority 2 (HIGH) tasks from the AGENTS_AUDIT_REPORT.md audit report. These tasks build upon the completed Priority 1 (CRITICAL) updates to ensure comprehensive documentation alignment with the current afi-reactor codebase.

**Priority 2 Tasks**:
1. Update Pipeline Description (Line 34-36)
2. Add afi-gateway Integration Section
3. Add Agent Registry Section

**Context**: Priority 1 tasks have been completed, including:
- Directory structure corrections
- Flexible DAG architecture documentation
- Node types documentation
- Build and test commands updates

---

## Comprehensive Audit Report Review

### Current State Analysis

**Completed Priority 1 Changes**:
- ✅ Directory structure updated (src/dags/ → src/dag/)
- ✅ All documented directories added (state/, aiMl/, adapters/, collectors/, core/, cpj/, enrichment/, indicator/, news/, novelty/, services/, uss/, utils/)
- ✅ Flexible DAG architecture section added (DAGBuilder, DAGExecutor, PluginRegistry, StateManager, MLProviderRegistry)
- ✅ Node types section added (AnalystNode, ExecutionNode, ObserverNode, and plugin nodes)
- ✅ Pipeline description updated to "flexible, plugin-based DAG pipeline"
- ✅ afi-gateway integration section added
- ✅ Build and test commands updated

**Remaining Priority 2 Tasks**:

#### Task 1: Update Pipeline Description (Line 34-36)
**Current State**: Already updated in Priority 1
**Status**: ✅ COMPLETED
**Action**: No additional action needed - this was addressed in Priority 1

#### Task 2: Add afi-gateway Integration Section
**Current State**: Already added in Priority 1
**Status**: ✅ COMPLETED
**Action**: No additional action needed - this was addressed in Priority 1

#### Task 3: Add Agent Registry Section
**Current State**: NOT YET IMPLEMENTED
**Status**: ⏳ PENDING
**Action**: This is the primary remaining Priority 2 task

### Architectural Drift Prevention

**Risk Assessment**: With Priority 1 changes complete, there is a risk of architectural drift if Priority 2 tasks are not implemented consistently with the same level of detail and accuracy.

**Mitigation Strategy**:
1. Maintain consistency with Priority 1 documentation style
2. Ensure all new sections reference existing Priority 1 content
3. Cross-reference with actual codebase implementations
4. Validate against audit report requirements before completion

---

## Priority 2 Task Analysis

### Task 3: Add Agent Registry Section

**Audit Report Requirement** (Issue 8.1):
```markdown
#### Issue 8.1: No Reference to Agent Registries

**What's Missing**:
- **agent.registry.json** - Registry of available agents
- **execution-agent.registry.json** - Registry of execution agents
- **agents.codex.json** - Codex metadata for agents

**Current AGENTS.md Coverage**: None

**Impact**: MEDIUM - Agent registries are not documented, making it unclear how agents are discovered and registered.

**Evidence from config directory**:
```json
// From afi-reactor/config/agent.registry.json
{
  "agents": [
    {
      "id": "froggy-analyst-node",
      "name": "Froggy Analyst",
      "type": "analyzer",
      "plugin": "froggy.trend_pullback_v1",
      "agentReady": true
    }
  ]
}
```

**Action Required**: Add section describing agent registry system and how agents are registered.
```

**Codebase Evidence**:

From [`afi-reactor/config/agent.registry.json`](afi-reactor/config/agent.registry.json):
- Contains agent definitions with fields: agentName, entry, strategy, version, description, enabled, tags
- Currently has 1 agent: "signal-agent" (stub strategy)

From [`afi-reactor/config/execution-agent.registry.json`](afi-reactor/config/execution-agent.registry.json):
- Contains execution agent configurations
- Three execution agents: binance-local, coinbase-remote, paper-sim
- Each has: type, auth, entry, description, mode, environment

From [`afi-reactor/config/agents.codex.json`](afi-reactor/config/agents.codex.json):
- Contains comprehensive agent metadata
- 12 agents defined with: agentId, linkedNodes, description, maintainer, agentReady, status, role, capabilities, version
- Agent types include: generators, analyzers, scorers, validators, persisters, executors, observers

**Key Fields**:
- `agentId`: Unique identifier for the agent
- `linkedNodes`: Array of node IDs this agent connects to
- `description`: Human-readable description of agent's purpose
- `maintainer`: Repository or team responsible for agent
- `agentReady`: Boolean flag indicating if agent is ready for production use
- `status`: Current status (active, deprecated, etc.)
- `role`: Functional role (generator, analyzer, scorer, validator, persister, executor, observer)
- `capabilities`: Array of capabilities the agent provides
- `version`: Semantic version of agent implementation

---

## Implementation Strategy

### Section Placement

**Insert Location**: After "afi-gateway Integration" section (approximately line 197)

**Rationale**: This placement follows the logical flow of the document:
1. Architecture Overview
2. Flexible DAG Architecture
3. Node Types
4. afi-gateway Integration
5. **Agent Registry** ← NEW SECTION HERE
6. Build and Test Commands
7. Security
8. Git Workflows
9. Conventions & Patterns
10. ESM Invariants
11. Scope & Boundaries for Agents

### Content Structure

The Agent Registry section should include:

1. **Overview**: Purpose of agent registry system
2. **Registry Files**: Description of each registry file
3. **Agent Metadata**: Explanation of key fields (agentId, linkedNodes, agentReady, etc.)
4. **Agent Roles**: Description of different agent roles (generator, analyzer, scorer, validator, persister, executor, observer)
5. **Agent Discovery**: How agents are discovered and loaded
6. **Agent Registration**: How new agents are registered
7. **agentReady Flag**: Purpose and usage
8. **Integration with DAG**: How agents connect to DAG nodes
9. **Examples**: Concrete examples from agents.codex.json

### Dependencies

**No Code Changes Required**: This is documentation-only task
**Cross-References**: Should reference existing sections (Flexible DAG Architecture, Node Types) for consistency
**Validation**: Must align with actual registry file structures

---

## Detailed Implementation Plan

### Step 1: Create Agent Registry Section

**Content to Add**:

```markdown
## Agent Registry

afi-reactor uses a registry system to manage agent configurations and their integration with the DAG pipeline. The registry enables dynamic agent discovery, registration, and lifecycle management.

### Registry Files

#### agent.registry.json
Located in `config/agent.registry.json`, this registry contains agent definitions for signal generation and analysis.

**Structure**:
```json
{
  "agents": [
    {
      "agentName": "signal-agent",
      "entry": "tools/agents/signal-agent.ts",
      "strategy": "mean-reversion",
      "version": "0.1.0",
      "description": "A stub strategy simulating mean-reversion behavior.",
      "enabled": true,
      "tags": ["stub", "strategy", "demo"]
    }
  ]
}
```

**Purpose**: Defines available signal agents and their entry points.

#### execution-agent.registry.json
Located in `config/execution-agent.registry.json`, this registry contains execution agent configurations for trade execution.

**Structure**:
```json
{
  "binance-local": {
    "type": "local",
    "auth": "env",
    "entry": "tools/execution/binance-local.ts",
    "description": "Direct Binance API execution using local environment variables.",
    "mode": "simulated",
    "environment": "dev"
  },
  "coinbase-remote": {
    "type": "remote",
    "auth": "injected",
    "entry": "tools/execution/coinbase-remote.ts",
    "description": "Remote execution via secure agent, credentials injected at runtime.",
    "mode": "simulated",
    "environment": "dev"
  },
  "paper-sim": {
    "type": "simulated",
    "auth": "none",
    "entry": "tools/execution/paper-sim.ts",
    "description": "Simulation agent for testing execution logic without real orders.",
    "mode": "simulated",
    "environment": "dev"
  }
}
```

**Purpose**: Defines available execution agents and their authentication methods.

#### agents.codex.json
Located in `config/agents.codex.json`, this registry contains comprehensive metadata for all agents in the AFI ecosystem.

**Structure**:
```json
[
  {
    "agentId": "MarketDataAgentV1",
    "linkedNodes": ["market-data-streamer"],
    "description": "Streams real-time market prices, OHLCV, and order books from multiple exchanges",
    "maintainer": "augmentcode",
    "agentReady": true,
    "status": "active",
    "role": "generator",
    "capabilities": ["price-streaming", "orderbook-analysis", "volume-tracking"],
    "version": "1.0.0"
  }
]
```

**Purpose**: Provides canonical metadata for agents, including their capabilities, roles, and integration points.

### Agent Metadata Fields

**Key Fields**:

- **agentId**: Unique identifier for the agent (e.g., "MarketDataAgentV1", "FroggyAnalystNode")
- **linkedNodes**: Array of DAG node IDs this agent connects to (e.g., ["market-data-streamer"], ["technical-indicators", "pattern-recognition"])
- **description**: Human-readable description of the agent's purpose and functionality
- **maintainer**: Repository or team responsible for maintaining the agent
- **agentReady**: Boolean flag indicating if the agent is ready for production use
- **status**: Current status of the agent (active, deprecated, experimental)
- **role**: Functional role in the pipeline:
  - **generator**: Produces signals or data (e.g., MarketDataAgent, OnchainFeedAgent, SocialSignalAgent, NewsFeedAgent, AIStrategyAgent)
  - **analyzer**: Analyzes signals or data (e.g., TechnicalAnalysisAgent, PatternRecognitionAgent, SentimentAnalysisAgent, NewsEventAgent, AIEnsembleAgent)
  - **scorer**: Assigns scores to signals (e.g., augmentcode)
  - **validator**: Validates signals (e.g., factory.droid)
  - **persister**: Persists signals (e.g., scarlet)
  - **executor**: Executes trades (e.g., ExchangeExecutionAgent)
  - **observer**: Observes and logs results (e.g., TelemetryAgent)
- **capabilities**: Array of capabilities the agent provides (e.g., ["price-streaming", "technical-indicators", "trade-execution"])
- **version**: Semantic version of the agent implementation

### Agent Roles

#### Generator Agents
Produce signals or data for the pipeline:

- **MarketDataAgentV1**: Streams real-time market prices, OHLCV, and order books
- **OnchainFeedAgentV1**: Ingests blockchain events and DeFi protocol data
- **SocialSignalAgentV1**: Collects Twitter, Discord, and social sentiment signals
- **NewsFeedAgentV1**: Parses financial news and RSS feeds for breaking events
- **AIStrategyAgentV1**: Generates candidate trading signals using AI models

#### Analyzer Agents
Analyze signals or data:

- **TechnicalAnalysisAgentV1**: Runs MACD, RSI, Bollinger, and other TA indicators
- **PatternRecognitionAgentV1**: Detects price action setups and chart patterns
- **SentimentAnalysisAgentV1**: Scores market and social sentiment for bias detection
- **NewsEventAgentV1**: Evaluates market impact of news and events
- **AIEnsembleAgentV1**: Aggregates multiple analyses into a final weighted score

#### Scorer Agents
Assign scores to signals:

- **augmentcode**: Handles ensemble-based signal scoring using PoI and PoInsight balancing

#### Validator Agents
Validate signals:

- **factory.droid**: Handles DAO quorum verification and checkpoint validation

#### Persister Agents
Persist signals:

- **scarlet**: Manages MongoDB T.S.S.D. Vault persistence of approved signals

#### Executor Agents
Execute trades:

- **ExchangeExecutionAgentV1**: Executes trades via exchanges with risk controls

#### Observer Agents
Observe and log results:

- **TelemetryAgentV1**: Logs all signals, scores, and execution results to T.S.S.D. vault

### Agent Discovery and Registration

**Discovery Process**:
1. Registry files are loaded at startup from `config/` directory
2. Agent metadata is parsed and validated
3. Agents are indexed by `agentId` for fast lookup
4. Agents with `agentReady: true` are marked as available for production use

**Registration Process**:
1. New agents are added to registry files
2. Agent metadata is validated against schema
3. `agentReady` flag is set to `false` for new agents until testing is complete
4. Once tested and validated, `agentReady` is set to `true`
5. Registry is reloaded to pick up new agents

### agentReady Flag

**Purpose**: The `agentReady` flag indicates whether an agent is ready for production use.

**Usage**:
- **true**: Agent has been tested, validated, and is ready for production deployment
- **false**: Agent is under development, testing, or not yet validated

**Lifecycle**:
1. Development: `agentReady: false`
2. Testing: `agentReady: false` (during testing)
3. Validation: `agentReady: false` (during validation)
4. Production: `agentReady: true` (after successful validation)

### Integration with DAG

Agents integrate with the DAG pipeline through their `linkedNodes` field:

1. **Generator Agents**: Connect to ingress nodes (e.g., ScoutNode, SignalIngressNode)
2. **Analyzer Agents**: Connect to enrichment nodes (e.g., TechnicalIndicatorsNode, PatternRecognitionNode, SentimentNode, NewsNode, AiMlNode)
3. **Scorer Agents**: Connect to AnalystNode for final scoring
4. **Validator Agents**: Connect to validation nodes in the DAG
5. **Persister Agents**: Connect to persistence nodes (e.g., TSSD Vault)
6. **Executor Agents**: Connect to ExecutionNode for trade execution
7. **Observer Agents**: Connect to ObserverNode for logging and telemetry

**Example Integration**:
```json
{
  "agentId": "TechnicalAnalysisAgentV1",
  "linkedNodes": ["technical-indicators"],
  "description": "Runs MACD, RSI, Bollinger, and other TA indicators",
  "maintainer": "augmentcode",
  "agentReady": true,
  "status": "active",
  "role": "analyzer",
  "capabilities": ["technical-indicators", "trend-analysis", "support-resistance"],
  "version": "1.0.0"
}
```

This agent connects to the `TechnicalIndicatorsNode` plugin in the DAG, providing technical indicator enrichment for signals.

### Examples

**Example 1: Generator Agent**
```json
{
  "agentId": "MarketDataAgentV1",
  "linkedNodes": ["market-data-streamer"],
  "description": "Streams real-time market prices, OHLCV, and order books from multiple exchanges",
  "maintainer": "augmentcode",
  "agentReady": true,
  "status": "active",
  "role": "generator",
  "capabilities": ["price-streaming", "orderbook-analysis", "volume-tracking"],
  "version": "1.0.0"
}
```

**Example 2: Analyzer Agent**
```json
{
  "agentId": "TechnicalAnalysisAgentV1",
  "linkedNodes": ["technical-indicators"],
  "description": "Runs MACD, RSI, Bollinger, and other TA indicators",
  "maintainer": "augmentcode",
  "agentReady": true,
  "status": "active",
  "role": "analyzer",
  "capabilities": ["technical-indicators", "trend-analysis", "support-resistance"],
  "version": "1.0.0"
}
```

**Example 3: Scorer Agent**
```json
{
  "agentId": "augmentcode",
  "linkedNodes": ["afi-ensemble-score"],
  "description": "AugmentCode handles ensemble-based signal scoring using PoI and PoInsight balancing",
  "maintainer": "augmentcode",
  "agentReady": true,
  "status": "active",
  "role": "scorer",
  "capabilities": ["poi-scoring", "insight-balancing", "ensemble-validation"],
  "version": "1.0.0"
}
```

**Example 4: Validator Agent**
```json
{
  "agentId": "factory.droid",
  "linkedNodes": ["dao-mint-checkpoint"],
  "description": "Factory Droids handle DAO quorum verification and checkpoint validation",
  "maintainer": "factory.droid",
  "agentReady": true,
  "status": "active",
  "role": "validator",
  "capabilities": ["dao-consensus", "quorum-verification", "mint-eligibility"],
  "version": "1.0.0"
}
```

**Example 5: Persister Agent**
```json
{
  "agentId": "scarlet",
  "linkedNodes": ["tssd-vault-persist"],
  "description": "Scarlet manages MongoDB T.S.S.D. Vault persistence of approved signals",
  "maintainer": "Scarlet",
  "agentReady": true,
  "status": "active",
  "role": "persister",
  "capabilities": ["vault-storage", "data-persistence", "signal-archival"],
  "version": "1.0.0"
}
```

**Example 6: Executor Agent**
```json
{
  "agentId": "ExchangeExecutionAgentV1",
  "linkedNodes": ["exchange-execution-node"],
  "description": "Executes trades via exchanges with risk controls and position management",
  "maintainer": "augmentcode",
  "agentReady": true,
  "status": "active",
  "role": "executor",
  "capabilities": ["trade-execution", "risk-management", "position-sizing"],
  "version": "1.0.0"
}
```

**Example 7: Observer Agent**
```json
{
  "agentId": "TelemetryAgentV1",
  "linkedNodes": ["telemetry-log-node"],
  "description": "Logs all signals, scores, and execution results to T.S.S.D. vault for monitoring",
  "maintainer": "Scarlet",
  "agentReady": true,
  "status": "active",
  "role": "observer",
  "capabilities": ["telemetry-logging", "performance-monitoring", "data-analytics"],
  "version": "1.0.0"
}
```

### Best Practices

**For Contributors**:
1. When adding a new agent, update the appropriate registry file
2. Set `agentReady: false` during development and testing
3. Set `agentReady: true` only after thorough testing and validation
4. Provide clear descriptions and capabilities
5. Specify the correct `linkedNodes` for DAG integration
6. Use semantic versioning for `version` field
7. Tag agents appropriately (e.g., "stub", "strategy", "demo")

**For Maintainers**:
1. Review agent registry changes in pull requests
2. Validate agent metadata against schema
3. Test agent integration with DAG before setting `agentReady: true`
4. Monitor agent performance and status
5. Update agent status as needed (active, deprecated, etc.)

### Related Documentation

- [Flexible DAG Architecture](#flexible-dag-architecture) - How DAG nodes are composed and executed
- [Node Types](#node-types) - Core nodes and plugin nodes in the DAG
- [afi-gateway Integration](#afi-gateway-integration) - ElizaOS agent integration
- [AFI Orchestrator Doctrine](../AFI_ORCHESTRATOR_DOCTRINE.md) - Guidelines for agent behavior
```

---

## Execution Approach

### Phase 1: Planning (Current Phase)
- [x] Review audit report Priority 2 requirements
- [x] Analyze agent registry files
- [x] Assess dependencies on existing codebase
- [x] Generate detailed implementation strategy
- [x] Create structured approach for execution

### Phase 2: Implementation (Next Phase)
- [ ] Add Agent Registry section to AGENTS.md
- [ ] Validate section placement and formatting
- [ ] Cross-reference with existing sections
- [ ] Ensure consistency with Priority 1 documentation style
- [ ] Verify all examples match actual registry files

### Phase 3: Validation
- [ ] Review completed section against audit report requirements
- [ ] Verify all registry files are accurately documented
- [ ] Check for consistency with codebase
- [ ] Validate markdown formatting and structure

### Phase 4: Completion
- [ ] Update todo list to mark Priority 2 tasks as complete
- [ ] Provide completion summary

---

## Risk Assessment

**Low Risk**: This is a documentation-only task with no code changes required.

**Mitigation**:
- All content is based on existing registry files
- No architectural changes required
- Can be easily validated and corrected if needed

---

## Success Criteria

The Agent Registry section will be considered complete when:

1. ✅ Section is added to AGENTS.md at the correct location
2. ✅ All three registry files are documented (agent.registry.json, execution-agent.registry.json, agents.codex.json)
3. ✅ Agent metadata fields are explained (agentId, linkedNodes, agentReady, status, role, capabilities, version)
4. ✅ Agent roles are described (generator, analyzer, scorer, validator, persister, executor, observer)
5. ✅ agentReady flag purpose and lifecycle are documented
6. ✅ Integration with DAG is explained
7. ✅ Concrete examples from agents.codex.json are provided
8. ✅ Best practices for contributors and maintainers are included
9. ✅ Section cross-references existing documentation sections
10. ✅ Content is validated against audit report requirements

---

## Next Steps

Once this plan is approved, the implementation will proceed in Code mode to:

1. Add the Agent Registry section to [`afi-reactor/AGENTS.md`](afi-reactor/AGENTS.md)
2. Validate the implementation against this plan
3. Provide completion summary

---

**Plan Created**: 2025-12-31
**Status**: Ready for Implementation
**Estimated Complexity**: Low (documentation-only task)
