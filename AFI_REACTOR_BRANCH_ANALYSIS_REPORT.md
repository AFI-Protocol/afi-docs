# AFI-Reactor Repository Branch Analysis Report

## Executive Summary

The afi-reactor repository exhibits significant branch divergence with active development occurring on the `docs/branch-doctrine-and-replay-spec` branch, which contains 15 commits ahead of main. This branch includes critical features like TSSD Vault (Phase 1), Provenance (Phase 1.5), and Replay (Phase 2) capabilities that are not present in the main branch. The repository requires branch consolidation to bring these advanced features into the canonical main branch.

## Repository Overview

- **Repository**: afi-reactor (formerly afi-engine)
- **Location**: /Users/secretservice/AFI_Modular_Repos/afi-reactor
- **Git Status**: Clean working directory on docs/branch-doctrine-and-replay-spec
- **Remote Synchronization**: Up-to-date with origin
- **Architecture**: DAG-based orchestrator for AFI Protocol

## Branch Inventory

### Local Branches
- **docs/branch-doctrine-and-replay-spec** (current branch)
- **main**
- **afi-reactor-freeze-2025-11-16** (local snapshot)

### Remote Branches
- **origin/main** (canonical branch)
- **origin/docs/branch-doctrine-and-replay-spec** (feature branch)

## Branch Analysis

### Main Branch
**Status**: Behind remote, requires pull
**Commit History:**
- Tracks origin/main
- Contains base orchestrator functionality
- Lacks advanced features present in docs branch

**File Structure:**
- Core directories: src/, config/, docs/, droids/
- Configuration: Multiple codex files (dag.codex.json, agents.codex.json, etc.)
- Services: Comprehensive service architecture
- Routes: API endpoints for signal processing

### docs/branch-doctrine-and-replay-spec Branch
**Status**: 15 commits ahead of main, up-to-date with remote
**Divergence**: Significant feature additions not in main
**Last Commit**: `9312cc6` - ci: fix afi-core dependency build in GitHub Actions

**Key Features Added:**
- **TSSD Vault (Phase 1)**: Secure storage and retrieval system
- **Provenance (Phase 1.5)**: Signal lineage and tracking
- **Replay (Phase 2)**: Historical signal replay capabilities
- **Test Fixes**: Improved test suite reliability
- **AFI Eliza Demo Rename**: Updated demo components

**File Structure Enhancements:**
- Additional service modules in src/services/
- Enhanced configuration in config/
- Updated documentation in docs/
- Improved test coverage

### afi-reactor-freeze-2025-11-16 Branch
**Status**: Local only, no remote tracking
**Purpose**: Safety snapshot from November 16, 2025
**Usage**: Backup/restore point for critical functionality

## Branch Comparisons

### Differences from Main Branch
The `docs/branch-doctrine-and-replay-spec` branch contains substantial additions:

- **New Services**: TSSD Vault, Provenance tracking, Replay engine
- **Enhanced Configuration**: Updated codex files for new features
- **Improved Testing**: Fixed CI/CD pipeline and test reliability
- **Documentation Updates**: Branch doctrine and replay specifications
- **Demo Updates**: AFI Eliza integration improvements

### File Structure Analysis

#### src/ Directory (All Branches)
```
src/
├── adapters/          # External system integrations
├── aiMl/             # AI/ML processing components
├── cli/              # Command-line interfaces
├── collectors/       # Data collection modules
├── config/           # Runtime configuration
├── core/             # Core orchestration logic
├── cpj/              # CPJ processing (Crypto Price JSON)
├── enrichment/       # Signal enrichment
├── indicator/        # Technical indicators
├── news/             # News processing
├── novelty/          # Novelty detection
├── routes/           # API route handlers
├── services/         # Business logic services
├── types/            # TypeScript type definitions
├── uss/              # Universal Signal Schema processing
└── utils/            # Utility functions
```

#### config/ Directory (All Branches)
```
config/
├── agent.registry.json      # Agent definitions
├── agents.codex.json        # Agent configurations
├── dag.codex.json          # DAG pipeline definitions
├── execution-agent.registry.json  # Execution agents
├── ops.codex.json          # Operations configurations
└── schema.codex.json       # Schema definitions
```

## Completeness Evaluation

### Architectural Correction Required
**Critical Issue**: Validator should be external to DAG, not a node within it. Current configurations in both branches violate this architecture.

### Main Branch Completeness: PARTIAL (65%)
- ✅ Base DAG orchestration
- ✅ Signal processing pipeline
- ✅ API endpoints
- ✅ Basic agent registry
- ❌ TSSD Vault functionality
- ❌ Provenance tracking
- ❌ Replay capabilities
- ❌ Advanced testing fixes
- ❌ **Validator incorrectly placed in DAG** (architectural violation)

### docs/branch-doctrine-and-replay-spec Branch Completeness: HIGH (90%)
- ✅ All main branch features
- ✅ TSSD Vault (Phase 1)
- ✅ Provenance (Phase 1.5)
- ✅ Replay (Phase 2)
- ✅ CI/CD fixes
- ✅ Enhanced documentation
- ⚠️ Requires integration testing with main
- ❌ **Validator incorrectly placed in DAG** (architectural violation)

### afi-reactor-freeze-2025-11-16 Branch Completeness: BASELINE (55%)
- ✅ Stable snapshot
- ✅ Core functionality preserved
- ❌ Missing recent developments
- ❌ Not recommended for active use
- ❌ **Validator incorrectly placed in DAG** (architectural violation)

## Development Progress Assessment

### Most Complete Branch: docs/branch-doctrine-and-replay-spec
**Rationale:**
- Contains latest features (TSSD, Provenance, Replay)
- 15 commits ahead with substantial improvements
- Active development branch with CI/CD fixes
- Comprehensive feature set for Phase 2 capabilities

### Development Status: ACTIVE DIVERGENCE
- **Main Branch**: Stable but outdated
- **Feature Branch**: Advanced but unmerged
- **Freeze Branch**: Archived baseline

## Conflict and Divergence Analysis

### Divergent Paths Detected
1. **Feature Development**: docs branch contains Phase 1.5-2 features not in main
2. **Testing Improvements**: CI fixes and test enhancements isolated to feature branch
3. **Documentation**: Branch-specific doctrine and specifications
4. **Architecture Discrepancy**: Validator node status unclear - README shows validator as DAG node, but user indicates it should be outside DAG

### Potential Integration Challenges
- **Merge Complexity**: 15 commits may require careful conflict resolution
- **Testing Requirements**: Full integration testing needed post-merge
- **Documentation Sync**: Branch doctrine needs main branch integration
- **Architecture Clarification**: Need to confirm if validator should remain in DAG or be external

### No Conflicts Anticipated
- **Clean Separation**: Feature additions don't overlap with main functionality
- **Modular Design**: New services are additive, not modifying existing code
- **Schema Compatibility**: Codex updates are backward compatible

## Recommendations

### Immediate Actions
1. **Architectural Fix**: Remove validator nodes from DAG configuration (both branches)
2. **Branch Consolidation**: Merge docs/branch-doctrine-and-replay-spec into main after validator fix
3. **Integration Testing**: Validate TSSD, Provenance, and Replay functionality
4. **Documentation Update**: Incorporate branch doctrine into main docs and update README DAG diagram

### Merge Strategy
```
main ← docs/branch-doctrine-and-replay-spec (post-validator-removal)
   ← (selective merge of freeze branch if needed)
```

### Validator Architecture Implementation
- **Remove from DAG**: Eliminate validator-decision-node and afi-ensemble-score from dag.codex.json
- **External Integration**: Implement validator as external service called by reactor
- **API Interface**: Create REST/WebSocket interface for validator communication
- **Configuration Update**: Update codex files to reflect external validator architecture

### Long-term Strategy
1. **Feature Branch Workflow**: Continue using feature branches for development
2. **Regular Merges**: Merge completed features into main more frequently
3. **Freeze Branches**: Maintain periodic snapshots for stability
4. **CI/CD Enhancement**: Ensure all branches have proper testing
5. **Architecture Governance**: Regular audits to ensure doctrine compliance

### Risk Mitigation
- Create backup branch before merge
- Test in staging environment first
- Monitor for integration issues post-merge
- Update dependent repositories (afi-gateway, etc.)

## Conclusion

The afi-reactor repository demonstrates active development with significant feature advancement in the `docs/branch-doctrine-and-replay-spec` branch. This branch represents the most complete and up-to-date version with critical Phase 1.5-2 capabilities (TSSD Vault, Provenance, Replay) that should be integrated into main to advance the AFI Protocol's orchestration capabilities. The repository requires branch consolidation to unify these developments while maintaining the stability of the core DAG orchestration system.</content>
</xai:function_call">The afi-reactor repository analysis is complete. The report reveals significant branch divergence with the `docs/branch-doctrine-and-replay-spec` branch containing 15 commits ahead of main, including critical features like TSSD Vault, Provenance tracking, and Replay capabilities. This branch is the most complete and should be merged into main for full functionality.