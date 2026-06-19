# AFI Deep Research Prompt — Mage.ai + GCP Pipeline Architecture Options

**Status:** Research charter (copy-paste to deep research agent)  
**Date:** 2026-06-03  
**Audience:** Deep research agent, protocol architects, data/platform leads  
**Prerequisite context:** AFI is pivoting **away from Mongo TSSD** as the reference evidence path toward **Mage.ai + GCP** for lowest barrier-to-entry testnet proof. Mongo/reactor remain in the monorepo as legacy reference; they are **not** the target spine.

**Companion docs:**
- [`../AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md`](../AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md) — normative vs reference, five planes
- [`AFI_TESTNET_E2E_CHECKLIST.md`](./AFI_TESTNET_E2E_CHECKLIST.md) — testnet acceptance criteria
- [`../AFI_ONCHAIN_ANCHOR_GAP_ANALYSIS.md`](../AFI_ONCHAIN_ANCHOR_GAP_ANALYSIS.md) — BASE commitment layer (unchanged by this pivot)

---

## Part A — Analysis of the three reference examples (for the researcher)

Study these before researching alternatives. Extract **patterns**, not product marketing.

### Example 1 — Real-time streaming: Kafka + Mage Pro + BigQuery

**Source:** [Building real-time crypto trading pipelines with Kafka and Mage Pro](https://www.mage.ai/blog/building-real-time-crypto-trading-pipelines-with-kafka-and-mage-pro)

| Aspect | What it does | Implications for AFI |
|--------|--------------|----------------------|
| **Ingest** | Custom Python WebSocket producer (Binance futures trades) | Decoupled from Mage; runs as separate long-lived process |
| **Buffer** | Apache Kafka (symbol-keyed partitioning, `acks=all`, batching) | Durable ordered stream; replay for backtest/debug |
| **Orchestration** | Mage Pro **streaming** pipeline: Kafka loader → Python transformer → BQ exporter | Mage consumes **batches** of messages (`batch_size: 100`) |
| **Transform** | Buy/sell pressure, running averages per symbol (stateful within batch) | Analytics-plane logic; not per-signal protocol lifecycle |
| **Sink** | BigQuery via YAML connector | Warehouse for ticks/features, not necessarily canonical evidence |
| **GCP note** | Blog lists **Google Cloud Pub/Sub** as Kafka deployment option | Native GCP path may avoid operating Kafka |

**Strengths:** Separation of capture vs processing; replay; scales to high-frequency market data.  
**Weaknesses for AFI:** Tick stream ≠ `VaultedSignalRecord` lifecycle; stateful transforms may not survive Mage batch boundaries without external state; producer is bespoke ops burden.

---

### Example 2 — Batch / micro-batch: PySpark + Mage Pro + BigQuery

**Source:** [Build a crypto trading data pipeline with PySpark in Mage Pro](https://www.mage.ai/blog/build-a-crypto-trading-data-pipeline-with-pyspark-in-mage-pro)

| Aspect | What it does | Implications for AFI |
|--------|--------------|----------------------|
| **Pattern** | Batch pipeline + scheduled trigger (poll-like “stream”) | Lower ops than Kafka for MVP |
| **Ingest** | Mage data loader: REST API → PySpark DataFrame | Single-block ingest inside Mage |
| **Compute** | PySpark transform (`price × quantity`); Mage Pro manages Spark session | Distributed math; 2-line `metadata.yaml` enables Spark |
| **Sink** | `df.toPandas()` → Mage BigQuery exporter (`io_config.yaml`) | **Anti-pattern at scale** but fine for proof-of-concept volume |
| **Schema** | Explicit Spark `StructType` | Good precedent for typed pipeline contracts |

**Strengths:** Fastest path to “data in BQ”; minimal moving parts; matches “lowest barrier” goal.  
**Weaknesses for AFI:** Not true real-time; pandas bridge limits throughput; still market **ticks**, not USS/scored signals.

---

### Example 3 — Pattern library: mage-pipeline-examples

**Source:** [mage-ai/mage-pipeline-examples](https://github.com/mage-ai/mage-pipeline-examples)

| Category | Relevant patterns | AFI mapping |
|----------|-------------------|-------------|
| **Data integration** | API → database, multi-source sync | Ingest boundary → evidence store |
| **Batch ETL** | CSV/JSON, Python+SQL hybrid | Enrichment batches, feature builds |
| **Streaming** | Kafka consumer pipelines | Market/analytics plane |
| **Data quality** | Validation, anomaly detection | USS/CPJ validation blocks |
| **ML models** | Train/infer blocks | Scoring DAG (if outputs conform) |
| **Cloud ops** | S3→RDS, multi-cloud | Adapt to GCS→BQ, Pub/Sub |

**Meta-pattern:** Loader → Transformer → Exporter blocks; `io_config.yaml` credentials; zip-import pipelines; Docker/local vs cloud deploy.

---

### Cross-example synthesis (research must not miss this)

All three examples are **crypto market data → warehouse** pipelines. None implement:

1. **Per-signal evidence lifecycle** (RAW → ENRICHED → ANALYZED → SCORED → MINTED → REPLAYED)
2. **Protocol ingest dialect** (USS v1.1, CPJ v0.1 from `afi-config`)
3. **Determinism pinning** (pipeline version, codex hash, content hash)
4. **Commitment plane handoff** (scored signal → `afi-mint` → Base Sepolia `mintForSignal`)
5. **Plane separation** (analytics ticks vs canonical signal rows)

Your research must map Mage+GCP options onto **AFI's five planes**, not just replicate Binance→BQ tutorials.

---

## Part B — Research mission (copy from here to agent)

```
# DEEP RESEARCH MISSION: Mage.ai + GCP Architecture Options for AFI Protocol

## Role
You are a senior data-platform architect and protocol engineer conducting 
**exhaustive, evidence-based research**. You produce comparison matrices, 
architecture recommendations, cost/ops estimates, and a ranked shortlist 
— not vendor cheerleading.

## Organization context
AFI (Agentic Financial Intelligence) is a **portable protocol** for signal 
intelligence: propose → enrich → score → commit (on-chain) → challenge/replay.

We are **departing from MongoDB** as the reference evidence vault (scope creep, 
incomplete implementation). We are standardizing on a **GCP + Mage.ai reference 
spine** for testnet proof and lowest barrier to entry.

**Non-negotiable constraints:**
- BASE / on-chain commitment stays in `afi-token` (Base Sepolia today)
- Normative schemas live in `afi-config` (USS, vault record shape, etc.)
- Mage/GCP/BQ are **reference implementations**, not protocol law
- Do NOT collapse analytics warehouse and per-signal evidence store
- Favor managed GCP services where they reduce ops without blocking portability

## Reference examples already analyzed (benchmark, do not stop here)
1. Kafka + Mage Pro streaming + BQ (Binance WebSocket producer)
   https://www.mage.ai/blog/building-real-time-crypto-trading-pipelines-with-kafka-and-mage-pro
2. PySpark batch + Mage Pro + BQ (Binance REST, scheduled triggers)
   https://www.mage.ai/blog/build-a-crypto-trading-data-pipeline-with-pyspark-in-mage-pro
3. Mage pipeline pattern library (loaders/transformers/exporters)
   https://github.com/mage-ai/mage-pipeline-examples

## Primary research question
What architecture options — **similar to, or superior to**, the three examples above —
best support AFI's reference spine on **GCP + Mage.ai**, for:
  (a) testnet MVP E2E (scored signal → mint → vault write-back), and
  (b) production-grade evolution (streaming market context, replay, cost control)?

"Superior" means: lower ops burden, better GCP-native fit, clearer plane separation,
stronger determinism/replay story, or lower cost — with tradeoffs stated explicitly.

---

## Phase 1 — Map AFI planes to infrastructure (required)

For each plane below, propose 2–4 architecture options on GCP (+ Mage where relevant).
Cite official docs, pricing pages, and real-world case studies where possible.

| Plane | AFI requirement | Research focus |
|-------|-----------------|----------------|
| **Ingest** | USS/CPJ-valid signals, webhooks, API | Gateway on Cloud Run vs Mage loader vs Pub/Sub ingress |
| **Scoring DAG** | Pinned transforms, conforming outputs | Mage batch/stream vs Composer/Airflow vs Dataflow vs keep afi-reactor as worker |
| **Evidence** | Per-signal lifecycle record (canonical row) | BQ table design vs Cloud SQL vs Firestore vs GCS+json vs hybrid |
| **Analytics** | Continuous market/features context | BQ datasets, Pub/Sub, Dataflow, streaming vs micro-batch |
| **Commitment** | BASE mint (external to Mage) | How evidence plane triggers `afi-mint` (Pub/Sub event, Cloud Run, Workflow) |

Deliverable: **plane map diagram** (text or mermaid) per option.

---

## Phase 2 — Evaluate Mage.ai placement (required)

Research and compare:

### 2.1 Mage deployment models on GCP
- Mage OSS self-hosted (GKE, Compute Engine, Cloud Run limitations)
- Mage Pro cloud (SOC2, managed Spark, streaming connectors)
- Hybrid: Mage orchestrates, GCP services execute (BQ, Dataflow, Cloud Functions)

### 2.2 Mage pipeline modes for AFI
| Mode | When to use | Risks for AFI |
|------|-------------|---------------|
| Batch + cron trigger | MVP testnet, signal batches | Latency, not tick-real-time |
| Streaming (Kafka/Pub/Sub loader) | Market analytics plane | Stateful scoring, batch boundaries |
| PySpark blocks | Heavy feature engineering | Cost, cluster management |
| Python-only blocks | Scoring, validation, mint prep | Simpler, may suffice for MVP |
| dbt blocks in Mage | SQL transforms in BQ | Good for analytics silver/gold layers |

### 2.3 Mage vs GCP-native orchestration alternatives
For each alternative, answer: **replace Mage entirely? complement Mage? or inferior for AFI?**
- Cloud Composer (Airflow)
- Cloud Workflows + Cloud Run jobs
- Vertex AI Pipelines
- Dataflow (Apache Beam) templates
- Pub/Sub → Dataflow → BQ (no Mage)
- dbt + BigQuery scheduled queries
- Estuary/Fivetran/Hevo (if relevant for ingest only)

### 2.4 Mage gaps for protocol use cases
Investigate in Mage docs/issues/community:
- Stateful stream processing across batches
- Schema enforcement / contract testing (USS JSON Schema)
- Pipeline versioning pinned in output records
- Exactly-once semantics to BQ
- Secret management (GCP Secret Manager integration)
- CI/CD for pipelines (GitHub Actions → Mage deploy)
- Cost at 10K / 100K / 1M signals per month

---

## Phase 3 — GCP messaging & storage matrix (required)

The Kafka example uses Kafka; the blog also mentions Pub/Sub. Research **GCP-native and hybrid** options:

| Pattern | Components | Compare on: latency, cost, replay, ops, Mage integration |
|---------|------------|----------------------------------------------------------|
| **A. Kafka on GCP** | Confluent Cloud, self-managed on GKE, Redpanda | Match Mage Kafka blog pattern |
| **B. Pub/Sub native** | WebSocket/Run producer → Pub/Sub → Mage or Dataflow → BQ | Fewer moving parts on GCP |
| **C. Batch-only** | Scheduled Mage batch, no message bus | Simplest MVP |
| **D. BQ streaming insert** | Producer → BQ streaming API directly | Skip Mage for ingest? |
| **E. GCS landing + batch** | Raw JSON to GCS → Mage/BQ load job | Cheap, higher latency |
| **F. Dataflow unified** | Beam pipeline end-to-end | Mage optional |

For **AFI specifically**, recommend:
- Which pattern for **analytics plane** (market ticks, features)
- Which pattern for **evidence plane** (per-signal lifecycle updates)
- Whether one bus can serve both (likely NO — justify)

---

## Phase 4 — Reference architecture candidates (required)

Produce **at least 5 distinct architecture candidates**, ranked for AFI testnet MVP.

Each candidate must include:
1. **Name** (e.g. "Mage Batch MVP", "Pub/Sub + Mage Stream + BQ dual-dataset")
2. **Diagram** (mermaid)
3. **Component list** with GCP services + Mage role
4. **Data flow** for one signal from ingest → SCORED → mint trigger → MINTED write-back
5. **Mapping to AFI lifecycle stages** (which store holds RAW/SCORED/MINTED)
6. **Determinism story** (what is pinned, what breaks replay)
7. **Estimated monthly cost** (rough order of magnitude, low traffic testnet)
8. **Time-to-first-E2E** (engineering weeks, assumptions stated)
9. **Ops burden** (1–5 scale, who oncalls)
10. **Portable-protocol fit** (does this remain a reference path strangers can swap?)

**Mandatory candidates to include (you may add more):**
- **C1:** Mage batch-only + BQ evidence table + Cloud Run mint trigger (simplest)
- **C2:** Pub/Sub + Mage streaming + BQ analytics + separate BQ evidence dataset
- **C3:** Kafka (Confluent or self-managed) + Mage streaming (replicate Mage blog)
- **C4:** Dataflow-centric, Mage as authoring/monitoring layer only
- **C5:** Composer/Airflow orchestrating GCP jobs, no Mage (baseline comparison)

---

## Phase 5 — Evidence store design on BigQuery (required)

Mongo is out; if BQ is in, research **how not to repeat the Mongo mistake**.

Answer:
1. Single wide table vs normalized stage tables vs JSON `stages` column for `VaultedSignalRecord`
2. Partitioning/clustering keys (`signal_id`, `epoch_id`, `stage`, `updated_at`)
3. Mutability policy (SCORED→MINTED updates: MERGE vs append-only event log)
4. Separation: `afi_evidence.signals_lifecycle` vs `afi_analytics.market_ticks`
5. BigQuery vs Cloud SQL for **transactional** per-signal updates (mint write-back)
6. GCS role for raw payloads / proprietary blobs (`opaqueBlobRef`)
7. How `afi-mint` reads scored rows (BQ client, Pub/Sub push, pre-export to Cloud SQL)

Reference AFI types conceptually:
- `VaultedSignalRecord`, `MintSnapshot`, lifecycle enum RAW|ENRICHED|ANALYZED|SCORED|MINTED|REPLAYED
- Workspace: `afi-infra/src/tssd/types.ts` (shape reference, not implementation mandate)

---

## Phase 6 — Scoring & enrichment options (required)

Research how to implement scoring DAG on Mage+GCP **without** mandating afi-reactor:

1. Port UWR scoring (`afi-core/validators/UniversalWeightingRule.ts`) as Mage Python block
2. Call afi-reactor as HTTP sidecar (hybrid — when worth it?)
3. Vertex AI / custom ML blocks for ANALYZED stage (optional)
4. External API enrichment (Binance, news) — snapshot strategy for determinism
5. How mage-pipeline-examples **data-quality** pipelines map to USS validation
6. Pipeline metadata pinning: store `pipeline_uuid`, `block_versions`, `git_sha` on each output row

Compare to PySpark example: when Spark is necessary vs overkill for AFI signal volume.

---

## Phase 7 — Mint handoff & on-chain integration (required)

Mage does not mint on-chain. Research trigger patterns:

| Trigger | Mechanism | Pros/cons |
|---------|-----------|-----------|
| BQ row insert trigger | Log-based alert → Cloud Function → `afi-mint` | |
| Pub/Sub `signal.ready_for_mint` | Mage exporter publishes event | |
| Scheduled poll | Cloud Run cron scans BQ for SCORED rows | |
| Mage callback block | HTTP POST to mint service at end of pipeline | |

Requirements:
- Idempotency (no double mint per `signal_id`)
- Write `stages.minted` after tx confirm
- Testnet contracts unchanged (Base Sepolia coordinator)
- See `afi-docs/specs/audit/AFI_TESTNET_E2E_CHECKLIST.md` §1.4–1.7

---

## Phase 8 — Security, compliance, and production hardening (required)

- GCP IAM least-privilege for Mage service account
- Secret Manager for exchange API keys, emissions agent key
- VPC-SC / private Google access for BQ
- Mage Pro SOC2 relevance for financial data
- Audit logging (Cloud Audit Logs + pipeline run history)
- Data residency considerations

---

## Phase 9 — Competitive landscape beyond Mage (required)

Find options **similar or superior** for AFI's specific combo (orchestration + GCP + financial/signal data):

Research at minimum:
- **Orchestration:** Airflow/Composer, Prefect, Dagster, Kestra, Temporal, Windmill
- **Stream:** Dataflow, Managed Service for Kafka, Pub/Sub Lite, Fluvio, Redpanda
- **Warehouse:** BigQuery (primary), optional ClickHouse on GCE comparison
- **ML/feature:** Vertex Feature Store, Feast on GCP
- **iPaaS:** Workato, Tray — likely out of scope but note why

For each, one paragraph: **AFI fit score (1–10)** and **why not chosen for reference spine**.

---

## Phase 10 — Deliverables (strict format)

Write all outputs to a single report: `afi-docs/specs/audit/research/AFI_MAGE_GCP_ARCHITECTURE_RESEARCH.md`

### Required sections
1. **Executive summary** (≤ 1 page) — top recommendation for testnet MVP + top recommendation for production
2. **Example analysis recap** (§Part A condensed)
3. **Comparison matrix** — rows = architecture candidates, columns = 15+ evaluation criteria
4. **Ranked shortlist** (top 3) with explicit tradeoffs
5. **Recommended testnet MVP architecture** — full spec with BQ table DDL sketch, Mage pipeline block list, env vars, mint trigger
6. **Migration notes** — what to retire (Mongo path), what to keep (`afi-token`, `afi-config`, `afi-mint` interfaces)
7. **Open questions** for human decision (≤ 7)
8. **Source bibliography** — URLs, docs, pricing pages, GitHub repos, dated access

### Evaluation criteria (must appear in matrix)
- Time to testnet E2E
- Monthly cost (testnet / low prod)
- Ops/on-call burden
- GCP-native affinity (less cross-cloud)
- Mage-specific value-add (vs replaceable)
- Real-time analytics capability
- Per-signal evidence lifecycle support
- Determinism / replay readiness
- USS/schema validation support
- Mint handoff cleanliness
- Team skill fit (Python-heavy)
- Vendor lock-in risk
- Portable-protocol alignment
- Scalability to 100K signals/month
- Documentation & community maturity

---

## Research rules

1. **Prefer primary sources:** Mage docs (docs.mage.ai), GCP docs, pricing calculators, GitHub issues
2. **Flag marketing claims** from Mage blogs (e.g. "sub-second latency", "zero message loss") — verify or mark unverified
3. **Quantify where possible** — don't say "cheap"; say "$X/month at Y QPS assuming Z"
4. **Separate planes explicitly** — never recommend "put everything in one BQ table"
5. **Acknowledge afi-reactor** as legacy reference orchestrator, not mandatory
6. **Do not recommend Mongo** for new work unless comparing as anti-pattern
7. **Include at least one architecture with NO Kafka** (GCP-native streaming)
8. **Include at least one architecture with NO Mage** (pure GCP baseline)

## Out of scope
- Mainnet deployment hardening
- Token economics / gauge splits (single beneficiary OK for MVP)
- Building code — research and recommendations only
- Non-GCP clouds (mention only for portability comparison)

## Success criteria
A human reader can:
- Pick an MVP architecture in one meeting
- Update `AFI_TESTNET_E2E_CHECKLIST.md` with concrete GCP resource names
- Brief an engineer to stand up Mage + BQ + mint trigger in < 2 weeks (if recommendation supports it)

END MISSION
```

---

## Part C — How to run this research

| Step | Action |
|------|--------|
| 1 | Create output dir: `afi-docs/specs/audit/research/` |
| 2 | Paste **Part B** into deep research agent |
| 3 | Attach links to Part A examples + `AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md` |
| 4 | Review ranked shortlist against worksheet Q5/Q6 |
| 5 | Update [`AFI_TESTNET_E2E_CHECKLIST.md`](./AFI_TESTNET_E2E_CHECKLIST.md) with winning architecture |

---

## Part D — Expected human decisions after research (preview)

The research should force answers to:

1. **Batch vs stream** for testnet MVP?
2. **Pub/Sub vs Kafka** on GCP?
3. **BQ as evidence store** vs BQ analytics + Cloud SQL evidence?
4. **Mage Pro vs OSS** for first 90 days?
5. **Replace afi-reactor entirely** or HTTP sidecar during transition?
6. **Mint trigger:** poll vs event-driven?
7. **Spark:** needed day one or defer?

---

*Charter aligns with [`AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md`](../AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md) §3.2–3.4 and audit theme F (analytics plane).*
