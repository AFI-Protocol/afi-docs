# AGENTS.md — AFI Docs Droid Instructions (v1)

This file is the canonical instruction set for Factory.ai droids and other agents working in this repository.
If AGENTS.md conflicts with README or docs, **AGENTS.md wins.**

---

## 0. Repo Purpose

**What this repo is for:**  
Documentation, contributor guides, specifications, and lore for AFI Protocol. Provides onboarding materials, technical specs, and narrative context for contributors and users.

**What this repo is NOT for:**  
- Code implementation (use afi-core, afi-reactor, etc.)
- Deployment scripts (use afi-infra)
- Infrastructure (use afi-infra)

---

## 1. Prime Directives (Global AFI Rules)

- **Scaffold, wire, and align context only.** Do not expand full feature logic unless explicitly instructed.
- **Keep changes minimal and deterministic.**
- **Preserve modular boundaries.** No cross-repo code moves unless asked.
- **Codex + AOS are truth sources.** Whitepaper is narrative, not canonical.
- **Never delete or overwrite without a replacement plan.**
- **Prefer small patches over large refactors.**

---

## 2. Allowed Tasks

Droids MAY:
- Add or improve guides in `guides/`
- Add or improve specs in `specs/`
- Add lore and narrative in `lore/`
- Fix typos and grammar errors
- Improve clarity and reduce ambiguity
- Add diagrams and visualizations
- Update contributor guides
- Add CLI usage examples in `cli_help.md` and `cli_usage.md`
- Improve droid contributor guide in `droid_contributor_guide.md`

---

## 3. Forbidden Tasks

Droids MUST NOT:
- Change canonical specifications without approval
- Modify core protocol concepts without coordination
- Add contradictory information
- Remove historical documentation without archiving
- Change terminology that's used across repos
- Add speculative features as if they're implemented

---

## 4. Key Invariants

These must remain true after changes:
- Specs remain consistent with code implementation
- Terminology is consistent across all docs
- Guides are beginner-friendly and clear
- No contradictions between docs
- All code examples are tested and working
- Links to other repos remain valid

---

## 5. Repo Layout Map

- `guides/` — How-to guides and tutorials
- `specs/` — Technical specifications
- `lore/` — Narrative and background context
- `cli_help.md` — CLI command reference
- `cli_usage.md` — CLI usage examples
- `droid_contributor_guide.md` — Guide for AI agents
- `SUMMARY.md` — Documentation index
- `CONTRIBUTING.md` — Contribution guidelines
- `afi.config.json` — Documentation config

---

## 6. Codex / AOS Touchpoints

- `afi.config.json` location: Root of repo
- AOS streams / registries referenced:
  - Documentation registry
  - Specification registry
- Schema contracts this repo must obey:
  - Documentation structure schema
  - Specification format schema

---

## 7. Safe Patch Patterns

When editing, prefer:
- Small diffs, one intent per commit/patch
- Additive changes over rewrites
- Clear section headings and structure
- Examples that are tested and working
- Links to source code for reference

Example safe patch:
```markdown
<!-- TODO(droid): Add guide for setting up local development -->
## Local Development Setup

This guide walks you through setting up AFI Protocol for local development.

### Prerequisites
- Node.js 20+
- pnpm 8+
- Git

### Steps
1. Clone the repository
2. Install dependencies: `pnpm install`
3. Run tests: `pnpm test`

<!-- Stub: Add detailed steps for each repo -->
```

---

## 8. How to Validate Locally

**Note**: This repo currently has no automated test suite. Validation is manual.

Run these before finalizing:
```bash
# Check for broken links (if tool available)
# markdown-link-check **/*.md

# Check markdown syntax (if tool available)
# markdownlint **/*.md

# Manual validation:
# - Read through changes
# - Verify links work
# - Check code examples are accurate
# - Ensure clarity and consistency
# - Test any code snippets
```

Expected outcomes:
- No broken links
- Markdown syntax is valid
- Code examples are correct and tested

**Validation currently manual; CI pending; do not add logic until tests exist.**
- Terminology is consistent

---

## 9. CI / PR Expectations

- Any new guide must include clear examples
- Any spec change must coordinate with code repos
- PR description must explain what was improved and why
- Documentation should reduce ambiguity for readers

---

## 10. Current Priorities

1. Improve droid contributor guide
2. Add comprehensive CLI documentation
3. Document all protocol specifications
4. Add architecture diagrams
5. Create onboarding tutorials

---

## 11. If You're Unsure

Default to:
1. Do nothing risky
2. Add a TODO comment
3. Document the uncertainty
4. Ask a human maintainer (tag @afi-docs-team in PR)

---

**Last Updated**: 2025-11-22  
**Maintainers**: AFI Docs Team  
**Version**: 1.0.0

