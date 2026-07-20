#!/usr/bin/env python3
"""Guardrail: AFI_Full_Architecture.md must agree with the canonical Atlas registry.

The human-readable current architecture map carries a District / API Atlas summary.
This check fails the build if that summary drifts from the vendored copy of the
canonical machine-readable registry (afi.protocol-atlas.v1), which is the single
structured foundation delegated to afi-config by ATLAS-GOV (D-ATLAS-9). It also
verifies the vendored copy's integrity against atlas/PROVENANCE.txt.

Checks (all derived FROM the registry, never hard-coded):
  * every ACTIVE District's id and display name appears in the document;
  * the reserved capability-domain and its CHAIN-GOV reservation are named;
  * the entity counts stated in the document match the registry
    (active Districts, capabilities, structures, interfaces, typed routes,
    participant roles);
  * every participant-role display name appears;
  * the five governed enrichment categories are named exactly;
  * the current operation identifier factory.official.list is named (residue
    policing of the retired operation name is left to check_stale_refs.py);
  * the registry contract id afi.protocol-atlas.v1 is referenced.

Usage:
  python3 scripts/check_atlas_summary.py          # RESULT: PASS / FAIL (exit 1)
"""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
REGISTRY = os.path.join(ROOT, "atlas", "afi-protocol-atlas.v1.json")
PROVENANCE = os.path.join(ROOT, "atlas", "PROVENANCE.txt")
DOC = os.path.join(ROOT, "AFI_Full_Architecture.md")


def main() -> int:
    failures = []

    for p in (REGISTRY, PROVENANCE, DOC):
        if not os.path.isfile(p):
            print(f"RESULT: FAIL (missing {os.path.relpath(p, ROOT)})")
            return 1

    raw = open(REGISTRY, "rb").read()
    reg = json.loads(raw.decode("utf-8"))
    # normalize the doc: drop markdown emphasis so '**2 active Districts**' matches
    doc = open(DOC, encoding="utf-8").read()
    flat = doc.replace("*", "").replace("`", "")
    flat_low = flat.lower()

    # 0. vendored-copy integrity vs PROVENANCE.txt
    recorded_sha = open(PROVENANCE, encoding="utf-8").read().split()[0].strip()
    actual_sha = hashlib.sha256(raw).hexdigest()
    if recorded_sha != actual_sha:
        failures.append(f"vendored registry sha256 {actual_sha} != PROVENANCE {recorded_sha}")

    # 1. registry contract id referenced
    if reg.get("schema") not in flat:
        failures.append(f"registry contract id {reg.get('schema')!r} not referenced in the document")

    # 2. active + reserved districts
    active = [d for d in reg["districts"] if d.get("active") is True]
    reserved = [d for d in reg["districts"] if d.get("active") is False]
    for d in active:
        if d["districtId"] not in doc:
            failures.append(f"active District id {d['districtId']!r} missing from the document")
        if d["name"] not in doc:
            failures.append(f"active District name {d['name']!r} missing from the document")
    if reserved and "reserved" not in flat_low:
        failures.append("a reserved capability-domain exists but the word 'reserved' is absent")
    if reserved and "chain-gov" not in flat_low:
        failures.append("the reserved settlement domain's CHAIN-GOV reservation is not named")

    # 3. entity counts stated in the doc must match the registry
    counts = {
        "active Districts": len(active),
        "capabilities": len(reg["capabilities"]),
        "structures": len(reg["structures"]),
        "interfaces": len(reg["interfaces"]),
        "typed routes": len(reg["routes"]),
        "participant roles": len(reg["participantRoles"]),
    }
    for label, n in counts.items():
        if not re.search(rf"\b{n}\s+{re.escape(label)}\b", flat):
            failures.append(f"the document must state '{n} {label}' (registry count) and does not")

    # 4. every participant-role display name appears
    for role in reg["participantRoles"]:
        if role["name"] not in doc:
            failures.append(f"participant role {role['name']!r} missing from the document")

    # 5. the five governed categories are named exactly (the superseded
    #    fifth-category identity is guarded structurally by the reactor/config
    #    residue tests, not by naming it here).
    for cat in ("technical", "pattern", "sentiment", "news", "aiMl"):
        if cat not in doc:
            failures.append(f"governed enrichment category {cat!r} missing from the document")

    # 6. current operation identifier present (residue policing of the retired
    #    operation name is check_stale_refs.py's job, tree-wide)
    if "factory.official.list" not in doc:
        failures.append("current operation 'factory.official.list' not named in the document")

    print()
    if failures:
        print(f"RESULT: FAIL ({len(failures)} Atlas-summary drift problem(s))")
        for f in failures:
            print(f"    {f}")
        print("AFI_Full_Architecture.md must agree with the vendored canonical Atlas "
              "registry (afi.protocol-atlas.v1). Update the document (or re-vendor "
              "atlas/afi-protocol-atlas.v1.json + PROVENANCE.txt) so they match.")
        return 1
    print(f"RESULT: PASS (Atlas summary agrees with the registry: "
          f"{counts['active Districts']} active Districts, {counts['capabilities']} capabilities, "
          f"{counts['structures']} structures, {counts['interfaces']} interfaces, "
          f"{counts['typed routes']} typed routes, {counts['participant roles']} participant roles; "
          f"vendored copy integrity verified)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
