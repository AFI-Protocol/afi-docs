# Report — AFI Settlement v1 Manifest + Provenance Schema Pass

**Date:** 2026-06-24
**Type:** Specification / interface pass (design only — implements nothing)
**Author scope:** schema consolidation of Layers 1 + 3; no Solidity, no deployments, no funds/roles/Safe/ENS changes
**Status of deliverables:** DRAFT — for review; **not committed, not pushed**

---

## 1. Summary

This pass produced a single precise, cross-layer **schema specification** for AFI Settlement v1's proof-to-money bridge, plus a companion **draft (non-implementation) JSON Schema**. It consolidates the already-canonical Layer 1 (signal provenance / EAS) and Layer 3 (epoch settlement manifest) shapes — the four roots, the four leaf shapes, the on-chain/off-chain boundary, the delayed-disclosure model, participant verification flows, and the EAS anchoring model — into one reference, reusing canonical field names verbatim and labelling everything undecided as `OPEN` or `PROPOSED`.

The pass was deliberately **additive and minimal-footprint**: three new files, no edits to any canonical doc, no runtime/config/contract changes. The new spec is explicitly **subordinate** to the constitution and the Accepted Layer 1–4 specs.

---

## 2. Files created / changed

| File | Repo | Status | Purpose |
|---|---|---|---|
| `afi-docs/specs/AFI_SETTLEMENT_V1_MANIFEST_AND_PROVENANCE_SCHEMA.md` | `afi-docs` | **created** (untracked) | The consolidated manifest+provenance schema spec (DRAFT). |
| `afi-config/schemas/afiEpochSettlementManifest.draft.schema.json` | `afi-config` | **created** (untracked) | Companion draft JSON Schema for a candidate manifest + leaf shapes; marked draft / non-implementation. |
| `afi-docs/reports/afi-settlement-v1-manifest-provenance-schema-report.md` | `afi-docs` | **created** (untracked) | This report. |

No existing files were modified. No files were deleted. The report was placed under the tracked `afi-docs/reports/` path (created in this pass) — **not** in the untracked root `reports/` directory, per instruction.

---

## 3. Key schema decisions proposed

These are the substantive design positions taken. **Canonical** = restated from existing doctrine; **PROPOSED** = new default offered for review, not yet Accepted.

1. **Two planes, four roots, one bridge (Canonical).** `signalRoot`, `evidenceRoot`, `strategyRoot` are the **proof plane**; `claimRoot` is the **money plane**; the EpochSettlementManifest is the only crossing, committed once per `epochId` on Base under human/governance authorization. `claimRoot` MUST reconcile to the proof roots + `rulesetHash` + `totalRewardPool` (MAN-S2).

2. **Four leaf shapes, with explicit canon-vs-proposed status:**
   - **Signal leaf** and **Evidence leaf** — **Canonical** (restated verbatim from Layer 1 §6/§7).
   - **Claim leaf** — **Canonical content** (`epochId, recipient, role, amount, leafIndex|nullifier`, optional `constraints`), encoding OPEN (Layer 4 §5.1 / ADR-004 D-V5). Per owner decision, the v1 **claim role set is exactly `Provider | Analyst-Scorer | Validator`** (Layer 4 §11 R-1); **governance and public-goods are out of scope** for v1 reward claims (see §10, CLM-GOV).
   - **Strategy leaf** — **PROPOSED**. The canonical docs commit a `strategyRoot` and define the ERC-6909 receipt, but never define the *leaf* under `strategyRoot`. A strategy-leaf field set is proposed, derived 1:1 from the receipt's committed metadata, and explicitly marked PROPOSED (open item S-A).

3. **`disclosureWindow` is the canonical field name (Canonical, naming reconciliation).** The mission brief used `delayedDisclosureWindow`; the canonical registry field is **`disclosureWindow`** (Layer 1 §4 / constitution §15.1), with "delayed-disclosure window" as the constitution's prose term for the same concept. The spec keeps `disclosureWindow` and explicitly declines to introduce a competing `delayedDisclosureWindow` field, to avoid forking the field registry.

4. **PROPOSED canonical leaf-encoding / hash-domain scheme (PROPOSED, subset of O6).** A concrete default — domain-separated `keccak256` leaf digests, sorted binary Merkle trees with duplicate rejection, `receiptId = keccak256(abi.encode(strategyId, epochId))` — is offered so implementers have an auditable starting point, while every encoding detail remains OPEN (O6) and the scheme is not cited as canon.

5. **Delayed disclosure is provenance-visibility only (Canonical).** `disclosureWindow`/`disclosureStatus` (`WITHHELD`→`DISCLOSED` minimum) govern when raw data is inspectable; they MUST NOT gate, accelerate, or condition payment. This is held strictly distinct from the payout-affecting `challengeWindow` / `holdbackPolicyRef`.

6. **Four participant verification flows (Canonical + one PROPOSED).** (a) verify one signal's inclusion/provenance; (b) verify one strategy/epoch reputation record; (c) verify one reward claim; (d) **PROPOSED** — verify without exposing proprietary raw signal data, via the existing commit/reveal model (existence pre-disclosure, selective single-leaf disclosure, commitment check without raw payload; optional ZK is OPEN). All four trust only chain data + the published manifest.

7. **EAS anchoring model stated at the schema level (Canonical direction; encodings OPEN).** What is attested = the batch root(s) + binding metadata (never raw data); who may attest/commit = a scoped agent MAY *build/submit*, but anchoring/commit is under documented Safe/governance authority (ENS never an attester); how it references the manifest = `attestationUID` ↔ committed root, mutually verifiable; what's OPEN = schema UID, resolver, attester address, tree/anchor specifics (O6/O8). The to-be-specified commitment contract is explicitly **not** the v0 `AFIMintCoordinator`.

8. **Draft JSON Schema fixes presence, not encoding (PROPOSED tooling).** Required-field arrays encode the doctrine MUST fields; encodings are left permissive (string commitments, no hash-width/units constraints); role-split values, clawback, holdback, and unclaimed-reward values are deliberately **not** modeled; OPEN items are annotated via `x-afiOpenItems` and `$comment`. It is marked draft / non-implementation and must not be referenced by any contract or runtime config.

---

## 4. Open questions (carried, not resolved)

All constitution OPEN items are carried as references/placeholders and **none is resolved or implemented as final**:

| ID | Open question | Disposition |
|---|---|---|
| O1 | Legal clawback / escheatment | OPEN — legal/compliance |
| O2 | Unclaimed-reward policy value (placeholder hook only) | OPEN — owner |
| O3 | Tokenomics **split values** across the three v1 claim roles (Providers / Analysts-Scorers / Validators); role set closed to these three (governance/public-goods out of scope, §10) | OPEN — owner |
| O4 | Holdback / vesting schedule (hook only) | OPEN — owner |
| O5 | Reserve allocation / L1 reserve vault | OPEN — owner |
| O6 | Exact EAS schema, hash domains, tree construction, enums, units, anchor contract | OPEN — implementation (direction locked) |
| O7 | Push vs. pull default (pull MUST exist at minimum) | OPEN — owner |
| O8 | Production Safe topology (attester/committer/vault) | OPEN — owner |

Schema-level opens surfaced by this pass (new):

| ID | Open question |
|---|---|
| S-A | Whether the **strategy leaf** (§5.3) is adopted as canonical, and whether it binds a cleartext aggregate score or a `reputationCommitment`. |
| S-B | Whether the **PROPOSED leaf-encoding scheme** (§5.5) is adopted. |
| S-C | Whether a **zero-knowledge** commitment scheme backs selective disclosure, or plain hash commitments + selective reveal. |
| S-D | Whether provenance (L1) and settlement (L3) share **one** anchor binding all four roots, or **two** anchors sharing roots. |

---

## 5. Contradictions / reconciliations found

No contradictions were found **between the canonical docs**; the Layer 1–4 specs, the constitution, and the ENS/Safe doctrine form a coherent, mutually consistent set. The items below are reconciliations between the *mission brief* and the *canonical registry*, plus one genuine specification **gap** (not a contradiction).

1. **Naming — `delayedDisclosureWindow` (brief) vs. `disclosureWindow` (canon).** The brief's root-semantics list named `delayedDisclosureWindow`; the canonical field is `disclosureWindow`. **Reconciled** by keeping the canonical name and documenting the prose-vs-field relationship (spec §4). No new field introduced. *Recommendation:* keep one canonical field name wherever the prose term appears (cross-link XL-4).

2. **"Strategy leaf" requested but not canonically defined (gap, not contradiction).** The brief asked for a strategy-leaf shape; the canonical docs define `strategyRoot` and the ERC-6909 receipt but **no strategy leaf**. **Resolved** by defining a PROPOSED strategy leaf derived from the receipt metadata and flagging open item S-A. This is a forward-fill, clearly labelled non-canonical.

3. **public-goods / governance vs. the v1 claim role set (resolved by owner decision, §10).** Canon (constitution §15.3, Layer 3 §2.3, Layer 4 §11, ADR-001/004) lists `public-goods` among the role-allocation set. The **owner decision (§10) removes governance/public-goods from the Settlement v1 reward/claim schema entirely**: v1 reward claims are a **three-way participant split** `Provider | Analyst-Scorer | Validator`. Governance MAY authorize/commit/administer protocol processes but MUST NEVER be a claimant; any future non-participant funding program requires a separate owner-approved spec/ADR. Because the canonical docs still list public-goods as a reward role, a **canonical follow-up cleanup** is required (NOT done in this pass) — enumerated in §10.1.

The background adversarial review surfaced **two additional wording nits** (FA-1, XDC-1), both confirmed against canon and **fixed**; details in §6.1. No substantive doctrinal contradiction was found in the new artifacts.

---

## 6. Validation performed

| Check | Tool | Result |
|---|---|---|
| New spec links resolve | python (relative-path resolver) | **21/21 relative link targets exist** |
| Draft JSON Schema is valid JSON | python `json` | **valid** |
| Draft JSON Schema is a valid Draft-07 schema | python `jsonschema` `Draft7Validator.check_schema` | **conforms** |
| Well-formed candidate manifest validates | python `jsonschema` | **validates** |
| Malformed manifests are rejected | python `jsonschema` (11 negative cases) | **all 11 rejected** (missing `claimRoot`, bad `role` enum, **`public-goods` as a claim role**, **`governance` as a claim role**, **`public-goods` as a `roleAllocationRoots` key**, claim leaf without `leafIndex`/`nullifier`, economics without any allocation, unknown top-level field, bad `disclosureStatus`, **`amount` as a JSON number**, **`amount` as a decimal string**, **`totalRewardPool` as a JSON number**) |
| Existing registry JSON still valid | python `json` | **valid** (untouched) |
| Adversarial conformance review (6 dimensions × verify) | multi-agent workflow | **see §6.1** |

`ajv` and `markdownlint` were not available in the environment; JSON Schema validation was performed with python `jsonschema` 4.23.0 (meta-validation + positive/negative instance tests), and link checking with a path resolver.

### 6.1 Adversarial conformance review results

A six-dimension adversarial review was run against the new spec and schema (8 agents, ~700k tokens, ~132s): **locked-decision conformance**, **forbidden-action guardrails**, **field-registry fidelity**, **OPEN/PROPOSED labelling**, **JSON-schema correctness**, and an independent **cross-document contradiction hunt**. Each dimension's findings were then re-checked by an independent skeptic that quoted the canonical source to confirm or refute.

**Outcome: 4 of 6 dimensions clean; 2 confirmed findings, both `nit` severity; no blockers, majors, or guardrail violations.**

| Dimension | Result |
|---|---|
| Locked-decision & layer-separation conformance (D1–D10, L-SEP-1…4) | **Clean** — no findings |
| Forbidden-action guardrails (no mintForSignal/ERC-1155/xERC20-replace/ERC-7802/ENS-authority/hard-coded-OPEN/implied-impl) | 1 `nit` (FA-1) |
| Field-registry & root/leaf fidelity (verbatim names) | **Clean** — no findings |
| OPEN/PROPOSED labelling discipline | **Clean** — no findings |
| Draft JSON-schema correctness & spec consistency | **Clean** — no findings |
| Independent cross-document contradiction hunt | 1 `nit` (XDC-1) |

Both confirmed nits were **fixed** in the spec:

- **FA-1 (forbidden-actions, nit) — fixed.** EAS-7 (§9.2) described the v0 `mintForSignal` anchor as an "event-only anchor," which understated it: `mintForSignal` mints the reward **and** an ERC-1155 `AFISignalReceipt` in a single call (mint-and-pay), recording provenance only as an event (no committed root). The normative content was already correct (MUST NOT wire/promote; D9). Reworded to describe the flow accurately. No endorsement of v0 was present; this was a wording-precision fix.
- **XDC-1 (contradiction-hunt, nit) — fixed.** §2 fact #3 read "the vault enforces *it* and never decides," where "it" bound the **one-root-per-epoch** invariant to the vault. Canonically, commit-once is enforced by the commitment/coordinator contract under Safe authority (COMMIT-2/COMMIT-3); the vault enforces the committed `claimRoot` for **payout** (L-SEP-4). The spec already attributed commit-once correctly at MAN-S5; the §2 sentence was reworded to match, removing the internal inconsistency.

Re-validation after the fixes: all 21 spec links still resolve; the draft schema still meta-validates and passes the positive/negative instance tests (the fixes touched prose only, not the schema).

---

## 7. Safety confirmation — no unsafe files touched

This pass made **no** changes to any production-sensitive surface. Confirmed:

- **No Solidity** authored or modified; no contract built, deployed, anchored, committed, or executed.
- **No deployments, roles, or Safe state** changed; no Safe threshold, signer, or role touched.
- **No ENS records** set, altered, renewed, unwrapped, or transferred.
- **No funds** moved; no minting, funding, or treasury action.
- **No tokenomics, reward math, or split values** decided; O3 left OPEN.
- **No clawback / escheatment / unclaimed-reward / holdback policy** hard-coded; O1/O2/O4 left as placeholder hooks only.
- **No production/runtime configuration** edited; the draft schema is non-implementation and unreferenced by any contract or config.
- **No v0 `mintForSignal` / `AFIMintCoordinator`** blessed, wired, or extended; **no ERC-1155** revived; **xERC20 retained**, **ERC-7802 deferred**; **ENS treated as alias only**.
- **No canonical doc mass-edited.** Cross-links were recorded as *recommendations only* (spec §13.2), not applied.

Working-tree state at report time (`git status --short`, repo-by-repo):

```
afi-docs (main):   ?? specs/AFI_SETTLEMENT_V1_MANIFEST_AND_PROVENANCE_SCHEMA.md
                   ?? reports/afi-settlement-v1-manifest-provenance-schema-report.md
afi-config (main): ?? schemas/afiEpochSettlementManifest.draft.schema.json
```

All three are **untracked (new)** files on `main`; nothing is staged or committed. No other AFI repo shows any change.

---

## 8. Disposition

- **Do not commit. Do not push.** Deliverables await owner review.
- Recommended next steps (owner-decided): review the PROPOSED items (strategy leaf S-A, leaf-encoding S-B, selective-disclosure/ZK S-C, single-vs-dual anchor S-D); on acceptance, raise the spec from DRAFT and apply the §13.2 cross-link recommendations (XL-1…XL-4); fold an adopted strategy leaf into the Layer 2/3 canon.

---

## 9. Owner-review patch applied (2026-06-24)

A focused owner-review patch was applied to the **same three draft files** (no other files touched; still uncommitted). Five decisions:

1. **`public-goods` demoted from the claim role set** (this step was **superseded by §10**, which removes it entirely). The v1 **claim role set is `Provider | Analyst-Scorer | Validator`** (Layer 4 §11 R-1). `definitions.role.enum` was reduced to the three roles; see **§10** for the final owner decision putting governance/public-goods fully out of scope.

2. **Manifest scope clarified as epoch-level.** Added a "Manifest scope (epoch-level)" note (§3.1): `epochId` is the single top-level scope key; **`strategyId` is NOT a top-level manifest field** — it is leaf/batch/receipt-scoped. The §4 `strategyId` row and the EAS §9.1 wording were updated so no "`(strategyId, epochId)`" pairing implies a single top-level manifest `strategyId`; per-strategy provenance batches roll up into the epoch-scoped manifest. (The schema already had `epochId` top-level and no top-level `strategyId`.)

3. **Token amounts tightened to string-encoded integer base units (draft schema).** `totalRewardPool` and claim `amount` changed from `["string","number"]` to `type:"string"` with `pattern:"^[0-9]+$"` and a `$comment` explaining this avoids JSON/IEEE-754 precision loss and **does not finalize tokenomics** (unit/decimals scale remains OPEN). Mirrored as a PROPOSED note in the spec rows (§3.3, §5.4).

4. **Push-vs-pull language tightened.** Added **CLM-0 (MUST)** to the spec (§5.4): **proof-based pull against `claimRoot` is the mandatory minimum**; a push-only design is non-conforming; push/distributor routing is OPEN/optional (O7) and never the sole path. Schema `distributor` and `roleAllocationLeaves` descriptions updated to state push is optional and `claimRoot` + claim verification remain mandatory.

5. **"claimRoot is a function of proof roots" reworded to avoid implying on-chain reward math.** MAN-S2 (§3.6), the §4 `claimRoot` row, the §8.3 verification step, and SC-2 (§10) now state: `claimRoot` is **produced off-chain from claim leaves generated under the frozen ruleset** and MUST be **accompanied by reconciliation evidence** tying it to the proof roots + `rulesetHash` + `totalRewardPool` — a reconciliation/audit duty, **not** an on-chain recomputation (the vault enforces, it does not decide). The reconciliation **invariant is preserved**; the wording no longer implies mechanical on-chain derivation.

**Re-validation after the patch:**

| Check | Result |
|---|---|
| Draft JSON Schema valid JSON + Draft-07 meta-schema | **conforms** |
| Well-formed candidate manifest validates (string amounts) | **validates** |
| Negative cases rejected | **9/9** at this step (later expanded to 11/11 in §10) |
| Spec relative links resolve | **21/21** |
| Only the 3 draft files changed | **confirmed** (afi-docs ×2, afi-config ×1; on `main`, untracked, uncommitted) |

No Solidity/deployment/runtime/Safe/ENS/funds/roles/tokenomics-finalizing change was introduced by the patch. **Still not committed, not pushed.**

---

## 10. Final owner decision — governance/public-goods removed from Settlement v1 claims (2026-06-24)

**Owner decision:** Settlement v1 rewards/claims are **exactly a three-way participant split — `Provider`, `Analyst-Scorer`, `Validator`**. **Governance must never be a claimant. Public-goods is not a Settlement v1 reward/claim role, claim track, claim-leaf role, `roleAllocationRoots` key, `roleAllocationLeaf` role, or budget line.** This **supersedes** the §9 decision-1 framing (which had retained public-goods as an OPEN/non-claimable budget line). Applied to the **same 3 draft files**; no other files touched.

**Changes (all OPEN/deferred/non-claimable/"possibly-future" public-goods wording removed from the v1 reward/claim schema):**

- *Spec* `AFI_SETTLEMENT_V1_MANIFEST_AND_PROVENANCE_SCHEMA.md`:
  - §3.3 economics row: removed the `public-goods` budget-line clause; now "three — and only three — v1 claim tracks," with an explicit "governance and public-goods are out of scope" MUST NOT.
  - §5.4 claim-leaf `role` row: "exactly `Provider | Analyst-Scorer | Validator`"; "governance and public-goods are NOT claim roles and MUST NEVER be claimants."
  - §5.4 added **CLM-GOV (MUST NOT)**: governance/public-goods out of scope for v1 reward claims; governance MAY authorize/commit/administer but MUST NEVER be a claim role/track/leaf-role/allocation-key/budget line; any future non-participant funding program requires a **separate owner-approved spec/ADR** and MUST NOT be encoded into v1 `claimRoot` semantics.
  - §12 O3 row: scoped to the three roles' **split values**; role set declared closed (governance/public-goods out of scope).
- *Schema* `afiEpochSettlementManifest.draft.schema.json`:
  - `definitions.role`: description rewritten — three-way split; governance/public-goods out of scope; no OPEN/budget-line language.
  - `economics.roleAllocationRoots`: **`public-goods` property removed**; keys are exactly the three claim roles, `additionalProperties:false` rejects any other key; added `$comment` recording the CLM-GOV exclusion.
  - (Claim leaves already constrained to the three-role enum, so a public-goods/governance claim leaf is rejected.)
- *Report:* §3, §5, §6, and this §10 updated; §9 decision-1 marked superseded.

**Re-validation after the final patch:**

| Check | Result |
|---|---|
| Draft JSON Schema valid JSON + Draft-07 meta-schema | **conforms** |
| Well-formed manifest (three roles only) validates | **validates** |
| Negative cases rejected | **11/11** — incl. **`public-goods` as claim role**, **`governance` as claim role**, **`public-goods` as a `roleAllocationRoots` key**, plus the prior 8 (missing `claimRoot`, bad role enum, no `leafIndex`/`nullifier`, no allocation, unknown top-level field, bad `disclosureStatus`, `amount`/`totalRewardPool` as JSON number, decimal-string amount) |
| Spec relative links resolve | **21/21** |
| Only the 3 draft files changed | **confirmed** |

**Prior owner-review improvements preserved (unchanged by this patch):** epoch-scoped manifest + no top-level `strategyId` (§3.1); string-encoded integer token amounts (§3.3/§5.4 + schema); mandatory pull/Merkle claim path (CLM-0); claimRoot reconciliation wording that avoids implying on-chain reward math (MAN-S2/§4/§8.3/SC-2).

### 10.1 Canonical docs needing follow-up cleanup (NOT edited in this pass)

The owner decision makes the following **canonical** references stale (they still list `public-goods` as a reward/allocation role). Per instruction these were **not** edited; they need a later owner-approved canonical cleanup (likely a small ADR or doctrine amendment), since the constitution's field registry currently includes public-goods:

| Doc | Line(s) | Reference to clean up |
|---|---|---|
| `afi-docs/specs/AFI_SETTLEMENT_V1_DOCTRINE.md` | 115 (O3), 230 (§15.3 economics) | `roleAllocation…` lists "Providers / Analysts-Scorers / Validators / public-goods" |
| `afi-docs/specs/AFI_EPOCH_SETTLEMENT_MANIFEST.md` | 85, 88, 90, 121 | `roleAllocationRoots` across "…/ public-goods"; ECON-1 residual "(e.g. … public-goods)"; ECON-3/§2.6 O3 splits |
| `afi-docs/specs/AFI_REWARDS_VAULT_AND_CLAIMS.md` | 106, 190, 251 | claim `role` "(Provider \| Analyst-Scorer \| Validator \| public-goods)"; §11 role table "public-goods (non-role budget)"; §15 field registry |
| `afi-docs/adrs/ADR-001-four-layer-settlement-architecture.md` | 37, 130 | "multiple roles (… / public-goods)"; O3 splits |
| `afi-docs/adrs/ADR-004-rewards-vault-merkle-claims.md` | 80, 145 | public-goods allocation; claim-leaf `role` "… / public-goods" |
| `afi-docs/specs/AFI_V0_DEPRECATION_AND_MIGRATION.md` | 87 | A5 replacement maps to roles "… / public-goods" |

Note: `ADR-006` line 30 mentions public-goods only as a *possible escheatment destination for forfeited funds* (O1, legal/compliance) — **not** a claim role — so it is **out of scope** of this decision and needs no cleanup. The constitution's O3 and the Layer-3/Layer-4 field registries are the load-bearing ones; aligning them to the three-role claim set is the recommended follow-up.

No Solidity/deployment/runtime/Safe/ENS/funds/roles/tokenomics-finalizing change was introduced by this patch. **Still not committed, not pushed.**

---

*Specification/interface pass only. No implementation, deployment, or production-sensitive change was made. Deliverables are DRAFT and uncommitted.*
