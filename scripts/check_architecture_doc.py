#!/usr/bin/env python3
"""Guardrail: AFI_Full_Architecture.md must describe the CURRENT organization only.

The full-architecture document is a present-tense map of AFI as it exists now. This
check fails the build if that one file drifts back into historical or stale shape:

  * a repository that has been permanently removed is named;
  * a stale organization count (anything other than 18) appears;
  * historical-transition vocabulary ("formerly", "legacy", "deprecated", ...) appears;
  * a current organization repository is missing from the document.

Scope is exactly afi-docs/AFI_Full_Architecture.md. This script names the banned
tokens only in order to ban them, so it exempts itself.

Usage:
  python3 scripts/check_architecture_doc.py          # RESULT: PASS / FAIL (exit 1)
"""
import os
import re
import sys

DOC = "AFI_Full_Architecture.md"

# The 18 current AFI-Protocol repositories. Each must appear in the document.
CURRENT_REPOS = [
    "afi-governance", "afi-config", "afi-math",
    "afi-core", "afi-reactor", "afi-infra", "afi-gateway", "afi-mint", "afi-token",
    "afi-factory", "afi-xerc20", "afi-docs", "afi-tiny-brains",
    "afi-econ", "afi-benchkit", "afi-artifacts",
    "afi-protocol", ".github",
]

# Repositories that no longer exist. They must not appear as repository names.
# Matched case-insensitively as the hyphenated repo token, so the DAO vault
# address "ops.afidao.eth" / "AFI_OPS_VAULT_PLACEHOLDER" (underscored, not the
# repo) does not trip the "afi-ops" pattern.
REMOVED_REPOS = [
    "afi-assets", "afi-plugins", "afi-cli-framework",
    "afi-skills", "afi-labs", "afi-ops",
]

# Historical-transition vocabulary. The document is present-tense only.
BANNED_VOCAB = [
    "formerly", "previously", "legacy", "deprecated",
    "superseded", "retired", "no longer", "used to be",
]

# Stale organization counts that must not appear.
STALE_COUNTS = [r"\b19 repositor", r"\b20 repositor", r"\b21 repositor", r"\b22 repositor"]


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.normpath(os.path.join(here, "..", DOC))
    if not os.path.isfile(path):
        print(f"RESULT: FAIL (missing {DOC})")
        return 1
    text = open(path, encoding="utf-8").read()
    low = text.lower()
    failures = []

    for repo in REMOVED_REPOS:
        for m in re.finditer(re.escape(repo), low):
            line = low.count("\n", 0, m.start()) + 1
            failures.append(f"removed repository named: {repo!r} (line {line})")

    for word in BANNED_VOCAB:
        for m in re.finditer(re.escape(word), low):
            line = low.count("\n", 0, m.start()) + 1
            failures.append(f"historical vocabulary: {word!r} (line {line})")

    for pat in STALE_COUNTS:
        for m in re.finditer(pat, low):
            line = low.count("\n", 0, m.start()) + 1
            failures.append(f"stale org count: {text[m.start():m.start()+16]!r} (line {line})")

    if not re.search(r"\b18 repositor", low):
        failures.append("missing the current organization count ('18 repositories')")

    for repo in CURRENT_REPOS:
        if repo not in text:
            failures.append(f"current repository missing from document: {repo!r}")

    print()
    if failures:
        print(f"RESULT: FAIL ({len(failures)} problem(s) in {DOC})")
        for f in failures:
            print(f"    {f}")
        print("The full-architecture document must describe the current 18-repository "
              "organization in present tense, with no removed repositories, no stale "
              "counts, and no historical-transition vocabulary.")
        return 1
    print(f"RESULT: PASS ({DOC}: 18 current repositories present; "
          f"0 removed repositories; 0 stale counts; 0 historical vocabulary)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
