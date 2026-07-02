# Report — District 2 M0: Canonical Data Boundary & Hash Doctrine

**Date:** 2026-07-02
**Type:** Doctrine / decision report (design only — implements nothing; no code, no schemas, no runtime changes)
**Author scope:** Canonical data/provenance boundary + hash doctrine for AFI District 2; docs-only
**Governance:** Subordinate to `AFI_DROID_CHARTER.v0.1.md` and `AFI_DROID_PIPEHEAD_ADDENDUM.v0.1.md`. Where this report conflicts with governance, governance wins.
**Status:** DRAFT — for review; opened as a docs-only PR, NOT merged. Recommendations are PROPOSED unless labeled Canonical.
**Baseline:** Written against origin/main — afi-reactor 069f56c, afi-config 400c167, afi-core 390b440, afi-math a27de91, afi-factory 59330cc, afi-docs 5d51d75.

> **Status: planning / M0 decision report.** This is a design-only artifact. It decides — on paper — which current data shapes become protocol canon and which stay reactor/strategy-local, plus the hash doctrine, provenance/disclosure structure, analyst-input shape, CPJ survival policy, replay profile, and the settlement/validator boundary. It **implements nothing**: no code, no JSON schemas, and no runtime/scoring/math/settlement/tokenomics/emissions/rewards/validator/pipehead changes. Every substantive recommendation is labeled **Canonical** / **PROPOSED** / **OPEN**; adoption is the owner's later decision.

---

## 1. Executive Summary

> **(INITIAL — finalized in §14/F8.)** This summary is written first and reconciled against the full body during finalization. Where it and a detailed section disagree, the detailed section governs until this summary is re-synced.

District 1 (the Signal-Evaluation Pipehead POC) has been **hardened by Mission 1.5-B** and, on `origin/main`, has **resolved DR-001 and DR-002**: the pipehead now runs canonical USS v1.1 validation (AJV + afi-config schemas) and the canonical Wilder indicator kernel (`trading-signals` v7), with `golden.json` re-pinned. District 2 builds on that hardened base. It does **not** re-do District 1 work; it targets the three things District 1 deliberately left in place: (a) which current data shapes become protocol canon vs. stay reactor/strategy-local, (b) a unified hash doctrine, and (c) provenance/disclosure/analyst-input structure.

**Boundary.** USS v1.1 and CPJ v0.1 are **[Canonical]** schema-backed inputs (afi-config JSON Schemas + AJV validators). `AnalystScoreTemplate` is a **[PROPOSED]** high-priority promotion (a real runtime Zod schema, but afi-core-only and reactor-stubbed as `any` — not yet protocol canon). `ReactorScoredSignalV1`, `AnalysisBundle`, and the five lane payloads are **reactor-local** (POC); `FroggyEnrichedView` is **strategy-local**; `AuditRecord` and the settlement manifest draft are **doctrine-only / frozen**. The report offers a **[PROPOSED]** promotion set with versioned names: a thin `ScoredSignal v1` projection, `AnalystInputEnvelope v1`, `ProvenanceRecord v1`, `SourceDisclosureProfile v1`, `EvidenceRef v1`, `EnrichmentProvenance v1`, optional `TradePlan v1` / `SignalLevels v1`, a `ReplayProfile v1` overlay, and a `CanonicalHash v1` spec.

**Hash doctrine.** Recommend one canonical off-chain hash — **[PROPOSED]** `CanonicalHash v1` (recursive key-sort → JSON serialize → sha256), formalizing the pipehead canonicalizer; on-chain keccak256 stays a **separate, explicitly-labeled domain**. Bind an explicit `canonicalizationVersion` into a per-object type+version domain tag (there is **zero** domain separation today). Timestamp policy is **domain-aware** (volatile processing stamps excluded; declared evidence/source stamps may be included). Number policy is **field-specific** and bans raw IEEE-754 floats in any hashed form, backed by the afi-math Wave 2 audit. Deprecate the **shallow/lossy TradingView `ingestHash`** while explicitly **not** generalizing that criticism to the recursive/lossless CPJ `ingestHash`.

**Provenance & boundaries.** Analyst input → **[PROPOSED]** Option B (`AnalystInputEnvelope v1` wrapping the strategy-local view + provenance/disclosure/evidence metadata). CPJ trade levels and author identity survive as optional `TradePlan v1` / `SignalLevels v1` metadata and a pseudonymous `authorRef` / `authorHash`. Keep USS broad and optional with a stricter `ReplayProfile v1` overlay. Disclosure metadata is descriptive and computable; **District 2 provides metadata, BenchKit defines evaluation weights, and reward/reputation consequences are deferred**. The settlement manifest draft stays **frozen [Canonical]**; `ProvenanceRecord v1` aligns to the canonical `signalLeaf` / `evidenceLeaf`; **no** Layer-1 anchoring, rewards, claims, settlement, or vault mechanics enter D2; disclosure is visibility-only; validator-decision schemas are **[OPEN]** (deferred). A consolidated owner-decision list, a proposed D2 milestone plan, risks-if-skipped, and explicit non-production / non-settlement guardrails follow.

---

## 2. Baseline & Scope Reconfirmation

### 2.1 Baseline note

**`origin/main` is canonical.** This report is written against the following `origin/main` pins, which match the mission brief's stated baseline commits **exactly**:

| Repo | `origin/main` pin (canonical) |
|---|---|
| afi-reactor | `069f56c` |
| afi-config | `400c167` |
| afi-core | `390b440` |
| afi-math | `a27de91` |
| afi-factory | `59330cc` |
| afi-docs | `5d51d75` |

During planning the **local clones were found stale** (2–6 commits behind `origin/main`) and were reconciled by `git fetch`, treating `origin/main` as the single canonical source. There is **no divergence between the mission brief and `origin/main`** — the brief's baseline commits and `origin/main` agree; the **staleness was local-only**. Every substantive claim in this report is verified against `origin/main` via `git -C <repo> show origin/main:<path>` (or the clean detached worktrees prepared at `/home/factory-user/afi-d2-m0-planning/wt/{afi-reactor,afi-config,afi-docs,afi-math}`); stale local working trees are never cited, and pre-existing dirty/untracked files in any repo are user-owned and untouched.

### 2.2 Verified data-shape inventory summary

The boundary and hash recommendations rest on a verified inventory of the current org's data shapes and hashing paths, confirmed on `origin/main`. This is a summary; the per-shape classification (canonical / promotion / reactor-local / strategy-local / doctrine-only / demo-only) is detailed in §3, and the hash-path analysis in §4.

- **Canonical schema-backed inputs [Canonical].** USS v1.1 and CPJ v0.1 are backed by JSON Schema (Draft-07) in afi-config and enforced by AJV validators. USS v1.1 self-labels as the *"v1.1 Runtime Canon"* (`origin/main afi-config/schemas/usignal/v1_1/index.schema.json`) with core `$ref` (`.../v1_1/core.schema.json`); CPJ v0.1 is the labeled first normalization stage before USS mapping (`afi-config/schemas/cpj/v0_1/{index,core}.schema.json`), validated in the reactor (`afi-reactor/src/uss/ussValidator.ts`, `afi-reactor/src/cpj/cpjValidator.ts`).
- **Ingest fidelity gap.** The CPJ→USS mapper (`afi-reactor/src/uss/cpjMapper.ts`) **drops** author identity (`authorId`/`authorName`) and the trade levels (`entry`/`stopLoss`/`takeProfits`/`leverageHint`) from USS output — they survive only inside the ingest-hash canonicalization. This loss is schema-enforced: USS `facts` is `additionalProperties:false` (`afi-config/schemas/usignal/v1_1/index.schema.json:31,57`), so there is no slot for those fields. (Survival policy → §7.)
- **Heavy / loose contracts.** `ReactorScoredSignalV1` embeds `rawUss:any`, `lenses:any[]`, `_priceFeedMetadata`, and the full `analystScore` (`afi-reactor/src/types/ReactorScoredSignalV1.ts`); `FroggyEnrichedView` is strategy-local and loose (loose `indicators` map, `enrichedView:unknown`), and the analyst receives only that view (`afi-reactor/plugins/froggy-enrichment-adapter.plugin.ts`). (Classification → §3; envelope → §6.)
- **`AnalystScoreTemplate`.** A real runtime **Zod** schema enforced **only** in the afi-core Froggy analyst via `safeParse` (`afi-core/analysts/froggy.trend_pullback_v1.ts`, defined `afi-core/src/analyst/AnalystScoreTemplate.ts`), stubbed as ambient `any` in the reactor (`afi-reactor/typings.d.ts`). Not protocol-wide canon → **[PROPOSED]** promotion (§3).
- **Hashing is not unified.** Off-chain, three distinct canonicalizers coexist — the pipehead `canonicalHash` (recursive key-sort + sha256, POC; `afi-reactor/src/pipeheads/canonicalHash.ts`), the CPJ `ingestHash` (**recursive / lossless**, production; `afi-reactor/src/uss/cpjMapper.ts`), and the TradingView `ingestHash` (**shallow / lossy** allow-list `JSON.stringify`, production; `afi-reactor/src/uss/tradingViewMapper.ts`) — plus on-chain keccak256 in the afi-token Solidity as a separate hash family. There is **no domain separation** and production **scoring is hash-free** (`canonicalHash`/audit/receipt live only under `afi-reactor/src/pipeheads/**`). (Doctrine → §4.)
- **Doctrine-only / frozen shapes.** `AuditRecord` (`afi-reactor/src/pipeheads/auditPipehead.ts`) is a POC shape whose *concept* seeds `ProvenanceRecord v1`; the settlement manifest draft (`afi-config/schemas/afiEpochSettlementManifest.draft.schema.json` + `afi-docs/specs/AFI_SETTLEMENT_V1_MANIFEST_AND_PROVENANCE_SCHEMA.md`) stays DRAFT/frozen. (Settlement boundary → §9.)

### 2.3 Terminology corrections & scope reconfirmation

- **CPJ = "Canonical Parsed JSON."** The canonical schemas and mapper name CPJ *"Canonical Parsed JSON"* (`origin/main afi-config/schemas/cpj/v0_1/core.schema.json` title: `"AFI Canonical Parsed JSON - Core (v0.1)"`; mapper header `afi-reactor/src/uss/cpjMapper.ts`). The afi-reactor `AGENTS.md` expands it as *"Canonical **Protocol** JSON"* — that is a stale/incorrect expansion. This report uses **Canonical Parsed JSON** throughout. CPJ is an *intermediate* canonical input (a normalization stage before USS v1.1), not a terminal signal.
- **DR-001 / DR-002 are RESOLVED on `origin/main` (scope reconfirmation).** Earlier local narratives (and the pipehead report body) framed "restore canonical USS validation" and "restore the canonical indicator kernel" as District 2's next mission. That work is **done** (Mission 1.5-B): `afi-reactor/src/pipeheads/schemaValidationPipehead.ts` now delegates to canonical `validateUsignalV11` (`import { validateUsignalV11 } from "../uss/ussValidator.js"`), and the real deps `ajv ^8.17.1`, `ajv-formats ^3.0.1`, and `trading-signals ^7.4.3` are present (`afi-reactor/package.json`). District 2's scope is therefore the boundary, hash doctrine, and provenance/disclosure work — **not** re-doing District 1's canonical validation/kernel hardening. Full reconciliation of the stale prior-doc language is recorded in §14.
- **Position size.** CPJ carries a `leverageHint` but **no** `size`/notional field, and USS v1.1 has neither leverage nor size — noted so §7 does not propose recovering a field that never existed.
