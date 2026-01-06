# AFI Protocol — Immediate Next Steps

**Date**: 2025-12-09  
**Status**: Post-Audit Action Plan

---

## Quick Start: Test What We Have Now

### 1. Run the Pipeline Smoke Test (5 minutes)

```bash
cd ~/AFI_Modular_Repos/afi-reactor

# Build the project
npm run build

# Run smoke test
node dist/scripts/pipeline-smoke.js
```

**Expected Output**:
- ✅ Signal processed with signalId
- ✅ Validator decision (approve/reject/flag)
- ✅ UWR score (0.0 - 1.0)
- ✅ Signal found in TSSD vault (if MongoDB configured)
- ✅ Replay successful with deterministic results

---

### 2. Test Individual Pipeline Stages (10 minutes)

**First, wire up the test endpoints**:

Add this to `afi-reactor/src/server.ts` (around line 30, after other routes):

```typescript
import testEndpoints from "./routes/testEndpoints.js";

// ... existing routes ...

// Test endpoints (dev/demo only)
if (process.env.NODE_ENV !== "production") {
  app.use("/test", testEndpoints);
  console.log("🧪 Test endpoints enabled: /test/enrichment, /test/analysis, /test/validator");
}
```

**Then run the stage tests**:

```bash
# Start the server
npm run start:demo

# In another terminal, run the test script
chmod +x scripts/test-pipeline-stages.sh
./scripts/test-pipeline-stages.sh
```

**Expected Output**:
- ✅ Full pipeline test passed
- ✅ Enrichment stage test passed
- ✅ Analysis stage test passed
- ✅ Validator stage test passed

---

## Critical Path: Real Pipeline in 2 Weeks

### Week 1: Real Data Sources

**Day 1-2: Market Data Integration**
- [ ] Create `afi-reactor/src/services/marketDataService.ts`
- [ ] Integrate ccxt library for OHLCV data
- [ ] Replace mocked enrichment data in `froggy-enrichment-adapter.plugin.ts`
- [ ] Test with real BTC/USDT data from Binance

**Day 3-4: Technical Indicators**
- [ ] Create `afi-reactor/src/services/technicalIndicatorService.ts`
- [ ] Add TA-Lib or custom indicator calculations (RSI, MACD, EMA, Bollinger Bands)
- [ ] Wire into enrichment adapter
- [ ] Test with real market data

**Day 5: Sentiment Data**
- [ ] Create `afi-reactor/src/services/sentimentService.ts`
- [ ] Integrate LunarCrush or Santiment API
- [ ] Wire into enrichment adapter
- [ ] Test with real social sentiment data

---

### Week 2: Emissions Wiring + Production Hardening

**Day 6-7: Emissions Coordinator**
- [ ] Create `afi-reactor/src/services/emissionsService.ts`
- [ ] Wire to afi-mint coordinator
- [ ] Call after validator approval
- [ ] Test with demo emissions (no real minting yet)

**Day 8: Codex Metadata**
- [ ] Create `afi-infra/src/codex/ReceiptProvenanceService.ts`
- [ ] Link TSSD vault → on-chain receipts
- [ ] Test metadata logging

**Day 9: Security Hardening**
- [ ] Add webhook signature verification (`src/middleware/auth.ts`)
- [ ] Add rate limiting (`src/middleware/rateLimit.ts`)
- [ ] Add duplicate signal detection
- [ ] Test with malicious payloads

**Day 10: Integration Testing**
- [ ] Run full end-to-end tests with real data
- [ ] Verify emissions flow (demo mode)
- [ ] Verify vault persistence
- [ ] Verify replay determinism

---

## Files Created in This Audit

### 1. Audit Report
**Location**: `~/AFI_Modular_Repos/AFI_PIPELINE_AUDIT_REPORT.md`

**Contents**:
- Executive summary (what's real vs demo)
- Complete pipeline map with 6 stages
- Stage-by-stage analysis (ingestion, enrichment, analysis, validator)
- Repo-by-repo readiness checklist
- Concrete test commands and file locations
- Priority action items
- Risk assessment

---

### 2. Pipeline Smoke Test
**Location**: `~/AFI_Modular_Repos/afi-reactor/scripts/pipeline-smoke.ts`

**Purpose**: End-to-end smoke test for the full pipeline

**Tests**:
- Signal ingestion and processing
- Validator decision
- TSSD vault persistence
- Vault replay determinism

**Usage**:
```bash
cd afi-reactor
npm run build
node dist/scripts/pipeline-smoke.js
```

---

### 3. Stage-Specific Test Endpoints
**Location**: `~/AFI_Modular_Repos/afi-reactor/src/routes/testEndpoints.ts`

**Purpose**: HTTP endpoints for testing individual pipeline stages in isolation

**Endpoints**:
- `POST /test/enrichment` — Test enrichment stage only
- `POST /test/analysis` — Test analysis stage only
- `POST /test/validator` — Test validator stage only

**Usage**: Wire into `server.ts` (see Quick Start section above)

---

### 4. Stage Test Script
**Location**: `~/AFI_Modular_Repos/afi-reactor/scripts/test-pipeline-stages.sh`

**Purpose**: Bash script to test all pipeline stages via HTTP

**Tests**:
- Full pipeline (TradingView webhook)
- Enrichment stage (isolated)
- Analysis stage (isolated)
- Validator stage (isolated)

**Usage**:
```bash
chmod +x scripts/test-pipeline-stages.sh
./scripts/test-pipeline-stages.sh
```

---

## Recommended Workflow

### Today (2 hours)
1. ✅ Review audit report (`AFI_PIPELINE_AUDIT_REPORT.md`)
2. ✅ Run pipeline smoke test
3. ✅ Wire up test endpoints in `server.ts`
4. ✅ Run stage test script

### This Week (20 hours)
1. Integrate ccxt for real market data
2. Add technical indicator calculations
3. Add sentiment data integration
4. Test with real data sources

### Next Week (20 hours)
1. Wire emissions coordinator
2. Add Codex metadata logging
3. Add security hardening (auth, rate limiting)
4. Run full integration tests

---

## Success Criteria

**By End of Week 1**:
- [ ] All enrichment data comes from real APIs (no mocks)
- [ ] Technical indicators calculated from real OHLCV data
- [ ] Sentiment data from real social APIs
- [ ] All smoke tests pass with real data

**By End of Week 2**:
- [ ] Validator approvals trigger emissions coordinator calls
- [ ] Codex metadata logged to on-chain receipts
- [ ] Webhook signature verification working
- [ ] Rate limiting protecting all endpoints
- [ ] Full end-to-end test with real data + emissions (demo mode)

---

**End of Next Steps Document**

