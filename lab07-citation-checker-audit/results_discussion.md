# Results and discussion outline — Prompt 14 — 2026-11-17

This is the reasoning behind the Results and Discussion sections of the paper. For each research question it separates what was directly observed from what might explain it and what can't be claimed. Numbers come from `results/phase4/`. See `evaluation_report.md` for the file map.

## RQ1 — Does metadata checking catch more errors than a DOI lookup?

**Observed.** Yes, by a wide margin and on both held-out sets. B1 catches only the synthetic DOIs that don't resolve (macro recall 0.20). B2 catches all five constructed error types (1.00). The preregistered rule (+0.10 recall, ≤ +0.05 FPR) is met. H1 is supported as stated.

**Why, and why that's less impressive than it sounds.** Four of the five error types leave the DOI pointing at a real, registered work. A registration check can't see them by design. B2 compares exactly the fields the mutations change, against the very records the mutations were made from. Any field comparison would score perfectly here. The zero-width bootstrap intervals say the same thing: all 40 random works behave identically.

**Not claimed.** That metadata checking catches 100% of real citation errors. That B2 is a good verifier. Anything about how often LLMs fabricate. The 12.5% of cases without a DOI were abstentions for every method, and none of the checkers helps there at all.

## RQ2 — Where do the checkers fail, and what do the misses and false flags look like?

**Observed, constructed errors.** B1 misses wrong-year, wrong-author, wrong-DOI and Frankenstein citations, every time, in every split. This is the contract working as designed: a resolving DOI only proves that *something* exists at that address.

**Observed, legitimate variants (amendment A1.3).** This is where the study finds something useful. B2 flags 47 of 87 legitimate variants (54%). Every one of those flags traces back to a single field rule:

| Variant | B2 false flags | Field that fired | What's going on |
|---|---|---|---|
| "et al." (first author only) | 30 / 30 | authors | Jaccard of 1 cited name vs n real names is 1/n, so it's at most 0.5 and never reaches 0.8 |
| Abbreviated venue | 11 / 11 | venue | Exact match after normalization can't equate "Polym. Chem." with "Polymer Chemistry" |
| Subtitle dropped | 5 / 6 | title | Character similarity falls to 0.40–0.86 when a long subtitle is missing; the one pass had ratio 0.90 |
| Print-year drift | 1 / 1 | year | The *Nursing Open* article was online in 2022 and in print in 2023 |
| Hyphenation break | 0 / 39 | — | Normalization plus ≥ 0.90 similarity absorbs "classi- fication" |

Several of the venue cases are also registry quirks, not citation mistakes. Crossref stores "Psychology &amp; Marketing" (an un-decoded HTML entity) and "Zeitschrift f�r Physik" (a replacement character), so a perfectly normal citation can't match them exactly. One 1975 article carries an online date of 2009, presumably from later digitisation. B2 compares against the earliest date, so it happens to be safe there, but it shows how slippery "the year" of a paper is.

**Possible mechanism.** These are exactly the kinds of false-positive causes Russinovich et al. describe qualitatively for their own tool (drift, editors and parsing artifacts, and so on; see `gap_matrix.md`). The contribution here is a count, on a controlled set, of how often a simple field matcher trips over them.

**Field ablation (`ablation.csv`).** No single field reaches full recall. Two categories are caught by every variant: synthetic DOIs don't resolve, and a wrong DOI points at a different paper whose title, authors, year and venue all differ from the citation. Beyond those, each field earns exactly one category: title catches Frankenstein, year catches wrong-year and authors catch wrong-author (0.60 macro recall each). The venue check catches nothing the other three don't already catch: dropping it keeps recall at 1.00 and cuts false flags from 54% to 41%. That last result needs care. There is no "wrong venue" mutation category, so the design gives the venue check nothing to do. The fair reading is "the venue check costs 11 false flags and, *in this design*, buys nothing", not "venue checks are useless".

**Threshold sensitivity (`sensitivity.csv`).** Lowering the title threshold barely helps (54% → 51% at 0.50). The subtitle cases sit well below any sensible threshold, and the venue and author flags don't depend on it. Lowering the author Jaccard threshold to 0.20 brings false flags down to 30%, but long author lists still fail, because 1/17 is below any threshold that would still catch a wrong author list. Recall stays at 1.00 across the whole grid, which again says more about how easy the mutations are than about robustness. The frozen operating point was not changed.

## RQ3 — Does the error definition change the picture?

**Observed.** Under identity-only labels, wrong-year and wrong-DOI citations count as valid. B2's flags on them become false positives: precision falls from 1.00 to 0.60 and FPR rises from 0.00 to 0.40, on both test and ext. B1's recall rises from 0.20 to 0.33, simply because there are fewer positives.

**Interpretation.** Nothing about the checkers changed. Only the definition did. The same predictions look like a near-perfect verifier under one definition and a noisy one under another. This matches the denominator and definition argument in the Lab06 review and in Russinovich et al. (who count venue/year drift as *not* hallucination). Any comparison of checkers needs to say which definition it uses.

## H3 — Does the containment author rule help?

**Supported.** B3 removes all 30 "et al." false flags (stress false-flag rate 54% → 19.5%; paired bootstrap difference −0.39 to −0.29) and keeps recall at 1.00 on every error category. It still flags a citation that names someone who isn't an author, and an empty author list.

**Caveat.** B3 would also pass a citation that drops *real* co-authors in a misleading way, for example listing only the third author. Whether that is an "error" is a definition question again. And a containment rule can't catch an error where the cited author is a real co-author of a *different* paper with the same DOI. That case doesn't exist in our design.

## Limitations to state plainly in the paper

- Constructed errors, not natural LLM output. Nothing here estimates fabrication prevalence.
- Labels and lookups share one registry. Recall on the error categories is close to guaranteed.
- 40 random journal articles is still small. Print-year drift has n = 1 and subtitle-dropping n = 6, so treat those rows as anecdotes.
- There is no wrong-venue mutation, so the ablation can't credit the venue check with anything.
- Only Crossref, only journal articles, no conference papers, books or preprints. Non-English titles were included only as far as the random sample happened to contain them.
- Simple teaching controls, not RefChecker or CiteCheck. Nothing here says how those tools would behave.
- The original Phase III pilot and test DOIs were a hand-picked convenience list. That's partly why the random extension set was added.

## Three follow-ups, ranked by information per unit of effort

1. **Add wrong-venue and partial-author-error mutations** (cheap: one function, no new data). This would tell us whether the venue check and the containment rule earn their place.
2. **Normalize venues through Crossref's own short titles and decode HTML entities before matching** (cheap). This is a direct test of how many of the 11 venue false flags are fixable, but it has to be frozen before scoring, like B3 was.
3. **Score a small, hand-labelled set of real LLM-generated references** (the optional GPU extension in `gap_matrix.md`). Expensive, but it's the only way to learn whether any of this matters for natural errors.
