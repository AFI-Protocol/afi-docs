# AFI On-Chain Anchor Gap Analysis

**Phase 4 synthesis report — AFI Portable Protocol Audit**
**Inputs:** theme C (commitment layer / on-chain anchor) + theme G (emissions, mint, settlement) + `themes/verified.json`, grounded in live Solidity at `afi-token/src/*.sol` and the mint coordinator types.
**Status:** Staged in `afi-docs/specs/audit/final/`. Read-only forensic synthesis; no protocol code, schemas, or contracts were modified.

This report answers Core Question C9–C12 / G23–G26 of the North Star charter ([`AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md`](../../AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md) — the Commitment / BASE plane and the emissions→mint→settlement spine). It **enumerates every relevant Solidity event, struct, field, role, cap, and error** in the AFI commitment plane, then contrasts the **current on-chain breadcrumb anchor** against the **intended immutable commitment layer** the docs imply — partitioning each datum into *what is on-chain today*, *what should be hash-anchored*, and *what legitimately stays off-chain*.

All paths are relative to `/home/user/AFI-Protocol/`. P0/P1 items carry a **Verified** status drawn from `themes/verified.json` (Phase 3 adversarial re-confirmation).

---

## Related reports (siblings)

This is one of six cross-linked Phase-4 reports. All link back to [`AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md`](../../AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md):

- [`AFI_PROTOCOL_SURFACE_AUDIT.md`](./AFI_PROTOCOL_SURFACE_AUDIT.md) — master report (exec summary, 31-repo table, findings by severity, solidification roadmap).
- [`AFI_NORMATIVE_REGISTER.md`](./AFI_NORMATIVE_REGISTER.md) — every normative schema/invariant/contract; the commitment-plane law that lives only in Solidity (§S11–S12, contract C-MC).
- [`AFI_REFERENCE_IMPL_MAP.md`](./AFI_REFERENCE_IMPL_MAP.md) — per-repo classification; confirms `afi-token` is the sole commitment-plane impl and `afi-mint/contracts` / `afi-xerc20` are stub/vendored.
- [`AFI_CONTRADICTION_REGISTER.md`](./AFI_CONTRADICTION_REGISTER.md) — the `BASE-ledger`, `mint-model`, and `econ-splits` tensions enumerated here, with verified status.
- [`AFI_REPLAY_READINESS_MATRIX.md`](./AFI_REPLAY_READINESS_MATRIX.md) — the `MINTED` and `REPLAYED` stage rows depend on the anchor enumerated below.

---

## 1. Scope & method

The portable spec frames **BASE / on-chain** as the **Commitment plane** — the immutable, third-party-auditable layer that anchors what the off-chain Evidence and Scoring planes produced ([`AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md`](../../AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md)). The audit's verified finding is that the **entire AFI commitment plane is three Foundry/OpenZeppelin contracts in `afi-token/src`**: `AFIToken.sol` (ERC-20 emissions + cap), `AFIMintCoordinator.sol` (orchestration + provenance event), and `AFISignalReceipt.sol` (ERC-1155 receipts). The other candidate on-chain repos hold **no AFI commitment surface**:

- `afi-mint/contracts/*.sol` are empty stubs — `afi-mint/contracts/MintManager.sol:4-5` (`contract MintManager { // Stub for minting logic }`).
- `afi-xerc20` is a vendored third-party bridge fork — `afi-xerc20/package.json:6` (`"homepage": "https://github.com/defi-wonderland/xERC20#readme"`).

This report therefore enumerates `afi-token/src/*.sol` exhaustively. Method: every event/struct/field/role/cap/error below was read directly from source and carries a `file:line`; the gap analysis reuses `confirmed:true` evidence from `themes/verified.json`.

---

## 2. Full enumeration of the on-chain commitment surface (`afi-token/src/*.sol`)

### 2.1 Contracts

| Contract | Path (`file:line`) | Base | Role in commitment plane |
|----------|--------------------|------|--------------------------|
| `AFIToken` | `afi-token/src/AFIToken.sol:30` | `XERC20`, `AccessControl` | Canonical ERC-20; `mintEmissions` is the ONLY emissions entrypoint; holds the hard supply cap. |
| `AFIMintCoordinator` | `afi-token/src/AFIMintCoordinator.sol:13` | `AccessControl` | Orchestrates a token mint + receipt mint per signal; emits the sole provenance event. |
| `AFISignalReceipt` | `afi-token/src/AFISignalReceipt.sol:12` | `ERC1155`, `AccessControl` | Mints opaque ERC-1155 receipts for signal provenance. |

### 2.2 Events (the only on-chain provenance trail)

| # | Event signature | Path (`file:line`) | Indexed topics | What it anchors |
|---|-----------------|--------------------|----------------|-----------------|
| E1 | `EmissionsMinted(address indexed beneficiary, uint256 amount)` | `afi-token/src/AFIToken.sol:40` | beneficiary | Emitted on every emissions mint; carries recipient + amount only — no signal/epoch/score/hash. |
| E2 | `AdminUpdated(address indexed previousAdmin, address indexed newAdmin)` | `afi-token/src/AFIToken.sol:45` | previousAdmin, newAdmin | Role wiring breadcrumb (init emits `address(0)→admin`). |
| E3 | `EmissionsControllerUpdated(address indexed previousController, address indexed newController)` | `afi-token/src/AFIToken.sol:50` | previousController, newController | Role wiring breadcrumb for `EMISSIONS_ROLE`. |
| E4 | `MintCoordinated(bytes32 indexed signalId, uint256 indexed epochId, address indexed beneficiary, uint256 tokenAmount, uint256 receiptAmount)` | `afi-token/src/AFIMintCoordinator.sol:38-44` | signalId, epochId, beneficiary | **The provenance link.** Binds a mint to a signal+epoch — but emitted in logs only, never persisted to contract storage (see §4). |
| E5 | `ReceiptMinted(address indexed to, uint256 indexed id, uint256 amount, bytes data)` | `afi-token/src/AFISignalReceipt.sol:15` | to, id | ERC-1155 receipt mint; `id` is an opaque uint256, `data` an opaque blob the reference coordinator passes through. |

### 2.3 Structs

| # | Struct / field | Path (`file:line`) | Storage? | Notes |
|---|----------------|--------------------|----------|-------|
| ST1 | `struct MintRequest { … }` | `afi-token/src/AFIMintCoordinator.sol:19-26` | **calldata only** | The complete on-chain mint payload. Passed as `calldata` to `mintForSignal`; never written to a storage mapping. |
| — | `address beneficiary` | `afi-token/src/AFIMintCoordinator.sol:20` | calldata | Single payee (see G-anchor gap). |
| — | `uint256 tokenAmount` | `afi-token/src/AFIMintCoordinator.sol:21` | calldata | ERC-20 emission amount (wei). |
| — | `uint256 receiptId` | `afi-token/src/AFIMintCoordinator.sol:22` | calldata | Opaque ERC-1155 id. |
| — | `uint256 receiptAmount` | `afi-token/src/AFIMintCoordinator.sol:23` | calldata | ERC-1155 quantity. |
| — | `bytes32 signalId` | `afi-token/src/AFIMintCoordinator.sol:24` | calldata → **event only** | The signal provenance key; survives only as a `MintCoordinated` topic. |
| — | `uint64 epoch` | `afi-token/src/AFIMintCoordinator.sol:25` | calldata → **event only** | Epoch budget bucket; emitted as `epochId`. |
| — | `bytes extraData` | `afi-token/src/AFIMintCoordinator.sol:26` | calldata → forwarded | Forwarded to `mintReceipt` as ERC-1155 `data`; reference path supplies `0x`. |

> There is **no struct anywhere in `afi-token/src` with a content/payload hash, score, validator id, ruleset version, or UWR axis field.** `MintRequest` is the entire on-chain mint vocabulary.

### 2.4 Roles (AccessControl)

| # | Role constant | Path (`file:line`) | Holder (mainnet Pattern A) | Power |
|---|---------------|--------------------|----------------------------|-------|
| R1 | `DEFAULT_ADMIN_ROLE` (OZ) — `AFIToken` | granted `afi-token/src/AFIToken.sol:78` | Treasury Safe | Grants/revokes all roles on the token. |
| R2 | `EMISSIONS_ROLE = keccak256("EMISSIONS_ROLE")` — `AFIToken` | `afi-token/src/AFIToken.sol:32`; granted `:79` | Treasury Safe → coordinator | **Sole gate on `mintEmissions`.** |
| R3 | `DEFAULT_ADMIN_ROLE` (OZ) — `AFIMintCoordinator` | granted `afi-token/src/AFIMintCoordinator.sol:60` | Treasury Safe | Admin of the coordinator. |
| R4 | `EMISSIONS_ROLE = keccak256("EMISSIONS_ROLE")` — `AFIMintCoordinator` | `afi-token/src/AFIMintCoordinator.sol:14` | emissions agent | Gate on `mintForSignal`. |
| R5 | `MINT_COORDINATOR_ROLE = keccak256("MINT_COORDINATOR_ROLE")` — `AFISignalReceipt` | `afi-token/src/AFISignalReceipt.sol:13`; granted `:24` (admin only at deploy) | coordinator | Gate on `mintReceipt`. |

Mainnet "Pattern A" grants **both** `DEFAULT_ADMIN_ROLE` and `EMISSIONS_ROLE` to a single Treasury Safe — `afi-token/script/DeployAFITokenMainnet.s.sol:62-63` (`address admin_ = treasurySafe; address emissionsController_ = treasurySafe;`).

### 2.5 Caps, errors, and mint functions

| # | Item | Path (`file:line`) | Notes |
|---|------|--------------------|-------|
| C1 | `TOTAL_SUPPLY_CAP = 86_000_000_000 * 1e18` | `afi-token/src/AFIToken.sol:35` | Immutable constant; the one strong, independently-verifiable on-chain invariant. |
| C2 | cap enforcement | `afi-token/src/AFIToken.sol:97` (`if (totalSupply() + amount > TOTAL_SUPPLY_CAP) revert CapExceeded();`) | Reverts via `error CapExceeded()` at `afi-token/src/AFIToken.sol:53`. |
| F1 | `mintEmissions(address beneficiary, uint256 amount) external onlyRole(EMISSIONS_ROLE)` | `afi-token/src/AFIToken.sol:92` | ONLY emissions entrypoint; checks role + non-zero + cap; emits E1. |
| F2 | `mintForSignal(MintRequest calldata req) external onlyRole(EMISSIONS_ROLE)` | `afi-token/src/AFIMintCoordinator.sol:68` | Calls `token.mintEmissions(req.beneficiary, req.tokenAmount)` at `:76`; emits E4 at `:85`. |
| F3 | `mintReceipt(address to, uint256 id, uint256 amount, bytes calldata data) external onlyRole(MINT_COORDINATOR_ROLE)` | `afi-token/src/AFISignalReceipt.sol:35` | `_mint` at `:42`; emits E5 at `:44`. |

### 2.6 Persisted on-chain state (what an indexer-free reader can query)

Only four kinds of state actually live in contract storage: ERC-20 balances/`totalSupply()` (XERC20 base), ERC-1155 `balanceOf(to,id)`, `AccessControl` role maps, and the coordinator's two `immutable` wirings — `token` (`afi-token/src/AFIMintCoordinator.sol:16`) and `receipts` (`:17`). **`signalId`, `epochId`, `extraData`, amounts-per-signal, and any provenance live only in event logs.**

---

## 3. Docs-claim vs contract-encoding (C10)

| Doc claim | Where stated | What the contracts actually encode | Verdict |
|-----------|--------------|-------------------------------------|---------|
| "✅ No centralized control" / "✅ Codex replayable & auditable" | `afi-token/README.md:225`, `:227` | Pattern A grants admin+emissions to one Treasury Safe (`DeployAFITokenMainnet.s.sol:62-63`) which can mint to the 86B cap and grant/revoke every role; no score/replay data on-chain. | **Contradiction** (BASE-ledger). |
| BASE is the "canonical chain" holding a replayable provenance ledger | `afi-token/README.md:63`; contract NatSpec `AFIMintCoordinator.sol:38-44` ("provenance link between on-chain mints and off-chain DAG/TSSD") | Provenance is a single event topic-set (`MintCoordinated`); no payload/content hash, no score, no persisted record. | **Breadcrumb only.** |
| Off-chain codex publishes a MintReceipt anchor `{signal_id, score, mint_amount, validator_id, challenge_status, timestamp}` | `afi-mint/codex/mint_receipt_schema.json:6-13` | On-chain `MintRequest` is `{beneficiary, tokenAmount, receiptId, receiptAmount, signalId, epoch, extraData}` — no `score`/`validator_id`/`challenge_status`. | **Two divergent receipt dialects** (mint-model). |
| Receipts carry verifiable metadata | mainnet deploy URI | URI is a placeholder — `afi-token/script/DeployAFITokenMainnet.s.sol:103` (`"https://afi.protocol/receipts/{id}.json", // TODO: Update to production URI`); receipt id is opaque. | **Unresolved.** |

---

## 4. Current anchor vs intended immutable commitment layer (C12 / G gap)

### 4.1 What is anchored on-chain TODAY (the breadcrumb)

The anchor for a mint is the **`MintCoordinated` event** (E4): indexed `signalId` (bytes32), indexed `epochId`, indexed `beneficiary`, plus `tokenAmount`/`receiptAmount`. The ERC-1155 receipt (E5) carries an opaque `id` and a pass-through `data` blob. Because `signalId`/`epoch`/`extraData` are **emitted in logs, never written to storage** (`emit MintCoordinated(req.signalId, req.epoch, …)` at `afi-token/src/AFIMintCoordinator.sol:85`, `MintRequest` is `calldata` at `:19-26`), the signal→mint binding is recoverable **only by an event indexer**, not from contract state. If logs are pruned/missed, the provenance is unrecoverable on-chain.

### 4.2 What the docs IMPLY should be anchored (intended)

A codex-replayable commitment layer that cryptographically binds each mint to (a) the off-chain signal evidence that justified it, (b) the deterministic score/decision, and (c) the exact emissions ruleset version used to compute the amount — so a third party can independently verify legitimacy from chain data + published rules.

### 4.3 The three-way partition: on-chain vs hash-anchored vs off-chain

| Datum | Today | Intended placement | Rationale |
|-------|-------|--------------------|-----------|
| Token amount / `totalSupply` / 86B cap | **On-chain** (storage + `TOTAL_SUPPLY_CAP` `AFIToken.sol:35`) | **On-chain** (keep) | The one strong, verifiable invariant; must stay enforced in `mintEmissions`. |
| `signalId`, `epochId`, beneficiary | On-chain **event topics only** (`MintCoordinated`) | **On-chain, ideally persisted** (or accept documented log-only) | Provenance key; persisting a minimal anchor mapping removes the indexer dependency. |
| **Content/payload hash** of signal evidence | **Absent** — `MintRequest` has no hash field (`AFIMintCoordinator.sol:19-26`); scoped grep `contentHash\|payloadHash\|merkle\|rulesetVersion` over `afi-token/src` ⇒ 0 hits | **Hash-anchored** (add `contentHash`/`payloadHash` to `MintRequest`/receipt) | A single `bytes32` cryptographically binds the mint to immutable off-chain evidence without putting the evidence on-chain. |
| **Emissions ruleset version** | **Absent** on-chain; schedule is inlined/copied off-chain (`afi-mint/src/adapters/EmissionsMintDataProvider.ts:19`, `:51`) | **Hash-anchored** (pin a ruleset/version hash in the receipt) | Makes the amount reproducible; today the "canonical" `afi-math` schedule is duplicated and never on-chain authoritative (`afi-math/src/emissions/emissionsSchedule.ts:60`). |
| Score / UWR axes / validator id / decision | **Absent** on-chain | **Hash-anchored** (commit to a scoring record hash) | Score itself is proprietary → commit a hash, keep the detail off-chain. |
| Reputation weight `R`, `epochPulseFactor` (amount multipliers) | **Absent** on-chain (`EmissionsMintDataProvider.ts:272-273`, `:281`) | **Hash-anchored** as part of the amount-derivation record | Today they scale the minted amount but are not anchored, so the allocation is non-replayable. |
| Full signal payload, scoring formulas, DAG topology | Off-chain (afi-mint / afi-reactor / TSSD vault) | **Off-chain** (keep) | Bulk/proprietary data legitimately stays off-chain; the chain need only hold its hash. |
| Multi-role splits / gauge distribution | **Absent** on-chain (single `beneficiary` only) | **Off-chain / research** (afi-econ) unless promoted to a normative split | `afi-econ` gauge model is research-only (`afi-econ/params/gauge_v0.yaml:5-8`); not in any contract. |

**Headline gap (one sentence):** there is **no cryptographic binding** between the on-chain receipt/mint and the off-chain evidence + scoring + ruleset that justified it — the chain proves only that *an authorized role minted within the cap*, not that the mint was *legitimately scored or bound to real evidence*.

---

## 5. Third-party verifiability (C11)

From chain data alone a third party **CAN**: read `MintCoordinated`/`EmissionsMinted`/`ReceiptMinted`, confirm the beneficiary balance changed, and confirm `totalSupply() <= TOTAL_SUPPLY_CAP` (`afi-token/src/AFIToken.sol:97`). They **CANNOT** verify: (a) that `tokenAmount` matches the published emissions formula (no emissions math on-chain; it is off-chain in `afi-mint/src/adapters/EmissionsMintDataProvider.ts:277-281`, and the documented goldpaper `clamp(B(t)…)` form at `:11`/`:202` is not even the implemented formula); (b) that `signalId` corresponds to real scored evidence (no hash binds it); (c) that no governance challenge overrode the deterministic decision (`afi-mint/src/orchestrator/SignalStateManager.ts:284-286`). Verification therefore collapses to **fully trusting the `EMISSIONS_ROLE` holder** (the Treasury Safe) — `mintEmissions` is `onlyRole(EMISSIONS_ROLE)` (`afi-token/src/AFIToken.sol:92`) with no scoring/finality check.

---

## 6. Findings (P0/P1 carry verified status from `themes/verified.json`)

| ID | Finding | Severity | Verified (Phase 3) | Evidence (`file:line`) |
|----|---------|----------|--------------------|------------------------|
| theme:C-onchain-anchor#0 | No content/payload hash or ruleset-version anchored on-chain; receipts cannot be cryptographically bound to off-chain evidence. | **P1** | ✅ confirmed (P1) — grep `contentHash\|payloadHash\|merkle\|rulesetVersion` over `afi-token/src` ⇒ 0 hits | `afi-token/src/AFIMintCoordinator.sol:19-26` |
| theme:C-onchain-anchor#1 | Mint legitimacy gated only by `EMISSIONS_ROLE`; on-chain enforces no scoring/finality, so an external validator must fully trust the role holder. | **P1** | ✅ confirmed (P1) — considered P0 but a conforming validator can still interoperate | `afi-token/src/AFIToken.sol:92`; `afi-token/script/DeployAFITokenMainnet.s.sol:62-63` |
| theme:G-emissions-mint#3 | On-chain emissions legitimacy gated only by `EMISSIONS_ROLE` (one Treasury Safe); no schedule/epoch-cap/score enforced on-chain. | **P1** | ✅ confirmed (P1) | `afi-token/src/AFIToken.sol:92`, `:97`; `afi-token/script/DeployAFITokenMainnet.s.sol:62-63` |
| theme:G-emissions-mint#4 | On-chain mint is single-beneficiary; the multi-role gauge/splits model exists only in research (afi-econ). | **P1** | ✅ confirmed (P1) | `afi-token/src/AFIMintCoordinator.sol:19-26`, `:76`; `afi-econ/params/gauge_v0.yaml:5-8` |
| theme:H-governance#1 | Mint amount scaled by unpinned `reputationWeight` + governance `epochPulseFactor`, none anchored in the on-chain receipt → non-replayable allocation. | **P1** | ✅ confirmed (P1) | `afi-mint/src/adapters/EmissionsMintDataProvider.ts:272-273`, `:281`; `afi-token/src/AFISignalReceipt.sol:15`; `afi-token/src/AFIMintCoordinator.sol:19-26` |
| theme:G-emissions-mint#0 | Canonical emissions schedule is copy-pasted (inlined) into afi-mint instead of imported → drift risk in the replay-critical mint path. | **P1** | ✅ confirmed (P1) | `afi-mint/src/adapters/EmissionsMintDataProvider.ts:19`, `:51`; `afi-math/src/emissions/emissionsSchedule.ts:60` |
| theme:G-emissions-mint#1 | Documented goldpaper formula `clamp(B(t)…)` is not the implemented proportional-epoch-budget formula. | **P1** | ✅ confirmed (P1) | `afi-mint/src/adapters/EmissionsMintDataProvider.ts:11` vs `:277-281` (`:202` `baseMultiplier` unused) |
| C-anchor-P2a | `signalId`/`epoch`/`extraData` emitted in logs only, never persisted to storage → provenance depends on an indexer. | P2 | n/a (P2 not in verified ledger) | `afi-token/src/AFIMintCoordinator.sol:85`, `:19-26` |
| C-anchor-P2b | ERC-1155 receipt has a placeholder URI and no canonical per-receipt provenance metadata schema. | P2 | n/a | `afi-token/script/DeployAFITokenMainnet.s.sol:103`; `afi-token/src/AFISignalReceipt.sol:35-44` |
| C-anchor-Info | 86B hard supply cap enforced on-chain as an immutable constant — the one strong verifiable guarantee. | Info | n/a | `afi-token/src/AFIToken.sol:35`, `:97` |

---

## 7. Tensions surfaced (cross-link [`AFI_CONTRADICTION_REGISTER.md`](./AFI_CONTRADICTION_REGISTER.md))

- **BASE-ledger:** README markets "no centralized control / codex replayable" but the chain anchors only a breadcrumb and Pattern A centralizes mint authority in one Safe — `afi-token/README.md:225`, `:227` vs `afi-token/script/DeployAFITokenMainnet.s.sol:62-63`; `afi-token/src/AFIMintCoordinator.sol:85`.
- **mint-model:** off-chain `mint_receipt_schema.json` (`afi-mint/codex/mint_receipt_schema.json:6-13`) and the documented `clamp(B(t)…)` formula diverge from the on-chain `MintRequest`/implemented allocation — `afi-token/src/AFIMintCoordinator.sol:19-26`.
- **econ-splits:** multi-role gauge distribution is documented (`afi-econ/params/gauge_v0.yaml:5-8`) but the contract mints to a single beneficiary — `afi-token/src/AFIMintCoordinator.sol:76`.

---

## 8. Recommendations (commitment-layer solidification)

1. **Add a `bytes32 contentHash` (and `rulesetVersion`) to `MintRequest`/receipt** so each mint is cryptographically bound to its off-chain evidence and the exact emissions ruleset — closes the headline gap (theme:C#0).
2. **Persist a minimal anchor mapping** (`signalId → {epoch, contentHash}`) or explicitly document the log-only provenance assumption (theme:C#2).
3. **Replace the inlined afi-math schedule copy with a versioned import and pin the version on-chain/in-receipt** so amounts are reproducible (theme:G#0/#1).
4. **Document the trust boundary explicitly:** on-chain data attests *authorized-role-minted-within-cap* only; scoring/finality legitimacy is enforced off-chain by afi-mint before `EMISSIONS_ROLE` mints (theme:C#1, theme:G#3).
5. **Resolve the receipt URI + define a canonical receipt metadata schema** in `afi-config` (commitment-plane schema is currently absent — see [`AFI_NORMATIVE_REGISTER.md`](./AFI_NORMATIVE_REGISTER.md) §5).
6. **Decide splits-vs-single-beneficiary** in the normative spec: either specify a normative on-chain split/gauge or document that role splits are research-only (theme:G#4).

---

*End of report. Cross-links: [`AFI_PROTOCOL_SURFACE_AUDIT.md`](./AFI_PROTOCOL_SURFACE_AUDIT.md) · [`AFI_NORMATIVE_REGISTER.md`](./AFI_NORMATIVE_REGISTER.md) · [`AFI_REFERENCE_IMPL_MAP.md`](./AFI_REFERENCE_IMPL_MAP.md) · [`AFI_CONTRADICTION_REGISTER.md`](./AFI_CONTRADICTION_REGISTER.md) · [`AFI_REPLAY_READINESS_MATRIX.md`](./AFI_REPLAY_READINESS_MATRIX.md) · North Star: [`AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md`](../../AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md).*
