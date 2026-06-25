# AFI Protocol — End-to-End Pipeline Audit Report

> ⚠️ Historical snapshot. The legacy Froggy demo chain (Alpha Scout → Pixel Rick → Val Dook → Execution Sim) was removed; the reactor is scored-only. Canonical pipeline: afi-reactor/src/config/froggyPipeline.ts.

**Date**: 2025-12-09  
**Auditor**: AFI Repo Auditor & Backend Architect  
**Scope**: All AFI modular repos under `~/AFI_Modular_Repos/`

---

## Executive Summary

### Current Pipeline Status: **DEMO-READY, NOT PRODUCTION-READY**

**What's Real**:
- ✅ Complete 6-stage Froggy pipeline (Alpha → Pixel Rick → Froggy → Val Dook → Execution Sim → Vault)
- ✅ HTTP endpoints for TradingView webhooks and demo flows
- ✅ MongoDB TSSD vault persistence (Phase 1 complete)
- ✅ Vault replay functionality (Phase 2 complete)
- ✅ UWR scoring with afi-core canonical implementation
- ✅ Validator decision logic with approve/reject/flag thresholds
- ✅ ElizaOS integration with 5 agent personas

**What's Still Demo/Stubbed**:
- ⚠️ Enrichment data is mocked (no real market data APIs)
- ⚠️ Execution is simulated only (no real exchange connections)
- ⚠️ No AFI token minting or emissions (contracts exist but not wired to pipeline)
- ⚠️ No real-time data ingestion (TradingView webhook is the only entry point)
- ⚠️ No production-grade error handling, rate limiting, or authentication
- ⚠️ No Codex metadata logging to on-chain receipts

**Bottom Line**: The pipeline is **functionally complete for testing and demos**, but requires **real data sources, exchange integrations, and emissions wiring** for production use.

---

## 1. Pipeline Map (Current State)

### 1.1 Discovered AFI Repos

**Core Pipeline Repos**:
- `afi-reactor` — DAG orchestrator, HTTP server, Froggy pipeline service
- `afi-core` — Validators, analysts (Froggy), UWR scoring, signal schemas
- `afi-infra` — TSSD vault (MongoDB), types, schemas
- `afi-gateway` — ElizaOS integration, agent personas, AFI client

**Supporting Repos**:
- `afi-config` — JSON schemas for pipelines, characters, vault configs
- `afi-token` — AFI token contracts (Solidity), emissions coordinator
- `afi-mint` — Mint coordination logic (not yet wired to pipeline)
- `afi-ops` — Deployment scripts, health checks, SLO monitoring
- `afi-skills` — Skill registry (not used in current pipeline)
- `afi-plugins` — Plugin templates (not used in current pipeline)
- `afi-math` — Math utilities (used by afi-core for UWR)

**Non-Pipeline Repos** (out of scope):
- `afi-research-site` — Civic tech / budget transparency (separate concern)
- `afi-benchkit` — Python benchmarking suite for PoI/PoInsight
- `afi-labs` — Experimental code sandbox
- `afi-artifacts` — Paper artifacts and reproducibility pack
- `afi-docs`, `afi-governance`, `afi-factory` — Documentation and scaffolding

### 1.2 Signal Lifecycle Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         AFI SIGNAL PIPELINE                              │
│                    (Froggy Trend-Pullback v1)                            │
└─────────────────────────────────────────────────────────────────────────┘

HTTP Entry Points:
  POST /api/webhooks/uss          (afi-reactor) - Canonical USS v1.1 ingestion
  POST /api/webhooks/tradingview  (afi-reactor) - Legacy (deprecated)
  POST /demo/afi-eliza-demo       (afi-reactor)
  GET  /replay/signal/:signalId   (afi-reactor)

Pipeline Stages (USS v1.1 Canonical Flow):

1. WEBHOOK INGESTION & VALIDATION
   Layer:  HTTP webhook handler with AJV schema validation
   Input:  USS v1.1 JSON payload
   Output: context.rawUss (validated USS object)
   Status: ✅ Working (canonical USS v1.1 flow)

2. TELEMETRY DERIVATION
   Plugin: uss-telemetry-deriver (internal stage)
   Input:  context.rawUss
   Output: context.telemetry (routing/debug fields extracted from USS)
   Status: ✅ Working

3. ENRICHMENT (Pixel Rick - Enrichment Legos)
   Plugins: froggy-enrichment-tech-pattern.plugin.ts (parallel)
            froggy-enrichment-sentiment-news.plugin.ts (parallel)
            froggy-enrichment-adapter.plugin.ts (merge + AI/ML)
   Input:  context.rawUss (USS v1.1 signal)
   Output: FroggyEnrichedView (technical, pattern, sentiment, news, aiMl)
   Status: ⚠️ Working but MOCKED (no real market data APIs)

4. ANALYSIS (Froggy Analyst)
   Plugin: froggy.trend_pullback_v1.plugin.ts
   Calls:  afi-core/analysts/froggy.trend_pullback_v1.ts
   Input:  FroggyEnrichedView
   Output: FroggyAnalyzedSignal (UWR score + axes breakdown)
   Status: ✅ Working (canonical UWR implementation)

5. VALIDATION (Val Dook)
   Plugin: validator-decision-evaluator.plugin.ts
   Input:  FroggyAnalyzedSignal
   Output: ValidatorDecisionBase { decision, uwrConfidence, reasonCodes }
   Status: ✅ Working (threshold-based: approve ≥0.7, reject ≤0.3, flag otherwise)

6. EXECUTION (Execution Sim)
   Plugin: execution-agent-sim.plugin.ts
   Input:  ValidatorDecisionBase
   Output: ExecutionResult { status: "simulated", type: "buy"|"sell"|"hold" }
   Status: ⚠️ SIMULATED ONLY (no real exchange execution)

PERSISTENCE (TSSD Vault):
   Service: tssdVaultService.ts (afi-reactor)
   Client:  MongoTSSDVaultClient.ts (afi-infra)
   Storage: MongoDB time-series collection
   Status:  ✅ Working (Phase 1 + Phase 2 replay complete)
```

### 1.3 Existing HTTP Endpoints

**afi-reactor** (`src/server.ts`):
- `GET /health` — Health check
- `POST /api/webhooks/tradingview` — TradingView webhook (runs full pipeline)
- `POST /demo/afi-eliza-demo` — Demo endpoint with stage summaries
- `GET /replay/signal/:signalId` — Vault replay (Phase 2)

**afi-gateway** (`src/server-full.ts`):
- `GET /` — ElizaOS web UI
- `GET /health` — ElizaOS health check
- `GET /api/agents` — List all agents
- `GET /api/afi/info` — AFI gateway metadata
- WebSocket: `ws://localhost:8081/` — ElizaOS real-time messaging

### 1.4 CLI Entrypoints

**afi-reactor**:
- `npm run start:demo` — Start HTTP server
- `npm run simulate-signal` — Run full pipeline simulation
- `npm run replay:signal -- --id=<signalId>` — Replay signal from vault
- `npm test` — Run Jest tests

**afi-core**:
- `npm run simulate-signal` — Simulate signal processing
- `npm test` — Run Vitest tests

**afi-gateway**:
- `npm run dev:server-full` — Start ElizaOS server with all 5 agents
- `/afi eliza-demo` — CLI command (in ElizaOS chat)
- `/afi reactor status` — Check AFI Reactor health
- `/afi validator explain-last` — Explain last validator decision

---

## 2. Stage-by-Stage Analysis

### 2.1 INGESTION STAGE

**Current Entrypoint**: `POST /api/webhooks/tradingview` (afi-reactor/src/server.ts)

**What Exists**:
- ✅ HTTP endpoint accepts TradingView-like JSON payload
- ✅ Payload normalized by `alpha-scout-ingest.plugin.ts`
- ✅ Generates `signalId` if missing
- ✅ Wraps into `ReactorSignalEnvelope` with metadata
- ✅ Optional shared secret authentication (`WEBHOOK_SHARED_SECRET` env var)

**What's Missing for Real Pipeline**:
- ❌ No real-time data validation (price, volume, timestamp freshness)
- ❌ No rate limiting or DDoS protection
- ❌ No webhook signature verification (beyond optional shared secret)
- ❌ No duplicate signal detection
- ❌ No multi-source ingestion (only TradingView webhook)

**Minimal Changes Needed**:
1. Add webhook signature verification (HMAC-SHA256)
2. Add rate limiting middleware (express-rate-limit)
3. Add duplicate detection (check TSSD vault for existing signalId)
4. Add timestamp freshness validation (reject signals older than N minutes)

**Test Entry Point** (already exists):
```bash
curl -X POST http://localhost:8080/api/webhooks/tradingview \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "BTC/USDT",
    "timeframe": "1h",
    "strategy": "froggy_trend_pullback_v1",
    "direction": "long",
    "setupSummary": "Bullish pullback to 20 EMA"
  }'
```

---

### 2.2 ENRICHMENT STAGE

**Current Implementation**: `froggy-enrichment-adapter.plugin.ts` (afi-reactor/plugins/)

**What Exists**:
- ✅ Enrichment profile support (technical, pattern, sentiment, news, aiMl)
- ✅ Structured enrichment output (`FroggyEnrichedView`)
- ✅ Honors `enrichmentProfile` from signal metadata
- ✅ Demo data generation for all enrichment categories

**What's Missing for Real Pipeline**:
- ❌ **All enrichment data is MOCKED** (no real APIs)
- ❌ No technical indicator calculation (RSI, MACD, EMA, etc.)
- ❌ No pattern recognition (no real chart pattern detection)
- ❌ No sentiment analysis (no Twitter/Reddit/news APIs)
- ❌ No news aggregation (no NewsAPI, CoinDesk, etc.)
- ❌ No AI/ML model inference (no real model calls)

**Minimal Changes Needed**:
1. **Technical Indicators**: Integrate TradingView API or ccxt library for real OHLCV data
2. **Pattern Recognition**: Add TA-Lib or custom pattern detection
3. **Sentiment**: Integrate LunarCrush, Santiment, or custom Twitter scraper
4. **News**: Integrate NewsAPI, CoinDesk API, or RSS feeds
5. **AI/ML**: Add model inference endpoint (e.g., HuggingFace, OpenAI, or custom model)

**Test Entry Point** (needs to be added):
```typescript
// afi-reactor/scripts/test-enrichment.ts
import froggyEnrichmentAdapter from "../plugins/froggy-enrichment-adapter.plugin.js";

const structuredSignal = {
  signalId: "test-enrichment-001",
  score: 0,
  confidence: 0.5,
  timestamp: new Date().toISOString(),
  meta: {
    symbol: "BTC/USDT",
    market: "spot",
    timeframe: "1h",
    strategy: "froggy_trend_pullback_v1",
    direction: "long",
    enrichmentProfile: {
      technical: { enabled: true, preset: "trend_pullback" },
      pattern: { enabled: true, preset: "reversal_patterns" }
    }
  },
  structured: { normalizedTimestamp: new Date().toISOString(), hasValidMeta: true, structuredBy: "test" }
};

const enriched = await froggyEnrichmentAdapter.run(structuredSignal);
console.log(JSON.stringify(enriched, null, 2));
```

**HTTP Entry Point** (needs to be added):
```typescript
// Add to afi-reactor/src/server.ts
app.post("/test/enrichment", async (req, res) => {
  const structuredSignal = req.body;
  const enriched = await froggyEnrichmentAdapter.run(structuredSignal);
  res.json(enriched);
});
```

---

### 2.3 ANALYSIS / SCORING STAGE

**Current Implementation**: `froggy.trend_pullback_v1.plugin.ts` → `afi-core/analysts/froggy.trend_pullback_v1.ts`

**What Exists**:
- ✅ Canonical UWR scoring implementation
- ✅ 4-axis scoring (structure, execution, risk, insight)
- ✅ Weighted average formula with governance-approved weights
- ✅ Deterministic scoring (same input → same output)
- ✅ Notes/reason codes for low-scoring axes

**What's Missing for Real Pipeline**:
- ❌ No multi-strategy support (only `trend_pullback_v1`)
- ❌ No ensemble scoring (no combining multiple analysts)
- ❌ No time decay application (signals don't age)
- ❌ No novelty scoring (no comparison to historical signals)

**Minimal Changes Needed**:
1. Add time decay to UWR scores (use `applyTimeDecayToUwrScore` from afi-core)
2. Add novelty scoring (use `computeNoveltyScore` from afi-core)
3. Add multi-strategy routing (if strategy !== "froggy_trend_pullback_v1", route to different analyst)

**Test Entry Point** (already exists in tests):
```typescript
// afi-core/analysts/__tests__/froggy.trend_pullback_v1.test.ts
import { scoreFroggyTrendPullback } from "../froggy.trend_pullback_v1.js";

const input = {
  weeklyBias: "bullish",
  dailyBias: "bullish",
  haFlatBackConfirmed: true,
  distanceFromDailyEmaPct: 2.5,
  pulledBackIntoSweetSpot: true,
  brokeEmaWithBody: true,
  liquiditySwept: true,
  triggerPatternQuality: 3,
  atrRegime: "normal",
  rrMultiplePlanned: 3.0
};

const score = scoreFroggyTrendPullback(input);
console.log(score); // { uwrScore: 0.85, uwrAxes: {...}, notes: [...] }
```

**HTTP Entry Point** (needs to be added):
```typescript
// Add to afi-reactor/src/server.ts
app.post("/test/analysis", async (req, res) => {
  const enrichedSignal = req.body;
  const analyzed = await froggyAnalyst.run(enrichedSignal);
  res.json(analyzed);
});
```

---

### 2.4 VALIDATOR STAGE

**Current Implementation**: `validator-decision-evaluator.plugin.ts` (afi-reactor/plugins/)

**What Exists**:
- ✅ Threshold-based decision logic (approve ≥0.7, reject ≤0.3, flag otherwise)
- ✅ `ValidatorDecisionBase` envelope (afi-core contract)
- ✅ Reason codes for weak axes
- ✅ `uwrConfidence` derived from UWR score

**What's Missing for Real Pipeline**:
- ❌ No multi-validator consensus (only one validator: Val Dook)
- ❌ No validator reputation tracking
- ❌ No challenge/dispute mechanism
- ❌ No emissions eligibility check (no connection to afi-mint)

**Minimal Changes Needed**:
1. Add emissions eligibility flag to `ValidatorDecisionBase`
2. Add validator reputation lookup (from afi-core validator registry)
3. Add multi-validator support (run multiple validators, aggregate decisions)

**Test Entry Point** (already exists in tests):
```typescript
// afi-reactor/test/froggyPipeline.test.ts
import validatorDecisionEvaluator from "../plugins/validator-decision-evaluator.plugin.js";

const scoredSignal = {
  signalId: "test-validator-001",
  analysis: {
    uwrScore: 0.78,
    uwrAxes: { structureAxis: 0.8, executionAxis: 0.7, riskAxis: 0.6, insightAxis: 0.9 },
    notes: []
  }
};

const decision = await validatorDecisionEvaluator.run(scoredSignal);
console.log(decision); // { decision: "approve", uwrConfidence: 0.78, reasonCodes: [...] }
```

**HTTP Entry Point** (needs to be added):
```typescript
// Add to afi-reactor/src/server.ts
app.post("/test/validator", async (req, res) => {
  const analyzedSignal = req.body;
  const decision = await validatorDecisionEvaluator.run(analyzedSignal);
  res.json(decision);
});
```

---

## 3. Repo-by-Repo Readiness Checklist

### 3.1 afi-reactor

**Current State**: ✅ Core pipeline working, HTTP server functional, TSSD vault integration complete

**Missing for Real Pipeline**:
- [ ] Real enrichment data sources (TradingView API, ccxt, TA-Lib)
- [ ] Real exchange execution (ccxt, Binance API, etc.)
- [ ] Emissions wiring (call afi-mint coordinator after validator approval)
- [ ] Codex metadata logging (write to on-chain receipts)
- [ ] Production error handling (retry logic, circuit breakers)
- [ ] Rate limiting and authentication
- [ ] Webhook signature verification

**Files to Add/Modify**:
- `src/services/enrichmentService.ts` — Real market data integration
- `src/services/executionService.ts` — Real exchange execution
- `src/services/emissionsService.ts` — Call afi-mint coordinator
- `src/middleware/auth.ts` — Webhook authentication
- `src/middleware/rateLimit.ts` — Rate limiting

---

### 3.2 afi-core

**Current State**: ✅ Validators, analysts, UWR scoring all working

**Missing for Real Pipeline**:
- [ ] Multi-strategy analyst routing
- [ ] Time decay application to UWR scores
- [ ] Novelty scoring integration
- [ ] Validator reputation tracking
- [ ] Multi-validator consensus logic

**Files to Add/Modify**:
- `analysts/strategyRouter.ts` — Route signals to correct analyst based on strategy
- `validators/ValidatorRegistry.ts` — Track validator reputation
- `validators/MultiValidatorConsensus.ts` — Aggregate multiple validator decisions

---

### 3.3 afi-infra

**Current State**: ✅ TSSD vault (MongoDB) working, types defined

**Missing for Real Pipeline**:
- [ ] Codex metadata schema for on-chain receipts
- [ ] Receipt provenance service (link vault → on-chain receipts)
- [ ] Training data export (for model training)

**Files to Add/Modify**:
- `src/codex/ReceiptProvenanceService.ts` — Link TSSD vault to on-chain receipts
- `src/tssd/TrainingDataExporter.ts` — Export training-eligible signals

---

### 3.4 afi-gateway

**Current State**: ✅ ElizaOS integration working, 5 agents functional

**Missing for Real Pipeline**:
- [ ] Real-time signal submission from Alpha (not just demo)
- [ ] Multi-agent collaboration (Alpha → Pixel Rick → Froggy → Val Dook)
- [ ] Persistent conversation history (currently in-memory)

**Files to Add/Modify**:
- `plugins/afi-reactor-actions/index.ts` — Add `SUBMIT_SIGNAL` action for Alpha
- `src/afiClient.ts` — Add real-time signal submission

---

### 3.5 afi-token / afi-mint

**Current State**: ✅ Contracts deployed, mint coordinator logic exists

**Missing for Real Pipeline**:
- [ ] **Wire afi-mint to afi-reactor validator decisions**
- [ ] Epoch tracking and emissions calculation
- [ ] On-chain receipt minting (AFISignalReceipt ERC-1155)

**Files to Add/Modify**:
- `afi-mint/src/mintCoordinator.ts` — Accept validator decisions from afi-reactor
- `afi-reactor/src/services/emissionsService.ts` — Call mint coordinator after approval

---

### 3.6 afi-config

**Current State**: ✅ Schemas defined, templates available

**Missing for Real Pipeline**:
- [ ] Production pipeline configs (not just demo)
- [ ] Enrichment provider configs (API keys, endpoints)
- [ ] Validator threshold configs (governance-approved)

**Files to Add/Modify**:
- `templates/production-pipeline.json` — Production pipeline config
- `templates/enrichment-providers.json` — Real data source configs

---

## 4. Concrete Test Harness & Commands

### 4.1 End-to-End Smoke Test Script

**Location**: `afi-reactor/scripts/pipeline-smoke.ts`

```typescript
#!/usr/bin/env node
/**
 * AFI Pipeline Smoke Test
 *
 * Tests the full pipeline end-to-end:
 * 1. Submit TradingView-like payload
 * 2. Wait for pipeline completion
 * 3. Verify validator decision
 * 4. Check TSSD vault persistence
 * 5. Test vault replay
 */

import { runFroggyPipeline } from "../src/services/froggyDemoService.js";
import { getTssdCollection } from "../src/services/tssdVaultService.js";
import { replaySignalById } from "../src/services/vaultReplayService.js";

async function main() {
  console.log("🧪 AFI Pipeline Smoke Test\n");

  // Step 1: Submit signal
  console.log("1️⃣ Submitting test signal...");
  const payload = {
    symbol: "BTC/USDT",
    timeframe: "1h",
    strategy: "froggy_trend_pullback_v1",
    direction: "long" as const,
    setupSummary: "Smoke test signal",
    enrichmentProfile: {
      technical: { enabled: true, preset: "trend_pullback" },
      pattern: { enabled: true, preset: "reversal_patterns" }
    }
  };

  const result = await runFroggyPipeline(payload, { isDemo: false });
  console.log(`✅ Signal processed: ${result.signalId}`);
  console.log(`   Decision: ${result.validatorDecision.decision}`);
  console.log(`   UWR Score: ${result.uwrScore.toFixed(2)}`);
  console.log(`   Confidence: ${result.validatorDecision.uwrConfidence.toFixed(2)}\n`);

  // Step 2: Verify TSSD vault persistence
  console.log("2️⃣ Checking TSSD vault...");
  const collection = await getTssdCollection();
  if (collection) {
    const doc = await collection.findOne({ signalId: result.signalId });
    if (doc) {
      console.log(`✅ Signal found in vault: ${doc.signalId}\n`);
    } else {
      console.error(`❌ Signal NOT found in vault!\n`);
      process.exit(1);
    }
  } else {
    console.warn(`⚠️  TSSD vault disabled (AFI_MONGO_URI not set)\n`);
  }

  // Step 3: Test vault replay
  console.log("3️⃣ Testing vault replay...");
  const replayResult = await replaySignalById(result.signalId);
  if (replayResult) {
    console.log(`✅ Replay successful`);
    console.log(`   UWR Score Delta: ${replayResult.comparison.uwrScoreDelta.toFixed(4)}`);
    console.log(`   Decision Changed: ${replayResult.comparison.decisionChanged}\n`);
  } else {
    console.error(`❌ Replay failed!\n`);
    process.exit(1);
  }

  console.log("🎉 All smoke tests passed!\n");
  process.exit(0);
}

main().catch((error) => {
  console.error("❌ Smoke test failed:", error);
  process.exit(1);
});
```

**Run Command**:
```bash
cd afi-reactor
npm run build
node dist/scripts/pipeline-smoke.js
```

---

### 4.2 Stage-Specific Test Commands

#### Test Ingestion Only
```bash
curl -X POST http://localhost:8080/api/webhooks/tradingview \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "BTC/USDT",
    "timeframe": "1h",
    "strategy": "froggy_trend_pullback_v1",
    "direction": "long",
    "setupSummary": "Test ingestion"
  }'
```

#### Test Enrichment Only (needs HTTP endpoint)
```bash
# First, add POST /test/enrichment endpoint to afi-reactor/src/server.ts
curl -X POST http://localhost:8080/test/enrichment \
  -H "Content-Type: application/json" \
  -d '{
    "signalId": "test-001",
    "score": 0,
    "confidence": 0.5,
    "timestamp": "2025-12-09T12:00:00Z",
    "meta": {
      "symbol": "BTC/USDT",
      "market": "spot",
      "timeframe": "1h",
      "strategy": "froggy_trend_pullback_v1",
      "direction": "long",
      "enrichmentProfile": {
        "technical": { "enabled": true, "preset": "trend_pullback" }
      }
    },
    "structured": {
      "normalizedTimestamp": "2025-12-09T12:00:00Z",
      "hasValidMeta": true,
      "structuredBy": "test"
    }
  }'
```

#### Test Analysis Only (needs HTTP endpoint)
```bash
# First, add POST /test/analysis endpoint to afi-reactor/src/server.ts
curl -X POST http://localhost:8080/test/analysis \
  -H "Content-Type: application/json" \
  -d @afi-reactor/test/fixtures/enriched-signal.json
```

#### Test Validator Only (needs HTTP endpoint)
```bash
# First, add POST /test/validator endpoint to afi-reactor/src/server.ts
curl -X POST http://localhost:8080/test/validator \
  -H "Content-Type: application/json" \
  -d '{
    "signalId": "test-001",
    "analysis": {
      "uwrScore": 0.78,
      "uwrAxes": {
        "structureAxis": 0.8,
        "executionAxis": 0.7,
        "riskAxis": 0.6,
        "insightAxis": 0.9
      },
      "notes": []
    }
  }'
```

#### Test Vault Replay
```bash
cd afi-reactor
npm run replay:signal -- --id=<signalId>
```

---

### 4.3 MongoDB TSSD Vault Setup

**Prerequisites**:
- MongoDB 5.0+ (for time-series collections)
- Connection string with read/write access

**Environment Variables** (add to `afi-reactor/.env`):
```bash
# TSSD Vault (MongoDB)
AFI_MONGO_URI=mongodb://localhost:27017
AFI_MONGO_DB_NAME=afi
AFI_MONGO_COLLECTION_TSSD=tssd_signals
```

**Verify Vault Connection**:
```bash
cd afi-reactor
npm run start:demo

# Check logs for:
# ✅ TSSD vault connected: afi.tssd_signals
```

**Query Vault Directly** (MongoDB shell):
```javascript
use afi
db.tssd_signals.find({ "identity.signalId": "your-signal-id" }).pretty()
db.tssd_signals.countDocuments()
db.tssd_signals.find().sort({ createdAt: -1 }).limit(10)
```

---

### 4.4 ElizaOS Agent Testing

**Start ElizaOS Server**:
```bash
cd afi-gateway
npm run dev:server-full

# Server starts on http://localhost:8081
# Web UI: http://localhost:8081
```

**Test Phoenix (Host)**:
```
User: Phoenix, what is AFI Protocol?
Phoenix: [Explains AFI Protocol]

User: Is AFI Reactor online?
Phoenix: [Calls CHECK_AFI_REACTOR_HEALTH action]

User: Run the AFI Eliza demo
Phoenix: [Calls RUN_AFI_ELIZA_DEMO action, shows stage summaries]
```

**Test Alpha (Scout)**:
```
User: Alpha, submit a BTC trend-pullback setup
Alpha: [Calls SUBMIT_FROGGY_DRAFT action]
```

**Test Froggy (Analyst)**:
```
User: Froggy, explain the last decision
Froggy: [Calls EXPLAIN_LAST_FROGGY_DECISION action]
```

**Test Val Dook (Validator)**:
```
User: Val Dook, would that signal qualify for AFI emissions?
Val Dook: [Explains validator decision criteria]
```

---

## 5. Priority Action Items

### 5.1 Critical Path to Real Pipeline (Ordered by Priority)

**Phase 1: Real Data Sources** (Highest Priority)
1. ✅ **Integrate TradingView API or ccxt for OHLCV data**
   - File: `afi-reactor/src/services/marketDataService.ts`
   - Replace mocked enrichment data with real market data
   - Estimated effort: 2-3 days

2. ✅ **Add TA-Lib or custom technical indicators**
   - File: `afi-reactor/src/services/technicalIndicatorService.ts`
   - Calculate RSI, MACD, EMA, Bollinger Bands, etc.
   - Estimated effort: 1-2 days

3. ✅ **Integrate sentiment data (LunarCrush, Santiment, or Twitter)**
   - File: `afi-reactor/src/services/sentimentService.ts`
   - Replace mocked sentiment with real social data
   - Estimated effort: 2-3 days

**Phase 2: Emissions Wiring** (High Priority)
4. ✅ **Wire afi-mint coordinator to afi-reactor validator decisions**
   - File: `afi-reactor/src/services/emissionsService.ts`
   - Call afi-mint after validator approval
   - Estimated effort: 3-4 days

5. ✅ **Add Codex metadata logging to on-chain receipts**
   - File: `afi-infra/src/codex/ReceiptProvenanceService.ts`
   - Link TSSD vault → on-chain receipts
   - Estimated effort: 2-3 days

**Phase 3: Production Hardening** (Medium Priority)
6. ✅ **Add webhook signature verification**
   - File: `afi-reactor/src/middleware/auth.ts`
   - HMAC-SHA256 signature verification
   - Estimated effort: 1 day

7. ✅ **Add rate limiting and DDoS protection**
   - File: `afi-reactor/src/middleware/rateLimit.ts`
   - Use express-rate-limit
   - Estimated effort: 1 day

8. ✅ **Add production error handling and retry logic**
   - Files: All service files in `afi-reactor/src/services/`
   - Circuit breakers, exponential backoff, dead letter queues
   - Estimated effort: 2-3 days

**Phase 4: Advanced Features** (Lower Priority)
9. ⚠️ **Add multi-strategy analyst routing**
   - File: `afi-core/analysts/strategyRouter.ts`
   - Route signals to correct analyst based on strategy
   - Estimated effort: 2-3 days

10. ⚠️ **Add multi-validator consensus**
    - File: `afi-core/validators/MultiValidatorConsensus.ts`
    - Aggregate multiple validator decisions
    - Estimated effort: 3-4 days

11. ⚠️ **Add real exchange execution (ccxt)**
    - File: `afi-reactor/src/services/executionService.ts`
    - Replace simulated execution with real exchange orders
    - Estimated effort: 5-7 days (HIGH RISK)

---

### 5.2 Quick Wins (Can Be Done Today)

**Add Stage-Specific HTTP Test Endpoints** (1-2 hours):
```typescript
// afi-reactor/src/server.ts

// Test enrichment only
app.post("/test/enrichment", async (req, res) => {
  const structuredSignal = req.body;
  const enriched = await froggyEnrichmentAdapter.run(structuredSignal);
  res.json(enriched);
});

// Test analysis only
app.post("/test/analysis", async (req, res) => {
  const enrichedSignal = req.body;
  const analyzed = await froggyAnalyst.run(enrichedSignal);
  res.json(analyzed);
});

// Test validator only
app.post("/test/validator", async (req, res) => {
  const analyzedSignal = req.body;
  const decision = await validatorDecisionEvaluator.run(analyzedSignal);
  res.json(decision);
});
```

**Add Pipeline Smoke Test Script** (1-2 hours):
- Create `afi-reactor/scripts/pipeline-smoke.ts` (see Section 4.1)
- Add `"smoke": "node dist/scripts/pipeline-smoke.js"` to package.json scripts

**Add Webhook Signature Verification** (1 hour):
```typescript
// afi-reactor/src/middleware/auth.ts
import crypto from "crypto";

export function verifyWebhookSignature(req, res, next) {
  const signature = req.headers["x-webhook-signature"];
  const secret = process.env.WEBHOOK_SHARED_SECRET;

  if (!secret) {
    return next(); // Skip verification if no secret configured
  }

  const payload = JSON.stringify(req.body);
  const expectedSignature = crypto
    .createHmac("sha256", secret)
    .update(payload)
    .digest("hex");

  if (signature !== expectedSignature) {
    return res.status(401).json({ error: "Invalid webhook signature" });
  }

  next();
}
```

---

## 6. Summary & Recommendations

### 6.1 Current State Assessment

**Strengths**:
- ✅ **Solid foundation**: 6-stage pipeline is functionally complete
- ✅ **Clean architecture**: Repo boundaries are well-defined and respected
- ✅ **Deterministic scoring**: UWR implementation is canonical and testable
- ✅ **Vault persistence**: MongoDB TSSD vault is working (Phase 1 + Phase 2)
- ✅ **Replay capability**: Signals can be replayed for validation
- ✅ **ElizaOS integration**: 5 agent personas are functional

**Weaknesses**:
- ❌ **All enrichment data is mocked** (biggest blocker for real pipeline)
- ❌ **No emissions wiring** (validator decisions don't trigger minting)
- ❌ **No real exchange execution** (all execution is simulated)
- ❌ **No production hardening** (no rate limiting, auth, error handling)

### 6.2 Recommended Next Steps

**Immediate (This Week)**:
1. Add stage-specific HTTP test endpoints (Section 5.2)
2. Add pipeline smoke test script (Section 4.1)
3. Add webhook signature verification (Section 5.2)

**Short-Term (Next 2 Weeks)**:
1. Integrate real market data (TradingView API or ccxt)
2. Add technical indicator calculation (TA-Lib or custom)
3. Wire afi-mint coordinator to validator decisions

**Medium-Term (Next Month)**:
1. Add sentiment data integration
2. Add Codex metadata logging
3. Add production error handling and rate limiting

**Long-Term (Next Quarter)**:
1. Add multi-strategy analyst routing
2. Add multi-validator consensus
3. Add real exchange execution (HIGH RISK - requires extensive testing)

### 6.3 Risk Assessment

**Low Risk**:
- Adding test endpoints
- Adding smoke test script
- Adding webhook signature verification
- Integrating market data APIs

**Medium Risk**:
- Wiring emissions coordinator (touches tokenomics)
- Adding Codex metadata logging (touches on-chain receipts)
- Adding multi-validator consensus (changes decision logic)

**High Risk**:
- Real exchange execution (can lose real money)
- Changing UWR scoring formula (breaks determinism)
- Modifying token contracts (requires audit)

---

## 7. Appendix: File Locations Reference

### 7.1 Key Files by Stage

**Ingestion (USS v1.1 Canonical)**:
- `afi-reactor/src/server.ts` — HTTP endpoints (POST /api/webhooks/uss)
- `afi-reactor/src/services/froggyWebhookService.ts` — USS v1.1 webhook handler with AJV validation
- `afi-reactor/plugins/_deprecated_ingest/` — ⚠️ DEPRECATED legacy ingest plugins (quarantined)

**Enrichment**:
- `afi-reactor/plugins/froggy-enrichment-tech-pattern.plugin.ts` — Technical + pattern enrichment (parallel)
- `afi-reactor/plugins/froggy-enrichment-sentiment-news.plugin.ts` — Sentiment + news enrichment (parallel)
- `afi-reactor/plugins/froggy-enrichment-adapter.plugin.ts` — Enrichment merge + AI/ML
- `afi-reactor/src/services/marketDataService.ts` — (TO BE ADDED) Real market data

**Analysis**:
- `afi-reactor/plugins/froggy.trend_pullback_v1.plugin.ts` — Froggy analyst wrapper
- `afi-core/analysts/froggy.trend_pullback_v1.ts` — Canonical UWR scoring

**Validation**:
- `afi-reactor/plugins/validator-decision-evaluator.plugin.ts` — Validator decision logic
- `afi-core/validators/ValidatorDecision.ts` — Decision types
- `afi-core/validators/UniversalWeightingRule.ts` — UWR formula

**Persistence**:
- `afi-reactor/src/services/tssdVaultService.ts` — TSSD vault service (afi-reactor)
- `afi-infra/src/tssd/MongoTSSDVaultClient.ts` — MongoDB client (afi-infra)
- `afi-infra/src/tssd/types.ts` — Vault types

**Replay**:
- `afi-reactor/src/services/vaultReplayService.ts` — Replay service
- `afi-reactor/src/cli/replaySignal.ts` — CLI tool

**ElizaOS**:
- `afi-gateway/src/server-full.ts` — ElizaOS server
- `afi-gateway/plugins/afi-reactor-actions/index.ts` — AFI actions
- `afi-gateway/src/afiClient.ts` — AFI Reactor HTTP client

### 7.2 Environment Variables Reference

**afi-reactor**:
```bash
# Server
PORT=8080
NODE_ENV=development

# TSSD Vault
AFI_MONGO_URI=mongodb://localhost:27017
AFI_MONGO_DB_NAME=afi
AFI_MONGO_COLLECTION_TSSD=tssd_signals

# Webhook Auth
WEBHOOK_SHARED_SECRET=your-secret-here
```

**afi-gateway**:
```bash
# ElizaOS Server
PORT=8081
NODE_ENV=development

# OpenAI
OPENAI_API_KEY=sk-proj-...

# AFI Reactor
AFI_REACTOR_BASE_URL=http://localhost:8080

# MongoDB (for ElizaOS sessions)
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=afi_eliza
```

---

**End of Audit Report**


