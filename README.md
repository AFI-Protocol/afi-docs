# AFI Protocol Documentation 📚

Welcome to the **canonical knowledge-base** for the Agentic Financial Intelligence Protocol (AFI).  
This repo aggregates **all public documentation**:  

| Section | Purpose |
|---------|---------|
| **`/specs`** | Formal specifications – schemas, consensus rules, mentor protocol, PoI logic |
| **`/guides`** | How-to & operational docs – local setup, CI/CD, Factory droid recipes (coming soon) |
| **`/lore`** | Narrative “signal logs” that dramatize real protocol flows & mentor interactions |

> **Why the mix?**  
> AFI is equal parts **engineering** and **agentic narrative**. Specs tell you “how”, lore shows you “why” in context.

---

## 1 · Quick Links
| • | Doc | When to read |
|---|-----|--------------|
| 🧬 **Mentor Protocol** | [`specs/mentor_protocol.md`](specs/mentor_protocol.md) | You’re building mentor logic or recovery hooks |
| 💻 **Codex Scaffold** | [`afi-codex`](afi-codex/) & [`afi.config.json`](afi.config.json) | You need the global type/registry map |
| ✨ **Lore Episodes** | [`/lore`](lore/) | You want an executable story of mentors, signals & anomalies |

---

## 2 · Getting Started
```bash
git clone https://github.com/AFI-Protocol/afi-docs.git
cd afi-docs
npm i gitbook-cli -g         # optional: local GitBook preview
gitbook serve
