# AFI CLI Standardization Implementation Plan

## Executive Summary

Following the comprehensive CLI audit of the AFI repositories, this plan addresses the critical finding that the project relies on **6 disparate CLI frameworks** across **15 implementations** with no unified approach. This creates maintenance overhead, inconsistent user experience, and development friction.

**Key Issues Identified:**
- Python: Click (afi-benchkit) vs argparse (afi-econ, afi-tiny-brains)
- Node.js: Commander.js (afi-econ) vs custom implementations vs stubs
- Shell scripts: No standardization across 50+ scripts
- No shared CLI utilities or standards

**Proposed Solution:** Establish a unified CLI framework ecosystem with standardized patterns, shared utilities, and consistent developer experience.

---

## Phase 1: Foundation (Weeks 1-2)

### 1.1 Create Shared CLI Framework Library
**Objective:** Develop `@afi/cli-framework` as the foundation for all AFI CLIs

**Deliverables:**
- `@afi/cli-framework` npm package with TypeScript utilities
- `afi-cli-shared` Python package for common CLI utilities
- Standardized error handling, logging, and help text patterns
- Configuration management utilities

**Responsible:** AFI Core Team (TypeScript) + Python Lead
**Timeline:** 1 week
**Risk Assessment:**
- **HIGH:** Requires coordination between Python and Node.js teams
- **MEDIUM:** Potential breaking changes to existing CLIs
- **LOW:** Well-established patterns in both ecosystems

**Success Criteria:**
- Package published to internal registry
- Basic CLI utilities (logging, config, validation) implemented
- Documentation for framework usage

### 1.2 Establish CLI Standards Document
**Objective:** Define comprehensive standards for all AFI CLIs

**Deliverables:**
- `docs/cli-standards.md` with complete specifications
- Naming conventions for commands, options, and arguments
- Help text formatting standards
- Error message patterns
- Testing requirements for CLI commands

**Responsible:** Technical Writing Team + CLI Audit Lead
**Timeline:** 3 days
**Risk Assessment:**
- **LOW:** Purely documentation, no code changes
- **LOW:** Standards can be adopted incrementally

**Success Criteria:**
- Document reviewed and approved by all repository maintainers
- Standards document linked from all repository READMEs

---

## Phase 2: Python CLI Standardization (Weeks 3-4)

### 2.1 Migrate afi-econ Python CLI to Click
**Objective:** Standardize afi-econ on Click framework for consistency

**Current State:** Uses argparse with 10+ subcommands
**Target State:** Click-based CLI with shared utilities

**Deliverables:**
- Migrate `afi_econ_kit/cli.py` from argparse to Click
- Integrate `@afi/cli-framework` utilities
- Maintain backward compatibility during transition
- Update documentation and examples

**Responsible:** afi-econ Python Developer
**Timeline:** 1 week
**Risk Assessment:**
- **MEDIUM:** argparse to Click migration requires careful testing
- **LOW:** Both frameworks are mature and well-documented
- **HIGH:** afi-econ CLI is production-critical for economic simulations

**Success Criteria:**
- All existing CLI functionality preserved
- Click framework adopted
- Shared utilities integrated
- All tests passing

### 2.2 Migrate afi-tiny-brains CLI to Click
**Objective:** Standardize ML training scripts on Click

**Current State:** Uses argparse for HMM and LightGBM training
**Target State:** Click-based CLI with shared utilities

**Deliverables:**
- Migrate training scripts to Click framework
- Add shared CLI utilities for ML workflows
- Improve error handling and user feedback
- Update training documentation

**Responsible:** afi-tiny-brains ML Engineer
**Timeline:** 3 days
**Risk Assessment:**
- **LOW:** Simple migration, training scripts are not production-critical
- **LOW:** Well-established migration path

**Success Criteria:**
- Training scripts use Click framework
- Shared utilities integrated
- Documentation updated

---

## Phase 3: Node.js/TypeScript CLI Standardization (Weeks 5-6)

### 3.1 Standardize afi-econ TypeScript CLI
**Objective:** Ensure afi-econ TypeScript CLI follows standards

**Current State:** Uses Commander.js (already correct choice)
**Target State:** Commander.js with shared utilities and standards compliance

**Deliverables:**
- Integrate `@afi/cli-framework` utilities
- Apply CLI standards (help text, error handling, etc.)
- Add comprehensive testing for CLI commands
- Update package.json scripts

**Responsible:** afi-econ TypeScript Developer
**Timeline:** 3 days
**Risk Assessment:**
- **LOW:** Already uses Commander.js, just needs utilities integration
- **LOW:** Well-established framework

**Success Criteria:**
- Shared utilities integrated
- Standards compliance verified
- CLI tests added

### 3.2 Implement Production CLIs for Development Repos
**Objective:** Replace stubs with production-ready CLIs in afi-governance, afi-mint

**Current State:** Placeholder/stub implementations
**Target State:** Functional CLIs using Commander.js + shared utilities

**Deliverables:**
- afi-governance: Proposal submission and validation CLI
- afi-mint: Minting simulation and challenge CLI
- Integration with shared CLI framework
- Basic functionality implementation

**Responsible:** Governance Team + Minting Team
**Timeline:** 1 week
**Risk Assessment:**
- **MEDIUM:** Requires implementing actual business logic
- **HIGH:** Governance and minting are security-critical areas
- **LOW:** Can start with safe, read-only operations

**Success Criteria:**
- Functional CLIs replace stubs
- Commander.js framework used
- Shared utilities integrated
- Basic security validations in place

### 3.3 Standardize afi-reactor CLI Entry Points
**Objective:** Clean up inconsistent CLI patterns in afi-reactor

**Current State:** Mix of custom scripts and tsx execution
**Target State:** Standardized Commander.js CLI with proper entry points

**Deliverables:**
- Create proper `afi-reactor-cli` package
- Standardize DAG execution, replay, and validation commands
- Integrate shared utilities
- Update package.json scripts

**Responsible:** afi-reactor Core Team
**Timeline:** 5 days
**Risk Assessment:**
- **MEDIUM:** Reactor is core infrastructure, changes need careful testing
- **HIGH:** DAG execution is production-critical
- **MEDIUM:** Current CLI is functional but inconsistent

**Success Criteria:**
- Unified CLI entry point
- Commander.js framework adopted
- Shared utilities integrated
- All existing functionality preserved

---

## Phase 4: Shell Script Standardization (Weeks 7-8)

### 4.1 Audit and Standardize Critical Shell Scripts
**Objective:** Bring order to the 50+ shell scripts across repositories

**Focus Areas:**
- afi-research-site: Data processing pipelines (appropriations_qa_cli.sh, etc.)
- afi-econ: Pipeline demos and examples
- afi-ops: Deployment and health check scripts

**Deliverables:**
- Standardize script headers, error handling, and logging
- Create shared shell script utilities
- Document script purposes and usage
- Add basic testing for critical scripts

**Responsible:** DevOps Team + Repository Maintainers
**Timeline:** 1 week
**Risk Assessment:**
- **MEDIUM:** Many scripts are production-critical (data processing, deployment)
- **LOW:** Shell script standardization is well-established
- **HIGH:** Breaking changes could affect CI/CD pipelines

**Success Criteria:**
- Critical scripts follow standards
- Shared utilities available
- Documentation updated
- Basic testing in place

---

## Phase 5: Testing and Validation (Weeks 9-10)

### 5.1 Implement CLI Testing Framework
**Objective:** Ensure all CLIs have comprehensive testing

**Deliverables:**
- CLI testing utilities in shared framework
- Integration tests for all CLI commands
- Regression testing for CLI migrations
- Performance testing for CLI operations

**Responsible:** QA Team + CLI Framework Team
**Timeline:** 1 week
**Risk Assessment:**
- **LOW:** Testing frameworks are well-established
- **MEDIUM:** Requires coordination across all repositories

**Success Criteria:**
- All CLIs have test coverage
- CLI testing utilities available
- Regression tests prevent breaking changes

### 5.2 Update Documentation and Training
**Objective:** Ensure all teams understand new CLI standards

**Deliverables:**
- Updated contributor documentation
- CLI development training materials
- Migration guides for existing CLIs
- Best practices documentation

**Responsible:** Technical Writing Team
**Timeline:** 3 days
**Risk Assessment:**
- **LOW:** Purely documentation
- **LOW:** Can be done incrementally

**Success Criteria:**
- All repository READMEs updated
- Training materials available
- Migration guides comprehensive

---

## Phase 6: Monitoring and Maintenance (Ongoing)

### 6.1 Establish CLI Governance Process
**Objective:** Maintain CLI standards long-term

**Deliverables:**
- CLI review checklist for PRs
- Automated CLI linting in CI
- Regular CLI audit schedule (quarterly)
- CLI standards update process

**Responsible:** Architecture Team
**Timeline:** 3 days
**Risk Assessment:**
- **LOW:** Governance processes are standard
- **LOW:** Can be implemented incrementally

**Success Criteria:**
- CLI standards enforced in CI
- Regular audits scheduled
- Governance process documented

---

## Risk Mitigation Strategy

### High-Risk Areas
1. **afi-econ CLI Migration:** Production-critical, requires extensive testing
   - *Mitigation:* Phased rollout with feature flags, comprehensive testing
2. **afi-reactor CLI Changes:** Core infrastructure
   - *Mitigation:* Incremental changes, maintain backward compatibility
3. **Shell Script Standardization:** Affects CI/CD pipelines
   - *Mitigation:* Audit all script usage before changes, maintain compatibility

### Rollback Plan
- All changes versioned and documented
- Feature flags for new CLI implementations
- Ability to revert to previous CLI versions
- Comprehensive testing before production deployment

---

## Success Metrics

### Quantitative Metrics
- **CLI Framework Consistency:** 100% of CLIs use approved frameworks (Click, Commander.js)
- **Test Coverage:** 90%+ test coverage for all CLI commands
- **Documentation Coverage:** 100% of CLI commands documented
- **User Experience:** <5% CLI error rate in production

### Qualitative Metrics
- Developer feedback on CLI usability
- Time-to-implement new CLI commands (target: <2 hours)
- Cross-repository CLI consistency
- Maintenance burden reduction

---

## Resource Requirements

### Team Allocation
- **Core Team (2 FTE):** CLI framework development, standards definition
- **Repository Teams (4 FTE):** CLI migrations and implementations
- **QA Team (1 FTE):** Testing and validation
- **DevOps Team (1 FTE):** Shell script standardization
- **Technical Writing (0.5 FTE):** Documentation and training

### Timeline Summary
- **Phase 1 (Foundation):** Weeks 1-2
- **Phase 2 (Python):** Weeks 3-4
- **Phase 3 (Node.js):** Weeks 5-6
- **Phase 4 (Shell Scripts):** Weeks 7-8
- **Phase 5 (Testing):** Weeks 9-10
- **Phase 6 (Maintenance):** Ongoing

**Total Timeline:** 10 weeks
**Total Effort:** ~12 FTE-weeks

---

## Dependencies and Prerequisites

### External Dependencies
- Access to internal npm and PyPI registries for shared packages
- CI/CD pipeline updates for new testing requirements
- Repository maintainer approval for CLI changes

### Internal Dependencies
- Completion of current CLI audit (✅ Complete)
- Agreement on CLI standards document
- Availability of shared CLI framework packages

---

## Communication Plan

### Weekly Updates
- Progress reports to all repository maintainers
- Risk assessment updates
- Blocker identification and resolution

### Key Milestones
- **Week 2:** Shared CLI framework published
- **Week 4:** Python CLIs standardized
- **Week 6:** Node.js CLIs standardized
- **Week 8:** Shell scripts standardized
- **Week 10:** Full testing and documentation complete

### Stakeholder Engagement
- Repository maintainers: Weekly updates
- Development teams: Training sessions
- QA Team: Early involvement in testing strategy
- Product Team: User experience validation

---

*This plan represents a comprehensive approach to standardizing AFI's CLI ecosystem. Success will significantly improve developer experience, reduce maintenance overhead, and establish scalable patterns for future CLI development.*