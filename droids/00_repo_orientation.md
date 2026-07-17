# AFI Docs - Droid Repo Orientation

**Quick Start**: You're in `afi-docs`, the official documentation hub for AFI Protocol.

---

## What This Repo Does

Official documentation for AFI Protocol including protocol specs, developer guides, governance blueprints, and Signal-Lore narrative series.

**Key Capabilities**:
- Protocol specifications
- Developer and operator guides
- Governance documentation
- Signal-Lore narratives

---

## Repo Boundaries

**This repo handles**:
- ✅ Documentation
- ✅ Guides and tutorials
- ✅ Specifications
- ✅ Narrative content (Signal-Lore)

**This repo does NOT handle**:
- ❌ Application code (that's afi-core, afi-reactor)
- ❌ Infrastructure (that's afi-infra)
- ❌ Deployment (that's afi-infra)

---

## Key Files to Know

```
specs/
  [Formal specifications]
  
guides/
  [Developer and operator guides]
  
lore/
  [Signal-Lore narratives]
  
cli_help.md
  [CLI documentation]
  
cli_usage.md
  [CLI usage examples]
```

---

## Quick Commands

```bash
# Install dependencies (if using GitBook)
npm install -g gitbook-cli

# Serve docs locally
gitbook serve

# Build docs
gitbook build
```

---

## Common Droid Tasks

See `10_common_tasks.md` for detailed workflows.

**Most frequent**:
1. Improve existing documentation
2. Add new guide
3. Fix typos and clarity
4. Add code examples

---

## Safety Notes

**Before making changes**:
1. Read `AGENTS.md` for constraints
2. Don't change canonical specs without approval
3. Ensure technical accuracy
4. Maintain consistent style

**Red flags** (ask a human):
- Changing protocol specifications
- Modifying governance rules
- Adding breaking changes to APIs

---

## Getting Help

- **AGENTS.md**: Canonical constraints
- **README.md**: High-level overview
- **Human maintainers**: Tag @afi-docs-team in PR

---

**Last Updated**: 2025-11-22

