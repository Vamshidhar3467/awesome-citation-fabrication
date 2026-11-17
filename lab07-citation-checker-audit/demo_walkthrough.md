# Five-minute demo and viva prep

A suggested running order for the code-and-results walkthrough, then the questions you're most likely to get and the honest answers. Practise it once yourself. The point of the viva is that *you* can explain it.

## The five minutes

**0:00 — The question (30 s).** "Citation checkers usually ask whether a DOI resolves. I wanted to know what that misses, and what a stricter checker costs in false alarms on citations that are actually fine."

**0:30 — Show it runs (60 s).** In PowerShell, from the project folder:

```powershell
python scripts/verify.py
```

Point at the `PASS` lines, then at `"phase4_regenerated_identical": true`: every result file was regenerated from frozen inputs and matched byte for byte. Mention it's offline and CPU-only.

**1:30 — One case end to end (90 s).** Open `results/phase4/predictions.csv` and filter for an "et al." row, e.g. `extstress-000-et_al_first_author`. B1 passes it (`doi_registered`), B2 flags it (`metadata_mismatch:authors`) and B3 passes it. Then open the same ID in `data/ext_cases.json` to show the citation has only the first author. Explain that one name against *n* real authors gives a Jaccard of 1/*n*, which is never ≥ 0.8.

**3:00 — The results (90 s).** Open the paper at Fig. 2. Left panel: B1 only catches fake DOIs, while B2/B3 catch everything, "but that's by construction." Right panel: B2 wrongly flags 47 of 87 legitimate citations, and B3's single rule change removes the 30 et-al flags. Then Table 2's last rows: the same predictions drop from precision 1.00 to 0.60 just by changing what counts as an error.

**4:30 — Limits (30 s).** "The errors are constructed, labels and lookups share Crossref, and the B3 fix was designed alongside the test it passes. So this shows mechanisms, not real-world rates."

## Likely viva questions

**Why is 100% recall for B2 not impressive?** The mutations change exactly the fields B2 compares, against the same Crossref records the mutations were built from. Any field comparison would score perfectly. The bootstrap intervals have zero width for the same reason: every work behaves identically.

**Why does a wrong-author citation pass B1?** B1 only checks that the DOI resolves. The DOI is real, so it passes, whatever the authors say.

**Why is a missing DOI an abstention, not a flag?** Lots of correct citations have no DOI. Flagging them would call valid references fabricated. Abstentions count as misses in recall and are reported as coverage (0.875).

**Why is a Crossref 404 not proof of fabrication?** Crossref isn't every registry. A real work can be registered elsewhere or not indexed yet. A flag means "unresolved here".

**What's leakage here, and how did you prevent it?** Variants of one work must never sit in two splits, and donors must come from the same split. `validate_cases` enforces both. The checker gets only the citation, never the label, category or source ID. Thresholds were frozen before any held-out run, and the B3 rule was written down before it too.

**Why resample source works in the bootstrap, not rows?** The eight variants of one work aren't independent. Resampling rows would pretend there's eight times more evidence than there is.

**Isn't B3's improvement cherry-picked?** Partly by construction, yes. The et-al variant and the containment rule were designed together, and the paper says so. What's informative is that B3 lost no recall elsewhere, but there's no partial-author error category, so even that is weakly tested.

**Why doesn't the venue check catch anything?** No mutation corrupts only the venue, so it had nothing to find. It still caused 11 false flags. That's a gap in the design, not proof that venue checks are useless.

**What did the AI do, and what did you do?** Be specific and honest, using `ai_audit.md`. Mention at least one bug the AI introduced and how it was caught (the `eligible()` string-instead-of-boolean crash is a good one).

**What would you do next?** Add wrong-venue and partial-author mutations. Normalise venues with Crossref short titles and HTML-entity decoding, frozen before scoring. Then score a small hand-labelled set of real LLM-generated references.
