# AFI Rewards Vault and Claims
**Status:** CANONICAL — Accepted (v1 doctrine)
**Date:** 2026-06-24
**Part of:** AFI Settlement v1 — see [AFI_SETTLEMENT_V1_DOCTRINE.md](./AFI_SETTLEMENT_V1_DOCTRINE.md)  (for ADRs use ../adrs/)

---

## 0. Scope and Status of This Document

This spec defines **Layer 4** of the AFI Settlement v1 four-layer model (see doctrine §3): **vault-based reward custody, routing, and claiming**. It is **doctrine and design law only**. **Nothing here is implemented, deployed, or executed.** No contract described in this document exists on any chain. No funds move, no roles are granted, and no Safe state changes by virtue of this document. Field **encodings and Solidity types are implementation design**; this spec commits only to field **presence and meaning** and to the normative rules below. Where the constitution marks a question OPEN, this spec keeps it OPEN and defines nothing OPEN as final.

The RewardsVault is the **missing custodial seam** identified in the vault recon (`../../reports/afi-vault-architecture-recon.md`): AFI today mints **per signal, push, to a single beneficiary**, which is DEPRECATED and FORBIDDEN for v1 (doctrine §5, D9). This document specifies the layer that replaces it.

**Normative language** (MUST / MUST NOT / SHOULD / SHOULD NOT / MAY / OPEN) is used exactly as defined in doctrine §1.

---

## 1. Position in the Four-Layer Model

| Layer | Spec | Produces | Consumed here? |
|-------|------|----------|----------------|
| 1 — Per-signal provenance | [AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md](./AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md) | `signalRoot`, `evidenceRoot` | No (provenance only; never redeemable) |
| 2 — Strategy/epoch reputation | [AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md](./AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md) | ERC-6909 receipts (reputation) | No (reputation is not a payout unit) |
| 3 — Epoch settlement manifest | [AFI_EPOCH_SETTLEMENT_MANIFEST.md](./AFI_EPOCH_SETTLEMENT_MANIFEST.md) | `claimRoot`, `roleAllocationRoots`, `totalRewardPool`, policy refs | **Yes — the only authority the vault obeys** |
| 4 — **Rewards vault / claims (this doc)** | this | Custody of epoch budget; claims/routes | — |

**Layer separation laws this document is bound by (from doctrine §3):**

- **L-SEP-3 (MUST):** The manifest (Layer 3) is the **only** authority that decides who is owed what. The vault MUST NOT recompute eligibility or scores.
- **L-SEP-4 (MUST):** The RewardsVault MUST pay strictly against a committed manifest root and MUST NOT decide eligibility, mint, or pay outside that root.

The RewardsVault is **downstream** of the manifest and is **dumb on purpose**: it enforces, it does not decide.

---

## 2. The Three Vaults — Naming Law (MUST NOT Conflate)

The word "vault" is overloaded in the AFI codebase and recon. This spec is bound by the doctrine naming law (§7) and extends it. These are **three distinct objects** with distinct custody semantics. Docs, schemas, comments, and contracts MUST NOT use bare "vault" in a way that conflates them.

| Object | Custodies | Layer / role | Defined by | Reward authority? |
|--------|-----------|--------------|------------|-------------------|
| **RewardsVault** | **Reward tokens** (the per-epoch reward budget) | Layer 4 — this document | this spec | Pays **only** against committed `claimRoot`; **never mints**, **never decides** |
| **Canonical evidence store** (`afi.scored-signal-evidence.v2`, carrying a composition reference per afi-governance `decisions/factory-configurable-pipelines-v1.md`; `VaultedSignalRecord`) | **Data** (scored-signal evidence and lifecycle records) | Layer 1 support; off-chain (MongoDB) | doctrine §7; `afi-infra/src/evidence/*`, `afi-infra/src/tssd/*` | **None.** Holds zero tokens. Unchanged by Settlement v1. |
| **xERC20 bridge lockbox** (`XERC20Lockbox`) | **Canonical AFI for bridging** (mint/burn xAFI, rate-limited) | Token posture (doctrine §10) | doctrine §10; `afi-xerc20/.../XERC20Lockbox.sol` | **None for rewards.** Bridge custody only. |

**Naming MUST rules:**

- **N-1 (MUST):** "RewardsVault" / "TreasuryVault" refer to **token custody**. "TSSD vault" / "evidence vault" / `VaultedSignalRecord` refer to **data custody**.
- **N-2 (MUST NOT):** The TSSD evidence vault MUST NOT be repurposed, extended, or schema-overloaded to hold tokens, balances, or claims.
- **N-3 (MUST NOT):** The xERC20 bridge lockbox MUST NOT be repurposed as the reward or treasury vault (doctrine §10).
- **N-4 (MUST):** The RewardsVault and the **Base Treasury Vault** (Safe that funds it) are **separate objects**. The Treasury funds the RewardsVault per epoch; the RewardsVault holds per-epoch reward custody only and MUST NOT hold long-term protocol reserves.

---

## 3. What the RewardsVault Is and Is Not

| The RewardsVault **MUST** | The RewardsVault **MUST NOT** |
|---------------------------|-------------------------------|
| Custody the per-epoch reward budget after funding | **Mint** any token under any condition |
| Pay only against the committed manifest `claimRoot` for that `epochId` | **Decide eligibility, scores, or amounts** (that is Layer 3) |
| Enforce the per-epoch budget cap at the funding seam | Pay for an epoch in excess of that epoch's funded budget / `totalRewardPool` |
| Prevent double-claims (per §6) | Allow a leaf to be claimed twice |
| Support **proof-based pull** at minimum (§5.2) | Require trusting AFI private infrastructure to verify a claim |
| Honor pause, challenge window, and holdback policy refs from the manifest | Pay during pause or before a holdback/challenge window resolves |
| Trace every payout to `signal → manifest → claimRoot → claim` | Pay to an address not committed under the `claimRoot` (or its role allocation root) |

**Reward entitlement** is established **only** by inclusion in a committed `EpochSettlementManifest` `claimRoot` (doctrine §8). A provenance artifact (EAS attestation, signal leaf, ERC-6909 reputation receipt, or any v0 ERC-1155 receipt) MUST NOT be redeemable at the vault.

---

## 4. Funding Flow (Treasury → Vault)

Rewards are settled **per epoch** and funded **as a lump sum to the vault**, never to end users (doctrine §9).

### 4.1 Funding sequence (normative)

1. **Manifest committed (Layer 3).** A single `EpochSettlementManifest` for `epochId` is committed once, exposing `claimRoot`, `roleAllocationRoots`, `totalRewardPool`, `rulesetHash`, `challengeWindow`, `holdbackPolicyRef`, `unclaimedRewardPolicyRef`, `chainId`, `contractAddresses`. **MUST** precede funding.
2. **Authorization.** Funding **MUST** be authorized by the documented Treasury Safe / governance (doctrine §12–§13). An agent-submitted manifest **MUST** pass human/governance authorization before funding (doctrine §13).
3. **Fund the vault (mint or transfer).** The epoch reward budget is moved to the RewardsVault as a lump sum:
   - **MAY** be funded by **transfer** of already-existing AFI from the Treasury, **or**
   - **MAY** be funded by a **mint** performed by the authorized emissions authority (Treasury Safe / coordinator) **into** the vault.
   - **MUST NOT (V-MINT):** The **vault itself MUST NOT mint.** Any minting happens **outside** the vault, by the emissions authority, with the vault as recipient. The vault holds custody only.
4. **Bind budget to epoch.** Funding **MUST** record the funded amount against `epochId` and the committed `claimRoot`. The vault **MUST** treat `min(funded amount, totalRewardPool)` as the hard ceiling of payouts for that epoch (see §4.2).

### 4.2 Per-epoch budget enforcement (the seam) — MUST

- **B-1 (MUST):** The per-epoch budget cap is enforced **at the funding seam** (doctrine §9). The vault **MUST NOT** pay more, in aggregate for an epoch, than that epoch's funded budget.
- **B-2 (MUST):** The vault **MUST** account rewards **per `epochId`**. Funds funded for one epoch **MUST NOT** be claimable under another epoch's `claimRoot`.
- **B-3 (MUST):** Aggregate claims for an epoch **MUST NOT** exceed `totalRewardPool` declared in that epoch's manifest. If funded amount and `totalRewardPool` disagree, the vault **MUST** treat the **lower** as the ceiling and the discrepancy **MUST** surface as a settlement error (§9).
- **B-4 (MUST NOT):** The vault **MUST NOT** rely on the global token supply cap (the 86B `TOTAL_SUPPLY_CAP`) as its epoch budget control. The supply cap is a token invariant, not an epoch budget.

---

## 5. Claim / Distribution Flow

Both **push** (router) and **pull** (claims) are **permitted** (doctrine §6 O7, §15.4). The default mode (push vs. pull) is **OPEN** (O7). However:

- **D-PULL (MUST):** The vault **MUST** support **proof-based pull** (Merkle/manifest proof) as a minimum capability. A push-only design is non-conforming.
- **D-PUSH (MAY):** The vault **MAY** additionally support **manifest-backed routing** (push) of role allocations, provided every pushed payment is justified by the same committed roots and obeys §6 double-pay prevention and §7 holdbacks.

### 5.1 What a claim proves

A claim is valid **iff** the claimant presents a leaf that verifies as included under the epoch's committed root. The leaf binds at least:

- `recipient` (payout address — concrete address, source of truth; ENS MUST NOT be resolved by the vault, doctrine §11, D7),
- `role` (Provider | Analyst-Scorer | Validator | public-goods — see §11),
- `amount`,
- `epochId`.

These derive from the manifest's `claimRoot` and/or `roleAllocationRoots` (doctrine §15.3–§15.4). Exact leaf encoding is implementation design (OPEN); leaf **content (recipient, role, amount, epoch)** is required.

### 5.2 Pull claim sequence (normative — minimum required path)

1. Claimant (or anyone on the claimant's behalf — claims **MAY** be permissionlessly relayed to a fixed `recipient`) submits `(epochId, leaf, proof)`.
2. Vault verifies the proof against the **committed** `claimRoot` (or the relevant `roleAllocationRoots`) for `epochId`. Invalid proof → **revert / reject** (no state change).
3. Vault checks **not already claimed** (§6), **not paused** (§8), **challenge window satisfied / holdback released** (§7).
4. Vault marks the leaf claimed (§6) **before** transferring (effects-before-interactions) and transfers `amount` of the **already-custodied** reward token to `recipient`.
5. Vault emits a claim event binding `epochId`, leaf identifier, `recipient`, `role`, `amount` for auditability (every payout traces to `signal → manifest → claimRoot → claim`).

The vault **MUST NOT mint** in this path; it transfers only tokens it already custodies.

### 5.3 Push/route sequence (optional)

If routing is enabled, the vault (or an authorized distributor) **MAY** push each `roleAllocation` leaf to its committed `recipient`, subject to identical root verification, double-pay prevention, pause, holdback, and budget rules. Push **MUST NOT** be the **only** path (D-PULL).

---

## 6. Double-Claim Prevention

- **DC-1 (MUST):** The vault **MUST** prevent any leaf from being paid more than once. A claimed-state record (e.g. a **claimed bitmap** keyed by leaf index, or a **nullifier set** keyed by a leaf-derived identifier) **MUST** be maintained per `(epochId, leaf)`.
- **DC-2 (MUST):** Claimed-state **MUST** be scoped per `epochId`. The same `recipient`/`role` appearing in two epochs is two independent entitlements; a claim in one epoch MUST NOT mark the other claimed.
- **DC-3 (MUST):** The vault **MUST** mark a leaf claimed **before** the value transfer (checks-effects-interactions) so a reentrant or repeated call cannot double-pay.
- **DC-4 (MUST):** A failed transfer **MUST NOT** silently leave the leaf marked-claimed-but-unpaid; see failed-claim handling (§9).
- **DC-5 (SHOULD):** The claimed-state representation SHOULD be gas-efficient and verifiable from chain data (bitmap or nullifier mapping) so that "unclaimed vs claimed" is independently auditable per epoch.

Exact representation (bitmap vs. nullifier mapping) is implementation design; the **guarantee** (exactly-once per leaf per epoch) is doctrine.

---

## 7. Challenge Window, Holdbacks, and Vesting

The manifest carries `challengeWindow`, `holdbackPolicyRef`, and (where applicable) holdback/vesting references (doctrine §15.3). The vault **enforces** these references; it does not author the policy values.

- **CW-1 (SHOULD):** Distribution to role-holders **SHOULD** occur in the **epoch following** settlement, to allow challenge/holdback windows to apply (doctrine §9).
- **CW-2 (MUST):** The vault **MUST** honor the `challengeWindow` for an epoch: a claim against a leaf whose challenge window has not elapsed **MUST** be either rejected or held until the window closes, per the committed `holdbackPolicyRef`.
- **HB-1 (MUST):** Where `holdbackPolicyRef` specifies a withheld portion, the vault **MUST** release only the unwithheld portion until the holdback condition resolves, and **MUST NOT** release the withheld portion early.
- **HB-2 (OPEN):** The **holdback / vesting schedule** (size, duration, release curve) is **OPEN (O4)**. This spec defines the **hook** (`holdbackPolicyRef`) and the enforcement obligation; the **schedule values are OPEN** and MUST NOT be hard-coded as final.
- **CH-1 (MUST):** On a **successful challenge** within the window, the affected entitlement **MUST NOT** be paid (or, if held, **MUST NOT** be released). The disposition of the withheld/forfeited amount is **OPEN** — see §10 (clawback) and §12 (unclaimed policy). The vault **MUST NOT** declare a final destination for challenge-failed funds in v1.

---

## 8. Pause Behavior

- **P-1 (MUST):** The vault **MUST** support an emergency **pause** that halts claims/routing.
- **P-2 (MUST):** While paused, the vault **MUST NOT** transfer reward tokens out via the claim or route path. Read-only verification (proof checks, view of claimed-state) **MAY** remain available.
- **P-3 (MUST):** Pause authority **MUST** be held by the documented Safe / governance (doctrine §12). Pause **MUST NOT** be controllable by an agent (doctrine §13, D10).
- **P-4 (MUST):** Pause **MUST NOT** alter entitlements. On unpause, valid unclaimed leaves remain claimable (subject to §12 unclaimed policy). Pause is a halt, not a forfeiture.
- **P-5 (SHOULD):** Pause SHOULD be paired with the challenge mechanism: if a systemic challenge or manifest defect is discovered, governance SHOULD pause before funds drain.

---

## 9. Failed Claims and Settlement Errors

- **FC-1 (MUST):** If a value transfer fails (e.g. non-receiving `recipient`, token transfer revert), the vault **MUST** ensure the leaf is **not** left in a claimed-but-unpaid state — either the whole claim reverts atomically (preferred) or a recorded, re-claimable failure is created. A failed claim **MUST NOT** consume the entitlement.
- **FC-2 (MUST):** A proof that does not verify, an unknown `epochId`, or an over-budget condition **MUST** reject without state change (no partial pay, no marking claimed).
- **FC-3 (MUST):** A funding/manifest discrepancy (funded ≠ `totalRewardPool`, or aggregate claims would exceed the ceiling per §4.2) **MUST** surface as a settlement error and **MUST NOT** be silently absorbed by paying from another epoch's funds.
- **FC-4 (SHOULD):** The vault SHOULD expose enough event/state data that a failed or partial settlement is independently detectable and reconcilable per epoch.

---

## 10. Legal Clawback Status — OPEN (Doctrine O1)

- **CL-OPEN (MUST NOT):** This spec **MUST NOT** declare any specific clawback or escheatment policy as final. Legal **clawback / escheatment** of unclaimed or challenge-failed rewards — its mechanics, jurisdiction, triggers, and the custody of forfeited funds — is **OPEN (O1)** and **pending legal/compliance review** (doctrine §6, D8).
- **CL-HOOK (MAY):** A **clawback hook** (a governed administrative action that disposes of a defined, withheld/forfeited amount) **MAY** be referenced as a *placeholder seam*. Its **trigger conditions, recipient of forfeited funds, and legal basis are OPEN** and MUST NOT be implemented as if settled.
- **CL-SCOPE (OPEN):** Whether holdback/vesting/clawback are in scope for mainnet v1 **at all** is itself owner/legal-decided. This document defines the **enforcement seam** only, not the policy.

No paragraph in this document may be read as asserting a final clawback or escheatment rule.

---

## 11. Role Allocations (Split Values OPEN)

The manifest commits `roleAllocationRoots | roleAllocationLeaves` for the v1 role set. The vault pays each role's committed leaves against its root.

| Role | Meaning | Split value |
|------|---------|-------------|
| **Providers** | Producers of qualified signals (provenance `producer`) | **OPEN (O3)** |
| **Analysts / Scorers** | Enrichment / analysis / scoring contributors | **OPEN (O3)** |
| **Validators** | Validation / challenge participants | **OPEN (O3)** |
| public-goods (non-role budget) | Protocol public-goods share | **OPEN (O3)** — MAY be segregated to a separate Safe, not the RewardsVault |

- **R-1 (MUST):** The vault **MUST** support **at minimum** the three role categories **Providers**, **Analysts/Scorers**, and **Validators** as distinct allocation tracks committed by the manifest.
- **R-2 (OPEN):** The exact **split VALUES** across roles are **OPEN (O3)**. The research gauge in `afi-econ` (e.g. `params/gauge_v0.yaml`) is **not** final law and MUST NOT be hard-coded as the production split.
- **R-3 (MUST):** The vault **MUST NOT** compute role splits. Splits are decided upstream and committed in the manifest's role allocation roots/leaves. The vault enforces; it does not allocate.

---

## 12. Unclaimed Reward Policy — PLACEHOLDER (Value OPEN, O2)

- **UC-PLACEHOLDER (MUST):** The vault **MUST** read an `unclaimedRewardPolicyRef` from the committed manifest (doctrine §15.3). This is a **placeholder hook**.
- **UC-OPEN (OPEN):** The **policy value** — expiry window, and disposition of unclaimed funds (**recycle** to a later epoch vs. **roll-forward** vs. **return-to-treasury** vs. other) — is **OPEN (O2)**. This spec **defines nothing OPEN as final** and MUST NOT hard-code an expiry or destination.
- **UC-1 (MUST):** Until the policy is resolved by the owner (and, where legal/compliance is implicated, by O1), valid unclaimed entitlements **MUST** remain claimable (a claim is not silently voided by the absence of a policy).
- **UC-2 (MUST NOT):** Unclaimed funds **MUST NOT** be swept to any address as "final" disposition before O2 (and any O1 legal dependency) is resolved.

| Candidate disposition | Status |
|-----------------------|--------|
| Recycle into a later epoch budget | OPEN (O2) |
| Roll-forward as a standing claim | OPEN (O2) |
| Return to Treasury | OPEN (O2) |
| Escheat / legal forfeiture | OPEN (O1 — legal/compliance) |

---

## 13. Authority, Agent Boundary, and Address Source-of-Truth

- **A-1 (MUST):** Authority over the RewardsVault (fund, pause, configure, govern parameter changes) **MUST** be held by a documented Safe (ideally + timelock), with governance (Snapshot `afidao.eth` + Zodiac Reality where wired) gating parameter changes (doctrine §12).
- **A-2 (MUST NOT):** **Agents MUST NEVER** control the vault's funds, hold production keys, pause/unpause, change vault parameters, or perform upgrades (doctrine §13, D10). Agents MAY at most **submit** a manifest for human/governance authorization upstream.
- **A-3 (MUST):** The vault **MUST** treat **concrete address + chainId** as the source of truth for `recipient` and authority (doctrine §11, D7). The vault **MUST NOT** resolve ENS dynamically for access control or fund routing.
- **A-4 (MUST NOT):** 1-of-1 Safe control of the vault is **not production-grade** (doctrine §12); production authority MUST be N-of-M multisig + timelock (parameters OPEN, O8).

---

## 14. Conformance Checklist (Layer 4)

A vault design conforms to AFI Settlement v1 **iff** all of the following hold:

- [ ] Pays **only** against a committed manifest `claimRoot` / `roleAllocationRoots` for the matching `epochId` (L-SEP-4).
- [ ] **Never mints** (V-MINT); funded by Treasury transfer or external emissions-authority mint into the vault.
- [ ] **Never decides** eligibility, scores, or splits (L-SEP-3, R-3).
- [ ] Enforces the **per-epoch budget at the funding seam** (B-1…B-4).
- [ ] Supports **proof-based pull** at minimum (D-PULL); push permitted but not sole path.
- [ ] Prevents **double-claims** exactly-once per leaf per epoch (DC-1…DC-5), marking claimed before transfer.
- [ ] Honors **pause** (P-1…P-5), **challenge window**, and **holdback** refs (CW/HB) without authoring policy values.
- [ ] Handles **failed claims** without consuming entitlement (FC-1…FC-4).
- [ ] Declares **no final clawback/escheatment** policy (CL-OPEN, O1).
- [ ] Treats **unclaimed-reward policy** as a placeholder with **OPEN** value (UC, O2).
- [ ] Supports Providers / Analysts-Scorers / Validators tracks with **OPEN split values** (R-1, R-2, O3).
- [ ] Keeps RewardsVault distinct from the **TSSD evidence vault** (data) and the **xERC20 bridge lockbox** (bridge custody) (N-1…N-4).
- [ ] Authority is a documented Safe; **agents excluded** (A-1…A-4, D10).

---

## 15. Field Registry (this layer)

Per doctrine §15.4, this layer's fields. Encodings/types are implementation design; **presence and meaning** are doctrine.

| Field / artifact | Meaning | Notes |
|------------------|---------|-------|
| `epochId` | The epoch this funding/claim batch settles | Scopes budget and claimed-state |
| `claimRoot` | Committed Merkle root the vault pays against (from manifest) | The **only** payout authority (L-SEP-4) |
| `roleAllocationRoots \| roleAllocationLeaves` | Per-role (Provider/Analyst-Scorer/Validator/public-goods) allocation commitments | Split **values OPEN (O3)** |
| `totalRewardPool` | Declared epoch reward total (from manifest) | Hard ceiling with funded amount (B-3) |
| funded amount (per epoch) | Lump-sum moved to vault at funding seam | `min(funded, totalRewardPool)` is the cap (B-1) |
| claimed bitmap / nullifier set | Per-`(epochId, leaf)` claimed-state | Exactly-once guarantee (DC) |
| claim leaf `(recipient, role, amount, epochId)` | The unit a proof redeems | Encoding OPEN; content required (§5.1) |
| `challengeWindow` | Window before/while a leaf may be challenged | Enforced, not authored (CW) |
| `holdbackPolicyRef` | Reference to holdback/vesting policy | Schedule **OPEN (O4)** |
| `unclaimedRewardPolicyRef` | Reference to unclaimed-reward policy | **Placeholder; value OPEN (O2)** |
| clawback hook | Governed disposal of forfeited/withheld funds | **OPEN (O1)** — no final policy |
| pause state | Emergency halt flag | Safe/governance controlled (P-3) |

---

## 16. Related Documents

- [AFI_SETTLEMENT_V1_DOCTRINE.md](./AFI_SETTLEMENT_V1_DOCTRINE.md) — constitution (this doc obeys §3, §4 D1/D2/D6/D8/D9/D10, §7–§13, §15.4).
- [AFI_EPOCH_SETTLEMENT_MANIFEST.md](./AFI_EPOCH_SETTLEMENT_MANIFEST.md) — Layer 3; the sole authority this vault enforces.
- [AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md](./AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md) — Layer 2 reputation (not a payout instrument).
- [AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md](./AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md) — Layer 1 provenance (not redeemable).
- [AFI_ENS_SAFE_ADDRESS_REGISTRY_DOCTRINE.md](./AFI_ENS_SAFE_ADDRESS_REGISTRY_DOCTRINE.md) — concrete-address source of truth for vault authority/recipients.
- ADRs: [../adrs/ADR-004-rewards-vault-merkle-claims.md](../adrs/ADR-004-rewards-vault-merkle-claims.md) (vault/manifest claim layer), [../adrs/ADR-006-unclaimed-rewards-legal-clawback-open.md](../adrs/ADR-006-unclaimed-rewards-legal-clawback-open.md) (clawback/escheatment OPEN).
- Prior recon (descriptive): `../../reports/afi-vault-architecture-recon.md`.

---

*Canonical Layer-4 doctrine. Design and law only; implements nothing on-chain. The RewardsVault enforces the manifest — it does not mint and it does not decide. Clawback/escheatment (O1) and unclaimed-reward disposition (O2), holdback/vesting (O4), role splits (O3), and push-vs-pull default (O7) remain OPEN and MUST NOT be frozen as final by this document.*
