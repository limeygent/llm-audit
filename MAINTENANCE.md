# Maintenance — llm-audit skill

The premortem (`PREMORTEM.md`, 2026-06-11) found that the skill's decay surface
is everything pinned to one system at one moment: empirical constants, marker
lists, and calibration anchors. The writing science (coreference, condition
preservation, anti-hallucination, density-over-length) ages well; the pinned
numbers do not. This file is the register that keeps the pinned parts honest.

**Operating rule:** a constant past its review-due date is *stale*. The audit
spec instructs auditors to label outputs derived from stale constants as
indicative. Refreshing the date requires actually re-checking the source — not
just bumping the date.

## Constants registry

| # | Constant | Where in skill.md | Source / provenance | Snapshot date | Review due | Status |
|---|---|---|---|---|---|---|
| 1 | Grounding constants (~380 words median/page; ~540-word plateau; ~1,900–2,000-word per-query budget; sentence-level extraction ~15 words; 66/42/25/12% coverage bands) | Step 2, "Page length and coverage" | Petrovic / DEJAN (Dec 2025 + Feb 2026); grounding format changed wholesale early 2026 — single source, unreplicated | 2026-Q1 | 2026-09 | Indicative — pattern (density beats length, sentence as unit) is durable; numbers are one system, one moment |
| 2 | Page-length bands (UNDER_BUILT / HEALTHY / OVER_BUILT per page type) | Step 2, "Page length check" | Derived heuristics from #1 + practitioner experience | 2025-Q4 | 2026-09 | Heuristic — bands are broad on purpose |
| 3 | AI-fingerprint marker registry (STRUCTURAL: contrastive negation, inflated significance, -ing analysis clauses, vague attribution, formulaic skeletons, uniform rhythm, rubric-shaped GEO sameness) | Step 4, Commoditization test 5 | Wikipedia Signs-of-AI-writing (maintained), LinkedIn down-weighting announcement 2026-05, arXiv:2509.19163 (rules > LLM-judge) | 2026-06 | 2026-12 | Lexical tells (em-dash, "delve") retired 2026-06 — false-positive against humans now |
| 4 | Query fan-out figures ("dozens" official; ~3x expansion; ~10–20 typical; ~95% of sub-queries zero search volume; 32.9% of ChatGPT citations fan-out-only) | Step 3, fan-out enumeration | Google I/O statements (official) + AirOps/Moz/Semrush observational data | 2026-Q2 | 2026-12 | Mechanism official; magnitudes indicative; fan-out is personalized — enumeration has a precision ceiling |
| 5 | AI crawler / user-agent matrix (GPTBot, OAI-SearchBot, ChatGPT-User [ignores robots since 2025-12], PerplexityBot, Perplexity-User [ignores robots], Google-Extended [does NOT gate AIO/AI Mode], ClaudeBot, Claude-SearchBot, Claude-User) + JS-rendering facts (only Googlebot/Applebot render) + CDN default-block landscape | Step 0, machine-access checklist | Vendor docs + Vercel/MERJ measurement + Cloudflare policy | 2026-06 | 2026-12 | Names and robots-compliance churn; re-verify vendor docs when refreshing; watch GSC AI opt-out toggle spreading beyond UK |
| 6 | 250-word split test + 40% page-share threshold | Step 2, section integrity | Practitioner heuristic, revised 2026-06 for fan-out container model | 2026-06 | 2027-06 | Stable unless retrieval consensus shifts again |
| 7 | Calibration anchor library (pinned H1 verdicts, worked examples) | Worked Examples section | Cross-LLM variance tuning sessions (fine-tuning/) | 2026-05 | re-validate on every canary failure | Binding per-run; `spec_feedback[]` accumulates pressure to revise |
| 8 | Organic-overlap rates (per-citation ~32–38% from top-10, surface-dependent; AI Mode ~88% NOT top-10; falling fast — Gemini 3 replaced ~42% of cited domains overnight) | Step 0 framing | Ahrefs / seoClarity / Moz 2026 studies. NOTE: the older "~94%" figure was query-level metric conflation — do not reintroduce it | 2026-Q1 | 2026-09 | The *spread and volatility* is the finding; never cite one number without date + surface |
| 9 | Brand-mention correlation (branded mentions ρ≈0.66 ≫ backlinks ρ≈0.22; news placements r≈0.07) | Step 0, entity corroboration row | Ahrefs 75K-brand study 2025 + Seer Interactive | 2025 | 2026-12 | Correlational, not causal — but directionally robust across two independent shops |
| 10 | Schema null result (no citation uplift, any platform; AIO −4.6%) + llms.txt dead (0.1% of bot visits) | Step 0a + 0b | Ahrefs diff-in-diff 2026-05; OtterlyAI log study; Google/Mueller official statements | 2026-05 | 2027-06 | Re-check if OpenAI/Perplexity ever announce schema or llms.txt consumption |

## Refresh procedure

1. Re-source the constant (vendor docs for crawler names; latest replication
   for grounding/fan-out data; current frontier-model output for the marker
   registry).
2. Edit the constant in `skill.md` AND update its row here (new snapshot date,
   new review-due date).
3. Bump `spec_version` in skill.md's JSON schema metadata (see below).
4. Run the drift canary (`canary/README.md`). A spec edit without a canary run
   is an unverified spec edit.
5. Review accumulated `spec_feedback[]` entries from recent production audits
   (the dashboard stores audit JSON; query for non-empty `spec_feedback`).
   Three or more audits flagging the same anchor is a revision signal.

## Spec version log

| spec_version | schema_version | Date | Changes |
|---|---|---|---|
| 1.x | 1.0 | 2026-05-10 | Original spec: 3 gates, zone model, single-intent anchor, commoditization check, calibration anchors |
| 2.0 | 1.1 | 2026-06-11 | Premortem hardening: fan-out coverage replaces single-intent scope-cutting; Step 0 authority/access preconditions; constants provenance-stamped; structural (2026) AI-fingerprint registry replaces lexical tells; validation_plan + spec_feedback JSON fields (additive); drift canary added. Verified same day on golden page (canary PASS, old+new spec). First spec_feedback cycle applied: definitional-anchor exemption to opener-filler test; Zone 1 rounding rule hardened against non-sentence blocks |
| 2.1 | 1.2 | 2026-06-12 | Commoditization recalibration after observed solo-leniency drift (HCG + golden page both scored NOT_COMMODITIZED under literal whole-page reading): test 1 → section-weighted substitution (≥40% body words swappable = fail), test 2 → length-normalized density (<3 unique-data sentences /1,000 words), tie-break toward the fail point, Worked Example 9 anchor. `rewrite_urgency` derived headline (SEVERE/SUBSTANTIAL/MODERATE/LIGHT) so CRITICAL-laden reports can't read as healthy. Fan-out placement strategy: `recommended_home` routing (BODY_SECTION/FAQ_ENTRY/ZONE1_MIRROR/EXTEND_EXISTING_SECTION), PAA merge channel with `source` provenance, `faq_plan` in rewrite_brief, signal-splitting DRY pattern. Canary rebuilt as planted-defect fixture suite (dental-dirty / dental-clean / slop) + Stratum demoted to contract fixture; commoditization band restored to PARTIALLY |
| 2.2 | 1.3 | 2026-06-12 | Disposition-first triage: every section gets KEEP_IN_PLACE/MOVE/MERGE_INTO/REPURPOSE/CUT before the six checks; CUT sections carry only the structural justification + trapped-signal salvage, never sentence polish (a finding is an implicit keep vote). `rewrite_brief.recommended_flow` added (additive): ordered assembly sequence pairing each section's sub-query (machine goal) with one persuasion job (human goal) and explicit CTA placements, built from per-page-type arc templates; NEW entries trace to BODY_SECTION-routed uncovered sub-queries. Rationale: section order is machine-free (chunk retrieval is order-indifferent bar first-passage) so it is spent entirely on the human conversion arc |

## Schema compatibility contract

Downstream consumers: `llm-rewrite` skill, agency-dashboard `run-post-audit.ts`
worker (stores the JSON, feeds the rewriter). The rule for schema changes:

- **Additive only** within a major schema version: new top-level fields, new
  enum tokens appended. Consumers must ignore unknown fields.
- Never rename or re-type an existing field; never remove an enum value.
- Breaking change → new major `schema_version` + coordinated dashboard change.

## The feedback loop (why this file exists)

The premortem's root-cause finding: the audit is open-loop — it scores copy
against heuristics and never observes whether audited pages actually get
cited. The durable fix is workflow-level, not spec-level:

1. Every audit now emits `validation_plan.prompt_corpus` (10–20 real-user
   prompts derived from the fan-out set).
2. The operator (or dashboard, eventually) runs the corpus across ≥3 engines
   before and after the rewrite ships and records citation presence.
3. When rubric-passing pages systematically fail to get cited, the rubric is
   wrong — that observation, not internal consistency, is what triggers a
   spec revision.

Until the dashboard automates step 2, run it manually on at least one page per
quarter alongside the canary.
