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
- **Purpose**: Agent factory for creating and managing AFI agents
- **Language**: TypeScript
- **Key Components**:
  - Agent templates
  - Agent registry
  - Agent lifecycle management
  - Agent configuration

### afi-agents
- **Purpose**: Collection of AFI agent implementations
- **Language**: TypeScript
- **Key Components**:
  - Signal processing agents
  - Analysis agents
  - Validation agents
  - Custom agent implementations

## CLI Repositories

### afi-cli-framework
- **Purpose**: Framework for building AFI CLI tools
- **Language**: TypeScript
- **Key Components**:
  - CLI application framework
  - Command registration
  - Configuration management
  - Extension points

### afi-cli-shared
- **Purpose**: Shared utilities for CLI tools
- **Language**: Python
- **Key Components**:
  - Shared CLI utilities
  - Configuration handling
  - Error handling
  - Validation helpers

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

### afi-assets
- **Purpose**: Digital assets and media
- **Language**: N/A
- **Key Components**:
  - Logos
  - Media kits
  - Token graphics
  - Brand assets

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
afi-gateway → afi-pipeline → afi-reactor
    ↓              ↓
afi-factory → afi-agents
    ↓
afi-cli-framework → afi-cli-shared
    ↓
afi-econ → afi-governance
    ↓
afi-benchkit → afi-tiny-brains
    ↓
afi-docs ← afi-assets ← afi-artifacts
    ↑
afi-config (all repos)
```

## Key Integration Points

1. **Gateway to Pipeline**: afi-gateway sends signals to afi-pipeline for processing
2. **Pipeline to Reactor**: afi-pipeline can trigger afi-reactor for real-time processing
3. **Factory to Agents**: afi-factory creates and manages agents in afi-agents
4. **CLI Framework to Shared**: afi-cli-framework uses utilities from afi-cli-shared
5. **Econ to Governance**: afi-econ provides economic data to afi-governance
6. **Benchkit to Tiny Brains**: afi-benchkit tests models from afi-tiny-brains
7. **Config to All**: afi-config provides configuration to all repositories

## Development Workflow

1. **Core Development**: Start with afi-core for protocol changes
2. **Gateway Integration**: Update afi-gateway for new endpoints
3. **Pipeline Updates**: Modify afi-pipeline for new processing stages
4. **Agent Development**: Use afi-factory to create agents in afi-agents
5. **CLI Tools**: Build CLI tools using afi-cli-framework and afi-cli-shared
6. **Economic Modeling**: Update afi-econ and afi-governance for economic changes
7. **Testing**: Use afi-benchkit and afi-tiny-brains for testing
8. **Documentation**: Update afi-docs with changes
9. **Assets**: Update afi-assets for new media
10. **Artifacts**: Add research artifacts to afi-artifacts
11. **Configuration**: Update afi-config for new configurations
