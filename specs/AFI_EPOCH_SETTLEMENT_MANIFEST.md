# AFI Epoch Settlement Manifest

**Status:** CANONICAL — Accepted (v1 doctrine)
**Date:** 2026-06-24
**Part of:** AFI Settlement v1 — see [AFI_SETTLEMENT_V1_DOCTRINE.md](./AFI_SETTLEMENT_V1_DOCTRINE.md)

---

## 0. Scope and Authority

This document is the **Layer 3** canonical specification of AFI Settlement v1: the **EpochSettlementManifest**. It defines the manifest's field set, its meaning, its lifecycle, and the normative rules that bind it to the layers above and below it.

This is **doctrine and design only**. It implements nothing. No contract described here is built, deployed, or executed. No funds move, no roles are granted, and no manifest is committed by virtue of this document existing. Exact field encodings, Solidity types, ABI shapes, and the precise on-chain commitment contract are **implementation design**, not settled here. What is settled here is the **presence and meaning** of each field, and the laws governing how the manifest is produced, committed, and enforced.

Where this document and [AFI_SETTLEMENT_V1_DOCTRINE.md](./AFI_SETTLEMENT_V1_DOCTRINE.md) (the constitution) appear to conflict on a v1 architecture question, **the constitution wins**. This spec elaborates §3 (Layer 3), §8, §9, §13, and §15.3 of the constitution and MUST NOT contradict them.

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, **MAY**, and **OPEN** are used as defined in [AFI_SETTLEMENT_V1_DOCTRINE.md §1](./AFI_SETTLEMENT_V1_DOCTRINE.md). **OPEN** means deliberately unsettled: it MUST NOT be implemented as final, MUST NOT be hard-coded as settled law, and MUST be resolved by the owner (and, where noted, legal/compliance) before implementation.

---

## 1. What the Manifest Is

The **EpochSettlementManifest** is the canonical per-epoch document that binds the qualified set, the role allocations, the ruleset hash, and the distribution roots for a single epoch. It is produced **once per epoch** at epoch close.

> **The manifest is the BRIDGE between PROOF and MONEY.**

Everything below it (Layer 4 — the RewardsVault and claim/route layer) is mechanics: custody, proofs, transfers, pause, holdbacks. Everything above it (Layers 1 and 2 — per-signal provenance and strategy/epoch reputation) is evidence: who produced what, whether it was true, and how much reputation accrued. The manifest is the single artifact that **converts adjudicated proof into an enforceable schedule of who is owed what for the epoch**.

Stated as law:

- **MANIFEST-1 (MUST):** The EpochSettlementManifest is the **only** authority that decides who is owed what for an epoch. This is the constitution's L-SEP-3 ([AFI_SETTLEMENT_V1_DOCTRINE.md §3](./AFI_SETTLEMENT_V1_DOCTRINE.md)).
- **MANIFEST-2 (MUST):** Reward entitlement is established **only** by inclusion in a committed manifest's `claimRoot`, and realized **only** through the Layer 4 RewardsVault/claim layer ([AFI_SETTLEMENT_V1_DOCTRINE.md §8](./AFI_SETTLEMENT_V1_DOCTRINE.md)).
- **MANIFEST-3 (MUST):** Exactly **one** committed manifest root exists per `(epochId)` for the v1 mainnet settlement path. There is no per-signal manifest and no per-signal settlement.
- **MANIFEST-4 (MUST NOT):** No contract downstream of the manifest MUST recompute eligibility, scores, or amounts. The vault **enforces** the manifest; it **does not decide** rewards.
- **MANIFEST-5 (MUST NOT):** No **raw signal arrays**, per-signal scores, or evidence blobs MUST appear in the on-chain footprint of the manifest. The on-chain footprint is **commitments** (roots and hashes) plus pointers (URIs). Raw data stays off-chain in the TSSD evidence vault until the delayed-disclosure window elapses ([AFI_SETTLEMENT_V1_DOCTRINE.md §7](./AFI_SETTLEMENT_V1_DOCTRINE.md)).

### 1.1 What the Manifest Is Not

| The manifest is NOT | Because |
|---|---|
| A token, IOU, or balance | Provenance ≠ payout. The manifest *records* entitlement; it does not *hold* funds. Custody is Layer 4. |
| A scoring engine | Scores and qualification are decided upstream (Layers 1–2) and at the off-chain epoch-close computation. The committed manifest is the *result*, not the *process*. |
| A per-signal artifact | Settlement is epoch-batched. Per-signal direct minting is deprecated v0 architecture ([AFI_SETTLEMENT_V1_DOCTRINE.md §5, D9](./AFI_SETTLEMENT_V1_DOCTRINE.md)). |
| A reputation receipt | Layer 2 ERC-6909 receipts are reputation, soulbound, non-redeemable. The manifest references them; it is not one of them. |
| Self-authorizing | An agent or generator MAY *build* and *submit* a manifest, but it becomes the epoch's settlement root only after human/governance authorization (see §6). |

---

## 2. Canonical Field Registry

The fields below are the authoritative Layer 3 field set. They expand [AFI_SETTLEMENT_V1_DOCTRINE.md §15.3](./AFI_SETTLEMENT_V1_DOCTRINE.md) and MUST NOT contradict it. Field names are reused **verbatim** from the constitution's registry.

**Encoding note (applies to the whole table):** the **type/encoding** columns describe *implementation design direction only*. Whether a value is a `bytes32`, a URI string, a packed struct, or an EAS-schema field is OPEN and owner/implementation-decided. What is normative here is the **field's presence and meaning**.

### 2.1 Identity / Version

| Field | Presence | Meaning | Notes |
|---|---|---|---|
| `epochId` | MUST | The accounting epoch this manifest settles. Exactly one committed manifest per `epochId`. | Epoch cadence is defined off-chain by `afi-math`; the manifest does not redefine it. |
| `settlementVersion` | MUST | The version of the settlement format/semantics this manifest conforms to. | Lets future format changes be unambiguous without reinterpreting old manifests. Distinct from `rulesetHash`. |
| `rulesetHash` | MUST | Cryptographic pin of the emissions + scoring + validation + allocation rules used to produce this manifest. | Same field name and meaning as Layers 1–2. Binds the manifest to a frozen ruleset so the result is reproducible. |
| `chainId` | MUST | The chain on which this manifest's root is committed and on which the vault enforces it (Base for v1). | Concrete `chainId` is source of truth, not ENS ([AFI_SETTLEMENT_V1_DOCTRINE.md §11, D7](./AFI_SETTLEMENT_V1_DOCTRINE.md)). |
| `contractAddresses` | MUST | The concrete addresses of the contracts this manifest binds to (commitment/coordinator contract, RewardsVault, distributor, token). | Concrete address + `chainId` is authoritative. Contracts MUST NOT resolve ENS for routing or access control. |

### 2.2 Proof Roots

These are the commitments that make the manifest's claims independently verifiable against off-chain (post-disclosure) data. They are **roots/hashes only** — never raw arrays.

| Field | Presence | Meaning | Notes |
|---|---|---|---|
| `signalRoot` | MUST | Merkle/EAS root over the qualified **signal leaves** for the epoch (Layer 1). | Same field as [AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md](./AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md) §15.1. |
| `evidenceRoot` | MUST | Merkle root over the per-signal **evidence leaves** (RAW→…→SCORED lifecycle snapshots). | Lets a verifier reproduce the evidence chain for any qualified signal post-disclosure. |
| `strategyRoot` | MUST | Merkle root over the strategy/epoch reputation set (Layer 2 receipts) for the epoch. | Ties the manifest to the ERC-6909 receipts in [AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md](./AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md). |
| `claimRoot` | MUST | Merkle root over the **entitlement leaves** — the (recipient, role, amount, constraints) tuples that the vault pays against. | This is the **money root**. The Layer 4 vault pays strictly against `claimRoot` and nothing else. |

- **PROOF-1 (MUST):** All four roots MUST be present in a committed manifest. Their on-chain representation MAY be a single committed manifest root that binds them (see §3.2), but each MUST be derivable/verifiable.
- **PROOF-2 (MUST):** Given the published manifest and the off-chain post-disclosure data, anyone MUST be able to reproduce every leaf and verify its inclusion under the committed root ([AFI_SETTLEMENT_V1_DOCTRINE.md §7](./AFI_SETTLEMENT_V1_DOCTRINE.md)).
- **PROOF-3 (MUST):** `claimRoot` MUST be a function of (and reconcilable with) `signalRoot`, `evidenceRoot`, `strategyRoot`, `rulesetHash`, and `totalRewardPool`. The money MUST trace back to proof.

### 2.3 Economics

| Field | Presence | Meaning | Notes |
|---|---|---|---|
| `totalRewardPool` | MUST | The total reward budget allocated to this epoch's manifest. | The funding cap is enforced at the vault-funding seam ([AFI_SETTLEMENT_V1_DOCTRINE.md §9](./AFI_SETTLEMENT_V1_DOCTRINE.md)). The pool size derives from the `afi-math` emissions schedule; the manifest records it, it does not invent it. |
| `roleAllocationRoots` \| `roleAllocationLeaves` | MUST | The per-role allocation of `totalRewardPool` across the canonical roles: **Providers**, **Analysts-Scorers**, **Validators**, and **public-goods**. | MAY be expressed as a root (for proof-based pull) or as explicit leaves (for routing). At least one form MUST be present and MUST reconcile to `totalRewardPool`. **The exact split values are OPEN** (see §2.6, O3). |
| strategy/epoch receipt references | MUST | References to the Layer 2 ERC-6909 receipts (`receiptId = hash(strategyId, epochId)`) backing each strategy's contribution in this epoch. | Receipts are **reputation, not claims**. The manifest references them for traceability; they are never redeemable ([AFI_SETTLEMENT_V1_DOCTRINE.md §8, L-SEP-2](./AFI_SETTLEMENT_V1_DOCTRINE.md)). |

- **ECON-1 (MUST):** The sum of the role allocations MUST reconcile to `totalRewardPool`. Any residual MUST be accounted for by an explicit policy reference (e.g. `unclaimedRewardPolicyRef`, public-goods), never silently dropped or silently retained.
- **ECON-2 (MUST NOT):** The manifest MUST NOT encode a **single `beneficiary` / `tokenAmount` / `receiptAmount`** per-signal payout shape. That is the deprecated v0 distribution shape ([AFI_SETTLEMENT_V1_DOCTRINE.md §5](./AFI_SETTLEMENT_V1_DOCTRINE.md)).
- **ECON-3 (OPEN):** The exact role split percentages across Providers / Analysts-Scorers / Validators / public-goods are **OPEN** (O3). The research gauge in `afi-econ` is **not** final law. The manifest commits to the *presence* of role allocation; it MUST NOT freeze the *values* as doctrine.

### 2.4 Policy References

These bind the manifest to the policies the Layer 4 vault must honor. They are **references** (hashes/URIs/identifiers), not the policy text itself, so policy can be governed independently and audited by hash.

| Field | Presence | Meaning | Notes |
|---|---|---|---|
| `challengeWindow` | MUST | The window during which this epoch's settlement (or specific claims) MAY be challenged before funds are releasable. | Distribution SHOULD occur in the *following* epoch to let this window apply ([AFI_SETTLEMENT_V1_DOCTRINE.md §9](./AFI_SETTLEMENT_V1_DOCTRINE.md)). |
| `holdbackPolicyRef` | MUST | Reference to the holdback/vesting policy that governs withheld portions of rewards under challenge/vesting. | The **policy value** (schedule, fraction, vesting curve) is **OPEN** (O4). The manifest commits to the *hook*; not the *value*. |
| `unclaimedRewardPolicyRef` | MUST (as placeholder) | Reference to the policy for rewards that are never claimed within the claim window. | **PLACEHOLDER. The policy value is OPEN** (O2): expiry window, recycle vs. roll-forward vs. return-to-treasury are all unsettled. Legal clawback/escheatment is **OPEN** (O1) and pending legal/compliance. The field MUST be present as a hook; it MUST NOT be implemented as if its value is final. |

- **POLICY-1 (MUST):** The manifest MUST carry these references so the Layer 4 vault can enforce the correct, governed policy version. The vault MUST NOT invent or substitute its own policy.
- **POLICY-2 (MUST NOT):** `unclaimedRewardPolicyRef` and any clawback/escheatment mechanics MUST NOT be hard-coded or asserted as final policy until legal/compliance review ([AFI_SETTLEMENT_V1_DOCTRINE.md §6 O1/O2, D8](./AFI_SETTLEMENT_V1_DOCTRINE.md)). A reference to an unresolved placeholder is permitted; a *committed value* claiming to be final is not.

### 2.5 Pointers / Disclosure / Meta

| Field | Presence | Meaning | Notes |
|---|---|---|---|
| `manifestURI` | MUST | Off-chain pointer to the full manifest document (the dense version with role allocations, leaves, and proof material needed to reconstruct the roots). | On-chain stores the root + this pointer, never the body. Storage SHOULD be content-addressed so the URI is tamper-evident against the committed root. |
| `disclosureURI` \| delayed-disclosure reference | MUST | Reference to the delayed-disclosure surface — where raw signal/evidence data becomes available **after** the configured disclosure window elapses. | Raw data MUST remain off-chain (in the TSSD evidence vault) until disclosure ([AFI_SETTLEMENT_V1_DOCTRINE.md §7](./AFI_SETTLEMENT_V1_DOCTRINE.md)). MAY be a pointer to a future-dated release; MUST track `disclosureStatus`. |
| `finalizedTimestamp` | MUST | The time at which the manifest was finalized/committed as the epoch's settlement root. | Anchors the start of challenge/holdback/claim windows. |
| `submitter` \| `signerMetadata` | MUST | Metadata identifying who **submitted** the manifest and who **authorized/signed** its commitment (e.g. the agent/generator that built it, and the human/governance/Safe that authorized commit + funding). | An agent-submitted manifest MUST record both the submitting agent and the human/governance authorizer (see §6). Concrete signer addresses + `chainId` are source of truth, ENS is alias only. |

- **META-1 (MUST):** `manifestURI` and the committed root MUST be mutually verifiable: fetching `manifestURI` and recomputing the roots MUST reproduce the committed root.
- **META-2 (SHOULD):** The off-chain manifest body SHOULD be content-addressed (e.g. IPFS/Arweave-style) so that `manifestURI` cannot be silently mutated after commitment.

### 2.6 OPEN Items Carried by the Manifest (do not implement as final)

| Field / area | OPEN ref | What is committed (presence/meaning) | What is OPEN (value) |
|---|---|---|---|
| `roleAllocationRoots`/`roleAllocationLeaves` split | O3 | Role allocation across Providers / Analysts-Scorers / Validators / public-goods MUST be present and reconcile to `totalRewardPool`. | The exact split percentages. |
| `holdbackPolicyRef` | O4 | A holdback/vesting hook MUST be referenced. | The schedule/fraction/vesting curve. |
| `unclaimedRewardPolicyRef` | O1, O2 | A placeholder hook for unclaimed rewards MUST be present. | The policy itself (expiry, recycle/roll-forward/return-to-treasury) and any legal clawback/escheatment. |
| push vs. pull distribution mode | O7 | The manifest MUST support **proof-based pull** at minimum (i.e. `claimRoot` MUST exist). Routing (push) MAY also be supported via explicit `roleAllocationLeaves`. | Which mode is the *default*. |
| exact EAS schema / commitment encoding | O6 | The *direction* (EAS-backed Merkle batch root on Base, roots committed once) is locked. | The exact schema field encodings and the precise anchor contract. |

---

## 3. Manifest Lifecycle

The manifest moves through four phases. Each phase has distinct authority and a distinct trust assumption. The phases are strictly ordered.

```
┌──────────────────────────────────────────────────────────────────────┐
│ Phase A — BUILD (off-chain, at epoch close)                          │
│   Roll up qualified signals (L1) + reputation (L2) under a frozen     │
│   rulesetHash → compute role allocations → derive signalRoot,        │
│   evidenceRoot, strategyRoot, claimRoot → assemble manifest body.    │
│   Output: a candidate manifest + manifestURI. NO funds, NO commit.   │
├──────────────────────────────────────────────────────────────────────┤
│ Phase B — AUTHORIZE + COMMIT (single root on Base)                   │
│   Human/governance authorization (Safe / governance gate) reviews    │
│   the candidate. On approval, commit ONE manifest root for the       │
│   epoch on Base. This is the moment proof becomes binding money.     │
├──────────────────────────────────────────────────────────────────────┤
│ Phase C — FUND (lump sum to RewardsVault)                            │
│   Fund the RewardsVault with the epoch budget (totalRewardPool),     │
│   lump sum, NOT to end users. Per-epoch budget cap enforced AT THIS  │
│   funding seam. Authorized by the same human/governance authority.   │
├──────────────────────────────────────────────────────────────────────┤
│ Phase D — CLAIM / ROUTE (Layer 4)                                    │
│   Role-holders claim via Merkle proof against claimRoot (pull) or    │
│   are routed by role allocation (push). Challenge/holdback windows   │
│   apply. The vault ENFORCES; it does not decide.                     │
└──────────────────────────────────────────────────────────────────────┘
```

### 3.1 Phase A — Build (off-chain, at epoch close)

- **BUILD-1 (MUST):** The manifest is built **off-chain** at epoch close by rolling up the epoch's qualified signal leaves (Layer 1), evidence leaves (Layer 1), and strategy/epoch reputation (Layer 2), under a **frozen `rulesetHash`**.
- **BUILD-2 (MUST):** Building the manifest MUST NOT move, mint, escrow, or earmark any token. Build is pure computation over evidence ([AFI_SETTLEMENT_V1_DOCTRINE.md §3, L-SEP-1](./AFI_SETTLEMENT_V1_DOCTRINE.md)).
- **BUILD-3 (MUST):** The build MUST produce `signalRoot`, `evidenceRoot`, `strategyRoot`, and `claimRoot` such that they are reproducible from the off-chain data + `rulesetHash` (PROOF-2, PROOF-3).
- **BUILD-4 (MAY):** A scoped, least-privilege **agent/generator** MAY perform the build and produce a candidate manifest + `manifestURI` ([AFI_SETTLEMENT_V1_DOCTRINE.md §13](./AFI_SETTLEMENT_V1_DOCTRINE.md)). The candidate has **no authority** until Phase B.

### 3.2 Phase B — Authorize + Commit (single root on Base)

- **COMMIT-1 (MUST):** A candidate manifest MUST pass **human/governance authorization** before it can be committed as the epoch's settlement root ([AFI_SETTLEMENT_V1_DOCTRINE.md §13](./AFI_SETTLEMENT_V1_DOCTRINE.md)). An agent MUST NOT self-authorize a commit.
- **COMMIT-2 (MUST):** Exactly **one** manifest root MUST be committed per `epochId` on Base. The on-chain footprint is the committed root + `manifestURI` + the minimal binding fields — **never** raw signal arrays (MANIFEST-5).
- **COMMIT-3 (MUST):** Authority over the commitment (SettlementCoordinator / manifest-commit contract) MUST be held by a documented Safe (ideally + timelock); governance gates parameter changes ([AFI_SETTLEMENT_V1_DOCTRINE.md §12](./AFI_SETTLEMENT_V1_DOCTRINE.md)). **1-of-1 Safe control is not production-grade** and MUST NOT hold settlement authority for mainnet v1.
- **COMMIT-4 (MUST):** Commitment sets `finalizedTimestamp` and starts the `challengeWindow`. After commitment, the committed root is the binding authority for the epoch.
- **COMMIT-5 (SHOULD):** A committed manifest SHOULD be immutable. Correction of a flawed committed manifest SHOULD occur via an explicitly versioned superseding manifest under governance, not silent mutation. (The exact correction/supersession mechanism is implementation design.)

### 3.3 Phase C — Fund (lump sum to the RewardsVault)

- **FUND-1 (MUST):** The epoch reward budget MUST be funded **to the RewardsVault** as a lump sum (`totalRewardPool`), **not** to end users ([AFI_SETTLEMENT_V1_DOCTRINE.md §9](./AFI_SETTLEMENT_V1_DOCTRINE.md)).
- **FUND-2 (MUST):** The **per-epoch budget cap MUST be enforced at this funding seam.** Funding MUST be authorized by the same human/governance authority that authorized the commit (or a documented governance gate); an agent MUST NEVER control treasury funds or perform the funding transfer ([AFI_SETTLEMENT_V1_DOCTRINE.md §13, D10](./AFI_SETTLEMENT_V1_DOCTRINE.md)).
- **FUND-3 (MUST):** Funding MUST reference the committed manifest for the epoch. The vault MUST NOT be funded for an epoch that has no committed manifest root.
- **FUND-4 (MUST NOT):** The xERC20 bridge lockbox MUST NOT be repurposed as the reward or treasury vault ([AFI_SETTLEMENT_V1_DOCTRINE.md §10](./AFI_SETTLEMENT_V1_DOCTRINE.md)).

### 3.4 Phase D — Claim / Route (Layer 4)

- **CLAIM-1 (MUST):** Role-holders realize rewards **only** through the Layer 4 RewardsVault/claim layer ([AFI_REWARDS_VAULT_AND_CLAIMS.md](./AFI_REWARDS_VAULT_AND_CLAIMS.md)), paying strictly against the committed `claimRoot`.
- **CLAIM-2 (MUST):** The manifest MUST support **proof-based pull** at minimum (`claimRoot` exists; claimants present Merkle proofs). Push/routing by `roleAllocationLeaves` MAY also be supported; the default (push vs. pull) is **OPEN** (O7).
- **CLAIM-3 (SHOULD):** Distribution to role-holders SHOULD occur in the **following** epoch (N+1 for work in N) so the `challengeWindow` and holdback policy can apply ([AFI_SETTLEMENT_V1_DOCTRINE.md §9](./AFI_SETTLEMENT_V1_DOCTRINE.md)).
- **CLAIM-4 (MUST):** The vault **enforces** the manifest (root membership, claimed-bitmap/nullifier, pause, challenge/holdback) and **MUST NOT decide** eligibility, recompute scores, mint, or pay outside the committed root (MANIFEST-4; [AFI_SETTLEMENT_V1_DOCTRINE.md §3, L-SEP-4](./AFI_SETTLEMENT_V1_DOCTRINE.md)).

---

## 4. The Bridge Between Proof and Money (the central law)

This section restates, in one place, the load-bearing separation that the manifest exists to enforce.

| Plane | Layer | Artifact | What it asserts | Can it move tokens? |
|---|---|---|---|---|
| Proof | L1 | signal/evidence leaves under `signalRoot`/`evidenceRoot` | "this signal existed, was authored by X, scored Y, true" | **No** |
| Proof | L2 | ERC-6909 strategy/epoch receipt | "this strategy earned this much reputation in this epoch" | **No** (soulbound, non-redeemable) |
| **Bridge** | **L3** | **EpochSettlementManifest (`claimRoot`)** | **"for this epoch, these recipients are owed these amounts by role"** | **No — it records entitlement; Layer 4 moves the tokens** |
| Money | L4 | RewardsVault + claims/router | "pay against the committed `claimRoot`" | **Yes — but only against the manifest** |

- **BRIDGE-1 (MUST):** The manifest is the **single** crossing point from proof to money. Nothing in Layers 1–2 moves money; nothing in Layer 4 decides entitlement. The crossing happens exactly once, at the manifest, and is gated by human/governance authorization.
- **BRIDGE-2 (MUST):** Because the manifest is the only crossing, it MUST be the only place where per-epoch entitlement is decided, and it MUST be reproducible and auditable from chain data + the published manifest + post-disclosure off-chain data. A third party MUST be able to confirm, without trusting AFI's private infrastructure, that the money matches the proof.
- **BRIDGE-3 (MUST):** This closes the v0 contradiction in which a single `mintForSignal` call emitted **both** a provenance receipt **and** the reward in one transaction. In v1, proof (Layers 1–2) and money (Layer 4) are **separate transactions, separate artifacts, separate trust assumptions**, joined only by the committed manifest.

---

## 5. Conformance Rules (manifest-specific)

A manifest, generator, or contract **conforms to this spec** if and only if all of the following hold. These restate the constitution's invariants for Layer 3.

| # | Rule | Normative |
|---|---|---|
| CONF-1 | Exactly one committed manifest root exists per `epochId`. | MUST |
| CONF-2 | The on-chain footprint is roots + hashes + pointers only; no raw signal arrays, scores, or evidence blobs. | MUST NOT (raw on-chain) |
| CONF-3 | `claimRoot` traces back to `signalRoot`, `evidenceRoot`, `strategyRoot`, `rulesetHash`, `totalRewardPool` and is reproducible off-chain. | MUST |
| CONF-4 | Role allocations sum/reconcile to `totalRewardPool`; residuals are explicitly policy-referenced. | MUST |
| CONF-5 | `unclaimedRewardPolicyRef` and clawback/escheatment are carried as references to OPEN placeholders, never as committed final values. | MUST NOT (final) |
| CONF-6 | The manifest does not encode a single-`beneficiary`/`tokenAmount`/`receiptAmount` per-signal payout shape. | MUST NOT |
| CONF-7 | Strategy/epoch receipt references are to reputation (non-redeemable), not to payout instruments. | MUST |
| CONF-8 | The manifest is built off-chain, committed once on Base, funds the vault, then is claimed/routed — in that order. | MUST |
| CONF-9 | Any agent-built/submitted manifest passes human/governance authorization before commit and before funding. | MUST |
| CONF-10 | Concrete `contractAddresses` + `chainId` are authoritative; no ENS resolution for routing or access control. | MUST |

---

## 6. Agent Boundary (Layer 3 specifics)

The manifest is the **one** v1 artifact that agents are explicitly permitted to *submit*. That permission is narrow and is bounded by the constitution ([AFI_SETTLEMENT_V1_DOCTRINE.md §13, D10](./AFI_SETTLEMENT_V1_DOCTRINE.md)).

- **AGENT-1 (MAY):** Agents MAY compute/score signals, build provenance leaves, derive the manifest roots, and **submit** a candidate EpochSettlementManifest for review, under **scoped, least-privilege permissions**.
- **AGENT-2 (MUST):** Any agent-submitted manifest MUST pass **human/governance authorization** before it can be committed as the epoch's settlement root and **before any funding occurs**. The `submitter`/`signerMetadata` MUST record both the submitting agent and the human/governance authorizer.
- **AGENT-3 (MUST NOT):** Agents MUST NEVER control treasury funds, hold or use production private keys, perform contract upgrades, hold or change Safe roles/thresholds, execute deployments, commit the manifest root, or fund the vault. The agent's authority ends at *submission*; everything from commit onward is human/governance authority.

---

## 7. Relationship to Other Layers and Documents

| Document | Relationship |
|---|---|
| [AFI_SETTLEMENT_V1_DOCTRINE.md](./AFI_SETTLEMENT_V1_DOCTRINE.md) | The constitution. This spec elaborates §3 (Layer 3), §7–§9, §12–§13, §15.3 and MUST NOT contradict it. |
| [AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md](./AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md) | Layer 1. Supplies the signal/evidence leaves and `signalRoot`/`evidenceRoot` the manifest commits to. |
| [AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md](./AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md) | Layer 2. Supplies the reputation receipts and `strategyRoot` the manifest references (reputation, not claims). |
| [AFI_REWARDS_VAULT_AND_CLAIMS.md](./AFI_REWARDS_VAULT_AND_CLAIMS.md) | Layer 4. Enforces this manifest's `claimRoot`; custodies and pays the epoch budget; it does not decide rewards. |
| [AFI_ENS_SAFE_ADDRESS_REGISTRY_DOCTRINE.md](./AFI_ENS_SAFE_ADDRESS_REGISTRY_DOCTRINE.md) | Source of truth for the concrete `contractAddresses`, `chainId`, and the Safe/governance authority that authorizes commit/funding. |
| [AFI_V0_DEPRECATION_AND_MIGRATION.md](./AFI_V0_DEPRECATION_AND_MIGRATION.md) | Why per-signal `mintForSignal` is deprecated as mainnet architecture and MUST NOT be presented as the v1 settlement path. |
| ADRs `../adrs/ADR-001` … `../adrs/ADR-006` | The locked decisions (epoch settlement, provenance ≠ payout, ERC-6909, xERC20, vault-backed claims, OPEN legal items) that this manifest implements. |

---

## 8. Summary

The EpochSettlementManifest is the Layer 3 **bridge between proof and money**. It is built off-chain at epoch close from qualified signals (Layer 1) and strategy reputation (Layer 2) under a frozen `rulesetHash`; it commits a single root per epoch on Base; it carries the proof roots (`signalRoot`, `evidenceRoot`, `strategyRoot`, `claimRoot`), the economics (`totalRewardPool`, role allocations, receipt references), the policy references (`challengeWindow`, `holdbackPolicyRef`, `unclaimedRewardPolicyRef` — the last a placeholder whose value is OPEN), and the pointers/meta (`manifestURI`, `disclosureURI`, `finalizedTimestamp`, `submitter`/`signerMetadata`, `chainId`, `contractAddresses`). The RewardsVault **enforces** this manifest and **does not decide** rewards; **no raw signal arrays** ever go on-chain. Agents MAY submit manifests under scoped permissions but MUST pass human/governance authorization before any commit or funding.

---

*Canonical Layer 3 spec. Design and doctrine only; nothing here is implemented, deployed, or executed. Exact field encodings/types and the precise commitment contract are implementation design; OPEN items (legal clawback/escheatment, tokenomics splits, holdback/vesting, unclaimed-reward policy, exact EAS schema, push-vs-pull default) MUST NOT be implemented as final.*
