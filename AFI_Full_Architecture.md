# AFI Protocol - Full Architecture Documentation

**Generated:** 2025-12-19  
**Purpose:** Comprehensive architecture documentation combining information from all AFI Protocol repositories

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [System Overview](#system-overview)
3. [Core Architecture](#core-architecture)
4. [Signal Processing Pipeline](#signal-processing-pipeline)
5. [Token Economics & Minting](#token-economics--minting)
6. [Infrastructure & Operations](#infrastructure--operations)
7. [Agent System](#agent-system)
8. [Integration & Extensions](#integration--extensions)
9. [Governance & Coordination](#governance--coordination)
10. [Development & Testing](#development--testing)
11. [Deployment Architecture](#deployment-architecture)
12. [Security Model](#security-model)
13. [Data Flow Diagrams](#data-flow-diagrams)
14. [Key Concepts & Terminology](#key-concepts--terminology)

---

## Executive Summary

**AFI Protocol (Agentic Financial Intelligence)** is a modular, decentralized protocol for harvesting, validating, and monetizing financial insight through autonomous agents. The protocol combines:

- **Signal Intelligence**: Multi-source data aggregation and enrichment
- **Validator Network**: Proof-of-Intelligence (PoI) and Proof-of-Insight (PoInsight) validation
- **Token Economics**: Signal-driven token minting with 86B AFI supply cap
- **Agent Framework**: ElizaOS-integrated autonomous agents
- **Reproducibility**: Deterministic pipeline with Codex replay and TSSD vault

**Key Principles:**
- **Agent-First**: Designed for autonomous agent operation
- **Modular**: Clean separation of concerns across repositories
- **Deterministic**: Reproducible results via Codex and TSSD
- **Auditable**: Full provenance tracking and replay capability
- **Cross-Chain**: xERC20 token standard on Base (primary)

---

## System Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      AFI Protocol Stack                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  afi-gateway │  │  afi-sdk-ts  │  │ afi-sdk-     │      │
│  │   (External   │  │              │  │  python      │      │
│  │   Integration)│  │ (TypeScript  │  │  (Python     │      │
│  │  (Phoenix,    │  │   SDK)       │  │   SDK)       │      │
│  │  Alpha, Froggy, │  │              │  │              │      │
│  │  Val Dook)     │  │              │  │              │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                  │                  │              │
│         └──────────────────┼──────────────────┘              │
│                            │                                 │
│                    ┌───────▼────────┐                        │
│                    │  afi-reactor   │                        │
│                    │  (DAG Orch.)   │                        │
│                    │  15-Node       │                        │
│                    │  Pipeline      │                        │
│                    └───┬───────┬────┘                        │
│                        │       │                             │
│         ┌──────────────┘       └──────────────┐              │
│         │                                     │              │
│   ┌─────▼─────┐                       ┌──────▼──────┐       │
│   │ afi-core  │                       │ afi-plugins │       │
│   │ (Runtime) │                       │ (Extensions)│       │
│   │ Validators│                       │             │       │
│   │ Scorers   │                       └─────────────┘       │
│   └─────┬─────┘                                             │
│         │                                                    │
│   ┌─────▼─────┐       ┌─────────────┐                      │
│   │ afi-govern │       │  afi-math   │                      │
│   │ (Vault)   │       │  (Pure Math)│                      │
│   └───────────┘       └─────────────┘                      │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              afi-config (Global Config)              │  │
│  │              Schemas, Governance, Droid Charter      │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │          Token Layer (On-Chain/Off-Chain)            │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │  │
│  │  │  afi-token   │  │  afi-mint    │  │ afi-govern │ │  │
│  │  │  (Contracts) │  │  (Coord.)    │  │  (Govern.) │ │  │
│  │  └──────────────┘  └──────────────┘  └────────────┘ │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           Operations & Deployment                    │  │
│  │  ┌──────────────┐              ┌──────────────┐     │  │
│  │  │  afi-ops     │              │  afi-infra   │     │  │
│  │  │  (Deploy)    │              │  (Infra)     │     │  │
│  │  └──────────────┘              └──────────────┘     │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Repository Organization

AFI Protocol is organized into **26 repositories**, each with specific responsibilities:

**Core Layer (3 repos):**
- `afi-config` - Global configuration and schemas
- `afi-core` - Runtime behavior (validators, scorers)
- `afi-reactor` - DAG orchestration (15-node pipeline)

**Token Layer (5 repos):**
- `afi-token` - Smart contracts (xERC20, receipts, coordinator)
- `afi-mint` - Minting coordination (off-chain)
- `afi-governance` - Governance and Epoch Pulse
- `afi-math` - Pure math primitives
- `afi-econ` - Economic modeling and simulation

**Infrastructure Layer (2 repos):**
- `afi-infra` - TSSD vault, templates, schemas
- `afi-ops` - Deployment, health checks, runbooks

**Extension Layer (4 repos):**
- `afi-plugins` - Plugin registry and templates
- `afi-skills` - Versioned skill library
- `afi-factory` - Agent templates and spawning
- `afi-starters` - Starter kits for developers

**Integration Layer (2 repos):**
- `afi-gateway` - ElizaOS integration (Phoenix, Alpha, Froggy, Val Dook)
- `afi-tiny-brains` - AI/ML microservice for enrichment

**Documentation Layer (3 repos):**
- `afi-docs` - Protocol specifications and guides
- `afi-artifacts` - Reproducibility bundle (paper-2025-v2.2)
- `afi-benchkit` - Validator benchmarking

**SDK Layer (2 repos):**
- `afi-sdk-ts` - TypeScript SDK
- `afi-sdk-python` - Python SDK

**Other (5 repos):**
- `afi-protocol` - Meta-repo (contributor manifest)
- `afi-labs` - Experimental playground
- `afi-assets` - Brand assets
- `afi-research-site` - Research website

---

## Core Architecture

### The AFI Orchestrator Doctrine (10 Commandments)

The AFI Orchestrator Doctrine defines the core architectural principles:

1. **afi-reactor is the orchestrator of AFI** - All canonical pipelines, DAGs, and routing logic live here
2. **afi-core is our runtime library, not our boss** - ElizaOS and agents run inside pipelines defined by afi-reactor
3. **The DAG is law** - Every signal path must be expressible as a Reactor DAG
4. **Agents are nodes, not gods** - Individual agents are pluggable nodes the DAG calls
5. **Eliza's native orchestrator is an implementation detail** - Wrapped/reused as a node under afi-reactor's authority
6. **State & replay belong here** - Pipeline state, Codex replay, audits owned by afi-reactor
7. **Configuration is externalized** - Reactor reads from afi-config and registries
8. **No token/econ logic in afi-reactor** - Emissions and rewards live in afi-token
9. **No infra glue in afi-reactor** - Deployment lives in afi-infra/afi-ops
10. **If orchestration logic doesn't fit this doctrine, it's in the wrong repo**

### Repository Boundaries

```
┌────────────────────────────────────────────────────────────────┐
│                      Boundary Definitions                       │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  afi-core = runtime behavior (validators, scoring, types)      │
│  afi-reactor = orchestration (DAG wiring, pipeline execution)  │
│                                                                 │
│  afi-token = on-chain contracts (minting execution)            │
│  afi-mint = off-chain coordination (minting logic)             │
│                                                                 │
│  afi-config = global schemas and governance                    │
│  afi-infra = templates, TSSD vault, agent stubs                │
│  afi-ops = deployment automation and monitoring                │
│                                                                 │
│  afi-plugins = extension surface (plugin definitions)          │
│  afi-skills = agent capabilities (skill library)               │
│  afi-factory = agent templates (spawning logic)                │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

### Dependency Direction Rules

**Critical Rule:** Dependencies flow in ONE direction only:

```
afi-config (base layer - no dependencies)
    ↓
afi-core (depends on afi-config)
    ↓
afi-reactor (depends on afi-core, afi-config)
    ↓
Consumers (afi-gateway, afi-sdk-*, afi-ops)
```

**Forbidden Patterns:**
- ❌ afi-core depending on afi-reactor (circular)
- ❌ afi-token depending on afi-reactor (wrong layer)
- ❌ Cross-repo relative imports (breaks modularity)
- ❌ Eliza code vendored into AFI repos (violates doctrine)

---

## Signal Processing Pipeline

### The 15-Node DAG

AFI-Reactor implements a **deterministic, 15-node DAG pipeline** for signal processing:

```
┌─────────────────────────────────────────────────────────────┐
│                  15-Node Signal Pipeline                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              GENERATORS (Signal Sources)             │  │
│  │                                                       │  │
│  │  1. market-data-streamer    (Price/volume feeds)    │  │
│  │  2. onchain-feed-ingestor   (Blockchain events)     │  │
│  │  3. social-signal-crawler   (Social sentiment)      │  │
│  │  4. news-feed-parser        (Financial news)        │  │
│  │  5. ai-strategy-generator   (AI strategies)         │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                    │
│                         ▼                                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           ANALYZERS (Deep Analysis & Insight)        │  │
│  │                                                       │  │
│  │  6. technical-analysis-node    (TA indicators)      │  │
│  │  7. pattern-recognition-node   (Chart patterns)     │  │
│  │  8. sentiment-analysis-node    (Market sentiment)   │  │
│  │  9. news-event-analysis-node   (News impact)        │  │
│  │  10. ai-ml-ensemble-node       (AI/ML scoring)      │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                    │
│                         ▼                                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │          VALIDATORS (Proof-of-Intelligence)          │  │
│  │                                                       │  │
│  │  11. signal-validator          (PoI/PoInsight)      │  │
│  │  12. mentorchain-orchestrator  (Mentor review)      │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                    │
│                         ▼                                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              EXECUTORS (Output Actions)              │  │
│  │                                                       │  │
│  │  13. exchange-execution-node   (Trade execution)    │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                    │
│                         ▼                                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           OBSERVERS (Telemetry & Monitoring)         │  │
│  │                                                       │  │
│  │  14. telemetry-log-node        (TSSD logging)       │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Signal Lifecycle

**1. Signal Creation:**
- Generators produce raw signals from various data sources
- Each signal has a unique `signalId` and `traceId`
- Initial signal schema: type, data, timestamp, source

**2. Signal Enrichment:**
- Analyzers add layers of analysis (technical, pattern, sentiment, news, AI/ML)
- Enrichment profile determines which analyzers to apply
- Result: `EnrichedSignal` with multiple analysis layers

**3. Signal Scoring:**
- Scorers (e.g., Froggy) produce final scores with breakdowns
- PoI (Proof-of-Intelligence): Capability assessment
- PoInsight (Proof-of-Insight): Usefulness assessment
- Result: `ScoredSignal` with composite score and confidence

**4. Signal Validation:**
- Validators assess signal quality and novelty
- MentorChain orchestrator coordinates mentor review
- Deterministic checks: schema validation, threshold checks, novelty scoring
- Result: `ValidatedSignal` with validator decisions

**5. Signal Execution (Optional):**
- Executor nodes route signals to trading systems
- Grid trading, DCA, market making, arbitrage strategies
- Result: Execution receipt and performance tracking

**6. Signal Observability:**
- Telemetry node logs all signals to TSSD vault
- Full provenance: signalId → enrichment → scoring → validation → execution
- Codex replay capability for audits and determinism testing

### Signal Schemas

**Universal Signal Ingestion Schema** (afi-artifacts):
```json
{
  "signalId": "alpha-001",
  "timestamp": "2025-12-19T19:00:00Z",
  "source": "market-data-streamer",
  "type": "market-data",
  "data": {
    "symbol": "BTCUSDT",
    "price": 50000,
    "volume": 1000
  }
}
```

**Vaulted TSSD Schema** (afi-artifacts):
```json
{
  "signalId": "alpha-001",
  "vault_timestamp": "2025-12-19T19:01:00Z",
  "enrichment": { ... },
  "scoring": { ... },
  "validation": { ... },
  "execution": { ... }
}
```

**Froggy Enriched View** (afi-core):
```typescript
{
  signalId: "alpha-001",
  technical: { emaDistancePct, indicators, ... },
  pattern: { regime, harmonics, ... },
  sentiment: { score, confidence, ... },
  newsFeatures: { hasNewsShock, headlineCount, ... },
  aiMl: { convictionScore, direction, regime, riskFlag }
}
```

### TSSD Vault (Time-Series Signal Database)

**Purpose:** Canonical storage for signal history and replay

**Key Features:**
- **Time-Series Storage:** MongoDB-based vault for signal records
- **Provenance Tracking:** Full signal lifecycle from ingestion to execution
- **Replay Capability:** Deterministic replay for audits and testing
- **Vault Clients:** TypeScript clients in afi-infra

**Vault Record Structure:**
```typescript
{
  _id: ObjectId,
  signalId: "alpha-001",
  traceId: "trace-123",
  vaultTimestamp: "2025-12-19T19:01:00Z",
  signal: { /* raw signal */ },
  enrichment: { /* enrichment layers */ },
  scoring: { /* PoI/PoInsight scores */ },
  validation: { /* validator decisions */ },
  execution: { /* execution results */ },
  provenance: {
    generator: "market-data-streamer",
    analyzers: ["technical-analysis-node", ...],
    scorer: "froggy-scorer",
    validator: "signal-validator"
  }
}
```

**TSSD Operations:**
- `write(record)` - Write signal record to vault
- `read(signalId)` - Read signal record by ID
- `replay(filters)` - Replay signals matching filters
- `query(timeRange, filters)` - Query signals by time range

---

## Token Economics & Minting

### AFI Token (xERC20)

**Contract:** `AFIToken.sol` (afi-token)

**Key Properties:**
- **Standard:** ERC-20 with xERC20 cross-chain compatibility
- **Supply Cap:** 86,000,000,000 AFI (86 billion with 18 decimals)
- **Emissions Entrypoint:** `mintEmissions(address beneficiary, uint256 amount)`
- **Role-Based Access:** `EMISSIONS_ROLE` gates minting
- **Provenance Events:** `EmissionsMinted(address indexed beneficiary, uint256 amount)`

**Deployment:**
- **Primary Chain:** Base (canonical source)
- **Future Chains:** Cross-chain via xERC20 standard
- **Testnet:** Base Sepolia (`0x43DC488caF49495d6abC0eEe021B725be38E81bd`)

**Roles:**
- `DEFAULT_ADMIN_ROLE` - Policy owner (Base Treasury Safe)
- `EMISSIONS_ROLE` - Emissions controller (MintCoordinator)

### Mint Coordinator

**Contract:** `AFIMintCoordinator.sol` (afi-token)

**Purpose:** Orchestrate token + receipt mints with signal/epoch metadata

**Key Functions:**
- `coordinateMint(beneficiary, amount, signalId, epochId, metadata)` - Main entrypoint
- Mints AFI tokens via `AFIToken.mintEmissions()`
- Mints receipt NFT via `AFISignalReceipt.mint()`
- Links token mint to signal provenance
- Emits `MintCoordinated(beneficiary, amount, signalId, epochId, receiptTokenId)`

### Signal Receipts

**Contract:** `AFISignalReceipt.sol` (afi-token)

**Standard:** ERC-1155 (multi-token)

**Purpose:** NFT receipts for mint provenance tracking

**Token Metadata:**
```json
{
  "tokenId": 1,
  "beneficiary": "0x...",
  "amount": "1000000000000000000000",
  "signalId": "alpha-001",
  "epochId": 5,
  "timestamp": "2025-12-19T19:00:00Z"
}
```

**Use Cases:**
- Audit trail for token minting
- Proof of signal contribution
- Governance voting rights (future)

### Minting Pipeline

**Off-Chain Coordination (afi-mint):**
```
1. Signal Validation
   └─> Signal scored and validated by afi-reactor

2. Threshold Check
   └─> Ensure sufficient qualified signals

3. Challenge Window
   └─> Allow disputes or slashing events (48 hours)

4. Mint Eligibility
   └─> Check minting thresholds and supply cap

5. Mint Trigger
   └─> Call MintCoordinator.coordinateMint()

6. Codex Recording
   └─> Log mint event to Mint Codex
```

**On-Chain Execution (afi-token):**
```
1. MintCoordinator receives coordinateMint() call

2. Validate parameters:
   - Beneficiary address
   - Amount within limits
   - Signal ID exists
   - Epoch ID valid

3. Mint AFI tokens:
   └─> AFIToken.mintEmissions(beneficiary, amount)

4. Mint receipt NFT:
   └─> AFISignalReceipt.mint(beneficiary, tokenId, metadata)

5. Emit provenance event:
   └─> MintCoordinated(beneficiary, amount, signalId, epochId, receiptTokenId)
```

### Epoch Pulse

**Concept:** Governance and emissions rhythm (heartbeat of AFI)

**Epoch Transitions:**
- Epoch duration: Configurable (e.g., 7 days)
- Transition logic: Automated via governance contracts
- Emissions schedule: Per-epoch minting caps

**Deferred Staking:**
- Staking activates after 1,000,000,000 AFI minted
- Until then: Validators operate without staking
- After threshold: Vote-weighted governance and staking rewards

### Reputation Scoring

**Composite Reputation Formula:**
```
Reputation = α × PoI + β × PoInsight

Where:
- α = 0.3 (PoI weight - capability)
- β = 0.7 (PoInsight weight - usefulness)
- PoI ∈ [0, 1] (success rate, latency)
- PoInsight ∈ [0, 1] (IC, hit rate, Sharpe)
```

**Evidence-Based Shrinkage:**
```
adjusted_score = (n × raw_score + n0 × neutral_prior) / (n + n0)

Where:
- n = evidence count (number of signals)
- n0 = 100 (shrinkage parameter)
- neutral_prior = 0.5 (neutral reputation)
- raw_score = observed performance
```

**Confidence Intervals:**
```
CI = [score - 1.96 × SE, score + 1.96 × SE]

Where:
- SE = standard error based on sample size
- 1.96 = 95% confidence z-score
```

**Benchmark Results (afi-benchkit):**
```json
{
  "poi": {"score": 0.85, "raw": 0.92, "ci": [0.78, 0.92]},
  "poinsight": {"score": 0.73, "raw": 0.68, "ci": [0.65, 0.81]},
  "reputation": {"score": 0.77, "alpha": 0.3, "beta": 0.7},
  "n": 150,
  "n_detail": {"poi": 80, "poinsight": 70}
}
```

---

## Infrastructure & Operations

### TSSD Vault Architecture

**Components:**
- **MongoTSSDVaultClient** (afi-infra): TypeScript client for vault operations
- **Database:** MongoDB (separate from Eliza gateway DB)
- **Collections:** `signals`, `vault_records`, `replay_logs`

**Vault Responsibilities:**
- Signal ingestion and storage
- Enrichment/scoring/validation history
- Replay and audit capability
- Provenance tracking

### Deployment Architecture

**Local Development:**
```bash
# Start AFI Reactor (backend)
cd afi-reactor
npm run dev
# Runs on http://localhost:8080

# Start AFI Eliza Gateway (agent runtime)
cd afi-gateway
npm run dev
# Runs ElizaOS runtime with character configs

# Start Tiny Brains (AI/ML service)
cd afi-tiny-brains
uvicorn tiny_brains_service.service:app --port 8090
```

**Health Checks (afi-ops):**
```bash
# Check all services
npm run health

# Check specific service
./scripts/health/check-health.sh afi-reactor

# View operations status
npm run status
```

**Local Deployment Script:**
```bash
# Deploy all services
npm run deploy:local

# Deploy specific services
./scripts/run-local-deploy.sh --services afi-core,afi-reactor

# Dry run (show plan)
./scripts/run-local-deploy.sh --dry-run
```

### Service Level Objectives (SLO)

**Availability Targets (afi-ops):**
- afi-reactor: 99.5% uptime
- afi-core: 99.5% uptime
- afi-gateway: 99.0% uptime
- afi-tiny-brains: 95.0% uptime (fail-soft design)

**Performance Targets:**
- Signal processing latency: p95 < 1000ms
- DAG execution time: p95 < 5000ms
- TSSD vault write: p95 < 500ms
- Health check response: p95 < 100ms

**Monitoring:**
- Prometheus metrics collection
- Grafana dashboards (planned)
- Sentry error tracking
- AgentOps metadata reporting

### Configuration Management

**afi-config Responsibilities:**
- Global JSON schemas (character, pipeline, blueprint, plugin-manifest, vault, codex)
- Configuration templates
- CLI validation utilities
- Codex governance artifacts (AFI Droid Charter v0.1)

**Configuration Files:**
- `.env` - Environment variables (secrets, URLs, ports)
- `config/*.codex.json` - DAG and Codex configurations
- `templates/` - Starter config files
- `schemas/` - JSON Schema definitions

---

## Agent System

### Agent Architecture

**Core Agents:**
- **Phoenix** - AFI Protocol's frontline agent and primary voice (concierge)
- **Alpha** - Scout agent (signal discovery)
- **Val Dook** - Validator agent (signal validation)
- **Froggy** - Strategy scorer (trend/pullback analysis)
- **Pixel Rick** - Additional character (afi-gateway)

**Agent Lifecycle:**
1. **Initialization:** Load character config from afi-gateway
2. **Runtime:** ElizaOS runtime with AFI plugins
3. **Signal Processing:** Participate in DAG pipeline
4. **Mentorship:** Mentor-agent review via MentorChain
5. **Governance:** Proposal submission and voting (future)

### Character Configs

**Phoenix Character** (afi-gateway):
```typescript
{
  name: "Phoenix",
  modelProvider: "openai",
  settings: {
    voice: "warm_technical",
    tone: "clear_and_concise"
  },
  bio: [
    "AFI Protocol's frontline agent",
    "Explains AFI's 'financial brain' in plain language",
    "Acts as concierge, not the tool itself"
  ],
  messageExamples: [ ... ],
  postExamples: [ ... ],
  topics: ["AFI Protocol", "Signal lifecycle", ...],
  style: {
    all: ["Warm", "Technically fluent", "Clear"],
    chat: ["Concise", "Helpful", "No financial advice"],
    post: ["Engaging", "Educational", "Neutral"]
  },
  adjectives: ["Warm", "Technically fluent", ...]
}
```

**Agent Boundaries:**
- ✅ Explain how AFI Protocol works
- ✅ Help users understand intelligence outputs
- ✅ Point to documentation and resources
- ❌ Provide financial advice or trade recommendations
- ❌ Guarantee returns, yields, or APY
- ❌ Execute transactions or sign contracts
- ❌ Access user funds or wallet

### Agent Skills (afi-skills)

**Skill Structure:**
```yaml
---
id: market-sentiment-analysis
name: Market Sentiment Analysis
version: 1.0.0
domain: news-sentiment
description: Analyze market sentiment from social and news sources
inputs:
  - name: social_signals
    type: array
    description: Array of social media signals
  - name: news_headlines
    type: array
    description: Array of news headlines
outputs:
  - name: sentiment_score
    type: number
    description: Sentiment score [-1, 1]
  - name: confidence
    type: number
    description: Confidence level [0, 1]
allowed_tools:
  - tssd:read
  - codex:replay
risk_level: medium
determinism_required: false
evals:
  golden_cases_path: evals/news-sentiment/market-sentiment-analysis/golden_cases.json
  expected_properties:
    - sentiment_score
    - confidence
owners:
  - afi-skills-team
last_updated: 2025-12-01
tags:
  - sentiment
  - news
  - social
---

# Market Sentiment Analysis Skill

[Skill body with detailed implementation notes]
```

**Skill Domains:**
- `market-structure/` - Futures, perps, contract specs
- `scoring/` - Signal scoring, epoch emissions
- `news-sentiment/` - Source trust, headline analysis
- `provenance/` - Receipt verification, vault replay
- `technical/` - Technical analysis indicators
- `pattern/` - Chart pattern recognition
- `ml/` - Machine learning models
- `ops/` - Operational utilities
- `governance/` - Governance proposals

**Skill Promotion Gates:**
- ✅ Front-matter validates against schema
- ✅ No security risk patterns detected
- ✅ Golden cases pass (if determinism_required: true)
- ✅ Code review by skill domain owner

### Agent Factory (afi-factory)

**Purpose:** Agent templates and spawning logic

**Agent Manifest:**
```json
{
  "agents": [
    {
      "id": "validator-agent-v1",
      "name": "Validator Agent",
      "version": "1.0.0",
      "template": "templates/validator-agent.yaml",
      "skills": [
        "signal-validation",
        "poi-scoring",
        "poinsight-scoring"
      ],
      "role": "validator"
    },
    {
      "id": "scorer-agent-v1",
      "name": "Scorer Agent",
      "version": "1.0.0",
      "template": "templates/scorer-agent.yaml",
      "skills": [
        "signal-scoring",
        "ensemble-scoring"
      ],
      "role": "scorer"
    }
  ]
}
```

**Agent Spawning:**
1. Load template from afi-factory
2. Inject skills from afi-skills
3. Configure character from afi-config
4. Deploy to afi-core runtime
5. Register with afi-reactor DAG

---

## Integration & Extensions

### Plugin System (afi-plugins)

**Plugin Architecture:**
```typescript
interface Plugin {
  id: PluginId;
  name: string;
  version: string;
  kind: PluginKind; // signal-generator, analyzer, scorer, validator, executor, observer
  description: string;
  inputs: PluginInput[];
  outputs: PluginOutput[];
  config?: PluginConfig;
  execute: (context: PluginContext) => Promise<PluginResult>;
}
```

**Plugin Kinds:**
1. **signal-generator** - Generate raw signals from data sources
2. **analyzer** - Analyze and enrich signals in DAG pipeline
3. **scorer** - Produce scored signals with breakdowns
4. **validator** - Validate signals and strategies
5. **executor** - Execute trading strategies
6. **observer** - Observe and log system behavior

**Seeded Plugins (Phase 1 - STUBS):**
```
afi.blofin.trendPullback      - Blofin perp trend/pullback signal generator
afi.core.greeksDecayAnalyzer  - Options Greeks decay analyzer
afi.scorer.signalScorer       - Signal scorer (composite score + breakdowns)
afi.validator.halfDecayReplay - Half-decay replay validator
afi.observer.signalTelemetry  - Signal lifecycle telemetry observer
afi.executor.gridTrading      - Grid trading strategy executor
```

**Plugin Registration:**
```typescript
import { getAllPlugins, getPluginById, filterPluginsByKind } from "afi-plugins";

// Get all plugins
const plugins = getAllPlugins();

// Get specific plugin
const plugin = getPluginById("afi.blofin.trendPullback");

// Filter by category
const generators = filterPluginsByKind("signal-generator");
const analyzers = filterPluginsByKind("analyzer");
```

### ElizaOS Integration (afi-gateway)

**Integration Model:**
```
┌─────────────────────────────────────┐
│  afi-gateway (this repo)            │
│  - Eliza character configs          │
│  - AFI-specific Eliza plugins       │
│  - HTTP/WS clients                  │
└──────────────┬──────────────────────┘
               │
               │ HTTP/WS API calls
               ▼
┌─────────────────────────────────────┐
│  AFI Services                       │
│  - afi-reactor (DAG orchestration)  │
│  - afi-core (validators, scoring)   │
│  - Codex (signal replay)            │
└─────────────────────────────────────┘
```

**Dependency Direction:**
- Gateway (afi-gateway) → **depends on** → AFI services
- AFI services → **never depend on** → Gateway

**Integration Principles:**
1. **AFI is the backend** - Gateway is a client, not the source of truth
2. **Call, don't reimplement** - Always call AFI APIs instead of duplicating logic
3. **Types from afi-core** - Import shared types and client libraries
4. **No direct DB access** - All AFI data access via HTTP/WS APIs
5. **Eliza stays external** - Upstream ElizaOS never vendored into AFI repos

**HTTP Endpoints:**
- `GET /` - ElizaOS Web UI (interactive chat)
- `GET /health` - Health check with agent status
- `GET /api/agents` - List all agents (Phoenix, Alpha, Froggy, Val Dook, Pixel Rick)
- `POST /api/agents/:id/message` - Send message to specific agent
- `ws://localhost:8080/` - WebSocket for real-time chat

### AI/ML Integration (afi-tiny-brains)

**Purpose:** ML-based predictions for Froggy enrichment pipeline

**Three Brains:**
1. **Chronos Brain** - Time-series forecasting (Chronos-Bolt or heuristics)
2. **HMM Brain** - Hidden Markov Model for regime detection (bull/bear/choppy)
3. **LightGBM Brain** - Meta-learner for conviction scoring

**Request Flow:**
```
1. Froggy enrichment adapter builds TinyBrainsFroggyInput
2. HTTP POST to {TINY_BRAINS_URL}/predict/froggy
3. Service runs three brains (parallel/sequence)
4. Returns FroggyAiMlV1 (convictionScore, direction, regime, riskFlag)
5. Attached to FroggyEnrichedView.aiMl field
```

**Model Types:**
- **Chronos:** Pre-trained from Hugging Face (amazon/chronos-bolt-small)
- **HMM:** Trained from historical OHLCV data via `scripts/train_hmm_froggy.py`
- **LightGBM:** Meta-learner trained via `scripts/train_lightgbm_froggy.py`

**Fail-Soft Design:**
- Models not loaded → heuristic fallbacks
- Missing features → neutral predictions with low conviction
- Service always returns valid response (never errors)

**Health Check:**
```bash
curl http://localhost:8090/health

Response:
{
  "status": "ok",
  "chronos": "model",  // or "heuristic"
  "hmm": "model",      // or "heuristic"
  "lightgbm": "model"  // or "unavailable"
}
```

---

## Governance & Coordination

### AFI Droid Charter v0.1

**Location:** `afi-config/codex/governance/droids/AFI_DROID_CHARTER.v0.1.md`

**Purpose:** Global authority for all agent/droid behavior in AFI Protocol

**Key Principles:**
1. **Global Authority:** All agents must follow this charter
2. **Repo-Specific Rules:** Each repo's `AGENTS.md` adds constraints
3. **Conflict Resolution:** If `AGENTS.md` conflicts with Charter, Charter wins
4. **Security-Critical Repos:** Smart contracts, minting, governance require explicit human approval
5. **No-Op Preference:** When unsure, prefer no-op over risky changes

### Governance Proposals

**Universal Proposal Signal Schema** (afi-governance):
```json
{
  "proposalId": "prop-001",
  "type": "governance",
  "title": "Increase validator rewards",
  "description": "Proposal to increase validator rewards by 10%",
  "author": "0x...",
  "timestamp": "2025-12-19T19:00:00Z",
  "scoring": {
    "clarity": 0.8,
    "feasibility": 0.7,
    "risk": 0.3,
    "alignment": 0.9
  },
  "voting": {
    "quorum": 1000000,
    "threshold": 0.66,
    "startTime": "2025-12-20T00:00:00Z",
    "endTime": "2025-12-27T00:00:00Z"
  }
}
```

**Proposal Lifecycle:**
1. **Submission:** Agent or human submits proposal
2. **Scoring:** Scoring agents evaluate (clarity, feasibility, risk, alignment)
3. **Review:** Validator agents review and provide feedback
4. **Voting:** Token holders vote (after staking threshold)
5. **Execution:** Passed proposals executed via governance contracts

### Codex System

**Codex Metadata Schema** (afi-config):
```json
{
  "name": "afi-reactor",
  "version": "0.2.0",
  "description": "DAG orchestrator for AFI Protocol",
  "capabilities": [
    "15-node-pipeline",
    "signal-replay",
    "deterministic-execution"
  ],
  "dependencies": {
    "afi-core": "^0.2.0",
    "afi-config": "^0.1.0"
  },
  "provenance": {
    "gitSha": "abc123...",
    "buildTimestamp": "2025-12-19T19:00:00Z",
    "builder": "github-actions"
  }
}
```

**Codex Replay:**
- All DAG runs logged to Codex
- Deterministic replay capability
- Audit trail for governance decisions
- Provenance tracking for signal lifecycle

---

## Development & Testing

### Testing Strategy

**Unit Tests:**
- `afi-core`: Vitest (validators, scorers, schemas)
- `afi-reactor`: Jest (DAG nodes, plugins)
- `afi-token`: Foundry (58 tests - roles, cap, core, receipts, coordinator, integration)
- `afi-infra`: Vitest (TSSD clients, DAG determinism)
- `afi-plugins`: Vitest (plugin interfaces)
- `afi-skills`: Vitest (skill linter, manifest builder)
- `afi-tiny-brains`: pytest (model tests, API tests)

**Integration Tests:**
- `afi-reactor`: End-to-end pipeline tests
- `afi-gateway`: Prize demo integration tests
- `afi-token`: MintCoordinatorIntegration.t.sol (6 tests)

**Benchmark Tests:**
- `afi-benchkit`: PoI and PoInsight benchmark suites
- Deterministic harness with golden outputs
- Hash verification for bit-for-bit reproducibility

**Smoke Tests:**
- `afi-artifacts`: Replay smoke tests
- `afi-gateway`: AFIScout smoke test
- `afi-ops`: Health check smoke tests

### CI/CD Pipelines

**GitHub Actions Workflows:**

**afi-reactor:**
```yaml
name: AFI-Reactor Validation
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm install
      - run: npm test
      - run: npm run validate-all
      - run: npm run simulate-signal
```

**afi-token:**
```yaml
name: Forge CI
on: [push, pull_request]
jobs:
  test-full-suite:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: foundry-rs/foundry-toolchain@v1
        with:
          version: nightly-cd86772a837b3f9e467f863ccfd090783ac2cd1b
      - run: forge install
      - run: forge build
      - run: forge test -vv
  
  test-mainnet-safety:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: foundry-rs/foundry-toolchain@v1
      - run: forge test --match-path="test/AFITokenRoles.t.sol" -vv
      - run: forge test --match-path="test/AFITokenCap.t.sol" -vv
      - run: forge test --match-path="test/MintCoordinatorIntegration.t.sol" -vv
```

### Development Workflows

**Local Development:**
```bash
# 1. Install dependencies
npm install

# 2. Build TypeScript
npm run build

# 3. Run tests
npm test

# 4. Type check
npm run typecheck

# 5. Lint code
npm run lint

# 6. Validate configs
npm run validate
```

**Git Workflows:**
- **Base branch:** `main` or `migration/multi-repo-reorg`
- **Branch naming:** `feat/`, `fix/`, `docs/`, `refactor/`
- **Commit messages:** Conventional commits (e.g., `feat(core): add validator`)
- **Before committing:** Run tests, typecheck, lint

**Code Review:**
- All PRs require human review
- Security-critical repos require explicit sign-off
- Automated checks must pass (tests, lint, typecheck)
- Follow AFI Droid Charter and repo-specific `AGENTS.md`

---

## Deployment Architecture

### Production Deployment

**Base Chain (Primary):**
- **Network:** Base Mainnet
- **Contracts:** AFIToken, AFISignalReceipt, AFIMintCoordinator
- **RPC:** Alchemy/Infura Base RPC
- **Explorer:** BaseScan

**Testnet (Rehearsal):**
- **Network:** Base Sepolia
- **Contracts:** Deployed and verified
- **AFIToken:** `0x43DC488caF49495d6abC0eEe021B725be38E81bd`
- **AFISignalReceipt:** `0xD1aDC1Ca4A98B141D8f3a4fE2cb9638003E70e23`
- **AFIMintCoordinator:** `0xDd825a05EFe22668Ffbd627C586f19D08d62eA5e`

**Off-Chain Services:**

**afi-reactor (DAG Orchestrator):**
- **Platform:** Railway, Render, or dedicated server
- **Port:** 8080 (configurable via `AFI_REACTOR_PORT`)
- **Endpoints:** `/api/signals`, `/api/replay`, `/health`
- **Dependencies:** afi-core, afi-plugins, MongoDB (TSSD)

**afi-gateway (Agent Runtime):**
- **Platform:** Railway, Render, or dedicated server
- **Port:** 8080 (configurable via `PORT`)
- **Dependencies:** ElizaOS, OpenAI API, MongoDB (gateway DB)

**afi-tiny-brains (AI/ML Service):**
- **Platform:** Railway, Render, or dedicated server with GPU (optional)
- **Port:** 8090 (configurable via `TINY_BRAINS_PORT`)
- **Endpoints:** `/health`, `/predict/froggy`
- **Dependencies:** PyTorch (optional), scikit-learn, LightGBM

**afi-research-site (Web UI):**
- **Platform:** Vercel (recommended) or Netlify
- **Domain:** research.afi.org
- **Build:** Next.js static generation
- **Dependencies:** Agent service (port 8787)

### Environment Variables

**afi-reactor:**
```bash
# Service binding
AFI_REACTOR_PORT=8080

# MongoDB (TSSD Vault)
MONGODB_URI=mongodb+srv://...
UFBE_DB_NAME=afi_tssd

# AFI Services
AFI_CORE_URL=http://localhost:3000
TINY_BRAINS_URL=http://localhost:8090

# Logging
LOG_LEVEL=INFO
UFBE_DEBUG_AIML=0
```

**afi-gateway:**
```bash
# Service binding
PORT=8080

# OpenAI (required)
OPENAI_API_KEY=sk-...

# MongoDB (gateway-specific)
MONGODB_URI=mongodb+srv://...
AFI_MONGO_DB_NAME=afi_eliza

# AFI Reactor
AFI_REACTOR_BASE_URL=http://localhost:8080

# Discord (optional)
# DISCORD_APPLICATION_ID=...
# DISCORD_API_TOKEN=...
```

**afi-tiny-brains:**
```bash
# Service binding
TINY_BRAINS_HOST=0.0.0.0
TINY_BRAINS_PORT=8090

# Model configuration
CHRONOS_ENABLED=true
CHRONOS_MODEL_ID=amazon/chronos-bolt-small
HMM_MODEL_PATH=models/hmm_froggy.joblib
LIGHTGBM_MODEL_PATH=models/lightgbm_froggy.txt

# Logging
LOG_LEVEL=INFO
```

**afi-research-site:**
```bash
# Build SHA (auto from Vercel)
VERCEL_GIT_COMMIT_SHA=auto

# Sentry (optional)
SENTRY_DSN=https://...

# Agent service
NEXT_PUBLIC_AGENT_URL=http://localhost:8787

# Debug mode
NEXT_PUBLIC_AFI_ENABLE_DEBUG=false
UFBE_ENABLE_DEBUG=false
```

---

## Security Model

### Risk Classification

**HIGH RISK / CRITICAL:**
- `afi-token` - Smart contracts (permanent loss of funds)
- `afi-mint` - Minting coordination (affects token supply)
- `afi-governance` - Governance contracts (systemic impact)
- `afi-plugins` - Plugins execute in signal pipeline (security-critical)

**MEDIUM RISK (PROTOCOL-WIDE IMPACT):**
- `afi-math` - Pure math functions (changes affect all consumers)

**STANDARD RISK:**
- All other repos

### Security Principles

**1. Separation of Concerns:**
- On-chain logic (afi-token) separate from off-chain coordination (afi-mint)
- Runtime behavior (afi-core) separate from orchestration (afi-reactor)
- Configuration (afi-config) separate from implementation

**2. Least Privilege:**
- Role-based access control (RBAC) for smart contracts
- API authentication for off-chain services
- Environment-specific configurations

**3. Defense in Depth:**
- Multiple validation layers (generators → analyzers → validators)
- Challenge windows for minting disputes
- Fail-soft design for AI/ML services

**4. Auditability:**
- Full provenance tracking via TSSD vault
- Codex replay capability for audits
- Event emissions for all critical operations

**5. No Secrets in Code:**
- Environment variables for API keys
- Secure vaults for private keys
- No hardcoded credentials

### Attack Vectors & Mitigations

**1. Malicious Signals:**
- **Attack:** Fake or manipulated signals to trigger minting
- **Mitigation:** Multi-layer validation (PoI/PoInsight), challenge windows, novelty scoring

**2. Smart Contract Exploits:**
- **Attack:** Reentrancy, overflow, unauthorized minting
- **Mitigation:** OpenZeppelin contracts, Foundry tests (58 tests), external audit

**3. Validator Collusion:**
- **Attack:** Validators collude to approve invalid signals
- **Mitigation:** MentorChain orchestrator, reputation scoring, slashing (future)

**4. Plugin Injection:**
- **Attack:** Malicious plugin exfiltrates data or corrupts signals
- **Mitigation:** Plugin review, security scanning, sandboxing

**5. API Abuse:**
- **Attack:** Rate limiting bypass, denial of service
- **Mitigation:** Rate limiting (20 req/min per IP), request validation, circuit breakers

---

## Data Flow Diagrams

### Signal Processing Flow

```
┌─────────────────────────────────────────────────────────────┐
│                  Signal Processing Flow                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  [External Data Sources]                                     │
│         │                                                    │
│         ├─> Market Feeds (price, volume)                    │
│         ├─> On-Chain Data (blockchain events)               │
│         ├─> Social Signals (Twitter, Reddit)                │
│         ├─> News Feeds (financial news)                     │
│         └─> AI Strategies (ML models)                       │
│                    │                                         │
│                    ▼                                         │
│           [GENERATORS]                                       │
│                    │                                         │
│                    ▼                                         │
│           [Raw Signal]                                       │
│            signalId: "alpha-001"                            │
│            type: "market-data"                              │
│            data: { ... }                                    │
│                    │                                         │
│                    ▼                                         │
│           [ANALYZERS]                                        │
│                    │                                         │
│                    ├─> Technical Analysis                   │
│                    ├─> Pattern Recognition                  │
│                    ├─> Sentiment Analysis                   │
│                    ├─> News Event Analysis                  │
│                    └─> AI/ML Ensemble                       │
│                    │                                         │
│                    ▼                                         │
│         [Enriched Signal]                                    │
│          technical: { ... }                                 │
│          pattern: { ... }                                   │
│          sentiment: { ... }                                 │
│          newsFeatures: { ... }                              │
│          aiMl: { ... }                                      │
│                    │                                         │
│                    ▼                                         │
│            [SCORERS]                                         │
│                    │                                         │
│                    ├─> Froggy Scorer                        │
│                    └─> MentorChain Orchestrator             │
│                    │                                         │
│                    ▼                                         │
│        [Scored Signal]                                    │
│         score: 0.85                                       │
│         conviction: 0.72                                  │
│         direction: "long"                                 │
│         breakdown: { ... }                                │
│                    │                                         │
│                    ▼                                         │
│          [VALIDATORS]                                        │
│                    │                                         │
│                    ├─> Signal Validator (PoI/PoInsight)     │
│                    └─> MentorChain Orchestrator             │
│                    │                                         │
│                    ▼                                         │
│        [Validated Signal]                                    │
│         validation: { ... }                                 │
│         poi: 0.85                                           │
│         poinsight: 0.73                                     │
│         reputation: 0.77                                    │
│                    │                                         │
│                    ├─> [EXECUTORS] (optional)               │
│                    │    └─> Exchange Execution              │
│                    │                                         │
│                    └─> [OBSERVERS]                          │
│                         └─> Telemetry Log                   │
│                         │                                    │
│                         ▼                                    │
│                   [TSSD Vault]                              │
│                    Full signal record                       │
│                    Provenance tracking                      │
│                    Replay capability                        │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Minting Flow

```
┌─────────────────────────────────────────────────────────────┐
│                      Minting Flow                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  [Validated Signal]                                          │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────────────────────────────┐                   │
│  │   afi-mint (Off-Chain Coordination)  │                   │
│  │                                       │                   │
│  │  1. Threshold Check                  │                   │
│  │     └─> Sufficient qualified signals │                   │
│  │                                       │                   │
│  │  2. Challenge Window (48h)           │                   │
│  │     └─> Allow disputes/slashing      │                   │
│  │                                       │                   │
│  │  3. Mint Eligibility                 │                   │
│  │     └─> Check thresholds & cap       │                   │
│  │                                       │                   │
│  │  4. Mint Trigger                     │                   │
│  │     └─> Call MintCoordinator         │                   │
│  └──────────────────┬───────────────────┘                   │
│                     │                                        │
│                     ▼                                        │
│  ┌──────────────────────────────────────┐                   │
│  │  afi-token (On-Chain Execution)      │                   │
│  │                                       │                   │
│  │  AFIMintCoordinator.coordinateMint() │                   │
│  │                     │                 │                   │
│  │                     ├─> Validate params                   │
│  │                     │                                     │
│  │                     ├─> AFIToken.mintEmissions()         │
│  │                     │   └─> Mint AFI tokens             │
│  │                     │                                     │
│  │                     ├─> AFISignalReceipt.mint()          │
│  │                     │   └─> Mint receipt NFT            │
│  │                     │                                     │
│  │                     └─> Emit MintCoordinated event       │
│  └──────────────────┬───────────────────┘                   │
│                     │                                        │
│                     ▼                                        │
│         [Mint Codex Recording]                              │
│          beneficiary: 0x...                                 │
│          amount: 1000 AFI                                   │
│          signalId: "alpha-001"                              │
│          epochId: 5                                         │
│          receiptTokenId: 1                                  │
│          timestamp: "2025-12-19T19:00:00Z"                  │
│                     │                                        │
│                     └─> [Audit Trail]                       │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## Key Concepts & Terminology

### Signal Types
- **Raw Signal** - Unprocessed data from generators
- **Enriched Signal** - Signal with analysis layers added
- **Scored Signal** - Signal with final score and breakdowns
- **Validated Signal** - Signal approved by validators

### Proof Systems
- **PoI (Proof-of-Intelligence)** - Validator capability assessment (success rate, latency)
- **PoInsight (Proof-of-Insight)** - Validator usefulness assessment (IC, hit rate, Sharpe)
- **PoInt (Proof-of-Intelligence, Testbed)** - Modal testbed for PoI/PoInsight

### Repositories
- **Core Repos** - afi-config, afi-core, afi-reactor
- **Token Repos** - afi-token, afi-mint, afi-governance, afi-math, afi-econ
- **Infra Repos** - afi-infra, afi-ops
- **Extension Repos** - afi-plugins, afi-skills, afi-factory, afi-starters
- **Integration Repos** - afi-gateway, afi-tiny-brains
- **Doc Repos** - afi-docs, afi-artifacts, afi-benchkit

### Agent Types
- **Validator Agents** - Assess signal quality (PoI/PoInsight)
- **Scorer Agents** - Produce final scores (Froggy)
- **Generator Agents** - Produce raw signals
- **Analyzer Agents** - Enrich signals with analysis
- **Executor Agents** - Execute trading strategies
- **Observer Agents** - Monitor and log system behavior

### Roles & Permissions
- `DEFAULT_ADMIN_ROLE` - Policy owner (Base Treasury Safe)
- `EMISSIONS_ROLE` - Emissions controller (MintCoordinator)
- `MINTER_ROLE` - Token minter (deprecated in favor of EMISSIONS_ROLE)

### Standards
- **xERC20** - Cross-chain ERC-20 standard
- **ERC-1155** - Multi-token NFT standard (receipts)
- **ESM** - ECMAScript Modules (TypeScript)
- **Codex** - Canonical registry for schemas, policies, provenance
- **TSSD** - Time-Series Signal Database

### Governance
- **Epoch Pulse** - Governance and emissions rhythm
- **Universal Proposal Signal** - Standardized proposal schema
- **Challenge Window** - Dispute period before minting (48 hours)
- **Staking Threshold** - 1B AFI minted before staking activates

### Testing & Quality
- **Golden Cases** - Reference test data for deterministic validation
- **Smoke Tests** - Quick sanity checks
- **Integration Tests** - End-to-end pipeline tests
- **Benchmark Tests** - PoI/PoInsight performance validation

---

## Appendix: Quick Reference

### Repository URLs (GitHub)

**Core:**
- https://github.com/AFI-Protocol/afi-config
- https://github.com/AFI-Protocol/afi-core
- https://github.com/AFI-Protocol/afi-reactor

**Token:**
- https://github.com/AFI-Protocol/afi-token
- https://github.com/AFI-Protocol/afi-mint
- https://github.com/AFI-Protocol/afi-governance
- https://github.com/AFI-Protocol/afi-math
- https://github.com/AFI-Protocol/afi-econ

**Infra:**
- https://github.com/AFI-Protocol/afi-infra
- https://github.com/AFI-Protocol/afi-ops

**Extensions:**
- https://github.com/AFI-Protocol/afi-plugins
- https://github.com/AFI-Protocol/afi-skills
- https://github.com/AFI-Protocol/afi-factory
- https://github.com/AFI-Protocol/afi-starters

**Integration:**
- https://github.com/AFI-Protocol/afi-gateway
- https://github.com/AFI-Protocol/afi-tiny-brains

**Documentation:**
- https://github.com/AFI-Protocol/afi-docs
- https://github.com/AFI-Protocol/afi-artifacts
- https://github.com/AFI-Protocol/afi-benchkit

**SDKs:**
- https://github.com/AFI-Protocol/afi-sdk-ts
- https://github.com/AFI-Protocol/afi-sdk-python

**Other:**
- https://github.com/AFI-Protocol/afi-protocol
- https://github.com/AFI-Protocol/afi-labs
- https://github.com/AFI-Protocol/afi-assets
- https://github.com/AFI-Protocol/afi-research-site

### Key Commands

**Development:**
```bash
# Build
npm run build

# Test
npm test

# Type check
npm run typecheck

# Lint
npm run lint

# Validate
npm run validate
```

**Deployment:**
```bash
# Local deployment
npm run deploy:local

# Health checks
npm run health

# Operations status
npm run status
```

**Signal Processing:**
```bash
# Simulate signal
npm run simulate-signal

# Replay from vault
npm run replay-vault

# Mentor evaluation
npm run mentor-eval
```

**Smart Contracts:**
```bash
# Build contracts
forge build

# Run tests
forge test

# Deploy (local)
forge script script/DeployAFILocal.s.sol --rpc-url local --broadcast
```

---

**End of Architecture Documentation**

For repository-specific details, see `AFI_Repository_Map.md`.
