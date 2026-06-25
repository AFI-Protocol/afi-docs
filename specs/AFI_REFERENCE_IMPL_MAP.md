# AFI Reference Implementation Map

**Phase 4 synthesis report — AFI Portable Protocol Audit**
**Inputs:** theme B (reference implementation map) + the persisted recon corpus (`audit/recon/AFI_RECON_CORPUS.json`, 25 records) + `themes/verified.json`
**Status:** Staged in `afi-docs/specs/audit/final/`. Read-only forensic synthesis; no protocol code modified.

This map answers the North Star's core directive to separate **protocol law from reference plumbing**: it classifies every repo as `NORMATIVE | REFERENCE_IMPL | SUPPORTING | RESEARCH | DOCS | STALE | OUT_OF_SCOPE` and shows which repos own each segment of the reference spine **ingest → scoring DAG → evidence vault → mint coordination → on-chain commitment**. It implements the portable-protocol distinction between "normative schemas/invariants at the top" and "pluggable implementations below" ([`AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md`](../../AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md) §3, §4).

All paths are relative to `/home/user/AFI-Protocol/`. P0/P1 items carry a **Verified** status drawn from `themes/verified.json` (Phase 3 adversarial re-confirmation). Theme-B's own findings are P2/P3/Info (reference-as-law and stale-naming, not protocol violations) and are annotated as such.

---

## Related reports (siblings)

This map is one of six cross-linked Phase-4 reports. All link back to [`AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md`](../../AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md):

- `AFI_PROTOCOL_SURFACE_AUDIT.md` — master report (exec summary, consolidated repo table, findings by severity, roadmap).
- `AFI_NORMATIVE_REGISTER.md` — every normative schema/invariant/contract with `file:line`; stated-but-unenforced invariants.
- `AFI_CONTRADICTION_REGISTER.md` — all six doc/code tensions with verified status.
- `AFI_REPLAY_READINESS_MATRIX.md` — per-lifecycle-stage replay readiness (RAW→ENRICHED→ANALYZED→SCORED→MINTED→REPLAYED).
- `AFI_ONCHAIN_ANCHOR_GAP_ANALYSIS.md` — every relevant Solidity event/struct/field/role; current vs intended anchor.

---

## 1. Scope & method

The portable spec frames AFI as a **portable protocol** (HTTP-like): a thin normative surface over pluggable implementations, where "any conforming orchestrator" and "any conforming vault engine" is permitted ([`AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md`](../../AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md) §3.2, §3.4). This map takes the Phase-1 recon classification of all 31 org repos (`audit/recon/AFI_RECON_CORPUS.json:1`, confirmed by `init.sh` reporting `corpus records: 31`) and the theme-B reference-spine analysis, and reconciles them against live source.

**Classification rubric** (North Star §4 / investigation prompt Group B):

| Class | Meaning |
|-------|---------|
| `NORMATIVE` | Owns protocol law: schemas, types, invariants other repos must obey. |
| `REFERENCE_IMPL` | A concrete, working implementation of one spine segment; swappable. |
| `SUPPORTING` | Tooling/libraries/ops that aid the stack but define no protocol surface. |
| `RESEARCH` | Experimental/simulation; explicitly not production or protocol law. |
| `DOCS` | Documentation/meta-repos; no code. |
| `STALE` | Archived or empty scaffold; must not be read as live spine code. |
| `OUT_OF_SCOPE` | Vendored third-party fork or non-protocol surface (marketing site). |

The headline result: the spine is owned by a small set of `REFERENCE_IMPL` repos anchored by two `NORMATIVE` repos (`afi-config`, `afi-infra`); **no STALE/RESEARCH/OUT_OF_SCOPE repo sits on the spine**; and two reference choices (MongoDB and afi-reactor) are widely documented *as if they were protocol law* (§4, §6).

---

## 2. Reference spine — segment → repo mapping

```
ingest (afi-gateway)
  → scoring DAG (afi-reactor + afi-core + afi-plugins + afi-tiny-brains)
    → evidence vault (afi-infra)
      → mint coordination (afi-mint, off-chain)
        → on-chain commitment (afi-token/src/*.sol)

normative surface (protocol law): afi-config (schemas) + afi-infra (TSSD types/spec)
```

| Spine segment | Repo(s) | Class | Implementing entry point (`file:line`) |
|---------------|---------|-------|----------------------------------------|
| **Ingest boundary** | `afi-gateway` | REFERENCE_IMPL | `POST /api/v1/signals` at `afi-gateway/src/http/app.ts:123`; normalize at `afi-gateway/src/http/app.ts:20`; persist via `afi-gateway/src/http/app.ts:134`; Mongo vault wired at `afi-gateway/src/services/vaultFactory.ts:24-33` |
| **Scoring DAG (orchestrator)** | `afi-reactor` | REFERENCE_IMPL | Froggy DAG executor `runPipeline` / `runPipelineDag` at `afi-reactor/src/services/pipelineRunner.ts:161` and `afi-reactor/src/services/pipelineRunner.ts:339` |
| **Scoring DAG (scoring primitives)** | `afi-core` | REFERENCE_IMPL | Canonical UWR scorer `afi-core/validators/UniversalWeightingRule.ts`; decay/novelty/analyst templates |
| **Scoring DAG (node registry)** | `afi-plugins` | REFERENCE_IMPL | Stub plugin registry consumed by reactor as DAG nodes (`afi-plugins/src/types/plugin.ts:22-26` RuntimeTarget `afi-reactor`/`afi-core`) |
| **Scoring DAG (ML enrichment)** | `afi-tiny-brains` | REFERENCE_IMPL | FastAPI `POST /predict/froggy`, called by reactor per `afi-tiny-brains/README.md:11` |
| **Evidence vault** | `afi-infra` | NORMATIVE | Canonical `VaultedSignalRecord` `afi-infra/src/tssd/types.ts:331`; storage contract `ITSSDVaultClient` `afi-infra/src/tssd/TSSDVaultClient.ts:36-68`; only persistent engine `afi-infra/src/tssd/MongoTSSDVaultClient.ts:72` |
| **Mint coordination (off-chain)** | `afi-mint` | REFERENCE_IMPL | FSM + `MintExecutor.mintForSignal` `afi-mint/src/orchestrator/MintExecutor.ts:33`; calls on-chain coordinator at `afi-mint/src/orchestrator/MintExecutor.ts:108` |
| **On-chain commitment** | `afi-token` | REFERENCE_IMPL | `AFIMintCoordinator.mintForSignal` `afi-token/src/AFIMintCoordinator.sol:68` → `AFIToken.mintEmissions` `afi-token/src/AFIToken.sol:92` |
| **Normative schema surface** | `afi-config` | NORMATIVE | USS/CPJ/vault/pipeline schemas, source of truth `afi-config/schemas/vault.schema.json:14-23` (engine enum) |
| **Normative type surface** | `afi-infra` | NORMATIVE | TSSD types + spec `afi-infra/src/tssd/types.ts:331`; lifecycle enum `afi-infra/src/tssd/types.ts:8-15` |

**Spine integrity note.** Every segment is owned by a `REFERENCE_IMPL` repo except the two `NORMATIVE` anchors. The on-chain commitment segment is implemented **only** by `afi-token/src` (3 Solidity contracts); `afi-mint` coordinates *off-chain* and merely invokes the coordinator through an interface (`afi-mint/src/orchestrator/MintExecutor.ts:108`), and `afi-xerc20` is a vendored bridge fork (OUT_OF_SCOPE) — neither should be read as the AFI commitment layer.

---

## 3. Repo classification table

Classification reconciled against the recon corpus (`audit/recon/AFI_RECON_CORPUS.json:1`) and theme B (`themes/B-reference-impl.json` answer B2). "Spine?" marks repos on the reference spine of §2.

| # | Repo | Visibility | Classification | Spine? | Basis / evidence (`file:line` where applicable) |
|---|------|------------|----------------|--------|--------------------------------------------------|
| 1 | `.github` | PRIVATE | SUPPORTING | no | Org config + repo-map README only; no schemas/code. |
| 2 | `afi-artifacts` | PUBLIC | SUPPORTING | no | Zenodo paper reproducibility bundle; schema *snapshots*, not canonical. |
| 3 | `afi-assets` | PRIVATE | SUPPORTING | no | Brand assets; dirs are empty `.gitkeep` placeholders. |
| 4 | `afi-benchkit` | PUBLIC | SUPPORTING | no | Validator benchmark toolkit; "Does NOT contain DAG/engine/scoring runtime logic". |
| 5 | `afi-cli-framework` | PRIVATE | SUPPORTING | no | Generic Commander.js CLI scaffold; zero protocol surface. |
| 6 | `afi-config` | PUBLIC | **NORMATIVE** | anchor | Canonical schema/spec library (USS/CPJ/vault/pipeline); engine enum `afi-config/schemas/vault.schema.json:14-23`. |
| 7 | `afi-core` | PUBLIC | REFERENCE_IMPL | yes | UWR scorer / decay / novelty primitives `afi-core/validators/UniversalWeightingRule.ts`. |
| 8 | `afi-docs` | PRIVATE | DOCS | no | Documentation hub (hosts the North Star itself); "NOT for code implementation". |
| 9 | `afi-econ` | PRIVATE | RESEARCH | no | "Research-Grade / Placeholder Models"; off-spine gauge splits `afi-econ/README.md:24-26`. |
| 10 | `afi-factory` | PUBLIC | SUPPORTING | no | Phase-1 agent-template registry; mirrors afi-config schemas, no protocol law. |
| 11 | `afi-gateway` | PUBLIC | REFERENCE_IMPL | **yes (ingest)** | ElizaOS gateway; ingest endpoint `afi-gateway/src/http/app.ts:123`. |
| 12 | `afi-governance` | PRIVATE | REFERENCE_IMPL | no (governance plane) | Universal Proposal Signal + Snapshot/Safe execution; not a signal-data spine segment. |
| 13 | `afi-infra` | PRIVATE | **NORMATIVE** | anchor + vault | Canonical TSSD types/spec `afi-infra/src/tssd/types.ts:331`; ITSSDVaultClient `afi-infra/src/tssd/TSSDVaultClient.ts:36-68`. |
| 14 | `afi-labs` | PRIVATE | RESEARCH | no | "experimental playground… prototypes, PoCs"; Mongo-only MVP scaffolds. |
| 15 | `afi-math` | PUBLIC | SUPPORTING | no (consumed by spine) | Pure deterministic math primitives; emissions schedule `afi-math/src/emissions/emissionsSchedule.ts:60`. |
| 16 | `afi-mint` | PRIVATE | REFERENCE_IMPL | **yes (off-chain mint)** | Off-chain mint coordination FSM `afi-mint/src/orchestrator/MintExecutor.ts:33`. |
| 17 | `afi-ops` | PRIVATE | SUPPORTING | no | Phase-1 ops/devops scaffold; deploy/health stubs; bakes Mongo as required infra. |
| 18 | `afi-plugins` | PUBLIC | REFERENCE_IMPL | **yes (DAG nodes)** | Thin plugin registry `afi-plugins/src/types/plugin.ts:22-26`; "NOT production logic". |
| 19 | `afi-protocol` | PRIVATE | DOCS | no | Governance/onboarding meta-repo; zero code/schemas. |
| 20 | `afi-reactor` | PUBLIC | REFERENCE_IMPL | **yes (orchestrator)** | Reference Froggy DAG `afi-reactor/src/services/pipelineRunner.ts:161`; "ONLY orchestrator" claim `afi-reactor/README.md:137`. |
| 21 | `afi-research-site` | PRIVATE | OUT_OF_SCOPE | no | Next.js marketing site (Axleo template); "explicitly separate from the protocol stack". |
| 22 | `afi-skills` | PUBLIC | SUPPORTING | no | Versioned agent-skill library + tooling; scoped skill contract only. |
| 23 | `afi-tiny-brains` | PRIVATE | REFERENCE_IMPL | **yes (ML enrich)** | FastAPI ML microservice called by reactor `afi-tiny-brains/README.md:11`. |
| 24 | `afi-token` | PRIVATE | REFERENCE_IMPL | **yes (on-chain)** | BASE/xERC20 contracts; `afi-token/src/AFIMintCoordinator.sol:68`, `afi-token/src/AFIToken.sol:92`. |
| 25 | `afi-xerc20` | PUBLIC | OUT_OF_SCOPE | no | Vendored defi-wonderland/xERC20 fork; not an AFI artifact. |

**Class tallies (25 total):** NORMATIVE = 2 (`afi-config`, `afi-infra`); REFERENCE_IMPL = 8 (`afi-core`, `afi-gateway`, `afi-governance`, `afi-mint`, `afi-plugins`, `afi-reactor`, `afi-tiny-brains`, `afi-token`); SUPPORTING = 9 (`.github`, `afi-artifacts`, `afi-assets`, `afi-benchkit`, `afi-cli-framework`, `afi-factory`, `afi-math`, `afi-ops`, `afi-skills`); RESEARCH = 2 (`afi-econ`, `afi-labs`); DOCS = 2 (`afi-docs`, `afi-protocol`); OUT_OF_SCOPE = 2 (`afi-research-site`, `afi-xerc20`). 2 + 8 + 9 + 2 + 2 + 2 = **25**.

---

## 4. Reference-as-law tensions (the two big "feels mandatory" choices)

The portable spec says the protocol law is *conforming outputs + pinned versions*, with the engine and orchestrator pluggable ([`AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md`](../../AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md) §3.2, §3.4). Two reference choices are nonetheless documented and wired as if they were protocol law.

### 4.1 MongoDB presented as the mandatory vault engine

- `vault.schema.json` advertises a four-engine pluggable Evidence plane — enum `["mongodb","postgresql","timescaledb","influxdb"]` (`afi-config/schemas/vault.schema.json:14-23`) — but only `mongodb` is implemented: the sole persistent `ITSSDVaultClient` is `afi-infra/src/tssd/MongoTSSDVaultClient.ts:72` (dynamic `import('mongodb')` + `new MongoClient` at `afi-infra/src/tssd/MongoTSSDVaultClient.ts:220-221`); the only other clients are an in-memory dev stub (`afi-infra/src/tssd/TSSDVaultClient.ts:90`) and a tenant-scoping wrapper that defaults to Mongo (`afi-infra/src/tssd/TenantScopedTSSDVaultClient.ts:19-25`). **postgresql/timescaledb/influxdb are schema-listed-only with zero client code.**
- Production hard-fails without a Mongo URI: `afi-infra/src/tssd/TSSDVaultClient.ts:197-201` — *"AFI_TSSD_MONGODB_URI is required in production. Falling back to in-memory is not allowed."* The reactor's scored-signal persistence is likewise Mongo-only and requires `AFI_MONGO_URI` (`afi-reactor/src/services/tssdVaultService.ts:6`), and ops bakes Mongo in as required infra.

**Verified status (P0/P1 from `verified.json`):**

| Source | Title | Orig | Verified | Revised |
|--------|-------|------|----------|---------|
| `draft:52` | TSSD vault production path is Mongo-only; multi-engine vault is absent | P1 | ✅ confirmed | P1 |
| `draft:84` | Vault layer hard-bound to MongoDB; no multi-engine seam | P1 | ✅ confirmed | P1 |

Theme-B's own framing of this as reference-as-law sits at **P2** (`themes/B-reference-impl.json` findings #0, #1; tension `Mongo-only`): fixable by documentation/abstraction, not a protocol violation.

### 4.2 afi-reactor presented as THE only orchestrator

Authoritative docs assert reactor is *the* orchestrator and "the DAG is law": `afi-reactor/README.md:137` (*"afi-reactor is the ONLY orchestrator in AFI Protocol."*), `afi-reactor/AGENTS.md:3`, and downstream echoes `afi-core/docs/AFI_CORE_RUNTIME_OVERVIEW.md:39` and `afi-config/codex/governance/droids/AFI_DROID_CHARTER.v0.1.md:117`. The North Star instead permits "afi-reactor, custom DAG, Mage blocks (if outputs conform)" and "any conforming orchestrator" ([`AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md`](../../AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md) §3.4).

**Verified status (P0/P1 from `verified.json`):**

| Source | Title | Orig | Verified | Revised |
|--------|-------|------|----------|---------|
| `theme:E-scoring-dag#1` | reactor self-declares THE "ONLY" orchestrator / "DAG is law" | P1 | ✅ confirmed | P1 |
| `draft:83` | Reactor self-declares as THE single orchestrator, contradicting pluggability | P1 | ✅ confirmed | P1 |

Theme-B's framing of the same quotes as reference-as-law is **P2** (`themes/B-reference-impl.json` finding #2; tension `reactor-only`). Cross-link `AFI_CONTRADICTION_REGISTER.md` (reactor-only tension) and `AFI_REPLAY_READINESS_MATRIX.md` (scoring stage).

---

## 5. Vault engines: implemented vs schema-listed

| Engine (schema enum) | Schema-listed | Implemented client | Status |
|----------------------|---------------|--------------------|--------|
| `mongodb` | yes (`afi-config/schemas/vault.schema.json:14-23`) | `afi-infra/src/tssd/MongoTSSDVaultClient.ts:72` (persistent, `import('mongodb')` `:220-221`) | **Implemented** (sole persistent engine) |
| `postgresql` | yes | none | Schema-listed only |
| `timescaledb` | yes | none | Schema-listed only |
| `influxdb` | yes | none | Schema-listed only |
| (in-memory) | not in enum | `afi-infra/src/tssd/TSSDVaultClient.ts:90` | Non-persistent dev/test fallback only |

The engine-neutral seam (`ITSSDVaultClient`, `afi-infra/src/tssd/TSSDVaultClient.ts:36-68`) is the correct extension point; the gap is that only one engine binding exists behind it. See `AFI_NORMATIVE_REGISTER.md` (schema S4) and `AFI_ONCHAIN_ANCHOR_GAP_ANALYSIS.md` for the commitment-plane counterpart.

---

## 6. Stale / out-of-scope repos that must not be read as spine code

| Repo | Why excluded from the live spine | Evidence |
|------|----------------------------------|----------|
| `afi-xerc20` | Vendored defi-wonderland/xERC20 bridge fork; not an AFI mint/receipt artifact | corpus record `afi-xerc20` (homepage defi-wonderland/xERC20) |
| `afi-research-site` | Marketing/brochure site; "explicitly separate from the AFI Network protocol stack" | corpus record `afi-research-site` |

Detailed drift cataloguing is deferred to Theme J / `AFI_CONTRADICTION_REGISTER.md` (stale-arch-docs tension).

---

## 7. Recommended actions (per North Star solidification)

1. **Annotate the vault engine enum** (`afi-config/schemas/vault.schema.json:14-23`) to state only `mongodb` is implemented today, and reframe the prod guard (`afi-infra/src/tssd/TSSDVaultClient.ts:197-201`) as "a persistent `ITSSDVaultClient` is required in production" (engine-agnostic). [Mongo-only]
2. **Reframe afi-reactor as the reference orchestrator** (not the only one): add a banner that any conforming, version-pinned DAG output is valid (`afi-reactor/README.md:137`). [reactor-only]
3. **Label the commitment segment precisely**: `afi-mint` = off-chain coordination; `afi-token/src` = sole on-chain commitment; `afi-xerc20` = OUT_OF_SCOPE vendored fork.

---

## 8. Sources

- Theme: `afi-docs/specs/audit/themes/B-reference-impl.json` (answers B1–B6; findings #0–#4).
- Verification ledger: `afi-docs/specs/audit/themes/verified.json` (P0/P1 re-confirmation).
- Recon corpus: `afi-docs/specs/audit/recon/AFI_RECON_CORPUS.json:1` (25 records).
- Draft baseline: `afi-docs/specs/audit/drafts/AFI_REFERENCE_IMPL_MAP.draft.md:13-62`.
- North Star: [`AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md`](../../AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md) §3–§4.
