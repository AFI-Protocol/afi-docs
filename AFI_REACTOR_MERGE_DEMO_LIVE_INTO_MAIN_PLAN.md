# AFI-Reactor: Merge demo/live into main - Orchestrator Action Plan

## Objective

Merge the feature-rich `demo/live` branch into the architecturally correct `main` branch, creating a unified production branch that combines:
- Advanced features from demo/live (TSSD Vault, Provenance, Replay, CPJ ingestion, Telegram MTProto)
- Architectural correctness from main (validators external to DAG)
- Security fixes from main (MongoDB credentials, secret scanning)

## Context

**Current State**:
- `main` branch: commit `97f949d` (correct architecture, security fixes, missing features)
- `demo/live` branch: commit `e14b916` (incorrect architecture, missing security, feature-rich)
- Merge base: `91e9f95189bb3d6d2fd097d7a12e2ad4be417cad`

**Key Challenge**: The demo/live branch contains validator nodes in the DAG, which violates the architectural principle that validators should be external to the reactor.

## Prerequisites

- [ ] Review [`AFI_REACTOR_MAIN_VS_DEMO_LIVE_ANALYSIS.md`](AFI_REACTOR_MAIN_VS_DEMO_LIVE_ANALYSIS.md) for detailed differences
- [ ] Ensure all work is committed and pushed
- [ ] Create backup branches before starting merge
- [ ] Verify current working directory is clean

## Action Plan

### Phase 1: Preparation

**Step 1.1**: Create backup branches
```bash
cd afi-reactor
git branch backup-main-before-merge
git branch backup-demo-live-before-merge
```
**Purpose**: Safety net in case merge goes wrong

**Step 1.2**: Verify branch status
```bash
git status
git log --oneline -1
```
**Expected**: Clean working directory, on main branch

**Step 1.3**: Pull latest changes
```bash
git fetch origin
git pull origin main
```
**Purpose**: Ensure main is up-to-date with remote

### Phase 2: Merge Execution

**Step 2.1**: Attempt merge
```bash
git merge demo/live --no-ff -m "Merge demo/live into main - combine features with correct architecture"
```
**Purpose**: Merge demo/live into main with explicit commit message

**Expected Outcome**: 
- Success with automatic merge (best case)
- OR merge conflicts requiring resolution (likely case)

**Step 2.2**: If merge conflicts occur

**Conflict Resolution Strategy**:

1. **DAG Configuration Conflicts** ([`config/dag.codex.json`](afi-reactor/config/dag.codex.json))
   - **Action**: Remove validator nodes (afi-ensemble-score, validator-decision-node)
   - **Reason**: Validators should be external to DAG per architectural doctrine
   - **Resolution**: Keep main's version (no validators) but preserve other demo/live features

2. **README Conflicts** ([`README.md`](afi-reactor/README.md))
   - **Action**: Update to reflect correct architecture
   - **Reason**: Remove validator section, update node count to 13, use "AFI-Reactor" naming
   - **Resolution**: Keep main's architectural description but preserve demo/live feature descriptions

3. **package.json Conflicts**
   - **Action**: Preserve Git dependencies from demo/live
   - **Reason**: Advanced features require Git dependencies
   - **Resolution**: Use demo/live's dependency structure but preserve main's security fixes

4. **server.ts Conflicts**
   - **Action**: Preserve test endpoints from demo/live
   - **Reason**: Demo capabilities require test endpoints
   - **Resolution**: Use demo/live's endpoint structure but preserve main's security gating

**Step 2.3**: Resolve conflicts systematically
```bash
# Check for conflicts
git status

# For each conflict file:
# 1. Open file
# 2. Review conflict markers (<<<<<<<, =======, >>>>>>>)
# 3. Choose correct resolution based on strategy above
# 4. Remove conflict markers
# 5. git add <file>
```

**Step 2.4**: Complete merge
```bash
git commit -m "Merge demo/live into main - combine features with correct architecture

- Preserved advanced features from demo/live:
  - TSSD Vault (Phase 1)
  - Provenance (Phase 1.5)
  - Replay (Phase 2)
  - CPJ ingestion
  - Telegram MTProto collector
  - Advanced enrichment (pattern regime, perp sentiment, news features)
  - Multiple price feeds (BloFin, Coinbase, Coinalyze)
  - Tiny Brains AI/ML integration
  - USS v1.1 canonical flow

- Maintained architectural correctness from main:
  - Validators external to DAG (removed validator nodes)
  - Security fixes (MongoDB credentials, secret scanning)
  - Correct naming (AFI-Reactor, not AFI-Engine)

- Resolved merge conflicts:
  - DAG configuration: removed validator nodes
  - README: updated to 13-node DAG, removed validator section
  - package.json: preserved Git dependencies for advanced features
  - server.ts: preserved test endpoints with security gating"
```

### Phase 3: Post-Merge Validation

**Step 3.1**: Verify DAG configuration
```bash
cat config/dag.codex.json | grep -i validator
```
**Expected**: No output (no validator nodes in DAG)

**Step 3.2**: Verify README
```bash
grep -i "validator" README.md
```
**Expected**: Only references to external validators, not DAG nodes

**Step 3.3**: Verify node count
```bash
grep -c "\"id\":" config/dag.codex.json
```
**Expected**: 13 nodes (not 15)

**Step 3.4**: Run tests
```bash
npm test
```
**Expected**: All tests pass

**Step 3.5**: Run validation
```bash
npm run validate-all
```
**Expected**: All validations pass

### Phase 4: Cleanup

**Step 4.1**: Delete backup branches (if merge successful)
```bash
git branch -D backup-main-before-merge
git branch -D backup-demo-live-before-merge
```

**Step 4.2**: Consider deleting demo/live branch
```bash
# Only if confident in merge and no longer need separate branch
git branch -D demo/live
git push origin --delete demo/live
```
**Caution**: Only do this after thorough testing and validation

### Phase 5: Deployment

**Step 5.1**: Push to remote
```bash
git push origin main
```

**Step 5.2**: Verify remote
```bash
git log --oneline origin/main -1
```
**Expected**: Shows merge commit

**Step 5.3**: Monitor CI/CD
```bash
# Check GitHub Actions for build/test status
```
**Expected**: All checks pass

## Risk Mitigation

### Risk 1: Merge Conflicts
**Mitigation**: 
- Systematic conflict resolution strategy
- Test each file after resolution
- Commit frequently during resolution

### Risk 2: Architectural Regression
**Mitigation**:
- Post-merge validation steps
- Automated checks (grep for validator nodes)
- Manual review of DAG configuration

### Risk 3: Test Failures
**Mitigation**:
- Run full test suite
- Run validation scripts
- Manual testing of key features

### Risk 4: Deployment Issues
**Mitigation**:
- Monitor CI/CD closely
- Have rollback plan ready
- Test in staging environment first

## Success Criteria

Merge is considered successful when:

- [ ] Merge completed without errors
- [ ] All conflicts resolved
- [ ] DAG configuration has no validator nodes
- [ ] README reflects 13-node DAG with correct architecture
- [ ] All tests pass
- [ ] All validations pass
- [ ] CI/CD checks pass
- [ ] Manual testing confirms features work

## Rollback Plan

If merge fails or introduces critical issues:

**Option A**: Reset to backup
```bash
git reset --hard backup-main-before-merge
git push origin main --force
```

**Option B**: Revert merge
```bash
git revert -m 1 HEAD
git push origin main
```

**Option C**: Create fix branch
```bash
git checkout -b fix-merge-issues
# Make fixes
git checkout main
git merge fix-merge-issues
git push origin main
```

## Timeline Estimate

- **Phase 1 (Preparation)**: 15 minutes
- **Phase 2 (Merge Execution)**: 60-120 minutes (depending on conflicts)
- **Phase 3 (Post-Merge Validation)**: 30 minutes
- **Phase 4 (Cleanup)**: 15 minutes
- **Phase 5 (Deployment)**: 30 minutes

**Total**: 2-3 hours

## Dependencies

- Git access to afi-reactor repository
- Node.js/npm environment for running tests
- Access to GitHub Actions for monitoring CI/CD
- Understanding of AFI-Reactor architecture and DAG configuration

## Notes

- This is a complex merge that requires careful attention to architectural principles
- The validator architecture difference is fundamental and cannot be automatically resolved
- Manual testing is critical to ensure features work correctly after merge
- Consider creating a PR for review before merging to main if working in a team

## References

- [`AFI_REACTOR_MAIN_VS_DEMO_LIVE_ANALYSIS.md`](AFI_REACTOR_MAIN_VS_DEMO_LIVE_ANALYSIS.md) - Detailed branch comparison
- [`AFI_REACTOR_BRANCH_ANALYSIS_REPORT.md`](AFI_REACTOR_BRANCH_ANALYSIS_REPORT.md) - Architectural guidelines
- [`afi-reactor/docs/BRANCH_DOCTRINE.v0.1.md`](afi-reactor/docs/BRANCH_DOCTRINE.v0.1.md) - Branch management principles
- [`afi-reactor/config/dag.codex.json`](afi-reactor/config/dag.codex.json) - DAG configuration
- [`afi-reactor/README.md`](afi-reactor/README.md) - Repository documentation

---

**Plan Created**: 2025-12-26  
**Repository**: afi-reactor  
**Branches**: main, demo/live  
**Strategy**: Option 1 - Merge demo/live into main  
**Status**: Ready for execution by Orchestrator mode