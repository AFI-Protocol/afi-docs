> **Historical note:** This document describes a superseded LangGraph-era architecture plan. AFI Reactor now uses a custom deterministic TypeScript DAG under `afi-reactor/src/dag/`. This file is retained only for historical context and should not be treated as current implementation guidance.
>

# AFI-Reactor: LangGraph Integration - Part 1 Implementation Plan

## Executive Summary

This document provides a comprehensive implementation plan for Part 1 of the AFI-Reactor LangGraph integration, synthesizing architectural insights from [`AFI_REACTOR_LANGGRAPH_FLEXIBLE_DAG_ANALYSIS.md`](AFI_REACTOR_LANGGRAPH_FLEXIBLE_DAG_ANALYSIS.md) and [`AFI_REACTOR_CONFIG_ARCHITECTURE_AND_DROID_MITIGATION.md`](AFI_REACTOR_CONFIG_ARCHITECTURE_AND_DROID_MITIGATION.md).

**Part 1 Scope**: Foundation layer - schemas, configuration infrastructure, and TypeScript interfaces that bridge [`afi-factory`](afi-factory/) and [`afi-config`](afi-config/) repositories.

**Part 2 Scope** (Future): LangGraph orchestrator, plugin system, and DAG execution (will be addressed in separate implementation plan).

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [TypeScript Interfaces](#typescript-interfaces)
3. [Node Logic Specifications](#node-logic-specifications)
4. [State Management Mechanisms](#state-management-mechanisms)
5. [Repository Bridge Design](#repository-bridge-design)
6. [Droid Mitigation Integration](#droid-mitigation-integration)
7. [Implementation Phases](#implementation-phases)
8. [Testing Strategy](#testing-strategy)
9. [Success Criteria](#success-criteria)

---

## 1. Architecture Overview

### 1.1 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    AFI-Reactor LangGraph System                  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  afi-config (Schema Layer)                                   │  │
│  │  • analyst-config.schema.json                                │  │
│  │  • enrichment-node.schema.json                               │  │
│  │  • pipeline.schema.json (updated)                            │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                              ↓                                    │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  afi-factory (Template Layer)                                │  │
│  │  • analyst-configs/ (runtime configurations)                 │  │
│  │  • schemas/index.ts (TypeScript types)                       │  │
│  │  • template_registry.ts (updated)                            │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                              ↓                                    │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  afi-reactor (Orchestration Layer)                           │  │
│  │  • src/langgraph/ (AFI DAG integration)                      │  │
│  │  • src/types/ (TypeScript interfaces)                        │  │
│  │  • src/state/ (State management)                             │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                              ↓                                    │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  afi-core (Runtime Layer)                                    │  │
│  │  • src/langgraph/ (AFI DAG signal envelope)                  │  │
│  │  • src/analysts/ (Analyst score template extensions)         │  │
│  └──────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Data Flow

```
Analyst Configuration (afi-factory)
    ↓
Validated against Schema (afi-config)
    ↓
Loaded by Template Registry (afi-factory)
    ↓
Consumed by AFI DAG Orchestrator (afi-reactor)
    ↓
Builds DAG with Required + Optional Nodes
    ↓
Executes DAG with State Management (afi-reactor)
    ↓
Returns Scored Signal (afi-core)
```

### 1.3 Key Design Principles

1. **Separation of Concerns**: Each repository has a clear, focused responsibility
2. **Type Safety**: All interfaces are strongly typed with TypeScript
3. **Validation**: All configurations are validated against schemas
4. **Backward Compatibility**: Existing analysts continue to work
5. **Incremental Migration**: New system is opt-in, not breaking

---

## 2. TypeScript Interfaces

### 2.1 afi-config Schema Interfaces

**Location**: [`afi-config/schemas/analyst-config.schema.json`](afi-config/schemas/analyst-config.schema.json)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://afi-protocol.org/schemas/analyst-config.schema.json",
  "title": "Analyst Configuration Schema",
  "description": "Schema for analyst-specific enrichment node configurations",
  "type": "object",
  "required": ["analystId", "enrichmentNodes"],
  "properties": {
    "analystId": {
      "type": "string",
      "description": "Unique identifier for the analyst",
      "pattern": "^[a-z0-9-]+$"
    },
    "version": {
      "type": "string",
      "description": "Configuration version",
      "pattern": "^v\\d+\\.\\d+\\.\\d+$"
    },
    "enrichmentNodes": {
      "type": "array",
      "description": "Array of enrichment node configurations",
      "items": {
        "$ref": "https://afi-protocol.org/schemas/definitions/enrichment-node.schema.json"
      }
    },
    "metadata": {
      "type": "object",
      "description": "Optional metadata about the configuration",
      "properties": {
        "description": {
          "type": "string",
          "description": "Human-readable description of the configuration"
        },
        "author": {
          "type": "string",
          "description": "Author of the configuration"
        },
        "createdAt": {
          "type": "string",
          "format": "date-time",
          "description": "Creation timestamp"
        },
        "updatedAt": {
          "type": "string",
          "format": "date-time",
          "description": "Last update timestamp"
        }
      }
    }
  }
}
```

**Location**: [`afi-config/schemas/definitions/enrichment-node.schema.json`](afi-config/schemas/definitions/enrichment-node.schema.json)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://afi-protocol.org/schemas/definitions/enrichment-node.schema.json",
  "title": "Enrichment Node Definition",
  "description": "Schema for enrichment node configuration",
  "type": "object",
  "required": ["id", "type", "plugin", "enabled"],
  "properties": {
    "id": {
      "type": "string",
      "description": "Unique identifier for the enrichment node",
      "pattern": "^[a-z0-9-]+$"
    },
    "type": {
      "type": "string",
      "enum": ["enrichment", "ingress"],
      "description": "Type of node"
    },
    "plugin": {
      "type": "string",
      "description": "LangGraph plugin ID",
      "pattern": "^[a-z0-9-]+$"
    },
    "enabled": {
      "type": "boolean",
      "description": "Whether this node is enabled"
    },
    "optional": {
      "type": "boolean",
      "description": "Whether this node is optional (default: true)",
      "default": true
    },
    "parallel": {
      "type": "boolean",
      "description": "Whether this node can run in parallel with others (default: false)",
      "default": false
    },
    "dependencies": {
      "type": "array",
      "description": "IDs of nodes this node depends on",
      "items": {
        "type": "string",
        "pattern": "^[a-z0-9-]+$"
      },
      "uniqueItems": true
    },
    "config": {
      "type": "object",
      "description": "Node-specific configuration",
      "additionalProperties": true
    }
  }
}
```

**Location**: [`afi-config/schemas/pipeline.schema.json`](afi-config/schemas/pipeline.schema.json) (updated)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://afi-protocol.org/schemas/pipeline.schema.json",
  "title": "Pipeline Configuration Schema",
  "description": "Schema for pipeline and DAG configuration",
  "type": "object",
  "required": ["requiredNodes", "enrichmentNodes"],
  "properties": {
    "requiredNodes": {
      "type": "array",
      "description": "Required nodes that are always present in the DAG",
      "items": {
        "type": "string",
        "enum": ["analyst", "execution", "observer"]
      },
      "uniqueItems": true
    },
    "enrichmentNodes": {
      "type": "object",
      "description": "Available enrichment nodes (analyst-configurable)",
      "additionalProperties": {
        "$ref": "https://afi-protocol.org/schemas/definitions/enrichment-node.schema.json"
      }
    },
    "version": {
      "type": "string",
      "description": "Pipeline configuration version",
      "pattern": "^v\\d+\\.\\d+\\.\\d+$"
    }
  }
}
```

---

### 2.2 afi-factory TypeScript Interfaces

**Location**: [`afi-factory/schemas/index.ts`](afi-factory/schemas/index.ts)

```typescript
/**
 * AFI Factory - Analyst Configuration Types
 * 
 * This file defines TypeScript interfaces for analyst configurations,
 * bridging afi-config schemas with afi-reactor orchestration.
 */

/**
 * Enrichment node configuration
 */
export interface EnrichmentNodeConfig {
  /** Unique identifier for the enrichment node */
  id: string;
  
  /** Type of node */
  type: 'enrichment' | 'ingress';
  
  /** LangGraph plugin ID */
  plugin: string;
  
  /** Whether this node is enabled */
  enabled: boolean;
  
  /** Whether this node is optional (default: true) */
  optional?: boolean;
  
  /** Whether this node can run in parallel with others (default: false) */
  parallel?: boolean;
  
  /** IDs of nodes this node depends on */
  dependencies?: string[];
  
  /** Node-specific configuration */
  config?: Record<string, unknown>;
}

/**
 * Analyst configuration metadata
 */
export interface AnalystConfigMetadata {
  /** Human-readable description of the configuration */
  description?: string;
  
  /** Author of the configuration */
  author?: string;
  
  /** Creation timestamp */
  createdAt?: string;
  
  /** Last update timestamp */
  updatedAt?: string;
}

/**
 * Analyst configuration
 */
export interface AnalystConfig {
  /** Unique identifier for the analyst */
  analystId: string;
  
  /** Configuration version */
  version?: string;
  
  /** Array of enrichment node configurations */
  enrichmentNodes: EnrichmentNodeConfig[];
  
  /** Optional metadata about the configuration */
  metadata?: AnalystConfigMetadata;
}

/**
 * Analyst configuration with validation result
 */
export interface ValidatedAnalystConfig extends AnalystConfig {
  /** Whether the configuration is valid */
  valid: boolean;
  
  /** Validation errors (if any) */
  errors?: string[];
  
  /** Validation warnings (if any) */
  warnings?: string[];
}

/**
 * Template registry entry
 */
export interface TemplateRegistryEntry {
  /** Template ID */
  id: string;
  
  /** Template type */
  type: 'analyst-config' | 'enrichment-node' | 'plugin';
  
  /** Template path */
  path: string;
  
  /** Schema ID for validation */
  schemaId?: string;
  
  /** Template version */
  version?: string;
}

/**
 * Load options for analyst configuration
 */
export interface LoadAnalystConfigOptions {
  /** Whether to validate against schema (default: true) */
  validate?: boolean;
  
  /** Whether to cache the result (default: true) */
  cache?: boolean;
  
  /** Custom configuration directory */
  configDir?: string;
}
```

---

### 2.3 afi-reactor TypeScript Interfaces

**Location**: [`afi-reactor/src/types/langgraph.ts`](afi-reactor/src/types/langgraph.ts)

```typescript
/**
 * AFI Reactor - AFI DAG Types
 *
 * This file defines TypeScript interfaces for AFI DAG integration,
 * bridging afi-factory configurations with AFI DAG orchestration.
 */

import type { AnalystConfig, EnrichmentNodeConfig } from 'afi-factory';

/**
 * AFI DAG node interface
 */
export interface AFIDAGNode {
  /** Node ID */
  id: string;
  
  /** Node type */
  type: 'required' | 'enrichment' | 'ingress';
  
  /** Plugin ID */
  plugin: string;
  
  /** Node execution function */
  execute: (state: AFIDAGState) => Promise<AFIDAGState>;
  
  /** Whether this node can run in parallel */
  parallel?: boolean;
  
  /** Node dependencies */
  dependencies?: string[];
}

/**
 * AFI DAG state interface
 */
export interface AFIDAGState {
  /** Signal ID */
  signalId: string;
  
  /** Raw signal data */
  rawSignal: unknown;
  
  /** Enrichment results (node ID -> result) */
  enrichmentResults: Map<string, unknown>;
  
  /** Analyst configuration */
  analystConfig: AnalystConfig;
  
  /** Current node being executed */
  currentNode?: string;
  
  /** Execution metadata */
  metadata: {
    /** Execution start time */
    startTime: string;
    
    /** Current node start time */
    currentNodeStartTime?: string;
    
    /** Execution trace */
    trace: ExecutionTraceEntry[];
  };
}

/**
 * Execution trace entry
 */
export interface ExecutionTraceEntry {
  /** Node ID */
  nodeId: string;
  
  /** Node type */
  nodeType: 'required' | 'enrichment' | 'ingress';
  
  /** Start time */
  startTime: string;
  
  /** End time */
  endTime?: string;
  
  /** Duration in milliseconds */
  duration?: number;
  
  /** Status */
  status: 'pending' | 'running' | 'completed' | 'failed';
  
  /** Error message (if failed) */
  error?: string;
}

/**
 * DAG configuration
 */
export interface DAGConfig {
  /** Required nodes */
  requiredNodes: string[];
  
  /** Enrichment nodes */
  enrichmentNodes: Map<string, EnrichmentNodeConfig>;
  
  /** DAG edges (from -> to) */
  edges: Map<string, string[]>;
}

/**
 * DAG build result
 */
export interface DAGBuildResult {
  /** Whether the DAG was built successfully */
  success: boolean;
  
  /** DAG configuration */
  config?: DAGConfig;
  
  /** Build errors (if any) */
  errors?: string[];
  
  /** Build warnings (if any) */
  warnings?: string[];
}

/**
 * DAG execution result
 */
export interface DAGExecutionResult {
  /** Whether the execution was successful */
  success: boolean;
  
  /** Final state */
  state?: AFIDAGState;
  
  /** Execution errors (if any) */
  errors?: string[];
  
  /** Execution warnings (if any) */
  warnings?: string[];
  
  /** Execution metrics */
  metrics: {
    /** Total execution time in milliseconds */
    totalTime: number;
    
    /** Number of nodes executed */
    nodesExecuted: number;
    
    /** Number of nodes failed */
    nodesFailed: number;
  };
}
```

---

### 2.4 afi-core TypeScript Interfaces

**Location**: [`afi-core/src/langgraph/AFIDAGSignalEnvelope.ts`](afi-core/src/langgraph/AFIDAGSignalEnvelope.ts)

```typescript
/**
 * AFI Core - AFI DAG Signal Envelope
 *
 * This file defines TypeScript interfaces for AFI DAG signal envelope,
 * extending the core signal schema with AFI DAG-specific metadata.
 */

/**
 * AFI DAG signal envelope
 */
export interface AFIDAGSignalEnvelope {
  /** Signal ID */
  signalId: string;
  
  /** Raw signal data */
  rawSignal: unknown;
  
  /** Enrichment results (node ID -> result) */
  enrichmentResults: Map<string, unknown>;
  
  /** Analyst configuration ID */
  analystConfigId: string;
  
  /** Envelope metadata */
  metadata: {
    /** Creation timestamp */
    createdAt: string;
    
    /** Last update timestamp */
    updatedAt: string;
    
    /** Enrichment nodes executed */
    enrichmentNodesExecuted: string[];
    
    /** Enrichment nodes skipped */
    enrichmentNodesSkipped: string[];
    
    /** Execution trace */
    executionTrace: ExecutionTraceEntry[];
  };
}

/**
 * Execution trace entry
 */
export interface ExecutionTraceEntry {
  /** Node ID */
  nodeId: string;
  
  /** Node type */
  nodeType: 'required' | 'enrichment' | 'ingress';
  
  /** Start time */
  startTime: string;
  
  /** End time */
  endTime?: string;
  
  /** Duration in milliseconds */
  duration?: number;
  
  /** Status */
  status: 'pending' | 'running' | 'completed' | 'failed';
  
  /** Error message (if failed) */
  error?: string;
}

/**
 * Enrichment result
 */
export interface EnrichmentResult {
  /** Node ID */
  nodeId: string;
  
  /** Result data */
  data: unknown;
  
  /** Result metadata */
  metadata: {
    /** Execution time in milliseconds */
    executionTime: number;
    
    /** Success flag */
    success: boolean;
    
    /** Error message (if failed) */
    error?: string;
  };
}
```

**Location**: [`afi-core/src/analysts/analyst-score-template.ts`](afi-core/src/analysts/analyst-score-template.ts) (extended)

```typescript
/**
 * AFI Core - Analyst Score Template (Extended)
 *
 * This file extends the analyst score template with AFI DAG configuration.
 */

/**
 * AFI DAG configuration for analyst score template
 */
export interface AFIDAGConfig {
  /** Enrichment nodes to use */
  enrichmentNodes: string[];
  
  /** Whether to enable parallel processing */
  parallelProcessing: boolean;
  
  /** Maximum parallel nodes */
  maxParallelNodes?: number;
  
  /** Timeout for enrichment nodes (in milliseconds) */
  enrichmentTimeout?: number;
}

/**
 * Analyst score template (extended with AFI DAG config)
 */
export interface AnalystScoreTemplate {
  /** UWR score */
  uwrScore: number;
  
  /** Confidence level */
  confidence: number;
  
  /** Signal ID */
  signalId: string;
  
  /** Analyst ID */
  analystId: string;
  
  /** Timestamp */
  timestamp: string;
  
  /** Optional AFI DAG configuration */
  langGraphConfig?: AFIDAGConfig;
  
  /** Optional enrichment results */
  enrichmentResults?: Map<string, unknown>;
}
```

---

## 3. Node Logic Specifications

### 3.1 Required Nodes

#### 3.1.1 Analyst Node

**Location**: [`afi-reactor/src/langgraph/nodes/AnalystNode.ts`](afi-reactor/src/langgraph/nodes/AnalystNode.ts)

```typescript
/**
 * Analyst Node - Required Node
 *
 * This node is responsible for:
 * - Loading the analyst configuration
 * - Initializing the enrichment pipeline
 * - Preparing the signal for enrichment
 */

import type { AFIDAGNode, AFIDAGState } from '../../types/langgraph';
import { loadAnalystConfig } from 'afi-factory/template_registry';

export class AnalystNode implements AFIDAGNode {
  id = 'analyst';
  type = 'required' as const;
  plugin = 'analyst';
  parallel = false;
  dependencies = [];

  async execute(state: AFIDAGState): Promise<AFIDAGState> {
    const startTime = Date.now();
    
    try {
      // Load analyst configuration
      const analystConfig = await loadAnalystConfig(state.analystConfig.analystId);
      
      // Update state with loaded configuration
      state.analystConfig = analystConfig;
      
      // Add trace entry
      state.metadata.trace.push({
        nodeId: this.id,
        nodeType: this.type,
        startTime: new Date(startTime).toISOString(),
        endTime: new Date().toISOString(),
        duration: Date.now() - startTime,
        status: 'completed',
      });
      
      return state;
    } catch (error) {
      // Add error trace entry
      state.metadata.trace.push({
        nodeId: this.id,
        nodeType: this.type,
        startTime: new Date(startTime).toISOString(),
        endTime: new Date().toISOString(),
        duration: Date.now() - startTime,
        status: 'failed',
        error: error instanceof Error ? error.message : String(error),
      });
      
      throw error;
    }
  }
}
```

#### 3.1.2 Execution Node

**Location**: [`afi-reactor/src/langgraph/nodes/ExecutionNode.ts`](afi-reactor/src/langgraph/nodes/ExecutionNode.ts)

```typescript
/**
 * Execution Node - Required Node
 *
 * This node is responsible for:
 * - Aggregating enrichment results
 * - Generating the final scored signal
 * - Preparing the signal for the observer
 */

import type { AFIDAGNode, AFIDAGState } from '../../types/langgraph';
import { generateScoredSignal } from 'afi-core';

export class ExecutionNode implements AFIDAGNode {
  id = 'execution';
  type = 'required' as const;
  plugin = 'execution';
  parallel = false;
  dependencies = [];

  async execute(state: AFIDAGState): Promise<AFIDAGState> {
    const startTime = Date.now();
    
    try {
      // Aggregate enrichment results
      const aggregatedResults = this.aggregateEnrichmentResults(state);
      
      // Generate scored signal
      const scoredSignal = await generateScoredSignal({
        signalId: state.signalId,
        rawSignal: state.rawSignal,
        enrichmentResults: aggregatedResults,
        analystConfig: state.analystConfig,
      });
      
      // Update state with scored signal
      state.enrichmentResults.set('scored-signal', scoredSignal);
      
      // Add trace entry
      state.metadata.trace.push({
        nodeId: this.id,
        nodeType: this.type,
        startTime: new Date(startTime).toISOString(),
        endTime: new Date().toISOString(),
        duration: Date.now() - startTime,
        status: 'completed',
      });
      
      return state;
    } catch (error) {
      // Add error trace entry
      state.metadata.trace.push({
        nodeId: this.id,
        nodeType: this.type,
        startTime: new Date(startTime).toISOString(),
        endTime: new Date().toISOString(),
        duration: Date.now() - startTime,
        status: 'failed',
        error: error instanceof Error ? error.message : String(error),
      });
      
      throw error;
    }
  }

  private aggregateEnrichmentResults(state: AFIDAGState): Map<string, unknown> {
    const aggregated = new Map<string, unknown>();
    
    for (const [nodeId, result] of state.enrichmentResults) {
      aggregated.set(nodeId, result);
    }
    
    return aggregated;
  }
}
```

#### 3.1.3 Observer Node

**Location**: [`afi-reactor/src/langgraph/nodes/ObserverNode.ts`](afi-reactor/src/langgraph/nodes/ObserverNode.ts)

```typescript
/**
 * Observer Node - Required Node
 *
 * This node is responsible for:
 * - Observing the final scored signal
 * - Logging execution metrics
 * - Publishing the signal to downstream consumers
 */

import type { AFIDAGNode, AFIDAGState } from '../../types/langgraph';
import { publishSignal } from 'afi-reactor/src/observers';

export class ObserverNode implements AFIDAGNode {
  id = 'observer';
  type = 'required' as const;
  plugin = 'observer';
  parallel = false;
  dependencies = [];

  async execute(state: AFIDAGState): Promise<AFIDAGState> {
    const startTime = Date.now();
    
    try {
      // Get scored signal
      const scoredSignal = state.enrichmentResults.get('scored-signal');
      
      if (!scoredSignal) {
        throw new Error('No scored signal found in state');
      }
      
      // Publish signal to downstream consumers
      await publishSignal(scoredSignal);
      
      // Log execution metrics
      this.logExecutionMetrics(state);
      
      // Add trace entry
      state.metadata.trace.push({
        nodeId: this.id,
        nodeType: this.type,
        startTime: new Date(startTime).toISOString(),
        endTime: new Date().toISOString(),
        duration: Date.now() - startTime,
        status: 'completed',
      });
      
      return state;
    } catch (error) {
      // Add error trace entry
      state.metadata.trace.push({
        nodeId: this.id,
        nodeType: this.type,
        startTime: new Date(startTime).toISOString(),
        endTime: new Date().toISOString(),
        duration: Date.now() - startTime,
        status: 'failed',
        error: error instanceof Error ? error.message : String(error),
      });
      
      throw error;
    }
  }

  private logExecutionMetrics(state: AFIDAGState): void {
    const totalTime = Date.now() - new Date(state.metadata.startTime).getTime();
    const nodesExecuted = state.metadata.trace.filter(entry => entry.status === 'completed').length;
    const nodesFailed = state.metadata.trace.filter(entry => entry.status === 'failed').length;
    
    console.log({
      signalId: state.signalId,
      analystId: state.analystConfig.analystId,
      totalTime,
      nodesExecuted,
      nodesFailed,
      trace: state.metadata.trace,
    });
  }
}
```

---

### 3.2 Enrichment Nodes

#### 3.2.1 Technical Indicators Node

**Location**: [`afi-reactor/src/langgraph/plugins/TechnicalIndicatorsNode.ts`](afi-reactor/src/langgraph/plugins/TechnicalIndicatorsNode.ts)

```typescript
/**
 * Technical Indicators Node - Enrichment Node
 *
 * This node is responsible for:
 * - Calculating technical indicators from price data
 * - Enriching the signal with technical analysis
 */

import type { AFIDAGNode, AFIDAGState } from '../../types/langgraph';

export class TechnicalIndicatorsNode implements AFIDAGNode {
  id = 'technical-indicators';
  type = 'enrichment' as const;
  plugin = 'technical-indicators';
  parallel = true;
  dependencies = [];

  async execute(state: AFIDAGState): Promise<AFIDAGState> {
    const startTime = Date.now();
    
    try {
      // Calculate technical indicators
      const indicators = await this.calculateIndicators(state.rawSignal);
      
      // Store enrichment result
      state.enrichmentResults.set(this.id, indicators);
      
      // Add trace entry
      state.metadata.trace.push({
        nodeId: this.id,
        nodeType: this.type,
        startTime: new Date(startTime).toISOString(),
        endTime: new Date().toISOString(),
        duration: Date.now() - startTime,
        status: 'completed',
      });
      
      return state;
    } catch (error) {
      // Add error trace entry
      state.metadata.trace.push({
        nodeId: this.id,
        nodeType: this.type,
        startTime: new Date(startTime).toISOString(),
        endTime: new Date().toISOString(),
        duration: Date.now() - startTime,
        status: 'failed',
        error: error instanceof Error ? error.message : String(error),
      });
      
      throw error;
    }
  }

  private async calculateIndicators(rawSignal: unknown): Promise<unknown> {
    // Implementation depends on signal structure
    // This is a placeholder for the actual implementation
    return {
      sma: 0,
      ema: 0,
      rsi: 0,
      macd: 0,
    };
  }
}
```

#### 3.2.2 Pattern Recognition Node

**Location**: [`afi-reactor/src/langgraph/plugins/PatternRecognitionNode.ts`](afi-reactor/src/langgraph/plugins/PatternRecognitionNode.ts)

```typescript
/**
 * Pattern Recognition Node - Enrichment Node
 *
 * This node is responsible for:
 * - Recognizing patterns in price data
 * - Enriching the signal with pattern analysis
 */

import type { AFIDAGNode, AFIDAGState } from '../../types/langgraph';

export class PatternRecognitionNode implements AFIDAGNode {
  id = 'pattern-recognition';
  type = 'enrichment' as const;
  plugin = 'pattern-recognition';
  parallel = false;
  dependencies = ['technical-indicators'];

  async execute(state: AFIDAGState): Promise<AFIDAGState> {
    const startTime = Date.now();
    
    try {
      // Get technical indicators from state
      const technicalIndicators = state.enrichmentResults.get('technical-indicators');
      
      // Recognize patterns
      const patterns = await this.recognizePatterns(state.rawSignal, technicalIndicators);
      
      // Store enrichment result
      state.enrichmentResults.set(this.id, patterns);
      
      // Add trace entry
      state.metadata.trace.push({
        nodeId: this.id,
        nodeType: this.type,
        startTime: new Date(startTime).toISOString(),
        endTime: new Date().toISOString(),
        duration: Date.now() - startTime,
        status: 'completed',
      });
      
      return state;
    } catch (error) {
      // Add error trace entry
      state.metadata.trace.push({
        nodeId: this.id,
        nodeType: this.type,
        startTime: new Date(startTime).toISOString(),
        endTime: new Date().toISOString(),
        duration: Date.now() - startTime,
        status: 'failed',
        error: error instanceof Error ? error.message : String(error),
      });
      
      throw error;
    }
  }

  private async recognizePatterns(rawSignal: unknown, technicalIndicators: unknown): Promise<unknown> {
    // Implementation depends on signal structure
    // This is a placeholder for the actual implementation
    return {
      patterns: [],
      confidence: 0,
    };
  }
}
```

#### 3.2.3 Sentiment Node

**Location**: [`afi-reactor/src/langgraph/plugins/SentimentNode.ts`](afi-reactor/src/langgraph/plugins/SentimentNode.ts)

```typescript
/**
 * Sentiment Node - Enrichment Node
 *
 * This node is responsible for:
 * - Analyzing sentiment from news and social media
 * - Enriching the signal with sentiment analysis
 */

import type { AFIDAGNode, AFIDAGState } from '../../types/langgraph';

export class SentimentNode implements AFIDAGNode {
  id = 'sentiment';
  type = 'enrichment' as const;
  plugin = 'sentiment';
  parallel = true;
  dependencies = [];

  async execute(state: AFIDAGState): Promise<AFIDAGState> {
    const startTime = Date.now();
    
    try {
      // Analyze sentiment
      const sentiment = await this.analyzeSentiment(state.rawSignal);
      
      // Store enrichment result
      state.enrichmentResults.set(this.id, sentiment);
      
      // Add trace entry
      state.metadata.trace.push({
        nodeId: this.id,
        nodeType: this.type,
        startTime: new Date(startTime).toISOString(),
        endTime: new Date().toISOString(),
        duration: Date.now() - startTime,
        status: 'completed',
      });
      
      return state;
    } catch (error) {
      // Add error trace entry
      state.metadata.trace.push({
        nodeId: this.id,
        nodeType: this.type,
        startTime: new Date(startTime).toISOString(),
        endTime: new Date().toISOString(),
        duration: Date.now() - startTime,
        status: 'failed',
        error: error instanceof Error ? error.message : String(error),
      });
      
      throw error;
    }
  }

  private async analyzeSentiment(rawSignal: unknown): Promise<unknown> {
    // Implementation depends on signal structure
    // This is a placeholder for the actual implementation
    return {
      sentiment: 'neutral',
      confidence: 0,
      sources: [],
    };
  }
}
```

#### 3.2.4 News Node

**Location**: [`afi-reactor/src/langgraph/plugins/NewsNode.ts`](afi-reactor/src/langgraph/plugins/NewsNode.ts)

```typescript
/**
 * News Node - Enrichment Node
 *
 * This node is responsible for:
 * - Fetching relevant news articles
 * - Enriching the signal with news analysis
 */

import type { AFIDAGNode, AFIDAGState } from '../../types/langgraph';

export class NewsNode implements AFIDAGNode {
  id = 'news';
  type = 'enrichment' as const;
  plugin = 'news';
  parallel = false;
  dependencies = ['sentiment'];

  async execute(state: AFIDAGState): Promise<AFIDAGState> {
    const startTime = Date.now();
    
    try {
      // Get sentiment from state
      const sentiment = state.enrichmentResults.get('sentiment');
      
      // Fetch news
      const news = await this.fetchNews(state.rawSignal, sentiment);
      
      // Store enrichment result
      state.enrichmentResults.set(this.id, news);
      
      // Add trace entry
      state.metadata.trace.push({
        nodeId: this.id,
        nodeType: this.type,
        startTime: new Date(startTime).toISOString(),
        endTime: new Date().toISOString(),
        duration: Date.now() - startTime,
        status: 'completed',
      });
      
      return state;
    } catch (error) {
      // Add error trace entry
      state.metadata.trace.push({
        nodeId: this.id,
        nodeType: this.type,
        startTime: new Date(startTime).toISOString(),
        endTime: new Date().toISOString(),
        duration: Date.now() - startTime,
        status: 'failed',
        error: error instanceof Error ? error.message : String(error),
      });
      
      throw error;
    }
  }

  private async fetchNews(rawSignal: unknown, sentiment: unknown): Promise<unknown> {
    // Implementation depends on signal structure
    // This is a placeholder for the actual implementation
    return {
      articles: [],
      summary: '',
    };
  }
}
```

#### 3.2.5 Scout Node

**Location**: [`afi-reactor/src/langgraph/plugins/ScoutNode.ts`](afi-reactor/src/langgraph/plugins/ScoutNode.ts)

```typescript
/**
 * Scout Node - Ingress Node
 *
 * This node is responsible for:
 * - Scouting for new signals
 * - Ingesting signals into the pipeline
 */

import type { AFIDAGNode, AFIDAGState } from '../../types/langgraph';

export class ScoutNode implements AFIDAGNode {
  id = 'scout';
  type = 'ingress' as const;
  plugin = 'scout';
  parallel = true;
  dependencies = [];

  async execute(state: AFIDAGState): Promise<AFIDAGState> {
    const startTime = Date.now();
    
    try {
      // Scout for signals
      const signals = await this.scoutSignals();
      
      // Store enrichment result
      state.enrichmentResults.set(this.id, signals);
      
      // Add trace entry
      state.metadata.trace.push({
        nodeId: this.id,
        nodeType: this.type,
        startTime: new Date(startTime).toISOString(),
        endTime: new Date().toISOString(),
        duration: Date.now() - startTime,
        status: 'completed',
      });
      
      return state;
    } catch (error) {
      // Add error trace entry
      state.metadata.trace.push({
        nodeId: this.id,
        nodeType: this.type,
        startTime: new Date(startTime).toISOString(),
        endTime: new Date().toISOString(),
        duration: Date.now() - startTime,
        status: 'failed',
        error: error instanceof Error ? error.message : String(error),
      });
      
      throw error;
    }
  }

  private async scoutSignals(): Promise<unknown> {
    // Implementation depends on signal sources
    // This is a placeholder for the actual implementation
    return {
      signals: [],
    };
  }
}
```

#### 3.2.6 Signal Ingress Node

**Location**: [`afi-reactor/src/langgraph/plugins/SignalIngressNode.ts`](afi-reactor/src/langgraph/plugins/SignalIngressNode.ts)

```typescript
/**
 * Signal Ingress Node - Ingress Node
 *
 * This node is responsible for:
 * - Ingesting signals from external sources
 * - Normalizing signals for processing
 */

import type { AFIDAGNode, AFIDAGState } from '../../types/langgraph';

export class SignalIngressNode implements AFIDAGNode {
  id = 'signal-ingress';
  type = 'ingress' as const;
  plugin = 'signal-ingress';
  parallel = true;
  dependencies = [];

  async execute(state: AFIDAGState): Promise<AFIDAGState> {
    const startTime = Date.now();
    
    try {
      // Ingest signals
      const signals = await this.ingestSignals();
      
      // Store enrichment result
      state.enrichmentResults.set(this.id, signals);
      
      // Add trace entry
      state.metadata.trace.push({
        nodeId: this.id,
        nodeType: this.type,
        startTime: new Date(startTime).toISOString(),
        endTime: new Date().toISOString(),
        duration: Date.now() - startTime,
        status: 'completed',
      });
      
      return state;
    } catch (error) {
      // Add error trace entry
      state.metadata.trace.push({
        nodeId: this.id,
        nodeType: this.type,
        startTime: new Date(startTime).toISOString(),
        endTime: new Date().toISOString(),
        duration: Date.now() - startTime,
        status: 'failed',
        error: error instanceof Error ? error.message : String(error),
      });
      
      throw error;
    }
  }

  private async ingestSignals(): Promise<unknown> {
    // Implementation depends on signal sources
    // This is a placeholder for the actual implementation
    return {
      signals: [],
    };
  }
}
```

---

## 4. State Management Mechanisms

### 4.1 State Manager

**Location**: [`afi-reactor/src/state/StateManager.ts`](afi-reactor/src/state/StateManager.ts)

```typescript
/**
 * State Manager
 *
 * This class is responsible for:
 * - Managing AFI DAG state
 * - Tracking execution progress
 * - Handling state transitions
 */

import type { AFIDAGState, ExecutionTraceEntry } from '../types/langgraph';

export class StateManager {
  private state: AFIDAGState;
  private stateHistory: AFIDAGState[];

  constructor(initialState: AFIDAGState) {
    this.state = initialState;
    this.stateHistory = [initialState];
  }

  /**
   * Get current state
   */
  getState(): AFIDAGState {
    return this.state;
  }

  /**
   * Update state
   */
  updateState(updater: (state: AFIDAGState) => AFIDAGState): void {
    const newState = updater(this.state);
    this.state = newState;
    this.stateHistory.push(newState);
  }

  /**
   * Get state history
   */
  getStateHistory(): AFIDAGState[] {
    return this.stateHistory;
  }

  /**
   * Add trace entry
   */
  addTraceEntry(entry: ExecutionTraceEntry): void {
    this.state.metadata.trace.push(entry);
  }

  /**
   * Get trace entries
   */
  getTraceEntries(): ExecutionTraceEntry[] {
    return this.state.metadata.trace;
  }

  /**
   * Get execution metrics
   */
  getExecutionMetrics(): {
    totalTime: number;
    nodesExecuted: number;
    nodesFailed: number;
  } {
    const totalTime = Date.now() - new Date(this.state.metadata.startTime).getTime();
    const nodesExecuted = this.state.metadata.trace.filter(entry => entry.status === 'completed').length;
    const nodesFailed = this.state.metadata.trace.filter(entry => entry.status === 'failed').length;

    return {
      totalTime,
      nodesExecuted,
      nodesFailed,
    };
  }

  /**
   * Reset state to initial state
   */
  resetState(): void {
    this.state = this.stateHistory[0];
    this.stateHistory = [this.state];
  }

  /**
   * Rollback to previous state
   */
  rollbackState(): void {
    if (this.stateHistory.length > 1) {
      this.stateHistory.pop();
      this.state = this.stateHistory[this.stateHistory.length - 1];
    }
  }
}
```

### 4.2 State Validator

**Location**: [`afi-reactor/src/state/StateValidator.ts`](afi-reactor/src/state/StateValidator.ts)

```typescript
/**
 * State Validator
 *
 * This class is responsible for:
 * - Validating AFI DAG state
 * - Checking state invariants
 * - Detecting state inconsistencies
 */

import type { AFIDAGState } from '../types/langgraph';

export class StateValidator {
  /**
   * Validate state
   */
  validate(state: AFIDAGState): {
    valid: boolean;
    errors: string[];
    warnings: string[];
  } {
    const errors: string[] = [];
    const warnings: string[] = [];

    // Check required fields
    if (!state.signalId) {
      errors.push('Missing signalId');
    }

    if (!state.rawSignal) {
      errors.push('Missing rawSignal');
    }

    if (!state.analystConfig) {
      errors.push('Missing analystConfig');
    }

    if (!state.analystConfig.analystId) {
      errors.push('Missing analystConfig.analystId');
    }

    // Check metadata
    if (!state.metadata) {
      errors.push('Missing metadata');
    }

    if (!state.metadata.startTime) {
      errors.push('Missing metadata.startTime');
    }

    if (!state.metadata.trace) {
      errors.push('Missing metadata.trace');
    }

    // Check enrichment results
    if (!state.enrichmentResults) {
      errors.push('Missing enrichmentResults');
    }

    // Check for duplicate trace entries
    const nodeIds = state.metadata.trace.map(entry => entry.nodeId);
    const duplicateNodeIds = nodeIds.filter((id, index) => nodeIds.indexOf(id) !== index);
    if (duplicateNodeIds.length > 0) {
      warnings.push(`Duplicate trace entries for nodes: ${duplicateNodeIds.join(', ')}`);
    }

    // Check for failed nodes
    const failedNodes = state.metadata.trace.filter(entry => entry.status === 'failed');
    if (failedNodes.length > 0) {
      warnings.push(`Failed nodes: ${failedNodes.map(entry => entry.nodeId).join(', ')}`);
    }

    return {
      valid: errors.length === 0,
      errors,
      warnings,
    };
  }

  /**
   * Check state invariants
   */
  checkInvariants(state: AFIDAGState): boolean {
    // Check that all trace entries have required fields
    for (const entry of state.metadata.trace) {
      if (!entry.nodeId || !entry.nodeType || !entry.startTime || !entry.status) {
        return false;
      }
    }

    // Check that all completed entries have end time and duration
    for (const entry of state.metadata.trace) {
      if (entry.status === 'completed' && (!entry.endTime || !entry.duration)) {
        return false;
      }
    }

    // Check that all failed entries have error message
    for (const entry of state.metadata.trace) {
      if (entry.status === 'failed' && !entry.error) {
        return false;
      }
    }

    return true;
  }
}
```

### 4.3 State Serializer

**Location**: [`afi-reactor/src/state/StateSerializer.ts`](afi-reactor/src/state/StateSerializer.ts)

```typescript
/**
 * State Serializer
 *
 * This class is responsible for:
 * - Serializing AFI DAG state to JSON
 * - Deserializing JSON to AFI DAG state
 * - Handling Map serialization/deserialization
 */

import type { AFIDAGState } from '../types/langgraph';

export class StateSerializer {
  /**
   * Serialize state to JSON
   */
  serialize(state: AFIDAGState): string {
    const serialized = {
      ...state,
      enrichmentResults: Array.from(state.enrichmentResults.entries()),
    };

    return JSON.stringify(serialized, null, 2);
  }

  /**
   * Deserialize JSON to state
   */
  deserialize(json: string): AFIDAGState {
    const deserialized = JSON.parse(json);

    return {
      ...deserialized,
      enrichmentResults: new Map(deserialized.enrichmentResults),
    };
  }

  /**
   * Serialize state to file
   */
  async serializeToFile(state: AFIDAGState, filePath: string): Promise<void> {
    const serialized = this.serialize(state);
    await Bun.write(filePath, serialized);
  }

  /**
   * Deserialize state from file
   */
  async deserializeFromFile(filePath: string): Promise<AFIDAGState> {
    const json = await Bun.file(filePath).text();
    return this.deserialize(json);
  }
}
```

---

## 5. Repository Bridge Design

### 5.1 afi-factory Template Registry (Updated)

**Location**: [`afi-factory/template_registry.ts`](afi-factory/template_registry.ts) (updated)

```typescript
/**
 * AFI Factory - Template Registry (Updated)
 * 
 * This file provides the programmatic interface for loading analyst configurations,
 * bridging afi-config schemas with afi-reactor orchestration.
 */

import type {
  AnalystConfig,
  EnrichmentNodeConfig,
  ValidatedAnalystConfig,
  LoadAnalystConfigOptions,
} from './schemas/index';
import { validateAnalystConfig } from './validators/analyst-config-validator';

/**
 * Load analyst configuration
 */
export async function loadAnalystConfig(
  analystId: string,
  options: LoadAnalystConfigOptions = {}
): Promise<ValidatedAnalystConfig> {
  const {
    validate = true,
    cache = true,
    configDir = './analyst-configs',
  } = options;

  // Construct file path
  const filePath = `${configDir}/${analystId}.json`;

  // Load configuration file
  const file = Bun.file(filePath);
  const json = await file.text();
  const config: AnalystConfig = JSON.parse(json);

  // Validate configuration if requested
  if (validate) {
    const validationResult = validateAnalystConfig(config);
    return {
      ...config,
      valid: validationResult.valid,
      errors: validationResult.errors,
      warnings: validationResult.warnings,
    };
  }

  return {
    ...config,
    valid: true,
  };
}

/**
 * Load enrichment node template
 */
export async function loadEnrichmentNodeTemplate(
  nodeId: string
): Promise<EnrichmentNodeConfig> {
  const filePath = `./analyst-configs/templates/enrichment-node.template.json`;
  const file = Bun.file(filePath);
  const json = await file.text();
  const template: EnrichmentNodeConfig = JSON.parse(json);

  return {
    ...template,
    id: nodeId,
  };
}

/**
 * List all analyst configurations
 */
export async function listAnalystConfigs(
  configDir = './analyst-configs'
): Promise<string[]> {
  const dir = Bun.dir(configDir);
  const configs: string[] = [];

  for await (const entry of dir) {
    if (entry.isFile && entry.name.endsWith('.json')) {
      configs.push(entry.name.replace('.json', ''));
    }
  }

  return configs;
}

/**
 * Validate analyst configuration
 */
export function validateAnalystConfig(config: AnalystConfig): {
  valid: boolean;
  errors: string[];
  warnings: string[];
} {
  const errors: string[] = [];
  const warnings: string[] = [];

  // Check required fields
  if (!config.analystId) {
    errors.push('Missing analystId');
  }

  if (!config.enrichmentNodes) {
    errors.push('Missing enrichmentNodes');
  }

  // Check enrichment nodes
  if (config.enrichmentNodes) {
    for (const node of config.enrichmentNodes) {
      if (!node.id) {
        errors.push('Missing node.id');
      }

      if (!node.type) {
        errors.push('Missing node.type');
      }

      if (!node.plugin) {
        errors.push('Missing node.plugin');
      }

      if (typeof node.enabled !== 'boolean') {
        errors.push('Missing or invalid node.enabled');
      }

      // Check for circular dependencies
      if (node.dependencies) {
        const visited = new Set<string>();
        const hasCycle = checkForCircularDependencies(node.id, node.dependencies, config.enrichmentNodes, visited);
        if (hasCycle) {
          errors.push(`Circular dependency detected for node ${node.id}`);
        }
      }
    }
  }

  return {
    valid: errors.length === 0,
    errors,
    warnings,
  };
}

/**
 * Check for circular dependencies
 */
function checkForCircularDependencies(
  nodeId: string,
  dependencies: string[],
  allNodes: EnrichmentNodeConfig[],
  visited: Set<string>
): boolean {
  if (visited.has(nodeId)) {
    return true;
  }

  visited.add(nodeId);

  for (const depId of dependencies) {
    const depNode = allNodes.find(node => node.id === depId);
    if (depNode && depNode.dependencies) {
      if (checkForCircularDependencies(depId, depNode.dependencies, allNodes, visited)) {
        return true;
      }
    }
  }

  visited.delete(nodeId);
  return false;
}
```

### 5.2 afi-factory Validators

**Location**: [`afi-factory/validators/analyst-config-validator.ts`](afi-factory/validators/analyst-config-validator.ts)

```typescript
/**
 * AFI Factory - Analyst Config Validator
 * 
 * This file provides validation functions for analyst configurations,
 * using schemas from afi-config.
 */

import type { AnalystConfig, EnrichmentNodeConfig } from '../schemas/index';

/**
 * Validate analyst configuration against schema
 */
export function validateAnalystConfig(config: AnalystConfig): {
  valid: boolean;
  errors: string[];
  warnings: string[];
} {
  const errors: string[] = [];
  const warnings: string[] = [];

  // Validate analystId
  if (!config.analystId) {
    errors.push('analystId is required');
  } else if (!/^[a-z0-9-]+$/.test(config.analystId)) {
    errors.push('analystId must match pattern ^[a-z0-9-]+$');
  }

  // Validate version
  if (config.version && !/^v\d+\.\d+\.\d+$/.test(config.version)) {
    errors.push('version must match pattern ^v\\d+\\.\\d+\\.\\d+$');
  }

  // Validate enrichmentNodes
  if (!config.enrichmentNodes) {
    errors.push('enrichmentNodes is required');
  } else if (!Array.isArray(config.enrichmentNodes)) {
    errors.push('enrichmentNodes must be an array');
  } else {
    for (let i = 0; i < config.enrichmentNodes.length; i++) {
      const node = config.enrichmentNodes[i];
      const nodeValidation = validateEnrichmentNode(node);
      errors.push(...nodeValidation.errors.map(err => `enrichmentNodes[${i}]: ${err}`));
      warnings.push(...nodeValidation.warnings.map(warn => `enrichmentNodes[${i}]: ${warn}`));
    }
  }

  // Validate metadata
  if (config.metadata) {
    if (config.metadata.createdAt && !isValidISODate(config.metadata.createdAt)) {
      errors.push('metadata.createdAt must be a valid ISO date');
    }

    if (config.metadata.updatedAt && !isValidISODate(config.metadata.updatedAt)) {
      errors.push('metadata.updatedAt must be a valid ISO date');
    }
  }

  return {
    valid: errors.length === 0,
    errors,
    warnings,
  };
}

/**
 * Validate enrichment node
 */
export function validateEnrichmentNode(node: EnrichmentNodeConfig): {
  valid: boolean;
  errors: string[];
  warnings: string[];
} {
  const errors: string[] = [];
  const warnings: string[] = [];

  // Validate id
  if (!node.id) {
    errors.push('id is required');
  } else if (!/^[a-z0-9-]+$/.test(node.id)) {
    errors.push('id must match pattern ^[a-z0-9-]+$');
  }

  // Validate type
  if (!node.type) {
    errors.push('type is required');
  } else if (!['enrichment', 'ingress'].includes(node.type)) {
    errors.push('type must be one of: enrichment, ingress');
  }

  // Validate plugin
  if (!node.plugin) {
    errors.push('plugin is required');
  } else if (!/^[a-z0-9-]+$/.test(node.plugin)) {
    errors.push('plugin must match pattern ^[a-z0-9-]+$');
  }

  // Validate enabled
  if (typeof node.enabled !== 'boolean') {
    errors.push('enabled is required and must be a boolean');
  }

  // Validate optional
  if (node.optional !== undefined && typeof node.optional !== 'boolean') {
    errors.push('optional must be a boolean');
  }

  // Validate parallel
  if (node.parallel !== undefined && typeof node.parallel !== 'boolean') {
    errors.push('parallel must be a boolean');
  }

  // Validate dependencies
  if (node.dependencies) {
    if (!Array.isArray(node.dependencies)) {
      errors.push('dependencies must be an array');
    } else {
      for (let i = 0; i < node.dependencies.length; i++) {
        const dep = node.dependencies[i];
        if (typeof dep !== 'string') {
          errors.push(`dependencies[${i}] must be a string`);
        } else if (!/^[a-z0-9-]+$/.test(dep)) {
          errors.push(`dependencies[${i}] must match pattern ^[a-z0-9-]+$`);
        }
      }
    }
  }

  return {
    valid: errors.length === 0,
    errors,
    warnings,
  };
}

/**
 * Check if string is a valid ISO date
 */
function isValidISODate(dateString: string): boolean {
  return !isNaN(Date.parse(dateString));
}
```

---

## 6. Droid Mitigation Integration

### 6.1 Documentation Droid Integration

**Location**: [`afi-reactor/src/droids/DocumentationDroid.ts`](afi-reactor/src/droids/DocumentationDroid.ts)

```typescript
/**
 * Documentation Droid
 *
 * This droid is responsible for:
 * - Generating API documentation from TypeScript types
 * - Creating architecture diagrams from code structure
 * - Documenting AFI DAG node interfaces and contracts
 */

import type { AFIDAGNode, AFIDAGState } from '../types/langgraph';

export class DocumentationDroid {
  /**
   * Generate API documentation from TypeScript types
   */
  async generateAPIDocumentation(): Promise<void> {
    // Scan all TypeScript files
    const types = await this.scanTypes();
    
    // Generate documentation
    const docs = await this.generateDocs(types);
    
    // Write to docs/
    await this.writeDocs(docs);
  }

  /**
   * Generate architecture diagrams from code structure
   */
  async generateArchitectureDiagrams(): Promise<void> {
    // Scan code structure
    const structure = await this.scanStructure();
    
    // Generate diagrams
    const diagrams = await this.generateDiagrams(structure);
    
    // Write to docs/
    await this.writeDiagrams(diagrams);
  }

  /**
   * Document AFI DAG node interfaces and contracts
   */
  async documentAFIDAGNodes(): Promise<void> {
    // Scan all LangGraph nodes
    const nodes = await this.scanNodes();
    
    // Generate documentation
    const docs = await this.generateNodeDocs(nodes);
    
    // Write to docs/
    await this.writeNodeDocs(docs);
  }

  private async scanTypes(): Promise<unknown> {
    // Implementation
    return {};
  }

  private async generateDocs(types: unknown): Promise<string> {
    // Implementation
    return '';
  }

  private async writeDocs(docs: string): Promise<void> {
    // Implementation
  }

  private async scanStructure(): Promise<unknown> {
    // Implementation
    return {};
  }

  private async generateDiagrams(structure: unknown): Promise<string> {
    // Implementation
    return '';
  }

  private async writeDiagrams(diagrams: string): Promise<void> {
    // Implementation
  }

  private async scanNodes(): Promise<AFIDAGNode[]> {
    // Implementation
    return [];
  }

  private async generateNodeDocs(nodes: AFIDAGNode[]): Promise<string> {
    // Implementation
    return '';
  }

  private async writeNodeDocs(docs: string): Promise<void> {
    // Implementation
  }
}
```

### 6.2 Validation Droid Integration

**Location**: [`afi-reactor/src/droids/ValidationDroid.ts`](afi-reactor/src/droids/ValidationDroid.ts)

```typescript
/**
 * Validation Droid
 * 
 * This droid is responsible for:
 * - Validating analyst configurations against schemas
 * - Providing clear error messages for validation failures
 * - Suggesting fixes for common configuration errors
 */

import { loadAnalystConfig, listAnalystConfigs } from 'afi-factory/template_registry';

export class ValidationDroid {
  /**
   * Validate all analyst configurations
   */
  async validateAllConfigurations(): Promise<void> {
    // List all analyst configurations
    const configs = await listAnalystConfigs();
    
    // Validate each configuration
    const results = await Promise.all(
      configs.map(async (configId) => {
        const config = await loadAnalystConfig(configId);
        return {
          configId,
          valid: config.valid,
          errors: config.errors,
          warnings: config.warnings,
        };
      })
    );
    
    // Generate validation report
    const report = this.generateValidationReport(results);
    
    // Write report
    await this.writeReport(report);
  }

  /**
   * Validate a single analyst configuration
   */
  async validateConfiguration(configId: string): Promise<{
    valid: boolean;
    errors: string[];
    warnings: string[];
    suggestions: string[];
  }> {
    const config = await loadAnalystConfig(configId);
    
    const suggestions = this.generateSuggestions(config);
    
    return {
      valid: config.valid,
      errors: config.errors || [],
      warnings: config.warnings || [],
      suggestions,
    };
  }

  /**
   * Generate suggestions for fixing configuration errors
   */
  private generateSuggestions(config: any): string[] {
    const suggestions: string[] = [];
    
    if (config.errors) {
      for (const error of config.errors) {
        if (error.includes('Missing analystId')) {
          suggestions.push('Add analystId field to configuration');
        } else if (error.includes('Missing enrichmentNodes')) {
          suggestions.push('Add enrichmentNodes array to configuration');
        } else if (error.includes('Circular dependency')) {
          suggestions.push('Remove circular dependencies in enrichment nodes');
        }
      }
    }
    
    return suggestions;
  }

  /**
   * Generate validation report
   */
  private generateValidationReport(results: any[]): string {
    const validConfigs = results.filter(r => r.valid).length;
    const invalidConfigs = results.filter(r => !r.valid).length;
    
    let report = `# Analyst Configuration Validation Report\n\n`;
    report += `Total configurations: ${results.length}\n`;
    report += `Valid configurations: ${validConfigs}\n`;
    report += `Invalid configurations: ${invalidConfigs}\n\n`;
    
    for (const result of results) {
      report += `## ${result.configId}\n\n`;
      report += `Status: ${result.valid ? '✅ Valid' : '❌ Invalid'}\n\n`;
      
      if (result.errors && result.errors.length > 0) {
        report += `### Errors\n\n`;
        for (const error of result.errors) {
          report += `- ${error}\n`;
        }
        report += '\n';
      }
      
      if (result.warnings && result.warnings.length > 0) {
        report += `### Warnings\n\n`;
        for (const warning of result.warnings) {
          report += `- ${warning}\n`;
        }
        report += '\n';
      }
    }
    
    return report;
  }

  /**
   * Write validation report
   */
  private async writeReport(report: string): Promise<void> {
    await Bun.write('./reports/validation/analyst-config-validation.md', report);
  }
}
```

---

## 7. Implementation Phases

### Phase 1: Schema Foundation (Week 1)

**Objective**: Create JSON schemas in afi-config for analyst configuration and enrichment nodes.

**Tasks**:
1. Create [`afi-config/schemas/analyst-config.schema.json`](afi-config/schemas/analyst-config.schema.json)
2. Create [`afi-config/schemas/definitions/enrichment-node.schema.json`](afi-config/schemas/definitions/enrichment-node.schema.json)
3. Update [`afi-config/schemas/pipeline.schema.json`](afi-config/schemas/pipeline.schema.json)
4. Add validation tests for all schemas
5. Generate example configurations

**Success Criteria**:
- All schemas are valid JSON Schema Draft 7+
- All schemas have comprehensive documentation
- All schemas have validation tests
- Example configurations validate successfully

**Droid**: Schema Droid

---

### Phase 2: TypeScript Interfaces (Week 2)

**Objective**: Create TypeScript interfaces in afi-factory, afi-reactor, and afi-core.

**Tasks**:
1. Create [`afi-factory/schemas/index.ts`](afi-factory/schemas/index.ts)
2. Create [`afi-reactor/src/types/langgraph.ts`](afi-reactor/src/types/langgraph.ts)
3. Create [`afi-core/src/langgraph/AFIDAGSignalEnvelope.ts`](afi-core/src/langgraph/AFIDAGSignalEnvelope.ts)
4. Update [`afi-core/src/analysts/analyst-score-template.ts`](afi-core/src/analysts/analyst-score-template.ts)
5. Add type tests for all interfaces

**Success Criteria**:
- All interfaces are strongly typed
- All interfaces have comprehensive documentation
- All interfaces have type tests
- TypeScript compilation succeeds

**Droid**: Type Droid

---

### Phase 3: Template Registry (Week 3)

**Objective**: Update afi-factory template registry to load and validate analyst configurations.

**Tasks**:
1. Update [`afi-factory/template_registry.ts`](afi-factory/template_registry.ts)
2. Create [`afi-factory/validators/analyst-config-validator.ts`](afi-factory/validators/analyst-config-validator.ts)
3. Create example analyst configurations
4. Add unit tests for template registry
5. Add integration tests for validation

**Success Criteria**:
- Template registry loads analyst configurations
- Template registry validates configurations against schemas
- Example configurations validate successfully
- All tests pass

**Droid**: Template Droid

---

### Phase 4: State Management (Week 4)

**Objective**: Create state management infrastructure in afi-reactor.

**Tasks**:
1. Create [`afi-reactor/src/state/StateManager.ts`](afi-reactor/src/state/StateManager.ts)
2. Create [`afi-reactor/src/state/StateValidator.ts`](afi-reactor/src/state/StateValidator.ts)
3. Create [`afi-reactor/src/state/StateSerializer.ts`](afi-reactor/src/state/StateSerializer.ts)
4. Add unit tests for state management
5. Add integration tests for state management

**Success Criteria**:
- State manager manages AFI DAG state
- State validator validates state
- State serializer serializes/deserializes state
- All tests pass

**Droid**: State Droid

---

### Phase 5: Required Nodes (Week 5)

**Objective**: Implement required nodes (analyst, execution, observer) in afi-reactor.

**Tasks**:
1. Create [`afi-reactor/src/langgraph/nodes/AnalystNode.ts`](afi-reactor/src/langgraph/nodes/AnalystNode.ts)
2. Create [`afi-reactor/src/langgraph/nodes/ExecutionNode.ts`](afi-reactor/src/langgraph/nodes/ExecutionNode.ts)
3. Create [`afi-reactor/src/langgraph/nodes/ObserverNode.ts`](afi-reactor/src/langgraph/nodes/ObserverNode.ts)
4. Add unit tests for all nodes
5. Add integration tests for node execution

**Success Criteria**:
- All required nodes implement AFIDAGNode interface
- All nodes have comprehensive tests
- All nodes have clear documentation
- All tests pass

**Droid**: Node Droid

---

### Phase 6: Enrichment Nodes (Week 6)

**Objective**: Implement enrichment nodes in afi-reactor.

**Tasks**:
1. Create [`afi-reactor/src/langgraph/plugins/TechnicalIndicatorsNode.ts`](afi-reactor/src/langgraph/plugins/TechnicalIndicatorsNode.ts)
2. Create [`afi-reactor/src/langgraph/plugins/PatternRecognitionNode.ts`](afi-reactor/src/langgraph/plugins/PatternRecognitionNode.ts)
3. Create [`afi-reactor/src/langgraph/plugins/SentimentNode.ts`](afi-reactor/src/langgraph/plugins/SentimentNode.ts)
4. Create [`afi-reactor/src/langgraph/plugins/NewsNode.ts`](afi-reactor/src/langgraph/plugins/NewsNode.ts)
5. Create [`afi-reactor/src/langgraph/plugins/ScoutNode.ts`](afi-reactor/src/langgraph/plugins/ScoutNode.ts)
6. Create [`afi-reactor/src/langgraph/plugins/SignalIngressNode.ts`](afi-reactor/src/langgraph/plugins/SignalIngressNode.ts)
7. Add unit tests for all nodes
8. Add integration tests for node execution

**Success Criteria**:
- All enrichment nodes implement AFIDAGNode interface
- All nodes have comprehensive tests
- All nodes have clear documentation
- All tests pass

**Droid**: Plugin Droid

---

### Phase 7: Droid Integration (Week 7)

**Objective**: Integrate droids for documentation and validation.

**Tasks**:
1. Create [`afi-reactor/src/droids/DocumentationDroid.ts`](afi-reactor/src/droids/DocumentationDroid.ts)
2. Create [`afi-reactor/src/droids/ValidationDroid.ts`](afi-reactor/src/droids/ValidationDroid.ts)
3. Add unit tests for droids
4. Add integration tests for droids
5. Create droid configuration files

**Success Criteria**:
- All droids comply with Droid Charter and Playbook
- All droids have comprehensive tests
- All droids have clear documentation
- All tests pass

**Droid**: Droid Droid

---

### Phase 8: Integration Testing (Week 8)

**Objective**: Perform end-to-end integration testing of the entire system.

**Tasks**:
1. Create integration tests for schema → type → registry → state → nodes flow
2. Create integration tests for analyst configuration loading
3. Create integration tests for DAG building (placeholder for Part 2)
4. Create integration tests for state management
5. Create integration tests for node execution
6. Performance testing
7. Documentation review

**Success Criteria**:
- All integration tests pass
- Performance meets requirements
- Documentation is comprehensive
- System is ready for Part 2 implementation

**Droid**: Integration Droid

---

## 8. Testing Strategy

### 8.1 Unit Testing

**Scope**: Test individual components in isolation.

**Tools**: Vitest, TypeScript

**Coverage**: > 90%

**Examples**:
- Test schema validation
- Test TypeScript type checking
- Test template registry functions
- Test state manager functions
- Test node execution logic

### 8.2 Integration Testing

**Scope**: Test interactions between components.

**Tools**: Vitest, TypeScript

**Coverage**: > 80%

**Examples**:
- Test schema → type flow
- Test type → registry flow
- Test registry → state flow
- Test state → nodes flow
- Test end-to-end analyst configuration loading

### 8.3 End-to-End Testing

**Scope**: Test the entire system from analyst configuration to node execution.

**Tools**: Vitest, TypeScript

**Coverage**: > 70%

**Examples**:
- Test complete analyst configuration loading and validation
- Test complete state management lifecycle
- Test complete node execution pipeline

### 8.4 Performance Testing

**Scope**: Test system performance under load.

**Tools**: Vitest, TypeScript

**Metrics**:
- Analyst configuration loading time < 100ms
- State validation time < 50ms
- Node execution time < 1s (per node)
- State serialization time < 100ms

### 8.5 Documentation Testing

**Scope**: Test that documentation is accurate and comprehensive.

**Tools**: Manual review, automated documentation generation

**Coverage**: 100%

**Examples**:
- All interfaces have documentation
- All functions have documentation
- All schemas have documentation
- All examples are accurate

---

## 9. Success Criteria

### 9.1 Technical Success Criteria

- [ ] All schemas are valid JSON Schema Draft 7+
- [ ] All TypeScript interfaces are strongly typed
- [ ] All TypeScript compilation succeeds
- [ ] All unit tests pass (> 90% coverage)
- [ ] All integration tests pass (> 80% coverage)
- [ ] All end-to-end tests pass (> 70% coverage)
- [ ] Performance meets requirements
- [ ] Documentation is comprehensive

### 9.2 Architectural Success Criteria

- [ ] Clear separation of concerns between afi-config, afi-factory, afi-reactor, and afi-core
- [ ] All configurations are validated against schemas
- [ ] All interfaces are strongly typed
- [ ] All components are testable
- [ ] All components are documented
- [ ] All components comply with Droid Charter and Playbook

### 9.3 Operational Success Criteria

- [ ] Analyst configurations can be loaded and validated
- [ ] State can be managed and validated
- [ ] Nodes can be executed
- [ ] Droids can generate documentation
- [ ] Droids can validate configurations
- [ ] System is ready for Part 2 implementation

---

## Conclusion

This implementation plan provides a comprehensive roadmap for Part 1 of the AFI-Reactor AFI DAG integration, focusing on the foundation layer: schemas, configuration infrastructure, and TypeScript interfaces that bridge afi-factory and afi-config repositories.

The plan is organized into 8 phases over 8 weeks, with clear objectives, tasks, success criteria, and droid assignments for each phase. The plan adheres to the Droid mitigation strategies outlined in the previous analysis documents.

Upon completion of Part 1, the system will be ready for Part 2 implementation: AFI DAG orchestrator, plugin system, and DAG execution.

**Next Steps**:
1. Review and approve this implementation plan
2. Transition to Orchestrator Mode to execute the implementation
3. Begin with Phase 1: Schema Foundation

---

**Document Version**: v1.0
**Last Updated**: 2025-12-26
**Author**: AFI Architecture Team
**Status**: Ready for Implementation