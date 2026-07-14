# AFI Districts / API Atlas Reconciliation Audit — Complete Record

> **This report is a read-only reconciliation record. It does not establish protocol authority, authorize implementation, ratify proposed doctrine, or supersede accepted governance decisions. Recommendations become authoritative only through an owner-approved AFI governance decision.**

**Status:** evidence and recommendation, not protocol law · **Scope:** read-only cross-repository reconciliation · **Preserved:** 2026-07-14

**Baseline — current `origin/main`, re-verified clean and unchanged from audit time:** afi-docs `c666224`, afi-protocol `7edb203`, afi-gateway `262fa30`, afi-reactor `9b56fb1`, afi-core `806db49`, afi-config `ce8c1de`, afi-governance `6b3638b`, afi-mint `d98a622`, afi-econ `471f4fe`, afi-token `d435b40`, afi-infra `e136a9c`, afi-math `f20c0dd`, afi-plugins `95d73f3`. **Access-limited (local `main` only; fetch failed):** afi-research-site, afi-sdk-python, afi-sdk-ts, afi-starters.

**Companion artifacts (same directory):** `AFI_DISTRICTS_API_ATLAS_FINDINGS.json` and `AFI_DISTRICTS_API_ATLAS_FINDINGS.csv` (machine-readable registers, 96 findings, parity-checked against this report) · `AFI_DISTRICTS_API_ATLAS_METHODOLOGY.md` (methodology, reliability, and the corrections appendix).

---

## 1. Executive verdict

**AFI has limited-but-real reconciliation debt plus a handful of missing governance decisions — not an architectural crisis, and not merely documentation drift.** The debt is unevenly distributed: the **head of the pipeline is sound; the tail is unbuilt; and the authority/naming layer is genuinely tangled.**

- **No live implementation is unsafe or internally contradictory in a dangerous way.** The deployed path (ingest → normalize → validate → score → persist) is coherent, deterministic, deployed, and correctly fenced: the D2 provenance builder structurally bars money-plane keys (`claimRoot`, `rewardAmount`, `vaultAddress`, `validatorDecision`) from proof-plane output (`afi-reactor/src/pipeheads/provenance/builders.ts:115-128`). The one genuinely-built economic invariant — the 86B supply cap — is governed and enforced on-chain (`afi-token/src/AFIToken.sol:35,97`).
- **The lifecycle is not one pipeline.** It exists as **three parallel, non-joined signal surfaces** with no persisted identifier continuity, and the entire tail (validation → qualification → epoch → receipt → reward → claim) is **unwired library code, documented types, and a revert-today contract**. This is coherent as "unbuilt," not as "broken."
- **The sharpest live contradiction is not unsafe but is worth flagging:** the gateway writes **unscored skeleton records directly into the canonical `afi_tssd.tssd_signals` vault**, violating its own external-client contract (`afi-gateway/src/http/app.ts:123-141` vs `src/index.ts:11-18`) — a two-writer situation with no governance reconciling ownership.
- **Governance authority is real but distributed and partly self-referential:** the supreme Charter lives in **afi-config** (not afi-governance); afi-governance decisions declare themselves *subordinate to "settlement/district doctrine in afi-docs,"* yet afi-governance holds **zero** settlement or district decision — so afi-docs functions as de-facto law that self-declares "CANONICAL" without ratification.

**Resumption posture (see §7 for the gates):**
- **MongoDB work may resume after a small reconciliation set** — not now (starting now would harden the two-store split), and not "only after major corrections." It needs one canonical-store + object-identity + lifecycle-finality decision (Gate A).
- **Blockchain design may resume once canonical off-chain inputs are defined** (ratify/scope the settlement doctrine, decide the epoch-scoped settlement object, fix object identity + finality) — Gate B.
- **Blockchain implementation is blocked on governance** (ungoverned numeric role weights, unratified settlement, an explicit decision to retire the deprecated `mintForSignal` v0 shape) — Gate C.

---

## 2. Canonical current-state map

**Districts (only two named anywhere; numbering is a docs invention).** The governing instrument is `afi-config/codex/governance/droids/AFI_DROID_PIPEHEAD_ADDENDUM.v0.1.md` (companion to the Charter), which names districts **functionally and never numbers them**: it authorizes only the first "Signal Evaluation Pipehead System" and lists a future roster (provenance, reputation, contracts, settlement-readiness, monitoring, docs, external-agent-interfaces).
- **District 1** ("Signal-Evaluation Pipehead POC"): GOVERNED (addendum §12) + IMPLEMENTED (`afi-reactor/src/pipeheads/`), non-production, `demoOnly`.
- **District 2** ("Canonical Data & Provenance Boundary"): docs-numbered; maps to the roster's "provenance." M1 is governed by `afi-docs/reports/district-2-d17-implementation-authorization.md` (M1-only); the shipped reactor "M2" (D2-native artifact surface) **has no authorization instrument** and spans documented M2+M3+M4.
- No District 0 or 3+. The numbers "1/2" appear only in afi-docs + afi-reactor docs; afi-protocol, afi-gateway, afi-core contain no "District" token at all.

**Repositories & dependency direction.** afi-math is the sink/root of truth; `afi-core ← {afi-infra, afi-reactor (+ afi-config file: dep), afi-mint (peer)}`; `afi-infra ← afi-gateway`. **afi-governance and afi-docs sit outside the code DAG** — they exert authority by citation only. Note: the governed "sole source of truth" afi-math resolves to **different commits** across consumers (afi-core pins `#6091cbf`, afi-mint pins `#f20c0dd`).

**Primary objects.** `signalId` (USS `provenance.signalId`) is the one shared join key. `AnalystScoreTemplate` (afi-core) is the canonical analyst score but carries no `signalId`/self-version. "Scored signal" has three representations at different maturities (reactor response `ReactorScoredSignalV1`, reactor persistence `ReactorScoredSignalDocument`, and the draft-only D2 `ScoredSignalV1`); the canonical D2 artifact is computed and thrown away while the non-canonical runtime doc is what persists.

**API surfaces.** Reactor: `/health`, `/debug/env`, `/api/webhooks/tradingview`, `/api/ingest/cpj`. Gateway REST (`start:minimal` only): `/healthz`, `/api/v1/api-keys*`, `/api/v1/signals` (→ TSSD vault), `/api/v1/skills*`; the default `npm start` (ElizaOS) exposes **no data plane**. No OpenAPI exists; four overlapping maps disagree; there is no canonical Atlas.

**Persistence.** Two independent Mongo stores, no join: `afi_reactor.reactor_scored_signals_v1` (reactor, scored, append-only, self-declared "isolated") and `afi_tssd.tssd_signals` (afi-infra time-series `VaultedSignalRecord`, gateway-written skeletons, non-atomic upsert, TTL-expirable). MongoDB currently acts as an **unseparated mixture** (operational storage + would-be canonical evidence + replay source).

**Chain attachment.** Only the 86B cap is governed-and-built. The four-layer settlement machinery (EpochSettlementManifest, four roots, ERC-6909 reputation receipt, RewardsVault claims) is DOCUMENTED + PROPOSED with zero implementation; the *implemented* reality is the deprecated v0 per-signal push-at-mint shape that doctrine forbids. The four planes must not be collapsed: (1) MongoDB persistence = evidence custody, (2) on-chain proof/receipt = v0 breadcrumb, (3) token/reward economics, (4) settlement/payout = unbuilt.

---
## 3. Complete findings register (96 findings)

_Every finding carries: ID · classification (C0–C8) · severity · confidence · evidence · consequence · recommended authority · minimal correction · pre-MongoDB / pre-blockchain / governance flags · suggested slot · duplicate/cluster. The two corrected agent errors (DIST-H-01, OBJ-08) appear with corrected text and a correction note; the original false claims are preserved only in the Methodology corrections appendix._

**Distribution:** 6 blocker · 32 high · 33 medium · 25 low. By class: C1=21, C2=21, C3=12, C4=17, C5=6, C6=6, C7=12, C8=1.


### 3.1 Blockers (6)

#### BG-1 — On-chain + off-chain runtime settlement is v0 per-signal push-at-mint, contradicting both the GOVERNED mint decision and the DOCUMENTED epoch-batched doctrine
- **Class/Severity/Confidence:** C1 · blocker · proven  |  **Repo:** afi-token  |  **Dimension:** blockchain
- **Contradiction/gap:** GOVERNED mint-formula D3/D4 and DOCUMENTED doctrine D1/D2/D9 require epoch-batched settlement where recording a signal MUST NOT move tokens and entitlement exists only via a committed manifest claimRoot; the IMPLEMENTED path mints ERC-20 directly to a single beneficiary per signal at validation time.
- **Evidence:** `afi-token/src/AFIMintCoordinator.sol:68-86 (mintForSignal → token.mintEmissions(beneficiary, tokenAmount) per signal)`; `afi-mint/src/orchestrator/MintExecutor.ts:107-108,142-150 (runtime builds per-signal MintRequest and calls mintForSignal)`; `afi-docs/specs/AFI_SETTLEMENT_V1_DOCTRINE.md:82-90,99-101,143 (D1 epoch-batched, D9 mintForSignal deprecated)`; `afi-governance/decisions/mint-formula-bt-86b-alignment-v0.1.md:84-86,89-91 (skeleton is epoch-budget→role-pool, direct per-signal clamp NOT adopted)`
- **Consequence:** The only implemented reward path is the exact architecture doctrine deprecates; recording provenance IS paying, so provenance≠payout separation is violated in production code, and no epoch/manifest attachment point exists to build against.
- **Recommended authority:** afi-governance decision + owner (settlement doctrine is afi-docs, not yet a governance decision)
- **Minimal correction:** None proposed (read-only). Resolution is an authorized rebuild to epoch-batched settlement; blocked by mint-formula §6 non-authorization.
- **Flags:** Gov, pre-Chain  |  **Suggested slot:** CHAIN-GOV (Gate B/C)  |  **Status:** open

#### BG-3 — Deprecated on-chain per-signal MintRequest shape leaked backward into the off-chain orchestrator API contract
- **Class/Severity/Confidence:** C4 · blocker · proven  |  **Repo:** afi-mint  |  **Dimension:** blockchain
- **Contradiction/gap:** The off-chain runtime's data contract is defined to 'match the on-chain struct' (single beneficiary/tokenAmount/receiptId/receiptAmount per signal), so the deprecated v0 blockchain assumption is embedded in the off-chain API/persistence layer, not just the contracts.
- **Evidence:** `afi-mint/src/orchestrator/MintExecutor.ts:16-27 (interface MintRequest — comment 'matches on-chain struct')`; `afi-mint/src/orchestrator/MintExecutor.ts:146 (hard-coded receiptAmount: 1n per signal)`; `afi-mint/src/adapters/EmissionsMintDataProvider.ts:24-38,127-167 (per-signal proportional amount, single beneficiary)`; `afi-docs/adrs/ADR-002-erc6909-strategy-epoch-receipts.md:26,59 (per-signal payload shape is exactly what is deprecated)`
- **Consequence:** Migrating to epoch-batched manifest settlement requires rewriting off-chain orchestration/adapter/API contracts, not merely redeploying Solidity; the leakage widens the blast radius of the v0→v1 change.
- **Recommended authority:** afi-mint maintainer under authorized settlement-v1 rebuild
- **Minimal correction:** Record the off-chain leak of the on-chain MintRequest shape; retire it only with the governed v0->v1 mint-shape migration behind Gate C.
- **Flags:** pre-Mongo, pre-Chain  |  **Suggested slot:** CHAIN-GOV (Gate B/C)  |  **Status:** open
- **Relationships:** depends-on G-1

#### GOV-01 — Numeric baseline role weights are ungoverned — hard block on live mint
- **Class/Severity/Confidence:** C5 · blocker · proven  |  **Repo:** afi-governance  |  **Dimension:** governance-corpus
- **Contradiction/gap:** mint-formula-bt-86b-alignment-v0.1.md D3 governs a mint settlement skeleton that routes the epoch budget through 'governed baseline role weights', but the same decision states no such governance record exists: 'no accepted governance record in afi-governance currently defines numeric baseline role weights, so they remain a required follow-up decision before live mint activation.'
- **Evidence:** `afi-governance/decisions/mint-formula-bt-86b-alignment-v0.1.md:87`; `afi-governance/decisions/mint-formula-bt-86b-alignment-v0.1.md:129`; `afi-governance/decisions/mint-formula-bt-86b-alignment-v0.1.md:163`; `afi-governance/decisions/mint-formula-bt-86b-alignment-v0.1.md:183`
- **Consequence:** Any mint/reward/settlement design or implementation that assumes role-pool routing has no numeric authority to route against; live mint activation is governance-blocked until a role-weights decision is accepted.
- **Recommended authority:** afi-governance/decisions (new decision record)
- **Minimal correction:** A new afi-governance decision pinning numeric baseline role weights (with KATs/version pins) before any mint activation resumes.
- **Flags:** Gov, pre-Chain  |  **Suggested slot:** CHAIN-GOV  |  **Status:** open

#### F-PERSIST-01 — Two divergent, unreconciled Mongo document schemas both DOCUMENTED as the one canonical evidence store
- **Class/Severity/Confidence:** C6 · blocker · proven  |  **Repo:** afi-reactor  |  **Dimension:** persistence
- **Contradiction/gap:** AFI_EVIDENCE_STORE_DECISION.md and the inventory assert a single 'canonical reference evidence store', but the code ships two schemas in two databases: ReactorScoredSignalDocument → afi_reactor.reactor_scored_signals_v1 (afi-reactor) and VaultedSignalRecord → afi_tssd.tssd_signals (afi-infra), with different keys, drivers (mongodb ^6 vs ^7) and lifecycle models, and tssdVaultService.ts:6 explicitly declares them ISOLATED.
- **Evidence:** `afi-reactor/src/types/ReactorScoredSignalV1.ts:122-187`; `afi-infra/src/tssd/types.ts:331-367`; `afi-reactor/src/services/tssdVaultService.ts:6`; `afi-docs/specs/audit/AFI_EVIDENCE_STORE_DECISION.md (Decision block)`; `afi-docs/specs/audit/AFI_MONGO_TSSD_INVENTORY.md:16,102`
- **Consequence:** 'Canonical protocol history' is ambiguous: a signal persisted via the reactor path and the same signal via the gateway path produce structurally incompatible records in different stores, with no reconciliation edge. Deeper Mongo machinery cannot resume without choosing one canonical schema or an explicit two-store contract.
- **Recommended authority:** afi-governance (MONGO-GOV) to name the canonical store; afi-infra to own the persistence implementation
- **Minimal correction:** Governance decision (MONGO-GOV) naming the single canonical scored-signal store and document shape, then reconcile reactor_scored_signals_v1 vs tssd_signals; do not implement before Gate A.
- **Flags:** Gov, pre-Mongo, pre-Chain  |  **Suggested slot:** MONGO-GOV  |  **Status:** open

#### BG-4 — No canonical off-chain epoch-close / EpochSettlementManifest builder exists — the governed epoch-budget skeleton has zero implementation
- **Class/Severity/Confidence:** C7 · blocker · proven  |  **Repo:** afi-docs  |  **Dimension:** blockchain
- **Contradiction/gap:** The GOVERNED mint skeleton and DOCUMENTED manifest require an off-chain epoch-close roll-up producing the qualified set, proof roots, and claimRoot; no such builder exists — the reactor emits only per-signal ProvenanceRecords that persist nothing and carry no on-chain commitments.
- **Evidence:** `afi-docs/specs/AFI_EPOCH_SETTLEMENT_MANIFEST.md:158-163 (Phase A build at epoch close)`; `afi-reactor/src/pipeheads/provenance/builders.ts:598-604 (ProvenanceRecord carries no storage, no on-chain commitments, no claims)`; `afi-reactor/src/pipeheads/provenance/builders.ts:115-128 (claimRoot/rewardAmount/vaultAddress explicitly FORBIDDEN in provenance artifacts)`; `afi-mint/src/adapters/EmissionsMintDataProvider.ts:224-254 (only an InMemoryEpochStateTracker test helper; no production epoch close)`
- **Consequence:** The manifest — the documented single bridge from proof to money — is unbuilt; there is no canonical off-chain input from which any on-chain root or reward entitlement could be derived.
- **Recommended authority:** owner/governance authorization (currently withheld per mint-formula §6)
- **Minimal correction:** Design (not build) the off-chain epoch-close / EpochSettlementManifest builder behind Gate B, after CHAIN-GOV ratifies the settlement object.
- **Flags:** Gov, pre-Chain  |  **Suggested slot:** CHAIN-GOV (Gate B/C)  |  **Status:** open

#### BG-6 — Numeric baseline role weights are explicitly ungoverned, yet the governed mint skeleton depends on them — a required-but-missing governance input for reward economics
- **Class/Severity/Confidence:** C7 · blocker · proven  |  **Repo:** afi-governance  |  **Dimension:** blockchain
- **Contradiction/gap:** mint-formula D3 routes the epoch budget 'using governed baseline role weights' (:43) while the same decision states 'no accepted governance record currently defines numeric baseline role weights' (:87, :129); the only concrete weights are afi-econ research-only and role-name-mismatched.
- **Evidence:** `afi-governance/decisions/mint-formula-bt-86b-alignment-v0.1.md:43,87,129,183 (skeleton needs governed weights; none governed; required follow-up before live mint)`; `afi-econ/params/gauge_v0.yaml:4-8 (producers 0.55/enrichment 0.25/validators 0.10/public_goods 0.10 — version v0, research-only)`; `afi-docs/specs/AFI_SETTLEMENT_V1_DOCTRINE.md:115,230 (O3 splits OPEN; gauge is not final law; roles Providers/Analysts-Scorers/Validators/public-goods)`
- **Consequence:** Plane (3) reward economics cannot be finalized: the role-split attachment point is a hard governance blocker and the only extant values are research placeholders whose role taxonomy does not even match the doctrine.
- **Recommended authority:** afi-governance decision (numeric baseline role weights) + owner
- **Minimal correction:** Govern the numeric baseline role weights (CHAIN-GOV) before any mint/settlement; duplicate of GOV-01.
- **Flags:** Gov, pre-Chain  |  **Suggested slot:** CHAIN-GOV (Gate B/C)  |  **Status:** open


### 3.2 High severity (32)

#### BG-2 — Implemented reputation receipt is ERC-1155 per-signal, directly contradicting the documented ERC-6909 soulbound per-(strategy,epoch) receipt
- **Class/Severity/Confidence:** C1 · high · proven  |  **Repo:** afi-token  |  **Dimension:** blockchain
- **Contradiction/gap:** ADR-002 D-002.1 states v1 receipts MUST be ERC-6909 and ERC-1155 MUST NOT be introduced, one per (strategyId,epochId), soulbound, non-payout; the implemented AFISignalReceipt is ERC-1155, minted per signal in lockstep with the reward.
- **Evidence:** `afi-token/src/AFISignalReceipt.sol:12,35-45 (ERC1155 mintReceipt per call)`; `afi-token/src/AFIMintCoordinator.sol:80-85 (receipt minted inside mintForSignal alongside token)`; `afi-docs/adrs/ADR-002-erc6909-strategy-epoch-receipts.md:57-65 (MUST ERC-6909, MUST NOT ERC-1155, one per epoch, not payout)`; `afi-mint/src/adapters/EmissionsMintDataProvider.ts:30-31,185-191 (off-chain adapter carries receiptId linking to AFISignalReceipt)`
- **Consequence:** The reputation-receipt attachment point (Layer 2) is implemented as the exact standard doctrine forbids, and the receipt reads as reward-proof=payout-unit; no ERC-6909 receipt exists anywhere in AFI src.
- **Recommended authority:** owner/governance (ADR-002 is owner-locked docs, not a governance decision)
- **Minimal correction:** Ratify the ERC-6909 reputation-receipt standard and record the deployed ERC-1155 AFISignalReceipt as historical/v0-only (CHAIN-GOV); do not build.
- **Flags:** Gov, pre-Chain  |  **Suggested slot:** CHAIN-GOV (Gate B/C)  |  **Status:** open
- **Relationships:** depends-on G-1

#### BG-7 — Mint authorization is a 1-of-1 single-key Treasury Safe with no on-chain finality/score gate — contradicts N-of-M doctrine and any 'no centralized control' claim
- **Class/Severity/Confidence:** C1 · high · strongly-supported  |  **Repo:** afi-token  |  **Dimension:** blockchain
- **Contradiction/gap:** Doctrine §12 requires not-1-of-1 (N-of-M + timelock) and separation of mint authority from settlement; the implemented EMISSIONS_ROLE sits on a threshold-1 Safe signed by a single EOA, and mintEmissions enforces only the 86B cap (no epoch/score/finality check).
- **Evidence:** `afi-token/src/AFIToken.sol:92,97 (mintEmissions onlyRole(EMISSIONS_ROLE); only cap enforced)`; `afi-config/registries/afi-vault-address-registry.v1.json:313-320,462 (Base Treasury Safe 0x1Dd6705 is 1-of-1, single signer 0xb87C…ad62; W-ONE-OF-ONE)`; `afi-docs/specs/AFI_SETTLEMENT_V1_DOCTRINE.md:179-182 (MUST NOT 1-of-1; N-of-M + timelock)`; `afi-docs/specs/audit/final/AFI_ONCHAIN_ANCHOR_GAP_ANALYSIS.md:139 (on-chain enforces no scoring/finality; full trust in role holder)`
- **Consequence:** The treasury-controlled-mint attachment point is centralized under a single key with no on-chain proof-of-performance gate; Safe topology (O8) is an OPEN owner decision.
- **Recommended authority:** owner (Safe topology O8), governance for role policy
- **Minimal correction:** Governance decision on N-of-M + timelock mint authorization and an on-chain finality/score gate (Gate C); do not change contracts now.
- **Flags:** Gov, pre-Chain  |  **Suggested slot:** CHAIN-GOV (Gate B/C)  |  **Status:** open

#### CHAIN-03 — Deprecated v0 per-signal reward/receipt/epoch shape is IMPLEMENTED on-chain, in runtime schemas, and in persistence — the exact shape doctrine forbids
- **Class/Severity/Confidence:** C1 · high · proven  |  **Repo:** afi-token  |  **Dimension:** objects-econ
- **Contradiction/gap:** AFIMintCoordinator.mintForSignal mints reward + ERC-1155 receipt to a single beneficiary in ONE call with struct MintRequest{address beneficiary; uint256 tokenAmount; uint256 receiptId; uint256 receiptAmount; bytes32 signalId; uint64 epoch} (afi-token/src/AFIMintCoordinator.sol:19-27,68-86). This same {beneficiary, tokenAmount, receiptId, receiptAmount, signalId, epoch} shape is re-declared in the live validator-pipeline Zod schema (afi-mint/schemas/MintTrigger.schema.ts:11-19, receiptId='ERC-1155 receipt ID', epoch='Epoch ID as string') and persisted as a `minted` lifecycle stage (afi-infra/src/tssd/types.ts:187-200,277-283). Doctrine ECON-2/MAN-S4 says the manifest MUST NOT encode a single beneficiary/tokenAmount/receiptAmount per-signal payout shape (AFI_EPOCH_SETTLEMENT_MANIFEST.md:89; …SCHEMA.md:145) and D9 deprecates mintForSignal.
- **Evidence:** `afi-token/src/AFIMintCoordinator.sol:19-27`; `afi-token/src/AFIMintCoordinator.sol:68-86`; `afi-mint/schemas/MintTrigger.schema.ts:11-19`; `afi-infra/src/tssd/types.ts:187-200`; `afi-docs/specs/AFI_EPOCH_SETTLEMENT_MANIFEST.md:89`
- **Consequence:** A receipt/reward/epoch object is already NAMED in on-chain, runtime, and persistence interfaces in the exact v0 push-at-mint shape the canonical settlement design deprecates — before any canonical/governed epoch-scoped manifest, claimRoot, or ERC-6909 reputation receipt exists. Future settlement work must either retire this shape or risk shipping two contradictory payout object models.
- **Recommended authority:** afi-token + afi-mint + afi-infra owners under the settlement doctrine's v0-deprecation posture
- **Minimal correction:** Mark the v0 MintRequest/mintForSignal/AFISignalReceipt path and its runtime Zod mirror + TSSD `minted` stage as explicitly v0/deprecated (matching ADR-002:112, AFI_ERC6909…:42-47) so they cannot be mistaken for the v1 object model; do not migrate v0 state (constitution §14).
- **Flags:** pre-Mongo, pre-Chain  |  **Suggested slot:** CHAIN-GOV  |  **Status:** open
- **Relationships:** cluster CL-08 (Deprecated v0 per-signal push-at-mint shape (beneficiary/tokenAmount/receiptId/epoch) is implemented on-chain+runtime+persistence, contradicting the documented v1 epoch-batch settlement doctrine); depends-on CHAIN-01

#### DIST-H-02 — Governed 'sole source of truth' afi-math resolves to two different commits across consumers
- **Class/Severity/Confidence:** C1 · high · proven  |  **Repo:** afi-core  |  **Dimension:** repo-authority
- **Contradiction/gap:** math-authority-v0.1.md §4.1 governs afi-math as the single source of truth for canonical executable math. afi-core pins afi-math at git commit 6091cbf55…, while afi-mint pins github commit f20c0dd… (the KAT-hardened PR-1 result cited as canonical in mint-formula-bt-86b-alignment-v0.1.md §2.3). The scoring/reactor lineage (reactor→core→math@6091cbf) and the mint/settlement lineage (mint→math@f20c0dd) therefore execute different revisions of the governed kernel.
- **Evidence:** `afi-core/package.json:69`; `afi-mint/package.json:40`; `afi-governance/decisions/math-authority-v0.1.md:96-104`; `afi-governance/decisions/mint-formula-bt-86b-alignment-v0.1.md:2`
- **Consequence:** Decay/emissions kernels can diverge numerically between the pipeline path and the mint path, defeating the 'one source of truth' invariant and any cross-repo KAT/replay guarantee before settlement math is wired.
- **Recommended authority:** afi-math
- **Minimal correction:** Pin all afi-math consumers (afi-core, afi-mint, and any future reactor direct dep) to a single governed afi-math commit; record the pinned commit in the decision ledger.
- **Flags:** pre-Chain  |  **Suggested slot:** OBJ-GOV  |  **Status:** open

#### DIST-H-03 — afi-docs acts as de-facto settlement/district law where no governance decision exists
- **Class/Severity/Confidence:** C1 · high · proven  |  **Repo:** afi-governance  |  **Dimension:** repo-authority
- **Contradiction/gap:** Governance decisions declare subordination to 'existing settlement/district doctrine in afi-docs', elevating a docs repo to binding authority. Yet settlement authority is scattered: doctrine in afi-docs (AFI_SETTLEMENT_V1_DOCTRINE.md, AFI_EPOCH_SETTLEMENT_MANIFEST.md, ADR-001), the manifest SCHEMA as a '.draft' in afi-config, and ZERO settlement decision in afi-governance/decisions/ (dir holds only math/mint/uwr decisions). Docs asserts law the governance ledger never ratified.
- **Evidence:** `afi-governance/decisions/math-authority-v0.1.md:6`; `afi-docs/specs/AFI_SETTLEMENT_V1_DOCTRINE.md`; `afi-docs/adrs/ADR-001-four-layer-settlement-architecture.md`; `afi-config/schemas/afiEpochSettlementManifest.draft.schema.json`; `afi-governance/decisions/`
- **Consequence:** Settlement/district object definitions are governed by unversioned docs + a draft schema rather than a decision, so blockchain/settlement design would attach to authority that governance never actually enacted — an authority inversion (docs above ledger).
- **Recommended authority:** afi-governance
- **Minimal correction:** Promote settlement/district doctrine into a numbered afi-governance decision (or explicitly designate specific afi-docs specs as governed-by-reference) and ratify the manifest schema out of '.draft'.
- **Flags:** Gov, pre-Chain  |  **Suggested slot:** D-GOV  |  **Status:** open
- **Relationships:** cluster CL-02 (Authority inversion: afi-docs Settlement-V1/District doctrine self-declares CANONICAL and governance defers to it, with zero ratifying afi-governance decision); depends-on DIST-H-01

#### DIST-H-04 — TSSD vault persistence authority is split between afi-infra (canonical) and afi-reactor (parallel isolated)
- **Class/Severity/Confidence:** C1 · high · proven  |  **Repo:** afi-infra  |  **Dimension:** repo-authority
- **Contradiction/gap:** afi-infra owns the canonical TSSD vault clients (MongoTSSDVaultClient, TenantScopedTSSDVaultClient) and VaultedSignalRecord type, which afi-gateway consumes. afi-reactor independently implements its own TSSD vault (src/services/tssdVaultService.ts, self-labeled 'ISOLATION: this service uses Reactor-owned collections, isolated from afi-infra') persisting ReactorScoredSignalDocument, and reactor's package.json has NO afi-infra dependency. Gateway's own comment names 'afi-reactor, afi-infra' jointly as where the canonical vault lives, confirming the ambiguity. Two persisted scored-signal object shapes, no single persistence owner.
- **Evidence:** `afi-infra/src/tssd/MongoTSSDVaultClient.ts`; `afi-infra/src/tssd/types.ts`; `afi-reactor/src/services/tssdVaultService.ts:6`; `afi-reactor/src/types/ReactorScoredSignalV1.ts`; `afi-gateway/src/lib/db/mongo.ts:11-12`; `afi-reactor/package.json`
- **Consequence:** No governed owner of the scored-signal persistence object; a replay or settlement consumer reading 'the TSSD vault' gets different schemas/collections depending on repo, blocking a single canonical persistence-map before MongoDB machinery resumes.
- **Recommended authority:** afi-infra
- **Minimal correction:** Designate one repo as the canonical TSSD vault/persistence owner (evidence favors afi-infra, which gateway already consumes) and record whether reactor's isolated collections are a sanctioned second store or must converge.
- **Flags:** Gov, pre-Mongo  |  **Suggested slot:** MONGO-GOV  |  **Status:** open
- **Relationships:** cluster CL-01 (Two isolated 'canonical' scored-signal vaults with no identifier join (afi-infra TSSD VaultedSignalRecord vs afi-reactor self-isolated ReactorScoredSignalDocument))

#### LIFE-04 — Reward/validation tail implemented as library but fully unwired (zero-owner bridge)
- **Class/Severity/Confidence:** C1 · high · proven  |  **Repo:** afi-mint  |  **Dimension:** lifecycle
- **Contradiction/gap:** afi-mint's validator→challenge→finalize→mint orchestrator is complete as code, but has no persistent state store (only InMemorySignalStateStore), no implementation of IAnalystScoreFetcher, no ValidatorDaemon instantiation/entrypoint anywhere, no concrete IMintCoordinatorContract binding, and reputation_bridge is self-labelled 'all placeholder.' No component moves a reactor/gateway scored signal into a SignalValidatorState.
- **Evidence:** `afi-mint/src/orchestrator/index.ts:31-36`; `afi-mint/src/orchestrator/ValidatorDaemon.ts:48-51`; `afi-mint/src/orchestrator/MintExecutor.ts:57-108`; `afi-mint/src/reputation_bridge.ts:9-11`
- **Consequence:** Qualification, finalization, and reward eligibility do not run in any deployed process. The lifecycle terminates at SCORED in production; everything downstream is inert code that cannot be triggered by a real signal.
- **Recommended authority:** afi-mint, gated by an afi-governance decision defining the scored-signal → validator handoff
- **Minimal correction:** Do not portray the tail as live. Before wiring, define (in governance) the canonical source store and the IAnalystScoreFetcher/ISignalStateStore bindings; this is a prerequisite for any mint machinery.
- **Flags:** Gov, pre-Mongo, pre-Chain  |  **Suggested slot:** LIFE-GOV, OBJ-GOV  |  **Status:** open
- **Relationships:** cluster CL-06 (Reactor→mint validator bridge is unwired: no IAnalystScoreFetcher impl, daemon never instantiated, qualification gate dark); depends-on LIFE-02

#### LIFE-05 — Epoch assignment/inclusion has zero implemented owner
- **Class/Severity/Confidence:** C1 · high · proven  |  **Repo:** afi-gateway  |  **Dimension:** lifecycle
- **Contradiction/gap:** epochId is REQUIRED by the gateway VaultedSignalRecord identity (app.ts:26) and is an indexed topic of the on-chain MintCoordinated event, but the deployed scoring path produces a ReactorScoredSignalDocument with NO epochId and nothing assigns one. The gateway obtains epochId only from the caller's payload; no component computes epoch membership for a scored signal.
- **Evidence:** `afi-gateway/src/http/app.ts:26`; `afi-reactor/src/services/froggyDemoService.ts:281-328`; `afi-token/src/AFIMintCoordinator.sol:38-44`; `afi-infra/src/tssd/types.ts:22-26`
- **Consequence:** Epoch inclusion — the pivot from per-signal scoring to per-epoch reward batching (ADR-001 core requirement) — has no implemented producer. A scored signal cannot be placed in an epoch, so reward computation and settlement cannot begin even if the tail were wired.
- **Recommended authority:** afi-governance (epoch definition) + afi-mint/afi-econ (epoch state tracker)
- **Minimal correction:** Define which component assigns epochId and at which transition; until then, treat epoch inclusion as PROPOSED, not a gap the scoring path silently ignores.
- **Flags:** Gov, pre-Mongo, pre-Chain  |  **Suggested slot:** LIFE-GOV  |  **Status:** open

#### GW-02 — Gateway writes directly to canonical TSSD vault, violating its own external-client contract
- **Class/Severity/Confidence:** C2 · high · proven  |  **Repo:** afi-gateway  |  **Dimension:** gateway-runtime
- **Contradiction/gap:** POST /api/v1/signals (app.ts:123-141) persists directly into the canonical TSSD store afi_tssd/tssd_signals via afi-infra TenantScopedTSSDVaultClient (vaultFactory.ts:7-33), while src/index.ts:11-18 declares the gateway 'MUST call AFI APIs over HTTP/WS' and 'MUST NOT reimplement signal logic', and src/lib/db/mongo.ts:11-16 says the gateway is 'NOT for TSSD vault data'. Atlas:18 assigns TSSD writes to reactor. Result: two independent writers into the canonical vault, and the gateway writes unscored skeleton records (empty stages, no analystScore).
- **Evidence:** `afi-gateway/src/http/app.ts:123-141`; `afi-gateway/src/services/vaultFactory.ts:7-33`; `afi-gateway/src/index.ts:11-18`; `afi-gateway/src/lib/db/mongo.ts:11-16`; `afi-docs/AFI_System_Atlas.md:18`; `afi-infra/src/tssd/TenantScopedTSSDVaultClient.ts:29-38`
- **Consequence:** Canonical TSSD collection accrues unscored gateway records alongside reactor's scored-lifecycle records with no schema/ownership arbitration; downstream training/replay/mint consumers cannot assume records passed the reactor pipeline; provenance and vault-ownership boundary is undefined.
- **Recommended authority:** afi-governance (TSSD vault write-ownership boundary) + afi-infra (canonical vault client)
- **Minimal correction:** Decide who may write afi_tssd/tssd_signals: either route gateway ingest through reactor HTTP (honoring index.ts:11-18) or governance-authorize the gateway as a second writer with a distinct collection/stage contract.
- **Flags:** Gov, pre-Mongo  |  **Suggested slot:** MONGO-GOV  |  **Status:** open

#### LIFE-01 — Three incompatible validator/lifecycle state vocabularies across surfaces
- **Class/Severity/Confidence:** C2 · high · proven  |  **Repo:** afi-infra  |  **Dimension:** lifecycle
- **Contradiction/gap:** The validator/finalization stage has three divergent status-name sets for the same lifecycle: afi-infra ValidatorStateKind = pending|decay_pass|challenge_open|voting_complete|minted|rejected (6 states); afi-mint SignalValidatorStateKind = pending|qualified|rejected|challenge_window|contested|dispute_resolved|finalized|minted|rejected_final (9 states); and afi-infra SignalLifecycleStage = RAW|ENRICHED|ANALYZED|SCORED|MINTED|REPLAYED. None references the others; the mint machine even claims signalId 'links to TSSD vault' while using a different state alphabet than the TSSD ValidatorSnapshot it supposedly links to.
- **Evidence:** `afi-infra/src/tssd/types.ts:277-318`; `afi-infra/src/tssd/types.ts:10-16`; `afi-mint/src/orchestrator/types.ts:33-42`; `afi-mint/src/orchestrator/types.ts:97-99`
- **Consequence:** No canonical state model exists for validation/qualification/finalization. Any component that reads 'state' must know which surface produced it; a validator transition in one vocabulary cannot be mapped deterministically to the other, blocking a coherent finality definition and any cross-surface audit.
- **Recommended authority:** afi-governance decision designating one canonical lifecycle state machine (candidate authority: afi-infra TSSD as the documented canonical record, or afi-mint as the operative one)
- **Minimal correction:** Pick one state enum as canonical; make the other a declared, versioned projection/alias with an explicit mapping table; cite it in a governance decision.
- **Flags:** Gov, pre-Mongo, pre-Chain  |  **Suggested slot:** LIFE-GOV, OBJ-GOV, OBJ-REACTOR  |  **Status:** open

#### OBJ-01 — Strategy identifier is non-canonical and self-conflicting within a single persisted document
- **Class/Severity/Confidence:** C2 · high · proven  |  **Repo:** afi-reactor  |  **Dimension:** objects-core
- **Contradiction/gap:** Strategy is a bare string under ≥4 field names (USS facts.strategy, AnalystScoreTemplate.strategyId, ReactorScoredSignalV1.meta.strategy, ReactorScoredSignalDocument.strategy.name, ScoredSignalV1.strategyId) with divergent formats ('froggy_trend_pullback_v1' vs 'trend_pullback_v1'). In froggyDemoService, meta.strategy and strategy.name are derived from rawUss.facts.strategy while pipeline.analystScore.strategyId is set independently by the analyst, so the same document carries two strategy ids that need not match and are never reconciled.
- **Evidence:** `afi-reactor/src/uss/ussValidator.ts:55`; `afi-core/src/analyst/AnalystScoreTemplate.ts:36-38`; `afi-reactor/src/types/ReactorScoredSignalV1.ts:110`; `afi-reactor/src/types/ReactorScoredSignalV1.ts:174-176`; `afi-reactor/src/services/froggyDemoService.ts:226`; `afi-reactor/src/services/froggyDemoService.ts:261`; `afi-reactor/src/services/froggyDemoService.ts:298`; `afi-reactor/src/services/froggyDemoService.ts:322`; `afi-reactor/src/pipeheads/provenance/builders.ts:81`
- **Consequence:** Any consumer keying rewards, replay, or provenance on strategy cannot trust a single field; a persisted doc can attribute the same signal to two different strategies. Cross-repo strategy attribution (mint/econ) is ambiguous.
- **Recommended authority:** afi-reactor (persistence contract owner) with a strategy-id format decision in afi-governance
- **Minimal correction:** Designate one canonical strategy identifier field + format and derive/validate all others from it; assert meta.strategy/strategy.name == analystScore.strategyId at persistence time.
- **Flags:** Gov, pre-Mongo, pre-Chain  |  **Suggested slot:** LIFE-GOV, OBJ-GOV, OBJ-REACTOR  |  **Status:** open

#### OBJ-02 — "Scored signal" has three structurally different canonical candidates at different maturities
- **Class/Severity/Confidence:** C2 · high · proven  |  **Repo:** afi-reactor  |  **Dimension:** objects-core
- **Contradiction/gap:** ReactorScoredSignalV1/ReactorScoredSignalDocument (IMPLEMENTED runtime, includes rawUss/lenses/_priceFeedMetadata/volatile timestamps) coexists with the D2 ScoredSignalV1 projection (DRAFT/NON-IMPLEMENTATION, x-afiStatus:'draft-non-implementation', structurally EXCLUDES rawUss/lenses/timestamps) and InternalScoringResult. All three are called a scored signal but have disjoint field sets and opposite timestamp doctrine.
- **Evidence:** `afi-reactor/src/types/ReactorScoredSignalV1.ts:75-114`; `afi-reactor/src/types/ReactorScoredSignalV1.ts:122-187`; `afi-reactor/src/pipeheads/provenance/types.ts:145-162`; `afi-config/schemas/provenance/v1/scored-signal.schema.json`; `afi-reactor/src/pipeheads/types.ts:109-115`
- **Consequence:** The eventual canonical scored-signal-of-record is undecided; MongoDB persistence and any hash/provenance commitment could bind to the runtime shape (with volatile baggage) or the D2 projection (thin) — incompatible choices.
- **Recommended authority:** afi-config D2 boundary + afi-reactor
- **Minimal correction:** Record which representation is the persisted canonical object vs a derived projection, and how the runtime doc maps to the D2 projection.
- **Flags:** Gov, pre-Mongo, pre-Chain  |  **Suggested slot:** MONGO-GOV, OBJ-GOV  |  **Status:** open
- **Relationships:** cluster CL-07 (Scored-signal split: the canonical D2 draft is computed but never persisted, while a non-canonical runtime doc is what actually persists); depends-on LIFE-01

#### ATLAS-02 — Documented 'gateway ingest -> reactor scoring DAG' spine edge is bypassed by the implemented HTTP ingest
- **Class/Severity/Confidence:** C3 · high · proven  |  **Repo:** afi-docs  |  **Dimension:** api-atlas
- **Contradiction/gap:** Reference Impl Map §2 and Repository_Map.md:167 state afi-gateway forwards signals to afi-reactor for Froggy scoring. The implemented ingest POST /api/v1/signals (afi-gateway/src/http/app.ts:123) normalizes the body into a VaultedSignalRecord and writes it directly to the Mongo TSSD vault (app.ts:133-134 vault.upsert) with no reactor call. The only reactor HTTP call in the gateway lives in the CLI lane (afiClient.ts -> /api/webhooks/tradingview), not in the API ingest path.
- **Evidence:** `afi-docs/specs/AFI_REFERENCE_IMPL_MAP.md:48-60`; `afi-docs/AFI_Repository_Map.md:167`; `afi-gateway/src/http/app.ts:123`; `afi-gateway/src/http/app.ts:133`; `afi-gateway/src/services/vaultFactory.ts:24-33`; `afi-gateway/src/afiClient.ts:121`
- **Consequence:** The atlas asserts scoring happens on ingest; in reality the HTTP-ingested record lands in the vault unscored, so persistence-map and lifecycle reasoning built on the documented spine is wrong at the first hop.
- **Recommended authority:** afi-gateway owns the ingest contract; afi-docs Reference Impl Map must reconcile the spine diagram
- **Minimal correction:** State that /api/v1/signals is a direct-to-vault ingest of already-structured records, and that the gateway->reactor scoring hop exists only in the CLI/actions lane; or wire the ingest to the reactor.
- **Flags:** Gov, pre-Mongo  |  **Suggested slot:** ATLAS-DOC  |  **Status:** open

#### CORP-03 — Audit finals frame v0 mint/on-chain 'contradictions' against a model canonical doctrine already deprecated by design
- **Class/Severity/Confidence:** C3 · high · strongly-supported  |  **Repo:** afi-docs  |  **Dimension:** prior-audit-drafts
- **Contradiction/gap:** The 06-25 audit finals (C-BL-*, C-ES-1, C-MM-*) treat the single-beneficiary per-signal mint as a contradiction-to-fix versus the Portable Surface North Star, but the North Star itself now carries a banner ceding that v0 mint/ERC-1155/direct-beneficiary path is 'superseded as mainnet architecture' by Settlement V1, which the finals never cite.
- **Evidence:** `afi-docs/specs/AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md:3`; `afi-docs/specs/AFI_CONTRADICTION_REGISTER.md:100-135`; `afi-docs/specs/AFI_V0_DEPRECATION_AND_MIGRATION.md:40-44`; `afi-docs/specs/audit/final/AFI_CONTRADICTION_REGISTER.md:34-35`
- **Consequence:** The audit's mint-model tension reads as an open defect list when the governing doctrine already reclassifies it as intentionally-deprecated v0; the two corpora present the same code with opposite intent framings, and neither cross-references the other.
- **Recommended authority:** afi-docs (reconcile audit corpus framing with Settlement V1 doctrine)
- **Minimal correction:** Reframe the v0 mint/on-chain 'contradiction' rows against the superseding Settlement-v1 doctrine with current status, not against a bare code diff.
- **Flags:** pre-Chain  |  **Suggested slot:** CORP-SYNC  |  **Status:** open
- **Relationships:** cluster CL-08 (Deprecated v0 per-signal push-at-mint shape (beneficiary/tokenAmount/receiptId/epoch) is implemented on-chain+runtime+persistence, contradicting the documented v1 epoch-batch settlement doctrine)

#### GOV-03 — Top-level governance index points to a Constitution + tokenomics model that no longer exist on main
- **Class/Severity/Confidence:** C3 · high · proven  |  **Repo:** afi-governance  |  **Dimension:** governance-corpus
- **Contradiction/gap:** docs/governance_links.md presents 'Immutable References for AFI Governance (v1.0)' — AFI Constitution, governance_schema, role_definitions, tokenomics/distribution_model.ts, staking_rights.md, board_structure, mentor_validator_policy — all linked at tag paper-v1 (06ab9c3). All seven files are absent from current main (verified missing); git log shows commit d1799e1 'deprecate v0 governance references'. The protocol's nominal Constitution and canonical tokenomics/staking governance docs live only in an archived tag.
- **Evidence:** `afi-governance/docs/governance_links.md:2-32`; `afi-governance/decisions/math-authority-v0.1.md:12`; `afi-governance (git log): d1799e1 'docs: deprecate v0 governance references'; paper-v1 == 06ab9c30`
- **Consequence:** Any dimension seeking the 'AFI Constitution' or the canonical token distribution/staking model finds a dangling index; the current governance repo has no constitution or tokenomics model on main, only the four cleanup/interpretation decisions.
- **Recommended authority:** afi-governance (index hygiene) + owner decision on whether a v1 constitution exists
- **Minimal correction:** Retire or re-scope governance_links.md to state these are archived v0 references at paper-v1, not current 'immutable references', and record where (if anywhere) the current constitution/tokenomics authority lives.
- **Flags:** pre-Chain  |  **Suggested slot:** D-GOV  |  **Status:** open

#### GOV-05 — Settlement v1 architecture is doctrine in afi-docs but has no afi-governance decision
- **Class/Severity/Confidence:** C3 · high · strongly-supported  |  **Repo:** afi-governance  |  **Dimension:** governance-corpus
- **Contradiction/gap:** AGENTS.md and SAFE_REALITY.md declare AFI Settlement v1 (epoch settlement, RewardsVault/Merkle claim, ERC-6909 receipts) the 'canonical mainnet architecture' and point to afi-docs/specs/AFI_SETTLEMENT_V1_DOCTRINE.md, yet no afi-governance/decisions/ record governs settlement, and mint-formula D3's settlement skeleton ('challenge/maturity/escrow before settlement') never references Settlement v1 doctrine or ERC-6909.
- **Evidence:** `afi-governance/AGENTS.md:3`; `afi-governance/SAFE REALITY/SAFE_REALITY.md:3`; `afi-governance/decisions/mint-formula-bt-86b-alignment-v0.1.md:80-87`
- **Consequence:** The mainnet settlement architecture is asserted as canonical without a governance decision behind it, and may diverge from the governed mint-formula skeleton; chain-attachment dimension cannot cite a governing line for Settlement v1.
- **Recommended authority:** afi-governance/decisions (new settlement decision) reconciled with afi-docs doctrine
- **Minimal correction:** Either accept an afi-governance decision that adopts/points to AFI_SETTLEMENT_V1_DOCTRINE.md as governed, or reconcile mint-formula D3 with the Settlement v1 doctrine explicitly.
- **Flags:** Gov, pre-Chain  |  **Suggested slot:** CHAIN-GOV  |  **Status:** open
- **Relationships:** cluster CL-02 (Authority inversion: afi-docs Settlement-V1/District doctrine self-declares CANONICAL and governance defers to it, with zero ratifying afi-governance decision); depends-on GOV-01

#### LIFE-02 — Two isolated 'canonical' persistence stores with different documents and no identifier join
- **Class/Severity/Confidence:** C3 · high · proven  |  **Repo:** afi-reactor  |  **Dimension:** lifecycle
- **Contradiction/gap:** The deployed scoring path persists ReactorScoredSignalDocument to Mongo afi_reactor.reactor_scored_signals_v1, EXPLICITLY isolated from the afi-infra TSSD vault. The gateway persists VaultedSignalRecord (self-described as 'the CANONICAL record of a signal's full lifecycle … single source of truth') to the afi-infra TSSD vault. Both claim canonicality; both key on signalId; nothing joins them, and the reactor doc lacks the fields (epochId, stages, validator, minted) that the 'canonical' record requires.
- **Evidence:** `afi-reactor/src/services/tssdVaultService.ts:6`; `afi-reactor/src/services/froggyDemoService.ts:281-328`; `afi-infra/src/tssd/types.ts:320-367`; `afi-gateway/src/http/app.ts:33-57`
- **Consequence:** There is no single durable record of a signal's lifecycle. A scored signal in the reactor store can never be found by a consumer reading the 'canonical' TSSD vault, and vice-versa. Downstream mint/epoch logic (which expects TSSD identity) has no path to reactor-scored signals.
- **Recommended authority:** afi-governance + afi-infra (owns the canonical VaultedSignalRecord contract)
- **Minimal correction:** Designate one store as canonical and define the write path from the reactor scoring stage into it (or a documented, keyed bridge), before any further MongoDB machinery is built.
- **Flags:** Gov, pre-Mongo  |  **Suggested slot:** MONGO-GOV, OBJ-GOV  |  **Status:** open
- **Relationships:** cluster CL-01 (Two isolated 'canonical' scored-signal vaults with no identifier join (afi-infra TSSD VaultedSignalRecord vs afi-reactor self-isolated ReactorScoredSignalDocument)); depends-on LIFE-05

#### BG-11 — Emissions amount derivation teaches a governance-rejected formula, inlines a drift-prone schedule copy, and scales by unanchored multipliers → non-replayable allocation
- **Class/Severity/Confidence:** C4 · high · proven  |  **Repo:** afi-mint  |  **Dimension:** blockchain
- **Contradiction/gap:** GOVERNED D4 rejects the direct clamp(B(t)·Q·N·R·E) as mint authority, yet the implemented provider docstring teaches exactly that formula; it also duplicates the canonical afi-math schedule instead of importing the pinned one, and multiplies by reputationWeight/epochPulseFactor that are anchored nowhere on-chain.
- **Evidence:** `afi-mint/src/adapters/EmissionsMintDataProvider.ts:10-11,118 (docstring goldpaper clamp formula) vs :127-167 (actual proportional epoch-budget calc)`; `afi-mint/src/adapters/EmissionsMintDataProvider.ts:81,151,160,202 (baseMultiplier unused; unpinned reputationWeight & epochPulseFactor)`; `afi-governance/decisions/mint-formula-bt-86b-alignment-v0.1.md:89-98 (direct clamp NOT adopted as mint authority)`; `afi-docs/specs/audit/final/AFI_ONCHAIN_ANCHOR_GAP_ANALYSIS.md:127,151-153 (inlined schedule drift; unpinned multipliers non-replayable)`
- **Consequence:** The token-economics attachment point carries doc/impl divergence (deprecated formula in docstrings) plus a replay hazard: the minted amount cannot be independently reproduced from published rules because the ruleset/multipliers are neither imported canonically nor anchored.
- **Recommended authority:** afi-mint maintainer (align to afi-math canonical import); governance for multiplier pinning
- **Minimal correction:** Import the afi-math emissions schedule instead of the inlined copy and remove the deprecated clamp docstring, under explicit economic governance (Gate C).
- **Flags:** pre-Chain  |  **Suggested slot:** CHAIN-GOV (Gate B/C)  |  **Status:** open

#### CHAIN-01 — Settlement v1 four-layer doctrine self-labels CANONICAL/Accepted but is absent from afi-governance/decisions
- **Class/Severity/Confidence:** C4 · high · proven  |  **Repo:** afi-docs  |  **Dimension:** objects-econ
- **Contradiction/gap:** The five settlement specs and ADR-001/002/004/005/006 carry 'Status: CANONICAL — Accepted (v1 doctrine)' (e.g. AFI_EPOCH_SETTLEMENT_MANIFEST.md:3, AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md:2, ADR-002:2), yet afi-governance/decisions/ contains only math-authority, mint-formula-bt-86b, uwr-profile-pin, uwr-runtime-consumption — none ratifying epoch settlement, EpochSettlementManifest, ERC-6909 receipts, claimRoot, or reputation records. The only GOVERNED settlement statement is the narrower epoch-budget→role-pool→pro-rata-credits skeleton (mint-formula-bt-86b-alignment-v0.1.md:43,72-86), which is silent on manifest/claimRoot/receipt/vault machinery. Governance decisions even declare themselves 'subordinate to existing settlement/district doctrine in afi-docs' (mint-formula-bt-86b:5), treating unratified docs as authority.
- **Evidence:** `afi-docs/specs/AFI_EPOCH_SETTLEMENT_MANIFEST.md:3`; `afi-docs/specs/AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md:2`; `afi-governance/decisions/mint-formula-bt-86b-alignment-v0.1.md:5`; `afi-governance/decisions/mint-formula-bt-86b-alignment-v0.1.md:43`; `afi-governance/decisions/mint-formula-bt-86b-alignment-v0.1.md:72-86`
- **Consequence:** 'Canonical' status of the settlement object model is doc-self-asserted, not governed; a reader cannot tell which settlement statements carry governance authority. Any chain design built on the manifest/claimRoot/receipt machinery would rest on unratified doctrine while the governed skeleton (D3) neither adopts nor mentions that machinery.
- **Recommended authority:** afi-governance (new decision) reconciling afi-docs settlement corpus with mint-formula-bt-86b D3
- **Minimal correction:** Either promote the settlement doctrine set into an afi-governance decision that explicitly adopts (or scopes) the four-layer manifest/claimRoot/ERC-6909 architecture, or downgrade the specs' status labels from 'CANONICAL — Accepted' to documented-proposal until ratified.
- **Flags:** Gov, pre-Chain  |  **Suggested slot:** CHAIN-GOV  |  **Status:** open
- **Relationships:** cluster CL-02 (Authority inversion: afi-docs Settlement-V1/District doctrine self-declares CANONICAL and governance defers to it, with zero ratifying afi-governance decision)

#### CHAIN-02 — Role-set contradiction between two afi-docs settlement specs: four tracks (incl public-goods) vs three-only
- **Class/Severity/Confidence:** C4 · high · proven  |  **Repo:** afi-docs  |  **Dimension:** objects-econ
- **Contradiction/gap:** AFI_EPOCH_SETTLEMENT_MANIFEST.md (status CANONICAL — Accepted) defines roleAllocationRoots across FOUR tracks 'Providers, Analysts-Scorers, Validators, and public-goods' and names public-goods a residual destination (:85,88,90,121). AFI_SETTLEMENT_V1_MANIFEST_AND_PROVENANCE_SCHEMA.md (status DRAFT) and its claim-leaf law state THREE and only three tracks and that 'Governance and public-goods … MUST NOT appear as a role-allocation key, claim track, or budget line' (:120,241,252 CLM-GOV). The two canonical field registries disagree on the role set.
- **Evidence:** `afi-docs/specs/AFI_EPOCH_SETTLEMENT_MANIFEST.md:85`; `afi-docs/specs/AFI_EPOCH_SETTLEMENT_MANIFEST.md:88`; `afi-docs/specs/AFI_SETTLEMENT_V1_MANIFEST_AND_PROVENANCE_SCHEMA.md:120`; `afi-docs/specs/AFI_SETTLEMENT_V1_MANIFEST_AND_PROVENANCE_SCHEMA.md:241`; `afi-docs/specs/AFI_SETTLEMENT_V1_MANIFEST_AND_PROVENANCE_SCHEMA.md:252`
- **Consequence:** The canonical claim-leaf `role` domain and roleAllocationRoots key set are ambiguous: is public-goods a reward track or forbidden? Any manifest/claimRoot schema or reward-allocation code would be built against contradictory field registries; a public-goods budget line is simultaneously required (Layer 3) and prohibited (schema/Layer 4).
- **Recommended authority:** afi-docs settlement doctrine owner (Layer 3 vs Layer 4 authority order), escalated to owner because role scope touches tokenomics
- **Minimal correction:** Reconcile the two specs to one role set. The DRAFT (subordinate) cannot override the Accepted Layer-3 spec; either amend Layer 3 to move public-goods out of Settlement-v1 reward claims (matching CLM-GOV) or amend the schema/Layer-4 rule to re-include it — via an owner decision, since it is a tokenomics-scope question.
- **Flags:** Gov, pre-Chain  |  **Suggested slot:** CHAIN-GOV  |  **Status:** open
- **Relationships:** depends-on CHAIN-01

#### DIST-01 — Reactor 'District 2 M2' runtime shipped with no matching authorization instrument
- **Class/Severity/Confidence:** C4 · high · proven  |  **Repo:** afi-docs  |  **Dimension:** districts
- **Contradiction/gap:** The only D2 authorization instrument (afi-docs/reports/district-2-d17-implementation-authorization.md:17-19,23) authorizes 'District 2 M1 — afi-config schema drafts and tests only ... No runtime wiring', and §9 (:80-89) states 'Every implementation phase after M1 (M2–M6, and any successor) requires its own scoped PR/mission authorization.' Yet afi-reactor shipped 'District 2 M2: Make signal evaluation artifacts D2-native' as merged runtime code (PR #38, commits 79c4a6f/3ecaa31/8081a8d) in src/pipeheads/provenance/. No M2 authorization instrument exists in afi-docs/reports/ or afi-governance/decisions/ (directory listings show only D-17 for M1; governance decisions dir has only math-authority, mint-formula, uwr-profile-pin, uwr-runtime-consumption).
- **Evidence:** `afi-docs/reports/district-2-d17-implementation-authorization.md:17-23`; `afi-docs/reports/district-2-d17-implementation-authorization.md:80-89`; `afi-reactor/src/pipeheads/provenance/builders.ts:1-2`; `afi-reactor (git log) 79c4a6f 'District 2 M2: Make signal evaluation artifacts D2-native (#38)'`; `afi-config/codex/governance/droids/AFI_DROID_PIPEHEAD_ADDENDUM.v0.1.md:305-310`
- **Consequence:** A District 2 implementation phase reached main without the per-phase governance authorization its own instrument mandates; the governance trail cannot show who authorized M2, and any settlement/chain layer that later consumes these D2-native provenance artifacts inherits an unauthorized provenance foundation.
- **Recommended authority:** afi-governance (or a new afi-docs D2 mission-authorization instrument amending/succeeding D-17)
- **Minimal correction:** Issue a retroactive or forward D2 M2 (and, per DIST-03, M3/M4) authorization instrument, or record in the governance trail that the reactor D2-native surface is covered by the Pipehead Addendum POC authorization rather than the D2 milestone track.
- **Flags:** Gov, pre-Mongo, pre-Chain  |  **Suggested slot:** D-GOV  |  **Status:** open
- **Relationships:** cluster CL-05 (District-2 'M2' runtime shipped past its authorization and under a divergent milestone scope); depends-on DIST-03

#### F-PERSIST-04 — Reactor write is non-idempotent append with no durable dedup
- **Class/Severity/Confidence:** C4 · high · proven  |  **Repo:** afi-reactor  |  **Dimension:** persistence
- **Contradiction/gap:** tssdVaultService writes via plain insertOne with no unique index (reactor src has zero createIndex calls); the only dedup is an opt-in in-memory LRU (AFI_INGEST_DEDUPE=1) that never touches Mongo, is process-local, and is lost on restart.
- **Evidence:** `afi-reactor/src/services/tssdVaultService.ts:112`; `afi-reactor/src/services/ingestDedupeService.ts:1-32`; `afi-reactor/src/services/froggyDemoService.ts:330`
- **Consequence:** No durable one-record-per-signal guarantee on the primary demo spine; corrupts replay/novelty baselines and any mint reader keyed on signalId.
- **Recommended authority:** afi-reactor (behind MONGO-GOV canonical-store decision)
- **Minimal correction:** After the canonical-store decision, add a durable unique key / idempotent write on signalId in the reactor path (behind Gate A); not now.
- **Flags:** pre-Mongo, pre-Chain  |  **Suggested slot:** MONGO-GOV  |  **Status:** open

#### F-PERSIST-05 — Infra 'upsert' is a non-atomic findOne+deleteOne+insertOne on a time-series collection that cannot enforce a unique index
- **Class/Severity/Confidence:** C4 · high · proven  |  **Repo:** afi-infra  |  **Dimension:** persistence
- **Contradiction/gap:** MongoTSSDVaultClient.upsert reads, deletes, then inserts as three separate ops, and its intended unique index on identity.signalId is rejected by time-series collections so it silently falls back to a non-unique index.
- **Evidence:** `afi-infra/src/tssd/MongoTSSDVaultClient.ts:120-161`; `afi-infra/src/tssd/MongoTSSDVaultClient.ts:240-254`
- **Consequence:** The multi-tenant 'canonical' store has a data-integrity race and no enforceable identity; concurrency-unsafe for the very lifecycle-merge semantics it advertises.
- **Recommended authority:** afi-infra (behind MONGO-GOV canonical-store decision)
- **Minimal correction:** Choose a collection model that supports a unique signalId index or an atomic upsert path for the canonical store (behind Gate A); not now.
- **Flags:** pre-Mongo, pre-Chain  |  **Suggested slot:** MONGO-GOV  |  **Status:** open

#### OBJ-05 — Qualification gate is unwired: no path from persisted scored signal to the mint validator
- **Class/Severity/Confidence:** C4 · high · proven  |  **Repo:** afi-mint  |  **Dimension:** objects-core
- **Contradiction/gap:** afi-mint ValidatorDaemon depends on IAnalystScoreFetcher.getAnalystScore(signalId) (returning AnalystScoreInput) but there is NO concrete implementation of IAnalystScoreFetcher anywhere in afi-mint on main. Reactor persists ReactorScoredSignalDocument to its own 'reactor_scored_signals' collection, while SignalValidatorState.signalId is documented to 'link to TSSD vault' (afi-infra) — a store the reactor never writes to.
- **Evidence:** `afi-mint/src/orchestrator/ValidatorDaemon.ts:50-52`; `afi-mint/src/orchestrator/ValidatorDaemon.ts:295`; `afi-mint/src/orchestrator/ValidatorDaemon.ts:132`; `afi-mint/src/orchestrator/types.ts:98`; `afi-reactor/src/services/tssdVaultService.ts:59`; `afi-reactor/src/services/froggyDemoService.ts:330`; `afi-reactor/src/types/ReactorScoredSignalV1.ts:120`
- **Consequence:** The lifecycle scored-signal → qualified → challenge → mint is not connected on main; the validator cannot read reactor output. This is the exact attachment seam for mint/reward/settlement.
- **Recommended authority:** afi-mint (consumer) + afi-infra/afi-reactor (persistence owners)
- **Minimal correction:** Define/record the concrete read contract and store from which the validator fetches analyst scores by signalId (reactor collection vs afi-infra TSSD vault).
- **Flags:** pre-Mongo, pre-Chain  |  **Suggested slot:** LIFE-GOV  |  **Status:** open
- **Relationships:** cluster CL-06 (Reactor→mint validator bridge is unwired: no IAnalystScoreFetcher impl, daemon never instantiated, qualification gate dark); depends-on LIFE-06

#### BG-5 — No cryptographic on-chain anchor: MintCoordinated is a log-only breadcrumb; off-chain canonical hashes exist but are unwired; no contentHash/rulesetVersion/signalRoot/claimRoot on-chain
- **Class/Severity/Confidence:** C5 · high · proven  |  **Repo:** afi-token  |  **Dimension:** blockchain
- **Contradiction/gap:** Doctrine requires commit-on-chain/store-off-chain via Merkle/EAS roots binding mints to evidence + ruleset; on-chain there is no root or content hash (only event topics, calldata-only struct), and the off-chain per-signal hashes are connected to no on-chain sink.
- **Evidence:** `afi-token/src/AFIMintCoordinator.sol:19-26,85 (MintRequest calldata-only; signalId/epoch survive only as event topics)`; `afi-docs/specs/audit/final/AFI_ONCHAIN_ANCHOR_GAP_ANALYSIS.md:126,147 (grep contentHash|payloadHash|merkle|rulesetVersion over afi-token/src ⇒ 0 hits)`; `afi-reactor/src/pipeheads/provenance/builders.ts:571-596 (off-chain CanonicalHash v1 input/enrichment/output — per-signal, no on-chain wiring)`; `afi-docs/specs/AFI_SETTLEMENT_V1_DOCTRINE.md:129 (on-chain footprint MUST be roots/hashes, never raw)`
- **Consequence:** A third party can verify only 'an authorized role minted within the 86B cap', not that a mint was legitimately scored or bound to real evidence; provenance is recoverable only via an event indexer and lost if logs are pruned.
- **Recommended authority:** commitment-plane design under authorized settlement-v1 work
- **Minimal correction:** Design an on-chain root/hash commitment as part of the settlement design (Gate B); no cryptographic anchor exists today.
- **Flags:** pre-Chain  |  **Suggested slot:** CHAIN-GOV (Gate B/C)  |  **Status:** open
- **Relationships:** depends-on G-4

#### CORP-01 — Protocol law is authored and self-blessed in afi-docs; governance defers to it with no ratification record
- **Class/Severity/Confidence:** C5 · high · proven  |  **Repo:** afi-docs  |  **Dimension:** prior-audit-drafts
- **Contradiction/gap:** Settlement V1 / District doctrine docs in afi-docs/specs self-declare 'CANONICAL — Accepted (v1 doctrine)' and 'DECIDED', and every afi-governance decision declares itself 'Subordinate to ... existing settlement/district doctrine in afi-docs' — yet no governance decision ratifies any of these docs by name (rg for portable/settlement-v1/contradiction-register/north-star in afi-governance = 0 hits).
- **Evidence:** `afi-docs/specs/AFI_V0_DEPRECATION_AND_MIGRATION.md:3-5`; `afi-docs/specs/AFI_SETTLEMENT_V1_DOCTRINE.md:1-6`; `afi-docs/specs/audit/AFI_EVIDENCE_STORE_DECISION.md:3-7`; `afi-governance/decisions/math-authority-v0.1.md:6`; `afi-governance/decisions/uwr-runtime-consumption-v0.1.md:5`
- **Consequence:** Documents in a docs repo function as binding protocol law without a governance ratification trail; a doc edit silently changes 'law' that governance decisions are bound to, with no decision record to audit.
- **Recommended authority:** afi-governance (issue a decision that names and ratifies, or explicitly scopes, the afi-docs settlement/district doctrine the decisions defer to)
- **Minimal correction:** Ratify or explicitly demote the afi-docs settlement/district doctrine through an afi-governance decision (CHAIN-GOV); until then label it DOCUMENTED-non-canonical.
- **Flags:** Gov  |  **Suggested slot:** CHAIN-GOV  |  **Status:** open
- **Relationships:** cluster CL-02 (Authority inversion: afi-docs Settlement-V1/District doctrine self-declares CANONICAL and governance defers to it, with zero ratifying afi-governance decision)

#### F-PERSIST-02 — Evidence-store decision is DOCUMENTED in afi-docs, never GOVERNED — afi-governance has zero persistence decisions
- **Class/Severity/Confidence:** C6 · high · proven  |  **Repo:** afi-docs  |  **Dimension:** persistence
- **Contradiction/gap:** AFI_EVIDENCE_STORE_DECISION.md is marked 'Status: DECIDED' but lives in afi-docs; afi-governance/decisions/ contains only math/mint/uwr decisions and zero persistence/Mongo/finality/evidence-store decisions (grep: 0 hits).
- **Evidence:** `afi-docs/specs/audit/AFI_EVIDENCE_STORE_DECISION.md (Status: DECIDED, afi-docs path)`; `afi-governance/decisions/ (math-authority-v0.1.md, mint-formula-bt-86b-alignment-v0.1.md, uwr-profile-pin-v0.1.md, uwr-runtime-consumption-v0.1.md only)`
- **Consequence:** The single most load-bearing architectural claim of the persistence layer (Mongo = canonical) has no governance authority behind it. Any resumption of Mongo machinery rests on an unratified doc.
- **Recommended authority:** afi-governance
- **Minimal correction:** Ratify the evidence-store decision through afi-governance (MONGO-GOV) or mark AFI_EVIDENCE_STORE_DECISION DOCUMENTED-only.
- **Flags:** Gov, pre-Mongo  |  **Suggested slot:** MONGO-GOV  |  **Status:** open

#### F-PERSIST-03 — Finality/immutability of the 'canonical evidence store' is unimplemented and self-contradictory
- **Class/Severity/Confidence:** C6 · high · proven  |  **Repo:** afi-infra  |  **Dimension:** persistence
- **Contradiction/gap:** Docs call Mongo 'canonical protocol history / single source of truth / the dense brain', but the reactor path is a fail-soft append that duplicates freely, the infra path deletes-then-inserts and can TTL-expire records, the document version is a hard literal 'v1.0', and no code ever writes to chain or enforces immutability.
- **Evidence:** `afi-infra/src/tssd/types.ts:321-329`; `afi-reactor/src/services/tssdVaultService.ts:104-122`; `afi-infra/src/tssd/MongoTSSDVaultClient.ts:156-161,264-272`; `afi-reactor/src/services/froggyDemoService.ts:327`
- **Consequence:** Mongo cannot be relied on as protocol history: records are mutable/expirable/duplicable with no versioning or audit trail. The append-only-vs-mutable question must be decided before any downstream (mint/settlement) treats a Mongo record as final.
- **Recommended authority:** afi-governance (MONGO-GOV) for finality semantics; afi-infra for implementation
- **Minimal correction:** Decide finality/immutability semantics (append-only vs mutable, and whether TTL expiry is permitted) in MONGO-GOV before any implementation; a canonical evidence store must not silently auto-expire.
- **Flags:** Gov, pre-Mongo, pre-Chain  |  **Suggested slot:** MONGO-GOV  |  **Status:** open

#### F-PERSIST-06 — Lifecycle stages beyond SCORED (validator/minted/replayed) are type-only; Mongo→mint read edge is unimplemented
- **Class/Severity/Confidence:** C6 · high · proven  |  **Repo:** afi-infra  |  **Dimension:** persistence
- **Contradiction/gap:** VaultedSignalRecord models RAW→…→MINTED→REPLAYED with a full ValidatorSnapshot/MintSnapshot, but no runtime code writes validator/minted/replayed stages; the gateway copies client-supplied stages verbatim; and afi-mint has no mongodb dependency and zero vault/tssd/reactor_scored references.
- **Evidence:** `afi-infra/src/tssd/types.ts:10-16,187-318`; `afi-gateway/src/http/app.ts:44`; `afi-mint/package.json (no mongodb dep)`; `afi-mint/src (0 mongo/vault/tssd refs)`; `afi-docs/specs/audit/AFI_MONGO_TSSD_INVENTORY.md:103,200`
- **Consequence:** The 'pre-chain staging' role and the Mongo→mint attachment are aspirational: the schema promises a chain-attached lifecycle no code produces, and the mint reader seam is a documented gap only. Chain attachment cannot begin until a writer/owner for these stages and a mint read edge are decided.
- **Recommended authority:** afi-governance (LIFE-GOV) for the seam contract; afi-mint/afi-infra for later wiring
- **Minimal correction:** Define the Mongo->mint read seam (ISignalMetadataFetcher/IAnalystScoreFetcher) in LIFE-GOV as an interface only; do not wire it now.
- **Flags:** Gov, pre-Chain  |  **Suggested slot:** MONGO-GOV  |  **Status:** open

#### LIFE-03 — Canonicalization-without-persistence vs persistence-without-canonicalization
- **Class/Severity/Confidence:** C6 · high · proven  |  **Repo:** afi-reactor  |  **Dimension:** lifecycle
- **Contradiction/gap:** The D2 pipehead harness computes the protocol's canonical, hash-anchored, replayable artifacts (AnalystInputEnvelope/ScoredSignal/ProvenanceRecord/ReplayProfile v1) but is invoked only by a CLI demo and tests — never by server.ts and never persisted. The deployed server persists ReactorScoredSignalDocument, which contains exactly the runtime/storage baggage (rawUss, lenses, _priceFeedMetadata) that ScoredSignal v1 was explicitly designed to exclude, and carries no ProvenanceRecord/hash/replay pin.
- **Evidence:** `afi-reactor/src/pipeheads/harness.ts:145-202`; `afi-reactor/src/pipeheads/provenance/types.ts:141-143`; `afi-reactor/src/pipeheads/provenance/types.ts:168-170`; `afi-reactor/src/services/froggyDemoService.ts:239-265`
- **Consequence:** The stored record is neither canonical nor independently verifiable/replayable; the canonical artifacts that would make a signal auditable and hash-anchorable are discarded. Any on-chain provenance anchor (MintCoordinated) has no persisted ProvenanceRecord to point at.
- **Recommended authority:** afi-reactor (owns both surfaces) under an afi-governance canonicalization decision
- **Minimal correction:** Route the deployed scoring path through (or additionally emit and persist) the D2 provenance artifacts, keyed by signalId, so the persisted record carries the canonical hash + replay profile.
- **Flags:** Gov, pre-Mongo, pre-Chain  |  **Suggested slot:** LIFE-GOV, OBJ-GOV  |  **Status:** open
- **Relationships:** cluster CL-07 (Scored-signal split: the canonical D2 draft is computed but never persisted, while a non-canonical runtime doc is what actually persists)

#### BG-12 — The entire Settlement v1 four-layer design is DOCUMENTED (afi-docs, owner-locked) but not an afi-governance decision, and the sole governance mint record authorizes no code/contract change
- **Class/Severity/Confidence:** C7 · high · proven  |  **Repo:** afi-docs  |  **Dimension:** blockchain
- **Contradiction/gap:** Attachment-point design is treated by contributors as canonical, but authority-wise the four-layer architecture lives only in afi-docs specs/ADRs (which self-declare they implement nothing), while the one afi-governance decision explicitly forbids contract/schema/afi-mint/afi-token changes and defers role weights and activation.
- **Evidence:** `afi-docs/specs/AFI_SETTLEMENT_V1_DOCTRINE.md:7 (doctrine implements nothing on-chain)`; `afi-docs/adrs/ADR-001-four-layer-settlement-architecture.md:14 (doctrine and design only)`; `afi-governance/decisions/mint-formula-bt-86b-alignment-v0.1.md:150-172 (Explicit Non-Authorization of contract/schema/afi-mint/afi-token/role-weight changes)`; `afi-governance/decisions/mint-formula-bt-86b-alignment-v0.1.md:3,5 (does not authorize implementation; subordinate to afi-docs settlement doctrine)`
- **Consequence:** No governance authorization currently exists to build any settlement/chain attachment point; proceeding to design would outrun the governance envelope. This is the meta-gate over G-4/G-6/G-7/G-8.
- **Recommended authority:** afi-governance decision promoting settlement-v1 from docs to authorized build + owner
- **Minimal correction:** Ratify or explicitly scope the Settlement-v1 four-layer doctrine into an afi-governance decision (CHAIN-GOV).
- **Flags:** Gov, pre-Chain  |  **Suggested slot:** CHAIN-GOV (Gate B/C)  |  **Status:** open

#### BG-8 — RewardsVault / claim / vault-routing layer is entirely unbuilt and its destination addresses are placeholder, lane-collapsed Safes
- **Class/Severity/Confidence:** C7 · high · proven  |  **Repo:** afi-config  |  **Dimension:** blockchain
- **Contradiction/gap:** ADR-004 requires a RewardsVault custody+claim layer funded lump-sum with cap enforced at the funding seam and a reconciled N-of-M controller; no vault exists and every candidate destination is an empty placeholder Safe with no lane segregation.
- **Evidence:** `afi-config/registries/afi-vault-address-registry.v1.json:463 (W-NO-REWARDS-VAULT: Settlement v1 RewardsVault is unbuilt)`; `afi-config/registries/afi-vault-address-registry.v1.json:458,460 (treasury.afidao.eth ≠ real Base Treasury Safe; treasury/grants/ops/liq all resolve to one Safe 0x7408)`; `afi-docs/adrs/ADR-004-rewards-vault-merkle-claims.md:93-124,182-191 (custody-not-mint, pay-only-against-claimRoot, N-of-M controller)`; `afi-config/registries/afi-vault-address-registry.v1.json:2-5 (registry is draft-owner-review, descriptive only)`
- **Consequence:** Plane (4) payout has no implemented custody, claiming, or routing seam and no reconciled governed destination address; the whole claiming/vault-routing map is documented-only.
- **Recommended authority:** owner (address reconciliation, Safe topology) + governance
- **Minimal correction:** Reconcile the vault-address-registry placeholders (lane collapse, treasury mismatch) and design the RewardsVault/claim layer behind Gate B/C.
- **Flags:** Gov, pre-Chain  |  **Suggested slot:** CHAIN-GOV (Gate B/C)  |  **Status:** open
- **Relationships:** depends-on G-4


### 3.3 Medium severity (33)

#### CORP-04 — Systemic file:line drift in the audit finals — cites predate the District-2 reactor/gateway rewrite
- **Class/Severity/Confidence:** C1 · medium · proven  |  **Repo:** afi-docs  |  **Dimension:** prior-audit-drafts
- **Contradiction/gap:** Evidence citations in the finals were captured at a pre-District-2 commit and no longer resolve: C-RO-1 cites afi-reactor/README.md:137 for 'ONLY orchestrator' (now README.md:200 / AGENTS.md:3); gateway ingest is now identity-nested vs the cited flat payload; TSSDVaultClient mongo-required guard moved off line 200.
- **Evidence:** `afi-docs/specs/AFI_CONTRADICTION_REGISTER.md:93`; `afi-reactor/README.md:200`; `afi-reactor/AGENTS.md:3`; `afi-gateway/src/http/app.ts:26`
- **Consequence:** Substance of most rows holds, but the line anchors are unreliable, so re-verification is manual; a reader cannot trust the register's file:line as current.
- **Recommended authority:** afi-docs (re-anchor cites during M6 sync)
- **Minimal correction:** Re-anchor drifted file:line citations to current main during the scheduled M6 contradiction-register sync.
- **Flags:** none  |  **Suggested slot:** CORP-SYNC  |  **Status:** open
- **Relationships:** cluster CL-13 (Prior audit corpus is a known-stale snapshot post-District-2 (resolved rows still marked confirmed; file:line cites drifted))

#### CORP-06 — Canonical v0-deprecation doctrine sources its facts from two recon reports absent from the repo
- **Class/Severity/Confidence:** C1 · medium · proven  |  **Repo:** afi-docs  |  **Dimension:** prior-audit-drafts
- **Contradiction/gap:** AFI_V0_DEPRECATION_AND_MIGRATION.md (self 'CANONICAL — Accepted') anchors its v0 facts on reports/afi-vault-architecture-recon.md and reports/afi-onchain-contract-discovery.md, but afi-docs/reports/ contains only 4 unrelated District/Settlement files — neither referenced report exists (memory: reports/ is unversioned).
- **Evidence:** `afi-docs/specs/AFI_V0_DEPRECATION_AND_MIGRATION.md:17-18`; `afi-docs/specs/AFI_V0_DEPRECATION_AND_MIGRATION.md:171`; `afi-docs/reports/`
- **Consequence:** A CANONICAL doctrine's evidentiary base is unverifiable/dangling; readers cannot check the on-chain 'facts' (totalSupply=0, incomplete role wiring, single-Safe authority) it relies on.
- **Recommended authority:** afi-docs (commit the recon reports or repoint the doctrine to surviving sources)
- **Minimal correction:** Vendor or cite the two referenced recon reports in-repo, or remove the dangling references that the v0-deprecation doctrine depends on.
- **Flags:** pre-Chain  |  **Suggested slot:** DIST-DOC  |  **Status:** open

#### GW-01 — Atlas gateway entry is stale: fabricated Phoenix persona, omits the entire /api/v1 REST surface
- **Class/Severity/Confidence:** C1 · medium · proven  |  **Repo:** afi-docs  |  **Dimension:** gateway-runtime
- **Contradiction/gap:** Atlas:29 describes an 'active Phoenix concierge persona (src/*.character.ts)' but no *.character.ts files exist (find → 0; 'phoenix' is only a package.json keyword). Atlas:34-35 describes the gateway as only 'HTTP health/ping and full Eliza API', omitting the implemented /api/v1 api-keys, signals→TSSD, and skills routes (app.ts:82-181).
- **Evidence:** `afi-docs/AFI_System_Atlas.md:29`; `afi-docs/AFI_System_Atlas.md:34-35`; `afi-gateway/src/http/app.ts:77-181`; `afi-gateway/src/afiscout/index.ts:4-10`; `afi-gateway/package.json:29`
- **Consequence:** The API-Atlas cannot be trusted as a route/contract inventory for the gateway: it advertises a persona/surface that does not exist and hides the only data-persisting API, misleading integrators and downstream reconciliation.
- **Recommended authority:** afi-docs (Atlas maintainer)
- **Minimal correction:** Rewrite the afi-gateway Atlas entries to reflect the three actual entrypoints and the /api/v1 REST contract; drop the Phoenix/*.character.ts claim or mark it PROPOSED.
- **Flags:** none  |  **Suggested slot:** ATLAS-DOC  |  **Status:** open
- **Relationships:** cluster CL-12 (System Atlas is stale re: the gateway — dead absolute macOS path, omits the entire /api/v1 surface, fabricates a Phoenix concierge persona)

#### GW-08 — Three disjoint gateway servers with inconsistent versioning; default start exposes no data plane
- **Class/Severity/Confidence:** C1 · medium · proven  |  **Repo:** afi-gateway  |  **Dimension:** gateway-runtime
- **Contradiction/gap:** package.json start=server-full.js (ElizaOS AgentServer, /api/agents + /api/afi/info v0.1.0, no agents started), start:minimal=server.js (/api/v1 REST), start:cli=cli.js. Versioning is mixed: /api/v1 (app.ts) vs /api/afi/info (server-full.ts:120) vs unversioned /api/agents. The default 'npm start' runs the ElizaOS server, which exposes none of the /api/v1 data routes.
- **Evidence:** `afi-gateway/package.json:9-21`; `afi-gateway/src/server-full.ts:91-125`; `afi-gateway/src/http/app.ts:82-181`; `afi-gateway/src/index.ts:60-107`
- **Consequence:** No single canonical 'gateway' contract; deployers who run the documented default (start) get the agent server with no persistence surface and no agents, while the REST API only runs under start:minimal. Reconciliation and Atlas mapping are ambiguous about which is 'the gateway'.
- **Recommended authority:** afi-gateway maintainer
- **Minimal correction:** Declare the canonical production entrypoint and unify route versioning; document the other surfaces as dev/optional.
- **Flags:** none  |  **Suggested slot:** GW-HYGIENE  |  **Status:** open

#### ATLAS-01 — System Atlas documents a reactor replay endpoint that is not implemented
- **Class/Severity/Confidence:** C2 · medium · proven  |  **Repo:** afi-docs  |  **Dimension:** api-atlas
- **Contradiction/gap:** AFI_System_Atlas.md:13 asserts reactor exposes replay endpoints `/replay/signal/:signalId`, but the reactor server registers only /health, gated /debug/env, POST /api/webhooks/tradingview, POST /api/ingest/cpj — no /replay route exists anywhere in afi-reactor/src or ops.
- **Evidence:** `afi-docs/AFI_System_Atlas.md:13`; `afi-reactor/src/server.ts:80`; `afi-reactor/src/server.ts:97`; `afi-reactor/src/server.ts:159`; `afi-reactor/src/server.ts:290`
- **Consequence:** Consumers/SDK authors expecting a replay HTTP surface will 404; replay-readiness claims in downstream reports rest on a nonexistent endpoint.
- **Recommended authority:** afi-docs (owns System Atlas); afi-reactor confirms route set
- **Minimal correction:** Remove the /replay/signal/:signalId claim from AFI_System_Atlas.md:13 or implement the route.
- **Flags:** none  |  **Suggested slot:** ATLAS-DOC  |  **Status:** open
- **Relationships:** cluster CL-09 (Documented reactor replay endpoint /replay/signal/:signalId does not exist)

#### ATLAS-03 — SDK READMEs advertise an AFIClient API surface that has no code and mismatches the real ingest contract
- **Class/Severity/Confidence:** C2 · medium · strongly-supported  |  **Repo:** afi-sdk  |  **Dimension:** api-atlas
- **Contradiction/gap:** afi-sdk-ts/README.md and afi-sdk-python/README.md document AFIClient against https://api.afi.protocol with client.signals.submit({type:'market-data', data:{...}}). No SDK source exists (README + package.json only), and the documented payload does not match the real gateway contract POST /api/v1/signals which requires identity.{signalId,epochId,market,timeframe} (afi-gateway/src/http/app.ts:26-30).
- **Evidence:** `afi-sdk-ts/README.md:1-45`; `afi-sdk-python/README.md:1-30`; `afi-gateway/src/http/app.ts:26`; `afi-gateway/src/http/app.ts:123`
- **Consequence:** Anyone building on the published SDK contract writes to a non-existent client and an incompatible request shape.
- **Recommended authority:** afi-sdk-ts / afi-sdk-python owners; must track afi-gateway ingest schema
- **Minimal correction:** Mark SDKs as scaffolds-only and align the documented submit() shape with /api/v1/signals identity fields.
- **Flags:** none  |  **Suggested slot:** ATLAS-DOC  |  **Status:** open

#### CHAIN-05 — Reputation record is DOCUMENTED intent only; implemented reputation surface is placeholder + simulation, not the canonical record
- **Class/Severity/Confidence:** C2 · medium · proven  |  **Repo:** afi-docs  |  **Dimension:** objects-econ
- **Contradiction/gap:** The canonical reputation record — the ERC-6909 strategy/epoch receipt (AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md:23,65-68,125-138) and the PROPOSED strategy leaf (…SCHEMA.md:210-226) — has no implementation: no ERC-6909/IERC6909 contract exists in afi-token/afi-mint/afi-xerc20 on main (grep: none). The implemented reputation surface is a stub bridge whose computeEmissionWeights returns [] (afi-mint/src/reputation_bridge.ts:47-99, header 'All logic here is placeholder'), plus economic simulation (afi-econ/src/models/rewards/agentReputationModel.ts:19-41) and poi/poInsight score fields.
- **Evidence:** `afi-docs/specs/AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md:23`; `afi-docs/specs/AFI_SETTLEMENT_V1_MANIFEST_AND_PROVENANCE_SCHEMA.md:210-226`; `afi-mint/src/reputation_bridge.ts:91-99`; `afi-econ/src/models/rewards/agentReputationModel.ts:19-41`
- **Consequence:** 'Reputation records' are intent, not real deployed schemas; the runtime 'reputation' inputs (ReputationSnapshotInput) are placeholder and unrelated to the governed/soulbound receipt semantics, so any claim that reputation is captured on-chain would be false today.
- **Recommended authority:** afi-docs Layer-2 owner + afi-mint
- **Minimal correction:** Keep reputation_bridge and agentReputationModel labeled as placeholder/simulation (they already are) and do not present them as the Layer-2 reputation record; track the ERC-6909 receipt as unbuilt.
- **Flags:** pre-Chain  |  **Suggested slot:** CHAIN-ATTACH  |  **Status:** open
- **Relationships:** depends-on CHAIN-01

#### CORP-05 — AFI_AUDIT_CHECKPOINT internally contradicts itself on completion and carries a pre-promotion date
- **Class/Severity/Confidence:** C2 · medium · proven  |  **Repo:** afi-docs  |  **Dimension:** prior-audit-drafts
- **Contradiction/gap:** The checkpoint's Investigation Status marks all four phases Complete/promoted, while its Source Provenance table records theme agents 0/10 and synthesis 0/6 all FAILED (API rate limit); 'Last updated 2026-06-15' predates the finals' actual promotion commit 02c01bf on 2026-06-25.
- **Evidence:** `afi-docs/specs/audit/AFI_AUDIT_CHECKPOINT.md:14-20`; `afi-docs/specs/audit/AFI_AUDIT_CHECKPOINT.md:31-32`; `afi-docs/specs/audit/AFI_AUDIT_CHECKPOINT.md:4`
- **Consequence:** The 'read this first when resuming' document cannot be trusted about its own completion state or date, undermining its role as the corpus entry point.
- **Recommended authority:** afi-docs
- **Minimal correction:** Reconcile AFI_AUDIT_CHECKPOINT's internal completion state and correct its pre-promotion date to the current baseline.
- **Flags:** none  |  **Suggested slot:** CORP-SYNC  |  **Status:** open

#### CORP-07 — Mongo 'canonical evidence store' decision narrowed by newer District-2 doctrine to 'reference impl, not canon'
- **Class/Severity/Confidence:** C2 · medium · strongly-supported  |  **Repo:** afi-docs  |  **Dimension:** prior-audit-drafts
- **Contradiction/gap:** AFI_EVIDENCE_STORE_DECISION.md and AFI_MONGO_TSSD_INVENTORY.md call MongoDB TSSD 'the canonical reference evidence store'; District 2 M0 doctrine reframes that as naming 'the reference implementation, NOT protocol canon ... the datastore is swappable.' The older 'DECIDED' doc's canon-flavored language conflicts with the newer doctrine's boundary framing.
- **Evidence:** `afi-docs/specs/audit/AFI_EVIDENCE_STORE_DECISION.md:7`; `afi-docs/specs/audit/AFI_MONGO_TSSD_INVENTORY.md:3`; `afi-docs/reports/district-2-m0-canonical-data-boundary-and-hash-doctrine.md:611`
- **Consequence:** Ambiguity over whether Mongo is protocol canon or a swappable backend directly affects any resumption of MongoDB machinery and the persistence-map dimension.
- **Recommended authority:** afi-docs / District 2 (M0 doctrine is the more recent authority)
- **Minimal correction:** Reconcile AFI_EVIDENCE_STORE_DECISION's 'canonical evidence store' against the newer District-2 'reference implementation' framing inside MONGO-GOV.
- **Flags:** pre-Mongo  |  **Suggested slot:** MONGO-GOV  |  **Status:** open

#### DIST-02 — Numbered 'District 1/District 2' scheme has no governance basis; governance names districts functionally and never numbers them
- **Class/Severity/Confidence:** C2 · medium · proven  |  **Repo:** afi-config  |  **Dimension:** districts
- **Contradiction/gap:** The governing instrument (AFI_DROID_PIPEHEAD_ADDENDUM.v0.1.md) names the first district by function ('Signal Evaluation Pipehead System', :297) and lists future districts by function only — 'provenance, reputation, contracts, settlement-readiness, monitoring, docs, and external agent interfaces' (:307) — and NEVER assigns any number. The numbers 'District 1'/'District One' (afi-docs/reports/afi-signal-evaluation-pipehead-system-report.md:258; reactor README:146) and 'District 2'/'D2' (afi-docs/reports/district-2-m0-...md:1,5; reactor code comments throughout src/pipeheads/) are a documentation/code convention with no governance decision behind them.
- **Evidence:** `afi-config/codex/governance/droids/AFI_DROID_PIPEHEAD_ADDENDUM.v0.1.md:297`; `afi-config/codex/governance/droids/AFI_DROID_PIPEHEAD_ADDENDUM.v0.1.md:307-310`; `afi-docs/reports/afi-signal-evaluation-pipehead-system-report.md:258`; `afi-docs/reports/district-2-m0-canonical-data-boundary-and-hash-doctrine.md:1`
- **Consequence:** Two district-identity models coexist (governance-functional vs docs-numbered) with no mapping instrument; future districts from the roster (reputation, contracts, etc.) have no governed number, so 'District 3+' could be minted inconsistently by whichever repo names it first.
- **Recommended authority:** afi-governance (canonical district registry mapping functional roster names ↔ numbers)
- **Minimal correction:** Adopt one canonical scheme in a governance instrument — either drop the numbers or record an explicit functional-name↔number mapping (provenance=District 2, etc.).
- **Flags:** Gov  |  **Suggested slot:** D-GOV  |  **Status:** open
- **Relationships:** cluster CL-04 (Numbered District 1/2 scheme has no governance basis; districts are authorized only in afi-docs)

#### DIST-H-05 — afi-gateway reaches into afi-infra internal source paths — no published API boundary
- **Class/Severity/Confidence:** C2 · medium · proven  |  **Repo:** afi-gateway  |  **Dimension:** repo-authority
- **Contradiction/gap:** afi-gateway imports afi-infra via deep source paths (afi-infra/src/tssd/index.js, /types.js, /MongoTSSDVaultClient.js) rather than a package entry, because afi-infra's package.json declares main:null with no exports map. There is no encapsulated API surface for the canonical persistence layer; consumers bind to internal file layout.
- **Evidence:** `afi-gateway/src/services/vaultFactory.ts:1-3`; `afi-gateway/src/http/app.ts:8`; `afi-infra/package.json`
- **Consequence:** Any refactor of afi-infra's src/tssd layout silently breaks the gateway; the persistence owner cannot evolve internals behind a contract, undermining infra's role as authoritative persistence provider.
- **Recommended authority:** afi-infra
- **Minimal correction:** Give afi-infra a package main/exports that publishes the TSSD client + VaultedSignalRecord type, and have gateway import from the package root instead of src/*.js.
- **Flags:** pre-Mongo  |  **Suggested slot:** OBJ-CORE-INFRA  |  **Status:** open
- **Relationships:** depends-on DIST-H-04

#### DIST-H-06 — afi-mint peerDependencies reference package names that do not exist
- **Class/Severity/Confidence:** C2 · medium · proven  |  **Repo:** afi-mint  |  **Dimension:** repo-authority
- **Contradiction/gap:** afi-mint declares peerDependencies '@afi-protocol/afi-core' and '@afi-protocol/afi-infra', but the actual published names of those packages are the unscoped 'afi-core' (afi-core/package.json name) and 'afi-infra' (afi-infra/package.json name). The declared peer constraint can never resolve against the real workspace packages.
- **Evidence:** `afi-mint/package.json`; `afi-core/package.json`; `afi-infra/package.json`
- **Consequence:** The mint→core/infra dependency edge is unenforceable; peer-version checks are inert, so the settlement-execution repo's declared dependency direction is fiction — a real defect before mint/settlement wiring.
- **Recommended authority:** afi-mint
- **Minimal correction:** Rename mint peerDeps to the actual package names (afi-core, afi-infra) or standardize all core/infra packages under the @afi-protocol scope (see DIST-H-08).
- **Flags:** pre-Chain  |  **Suggested slot:** GW-HYGIENE  |  **Status:** open
- **Relationships:** cluster CL-15 (Package naming/scoping has no authority (some @afi-protocol/*, some bare, some @afi/*); afi-mint peerDependencies name packages that do not exist); depends-on DIST-H-08

#### DIST-H-07 — afi-reactor .afi-codex.json dependency metadata does not match real edges
- **Class/Severity/Confidence:** C2 · medium · proven  |  **Repo:** afi-reactor  |  **Dimension:** repo-authority
- **Contradiction/gap:** reactor .afi-codex.json dependsOn lists afi-math and afi-plugins (neither appears in reactor/package.json) and omits afi-factory (a real file: dep); it also lists consumers afi-ops and afi-infra, though afi-infra's package.json depends on afi-core, not afi-reactor. math-authority-v0.1.md §5 already flagged the afi-math metadata as 'not aligned with the current dependency lineage'.
- **Evidence:** `afi-reactor/.afi-codex.json:19-30`; `afi-reactor/package.json`; `afi-infra/package.json`; `afi-governance/decisions/math-authority-v0.1.md:106-108`
- **Consequence:** Codex/atlas discovery built from .afi-codex.json metadata produces a wrong dependency graph — inventing a reactor→afi-math edge that governance says must NOT exist (reactor is 'not a math authority') and hiding the real reactor→afi-factory edge.
- **Recommended authority:** afi-reactor
- **Minimal correction:** Reconcile reactor .afi-codex.json dependsOn/consumers to package.json reality: drop afi-math + afi-plugins, add afi-factory, correct consumers.
- **Flags:** none  |  **Suggested slot:** GW-HYGIENE  |  **Status:** open

#### OBJ-04 — "Validation" is overloaded: five schema *ValidationResult types vs the mint validator's certification decision
- **Class/Severity/Confidence:** C2 · medium · proven  |  **Repo:** afi-reactor  |  **Dimension:** objects-core
- **Contradiction/gap:** reactor/core 'validation' means schema/USS conformance (ValidationResult, UssValidationResult, D2ValidationResult, DAGValidationResult, SignalEnvelopeValidationResult), while afi-mint 'validation'/'Validator' means signal certification (ValidatorDecisionKind, SignalValidatorState). The word Validator/Validation spans two unrelated concerns with no naming boundary.
- **Evidence:** `afi-reactor/src/uss/ussValidator.ts:24`; `afi-reactor/src/types/pipeline.ts:233`; `afi-core/src/dag/SignalEnvelope.ts`; `afi-mint/src/orchestrator/types.ts:47`; `afi-mint/src/orchestrator/types.ts:115`; `afi-reactor/src/types/ReactorScoredSignalV1.ts:8`
- **Consequence:** Discussions/specs conflate schema validation with certification; a 'validation result' in one repo is unrelated to a 'validator decision' in another.
- **Recommended authority:** afi-governance terminology / district glossary
- **Minimal correction:** Reserve 'validation' for schema conformance and 'certification/qualification' for the validator decision in shared terminology.
- **Flags:** pre-Chain  |  **Suggested slot:** LIFE-GOV, OBJ-GOV  |  **Status:** open

#### OBJ-06 — TssdVaultService / 'tssd-vault-write' names collide with the afi-infra TSSD vault it is explicitly NOT
- **Class/Severity/Confidence:** C2 · medium · proven  |  **Repo:** afi-reactor  |  **Dimension:** objects-core
- **Contradiction/gap:** The reactor's persistence service is named TssdVaultService and its pipeline stage 'tssd-vault-write', yet code and comments state it writes a Reactor-owned collection 'isolated from afi-infra TSSD vault'. The real TSSD vault is afi-infra MongoTSSDVaultClient. Mint expects signals in 'TSSD vault'.
- **Evidence:** `afi-reactor/src/services/tssdVaultService.ts:6`; `afi-reactor/src/services/tssdVaultService.ts:41`; `afi-reactor/src/services/froggyDemoService.ts:189`; `afi-reactor/src/types/ReactorScoredSignalV1.ts:120`; `afi-infra/src/tssd/MongoTSSDVaultClient.ts`; `afi-mint/src/orchestrator/types.ts:98`
- **Consequence:** Persistence-map ambiguity: readers cannot tell whether 'TSSD vault' means the reactor-owned collection or the afi-infra vault, compounding LIFE-05.
- **Recommended authority:** afi-reactor + afi-infra
- **Minimal correction:** Rename or disambiguate the reactor service/stage, and record the authoritative store name for scored signals.
- **Flags:** pre-Mongo, pre-Chain  |  **Suggested slot:** MONGO-PERSIST, OBJ-GOV, OBJ-REACTOR  |  **Status:** open
- **Relationships:** cluster CL-01 (Two isolated 'canonical' scored-signal vaults with no identifier join (afi-infra TSSD VaultedSignalRecord vs afi-reactor self-isolated ReactorScoredSignalDocument))

#### DIST-03 — 'District 2 M2' means different scopes in the M0 milestone plan vs the shipped reactor code
- **Class/Severity/Confidence:** C3 · medium · proven  |  **Repo:** afi-docs  |  **Dimension:** districts
- **Contradiction/gap:** The M0 report's milestone table (district-2-m0-...md:551, §11) defines M2 = 'Canonical hash unification' (implement CanonicalHash v1, migrate ingestHash), with 'Reactor production provenance wiring' as M3 and 'Analyst input envelope integration' as M4. The reactor's shipped 'District 2 M2' (PR #38) instead delivers the full D2-native artifact surface — AnalystInputEnvelope v1 + ProvenanceRecord v1 + ScoredSignal v1 + CanonicalHash v1 (afi-reactor/docs/PIPEHEAD_SYSTEM.md:69; src/pipeheads/types.ts:7; provenance/envelopePipehead.ts) — collapsing documented M2+M3+M4 into a single 'M2' label.
- **Evidence:** `afi-docs/reports/district-2-m0-canonical-data-boundary-and-hash-doctrine.md:551`; `afi-reactor/docs/PIPEHEAD_SYSTEM.md:69-72`; `afi-reactor/src/pipeheads/types.ts:7`; `afi-reactor/src/pipeheads/provenance/envelopePipehead.ts:3`
- **Consequence:** The 'M2' identifier is ambiguous: a reader cannot tell whether 'M2' means the hash-unification milestone or the reactor artifact-surface milestone, which undermines the per-phase authorization gating (DIST-01) since the phase names no longer line up.
- **Recommended authority:** afi-docs (reconcile the milestone plan with the shipped reactor milestone naming)
- **Minimal correction:** Either renumber the reactor deliverable to match the M0 plan (M2/M3/M4) or amend the M0 §11 table to reflect the collapsed scope, and record which milestone each shipped artifact satisfies.
- **Flags:** Gov  |  **Suggested slot:** DIST-DOC  |  **Status:** open
- **Relationships:** cluster CL-05 (District-2 'M2' runtime shipped past its authorization and under a divergent milestone scope); depends-on DIST-01

#### DIST-H-08 — Orphaned afi-infra signal schemas define a competing 'scored signal' shape consumed by nothing
- **Class/Severity/Confidence:** C3 · medium · proven  |  **Repo:** afi-infra  |  **Dimension:** repo-authority
- **Contradiction/gap:** afi-infra ships a full set of signal schemas (schemas/signal_scoring_schema.ts etc. + afi-codex/*.afi-codex.json) whose SignalScoringSchema uses strength/confidence (0-1) and aiConsensusScore (0-100) — a different scored-signal shape than afi-config's canonical scored-signal.schema.json / UWR four-axis model. No file in afi-reactor, afi-core, or afi-gateway imports these infra schemas; they are dead but present, asserting a rival domain-object definition.
- **Evidence:** `afi-infra/schemas/signal_scoring_schema.ts:5-14`; `afi-infra/afi-codex/signal_scoring_schema.afi-codex.json`; `afi-config/schemas/provenance/v1/scored-signal.schema.json`
- **Consequence:** Object-identity reconnaissance finds two incompatible 'scored signal' schemas across infra vs config; a future implementer could wire the wrong one. Latent contradiction in what a scored signal IS.
- **Recommended authority:** afi-config
- **Minimal correction:** Either retire the unused afi-infra signal schemas or explicitly mark them non-authoritative and cross-reference afi-config as the canonical scored-signal owner.
- **Flags:** pre-Mongo  |  **Suggested slot:** OBJ-CORE-INFRA, OBJ-GOV  |  **Status:** open

#### GW-03 — GET /api/v1/skills/capabilities is permanently shadowed by /skills/:id
- **Class/Severity/Confidence:** C3 · medium · proven  |  **Repo:** afi-gateway  |  **Dimension:** gateway-runtime
- **Contradiction/gap:** app.ts registers /api/v1/skills/:id (line 162) BEFORE /api/v1/skills/capabilities (line 173). Express matches in registration order, so a request to /api/v1/skills/capabilities binds :id='capabilities', calls getSkillById('capabilities'), finds no such skill, and returns 404 not_found. The capabilities summary endpoint is unreachable.
- **Evidence:** `afi-gateway/src/http/app.ts:162-171`; `afi-gateway/src/http/app.ts:173-181`
- **Consequence:** summarizeCapabilities is never served over HTTP; any client relying on GET /api/v1/skills/capabilities gets a 404. Not caught by tests (skills.test.ts exercises the service, not the routes).
- **Recommended authority:** afi-gateway maintainer
- **Minimal correction:** Register /api/v1/skills/capabilities before /api/v1/skills/:id (or constrain the :id param).
- **Flags:** none  |  **Suggested slot:** GW-HYGIENE  |  **Status:** open
- **Relationships:** cluster CL-10 (GET /api/v1/skills/capabilities is permanently route-shadowed by /skills/:id)

#### OBJ-07 — ValidatorConfig: documented afi-config schema diverges from the implemented mint interface
- **Class/Severity/Confidence:** C3 · medium · proven  |  **Repo:** afi-config  |  **Dimension:** objects-core
- **Contradiction/gap:** afi-config validatorConfig.schema.json requires decayCheckIntervalMs, challengeWindowDurationHours, mintApprovalThreshold, snapshotSpaceId; the runtime ValidatorConfig interface uses processingIntervalMs, challengeWindowDurationHours, minDecayScoreThreshold, ... with NO mintApprovalThreshold and NO decayCheckIntervalMs. The interface comment even claims it is 'sourced from afi-config'.
- **Evidence:** `afi-config/schemas/validatorConfig.schema.json:8-13`; `afi-mint/src/orchestrator/types.ts:164-217`
- **Consequence:** The documented validator config contract cannot validate or produce the object the daemon actually consumes; 'sourced from afi-config' is false on main.
- **Recommended authority:** afi-mint + afi-config
- **Minimal correction:** Reconcile the schema field set with the runtime interface (or record which is authoritative).
- **Flags:** pre-Chain  |  **Suggested slot:** LIFE-BRIDGE, LIFE-GOV  |  **Status:** open

#### ATLAS-04 — No canonical API Atlas; four maps disagree and no OpenAPI surface exists
- **Class/Severity/Confidence:** C4 · medium · proven  |  **Repo:** afi-docs  |  **Dimension:** api-atlas
- **Contradiction/gap:** System Atlas, Repository Map, Mintlify SiteMap, and Reference Impl Map overlap with divergent scopes and no self-declared canonical owner; none names the gateway /api/v1/* surface as a set. AFI_ANALYST_SHOP_MVP.md:163 promises a 'POST /api/v1/signals + OpenAPI snippet' but no OpenAPI/Swagger file exists in the workspace.
- **Evidence:** `afi-docs/AFI_System_Atlas.md:3`; `afi-docs/AFI_Repository_Map.md:1`; `afi-docs/AFI_Mintlify_SiteMap.md:1`; `afi-docs/specs/AFI_REFERENCE_IMPL_MAP.md:5`; `afi-docs/specs/AFI_ANALYST_SHOP_MVP.md:163`
- **Consequence:** There is no single source of truth for API routes/objects; each map can drift independently and already has.
- **Recommended authority:** afi-governance/afi-docs must designate one canonical API atlas and a versioning model
- **Minimal correction:** Designate AFI_REFERENCE_IMPL_MAP as canonical (or generate an OpenAPI from gateway/reactor routes) and mark the others as historical.
- **Flags:** Gov  |  **Suggested slot:** ATLAS-GOV  |  **Status:** open

#### CHAIN-04 — Epoch object identity split: per-signal attribute in runtime/persistence vs epoch-scoped batch in doctrine
- **Class/Severity/Confidence:** C4 · medium · proven  |  **Repo:** afi-token  |  **Dimension:** objects-econ
- **Contradiction/gap:** Runtime/persistence treat epoch as a per-signal field: MintRequest.epoch is uint64 per mint call (afi-token/src/AFIMintCoordinator.sol:25,85) and SignalIdentity.epochId is carried per VaultedSignalRecord (afi-infra/src/tssd/types.ts:22-26,331-351). Doctrine treats epoch as a top-level batch scope with exactly ONE EpochSettlementManifest per epochId spanning all strategies (AFI_EPOCH_SETTLEMENT_MANIFEST.md:23-27,33; …SCHEMA.md:98,104). No epoch-scoped object exists in runtime or persistence.
- **Evidence:** `afi-token/src/AFIMintCoordinator.sol:25`; `afi-infra/src/tssd/types.ts:22-26`; `afi-docs/specs/AFI_EPOCH_SETTLEMENT_MANIFEST.md:33`; `afi-docs/specs/AFI_SETTLEMENT_V1_MANIFEST_AND_PROVENANCE_SCHEMA.md:104`
- **Consequence:** There is no epoch-scoped aggregate in the persistence or runtime model for the doctrine's 'one committed manifest per epoch' to bind to; an epoch is only ever a tag on individual signals/mints. Building the manifest layer requires first introducing an epoch-scoped object that the current storage grouping does not provide.
- **Recommended authority:** afi-infra (persistence model) with afi-docs Layer-3 authority
- **Minimal correction:** Introduce (in persistence design) an epoch-scoped aggregation object distinct from the per-signal epochId tag before manifest/claimRoot work, or explicitly document that the epoch-scoped manifest is derived off-chain by rollup over per-signal epochId records.
- **Flags:** pre-Mongo, pre-Chain  |  **Suggested slot:** CHAIN-ATTACH, OBJ-GOV  |  **Status:** open
- **Relationships:** cluster CL-08 (Deprecated v0 per-signal push-at-mint shape (beneficiary/tokenAmount/receiptId/epoch) is implemented on-chain+runtime+persistence, contradicting the documented v1 epoch-batch settlement doctrine); depends-on CHAIN-01

#### CORP-02 — Contradiction Register C-MM-1 is stale — afi-mint now imports the afi-math schedule instead of inlining it
- **Class/Severity/Confidence:** C4 · medium · proven  |  **Repo:** afi-docs  |  **Dimension:** prior-audit-drafts
- **Contradiction/gap:** AFI_CONTRADICTION_REGISTER.md lists C-MM-1 as CONFIRMED P1: 'afi-mint inlines (copy-pastes) the schedule to avoid circular dependency, duplicating the 86B cap.' Current afi-mint imports the canonical schedule and builds it from afi-math — the register's own recommendation #5 has already been implemented, but the row is still marked CONFIRMED.
- **Evidence:** `afi-docs/specs/AFI_CONTRADICTION_REGISTER.md:130`; `afi-docs/specs/AFI_CONTRADICTION_REGISTER.md:201`; `afi-mint/src/adapters/EmissionsMintDataProvider.ts:14`; `afi-mint/src/adapters/EmissionsMintDataProvider.ts:101`
- **Consequence:** Anyone resuming mint/blockchain design off the register would re-fix an already-closed P1 and mistrust the whole 'verified' register; the '33/33 CONFIRMED' claim is no longer accurate on main.
- **Recommended authority:** afi-docs (M6 contradiction-register sync already scheduled by District 2 M0)
- **Minimal correction:** Mark contradiction-register row C-MM-1 RESOLVED and update its cite to afi-mint EmissionsMintDataProvider.ts:14 (afi-mint now imports the afi-math schedule).
- **Flags:** pre-Chain  |  **Suggested slot:** CORP-SYNC  |  **Status:** open
- **Relationships:** cluster CL-13 (Prior audit corpus is a known-stale snapshot post-District-2 (resolved rows still marked confirmed; file:line cites drifted))

#### F-PERSIST-07 — All reactor persistence tests are jest-IGNORED; two test services/types that do not exist in src
- **Class/Severity/Confidence:** C4 · medium · proven  |  **Repo:** afi-reactor  |  **Dimension:** persistence
- **Contradiction/gap:** jest.config.js testMatch excludes every persistence test and testPathIgnorePatterns explicitly ignores tssdVaultService, scoreDecayService, vaultReplayService, receiptProvenanceService, novelty, and pipelineRunnerDag; receiptProvenanceService.test.ts imports a nonexistent ../src/types/TssdSignalDocument and a receiptProvenance field with zero src references, and vaultReplayService.test.ts has no corresponding src service.
- **Evidence:** `afi-reactor/jest.config.js (testMatch + testPathIgnorePatterns)`; `afi-reactor/test/receiptProvenanceService.test.ts:12 (imports ../src/types/TssdSignalDocument.js — file absent)`; `afi-reactor/test/vaultReplayService.test.ts (local interfaces only; no src service)`; `afi-reactor/src/services/scoreDecayService.ts:1 (@ts-nocheck)`
- **Consequence:** The persistence layer has no executed test coverage and carries stale tests referencing removed/never-built code — must be reconciled before Mongo machinery resumes.
- **Recommended authority:** afi-reactor (implementation-review-only)
- **Minimal correction:** Restore or remove the jest-ignored reactor persistence tests and delete references to test services/types that do not exist (implementation-review-only hygiene).
- **Flags:** pre-Mongo  |  **Suggested slot:** MONGO-GOV  |  **Status:** open

#### GW-06 — TSSD read capability unexposed; gateway is write-only into the vault
- **Class/Severity/Confidence:** C4 · medium · proven  |  **Repo:** afi-gateway  |  **Dimension:** gateway-runtime
- **Contradiction/gap:** TenantScopedTSSDVaultClient exposes getBySignalId/query/listForTraining (afi-infra/src/tssd/TSSDVaultClient.ts:43-68), but the gateway exposes only POST /api/v1/signals (app.ts:123-141) with no GET/read route. Signals the gateway ingests cannot be read back through the gateway.
- **Evidence:** `afi-gateway/src/http/app.ts:123-141`; `afi-infra/src/tssd/TSSDVaultClient.ts:43-68`; `afi-infra/src/tssd/types.ts:331-367`
- **Consequence:** The gateway can only push into the canonical vault; tenants have no retrieval/verification path, compounding GW-02 (unscored records land in the vault with no gateway read-back or scoring feedback).
- **Recommended authority:** afi-gateway maintainer + afi-infra vault contract
- **Minimal correction:** Add a tenant-scoped read route (GET /api/v1/signals/:signalId) or formally document the gateway as write-only ingress.
- **Flags:** pre-Mongo  |  **Suggested slot:** MONGO-PERSIST  |  **Status:** open
- **Relationships:** depends-on GW-02

#### LIFE-09 — Production scoring+persistence path is @ts-nocheck (type safety disabled on the live lifecycle)
- **Class/Severity/Confidence:** C4 · medium · proven  |  **Repo:** afi-reactor  |  **Dimension:** lifecycle
- **Contradiction/gap:** froggyDemoService.ts — the only implemented ingest→enrich→score→persist path — is wrapped in @ts-nocheck at top and bottom, disabling TypeScript checking across the stage that builds ReactorScoredSignalDocument, reads plugin intermediates via untyped `as any`, and writes to Mongo. scoreDecayService.ts is likewise @ts-nocheck.
- **Evidence:** `afi-reactor/src/services/froggyDemoService.ts:1`; `afi-reactor/src/services/froggyDemoService.ts:335`; `afi-reactor/src/services/froggyDemoService.ts:231-250`; `afi-reactor/src/services/scoreDecayService.ts:1`
- **Consequence:** The persisted document shape is unverified against ReactorScoredSignalDocument; field drift (e.g., a missing epochId, a renamed pipeline field, or an untyped analystScore) would not be caught at build time on the exact path that produces the durable lifecycle record.
- **Recommended authority:** afi-reactor
- **Minimal correction:** Remove @ts-nocheck and type the plugin-intermediate boundary, so the persisted-document contract is enforced.
- **Flags:** pre-Mongo  |  **Suggested slot:** OBJ-CORE-INFRA, OBJ-REACTOR  |  **Status:** open

#### BG-10 — MongoDB TSSD persistence is evidence-plane data custody only and must not be conflated with settlement finality; its time-series store cannot enforce a unique signalId index
- **Class/Severity/Confidence:** C5 · medium · proven  |  **Repo:** afi-infra  |  **Dimension:** blockchain
- **Contradiction/gap:** Doctrine naming law separates the TSSD evidence (data) vault from token/reward custody; the only implemented 'finality' is Mongo persistence, which is not settlement, not chain proof, and cannot hold a unique index on identity.signalId (time-series limitation → non-unique fallback).
- **Evidence:** `afi-infra/src/tssd/MongoTSSDVaultClient.ts:120-161,231-238 (time-series VaultedSignalRecord upsert)`; `afi-infra/src/tssd/MongoTSSDVaultClient.ts:245-254 (unique index unsupported on time-series; falls back to non-unique)`; `afi-docs/specs/AFI_SETTLEMENT_V1_DOCTRINE.md:128,133 (TSSD = data custody, MUST NOT conflate with token vault)`
- **Consequence:** Treating Mongo persistence as a settlement/finality input is premature: it is plane (1) only, provides weak per-signal dedupe, and is not the canonical epoch roll-up needed to derive any on-chain root.
- **Recommended authority:** afi-infra maintainer
- **Minimal correction:** Record the plane separation (MongoDB = evidence custody, not settlement finality) in CHAIN-GOV; do not conflate.
- **Flags:** pre-Mongo  |  **Suggested slot:** CHAIN-GOV (Gate B/C)  |  **Status:** open

#### LIFE-06 — Reactor persistence failure is swallowed; caller gets 200 with unpersisted score
- **Class/Severity/Confidence:** C5 · medium · proven  |  **Repo:** afi-reactor  |  **Dimension:** lifecycle
- **Contradiction/gap:** TssdVaultService.insertSignalDocument catches all errors and returns the string 'failed' rather than throwing, and froggyDemoService awaits it but ignores the return value, then returns the scored result. The HTTP handler responds 200 regardless of whether the Mongo write succeeded (persistence-without-finality; silent data loss).
- **Evidence:** `afi-reactor/src/services/tssdVaultService.ts:104-122`; `afi-reactor/src/services/froggyDemoService.ts:330`; `afi-reactor/src/server.ts:229-237`
- **Consequence:** A signal can be reported as successfully scored to the caller while never being persisted, with no error surfaced. Any downstream consumer polling the store will silently miss it; there is no reconciliation.
- **Recommended authority:** afi-reactor
- **Minimal correction:** Check the VaultWriteStatus return and surface a non-2xx or explicit degraded status when the write fails.
- **Flags:** pre-Mongo  |  **Suggested slot:** MONGO-PERSIST, OBJ-GOV, OBJ-REACTOR  |  **Status:** open

#### LIFE-08 — Finality is defined only in unwired/documented surfaces; the live path has no finality marker
- **Class/Severity/Confidence:** C5 · medium · proven  |  **Repo:** afi-infra  |  **Dimension:** lifecycle
- **Contradiction/gap:** Finality semantics (validator decision, decay_pass, finalized, minted, rejected_final) exist only in the afi-infra ValidatorSnapshot and afi-mint SignalValidatorState — neither of which is written by any running process. The D2 ProvenanceRecord explicitly carries no validator-decision/finality fields. The deployed ReactorScoredSignalDocument has no finality field at all: 'SCORED' is stored with no notion of whether it is provisional or final.
- **Evidence:** `afi-infra/src/tssd/types.ts:291-318`; `afi-reactor/src/pipeheads/provenance/types.ts:168-170`; `afi-reactor/src/services/froggyDemoService.ts:281-328`; `afi-mint/src/orchestrator/types.ts:33-42`
- **Consequence:** No consumer can determine whether a persisted scored signal is final, provisional, qualified, or rejected. Finality-without-persistence (validator/minted stages) coexists with persistence-without-finality (reactor doc), so the lifecycle has no authoritative 'is this signal done?' answer.
- **Recommended authority:** afi-governance + afi-infra
- **Minimal correction:** Add an explicit lifecycle-stage/finality field to the persisted record and define which transition sets it.
- **Flags:** Gov, pre-Mongo, pre-Chain  |  **Suggested slot:** LIFE-GOV, OBJ-CORE-INFRA  |  **Status:** open
- **Relationships:** depends-on LIFE-01

#### GOV-04 — Supreme governing instrument (the Charter) lives outside the governance repo
- **Class/Severity/Confidence:** C6 · medium · proven  |  **Repo:** afi-governance  |  **Dimension:** governance-corpus
- **Contradiction/gap:** All four afi-governance decisions declare themselves subordinate to AFI_DROID_CHARTER.v0.1.md ('the Charter wins'), but the Charter is stored in afi-config/codex/governance/droids/, and Charter §8.3 makes afi-config canonical for droid governance. Governance ground truth is therefore split across two repos with no single index tying them.
- **Evidence:** `afi-governance/decisions/math-authority-v0.1.md:6`; `afi-config/codex/governance/droids/AFI_DROID_CHARTER.v0.1.md:262`; `afi-config/codex/governance/droids/AFI_DROID_CHARTER.v0.1.md:277`
- **Consequence:** A dimension that reads only afi-governance/decisions/ misses the top of the authority hierarchy; conflicts between afi-config droid-governance docs and afi-governance decisions have no declared tie-break location.
- **Recommended authority:** afi-config codex/governance (Charter is canonical) + afi-governance index
- **Minimal correction:** Add a cross-reference index (in afi-governance) naming the Charter's afi-config home as the apex authority, and vice-versa.
- **Flags:** none  |  **Suggested slot:** D-GOV  |  **Status:** open
- **Relationships:** cluster CL-03 (Supreme Charter lives outside the governance repo (two-headed governance root) — NOT missing)

#### BG-9 — Clawback/unclaimed/holdback correctly OPEN, but the implemented push-at-mint path destroys the custody seam those OPEN policies depend on
- **Class/Severity/Confidence:** C7 · medium · strongly-supported  |  **Repo:** afi-docs  |  **Dimension:** blockchain
- **Contradiction/gap:** ADR-006 D-006-8 requires preserving a vault custody seam so a future unclaimed/clawback policy is implementable at all; the implemented push-at-mint model leaves no seam, so the deferred policies have no architectural home in the built system.
- **Evidence:** `afi-docs/adrs/ADR-006-unclaimed-rewards-legal-clawback-open.md:38,71 (push-at-mint has no seam where 'unclaimed' can exist; keep custody seam)`; `afi-token/src/AFIMintCoordinator.sol:76 (tokens minted directly to beneficiary — no custody)`; `afi-docs/specs/AFI_SETTLEMENT_V1_DOCTRINE.md:113-114 (O1/O2 OPEN, pending legal/compliance)`
- **Consequence:** The deferral is sound, but until the epoch/vault seam is built the OPEN legal policies cannot attach anywhere; do NOT design these (out of scope), only note the missing precondition.
- **Recommended authority:** owner + legal/compliance (per ADR-006)
- **Minimal correction:** Preserve the custody seam ADR-006 depends on by deferring the push-at-mint path; keep the unclaimed/holdback options open.
- **Flags:** Gov, pre-Chain  |  **Suggested slot:** CHAIN-GOV (Gate B/C)  |  **Status:** open
- **Relationships:** depends-on G-8

#### GW-04 — DEFERRED: gateway ReactorScoredSignalV1.uwrAxes drift {utility,workQuality,rarity}
- **Class/Severity/Confidence:** C7 · medium · proven  |  **Repo:** afi-gateway  |  **Dimension:** gateway-runtime
- **Contradiction/gap:** afiClient.ts:61-66 types uwrAxes as {utility, workQuality, rarity}; canonical axes are {structure, execution, risk, insight} (afi-reactor/src/pipeheads/types.ts:112, builders.ts:493-496; afi-infra/src/tssd/types.ts:145-150; Atlas:13). Confirmed as the known deferred gateway uwrAxes issue; used only by the ElizaOS plugin/CLI lane, not the REST server.
- **Evidence:** `afi-gateway/src/afiClient.ts:61-66`; `afi-reactor/src/pipeheads/types.ts:112`; `afi-reactor/src/pipeheads/provenance/builders.ts:493-496`; `afi-infra/src/tssd/types.ts:145-150`
- **Consequence:** If the ElizaOS plugin ever deserialized reactor scores by these field names it would read undefined; currently latent because the plugin passes results through opaquely. Deferred per audit scope.
- **Recommended authority:** afi-gateway maintainer (deferred UWR cleanup track)
- **Minimal correction:** Deferred — no action in this audit; align the type to canonical axes when the deferred UWR cleanup is authorized.
- **Flags:** none  |  **Suggested slot:** GW-HYGIENE  |  **Status:** open

#### LIFE-07 — Off-chain orchestrator treats mint as terminal finality against a revert-today / stubbed contract
- **Class/Severity/Confidence:** C7 · medium · strongly-supported  |  **Repo:** afi-mint  |  **Dimension:** lifecycle
- **Contradiction/gap:** MintExecutor.executeMint calls contract.mintForSignal and treats a returned txHash as the terminal MINTED state, but the deployed v0 AFIMintCoordinator 'would revert today' (role-wiring incomplete, per CANONICAL ADR-001 and the on-chain gap audit) and afi-mint/contracts/MintManager.sol is a literal stub. The off-chain code assumes a callable, finalizing on-chain mint that does not currently exist.
- **Evidence:** `afi-mint/src/orchestrator/MintExecutor.ts:101-108`; `afi-mint/contracts/MintManager.sol:4-5`; `afi-docs/adrs/ADR-001-four-layer-settlement-architecture.md:1-30`; `afi-token/src/AFIMintCoordinator.sol:38-44`
- **Consequence:** Premature on-chain assumption in off-chain code: if the tail were wired, mint would revert; the 'finalized→minted' transition rests on a contract that is not operational and a doctrine (ADR-001) that mandates separating provenance from payout (which the v0 mintForSignal fuses).
- **Recommended authority:** afi-governance (ADR-001 settlement doctrine) + afi-token (contract wiring)
- **Minimal correction:** Keep mint stages labelled PROPOSED; do not resume chain-attachment design until ADR-001's four-layer separation is reflected in the coordinator and role-wiring is complete.
- **Flags:** Gov, pre-Chain  |  **Suggested slot:** LIFE-BRIDGE, LIFE-GOV  |  **Status:** open
- **Relationships:** depends-on LIFE-04

#### GOV-02 — 1B staking threshold: implemented + documented as auto-activating, but governance says 'unresolved'
- **Class/Severity/Confidence:** C8 · medium · proven  |  **Repo:** afi-governance  |  **Dimension:** governance-corpus
- **Contradiction/gap:** README.md asserts staking activates automatically after 1,000,000,000 AFI minted and code hard-codes MIN_SUPPLY_FOR_STAKING = 1_000_000_000, yet math-authority-v0.1.md Open Decision 5 records the 'status and authorization of the 1B staking threshold … if staking activates' as explicitly UNRESOLVED. No decision authorizes the threshold or the auto-activation.
- **Evidence:** `afi-governance/README.md:24-34`; `afi-governance/config/config_staking.ts:4`; `afi-governance/decisions/math-authority-v0.1.md:134`
- **Consequence:** A reader treats staking activation as governed and automatic; in fact it is an ungoverned constant contradicted by an open governance decision. Any staking/tokenomics dimension inherits an unauthorized activation trigger.
- **Recommended authority:** afi-governance/decisions (resolve math-authority OD-5)
- **Minimal correction:** Either govern the 1B threshold via a decision (resolving OD-5) or annotate README/config as ungoverned-provisional pending OD-5.
- **Flags:** Gov, pre-Chain  |  **Suggested slot:** CHAIN-GOV  |  **Status:** open


### 3.4 Low severity (25)

#### ATLAS-05 — Repository_Map lists afi-pipeline as a live core repo while the same doc says it no longer exists
- **Class/Severity/Confidence:** C1 · low · proven  |  **Repo:** afi-docs  |  **Dimension:** api-atlas
- **Contradiction/gap:** AFI_Repository_Map.md:24-33 documents afi-pipeline as a Core Repository owning the DAG execution engine, but line 167 states the legacy afi-pipeline hop no longer exists; the repo is absent from the workspace (ls afi-pipeline -> No such file).
- **Evidence:** `afi-docs/AFI_Repository_Map.md:24-33`; `afi-docs/AFI_Repository_Map.md:167`
- **Consequence:** Readers may attribute the DAG engine to a phantom repo instead of afi-reactor/afi-core.
- **Recommended authority:** afi-docs
- **Minimal correction:** Delete the afi-pipeline Core Repository entry (lines 24-33).
- **Flags:** none  |  **Suggested slot:** ATLAS-DOC  |  **Status:** open
- **Relationships:** cluster CL-11 (AFI_Repository_Map lists afi-pipeline as a live core repo while the same doc (and the workspace) says it no longer exists)

#### ATLAS-06 — System Atlas is stale: dead absolute path and omits the entire gateway /api/v1 surface
- **Class/Severity/Confidence:** C1 · low · proven  |  **Repo:** afi-docs  |  **Dimension:** api-atlas
- **Contradiction/gap:** AFI_System_Atlas.md:3 anchors to /Users/secretservice/AFI_Modular_Repos and describes the reactor as HTTP ingress while never mentioning the implemented gateway HTTP API (/healthz, /api/v1/api-keys, /api/v1/signals, /api/v1/skills at afi-gateway/src/http/app.ts:77-181).
- **Evidence:** `afi-docs/AFI_System_Atlas.md:3`; `afi-docs/AFI_System_Atlas.md:34-35`; `afi-gateway/src/http/app.ts:77`; `afi-gateway/src/http/app.ts:123`; `afi-gateway/src/http/app.ts:144`
- **Consequence:** The primary component atlas misrepresents where ingest/auth/skills APIs live.
- **Recommended authority:** afi-docs
- **Minimal correction:** Refresh the path and add a Gateway HTTP API section enumerating /api/v1/* routes.
- **Flags:** none  |  **Suggested slot:** ATLAS-DOC  |  **Status:** open
- **Relationships:** cluster CL-12 (System Atlas is stale re: the gateway — dead absolute macOS path, omits the entire /api/v1 surface, fabricates a Phoenix concierge persona)

#### ATLAS-08 — An implemented endpoint self-atlas (/api/afi/info) is not referenced by any documentation atlas
- **Class/Severity/Confidence:** C1 · low · strongly-supported  |  **Repo:** afi-gateway  |  **Dimension:** api-atlas
- **Contradiction/gap:** afi-gateway/src/server-full.ts:102-125 serves GET /api/afi/info embedding its own endpoint catalog (ElizaOS + afi routes), but no afi-docs atlas references this route or the ElizaOS API surface it lists.
- **Evidence:** `afi-gateway/src/server-full.ts:102`; `afi-gateway/src/server-full.ts:111-122`; `afi-docs/AFI_Mintlify_SiteMap.md:17-21`
- **Consequence:** The ElizaOS gateway API (/api/agents, /api/agents/:id/message, WebSocket) is implemented-but-undocumented in the atlas layer.
- **Recommended authority:** afi-docs / afi-gateway
- **Minimal correction:** Add the ElizaOS + /api/afi/info routes to the canonical atlas.
- **Flags:** none  |  **Suggested slot:** ATLAS-DOC  |  **Status:** open

#### CORP-09 — PURGE_RESULTS 'afi-core does not build' note is stale after UWR runtime work
- **Class/Severity/Confidence:** C1 · low · strongly-supported  |  **Repo:** afi-docs  |  **Dimension:** prior-audit-drafts
- **Contradiction/gap:** PURGE_RESULTS.md:92 records afi-core failing tsc with an incomplete dist/; on baseline 806db49 afi-core ships dist/ and validators/ValidatorDecision.ts, and the UWR runtime-consumption program has since landed — the build-broken note no longer reflects main.
- **Evidence:** `afi-docs/specs/audit/PURGE_RESULTS.md:92`; `afi-core/validators/ValidatorDecision.ts:1`
- **Consequence:** A reader treating the note as current would wrongly believe afi-core is unbuildable; minor but propagates through readiness claims.
- **Recommended authority:** afi-docs
- **Minimal correction:** Update the PURGE_RESULTS 'afi-core does not build' note; afi-core builds on main after the UWR runtime work.
- **Flags:** none  |  **Suggested slot:** CORP-SYNC  |  **Status:** open
- **Relationships:** cluster CL-13 (Prior audit corpus is a known-stale snapshot post-District-2 (resolved rows still marked confirmed; file:line cites drifted))

#### CORP-10 — Audit sibling-set version skew and recon record-count inconsistency (25 vs 31)
- **Class/Severity/Confidence:** C1 · low · proven  |  **Repo:** afi-docs  |  **Dimension:** prior-audit-drafts
- **Contradiction/gap:** Four of six 'final' reports were re-synthesized 2026-06-25 while AFI_ONCHAIN_ANCHOR_GAP_ANALYSIS.md and AFI_REPLAY_READINESS_MATRIX.md remain at 2026-06-15; AFI_REFERENCE_IMPL_MAP.md header cites '25 records' for the recon corpus while the master report and checkpoint cite '31 records'.
- **Evidence:** `afi-docs/specs/AFI_REFERENCE_IMPL_MAP.md:4`; `afi-docs/specs/AFI_PROTOCOL_SURFACE_AUDIT.md:3`; `afi-docs/specs/AFI_ONCHAIN_ANCHOR_GAP_ANALYSIS.md:1`
- **Consequence:** The six-report set is presented as a coherent cross-linked deliverable but is internally date- and count-inconsistent, weakening its 'complete synthesis' claim.
- **Recommended authority:** afi-docs
- **Minimal correction:** Reconcile the recon record count (25 vs 31) and sibling-set versions in the audit corpus.
- **Flags:** none  |  **Suggested slot:** CORP-SYNC  |  **Status:** open

#### DIST-04 — Triple 'D2' token collision across district / settlement-ADR / mint governance
- **Class/Severity/Confidence:** C1 · low · proven  |  **Repo:** afi-docs  |  **Dimension:** districts
- **Contradiction/gap:** 'D2' resolves to three unrelated things: (a) District 2 (afi-docs/reports/district-2-m0-...md:1); (b) ADR-001 decision D2 = 'Provenance ≠ payout (D2, MUST)' (afi-docs/adrs/ADR-001-four-layer-settlement-architecture.md:69); (c) mint-formula decision D2 = '86B hard cap' (afi-governance/decisions/mint-formula-bt-86b-alignment-v0.1.md:42). Additionally the M0 report uses its own D-1..D-17 owner-decision numbering and ADR-001 uses D1..D10, which overlap textually with the district numbers.
- **Evidence:** `afi-docs/reports/district-2-m0-canonical-data-boundary-and-hash-doctrine.md:1`; `afi-docs/adrs/ADR-001-four-layer-settlement-architecture.md:69`; `afi-governance/decisions/mint-formula-bt-86b-alignment-v0.1.md:42`; `afi-docs/reports/district-2-m0-canonical-data-boundary-and-hash-doctrine.md:523`
- **Consequence:** Cross-references to 'D2' are ambiguous without context, raising the risk that a settlement/chain decision ('provenance ≠ payout', '86B cap') is confused with the District 2 data-boundary unit — precisely at the seam where provenance meets settlement.
- **Recommended authority:** afi-docs / afi-governance (adopt a disambiguating prefix convention, e.g. DISTRICT-2 vs ADR001-D2 vs MINT-D2)
- **Minimal correction:** Namespace the decision IDs (prefix by document) so 'D2' is never bare in cross-references.
- **Flags:** none  |  **Suggested slot:** D-GOV  |  **Status:** open

#### GW-07 — Atlas claims reactor replay HTTP endpoint that does not exist
- **Class/Severity/Confidence:** C1 · low · proven  |  **Repo:** afi-docs  |  **Dimension:** gateway-runtime
- **Contradiction/gap:** Atlas:13 asserts reactor 'replay endpoints /replay/signal/:signalId', but afi-reactor/src/server.ts registers only /health, /debug/env, /api/webhooks/tradingview, /api/ingest/cpj — no /replay route. 'replay' appears only as a comment in novelty/canonicalNovelty.ts.
- **Evidence:** `afi-docs/AFI_System_Atlas.md:13`; `afi-reactor/src/server.ts:80-290`; `afi-reactor/src/novelty/canonicalNovelty.ts:6`
- **Consequence:** Atlas advertises a runtime route with no implementation; any gateway/consumer coded against /replay/signal/:signalId would 404.
- **Recommended authority:** afi-docs (Atlas) / afi-reactor
- **Minimal correction:** Remove or mark the replay-endpoint claim as PROPOSED in Atlas, or implement the route in reactor.
- **Flags:** none  |  **Suggested slot:** ATLAS-DOC  |  **Status:** open
- **Relationships:** cluster CL-09 (Documented reactor replay endpoint /replay/signal/:signalId does not exist)

#### OBJ-08 — AnalystScoreTemplate cites validators/UniversalWeightingRule.ts via a relative path that does not resolve from its own location
- **Class/Severity/Confidence:** C1 · low · proven  |  **Repo:** afi-core  |  **Dimension:** objects-core
- **Contradiction/gap:** afi-core/src/analyst/AnalystScoreTemplate.ts:16-17,102 name 'validators/UniversalWeightingRule.ts' / computeUwrScore() as the UWR math source; the file exists at afi-core/validators/UniversalWeightingRule.ts (repo root, OUTSIDE src/), so the relative citation mis-resolves from src/analyst/. [CORRECTED: the original recon claim that the file/symbol existed nowhere in the workspace is FALSE and is retained only in the corrections appendix.]
- **Evidence:** `afi-core/src/analyst/AnalystScoreTemplate.ts:16-17`; `afi-core/src/analyst/AnalystScoreTemplate.ts:100-105`
- **Consequence:** A reader following the doc-comment cannot locate the UWR math; reflects an afi-core validators/ vs src/ layout split.
- **Recommended authority:** afi-core, per afi-governance math-authority-v0.1
- **Minimal correction:** Repoint the comment to the actual UWR authority (afi-math / uwr-profile) or delete the stale reference.
- **Flags:** none  |  **Suggested slot:** LIFE-GOV, OBJ-CORE-INFRA  |  **Status:** open
- **⚠ Correction note:** ORIGINAL (false): 'no file named UniversalWeightingRule.ts and no computeUwrScore symbol exist anywhere on main.' CORRECTED: afi-core/validators/UniversalWeightingRule.ts exists on main (806db49); the real issue is the broken relative citation. Downgraded medium->low.

#### ATLAS-07 — Gateway skills capabilities endpoint is route-shadowed and unreachable
- **Class/Severity/Confidence:** C2 · low · proven  |  **Repo:** afi-gateway  |  **Dimension:** api-atlas
- **Contradiction/gap:** app.get('/api/v1/skills/:id') is registered at afi-gateway/src/http/app.ts:162 before app.get('/api/v1/skills/capabilities') at :173, so Express resolves GET /api/v1/skills/capabilities to the :id handler with id='capabilities' (returns 404 not_found from getSkillById), making the capabilities endpoint unreachable.
- **Evidence:** `afi-gateway/src/http/app.ts:162`; `afi-gateway/src/http/app.ts:173`; `afi-gateway/src/http/app.ts:164`
- **Consequence:** The advertised skills capabilities summary route can never be hit; any atlas listing it would be documenting a dead endpoint.
- **Recommended authority:** afi-gateway
- **Minimal correction:** Register /api/v1/skills/capabilities before /api/v1/skills/:id.
- **Flags:** none  |  **Suggested slot:** GW-HYGIENE  |  **Status:** open
- **Relationships:** cluster CL-10 (GET /api/v1/skills/capabilities is permanently route-shadowed by /skills/:id)

#### CHAIN-07 — 'Receipt' term collides across five unrelated objects
- **Class/Severity/Confidence:** C2 · low · proven  |  **Repo:** afi-token  |  **Dimension:** objects-econ
- **Contradiction/gap:** 'Receipt' names: (1) the deprecated ERC-1155 AFISignalReceipt payout artifact (afi-token/src/AFISignalReceipt.sol; AFIMintCoordinator.sol:80-82); (2) the persistence breadcrumb MintSnapshot.receiptAddress (afi-infra/src/tssd/types.ts:192); (3) the unbuilt canonical ERC-6909 reputation record (AFI_ERC6909…:23); (4) 'receipt-verified work' in governance (mint-formula-bt-86b:86); (5) by adjacency, the money-plane claim leaf. These are structurally different objects.
- **Evidence:** `afi-token/src/AFIMintCoordinator.sol:80-82`; `afi-infra/src/tssd/types.ts:192`; `afi-docs/specs/AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md:23`; `afi-governance/decisions/mint-formula-bt-86b-alignment-v0.1.md:86`
- **Consequence:** Cross-repo readers can conflate a deprecated payout receipt, a storage breadcrumb, a reputation record, and a governance work-verification concept, exactly the provenance/payout conflation v1 exists to prevent.
- **Recommended authority:** afi-docs naming law + afi-infra/afi-mint types
- **Minimal correction:** Adopt distinct nouns (e.g. v0-signal-receipt / reputation-receipt / mint-breadcrumb) in interfaces and docs; already partially done in doctrine but not in runtime types.
- **Flags:** none  |  **Suggested slot:** OBJ-GOV  |  **Status:** open

#### CORP-08 — AFI_Repository_Map lists a non-existent afi-pipeline repo it elsewhere declares removed
- **Class/Severity/Confidence:** C2 · low · proven  |  **Repo:** afi-docs  |  **Dimension:** prior-audit-drafts
- **Contradiction/gap:** AFI_Repository_Map.md carries a full '### afi-pipeline' repo section describing it as a live DAG-engine repo (line 24), while line 167 states the afi-pipeline hop 'no longer exists'; afi-pipeline is absent from the workspace.
- **Evidence:** `afi-docs/AFI_Repository_Map.md:24`; `afi-docs/AFI_Repository_Map.md:167`
- **Consequence:** The repo map self-contradicts on live topology and would mislead a reader building a current repository/persistence map.
- **Recommended authority:** afi-docs
- **Minimal correction:** Remove the afi-pipeline live-repo entry in AFI_Repository_Map; retain only the 'no longer exists' note.
- **Flags:** none  |  **Suggested slot:** ATLAS-DOC  |  **Status:** open
- **Relationships:** cluster CL-11 (AFI_Repository_Map lists afi-pipeline as a live core repo while the same doc (and the workspace) says it no longer exists)

#### F-PERSIST-08 — 'vault' naming collision: the vault-address-registry is on-chain settlement, not TSSD persistence; plus three 'tssd-vault' reactor artifacts (one persists)
- **Class/Severity/Confidence:** C2 · low · proven  |  **Repo:** afi-config  |  **Dimension:** persistence
- **Contradiction/gap:** afi-config/registries/afi-vault-address-registry.v1.json is an ENS/Safe settlement-address map (doctrineRefs to AFI_SETTLEMENT_V1_DOCTRINE.md), unrelated to signal persistence; and the reactor has three 'tssd-vault' artifacts of which only src/services/tssdVaultService.ts writes to Mongo.
- **Evidence:** `afi-config/registries/afi-vault-address-registry.v1.json:1-20 (settlement/ENS/Safe metadata)`; `afi-docs/specs/audit/AFI_MONGO_TSSD_INVENTORY.md:56-59 (three tssd-vault artifacts, one persists)`
- **Consequence:** The 'vault' homonym invites conflating on-chain settlement Safes with the TSSD signal store; any resumption doc must disambiguate to avoid mis-mapping where persistence vs settlement attaches.
- **Recommended authority:** afi-docs / afi-config (naming-law application)
- **Minimal correction:** Apply the doctrine naming law separating on-chain 'vault' (Rewards/Treasury) from data-plane 'TSSD/evidence vault' so the address-registry name does not collide with TSSD persistence.
- **Flags:** none  |  **Suggested slot:** MONGO-GOV  |  **Status:** open

#### LIFE-10 — On-chain epoch field type divergence (struct uint64 vs event uint256)
- **Class/Severity/Confidence:** C2 · low · proven  |  **Repo:** afi-token  |  **Dimension:** lifecycle
- **Contradiction/gap:** AFIMintCoordinator.MintRequest declares `uint64 epoch` while the MintCoordinated event declares `uint256 epochId` for the same concept, in the same contract.
- **Evidence:** `afi-token/src/AFIMintCoordinator.sol:24`; `afi-token/src/AFIMintCoordinator.sol:38-44`
- **Consequence:** Minor, but a silent widening at emit time and a naming mismatch (epoch vs epochId) that will confuse any indexer or ABI consumer building the epoch-inclusion → proof linkage; flag before chain-attachment design resumes.
- **Recommended authority:** afi-token
- **Minimal correction:** Unify the epoch field name and width across struct and event.
- **Flags:** pre-Chain  |  **Suggested slot:** CHAIN-ATTACH, OBJ-GOV  |  **Status:** open

#### OBJ-03 — "Pipeline result" names three distinct objects
- **Class/Severity/Confidence:** C2 · low · proven  |  **Repo:** afi-reactor  |  **Dimension:** objects-core
- **Contradiction/gap:** ReactorScoredSignalV1 is surfaced at the API as pipelineResult; DAGExecutionResult is the DAG's pipeline result; runPipelineDag returns a third pipelineResult carrying intermediatePayloads.
- **Evidence:** `afi-reactor/src/server.ts:396`; `afi-reactor/src/server.ts:410`; `afi-reactor/src/types/pipeline.ts:161-185`; `afi-reactor/src/services/froggyDemoService.ts:197-206`
- **Consequence:** Ambiguous API/response naming; 'pipelineResult' at the gateway/API is a scored signal, not the DAG execution result.
- **Recommended authority:** afi-reactor
- **Minimal correction:** Rename the API field to scoredSignal (or document the alias).
- **Flags:** none  |  **Suggested slot:** LIFE-GOV, OBJ-GOV  |  **Status:** open

#### DIST-H-09 — Package-name scoping is inconsistent across the org, with no naming authority
- **Class/Severity/Confidence:** C3 · low · proven  |  **Repo:** afi-math  |  **Dimension:** repo-authority
- **Contradiction/gap:** Four packages are scoped @afi-protocol/* (afi-math, afi-mint, afi-gateway, afi-econ), while core/config/reactor/infra/plugins/token/governance/protocol are unscoped bare names; gateway consumes yet another scope (@afi/cli-framework), and afi-xerc20's package name is bare 'xerc20'. No governed naming convention exists.
- **Evidence:** `afi-math/package.json`; `afi-core/package.json`; `afi-gateway/package.json`; `afi-xerc20/package.json`; `afi-config/package.json`
- **Consequence:** Scoped imports and peerDep constraints break unpredictably (root cause of DIST-H-06); atlas/discovery cannot key on a consistent org namespace.
- **Recommended authority:** afi-governance
- **Minimal correction:** Adopt a single governed naming convention (e.g. @afi-protocol/*) and align all package.json name fields + cross-repo dep references.
- **Flags:** Gov  |  **Suggested slot:** D-GOV  |  **Status:** open
- **Relationships:** cluster CL-15 (Package naming/scoping has no authority (some @afi-protocol/*, some bare, some @afi/*); afi-mint peerDependencies name packages that do not exist)

#### DIST-H-10 — afi-governance carries executable stubs and duplicate proposal schemas alongside the law ledger
- **Class/Severity/Confidence:** C3 · low · strongly-supported  |  **Repo:** afi-governance  |  **Dimension:** repo-authority
- **Contradiction/gap:** afi-governance owns the decision ledger but also ships behavior: validator/proposal_scorer.ts (returns Math.random() per math-authority §5), agents/proposal_executor_agent.ts, cli/submit-proposal.ts, config/config_staking.ts. It also carries TWO proposal-schema definitions: schemas/UniversalProposalSignal.schema.json and specs/universal_proposal_schema.json. math-authority §3/§5 warns this stub logic must never be treated as deterministic authority.
- **Evidence:** `afi-governance/validator/proposal_scorer.ts`; `afi-governance/schemas/UniversalProposalSignal.schema.json`; `afi-governance/specs/universal_proposal_schema.json`; `afi-governance/decisions/math-authority-v0.1.md:113-115`
- **Consequence:** The law-owning repo mixes non-authoritative executable stubs with governance records and holds two proposal schemas, risking a consumer wiring the stub scorer or the wrong schema copy as authority.
- **Recommended authority:** afi-governance
- **Minimal correction:** Mark governance executable stubs non-authoritative (or move to a sandbox path) and collapse the duplicate proposal schema to one canonical file.
- **Flags:** none  |  **Suggested slot:** D-GOV  |  **Status:** open
- **Relationships:** cluster CL-14 (afi-governance ships executable stubs alongside the law ledger — proposal scorer is Math.random() on main)

#### GW-05 — Dead npm entrypoints reference nonexistent src/community/ servers
- **Class/Severity/Confidence:** C3 · low · proven  |  **Repo:** afi-gateway  |  **Dimension:** gateway-runtime
- **Contradiction/gap:** package.json dev:discord→src/community/discord-server.ts and dev:telegram→src/community/telegram-server.ts, but src/community/ does not exist.
- **Evidence:** `afi-gateway/package.json:12-13`
- **Consequence:** Documented community entrypoints are broken; running them fails immediately. Signals planned-but-absent Discord/Telegram surfaces.
- **Recommended authority:** afi-gateway maintainer
- **Minimal correction:** Remove the dead scripts or add the community server files.
- **Flags:** none  |  **Suggested slot:** GW-HYGIENE  |  **Status:** open

#### DIST-H-01 — Supreme Charter lives outside the governance repo (in afi-config), not in afi-governance — NOT missing
- **Class/Severity/Confidence:** C4 · low · proven  |  **Repo:** afi-governance  |  **Dimension:** repo-authority
- **Contradiction/gap:** All four afi-governance decisions declare subordination to AFI_DROID_CHARTER.v0.1.md; the charter exists at afi-config/codex/governance/droids/AFI_DROID_CHARTER.v0.1.md (verified by direct read), i.e. the supreme cited authority lives in the config repo, not afi-governance, and is a droid-behavior charter that never mentions Districts. [CORRECTED: the original recon claim that the charter was absent from all checkouts is FALSE and is retained only in the corrections appendix.]
- **Evidence:** `afi-governance/decisions/math-authority-v0.1.md:6`; `afi-governance/decisions/mint-formula-bt-86b-alignment-v0.1.md:5`; `afi-governance/decisions/uwr-profile-pin-v0.1.md:5`; `afi-governance/decisions/uwr-runtime-consumption-v0.1.md:5`; `afi-docs/AFI_CLI_GOVERNANCE_COMMITTEE_CHARTER.md`
- **Consequence:** Two-headed governance root: authority resolution must know the charter is in afi-config and scoped to droid behavior, not protocol architecture.
- **Recommended authority:** afi-governance (record the charter's canonical home + scope in D-GOV)
- **Minimal correction:** In the authority-topology decision, record that AFI_DROID_CHARTER.v0.1.md lives in afi-config and governs droid behavior, and place protocol-development authority in afi-governance.
- **Flags:** Gov, pre-Chain  |  **Suggested slot:** D-GOV  |  **Status:** open
- **Relationships:** duplicate-of GOV-04; cluster CL-03 (Supreme Charter lives outside the governance repo (two-headed governance root) — NOT missing)
- **⚠ Correction note:** ORIGINAL (false): 'Supreme authority AFI_DROID_CHARTER.v0.1.md ... exists in no checkout.' CORRECTED: it exists at afi-config/codex/governance/droids/AFI_DROID_CHARTER.v0.1.md; the real residual is that it lives outside afi-governance (captured by GOV-04). Downgraded blocker->low.

#### GW-09 — API-key bootstrap requires an existing API key (chicken-and-egg); unsalted hash default
- **Class/Severity/Confidence:** C4 · low · strongly-supported  |  **Repo:** afi-gateway  |  **Dimension:** gateway-runtime
- **Contradiction/gap:** POST /api/v1/api-keys (app.ts:82) is behind the same auth middleware, so creating the first tenant key requires a pre-existing key; no unauthenticated seed/admin route exists in-repo. Separately, API_KEY_SALT defaults to '' (apiKeyStore.ts:53), so keys are hashed unsalted if unset.
- **Evidence:** `afi-gateway/src/http/app.ts:82-94`; `afi-gateway/src/services/apiKeyStore.ts:52-54`
- **Consequence:** First-key provisioning must happen out-of-band (direct DB insert); default deployments risk unsalted key hashes if the operator does not set API_KEY_SALT.
- **Recommended authority:** afi-gateway maintainer
- **Minimal correction:** Document/provide an admin bootstrap path and require a non-empty API_KEY_SALT at startup.
- **Flags:** none  |  **Suggested slot:** GW-HYGIENE  |  **Status:** open

#### OBJ-09 — AnalystScoreTemplate carries no signalId and no self version, so a 'per-signal' score is not self-identifying
- **Class/Severity/Confidence:** C4 · low · proven  |  **Repo:** afi-core  |  **Dimension:** objects-core
- **Contradiction/gap:** AnalystScoreTemplate is described as per-signal but has no signalId field and no version field of its own; the signal binding exists only in its wrappers (ReactorScoredSignalV1.signalId, AnalystScoreInput.signalId).
- **Evidence:** `afi-core/src/analyst/AnalystScoreTemplate.ts:31-123`; `afi-reactor/src/types/ReactorScoredSignalV1.ts:76`; `afi-mint/src/orchestrator/ValidatorDaemon.ts:24-29`
- **Consequence:** A detached analyst score cannot be traced to its signal or template version without its wrapper; complicates independent persistence/replay.
- **Recommended authority:** afi-core
- **Minimal correction:** Record whether analyst score is ever persisted/transported independently and, if so, add signalId + template version.
- **Flags:** pre-Mongo  |  **Suggested slot:** OBJ-CORE-INFRA, OBJ-REACTOR  |  **Status:** open

#### CHAIN-06 — Reactor 'Receipt Provenance Service' test imports a non-existent type; receipt-provenance in reactor is aspirational/test-only
- **Class/Severity/Confidence:** C7 · low · strongly-supported  |  **Repo:** afi-reactor  |  **Dimension:** objects-econ
- **Contradiction/gap:** afi-reactor/test/receiptProvenanceService.test.ts:11 imports type TssdSignalDocument from ../src/types/TssdSignalDocument.js, but that file does not exist in afi-reactor/src/types (only ReactorScoredSignalV1.ts is present). There is no receiptProvenanceService implementation in src (grep found none outside tests).
- **Evidence:** `afi-reactor/test/receiptProvenanceService.test.ts:11`; `afi-reactor/src/types/ReactorScoredSignalV1.ts`
- **Consequence:** A 'receipt provenance' object appears named in reactor tests with a dangling type import and no runtime implementation, so it cannot be treated as an implemented object; low-priority cleanup or missing-file signal.
- **Recommended authority:** afi-reactor maintainers
- **Minimal correction:** Restore/author the TssdSignalDocument type or remove the dangling test; classify receipt-provenance in reactor as not-yet-implemented.
- **Flags:** none  |  **Suggested slot:** CHAIN-GOV  |  **Status:** open

#### DIST-H-11 — Deferred UWR-program items — recorded attach points only (program COMPLETE, do not fix)
- **Class/Severity/Confidence:** C7 · low · proven  |  **Repo:** afi-core  |  **Dimension:** repo-authority
- **Contradiction/gap:** Deferred items from the completed UWR runtime-consumption program attach to specific ownership seams: gateway uwrAxes cleanup → afi-gateway; UP-8 decay-engine canonicality → afi-math decay/decayModels vs afi-core GreeksDecayTemplate; uwr-default-stub retirement / CONFIG-PACKAGING / flag-default flip → afi-core validators/UniversalWeightingRule.ts, afi-config packaging, afi-reactor src/config/uwrRuntimeProfile.ts. Also core's root package entry dangles (no root src/index.ts).
- **Evidence:** `afi-core/validators/UniversalWeightingRule.ts`; `afi-reactor/src/config/uwrRuntimeProfile.ts`; `afi-governance/decisions/uwr-runtime-consumption-v0.1.md:1`; `afi-core/package.json`
- **Consequence:** No action in this dimension; recorded so the deferred items map to owners without reopening the stopped UWR program.
- **Recommended authority:** afi-governance
- **Minimal correction:** None — classify C7/deferred; owners noted for when those separately-authorized programs resume.
- **Flags:** none  |  **Suggested slot:** D-GOV  |  **Status:** open

#### GOV-06 — Governance proposal scorer is still a Math.random() stub on main
- **Class/Severity/Confidence:** C7 · low · proven  |  **Repo:** afi-governance  |  **Dimension:** governance-corpus
- **Contradiction/gap:** validator/proposal_scorer.ts returns Math.random(); math-authority §5 records this as a finding and §8 proposes PR-10 hygiene, but that PR is unauthorized and the stub remains on main. math-authority §3 states placeholder scoring 'must never be treated as deterministic protocol authority.'
- **Evidence:** `afi-governance/validator/proposal_scorer.ts:2-4`; `afi-governance/decisions/math-authority-v0.1.md:124`; `afi-governance/decisions/math-authority-v0.1.md:177`
- **Consequence:** Non-deterministic stub sits in the governance validator surface; harmless while unwired, but a latent hazard if any flow starts calling it as authority.
- **Recommended authority:** afi-governance (PR-10, when scoped)
- **Minimal correction:** Deferred PR-10 scorer/stub hygiene (already proposed, unauthorized) — classify C7/deferred; do not wire.
- **Flags:** none  |  **Suggested slot:** D-GOV/CHAIN-GOV  |  **Status:** open
- **Relationships:** cluster CL-14 (afi-governance ships executable stubs alongside the law ledger — proposal scorer is Math.random() on main)

#### GOV-07 — No District is authorized by any afi-governance decision; District authority sits in afi-docs with a 3-way D-n identifier collision
- **Class/Severity/Confidence:** C7 · low · proven  |  **Repo:** afi-governance  |  **Dimension:** governance-corpus
- **Contradiction/gap:** Districts are referenced everywhere (D2 M2 goldens, D-17 pattern) but no afi-governance decision authorizes a District; math-authority §9 is a 'cross-district guardrail' that 'does not by itself start or define a new district', and §7 lists 'starting any new district implementation' as non-authorized. District decisions D-1…D-17 live in afi-docs, colliding with Settlement v1 D1–D10 and mint-formula D1–D8.
- **Evidence:** `afi-governance/decisions/math-authority-v0.1.md:155`; `afi-governance/decisions/math-authority-v0.1.md:179-181`; `afi-governance/decisions/uwr-profile-pin-v0.1.md:66`
- **Consequence:** The Districts dimension must source District authority from afi-docs, not afi-governance, and must disambiguate three distinct D-n numbering schemes before citing any 'Dn' decision.
- **Recommended authority:** afi-docs (District doctrine) — out of afi-governance scope
- **Minimal correction:** Record in the register that District governance authority resides in afi-docs; carry the identifier-namespace map (District D-n vs Settlement D-n vs mint D-n) as a standing disambiguation.
- **Flags:** none  |  **Suggested slot:** D-GOV  |  **Status:** open
- **Relationships:** cluster CL-04 (Numbered District 1/2 scheme has no governance basis; districts are authorized only in afi-docs)

#### GOV-08 — Runtime-consumption ledger frontier: 3 rows authorized, behavior-changing rows still 'No'
- **Class/Severity/Confidence:** C7 · low · proven  |  **Repo:** afi-governance  |  **Dimension:** governance-corpus
- **Contradiction/gap:** uwr-runtime-consumption §7 ledger (file + git log verified) has PR-UWR-RUNTIME-LOADER / RUNTIME-READ / STAMP-SEMANTICS flipped to 'Yes', while PR-UWR-KAT-RERUN, PR-UWR-CONFIG-PACKAGING, the flag-default flip (builtin→registry), and stub retirement remain 'No'. The scored value therefore still comes from defaultUwrConfig by default; UP-8 decay canonicality remains OPEN despite PR-7 having landed.
- **Evidence:** `afi-governance/decisions/uwr-runtime-consumption-v0.1.md:228-234`; `afi-governance/decisions/uwr-runtime-consumption-v0.1.md:17`; `afi-governance/decisions/uwr-profile-pin-v0.1.md:51`
- **Consequence:** The UWR runtime-consumption program is the authorization frontier: source default is still 'builtin', qualification gate unwired (UP-9), and these are the deferred attach points other dimensions may reference — classify C7, do not extend.
- **Recommended authority:** afi-governance (owner row-flips, RC-12)
- **Minimal correction:** None — deferred by design; record the ledger state as the yardstick for 'what is authorized right now'.
- **Flags:** pre-Mongo  |  **Suggested slot:** D-GOV/CHAIN-GOV  |  **Status:** open

---

## 4. Contract & identifier crosswalk

| Concept | Canonical candidate | Alternate names / representations | Owning-repo candidate → **recommended owner** | Required action |
|---|---|---|---|---|
| **Signal** | USS v1.1 payload (schema-first, `afi-config/schemas/usignal/v1_1`) | `UssV11Payload` (`@ts-nocheck`), CPJ v0.1, `AfiScoutSignalDraft` (self-non-canonical) | afi-config (schema) / afi-reactor → **afi-config** | Name the first-class Signal contract in OBJ-GOV |
| **Strategy id** | *none canonical* | `facts.strategy` (`froggy_trend_pullback_v1`) vs `strategyId` (`trend_pullback_v1`) vs `meta.strategy` vs `strategy.name` vs D2 `strategyId` | afi-core → **afi-config/afi-core** | One field name + one format; forbid two ids in one doc (LIFE-01) |
| **Analyst score** | `AnalystScoreTemplate` (afi-core) | `AnalystScoreInput` projection (afi-mint) | **afi-core** | Add `signalId` + self-version (OBJ-09) |
| **Scored signal** | *contested* — `ReactorScoredSignalDocument` (persisted) vs D2 `ScoredSignalV1` (canonical, unpersisted) | `ReactorScoredSignalV1` (response), `InternalScoringResult` | afi-reactor + afi-config → **decide in OBJ-GOV** | Persist the canonical D2 shape or bless the runtime doc (OBJ-02/LIFE-03) |
| **Validation** | overloaded | 5 `*ValidationResult` (schema conformance) vs `ValidatorDecisionKind` (certification) | reactor (schema) / afi-mint (certification) | Split the vocabulary (OBJ-04) |
| **Qualification** | afi-mint `SignalValidatorState` | unwired | **afi-mint** | Wire only after LIFE-GOV; no impl now |
| **Epoch** | *three identities* | emissions unit `E_t=B(t)·AIM_t` (governed) vs per-signal `epochId`/`uint64` (impl) vs epoch-batch manifest (doc) | afi-math + afi-docs → **afi-governance** | Decide the epoch-scoped settlement object (CHAIN-04) |
| **Receipt** | *five meanings* | ERC-6909 reputation (doc) vs ERC-1155 v0 (impl, deprecated) vs `MintSnapshot` breadcrumb vs "receipt-verified work" vs claim leaf | afi-token / afi-docs → **afi-governance** | Ratify ERC-6909 vs deprecate v0 (BG-2) |
| **Reputation record** | ERC-6909 receipt / strategy leaf (doc/proposed) | placeholder `reputation_bridge.ts`, econ simulation, TSSD `poiLevel` fields | afi-docs/afi-mint → **afi-governance** | Intent only; do not build (CHAIN-05) |
| **Reward / Claim / Settlement** | manifest `claimRoot` + RewardsVault (doc) | `mintForSignal` push (impl, forbidden) | afi-docs/afi-token → **afi-governance** | Ratify or demote doctrine (CHAIN-01) |
| **District** | pipehead addendum functional names (afi-config) | numbered "District 1/2" (afi-docs) | afi-config addendum + afi-docs → **afi-governance registry** | Reconcile numbering ↔ function (DIST-02) |
| **API resource** | *none* | epoch/receipt/reward/claim have no API surface | — | Out of scope now |

---

## 5. Lifecycle transition table

| Transition | Input → Output | Owner (repo) | Impl | Doc | Gov | Persisted | Replayable | Chain-relevant | Clear? |
|---|---|---|---|---|---|---|---|---|---|
| Ingestion | HTTP → `TradingViewAlertPayload`/CPJ | reactor `server.ts` | ✅ | ✅ | – | – | – | – | clear |
| Normalization | raw → USS v1.1 | reactor `tradingViewMapper`/`mapCpj` | ✅ | ✅ | – | – | – | – | clear |
| Validation (schema) | USS → `{ok,errors}` | reactor `ussValidator` | ✅ | ✅ | – | – | – | – | clear |
| Enrichment + Scoring | USS → `analystScore`/`uwrScore` | reactor DAG + afi-core | ✅ | ✅ | UWR pinned | – | – | – | clear (but `@ts-nocheck`) |
| Persistence (scored) | doc → `reactor_scored_signals_v1` | reactor `tssdVaultService` | ✅ | ⚠ | ❌ | ✅ append | reactor-only | – | **ambiguous** (2 stores, swallowed failure) |
| Canonical artifact | USS → `ScoredSignal v1`/`ProvenanceRecord v1` | reactor D2 harness | ✅ (CLI/test) | ✅ | D2 M1 | ❌ never | pins exist | seam | **ambiguous** (computed, thrown away) |
| Gateway ingest | HTTP → `VaultedSignalRecord` | gateway `app.ts` → afi-infra | ✅ | ⚠ | ❌ | ✅ `tssd_signals` | stub | – | **contested** (writes canonical vault, unscored) |
| Validation (certify) → Qualification | score → `qualified/rejected` | afi-mint orchestrator | library-only | ✅ | ❌ | in-memory | – | – | **unwired** (no fetcher, no daemon) |
| Challenge → Finalization | state machine | afi-mint `ValidatorDaemon` | library-only | ✅ | ❌ | in-memory | – | – | **unwired / zero-owner** |
| Epoch inclusion | qualified set → epoch batch | *none* | ❌ | ✅ | partial | ❌ | – | ✅ | **zero implemented owner** |
| Proof / receipt | leaf → root/receipt | *none* (doc: manifest/ERC-6909) | ❌ (v0 ERC-1155 only) | ✅ | ❌ | ❌ | – | ✅ | **unbuilt / v0 conflict** |
| Reward eligibility | inclusion → entitlement | afi-token `mintForSignal` (v0) | ✅ (forbidden shape) | ✅ (claimRoot) | skeleton | breadcrumb | – | ✅ | **conflicting** |
| Claim / Settlement | proof → payout | *none* (RewardsVault) | ❌ | ✅ | ❌ | ❌ | – | ✅ | **unbuilt** |

---

## 6. Minimal implementation program (recommendation only — not authorized here)

A **governance-first spine of six owner-gated decisions**, each merged before any code slot depends on it, honoring the Charter's propose-don't-decide rule and the math-authority/mint-formula non-authorizations. Prefer these small gated PRs over any cross-repo mega-PR. Code/doc alignment slots follow each decision; every code slot is gated behind its governance prerequisite.

| Slot | Repo | Scope (summary) | Depends on | Clears (examples) |
|---|---|---|---|---|
| **D-GOV** | afi-governance | Authority-topology & District registry: record the Charter's real home (afi-config, droid-behavior scope); ratify a canonical District registry reconciling functional names with the docs' numbers; rule on the shipped-but-unauthorized D2 "M2"; restore-or-retire the missing Constitution refs | — (root) | DIST-H-01, GOV-04, DIST-02/04, GOV-07, DIST-01, GOV-03 |
| **DIST-DOC** | afi-docs | Align district reports to the D-GOV registry; reconcile the M2 milestone-scope divergence | D-GOV | DIST-03, CORP-06 |
| **ATLAS-GOV** | afi-governance | Designate ONE canonical API Atlas + versioning; declare the four overlapping maps derived; name gateway `/api/v1/*` as the external API set | D-GOV | ATLAS-04 |
| **ATLAS-DOC** | afi-docs | Rewrite the canonical Atlas to implemented reality (remove phantom replay endpoint, Phoenix persona, afi-pipeline) | ATLAS-GOV | GW-01, ATLAS-01/05/06/08, GW-07, ATLAS-02/03 |
| **CORP-SYNC** | afi-docs | Execute the scheduled M6 contradiction-register sync (mark resolved rows, re-anchor cites) | ATLAS-GOV | CORP-02/03/04/05/09/10 |
| **OBJ-GOV** | afi-governance | Canonical object identity & identifier continuity (signalId join key; one strategy id; one scored-signal shape; epoch/receipt identity) | ATLAS-GOV | LIFE-01, OBJ-02, DIST-H-08, OBJ-04, LIFE-03, OBJ-06, CHAIN-07, DIST-H-02, CHAIN-04, LIFE-10 |
| **OBJ-REACTOR** | afi-reactor | Align reactor types to OBJ-GOV (unify strategy id; adopt canonical scored-signal shape; rename `TssdVaultService`; remove `@ts-nocheck`) | OBJ-GOV | LIFE-01, OBJ-06, OBJ-09 |
| **OBJ-CORE-INFRA** | afi-core | Add `signalId`+self-version to `AnalystScoreTemplate`; fix the `validators/UniversalWeightingRule.ts` broken relative citation | OBJ-GOV | OBJ-09, OBJ-08, DIST-H-08, DIST-H-05 |
| **LIFE-GOV** | afi-governance | Canonical lifecycle state machine + per-transition owner + finality writer + `IAnalystScoreFetcher` handoff owner | OBJ-GOV | LIFE-01/03/04/05/07 |
| **LIFE-BRIDGE** | afi-mint | Converge status enums; declare the handoff interface (no wiring) | LIFE-GOV | LIFE-07 |
| **MONGO-GOV** | afi-governance | Canonical TSSD vault owner + shape; rule on the reactor "isolated" store; resolve gateway/reactor two-writer; decide finality/immutability | OBJ-GOV + LIFE-GOV | DIST-H-04, LIFE-02, GW-02, CORP-07 |
| **MONGO-PERSIST** | afi-infra | Implement MONGO-GOV **behind Gate A** | MONGO-GOV | GW-06, OBJ-06 |
| **CHAIN-GOV** | afi-governance | Ratify-or-scope Settlement v1; resolve the four-vs-three role-set contradiction; decide epoch settlement object; govern numeric role weights; resolve staking | OBJ/LIFE/MONGO-GOV | GOV-05, CHAIN-01/02, GOV-01/02 |
| **CHAIN-ATTACH** | afi-docs | Document chain-attachment design readiness **behind Gate B** | CHAIN-GOV | CHAIN-04/05, LIFE-10 |
| **GW-HYGIENE** | afi-gateway | Off-critical-path cleanup: route-shadow, dead entrypoints, unsalted salt, dep-metadata (`GW-03/05/08/09`, `DIST-H-06/07`) | — | GW-03, ATLAS-07, GW-08, GW-05, GW-09, DIST-H-06/07 |

---

## 7. MongoDB and blockchain machinery-resumption gates

**Gate A — MongoDB machinery may resume when** all three are merged: (1) **OBJ-GOV** designates the single canonical scored-signal shape and `signalId` as the join key; (2) **LIFE-GOV** designates the one lifecycle state machine + finality writer; (3) **MONGO-GOV** names the single canonical vault owner and the write-ownership boundary. *Rationale:* persisting before object+lifecycle are canonical would harden the two-store split. *Clears:* DIST-H-04, LIFE-02, GW-02/06, CORP-07, F-PERSIST-01..06.

**Gate B — Blockchain architecture/design may resume when:** (1) **CHAIN-GOV** ratifies-or-scopes the settlement doctrine (ends the authority inversion), resolves the role-set contradiction, and decides the epoch settlement-object identity; and (2) OBJ-GOV epoch/receipt identity + LIFE-GOV finality are in place. **Does not require numeric role-weight values or contract authorization** — design may proceed on ratified authority + canonical identity alone. *Clears:* GOV-05, CHAIN-01/02/04/05.

**Gate C — Blockchain implementation may resume when** Gate B is satisfied **and**: (1) numeric baseline role weights are governed (GOV-01/BG-6); (2) the 1B staking threshold is resolved (GOV-02); (3) an explicit owner decision authorizes contract deployment and the v0→v1 `mintForSignal` retirement (Charter §5.2 economic-behavior gate); (4) math→token constant traceability (math-authority OD-4) and the would-revert-today role-wiring gap (BG-7) are addressed. *Entirely outside this read-only audit's scope.*

---

## 8. Deferred register (real, but outside the District/API critical path)

- **UWR program (COMPLETE/stopped):** KAT-RERUN, CONFIG-PACKAGING, registry-default flag flip, `uwr-default-stub` retirement (GOV-08); UP-8 decay canonicality; the 0650 KAT erratum; **gateway `uwrAxes` drift** `{utility,workQuality,rarity}` vs `{structure,execution,risk,insight}` (GW-04). *Off-path: attaches to the already-shipped runtime-consumption program, not to District/API identity.*
- **Mint / reward / payout / vault / settlement / production scoring law:** the entire tail (CHAIN-*, BG-*, LIFE-07). *Off-path: gated behind Gates B/C; this audit maps where they attach, does not design them.*
- **Economic OPENs** correctly deferred by doctrine: clawback/escheatment (ADR-006), push-vs-pull default, holdback schedule, EAS schema, Safe topology, tokenomics split values, role-weight numbers.
- **Security/dependency hygiene encountered** (record, don't fix here): gateway unsalted `API_KEY_SALT` default and api-key bootstrap chicken-and-egg (GW-09); afi-mint peerDeps naming non-existent packages (DIST-H-06); afi-governance `proposal_scorer.ts` still `Math.random()` on main (GOV-06); Dependabot criticals previously surfaced on afi-ops/afi-config.

---

_End of report. See `AFI_DISTRICTS_API_ATLAS_METHODOLOGY.md` for methodology, reliability, access limits, and the corrections appendix (the two corrected agent errors). Machine-readable registers: `AFI_DISTRICTS_API_ATLAS_FINDINGS.json`, `AFI_DISTRICTS_API_ATLAS_FINDINGS.csv`._
