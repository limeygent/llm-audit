

# LLM Readability Audit: Model-Perspective Methodology

## Version 1.0 — A Mechanistic Framework for Content Citability

---

## Preamble: Why This Audit Exists

When an LLM answers a user query, it does not "read" a page the way a human does. It operates under hard constraints: a finite grounding budget, a chunking process that shreds context, and a confidence threshold below which it will not cite. This audit reverse-engineers those constraints into testable checks. Every check maps to a specific failure mode in one of three citation gates: **Retrieval**, **Ranking**, or **Citation**.

---

## The Three Citation Gates (Reference Framework)

| Gate | Core Question | Failure = |
|---|---|---|
| **G1: Retrieval** | Does this content surface in the candidate set at all? | Invisible. The LLM never sees it. |
| **G2: Ranking** | Does it score higher than competing chunks on the same query? | Buried. The LLM sees it but prefers a competitor's content. |
| **G3: Citation** | Can the LLM confidently attribute a claim to this source? | Unquotable. The LLM saw it, preferred it, but cannot safely use it. |

A page must pass all three gates sequentially. Failure at any gate is total for that query.

---

## Audit Procedure: 12 Checks in 4 Phases

### Phase 1: Structural Fitness (Retrieval Gate)

These checks determine whether the page's architecture allows its most important content to survive chunking and enter the candidate set.

---

#### Check 1: Answer-First Position Compliance

**Gate tested:** G1 — Retrieval

**Mechanism:** LLMs process retrieved chunks with measurable position bias. Liu et al. (2023) demonstrated that content in the first and last 20% of a document is extracted with significantly higher fidelity than content in the middle. Separately, Petrovic/DEJAN (2025) found that approximately 380 words are selected per page from a grounding budget of roughly 1,900 words per query across approximately 5 sources. If the primary answer sits in the middle 60% of a long page, it may fall outside the selection window entirely.

**Procedure:**

1. Identify the page's primary claim or answer (the single sentence a user would quote).
2. Calculate its character offset from the start of the body content.
3. Calculate total body content length in characters.
4. Compute position ratio: `offset / total_length`.

**Scoring (0-10):**

| Position Ratio | Score | Rationale |
|---|---|---|
| 0.00 - 0.10 | 10 | Within first 10%. Maximum extraction probability. |
| 0.11 - 0.20 | 8 | Within first 20%. Still in the high-fidelity zone. |
| 0.21 - 0.40 | 5 | Approaching the middle. Extraction degrades. |
| 0.41 - 0.60 | 2 | "Lost in the middle" zone. Severe extraction penalty. |
| 0.61 - 0.80 | 4 | Approaching the end. Moderate recency benefit. |
| 0.81 - 1.00 | 7 | Final 20%. Benefits from recency effect. |

**Fix template:** Move the primary answer to the first paragraph of body content. Use the AI Inverted Pyramid: answer, then context, then evidence, then elaboration under subheadings.

---

#### Check 2: Chunk Boundary Resilience

**Gate tested:** G1 — Retrieval

**Mechanism:** Retrieval systems chunk pages at boundaries (headings, paragraph breaks, token limits). If a key claim spans two chunks — for example, a condition stated in one paragraph and the claim it governs in the next — neither chunk is self-sufficient. Dense X Retrieval (Chen et al., 2024) showed that proposition-level indexing outperforms passage-level precisely because propositions are self-contained. Content that depends on cross-chunk resolution is functionally invisible.

**Procedure:**

1. Segment the page into chunks using two methods: (a) by heading sections, (b) by a sliding window of 512 tokens with 64-token overlap.
2. For each chunk, count the number of sentences that require information from outside the chunk to be fully understood. Flag: backward references ("as mentioned above"), split conditionals ("if" in one chunk, consequence in another), tables separated from their headers.
3. Compute: `resilience_score = 1 - (dependent_sentences / total_sentences)`.

**Scoring (0-10):** Multiply resilience_score by 10, round to nearest integer.

| Resilience Score | Page Score | Interpretation |
|---|---|---|
| 0.90 - 1.00 | 9 - 10 | Chunks are self-sufficient. |
| 0.70 - 0.89 | 7 - 8 | Minor cross-boundary dependencies. |
| 0.50 - 0.69 | 5 - 6 | Significant information loss at boundaries. |
| Below 0.50 | 0 - 4 | Most chunks are incomplete without context. |

**Fix template:** Restate the subject and any governing conditions at the start of each section. Never let a conditional span a heading boundary. Repeat table headers or column labels if a table could be split.

---

#### Check 3: Character-Length Budget Fit

**Gate tested:** G1 — Retrieval

**Mechanism:** Petrovic/DEJAN (2025) quantified coverage decay: pages under 5,000 characters achieved 66% content coverage in LLM grounding; pages over 20,000 characters dropped to 12%. This is not a style preference — it is a mathematical consequence of a fixed selection budget applied to varying content lengths. A 25,000-character page competing against a 3,000-character page on the same query will have roughly one-fifth the coverage, meaning four-fifths of its content is never evaluated.

**Procedure:**

1. Count total body content characters (excluding navigation, footers, boilerplate).
2. If the page serves multiple intents (see Check 12), evaluate whether it should be split.

**Scoring (0-10):**

| Character Count | Score | Coverage Estimate |
|---|---|---|
| Under 2,000 | 6 | High coverage but may lack sufficient depth for ranking. |
| 2,000 - 5,000 | 10 | Optimal zone. ~66% coverage. |
| 5,001 - 10,000 | 7 | Moderate dilution. ~40% coverage. |
| 10,001 - 20,000 | 4 | Significant dilution. ~20% coverage. |
| Over 20,000 | 2 | Severe dilution. ~12% coverage. |

**Fix template:** For pages over 10,000 characters, identify distinct query intents served and split into focused pages. If a single long page is unavoidable, front-load all primary claims within the first 2,000 characters and use the remainder as supporting evidence.

---

### Phase 2: Selection and Ranking Fitness (Ranking Gate)

These checks determine whether, once retrieved, the content scores higher than competing sources.

---

#### Check 4: Proposition Density

**Gate tested:** G2 — Ranking

**Mechanism:** Within the ~380-word selection window per page, every word either advances a citable claim or dilutes one. Dense X Retrieval (Chen et al., 2024) demonstrated that decomposing passages into atomic propositions improves retrieval precision because each proposition directly matches a query facet. Filler text (throat-clearing introductions, generic context everyone knows, transitional padding) consumes budget without adding retrievable propositions. Bagga et al. (2025) confirmed this: minimalist rewriting — stripping content to bare facts — scored second-worst of 15 strategies, but the failure was in stripping too much context, not in being dense. The optimum is high density with sufficient context.

**Procedure:**

1. Sample the first 400 words of body content (approximating the LLM's selection window for this page).
2. Count atomic propositions: statements that could independently answer or partially answer a search query. A proposition must contain a subject, a relationship, and an object or value.
3. Count filler sentences: sentences that contain no proposition (e.g., "In this article, we will explore...", "It is important to note that...", "Let's take a closer look.").
4. Compute: `density = propositions / total_sentences_in_sample`.

**Scoring (0-10):**

| Density Ratio | Score | Interpretation |
|---|---|---|
| 0.85 - 1.00 | 10 | Nearly every sentence carries a proposition. |
| 0.70 - 0.84 | 8 | Strong density with minor filler. |
| 0.50 - 0.69 | 5 | Half the budget consumed by non-propositional content. |
| 0.30 - 0.49 | 3 | Severe dilution. Competitor content likely outranks. |
| Below 0.30 | 1 | Page is mostly filler in the selection window. |

**Fix template:** Delete or relocate sentences scoring zero propositions. Replace "It is important to understand that X affects Y" with "X affects Y." Move contextual setup below the first propositional paragraph.

---

#### Check 5: Competitive Differentiation Signal

**Gate tested:** G2 — Ranking

**Mechanism:** When multiple pages answer the same query, the LLM must select among them. Content that restates what every competitor says provides no ranking advantage — the LLM has no reason to prefer it. Eikhart's second utility principle identifies competitive differentiation as a ranking factor: the LLM favors sources that provide information not available elsewhere or that state common information with greater specificity.

**Procedure:**

1. Identify the page's target query (or top 3 queries).
2. For each query, identify the consensus answer across the top 5 competing pages (the "commodity answer").
3. Count unique propositions on the audited page that are absent from the commodity answer. These are: proprietary data, original research findings, specific numerical claims with attribution, unique methodologies, named frameworks.
4. Compute: `differentiation_ratio = unique_propositions / total_propositions`.

**Scoring (0-10):**

| Differentiation Ratio | Score |
|---|---|
| 0.40+ | 10 — Strongly differentiated. |
| 0.25 - 0.39 | 7 — Moderate differentiation. |
| 0.10 - 0.24 | 4 — Mostly commodity content. |
| Below 0.10 | 1 — Fully substitutable. |

**Fix template:** Add at least 3 propositions per target query that no competitor provides. Prioritize: original data with specific numbers, named frameworks or methodologies, direct experience statements with verifiable details.

---

#### Check 6: Heading-Query Alignment

**Gate tested:** G2 — Ranking

**Mechanism:** Headings receive approximately 17.54% relevance boost in retrieval scoring (per empirical measurement). This is not cosmetic — headings are weighted as section-level topic signals during both chunking and relevance scoring. A heading that matches query language directly increases the probability that its section ranks above a competitor's section that contains the same information under a vague heading.

**Procedure:**

1. List all H1-H3 headings on the page.
2. For each target query, assess whether a heading contains the query's key entities and intent.
3. Flag headings that are clever/branded but do not contain query-relevant terms (e.g., "Our Secret Sauce" instead of "Pricing Model for Enterprise SaaS").
4. Compute: `alignment_ratio = query-aligned_headings / total_headings`.

**Scoring (0-10):**

| Alignment Ratio | Score |
|---|---|
| 0.80+ | 10 |
| 0.60 - 0.79 | 7 |
| 0.40 - 0.59 | 5 |
| Below 0.40 | 2 |

**Fix template:** Rewrite each heading to contain the primary entity and intent of the section's target query. Preserve brand terms as secondary modifiers, not primary heading content. Example: "Our Secret Sauce" becomes "Enterprise SaaS Pricing Model: The [Brand] Approach."

---

### Phase 3: Extractability (Citation Gate)

These checks determine whether the LLM can confidently quote, paraphrase, or attribute claims from the content.

---

#### Check 7: Sentence Independence (Coreference Resolution)

**Gate tested:** G3 — Citation

**Mechanism:** This is the single most important citation-gate check. Dense X Retrieval (Chen et al., 2024) identified unresolved coreference as the primary failure mode in proposition extraction. When a sentence uses "it," "they," "this," "these," "the company," or "the product" without the referent being present in the same sentence, the LLM cannot safely attribute the claim. It does not know what "it" refers to once the sentence is extracted from context.

**Procedure:**

1. Examine every sentence in the page's primary content sections (first 2,000 words minimum).
2. For each sentence, test: if this sentence were extracted alone and shown to someone with no context, would every noun phrase resolve unambiguously?
3. Flag: pronouns without in-sentence antecedents, demonstrative references ("this approach," "these results"), definite articles referring to previously introduced entities ("the study," "the tool"), elliptical constructions.
4. Compute: `independence_ratio = fully_independent_sentences / total_sentences`.

**Scoring (0-10):**

| Independence Ratio | Score |
|---|---|
| 0.90+ | 10 |
| 0.75 - 0.89 | 7 |
| 0.60 - 0.74 | 5 |
| 0.40 - 0.59 | 3 |
| Below 0.40 | 1 |

**Fix template (sentence-level rewrites):**

| Before | Problem | After |
|---|---|---|
| "It reduces processing time by 40%." | Unresolved "it." | "[Product Name] reduces processing time by 40%." |
| "This approach works well for enterprise teams." | Vague demonstrative. | "Role-based access control works well for enterprise teams." |
| "The study found a 3x improvement." | Unidentified study. | "MIT's 2024 retrieval benchmark found a 3x improvement." |
| "They support over 50 integrations." | Unresolved "they." | "Acme Platform supports over 50 integrations." |

---

#### Check 8: S-V-O Triple Completeness

**Gate tested:** G3 — Citation

**Mechanism:** HippoRAG (Gutierrez et al., 2024) demonstrated that LLMs extract Subject-Verb-Object triples more accurately than verb-less fragments or noun-phrase-only constructions. A sentence like "AI-powered analytics for real-time decision-making" contains no extractable triple — there is no subject performing an action on an object. The LLM cannot convert this into a citable claim because there is no stated relationship.

**Procedure:**

1. Parse each sentence in the primary content for the presence of: explicit subject, active verb, explicit object or complement.
2. Flag sentences that are: noun-phrase lists without verbs, passive constructions with deleted agents ("costs are reduced"), gerund phrases posing as sentences ("Leveraging AI to drive outcomes"), headline fragments used as body text.
3. Compute: `svo_ratio = complete_SVO_sentences / total_sentences`.

**Scoring (0-10):**

| S-V-O Ratio | Score |
|---|---|
| 0.85+ | 10 |
| 0.70 - 0.84 | 7 |
| 0.50 - 0.69 | 5 |
| Below 0.50 | 2 |

**Fix template:**

| Before | Problem | After |
|---|---|---|
| "AI-powered analytics for real-time decisions." | No verb, no subject. | "Acme's analytics engine processes streaming data in under 200ms." |
| "Costs are reduced significantly." | Deleted agent, vague degree. | "Acme reduces infrastructure costs by 35% compared to self-hosted Elasticsearch." |
| "Leveraging machine learning to optimize workflows." | Gerund fragment, no subject. | "The platform uses gradient-boosted models to route tickets to the correct team." |

---

#### Check 9: Claim Anchorability

**Gate tested:** G3 — Citation

**Mechanism:** An LLM will not cite a claim it cannot verify as specific and bounded. Eikhart's fifth utility principle — anchorable statements — requires that claims contain enough specificity (numbers, named entities, conditions, timeframes) that the LLM can commit to them without risk of misrepresentation. Relative claims without baselines ("50% faster"), conditional claims without stated conditions ("works great for teams"), and superlatives without scope ("the best solution") all fail this test because the LLM cannot determine their truth boundaries.

**Procedure:**

1. Identify all claims in the content (statements asserting a fact, capability, comparison, or outcome).
2. For each claim, check for the presence of:
   - **Specificity anchor**: a number, named entity, date, or scope delimiter.
   - **Baseline** (for comparative claims): "faster than X," "compared to Y."
   - **Conditions** (for conditional claims): "when used with," "for teams of N+," "in scenarios where."
   - **Source** (for factual claims): attribution to a study, dataset, or verifiable origin.
3. Score each claim: 1 point for each anchor present (max 4 per claim if all four categories apply).
4. Compute: `anchorability = total_anchor_points / (total_claims * max_applicable_anchors_per_claim)`.

**Scoring (0-10):**

| Anchorability | Score |
|---|---|
| 0.75+ | 10 |
| 0.55 - 0.74 | 7 |
| 0.35 - 0.54 | 4 |
| Below 0.35 | 1 |

**Fix template:**

| Before | Problem | After |
|---|---|---|
| "50% faster processing." | No baseline. | "50% faster processing than Apache Kafka for streams under 10K events/sec." |
| "Works great for enterprise teams." | No conditions or specificity. | "Reduces mean ticket resolution time by 28% for support teams handling 500+ tickets/day." |
| "The leading platform in the space." | Unscoped superlative. | "Ranked #1 in G2's 2025 Winter Grid for mid-market ITSM platforms (4.7/5, 340 reviews)." |

---

#### Check 10: Condition Preservation

**Gate tested:** G3 — Citation (with special relevance to regulated industries)

**Mechanism:** When an LLM extracts a claim, it strips surrounding context. If a claim's validity depends on a condition stated in a preceding sentence or paragraph, the extracted claim becomes unconditionally stated — and potentially false or misleading. This is especially dangerous in regulated industries (healthcare, finance, legal) where stripped conditions can create liability. The extractability pitfall of "stripped conditions" and "assumed knowledge" directly causes this failure.

**Procedure:**

1. Identify all conditional claims: statements whose truth depends on a prerequisite, limitation, timeframe, jurisdiction, dosage, audience, or other qualifier.
2. For each conditional claim, check: is the condition stated within the same sentence as the claim?
3. Flag claims where the condition is in a different sentence, a footnote, a preceding paragraph, or a page-level disclaimer.
4. Compute: `condition_preservation_ratio = self_contained_conditional_claims / total_conditional_claims`.

**Scoring (0-10):**

| Preservation Ratio | Score | Regulatory Modifier |
|---|---|---|
| 0.90+ | 10 | No modifier needed. |
| 0.70 - 0.89 | 7 | Subtract 2 if regulated industry. |
| 0.50 - 0.69 | 4 | Subtract 3 if regulated industry. |
| Below 0.50 | 1 | Automatic 0 if regulated industry. |

**Regulated industry flag:** If the page concerns healthcare, pharmaceuticals, financial advice, legal guidance, or safety-critical information, apply the regulatory modifier. A stripped condition in these domains is not just a ranking issue — it is a misinformation vector.

**Fix template:**

| Before | Problem | After |
|---|---|---|
| "Patients saw a 60% improvement. *Note: results based on a 12-week trial of adults aged 30-55 with moderate symptoms.*" | Condition in a separate sentence/footnote. | "Adults aged 30-55 with moderate symptoms saw a 60% improvement over 12 weeks in a controlled trial (n=450)." |
| "Returns averaged 12% annually." (Page disclaimer: "Past performance does not guarantee future results.") | Condition is page-level boilerplate, stripped during extraction. | "The fund returned an average of 12% annually from 2019-2024; past performance does not guarantee future results." |

---

### Phase 4: Entity and Format Fitness

---

#### Check 11: Entity Completeness and Consistency

**Gate tested:** G1 (Retrieval) and G3 (Citation)

**Mechanism:** LLMs match content to queries through entity recognition. If a page refers to the same entity by multiple names without establishing equivalence (e.g., "Acme Corp," "Acme," "the company," "our platform," "the solution"), the LLM may fail to associate all references with the queried entity (retrieval failure) or may be unable to confidently attribute a claim to a specific entity (citation failure).

**Procedure:**

1. List all entities on the page: company names, product names, person names, technical terms.
2. For each entity, count the number of variant forms used.
3. Check whether equivalence is explicitly stated on first variant use (e.g., "Acme Corp (hereafter 'Acme')").
4. Check whether the canonical form is used at least once per section/chunk boundary.
5. Compute: `consistency_ratio = sections_with_canonical_entity / total_sections`.

**Scoring (0-10):**

| Consistency Ratio | Score |
|---|---|
| 0.90+ | 10 |
| 0.70 - 0.89 | 7 |
| 0.50 - 0.69 | 4 |
| Below 0.50 | 2 |

**Fix template:** Establish canonical names in the first sentence. Reintroduce the full canonical name after every heading. Reserve pronouns and short forms for within-sentence use only when the canonical name appears in the same sentence.

---

#### Check 12: Format-Appropriate Structure and Multi-Intent Separation

**Gate tested:** G1 (Retrieval) and G2 (Ranking)

**Mechanism:** Different content formats have different extraction fidelity. Tables are extracted as structured data when they have clear headers and consistent columns, but they fail when headers are missing or merged cells create ambiguity. Lists extract well when each item is self-contained but fail when items depend on a lead-in sentence that may be chunked separately. Prose extracts well for narrative claims but poorly for comparative data that would be clearer in a table. Multi-intent pages (a single page answering "what is X," "how much does X cost," and "X vs. Y") force the LLM to chunk-select across competing sections, diluting each intent's ranking signal.

**Procedure:**

1. **Format audit**: For each content block, assess whether the format matches the content type:
   - Comparative data (features, pricing, specs) should be in tables with explicit headers.
   - Sequential processes should be in numbered lists with self-contained steps.
   - Definitions and explanations should be in prose with S-V-O sentences.
   - Collections of independent items should be in bullet lists with full sentences per item.
2. **Multi-intent audit**: Count the number of distinct query intents the page serves. For each intent, check whether it has its own heading-delimited section and whether that section could stand alone as a chunk.
3. **Table integrity check**: For each table, verify: column headers present, no merged cells, each cell is self-explanatory without reading the surrounding prose.
4. **List integrity check**: For each list, verify: the lead-in sentence is not required to understand any list item, each item is a complete sentence or complete phrase.

**Scoring (0-10):**

| Sub-check | Weight | Scoring |
|---|---|---|
| Format-content match | 40% | 10 if all blocks use appropriate format; subtract 2 per mismatched block (min 0). |
| Multi-intent separation | 30% | 10 if each intent has its own section; 5 if intents are partially mixed; 0 if intents are interleaved. |
| Table integrity | 15% | 10 if all tables have headers and no merged cells; 0 if any table lacks headers. |
| List integrity | 15% | 10 if all list items are self-contained; 0 if items depend on lead-in context. |

Weighted average produces the check score.

**Fix template:** Split multi-intent pages when they serve 3+ distinct query intents and exceed 10,000 characters. Convert comparative prose to tables. Ensure every list item begins with its subject, not a pronoun or continuation word.

---

## Composite Scoring Model

### Weight Distribution

| Check | Gate | Weight | Rationale |
|---|---|---|---|
| 1. Answer-First Position | G1 | 10% | Position determines whether content enters the selection window. |
| 2. Chunk Boundary Resilience | G1 | 8% | Cross-chunk dependency destroys proposition integrity. |
| 3. Character-Length Budget Fit | G1 | 8% | Coverage percentage is mechanistically determined by length. |
| 4. Proposition Density | G2 | 10% | Density directly determines value per budget-word. |
| 5. Competitive Differentiation | G2 | 10% | Substitutable content has no ranking advantage. |
| 6. Heading-Query Alignment | G2 | 7% | Measured 17.54% relevance boost from aligned headings. |
| 7. Sentence Independence | G3 | 15% | Primary citation failure mode per Dense X Retrieval. |
| 8. S-V-O Completeness | G3 | 10% | Extractable triples are the unit of citation. |
| 9. Claim Anchorability | G3 | 8% | Unanchored claims cannot be confidently stated. |
| 10. Condition Preservation | G3 | 7% | Stripped conditions create false unconditional claims. |
| 11. Entity Completeness | G1+G3 | 4% | Entity inconsistency fragments retrieval and attribution. |
| 12. Format and Multi-Intent | G1+G2 | 3% | Format mismatch reduces extraction fidelity. |
| **Total** | | **100%** | |

### Score Interpretation

| Composite Score | Grade | Interpretation |
|---|---|---|
| 85 - 100 | A | Content is structurally optimized for LLM retrieval, ranking, and citation. |
| 70 - 84 | B | Content is broadly citable with specific weaknesses to address. |
| 55 - 69 | C | Content has systemic issues in at least one gate. Partial citability. |
| 40 - 54 | D | Content fails multiple gate checks. Unlikely to be cited over competitors. |
| Below 40 | F | Content is functionally invisible or uncitable. Requires structural rewrite. |

### Gate-Level Subtotals

In addition to the composite score, compute gate-level subtotals to identify which gate is the bottleneck:

- **G1 Retrieval subtotal** = weighted sum of Checks 1, 2, 3, 11 (retrieval portion), 12 (retrieval portion)
- **G2 Ranking subtotal** = weighted sum of Checks 4, 5, 6, 12 (ranking portion)
- **G3 Citation subtotal** = weighted sum of Checks 7, 8, 9, 10, 11 (citation portion)

The lowest gate subtotal identifies the primary bottleneck. Fixes should prioritize the weakest gate because gates are sequential — a high ranking score is worthless if the content fails retrieval.

---

## Audit Report Template

```
================================================================
LLM READABILITY AUDIT REPORT
================================================================

Page URL:        [URL]
Audit Date:      [Date]
Auditor:         [Name/System]
Target Queries:  [Query 1], [Query 2], [Query 3]
Industry:        [General / Regulated: specify]
Page Length:      [X] characters / [Y] words

================================================================
COMPOSITE SCORE: [XX]/100 — Grade [X]
================================================================

GATE SUBTOTALS:
  G1 Retrieval:   [XX]/100 — [PASS/BOTTLENECK]
  G2 Ranking:     [XX]/100 — [PASS/BOTTLENECK]
  G3 Citation:    [XX]/100 — [PASS/BOTTLENECK]

Primary Bottleneck: [Gate X — brief explanation]

================================================================
DETAILED SCORES
================================================================

PHASE 1: STRUCTURAL FITNESS (Retrieval)
---------------------------------------
Check 1  — Answer-First Position:     [X]/10
  Finding: [Primary answer at position ratio X.XX]
  Fix:     [Specific instruction or "No action needed"]

Check 2  — Chunk Boundary Resilience:  [X]/10
  Finding: [X of Y sentences are chunk-dependent]
  Fix:     [Specific instruction or "No action needed"]

Check 3  — Character-Length Budget:    [X]/10
  Finding: [X characters, estimated Y% coverage]
  Fix:     [Specific instruction or "No action needed"]

PHASE 2: SELECTION & RANKING (Ranking)
--------------------------------------
Check 4  — Proposition Density:        [X]/10
  Finding: [X propositions in Y sentences = Z ratio]
  Fix:     [Specific instruction or "No action needed"]

Check 5  — Competitive Differentiation: [X]/10
  Finding: [X unique propositions out of Y total]
  Fix:     [Specific instruction or "No action needed"]

Check 6  — Heading-Query Alignment:    [X]/10
  Finding: [X of Y headings align with target queries]
  Fix:     [Specific instruction or "No action needed"]

PHASE 3: EXTRACTABILITY (Citation)
----------------------------------
Check 7  — Sentence Independence:      [X]/10  [CRITICAL]
  Finding: [X of Y sentences have unresolved references]
  Examples:
    Line [N]: "[sentence]" — [problem]
    Line [N]: "[sentence]" — [problem]
  Fix:     [Specific rewrites]

Check 8  — S-V-O Completeness:        [X]/10
  Finding: [X of Y sentences lack complete S-V-O triples]
  Examples:
    Line [N]: "[fragment]" — [problem]
  Fix:     [Specific rewrites]

Check 9  — Claim Anchorability:        [X]/10
  Finding: [X of Y claims lack anchors]
  Examples:
    "[claim]" — Missing: [baseline/condition/source/specificity]
  Fix:     [Specific rewrites]

Check 10 — Condition Preservation:     [X]/10
  Finding: [X conditional claims with separated conditions]
  Regulatory flag: [Yes/No — if yes, modifier applied]
  Fix:     [Specific rewrites]

PHASE 4: ENTITY & FORMAT FITNESS
---------------------------------
Check 11 — Entity Completeness:        [X]/10
  Finding: [Entity X appears as Y variants across Z sections]
  Fix:     [Specific instruction or "No action needed"]

Check 12 — Format & Multi-Intent:      [X]/10
  Finding: [X intents on page; format mismatches at Y locations]
  Fix:     [Specific instruction or "No action needed"]

================================================================
PRIORITY FIXES (ordered by impact)
================================================================

1. [Highest-impact fix — gate, check number, specific action]
2. [Second-highest fix]
3. [Third-highest fix]
4. [Fourth fix]
5. [Fifth fix]

================================================================
REWRITE EXAMPLES
================================================================

BEFORE (Line X):
"[Original sentence]"

AFTER:
"[Rewritten sentence]"

MECHANISM: [Which gate this fixes and why]

---

BEFORE (Line X):
"[Original sentence]"

AFTER:
"[Rewritten sentence]"

MECHANISM: [Which gate this fixes and why]

---

[Repeat for top 5-10 most impactful rewrites]

================================================================
NOTES
================================================================

- [Any page-specific observations]
- [Competitor comparison notes]
- [Regulated industry considerations if applicable]
```

---

## Execution Guidelines

### When to Run This Audit

- Before publishing any page targeting queries where LLM citation is a business goal.
- After competitive analysis reveals a page is not being cited despite ranking in traditional search.
- Quarterly, on high-value pages, as LLM retrieval mechanisms evolve.

### Who Runs It

This audit can be performed manually by a content strategist using the check procedures above, or automated with the following approach:

- Checks 1, 3, 6, 11: Fully automatable via parsing.
- Checks 2, 4, 7, 8, 12: Automatable via NLP pipeline (dependency parsing, coreference resolution, SVO extraction).
- Checks 5, 9, 10: Require human judgment or LLM-assisted evaluation (competitive analysis, condition identification).

### DRY Principle Application

Several checks share underlying analyses. To avoid redundant work:

- **Sentence parse** (used by Checks 4, 7, 8, 9, 10): Parse all sentences once. Tag each with: proposition count, independence status, SVO completeness, claim anchors, condition status.
- **Chunk simulation** (used by Checks 2, 12): Perform chunking once, reuse boundaries for both checks.
- **Entity list** (used by Checks 7, 11): Build entity registry once, reference it for both coreference resolution and consistency checks.

---

## Appendix: Research Grounding Summary

| Check | Primary Research Basis | Mechanism |
|---|---|---|
| 1 | Liu et al. 2023 "Lost in the Middle" | Position-dependent extraction fidelity |
| 2 | Chen et al. 2024 Dense X Retrieval | Proposition self-containment at chunk boundaries |
| 3 | Petrovic/DEJAN 2025 | Fixed grounding budget vs. variable page length |
| 4 | Chen et al. 2024; Bagga et al. 2025 | Proposition density determines per-word value |
| 5 | Eikhart Utility Principle 2 | Substitutable content has no selection advantage |
| 6 | Empirical heading boost measurement | 17.54% relevance weight on heading text |
| 7 | Chen et al. 2024 Dense X Retrieval | Unresolved coreference is primary extraction failure |
| 8 | Gutierrez et al. 2024 HippoRAG | S-V-O triples extracted more accurately than fragments |
| 9 | Eikhart Utility Principle 5 | Confidence threshold requires anchored specificity |
| 10 | Extractability pitfalls research | Stripped conditions create false unconditional claims |
| 11 | Entity recognition in retrieval matching | Inconsistent naming fragments entity resolution |
| 12 | Format-dependent extraction fidelity | Tables, lists, prose have different extraction accuracy |
