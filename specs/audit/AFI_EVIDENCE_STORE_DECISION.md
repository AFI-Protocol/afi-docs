# AFI Evidence Store — Decision Record

**Status:** DECIDED · **Date:** 2026-06 · **Scope:** AFI reference implementation (testnet T2 MVP and forward)

## Decision

**MongoDB TSSD is the canonical reference evidence store for AFI.** The single working
ingest → score → persist spine is:

```
POST /api/webhooks/tradingview
  → afi-reactor (froggyDemoService → runPipelineDag → afi-core UWR score)
  → tssdVaultService.insertSignalDocument → Mongo afi_reactor.reactor_scored_signals_v1
```

For multi-tenant ingest, `afi-gateway` persists via `afi-infra`'s
`MongoTSSDVaultClient` (native Mongo time-series collection `afi_tssd.tssd_signals`).

Minimum to run: set `AFI_MONGO_URI` and `npm run build && npm run start:demo`. No other
data plane is required at any tier.

## What was retracted

An earlier round of planning docs proposed a separate **warehouse/streaming evidence plane**
(a cloud message-bus → external scoring DAG → append-only warehouse) and framed Mongo +
`afi-reactor` as a "legacy/deprecated" spine. **That detour was never implemented** — there is
zero cloud-warehouse client dependency, zero external scoring pipeline, zero message-bus
publisher, and zero warehouse DDL in any runtime repo. It is **retracted**. The associated
planning docs were deleted and all operational/audit docs were rewritten to the single
Mongo + reactor spine (2026-06).

This file is the one place that records the retraction. The forensic audit corpus
(`recon/`, `themes/`, `verified.json`) and the synthesis reports no longer reference the
retracted warehouse/streaming detour; they state Mongo TSSD as the implemented evidence store.

## Non-normative note

The portable-protocol spec ([`AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md`](../AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md))
keeps warehouse/stream engines listed **only** as hypothetical
*other-operator* implementations of the optional Market/analytics plane — never as AFI's
chosen evidence store, and never implying Mongo is deprecated. AFI's reference evidence
plane is, and remains, MongoDB TSSD.

## Related

- [`AFI_MONGO_TSSD_INVENTORY.md`](./AFI_MONGO_TSSD_INVENTORY.md) — code-level inventory of the Mongo/TSSD spine
- [`AFI_TESTNET_E2E_CHECKLIST.md`](./AFI_TESTNET_E2E_CHECKLIST.md) — testnet build checklist (Mongo + reactor spine)
