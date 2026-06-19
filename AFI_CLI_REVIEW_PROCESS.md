# AFI CLI Review Process

> **Status: RETIRED (2026-06-19)** — Aspirational only; not an active mandate. See [`specs/audit/AFI_CLI_FRAMEWORKS_DECISIONS.md`](./specs/audit/AFI_CLI_FRAMEWORKS_DECISIONS.md).

## Overview

This document defines the review and approval processes for CLI proposals, changes, and maintenance activities. It ensures quality, security, and compliance while maintaining efficient development workflows.

## CLI Proposal Review Process

### Phase 1: Proposal Submission
- **Submitter:** CLI developer or repository maintainer
- **Format:** Standard proposal template in AFI governance system
- **Required Information:**
  - Business justification and use cases
  - Technical design and framework compliance
  - Security and privacy considerations
  - Timeline and resource requirements
  - Migration plan for existing tools (if applicable)
- **Timeline:** 1-2 weeks for initial review

### Phase 2: Technical Review
- **Reviewer:** CLI Governance Committee
- **Criteria:**
  - Compliance with CLI standards and frameworks
  - Code quality and maintainability
  - Performance and scalability
  - Integration with existing systems
- **Deliverables:** Technical review report with recommendations
- **Timeline:** 1 week

### Phase 3: Security Review
- **Reviewer:** AFI Security Team
- **Focus Areas:**
  - Input validation and sanitization
  - Authentication and authorization
  - Data protection and privacy
  - Dependency security
  - Logging and monitoring
- **Timeline:** 1 week for standard reviews, 2 weeks for complex tools

### Phase 4: Stakeholder Approval
- **Approvers:** Tech lead, product owner, governance committee
- **Criteria:** Business value, resource availability, strategic alignment
- **Timeline:** 3-5 business days

### Phase 5: Implementation and Testing
- **Development:** Using approved frameworks and standards
- **Testing:** Full test suite including security and performance
- **Documentation:** Complete README and API docs
- **Timeline:** As specified in proposal

## Approval Workflows

### New CLI Tools
1. **Pre-submission:** Consult with governance committee
2. **Submission:** Formal proposal via governance system
3. **Review Cycle:** Technical → Security → Stakeholder
4. **Approval:** Committee consensus or majority vote
5. **Implementation:** Start after approval

### Major Changes to Existing CLIs
1. **Impact Assessment:** Evaluate scope and risk
2. **Proposal:** If significant impact, full review process
3. **Fast-track:** Minor changes with maintainer approval
4. **Testing:** Regression testing required
5. **Deployment:** Phased rollout with rollback plan

### Framework Updates
1. **Compatibility Check:** Test against all dependent CLIs
2. **Security Review:** Assess vulnerability implications
3. **Committee Approval:** Required for major versions
4. **Migration Plan:** Provided for breaking changes
5. **Rollout:** Coordinated across repositories

### Emergency Changes
1. **Justification:** Critical security or functionality issue
2. **Fast-track Approval:** Security lead + committee chair
3. **Post-review:** Full review within 1 week
4. **Documentation:** Incident report and lessons learned

## Escalation Procedures

### Level 1: Team Resolution
- **Scope:** Routine disagreements or minor issues
- **Process:** Discussion between submitter and reviewer
- **Timeline:** 2-3 business days
- **Escalation:** If unresolved, move to Level 2

### Level 2: Committee Mediation
- **Scope:** Technical disagreements, resource conflicts
- **Process:** Committee meeting with all parties
- **Decision:** Committee consensus or vote
- **Timeline:** 1 week
- **Escalation:** If blocking, move to Level 3

### Level 3: Leadership Review
- **Scope:** Strategic conflicts, major policy issues
- **Process:** AFI Tech Leadership review
- **Decision:** Final authority
- **Timeline:** 2 weeks
- **Communication:** All parties notified of decision

### Emergency Escalation
- **Trigger:** Security incidents or system outages
- **Process:** Immediate notification to security lead
- **Authority:** Security team can implement temporary fixes
- **Review:** Post-incident review within 24 hours

## Process Implementation

### Review Queues
- **Submission Queue:** GitHub Issues or JIRA board
- **Review Pipeline:** Automated assignment based on type
- **Priority Levels:** Critical, High, Medium, Low
- **SLA Tracking:** Automated reminders and escalations

### Approval Workflows
- **Digital Tools:** GitHub Actions for automated checks
- **Manual Gates:** Committee reviews for complex decisions
- **Audit Trail:** All decisions logged with rationale
- **Templates:** Standardized forms for consistent submissions

### Tracking Systems
- **Project Management:** JIRA for issue tracking
- **Metrics Dashboard:** Real-time status of all reviews
- **Reporting:** Weekly status reports to stakeholders
- **Archival:** All documents stored in central repository

### Quality Gates
- **Automated:** Code quality, security scans, test coverage
- **Manual:** Design reviews, security assessments
- **Integration:** CI/CD pipeline with approval gates
- **Metrics:** Track approval times and success rates

## Timeline and SLAs

### Standard Reviews
- **New CLI:** 4-6 weeks total
- **Major Changes:** 2-4 weeks
- **Minor Changes:** 1-2 weeks
- **Framework Updates:** 2-3 weeks

### Escalation Timelines
- **Level 1:** 3 days
- **Level 2:** 1 week
- **Level 3:** 2 weeks

### Monitoring
- **SLA Compliance:** > 90% on-time completion
- **Quality Metrics:** < 5% rework rate
- **Stakeholder Satisfaction:** > 4.0/5.0 rating

## Training and Support

### Process Training
- **New Members:** Orientation session on review processes
- **Annual Refresh:** Updates on process changes
- **Documentation:** Online guides and checklists

### Support Resources
- **Help Desk:** Dedicated channel for process questions
- **Templates:** Pre-filled forms and examples
- **Mentorship:** Experienced reviewers guide new submitters

**Effective Date:** [Date of approval]  
**Review Date:** Quarterly  
**Responsible Party:** AFI CLI Governance Committee