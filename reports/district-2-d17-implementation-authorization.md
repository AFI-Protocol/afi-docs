# Authorization — District 2 D-17: Implementation Authorization (M1 only)

**Date:** 2026-07-03
**Type:** Mission-specific implementation authorization (docs-only artifact; authorizes future work, performs none)
**Satisfies:** Decision **D-17** of the merged District 2 M0 report — `reports/district-2-m0-canonical-data-boundary-and-hash-doctrine.md` (§10, §13.1, §14.2 OQ-1) — **for the first implementation phase (M1) only**
**Governance:** Subordinate to `AFI_DROID_CHARTER.v0.1.md` and `AFI_DROID_PIPEHEAD_ADDENDUM.v0.1.md`. Where this authorization conflicts with governance, governance wins.
**Baseline:** afi-docs `main` @ `6a25ab6` (merge commit of PR #8, "District 2 M0: Canonical data boundary and hash doctrine")

---

## 1. Planning baseline

The **District 2 M0 report is merged** (afi-docs PR #8, merge commit `6a25ab6`) and is hereby **accepted as the planning baseline** for District 2. Its boundary classifications, hash doctrine, provenance/disclosure structure, milestone plan (§11), and guardrails (§13) frame all District 2 implementation work.

## 2. D-17 satisfaction — scope of this instrument

D-17 requires a separate D2 authorization — "a new version of the Pipehead Addendum and/or a separate mission-specific authorization" — before any District 2 implementation begins. This document is that **separate mission-specific authorization** (resolving OQ-1's instrument choice), and it **satisfies D-17 for the first implementation phase (M1) only**.

It authorizes nothing beyond M1. It does not amend the Pipehead Addendum, and it does not authorize M2–M6 or any other District work.

## 3. What is authorized

**District 2 M1 — afi-config schema drafts and tests only**, per the M0 report's §11 M1 milestone: authoring draft JSON Schemas for the promotion set (including lifting `AnalystScoreTemplate` to a canonical JSON-Schema contract) plus positive/negative fixture tests, in afi-config. **No runtime wiring.**

## 4. Decisions accepted as implementation direction

The following M0 §10 owner decisions are **accepted as implementation direction** for District 2, to be realized only within phase scopes that are separately authorized (M1 now; later phases per §9 below):

| Decision | Accepted direction | Caveat |
|---|---|---|
| **D-1** | Canonical-vs-reactor-local classification boundary as classified in M0 §3.1 | — |
| **D-2** | Promotion roadmap (versioned promotion set) | Field-level details remain subject to PR review |
| **D-3** | `AnalystScoreTemplate` promotion to a canonical JSON-Schema contract | — |
| **D-4** | `CanonicalHash v1` as the single canonical off-chain hash | Hash doctrine cluster (D-4–D-7); spec drafting is M1, migration is not |
| **D-5** | Canonicalization-version + domain-separation discipline | " |
| **D-6** | Domain-aware timestamp policy | " |
| **D-7** | Field-specific number policy (no raw IEEE-754 floats in hashed forms) | " |
| **D-10** | `SourceDisclosureProfile v1` descriptive metadata direction | Exact enum values remain reviewable (see §5) |
| **D-11** | Option B — `AnalystInputEnvelope v1` | — |
| **D-12** | CPJ trade-level preservation (`TradePlan v1` / `SignalLevels v1`) and pseudonymous `authorRef` / `authorHash` | No raw author identity (see §5) |
| **D-13** | `ReplayProfile v1` overlay direction | — |
| **D-14** | Settlement **alignment only** (`ProvenanceRecord v1` fields aligned to canonical `signalLeaf` / `evidenceLeaf`; manifest draft stays frozen) | — |
| **D-15** | **No settlement, no L1 anchoring, no rewards, no claims, no vault mechanics** in District 2; disclosure is visibility-only | — |

**Not actioned by this instrument:** D-8 (shallow TradingView `ingestHash` deprecation/migration) and D-9 (hash-committed object set in `ProvenanceRecord v1`) are neither accepted nor rejected here — they concern hash migration and production provenance wiring, both outside M1's scope and forbidden in M1 (§7). They remain PROPOSED per the M0 report and fall to a later phase authorization.

## 5. Explicitly OPEN / deferred

The following remain **OPEN or deferred** and are **not** decided or authorized by this instrument:

- **D-16 — validator-decision schemas.** Deferred; the v0 `ValidatorDecision.ts` is non-canonical/mint-gating and MUST NOT be wired (M0 §9.5).
- **Exact D-10 enum values.** The disclosure metadata direction is accepted; the precise enum values remain reviewable at schema-PR time.
- **BenchKit ingestion seam and weighting policy** (M0 OQ-3). No BenchKit weights are defined or implied by District 2.
- **Any raw CPJ author identity disclosure.** Only the pseudonymous `authorRef` / `authorHash` direction is accepted; raw `authorId`/`authorName` exposure remains out of scope.

## 6. Allowed surface (M1)

District 2 M1 may touch **only the afi-config schema, test, and docs surfaces needed for the schema drafts** — draft JSON Schemas, positive/negative fixtures, and their accompanying documentation. Nothing else.

## 7. Forbidden in M1

District 2 M1 MUST NOT touch:

- afi-reactor production wiring
- hash migration (including any `ingestHash` migration)
- CPJ mapper behavior
- MongoDB persistence
- BenchKit weighting
- settlement / rewards / vault / claims
- validator-decision schemas
- tokenomics / emissions / economic math

## 8. Restated boundaries

Consistent with M0 §13.3–§13.4, the following boundaries govern all District 2 work:

- **MongoDB/storage is an implementation profile, not protocol canon.** Canonical truth lives in the schema/validation/hash/provenance/replay layer, never in the datastore; persistence MUST NOT alter canonical bytes.
- **BenchKit owns weighting/evaluation policy.** District 2 provides metadata only.
- **Agents/droids are protocol participants/tooling, not protocol canon.** Nothing becomes canon by virtue of an agent doing it.
- **Pipeheads are deterministic protocol processing stations.**

## 9. Phase gating

**Every implementation phase after M1 (M2–M6, and any successor) requires its own scoped PR/mission authorization.** This instrument authorizes M1 only; it neither pre-authorizes nor sequences any later phase. Completion and review of M1 do not by themselves authorize M2.

---

*This authorization performs no implementation. It changes no code, schemas, configs, packages, tests, or runtime behavior in any repository; it adds only this file to afi-docs.*
