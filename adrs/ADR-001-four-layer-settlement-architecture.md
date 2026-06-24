# ADR-001 — Four-Layer Settlement Architecture
**Status:** CANONICAL — Accepted (v1 doctrine)
**Date:** 2026-06-24
**Part of:** AFI Settlement v1 — see [AFI_SETTLEMENT_V1_DOCTRINE.md](../specs/AFI_SETTLEMENT_V1_DOCTRINE.md)

---

## Status

**Accepted — 2026-06-24.**

This is the foundational ADR of the AFI Settlement v1 doctrine set. It establishes the four-layer settlement architecture and the layer-separation laws that every other v1 spec and ADR depends on. It corresponds to Locked Decisions **D1, D2, D9, D10** (and partially anchors **D6**) in [AFI_SETTLEMENT_V1_DOCTRINE.md](../specs/AFI_SETTLEMENT_V1_DOCTRINE.md) §4.

This ADR is **doctrine and design only**. It does **not** deploy contracts, mint tokens, grant roles, move funds, or modify any ENS/Safe state. It defines *what the v1 architecture is* so that the repository stops teaching the v0 model as canonical.

Per the constitution's change control (§17), this decision may only be altered by a superseding ADR that marks the affected Locked Decisions as `Superseded`.

---

## Context

### The v0 reality being corrected

The deployed v0 reference stack (Base Sepolia, chain ID `84532`) **collapses provenance and payout into a single on-chain action**. The recon reports (linked under *Related docs*, and accurate as descriptions of v0 as-it-is) establish the following facts:

- **`mintForSignal` fuses provenance with payout.** The deployed coordinator (verified on-chain as `TestMintCoordinator`, selector `0xf6d6defe`) exposes `mintForSignal(MintRequest)`. In **one call**, gated by a single `EMISSIONS_ROLE`, it can mint **both** ERC-20 emissions (`AFIToken.mintEmissions(beneficiary, tokenAmount)`) **and** an ERC-1155 "receipt" (`AFISignalReceipt.mintReceipt(...)`). `tokenAmount` and `receiptAmount` are independent, but they travel in the same transaction. This means: recording that a signal happened *is* paying for it.
- **Per-signal, single-beneficiary, push-at-mint.** The `MintRequest` struct carries a single `address beneficiary` and a single `tokenAmount`. There is **no** strategy/epoch parent receipt, **no** manifest root, **no** multi-recipient role split, and **no** epoch batching. Rewards are pushed to one wallet at mint time, per signal, as validation completes — not at epoch close.
- **ERC-1155 receipt conflated as the payout/proof unit.** `AFISignalReceipt` (ERC-1155) is minted alongside the reward, so any operator or auditor reading the stack reasonably infers *receipt = reward proof = payout unit*. That inference is exactly backwards from the owner's intended model, where a receipt is **performance/provenance** and a reward is a **separate epoch settlement**.
- **1-of-1 Safe holds admin + emissions authority.** On Base Sepolia, the Treasury Safe `0x1Dd6705ff84Ecd5eaDc51A913Ad8e2c6C9E79aC4` holds `DEFAULT_ADMIN_ROLE` and `EMISSIONS_ROLE`. That Safe is **threshold 1**, signed by a **single key** (`0xb87C647a…ad62`) — the *same* sole signer that controls the L1 `afidao.eth` namespace Safes. A single key is therefore the root of trust for emissions, admin, and governance namespace alike. (Note: coordinator role-wiring is currently incomplete, so `mintForSignal` would revert today — but the *architecture*, once wired, is the per-signal push flow described above.)
- **Stale governance pointer (legacy three-letter ENS alias).** The repo references a previously-used non-canonical ENS alias as the Snapshot/governance space. This is **incorrect**: the live AFI DAO space is `afidao.eth` (network 1). That legacy three-letter alias is owned by an unrelated name and MUST NOT be treated as AFI governance.

### Why this must change

The v0 model has no clean place to express the owner's actual requirements:

1. **Provenance must be cheap, dense, and independently verifiable** for *every* qualified signal — but it must not move money.
2. **Rewards must be computed per epoch**, across **multiple roles** (Providers / Analysts-Scorers / Validators / public-goods), against a **single committed authority**, and paid through a **custodial layer** that can enforce challenge/holdback windows.
3. **Reputation** (how a strategy is performing over an epoch) is a distinct concept from both raw provenance and from any token claim, and conflating it with either is a correctness and security hazard.
4. **Agents** that score signals and assemble settlement proposals must never be the same trust boundary as the keys/roles/funds that execute payment.

A flow that mints reward and receipt together, per signal, to one wallet, under one role held by one key, cannot satisfy any of these without being torn apart. v1 therefore does not patch `mintForSignal`; it replaces the *architecture* with one in which the four concerns above are first-class, separated layers.

This ADR records the decision to do so. See [AFI_V0_DEPRECATION_AND_MIGRATION.md](../specs/AFI_V0_DEPRECATION_AND_MIGRATION.md) for the full v0 posture (D9) and the runtime-sensitive items that remain owner-deferred.

---

## Decision

**AFI Settlement v1 MUST be a four-layer architecture.** Each layer is a distinct concern, with a dedicated canonical spec, and the layers are **strictly ordered**: a later layer MUST NOT collapse into an earlier one.

| Layer | Name | Concern | Output (canonical fields per §15) | Spec |
|------:|------|---------|-----------------------------------|------|
| **1** | **Per-signal provenance** | Truth & authorship of each qualified signal, committed on-chain as a **batch root** (EAS-backed Merkle on Base), stored off-chain (TSSD evidence). **NOT** payout. | `signalRoot`, `evidenceRoot`, signal/evidence leaves (`signalId`, `contentHash`, `scoreCommitment`, `producer`, `rulesetHash`, …) | [AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md](../specs/AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md) |
| **2** | **Strategy / epoch reputation** | Aggregate, soulbound reputation per `(strategyId, epochId)`. **NOT** a payout instrument. | `receiptId = hash(strategyId, epochId)`, `owner`, `balance\|score`, `finalized`, `strategyRoot` linkage | [AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md](../specs/AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md) |
| **3** | **Epoch settlement manifest** | The single per-epoch document binding qualified set + role allocations + ruleset + distribution roots. The **bridge between proof and money**. Committed **once** per epoch. | `epochId`, `settlementVersion`, `rulesetHash`, `signalRoot`, `evidenceRoot`, `strategyRoot`, `claimRoot`, `totalRewardPool`, `roleAllocationRoots\|roleAllocationLeaves`, `manifestURI`, … | [AFI_EPOCH_SETTLEMENT_MANIFEST.md](../specs/AFI_EPOCH_SETTLEMENT_MANIFEST.md) |
| **4** | **Vault-based reward custody / routing / claiming** | Custody of the epoch budget and payment **strictly against** the committed manifest. The vault **enforces** the manifest; it does not decide rewards. | funding flow, `claimRoot` proofs, claimed bitmap/nullifier, pause/challenge/holdback, `unclaimedRewardPolicy` (placeholder; value OPEN) | [AFI_REWARDS_VAULT_AND_CLAIMS.md](../specs/AFI_REWARDS_VAULT_AND_CLAIMS.md) |

### Layer-separation laws (normative)

These mirror the constitution's L-SEP laws (§3) and are binding on every v1 artifact:

- **L-SEP-1 (MUST):** Recording provenance (Layer 1) **MUST NOT** mint, transfer, or escrow any reward token. Provenance and payout are separate transactions, separate artifacts, and separate trust assumptions. This is the **direct correction** of `mintForSignal`'s coupling.
- **L-SEP-2 (MUST):** Reputation receipts (Layer 2) **MUST NOT** be transferable claims on tokens and **MUST NOT** be the unit of payout. A receipt is reputation, not money.
- **L-SEP-3 (MUST):** The manifest (Layer 3) is the **only** authority that decides who is owed what for an epoch. No contract downstream of the manifest may recompute eligibility or scores.
- **L-SEP-4 (MUST):** The RewardsVault (Layer 4) **MUST** pay strictly against a committed manifest root and **MUST NOT** decide eligibility, mint, or pay outside that root.

### Core laws established by this ADR

- **Provenance ≠ payout (D2, MUST).** A per-signal provenance record/commitment is a statement of *truth and authorship*. It is **NOT** a reward, an IOU, or a claim. No provenance artifact — EAS attestation, signal leaf, ERC-6909 reputation receipt, or any retained v0 ERC-1155 receipt — **MUST** be redeemable for tokens. Reward entitlement is established **only** by inclusion in a committed `EpochSettlementManifest.claimRoot` (Layer 3) and realized **only** through Layer 4. This closes the v0 contradiction in which one call emitted both provenance and reward.
- **Settle by epoch, not per signal (D1, MUST).** Reward payout **MUST** be epoch-batched. **Per-signal direct minting to a final wallet MUST NOT be the v1 mainnet settlement path.** At epoch close, exactly one `EpochSettlementManifest` is committed (a single manifest root per epoch); the epoch budget is funded **to the vault as a lump sum**, and no reward is paid except against that epoch's committed root. (Detailed vault/claim mechanics: ADR-004.)
- **v0 `mintForSignal` architecture is deprecated as mainnet architecture (D9, MUST NOT).** The per-signal `mintForSignal → mintEmissions(beneficiary, amount)` push flow **MUST NOT** be activated as the production reward path and **MUST NOT** be presented as canonical. v0 Base Sepolia contracts are prototypes; `AFIToken`/xERC20 MAY be retained, but `AFIMintCoordinator` MUST NOT be treated as the v1 coordinator, and the v0 ERC-1155 `AFISignalReceipt` MAY survive only as a clearly-labelled historical/prototype artifact — it is neither the Layer-2 reputation receipt nor a payout instrument.
- **Agent boundary (D10).** Agents **MAY** compute/score signals, build provenance leaves, and **submit** epoch settlement manifests for review under **scoped, least-privilege** permissions. Agents **MUST NEVER** control treasury funds, hold or use production private keys, perform contract upgrades, hold or change Safe roles/thresholds, or execute deployments. Any agent-submitted manifest **MUST** pass human/governance authorization before it can be committed as the epoch's settlement root and before any funding occurs.

### What this ADR deliberately does NOT decide

This ADR establishes the **four layers and their separation**. It does **not** fix value-level mechanics that the constitution marks OPEN or that other ADRs own:

- The **receipt standard** (ERC-6909) and its soulbound default → **ADR-002**.
- The **token posture** (xERC20 retained; ERC-7802 deferred) → **ADR-003**.
- The **vault/claim mechanics** (funding seam, claim vs. route, double-claim prevention) → **ADR-004**.
- **ENS-alias-vs-concrete-address** source-of-truth and Safe hardening → **ADR-005**.
- **Legal clawback / escheatment / unclaimed-reward** policy → **ADR-006** (OPEN, see O1/O2).
- **Exact EAS schema encodings** (O6), **push-vs-pull default** (O7), **tokenomics splits** (O3), **holdback/vesting** (O4), **reserve allocation** (O5), **production Safe topology** (O8) — all remain **OPEN**; this ADR commits only to *field presence and meaning*, never to value-level specifics.

---

## Consequences

### Positive

- **Provenance becomes cheap and money becomes deliberate.** Layer 1 can anchor every qualified signal as a batch root without touching tokens; payment is a separate, auditable, epoch-scoped act. The v0 inference "every qualified signal mints a reward" is eliminated by construction.
- **Independent verifiability.** Given the committed manifest plus post-disclosure off-chain data, anyone can reproduce a leaf and verify its inclusion under the committed root — without trusting AFI's private infrastructure (constitution §7).
- **Clean trust boundaries.** Scoring/agents (Layer 1–3 proposal), settlement authority (Layer 3 commit), and fund custody (Layer 4) are distinct surfaces with distinct controls. Agents can be permissioned to *propose* without ever touching funds, keys, roles, or deployments.
- **A single point of economic truth per epoch.** The manifest is the one authority for "who is owed what," so downstream contracts never recompute eligibility — reducing the attack surface and the risk of divergent answers.
- **Role-aware distribution and challenge windows become expressible.** Multi-recipient role allocations, holdbacks, and challenge windows have a natural home (manifest + vault) that the single-`beneficiary` v0 struct could not represent.

### Negative / costs

- **More moving parts.** Four layers, four specs, and four sets of artifacts replace one coordinator call. This is more to build, document, audit, and operate.
- **Two-phase latency by design.** Rewards SHOULD distribute in the *following* epoch (to allow challenge/holdback windows), so contributors are not paid the instant a signal qualifies. This is intentional but is a UX change from v0's immediate push.
- **Off-chain dependency.** v1 is commit-on-chain, store-off-chain (TSSD evidence vault). Verifiability depends on the off-chain data being available after the disclosure window; that availability is an operational responsibility, not a contract guarantee.
- **Migration burden.** Docs, schemas, and examples that teach the v0 `mintForSignal`/ERC-1155 model must be corrected or banner-deprecated (constitution §16; [AFI_V0_DEPRECATION_AND_MIGRATION.md](../specs/AFI_V0_DEPRECATION_AND_MIGRATION.md)).

### Neutral / follow-on obligations

- Layers 2–4 require their own committed specs and ADRs (002–006) before any Solidity is written; v1 MUST be cleanly specified before contract changes.
- A concrete-address registry (ADR-005) MUST exist before settlement contracts reference any account.
- The single-key root of trust (1-of-1 Safe) MUST be replaced for mainnet (ADR-005; constitution §12); this ADR makes the architectural need explicit but defers parameters (O8) to the owner.

---

## Alternatives considered

| Alternative | Summary | Why rejected |
|-------------|---------|--------------|
| **A. Keep v0 `mintForSignal` (single coupled call)** | Patch the existing per-signal coordinator that mints reward + ERC-1155 receipt together. | **Rejected.** Structurally conflates provenance and payout (violates D2/L-SEP-1), is per-signal/push-at-mint (violates D1), single-beneficiary (no role splits, no challenge windows), and concentrates emissions under one role/one key. No clean place for epoch settlement, reputation, or custody. |
| **B. Two layers (provenance + payout)** | Anchor provenance, then pay — drop the explicit reputation and manifest layers. | **Rejected.** Folding reputation into provenance reinvents the v0 "receipt = proof = payout" conflation (violates L-SEP-2). Folding the manifest into the vault makes the vault *decide* rewards rather than *enforce* them (violates L-SEP-3/L-SEP-4) and gives no single committed authority per epoch. |
| **C. Three layers (provenance + manifest + vault), reputation as manifest metadata** | Keep provenance, manifest, and vault, but treat strategy/epoch reputation as a field inside the manifest rather than a standalone receipt. | **Rejected.** Reputation has its own lifecycle (accrues across signals, finalizes at epoch close, is queried independently of any payout) and its own non-transferable, soulbound semantics. Burying it in the manifest loses that independent, auditable, standardized receipt and risks re-coupling reputation to the payout artifact. A dedicated Layer 2 (ADR-002) keeps it cleanly separated. |
| **D. Per-signal payout via Merkle batch (still per-signal economics)** | Anchor a batch root but still pay each signal its own amount to its own producer. | **Rejected.** Batching the *anchor* without batching the *economics* still pays per-signal to single beneficiaries and provides no role-aware allocation, no single epoch authority, and no custody/challenge layer. It is v0's economics with a cheaper anchor — it does not satisfy D1's epoch-settlement requirement. |
| **E. Push-only distribution baked into the architecture** | Make the router-push model the architectural default and omit proof-based pull. | **Rejected at the architecture level (the value-level default is OPEN — O7).** The architecture MUST support proof-based pull at minimum so entitlement is realizable from the committed `claimRoot` without trusting a push operator. Whether push or pull is the *default* mode is deferred to O7 / ADR-004; both are permitted, but pull-capability is mandatory. |

---

## Open questions

Per the constitution (§6), the following remain **OPEN** and **MUST NOT** be implemented as final. This ADR does not resolve them; it only fixes the layered structure within which they will be answered:

- **O1 — Legal clawback / escheatment** of unclaimed or challenge-failed rewards (mechanics, jurisdiction, custody of forfeited funds). Pending legal/compliance → ADR-006.
- **O2 — Unclaimed-reward policy** (expiry, recycle vs. roll-forward vs. return-to-treasury). A *placeholder* hook MAY be specified at Layers 3/4; the policy *value* is OPEN.
- **O3 — Exact tokenomics splits** across Providers / Analysts-Scorers / Validators / public-goods. The Layer-3 manifest carries `roleAllocationRoots|roleAllocationLeaves`; the *split values* are OPEN.
- **O4 — Holdback / vesting** schedule for rewards under challenge windows (Layer 4).
- **O6 — Exact EAS schema** field encodings and the precise on-chain anchor contract for Layer 1 (the *direction* — EAS/Merkle batch-root — is locked here; the *schema details* are implementation design).
- **O7 — Push (router) vs. pull (claims)** as the default distribution mode for Layer 4 (both permitted; pull-capability is mandatory per Alternative E).
- **O8 — Production Safe topology** (N-of-M threshold, signer roster, timelock) for settlement authority. The *principle* (not 1-of-1; addresses are truth) is locked; the *parameters* are owner decisions → ADR-005.

Additionally **OPEN within the layers** (deferred to their specs/ADRs, not to this ADR):

- Whether Layer-2 receipts may be updated after finalization, or are strictly immutable (constitution §15.2; ADR-002).
- Whether an L1 reserve vault exists at all (O5; constitution §6).

---

## Related docs

**Constitution (governing law):**
- [AFI_SETTLEMENT_V1_DOCTRINE.md](../specs/AFI_SETTLEMENT_V1_DOCTRINE.md) — the v1 constitution (this ADR implements §3 four-layer model, §4 D1/D2/D9/D10, §8–§9 core/epoch laws, §13 agent boundary).

**Layer specs (this ADR establishes the layers; specs elaborate them):**
- [AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md](../specs/AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md) — Layer 1.
- [AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md](../specs/AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md) — Layer 2.
- [AFI_EPOCH_SETTLEMENT_MANIFEST.md](../specs/AFI_EPOCH_SETTLEMENT_MANIFEST.md) — Layer 3.
- [AFI_REWARDS_VAULT_AND_CLAIMS.md](../specs/AFI_REWARDS_VAULT_AND_CLAIMS.md) — Layer 4.
- [AFI_ENS_SAFE_ADDRESS_REGISTRY_DOCTRINE.md](../specs/AFI_ENS_SAFE_ADDRESS_REGISTRY_DOCTRINE.md) — addresses/ENS/Safe source-of-truth.
- [AFI_V0_DEPRECATION_AND_MIGRATION.md](../specs/AFI_V0_DEPRECATION_AND_MIGRATION.md) — v0 deprecation posture (D9).

**Sibling ADRs:**
- [ADR-002 — ERC-6909 strategy/epoch receipts](./ADR-002-erc6909-strategy-epoch-receipts.md) (Layer 2 standard).
- [ADR-003 — xERC20 retained, ERC-7802 deferred](./ADR-003-xerc20-retained-erc7802-deferred.md) (token posture).
- [ADR-004 — RewardsVault + manifest-backed claims](./ADR-004-rewards-vault-merkle-claims.md) (Layer 4 mechanics).
- [ADR-005 — ENS aliases vs. concrete-address source of truth](./ADR-005-ens-aliases-addresses-source-of-truth.md) (addresses & Safe hardening).
- [ADR-006 — Clawback / escheatment OPEN](./ADR-006-unclaimed-rewards-legal-clawback-open.md) (legal policy, OPEN).

**Prior recon (descriptive of v0 as-it-is; still accurate, not in conflict):**
- [afi-signal-provenance-vs-reward-settlement-recon.md](../../reports/afi-signal-provenance-vs-reward-settlement-recon.md)
- [afi-onchain-contract-discovery.md](../../reports/afi-onchain-contract-discovery.md)
- [afi-settlement-semantics-recon.md](../../reports/afi-settlement-semantics-recon.md)
- [afi-vault-architecture-recon.md](../../reports/afi-vault-architecture-recon.md)
- [afi-ens-vault-registry-recon.md](../../reports/afi-ens-vault-registry-recon.md)

---

*Canonical ADR. Doctrine and design only — it implements nothing on-chain, moves no funds, and grants no roles. v0 remains a prototype and is accurately described in the recon reports above; this ADR governs the intended v1 architecture.*
