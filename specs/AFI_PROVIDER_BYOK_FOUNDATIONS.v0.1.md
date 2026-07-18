# AFI Provider Adapter and BYOK Foundations v0.1

**Status:** Current specification of the implemented provider-neutral adapter socket and secure bring-your-own-key (BYOK) credential boundary. Governed by `afi-governance/decisions/provider-byok-foundations-v0.1.md` (PBF-GOV). Documents the Wave-1 foundation delivered across `afi-config`, `afi-factory`, and `afi-reactor` on the existing configurable executor and Evidence V2.

This foundation establishes the provider **socket** and the credential **boundary**. It does not complete all commercial provider integrations, and it deploys nothing.

## 1. Five provider-open categories, one resolved result each

AFI has exactly five analysis categories — `technical`, `pattern`, `sentiment`, `news`, `aiMl` (governed namespace; casing `aiMl` exact). Each is an **open capability lane**: a category is not a vendor, not one hardcoded service, not one required algorithm, and not an ensemble. An analyst may select a conforming implementation or provider for each category.

The scorer-facing pipeline consumes **at most one resolved result per category**. A provider may internally aggregate many articles, sources, indicators, or models, but AFI treats one provider invocation as one category implementation producing one category result at the pipeline boundary. The deterministic one-per-category join is unchanged; there is no generic ensemble.

## 2. Three non-secret canonical objects

Three first-class objects (governed by afi-config) model the provider socket. All are non-secret.

- **Provider** (`afi.provider.v1`) — a stable, non-secret identity for a source of an analytical capability (local implementation, open-source library, external API, data vendor, hosted inference service, local model runtime, proprietary service, or Tiny Brains). It carries id, record version, display name, supported categories, execution class (`local`/`remote`), deterministic posture, the trusted registered adapter that implements it, and — only when a capability requires one — the credential **kind** (never a value). Registry presence means available to the relevant deployment, not an endorsement.
- **CredentialRef** (`afi.credential-ref.v1`) — an opaque, non-secret **pointer** to a credential (id, tenant/owner scope, provider compatibility, credential kind, active/disabled state). It contains no API key, token, password, private key, authorization header, or any secret payload. The actual secret lives in a deployment secret backend keyed by `(tenant, credentialRef)`; rotation and revocation happen behind the reference.
- **ProviderInstance** (`afi.provider-instance.v1`) — a tenant/operator-scoped, non-secret configuration binding one provider to one registered adapter for exactly one category. It is version-pinned for deterministic composition, optionally references one compatible CredentialRef (by opaque id), and carries only non-secret invocation settings. It contains no credential value, no arbitrary code, and no analyst-supplied remote endpoint (a named `endpointProfile` only — anti-SSRF).

The existing **plugin/adapter** identity remains the executable boundary: `Category` is the semantic lane, `Plugin/adapter` is the trusted registered implementation, `Provider` is the source, `ProviderInstance` is this tenant's configured use, `CredentialRef` is the non-secret pointer.

## 3. Factory authoring

`afi-factory` authors and validates provider-backed category nodes across all five surfaces (SDK, CLI, capability catalog, framework-neutral tool definitions, MCP stdio adapter). A category node may carry an optional, versioned, non-secret `providerInstanceRef` (identity + version only). Factory validates the reference shape, enforces that it appears only on the five analysis-category nodes (not merge/scorer), preserves it in the artifact, includes it in canonical hashing, and exposes it through inspection. Factory **cannot** resolve credentials, call a provider, inspect a secret backend, or print a secret; artifacts, CLI output, and MCP output contain no credential.

## 4. Reactor execution and the SecretResolver boundary

`afi-reactor` runs one bounded provider-adapter layer inside the Reactor, below the category node. It is not a second executor; the `GraphExecutor` and the scorer-facing join are unchanged. For a provider-backed node the runtime:

1. resolves the non-secret ProviderInstance record;
2. validates tenant/operator scope and provider/category/adapter compatibility;
3. resolves **only** the authorized credential (when required) through an injected least-privilege `SecretResolver`;
4. invokes the trusted registered adapter with a bounded credential bundle and a scrubbing logger;
5. validates the returned category result against its canonical `afi.enrichment.<category>.v1` contract before scoring.

Every boundary fails closed. The **SecretResolver** resolves only the exact authorized `(tenant, credentialRef)`; it cannot list secrets, resolve arbitrary references, read another tenant's credential, discover backend paths, or write/delete/rotate. The adapter receives only a bounded credential bundle — never a resolver or a secret-management client. Adapters are compiled, explicitly registered, versioned, and validated at boot (a duplicate or unknown adapter fails closed); there is no dynamic import, arbitrary module path, or remote code loading.

**Two reference proofs:** a **keyless technical** adapter (reuses the exact production kernels; the resolver is never invoked) and a **credentialed news** adapter (BYOK; the key rides in a request header, never a URL; a deterministic transport proves it without a live paid key).

## 5. Security invariant

> **AFI pipeline artifacts identify provider configurations but never contain provider credentials.**

Secret resolution occurs only at runtime, at the adapter edge. Factory cannot resolve secrets. Adapters receive only scoped credentials. Logs, errors, traces, canonical hashes, and Evidence exclude credentials (structural closure plus a redaction boundary). Deployment-specific secret backends (for example GCP Secret Manager) are pending a later staging wave; this foundation provisions none.

## 6. Evidence V2 freeze

Evidence V2 (`afi.scored-signal-evidence.v2`) is unchanged: schema, semantics, canonical Mongo record shape, store version pin, and lifecycle status are all identical. The versioned pipeline composition may commit to a non-secret ProviderInstance reference through its existing artifact hash, but no provider credential, provider-invocation object, or new collection is persisted. Detailed provider/model **invocation provenance** is deferred to a later governed evidence decision that will determine Evidence V3 after real adapters reveal the true provenance fields. Evidence V2 does not contain provider-invocation provenance.

## 7. Scoring, UWR, Tiny Brains

Provider-backed enrichment is input to the existing scorer, never a replacement. Category weighting, scorer logic, UWR, Core, and Math authority are unchanged; equivalent category outputs produce identical scores.

Tiny Brains enriches the `aiMl` category and may **later** orchestrate several internal models plus a critic/meta-model, emitting exactly one resolved `aiMl` result:

```
Tiny Brains may later use internal model orchestration
  → emits one aiMl category result
  → canonical AFI scoring remains authoritative
```

Its internal orchestration is not an AFI-level ensemble and never creates duplicate `aiMl` results. This foundation implements no Tiny Brains ensemble and no generic ensemble contract; Tiny Brains does not become a scorer and does not alter UWR.

## 8. Independent operators and the Institute

Independent parties may author and operate conforming providers and adapters; a conforming implementation is not invalid because AFI did not author it. Adding a conforming provider, adapter, credential reference, or provider instance is an administrative registry or deployment update, not per-participant governance. AFI Research Institute may operate reference adapters, but that role is non-exclusive and confers no protocol authority (INST-GOV); no Institute adapter is deployed or privileged here.

## 9. Non-deployment status

This foundation deploys nothing. No provider, adapter, or service is deployed; no GCP resource, Secret Manager resource, IAM, or service account is provisioned; no runtime agent operates providers; no generic ensemble exists; no commercial provider integration beyond the two reference proofs is claimed.
