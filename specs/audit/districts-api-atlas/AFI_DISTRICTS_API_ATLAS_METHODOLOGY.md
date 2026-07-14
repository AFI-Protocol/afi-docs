# AFI Districts / API Atlas Audit — Methodology, Reliability & Corrections

> **This document is a read-only reconciliation record. It does not establish protocol authority, authorize implementation, ratify proposed doctrine, or supersede accepted governance decisions. Recommendations become authoritative only through an owner-approved AFI governance decision.**

## 1. Nature of this audit

This is an **evidence and recommendation record**, not protocol law. Every "recommended authority," "minimal correction," and "suggested slot" in the findings register is a proposal for owner review. Nothing here authorizes runtime, API, MongoDB, blockchain, minting, reward, settlement, or scoring changes. A document labeling itself "CANONICAL" was treated as a **claim to be evaluated**, not as authority.

Throughout, four states were kept distinct and never collapsed: **GOVERNED** (an accepted `afi-governance` decision or the DROID charter) · **IMPLEMENTED** (runtime code on `main`) · **DOCUMENTED** (a doc asserts it) · **PROPOSED** (draft/ADR/comment).

## 2. Repository baseline

All 13 primary repositories were re-fetched and confirmed at `origin/main` == local `main`, clean, and unchanged from the audit baseline:

| Repo | Commit | | Repo | Commit |
|---|---|---|---|---|
| afi-docs | `c666224` | | afi-mint | `d98a622` |
| afi-protocol | `7edb203` | | afi-econ | `471f4fe` |
| afi-gateway | `262fa30` | | afi-token | `d435b40` |
| afi-reactor | `9b56fb1` | | afi-infra | `e136a9c` |
| afi-core | `806db49` | | afi-math | `f20c0dd` |
| afi-config | `ce8c1de` | | afi-plugins | `95d73f3` |
| afi-governance | `6b3638b` | | | |

## 3. Access limitations

- **Fetch failed; inspected via local `main` only** (could not confirm local == `origin/main`): `afi-research-site`, `afi-sdk-python`, `afi-sdk-ts`, `afi-starters`. No blocker or high-severity finding depends on these; the SDK-README contract-drift finding (ATLAS-03) reflects local state and may differ from origin.
- **Live-chain state not verified:** on-chain role-wiring, deployed-contract status, and Safe balances are asserted from the vault-address registry and the on-chain anchor gap analysis (both DOCUMENTED), not re-verified against a live RPC.
- **Library-provided routes** (`@elizaos/server`) and vendored dependencies were not read (`.claudeignore` scope); their contracts are inferred from the gateway's own documentation.

## 4. Investigation method & reliability

- **Recon:** 11 parallel read-only dimension readers (governance corpus, prior-audit corpus, districts, API atlas, core objects, economic objects, lifecycle, gateway↔runtime, persistence, blockchain attachment, repository authority), each paired with an independent adversarial verifier that re-opened cited files (22 agents).
- **Repair pass:** the first-run persistence and blockchain-attachment agents produced degenerate output (a placeholder and a citation-only stub, respectively) and were **re-run** with full prompts and re-verified. This is disclosed rather than hidden.
- **Synthesis:** independent contradiction/dedup and minimal-program agents ran over the full finding set; the dependency spine and resumption gates were cross-checked.
- **Auditor-verified primary sources:** the human auditor independently read and verified the load-bearing sources directly — the DROID Charter, all four `afi-governance` decisions, the System Atlas, the pipehead-addendum district evidence, and the persistence/lifecycle code paths — so the executive verdict and authority findings rest on primary reads, not only agent summaries.
- **Reliability:** 22 of 24 recon/verify agents rated high-reliability. Two dimensions required the repair pass above. Where a claim was self-reviewed rather than independently verified, it is not described as independently verified.

## 5. Corrections appendix — two agent errors caught and corrected

Per the mission, superseded erroneous claims are **not** preserved as live findings. Both were corrected before the register was finalized; the live register carries only the corrected characterization, and the two originals are recorded here.

### Correction 1 — DROID Charter is NOT missing (finding DIST-H-01)
- **Original (false) recon claim:** "Supreme authority `AFI_DROID_CHARTER.v0.1.md` is referenced by every governance decision but exists in no checkout" (implying the supreme cited authority is absent).
- **Verified truth (direct read, afi-config `ce8c1de`):** the Charter **exists** at `afi-config/codex/governance/droids/AFI_DROID_CHARTER.v0.1.md`. The agent had searched only afi-governance and afi-docs, not afi-config. The governance-corpus agent found it correctly, and the contradiction reviewer confirmed the retraction.
- **Live finding (corrected):** DIST-H-01 was **downgraded blocker → low** and recharacterized as "the supreme Charter lives outside the governance repo (in afi-config) and is a droid-behavior charter that never mentions Districts" — the real residual, which is duplicated by GOV-04.

### Correction 2 — `UniversalWeightingRule.ts` exists (finding OBJ-08, originally objects-core LIFE-08)
- **Original (false) recon claim:** "no file named `UniversalWeightingRule.ts` and no `computeUwrScore` symbol exist anywhere in the workspace on main."
- **Verified truth (direct read, afi-core `806db49`):** the file **exists** at `afi-core/validators/UniversalWeightingRule.ts` (repo root, outside `src/`). `AnalystScoreTemplate.ts` (in `src/analyst/`) cites it via a relative path (`validators/UniversalWeightingRule.ts`) that does not resolve from its own location.
- **Live finding (corrected):** OBJ-08 was **downgraded medium → low** and recharacterized as a broken-relative-citation / `validators/`-vs-`src/` layout-split issue — a real but minor documentation defect, not a missing math file.

Neither original false claim survives in the live register (§3 of the report). Each corrected finding carries a **⚠ Correction note** field recording the original wording.

## 6. Register integrity

- **96 findings**, deduplicated, present identically in the human-readable report (`AFI_DISTRICTS_API_ATLAS_AUDIT.md` §3), the JSON register, and the CSV register (parity-checked by matching finding-ID sets and total count).
- **Distribution:** 6 blocker · 32 high · 33 medium · 25 low. By classification: C0=0, C1=21, C2=21, C3=12, C4=17, C5=6, C6=6, C7=12, C8=1.
- **Finding-ID namespace:** the objects-core dimension's `LIFE-*` IDs were re-namespaced to `OBJ-*` to remove a collision with the lifecycle dimension's `LIFE-*` IDs; all IDs are globally unique. The IDs used in the originally-delivered audit narrative map to these directly (objects-core `LIFE-NN` → `OBJ-NN`).
- **Severity reranks applied** (from the contradiction/synthesis pass, on evidence): DIST-H-01 blocker→low, OBJ-08 medium→low, CORP-02 high→medium, GW-01 high→medium, GOV-02 high→medium.

## 7. Standing caveat

Recommendations in this audit — including the six-decision governance spine and the three resumption gates — become authoritative only through an owner-approved AFI governance decision. This preservation record changes no code, schema, package, contract, or governance ledger.
