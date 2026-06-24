# AFI ENS / Safe / Address Registry Doctrine

**Status:** CANONICAL — Accepted (v1 doctrine)
**Date:** 2026-06-24
**Part of:** AFI Settlement v1 — see [AFI_SETTLEMENT_V1_DOCTRINE.md](./AFI_SETTLEMENT_V1_DOCTRINE.md)

---

## 1. Purpose & Scope

This document is the canonical law for how AFI Settlement v1 treats **ENS names, Gnosis Safes, vault labels, and concrete addresses**. It elaborates §11 (ENS Aliases vs. Concrete Address Source of Truth), §12 (Safe / Governance Hardening Principles), and §15.5 (ENS/Safe registry entry) of the [constitution](./AFI_SETTLEMENT_V1_DOCTRINE.md), and binds Locked Decision **D7** ("ENS names are aliases; concrete addresses are the source of truth") and **D10** (agent boundary).

**This is doctrine/design only.** Nothing in this document is implemented, deployed, or executed. It does **not** set, alter, renew, unwrap, or transfer any ENS record; it does **not** submit any Safe transaction, change any Safe owner/threshold, grant any role, or move any funds. It tells contributors, auditors, integrators, and agents **what the address/identity layer means** so that no one trusts a name where they must trust an address.

The factual baseline for this doctrine is the read-only recon report [`../../reports/afi-ens-vault-registry-recon.md`](../../reports/afi-ens-vault-registry-recon.md) and its machine-readable companion [`../../reports/afi-ens-vault-registry.draft.json`](../../reports/afi-ens-vault-registry.draft.json). Those reports **describe v0/current reality and remain accurate**; this spec governs the **intended v1 treatment** of that reality. Where this spec and the recon report appear to differ, the recon describes *what is*, and this spec states *what the law is going forward*.

> **Normative language** (MUST / MUST NOT / SHOULD / SHOULD NOT / MAY / OPEN) is used exactly as defined in [§1 of the constitution](./AFI_SETTLEMENT_V1_DOCTRINE.md#1-normative-language). **OPEN** items MUST NOT be implemented as if final.

---

## 2. The Core Law — Names Are Aliases, Addresses Are Truth

| # | Rule | Strength |
|---|------|----------|
| **R-1** | An ENS name (e.g. `afidao.eth`, `treasury.afidao.eth`) is a **human-readable alias only**. It carries no authority of its own. | **MUST** |
| **R-2** | The **concrete address + `chainId` + Safe threshold + signer policy** is the **source of truth** for every contract, config, governance action, and settlement step. | **MUST** |
| **R-3** | Contracts **MUST NOT** resolve ENS dynamically for **access control, fund routing, authorization, or role checks**. ENS resolution is an off-chain convenience for humans and tooling, never an on-chain trust anchor. | **MUST NOT** |
| **R-4** | Where a name and an address disagree, the **address wins**. A document, config, or comment that asserts a name *is* an account (rather than *aliases* one) is non-conforming and MUST be corrected. | **MUST** |
| **R-5** | An ENS name maps to a funded, trusted account **only after** a concrete address, `chainId`, account type, and signer policy are **bound and owner-verified** in the future concrete-address registry (§7). Until then a name is **scaffolding**, not a vault. | **MUST** |

### 2.1 Why ENS MUST NOT be an on-chain trust anchor (technical basis)

The recon establishes that the `afidao.eth` subnames are **mutable**: all five subnames (`treasury` / `reserve` / `grants` / `ops` / `liq`) have **fuses `0` and expiry `0`** (not emancipated), so the parent owner can **silently rewrite or replace any subname's target address at any time**. The root `afidao.eth` itself has **`CANNOT_UNWRAP` not burned** (owner can still unwrap/transfer) and **expires 2026-12-01**. A contract that resolved ENS for authorization would therefore delegate its access control to a single mutable, expiring, off-chain-administered record. This is exactly why **R-3 is a hard MUST NOT**, not a recommendation.

---

## 3. Current ENS Scaffolding — Status of `afidao.eth` and Subnames

The following reflects the recon baseline and is stated here as **canonical status**, not as production wiring.

- **MUST (status):** The current `afidao.eth` subnames — `treasury` / `reserve` / `grants` / `ops` / `liq` — are **placeholder scaffolding**, **not active funded vaults**. They are reserved identity labels expressing **intent**; they are **not** an implemented multi-vault custody system.
- **MUST NOT:** No document, config, integration, or contract MUST treat any current `afidao.eth` subname as a funded, production vault or as a settlement custody account.
- **Observed collapse (informative):** The five subnames do **not** resolve to five distinct accounts. Per recon, the namespace collapses to **two empty 1-of-1 Safes on Ethereum mainnet**:
  - `afidao.eth` (root) **and** `reserve.afidao.eth` → `0x4b02AC8E5551C30c4C92814F63D4576F335E4112` (the ENS-admin Safe; ~18 txs of namespace setup; **0 ETH**, holds only ENS wrapped-name NFTs).
  - `treasury.afidao.eth` = `grants.afidao.eth` = `ops.afidao.eth` = `liq.afidao.eth` → `0x7408d8e97280e391A38DffE3AE8dF7E5c553438f` (**one** Safe, **0 transactions ever**, **0 ETH/0 value tokens**).
- **MUST (de-duplication law):** A production registry **MUST NOT** let four lanes share one address, and **MUST NOT** let `reserve` collide with the root/admin identity. Each funded lane that is retained MUST resolve to a **distinct, owner-verified account** with its own signer policy.
- **MUST (chain law):** Every current `afidao.eth` address record is **L1 (Ethereum mainnet, coinType 60)**, but **AFI executes on Base**. **No** `afidao.eth` name carries a Base/L2 (ENSIP-11) address record. The L1-ENS-vs-Base-execution mismatch MUST be resolved explicitly in the future registry; a name's chain is part of its identity, not an afterthought.

> **None of these names, Safe addresses, or the operator key appear anywhere in the AFI repos** (recon: zero references across all repos). The ENS identity layer and the codebase are currently **disconnected**. This disconnection is a gap to be closed by the registry of §7 — not by hard-coding ENS into contracts.

---

## 4. Treasury Reconciliation Law (`treasury.afidao.eth` ≠ the real Base Treasury Safe)

This is the **highest-risk mismatch** in the address layer and is elevated to its own normative section.

- **MUST (status):** `treasury.afidao.eth` currently resolves to an **empty placeholder Safe** (`0x7408d8e97280e391A38DffE3AE8dF7E5c553438f`, Ethereum mainnet, 0 ETH, **zero executed transactions**). It is **NOT** the real Base Treasury Safe.
- **MUST (truth):** The real on-chain AFI Treasury Safe — the account holding `DEFAULT_ADMIN_ROLE` + `EMISSIONS_ROLE` per [`../../reports/afi-onchain-contract-discovery.md`](../../reports/afi-onchain-contract-discovery.md), and the Snapshot `member` of `afidao.eth` — is **`0x1Dd6705ff84Ecd5eaDc51A913Ad8e2c6C9E79aC4`** on **Base** (`chainId 8453`; also present on Base Sepolia). **No ENS name resolves to this address today.**
- **MUST NOT:** No document, config, integration, audit, or contract MUST present `treasury.afidao.eth` as the production treasury, nor treat the empty L1 placeholder as equal to the real Base authority Safe.
- **MUST (reconciliation):** The real Base Treasury Safe `0x1Dd6705…` **MUST be reconciled in a future concrete-address registry** (§7) before any settlement contract references a "treasury" account. Reconciliation means either re-pointing the `treasury` alias to the verified Base Safe (or a new dedicated Base treasury Safe) **and** recording the concrete address as the source of truth — with the address, not the alias, as the on-chain anchor.
- **MUST (no blind routing):** Until reconciliation is complete and owner-verified, **no funds, roles, or settlement routing MUST be directed by the `treasury.afidao.eth` alias**. The trap to avoid: an integrator trusting ENS would route treasury, grants, ops, and liquidity to **one empty placeholder on the wrong chain**.

---

## 5. Safe / Control Hardening Law

- **MUST NOT:** **1-of-1 Safe control is not production-grade.** Per recon, all three relevant Safes — `0x4b02` (L1), `0x7408` (L1), and the real Base Treasury Safe `0x1Dd6705` — are **threshold-1, signed by the single key `0xb87C647a1a0857a4f96271F1d9846fd470e4ad62`**. Treasury, reserve, and settlement authority **MUST NOT** remain under a single 1-of-1 Safe for mainnet v1.
- **SHOULD:** Production authority over treasury/reserve and over the SettlementCoordinator / RewardsVault **SHOULD** be an **N-of-M multisig + timelock**, with a documented signer roster and threshold. (The constitution marks the **exact** N-of-M parameters, signer set, and timelock as **OPEN — O8**; the *principle* is locked, the *values* are owner decisions.)
- **MUST (single-key risk):** The fact that one key (`0xb87C…`) currently signs the L1 ENS Safes **and** the Base treasury authority is a single-point-of-control and single-point-of-failure risk. The registry MUST surface this so it is visible and removable, not hidden.
- **MUST (agent boundary, per D10):** Agents **MUST NEVER** hold or use production private keys, control treasury funds, change Safe roles/thresholds, or execute deployments. Agents **MAY** *reference* registry entries (read-only) when building or submitting manifests, but a registry entry never grants an agent control of the account it describes. See [§13 of the constitution](./AFI_SETTLEMENT_V1_DOCTRINE.md#13-agent-boundary-rules).

---

## 6. Governance Pointer Law (`afidao.eth` is live; the legacy three-letter ENS alias is stale/wrong)

- **MUST:** The **live** AFI DAO Snapshot/governance space is **`afidao.eth`** (Snapshot `network: "1"`). Its identity is confirmed: `website = https://afiprotocol.org/`, `github = AFI-Protocol`, `symbol = AFI`, with the real Base Treasury Safe `0x1Dd6705…` as a Snapshot `member`.
- **MUST NOT:** References to **the legacy (non-canonical) three-letter ENS alias** as the Snapshot/governance space are **stale/incorrect** and MUST NOT be used as the AFI governance pointer. Per recon: **no Snapshot space under that legacy three-letter alias exists**, and that ENS name is owned by an **unrelated third party** (resolves to EOA `smilefox.eth`, `0x057302a507F41415DcC68A2C62D5b8abF207a20d`).
- **MUST (correction in prescriptive docs):** Prescriptive docs/examples that carry the legacy three-letter ENS alias as the governance space MUST be corrected to `afidao.eth`. Per the constitution, **runtime config** still carrying that legacy alias (e.g. `snapshotSpaceId` defaults observed in the repo) is **runtime-sensitive and owner-deferred** — it MUST NOT be silently edited by this doctrine work; it is to be tracked for owner action, not executed.
- **Note (informative):** The Snapshot space `afidao.eth` is configured for **L1 (network 1)** while AFI contracts execute on **Base** — the same chain-mapping mismatch flagged in §3. It currently has **0 proposals** and declares **no treasuries**.

---

## 7. The Future Concrete-Address Registry (required shape)

Per [§12 of the constitution](./AFI_SETTLEMENT_V1_DOCTRINE.md#12-safe--governance-hardening-principles), a **concrete-address registry MUST exist before settlement contracts reference any account.** This section fixes the **required per-entry fields**. Field **presence and meaning** are doctrine; exact encodings/types and the concrete address *values* are implementation design and owner-verified data (the latter is **OPEN** until verified).

### 7.1 Required fields per registry entry

Using the canonical field names from [§15.5 of the constitution](./AFI_SETTLEMENT_V1_DOCTRINE.md#155-enssafe-registry-entry-afi_ens_safe_address_registry_doctrinemd) verbatim. Every entry **MUST** carry all nine:

| Field | Meaning | Normative notes |
|-------|---------|-----------------|
| `ensAlias` | The human-readable ENS name (or `null` if the account has none). | **MUST** be treated as an alias only (R-1). An account MAY exist with no `ensAlias` (e.g. the real Base Treasury Safe today). |
| `resolvedAddress` | The concrete on-chain address. | **This is the source of truth (R-2).** MUST be present for any entry that can be referenced by config/contracts. MUST be owner-verified before the entry is trusted. |
| `chainId` | The chain the address is authoritative on (e.g. `1` Ethereum mainnet, `8453` Base, `84532` Base Sepolia). | **MUST** be present; an address without a chain is ambiguous. Resolves the L1-vs-Base mismatch (§3). |
| `accountType` | What the account is: `safe`, `eoa`, `contract`, `lockbox`, etc. | **MUST** be present. An `eoa` MUST NOT be a production treasury/reserve custody account. |
| `safeThreshold` | For Safes, the `N-of-M` threshold (e.g. `1-of-1`, `3-of-5`); `null`/`n/a` for non-Safe accounts. | **MUST** be present for `safe` entries. `1-of-1` MUST be flagged as not production-grade (§5). |
| `status` | Lifecycle state: `placeholder` / `scaffolding` / `unverified` / `verified` / `active` / `deprecated`. | **MUST** be present. Current `afidao.eth` subnames MUST be `placeholder`/`scaffolding` until owner-verified. |
| `allowedActions` | The actions this account is permitted to perform. | **MUST** be present and least-privilege. e.g. "fund RewardsVault per epoch", "manage ENS namespace". |
| `forbiddenActions` | The actions this account MUST NOT perform. | **MUST** be present and explicit. e.g. "custody per-user reward balances", "bypass the committed manifest root", "be resolved by a contract for access control". |
| `controller` | Who/what controls the account (signer policy: the signer set or owning Safe, threshold, timelock if any). | **MUST** be present. For Safes MUST name the signer policy; 1-of-1 hot-key control MUST be visible here. |

### 7.2 Registry laws

- **MUST:** Every account that any settlement contract, config, or governance action references **MUST** have a registry entry with all nine fields **before** it is referenced.
- **MUST:** The registry MUST bind `ensAlias → resolvedAddress → chainId` with `resolvedAddress` as the trust anchor; ENS is recorded **only** as an off-chain alias.
- **MUST:** The registry MUST **de-duplicate** lanes (§3) and **reconcile** the real Base Treasury Safe (§4) before those lanes are funded or referenced.
- **MUST NOT:** A registry entry MUST NOT be marked `verified`/`active` until the owner has confirmed ownership of the keys and the intended meaning of the lane.
- **SHOULD:** The registry SHOULD live in `afi-config` as the canonical machine-readable artifact (the recon's draft JSON is a **non-canonical** precursor, not the registry).

---

## 8. Worked Example Registry (DRAFT — illustrative only)

> **DRAFT.** The table below is an **illustrative** example of the §7 shape applied to the recon baseline. It is **not canonical**, **not owner-verified**, and **not an instruction to wire anything**. **Concrete addresses are the source of truth; ENS aliases are aliases.** All `resolvedAddress` values are owner-verification-pending; all `target` re-pointings are proposals only.

| `ensAlias` | `resolvedAddress` (source of truth) | `chainId` | `accountType` | `safeThreshold` | `status` | `allowedActions` | `forbiddenActions` | `controller` |
|---|---|---|---|---|---|---|---|---|
| `afidao.eth` | `0x4b02AC8E5551C30c4C92814F63D4576F335E4112` | `1` | `safe` | `1-of-1` | `active` (ENS admin) | own/manage ENS namespace; Snapshot admin | custody rewards/treasury; be resolved for on-chain access control | 1-of-1 Safe, signer `0xb87C…ad62` → **SHOULD move to N-of-M** |
| `treasury.afidao.eth` | `0x7408d8e97280e391A38DffE3AE8dF7E5c553438f` *(placeholder; **target → reconcile to** `0x1Dd6705…` on Base or a new Base treasury Safe)* | `1` → target `8453` | `safe` | `1-of-1` | `placeholder` | reserve the "treasury" alias for future use | be presented as the production treasury; receive funds pre-verification; share its address with grants/ops/liq | 1-of-1 Safe, signer `0xb87C…ad62` |
| `reserve.afidao.eth` | `0x4b02AC8E5551C30c4C92814F63D4576F335E4112` *(**collision** with root; **target → dedicated cold Safe**)* | `1` | `safe` | `1-of-1` | `placeholder` | reserve the "reserve" alias for future use | be a segregated reserve while it equals the admin Safe; hold reserves under a 1-of-1 hot signer | 1-of-1 Safe, signer `0xb87C…ad62` |
| `grants.afidao.eth` | `0x7408d8e97280e391A38DffE3AE8dF7E5c553438f` *(shared placeholder; **target → dedicated grants Safe**)* | `1` → target `8453` | `safe` | `1-of-1` | `placeholder` | reserve the "grants" alias for future use | share one address with treasury/ops/liq; mix grant budget with role rewards | 1-of-1 Safe, signer `0xb87C…ad62` |
| `ops.afidao.eth` | `0x7408d8e97280e391A38DffE3AE8dF7E5c553438f` *(shared placeholder; **target → dedicated ops Safe**)* | `1` → target `8453` | `safe` | `1-of-1` | `placeholder` | reserve the "ops" alias for future use | share one address with treasury/grants/liq; hold role rewards; be conflated with the deployer EOA | 1-of-1 Safe, signer `0xb87C…ad62` |
| `liq.afidao.eth` | `0x7408d8e97280e391A38DffE3AE8dF7E5c553438f` *(shared placeholder; **target → dedicated Base liquidity Safe**)* | `1` → target `8453` | `safe` | `1-of-1` | `placeholder` | reserve the "liq" alias for future use | share one address with treasury/grants/ops; be the reward/treasury vault; be conflated with the xERC20 lockbox | 1-of-1 Safe, signer `0xb87C…ad62` |
| *(none)* | `0x1Dd6705ff84Ecd5eaDc51A913Ad8e2c6C9E79aC4` | `8453` | `safe` | `1-of-1` | `verified` (real authority) | hold `DEFAULT_ADMIN_ROLE` + `EMISSIONS_ROLE`; be the canonical treasury referenced in `afi-config`; fund RewardsVault per epoch (post-hardening) | remain conflated with `treasury.afidao.eth`; remain 1-of-1 in production | 1-of-1 Safe, signer `0xb87C…ad62` → **SHOULD move to N-of-M + timelock** |
| *(legacy three-letter ENS alias, stale/wrong)* | `0x057302a507F41415DcC68A2C62D5b8abF207a20d` *(`smilefox.eth`, third party)* | `1` | `eoa` | `n/a` | `deprecated` (not AFI) | — none — | be used as the AFI governance/Snapshot space (real space is `afidao.eth`) | third party (not AFI-controlled) |

**Reading the DRAFT table:**
- The **real treasury authority** has **no ENS alias** today and lives on **Base (`8453`)** — the opposite of where `treasury.afidao.eth` points (empty L1 Safe). This is the §4 reconciliation gap, made explicit.
- Four lanes (`treasury`/`grants`/`ops`/`liq`) currently **collapse to one address**; `reserve` **collides with root**. The `forbiddenActions` column encodes the de-duplication law (§3).
- `1-of-1` everywhere is recorded as `safeThreshold` precisely so the §5 hardening obligation is visible per entry.
- the legacy three-letter ENS alias is included only to mark it **`deprecated` / not AFI** so it is never mistaken for the governance pointer (§6).

---

## 9. Conformance

A document, config, schema, or contract **conforms to this doctrine** if and only if:

1. It treats ENS names as aliases and concrete addresses (+ `chainId` + threshold + signer policy) as the source of truth (§2);
2. It does **not** resolve ENS dynamically for access control, routing, or authorization (R-3);
3. It does **not** present any current `afidao.eth` subname as a funded production vault (§3), and does **not** present `treasury.afidao.eth` as the real treasury (§4);
4. It uses `afidao.eth` (network 1) — **not** the legacy three-letter ENS alias — as the governance/Snapshot pointer in prescriptive material (§6);
5. Where it references any account, it carries (or links) a §7 registry entry with all nine fields.

Recon/audit artifacts that **describe** the v0/current ENS reality (including this doctrine's source recon) conform as long as they do not present that reality as the canonical intended future.

---

## 10. Related Documents

- [`./AFI_SETTLEMENT_V1_DOCTRINE.md`](./AFI_SETTLEMENT_V1_DOCTRINE.md) — the constitution (D7, D10, §11, §12, §15.5).
- [`./AFI_EPOCH_SETTLEMENT_MANIFEST.md`](./AFI_EPOCH_SETTLEMENT_MANIFEST.md) — Layer 3; manifest `chainId` + `contractAddresses` MUST reference verified registry entries.
- [`./AFI_REWARDS_VAULT_AND_CLAIMS.md`](./AFI_REWARDS_VAULT_AND_CLAIMS.md) — Layer 4; the RewardsVault/treasury accounts it funds MUST be verified registry entries (concrete addresses, hardened Safes).
- [`./AFI_V0_DEPRECATION_AND_MIGRATION.md`](./AFI_V0_DEPRECATION_AND_MIGRATION.md) — v0 posture; runtime-sensitive legacy-ENS-alias/placeholder items are owner-deferred there.
- **ADRs:** [`../adrs/ADR-005-ens-aliases-addresses-source-of-truth.md`](../adrs/ADR-005-ens-aliases-addresses-source-of-truth.md) (D7), [`../adrs/ADR-001-four-layer-settlement-architecture.md`](../adrs/ADR-001-four-layer-settlement-architecture.md) (D10).
- **Prior recon (descriptive, still accurate):** [`../../reports/afi-ens-vault-registry-recon.md`](../../reports/afi-ens-vault-registry-recon.md) and [`../../reports/afi-ens-vault-registry.draft.json`](../../reports/afi-ens-vault-registry.draft.json); supporting: [`../../reports/afi-onchain-contract-discovery.md`](../../reports/afi-onchain-contract-discovery.md), [`../../reports/afi-vault-architecture-recon.md`](../../reports/afi-vault-architecture-recon.md).

---

*Canonical doctrine. Defines the address/identity law only; it implements nothing on-chain and changes no ENS, Safe, role, or fund state. Concrete addresses + chainId + threshold + signer policy are the source of truth; ENS names are aliases. The current `afidao.eth` subnames are placeholder scaffolding pending an owner-verified concrete-address registry.*
