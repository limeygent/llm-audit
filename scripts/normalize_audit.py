#!/usr/bin/env python3
"""
normalize_audit.py — recompute the DERIVED tally fields of an llm-audit output
from the authoritative findings[] array, so the auditor never hand-tallies.

Why this exists: the recurring contract failure in production is gate_diagnosis
issue_counts (and the markdown 🚦 lines) disagreeing with findings[] — the model
itemises the findings correctly but fat-fingers the totals. Counting is a
machine's job. Run this immediately after an audit is emitted, before the canary
checker; it makes the whole "gate parity / sum check" failure class impossible.

What it recomputes, purely from findings[]:
  - gate_diagnosis.{G1_retrieval,G2_ranking,G3_citation}.issue_count  (objective)
  - the per-gate issue-count number in the markdown 🚦 GATE DIAGNOSIS lines
  - rewrite_urgency.level (only when wrong) from CRITICAL count + commoditization
    verdict + uncovered sub-query count, per the spec's urgency table, plus the
    markdown 🚨 Rewrite urgency line

What it deliberately does NOT recompute: gate_diagnosis.weighted_score and
dominant_gate. Those need each finding's zone (Zone 1 ×2 vs Body ×1), and zone is
not reliably recoverable from the JSON — the first content section often carries
a topical heading, not a "Zone 1 / hero" label, so neither a heuristic nor the
auditor's own summary can be trusted to reconstruct it. The fix for that is an
explicit per-finding "zone" field: when EVERY finding carries one (value
"ZONE_1" or "BODY"), this tool also recomputes weighted_score + dominant_gate +
the markdown weighted numbers. Until the schema adds that field, weighted_score
and dominant_gate stay the auditor's.

Scope note: every contract failure observed in production was an issue_count /
sum mismatch — all fully objective and all fixed here. weighted_score is not
contract-checked, so leaving it untouched keeps the canary green.

Source-of-truth guard: findings[] AND the markdown "ALL ISSUES" list are the
truth. If their COUNTS disagree, this refuses to run — that is a real authoring
error (a finding present in one but not the other), not a tally to paper over.

Usage:
  normalize_audit.py <audit.md>           # fix in place, print a summary
  normalize_audit.py <audit.md> --check   # exit 1 if changes are needed; write nothing
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

GATE_KEYS = [("G1", "G1_retrieval"), ("G2", "G2_ranking"), ("G3", "G3_citation")]
GATE_LABEL = {"G1": "Retrieval", "G2": "Ranking", "G3": "Citation"}


def extract_json(text):
    blocks = re.findall(r"```json\s*\n(.*?)\n```", text, re.DOTALL)
    if not blocks:
        sys.exit("ERROR: no fenced ```json block found in the audit")
    return blocks[-1]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    if not args:
        sys.exit(__doc__)
    path = Path(args[0])
    check_only = "--check" in flags
    text = path.read_text()
    audit = json.loads(extract_json(text))
    findings = audit.get("findings", [])

    md_issue_count = len(re.findall(
        r"^\s*\d+\.\s*\[(?:CRITICAL|IMPORTANT|MINOR)\]", text, re.MULTILINE))
    if md_issue_count != len(findings):
        sys.exit(f"REFUSING: markdown ALL ISSUES ({md_issue_count}) != findings[] "
                 f"({len(findings)}). That is a content error, not a tally — "
                 "reconcile the findings list first.")

    changes = []

    # zone is recomputable only if EVERY finding carries an explicit zone field
    zone_encoded = bool(findings) and all(
        f.get("zone") in ("ZONE_1", "BODY") for f in findings)

    # ---- gate_diagnosis ----
    by_gate = Counter(f.get("gate") for f in findings)
    weighted = {g: 0 for g, _ in GATE_KEYS}
    for f in findings:
        g = f.get("gate")
        if g not in weighted:
            continue
        weighted[g] += 2 if f.get("zone") == "ZONE_1" else 1
        if f.get("severity") == "CRITICAL":
            weighted[g] += 1

    gd = audit.setdefault("gate_diagnosis", {})
    for g, key in GATE_KEYS:
        blk = gd.setdefault(key, {})
        # issue_count is always objective
        if blk.get("issue_count") != by_gate.get(g, 0):
            changes.append(f"{key}.issue_count: {blk.get('issue_count')} -> {by_gate.get(g, 0)}")
            blk["issue_count"] = by_gate.get(g, 0)
        # weighted_score only when zone is reliably encoded
        if zone_encoded and blk.get("weighted_score") != weighted[g]:
            changes.append(f"{key}.weighted_score: {blk.get('weighted_score')} -> {weighted[g]}")
            blk["weighted_score"] = weighted[g]

    if zone_encoded:
        rank = {"G1": 0, "G2": 1, "G3": 2}  # tie-break G1 > G2 > G3
        dom = max(("G1", "G2", "G3"), key=lambda g: (weighted[g], -rank[g]))
        if gd.get("dominant_gate") != dom:
            changes.append(f"dominant_gate: {gd.get('dominant_gate')} -> {dom}")
            gd["dominant_gate"] = dom

    # ---- rewrite_urgency (derived from findings + commoditization + fan-out) ----
    n_crit = sum(1 for f in findings if f.get("severity") == "CRITICAL")
    verdict = (audit.get("commoditization_check") or {}).get("verdict")
    fc = audit.get("fanout_coverage") or {}
    uncovered = max(
        sum(1 for s in fc.get("subqueries", []) if s.get("coverage") == "UNCOVERED"),
        fc.get("uncovered_count") or 0,
        sum(1 for f in findings if f.get("issue_type") == "UNCOVERED_SUBQUERY"),
    )
    if n_crit >= 3 or verdict in ("COMMODITIZED", "FULLY_COMMODITIZED_AI_SLOP"):
        level = "SEVERE"
    elif n_crit >= 1 or verdict == "PARTIALLY_COMMODITIZED" or uncovered >= 3:
        level = "SUBSTANTIAL"
    elif len(findings) >= 5:
        level = "MODERATE"
    else:
        level = "LIGHT"
    trigger = (f"{n_crit} CRITICAL, commoditization {verdict}, "
               f"{uncovered} uncovered sub-queries, {len(findings)} findings")
    ru = audit.setdefault("rewrite_urgency", {})
    urgency_changed = ru.get("level") != level
    if urgency_changed:  # only touch urgency when the level is actually wrong
        changes.append(f"rewrite_urgency.level: {ru.get('level')} -> {level}")
        ru["level"] = level
        ru["derivation"] = f"derived: {trigger}"

    # ---- markdown body: 🚦 gate issue-count numbers (+ weighted iff zone-encoded) ----
    head_old = text[:text.rfind("```json")]
    head_new = head_old
    for g, _ in GATE_KEYS:
        if zone_encoded:
            pat = re.compile(
                rf"({g}\s+{GATE_LABEL[g]}:\s*)\d+(\s+issues?,\s+weighted\s+)\d+",
                re.IGNORECASE)
            head_new = pat.sub(rf"\g<1>{by_gate.get(g, 0)}\g<2>{weighted[g]}", head_new)
        else:  # fix only the issue-count number, leave the auditor's "weighted Y"
            pat = re.compile(
                rf"({g}\s+{GATE_LABEL[g]}:\s*)\d+(\s+issues?,\s+weighted\s+\d+)",
                re.IGNORECASE)
            head_new = pat.sub(rf"\g<1>{by_gate.get(g, 0)}\g<2>", head_new)
    if urgency_changed:
        head_new = re.sub(
            r"(🚨\s*Rewrite urgency:\s*)\w+(\s*[—-]\s*).*",
            lambda m: f"{m.group(1)}{level}{m.group(2)}{trigger}", head_new)
    md_changed = head_new != head_old
    if md_changed and not any(c.startswith(("G1", "G2", "G3", "rewrite_urgency")) for c in changes):
        changes.append("markdown 🚦/🚨 lines re-synced to findings[]")

    needs = bool(changes) or md_changed
    if check_only:
        if needs:
            print(f"{path.name}: NEEDS NORMALIZATION")
            for c in changes:
                print(f"  - {c}")
            sys.exit(1)
        print(f"{path.name}: already normalized")
        return

    if not needs:
        print(f"{path.name}: already normalized (no changes)")
        return

    # reassemble: re-serialize the JSON only when a JSON field changed; otherwise
    # keep the original block verbatim so a markdown-only fix doesn't reformat it
    json_changed = any(not c.startswith("markdown") for c in changes)
    json_block = (json.dumps(audit, indent=2, ensure_ascii=False)
                  if json_changed else extract_json(text))
    new_text = head_new + "```json\n" + json_block + "\n```"
    if text.endswith("\n"):
        new_text += "\n"
    path.write_text(new_text)
    print(f"{path.name}: normalized -> G1={by_gate.get('G1', 0)} "
          f"G2={by_gate.get('G2', 0)} G3={by_gate.get('G3', 0)} "
          f"(sum {len(findings)}); dominant {gd.get('dominant_gate')}; urgency {level}")
    for c in changes:
        print(f"  - {c}")


if __name__ == "__main__":
    main()
