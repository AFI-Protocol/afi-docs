# AFI v0 Deprecation and Migration

**Status:** CANONICAL — Accepted (v1 doctrine)
**Date:** 2026-06-24
**Part of:** AFI Settlement v1 — see [AFI_SETTLEMENT_V1_DOCTRINE.md](./AFI_SETTLEMENT_V1_DOCTRINE.md)

---

## 1. Purpose and Scope

This spec defines **how AFI Settlement v1 treats the existing v0 architecture**. It is the authoritative companion to §5 ("Deprecated") and §14 ("v0 Migration / Deprecation Posture") of the [constitution](./AFI_SETTLEMENT_V1_DOCTRINE.md), and it governs every contributor, auditor, and agent decision about what to keep, what to retire, what to replace, what to reconcile, and what to leave untouched as the protocol moves from the v0 Base Sepolia prototype toward a cleanly-specified v1.

**This document is doctrine and migration law only.** It implements nothing. It does **not** deploy, mint, grant roles, revoke roles, move funds, modify ENS/Safe state, edit Solidity, or alter runtime config. It tells you what posture to take so that the repository stops teaching the v0 per-signal mint as canonical, and so that nobody accidentally promotes a testnet prototype into a mainnet settlement system.

The v0 facts referenced here are sourced from the read-only recon reports and remain accurate as descriptions of v0 **as it is**:

- [`../../reports/afi-vault-architecture-recon.md`](../../reports/afi-vault-architecture-recon.md) — vault / custody / routing / claiming dimension; confirms **no token/reward/treasury vault exists** and that `mintForSignal` pushes per signal to a single beneficiary.
- [`../../reports/afi-onchain-contract-discovery.md`](../../reports/afi-onchain-contract-discovery.md) — live on-chain state (Base Sepolia / Base mainnet), addresses, role wiring, `totalSupply = 0`, incomplete coordinator role grants.

Where this spec and the constitution agree (they must), the constitution wins on any conflict. Where any v0 README, comment, schema, or contract conflicts with this spec on a **v1 architecture** question, this spec and the constitution win, and the v0 artifact is to be treated as stale, prototype, or runtime-deferred.

---

## 2. Normative Language

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, **MAY**, and **OPEN** are used as defined in [AFI_SETTLEMENT_V1_DOCTRINE.md §1](./AFI_SETTLEMENT_V1_DOCTRINE.md). In particular, **OPEN** means a decision is deliberately not settled: it MUST NOT be implemented as if final and MUST be resolved by the owner (and, where noted, legal/compliance) before implementation.

---

## 3. Core Deprecation Law

These are the non-negotiable rules for treating v0. They restate and bind §5 and §14 of the constitution.

### 3.1 v0 contracts are prototypes (MUST)

- **MUST:** The v0 Base Sepolia contracts (`AFIToken` / `AFISignalReceipt` / `AFIMintCoordinator` at the canonical testnet addresses) are **prototypes**. They MUST NOT be treated, presented, marketed, or relied upon as mainnet-ready or as the v1 settlement architecture.
- **MUST NOT:** No document MAY claim the v0 Base Sepolia stack is "mainnet-ready," or that AFI has "no centralized control," while a single 1-of-1 Safe (`0x1Dd6705ff84Ecd5eaDc51A913Ad8e2c6C9E79aC4`) holds `DEFAULT_ADMIN_ROLE` + `EMISSIONS_ROLE`. Per the recon, that Safe holds **authority, not custody** (0 token balance, 0 outgoing txs); concentrated admin/emissions authority in one 1-of-1 Safe is **not production-grade** (constitution §12).
- **Fact anchor:** Base mainnet has **no AFI token stack** deployed; the deployed trio lives on Base Sepolia only, with `totalSupply = 0` and incomplete coordinator role wiring (`mintForSignal` would currently revert) — see [`../../reports/afi-onchain-contract-discovery.md`](../../reports/afi-onchain-contract-discovery.md).

### 3.2 `mintForSignal` is deprecated as mainnet settlement architecture (MUST NOT)

- **MUST NOT:** `AFIMintCoordinator.mintForSignal` → `AFIToken.mintEmissions(beneficiary, amount)` (per-signal, single `beneficiary`, push-to-wallet at mint time, with an `AFISignalReceipt` ERC-1155 minted **in the same call**) MUST NOT be activated, wired, or promoted as the **production / mainnet reward settlement flow**. It is **deprecated as mainnet settlement architecture** (constitution D9, ADR-001).
- **Why:** It violates the v1 layer-separation laws (constitution §3): recording provenance MUST NOT mint or pay (L-SEP-1), and reward entitlement MUST be established only via a committed `EpochSettlementManifest` `claimRoot` and realized only through the RewardsVault/claim layer (constitution §8, §9). `mintForSignal` conflates provenance and payout in one transaction — the exact contradiction v1 exists to close.
- **MUST:** v1 rewards MUST be **epoch-batched**, funded as a lump sum to a `RewardsVault`, and paid only against a committed manifest root (constitution D1, D6, §9). Per-signal direct minting to a final wallet MUST NOT be the v1 mainnet settlement path.

### 3.3 Do NOT grant roles to activate per-signal minting as production (MUST NOT)

- **MUST NOT:** Contributors and agents MUST NOT execute (or instruct anyone to execute) the pending Safe role grants for the purpose of turning on per-signal reward minting as a production flow. Specifically, granting `EMISSIONS_ROLE` on `AFIToken` to the coordinator, `MINT_COORDINATOR_ROLE` on receipts to the coordinator, and `EMISSIONS_ROLE` on the coordinator to an agent — in order to make `mintForSignal` live as the settlement path — MUST NOT be done under v1.
- **MAY (testnet only, owner-decided):** The owner MAY still exercise these grants **on testnet** for prototype/experimentation purposes, clearly labelled as non-canonical. That is a runtime decision reserved to the owner (see §6) and is **not** a v1 production activation.
- **MUST NOT (agent boundary):** Agents MUST NEVER grant, hold, or change Safe roles/thresholds, hold production private keys, or execute deployments (constitution §13, D10). The role-grant decision is owner/Safe-only.

### 3.4 Do NOT migrate flawed testnet state into v1 (MUST NOT)

- **MUST NOT:** Flawed or prototype testnet state MUST NOT be migrated, snapshotted, replayed, or "promoted" into v1 as if it were authoritative settlement history. This includes any per-signal mint records, ERC-1155 receipt balances, simulation-contract artifacts, and incomplete/ad-hoc role wiring.
- **MUST:** v1 begins from a **clean, cleanly-specified baseline**. Any historical v0 data retained is **historical/prototype evidence only** and MUST NOT seed v1 reward entitlements, balances, or manifests.
- **MAY:** The off-chain **TSSD evidence vault** (data, not tokens) is **unchanged** by Settlement v1 (constitution §7) and its records MAY continue to be used as evidence/training corpus. This is a data store, not settlement state, and does not constitute "flawed testnet state" in the sense prohibited above.

### 3.5 Token retention vs. coordinator/receipt disposition

- **MAY:** `AFIToken` / its **xERC20** posture **MAY be retained** for v1. The AFI token MUST remain xERC20-compatible; **ERC-7802 / SuperchainERC20 is deferred** and MUST NOT be presented as a v1 dependency (constitution D4, D5, §10). The xERC20 lockbox is **bridge custody only** and MUST NOT be repurposed as the reward or treasury vault.
- **MUST NOT:** `AFIMintCoordinator` MUST NOT be treated as the v1 coordinator. The v1 settlement authority is the (to-be-specified) Settlement/Epoch coordinator that commits one `EpochSettlementManifest` root per epoch — a **different object** from `AFIMintCoordinator`, which only orchestrates per-signal mints and custodies nothing.
- **MAY (constrained):** `AFISignalReceipt` (ERC-1155) **MAY be retained only as a historical/prototype artifact**, clearly labelled, **unless separately approved** by the owner for some other narrow purpose. It is **not** the Layer-2 reputation receipt (v1 uses **ERC-6909**, soulbound by default — constitution D3, §15.2) and it is **not** a payout instrument. A provenance artifact MUST NOT be redeemable for tokens (constitution §8).

### 3.6 Specify v1 before touching Solidity (SHOULD / MUST)

- **MUST:** v1 MUST be **cleanly specified** (this doctrine set: the constitution plus the Layer 1–4 specs and the ENS/Safe registry doctrine) **before** any Solidity changes are made to implement settlement.
- **SHOULD:** No production Solidity, deploy script, role grant, or mainnet config change SHOULD be authored to "fix v0" in place. The correct path is **specify v1 → owner approval → implement v1**, not patch the prototype. Doctrine-only documentation work proceeds now; runtime work is owner-gated (see §6).

---

## 4. v0 Artifact → v1 Disposition Map

Disposition vocabulary:

- **Retain** — keep as-is; permitted into v1 (possibly relabelled), no replacement required.
- **Deprecate** — keep only as historical/prototype artifact, clearly labelled; MUST NOT be taught as canonical or activated as production.
- **Replace** — superseded by a v1 object that MUST be newly specified/built; the v0 form MUST NOT be the v1 form.
- **Reconcile** — a runtime fact (address/config/Safe) that MUST be corrected/registered against v1 source-of-truth before settlement contracts reference it.
- **Owner-defer** — decision and/or runtime action reserved to the protocol owner; doctrine MUST NOT pre-empt it.

| # | v0 artifact | v1 disposition | Normative basis | Notes |
|---|-------------|----------------|-----------------|-------|
| A1 | **`AFIToken`** (xERC20, tAFI; supply cap 86B) | **Retain** (+ Owner-defer on any mainnet deploy) | D4, D5, §10 | Token + xERC20 posture MAY be kept; ERC-7802 deferred; bridge lockbox MUST NOT become the reward vault. Mainnet deployment is owner-deferred (none exists today). |
| A2 | **`AFIMintCoordinator`** (`mintForSignal`) | **Replace** (and **Deprecate** the v0 form) | D9, §3, §8, §9 | MUST NOT be treated as the v1 coordinator. v1 introduces a separate Settlement/Epoch coordinator that commits one manifest root per epoch and custodies nothing. |
| A3 | **`AFISignalReceipt`** (ERC-1155 per-signal receipt) | **Deprecate** (retain as historical/prototype only, unless separately approved) | D3, §5, §8, §15.2 | Not the Layer-2 receipt (v1 = ERC-6909 soulbound), not a payout instrument, not redeemable for tokens. |
| A4 | **`mintForSignal` flow** (per-signal, push, mint-time receipt+reward coupled) | **Replace** (and **Deprecate** as mainnet architecture) | D1, D2, D9, §8, §9 | Provenance ≠ payout. Replaced by Layer 1 commitment + Layer 3 manifest + Layer 4 vault/claim. MUST NOT be the production reward path. |
| A5 | **Single-beneficiary payout** (one `address beneficiary`, `tokenAmount`/`receiptAmount` per signal) | **Replace** | D1, §15.3, §15.4 | Replaced by manifest `claimRoot` + `roleAllocationRoots` over (recipient, role, amount) for Providers / Analysts-Scorers / Validators / public-goods. Exact split values are **OPEN** (O3). |
| A6 | **`validatorConfig` `snapshotSpaceId: "afidao.eth"`** | **Reconcile** (+ Owner-defer the runtime edit) | D7, §11 | Governance space is **`afidao.eth`** (network 1); the legacy three-letter ENS alias as a Snapshot/governance pointer is **stale/incorrect**. Docs/examples MUST be corrected; editing the runtime `validatorConfig.schema.json` default is owner-deferred (§6). |
| A7 | **Treasury Safe 1-of-1** (`0x1Dd6705…`, admin + emissions authority) | **Reconcile** (+ Owner-defer the topology) | §12, O8 | 1-of-1 is **not production-grade**; production authority SHOULD be N-of-M multisig + timelock. Concrete address + chainId + threshold are source of truth (D7). Exact topology is **OPEN/owner** (O8). |
| A8 | **`afi-mint` Solidity stubs** (`MintManager`, `ChallengeRegistry`, `ThresholdRules`) | **Replace** | §3, §9 | Empty stubs; no logic. Superseded by v1 settlement design; MUST NOT be filled in to revive per-signal minting. |
| A9 | **Legacy simulation contracts** (`0x5b01…`, `0x574f…`, `0xa222…`, Base Sepolia) | **Deprecate** | §5 | Superseded by the verified trio; historical only; MUST NOT be referenced as canonical. |
| A10 | **`afi-econ` gauge / reward models** (e.g. `gauge_v0.yaml`) | **Owner-defer** (research-only) | O3, §6 | Self-disclaimed placeholders; define role-split **intent**, not law. Exact tokenomics splits are **OPEN**. MUST NOT be wired to contracts as final. |
| A11 | **TSSD evidence vault** (data store; `VaultedSignalRecord`) | **Retain (unchanged)** | §7 | Data custody, not token custody. Unchanged by Settlement v1. Naming MUST stay distinct from "RewardsVault"/"TreasuryVault." |

---

## 5. Disposition Detail Notes

### 5.1 Retain (A1, A11)

`AFIToken` and the TSSD evidence vault are the two clean inheritances into v1. The token's xERC20 surface is the basis for v1's token posture (constitution §10); the existing `XERC20Lockbox` remains **bridging** custody and MUST NOT be wired as the reward or treasury vault. The TSSD vault remains a **data** store: per constitution §7, raw signal data stays off-chain until the delayed-disclosure window elapses, and only commitments (roots/hashes/pointers) go on-chain.

### 5.2 Replace (A2, A4, A5, A8)

These embody the v0 contradiction the recon flagged as P1: per-signal direct mint vs. intended epoch-batched, role-split, vault-routed settlement. v1 replaces them with the four-layer model — Layer 1 provenance commitment (EAS-backed Merkle batch root), Layer 2 ERC-6909 reputation, Layer 3 `EpochSettlementManifest`, Layer 4 `RewardsVault` + claims. The v0 coordinator and stubs MUST NOT be incrementally extended into these roles; they are superseded, not upgraded.

### 5.3 Deprecate (A3, A9; and the v0 form of A2/A4)

Deprecated artifacts MAY remain on-chain / in-repo as historical evidence but MUST carry clear labelling and MUST NOT be taught as canonical or activated as production. `AFISignalReceipt` is the sensitive case: it MAY be retained **only** as a historical/prototype artifact unless the owner separately approves a narrow alternative use; it is explicitly not the Layer-2 receipt and not redeemable.

### 5.4 Reconcile (A6, A7)

Reconcile items are runtime facts that must be made correct against v1 source-of-truth (concrete address + chainId + threshold; correct governance space) **before** any settlement contract references them. Doctrine corrects the **documentation/examples now**; the **runtime edits themselves are owner-deferred** (§6). A concrete-address registry (constitution §12, §15.5; `AFI_ENS_SAFE_ADDRESS_REGISTRY_DOCTRINE.md`) MUST exist before settlement contracts reference any account, and the real Base Treasury Safe MUST be reconciled there (note: `treasury.afidao.eth` currently resolves to an empty placeholder Safe and is **not** `0x1Dd6705…` — constitution §11).

### 5.5 Owner-defer (A10; and the runtime edits of A6/A7, mainnet of A1)

Owner-defer covers economic policy (tokenomics splits — OPEN O3), production Safe topology (OPEN O8), and every runtime action that grants roles, edits mainnet config, or moves funds. Doctrine MUST NOT pre-empt these; it records the **principle** (e.g., "not 1-of-1," "addresses are truth," "splits are OPEN") and leaves the **values/actions** to the owner.

---

## 6. Runtime-Sensitive Files — Owner-Deferred (DO NOT MODIFY)

The following are **runtime-sensitive** and MUST be left to the protocol owner. This doctrine work MUST NOT edit, deploy, execute, grant/revoke against, or otherwise mutate any of them. They are listed so contributors and agents know to stop at the doctrine boundary. (Agents are additionally bound by the constitution §13 / D10 agent boundary: never control treasury funds, production keys, upgrades, Safe roles, or deployments.)

| Runtime-sensitive item | Path / locus | Why owner-deferred |
|------------------------|--------------|--------------------|
| AFI token / receipt / coordinator Solidity | `afi-token/src/*.sol` (`AFIToken.sol`, `AFISignalReceipt.sol`, `AFIMintCoordinator.sol`) | Live prototype contracts; v1 MUST be specified before Solidity changes (§3.6). |
| Deploy / sanity scripts | `afi-token/script/*.s.sol` (`DeployAFITestnet`, `DeployAFIToken`, `DeployAFITokenMainnet`, `DeployAFILocal`) + sanity `.sh` | Encode deployment + role-grant runbooks; running them is a runtime/owner action. |
| xERC20 bridge subsystem | `afi-xerc20/**` | Bridge custody (lockbox/factory); MUST NOT be repurposed as reward/treasury vault; vendored runtime. |
| `afi-mint` Solidity stubs | `afi-mint/contracts/*.sol` | Empty stubs; filling them is a v1 implementation/owner decision, not doctrine. |
| Mainnet config | any mainnet address/chainId/config file referenced by deploy scripts | Source-of-truth runtime config; owner-controlled. |
| Safe config | Treasury / governance Safe config (e.g. `afi-governance/SAFE REALITY/*`, any multisig config) | Threshold, signer set, roles — owner/Safe-only. |
| Role grants | any `grantRole`/`revokeRole` action (token/receipt/coordinator) | Activating these is the prohibited production-activation step (§3.3); owner/Safe-only. |
| Tokenomics / reward math | `afi-econ/**` (gauge, reward/reputation models), `afi-math/src/emissions/*` | Splits are **OPEN** (O3); research-only; MUST NOT be wired as final law. |
| Validator config schema | `afi-config/schemas/validatorConfig.schema.json` | Carries a stale `snapshotSpaceId` default (the legacy three-letter ENS alias); correcting the runtime default is an owner-deferred edit (A6). |
| Orchestrator types | `afi-mint/src/orchestrator/types.ts` | Runtime FSM/payload shapes (e.g. `SignalValidatorState`, single-beneficiary mint payloads); v1 alignment is an owner-gated implementation step. |

**MUST NOT:** Nothing in this migration spec authorizes editing the above. Where a v0 default is wrong for v1 (e.g. the legacy three-letter ENS alias as a governance pointer, single-beneficiary payload shape, 1-of-1 Safe), this spec records the **correct v1 position in doctrine**; the **runtime correction is owner-deferred**.

---

## 7. Migration Sequencing (doctrine, not execution)

The correct order of operations — **none of which this document performs** — is:

1. **Specify v1 cleanly** (this doctrine set + Layer 1–4 specs + ENS/Safe registry doctrine). _In progress; doctrine-only._
2. **Owner approval** of the locked v1 architecture and resolution of the relevant OPEN items (constitution §6) where they block implementation.
3. **Build the concrete-address registry** (constitution §12, §15.5) and reconcile A6/A7 runtime facts (governance space, real Treasury Safe, Safe topology).
4. **Implement v1 contracts/services** (Settlement coordinator, RewardsVault, claims/Merkle, ERC-6909 receipts, manifest generator) — only after Stage 1 doctrine is locked.
5. **Owner-executed runtime actions** (deploy, role grants behind an N-of-M Safe + timelock, funding). Agents MUST NOT perform these.

v0 is **frozen as a prototype** through this sequence. It is not patched into v1; v1 supersedes it.

---

## 8. Conformance

A document, schema, comment, or contract conforms to this migration spec if and only if it: (a) does not present any v0 artifact in §4 as the canonical v1 form against its stated disposition; (b) does not activate or promote `mintForSignal`/single-beneficiary per-signal payout as the production reward path; (c) does not migrate flawed testnet state into v1; and (d) does not edit any §6 runtime-sensitive file under the guise of doctrine. v0 recon/audit reports that **describe** v0 as historical reality (including the two referenced reports) conform, as they do not present v0 as the intended v1 future.

---

## 9. Related Documents

- [`./AFI_SETTLEMENT_V1_DOCTRINE.md`](./AFI_SETTLEMENT_V1_DOCTRINE.md) — the constitution (esp. §5, §10, §11, §12, §13, §14, §15).
- [`./AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md`](./AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md) — Layer 1 (replaces on-chain provenance coupling).
- [`./AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md`](./AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md) — Layer 2 (replaces ERC-1155 as the v1 receipt standard).
- [`./AFI_EPOCH_SETTLEMENT_MANIFEST.md`](./AFI_EPOCH_SETTLEMENT_MANIFEST.md) — Layer 3 (replaces single-beneficiary payout).
- [`./AFI_REWARDS_VAULT_AND_CLAIMS.md`](./AFI_REWARDS_VAULT_AND_CLAIMS.md) — Layer 4 (the custodial seam v0 lacks).
- [`./AFI_ENS_SAFE_ADDRESS_REGISTRY_DOCTRINE.md`](./AFI_ENS_SAFE_ADDRESS_REGISTRY_DOCTRINE.md) — addresses/ENS/Safe source-of-truth (reconciles A6/A7).
- **ADRs:** [`../adrs/ADR-001`](../adrs/) (epoch settlement / provenance ≠ payout / v0 deprecation), [`../adrs/ADR-002`](../adrs/) (ERC-6909), [`../adrs/ADR-003`](../adrs/) (xERC20 / ERC-7802 deferred), [`../adrs/ADR-004`](../adrs/) (RewardsVault), [`../adrs/ADR-005`](../adrs/) (addresses are truth), [`../adrs/ADR-006`](../adrs/) (clawback/escheatment OPEN).
- **Recon (descriptive, still accurate):** [`../../reports/afi-vault-architecture-recon.md`](../../reports/afi-vault-architecture-recon.md), [`../../reports/afi-onchain-contract-discovery.md`](../../reports/afi-onchain-contract-discovery.md).

---

*Canonical migration doctrine. This document defines posture and law only; it implements nothing on-chain and edits no runtime-sensitive file. v0 remains as a labelled prototype and as accurately described in the existing recon reports; v1 supersedes it once cleanly specified and owner-approved.*
