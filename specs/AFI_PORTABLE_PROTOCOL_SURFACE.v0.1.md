# AFI Portable Protocol Surface v0.1

> **AFI Settlement v1 note:** Parts of this document reference the **v0** per-signal mint / ERC-1155 receipt / direct-beneficiary path, which is **superseded as mainnet architecture** by AFI Settlement v1 — rewards settle **by epoch** through a RewardsVault / Merkle-claim layer funded from an EpochSettlementManifest, strategy/epoch receipts use **ERC-6909** (not ERC-1155), provenance is separated from payout, and ENS names are aliases (concrete addresses + chainId are the source of truth). See `afi-docs/specs/AFI_SETTLEMENT_V1_DOCTRINE.md` for the canonical architecture.

**Status:** Draft — direction-setting + investigation charter  
**Version:** 0.1  
**Date:** 2026-06-03  
**Audience:** Protocol architects, repo maintainers, in-house coding agent team  
**Purpose:** Capture the portable-protocol direction we have converged on, distinguish normative rules from reference implementations, and charter a full-org investigation to begin solidifying AFI along these lines.

---

## 1. Executive Summary

AFI was always intended to be a **portable protocol**: a thin, shared semantics layer that any validator, operator, or builder can implement on their own stack—so long as communication and commitment follow the rules. MongoDB, `afi-reactor`, and the current monorepo layout are **reference paths** built to learn the end-user journey. They are not the protocol itself.

The correct mental model is closer to **HTTP** than to “everyone runs our Mongo cluster”:

- **Normative:** what must be true for interoperability (schemas, lifecycle semantics, determinism, on-chain anchors).
- **Reference:** one working spine (gateway → reactor DAG → vault → mint on BASE) that demonstrates the rules in code.
- **Pluggable:** databases, DAG frameworks, analytics warehouses, and ingest pipelines—chosen per operator.

This document records that direction, names the layers, and lists known gaps between vision and encoded reality. The **agent investigation prompt** lives in a standalone companion doc: [`AFI_PROTOCOL_INVESTIGATION_PROMPT.md`](./AFI_PROTOCOL_INVESTIGATION_PROMPT.md) (see Section 8).

---

## 2. Background: How We Drifted (and Why That Is Normal)

Building AFI required concreteness. You cannot protocol-ize in the abstract forever; you need one working spine. The spine that emerged:

```
ingest (gateway/webhooks) → enrich + score (afi-reactor DAG) → persist (TSSD vault) → commit (BASE mint/receipt)
```

That spine is valuable. The trap is **narrative drift**: when collaborators (or future-you) read the spine as the spec. Rabbit holes amplified this—vault design, enrichment APIs, emissions math, mint FSM, econ simulation, doctrine docs—each layer has gravity. Over time “AFI” started to mean “this repo layout” instead of “these rules for proposing, enriching, scoring, committing, and challenging signal intelligence.”

**This document recenters the portable protocol** and charters work to solidify it.

---

## 3. Arrived-At Direction

### 3.1 One-Sentence North Star

> **AFI is the rules for how signal intelligence is proposed, enriched, scored, committed, and challenged—not the database or DAG framework used to build the first working example.**

### 3.2 Layer Model

AFI is best understood as **separated planes**, not one monolithic stack:

| Plane | Role | What strangers must agree on | Typical implementations (non-normative) |
|-------|------|------------------------------|-------------------------------------------|
| **Commitment** | Immutable attestation of what the network accepted | BASE: mint events, receipts, emissions caps, epoch linkage, content anchors/hashes (present + future) | `afi-token`, `afi-mint` |
| **Evidence** | Dense per-signal lifecycle for replay and challenge | Full RAW → ENRICHED → ANALYZED → SCORED → MINTED → REPLAYED record; public vs proprietary surface | Mongo, PostgreSQL, TimescaleDB, InfluxDB (per `vault.schema.json`) |
| **Scoring DAG** | Deterministic transforms on declared inputs | Pinned topology, plugin/analyst/validator versions; conforming outputs | `afi-reactor`, custom DAG, any conforming orchestrator (if outputs conform) |
| **Market / analytics** | Continuous context at scale (not per-signal canon) | Published feature schemas, snapshot refs for replay | warehouses/streams chosen per operator — non-normative, never AFI's evidence store |
| **Ingest boundary** | Valid entry dialect into the protocol | USS v1.1, CPJ v0.1, lens extensions | `afi-gateway`, webhooks, SDKs |

**Key rule:** Do not collapse commitment, evidence, and analytics into one store. A single-store design (whatever the engine) is wrong if it is the *only* layer.

### 3.3 The HTTP Analogy (Formal)

| HTTP | AFI portable protocol |
|------|------------------------|
| Request/response contract | USS / CPJ at ingest boundaries |
| Semantics (methods, status codes) | Lifecycle states, scored signal surface, epoch/mint semantics |
| Headers (content-type, cache-control) | Schema IDs, pipeline/DAG version pins, content hashes |
| Immutable audit (server logs, CDN edge) | BASE commitments (events, receipts) |
| Message body | Off-chain evidence vault (operator’s choice) |
| Client (curl, browser, fetch) | Reactor, custom Python, any conforming orchestrator |
| CDN / analytics / log pipeline | warehouses, streams, benchkit, research tooling |

HTTP did not mandate Apache. AFI must not mandate Mongo or `afi-reactor`—only **conforming artifacts and behavior**.

### 3.4 Decentralization: What “Follow the Rules” Means

Any validator or operator may erect their own database and DAG pipeline if:

1. **Canonical dialect** — Signals and outputs validate against declared `afi-config` schemas (USS, vault record, pipeline contracts, plugin manifests).
2. **Pinned transforms** — Pipeline/DAG identity and versions are recorded so replay is possible.
3. **Determinism** — Same inputs + same pinned rules ⇒ same scored outputs (modulo explicitly snapshotted external API data).
4. **Commitment linkage** — On-chain artifacts link to off-chain evidence via `signalId`, epoch, and (where specified) content hashes.
5. **Challenge-ready evidence** — Enough dense lifecycle data exists for an independent party on a different stack to reproduce or dispute.

Reputation, registries, and governance influence **selection and allocation**—they must not override deterministic scoring or protocol finality (`afi-config/docs/REGISTRIES_AND_REPUTATION.v0.1.md`).

### 3.5 BASE as Ledger

**Intended direction:** BASE is the **immutable commitment layer**—what the network agrees was scored, minted, and settled under which rules.

**Current encoded reality (partial):** On-chain today stores lightweight breadcrumbs (`MintCoordinated` / receipt metadata: `signalId`, epoch, amounts, beneficiary)—not full enrichment payloads or UWR axis breakdowns. Off-chain TSSD is the dense brain; receipt is the surface breadcrumb (`afi-infra/docs/TSSD_VAULT_SPEC.md`).

**Aspirational extension (not yet normative):** Richer on-chain anchors—hashes of canonical payloads, expanded receipt metadata, registries—for strangers to verify without trusting any operator’s Mongo.

---

## 4. Normative Surface vs Reference Implementation

### 4.1 Normative (Protocol Law)

Owned primarily by **`afi-config`** and cross-repo schema contracts:

| Artifact | Location (starting points) |
|----------|----------------------------|
| USS v1.1 | `afi-config/schemas/usignal/v1/` |
| CPJ | `afi-config` (CPJ v0.1) |
| Vault configuration | `afi-config/schemas/vault.schema.json` |
| Pipeline / blueprint contracts | `afi-config/schemas/pipeline.schema.json`, `blueprint.schema.json` |
| Plugin manifests | `afi-config/schemas/plugin-manifest.schema.json` |
| Registries & reputation invariants | `afi-config/docs/REGISTRIES_AND_REPUTATION.v0.1.md` |
| TSSD record shape & lifecycle | `afi-infra/docs/TSSD_VAULT_SPEC.md`, `afi-infra/src/tssd/types.ts` |
| Validator replay invariants | `afi-reactor/docs/VALIDATOR_REPLAY_SPEC.v0.1.md` |
| On-chain mint/receipt semantics | `afi-token/src/*.sol`, `afi-mint` orchestrator types |

### 4.2 Reference Implementation (Demonstration Spine)

Convenience defaults for the AFI org’s first end-to-end path—not binding on external validators:

| Component | Repo | Notes |
|-----------|------|-------|
| Ingest gateway | `afi-gateway` | Webhooks, tenant routing |
| Orchestrator / DAG | `afi-reactor` | Froggy pipeline, `pipelineRunner.ts` |
| Runtime agents/tools | `afi-core`, `afi-plugins` | Nodes invoked by DAG |
| Vault adapter | `afi-infra` | Mongo-oriented examples; multi-engine in schema |
| Mint pipeline | `afi-mint` | Off-chain FSM → on-chain `mintForSignal` |
| Contracts | `afi-token` | Emissions, coordinator, ERC-1155 receipts |
| Math | `afi-math` | Emissions schedule |

### 4.3 Known Tensions (To Resolve in Investigation)

These are **starting hypotheses** for the agent team to verify and expand:

| Tension | Symptom | Desired resolution |
|---------|---------|-------------------|
| Reactor as “the” orchestrator | `afi-reactor/docs/AFI_ORCHESTRATOR_DOCTRINE.md` §1 | Reframe: reactor is **reference orchestrator**; protocol law is conforming DAG outputs + pinned versions |
| Mongo tunnel vision | TSSD spec, gateway, reactor defaults | Docs/code should say “default reference vault”; schema already allows PG/Timescale/Influx |
| BASE = full signal ledger | User vision vs receipt-only contracts | Spec what **must** be on-chain vs hash-anchored vs off-chain only |
| Econ splits vs on-chain settlement | `afi-econ` gauge vs single `beneficiary` mint | Classify econ as research/simulation unless wired to production |
| Stale architecture docs | `afi-docs/AFI_Full_Architecture.md`, `AFI_Repository_Map.md` | Mark stale sections; align to portable protocol surface |
| Analytics/warehouse plane absent from normative layer | Considered, never built | Optional, non-normative; Mongo TSSD is the reference evidence store, warehouses pluggable per operator |

---

## 5. Solidification Goals

The investigation and follow-on work should move AFI toward:

1. **Published Protocol Surface** — Single doc (successor to this one) listing normative schemas, invariants, and on-chain/off-chain division of responsibility.
2. **Reference Implementation Index** — Which repos implement which spine segment; explicitly non-mandatory for external validators.
3. **Contradiction Register** — Every place code, docs, or comments imply Mongo-only, reactor-only, or full payload on-chain.
4. **Anchor Specification** — Minimum on-chain commitments + required off-chain evidence for replay/challenge (the “HTTP headers” of AFI).
5. **Replay Contract** — Cross-repo checklist: what a third-party validator needs to reproduce a mint decision without org infra.
6. **Doc hygiene** — Stale docs tagged; architecture maps updated or archived.

---

## 6. Investigation Outputs (Expected Artifacts)

The agent team should produce:

| Deliverable | Description |
|-------------|-------------|
| `AFI_PROTOCOL_SURFACE_AUDIT.md` | Master report with executive summary, findings, severity |
| `AFI_NORMATIVE_REGISTER.md` | Every normative schema, invariant, and contract with file paths |
| `AFI_REFERENCE_IMPL_MAP.md` | Per-repo: reference vs normative vs research vs stale |
| `AFI_CONTRADICTION_REGISTER.md` | Doc/code conflicts with portable-protocol direction |
| `AFI_REPLAY_READINESS_MATRIX.md` | Per lifecycle stage: what is stored, where, replayable? |
| `AFI_ONCHAIN_ANCHOR_GAP_ANALYSIS.md` | Current vs intended BASE commitment layer |
| Per-repo addenda | Short `PROTOCOL_CLASSIFICATION.md` stub or section in each repo (optional follow-up) |

Store master reports in **`afi-docs/specs/`** (or `afi-config/docs/` for normative register if appropriate after review).

---

## 7. Repo Inventory (Starting Point)

Audit **all repositories** in the AFI-Protocol GitHub organization—public **and** private—including any not present in the local workspace. Use `gh repo list <org> --limit 500` (or internal equivalent) to discover repos; do not rely only on the local monorepo folder.

**Known local workspace repos (non-exhaustive):**

`afi-artifacts`, `afi-assets`, `afi-benchkit`, `afi-cli-framework`, `afi-config`, `afi-core`, `afi-docs`, `afi-econ`, `afi-factory`, `afi-gateway`, `afi-governance`, `afi-infra`, `afi-labs`, `afi-math`, `afi-mint`, `afi-ops`, `afi-plugins`, `afi-protocol`, `afi-reactor`, `afi-research-site`, `afi-skills`, `afi-tiny-brains`, `afi-token`, `afi-xerc20`

Also check for renamed, archived, or external-reference repos (e.g. historical `afi-pipeline` references in older docs).

---

## 8. Agent Investigation Prompt

The full copy-paste prompt for the in-house coding agent team lives in a **standalone document** for easy distribution:

**→ [`AFI_PROTOCOL_INVESTIGATION_PROMPT.md`](./AFI_PROTOCOL_INVESTIGATION_PROMPT.md)**

That file contains:

- Usage instructions (read companion spec first, grant org-wide read access)
- The complete investigation mission, constraints, and 30 core questions (A–J)
- Per-repo checklist template, search patterns, deliverables, severity rubric, and definition of done

**Quick start for maintainers:**

1. Open [`AFI_PROTOCOL_INVESTIGATION_PROMPT.md`](./AFI_PROTOCOL_INVESTIGATION_PROMPT.md).
2. Copy everything below the horizontal rule into the agent system or task prompt.
3. Grant read access to all AFI-Protocol org repos (public and private).

---

## 9. Next Steps (Human)

1. **Resume in-progress audit** — Phase 1 recon is complete; use [`audit/AFI_AUDIT_CHECKPOINT.md`](./audit/AFI_AUDIT_CHECKPOINT.md) and [`audit/AFI_AUDIT_RESUME_PROMPT.md`](./audit/AFI_AUDIT_RESUME_PROMPT.md) for Phases 2–4.
2. **Distribute** [`AFI_PROTOCOL_INVESTIGATION_PROMPT.md`](./AFI_PROTOCOL_INVESTIGATION_PROMPT.md) only for a fresh full-org run (all phases).
3. **Review** master reports when delivered; resolve open questions in Phase 2 (anchor spec).
4. **Promote** v0.1 → v1.0 after audit findings are incorporated.

---

## 10. Related Documents

| Document | Repo | Role |
|----------|------|------|
| Audit checkpoint (in progress) | `afi-docs` | [`audit/AFI_AUDIT_CHECKPOINT.md`](./audit/AFI_AUDIT_CHECKPOINT.md) |
| Audit resume prompt (Phases 2–4) | `afi-docs` | [`audit/AFI_AUDIT_RESUME_PROMPT.md`](./audit/AFI_AUDIT_RESUME_PROMPT.md) |
| Agent Investigation Prompt | `afi-docs` | [`AFI_PROTOCOL_INVESTIGATION_PROMPT.md`](./AFI_PROTOCOL_INVESTIGATION_PROMPT.md) |
| AFI Config Overview | `afi-config` | Schema catalog |
| TSSD Vault Spec | `afi-infra` | Evidence layer |
| Orchestrator Doctrine | `afi-reactor` | Reference orchestration (needs reframing) |
| Validator Replay Spec v0.1 | `afi-reactor` | Replay invariants |
| Registries & Reputation v0.1 | `afi-config` | Governance boundaries |
| AFI Repo Census | `afi-docs` | Local repo inventory (may be stale) |

---

## Changelog

| Version | Date | Notes |
|---------|------|-------|
| 0.1 | 2026-06-03 | Initial direction + investigation charter |
| 0.1.1 | 2026-06-03 | Split investigation prompt to standalone doc; cross-repo links added |
| 0.1.2 | 2026-06-15 | Phase 1 recon extracted to `audit/` workspace; resume prompt added |
