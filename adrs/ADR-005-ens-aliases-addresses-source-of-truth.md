# ADR-005 — ENS Names as Aliases, Addresses as Source of Truth

**Status:** CANONICAL — Accepted (v1 doctrine)
**Date:** 2026-06-24
**Part of:** AFI Settlement v1 — see [AFI_SETTLEMENT_V1_DOCTRINE.md](../specs/AFI_SETTLEMENT_V1_DOCTRINE.md)

---

## Status

**Accepted — 2026-06-24.**

This ADR records Locked Decision **D7** of the AFI Settlement v1 constitution: *ENS names are aliases; concrete addresses are the source of truth.* It also carries the governance-pointer and treasury-reconciliation laws of constitution §11 and the Safe-hardening principles of §12. It does **not** implement, deploy, mutate ENS records, change Safe ownership/threshold, grant roles, or move funds. It is doctrine and design law only.

This ADR is **scoped to identity and authorization source-of-truth**. The full ENS → address → chain → Safe → action registry shape is specified in the sibling spec [AFI_ENS_SAFE_ADDRESS_REGISTRY_DOCTRINE.md](../specs/AFI_ENS_SAFE_ADDRESS_REGISTRY_DOCTRINE.md); this ADR states *why* addresses (not names) are authoritative and *what* contracts/configs/governance MUST therefore do.

---

## Context

### The v0 reality this ADR corrects

AFI's v0 prototype and its supporting documents made identity and authorization assumptions that are **wrong as v1 mainnet architecture**. The recon that grounds this ADR ([afi-ens-vault-registry-recon.md](../../reports/afi-ens-vault-registry-recon.md), [afi-onchain-contract-discovery.md](../../reports/afi-onchain-contract-discovery.md)) established the following live facts as of 2026-06-24:

1. **The reward path conflated provenance with payout.** v0's `AFIMintCoordinator.mintForSignal` → `AFIToken.mintEmissions(beneficiary, amount)` minted per signal, to a single `beneficiary`, push-to-wallet at mint time, and emitted an **`AFISignalReceipt` (ERC-1155)** in the same act. That entangling of *who produced a truth* with *who gets paid* is deprecated as mainnet architecture (constitution §5, §8; ADR-001). It is named here because the same prototype that minted per signal is the prototype that anchored its trust in the wrong identity assumptions this ADR fixes.

2. **A single 1-of-1 Safe holds admin + emissions authority.** The real AFI Treasury Safe on **Base** — `0x1Dd6705ff84Ecd5eaDc51A913Ad8e2c6C9E79aC4` — holds `DEFAULT_ADMIN_ROLE` + `EMISSIONS_ROLE`, is **threshold 1**, and is signed by the single operator key `0xb87C647a1a0857a4f96271F1d9846fd470e4ad62`. That same key is the **sole 1-of-1 signer** of the two Ethereum-mainnet `afidao.eth` Safes as well. One hot key controls the entire ENS namespace **and** the Base treasury/emissions authority. This is a single point of failure, not a custody architecture.

3. **The repo's only ENS reference (the legacy non-canonical three-letter ENS alias) is stale and mis-pointed.** Repo configs hard-code `snapshotSpaceId: 'afidao.eth'` (e.g. `afi-config/schemas/validatorConfig.schema.json`, `afi-mint/src/orchestrator/types.ts` `DEFAULT_VALIDATOR_CONFIG`, `afi-governance/schemas/SignalChallengeProposal.schema.json`). But **no Snapshot space under the legacy three-letter ENS alias exists**, and that legacy ENS name is owned by an **unrelated third party** (`smilefox.eth`, `0x057302a5…a20d`). The **live** AFI DAO Snapshot/governance space is **`afidao.eth`** (network `1`), which the repo never references.

4. **`treasury.afidao.eth` is a placeholder, not the real treasury.** `treasury.afidao.eth` resolves to an **empty, never-used Ethereum-mainnet Safe `0x7408d8e97280e391A38DffE3AE8dF7E5c553438f`** (0 ETH, 0 value tokens, zero executed transactions). The same empty L1 Safe also backs `grants.afidao.eth`, `ops.afidao.eth`, and `liq.afidao.eth`. Meanwhile the **real** authority Safe (`0x1Dd6705…`) on **Base** has **no ENS name resolving to it at all**. Anyone who trusted ENS as canonical would route treasury, grants, ops, and liquidity to one empty placeholder on the wrong chain.

### Why ENS cannot be the on-chain source of truth

The same recon documents the structural reasons ENS subnames are unsafe as on-chain trust anchors:

- **ENS bindings are mutable.** All five `afidao.eth` subnames have **fuses `0`, expiry `0`** — they are **not emancipated**. The parent owner (`0x4b02AC8E…4112`, itself a 1-of-1 Safe) can **silently rewrite or replace** any subname's address record at any time. A contract that resolved `treasury.afidao.eth` for fund routing would follow whatever address that key most recently wrote.
- **The root name can lapse.** `afidao.eth` expires **2026-12-01** and has **not** burned `CANNOT_UNWRAP`; the owner can still unwrap/transfer. A name that can expire or be transferred is not an authorization primitive.
- **Resolution is an external, dynamic dependency.** ENS resolution at access-control time adds an off-chain/registry read into the trust path of every privileged action, expands the attack surface (resolver compromise, CCIP off-chain resolvers, registry reorg), and breaks the determinism a settlement system requires.
- **The namespace is L1; AFI executes on Base.** Every `afidao.eth` address record is Ethereum-mainnet (coinType 60); the protocol and its treasury authority live on **Base**. No ENS name carries a Base address. Name-based resolution does not even point at the chain where settlement happens.
- **The namespace is invisible to the repo.** Grep across all 28 repos returns **zero** references to `afidao.eth`, any subname, or the resolved Safe addresses. The names and the code are disconnected; treating names as authoritative would import an unverified, undocumented dependency.

The conclusion is forced: **ENS gives human-readable labels and intent; it does not give authoritative, immutable, chain-correct identity.** Authority must rest on the concrete addresses, chain IDs, and Safe policy that the names merely point at.

This ADR exists so the repository stops teaching the legacy three-letter ENS alias as governance, stops teaching `treasury.afidao.eth` as the treasury, and stops any future contract from resolving ENS to decide who is paid or who may act.

---

## Decision

The following are **v1 law** (constitution D7, §11, §12). They are normative.

### 1. Addresses are authoritative; ENS names are aliases only

- **D7.1 (MUST):** **Concrete addresses + `chainId` + Safe `safeThreshold` + signer policy** are the **source of truth** for contracts, configs, governance, and settlement. Every authorization, fund-routing, and parameter decision MUST be made against a concrete `resolvedAddress` on a named `chainId`, never against a name.
- **D7.2 (MUST):** ENS names (`afidao.eth` and its subnames `treasury` / `reserve` / `grants` / `ops` / `liq`) are **human-readable aliases only**. They MAY appear in documentation, dashboards, and off-chain operator tooling as labels, and MAY appear in a registry **only as the `ensAlias` field beside an authoritative `resolvedAddress`**.

### 2. Contracts MUST NOT resolve ENS for authority

- **D7.3 (MUST NOT):** Contracts MUST NOT resolve ENS **dynamically** for **access control**, **fund routing**, or **authorization**. Privileged roles, recipient addresses, vault targets, and signer/owner checks MUST be configured as concrete addresses, not as names resolved at execution time.
- **D7.4 (MUST NOT):** No contract in any v1 layer (Layer 1 provenance anchor, Layer 4 RewardsVault, the SettlementCoordinator, the bridge `XERC20Lockbox`) may take an ENS name, namehash, or resolver call result as an input that decides who is paid, who may pay, or who may change parameters.
- **D7.5 (MAY):** If a name-to-address mapping is ever needed on-chain (it is **not** required for v1), it MUST be a **manually curated, owner-set immutable mapping** committed as concrete addresses — never a live registry/resolver lookup. Resolving the live ENS registry in the authorization path remains prohibited (D7.3).

### 3. Configs and governance treat (address + chainId) as canonical

- **D7.6 (MUST):** Configuration files, deployment manifests, and the `EpochSettlementManifest` `contractAddresses` / `chainId` fields (Layer 3) MUST carry **concrete addresses and chain IDs** as the binding values. Any ENS string present is decorative and non-binding.
- **D7.7 (MUST):** A **concrete-address registry** (the [ENS/Safe registry](../specs/AFI_ENS_SAFE_ADDRESS_REGISTRY_DOCTRINE.md), entry shape `ensAlias`, `resolvedAddress`, `chainId`, `accountType`, `safeThreshold`, `status`, `allowedActions`, `forbiddenActions`, `controller`) MUST exist and be reconciled **before** any settlement contract references any account. No settlement contract may reference an account that is not a registry entry with `status` confirmed.

### 4. Governance-pointer law — `afidao.eth` (legacy ENS alias deprecated)

- **D7.8 (MUST):** The live AFI DAO Snapshot/governance space is **`afidao.eth`** (network `1`). Docs and examples MUST use `afidao.eth` for any governance reference.
- **D7.9 (MUST NOT):** References to **the legacy non-canonical three-letter ENS alias** as the Snapshot/governance space are **stale/incorrect** and MUST NOT be presented as canonical. That legacy alias is owned by an **unrelated third party** and resolves to **no existing Snapshot space**; it MUST NOT be trusted as AFI-controlled.
- **D7.10 (runtime-sensitive — owner-deferred):** Runtime config that historically carried the legacy three-letter ENS alias (the `snapshotSpaceId` defaults and examples noted in Context) is **runtime-sensitive** and is **owner-deferred** per [AFI_V0_DEPRECATION_AND_MIGRATION.md](../specs/AFI_V0_DEPRECATION_AND_MIGRATION.md). This ADR corrects the **doctrine**; it does **not** authorize editing live config during doctrine work. Correcting the pointer in config is a separate owner-approved change.

### 5. Treasury-reconciliation law — placeholder ≠ real treasury

- **D7.11 (MUST NOT):** `treasury.afidao.eth` currently resolves to an **empty placeholder Safe** (`0x7408d8e97280e391A38DffE3AE8dF7E5c553438f`, Ethereum mainnet) and MUST NOT be presented or wired as the production treasury. The same prohibition applies to `grants` / `ops` / `liq`, which collapse to that **same** empty L1 Safe, and to `reserve.afidao.eth`, which collapses to the **root/admin** Safe (`0x4b02AC8E…4112`).
- **D7.12 (MUST):** The **real** Base Treasury Safe `0x1Dd6705ff84Ecd5eaDc51A913Ad8e2c6C9E79aC4` (holder of `DEFAULT_ADMIN_ROLE` + `EMISSIONS_ROLE`) MUST be reconciled into the concrete-address registry as the authoritative treasury account, and the currently-collapsed lanes MUST be **de-duplicated** to distinct accounts, **before** any settlement contract references a treasury, reserve, grants, ops, or liquidity account. The exact target topology (re-point ENS vs. mint new Base Safes) is owner-decided.

### 6. Safe / signer policy is part of the source of truth

- **D7.13 (MUST NOT):** **1-of-1 Safe control is not production-grade.** Treasury, reserve, and settlement authority MUST NOT remain under a single 1-of-1 Safe (current `safeThreshold = 1`, sole signer `0xb87C…ad62`) for mainnet v1.
- **D7.14 (SHOULD):** Production authority SHOULD be an **N-of-M multisig + timelock**, with a documented signer roster and threshold recorded in the registry (`safeThreshold`, `controller`). The exact N-of-M parameters, signer set, and timelock delay are **OPEN** owner decisions (constitution O8).
- **D7.15 (MUST):** Authority over the SettlementCoordinator / RewardsVault MUST be a documented Safe (ideally + timelock); parameter changes are gated by governance at **`afidao.eth`** (Snapshot `afidao.eth` + Zodiac Reality where wired).

### 7. Agent boundary (identity dimension)

- **D7.16 (MUST NOT):** Agents MUST NEVER hold or change Safe roles/thresholds, hold production private keys, or be configured as authoritative addresses in the registry with custody/upgrade `allowedActions`. Agents MAY be referenced by alias for *submission* permissions only; their concrete address (if any) MUST carry `forbiddenActions` covering treasury control, key custody, upgrades, role changes, and deployments (constitution §13, ADR-001).

---

## Consequences

### Positive

- **Authorization is deterministic and auditable.** Every privileged action resolves to a fixed address on a fixed chain that an auditor can verify on-chain without trusting a mutable name or an external resolver.
- **The legacy ENS alias trap is closed in doctrine.** Governance references converge on the real space (`afidao.eth`), removing the risk that proposals, challenges, or validator configs point at a non-existent, third-party-owned space.
- **The treasury-misroute trap is closed in doctrine.** No conforming doc or contract may treat the empty L1 placeholder as the treasury; the real Base authority Safe is named as the thing that MUST be reconciled.
- **Centralization is named, not hidden.** 1-of-1 control is explicitly declared non-production-grade, forcing an N-of-M + timelock decision before mainnet, instead of shipping a single hot key as if it were custody.
- **Names stay useful where they are safe.** ENS remains a convenient human alias in docs and tooling, without leaking into the trust path.

### Negative / costs

- **More configuration surface.** Operators and contracts must carry concrete addresses + chain IDs (and keep them current across redeployments) rather than a single readable name. This is the intended cost: explicitness over convenience.
- **A registry must be built and maintained.** D7.7 makes the concrete-address registry a precondition for settlement contracts; building and owner-verifying it is required work before contract wiring.
- **Reconciliation work is owner-gated and not yet done.** De-duplicating the collapsed lanes, re-pointing/replacing the treasury account, and standing up N-of-M + timelock are owner actions (runtime-sensitive); this ADR creates the obligation but does not perform it.
- **Possible drift between alias and address.** Because ENS bindings are mutable, a name shown in docs could diverge from the authoritative address. Mitigation: the registry's `resolvedAddress` is canonical and the `ensAlias` is explicitly non-binding; periodic reconciliation is an operational duty.

### Conformance impact

- A doc, schema, comment, or contract that resolves ENS for access control or fund routing, that presents the legacy three-letter ENS alias as governance, or that presents `treasury.afidao.eth` (or the collapsed lanes) as the production treasury, **does not conform** to v1 (constitution §16) and MUST be corrected or banner-deprecated. Runtime config carrying these values is owner-deferred (D7.10), not edited under this ADR.

---

## Alternatives considered

| Alternative | Why rejected |
|---|---|
| **A1 — Resolve ENS on-chain for access control / routing** | ENS subnames here are mutable (fuses `0`, expiry `0`); the parent key can silently rewrite any binding, the root can lapse (`2026-12-01`), and resolution injects an external dynamic dependency and an L1/Base chain mismatch into every privileged action. This is exactly the trust anchor a settlement system must not have. Rejected (codified as the D7.3 prohibition). |
| **A2 — Treat the legacy three-letter ENS alias as the governance space (status quo in repo config)** | The legacy three-letter ENS alias resolves to no Snapshot space and is owned by an unrelated third party (`smilefox.eth`). Trusting it would point governance at a non-existent, non-AFI space. Rejected (D7.8–D7.9). |
| **A3 — Treat `treasury.afidao.eth` (and the collapsed lanes) as the real treasury** | It is an empty, never-used L1 Safe on the wrong chain; the real authority Safe is `0x1Dd6705…` on Base with no ENS name. Wiring the alias would misroute treasury/grants/ops/liquidity to one empty placeholder. Rejected (D7.11–D7.12). |
| **A4 — Keep 1-of-1 Safe control for mainnet v1** | A single hot key (`0xb87C…ad62`) signing all three Safes is a single point of failure, not custody. Rejected for production (D7.13); N-of-M + timelock is the direction (D7.14, parameters OPEN). |
| **A5 — Names-only (no concrete-address registry)** | Without an authoritative `resolvedAddress`/`chainId`/`safeThreshold` registry, there is no stable thing for contracts/configs to reference, and the L1/Base mismatch and lane collapse stay invisible. Rejected; the registry is mandatory (D7.7). |
| **A6 — Emancipate/lock ENS subnames and then trust them on-chain** | Burning fuses would reduce *mutability*, but ENS would still be an external dependency, still L1, still lapse-on-expiry, and still not the source of truth a deterministic settlement layer needs. Hardening names is at best defense-in-depth for the *alias* layer; it does not make names authoritative. Rejected as a basis for authority. |

---

## Open questions

These are **OPEN** (constitution §6). They MUST NOT be implemented as final until owner-resolved.

- **OQ-1 (→ O8) — Production Safe topology.** Exact N-of-M threshold, signer roster, and timelock delay for treasury / reserve / settlement authority. The *principle* (not 1-of-1; addresses + policy are truth) is locked; the *parameters* are owner decisions.
- **OQ-2 — Treasury target topology.** Whether to **re-point** `treasury.afidao.eth` to the real Base authority Safe (`0x1Dd6705…`) or stand up a **new dedicated Base treasury Safe**, and how to de-duplicate `grants` / `ops` / `liq` / `reserve` into distinct accounts. Owner-decided; this ADR only mandates reconciliation (D7.12).
- **OQ-3 — Chain alignment of the namespace.** Whether ENS aliases should carry Base (ENSIP-11) address records to match where AFI executes, or remain L1 labels with the registry holding the authoritative Base addresses. Either is consistent with this ADR (names are non-binding); the operational choice is OPEN.
- **OQ-4 — `afidao.eth` renewal.** The root name expires **2026-12-01**; whether/when to renew is an operational owner decision. Lapse does not affect authority (addresses are the source of truth) but would break the alias layer.
- **OQ-5 — Runtime correction of the legacy ENS alias pointer.** *When* and *how* the runtime `snapshotSpaceId` defaults/examples are corrected to `afidao.eth` is owner-deferred (D7.10); the doctrine correction is settled here.
- **OQ-6 — On-chain alias mapping.** Whether any owner-set immutable name→address mapping is ever published on-chain for convenience (D7.5). Not required for v1; live-registry resolution remains prohibited regardless.

---

## Related docs

**Constitution:**
- [AFI_SETTLEMENT_V1_DOCTRINE.md](../specs/AFI_SETTLEMENT_V1_DOCTRINE.md) — v1 constitution (this ADR records D7; see §11 ENS/address law, §12 Safe hardening, §13 agent boundary, §6 O8).

**Specs (this set):**
- [AFI_ENS_SAFE_ADDRESS_REGISTRY_DOCTRINE.md](../specs/AFI_ENS_SAFE_ADDRESS_REGISTRY_DOCTRINE.md) — the concrete-address registry shape this ADR makes mandatory (D7.7).
- [AFI_EPOCH_SETTLEMENT_MANIFEST.md](../specs/AFI_EPOCH_SETTLEMENT_MANIFEST.md) — Layer 3; carries authoritative `chainId` + `contractAddresses` (D7.6).
- [AFI_REWARDS_VAULT_AND_CLAIMS.md](../specs/AFI_REWARDS_VAULT_AND_CLAIMS.md) — Layer 4; funded by the reconciled treasury authority, MUST NOT resolve ENS (D7.4).
- [AFI_V0_DEPRECATION_AND_MIGRATION.md](../specs/AFI_V0_DEPRECATION_AND_MIGRATION.md) — runtime-sensitive legacy ENS alias config and Safe state are owner-deferred (D7.10).

**Sibling ADRs:**
- [ADR-001](./ADR-001-four-layer-settlement-architecture.md) — epoch settlement, provenance ≠ payout, agent boundary (D1, D2, D10).
- [ADR-004](./ADR-004-rewards-vault-merkle-claims.md) — RewardsVault + manifest-backed claim/route layer (D6).
- [ADR-006](./ADR-006-unclaimed-rewards-legal-clawback-open.md) — OPEN legal clawback/escheatment (D8).

**Prior recon (descriptive, still accurate):**
- [afi-ens-vault-registry-recon.md](../../reports/afi-ens-vault-registry-recon.md) — ENS namespace, the two empty L1 Safes, the collapsed lanes, the 1-of-1 signer, the legacy ENS alias vs `afidao.eth` discrepancy.
- [afi-onchain-contract-discovery.md](../../reports/afi-onchain-contract-discovery.md) — real Base Treasury Safe `0x1Dd6705…`, roles, v0 contracts.

---

*Canonical ADR. Records Locked Decision D7 of AFI Settlement v1. This document defines identity/authorization law and design only; it implements nothing on-chain, mutates no ENS or Safe state, and moves no funds. Concrete on-chain addresses cited are observed recon facts as of 2026-06-24, not deployment instructions.*
