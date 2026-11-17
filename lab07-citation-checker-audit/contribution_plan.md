# Contribution plan and protocol amendment A1 — Prompt 12

*Written 2026-11-17, before any held-out prediction existed. At the time of writing, the only outputs anyone had seen were the 32 pilot rows from Phase III. The `results/` folder held no test or extension predictions.*

## Where the baseline left us

The DOI-only control (B1) did what its contract says, no more and no less. On the pilot it flagged the four synthetic DOIs that Crossref doesn't know about and let every other mutated citation through. Wrong year, wrong author list, a DOI borrowed from another paper, a title spliced onto someone else's metadata: all passed. That isn't a bug. It's the point of the control. A DOI that resolves tells you a work exists, not that the citation describes it.

The obvious next step is B2, which already sits in the code. It uses the same DOI lookup but also compares title, authors, year and venue. Here's the uncomfortable part. Our labels come from mutating Crossref records, and B2 checks citations against those same Crossref records. So B2 is close to guaranteed to catch every frozen mutation. If the paper stopped at "B2 beats B1 on the frozen categories", it would mostly be reporting the design of the dataset back to itself.

The more useful question comes from the Russinovich et al. reading recorded in `gap_matrix.md` (G2, student-verified 2026-10-22). Their checker's flags needed human review because many were false positives, caused by things like venue/year drift, an editor listed as a co-author or PDF extraction glitches. They describe those causes but never measure them. A field-matching checker has exactly this weakness: real citations are routinely written differently from the registry record without being wrong.

## Three pathways considered

| Pathway | Scientific question | Code change | Risk | Decision |
|---|---|---|---|---|
| A. Reproduce RefChecker under a new condition | Does the published multi-database tool show the same blind spots? | Separate environment, several external services, PDF parsing | High. Many moving parts and no pinned behaviour to compare against in the time left | Not chosen. Recorded as future work |
| B. Controlled comparison of B1 and B2, extended with benign-variation stress cases | What does metadata checking buy in recall, and what does it cost in false flags on legitimate citations? | New evaluation script, stress-case builder, source-clustered bootstrap. No change to B1 or B2 | Small dataset; synthetic positives | **Chosen (primary)** |
| C. One isolated modification of B2 | Can a single principled change to the author rule reduce benign false flags without losing recall? | One new author rule (B3). Everything else identical to B2 | Could look like tuning if the rule were chosen after looking at results | **Chosen (secondary)**, rule fixed below before any held-out run |

## Amendment A1 (logged 2026-11-17, before held-out outputs were generated)

**Why amend.** The frozen protocol already said that eight held-out source works are too few for any interval estimate and that the source count should be scaled "under an explicitly logged amendment before evaluating it". This is that amendment. The original preregistered comparison stays exactly as it was and is reported first.

**A1.1 — Primary comparison unchanged.** B1 and B2 run on the original 64 held-out cases (`split = test`) with the frozen thresholds (title ≥ 0.90, author Jaccard ≥ 0.80, exact year, exact normalized venue). Decision rule as frozen: B2 macro recall ≥ B1 + 0.10, with an FPR increase of ≤ 0.05.

**A1.2 — Extension set E.** Draw one random sample of journal articles from the Crossref `sample` endpoint (`/works?sample=100&filter=type:journal-article`). Keep records with a title of at least three words, at least one named author, a publication year and a container title. Exclude the 12 original DOIs. Sort the eligible DOIs, take the first 40 and freeze the snapshot with its retrieval timestamp and SHA-256. Each of the 40 DOIs then goes through the same `fetch_record` lookup as everything else, so B1–B3 see exactly the registry view used in Phase III. The eight frozen mutation categories are built inside E with E-only donors. This gives 320 cases, all held-out. The sample can't be redrawn identically from the API, so the saved snapshot is the frozen artifact. Random sampling replaces the earlier hand-picked DOI list, which was one of the threats listed in the protocol.

**A1.3 — Benign stress cases (new, all labelled valid).** For each E record, generate these legitimate variants where the record allows it:

| Stress category | What changes | Applicable when | Real-world mechanism it imitates |
|---|---|---|---|
| `et_al_first_author` | Author list cut to the first author only | ≥ 2 authors | "Smith et al." style references |
| `subtitle_dropped` | Title cut at the first colon | Colon present, and ≥ 3 words before it | Short-title citation habits |
| `venue_abbrev` | Venue replaced by Crossref's own `short-container-title` | Short title exists and differs after normalization | Abbreviated journal names (ISO4-style) |
| `print_year` | Year replaced by the `published-print` year | Print year exists and differs from the year B2 checks against | Online-first vs print drift. Russinovich et al. count this kind of drift as *not* a hallucination |
| `title_hyphen_break` | Longest title word (≥ 8 letters) split as `"classi- fication"` | Such a word exists | PDF line-break extraction artifact |

These are reported as a separate stress analysis. They are **not** folded into the preregistered any-error metrics. Their only purpose is to measure false-flag rates on legitimate variation.

**A1.4 — B3, the single modification.** B3 is identical to B2 except for the author rule. B2 requires Jaccard(cited surnames, registry surnames) ≥ 0.80. B3 instead requires that every cited surname appears among the registry surnames (non-empty containment). The rationale is about citation practice, not our data: a citation that lists fewer authors than the paper has ("et al.") is incomplete, not wrong, while a citation naming someone who isn't an author is wrong. Hypothesis H3: B3 removes the `et_al_first_author` false flags without losing recall on the five error categories. A contrary observation would be any recall drop on `wrong_author` or `frankenstein`.

**A1.5 — Deeper analyses.**
1. *Error-type breakdown.* Per-category recall, false flags and coverage for B1, B2 and B3 on test and E. This was already preregistered.
2. *Label-definition rescoring (RQ3).* The same predictions rescored under identity-only labels. Preregistered.
3. *Field ablation.* B2 restricted to a single field (title, authors, year or venue only) and B2 with each field left out, on E plus the stress cases. This shows which check catches which error and which check causes which false flag.
4. *Threshold sensitivity.* Title thresholds 0.50–1.00 and author thresholds 0.20–1.00, scored on E plus the stress cases. Descriptive only. The frozen operating point does **not** move, whatever the curves show.
5. *Uncertainty.* Source-clustered percentile bootstrap (2,000 resamples, seed 20261117) for macro recall, FPR and their paired B2−B1 and B3−B2 differences. Whole source works are resampled, never individual mutated rows. Intervals on the eight-source test split are reported but flagged as unreliable.

**A1.6 — Order of work.** Run B2 and B3 on the 32 pilot cases first to check the code paths (development data, already seen). Then run every held-out evaluation once. If a bug turns up after held-out outputs exist, the fix and the rerun get a dated entry here, not a silent overwrite.

**A1.7 — Budget.** Roughly 100 Crossref requests (one sample query, 40 lookups, 40 synthetic-DOI 404 checks, 8 test synthetic DOIs), serial with the existing back-off. This supersedes the "fewer than 25 calls" estimate in protocol v1.0, which only covered Phase III.

## What this can and can't show

It can show which kinds of citation error each control catches, what metadata checking costs in false flags on realistic legitimate variation, and whether one principled rule change helps. It can't say anything about how often language models actually fabricate citations. It isn't a reproduction of RefChecker or CiteCheck. And the circularity remains: labels and lookups share one registry, which flatters every checker on the mutation categories. The stress set is partly a response to that, because there the registry record is held fixed while the citation legitimately differs from it.
