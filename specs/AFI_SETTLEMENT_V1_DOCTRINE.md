# AFI Settlement v1 Doctrine

**Status:** CANONICAL — Accepted (v1 doctrine baseline)
**Date:** 2026-06-24
**Owner decisions:** Locked by protocol owner (see ADR-001 … ADR-006)
**Supersedes (as mainnet architecture):** the v0 per-signal `mintForSignal` flow and any doc that presents it as canonical.
**Scope of this document:** doctrine and normative law only. **No contracts are implemented by this document.** It does not deploy, mint, grant roles, move funds, or modify ENS/Safe state. It tells contributors, auditors, and agents what AFI Settlement v1 *is*, so the repository stops teaching the wrong architecture.

> This is the AFI Settlement v1 **constitution**. Where any other document, comment, README, schema, or contract conflicts with this file on a **v1 architecture** question, **this file wins** and the other artifact is to be treated as stale, prototype, or runtime-deferred (see `AFI_V0_DEPRECATION_AND_MIGRATION.md`). Existing audit/recon reports that *describe* v0 as-it-is remain accurate and are not in conflict.

---

## 1. Normative Language

The key words below are used with these meanings throughout the v1 doctrine set:

- **MUST / MUST NOT** — an absolute requirement or prohibition. Conformance is mandatory.
- **SHOULD / SHOULD NOT** — a strong recommendation; deviation requires a documented, owner-approved reason.
- **MAY** — an optional, permitted choice.
- **OPEN** — a decision that is **deliberately not settled**. It MUST NOT be implemented as if final, MUST NOT be hard-coded into contracts or doctrine as settled law, and MUST be resolved by the owner (and, where noted, legal/compliance) before implementation.

---

## 2. Purpose

AFI Settlement v1 defines **how a qualified signal becomes a provable, auditable, epoch-settled reward** without conflating *provenance* (who produced what, and is it true) with *payout* (who gets paid, how much, when). v1 exists to:

1. Make **every qualified signal independently traceable and verifiable** from chain data + a published manifest, without trusting AFI's private infrastructure.
2. **Decouple provenance from payout** so that recording a signal never, by itself, moves tokens.
3. Settle rewards **by epoch**, through a **custodial vault / claim layer**, against a **single committed manifest** — not per-signal, not push-to-wallet, not at mint time.
4. Establish **concrete addresses, chain IDs, Safe thresholds, and signer policy as the source of truth**, with ENS names as human-readable aliases only.
5. Keep clearly-open economic and legal questions **open**, rather than freezing premature mechanics into code.

---

## 3. The Four-Layer Model

AFI Settlement v1 is a four-layer architecture. Each layer has a **dedicated canonical spec** (see §15). The layers are strictly ordered: a later layer MUST NOT collapse into an earlier one.

```
┌─────────────────────────────────────────────────────────────────────────┐
│ Layer 1 — PER-SIGNAL PROVENANCE                                           │
│   Every qualified signal is recorded off-chain (TSSD evidence) and        │
│   committed on-chain as part of a BATCH ROOT (EAS-backed Merkle).         │
│   Output: signalRoot / evidenceRoot leaves, independently verifiable.     │
│   → AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md                               │
├─────────────────────────────────────────────────────────────────────────┤
│ Layer 2 — STRATEGY / EPOCH REPUTATION                                     │
│   One ERC-6909 receipt per (strategyId, epochId): aggregate reputation,   │
│   NOT a payout instrument. Soulbound by default.                          │
│   → AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md                                │
├─────────────────────────────────────────────────────────────────────────┤
│ Layer 3 — EPOCH SETTLEMENT MANIFEST                                       │
│   The canonical per-epoch document binding qualified set, role            │
│   allocations, ruleset hash, and distribution roots. The bridge between   │
│   PROOF and MONEY. Committed once per epoch.                              │
│   → AFI_EPOCH_SETTLEMENT_MANIFEST.md                                      │
├─────────────────────────────────────────────────────────────────────────┤
│ Layer 4 — VAULT-BASED REWARD CUSTODY / ROUTING / CLAIMING                 │
│   Rewards mint/transfer to a RewardsVault per epoch, then are claimed     │
│   (Merkle proof) or routed by role. The vault ENFORCES the manifest;      │
│   it does not decide rewards.                                             │
│   → AFI_REWARDS_VAULT_AND_CLAIMS.md                                       │
└─────────────────────────────────────────────────────────────────────────┘
```

**Layer separation laws (MUST):**

- **L-SEP-1 (MUST):** Recording provenance (Layer 1) MUST NOT mint, transfer, or escrow any reward token. Provenance and payout are separate transactions, separate artifacts, and separate trust assumptions.
- **L-SEP-2 (MUST):** Reputation receipts (Layer 2) MUST NOT be transferable claims on tokens and MUST NOT be used as the unit of payout.
- **L-SEP-3 (MUST):** The manifest (Layer 3) is the **only** authority that decides who is owed what for an epoch. No contract downstream of the manifest may recompute eligibility or scores.
- **L-SEP-4 (MUST):** The RewardsVault (Layer 4) MUST pay strictly against a committed manifest root and MUST NOT decide eligibility, mint, or pay outside that root.

---

## 4. Locked Decisions (v1 Law)

These are owner-approved and locked. Each maps to an ADR.

| # | Locked decision | Normative | ADR |
|---|-----------------|-----------|-----|
| D1 | AFI rewards settle **by epoch**, not per signal. | Reward payout MUST be epoch-batched. Per-signal direct minting to a final wallet MUST NOT be the v1 mainnet settlement path. | ADR-001, ADR-004 |
| D2 | **Provenance ≠ payout.** Every qualified signal MUST remain traceable, but recording it MUST NOT pay it. | MUST | ADR-001 |
| D3 | Strategy/epoch reputation receipts use **ERC-6909** (not ERC-1155) for v1. | v1 strategy/epoch receipts MUST be ERC-6909. ERC-1155 MUST NOT be introduced as the v1 receipt standard. | ADR-002 |
| D4 | AFI retains the **xERC20** token posture for v1. | The AFI token MUST remain xERC20-compatible for v1. | ADR-003 |
| D5 | **ERC-7802 / SuperchainERC20 is deferred.** | v1 MUST NOT require ERC-7802. Adoption is a future, separate decision. | ADR-003 |
| D6 | Rewards flow through a **RewardsVault + manifest-backed claim/route** layer. | The vault MUST custody the epoch budget and pay only against the committed manifest root. | ADR-004 |
| D7 | **ENS names are aliases; concrete addresses are the source of truth.** | Contracts MUST NOT resolve ENS for access control or fund routing. Configs/governance MUST treat concrete address + chainId as authoritative. | ADR-005 |
| D8 | Legal **clawback / escheatment / unclaimed-reward** mechanics are **OPEN**. | These MUST NOT be hard-coded or asserted as final policy until legal/compliance review. | ADR-006 |
| D9 | v0 `mintForSignal`-style architecture is **deprecated as mainnet architecture**. | MUST NOT be activated as the production reward flow; MUST NOT be presented as canonical. | ADR-001, `AFI_V0_DEPRECATION_AND_MIGRATION.md` |
| D10 | **Agent boundary.** Agents MAY submit manifests under scoped permissions. | Agents MUST NEVER control treasury funds, production private keys, upgrades, Safe roles, or deployments. | ADR-001, ADR-005 |

---

## 5. Deprecated (v0 posture)

The following are **deprecated as mainnet/v1 architecture**. They MAY be retained as historical/prototype artifacts (clearly labelled) but MUST NOT be taught as canonical:

- **`AFIMintCoordinator.mintForSignal` → `AFIToken.mintEmissions(beneficiary, amount)`** as the reward path (per-signal, single beneficiary, push-to-wallet at mint time).
- **`AFISignalReceipt` (ERC-1155)** as the v1 receipt standard. (It MAY remain a v0 prototype/historical artifact; it is **not** the Layer-2 reputation receipt and **not** a payout instrument.)
- Any **single `beneficiary` / `tokenAmount` / `receiptAmount`** per-signal payout structure as the canonical distribution shape.
- Any documentation claiming the v0 Base Sepolia contracts are **"mainnet-ready"** or that AFI has **"no centralized control"** while a single 1-of-1 Safe holds admin + emissions authority.
- The Snapshot space pointer using the **legacy (non-canonical) three-letter ENS alias** in any *governance* sense (see §11).

See `AFI_V0_DEPRECATION_AND_MIGRATION.md` for the full migration posture and the runtime-sensitive items that MUST be left to the owner.

---

## 6. Open Questions (NOT settled)

The following are **OPEN**. They MUST NOT be implemented as final:

- **O1 — Legal clawback / escheatment** of unclaimed or challenge-failed rewards (mechanics, jurisdiction, custody of forfeited funds). Pending legal/compliance.
- **O2 — Unclaimed-reward policy** (expiry window, recycle vs. roll-forward vs. return-to-treasury). A *placeholder* hook MAY be specified; the *policy value* is OPEN.
- **O3 — Exact tokenomics splits** across Providers / Analysts-Scorers / Validators / public-goods (the research gauge in `afi-econ` is **not** final law).
- **O4 — Holdback / vesting** schedule for rewards under challenge windows.
- **O5 — Reserve allocation** and whether an L1 reserve vault exists at all.
- **O6 — Exact EAS schema** field encodings and the precise on-chain anchor contract (the *direction* — EAS/Merkle batch-root — is locked; the *schema details* are implementation design).
- **O7 — Push (router) vs. pull (claims)** as the default distribution mode (both are permitted; the manifest MUST support proof-based pull at minimum).
- **O8 — Production Safe topology** (N-of-M thresholds, signer set, timelock) — the *principle* (not 1-of-1, addresses are truth) is locked; the *parameters* are owner decisions.

---

## 7. Off-Chain Evidence vs. On-Chain Commitments

AFI v1 is **commit-on-chain, store-off-chain**:

- **MUST:** The dense signal record (raw + enriched + scored lifecycle) lives **off-chain** in the **TSSD evidence vault** (a *data* store — **not** a token vault; see §10). Raw signal data MUST remain off-chain until the configured **delayed-disclosure** window elapses.
- **MUST:** The on-chain footprint per epoch is **commitments** — Merkle/EAS **roots** and hashes (`signalRoot`, `evidenceRoot`, `strategyRoot`, `claimRoot`, `rulesetHash`) plus pointers (`manifestURI`) — **not** raw signal arrays.
- **MUST NOT:** Raw per-signal arrays, scores, or evidence blobs MUST NOT be written on-chain.
- **MUST:** Every qualified signal MUST be **independently verifiable**: given the published manifest and the off-chain (post-disclosure) data, anyone MUST be able to reproduce the leaf and verify its inclusion under the committed root.

**TSSD vault vs. reward vault (naming law):** "TSSD vault" / "evidence vault" / `VaultedSignalRecord` refer to **data custody**. "RewardsVault" / "TreasuryVault" refer to **token custody**. Docs MUST NOT use bare "vault" in a way that conflates the two. The TSSD evidence vault is **unchanged** by Settlement v1.

---

## 8. Per-Signal Provenance vs. Reward Settlement (the core law)

- **MUST:** A per-signal provenance record/commitment is a statement of *truth and authorship*. It is **not** a reward, an IOU, or a claim.
- **MUST NOT:** A provenance artifact (EAS attestation, signal leaf, ERC-6909 reputation receipt, or any v0 ERC-1155 receipt) MUST NOT be redeemable for tokens.
- **MUST:** Reward entitlement is established **only** by inclusion in a **committed EpochSettlementManifest** `claimRoot` (Layer 3), and realized **only** through the RewardsVault/claim layer (Layer 4).

This closes the v0 contradiction in which the same `mintForSignal` call emitted both a provenance receipt and the reward.

---

## 9. Epoch-Batched Reward Law

- **MUST:** Rewards are computed and settled **per epoch** (AFI's `afi-math` schedule defines epoch cadence; off-chain).
- **MUST:** At epoch close, an **EpochSettlementManifest** (Layer 3) is produced and **committed once** (a single manifest root per epoch).
- **MUST:** The epoch reward budget is funded **to the RewardsVault** (lump sum), **not** to end users, and the per-epoch budget cap is enforced **at that funding seam**.
- **SHOULD:** Distribution to role-holders SHOULD occur in the **following** epoch to allow challenge/holdback windows to apply.
- **MUST NOT:** No reward may be paid for an epoch except against that epoch's committed manifest root.

---

## 10. Token Posture — xERC20 Retained, ERC-7802 Deferred

- **MUST:** The AFI token retains its **xERC20** posture for v1 (bridge-mint/burn with rate limits; the existing `XERC20Lockbox` remains the canonical-token custody for *bridging*, not rewards).
- **MUST NOT:** v1 MUST NOT require **ERC-7802 / SuperchainERC20**. ERC-7802 adoption is **deferred** to a future, separate owner decision (ADR-003) and MUST NOT be presented as a v1 dependency.
- **MUST:** The bridge lockbox MUST NOT be repurposed as the reward or treasury vault.

---

## 11. ENS Aliases vs. Concrete Address Source of Truth

- **MUST:** ENS names (e.g. `afidao.eth` and its subnames `treasury` / `reserve` / `grants` / `ops` / `liq`) are **human-readable aliases only**.
- **MUST:** **Concrete addresses + chainId + Safe threshold + signer policy** are the **source of truth** for contracts, configs, governance, and settlement.
- **MUST NOT:** Contracts MUST NOT resolve ENS dynamically for access control, fund routing, or authorization.
- **Governance pointer law (MUST):** The live AFI DAO Snapshot/governance space is **`afidao.eth`** (network 1). References to the **legacy (non-canonical) three-letter ENS alias** as the Snapshot/governance space are **stale/incorrect** and MUST be corrected in docs/examples (runtime config carrying that previously-used non-canonical alias is **runtime-sensitive** and is owner-deferred — see `AFI_V0_DEPRECATION_AND_MIGRATION.md`).
- **Treasury reconciliation law (MUST):** `treasury.afidao.eth` currently resolves to an **empty placeholder Safe** and is **NOT** the real Base Treasury Safe `0x1Dd6705ff84Ecd5eaDc51A913Ad8e2c6C9E79aC4`. Docs MUST NOT present `treasury.afidao.eth` as the production treasury. The real Safe MUST be reconciled in a future concrete-address registry.

See `AFI_ENS_SAFE_ADDRESS_REGISTRY_DOCTRINE.md`.

---

## 12. Safe / Governance Hardening Principles

- **MUST NOT:** **1-of-1 Safe control is not production-grade.** Treasury, reserve, and settlement authority MUST NOT remain under a single 1-of-1 Safe for mainnet v1.
- **SHOULD:** Production authority SHOULD be an **N-of-M multisig + timelock**, with a documented signer roster and threshold.
- **MUST:** Authority over the SettlementCoordinator / RewardsVault MUST be held by a documented Safe (ideally + timelock); governance (Snapshot `afidao.eth` + Zodiac Reality, where wired) gates parameter changes.
- **MUST:** A **concrete-address registry** (ENS alias → resolved address → chainId → account type → Safe threshold → status → allowed/forbidden actions → controller) MUST exist before settlement contracts reference any account.

---

## 13. Agent Boundary Rules

- **MAY:** Agents MAY compute/score signals, build provenance leaves, and **submit** epoch settlement manifests for review under **scoped, least-privilege permissions**.
- **MUST NOT:** Agents MUST NEVER control treasury funds, hold or use production private keys, perform contract upgrades, hold or change Safe roles/thresholds, or execute deployments.
- **MUST:** Any agent-submitted manifest MUST pass human/governance authorization before it can be committed as the epoch's settlement root and before any funding occurs.

---

## 14. v0 Migration / Deprecation Posture (summary)

- **MUST:** v0 Base Sepolia contracts are **prototypes**; they MUST NOT be treated as mainnet-ready.
- **MUST NOT:** Do **not** grant roles to activate per-signal reward minting as a production flow.
- **MUST NOT:** Do **not** migrate flawed testnet state into v1.
- **MAY:** `AFIToken` / xERC20 MAY be retained. `AFIMintCoordinator` MUST NOT be treated as the v1 coordinator. `AFISignalReceipt` (ERC-1155) MAY be retained only as a historical/prototype artifact unless separately approved.
- **MUST:** v1 MUST be cleanly specified (this doctrine set) **before** any Solidity changes.

Full detail: `AFI_V0_DEPRECATION_AND_MIGRATION.md`.

---

## 15. Canonical Artifacts & Field Registry (shared shapes)

This registry is the **authoritative field list** for v1 artifacts. The sub-specs elaborate semantics but MUST NOT contradict these field sets. Exact encodings/types are implementation design (OPEN where noted); the **field presence and meaning** are doctrine.

### 15.1 Signal provenance leaves (Layer 1) — `AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md`
Commitment direction: **EAS-backed Merkle batch root on Base**, batch-root-first (NOT per-signal NFT minting).

- Epoch/anchor fields: `epochId`, `strategyId`, `signalRoot`, `evidenceRoot`, `rulesetHash`, `disclosureWindow`, `manifestURI`, `attestationUID` (if EAS), `disclosureStatus`.
- **Signal leaf** (per qualified signal): `signalId`, `strategyId`, `epochId`, `contentHash`, `scoreCommitment`, `producer` (identity ref), `timestamp`, `rulesetHash`.
- **Evidence leaf** (per signal lifecycle): `signalId`, `evidenceHash` (RAW→…→SCORED snapshot hash), `stage`, `disclosureStatus`.

### 15.2 Strategy/epoch receipt (Layer 2) — `AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md`
Standard: **ERC-6909**, soulbound by default.

- `receiptId = hash(strategyId, epochId)` (deterministic derivation).
- `owner` (strategy controller / reputation subject), `balance|score` (reputation magnitude semantics — NOT a token claim), `finalized` flag.
- Linkage: references `signalRoot`, `evidenceRoot`, `strategyRoot`, and the `EpochSettlementManifest` (by `epochId` + manifest root).
- Immutability: receipts SHOULD be immutable after epoch finalization (updates OPEN/owner-decided).

### 15.3 EpochSettlementManifest (Layer 3) — `AFI_EPOCH_SETTLEMENT_MANIFEST.md`
The bridge between proof and money. Committed once per epoch.

- Identity/version: `epochId`, `settlementVersion`, `rulesetHash`, `chainId`, `contractAddresses`.
- Proof roots: `signalRoot`, `evidenceRoot`, `strategyRoot`, `claimRoot`.
- Economics: `totalRewardPool`, `roleAllocationRoots|roleAllocationLeaves` (Providers / Analysts-Scorers / Validators / public-goods), strategy/epoch receipt references.
- Policy refs: `challengeWindow`, `holdbackPolicyRef`, `unclaimedRewardPolicyRef` (placeholder; value OPEN).
- Pointers/meta: `manifestURI`, `disclosureURI` (delayed-disclosure reference), `finalizedTimestamp`, `submitter|signerMetadata`.
- **MUST:** No raw signal arrays on-chain. The vault enforces the manifest; it does not decide rewards.

### 15.4 RewardsVault / claims (Layer 4) — `AFI_REWARDS_VAULT_AND_CLAIMS.md`
- Funding flow (mint/transfer epoch budget to vault), claim flow (Merkle proof) or manifest-backed routing, double-claim prevention (claimed bitmap/nullifier), pause behavior, challenge window, holdbacks, failed-claim handling.
- `unclaimedRewardPolicy` = **placeholder** (value OPEN); legal clawback/escheatment = **OPEN** (MUST NOT be final).
- Role allocations for Providers / Analysts-Scorers / Validators (exact split values = OPEN, see O3).

### 15.5 ENS/Safe registry entry — `AFI_ENS_SAFE_ADDRESS_REGISTRY_DOCTRINE.md`
- `ensAlias`, `resolvedAddress`, `chainId`, `accountType`, `safeThreshold`, `status`, `allowedActions`, `forbiddenActions`, `controller`.

---

## 16. Conformance

A document, schema, comment, or contract **conforms to AFI Settlement v1** if and only if it does not contradict §4 (Locked Decisions), §7–§13, and §15. Artifacts that describe v0 *as historical reality* (audit reports, recon) conform as long as they do not present v0 as the intended/canonical future. Non-conforming **prescriptive** docs MUST be corrected or banner-deprecated; non-conforming **runtime** artifacts are owner-deferred and listed in the contradiction report.

---

## 17. Change Control

- This doctrine and its ADRs change only via a new ADR (or an ADR superseding an existing one). Editing a Locked Decision MUST be done through an ADR with `Status: Superseded` on the prior decision.
- OPEN items are resolved by an ADR that moves them to Locked, citing the owner (and legal/compliance for O1/O2).

---

## 18. Related Documents

**Specs (this set):**
- `AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md` — Layer 1.
- `AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md` — Layer 2.
- `AFI_EPOCH_SETTLEMENT_MANIFEST.md` — Layer 3.
- `AFI_REWARDS_VAULT_AND_CLAIMS.md` — Layer 4.
- `AFI_ENS_SAFE_ADDRESS_REGISTRY_DOCTRINE.md` — addresses/ENS/Safe source-of-truth.
- `AFI_V0_DEPRECATION_AND_MIGRATION.md` — v0 posture.

**ADRs:**
- [`../adrs/ADR-001-four-layer-settlement-architecture.md`](../adrs/ADR-001-four-layer-settlement-architecture.md)
- [`../adrs/ADR-002-erc6909-strategy-epoch-receipts.md`](../adrs/ADR-002-erc6909-strategy-epoch-receipts.md)
- [`../adrs/ADR-003-xerc20-retained-erc7802-deferred.md`](../adrs/ADR-003-xerc20-retained-erc7802-deferred.md)
- [`../adrs/ADR-004-rewards-vault-merkle-claims.md`](../adrs/ADR-004-rewards-vault-merkle-claims.md)
- [`../adrs/ADR-005-ens-aliases-addresses-source-of-truth.md`](../adrs/ADR-005-ens-aliases-addresses-source-of-truth.md)
- [`../adrs/ADR-006-unclaimed-rewards-legal-clawback-open.md`](../adrs/ADR-006-unclaimed-rewards-legal-clawback-open.md)

**Prior recon (descriptive, still accurate):**
- `../../reports/afi-vault-architecture-recon.md`
- `../../reports/afi-settlement-semantics-recon.md`
- `../../reports/afi-signal-provenance-vs-reward-settlement-recon.md`
- `../../reports/afi-onchain-contract-discovery.md`
- `../../reports/afi-ens-vault-registry-recon.md`

---

*Canonical doctrine. This document defines architecture and law only; it implements nothing on-chain. v0 remains as a prototype and as accurately described in existing audit/recon reports; this doctrine governs the intended v1 architecture.*
