# ADR-003 — xERC20 Retained, ERC-7802 Deferred
**Status:** CANONICAL — Accepted (v1 doctrine)
**Date:** 2026-06-24
**Part of:** AFI Settlement v1 — see [AFI_SETTLEMENT_V1_DOCTRINE.md](../specs/AFI_SETTLEMENT_V1_DOCTRINE.md)

---

## Status

**Accepted — 2026-06-24.**

This ADR records two coupled, owner-approved Locked Decisions from the constitution:

- **D4 — xERC20 retained.** The AFI token MUST remain xERC20-compatible for v1.
- **D5 — ERC-7802 deferred.** v1 MUST NOT require ERC-7802 / SuperchainERC20; adoption is a future, separate decision.

This ADR does not implement, deploy, upgrade, wire, or re-wire any contract. It is **doctrine/design only**. It does not change the AFI token, its roles, its bridge minter limits, the `XERC20Lockbox`, or any deployed address. It states what the v1 token posture **is** so the repository stops drifting between "we are xERC20" and "we should be SuperchainERC20" without a recorded decision.

This ADR is **scoped to bridge / cross-chain token posture only.** It does not govern reward emission, settlement, or custody — those are owned by ADR-001 and ADR-004. The bridge token standard and the reward path are deliberately kept separate (see Decision §D-3 and L-SEP-1).

---

## Context

### The v0 reality being corrected

The deployed v0 stack on Base Sepolia conflates several concerns that v1 separates. The pieces relevant to *token posture* are:

- **`AFIToken` is already xERC20.** `AFIToken` inherits `XERC20` (`afi-token/src/AFIToken.sol`), which is the defi-wonderland xERC20 standard vendored in `afi-xerc20/`. The xERC20 surface gives per-bridge mint/burn **rate limits** (minter limits) and is the canonical cross-chain token standard the token was built against. This part of v0 is **sound** and is **retained**.
- **`XERC20Lockbox` exists but is UNWIRED.** The lockbox (`afi-xerc20/solidity/contracts/XERC20Lockbox.sol`) is the only true token-custody contract in the workspace, but it is a **bridge** lockbox — it holds canonical AFI to mint/burn the bridged representation across chains. It is **not** deployed for AFI and is **not** connected to the emissions stack. It is trivially mistaken for a reward/treasury vault; it is not one.
- **`XERC20Factory` is deployed on Base mainnet** at `0xb913bE186110B1119d5B9582F316f142c908fc25` (~35 KB bytecode). It is an **upstream bridge dependency**, not part of the AFI emissions stack, and its presence on mainnet does **not** mean any AFI token stack is live on mainnet (it is not — known AFI addresses have no bytecode on Base mainnet).
- **The reward path that is being deprecated is unrelated to the bridge standard.** v0 paid rewards through `AFIMintCoordinator.mintForSignal → AFIToken.mintEmissions(beneficiary, amount)`: **per-signal, single `beneficiary`, push-to-wallet at mint time**, optionally emitting an **`AFISignalReceipt` (ERC-1155)** in the same call. That path is deprecated as mainnet architecture (ADR-001, ADR-002), and **provenance is being decoupled from payout** (D2). None of that is a reason to change the *bridge token standard*. The xERC20 posture is orthogonal to, and survives, the deprecation of `mintForSignal`.
- **Governance / address hygiene context (carried by ADR-005, noted here for completeness).** v0 admin + emissions authority sits under a single **1-of-1 Safe**, and a stale Snapshot pointer (**the legacy, non-canonical three-letter ENS alias**) appears in places where the live governance space is `afidao.eth`. These are corrected elsewhere (ADR-005, `../specs/AFI_ENS_SAFE_ADDRESS_REGISTRY_DOCTRINE.md`); they are listed here only so this ADR is read against the true v0 baseline. **This ADR does not resolve them.**

### Why the question even arises

ERC-7802 (the `IERC7802` crosschain mint/burn interface, as used by **SuperchainERC20**) is an attractive newer pattern for native OP-Stack/Superchain interop: a single standardized `crosschainMint`/`crosschainBurn` surface callable by a canonical cross-chain messenger, no per-route lockbox, no per-minter rate-limit bookkeeping. Because AFI already lives on Base (an OP-Stack chain), there is a standing temptation to "just adopt SuperchainERC20." The codebase contains **no** ERC-7802 / SuperchainERC20 code today; adopting it would be a **new** dependency and a **new** trust/security model, not a refactor.

### The forces in tension

| Force | Pull toward xERC20 (retain) | Pull toward ERC-7802 (adopt now) |
|---|---|---|
| Existing code | Token already **is** xERC20; lockbox + factory vendored and (partly) deployed | None present; greenfield |
| Trust model | Per-bridge minter limits are explicit, auditable, owner-set | Trust delegated to the canonical Superchain messenger / predeploys |
| Maturity for AFI's needs | Battle-tested standard, broad bridge support | Newer; ecosystem and AFI's own integration are not yet proven for v1 |
| Scope of change | Zero token changes required for v1 | Token interface + deploy + cross-chain assumptions all change |
| v1 critical path | Settlement layers (1–4) are the priority, not bridging | Would inject bridge-standard risk into the v1 settlement milestone |

v1's priority is **getting Settlement (Layers 1–4) right** — provenance, manifest, vault, claims. The token's cross-chain standard is **not** on that critical path. Changing it now would add a new security surface and a new external dependency to a release whose whole point is to stop teaching the wrong architecture, for a benefit (Superchain-native interop) that v1 does not need.

---

## Decision

**D-1 (MUST) — Retain xERC20 for v1.**
The AFI token MUST remain **xERC20-compatible** for v1. The existing xERC20 posture (per-bridge mint/burn with explicit, owner-configured rate limits) is the canonical cross-chain token standard for AFI v1. No token-standard migration is part of the v1 scope.

**D-2 (MUST NOT) — Do not require ERC-7802 in v1.**
v1 MUST NOT **require** ERC-7802 / SuperchainERC20. No v1 doctrine, spec, schema, contract, or config may list ERC-7802 as a dependency or assume a SuperchainERC20 mint/burn surface. ERC-7802 MUST NOT be presented as a v1 dependency or as already-decided. Its adoption is **deferred** to a future, **separate** owner decision (a later ADR), to be taken on its own merits and timeline.

**D-3 (MUST) — Bridge custody is not reward custody.**
The `XERC20Lockbox` MUST NOT be repurposed as the reward vault or the treasury vault. The lockbox is **bridging** custody for the canonical token only. Reward custody is the **RewardsVault** (Layer 4, ADR-004); treasury custody is a **Safe** (ADR-005). The word "vault" MUST NOT be used in a way that conflates bridge custody, reward custody, and data/evidence custody (constitution §7, §10). This restates L-SEP-1 at the token layer: choosing or operating the bridge standard MUST NOT mint, escrow, or move any reward token.

**D-4 (MUST) — xERC20 retention does not re-bless the v0 reward path.**
Retaining the xERC20 token in no way retains, re-blesses, or reactivates `AFIMintCoordinator.mintForSignal`, `mintEmissions`-to-a-single-beneficiary, or the ERC-1155 `AFISignalReceipt` as the reward/receipt path. The token MAY be retained (constitution §14); the **per-signal push-to-wallet emission flow MUST NOT** be the v1 mainnet settlement path (ADR-001). v1 reward minting/funding flows **to the RewardsVault per epoch against a committed manifest root** (ADR-004), regardless of the token's bridge standard.

**D-5 (MUST) — Non-coupling of standards.**
The choice of bridge token standard (xERC20 vs. a future ERC-7802 decision) is **independent** of: the settlement model (epoch-batched, D1), the reputation receipt standard (ERC-6909, ADR-002), and the address/Safe source-of-truth (ADR-005). A future move to ERC-7802 — if ever taken — MUST NOT silently change any of those, and MUST NOT be smuggled in as a side effect of a bridge upgrade.

### What this decision does and does not touch

| Item | v1 posture under this ADR |
|---|---|
| `AFIToken` xERC20 inheritance | **Retained** — unchanged, canonical for v1 |
| Per-bridge mint/burn rate limits (minter limits) | **Retained** — explicit, owner-configured, auditable |
| `XERC20Lockbox` (bridge custody) | **Retained as a bridge primitive only**; MUST NOT become reward/treasury vault; not required to be wired for v1 |
| `XERC20Factory` (`0xb913bE18…`, Base mainnet) | Acknowledged as an **upstream bridge dependency**; not the AFI emissions stack |
| ERC-7802 / SuperchainERC20 | **Deferred** — MUST NOT be a v1 requirement; future separate ADR |
| `AFIMintCoordinator.mintForSignal` / push emission | **Deprecated** as mainnet reward path (ADR-001); not affected/protected by retaining xERC20 |
| Reward emission / settlement standard | **Out of scope here** — owned by ADR-001 / ADR-004 |

---

## Consequences

### Positive

- **Zero token-standard churn on the v1 critical path.** v1 ships Settlement Layers 1–4 without also taking on a bridge-standard migration and its audit/security cost.
- **Explicit, auditable cross-chain trust.** xERC20 minter rate limits are owner-set and inspectable per bridge, rather than delegated wholesale to a canonical messenger.
- **No new external dependency or trust assumption** is introduced into a release whose purpose is to *reduce* architectural ambiguity.
- **Clear separation preserved.** Bridge custody (lockbox), reward custody (RewardsVault), treasury custody (Safe), and data custody (TSSD evidence vault) stay distinct (D-3; constitution §7, §10).

### Negative / costs

- **No native Superchain interop in v1.** AFI forgoes the ergonomics of SuperchainERC20 (single standardized crosschain mint/burn, no per-route lockbox) until a future decision. If/when AFI wants deep OP-Stack-native interop, that work is still ahead.
- **Lockbox/factory must be operated and audited as bridge infrastructure** if bridging is exercised — i.e., AFI continues to own per-bridge rate-limit configuration and lockbox custody as an operational surface.
- **Standing temptation remains.** Because AFI is on Base, contributors may keep proposing ERC-7802; this ADR exists precisely to make that a *deliberate future ADR* rather than ambient drift.

### Neutral / obligations

- Docs, schemas, configs, and contract comments MUST NOT list ERC-7802 as a v1 requirement. References that imply SuperchainERC20 is "the plan" MUST be corrected to "deferred — see ADR-003."
- The `XERC20Lockbox` MUST be labelled as bridge custody wherever it appears, never as a reward or treasury vault.
- Any future ERC-7802 adoption MUST come as a new ADR that explicitly addresses migration, messenger trust, rate-limit equivalence, and L-SEP-1 (no coupling to reward flow), and that supersedes D5 in the constitution via Change Control (§17).

---

## Alternatives considered

**A1 — Adopt ERC-7802 / SuperchainERC20 now (rejected).**
Migrate `AFIToken` to the `IERC7802` crosschain mint/burn surface for native Superchain interop in v1.
*Rejected:* introduces a new external standard, a new trust model (delegation to the canonical cross-chain messenger/predeploys), and a token-interface change — all onto the v1 settlement critical path, for interop v1 does not need. It would also re-open audit scope on the token at exactly the moment v1 is trying to stabilize architecture. This is a legitimate **future** decision, not a v1 one.

**A2 — Run both xERC20 and ERC-7802 simultaneously (rejected for v1).**
Keep xERC20 and *also* implement the ERC-7802 surface so AFI is "future-proof."
*Rejected:* dual cross-chain mint/burn surfaces multiply the attack surface and the rate-limit/accounting reconciliation burden, with two independent paths to mint the same token. Strictly worse than A1 on risk; deferred wholesale.

**A3 — Drop cross-chain posture entirely; single-chain ERC-20 for v1 (rejected).**
Strip xERC20 and ship a plain single-chain ERC-20, re-adding bridging later.
*Rejected:* the token already **is** xERC20 and the standard is sound; ripping it out is gratuitous churn with no v1 benefit, and would itself be a token change requiring re-audit. Retention is the lower-risk path.

**A4 — Repurpose `XERC20Lockbox` as the reward/treasury vault (rejected, explicitly forbidden).**
Use the existing lockbox as the place rewards accrue, since it is "the one custody contract that exists."
*Rejected and prohibited (D-3):* the lockbox is bridging custody with bridge semantics; using it for rewards would re-conflate provenance/payout/bridge concerns the v1 doctrine exists to separate (constitution §7, §10; L-SEP-1).

**A5 (chosen) — Retain xERC20, defer ERC-7802 to a separate future ADR.**
Keep the proven, already-integrated standard; record ERC-7802 as an explicit, deferred, future decision rather than ambient drift.

---

## Open questions

These are **OPEN**. They MUST NOT be implemented as final.

- **Q1 — When, if ever, to revisit ERC-7802.** No trigger condition is fixed here (e.g., "when ≥N OP-Stack deployments are live" or "when Superchain interop is GA and audited"). Any revisit is a **future, separate** owner decision via a new ADR. Defining the trigger is **OPEN**.
- **Q2 — Reserve / lockbox topology.** Whether an L1 reserve vault exists at all, and whether reserves bridge via the existing lockbox, is **OPEN** (constitution O5). This ADR neither requires nor forbids it; it only forbids repurposing the lockbox as a *reward/treasury* vault.
- **Q3 — Bridge rate-limit parameters and authorized minters.** Concrete minter limits, the set of authorized bridges, and who configures them are **owner / operational parameters** (related to constitution O8 / Safe topology, ADR-005). Not settled here.
- **Q4 — Migration mechanics if ERC-7802 is ever adopted.** Coexistence vs. cut-over, messenger-trust assumptions, and rate-limit equivalence are deferred to that future ADR. **OPEN.**

Nothing in this section is to be treated as decided.

---

## Related docs

- **Constitution:** [`../specs/AFI_SETTLEMENT_V1_DOCTRINE.md`](../specs/AFI_SETTLEMENT_V1_DOCTRINE.md) — see §4 (D4, D5), §10 (Token Posture — xERC20 Retained, ERC-7802 Deferred), §7 (vault naming law), §14 (v0 migration posture).
- **Spec — ENS/Safe & address source of truth:** [`../specs/AFI_ENS_SAFE_ADDRESS_REGISTRY_DOCTRINE.md`](../specs/AFI_ENS_SAFE_ADDRESS_REGISTRY_DOCTRINE.md) — concrete addresses (incl. `XERC20Factory` `0xb913bE18…`) as the source of truth; legacy non-canonical ENS alias → `afidao.eth` correction.
- **Spec — Rewards vault & claims (Layer 4):** [`../specs/AFI_REWARDS_VAULT_AND_CLAIMS.md`](../specs/AFI_REWARDS_VAULT_AND_CLAIMS.md) — the actual reward custody, distinct from the bridge lockbox.
- **Spec — v0 deprecation & migration:** [`../specs/AFI_V0_DEPRECATION_AND_MIGRATION.md`](../specs/AFI_V0_DEPRECATION_AND_MIGRATION.md) — `AFIToken`/xERC20 MAY be retained; `mintForSignal` MUST NOT be the v1 path.
- **ADR-001 — Epoch settlement / provenance ≠ payout / agent boundary:** [`./ADR-001-four-layer-settlement-architecture.md`](./ADR-001-four-layer-settlement-architecture.md) — deprecates the `mintForSignal` reward path that this ADR does **not** re-bless.
- **ADR-002 — ERC-6909 reputation receipts:** [`./ADR-002-erc6909-strategy-epoch-receipts.md`](./ADR-002-erc6909-strategy-epoch-receipts.md) — independent of the bridge token standard (D-5).
- **ADR-004 — RewardsVault + manifest-backed claim/route:** [`./ADR-004-rewards-vault-merkle-claims.md`](./ADR-004-rewards-vault-merkle-claims.md) — reward custody that the lockbox MUST NOT become.
- **ADR-005 — ENS aliases vs. concrete-address source of truth / Safe hardening:** [`./ADR-005-ens-aliases-addresses-source-of-truth.md`](./ADR-005-ens-aliases-addresses-source-of-truth.md).

**Prior recon (descriptive, still accurate):** `../../reports/afi-vault-architecture-recon.md` (V4 — xERC20 Lockbox, UNWIRED), `../../reports/afi-onchain-contract-discovery.md` (`XERC20Factory` deployed; no AFI stack on mainnet), `../../reports/smart-contract-inventory.md` (vendored `afi-xerc20` bridge dependency).
