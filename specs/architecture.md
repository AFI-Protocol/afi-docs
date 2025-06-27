# 🧠 AFI Protocol Architecture

The Agentic Financial Intelligence (AFI) Protocol is designed as a modular, multi-agent system that enables scalable validation, scoring, and storage of financial signals. The architecture prioritizes transparency, modularity, and agent autonomy through a combination of human-deployable logic and droid-enhanced infrastructure.

---

## 🔗 Core Components

### 1. **AFI Codex**
A shared type and ruleset registry that defines all schemas and signal definitions. It ensures agents and validators speak a common language.

### 2. **Mentor Agents**
Validator logic units responsible for ingesting, analyzing, and scoring market signals. These can be human-coded or droid-generated.

### 3. **Modal**
A pre-production agent training environment. Agents must demonstrate sufficient intelligence (Proof-of-Intelligence) to graduate and participate in the live network via Proof-of-Insight.

### 4. **AFI Token**
The economic layer. Tokens are minted dynamically when agents submit validated, high-confidence insight based on our evolving standards.

### 5. **Time-Series Signal Data Vault (T.S.S.D.)**
A decentralized signal archive. Only signals that surpass scoring thresholds and community review are stored here.

### 6. **Factory.ai & Augmentcode**
Agentic CI/CD. These systems automate module generation, documentation, and deployment pipelines using AFI-specific GitHub heuristics.

---

## ⚙️ Repo Structure Overview

- `afi-core`: Base logic for validation and scoring.
- `afi-docs`: Documentation, GitBook, and lore.
- `afi-infra`: Infrastructure, cloud, and compute configuration.
- `afi-agents`: Home of AI-driven agents (including droids).
- `afi-factory`: CI/CD automation logic and recipes.
- `afi-config`: Global schemas and `afi.config.json` defaults.
- `afi-labs`: Experiments, previews, and developer sandbox.

---

## 🧬 Consensus Flow

1. Agents ingest signals (on-chain, TradingView, manual).
2. Scoring logic is applied based on schemas and codex rules.
3. Signals above a threshold are committed to the vault.
4. Proof-of-Insight confirms their legitimacy.
5. AFI tokens are minted and distributed to validators.

---

## 🛡️ Governance

AFI uses an evolving DAO model. All validator logic, tokenomics, and vault criteria are community-governed, while autonomous agents operate within these bounds using on-chain reputation and staking.

---

*Built with care, curiosity, and conviction.*