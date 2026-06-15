# AFI Protocol Audit — Resume Prompt (Phases 2–4)

**Status:** Active — use when Phase 1 recon is already complete  
**Version:** 0.1  
**Date:** 2026-06-15  
**Checkpoint:** [`AFI_AUDIT_CHECKPOINT.md`](./AFI_AUDIT_CHECKPOINT.md)

> **Phase 1 is DONE.** Do not re-audit all 31 repos unless you find a gap in the persisted corpus. Use this prompt instead of [`AFI_PROTOCOL_INVESTIGATION_PROMPT.md`](../AFI_PROTOCOL_INVESTIGATION_PROMPT.md).

---

## How to Use

1. Read [`AFI_AUDIT_CHECKPOINT.md`](./AFI_AUDIT_CHECKPOINT.md) for current status.
2. Load [`recon/AFI_RECON_CORPUS.json`](./recon/AFI_RECON_CORPUS.json) as your per-repo map (verify claims against source files yourself).
3. Review [`drafts/`](./drafts/) for starting context (unverified).
4. Copy **everything below the horizontal rule** into the agent task prompt.
5. Run **one theme at a time** — no parallel theme agents.

---

# AFI Protocol Surface Investigation — Resume (Phases 2–4)

## Mission

Continue the read-only forensic audit of AFI Protocol to **solidify the portable protocol** per [`AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md`](../AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md).

**Phase 1 recon is complete** (31/31 repos). Your job:

1. **Phase 2 — Themes:** Answer core questions A–J with cross-repo evidence.
2. **Phase 3 — Verify:** Adversarially confirm P0/P1 claims from themes + drafts.
3. **Phase 4 — Synthesize:** Write the 6 master reports into `afi-docs/specs/`.

AFI is a **portable protocol** (HTTP-like): normative schemas and invariants at the top; pluggable implementations below. Mongo, reactor, and org infra are **reference paths**, not protocol law—unless code/docs incorrectly present them as mandatory.

## Authority and Constraints

- **Read-only:** Do not modify protocol code unless explicitly authorized.
- **Evidence-based:** Every claim cites `file:line` (or commit SHA for archived repos).
- **Use persisted corpus:** [`recon/AFI_RECON_CORPUS.json`](./recon/AFI_RECON_CORPUS.json) — verify, do not blindly trust.
- **Sequential execution:** One theme agent at a time; one synthesis report at a time.
- **No recon redo:** Skip per-repo re-audit unless corpus is missing a repo.

## Read First (in order)

1. [`audit/AFI_AUDIT_CHECKPOINT.md`](./AFI_AUDIT_CHECKPOINT.md)
2. [`audit/recon/AFI_RECON_CORPUS.json`](./recon/AFI_RECON_CORPUS.json)
3. [`audit/drafts/AFI_REFERENCE_IMPL_MAP.draft.md`](./drafts/AFI_REFERENCE_IMPL_MAP.draft.md)
4. [`audit/drafts/AFI_CONTRADICTION_REGISTER.draft.md`](./drafts/AFI_CONTRADICTION_REGISTER.draft.md)
5. [`AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md`](../AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md)

Local repo paths: `/home/user/AFI-Protocol/<repo>/`

---

## Phase 2: Themes (run sequentially)

Write each completed theme to `afi-docs/specs/audit/themes/<key>.json` using this structure:

```json
{
  "theme": "<key>",
  "summary": "...",
  "answers": [{"question": "...", "answer": "...", "evidence": "file:line"}],
  "findings": [{"title": "...", "severity": "P0|P1|P2|P3|Info", "theme": "...", "evidence": "...", "recommendation": "..."}],
  "contradictions": [{"doc_says": "...", "code_does": "...", "evidence": "...", "severity": "...", "tension": "..."}]
}
```

### Theme priority order (run in this sequence)

| Order | Key | Title | Focus repos |
|-------|-----|-------|-------------|
| 1 | `C-onchain-anchor` | Commitment Layer (BASE / On-Chain) | `afi-token`, `afi-mint`, `afi-xerc20` |
| 2 | `D-evidence-vault` | Evidence Layer & Replay Readiness | `afi-infra`, `afi-config`, `afi-reactor` |
| 3 | `G-emissions-mint` | Emissions, Mint, Settlement | `afi-math`, `afi-mint`, `afi-token`, `afi-econ` |
| 4 | `B-reference-impl` | Reference Implementation Map | all repos |
| 5 | `A-normative-surface` | Normative Protocol Surface | `afi-config`, `afi-infra`, `afi-reactor`, `afi-token` |
| 6 | `E-scoring-dag` | Scoring & DAG Plane | `afi-reactor`, `afi-core`, `afi-plugins` |
| 7 | `J-docs-drift` | Documentation & Drift | `afi-docs`, all repos |
| 8 | `I-sdks-gateway` | SDKs, Gateway, External Validators | `afi-sdk-*`, `afi-gateway`, `afi-starters` |
| 9 | `H-governance` | Governance, Registries, Reputation | `afi-governance`, `afi-config`, `afi-core` |
| 10 | `F-analytics` | Market / Analytics Plane | `afi-benchkit`, `afi-econ`, `afi-reactor`, `afi-ops` |

### Core questions (answer all in themes)

**A — Normative:** schemas/docs that are protocol law; stated-but-unenforced invariants; ingest boundary; lifecycle stages defined vs implemented; determinism/replay rules.

**B — Reference impl:** reference spine map; mandatory-stack implications (Mongo/reactor/org infra); vault engines implemented vs schema-listed.

**C — On-chain:** what is stored on-chain today (every event/struct/field/role); docs vs contracts; third-party mint verification requirements; anchor gap analysis.

**D — Evidence:** VaultedSignalRecord define/write/read sites; public vs proprietary surface in practice; replay readiness per lifecycle stage.

**E — Scoring DAG:** all pipeline/DAG definitions; replay-critical nodes; scoring formula locations; reactor-as-only-orchestrator quotes.

**F — Analytics:** BigQuery/Kafka/warehouse integrations; Mage fit; operational vs analytics plane separation.

**G — Emissions/mint:** emissions handoff math→mint→token; per-signal vs epoch batch; beneficiary model; treasury vs mint recipient.

**H — Governance:** registries/reputation vs scoring boundary; wired vs simulation-only.

**I — SDKs/gateway:** public protocol API surface; external validator integration gaps.

**J — Doc drift:** stale repo names; contradiction register expansion; normative vs reference vs archive classification for docs.

### Search patterns

`mongodb`, `MongoTSSD`, `vault`, `TSSD`, `VaultedSignalRecord`, `usignal`, `USS`, `cpj`, `CPJ`, `mintForSignal`, `coordinateMint`, `beneficiary`, `epoch`, `replay`, `ReplaySession`, `determinism`, `codex`, `publicSurface`, `proprietaryDetail`, `AFIMintCoordinator`, `AFISignalReceipt`, `EmissionsMinted`, `pipeline`, `DAG`, `froggy`, `orchestrator`, `doctrine`, `BigQuery`, `kafka`, `warehouse`, `normative`, `canonical`, `postgresql`, `timescaledb`, `influxdb`

---

## Phase 3: Verify

For every **P0** and **P1** finding from themes + [`drafts/AFI_CONTRADICTION_REGISTER.draft.md`](./drafts/AFI_CONTRADICTION_REGISTER.draft.md):

1. Re-open cited `file:line` evidence.
2. Confirm or refute the claim.
3. Record in `afi-docs/specs/audit/themes/verified.json`:

```json
{
  "verifications": [
    {
      "source": "theme:C-onchain-anchor#0",
      "title": "...",
      "original_severity": "P1",
      "confirmed": true,
      "corrected_evidence": "file:line + quote",
      "revised_severity": "P1",
      "note": "..."
    }
  ]
}
```

Prefer `confirmed: true` findings in Phase 4 synthesis. Drop or correct refuted claims.

---

## Phase 4: Synthesize (one report at a time)

Write final reports to `afi-docs/specs/` (optionally stage in `audit/final/` first):

| Report | Primary theme inputs |
|--------|---------------------|
| `AFI_NORMATIVE_REGISTER.md` | A, C, D, G, H |
| `AFI_REFERENCE_IMPL_MAP.md` | B + recon corpus |
| `AFI_CONTRADICTION_REGISTER.md` | All themes + verified.json |
| `AFI_REPLAY_READINESS_MATRIX.md` | A, D, E, C |
| `AFI_ONCHAIN_ANCHOR_GAP_ANALYSIS.md` | C, G |
| `AFI_PROTOCOL_SURFACE_AUDIT.md` | All (master report) |

Each report must:

- Link back to `AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md`
- Cross-link sibling reports by filename
- Carry `file:line` citations on factual claims
- Mark verified status for P0/P1 items

### Master report sections (`AFI_PROTOCOL_SURFACE_AUDIT.md`)

1. Executive summary (alignment score, top 10 blockers, top 10 quick wins)
2. Scope and method (31 repos, phases, verification approach)
3. Consolidated 31-repo classification table
4. Per-repo subsections (checklist fields)
5. Findings by severity with verified status
6. Solidification roadmap (Phases 0–4)
7. Open questions for human review
8. Definition-of-done checklist + cross-links

---

## Severity Rubric

| Severity | Definition |
|----------|------------|
| **P0** | External validator cannot interoperate; normative rule violated in production path |
| **P1** | Doc/code contradiction causes wrong architectural decisions |
| **P2** | Reference impl presented as protocol law; fixable by documentation |
| **P3** | Stale naming, typos, archived repo references |
| **Info** | Observation only |

---

## Definition of Done (resume)

- [ ] Themes A–J written to `audit/themes/<key>.json`
- [ ] `audit/themes/verified.json` complete for all P0/P1
- [ ] All 6 master reports in `afi-docs/specs/`
- [ ] Replay matrix covers RAW → ENRICHED → ANALYZED → SCORED → MINTED → REPLAYED
- [ ] On-chain gap analysis enumerates every relevant Solidity event/field
- [ ] Contradiction register includes all six tensions with verified status
- [ ] Checkpoint [`AFI_AUDIT_CHECKPOINT.md`](./AFI_AUDIT_CHECKPOINT.md) updated

---

## Rate-Limit Rules

- **Never** launch 10 theme agents in parallel
- **Never** launch 6 synthesis writers in parallel
- Complete one theme → save JSON → then start next theme
- Complete one report → then start next report

Begin with **Theme C (on-chain anchor)**. Be exhaustive. Cite evidence. Do not skip private repos when verifying.
