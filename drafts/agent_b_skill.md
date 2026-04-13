

# LLM Readability Audit Methodology

## Complete Skill Specification v1.0

---

## 1. Purpose and Scope

This methodology scores any web page on how effectively its content will be retrieved, ranked, and cited by AI systems (ChatGPT, Gemini, Perplexity, Claude, etc.) during grounded generation. It produces a 0-100 composite score across five diagnostic lenses, with sentence-level diagnostics and a prioritized fix list.

The methodology is page-type agnostic. It applies to landing pages, blog posts, product pages, service descriptions, legal/medical content, comparison pages, and documentation.

---

## 2. Audit Workflow — Ordered Steps

### Step 1: Page Classification and Intent Mapping

Before scoring, classify the page to calibrate expectations.

1. **Identify page type:** Service, product, blog/article, comparison, FAQ, documentation, legal/regulatory, homepage.
2. **Map query intents served.** List every distinct query a reasonable user might issue that this page should answer. A product page might serve "what is [product]", "[product] vs [competitor]", "[product] pricing", "[product] for [use case]". Aim for 3-8 intents per page.
3. **For each intent, identify the ideal extractable answer.** This is the 1-3 sentence passage an AI system would need to pull to answer that query. If that passage does not exist on the page, flag it as a **coverage gap**.

**Output:** Intent map table.

| # | Query Intent | Ideal Answer Location | Present? (Y/N) | Position (word offset) |
|---|---|---|---|---|
| 1 | "What does [brand] do?" | Paragraph 1 | Y | Words 1-45 |
| 2 | "[brand] pricing" | Pricing section | N | — |

---

### Step 2: Structural Fitness Analysis (Lens 1)

Score how well the page architecture supports retrieval.

#### 2a. Document Length Assessment

| Metric | Measurement | Scoring |
|---|---|---|
| Total word count | Count all body text | Under 1,900 words = +10; 1,900-3,500 = +7; 3,500-5,000 = +4; Over 5,000 = +0 |
| Total character count | Count all body characters | Under 5,000 chars = high coverage expected; Over 20,000 = flag for restructuring |
| Grounding budget ratio | 380 / total words | Above 20% = good; 10-20% = acceptable; Below 10% = poor — most content will be ignored |

**Rationale:** Petrovic's data shows coverage drops from 66% to 12% as pages exceed 20,000 characters. Shorter, denser pages win.

#### 2b. Information Architecture

| Check | Pass Criteria | Points |
|---|---|---|
| H1 present and unique | Exactly one H1 containing primary entity + primary intent | 0-2 |
| Heading hierarchy valid | No skipped levels (H1 > H2 > H3), no decorative headings | 0-2 |
| Headings contain query-aligned phrases | At least 60% of H2s match or paraphrase a mapped query intent | 0-3 |
| First 20% contains primary answer | The answer to the page's dominant intent appears in the first 20% of word count | 0-3 |
| Last 20% contains summary or CTA with entity restatement | Final section restates the entity + key claim (not just "contact us") | 0-2 |
| AI Inverted Pyramid followed | Answer precedes context, context precedes evidence, evidence precedes follow-up | 0-3 |

**Scoring:** /15 points, scaled to 0-20.

#### 2c. Position Audit

For each mapped query intent, record where its answer sits as a percentage of total document length.

- **First 20% or last 20%:** Optimal (Liu et al. — primacy/recency effect in context windows).
- **Middle 40%:** Penalized. Critical answers buried in the middle are least likely to influence generation.

Flag any intent whose answer sits entirely in the 30-70% range as **positionally vulnerable**.

---

### Step 3: Selection Likelihood Analysis (Lens 2)

Score how likely a retrieval system is to select this page's content over competitors.

#### 3a. Competitive Differentiation Check

For each mapped intent, evaluate whether the page content contains all four differentiation signals:

| Signal | Definition | Example (pass) | Example (fail) |
|---|---|---|---|
| **What** | Named product, service, or concept | "Acme Roof Coating" | "our solution" |
| **Who** | Named entity performing or providing | "Acme Industrial, a Memphis-based manufacturer" | "we" (unresolvable in extraction) |
| **What job** | Explicit problem solved or outcome delivered | "extends flat roof lifespan by 15 years" | "provides great results" |
| **What constraint** | Conditions, limits, qualifications, or scope | "for commercial buildings over 10,000 sq ft in USDA zones 5-8" | (absent) |

**Scoring per intent:**
- All 4 present in a single extractable passage: 5 points
- 3 of 4: 3 points
- 2 of 4: 1 point
- 1 or 0: 0 points

Average across all intents. Scale to 0-20.

#### 3b. Trust Signal Density

Count and evaluate:

| Trust Signal | Weight | Notes |
|---|---|---|
| Named author with credentials | 2 | Must be in body text, not just byline metadata |
| Publication or review date | 1 | Must be human-readable, not just schema |
| Cited sources (links, references) | 1 per source, max 5 | External authoritative references |
| Specific statistics with attribution | 2 per stat, max 6 | "According to [source], [metric] is [value]" |
| Named certifications, awards, affiliations | 1 per, max 3 | Verifiable, not self-awarded |

**Maximum trust points:** 20. Record raw score.

---

### Step 4: Extractability Analysis (Lens 3)

This is the core diagnostic. Score every paragraph/sentence for survivability when extracted in isolation.

#### 4a. Sentence Independence Audit

Sample method: audit every sentence in the first 20%, last 20%, and all heading-adjacent paragraphs (first paragraph after each H2/H3). For pages under 1,000 words, audit every sentence.

For each sentence, check for these **extraction failure modes:**

| Failure Mode | Code | Example (fail) | Fix Pattern |
|---|---|---|---|
| Unresolved pronoun | EF-01 | "They offer three tiers." | Replace "They" with entity name |
| Vague demonstrative | EF-02 | "This makes it effective." | Replace "This" with the specific referent |
| Context-dependent claim | EF-03 | "The above method also works for steel." | Restate the method by name |
| Stripped condition | EF-04 | "Results are guaranteed." (but only under warranty) | Add the condition inline |
| Assumed knowledge | EF-05 | "Unlike the traditional approach..." | Name the traditional approach |
| Relative claim without baseline | EF-06 | "50% faster" | "50% faster than [named baseline]" |
| Hedging without specificity (regulated) | EF-07 | "May help with symptoms." | "May reduce joint inflammation symptoms in patients with mild osteoarthritis, per [study]." |
| Orphaned list item | EF-08 | "- Durability" (no verb, no context) | "Acme Coating delivers durability rated to 25-year exposure cycles." |

**Scoring:**
- Count total sentences audited.
- Count sentences with one or more failure modes.
- **Extractability rate** = (clean sentences / total audited) x 100.
- Scale: 90-100% = 20 points; 75-89% = 15; 60-74% = 10; 40-59% = 5; Below 40% = 0.

#### 4b. Proposition Density Check

A proposition is a self-contained factual claim (per Dense X Retrieval). Count the number of unique propositions per 100 words.

| Density | Rating | Points |
|---|---|---|
| 4+ propositions per 100 words | High | 5 |
| 2-3 per 100 words | Medium | 3 |
| Under 2 per 100 words | Low — content is padded | 1 |

**Warning:** Do NOT reward density achieved through oversimplification. If propositions drop critical conditions or nuance, they fail EF-04 and the extractability score corrects for this. E-GEO found minimalist rewriting scored second-worst because stripping nuance is functionally equivalent to fabrication.

---

### Step 5: Entity Completeness Analysis (Lens 4)

Score how well the page establishes its entities for knowledge graph construction.

#### 5a. Primary Entity Resolution

| Check | Pass | Fail |
|---|---|---|
| Primary entity named in H1 | "Acme Industrial Roof Coating" in H1 | "Our Premier Solution" |
| Primary entity named in first sentence of body | Full name used, not pronoun | Pronoun or abbreviated reference |
| Primary entity restated every 300 words | Full name or unambiguous short name | "it", "the product", "our service" |
| Entity type declared | "Acme Roof Coating is a silicone-based commercial roofing membrane" | No is-a statement |

**Scoring:** 0-4 checks passed, scale to 0-10.

#### 5b. Relationship Mapping (S-V-O Triple Audit)

HippoRAG and graph-based retrieval systems index Subject-Verb-Object triples. Audit whether the page's key claims are expressed as explicit S-V-O structures.

For each mapped intent, identify whether the answer contains a clear triple:

- **Subject:** Named entity (not pronoun).
- **Verb:** Active, specific (not "is related to", "involves", "pertains to").
- **Object:** Concrete outcome, metric, or entity.

**Example pass:** "Acme Roof Coating [S] extends [V] flat roof lifespan by 15 years [O]."
**Example fail:** "There are many benefits associated with proper roof maintenance."

**Scoring:** Percentage of intents with clean S-V-O answer triples. Scale to 0-10.

**Lens 4 total:** /20.

---

### Step 6: Natural Language Quality Analysis (Lens 5)

#### 6a. Readability Calibration

This is NOT about dumbing down. It is about matching linguistic complexity to the page's audience and the retrieval context.

| Check | Measurement | Target |
|---|---|---|
| Average sentence length | Word count / sentence count | 12-22 words (sweet spot for extraction) |
| Passive voice rate | Passive constructions / total sentences | Under 15% for commercial; under 30% for regulatory/legal |
| Jargon with inline definition | Technical terms defined on first use | 100% of domain-specific terms defined in same sentence or parenthetical |
| Transition dependency | Sentences beginning with "However," "Moreover," "Additionally," etc. | Under 10% — these signal the sentence depends on its predecessor |

#### 6b. Format Mix Assessment

| Check | Pass | Fail |
|---|---|---|
| No wall-of-text blocks (paragraphs over 80 words) | All paragraphs under 80 words | Any paragraph exceeding 80 words |
| Lists include verb phrases | Every bullet contains S-V or V-O minimum | Noun-only bullets ("Durability", "Speed") |
| Tables have descriptive headers | Column headers are full phrases | Single-word or abbreviated headers |
| Code/data blocks are labeled | Every block has a preceding sentence explaining what it shows | Unlabeled blocks |

#### 6c. DRY Principle (Don't Repeat Yourself)

Repetition wastes grounding budget. Flag any proposition stated more than twice on the same page. Each redundant restatement beyond the second costs 1 point (max -5 penalty).

**Lens 5 scoring:** Start at 20. Deduct for failures:
- Each readability metric outside target: -2
- Each format failure: -2
- DRY violations: -1 each, max -5
- Floor: 0.

---

## 3. Composite Scoring

| Lens | Max Points | Weight |
|---|---|---|
| 1. Structural Fitness | 20 | 20% |
| 2. Selection Likelihood | 20 | 20% |
| 3. Extractability | 20 | 25% |
| 4. Entity Completeness | 20 | 20% |
| 5. Natural Language Quality | 20 | 15% |

**Composite Score** = (L1 x 0.20) + (L2 x 0.20) + (L3 x 0.25) + (L4 x 0.20) + (L5 x 0.15), scaled to 0-100.

### Score Interpretation

| Score | Grade | Interpretation |
|---|---|---|
| 85-100 | A | Content is retrieval-optimized. Minor refinements only. |
| 70-84 | B | Structurally sound. Sentence-level extraction issues to fix. |
| 55-69 | C | Significant gaps. Likely losing citations to competitors with cleaner content. |
| 40-54 | D | Major restructuring needed. AI systems will struggle to extract reliable answers. |
| Below 40 | F | Content is functionally invisible to AI retrieval. Rewrite recommended. |

---

## 4. Diagnostic Report Template

```
================================================================
LLM READABILITY AUDIT REPORT
================================================================
Page URL:        [url]
Page Type:       [classification]
Audit Date:      [date]
Word Count:      [n] words / [n] characters
Grounding Ratio: [n]% (380 / total words)
Intents Mapped:  [n]
================================================================

COMPOSITE SCORE: [XX] / 100  —  Grade: [X]

----------------------------------------------------------------
LENS SCORES
----------------------------------------------------------------
1. Structural Fitness:      [XX] / 20
2. Selection Likelihood:    [XX] / 20
3. Extractability:          [XX] / 20
4. Entity Completeness:     [XX] / 20
5. Natural Language Quality: [XX] / 20

================================================================
INTENT COVERAGE MAP
================================================================
| # | Query Intent | Answered? | Position | Differentiation | S-V-O Clean? |
|---|---|---|---|---|---|
| 1 | [intent] | Y/N | [first/mid/last 20%] | [4/4, 3/4...] | Y/N |

================================================================
EXTRACTION FAILURE LOG
================================================================
| Line/Para | Sentence | Failure Code | Severity | Suggested Rewrite |
|---|---|---|---|---|
| P3-S2 | "They offer this at scale." | EF-01, EF-02 | High | "[Company] offers [Product] at scale to [audience]." |

Severity Guide:
  HIGH   = Sentence answers a mapped intent but fails extraction
  MEDIUM = Sentence is in first/last 20% but fails extraction
  LOW    = Sentence is supporting content with failure mode

================================================================
PRIORITIZED FIX LIST
================================================================

PRIORITY 1 — COVERAGE GAPS (missing answers)
  [ ] Add answer for intent: "[missing intent]"
      Recommended location: [section]
      Template: "[Entity] [verb] [outcome] for [audience] under [condition]."

PRIORITY 2 — POSITIONALLY VULNERABLE ANSWERS
  [ ] Move answer for "[intent]" from middle (word 850/2100)
      to first section or summary section

PRIORITY 3 — HIGH-SEVERITY EXTRACTION FAILURES
  [ ] P3-S2: Resolve pronoun "They" → "[Entity name]"
  [ ] P7-S1: Add baseline to "30% more efficient" → "than [competitor/standard]"

PRIORITY 4 — ENTITY COMPLETENESS
  [ ] Add is-a statement for primary entity in first paragraph
  [ ] Restate entity name at word ~600 (currently using "it")

PRIORITY 5 — STRUCTURAL IMPROVEMENTS
  [ ] Break paragraph 5 (112 words) into two paragraphs
  [ ] Add verb phrases to bullet list in section 3
  [ ] Remove 3rd restatement of [proposition] (DRY violation)

PRIORITY 6 — TRUST SIGNAL GAPS
  [ ] Add author credentials to body text
  [ ] Add source attribution to statistic in paragraph 4
  [ ] Add review/update date in human-readable format

================================================================
REGULATED CONTENT NOTES (if applicable)
================================================================
  - Hedged claims identified: [n]
  - Hedged claims with sufficient specificity: [n]
  - Recommendation: Retain hedging but add scope, population,
    or source to each hedged claim per EF-07 pattern.
  - Example: "may help" → "may reduce [symptom] in [population],
    according to [source/study]"

================================================================
REWRITE EXAMPLES (Top 3 highest-impact sentences)
================================================================

ORIGINAL (P1-S1):
  "We provide industry-leading solutions that help businesses
   grow and succeed in today's competitive landscape."

REWRITTEN:
  "Acme Industrial manufactures silicone roof coatings that
   extend commercial flat roof lifespan by 15 years for
   buildings over 10,000 sq ft in USDA climate zones 5-8."

RATIONALE:
  - Resolves "We" → named entity (EF-01)
  - Replaces vague claim → specific S-V-O triple
  - Adds constraint (EF-04 fix)
  - Adds job-to-be-done
  - Survives extraction as standalone sentence

[Repeat for sentences 2 and 3]

================================================================
END OF REPORT
================================================================
```

---

## 5. Special Handling Rules

### Multi-Intent Pages

Pages serving more than 5 distinct intents should be flagged with a **splitting recommendation**. The grounding budget of ~380 words per page per query means a 3,000-word page covering 8 intents will have most answers outside the selection window for any given query. Score as-is, but add a recommendation to split into focused pages if score falls below 70.

### Regulated Industries (Medical, Legal, Financial)

- Do NOT penalize hedging language ("may", "could", "in some cases").
- DO penalize hedging without specificity (EF-07). "May help" is vague. "May reduce LDL cholesterol by 10-15% in adults with mild hyperlipidemia, per the 2024 AHA guidelines" is hedged but extractable.
- Score condition-preservation (EF-04) at double weight. Stripping conditions from medical/legal claims is the highest-risk extraction failure.

### E-Commerce / Product Pages

- Require at minimum: product name, category (is-a), price or price range, 3 differentiating specs with units, and availability scope.
- Each missing element is -2 from Entity Completeness.
- Structured data (schema markup) does not substitute for in-body-text statements. AI grounding systems read rendered text, not JSON-LD.

### Documentation / Technical Pages

- Allow higher jargon density but still require inline definitions for terms not in common developer vocabulary.
- Code blocks must be preceded by a natural language sentence stating what the code does — retrieval systems index the text, not the code.
- Allow passive voice up to 30% (technical writing convention).

---

## 6. Audit Execution Checklist

| Step | Action | Time Est. |
|---|---|---|
| 1 | Classify page, map 3-8 query intents | 10 min |
| 2 | Measure document length, heading structure, position of answers | 10 min |
| 3 | Evaluate differentiation signals and trust signals per intent | 15 min |
| 4 | Sentence-level extraction audit (sample or full) | 20-30 min |
| 5 | Entity resolution and S-V-O triple check | 10 min |
| 6 | Readability metrics, format mix, DRY check | 10 min |
| 7 | Calculate composite score | 5 min |
| 8 | Generate prioritized fix list and rewrite examples | 15 min |
| **Total** | | **~90-105 min** |

---

## 7. Key Principles Underlying This Methodology

1. **The grounding budget is finite.** AI systems select roughly 380 words from your page. Every word must earn its place.
2. **Extraction is lossy.** Any sentence that cannot stand alone will be misrepresented or skipped.
3. **Position matters.** First and last 20% of a document receive disproportionate attention from models.
4. **Explicitness beats elegance.** Named entities, stated relationships, and inline conditions outperform literary devices, pronoun chains, and implied context.
5. **Density without distortion.** Compress, but never at the cost of accuracy. Oversimplification is functionally equivalent to hallucination — you are pre-fabricating the distortion the model would otherwise introduce.
6. **Structure is signal.** Headings that match query patterns, S-V-O sentences that map to knowledge graph triples, and clear hierarchy all increase selection probability.

---

*Methodology version 1.0. Designed for application across all page types, industries, and content management systems.*
