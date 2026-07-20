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

# District/Atlas anchors. Originally mandated by D1CAP-GOV D-D1CAP-8 item 3;
# AMENDED by ATLAS-GOV D-ATLAS-9(3) (afi-governance
# decisions/district-api-atlas-foundation-v0.1.md). The API-Atlas honesty pair is
# re-homed: the API Atlas now has a canonical foundation (afi.protocol-atlas.v1),
# and the literal "not started" anchor attaches to the AFI Protocol City and the
# AFI Participant Gateway, which are genuinely not started. Both District names
# and the retired-POC-path ban are retained unchanged. Matched as literal substrings
# against the raw document text.
REQUIRED_PHRASES = [
    "District 1 — Signal Evaluation",
    "District 2 — Canonical Data",
    "API Atlas",
    "afi.protocol-atlas.v1",
    "not started",
]

# Paths that must never reappear in the current-state map (D1CAP-GOV
# D-D1CAP-8 item 3: District 1 must not be mapped to the removed POC tree).
# Assembled from fragments so this guard's own source carries no complete
# retired literal (Mission R1 D-R1-11); it still bans the path in the document.
BANNED_PATHS = [
    "src/" + "pipe" + "heads",
]

# Retired terminology that must not appear as current architecture in this
# present-tense map (Mission R0 forward-only closure). Matched case-insensitively
# as a substring. The retired POC is superseded; git history is the archive.
# Assembled from fragments (Mission R1 D-R1-11); still banned in the document.
BANNED_TERMS = [
    "pipe" + "head",
]


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

    for phrase in REQUIRED_PHRASES:
        if phrase not in text:
            failures.append(f"required District/Atlas anchor missing: {phrase!r}")

    for banned_path in BANNED_PATHS:
        for m in re.finditer(re.escape(banned_path), low):
            line = low.count("\n", 0, m.start()) + 1
            failures.append(f"banned path named: {banned_path!r} (line {line})")

    for term in BANNED_TERMS:
        for m in re.finditer(re.escape(term), low):
            line = low.count("\n", 0, m.start()) + 1
            failures.append(f"retired terminology named as current: {term!r} (line {line})")

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
          f"0 removed repositories; 0 stale counts; 0 historical vocabulary; "
          f"District/Atlas anchors present; 0 banned paths)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
