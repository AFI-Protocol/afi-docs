# AFI Docs Inventory (Human Summary)

Source: filesystem scan of `/Users/secretservice/AFI_Modular_Repos` (see machine-readable `AFI_Docs_Inventory.json`).

## Repos covered
ElizaOS_Ext_Ref, Spartan_reference, _archived, afi-artifacts, afi-assets, afi-benchkit, afi-config, afi-core, afi-docs, afi-econ, afi-gateway, afi-factory, afi-governance, afi-infra, afi-labs, afi-math, afi-mint, afi-ops, afi-plugins, afi-protocol, afi-reactor, afi-research-site, afi-sdk-python, afi-sdk-ts, afi-skills, afi-starters, afi-tiny-brains, afi-token, augmentcode_rules, scripts.

## Key documentation-rich repos
- **afi-config**: USS schemas (`schemas/usignal/v1_1/*.json`), examples (`examples/`), templates. Anchor for schema docs.
- **afi-reactor**: HTTP server (`src/server.ts`), TradingView→USS v1.1 mapper/validator (`src/uss/*`), DAG config (`src/config/froggyPipeline.ts`), vault persistence (`src/services/tssdVaultService.ts`). Primary pipeline docs.
- **afi-gateway**: Eliza agent runtime (`src/server-full.ts`, `src/index.ts`), AFI Reactor Actions plugin (`plugins/afi-reactor-actions`), OpenAI models plugin (`plugins/afi-openai-models`), .env.example for gateway envs.
- **afi-core**: Core logic (validators/analysis), docs/ present.
- **afi-math / afi-econ / afi-benchkit**: Research/eval primitives; math/econ libs and benchmarking toolkit.
- **afi-token / afi-mint / afi-labs**: Token/minting/solidity-focused code.
- **afi-docs**: Documentation site source.

## Env vars detected (via .env.example)
- **afi-reactor**: AFI_REACTOR_PORT, AFI_MONGO_URI, AFI_PRICE_FEED_SOURCE, TELEGRAM/MTProto settings, NEWS* settings, dedupe knobs, etc. (see `afi-reactor/.env.example`).
- **afi-gateway**: OPENAI_API_KEY, AFI_REACTOR_BASE_URL, MONGODB_URI, AFI_MONGO_DB_NAME, NODE_ENV (`afi-gateway/.env.example`).
- **afi-ops**: AFI_ENV, DB_URI, AGENT_KEY (`afi-ops/.env.example`).
- **afi-research-site**: NEXT_PUBLIC_SUPABASE_*, STRIPE_*, SENDGRID_API_KEY, POSTHOG (`afi-research-site/.env.example`).
- **afi-token**: BASE_SEPOLIA_RPC_URL, PRIVATE_KEY_TESTNET/LOCAL, ETHERSCAN_API_KEY (`afi-token/.env.example`).

## Endpoints extracted
- **afi-reactor/src/server.ts**: `/api/webhooks/tradingview`, `/api/ingest/cpj`, `/demo/afi-eliza-demo`, `/health`, `/replay/signal/:signalId`.
- **afi-gateway/src/server.ts & src/server-full.ts**: `/healthz`, `/demo/ping`, `/`, `/api/afi/info`, `/api/agents`, `/api/agents/:id/message`.

## Pipelines / stages / plugins
- **afi-reactor** (scored-only, 6 stages): `FROGGY_TREND_PULLBACK_PIPELINE` stages — uss-telemetry-deriver; froggy-enrichment-tech-pattern; froggy-enrichment-sentiment-news; froggy-enrichment-adapter; froggy-analyst; tssd-vault-write (`src/config/froggyPipeline.ts`). Validator certification and execution are external concerns, not pipeline stages.

## NPM scripts (highlights)
- **afi-reactor**: build, start:demo, demo:mock, simulate/replay, validate-all, verify:tssd:blofin, test suites.
- **afi-gateway**: dev modes (CLI/server/full), start, tests (afi-reactor-actions, mongo), telemetry offline, afiscout smoke.
- **afi-config**: build, validate, test, typecheck.
- **afi-core**: build, test, typecheck, esm:check.
- **afi-math / afi-plugins / afi-infra / afi-mint / afi-governance / afi-factory / afi-assets / afi-artifacts / afi-starters / afi-token / afi-sdk-ts**: build/test/typecheck variants.
- **afi-econ**: build, dev, cli, test, clean.
- **afi-research-site**: dev/web/agent, build, analyze, backfill.
- **afi-ops**: build, test, lint, deploy:local, health/status checks.
- **afi-skills**: build:manifest, lint:skills, test.

## Schemas
- USS v1.1 schemas in `afi-config/schemas/usignal/v1_1/index.schema.json` and `core.schema.json`.

## Benchmarks / research
- **afi-benchkit**: Python bench/eval toolkit (details pending deep dive).
- **afi-math**: Math primitives library (Node/TS).
- **afi-econ**: Econ models/tooling (Node/Python mix).

## Gaps / next extraction steps
- Contracts and tokenomics mechanics need extraction from `afi-token`, `afi-mint`, `afi-labs`.
- CLI commands and endpoint catalogs beyond reactor/gateway remain to be mined.
- Diagrams/assets locations not yet enumerated.
- Governance/ops deployment flows need structured docs.
