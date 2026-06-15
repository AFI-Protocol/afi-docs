# AFI Protocol Audit Workspace

Persistent handoff for the portable-protocol surface investigation. Phase 1 recon is extracted here so Claude agents can resume without re-auditing 31 repos.

**Start here:** [`AFI_AUDIT_CHECKPOINT.md`](./AFI_AUDIT_CHECKPOINT.md)  
**Resume agents with:** [`AFI_AUDIT_RESUME_PROMPT.md`](./AFI_AUDIT_RESUME_PROMPT.md)

---

## Layout

```
audit/
├── AFI_AUDIT_CHECKPOINT.md      # Phase status, DoD tracker, resume instructions
├── AFI_AUDIT_RESUME_PROMPT.md   # Copy-paste prompt for Phases 2–4
├── scripts/
│   ├── extract_recon.py         # jsonl → AFI_RECON_CORPUS.json
│   └── generate_drafts.py       # corpus → draft markdown reports
├── recon/
│   ├── AFI_RECON_CORPUS.json    # Machine-readable Phase 1 output (31 records)
│   ├── AFI_RECON_SUMMARY.md     # Human-readable Phase 1 summary
│   └── per-repo/                # One JSON file per repo
├── drafts/                      # Phase 1-derived, unverified
├── themes/                      # Phase 2 theme outputs (A–J)
└── final/                       # Optional staging before promotion to specs/
```

---

## Regenerating Phase 1 Artifacts

If you need to re-extract from Claude workflow logs:

```bash
cd afi-docs/specs/audit/scripts
python3 extract_recon.py
python3 generate_drafts.py
```

Default jsonl source: `~/.claude/projects/-home-user-AFI-Protocol/.../subagents/workflows/wf_854527ef-4aa/`

**Do not hand-edit** `recon/AFI_RECON_CORPUS.json` without re-running extraction or documenting the change in the checkpoint.

---

## Charter Documents

| Document | Role |
|----------|------|
| [`../AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md`](../AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md) | North star |
| [`../AFI_PROTOCOL_INVESTIGATION_PROMPT.md`](../AFI_PROTOCOL_INVESTIGATION_PROMPT.md) | Full investigation (all phases) |
| [`AFI_AUDIT_RESUME_PROMPT.md`](./AFI_AUDIT_RESUME_PROMPT.md) | Resume only (phases 2–4) |

---

## Final Deliverables (Phase 4)

Promoted to `afi-docs/specs/` when complete:

- `AFI_PROTOCOL_SURFACE_AUDIT.md`
- `AFI_NORMATIVE_REGISTER.md`
- `AFI_REFERENCE_IMPL_MAP.md`
- `AFI_CONTRADICTION_REGISTER.md`
- `AFI_REPLAY_READINESS_MATRIX.md`
- `AFI_ONCHAIN_ANCHOR_GAP_ANALYSIS.md`
