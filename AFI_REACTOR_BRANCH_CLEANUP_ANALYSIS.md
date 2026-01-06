# AFI-Reactor Branch Cleanup Analysis

## Executive Summary

This analysis examines two branches in the afi-reactor repository to determine if they are still needed:
- `feature/remove-dag-validators`
- `release/reactor-scored-only-public`

**Conclusion**: Both branches can be safely deleted after pushing the validator removal changes to remote main.

## Branch Analysis

### 1. feature/remove-dag-validators

**Status**: ✅ **CAN BE DELETED** (after pushing to remote)

**Purpose**: Remove validator nodes from DAG configuration because validators should be external to reactor, not nodes within it.

**Key Commit**: `d85a446` - "fix: remove validator nodes from DAG - validators should be external to reactor"

**Changes Made**:
- Removed `afi-ensemble-score` node from [`config/dag.codex.json`](afi-reactor/config/dag.codex.json)
- Removed `validator-decision-node` from [`config/dag.codex.json`](afi-reactor/config/dag.codex.json)
- Updated [`README.md`](afi-reactor/README.md) to reflect 13-node DAG instead of 15-node DAG
- Removed validator section from README DAG description

**Current State**:
- Local `main` branch is at commit `d85a446` (same as this branch)
- Remote `origin/main` is at commit `19ad90d` (merge commit, 1 commit behind)
- Local `origin/feature/remove-dag-validators` is at commit `d85a446`
- This branch is identical to local `main` (no diff)

**Architectural Alignment**: ✅ **CORRECT**
- Aligns with [`AFI_REACTOR_BRANCH_ANALYSIS_REPORT.md`](AFI_REACTOR_BRANCH_ANALYSIS_REPORT.md) recommendation
- Validators should be external to DAG, not nodes within it
- Current DAG configuration has no validator nodes (correct architecture)

**Recommendation**: 
1. Push local `main` to `origin/main` to propagate validator removal
2. Delete both local and remote `feature/remove-dag-validators` branches

---

### 2. release/reactor-scored-only-public

**Status**: ❌ **CAN BE DELETED** (contains incorrect architecture)

**Purpose**: Create a "scored-only public runtime" with isolated vault, removing demo/validator/replay functionality.

**Key Commit**: `96c5111` - "Reactor: scored-only public runtime (isolated vault, no demo/validator/replay)"

**Changes Made**:
- Massive refactoring (8048 files changed, 14928 insertions, 1517665 deletions)
- Added `afi-ensemble-score` node to [`config/dag.codex.json`](afi-reactor/config/dag.codex.json)
- Added `validator-decision-node` to [`config/dag.codex.json`](afi-reactor/config/dag.codex.json)
- Updated [`README.md`](afi-reactor/README.md) to reference "AFI-Engine" (old naming) instead of "AFI-Reactor"
- Updated README to reflect 15-node DAG instead of 13-node DAG
- Added validator section to README DAG description

**Current State**:
- Branch is at commit `0e372b0` (parent of merge commit `19ad90d`)
- Remote `origin/release/reactor-scored-only-public` is at commit `0e372b0`
- This branch was merged into `main` via PR #12 (commit `19ad90d`)
- The merge has since been corrected by `feature/remove-dag-validators`

**Architectural Alignment**: ❌ **INCORRECT**
- Violates [`AFI_REACTOR_BRANCH_ANALYSIS_REPORT.md`](AFI_REACTOR_BRANCH_ANALYSIS_REPORT.md) recommendation
- Validators should be external to DAG, not nodes within it
- Uses old "AFI-Engine" naming (repo was renamed to "AFI-Reactor" on 2025-11-14)
- Contains outdated documentation

**Recommendation**: 
1. Delete both local and remote `release/reactor-scored-only-public` branches
2. The useful changes from this branch (security fixes, CI improvements) are already in main
3. The incorrect architectural changes (validator nodes in DAG) have been corrected

---

## Git History Context

```
* d85a446 (HEAD -> feature/remove-dag-validators, origin/feature/remove-dag-validators, main) 
  fix: remove validator nodes from DAG - validators should be external to reactor
*   19ad90d (origin/main, origin/HEAD) 
  Merge pull request #12 from AFI-Protocol/release/reactor-scored-only-public
|\  
| * 0e372b0 (origin/release/reactor-scored-only-public, release/reactor-scored-only-public) 
  ci: build afi-core and rely on package exports
| * 96c5111 
  Reactor: scored-only public runtime (isolated vault, no demo/validator/replay)
|/  
*   9915a27 (release/reactor-live-testing) 
  security: Eliminate exposed MongoDB credentials and add secret scanning
```

## Current Repository State

### Local Branches
- `main` - at commit `d85a446` (validator removal applied)
- `feature/remove-dag-validators` - at commit `d85a446` (identical to main)
- `release/reactor-scored-only-public` - at commit `0e372b0` (incorrect architecture)

### Remote Branches
- `origin/main` - at commit `19ad90d` (merge commit, needs validator removal)
- `origin/feature/remove-dag-validators` - at commit `d85a446` (validator removal)
- `origin/release/reactor-scored-only-public` - at commit `0e372b0` (incorrect architecture)

### Current HEAD
- HEAD is on `feature/remove-dag-validators` (commit `d85a446`)

## Recommendations

### Immediate Actions

1. **Push validator removal to remote main**:
   ```bash
   git checkout main
   git push origin main
   ```
   This will propagate the validator removal changes to `origin/main`.

2. **Delete feature/remove-dag-validators branches**:
   ```bash
   git branch -d feature/remove-dag-validators
   git push origin --delete feature/remove-dag-validators
   ```
   This branch has served its purpose and is no longer needed.

3. **Delete release/reactor-scored-only-public branches**:
   ```bash
   git branch -D release/reactor-scored-only-public
   git push origin --delete release/reactor-scored-only-public
   ```
   This branch contains incorrect architecture and outdated naming.

### Rationale

**Why delete feature/remove-dag-validators?**
- Changes have been applied to local `main` branch
- Branch is identical to `main` (no diff)
- Purpose was to remove validator nodes, which is now complete
- Keeping it creates confusion about which branch is canonical

**Why delete release/reactor-scored-only-public?**
- Contains incorrect architecture (validator nodes in DAG)
- Uses outdated "AFI-Engine" naming
- Was merged into main via PR #12, but has since been corrected
- Useful changes (security, CI) are already preserved in main
- Keeping it risks accidental re-introduction of incorrect architecture

### Branch Doctrine Compliance

According to [`afi-reactor/docs/BRANCH_DOCTRINE.v0.1.md`](afi-reactor/docs/BRANCH_DOCTRINE.v0.1.md):

- **feature/*** branches should be short-lived and focused ✅
- **release/*** branches are not mentioned in doctrine (human-only operations)
- Branches should be deleted after merging ✅
- No history rewrites on main ✅

Both branches comply with the doctrine's intent of keeping the repository clean and focused.

## Architectural Impact

### Before Cleanup
- Confusion about which branch contains correct architecture
- Risk of accidentally using incorrect validator-in-DAG configuration
- Outdated documentation references in release branch

### After Cleanup
- Single source of truth: `main` branch with correct architecture
- No validator nodes in DAG (correct external validator architecture)
- Clean branch history aligned with branch doctrine
- Reduced risk of architectural regression

## Verification Steps

After cleanup, verify:

1. **Main branch has correct architecture**:
   ```bash
   git checkout main
   git log --oneline -1
   # Should show: d85a446 fix: remove validator nodes from DAG
   ```

2. **DAG configuration has no validator nodes**:
   ```bash
   cat config/dag.codex.json | grep -i validator
   # Should return nothing
   ```

3. **Remote branches are deleted**:
   ```bash
   git branch -r | grep -E "feature/remove-dag-validators|release/reactor-scored-only-public"
   # Should return nothing
   ```

4. **Local branches are deleted**:
   ```bash
   git branch | grep -E "feature/remove-dag-validators|release/reactor-scored-only-public"
   # Should return nothing
   ```

## Conclusion

Both branches can be safely deleted:

- **feature/remove-dag-validators**: ✅ Completed its purpose, changes are in main
- **release/reactor-scored-only-public**: ❌ Contains incorrect architecture, has been corrected

The cleanup will:
- Align the repository with correct architectural principles
- Remove confusion about which branch is canonical
- Prevent accidental re-introduction of incorrect architecture
- Maintain compliance with branch doctrine

**Next Steps**: Execute the recommended cleanup commands and verify the results.

---

**Analysis Date**: 2025-12-26  
**Repository**: afi-reactor  
**Branches Analyzed**: feature/remove-dag-validators, release/reactor-scored-only-public  
**Status**: Ready for cleanup
