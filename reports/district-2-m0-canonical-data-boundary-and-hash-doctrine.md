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

- **Canonical schema-backed inputs [Canonical].** USS v1.1 and CPJ v0.1 are backed by JSON Schema (Draft-07) in afi-config and enforced by AJV validators. USS v1.1 self-labels as the *"v1.1 Runtime Canon"* (`afi-config/schemas/usignal/v1_1/index.schema.json:4`) with core `$ref` (`.../v1_1/core.schema.json`); CPJ v0.1 is the labeled first normalization stage before USS mapping (`afi-config/schemas/cpj/v0_1/{index,core}.schema.json`, title at `core.schema.json:4`), validated in the reactor (`afi-reactor/src/uss/ussValidator.ts:109` `validateUsignalV11`, `afi-reactor/src/cpj/cpjValidator.ts:122` `validateCpjV01`).
- **Ingest fidelity gap.** The CPJ→USS mapper (`afi-reactor/src/uss/cpjMapper.ts:306-329`) **drops** author identity (`authorId`/`authorName`) and the trade levels (`entry`/`stopLoss`/`takeProfits`/`leverageHint`) from USS output — they survive only inside the ingest-hash canonicalization. This loss is schema-enforced: USS `facts` is `additionalProperties:false` (`afi-config/schemas/usignal/v1_1/index.schema.json:31,57`), so there is no slot for those fields. (Survival policy → §7.)
- **Heavy / loose contracts.** `ReactorScoredSignalV1` embeds `rawUss:any` (`afi-reactor/src/types/ReactorScoredSignalV1.ts:25`), `lenses:any[]` (`:28`), `_priceFeedMetadata` (`:31-37`), and the full `analystScore` (`:40`); `FroggyEnrichedView` is strategy-local and loose (loose `indicators` map, `enrichedView:unknown`), and the analyst receives only that view (`afi-reactor/plugins/froggy-enrichment-adapter.plugin.ts:622`). (Classification → §3; envelope → §6.)
- **`AnalystScoreTemplate`.** A real runtime **Zod** schema enforced **only** in the afi-core Froggy analyst via `safeParse` (`afi-core/analysts/froggy.trend_pullback_v1.ts:262`, defined `afi-core/src/analyst/AnalystScoreTemplate.ts:135`), stubbed as ambient `any` in the reactor (`afi-reactor/typings.d.ts:11`). Not protocol-wide canon → **[PROPOSED]** promotion (§3).
- **Hashing is not unified.** Off-chain, three distinct canonicalizers coexist — the pipehead `canonicalHash` (recursive key-sort + sha256, POC; `afi-reactor/src/pipeheads/canonicalHash.ts:34`), the CPJ `ingestHash` (**recursive / lossless**, production; `afi-reactor/src/uss/cpjMapper.ts:222`), and the TradingView `ingestHash` (**shallow / lossy** allow-list `JSON.stringify`, production; `afi-reactor/src/uss/tradingViewMapper.ts:50`) — plus on-chain keccak256 in the afi-token Solidity as a separate hash family. There is **no domain separation** and production **scoring is hash-free** (`canonicalHash`/audit/receipt live only under `afi-reactor/src/pipeheads/**`). (Doctrine → §4.)
- **Doctrine-only / frozen shapes.** `AuditRecord` (`afi-reactor/src/pipeheads/auditPipehead.ts:60`) is a POC shape whose *concept* seeds `ProvenanceRecord v1`; the settlement manifest draft (`afi-config/schemas/afiEpochSettlementManifest.draft.schema.json:4` + `afi-docs/specs/AFI_SETTLEMENT_V1_MANIFEST_AND_PROVENANCE_SCHEMA.md:3`) stays DRAFT/frozen. (Settlement boundary → §9.)

### 2.3 Terminology corrections & scope reconfirmation

- **CPJ = "Canonical Parsed JSON."** The canonical schemas and mapper name CPJ *"Canonical Parsed JSON"* (`afi-config/schemas/cpj/v0_1/core.schema.json:4` title: `"AFI Canonical Parsed JSON - Core (v0.1)"`; mapper header `afi-reactor/src/uss/cpjMapper.ts:4`). The afi-reactor `AGENTS.md:111` expands it as *"Canonical **Protocol** JSON"* — that is a stale/incorrect expansion. This report uses **Canonical Parsed JSON** throughout. CPJ is an *intermediate* canonical input (a normalization stage before USS v1.1), not a terminal signal.
- **DR-001 / DR-002 are RESOLVED on `origin/main` (scope reconfirmation).** Earlier local narratives (and the pipehead report body) framed "restore canonical USS validation" and "restore the canonical indicator kernel" as District 2's next mission. That work is **done** (Mission 1.5-B): `afi-reactor/src/pipeheads/schemaValidationPipehead.ts:28` now delegates to canonical `validateUsignalV11` (`import { validateUsignalV11 } from "../uss/ussValidator.js"`), and the real deps `ajv ^8.17.1`, `ajv-formats ^3.0.1`, and `trading-signals ^7.4.3` are present (`afi-reactor/package.json:40-41,50`). District 2's scope is therefore the boundary, hash doctrine, and provenance/disclosure work — **not** re-doing District 1's canonical validation/kernel hardening. Full reconciliation of the stale prior-doc language is recorded in §14.
- **Position size.** CPJ carries a `leverageHint` but **no** `size`/notional field, and USS v1.1 has neither leverage nor size — noted so §7 does not propose recovering a field that never existed.

---

## 3. Canonical vs Reactor-Local Boundary

This section classifies every current data shape in the org into one of six categories — **canonical schema-backed**, **candidate for promotion (PROPOSED)**, **reactor-local**, **strategy-local**, **deprecated/demo-only**, or **doctrine-only/frozen draft** — and then lists the firm promotion recommendations. The governing principle: a shape is **canonical** only when it is backed by a runtime schema owned by the protocol schema repo (afi-config JSON Schema, AJV-enforced at the reactor boundary). Everything else is local (reactor or strategy), a POC/demo artifact, or a frozen draft, and stays that way unless explicitly promoted. All classifications are verified against `origin/main`; only USS v1.1 and CPJ v0.1 clear the canonical bar today.

> **AFI Agent Boundary — [Canonical].** Before the per-shape classification, this report states the governance relationship that frames the whole boundary exercise. Four points:
>
> 1. **Pipeheads are deterministic protocol processing stations — fixed, replayable rules, not agent discretion.** The Pipehead Addendum requires that "the trust-critical AFI logic invoked by that node remains deterministic, auditable, and governed by explicit protocol rules" (`afi-config/codex/governance/droids/AFI_DROID_PIPEHEAD_ADDENDUM.v0.1.md:17`), that "AFI's deterministic modules produce protocol truth" (`AFI_DROID_PIPEHEAD_ADDENDUM.v0.1.md:197`), and that a droid "may not silently alter, replace, or reinterpret" deterministic kernel logic (`:77`); substituting LLM judgment for deterministic scoring (`:110`) and deciding a signal is "good" by subjective reasoning (`:111`) are explicitly **forbidden** droid actions, and trust-critical outputs "must remain deterministic, auditable, replayable, and governed by explicit protocol rules" (`:328`). **[Canonical]** — restated governance.
> 2. **Agents/droids MAY build, configure, inspect, and operate AFI-compatible pipelines.** The Addendum authorizes a droid to "build, maintain, operate, test, monitor, repair, and report on that node's execution surface" (`AFI_DROID_PIPEHEAD_ADDENDUM.v0.1.md:17`), to "operate AFI pipeline nodes" (`:25`), to "invoke deterministic AFI modules" (`:27`) and "maintain the machinery around those modules" (`:29`), and enumerates the allowed pipehead actions — operating a DAG node, managing APIs and adapters, validating schemas, normalizing and routing inputs, running deterministic scoring and reputation modules, executing tests and replay checks, generating fixtures, audit records, and reports, and monitoring pipeline health (`:83-101`). Droids are the tooling/operators that assemble and run pipeheads. **[Canonical]** — restated governance.
> 3. **Canonical truth remains in the schemas, deterministic validation, the hash doctrine, provenance records, replay profiles, and documented standards — never in an agent's runtime behavior.** Governance establishes the principle that "AFI's deterministic modules produce protocol truth" (`AFI_DROID_PIPEHEAD_ADDENDUM.v0.1.md:197`) and that "Droids may not become the source of financial truth" (`:326`). The specific District 2 enumeration of where canonical truth resides — the schemas, deterministic validation, the hash doctrine, provenance records, replay profiles, and documented standards — is this report's own framing of the canon layer that the governance principle protects; governance does not enumerate that set itself. **[Canonical]** — principle restated from governance; the District 2 canon enumeration is the report's framing.
> 4. **Agents/droids are users/tooling of the protocol, NOT protocol canon themselves — nothing an agent does becomes canon by virtue of the agent doing it; only the schema / validation / hash / provenance / replay / standards layer is canon.** The Addendum's trust boundary "separates **operation** from **authority**": "Droids may operate the pipeline machinery," "AFI's deterministic modules produce protocol truth," and "Humans and governance processes decide high-risk protocol changes" (`AFI_DROID_PIPEHEAD_ADDENDUM.v0.1.md:193,195,197,199`); the Charter's "Propose, Don't Decide" rule binds droids to proposing via branches and PRs while "Humans (and, where appropriate, AOS-governed workflows) make final decisions" (`afi-config/codex/governance/droids/AFI_DROID_CHARTER.v0.1.md:90-92`), and the Addendum closes with "Droids may not become the source of financial truth" (`AFI_DROID_PIPEHEAD_ADDENDUM.v0.1.md:326`). The "nothing an agent does becomes canon by virtue of the agent doing it" phrasing is this report's own framing of that operation-≠-authority separation. **[Canonical]** — restated governance (operation ≠ authority); the canon-by-virtue phrasing is the report's framing.

### 3.1 Per-shape classification

| Shape | Classification | Notes / evidence (`origin/main`) |
|---|---|---|
| **USS v1.1** | **[Canonical]** schema-backed | JSON Schema Draft-07 in afi-config (`afi-config/schemas/usignal/v1_1/index.schema.json:4` title *"AFI Universal Signal Schema - Root (v1.1 Runtime Canon)"*; `core.schema.json` via `$ref`), enforced by AJV in the live ingest path (`afi-reactor/src/uss/ussValidator.ts:109` `validateUsignalV11`, invoked `afi-reactor/src/server.ts:356`). Terminal runtime signal. |
| **CPJ v0.1** | **[Canonical]** schema-backed | JSON Schema Draft-07 (`afi-config/schemas/cpj/v0_1/{index,core}.schema.json`; `core.schema.json:4` title *"AFI Canonical Parsed JSON - Core (v0.1)"*), enforced by AJV (`afi-reactor/src/cpj/cpjValidator.ts:122` `validateCpjV01`, invoked `afi-reactor/src/server.ts:314`). Intermediate normalization stage before USS mapping — not a terminal signal. |
| **AnalystScoreTemplate** | **[PROPOSED]** high-priority promotion (**NOT** yet Canonical) | Real runtime **Zod** schema `AnalystScoreTemplateSchema` (`afi-core/src/analyst/AnalystScoreTemplate.ts:135`; interface `:31`), enforced **only** in the afi-core Froggy analyst via `safeParse` (`afi-core/analysts/froggy.trend_pullback_v1.ts:262`). BUT: lives in **afi-core** (not the afi-config schema repo), is **Zod** (not the canonical JSON-Schema form), and the reactor stubs it as ambient **`any`** (`afi-reactor/typings.d.ts:11` `export type AnalystScoreTemplate = any;`). ⇒ partially schema-backed only → promote (full rationale §3.2). |
| **ReactorScoredSignalV1** | **reactor-local** | Very heavy response contract: embeds `rawUss: any` (`afi-reactor/src/types/ReactorScoredSignalV1.ts:25`), `lenses?: any[]` (`:28`), `_priceFeedMetadata` with `technicalIndicators?: any`/`patternSignals?: any` (`:31-37`), and the full `analystScore` (`:40`). No schema for the envelope. Recommend a thin projection instead (§3.3). |
| **AnalysisBundle** | **reactor-local** (POC) | TS-only interface, POC-only (`afi-reactor/src/pipeheads/types.ts:77`; `enrichedView: unknown` at `:84`). Lives entirely under `afi-reactor/src/pipeheads/**`; not on the production scored path. |
| **Lane payloads (5 lanes)** | **reactor-local / strategy-local** (POC; 3 provisional) | Five TS-only payloads under `afi-reactor/src/pipeheads/lanes/**` (`technicalLane.ts:56`, `patternLane.ts:31`, `newsLane.ts:46`, `socialLane.ts:40`, `aimlLane.ts:39`). `technical`/`pattern` are wired; `news`/`social`/`ai-ml` are provisional committed fixtures. POC-only; not promoted. |
| **FroggyEnrichedView** | **strategy-local** | Froggy-specific and loose: `technical.indicators?: Record<string, number \| null>` loose map, and `AnalysisBundle.enrichedView: unknown` (`afi-reactor/src/pipeheads/types.ts:84`); defined in afi-core (`afi-core/analysts/froggy.enrichment_adapter.ts:104`), reactor-stubbed `any` (`afi-reactor/typings.d.ts:15`). Produced in production by `afi-reactor/plugins/froggy-enrichment-adapter.plugin.ts:622`. Do **not** promote — wrap it (§6). |
| **AuditRecord** | **doctrine-only** → basis for `ProvenanceRecord v1` | POC shape self-labeled `demoOnly: true` (`afi-reactor/src/pipeheads/types.ts:108`; built by `afi-reactor/src/pipeheads/auditPipehead.ts:60`). Promote the **concept** (a hash-committed provenance record), aligned to the canonical `signalLeaf`/`evidenceLeaf` — **not** this demo shape (§9). |
| **pipehead demo JSON blocks** | **deprecated/demo-only** | POC CLI output printed by `afi-reactor/src/cli/run-pipehead-demo.ts:135-138` (non-production POC). Illustrative only; never canon. |
| **Settlement manifest draft** | **doctrine-only / frozen draft** | DRAFT JSON Schema (`afi-config/schemas/afiEpochSettlementManifest.draft.schema.json:4`) + spec (`afi-docs/specs/AFI_SETTLEMENT_V1_MANIFEST_AND_PROVENANCE_SCHEMA.md:3`, DRAFT/not-Accepted). Keep **frozen** — do not resolve its OPEN items (§9). |

**Reading the table:** only USS v1.1 and CPJ v0.1 are **[Canonical]**. `AnalystScoreTemplate` is the single near-miss — schema-backed, but in the wrong repo, wrong schema form, and unenforced at the reactor boundary — so it is a **[PROPOSED]** promotion, not canon (§3.2). Everything else is reactor-local, strategy-local, demo-only, or a frozen draft, and none of it is promoted to canon as-is.

### 3.2 AnalystScoreTemplate — why [PROPOSED], not [Canonical]

`AnalystScoreTemplate` is the one shape that could be mistaken for already-canonical, because it is genuinely schema-validated at runtime. It is **[PROPOSED]** for high-priority promotion, **not [Canonical]**, for three precise reasons verifiable on `origin/main`:

1. **It is a Zod schema, not the canonical JSON-Schema form.** The runtime guard is `AnalystScoreTemplateSchema = z.object({ … })` (`afi-core/src/analyst/AnalystScoreTemplate.ts:135`), a TypeScript-runtime Zod object with enum/range constraints — a different validator family from the AJV + JSON-Schema Draft-07 mechanism that backs USS v1.1 and CPJ v0.1 in afi-config.
2. **It lives in afi-core, not the afi-config schema repo.** Both interface (`AnalystScoreTemplate.ts:31`) and schema (`:135`) sit in **afi-core**. The protocol's canonical schemas are owned by afi-config; a strategy/analyst-layer Zod object in afi-core is not protocol canon.
3. **Enforcement is single-analyst and reactor-opaque.** The `safeParse` call fires **only** inside the afi-core Froggy analyst (`afi-core/analysts/froggy.trend_pullback_v1.ts:262` `AnalystScoreTemplateSchema.safeParse(analystScore)`) — one strategy, not a protocol-wide boundary. Worse, the reactor that carries the score treats the type as ambient **`any`** (`afi-reactor/typings.d.ts:11` `export type AnalystScoreTemplate = any;`), so no validation occurs at the reactor boundary at all.

**Recommendation — [PROPOSED]:** lift `AnalystScoreTemplate` to a canonical **JSON-Schema** contract in **afi-config** and enforce it (AJV) at the reactor boundary, so the analyst score is validated where it crosses the protocol seam rather than only inside one afi-core analyst. This is the highest-priority promotion because the shape is already stable and schema-shaped — it just lives in the wrong place, in the wrong form, and is unenforced where it matters. It must **not** be described as already-canonical or protocol-wide schema-backed today.

### 3.3 Recommended promotions (all [PROPOSED])

The following promotions are offered as firm defaults for owner review. Each is **[PROPOSED]** (not Canonical) and carries a versioned name; none is adopted by this report. Detailed field-level shape is deferred to the sections noted; here they are named, scoped, and justified.

- **[PROPOSED] `ScoredSignal v1`** — a **thin** scored-signal projection to replace the heavy `ReactorScoredSignalV1` as the canonical scored output. Keep only `{ signalId, uwrScore, uwrAxes, scoredAt, meta }` and **drop** `rawUss: any` / `lenses?: any[]` / `_priceFeedMetadata` (`afi-reactor/src/types/ReactorScoredSignalV1.ts:25,28,31`), which today drag the entire raw input and all enrichment through every scored signal. (Cross-ref §4 for its hash commitment.)
- **[PROPOSED] `AnalystInputEnvelope v1`** — a protocol envelope that **wraps** the strategy-local `FroggyEnrichedView` alongside provenance/disclosure/evidence metadata, rather than expanding the loose strategy shape itself. Keeps a clean seam between strategy-local enrichment and protocol metadata. (Recommendation and Option A vs B analysis in §6.)
- **[PROPOSED] `ProvenanceRecord v1`** — the promoted **concept** behind the POC `AuditRecord` (`afi-reactor/src/pipeheads/types.ts:108`), redesigned to align with the canonical `signalLeaf` / `evidenceLeaf` (Layer 1 spec) and to carry the D2 hash commitments — **not** the demo shape. (Field alignment in §9.)
- **[PROPOSED] `SourceDisclosureProfile v1`** — a descriptive disclosure/transparency metadata shape (source class, disclosure level, withheld reason, license constraint, replayability, freshness, provider attestation, etc.). Descriptive only; defines no BenchKit weights. (Field set in §5.)
- **[PROPOSED] `EvidenceRef v1`** — a hash-addressable reference to a piece of evidence (payload/evidence hash + source ref + stage), so evidence can be committed and cited without inlining raw payloads. (Used by the hash-committed set in §4 and the disclosure profile in §5.)
- **[PROPOSED] `EnrichmentProvenance v1`** — a **lane-provenance carrier**. This is needed because the normalize step **currently destroys lane self-labels**: `normalizePipehead.buildEnrichedView` → `projectTechnical` (`afi-reactor/src/pipeheads/normalizePipehead.ts:196-212`) keeps only `emaDistancePct` + `{ema20,ema50,rsi14,atr14}` and **drops** `trendBias`, `indicatorSource`, and `canonicalIndicatorKernel` (and the sibling projections likewise drop each lane's `provisional`/`fixtureSource`/`note`). So the analyst never learns which lane produced a field, whether it was the canonical Wilder kernel or a provisional committed fixture. `EnrichmentProvenance v1` preserves that per-lane attribution (lane id, provisional/fixture status, kernel identity, source label) through normalization.
- **[PROPOSED] `CanonicalHash v1`** — a single canonical off-chain hash spec formalizing the pipehead recursive canonicalizer (`afi-reactor/src/pipeheads/canonicalHash.ts:34`), with explicit domain separation and canonicalization version. (Full doctrine in §4.)
- **[PROPOSED] optional `TradePlan v1` / `SignalLevels v1`** — optional metadata to preserve CPJ trade levels (`entry`/`stopLoss`/`takeProfits`/`leverageHint`) that the mapper currently drops from USS output. (CPJ survival policy in §7.)
- **[PROPOSED] `ReplayProfile v1`** — a stricter overlay on top of broad/optional USS for D2-conformant provenance records (facts, datasetId, codeCommit, seed, evidence hashes, source refs). (Replay policy in §8.)

All ten items above are **[PROPOSED]** — new defaults offered for owner decision (§10). Nothing in this section is adopted; USS v1.1 and CPJ v0.1 remain the only **[Canonical]** shapes, and every reactor-local / strategy-local / demo-only / frozen shape retains its classification until the owner approves a promotion.

---

## 4. Hash Doctrine

Hashing in the current org is **fragmented and undisciplined**: off-chain there are three distinct JSON canonicalizers (one recursive POC, one recursive-lossless production, one shallow-lossy production), on-chain there is a separate `keccak256` domain, there is **no domain separation** anywhere, and the production scoring path computes no content hash at all. This section proposes a single canonical off-chain hash, a domain/version discipline, a domain-aware timestamp policy, a field-specific number policy, and names the object set District 2 should hash-commit. Every claim is verified on `origin/main`; nothing here is adopted — all recommendations are **[PROPOSED]** unless labeled **[Canonical]**.

### 4.1 One canonical off-chain hash — [PROPOSED] `CanonicalHash v1`

**[PROPOSED] `CanonicalHash v1`** — adopt the pipehead recursive canonicalizer as the single off-chain canonical hash function: **recursive key-sort → `JSON.stringify` → sha256**, emitted as a **64-char lowercase hex** digest. This formalizes the existing `afi-reactor/src/pipeheads/canonicalHash.ts`, whose `canonicalValue` recurses arrays element-wise and sorts object keys at every depth (`Object.keys(source).sort()`, `canonicalHash.ts:41`), serializes via `JSON.stringify` (`canonicalize`, `:65`), and hashes with `crypto.createHash("sha256")…digest("hex")` (`canonicalHash`, `:70`). Its own module docstring (`canonicalHash.ts:1-9`) already names itself the generalization of the TradingView `generateIngestHash` "precedent" into "a recursive, key-SORTED canonicalizer" — i.e. the intended single discipline already exists in POC form and merely needs promotion, versioning, and domain separation.

**On-chain `keccak256` is a separate, explicitly-labeled domain [Canonical].** The only domain-tag-like hashing in the tree today is on-chain Solidity `keccak256` over role/identifier constants — `keccak256("EMISSIONS_ROLE")` (`afi-token/src/AFIToken.sol:32`, `afi-token/src/AFIMintCoordinator.sol:14`), `keccak256("MINT_COORDINATOR_ROLE")` (`afi-token/src/AFISignalReceipt.sol:13`). This is a **different hash family** (keccak256, not sha256) serving the on-chain domain. `CanonicalHash v1` (off-chain sha256 content addressing) and on-chain `keccak256` MUST stay **distinct, explicitly-labeled domains** and must never be conflated or treated as interchangeable.

### 4.2 Canonicalization version + domain separation — [PROPOSED]

**Zero domain separation today (verified).** None of the three off-chain JSON hashers prefixes, tags, or salts its input: `canonicalHash` hashes the bare canonical JSON (`canonicalHash.ts:65,70`), the TradingView `ingestHash` hashes `JSON.stringify(payload, …)` directly (`tradingViewMapper.ts:51-52`), and the CPJ `ingestHash` hashes `JSON.stringify(normalized)` directly (`cpjMapper.ts:253-255`). A raw USS, an `AnalysisBundle`, and a scoring projection are therefore all fed through the **same bare `sha256(JSON)`** with no type discriminator — so a cross-type collision is structurally possible (only incidental field-shape differences prevent it today).

**[PROPOSED] Bind an explicit `canonicalizationVersion` into a per-object type+version domain tag.** `CanonicalHash v1` MUST prepend a type+version **domain tag** to the canonical bytes before hashing — e.g. `AFI:signal:v1`, `AFI:evidence:v1`, `AFI:scored:v1` — and carry an explicit `canonicalizationVersion` (e.g. `afi.canon.v1`) that is **bound into** that tag. This makes a hash depend on *what* is being hashed (preventing cross-type collision) and makes any future change to the canonicalization rules **detectable** (a version bump changes every digest by construction), rather than silently re-pinning hashes as happens today.

### 4.3 Timestamp policy — [PROPOSED] (domain-aware, not blanket exclusion)

The policy distinguishes **two classes** of timestamp rather than excluding all of them:

- **(a) Volatile runtime/processing timestamps — EXCLUDED by default.** These are the current `EXCLUDED_TIMESTAMP_KEYS` constant, stripped recursively at every depth before hashing (`canonicalHash.ts:18-27,42-44`): **`scoredAt`, `issuedAt`, `producedAt`, `normalizedAt`, `startedAt`, `finishedAt`, `at`, `timestamp`**. These are human/processing artifacts and must never influence a content hash.
- **(b) Normalized evidence/source timestamps — MAY be INCLUDED when domain-declared.** Timestamps such as **`asOf`, `fetchedAt`, `postedAt`, `observationTime`** are part of a signal's evidentiary identity/provenance (when a fact was true / observed / fetched) and MAY be **included** in the hashed form when the object's domain tag (§4.2) explicitly declares them. Blanket exclusion would erase legitimate provenance; hence the policy is **domain-aware**, not a uniform strip.

**[PROPOSED] `scoredAt`-inside-the-scored-object hazard — flag & fix.** The afi-core scorer writes a wall-clock stamp **inside** the scored object: `buildAnalystScoreTemplate` sets `scoredAt: new Date().toISOString()` (`afi-core/analysts/froggy.trend_pullback_v1.ts:239`). Today the POC is insulated only because `outputHash` hashes an explicit projection that omits `scoredAt` (`buildScoringProjection`, `canonicalHash.ts:88-99`) and `scoredAt` is in the excluded set; the audit record self-labels `scoredAtExcluded: true` (`afi-reactor/src/pipeheads/auditPipehead.ts:79`). But **any future production hash taken over the raw `AnalystScoreTemplate` would be non-deterministic** unless `scoredAt` (and peers) are stripped or injected out-of-band. Doctrine: volatile stamps like `scoredAt` MUST live **outside** the hashed canonical form (or be excluded by `CanonicalHash v1`), never embedded in the object being content-addressed.

### 4.4 Number policy — [PROPOSED] field-specific (the crux)

**[PROPOSED] Ban raw IEEE-754 floats (and transcendentals) in any hashed canonical form.** Today every off-chain hasher relies on default `JSON.stringify` number serialization, so any float drift propagates directly into the digest. The policy is **field-specific**:

- **(i) Money / emissions → integer base units.** Represent monetary and emission quantities as **integer base units** (e.g. wei) using integer/decimal math — **never** `float × 1e18` then floor. The concrete anti-pattern to ban: `EmissionsMintDataProvider.calculateTokenAmount` computes `const amountWei = BigInt(Math.floor(adjustedAmount * 10 ** this.config.decimals))` (`afi-mint/src/adapters/EmissionsMintDataProvider.ts:284`, `decimals = 18`), i.e. multiplies a float by `1e18` in double precision (≈15–16 significant digits) before flooring — so the low ~3 digits of an 18-decimal wei value are quantization noise.
- **(ii) Prices / levels → fixed-precision decimal strings.** CPJ trade levels and any price/level fields MUST be canonicalized to **decimal strings at a fixed, declared precision** (canonical quantization), not floats.
- **(iii) Scores / indicators → fixed-precision decimal strings or documented bucketed integers.** UWR scores and indicator values MUST be emitted at fixed precision or as explicitly documented bucketed integers.

**Backed by the afi-math Wave 2 audit.** Emissions are `number[]` (float64) throughout — the lone `bigint cap` is downcast on entry (`const cap = Number(p.cap)`, `afi-math/src/emissions/emissionsSchedule.ts:15,42,116`) — and the curves/decay modules rely on `Math.exp/log/pow/tanh` (`afi-math/src/curves/curves.ts:26,60,74,91,107`). The Wave 2 audit (`afi-math/docs/AFI_MATH_WAVE2_AUDIT.md`, §3; distilled in `library/reference-afi-math-wave2-audit.md`) finds these transcendentals are **not guaranteed bit-identical across JS engines/libm versions** and states this is **"a significant technical risk for any scheme that hashes or content-addresses emitted values."** Hence: keep transcendental/float math out of anything hashed, and content-address only quantized integer/fixed-precision representations.

### 4.5 The four current hash paths — [PROPOSED] deprecate only the shallow TradingView `ingestHash`

There are **four** distinct hash paths today; they are materially different and must be described distinctly. Critically, the two production `ingestHash` functions are **not** the same discipline — the CPJ one is recursive/lossless, the TradingView one is shallow/lossy — so the deprecation applies to **only** the TradingView variant.

| Path | Location (`origin/main`) | Discipline | Prod? |
|---|---|---|---|
| pipehead `canonicalHash` | `afi-reactor/src/pipeheads/canonicalHash.ts:34-70` | recursive key-sort + sha256; strips `EXCLUDED_TIMESTAMP_KEYS` recursively; `buildScoringProjection` backs `outputHash` | **POC only** |
| CPJ `ingestHash` | `afi-reactor/src/uss/cpjMapper.ts:222-256` | **recursive / lossless** — `canonicalizeCpjForHashing` normalizes entry `{min,max}` + sorts TP/SL, then `sortKeys` recurses at all depths + sha256 | **production** ingest |
| TradingView `ingestHash` | `afi-reactor/src/uss/tradingViewMapper.ts:50-53` | **shallow / lossy** — `JSON.stringify(payload, Object.keys(payload).sort())` array-**replacer** allow-list: only top-level keys govern, nested keys not in that set are silently dropped → collision risk | **production** ingest |
| on-chain role/leaf hashing | `afi-token/src/AFIToken.sol:32`, `AFIMintCoordinator.sol:14`, `AFISignalReceipt.sol:13` | **keccak256** — different hash family/domain | on-chain |

**[PROPOSED] Deprecate the shallow/lossy TradingView `ingestHash`.** Its second `JSON.stringify` argument is an **array replacer** (an allow-list of property names) built from `Object.keys(payload).sort()` — only the **top-level** keys. That allow-list is applied at every nesting level, so any nested property whose name is not also a top-level key is **silently erased** from the hash (two different nested `enrichmentProfile` objects can hash equal). Migrate all ingest hashing to `CanonicalHash v1`; keep `ingestHash` only as a clearly-labeled **non-canonical dedupe/integrity aid** (`ingestHash?: string` on USS provenance, `afi-reactor/src/uss/ussValidator.ts:42`; consumed for dedupe by the webhook server) until migration completes.

**[PROPOSED] Do NOT generalize the criticism to the CPJ `ingestHash`.** The CPJ path is a **different, stronger** discipline: `canonicalizeCpjForHashing` normalizes field semantics (entry range → `{min,max}` with `min ≤ max`, TP/SL arrays sorted, `cpjMapper.ts:159-193`) and `sortKeys` **recursively** sorts object keys at all depths (`cpjMapper.ts:229-250`) before `sha256` (`:253-255`). It is recursive and lossless; the "shallow/lossy" critique is **specific to TradingView** and must not be applied to CPJ. (The CPJ `ingestHash` still lacks domain separation and the number policy, so it too should eventually adopt `CanonicalHash v1`, but it is **not** deprecated for losing data.)

### 4.6 Production scoring is hash-free (accurate posture) — [Canonical] observation

Production **scoring** computes **no content hash at all**. The canonical-hashing machinery — `canonicalHash`, the audit record, and the reputation receipt — lives **only** under `afi-reactor/src/pipeheads/**` (POC), and every consuming record self-labels `demoOnly: true` (`afi-reactor/src/pipeheads/auditPipehead.ts:80`). The only hash on the production path is `ingestHash` (dedupe/integrity), computed at ingest by the two mappers (`tradingViewMapper.ts:99,109`; `cpjMapper.ts:300,313`) and consumed by the webhook server for duplicate detection — never for scoring or commitment. Any D2 provenance/commitment work is therefore **greenfield on the production path**, not a modification of an existing production hash.

### 4.7 Objects to hash-commit in D2 — [PROPOSED] inside `ProvenanceRecord v1`, no anchoring

**[PROPOSED]** District 2 should compute and carry the following hash commitments as **computable commitments inside `ProvenanceRecord v1`** (§3.3, §9), each produced by `CanonicalHash v1` under its own domain tag (§4.2):

- **signal (USS) `contentHash`** — a `CanonicalHash v1` over the canonical USS content (domain `AFI:signal:v1`);
- **evidence hashes (`EvidenceRef v1`)** — payload/evidence hashes for each referenced piece of evidence (domain `AFI:evidence:v1`);
- **`ScoredSignal v1` projection hash** — over the thin scored projection (domain `AFI:scored:v1`), formalizing today's `outputHash`-over-`buildScoringProjection` pattern (`canonicalHash.ts:88-99`);
- **`EnrichmentProvenance v1` hash** — over the lane-provenance carrier that preserves the per-lane attribution normalize currently destroys.

**[Canonical] No on-chain anchoring in D2.** These are **off-chain computable commitments only**. District 2 introduces **no** Layer-1 anchoring, Merkle aggregation, or on-chain publication of these hashes (there is no Merkle/`evidenceHash` aggregation structure in the org today, and none is added here). Alignment of `ProvenanceRecord v1` to the canonical `signalLeaf`/`evidenceLeaf` so a *future* settlement layer could consume them is covered in §9; the actual anchoring remains out of scope.

### 4.8 Concrete illustration — the `golden.json` re-pin

The DR-002 canonical-indicator-kernel switch (Mission 1.5-B) re-pinned the pipehead golden fixture's **`bundleHash`** while the scoring outputs held steady, which is exactly why *what* you hash and the number policy both matter:

| Field in `test/pipeheads/fixtures/golden.json` | Value (`origin/main`) |
|---|---|
| `bundleHash` (before, simple kernel) | `c75a1860df037619f257af024f8b0a3fc3ef057950bf9e36477c3c6a1d1add31` |
| **`bundleHash` (after, canonical Wilder kernel — RE-PINNED)** | **`6e2c91560da14bfca98bb49d83581db9519bd15962b80cf7142b65d1255da948`** |
| `inputHash` (unchanged) | `92258c5bea8c613238c1f2f7f746c99084251510195682cbaf4cf39884e2422d` |
| `outputHash` (unchanged) | `4b6dd610cba2b64831b0aa2a9e27707908affdf8134ca77d1083535de78ad8dc` |
| `uwrScore` (unchanged) | **`0.1875`** |
| `uwrAxes` (unchanged) | `structure 0.15 / execution 0 / risk 0.2 / insight 0.4` |

The change is documented at `afi-reactor/docs/PIPEHEAD_SYSTEM.md:210-211` (`c75a1860…` → `6e2c9156…`) and the fixture is at `afi-reactor/test/pipeheads/fixtures/golden.json`. The **`bundleHash` moved** (it commits the full enriched bundle, whose EMA/RSI/ATR numbers changed when the canonical Wilder kernel replaced the simple-average helper), while **`outputHash` and `uwrScore` (0.1875) held steady** because the scoring projection is insulated: the UWR landed on the same discrete value over the canonical indicators for that fixture. Lesson: a content hash is only as deterministic as the numbers it covers — the bundle hash is **kernel/number-sensitive**, so `CanonicalHash v1` (what you hash) and the field-specific number policy (§4.4) are both prerequisites for stable content addressing.

---

## 5. Source Disclosure & Transparency Metadata

District 1's pipehead proved deterministic scoring over a USS/CPJ input, but the signal record that reaches the analyst — and any future evaluator — carries almost nothing about *where its evidence came from, how it was disclosed, under what license, or how replayable it is*. District 2's job here is narrow and deliberately bounded: **define the descriptive transparency metadata District 2 should represent**, as computable fields and enums on the provenance/disclosure carrier — and explicitly **stop short** of defining how an evaluator weights that metadata or what reward/reputation consequences follow. Every recommendation in this section is **[PROPOSED]**; the metadata shape is `SourceDisclosureProfile v1` (named in §3.3), and its evidence-reference companion is `EvidenceRef v1`.

### 5.1 Scope boundary — what D2 owns, what it does not

**[PROPOSED] Three-way delineation (the load-bearing statement for this section):**

| Layer | Owner | What it does | What it does NOT do |
|---|---|---|---|
| **D2 transparency metadata** | District 2 (this report) | Defines *computable, descriptive* per-source/per-evidence fields and enums (source class, disclosure level, withheld reason, license constraint, replayability, hashes, freshness, attestation, summaries) that an evaluator *can* read | Does not define evaluation weights, scores, or any reward/reputation consequence |
| **Evaluation weights** | BenchKit | Owns the tunable weighting engine that would score/weight transparency metadata once it exists | Does not define the metadata vocabulary; consumes whatever D2 surfaces |
| **Reward / reputation consequences** | Deferred (out of D2 M0) | — | Not specified here; any reputation/reward implication of a disclosure level is a later, owner-approved decision (settlement is frozen — §9) |

This mirrors the existing settlement doctrine that disclosure is **visibility-only** and "MUST NOT gate, accelerate, or condition any reward payment" (DSC-3, `afi-docs/specs/AFI_SETTLEMENT_V1_MANIFEST_AND_PROVENANCE_SCHEMA.md:309`; DISC-4, `afi-docs/specs/AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md:88`): D2 makes disclosure *describable*, it does not make disclosure *consequential*. **No BenchKit weights are defined in this report.**

### 5.2 Current state — BenchKit ingests a market-only CSV and owns a weighting engine, but has zero transparency metadata

BenchKit is a deterministic validator benchmarking/verification toolkit. Its input is a **flat CSV**, not any AFI signal envelope: the recognized header vocabulary is market/statistics fields only — `time`, `symbol`, `side`, `confidence` (aliases `score`/`strength`), `ret_1h`, `ret_4h`, `value` (aliases `amount`/`x`) (`afi-benchkit/src/afi_benchkit/io.py:9-16`). The two suites require only those columns: PoI-01 requires `["time","value"]` (`afi-benchkit/src/afi_benchkit/tasks/poi01.py:22`), PoInsight-01 requires `["time","symbol","side","confidence","ret_1h","ret_4h"]` (`afi-benchkit/src/afi_benchkit/tasks/poinsight01.py:25-28`), with `side` mapped buy/long→1, sell/short→−1 (`poinsight01.py:15-20`) and `confidence` clipped to `[0,1]` (`poinsight01.py:44`).

BenchKit already owns a **tunable weighting engine** — the part D2 explicitly does *not* touch:

- composite reputation `reputation_score = alpha*poi_score + beta*poinsight_score`, default `alpha=0.3, beta=0.7, N0=100` (`afi-benchkit/src/afi_benchkit/reputation.py:17-22,65`);
- evidence shrinkage toward neutral 0.5: `w = 1 - exp(-n/N0)`, `poi_score = (1-w)*0.5 + w*poi_raw` (`reputation.py:56-57`);
- PoI composite weights `0.6*success + 0.4*f_L` (`reputation.py:153`);
- PoInsight composite weights IC `0.4`, hit-rate `0.3`, Sharpe `0.3` (`reputation.py:204-218`);
- all weights overridable via env `AFI_BENCHKIT_ALPHA`/`AFI_BENCHKIT_BETA`/`AFI_BENCHKIT_N0` (`reputation.py:258-263`).

But BenchKit reads **no transparency metadata at all**. Its only "provenance" is a **run-level** `Stamp` — `data_hash` (sha256 of the whole dataset file), `cfg_hash`, `git_sha`, `utc_ts` (`afi-benchkit/src/afi_benchkit/stamp.py:13-20`, with `data_hash = sha256(dataset bytes)` at `:25`) — plus a determinism self-check that re-canonicalizes the CSV and compares `sha256` of the output (`poi01.py:120-123`). There is **no per-signal, per-source disclosure, license, source-class, withheld-reason, or attestation field** anywhere in BenchKit's input model or scorer. To evaluate transparency, BenchKit would need new structured per-signal metadata surfaced into its report — today it receives a market-only CSV and computes only capability/usefulness metrics. (The BenchKit↔signal-schema ingestion seam — extend CSV columns vs. teach BenchKit to read the USS/CPJ envelope — is itself an open implementation question this report does not resolve.)

### 5.3 Current state — what disclosure vocabulary already exists (and is NOT enough)

A scoped search across the org finds that almost none of the D2 target vocabulary exists as a structured, BenchKit-ingestable field:

| D2 target field | Already exists? | Location / status (`origin/main`) |
|---|---|---|
| `disclosureLevel` / `disclosureStatus` | **PARTIAL — design-only, on-chain doctrine** | Only `disclosureStatus` with enum **`WITHHELD` → `DISCLOSED`** (`afi-docs/specs/AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md:80-85` DISC-3 table; restated `afi-docs/specs/AFI_SETTLEMENT_V1_MANIFEST_AND_PROVENANCE_SCHEMA.md:296-305`). Intermediate states and exact enum encoding are **OPEN (O6)** (`AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md:87`). It is a binary *status*, not a graded *level*, and it is on-chain-provenance doctrine, not a structured signal-metadata schema BenchKit can read. |
| provider attestation | **PARTIAL — design-only (EAS), not implemented** | `attestationUID` is an EAS field whose existence/format is **OPEN (O6)** (`afi-docs/specs/AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md:67`). No attestation primitive exists in code. |
| `sourceId` / `sourceRef` | **PARTIAL — free-text, not a canonical typed ref** | USS v1.1 `provenance.source` free-text (`afi-config/schemas/usignal/v1_1/index.schema.json:241-244`), `providerId` (`:245-248`), `providerRef` free-form (`:267-270`); CPJ `provenance.providerId` (`afi-config/schemas/cpj/v0_1/core.schema.json:34-38`); infra `source: string` (`afi-infra/src/tssd/types.ts:49`). No canonical, typed `sourceId`/`sourceRef` on the scored-signal record that an evaluator can read. |
| `payloadHash` / `evidenceHash` | **PARTIAL — optional/uncomputed or doctrine-only** | `payloadHash?: string` optional and **never computed** by the gateway writer (`afi-infra/src/tssd/types.ts:53`); `contentHash`/`scoreCommitment`/`evidenceHash` are doctrine-only Merkle-leaf commitments (`afi-docs/specs/AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md:102-103,122`, signalLeaf/evidenceLeaf). |
| `fetchedAt` / `asOf` / freshness | **PARTIAL — exist scattered, no freshness field on evaluator input** | `fetchedAt` in reactor price types (`afi-reactor/src/adapters/exchanges/types.ts:139`) and news node (`afi-reactor/src/dag/plugins/NewsNode.ts:81`); `asOf` on USS v1.1 (`afi-config/schemas/usignal/v1_1/index.schema.json:69`, greeks `core.schema.json:168`); RAW `receivedAt` (`afi-infra/src/tssd/types.ts:47`). No freshness field reaches BenchKit. |
| existing `provenance` objects (lineage, not transparency) | **present but not transparency metadata** | USS v1.1 `provenance` (required `source`/`providerId`/`signalId`, plus `ingestedAt`/`ingestHash`/`providerType`/`datasetId`/`codeCommit`/`seed`/`timestamp`, `additionalProperties:true`, `afi-config/schemas/usignal/v1_1/index.schema.json:232-294`); CPJ `provenance` (required `providerType`/`providerId`/`messageId`/`postedAt`, optional `rawText`/`channelName`/`authorId`/`authorName`, `additionalProperties:true`, `afi-config/schemas/cpj/v0_1/core.schema.json:19-64`). These are **source-of-origin / lineage** envelopes, not transparency-scoring metadata — none of the D2 target concepts (`sourceClass`, `disclosureLevel`, `withheldReason`, `licenseConstraint`, `replayabilityLevel`, `qualityClaim`) appear in them. |
| `sourceClass` | **ABSENT** | No `sourceClass`/`source_class` trust enum anywhere. Closest is *platform/venue* typing, not a trust class: CPJ `providerType` enum (`telegram\|discord\|twitter\|other`, `cpj/v0_1/core.schema.json:29-33`); USS `providerType` enum (`tradingview\|manual\|bot\|mcp\|api\|other`, `usignal/v1_1/index.schema.json:262-266`). Neither classifies *transparency/trust*. |
| `withheldReason` | **ABSENT** | `WITHHELD` is a *status* only; no field captures *why* something is withheld anywhere. |
| `licenseConstraint` | **ABSENT** | `license` appears only as npm dependency metadata. No signal/source license-constraint concept. |
| `replayabilityLevel` | **ABSENT (as a field)** | Replayability is an aspirational SLO + audit theme, but there is **no `replayabilityLevel` field/enum**. |
| analyst-visible summary | **ABSENT** | No structured analyst-facing summary field exists. |
| validator-visible summary | **ABSENT** | No structured validator-facing summary field exists. |
| `qualityClaim` | **ABSENT (as a self-declared field)** | No signal carries a self-declared `qualityClaim`. |

**Bottom line:** of the D2 target vocabulary, only `disclosureStatus` (binary `WITHHELD`/`DISCLOSED`, design-only, on-chain doctrine) and hash commitments (`payloadHash` optional-uncomputed; `contentHash`/`evidenceHash` doctrine-only) exist as named concepts — and both live in the on-chain provenance doctrine, not in a structured signal-metadata schema an evaluator can read. `sourceClass`, a graded `disclosureLevel`, `withheldReason`, `licenseConstraint`, `replayabilityLevel`, analyst/validator summaries, and `qualityClaim` are **effectively net-new** definitions D2 must author. (Both USS and CPJ `provenance` are `additionalProperties:true` — `usignal/v1_1/index.schema.json:293`, `cpj/v0_1/core.schema.json:64` — so they are extensible; but extending a lineage object is not the same as defining a dedicated disclosure profile. The envelope recommendation is in §6.)

### 5.4 [PROPOSED] `SourceDisclosureProfile v1` — the descriptive field/enum set

**[PROPOSED]** District 2 should represent the following descriptive fields and enums as a dedicated `SourceDisclosureProfile v1` (named in §3.3), carried alongside the signal/evidence provenance (wrapping strategy in §6; commitment in §9). These are **computable metadata** — each field is either machine-derivable from the ingest/enrich/score path or self-declared by the provider; none is a reward/reputation parameter. Enums below are illustrative defaults for owner review; exact enum encodings are implementation decisions, not fixed here.

| Field | Kind | Illustrative enum / shape | Purpose (descriptive only) |
|---|---|---|---|
| `sourceClass` | enum | e.g. `on-chain-market \| licensed-feed \| open-public \| social-signal \| internal-model \| demo` | Classifies the *transparency/trust class* of a source — distinct from platform/venue typing (CPJ/USS `providerType` name only the channel, not trust). |
| `disclosureLevel` | enum (graded) | e.g. `fully-disclosed \| partially-disclosed \| summary-only \| withheld` | A graded disclosure level — generalizes the binary `disclosureStatus` WITHHELD/DISCLOSED (`AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md:80-85`) into a richer, per-evidence-stage scale. Backward-compatible: WITHHELD/DISCLOSED remain the minimum. |
| `withheldReason` | enum / free-text | e.g. `proprietary \| licensing \| privacy-pii \| regulatory \| pending-window \| other` | Captures *why* a payload is withheld — the field that does not exist anywhere today. Enables an evaluator/analyst to distinguish "secret because proprietary" from "secret because of a disclosure window." |
| `licenseConstraint` | enum / ref | e.g. `none \| redistributable \| non-commercial \| research-only \| attestation-required \| unknown` | Records the licensing constraint on the source/evidence payload — absent today. |
| `replayabilityLevel` | enum | e.g. `fully-replayable \| replayable-with-seed \| replayable-with-data \| non-replayable \| unknown` | Records how reconstructable the evidence is — generalizes the replay SLO concept into a per-evidence field (no such field exists today). Cross-refs the `ReplayProfile v1` overlay (§8). |
| `sourceId` / `sourceRef` | typed string | canonical, typed identifier for the source (replaces free-text `source`/`providerRef`) | A canonical, typed source identifier on the scored-signal record that an evaluator can read — today only free-text `source`/`providerId`/`providerRef` exist (`usignal/v1_1/index.schema.json:241-244,245-248,267-270`). |
| `payloadHash` / `evidenceHash` | hash (string) | `CanonicalHash v1` (§4) over the evidence payload | A computed integrity/hash commitment — today `payloadHash` is optional and **never computed** (`afi-infra/src/tssd/types.ts:53`); `evidenceHash` is doctrine-only (`AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md:122`). Carried via `EvidenceRef v1` (§3.3). |
| `fetchedAt` / `asOf` / `freshness` | timestamp + derived | `fetchedAt` (ISO 8601), `asOf` (the fact's observation time), `freshness` (derived staleness, e.g. age or decay score) | Records when evidence was fetched / what point in time it describes / how stale it is. `fetchedAt`/`asOf` exist scattered (`adapters/exchanges/types.ts:139`, `usignal/v1_1/index.schema.json:69`) but never reach an evaluator; `freshness` as a structured field is net-new. |
| provider attestation | ref / UID | pointer to an attestation (e.g. EAS `attestationUID`) when present | A provider attestation reference — design-only today (`AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md:67`, OPEN O6); D2 represents the *reference* as metadata, not the attestation scheme itself. |
| analyst-visible summary | structured text | a brief, analyst-facing summary of the source/evidence (source class, what it is, key constraints) | A structured summary the **analyst** can read — absent today (the analyst receives only `FroggyEnrichedView` with no disclosure context; §6). |
| validator-visible summary | structured text | a brief, validator-facing summary (commitment pointers, disclosure level, withheld reason, replayability) | A structured summary a **validator** can read for verification — absent today. The two summaries MAY differ (analyst sees context for decision-making; validator sees commitments/flags for verification). |
| `qualityClaim` | optional, self-declared | a provider self-declared quality claim (a *claim*, not a canonical quality policy) | An **optional** self-declared quality claim — absent today. It is a claim an evaluator may weigh, **not** a canonical quality metric or weight; BenchKit would decide any weight (§5.1). |

**[PROPOSED] All twelve rows are descriptive metadata.** None defines a BenchKit weight, a reputation score, or a reward consequence. `disclosureLevel` generalizes the existing binary `disclosureStatus` but does **not** alter its visibility-only semantics (DSC-3, `AFI_SETTLEMENT_V1_MANIFEST_AND_PROVENANCE_SCHEMA.md:309`); a richer disclosure level still MUST NOT gate/accelerate/condition payment. `qualityClaim` is explicitly optional and explicitly a *claim* — D2 does not endorse it as canonical quality policy.

### 5.5 Relationship to the canonical leaves and the envelope

`SourceDisclosureProfile v1` is **descriptive metadata**, not a settlement leaf. It aligns with — but does not duplicate — the canonical `evidenceLeaf` (`signalId`, `evidenceHash`, `stage`, `disclosureStatus`, `AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md:115-124`): the leaf commits a hash + stage + disclosure status; the profile carries the richer descriptive context (source class, withheld reason, license, replayability, summaries) that the leaf deliberately omits. Likewise it sits beside `signalLeaf` (`:93-106`), which carries only commitments and identity references (`producer` is a reference, not PII, `:104`), never validator decisions (`:109`). The profile is carried on the analyst-input envelope (`AnalystInputEnvelope v1`, §6) and its hashes are committed inside `ProvenanceRecord v1` (§9) — it is **not** placed on-chain (no L1 anchoring in D2, §9) and **not** wired into any reward/claim path (settlement frozen, §9).

---

## 6. Analyst Input Envelope

The analyst in this org is the **afi-core Froggy UWR scorer** — `scoreFroggyTrendPullbackFromEnriched` — invoked on the production path by the `froggy-analyst` DAG plugin (`afi-reactor/plugins/froggy.trend_pullback_v1.plugin.ts:34` `async function run(enriched: FroggyEnrichedView)`, `:36` `scoreFroggyTrendPullbackFromEnriched(enriched)`). That scorer receives **exactly one typed argument: a `FroggyEnrichedView`** (`afi-core/analysts/froggy.enrichment_adapter.ts:104`), and nothing else. This section decides how provenance, disclosure, and evidence metadata should reach that analyst surface: push it into the strategy-local view (Option A), or wrap the view in a new protocol envelope (Option B). The recommendation is **[PROPOSED] Option B** — `AnalystInputEnvelope v1`.

### 6.1 Current state — the analyst receives only `FroggyEnrichedView`, which carries no protocol provenance

`FroggyEnrichedView` is **strategy-local** (classified in §3.1): a loose afi-core interface (`froggy.enrichment_adapter.ts:104`) with an untyped `indicators?: Record<string, number | null>` map and an `enrichedView: unknown` seam (`AnalysisBundle.enrichedView`, `afi-reactor/src/pipeheads/types.ts:84`), reactor-stubbed as ambient `any` (`afi-reactor/typings.d.ts:15`). It is produced in production by the enrichment adapter (`afi-reactor/plugins/froggy-enrichment-adapter.plugin.ts:622` `const enriched: FroggyEnrichedView = { … }`) and handed directly to the scorer with **no protocol metadata alongside it**. A field-by-field check against the District 2 transparency/provenance vocabulary (§5) shows the analyst-facing view is blind to every category D2 needs to surface:

| District 2 capability the analyst needs | Present on `FroggyEnrichedView`? | Evidence (`origin/main`) |
|---|---|---|
| **Provider identity** | **NO** (only a coarse producer string) | The type (`froggy.enrichment_adapter.ts:104`) has no provider field. The production adapter attaches a single coarse string `enrichmentMeta.enrichedBy: "froggy-enrichment-adapter"` (`froggy-enrichment-adapter.plugin.ts:635`) and a price-source-only `_priceFeedMetadata.priceSource` (attached as `any`). No per-lane / per-provider identity. |
| **Source disclosure metadata** | **PARTIAL** (news + price crumbs only) | Per-article `news.items[].source`/`url` and runtime `_priceFeedMetadata.priceSource`/`venueType` exist, but **nothing** for sentiment, pattern, or aiMl sources (`froggy.enrichment_adapter.ts:104`). |
| **Licensing / withheld reasons** | **NO** | No such field exists in `FroggyEnrichedView` (`froggy.enrichment_adapter.ts:104`) or in the runtime extras. |
| **Evidence hashes** | **NO** | No hash field on the view. Canonical hashes exist only in the POC `AuditRecord` (`afi-reactor/src/pipeheads/types.ts:108`) / `BundleProvenance.inputHash` (`:72`), and they are **never delivered to the analyst**. |
| **Replay pins** (`datasetId`, `codeCommit`, `seed`, …) | **NO** | No pins on the view. `enrichmentMeta.enrichedAt` is a wall-clock timestamp (`froggy-enrichment-adapter.plugin.ts:636`), not a deterministic replay pin. The POC `inputHash` is the nearest analogue but lives only under `src/pipeheads/**`, not on the production analyst input. |
| **Lane provenance** (which lane produced what) | **NO** (coarse categories only) | The type carries only `enrichmentMeta.categories?: string[]` (which categories ran). Per-field lane attribution and provisional/degraded status are **destroyed at normalize**: `projectTechnical` (`afi-reactor/src/pipeheads/normalizePipehead.ts:196-212`) keeps only `emaDistancePct` + `{ema20,ema50,rsi14,atr14}` and **drops** `trendBias`, `indicatorSource`, `canonicalIndicatorKernel`, and `note` — and the sibling projections drop each lane's `provisional`/`fixtureSource`/`note` likewise. Only the bundle-level `provisionalLanes` array survives, and it is **not** part of `FroggyEnrichedView`. |

**This is the analyst provenance gap.** On the production path the scorer sees the enrichment — the *what* — but never the *where it came from, under what license, how replayable it is, which lane produced each field, or whether any lane was a provisional fixture*. It cannot make a provenance-aware decision, and any future evaluator (BenchKit, §5) that consumes the scored output inherits the same blindness because the transparency metadata never entered the pipeline at the analyst seam.

### 6.2 Option A (metadata into `FroggyEnrichedView`) vs Option B (a new `AnalystInputEnvelope v1`)

| | **Option A — expand `FroggyEnrichedView`** | **Option B — new `AnalystInputEnvelope v1` wrapping the view** |
|---|---|---|
| **What it does** | Add provider identity, `SourceDisclosureProfile`, `EvidenceRef`s, replay pins, and `EnrichmentProvenance` fields directly onto the `FroggyEnrichedView` interface (`froggy.enrichment_adapter.ts:104`). | Define a separate protocol envelope `{ enrichedView, provenance, disclosure, evidence, enrichmentProvenance, replayProfile? }` where `enrichedView` remains the **strategy-local** `FroggyEnrichedView`, unchanged, and the protocol metadata rides alongside it. |
| **Coupling** | Couples protocol metadata to a **strategy-local** shape. `FroggyEnrichedView` is Froggy-specific (it carries Froggy's `technical`/`pattern`/`sentiment`/`news`/`aiMl` blocks) and loose (`indicators` untyped, reactor-stubbed `any`). Protocol-level provenance/disclosure/evidence fields would become fields of a strategy-owned object. | Keeps a **clean seam**: the strategy owns its enrichment view; the protocol owns the envelope. A different strategy's analyst could swap its own local view into the same envelope without touching protocol metadata, and protocol metadata can evolve without disturbing the strategy shape. |
| **Pollution risk** | Pollutes a strategy shape with protocol metadata it was never designed to carry — and the view is **strategy-local**, explicitly **not** a candidate for promotion to canon (§3.1). Expanding a shape this report recommends *not* promoting would bake protocol fields into a non-canonical object. | Leaves `FroggyEnrichedView` untouched (it stays strategy-local, §3.1) and puts the protocol metadata on a **[PROPOSED]** canonical envelope that **is** a promotion candidate — the seam the protocol owns. |
| **Lane-provenance handling** | Would have to retrofit per-lane attribution onto a view whose normalize step **already destroyed** the lane self-labels (`normalizePipehead.ts:196-212`). The view is the wrong place to re-introduce lane provenance — the loss happens *before* the view is built. | Carries `EnrichmentProvenance v1` (§3.3) **on the envelope**, populated upstream of normalize, so the per-lane attribution survives normalization and reaches the analyst regardless of what the strategy view projects. |
| **Analyst contract** | The scorer's typed argument (`run(enriched: FroggyEnrichedView)`, `froggy.trend_pullback_v1.plugin.ts:34`) would have to change shape — every strategy analyst would need its own enrichment view to grow protocol fields. | The scorer continues to receive its strategy view; the envelope is a **protocol-level wrapper** the pipeline hands to the analyst stage, which can read the view for scoring and the metadata for provenance-aware context. The strategy contract is unchanged. |
| **Consistency with §3 / §5** | Contradicts the §3.1 classification (do **not** promote `FroggyEnrichedView` — wrap it) and the §5 disclosure design (a dedicated `SourceDisclosureProfile v1`, not fields bolted onto a strategy view). | Directly implements the §3.1 "do not promote — wrap it" recommendation and the §5 disclosure profile as a carried field of the envelope. |

### 6.3 Recommendation — **[PROPOSED]** Option B: `AnalystInputEnvelope v1`

**[PROPOSED]** Adopt a new **`AnalystInputEnvelope v1`** that **wraps** the strategy-local `enrichedView` (a `FroggyEnrichedView` today, swappable for another strategy's view) alongside protocol-level provenance, disclosure, evidence, and lane-provenance metadata. The envelope is the **protocol-owned seam** between strategy-local enrichment and the analyst; the strategy view stays strategy-local and is never expanded with protocol fields.

**Rationale (the load-bearing points):**

1. **`FroggyEnrichedView` is strategy-local and loose, and this report recommends it stay that way** (§3.1). Pushing protocol metadata into it (Option A) would expand a shape explicitly classified as *not a promotion candidate* — baking canonical concerns into a non-canonical object. Wrapping (Option B) keeps the strategy shape clean and puts the protocol metadata where the protocol owns it.
2. **Lane provenance is destroyed at normalize, before the view is built** (`normalizePipehead.ts:196-212`). The view is the wrong place to recover it. The envelope carries `EnrichmentProvenance v1` (§3.3) populated upstream, so per-lane attribution survives normalization and reaches the analyst regardless of what the strategy view projects.
3. **The analyst contract should not have to change per strategy.** Every strategy analyst would need its own enrichment view to grow protocol fields under Option A. Under Option B the scorer keeps its strategy view; the envelope is a uniform protocol wrapper the pipeline stage hands to the analyst.
4. **Consistency with §5.** The disclosure profile (`SourceDisclosureProfile v1`) is a dedicated shape (§5.4), not a set of fields bolted onto a strategy view. The envelope is its natural carrier.

### 6.4 What the envelope carries (**[PROPOSED]**)

`AnalystInputEnvelope v1` is a **[PROPOSED]** promotion (named in §3.3). Its illustrative shape — exact field-level definitions are an implementation decision, not fixed here — is:

| Field | Kind | Purpose | Cross-ref |
|---|---|---|---|
| `enrichedView` | strategy-local object (`FroggyEnrichedView` today) | the strategy's enrichment, **unchanged** — the *what* the analyst scores | §3.1 (strategy-local) |
| `provenance` | `ProvenanceRecord v1` (ref) | signal/evidence provenance and hash commitments | §3.3, §9 |
| `disclosure` | `SourceDisclosureProfile v1` | per-source disclosure/transparency metadata (source class, disclosure level, withheld reason, license, replayability, freshness, attestation, summaries) | §5.4 |
| `evidence` | `EvidenceRef v1[]` | hash-addressable evidence references (payload/evidence hash + source ref + stage) | §3.3, §4.7 |
| `enrichmentProvenance` | `EnrichmentProvenance v1` | per-lane attribution (lane id, provisional/fixture status, kernel identity, source label) that normalize currently destroys | §3.3 |
| `replayProfile?` | `ReplayProfile v1` (optional) | the stricter D2 replay overlay (facts, datasetId, codeCommit, seed, evidence hashes, source refs) when the signal is D2-conformant | §8 |

**[PROPOSED]** The envelope is **not** placed on-chain (no L1 anchoring in D2, §9) and **not** wired into any reward/claim path (settlement frozen, §9). It is the protocol surface that makes the analyst provenance-aware; the strategy view inside it remains the strategy's own.

---

## 7. CPJ Survival Policy

CPJ v0.1 (Canonical Parsed JSON, §2.3) is a **[Canonical]** schema-backed intermediate input that carries richer trade and author data than USS v1.1 can hold. The CPJ→USS mapper (`afi-reactor/src/uss/cpjMapper.ts:267` `mapCpjToUssV11`) builds the USS literal at `:306-329` and **drops** two classes of CPJ fields that have no USS slot: the **trade levels** (`entry`/`stopLoss`/`takeProfits`/`leverageHint`) and the **author identity** (`authorId`/`authorName`). This section recommends how District 2 should preserve both — not by forcing them into USS `facts` (which is `additionalProperties:false`), but as optional metadata and pseudonymous references respectively. Both recommendations are **[PROPOSED]**.

### 7.1 Current state — CPJ carries trade levels and author identity; the mapper drops both

**Trade levels are defined in CPJ and dropped from USS.** CPJ `extracted` carries `entry` (number or `{min,max}`, `afi-config/schemas/cpj/v0_1/core.schema.json:83-101`), `stopLoss` (`:102-105`), `takeProfits` (array of `{price, percentage?}`, `:106-118`), and `leverageHint` (`:119-122`); the TS type mirrors them (`afi-reactor/src/cpj/cpjValidator.ts:54-60`). They are populated in real examples — e.g. `entry: {min:42500, max:42800}`, `stopLoss: 41800`, `takeProfits: [{price:43500,percentage:50},…]`, `leverageHint: 5` (`afi-config/examples/cpj/v0_1/telegram-blofin-perp.example.json:16,20,21,35`). Yet in the mapper these fields appear **only** inside the ingest-hash canonicalization (`canonicalizeCpjForHashing`, `cpjMapper.ts:159-195` — entry at `:164-171`, takeProfits at `:177-178`, stopLoss at `:188-189`) and are **absent from the USS literal** (`:306-329`): the emitted `facts` carries only `{symbol, market, timeframe, strategy, direction}` (`:322-328`). `leverageHint` is not referenced in the mapper output at all. So the trade levels influence the `ingestHash` but are **not retrievable** downstream — they survive only as hash bits, never as data.

**Author identity is defined in CPJ, populated in examples, and never emitted.** CPJ `provenance` carries optional `authorId` and `authorName` (`afi-config/schemas/cpj/v0_1/core.schema.json:55-62`; TS type `afi-reactor/src/cpj/cpjValidator.ts:47-48`). They are populated in the same real example — `authorId: "user-456"`, `authorName: "TraderAlpha"` (`afi-config/examples/cpj/v0_1/telegram-blofin-perp.example.json:10-11`). Yet a full grep of `cpjMapper.ts` finds **zero** references to `authorId` or `authorName`: the mapper's `provenance` block (`:308-320`) maps `providerType`, `providerId`, `signalId`, `ingestedAt`, `ingestHash`, `providerRef` (from `channelName`), `cpjMessageId`, `cpjPostedAt`, and `cpjParseConfidence` — and **never reads** the author fields. They are populated-but-unused: present in the CPJ input, absent from the USS output.

**Why the loss is schema-enforced, not incidental.** USS `facts` is `additionalProperties:false` (`afi-config/schemas/usignal/v1_1/index.schema.json:31,57`) and defines only `symbol/market/timeframe/strategy/direction` — there is **no schema slot** for entry/SL/TP/leverage, so even ad-hoc attachment of trade levels to `facts` would fail USS validation. USS `provenance` is `additionalProperties:true` (`:293`), so author fields *could* be stashed there as extra keys — but they are not, and `additionalProperties:true` is a tolerance, not a contract. (Note: CPJ has `leverageHint` but **no** position-`size`/notional field, and USS has neither leverage nor size — §2.3 — so §7 recovers only fields that actually exist in CPJ.)

### 7.2 Trade levels — **[PROPOSED]** optional `TradePlan v1` / `SignalLevels v1` metadata

**[PROPOSED]** Preserve CPJ trade levels (`entry`, `stopLoss`, `takeProfits`, `leverageHint`) as **optional `TradePlan v1` / `SignalLevels v1` metadata**, carried alongside the USS signal — **not** forced into USS `facts`.

**Why not into `facts`:** USS `facts` is `additionalProperties:false` (`afi-config/schemas/usignal/v1_1/index.schema.json:57`), so trade levels **cannot** be added there without a schema change (which is out of scope for this docs-only mission and would be an owner decision). `facts` is the replay-canonical ingest metadata (`index.schema.json:31-33`); trade levels are strategy/trade-plan detail, not replay-canonical market metadata, so they belong on a separate optional carrier even if the schema were extended.

**Why optional metadata, not a required field:** CPJ trade levels are themselves optional in the CPJ schema (`core.schema.json:83-121` — none are in `extracted.required`, which is only `["symbolRaw","side"]` at `:69-72`). Many CPJ signals carry no levels. Making them optional metadata preserves the signal when levels are present and degrades cleanly when they are not, without requiring every USS signal to carry a `TradePlan`.

**Where it rides:** `TradePlan v1` / `SignalLevels v1` is a **[PROPOSED]** promotion (named in §3.3). It is optional metadata on the analyst-input envelope (`AnalystInputEnvelope v1`, §6) or on the `ProvenanceRecord v1` (§9), not on USS `facts`. It carries the levels the mapper currently drops, so a downstream analyst/evaluator can see the signal author's intended entry/exit/leverage without altering the canonical USS replay contract. The levels MUST be canonicalized under the §4.4 number policy (prices/levels → fixed-precision decimal strings) if they are ever hash-committed.

### 7.3 Author identity — **[PROPOSED]** pseudonymous `authorRef` / `authorHash`

**[PROPOSED]** Preserve CPJ author identity (`authorId`/`authorName`) as a **pseudonymous `authorRef` / `authorHash`** — **not** raw, and **not** dropped.

**Why pseudonymous, not raw:** Raw author identity may carry **PII and licensing constraints**. A display name like `"TraderAlpha"` (`telegram-blofin-perp.example.json:11`) and a platform user id like `"user-456"` (`:10`) can identify a person; redistributing raw identity in a protocol-level signal record could breach privacy expectations or source-platform licensing terms. A pseudonymous reference — a stable `authorRef` (opaque handle) and/or a `authorHash` (a `CanonicalHash v1`, §4, over the canonical author identity) — preserves the **provenance linkage** (the same author across signals is correlatable) **without exposing raw identity**. This mirrors the §3.7 / §9 principle that `signalLeaf.producer` is a reference, not PII (`afi-docs/specs/AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md:104`): the protocol carries identity *references*, not raw identity.

**Why not dropped:** Today the mapper drops author identity entirely (§7.1), which means the signal loses its human-author provenance — there is no way downstream to attribute a signal to its author or to correlate an author's track record. That is silent data loss (flagged as a risk in §12). Preserving a pseudonymous ref/hash keeps the provenance linkage while respecting privacy/licensing.

**Where it rides:** `authorRef` / `authorHash` is optional metadata carried on the `ProvenanceRecord v1` (§9) or the `AnalystInputEnvelope v1` (§6), not on USS `facts` (which is `additionalProperties:false` and carries no author field). It is **not** placed on-chain (no L1 anchoring in D2, §9) and **not** wired into any reward/claim path (settlement frozen, §9). If the owner later decides to surface raw author identity (e.g. under a disclosure window), that is a separate, explicit decision — the default D2 posture is pseudonymous.

### 7.4 Summary — what survives, and how

| CPJ field | Today (mapper) | **[PROPOSED]** D2 survival | Carrier | Rationale |
|---|---|---|---|---|
| `extracted.entry` | dropped (hash-only, `cpjMapper.ts:164-171`) | optional `TradePlan v1` / `SignalLevels v1` metadata | `AnalystInputEnvelope v1` (§6) or `ProvenanceRecord v1` (§9) | trade-plan detail, not replay-canonical `facts`; `facts` is `additionalProperties:false` |
| `extracted.stopLoss` | dropped (hash-only, `:188-189`) | optional `TradePlan v1` / `SignalLevels v1` metadata | same | same |
| `extracted.takeProfits` | dropped (hash-only, `:177-178`) | optional `TradePlan v1` / `SignalLevels v1` metadata | same | same |
| `extracted.leverageHint` | dropped (not referenced in output) | optional `TradePlan v1` / `SignalLevels v1` metadata | same | same |
| `provenance.authorId` | dropped (never read by mapper) | pseudonymous `authorRef` / `authorHash` | `ProvenanceRecord v1` (§9) or `AnalystInputEnvelope v1` (§6) | privacy/licensing: preserve linkage without raw PII |
| `provenance.authorName` | dropped (never read by mapper) | pseudonymous `authorRef` / `authorHash` | same | same |

All six rows are **[PROPOSED]** — new defaults offered for owner decision (§10). Nothing here is adopted; the canonical USS `facts` contract (`additionalProperties:false`) is unchanged, and no schema/code/runtime change is made by this report.

---

## 8. Replay Profile Policy

Replayability — the ability to re-derive a signal's scored output from a pinned set of inputs — is an aspirational SLO and audit theme across the org, but there is **no structured replay profile** on any current signal record. USS v1.1 is deliberately broad: it defines a `facts` block ("replay-canonical market/strategy metadata populated at ingest time and persisted in TSSD vault for deterministic replay," `afi-config/schemas/usignal/v1_1/index.schema.json:31-33`) and an `additionalProperties:true` `provenance` object (`:293`) that already carries optional legacy replay pins — `datasetId` (`:271-274`), `codeCommit` (`:275-278`), and `seed` (`:279-286`) — but none of these is required, none is enforced as a replay contract, and most production signals omit them. This section recommends keeping USS broad while defining a **stricter D2 overlay** that makes replayability a first-class, verifiable property of D2-conformant provenance records. The recommendation is **[PROPOSED]**; the overlay shape is `ReplayProfile v1` (named in §3.3).

### 8.1 Current state — replay pins exist but are optional, unenforced, and incomplete

| Replay pin | Present on USS v1.1? | Status (`origin/main`) |
|---|---|---|
| `facts` (symbol/market/timeframe/strategy/direction) | **YES — required** | `index.schema.json:31-57`; the replay-canonical ingest metadata block (`:33` description). `additionalProperties:false` (`:57`) — a closed, stable replay contract. |
| `datasetId` | **YES — optional, legacy** | `provenance.datasetId` (`index.schema.json:271-274`), described as "Source dataset identifier (legacy field from v1)." Optional; not required; not enforced as a replay pin. |
| `codeCommit` | **YES — optional, legacy** | `provenance.codeCommit` (`:275-278`), "Code commit hash that generated this signal (legacy field from v1)." Optional; not required. |
| `seed` | **YES — optional, legacy** | `provenance.seed` (`:279-286`), "Random seed for reproducibility (legacy field from v1)." Optional; typed `string \| number \| null`; not required. |
| evidence hashes | **NO** (doctrine-only) | `contentHash`/`evidenceHash` exist only as Layer 1 provenance-leaf commitments (`AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md:102,122`), not on the USS signal record. `payloadHash` is optional and never computed (`afi-infra/src/tssd/types.ts:53`). |
| source refs (typed) | **PARTIAL — free-text** | `provenance.source` (free-text, `index.schema.json:241-244`), `providerRef` (free-form, `:267-270`). No canonical, typed `sourceRef` on the scored-signal record. |

**The gap:** USS v1.1 *can* carry replay pins, but it does not *require* them, and it lacks evidence hashes and typed source refs entirely. A signal that omits `datasetId`/`codeCommit`/`seed` is perfectly valid USS — but it is **not reproducible**. There is no way today to distinguish a replayable signal from a non-replayable one at the record level. The POC pipehead's `golden.json` fixture (`afi-reactor/test/pipeheads/fixtures/golden.json`) pins `inputHash`/`bundleHash`/`outputHash` for its own determinism self-check (§4.8), but that machinery lives only under `src/pipeheads/**` (POC) and never reaches the production signal record.

### 8.2 Recommendation — **[PROPOSED]** keep USS broad/optional; define a stricter `ReplayProfile v1` overlay

**[PROPOSED]** Keep **USS v1.1 broad and optional** — do not add required replay pins to the canonical USS schema (that would be a schema change, out of scope for this docs-only mission, and would break signals that legitimately lack replay data). Instead, define a **stricter D2 `ReplayProfile v1` overlay** that a signal **opts into** when it claims D2-conformant replayability. The overlay rides on the `AnalystInputEnvelope v1` (§6.4, where `replayProfile?` is already listed as an optional field) and/or on the `ProvenanceRecord v1` (§9), not on USS `facts` (which is `additionalProperties:false` and carries only market/strategy metadata, not replay pins).

**`ReplayProfile v1` — [PROPOSED] required fields for a D2-conformant provenance record:**

| Field | Kind | Purpose | Cross-ref |
|---|---|---|---|
| `facts` | object (USS `facts`) | The replay-canonical ingest metadata (symbol/market/timeframe/strategy/direction) that scopes the signal — already required on USS (`index.schema.json:31-57`). The overlay requires its **presence and invariance** as the replay baseline. | §7.1; USS schema |
| `datasetId` | string | Pinned source dataset identifier — the data snapshot the signal was computed against. Generalizes the optional USS `provenance.datasetId` (`:271-274`) into a **required** D2 pin. | §8.1 |
| `codeCommit` | string (git SHA) | Pinned code commit hash that generated the signal — so the exact scoring/enrichment logic is reproducible. Generalizes the optional `provenance.codeCommit` (`:275-278`) into a **required** D2 pin. | §8.1 |
| `seed` | string \| number \| null | Random seed for reproducibility — **where applicable** (stochastic pipelines). Generalizes the optional `provenance.seed` (`:279-286`) into a required D2 pin when the pipeline uses randomness. Deterministic-only pipelines MAY set `seed: null`. | §8.1 |
| evidence hashes | `EvidenceRef v1[]` (hashes) | Hash-addressable references to each piece of evidence (payload/evidence hash + source ref + stage), so the evidence trail is pinned and verifiable. Absent from USS today (`contentHash`/`evidenceHash` are doctrine-only, `AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md:102,122`). | §3.3 (`EvidenceRef v1`); §4.7; §5.4 |
| source refs | typed `sourceId` / `sourceRef` | Canonical, typed source identifiers (replacing free-text `source`/`providerRef`, `index.schema.json:241-244,267-270`) so the source of each evidence piece is unambiguously pinned for replay. | §5.4 (`SourceDisclosureProfile v1`) |

**[PROPOSED] The overlay is opt-in, not mandatory on all USS signals.** A signal without a `ReplayProfile v1` is still valid USS — it simply does not claim D2-conformant replayability. The overlay is the contract that makes "this signal is replayable" a **verifiable, machine-checkable** property: a verifier that sees a `ReplayProfile v1` can fetch the pinned `datasetId`, check out the pinned `codeCommit`, supply the `seed`, pull the evidence hashes, and re-derive the scored output. Without the overlay, replayability is an unverified aspiration.

### 8.3 Relationship to the hash doctrine and provenance record

`ReplayProfile v1` is the **replay-pin carrier**; the hash commitments it pins (evidence hashes) are produced by `CanonicalHash v1` (§4) under their domain tags (§4.2). The overlay is carried on the `AnalystInputEnvelope v1` (§6.4) and its commitments are recorded inside `ProvenanceRecord v1` (§9), which aligns to the canonical `signalLeaf` (`contentHash`) and `evidenceLeaf` (`evidenceHash`) so a future settlement layer could consume them. The overlay introduces **no** on-chain anchoring (§9) and **no** reward/claim consequence — it is a descriptive replayability contract, not a settlement artifact.

---

## 9. Settlement & Validator Boundary

This section defines the boundary between District 2's provenance/disclosure work and the Settlement v1 manifest draft. The position is firm and deliberately conservative: **keep the settlement manifest draft frozen**, align `ProvenanceRecord v1` to the canonical `signalLeaf`/`evidenceLeaf` so a *future* settlement layer can consume D2 provenance, introduce **no** Layer-1 anchoring/rewards/claims/settlement/vault mechanics into D2, keep disclosure **visibility-only**, and **defer** validator-decision schemas as **[OPEN]**. Every claim is verified on `origin/main`.

### 9.1 Settlement manifest draft stays **frozen [Canonical]**

**[Canonical]** The Settlement v1 consolidation spec remains **DRAFT — not yet Accepted** (`afi-docs/specs/AFI_SETTLEMENT_V1_MANIFEST_AND_PROVENANCE_SCHEMA.md:3`), and its companion JSON Schema is explicitly a "DRAFT, non-implementation" schema (`afi-config/schemas/afiEpochSettlementManifest.draft.schema.json:4` title, `:6` `x-afiStatus: "draft-non-implementation"`). The *shapes* it restates are canonical — sourced from the Accepted Layer 3 spec (`afi-docs/specs/AFI_EPOCH_SETTLEMENT_MANIFEST.md:3` `**Status:** CANONICAL — Accepted (v1 doctrine)`) — but the consolidation document itself and every encoding are DRAFT/OPEN. District 2 does **not** resolve, implement, or promote any of its open items (O1–O8, S-A…S-D, `AFI_SETTLEMENT_V1_MANIFEST_AND_PROVENANCE_SCHEMA.md` §12).

**[Canonical]** The manifest's four roots are proof-plane commitments plus a single money root:

| Root | Plane | Commits | Status (`origin/main`) |
|---|---|---|---|
| `signalRoot` | proof | Merkle/EAS root over qualified **signal leaves** (§5.1) | Canonical (`AFI_SETTLEMENT_V1_MANIFEST_AND_PROVENANCE_SCHEMA.md:110`) |
| `evidenceRoot` | proof | Merkle root over **evidence leaves** (§5.2) | Canonical (`:111`) |
| `strategyRoot` | proof | Merkle root over strategy/epoch reputation set (§5.3) | Canonical root; leaf PROPOSED (`:112`) |
| `claimRoot` | **money** | Merkle root over **claim leaves** (§5.4) — `(recipient, role, amount, …)`. **The only payout authority.** | Canonical content (`:113`) |

**Load-bearing law [Canonical]:** proof roots confer **no** entitlement; `claimRoot` is the only crossing to money, gated by human/governance authorization. Provenance ≠ payout. District 2 touches **none** of these roots — it aligns its `ProvenanceRecord v1` *fields* to the canonical leaf shapes so future settlement *could* consume them, but it does not build, commit, or anchor any root.

### 9.2 `ProvenanceRecord v1` aligned to canonical `signalLeaf` / `evidenceLeaf` — **[PROPOSED]**

**[PROPOSED]** Align `ProvenanceRecord v1` (the promoted concept behind the POC `AuditRecord`, §3.3) to the **canonical** Layer 1 leaf shapes so a future settlement layer can consume D2 provenance without redesign. The alignment reuses canonical field names verbatim and preserves the canonical scoping and content-commitment semantics. The canonical sources are the Accepted Layer 1 spec (`AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md`), restated in the DRAFT consolidation spec (`AFI_SETTLEMENT_V1_MANIFEST_AND_PROVENANCE_SCHEMA.md` §5.1–§5.2).

**`signalLeaf` — CANONICAL (Layer 1 §6, `AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md:93`)** — `ProvenanceRecord v1` signal-side fields align to:

| `signalLeaf` field | `ProvenanceRecord v1` alignment | Canonical meaning (`AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md`) |
|---|---|---|
| `signalId` | carry verbatim | Stable unique id (`:99`) |
| `strategyId` | carry verbatim | Producing strategy; MUST equal batch `strategyId` (`:100`) |
| `epochId` | carry verbatim | Epoch signal qualified in; MUST equal batch `epochId` (`:101`) |
| `contentHash` | carry verbatim | Hash binding canonical off-chain content (raw + enriched) (`:102`) |
| `scoreCommitment` | carry verbatim — a **commitment (hash)** to the deterministic score/decision; the score itself stays off-chain (`:103`) | Commitment, never cleartext score |
| `producer` | carry verbatim — identity **reference** (ref/id/address ref, not raw PII); confers **no** token entitlement (`:104`) | Reference, not PII |
| `timestamp` | carry verbatim | Authoritative time reference (e.g. scored-at) (`:105`) |
| `rulesetHash` | carry verbatim | Ruleset version under which signal was scored/qualified (`:106`) |

**`evidenceLeaf` — CANONICAL (Layer 1 §7, `AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md:115`)** — `ProvenanceRecord v1` evidence-side fields align to:

| `evidenceLeaf` field | `ProvenanceRecord v1` alignment | Canonical meaning (`AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md`) |
|---|---|---|
| `signalId` | carry verbatim | Signal this evidence pertains to; MUST match a `signalLeaf` `signalId` (`:121`) |
| `evidenceHash` | carry verbatim | Hash of the lifecycle evidence snapshot (`:122`) |
| `stage` | carry verbatim | Lifecycle stage: `RAW` / `ENRICHED` / `SCORED` (`:123`) |
| `disclosureStatus` | carry verbatim | Disclosure state of this snapshot; MAY differ per stage (`:124`) |

**[Canonical] Scoping and content laws preserved:** `signalId + strategyId + epochId` uniquely scope a leaf within a batch (`AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md:110`). The signal leaf **MUST NOT** contain the raw payload, cleartext score, **validator decisions**, or UWR axis values — only `contentHash` and `scoreCommitment` over them (`:109`). The evidence leaf **MUST NOT** carry snapshot contents — only `evidenceHash` (`:128`). `ProvenanceRecord v1` inherits these constraints verbatim.

**[PROPOSED]** `ProvenanceRecord v1` is a **[PROPOSED]** promotion (named in §3.3). It is **not** the frozen POC `AuditRecord` demo shape (`afi-reactor/src/pipeheads/types.ts:108`, self-labeled `demoOnly: true`); it is the promoted *concept*, redesigned to align with the canonical leaves and to carry the D2 hash commitments (§4.7). It is **not** placed on-chain and **not** wired into any reward/claim path.

### 9.3 No Layer-1 anchoring, rewards, claims, settlement, or vault — **[Canonical]**

**[Canonical]** District 2 introduces **none** of the following:

- **No Layer-1 anchoring** — no EAS attestation, no committed Merkle root, no `attestationUID`, no commitment/anchor contract, no manifest commit. The EAS anchoring model (spec §9) is direction-locked but encoding-OPEN (O6); D2 does not implement it. The v0 `AFIMintCoordinator.mintForSignal` flow — which mints reward + ERC-1155 `AFISignalReceipt` in a single call — is **not** the v1 anchor and **MUST NOT** be wired (EAS-7, `AFI_SETTLEMENT_V1_MANIFEST_AND_PROVENANCE_SCHEMA.md:389`). The precise commitment/anchor contract ("SettlementCoordinator") is to-be-specified and explicitly **not** `AFIMintCoordinator` (`:406`).
- **No rewards, minting, or funding** — no `totalRewardPool`, no `claimRoot`/claim leaves, no `mintEligible`/`mintForSignal`/`AFIMintCoordinator` wiring, no ERC-1155/ERC-6909 receipt issuance.
- **No claims or vault** — no `claimLeaf` (`recipient`/`role`/`amount`), no `roleAllocationRoots`/`roleAllocationLeaves`, no vault custody. The claim leaf is a **money-plane** shape (`AFI_SETTLEMENT_V1_MANIFEST_AND_PROVENANCE_SCHEMA.md:233-244`); D2 does not touch it.
- **No settlement** — the manifest draft stays frozen (§9.1); no open item is resolved.

**[Canonical] Boundary law (BND-1):** raw per-signal arrays, cleartext scores, UWR axes, **validator decisions**, or evidence blobs MUST NOT be written on-chain — only roots, `rulesetHash`, `disclosureWindow`/`disclosureStatus`, and pointers (`AFI_SETTLEMENT_V1_MANIFEST_AND_PROVENANCE_SCHEMA.md:280`). D2's off-chain `ProvenanceRecord v1` carries only content commitments (`contentHash`, `scoreCommitment`, `evidenceHash`), never cleartext scores or validator decisions — consistent with BND-1.

### 9.4 Disclosure is visibility-only — **[Canonical]**

**[Canonical]** Disclosure — `disclosureWindow` / `disclosureStatus` / `disclosureURI` — relates to **provenance visibility only**. It **MUST NOT gate, accelerate, or condition any reward payment** (DSC-3, `AFI_SETTLEMENT_V1_MANIFEST_AND_PROVENANCE_SCHEMA.md:309`; restated DISC-4, `AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md:88`). Payout-affecting windows (`challengeWindow`, `holdbackPolicyRef`) are a distinct Layer 3/4 concern, separate parameters from `disclosureWindow`.

**[Canonical]** This boundary carries directly into D2's `SourceDisclosureProfile v1` (§5): a richer `disclosureLevel` (§5.4) generalizes the binary `disclosureStatus` WITHHELD/DISCLOSED but **does not** alter its visibility-only semantics. Disclosure metadata makes provenance *describable*; it does not make disclosure *consequential*. No D2 disclosure field gates, accelerates, or conditions any payment — there is no payment path in D2 to gate (§9.3).

### 9.5 Validator decision schemas deferred — **[OPEN]**

**[OPEN]** Validator-decision schemas (verdict / accept-reject records) are **deferred** unless explicitly owner-approved. District 2 does **not** define, promote, or wire any validator-decision schema.

**Why deferred — no canonical validator-decision schema exists.** There is **no** validator-decision root among the four manifest roots (`AFI_SETTLEMENT_V1_MANIFEST_AND_PROVENANCE_SCHEMA.md:110-113` — only `signalRoot`/`evidenceRoot`/`strategyRoot`/`claimRoot`), **no** validator-verdict leaf, and **no** accept/reject settlement record. In canonical Layer 3, "Validator" appears **only as a payout ROLE** in `roleAllocationRoots` (`AFI_EPOCH_SETTLEMENT_MANIFEST.md:85`) and in the closed claim-leaf role set `Provider | Analyst-Scorer | Validator` (`AFI_SETTLEMENT_V1_MANIFEST_AND_PROVENANCE_SCHEMA.md:241`) — not as a decision artifact. The signal leaf binds only a `scoreCommitment` — "a commitment to the deterministic score/decision … Score stays off-chain" (`AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md:103`) — and **MUST NOT** contain validator decisions (`:109`). BND-1 bars validator decisions on-chain (`AFI_SETTLEMENT_V1_MANIFEST_AND_PROVENANCE_SCHEMA.md:280`). Any on-chain validator-decision or validator-verdict root/leaf would be a new artifact requiring a **separate, owner-approved spec/ADR** and MUST NOT be introduced by D2.

**The only existing validator-decision code is v0/non-canonical and tied to deprecated mint-gating — do NOT wire it.** `afi-core/validators/ValidatorDecision.ts` (header: "ValidatorDecision v0.2 + UWR contracts + Decay Integration," `:1-2`) defines:

- `ValidatorDecisionKind = "approve" | "reject" | "flag" | "abstain"` (`:17`) — a genuine accept/reject verdict enum;
- `ValidatorDecisionBase` (`:91-114`) — `signalId`, `validatorId`, `decision`, `uwrConfidence`, `decayedScore?`, `ageHours?`, `regimeTag?`, `novelty?`, `reasonCodes?`, `notes?`, `createdAt`;
- `ValidatorOutcome` (`:120-127`) — **`mintEligible: boolean`**, `mintReason?`, `replaySessionId?`, `decision`, `scoring?` — i.e. **wired to mint gating**.

The file's own header states it is "Structural envelopes only; emissions/mint/replay wiring live in afi-token / afi-reactor / afi-infra" (`:6`), and its flow positioning says it is "Consumed by validators after scoring and novelty evaluation, **before mint gating**" (`:131`). This is the **v0 mint-gating path** — the same deprecated `mintForSignal` flow that EAS-7 (`AFI_SETTLEMENT_V1_MANIFEST_AND_PROVENANCE_SCHEMA.md:389`) explicitly closes: the v0 `AFIMintCoordinator.mintForSignal` flow "is **not** the v1 attester/anchor and MUST NOT be wired or promoted as such." `ValidatorDecision.ts` is v0/implementation-adjacent, non-canonical, and coupled to that deprecated mint-gating path. **[OPEN]** It MUST NOT be wired as the v1 validator-decision schema. A canonical settlement validator-decision artifact, if one is ever needed, would require a separate, owner-approved spec/ADR — it is not defined here and not defined by D2.

**Signal leaves MUST NOT contain validator decisions.** This is a canonical constraint (`AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md:109`), restated in the consolidation spec ("no raw payloads, cleartext scores, **validator decisions**, UWR axis values, or evidence blobs," `AFI_SETTLEMENT_V1_MANIFEST_AND_PROVENANCE_SCHEMA.md:180`). `ProvenanceRecord v1` inherits this verbatim: its signal-side fields carry `contentHash` and `scoreCommitment` (a commitment to the score, never the cleartext score or a validator verdict) — **never** a validator decision, a cleartext score, or UWR axis values.

### 9.6 Summary — the D2 settlement/validator boundary

| Boundary | Position | Label | Evidence (`origin/main`) |
|---|---|---|---|
| Settlement manifest draft | **FROZEN** — DRAFT, not Accepted; do not resolve O1–O8 / S-A…S-D | **[Canonical]** | `AFI_SETTLEMENT_V1_MANIFEST_AND_PROVENANCE_SCHEMA.md:3`; `afiEpochSettlementManifest.draft.schema.json:4,6`; `AFI_EPOCH_SETTLEMENT_MANIFEST.md:3` |
| `ProvenanceRecord v1` field alignment | Align to canonical `signalLeaf` / `evidenceLeaf` | **[PROPOSED]** | `AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md:93-106` (signalLeaf), `:115-124` (evidenceLeaf); restated `AFI_SETTLEMENT_V1_MANIFEST_AND_PROVENANCE_SCHEMA.md:182-195,199-208` |
| Layer-1 anchoring / rewards / claims / settlement / vault | **NONE in D2** | **[Canonical]** | Four roots `:110-113`; BND-1 `:280`; EAS-7 `:389`; anchor contract `:406` |
| Disclosure | **Visibility-only** — MUST NOT gate/accelerate/condition payment | **[Canonical]** | DSC-3 `AFI_SETTLEMENT_V1_MANIFEST_AND_PROVENANCE_SCHEMA.md:309`; DISC-4 `AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md:88` |
| Validator-decision schemas | **DEFERRED** — no canonical schema exists; existing v0 `ValidatorDecision.ts` is mint-gating, MUST NOT be wired | **[OPEN]** | No verdict root (`:110-113`); signal leaf MUST NOT contain validator decisions (`AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md:109`); `ValidatorDecision.ts:1-2,17,91-127,131`; EAS-7 `:389` |
| Signal leaves vs validator decisions | **MUST NOT** contain validator decisions | **[Canonical]** | `AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md:109`; `AFI_SETTLEMENT_V1_MANIFEST_AND_PROVENANCE_SCHEMA.md:180,280` |

All positions above are firm defaults for owner review (§10). Nothing here is adopted; the settlement manifest draft remains frozen, no anchoring/reward/claim/vault mechanic enters D2, disclosure stays visibility-only, and validator-decision schemas stay deferred.

---

## 10. Owner Decisions Needed

Every firm recommendation in this report is, by construction, a decision the owner must make before any District 2 implementation begins. This section consolidates them into a single enumerated owner-decision list — `D-1` through `D-17` — with one crisp decision per doctrine position. Each row carries the underlying label (`[Canonical]` / `[PROPOSED]` / `[OPEN]`) of the position it restates and a pointer to the section that argues it. The owner's choices here gate the proposed D2 milestones (§11); until decided, every recommendation remains `PROPOSED` (or `OPEN`) and nothing is adopted (§13 guardrails).

| ID | Owner decision (one crisp ask) | Underlying position | Label | Section |
|---|---|---|---|---|
| **D-1** | **Approve the canonical-vs-reactor-local boundary as classified.** Confirm that USS v1.1 and CPJ v0.1 are the only **[Canonical]** schema-backed shapes today, and that `ReactorScoredSignalV1`, `AnalysisBundle`, lane payloads, `FroggyEnrichedView`, `AuditRecord`, demo JSON, and the settlement manifest draft stay reactor-local / strategy-local / demo-only / doctrine-only-frozen respectively. | Boundary classification (six categories) | **[Canonical]** (classifications of existing shapes are factual) | §3.1 |
| **D-2** | **Approve the PROPOSED promotion set with versioned names.** Approve promoting the ten named shapes — `ScoredSignal v1`, `AnalystInputEnvelope v1`, `ProvenanceRecord v1`, `SourceDisclosureProfile v1`, `EvidenceRef v1`, `EnrichmentProvenance v1`, `CanonicalHash v1`, optional `TradePlan v1` / `SignalLevels v1`, and `ReplayProfile v1` — as the D2 canonical-shape roadmap (exact field-level definitions are implementation decisions, not fixed here). | Promotions offered | **[PROPOSED]** | §3.3 |
| **D-3** | **Approve `AnalystScoreTemplate` as the highest-priority promotion (NOT yet canonical).** Approve lifting the Zod schema from afi-core to a canonical JSON-Schema contract in afi-config, enforced (AJV) at the reactor boundary. Confirm it is **not** to be described as already-canonical or protocol-wide schema-backed today. | AnalystScoreTemplate promotion | **[PROPOSED]** | §3.2 |
| **D-4** | **Adopt `CanonicalHash v1` as the single canonical off-chain hash.** Approve recursive key-sort → JSON serialize → sha256 (64-char lowercase hex) as the one off-chain canonical hash, formalizing the pipehead canonicalizer, with on-chain `keccak256` kept as a separate, explicitly-labeled domain. | Single canonical hash function | **[PROPOSED]** | §4.1 |
| **D-5** | **Adopt the canonicalization-version + domain-separation discipline.** Approve binding an explicit `canonicalizationVersion` (e.g. `afi.canon.v1`) into a per-object type+version domain tag (e.g. `AFI:signal:v1`, `AFI:evidence:v1`, `AFI:scored:v1`), closing the current zero-domain-separation gap. | Canonicalization version + domain tag | **[PROPOSED]** | §4.2 |
| **D-6** | **Adopt the domain-aware timestamp policy.** Approve excluding volatile runtime/processing timestamps (`scoredAt`, `issuedAt`, `producedAt`, `normalizedAt`, `startedAt`, `finishedAt`, `at`, `timestamp`) by default while allowing normalized evidence/source timestamps (`asOf`, `fetchedAt`, `postedAt`, `observationTime`) to be included when domain-declared; and approve the `scoredAt`-outside-the-hashed-form fix. | Timestamp policy | **[PROPOSED]** | §4.3 |
| **D-7** | **Adopt the field-specific number policy.** Approve banning raw IEEE-754 floats/transcendentals in any hashed canonical form, with money/emissions → integer base units, prices/levels → fixed-precision decimal strings, scores/indicators → fixed-precision decimals or documented bucketed integers (backed by the afi-math Wave 2 audit). | Number policy | **[PROPOSED]** | §4.4 |
| **D-8** | **Approve deprecating the shallow/lossy TradingView `ingestHash` (only).** Approve migrating all ingest hashing to `CanonicalHash v1`, deprecating the shallow TradingView `ingestHash` as a non-canonical dedupe/integrity aid, while explicitly **not** generalizing that criticism to the recursive/lossless CPJ `ingestHash`. | ingestHash deprecation | **[PROPOSED]** | §4.5 |
| **D-9** | **Approve the hash-committed object set inside `ProvenanceRecord v1` with no on-chain anchoring.** Approve committing the USS `contentHash`, `EvidenceRef` hashes, the `ScoredSignal v1` projection hash, and the `EnrichmentProvenance v1` hash as off-chain computable commitments only — with **no** Layer-1 anchoring in D2. | Hash-committed object set | **[PROPOSED]** (commit set) / **[Canonical]** (no anchoring) | §4.7 |
| **D-10** | **Approve the `SourceDisclosureProfile v1` descriptive metadata set and the D2 / BenchKit / rewards-deferred delineation.** Approve the twelve descriptive fields/enums (§5.4) as computable metadata District 2 represents, and confirm that D2 provides metadata, BenchKit defines evaluation weights, and reward/reputation consequences are deferred. Confirm no BenchKit weights are defined by D2. | Disclosure metadata set + BenchKit boundary | **[PROPOSED]** | §5.1, §5.4 |
| **D-11** | **Approve Option B — `AnalystInputEnvelope v1`.** Approve wrapping the strategy-local `enrichedView` in a new protocol envelope carrying provenance/disclosure/evidence/lane-provenance metadata, rather than expanding the strategy-local `FroggyEnrichedView` (Option A). | Analyst input envelope | **[PROPOSED]** | §6.3 |
| **D-12** | **Approve the CPJ survival policy.** Approve preserving CPJ trade levels (`entry`/`stopLoss`/`takeProfits`/`leverageHint`) as optional `TradePlan v1` / `SignalLevels v1` metadata (not forced into USS `facts`), and preserving author identity (`authorId`/`authorName`) as a pseudonymous `authorRef` / `authorHash` (not raw, not dropped), with the privacy/licensing rationale. | CPJ trade-level + author-ref policy | **[PROPOSED]** | §7.2, §7.3 |
| **D-13** | **Approve the `ReplayProfile v1` overlay.** Approve keeping USS v1.1 broad and optional while defining a stricter D2 `ReplayProfile v1` overlay (facts, `datasetId`, `codeCommit`, `seed` where applicable, evidence hashes, source refs) that a signal opts into to claim D2-conformant replayability. | Replay profile | **[PROPOSED]** | §8.2 |
| **D-14** | **Confirm the settlement manifest draft stays frozen and approve the `ProvenanceRecord v1` leaf alignment.** Confirm the Settlement v1 manifest draft remains DRAFT/frozen (do not resolve O1–O8 / S-A…S-D), and approve aligning `ProvenanceRecord v1` fields to the canonical `signalLeaf` / `evidenceLeaf` so a future settlement layer could consume them. | Settlement-frozen confirmation + leaf alignment | **[Canonical]** (frozen) / **[PROPOSED]** (alignment) | §9.1, §9.2 |
| **D-15** | **Confirm no L1 anchoring/rewards/claims/settlement/vault in D2, and disclosure is visibility-only.** Confirm District 2 introduces none of those mechanics, and that disclosure metadata MUST NOT gate/accelerate/condition any payment. | Non-settlement boundary + disclosure visibility-only | **[Canonical]** | §9.3, §9.4 |
| **D-16** | **Defer validator-decision schemas.** Confirm validator-decision schemas are **[OPEN]** (deferred unless explicitly approved), that the existing v0 `ValidatorDecision.ts` is non-canonical/mint-gating and MUST NOT be wired, and that signal leaves MUST NOT contain validator decisions. | Validator deferral | **[OPEN]** | §9.5 |
| **D-17** | **Authorize District 2 implementation via its own instrument.** Approve a **separate D2 authorization** — a new version of the Pipehead Addendum and/or a separate mission-specific authorization — before any D2 implementation begins. The v0.1 Pipehead Addendum authorizes **only** the first non-production Signal Evaluation Pipehead POC (`AFI_DROID_PIPEHEAD_ADDENDUM.v0.1.md:305`); future Droid factory districts — including provenance — require either a new addendum version or a separate mission-specific authorization (`:307-310`). This M0 report is a planning artifact, **not** an implementation authorization. | D2 authorization instrument | **[OPEN]** (instrument to be chosen) / **[Canonical]** (authorization required) | §13; `AFI_DROID_PIPEHEAD_ADDENDUM.v0.1.md:303-310` |

**Reading the table:** D-1 through D-16 restate the doctrine positions of §3–§9 as crisp owner asks; D-17 is the governance gate. Until the owner decides, every `[PROPOSED]` / `[OPEN]` row stays un-adopted and the report's guardrails (§13) hold. The proposed milestone plan (§11) sequences the implementation work that would follow owner approval of D-2 through D-16 under the D-17 authorization.

---

## 11. Proposed District 2 Milestones

Assuming the owner approves the decision list (§10) and grants a D2 authorization (D-17), the following milestone plan sequences the implementation work. Each milestone builds on the prior one and on the hardened District 1 base (§14). These are **[PROPOSED]** ordering defaults for owner review; exact scope and gates are implementation decisions. No milestone here is authorized or begun by this M0 report.

| Milestone | Name | Scope (builds on prior) | Key outputs | Doctrine drivers |
|---|---|---|---|---|
| **M1** | afi-config schema drafts + tests | Author draft JSON Schemas (Draft-07) in afi-config for the promotion set — `ScoredSignal v1`, `ProvenanceRecord v1`, `SourceDisclosureProfile v1`, `EvidenceRef v1`, `EnrichmentProvenance v1`, `CanonicalHash v1` spec, optional `TradePlan v1` / `SignalLevels v1`, `ReplayProfile v1` — plus positive/negative fixture tests. Lift `AnalystScoreTemplate` to a canonical JSON-Schema contract. No runtime wiring yet. | Draft schemas + test fixtures in afi-config | D-2, D-3 |
| **M2** | Canonical hash unification | Implement `CanonicalHash v1` with the `canonicalizationVersion` + per-object domain tag, the domain-aware timestamp policy, and the field-specific number policy. Migrate the shallow TradingView `ingestHash` to `CanonicalHash v1`; keep the recursive CPJ `ingestHash` distinct but adopt the same version/domain/number discipline. Re-pin any fixtures under the new domain-tagged hash. | Unified `CanonicalHash v1` replacing the fragmented paths | D-4, D-5, D-6, D-7, D-8 |
| **M3** | Reactor production provenance wiring | Wire `ProvenanceRecord v1` (aligned to `signalLeaf` / `evidenceLeaf`) into the reactor production path, carrying the hash-committed object set (USS `contentHash`, `EvidenceRef` hashes, `ScoredSignal v1` projection hash, `EnrichmentProvenance v1` hash) as off-chain computable commitments. No on-chain anchoring. Replace the heavy `ReactorScoredSignalV1` with the thin `ScoredSignal v1` projection at the scored seam. | Production provenance record + thin scored projection | D-9, D-14, D-15 |
| **M4** | Analyst input envelope integration | Implement `AnalystInputEnvelope v1` wrapping the strategy-local `enrichedView` with provenance/disclosure/evidence/lane-provenance metadata. Populate `EnrichmentProvenance v1` upstream of normalize so per-lane attribution survives. Carry `SourceDisclosureProfile v1` on the envelope. | Analyst provenance-aware input surface | D-10, D-11 |
| **M5** | CPJ field survival + replay profile | Implement `TradePlan v1` / `SignalLevels v1` to preserve CPJ trade levels the mapper drops, and a pseudonymous `authorRef` / `authorHash` for author identity. Implement the `ReplayProfile v1` overlay (facts, `datasetId`, `codeCommit`, `seed`, evidence hashes, source refs) as an opt-in D2-conformant replayability contract. | CPJ survival + replay overlay | D-12, D-13 |
| **M6** | Docs + contradiction-register sync | Update afi-docs to reflect the adopted D2 shapes; sync the existing `AFI_CONTRADICTION_REGISTER.md` (`afi-docs` @ `1f3f959`, `specs/AFI_CONTRADICTION_REGISTER.md:1,3`) — express any new D2 doc/code tensions in its six-tension + `C-*` table format and reconcile whether D2 closes/narrows existing rows touching USS validation / the ingest boundary. Finalize this report's status from DRAFT. | Updated docs + contradiction-register reconciliation | D-1..D-16 |

**[PROPOSED] Ordering rationale.** Schemas precede hash unification (M2 needs the `CanonicalHash v1` spec from M1); hash unification precedes provenance wiring (M3 commits via `CanonicalHash v1`); provenance wiring precedes the analyst envelope (M4 carries the `ProvenanceRecord v1` from M3); CPJ survival and the replay overlay depend on the envelope and provenance record (M5); docs and the contradiction-register sync land last (M6 reflects everything adopted). Each milestone is independently reviewable and owner-gated; nothing here authorizes skipping the D-17 authorization.

---

## 12. Risks if Skipped

If the owner declines to act on this report's recommendations (or defers indefinitely), the current state persists and the following risks compound. Each is a concrete, verified consequence of the status quo on `origin/main`, not speculation. All are **[Canonical]** observations of current exposure (the risks are factual); the mitigations referenced are the **[PROPOSED]** doctrine positions above.

- **R-1 — Hash non-determinism (especially emissions float risk) corrupts any future content-addressing or settlement.** **[Canonical]** Today every off-chain hasher relies on default `JSON.stringify` number serialization with **no domain separation** and **no number policy** (§4.2, §4.4). Emissions are `number[]` (float64) throughout (`afi-math/src/emissions/emissionsSchedule.ts:42,44,116`), and the curves/decay modules rely on `Math.exp/log/pow/tanh` (`afi-math/src/curves/curves.ts:26,60,74,91,107`) which the afi-math Wave 2 audit finds are **not guaranteed bit-identical across JS engines/libm versions** — "a significant technical risk for any scheme that hashes or content-addresses emitted values." The concrete anti-pattern `BigInt(Math.floor(adjustedAmount * 10 ** this.config.decimals))` (`afi-mint/src/adapters/EmissionsMintDataProvider.ts:284`, `decimals = 18`) bakes float quantization noise into a wei value. If D2 is skipped, any future content-addressing, provenance commitment, or settlement leaf built on these numbers inherits non-determinism: the same logical value hashes differently across engines, breaking replay, audit, and any Merkle proof that depends on hash stability. **Mitigation:** D-5, D-6, D-7 (§4.2–§4.4).
- **R-2 — Reactor/strategy-local shapes leak into canon.** **[Canonical]** Without an explicit boundary, the heavy `ReactorScoredSignalV1` (`rawUss:any`, `lenses:any[]`, `_priceFeedMetadata` — `afi-reactor/src/types/ReactorScoredSignalV1.ts:25,28,31`) and the loose strategy-local `FroggyEnrichedView` (`enrichedView:unknown`, `afi-reactor/src/pipeheads/types.ts:84`) risk being treated as de-facto canonical simply because they are the shapes the pipeline currently produces. Promoting `any`-typed reactor envelopes or strategy-specific views to protocol canon would bake non-deterministic, un-schema-backed shapes into the protocol's truth layer — exactly the failure mode the boundary (§3) prevents. The `AnalystScoreTemplate` near-miss (Zod in afi-core, reactor-stubbed `any` — §3.2) is the live example of how a real schema can look canonical without actually being protocol-wide. **Mitigation:** D-1, D-2, D-3 (§3).
- **R-3 — Analyst provenance blindness.** **[Canonical]** On the production path the scorer receives **only** `FroggyEnrichedView` (`afi-reactor/plugins/froggy-enrichment-adapter.plugin.ts:622`) with no provider identity, source disclosure, licensing/withheld reasons, evidence hashes, replay pins, or lane provenance (§6.1). The analyst cannot make a provenance-aware decision, and any future evaluator (BenchKit) inherits the same blindness because transparency metadata never enters the pipeline at the analyst seam. Lane provenance is destroyed at normalize (`afi-reactor/src/pipeheads/normalizePipehead.ts:196-212`), so the analyst never learns which lane produced a field or whether it was a provisional fixture. **Mitigation:** D-10, D-11 (§5, §6).
- **R-4 — Silent CPJ data loss.** **[Canonical]** The CPJ→USS mapper drops author identity (`authorId`/`authorName`) and trade levels (`entry`/`stopLoss`/`takeProfits`/`leverageHint`) from USS output — they survive only as hash bits inside `ingestHash` and are never retrievable downstream (§7.1, `afi-reactor/src/uss/cpjMapper.ts:306-329`). This is silent: there is no error, no warning, just absence. The signal loses its human-author provenance (no way to attribute or correlate an author's track record) and its trade-plan detail (entry/exit/leverage the author intended). `authorName: "TraderAlpha"` is populated in CPJ (`afi-config/examples/cpj/v0_1/telegram-blofin-perp.example.json:11`) but never emitted. **Mitigation:** D-12 (§7).
- **R-5 — Replay non-reproducibility.** **[Canonical]** USS v1.1 can carry replay pins (`datasetId`, `codeCommit`, `seed` — `afi-config/schemas/usignal/v1_1/index.schema.json:271-286`) but does not require them, lacks evidence hashes and typed source refs entirely, and most production signals omit them (§8.1). There is no way today to distinguish a replayable signal from a non-replayable one at the record level. A signal that omits the pins is perfectly valid USS but is **not reproducible**. Any future audit/replay/settlement verification that depends on re-deriving a scored output from pinned inputs has no contract to rely on. **Mitigation:** D-13 (§8).

**[Canonical] Compounding effect.** These risks are not independent: hash non-determinism (R-1) undermines any provenance commitment (R-3/R-4 mitigation) and any replay pin (R-5); reactor-local leakage (R-2) would propagate the non-deterministic shapes into the truth layer, making R-1 worse; analyst blindness (R-3) and silent CPJ loss (R-4) mean the provenance record that a replay profile (R-5) would pin is incomplete from the start. Acting on the doctrine positions (§3–§9) closes all five; skipping leaves them compounding.

---

## 13. Non-Production & Non-Settlement Guardrails

This section states the explicit guardrails that bound this report and any D2 implementation that follows it. Every guardrail here is **[Canonical]** — it restates the mission boundaries, the settlement doctrine, and the governance relationship, none of which this report can waive. The section closes by restating the **AFI Agent Boundary** from §3 (required by VAL-OWN-004 / VAL-BND-005).

### 13.1 Non-production guardrails — **[Canonical]**

- **No runtime, schema, or code changes.** This M0 report is **docs-only**. It creates/modifies no code, no JSON schemas, and no runtime/scoring/math/settlement/tokenomics/emissions/rewards/validator/pipehead behavior anywhere. The single writable artifact is this report file on the feature branch. Any D2 implementation that follows owner approval is a separate, separately-authorized body of work (D-17) — this report does not begin it.
- **No L1 anchoring, rewards, claims, settlement, or vault.** District 2 introduces **no** Layer-1 anchoring (no EAS attestation, no committed Merkle root, no `attestationUID`, no anchor contract), **no** rewards/minting/funding, **no** claims or vault custody, and **no** settlement resolution. The settlement manifest draft stays frozen (§9.1). The four manifest roots (`signalRoot`/`evidenceRoot`/`strategyRoot`/`claimRoot`, `AFI_SETTLEMENT_V1_MANIFEST_AND_PROVENANCE_SCHEMA.md:110-113`) are untouched; D2 aligns `ProvenanceRecord v1` *fields* to the canonical leaves so a future settlement layer *could* consume them, but builds, commits, or anchors no root.
- **Recommendations are PROPOSED until owner-approved.** Every substantive recommendation in this report carries a label (`[Canonical]` / `[PROPOSED]` / `[OPEN]`). The `[PROPOSED]` and `[OPEN]` positions are **not adopted** — they are firm defaults offered for owner decision (§10). Nothing in this report is canonical protocol truth by virtue of being written here; only the `[Canonical]` restatements of existing doctrine carry that weight, and they restate doctrine that already governed before this report.
- **D2 implementation needs its own authorization.** The v0.1 Pipehead Addendum authorizes **only** the first non-production Signal Evaluation Pipehead POC (`AFI_DROID_PIPEHEAD_ADDENDUM.v0.1.md:305`); future Droid factory districts — including provenance — require either a new version of the addendum or a separate mission-specific authorization (`:307-310`). This M0 report is a **planning artifact, not an implementation authorization**. No D2 implementation may begin until the owner grants a separate D2 authorization instrument (D-17).

### 13.2 Non-settlement guardrails — **[Canonical]**

- **Disclosure is visibility-only.** Disclosure metadata (`disclosureWindow` / `disclosureStatus` / `disclosureLevel`) relates to provenance visibility only and **MUST NOT gate, accelerate, or condition any reward payment** (DSC-3, `AFI_SETTLEMENT_V1_MANIFEST_AND_PROVENANCE_SCHEMA.md:309`; DISC-4, `AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md:88`). A richer `disclosureLevel` (§5.4) generalizes the binary `disclosureStatus` but does not alter its visibility-only semantics.
- **Provenance ≠ payout.** Recording provenance MUST NOT mint, pay, gate, or accelerate payment (L-SEP-1..L-SEP-4, settlement doctrine). D2's `ProvenanceRecord v1` carries only content commitments (`contentHash`, `scoreCommitment`, `evidenceHash`), never cleartext scores, validator decisions, or claim leaves.
- **Signal leaves MUST NOT contain validator decisions.** (`AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md:109`; BND-1, `AFI_SETTLEMENT_V1_MANIFEST_AND_PROVENANCE_SCHEMA.md:280`). Validator-decision schemas are deferred **[OPEN]** (§9.5); the existing v0 `ValidatorDecision.ts` is non-canonical/mint-gating and MUST NOT be wired.
- **No BenchKit weights defined.** District 2 provides computable transparency metadata; BenchKit defines evaluation weights; reward/reputation consequences are deferred (§5.1). No BenchKit weight is defined in this report.

### 13.3 AFI Agent Boundary — restated from §3 — **[Canonical]**

The boundary doctrine stated at the head of §3 (§3.0) is restated here so the guardrails section carries the full governance framing. Four points:

1. **Pipeheads are deterministic protocol processing stations — fixed, replayable rules, not agent discretion.** The Pipehead Addendum requires that trust-critical AFI logic "remains deterministic, auditable, and governed by explicit protocol rules" (`AFI_DROID_PIPEHEAD_ADDENDUM.v0.1.md:17`) and that "AFI's deterministic modules produce protocol truth" (`:197`); substituting LLM judgment for deterministic scoring (`:110`) is explicitly forbidden. **[Canonical]** — restated governance.
2. **Agents/droids MAY build, configure, inspect, and operate AFI-compatible pipelines.** The Addendum authorizes a droid to "build, maintain, operate, test, monitor, repair, and report on that node's execution surface" (`AFI_DROID_PIPEHEAD_ADDENDUM.v0.1.md:17`) and to "operate AFI pipeline nodes" (`:25`). Droids are the tooling/operators that assemble and run pipeheads. **[Canonical]** — restated governance.
3. **Canonical truth remains in the schemas, deterministic validation, the hash doctrine, provenance records, replay profiles, and documented standards — never in an agent's runtime behavior.** Governance establishes that "AFI's deterministic modules produce protocol truth" (`AFI_DROID_PIPEHEAD_ADDENDUM.v0.1.md:197`) and that "Droids may not become the source of financial truth" (`:326`); the District 2 enumeration of where canonical truth resides is this report's framing of the canon layer that principle protects. **[Canonical]** — principle restated from governance; the canon enumeration is the report's framing.
4. **Agents/droids are users/tooling of the protocol, NOT protocol canon themselves — nothing an agent does becomes canon by virtue of the agent doing it; only the schema / validation / hash / provenance / replay / standards layer is canon.** The Addendum's trust boundary "separates **operation** from **authority**" (`AFI_DROID_PIPEHEAD_ADDENDUM.v0.1.md:193,195,197,199`); the Charter's "Propose, Don't Decide" rule binds droids to proposing via branches and PRs while "Humans (and, where appropriate, AOS-governed workflows) make final decisions" (`AFI_DROID_CHARTER.v0.1.md:90-92`). **[Canonical]** — restated governance (operation ≠ authority); the canon-by-virtue phrasing is the report's framing.

This restatement completes the cross-reference begun by VAL-BND-005 (the §3 statement) and satisfies the §13 portion of VAL-OWN-004: the guardrails section explicitly carries the AFI Agent Boundary — pipeheads are deterministic protocol processing stations, and agents/droids are tooling/operators of AFI-compatible pipelines, not protocol canon themselves.

### 13.4 Storage Boundary / Persistence Profile — **[Canonical]**

The concrete datastore backing the TSSD signal/evidence vault is an **implementation storage backend, NOT protocol canon.** The audit corpus designates MongoDB TSSD as AFI's "canonical reference evidence store," but that designation names the **reference implementation**, not protocol canon — the datastore is swappable, and canon lives in the schema/validation/hash/provenance/replay layer this report defines. Four points:

1. **The TSSD signal/evidence vault is currently backed by MongoDB.** `afi-infra` ships a concrete `MongoTSSDVaultClient` ("T.S.S.D. Vault - MongoDB Implementation (Time-Series)", `afi-infra/src/tssd/MongoTSSDVaultClient.ts:1`) that `implements ITSSDVaultClient` (`:72`) and persists to a native Mongo time-series collection `afi_tssd.tssd_signals` (`afi-docs` @ `1f3f959`, `specs/audit/AFI_EVIDENCE_STORE_DECISION.md:16-17`). The audit inventory records that "MongoDB TSSD is AFI's canonical reference evidence store" (`afi-docs` @ `1f3f959`, `specs/audit/AFI_MONGO_TSSD_INVENTORY.md:3`; reiterated `:13`) and that "MongoDB TSSD is the canonical reference evidence store for AFI" (`afi-docs` @ `1f3f959`, `specs/audit/AFI_EVIDENCE_STORE_DECISION.md:7`) — read here as the **reference-implementation** designation, not a canon claim about the datastore itself. **[Canonical]** — restated implementation posture on origin/main.

2. **The backend sits behind an abstraction and is a swappable operational/implementation choice — a different datastore could replace Mongo without changing protocol canon.** `ITSSDVaultClient` is the vault-operations contract and documents that implementations "may use: In-memory storage (for dev/test), MongoDB time-series collections (for production), Other persistent storage backends" (`afi-infra/src/tssd/TSSDVaultClient.ts:31-34`, interface declared at `:36`). The vault configuration schema enumerates `mongodb`, `postgresql`, `timescaledb`, and `influxdb` as engine choices (`afi-config/schemas/vault.schema.json:14-22`). Mongo is one selectable backend behind the interface, not a protocol fixture. **[Canonical]** — abstraction boundary on origin/main.

3. **Canonical truth resides in the schemas, deterministic validation, the hash doctrine (`CanonicalHash v1`), provenance records, and replay profiles — never in the datastore, its indexes, or its query/serialization behavior.** This is the canon layer enumerated throughout this report (§3 boundary, §4 hash doctrine, §8 replay profile, §9 settlement alignment); the datastore is the persistence substrate that *stores* vaulted records, not the arbiter of what they mean. Mongo's indexes, query semantics, and serialization shape are operational concerns of the implementation, not sources of canonical truth. **[Canonical]** — restated canon-layer framing.

4. **Persistence MUST NOT alter canonical bytes.** What is hashed and committed under the hash doctrine (§4) and the settlement-alignment leaves (§9) is canonical **regardless of how Mongo stores it**, and Mongo-specific encodings (BSON, `ObjectId`, its number/date handling) MUST NOT leak into any canonical hashed form. The Mongo document type projects `createdAt`/`updatedAt` as `Date` (`afi-infra/src/tssd/MongoTSSDVaultClient.ts:55-61`) — a storage-layer concern that must not enter the hashed canonical bytes; the field-specific number policy (§4, integer base units / fixed-precision decimal strings) likewise forbids any BSON/float representation from appearing in a hashed form. **[Canonical]** — persistence-encoding boundary.

---

## 14. Open Questions, Contradictions & Reconciliations

This section records open questions the report does not resolve, and reconciles the stale prior-document language that this report supersedes. Open questions are labeled **[OPEN]**; reconciliations are labeled **[Canonical]** (factual corrections of stale framing against `origin/main`).

### 14.1 Reconciliation — the stale pipehead-report "restore canonical validator/kernel as future work" language is superseded — **[Canonical]**

The District 1 pipehead report (archived in afi-docs git history) was written against the **pre-Mission-1.5-B** state and frames the restoration of canonical USS validation and the canonical indicator kernel as **future work**:

- The executive summary states the two modules "could not be reused **offline**, so self-contained equivalents were used behind clean seams … Both have a documented future restoration path" (pipehead report, executive summary).
- The files-changed table labels `schemaValidationPipehead.ts` as a "Self-contained **OFFLINE structural** USS v1.1 validator (DR-001; NOT canonical `ussValidator`)" (`:39`) and the technical lane/indicators as DR-002 offline helpers (`:40-41`).
- §8 records DR-001 and DR-002 as open limitations with "*Recommended future fix.* Restore canonical USS validation …" (`:214-217`) and "*Recommended future fix.* Restore the canonical indicator kernel …" (`:219-222`).
- §10 "Recommended next mission" proposes: "**Restore canonical USS validation and the canonical indicator kernel (online-enabled).**" (`:243-248`), with step 1 "Restore canonical USS validation (DR-001)" (`:247`) and step 2 "Restore the canonical indicator kernel (DR-002)" (`:248`).

**[Canonical] That future work is DONE — DR-001 and DR-002 are RESOLVED on `origin/main` (Mission 1.5-B).** The pipehead report itself carries two append-only addenda recording the resolution, but the body (§1–§10) still reads as if the restoration is pending. The verified current state on `origin/main`:

- **DR-001 RESOLVED** — `afi-reactor/src/pipeheads/schemaValidationPipehead.ts:28` now delegates to canonical `validateUsignalV11` (`import { validateUsignalV11 } from "../uss/ussValidator.js"`), the AJV + afi-config schema path is live, and the module header states "DR-001 RESOLVED." The real deps `ajv ^8.17.1`, `ajv-formats ^3.0.1`, and `trading-signals ^7.4.3` are present (`afi-reactor/package.json:40-41,50`). The pipehead report addendum records DR-001 resolved, merged via **afi-reactor PR #36 @ `5f8c358`**.
- **DR-002 RESOLVED** — the technical lane now defaults to the canonical Wilder indicator kernel (`trading-signals` v7), with `golden.json` re-pinned (`bundleHash` `c75a1860…` → `6e2c9156…` while `outputHash`/`uwrScore` 0.1875 held steady; §4.8). The pipehead report addendum records DR-002 resolved, merged via **afi-reactor PR #37 @ `069f56c`**, which is the `origin/main` pin this report is written against.

**[Canonical] Reconciliation.** The pipehead report's "restore canonical validator/kernel as future work" language is **stale** — it describes the pre-Mission-1.5-B state. District 2 does **not** re-do that work; it builds on the hardened base. District 1 hardening (Mission 1.5-B) deliberately did **not** touch the three things that are now District 2's scope: (a) the canonical-vs-reactor-local boundary, (b) the unified hash doctrine, and (c) the provenance/disclosure/analyst-input structure (§2.3, §14 of `library/evidence-G-origin-main-delta-reactor.md`). This report treats DR-001/DR-002 as **resolved** throughout (§1, §2.3) and frames District 2 as the boundary/hash/provenance work that builds on the hardened base — never as re-doing District 1's canonical validation/kernel hardening. The M6 milestone (§11) includes syncing the contradiction register (`afi-docs` @ `1f3f959`, `specs/AFI_CONTRADICTION_REGISTER.md:1,3`) so the stale framing is formally reconciled there as well.

### 14.2 Open questions — **[OPEN]**

These are explicitly undecided and are not resolved by this report. Each carries forward to the owner (§10) or to a D2 implementation milestone (§11) under the D-17 authorization.

| ID | Open question | Disposition | Cross-ref |
|---|---|---|---|
| **OQ-1** | **D2 authorization instrument.** Whether D2 implementation is authorized via a new Pipehead Addendum version or a separate mission-specific authorization. | **[OPEN]** — owner decision (D-17). This M0 report is not an authorization. | §13.1; `AFI_DROID_PIPEHEAD_ADDENDUM.v0.1.md:303-310` |
| **OQ-2** | **Validator-decision schema.** Whether a canonical settlement validator-decision artifact is ever needed, and if so what shape it takes (separate owner-approved spec/ADR required). | **[OPEN]** — deferred (D-16). The v0 `ValidatorDecision.ts` is non-canonical/mint-gating and MUST NOT be wired. | §9.5 |
| **OQ-3** | **BenchKit ingestion seam.** Whether BenchKit consumes D2 transparency metadata by extending its CSV columns or by learning to read the USS/CPJ/`AnalystInputEnvelope v1` — an implementation question this report does not resolve. | **[OPEN]** — D2 implementation decision (M1/M4). No BenchKit weights are defined here. | §5.2 |
| **OQ-4** | **Disclosure intermediate states / exact enum encoding.** The on-chain doctrine's `disclosureStatus` intermediate states and exact enum encoding remain OPEN (O6, `AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md:87`); D2's graded `disclosureLevel` generalizes the binary status but the exact encoding is an implementation decision. | **[OPEN]** — D2 implementation decision (M1). Backward-compatible: WITHHELD/DISCLOSED remain the minimum. | §5.3, §5.4 |
| **OQ-5** | **Raw author identity surfacing.** Whether the owner later decides to surface raw author identity (e.g. under a disclosure window) rather than the default pseudonymous `authorRef` / `authorHash`. | **[OPEN]** — separate, explicit owner decision. Default D2 posture is pseudonymous. | §7.3 |
| **OQ-6** | **Contradiction-register sync scope.** Whether M6 "sync" means adding new D2 doc/code tension rows in the register's six-tension + `C-*` format, marking existing rows D2 closes/narrows, or both. | **[OPEN]** — D2 implementation decision (M6). The existing register is an audit-era catalogue, not a per-mission ledger. | §11 (M6); `afi-docs` @ `1f3f959`, `specs/AFI_CONTRADICTION_REGISTER.md:1,3` |

### 14.3 Contradictions noted (not resolved here) — **[Canonical]** observation

This report does not introduce contradictions; it records two pre-existing doc-vs-code tensions it depends on, both already catalogued in the verified inventory, for the M6 sync to reconcile formally:

- **C-1 — CPJ expansion (stale).** The afi-reactor `AGENTS.md:111` expands CPJ as "Canonical **Protocol** JSON," but the canonical schema title is "AFI Canonical **Parsed** JSON - Core (v0.1)" (`afi-config/schemas/cpj/v0_1/core.schema.json:4`) and the mapper header agrees (`afi-reactor/src/uss/cpjMapper.ts:4`). This report uses **Canonical Parsed JSON** throughout (§2.3) and flags the stale expansion for M6 reconciliation.
- **C-2 — Pipehead-report body vs. addenda (stale).** The pipehead report body (§1–§10) frames DR-001/DR-002 as open/future work while its own append-only addenda record them RESOLVED (§14.1). The body is stale relative to `origin/main`; the addenda are current. This report treats the addenda/current state as authoritative and flags the body for M6 reconciliation.

Neither contradiction is resolved by this docs-only report (no doc edits outside this file); both are carry-forward items for the M6 contradiction-register sync (§11) under the D-17 authorization.

---

## Appendix A. Evidence Index

This appendix consolidates the key substantive claims of the report with their `origin/main` `repo/path:line` citations. Every line below was re-derived against the canonical `origin/main` pins recorded in §2.1 (afi-reactor `069f56c`, afi-config `400c167`, afi-core `390b440`, afi-math `a27de91`, afi-factory `59330cc`, afi-docs `5d51d75`) via `git -C <repo> show origin/main:<path> | nl -ba`; line numbers are current to those pins, not copied from the planning evidence files (which were captured against stale local commits). Inline citations in the body repeat these same pointers; this index gathers them in one place for reviewer spot-checking. Citations are grouped by the report section that makes the claim.

### A.1 §2 Baseline & §3 Boundary

| Key claim | Citation (`origin/main`) |
|---|---|
| USS v1.1 self-labels *"v1.1 Runtime Canon"* | `afi-config/schemas/usignal/v1_1/index.schema.json:4` (title) |
| USS `facts` is `additionalProperties:false` (no slot for trade levels/author) | `afi-config/schemas/usignal/v1_1/index.schema.json:57` (`:31` opens the block) |
| USS v1.1 validated by AJV `validateUsignalV11` | `afi-reactor/src/uss/ussValidator.ts:109`; invoked `afi-reactor/src/server.ts:356` |
| CPJ v0.1 titled *"AFI Canonical Parsed JSON - Core (v0.1)"* | `afi-config/schemas/cpj/v0_1/core.schema.json:4` |
| CPJ v0.1 validated by AJV `validateCpjV01` | `afi-reactor/src/cpj/cpjValidator.ts:122`; invoked `afi-reactor/src/server.ts:314` |
| `AnalystScoreTemplate` is a Zod schema in afi-core (not afi-config) | `afi-core/src/analyst/AnalystScoreTemplate.ts:135` (schema), `:31` (interface) |
| `safeParse` enforced only in the afi-core Froggy analyst | `afi-core/analysts/froggy.trend_pullback_v1.ts:262` |
| Reactor stubs `AnalystScoreTemplate` as ambient `any` | `afi-reactor/typings.d.ts:11` |
| `ReactorScoredSignalV1` is heavy (`rawUss:any`, `lenses:any[]`, full `analystScore`) | `afi-reactor/src/types/ReactorScoredSignalV1.ts:25,28,31-37,40` |
| `FroggyEnrichedView` defined in afi-core, reactor-stubbed `any` | `afi-core/analysts/froggy.enrichment_adapter.ts:104`; `afi-reactor/typings.d.ts:15` |
| `FroggyEnrichedView` produced on the production path | `afi-reactor/plugins/froggy-enrichment-adapter.plugin.ts:622` |
| `AnalysisBundle` / `AuditRecord` are POC-only under `src/pipeheads/**` | `afi-reactor/src/pipeheads/types.ts:77` (AnalysisBundle), `:84` (`enrichedView: unknown`), `:108` (AuditRecord) |
| `AuditRecord` built by the POC audit pipehead, self-labeled `demoOnly: true` | `afi-reactor/src/pipeheads/auditPipehead.ts:60,79-80` |
| Settlement manifest draft is DRAFT / frozen | `afi-docs/specs/AFI_SETTLEMENT_V1_MANIFEST_AND_PROVENANCE_SCHEMA.md:3`; `afi-config/schemas/afiEpochSettlementManifest.draft.schema.json:4,6` |
| Layer 3 manifest is CANONICAL-Accepted (the *shapes* the draft restates) | `afi-docs/specs/AFI_EPOCH_SETTLEMENT_MANIFEST.md:3` |

### A.2 §3.0 AFI Agent Boundary (governance)

| Key claim | Citation (`origin/main`) |
|---|---|
| Pipeheads are deterministic; trust-critical logic "governed by explicit protocol rules" | `afi-config/codex/governance/droids/AFI_DROID_PIPEHEAD_ADDENDUM.v0.1.md:17` |
| Droids MAY build/maintain/operate/test/monitor the pipehead execution surface | `AFI_DROID_PIPEHEAD_ADDENDUM.v0.1.md:17,25,27,29` |
| Droid may not silently alter/replace deterministic kernel logic | `AFI_DROID_PIPEHEAD_ADDENDUM.v0.1.md:77` |
| Substituting LLM judgment for deterministic scoring is forbidden | `AFI_DROID_PIPEHEAD_ADDENDUM.v0.1.md:110-111` |
| Trust boundary separates operation from authority | `AFI_DROID_PIPEHEAD_ADDENDUM.v0.1.md:193,195,197,199` |
| "AFI's deterministic modules produce protocol truth" | `AFI_DROID_PIPEHEAD_ADDENDUM.v0.1.md:197` |
| "Droids may not become the source of financial truth" | `AFI_DROID_PIPEHEAD_ADDENDUM.v0.1.md:326` |
| Trust-critical outputs "must remain deterministic, auditable, replayable…" | `AFI_DROID_PIPEHEAD_ADDENDUM.v0.1.md:328` |
| Charter "Propose, Don't Decide": humans make final decisions | `afi-config/codex/governance/droids/AFI_DROID_CHARTER.v0.1.md:90-92` |
| v0.1 Addendum authorizes only the first non-production pipehead POC; future districts need new auth | `AFI_DROID_PIPEHEAD_ADDENDUM.v0.1.md:305,307-310` |

### A.3 §4 Hash Doctrine

| Key claim | Citation (`origin/main`) |
|---|---|
| pipehead `canonicalHash` = recursive key-sort → `JSON.stringify` → sha256 (hex) | `afi-reactor/src/pipeheads/canonicalHash.ts:34` (`canonicalValue`), `:41` (sort), `:65` (`JSON.stringify`), `:70` (sha256 hex) |
| `EXCLUDED_TIMESTAMP_KEYS` = `scoredAt, issuedAt, producedAt, normalizedAt, startedAt, finishedAt, at, timestamp` | `afi-reactor/src/pipeheads/canonicalHash.ts:18-27` |
| `buildScoringProjection` backs `outputHash` (omits `scoredAt`) | `afi-reactor/src/pipeheads/canonicalHash.ts:88-99` |
| Zero domain separation — bare `sha256(JSON)` in all three off-chain hashers | `afi-reactor/src/pipeheads/canonicalHash.ts:65,70`; `afi-reactor/src/uss/cpjMapper.ts:253-255`; `afi-reactor/src/uss/tradingViewMapper.ts:51-52` |
| CPJ `ingestHash` is recursive/lossless (sortKeys at all depths) | `afi-reactor/src/uss/cpjMapper.ts:222` (`generateIngestHash`), `:229-250` (`sortKeys`), `:253-255` (sha256) |
| TradingView `ingestHash` is shallow/lossy (array-replacer allow-list) | `afi-reactor/src/uss/tradingViewMapper.ts:50-52` |
| `ingestHash` consumed for dedupe on the production path | `afi-reactor/src/uss/tradingViewMapper.ts:99,109`; `afi-reactor/src/uss/cpjMapper.ts:300,313` |
| On-chain keccak256 is a separate hash family/domain | `afi-token/src/AFIToken.sol:32`; `afi-token/src/AFIMintCoordinator.sol:14` |
| `scoredAt` written inside the scored object (the hazard) | `afi-core/analysts/froggy.trend_pullback_v1.ts:239` |
| Production scoring is hash-free (canonicalHash/audit/receipt only under `src/pipeheads/**`) | `afi-reactor/src/pipeheads/auditPipehead.ts:80` (`demoOnly: true`) |
| Emissions are `number[]` (float64); lone `bigint cap` downcast on entry | `afi-math/src/emissions/emissionsSchedule.ts:15,42,116` |
| Curves/decay rely on `Math.exp/log/pow/tanh` (not bit-identical across engines) | `afi-math/src/curves/curves.ts:26,60,74,91,107` |
| Anti-pattern `BigInt(Math.floor(adjustedAmount * 10 ** this.config.decimals))` bakes float noise into wei | `afi-mint/src/adapters/EmissionsMintDataProvider.ts:284` |
| Wave 2 audit (transcendentals risk for content-addressing) | `afi-math/docs/AFI_MATH_WAVE2_AUDIT.md` §3 (distilled in `library/reference-afi-math-wave2-audit.md`) |
| `golden.json` re-pin: `bundleHash` `c75a1860…` → `6e2c9156…`; `outputHash`/`uwrScore` 0.1875 held | `afi-reactor/test/pipeheads/fixtures/golden.json:8,15,16,17`; documented `afi-reactor/docs/PIPEHEAD_SYSTEM.md:210-211` |

### A.4 §5 Source Disclosure & §6 Analyst Input Envelope

| Key claim | Citation (`origin/main`) |
|---|---|
| BenchKit ingests a flat market-only CSV (header vocabulary) | `afi-benchkit/src/afi_benchkit/io.py:9-16` |
| BenchKit owns a tunable weighting engine (default `alpha=0.3, beta=0.7, N0=100`) | `afi-benchkit/src/afi_benchkit/reputation.py:17-22,56-57,153,204-218,258-263` |
| `disclosureStatus` binary `WITHHELD`→`DISCLOSED` is design-only, on-chain doctrine | `afi-docs/specs/AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md:80-85`; intermediate states OPEN `:87` |
| Disclosure is visibility-only (MUST NOT gate/accelerate/condition payment) | `afi-docs/specs/AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md:88` (DISC-4); `afi-docs/specs/AFI_SETTLEMENT_V1_MANIFEST_AND_PROVENANCE_SCHEMA.md:309` (DSC-3) |
| `attestationUID` is design-only (OPEN O6) | `afi-docs/specs/AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md:67` |
| Analyst scorer receives exactly one `FroggyEnrichedView` argument | `afi-core/analysts/froggy.enrichment_adapter.ts:104`; `afi-reactor/plugins/froggy.trend_pullback_v1.plugin.ts:34,36` |
| Lane provenance destroyed at normalize (`projectTechnical` keeps only EMA/RSI/ATR) | `afi-reactor/src/pipeheads/normalizePipehead.ts:196-212` |

### A.5 §7 CPJ Survival & §8 Replay Profile

| Key claim | Citation (`origin/main`) |
|---|---|
| CPJ carries trade levels (`entry`/`stopLoss`/`takeProfits`/`leverageHint`) | `afi-config/schemas/cpj/v0_1/core.schema.json:83-122`; TS `afi-reactor/src/cpj/cpjValidator.ts:54-60` |
| CPJ carries optional `authorId`/`authorName` | `afi-config/schemas/cpj/v0_1/core.schema.json:55-62`; TS `afi-reactor/src/cpj/cpjValidator.ts:47-48` |
| Mapper drops author + trade levels from USS output (survive only in `ingestHash`) | `afi-reactor/src/uss/cpjMapper.ts:306-329` (USS literal); canonicalized `:159-195` |
| USS `provenance` is `additionalProperties:true` (tolerance, not contract) | `afi-config/schemas/usignal/v1_1/index.schema.json:293` |
| USS provenance carries optional legacy replay pins (`datasetId`/`codeCommit`/`seed`) | `afi-config/schemas/usignal/v1_1/index.schema.json:271-286` |

### A.6 §9 Settlement & Validator Boundary

| Key claim | Citation (`origin/main`) |
|---|---|
| Settlement manifest draft status DRAFT / not-Accepted | `afi-docs/specs/AFI_SETTLEMENT_V1_MANIFEST_AND_PROVENANCE_SCHEMA.md:3` |
| Four manifest roots (`signalRoot`/`evidenceRoot`/`strategyRoot`/`claimRoot`) | `afi-docs/specs/AFI_SETTLEMENT_V1_MANIFEST_AND_PROVENANCE_SCHEMA.md:110-113` |
| `claimRoot` is the only money root / payout authority | `afi-docs/specs/AFI_SETTLEMENT_V1_MANIFEST_AND_PROVENANCE_SCHEMA.md:113` |
| Canonical `signalLeaf` field list | `afi-docs/specs/AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md:93-106` |
| Signal leaf MUST NOT contain validator decisions / cleartext score / UWR axes | `afi-docs/specs/AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md:109` |
| Canonical `evidenceLeaf` field list | `afi-docs/specs/AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md:115-124` |
| Evidence leaf MUST NOT carry snapshot contents (only `evidenceHash`) | `afi-docs/specs/AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md:128` |
| BND-1: validator decisions MUST NOT be written on-chain | `afi-docs/specs/AFI_SETTLEMENT_V1_MANIFEST_AND_PROVENANCE_SCHEMA.md:280` |
| EAS-7: v0 `AFIMintCoordinator.mintForSignal` is not the v1 anchor, MUST NOT be wired | `afi-docs/specs/AFI_SETTLEMENT_V1_MANIFEST_AND_PROVENANCE_SCHEMA.md:389` |
| Anchor contract "SettlementCoordinator" is to-be-specified, not `AFIMintCoordinator` | `afi-docs/specs/AFI_SETTLEMENT_V1_MANIFEST_AND_PROVENANCE_SCHEMA.md:406` |
| No validator-decision root among the four roots (only payout ROLE) | `afi-docs/specs/AFI_SETTLEMENT_V1_MANIFEST_AND_PROVENANCE_SCHEMA.md:110-113`; `afi-docs/specs/AFI_EPOCH_SETTLEMENT_MANIFEST.md:85` |
| v0 `ValidatorDecision.ts` is non-canonical, tied to mint gating | `afi-core/validators/ValidatorDecision.ts:1-2` (header), `:17` (verdict enum), `:91-114` (base), `:120-127` (`mintEligible: boolean`), `:131` ("before mint gating") |

### A.7 §14 District 1 → District 2 Reconciliation

| Key claim | Citation (`origin/main`) |
|---|---|
| DR-001 RESOLVED: `schemaValidationPipehead.ts` delegates to canonical `validateUsignalV11` | `afi-reactor/src/pipeheads/schemaValidationPipehead.ts:28` |
| Real deps present (`ajv`, `ajv-formats`, `trading-signals`) | `afi-reactor/package.json:40,41,50` |
| DR-002 RESOLVED: canonical Wilder kernel, `golden.json` re-pinned | `afi-reactor/test/pipeheads/fixtures/golden.json:16`; `afi-reactor/docs/PIPEHEAD_SYSTEM.md:210-211` |
| Stale CPJ expansion "Canonical Protocol JSON" (correct = "Canonical Parsed JSON") | `afi-config/schemas/cpj/v0_1/core.schema.json:4` (correct title); `afi-reactor/src/uss/cpjMapper.ts:4` (mapper header) |
| Contradiction register exists for M6 sync | `afi-docs` @ `1f3f959`, `specs/AFI_CONTRADICTION_REGISTER.md:1,3` |

**Spot-check note.** A validator can confirm any row above by running `git -C /home/factory-user/repos/<repo> show origin/main:<path> | nl -ba` and reading the cited line(s). The citations in §A.1–§A.7 span all seven repos touched by the report's claims (afi-config, afi-reactor, afi-core, afi-math, afi-mint, afi-token, afi-docs) and all fourteen body sections; they are the same pointers used inline in §2–§14, gathered here for ease of cross-checking. No claim in this index is path-only — every entry carries an exact line or line range.
