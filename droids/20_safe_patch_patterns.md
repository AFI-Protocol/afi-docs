# AFI Docs - Safe Patch Patterns

How to make safe, reviewable documentation changes.

---

## Pattern 1: Additive Documentation

**Good** ✅:
```markdown
<!-- Add new section without changing existing content -->
## New Feature: Signal Validation

This section documents the new signal validation feature.
```

**Bad** ❌:
```markdown
<!-- Rewriting existing section without approval -->
## Signal Processing (COMPLETELY REWRITTEN)
```

**Why**: Additive changes are easier to review and revert.

---

## Pattern 2: Test Code Examples

**Good** ✅:
```markdown
## Example: Create Signal

\`\`\`typescript
// Tested and verified to work
const signal = createSignal({ id: '123' });
\`\`\`
```

**Bad** ❌:
```markdown
## Example: Create Signal

\`\`\`typescript
// Untested code that might not work
const signal = createSignal();  // Missing required parameter!
\`\`\`
```

**Why**: Broken examples frustrate users.

---

## Pattern 3: Maintain Consistent Style

**Good** ✅:
```markdown
<!-- Follow existing style -->
## Installation

Install the CLI:
\`\`\`bash
npm install -g @afi-protocol/cli
\`\`\`
```

**Bad** ❌:
```markdown
<!-- Inconsistent style -->
# installation

install the cli:
npm install -g @afi-protocol/cli
```

**Why**: Consistency improves readability.

---

## Pattern 4: Link to Related Docs

**Good** ✅:
```markdown
## Signal Validation

For more information on signals, see [Signal Specification](specs/signal-spec.md).

For validation examples, see [Validation Guide](guides/validation.md).
```

**Why**: Links help users find related information.

---

## Pattern 5: Document Breaking Changes

**Good** ✅:
```markdown
## Migration Guide: v2.0.0

### Breaking Changes

1. `createSignal()` now requires `id` parameter
   - **Before**: `createSignal()`
   - **After**: `createSignal({ id: '123' })`

2. `validate()` returns object instead of boolean
   - **Before**: `const isValid = validate(signal);`
   - **After**: `const { valid, errors } = validate(signal);`
```

**Why**: Migration guides help users upgrade.

---

## Pattern 6: Use Clear Headings

**Good** ✅:
```markdown
## How to Validate a Signal

### Prerequisites
- AFI CLI installed
- Signal ID

### Steps
1. Run validation command
2. Check output
```

**Bad** ❌:
```markdown
## Validation

Some stuff about validation...
```

**Why**: Clear headings improve navigation.

---

## Pattern 7: Include Troubleshooting

**Good** ✅:
```markdown
## Troubleshooting

### Error: "Signal not found"

**Cause**: Signal ID does not exist in database.

**Solution**: Verify signal ID with `afi list-signals`.
```

**Why**: Troubleshooting helps users solve problems.

---

## Checklist Before Submitting

- [ ] Changes are additive (no deletions unless necessary)
- [ ] Code examples tested and working
- [ ] Consistent style with existing docs
- [ ] Links to related documentation
- [ ] Breaking changes documented
- [ ] Clear headings and structure
- [ ] Troubleshooting included (if applicable)

---

**Last Updated**: 2025-11-22

