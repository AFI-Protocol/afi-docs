# AFI Signal Provenance and EAS Schema
**Status:** CANONICAL — Accepted (v1 doctrine)
**Date:** 2026-06-24
**Part of:** AFI Settlement v1 — see [AFI_SETTLEMENT_V1_DOCTRINE.md](./AFI_SETTLEMENT_V1_DOCTRINE.md)

> This is the **Layer 1** spec of the four-layer AFI Settlement v1 model (see doctrine §3). It governs **per-signal provenance** only. It defines *truth and authorship*, never *payment*. Where this spec and the constitution conflict on a v1 architecture question, the constitution wins. This document is **doctrine/design only**: nothing here is implemented, deployed, or executed, and no contract described here is built.

---

## 1. Scope and Position in the Stack

Layer 1 answers a single question: **"For a given epoch and strategy, which qualified signals existed, who authored them, and can a third party verify each one independently from chain data plus a published manifest — without trusting AFI's private infrastructure?"**

It does **not** answer who gets paid, how much, or when. Those are Layers 3 (EpochSettlementManifest) and 4 (RewardsVault). Per doctrine §3:

| Layer | Spec | This spec's relationship |
|-------|------|--------------------------|
| **1 — Per-signal provenance** | **this document** | Produces `signalRoot` / `evidenceRoot` leaves; anchors a batch root on Base. |
| 2 — Strategy/epoch reputation | [AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md](./AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md) | Layer 2 receipts **reference** the roots committed here; they are not payout. |
| 3 — Epoch settlement manifest | [AFI_EPOCH_SETTLEMENT_MANIFEST.md](./AFI_EPOCH_SETTLEMENT_MANIFEST.md) | The manifest **carries** `signalRoot` / `evidenceRoot` as proof inputs (doctrine §15.3). |
| 4 — Vault / claims | [AFI_REWARDS_VAULT_AND_CLAIMS.md](./AFI_REWARDS_VAULT_AND_CLAIMS.md) | MUST NOT read provenance leaves to decide payment. |

Background (descriptive, still accurate): the v0 anchor is "breadcrumb-only" — `MintCoordinated` carries no content/payload hash, ruleset version, or merkle commitment (verifiable directly against `afi-token/src/AFIMintCoordinator.sol`); its v1-conformance is **not** verified by this document. See also `../../reports/afi-signal-provenance-vs-reward-settlement-recon.md`.

---

## 2. Locked Direction

The **direction** below is locked v1 law (doctrine §15.1, ADR-001). The **schema details** (exact field encodings/types, the precise on-chain anchor contract, the exact EAS schema UID and field layout) remain **implementation design and are OPEN** (doctrine O6). This spec commits to field **presence and meaning**, not value-level encodings.

- **PROV-D1 (MUST):** Layer 1 commits provenance as an **EAS-backed Merkle batch ROOT anchored on Base**. The commitment is a **root**, not a per-signal artifact.
- **PROV-D2 (MUST):** **Batch-root-first.** Per-signal NFT minting (e.g. the v0 per-signal ERC-1155 `AFISignalReceipt` flow) MUST NOT be the v1 provenance mechanism. Per-signal provenance is realized as a **leaf under a committed root**, not as one token per signal.
- **PROV-D3 (MUST):** **Raw signal data stays off-chain** in the **TSSD evidence vault** (a *data* store; see §8) until the configured **delayed-disclosure** window elapses. Only roots, hashes, and pointers go on-chain (doctrine §7).
- **PROV-D4 (MUST):** **Every qualified signal remains independently verifiable** via a **manifest proof**: given the published manifest and the post-disclosure off-chain record, anyone MUST be able to reproduce the leaf and verify its inclusion under the committed root (doctrine §7, §15.1).
- **PROV-D5 (MUST):** EAS is the locked *direction* for attesting the batch root on Base. The **exact EAS schema** (schema UID, ABI of attested fields, resolver presence) is **OPEN** (O6) and MUST NOT be frozen into doctrine as final. Where this spec names EAS fields it does so as *design intent*, and any such field is OPEN at the encoding level.

> **Why batch-root-first, bluntly:** per-signal NFT/attestation minting couples gas and on-chain footprint to signal volume, invites the v0 "receipt = reward" confusion, and tempts implementers to put score/payload data on-chain. A batch root commits an unbounded set of signals in one anchor while keeping each signal independently provable. We do not claim the root contract is built; it is not.

---

## 3. The Provenance Non-Payment Law (hard boundary)

This is the load-bearing constraint of Layer 1. It restates doctrine L-SEP-1, D2, §8 for this spec and is non-negotiable.

- **PROV-NP-1 (MUST NOT):** **Provenance MUST NOT pay.** Recording a signal leaf, computing a `signalRoot`/`evidenceRoot`, or anchoring an EAS attestation MUST NOT mint, transfer, escrow, or earmark any reward token. Provenance ≠ payout.
- **PROV-NP-2 (MUST NOT):** **Provenance MUST NOT mint rewards.** No Layer 1 artifact (signal leaf, evidence leaf, batch root, or `attestationUID`) is redeemable, claimable, or convertible to AFI tokens, and none MAY be used as the unit of payout.
- **PROV-NP-3 (MUST):** A provenance leaf is a statement of **truth and authorship only**. Reward entitlement is established **solely** by inclusion in a committed `EpochSettlementManifest` `claimRoot` (Layer 3) and realized **solely** through the RewardsVault/claim layer (Layer 4).
- **PROV-NP-4 (MUST):** Anchoring a provenance batch root and funding/settling rewards MUST be **separate transactions, separate artifacts, and separate trust assumptions**. A single call MUST NOT both anchor provenance and move value (this is the v0 `mintForSignal` contradiction that v1 closes — doctrine §8, §5).

A verifier inspecting a `signalRoot` learns *that AFI committed to a set of authored, scored signals for this epoch/strategy*. It does **not** learn, and MUST NOT infer, that any payment occurred or is owed.

---

## 4. Anchor / Batch Fields (per strategy × epoch)

These are the per-batch anchor fields. They reuse doctrine §15.1 verbatim. A "batch" is the qualified-signal set for one `(strategyId, epochId)` (an implementation MAY further sub-batch; the root semantics are unchanged).

| Field | Meaning | Normative | On-chain? | OPEN at encoding? |
|-------|---------|-----------|-----------|-------------------|
| `epochId` | The epoch this batch belongs to (AFI weekly epoch; cadence is off-chain via `afi-math`). | MUST | yes (in anchor/manifest) | yes (id encoding) |
| `strategyId` | The strategy (provider methodology) the batch covers. | MUST | yes | yes |
| `signalRoot` | Merkle root over all **signal leaves** (§6) in this batch. The primary provenance commitment. | MUST | yes (root only) | yes (hash domain) |
| `evidenceRoot` | Merkle root over all **evidence leaves** (§7) for the batch's signals. Binds lifecycle/evidence snapshots. | MUST | yes (root only) | yes |
| `rulesetHash` | Pin of the exact scoring + validation (+ qualification) ruleset version used to produce/qualify these signals. Makes leaves reproducible. | MUST | yes | yes |
| `disclosureWindow` | The configured delayed-disclosure period (relative or absolute) after which raw off-chain data becomes inspectable for verification. | MUST | yes (as committed parameter) | yes (units/value OPEN) |
| `manifestURI` | Pointer to the off-chain manifest/index needed to reconstruct leaves and proofs (e.g. content-addressed URI). | MUST | yes (pointer) | yes |
| `attestationUID` | The EAS attestation identifier for this batch root **if and when** EAS anchoring is used. | MUST (if EAS) | yes | yes — **OPEN (O6)**: existence/format tied to final EAS schema |
| `disclosureStatus` | Current state of delayed disclosure for the batch (e.g. `WITHHELD` → `DISCLOSED`; see §5). | MUST | yes (status flag/commitment) | yes (enum encoding) |

**MUST NOT:** Raw per-signal arrays, scores, UWR axes, or evidence blobs MUST NOT appear in any anchor field. Only roots, the `rulesetHash`, the `disclosureWindow` parameter, `disclosureStatus`, and pointers (`manifestURI`, and via the manifest the `disclosureURI`) are anchored (doctrine §7).

---

## 5. Delayed Disclosure

Raw signal data is competitively sensitive: a trading signal disclosed in real time can be front-run or copied. v1 therefore **commits early, discloses late**.

- **DISC-1 (MUST):** At batch anchoring time, the `signalRoot` and `evidenceRoot` are committed, but the **raw signal payloads remain off-chain and withheld** in the TSSD evidence vault until `disclosureWindow` elapses.
- **DISC-2 (MUST):** The leaves are constructed over **content hashes / commitments** (`contentHash`, `scoreCommitment`, `evidenceHash`), so the root binds the *exact* off-chain content **without revealing it**. Disclosure later reveals the pre-images; it MUST NOT change any committed root.
- **DISC-3 (MUST):** `disclosureStatus` reflects the batch's disclosure state. The minimal lifecycle is:

  | `disclosureStatus` | Meaning | Verifier can reproduce leaves? |
  |--------------------|---------|--------------------------------|
  | `WITHHELD` | Root committed; pre-images not yet released. | No — can verify a root exists and is well-formed; cannot reproduce leaves from raw data yet. |
  | `DISCLOSED` | `disclosureWindow` elapsed; pre-images published (via `manifestURI` / the manifest's `disclosureURI`). | **Yes** — full leaf reproduction + inclusion check (§9). |

  Additional/intermediate states and the exact enum encoding are **OPEN** (O6); these two are the minimum a conforming implementation MUST support.
- **DISC-4 (MUST):** Disclosure status and timing relate to **provenance visibility only**. They MUST NOT gate, accelerate, or condition any reward payment (PROV-NP-1). Holdback/challenge windows that *do* affect payout are a Layer 3/4 concern (`challengeWindow`, `holdbackPolicyRef`) and are distinct from `disclosureWindow`.
- **DISC-5 (SHOULD):** The pre-image/disclosure reference SHOULD be content-addressed so that disclosure is verifiable (the published pre-images hash back to the committed leaves). The manifest carries this as `disclosureURI` (doctrine §15.3).

---

## 6. Signal Leaf Shape

One leaf per **qualified signal**. Fields are doctrine §15.1 verbatim. The leaf is a deterministic commitment; its exact serialization/hash domain is implementation design (OPEN, O6), but field presence and meaning are doctrine.

| Field | Meaning | Normative |
|-------|---------|-----------|
| `signalId` | Stable unique id for the signal (e.g. the TSSD/USS `provenance.signalId`). | MUST |
| `strategyId` | The strategy that produced the signal. MUST equal the batch `strategyId`. | MUST |
| `epochId` | The epoch the signal qualified in. MUST equal the batch `epochId`. | MUST |
| `contentHash` | Hash binding the signal's canonical off-chain content (raw + enriched record). The cryptographic tie to TSSD evidence; closes the v0 "no content hash on-chain" gap. | MUST |
| `scoreCommitment` | Commitment (hash) to the deterministic score/decision (e.g. UWR axes + composite + qualify flag). The **score itself stays off-chain**; only a commitment is bound. | MUST |
| `producer` | Identity **reference** of the signal's author/provider (a ref/id or address ref, not raw PII). | MUST |
| `timestamp` | The signal's authoritative time reference (e.g. scored-at). | MUST |
| `rulesetHash` | The ruleset version under which this signal was scored/qualified. MUST be consistent with the batch `rulesetHash`. | MUST |

**Notes (normative):**
- **MUST NOT:** The signal leaf MUST NOT contain the raw payload, the cleartext score, validator decisions, or UWR axis values — only `contentHash` and `scoreCommitment` over them.
- **MUST:** `signalId` + `strategyId` + `epochId` uniquely scope a leaf within a batch (no duplicate qualified signals per batch).
- A signal leaf is provenance, not payout (PROV-NP-2). `producer` being present in a leaf confers **no** token entitlement.

---

## 7. Evidence Leaf Shape

One or more leaves per signal **lifecycle stage**, capturing the off-chain evidence trail (RAW → ENRICHED → SCORED snapshots in the TSSD vault). Fields are doctrine §15.1 verbatim.

| Field | Meaning | Normative |
|-------|---------|-----------|
| `signalId` | The signal this evidence pertains to. MUST match a signal leaf `signalId` in the same batch. | MUST |
| `evidenceHash` | Hash of the lifecycle evidence snapshot (the RAW→…→SCORED record state being attested). | MUST |
| `stage` | The lifecycle stage the snapshot represents (e.g. `RAW`, `ENRICHED`, `SCORED`). | MUST |
| `disclosureStatus` | Disclosure state of *this* evidence snapshot (§5), which MAY differ per stage (e.g. enriched features disclosed later than raw). | MUST |

**Notes (normative):**
- **MUST:** `evidenceRoot` is the Merkle root over the batch's evidence leaves; it lets a verifier confirm that the disclosed lifecycle record is exactly what was committed.
- **MUST NOT:** The evidence leaf MUST NOT carry the snapshot contents — only `evidenceHash` over them.
- The naming law applies: "evidence" here is **data custody** in the TSSD vault, never token custody (doctrine §7). `evidenceRoot` does not pay anything.

---

## 8. Relationship to the TSSD Evidence Vault (data, off-chain)

The TSSD evidence vault is the **dense off-chain data store** that holds the raw + enriched + scored signal lifecycle (the `VaultedSignalRecord`: `identity.signalId`, `epochId`, `strategyId`, stage snapshots, outcome snapshot). It is **unchanged by Settlement v1** (doctrine §7) and is a **data** store, **not** a token vault.

- **TSSD-1 (MUST):** The dense record MUST live in the TSSD evidence vault off-chain. The Layer 1 leaves (§6, §7) are **commitments over** that record, not copies of it.
- **TSSD-2 (MUST):** `contentHash` (signal leaf) and `evidenceHash` (evidence leaf) MUST be computed over the canonical TSSD record content, so that disclosure reproduces them exactly.
- **TSSD-3 (MUST):** Raw TSSD data MUST remain withheld until `disclosureWindow` elapses (§5); the on-chain footprint is roots + `rulesetHash` + pointers only (doctrine §7).
- **TSSD-4 (MUST NOT):** "TSSD vault" / "evidence vault" MUST NOT be conflated with "RewardsVault" / "TreasuryVault" (token custody). Layer 1 touches only the data vault and MUST NOT touch token vaults (PROV-NP-1, doctrine §7 naming law).
- **TSSD-5 (SHOULD):** The vault's `publicSurface` (explorer-safe projection) SHOULD be the disclosure surface served at/after disclosure, consistent with the committed roots.

> The TSSD vault is the **dense brain**; the on-chain root is the **immutable commitment**. Disclosure is the bridge: post-window, the off-chain record + manifest let anyone reproduce and verify every leaf.

---

## 9. How a Verifier Reproduces a Leaf and Checks Inclusion

This is the independent-verifiability procedure required by doctrine §7 / PROV-D4. It assumes the batch is `DISCLOSED` (pre-images available) for full leaf reproduction.

**Inputs the verifier needs (all public or post-disclosure):**
1. The on-chain anchor: `signalRoot`, `evidenceRoot`, `rulesetHash`, `epochId`, `strategyId`, `disclosureWindow`, `disclosureStatus`, and `attestationUID` (if EAS) — committed for the batch and also carried in the EpochSettlementManifest (§10).
2. `manifestURI` → the off-chain manifest/index; and the manifest's `disclosureURI` → the disclosed pre-images (raw + enriched + scored record from the TSSD `publicSurface`).
3. The Merkle proof (sibling path) for the target leaf, from the manifest/index.

**Procedure for a single qualified signal:**
1. **Fetch** the disclosed off-chain record for `signalId` (post-window) via `manifestURI` / `disclosureURI`.
2. **Recompute the commitments:** derive `contentHash` over the canonical content and `scoreCommitment` over the disclosed score/decision, using the **exact ruleset** identified by `rulesetHash`. Independently recompute `rulesetHash` from the published ruleset and confirm it matches the anchor.
3. **Reconstruct the signal leaf** from `{signalId, strategyId, epochId, contentHash, scoreCommitment, producer, timestamp, rulesetHash}` using the canonical serialization, and hash it to the leaf digest.
4. **Verify inclusion:** apply the supplied Merkle proof to the leaf digest and confirm it reduces to the committed `signalRoot`.
5. **Reconstruct + verify each evidence leaf** `{signalId, evidenceHash, stage, disclosureStatus}` against `evidenceRoot` the same way, confirming the disclosed lifecycle snapshots hash to the committed `evidenceHash` values.
6. **Confirm the anchor is real:** check the `signalRoot`/`evidenceRoot` against the on-chain anchor (and, if EAS, that `attestationUID` resolves to an attestation committing these roots for this `epochId`/`strategyId`).

**Outcome:** if steps 2–6 pass, the verifier has *independently* confirmed that this signal was authored, scored under the named ruleset, and committed in the batch root — **without trusting AFI's private infrastructure**, and **without any payment having occurred**. A `WITHHELD` batch supports only the existence/well-formedness checks (step 6) until disclosure.

```
disclosed record ──hash(ruleset@rulesetHash)──► contentHash, scoreCommitment
        │                                              │
        ▼                                              ▼
   evidence leaf ──┐                            signal leaf
        │          │                                 │
   merkle proof    │                            merkle proof
        ▼          │                                 ▼
   == evidenceRoot │                            == signalRoot
        └──────────┴──► both roots == on-chain anchor (EAS attestationUID, if used)
                          ⇒ signal independently verified  (NO payout implied)
```

---

## 10. Relationship to the EpochSettlementManifest (Layer 3)

The EpochSettlementManifest (doctrine §15.3) is the bridge between **proof** (Layers 1–2) and **money** (Layer 4). Layer 1 feeds it the proof inputs.

- **MAN-1 (MUST):** The manifest **carries** Layer 1's `signalRoot` and `evidenceRoot` (alongside `strategyRoot` and the payout `claimRoot`) and the shared `rulesetHash`, plus `manifestURI` / `disclosureURI` pointers (doctrine §15.3). Layer 1 produces these roots; Layer 3 commits them once per epoch.
- **MAN-2 (MUST):** A reward is owed **only** via the manifest's `claimRoot` (Layer 3) and paid **only** by the RewardsVault (Layer 4). The `signalRoot` / `evidenceRoot` are **proof of provenance**, never proof of entitlement (PROV-NP-3, doctrine L-SEP-3/L-SEP-4).
- **MAN-3 (MUST NOT):** No contract downstream of the manifest — and in particular the RewardsVault — MUST recompute eligibility from provenance leaves or treat a `signalRoot` inclusion as a claim. Provenance roots and the `claimRoot` are **distinct roots with distinct authority**.
- **MAN-4 (MUST):** Anchoring the Layer 1 batch root (provenance) and committing the manifest (settlement authority) are separate acts; provenance anchoring MUST be possible **without** any manifest commitment or funding (PROV-NP-4).

This preserves the core v1 separation: Layer 1 proves *what is true*; Layer 3 decides *who is owed*; Layer 4 *pays*, strictly against the manifest root.

---

## 11. Conformance Checklist (Layer 1)

A document, schema, or contract conforms to this spec iff:

1. Provenance is committed as an **EAS-backed Merkle batch root on Base**, **batch-root-first**, with **no per-signal NFT minting** as the v1 mechanism (PROV-D1, PROV-D2).
2. Raw signal data stays **off-chain in the TSSD evidence vault** until `disclosureWindow` elapses; only roots/hashes/pointers are anchored (PROV-D3, §8).
3. Every qualified signal is **independently verifiable** via the manifest-proof procedure of §9 (PROV-D4).
4. The anchor fields (§4), signal leaf (§6), and evidence leaf (§7) carry exactly the doctrine §15.1 fields, by meaning.
5. **Provenance MUST NOT pay and MUST NOT mint rewards** (§3); reward entitlement comes only from the Layer 3 `claimRoot` and Layer 4 vault.
6. Value-level specifics (exact EAS schema/UID, hash domains, `disclosureStatus` enum, `disclosureWindow` units, anchor contract) are treated as **OPEN (O6)** and not frozen as final.

---

## 12. Related Documents

- Constitution: [AFI_SETTLEMENT_V1_DOCTRINE.md](./AFI_SETTLEMENT_V1_DOCTRINE.md) (§3, §7, §8, §15.1, O6).
- Layer 2: [AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md](./AFI_ERC6909_STRATEGY_EPOCH_RECEIPTS.md).
- Layer 3: [AFI_EPOCH_SETTLEMENT_MANIFEST.md](./AFI_EPOCH_SETTLEMENT_MANIFEST.md).
- Layer 4: [AFI_REWARDS_VAULT_AND_CLAIMS.md](./AFI_REWARDS_VAULT_AND_CLAIMS.md).
- Addresses/ENS/Safe source of truth: [AFI_ENS_SAFE_ADDRESS_REGISTRY_DOCTRINE.md](./AFI_ENS_SAFE_ADDRESS_REGISTRY_DOCTRINE.md).
- v0 posture: [AFI_V0_DEPRECATION_AND_MIGRATION.md](./AFI_V0_DEPRECATION_AND_MIGRATION.md).
- Background (descriptive): the v0 "breadcrumb-only" `MintCoordinated` anchor and its gaps, verifiable against `afi-token/src/AFIMintCoordinator.sol` (carried as background only, v1-conformance **unverified** here — not one of the Layer 1–4 docs under review); `../../reports/afi-signal-provenance-vs-reward-settlement-recon.md`.

---

*Canonical Layer 1 doctrine. Design only — nothing here is implemented, deployed, or executed. The provenance direction (EAS/Merkle batch root, batch-root-first, off-chain raw data, delayed disclosure, independent per-signal verifiability) is locked; exact EAS schema and field encodings are implementation design and remain OPEN (O6). Provenance ≠ payout: Layer 1 proves truth and authorship and MUST NOT pay or mint rewards.*
