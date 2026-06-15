# Theme Outputs (Phase 2)

Write one file per theme after completing cross-repo deep-dives. Run themes **sequentially** (see [`AFI_AUDIT_RESUME_PROMPT.md`](../AFI_AUDIT_RESUME_PROMPT.md)).

## Expected Files

| Key | Filename | Status |
|-----|----------|--------|
| A | `A-normative-surface.json` | Pending |
| B | `B-reference-impl.json` | Pending |
| C | `C-onchain-anchor.json` | Pending |
| D | `D-evidence-vault.json` | Pending |
| E | `E-scoring-dag.json` | Pending |
| F | `F-analytics.json` | Pending |
| G | `G-emissions-mint.json` | Pending |
| H | `H-governance.json` | Pending |
| I | `I-sdks-gateway.json` | Pending |
| J | `J-docs-drift.json` | Pending |

## Phase 3 Output

| File | Description |
|------|-------------|
| `verified.json` | Adversarial verification of P0/P1 claims |

## JSON Schema (informal)

Each theme file should include:

- `theme` — key string
- `summary` — narrative answer
- `answers[]` — `{question, answer, evidence}`
- `findings[]` — `{title, severity, theme, evidence, recommendation}`
- `contradictions[]` — `{doc_says, code_does, evidence, severity, tension}`

## Priority Order

1. C → 2. D → 3. G → 4. B → 5. A → 6. E → 7. J → 8. I → 9. H → 10. F
