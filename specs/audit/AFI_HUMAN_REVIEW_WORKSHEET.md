# AFI Portable Protocol Audit — Human Review Worksheet (with references)

**Workspace root:** `/home/user/AFI-Protocol/` — each `afi-*` is its own git repo; open paths below from this root.

**Purpose:** Fill in decisions with **immediate links** to audit evidence and source files.

**Related:** [`AFI_TESTNET_E2E_CHECKLIST.md`](./AFI_TESTNET_E2E_CHECKLIST.md) — Base Sepolia MVP vs protocol-complete build path.

**Reviewer:** _________________________  
**Date:** _________________________

---

## Reference map (bookmark this)

### Audit reports (read these)

| Report | Path | Use for |
|--------|------|---------|
| **Master (start here)** | [`../AFI_PROTOCOL_SURFACE_AUDIT.md`](../AFI_PROTOCOL_SURFACE_AUDIT.md) | §1 scorecard, §1.3 blockers, §1.5 quick wins, §6 roadmap, §7 open questions |
| On-chain gap | [`../AFI_ONCHAIN_ANCHOR_GAP_ANALYSIS.md`](../AFI_ONCHAIN_ANCHOR_GAP_ANALYSIS.md) | Q2, B2 — §2 events/fields, §4 anchor gap, §8 recommendations |
| Replay matrix | [`../AFI_REPLAY_READINESS_MATRIX.md`](../AFI_REPLAY_READINESS_MATRIX.md) | Q1, B4, B8 — §2 six lifecycle stages |
| Contradictions | [`../AFI_CONTRADICTION_REGISTER.md`](../AFI_CONTRADICTION_REGISTER.md) | All tensions — §3 Mongo, §4 reactor, §5 BASE, §6 econ, §7 mint, §8 stale |
| Normative register | [`../AFI_NORMATIVE_REGISTER.md`](../AFI_NORMATIVE_REGISTER.md) | Q5–Q7, B3, B5 — what is protocol law today |
| Reference impl map | [`../AFI_REFERENCE_IMPL_MAP.md`](../AFI_REFERENCE_IMPL_MAP.md) | 31-repo table, reference spine |
| Your north star | [`../AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md`](../AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md) | Original portable-protocol intent |
| Checkpoint / DoD | [`./AFI_AUDIT_CHECKPOINT.md`](./AFI_AUDIT_CHECKPOINT.md) | Investigation complete? |

### Theme JSONs (primary evidence)

| Theme | File | Topics |
|-------|------|--------|
| C On-chain | [`./themes/C-onchain-anchor.json`](./themes/C-onchain-anchor.json) | B2, Q2 |
| D Vault / replay | [`./themes/D-evidence-vault.json`](./themes/D-evidence-vault.json) | B4, B7, B8, B10, Q6 |
| G Emissions / mint | [`./themes/G-emissions-mint.json`](./themes/G-emissions-mint.json) | B9, Q3, Q4 |
| A Normative | [`./themes/A-normative-surface.json`](./themes/A-normative-surface.json) | B3, B5, B6, Q7 |
| B Reference impl | [`./themes/B-reference-impl.json`](./themes/B-reference-impl.json) | B7, Mongo/reactor framing |
| E Scoring DAG | [`./themes/E-scoring-dag.json`](./themes/E-scoring-dag.json) | Reactor-as-law, Froggy pipeline |
| I SDKs / gateway | [`./themes/I-sdks-gateway.json`](./themes/I-sdks-gateway.json) | B1, B6, Q1 |
| H Governance | [`./themes/H-governance.json`](./themes/H-governance.json) | B9, Q4 |
| J Doc drift | [`./themes/J-docs-drift.json`](./themes/J-docs-drift.json) | Stale arch docs |
| F Analytics | [`./themes/F-analytics.json`](./themes/F-analytics.json) | Warehouse/analytics plane (absent); Mongo TSSD is the evidence store |
| **Verification** | [`./themes/verified.json`](./themes/verified.json) | 33/33 P0/P1 re-confirmed |

### Recon corpus

| Artifact | Path |
|----------|------|
| Full corpus | [`./recon/AFI_RECON_CORPUS.json`](./recon/AFI_RECON_CORPUS.json) |
| Human summary | [`./recon/AFI_RECON_SUMMARY.md`](./recon/AFI_RECON_SUMMARY.md) |
| Per-repo (example) | [`./recon/per-repo/afi-reactor.json`](./recon/per-repo/afi-reactor.json) |

---

## A. Verdict (~5 min)

**Read:** [`AFI_PROTOCOL_SURFACE_AUDIT.md` §1.1–§1.2](../AFI_PROTOCOL_SURFACE_AUDIT.md)

### A1. Accept overall alignment score?

Audit: **≈32/100** (partial / fragmented). Method: mean of five plane scores in [§1.1](../AFI_PROTOCOL_SURFACE_AUDIT.md).

- [ ] **Accept**
- [ ] **Accept with reservations** — disagree on: _________________________
- [ ] **Reject / re-audit** — reason: _________________________

### A2. Per-plane scores

**Read:** [§1.1 scorecard](../AFI_PROTOCOL_SURFACE_AUDIT.md) + plane evidence column.

| Plane | Audit /10 | Evidence to open | Your /10 | Notes |
|-------|-----------|------------------|----------|-------|
| Ingest | 4 | [`afi-gateway/src/http/app.ts`](../../../afi-gateway/src/http/app.ts) (4-field check) vs [`afi-reactor/src/server.ts`](../../../afi-reactor/src/server.ts) (AJV USS) | _____ | |
| Scoring DAG | 4 | [`afi-reactor/README.md`](../../../afi-reactor/README.md), [`afi-core/validators/UniversalWeightingRule.ts`](../../../afi-core/validators/UniversalWeightingRule.ts) | _____ | |
| Evidence | 4 | [`afi-infra/src/tssd/types.ts`](../../../afi-infra/src/tssd/types.ts), [`afi-infra/src/tssd/TSSDVaultClient.ts`](../../../afi-infra/src/tssd/TSSDVaultClient.ts) | _____ | |
| Commitment | 3 | [`afi-token/src/AFIMintCoordinator.sol`](../../../afi-token/src/AFIMintCoordinator.sol), [`afi-token/src/AFIToken.sol`](../../../afi-token/src/AFIToken.sol) | _____ | |
| Analytics | 1 | No hits in [`afi-config/schemas/`](../../../afi-config/schemas/) — see [`themes/F-analytics.json`](./themes/F-analytics.json) | _____ | |

### A3. What to keep (check)

| Item | Source file |
|------|-------------|
| [ ] 86B supply cap | [`afi-token/src/AFIToken.sol`](../../../afi-token/src/AFIToken.sol) — `TOTAL_SUPPLY_CAP` |
| [ ] `VaultedSignalRecord` lifecycle | [`afi-infra/src/tssd/types.ts`](../../../afi-infra/src/tssd/types.ts) ~L331 |
| [ ] Deterministic UWR math | [`afi-core/validators/UniversalWeightingRule.ts`](../../../afi-core/validators/UniversalWeightingRule.ts) |
| [ ] `ITSSDVaultClient` seam | [`afi-infra/src/tssd/TSSDVaultClient.ts`](../../../afi-infra/src/tssd/TSSDVaultClient.ts) |
| [ ] USS / schema library | [`afi-config/schemas/`](../../../afi-config/schemas/), [`afi-config/docs/AFI_CONFIG_OVERVIEW.md`](../../../afi-config/docs/AFI_CONFIG_OVERVIEW.md) |
| [ ] Other: _________________ | |

---

## B. Open questions (REQUIRED)

**Read first:** [Master §7](../AFI_PROTOCOL_SURFACE_AUDIT.md) · [North star §3–§5](../AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md)

---

### Q1 — Third-party validator promise (MOST IMPORTANT)

**What you're deciding:** Is portable-protocol / external replay a **hard v1.0 requirement**?

**Read before answering:**
- Your intent: [`AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md` §3.4, §5.5](../AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md)
- Escalation logic: [Master §1.4](../AFI_PROTOCOL_SURFACE_AUDIT.md)
- Evidence: [`themes/I-sdks-gateway.json`](./themes/I-sdks-gateway.json) · B1 in [§1.3](../AFI_PROTOCOL_SURFACE_AUDIT.md)
- Code/docs claiming "external layer" but no implementation:
  - [`afi-gateway/src/afiClient.ts`](../../../afi-gateway/src/afiClient.ts) ~L46
  - [`afi-reactor/src/config/froggyPipeline.ts`](../../../afi-reactor/src/config/froggyPipeline.ts) ~L93
- Verifier note: [`themes/verified.json`](./themes/verified.json) → search `I-sdks-gateway#2`

- [ ] **Yes — hard for v1.0** → B1 + B2 = **P0 blockers** ([§1.4](../AFI_PROTOCOL_SURFACE_AUDIT.md))
- [ ] **No — reference-stack v1.0 is OK** → B1/B2 stay P1; Phase 4 later
- [ ] **Hybrid:** _________________________

**My decision:** _________________________

---

### Q2 — Anchor specification (on-chain vs off-chain)

**What you're deciding:** What must live on BASE vs hash-anchored vs off-chain only?

**Read before answering:**
- [`AFI_ONCHAIN_ANCHOR_GAP_ANALYSIS.md` §2–§4, §8](../AFI_ONCHAIN_ANCHOR_GAP_ANALYSIS.md)
- [`themes/C-onchain-anchor.json`](./themes/C-onchain-anchor.json)
- Contracts: [`afi-token/src/AFIMintCoordinator.sol`](../../../afi-token/src/AFIMintCoordinator.sol), [`afi-token/src/AFISignalReceipt.sol`](../../../afi-token/src/AFISignalReceipt.sol)
- Deploy / roles: [`afi-token/script/DeployAFITokenMainnet.s.sol`](../../../afi-token/script/DeployAFITokenMainnet.s.sol)
- Off-chain spec: [`afi-infra/docs/TSSD_VAULT_SPEC.md`](../../../afi-infra/docs/TSSD_VAULT_SPEC.md)
- Contradiction: [Register §5 BASE-ledger](../AFI_CONTRADICTION_REGISTER.md)

| Data | On-chain full | Hash only | Off-chain only | Undecided |
|------|---------------|-----------|----------------|-----------|
| `signalId` + epoch | | | | |
| Mint amount + `beneficiary` | | | | |
| Scored payload / UWR axes | | | | |
| Ruleset / codex version | | | | |
| Enrichment snapshots | | | | |
| Receipt `publicSurface` | | | | |

**Minimum on-chain anchor for v1.0 (one sentence):**  
_________________________________________________________

**Sign-off for contract changes?** [ ] Yes  [ ] No  [ ] After security review

---

### Q3 — Emissions splits vs single beneficiary

**What you're deciding:** Are multi-recipient splits normative or research-only?

**Read before answering:**
- Research / splits: [`afi-econ/README.md`](../../../afi-econ/README.md), [`afi-econ/params/gauge_v0.yaml`](../../../afi-econ/params/gauge_v0.yaml) (if present)
- Theme: [`themes/G-emissions-mint.json`](./themes/G-emissions-mint.json)
- Production mint (single payee): [`afi-token/src/AFIMintCoordinator.sol`](../../../afi-token/src/AFIMintCoordinator.sol), [`afi-mint/src/orchestrator/MintExecutor.ts`](../../../afi-mint/src/orchestrator/MintExecutor.ts)
- Token docs (if any split language): [`afi-token/docs/`](../../../afi-token/docs/)
- Contradiction: [Register §6 econ-splits](../AFI_CONTRADICTION_REGISTER.md)

- [ ] **Normative** — implement splits in production
- [ ] **Research only** — single `beneficiary` is correct now
- [ ] **Future** — spec only, no implementation yet

**My decision:** _________________________

---

### Q4 — Governance / reputation vs deterministic mint

**What you're deciding:** Can Snapshot / reputation change mint outcome or amount?

**Read before answering:**
- Rule (reputation must NOT override scores): [`afi-config/docs/REGISTRIES_AND_REPUTATION.v0.1.md`](../../../afi-config/docs/REGISTRIES_AND_REPUTATION.v0.1.md)
- Theme: [`themes/H-governance.json`](./themes/H-governance.json), [`themes/G-emissions-mint.json`](./themes/G-emissions-mint.json)
- Implementation: [`afi-mint/src/orchestrator/SignalStateManager.ts`](../../../afi-mint/src/orchestrator/SignalStateManager.ts) ~L284
- Amount scaling: [`afi-mint/src/adapters/EmissionsMintDataProvider.ts`](../../../afi-mint/src/adapters/EmissionsMintDataProvider.ts) ~L272
- Governance plane: [`afi-governance/`](../../../afi-governance/) README + schemas
- Blocker B9: [Master §1.3](../AFI_PROTOCOL_SURFACE_AUDIT.md)

- [ ] **No** — deterministic mint; governance = selection/allocation only
- [ ] **Yes, but pinned** — versioned rules + anchors required
- [ ] **Yes, as today** — accept current `afi-mint` behavior

**My decision:** _________________________

---

### Q5 — Vault engine portability

**What you're deciding:** Mongo-only OK as reference default, or require second engine?

**Read before answering:**
- Schema (4 engines listed): [`afi-config/schemas/vault.schema.json`](../../../afi-config/schemas/vault.schema.json) L14–23
- Only Mongo implemented: [`afi-infra/src/tssd/TSSDVaultClient.ts`](../../../afi-infra/src/tssd/TSSDVaultClient.ts) ~L197–201
- Mongo client: [`afi-infra/src/tssd/MongoTSSDVaultClient.ts`](../../../afi-infra/src/tssd/MongoTSSDVaultClient.ts)
- Reactor hard dependency: [`afi-reactor/src/services/tssdVaultService.ts`](../../../afi-reactor/src/services/tssdVaultService.ts)
- TSSD spec: [`afi-infra/docs/TSSD_VAULT_SPEC.md`](../../../afi-infra/docs/TSSD_VAULT_SPEC.md)
- Theme: [`themes/D-evidence-vault.json`](./themes/D-evidence-vault.json), [`themes/B-reference-impl.json`](./themes/B-reference-impl.json)
- Contradiction: [Register §3 Mongo-only](../AFI_CONTRADICTION_REGISTER.md)

- [ ] **Mongo reference default OK** — fix docs only (Phase 0 Q2)
- [ ] **Require second engine:** PostgreSQL / TimescaleDB / InfluxDB / other: _______
- [ ] **Schema-only** — no second adapter until post-v1.0

**My decision:** _________________________

---

### Q6 — Canonical scored record

**What you're deciding:** Which store owns SCORED lifecycle data?

**Read before answering:**
- Canonical type (TSSD): [`afi-infra/src/tssd/types.ts`](../../../afi-infra/src/tssd/types.ts) — `VaultedSignalRecord`, `stages.scored`
- Reactor scored store: [`afi-reactor/src/services/tssdVaultService.ts`](../../../afi-reactor/src/services/tssdVaultService.ts), [`afi-reactor/src/types/ReactorScoredSignalV1.ts`](../../../afi-reactor/src/types/ReactorScoredSignalV1.ts)
- Replay matrix SCORED row: [`AFI_REPLAY_READINESS_MATRIX.md` §2–§3](../AFI_REPLAY_READINESS_MATRIX.md)
- Theme: [`themes/D-evidence-vault.json`](./themes/D-evidence-vault.json) — B8
- Blocker B8: [Master §1.3](../AFI_PROTOCOL_SURFACE_AUDIT.md)

- [ ] **TSSD `stages.scored`** — reactor must write canonical vault
- [ ] **`reactor_scored_signals_v1`** — promote reactor doc to normative
- [ ] **Both** — sync rules: _________________________

**My decision:** _________________________

---

### Q7 — USS versioning

**What you're deciding:** Which USS is canonical ingest?

**Read before answering:**
- USS v1: [`afi-config/schemas/usignal/v1/`](../../../afi-config/schemas/usignal/v1/)
- USS v1.1: [`afi-config/schemas/usignal/v1_1/index.schema.json`](../../../afi-config/schemas/usignal/v1_1/index.schema.json)
- Overview conflict: [`afi-config/docs/AFI_CONFIG_OVERVIEW.md`](../../../afi-config/docs/AFI_CONFIG_OVERVIEW.md) ~L122 (`provenance.timestamp` required)
- Reactor validation: [`afi-reactor/src/server.ts`](../../../afi-reactor/src/server.ts) ~L211
- Gateway (weak check): [`afi-gateway/src/http/app.ts`](../../../afi-gateway/src/http/app.ts)
- Theme: [`themes/A-normative-surface.json`](./themes/A-normative-surface.json)

- [ ] **v1.1 only** — deprecate v1
- [ ] **v1 + v1.1 coexist** — document supersession
- [ ] **Undecided** — need: _________________________

**Retire mandatory `provenance.timestamp`?** [ ] Yes  [ ] No  [ ] Unsure

**My decision:** _________________________

---

## C. Blockers — rank your top 5

**Read:** [Master §1.3 full table](../AFI_PROTOCOL_SURFACE_AUDIT.md) · [Register §10](../AFI_CONTRADICTION_REGISTER.md)

| ID | Blocker (short) | Phase fix | Key files to open | Audit |
|----|-----------------|-----------|-------------------|-------|
| **B1** | No external-validator surface | 4 | [`afi-gateway/src/afiClient.ts`](../../../afi-gateway/src/afiClient.ts), [`themes/I-sdks-gateway.json`](./themes/I-sdks-gateway.json) | [§1.3](../AFI_PROTOCOL_SURFACE_AUDIT.md) |
| **B2** | No on-chain verifiability / content hash | 3 | [`afi-token/src/AFIMintCoordinator.sol`](../../../afi-token/src/AFIMintCoordinator.sol), [`AFI_ONCHAIN_ANCHOR_GAP_ANALYSIS.md`](../AFI_ONCHAIN_ANCHOR_GAP_ANALYSIS.md) | [§1.3](../AFI_PROTOCOL_SURFACE_AUDIT.md) |
| **B3** | 2/5 planes lack normative schema | 1 | [`afi-config/schemas/`](../../../afi-config/schemas/), [`themes/A-normative-surface.json`](./themes/A-normative-surface.json) | [§1.3](../AFI_PROTOCOL_SURFACE_AUDIT.md) |
| **B4** | No replay pinning on records | 2 | [`afi-infra/src/tssd/types.ts`](../../../afi-infra/src/tssd/types.ts), [`afi-reactor/src/dag/DAGExecutor.ts`](../../../afi-reactor/src/dag/DAGExecutor.ts) | [§1.3](../AFI_PROTOCOL_SURFACE_AUDIT.md) |
| **B5** | Lifecycle stage not in `afi-config` | 1 | [`afi-config/schemas/vault.schema.json`](../../../afi-config/schemas/vault.schema.json) vs [`afi-infra/src/tssd/types.ts`](../../../afi-infra/src/tssd/types.ts) L8–15 | [§1.3](../AFI_PROTOCOL_SURFACE_AUDIT.md) |
| **B6** | Gateway skips USS validation | 2 | [`afi-gateway/src/http/app.ts`](../../../afi-gateway/src/http/app.ts) vs [`afi-reactor/src/server.ts`](../../../afi-reactor/src/server.ts) | [§1.3](../AFI_PROTOCOL_SURFACE_AUDIT.md) |
| **B7** | Mongo-only evidence plane | 0–2 | [`vault.schema.json`](../../../afi-config/schemas/vault.schema.json), [`TSSDVaultClient.ts`](../../../afi-infra/src/tssd/TSSDVaultClient.ts) | [§1.3](../AFI_PROTOCOL_SURFACE_AUDIT.md) |
| **B8** | Scoring bypasses canonical vault | 2 | [`tssdVaultService.ts`](../../../afi-reactor/src/services/tssdVaultService.ts), [`ReactorScoredSignalV1.ts`](../../../afi-reactor/src/types/ReactorScoredSignalV1.ts) | [§1.3](../AFI_PROTOCOL_SURFACE_AUDIT.md) |
| **B9** | Governance can override mint | 2 | [`SignalStateManager.ts`](../../../afi-mint/src/orchestrator/SignalStateManager.ts), [`EmissionsMintDataProvider.ts`](../../../afi-mint/src/adapters/EmissionsMintDataProvider.ts) | [§1.3](../AFI_PROTOCOL_SURFACE_AUDIT.md) |
| **B10** | Vault immutability unenforced | 2 | [`REGISTRIES_AND_REPUTATION.v0.1.md`](../../../afi-config/docs/REGISTRIES_AND_REPUTATION.v0.1.md) vs [`MongoTSSDVaultClient.ts`](../../../afi-infra/src/tssd/MongoTSSDVaultClient.ts) | [§1.3](../AFI_PROTOCOL_SURFACE_AUDIT.md) |

**Rank your top 5 (1 = highest):**

| Rank | ID | Phase |
|------|-----|-------|
| ___ | B__ | |
| ___ | B__ | |
| ___ | B__ | |
| ___ | B__ | |
| ___ | B__ | |

**Dispute / downgrade (why):** _________________________  
**Missing blockers:** _________________________

---

## D. Phase 0 quick wins (doc hygiene)

**Read:** [Master §1.5](../AFI_PROTOCOL_SURFACE_AUDIT.md) — check what to do first sprint.

| Done? | ID | What | Files to edit |
|-------|-----|------|---------------|
| [ ] | Q1 | Fix CI schema gate (`validate:config` → `validate`) | [`afi-config/.github/workflows/ci.yml`](../../../afi-config/.github/workflows/ci.yml), [`afi-config/package.json`](../../../afi-config/package.json) |
| [ ] | Q2 | Annotate vault engines (Mongo = reference default) | [`afi-config/schemas/vault.schema.json`](../../../afi-config/schemas/vault.schema.json), [`afi-infra/src/tssd/TSSDVaultClient.ts`](../../../afi-infra/src/tssd/TSSDVaultClient.ts) |
| [ ] | Q3 | Reframe reactor as reference orchestrator | [`afi-reactor/README.md`](../../../afi-reactor/README.md), [`afi-reactor/docs/AFI_ORCHESTRATOR_DOCTRINE.md`](../../../afi-reactor/docs/AFI_ORCHESTRATOR_DOCTRINE.md) |
| [ ] | Q4 | Reconcile `dag.codex.json` vs Froggy runtime | [`afi-reactor/config/dag.codex.json`](../../../afi-reactor/config/dag.codex.json), [`afi-reactor/src/config/froggyPipeline.ts`](../../../afi-reactor/src/config/froggyPipeline.ts) |
| [ ] | Q6 | Add `stage` enum to vault schema | [`afi-config/schemas/vault.schema.json`](../../../afi-config/schemas/vault.schema.json), copy enum from [`afi-infra/src/tssd/types.ts`](../../../afi-infra/src/tssd/types.ts) |
| [ ] | Q7 | Fix `afi-token` stale metadata | [`afi-token/.droid.json`](../../../afi-token/.droid.json), [`afi-token/.afi-codex.json`](../../../afi-token/.afi-codex.json) |
| [ ] | Q8 | Purge stale repo names; add canonical-doc banner | [`afi-docs/AFI_Repository_Map.md`](../../AFI_Repository_Map.md), [`afi-docs/ARCHITECTURE_STATUS.md`](../../ARCHITECTURE_STATUS.md) |
| [ ] | Q9 | Reconcile `provenance.timestamp` vs USS v1.1 | [`afi-config/docs/AFI_CONFIG_OVERVIEW.md`](../../../afi-config/docs/AFI_CONFIG_OVERVIEW.md), [`afi-config/schemas/usignal/v1_1/`](../../../afi-config/schemas/usignal/v1_1/) |
| [ ] | Q10 | Receipt URI / log-only provenance docs | [`afi-token/script/DeployAFITokenMainnet.s.sol`](../../../afi-token/script/DeployAFITokenMainnet.s.sol), [`afi-token/src/AFIMintCoordinator.sol`](../../../afi-token/src/AFIMintCoordinator.sol) |

**Phase 0 owner / date:** _________________________

---

## E. Solidification phases (what to build)

**Read:** [Master §6 roadmap](../AFI_PROTOCOL_SURFACE_AUDIT.md)

| Phase | Authorize? | Primary repos | Key deliverable |
|-------|------------|---------------|-----------------|
| [ ] **0** | Doc hygiene (§D above) | `afi-docs`, `afi-config`, `afi-reactor` | Honest labeling, CI gate works |
| [ ] **1** | Normative surface | [`afi-config/schemas/`](../../../afi-config/schemas/) | Commitment + lifecycle schemas (closes B3, B5) |
| [ ] **2** | Replay + evidence | [`afi-infra/`](../../../afi-infra/), [`afi-reactor/`](../../../afi-reactor/), [`afi-gateway/`](../../../afi-gateway/) | Pinning, canonical scored store (B4, B6, B8, B10) |
| [ ] **3** | On-chain anchors | [`afi-token/`](../../../afi-token/), [`afi-mint/`](../../../afi-mint/) | `contentHash`, `rulesetVersion` (B2) |
| [ ] **4** | External validator + Replay Contract | [`afi-gateway/`](../../../afi-gateway/), new spec in `afi-config` | Interop surface (B1) |

**First phase after Phase 0:** Phase _____

**In scope repos:** _________________________  
**Out of scope:** _________________________

---

## F. Charter v1.0 promotion

| Done? | Item | Location |
|-------|------|----------|
| [ ] | Promote after this worksheet | [`../AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md`](../AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md) → v1.0 |
| [ ] | Normative vs reference explicit | North star §4 |
| [ ] | Five-plane model | North star §3.2 |
| [ ] | On-chain/off-chain from Q2 | Your Q2 table above |
| [ ] | Replay contract checklist (even if not built) | North star §5.5 / Phase 4 spec |
| [ ] | Link six audit reports as evidence | [`../AFI_PROTOCOL_SURFACE_AUDIT.md`](../AFI_PROTOCOL_SURFACE_AUDIT.md) + siblings |

**Promote when?** [ ] After worksheet  [ ] After Phase 0  [ ] Not yet — need: ___________

---

## G. Spot-check (optional)

Pre-filled citations — open path, confirm audit claim, check box.

| Finding | Open this | OK? | Notes |
|---------|-----------|-----|-------|
| B2 no content hash | [`afi-token/src/AFIMintCoordinator.sol`](../../../afi-token/src/AFIMintCoordinator.sol) L19–26 | [ ] | |
| B6 gateway ingest | [`afi-gateway/src/http/app.ts`](../../../afi-gateway/src/http/app.ts) L26–27, L134 | [ ] | |
| B8 reactor scored store | [`afi-reactor/src/services/tssdVaultService.ts`](../../../afi-reactor/src/services/tssdVaultService.ts) | [ ] | |
| B7 Mongo-only | [`afi-infra/src/tssd/TSSDVaultClient.ts`](../../../afi-infra/src/tssd/TSSDVaultClient.ts) L197–201 | [ ] | |
| Reactor "ONLY orchestrator" | [`afi-reactor/README.md`](../../../afi-reactor/README.md) ~L137 | [ ] | |

---

## H. Sign-off

| Done? | Item |
|-------|------|
| [ ] | Investigation Phases 1–4 accepted ([`AFI_AUDIT_CHECKPOINT.md`](./AFI_AUDIT_CHECKPOINT.md)) |
| [ ] | Q1–Q7 answered in Section B |
| [ ] | Ready to assign Phase 0 / solidification |

| Action | Owner | Due |
|--------|-------|-----|
| Publish completed worksheet | | |
| Charter v1.0 draft | | |
| Phase 0 PRs | | |
| Next Factory / human implementation mission | | |

---

## I. Summary (fill last)

**AFI today vs v1.0 (one paragraph):**  
_________________________________________________________
_________________________________________________________

**Most important decision:** _________________________

**Not doing in next 90 days:** _________________________

---

*Save completed worksheet in `afi-docs/specs/audit/` or attach to a tracking issue. Paths assume monorepo at `/home/user/AFI-Protocol/`.*
