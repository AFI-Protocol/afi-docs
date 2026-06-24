# ADR-006 — Unclaimed Rewards and Legal Clawback Remain Open
**Status:** CANONICAL — Accepted (v1 doctrine)
**Date:** 2026-06-24
**Part of:** AFI Settlement v1 — see [AFI_SETTLEMENT_V1_DOCTRINE.md](../specs/AFI_SETTLEMENT_V1_DOCTRINE.md)

---

## Status

**Accepted — 2026-06-24.**

This ADR records the locked decision that AFI's **unclaimed-reward policy** and its **legal clawback / escheatment mechanics** are **deliberately OPEN** for Settlement v1. It locks the *meta-decision* ("this stays open, and here is how the architecture must behave while it is open"), not the policy values themselves. It maps to **Locked Decision D8** and to **Open Questions O1 and O2** in the constitution (`AFI_SETTLEMENT_V1_DOCTRINE.md` §4, §6).

This ADR does **not** implement anything on-chain. It defines doctrine and constrains future design. No contract described here is built, deployed, funded, or authorized to move tokens.

---

## Context

### What "unclaimed rewards" and "clawback" mean here

In AFI Settlement v1, reward entitlement is established **only** by inclusion in a committed `EpochSettlementManifest` `claimRoot` (Layer 3), and realized **only** through the RewardsVault / claim layer (Layer 4). See `../specs/AFI_EPOCH_SETTLEMENT_MANIFEST.md` and `../specs/AFI_REWARDS_VAULT_AND_CLAIMS.md`. Because settlement is **pull-capable** (proof-based claims MUST be supported, per constitution O7), there will inevitably be funds that are **owed-but-unclaimed**: an epoch budget is funded to the RewardsVault, the manifest names entitlements, but some entitled parties never claim within any given window.

This ADR concerns three distinct, easily-conflated questions:

| Term | Question it answers | Settlement v1 status |
|------|---------------------|----------------------|
| **Unclaimed-reward policy** (O2) | What happens to funds that are validly owed but never claimed? (expiry window, recycle vs. roll-forward vs. return-to-treasury) | **OPEN** — placeholder hook MAY exist; value is OPEN |
| **Legal clawback** (O1) | May AFI reverse, withhold, or reclaim a reward that was wrongly settled, sanctioned, or legally encumbered — and under what jurisdiction/authority? | **OPEN** — pending legal/compliance |
| **Escheatment** (O1) | Where do forfeited/abandoned funds ultimately go (treasury, public-goods, statutory unclaimed-property regimes)? | **OPEN** — pending legal/compliance |

These are not engineering conveniences. They carry securities, money-transmission, unclaimed-property (escheat), tax, sanctions, and consumer-protection implications that vary by jurisdiction and by how an AFI reward is legally characterized. AFI has **not** completed that legal/compliance review. Freezing a specific clawback or sweep mechanic into a contract now would assert a legal posture AFI cannot yet defend.

### The v0 reality this corrects

The v0 architecture made the question impossible to even ask cleanly, because it never separated provenance from payout:

- **`AFIMintCoordinator.mintForSignal` → `AFIToken.mintEmissions(beneficiary, amount)`** minted the reward **at signal time**, per signal, **directly to a single `beneficiary` wallet** (push-to-wallet). With a push-at-mint model there is no custody seam at which "unclaimed" can exist as a state — tokens are *already in the recipient's wallet* the moment the signal is recorded. There is consequently **no architectural place** to express "owed-but-unclaimed," "expired," "held back," or "reclaimed."
- The per-signal **`AFISignalReceipt` (ERC-1155)** receipt conflated a provenance artifact with the reward event, so any "clawback" in v0 would have meant clawing back from end-user wallets after the fact — operationally and legally the worst possible posture.
- Admin + emissions authority sat under a **single 1-of-1 Safe**, so any unilateral "reclaim" capability would have been an un-checked centralized power, contradicting AFI's own "no centralized control" claims.
- The stale Snapshot pointer (a legacy, non-canonical three-letter ENS alias; the governance space is `afidao.eth`, network 1) and the placeholder `treasury.afidao.eth` Safe mean there is, today, **no reconciled, governance-gated destination** to which forfeited or unclaimed funds could even be routed. (See `../specs/AFI_ENS_SAFE_ADDRESS_REGISTRY_DOCTRINE.md`.)

Settlement v1 fixes the *structural* precondition: by moving to **epoch-batched settlement through a custodial RewardsVault** (D1, D6), there is now a **custody seam** — funds sit in the vault, owed-against-a-manifest, before they are claimed. That seam is exactly where an unclaimed/clawback policy *could* live. This ADR governs how that seam behaves **while the policy itself remains OPEN**.

### Why not just pick a policy now

- **Legal characterization is unresolved.** Whether an unclaimed AFI reward is "abandoned property," an unredeemed obligation, a reversible book entry, or something else determines whether *recycling* it is even lawful, and to whom escheat is owed. That is a legal/compliance call, not an engineering one.
- **Irreversibility cuts the wrong way.** A hard-coded sweep ("after N epochs, unclaimed funds are burned / sent to treasury / re-pooled") is, once deployed and funded, an irreversible assertion that AFI is *entitled* to take those funds. If that characterization is later found wrong, the contract has already acted.
- **It interacts with other OPEN items.** Unclaimed-reward handling is entangled with holdback/vesting under challenge windows (O4), reserve allocation (O5), and tokenomics splits (O3) — all OPEN. Settling O2/O1 in isolation would prejudge those.

---

## Decision

**AFI Settlement v1 leaves the unclaimed-reward policy and all legal clawback / escheatment mechanics OPEN. They MUST NOT be hard-coded or asserted as final policy until owner-approved legal/compliance review resolves them via a superseding ADR.** A **placeholder hook MAY** be specified so that v1 artifacts can *reference* a future policy without *defining its value*. Concretely:

1. **D-006-1 (MUST NOT — no final policy in v1).** No v1 contract, manifest, schema, or doctrine document MUST hard-code, or assert as final, any specific unclaimed-reward disposition (expiry window length, recycle vs. roll-forward vs. return-to-treasury vs. burn) or any clawback/escheatment mechanic. Any such value present today is to be treated as **placeholder/illustrative, not law**.

2. **D-006-2 (MUST — placeholder reference only).** The `EpochSettlementManifest` (Layer 3) carries `unclaimedRewardPolicyRef` and `holdbackPolicyRef` as **placeholder policy references** (constitution §15.3). For v1 these references MUST resolve to an **OPEN / unresolved policy** marker, not to an executable disposition. The RewardsVault `unclaimedRewardPolicy` (constitution §15.4) is likewise a **placeholder whose value is OPEN**.

3. **D-006-3 (MAY — inert hook).** Layer-4 design MAY reserve an **inert, no-op hook surface** (e.g., a policy-reference field, an extension point, or a disabled function path) so the *shape* of a future policy is anticipated. Any such hook, if specified, **MUST default to "no disposition"**: while OPEN, unclaimed funds simply **remain custodied in the RewardsVault, owed against the committed manifest, claimable**. Inaction is the only conforming default.

4. **D-006-4 (MUST — no silent forfeiture / no auto-sweep).** Until O1/O2 are resolved, the vault MUST NOT auto-expire, auto-sweep, auto-burn, auto-recycle, or otherwise reduce an entitled party's claim against a committed manifest. A reward that is owed-but-unclaimed MUST remain claimable. Expiry/forfeiture is **itself** an OPEN policy and MUST NOT be enabled by default.

5. **D-006-5 (MUST NOT — no clawback from settled/claimed funds without governed authority).** No v1 mechanism MUST be specified that lets any actor (including the owner, a Safe, or an agent) **reverse or reclaim a reward already validly claimed** without an explicit, governance-gated, legally-reviewed authority defined by a future superseding ADR. Clawback is OPEN, not "owner can do it by default."

6. **D-006-6 (MUST — agent boundary holds).** Agents MUST NEVER hold, route, sweep, reclaim, or escheat reward funds, and MUST NEVER be the actor that resolves O1/O2. Per constitution §13 and ADR-005, agents MAY at most *submit* manifests referencing the (OPEN) policy ref; they MUST NOT control treasury/vault funds or execute any disposition. See `./ADR-005-ens-aliases-addresses-source-of-truth.md`.

7. **D-006-7 (MUST — resolution path is an ADR, with legal/compliance).** O1 and O2 are resolved **only** by a future ADR that moves them from OPEN to Locked, citing the **owner and legal/compliance** (constitution §17). That ADR MUST define: the legal characterization relied upon, the expiry/window (if any), the disposition (recycle / roll-forward / return-to-treasury / escheat / hold), the **destination address** (a reconciled, governance-gated Safe — never a placeholder ENS name, never `treasury.afidao.eth` as-is), and the authority/threshold required to execute it.

8. **D-006-8 (SHOULD — design to keep the option open).** Because v1 settles per epoch through a custodial vault (D1, D6), the architecture SHOULD preserve the **custody seam** that makes a future policy *possible* (e.g., do not push rewards directly to end wallets at settlement; keep funds in the vault, owed-against-manifest). This is what distinguishes v1 from the v0 push-at-mint model and is the precondition for *any* future unclaimed-reward or clawback policy to be implementable at all.

---

## Consequences

### Positive

- **Legal exposure is minimized.** AFI does not assert, in code, a contested entitlement to user funds before legal/compliance has characterized them. Inaction (funds remain claimable) is the legally safest default.
- **The structural precondition is preserved.** By keeping the vault custody seam (D-006-8), AFI retains the *ability* to implement an unclaimed/clawback policy later — something v0's push-at-mint model destroyed.
- **No prejudgment of entangled OPEN items.** Holdback/vesting (O4), reserve (O5), and splits (O3) are not pre-decided by a premature sweep rule.
- **Auditability.** The manifest's `unclaimedRewardPolicyRef` makes the *absence* of a settled policy explicit and machine-checkable, rather than implied.

### Negative / costs

- **Funds may sit indefinitely.** With no expiry and no sweep, owed-but-unclaimed balances accumulate in the RewardsVault across epochs. This is an accepted cost: dormant-but-claimable is preferable to wrongful forfeiture. Accounting/reporting for these balances is an operational concern the owner SHOULD track.
- **Budget accounting must account for carryover.** Per-epoch budget caps (constitution §9) are enforced at the funding seam; unclaimed carryover does not refund the budget automatically. How (or whether) carryover interacts with future epoch budgets is itself part of the OPEN policy.
- **A second decision is required later.** v1 ships without a final answer; a future ADR (with legal/compliance) is a known, deferred obligation, not a forgotten one.

### Conformance impact

- A document, schema, or contract that **hard-codes** an expiry/sweep/burn/recycle rule, or that grants a default clawback power, **does not conform** to Settlement v1 and MUST be corrected or banner-deprecated (constitution §16).
- Any `unclaimedRewardPolicyRef` / `unclaimedRewardPolicy` value that points at an *executable disposition* (rather than an OPEN marker or inert no-op hook) is non-conforming for v1.

---

## Alternatives considered

| Alternative | Description | Why rejected for v1 |
|-------------|-------------|---------------------|
| **A. Hard-code an expiry + return-to-treasury sweep** | After N epochs, unclaimed funds auto-return to the treasury Safe. | Asserts, irreversibly and in code, that AFI is *entitled* to reclaim user funds — exactly the legal characterization that is unresolved (O1). Also depends on a reconciled treasury address that does not yet exist (the real Base Treasury Safe `0x1Dd6705ff84Ecd5eaDc51A913Ad8e2c6C9E79aC4` is not yet reconciled with `treasury.afidao.eth`). Premature and legally exposed. |
| **B. Hard-code an expiry + burn** | Unclaimed funds are burned after a window. | Same irreversibility problem, plus it destroys value that may be legally owed (potential abandoned-property / escheat obligations). Strongest possible assertion of forfeiture with the least legal cover. |
| **C. Auto-recycle into the next epoch's reward pool** | Unclaimed funds roll forward into future distributions. | Plausible *candidate* for the eventual policy, but it (a) prejudges tokenomics splits (O3) and roll-forward semantics, and (b) still asserts AFI may reassign owed funds without legal review. May be revisited by the resolving ADR; MUST NOT be the v1 default. |
| **D. Grant the owner/Safe a discretionary clawback power now** | A privileged actor can reclaim any reward at will. | Reintroduces exactly the centralized, un-gated power the v0 1-of-1 Safe critique condemns (constitution §12). Clawback authority, if it ever exists, MUST be governance-gated and legally reviewed — not a default admin capability. |
| **E. Specify nothing at all (no hook, no field)** | Stay silent; add fields only when policy is decided. | Rejected because silence makes the *open* status implicit and un-auditable, and would force a later breaking change to the manifest/vault shape. The constitution explicitly provides for a **placeholder ref** (§15.3, §15.4); a documented inert hook (D-006-3) is better than silence. |
| **F. Resolve it now via a quick internal decision** | Pick a policy without full legal/compliance review. | Violates constitution §17 (O1/O2 resolution requires owner **and** legal/compliance). Out of scope for an engineering ADR. |

**Chosen:** keep OPEN, with a **placeholder ref + optional inert no-op hook** and a **claimable-by-default, no-auto-disposition** posture (D-006-1 … D-006-8).

---

## Open questions

These remain **OPEN** and MUST NOT be implemented as final until resolved by a superseding ADR citing the owner and legal/compliance (constitution §6, §17):

- **O1 — Legal clawback / escheatment.** Under what authority, jurisdiction, and legal characterization (if any) may AFI reverse or reclaim a settled reward, and where do forfeited funds go? Custody of forfeited funds is undefined.
- **O2 — Unclaimed-reward policy value.** Is there an expiry window at all? If so, how long? Disposition on expiry: **recycle**, **roll-forward**, **return-to-treasury**, **escheat**, or **hold indefinitely**? The placeholder hook exists; the **value** is OPEN.
- **Destination address for any disposition.** Must be a reconciled, governance-gated Safe (chainId + threshold + signer policy), never a placeholder ENS alias. Blocked on the concrete-address registry (`../specs/AFI_ENS_SAFE_ADDRESS_REGISTRY_DOCTRINE.md`) and on reconciling the real treasury Safe.
- **Interaction with holdback/vesting (O4) and challenge windows.** Whether a challenge-failed reward is "unclaimed," "clawed back," or "never owed" — and which window governs — is unresolved and entangled with O4.
- **Accounting treatment of long-dormant balances.** How carryover is reported, capped, or surfaced for governance is undefined.

---

## Related docs

**Constitution (authoritative):**
- `../specs/AFI_SETTLEMENT_V1_DOCTRINE.md` — Settlement v1 doctrine; this ADR maps to **D8** (§4) and **O1/O2** (§6); placeholder fields defined in **§15.3** (`unclaimedRewardPolicyRef`, `holdbackPolicyRef`) and **§15.4** (`unclaimedRewardPolicy`).

**Specs (this set):**
- `../specs/AFI_EPOCH_SETTLEMENT_MANIFEST.md` — Layer 3; carries the placeholder policy refs.
- `../specs/AFI_REWARDS_VAULT_AND_CLAIMS.md` — Layer 4; where the inert no-op hook and claimable-by-default custody seam live.
- `../specs/AFI_ENS_SAFE_ADDRESS_REGISTRY_DOCTRINE.md` — the reconciled, governed destination any future disposition MUST target.
- `../specs/AFI_V0_DEPRECATION_AND_MIGRATION.md` — v0 push-at-mint posture this decision corrects.

**Sibling ADRs:**
- `./ADR-001-four-layer-settlement-architecture.md` — epoch-batched settlement and provenance ≠ payout (D1, D2, D9); creates the custody seam this ADR relies on.
- `./ADR-004-rewards-vault-merkle-claims.md` — RewardsVault + manifest-backed claim/route layer (D6).
- `./ADR-005-ens-aliases-addresses-source-of-truth.md` — concrete-address source of truth (D7); any disposition destination MUST be a concrete, governed address.
