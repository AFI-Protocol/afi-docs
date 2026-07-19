#!/usr/bin/env python3
"""Guardrail: no afi-docs file may name implementation machinery that no longer exists.

The Reactor Slot 3 and Gateway Slot 4 work removed a set of files, symbols and
collections. Documentation that still names them as live reads as current truth and
is wrong. This check fails the build if any of them reappears anywhere in the tracked
tree.

Scope is the WHOLE tracked tree — every tracked text file, every JSON string field,
prose included. There are no path exemptions by design: an exemption is how the last
set of stale references survived a green gate. Git history is the archive; nothing
here needs to name removed machinery to preserve it.

Usage:
  python3 scripts/check_stale_refs.py          # RESULT: PASS / FAIL (exit 1)
  python3 scripts/check_stale_refs.py --list   # list what is banned and why
"""
import subprocess
import sys

# symbol -> why it is banned / what replaced it.
BANNED = {
    "tssdVaultService": (
        "Reactor-owned divergent scored-signal writer; deleted in afi-reactor ce4c178 "
        "(PR #42). The Reactor now submits canonical evidence via src/evidence/."
    ),
    "vaultFactory": (
        "Gateway TSSD vault writer; deleted in afi-gateway 8a15604 (PR #3). The Gateway "
        "routes only — see afi-gateway/src/services/reactorSubmitter.ts."
    ),
    "froggyDemoService": (
        "Renamed to froggyScoringService in afi-reactor 81c2139."
    ),
    "canonicalNovelty": (
        "Novelty reader; removed in afi-reactor ce4c178 with no replacement."
    ),
    "factory.templates.list": (
        "Factory bundled-template listing operation; renamed to factory.official.list "
        "when the official composition became manifest-authored canonical records "
        "(afi-factory PR #10). Only factory.official.list may be named as live."
    ),
    "reactor_scored_signals_v1": (
        "Reactor-owned Mongo collection behind the removed writer; superseded by the "
        "canonical afi.scored-signal-evidence.v3 evidence store (MongoDB "
        "'scored_signal_evidence') owned by afi-infra."
    ),
}

# Files that legitimately name the banned symbols in order to ban them.
SELF = {"scripts/check_stale_refs.py"}


def tracked_hits(symbol):
    """Every tracked-tree occurrence of symbol, as (path, line_no, text)."""
    proc = subprocess.run(
        ["git", "grep", "-n", "--fixed-strings", "-I", "--", symbol],
        capture_output=True, text=True,
    )
    # git grep: 0 = found, 1 = clean, >1 = real error (do not read as clean).
    if proc.returncode > 1:
        print(f"ERROR: git grep failed for {symbol!r}: {proc.stderr.strip()}", file=sys.stderr)
        sys.exit(2)
    out = []
    for line in proc.stdout.splitlines():
        path, _, rest = line.partition(":")
        num, _, text = rest.partition(":")
        if path in SELF:
            continue
        out.append((path, num, text.strip()))
    return out


def main():
    if "--list" in sys.argv:
        for sym, why in BANNED.items():
            print(f"{sym}\n    {why}\n")
        return 0

    failures = 0
    for sym, why in BANNED.items():
        hits = tracked_hits(sym)
        if not hits:
            print(f"[stale-refs] OK   {sym}: 0 occurrences")
            continue
        failures += len(hits)
        print(f"[stale-refs] FAIL {sym}: {len(hits)} occurrence(s) — {why}")
        for path, num, text in hits[:20]:
            print(f"    {path}:{num}: {text[:120]}")
        if len(hits) > 20:
            print(f"    ... and {len(hits) - 20} more")

    print()
    if failures:
        print(f"RESULT: FAIL ({failures} stale reference(s) to removed machinery)")
        print("Removed machinery must not be named as live. Describe the current "
              "architecture instead: the Gateway routes, the Reactor scores and "
              "constructs evidence, afi-infra persists canonical evidence.")
        return 1
    print(f"RESULT: PASS (0 stale references; {len(BANNED)} symbols checked across the tracked tree)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
