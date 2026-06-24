# AFI Settlement v1 — Manifest & Provenance Schema

**Status:** DRAFT — Specification / interface pass (not yet Accepted)
**Date:** 2026-06-24
**Part of:** AFI Settlement v1 — see [AFI_SETTLEMENT_V1_DOCTRINE.md](./AFI_SETTLEMENT_V1_DOCTRINE.md)
**Companion (draft, non-implementation):** [`../../afi-config/schemas/afiEpochSettlementManifest.draft.schema.json`](../../afi-config/schemas/afiEpochSettlementManifest.draft.schema.json)

---

## 0. Scope, Status, and Authority

This document is a **schema and interface consolidation** for AFI Settlement v1. It draws the **Layer 1** provenance shapes ([AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md](./AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md)) and the **Layer 3** manifest shapes ([AFI_EPOCH_SETTLEMENT_MANIFEST.md](./AFI_EPOCH_SETTLEMENT_MANIFEST.md)) into a single precise reference: the **EpochSettlementManifest object**, the **four roots**, the **four leaf shapes**, the **on-chain/off-chain boundary**, the **delayed-disclosure model**, the **participant verification flows**, and the **EAS anchoring model**.

It is **specification and design only**. **It implements nothing.** No contract, schema, attestation, or manifest described here is built, deployed, anchored, committed, funded, or executed by virtue of this document existing. No funds move, no roles are granted, no Safe/ENS state changes, and no tokenomics, reward math, or production configuration is decided here. Exact field encodings, Solidity/ABI types, hash domains, the precise commitment/anchor contract, and the exact EAS schema remain **implementation design** and are explicitly **OPEN** (doctrine O6).

**Authority order.** This document is **subordinate** to the canonical doctrine set. Where it and the [constitution](./AFI_SETTLEMENT_V1_DOCTRINE.md) or any Accepted Layer 1–4 spec appear to conflict on a v1 architecture question, **the canonical doctrine wins** and this document is to be corrected. This document MUST NOT introduce a field, root, leaf, or rule that contradicts §4 (Locked Decisions), §7–§13, or §15 of the constitution.

**This document does not promote itself to canon.** It is a DRAFT consolidation. It does not re-decide any Locked Decision, does not resolve any OPEN item, and does not bless, wire, or extend any v0 mechanism.

### 0.1 Normative language

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, **MAY**, and **OPEN** are used exactly as defined in [AFI_SETTLEMENT_V1_DOCTRINE.md §1](./AFI_SETTLEMENT_V1_DOCTRINE.md#1-normative-language). This document adds one editorial label:

- **PROPOSED** — a concrete default offered by *this consolidation* to fill a shape that the canonical docs name but do not fully specify (e.g. the strategy-leaf field set, a canonical leaf-encoding scheme). A **PROPOSED** item is a recommended starting point for owner/implementation review. It is **not** Accepted doctrine, MUST NOT be implemented as final, and MUST NOT be cited as canon until adopted via the change-control process ([constitution §17](./AFI_SETTLEMENT_V1_DOCTRINE.md#17-change-control)). Where a **PROPOSED** default touches an existing **OPEN** item, the underlying decision remains **OPEN**.

### 0.2 What is canonical vs. PROPOSED in this document

| Element | Status here | Source of authority |
|---|---|---|
| EpochSettlementManifest field set (§3) | Canonical (restated) | [Layer 3 §2](./AFI_EPOCH_SETTLEMENT_MANIFEST.md), [constitution §15.3](./AFI_SETTLEMENT_V1_DOCTRINE.md#153-epochsettlementmanifest-layer-3--afi_epoch_settlement_manifestmd) |
| `signalRoot` / `evidenceRoot` / `rulesetHash` / `manifestURI` / `epochId` / `strategyId` / `disclosureWindow` (§4) | Canonical (restated) | [Layer 1 §4](./AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md), [constitution §15.1](./AFI_SETTLEMENT_V1_DOCTRINE.md#151-signal-provenance-leaves-layer-1--afi_signal_provenance_and_eas_schemamd) |
| `strategyRoot` / `claimRoot` (§4) | Canonical (restated) | [Layer 3 §2.2](./AFI_EPOCH_SETTLEMENT_MANIFEST.md), [constitution §15.3](./AFI_SETTLEMENT_V1_DOCTRINE.md) |
| Signal leaf (§5.1), Evidence leaf (§5.2) | Canonical (restated) | [Layer 1 §6, §7](./AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md) |
| Claim leaf **content** (§5.4) | Canonical (restated) | [Layer 4 §5.1](./AFI_REWARDS_VAULT_AND_CLAIMS.md), ADR-004 D-V5 |
| **Strategy leaf** field set (§5.3) | **PROPOSED** | derived from [Layer 2 §8](./AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md); not yet a canonical *leaf* |
| Canonical leaf-encoding / hash-domain scheme (§5.5) | **PROPOSED** | fills OPEN (O6); not Accepted |
| Verification flow #4, selective disclosure (§8.4) | **PROPOSED** | elaborates [Layer 1 §9](./AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md) |
| Every encoding/type/UID/resolver/attester address | **OPEN (O6)** | [constitution §6](./AFI_SETTLEMENT_V1_DOCTRINE.md#6-open-questions-not-settled) |

---

## 1. What This Document Is (and Is Not)

This is a **cross-layer schema reference**, not a fifth layer and not a new authority. It exists so that an integrator, auditor, or scoped agent can read **one** document and know the exact **shape** of the artifacts that bind proof to money — without re-reading four specs to reconstruct the field set, and without inventing encodings that contradict doctrine.

| This document **IS** | This document **IS NOT** |
|---|---|
| A consolidated schema view of Layers 1 + 3 (provenance leaves/roots and the manifest) | A new protocol layer, contract, or authority |
| A precise field/root/leaf registry that reuses canonical names **verbatim** | A re-decision of any Locked Decision or OPEN item |
| A statement of on-chain/off-chain boundaries and verification procedures | An implementation, deployment, ABI, or wiring instruction |
| A place where **PROPOSED** defaults are offered for the under-specified shapes (strategy leaf, leaf encoding) and clearly labelled | A blessing of v0 `mintForSignal`, ERC-1155 receipts, ENS-as-authority, or any payout-on-provenance |
| Subordinate to the constitution and the Accepted Layer 1–4 specs | A source of truth that overrides them |

The **load-bearing invariant** this schema serves is the constitution's central law: **provenance ≠ payout** ([constitution §8](./AFI_SETTLEMENT_V1_DOCTRINE.md#8-per-signal-provenance-vs-reward-settlement-the-core-law), L-SEP-1…L-SEP-4). The roots and leaves below are partitioned into a **proof plane** (signal/evidence/strategy) and a **money plane** (claim), joined **only** by the committed manifest and **only** under human/governance authorization.

---

## 2. The Object Model at a Glance

```
 PROOF PLANE  (truth & authorship — never pays)            MONEY PLANE (pays only vs claimRoot)
 ───────────────────────────────────────────────          ───────────────────────────────────
 signal leaves  ──► signalRoot   ┐                                            ┌─► claim leaves
 evidence leaves ─► evidenceRoot ┼─►  EpochSettlementManifest (Layer 3)  ─────┤    └─► claimRoot
 strategy leaves ─► strategyRoot ┘     • binds the 4 roots + rulesetHash       │         │
   (Layer 2 receipts)                  • carries totalRewardPool, role allocs   │   RewardsVault (L4)
                                       • carries policy refs (challenge/hold/    │   pays strictly vs
 rulesetHash  ──────────────────────►    unclaimed) + pointers (manifestURI,    │   claimRoot, never
 (pins the ruleset for every root)       disclosureURI)                         │   mints, never decides
                                       • COMMITTED ONCE per epochId on Base ─────┘
                                              │
                                              ▼
                                    EAS-backed Merkle root anchor on Base
                                    (attestationUID ↔ committed root)  — encoding OPEN (O6)

 OFF-CHAIN: dense records in the TSSD evidence vault (data, not tokens); raw stays withheld
            until disclosureWindow elapses. ON-CHAIN: roots + hashes + pointers only.
```

Three facts to carry through the rest of the document:

1. **Four roots, two planes, one bridge.** `signalRoot`, `evidenceRoot`, `strategyRoot` are **proof**; `claimRoot` is **money**; the **manifest** is the only crossing, gated by human/governance authorization ([Layer 3 §4](./AFI_EPOCH_SETTLEMENT_MANIFEST.md)).
2. **Commit on-chain, store off-chain.** Only roots/hashes/pointers are anchored; raw signal data lives in the TSSD evidence vault and is withheld until disclosure ([constitution §7](./AFI_SETTLEMENT_V1_DOCTRINE.md#7-off-chain-evidence-vs-on-chain-commitments)).
3. **One committed manifest per `epochId`.** Exactly one manifest root is committed per epoch on Base by the commitment/coordinator contract under documented Safe/governance authority; the RewardsVault then **enforces that committed `claimRoot`** for payout and never decides rewards ([Layer 3 MANIFEST-3, COMMIT-2/COMMIT-3](./AFI_EPOCH_SETTLEMENT_MANIFEST.md), L-SEP-3/L-SEP-4).

---

## 3. Epoch Manifest Structure

The **EpochSettlementManifest** is the canonical per-epoch document that binds the qualified set, the role allocations, the ruleset hash, and the distribution roots ([Layer 3 §1](./AFI_EPOCH_SETTLEMENT_MANIFEST.md)). The field set below is **restated verbatim** from [Layer 3 §2](./AFI_EPOCH_SETTLEMENT_MANIFEST.md) / [constitution §15.3](./AFI_SETTLEMENT_V1_DOCTRINE.md#153-epochsettlementmanifest-layer-3--afi_epoch_settlement_manifestmd); this document adds the **on-chain/off-chain** column and cross-references but changes **no** presence or meaning.

**Encoding note (whole table):** the type/encoding of every field is **implementation design and OPEN (O6)**. What is normative is each field's **presence and meaning**. "On-chain?" describes the minimal footprint: the manifest's *committed root* + binding fields + pointers go on-chain; the dense body (leaves, allocations, proof material) stays off-chain behind `manifestURI`.

### 3.1 Identity / version

| Field | Presence | Meaning | On-chain? |
|---|---|---|---|
| `epochId` | MUST | The accounting epoch this manifest settles. Exactly one committed manifest per `epochId`. Epoch cadence is off-chain (`afi-math`). | yes |
| `settlementVersion` | MUST | The settlement format/semantics version this manifest conforms to. Distinct from `rulesetHash`. | yes |
| `rulesetHash` | MUST | Cryptographic pin of the emissions + scoring + validation + allocation rules used to produce this manifest. Same field/meaning as Layers 1–2. | yes |
| `chainId` | MUST | The chain on which the root is committed and the vault enforces (Base, `8453`, for v1). Concrete `chainId` is source of truth, not ENS. | yes |
| `contractAddresses` | MUST | Concrete addresses of the contracts this manifest binds to (commitment/coordinator contract, RewardsVault, distributor, token). Concrete address + `chainId` authoritative; **no ENS resolution** for routing/access control. | yes |

> **Manifest scope (epoch-level).** The EpochSettlementManifest is **epoch-scoped**: `epochId` is the single top-level scope key, and exactly one manifest is committed per `epochId`, spanning **all** strategies that qualified in the epoch. `strategyId` is **NOT** a top-level manifest field — it is carried **per leaf / per provenance batch / per receipt-reference** (signal leaves §5.1, evidence leaves §5.2, strategy leaves §5.3, and the strategy/epoch receipt references §3.3). Provenance **batches/anchors are per-`(strategyId, epochId)`** (§9) and roll up into the epoch-scoped manifest roots; a per-strategy artifact is a **batch anchor / sub-manifest**, never the epoch manifest itself. Do not read any "`(strategyId, epochId)`" pairing in this document as implying the manifest carries one top-level `strategyId`.

### 3.2 Proof roots (commitments only — never raw arrays)

| Field | Presence | Meaning | On-chain? |
|---|---|---|---|
| `signalRoot` | MUST | Merkle/EAS root over the qualified **signal leaves** (§5.1) for the epoch (Layer 1). | yes (root only) |
| `evidenceRoot` | MUST | Merkle root over the per-signal **evidence leaves** (§5.2). | yes (root only) |
| `strategyRoot` | MUST | Merkle root over the strategy/epoch reputation set (Layer 2 receipts) — i.e. the **strategy leaves** (§5.3). | yes (root only) |
| `claimRoot` | MUST | Merkle root over the **claim leaves** (§5.4) — the `(recipient, role, amount, …)` tuples the vault pays against. **The money root.** | yes (root only) |

### 3.3 Economics

| Field | Presence | Meaning | On-chain? |
|---|---|---|---|
| `totalRewardPool` | MUST | Total reward budget for this epoch's manifest. Derived from the `afi-math` emissions schedule; the manifest **records** it. Funding cap enforced at the vault funding seam. Amounts SHOULD be **string-encoded integer base units** (PROPOSED, avoids JSON precision loss); units/decimals OPEN. | yes |
| `roleAllocationRoots` \| `roleAllocationLeaves` | MUST | Per-role allocation of `totalRewardPool` across the **three — and only three — v1 claim tracks: Providers, Analysts-Scorers, Validators** ([Layer 4 §11 R-1](./AFI_REWARDS_VAULT_AND_CLAIMS.md)). **Governance and public-goods are out of scope for Settlement v1 reward claims** and MUST NOT appear as a role-allocation key, claim track, or budget line here (§5.4, CLM-GOV). At least one form present (root for pull / leaves for push) and reconciling to `totalRewardPool`. **Split VALUES across the three roles are OPEN (O3).** | yes (root) / off-chain (leaves) |
| strategy/epoch receipt references | MUST | References to Layer 2 ERC-6909 receipts (`receiptId = hash(strategyId, epochId)`) backing each strategy's contribution. **Reputation, not claims** — never redeemable. | pointer |

### 3.4 Policy references (hooks, not values)

| Field | Presence | Meaning | On-chain? |
|---|---|---|---|
| `challengeWindow` | MUST | Window during which the epoch's settlement / specific claims MAY be challenged before funds release. Distinct from `disclosureWindow` (§7.3). | yes |
| `holdbackPolicyRef` | MUST | Reference to the holdback/vesting policy governing withheld portions. **Schedule/fraction/curve is OPEN (O4).** Commits the *hook*, not the *value*. | yes (ref) |
| `unclaimedRewardPolicyRef` | MUST (as placeholder) | Reference to the policy for never-claimed rewards. **PLACEHOLDER; value OPEN (O2).** Legal clawback/escheatment **OPEN (O1)**, pending legal/compliance. Present as a hook; MUST NOT be implemented as final. | yes (ref) |

### 3.5 Pointers / disclosure / meta

| Field | Presence | Meaning | On-chain? |
|---|---|---|---|
| `manifestURI` | MUST | Off-chain pointer to the full manifest body (dense allocations, leaves, proof material). On-chain stores root + pointer, never body. SHOULD be content-addressed. | pointer |
| `disclosureURI` \| delayed-disclosure reference | MUST | Reference to the delayed-disclosure surface where raw signal/evidence data becomes available **after** `disclosureWindow` elapses. Raw data stays in the TSSD vault until then. Tracks `disclosureStatus`. | pointer |
| `finalizedTimestamp` | MUST | Time the manifest was finalized/committed as the epoch's settlement root. Anchors the start of challenge/holdback/claim windows. | yes |
| `submitter` \| `signerMetadata` | MUST | Identifies who **submitted** the manifest (e.g. the scoped agent/generator) and who **authorized/signed** its commit + funding (human/governance/Safe). Both MUST be recorded for an agent-submitted manifest. Concrete signer addresses + `chainId` are source of truth; ENS is alias only. | yes |

### 3.6 Manifest invariants (restated, normative)

- **MAN-S1 (MUST):** All four roots (§3.2) MUST be present in a committed manifest; each MUST be derivable/verifiable even if bound under a single committed manifest root (PROOF-1, [Layer 3 §2.2](./AFI_EPOCH_SETTLEMENT_MANIFEST.md)).
- **MAN-S2 (MUST):** `claimRoot` is **produced off-chain from the claim leaves generated under the frozen `rulesetHash`**, and MUST be **accompanied by reconciliation evidence** tying it to `signalRoot`, `evidenceRoot`, `strategyRoot`, `rulesetHash`, and `totalRewardPool` (PROOF-3). **The money MUST trace back to proof.** This is a **reconciliation/audit** obligation, **not** an on-chain recomputation: no contract recomputes eligibility, scores, or amounts — the off-chain ruleset execution produces the claim leaves, and the vault *enforces* the committed root; it *does not decide* (MANIFEST-4, L-SEP-3).
- **MAN-S3 (MUST NOT):** No raw signal arrays, per-signal scores, or evidence blobs MUST appear in the manifest's on-chain footprint (MANIFEST-5, [constitution §7](./AFI_SETTLEMENT_V1_DOCTRINE.md#7-off-chain-evidence-vs-on-chain-commitments)).
- **MAN-S4 (MUST NOT):** The manifest MUST NOT encode a single `beneficiary` / `tokenAmount` / `receiptAmount` per-signal payout shape — that is the deprecated v0 distribution shape ([constitution §5](./AFI_SETTLEMENT_V1_DOCTRINE.md#5-deprecated-v0-posture), ECON-2).
- **MAN-S5 (MUST):** Exactly **one** manifest root is committed per `epochId` on Base, after human/governance authorization; an agent MUST NOT self-authorize a commit (CONF-1, CONF-9, COMMIT-1).

---

## 4. Root Semantics

Each root/identifier below is named **verbatim** from doctrine. This section fixes **what set each root commits**, **its plane** (proof vs money), and **its reconciliation duty**. Encodings (hash function, domain separation, tree arity, sort order) are **OPEN (O6)**; a PROPOSED canonical scheme is in §5.5.

| Identifier | Plane | Commits / identifies | Reconciliation / law |
|---|---|---|---|
| `epochId` | both | The accounting epoch (off-chain cadence via `afi-math`). | Exactly one committed manifest per `epochId`. Every leaf in every root for the epoch MUST carry this `epochId`. |
| `strategyId` | proof | The strategy (provider methodology) a **batch / leaf / receipt** belongs to. **Leaf/batch/receipt-scoped — NOT a top-level manifest field** (the manifest is epoch-scoped, §3.1). | A signal/strategy leaf's `strategyId` MUST equal its batch `strategyId`. `receiptId = hash(strategyId, epochId)`. |
| `rulesetHash` | both | Pin of the exact emissions+scoring+validation(+allocation) ruleset version used to produce every root for the epoch. | The **same** `rulesetHash` value MUST appear in the anchor, the signal/evidence/strategy leaves, and the manifest. Makes all leaves reproducible. Distinct from `settlementVersion`. |
| `signalRoot` | proof | Merkle/EAS root over all **signal leaves** (§5.1) qualified for `(strategyId, epochId)` (Layer 1). The primary provenance commitment. | Independently verifiable post-disclosure (§8.1). **Proves provenance, never entitlement.** |
| `evidenceRoot` | proof | Merkle root over all **evidence leaves** (§5.2) — the RAW→…→SCORED lifecycle snapshots for the batch's signals. | Lets a verifier confirm the disclosed lifecycle record is exactly what was committed (§8.1). |
| `strategyRoot` | proof | Merkle root over the **strategy leaves** (§5.3) — the per-`(strategyId, epochId)` reputation set (Layer 2 receipts) for the epoch. | The receipt's score MUST be an aggregate **consistent with** `strategyRoot` ([Layer 2 §9](./AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md)). **Reputation, never a claim.** |
| `claimRoot` | **money** | Merkle root over the **claim leaves** (§5.4) — `(recipient, role, amount, …)` tuples. **The only payout authority.** | Produced off-chain from the claim leaves (frozen ruleset); MUST be **accompanied by reconciliation evidence** tying it to the proof roots + `rulesetHash` + `totalRewardPool` (MAN-S2) — a reconciliation duty, **not** on-chain reward math. The vault pays strictly against this root and nothing else (L-SEP-4). |
| `manifestURI` | pointer | Content-addressed pointer to the dense off-chain manifest body needed to reconstruct leaves and proofs. | Fetching `manifestURI` and recomputing the roots MUST reproduce the committed manifest root (META-1). SHOULD be content-addressed (META-2). |
| `disclosureWindow` | parameter | The configured **delayed-disclosure** period after which raw off-chain data becomes inspectable (§7). | Governs **provenance visibility only**; MUST NOT gate, accelerate, or condition any reward payment (DISC-4). Units/value **OPEN (O6)**. |

> **Naming reconciliation (`disclosureWindow` vs. "delayedDisclosureWindow").** The canonical field name is **`disclosureWindow`** ([Layer 1 §4](./AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md), [constitution §15.1](./AFI_SETTLEMENT_V1_DOCTRINE.md#151-signal-provenance-leaves-layer-1--afi_signal_provenance_and_eas_schemamd)). The constitution's prose calls the concept the "**delayed-disclosure window**" ([§7](./AFI_SETTLEMENT_V1_DOCTRINE.md#7-off-chain-evidence-vs-on-chain-commitments)). This document keeps the canonical field name **`disclosureWindow`** and treats "delayed disclosure window" strictly as descriptive prose for the **same** parameter. No new `delayedDisclosureWindow` field is introduced; doing so would fork the field registry. See the report's *Contradictions/Reconciliations* section.

**Root-coupling prohibitions (restated):**

- **ROOT-1 (MUST NOT):** `claimRoot` MUST NOT be derived from, gated by, or substituted for any proof root in a way that lets provenance inclusion *imply* entitlement. Inclusion in `signalRoot`/`evidenceRoot`/`strategyRoot` confers **no** token entitlement (PROV-NP-3, MAN-3).
- **ROOT-2 (MUST NOT):** Layer-2 receipt balances/scores MUST NOT be the unit, weight, or denominator of any on-chain distribution; reputation→reward weighting happens off-chain in the ruleset and is then frozen into `claimRoot` (whose splits are OPEN, O3) ([Layer 2 §11](./AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md)).
- **ROOT-3 (MUST):** Where a field appears in more than one root/leaf/receipt (`rulesetHash`, `signalRoot`, `evidenceRoot`, `strategyRoot`, `epochId`, `strategyId`), every artifact MUST reference the **same committed value**; none may restate a divergent value ([Layer 2 §8](./AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md)).

---

## 5. Leaf Shapes

Four leaf shapes feed the four roots. **Signal** and **evidence** leaves are **canonical** (restated from [Layer 1 §6, §7](./AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md)). The **claim** leaf's **content** is canonical ([Layer 4 §5.1](./AFI_REWARDS_VAULT_AND_CLAIMS.md), ADR-004 D-V5); its encoding is OPEN. The **strategy** leaf is **PROPOSED** here — the canonical docs define `strategyRoot` and the ERC-6909 receipt but do **not** yet define a strategy *leaf*; §5.3 offers a default derived from the receipt's committed metadata.

Across all leaves: **no raw payloads, cleartext scores, validator decisions, UWR axis values, or evidence blobs** — only hashes/commitments and identity references (MAN-S3, [Layer 1 §6 notes](./AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md)).

### 5.1 Signal leaf — CANONICAL (Layer 1 §6)

One leaf per **qualified signal**. Commits to `signalRoot`.

| Field | Presence | Meaning |
|---|---|---|
| `signalId` | MUST | Stable unique id for the signal (e.g. TSSD/USS `provenance.signalId`). |
| `strategyId` | MUST | The strategy that produced the signal. MUST equal the batch `strategyId`. |
| `epochId` | MUST | The epoch the signal qualified in. MUST equal the batch `epochId`. |
| `contentHash` | MUST | Hash binding the signal's canonical off-chain content (raw + enriched record). The cryptographic tie to TSSD evidence. |
| `scoreCommitment` | MUST | Commitment (hash) to the deterministic score/decision (UWR axes + composite + qualify flag). **Score stays off-chain;** only a commitment is bound. |
| `producer` | MUST | Identity **reference** of the author/provider (ref/id or address ref, not raw PII). Presence confers **no** token entitlement. |
| `timestamp` | MUST | The signal's authoritative time reference (e.g. scored-at). |
| `rulesetHash` | MUST | The ruleset version under which the signal was scored/qualified. MUST be consistent with the batch `rulesetHash`. |

**Scoping law:** `signalId` + `strategyId` + `epochId` uniquely scope a leaf within a batch (no duplicate qualified signals per batch).

### 5.2 Evidence leaf — CANONICAL (Layer 1 §7)

One or more leaves per signal **lifecycle stage**. Commits to `evidenceRoot`.

| Field | Presence | Meaning |
|---|---|---|
| `signalId` | MUST | The signal this evidence pertains to. MUST match a signal leaf `signalId` in the same batch. |
| `evidenceHash` | MUST | Hash of the lifecycle evidence snapshot (the RAW→…→SCORED record state being attested). |
| `stage` | MUST | The lifecycle stage the snapshot represents (e.g. `RAW`, `ENRICHED`, `SCORED`). |
| `disclosureStatus` | MUST | Disclosure state of *this* snapshot (§7), which MAY differ per stage (e.g. enriched disclosed later than raw). |

### 5.3 Strategy leaf — PROPOSED (not yet canonical)

> **PROPOSED.** The canonical docs commit a `strategyRoot` ([Layer 3 §2.2](./AFI_EPOCH_SETTLEMENT_MANIFEST.md)) as "the root over the strategy/epoch reputation set (Layer 2 receipts)," and specify the ERC-6909 receipt's committed metadata ([Layer 2 §8](./AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md)) — but they do **not** define the *leaf* under `strategyRoot`. The shape below is the **PROPOSED** strategy-leaf field set, derived 1:1 from the receipt's committed metadata so that `strategyRoot` commits exactly the reputation records the receipts attest. It is offered for owner/implementation review; it is **not** Accepted doctrine.

One leaf per `(strategyId, epochId)` reputation record. Commits to `strategyRoot`.

| Field | Presence (PROPOSED) | Meaning | Anchored to |
|---|---|---|---|
| `receiptId` | MUST | `hash(strategyId, epochId)` — the ERC-6909 `id`, deterministically reproducible off-chain. | Layer 2 §4 |
| `strategyId` | MUST | The strategy this reputation belongs to. MUST equal the batch/manifest `strategyId`. | Layer 2 §8 |
| `epochId` | MUST | The epoch this reputation is scoped to. | Layer 2 §8 |
| `owner` | MUST | Strategy controller / reputation subject — **concrete address ref**, not ENS. Confers **no** payout entitlement. | Layer 2 §6 |
| `reputationCommitment` | MUST | Commitment to the finalized reputation magnitude (`balance \| score`). **PROPOSED:** a commitment rather than a cleartext score so the leaf carries no raw score on-chain beyond the receipt's own `score` storage; whether the leaf binds the cleartext aggregate or a commitment is **OPEN** (L2-O2/O5). NOT a token amount, NOT a claim. | Layer 2 §7 |
| `signalRoot` | MUST | Linkage to the Layer-1 signal provenance basis for the score (reference, not recompute). | Layer 2 §9 |
| `evidenceRoot` | MUST | Linkage to the Layer-1 evidence root (reference, not recompute). | Layer 2 §9 |
| `rulesetHash` | MUST | The scoring ruleset the score is attributable to. MUST equal the batch/manifest `rulesetHash`. | Layer 2 §9 |
| `finalized` | MUST | Flag: epoch reputation finalized. A finalized record SHOULD be immutable (Layer 2 §10). | Layer 2 §8/§10 |

**Strategy-leaf laws (restating Layer 2 prohibitions, PROPOSED scope):**

- **STR-1 (MUST NOT):** A strategy leaf (or its `reputationCommitment`) MUST NOT be redeemable, a transferable claim, the unit of payout, or readable by any vault/claim contract to decide eligibility ([Layer 2 §11](./AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md)). It is provenance/reputation, anchored to the proof plane.
- **STR-2 (MUST NOT):** `strategyRoot` MUST NOT be coupled to `claimRoot` as a payout mechanism, and `claimRoot` MUST NOT be derived from strategy-leaf reputation (ROOT-1, [Layer 2 §9](./AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md)).

### 5.4 Claim leaf — CANONICAL content, OPEN encoding (Layer 4 §5.1, ADR-004 D-V5)

One leaf per **entitlement**. Commits to `claimRoot` (and/or the relevant `roleAllocationRoots`). **The only leaf the vault redeems.**

| Field | Presence | Meaning |
|---|---|---|
| `epochId` | MUST | The epoch this entitlement settles. Scopes budget and claimed-state; a leaf is claimable only under its own epoch's root. |
| `recipient` | MUST | Payout address — **concrete address, source of truth**. The vault MUST NOT resolve ENS for `recipient` (D7, A-3). |
| `role` | MUST | The v1 **claim role set is exactly `Provider \| Analyst-Scorer \| Validator`** ([Layer 4 §11 R-1](./AFI_REWARDS_VAULT_AND_CLAIMS.md)) — Settlement v1 rewards are a **three-way participant split**. **Governance and public-goods are NOT claim roles and MUST NEVER be claimants** (CLM-GOV). |
| `amount` | MUST | The entitled amount. SHOULD be **string-encoded integer base units** (PROPOSED, avoids JSON precision loss); units/decimals OPEN. Aggregate claims per epoch MUST NOT exceed `totalRewardPool` (B-3). |
| `leafIndex` \| `nullifier` | MUST | The per-`(epochId, leaf)` identifier backing exactly-once claim prevention (DC-1, ADR-004 D-V4). |
| `constraints` | MAY (PROPOSED optional) | Optional per-leaf constraints (e.g. holdback/vesting reference, challenge binding) consistent with the manifest's `holdbackPolicyRef` / `challengeWindow`. Encoding OPEN; values OPEN (O4). |

**Claim-leaf laws (restated):**

- **CLM-0 (MUST):** **Proof-based pull is the mandatory minimum v1 settlement path** — a claimant (or a permissionless relayer paying a fixed `recipient`) presents a Merkle proof of the claim leaf against the committed `claimRoot`, and the vault pays against it (D-PULL, [Layer 4 §5](./AFI_REWARDS_VAULT_AND_CLAIMS.md)). A **push-only** design is **non-conforming**. Push/distributor routing (§9, `distributor`) MAY *additionally* be supported but is **OPEN/optional (O7)** and MUST NOT be the sole path; it never substitutes for the mandatory pull capability and is subject to the same root verification, double-pay prevention, pause, holdback, and budget rules.
- **CLM-1 (MUST):** A claim is valid **iff** the claimant presents a leaf that verifies as included under the epoch's committed `claimRoot` (or `roleAllocationRoots`) ([Layer 4 §5.2](./AFI_REWARDS_VAULT_AND_CLAIMS.md)). A proof that does not verify rejects without state change (FC-2).
- **CLM-2 (MUST NOT):** A provenance artifact (signal/evidence/strategy leaf, EAS `attestationUID`, ERC-6909 receipt, or any v0 ERC-1155 receipt) MUST NOT be redeemable at the vault ([Layer 4 §3](./AFI_REWARDS_VAULT_AND_CLAIMS.md)). Only a claim leaf under `claimRoot` is payable.
- **CLM-3 (MUST):** The vault marks the leaf claimed **before** transfer (checks-effects-interactions) and never mints (DC-3, V-MINT).
- **CLM-GOV (MUST NOT):** **Governance and public-goods are out of scope for Settlement v1 reward claims.** Governance MAY authorize, commit, and administer protocol processes (manifest commit, funding, pause — §9.2, [Layer 3 §6](./AFI_EPOCH_SETTLEMENT_MANIFEST.md)), but MUST NEVER be a claim role, a claim-leaf `role`, a `roleAllocationRoots` key, a `roleAllocationLeaves` role, or a budget line in the v1 `claimRoot`. The Settlement v1 reward/claim set is exactly the **three participant roles** `Provider | Analyst-Scorer | Validator`. Any future **non-participant** funding program (e.g. a public-goods or grants program) would require a **separate, owner-approved spec/ADR** and MUST NOT be encoded into Settlement v1 `claimRoot` semantics.

### 5.5 PROPOSED canonical leaf-encoding & hash-domain scheme (fills OPEN O6)

> **PROPOSED — not Accepted; O6 remains OPEN.** Exact hash function, serialization, domain separation, and tree construction are implementation design ([Layer 1 §2 PROV-D5](./AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md), constitution O6). The following is a **recommended default** so implementers have a concrete, auditable starting point. Adopting it requires the change-control process (constitution §17); until then it MUST NOT be cited as canon.

- **ENC-P1 (PROPOSED):** Each leaf digest = `keccak256( domainTag ‖ canonical(fields) )`, where `domainTag` is a per-leaf-type, per-`settlementVersion` domain-separation constant (distinct tags for signal / evidence / strategy / claim leaves) and `canonical(fields)` is a deterministic ABI-style encoding of the field set in the table order above.
- **ENC-P2 (PROPOSED):** Trees are binary Merkle trees over **sorted** leaf digests (sort by digest) with duplicate-leaf rejection, so a root is independent of input ordering and re-derivable by any verifier from the disclosed leaf set.
- **ENC-P3 (PROPOSED):** `rulesetHash` = a domain-separated hash of the published, frozen ruleset bundle, recomputable by a third party from the published ruleset (§8.1 step 2).
- **ENC-P4 (PROPOSED):** `receiptId = keccak256( abi.encode(strategyId, epochId) )` unless a documented domain-separated variant is adopted, satisfying the determinism/collision properties of [Layer 2 §4](./AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md).
- **ENC-OPEN:** Tree arity, sort vs. position-indexed proofs, the exact `domainTag` values, the EAS schema ABI, and whether `signalRoot` is a plain Merkle root or an EAS-resolver-bound root are **OPEN (O6)** and owner/implementation-decided.

---

## 6. On-Chain vs. Off-Chain Boundary

AFI v1 is **commit-on-chain, store-off-chain** ([constitution §7](./AFI_SETTLEMENT_V1_DOCTRINE.md#7-off-chain-evidence-vs-on-chain-commitments)). The boundary is a hard law, not an optimization.

| Concern | On-chain (committed) | Off-chain (TSSD evidence vault / content-addressed store) |
|---|---|---|
| Provenance | `signalRoot`, `evidenceRoot` (+ EAS `attestationUID` if used) | signal/evidence leaf **pre-images**, raw + enriched + scored `VaultedSignalRecord` |
| Reputation | `strategyRoot`, the ERC-6909 receipt (`receiptId`, `owner`, `score`, `finalized`, root linkages) | strategy-leaf pre-images, score derivation inputs |
| Settlement | committed **manifest root**, the four roots, `rulesetHash`, `chainId`, `contractAddresses`, `finalizedTimestamp`, policy **refs**, `totalRewardPool` | dense manifest body (allocations, leaves, proofs) behind `manifestURI` |
| Money | `claimRoot`, claimed-bitmap/nullifier set, vault custody, claim/route events | claim-leaf pre-images + Merkle proofs behind `manifestURI` |
| Disclosure | `disclosureWindow` (parameter), `disclosureStatus` (flag), `disclosureURI` (pointer) | the disclosed pre-images themselves (released at/after the window) |

**Boundary laws (restated):**

- **BND-1 (MUST NOT):** Raw per-signal arrays, cleartext scores, UWR axes, validator decisions, or evidence blobs MUST NOT be written on-chain — only roots, `rulesetHash`, the `disclosureWindow` parameter, `disclosureStatus`, and pointers (MANIFEST-5, [Layer 1 §4](./AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md)).
- **BND-2 (MUST):** Every qualified signal MUST be independently verifiable from chain data + the published manifest + post-disclosure off-chain data (PROOF-2, §8.1), **without trusting AFI's private infrastructure**.
- **BND-3 (MUST):** `manifestURI` (and the manifest body) MUST be mutually verifiable against the committed root: fetching the pointer and recomputing the roots reproduces the committed root (META-1). The body SHOULD be content-addressed (META-2).
- **BND-4 (MUST):** "TSSD vault" / "evidence vault" (**data** custody) MUST NOT be conflated with "RewardsVault" / "TreasuryVault" (**token** custody) or the "xERC20 bridge lockbox" (bridge custody) (N-1…N-4, [constitution §7 naming law](./AFI_SETTLEMENT_V1_DOCTRINE.md#7-off-chain-evidence-vs-on-chain-commitments)). The on-chain roots touch **data** commitments; only `claimRoot` → vault touches tokens.

---

## 7. Delayed Disclosure Model

Raw signal data is competitively sensitive (a disclosed live signal can be front-run/copied). v1 therefore **commits early, discloses late** ([Layer 1 §5](./AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md)).

### 7.1 Commitment-before-disclosure

- **DSC-1 (MUST):** At anchoring, `signalRoot` / `evidenceRoot` (and the manifest's roots) are committed, but raw payloads remain **off-chain and withheld** in the TSSD evidence vault until `disclosureWindow` elapses (DISC-1).
- **DSC-2 (MUST):** Leaves are built over **content commitments** (`contentHash`, `scoreCommitment`, `evidenceHash`, and the PROPOSED `reputationCommitment`), so a root binds the exact off-chain content **without revealing it**. Disclosure reveals pre-images; it MUST NOT change any committed root (DISC-2).

### 7.2 `disclosureStatus` lifecycle

The minimum lifecycle a conforming implementation MUST support ([Layer 1 §5](./AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md)):

| `disclosureStatus` | Meaning | Verifier can reproduce leaves? |
|---|---|---|
| `WITHHELD` | Root committed; pre-images not yet released. | No — can verify a root exists and is well-formed; cannot reproduce leaves from raw data yet (§8 step "existence only"). |
| `DISCLOSED` | `disclosureWindow` elapsed; pre-images published via `manifestURI` / `disclosureURI`. | **Yes** — full leaf reproduction + inclusion check. |

Additional intermediate states and the exact enum encoding are **OPEN (O6)**; these two are the minimum. `disclosureStatus` MAY differ per evidence stage (§5.2).

### 7.3 Disclosure timing is NOT payout timing

- **DSC-3 (MUST):** `disclosureWindow` / `disclosureStatus` relate to **provenance visibility only**. They MUST NOT gate, accelerate, or condition any reward payment (DISC-4). Holdback/challenge windows that *do* affect payout are a Layer 3/4 concern (`challengeWindow`, `holdbackPolicyRef`) and are **distinct** parameters from `disclosureWindow`.
- **DSC-4 (SHOULD):** The disclosure reference SHOULD be content-addressed so disclosure is itself verifiable (published pre-images hash back to the committed leaves) (DISC-5).

---

## 8. Participant Verification Flows

All flows assume the verifier trusts **only** chain data + the published manifest + (post-disclosure) off-chain records — never AFI's private infrastructure ([Layer 1 §9](./AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md), BRIDGE-2). Inputs common to every flow: the on-chain committed root(s) for `epochId` (and `attestationUID` if EAS), `rulesetHash`, `manifestURI` → manifest body, and the Merkle proof (sibling path) for the target leaf.

### 8.1 Verify one signal's inclusion / provenance

Goal: confirm a specific signal was authored, scored under the named ruleset, and committed — **without any payment implied**.

1. **Fetch** the disclosed off-chain record for `signalId` (post-window) via `manifestURI` / `disclosureURI`.
2. **Recompute commitments:** derive `contentHash` over the canonical content and `scoreCommitment` over the disclosed score/decision using the **exact** ruleset identified by `rulesetHash`; independently recompute `rulesetHash` from the published ruleset and confirm it matches the anchor.
3. **Reconstruct the signal leaf** from `{signalId, strategyId, epochId, contentHash, scoreCommitment, producer, timestamp, rulesetHash}` (canonical serialization, §5.5) and hash to the leaf digest.
4. **Verify inclusion:** apply the Merkle proof; confirm it reduces to the committed `signalRoot`.
5. **Reconstruct + verify evidence leaves** `{signalId, evidenceHash, stage, disclosureStatus}` against `evidenceRoot` the same way.
6. **Confirm the anchor is real:** check `signalRoot`/`evidenceRoot` against the on-chain anchor (and, if EAS, that `attestationUID` resolves to an attestation committing these roots for this `epochId`/`strategyId`).

**Outcome:** steps 2–6 passing ⇒ the signal is independently verified as authored and committed. A `WITHHELD` batch supports only step 6 (existence/well-formedness) until disclosure. **No payout is implied or inferable** (PROV-NP, ROOT-1).

### 8.2 Verify one strategy/epoch reputation record

Goal: confirm a strategy's epoch reputation is the one committed — **as reputation, never a claim**.

1. **Recompute `receiptId`** = `hash(strategyId, epochId)` off-chain (§5.5 ENC-P4) and locate the ERC-6909 receipt.
2. **Read the receipt's committed metadata** (`owner`, `score`/`finalized`, and the `signalRoot`/`evidenceRoot`/`strategyRoot`/`rulesetHash`/manifest linkages) ([Layer 2 §8](./AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md)).
3. **Reconstruct the strategy leaf** (§5.3 PROPOSED) and **verify inclusion** under the committed `strategyRoot` via its Merkle proof.
4. **Check root consistency:** the leaf's `signalRoot`/`evidenceRoot`/`rulesetHash` MUST equal the values committed by Layer 1 and the manifest (ROOT-3).
5. **(SHOULD) Recompute the magnitude:** given `rulesetHash` + post-disclosure Layer-1 evidence, recompute the reputation magnitude and check it against the on-chain receipt ([Layer 2 §7](./AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md)).
6. **Confirm decoupling:** verify the receipt/`strategyRoot` is **not** wired to `claimRoot` — there is no on-chain path turning the receipt into a claim (STR-1, STR-2).

**Outcome:** the strategy's reputation is verified and provably **outside** the money chain.

### 8.3 Verify one reward claim

Goal: confirm a payout is owed and traces back to proof — **the money matches the proof**.

1. **Confirm the committed manifest** for `epochId`: exactly one manifest root on Base; read `claimRoot`, `totalRewardPool`, `challengeWindow`, `holdbackPolicyRef`, `unclaimedRewardPolicyRef`, `chainId`, `contractAddresses`, `finalizedTimestamp`.
2. **Reconstruct the claim leaf** `{epochId, recipient, role, amount, leafIndex|nullifier, [constraints]}` (§5.4) and **verify inclusion** under the committed `claimRoot` (or the relevant `roleAllocationRoots`).
3. **Check reconciliation:** confirm the published **reconciliation evidence** ties `claimRoot` to `signalRoot`/`evidenceRoot`/`strategyRoot`/`rulesetHash`/`totalRewardPool` (MAN-S2) — i.e. the claim leaves were generated off-chain under the frozen ruleset, **not** recomputed on-chain — and that the role allocations reconcile to `totalRewardPool` (ECON-1).
4. **Check claim hygiene:** the leaf is **not already claimed** (claimed-bitmap/nullifier for `(epochId, leaf)`), the vault is **not paused**, and the `challengeWindow`/holdback are satisfied/released per the committed refs ([Layer 4 §5.2, §6–§8](./AFI_REWARDS_VAULT_AND_CLAIMS.md)).
5. **Confirm authority + custody:** the paying contract is the registry-verified RewardsVault at the manifest's `contractAddresses`/`chainId`, funded for this `epochId` within `min(funded, totalRewardPool)` (B-1…B-3); `recipient` is a concrete address (no ENS resolution).
6. **Trace end-to-end:** `signal → manifest → claimRoot → claim` resolves to the exact payout (every payout traces; [Layer 4 §5.2 step 5](./AFI_REWARDS_VAULT_AND_CLAIMS.md)).

**Outcome:** the claim is verified as authorized **only** by the committed manifest, paid **only** by the enforcing vault, with no recomputation or minting.

### 8.4 Verify without exposing proprietary raw signal data — PROPOSED

> **PROPOSED elaboration** of the commit/reveal model in [Layer 1 §5, §9](./AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md). It introduces no new on-chain artifact; it states how the existing commitments support selective, privacy-preserving verification.

Because each leaf binds **content commitments** (`contentHash`, `scoreCommitment`, `evidenceHash`) rather than payloads, and each leaf is an **independent** member of its tree, verification can be performed at several disclosure depths **without** revealing the proprietary raw signal:

- **SD-1 (existence, pre-disclosure):** While `WITHHELD`, a third party can verify that a well-formed root exists and is anchored (and EAS-attested, if used) for `(epochId, strategyId)` — proving *a committed set exists* — **without any pre-image** (§8.1 step 6 only).
- **SD-2 (selective single-leaf disclosure):** Because each leaf is an independent tree member, the prover MAY disclose the pre-image and Merkle proof for **one** signal (or one strategy/claim leaf) to a counterparty, who verifies inclusion under the committed root **without** the prover revealing any **other** leaf's raw data. One signal's provenance can be proven without disclosing the rest of the batch.
- **SD-3 (commitment check without raw payload):** A holder of the raw record can prove to a verifier that a given `contentHash`/`scoreCommitment` corresponds to a claimed record by revealing only the commitment inputs the verifier needs — or, where the ruleset's commitment scheme permits, via a succinct proof — so the verifier confirms *binding* without receiving the proprietary payload in full. (Whether a zero-knowledge commitment scheme is used is **OPEN (O6)**; the default is plain hash commitments with selective pre-image reveal.)
- **SD-4 (MUST):** None of these flows move, gate, or imply any payment (DSC-3, ROOT-1). Selective disclosure is a **provenance-visibility** mechanism only.

**Outcome:** a participant can prove *their* signal is genuinely committed (and, post-disclosure, fully reproduce it) while keeping competitively sensitive raw data — and other participants' data — undisclosed.

---

## 9. EAS Anchoring Model

Layer 1 commits provenance as an **EAS-backed Merkle batch root anchored on Base** ([Layer 1 §2 PROV-D1](./AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md)). The **direction** is locked; the **exact EAS schema** (schema UID, attested-field ABI, resolver presence) is **OPEN (O6)** and MUST NOT be frozen as final. This section states the model at the schema level; it asserts no concrete UID, resolver, or attester address (there is none — confirmed against the gap analysis and ADRs).

### 9.1 What is attested

- **EAS-1 (MUST):** The attestation commits the **batch root(s)** and their binding metadata for a per-strategy provenance batch `(strategyId, epochId)` — the per-strategy batch anchors that roll up into the **epoch-scoped** manifest (§3.1) — at minimum `signalRoot`, `evidenceRoot`, `rulesetHash`, `disclosureWindow`/`disclosureStatus`, and the `manifestURI` pointer — **never** raw signal arrays, scores, or evidence blobs (BND-1, [Layer 1 §4](./AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md)).
- **EAS-2 (MUST):** The attestation is a **commitment**, not a payout instrument. An `attestationUID` is **not** redeemable, claimable, or convertible to tokens, and MUST NOT be the unit of payout (PROV-NP-2, CLM-2).
- **EAS-3 (PROPOSED):** The manifest-level commitment MAY additionally bind `strategyRoot` and `claimRoot` under the single committed **manifest root** (Phase B), with the provenance attestation (Layer 1) and the settlement commitment (Layer 3) as **separate acts** that share the same roots — see §9.3.

### 9.2 Who may attest / commit

The anchor follows the manifest lifecycle's authority model ([Layer 3 §3, §6](./AFI_EPOCH_SETTLEMENT_MANIFEST.md), [constitution §12–§13](./AFI_SETTLEMENT_V1_DOCTRINE.md#12-safe--governance-hardening-principles)). No EAS attester address is fixed here; the **authority rules** are:

- **EAS-4 (MAY):** A scoped, least-privilege **agent/generator** MAY *build* the batch, derive the roots, and *submit* a candidate attestation/manifest (Phase A, BUILD-4, AGENT-1). The candidate has **no authority** until authorized.
- **EAS-5 (MUST):** Anchoring the provenance root and/or committing the manifest root MUST be performed under **documented Safe / governance authority** (ideally N-of-M + timelock; 1-of-1 is not production-grade), the same authority that authorizes commit + funding (COMMIT-1, COMMIT-3, A-1). The agent's authority ends at **submission**.
- **EAS-6 (MUST NOT):** Agents MUST NEVER hold the attester/commit keys, control treasury funds, or self-authorize an anchor/commit (AGENT-3, D10). The attester/committer is a **registry-verified concrete account** ([ENS/Safe doctrine §7](./AFI_ENS_SAFE_ADDRESS_REGISTRY_DOCTRINE.md)); **ENS MUST NOT be resolved** to determine attester authority (R-3, D7).
- **EAS-7 (MUST):** Provenance anchoring and reward funding/settlement are **separate transactions, separate artifacts, separate trust assumptions** — a single call MUST NOT both anchor provenance and move value (PROV-NP-4; this is the v0 `mintForSignal` contradiction v1 closes). The v0 `AFIMintCoordinator.mintForSignal` flow — which mints the reward **and** an ERC-1155 `AFISignalReceipt` in a single call while recording provenance only as an event (no committed root) — is **not** the v1 attester/anchor and MUST NOT be wired or promoted as such ([V0 deprecation §3.2](./AFI_V0_DEPRECATION_AND_MIGRATION.md), D9).

### 9.3 How the attestation references the manifest / roots

- **EAS-8 (MUST):** The manifest carries `attestationUID` (if EAS is used) alongside its roots, and the attestation commits the same root values, so the two are **mutually verifiable**: resolving `attestationUID` yields an attestation committing `signalRoot`/`evidenceRoot`/`rulesetHash` for the manifest's `epochId`/`strategyId` (§8.1 step 6, [Layer 1 §10 MAN-1](./AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md)).
- **EAS-9 (MUST):** Provenance anchoring MUST be possible **without** any manifest commitment or funding (MAN-4): the proof plane can exist before — and independently of — the money plane.
- **EAS-10 (SHOULD):** A committed manifest/attestation SHOULD be immutable; correction SHOULD occur via an explicitly versioned superseding artifact under governance, not silent mutation (COMMIT-5).

### 9.4 What remains OPEN (EAS)

| Item | Status |
|---|---|
| Exact EAS **schema UID** and attested-field **ABI** | OPEN (O6) |
| **Resolver** presence/behaviour (e.g. access-control resolver, revocation policy) | OPEN (O6) |
| Concrete **attester/committer address(es)** and Safe topology (N-of-M + timelock) | OPEN (O6, O8) — registry-verified, owner-decided |
| Whether `signalRoot` is a plain Merkle root or an **EAS-resolver-bound** root | OPEN (O6) |
| Whether provenance and settlement commitments share one anchor or are two anchors sharing roots (§9.3 EAS-3) | OPEN (O6) |
| The precise **commitment/anchor contract** ("SettlementCoordinator" / manifest-commit contract) | OPEN (O6) — to-be-specified; **not** the v0 `AFIMintCoordinator` |

---

## 10. Conformance (schema-level)

A schema, manifest instance, generator, or document **conforms to this consolidation** iff all of the following hold (each restates an Accepted invariant; this document adds no new MUST beyond restatement and labelled PROPOSED items):

| # | Rule | Normative | Source |
|---|---|---|---|
| SC-1 | Exactly one committed manifest root per `epochId`; on-chain footprint is roots + hashes + pointers only. | MUST / MUST NOT(raw) | CONF-1, CONF-2 |
| SC-2 | `claimRoot` is produced off-chain under the frozen ruleset and is accompanied by reconciliation evidence tying it to the proof roots + `rulesetHash` + `totalRewardPool` (a reconciliation duty, **not** on-chain reward math). | MUST | MAN-S2, CONF-3 |
| SC-3 | Proof roots (`signalRoot`/`evidenceRoot`/`strategyRoot`) confer no entitlement; only `claimRoot` pays. | MUST | ROOT-1, PROV-NP-3 |
| SC-4 | Signal/evidence/strategy leaves carry no raw payloads/scores/blobs — only commitments + identity refs. | MUST NOT(raw) | BND-1, MAN-S3 |
| SC-5 | `disclosureWindow`/`disclosureStatus` govern visibility only and never gate payment. | MUST | DSC-3 |
| SC-6 | The manifest does not encode a single-`beneficiary`/`tokenAmount`/`receiptAmount` per-signal payout shape. | MUST NOT | MAN-S4, ECON-2 |
| SC-7 | Strategy/epoch receipt references are reputation (non-redeemable), decoupled from `claimRoot`. | MUST | STR-1, STR-2 |
| SC-8 | Concrete `contractAddresses` + `chainId` are authoritative; no ENS resolution for routing/authorization/attester. | MUST | CONF-10, EAS-6 |
| SC-9 | EAS anchoring commits roots only; `attestationUID` is not a payout instrument; provenance and funding are separate acts. | MUST | EAS-1, EAS-2, EAS-7 |
| SC-10 | Agent-built artifacts pass human/governance authorization before any anchor/commit/funding. | MUST | EAS-5, AGENT-2, CONF-9 |
| SC-11 | OPEN items (O1–O8) are carried as references/placeholders, never committed as final values; PROPOSED items are not cited as canon. | MUST NOT(final) | CONF-5, §0.1 |

---

## 11. Non-Goals

This document explicitly does **not**:

- **NG-1** Implement, deploy, anchor, commit, fund, or execute anything. It is design/spec only.
- **NG-2** Decide any tokenomics split (O3), holdback/vesting schedule (O4), unclaimed-reward policy (O2), reserve allocation (O5), clawback/escheatment mechanics (O1), push-vs-pull default (O7), or Safe topology (O8). These remain **OPEN**.
- **NG-3** Fix any EAS schema UID, resolver, attester address, hash domain, tree arity, or enum encoding (O6). The PROPOSED §5.5/§9 defaults are recommendations, not adoptions.
- **NG-4** Promote the strategy-leaf shape (§5.3) or the selective-disclosure flow (§8.4) to canon; they are **PROPOSED** pending owner/implementation review.
- **NG-5** Revive ERC-1155 as a receipt standard, replace xERC20, require ERC-7802, treat any ENS name as an authority, or bless/wire/extend the v0 `mintForSignal` flow or `AFIMintCoordinator`.
- **NG-6** Modify deployments, roles, Safe state, ENS records, funds, reward math, or production-sensitive configuration.
- **NG-7** Override the constitution or any Accepted Layer 1–4 spec. Where it appears to, the canonical doctrine wins and this document is to be corrected.

---

## 12. Open Questions

Carried verbatim from the constitution ([§6](./AFI_SETTLEMENT_V1_DOCTRINE.md#6-open-questions-not-settled)) plus schema-level opens surfaced by this consolidation. **None may be implemented as final.**

| ID | Open question | Disposition |
|---|---|---|
| O1 | Legal clawback / escheatment of unclaimed or challenge-failed rewards. | OPEN — legal/compliance |
| O2 | Unclaimed-reward policy (expiry; recycle vs. roll-forward vs. return-to-treasury). | OPEN — owner (placeholder hook only: `unclaimedRewardPolicyRef`) |
| O3 | Exact tokenomics **split values** across the three v1 claim roles (Providers / Analysts-Scorers / Validators). The **role set is closed to these three** (governance/public-goods out of scope, CLM-GOV); only the split *values* are OPEN. | OPEN — owner (not the `afi-econ` gauge) |
| O4 | Holdback / vesting schedule under challenge windows. | OPEN — owner (hook only: `holdbackPolicyRef`) |
| O5 | Reserve allocation and whether an L1 reserve vault exists. | OPEN — owner |
| O6 | Exact EAS schema/field encodings, hash domains, tree construction, `disclosureStatus` enum, `disclosureWindow` units, and the precise anchor contract. | OPEN — implementation (direction locked; §5.5/§9 are PROPOSED) |
| O7 | Push (router) vs. pull (claims) default distribution mode. | OPEN — owner (proof-based pull MUST exist at minimum) |
| O8 | Production Safe topology (N-of-M, signer set, timelock) for attester/committer/vault authority. | OPEN — owner (principle locked: not 1-of-1, addresses are truth) |
| S-A | Whether the **strategy leaf** (§5.3) is adopted as the canonical leaf under `strategyRoot`, and whether it binds a cleartext aggregate score or a `reputationCommitment`. | OPEN/PROPOSED — owner (ties to L2-O2/O5) |
| S-B | Whether the **PROPOSED leaf-encoding scheme** (§5.5) is adopted. | OPEN/PROPOSED — implementation (subset of O6) |
| S-C | Whether a **zero-knowledge** commitment scheme backs selective disclosure (§8.4 SD-3) or plain hash commitments + selective reveal. | OPEN/PROPOSED — implementation |
| S-D | Whether provenance (Layer 1) and settlement (Layer 3) share **one** anchor binding all four roots, or **two** anchors sharing roots (§9.3). | OPEN — implementation |

---

## 13. Relationship to Other Documents & Cross-Link Recommendations

### 13.1 Authority map

| Document | Relationship |
|---|---|
| [AFI_SETTLEMENT_V1_DOCTRINE.md](./AFI_SETTLEMENT_V1_DOCTRINE.md) | The constitution. This document is subordinate; it restates §15.1/§15.3 shapes and MUST NOT contradict §4, §7–§13, §15. |
| [AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md](./AFI_SIGNAL_PROVENANCE_AND_EAS_SCHEMA.md) | Layer 1 (canonical). Source of the signal/evidence leaves, `signalRoot`/`evidenceRoot`, `disclosureWindow`, EAS direction. |
| [AFI_EPOCH_SETTLEMENT_MANIFEST.md](./AFI_EPOCH_SETTLEMENT_MANIFEST.md) | Layer 3 (canonical). Source of the manifest field set and `claimRoot`/`strategyRoot` carriage. |
| [AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md](./AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md) | Layer 2 (canonical). Source of the receipt metadata the PROPOSED strategy leaf (§5.3) is derived from. |
| [AFI_REWARDS_VAULT_AND_CLAIMS.md](./AFI_REWARDS_VAULT_AND_CLAIMS.md) | Layer 4 (canonical). Source of the claim-leaf content and the enforce-not-decide payout law. |
| [AFI_ENS_SAFE_ADDRESS_REGISTRY_DOCTRINE.md](./AFI_ENS_SAFE_ADDRESS_REGISTRY_DOCTRINE.md) | Source of truth for `chainId`, `contractAddresses`, and attester/committer/vault authority (registry-verified, not ENS). |
| [AFI_V0_DEPRECATION_AND_MIGRATION.md](./AFI_V0_DEPRECATION_AND_MIGRATION.md) | Why v0 `mintForSignal` / `AFIMintCoordinator` / ERC-1155 `AFISignalReceipt` are deprecated and MUST NOT be wired as the v1 path. |
| ADRs [ADR-001](../adrs/ADR-001-four-layer-settlement-architecture.md) … [ADR-006](../adrs/ADR-006-unclaimed-rewards-legal-clawback-open.md) | The Locked Decisions this schema serves (four-layer model, ERC-6909, xERC20/ERC-7802, vault-Merkle claims, ENS-aliases, legal-clawback-OPEN). |
| [`afi-config` schemas/](../../afi-config/schemas/) | Home of the companion draft JSON schema (§14). |

### 13.2 Cross-link recommendations (advisory only — not applied here)

These are **recommendations** for the owner/maintainer. This document does **not** mass-edit the canonical specs; applying them is a separate, reviewed step.

- **XL-1 (recommend):** Add this document to the "Related Documents" list of Layer 1 and Layer 3 as the *consolidated manifest/provenance schema reference* (one line each), once it is reviewed and its status is raised from DRAFT.
- **XL-2 (recommend):** Add a row to [AFI_NORMATIVE_REGISTER.md](./AFI_NORMATIVE_REGISTER.md) for the companion draft schema (`afiEpochSettlementManifest.draft.schema.json`) once adopted, marking it **draft / non-implementation**.
- **XL-3 (recommend):** If the strategy-leaf shape (§5.3) is adopted, fold it into [AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md](./AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md) (or Layer 3) as the canonical leaf under `strategyRoot`, and resolve S-A.
- **XL-4 (recommend):** Record the `disclosureWindow` vs. "delayedDisclosureWindow" naming note (§4) wherever the prose term appears, to keep one canonical field name.
- **XL-5 (do NOT):** Do **not** add this draft to any contract, deployment manifest, runtime config, or registry that would imply implementation; it is specification only.

---

## 14. Companion Draft Machine-Readable Schema

A **draft, non-implementation** JSON Schema accompanies this document:

- [`../../afi-config/schemas/afiEpochSettlementManifest.draft.schema.json`](../../afi-config/schemas/afiEpochSettlementManifest.draft.schema.json)

It models the EpochSettlementManifest object (§3), the four roots (§4), and the four leaf shapes (§5) as a validation schema for **candidate** manifest documents. It is explicitly marked **DRAFT / non-implementation**: it fixes field **presence** (required arrays) per doctrine but deliberately leaves encodings permissive and OPEN (it does **not** constrain hash widths, enumerate role-split values, or define clawback mechanics). It MUST NOT be referenced by any contract, deployment, or runtime config, and it does not promote any PROPOSED item to canon.

---

## 15. Summary

This consolidation states, in one place, the **shape** of AFI Settlement v1's proof-to-money bridge: four roots (`signalRoot`, `evidenceRoot`, `strategyRoot` on the proof plane; `claimRoot` on the money plane), pinned by a shared `rulesetHash`, carried by an EpochSettlementManifest committed **once** per `epochId` on Base under human/governance authority, and anchored as an EAS-backed Merkle root whose exact schema is **OPEN**. Four leaf shapes feed the roots — **signal** and **evidence** (canonical), **claim** (canonical content), and **strategy** (**PROPOSED**). Raw data stays off-chain in the TSSD evidence vault until `disclosureWindow` elapses; only roots, hashes, and pointers are anchored. Participants can verify a signal, a reputation record, or a claim — and prove their own signal's inclusion without exposing proprietary raw data — trusting only chain data + the published manifest. **Provenance never pays; only the committed `claimRoot`, enforced by the RewardsVault, moves tokens.** Nothing here is implemented, and every undecided value remains **OPEN** or clearly **PROPOSED**.

---

*DRAFT consolidation — specification and design only. Implements, deploys, anchors, commits, and funds nothing. Subordinate to the constitution and the Accepted Layer 1–4 specs; where it appears to conflict, the canonical doctrine wins. OPEN items (O1–O8 and S-A…S-D) MUST NOT be implemented as final; PROPOSED items MUST NOT be cited as canon until adopted via change control. Does not bless or wire v0 `mintForSignal`, does not revive ERC-1155, does not replace xERC20, and treats ENS names as aliases only.*
