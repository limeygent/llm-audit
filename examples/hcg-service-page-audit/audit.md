📋 LLM Readability Audit
🚨 Rewrite urgency: SEVERE — 11 CRITICAL findings (8 of them regulated-claim compliance violations) + commoditization verdict COMMODITIZED + 3 uncovered fan-out sub-queries emitted as findings
🏥 Healthcare Mode Active — Scoring adjusted for compliance. Hedged therapeutic language and absent clinical outcome data are not penalised; unhedged numeric outcome claims auto-escalate to CRITICAL.
🧭 Intent source: INTENT_ANALYZER (analyzer confidence: medium)

🛰️ AUTHORITY & ACCESS (STAGE ONE)
  On-page (operator-verified against raw HTML fetched 2026-06-11): schema — none found (no schema.org JSON-LD of any type) ⚠️ · author byline — ⚠️ missing (no author/reviewer attribution anywhere) · date signals — ⚠️ none visible (no published/modified date)
  Server-side rendering: ✅ operator-verified — body content IS server-rendered, so AI crawlers (GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot — none of which execute JavaScript) can read the copy.
  Off-page (operator must verify — NOT findings): AI-crawler access at CDN/WAF layer · server-log evidence of AI fetches · brand-mention breadth · author entity findable online
  ⚠️ Stage-one caveat: this audit scores chunk quality. A page that fails authority/access preconditions will not be cited regardless of how clean the findings below are.

---

🌐 PAGE-LEVEL COMMODITIZATION
  Verdict: COMMODITIZED — CRITICAL. The page's proprietary nouns (MealTrack Planner™, Mara's Cookbook, Dr. Hartwell) are tokens, not distributed uniqueness: the bulk of body words live in sections any competing HCG clinic could host unmodified, including an FAQ that recycles 70-year-old public-domain Simeons protocol boilerplate. The rewriter cannot fix this with sentence-level tweaks — the page needs a committed unique angle first.
  Section-weighted substitution: ⚠️ fails — ~55% of body words in swappable sections ("Lose Weight with HCG:", "HCG Helps With Weight Loss", "How Our Weight Loss Program Works", "FREE When You Join!", "Why Choose Us?", "What Our Patients Say About Our Program", "Frequently Asked Questions About HCG") | Unique-data density: 5 provider-specific sentences ÷ 1.85 body kilowords = 2.7/1,000 — ⚠️ below the 3/1,000 threshold (borderline → tie-break awards the fail point) | Unique-angle present: ⚠️ absent — "real HCG, not homeopathic" and "no prepackaged foods" are stock HCG-clinic claims any 5+ competitors also state; no named protocol, no contrarian stance | External-verifiable trust signals: 4 (Kevin M Hartwell, MD; Beth Hanlon, NP; MealTrack Planner™ named technology; "Over 20 years of experience") — ✅ | AI fingerprint markers: 2 (one contrastive negation, vague attribution "HCG dieters report") — ✅ (structural registry, dated 2026-06; this is legacy human marketing copy, not AI slop)
  Fail points: 3 / 5
  Recommended unique angle: Commit to a named, specific protocol the page already implies but never states: "Dr. Hartwell's three-tier physician-directed HCG protocol (Rapid / Standard / HCG-Only), segmented by weight-loss target (30+ lbs vs ≤15 lbs), with monthly BIA body-composition verification, on-site medication dispensing, and a published 500–900-calorie diet structure" — plus a transparent statement of HCG's FDA status as a trust differentiator (no competitor HCG page states it honestly, and the skeptical post-failed-diet reader the analyzer identified is precisely the reader who rewards transparency).

---

✅ WHAT'S WORKING
- Three-tier program architecture (Rapid + HCG / Standard + HCG / HCG Only) with explicit self-selection criteria ("lose 30 lbs or more" vs "lose 15 lbs or less") — this is the page's strongest decision scaffolding; preserve it.
- Named physician and nurse practitioner (Kevin M Hartwell, MD; Beth Hanlon, NP) and consistent "physician-directed" framing — exactly what the analyzer's hidden driver (medical-legitimacy reassurance) needs; it just needs credentials completed.
- Program inclusion bullet lists are parallel, discrete, and scannable — correct format for the content.
- The FAQ uses real question-formatted headings ("Is HCG safe for weight loss?", "How much weight can I expect to lose with HCG?") — strong G1 query-match surface; the answers need a compliance rebuild, but the structure is right.
- Clear 3-step process (Free Consultation & Body Fat Analysis → Medications & Follow Ups → Support Between Visits) that de-risks the first step.
- Real proof assets exist: a hero case (Ian), a 17-photo before/after gallery, six named-ish testimonials — they need machine-readable captions, not replacement.
- Distinctive named assets to build the unique angle from: MealTrack Planner & Fitness Tracker™, Mara's Cookbook (60+ physician-approved recipes), monthly BIA testing, on-site dispensing.
- Body content is server-rendered (operator-verified 2026-06-11) — the page is readable by every AI crawler.

---

🚦 GATE DIAGNOSIS  (counts equal total findings = 25; weighted score = Zone1×2 + Body×1 + CRITICAL×1)
  G1 Retrieval:  8 issues, weighted 9  — uncovered sub-queries (cost, diet structure, timeline), incomplete practitioner credentials, comparison data not in table form, missing author byline and schema, duplicate heading
  G2 Ranking:    7 issues, weighted 9  — off-topic members-area section, verbatim duplicate section, boilerplate FAQ answer, proof sections with no machine-readable outcomes, guarantee-flavored filler opener
  G3 Citation:   10 issues, weighted 22 — unhedged numeric outcome claims across Zone 1, FAQ, Why Choose Us, and image alt text; no anchorable statement in Zone 1; unresolved pronoun; FDA-contradicted safety claims needing verification
  Primary bottleneck: G3 (Citation) — the page's claims are extractable but uncitable: in healthcare mode, nearly every outcome number on the page (1–2 lbs/day, 10–30 lbs/month, 337→229 lbs) is stated without its qualifying condition in the same sentence, making every retrieved chunk a misinformation vector an LLM cannot safely quote.

---

🗺️ Zone Analysis
  Page length: ~10,800 characters / ~1,850 words → page_length_band: HEALTHY — but marginally above the 10,000-char healthy ceiling for a service page; the recommended cuts (duplicate app section, members-area block, CTA interstitial) bring it back inside the band
  Estimated grounding coverage: ~25% (indicative — constant dated 2025-Q4, single system)
  Zone 1: first 2,000 characters (computed: min(0.20 × ~10,800 = ~2,160, 2000) = 2,000; the boundary lands inside the "How Our Weight Loss Program Works" H3 card stack, so per the non-sentence rounding rule Zone 1 closes at the preceding sentence end, "…These results are from using real HCG, not the homeopathic brands sold on the internet." — ~1,980 chars)
  Zone 1 spans: hero block, "Lose Weight with HCG:", and "HCG Helps With Weight Loss"
  Zone 1 contents: named_entity ✅ (Dr. Hartwell's Example Weight Loss Clinics) · core_service ✅ (HCG injections for weight loss) · target_user ✅ ("If you are tired of failing with your weight loss attempts…", belly/love-handle fat) · anchorable_statement ⚠️ MISSING — no Zone 1 sentence passes the 4-test anchorable check (the opening sentence fails the data-point and substitution tests)
  Body (13 content sections): How Our Weight Loss Program Works, Program Options, Rapid Weight Loss Medications, Our Success Stories, FREE When You Join! (Members Area), Mara's Cookbook / Weight Loss Recipes, Follow Your Program Between Office Visits, Follow Your Program Between Visits (verbatim duplicate), Meet Dr. Hartwell and the Rapid Weight Loss Team, Why Choose Us?, What Our Patients Say About Our Program, In the Media, Frequently Asked Questions About HCG
  ⚠️ Architecture gap: the page's only hard differentiators (named MD, 3 locations, program weight-target segmentation, 250 IU dosing) all live in Body sections; none is mirrored into Zone 1 as a dense anchor — fixed by finding 1's Zone 1 anchorable rewrite
  ⚠️ Section integrity issues: "FREE When You Join!" fails topical binding (analyzer drift — auto-fail); "Follow Your Program Between Visits" is a verbatim duplicate (DRY); "Mara's Cookbook" fails topical binding as written (analyzer drift — REPURPOSE, not cut); FAQ "What is HCG?" fails single-concept (fertility-drug digression competing with the weight-loss answer in one chunk)

🎯 Primary intent: "hcg injections for weight loss" — commercial investigation: decide whether a doctor-supervised HCG injection program is a safe, legitimate way to lose stubborn belly fat, and whether this clinic is credible enough to book a consultation with (source: INTENT_ANALYZER, confidence medium)
  Hidden driver (analyzer): frustration after repeated failed diets, paired with skepticism — the reader needs medical-legitimacy reassurance that HCG is safe and real before committing.
  H1 alignment: ✅ pass — "HCG for Belly Fat Reduction" contains the categorical topic (HCG) plus a job qualifier (belly fat reduction) and reads as a plausible literal search. Note (not a finding): the H1 is narrower than the primary intent and the page's own title tag ("HCG Injections for Weight Loss…"); the rewrite_brief recommends widening it to "HCG Injections for Weight Loss" phrasing.
  H1 quoted: "HCG for Belly Fat Reduction"
🎯 Secondary intents: none (analyzer: secondary = null)
🎯 Anchor sections (from intent-analyzer — auto-pass topical binding): Lose Weight with HCG:; HCG Helps With Weight Loss; How Our Weight Loss Program Works; Program Options; Rapid Weight Loss Medications; Our Success Stories; Follow Your Program Between Office Visits; Meet Dr. Hartwell and the Rapid Weight Loss Team; Why Choose Us?; What Our Patients Say About Our Program; Frequently Asked Questions About HCG; North Shoreline / Riverton / Bayside
🎯 Drift sections (from intent-analyzer — auto-fail topical binding): Follow Your Program Between Visits (duplicate → CUT); FREE When You Join! (Members Area → CUT); Mara's Cookbook / Weight Loss Recipes block (→ REPURPOSE into a diet-structure answer per the analyzer's note, not cut); Start Your Weight Loss Journey Today! (CTA interstitial → excluded as UI, removed from content flow)

🎯 Intent & Fan-Out Coverage  (fan-out set: reasoned estimate, not engine telemetry — no PAA data supplied; ~95% of fan-out queries have zero traditional search volume, dated 2026-Q2)
  | # | Query | Type | Source | Extractable Answer? | Section | Recommended home | Notes |
  |---|---|---|---|---|---|---|---|
  | 1 | hcg injections for weight loss (doctor-supervised — safe, legit, this clinic?) | primary | INTENT_ANALYZER | ⚠️ No | Hero / Lose Weight with HCG: | ZONE1_MIRROR | content exists but no sentence passes the anchorable test; finding 1 builds the Zone 1 anchor |
  | 2 | what is hcg and how does it work for weight loss | fanout | ENUMERATED | ✅ COVERED | HCG Helps With Weight Loss + FAQ "What is HCG?" | — | mechanism present; FAQ answer needs single-concept fix |
  | 3 | how much does the hcg diet cost at a medical clinic | fanout | ENUMERATED | ⚠️ UNCOVERED | — | BODY_SECTION | zero pricing anywhere; highest-value gap (finding 12) |
  | 4 | what do you eat on the hcg diet — 500-calorie diet structure | fanout | ENUMERATED | ◐ PARTIAL | FAQ "What is HCG?" (one parenthetical: "500-900 calories") | BODY_SECTION | no self-contained answer; cookbook block REPURPOSEs into this (finding 13) |
  | 5 | how long does the hcg program take / how fast will I see results | fanout | ENUMERATED | ⚠️ UNCOVERED | — | FAQ_ENTRY | no phase lengths or program duration anywhere (finding 14) |
  | 6 | is hcg safe for weight loss — side effects | fanout | ENUMERATED | ◐ PARTIAL | FAQ "Is HCG safe…" / "Are there adverse effects for men?" | EXTEND_EXISTING_SECTION | safety asserted, never substantiated: no side-effect list, no contraindications, FDA conflict (findings 8, 16, 21) |
  | 7 | who qualifies for hcg / who should NOT take it | fanout | ENUMERATED | ◐ PARTIAL | Program Options (weight-target self-selection only) | FAQ_ENTRY | no medical eligibility or contraindications; routed to faq_plan |
  | 8 | hcg injections vs semaglutide or phentermine | fanout | ENUMERATED | ◐ PARTIAL | Rapid Weight Loss Medications + FAQ combo answers | EXTEND_EXISTING_SECTION | medication cards → comparison table (finding 18) |
  | 9 | prescription hcg injections vs homeopathic hcg drops | fanout | ENUMERATED | ◐ PARTIAL | HCG Helps With Weight Loss (one sentence) | FAQ_ENTRY | a real differentiation seed; routed to faq_plan |
  | 10 | how much weight can I lose with hcg | fanout | ENUMERATED | ✅ COVERED | FAQ "How much weight can I expect to lose…" | — | extractable but compliance-broken (findings 6, 7) |
  | 11 | what happens at the first consultation / how the program works | fanout | ENUMERATED | ✅ COVERED | How Our Weight Loss Program Works + HCG Only inclusions | — | solid |
  | 12 | hcg diet clinic near Riverton / North Shoreline / Bayside SC | fanout | ENUMERATED | ◐ PARTIAL | Why Choose Us? ("3 convenient locations" + phone) | EXTEND_EXISTING_SECTION | analyzer reports a locations block on the live page that is absent from the extracted body — surface cities + addresses as machine-readable body text |
  | 13 | can I combine hcg with semaglutide or my current program | fanout | ENUMERATED | ✅ COVERED | FAQ (two combination entries) | — | tight, self-contained answers |
  | 14 | is Dr. Hartwell's hcg program legit — reviews | fanout | ENUMERATED | ◐ PARTIAL | Testimonials + Meet Dr. Hartwell | EXTEND_EXISTING_SECTION | generic praise + incomplete credentials (findings 4, 20) |
  ⚠️ Coverage gap: cost (#3 — BODY_SECTION, pricing table in Program Options), diet structure (#4 — BODY_SECTION, repurposed cookbook block), timeline (#5 — FAQ_ENTRY) emitted as the top-3 UNCOVERED_SUBQUERY findings. Further gaps (contraindications #7, homeopathic comparison #9) recorded here and in faq_plan only. Primary intent has no Zone 1 anchorable answer (finding 1).

🔀 Flow check:
  ✅ Intent answered in opening — hero states what HCG is for and who offers it
  ⚠️ Credibility established early — the team section (the analyzer's medical-legitimacy payload) sits below two junk sections near the page bottom; credentials are incomplete; the skeptical reader gets selling before legitimacy
  ⚠️ Options / content in logical order — process appears before options; cookbook/members-area/duplicate-app blocks interrupt the proof → decision arc
  ✅ CTA / next step clear — abundant Book Now / Call Us placements (if anything, over-supplied: 6 CTA blocks)
  ⚠️ Flow gap: the skeptical post-failed-diet reader needs mechanism → legitimacy → diet reality → options/price; the current page delivers mechanism → process → options → retention upsells → legitimacy, and never delivers diet reality or price.

🔗 Reasoning chain:
  "Is a doctor-supervised HCG program at this clinic worth booking?" requires: does HCG work (mechanism) → is it safe and who shouldn't take it → what is the diet actually like day-to-day → what does it cost → can I do it near me
  ⚠️ Missing links: cost (absent entirely) and diet structure (one parenthetical). The safety link is present but compliance-broken (unhedged claims contradicted by the FDA's published position). An LLM building this answer must leave the page for cost and diet — and will likely complete the chain from a competitor.

🏷️ Competitive Differentiation
  What: ✅ HCG injections as add-on or standalone, within named Rapid/Standard programs
  Who: ✅ Dr. Hartwell's Example Weight Loss Clinics / Kevin M Hartwell, MD
  What job: ✅ "lose stubborn fat from around problem areas like the stomach, hips and waist"
  What constraint: ✅ present but scattered — "designed for people wanting to lose 30 lbs or more" / "typically need to lose 15 lbs or less" (Program Options, far from the other signals)
  Result: PARTIAL — all 4 signals exist on the page but no contiguous ≤3-sentence window contains them; an LLM extracting any 3-sentence window cannot get all four. No extractable 3-sentence window identified.
  ⚠️ Substitution test: FAIL — swap "Dr. Hartwell's" for any competitor in the opening sentence, the mechanism section, the FAQ, and Why Choose Us, and every sentence still works.

📐 Format Audit
  ⚠️ Tables used where comparison data exists — none on the page: three programs with parallel inclusions (Program Options) and three medications with parallel attributes (Rapid Weight Loss Medications) are prose/link-blobs; both should be tables
  ✅ Numbered/stepped content acceptable — the 3-step process renders as labeled H3 cards in sequence
  ✅ Bullet lists used for parallel discrete items (program inclusions, Why Choose Us)
  ✅ Paragraphs reserved for relational content (mechanism explanation)
  ⚠️ Headings descriptive and hierarchical — mostly yes, with one duplicate stacked H2 ("Weight Loss Medications" directly under "Rapid Weight Loss Medications")
  ⚠️ Format gap: Rapid Weight Loss Medications — the three medication "cards" are run-on link texts ("Phentermine Safe & Effective Appetite Suppressant –Jump Start for Weight Loss – Oral Medication Book Appointment"); convert to a 3-row comparison table (finding 18). Program Options pricing should enter as a table (finding 12).
  ⚠️ Heading issue: duplicate generic H2 "Weight Loss Medications" (finding 24).

🔁 DRY Check
  ⚠️ Violations found:
  ⚠️ "Follow Your Program / Between Visits" is a verbatim duplicate of "Follow Your Program Between Office Visits" (responsive page-builder artifact) — same copy, same bullets, same app; the two footnotes even conflict ("Rapid Program Only" vs "Rapid or Rapid+ Programs Only"). Cut the duplicate, reconcile the eligibility footnote (finding 15).
  ⚠️ "Access to our Private Members Area plus Mara's Cookbook" is restated four times (both program lists, Why Choose Us, and the members-area section) with zero new attributes — claim restatement; the members-area section adds nothing not already stated (subsumed in finding 11's cut).

🛡️ Trust Signals
  ✅ Present: named practitioner (Kevin M Hartwell, MD, Bariatric Physician), named NP (Beth Hanlon), years of operation ("Over 20 years of experience"), named technology (MealTrack Planner & Fitness Tracker™, Bioelectric Impedance Analysis testing), named product (Mara's Cookbook, 60+ physician-approved recipes), phone number, on-site medication dispensing
  ⚠️ Missing: licence/registration number and certifying board for Dr. Hartwell ("Board certified" names no board — finding 4), street addresses for the 3 locations, named external sources for any clinical claim, pricing, honest side-effect/risk data, named insurance/payment information, author byline (finding 22)

⚓ Anchorable Statements
  Zone 1: ⚠️ MISSING — best candidate "Dr. Hartwell's Example Weight Loss Clinics is a weight loss clinic offering HCG Injections to help patients lose weight fast and keep it off!" fails test 2 (no specific data point) and test 4 (substitution: any clinic could claim it). Finding 1 supplies the replacement.
  Closest on-page candidate: "Our Rapid Weight Loss Program with HCG is designed for people wanting to **lose 30 lbs or more** and would like to do it FAST!" — has a named program + data point + condition but needs the clinic name re-anchored to pass substitution.
  Intent coverage: 0 of 1 intents has an anchorable statement (primary intent uncovered in Zone 1)
  ⚠️ Gap: primary intent — the Zone 1 hero must carry the anchor (finding 1); the new cost and diet-structure sections must each open with one (findings 12, 13).

🔒 Condition Preservation
  ⚠️ Violations found (healthcare auto-escalation — all CRITICAL):
  ⚠️ Image alt text (machine-only): "Clinical observations demonstrate daily weight reduction of 0.45-0.9 kg…" — full unhedged clinical paragraph in an alt attribute; second instance in Image 6 alt ("patients can lose 1-2 pounds of fat per day"). Invisible to human readers, fully visible to every AI crawler (finding 2).
  ⚠️ Hero quote "I weighed 337 lb. and I'm currently sitting at 229 lb." — hedge lives only in the gallery disclaimer several sections away → duplicate the hedge inline; do not move the protected disclaimer (finding 3).
  ⚠️ "Lose 10-30 lbs. a month eating foods from your local store" (Why Choose Us) — no hedge in the bullet (finding 5).
  ⚠️ "…HCG injections can help you lose 1-2 pounds of stubborn fat a day…" (FAQ) — no inline results-vary condition (finding 6).
  ⚠️ "Those who follow our Rapid Weight Loss Program with HCG report a 1-2 lb. drop in weigh per day!" (FAQ) — the hedge ("results vary by person") sits two sentences later (finding 7).
  ⚠️ "HCG is currently being used in weight loss clinics because it works and it is safe." (FAQ) — efficacy + safety claim, no hedge (finding 8).
  ⚠️ "It is commonly used as a fertility drug with no side effects." (FAQ) — absolute safety claim (finding 9).

🔘 CTA Blocks Detected (excluded from all section assessment; no trapped trust signals — "FREE Consultation & Body Fat Analysis" is duplicated in body content)
  - Book Now / Call Us (hero) — inline hero CTA
  - Book Now / Call Us (after "HCG Helps With Weight Loss")
  - Book Now / Call Us (after "Program Options")
  - Book Now / Call Us (after "Why Choose Us?")
  - "Start Your Weight Loss Journey Today!" — H2-tagged CTA interstitial ("Call now or use our online scheduler to book a FREE Consultation…"); the H2 creates a false section boundary; treated as UI, removed from the content flow
  - "If you are thinking about trying HCG for weight loss, call our office today…" + Book Now (FAQ close)

---

Section: Hero ("HCG for Belly Fat Reduction") — Zone 1
Disposition: KEEP_IN_PLACE
Integrity: ✅ (anchors the primary intent)

✅ Strengths:
- Names the full entity ("Dr. Hartwell's Example Weight Loss Clinics") and the service (HCG injections) in the first sentence — first-passage bias well spent (~44% of ChatGPT citations come from the first 30% of the page, dated 2026).
- Leads with a concrete patient case (Ian) rather than abstract promises.

⚠️ Issues:
- [CRITICAL] [G3] No anchorable statement — the opening sentence has no specific data point and fails the substitution test — replace with a dense, hedged anchor (finding 1).
- [CRITICAL] [G3] The Ian quote is a numeric outcome testimonial whose "results may not be typical" condition lives only in the gallery disclaimer sections away — duplicate the hedge inline (finding 3).

⚠️ Flagged sentences:
  `Dr. Hartwell’s Example Weight Loss Clinics is a weight loss clinic offering HCG Injections to help patients lose weight fast and keep it off!`
  Issue: Fails the anchorable-statement test (G3) — no specific data point, and the substitution test fails: any clinic could host this sentence unchanged.
  ✅ Rewrite: Dr. Hartwell’s Example Weight Loss Clinics is a physician-directed weight loss clinic with three the clinic's state locations (Riverton, North Shoreline, and Bayside) offering pharmaceutical-grade HCG injections combined with a 500–900-calorie structured diet to target stubborn belly fat; a free consultation determines whether the program suits you, and individual results vary.

  `When I started this journey, I weighed 337 lb. and I’m currently sitting at 229 lb.`
  Issue: Condition preservation (G3) — numeric outcome claim in Zone 1; the qualifying "results may not be typical" condition is in a different section. Healthcare auto-escalation → CRITICAL.
  ✅ Rewrite: Keep the quote verbatim and append directly beneath it: "— Ian, Rapid Program + HCG patient. Results are not typical; individual results vary." (Duplicate of the protected gallery disclaimer — leave the original in place.)

---

Section: Lose Weight with HCG: — Zone 1
Disposition: KEEP_IN_PLACE
Integrity: ✅ (analyzer anchor — auto-pass topical binding)

✅ Strengths:
- States who HCG is for (patients tired of failed attempts, targeting belly/hip/waist fat) and how it is purchased (add-on or standalone) — opens the commercial investigation correctly.
- Benefit bullets are parallel and discrete.

⚠️ Issues:
- [CRITICAL] [G3] Machine-only artifact: the section's image alt attribute carries a full clinical paragraph with unhedged outcome claims ("daily weight reduction of 0.45-0.9 kg", "Documented outcomes include…") — invisible to human readers, fully extractable by AI crawlers; a compliance liability in exactly the channel this audit optimizes (finding 2; second instance in the "HCG Helps With Weight Loss" Image 6 alt).
- [IMPORTANT] [G3] Unresolved pronoun in a Zone 1 sentence (finding 17).

⚠️ Flagged sentences:
  `Clinical observations demonstrate daily weight reduction of 0.45-0.9 kg, predominantly from adipose tissue stores.`
  Issue: Condition preservation (G3) — unhedged clinical outcome claim living in an image alt attribute (machine-only text). Healthcare auto-escalation → CRITICAL.
  ✅ Rewrite: Replace the entire alt attribute with a short descriptive label — "Patient receiving a subcutaneous HCG injection at Dr. Hartwell's Example Weight Loss Clinics" — and move any claim worth keeping into visible body copy with its hedge in the same sentence. Apply the same fix to the Image 6 alt ("patients can lose 1-2 pounds of fat per day…").

  `It’s for patients looking for additional help targeting belly and love handle fat.`
  Issue: Extractability (G3) — "It's" has no in-sentence antecedent; extracted alone, the sentence doesn't say what "it" is.
  ✅ Rewrite: HCG is for patients looking for additional help targeting belly and love handle fat.

---

Section: HCG Helps With Weight Loss — Zone 1
Disposition: KEEP_IN_PLACE
Integrity: ✅ (analyzer anchor)

✅ Strengths:
- Plain-language mechanism explanation (mobilizes stored fat, suppresses appetite, preserves muscle) answering the core skeptic question.
- "These results are from using real HCG, not the homeopathic brands sold on the internet." — the page's one genuine differentiation seed; preserve and expand it (faq_plan entry).

⚠️ Issues:
- None flagged beyond the Image 6 alt-text instance covered by finding 2. The "trick" your body phrasing is informal but readable; mechanism claims here are non-numeric and acceptably hedged for healthcare mode.

---

Section: How Our Weight Loss Program Works — Body
Disposition: MOVE (later in the arc — process/de-risk belongs after options + pricing; see 📜 flow position 8)
Integrity: ✅ (analyzer anchor)

✅ Strengths:
- Clean 3-step sequence with the FREE Consultation & Body Fat Analysis named as step one — strong de-risking content.
- Each step is one tight sentence; no filler openers.

⚠️ Issues:
- None at sentence level. The position fix lives in the recommended flow, not as a finding.

---

Section: Program Options — Body
Disposition: KEEP_IN_PLACE
Integrity: ✅ (analyzer anchor)

✅ Strengths:
- The heart of the commercial investigation: three named tiers with explicit self-selection criteria (30+ lbs vs ≤15 lbs vs medication-only) and full inclusion lists.
- "Our Rapid Weight Loss Program with HCG is designed for people wanting to lose 30 lbs or more" is the page's closest-to-anchorable sentence — re-anchor the clinic name into it during the rewrite.

⚠️ Issues:
- [IMPORTANT] [G1] UNCOVERED_SUBQUERY: cost — three programs, zero prices; the single highest-value fan-out gap on the page (finding 12). Placement: BODY_SECTION — a pricing comparison table here, not an FAQ one-liner.

---

Section: Rapid Weight Loss Medications — Body
Disposition: KEEP_IN_PLACE
Integrity: ✅ (analyzer anchor)

✅ Strengths:
- Situates HCG against Phentermine and B12/Lipotropics — serves the comparison sub-query and positions HCG as add-on or standalone.

⚠️ Issues:
- [IMPORTANT] [G1] Format mismatch: three medications with parallel attributes rendered as run-on link blobs — should be a comparison table (finding 18).
- [MINOR] [G1] Duplicate stacked H2 "Weight Loss Medications" directly beneath "Rapid Weight Loss Medications" — false section boundary for chunkers (finding 24).

---

Section: Our Success Stories — Body
Disposition: KEEP_IN_PLACE
Integrity: ✅ (analyzer anchor)

✅ Strengths:
- 17 before/after cases — real proof volume most competitors can't match; result-range filters (20-60 / 61-80 / 81-100+ lbs) imply quantified outcomes.

⚠️ Issues:
- [IMPORTANT] [G2] Every outcome is locked inside images: the visible text is filter labels only; alt texts are wrong (several different patients share "Caroline before after"). Zero machine-readable outcome data survives extraction (finding 19).

---

Section: Testimonial results disclaimer ("*The results described in these testimonials may not be typical…") — Body
Integrity: ✅ N/A (protected compliance content)

✅ Strengths: Compliance language present and verbatim.
⚠️ Issues: None — protected from rewrite.

*(No flagged sentences. Recorded in `protected_sections[]` with `rewrite_permissions`; the rewriter must preserve it verbatim. Finding 3 requires DUPLICATING its hedge beside the hero quote, leaving this block intact.)*

---

Section: FREE When You Join! (Members Area) — Body
Disposition: CUT  [structural finding only — no sentence polish]
Integrity: ⚠️ fails topical binding (analyzer drift — auto-fail: membership-perk promotion serving the author's retention upsell, not the evaluating reader's decision; answers no fan-out sub-query)

✅ Strengths: None worth preserving in place — its payloads (recipes, MealTrack Planner access, Eat Smart videos) are already stated in Program Options and the app section.
⚠️ Issues:
- [CRITICAL] [G2] OFF_TOPIC_SECTION — cut entirely; no unique trust signals trapped here (finding 11).

---

Section: Mara's Cookbook / Weight Loss Recipes — Body
Disposition: REPURPOSE → "What You'll Eat on the HCG Diet" (diet-structure answer)  [one finding: new job + salvage list — no polish of copy that won't survive]
Integrity: ⚠️ fails topical binding as written (analyzer drift: feature marketing that gestures at the reader's real question — what will I actually eat? — without answering it; analyzer disposition: repurpose, not cut)

✅ Strengths (salvage list):
- "over 60 recipes approved by Dr. Hartwell" — provider-specific data point.
- Phase 1 (16 recipes) / Phase 2 (51 recipes) split — implies the diet has a named phase structure; the repurposed section must explain it.
- Meal-category breadth (Breakfast, Main Dishes, Appetizers, Soups, Salads, Desserts) — proof the diet is liveable, the exact objection a failed dieter holds.

⚠️ Issues:
- [IMPORTANT] [G1] UNCOVERED_SUBQUERY: diet structure — the page never answers "what do you eat on the hcg diet" beyond one parenthetical (500-900 calories) buried in an FAQ; repurpose this block into the answer (finding 13).

---

Section: Follow Your Program Between Office Visits — Body
Disposition: KEEP_IN_PLACE
Integrity: ✅ (analyzer anchor — accountability concern of a reader who has failed solo dieting)

✅ Strengths:
- Named technology (MealTrack Planner & Fitness Tracker™) with concrete capabilities (plan meals, log workouts, track progress); the eligibility footnote keeps its condition inline.

⚠️ Issues:
- None flagged here — but reconcile its eligibility footnote ("Rapid Program Only") against the duplicate's ("Rapid or Rapid+ Programs Only") when cutting the duplicate (finding 15).

---

Section: Follow Your Program / Between Visits (second app section) — Body
Disposition: CUT  [structural finding only — no sentence polish]
Integrity: ⚠️ fails (verbatim duplicate; analyzer drift — auto-fail)

✅ Strengths: None — adds nothing the first copy does not.
⚠️ Issues:
- [IMPORTANT] [G2] DRY_VIOLATION — verbatim duplicate of the preceding app section (responsive page-builder artifact); two identical chunks split the accountability sub-query's signal. Salvage before cutting: the conflicting eligibility footnote must be reconciled (finding 15).

---

Section: Meet Dr. Hartwell and the Rapid Weight Loss Team — Body
Disposition: MOVE (up — position 4; the analyzer's hidden driver demands legitimacy before selling)
Integrity: ✅ (analyzer anchor — "the MD and NP entries do the work, the three administrative staff dilute it")

✅ Strengths:
- Named MD and NP — the medical-legitimacy payload the skeptical reader needs.

⚠️ Issues:
- [CRITICAL] [G1] Credential stated without registration number or issuing body: "Kevin M Hartwell, MD Bariatric Physician" (and "Board certified physician directed program" in Why Choose Us names no board) — healthcare auto-escalation (finding 4). Add board + licence; add one-line bios for the MD and NP; the three administrative staff can stay but should not lead.

⚠️ Flagged sentences:
  `Kevin M Hartwell, MD Bariatric Physician`
  Issue: Entity completeness (G1) — credential without certifying board or licence number; healthcare auto-escalation → CRITICAL.
  ✅ Rewrite: Kevin M. Hartwell, MD — board-certified bariatric physician [DATA_NEEDED: certifying board, e.g. ABOM, and SC licence number], 20+ years directing medically supervised weight loss programs in Riverton, North Shoreline, and Bayside, SC.

---

Section: Why Choose Us? — Body
Disposition: KEEP_IN_PLACE
Integrity: ✅ (analyzer anchor)

✅ Strengths:
- Carries most of the page's verifiable trust signals (3 locations, 20 years, on-site dispensing, monthly BIA testing) — keep all, then make each verifiable (cities, board name).

⚠️ Issues:
- [CRITICAL] [G3] Unhedged numeric outcome bullet (finding 5).

⚠️ Flagged sentences:
  `Lose 10-30 lbs. a month eating foods from your local store`
  Issue: Condition preservation (G3) — numeric outcome claim with no qualifying condition in the same line; healthcare auto-escalation → CRITICAL.
  ✅ Rewrite: Patients typically lose 10–30 lbs. a month eating foods from your local store, though individual results vary.

---

Section: What Our Patients Say About Our Program — Body
Disposition: KEEP_IN_PLACE
Integrity: ✅ (analyzer anchor)

✅ Strengths:
- Six attributed quotes; the Linda S. quote ("As a retired RN, I was very impressed…") carries a credibility detail worth leading with.

⚠️ Issues:
- [IMPORTANT] [G2] Generic praise with zero named outcomes — partial-name testimonials with no program, amount, or timeframe are decoration, not citable proof (finding 20).

⚠️ Flagged sentences:
  `Staff was extremely professional and supportive. 10/10 would recommend.`
  Issue: Anchorable statement / trust (G2) — no outcome, no program, effectively unverifiable; swappable with any clinic's review.
  ✅ Rewrite: Replace with a consented outcome-bearing quote: "I lost [DATA_NEEDED: amount] lbs in [DATA_NEEDED: months] on the Standard Program + HCG." — Jodie K. (individual results vary).

---

Section: In the Media — Body
Disposition: KEEP_IN_PLACE
Integrity: ✅ (media trust strip supporting provider evaluation)

✅ Strengths: Implies third-party coverage — a trust signal class the rest of the page lacks.
⚠️ Issues:
- [MINOR] [G2] Logo-only strip: no machine-readable text at all; the trust signal is invisible to every AI engine (finding 25).

---

Section: Frequently Asked Questions About HCG — Body (FAQ exception: each Q&A pair assessed as its own micro-section)
Disposition: KEEP_IN_PLACE
Integrity: ⚠️ "What is HCG?" fails single-concept (fertility-drug digression competes with the weight-loss definition in one chunk); remaining pairs pass

✅ Strengths:
- Nine question-formatted headings that match real queries — the densest G1 surface on the page.
- The dosage contrast (250 IU diet dose vs up to 6,000 IU fertility doses vs 200,000-300,000 IU in pregnancy) is genuinely specific content — keep the numbers, fix the framing.
- Combination answers (HCG + Rapid/Standard, HCG + Semaglutide) are tight and self-contained.

⚠️ Issues:
- [CRITICAL] [G3] "How does HCG work for weight loss?" — unhedged 1–2 lbs/day claim (finding 6).
- [CRITICAL] [G3] "How much weight can I expect to lose with HCG?" — 1–2 lb/day sentence unhedged; the hedge sits two sentences later (finding 7).
- [CRITICAL] [G3] "Is HCG safe for weight loss?" — "because it works and it is safe" efficacy/safety claim, no hedge (finding 8).
- [CRITICAL] [G3] "What is HCG?" — "fertility drug with no side effects" absolute safety claim inside an off-concept digression (finding 9).
- [CRITICAL] [G2] "What can I do to ensure I lose 1 lb. a day…" — opener fails the 3-element filler test (0/3) and restates the question as a guarantee (finding 10).
- [IMPORTANT] [G3] Safety claims conflict with the FDA's published position on HCG for weight loss — operator verification required before republishing (finding 16).
- [IMPORTANT] [G2] "Are there adverse effects for men?" — answer is 70-year-old Simeons protocol boilerplate, verbatim, that every HCG clinic hosts; fails substitution and mentions treating children (finding 21).
- [IMPORTANT] [G1] No timeline Q&A — "how long does the program last" is uncovered (finding 14).

⚠️ Flagged sentences:
  `When combined with our calorie specific diet, HCG injections can help you lose 1-2 pounds of stubborn fat a day from around problem areas like the stomach, hips and thighs.`
  Issue: Condition preservation (G3) — numeric outcome claim, no inline results-vary condition; healthcare auto-escalation → CRITICAL.
  ✅ Rewrite: When combined with Dr. Hartwell's calorie-specific diet (500–900 calories per day), patients report losing 1–2 pounds of stubborn fat per day from areas like the stomach, hips and thighs [DATA_NEEDED: cohort size and timeframe]; individual results vary with health status and adherence.

  `Those who follow our Rapid Weight Loss Program with HCG report a 1-2 lb. drop in weigh per day!`
  Issue: Condition preservation (G3) — numeric claim with the hedge stranded two sentences later (also a typo: "weigh"); healthcare auto-escalation → CRITICAL.
  ✅ Rewrite: Patients who follow Dr. Hartwell's Rapid Weight Loss Program with HCG typically lose 10–30 pounds per month [DATA_NEEDED: cohort data], though individual results vary by person, health status and adherence.

  `HCG is currently being used in weight loss clinics because it works and it is safe.`
  Issue: Condition preservation (G3) — therapeutic efficacy and safety claim with no hedge, and contradicted by the FDA's published position; healthcare auto-escalation → CRITICAL.
  ✅ Rewrite: At weight-loss doses (250 IU per day — far below fertility doses of up to 6,000 IU), HCG is prescribed and supervised by Dr. Hartwell's medical team; it may support fat loss when combined with a supervised low-calorie diet, though the FDA has not approved HCG for weight loss and individual results vary.

  `It is commonly used as a fertility drug with no side effects.`
  Issue: Condition preservation (G3) — absolute "no side effects" safety claim inside a fertility digression that also breaks the single-concept rule; healthcare auto-escalation → CRITICAL.
  ✅ Rewrite: [DELETE] — remove the fertility-treatment digression entirely (it answers a query outside the fan-out set and dilutes the weight-loss definition chunk); keep the answer focused on what HCG is and how it is used in the weight-loss protocol.

  `Things you can do to ensure that you lose one pound a day or more.`
  Issue: Information density (G2) — opener fails the 3-element filler test (0/3: no new named entity, no data point, no condition) and "ensure… one pound a day" reads as an outcome guarantee in healthcare mode.
  ✅ Rewrite: [DELETE] — lead the answer with the first real tip, rewritten hedged: "To support your results on Dr. Hartwell's program: drink more than 2 liters of water daily, use the B-12/Lipotropic injections, and avoid high-fructose corn syrup, artificial sweeteners, and fast food — individual results vary."

  `It cannot be sufficiently emphasized that HCG is not a sex-hormone, that its action is identical in men, women, children and in those cases in which the sex-glands no longer function owing to old age or their surgical removal.`
  Issue: Natural language / differentiation (G2) — verbatim 1954 Simeons manuscript boilerplate hosted by every HCG clinic; archaic register, fails substitution, and inappropriately references children on a commercial weight-loss page.
  ✅ Rewrite: At the weight-loss doses Dr. Hartwell prescribes (250 IU daily), HCG is not a sex hormone and acts the same way in men and women; men in the program receive the same dosing and supervision as women, and side effects are reviewed at every follow-up visit [DATA_NEEDED: clinic-observed side-effect profile].

---

📜 RECOMMENDED PAGE FLOW  (order serves the human arc — a skeptical, repeatedly-failed dieter who needs medical legitimacy before committing; chunks serve the machines. Service arc: Zone 1 answer + credibility → mechanism → legitimacy → diet reality → options + pricing (CTA) → process → proof (CTA) → objections (FAQ) → location (final CTA))
  | # | Section | Disposition | Serves sub-query | Human goal | CTA after? |
  |---|---|---|---|---|---|
  | 1 | Hero ("HCG for Belly Fat Reduction") | KEEP_IN_PLACE | primary intent | query answered with a credible, hedged anchor (named clinic, MD, 3 cities, what HCG is for) — the skeptic doesn't bounce | (inline hero CTA retained) |
  | 2 | Lose Weight with HCG: | KEEP_IN_PLACE | who is HCG for / how is it purchased | failed-diet reader self-identifies; sees HCG as add-on or standalone | |
  | 3 | HCG Helps With Weight Loss | KEEP_IN_PLACE | how does hcg work for weight loss | the skeptic's "does this actually work" answered with mechanism + honest, hedged expectations | |
  | 4 | Meet Dr. Hartwell and the Rapid Weight Loss Team | MOVE | is this clinic/doctor legitimate | medical legitimacy lands BEFORE any selling: board-certified MD + NP with completed credentials | |
  | 5 | NEW: What You'll Eat on the HCG Diet (500–900-Calorie Structure) | NEW | what do you eat on the hcg diet | the "can I actually live on this diet" objection cleared with concrete meals from a normal grocery store (built from repurposed cookbook salvage) | |
  | 6 | Program Options | KEEP_IN_PLACE | which hcg program fits me | reader self-selects a tier (30+ lbs / ≤15 lbs / medication-only) | |
  | 7 | NEW: HCG Program Costs | NEW | how much does the hcg diet cost | price transparency clears the last rational objection; reader can budget before booking | ✅ |
  | 8 | How Our Weight Loss Program Works | MOVE | what happens when I sign up | de-risk the commitment: free consultation first, then medications and follow-ups | |
  | 9 | Rapid Weight Loss Medications | KEEP_IN_PLACE | hcg vs phentermine vs b12 | reader understands the toolkit and where HCG fits (comparison table) | |
  | 10 | Our Success Stories | KEEP_IN_PLACE | does this work for people like me | proof: captioned, named outcomes with timeframes, hedged | |
  | 11 | What Our Patients Say About Our Program | KEEP_IN_PLACE | is Dr. Hartwell's program legit / reviews | third-party voices confirm safety, supervision, and no-judgement support | ✅ |
  | 12 | Follow Your Program Between Office Visits | KEEP_IN_PLACE | what support do I get between visits | the failed-solo-dieter believes accountability will be different this time | |
  | 13 | Frequently Asked Questions About HCG | KEEP_IN_PLACE | safety, dosage, timeline, eligibility, combinations | remaining objections cleared one self-contained micro-answer at a time | |
  | 14 | Locations (North Shoreline / Riverton / Bayside) | KEEP_IN_PLACE | hcg clinic near me in SC | reader confirms they can do this nearby and books (analyzer anchor — on the live page but absent from the extracted body; must surface as machine-readable text with addresses) | ✅ (final) |
  | — | Mara's Cookbook / Weight Loss Recipes | REPURPOSE | what do you eat on the hcg diet | content folds into position 5; salvage: 60+ physician-approved recipe count, Phase 1/Phase 2 split, meal categories | |
  | — | Follow Your Program / Between Visits (duplicate) | CUT | — | verbatim duplicate; signal-splitting artifact (reconcile the eligibility footnote first) | |
  | — | FREE When You Join! (Members Area) | CUT | — | retention upsell serving the author, not the evaluating reader; payloads already stated elsewhere | |
  | — | Start Your Weight Loss Journey Today! | CUT | — | CTA interstitial (conversion furniture) — replaced by the explicit CTA placements at positions 7, 11, and 14 | |

---

🧪 VALIDATION PLAN
  Prompt corpus (14 prompts — run verbatim):
  Discovery:
  1. "best hcg diet clinic near Riverton"
  2. "doctor supervised hcg injections near North Shoreline"
  Comparison:
  3. "hcg injections vs semaglutide for stubborn belly fat — which should I do?"
  4. "are prescription hcg shots better than the hcg drops sold online?"
  5. "hcg diet vs phentermine for fast weight loss"
  Recommendation:
  6. "I've failed every diet — should I try medically supervised hcg injections?"
  7. "is a doctor-supervised hcg program worth the money?"
  Factual:
  8. "how much weight can you actually lose on the hcg diet?"
  9. "what do you eat on the hcg diet — is it really only 500 calories?"
  10. "how much does the hcg diet cost at a medical weight loss clinic?"
  11. "is hcg safe for weight loss and is it FDA approved?"
  12. "how long does a round of the hcg diet last?"
  Brand:
  13. "is Dr. Hartwell's Example Weight Loss Clinics legit?"
  14. "Dr. Hartwell rapid weight loss reviews hcg program"
  Engines: ≥3 — Google AI Mode/AI Overviews, ChatGPT, Perplexity (add Claude and Copilot if capacity allows).
  Protocol: run the corpus BEFORE the rewrite ships and again ~4 weeks after. Record per prompt: Was any example-weightloss-clinic.com page cited? Was the brand NAMED (not just linked — citations and mentions are separate KPIs, dated 2026-06)? Which competitor won the prompt instead?
  First-party: enable Bing Webmaster Tools' AI Performance report (ChatGPT/Copilot surface, available since 2026-02); watch server logs for OAI-SearchBot / ChatGPT-User / PerplexityBot / ClaudeBot fetches.
  Interpretation caveat: zero-citation answers are increasingly common (ChatGPT's zero-citation rate roughly doubled in 2026-Q2). If NO competitor gets cited on a prompt either, that query class is being answered parametrically — brand-mention breadth then matters more than page citations, and that is an off-page program, not a rewrite problem.

---

⚠️ ALL ISSUES (ordered by severity — Critical first, then Important, then Minor):
1. [CRITICAL] [G3] Hero (Zone 1) — No anchorable statement in Zone 1: replace the opening sentence with the dense, hedged anchor naming clinic, MD, 3 SC cities, pharmaceutical-grade HCG + 500–900-calorie diet, and the free-consultation condition.
2. [CRITICAL] [G3] Lose Weight with HCG: (Zone 1) — Machine-only artifact: strip the unhedged clinical-outcomes paragraph from the image alt attribute (and the Image 6 alt); replace with short descriptive alt text; move surviving claims into body copy with inline hedges.
3. [CRITICAL] [G3] Hero (Zone 1) — Ian's 337→229 lb testimonial: duplicate the "results are not typical; individual results vary" hedge directly beneath the quote (leave the protected gallery disclaimer intact).
4. [CRITICAL] [G1] Meet Dr. Hartwell and the Rapid Weight Loss Team — "Kevin M Hartwell, MD Bariatric Physician" lacks certifying board and licence number ("Board certified" in Why Choose Us names no board): add board + licence [DATA_NEEDED] and one-line MD/NP bios.
5. [CRITICAL] [G3] Why Choose Us? — "Lose 10-30 lbs. a month eating foods from your local store": add the inline hedge ("…though individual results vary").
6. [CRITICAL] [G3] FAQ "How does HCG work for weight loss?" — unhedged "lose 1-2 pounds of stubborn fat a day": merge population, calorie condition, [DATA_NEEDED: cohort], and results-vary hedge into the same sentence.
7. [CRITICAL] [G3] FAQ "How much weight can I expect to lose with HCG?" — "report a 1-2 lb. drop in weigh per day!": fold the stranded "results vary by person" hedge into the claim sentence; fix the "weigh" typo.
8. [CRITICAL] [G3] FAQ "Is HCG safe for weight loss?" — "because it works and it is safe": rewrite as a hedged, dose-anchored statement that discloses the FDA position.
9. [CRITICAL] [G3] FAQ "What is HCG?" — "fertility drug with no side effects": [DELETE] the fertility digression; restore the single-concept weight-loss definition.
10. [CRITICAL] [G2] FAQ "What can I do to ensure I lose 1 lb. a day…" — opener fails the 3-element filler test (0/3) and reads as an outcome guarantee: [DELETE]; lead with the hedged tips.
11. [CRITICAL] [G2] FREE When You Join! (Members Area) — OFF_TOPIC_SECTION (analyzer drift): cut entirely; payloads already stated in Program Options and the app section.
12. [IMPORTANT] [G1] Program Options — UNCOVERED_SUBQUERY (cost): add a body-section pricing comparison table (Rapid + HCG / Standard + HCG / HCG Only × monthly price [DATA_NEEDED] / visit cadence / inclusions / who it's for) headed "HCG Program Costs at Dr. Hartwell's".
13. [IMPORTANT] [G1] Mara's Cookbook / Weight Loss Recipes — UNCOVERED_SUBQUERY (diet structure): REPURPOSE the block into a body section "What You'll Eat on the HCG Diet" — daily calorie band (500–900), Phase 1 vs Phase 2 meaning, a sample day of meals, grocery-store sourcing; salvage the 60+ recipe count, phase split, and meal categories.
14. [IMPORTANT] [G1] Frequently Asked Questions About HCG — UNCOVERED_SUBQUERY (timeline): add FAQ entry "How long does the HCG program last?" — 40–80 words naming phase lengths and typical duration [DATA_NEEDED], hedge inline.
15. [IMPORTANT] [G2] Follow Your Program / Between Visits (duplicate) — DRY_VIOLATION: delete the verbatim duplicate app section; first reconcile the conflicting eligibility footnotes ("Rapid Program Only" vs "Rapid or Rapid+ Programs Only") [DATA_NEEDED: which is correct].
16. [IMPORTANT] [G3] FAQ "Is HCG safe for weight loss?" — VERIFY_BEFORE_PUBLISH: the page's HCG safety/efficacy claims conflict with the FDA's published position (HCG is not FDA-approved for weight loss); legal/compliance review required before any republish — the rewriter must not restate these claims as fact.
17. [IMPORTANT] [G3] Lose Weight with HCG: (Zone 1) — unresolved pronoun: "It's for patients looking for additional help…" → "HCG is for patients looking for additional help targeting belly and love handle fat."
18. [IMPORTANT] [G1] Rapid Weight Loss Medications — FORMAT_MISMATCH: convert the three run-on medication link-blobs into a comparison table (Medication / What it does / How it's taken / Included in which program).
19. [IMPORTANT] [G2] Our Success Stories — outcomes locked in images: add a text caption per photo (first name, program, amount lost, timeframe [DATA_NEEDED: confirm], hedge) and fix the mismatched alt attributes.
20. [IMPORTANT] [G2] What Our Patients Say About Our Program — generic, outcome-free testimonials: replace 2–3 with consented outcome-bearing quotes naming program + result + hedge [DATA_NEEDED].
21. [IMPORTANT] [G2] FAQ "Are there adverse effects for men?" — verbatim 1954 Simeons boilerplate: replace with a self-contained, clinic-anchored, hedged answer about male dosing and side-effect review.
22. [IMPORTANT] [G1] Page-level — MISSING_AUTHOR_ATTRIBUTION (operator-verified HTML): add "Medically reviewed by Kevin M. Hartwell, MD [credentials], last reviewed [date]" — named human expert attribution on YMYL content (2026 quality-update direction).
23. [MINOR] [G1] Page-level — MISSING_SCHEMA_MARKUP (operator-verified HTML): add MedicalBusiness/LocalBusiness + FAQPage JSON-LD — hygiene for entity disambiguation and Bing/Copilot, not a primary GEO lever (controlled study, 2026-05, found no AI-citation uplift).
24. [MINOR] [G1] Rapid Weight Loss Medications — duplicate stacked H2 "Weight Loss Medications": delete one; keep a single descriptive H2.
25. [MINOR] [G2] In the Media — logo-only strip with zero machine-readable text: name the outlets in visible text ("As featured in [DATA_NEEDED: outlet names]").

---

```json
{
  "schema_version": "1.3",
  "spec_version": "2.2",
  "audit_timestamp": "2026-06-12T00:00:00Z",
  "audit_metadata": {
    "source_url": "https://www.example-weightloss-clinic.com/hcg-diet/",
    "primary_intent": "hcg injections for weight loss — commercial investigation: decide whether a doctor-supervised HCG injection program is a safe, legitimate way to lose stubborn belly fat, and whether this clinic is credible enough to book a consultation with",
    "intent_source": "INTENT_ANALYZER",
    "intent_analyzer_confidence": "medium",
    "anchor_sections_from_analyzer": ["Lose Weight with HCG:", "HCG Helps With Weight Loss", "How Our Weight Loss Program Works", "Program Options", "Rapid Weight Loss Medications", "Our Success Stories", "Follow Your Program Between Office Visits", "Meet Dr. Hartwell and the Rapid Weight Loss Team", "Why Choose Us?", "What Our Patients Say About Our Program", "Frequently Asked Questions About HCG", "North Shoreline / Riverton / Bayside"],
    "drift_sections_from_analyzer": ["Follow Your Program Between Visits", "FREE When You Join! (Members Area)", "Mara's Cookbook / Weight Loss Recipes block", "Start Your Weight Loss Journey Today!"],
    "industry_mode": "HEALTHCARE",
    "page_type": "service",
    "page_length_chars": 10800,
    "page_length_band": "HEALTHY",
    "estimated_grounding_coverage_pct": 25,
    "grounding_constant_provenance": "indicative — 2025-Q4 snapshot, single system; page is marginally above the 10,000-char healthy ceiling and the recommended cuts bring it back inside"
  },
  "authority_access": {
    "input_format": "markdown extraction + operator-verified raw-HTML signals (fetched 2026-06-11)",
    "onpage": {
      "schema_types_found": [],
      "author_byline_present": false,
      "date_signals_present": false,
      "note": "operator-verified against raw HTML 2026-06-11: no schema.org JSON-LD of any type, no author/reviewer byline, no visible published/modified dates; body content IS server-rendered"
    },
    "offpage_checklist": [
      { "item": "ai_crawler_access_cdn_layer", "status": "NOT_VERIFIABLE_FROM_COPY" },
      { "item": "server_side_rendering", "status": "VERIFIED_BY_OPERATOR_2026-06-11 — body content is server-rendered" },
      { "item": "server_log_ai_fetch_evidence", "status": "NOT_VERIFIABLE_FROM_COPY" },
      { "item": "brand_mention_breadth", "status": "NOT_VERIFIABLE_FROM_COPY" },
      { "item": "author_entity_online", "status": "NOT_VERIFIABLE_FROM_COPY" }
    ]
  },
  "gate_diagnosis": {
    "G1_retrieval": { "issue_count": 8, "weighted_score": 9 },
    "G2_ranking": { "issue_count": 7, "weighted_score": 9 },
    "G3_citation": { "issue_count": 10, "weighted_score": 22 },
    "dominant_gate": "G3",
    "bottleneck_summary": "The page's claims are extractable but uncitable: nearly every outcome number (1-2 lbs/day, 10-30 lbs/month, 337-to-229 lbs) lacks its qualifying condition in the same sentence, so in healthcare mode every retrieved chunk is a misinformation vector an LLM cannot safely quote."
  },
  "rewrite_urgency": {
    "level": "SEVERE",
    "derivation": "11 CRITICAL findings (>= 3 threshold) AND commoditization verdict COMMODITIZED — both SEVERE triggers met; 3 uncovered fan-out sub-queries additionally meet the SUBSTANTIAL trigger"
  },
  "zone_analysis": {
    "zone_1_chars": 1980,
    "zone_1_present": ["named_entity", "core_service", "target_user"],
    "zone_1_missing": ["anchorable_statement"],
    "body_section_count": 13,
    "section_integrity_failures": ["FREE When You Join! (Members Area) — topical binding (analyzer drift)", "Follow Your Program Between Visits — verbatim duplicate (analyzer drift)", "Mara's Cookbook / Weight Loss Recipes — topical binding as written (analyzer drift; REPURPOSE)", "FAQ 'What is HCG?' — single concept (fertility digression)"]
  },
  "commoditization_check": {
    "whole_page_substitution_passes": false,
    "substitutable_body_word_share_pct": 55,
    "unique_data_sentence_count": 5,
    "unique_data_sentences_per_1000_words": 2.7,
    "unique_angle_present": false,
    "external_verifiable_trust_signal_count": 4,
    "ai_fingerprint_marker_count": 2,
    "fail_points": 3,
    "verdict": "COMMODITIZED",
    "unique_angle_recommendation": "Commit to a named protocol the page already implies: Dr. Hartwell's three-tier physician-directed HCG protocol (Rapid / Standard / HCG-Only) segmented by weight-loss target (30+ lbs vs 15 lbs or less), with monthly BIA body-composition verification, on-site dispensing, and a published 500-900-calorie diet structure — plus a transparent statement of HCG's FDA status as a trust differentiator for the skeptical post-failed-diet reader."
  },
  "intent_coverage": [
    {
      "intent": "hcg injections for weight loss (doctor-supervised — safe, legitimate, this clinic credible enough to book?)",
      "is_primary": true,
      "extractable_answer_present": false,
      "section_name": "Hero (Zone 1)",
      "gap_reason": "the opening states the offer but no sentence passes the anchorable test — no specific data point and the substitution test fails; finding find_001 builds the Zone 1 anchor"
    }
  ],
  "fanout_coverage": {
    "note": "reasoned estimate of the engine fan-out distribution — not engine telemetry; no PAA data supplied",
    "subqueries": [
      { "subquery": "what is hcg and how does it work for weight loss", "dimension": "definition_mechanism", "source": "ENUMERATED", "coverage": "COVERED", "covering_section": "HCG Helps With Weight Loss + FAQ 'What is HCG?'", "recommended_home": null },
      { "subquery": "how much does the hcg diet cost at a medical clinic", "dimension": "cost", "source": "ENUMERATED", "coverage": "UNCOVERED", "covering_section": null, "recommended_home": "BODY_SECTION" },
      { "subquery": "what do you eat on the hcg diet — 500-calorie diet structure", "dimension": "process_diet", "source": "ENUMERATED", "coverage": "PARTIAL", "covering_section": "FAQ 'What is HCG?' (one parenthetical)", "recommended_home": "BODY_SECTION" },
      { "subquery": "how long does the hcg program take / how fast will I see results", "dimension": "duration_timeline", "source": "ENUMERATED", "coverage": "UNCOVERED", "covering_section": null, "recommended_home": "FAQ_ENTRY" },
      { "subquery": "is hcg safe for weight loss — side effects", "dimension": "risk_safety", "source": "ENUMERATED", "coverage": "PARTIAL", "covering_section": "FAQ 'Is HCG safe for weight loss?' / 'Are there adverse effects for men?'", "recommended_home": "EXTEND_EXISTING_SECTION" },
      { "subquery": "who qualifies for hcg / who should not take it", "dimension": "eligibility", "source": "ENUMERATED", "coverage": "PARTIAL", "covering_section": "Program Options (weight-target self-selection only)", "recommended_home": "FAQ_ENTRY" },
      { "subquery": "hcg injections vs semaglutide or phentermine", "dimension": "comparison", "source": "ENUMERATED", "coverage": "PARTIAL", "covering_section": "Rapid Weight Loss Medications + FAQ combination answers", "recommended_home": "EXTEND_EXISTING_SECTION" },
      { "subquery": "prescription hcg injections vs homeopathic hcg drops", "dimension": "comparison", "source": "ENUMERATED", "coverage": "PARTIAL", "covering_section": "HCG Helps With Weight Loss (one sentence)", "recommended_home": "FAQ_ENTRY" },
      { "subquery": "how much weight can I lose with hcg", "dimension": "outcomes", "source": "ENUMERATED", "coverage": "COVERED", "covering_section": "FAQ 'How much weight can I expect to lose with HCG?'", "recommended_home": null },
      { "subquery": "what happens at the first consultation / how the program works", "dimension": "process", "source": "ENUMERATED", "coverage": "COVERED", "covering_section": "How Our Weight Loss Program Works + HCG Only inclusions", "recommended_home": null },
      { "subquery": "hcg diet clinic near Riverton / North Shoreline / Bayside SC", "dimension": "location", "source": "ENUMERATED", "coverage": "PARTIAL", "covering_section": "Why Choose Us? ('3 convenient locations' + phone); analyzer reports a locations block on the live page absent from the extracted body", "recommended_home": "EXTEND_EXISTING_SECTION" },
      { "subquery": "can I combine hcg with semaglutide or my current program", "dimension": "compatibility", "source": "ENUMERATED", "coverage": "COVERED", "covering_section": "FAQ (two combination entries)", "recommended_home": null },
      { "subquery": "is Dr. Hartwell's hcg program legit — reviews", "dimension": "provider_selection", "source": "ENUMERATED", "coverage": "PARTIAL", "covering_section": "What Our Patients Say About Our Program + Meet Dr. Hartwell", "recommended_home": "EXTEND_EXISTING_SECTION" }
    ],
    "uncovered_count": 2,
    "top_gaps_emitted_as_findings": 3
  },
  "competitive_differentiation": {
    "what": { "present": true, "evidence": "HCG injections as add-on or standalone within named Rapid/Standard programs" },
    "who": { "present": true, "evidence": "Dr. Hartwell's Example Weight Loss Clinics / Kevin M Hartwell, MD" },
    "what_job": { "present": true, "evidence": "lose stubborn fat from around problem areas like the stomach, hips and waist" },
    "what_constraint": { "present": true, "evidence": "designed for people wanting to lose 30 lbs or more / typically need to lose 15 lbs or less — but located in Program Options, far from the other signals" },
    "result": "PARTIAL",
    "extractable_3_sentence_window": null,
    "substitution_test_passed": false,
    "monopoly_market_bypass": false,
    "skipped_educational_mode": false
  },
  "format_audit": {
    "tables_used_appropriately": false,
    "lists_used_appropriately": true,
    "headings_query_matchable": true,
    "heading_issues": [
      { "heading": "Weight Loss Medications", "problem": "duplicate stacked H2 directly beneath 'Rapid Weight Loss Medications' — false section boundary for chunking systems" }
    ]
  },
  "dry_violations": [
    {
      "section_name": "Follow Your Program / Between Visits (second app section)",
      "repeated_claim": "With the MealTrack Planner & Fitness Tracker app, you can follow the calorie specific meal plan and activities Dr. Hartwell prescribes for you right from your computer or phone",
      "first_section": "Follow Your Program Between Office Visits",
      "rewrite_action": "delete the duplicate section; reconcile the conflicting eligibility footnotes ('Rapid Program Only' vs 'Rapid or Rapid+ Programs Only') and keep the correct one in the surviving section"
    },
    {
      "section_name": "FREE When You Join! (Members Area)",
      "repeated_claim": "Access to our Private Members Area plus Mara's Cookbook (also stated in both program inclusion lists and Why Choose Us)",
      "first_section": "Program Options",
      "rewrite_action": "cut the members-area section; the claim already lives in the program inclusion lists"
    }
  ],
  "trust_signals": {
    "present": ["named_practitioner_md", "named_nurse_practitioner", "years_of_operation_20_plus", "named_technology_MealTrack Planner_and_bia", "named_product_loris_cookbook_60_recipes", "phone_number", "onsite_medication_dispensing"],
    "missing": ["practitioner_licence_number_and_certifying_board", "street_addresses_for_3_locations", "named_external_sources", "pricing", "honest_side_effect_risk_data", "insurance_payment_information", "author_byline"]
  },
  "anchorable_statements": {
    "zone_1_anchorable_present": false,
    "zone_1_anchorable_quote": null,
    "intent_anchorable_count": 0,
    "intent_anchorable_total": 1,
    "gaps": [
      { "intent": "primary", "should_appear_in_section": "Hero (Zone 1) — supplied by finding find_001; the new cost and diet-structure sections must each open with their own anchorable statement" }
    ]
  },
  "condition_preservation": {
    "violations": [
      { "claim_quote": "Clinical observations demonstrate daily weight reduction of 0.45-0.9 kg, predominantly from adipose tissue stores.", "missing_condition": "any hedge or population/cohort condition; claim lives in a machine-only image alt attribute", "fix_instruction": "strip the clinical paragraph from the alt attribute; move surviving claims into visible body copy with inline hedges (find_002)" },
      { "claim_quote": "When I started this journey, I weighed 337 lb. and I’m currently sitting at 229 lb.", "missing_condition": "results-not-typical hedge (exists only in the gallery disclaimer sections away)", "fix_instruction": "duplicate the hedge directly beneath the hero quote; leave the protected disclaimer intact (find_003)" },
      { "claim_quote": "Lose 10-30 lbs. a month eating foods from your local store", "missing_condition": "individual-results-vary hedge in the same line", "fix_instruction": "rewrite the bullet with the inline hedge (find_005)" },
      { "claim_quote": "When combined with our calorie specific diet, HCG injections can help you lose 1-2 pounds of stubborn fat a day from around problem areas like the stomach, hips and thighs.", "missing_condition": "cohort/timeframe and results-vary clause", "fix_instruction": "merge population, calorie condition, [DATA_NEEDED: cohort], and hedge into the same sentence (find_006)" },
      { "claim_quote": "Those who follow our Rapid Weight Loss Program with HCG report a 1-2 lb. drop in weigh per day!", "missing_condition": "the 'results vary by person' hedge sits two sentences later", "fix_instruction": "fold the hedge into the claim sentence (find_007)" },
      { "claim_quote": "HCG is currently being used in weight loss clinics because it works and it is safe.", "missing_condition": "efficacy hedge and FDA-status disclosure", "fix_instruction": "rewrite as a hedged, dose-anchored statement disclosing the FDA position (find_008)" },
      { "claim_quote": "It is commonly used as a fertility drug with no side effects.", "missing_condition": "absolute safety claim with no hedge possible — delete with the fertility digression", "fix_instruction": "[DELETE] (find_009)" }
    ]
  },
  "cta_blocks_detected": [
    { "section_name": "Book Now / Call Us (hero)", "trapped_signal": null, "excluded_from_assessment": true },
    { "section_name": "Book Now / Call Us (after HCG Helps With Weight Loss)", "trapped_signal": null, "excluded_from_assessment": true },
    { "section_name": "Book Now / Call Us (after Program Options)", "trapped_signal": null, "excluded_from_assessment": true },
    { "section_name": "Book Now / Call Us (after Why Choose Us?)", "trapped_signal": null, "excluded_from_assessment": true },
    { "section_name": "Start Your Weight Loss Journey Today!", "trapped_signal": null, "excluded_from_assessment": true },
    { "section_name": "If you are thinking about trying HCG for weight loss, call our office today… + Book Now (FAQ close)", "trapped_signal": null, "excluded_from_assessment": true }
  ],
  "protected_sections": [
    {
      "section_id": "testimonial_results_disclaimer",
      "section_name": "Testimonial results disclaimer (Our Success Stories)",
      "protection_type": "COMPLIANCE_OTHER",
      "original_text": "*The results described in these testimonials may not be typical. Individual results may vary. The testimonials are for illustrative purposes only and are meant to showcase some of the results Dr. Hartwell’s Example Weight Loss Clinics have produced.",
      "rewrite_permissions": {
        "can_delete": false,
        "can_shorten": false,
        "can_relocate": true,
        "can_rewrite_for_clarity": false,
        "must_preserve_meaning": true
      },
      "rewriter_instruction": "Preserve verbatim (FTC testimonial disclaimer). May be relocated within the page but must not be paraphrased, shortened, or removed. Finding find_003 requires DUPLICATING its hedge beside the hero quote — duplication, not relocation."
    }
  ],
  "findings": [
    { "id": "find_001", "severity": "CRITICAL", "gate": "G3", "section_name": "Hero (Zone 1)", "check": "anchorable_statement", "issue_type": "MISSING_ANCHORABLE_STATEMENT", "flagged_sentence": "Dr. Hartwell’s Example Weight Loss Clinics is a weight loss clinic offering HCG Injections to help patients lose weight fast and keep it off!", "rewrite": "Dr. Hartwell’s Example Weight Loss Clinics is a physician-directed weight loss clinic with three the clinic's state locations (Riverton, North Shoreline, and Bayside) offering pharmaceutical-grade HCG injections combined with a 500–900-calorie structured diet to target stubborn belly fat; a free consultation determines whether the program suits you, and individual results vary.", "rationale": "Zone 1 has no sentence passing the 4-test anchorable check — the opener has no data point and fails substitution; this rewrite packs entity, locations, program specifics, condition, and hedge into the highest-retrieval zone." },
    { "id": "find_002", "severity": "CRITICAL", "gate": "G3", "section_name": "Lose Weight with HCG:", "check": "condition_preservation", "issue_type": "CONDITION_SEPARATED", "flagged_sentence": "Clinical observations demonstrate daily weight reduction of 0.45-0.9 kg, predominantly from adipose tissue stores.", "rewrite": "Replace the entire alt attribute with: \"Patient receiving a subcutaneous HCG injection at Dr. Hartwell's Example Weight Loss Clinics\" — and move any claim worth keeping into visible body copy with its hedge in the same sentence. Apply the same fix to the Image 6 alt (\"patients can lose 1-2 pounds of fat per day…\").", "rationale": "Machine-only artifact verified in the raw HTML: a full clinical paragraph with unhedged outcome claims lives in an image alt attribute — invisible to human readers but fully extractable by AI crawlers, making it a compliance liability in precisely the channel this audit optimizes; healthcare auto-escalation applies. The flagged sentence is quoted from the alt text present in the extraction." },
    { "id": "find_003", "severity": "CRITICAL", "gate": "G3", "section_name": "Hero (Zone 1)", "check": "condition_preservation", "issue_type": "CONDITION_DUPLICATION_REQUIRED", "flagged_sentence": "When I started this journey, I weighed 337 lb. and I’m currently sitting at 229 lb.", "rewrite": "Keep the quote verbatim and append directly beneath it: \"— Ian, Rapid Program + HCG patient. Results are not typical; individual results vary.\"", "rationale": "Numeric outcome testimonial in Zone 1 whose qualifying condition exists only inside the protected gallery disclaimer sections away — duplicate the hedge inline and leave the protected block intact (healthcare auto-escalation)." },
    { "id": "find_004", "severity": "CRITICAL", "gate": "G1", "section_name": "Meet Dr. Hartwell and the Rapid Weight Loss Team", "check": "entity_completeness", "issue_type": "MISSING_ENTITY_CREDENTIAL", "flagged_sentence": "Kevin M Hartwell, MD Bariatric Physician", "rewrite": "Kevin M. Hartwell, MD — board-certified bariatric physician [DATA_NEEDED: certifying board, e.g. ABOM, and SC licence number], 20+ years directing medically supervised weight loss programs in Riverton, North Shoreline, and Bayside, SC.", "rationale": "Healthcare auto-escalation: an expert credential stated without registration/licence number or issuing body ('Board certified' in Why Choose Us also names no board); completing it is the cheapest medical-legitimacy win for the analyzer's skeptical reader." },
    { "id": "find_005", "severity": "CRITICAL", "gate": "G3", "section_name": "Why Choose Us?", "check": "condition_preservation", "issue_type": "CONDITION_SEPARATED", "flagged_sentence": "Lose 10-30 lbs. a month eating foods from your local store", "rewrite": "Patients typically lose 10–30 lbs. a month eating foods from your local store, though individual results vary.", "rationale": "Numeric outcome claim in a bullet with no qualifying condition anywhere in the section — healthcare auto-escalation requires the hedge in the same line." },
    { "id": "find_006", "severity": "CRITICAL", "gate": "G3", "section_name": "FAQ — How does HCG work for weight loss?", "check": "condition_preservation", "issue_type": "CONDITION_SEPARATED", "flagged_sentence": "When combined with our calorie specific diet, HCG injections can help you lose 1-2 pounds of stubborn fat a day from around problem areas like the stomach, hips and thighs.", "rewrite": "When combined with Dr. Hartwell's calorie-specific diet (500–900 calories per day), patients report losing 1–2 pounds of stubborn fat per day from areas like the stomach, hips and thighs [DATA_NEEDED: cohort size and timeframe]; individual results vary with health status and adherence.", "rationale": "Numeric outcome claim with no inline results-vary condition; healthcare auto-escalation. The rewrite also re-anchors the clinic entity into the FAQ chunk." },
    { "id": "find_007", "severity": "CRITICAL", "gate": "G3", "section_name": "FAQ — How much weight can I expect to lose with HCG?", "check": "condition_preservation", "issue_type": "CONDITION_SEPARATED", "flagged_sentence": "Those who follow our Rapid Weight Loss Program with HCG report a 1-2 lb. drop in weigh per day!", "rewrite": "Patients who follow Dr. Hartwell's Rapid Weight Loss Program with HCG typically lose 10–30 pounds per month [DATA_NEEDED: cohort data], though individual results vary by person, health status and adherence.", "rationale": "The hedge ('results vary by person') is stranded two sentences after the numeric claim; extraction strips it. The rewrite consolidates claim + hedge in one sentence and fixes the 'weigh' typo (healthcare auto-escalation)." },
    { "id": "find_008", "severity": "CRITICAL", "gate": "G3", "section_name": "FAQ — Is HCG safe for weight loss?", "check": "condition_preservation", "issue_type": "CONDITION_SEPARATED", "flagged_sentence": "HCG is currently being used in weight loss clinics because it works and it is safe.", "rewrite": "At weight-loss doses (250 IU per day — far below fertility doses of up to 6,000 IU), HCG is prescribed and supervised by Dr. Hartwell's medical team; it may support fat loss when combined with a supervised low-calorie diet, though the FDA has not approved HCG for weight loss and individual results vary.", "rationale": "Therapeutic efficacy and safety claim with no hedge — healthcare auto-escalation; the rewrite preserves the genuinely specific dosage contrast while adding the hedge and FDA disclosure (see find_016 for the verification requirement)." },
    { "id": "find_009", "severity": "CRITICAL", "gate": "G3", "section_name": "FAQ — What is HCG?", "check": "condition_preservation", "issue_type": "CONDITION_SEPARATED", "flagged_sentence": "It is commonly used as a fertility drug with no side effects.", "rewrite": "[DELETE]", "rationale": "Absolute 'no side effects' safety claim (healthcare auto-escalation) inside a fertility-treatment digression that also breaks the single-concept rule — delete the digression and keep the answer focused on the weight-loss definition." },
    { "id": "find_010", "severity": "CRITICAL", "gate": "G2", "section_name": "FAQ — What can I do to ensure I lose 1 lb. a day or more while taking HCG?", "check": "information_density", "issue_type": "FILLER_OPENER", "flagged_sentence": "Things you can do to ensure that you lose one pound a day or more.", "rewrite": "[DELETE] — lead with the hedged tips: \"To support your results on Dr. Hartwell's program: drink more than 2 liters of water daily, use the B-12/Lipotropic injections, and avoid high-fructose corn syrup, artificial sweeteners, and fast food — individual results vary.\"", "rationale": "Opener fails the 3-element filler test (0 of 3: no new named entity, no data point, no condition) and 'ensure… one pound a day' reads as an outcome guarantee in healthcare mode." },
    { "id": "find_011", "severity": "CRITICAL", "gate": "G2", "section_name": "FREE When You Join! (Members Area)", "check": "section_integrity", "issue_type": "OFF_TOPIC_SECTION", "flagged_sentence": null, "rewrite": "Remove the section entirely; its payloads (members-area recipes, MealTrack Planner access, Eat Smart videos) are already stated in the Program Options inclusion lists and the app section.", "rationale": "Analyzer drift section (auto-fail topical binding): a retention upsell serving the author's intent, not the evaluating reader's decision, and answering no fan-out sub-query; structural finding only — disposition CUT, no sentence polish." },
    { "id": "find_012", "severity": "IMPORTANT", "gate": "G1", "section_name": "Program Options", "check": "fanout_coverage", "issue_type": "UNCOVERED_SUBQUERY", "flagged_sentence": null, "rewrite": "Add a body section 'HCG Program Costs at Dr. Hartwell's' adjoining Program Options: a 3-row comparison table (Rapid + HCG / Standard + HCG / HCG Only) with columns monthly price [DATA_NEEDED: prices], visit cadence, inclusions, and who it's for — a BODY_SECTION, not an FAQ one-liner, because cost is decision-critical.", "rationale": "'how much does the hcg diet cost' is the highest-commercial-value fan-out gap; the page lists three programs with zero prices, so the cost sub-query is silently lost to competitors with pricing sections." },
    { "id": "find_013", "severity": "IMPORTANT", "gate": "G1", "section_name": "Mara's Cookbook / Weight Loss Recipes", "check": "fanout_coverage", "issue_type": "UNCOVERED_SUBQUERY", "flagged_sentence": null, "rewrite": "REPURPOSE this block into a body section 'What You'll Eat on the HCG Diet': daily calorie band (500–900), what Phase 1 vs Phase 2 means, a sample day of meals, and grocery-store sourcing. Salvage list: 'over 60 recipes approved by Dr. Hartwell', the Phase 1 (16) / Phase 2 (51) recipe split, and the meal-category breadth (Breakfast, Main Dishes, Appetizers, Soups, Salads, Desserts).", "rationale": "Per the intent analyzer, this block gestures at the reader's real question — what will I actually eat? — without answering it; disposition REPURPOSE (not cut): the section's new job is the diet-structure answer, with the listed facts carried over and no polish of copy that won't survive." },
    { "id": "find_014", "severity": "IMPORTANT", "gate": "G1", "section_name": "Frequently Asked Questions About HCG", "check": "fanout_coverage", "issue_type": "UNCOVERED_SUBQUERY", "flagged_sentence": null, "rewrite": "Add an FAQ entry: 'How long does the HCG program last?' — 40–80 words naming phase lengths and typical program duration [DATA_NEEDED: round length and follow-up schedule], with 'individual results vary' inline.", "rationale": "Duration/timeline is a high-probability fan-out dimension with zero coverage anywhere on the page; a tight self-contained FAQ_ENTRY is the right chunk size for it." },
    { "id": "find_015", "severity": "IMPORTANT", "gate": "G2", "section_name": "Follow Your Program / Between Visits (second app section)", "check": "dry", "issue_type": "DRY_VIOLATION", "flagged_sentence": null, "rewrite": "Delete the duplicated app section (responsive page-builder artifact). Before deleting, reconcile the conflicting eligibility footnotes — 'Rapid Program Only' vs 'Rapid or Rapid+ Programs Only' [DATA_NEEDED: which is correct] — and keep the correct one in the surviving section.", "rationale": "A verbatim duplicate splits the accountability sub-query's signal across two identical chunks and dilutes grounding budget; disposition CUT — structural finding plus footnote salvage only." },
    { "id": "find_016", "severity": "IMPORTANT", "gate": "G3", "section_name": "FAQ — Is HCG safe for weight loss?", "check": "anchorable_statement", "issue_type": "VERIFY_BEFORE_PUBLISH", "flagged_sentence": "HCG is a natural hormone and safe for men and women with correct dosages.", "rewrite": "Operator action (not a copy edit): obtain legal/compliance review of all HCG safety-and-efficacy claims against the FDA's published position (HCG is not FDA-approved for weight loss, and FDA-required labeling for HCG weight-loss products states it has not been demonstrated to be effective adjunctive therapy for obesity) before republishing; the rewriter must not restate these claims as fact.", "rationale": "The page's safety/efficacy claims are externally contradicted by the regulator; the audit cannot verify them from the page, and shipping them unverified makes the rewrite a misinformation vector." },
    { "id": "find_017", "severity": "IMPORTANT", "gate": "G3", "section_name": "Lose Weight with HCG:", "check": "extractability", "issue_type": "UNRESOLVED_PRONOUN", "flagged_sentence": "It’s for patients looking for additional help targeting belly and love handle fat.", "rewrite": "HCG is for patients looking for additional help targeting belly and love handle fat.", "rationale": "'It's' has no in-sentence antecedent; extracted alone the sentence doesn't identify its subject — a Zone 1 coreference failure." },
    { "id": "find_018", "severity": "IMPORTANT", "gate": "G1", "section_name": "Rapid Weight Loss Medications", "check": "format_appropriateness", "issue_type": "FORMAT_MISMATCH", "flagged_sentence": null, "rewrite": "Convert the three medication link-blobs into a comparison table — columns: Medication / What it does / How it's taken / Included in which program — rows: Phentermine (oral appetite suppressant), HCG (weekly injection targeting stored belly/waist fat), B12/Lipotropics (weekly injection for energy and fat metabolism).", "rationale": "Three entities compared across the same attributes is table content; the current run-on link texts ('Phentermine Safe & Effective Appetite Suppressant –Jump Start for Weight Loss – Oral Medication Book Appointment') are barely parseable by humans or machines." },
    { "id": "find_019", "severity": "IMPORTANT", "gate": "G2", "section_name": "Our Success Stories", "check": "information_density", "issue_type": "INFORMATION_DENSITY_LOW", "flagged_sentence": null, "rewrite": "Add a text caption under each before/after photo — first name, program, amount lost, timeframe [DATA_NEEDED: confirm per patient], plus 'individual results vary' — and fix the mismatched alt attributes (several different patients currently share the alt text 'Caroline before after').", "rationale": "Seventeen proof cases contribute zero machine-readable outcome data: the visible text is filter labels only, so the page's strongest evidence is invisible to extraction." },
    { "id": "find_020", "severity": "IMPORTANT", "gate": "G2", "section_name": "What Our Patients Say About Our Program", "check": "trust_signals", "issue_type": "ANONYMOUS_TESTIMONIAL", "flagged_sentence": "Staff was extremely professional and supportive. 10/10 would recommend.", "rewrite": "Replace 2–3 generic quotes with consented outcome-bearing ones naming the program and a specific result with an inline hedge, e.g.: \"I lost [DATA_NEEDED: amount] lbs in [DATA_NEEDED: months] on the Standard Program + HCG.\" — Jodie K. (individual results vary).", "rationale": "Partial-name testimonials with no program, amount, or timeframe are decoration, not citable proof — swappable with any clinic's reviews and contributing to the commoditization fail." },
    { "id": "find_021", "severity": "IMPORTANT", "gate": "G2", "section_name": "FAQ — Are there adverse effects for men?", "check": "natural_language_quality", "issue_type": "SUBSTITUTION_TEST_FAILED", "flagged_sentence": "It cannot be sufficiently emphasized that HCG is not a sex-hormone, that its action is identical in men, women, children and in those cases in which the sex-glands no longer function owing to old age or their surgical removal.", "rewrite": "At the weight-loss doses Dr. Hartwell prescribes (250 IU daily), HCG is not a sex hormone and acts the same way in men and women; men in the program receive the same dosing and supervision as women, and side effects are reviewed at every follow-up visit [DATA_NEEDED: clinic-observed side-effect profile].", "rationale": "Verbatim 1954 Simeons manuscript boilerplate hosted by every HCG clinic — archaic register, fails the substitution test, inappropriately references children, and supplies the commoditization check's clearest evidence; the rewrite re-anchors the clinic and answers the actual question." },
    { "id": "find_022", "severity": "IMPORTANT", "gate": "G1", "section_name": null, "check": "authority_access", "issue_type": "MISSING_AUTHOR_ATTRIBUTION", "flagged_sentence": null, "rewrite": "Add a visible byline/review line to the page template: 'Medically reviewed by Kevin M. Hartwell, MD [DATA_NEEDED: credentials/licence], last reviewed [date]'.", "rationale": "Operator-verified raw HTML (2026-06-11) shows no author or reviewer attribution on YMYL healthcare content; 2026 quality-update direction explicitly favors named human experts." },
    { "id": "find_023", "severity": "MINOR", "gate": "G1", "section_name": null, "check": "authority_access", "issue_type": "MISSING_SCHEMA_MARKUP", "flagged_sentence": null, "rewrite": "Add JSON-LD: MedicalBusiness/LocalBusiness (name, three location addresses, phone, physician) and FAQPage for the nine Q&A pairs.", "rationale": "Operator-verified raw HTML (2026-06-11) contains no schema.org JSON-LD of any type; recommended as hygiene for entity disambiguation and Bing/Copilot only — the sole controlled study (2026-05) found no AI-citation uplift from schema, so this is deliberately MINOR." },
    { "id": "find_024", "severity": "MINOR", "gate": "G1", "section_name": "Rapid Weight Loss Medications", "check": "heading_hygiene", "issue_type": "GENERIC_HEADING", "flagged_sentence": "Weight Loss Medications", "rewrite": "Delete the stacked duplicate H2 'Weight Loss Medications' (it sits directly under 'Rapid Weight Loss Medications'); keep a single descriptive H2 such as 'Weight Loss Medications We Prescribe: Phentermine, HCG, B12/Lipotropics'.", "rationale": "Two H2s back-to-back create a false section boundary for heading-based chunkers and the surviving heading should carry the medication entities for query matching." },
    { "id": "find_025", "severity": "MINOR", "gate": "G2", "section_name": "In the Media", "check": "trust_signals", "issue_type": "INFORMATION_DENSITY_LOW", "flagged_sentence": null, "rewrite": "Name the outlets in visible text: 'As featured in [DATA_NEEDED: outlet names]' — keep the logos, add the words.", "rationale": "A logo-only strip carries zero machine-readable text; the third-party-coverage trust signal is invisible to every AI engine." }
  ],
  "rewrite_brief": {
    "dominant_gate_focus": "G3",
    "target_length_chars_min": 6000,
    "target_length_chars_max": 10000,
    "keep_sections": ["Hero (HCG for Belly Fat Reduction)", "Lose Weight with HCG:", "HCG Helps With Weight Loss", "How Our Weight Loss Program Works", "Program Options", "Rapid Weight Loss Medications", "Our Success Stories", "What Our Patients Say About Our Program", "In the Media", "Follow Your Program Between Office Visits", "Meet Dr. Hartwell and the Rapid Weight Loss Team", "Why Choose Us?", "Frequently Asked Questions About HCG", "Locations (North Shoreline / Riverton / Bayside)", "Testimonial results disclaimer (protected)"],
    "merge_sections": [],
    "cut_sections": ["Follow Your Program / Between Visits (duplicate app section)", "FREE When You Join! (Members Area)", "Start Your Weight Loss Journey Today! (CTA interstitial)"],
    "primary_focus": "Compliance-first: merge an inline hedge into every numeric outcome claim (1-2 lbs/day, 10-30 lbs/month, the Ian testimonial), strip the unhedged clinical paragraph from the image alt attributes, and complete Dr. Hartwell's credentials. Then build the Zone 1 anchorable statement, add the two missing decision sections (pricing table, diet structure from the repurposed cookbook block), and move the team section above the selling so legitimacy lands first for the skeptical post-failed-diet reader.",
    "unique_angle_recommendation": "Commit to a named protocol the page already implies: Dr. Hartwell's three-tier physician-directed HCG protocol (Rapid / Standard / HCG-Only) segmented by weight-loss target (30+ lbs vs 15 lbs or less), with monthly BIA body-composition verification, on-site dispensing, and a published 500-900-calorie diet structure — plus a transparent statement of HCG's FDA status as a trust differentiator no competitor HCG page offers.",
    "do_not_do": [
      "Do not delete, shorten, or paraphrase the testimonial results disclaimer — duplicate its hedge beside the hero quote, leaving the original intact.",
      "Do not invent prices, cohort data, licence numbers, board names, or patient outcomes the page does not contain — use [DATA_NEEDED:] placeholders and the operator_fact_requests array.",
      "Do not soften or remove hedges to make claims read more confidently; in healthcare mode the hedge belongs in the same sentence as the claim.",
      "Do not restate the HCG safety/efficacy claims as fact before the operator's legal/compliance review (find_016).",
      "Do not place outcome or clinical claims in image alt attributes — alt text is descriptive only.",
      "Do not add an FAQ entry re-answering cost once the pricing body section exists — one sub-query, one canonical home (signal splitting)."
    ],
    "faq_plan": [
      { "question": "How long does the HCG program last?", "answer_guidance": "40-80 words; phase lengths and typical duration [DATA_NEEDED: round length and follow-up schedule]; 'individual results vary' inline", "derived_from": "fanout:duration_timeline" },
      { "question": "Who should not take HCG? (contraindications and side effects)", "answer_guidance": "40-80 words; name contraindication categories and the consult-first screening step [DATA_NEEDED: clinic screening criteria]; hedge inline", "derived_from": "fanout:eligibility" },
      { "question": "What's the difference between prescription HCG injections and homeopathic HCG drops?", "answer_guidance": "40-80 words; expand the page's one-line 'real HCG, not homeopathic brands' differentiation seed: prescription-grade, physician-dosed (250 IU/day), dispensed on site", "derived_from": "fanout:comparison_homeopathic" },
      { "question": "Is HCG FDA-approved for weight loss?", "answer_guidance": "40-80 words; honest answer (it is not — approved for other uses, prescribed off-label under physician supervision) [VERIFY with legal review per find_016]; transparency is the trust play for the skeptical reader", "derived_from": "fanout:risk_safety" }
    ],
    "recommended_flow": [
      { "position": 1, "section": "Hero (HCG for Belly Fat Reduction)", "disposition": "KEEP_IN_PLACE", "serves_subquery": "primary intent", "human_goal": "query answered with a credible, hedged anchor (named clinic, MD, 3 cities) so the skeptic doesn't bounce", "cta_after": false },
      { "position": 2, "section": "Lose Weight with HCG:", "disposition": "KEEP_IN_PLACE", "serves_subquery": "who is HCG for / how is it purchased", "human_goal": "failed-diet reader self-identifies and sees HCG as add-on or standalone", "cta_after": false },
      { "position": 3, "section": "HCG Helps With Weight Loss", "disposition": "KEEP_IN_PLACE", "serves_subquery": "how does hcg work for weight loss", "human_goal": "the skeptic's 'does this actually work' answered with mechanism and honest hedged expectations", "cta_after": false },
      { "position": 4, "section": "Meet Dr. Hartwell and the Rapid Weight Loss Team", "disposition": "MOVE", "serves_subquery": "is this clinic/doctor legitimate", "human_goal": "medical legitimacy lands before any selling: board-certified MD and NP with completed credentials", "cta_after": false },
      { "position": 5, "section": "NEW: What You'll Eat on the HCG Diet (500-900-Calorie Structure)", "disposition": "NEW", "serves_subquery": "fanout:process_diet — what do you eat on the hcg diet", "human_goal": "the 'can I actually live on this diet' objection cleared with concrete meals from a normal grocery store", "cta_after": false },
      { "position": 6, "section": "Program Options", "disposition": "KEEP_IN_PLACE", "serves_subquery": "which hcg program fits me", "human_goal": "reader self-selects a tier (30+ lbs / 15 lbs or less / medication-only)", "cta_after": false },
      { "position": 7, "section": "NEW: HCG Program Costs", "disposition": "NEW", "serves_subquery": "fanout:cost — how much does the hcg diet cost", "human_goal": "price transparency clears the last rational objection; reader can budget before booking", "cta_after": true },
      { "position": 8, "section": "How Our Weight Loss Program Works", "disposition": "MOVE", "serves_subquery": "what happens when I sign up", "human_goal": "de-risk the commitment: free consultation first, then medications and follow-ups", "cta_after": false },
      { "position": 9, "section": "Rapid Weight Loss Medications", "disposition": "KEEP_IN_PLACE", "serves_subquery": "hcg vs phentermine vs b12", "human_goal": "reader understands the toolkit and where HCG fits via the comparison table", "cta_after": false },
      { "position": 10, "section": "Our Success Stories", "disposition": "KEEP_IN_PLACE", "serves_subquery": "does this work for people like me", "human_goal": "proof: captioned, named outcomes with timeframes, hedged", "cta_after": false },
      { "position": 11, "section": "What Our Patients Say About Our Program", "disposition": "KEEP_IN_PLACE", "serves_subquery": "is Dr. Hartwell's program legit / reviews", "human_goal": "third-party voices confirm safety, supervision, and no-judgement support", "cta_after": true },
      { "position": 12, "section": "Follow Your Program Between Office Visits", "disposition": "KEEP_IN_PLACE", "serves_subquery": "what support do I get between visits", "human_goal": "the failed-solo-dieter believes accountability will be different this time", "cta_after": false },
      { "position": 13, "section": "Frequently Asked Questions About HCG", "disposition": "KEEP_IN_PLACE", "serves_subquery": "safety, dosage, timeline, eligibility, combination edge cases", "human_goal": "remaining objections cleared one self-contained micro-answer at a time", "cta_after": false },
      { "position": 14, "section": "Locations (North Shoreline / Riverton / Bayside)", "disposition": "KEEP_IN_PLACE", "serves_subquery": "hcg clinic near me in SC", "human_goal": "reader confirms they can do this nearby and books the free consultation (must surface as machine-readable text with addresses)", "cta_after": true },
      { "position": null, "section": "Mara's Cookbook / Weight Loss Recipes", "disposition": "REPURPOSE", "serves_subquery": "fanout:process_diet", "human_goal": "content folds into position 5; salvage the 60+ recipe count, Phase 1/Phase 2 split, and meal categories", "cta_after": false },
      { "position": null, "section": "Follow Your Program / Between Visits (duplicate)", "disposition": "CUT", "serves_subquery": null, "human_goal": null, "cta_after": false },
      { "position": null, "section": "FREE When You Join! (Members Area)", "disposition": "CUT", "serves_subquery": null, "human_goal": null, "cta_after": false },
      { "position": null, "section": "Start Your Weight Loss Journey Today!", "disposition": "CUT", "serves_subquery": null, "human_goal": null, "cta_after": false }
    ]
  },
  "operator_fact_requests": [
    { "field": "Program pricing for Rapid + HCG, Standard + HCG, and HCG Only (and any consultation/medication fees)", "reason": "Required for the new HCG Program Costs body section — the highest-value fan-out gap (find_012)." },
    { "field": "Dr. Hartwell's certifying board (e.g. ABOM) and SC medical licence number; Beth Hanlon's NP credentials", "reason": "Healthcare auto-escalation: credentials stated without issuing body or number (find_004)." },
    { "field": "Cohort data behind the 1-2 lbs/day and 10-30 lbs/month claims (sample size, timeframe, population)", "reason": "Required for condition preservation in findings find_006 and find_007; without it the rewrite uses [DATA_NEEDED:] placeholders." },
    { "field": "Program duration: HCG round length, phase lengths, follow-up schedule", "reason": "Required for the timeline FAQ entry (find_014)." },
    { "field": "Correct MealTrack Planner eligibility — 'Rapid Program Only' or 'Rapid or Rapid+ Programs Only'", "reason": "The duplicate sections carry conflicting footnotes; reconcile before cutting the duplicate (find_015)." },
    { "field": "Street addresses for the Riverton, North Shoreline, and Bayside locations", "reason": "Location sub-query is PARTIAL; the locations block must surface as machine-readable body text with addresses." },
    { "field": "Patient-consented outcome details for testimonials and before/after captions (name, program, amount lost, timeframe)", "reason": "Required to convert decoration proof into citable proof (find_019, find_020)." },
    { "field": "Legal/compliance review of all HCG safety-and-efficacy claims against the FDA's published position", "reason": "find_016 — the page's claims are externally contradicted by the regulator; the rewrite cannot ship them as fact." },
    { "field": "Media outlet names for the In the Media strip", "reason": "Trust signal currently trapped in logo images (find_025)." }
  ],
  "validation_plan": {
    "prompt_corpus": [
      { "prompt": "best hcg diet clinic near Riverton", "intent_class": "discovery", "derived_from": "fanout:location" },
      { "prompt": "doctor supervised hcg injections near North Shoreline", "intent_class": "discovery", "derived_from": "fanout:location" },
      { "prompt": "hcg injections vs semaglutide for stubborn belly fat — which should I do?", "intent_class": "comparison", "derived_from": "fanout:comparison" },
      { "prompt": "are prescription hcg shots better than the hcg drops sold online?", "intent_class": "comparison", "derived_from": "fanout:comparison_homeopathic" },
      { "prompt": "hcg diet vs phentermine for fast weight loss", "intent_class": "comparison", "derived_from": "fanout:comparison" },
      { "prompt": "I've failed every diet — should I try medically supervised hcg injections?", "intent_class": "recommendation", "derived_from": "primary" },
      { "prompt": "is a doctor-supervised hcg program worth the money?", "intent_class": "recommendation", "derived_from": "fanout:cost" },
      { "prompt": "how much weight can you actually lose on the hcg diet?", "intent_class": "factual", "derived_from": "fanout:outcomes" },
      { "prompt": "what do you eat on the hcg diet — is it really only 500 calories?", "intent_class": "factual", "derived_from": "fanout:process_diet" },
      { "prompt": "how much does the hcg diet cost at a medical weight loss clinic?", "intent_class": "factual", "derived_from": "fanout:cost" },
      { "prompt": "is hcg safe for weight loss and is it FDA approved?", "intent_class": "factual", "derived_from": "fanout:risk_safety" },
      { "prompt": "how long does a round of the hcg diet last?", "intent_class": "factual", "derived_from": "fanout:duration_timeline" },
      { "prompt": "is Dr. Hartwell's Example Weight Loss Clinics legit?", "intent_class": "brand", "derived_from": "brand" },
      { "prompt": "Dr. Hartwell rapid weight loss reviews hcg program", "intent_class": "brand", "derived_from": "brand" }
    ],
    "engines_recommended": ["google_ai_mode", "chatgpt", "perplexity"],
    "measurement_window_days": 28,
    "kpis": ["domain_cited", "brand_named", "winning_competitor"]
  },
  "spec_feedback": [
    {
      "anchor": "Severity guide — 'off-topic sections' listed as CRITICAL",
      "observation": "The Members Area block is a 45-word off-topic interstitial; CRITICAL severity (applied per the guide) reads heavy next to the page's genuine compliance CRITICALs, though the verdict in findings[] follows the guide.",
      "suggested_spec_change": "Consider scaling OFF_TOPIC_SECTION severity by section word count (e.g. IMPORTANT below 100 words) so tiny drift blocks don't dilute the CRITICAL tier."
    }
  ]
}
```
