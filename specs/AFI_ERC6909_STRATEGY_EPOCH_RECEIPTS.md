# AFI ERC-6909 Strategy/Epoch Receipts
**Status:** CANONICAL — Accepted (v1 doctrine)
**Date:** 2026-06-24
**Part of:** AFI Settlement v1 — see [AFI_SETTLEMENT_V1_DOCTRINE.md](./AFI_SETTLEMENT_V1_DOCTRINE.md)

> This document specifies **Layer 2** of the four-layer model (see doctrine §3). It is **doctrine/design only**. It implements nothing on-chain: it deploys no contract, mints no receipt, grants no role, and moves no funds. Where this spec and the constitution conflict on a v1 architecture question, the **constitution wins** ([AFI_SETTLEMENT_V1_DOCTRINE.md](./AFI_SETTLEMENT_V1_DOCTRINE.md) §15.2, §4/D3, §8). Field names are reused verbatim from the constitution's Canonical Artifacts & Field Registry (§15).

---

## 1. Normative Language

This spec uses **MUST / MUST NOT / SHOULD / SHOULD NOT / MAY / OPEN** exactly as defined in [AFI_SETTLEMENT_V1_DOCTRINE.md](./AFI_SETTLEMENT_V1_DOCTRINE.md) §1. In particular, **OPEN** means a decision is deliberately not settled, MUST NOT be implemented as if final, and MUST be resolved by the owner before implementation.

---

## 2. Scope and Position in the Four-Layer Model

This spec defines the **strategy/epoch reputation receipt** — Layer 2 of AFI Settlement v1.

| Layer | Artifact | This spec? |
|-------|----------|-----------|
| Layer 1 — Per-signal provenance | `signalRoot` / `evidenceRoot` leaves (EAS-backed Merkle batch root) | No — see [AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md](./AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md) |
| **Layer 2 — Strategy/epoch reputation** | **One ERC-6909 receipt per `(strategyId, epochId)`** | **Yes** |
| Layer 3 — Epoch settlement manifest | `EpochSettlementManifest` (the only payout authority) | No — see [AFI_EPOCH_SETTLEMENT_MANIFEST.md](./AFI_EPOCH_SETTLEMENT_MANIFEST.md) |
| Layer 4 — Vault custody / claims | `RewardsVault` + manifest-backed claim/route | No — see [AFI_REWARDS_VAULT_AND_CLAIMS.md](./AFI_REWARDS_VAULT_AND_CLAIMS.md) |

A Layer-2 receipt is a **durable, on-chain record of a strategy's aggregate reputation for a single epoch**. It exists so that reputation has a canonical, queryable, soulbound anchor that is **structurally separate** from money. It is **not** an entry in the payout path.

**This receipt is downstream of provenance (Layer 1) and strictly upstream-and-independent of payout (Layers 3–4).** Reputation MAY *inform* the off-chain ruleset that produces the manifest, but the receipt itself is never the unit of payout and is never consulted by a vault to release funds (see §10, §11).

---

## 3. Owner Decision: ERC-6909, NOT ERC-1155 (D3, ADR-002)

This is **locked v1 law** (doctrine §4/D3, ADR-002):

- **MUST:** v1 strategy/epoch reputation receipts **MUST be ERC-6909**.
- **MUST NOT:** ERC-1155 **MUST NOT** be introduced as the v1 receipt standard.

### 3.1 `AFISignalReceipt` (ERC-1155) is prototype/historical only

The existing `AFISignalReceipt` contract (`afi-token/src/AFISignalReceipt.sol`) is an **ERC-1155** mintable by `MINT_COORDINATOR_ROLE`, wired to the v0 `AFIMintCoordinator.mintForSignal` flow. Under v1 doctrine (§5, §14, ADR-001):

- `AFISignalReceipt` (ERC-1155) is a **v0 prototype / historical artifact only**. It MAY be retained, clearly labelled, but MUST NOT be taught as canonical.
- It is **NOT** the Layer-2 reputation receipt specified here.
- It is **NOT** a payout instrument and MUST NOT be presented as one.
- It MUST NOT be migrated, renamed, or "upgraded" into the Layer-2 receipt. The Layer-2 receipt is a **new, separately specified** ERC-6909 artifact.

### 3.2 Why ERC-6909 over ERC-1155 (rationale, non-normative)

ERC-6909 is the owner-selected minimal multi-token standard. Reasons it fits Layer 2:

- **Per-`id` accounting without batch/callback surface.** ERC-6909 drops ERC-1155's batch-transfer and `onERC1155Received` acceptance-hook machinery. A reputation receipt needs `id → owner → balance`, not transfer batching or receiver hooks. Less surface = fewer ways for a "receipt" to behave like a transferable financial instrument.
- **Cleaner soulbound posture.** Non-transferability is enforced by overriding a small, well-defined transfer surface (`transfer`, `transferFrom`, `approve`, `setOperator`) rather than ERC-1155's broader transfer/approval/batch API (see §5).
- **Disambiguation from the deprecated artifact.** Choosing a different standard from the v0 ERC-1155 receipt makes the architectural break explicit at the type level: a v1 reputation receipt can never be mistaken for the v0 ERC-1155 signal receipt.

> **Design note (not a hard requirement):** The exact contract name, `id` type width, and event set are **implementation design**. This spec commits to the **standard (ERC-6909)**, the **`receiptId` semantics**, the **soulbound default**, the **score semantics**, and the **prohibitions**. Encoding-level specifics are left to implementation and MUST NOT contradict this spec or §15.2.

---

## 4. `receiptId` Derivation

Per constitution §15.2, the receipt identifier is a **deterministic derivation** from the strategy and epoch.

- **MUST:** `receiptId = hash(strategyId, epochId)`.
- **MUST:** The derivation MUST be deterministic and collision-resistant: the same `(strategyId, epochId)` pair MUST always map to the same `receiptId`, and distinct pairs MUST NOT (within cryptographic assumptions) collide.
- **MUST:** Exactly **one** receipt `id` exists per `(strategyId, epochId)` pair. There is no per-signal receipt and no per-wallet receipt at Layer 2.
- **MUST:** `receiptId` MUST be reproducible **off-chain** from the published `strategyId` and `epochId` so that any verifier can locate and check a receipt without trusting AFI infrastructure.

**OPEN (implementation design):** the exact hash function (e.g. `keccak256(abi.encode(strategyId, epochId))` vs. a domain-separated hash), the encoding/widths of `strategyId` and `epochId`, and any domain-separation tag are **implementation design**. They MUST satisfy the determinism/collision properties above and MUST be documented at implementation time. Field PRESENCE and MEANING are doctrine; value-level encoding is not frozen here.

---

## 5. Non-Transferability / Soulbound Posture

### 5.1 Default: soulbound (MUST)

- **MUST:** Layer-2 receipts are **soulbound by default** (doctrine §3 Layer-2 box, §15.2, §4/D3).
- **MUST NOT:** A soulbound receipt MUST NOT be transferable between accounts. Reputation is bound to its subject; it is not a bearer object and not a market good.
- **MUST:** The transfer-bearing surface of the ERC-6909 interface MUST be neutralized for soulbound receipts. Concretely, the following MUST revert (or be made permanently no-op such that no value/ownership can move): `transfer`, `transferFrom`, and the approval surface (`approve`, `setOperator`) insofar as it would enable a third party to move a receipt.
- **MUST:** Issuance and revocation occur only through controlled, authorized issuance paths (mint/burn-equivalent under owner-/governance-scoped authority), **not** through holder-initiated transfers.

### 5.2 Justification for the soulbound default

- **Reputation is non-fungible to a subject.** A strategy's epoch reputation describes *that strategy in that epoch*. Transferring it would let one actor wear another's track record — defeating provenance.
- **Anti-financialization.** A transferable "reputation token" trends toward a tradable claim. Doctrine **L-SEP-2** forbids Layer-2 receipts from being transferable claims on tokens. Soulbinding closes the easiest path by which a receipt could become a de-facto IOU or speculative instrument.
- **Sybil/wash resistance.** Non-transferability prevents reputation from being pooled, sold, or laundered across identities to manufacture standing.

### 5.3 Status of transferability beyond the default

- The **default is soulbound and that default is locked** (§15.2: "soulbound by default"). Any *non-soulbound* posture for a specific receipt class would be a **deviation** and, under §1, requires a **documented, owner-approved reason** (SHOULD-strength deviation control). It MUST NOT be assumed.
- Even if a future owner decision permitted any controlled transfer/delegation of a receipt, that transfer **MUST NOT** make the receipt redeemable for tokens or a claim on a vault (the §11 prohibitions are absolute and survive any transferability change).

---

## 6. Receipt Owner

Per constitution §15.2, the receipt has an `owner` defined as the **strategy controller / reputation subject**.

- **MUST:** Each receipt has exactly one `owner`, which is the **reputation subject** for `(strategyId, epochId)` — i.e., the strategy controller account, as resolved by the address-source-of-truth registry, **not** an ENS name (doctrine §11, §15.5; [AFI_ENS_SAFE_ADDRESS_REGISTRY_DOCTRINE.md](./AFI_ENS_SAFE_ADDRESS_REGISTRY_DOCTRINE.md)).
- **MUST NOT:** The receipt owner MUST NOT be treated as a "beneficiary" in any payout sense. Ownership of a reputation receipt confers **no entitlement to funds** (see §10, §11). Payout entitlement is established **only** by inclusion in a committed `EpochSettlementManifest` `claimRoot` (doctrine §8).
- **MUST NOT:** Contracts MUST NOT resolve ENS to determine the owner (doctrine §7/D7). The concrete address + `chainId` is authoritative.
- **OPEN (owner):** Whether the `owner` is the strategy's operating account, a delegated reputation account, or a registry-mapped identity is an **owner decision** to be fixed against the concrete-address registry. The **presence and meaning** of `owner` (= reputation subject) is doctrine; the **binding rule** to a concrete account is owner-deferred.

---

## 7. Score / Balance Semantics — Reputation Magnitude, NOT a Token Claim

Per constitution §15.2, the receipt carries a `balance|score` field whose meaning is **"reputation magnitude semantics — NOT a token claim."** This is the most-abused field in any reputation system, so it is constrained hard.

- **MUST:** The receipt's `balance | score` is a **reputation magnitude** for `(strategyId, epochId)`: a scalar standing/quality measure derived from the epoch's qualified-signal provenance and the committed `rulesetHash`.
- **MUST NOT:** The `balance | score` is **NOT** a token amount, **NOT** an entitlement, **NOT** an IOU, and **NOT** a claim on the `RewardsVault` or treasury. A receipt balance of *N* does **not** mean *N* tokens, *N* shares, or *N* of anything redeemable.
- **MUST NOT:** No contract MAY read a Layer-2 receipt balance/score and pay, mint, or release tokens on that basis. Payout authority is the manifest `claimRoot` alone (doctrine §8, L-SEP-3).
- **MUST:** Because ERC-6909 names the per-`id` quantity `balanceOf(owner, id)`, the implementation MUST make the **non-financial meaning explicit** (documentation, naming, and ideally metadata), so the standard's `balance` vocabulary is never mistaken for a fungible token balance. The recommended canonical term in docs and metadata is **`score`** (reputation magnitude); `balance` is the ERC-6909 storage primitive carrying that score.
- **SHOULD:** The score SHOULD be reproducible: given the published `rulesetHash` and the post-disclosure Layer-1 evidence, an independent party SHOULD be able to recompute the reputation magnitude and check it against the on-chain receipt.

**OPEN (implementation design / owner):** the score's **range, decimals/precision, units, decay, and aggregation formula** are NOT settled here. These are governed by AFI's off-chain scoring ruleset (`rulesetHash`) and are **implementation/owner design**. This spec freezes only that the field *exists* and *means reputation magnitude, never a token claim*. Tokenomics splits and economic weighting remain OPEN (doctrine O3) and MUST NOT be inferred from receipt scores.

---

## 8. Metadata Fields

Each receipt commits to a small, audit-grade metadata set. These bind the receipt to the provenance and settlement record **without** putting raw signals on-chain (doctrine §7).

| Field | Source / §15 name | Meaning | Normative |
|-------|-------------------|---------|-----------|
| `receiptId` | §15.2 | `hash(strategyId, epochId)` — the ERC-6909 `id`. | MUST |
| `strategyId` | §15.1/§15.2 | The strategy this reputation belongs to. | MUST |
| `epochId` | §15.1/§15.2 | The epoch this reputation is scoped to. | MUST |
| `owner` | §15.2 | Strategy controller / reputation subject (concrete address; see §6). | MUST |
| `balance` \| `score` | §15.2 | Reputation magnitude — NOT a token claim (see §7). | MUST |
| `finalized` | §15.2 | Flag: epoch reputation has been finalized (see §9). | MUST |
| `signalRoot` | §15.1/§15.2 | Linkage to Layer-1 signal provenance root (see §9). | MUST |
| `evidenceRoot` | §15.1/§15.2 | Linkage to Layer-1 evidence root (see §9). | MUST |
| `strategyRoot` | §15.2/§15.3 | Linkage to the strategy-aggregation root (see §9). | MUST |
| `rulesetHash` | §15.1/§15.3 | The scoring ruleset under which the score was computed. | MUST |
| `manifestURI` / manifest root ref | §15.2/§15.3 | Reference to the `EpochSettlementManifest` for this epoch (by `epochId` + manifest root) (see §9). | MUST |
| `disclosureStatus` | §15.1 | Delayed-disclosure state of the underlying evidence (raw stays off-chain until window elapses, doctrine §7). | SHOULD |

- **MUST NOT:** Metadata MUST NOT include raw per-signal arrays, raw scores, or evidence blobs on-chain (doctrine §7). Only **commitments / roots / hashes / pointers** are recorded.
- **MUST:** Where a field also appears in a sibling artifact (e.g. `signalRoot`, `evidenceRoot`, `strategyRoot`, `rulesetHash`), the receipt MUST reference the **same value** committed by Layer 1 / the manifest; it MUST NOT recompute or restate a divergent value.
- **OPEN (implementation design):** whether metadata is stored as on-chain struct fields, an `IERC6909ContentURI`-style `tokenURI` document, or a hybrid, and the exact off-chain metadata schema, are **implementation design** consistent with §15.2 and doctrine §7. The **field set above is doctrine.**

---

## 9. Relationship to `signalRoot`, `evidenceRoot`, `strategyRoot`, `claimRoot`, and the `EpochSettlementManifest`

The receipt is a **reputation anchor that points at the proof chain**, while remaining outside the money chain.

```
Layer 1                          Layer 2                      Layer 3                Layer 4
signalRoot ───┐                                                                          
evidenceRoot ─┼──► strategyRoot ──► ERC-6909 receipt ····(informs ruleset, off-chain)···► EpochSettlementManifest ──► RewardsVault
              │     (aggregation)    (this spec)                                          claimRoot = payout authority   (pays vs claimRoot)
rulesetHash ──┘
```

| Root / artifact | §15 name | Relationship to the receipt | Normative |
|-----------------|----------|-----------------------------|-----------|
| `signalRoot` | §15.1/§15.2 | Layer-1 commitment over the epoch's qualified signal leaves. The receipt **references** it as the provenance basis for the score. | MUST reference; MUST NOT recompute |
| `evidenceRoot` | §15.1/§15.2 | Layer-1 commitment over signal-lifecycle evidence leaves. The receipt **references** it. | MUST reference; MUST NOT recompute |
| `strategyRoot` | §15.2/§15.3 | The strategy-aggregation root binding a strategy's qualified set for the epoch. The receipt's score is an aggregate **consistent with** `strategyRoot`. | MUST reference |
| `rulesetHash` | §15.1/§15.3 | The committed scoring ruleset. The receipt's score MUST be attributable to **this** `rulesetHash`. | MUST reference |
| `claimRoot` | §15.3 | The **payout authority** in the manifest. The receipt MUST **NOT** be derived from, gate, or substitute for `claimRoot`, and `claimRoot` MUST NOT be derived from receipt balances. | MUST NOT couple to payout |
| `EpochSettlementManifest` | §15.3 | The receipt **references** the manifest for its epoch (by `epochId` + manifest root) for traceability. The manifest, **not** the receipt, decides who is owed what (L-SEP-3). | MUST reference; MUST NOT be the payout unit |

**Laws:**

- **MUST:** The receipt MUST reference `signalRoot`, `evidenceRoot`, `strategyRoot`, `rulesetHash`, and the `EpochSettlementManifest` (by `epochId` + manifest root), so reputation is traceable to its provenance and to the epoch's settlement record (constitution §15.2).
- **MUST NOT:** The receipt MUST NOT be coupled to `claimRoot` as a payout mechanism. Reputation MAY *inform* the off-chain ruleset that produces the manifest, but the **manifest `claimRoot` is the sole on-chain payout authority** (doctrine §8, L-SEP-3). No on-chain code path may turn a receipt into a claim against `claimRoot`.
- **MUST NOT:** No contract downstream of the manifest may recompute eligibility or scores from receipts (doctrine L-SEP-3). The receipt is a *record*, not an *oracle* for the vault.

---

## 10. Immutability After Finalization

- **SHOULD:** Receipts **SHOULD be immutable after epoch finalization** (constitution §15.2). Once an epoch's reputation is finalized (`finalized = true`, bound to the committed `EpochSettlementManifest` and its roots), the receipt's `score`, roots, and linkage SHOULD NOT change.
- **MUST:** The `finalized` flag MUST faithfully reflect whether the epoch's reputation is closed. A finalized receipt MUST NOT silently mutate; any post-finalization correction MUST be explicit, authorized, and auditable (e.g. a new epoch's receipt or an explicitly recorded, owner-/governance-approved correction event) — never an in-place rewrite that breaks the prior committed record.
- **MUST NOT:** Finalization MUST NOT be reachable by an agent or by any holder-initiated action. It is an authorized issuance/settlement operation under owner-/governance-scoped authority (doctrine §12, §13).
- **OPEN (owner):** The **update policy before finalization** and the **mechanics of any permitted post-finalization correction** (whether allowed at all, who may authorize, append-only vs. supersede-by-new-receipt, challenge-window interaction) are **OPEN / owner-decided** (constitution §15.2: "updates OPEN/owner-decided"). They MUST NOT be implemented as final policy without an owner decision. This spec locks only that the **default-and-recommendation is immutability after finalization** and that any deviation is owner-governed and auditable.

---

## 11. What the Layer-2 Receipt Contract MUST NEVER Do

These prohibitions are **absolute** and derive directly from doctrine §3 (L-SEP-2), §8, and §15.2. They survive any future change to transferability, scoring, or update policy.

- **MUST NOT — Be redeemable for tokens.** A receipt (or its balance/score) MUST NOT be redeemable, burnable-for-value, or exchangeable for AFI tokens, any other token, or treasury funds (doctrine §8, §15.2).
- **MUST NOT — Be a transferable claim.** A receipt MUST NOT be a transferable claim on tokens and MUST NOT be tradable, collateralizable, or assignable as a financial instrument (doctrine L-SEP-2, §15.2). It is soulbound by default (§5).
- **MUST NOT — Decide or trigger payouts.** The receipt contract MUST NOT mint, transfer, escrow, route, or release any reward token, and MUST NOT be read by any vault/claim contract to decide eligibility or amounts. Payout authority is the manifest `claimRoot` via Layers 3–4 only (doctrine L-SEP-2, L-SEP-3, L-SEP-4).
- **MUST NOT — Be the unit of payout.** Receipt balances/scores MUST NOT be used as the unit, weight, or denominator of any on-chain distribution (doctrine L-SEP-2). Any reputation→reward weighting happens **off-chain** in the ruleset that produces the manifest, and is then frozen into `claimRoot` (whose splits remain OPEN, doctrine O3).
- **MUST NOT — Move funds on provenance/issuance.** Issuing, finalizing, or updating a receipt MUST NOT mint, transfer, or escrow any reward token (doctrine L-SEP-1). Recording reputation is a provenance act, not a payment.
- **MUST NOT — Resolve ENS for authorization or routing.** The contract MUST NOT resolve ENS to determine owner, issuer authority, or any address (doctrine §11/D7). Concrete address + `chainId` is authoritative.
- **MUST NOT — Be controlled by agents over privileged operations.** Agents MUST NOT hold issuance/finalization authority, production keys, upgrade rights, or Safe roles for this contract (doctrine §13/D10). Agents MAY compute reputation off-chain and submit it for authorized issuance; they MUST NOT self-issue or self-finalize.

---

## 12. Conformance Checklist

A Layer-2 receipt design **conforms** to AFI Settlement v1 iff all of the following hold (and it does not otherwise contradict the constitution §4, §7–§13, §15):

- [ ] Standard is **ERC-6909**; ERC-1155 is **not** used for the v1 receipt (§3, D3).
- [ ] `AFISignalReceipt` (ERC-1155) is treated as prototype/historical only and is **not** the Layer-2 receipt (§3.1).
- [ ] `receiptId = hash(strategyId, epochId)`, deterministic and off-chain-reproducible (§4).
- [ ] Receipts are **soulbound by default**; transfer/approval surface is neutralized (§5).
- [ ] `owner` = strategy controller / reputation subject, bound to a concrete address (not ENS); confers no payout entitlement (§6).
- [ ] `balance | score` = reputation magnitude, explicitly **NOT** a token claim; no contract pays on it (§7).
- [ ] Metadata is commitments/roots/pointers only; **no raw signal arrays on-chain** (§8).
- [ ] References `signalRoot`, `evidenceRoot`, `strategyRoot`, `rulesetHash`, and the `EpochSettlementManifest`; is **decoupled** from `claimRoot` as a payout path (§9).
- [ ] Immutable after finalization (SHOULD); update policy left **OPEN/owner** (§10).
- [ ] Never redeemable, never a transferable claim, never decides/triggers payouts, never the unit of payout, never moves funds on issuance (§11).

---

## 13. Open Items (this layer)

| ID | Open item | Disposition |
|----|-----------|-------------|
| L2-O1 | Exact `hash` function, domain separation, and `strategyId`/`epochId` encodings for `receiptId`. | Implementation design; properties in §4 are binding. |
| L2-O2 | Score range, precision, units, decay, and aggregation formula. | Off-chain ruleset (`rulesetHash`); owner/implementation. Splits tie to doctrine O3 (OPEN). |
| L2-O3 | Binding rule from `owner` to a concrete account (operating vs. delegated vs. registry-mapped). | Owner; resolved against the concrete-address registry (§15.5). |
| L2-O4 | Pre-finalization update policy and any permitted post-finalization correction mechanics. | OPEN/owner (doctrine §15.2); default is immutability after finalization (§10). |
| L2-O5 | Metadata storage form (on-chain struct vs. `tokenURI` document vs. hybrid) and off-chain schema. | Implementation design; field set in §8 is doctrine. |
| L2-O6 | Whether any controlled, non-tradable delegation of a receipt is ever permitted. | Owner; default soulbound (§5); §11 prohibitions are absolute regardless. |

---

## 14. Related Documents

- [AFI_SETTLEMENT_V1_DOCTRINE.md](./AFI_SETTLEMENT_V1_DOCTRINE.md) — the constitution (this spec implements its §3 Layer 2 / §15.2).
- [AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md](./AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md) — Layer 1 (`signalRoot` / `evidenceRoot` leaves) feeding this receipt.
- [AFI_EPOCH_SETTLEMENT_MANIFEST.md](./AFI_EPOCH_SETTLEMENT_MANIFEST.md) — Layer 3 (`claimRoot`, the sole payout authority).
- [AFI_REWARDS_VAULT_AND_CLAIMS.md](./AFI_REWARDS_VAULT_AND_CLAIMS.md) — Layer 4 (vault pays only against the manifest).
- [AFI_ENS_SAFE_ADDRESS_REGISTRY_DOCTRINE.md](./AFI_ENS_SAFE_ADDRESS_REGISTRY_DOCTRINE.md) — concrete-address source of truth for `owner`/authority.
- [AFI_V0_DEPRECATION_AND_MIGRATION.md](./AFI_V0_DEPRECATION_AND_MIGRATION.md) — v0 posture for `AFISignalReceipt` (ERC-1155) and `AFIMintCoordinator`.
- ADRs: [../adrs/ADR-002-erc6909-strategy-epoch-receipts.md](../adrs/ADR-002-erc6909-strategy-epoch-receipts.md) (ERC-6909 vs. ERC-1155), [../adrs/ADR-001-four-layer-settlement-architecture.md](../adrs/ADR-001-four-layer-settlement-architecture.md) (provenance ≠ payout, agent boundary).

---

*Canonical doctrine. This document defines the Layer-2 reputation receipt's architecture and law only; it implements nothing on-chain and creates no payout instrument. The v0 `AFISignalReceipt` (ERC-1155) remains a prototype/historical artifact and is not the v1 receipt.*
