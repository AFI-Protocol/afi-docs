# AFI Docs - Common Droid Tasks

Frequent tasks with step-by-step instructions.

---

## Task 1: Improve Existing Documentation

**When**: Documentation is unclear or incomplete.

**Steps**:

1. **Identify gap**:
   - Missing information?
   - Unclear explanation?
   - Outdated content?

2. **Make improvement**:
   ```markdown
   <!-- guides/getting-started.md -->
   ## Installation
   
   Install AFI CLI:
   \`\`\`bash
   npm install -g @afi-protocol/cli
   \`\`\`
   
   Verify installation:
   \`\`\`bash
   afi --version
   \`\`\`
   ```

3. **Verify accuracy**:
   - Test code examples
   - Check links
   - Ensure consistency

**Expected time**: 15-30 minutes

---

## Task 2: Add New Guide

**When**: You need to document a new feature or workflow.

**Steps**:

1. **Create guide file**:
   ```bash
   touch guides/my-new-guide.md
   ```

2. **Write guide**:
   ```markdown
   # My New Guide
   
   ## Overview
   Brief description of what this guide covers.
   
   ## Prerequisites
   - Requirement 1
   - Requirement 2
   
   ## Steps
   1. First step
   2. Second step
   
   ## Examples
   \`\`\`bash
   # Example command
   afi my-command
   \`\`\`
   
   ## Troubleshooting
   Common issues and solutions.
   ```

3. **Add to navigation**:
   ```json
   // SUMMARY.md or book.json
   {
     "guides": [
       "guides/my-new-guide.md"
     ]
   }
   ```

**Expected time**: 1-2 hours

---

## Task 3: Fix Typos and Clarity

**When**: You find typos or unclear language.

**Steps**:

1. **Fix typos**:
   ```markdown
   <!-- Before -->
   The AFI Protocol is a decentralised system for finanical intelligence.
   
   <!-- After -->
   The AFI Protocol is a decentralized system for financial intelligence.
   ```

2. **Improve clarity**:
   ```markdown
   <!-- Before -->
   Run the thing to do the stuff.
   
   <!-- After -->
   Run the validator to check signal quality:
   \`\`\`bash
   afi validate --signal-id <id>
   \`\`\`
   ```

**Expected time**: 5-15 minutes

---

## Task 4: Add Code Examples

**When**: Documentation lacks practical examples.

**Steps**:

1. **Add example**:
   ```markdown
   ## Example: Validating a Signal
   
   \`\`\`typescript
   import { SignalValidator } from '@afi-protocol/core';
   
   const validator = new SignalValidator();
   const signal = {
     id: '123',
     confidence: 0.8,
     data: { /* ... */ }
   };
   
   const isValid = validator.validate(signal);
   console.log('Signal is valid:', isValid);
   \`\`\`
   ```

2. **Test example**:
   - Ensure code runs
   - Verify output is correct

**Expected time**: 30-60 minutes

---

## Task 5: Update CLI Documentation

**When**: CLI commands have changed.

**Steps**:

1. **Generate help text**:
   ```bash
   afi --help > cli_help.md
   afi validate --help >> cli_help.md
   ```

2. **Add usage examples**:
   ```markdown
   <!-- cli_usage.md -->
   ## afi validate
   
   Validate a signal for quality and correctness.
   
   ### Usage
   \`\`\`bash
   afi validate --signal-id <id>
   \`\`\`
   
   ### Examples
   \`\`\`bash
   # Validate signal by ID
   afi validate --signal-id abc123
   
   # Validate with verbose output
   afi validate --signal-id abc123 --verbose
   \`\`\`
   ```

**Expected time**: 30-60 minutes

---

## Getting Help

If stuck on any task:
1. Check `AGENTS.md` for constraints
2. Look at existing docs for style
3. Test code examples
4. Ask human maintainer if unsure

---

**Last Updated**: 2025-11-22

