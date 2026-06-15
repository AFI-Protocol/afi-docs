#!/usr/bin/env python3
"""
Extract Phase 1 recon records from Claude workflow agent jsonl logs.

Usage:
  python3 extract_recon.py [--jsonl-dir PATH] [--out-dir PATH]

Defaults:
  jsonl-dir: ~/.claude/projects/-home-user-AFI-Protocol/.../subagents/workflows/wf_854527ef-4aa
  out-dir:   afi-docs/specs/audit/recon (relative to repo root)
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

WORKFLOW_ID = "wf_854527ef-4aa"
DEFAULT_JSONL_DIR = Path.home() / (
    ".claude/projects/-home-user-AFI-Protocol/"
    "2bcd228c-6aed-4cda-87d6-883d0a0fcfbd/subagents/workflows/wf_854527ef-4aa"
)
SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_OUT_DIR = SCRIPT_DIR.parent / "recon"


def repo_slug(repo_name: str) -> str:
    """Sanitize repo name for filename (e.g. AFI-Protocol/afi-agents -> afi-agents)."""
    name = repo_name.strip()
    if "/" in name:
        name = name.split("/")[-1]
    return re.sub(r"[^a-zA-Z0-9._-]", "-", name)


def extract_best_record(jsonl_path: Path) -> dict | None:
    best: dict | None = None
    best_len = 0
    with jsonl_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            msg = obj.get("message")
            if not isinstance(msg, dict):
                continue
            content = msg.get("content")
            if not isinstance(content, list):
                continue
            for block in content:
                if not isinstance(block, dict):
                    continue
                if block.get("name") != "StructuredOutput":
                    continue
                inp = block.get("input")
                if not isinstance(inp, dict) or not inp.get("repo"):
                    continue
                size = len(json.dumps(inp))
                if size > best_len:
                    best = inp
                    best_len = size
    return best


def collect_records(jsonl_dir: Path) -> list[dict]:
    records: list[dict] = []
    seen_repos: set[str] = set()
    for path in sorted(jsonl_dir.glob("agent-*.jsonl")):
        record = extract_best_record(path)
        if not record:
            continue
        repo = record.get("repo", "")
        if repo in seen_repos:
            continue
        seen_repos.add(repo)
        records.append(record)
    return sorted(records, key=lambda r: str(r.get("repo", "")).lower())


def write_corpus(records: list[dict], out_dir: Path, jsonl_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    per_repo_dir = out_dir / "per-repo"
    per_repo_dir.mkdir(exist_ok=True)

    corpus = {
        "metadata": {
            "extracted_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "source_workflow_id": WORKFLOW_ID,
            "source_jsonl_dir": str(jsonl_dir),
            "phase": "1_complete",
            "repo_count": len(records),
        },
        "records": records,
    }

    corpus_path = out_dir / "AFI_RECON_CORPUS.json"
    with corpus_path.open("w", encoding="utf-8") as f:
        json.dump(corpus, f, indent=2, ensure_ascii=False)
        f.write("\n")

    for record in records:
        slug = repo_slug(str(record.get("repo", "unknown")))
        per_path = per_repo_dir / f"{slug}.json"
        with per_path.open("w", encoding="utf-8") as f:
            json.dump(record, f, indent=2, ensure_ascii=False)
            f.write("\n")

    return corpus_path


def print_summary(records: list[dict]) -> None:
    classifications = Counter(r.get("classification") for r in records)
    replay = Counter(r.get("replay_relevance") for r in records)

    contradictions: list[tuple[str, dict]] = []
    p01_findings: list[tuple[str, dict]] = []
    for r in records:
        repo = str(r.get("repo", ""))
        for c in r.get("contradictions") or []:
            contradictions.append((repo, c))
        for n in r.get("notable_findings") or []:
            if n.get("severity") in ("P0", "P1"):
                p01_findings.append((repo, n))

    contra_by_sev = Counter(c.get("severity") for _, c in contradictions)

    print(f"Records extracted: {len(records)}")
    print("Classifications:", dict(classifications))
    print("Replay relevance:", dict(replay))
    print(f"Contradictions: {len(contradictions)}", dict(contra_by_sev))
    print(f"P0/P1 notable findings: {len(p01_findings)}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract AFI audit recon corpus from agent jsonl logs.")
    parser.add_argument(
        "--jsonl-dir",
        type=Path,
        default=DEFAULT_JSONL_DIR,
        help="Directory containing agent-*.jsonl files",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=DEFAULT_OUT_DIR,
        help="Output directory for AFI_RECON_CORPUS.json and per-repo/",
    )
    args = parser.parse_args()

    if not args.jsonl_dir.is_dir():
        print(f"ERROR: jsonl dir not found: {args.jsonl_dir}")
        return 1

    records = collect_records(args.jsonl_dir)
    if not records:
        print("ERROR: no recon records extracted")
        return 1

    corpus_path = write_corpus(records, args.out_dir, args.jsonl_dir)
    print(f"Wrote {corpus_path}")
    print(f"Wrote {len(records)} per-repo files under {args.out_dir / 'per-repo'}")
    print_summary(records)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
