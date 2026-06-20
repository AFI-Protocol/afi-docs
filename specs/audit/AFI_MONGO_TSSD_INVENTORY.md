# MongoDB / TSSD Inventory

> **Scope:** Code-level inventory of every Mongo/TSSD touchpoint across the AFI-Protocol workspace. **MongoDB TSSD is AFI's canonical reference evidence store** — see [`AFI_EVIDENCE_STORE_DECISION.md`](./AFI_EVIDENCE_STORE_DECISION.md).
> **Investigated:** 2026-06-20 · **Method:** ripgrep sweep + per-repo file:line trace + multi-agent fan-out + adversarial verification.
> **Constraint:** No code changes — read-only inventory.
>
> *Retrospective note: a warehouse/streaming "evidence plane" was proposed in planning docs only and never implemented; it was retracted and scrubbed 2026-06.*

---

## Executive verdict

> **The Mongo ingest → score → persist path is implemented and runnable today.** MongoDB TSSD is the canonical evidence store; a scored signal reaches Mongo with only env + `npm run` — no new architecture.

- The **ingest → score → Mongo-persist** path is fully implemented and reachable in `afi-reactor`. Persistence is *off by default* (empty `AFI_MONGO_URI`) and switches on the moment that one env var is set.
- **Three repos ship `mongodb` as a runtime dependency** — `afi-reactor ^6.18.0`, `afi-infra ^7.0.0`, `afi-gateway ^6.21.0` — and contain live `insertOne`/`upsert` code.
- The legacy/demo **purge did not touch the Mongo path** — only demo-chain plugins (alpha-scout, structurer, validator-decision, execution-sim) were removed; a guardrail test enforces their continued absence.
- **Active operator/architecture docs correctly present Mongo TSSD as the canonical persistence layer** (`AFI_Full_Architecture.md`, `TSSD_VAULT_SPEC.md`, `AGENTS.md`, `AFI_System_Atlas.md`, the testnet checklist, etc.).

**Bottom line:** Mongo is the reference spine because it is the path that exists in code. The one prerequisite to demo it is a reachable MongoDB + `AFI_MONGO_URI`.

---

## Runtime path diagram (ingest → score → Mongo)

There are **two Mongo write surfaces** with two env conventions. The reactor surface is the simplest demo; the gateway surface is a parallel multi-tenant ingest.

### Surface A — `afi-reactor` scored store (the fast path) — `RUNTIME`, reachable

```
POST /api/webhooks/tradingview                         afi-reactor/src/server.ts:159
   │   (optional WEBHOOK_SHARED_SECRET :193, TV→USS map :208, AJV validate :211)
   ▼
runFroggyTrendPullbackFromCanonicalUss(canonicalUss)   afi-reactor/src/server.ts:229
   │   (twin entry POST /api/ingest/cpj :290 → :396 funnels into the same fn)
   ▼
runFroggyTrendPullbackDagInternal → runPipelineDag      froggyDemoService.ts:75 → :196
   │   FROGGY_TREND_PULLBACK_PIPELINE (Kahn topo-sort, pipelineRunner.ts:339)
   │   uss-telemetry-deriver → [tech-pattern ∥ sentiment-news] → enrichment-adapter
   ▼
froggy-analyst  →  afi-core UWR score                   froggyPipeline.ts:136 / plugin :36
   │   demo price feed is network-free (Math.random OHLCV) → no API keys needed
   ▼
── pipeline returns ──
   ▼
getTssdVaultService()  (null iff AFI_MONGO_URI unset)   froggyDemoService.ts:268
   │   provenance guardrail :272 (throws 500 iff priceSource/venueType missing —
   │   never trips on demo path: adapter always sets both, :646-653)
   ▼
vaultService.insertSignalDocument(reactorDoc)           froggyDemoService.ts:315
   ▼
collection.insertOne(doc)                               tssdVaultService.ts:112
   → afi_reactor.reactor_scored_signals_v1   (MongoClient, mongodb ^6.18.0)
```

> ⚠️ **Naming trap (three "tssd-vault" artifacts, only one persists):**
> 1. DAG stage `tssd-vault-write` (`froggyPipeline.ts:145`) → its handler is a **pass-through no-op** (`froggyDemoService.ts:188-193`).
> 2. `afi-reactor/plugins/tssd-vault-service.ts` → a **DEAD dev stub** wired only via the unused `config/dag.codex.json:19`.
> 3. **`src/services/tssdVaultService.ts` (camelCase)** → **the real Mongo write**, called post-pipeline at `froggyDemoService.ts:268→315`.

### Surface B — `afi-gateway` TSSD vault (multi-tenant) — `RUNTIME`, reachable via `start:minimal`

```
POST /api/v1/signals                                    afi-gateway/src/http/app.ts:122
   │   apiKeyAuth (Mongo api_keys read/markUsed) → tenant scope
   ▼
vault = createVaultFactoryFromEnv()(tenantId)           vaultFactory.ts:24
   ▼
TenantScopedTSSDVaultClient → MongoTSSDVaultClient       afi-infra/src/tssd/*
   ▼
vault.upsert(record)  (findOne + deleteOne + insertOne)  app.ts:133-134
   → MongoTSSDVaultClient.upsert                          afi-infra/.../MongoTSSDVaultClient.ts:120-161
   → native time-series collection afi_tssd.tssd_signals  (dynamic import("mongodb") :219-221)
```

> ⚠️ **Gateway caveats:** the vault-wired app (`buildApp`) is mounted **only by `start:minimal`** (`server.ts`). The default `start` runs `server-full.ts` (ElizaOS AgentServer) which has no vault wiring. Also, the `AFI_TSSD_*` env vars are **absent from `.env.example`**, so a default deploy throws on the first `/api/v1/signals` call unless the `MONGODB_URI` fallback is set.

---

## Per-repo inventory table

| Repo | Files (Mongo/TSSD) | Classification | MVP relevance | Still runnable? |
|------|--------------------|----------------|---------------|-----------------|
| **afi-reactor** | 35 (scored store + pipeline + dead stub/codex) | **RUNTIME** + CONFIG + TEST + DOCS | **critical** | **yes** |
| **afi-infra** | 22 (Mongo vault client, types, spec) | **RUNTIME** (library) + TEST + DOCS | **critical** (gateway path) | unknown (lib; no entrypoint) |
| **afi-gateway** | 15 (vaultFactory, app, local mongo, api keys) | **RUNTIME** + CONFIG + TEST | supporting | yes (`start:minimal`) |
| afi-mint | 2 (JSDoc only; DI seam) | RUNTIME types, **no Mongo** (in-memory stub) | supporting | yes |
| afi-config | 2 (engine-agnostic `vault.schema.json`) | CONFIG/DOCS | supporting | yes |
| afi-starters | 4 (`docker-compose` mongo:7, railway, render) | **CONFIG** (deploy) | supporting | unknown |
| afi-docs | active operator + architecture + audit docs | DOCS | supporting | n/a |
| afi-ops | 9 (env/compose templates, stub health scripts) | CONFIG + DOCS (stubs) | supporting | no |
| afi-token | 4 (NatSpec comments; on-chain Solidity) | DOCS (off-chain provenance label) | supporting | unknown |
| afi-core | 7 (docstrings/comments only) | DOCS | supporting | unknown |
| afi-labs | 10 (sandbox Mongo code, unwired) | **DEAD** (sandbox) + DOCS | supporting | no |
| afi-skills | 10 (`tssd:read` permission scope) | CONFIG/DOCS | supporting | unknown |
| afi-research-site | 2 (Boxicons brand glyph) | **DEAD** (vendor asset noise) | dead | unknown |
| afi-artifacts | 6 (`vaulted_tssd.schema.json` + stub replay) | CONFIG/TEST + stub | supporting | no |

**Classification legend:** RUNTIME = imports `mongodb`/calls vault write on a live path · CONFIG = env/schema/compose · TEST = smoke/unit · DOCS = active prose · DEAD = unreachable/commented/sandbox/vendor noise.

### Notable per-repo detail

- **afi-infra** — the production vault library. `MongoTSSDVaultClient` creates a **native Mongo time-series collection** (timeField `createdAt`, metaField `identity`, optional TTL), `upsert()` = `findOne`+`deleteOne`+`insertOne`. Consumed by gateway; **`afi-reactor` has its own isolated `tssdVaultService.ts`** (different collection/env/driver). Version note: infra pins `mongodb ^7.0.0`, gateway `^6.21.0`.
- **afi-mint** — TSSD/vault appear **only in JSDoc**. Signal-metadata reads go through an injected `ISignalMetadataFetcher` with **no concrete implementation** (in-memory stub seam). Wiring a Mongo reader is the T2 MVP gap (see testnet checklist §1.4).
- **afi-labs** — the only *genuine* Mongo code in the lighter set (`code-sandbox/infra/mongo.ts`, `agent_registry_server_mongo.py`) but **unwired sandbox** — no `package.json` declares `mongodb`. `DEAD`.
- **afi-core** — `validators/ValidatorDecision.ts` is a **future cert/decision-envelope type** (structural only), **not** a reactor vault plugin; every TSSD hit is a docstring invariant.
- **afi-research-site** — both hits are the `.bxl-mongodb` Boxicons brand glyph. Noise.

---

## Env vars & run commands (minimum MVP demo)

### Reactor scored store (Surface A) — env

| Var | Default | Required? | Source |
|-----|---------|-----------|--------|
| `AFI_MONGO_URI` | *(empty → vault disabled)* | **yes (to enable persist)** | `tssdVaultService.ts:57`, `.env.example:20` |
| `AFI_MONGO_DB_NAME` | `afi_reactor` | no | `tssdVaultService.ts:58` |
| `AFI_MONGO_COLLECTION_SCORED` | `reactor_scored_signals_v1` | no | `tssdVaultService.ts:59` |
| `AFI_PRICE_FEED_SOURCE` | `demo` (network-free OHLCV) | no | `priceFeedRegistry.ts:59` |
| `WEBHOOK_SHARED_SECRET` | *(unset → auth skipped)* | no | `server.ts:193` |
| `PORT` / `AFI_REACTOR_PORT` | `8080` | no | `server.ts:435` |

### Gateway TSSD vault (Surface B) — env

| Var | Default | Required? | Source |
|-----|---------|-----------|--------|
| `AFI_TSSD_MONGODB_URI` (← `MONGODB_URI`/`MONGO_URI`) | *(throws in prod if unset)* | **yes** | `MongoTSSDVaultClient.ts:86-113` |
| `AFI_TSSD_DB_NAME` | `afi_tssd` | no | `MongoTSSDVaultClient.ts` |
| `AFI_TSSD_COLLECTION` | `tssd_signals` | no | `MongoTSSDVaultClient.ts` |
| `OPENAI_API_KEY` | *(hard-required by gateway env)* | **yes** | `gateway/src/config/env.ts` |

> ⚠️ `AFI_TSSD_*` are **not in `afi-gateway/.env.example`** — a config-doc gap for the signals path (P1).

### Minimum commands to demo one scored signal in Mongo (Surface A — fastest)

```bash
# 1. Provision a local Mongo (reuse the starters compose — image mongo:7 on :27017)
cd afi-starters/self-hosted-pipeline && docker compose up -d mongo

# 2. Build + run the reactor, pointed at that Mongo
cd ../../afi-reactor
npm install
npm run build                                   # tsc -> dist/
AFI_MONGO_URI='mongodb://localhost:27017' \
AFI_MONGO_DB_NAME=afi_reactor \
  npm run start:demo                            # node dist/src/server.js, listens :8080

# 3. Fire one webhook (no API keys: demo price feed + fail-soft sentiment/news/aiMl)
curl -X POST http://localhost:8080/api/webhooks/tradingview \
  -H 'Content-Type: application/json' \
  -d '{"symbol":"BTCUSDT","timeframe":"15m","strategy":"froggy_trend_pullback_v1","direction":"long"}'

# 4. Verify the scored signal landed
mongosh afi_reactor --eval 'db.reactor_scored_signals_v1.find().pretty()'
```

**Graceful degradation (why this is low-risk to demo):**
- `AFI_MONGO_URI` unset → `getTssdVaultService()` returns `null`, persist skipped, webhook still returns **200 with the score** (`tssdVaultService.ts:61-64`).
- Mongo down / insert fails → `insertSignalDocument` `try/catch` logs `❌`, returns `"failed"`, throw swallowed → still **200** (`tssdVaultService.ts:104-122`).
- **Only hard-fail:** the provenance guardrail throws 500 if `priceSource`/`venueType` are missing (`froggyDemoService.ts:272-278`) — but the enrichment adapter always sets both on the demo path.
- **Framing nit:** the reactor write is a plain `insertOne` (append), not an upsert (the gateway/infra path is the upsert).

---

## Active docs (Mongo correctly presented as canonical)

These active docs present MongoDB TSSD as the canonical persistence layer — consistent with the [evidence-store decision](./AFI_EVIDENCE_STORE_DECISION.md):

| Doc | Says Mongo is… | Evidence |
|-----|----------------|----------|
| `afi-infra/docs/TSSD_VAULT_SPEC.md` | the single source of truth for the signal lifecycle | L7, L98, L133-137 |
| `afi-docs/AFI_Full_Architecture.md` | canonical "Time-Series Storage: MongoDB" | L353-358, 557-561 |
| `afi-reactor/AGENTS.md` | pipeline terminus = MongoDB collection | L27, 382, 394 |
| `afi-reactor/docs/HTTP_WEBHOOK_SERVER.md` | persists scored signal to MongoDB | L278 |
| `afi-docs/AFI_System_Atlas.md` | TSSD vault persistence via `tssdVaultService.ts` | L18 |
| `afi-docs/specs/audit/AFI_TESTNET_E2E_CHECKLIST.md` | reference spine = afi-reactor + Mongo TSSD | Reference spine table |

No active doc conflicts with the Mongo-canonical position.

---

## Purge impact assessment

The legacy/demo purge **did not remove or break the Mongo vault path** (adversarially verified, `confirmed/high`):

| Check | Result | Evidence |
|-------|--------|----------|
| `tssd-vault-write` still in `froggyPipeline.ts`? | **yes** | `froggyPipeline.ts:144-151` |
| `plugins/tssd-vault-service.ts` still exists? | **yes (but DEAD)** | dev stub, referenced only by unused `config/dag.codex.json:19` |
| Real `tssdVaultService.ts` imported on webhook path? | **yes** | `froggyDemoService.ts:23` → `:268`; webhook via `server.ts:34-38` |
| Purged plugins were demo-chain only? | **yes** | named only in `REMOVED STAGES` comment `froggyPipeline.ts:90-94`; guardrail test `test/guardrails/no-legacy-ingest.test.ts:114-118` |

The Mongo persist sits **downstream of `froggy-analyst`** and was never part of the demo chain — untouched by the purge.

---

## Gaps / blockers (for a full T2 E2E)

- **No blocker to a Mongo persist demo.** The only prerequisite is a reachable MongoDB + `AFI_MONGO_URI` (one env var). A one-command local Mongo ships (`afi-starters/self-hosted-pipeline/docker-compose.yml`, `mongo:7`).
- **T2 mint wire-up gap:** `afi-mint` reads scored-signal metadata via an injected `ISignalMetadataFetcher` with no concrete impl — a Mongo reader of `reactor_scored_signals_v1` must be implemented, plus an on-chain `mintForSignal` client. See testnet checklist §1.4.
- **Config-doc gap (P1, gateway):** `AFI_TSSD_*` vault env vars are missing from `afi-gateway/.env.example`; Surface B throws on first `/api/v1/signals` unless `MONGODB_URI` fallback is set, and only `start:minimal` mounts the vault.
- **Persistence-default OFF:** reactor ships with empty `AFI_MONGO_URI`, so a fresh checkout scores-but-does-not-persist until it is set.

---

## Recommended next action

1. **Demo the Mongo spine as-is** (Surface A): the recipe above produces a persisted scored signal in minutes with no new code or API keys.
2. **Close the T2 mint gap:** implement `afi-mint`'s Mongo reader + on-chain mint client (testnet checklist §1.4) to complete ingest → score → Mongo → mint on Base Sepolia.

---

*Companion machine-readable inventory: [`AFI_MONGO_TSSD_INVENTORY.json`](./AFI_MONGO_TSSD_INVENTORY.json). Every row above is backed by a `repo/path:line` citation or command output.*
