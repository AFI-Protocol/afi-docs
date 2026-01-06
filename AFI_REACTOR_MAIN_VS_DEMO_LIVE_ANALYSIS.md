AFI-Reactor: main vs demo/live Branch Analysis

## Executive Summary

The `main` and `demo/live` branches in afi-reactor have significant architectural and functional divergence. The `demo/live` branch contains advanced features (TSSD Vault, Provenance, Replay, CPJ ingestion, Telegram MTProto) that are not present in `main`, while `main` contains security fixes and architectural corrections (validator removal) that are not in `demo/live`.

**Key Finding**: The `demo/live` branch represents a more feature-complete but architecturally incorrect version (validators in DAG), while `main` represents a more secure but less feature-complete version (validators external to DAG).

## Branch Overview

### main Branch

**Current Commit**: `97f949d` (Merge pull request #13 from AFI-Protocol/feature/remove-dag-validators)

**Purpose**: Canonical production branch with security fixes and architectural corrections.

**Key Characteristics**:
- ✅ Validators are external to DAG (correct architecture)
- ✅ Security fixes for MongoDB credentials
- ✅ Secret scanning infrastructure
- ✅ CI/CD improvements
- ❌ Missing TSSD Vault functionality
- ❌ Missing Provenance tracking
- ❌ Missing Replay capabilities
- ❌ Missing CPJ ingestion
- ❌ Missing Telegram MTProto collector
- ❌ Missing advanced enrichment features

### demo/live Branch

**Current Commit**: `e14b916` (test: add Pattern Regime provider test script)

**Purpose**: Feature-rich demo branch with advanced capabilities for live deployment.

**Key Characteristics**:
- ✅ TSSD Vault (Phase 1) - MongoDB persistence
- ✅ Provenance tracking (Phase 1.5) - Signal lineage
- ✅ Replay capabilities (Phase 2) - Historical signal replay
- ✅ CPJ ingestion - Crypto Price JSON format
- ✅ Telegram MTProto collector - Social signal collection
- ✅ Advanced enrichment - Pattern regime, perp sentiment, news features
- ✅ Multiple price feeds - BloFin, Coinbase, Coinalyze
- ✅ Tiny Brains AI/ML integration
- ✅ USS v1.1 canonical flow
- ❌ Validators are in DAG (incorrect architecture)
- ❌ Missing security fixes from main
- ❌ Uses outdated "AFI-Engine" naming
- ❌ Uses Git dependencies instead of local file dependencies

## Divergence Analysis

### Commits Unique to main (not in demo/live)

```
97f949d Merge pull request #13 from AFI-Protocol/feature/remove-dag-validators
d85a446 fix: remove validator nodes from DAG - validators should be external to reactor
19ad90d Merge pull request #12 from AFI-Protocol/release/reactor-scored-only-public
0e372b0 ci: build afi-core and rely on package exports
96c5111 Reactor: scored-only public runtime (isolated vault, no demo/validator/replay)
9915a27 security: Eliminate exposed MongoDB credentials and add secret scanning
ba6fa7a fix: exclude more placeholder patterns from secret scan
74a91f7 fix: exclude node_modules and build artifacts from secret scan
a38bcb8 fix: scan only tracked files, not git history
655501a fix: exclude placeholder values from secret scanner
0f1fb59 fix: simplify secret scanner to use basic scan only
e804628 fix: make secret scanner work without Gitleaks license
6ac702c security: add secret management and scanning infrastructure
f2611db fix(reactor): restore main build + align tests to canonical analystScore
6177828 fix: install afi-core dependencies before afi-reactor
a31bb5e fix: properly checkout afi-core in CI and remove stub/typings hacks
33af96b fix: add froggy.trend_pullback_v1 stub for CI
434b62d fix: add enrichmentMeta.categories to FroggyEnrichedView type
da3fff2 fix: add strategyId to AnalystScoreTemplate and FroggyTrendPullbackScore
a24451f fix: add froggy.trend_pullback_v1 module declarations
a1ec593 fix: expand FroggyEnrichedView type definition for test assertions
ea337ac fix: add afi-core module declarations for CI TypeScript compilation
0f2ab31 fix: use local type stubs for afi-core imports in CI
e9f9eba fix: define EnrichmentProfile locally for CI (afi-core unavailable)
b472378 fix: add supertest devDependency for prizeDemoEndpoint tests
e7ee298 fix: CI runs tests only (afi-core private repo access limitation)
db3875d fix: remove explicit token param (use default GITHUB_TOKEN behavior)
bfc8569 fix: checkout afi-core as sibling for file: dependency resolution
3990bfe chore: ignore local env + local afi-core symlink
505bf91 fix: checkout afi-core in CI for file: dependency resolution
be32f23 fix: include plugins in tsconfig for tsc compilation
3252ee6 fix: resolve 5 test failures (network deps + type mismatches)
10d5929 fix: restore reactor main build after PR #7
```

**Summary**: 35 commits focused on security, CI/CD improvements, and architectural corrections.

### Commits Unique to demo/live (not in main)

```
e14b916 test: add Pattern Regime provider test script
b3a0e87 feat: replace CoinGecko with exchange OHLC for Pattern Regime
0118353 feat: add CPJ ingestion and Telegram MTProto collector
991d6d6 build: switch to HTTPS Git deps and prioritize PORT env var for Render
852d796 build: use Git dependencies and add build:deps script for Render deployment
37cf7fa chore: ignore deps/build outputs; stop tracking node_modules
37e40c5 test: update expectations after merge with main
36e49a9 Merge remote-tracking branch 'origin/main' into docs/branch-doctrine-and-replay-spec
c7b0437 feat(uss): add replay-canonical ingest facts block (symbol/timeframe/strategy)
2251530 refactor(demo): enforce canonical USS v1.1 flow (no backward compat)
275659f fix(tests): restore demo endpoint + aiMl category expectations
92657f1 fix(tests): resolve ussValidator ESM syntax errors in Jest
69fb498 feat(validator): implement real novelty scoring with replay-canonical guarantees
3513ec1 feat(validator): add validatorConfigId/version to decision + replay checks
c103b38 chore(ingest): quarantine legacy ingest plugins; add guardrails
1393640 feat(vault): persist canonical rawUss v1.1 in TSSD document
ba5b90a refactor(reactor): pipeline consumes rawUss; remove legacy ingest stages
0ef7d66 feat(reactor): pass canonical uss v1.1 into DAG as rawUss
4f828f1 feat(reactor): enforce canonical ussignal at tradingview webhook boundary
9ecfb02 feat(time): wire scoredAt/decayParams + runtime ESM smoke test
395b0af feat(reactor): consume AnalystScoreTemplate as canonical analyst output
d9b6e6b feat(dag): add DAG runner and Froggy DAG pipeline helper
cafd132 chore: point Tiny Brains integration to standalone afi-tiny-brains service
a3e08ab feat: add Tiny Brains aiMl integration and observability for Froggy
c6d78e1 feat: add news features and max enrichment profile for Froggy
60e9941 feat: add pluggable NewsProvider system with NewsData.io integration
21a03a0 feat: add pattern regime lens and mirror regime to top-level pattern
1ca48f5 feat: add Froggy perp sentiment via Coinalyze and fix /test/enrichment
bb4bdfd feat: add Froggy indicator profile and indicator kernel integration
c3bf054 feat: wire USS lenses through enrichment → TSSD → replay
d01b5d0 feat: add Coinbase price feed + TSSD simple replay with provenance audit
a0afa58 feat: add BloFin price feed and TSSD provenance wiring
9312cc6 ci: fix afi-core dependency build in GitHub Actions
4c75727 chore(dev): add supertest and update Jest moduleNameMapper
fdea7cc test(core): fix DAG config shape test import syntax
173acdd test(eliza-demo): add in-process HTTP tests with supertest
653c909 feat(eliza-demo): rename Prize to AFI Eliza Demo with enhanced docs
3388523 feat(replay): add read-only TSSD vault replay (Phase 2)
e853d9b feat(provenance): extend TSSD schema for mint lifecycle (Phase 1.5)
b2b6f81 feat(vault): implement TSSD MongoDB persistence (Phase 1)
```

**Summary**: 40 commits focused on advanced features, integrations, and demo capabilities.

## Key Differences

### 1. DAG Configuration (config/dag.codex.json)

**main branch**:
- 13-node DAG
- No validator nodes in DAG (correct architecture)
- No deprecated nodes
- Clean, minimal configuration

**demo/live branch**:
- 15-node DAG
- Contains `afi-ensemble-score` node (validator in DAG - incorrect)
- Contains `validator-decision-node` (validator in DAG - incorrect)
- Marks `alpha-scout-ingest` and `pixelrick-structurer` as deprecated
- More complex configuration with additional nodes

**Impact**: The demo/live branch violates the architectural principle that validators should be external to the DAG.

### 2. README.md

**main branch**:
- References "AFI-Reactor" (correct naming)
- Describes 13-node DAG
- No validator section in DAG description
- Includes security section with secret scanning setup

**demo/live branch**:
- References "AFI-Engine" (outdated naming)
- Describes 15-node DAG
- Includes validator section in DAG description
- Missing security section

**Impact**: The demo/live branch has outdated documentation and incorrect architectural description.

### 3. package.json

**main branch**:
- Uses local file dependencies: `"afi-core": "file:../afi-core"`
- Minimal dependencies
- Basic scripts

**demo/live branch**:
- Uses Git dependencies: `"afi-core": "git+https://github.com/AFI-Protocol/afi-core.git#0be9be4"`
- Additional dependencies: ajv, ccxt, node-telegram-bot-api, telegram, trading-signals
- Advanced scripts: build:deps, build:smoke, test:cpj:smoke, test:mtproto:smoke, verify:tssd:blofin

**Impact**: The demo/live branch has more dependencies and build complexity for advanced features.

### 4. src/server.ts

**main branch**:
- Minimal server with only `/health` and `/api/webhooks/tradingview` endpoints
- No test endpoints
- Gated debug endpoint (only when DEBUG_ENDPOINTS_ENABLED=true)
- Focus on scoring-only functionality

**demo/live branch**:
- Rich server with multiple test endpoints: `/test`, `/test/blofin`, `/test/coinbase`
- Includes replay and vault services
- More permissive debug endpoint
- Focus on demo and testing capabilities

**Impact**: The demo/live branch has more endpoints and services for testing and demo purposes.

### 5. Architecture

**main branch**:
- ✅ Validators external to DAG (correct)
- ✅ Security-focused
- ✅ Minimal, production-ready
- ❌ Missing advanced features

**demo/live branch**:
- ❌ Validators in DAG (incorrect)
- ❌ Security fixes missing
- ✅ Feature-rich
- ✅ Advanced integrations

**Impact**: Fundamental architectural difference that affects the entire system design.

## Feature Comparison

| Feature | main | demo/live | Notes |
|---------|------|-----------|-------|
| TSSD Vault (Phase 1) | ❌ | ✅ | MongoDB persistence |
| Provenance (Phase 1.5) | ❌ | ✅ | Signal lineage tracking |
| Replay (Phase 2) | ❌ | ✅ | Historical signal replay |
| CPJ Ingestion | ❌ | ✅ | Crypto Price JSON format |
| Telegram MTProto | ❌ | ✅ | Social signal collection |
| Pattern Regime | ❌ | ✅ | Technical analysis |
| Perp Sentiment | ❌ | ✅ | Coinalyze integration |
| News Features | ❌ | ✅ | NewsData.io integration |
| Multiple Price Feeds | ❌ | ✅ | BloFin, Coinbase, Coinalyze |
| Tiny Brains AI/ML | ❌ | ✅ | AI/ML integration |
| USS v1.1 Flow | ❌ | ✅ | Canonical signal format |
| Validator Architecture | ✅ External | ❌ In DAG | Architectural violation |
| Security Fixes | ✅ | ❌ | MongoDB credentials, secret scanning |
| CI/CD Improvements | ✅ | ❌ | Build fixes, dependency resolution |
| Naming | ✅ AFI-Reactor | ❌ AFI-Engine | Outdated naming |
| Dependencies | ✅ Local | ❌ Git | More complex |

## Merge Base

**Merge Base Commit**: `91e9f95189bb3d6d2fd097d7a12e2ad4be417cad`

This is the common ancestor where the two branches diverged.

## Recommendations

### Option 1: Merge demo/live into main (Recommended)

**Steps**:
1. Cherry-pick or merge the feature commits from demo/live into main
2. Remove validator nodes from DAG after merge
3. Update documentation to reflect correct architecture
4. Apply security fixes from main to demo/live features
5. Test thoroughly

**Pros**:
- Combines best of both branches
- Main becomes feature-complete with correct architecture
- Single source of truth

**Cons**:
- Complex merge with potential conflicts
- Requires careful testing
- May need to resolve architectural conflicts

### Option 2: Rebase demo/live onto main

**Steps**:
1. Rebase demo/live onto main
2. Remove validator nodes from DAG after rebase
3. Update documentation
4. Test thoroughly

**Pros**:
- Cleaner history
- Main becomes feature-complete

**Cons**:
- Rewrites history (may affect collaborators)
- Complex rebase with potential conflicts

### Option 3: Keep branches separate

**Steps**:
1. Keep main as production branch
2. Keep demo/live as experimental branch
3. Periodically merge security fixes from main to demo/live
4. Eventually merge demo/live features into main when ready

**Pros**:
- No merge conflicts
- Clear separation of concerns
- Safe experimentation

**Cons**:
- Divergence will increase over time
- Confusion about which branch to use
- Duplicate maintenance effort

### Option 4: Create new integration branch

**Steps**:
1. Create new branch from main
2. Cherry-pick feature commits from demo/live
3. Remove validator nodes from DAG
4. Update documentation
5. Test thoroughly
6. Merge into main when ready

**Pros**:
- Clean integration
- No history rewriting
- Safe testing

**Cons**:
- Additional branch to maintain
- More complex workflow

## Conclusion

The `main` and `demo/live` branches have significant divergence in both architecture and features. The `demo/live` branch contains advanced features that are not present in `main`, but it also contains architectural violations (validators in DAG) and missing security fixes.

**Recommendation**: Option 1 (Merge demo/live into main) is the best approach, as it combines the feature completeness of demo/live with the architectural correctness and security of main. This will require careful merge conflict resolution and thorough testing.

**Next Steps**:
1. Decide on merge strategy
2. Create backup branches
3. Perform merge/rebase
4. Remove validator nodes from DAG
5. Update documentation
6. Test thoroughly
7. Deploy to production

---

**Analysis Date**: 2025-12-26  
**Repository**: afi-reactor  
**Branches Analyzed**: main, demo/live  
**Status**: Significant divergence detected - requires integration planning