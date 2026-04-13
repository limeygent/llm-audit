---
name: llm-readability-audit
description: Audits website copy for LLM readability, extractability, and AI search visibility. Use this skill whenever a user wants to audit, score, check, or improve web page copy for AI search, GEO, LLM readability, machine readability, or AI visibility. Also use when a user pastes any page content and asks if it is well-structured, dense enough, or LLM-friendly. Triggers on phrases like "audit this copy", "check this page", "is this LLM-ready", "score my content", "AI slop check", or any time a page is pasted for review. Always use this skill even if the request is phrased casually. This skill is standalone — it has no dependencies and does not require the intent analyzer or any other skill to run first.
---

# LLM Readability Audit

## Objective

Audit existing web page content and produce a structured report that an LLM writer can use as direct instructions to rewrite the page for AI citation — getting the page's content chunks retrieved, ranked above competitors, and cited in AI-generated answers (Google AI Overviews, ChatGPT, Perplexity, Bing Copilot) while keeping it readable and scannable for human visitors.

### The problem this solves

Most web content was written for human readers browsing a full page in order. AI systems don't read pages — they chunk them, embed them, and retrieve individual sections in isolation. A page that reads well top-to-bottom can fail completely when its sections are pulled apart: pronouns have no referent, claims have no context, entities aren't named, and generic marketing copy is indistinguishable from every competitor.

This audit identifies exactly where and why content fails when chunked, and produces actionable findings that feed directly into a rewriting workflow.

### Scope

Local B2C service businesses — dental, trades, legal, allied health, emergency services, and similar. The audit covers service pages, location pages, and supporting blog content. It is not designed for e-commerce product pages, SaaS landing pages, or enterprise B2B content.

### How the output is used

The audit report is the **input for an LLM writer** that rewrites the page. The report must therefore be:

1. **Specific enough to act on** — every finding names the exact section, the exact problem, and what the fix looks like
2. **Prioritised** — the actions list is ordered so the writer tackles the highest-impact fixes first (Zone 1 issues → section integrity issues → per-section content fixes)
3. **Non-contradictory** — findings must not conflict with each other; the writer should be able to apply all of them
4. **Mode-aware** — healthcare compliance constraints, legal disclaimers, and industry-specific hedging are flagged as protected so the writer doesn't strip them

The gate diagnosis and strengths/issues summary tell the operator (you) where the page stands and what category of problem dominates. The section-by-section findings and rewrites tell the LLM writer exactly what to change.

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
| Zone 1 | First ~20% | 2x | Dense atomic facts — answers primary intent immediately. Benefits from first-passage retrieval bias. |
| Body | Remaining ~80% | 1x | All other content sections. Each section competes independently on content quality, not position. |

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

**The split test:** If a section is 3+ paragraphs answering a distinct query that someone would search for independently, it's a candidate for its own page. A brief mention or summary table is fine; a full treatment is scope creep that dilutes both pages (this one and the dedicated one you should have instead).

**2. Single concept** — One section answers one question or covers one concept. If a section covers both "how long do implants last" and "what do implants cost", those are two different queries competing in the same chunk. An LLM retrieving this chunk for a cost query gets diluted by longevity content, and vice versa. Split them.

**3. Self-containment** — The section makes complete sense pulled out of the page entirely. No "as mentioned above", no pronouns pointing to a previous section, no assumed context from earlier content. A reader (or retrieval system) landing on just this section gets a complete answer. The primary entity must be re-anchored within the section so the chunk identifies who/what it's about without needing the page title or preceding sections.

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

**Page length check:** Assess whether the page length is appropriate for the intent complexity. Flag if the page is significantly over-built for a simple informational intent, or under-built for complex commercial investigation. Note the approximate character count and estimated coverage percentage.

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

**Always ask the operator.** Before running the audit, ask: "What search query or intent is this page targeting?" The operator knows why the page exists. Do not guess from the content — if the content accurately reflected the intent, it probably wouldn't need auditing.

If the operator provides a URL without stating the intent, ask before proceeding. The entire audit anchors to this — getting it wrong wastes the whole assessment.

**Validate the stated intent against the page content.** After reading the page, check whether the stated intent is too narrow or too broad for what the page actually contains:

- **Too narrow:** The operator says "dental implant costs" but the page covers costs, risks, procedure steps, recovery, and comparisons with alternatives. If you anchor to "costs", every non-cost section gets flagged as scope creep. Flag the mismatch: "You said this page targets 'dental implant costs', but the page contains [N] sections covering [topics]. The page appears to serve a broader intent like 'dental implants [location]' with costs as one sub-question. Which intent should I anchor to?"
- **Too broad:** The operator says "dental services Westminster" but the page only covers implants. The intent is broader than the content. Flag it: "You said 'dental services' but the page only covers implants. Should I anchor to 'dental implants Westminster' instead?"
- **Good fit:** The stated intent matches the scope of the content. Proceed.

Do not silently override the operator's intent. State the mismatch, propose an alternative, and let the operator decide before running the assessment.

> 🎯 **Primary intent:** [e.g. "Can I get dental implants near Westminster WA and who should I go to?"]
> *Derived from: [URL slug / title tag / H1 / operator-provided — state the source]*
> 🎯 **Secondary intents:** [e.g. "How much do dental implants cost in Perth?", "Dental implants vs bridges vs dentures", "What happens during dental implant surgery?"]

Long pages often serve multiple search intents. Identify the primary intent, then identify any secondary intents the page also serves. Each intent should map to at least one anchorable statement somewhere on the page. If a secondary intent is served by content but has no self-contained citable statement, flag it — the page has the information but an LLM can't efficiently cite it for that query.

**H1 alignment check:** If the H1 does not clearly reflect the primary intent, flag it as a heading issue. A misaligned H1 is a Gate 1 (retrieval) problem — it signals the wrong topic to systems that weight heading content.

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

- **PASS:** All 4 signals present in an extractable passage (ideally in Zone 1). An LLM could cite this page and the reader would know exactly who provides what, for whom, under what conditions.
- **PARTIAL:** 2–3 signals present. The page differentiates on some dimensions but an LLM could still substitute a competitor's content without loss of specificity.
- **FAIL:** 0–1 signals present. The content is commodity — any business in the category could claim the same statements.

### The substitution test

Quick validation: mentally replace the brand name with a competitor's name. If every sentence still works, the page has no competitive differentiation and will lose ranking contests to pages that do.

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

Not all repetition is a DRY violation. **Entity re-anchoring** — restating a named entity in a new section so the section becomes self-contained — is good for extractability, provided each mention adds a new attribute or relationship. The test: does this repetition make a section independently citable, or does it restate a claim already made without adding information?

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

### What is NOT anchorable
- Marketing slogans ("Your smile, our passion")
- Vague generalisations ("Recovery times vary depending on the individual")
- Sentences that require context from the previous paragraph
- Claims without specifics ("We offer competitive pricing")

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

**Regulated industry escalation:** In healthcare, legal, or financial content, any claim with a separated condition is flagged as HIGH priority regardless of zone. A stripped condition in these domains is not just a ranking issue — it is a misinformation vector.

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
- Contains a direct action phrase ("Book Now", "Get Started", "Call Us", "Let's Chat", "Schedule", "Request")
- Is 1–3 sentences long with no substantive informational content
- Sits between two content sections as an interstitial break
- Contains no named entities, data points, or claims beyond a generic value proposition
- Would render on the live page as a button, banner, or visual break rather than a readable content section

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
- Opening sentences that restate the heading or state the obvious. These are a commonly missed slop pattern — flag them consistently. Examples: "Like any surgical procedure, X carries risks" (heading already says "Understanding the Risks"), "This is one of the most common concerns" (heading already says "Does X Hurt?"), "X is a significant investment" (heading already says "X Costs"). If the first sentence could be deleted and the section would lose zero information, it is slop.
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

**Page-level entity re-anchoring check:** After scoring all sections individually, look for a pattern: if 3+ sections score below 6/10 on Entity Completeness because they fail to re-anchor to the primary entity (clinic, brand, practitioner), flag this as a **page-level entity gap** in the priority actions — not just per-section notes. The fix is a single re-anchoring sentence per affected section, not a rewrite. Generic educational content that could appear on any competitor's site is the #1 reason pages lose G2 ranking contests. Aggregate the pattern; don't bury it in section notes.

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

- **Critical:** Zone 1 missing required elements, off-topic sections, scope creep (sections that should be their own page), section integrity failures, condition preservation violations in regulated content. These are structural problems — the page can't compete until they're fixed.
- **Important:** Entity completeness gaps, format mismatches, missing anchorable statements, unresolved coreference. These reduce the page's chances of being cited.
- **Minor:** Natural language quality issues, minor density improvements, heading tweaks. These are polish — fix them after the critical and important issues.

### Gate diagnosis

After assessing all sections, count the findings per gate to identify the primary bottleneck. This tells the operator which *category* of problem dominates the page.

| Gate | Checks that feed it | What findings here mean |
|---|---|---|
| **G1: Retrieval** | Entity Completeness, Format Appropriateness | Content doesn't surface at all — wrong language, missing entities, format makes content unparseable |
| **G2: Ranking** | Structural Fitness, Information Density, Entity Completeness, Natural Language Quality | Content surfaces but loses to competitors — not dense enough, not differentiated, not well-structured |
| **G3: Citation** | Structural Fitness, Extractability, Format Appropriateness, Natural Language Quality | Content ranks but LLM can't confidently use it — unresolved pronouns, missing conditions, no anchorable statement |

**How to identify the bottleneck:** Count the issues per gate across all sections. The gate with the most findings (weighted toward Zone 1) is the primary bottleneck. Report it as:

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
🏥 Healthcare Mode / ⚙️ Standard Mode

---

✅ WHAT'S WORKING
- [Strength 1 — be specific so the LLM writer knows to preserve this]
- [Strength 2]
- [...]

---

🚦 GATE DIAGNOSIS
  G1 Retrieval: [X issues] — [brief summary or "no issues"]
  G2 Ranking: [X issues] — [brief summary or "no issues"]
  G3 Citation: [X issues] — [brief summary or "no issues"]
  Primary bottleneck: [Gate X — one-sentence explanation]

---

🗺️ Zone Analysis
  Page length: [~X characters / ~X words]
  Zone 1 (first ~20%): [present ✅ / missing ⚠️ — be specific about what's present/missing]
  Body ([N] content sections): [summary]
  ⚠️ Architecture gap: [if applicable]
  ⚠️ Section integrity issues: [if applicable]
  ⚠️ Length flag: [if applicable]

🎯 Primary intent: [as provided by operator]
  H1 alignment: ✅ / ⚠️ [H1 does not reflect intent — flag as Gate 1 issue]
🎯 Secondary intents: [list]

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
```

---

## Instructions

1. **Ask the operator for the primary search intent before starting.** "What search query or intent is this page targeting?" Do not proceed until you have this — the entire audit anchors to it. If the operator provides a URL without an intent, ask.
2. Read the full page before assessing anything.
2. Run Steps 1–9 (mode, zone analysis + section integrity, flow/intents, differentiation, format, DRY, trust signals, anchorable statements + condition preservation, CTA detection) before section assessment. Page-level issues outrank sentence-level issues in priority.
3. Identify and exclude CTA blocks before assessing sections.
4. Label each content section as Zone 1 or Body. Assess each section against the three section integrity rules (topical binding, single concept, self-containment).
5. For each section, list specific strengths (what to preserve) and specific issues (what to fix). Every issue must name the gate it affects and what the fix looks like. Categorise each issue as Critical, Important, or Minor using the severity guide.
6. Count issues per gate to identify the primary bottleneck. The issues list should fix the bottleneck gate first.
7. Flag the highest-impact sentences per section for rewrite. Zone 1 sentences take priority over Body sentences regardless of issue type.
8. Rewrites must be mode-compliant. In healthcare mode preserve all hedged language. In standard mode add specific data points where original is too vague — note when specifics are invented.
9. Do not push rewrites toward oversimplification. Dense, condition-preserving prose is the goal — not stripped-down data points.
10. List ALL findings in the issues list, ordered by severity (Critical → Important → Minor). Every non-conflicting fix should be listed — the LLM writer applies all of them. The ordering tells the operator what matters most.
11. The output is input for an LLM writer. Every finding must be specific enough that the writer can act on it without additional context. "Improve density" is not actionable. "Section X opener restates the heading — delete it and lead with the first fact" is actionable.
12. Keep the tone professional and direct — this is a technical audit, not a critique.
13. If the page is clearly AI-generated slop (uniform sentence structure, no trust signals, high DRY violations, no tables or lists, zero named entities), say so directly in the summary before the detailed audit.

---

## Quick-Reference Checklist

For content creators to verify before publishing. This is the minimum bar — not a substitute for a full audit.

- [ ] The single most important claim appears in the first 20% of the page
- [ ] Every section answers a sub-question of the primary search intent — no off-topic sections, no oversized sections that should be their own page
- [ ] Every section covers one concept/question, not two (single concept)
- [ ] Every section makes sense if pulled out of the page with no surrounding context (self-containment)
- [ ] Every sentence with a pronoun subject ("it," "this," "they") has been checked — can it stand alone?
- [ ] Every claim with a number includes its source, timeframe, and population in the same sentence
- [ ] The page uses at least 2–3 content formats (prose + list, prose + table, etc.)
- [ ] Every heading describes what the section contains, not a clever metaphor
- [ ] At least one sentence per section is directly quotable — specific, self-contained, condition-preserving
- [ ] No claim is repeated more than twice on the page
- [ ] Conditions and caveats share a sentence with the claims they qualify
- [ ] The substitution test: replacing the brand name with a competitor's breaks at least some sentences
- [ ] The page identifies what it is, who it's for, what job it does, and what constraint it wins under