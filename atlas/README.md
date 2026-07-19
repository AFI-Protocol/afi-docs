# Vendored AFI District / API Atlas registry

This directory holds a **byte-pinned copy** of the canonical machine-readable
AFI District / API Atlas registry. The canonical source of truth is **afi-config**:

- Canonical schema: `afi-config/schemas/atlas/v1/afi-protocol-atlas.schema.json` (`afi.protocol-atlas.v1`)
- Canonical registry: `afi-config/registries/afi-protocol-atlas.v1.json`
- Governance: `afi-governance/decisions/district-api-atlas-foundation-v0.1.md` (**ATLAS-GOV**)

`atlas/afi-protocol-atlas.v1.json` here is a vendored copy so that afi-docs can
mechanically drift-check its human-readable architecture map against the registry
**without a build-time dependency on afi-config**. `atlas/PROVENANCE.txt` records
the vendored copy's `sha256` and the afi-config source commit it was copied from.

- `scripts/check_atlas_summary.py` asserts that `AFI_Full_Architecture.md` agrees
  with this vendored registry on the active District ids/names, entity counts,
  participant roles, the five governed enrichment categories, and the current
  operation identifiers (ATLAS-GOV D-ATLAS-9(2)).

This copy is **descriptive** and holds no authority: it never overrides the
afi-config canonical registry. When the canonical registry changes, re-vendor this
copy and update `PROVENANCE.txt` in the same change (forward-only; ATLAS-GOV
D-ATLAS-14).
