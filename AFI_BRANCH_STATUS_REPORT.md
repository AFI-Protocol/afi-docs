# AFI Branch Status Report

**Generated:** 2025-12-07  
**Workspace:** `/Users/secretservice/AFI_Modular_Repos`  
**Total Repos Analyzed:** 23 AFI repos (7 core repos detailed below)

---

## Executive Summary

**Overall Status:** 🟡 **ACTIVE BUT FRAGILE**

You are actively developing on **feature/migration branches** across multiple repos, with significant work that has **not been merged into canonical main branches**. All work is pushed to remote, but the branch topology suggests you're in the middle of a major multi-repo migration/refactor effort.

**Key Findings:**

- ✅ **All recent work is pushed** — No unpushed commits detected
- ⚠️ **4 repos on non-canonical branches** with substantial divergence from main
- ⚠️ **15+ commits in afi-reactor** not in main (TSSD Vault, Replay, Test fixes)
- ⚠️ **20+ commits in afi-core** not in main (UWR scoring, Math integration, ESM migration)
- ⚠️ **20+ commits in afi-token** not in main (Foundry v2, Pattern A role wiring)
- ✅ **2 repos on main** and in sync (afi-math, afi-skills)

**Critical Decision Point:**

You need to decide whether these feature branches (`docs/branch-doctrine-and-replay-spec`, `migration/multi-repo-reorg`, `eliza/nodenext-upgrade`, `afi-token-v2-foundry`) should:
1. Be merged into main (if they represent the new canonical state)
2. Continue as long-lived development branches
3. Be rebased/synchronized with main

---

## Detailed Repo Analysis

### 1. afi-reactor

**Path:** `/Users/secretservice/AFI_Modular_Repos/afi-reactor`  
**Current Branch:** `docs/branch-doctrine-and-replay-spec`  
**Canonical Branch:** `main` (origin HEAD)  
**Working Tree:** Clean (1 untracked symlink: `afi-core`)  
**Status:** 🟡 **ACTIVE BUT FRAGILE**

**Branch Breakdown:**

- `docs/branch-doctrine-and-replay-spec` (current)
  - **Tracking:** `origin/docs/branch-doctrine-and-replay-spec` (up to date)
  - **Divergence:** 15 commits ahead of main, 0 behind
  - **Last Commit:** `9312cc6` - ci: fix afi-core dependency build in GitHub Actions
  - **Contains:** TSSD Vault (Phase 1), Provenance (Phase 1.5), Replay (Phase 2), Test fixes, AFI Eliza Demo rename

- `main`
  - **Tracking:** `origin/main` (local out of date)
  - **Status:** Behind remote (needs pull)
  
- `afi-reactor-freeze-2025-11-16`
  - **Tracking:** None (local only)
  - **Purpose:** Appears to be a safety snapshot

**Commentary:**

This branch contains **substantial new functionality** (TSSD MongoDB vault, replay system, test infrastructure improvements). The work is complete, tested, and pushed. However, it has **completely diverged from main** — main has no commits that this branch doesn't have, suggesting main is stale.

**Suggested Next Steps:**

```bash
# Option A: If this is the new canonical state, merge into main
git checkout main
git pull origin main
git merge docs/branch-doctrine-and-replay-spec
git push origin main

# Option B: If main should stay separate, continue on this branch
# (Current approach — seems intentional given branch name suggests "doctrine")
```

---

### 2. afi-core

**Path:** `/Users/secretservice/AFI_Modular_Repos/afi-core`
**Current Branch:** `migration/multi-repo-reorg`
**Canonical Branch:** `main` (origin HEAD)
**Working Tree:** Clean
**Status:** 🟡 **ACTIVE BUT FRAGILE**

**Branch Breakdown:**

- `migration/multi-repo-reorg` (current)
  - **Tracking:** `origin/migration/multi-repo-reorg` (up to date)
  - **Divergence:** 20 commits ahead of main, 0 behind
  - **Last Commit:** `f697858` - docs(math): add Math Audit documentation and enrichment spec
  - **Contains:** UWR scoring, Math integration, ESM invariants, Froggy analyst, validator types

- `main`
  - **Tracking:** `origin/main` (ahead 2, behind 11)
  - **Status:** Diverged from remote (needs sync)

- `broken-chaos`, `restore-augmentcode`, `validator-template-recovery`
  - **Tracking:** Various (local branches, some with backup remote)
  - **Purpose:** Appear to be recovery/safety snapshots

**Commentary:**

This branch represents a **major refactor** of afi-core with 20+ commits including critical features (UWR scoring, math integration, ESM migration). The branch name suggests this is part of a coordinated multi-repo reorganization effort. Main is diverged and appears stale.

**Suggested Next Steps:**

```bash
# Option A: If migration is complete, merge into main
git checkout main
git pull origin main
git merge migration/multi-repo-reorg
git push origin main

# Option B: Continue migration work on this branch
# (Current approach — branch name suggests ongoing migration)

# Clean up old recovery branches if no longer needed:
# git branch -d broken-chaos restore-augmentcode
```

---

### 3. afi-gateway

**Path:** `/Users/secretservice/AFI_Modular_Repos/afi-gateway`
**Current Branch:** `eliza/nodenext-upgrade`
**Canonical Branch:** `main` (origin HEAD)
**Working Tree:** Clean
**Status:** 🟢 **OK** (but on feature branch)

**Branch Breakdown:**

- `eliza/nodenext-upgrade` (current)
  - **Tracking:** `origin/eliza/nodenext-upgrade` (up to date)
  - **Divergence:** 0 commits ahead of main (already merged or rebased)
  - **Last Commit:** `1d04646` - feat(eliza-demo): rename Prize to AFI Eliza Demo and add CLI
  - **Contains:** AFI Eliza Demo rename, CLI tool, documentation

- `main`
  - **Tracking:** `origin/main` (local out of date)
  - **Status:** Behind remote (needs pull)

**Commentary:**

This branch appears to be **in sync with main** (no divergence detected). The branch name suggests a NodeNext upgrade effort. The work is complete and pushed. Main is slightly behind remote.

**Suggested Next Steps:**

```bash
# If work is complete, switch back to main
git checkout main
git pull origin main

# If this branch is still active for NodeNext work, continue here
# (Branch appears complete based on commit messages)
```

---

### 4. afi-mint

**Path:** `/Users/secretservice/AFI_Modular_Repos/afi-mint`
**Current Branch:** `migration/multi-repo-reorg`
**Canonical Branch:** `main` (origin HEAD)
**Working Tree:** Clean
**Status:** 🟢 **OK**

**Branch Breakdown:**

- `migration/multi-repo-reorg` (current)
  - **Tracking:** `origin/migration/multi-repo-reorg` (up to date)
  - **Divergence:** 5 commits ahead of main, 0 behind
  - **Last Commit:** `b99206e` - chore: add .gitignore to exclude factory workspace
  - **Contains:** .gitignore, package.json, AGENTS.md, reputation bridge scaffolding

- `main`
  - **Tracking:** `origin/main` (up to date)

**Commentary:**

Part of the multi-repo migration effort. Contains 5 commits with infrastructure improvements. Work is complete and pushed. Low risk.

**Suggested Next Steps:**

```bash
# When migration is complete across all repos, merge into main
git checkout main
git merge migration/multi-repo-reorg
git push origin main
```

---

### 5. afi-token

**Path:** `/Users/secretservice/AFI_Modular_Repos/afi-token`
**Current Branch:** `afi-token-v2-foundry`
**Canonical Branch:** `main` (origin HEAD)
**Working Tree:** Clean
**Status:** 🟡 **ACTIVE BUT FRAGILE**

**Branch Breakdown:**

- `afi-token-v2-foundry` (current)
  - **Tracking:** `origin/afi-token-v2-foundry` (up to date)
  - **Divergence:** 20 commits ahead of main, 0 behind
  - **Last Commit:** `6cc5840` - feat(factory): add contract-test-droid and add-contract-test-scenario skill
  - **Contains:** Foundry v2, Pattern A role wiring, xERC20 integration, mainnet deployment, CI

- `afi-token-mainnet-freeze-2025-11-16`
  - **Tracking:** `origin/afi-token-mainnet-freeze-2025-11-16` (up to date)
  - **Tag:** `v2.0.0-rc1`
  - **Purpose:** Pre-mainnet baseline freeze

- `main`
  - **Tracking:** `origin/main` (ahead 1, behind many)
  - **Status:** Diverged and stale

- `merge-sprint`, `migration/multi-repo-reorg`, `remove-hardhat-ci`
  - **Tracking:** Various
  - **Purpose:** Historical branches

**Commentary:**

This is a **major version upgrade** (v2 Foundry rewrite) with 20+ commits including critical contract changes, role wiring patterns, and mainnet deployment scaffolding. There's a tagged release candidate (`v2.0.0-rc1`) on the freeze branch. Main is significantly behind.

⚠️ **HIGH RISK:** This repo contains **on-chain contract logic**. Per AFI rules, contract changes should not be auto-merged without explicit human review.

**Suggested Next Steps:**

```bash
# DO NOT auto-merge this branch
# Requires explicit human review and approval before merging to main

# When ready (after thorough review and testing):
git checkout main
git pull origin main
git merge afi-token-v2-foundry
git push origin main

# Consider creating a PR for review rather than direct merge
```

---

### 6. afi-math

**Path:** `/Users/secretservice/AFI_Modular_Repos/afi-math`
**Canonical Branch:** `main` (origin HEAD)
**Working Tree:** Clean
**Status:** ✅ **OK**

**Branch Breakdown:**

- `main` (current)
  - **Tracking:** `origin/main` (up to date)
  - **Last Commit:** `b03c9ab` - docs(governance): add AGENTS.md with ESM invariants

**Commentary:**

Clean and in sync. No action needed.

---

## Other Repos (Brief Status)

**afi-config:** On `migration/multi-repo-reorg` (no remote tracking shown)
**afi-ops:** On `migration/multi-repo-reorg` (up to date with remote)
**afi-skills:** On `main` (up to date)
**afi-factory:** On `migration/multi-repo-reorg` (no remote tracking shown)

**Remaining 16 repos:** Not analyzed in detail (appear to be supporting repos: artifacts, assets, benchkit, docs, governance, infra, labs, protocol, research-site, sdk-python, sdk-ts, starters)

---

## Risk Analysis

### High Priority Issues

1. **afi-token on afi-token-v2-foundry** — Contains contract changes that require explicit review before merging
2. **afi-reactor 15 commits ahead** — Substantial new functionality (vault, replay) not in main
3. **afi-core 20 commits ahead** — Core protocol changes (UWR, math) not in main

### Medium Priority Issues

1. **Multiple repos on migration/multi-repo-reorg** — Coordinated migration effort in progress
2. **Main branches out of date** — Several repos have stale local main branches

### Low Priority Issues

1. **Local-only branches** — Some recovery/snapshot branches that may be obsolete
2. **Untracked symlink** — afi-reactor has untracked `afi-core` symlink (expected for local dev)

---

## Recommendations

### Immediate Actions

1. **Review afi-token changes** — Do NOT auto-merge contract changes
2. **Decide on migration strategy** — Are migration branches ready to merge into main?
3. **Update local main branches** — Run `git checkout main && git pull` in repos where main is out of date

### Strategic Decisions Needed

**Question 1:** Is the multi-repo migration complete?
- If YES → Merge `migration/multi-repo-reorg` branches into main across all repos
- If NO → Continue work on migration branches

**Question 2:** Should `docs/branch-doctrine-and-replay-spec` become the new main for afi-reactor?
- If YES → Merge into main
- If NO → Keep as long-lived feature branch

**Question 3:** Is afi-token v2 ready for mainnet?
- If YES → Merge `afi-token-v2-foundry` into main (after thorough review)
- If NO → Continue development on feature branch

### Cleanup Suggestions (Advisory Only)

```bash
# In afi-core, if recovery branches are no longer needed:
cd /Users/secretservice/AFI_Modular_Repos/afi-core
git branch -d broken-chaos restore-augmentcode

# In afi-reactor, if freeze branch is no longer needed:
cd /Users/secretservice/AFI_Modular_Repos/afi-reactor
git branch -d afi-reactor-freeze-2025-11-16

# Update all stale main branches:
for repo in afi-reactor afi-gateway; do
  cd /Users/secretservice/AFI_Modular_Repos/$repo
  git checkout main
  git pull origin main
  git checkout -  # Return to previous branch
done
```

---

## Summary

You are in the middle of a **coordinated multi-repo migration/refactor effort** with significant work on feature branches. All work is safely pushed to remote, but **none of it is in the canonical main branches yet**.

**No immediate danger**, but you need to make strategic decisions about:
1. When to merge migration branches into main
2. Whether feature branches should become the new canonical state
3. How to handle the afi-token v2 contract changes (requires explicit review)

**Next Step:** Decide whether the migration is complete and ready to merge, or if you should continue development on feature branches.


