

# LLM Readability Audit: Dual-Signal Methodology

## Purpose

This audit evaluates content for two equally weighted outcomes: (1) whether an LLM will surface, select, and cite your content when answering user queries, and (2) whether a human reader will trust, understand, and convert. Over-optimizing for either signal degrades the other. The goal is content that reads naturally while remaining structurally extractable.

---

## Part 1: Process Overview

### Phase 1 — Inventory (5 minutes per page)

1. Record the page URL, word count, character count, and primary conversion goal.
2. Identify the target query cluster — the 3-5 questions a user (or LLM) would ask that this page should answer.
3. Note the page type: landing page, product page, blog post, comparison, FAQ, legal/regulated content.
4. Flag the industry vertical. If healthcare, legal, or finance, activate the Regulated Content Module (Section 6).

### Phase 2 — Structural Scan (10 minutes)

Run through all checks in Part 3 below. Score each dimension. Do not rewrite yet — just annotate.

### Phase 3 — Extraction Simulation (10 minutes)

Select 5 non-contiguous sentences from the page at random. Read each sentence completely isolated from surrounding context. Ask: "Does this sentence make a complete, accurate, useful claim on its own?" If fewer than 3 out of 5 pass, the page has a systemic extractability problem.

### Phase 4 — Competitive Differentiation Test (5 minutes)

For each target query, ask: "If an LLM had this page and three competitor pages, what specific sentence from THIS page would it quote?" If you cannot identify one, the page lacks a citable differentiator.

### Phase 5 — Scoring and Report (10 minutes)

Compile dimension scores, calculate composite, write prioritized fix list using the report template in Part 5.

---

## Part 2: Scoring System

### Dimensions (10 points each, 100 total)

| # | Dimension | Weight | Measures |
|---|-----------|--------|----------|
| 1 | Position Architecture | 10 | Key claims in first/last 20% of page |
| 2 | Sentence Sovereignty | 10 | Self-contained, context-free sentences |
| 3 | Entity Completeness | 10 | Named subjects, resolved references |
| 4 | Relationship Clarity | 10 | S-V-O structure, explicit cause-effect |
| 5 | Trust Infrastructure | 10 | Credentials, sources, evidence, specificity |
| 6 | Format Diversity | 10 | Balanced mix of prose, lists, tables |
| 7 | Conversion Mechanics | 10 | CTAs, benefit framing, urgency, clarity |
| 8 | Natural Language Quality | 10 | Reads like a human expert wrote it |
| 9 | Heading Taxonomy | 10 | Query-aligned, descriptive, hierarchical |
| 10 | Condition Preservation | 10 | Caveats, timeframes, qualifiers intact |

### Scoring Scale Per Dimension

- **9-10:** Publication ready. No fixes needed.
- **7-8:** Minor issues. 1-2 sentence-level edits.
- **5-6:** Structural weakness. Paragraph-level rewrites needed.
- **3-4:** Systemic failure. Section-level restructuring required.
- **1-2:** Hostile to the signal being measured. Major overhaul.

### Composite Score Interpretation

| Range | Rating | Action |
|-------|--------|--------|
| 85-100 | Dual-Signal Strong | Monitor only |
| 70-84 | Functional | Targeted fixes, schedule within 2 weeks |
| 50-69 | Underperforming | Rewrite priority sections, schedule within 1 week |
| Below 50 | Structurally Broken | Full page rewrite required |

### Over-Optimization Penalty

If any single dimension scores 10 but two or more others score below 5, apply a -5 penalty to the composite score and flag "Signal Imbalance" in the report. This catches pages that are perfectly machine-readable but repel humans (or vice versa).

---

## Part 3: The 10 Checks — With Examples

### Check 1: Position Architecture

**What to look for:** Are the page's most important claims — the ones you want an LLM to cite — located in the first 20% or last 20% of the page body? The "lost in the middle" effect means content buried in the center of a long page has significantly lower extraction probability.

**Procedure:**
- Divide the page into fifths by word count.
- Highlight the single most important claim for each target query.
- Count how many fall in the first or last fifth.

**Scoring:**
- All key claims in first/last 20%: 10
- Most key claims well-positioned, one buried: 7-8
- Key claims scattered randomly: 5-6
- Most important claim buried in middle third: 3-4
- Page buries the lede entirely, key claim appears only in paragraph 8 of 10: 1-2

**Bad example:**
> "Welcome to our comprehensive guide about joint health. In this article, we'll cover everything you need to know. Joint health is important for people of all ages. Many factors contribute to joint discomfort. Let's explore the options available today. [... 600 more words ...] Studies at Johns Hopkins found that UC-II collagen at 40mg/day reduced knee pain scores by 33% versus placebo over 90 days."

The only citable, specific claim is buried at the bottom of a 900-word preamble.

**Good example:**
> "UC-II collagen at 40mg/day reduced knee pain scores by 33% versus placebo in a 90-day Johns Hopkins trial — making it the most studied single-ingredient option for age-related joint stiffness. Here's how it compares to the other evidence-backed approaches."

The citable claim leads. The rest of the page can elaborate.

---

### Check 2: Sentence Sovereignty

**What to look for:** Can each sentence be extracted and understood without reading the sentence before or after it? LLMs pull fragments. If a sentence depends on its neighbors for meaning, the extracted fragment will be incomplete or misleading.

**Procedure:**
- Select 10 sentences distributed across the page.
- Read each one in total isolation.
- Mark as "sovereign" (fully understandable alone) or "dependent" (requires context).
- Score = (sovereign count / 10) x 10.

**Bad examples:**

> "It also features a 120Hz refresh rate."

Problem: "It" is unresolved. An LLM citing this sentence cannot tell the reader what product is being discussed.

> "This makes it the best choice for most users."

Problem: "This" and "it" are both unresolved. "Best" by what measure? "Most users" in what context?

> "Combined with the above specs, you get a compelling package."

Problem: "The above specs" is a positional reference that means nothing when extracted.

**Good examples:**

> "The Samsung Galaxy S25 Ultra features a 120Hz LTPO AMOLED display with 2600-nit peak brightness."

Fully self-contained. An LLM can cite this with zero ambiguity.

> "For photographers who shoot in low light, the Galaxy S25 Ultra's 200MP main sensor with f/1.7 aperture captures 35% more light than the iPhone 16 Pro Max's 48MP sensor."

Self-contained, comparative, audience-qualified.

---

### Check 3: Entity Completeness

**What to look for:** Every claim must name its subject explicitly. Products, brands, people, organizations, locations, and timeframes should be stated, not assumed.

**Procedure:**
- Scan for pronouns (it, they, this, that, these, those, which) used as sentence subjects.
- Scan for assumed knowledge ("the product," "our solution," "the popular option").
- Count unresolved entities.

**Scoring:**
- 0 unresolved entities: 10
- 1-2 unresolved entities: 7-8
- 3-5 unresolved entities: 5-6
- 6-10 unresolved entities: 3-4
- 11+ unresolved entities: 1-2

**Bad example:**
> "It's one of the most popular supplements on the market. They've been making it for over 20 years. Most doctors recommend it."

Three sentences. Zero named entities. An LLM cannot cite any of these.

**Good example:**
> "Garden of Life Raw Probiotics Ultimate Care (100 billion CFU, 34 strains) has been manufactured by Garden of Life since 2004. The product ranks as the top-selling refrigerated probiotic on Amazon, with recommendations from over 2,300 practitioners listed in the company's provider directory."

Every claim has a named subject, a specific quantity, and a verifiable source reference.

---

### Check 4: Relationship Clarity

**What to look for:** Sentences should express clear Subject-Verb-Object relationships. Research shows that S-V-O triples are significantly more extractable than verb-less bullet lists or noun-stacked phrases.

**Procedure:**
- Identify all bullet-point lists on the page.
- For each list, check: Are the items full S-V-O sentences, or are they noun fragments?
- Identify passive-voice sentences that obscure agency.
- Score based on percentage of content using clear relational structure.

**Bad example (verb-less bullet list):**
> Features:
> - 5000mAh battery
> - Titanium frame
> - 200MP camera
> - IP68 water resistance

An LLM cannot form a relationship from these fragments. It does not know what product these belong to, and the items lack verbs.

**Good example (relational bullets):**
> The Galaxy S25 Ultra's key hardware advantages:
> - The 5000mAh silicon-carbon battery delivers 28 hours of mixed use, 3 hours longer than the Galaxy S24 Ultra.
> - Samsung's Grade 5 titanium frame weighs 218g while surviving 1.2m drop tests onto concrete.
> - The 200MP HP2 main sensor produces 12MP pixel-binned images with 2.4μm effective pixel size, matching dedicated compact cameras in detail.

Each bullet names the subject, states a verb, provides an object, and includes a comparative or quantitative anchor.

---

### Check 5: Trust Infrastructure

**What to look for:** Claims need evidence. LLMs are trained to prefer content with verifiable specifics, named sources, and professional credentials. Humans convert better when they trust the author.

**Procedure:**
- Count claims that include a named source (study, institution, expert, publication).
- Count claims with specific numbers (percentages, dates, measurements).
- Check for author credentials or "why should I trust this page" signals.
- Check for recency markers (dates on data, "as of [date]" qualifiers).

**Scoring:**
- 80%+ of major claims sourced and specific: 10
- 60-79% sourced: 7-8
- 40-59% sourced: 5-6
- 20-39% sourced: 3-4
- Under 20% sourced or actively misleading: 1-2

**Bad example:**
> "Studies show that this ingredient is effective. Experts agree it works. Thousands of customers love it."

Zero named studies. Zero named experts. Zero named customers. Zero numbers.

**Good example:**
> "A 2023 randomized controlled trial published in the Journal of Bone and Mineral Research (n=440) found that 5,000 IU daily vitamin D3 supplementation reduced fracture risk by 18% in postmenopausal women over 24 months (p<0.01). Dr. Sarah Chen, endocrinologist at UCSF, called this dosage 'the evidence-based minimum for women over 60' in her 2024 clinical review."

Named journal, sample size, specific dosage, specific outcome, named expert with credentials, quoted statement, publication date.

---

### Check 6: Format Diversity

**What to look for:** Pages that use only one format — all prose, all bullets, or all tables — underperform on both signals. LLMs extract different content types for different query intents. Humans skim differently depending on format. A healthy page mixes formats purposefully.

**Procedure:**
- Catalog each content block by format: prose paragraph, bullet list, numbered list, table, blockquote, code block, FAQ pair.
- Calculate the percentage of total content each format represents.
- Flag if any single format exceeds 70% of total content.
- Flag if the page uses fewer than 3 distinct formats.

**Scoring:**
- 3+ formats, no single format above 60%, format choices match content type: 10
- 3+ formats but slightly imbalanced: 7-8
- 2 formats or one format dominates at 70%+: 5-6
- Single format for entire page: 3-4
- Single format AND that format is purely decorative (e.g., bullets used as prose): 1-2

**Bad example (all bullets):**
> - We offer CRM integration
> - Our platform supports 50+ languages
> - Pricing starts at $29/month
> - Founded in 2018
> - Used by 3,000 companies
> - SOC 2 Type II certified
> - Average onboarding time: 2 days

This is a data dump. It lacks narrative, context, or relational structure. It fails both humans (no story, no benefit framing) and machines (no S-V-O, no relationships between items).

**Good example (mixed format, same information):**
> Acme CRM launched in 2018 and now serves over 3,000 companies across 50+ languages, with SOC 2 Type II certification maintained since 2021.
>
> | Plan | Monthly Price | Users | Integrations |
> |------|--------------|-------|-------------|
> | Starter | $29 | Up to 5 | 12 native + Zapier |
> | Growth | $79 | Up to 25 | 40 native + API |
> | Enterprise | Custom | Unlimited | Full API + SSO |
>
> Most teams complete onboarding in under 2 days — including data migration from Salesforce, HubSpot, or Pipedrive.

Prose for narrative context, table for comparison data, short closing sentence for conversion nudge.

---

### Check 7: Conversion Mechanics

**What to look for:** The page must still sell. AI readability means nothing if the page loses its persuasive structure. Check for benefit framing, clear CTAs, objection handling, urgency signals, and reader-addressed language.

**Procedure:**
- Locate every CTA on the page. Is it clear what happens when the user clicks?
- Check if features are translated into benefits (what the user gains, not just what exists).
- Look for objection handling (money-back guarantees, free trials, social proof near decision points).
- Verify the page addresses the reader directly ("you") at least occasionally — pure third-person encyclopedia tone kills conversion.

**Scoring:**
- Strong benefit framing, clear CTAs, objection handling, direct address, natural urgency: 10
- Most elements present, minor gaps: 7-8
- CTAs present but benefit framing weak or objection handling missing: 5-6
- Page reads like a Wikipedia entry — informative but not persuasive: 3-4
- No discernible conversion path or actively hostile to conversion (e.g., buried CTA, zero benefits): 1-2

**Bad example (over-optimized for AI, no conversion):**
> "Acme CRM is a customer relationship management platform headquartered in Austin, Texas. Acme CRM was founded in 2018 by John Doe. Acme CRM offers three pricing tiers. Acme CRM integrates with 50 third-party tools."

Technically extractable. Zero reason for a human to care, click, or buy.

**Good example (dual-signal):**
> "If your sales team wastes 5+ hours per week copying data between tools, Acme CRM's one-click integrations with Salesforce, HubSpot, and 48 other platforms eliminate that manual work — starting at $29/month with a 14-day free trial, no credit card required."

Self-contained (LLM can cite it). Benefit-framed (human feels the problem and solution). CTA-adjacent (price, trial, and friction removal in one sentence).

---

### Check 8: Natural Language Quality

**What to look for:** Over-optimized content sounds robotic. If every sentence is an entity-stuffed, keyword-front-loaded data statement, humans bounce. The page should sound like a knowledgeable expert speaking to a peer — not a database readout.

**Procedure:**
- Read the first three paragraphs aloud. Does it sound like a person talking?
- Check for variety in sentence length (mix of short, medium, and long).
- Check for variety in sentence openings (not every sentence starts with the brand name or product name).
- Look for transitional language that guides the reader.
- Flag "keyword stuffing" patterns where the primary keyword appears in every single sentence.

**Scoring:**
- Reads naturally, varied rhythm, smooth transitions, authoritative voice: 10
- Mostly natural, occasional stiffness: 7-8
- Noticeably formulaic but still readable: 5-6
- Robotic or keyword-stuffed: 3-4
- Unreadable — either machine-generated slop or so over-optimized it feels like reading a parts catalog: 1-2

**Bad example (robotic over-optimization):**
> "Acme CRM is a CRM platform. Acme CRM pricing starts at $29. Acme CRM integrates with Salesforce. Acme CRM integrates with HubSpot. Acme CRM was founded in 2018. Acme CRM is SOC 2 certified."

Every sentence is sovereign. Every entity is complete. The writing is insufferable.

**Good example (natural and extractable):**
> "Acme CRM was built for small sales teams that outgrew their spreadsheets but don't need Salesforce-level complexity. Since launching in 2018, the platform has grown to 3,000 customers — mostly B2B companies with 5-50 reps. Pricing starts at $29/month, with native integrations for the tools most small teams already use: Slack, Google Workspace, and Stripe."

Varied sentence structure. Conversational. Still fully extractable — every sentence names its subject, includes specifics, and stands alone.

---

### Check 9: Heading Taxonomy

**What to look for:** Headings serve dual duty. For LLMs, they signal topic boundaries and boost relevance by approximately 17%. For humans, they enable scanning. Headings should be query-aligned (phrased the way someone would search or ask), descriptive (not clever or vague), and hierarchical (H2 > H3 > H4, no skipped levels).

**Procedure:**
- List all headings in order with their level (H1, H2, H3, etc.).
- Check for skipped heading levels (H2 directly to H4).
- Check if headings match likely search queries or question formats.
- Flag headings that are purely clever/branding-focused with no descriptive value.

**Scoring:**
- All headings query-aligned, descriptive, properly hierarchical: 10
- Mostly aligned, 1-2 vague headings: 7-8
- Mix of descriptive and vague, or minor hierarchy issues: 5-6
- Most headings are clever but not descriptive, or hierarchy is broken: 3-4
- Headings are missing, purely decorative, or actively misleading: 1-2

**Bad examples:**
> - "The Magic Inside" (what does this section contain?)
> - "More Than Meets the Eye" (clever, unsearchable)
> - "Details" (too generic to signal anything)

**Good examples:**
> - "UC-II Collagen Dosage: 40mg Daily for Joint Pain Relief"
> - "Acme CRM Pricing: Three Plans from $29 to Enterprise"
> - "Side Effects and Drug Interactions for Vitamin D3 at 5,000 IU"

---

### Check 10: Condition Preservation

**What to look for:** One of the most dangerous AI-hostile patterns is stripping conditions, caveats, and qualifiers from claims. When an LLM extracts a sentence that originally had a caveat but was written without it, the LLM may state the claim as unconditional — creating legal liability, misinformation, and trust erosion.

**Procedure:**
- Identify all claims involving numbers, timeframes, guarantees, health outcomes, pricing, or legal statements.
- For each claim, check: Is the condition stated within the same sentence as the claim?
- Flag claims where the condition is in a different sentence, a footnote, or a separate section.

**Scoring:**
- All conditions co-located with their claims: 10
- 1-2 conditions separated but nearby: 7-8
- Multiple conditions in separate paragraphs or footnotes: 5-6
- Conditions in fine print while claims are in headlines: 3-4
- Claims made without conditions entirely: 1-2

**Bad example:**
> "Our supplement reduces joint pain by 33%."
> [17 paragraphs later, in 9pt gray text]
> "*Results based on a single 90-day study in postmenopausal women with moderate osteoarthritis. Individual results may vary."

The claim will be extracted without the caveat. An LLM will state it as unconditional fact.

**Good example:**
> "In a 90-day trial of postmenopausal women with moderate osteoarthritis (n=120), UC-II collagen at 40mg/day reduced joint pain scores by 33% versus placebo — though results in other populations have not yet been studied."

Claim and condition live in the same sentence. Extraction preserves both.

---

## Part 4: Special Modules

### Module A: DRY Violation Check

Content that repeats the same claim in multiple locations wastes the grounding budget. An LLM pulling from a page with heavy repetition may use 3 of its approximately 380-word budget on three phrasings of the same point, leaving other important information unextracted.

**Procedure:**
- Search the page for the primary claim or value proposition.
- Count how many times it appears (exact repetition or close paraphrasing).
- Flag if the same claim appears more than twice.

**Acceptable:** Once in the intro, once in the conclusion (position architecture). **Unacceptable:** Repeated in the intro, two body paragraphs, a callout box, and the conclusion.

### Module B: Regulated Industry Content (Healthcare, Legal, Finance)

When auditing content in regulated verticals, add these additional checks:

1. **Qualification statements co-located with claims:** "Consult your doctor" cannot be only in the footer if health claims appear throughout.
2. **Temporal anchoring on all data:** Drug prices, interest rates, legal precedents — all must include "as of [date]" in the same sentence.
3. **Disclaimer extraction safety:** If the page has required disclaimers, verify they appear in the first or last 20% of the page, increasing their extraction probability.
4. **Source hierarchy:** Peer-reviewed > institutional > practitioner opinion > anecdotal. Flag pages where the strongest claims rely on the weakest source type.

### Module C: Over-Optimization Detection

Flag the page as "over-optimized for machines" if three or more of the following are true:

- Every sentence begins with the brand or product name.
- Zero use of second-person ("you") or reader-addressed language.
- No transitional phrases between paragraphs.
- All content is in bullet or table format with no prose.
- The page reads like a data sheet rather than a communication to a person.
- Sentence length variance is under 5 words (all sentences roughly the same length).

Flag the page as "over-optimized for humans" if three or more of the following are true:

- Heavy use of unresolved pronouns ("it," "this," "they") as sentence subjects.
- Claims lack named sources or specific numbers.
- Headings are clever/branded rather than descriptive.
- Key claims are buried in the middle 60% of the page.
- Conditions and caveats are separated from their claims by multiple paragraphs.
- Emotional language dominates with no verifiable specifics.

---

## Part 5: Report Template

```
====================================================
LLM READABILITY AUDIT REPORT
====================================================

Page: [URL]
Audited: [Date]
Word Count: [X] | Character Count: [X]
Page Type: [Landing / Product / Blog / Comparison / FAQ]
Industry: [General / Healthcare / Legal / Finance]
Target Queries: [List 3-5]

----------------------------------------------------
COMPOSITE SCORE: [X] / 100  |  Rating: [Strong / Functional / Underperforming / Broken]
Signal Imbalance Penalty Applied: [Yes / No]
Over-Optimization Flag: [None / Machine-biased / Human-biased]
----------------------------------------------------

DIMENSION SCORES
----------------------------------------------------
 #  | Dimension               | Score | Notes
----|-------------------------|-------|------------------
 1  | Position Architecture   | X/10  |
 2  | Sentence Sovereignty    | X/10  |
 3  | Entity Completeness     | X/10  |
 4  | Relationship Clarity    | X/10  |
 5  | Trust Infrastructure    | X/10  |
 6  | Format Diversity        | X/10  |
 7  | Conversion Mechanics    | X/10  |
 8  | Natural Language Quality | X/10  |
 9  | Heading Taxonomy        | X/10  |
10  | Condition Preservation  | X/10  |
----------------------------------------------------

EXTRACTION SIMULATION RESULTS
----------------------------------------------------
Sentences tested: 5
Sovereign: [X] / 5
Failed sentences:
  - "[Sentence]" — Failure reason: [unresolved pronoun / missing subject / etc.]
  - "[Sentence]" — Failure reason: [...]

COMPETITIVE DIFFERENTIATION TEST
----------------------------------------------------
Query 1: "[query]"
  Citable sentence found: [Yes/No]
  Sentence: "[...]"

Query 2: "[query]"
  Citable sentence found: [Yes/No]
  Sentence: "[...]"

[Repeat for all target queries]

DRY VIOLATIONS
----------------------------------------------------
Repeated claim: "[claim]"
  Locations: [paragraph X, paragraph Y, callout box Z]
  Recommendation: Consolidate to intro + conclusion only.

[Repeat for each violation]

REGULATED CONTENT FLAGS (if applicable)
----------------------------------------------------
[List any issues from Module B]

====================================================
PRIORITIZED FIXES
====================================================

PRIORITY 1 — FIX IMMEDIATELY (score impact: high, effort: low)
----------------------------------------------------

Fix 1.1: [Dimension affected]
  Location: [Section / paragraph / sentence]
  Current:
    "[Exact current text]"
  Rewrite:
    "[Exact replacement text]"
  Why: [1-sentence rationale — what signal this fixes]

Fix 1.2: [...]

PRIORITY 2 — FIX THIS WEEK (score impact: high, effort: medium)
----------------------------------------------------

Fix 2.1: [...]

PRIORITY 3 — FIX WHEN POSSIBLE (score impact: moderate, effort: varies)
----------------------------------------------------

Fix 3.1: [...]

ITEMS TO LEAVE ALONE
----------------------------------------------------
[List any sections that are already strong and should
not be touched — prevents well-meaning editors from
breaking what works.]

====================================================
ESTIMATED SCORE AFTER FIXES: [X] / 100
====================================================
```

---

## Part 6: Auditor Rules

1. **Never sacrifice clarity for extractability.** If making a sentence sovereign makes it awkward, find a rewrite that achieves both. There is always one.

2. **The brand name test:** If you replaced every instance of the brand name with a competitor's name and the content still worked, the page has no real differentiation. Flag it.

3. **The 380-word test:** If an LLM could only extract 380 words from this page, would those words contain the page's most important claims? If not, restructure.

4. **The screenshot test:** If you took a screenshot of the page and showed it to someone for 8 seconds, would they understand what the page is about and what to do next? If not, conversion mechanics need work.

5. **The phone-a-friend test:** Read the page's opening paragraph aloud to someone unfamiliar with the topic. If they ask "what are you talking about?" within the first two sentences, entity completeness or natural language quality is failing.

6. **Rewrites must preserve voice.** The audit corrects structural problems. It does not flatten the brand's tone into generic corporate language. Every rewrite should match the existing voice while fixing the identified issue.

7. **Flag, don't fabricate.** If a claim needs a source and none exists, flag it as "source needed" in the report. Do not invent citations, numbers, or credentials.

8. **One fix, one problem.** Each rewrite in the prioritized fix list should address exactly one dimension. If a sentence has three problems, write three sequential rewrites, each building on the last, so the editor understands what changed and why.

---

## Part 7: Quick-Reference Checklist (for ongoing content production)

Before publishing any page, the writer or editor should confirm:

- [ ] The single most important claim appears in the first 20% of the page.
- [ ] Every sentence with a pronoun subject ("it," "this," "they") has been checked — can it stand alone?
- [ ] Every claim with a number includes its source, timeframe, and population in the same sentence.
- [ ] The page uses at least 3 content formats (prose, list, table, FAQ, blockquote).
- [ ] Every heading describes what the section contains, not a clever metaphor.
- [ ] At least one sentence per section is directly quotable — specific, sourced, self-contained.
- [ ] The page addresses the reader as "you" at least once per scroll-depth.
- [ ] No claim is repeated more than twice on the page.
- [ ] Conditions and caveats share a sentence with the claims they qualify.
- [ ] Reading the page aloud takes under 4 minutes (under 800 words) or the page is chunked with clear headings for longer content.

---

*This methodology treats AI citation and human conversion as two expressions of the same underlying principle: content that is clear, specific, complete, and trustworthy serves both audiences. The audit does not ask writers to choose a signal. It asks them to write with enough precision that both signals are satisfied by the same text.*
