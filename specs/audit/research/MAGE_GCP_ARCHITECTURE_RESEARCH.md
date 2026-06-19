# **AFI Protocol Infrastructure: Exhaustive Analysis of Mage.ai and GCP Architecture Pathways**

## **Executive Summary**

The strategic pivot from MongoDB (TSSD) to a Google Cloud Platform (GCP) and Mage.ai reference architecture marks a fundamental realignment of the Agentic Financial Intelligence (AFI) protocol. The legacy reliance on MongoDB introduced architectural scope creep and failed to strictly separate analytical market context from the transactional, per-signal evidence lifecycle. Furthermore, in-place document mutations fundamentally compromised the cryptographic determinism required for protocol challenge and replay mechanisms. Establishing GCP and Mage.ai as the reference spine prioritizes a low barrier-to-entry for testnet validators while offering a portable, scalable framework for production environments.  
Extensive analysis reveals that standard Mage.ai pipeline implementations—which typically focus on ingesting continuous streams of high-frequency cryptocurrency market data—are misaligned with the AFI protocol's core requirement: a highly deterministic, verifiable progression of discrete signal states (RAW → ENRICHED → ANALYZED → SCORED → MINTED → REPLAYED). The protocol requires rigid state orchestration rather than high-throughput tick aggregation.  
For the **testnet MVP**, the optimal architecture is a **Pub/Sub to Mage Streaming hybrid coupled with a BigQuery Append-Only Evidence Log**. This configuration bypasses the severe operational burden of self-managed Kafka clusters, leverages GCP-native exactly-once delivery semantics for idempotency, strictly isolates the analytics plane from the canonical evidence plane, and enables seamless event-driven handoffs to the afi-mint service for on-chain Base Sepolia commitments.  
For **production-grade evolution**, the architecture should transition toward leveraging BigQuery's Storage Write API for high-throughput market tick ingestion and Dataflow for continuous analytics, retaining Mage.ai exclusively as the orchestrator for discrete batch-scoring Directed Acyclic Graphs (DAGs) and pipeline metadata management.

## **Example Analysis Recap**

A critical evaluation of three canonical Mage.ai reference implementations reveals distinct architectural patterns alongside notable deficiencies when applied to the AFI protocol context. Existing references focus almost exclusively on aggregating market data into data warehouses, entirely omitting the concept of a state-machine-driven protocol lifecycle.

| Reference Implementation | Structural Pattern | Implications for AFI Protocol | Identified Deficiencies |
| :---- | :---- | :---- | :---- |
| **Kafka \+ Mage Pro Streaming \+ BigQuery** | Custom WebSocket producer feeding Apache Kafka; Mage consumes micro-batches (batch\_size: 100\) and exports to BigQuery1. | Separates data capture from processing. Provides a durable buffer for replay capabilities, scaling efficiently to high-frequency market data. | A continuous tick stream does not align with the VaultedSignalRecord lifecycle. Stateful transforms managed within Mage micro-batch boundaries risk state loss without external cache stores2. Self-managed Kafka creates an unacceptable operations burden for a testnet MVP. |
| **PySpark Batch \+ Mage Pro \+ BigQuery** | Scheduled batch triggers polling REST APIs; PySpark DataFrames manage distributed transformations3. | Represents the lowest barrier to entry and the fastest path to warehousing data. Explicit Spark StructType schemas provide a precedent for typed pipeline contracts. | Bypasses real-time requirements entirely. The reliance on df.toPandas() before BigQuery export is a documented anti-pattern that creates severe memory bottlenecks at scale. Dynamic Spark clusters are overkill for low-volume testnet signal generation. |
| **Mage Pipeline Pattern Library** | Modular Loader → Transformer → Exporter blocks; credential management via io\_config.yaml5. | Provides structural templates for isolating external API interactions and enforcing data quality validation. | Fails to implement deterministic pinning (e.g., embedding pipeline versions and git commit hashes into the output). Does not address event-driven handoffs to external commitment layers (e.g., Base Sepolia). |

The synthesis of these examples demonstrates that while Mage.ai excels at standard Extract-Transform-Load (ETL) operations, applying it directly to the AFI protocol requires strict modifications. Conflating the continuous market analytics plane with the discrete, canonical signal evidence plane will recreate the architectural flaws of the deprecated MongoDB implementation.

## **Phase 1: Mapping AFI Planes to Infrastructure**

To successfully implement the AFI protocol on GCP, infrastructure components must be strictly isolated across the five protocol planes. Mixing compute execution or storage responsibilities across these boundaries fundamentally compromises both determinism and scalability.

| Protocol Plane | AFI Requirement | Evaluated Infrastructure Options (GCP \+ Mage.ai) | Architectural Justification |
| :---- | :---- | :---- | :---- |
| **Ingest** | USS/CPJ-valid signals, standardized webhook entry points. | 1\. API Gateway → Pub/Sub 2\. Cloud Run Webhook → Pub/Sub 3\. Mage API Trigger | A dedicated Cloud Run Webhook publishing directly to Pub/Sub removes the Mage orchestrator from the synchronous critical path. This prevents dropped payloads during traffic spikes by utilizing Cloud Run's high concurrency limits (up to 1000 concurrent requests per instance)7. |
| **Scoring DAG** | Pinned transforms generating conforming outputs. | 1\. Mage Python Batch (Scheduled) 2\. Mage Streaming (Pub/Sub source) 3\. Cloud Run Jobs (Eventarc) | Mage Python blocks are optimal for the testnet MVP due to rapid authoring capabilities. For long-term production, isolating complex scoring logic into dedicated Cloud Run jobs decoupling compute limits from the orchestrator is necessary9. |
| **Evidence** | Canonical per-signal lifecycle tracking. | 1\. BigQuery Append-Only Log 2\. Cloud SQL (PostgreSQL) 3\. Firestore | BigQuery serves as an immutable, append-only ledger. Utilizing the native JSON column type for the VaultedSignalRecord provides a balance between schema evolution and performant analytical querying11. |
| **Analytics** | Continuous market and feature context. | 1\. BQ Native Pub/Sub Subscriptions 2\. Dataflow → BigQuery 3\. Mage Streaming → BigQuery | BigQuery natively supports direct ingestion from Pub/Sub subscriptions. Bypassing compute orchestrators entirely for raw tick data maximizes cost efficiency and minimizes latency13. |
| **Commitment** | Immutable BASE minting external to Mage. | 1\. Pub/Sub Push Subscription → Cloud Run 2\. Mage Callback HTTP POST 3\. BigQuery Log Analytics Trigger | A Pub/Sub push subscription triggering a Cloud Run instance (afi-mint) ensures event-driven, decoupled execution. This approach natively supports exponential backoff retries and dead-letter queues (DLQ) for failed blockchain transactions15. |

## **Phase 2: Evaluating Mage.ai Placement within the Ecosystem**

### **2.1 Mage Deployment Models on GCP**

Mage.ai can be deployed across several network topologies on GCP. Deploying Mage Open Source Software (OSS) via Cloud Run or Google Kubernetes Engine (GKE) provides the lowest initial infrastructure cost. Terraform-based deployment enables infrastructure-as-code principles, natively integrating GCP Secret Manager to securely inject API keys directly into the io\_config.yaml file via {{gcp\_secret\_var('...')}}17.  
Alternatively, Mage Pro Cloud offers a fully managed control plane, strict tenant isolation, SOC2 compliance, and built-in continuous integration and deployment (CI/CD) via Git integrations19. However, for an AFI testnet MVP that prioritizes open-source portability and low barrier-to-entry, a self-hosted Dockerized Mage instance on Cloud Run configured with the gcp\_cloud\_run executor type allows specific pipeline blocks to spin up isolated container instances, preventing resource exhaustion on the central server9.

### **2.2 Mage Pipeline Modes for AFI**

Mage supports multiple pipeline execution modalities. Selecting the correct mode is critical to maintaining the integrity of the AFI evidence lifecycle.

* **Batch \+ Cron Trigger:** Highly reliable and leverages cost-effective BigQuery batch exports. However, it fails to meet the real-time, event-driven signal minting requirements necessary for live protocol operation. This mode should be strictly reserved for offline feature engineering and historical backtesting.  
* **Streaming (Pub/Sub Loader):** Enables real-time progression of signals through the lifecycle stages. The primary risk involves stateful transforms. Mage's stateful streaming relies on external Redis instances for cross-batch state continuity2. Improperly managed batch boundaries may result in the scoring DAG failing to compile necessary historical state for active signals.  
* **Python-only Blocks:** Standardizes the scoring DAG into highly readable, portable Python modules without the overhead of Java Virtual Machines (JVMs) or PySpark cluster management. This is the optimal configuration for the testnet MVP.  
* **dbt Blocks in Mage:** Excellent for the downstream analytics plane to construct dimensional silver and gold views from raw tick data23. It is irrelevant for the transactional evidence plane, which relies on JSON payloads rather than relational joins.

### **2.3 Mage vs. GCP-Native Orchestration Alternatives**

The orchestration landscape offers several alternatives to Mage.ai. Evaluating these clarifies Mage's specific value proposition for the AFI protocol.

* **Cloud Composer (Apache Airflow):** Replaces Mage entirely. Airflow represents the mature industry standard but carries a massive operational burden. The split architecture (metadata database, scheduler, web server, DAG processor, and worker nodes) demands significant baseline costs just to maintain an idle environment25. It is definitively inferior for an agile AFI testnet.  
* **Cloud Workflows \+ Cloud Run Jobs:** Replaces Mage entirely. This configuration is lightweight, entirely serverless, and native to GCP. It excels at orchestrating HTTP APIs but completely lacks a visual DAG builder, data-centric execution context, and inline data previewing10. It is complementary for triggering long-running scoring tasks but lacks developer ergonomics for building pipelines.  
* **Dataflow (Apache Beam):** Replaces Mage for high-volume streaming. Dataflow provides true exactly-once streaming semantics and unified batch/stream processing14. While optimal for the analytics plane, developing Apache Beam topologies is excessively complex for orchestrating the discrete, sequential signal scoring DAG.  
* **dbt \+ BigQuery Scheduled Queries:** Complementary to Mage. Useful only for post-processing the analytics plane. Cannot handle the webhooks or Python-based scoring algorithms required by AFI.

### **2.4 Identified Mage Gaps for Protocol Use Cases**

Exhaustive analysis reveals several technical gaps within Mage.ai regarding AFI's strict protocol requirements.

1. **Contract Testing and Schema Enforcement:** Mage lacks native integration for JSON Schema validation. Validating incoming payloads against normative afi-config Universal Signal Standard (USS v1.1) definitions requires custom Python blocks.  
2. **Deterministic Pipeline Versioning:** AFI requires cryptographic proof of the execution environment. Mage does not natively inject its own internal identifiers or Git commit hashes into every output row automatically. Determinism pinning requires custom boilerplate in every exporter block to explicitly extract kwargs.get('pipeline\_uuid') and the underlying GIT\_SHA to append to the signal metadata20.  
3. **Exactly-Once Semantics to BigQuery:** While Mage advertises exactly-once processing, this relies on strict internal checkpointing. Writing to BigQuery via pandas DataFrames—as demonstrated in Mage tutorials—risks duplicate row insertion upon network retries. Utilizing the BigQuery Storage Write API within the exporter block is necessary to enforce exactly-once semantics at the storage layer28.

## **Phase 3: GCP Messaging and Storage Matrix**

The absolute distinction between the Analytics Plane (high-frequency, low-value market context) and the Evidence Plane (low-frequency, high-value protocol state changes) dictates that a single message bus should not serve both. Conflating the two violates the separation of concerns necessary for protocol scalability.

| Messaging/Storage Pattern | Latency Profile | Estimated Cost Implications | Determinism / Replayability | Ops Burden | Fit for AFI Protocol |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **A. Kafka on GCP (Confluent / GKE)** | Sub-millisecond | $200 \- $800+ per month | Excellent (Native log replay via offset manipulation) | 5/5 (Requires Zookeeper/Kraft, partition tuning) | **Inferior.** Massively overpowered for testnet signal volume; violates the lowest-barrier-to-entry directive1. |
| **B. Pub/Sub Native** | \~50-100ms | \< $10/month (Pay per byte) | Good (7-day retention, replay via topic snapshots) | 1/5 (Fully managed, serverless) | **Optimal for Evidence.** Handles event routing seamlessly. Recent additions of exactly-once delivery guarantees natively solve idempotency16. |
| **C. Batch-Only (No Bus)** | Minutes to Hours | \~$0 (Free tier utilization) | Moderate (Relies entirely on source system state) | 1/5 | **Inferior.** Fails to support prompt, event-driven on-chain commitments. |
| **D. BQ Storage Write API** | Seconds | $0.025 per GiB (First 2 TiB free) | Moderate (Data lands immediately in warehouse) | 1/5 | **Optimal for Analytics.** Bypasses middleware entirely; handles millions of rows effortlessly through gRPC streaming28. |
| **E. GCS Landing \+ Batch** | Minutes | Near zero | Excellent (Immutable raw blobs) | 2/5 | **Complementary.** Useful for storing massive, opaque payload blobs (opaqueBlobRef), referenced via URI in the BigQuery evidence store31. |

**Architectural Recommendation:** The **Analytics Plane** must utilize direct ingestion into BigQuery via the Storage Write API or a native Pub/Sub-to-BigQuery subscription to eliminate compute overhead13. Conversely, the **Evidence Plane** must utilize **Pub/Sub** to orchestrate lifecycle state transitions. Pub/Sub's tracking of acknowledgment states provides exactly-once delivery guarantees within a single cloud region, making it a highly viable, low-maintenance replacement for Kafka in this architecture29.

## **Phase 4: Reference Architecture Candidates**

The following five architectural candidates are structured and ranked in order of suitability for the AFI testnet MVP, optimizing for engineering velocity while maintaining a pathway to production scaling.

### **C1: The Pub/Sub \+ Mage Event-Driven Backbone (Rank 1: Optimal MVP)**

* **Name:** Pub/Sub \+ Mage Stream \+ BQ Append-Log  
* **Component List:** Cloud Run (Ingest API), Pub/Sub (Topics per stage), Mage OSS (Scoring/Enrichment), BigQuery (Evidence Store), Cloud Run (afi-mint).  
* **Data Flow:**  
  1. An external webhook payload strikes the Cloud Run Ingest API. The service validates the payload against USS v1.1 schemas and publishes it to the signal-raw Pub/Sub topic.  
  2. A Mage Streaming Pipeline consumes the signal-raw topic, executing the Python enrichment and scoring DAG.  
  3. The Mage exporter block writes the output to the BigQuery signals\_lifecycle table (append-only) AND simultaneously publishes the payload to the signal-scored Pub/Sub topic.  
  4. A Pub/Sub push subscription natively triggers the afi-mint Cloud Run service.  
  5. afi-mint executes the Base Sepolia transaction, waits for the receipt, and publishes to the signal-minted topic.  
  6. A separate Mage micro-batch consumes signal-minted and appends the final protocol row to BigQuery.  
* **AFI Lifecycle Mapping:** RAW and SCORED states are transiently held in Pub/Sub and durably logged in BigQuery. MINTED is confirmed via the blockchain and reflected as the terminal state in BigQuery.  
* **Determinism Story:** Absolute. Mage explicitly injects git\_sha and pipeline\_version into the scored payload. The BigQuery append-log preserves all historical transitions, enabling exact timeline reconstruction.  
* **Estimated Monthly Cost:** \~$30-50 (Assuming minimal testnet traffic and Mage hosted on a basic Cloud Run/GCE instance).  
* **Time-to-first-E2E:** 1.5 \- 2 weeks.  
* **Ops Burden:** 2/5. The infrastructure is entirely serverless with the exception of the Mage instance itself.  
* **Portable Protocol Fit:** Excellent. Any third-party validator can swap Pub/Sub for RabbitMQ, or Mage for native Python scripts, without altering the protocol's mathematical execution.

Code snippet  
graph TD  
    A\[External Signal\] \--\> B(Cloud Run: Ingest Gateway)  
    B \--\>|USS Validated| C{Pub/Sub: signal-raw}  
    C \--\> D\[Mage.ai: Scoring DAG\]  
    D \--\>|Append Row| E\[(BigQuery: Evidence Log)\]  
    D \--\>|Publish| F{Pub/Sub: signal-scored}  
    F \--\>|Push| G(Cloud Run: afi-mint)  
    G \--\>|TxHash| H{Pub/Sub: signal-minted}  
    H \--\>|Append Row| E  
    G \-.-\>|Mint| I\[Base Sepolia\]

### **C2: The Cloud-Native Orchestrator (Rank 2: Production Baseline)**

* **Name:** Pub/Sub \+ Cloud Run Jobs \+ Workflows \+ BQ  
* **Component List:** Pub/Sub, Eventarc, Cloud Workflows, Cloud Run Jobs (Scoring), BigQuery.  
* **Data Flow:** Ingest to Pub/Sub → Eventarc triggers Cloud Workflow → Workflow executes a Cloud Run Job containing the scoring script → Job writes to BigQuery via the Storage Write API → Workflow triggers afi-mint.  
* **Determinism Story:** Container image hashes used for Cloud Run Job execution environments provide absolute, immutable determinism.  
* **Estimated Monthly Cost:** \~$20.  
* **Time-to-first-E2E:** 3 \- 4 weeks (Requires custom YAML orchestration logic).  
* **Ops Burden:** 1.5/5.  
* **Portable Protocol Fit:** Poor. This architecture deeply couples the protocol to GCP Cloud Workflows10. It actively eliminates Mage, rendering the reference architecture highly proprietary to Google Cloud.

### **C3: The Simplest Path (Rank 3: Rapid Prototyping Only)**

* **Name:** Mage Batch MVP \+ BQ Log Trigger  
* **Component List:** Mage OSS, BigQuery, Cloud Functions.  
* **Data Flow:** A Mage batch pipeline runs every 5 minutes. It pulls from an external REST API, scores the signals, and performs a batch load to a BigQuery table. BigQuery Log Analytics detects the INSERT operation, triggering a Cloud Function which calls afi-mint.  
* **Determinism Story:** Poor. It is exceedingly difficult to guarantee exact state matching if the upstream API changes data between the 5-minute polling windows.  
* **Estimated Monthly Cost:** \~$15.  
* **Time-to-first-E2E:** \< 1 week.  
* **Ops Burden:** 1/5.  
* **Portable Protocol Fit:** High. However, it completely violates the real-time minting requirements and relies on fragile BigQuery audit-log triggers for crucial on-chain actions.

### **C4: The Analytics Heavyweight (Rank 4: Overkill)**

* **Name:** Dataflow Unified Streaming  
* **Component List:** Pub/Sub, Dataflow (Apache Beam), BigQuery.  
* **Data Flow:** A compiled Beam pipeline handles windowing, enrichment, and scoring within a single, highly distributed graph.  
* **Determinism Story:** Excellent. Apache Beam guarantees exactly-once processing semantics and rigorous state checkpointing14.  
* **Estimated Monthly Cost:** $150 \- $300+ (Dataflow continuous streaming instances require persistent compute allocation)14.  
* **Time-to-first-E2E:** 4 \- 6 weeks (Java/Python Beam development is notoriously slow).  
* **Ops Burden:** 4/5.  
* **Portable Fit:** Fair. Apache Beam is open-source (capable of running on Flink or Spark), but it is operationally restrictive for lightweight validators.

### **C5: The Legacy Pipeline (Rank 5: Anti-Pattern)**

* **Name:** Kafka \+ Mage Stream \+ BQ Dual-Dataset  
* **Component List:** Confluent Cloud Kafka, Mage Pro, BigQuery.  
* **Data Flow:** Directly replicates the Mage Kafka tutorial architecture1.  
* **Estimated Monthly Cost:** $400+.  
* **Ops Burden:** 5/5. Managing Kafka schemas, partitioning logic, and Zookeeper/Kraft configurations for low-volume testnet data represents a severe misallocation of engineering resources.

## **Phase 5: Evidence Store Design on BigQuery**

The architectural departure from MongoDB TSSD centers on resolving the "Mongo mistake": allowing in-place mutations of document state. Modifying a signal document from RAW to SCORED silently destroys the historical state and breaks the cryptographic replayability required for decentralized challenge windows. BigQuery must not be treated as an Online Transaction Processing (OLTP) database.

1. **Architecture (Append-Only Event Log vs. MERGE):** BigQuery's MERGE statement is severely rate-limited. Under on-demand pricing, BigQuery limits DML UPDATE/MERGE operations to 20 per table per day32. Therefore, the evidence store must be designed as an **append-only event log**. Every lifecycle state change (RAW, SCORED, MINTED) mandates the insertion of a completely *new row*.  
2. **Table Schema and JSON Columns:** Avoid excessive schema normalization for the signal payload. The VaultedSignalRecord should utilize BigQuery's native JSON data type for the payload and metadata fields. BigQuery physically shreds JSON data into virtual columns at ingestion. This ensures that querying nested fields (e.g., SELECT payload.signal\_strength) only scans the required binary data, applying Dictionary and Run Length Encoding, which saves upwards of 25% on logical bytes scanned compared to legacy stringified JSON11.  
3. **Partitioning and Clustering Strategy:** The evidence table (afi\_evidence.signals\_lifecycle) must be partitioned by an ingestion timestamp (DATE(ingested\_at)) to tightly control query scan costs over time. It must be clustered by signal\_id and stage. This clustering enables rapid, cost-effective retrieval of a specific signal's entire lifecycle history by pruning unneeded storage blocks34.  
4. **Strict Plane Separation:** A rigid dataset separation is required. afi\_evidence holds the deterministic, protocol-critical signal states. afi\_analytics.market\_ticks holds continuous market data. They must never be conflated within the same dataset or queried via cross-joins during standard protocol operations.  
5. **Transactionality and Mint Write-Backs:** Because BigQuery is not an OLTP database, the orchestrator (Pub/Sub) manages the transaction boundary. The afi-mint service does not poll BigQuery; it receives the scored payload via a Pub/Sub push containing the full JSON payload, executes the blockchain transaction, and writes the resulting MINTED status back to Pub/Sub. The final BigQuery insertion acts merely as a historical ledger entry.  
6. **GCS Landing for Raw Payloads:** Any proprietary, massively sized blobs (opaqueBlobRef) must not enter BigQuery. They must be routed directly to Google Cloud Storage (GCS) as immutable objects, with BigQuery storing only the reference URI (gs://bucket-name/blob\_id)31.

## **Phase 6: Scoring & Enrichment Options**

To decouple the architecture from the legacy afi-reactor while retaining strict protocol determinism, the scoring Directed Acyclic Graph (DAG) must be meticulously constructed.

1. **Porting UWR to Mage:** The Universal Weighting Rule (UWR) logic currently residing in afi-core/validators/UniversalWeightingRule.ts must be ported to a standalone Mage Python block. This block acts as a pure function: it accepts a dictionary (the signal), applies the mathematical weighting, and returns a modified dictionary.  
2. **Sidecar Architecture Transition:** During the migration phase, calling afi-reactor as an HTTP sidecar from within a Mage block is a highly viable hybrid pattern. This allows the legacy TypeScript validation logic to run unmodified inside a separate Cloud Run container36, while Mage manages the orchestration, retries, and data movement.  
3. **Determinism Pinning in Pipeline Metadata:** Mage blocks must be configured to append cryptographic proofs of the execution environment to the output payload. Specifically, the environment variable MAGE\_PIPELINE\_UUID, the Git commit hash (GIT\_SHA), and the specific afi-config schema version must be appended to the metadata object of the VaultedSignalRecord before it is flushed to the BigQuery log37.  
4. **External API Enrichment Snapshots:** Fetching external context (e.g., live Binance pricing data) inherently breaks determinism if the exact response is not preserved. The enrichment block must pull the external data, stamp it with the exact retrieval timestamp, and store the raw response within the RAW or ENRICHED row in BigQuery. Subsequent scoring blocks must *only* calculate based on the data contained in that specific BigQuery row, never executing outbound network requests themselves.

## **Phase 7: Mint Handoff & On-Chain Integration**

Mage.ai is fundamentally an orchestration and data movement platform; it is not designed to securely sign and broadcast Ethereum or Base transactions. The mechanism utilized to hand off the scored signal to the afi-mint service is critical for preventing duplicate on-chain commitments.

| Trigger Mechanism | Execution Flow | Idempotency & Replayability | Verdict |
| :---- | :---- | :---- | :---- |
| **Pub/Sub Push** | Mage outputs to a signal-scored topic. Topic pushes to the afi-mint Cloud Run URL. | Handled via Pub/Sub unique message IDs. If afi-mint crashes, Pub/Sub retries automatically. | **Highly Recommended.** Event-driven, low latency, robust DLQ support16. |
| **BigQuery Row Trigger** | Log-based metric detects new row → Triggers Cloud Function → calls afi-mint. | Poor. Audit logs can be delayed. Complex to pass the actual row data to the function securely. | **Rejected.** Fragile, high latency, and difficult to debug. |
| **Scheduled Poll** | Cloud Run cron job runs every 1 minute, querying BQ for stage \= SCORED. | Requires stateful tracking of which rows have been sent to avoid double minting. | **Rejected.** Introduces unnecessary BigQuery compute scan costs and high latency. |
| **Mage Callback** | Mage HTTP block POSTs to afi-mint at the end of the pipeline. | High risk of double minting if the Mage block retries after a network timeout (even if the blockchain tx succeeded). | **Rejected.** |

**Idempotency and Base Sepolia Integration:** The afi-mint service must be structurally idempotent. It must query the Base Sepolia coordinator contract to verify if the signal\_id has already been minted before signing a new transaction.  
Furthermore, Base Sepolia utilizes "Flashblocks"—a preconfirmation mechanism that builds sub-blocks every 200 milliseconds, reducing effective block times by a factor of ten38. The afi-mint service can utilize Flashblock RPC endpoints to achieve near-instant inclusion confirmation without waiting for the full 2-second Ethereum block cadence, accelerating the write-back of the MINTED state to the evidence log.

## **Phase 8: Security, Compliance, and Production Hardening**

Financial signal intelligence requires robust infrastructure security at every layer of the architecture.

* **VPC Service Controls (VPC-SC):** BigQuery and Pub/Sub must be enclosed within a VPC Service Perimeter to prevent unauthorized data exfiltration31. Because Cloud Run functions operate on Google-managed infrastructure outside the customer VPC by default, they require a Serverless VPC Access connector or Direct VPC Egress configured with \--egress-settings=all to securely interact with the protected BigQuery API via the restricted.googleapis.com VIP42.  
* **Secret Management Integration:** Hardcoding exchange API keys or wallet private keys in io\_config.yaml is strictly prohibited. Mage natively integrates with GCP Secret Manager18. The afi-mint service must retrieve the Base Sepolia emissions agent private key dynamically from Secret Manager at runtime, ensuring keys are never written to disk, exposed in container environment variables, or printed in Cloud Logging.  
* **Least-Privilege IAM:** The Mage service account must be heavily restricted. It requires only roles/pubsub.publisher, roles/pubsub.subscriber, and roles/bigquery.dataEditor. It must *strictly not* have IAM permissions to access the Secret Manager payload containing the afi-mint private key.

## **Phase 9: Competitive Landscape Beyond Mage.ai**

While Mage.ai provides an excellent visual interface and strong integration with GCP, the broader orchestration and data pipeline landscape presents viable alternatives. Analyzing these alternatives clarifies why Mage.ai was selected for the reference spine.

* **Apache Airflow / Cloud Composer:** The industry standard for data orchestration. **AFI Fit Score: 4/10.** *Why not chosen:* Airflow carries an extremely heavy operational burden, features a steep Python DAG learning curve, and is primarily designed for slow, batch-oriented data warehousing rather than rapid, event-driven signal progression25.  
* **Prefect:** Code-as-workflows orchestration. **AFI Fit Score: 6/10.** *Why not chosen:* Prefect executes pure Python as distributed workflows flawlessly and offers excellent developer ergonomics43. However, it lacks native data integration blocks and visual ETL capabilities, requiring protocol engineers to write all BigQuery and Pub/Sub integration boilerplate manually26.  
* **Dagster:** An asset-centric orchestrator. **AFI Fit Score: 7/10.** *Why not chosen:* Dagster's Software-Defined Assets (SDAs) provide unparalleled data lineage tracking, which aligns perfectly with protocol determinism requirements. However, the conceptual learning curve is substantial, and it lacks the immediate low-code visual blocks that Mage provides for a rapid testnet MVP45.  
* **Kestra:** YAML-based, event-driven orchestration. **AFI Fit Score: 8/10.** *Why not chosen:* Kestra is arguably the strongest direct competitor to Mage for the AFI protocol. It is natively event-driven, handles Kafka/PubSub triggers elegantly, and utilizes accessible declarative YAML46. Mage was selected over Kestra primarily for its interactive notebook interface, which drastically reduces the time-to-first-E2E for onboarding new developers3.  
* **Temporal:** Durable execution engine. **AFI Fit Score: 5/10.** *Why not chosen:* Temporal provides invincible stateful durability through code replay47. However, writing Temporal workflows requires deep SDK knowledge and it is not explicitly designed for data pipeline orchestration or warehouse integration.  
* **Vertex Feature Store / Feast:** Machine Learning feature stores. **AFI Fit Score: 3/10.** *Why not chosen:* Feature stores are designed to solve train/serve skew for deep learning models by providing low-latency online serving49. The AFI protocol currently relies on discrete deterministic mathematical scoring (UWR), not real-time serving of complex embedding vectors. Deploying a feature store would introduce massive infrastructure cost ($0.30/hr/node minimum) with zero tangible benefit to the protocol50.

## **Phase 10: Deliverables**

### **Comparison Matrix: Architecture Candidates**

| Evaluation Criteria | C1: Batch-Only MVP | C2: Pub/Sub \+ Mage Stream | C3: Kafka \+ Mage Stream | C4: Dataflow Unified | C5: Airflow Baseline |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **Time to testnet E2E** | \< 1 week | **1.5 \- 2 weeks** | 3 \- 4 weeks | 4 \- 6 weeks | 3 \- 4 weeks |
| **Monthly Cost (Testnet)** | \~$15 | **\~$40** | $300+ | $150+ | $300+ |
| **Ops/On-call Burden** | 1 (Lowest) | **2 (Low)** | 5 (Highest) | 4 (High) | 4 (High) |
| **GCP-Native Affinity** | High | **High** | Low | Very High | High |
| **Mage Value-Add** | High (ETL logic) | **High (Streaming UI)** | High | Low | N/A |
| **Real-Time Capability** | None | **Good (\~100ms)** | Best (\<10ms) | Best (\<10ms) | None |
| **Evidence Lifecycle** | Poor (Batch overlaps) | **Excellent (Event logs)** | Excellent | Good | Poor |
| **Determinism/Replay** | Moderate | **Excellent** | Excellent | Excellent | Moderate |
| **USS Schema Valid.** | Manual Python | **Manual Python** | Schema Registry | Native Beam | Manual Python |
| **Mint Handoff** | High latency poll | **Event-driven push** | Event-driven | Event-driven | High latency poll |
| **Team Skill Fit** | High (Python) | **High (Python)** | Low (Java/Scala) | Low (Java/Beam) | High (Python) |
| **Vendor Lock-in Risk** | Low | **Low** | High (Confluent) | High (Dataflow) | Low |
| **Portable Protocol Fit** | Excellent | **Excellent** | Poor (Kafka coupled) | Poor (Beam coupled) | Moderate |
| **Scale to 100K/mo** | Yes | **Yes** | Yes | Yes | Yes |

### **Ranked Shortlist & Explicit Tradeoffs**

1. **Candidate 2: Pub/Sub \+ Mage Stream \+ BQ Append-Log (Winner)**  
   * *Explicit Tradeoffs:* Sacrifices the absolute sub-millisecond latency guarantees of Kafka, but eliminates 90% of the operational overhead. It relies on Pub/Sub exactly-once semantics, which are highly robust but strictly region-locked, preventing global active-active replication without duplicate handling29.  
2. **Candidate 1: Mage Batch MVP \+ BQ Poll**  
   * *Explicit Tradeoffs:* Extremely cheap and fast to build. However, it sacrifices all real-time capabilities. This architecture is suitable *only* if the testnet parameters can tolerate signal-to-mint latencies exceeding 5 minutes.  
3. **Candidate 4: Dataflow Unified Streaming**  
   * *Explicit Tradeoffs:* This is the most technically robust distributed systems architecture for GCP. However, writing Apache Beam pipelines in Java or Python drastically increases development time, creates developer friction, and introduces persistent compute costs that violate the low-barrier-to-entry objective for validators.

### **Recommended Testnet MVP Architecture Specification**

Based on exhaustive analysis, **Candidate 2 (Pub/Sub \+ Mage Stream \+ BQ Append-Log)** is the definitive choice for the AFI reference spine.  
**Architecture Flow:**

1. **Ingress:** A lightweight Cloud Run service exposes a webhook. It validates the payload against afi-config USS v1.1 schemas and publishes the payload to a Pub/Sub topic: projects/afi-testnet/topics/signal-raw.  
2. **Orchestration:** A self-hosted Mage.ai instance (deployed via Docker on Cloud Run or a minimum GCE instance) runs a continuous Streaming Pipeline.  
3. **Mage Pipeline Blocks:**  
   * Loader: Subscribes to the Pub/Sub topic (signal-raw).  
   * Transformer 1: Python block executing the ported UWR scoring logic. Explicitly appends pipeline\_uuid and git\_sha to the payload metadata.  
   * Exporter 1: Writes the resulting state to BigQuery. It must utilize the Storage Write API for exactly-once ingestion to prevent duplicates28.  
   * Exporter 2: Publishes the scored payload to a subsequent Pub/Sub topic: projects/afi-testnet/topics/signal-scored.  
4. **Commitment:** A Pub/Sub Push Subscription is attached to signal-scored, pushing directly to the afi-mint Cloud Run service URL16. afi-mint deduplicates the request, signs the transaction, mints to Base Sepolia, and writes the transaction receipt back to a signal-minted topic, which is subsequently ingested into the BigQuery evidence log.

**BigQuery DDL Sketch:**

SQL  
CREATE TABLE \`afi\-testnet.afi\_evidence.signals\_lifecycle\` (  
    signal\_id STRING NOT NULL,  
    epoch\_id INT64 NOT NULL,  
    stage STRING NOT NULL, \-- Allowed values: 'RAW', 'SCORED', 'MINTED'  
    ingested\_at TIMESTAMP DEFAULT CURRENT\_TIMESTAMP(),  
    payload JSON,          \-- Native JSON data type for USS payload body  
    metadata JSON,         \-- Contains pipeline\_uuid, git\_sha, tx\_hash  
    PRIMARY KEY (signal\_id, stage) NOT ENFORCED  
)  
PARTITION BY DATE(ingested\_at)  
CLUSTER BY signal\_id, stage  
OPTIONS(  
    description \= "Append-only immutable event log for AFI protocol signal state transitions."  
);

### **Migration Notes and Legacy Retirement**

* **Retire:** The entire MongoDB TSSD stack must be deprecated and removed from the active critical path. Any legacy code relying on in-place document mutations (e.g., utilizing db.collection.updateOne) is fundamentally incompatible with the new append-only BigQuery architecture and breaks protocol determinism.  
* **Keep:** The afi-config USS schemas remain the absolute normative source of truth. The schemas must be dynamically loaded by the Ingest Cloud Run service to validate JSON payloads *before* they enter the Pub/Sub buffer.  
* **Keep:** The afi-token smart contracts and afi-mint service interfaces remain functionally identical. The primary modification to afi-mint is architectural: it now acts as an event-driven web server responding to HTTP POST requests from a Pub/Sub push subscription, rather than a cron-driven worker continuously polling a database.

### **Open Questions for Architectural Decision**

1. **Testnet Latency Tolerance:** Can the initial testnet MVP tolerate a 1-to-5 minute delay between signal ingestion and on-chain minting? If yes, Candidate 1 (Batch) could save approximately one week of engineering time over Candidate 2 (Pub/Sub Stream).  
2. **Mage OSS vs Mage Pro:** Does the operational budget allow for licensing Mage Pro to avoid self-managing the Cloud Run/GCE deployment, while gaining native GitHub CI/CD deployments and role-based access control (RBAC)?  
3. **Sidecar vs Python Port:** Should the engineering team expend resources porting the UWR validation logic from TypeScript to Python (for native execution within a Mage block), or deploy the legacy afi-reactor codebase immediately as a sidecar container to accelerate time-to-market?  
4. **Pub/Sub Region Locking:** Pub/Sub exactly-once delivery guarantees apply strictly within a single GCP region. Is cross-region high-availability a strict requirement for the testnet phase? (Architectural Recommendation: No, single-region is sufficient for MVP).  
5. **Handling Opaque Blobs:** If signal payloads regularly exceed 1MB (Pub/Sub maximum message size) or 10MB (BigQuery cell limit), they must route to GCS. Are large opaque blobs anticipated in the MVP phase?  
6. **VPC-SC Enforcement:** Will VPC Service Controls be strictly enforced on day one of the testnet, or introduced as a post-MVP production hardening step? Enforcing VPC-SC immediately requires configuring Serverless VPC Access connectors for all Cloud Run instances.  
7. **Flashblocks Utilization:** Will the afi-mint service integrate with Base Sepolia Flashblock RPC endpoints to utilize 200ms preconfirmations, or rely on standard 2-second block finality?

### **Source Bibliography**

* \[1\] Mage.ai Documentation: Introduction and Deployments. Available at: https://mage-ai-mage-ai.mintlify.app/introduction  
* \[3\] Mage.ai Documentation: GCP Cloud Run Executor. Available at: https://docs.mage.ai/production/executors/gcp  
* \[5\] Mage.ai Documentation: Deploying to GCP Setup and Permissions. Available at: https://docs.mage.ai/production/deploying-to-cloud/gcp/setup  
* \[6\] Mage.ai Documentation: GCP Secret Manager Integration. Available at: https://docs.mage.ai/production/deploying-to-cloud/secrets/GCP  
* \[7\] Mage.ai Documentation: Data Loading and io\_config.yaml. Available at: https://docs.mage.ai/design/data-loading  
* \[9\] Mage.ai Documentation: Mage Secret Manager. Available at: https://docs.mage.ai/production/deploying-to-cloud/secrets/mage  
* \[19\] Mage.ai Documentation: Streaming Stateful Store. Available at: https://docs.mage.ai/guides/streaming/tutorials/streaming-stateful-store  
* \[21\] OneUptime Blog: Debugging BigQuery DML Quota Exceeded Errors. Available at: https://oneuptime.com/blog/post/2026-02-17-how-to-debug-bigquery-dml-quota-exceeded-errors-for-high-frequency-table-updates/view  
* \[24\] E6Data: BigQuery Query and Cost Optimization. Available at: https://www.e6data.com/query-and-cost-optimization-hub/how-to-optimize-bigquery-costs  
* \[26\] Google Cloud Documentation: BigQuery JSON Data. Available at: https://docs.cloud.google.com/bigquery/docs/json-data  
* \[29\] Google Cloud Blog: How BigQuery Powers Semi-Structured Data Storage. Available at: https://cloud.google.com/blog/products/databases/how-bigquery-powers-semi-structured-data-storage  
* \[33\] Mage.ai Documentation: Version Control Guide and CI/CD. Available at: https://docs.mage.ai/guides/data-sync/version-control-guide  
* \[36\] OneUptime Blog: BigQuery DML Limits and Streaming Inserts. Available at: https://oneuptime.com/blog/post/2026-02-17-how-to-debug-bigquery-dml-quota-exceeded-errors-for-high-frequency-table-updates/view  
* \[39\] E6Data: BigQuery Streaming Optimization. Available at: https://www.e6data.com/query-and-cost-optimization-hub/how-to-optimize-bigquery-costs  
* \[44\] Google Cloud Blog: Shredding JSON in BigQuery. Available at: https://cloud.google.com/blog/products/databases/how-bigquery-powers-semi-structured-data-storage  
* \[45\] Stack Overflow: Cost and Performance of BigQuery JSON Type. Available at: https://stackoverflow.com/questions/76305485/whats-the-cost-and-performance-implications-for-bigquery-native-json-data-type  
* \[50\] Mage.ai Documentation: Migrating from OSS to Mage Pro. Available at: https://docs.mage.ai/migrations/mage-oss-to-mage-pro  
* \[51\] Bruin Blog: Best Data Pipeline Tools in 2026 (Airflow vs Mage vs Prefect vs Dagster). Available at: https://getbruin.com/blog/best-data-pipeline-tools-2026/  
* \[52\] Kestra Blog: Top 5 Alternatives to Mage.ai. Available at: https://kestra.io/resources/data/mage-alternatives  
* \[53\] Mage.ai Documentation: Migrating from Prefect to Mage Pro. Available at: https://docs.mage.ai/migrations/prefect-to-mage-pro  
* \[54\] Sliplane Blog: 5 Awesome Mage.ai Alternatives. Available at: https://sliplane.io/blog/5-awesome-mage-ai-alternatives  
* \[55\] Kestra vs Temporal Orchestration Comparison. Available at: https://kestra.io/vs/temporal  
* \[56\] Kestra vs Dagster Orchestration Comparison. Available at: https://kestra.io/vs/dagster  
* \[59\] Orchestra Blog: Dagster vs Kestra Key Differences 2024\. Available at: https://www.getorchestra.io/guides/dagster-vs-kestra-key-differences-2024  
* \[69\] Mage.ai Documentation: Block Executor Configurations. Available at: https://docs.mage.ai/extensibility/api-reference/blocks/overview  
* \[70\] Mage.ai Documentation: GCP Cloud Run Block Execution. Available at: https://docs.mage.ai/production/executors/gcp  
* \[72\] Google Cloud: BigQuery Storage Write API Pricing. Available at: https://cloud.google.com/bigquery  
* \[73\] Google Cloud Documentation: BigQuery Pricing. Available at: https://cloud.google.com/bigquery/pricing  
* \[75\] Google Cloud Documentation: BigQuery Storage Write API. Available at: https://docs.cloud.google.com/bigquery/docs/write-api  
* \[77\] Feast Documentation: Feature Store Architecture. Available at: https://docs.feast.dev/  
* \[81\] Google Cloud Documentation: Cloud Run Concurrency Limits. Available at: https://docs.cloud.google.com/run/docs/about-concurrency  
* \[82\] Google Cloud Documentation: Configuring Cloud Run CPU Limits. Available at: https://docs.cloud.google.com/run/docs/configuring/services/cpu  
* \[83\] Google Cloud Documentation: Cloud Run Jobs CPU Configurations. Available at: https://docs.cloud.google.com/run/docs/configuring/jobs/cpu  
* \[84\] OneUptime Blog: Cloud Run Request Timeout and Retry Policies. Available at: https://oneuptime.com/blog/post/2026-02-17-how-to-configure-cloud-run-request-timeout-and-retry-policies-for-long-running-tasks/view  
* \[85\] Google Cloud Documentation: Cloud Run Resource Limits. Available at: https://docs.cloud.google.com/run/quotas  
* \[86\] Google Cloud Documentation: Pub/Sub Exactly-Once Delivery. Available at: https://docs.cloud.google.com/pubsub/docs/exactly-once-delivery  
* \[87\] Google Cloud Documentation: Pub/Sub to BigQuery Subscriptions. Available at: https://docs.cloud.google.com/pubsub/docs/bigquery  
* \[89\] OneUptime Blog: Streaming Dataflow Pipeline from Pub/Sub to BigQuery. Available at: https://oneuptime.com/blog/post/2026-02-17-how-to-read-from-pubsub-and-write-to-bigquery-in-a-streaming-dataflow-pipeline/view  
* \[90\] Medium: Google Pub/Sub Subscription Concepts. Available at: https://medium.com/@kandaanusha/google-pub-sub-subscription-concepts-cfed07648352  
* \[91\] Chainstack Blog: Base RPC Endpoint and Flashblocks. Available at: https://chainstack.com/learn/how-to/how-to-get-base-rpc-endpoint-for-defi-2026/  
* \[92\] Alchemy Documentation: Base Flashblocks API. Available at: https://www.alchemy.com/docs/reference/base-flashblocks-api-quickstart  
* \[93\] Base Documentation: Network Information and Block Building. Available at: https://docs.base.org/base-chain/network-information/block-building  
* \[97\] Google Cloud Documentation: VPC Service Controls for BigQuery. Available at: https://docs.cloud.google.com/bigquery/docs/vpc-sc  
* \[98\] OneUptime Blog: Cloud Functions and VPC Service Perimeters. Available at: https://oneuptime.com/blog/post/2026-02-17-how-to-allow-cloud-functions-to-access-resources-inside-a-vpc-service-perimeter/view  
* \[99\] Google Cloud Documentation: VPC Service Controls Overview. Available at: https://docs.cloud.google.com/vpc-service-controls/docs/overview  
* \[106\] The Cloud Side Blog: Mage.ai Streaming Data Loaders. Available at: https://blog.thecloudside.com/mage-ai-the-easy-way-to-automate-your-data-pipelines-1c8b01315eb4  
* \[107\] Towards Data Engineering: ETL Mage. Available at: https://medium.com/towardsdev/etl-mage-the-airflow-replacement-06f46c567248  
* \[109\] Mage.ai Documentation: Streaming Pipelines and Kafka. Available at: https://docs.mage.ai/guides/streaming/tutorials/streaming-pipeline  
* \[110\] Mage.ai Blog: 7 Essential Features for Data Engineers. Available at: https://m.mage.ai/7-essential-mage-features-for-data-engineers-in-2024-c01bfd73cab4  
* \[116\] Mage.ai Documentation: Developing dbt in Mage. Available at: https://docs.mage.ai/guides/dbt/developing-dbt-in-mage  
* \[120\] Mage.ai Blog: Make dbt Magic with Mage. Available at: https://www.mage.ai/blog/make-dbt-magic-with-mage  
* \[121\] Cloud Consulting Firms: Vertex AI Implementation Patterns and Pricing. Available at: https://cloudconsultingfirms.com/insights/vertex-ai-implementation-patterns/  
* \[122\] Roboflow Blog: Computer Vision Platforms Evaluation Matrix. Available at: https://blog.roboflow.com/best-computer-vision-platforms/

#### **Works cited**

1. Kafka streaming pipeline \- Mage AI, [https://docs.mage.ai/guides/streaming/tutorials/streaming-pipeline](https://docs.mage.ai/guides/streaming/tutorials/streaming-pipeline)  
2. Stateful Streaming Pipeline \- Mage AI, [https://docs.mage.ai/guides/streaming/tutorials/streaming-stateful-store](https://docs.mage.ai/guides/streaming/tutorials/streaming-stateful-store)  
3. Welcome to Mage \- Mage, [https://mage-ai-mage-ai.mintlify.app/introduction](https://mage-ai-mage-ai.mintlify.app/introduction)  
4. ETL Mage Ai, the Airflow replacement | by Abdelbarre Chafik | Towards Dev \- Medium, [https://medium.com/towardsdev/etl-mage-the-airflow-replacement-06f46c567248](https://medium.com/towardsdev/etl-mage-the-airflow-replacement-06f46c567248)  
5. Data loader utilities \- Mage AI, [https://docs.mage.ai/design/data-loading](https://docs.mage.ai/design/data-loading)  
6. Mage.ai: The Easy Way to Automate Your Data Pipelines \- The Cloudside View, [https://blog.thecloudside.com/mage-ai-the-easy-way-to-automate-your-data-pipelines-1c8b01315eb4](https://blog.thecloudside.com/mage-ai-the-easy-way-to-automate-your-data-pipelines-1c8b01315eb4)  
7. Maximum concurrent requests for services | Cloud Run \- Google Cloud Documentation, [https://docs.cloud.google.com/run/docs/about-concurrency](https://docs.cloud.google.com/run/docs/about-concurrency)  
8. Cloud Run Quotas and Limits \- Google Cloud Documentation, [https://docs.cloud.google.com/run/quotas](https://docs.cloud.google.com/run/quotas)  
9. GCP Cloud Run executor \- Mage Pro, [https://docs.mage.ai/production/executors/gcp](https://docs.mage.ai/production/executors/gcp)  
10. Configure CPU limits for jobs | Cloud Run \- Google Cloud Documentation, [https://docs.cloud.google.com/run/docs/configuring/jobs/cpu](https://docs.cloud.google.com/run/docs/configuring/jobs/cpu)  
11. Working with JSON data in GoogleSQL | BigQuery \- Google Cloud Documentation, [https://docs.cloud.google.com/bigquery/docs/json-data](https://docs.cloud.google.com/bigquery/docs/json-data)  
12. How BigQuery powers semi-structured data storage | Google Cloud Blog, [https://cloud.google.com/blog/products/databases/how-bigquery-powers-semi-structured-data-storage](https://cloud.google.com/blog/products/databases/how-bigquery-powers-semi-structured-data-storage)  
13. BigQuery subscriptions | Pub/Sub \- Google Cloud Documentation, [https://docs.cloud.google.com/pubsub/docs/bigquery](https://docs.cloud.google.com/pubsub/docs/bigquery)  
14. How to Read from Pub/Sub and Write to BigQuery in a Streaming Dataflow Pipeline, [https://oneuptime.com/blog/post/2026-02-17-how-to-read-from-pubsub-and-write-to-bigquery-in-a-streaming-dataflow-pipeline/view](https://oneuptime.com/blog/post/2026-02-17-how-to-read-from-pubsub-and-write-to-bigquery-in-a-streaming-dataflow-pipeline/view)  
15. How to Configure Cloud Run Request Timeout \- OneUptime, [https://oneuptime.com/blog/post/2026-02-17-how-to-configure-cloud-run-request-timeout-and-retry-policies-for-long-running-tasks/view](https://oneuptime.com/blog/post/2026-02-17-how-to-configure-cloud-run-request-timeout-and-retry-policies-for-long-running-tasks/view)  
16. Google Pub/Sub Subscription Concepts | by Kandaanusha \- Medium, [https://medium.com/@kandaanusha/google-pub-sub-subscription-concepts-cfed07648352](https://medium.com/@kandaanusha/google-pub-sub-subscription-concepts-cfed07648352)  
17. Deploy to GCP with Terraform \- Mage Pro, [https://docs.mage.ai/production/deploying-to-cloud/gcp/setup](https://docs.mage.ai/production/deploying-to-cloud/gcp/setup)  
18. GCP Secret Management \- Mage AI, [https://docs.mage.ai/production/deploying-to-cloud/secrets/GCP](https://docs.mage.ai/production/deploying-to-cloud/secrets/GCP)  
19. Git terminal with built-in authentication and shortcuts \- Mage AI, [https://docs.mage.ai/guides/data-sync/git-terminal](https://docs.mage.ai/guides/data-sync/git-terminal)  
20. Mage Pro Version Control, [https://docs.mage.ai/guides/data-sync/version-control-guide](https://docs.mage.ai/guides/data-sync/version-control-guide)  
21. Migrate from Mage OSS to Mage Pro, [https://docs.mage.ai/migrations/mage-oss-to-mage-pro](https://docs.mage.ai/migrations/mage-oss-to-mage-pro)  
22. Overview \- Mage AI, [https://docs.mage.ai/extensibility/api-reference/blocks/overview](https://docs.mage.ai/extensibility/api-reference/blocks/overview)  
23. Develop dbt in Mage, [https://docs.mage.ai/guides/dbt/developing-dbt-in-mage](https://docs.mage.ai/guides/dbt/developing-dbt-in-mage)  
24. Make dbt Magic with Mage – Mage AI Blog, [https://www.mage.ai/blog/make-dbt-magic-with-mage](https://www.mage.ai/blog/make-dbt-magic-with-mage)  
25. Best Data Pipeline Tools in 2026: Airflow vs Mage vs Prefect vs Dagster vs Bruin, [https://getbruin.com/blog/best-data-pipeline-tools-2026/](https://getbruin.com/blog/best-data-pipeline-tools-2026/)  
26. 5 Awesome Mage AI Alternatives \- Sliplane, [https://sliplane.io/blog/5-awesome-mage-ai-alternatives](https://sliplane.io/blog/5-awesome-mage-ai-alternatives)  
27. 7 essential Mage features for data engineers in 2024 | by Cole Freeman, [https://m.mage.ai/7-essential-mage-features-for-data-engineers-in-2024-c01bfd73cab4](https://m.mage.ai/7-essential-mage-features-for-data-engineers-in-2024-c01bfd73cab4)  
28. Introduction to the BigQuery Storage Write API \- Google Cloud Documentation, [https://docs.cloud.google.com/bigquery/docs/write-api](https://docs.cloud.google.com/bigquery/docs/write-api)  
29. Exactly-once delivery | Pub/Sub \- Google Cloud Documentation, [https://docs.cloud.google.com/pubsub/docs/exactly-once-delivery](https://docs.cloud.google.com/pubsub/docs/exactly-once-delivery)  
30. BigQuery | AI data platform | EDW \- Google Cloud, [https://cloud.google.com/bigquery](https://cloud.google.com/bigquery)  
31. Overview of VPC Service Controls \- Google Cloud Documentation, [https://docs.cloud.google.com/vpc-service-controls/docs/overview](https://docs.cloud.google.com/vpc-service-controls/docs/overview)  
32. How to Debug BigQuery DML Quota Exceeded Errors for High-Frequency Table Updates, [https://oneuptime.com/blog/post/2026-02-17-how-to-debug-bigquery-dml-quota-exceeded-errors-for-high-frequency-table-updates/view](https://oneuptime.com/blog/post/2026-02-17-how-to-debug-bigquery-dml-quota-exceeded-errors-for-high-frequency-table-updates/view)  
33. What's the cost and performance implications for BigQuery Native JSON data type?, [https://stackoverflow.com/questions/76305485/whats-the-cost-and-performance-implications-for-bigquery-native-json-data-type](https://stackoverflow.com/questions/76305485/whats-the-cost-and-performance-implications-for-bigquery-native-json-data-type)  
34. BiqQuery Cost Optimization 2025 \- BigQuery \- e6data, [https://www.e6data.com/query-and-cost-optimization-hub/how-to-optimize-bigquery-costs](https://www.e6data.com/query-and-cost-optimization-hub/how-to-optimize-bigquery-costs)  
35. BigQuery | Google Cloud, [https://cloud.google.com/bigquery/pricing](https://cloud.google.com/bigquery/pricing)  
36. Configure CPU limits for services | Cloud Run \- Google Cloud Documentation, [https://docs.cloud.google.com/run/docs/configuring/services/cpu](https://docs.cloud.google.com/run/docs/configuring/services/cpu)  
37. Mage's built-in secret manager, [https://docs.mage.ai/production/deploying-to-cloud/secrets/mage](https://docs.mage.ai/production/deploying-to-cloud/secrets/mage)  
38. How to get a Base RPC endpoint for DeFi (2026 tutorial) \- Chainstack, [https://chainstack.com/learn/how-to/how-to-get-base-rpc-endpoint-for-defi-2026/](https://chainstack.com/learn/how-to/how-to-get-base-rpc-endpoint-for-defi-2026/)  
39. Base Flashblocks API quickstart | Alchemy Docs, [https://www.alchemy.com/docs/reference/base-flashblocks-api-quickstart](https://www.alchemy.com/docs/reference/base-flashblocks-api-quickstart)  
40. Block Building \- Base documentation, [https://docs.base.org/base-chain/network-information/block-building](https://docs.base.org/base-chain/network-information/block-building)  
41. VPC Service Controls for BigQuery \- Google Cloud Documentation, [https://docs.cloud.google.com/bigquery/docs/vpc-sc](https://docs.cloud.google.com/bigquery/docs/vpc-sc)  
42. How to Allow Cloud Functions to Access Resources Inside a VPC Service Perimeter, [https://oneuptime.com/blog/post/2026-02-17-how-to-allow-cloud-functions-to-access-resources-inside-a-vpc-service-perimeter/view](https://oneuptime.com/blog/post/2026-02-17-how-to-allow-cloud-functions-to-access-resources-inside-a-vpc-service-perimeter/view)  
43. Migrate from Prefect to Mage Pro, [https://docs.mage.ai/migrations/prefect-to-mage-pro](https://docs.mage.ai/migrations/prefect-to-mage-pro)  
44. Orchestration Tools: Choose the Right Tool for the Job \- Prefect, [https://www.prefect.io/blog/orchestration-tools-choose-the-right-tool-for-the-job](https://www.prefect.io/blog/orchestration-tools-choose-the-right-tool-for-the-job)  
45. Top 5 Mage.ai Alternatives & Competitors (2026) \- Data \- Kestra, [https://kestra.io/resources/data/mage-alternatives](https://kestra.io/resources/data/mage-alternatives)  
46. Dagster vs. Kestra: key differences 2024 \- Orchestra, [https://www.getorchestra.io/guides/dagster-vs-kestra-key-differences-2024](https://www.getorchestra.io/guides/dagster-vs-kestra-key-differences-2024)  
47. Kestra vs. Temporal: Orchestration for Every Team, Not Just Every Engineer, [https://kestra.io/vs/temporal](https://kestra.io/vs/temporal)  
48. Dagster vs Kestra for Data Pipeline Orchestration, [https://kestra.io/vs/dagster](https://kestra.io/vs/dagster)  
49. Introduction | Feast: the Open Source Feature Store, [https://docs.feast.dev/](https://docs.feast.dev/)  
50. Vertex AI in Production: What Actually Ships in 90 Days (and What Doesn't) \- Cloud Intel, [https://cloudconsultingfirms.com/insights/vertex-ai-implementation-patterns/](https://cloudconsultingfirms.com/insights/vertex-ai-implementation-patterns/)  
51. Best Computer Vision Platforms 2026 \- Roboflow Blog, [https://blog.roboflow.com/best-computer-vision-platforms/](https://blog.roboflow.com/best-computer-vision-platforms/)