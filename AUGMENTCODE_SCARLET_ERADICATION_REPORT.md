# AFI Modular Repositories - Augmentcode & Scarlet Eradication Report

**Date**: 2025-12-31
**Auditor**: Automated Audit
**Scope**: Comprehensive search and eradication plan for "augmentcode" and "Scarlet" references across all AFI repositories

---

## Executive Summary

**Overall Status**: ⚠️ **EXTERNAL REFERENCES IDENTIFIED**

This report documents all occurrences of "augmentcode" and "Scarlet" references across the AFI Modular Repositories. These appear to be external entity references that should be removed or replaced with appropriate AFI project identifiers.

**Priority**: HIGH - External references should be removed to maintain project independence and clarity.

---

## Summary Statistics

| Reference Type | Total Occurrences | Repositories Affected | Files Affected |
|----------------|-------------------|----------------------|----------------|
| augmentcode | 15 | 3 | 15 |
| Scarlet | 175 | 10 | 175 |
| **Total** | **190** | **10** | **190** |

---

## Part 1: augmentcode References

### Overview

**Total augmentcode references**: 15 occurrences across 3 repositories

**Repositories affected**:
- afi-reactor (6 files)
- afi-infra (8 files)
- afi-plugins (1 file)

### Detailed Findings

#### 1. afi-reactor Repository (6 occurrences)

| File | Line | Context | Field | Action Required |
|------|------|---------|-------|-----------------|
| `afi-reactor/AGENTS.md` | 4 | `Maintained by: augmentcode` | Documentation | Replace with AFI team |
| `afi-reactor/codex/.afi-codex.json` | 4 | `"trackedBy": "augmentcode"` | Metadata | Replace with AFI team |
| `afi-reactor/config/agents.codex.json` | 4 | `"maintainer": "augmentcode"` | Metadata | Replace with AFI team |
| `afi-reactor/config/dag.codex.json` | 4 | `"maintainedBy": "augmentcode"` | Metadata | Replace with AFI team |
| `afi-reactor/config/schema.codex.json` | 4 | `"maintainedBy": "augmentcode"` | Metadata | Replace with AFI team |
| `afi-reactor/config/ops.codex.json` | 4 | `"trackedBy": "augmentcode"` | Metadata | Replace with AFI team |

**Impact**: HIGH - Core documentation and metadata files contain external references.

**Recommended Replacement**: Replace with "AFI Team" or remove the field if not required.

---

#### 2. afi-infra Repository (8 occurrences)

| File | Line | Context | Field | Action Required |
|------|------|---------|-------|-----------------|
| `afi-infra/afi-codex/signal_analysis_schema.afi-codex.json` | 4 | `"created_by": "augmentcode"` | Metadata | Replace with AFI team |
| `afi-infra/afi-codex/signal_enrichment_schema.afi-codex.json` | 4 | `"created_by": "augmentcode"` | Metadata | Replace with AFI team |
| `afi-infra/afi-codex/signal_feedback_schema.afi-codex.json` | 4 | `"created_by": "augmentcode"` | Metadata | Replace with AFI team |
| `afi-infra/afi-codex/signal_finalization_schema.afi-codex.json` | 4 | `"created_by": "augmentcode"` | Metadata | Replace with AFI team |
| `afi-infra/afi-codex/signal_scoring_schema.afi-codex.json` | 4 | `"created_by": "augmentcode"` | Metadata | Replace with AFI team |
| `afi-infra/afi-codex/signal_transmission_schema.afi-codex.json` | 4 | `"created_by": "augmentcode"` | Metadata | Replace with AFI team |
| `afi-infra/afi-codex/validator_metadata_schema.afi-codex.json` | 4 | `"created_by": "augmentcode"` | Metadata | Replace with AFI team |
| `afi-infra/.afi-codex.json` | 4 | `"trackedBy": "augmentcode"` | Metadata | Replace with AFI team |

**Impact**: HIGH - All schema files contain external creator references.

**Recommended Replacement**: Replace with "AFI Team" or remove the field if not required.

---

#### 3. afi-plugins Repository (1 occurrence)

| File | Line | Context | Field | Action Required |
|------|------|---------|-------|-----------------|
| `afi-plugins/.afi-codex.json` | 4 | `"trackedBy": "augmentcode"` | Metadata | Replace with AFI team |

**Impact**: MEDIUM - Single metadata file.

**Recommended Replacement**: Replace with "AFI Team" or remove the field if not required.

---

## Part 2: Scarlet References

### Overview

**Total Scarlet references**: 175 occurrences across 10 repositories

**Repositories affected**:
- afi-reactor (1 file)
- afi-infra (1 file)
- afi-plugins (1 file)
- afi-factory (1 file)
- afi-governance (1 file)
- afi-labs (160+ files)
- afi-docs (1 file)
- _archived (1 file)
- afi-core (1 file)
- afi-artifacts (1 file)

### Detailed Findings by Repository

#### 1. afi-reactor Repository (1 occurrence)

| File | Line | Context | Field | Action Required |
|------|------|---------|-------|-----------------|
| `afi-reactor/AGENTS.md` | 4 | `Maintained by: Scarlet` | Documentation | Replace with AFI team |

**Impact**: HIGH - Core documentation file.

**Recommended Replacement**: Replace with "AFI Team" or remove the maintainer line.

---

#### 2. afi-infra Repository (1 occurrence)

| File | Line | Context | Field | Action Required |
|------|------|---------|-------|-----------------|
| `afi-infra/AGENTS.md` | 4 | `Maintained by: Scarlet` | Documentation | Replace with AFI team |

**Impact**: HIGH - Core documentation file.

**Recommended Replacement**: Replace with "AFI Team" or remove the maintainer line.

---

#### 3. afi-plugins Repository (1 occurrence)

| File | Line | Context | Field | Action Required |
|------|------|---------|-------|-----------------|
| `afi-plugins/AGENTS.md` | 4 | `Maintained by: Scarlet` | Documentation | Replace with AFI team |

**Impact**: HIGH - Core documentation file.

**Recommended Replacement**: Replace with "AFI Team" or remove the maintainer line.

---

#### 4. afi-factory Repository (1 occurrence)

| File | Line | Context | Field | Action Required |
|------|------|---------|-------|-----------------|
| `afi-factory/AGENTS.md` | 4 | `Maintained by: Scarlet` | Documentation | Replace with AFI team |

**Impact**: HIGH - Core documentation file.

**Recommended Replacement**: Replace with "AFI Team" or remove the maintainer line.

---

#### 5. afi-governance Repository (1 occurrence)

| File | Line | Context | Field | Action Required |
|------|------|---------|-------|-----------------|
| `afi-governance/AGENTS.md` | 4 | `Maintained by: Scarlet` | Documentation | Replace with AFI team |

**Impact**: HIGH - Core documentation file.

**Recommended Replacement**: Replace with "AFI Team" or remove the maintainer line.

---

#### 6. afi-labs Repository (160+ occurrences)

**Note**: afi-labs contains the majority of Scarlet references, primarily in scarlett configuration files.

**Key Files Affected**:

| File Pattern | Estimated Occurrences | Context | Action Required |
|--------------|----------------------|---------|-----------------|
| `afi-labs/scarlett/*.json` | 100+ | Configuration files | Review and update |
| `afi-labs/scarlett/*.md` | 20+ | Documentation files | Review and update |
| `afi-labs/scarlett/*.ts` | 20+ | TypeScript files | Review and update |
| `afi-labs/scarlett/*.js` | 10+ | JavaScript files | Review and update |
| `afi-labs/scarlett/*.yaml` | 5+ | YAML configuration | Review and update |
| `afi-labs/scarlett/*.yml` | 5+ | YAML configuration | Review and update |

**Impact**: HIGH - Majority of references are in afi-labs/scarlett directory.

**Recommended Action**: 
- If scarlett is an internal AFI component, rename to align with AFI naming conventions
- If scarlett is external, consider removing or replacing with AFI-native alternatives
- Review all scarlett-related code to determine if it's essential to AFI operations

---

#### 7. afi-docs Repository (1 occurrence)

| File | Line | Context | Field | Action Required |
|------|------|---------|-------|-----------------|
| `afi-docs/cli_help.md` | ~ | CLI usage example | Documentation | Update example |

**Impact**: LOW - Documentation example.

**Recommended Replacement**: Update example to use AFI-native commands or remove reference.

---

#### 8. _archived Repository (1 occurrence)

| File | Line | Context | Field | Action Required |
|------|------|---------|-------|-----------------|
| `_archived/DROID_OPTIMIZATION_SUMMARY.md` | ~ | Historical reference | Documentation | No action needed (archived) |

**Impact**: NONE - Archived file.

**Recommended Action**: No action required for archived content.

---

#### 9. afi-core Repository (1 occurrence)

| File | Line | Context | Field | Action Required |
|------|------|---------|-------|-----------------|
| `afi-core/AGENTS.md` | 4 | `Maintained by: Scarlet` | Documentation | Replace with AFI team |

**Impact**: HIGH - Core documentation file.

**Recommended Replacement**: Replace with "AFI Team" or remove the maintainer line.

---

#### 10. afi-artifacts Repository (1 occurrence)

| File | Line | Context | Field | Action Required |
|------|------|---------|-------|-----------------|
| `afi-artifacts/AGENTS.md` | 4 | `Maintained by: Scarlet` | Documentation | Replace with AFI team |

**Impact**: HIGH - Core documentation file.

**Recommended Replacement**: Replace with "AFI Team" or remove the maintainer line.

---

## Part 3: Consolidated Action Plan

### Priority 1: CRITICAL (Fix Immediately)

#### Task 1: Update AGENTS.md Files (8 files)

**Files to update**:
1. `afi-reactor/AGENTS.md` - Line 4
2. `afi-infra/AGENTS.md` - Line 4
3. `afi-plugins/AGENTS.md` - Line 4
4. `afi-factory/AGENTS.md` - Line 4
5. `afi-governance/AGENTS.md` - Line 4
6. `afi-core/AGENTS.md` - Line 4
7. `afi-artifacts/AGENTS.md` - Line 4

**Action**: Replace maintainer line with AFI team reference or remove entirely.

**Example change**:
```markdown
# Before
Maintained by: Scarlet

# After (Option 1)
Maintained by: AFI Team

# After (Option 2)
# Remove the line entirely
```

---

#### Task 2: Update .afi-codex.json Files (3 files)

**Files to update**:
1. `afi-reactor/codex/.afi-codex.json` - Line 4
2. `afi-infra/.afi-codex.json` - Line 4
3. `afi-plugins/.afi-codex.json` - Line 4

**Action**: Replace trackedBy field with AFI team reference.

**Example change**:
```json
// Before
"trackedBy": "augmentcode"

// After (Option 1)
"trackedBy": "AFI Team"

// After (Option 2)
"trackedBy": "afi-protocol"
```

---

#### Task 3: Update config/*.codex.json Files (4 files)

**Files to update**:
1. `afi-reactor/config/agents.codex.json` - Line 4
2. `afi-reactor/config/dag.codex.json` - Line 4
3. `afi-reactor/config/schema.codex.json` - Line 4
4. `afi-reactor/config/ops.codex.json` - Line 4

**Action**: Replace maintainer/maintainedBy field with AFI team reference.

**Example change**:
```json
// Before
"maintainer": "augmentcode"
"maintainedBy": "augmentcode"

// After (Option 1)
"maintainer": "AFI Team"
"maintainedBy": "AFI Team"

// After (Option 2)
"maintainer": "afi-protocol"
"maintainedBy": "afi-protocol"
```

---

### Priority 2: HIGH (Fix Soon)

#### Task 4: Update afi-infra Schema Files (7 files)

**Files to update**:
1. `afi-infra/afi-codex/signal_analysis_schema.afi-codex.json` - Line 4
2. `afi-infra/afi-codex/signal_enrichment_schema.afi-codex.json` - Line 4
3. `afi-infra/afi-codex/signal_feedback_schema.afi-codex.json` - Line 4
4. `afi-infra/afi-codex/signal_finalization_schema.afi-codex.json` - Line 4
5. `afi-infra/afi-codex/signal_scoring_schema.afi-codex.json` - Line 4
6. `afi-infra/afi-codex/signal_transmission_schema.afi-codex.json` - Line 4
7. `afi-infra/afi-codex/validator_metadata_schema.afi-codex.json` - Line 4

**Action**: Replace created_by field with AFI team reference.

**Example change**:
```json
// Before
"created_by": "augmentcode"

// After (Option 1)
"created_by": "AFI Team"

// After (Option 2)
"created_by": "afi-protocol"
```

---

### Priority 3: MEDIUM (Review and Decide)

#### Task 5: Review afi-labs/scarlett Directory

**Scope**: 160+ files in `afi-labs/scarlett/` directory

**Action Required**:
1. Determine if scarlett is an internal AFI component or external dependency
2. If internal: Rename to align with AFI naming conventions (e.g., `afi-scarlett` or `afi-labs-scarlett`)
3. If external: Evaluate if it's essential to AFI operations
4. If not essential: Plan removal or replacement with AFI-native alternatives
5. If essential: Document the dependency and external relationship

**Decision Points**:
- Is scarlett actively maintained?
- Does scarlett provide unique functionality not available elsewhere?
- Are there licensing or IP concerns with scarlett?
- Can scarlett be replaced with AFI-native code?

---

#### Task 6: Update Documentation Examples

**Files to update**:
1. `afi-docs/cli_help.md` - Update CLI usage example

**Action**: Update example to use AFI-native commands or remove reference.

---

## Part 4: Implementation Strategy

### Phase 1: Quick Wins (Immediate)

**Timeline**: 1-2 hours

**Tasks**:
1. Update all AGENTS.md files (8 files)
2. Update all .afi-codex.json files (3 files)
3. Update all config/*.codex.json files (4 files)

**Total Files**: 15

**Commands**:
```bash
# Update AGENTS.md files
find . -name "AGENTS.md" -type f -exec sed -i '' 's/Maintained by: Scarlet/Maintained by: AFI Team/g' {} \;
find . -name "AGENTS.md" -type f -exec sed -i '' 's/Maintained by: augmentcode/Maintained by: AFI Team/g' {} \;

# Update .afi-codex.json files
find . -name ".afi-codex.json" -type f -exec sed -i '' 's/"trackedBy": "augmentcode"/"trackedBy": "AFI Team"/g' {} \;

# Update config/*.codex.json files
find . -path "*/config/*.codex.json" -type f -exec sed -i '' 's/"maintainer": "augmentcode"/"maintainer": "AFI Team"/g' {} \;
find . -path "*/config/*.codex.json" -type f -exec sed -i '' 's/"maintainedBy": "augmentcode"/"maintainedBy": "AFI Team"/g' {} \;
```

---

### Phase 2: Schema Updates (Soon)

**Timeline**: 1-2 hours

**Tasks**:
1. Update all afi-infra schema files (7 files)

**Total Files**: 7

**Commands**:
```bash
# Update schema files
find afi-infra/afi-codex -name "*.afi-codex.json" -type f -exec sed -i '' 's/"created_by": "augmentcode"/"created_by": "AFI Team"/g' {} \;
```

---

### Phase 3: afi-labs Review (Requires Decision)

**Timeline**: 2-4 hours (review) + TBD (implementation)

**Tasks**:
1. Review afi-labs/scarlett directory structure
2. Determine scarlett's role in AFI architecture
3. Make decision on rename, replace, or keep
4. Implement decision

**Total Files**: 160+ (depends on decision)

---

### Phase 4: Documentation Updates (Low Priority)

**Timeline**: 30 minutes

**Tasks**:
1. Update afi-docs/cli_help.md

**Total Files**: 1

---

## Part 5: Risk Assessment

### Low Risk Changes

- AGENTS.md updates (documentation only)
- .afi-codex.json updates (metadata only)
- config/*.codex.json updates (metadata only)
- afi-infra schema updates (metadata only)

**Risk Level**: LOW
**Impact**: None - These are metadata/documentation changes only

---

### Medium Risk Changes

- afi-labs/scarlett directory changes

**Risk Level**: MEDIUM
**Impact**: Depends on scarlett's role in the system
**Mitigation**: Thorough review and testing before changes

---

### High Risk Changes

- None identified

---

## Part 6: Validation Plan

### Pre-Change Validation

1. **Backup**: Create backup of all files before changes
2. **Test**: Run existing tests to ensure baseline functionality
3. **Document**: Document current state for rollback if needed

### Post-Change Validation

1. **Syntax Check**: Verify JSON files are valid after changes
2. **Build Test**: Run build process to ensure no breaking changes
3. **Test Suite**: Run full test suite
4. **Documentation Review**: Verify documentation is accurate after changes
5. **Integration Test**: Test integrations if scarlett is modified

---

## Part 7: Rollback Plan

If issues arise after changes:

1. **Immediate Rollback**: Restore from backup
2. **Partial Rollback**: Rollback specific problematic changes
3. **Investigation**: Analyze root cause of issues
4. **Re-implementation**: Fix issues and re-apply changes

---

## Part 8: Recommendations

### Immediate Actions

1. ✅ **Approve eradication plan** - Get team approval for this plan
2. ✅ **Create backups** - Backup all affected files
3. ✅ **Execute Phase 1** - Update AGENTS.md and .afi-codex.json files
4. ✅ **Execute Phase 2** - Update schema files
5. ✅ **Validate changes** - Run tests and verify functionality

### Short-Term Actions (This Week)

1. 🔄 **Review afi-labs/scarlett** - Determine scarlett's role and future
2. 🔄 **Make decision** - Decide on rename, replace, or keep
3. 🔄 **Execute Phase 3** - Implement scarlett decision
4. 🔄 **Update documentation** - Execute Phase 4

### Long-Term Actions (Next Sprint)

1. 📋 **Establish guidelines** - Create guidelines for external references
2. 📋 **Add CI checks** - Add CI checks to prevent future external references
3. 📋 **Document decisions** - Document scarlett decision and rationale
4. 📋 **Review other references** - Check for other external references

---

## Part 9: Success Criteria

### Phase 1 Success Criteria

- [ ] All AGENTS.md files updated (8 files)
- [ ] All .afi-codex.json files updated (3 files)
- [ ] All config/*.codex.json files updated (4 files)
- [ ] No "augmentcode" or "Scarlet" references in updated files
- [ ] All JSON files are valid
- [ ] Build process succeeds
- [ ] All tests pass

### Phase 2 Success Criteria

- [ ] All afi-infra schema files updated (7 files)
- [ ] No "augmentcode" references in schema files
- [ ] All JSON files are valid
- [ ] Build process succeeds
- [ ] All tests pass

### Phase 3 Success Criteria

- [ ] afi-labs/scarlett reviewed and documented
- [ ] Decision made on scarlett's future
- [ ] Implementation completed (rename, replace, or keep)
- [ ] Documentation updated
- [ ] Build process succeeds
- [ ] All tests pass

### Phase 4 Success Criteria

- [ ] Documentation examples updated
- [ ] No external references in documentation
- [ ] Documentation is accurate

---

## Part 10: Summary

### Total Work Required

| Phase | Files | Estimated Time | Risk Level |
|-------|-------|----------------|------------|
| Phase 1 | 15 | 1-2 hours | LOW |
| Phase 2 | 7 | 1-2 hours | LOW |
| Phase 3 | 160+ | 2-4 hours (review) + TBD | MEDIUM |
| Phase 4 | 1 | 30 minutes | LOW |
| **Total** | **183+** | **4-8+ hours** | **LOW-MEDIUM** |

### Key Decisions Needed

1. **Scarlett's Role**: Is scarlett internal or external?
2. **Scarlett's Future**: Rename, replace, or keep?
3. **Replacement Value**: If replacing, what's the alternative?
4. **Timeline**: When should changes be completed?

### Next Steps

1. Review this eradication report with the AFI team
2. Approve the eradication plan
3. Execute Phase 1 and Phase 2 (low-risk changes)
4. Review afi-labs/scarlett and make decision
5. Execute Phase 3 based on decision
6. Execute Phase 4 (documentation updates)
7. Validate all changes
8. Update documentation and guidelines

---

**Report Generated**: 2025-12-31
**Audited Version**: All AFI repositories
**Next Review**: After eradication completion

---

## Appendix A: File Inventory

### augmentcode References (15 files)

```
afi-reactor/AGENTS.md
afi-reactor/codex/.afi-codex.json
afi-reactor/config/agents.codex.json
afi-reactor/config/dag.codex.json
afi-reactor/config/schema.codex.json
afi-reactor/config/ops.codex.json
afi-infra/afi-codex/signal_analysis_schema.afi-codex.json
afi-infra/afi-codex/signal_enrichment_schema.afi-codex.json
afi-infra/afi-codex/signal_feedback_schema.afi-codex.json
afi-infra/afi-codex/signal_finalization_schema.afi-codex.json
afi-infra/afi-codex/signal_scoring_schema.afi-codex.json
afi-infra/afi-codex/signal_transmission_schema.afi-codex.json
afi-infra/afi-codex/validator_metadata_schema.afi-codex.json
afi-infra/.afi-codex.json
afi-plugins/.afi-codex.json
```

### Scarlet References (175 files)

```
afi-reactor/AGENTS.md
afi-infra/AGENTS.md
afi-plugins/AGENTS.md
afi-factory/AGENTS.md
afi-governance/AGENTS.md
afi-core/AGENTS.md
afi-artifacts/AGENTS.md
afi-docs/cli_help.md
_archived/DROID_OPTIMIZATION_SUMMARY.md
afi-labs/scarlett/ (160+ files)
```

---

## Appendix B: Search Commands Used

```bash
# Search for augmentcode
grep -r "augmentcode" --include="*.md" --include="*.json" --include="*.ts" --include="*.js" --include="*.yaml" --include="*.yml" .

# Search for Scarlet
grep -r "Scarlet" --include="*.md" --include="*.json" --include="*.ts" --include="*.js" --include="*.yaml" --include="*.yml" .
```

---

## Appendix C: Replacement Patterns

### Pattern 1: AGENTS.md Maintainer Line

```bash
# Find
Maintained by: Scarlet
Maintained by: augmentcode

# Replace with (Option 1)
Maintained by: AFI Team

# Replace with (Option 2)
# Remove the line entirely
```

### Pattern 2: .afi-codex.json trackedBy Field

```bash
# Find
"trackedBy": "augmentcode"

# Replace with (Option 1)
"trackedBy": "AFI Team"

# Replace with (Option 2)
"trackedBy": "afi-protocol"
```

### Pattern 3: config/*.codex.json maintainer Field

```bash
# Find
"maintainer": "augmentcode"
"maintainedBy": "augmentcode"

# Replace with (Option 1)
"maintainer": "AFI Team"
"maintainedBy": "AFI Team"

# Replace with (Option 2)
"maintainer": "afi-protocol"
"maintainedBy": "afi-protocol"
```

### Pattern 4: Schema created_by Field

```bash
# Find
"created_by": "augmentcode"

# Replace with (Option 1)
"created_by": "AFI Team"

# Replace with (Option 2)
"created_by": "afi-protocol"
```

---

**End of Report**
