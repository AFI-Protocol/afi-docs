# AFI Protocol Audit Workspace

Persistent handoff for the portable-protocol surface investigation across the 31-repo workspace.

**Status: COMPLETE.** All four phases are done — Phase 1 recon, Phase 2 themes (A–J), Phase 3 adversarial verification (`themes/verified.json`, 33/33 P0/P1 confirmed), and Phase 4 synthesis (6 master reports written, validated, and promoted to `afi-docs/specs/`). The deterministic gate `scripts/validate_audit.py all` reports `RESULT: PASS`.

**Org delta (2026-06-20):** Three repos were **permanently deleted** from GitHub: `afi-cli-shared`, `afi-agents`, `afi-construct`. The live org is **28 `afi-*` repos** (+ `.github`, `afi-xerc20`). Phase 4 classification reports below still reflect the **31-repo audit snapshot** (June 2026) — treat deleted repos as historical catalog entries, not operational dependencies. Operational docs (`AFI_Repository_Map.md`, governance READMEs) were scrubbed; forensic corpus (`recon/`, `themes/*.json`) was intentionally left intact.

**Start here:** [`AFI_AUDIT_CHECKPOINT.md`](./AFI_AUDIT_CHECKPOINT.md) (phase status + Definition-of-Done tracker)  
**Human review:** [`AFI_HUMAN_REVIEW_WORKSHEET.md`](./AFI_HUMAN_REVIEW_WORKSHEET.md) (Q1–Q7 decisions with file links)  
**Testnet E2E:** [`AFI_TESTNET_E2E_CHECKLIST.md`](./AFI_TESTNET_E2E_CHECKLIST.md) (MVP vs protocol-complete, Base Sepolia)  
**Mage + GCP research:** [`AFI_MAGE_GCP_RESEARCH_PROMPT.md`](./AFI_MAGE_GCP_RESEARCH_PROMPT.md) (deep agent charter)  
**Mage Pro plan pick:** [`AFI_MAGE_PRO_PLAN_DECISION.md`](./AFI_MAGE_PRO_PLAN_DECISION.md) (OSS default; Pro fallback)  
**Froggy → Mage map:** [`AFI_FROGGY_MAGE_MIGRATION_MAP.md`](./AFI_FROGGY_MAGE_MIGRATION_MAP.md) (stage-by-stage reuse)  
**Legacy purge prompt:** [`AFI_LEGACY_PIPELINE_PURGE_PROMPT.md`](./AFI_LEGACY_PIPELINE_PURGE_PROMPT.md) (remove alpha-scout / structurer / validator-decision / execution-sim)  
**afi-core build fix:** [`AFI_CORE_BUILD_FIX_PROMPT.md`](./AFI_CORE_BUILD_FIX_PROMPT.md) (P0 — unblock npm install)  
**Analyst Shop MVP:** [`../AFI_ANALYST_SHOP_MVP.md`](../AFI_ANALYST_SHOP_MVP.md) (onboarding tiers, Ably as optional storefront)  
**Final reports:** see [Final Deliverables](#final-deliverables-phase-4) below.

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
├── drafts/                      # Phase 1-derived, unverified (inputs to verification)
├── themes/                      # Phase 2 theme outputs (A–J) + verified.json (Phase 3)
└── final/                       # Phase 4 staging; promoted verbatim to ../ (specs/)
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

All six reports are complete and promoted to `afi-docs/specs/` (byte-identical to the `final/` staging copies). Each carries `file:line` evidence, verified status from `themes/verified.json`, a backlink to the North Star, and cross-links to its five siblings.

| Report (in `../`) | Scope |
|-------------------|-------|
| [`AFI_PROTOCOL_SURFACE_AUDIT.md`](../AFI_PROTOCOL_SURFACE_AUDIT.md) | Master audit: 5-plane alignment scorecard, top-10 blockers/quick-wins, 31-repo classification, findings by severity, solidification roadmap |
| [`AFI_NORMATIVE_REGISTER.md`](../AFI_NORMATIVE_REGISTER.md) | Every normative schema/invariant/contract + stated-but-unenforced invariants |
| [`AFI_REFERENCE_IMPL_MAP.md`](../AFI_REFERENCE_IMPL_MAP.md) | 31-repo classification + reference spine (ingest→DAG→vault→mint→on-chain) |
| [`AFI_CONTRADICTION_REGISTER.md`](../AFI_CONTRADICTION_REGISTER.md) | All six tensions with verified-status entries |
| [`AFI_REPLAY_READINESS_MATRIX.md`](../AFI_REPLAY_READINESS_MATRIX.md) | Per-stage RAW→…→REPLAYED storage + replayability |
| [`AFI_ONCHAIN_ANCHOR_GAP_ANALYSIS.md`](../AFI_ONCHAIN_ANCHOR_GAP_ANALYSIS.md) | On-chain events/structs/fields/roles vs intended commitment anchor |

### Validation

```bash
cd afi-docs/specs/audit/scripts && python3 validate_audit.py all   # RESULT: PASS
```
