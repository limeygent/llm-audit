# Example: healthcare service page audit (spec v2.2)

A complete, real output of the llm-audit skill (Mode A solo) on an HCG weight-loss
service page — **all business identifiers anonymized** (clinic, practitioners,
locations, product names are fictional replacements; findings and verdicts are
unmodified).

| File | What it is |
|---|---|
| `audit.md` | The full audit: markdown report + fenced JSON appendix (schema 1.3) |
| `audit.html` | The same report as a self-contained browser page (open directly) |
| `intent.json` | The upstream page-intent-analyzer sidecar the audit anchored on (`intent_source: INTENT_ANALYZER`) |

What this example demonstrates:

- 🚨 derived `rewrite_urgency` headline (SEVERE — 11 CRITICAL findings)
- Healthcare-mode auto-escalation on unhedged numeric outcome claims
- Section-weighted commoditization scoring (COMMODITIZED, 3/5 fail points)
- Query fan-out coverage with per-sub-query placement routing (`recommended_home`)
- Disposition-first triage (CUT sections carry no sentence polish)
- 📜 Recommended page flow: an 18-entry assembly sequence pairing each section's
  sub-query (machine goal) with one persuasion job (human goal) and CTA placements
- A machine-only finding: clinical claims hidden in an image `alt` attribute
