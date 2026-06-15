#!/usr/bin/env python3
"""Deterministic validation harness for the AFI portable-protocol audit (Phases 2-4).

Read-only: validates produced audit artifacts against architecture.md s4/s6 and the
validation contract. Never edits artifacts. Exit code 0 = all applicable checks pass.

Modes:
  themes                 Validate every themes/<key>.json (excluding verified.json).
  verify                 Validate themes/verified.json + full P0/P1 coverage.
  reports [--dir D]      Validate the 6 reports in D (default: final). D in {final, specs}.
  citations [--sample N] Resolve a random sample of file:line citations against live source.
  all                    Run every mode applicable to currently-present artifacts.

Usage:
  python3 validate_audit.py all
  python3 validate_audit.py themes
  python3 validate_audit.py reports --dir specs
  python3 validate_audit.py citations --sample 8 [--seed 0]
"""
import argparse
import json
import os
import random
import re
import sys

# Resolve workspace + audit paths relative to this script (scripts/ -> audit/).
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIT_DIR = os.path.dirname(SCRIPT_DIR)                       # .../afi-docs/specs/audit
SPECS_DIR = os.path.dirname(AUDIT_DIR)                        # .../afi-docs/specs
WORKSPACE = os.path.abspath(os.path.join(SPECS_DIR, os.pardir, os.pardir))  # /home/user/AFI-Protocol
THEMES_DIR = os.path.join(AUDIT_DIR, "themes")
FINAL_DIR = os.path.join(AUDIT_DIR, "final")
DRAFT_REGISTER = os.path.join(AUDIT_DIR, "drafts", "AFI_CONTRADICTION_REGISTER.draft.md")
PORTABLE_SPEC = "AFI_PORTABLE_PROTOCOL_SURFACE.v0.1.md"

SEVERITIES = {"P0", "P1", "P2", "P3", "Info"}
TENSIONS = {"Mongo-only", "reactor-only", "BASE-ledger", "econ-splits",
            "mint-model", "stale-arch-docs", "other"}

# theme key -> assigned core question group -> minimum answer count
THEME_MIN_ANSWERS = {
    "A-normative-surface": 5, "B-reference-impl": 3, "C-onchain-anchor": 4,
    "D-evidence-vault": 3, "E-scoring-dag": 4, "F-analytics": 3,
    "G-emissions-mint": 4, "H-governance": 2, "I-sdks-gateway": 2, "J-docs-drift": 3,
}
THEME_KEYS = set(THEME_MIN_ANSWERS)

REPORTS = [
    "AFI_PROTOCOL_SURFACE_AUDIT.md",
    "AFI_NORMATIVE_REGISTER.md",
    "AFI_REFERENCE_IMPL_MAP.md",
    "AFI_CONTRADICTION_REGISTER.md",
    "AFI_REPLAY_READINESS_MATRIX.md",
    "AFI_ONCHAIN_ANCHOR_GAP_ANALYSIS.md",
]

# <path with extension>:<line>[-<line>]  (also matches the path:line tail of repo@sha:path:line)
# Excludes surrounding punctuation ()[]{},; so inline parenthetical mentions like
# "(afi-token/src/AFIToken.sol:92)" extract the bare path, not the leading bracket.
CITATION_RE = re.compile(r"[^\s:'\"()\[\]{},;]+\.[A-Za-z0-9]+:\d+(?:-\d+)?")

errors = []
warnings = []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def has_citation(s):
    return isinstance(s, str) and bool(CITATION_RE.search(s))


def extract_citations(s):
    return CITATION_RE.findall(s) if isinstance(s, str) else []


# ---------------------------------------------------------------- themes
def theme_files():
    if not os.path.isdir(THEMES_DIR):
        return []
    out = []
    for fn in sorted(os.listdir(THEMES_DIR)):
        if fn.endswith(".json") and fn != "verified.json":
            out.append(os.path.join(THEMES_DIR, fn))
    return out


def validate_theme(path):
    name = os.path.basename(path)
    key = name[:-5]
    try:
        data = json.load(open(path))
    except Exception as e:
        err(f"[themes] {name}: invalid JSON ({e})")
        return
    for k in ("theme", "summary", "answers", "findings", "contradictions"):
        if k not in data:
            err(f"[themes] {name}: missing required key '{k}'")
    if data.get("theme") != key:
        err(f"[themes] {name}: 'theme' field '{data.get('theme')}' != filename key '{key}'")
    if not str(data.get("summary", "")).strip():
        err(f"[themes] {name}: empty summary")

    answers = data.get("answers", [])
    if not isinstance(answers, list) or not answers:
        err(f"[themes] {name}: answers[] missing or empty")
        answers = []
    min_ans = THEME_MIN_ANSWERS.get(key)
    if min_ans and len(answers) < min_ans:
        err(f"[themes] {name}: only {len(answers)} answers, expected >= {min_ans} (one per Group {key[0]} sub-question)")
    for i, a in enumerate(answers):
        if not isinstance(a, dict):
            err(f"[themes] {name}: answers[{i}] not an object"); continue
        for k in ("question", "answer", "evidence"):
            if not str(a.get(k, "")).strip():
                err(f"[themes] {name}: answers[{i}] empty '{k}'")
        if not has_citation(a.get("evidence", "")):
            err(f"[themes] {name}: answers[{i}].evidence lacks a file:line citation -> {a.get('evidence','')!r}")

    for i, f in enumerate(data.get("findings", [])):
        if not isinstance(f, dict):
            err(f"[themes] {name}: findings[{i}] not an object"); continue
        sev = f.get("severity")
        if sev not in SEVERITIES:
            err(f"[themes] {name}: findings[{i}] bad severity {sev!r}")
        if sev in ("P0", "P1") and not has_citation(f.get("evidence", "")):
            err(f"[themes] {name}: findings[{i}] ({sev}) evidence lacks file:line -> {f.get('evidence','')!r}")
        for k in ("title", "recommendation"):
            if not str(f.get(k, "")).strip():
                warn(f"[themes] {name}: findings[{i}] empty '{k}'")

    for i, c in enumerate(data.get("contradictions", [])):
        if not isinstance(c, dict):
            err(f"[themes] {name}: contradictions[{i}] not an object"); continue
        if c.get("severity") not in SEVERITIES:
            err(f"[themes] {name}: contradictions[{i}] bad severity {c.get('severity')!r}")
        if c.get("tension") not in TENSIONS:
            err(f"[themes] {name}: contradictions[{i}] bad tension {c.get('tension')!r}")
        if not has_citation(c.get("evidence", "")):
            warn(f"[themes] {name}: contradictions[{i}].evidence lacks file:line")


def run_themes():
    files = theme_files()
    if not files:
        warn("[themes] no theme files present yet")
        return
    present = {os.path.basename(p)[:-5] for p in files}
    for p in files:
        k = os.path.basename(p)[:-5]
        if k not in THEME_KEYS:
            warn(f"[themes] unexpected theme file: {os.path.basename(p)}")
        validate_theme(p)
    print(f"[themes] validated {len(files)} file(s): {sorted(present)}")


# ---------------------------------------------------------------- verify
def collect_theme_p0p1():
    """Return dict source -> (severity, title) for all P0/P1 theme findings."""
    out = {}
    for p in theme_files():
        key = os.path.basename(p)[:-5]
        try:
            data = json.load(open(p))
        except Exception:
            continue
        for i, f in enumerate(data.get("findings", [])):
            if isinstance(f, dict) and f.get("severity") in ("P0", "P1"):
                out[f"theme:{key}#{i}"] = (f.get("severity"), f.get("title", ""))
    return out


def collect_draft_p0p1():
    """Parse the draft contradiction register markdown table for P0/P1 rows."""
    out = {}
    if not os.path.isfile(DRAFT_REGISTER):
        warn("[verify] draft register not found; skipping draft P0/P1 coverage")
        return out
    for line in open(DRAFT_REGISTER):
        line = line.rstrip("\n")
        if not line.startswith("|"):
            continue
        cols = [c.strip() for c in line.split("|")[1:-1]]
        if len(cols) < 7:
            continue
        rid, sev = cols[0], cols[3]
        if not rid.isdigit():
            continue
        if sev in ("P0", "P1"):
            out[f"draft:{rid}"] = (sev, cols[4])
    return out


def run_verify():
    vpath = os.path.join(THEMES_DIR, "verified.json")
    if not os.path.isfile(vpath):
        warn("[verify] verified.json not present yet")
        return
    try:
        data = json.load(open(vpath))
    except Exception as e:
        err(f"[verify] verified.json invalid JSON ({e})"); return
    entries = data.get("verifications")
    if not isinstance(entries, list) or not entries:
        err("[verify] verifications[] missing or empty"); return

    seen = {}
    for i, v in enumerate(entries):
        if not isinstance(v, dict):
            err(f"[verify] verifications[{i}] not an object"); continue
        src = v.get("source", "")
        if not src:
            err(f"[verify] verifications[{i}] missing source")
        else:
            seen[src] = seen.get(src, 0) + 1
        if not isinstance(v.get("confirmed"), bool):
            err(f"[verify] {src or i}: 'confirmed' must be a bool")
        if v.get("revised_severity") not in SEVERITIES:
            err(f"[verify] {src or i}: bad revised_severity {v.get('revised_severity')!r}")
        if not has_citation(v.get("corrected_evidence", "")):
            err(f"[verify] {src or i}: corrected_evidence lacks file:line -> {v.get('corrected_evidence','')!r}")
        if v.get("confirmed") is False and not str(v.get("note", "")).strip():
            err(f"[verify] {src or i}: refuted entry must justify in 'note'")

    for s, n in seen.items():
        if n > 1:
            err(f"[verify] duplicate source '{s}' appears {n} times")

    expected = {}
    expected.update(collect_theme_p0p1())
    expected.update(collect_draft_p0p1())
    missing = [s for s in expected if s not in seen]
    print(f"[verify] P0/P1 coverage: {len(expected) - len(missing)}/{len(expected)} covered "
          f"(themes+draft); {len(entries)} verification entries")
    if missing:
        err(f"[verify] {len(missing)} P0/P1 finding(s) NOT covered in verified.json: "
            + ", ".join(sorted(missing)[:25]) + (" ..." if len(missing) > 25 else ""))


# ---------------------------------------------------------------- reports
def run_reports(which):
    base = FINAL_DIR if which == "final" else SPECS_DIR
    label = which
    siblings = set(REPORTS)
    any_present = False
    for rep in REPORTS:
        path = os.path.join(base, rep)
        if not os.path.isfile(path):
            err(f"[reports:{label}] missing {rep}")
            continue
        any_present = True
        text = open(path, encoding="utf-8", errors="replace").read()
        if PORTABLE_SPEC not in text:
            err(f"[reports:{label}] {rep}: no link back to {PORTABLE_SPEC}")
        missing_links = [s for s in siblings - {rep} if s not in text]
        if missing_links:
            err(f"[reports:{label}] {rep}: missing sibling cross-links: {missing_links}")
        if len(text.strip()) < 400:
            warn(f"[reports:{label}] {rep}: suspiciously short ({len(text)} chars)")
    if not any_present:
        warn(f"[reports:{label}] no reports present yet in {base}")
    else:
        print(f"[reports:{label}] checked {len(REPORTS)} report slots under {base}")

    if which == "specs":
        for rep in REPORTS:
            fp, sp = os.path.join(FINAL_DIR, rep), os.path.join(SPECS_DIR, rep)
            if os.path.isfile(fp) and os.path.isfile(sp):
                if open(fp, 'rb').read() != open(sp, 'rb').read():
                    err(f"[reports:specs] {rep}: promoted copy differs from final/ staging")


# ---------------------------------------------------------------- citations
def run_citations(sample, seed):
    cites = []
    for p in theme_files():
        try:
            data = json.load(open(p))
        except Exception:
            continue
        for a in data.get("answers", []):
            cites += extract_citations(a.get("evidence", "")) if isinstance(a, dict) else []
        for f in data.get("findings", []):
            if isinstance(f, dict):
                cites += extract_citations(f.get("evidence", ""))
    vpath = os.path.join(THEMES_DIR, "verified.json")
    if os.path.isfile(vpath):
        try:
            for v in json.load(open(vpath)).get("verifications", []):
                if isinstance(v, dict):
                    cites += extract_citations(v.get("corrected_evidence", ""))
        except Exception:
            pass
    cites = sorted(set(cites))
    if not cites:
        warn("[citations] no citations found to sample yet")
        return
    rnd = random.Random(seed)
    chosen = rnd.sample(cites, min(sample, len(cites)))
    ok = bad = skipped = 0
    for c in chosen:
        m = re.match(r"(.+):(\d+)(?:-(\d+))?$", c)
        if not m:
            skipped += 1; continue
        rel, start, end = m.group(1), int(m.group(2)), m.group(3)
        end = int(end) if end else start
        fpath = os.path.join(WORKSPACE, rel)
        if not os.path.isfile(fpath):
            err(f"[citations] file not found: {rel} (from '{c}')"); bad += 1; continue
        try:
            n = sum(1 for _ in open(fpath, encoding="utf-8", errors="replace"))
        except Exception as e:
            err(f"[citations] cannot read {rel} ({e})"); bad += 1; continue
        if end > n:
            err(f"[citations] {rel}:{start}-{end} out of range (file has {n} lines)"); bad += 1
        else:
            ok += 1
    print(f"[citations] sampled {len(chosen)}/{len(cites)} -> resolved={ok} failed={bad} skipped={skipped} (seed={seed})")


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["themes", "verify", "reports", "citations", "all"])
    ap.add_argument("--dir", choices=["final", "specs"], default="final")
    ap.add_argument("--sample", type=int, default=8)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    if args.mode == "themes":
        run_themes()
    elif args.mode == "verify":
        run_verify()
    elif args.mode == "reports":
        run_reports(args.dir)
    elif args.mode == "citations":
        run_citations(args.sample, args.seed)
    elif args.mode == "all":
        run_themes()
        if os.path.isfile(os.path.join(THEMES_DIR, "verified.json")):
            run_verify()
        if any(os.path.isfile(os.path.join(FINAL_DIR, r)) for r in REPORTS):
            run_reports("final")
        if any(os.path.isfile(os.path.join(SPECS_DIR, r)) for r in REPORTS):
            run_reports("specs")
        run_citations(args.sample, args.seed)

    print()
    for w in warnings:
        print("WARN ", w)
    for e in errors:
        print("FAIL ", e)
    if errors:
        print(f"\nRESULT: FAIL ({len(errors)} error(s), {len(warnings)} warning(s))")
        sys.exit(1)
    print(f"\nRESULT: PASS ({len(warnings)} warning(s))")
    sys.exit(0)


if __name__ == "__main__":
    main()
