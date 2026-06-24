# ADR-002 — ERC-6909 Strategy/Epoch Receipts
**Status:** CANONICAL — Accepted (v1 doctrine)
**Date:** 2026-06-24
**Part of:** AFI Settlement v1 — see [AFI_SETTLEMENT_V1_DOCTRINE.md](../specs/AFI_SETTLEMENT_V1_DOCTRINE.md)

---

## Status

**Accepted — 2026-06-24.**

This ADR records the locked v1 decision for **Locked Decision D3** in the constitution ([AFI_SETTLEMENT_V1_DOCTRINE.md](../specs/AFI_SETTLEMENT_V1_DOCTRINE.md) §4): *Strategy/epoch reputation receipts use **ERC-6909** (not ERC-1155) for v1, soulbound by default, and are **NOT** a payout instrument.*

This is **doctrine/design only**. Nothing in this ADR is implemented, deployed, or executed. It defines the standard, the soulbound posture, and the non-payout law for the Layer-2 receipt; the elaborating spec is [AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md](../specs/AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md). Exact field encodings and the on-chain interface are implementation design and are marked OPEN where noted below.

---

## Context

### The v0 reality being corrected

The v0 commitment plane is three Foundry/OpenZeppelin contracts in `afi-token/src`. The relevant v0 facts this ADR corrects are:

- **Per-signal mint, not epoch-batched.** `AFIMintCoordinator.mintForSignal(MintRequest)` is gated on `EMISSIONS_ROLE` and, in a **single call**, both records provenance (emits `MintCoordinated`) and pays the reward (`AFIToken.mintEmissions(req.beneficiary, req.tokenAmount)`). One signal → one mint → one wallet. This conflates *provenance* with *payout* and is deprecated as the mainnet flow (constitution §5, §8; ADR-001).
- **ERC-1155 receipt.** `AFISignalReceipt` is an `ERC1155 + AccessControl` contract whose `mintReceipt(to, id, amount, data)` mints an **opaque** receipt: `id` is an opaque `uint256`, `data` is a pass-through blob (the reference path supplies `0x`). It has a **placeholder URI** and **no canonical per-receipt provenance metadata schema**. The receipt is therefore neither independently meaningful nor independently verifiable from chain state.
- **Per-signal payload shape.** The receipt is parameterized **per signal** (`receiptId`, `receiptAmount`, `extraData` in the calldata `MintRequest`) and is minted alongside, and in lockstep with, a token payout to a single `beneficiary`. The receipt thus reads as an artifact of *the same event that paid the reward* — exactly the provenance/payout conflation v1 forbids.
- **Storage-less provenance.** `signalId`, `epochId`, `extraData`, and per-signal amounts live **only in event logs**, not in contract storage. The receipt `id` is opaque, so there is no on-chain object that aggregates a strategy's reputation for an epoch.
- **1-of-1 Safe.** Admin + emissions authority over this flow has sat under a single 1-of-1 Safe — not production-grade (constitution §12). This is governance context, not a receipt-standard fact, but it is part of *why* v0 must not be promoted as canonical.
- **Legacy ENS alias stale pointer.** The v0 governance/Snapshot pointer used a legacy (non-canonical) three-letter ENS alias that is **stale/incorrect**; the live AFI DAO governance space is `afidao.eth` (network 1) (constitution §11). No receipt, v0 or v1, may treat ENS as authority for access control or routing (constitution §11, ADR-005).

### What Layer 2 actually needs

The four-layer model (constitution §3) places **Strategy/Epoch Reputation** at **Layer 2**, strictly between per-signal provenance (Layer 1) and the settlement manifest (Layer 3). Layer 2 needs an on-chain object that:

1. Represents **aggregate reputation per `(strategyId, epochId)`** — *one* receipt per strategy per epoch, not one per signal.
2. Is **soulbound** — reputation is an attribute of a strategy/subject, not a transferable bearer asset.
3. **Carries no token claim** — it is not redeemable, not an IOU, not the unit of payout (constitution §8, L-SEP-2).
4. **Links to the proof and money layers by reference** — it references `signalRoot`, `evidenceRoot`, `strategyRoot`, and the `EpochSettlementManifest` (by `epochId` + manifest root), so it is independently locatable and verifiable.
5. Is **cheap to mint at epoch cadence** and avoids the per-id ERC-1155 metadata/URI baggage that v0 left as a placeholder.

The constitution **already locks the answer** (D3, §15.2): ERC-6909, soulbound by default. This ADR documents the rationale and the consequences; it does not re-open the choice.

### Why ERC-6909 over ERC-1155 (and over ERC-20/721/SBT one-offs)

ERC-6909 is a minimal multi-token standard: an `(owner, id) → balance` accounting model with a small, transfer/approval-centric interface and **no mandated metadata/URI or batch-callback surface**. For an epoch-cadence reputation object keyed by a derived `receiptId`, that minimalism is the point:

- **Per-id reputation without per-id metadata law.** ERC-6909's id space lets `receiptId = hash(strategyId, epochId)` index a reputation magnitude directly, without ERC-1155's `uri(id)` expectations or the opaque-`id` + placeholder-URI mess of v0.
- **No transfer-hook / batch-callback surface to neutralize.** ERC-1155's `safeTransferFrom`/`onERC1155Received` receiver-callback machinery exists to move tokens safely between holders — irrelevant and undesirable for a soulbound, non-transferable reputation marker. ERC-6909's leaner surface is easier to lock down to soulbound semantics.
- **Cheaper, simpler accounting** at epoch cadence than a bespoke ERC-721 SBT per receipt, while still giving a distinct `id` per `(strategyId, epochId)`.

This decision is also consistent across the doctrine set: ADR-001 separates provenance from payout and batches by epoch; this ADR makes Layer 2's on-chain object honor that separation by construction.

---

## Decision

**D-002.1 (MUST) — Standard.** v1 strategy/epoch reputation receipts **MUST** use **ERC-6909**. ERC-1155 **MUST NOT** be introduced as the v1 receipt standard. (Constitution D3, §15.2.)

**D-002.2 (MUST) — One receipt per `(strategyId, epochId)`.** There **MUST** be exactly one Layer-2 receipt per `(strategyId, epochId)`, identified by a deterministic `receiptId = hash(strategyId, epochId)`. Receipts **MUST NOT** be minted per signal. (The per-signal v0 `mintForSignal`/`AFISignalReceipt` shape is deprecated — constitution §5.)

**D-002.3 (MUST) — Soulbound by default.** Layer-2 receipts **MUST** be **non-transferable (soulbound) by default**. The contract **MUST NOT** expose, and **MUST** disable, the transfer/approval semantics that would let a receipt move between owners under normal operation. Any future transferability exception is an owner/governance decision (see Open questions) and **MUST NOT** be assumed.

**D-002.4 (MUST) — Not a payout instrument.** A Layer-2 receipt **MUST NOT** be a transferable claim on tokens, **MUST NOT** be redeemable for tokens, and **MUST NOT** be used as the unit of payout. (Constitution L-SEP-2 §3, §8; D2.) The receipt's `balance|score` field carries **reputation magnitude semantics — NOT a token claim** (constitution §15.2). Reward entitlement is established **only** by inclusion in a committed `EpochSettlementManifest` `claimRoot` (Layer 3) and realized **only** through the RewardsVault/claim layer (Layer 4).

**D-002.5 (MUST) — Provenance, not reward.** Minting or updating a Layer-2 receipt **MUST NOT** mint, transfer, or escrow any reward token. Recording reputation and paying a reward are **separate transactions, separate artifacts, and separate trust assumptions** (constitution L-SEP-1 §3). This explicitly closes the v0 contradiction in which a single `mintForSignal` call emitted both a provenance receipt and the reward (constitution §8).

**D-002.6 (MUST) — Canonical fields (presence + meaning; encodings OPEN).** Per the constitution's field registry (§15.2), a Layer-2 receipt **MUST** carry, at minimum, the following fields. Field **presence and meaning are doctrine**; exact types/encodings are implementation design.

| Field | Meaning | Normative |
|---|---|---|
| `receiptId` | `hash(strategyId, epochId)` — deterministic derivation; one per strategy per epoch. | MUST |
| `owner` | Strategy controller / reputation subject. **MUST NOT** be resolved via ENS for authority (constitution §11). | MUST |
| `balance \| score` | Reputation magnitude semantics. **NOT** a token claim, **NOT** redeemable. | MUST |
| `finalized` | Flag indicating the receipt is sealed at epoch finalization. | MUST |
| Linkage refs | References to `signalRoot`, `evidenceRoot`, `strategyRoot`, and the `EpochSettlementManifest` (by `epochId` + manifest root). | MUST |

**D-002.7 (SHOULD) — Immutability after finalization.** Receipts **SHOULD** be immutable after epoch finalization (`finalized = true`). Whether any post-finalization update path exists is **OPEN/owner-decided** (constitution §15.2); a contract **MUST NOT** ship an arbitrary post-finalization mutate path asserted as final policy.

**D-002.8 (MUST) — Addresses are truth.** Any contract implementing this receipt **MUST NOT** resolve ENS dynamically for access control, ownership, or routing; concrete address + chainId are authoritative (constitution §11, D7, ADR-005).

**D-002.9 (MUST) — Agent boundary.** Agents **MAY** compute reputation magnitudes and **submit** the inputs that drive receipt issuance under scoped, least-privilege permissions, but **MUST NEVER** control the minting authority, hold production keys, or hold Safe roles for the receipt contract (constitution §13, D10, ADR-001/ADR-005). Receipt issuance for an epoch **MUST** follow the same human/governance authorization that gates the epoch's settlement (constitution §13).

---

## Consequences

### Positive

- **Layer separation enforced by construction.** Because the receipt is soulbound and carries no claim, it is structurally impossible to use it as a payout instrument — directly satisfying L-SEP-2 and closing the v0 `mintForSignal` conflation.
- **Independently locatable reputation.** A deterministic `receiptId = hash(strategyId, epochId)` plus the linkage refs make a strategy's per-epoch reputation a first-class on-chain object that ties back to Layer-1 roots and the Layer-3 manifest — unlike v0's opaque ERC-1155 `id` and placeholder URI.
- **Cheaper, leaner standard.** No ERC-1155 receiver-callback / batch-transfer / URI surface to implement, audit, or neutralize for a non-transferable object.
- **Doctrine-consistent.** Aligns with ADR-001 (epoch-batched, provenance ≠ payout), ADR-004 (vault/manifest pays the money), and ADR-005 (addresses are truth).

### Negative / costs

- **New contract surface.** v1 introduces an ERC-6909 receipt contract distinct from v0's `AFISignalReceipt`; it is **not** a migration of v0 receipt state (constitution §14 — flawed testnet state MUST NOT be migrated). Net-new design, implementation, and audit work.
- **Soulbound enforcement is a hard requirement, not a default to skip.** "Soulbound by default" on a standard built around transfer/approval semantics requires deliberate disabling of those paths; getting this wrong would silently violate L-SEP-2.
- **Tooling/wallet support.** ERC-6909 is less widely supported by wallets/indexers than ERC-1155; surfacing reputation to humans relies on AFI tooling rather than generic NFT viewers. Acceptable because the receipt is soulbound and not user-tradable.
- **Coordination with the manifest.** Linkage to the `EpochSettlementManifest` (manifest root) means receipt finalization and manifest commitment must be sequenced coherently per epoch; this is a process obligation on Layer 3 (constitution §9).

### Things this ADR does NOT decide (left to other layers/ADRs)

- It does **not** define reward amounts, role splits, holdback, or unclaimed-reward policy — those live in the manifest (Layer 3) and vault (Layer 4) and are OPEN where the constitution says OPEN (O2–O4).
- It does **not** define the EAS/Merkle leaf schema (Layer 1 / ADR / spec; O6 OPEN).

---

## Alternatives considered

| Alternative | Why rejected |
|---|---|
| **Keep ERC-1155 (`AFISignalReceipt`) as the v1 receipt** | Deprecated by constitution D3/§5. The v0 receipt is per-signal, opaque (`id` is an opaque `uint256`, placeholder URI, no provenance schema), and minted in lockstep with the reward payout — it embodies the provenance/payout conflation v1 forbids. Its receiver-callback/batch/URI surface is dead weight for a soulbound, non-transferable object. **It MAY be retained only as a historical/prototype artifact** (constitution §5, §14), never as the Layer-2 reputation receipt. |
| **ERC-20 per strategy/epoch** | Fungible balances are a transferable bearer claim by default — the opposite of soulbound, non-payout reputation. Would re-introduce exactly the "receipt as money" risk. No native per-`(strategyId, epochId)` id space. |
| **ERC-721 soulbound (one SBT per receipt)** | Workable for non-transferability, but heavier per-token (metadata/URI, one contract-call shape per mint) and gives no native multi-id accounting; more gas and surface than ERC-6909 for an epoch-cadence object. |
| **Bespoke non-standard reputation mapping (no token standard)** | Loses interoperability with indexers/tooling and the shared mental model; reinvents id/accounting semantics ERC-6909 already provides minimally. |
| **Make the receipt itself redeemable / a claim** | Directly violates L-SEP-2 and §8 (provenance artifacts MUST NOT be redeemable for tokens). The whole point of v1 is that the **manifest** (Layer 3) and **vault** (Layer 4) — not a provenance receipt — decide and pay rewards. |
| **ERC-7802 / SuperchainERC20-flavored receipt** | ERC-7802 is explicitly **deferred** for v1 (constitution D5, §10, ADR-003) and MUST NOT be a v1 dependency. |

---

## Open questions

These are **OPEN** (constitution §1, §6). They **MUST NOT** be implemented as final until resolved by the owner.

- **OQ-002.1 — Post-finalization updatability.** Whether a `finalized` receipt may ever be updated (e.g. correction, slashing of reputation, re-scoring) and under what authority. Constitution §15.2 marks updates OPEN/owner-decided. Default doctrine is **immutable after finalization** (D-002.7); any mutate path is a separate owner decision.
- **OQ-002.2 — Soulbound exceptions.** Whether any narrow transfer path (e.g. owner-key rotation / subject-controlled migration) is ever permitted, and how it would be authorized without re-opening transferability. Default is **fully soulbound** (D-002.3).
- **OQ-002.3 — `balance|score` encoding.** Exact type/scale/precision of the reputation magnitude and its derivation from `strategyRoot` / scoring. Implementation design; **MUST NOT** be frozen as final here, and **MUST NOT** be read as a token amount.
- **OQ-002.4 — Exact ERC-6909 interface profile.** Which ERC-6909 functions/events are exposed vs. disabled to enforce soulbound semantics, and the precise on-chain anchor contract. Implementation design; consistent with the EAS-schema "direction locked, details OPEN" posture (O6).
- **OQ-002.5 — Receipt ↔ manifest sequencing.** The exact ordering/coupling between receipt finalization and `EpochSettlementManifest` commitment per epoch. Constrained by constitution §9 (manifest committed once per epoch) but the operational sequence is owner/process design.

---

## Related docs

**Constitution:**
- [AFI_SETTLEMENT_V1_DOCTRINE.md](../specs/AFI_SETTLEMENT_V1_DOCTRINE.md) — v1 doctrine baseline; D2, D3, L-SEP-1/L-SEP-2, §8, §15.2.

**Specs (this set):**
- [AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md](../specs/AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md) — Layer 2, the spec this ADR governs.
- [AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md](../specs/AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md) — Layer 1; source of `signalRoot` / `evidenceRoot` / `strategyRoot` linkage.
- [AFI_EPOCH_SETTLEMENT_MANIFEST.md](../specs/AFI_EPOCH_SETTLEMENT_MANIFEST.md) — Layer 3; the manifest the receipt links to and which (not the receipt) decides rewards.
- [AFI_REWARDS_VAULT_AND_CLAIMS.md](../specs/AFI_REWARDS_VAULT_AND_CLAIMS.md) — Layer 4; where money is actually paid.
- [AFI_ENS_SAFE_ADDRESS_REGISTRY_DOCTRINE.md](../specs/AFI_ENS_SAFE_ADDRESS_REGISTRY_DOCTRINE.md) — addresses-are-truth; ENS aliases only.
- [AFI_V0_DEPRECATION_AND_MIGRATION.md](../specs/AFI_V0_DEPRECATION_AND_MIGRATION.md) — v0 (`mintForSignal`, `AFISignalReceipt`) deprecation posture.

**Sibling ADRs:**
- [ADR-001](./ADR-001-four-layer-settlement-architecture.md) — epoch settlement; provenance ≠ payout (the law this receipt honors).
- [ADR-003](./ADR-003-xerc20-retained-erc7802-deferred.md) — xERC20 retained, ERC-7802 deferred (why no ERC-7802 receipt).
- [ADR-004](./ADR-004-rewards-vault-merkle-claims.md) — RewardsVault + manifest-backed claims (where rewards are decided/paid, not here).
- [ADR-005](./ADR-005-ens-aliases-addresses-source-of-truth.md) — ENS aliases vs. concrete-address source of truth.
- [ADR-006](./ADR-006-unclaimed-rewards-legal-clawback-open.md) — legal clawback/escheatment OPEN.
