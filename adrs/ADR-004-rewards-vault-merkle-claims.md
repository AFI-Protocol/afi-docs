# ADR-004 — RewardsVault and Merkle Claim Settlement
**Status:** CANONICAL — Accepted (v1 doctrine)
**Date:** 2026-06-24
**Part of:** AFI Settlement v1 — see [AFI_SETTLEMENT_V1_DOCTRINE.md](../specs/AFI_SETTLEMENT_V1_DOCTRINE.md)

---

## Status

**Accepted** — 2026-06-24.

This ADR records a **locked v1 decision** (constitution §4, D1 and D6) for the Layer-4
reward custody/routing/claiming seam. It is **doctrine and design only**: it implements
no Solidity, deploys nothing, grants no roles, and moves no funds. It commits to the
**presence and meaning** of the RewardsVault settlement seam and its fields; exact
encodings, types, split values, and policy values are implementation design and are
marked **OPEN** where the constitution marks them OPEN.

This ADR maps to constitution Locked Decisions **D1** (epoch-batched payout), **D6**
(rewards flow through a RewardsVault + manifest-backed claim/route layer), and is bound
by the Layer-separation law **L-SEP-4**. It also carries the constitution's OPEN items
**O1, O2, O4, O7** as open questions below.

---

## Context

### The v0 reality being corrected

The deployed v0 stack (Base Sepolia prototype) settles rewards in a way that v1 **MUST NOT**
adopt as the mainnet architecture. The salient facts (descriptive recon, still accurate —
see [Related docs](#related-docs)):

- **Per-signal direct mint, push-to-wallet.** `AFIMintCoordinator.mintForSignal(MintRequest)`
  (verified on-chain as `TestMintCoordinator`, selector `0xf6d6defe`) calls
  `AFIToken.mintEmissions(req.beneficiary, req.tokenAmount)` → `_mint(beneficiary, amount)`.
  A reward is minted **directly to a single `beneficiary` address, per signal, at mint time**.
  There is **no vault, no escrow, no holdback, no claim step** between mint and wallet.
- **Provenance coupled to payout.** The *same* `mintForSignal` call can also mint an
  **ERC-1155 receipt** via `AFISignalReceipt.mintReceipt` (`tokenAmount` and `receiptAmount`
  are independent but emitted together). The receipt thus reads as "reward proof = payout
  unit" — the core v0 contradiction this ADR (with ADR-001) closes.
- **No on-chain settlement authority.** The chain enforces only the `TOTAL_SUPPLY_CAP`
  (86B). There is **no epoch budget cap, no manifest root, no eligibility check, no
  role split, no double-claim guard** on-chain. Role allocations exist only as
  research-only placeholders (`afi-econ` gauge), self-disclaimed for production use.
- **No reward/treasury vault exists at all.** A workspace search for
  `RewardsVault|TreasuryVault|ClaimVault|MerkleDistributor` returns zero hits outside the
  recon reports. The only true token-custody contract is the **unwired xERC20 bridge
  lockbox** — which MUST NOT be repurposed as the reward vault (constitution §10).
- **1-of-1 Safe authority.** The Treasury Safe `0x1Dd6705ff84Ecd5eaDc51A913Ad8e2c6C9E79aC4`
  (Base) holds `DEFAULT_ADMIN_ROLE` + `EMISSIONS_ROLE` but is a **threshold-1 Safe signed
  by a single key** (`0xb87C647a…ad62`, the sole signer of all three AFI Safes). It holds
  **0 tokens and has 0 outgoing transactions**. A 1-of-1 Safe controlling mint + emissions
  authority is **not production-grade** (constitution §12) and contradicts any "no
  centralized control" claim.
- **Stale ENS / governance pointers.** Repos hard-code `snapshotSpaceId` to a legacy
  (non-canonical) three-letter ENS alias, but **no Snapshot space exists under that legacy
  alias** and that name is owned by an unrelated party (`smilefox.eth`). The live governance
  space is **`afidao.eth`**. `treasury.afidao.eth`
  resolves to an **empty, never-used L1 placeholder Safe `0x7408…438f`** — *not* the real
  Base Treasury Safe. These pointers MUST NOT be used as the source of truth for fund
  routing (constitution §11, ADR-005). They are relevant here only insofar as the
  RewardsVault's funding authority and controller MUST be resolved by concrete address +
  chainId, never by ENS.

### Why a vault/claim layer is required

The constitution's four-layer model (§3) places **payout** strictly downstream of
**provenance** (Layer 1), **reputation** (Layer 2), and the **EpochSettlementManifest**
(Layer 3). The manifest is the *only* authority that decides who is owed what
(**L-SEP-3**). What is missing in v0 is the **custodial seam** that (a) holds the epoch
budget as a lump sum, (b) enforces the per-epoch budget cap at the funding boundary, and
(c) releases tokens to role-holders strictly against the manifest's committed root —
without recomputing eligibility. That seam is **Layer 4: the RewardsVault + claim/route
layer**, specified by [AFI_REWARDS_VAULT_AND_CLAIMS.md](../specs/AFI_REWARDS_VAULT_AND_CLAIMS.md)
and decided here.

The roles the vault settles for are **Providers / Analysts-Scorers / Validators**, plus a
**public-goods** allocation (the exact split values across these roles are **OPEN**,
constitution O3, governed by ADR-006).

---

## Decision

**AFI rewards settle through a vault/claim layer by epoch — Merkle-proof claims or
manifest-backed role routing — and NOT through direct per-signal token minting. The
RewardsVault enforces the committed manifest; it does not decide rewards.**

The following are **normative law** for v1.

### D-V1 — Custody, not direct mint (MUST)

- **MUST:** The epoch reward budget is **minted/transferred to the RewardsVault as a lump
  sum** (constitution §9). Tokens MUST NOT be minted or pushed directly to end-user wallets
  as the v1 settlement path.
- **MUST:** The **per-epoch budget cap is enforced at the funding seam** (the vault's
  funding boundary), once per epoch.
- **MUST NOT:** The RewardsVault MUST NOT mint. It custodies and releases only what it has
  been funded (separation of minting authority from settlement authority).
- **MUST NOT:** The xERC20 bridge lockbox MUST NOT be used as the RewardsVault
  (constitution §10).

### D-V2 — Pay only against the committed manifest root (MUST)

- **MUST:** Every payout MUST be authorized by inclusion in the **committed
  `EpochSettlementManifest` `claimRoot`** for that epoch (Layer 3 → Layer 4 binding).
- **MUST NOT (L-SEP-4):** The RewardsVault MUST NOT decide eligibility, recompute scores,
  or pay outside the committed root. It is an **enforcer of the manifest, not an oracle of
  rewards**.
- **MUST:** No reward may be paid for an epoch except against **that epoch's** committed
  manifest root (one manifest root per epoch; constitution §9).

### D-V3 — Settlement modes: pull (Merkle claim) and/or push (manifest-backed route)

- **MUST:** The vault MUST support **proof-based pull** at minimum: a role-holder presents a
  **Merkle proof** of their leaf against the epoch `claimRoot` to claim their allocation.
- **MAY:** The vault MAY additionally support **manifest-backed push routing** (the vault
  routes allocations to role-holders / role sub-allocations per the manifest's
  `roleAllocationRoots|roleAllocationLeaves`).
- **OPEN (O7):** Whether **push (router)** or **pull (claims)** is the *default* distribution
  mode is **OPEN**. Both are permitted; proof-based pull MUST be supported regardless of the
  default chosen.

### D-V4 — Double-claim prevention (MUST)

- **MUST:** The vault MUST prevent double-claiming via a **claimed-bitmap or nullifier**
  keyed per `(epochId, leaf/index)`. A successfully settled leaf MUST NOT be settleable
  again for the same epoch.
- **MUST:** Re-committing or re-funding an epoch MUST NOT reset already-settled state in a
  way that enables a second payout for the same leaf.

### D-V5 — Claim leaf shape (field presence + meaning; encoding OPEN)

Each Merkle leaf under the manifest `claimRoot` MUST commit, at minimum, to the
**recipient identity, the role, the amount, and the epoch binding**, so that a claim is
fully determined by the manifest and the proof — never by vault-side computation. Field
presence and meaning are doctrine; exact encoding/type is implementation design.

| Field | Presence | Meaning |
|-------|----------|---------|
| `epochId` | MUST | Binds the leaf to exactly one epoch's committed root. |
| `recipient` | MUST | The role-holder entitled to the allocation (concrete address; resolved per ADR-005, never via ENS). |
| `role` | MUST | Provider / Analyst-Scorer / Validator / public-goods (the role split values are OPEN, O3). |
| `amount` | MUST | The token amount owed to this recipient for this epoch/role (decided by the manifest, not the vault). |
| `leafIndex` \| `nullifier` | MUST | Stable key for double-claim prevention (D-V4). Encoding OPEN. |

The leaf MUST be reproducible from the published manifest and (post-disclosure) data so
that any party can independently verify inclusion under the committed `claimRoot`
(constitution §7).

### D-V6 — Holdback / challenge window (presence MUST; schedule OPEN)

- **SHOULD:** Distribution to role-holders SHOULD occur in the **epoch following** the one
  being settled, so that challenge/holdback windows can apply (constitution §9).
- **MUST:** The vault MUST honor a **`holdbackPolicyRef`** and **`challengeWindow`** carried
  by the manifest: allocations for leaves under an open challenge window MUST be
  **withholdable** until the window resolves.
- **OPEN (O4):** The **holdback / vesting schedule** (durations, fractions, release curve)
  is **OPEN** and MUST NOT be hard-coded as final.

### D-V7 — Unclaimed rewards and clawback (placeholder hook; policy OPEN)

- **MAY:** A **placeholder hook** for unclaimed-reward handling MAY be specified
  (`unclaimedRewardPolicyRef` on the manifest; constitution §15.3/§15.4).
- **OPEN (O2):** The **unclaimed-reward policy value** — expiry window and
  recycle vs. roll-forward vs. return-to-treasury — is **OPEN**. The placeholder MUST NOT be
  implemented as if it encodes a settled policy.
- **OPEN (O1):** **Legal clawback / escheatment** of unclaimed or challenge-failed rewards
  (mechanics, jurisdiction, custody of forfeited funds) is **OPEN** pending legal/compliance
  review (ADR-006). It MUST NOT be hard-coded or asserted as final policy.

### D-V8 — Pause and safety (MUST)

- **MUST:** The vault MUST be **pausable** by its documented controller such that claims/routes
  can be halted in an incident, without enabling that controller to redirect funds outside
  the committed manifest.
- **MUST NOT:** Pause/admin authority MUST NOT be a path to pay outside the manifest root,
  to mint, or to alter the committed root (L-SEP-4).

### D-V9 — Authority and the agent boundary (MUST)

- **MUST:** Authority over the RewardsVault (funding, pausing, parameter changes) MUST be
  held by a **documented Safe (SHOULD be N-of-M multisig + timelock)** — explicitly **NOT** a
  1-of-1 Safe (constitution §12). The funding authority and controller MUST be identified by
  **concrete address + chainId**, never resolved via ENS (constitution §11, ADR-005).
- **MUST NOT (agent boundary, D10):** Agents MUST NEVER control the RewardsVault's funds,
  hold its keys, pause it, change its parameters, or fund it. Agents MAY *submit* manifests
  for review; only after human/governance authorization may a manifest become the epoch's
  settlement root and trigger funding (constitution §13).

---

## Consequences

### Positive

- **Provenance is decoupled from payout.** Recording a signal (Layer 1) never moves tokens;
  the only path to tokens is a committed manifest root settled by the vault. This closes the
  v0 `mintForSignal` contradiction (with ADR-001).
- **Auditability end-to-end.** Every payout traces `signal → manifest → claimRoot → claim`,
  with the `rulesetHash` anchored. Anyone can reproduce a leaf and verify inclusion without
  trusting AFI's private infrastructure.
- **Budget containment.** The per-epoch cap is enforced once, at the funding seam; the vault
  cannot exceed what it was funded because it cannot mint.
- **Smaller trusted surface.** The vault is a dumb enforcer: it cannot decide who is owed
  what. Errors in scoring/eligibility are contained to the (reviewable, governance-gated)
  manifest, not the custody contract.
- **Flexibility preserved.** Push-vs-pull is left OPEN (O7) while guaranteeing pull as a
  floor, so the default can be chosen later without re-architecting.

### Negative / costs

- **More moving parts than v0.** v1 requires a manifest generator, a commit step, a funding
  step, and a vault — versus a single `mintForSignal` call. This is the intended cost of
  decoupling provenance from payout.
- **Latency.** Settling in the following epoch (D-V6) delays role-holder receipt relative to
  v0's mint-time payout. This is deliberate (challenge/holdback windows).
- **Claim UX / gas (pull mode).** Pull-based Merkle claims push gas onto recipients and
  require a claim UI; push/routing shifts gas to the protocol. The trade-off is unresolved
  (O7).
- **Unclaimed-reward overhang.** Because O1/O2 are OPEN, the vault will accumulate unclaimed
  balances with **no final disposition policy**. This is acceptable for doctrine but MUST be
  resolved before production (ADR-006), and the vault MUST expose a placeholder hook rather
  than silently stranding funds.

### Migration / deprecation impact

- The v0 per-signal `mintForSignal` → `mintEmissions(beneficiary, amount)` path is
  **deprecated as mainnet architecture** (constitution §5, D9). It MUST NOT be activated as
  the production reward flow. The Base Sepolia prototype MAY remain as a clearly-labelled
  historical artifact. No v0 testnet reward state migrates into v1.

---

## Alternatives considered

| # | Alternative | Why rejected |
|---|-------------|--------------|
| A1 | **Keep v0 per-signal direct mint** (`mintForSignal` → beneficiary). | Conflates provenance with payout, has no epoch budget cap, no role splits, no holdback/challenge, no double-claim model, and pushes to a single wallet at mint time. Contradicts constitution §8/§9 and D1/D2/D6. **Rejected.** |
| A2 | **Vault that computes rewards** (vault reads scores/eligibility and decides amounts). | Violates **L-SEP-3** and **L-SEP-4**: the manifest is the sole eligibility authority; the vault must not recompute. Bloats and endangers the custody contract. **Rejected.** |
| A3 | **Vault mints on claim** (vault holds `EMISSIONS_ROLE` and mints per claim). | Couples minting authority to settlement, removes the funding-seam budget cap, and re-creates a per-claim mint surface. Minting authority MUST stay separate from settlement (D-V1). **Rejected.** |
| A4 | **Push-only router (no claims).** | Forecloses proof-based pull, increases protocol gas and forced-send risk to possibly-hostile/contract recipients, and removes the recipient's ability to verify-then-claim. v1 MUST support pull at minimum (D-V3); push remains permitted as an option. **Rejected as the sole mode; retained as an optional mode (O7).** |
| A5 | **Reuse the xERC20 bridge lockbox as the reward vault.** | The lockbox is canonical-token custody for *bridging* with rate limits; repurposing it conflates bridge custody with reward custody and is explicitly forbidden (constitution §10). **Rejected.** |
| A6 | **Treasury Safe pays role-holders directly each epoch (no vault contract).** | Re-centralizes payout into a (currently 1-of-1) Safe, provides no on-chain proof-of-inclusion, no double-claim guard, and no permissionless verifiability. Fails constitution §12 and the auditability goal. **Rejected;** the Safe instead *funds* the vault (D-V9). |
| A7 | **Streaming / continuous distribution** (e.g. per-block streams). | Incompatible with epoch-batched settlement (D1) and with challenge/holdback windows; adds custody complexity with no provenance benefit. **Rejected for v1** (MAY be revisited as a future ADR). |

---

## Open questions

These are **OPEN** (constitution §6). They MUST NOT be implemented as final.

- **OQ-1 (O7) — Push vs. pull default.** Is the default distribution mode manifest-backed
  **push routing** or proof-based **pull claims**? Pull MUST be supported regardless; the
  default is owner-decided.
- **OQ-2 (O4) — Holdback / vesting schedule.** Durations, fractions, and release curve for
  rewards under challenge windows are unset.
- **OQ-3 (O2) — Unclaimed-reward policy.** Expiry window and recycle vs. roll-forward vs.
  return-to-treasury. Only a **placeholder hook** is permitted now.
- **OQ-4 (O1) — Legal clawback / escheatment.** Mechanics, jurisdiction, and custody of
  forfeited (unclaimed or challenge-failed) funds — pending legal/compliance (ADR-006).
- **OQ-5 (O8) — Vault controller Safe topology.** N-of-M threshold, signer roster, and
  timelock for the vault's funding/pause authority. The *principle* (not 1-of-1; concrete
  address is truth) is locked; the *parameters* are owner decisions.
- **OQ-6 — Exact claim-leaf encoding & proof scheme.** Field types, leaf hashing, and the
  Merkle/commitment scheme for `claimRoot` are implementation design; only field
  **presence + meaning** (D-V5) are fixed here.
- **OQ-7 — Multi-claim / batched-claim ergonomics.** Whether a recipient may settle multiple
  epochs or multiple role leaves in one transaction, and how that interacts with the
  double-claim guard (D-V4).

---

## Related docs

**Constitution:**
- [AFI_SETTLEMENT_V1_DOCTRINE.md](../specs/AFI_SETTLEMENT_V1_DOCTRINE.md) — the v1 constitution
  (this ADR maps to Locked Decisions D1, D6; bound by L-SEP-4; carries OPEN O1, O2, O4, O7).

**Specs (this set):**
- [AFI_REWARDS_VAULT_AND_CLAIMS.md](../specs/AFI_REWARDS_VAULT_AND_CLAIMS.md) — Layer 4; the
  vault/claims spec this ADR governs.
- [AFI_EPOCH_SETTLEMENT_MANIFEST.md](../specs/AFI_EPOCH_SETTLEMENT_MANIFEST.md) — Layer 3; the
  `claimRoot` / `roleAllocationRoots` authority the vault enforces.
- [AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md](../specs/AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md) —
  Layer 2; reputation receipts (NOT a payout instrument).
- [AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md](../specs/AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md) —
  Layer 1; provenance leaves (NOT redeemable for tokens).
- [AFI_ENS_SAFE_ADDRESS_REGISTRY_DOCTRINE.md](../specs/AFI_ENS_SAFE_ADDRESS_REGISTRY_DOCTRINE.md) —
  concrete-address source of truth for the vault's funder/controller.
- [AFI_V0_DEPRECATION_AND_MIGRATION.md](../specs/AFI_V0_DEPRECATION_AND_MIGRATION.md) — v0
  `mintForSignal` deprecation posture.

**Sibling ADRs:**
- [ADR-001](./ADR-001-four-layer-settlement-architecture.md) — epoch settlement;
  provenance ≠ payout; agent boundary.
- [ADR-002](./ADR-002-erc6909-strategy-epoch-receipts.md) — ERC-6909 reputation receipts.
- [ADR-003](./ADR-003-xerc20-retained-erc7802-deferred.md) — xERC20 retained; ERC-7802 deferred.
- [ADR-005](./ADR-005-ens-aliases-addresses-source-of-truth.md) — ENS aliases vs.
  concrete-address source of truth; agent boundary for fund routing.
- [ADR-006](./ADR-006-unclaimed-rewards-legal-clawback-open.md) — OPEN economic/legal items
  (clawback/escheatment, unclaimed policy, role splits, holdback/vesting).

**Prior recon (descriptive, still accurate):**
- [afi-vault-architecture-recon.md](../../reports/afi-vault-architecture-recon.md)
- [afi-settlement-semantics-recon.md](../../reports/afi-settlement-semantics-recon.md)
- [afi-signal-provenance-vs-reward-settlement-recon.md](../../reports/afi-signal-provenance-vs-reward-settlement-recon.md)
- [afi-onchain-contract-discovery.md](../../reports/afi-onchain-contract-discovery.md)
- [afi-ens-vault-registry-recon.md](../../reports/afi-ens-vault-registry-recon.md)

---

*Canonical ADR. Doctrine and design only — implements nothing on-chain, deploys nothing,
grants no roles, and moves no funds. v0 remains a prototype as accurately described in the
recon reports; this ADR governs the intended v1 Layer-4 reward custody/claim architecture.*
