#!/usr/bin/env python3
"""
Generate Phase 1 draft markdown reports from AFI_RECON_CORPUS.json.

Usage:
  python3 generate_drafts.py [--corpus PATH]
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
AUDIT_DIR = SCRIPT_DIR.parent
CORPUS_DEFAULT = AUDIT_DIR / "recon" / "AFI_RECON_CORPUS.json"
RECON_DIR = AUDIT_DIR / "recon"
DRAFTS_DIR = AUDIT_DIR / "drafts"

SPINE = {
    "Ingest boundary": ["afi-gateway"],
    "Scoring DAG": ["afi-reactor", "afi-core", "afi-plugins", "afi-tiny-brains"],
    "Evidence vault": ["afi-infra"],
    "Mint coordination": ["afi-mint"],
    "On-chain commitment": ["afi-token"],
    "Normative schemas/types": ["afi-config", "afi-infra"],
}

TENSION_KEYWORDS = {
    "Mongo-only": re.compile(r"mongo|tssd|vault", re.I),
    "reactor-only": re.compile(r"reactor|orchestrator|doctrine|DAG is law", re.I),
    "BASE-ledger": re.compile(r"on-?chain|base|receipt|breadcrumb|ledger|commitment", re.I),
    "econ-splits": re.compile(r"split|gauge|beneficiary|payout|60/30|55/25", re.I),
    "mint-model": re.compile(r"mint|epoch|per-signal|batch|coordinateMint", re.I),
    "stale-arch-docs": re.compile(r"stale|afi-pipeline|archived|repository.?map", re.I),
}

MANDATORY_STACK = re.compile(r"mongo|reactor|org infra|mandatory|only orchestrator|afi-reactor", re.I)


def load_corpus(path: Path) -> tuple[dict, list[dict]]:
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    return data.get("metadata", {}), data.get("records", data if isinstance(data, list) else [])


def tag_tension(title: str, detail: str) -> str:
    text = f"{title} {detail}"
    for tag, pat in TENSION_KEYWORDS.items():
        if pat.search(text):
            return tag
    return "other"


def generate_summary(metadata: dict, records: list[dict]) -> str:
    classifications = Counter(r.get("classification") for r in records)
    replay = Counter(r.get("replay_relevance") for r in records)

    p01: list[tuple[str, dict]] = []
    for r in records:
        repo = str(r.get("repo", ""))
        for n in r.get("notable_findings") or []:
            if n.get("severity") in ("P0", "P1"):
                p01.append((repo, n))

    lines = [
        "# AFI Recon Summary (Phase 1)",
        "",
        "**Status:** DRAFT — Phase 1 recon complete; themes and verification pending",
        f"**Extracted:** {metadata.get('extracted_at', 'unknown')}",
        f"**Source workflow:** `{metadata.get('source_workflow_id', 'unknown')}`",
        f"**Repos audited:** {metadata.get('repo_count', len(records))}",
        "",
        "Companion: [`AFI_RECON_CORPUS.json`](./AFI_RECON_CORPUS.json) | Checkpoint: [`../AFI_AUDIT_CHECKPOINT.md`](../AFI_AUDIT_CHECKPOINT.md)",
        "",
        "---",
        "",
        "## Classification Snapshot",
        "",
        "| Classification | Count |",
        "|----------------|-------|",
    ]
    order = ["NORMATIVE", "REFERENCE_IMPL", "SUPPORTING", "RESEARCH", "DOCS", "STALE", "OUT_OF_SCOPE"]
    for cls in order:
        if classifications.get(cls):
            lines.append(f"| {cls} | {classifications[cls]} |")

    lines.extend([
        "",
        "## Replay Relevance",
        "",
        "| Level | Count |",
        "|-------|-------|",
    ])
    for level in ["critical", "partial", "none"]:
        if replay.get(level):
            lines.append(f"| {level} | {replay[level]} |")

    lines.extend([
        "",
        "## Reference Spine",
        "",
        "| Segment | Repo(s) |",
        "|---------|---------|",
    ])
    for segment, repos in SPINE.items():
        lines.append(f"| {segment} | {', '.join(f'`{r}`' for r in repos)} |")

    lines.extend([
        "",
        "## Full Classification Table",
        "",
        "| Repo | Classification | Replay | Purpose (abbrev.) |",
        "|------|----------------|--------|-------------------|",
    ])
    for r in records:
        repo = r.get("repo", "")
        purpose = (r.get("primary_purpose") or "")[:80].replace("|", "/")
        if len((r.get("primary_purpose") or "")) > 80:
            purpose += "…"
        lines.append(
            f"| `{repo}` | {r.get('classification', '')} | {r.get('replay_relevance', '')} | {purpose} |"
        )

    lines.extend([
        "",
        "## P0/P1 Notable Findings (Unverified)",
        "",
    ])
    for repo, n in p01:
        lines.append(f"- **[{n.get('severity')}] `{repo}`** — {n.get('title')}")
        if n.get("evidence"):
            lines.append(f"  - Evidence: `{n.get('evidence')}`")

    lines.append("")
    return "\n".join(lines)


def generate_refimpl_map(records: list[dict]) -> str:
    lines = [
        "# AFI Reference Implementation Map",
        "",
        "**Status:** DRAFT — Phase 1 recon only; themes unverified",
        "**Date:** 2026-06-15",
        "",
        "Promote to [`afi-docs/specs/AFI_REFERENCE_IMPL_MAP.md`](../../AFI_REFERENCE_IMPL_MAP.md) after Phase 3 verification.",
        "",
        "Source: [`recon/AFI_RECON_CORPUS.json`](../recon/AFI_RECON_CORPUS.json)",
        "",
        "---",
        "",
        "## Reference Spine",
        "",
        "```",
        "ingest (afi-gateway)",
        "  -> scoring DAG (afi-reactor + afi-core + afi-plugins + afi-tiny-brains)",
        "  -> evidence vault (afi-infra)",
        "  -> mint coordination (afi-mint)",
        "  -> on-chain commitment (afi-token)",
        "",
        "normative surface: afi-config + afi-infra (TSSD types/spec)",
        "```",
        "",
        "| Segment | Repo(s) | Classification |",
        "|---------|---------|----------------|",
    ]
    repo_by_name = {r.get("repo"): r for r in records}
    for segment, repos in SPINE.items():
        for repo in repos:
            r = repo_by_name.get(repo, {})
            lines.append(f"| {segment} | `{repo}` | {r.get('classification', '—')} |")

    lines.extend([
        "",
        "## 31-Repo Classification Table",
        "",
        "| Repo | Visibility | Classification | Replay | Recommended action |",
        "|------|------------|----------------|--------|----------------------|",
    ])
    for r in records:
        lines.append(
            f"| `{r.get('repo', '')}` | {r.get('visibility', '—')} | "
            f"{r.get('classification', '')} | {r.get('replay_relevance', '')} | "
            f"{(r.get('recommended_action') or 'none')[:60]} |"
        )

    lines.extend([
        "",
        "## Per-Repo Blocks",
        "",
    ])
    for r in records:
        repo = r.get("repo", "")
        lines.append(f"### `{repo}`")
        lines.append("")
        lines.append(f"- **Purpose:** {r.get('primary_purpose', '—')}")
        lines.append(f"- **Classification:** {r.get('classification', '—')}")
        if r.get("classification_rationale"):
            lines.append(f"- **Rationale:** {r.get('classification_rationale')[:300]}…" if len(r.get("classification_rationale", "")) > 300 else f"- **Rationale:** {r.get('classification_rationale')}")
        touch = r.get("protocol_touchpoints") or []
        if touch:
            lines.append(f"- **Touchpoints:** {', '.join(touch)}")
        norm = r.get("normative_artifacts") or []
        if norm:
            lines.append("- **Normative artifacts:**")
            for a in norm[:8]:
                lines.append(f"  - `{a}`")
            if len(norm) > 8:
                lines.append(f"  - … (+{len(norm) - 8} more)")
        deps = r.get("dependencies") or {}
        if deps.get("upstream") or deps.get("downstream"):
            lines.append(f"- **Dependencies:** upstream={deps.get('upstream', [])}; downstream={deps.get('downstream', [])}")
        lines.append("")

    lines.extend([
        "## Mandatory-Stack Implication Catalog",
        "",
        "Code/docs implying Mongo, reactor, or org infra is **mandatory** (not merely default).",
        "",
        "| Repo | Path | Quote |",
        "|------|------|-------|",
    ])
    for r in records:
        repo = r.get("repo", "")
        for item in r.get("reference_only_assumptions") or []:
            path = item.get("path", "")
            quote = (item.get("quote") or "").replace("|", "/").replace("\n", " ")[:180]
            if MANDATORY_STACK.search(f"{path} {quote}") or MANDATORY_STACK.search(quote):
                lines.append(f"| `{repo}` | `{path}` | {quote} |")

    lines.append("")
    return "\n".join(lines)


def generate_contradiction_register(records: list[dict]) -> str:
    rows: list[dict] = []
    idx = 1
    for r in records:
        repo = str(r.get("repo", ""))
        for c in r.get("contradictions") or []:
            title = c.get("title", "")
            detail = c.get("detail", "")
            rows.append({
                "id": idx,
                "repo": repo,
                "tension": tag_tension(title, detail),
                "title": title,
                "evidence": c.get("evidence", ""),
                "severity": c.get("severity", "Info"),
                "verified": "no",
            })
            idx += 1

    tension_coverage = {tag: False for tag in TENSION_KEYWORDS}
    for row in rows:
        if row["tension"] in tension_coverage:
            tension_coverage[row["tension"]] = True

    p01: list[tuple[str, dict]] = []
    for r in records:
        repo = str(r.get("repo", ""))
        for n in r.get("notable_findings") or []:
            if n.get("severity") in ("P0", "P1"):
                p01.append((repo, n))

    lines = [
        "# AFI Contradiction Register",
        "",
        "**Status:** DRAFT — unverified; adversarial verify required in Phase 3",
        "**Date:** 2026-06-15",
        f"**Entries:** {len(rows)} contradictions from Phase 1 recon",
        "",
        "Promote to [`afi-docs/specs/AFI_CONTRADICTION_REGISTER.md`](../../AFI_CONTRADICTION_REGISTER.md) after verification.",
        "",
        "---",
        "",
        "## Tension Coverage Check",
        "",
        "| Tension | Covered in recon? |",
        "|---------|-------------------|",
    ]
    for tag, covered in tension_coverage.items():
        lines.append(f"| {tag} | {'yes' if covered else '**GAP**'} |")

    lines.extend([
        "",
        "## Register",
        "",
        "| ID | Repo | Tension | Severity | Title | Evidence | Verified? |",
        "|----|------|---------|----------|-------|----------|-----------|",
    ])
    for row in rows:
        title = row["title"].replace("|", "/")[:70]
        evidence = row["evidence"].replace("|", "/").replace("\n", " ")[:100]
        lines.append(
            f"| {row['id']} | `{row['repo']}` | {row['tension']} | {row['severity']} | "
            f"{title} | `{evidence}` | {row['verified']} |"
        )

    lines.extend([
        "",
        "## P0/P1 Notable Findings Appendix",
        "",
        "High-severity items from `notable_findings[]` (distinct from contradiction register).",
        "",
    ])
    for repo, n in p01:
        lines.append(f"### [{n.get('severity')}] `{repo}` — {n.get('title')}")
        if n.get("evidence"):
            lines.append(f"- Evidence: `{n.get('evidence')}`")
        if n.get("recommendation"):
            lines.append(f"- Recommendation: {n.get('recommendation')}")
        lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path, default=CORPUS_DEFAULT)
    args = parser.parse_args()

    if not args.corpus.is_file():
        print(f"ERROR: corpus not found: {args.corpus}")
        return 1

    metadata, records = load_corpus(args.corpus)
    RECON_DIR.mkdir(parents=True, exist_ok=True)
    DRAFTS_DIR.mkdir(parents=True, exist_ok=True)

    summary_path = RECON_DIR / "AFI_RECON_SUMMARY.md"
    summary_path.write_text(generate_summary(metadata, records), encoding="utf-8")
    print(f"Wrote {summary_path}")

    refimpl_path = DRAFTS_DIR / "AFI_REFERENCE_IMPL_MAP.draft.md"
    refimpl_path.write_text(generate_refimpl_map(records), encoding="utf-8")
    print(f"Wrote {refimpl_path}")

    contra_path = DRAFTS_DIR / "AFI_CONTRADICTION_REGISTER.draft.md"
    contra_path.write_text(generate_contradiction_register(records), encoding="utf-8")
    print(f"Wrote {contra_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
