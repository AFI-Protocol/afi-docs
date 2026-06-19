# Mage Pro vs OSS — Plan & Deployment Decision (AFI Testnet)

**Date:** 2026-06-03 (updated)  
**Scope:** Phase A testnet (T2 gate) — Pub/Sub → Mage streaming → BQ → `afi-mint` → Base Sepolia  
**Pricing source:** [Mage Pro pricing](https://www.mage.ai/pricing) (verify before purchase)

**Parent:** [`AFI_TESTNET_E2E_CHECKLIST.md`](./AFI_TESTNET_E2E_CHECKLIST.md) §1.0

---

## Context (read this first)

**AFI does not have Mage infrastructure today.** No Mage Terraform, Docker, or GCP deploy exists in this monorepo yet.

**Transferable experience (unrelated projects):** Commission-based sales tracking / auditing ETL·ELT pipelines built with **Mage OSS + Terraform + Docker + GCP + BigQuery**. That stack is proven elsewhere — it is **not** wired to AFI repos, Pub/Sub signal topics, or `afi-mint`.

**We are on the same page if:**

| Statement | True for AFI? |
|-----------|---------------|
| Mage/GCP/BQ ops skills transfer to AFI | ✅ Yes |
| AFI Mage is already running | ❌ No — net-new deploy |
| ETL patterns (loader → transform → export) map to signal lifecycle | ✅ Yes — different payloads, same shape |
| AFI still needs custom blocks + `afi-mint` + on-chain | ✅ Yes — Mage is scoring orchestration only |

**Default recommendation:** **Mage OSS self-hosted on GCP** — reuse your Terraform/Docker playbook, adapt for AFI's Pub/Sub streaming + evidence schema. Skip Pro unless you hit the fallback triggers below.

---

## Executive recommendation

| Phase | Default | Monthly platform | Deployment |
|-------|---------|------------------|------------|
| **Testnet MVP (T2)** | **Mage OSS** | **~$20–80 GCP only** | Terraform + Docker in **new** `afi-testnet` GCP project |
| **Fallback** | Mage Pro Team | $500/mo + GCP | Hybrid GCP — if no bandwidth for self-host ops |
| **Pilot analysts** | OSS or Plus | varies | Add GCE/GKE or second cluster when needed |
| **Marketplace scale** | Re-evaluate | — | Defer |

**Do not use fully managed Mage SaaS** for signal payloads — data should stay in your GCP project.

---

## What carries over from your ETL projects vs what's net-new

### Reuse directly (skills + patterns)

- Mage OSS Terraform GCP deploy ([docs](https://docs.mage.ai/production/deploying-to-cloud/gcp/setup))
- Docker image (`mageai/mageai`) + `io_config.yaml` for BigQuery credentials
- Loader → Transformer → Exporter block structure
- GCP IAM, Secret Manager, service accounts
- BigQuery append/load patterns (adapt table schema)

### Net-new for AFI (not in sales ETL)

| Item | Why different |
|------|---------------|
| Pub/Sub **streaming** consumer (`signal-raw`) | Sales ETL is usually batch/cron; AFI needs event-driven scoring |
| Topics `signal-raw` / `signal-scored` / `signal-minted` | Protocol workflow bus — not warehouse-only |
| USS/CPJ validation blocks | `afi-config` schemas, not sales commission schemas |
| UWR scoring block or `afi-reactor` HTTP sidecar | Protocol math, not commission rules |
| Determinism metadata (`pipeline_uuid`, `git_sha`, ruleset version) | Replay/challenge requirement |
| `afi-mint` Pub/Sub push → Base Sepolia | Commitment plane — outside Mage entirely |
| Evidence table `afi_evidence.signals_lifecycle` | Append-only lifecycle log, not dimensional sales facts |

**Same infra muscle, different pipeline content.** Confidence to self-host OSS is warranted; the work is AFI-specific blocks and wiring, not learning Mage from zero.

---

## OSS deployment topology for AFI

Do **not** put the always-on streaming consumer on Cloud Run alone (request timeout).

| Component | Target | Notes |
|-----------|--------|-------|
| Mage UI + dev/batch | Cloud Run via Terraform | Same as your other projects |
| **Streaming scoring pipeline** | **GCE small instance or GKE** | Long-lived Pub/Sub consumer |
| Pub/Sub + BQ | Your `afi-testnet` project | Same region (`us-central1` recommended) |
| Ingest | `afi-gateway` or Cloud Run | Outside Mage |
| Mint | `afi-mint` Cloud Run | Outside Mage; push from `signal-scored` |

**Total testnet cost (OSS):** ~**$40–80/mo GCP** (Pub/Sub, BQ, Cloud Run, small GCE) — no Mage license.

---

## When to choose Pro instead of OSS

| Trigger | Action |
|---------|--------|
| No time to own Mage server/streaming uptime during T2 crunch | Pro Team + Hybrid |
| Streaming consumer keeps failing and you need vendor support | Pro + Basics support ($20k/yr) |
| Multi-tenant analyst workspaces at scale | Plus ($2k/mo) — post-T2 |
| Block-run/debug volume irrelevant on OSS | N/A — OSS has no block caps |

Pro does **not** remove AFI custom work (USS, UWR, mint handoff, chain adapter).

---

## Mage Pro plan reference (fallback only)

Use this section only if OSS self-host is rejected.

| Plan | Price | Block runs/mo | When |
|------|-------|---------------|------|
| Starter | $100 + compute | Metered | Authoring only — not testnet |
| **Team** | $500 | 15,000 | Light testnet via Hybrid |
| Plus | $2,000 | 50,000 | Dev + testnet clusters, pilot analysts |
| Business+ | $5,500+ | 200k+ | Defer |

Block-run estimate: ~6 blocks × signals/mo. Testnet dress rehearsal ≪ Team cap.

Hybrid/Private often require sales quote even on Team — see questions below if pursuing Pro.

---

## OSS checklist (default path)

| Done? | Task | Notes |
|-------|------|-------|
| [ ] | Create `afi-testnet` GCP project + region | Single region for Pub/Sub exactly-once |
| [ ] | Fork/adapt Mage Terraform from other project | [GCP setup guide](https://docs.mage.ai/production/deploying-to-cloud/gcp/setup) |
| [ ] | Deploy Mage UI (Cloud Run) | Dev + batch triggers |
| [ ] | Deploy streaming worker (GCE/GKE) | Pub/Sub consumer — **not** Cloud Run only |
| [ ] | Wire `io_config.yaml` → BQ + Pub/Sub SA | Secret Manager for credentials |
| [ ] | Create AFI streaming pipeline repo/folder | Blocks per §1.3 of E2E checklist |
| [ ] | Smoke test: publish to `signal-raw` → BQ SCORED row | Before `afi-mint` integration |

---

## Pro sales questions (fallback only)

1. Does Team include Hybrid GCP with always-on Pub/Sub streaming in our project?
2. Do empty streaming polls count as block runs?
3. Can blocks call external Cloud Run (`afi-reactor` sidecar)?

---

## Decision fields (fill when decided)

| Field | Your choice |
|-------|-------------|
| Platform | [ ] **OSS self-host**  [ ] Mage Pro Team  [ ] Plus |
| Prior Mage/GCP experience | [ ] Transferable from other ETL projects  [ ] None |
| AFI Mage deployed | [ ] No (net-new)  [ ] Yes |
| Streaming worker | [ ] GCE  [ ] GKE  [ ] TBD |
| GCP project | e.g. `afi-testnet` / `us-central1` |
| Pro quote (if fallback) | [ ] N/A  [ ] Received |

---

## Upgrade path

| Milestone | Action |
|-----------|--------|
| T2 gate passed on OSS | Stay on OSS |
| Pilot analysts + ops load | Add GCE capacity or second env |
| No ops bandwidth | Evaluate Pro Team |
| Analyst marketplace | Pro Plus/Business or multi-instance OSS |

---

*Companion: [`Mage And GCP Architecture Research.md`](../../../Mage%20And%20GCP%20Architecture%20Research.md) · [`AFI_ANALYST_SHOP_MVP.md`](../AFI_ANALYST_SHOP_MVP.md)*
