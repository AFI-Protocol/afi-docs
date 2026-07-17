# AFI Repository Map

## Core Repositories

### afi-core
- **Purpose**: Core protocol implementation and shared utilities
- **Language**: TypeScript
- **Key Components**:
  - Protocol definitions
  - Shared types and interfaces
  - Core business logic
  - Validation utilities

### afi-gateway
- **Purpose**: Gateway service for signal ingestion and routing
- **Language**: TypeScript
- **Key Components**:
  - Signal ingestion endpoints
  - Request routing
  - Authentication and authorization
  - Rate limiting
  - Telemetry integration

### afi-pipeline
- **Purpose**: Signal processing pipeline with DAG execution
- **Language**: TypeScript
- **Key Components**:
  - DAG execution engine
  - Stage processors
  - Mapper implementations
  - Validator implementations
  - Vault persistence layer

### afi-reactor
- **Purpose**: Reactor service for real-time signal processing
- **Language**: TypeScript
- **Key Components**:
  - Real-time signal ingestion
  - Stream processing
  - Event-driven architecture
  - Integration with pipeline

## Agent Repositories

### afi-factory
- **Purpose**: Pipeline authoring system (afi-governance `decisions/factory-configurable-pipelines-v1.md`)
- **Language**: TypeScript
- **Key Components**:
  - Pipeline template authoring (`afi.pipeline-template.v1`)
  - Template instantiation to `afi.pipeline.v1` manifests
  - Manifest validation against the governed afi-config contracts
  - Canonical (timestamp-free) hashing

## Economic System

### afi-econ
- **Purpose**: Economic simulation and analysis tools
- **Language**: TypeScript/Python
- **Key Components**:
  - Economic models
  - Simulation tools
  - Reward distribution
  - Token economics

### afi-governance
- **Purpose**: Governance system for AFI protocol
- **Language**: TypeScript
- **Key Components**:
  - Proposal submission
  - Voting mechanisms
  - Proposal validation
  - Governance rules

## Testing & Benchmarking

### afi-benchkit
- **Purpose**: Benchmarking and testing toolkit
- **Language**: Python
- **Key Components**:
  - Benchmarking tools
  - Test harnesses
  - Metrics collection
  - Performance analysis

### afi-tiny-brains
- **Purpose**: Machine learning models for signal analysis
- **Language**: Python
- **Key Components**:
  - ML model implementations
  - Training scripts
  - Model evaluation
  - Prediction services

## Documentation & Assets

### afi-docs
- **Purpose**: Documentation site
- **Language**: Markdown/Mintlify
- **Key Components**:
  - API documentation
  - User guides
  - Architecture documentation
  - Tutorials

### afi-artifacts
- **Purpose**: Research artifacts and reproducibility
- **Language**: Various
- **Key Components**:
  - Research papers
  - Datasets
  - Reproducibility scripts
  - Citation metadata

## Configuration

### afi-config
- **Purpose**: Configuration management
- **Language**: TypeScript/JSON
- **Key Components**:
  - Configuration schemas
  - Environment configurations
  - Deployment configs
  - Feature flags

## Repository Interdependencies

```
afi-core
    ↓
afi-gateway → afi-reactor
    ↓
afi-factory
    ↓
afi-econ → afi-governance
    ↓
afi-benchkit → afi-tiny-brains
    ↓
afi-docs ← afi-artifacts
    ↑
afi-config (all repos)
```

## Key Integration Points

1. **Gateway to Reactor**: afi-gateway forwards USS v1.1 signals to afi-reactor for Froggy scoring (canonical spine — the legacy `afi-pipeline` hop no longer exists)
2. **Factory**: afi-factory provides pipeline/template authoring, manifest validation, and canonical hashing (the standalone agents repo no longer exists)
3. **Econ to Governance**: afi-econ provides economic data to afi-governance
4. **Benchkit to Tiny Brains**: afi-benchkit tests models from afi-tiny-brains
5. **Config to All**: afi-config provides configuration to all repositories

> Note: the deprecated Python CLI utilities repo was removed (2026-06-19) and its bash lib was rehomed to `afi-ops/scripts/lib/afi-shared.sh`.

## Development Workflow

1. **Core Development**: Start with afi-core for protocol changes
2. **Gateway Integration**: Update afi-gateway for new endpoints
3. **Reactor Updates**: Modify afi-reactor for new scoring/pipeline stages
4. **Pipeline Authoring**: Use afi-factory to author and validate pipeline manifests
5. **Economic Modeling**: Update afi-econ and afi-governance for economic changes
6. **Testing**: Use afi-benchkit and afi-tiny-brains for testing
7. **Documentation**: Update afi-docs with changes
8. **Artifacts**: Add research artifacts to afi-artifacts
9. **Configuration**: Update afi-config for new configurations
