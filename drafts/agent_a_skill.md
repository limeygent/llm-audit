

# LLM Readability Audit Methodology

## Purpose

This methodology scores any webpage's copy on how effectively it can be retrieved, chunked, understood, and cited by large language models — whether operating inside Google AI Overviews, ChatGPT browse, Perplexity, or enterprise RAG pipelines. The output is a quantitative scorecard (0-100) with sentence-level fixes.

---

## Foundational Premises

1. **AI systems do not read pages. They sample them.** Roughly 380 words per page get selected for grounding, from a budget of approximately 1,900 words across all sources for a single query. Every word competes for inclusion.
2. **Extraction is destructive.** Sentences get ripped from context. Paragraphs get truncated. Headings get separated from their body text. Copy must survive this violence intact.
3. **Machines build knowledge graphs, not impressions.** Subject-verb-object triples, named entities, and explicit relationships are what get indexed. Mood, tone, and cleverness are invisible unless they ride on top of structural clarity.
4. **Position is not neutral.** The first 20% and last 20% of a page receive disproportionate attention from retrieval systems. The middle is a graveyard.

---

## Audit Steps

### STEP 1: Page Inventory and Classification

Before scoring anything, classify the page.

**Actions:**
- Record the page URL, title tag, H1, meta description, and word count
- Classify the page type: Service, Product, Blog/Article, Landing Page, FAQ, About, Legal/Policy, Resource/Tool
- Identify the regulated industry flag: Yes/No (healthcare, legal, finance, insurance, pharma)
- Count the total number of: headings (H2-H4), paragraphs, lists, tables, images with alt text, internal links, external links
- Identify the primary query intent the page should answer (informational, navigational, transactional, comparative)

**Why it matters:** Page type determines which audit criteria carry extra weight. A service page with zero comparative statements has a different problem than a blog post with zero comparative statements.

**Output:** A one-paragraph page profile that a stranger could read and understand what this page is, who it targets, and what job it does.

---

### STEP 2: Grounding Budget Analysis

Determine whether the page is working within or against the extraction constraints of AI systems.

**Actions:**
- Calculate the grounding ratio: 380 / total word count = percentage of page likely to be sampled
- If word count is under 5,000 characters: flag as "high coverage" (approximately 66% sampled)
- If word count exceeds 20,000 characters: flag as "diluted" (approximately 12% sampled)
- Identify the "golden zones" — the first 20% and last 20% of the page body content (by word count)
- Assess what occupies the golden zones: Is it the most important, differentiated, citable material? Or is it throat-clearing, generic context, or boilerplate?
- Identify what sits in the "dead middle" (the 20%-80% range) — flag any critical claims, differentiators, or answer-worthy content buried there

**Scoring (0-10): Grounding Efficiency**

| Score | Description |
|-------|-------------|
| 9-10 | Under 2,000 words. Best claims in first and last 20%. No filler. |
| 7-8 | Under 3,000 words. Most key material is well-positioned. Minor burial. |
| 5-6 | 3,000-5,000 words. Some critical content in dead middle. Moderate filler. |
| 3-4 | Over 5,000 words. Key differentiators buried. Significant dilution. |
| 1-2 | Over 8,000 words. Core value proposition lost in noise. |
| 0 | Thin page with under 100 words or entirely boilerplate. |

---

### STEP 3: Structural Fitness Assessment

Evaluate whether the page architecture helps or hinders machine parsing.

**Actions:**
- Check heading hierarchy: Does it follow H1 > H2 > H3 > H4 without skipping levels?
- Evaluate whether each H2/H3 functions as a standalone query: Could someone type that heading into a search bar and expect the content beneath it to answer?
- Check for the "AI Inverted Pyramid" pattern under each heading: Does the first sentence directly answer the heading's implied question in 40-60 words, followed by context, then evidence?
- Assess content format diversity: Does the page use a mix of prose, lists, and tables where appropriate? Or is it a wall of undifferentiated paragraphs?
- Check table usage: Are comparison data and specifications presented in tables (which LLMs parse with high accuracy) or buried in prose?
- Verify that lists use explicit, complete items — not fragments that depend on the list title for meaning

**Scoring (0-10): Structural Fitness**

| Score | Description |
|-------|-------------|
| 9-10 | Clean hierarchy. Every heading is query-shaped. Inverted pyramid under each. Format diversity matches content type. |
| 7-8 | Good hierarchy with 1-2 skips. Most headings are query-shaped. Generally answers-first. |
| 5-6 | Hierarchy present but headings are decorative or vague. Answers buried mid-paragraph. |
| 3-4 | Flat structure. Generic headings ("Our Approach," "More Info"). No inverted pyramid. |
| 1-2 | No headings or single H1 only. One continuous block of text. |
| 0 | Content is in images, JavaScript-rendered without HTML fallback, or inaccessible. |

---

### STEP 4: Sentence Extraction Survivability

This is the most granular and most important step. Test whether individual sentences survive being ripped from context.

**Actions:**

Select 15-20 sentences from across the page (5-7 from golden zones, 5-7 from dead middle, 3-6 from lists/tables). For each sentence, apply five sub-tests:

**4A. The Isolation Test**
Remove the sentence from the page entirely. Read it alone. Does it make a complete, true, useful claim without any surrounding context?

Failure patterns to flag:
- Unresolved pronouns: "They offer this at scale" — who is "they"? What is "this"?
- Vague demonstratives: "This approach works best" — which approach?
- Context-dependent claims: "Unlike the alternative, it is faster" — alternative to what? Faster than what?
- Stripped conditions: "Results in 30 days" — under what conditions? For whom?
- Assumed knowledge: "Uses the standard protocol" — standard according to whom?
- Relative claims without baseline: "50% more efficient" — than what?

**4B. The Attribution Test**
If an AI system cited this sentence and attributed it to this page, would the claim be accurate, complete, and not misleading when standing alone?

Flag sentences where isolated citation would:
- Overstate a capability (missing qualifiers)
- Misrepresent scope (applies to one product but sounds universal)
- Violate regulatory requirements (medical/legal/financial claims without required hedging)

**4C. The Entity Resolution Test**
Does the sentence contain all named entities needed to understand it? Every important noun should be a specific name, not a pronoun or category.

Good: "Acme Corp's DataVault platform encrypts files at rest using AES-256."
Bad: "Our platform encrypts your files using industry-standard encryption."

**4D. The Relationship Clarity Test**
Does the sentence express at least one clear subject-verb-object relationship? Can you extract a knowledge triple from it?

Good: "PostgreSQL handles concurrent writes faster than MySQL under high-transaction workloads." (Triple: PostgreSQL > outperforms > MySQL > condition: high-transaction)
Bad: "Great performance, scalability, and reliability." (No relationships, no triples.)

**4E. The Quotability Test**
Could an AI system drop this sentence into a response as a direct quote without needing to paraphrase, hedge, or add context?

Good: "The FDA approved Keytruda for adjuvant treatment of stage IIB/IIC melanoma in December 2023."
Bad: "We recently got approved for another exciting indication!"

**Scoring (0-10): Extraction Survivability**

Calculate the pass rate across all tested sentences for each sub-test. Average them.

| Score | Description |
|-------|-------------|
| 9-10 | 90%+ of tested sentences pass all five sub-tests. |
| 7-8 | 75-89% pass rate. Failures are minor (missing one qualifier, one pronoun). |
| 5-6 | 50-74% pass rate. Regular pronoun issues, some buried conditions. |
| 3-4 | 25-49% pass rate. Most sentences need surrounding context to make sense. |
| 1-2 | Under 25% pass rate. Copy is conversational, referential, and context-dependent throughout. |
| 0 | No sentence on the page survives extraction. |

---

### STEP 5: Entity and Differentiation Completeness

Assess whether the page provides enough named, specific information for an AI to build a knowledge node about this entity.

**Actions:**
- Check whether the page explicitly states, within the first 20% of content:
  - **What it is** (category, type, definition)
  - **Who it is for** (named audience, role, or segment)
  - **What job it does** (specific outcome or function)
  - **What constraint it wins under** (price, speed, geography, regulation, use case)
- Count unique named entities on the page (brand names, product names, people, places, specific technologies, standards, certifications)
- Check for comparative positioning: Does the page state how this entity relates to alternatives, competitors, or adjacent categories?
- Check for factual anchors: dates, version numbers, statistics, certifications, regulatory references, geographic scope
- Flag any "orphan entities" — names or products mentioned without enough context for an AI to understand what they are

**Scoring (0-10): Entity Completeness**

| Score | Description |
|-------|-------------|
| 9-10 | All four differentiation elements present in first 20%. Rich entity network. Clear comparisons. Factual anchors throughout. |
| 7-8 | Three of four elements present. Good entity density. Some comparisons. |
| 5-6 | Two of four elements. Moderate entity density. No comparisons or only vague ones. |
| 3-4 | One element. Few named entities. Generic positioning. |
| 1-2 | No differentiation framework. Copy could describe any company in the category. |
| 0 | No named entities. No specifics. Entirely generic. |

---

### STEP 6: Trust and Authority Signals

Evaluate whether the page provides the evidence markers that AI systems use to gauge source quality.

**Actions:**
- Check for cited sources: Are statistics attributed? Are claims linked to studies, standards, or authoritative bodies?
- Check for authorship signals: Is there a named author, credentials, or "reviewed by" attribution?
- Check for recency signals: Are dates present? Is there a "last updated" timestamp?
- Check for experience signals: Are there specific case studies, named clients (with permission), or concrete examples rather than hypothetical scenarios?
- Check for appropriate hedging in regulated industries:
  - Healthcare: "may," "consult your physician," disclaimers present?
  - Legal: "this is not legal advice," jurisdiction noted?
  - Finance: "past performance," risk disclosures present?
- Check the DRY principle: Is the same claim made multiple times in different words? Repetition wastes grounding budget and signals low information density.
- Flag any unsupported superlatives: "best," "leading," "top," "#1" without evidence

**Scoring (0-10): Trust Signals**

| Score | Description |
|-------|-------------|
| 9-10 | Statistics sourced. Author credentialed. Dates present. Hedging appropriate. No unsupported superlatives. Zero unnecessary repetition. |
| 7-8 | Most claims supported. Minor attribution gaps. Appropriate hedging. Minimal repetition. |
| 5-6 | Some sourcing. No author signals. Dates sparse. A few superlatives. Some repetition. |
| 3-4 | Mostly unsourced. No credentials. No dates. Multiple superlatives. Significant repetition. |
| 1-2 | All claims unsupported. Heavy self-promotion. No trust indicators. |
| 0 | Actively misleading or entirely unverifiable claims. Regulated content without required disclosures. |

---

### STEP 7: Natural Language Quality for Machine Processing

Assess the linguistic properties that affect how accurately NLP systems parse the content.

**Actions:**
- Check sentence length distribution: Flag sentences over 40 words (harder to parse) and under 5 words (often lack a complete proposition)
- Check for passive voice density: Passive constructions obscure the subject (the agent doing the action), which weakens entity extraction. Flag pages with more than 30% passive voice.
- Check for nominalizations: Verbs turned into nouns ("implementation" instead of "implements," "utilization" instead of "uses") reduce clarity of who does what to whom
- Check for jargon density without definition: Industry terms are fine if defined on first use; undefined jargon creates entity resolution failures
- Check for ambiguous scope modifiers: "some," "many," "often," "sometimes," "generally" — these are acceptable for hedging but problematic when they replace specifics unnecessarily
- Check list items for completeness: Each bullet should contain a subject and predicate, not just a noun phrase

**Scoring (0-10): Language Quality**

| Score | Description |
|-------|-------------|
| 9-10 | Average sentence length 15-25 words. Under 15% passive. Clear S-V-O throughout. Jargon defined. |
| 7-8 | Occasional long sentences. 15-25% passive. Most structures clear. Minor jargon issues. |
| 5-6 | Multiple long sentences. 25-35% passive. Some nominalization clusters. Undefined terms. |
| 3-4 | Frequently over 40 words. Over 35% passive. Heavy nominalizations. Jargon-heavy. |
| 1-2 | Run-on sentences throughout. Mostly passive. Academic or legal density without simplification layer. |
| 0 | Incomprehensible, machine-generated word salad, or keyword-stuffed text. |

---

### STEP 8: Technical Accessibility

Verify that AI crawlers and retrieval systems can actually access and parse the content.

**Actions:**
- Check robots.txt: Is the page blocked from AI crawlers (GPTBot, Google-Extended, CCBot, anthropic-ai)?
- Check meta robots tags: noindex, nofollow, nosnippet, max-snippet restrictions?
- Check whether critical content is rendered in JavaScript only (invisible to crawlers that do not execute JS)
- Check for canonical URL correctness
- Check page load time: pages that time out are not crawled
- Check for content behind login walls, cookie gates, or aggressive interstitials
- Verify structured data markup: Schema.org, FAQ schema, HowTo schema, Product schema where applicable

**Scoring (0-10): Technical Accessibility**

| Score | Description |
|-------|-------------|
| 9-10 | All AI crawlers permitted. Content in HTML. Schema markup present. Fast load. Clean canonical. |
| 7-8 | Most crawlers permitted. Mostly HTML-rendered. Some schema. Good performance. |
| 5-6 | One major crawler blocked. Some JS-dependent content. No schema. Moderate speed. |
| 3-4 | Multiple crawlers blocked. Significant JS rendering. Slow load. |
| 1-2 | Most crawlers blocked. Content behind gates. No structured data. |
| 0 | Page is noindexed, login-walled, or returns errors. |

---

## Scoring Summary

### Category Weights

Not all categories contribute equally. Weights vary by page type:

| Category | Service Page | Blog/Article | Product Page | Landing Page |
|----------|-------------|--------------|-------------|-------------|
| 1. Grounding Efficiency | 10% | 10% | 10% | 15% |
| 2. Structural Fitness | 15% | 15% | 10% | 10% |
| 3. Extraction Survivability | 25% | 20% | 20% | 20% |
| 4. Entity Completeness | 15% | 10% | 20% | 15% |
| 5. Trust Signals | 10% | 20% | 15% | 10% |
| 6. Language Quality | 10% | 15% | 10% | 15% |
| 7. Technical Accessibility | 15% | 10% | 15% | 15% |

**Final Score = Sum of (Category Score x Weight) x 10**

Result is on a 0-100 scale.

### Grade Bands

| Score | Grade | Interpretation |
|-------|-------|---------------|
| 85-100 | A | Highly citable. Likely to be retrieved and quoted by AI systems. |
| 70-84 | B | Good foundation. Specific improvements will increase citation probability. |
| 55-69 | C | Mediocre. AI systems can parse it but will prefer better-structured competitors. |
| 40-54 | D | Poor. Significant structural and linguistic barriers to machine extraction. |
| 0-39 | F | Functionally invisible to AI retrieval systems. |

---

## Final Report Template

```
================================================================
LLM READABILITY AUDIT REPORT
================================================================

Page: [URL]
Audited: [Date]
Page Type: [Classification]
Regulated Industry: [Yes/No — which]
Word Count: [N]
Grounding Ratio: [380/N = X%]

================================================================
OVERALL SCORE: [XX] / 100 — Grade [X]
================================================================

CATEGORY SCORES
----------------------------------------------------------------
1. Grounding Efficiency:        [X] / 10  (weight: XX%)
2. Structural Fitness:          [X] / 10  (weight: XX%)
3. Extraction Survivability:    [X] / 10  (weight: XX%)
4. Entity Completeness:         [X] / 10  (weight: XX%)
5. Trust Signals:               [X] / 10  (weight: XX%)
6. Language Quality:            [X] / 10  (weight: XX%)
7. Technical Accessibility:     [X] / 10  (weight: XX%)

================================================================
TOP 3 ISSUES (by impact on score)
================================================================

Issue 1: [Name]
- What: [Specific finding]
- Why it matters: [Impact on AI retrieval]
- Fix: [Specific action]

Issue 2: [Name]
- What: [Specific finding]
- Why it matters: [Impact on AI retrieval]
- Fix: [Specific action]

Issue 3: [Name]
- What: [Specific finding]
- Why it matters: [Impact on AI retrieval]
- Fix: [Specific action]

================================================================
SENTENCE-LEVEL REWRITES (up to 10)
================================================================

Location: [Heading or section where sentence appears]

BEFORE:
"[Original sentence]"

PROBLEM: [Which sub-test(s) it fails and why]

AFTER:
"[Rewritten sentence]"

IMPROVEMENT: [What changed and why the rewrite scores higher]

---
[Repeat for each rewrite]

================================================================
POSITIONING ANALYSIS
================================================================

Golden Zone (First 20%):
- Currently contains: [Summary]
- Should contain: [Recommendation]
- Missing: [What needs to move here]

Golden Zone (Last 20%):
- Currently contains: [Summary]
- Should contain: [Recommendation]
- Missing: [What needs to move here]

Dead Middle (20%-80%):
- Buried critical content: [List items that should be repositioned]

================================================================
ENTITY MAP
================================================================

Entities Found: [List all named entities on the page]
Entities Missing: [Entities that should be present but are not]
Orphan Entities: [Names mentioned without sufficient context]

Differentiation Checklist:
- [ ] What it is: [Present/Missing — quote or note]
- [ ] Who it is for: [Present/Missing — quote or note]
- [ ] What job it does: [Present/Missing — quote or note]
- [ ] What constraint it wins under: [Present/Missing — quote or note]

================================================================
CONTENT FORMAT RECOMMENDATIONS
================================================================

- [Specific recommendation, e.g., "Convert the feature comparison 
  in paragraph 4 to a table with columns: Feature, This Product, 
  Competitor A, Competitor B"]
- [Specific recommendation, e.g., "Break the 847-word section under 
  'Our Process' into 4 sub-headed sections of 150-200 words each"]
- [Specific recommendation]

================================================================
REGULATED CONTENT FLAGS (if applicable)
================================================================

- [Finding, e.g., "Claim 'cures back pain' on line 47 lacks 
  required FDA-compliant hedging. Rewrite: 'may help reduce 
  back pain symptoms'"]
- [Finding]

================================================================
TECHNICAL FIXES
================================================================

- [Finding, e.g., "GPTBot is blocked in robots.txt. Remove 
  'User-agent: GPTBot / Disallow: /' to allow AI crawling"]
- [Finding]

================================================================
PRIORITY ACTION PLAN
================================================================

Immediate (this week):
1. [Highest-impact fix]
2. [Second-highest]
3. [Third]

Short-term (this month):
4. [Fix]
5. [Fix]

Ongoing:
6. [Process or standard to adopt]

================================================================
```

---

## Usage Notes

**Time estimate:** A thorough audit of one page takes 45-90 minutes depending on word count and complexity. The sentence extraction survivability step (Step 4) takes the longest and delivers the most actionable findings.

**Repeatability:** Run this audit after implementing fixes. Score improvements of 15+ points typically correlate with measurable increases in AI citation frequency within 4-8 weeks, contingent on crawl cycles.

**Batch auditing:** When auditing an entire site, start with the 5-10 pages that rank for your highest-value queries. These are the pages most likely to be candidates for AI grounding. Audit those first, establish patterns, then create site-wide writing guidelines from the recurring fixes.

**Calibration:** The first time you use this methodology, audit three pages of varying quality to calibrate your scoring. Adjust your internal baseline so that a "5" genuinely represents the median — not generous, not harsh.
