# AFI CLI Standards and Governance

## Introduction

This document establishes comprehensive guidelines for developing, maintaining, and governing Command Line Interface (CLI) tools across all AFI project repositories. The goal is to ensure consistency, maintainability, and high quality across all CLI tools while leveraging shared frameworks and best practices.

**Effective Date:** Immediate upon approval  
**Review Cycle:** Quarterly  
**Responsible Party:** AFI CLI Governance Committee  

## 1. Framework Standards

All new CLI tools must use the designated shared frameworks. Existing CLIs must migrate to these frameworks within 3 months of this document's approval.

### Node.js CLIs
- **Framework:** `@afi/cli-framework` (built on Commander.js)
- **Usage:** Extend `CliApp` class for base functionality
- **Example:** See [`CliApp.ts`](afi-cli-framework/src/base/CliApp.ts:17) for base implementation

### Python CLIs
- **Framework:** `afi-cli-shared` (built on Click)
- **Usage:** Extend `BaseCli` class for base functionality
- **Example:** See [`base.py`](afi-cli-shared/src/afi_cli_shared/base.py:9) for base implementation

### Prohibited Frameworks
- No new CLIs using `argparse`, `yargs`, `custom` frameworks, or direct Commander.js/Click usage
- Existing non-compliant CLIs (e.g., `afi-benchkit` using direct Click) must migrate

**Responsibilities:**
- CLI Developers: Use designated frameworks for new tools
- Repository Maintainers: Ensure migration of existing CLIs
- Timeline: Complete migration within 3 months

## 2. CLI Design Standards

### Command Naming Conventions
- **Commands:** kebab-case (e.g., `submit-proposal`, `run-suite`)
- **Subcommands:** kebab-case, hierarchical (e.g., `config set`, `config get`)
- **Options:** camelCase (e.g., `--dryRun`, `--verboseLevel`)

### Standard Arguments
All CLIs must support these standard options:
- `--config <path>`: Path to config file (default: `.afi-cli.json`)
- `--verbose`: Enable verbose logging
- `--dry-run`: Preview actions without execution
- `--help`: Display help (automatic via frameworks)
- `--version`: Display version (automatic via frameworks)

### Help Text and Error Messages
- **Help Format:** Consistent structure with description, usage, options
- **Error Messages:** Prefix with "Error:", use consistent terminology
- **Exit Codes:**
  - 0: Success
  - 1: General error
  - 2: Invalid usage/command not found
  - 3: Configuration error

**Examples:**
- Compliant: `afi-benchkit run --suite poi --dataset data.json` (from [`cli.py`](afi-benchkit/src/afi_benchkit/cli.py:18))
- Non-compliant: Custom error handling in existing CLIs should standardize to framework patterns

**Responsibilities:**
- CLI Developers: Implement standard options and exit codes
- Timeline: Immediate for new CLIs, 1 month for existing

## 3. Development Standards

### Code Structure
```
cli/
├── src/
│   ├── commands/     # Command implementations
│   ├── utils/        # Shared utilities
│   └── index.ts      # Main entry point
├── tests/
│   ├── unit/         # Unit tests
│   ├── integration/  # Integration tests
│   └── cli/          # CLI smoke tests
├── docs/
│   ├── README.md     # Usage documentation
│   └── api.md        # API documentation
└── package.json/pyproject.toml
```

### Testing Requirements
- **Unit Tests:** Cover all functions and classes (90%+ coverage)
- **Integration Tests:** End-to-end command execution
- **CLI Smoke Tests:** Basic command validation
- **Test Frameworks:** Jest (Node.js), pytest (Python)

### Documentation Requirements
- **README:** Installation, usage examples, configuration
- **API Docs:** Generated from code comments (TypeDoc/Sphinx)
- **Changelog:** Semantic versioning with change descriptions

### Versioning and Changelog
- **Versioning:** Semantic versioning (MAJOR.MINOR.PATCH)
- **Changelog:** Keep CHANGELOG.md with categorized changes
- **Releases:** Tag releases in git with changelog updates

**Examples:**
- Framework documentation: [`README.md`](afi-cli-framework/README.md)
- Testing structure: Follow framework examples

**Responsibilities:**
- CLI Developers: Maintain 90% test coverage
- Repository Maintainers: Enforce documentation standards
- Timeline: Achieve compliance within 2 months

## 4. Governance Process

### CLI Review Process
1. **Proposal:** Submit CLI proposal via AFI governance system
2. **Technical Review:** CLI Governance Committee reviews design
3. **Implementation:** Develop using standards
4. **Security Review:** Security team audit
5. **Approval:** Tech lead final approval

### Maintenance Responsibilities
- **Primary Maintainers:** Assigned per CLI (rotate annually)
- **Backup Maintainers:** At least one per CLI
- **Support:** Respond to issues within 24 hours

### Deprecation and Migration
- **Deprecation Notice:** 6 months advance notice
- **Migration Path:** Provide migration guides
- **Sunset:** Remove deprecated CLIs after 12 months

### Weekly Status Meetings
- **Frequency:** Weekly on Wednesdays
- **Attendees:** CLI maintainers, governance committee
- **Agenda:** Status updates, blockers, new proposals
- **Duration:** 30 minutes

### Stakeholder Approval Requirements
- **New CLIs:** Require tech lead approval
- **Major Changes:** Require governance committee approval
- **Security Impact:** Require security team review

**Responsibilities:**
- Governance Committee: Conduct reviews and meetings
- Maintainers: Attend meetings and maintain CLIs
- Timeline: Establish committee within 1 week

## 5. Migration Guidelines

### Process for Migrating Existing CLIs
1. **Assessment:** Evaluate current CLI against standards
2. **Planning:** Create migration plan with timeline
3. **Implementation:** Refactor to use shared frameworks
4. **Testing:** Full test suite including backward compatibility
5. **Deployment:** Rollout with feature flags
6. **Sunset:** Remove old implementation

### Backward Compatibility Requirements
- **API Compatibility:** Maintain existing command interfaces
- **Config Compatibility:** Support old config formats
- **Duration:** 1 major version cycle minimum

### Feature Flags During Transitions
- **Implementation:** Use framework extension system for flags
- **Duration:** Enable flags for 2 releases
- **Removal:** Remove after full migration

### Rollback Procedures
- **Version Rollback:** Ability to revert to previous version
- **Data Migration:** Scripts to restore old configurations
- **Documentation:** Rollback procedures in README

**Examples:**
- Migrate `afi-benchkit` from direct Click to `afi-cli-shared`
- Maintain `--suite` and `--dataset` options during transition

**Responsibilities:**
- Repository Maintainers: Plan and execute migrations
- Timeline: Complete all migrations within 3 months

## 6. Quality Assurance

### Test Coverage Requirements
- **Minimum Coverage:** 90% for all CLIs
- **Measurement:** Line and branch coverage
- **Reporting:** Include in CI/CD pipelines

### Performance Benchmarks
- **Startup Time:** < 500ms for basic commands
- **Memory Usage:** < 100MB baseline
- **Benchmarks:** Include performance tests in CI

### Security Considerations
- **Input Validation:** Validate all user inputs
- **Secrets Management:** No hardcoded secrets
- **Dependency Scanning:** Regular security audits
- **Logging:** No sensitive data in logs

### Accessibility Standards
- **Screen Readers:** Compatible with screen readers
- **Keyboard Navigation:** Full keyboard support
- **Color Independence:** No color-only indicators
- **Help Text:** Clear, descriptive help messages

**Responsibilities:**
- CLI Developers: Maintain quality standards
- Security Team: Conduct regular audits
- Timeline: Achieve 90% coverage within 2 months

## Conclusion

These standards ensure AFI CLIs are consistent, maintainable, and high-quality. Implementation will be tracked through the governance process with regular reviews and updates.

**Next Steps:**
1. Form CLI Governance Committee (within 1 week)
2. Audit existing CLIs for compliance (within 2 weeks)
3. Begin migration of non-compliant CLIs (within 1 month)
4. Establish weekly status meetings (immediate)

For questions or clarifications, contact the CLI Governance Committee.