---
name: llm-readability-audit
description: Audits website copy for LLM readability, extractability, and AI search visibility. Use this skill whenever a user wants to audit, score, check, or improve web page copy for AI search, GEO, LLM readability, machine readability, or AI visibility. Also use when a user pastes any page content and asks if it is well-structured, dense enough, or LLM-friendly. Triggers on phrases like "audit this copy", "check this page", "is this LLM-ready", "score my content", "AI slop check", or any time a page is pasted for review. Always use this skill even if the request is phrased casually. This skill is standalone — it has no dependencies and does not require the intent analyzer or any other skill to run first.
---

# LLM Readability Audit

> ## Execution mode — read this before anything else
>
> **Default: Mode A — single-LLM solo audit.** Apply this spec directly to the supplied article body and emit the audit per the Output Format section. Do NOT orchestrate a council, do NOT spawn subagents, do NOT read other files. The audit comes from your own reasoning over the embedded methodology + article. This is what worker scripts (e.g. `run-post-audit.ts`) and most `claude -p` invocations expect.
>
> **Mode B — multi-LLM council orchestration.** Only enter Mode B when one of these explicit signals is present:
>
> 1. The operator's prompt contains the literal phrase `Mode B`, `use council mode`, `council mode`, `multi-LLM audit`, or `run the council`
> 2. The orchestrating environment provides the `Agent` tool AND the operator's prompt explicitly invokes the council
> 3. You have been told by name to read `/Users/nomis/.claude/skills/llm-audit/RUNNING.md`
>
> If none of those apply, you are in Mode A. Produce the audit and stop. Do NOT try to spawn an `Agent` tool, do NOT try to invoke `council_cli.py`, do NOT create a `runs/<id>/` directory, do NOT read `RUNNING.md`. These add latency and cost for no benefit when the consumer just wants a solo audit.
>
> **If you are unsure, default to Mode A.** Mode B is opt-in.

## Objective

Audit a web page (HTML or markdown) for AI-search retrieval, ranking, and citation problems and emit a structured report — a human-readable markdown body followed by a fenced JSON appendix — that an LLM rewriter agent can mechanically consume. Success is defined precisely:

1. Every finding names the section, the gate (G1/G2/G3), the check, the severity (CRITICAL/IMPORTANT/MINOR), the verbatim flagged sentence, the literal replacement, and a one-sentence rationale.
2. The JSON appendix parses with a standard `json.loads()` call without manual cleanup.
3. Protected compliance content (FDA disclaimers, AHPRA hedging, legal location disclaimers, financial disclosures) is preserved verbatim and recorded with `rewrite_permissions` so the rewriter cannot strip it.
4. The same input run through any frontier LLM produces ≥70% finding overlap on top-N CRITICAL findings — the spec is mechanical, not interpretive.
5. The rewriter receives a `rewrite_brief` with dominant gate, target length range, keep/merge/cut sections, a unique-angle recommendation, and a `do_not_do` list.

The audit's downstream consumer is an LLM rewriter (e.g. `llm-rewrite`). Both the markdown and the JSON are required output.

### The problem this solves

Most web content was written for human readers browsing a page top-to-bottom. AI systems don't read pages — they chunk them, embed them, and retrieve individual sections in isolation. A page that reads well in order can fail completely when its sections are pulled apart: pronouns lose referents, claims lose context, entities aren't named, and generic marketing copy is indistinguishable from every competitor. Worse, when 100 competitors use LLMs to produce vanilla content, no individual sentence is wrong but no page surfaces as the authoritative winner — the page-level Commoditization check addresses this directly.

This audit identifies exactly where and why content fails when chunked, scores the page's commoditization risk, and produces actionable findings that feed directly into a rewriting workflow.

### Scope

Local B2C service businesses — dental, trades, legal, allied health, emergency services, and similar. The audit covers service pages, location pages, and supporting blog content. It is not designed for e-commerce product pages, SaaS landing pages, or enterprise B2B content. Educational/informational pages with no commercial intent are supported via the educational-mode adjustments in Step 4.

### How the output is used

The audit report is the **input for an LLM writer** that rewrites the page. The report must therefore be:

1. **Specific enough to act on** — every finding names the exact section, the exact problem, and what the fix looks like.
2. **Prioritised** — the actions list is ordered so the writer tackles the highest-impact fixes first (page-level commoditization → Zone 1 issues → section integrity issues → per-section content fixes).
3. **Non-contradictory** — findings must not conflict with each other; the writer should be able to apply all of them.
4. **Mode-aware** — healthcare compliance constraints, legal disclaimers, and industry-specific hedging are flagged as protected so the writer doesn't strip them.
5. **Mechanically consumable** — the JSON appendix uses stable field names, fixed enums, and deterministic structure so the rewriter parses without interpretation.

### Side benefit: SEO

Content optimised for LLM citation is also well-structured, entity-dense, query-matchable, and free of filler — which aligns with what traditional search engines reward. This audit is not an SEO audit, but pages that score well here will also tend to perform well in organic search.

---

## What this skill does

1. Detects industry mode (healthcare or standard)
2. Maps Zone 1 (first ~20%), checks page length, and assesses section integrity across all Body sections
3. Checks reader flow, search intent logic, multi-intent coverage, and multi-hop reasoning chains
4. Runs a competitive differentiation check (what, who, what job, what constraint)
5. Runs a content format audit (tables / lists / paragraphs / headings)
6. Runs a DRY (Don't Repeat Yourself) check
7. Runs a trust signals check
8. Runs an anchorable statement check with condition preservation
9. Detects and excludes CTA blocks from section assessment
10. Assesses each content section across 6 checks, producing strengths and issues per section
11. Flags worst offending sentences with rewrites
12. Outputs a structured report: what's working, what needs fixing (by severity), gate diagnosis, and a prioritised issues list for the LLM writer

---

## Theoretical Foundation

This skill combines peer-reviewed research, established IR principles, and practitioner frameworks. Each source is labelled below so you know what's empirical, what's logical inference, and what's industry perspective.

### The three citation gates — a diagnostic model

This is a **diagnostic framework** for categorising content problems, not a description of how any specific system works internally. Real AI answer systems are proprietary and vary across Google, OpenAI, Perplexity, and others. But the three failure modes are logically distinct and useful for deciding what to fix:

| Gate | What goes wrong | Content problems |
|---|---|---|
| **1. Retrieval** | The chunk never surfaces for the query | Wrong categorical language, missing entity names, page too long for coverage |
| **2. Ranking** | The chunk surfaces but loses to competitors | Low information density, vague claims, missing relationships, no competitive differentiation |
| **3. Citation** | The chunk ranks but the LLM can't confidently use it | Unresolved pronouns, missing conditions, no self-contained quotable statement |

A page can pass Gate 1 (retrieved) and fail Gate 3 (never cited) because it has no self-contained statement the LLM can confidently use. The gate model helps you categorise each finding so you know whether you're solving a retrieval problem, a ranking problem, or a citation problem.

### Sources — what's proven, what's inferred, what's perspective

**Peer-reviewed research:**

- **"Lost in the Middle" (Liu et al., 2023):** 📄 *Peer-reviewed.* Information position within a context window affects model attention during generation. Claims near the beginning or end of the context are used more reliably than claims in the middle. This is a secondary attention effect during answer generation, not a retrieval mechanism — it does not affect which chunks get retrieved in RAG systems. It reinforces the importance of Zone 1 (first-passage bias) but does not justify position-based weighting for the rest of the page.
- **Dense X Retrieval (Chen et al., EMNLP 2024):** 📄 *Peer-reviewed.* Proposition-level retrieval (atomic, self-contained claims) outperforms passage and sentence-level retrieval. The main quality failure in automated proposition extraction is unresolved coreference — the "it" and "this" problem. This directly underpins the Extractability checks in this audit.
- **HippoRAG (Gutierrez et al., NeurIPS 2024):** 📄 *Peer-reviewed.* Graph-based retrieval builds knowledge from (subject, predicate, object) triples. The paper tests a retrieval *method*, not a content authoring strategy. The inference that content with clear SVO structures is easier for such systems to process is reasonable but not directly tested by the paper. Multi-hop reasoning chains break when any link is missing.
- **E-GEO (Bagga et al., 2025):** 📄 *Peer-reviewed.* Tested multiple GEO rewriting strategies on thousands of product queries. Key finding: minimalist rewriting (stripping content to bare data points) performed near the bottom — oversimplifying is almost as harmful as making things up. This underpins the oversimplification warning in this audit.

**Industry data (not peer-reviewed, but data-driven):**

- **Petrovic / DEJAN (2025):** 📊 *Industry research.* Analysis of queries and snippets from Google's Gemini grounding system. Reports that the typical page gets a limited number of words selected for grounding regardless of total page length, with coverage dropping sharply as page length increases. The core principle — density beats length because grounding coverage is finite — is logically sound and aligns with how retrieval systems work. Specific numbers should be treated as indicative of the pattern, not as universal constants, since the data is specific to one system at one point in time.

**Practitioner frameworks (informed perspectives, not empirical findings):**

- **Eikhart Language Utility Framework (Eijkemans, 2026):** 💡 *Practitioner framework.* Five-point content utility model — position, competitive differentiation, sentence independence, stated relationships, and anchorable statements. Core principle: structure should be in the language itself, not in technical overlays. Useful as a content quality model, not empirically validated.
- **Kopp / Aufgesang:** 💡 *Practitioner framework.* LLM readability optimisation model. Proposes that pages pass source qualification (E-E-A-T, domain trust) as a gate, then individual chunks compete on quality. The two-stage model (authority gets you in the door, content quality gets you cited) is a reasonable mental model.
- **Forrester / DuaneForresterDecodes (2026):** 💡 *Practitioner perspective* (former Bing product manager). The Utility Gap — content can be great for humans and useless to a model. The concept of "anchorable statements" (self-contained, quotable claims) is logically sound: a sentence that works in isolation is obviously easier for an LLM to cite than one requiring surrounding context.

**Established IR principles:**

- **Turnbull (2026):** 📚 *Established IR principle.* Semantic search systems don't just measure similarity — they also need to match (include or exclude). Precise categorical language ("semi-automatic espresso machine" not "coffee maker") gives retrieval systems more to work with. This is well-established in information retrieval literature, not a novel claim.

---

## Step 1 — Industry Mode Detection

Determine whether the content is from a **regulated healthcare context** or a **standard commercial context** before assessing anything.

**Detect healthcare mode if the copy includes any of:**
- References to clinical procedures, treatments, or diagnoses
- Practitioner names, registration numbers, or credentials (e.g. AHPRA)
- Hedged therapeutic language ("may help," "may reduce," "can support")
- Healthcare provider names (dental, medical, allied health, psychology, pharmacy, etc.)

**Note on other regulated industries:** Financial services, legal, and education content may also require hedged language or compliance-constrained phrasing. If the content is from one of these industries, apply the same principle as healthcare mode — do not penalise compliance-required hedging — and note the mode in the report header.

Declare mode at the top of every report:
> 🏥 **Healthcare Mode Active** — Scoring adjusted for AHPRA compliance. Hedged therapeutic language and absent clinical outcome data are not penalised.
> ⚙️ **Standard Mode Active**

---

## Step 2 — Zone Analysis & Page Length Check

### Zone model

The page is divided into two zones based on one well-supported finding: **first-passage retrieval bias**. In both traditional IR and embedding-based retrieval, the opening content of a page (title, H1, first paragraphs) carries disproportionate weight in matching and ranking. This is the only position-based retrieval advantage with strong evidence across systems.

Beyond the opening, **position does not affect retrieval**. Modern RAG systems chunk pages into ~500-token passages and embed each chunk independently. Each chunk competes on its own semantic similarity to the query — its position on the original page is not a retrieval signal. The "Lost in the Middle" effect (Liu et al., 2023) applies to how LLMs attend to information *within their context window during generation*, not to how retrieval systems select chunks. It is a secondary attention effect, not a retrieval mechanism.

| Zone | Position | Weight | Purpose |
|---|---|---|---|
| Zone 1 | First 20% by character count, capped at 2,000 chars | 2x | Dense atomic facts — answers primary intent immediately. Benefits from first-passage retrieval bias. |
| Body | Remaining content | 1x | All other content sections. Each section competes independently on content quality, not position. |

**How to compute Zone 1 mechanically (do not estimate visually):**

1. Count the total characters of the visible body content (exclude HTML, navigation, footer, sidebar, and any detected CTA blocks).
2. Zone 1 boundary = `min(0.20 × total_chars, 2000)`, rounded UP to the end of the current sentence (do not split a sentence).
3. If the body is < 2,000 characters total, Zone 1 IS the entire body — flag the page as `UNDER_BUILT` for any commercial intent (see Page Length Bands below).
4. Record the computed Zone 1 character count in the report header (e.g. "Zone 1: first 840 characters / 2 sentences").

**Do not write "first ~20%" without computing it. Every audit must show the character count.**

**Zone 1 must contain at minimum:**
- Named entity (clinic, product, practitioner, brand, location)
- Core service or offering explicitly stated
- Target user or patient described
- At least one anchorable statement (dense, self-contained, citable without context)

**Body sections are not ordered by retrieval priority.** Section ordering is a UX decision for the human reader (logical flow, narrative progression). It does not affect how retrieval systems find or rank individual chunks. A well-written section in the middle of the page retrieves identically to the same section at the bottom.

**What matters for every Body section is content quality per chunk** — see Section Integrity below.

**CTA blocks and zone mapping:** CTA interstitial sections (e.g., "Book Now / Let's Chat", "Get Started") are UI elements, not content. Skip them when calculating zone boundaries and assessing whether a zone contains required elements. If a trust signal or atomic fact is embedded inside a CTA block, flag it as trapped — it does not count as present in the zone.

### Section integrity

Every content section (under an H2 or H3) will be retrieved as an independent chunk. It must work in isolation. The section integrity test has three rules:

**1. Topical binding** — Every section must fall within the scope of the **primary search intent** the page serves (identified in Step 3). The search intent — not the H1 — is the anchor. If the H1 doesn't reflect the search intent, that's a separate finding (flag the H1 as misaligned under heading hygiene).

**The intent scope test:** Does this section answer a sub-question that someone with the primary search intent would naturally ask? If someone searching "dental implants Westminster WA" would plausibly want to know this, the section is within scope. If they wouldn't, it's drifting.

Three levels of drift:

- **On-topic:** The section directly answers a sub-question of the primary intent. "What do dental implants cost?" for a page serving "dental implants Westminster" — cost is something an implant searcher naturally asks.
- **Adjacent but oversized (scope creep):** The section covers a related query that deserves its own page. "Dental Implants vs Bridges vs Dentures — A Complete Comparison" running 3+ paragraphs on an implants page is a mini-page within a page. It will never compete against a dedicated comparison page, and it dilutes the implants page's focus. **Flag as scope creep** — recommend splitting into its own page and linking to it, or reducing to a brief comparison table that stays focused on implants as the primary option.
- **Off-topic:** The section's topic is not a sub-question of the primary intent at all. "All About Westminster, WA" on a dental implants page — no one searching for dental implants is looking for suburb facts. **Flag as off-topic** — recommend removing or replacing entirely.

**The split test (mechanical):** Count the words in the section. If the section exceeds **250 words** AND fully answers a distinct query someone would search for independently, flag it as **scope creep** — recommend splitting into its own page or reducing to a brief comparison summary that stays focused on the primary intent. Sections under 250 words that mention the adjacent topic but stay focused on the primary intent are fine; a brief comparison table or a single referencing paragraph is allowed. Do not use "paragraphs" as the unit — paragraph length varies wildly. Use word count.

**2. Single concept** — One section answers one question or covers one concept. If a section covers both "how long do implants last" and "what do implants cost", those are two different queries competing in the same chunk. An LLM retrieving this chunk for a cost query gets diluted by longevity content, and vice versa. Split them.

**3. Self-containment** — The section makes complete sense pulled out of the page entirely. No "as mentioned above", no pronouns pointing to a previous section, no assumed context from earlier content. A reader (or retrieval system) landing on just this section gets a complete answer. The primary entity must be re-anchored within the section so the chunk identifies who/what it's about without needing the page title or preceding sections.

**FAQ accordion exception.** If a section is structurally an FAQ — its heading is a generic FAQ label (e.g. "Frequently Asked Questions", "FAQs", "Common Questions") AND its body contains 3 or more discrete question-answer pairs (each Q being a search-style question and each A being a 1–4 sentence answer) — assess each Q&A pair as its own micro-section for the integrity rules above. The single-concept rule applies *per Q&A pair*, not to the entire FAQ block. Re-anchoring of the primary entity is required only in the answer body, not in the question.

**Pages without semantic H2/H3.** If the body contains zero H2 or H3 elements (the entire page is one flat block, with topic shifts marked only by line breaks, bolding, or visual whitespace), emit a page-level CRITICAL finding `MISSING_SEMANTIC_HEADINGS`. For the rest of the audit, infer sections from paragraph clusters separated by ≥1 blank line plus a topic shift, and assess each cluster against the integrity rules. The rewriter's first job in this case is to add semantic H2/H3 markers — most other findings cascade from this.

**The test:** Could this section be the only thing an LLM retrieves, and would it (a) fully answer one specific question, (b) clearly belong within the scope of the page's primary search intent, and (c) make sense without any other section? If yes, the section is well-constructed. If (a) is true but the section is large enough to be its own page, flag it as scope creep.

### Page length and coverage

Petrovic's research on Google's Gemini grounding system (7,060 queries, 883,262 snippets) shows that the typical page gets ~380 words selected for grounding regardless of total page length. Coverage drops sharply as page length increases:

| Page length | Approximate content used for grounding |
|---|---|
| Under 5,000 characters | ~66% |
| 5,000–10,000 characters | ~42% |
| 10,000–20,000 characters | ~25% |
| Over 20,000 characters | ~12% |

This data is specific to Google's Gemini system but serves as a useful proxy: adding more content dilutes coverage without increasing what gets selected. Every section on the page should justify its length by carrying new atomic facts. On long pages, section integrity becomes critical — each section must earn its place by covering a distinct subtopic with dense, self-contained content. Sections that dilute the page with filler or off-topic content waste grounding budget.

**Page length check (mechanical thresholds):** Assess whether the page length is appropriate for the intent complexity using these character-count bands. Use the operator-supplied `page_type` (or infer it from URL slug, H1, and content) and apply the matching row.

| Page type | Under-built (flag CRITICAL) | Healthy range | Over-built (flag IMPORTANT) |
|---|---|---|---|
| Informational / blog post | < 2,000 chars | 2,000–8,000 | > 12,000 chars |
| Service / location page | < 3,000 chars | 3,000–10,000 | > 15,000 chars |
| Comparison / commercial investigation | < 5,000 chars | 5,000–15,000 | > 22,000 chars |
| Emergency service (locksmith, plumber, towing) | < 1,500 chars | 1,500–5,000 | > 8,000 chars |

Record the band as `page_length_band` (`UNDER_BUILT`, `HEALTHY`, or `OVER_BUILT`) in the JSON appendix. Note the approximate character count AND the estimated grounding-coverage percentage from the table earlier in this section. An under-built page typically fails Gate 1 (not enough surface area for retrieval); an over-built page typically fails Gate 2 (grounding budget diluted).

### Zone analysis output
> 🗺️ **Zone Analysis**
> **Page length:** [~X characters / ~X words — estimated ~X% grounding coverage]
> **Zone 1 (first ~20%):** [present ✅ / missing ⚠️ — be specific about what's present/missing from the required minimum]
> **Body ([N] content sections):** [summary — note section integrity issues if any]
> ⚠️ **Architecture gap:** [if key facts or trust signals exist only in Body sections and not in Zone 1, flag them here with a specific recommendation to mirror in Zone 1]
> ⚠️ **Section integrity issues:** [flag any sections that fail topical binding, single concept, or self-containment]
> ⚠️ **Length flag:** [if applicable]

---

## Step 3 — Reader Flow, Search Intent & Reasoning Chains

### Primary and secondary intents

**The primary search intent is the anchor for the entire audit.** Every section's topical binding, every scope creep assessment, and every priority action is evaluated against it. Getting the intent wrong means the whole audit is anchored to the wrong thing.

**How to determine the primary intent:**

**Three accepted modes for supplying the primary intent:**

The audit accepts the primary intent in any of three forms — pick the highest-fidelity one available before falling back.

**Mode 1 — Operator-supplied string (default).** The operator answers the question "What search query or intent is this page targeting?" before the audit runs. The intent is a single string, e.g. `"medically supervised weight loss program — informational/awareness intent"`. Record `intent_source: "OPERATOR"` in the JSON appendix.

**Mode 2 — Upstream intent-analyzer report (preferred when available).** The operator (or an upstream automation) supplies a `page-intent-analyzer` report — a structured analysis containing `discovered_intent` (primary + secondary + hidden), `anchor_sections` (sections that anchor the page's true purpose), `drift_sections` (sections drifting from intent), and a confidence value. When this is supplied:

- Use the analyzer's `discovered_intent.primary` as the primary intent for this audit.
- Use the analyzer's `secondary` list as the secondary intents for the Intent Coverage check.
- For Section Integrity: a section listed in `anchor_sections` automatically passes topical binding (the analyzer has already verified it anchors the intent); a section listed in `drift_sections` automatically fails topical binding (recommend cut or merge per the analyzer's note). You may still apply the other integrity rules (single concept, self-containment) and the per-section content checks.
- Record `intent_source: "INTENT_ANALYZER"` in the JSON appendix and copy the analyzer's `confidence` value into a new `intent_analyzer_confidence` field.
- If the analyzer's `discovered_intent.author_intent_only` differs from `discovered_intent.primary`, the rewriter will need to refocus drift content; flag this in the rewrite_brief.

This mode is the highest-fidelity path because the upstream skill has already done the work of separating what the page IS trying to be from what it currently SAYS. The audit can defer to those classifications instead of re-deriving them.

**Mode 3 — No operator, no analyzer (automated context).** If the audit is invoked in a context where neither a human operator nor an intent-analyzer report can be supplied (API call, batch worker, scheduled job, and the calling environment did not pre-fetch intent):

- **Default behaviour:** halt and emit a structured error to the JSON appendix: `{"error": "INTENT_REQUIRED", "message": "Primary search intent must be supplied as either an operator string or a page-intent-analyzer report; the audit refuses to fabricate."}`. Do not proceed.
- **Inferred-intent override:** if the runner explicitly authorises inference (e.g. via a documented `--inferred` flag in the calling environment), infer the primary intent from the URL slug, the H1, and the page `<title>`. Record `"intent_source": "INFERRED"` so the rewriter knows the anchor is a guess and can be challenged.

Never silently fabricate the primary intent. The output must always state whether the intent was operator-supplied, analyzer-supplied, or inferred. The downstream rewriter trusts the audit's `intent_source` value to know how confident to be in the rewrite anchor.

**Validate the stated intent against the page content.** After reading the page, check whether the stated intent is too narrow or too broad for what the page actually contains:

- **Too narrow:** The operator says "dental implant costs" but the page covers costs, risks, procedure steps, recovery, and comparisons with alternatives. If you anchor to "costs", every non-cost section gets flagged as scope creep. Flag the mismatch: "You said this page targets 'dental implant costs', but the page contains [N] sections covering [topics]. The page appears to serve a broader intent like 'dental implants [location]' with costs as one sub-question. Which intent should I anchor to?"
- **Too broad:** The operator says "dental services Westminster" but the page only covers implants. The intent is broader than the content. Flag it: "You said 'dental services' but the page only covers implants. Should I anchor to 'dental implants Westminster' instead?"
- **Good fit:** The stated intent matches the scope of the content. Proceed.

Do not silently override the operator's intent. State the mismatch, propose an alternative, and let the operator decide before running the assessment.

> 🎯 **Primary intent:** [e.g. "Can I get dental implants near Westminster WA and who should I go to?"]
> *Derived from: [URL slug / title tag / H1 / operator-provided — state the source]*
> 🎯 **Secondary intents:** [e.g. "How much do dental implants cost in Perth?", "Dental implants vs bridges vs dentures", "What happens during dental implant surgery?"]

Long pages often serve multiple search intents. Identify the primary intent, then identify any secondary intents the page also serves. Each intent should map to at least one anchorable statement somewhere on the page. If a secondary intent is served by content but has no self-contained citable statement, flag it — the page has the information but an LLM can't efficiently cite it for that query.

**H1 alignment check (mechanical substitution test):**

Apply this test to the H1:

1. Does the H1 contain the primary intent's categorical query language? (e.g. for "dental implants Westminster WA", does the H1 contain "dental implants" + a location/qualifier?)
2. Could the H1 be the literal title of someone's Google search? Or does it read as a metaphorical/decorative framing ("Beyond the Diet:", "Your Journey to a Better Smile", "The Path to Wellness")?
3. Strip any framing/decoration from the H1 (everything before a colon that does not contain query language). Does the remaining string still match the intent?

| H1 verdict | Severity |
|---|---|
| Contains primary categorical query + entity/location qualifier | ✅ pass |
| Contains primary categorical query but with decorative framing prefix | ⚠️ MINOR — strip the framing |
| Contains the topic but as a metaphor/decoration with no query language | ⚠️ IMPORTANT — Gate 1 retrieval signal damaged |
| Topic absent or replaced by abstract noun ("Restoring Confidence", "A New Beginning") | ⚠️ CRITICAL — H1 is unmatchable to any query |

A misaligned H1 is a Gate 1 (retrieval) problem — it signals the wrong topic to systems that weight heading content. Always quote the H1 verbatim in the report and state which row of the table it matches.

### Intent coverage table

For each identified intent, check whether the page contains an extractable answer — a self-contained passage (1–3 sentences) that an LLM could use to directly answer that query. Record the answer's position to identify burial risk.

> 🎯 **Intent Coverage**
>
> | # | Query Intent | Extractable Answer? | Section | Notes |
> |---|---|---|---|---|
> | 1 | [primary intent] | ✅ Yes / ⚠️ No | [section name] | [e.g. "answer exists but not mirrored in Zone 1"] |
> | 2 | [secondary intent] | ✅ Yes / ⚠️ No | [section name] | |
>
> ⚠️ **Coverage gap:** [any intent without an extractable answer, or any primary intent answer missing from Zone 1]

### Flow check

Assess whether the page answers its primary intent in a logical sequence. The expected flow depends on the page type:

**Service pages:** What is this → Is this provider credible → Which option fits → What does the process involve → What do I do next

**Emergency service pages (locksmith, plumber, towing, emergency dental, water damage):** Can you help right now → Where are you / how fast can you get here → How much will it cost → Call now. Credibility and process detail come *after* the immediate answer, not before. Zone 1 must contain: service availability (24/7, after-hours), response time, service area, and phone number. A page that opens with company history or educational content before stating availability and response time has a fatal flow break for emergency intent.

**Comparison pages (service options, treatment alternatives):** What are the options → How do they compare → What are the trade-offs → What does each cost → What do I do next

**Educational / blog pages:** What is the topic → Why does it matter → How does it work → What are the implications → What should the reader do

**Location / landing pages:** Am I in the right place → What's offered here → Why this provider → What do I do next

Flag sequence breaks:
> 🔀 **Flow check:**
> ✅/⚠️ Intent answered in opening
> ✅/⚠️ Credibility established early
> ✅/⚠️ Options / content in logical order
> ✅/⚠️ CTA or next step clear
> ⚠️ **Flow gap:** [specific issue if present]

### Multi-hop reasoning chains

Some queries require chaining multiple claims to build an answer. Example: "Is it worth getting dental implants?" requires: what they cost → how long they last → what the alternatives cost over time → what happens if you don't treat. If any link in the chain is missing, the LLM cannot build a complete answer from this page and will go to a competitor for the missing link.

Identify the primary reasoning chain the page needs to support. Check whether all links are present. Flag missing links.

> 🔗 **Reasoning chain:**
> [Query the chain answers] requires: [Link 1] → [Link 2] → [Link 3] → [Link 4]
> ✅/⚠️ All links present / ⚠️ Missing: [specific link]

---

## Step 4 — Competitive Differentiation Check

*Tests Gate 2 (ranking).*

When multiple pages answer the same query, the LLM must select among them. Content that restates what every competitor says provides no ranking advantage — the LLM has no reason to prefer it. This check tests whether the page gives an LLM a reason to cite *this* source over alternatives.

### The four differentiation signals

For the page's primary intent (and ideally each secondary intent), check whether the content explicitly states:

| Signal | Question | Example (pass) | Example (fail) |
|---|---|---|---|
| **What** | Named product, service, or entity? | "Odin House Dental Surgery provides single tooth implants" | "We offer dental solutions" |
| **Who** | Named provider or brand? | "Dr Johannes Yap (DEN0001580350)" | "Our experienced team" |
| **What job** | Specific outcome or problem solved? | "Replaces a missing tooth with a permanent titanium-post restoration" | "Helps restore your smile" |
| **What constraint** | Conditions, scope, or advantage over alternatives? | "For patients with sufficient jawbone density, completed in 3–6 months at $3,500–$7,000" | (absent) |

### Scoring

- **PASS:** All 4 signals appear within a contiguous block of **≤3 consecutive sentences** with no paragraph break between them, ideally in Zone 1. An LLM retrieving this 3-sentence chunk could cite the page and a reader would know exactly who provides what, for whom, under what conditions.
- **PARTIAL:** 2–3 signals present, OR all 4 signals present but spread across more than 3 consecutive sentences (an LLM extracting any 3-sentence window cannot get all 4). The page differentiates on some dimensions but an LLM could still substitute a competitor's content without loss of specificity.
- **FAIL:** 0–1 signals present anywhere on the page. The content is commodity — any business in the category could claim the same statements.

Do not call a passage "extractable" without identifying the exact 3-sentence window. Quote the window in the report.

### The substitution test

Quick validation: mentally replace the brand name with a competitor's name. If every sentence still works, the page has no competitive differentiation and will lose ranking contests to pages that do.

### Page-level Commoditization Check

*Tests Gate 2 (ranking). Critical for the AI-slop saturation problem — when 100 competitors use LLMs to produce vanilla content, no individual sentence is wrong, but no page surfaces as the authoritative winner.*

The four-signal differentiation check above tests whether the page *names* what makes it different. This check tests whether the page *substantiates* anything different at all — whether there is any unique surface area for an LLM to prefer this source over its competitors.

A page can pass all four differentiation signals at the sentence level and still be commodity content. The sentence-level substitution test catches single sentences; this check catches the *whole-page* pattern: every claim plausible, every fact generic, every entity vague enough to belong to anyone.

**Apply these five tests to the page as a whole:**

| # | Test | How to count | Threshold |
|---|---|---|---|
| 1 | **Whole-page substitution** | Replace the brand/clinic/practitioner name throughout the entire page. Does the page still read as a complete coherent article that a competitor could host without modification? | If yes → 1 fail point |
| 2 | **Unique-data density** | Count sentences containing data specific to this provider (this clinic's success rate, this practitioner's case count, this firm's settlement range, named technology in-house, named insurance providers, named protocol). Exclude generic industry stats ("10 million Americans suffer..."). | < 3 such sentences → 1 fail point |
| 3 | **Unique-angle presence** | Does the page contain a named methodology, contrarian take, specific protocol, refusal stance, or viewpoint that 5+ competitor pages would not also state? Examples: "Dr. Yap's three-stage immediate-load protocol", "we do not perform X procedure because Y", "we only treat patients with Z condition profile". | Absent → 1 fail point |
| 4 | **External-verifiable trust signal density** | Count named, externally verifiable trust signals (registration number, named credential, named external citation, specific year-founded, named technology with model number, named insurance providers, named partnerships). Generic claims ("our experienced team", "decades of experience") do not count. | < 3 such signals → 1 fail point |
| 5 | **AI fingerprint markers** | Count AI-fingerprint signals: em-dashes used as primary punctuation, AI-signature transitions ("Moreover,", "Furthermore,", "That said,", "It's worth noting"), parallel-structure pile-ups ("Not just X, but Y" appearing 3+ times), gerund+abstract-noun headings ("Restoring Confidence"), uniform sentence length blocks (3+ consecutive 13–15 word sentences). | ≥ 5 distinct markers → 1 fail point |

**Score the page:**

| Fail points | Verdict | Severity |
|---|---|---|
| 0 | NOT_COMMODITIZED | n/a |
| 1–2 | PARTIALLY_COMMODITIZED | IMPORTANT — page is competitive but missing unique surface area |
| 3–4 | COMMODITIZED | CRITICAL — page reads as AI-vanilla; single highest-leverage fix is at the page level, not the section level |
| 5 | FULLY_COMMODITIZED_AI_SLOP | CRITICAL — say so directly in the summary; recommend rewrite from a unique angle before any sentence-level fixes |

**Reporting.** When a page is COMMODITIZED or worse, flag it at the TOP of the report (above the gate diagnosis) as the dominant problem. The rewriter cannot fix commoditization with sentence-level tweaks — the page needs a unique angle first. Identify the angle in the `rewrite_brief.unique_angle_recommendation` field of the JSON appendix (e.g. "Lead with Dr. Sattele's specific protocol stages and patient-population eligibility criteria — these are present nowhere on the page").

**Commoditization output:**
> 🌐 **Page-level Commoditization Check**
> 1. Whole-page substitution: ✅ passes / ⚠️ fails — [evidence]
> 2. Unique-data density: [N specific sentences found] — ✅/⚠️
> 3. Unique-angle presence: ✅ present ("[quote angle]") / ⚠️ absent
> 4. External-verifiable trust signals: [N found] — ✅/⚠️
> 5. AI fingerprint markers: [N found, list them] — ✅/⚠️
> **Verdict:** NOT_COMMODITIZED / PARTIALLY_COMMODITIZED / COMMODITIZED / FULLY_COMMODITIZED_AI_SLOP
> **Recommended unique angle (if applicable):** [specific suggestion based on what the page already implies but does not commit to]

### Differentiation check output
> 🏷️ **Competitive Differentiation**
> **What:** ✅/⚠️ [Named entity or missing]
> **Who:** ✅/⚠️ [Named provider or missing]
> **What job:** ✅/⚠️ [Specific outcome or missing]
> **What constraint:** ✅/⚠️ [Conditions/scope or missing]
> **Result:** PASS / PARTIAL / FAIL
> ⚠️ **Substitution test:** [Pass = content is unique to this entity / Fail = interchangeable with competitors]

---

## Step 5 — Content Format Audit

LLMs extract structured formatting more reliably than undifferentiated prose. Each format type has a specific use case. Mismatches between content type and format reduce extractability and waste grounding budget.

### Format decision rules

**Use a TABLE when:**
- Comparing 2+ entities across the same set of attributes (e.g. implants vs bridges vs dentures)
- Presenting options with parallel trade-offs
- Showing stage/step data with consistent columns (stage, timeframe, what happens)
- Rule of thumb: if you have 3+ rows AND 2+ consistent columns, it should be a table

**Use a NUMBERED LIST when:**
- Sequence or order matters (steps, stages, instructions, recovery timeline)
- Items must be followed in order

**Use a BULLET LIST when:**
- Items are parallel and discrete but unordered (symptoms, indications, features, inclusions)
- Each item stands fully alone
- There are 3+ items that would create a run-on sentence if written as prose

**Use a PARAGRAPH when:**
- The relationship between ideas is the content (cause-and-effect, explanation, narrative)
- A well-structured paragraph with explicit subject-verb-object is highly extractable
- Do NOT use paragraphs where a table or list would serve — this is the most common format waste on AI-generated pages

### Heading hygiene

Headings serve two functions: **chunk labelling** (some RAG systems split on H tags, making the heading the chunk's context label — though not all chunking implementations use heading boundaries) and **passage matching** (search systems use headings to match query intent to page sections — this is well-established in IR). For human readers, headings are how people scan a page to find the section they need. Good headings help both machines and humans; bad headings hurt both.

**A good heading:**
- Describes the section's content at the right level of specificity ("Dental Implant Costs for Westminster Patients" not "Your Investment")
- Matches the query the section answers, not just the topic category. A category-level heading tells you the subject; a query-matching heading tells you what the section will answer, which is what retrieval systems match against. Category-level: "Dental Crown Materials" / "Tree Removal Process" / "Family Law Services." Query-matching: "Porcelain vs Zirconia Crowns — Which Lasts Longer?" / "How Long Does Tree Removal Take?" / "How Much Does a Family Lawyer Cost in Perth?" Prefer headings that signal the specific question or answer.
- Uses categorical language that matches how users search ("Does Getting a Dental Implant Hurt?" matches the query directly)
- Follows semantic hierarchy — H2 marks a new major section, H3 marks a subsection within it

**Heading problems to flag:**
- **Decorative H tags:** H2/H3 used for visual styling on CTA blocks, taglines, or pull quotes rather than section labels. These create false section boundaries for chunking systems. Flag as: "H tag used for visual formatting, not semantic structure"
- **Creative/metaphorical headings:** "Your Journey to a Better Smile" instead of "The Dental Implant Procedure Step by Step." The creative heading is unmatchable to any query
- **Missing referent headings:** "Restoring Strength and Function" — strength *of what?* Function *of what?* The heading uses abstract nouns with no stated referent. A human infers "teeth" from context; a retrieval system matching against a query cannot. Fix: make the referent explicit ("Dental Crowns Restore Damaged Teeth"). This is a common AI-generated heading pattern — gerund + abstract noun + no object.
- **Filler framing:** Padding phrases prepended to headings that push the actual topic keyword deeper into the string and add zero retrieval signal. Common patterns: "Understanding the Role of...", "The Importance of...", "The Broader Impact of...", "Exploring the Benefits of...", "A Comprehensive Guide to...", "Everything You Need to Know About...". Fix: strip the framing and lead with the topic. "The Importance of Aftercare and Maintenance" → "Dental Crown Aftercare" or "How to Care for a Dental Crown." These are a reliable AI-generated heading signal.
- **Broken hierarchy:** H3 appearing without a parent H2, or H2 used for a subsection that should be H3. This confuses systems that use heading level to infer content relationships
- **Generic headings:** "Overview," "Details," "More Information" — these carry no categorical language and provide zero retrieval signal

Include heading hygiene in the format audit output. Do not score headings as a separate lens — assess them as part of Format Appropriateness (Lens 5) and flag issues in the format audit section.

### AI slop format patterns to flag
- Long paragraphs that list features without relational verbs — should be bullet lists
- Sequential steps buried in prose — should be numbered lists
- Comparison data written as prose across multiple paragraphs — should be a table
- Parallel options described in separate paragraphs with identical structure — should be a table

### Monopoly / sole-provider geographic markets

If the operator marks the page as a sole-provider scenario (e.g., the only clinic of its type within a stated radius) OR the page itself explicitly claims sole-provider status with verifiable evidence (named registry, named licence, named regulator confirmation, geographic-isolation language like "the only X within 500km"), the strict substitution test in Step 4 produces a false fail — by definition there is no competitor to substitute. In this case:

- Bypass the strict sentence-level substitution test for the four differentiation signals.
- Assess differentiation instead on the basis of: (a) verifiable provider credentialing, (b) clear geographic boundary statement, (c) named scope of services, (d) named eligibility constraints.
- Apply the page-level Commoditization check normally — even sole providers can have AI-slop content.
- Set `competitive_differentiation.monopoly_market_bypass` to `true` in the JSON appendix.

### Educational / informational content with no commercial intent

If the operator marks the page as pure educational/informational (no service offering, no provider differentiation expected — e.g. an industry-association explainer, a regulator's consumer guide, a journalist's explainer post hosted on a publication), apply these adjustments:

- **Skip** the four-signal Competitive Differentiation check entirely; record `competitive_differentiation.skipped_educational_mode: true` in the JSON appendix.
- **Skip** the "Years of operation", "Named insurance providers", and "Named technology" rows of the Trust Signals check. Keep "Named author / practitioner", "Credentials / qualifications", "Named external sources", and "Specific data with source" — these still apply for credibility.
- **Apply** the Commoditization check normally — educational pages that read as AI commodity content are still useless even when no commercial differentiation is expected.
- The primary intent is treated as the question/topic the page explains, not a commercial transaction.

### Format audit output
> 📐 **Format Audit**
> ✅/⚠️ Tables used where comparison data exists
> ✅/⚠️ Numbered lists used for sequential content
> ✅/⚠️ Bullet lists used for parallel discrete items
> ✅/⚠️ Paragraphs reserved for relational/explanatory content
> ✅/⚠️ Headings are descriptive, query-matchable, and follow semantic hierarchy
> ⚠️ **Format gap:** [specific section + what format it should use instead + why]
> ⚠️ **Heading issue:** [specific heading + problem (decorative, creative, broken hierarchy, generic)]

---

## Step 6 — DRY Check (Don't Repeat Yourself)

Repetition dilutes grounding budget. Every word repeated is a word that could have been a new atomic fact. DRY violations are one of the most reliable signals of AI-generated filler content.

### Strategic repetition vs waste

Not all repetition is a DRY violation. **Entity re-anchoring** — restating a named entity in a new section so the section becomes self-contained — is good for extractability, provided each mention adds a new attribute or relationship.

**Mechanical disambiguation (synonym cycling vs new-attribute re-anchoring):**

For every repeated mention of an entity, identify whether the new mention adds at least ONE of the following attributes that was not already stated earlier on the page:

- A new credential or registration (e.g., AHPRA, DEN, ABN, Bar admission number)
- A new location or service area
- A named technology, technique, or method
- A specific date, year, duration, or quantity
- A specific scope, eligibility constraint, or condition
- A named insurance provider, partner, or external source
- A specific outcome, success rate, or comparison
- A new product/service line not previously named

| Repeat mention adds at least one new attribute? | Verdict |
|---|---|
| Yes | ✅ Entity re-anchoring — keep |
| No (just a synonym/restatement) | ⚠️ DRY violation — flag |

Synonym cycling ("our team of experts" / "our skilled professionals" / "our experienced practitioners") fails this test because each phrase carries the same payload — it's three labels for the same claim with zero new attributes. Re-anchoring ("Dr Yap" → "Dr Yap, our principal dentist with 20 years' experience" → "Dr Yap, who performs all surgeries in-house using a CBCT cone-beam scanner") passes because each mention introduces a new attribute.

The test: does this repetition make a section independently citable, or does it restate a claim already made without adding information?

| Repetition type | Example | Verdict |
|---|---|---|
| Entity re-anchoring with new attribute | "Dr Yap" in intro (with registration) → "Dr Yap" in procedure section (performs surgery in-house) | ✅ Not a violation — new fact each time |
| Geo re-anchoring with new fact | "Westminster" + service in intro → "Westminster" + drive time in closing | ✅ Not a violation — new fact attached |
| Claim restatement | Same benefit stated in intro AND features AND conclusion | ⚠️ Violation — same claim, no new information |
| Entity re-introduction with identical description | Same practitioner introduced the same way in two sections | ⚠️ Violation — add a new attribute or remove |

### DRY violation patterns to flag

| Pattern | Example | Problem |
|---|---|---|
| Claim restatement | Same benefit stated in intro AND features AND conclusion | Dilutes grounding budget; LLM sees it as low-density |
| Summary padding | "As we discussed above..." / "In summary..." paragraphs that add no new information | Pure budget waste |
| Synonym cycling | "Our team of experts... our skilled professionals... our experienced practitioners..." | Three phrases, one claim |
| Transitional filler | "Now that you understand X, let's explore Y..." | Zero information density |
| Conclusion restating intro | Final section repeats opening claims verbatim or near-verbatim | Confirms AI generation pattern |

### DRY check output
> 🔁 **DRY Check**
> ✅ No significant repetition detected
> — OR —
> ⚠️ **DRY violation:** [Section A] repeats the claim "[claim]" already made in [Section B]. Recommend removing or replacing with a new atomic fact.
> [Flag each distinct violation separately]

---

## Step 7 — Trust Signals Check

Trust signals help at two levels: they strengthen source qualification (E-E-A-T signals help the page get into the retrieval pool), and they make individual claims more specific and verifiable, which improves information density. Whether trust signals directly affect LLM citation probability at the chunk level is unproven — but named credentials, specific data, and verifiable facts are objectively denser and more specific than their generic alternatives, which helps regardless. This check is separate from entity completeness — trust signals are specifically about external verifiability.

### Trust signal types to check for

| Signal | Example | Notes |
|---|---|---|
| Named author / practitioner | "Dr Johannes Yap (DEN0001580350)" | Registration numbers strengthen this |
| Credentials / qualifications | "Registered Dental Practitioner" | Named, not generic ("our experienced team") |
| Named external sources | "According to the Australian Dental Association..." | Cited, not paraphrased anonymously |
| Specific data with source | "$3,500–$7,000 (Australian average)" | Even without citation, specificity signals verifiability |
| Years of operation | "More than 20 years" | Anchored claim, not vague |
| Named technology | "In-house CBCT cone beam scanner" | Specific, verifiable |
| Named insurance providers | "Bupa, Medibank, HBF, HIF, NIB, CBHS" | Verifiable relationships |
| Failure / risk rates | "Implant failure occurs in roughly 2–5% of cases" | Honest data builds citation confidence |
| Named location / address | "3/8 Odin Rd, Innaloo WA 6018" | Physical verifiability |

### Trust signals check output
> 🛡️ **Trust Signals**
> ✅ Present: [list what's found]
> ⚠️ Missing: [list what's absent and would strengthen the page]

---

## Step 8 — Anchorable Statement & Condition Preservation Check

An anchorable statement is a sentence that an LLM could confidently drop into a generated response as a direct citation or closely paraphrased claim. This is the final gate between "retrieved" and "actually cited." A page can pass every other check and still fail here if it has no single sentence that reads like a stable, self-contained answer.

Anchorable statements have these properties (Forrester, 2026):
- Clear definition or specific claim
- Explicit constraints or conditions stated inline
- Direct cause-and-effect or comparison phrasing
- Fully self-contained — makes sense without any surrounding text
- Reads like something a knowledgeable source would say in an interview

### Mechanical anchorable-statement test (apply to every candidate sentence)

A sentence qualifies as anchorable ONLY IF it passes ALL FOUR of these binary tests. Any failure = not anchorable.

1. **Named entity present** — the sentence contains at least one named entity (clinic, practitioner, product, brand, location, technology) that distinguishes the source from competitors.
2. **Specific claim present** — the sentence contains at least one specific data point (number, range, percentage, named procedure, named credential, named outcome, named timeframe, named eligibility condition).
3. **Self-contained** — every pronoun in the sentence resolves to an antecedent within the same sentence. No "this", "that", "these", "above", "below", "as mentioned", "our approach" without a same-sentence noun.
4. **Substitution test passes** — replace the named entity with a generic competitor name (e.g., "Dr. Smith" → "any local dentist", "Acme Roofing" → "any roofing contractor"). If the sentence still reads as a competitor's claim with no loss of specificity, the entity isn't doing work — fail.

If a sentence fails the substitution test, it is NOT anchorable even if it passes 1–3. This is the most common false positive: GPT-class models often accept generic statements ("Medical supervision means your plan is overseen by licensed healthcare professionals") as anchorable. They are not — any clinic could write the same line.

### What is NOT anchorable (examples to consult before flagging)
- Marketing slogans ("Your smile, our passion")
- Vague generalisations ("Recovery times vary depending on the individual")
- Sentences that require context from the previous paragraph
- Claims without specifics ("We offer competitive pricing")
- **Generic category statements that fail the substitution test** ("Medical supervision means your plan is overseen by licensed healthcare professionals" — replace "Medical supervision" with "Our program" and the line still works for any clinic)
- Anonymous testimonials with no named patient AND no named outcome ("I'd tried everything before I found Dr. Smith. Things changed." — anonymous + no specific outcome = decoration, not anchorable)

### Check requirements

**Zone 1 must contain at least one anchorable statement.** This is the highest-retrieval zone due to first-passage bias. If Zone 1 has no statement an LLM could directly cite, the page's best content is functionally invisible for citation purposes.

**Each secondary intent identified in Step 3 should have at least one anchorable statement somewhere on the page.** If the page serves four intents but only has anchorable statements for two, flag the uncovered intents. The position of these statements does not matter — only that they exist in a self-contained section that passes the section integrity test.

### Condition preservation

*Tests Gate 3 (citation). Critical for regulated industries.*

When an LLM extracts a claim, it strips surrounding context. If a claim's validity depends on a condition stated in a different sentence, paragraph, or footnote, the extracted claim becomes unconditionally stated — and potentially false or misleading. This is the highest-risk extraction failure for healthcare, legal, and financial content.

**Check:** For every claim that includes a number, timeframe, guarantee, health outcome, pricing, or legal statement — is the qualifying condition stated *within the same sentence*?

| Before (condition separated) | After (condition preserved) |
|---|---|
| "Patients saw a 60% improvement." *Note: based on 12-week trial, adults 30–55.* | "Adults aged 30–55 with moderate symptoms saw a 60% improvement over 12 weeks in a controlled trial (n=450)." |
| "Returns averaged 12% annually." Footer: *Past performance does not guarantee future results.* | "The fund returned an average of 12% annually from 2019–2024; past performance does not guarantee future results." |
| "Our supplement reduces joint pain by 33%." | "In a 90-day trial of postmenopausal women with moderate osteoarthritis, UC-II collagen at 40mg/day reduced joint pain scores by 33% versus placebo." |

**Regulated industry escalation:** In healthcare, legal, or financial content, any claim with a separated condition is flagged as **CRITICAL** priority regardless of zone (see auto-escalation rule in the Severity guide). A stripped condition in these domains is not just a ranking issue — it is a misinformation vector.

**Conditions trapped inside protected compliance blocks.** If a required qualifying condition (e.g. "Results vary between individuals", "Past performance does not guarantee future results", AHPRA hedge) exists ONLY inside a protected compliance block AND the body of the page makes a claim that needs that condition, do not strip the compliance block. Instead emit a `condition_duplication_required` finding instructing the rewriter to *duplicate* the condition into the claim's sentence while leaving the original compliance block intact. This satisfies both the regulated-mode auto-escalation rule and the don't-touch-compliance rule.

**Anchorable-statement factual verification.** When a candidate anchorable statement contains a specific number, percentage, claim of firsts ("Perth's only..."), named outcome ("85% success rate"), or competitor comparison that cannot be verified from the page itself, emit a `verify_before_publish` finding (severity IMPORTANT). Do NOT instruct the rewriter to invent verification or substitute a placeholder — the operator must verify the claim externally before publication. This protects the audit from being a hallucination vector.

### Anchorable statement & condition preservation output
> ⚓ **Anchorable Statements**
> **Zone 1:** [quote the statement or flag as missing]
> **Intent coverage:** [X of Y identified intents have at least one anchorable statement]
> ⚠️ **Gap:** [specific intent with no anchorable statement + which section should contain one]
>
> 🔒 **Condition Preservation**
> ✅ All conditional claims self-contained / ⚠️ Violations found:
> ⚠️ [Claim] — condition "[condition]" is in [separate sentence / footnote / different section]. Merge into same sentence.
> [Flag each violation. Mark HIGH priority if regulated industry.]

---

## Step 9 — CTA Block Detection

Raw page text often includes CTA (call-to-action) interstitial sections — short blocks like "Book Now / Let's Chat", "Ready To Get Started?", or "Request a Free Consultation Today". These are **UI elements, not content blocks**. They exist for conversion, not for information delivery, and their visual layout on the rendered page is not visible in raw text.

**Do not assess CTA blocks as content sections.** Assessing them as content produces misleading findings.

### How to identify a CTA block

A section is a CTA block if it matches **two or more** of:
- Contains a direct action phrase ("Book Now", "Get Started", "Call Us", "Let's Chat", "Schedule", "Request", "Contact Us Today")
- Is 1–3 sentences long
- Sits between two content sections as an interstitial break
- Would render on the live page as a button, banner, or visual break rather than a readable content section
- Has zero of the following: (a) named external entities (clinic name + new attribute, practitioner name + new attribute, product/technology name), (b) verifiable trust signals (registration numbers, credentials, named insurance providers, named external sources), (c) specific data points (numbers, percentages, ranges, timeframes), (d) claims with stated conditions

**Trapped trust signals.** If a section matches two or more CTA criteria but contains exactly **one** named entity, trust signal, or specific data point that is not duplicated elsewhere on the page, classify it as a CTA AND emit a `trapped_signal` finding (severity IMPORTANT) instructing the rewriter to relocate that signal into a body section before treating the CTA as UI. Do NOT score the CTA itself. Quote the trapped signal verbatim.

### What to do with CTA blocks

1. **Exclude from section assessment entirely.** Do not run checks against CTA blocks.
2. **Exclude from zone content assessment.** CTA blocks do not count as Zone 1 or Body content when assessing whether zones contain required elements.
3. **Flag trapped trust signals.** If a CTA block contains a genuine trust signal or atomic fact (e.g., "More than 20 years of experience" buried in a CTA interstitial), flag it as trapped and recommend moving it to a content section — but still do not score the CTA block itself.
4. **List detected CTA blocks in the output** so the user can see what was excluded and why.

### CTA detection output
> 🔘 **CTA Blocks Detected**
> - [Section heading or first line] — Excluded from assessment. [Note if trust signal is trapped.]
> — OR —
> 🔘 **CTA Blocks Detected:** None

---

## Step 10 — Section-by-Section Assessment (6 Checks)

Assess each content section against six checks. Exclude CTA blocks identified in Step 9. Label each section as Zone 1 or Body. Apply mode-specific rules where indicated.

For each section, produce:
- **Strengths:** What's working well — be specific. These tell the LLM writer what to preserve.
- **Issues:** What needs fixing — name the exact problem, which gate it affects, and what the fix looks like. These are the writer's instructions.
- **Section integrity:** Pass or fail on topical binding, single concept, and self-containment. A section that fails any of these has a structural problem that content-level fixes won't solve — it needs restructuring.

The six checks replace numerical scores with specific, actionable findings. Each check asks a clear question about the section.

### Disclaimer / protected-section assessment policy

Sections whose entire body is regulatory-required compliance text (FDA disclaimers, AHPRA hedge-only sections, location disclaimers, "past performance" language, "not legal advice" footers) are **always listed in the per-section assessment, but always assessed as `N/A — protected`**. Do NOT skip them and do NOT subject them to the six checks. Use this exact format:

> **Section: [Disclaimer heading or first line]** — Body
> Integrity: ✅ N/A (protected compliance content)
>
> ✅ Strengths: Compliance language present and verbatim.
> ⚠️ Issues: None — protected from rewrite.
>
> *(No flagged sentences. This section is recorded in the JSON appendix's `protected_sections[]` array with `protection_type` and `rewrite_permissions` set; the rewriter must preserve it verbatim.)*

This eliminates the inconsistency where some auditors include the disclaimer with content checks (and incorrectly flag it) and others omit it entirely (so the rewriter doesn't know it's protected). Always include. Always mark protected.

### Sentence-flagging rules (apply consistently across all sections)

When flagging sentences for rewrite, follow these mechanical rules so different LLMs produce the same picks:

1. **Quote verbatim.** The `flagged_sentence` must be a literal substring of the page. No paraphrasing. No ellipses. If you can't quote it, don't flag it.
2. **Cap at 3 per section.** Maximum 3 flagged sentences per section. If more issues exist, list them as bullet-level Issues without sentence-level rewrites; the operator can request more on demand.
3. **Priority order within a section:** (a) sentences that fail the anchorable-statement test in Zone 1, (b) sentences with stripped conditions on numeric/regulated claims, (c) sentences that fail the substitution test, (d) sentences that fail the opener-filler test, (e) sentences with unresolved coreference. Stop at 3.
4. **Every flagged sentence must include all four fields:** `flagged_sentence`, `issue` (named gate + named check), `rewrite` (the literal replacement, mode-compliant, not "make it more specific"), and `rationale` (one sentence explaining why the rewrite fixes the gate the issue belongs to).
5. **The rewrite is a literal replacement.** It must be ready to paste into the page as-is. If the original sentence cannot be salvaged with a one-sentence rewrite, propose `[DELETE]` as the rewrite and add a note in the rationale (e.g. "Filler opener — delete; lead the section with the next sentence.").

### Check 1: Structural Fitness

*Affects Gate 2 (ranking) and Gate 3 (citation).*

**Question:** Does each sentence carry its own structure — explicit subject, verb, and object?

Clear subject-verb-object structures are easier for retrieval systems to process than fragments, bullet dumps without verbs, or passive constructions that obscure who does what. This is a reasonable inference from how graph-based retrieval works (HippoRAG, 2024) and a basic principle of clear writing.

**Flag as an issue:** Passive voice obscuring who does what, bullet lists with no relational verbs, marketing fluff with no structure, entities listed without relationships stated between them.

### Check 2: Information Density

*Affects Gate 2 (ranking).*

**Question:** Does every sentence carry a new fact, or is space wasted on filler?

The principle is straightforward: AI systems select a limited amount of content from any page for grounding. Every sentence that doesn't carry a new fact is a sentence that could have carried one, losing competitive ground to pages that did. Industry data (Petrovic/DEJAN) suggests coverage drops sharply as page length increases, reinforcing that density matters more than length.

**Standard mode:** Penalise vague, unverifiable claims. Reward named entities, specific data points, quantified outcomes.
- Weak: "We offer SEO services" → Strong: "Our agency reduces cost-per-acquisition by 15% within 90 days using integrated PPC and SEO data"

**Healthcare mode (AHPRA):** Do NOT penalise hedged language, absent clinical outcome data, or compliance-required disclaimers (e.g., "results vary between individuals," "individual assessment required," "outcomes are not guaranteed"). These sentences exist for regulatory reasons and must not be flagged as filler or recommended for removal. DO penalise generic marketing fluff and missing structural specifics (procedure names, named technologies, named patient conditions).

**Compliance disclaimers (all modes):** Location disclaimers required by law (e.g., Australian Consumer Law requires stating the practice is not located in the target suburb on city-service pages), regulatory disclaimers, and legal CYA statements must not be penalised on any lens. They are not filler — they are compliance constraints. Do not recommend removing them. If the disclaimer can be improved (e.g., by adding useful information to the same sentence), suggest the improvement but keep the disclaimer. Score the section as if the compliance disclaimer were not present when calculating density and quality — it is invisible to the scoring, the same way AHPRA hedging is.
- Weak: "We offer dental treatment" → Strong: "Odin House Dental Surgery provides single tooth implants, implant-supported bridges, and implant-supported dentures for patients in Innaloo and Westminster WA"

**AI slop density flags** (apply in both modes):
- Transitional sentences that carry no information ("Now that we've covered X...")
- Opening sentences that restate the heading or state the obvious. These are a commonly missed slop pattern — flag them consistently. Examples: "Like any surgical procedure, X carries risks" (heading already says "Understanding the Risks"), "This is one of the most common concerns" (heading already says "Does X Hurt?"), "X is a significant investment" (heading already says "X Costs").

  **Mechanical opener-filler test (apply to the FIRST sentence of every section):**
  Check whether the sentence contains each of these three elements:
    (a) a **named entity** that is NOT already stated in the heading (clinic, practitioner, product, location, technology),
    (b) a **specific data point** (number, percentage, range, timeframe, or quantified outcome),
    (c) a **stated condition or constraint** (eligibility, scope, limitation, prerequisite).

  | Elements present | Verdict |
  |---|---|
  | 0 of 3 | **CRITICAL filler** — delete the sentence; lead with the section's first real fact |
  | 1 of 3 | **MINOR filler** — strengthen by adding a second element from the list |
  | 2 or 3 of 3 | Not filler — pass |

  Do not say "the sentence loses zero information." Apply the 3-test. The verdict is binary.
- Closing sentences that summarise the paragraph just read
- Phrases like "it's important to note," "it goes without saying," "as mentioned above"

**Oversimplification warning:** Do not push density to the point of stripping content down to bare data points. E-GEO research (Bagga et al., 2025) found that a minimalist rewriting strategy scored second-worst of 15 strategies — worse than nearly everything except deliberately making things up. "Battery: 18 hours" is extractable but useless without conditions. "Starts at $49/month" without stating what's included is misleading. Dense, condition-preserving prose beats both verbose marketing copy and stripped-down data points. Add structure to language — don't strip language down to structure.

### Check 3: Extractability

*Affects Gate 3 (citation). Grounded in Dense X Retrieval (Chen et al., 2024).*

**Question:** Can every sentence be understood in total isolation?

This is the coreference test. Proposition-level retrieval outperforms passage and sentence-level retrieval, but the main failure mode in automated proposition extraction is unresolved coreference — pronouns and vague references that break the moment a sentence is pulled from its context. This is one of the best-supported checks in the audit.

**This check tests sentence-level independence.** If this sentence were extracted without its neighbours, would a reader know exactly what it's about?

| Pattern | Example | Problem |
|---|---|---|
| Unresolved pronoun | "It features a 120Hz display" | What device? |
| Vague demonstrative | "This gives it an advantage" | What gives what an advantage? |
| Context-dependent | "The above specs outperform the competition" | Which specs? Which competition? |
| Stripped conditions | "The price has dropped significantly" | From what? To what? When? |
| Assumed knowledge | "The popular supplement helps with recovery" | Which supplement? Recovery from what? |
| Relative claim | "Our fastest-selling product" | Fastest over what period? Compared to what? |
| Specificity demotion | "Whether you need X, Y, or Z, we offer a range of options" | Specific entities buried in subordinate clause; main clause is generic filler. LLM extracts the commodity main clause, not the named types. Fix: promote specifics to main clause position |

*Healthcare mode: do not flag hedged therapeutic language as a stripped condition.*

### Check 4: Entity Completeness

*Affects Gate 1 (retrieval) and Gate 2 (ranking). Grounded in established IR principles (Turnbull).*

**Question:** Are all entities explicitly named at the right level of categorical specificity, and are relationships between entities stated?

**This check tests the page's entity graph** — does the page fully specify what things exist, what they're called, and how they connect to each other?

The distinction from Extractability (Lens 3): Extractability tests whether individual sentences survive isolation. Entity Completeness tests whether the page as a whole names all its actors and connects them. A page could have perfect extractability (no unresolved pronouns) but poor entity completeness (never names the specific product category or never states the relationship between the brand and the service).

**Categorical precision:** Retrieval systems don't just measure similarity — they also need to match, deciding whether a chunk should be included or excluded from results (Turnbull, 2026). Precise categorical language gives systems more to work with. "Semi-automatic espresso machine" is more matchable than "coffee maker." "Anterior approach hip replacement" is more matchable than "hip surgery." "Single tooth dental implant with titanium post" is more matchable than "dental implant."

**Standard mode:** Name the product/plan at the correct categorical level, state the relationship, include the target user condition, include a specific data point.

**Healthcare mode:** Name the clinic or practitioner, name the procedure at clinical specificity, name the patient condition, include compliant outcome language. Do NOT require: prices (if unpublished), clinical success rates, or guaranteed timeframes.

**Page-level entity re-anchoring check:** After assessing all sections, look for a pattern: if **three or more sections** are flagged for an Entity Completeness issue specifically because they fail to re-anchor to the primary entity (clinic, brand, practitioner) — meaning the section reads as generic educational content that any competitor could host — flag this as a **page-level entity gap** in the priority actions, not just per-section notes. The fix is a single re-anchoring sentence per affected section, not a rewrite. Generic educational content that could appear on any competitor's site is the #1 reason pages lose G2 ranking contests. Aggregate the pattern; don't bury it in section notes.

(Note: this check uses the spec's "issue / no-issue" assessment, not numerical scores. If you read older versions of this rule referring to "score below 6/10", ignore the score; trigger on the *count of sections flagged for primary-entity re-anchoring failure*.)

### Check 5: Format Appropriateness

*Affects Gate 1 (retrieval) and Gate 3 (citation).*

**Question:** Is each content type presented in the format that's easiest for both humans to scan and machines to parse?

Tables, ordered lists, and unordered lists are structurally unambiguous — a machine can parse them without interpreting natural language, and a human can scan them faster than prose. When content has a natural tabular or list structure, using prose instead forces both humans and machines to work harder to extract the same information.

**Format matches (flag as strength):**
- Comparison data in tables
- Sequential content in numbered lists
- Parallel discrete items in bullet lists
- Relational/explanatory content in well-structured paragraphs

**Format mismatches (flag as issue):**
- Comparison data written as prose across paragraphs — should be a table
- Sequential steps buried in prose — should be a numbered list
- 3+ parallel items written as a run-on sentence — should be a bullet list
- Bullet lists used for content that needs relational context — should be paragraphs

### Check 6: Natural Language Quality

*Affects Gate 2 (ranking) and Gate 3 (citation). Supported by E-GEO finding that oversimplification hurts.*

**Question:** Is the writing human and readable without being vague or robotic?

Flag both marketing fluff AND over-engineered keyword stuffing. Flag AI slop patterns: repetitive sentence openings, uniform sentence length, generic transitional phrases, absence of specific examples.

Also flag oversimplified data-point writing that strips all human readability in pursuit of density. The goal is structured language that reads naturally — not marketing prose, and not a database dump.

---

## Overall Assessment

Instead of a numerical score, the audit produces a structured summary that tells the operator the page's current state and tells the LLM writer what to fix.

### Page-level summary

After assessing all sections, produce:

1. **What's working** — list the page's strengths across all sections. These are instructions to the writer: preserve these.
2. **What needs fixing** — list all issues found, grouped by gate (Retrieval → Ranking → Citation). Each issue names the section, the specific problem, and what the fix looks like.
3. **Primary bottleneck** — which gate has the most issues? This tells the operator what category of problem dominates the page.
4. **Section integrity failures** — any section that fails topical binding, single concept, or self-containment. These need restructuring, not just rewriting.
5. **Zone 1 assessment** — Zone 1 has a real positional advantage due to first-passage retrieval bias. If Zone 1 is missing required elements (named entity, core service, target user, anchorable statement), flag this as the highest-priority fix regardless of what else is wrong.

### Severity guide

Findings are categorised by severity to help the operator and writer prioritise:

- **Critical:** Zone 1 missing required elements, off-topic sections, scope creep (sections that should be their own page), section integrity failures, condition preservation violations in regulated content, **any numeric outcome claim in healthcare/legal/financial mode without an inline qualifying condition** (see auto-escalation below), CTA blocks containing trapped trust signals not duplicated elsewhere, missing semantic H2/H3 hierarchy, page-length UNDER_BUILT verdicts. These are structural problems — the page can't compete until they're fixed.
- **Important:** Entity completeness gaps, format mismatches, missing anchorable statements, unresolved coreference, page-length OVER_BUILT verdicts, anonymous unverifiable testimonials, factually unverifiable anchorable statements (`verify_before_publish`). These reduce the page's chances of being cited.
- **Minor:** Natural language quality issues, minor density improvements, heading tweaks. These are polish — fix them after the critical and important issues.

**Healthcare / legal / financial auto-escalation rule.** In regulated mode, the following automatically escalate to **CRITICAL** regardless of where they appear on the page:
- A numeric outcome claim (e.g., "patients lose 10–20 pounds in the first month", "investors saw 12% returns", "settlement averages $250,000") that does NOT have its qualifying condition (sample size, duration, eligibility population, comparator, "results may vary" clause, etc.) within the SAME sentence.
- A claim of clinical or therapeutic efficacy without the AHPRA-style hedge ("may help", "may reduce", "results vary") in the same sentence.
- An expert credential or licence stated without the registration/licence number or issuing body.

Do not downgrade these to IMPORTANT or MINOR. Regulated-content claim violations are misinformation vectors and must be flagged at the highest severity.

### Gate diagnosis

After assessing all sections, count the findings per gate to identify the primary bottleneck. This tells the operator which *category* of problem dominates the page.

| Gate | Checks that feed it | What findings here mean |
|---|---|---|
| **G1: Retrieval** | Entity Completeness, Format Appropriateness | Content doesn't surface at all — wrong language, missing entities, format makes content unparseable |
| **G2: Ranking** | Structural Fitness, Information Density, Entity Completeness, Natural Language Quality | Content surfaces but loses to competitors — not dense enough, not differentiated, not well-structured |
| **G3: Citation** | Structural Fitness, Extractability, Format Appropriateness, Natural Language Quality | Content ranks but LLM can't confidently use it — unresolved pronouns, missing conditions, no anchorable statement |

**How to identify the bottleneck (mechanical formula):**

1. Every flagged finding maps to **exactly one** gate (G1, G2, or G3) — the spec lists which checks feed which gates in the table above. If a finding plausibly fits two gates, choose the upstream gate (G1 > G2 > G3) — fixing an upstream gate often fixes the downstream one.
2. Compute weighted score per gate:
   - Each Zone 1 finding contributes **2 points** to its gate.
   - Each Body finding contributes **1 point** to its gate.
   - Each finding marked CRITICAL contributes an additional **1 point** to its gate (regardless of zone).
3. The gate with the **highest weighted score** is the dominant bottleneck. On ties, break in order **G1 > G2 > G3** (retrieval problems block ranking; ranking problems block citation — fix upstream first).
4. Report all three gates' issue counts AND weighted scores so the bottleneck is reproducible by anyone re-running the math:

> 🚦 **Gate Diagnosis**
> G1 Retrieval: [X issues found — brief summary]
> G2 Ranking: [X issues found — brief summary]
> G3 Citation: [X issues found — brief summary]
> **Primary bottleneck:** [Gate X — the category of problem that appears most, with one-sentence explanation]

This directs the priority actions: fix the bottleneck gate first because downstream gates don't matter until the upstream gate passes.

---

## Output Format

```
📋 LLM Readability Audit
🏥 Healthcare Mode / ⚖️ Legal Mode / 💼 Financial Mode / 📚 Educational Mode / ⚙️ Standard Mode
🧭 Intent source: OPERATOR / INTENT_ANALYZER / INFERRED  (analyzer confidence: X.XX if applicable)

---

🌐 PAGE-LEVEL COMMODITIZATION
  Verdict: NOT_COMMODITIZED / PARTIALLY_COMMODITIZED / COMMODITIZED / FULLY_COMMODITIZED_AI_SLOP
  [If COMMODITIZED or FULLY_COMMODITIZED_AI_SLOP: emit a one-line summary of what the page lacks AND a one-line unique-angle recommendation. The rewriter cannot fix this with sentence-level tweaks.]
  Whole-page substitution: ✅/⚠️ | Unique-data sentences: [N] | Unique-angle present: ✅/⚠️ | External-verifiable trust signals: [N] | AI fingerprint markers: [N]
  Fail points: X / 5

---

✅ WHAT'S WORKING
- [Strength 1 — be specific so the LLM writer knows to preserve this]
- [Strength 2]
- [...]

---

🚦 GATE DIAGNOSIS  (counts must equal total findings; weighted score = Zone1×2 + Body×1 + CRITICAL×1)
  G1 Retrieval:  [X issues, weighted Y]  — [brief summary or "no issues"]
  G2 Ranking:    [X issues, weighted Y]  — [brief summary or "no issues"]
  G3 Citation:   [X issues, weighted Y]  — [brief summary or "no issues"]
  Primary bottleneck: [Gate X — one-sentence explanation, tie-break order G1 > G2 > G3]

---

🗺️ Zone Analysis
  Page length: [X characters / ~X words]  → page_length_band: UNDER_BUILT / HEALTHY / OVER_BUILT
  Estimated grounding coverage: ~X%
  Zone 1: first [X] characters (computed: min(0.20 × total, 2000), rounded to sentence end)
  Zone 1 contents: [present ✅ / missing ⚠️ — list what's present/missing from named_entity, core_service, target_user, anchorable_statement]
  Body ([N] content sections): [summary]
  ⚠️ Architecture gap: [if applicable — facts trapped in Body that should mirror to Zone 1]
  ⚠️ Section integrity issues: [if applicable]

🎯 Primary intent: [exact wording] (source: OPERATOR / INTENT_ANALYZER / INFERRED)
  H1 alignment: ✅ pass / ⚠️ MINOR (decorative framing) / ⚠️ IMPORTANT (metaphor) / ⚠️ CRITICAL (unmatchable)
  H1 quoted: "[verbatim H1]"
🎯 Secondary intents: [list]
🎯 Anchor sections (from intent-analyzer, if supplied): [list]
🎯 Drift sections (from intent-analyzer, if supplied): [list]

🎯 Intent Coverage
  | # | Query Intent | Extractable Answer? | Section | Notes |
  |---|---|---|---|---|
  | 1 | [intent] | ✅/⚠️ | [section name] | |
  ⚠️ Coverage gap: [if applicable]

🔀 Flow check:
  ✅/⚠️ Intent answered in opening
  ✅/⚠️ Credibility established early
  ✅/⚠️ Options / content in logical order
  ✅/⚠️ CTA / next step clear
  ⚠️ Flow gap: [if applicable]

🔗 Reasoning chain:
  [Query] requires: [Link 1] → [Link 2] → [Link 3] → [Link 4]
  ✅/⚠️ All links present / ⚠️ Missing: [specific link]

🏷️ Competitive Differentiation
  What: ✅/⚠️ [Named entity or missing]
  Who: ✅/⚠️ [Named provider or missing]
  What job: ✅/⚠️ [Specific outcome or missing]
  What constraint: ✅/⚠️ [Conditions/scope or missing]
  Result: PASS / PARTIAL / FAIL
  ⚠️ Substitution test: [pass/fail]

📐 Format Audit
  ✅/⚠️ Tables used where comparison data exists
  ✅/⚠️ Numbered lists used for sequential content
  ✅/⚠️ Bullet lists used for parallel discrete items
  ✅/⚠️ Paragraphs reserved for relational content
  ✅/⚠️ Headings are descriptive, query-matchable, and follow semantic hierarchy
  ⚠️ Format gap: [section + recommended change + why]
  ⚠️ Heading issue: [specific heading + problem]

🔁 DRY Check
  ✅ No significant repetition / ⚠️ Violations found:
  ⚠️ [Section] repeats [claim] from [Section]. Replace with new atomic fact.

🛡️ Trust Signals
  ✅ Present: [list]
  ⚠️ Missing: [list with recommendation]

⚓ Anchorable Statements
  Zone 1: [quote or flag missing]
  Intent coverage: [X of Y intents covered]
  ⚠️ Gap: [intent without anchorable statement + which section should contain one]

🔒 Condition Preservation
  ✅ All conditional claims self-contained / ⚠️ Violations found:
  ⚠️ [Claim] — condition in [separate location]. Merge into same sentence.

🔘 CTA Blocks Detected
  - [Section heading or first line] — Excluded from assessment. [Trapped trust signal if applicable.]
  — OR —
  None detected.

---

Section: [Name] — [Zone 1 / Body]
Integrity: ✅ / ⚠️ [which rule fails: off-topic / scope creep / single concept / self-containment]

✅ Strengths:
- [What's working in this section — preserve these]

⚠️ Issues:
- [CRITICAL/IMPORTANT/MINOR] [Gate X] [Specific problem] — [What the fix looks like]
- [...]

⚠️ Flagged sentences:
  `[Exact original sentence]`
  Issue: [specific problem — name the gate it affects]
  ✅ Rewrite: [improved, mode-compliant version]

  [1–3 flagged sentences per section max — Zone 1 sections take priority]

---

[Repeat for all content sections]

---

⚠️ ALL ISSUES (ordered by severity — Critical first, then Important, then Minor):
1. [CRITICAL] [Section] — [specific fix]
2. [CRITICAL] [Section] — [specific fix]
3. [IMPORTANT] [Section] — [specific fix]
... [List ALL findings. The LLM writer applies all of them.]

---

```json
[ JSON appendix — see "JSON Appendix Schema" below for the exact structure ]
```
```

**The audit always emits TWO things in this order:** (1) the human-readable markdown report above, then (2) a single fenced ` ```json ` block at the very end. The JSON is what `llm-rewrite` (and other downstream consumers) parse mechanically. Both are required. No prose may follow the closing JSON fence.

---

## JSON Appendix Schema

The JSON appendix is the machine contract between this audit and downstream rewriters. Every audit must end with a single fenced ` ```json ` block that conforms exactly to this schema. Field names, nesting, and enum values are stable. Do not invent new top-level fields. Do not rename fields. Use `null` (not omission) when a value is genuinely unavailable.

### Enum values (use literally — no synonyms)

- `severity`: `"CRITICAL"` | `"IMPORTANT"` | `"MINOR"`
- `gate`: `"G1"` | `"G2"` | `"G3"`
- `industry_mode`: `"STANDARD"` | `"HEALTHCARE"` | `"LEGAL"` | `"FINANCIAL"` | `"EDUCATIONAL"`
- `page_type`: `"service"` | `"location"` | `"blog"` | `"comparison"` | `"landing"` | `"emergency"` | `"educational"`
- `page_length_band`: `"UNDER_BUILT"` | `"HEALTHY"` | `"OVER_BUILT"`
- `intent_source`: `"OPERATOR"` | `"INTENT_ANALYZER"` | `"INFERRED"`
- `commoditization_verdict`: `"NOT_COMMODITIZED"` | `"PARTIALLY_COMMODITIZED"` | `"COMMODITIZED"` | `"FULLY_COMMODITIZED_AI_SLOP"`
- `protection_type`: `"AHPRA_HEDGING"` | `"LEGAL_DISCLAIMER"` | `"LEGAL_LOCATION"` | `"FDA_DISCLAIMER"` | `"FINANCIAL_DISCLOSURE"` | `"COMPLIANCE_OTHER"`
- `check`: `"structural_fitness"` | `"information_density"` | `"extractability"` | `"entity_completeness"` | `"format_appropriateness"` | `"natural_language_quality"` | `"section_integrity"` | `"anchorable_statement"` | `"condition_preservation"` | `"dry"` | `"trust_signals"` | `"competitive_differentiation"` | `"commoditization"` | `"heading_hygiene"` | `"trapped_signal"`
- `issue_type`: short SCREAMING_SNAKE_CASE token chosen from `MISSING_ANCHORABLE_STATEMENT` | `OFF_TOPIC_SECTION` | `SCOPE_CREEP` | `CONDITION_SEPARATED` | `UNRESOLVED_PRONOUN` | `FILLER_OPENER` | `SUBSTITUTION_TEST_FAILED` | `DRY_VIOLATION` | `MISSING_ENTITY_CREDENTIAL` | `H1_DECORATIVE` | `H1_UNMATCHABLE` | `MISSING_SEMANTIC_HEADINGS` | `TRAPPED_TRUST_SIGNAL` | `ANONYMOUS_TESTIMONIAL` | `VERIFY_BEFORE_PUBLISH` | `CONDITION_DUPLICATION_REQUIRED` | `INFORMATION_DENSITY_LOW` | `FORMAT_MISMATCH` | `INSUFFICIENT_DIFFERENTIATION` (extend only by appending new SCREAMING_SNAKE_CASE tokens; existing tokens are stable).

### Required top-level shape

```json
{
  "schema_version": "1.0",
  "audit_timestamp": "2026-05-10T10:00:00Z",
  "audit_metadata": {
    "source_url": "https://www.example.com/page",
    "primary_intent": "string — exact wording supplied by operator, copied from the intent-analyzer's discovered_intent.primary, or inferred",
    "intent_source": "OPERATOR",
    "intent_analyzer_confidence": null,
    "anchor_sections_from_analyzer": [],
    "drift_sections_from_analyzer": [],
    "industry_mode": "HEALTHCARE",
    "page_type": "blog",
    "page_length_chars": 4200,
    "page_length_band": "HEALTHY",
    "estimated_grounding_coverage_pct": 66
  },
  "gate_diagnosis": {
    "G1_retrieval": { "issue_count": 2, "weighted_score": 4 },
    "G2_ranking":   { "issue_count": 9, "weighted_score": 14 },
    "G3_citation":  { "issue_count": 4, "weighted_score": 6 },
    "dominant_gate": "G2",
    "bottleneck_summary": "Page surfaces but loses to competitors — generic claims, no unique angle, no specific outcomes data."
  },
  "zone_analysis": {
    "zone_1_chars": 840,
    "zone_1_present": ["named_entity", "core_service"],
    "zone_1_missing": ["target_user_specific", "anchorable_statement"],
    "body_section_count": 8,
    "section_integrity_failures": []
  },
  "commoditization_check": {
    "whole_page_substitution_passes": false,
    "unique_data_sentence_count": 1,
    "unique_angle_present": false,
    "external_verifiable_trust_signal_count": 0,
    "ai_fingerprint_marker_count": 6,
    "fail_points": 5,
    "verdict": "FULLY_COMMODITIZED_AI_SLOP",
    "unique_angle_recommendation": "Lead with Dr. Sattele's specific protocol stages (e.g. evaluation → physician-approved suppressant → bi-weekly hormone monitoring) and patient-population eligibility criteria — these are present nowhere on the page in concrete form."
  },
  "intent_coverage": [
    {
      "intent": "What is medically supervised weight loss and why is it safer than DIY dieting?",
      "is_primary": true,
      "extractable_answer_present": false,
      "section_name": null,
      "gap_reason": "page describes the concept generically but provides no anchorable statement that names Dr. Sattele's program AND distinguishes it"
    }
  ],
  "competitive_differentiation": {
    "what":            { "present": true,  "evidence": "medically supervised weight loss program" },
    "who":             { "present": true,  "evidence": "Dr. Sattele's Rapid Weight Loss Centers" },
    "what_job":        { "present": false, "evidence": null },
    "what_constraint": { "present": false, "evidence": null },
    "result": "PARTIAL",
    "extractable_3_sentence_window": null,
    "substitution_test_passed": false,
    "monopoly_market_bypass": false,
    "skipped_educational_mode": false
  },
  "format_audit": {
    "tables_used_appropriately": false,
    "lists_used_appropriately": "OVERUSED_AT_EXPENSE_OF_PROSE",
    "headings_query_matchable": false,
    "heading_issues": [
      { "heading": "Beyond the Diet: Why Medical Supervision Matters for Safe, Lasting Weight Loss", "problem": "decorative_framing_prefix" },
      { "heading": "The Bottom Line: It's Not Just About Weight—It's About Health", "problem": "creative_metaphor" }
    ]
  },
  "dry_violations": [
    {
      "section_name": "The Bottom Line",
      "repeated_claim": "medical supervision works with your body",
      "first_section": "What Does Medically Supervised Really Mean?",
      "rewrite_action": "delete or replace with a section-specific atomic fact"
    }
  ],
  "trust_signals": {
    "present": ["named_provider"],
    "missing": ["practitioner_credential_number", "named_technology", "specific_outcome_data_with_n", "named_external_source", "years_of_operation"]
  },
  "anchorable_statements": {
    "zone_1_anchorable_present": false,
    "zone_1_anchorable_quote": null,
    "intent_anchorable_count": 0,
    "intent_anchorable_total": 1,
    "gaps": [
      { "intent": "primary", "should_appear_in_section": "Zone 1 / opening" }
    ]
  },
  "condition_preservation": {
    "violations": [
      {
        "claim_quote": "Patients often lose 10–20 pounds in the first month, with some losing up to 30 pounds or more",
        "missing_condition": "sample size, study duration, patient population, AHPRA-style 'individual results vary' hedge",
        "fix_instruction": "merge inline: 'Among Dr. Sattele's supervised patients, [DATA_NEEDED: cohort size and timeframe], typical losses range from 10–20 pounds in the first month, though individual results vary based on health status and adherence.'"
      }
    ]
  },
  "cta_blocks_detected": [
    {
      "section_name": "Ready for Real Change? Let's Talk.",
      "trapped_signal": null,
      "excluded_from_assessment": true
    }
  ],
  "protected_sections": [
    {
      "section_id": "footer_disclaimer",
      "section_name": "Disclaimer",
      "protection_type": "FDA_DISCLAIMER",
      "original_text": "Compounded Semaglutide is not FDA-approved, meaning its safety, efficacy, and quality are not verified by the FDA. Use of compounded medications involves potential risks and should be discussed with a qualified healthcare provider.",
      "rewrite_permissions": {
        "can_delete": false,
        "can_shorten": false,
        "can_relocate": true,
        "can_rewrite_for_clarity": false,
        "must_preserve_meaning": true
      },
      "rewriter_instruction": "Preserve verbatim. May be relocated within the page but must not be paraphrased, shortened, or removed."
    }
  ],
  "findings": [
    {
      "id": "find_001",
      "severity": "CRITICAL",
      "gate": "G3",
      "section_name": "Faster Results, Healthier Outcomes",
      "check": "condition_preservation",
      "issue_type": "CONDITION_SEPARATED",
      "flagged_sentence": "Patients often lose 10–20 pounds in the first month, with some losing up to 30 pounds or more",
      "rewrite": "Among Dr. Sattele's supervised patients [DATA_NEEDED: cohort size and timeframe], typical first-month weight loss is 10–20 pounds, with some patients losing up to 30 pounds; individual results vary based on health status and adherence.",
      "rationale": "Healthcare-mode auto-escalation: numeric outcome claim with no inline qualifying condition is a misinformation vector and must merge the AHPRA-style hedge into the same sentence."
    }
  ],
  "rewrite_brief": {
    "dominant_gate_focus": "G2",
    "target_length_chars_min": 4500,
    "target_length_chars_max": 7000,
    "keep_sections": ["What Does Medically Supervised Really Mean?", "The Hidden Risks of DIY Dieting", "Disclaimer"],
    "merge_sections": [
      { "from": "Accountability, Support, and Personalization", "into": "Safety First: Why Physician Oversight Protects Your Health" }
    ],
    "cut_sections": ["The Bottom Line: It's Not Just About Weight—It's About Health"],
    "primary_focus": "Replace generic medical-supervision platitudes with Dr. Sattele's named protocol and patient-population specifics. Add an anchorable statement to Zone 1 that passes the substitution test. Merge AHPRA hedges into every numeric outcome claim.",
    "unique_angle_recommendation": "Lead with Dr. Sattele's named protocol (testing → physician-approved suppressant → bi-weekly monitoring) plus eligibility criteria (e.g. BMI range, comorbidity inclusion). The page currently lists capabilities; the rewrite should commit to a specific methodology no competitor lists.",
    "do_not_do": [
      "Do not strip the FDA disclaimer about Compounded Semaglutide.",
      "Do not invent specific patient outcome numbers (n, %, success rate) the page does not currently contain — use [DATA_NEEDED:] placeholders and the operator_fact_requests array.",
      "Do not soften AHPRA-style hedges to make claims read as more confident."
    ]
  },
  "operator_fact_requests": [
    {
      "field": "Dr. Sattele's medical credentials and registration/licence number",
      "reason": "Required for healthcare-mode trust signals; absent on page."
    },
    {
      "field": "Specific cohort data behind '10–20 pounds in the first month' (sample size, study duration, patient inclusion criteria)",
      "reason": "Required for healthcare-mode condition preservation; without this the rewrite uses [DATA_NEEDED:] placeholders."
    },
    {
      "field": "Named protocol stages and any standardised testing protocol (e.g. fasting insulin, TSH panel, body composition method)",
      "reason": "Required for unique-angle commitment to break commoditization; the page implies these exist but does not name them."
    }
  ]
}
```

### Schema rules

1. The JSON appendix is **always emitted**, even when no issues are found. In a clean page, `findings` is an empty array, `gate_diagnosis.G[1-3].issue_count` are zero, `commoditization_check.verdict` is `"NOT_COMMODITIZED"`.
2. **Do not omit fields** to indicate "not applicable". Use `null` for genuinely unavailable scalars and empty arrays `[]` for empty collections.
3. **Every finding must populate every field** (`id`, `severity`, `gate`, `section_name`, `check`, `issue_type`, `flagged_sentence`, `rewrite`, `rationale`). If `flagged_sentence` is genuinely null (the issue is structural, not sentence-level), use `null` and explain in `rationale`.
4. The `rewrite` field is the literal string the writer pastes in. If the sentence should be deleted, use `"[DELETE]"` and explain in `rationale`.
5. The `rewrite_brief.target_length_chars_min` and `_max` reflect the Page Length Bands table, scaled to the page type.
6. Emit valid JSON. The block must parse with a standard `json.loads()` call without manual cleanup. Do not include comments. Do not use trailing commas. Do not use single quotes.

---

## Output Discipline Rules

These rules are non-negotiable for cross-LLM consistency. Apply them before emitting the audit.

1. **Section order is fixed.** Produce the markdown sections in the exact order shown in the Output Format template above. Do not invent additional sections. Do not rename headings. Do not split or merge sections.
2. **Both formats are mandatory.** Every audit emits the human-readable markdown FIRST and the JSON appendix SECOND, separated by `---` and a fenced ` ```json ` block. No prose may appear after the closing JSON fence.
3. **Enums are literal.** Severity, gate, industry_mode, page_type, page_length_band, intent_source, commoditization_verdict, protection_type, check, and issue_type are enums with the exact values listed above. Do not output synonyms. Do not lowercase severity. Do not write `"G2_ranking"` instead of `"G2"`.
4. **Quote, do not paraphrase.** The `flagged_sentence` field and any `original_text` field must be a verbatim substring of the input page. If you cannot quote it, do not flag it.
5. **Markdown "ALL ISSUES" and JSON `findings[]` must be a 1-to-1 mirror.** This is non-negotiable.
   - Every numbered item in the markdown's ALL ISSUES list corresponds to exactly one object in JSON `findings[]`.
   - The order is the same in both.
   - The severity tag in the markdown line (`[CRITICAL]`, `[IMPORTANT]`, `[MINOR]`) matches the `severity` field of the matching JSON object.
   - The gate tag in the markdown line (`[G1]`, `[G2]`, `[G3]`) matches the `gate` field of the matching JSON object.
   - **Do not** flag an issue in the markdown without a corresponding JSON entry. **Do not** add a JSON finding the markdown doesn't list. Count them before emitting — if the counts differ, fix the audit.

6. **Apply the gate-attribution rule mechanically.** Every finding maps to exactly one gate. Then:
   - `len(findings)` = total findings emitted in the JSON `findings[]` array.
   - `gate_diagnosis.G1_retrieval.issue_count` = the number of `findings[]` objects whose `gate == "G1"`. **Same for G2 and G3.**
   - **Sum check:** `G1.issue_count + G2.issue_count + G3.issue_count` MUST equal `len(findings)`. If they do not, the gate-attribution is wrong — fix it before emitting.
   - Do NOT count "general audit observations" in `gate_diagnosis.issue_count` separately from `findings[]`. The fields measure the same set of items, just bucketed by gate.
   - The `bottleneck_summary` names the gate with the highest weighted score (Zone 1 ×2 + Body ×1 + CRITICAL ×1) and quotes a one-line explanation.
7. **Healthcare-mode auto-escalation is mechanical.** Numeric outcome claims without an inline AHPRA-style hedge automatically receive `severity: "CRITICAL"` regardless of zone. Do not downgrade. Do not negotiate.
8. **Mode-aware preservation.** Sections marked as `protected` in `protected_sections[]` must NOT generate findings in `findings[]` and must NOT be subjected to the six checks. They are listed in the per-section markdown as "N/A — protected" and recorded in the JSON with their `rewrite_permissions`.
9. **Determinism over creativity.** When the rubric gives a binary test, apply it. Do not write "this section feels weak" — write "the opener fails the 3-element filler test (0/3 elements present)".
10. **No preamble or closing summary.** The first character of the audit output is the emoji header `📋`. The last character is the closing ` ``` ` of the JSON fence.

11. **No outer fence around the response.** The audit response must NOT be wrapped in any outer code fence (no leading ` ```markdown `, no leading ` ``` `, no leading ` ```text `). The markdown body is plain markdown. The ONLY fence in the response is the inner ` ```json ` block at the end. If you find yourself starting your output with three backticks before the 📋 header, delete them.

12. **Findings count check before emitting.** Before producing the JSON appendix, count the items in the markdown ALL ISSUES list. The JSON `findings[]` array MUST have the same length. The sum of `gate_diagnosis.G[1-3].issue_count` MUST equal that same length. If any of these three numbers disagree, the audit is wrong — re-audit before emitting. Do not emit a known-broken parity.

13. **Derive `gate_diagnosis.issue_count` from `findings[]`, never hand-author it.** Before writing `gate_diagnosis.G1_retrieval.issue_count`, count how many objects in `findings[]` have `gate == "G1"`. That count is the value. Repeat for G2 and G3. Do NOT independently estimate the counts based on "audit observations" or markdown-section impressions — that is the source of off-by-one errors. The triple `(G1_count, G2_count, G3_count)` is a literal `Counter(f["gate"] for f in findings).most_common()` projection.

14. **H1 alignment markdown↔JSON parity.** If the markdown body asserts an H1 alignment severity (✅ pass / ⚠️ MINOR / ⚠️ IMPORTANT / ⚠️ CRITICAL), the JSON `findings[]` array MUST contain a corresponding object whose `section_name` quotes the actual H1 verbatim, `check == "heading_hygiene"`, `issue_type == "H1_DECORATIVE"` (or `"H1_UNMATCHABLE"` for the CRITICAL case), and `severity` equal to the markdown's verdict. The only exception: if markdown says ✅ pass, no JSON entry is required (passes are not findings). Do not assert a severity in markdown without a matching JSON finding — the rewriter must be able to act on the H1 issue from the JSON alone.

15. **No reasoning artifacts in the audit body.** The audit output must read as a final deliverable, not a stream of thought. Do NOT include text like `Correction:`, `Withdrawing the flag.`, `Actually, on second look...`, `Let me re-check...`, or any other meta-commentary about your own audit process. If you change your mind mid-audit, silently revise — the published output is the final answer. The rewriter consumes the audit as authoritative; visible self-correction undermines that.

16. **Verify-inline-first before flagging condition preservation.** Before emitting a `condition_preservation` finding, read the ENTIRE sentence (not just the numeric clause) plus the sentence immediately preceding it. If the qualifying condition is already present in either, do NOT flag — the condition is preserved. Common false-positive pattern: a sentence like "Texas caps the bondsman's fee at 15 percent of the bail amount or $50, whichever is higher" already contains both bounds and the comparator inline. Re-read the full sentence before flagging.

17. **Domain-appropriate format suppression.** When `industry_mode == "LEGAL"` AND `commoditization_check.external_verifiable_trust_signal_count >= 5`, do NOT count parallel-structure tables (e.g., a comparison table of statute references, jurisdictions, fees, or timelines with consistent column headers) as AI fingerprint markers in the Commoditization check. Legal explainers legitimately use parallel tables — punishing them produces false positives. The same exemption applies to `industry_mode == "FINANCIAL"` for parallel disclosure tables. The other AI fingerprint markers (em-dashes as primary punctuation, AI-signature transitions, parallel-structure prose pile-ups, gerund+abstract-noun headings, uniform sentence-length blocks) still count normally.

18. **Markdown gate-diagnosis header is computed LAST, not first.** The markdown gate diagnosis block (`G1 Retrieval: [N issues, weighted Y]` lines near the top of the report) must reflect the FINAL count of findings after the section-by-section sweep is complete. Do NOT write the gate header during the page-level summary phase using a preview count, then forget to update it after the section-by-section sweep adds more findings. The recommended order:
    1. Run all checks and section-by-section assessment.
    2. Build the JSON `findings[]` array.
    3. Count `findings[].gate` to derive `gate_diagnosis.G[1-3].issue_count`.
    4. ONLY THEN write the markdown gate-diagnosis header using the same numbers.
    The markdown gate header counts MUST equal the JSON `gate_diagnosis` counts MUST equal the per-gate count of `findings[]`. All three numbers come from the same source — the finalised findings array — so they cannot disagree without a bug. If they disagree, you wrote the markdown before the audit was finished.

---

## Worked Examples — Calibration Library

These examples disambiguate the most variance-prone judgment calls. Apply them as calibration anchors when in doubt about a check.

### Example 1 — Anchorable Statement vs Marketing Slogan
*Calibrates: Anchorable Statement test, substitution test*

**FAIL.** "We offer competitive pricing and flexible terms on all of our dental implant options so you can smile with confidence."
*Why fail: zero named entities specific to the source, zero data points, fails substitution (any clinic could write this).*

**PASS.** "Odin House Dental Surgery in Innaloo provides single-tooth titanium implants for Westminster patients starting from $3,500, pending jawbone density."
*Why pass: 4 differentiation signals in one sentence (named clinic, named procedure, named target population, named price + condition). Substitution test fails — replace "Odin House Dental Surgery" with "any local clinic" and the specifics break.*

**Common false positive to avoid.** "Medical supervision in weight loss means your plan is overseen by licensed healthcare professionals" reads as a definition but is NOT anchorable — it's generic; replace "medical supervision" with "our program" and any clinic can host the same line. Reject.

### Example 2 — Scope Creep vs Adjacent Reference
*Calibrates: Section integrity (topical binding), 250-word split test*

**FAIL.** A 400-word section titled "Dentures vs Bridges vs Implants — A Complete Comparison" inside a page targeting "dental implants Westminster". Three full paragraphs on denture care + a paragraph on bridge longevity.
*Why fail: 400 words > 250-word threshold AND fully answers a distinct query ("dentures vs bridges"). It's a mini-page within the page; flag as scope creep, recommend its own page.*

**PASS.** "Patients lacking sufficient jawbone for dental implants at Odin House may be eligible for custom dental bridges or removable dentures as alternatives — see our [bridges page] for the full comparison."
*Why pass: 25 words, references the adjacent topic without competing for the comparison query. Stays focused on implants.*

### Example 3 — In-Sentence Pronoun Resolution (false-positive prevention)
*Calibrates: Extractability (Check 3) — coreference test*

**FALSE FLAG (do not flag).** "Dr Yap performs all of his surgeries in-house using a CBCT cone-beam scanner."
*Why this looks flaggable but isn't: "his" has a clear antecedent — "Dr Yap" — within the same sentence. Pronouns ARE allowed when their antecedent is in-sentence.*

**TRUE FLAG.** "He performs all of his surgeries in-house using a CBCT cone-beam scanner."
*Why fail: "He" has no in-sentence antecedent. This sentence retrieved alone tells a reader nothing about who "he" is.*

The rule is binary: **a pronoun is fine if its antecedent appears in the same sentence; a pronoun fails if the antecedent is in a different sentence or paragraph.** Do not flag in-sentence pronouns.

### Example 4 — Condition Preservation in Healthcare (preserve hedge while merging)
*Calibrates: Condition preservation, healthcare auto-escalation*

**FAIL.** "Patients often lose 10–20 pounds in the first month, with some losing up to 30 pounds." [Disclaimer footer: *Individual results vary based on health status and adherence.*]
*Why fail: numeric outcome claim with stripped condition + the AHPRA-style hedge is in a different section. Healthcare-mode auto-escalation → CRITICAL.*

**PASS.** "Among Dr. Sattele's medically supervised patients [DATA_NEEDED: cohort size and timeframe], typical first-month weight loss is 10–20 pounds (some patients losing up to 30 pounds), though individual results vary based on health status and adherence."
*Why pass: numeric claim, qualifying conditions, AND the AHPRA hedge are all inside the same sentence. The hedge is preserved verbatim — not softened. Specific numbers the page didn't supply are placeholdered, not invented.*

### Example 5 — Filler Opener (delete recursive padding)
*Calibrates: Information Density opener test (3-element rule)*

**FAIL.** Section heading: "Dental Implant Costs". Opening sentence: "Understanding the costs associated with dental implants is an important part of your medical journey."
*Why fail: 0 of 3 elements present (no named entity not in heading, no specific data point, no stated condition). Score: CRITICAL filler. Action: delete entirely.*

**PASS.** Section heading: "Dental Implant Costs". Opening sentence: "A standard single-tooth implant procedure at Odin House costs $3,500–$7,000, with the upper end reflecting cases requiring bone grafting."
*Why pass: 3 of 3 elements (named clinic, named price range, named condition). The opener IS the answer; no recursive padding.*

### Example 6 — CTA with Trapped Trust Signal
*Calibrates: CTA detection + trapped-signal flagging*

**Section text.** "Ready to restore your smile? Book your free consultation today with our team of 20-year veterans."
*Diagnosis: matches CTA criteria (action phrase, 1-3 sentences, sits between content sections, would render as a button). BUT contains a unique trust signal ("20-year veterans") that may not be duplicated elsewhere. Action: classify as CTA AND emit `trapped_signal` finding (severity IMPORTANT). The rewriter relocates "20 years of clinical experience at Odin House" into a body section before the rewrite finalises.*

### Example 7 — DRY: Synonym Cycling vs Re-anchoring
*Calibrates: DRY check, new-attribute disambiguation*

**FAIL (synonym cycling).** Section A: "Our team of experts will guide you." Section B: "Our skilled professionals work with you." Section C: "Our experienced practitioners are here to help."
*Why fail: three labels for the same claim with zero new attributes. None of "experts / skilled professionals / experienced practitioners" introduces a credential, technology, location, year, or scope.*

**PASS (re-anchoring).** Section A: "Dr Yap, principal dentist at Odin House." Section B: "Dr Yap performs all surgeries in-house using a CBCT cone-beam scanner." Section C: "Dr Yap completed his AHPRA-registered specialist training in 2008 and has placed over 1,200 implants."
*Why pass: each repeat of "Dr Yap" introduces a new attribute (in-house surgery, named technology, registration year, case count). Three mentions, three new facts.*

### Example 8 — H1 Substitution Check
*Calibrates: H1 alignment severity matrix*

Apply the matrix from Step 3 mechanically. Use these pinned verdicts as calibration anchors — when an H1 looks like one of these patterns, copy the verdict.

**Pattern: decorative prefix + query language present after the colon.** H1: "Beyond the Diet: Why Medical Supervision Matters for Safe, Lasting Weight Loss" — page targets "medically supervised weight loss program".
*Verdict: ⚠️ **MINOR** — strip the framing. Reasoning: "Beyond the Diet:" is decorative, but stripping it leaves "Why Medical Supervision Matters for Safe, Lasting Weight Loss" which contains the categorical query language ("medical supervision", "weight loss"). The H1 is recoverable with a one-line edit. Severity = MINOR is the canonical answer for decorative-prefix-but-recoverable. Do NOT escalate to IMPORTANT or CRITICAL.*

**Pattern: thesis statement, not a query.** H1: "Why Doctor-Led Programs Deliver Safer, Lasting Results"
*Verdict: ⚠️ **IMPORTANT** — Gate 1 retrieval signal damaged. Reasoning: contains the topic obliquely ("doctor-led programs") but is phrased as a thesis a content writer would write, not a query a user would type. Recoverable but the rewrite is not just stripping a prefix.*

**Pattern: pure metaphor, no query language.** H1: "Your Journey to a Healthier Tomorrow" — page targets "dental implants Westminster WA".
*Verdict: ⚠️ **CRITICAL** — H1 unmatchable to any query. Reasoning: zero query language anywhere; topic ("dental implants") absent; abstract-noun framing only.*

**Pattern: pass.** H1: "Medically Supervised Weight Loss Programs in Charlotte, NC"
*Verdict: ✅ **PASS**. Reasoning: contains primary categorical query language, entity qualifier (location), reads as a literal search query.*

**Decision rule when uncertain:** If the H1 matches BOTH a decorative-prefix pattern AND retains query language after stripping, severity is MINOR. If query language is fully absent, severity is CRITICAL. There is no "this H1 feels like maybe IMPORTANT" — pick the matrix row that best matches the pattern.

**Counter-example (do NOT do this).** Tempting wrong rationale: "Decorative prefix dilutes retrieval signal; strip to query-matchable core — therefore IMPORTANT." This rationale escalates above the pinned verdict. The pinned verdict for decorative-prefix-but-recoverable is **MINOR**, full stop. Yes, the prefix dilutes signal. Yes, stripping it improves retrieval. That is exactly why the verdict is MINOR (small, recoverable fix), not IMPORTANT (substantial damage). Do not let the strength of the underlying logic talk you out of the matrix.

**Counter-example.** Tempting wrong rationale: "The H1 is the highest-weighted on-page heading, therefore any issue with it is IMPORTANT or CRITICAL by default." This conflates H1 IMPORTANCE-of-position with severity-of-this-specific-defect. A small recoverable defect on a high-weight element is still a small recoverable defect. Use the matrix row, not the heading's structural rank.

---

## Instructions

1. **Resolve the primary search intent FIRST.** Use the highest-fidelity source available, in this order: (a) an upstream `page-intent-analyzer` report (record `intent_source: "INTENT_ANALYZER"` and copy the analyzer's confidence + anchor/drift sections); (b) an operator-supplied intent string (`OPERATOR`); (c) inferred from URL slug + H1 + title, only if the runner explicitly authorises inference (`INFERRED`). If none of the three is available, halt and emit `INTENT_REQUIRED`. Never silently fabricate the intent — the entire audit anchors to it.
2. Read the full page before assessing anything. Detect industry mode (Step 1).
3. Compute Zone 1 mechanically (Step 2): count visible body characters, take `min(0.20 × total, 2000)` rounded up to the next sentence end, and record the exact number.
4. Run Steps 1–9 in order (mode, zone analysis + page-length band, flow/intents, differentiation + page-level commoditization, format, DRY, trust signals, anchorable + condition preservation, CTA detection) before section assessment. Page-level issues outrank sentence-level issues in priority.
5. Identify and exclude CTA blocks before assessing sections (Step 9). Inspect each CTA for trapped trust signals; flag with `TRAPPED_TRUST_SIGNAL` if a unique signal is found.
6. Label each content section as Zone 1 or Body. Assess each section against the three section integrity rules (topical binding, single concept, self-containment). When an upstream intent-analyzer report is supplied, use its `anchor_sections` / `drift_sections` to short-circuit the topical-binding assessment (anchors pass automatically; drifts fail automatically).
7. For each section, list specific strengths (what to preserve) and specific issues (what to fix). Every issue names the gate it affects, the check it belongs to, and what the fix looks like. Categorise each issue as Critical, Important, or Minor using the severity guide — and apply the **healthcare/legal/financial auto-escalation rule** mechanically (numeric outcome claims without inline qualifying conditions in regulated mode → CRITICAL).
8. Apply the gate-attribution rule mechanically: every finding maps to exactly one gate. Compute the weighted score per gate (Zone 1 ×2, Body ×1, +1 for CRITICAL) and report the dominant bottleneck.
9. Flag the highest-impact sentences per section for rewrite (max 3 per section). Zone 1 sentences take priority over Body sentences regardless of issue type. Apply the sentence-flagging priority order from Step 10.
10. Rewrites must be mode-compliant. In healthcare/legal/financial mode preserve all hedged language verbatim. When the original is too vague AND the page does not provide specific data anywhere, **never invent specifics** — use the placeholder pattern `[DATA_NEEDED: <what is missing>]` and add a corresponding entry to `operator_fact_requests`. Inventing facts is a hallucination vector and is forbidden in every mode.
11. Do not push rewrites toward oversimplification. Dense, condition-preserving prose is the goal — not stripped-down data points.
12. List ALL findings in the markdown's "ALL ISSUES" list, ordered by severity (Critical → Important → Minor). Every finding must also appear in the JSON `findings[]` array — the two must agree exactly (same count, same severities, same gates).
13. **Always emit the JSON appendix** at the end of the report, fenced as ` ```json `. Even on a clean page, emit the schema with empty arrays and zero counts. The JSON must parse with `json.loads` without manual cleanup.
14. The output is input for an LLM writer. Every finding must be specific enough that the writer can act on it without additional context. "Improve density" is not actionable. "Section X opener fails the 3-element filler test (0 of 3 elements present); delete the sentence and lead with the next fact" is actionable.
15. Keep the tone professional and direct — this is a technical audit, not a critique.
16. If the page-level Commoditization check returns `COMMODITIZED` or `FULLY_COMMODITIZED_AI_SLOP`, say so directly at the TOP of the markdown summary (above the gate diagnosis). The single highest-leverage fix is at the page level — the rewriter cannot fix commoditization with sentence-level tweaks.

---

## Quick-Reference Checklist

For content creators to verify before publishing. This is the minimum bar — not a substitute for a full audit.

- [ ] The single most important claim appears in the first 2,000 characters (or first 20% if shorter), and contains a named entity + specific data + stated condition
- [ ] Every section answers a sub-question of the primary search intent — no off-topic sections, no sections > 250 words covering an independently-searchable adjacent query
- [ ] Every section covers one concept/question, not two (single concept)
- [ ] Every section makes sense if pulled out of the page with no surrounding context (self-containment); the primary entity is re-anchored within each section
- [ ] Every pronoun's antecedent is in the SAME sentence — not "in the previous paragraph" or "in the heading"
- [ ] Every claim with a number includes its source, timeframe, and population in the same sentence; in healthcare/legal/financial mode the AHPRA-style hedge is in the same sentence too
- [ ] The page uses at least 2–3 content formats appropriately (table for comparison, list for parallel items, prose for narrative)
- [ ] Every heading contains query-matching language — not a metaphor, not "Understanding the Importance of...", not gerund + abstract noun
- [ ] At least one sentence per section is directly quotable — specific, self-contained, condition-preserving, and passes the substitution test
- [ ] Two or more mentions of the same entity each add a NEW attribute (credential, location, technology, year, scope) — not just synonym cycling
- [ ] Conditions and caveats share a sentence with the claims they qualify
- [ ] The whole-page substitution test: replacing the brand name throughout breaks the page — it doesn't read as a generic article a competitor could host
- [ ] The page identifies what it is, who it's for, what job it does, and what constraint it wins under — within a 3-sentence contiguous window
- [ ] The page commits to a unique angle (named methodology, specific protocol, contrarian stance, specific case data) — not just "personalised" / "expert" generic claims