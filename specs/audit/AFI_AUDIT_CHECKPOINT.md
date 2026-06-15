# AFI Protocol Audit Checkpoint

**Status:** Phases 1–4 complete — audit synthesized and promoted  
**Last updated:** 2026-06-15  
**Source workflow:** `wf_854527ef-4aa` (Claude agent workflow, interrupted by API rate limits)

Read this document first when resuming the portable-protocol audit.

---

## Investigation Status

| Phase | Description | Status | Output |
|-------|-------------|--------|--------|
| **1 — Recon** | 31 per-repo structured audits | **Complete** | [`recon/AFI_RECON_CORPUS.json`](./recon/AFI_RECON_CORPUS.json) |
| **2 — Themes** | 10 cross-cutting deep-dives (A–J) | **Complete** | [`themes/`](./themes/) (A–J, 10 files) |
| **3 — Verify** | Adversarial P0/P1 verification | **Complete** | [`themes/verified.json`](./themes/verified.json) (33/33 P0/P1) |
| **4 — Synthesize** | 6 master reports | **Complete** | [`final/`](./final/) staged + promoted to [`../`](../) root specs |

**Overall progress:** 100% (recon → themes → verify → synthesize → promote complete)

---

## Source Provenance

| Field | Value |
|-------|-------|
| Workflow ID | `wf_854527ef-4aa` |
| Workflow script | `.claude/projects/.../workflows/scripts/afi-protocol-surface-audit-wf_854527ef-4aa.js` |
| Recon agents | 31/31 completed |
| Theme agents | 0/10 (all failed: API rate limit) |
| Synthesis agents | 0/6 (all failed: API rate limit) |
| Approx. recon tokens | ~2.8M |
| Failure mode | Parallel burst: 10 theme agents + 6 writers launched simultaneously after recon |

Ephemeral source logs (for re-extraction only):

`~/.claude/projects/-home-user-AFI-Protocol/2bcd228c-6aed-4cda-87d6-883d0a0fcfbd/subagents/workflows/wf_854527ef-4aa/agent-*.jsonl`

Re-extract with: `python3 scripts/extract_recon.py`

---

## Classification Snapshot (Phase 1)

| Classification | Count | Repos |
|----------------|-------|-------|
| NORMATIVE | 2 | `afi-config`, `afi-infra` |
| REFERENCE_IMPL | 8 | `afi-gateway`, `afi-mint`, `afi-governance`, `afi-reactor`, `afi-core`, `afi-plugins`, `afi-token`, `afi-tiny-brains` |
| SUPPORTING | 11 | `afi-math`, `afi-starters`, `afi-skills`, `afi-benchkit`, `afi-factory`, `afi-artifacts`, `afi-ops`, `afi-cli-shared`, `afi-cli-framework`, `afi-assets`, `.github` |
| RESEARCH | 2 | `afi-econ`, `afi-labs` |
| DOCS | 2 | `afi-protocol`, `afi-docs` |
| STALE | 4 | `afi-sdk-python`, `afi-sdk-ts`, `afi-construct`, `afi-agents` |
| OUT_OF_SCOPE | 2 | `afi-xerc20`, `afi-research-site` |

**Replay-critical:** `afi-config`, `afi-infra`, `afi-reactor`  
**Portable-protocol alignment (qualitative):** partial / fragmented

Human summary: [`recon/AFI_RECON_SUMMARY.md`](./recon/AFI_RECON_SUMMARY.md)

---

## Phase 1 Draft Artifacts (Unverified)

| Artifact | Path | Notes |
|----------|------|-------|
| Recon corpus (machine) | [`recon/AFI_RECON_CORPUS.json`](./recon/AFI_RECON_CORPUS.json) | 31 records + metadata |
| Per-repo JSON | [`recon/per-repo/`](./recon/per-repo/) | One file per repo |
| Reference impl map | [`drafts/AFI_REFERENCE_IMPL_MAP.draft.md`](./drafts/AFI_REFERENCE_IMPL_MAP.draft.md) | 103 contradictions aggregated elsewhere |
| Contradiction register | [`drafts/AFI_CONTRADICTION_REGISTER.draft.md`](./drafts/AFI_CONTRADICTION_REGISTER.draft.md) | All six tension tags covered |

---

## Key Unverified Hypotheses (P1 — verify in Phase 3)

1. **Mongo tunnel vision** — `afi-infra`, `afi-reactor`, `afi-gateway` treat Mongo TSSD as production vault; multi-engine schema not implemented.
2. **Reactor as protocol law** — `afi-reactor` doctrine/README present orchestrator as mandatory, not reference-only.
3. **Weak ingest validation** — `afi-gateway` minimal field checks, not full USS/CPJ schema validation.
4. **No commitment-plane schema** — `afi-config` lacks normative on-chain anchor / mint receipt schema.
5. **Econ vs production mint** — `afi-econ` split models vs single `beneficiary` on-chain path.
6. **SDK stubs** — `afi-sdk-ts` / `afi-sdk-python` have no real public protocol API.
7. **CI validation gap** — `afi-config` schema validation script name mismatch (gate may be no-op).

Full list: [`drafts/AFI_CONTRADICTION_REGISTER.draft.md`](./drafts/AFI_CONTRADICTION_REGISTER.draft.md)

---

## Definition of Done Tracker

From [`AFI_PROTOCOL_INVESTIGATION_PROMPT.md`](../AFI_PROTOCOL_INVESTIGATION_PROMPT.md):

- [x] All org repos enumerated (31: 29 local + 2 archived)
- [x] Every repo has a classification row (in recon corpus)
- [x] All six master reports exist with cross-links (promoted to `afi-docs/specs/`, gate PASS)
- [x] Contradiction register has ≥1 entry per major tension (all six tensions, verified status from `verified.json`)
- [x] Replay readiness matrix covers all six lifecycle stages (RAW→ENRICHED→ANALYZED→SCORED→MINTED→REPLAYED)
- [x] On-chain anchor gap analysis cites every relevant Solidity event/field (`afi-token/src/*.sol`)
- [x] Solidification roadmap approved-ready for human review (master report Phases 0–4)
- [x] Theme answers A1–J33 completed (10 theme files A–J)
- [x] P0/P1 claims adversarially verified (`themes/verified.json`, 33/33 covered)

### Master reports (Phase 4 targets)

| Report | Status | Target path |
|--------|--------|-------------|
| `AFI_PROTOCOL_SURFACE_AUDIT.md` | Promoted | `afi-docs/specs/` |
| `AFI_NORMATIVE_REGISTER.md` | Promoted | `afi-docs/specs/` |
| `AFI_REFERENCE_IMPL_MAP.md` | Promoted | `afi-docs/specs/` |
| `AFI_CONTRADICTION_REGISTER.md` | Promoted | `afi-docs/specs/` |
| `AFI_REPLAY_READINESS_MATRIX.md` | Promoted | `afi-docs/specs/` |
| `AFI_ONCHAIN_ANCHOR_GAP_ANALYSIS.md` | Promoted | `afi-docs/specs/` |

---

## Resume Instructions

1. **Do not re-run Phase 1** unless a corpus gap is found.
2. Read [`AFI_AUDIT_RESUME_PROMPT.md`](./AFI_AUDIT_RESUME_PROMPT.md) and paste into agent task prompt.
3. Run **themes sequentially** (one at a time), writing outputs to `themes/<key>.json`.
4. **Verify** P0/P1 claims; write `themes/verified.json`.
5. **Synthesize** final reports one at a time into `afi-docs/specs/`.

### Theme priority order

1. `C-onchain-anchor`
2. `D-evidence-vault`
3. `G-emissions-mint`
4. `B-reference-impl`
5. `A-normative-surface`
6. `E-scoring-dag`
7. `J-docs-drift`
8. `I-sdks-gateway`
9. `H-governance`
10. `F-analytics`

---

## Rate-Limit Mitigation

The original workflow failed because **10 theme agents + 6 synthesis writers** launched in parallel immediately after a 2.8M-token recon phase.

**Rules for resume:**

- **No parallel theme agents** — max 1 theme at a time
- **Synthesize one report at a time**
- **Skip recon** — use persisted corpus
- **Verify before synthesize** — do not promote draft contradictions without Phase 3

---

## Related Documents

| Document | Role |
|----------|------|
| [`AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md`](../AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md) | North star / charter |
| [`AFI_PROTOCOL_INVESTIGATION_PROMPT.md`](../AFI_PROTOCOL_INVESTIGATION_PROMPT.md) | Full investigation prompt (Phase 1–4) |
| [`AFI_AUDIT_RESUME_PROMPT.md`](./AFI_AUDIT_RESUME_PROMPT.md) | Resume prompt (Phase 2–4 only) |
| [`README.md`](./README.md) | Workspace layout |
