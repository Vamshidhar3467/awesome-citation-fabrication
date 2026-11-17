# Evaluation on real outputs — Prompt 13 — 2026-11-17

Everything below was produced by `scripts/evaluate.py`, run offline against the frozen cases and the Crossref lookup cache. The run log is `results/phase4/evaluate.log`. If a number in the paper doesn't appear in one of the files listed at the end, it shouldn't be in the paper.

## What happened, in order

1. **Extension set drawn** (`scripts/acquire_ext.py`, 09:36 UTC). Crossref's sample endpoint returned 100 journal articles and 91 passed the eligibility rules. The first 40 by DOI were frozen in `data/ext_snapshot.json` (SHA-256 `7eb0b029…`). The first attempt crashed before writing anything, because a helper returned a string where a boolean was expected. Fixed and rerun; see the debugging log in `ai_assistance_log.md`.
2. **Pilot development run** (`evaluate.py --pilot-only`). B1 reproduced the Phase III pilot numbers exactly (4 correct flags, 0 false flags, 4 abstentions). B2 and B3 flagged all 20 pilot mutations and passed all valid pilot cases. This only checked that the code paths behave as specified. The pilot had already been seen in Phase III.
3. **Seven new unit tests** for B3, field ablation, stress-case construction, the extended split check and macro recall. One test failed the first time because *my test expectation* was wrong ("characterisation" is longer than "Spectroscopic", so the code split the right word). All 17 tests now pass.
4. **First held-out attempt** stopped with `FileNotFoundError` before writing any output. Phase III had deliberately cached lookups only for pilot cases, so the eight synthetic test DOIs had never been queried. They were looked up (eight real 404s) and the evaluation ran once, start to finish.

## Checks made before any metric is computed

`check_alignment()` runs per method and stops the run if any of these fail:

- the number of predictions equals the number of cases, and there are no duplicate IDs;
- every prediction's label matches the case file by ID, under both label definitions;
- every decision is `pass`, `flag` or `abstain`, with a non-empty reason;
- stress cases are labelled valid and belong to a declared stress category.

Before that, `load_cases()` compares SHA-256 hashes of the frozen protocol, the Phase III cases, the snapshot and the extension cases against their manifests. `validate_cases()` then rejects duplicate IDs, sources that appear in two partitions, and donors from another partition. The predictor sees only the observed citation. Labels, categories and source IDs go to the scorer only.

**Metric direction.** Higher is better for recall, macro recall, precision, F1 and coverage. Lower is better for FPR and for the stress false-flag rate. Abstentions (missing DOI) count as misses in the recall denominator and as non-flags for FPR, and the coverage column shows how many there were.

## Headline results (from `results/phase4/results.csv`)

| Split | Method | Labels | n | TP | FP | Recall | Macro recall | FPR | Coverage |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| test (8 works) | B1 | any-error | 64 | 8 | 0 | 0.200 | 0.200 | 0.000 | 0.875 |
| test | B2 | any-error | 64 | 40 | 0 | 1.000 | 1.000 | 0.000 | 0.875 |
| test | B3 | any-error | 64 | 40 | 0 | 1.000 | 1.000 | 0.000 | 0.875 |
| ext (40 works) | B1 | any-error | 320 | 40 | 0 | 0.200 | 0.200 | 0.000 | 0.875 |
| ext | B2 | any-error | 320 | 200 | 0 | 1.000 | 1.000 | 0.000 | 0.875 |
| ext | B3 | any-error | 320 | 200 | 0 | 1.000 | 1.000 | 0.000 | 0.875 |
| ext | B2 | identity-only | 320 | 120 | 80 | 1.000 | 1.000 | 0.400 | 0.875 |
| ext_stress | B1 | valid only | 87 | – | 0 | – | – | 0.000 | – |
| ext_stress | B2 | valid only | 87 | – | 47 | – | – | **0.540** | – |
| ext_stress | B3 | valid only | 87 | – | 17 | – | – | **0.195** | – |

**Preregistered decision rule.** B2's macro recall exceeds B1's by 0.80 on test and on ext (threshold +0.10), and FPR on the preregistered valid cases rises by 0.00 (limit +0.05). So the rule is met on both held-out sets.

**Bootstrap** (`bootstrap.json`, 2,000 source-clustered resamples). The recall and FPR intervals all have zero width. Every source work behaves the same way on the mutation categories, so resampling sources changes nothing. That isn't precision. It shows how mechanical the mutations are. The one interval that carries information is the stress false-flag rate: B2 0.50–0.58, B3 0.13–0.25, paired B3−B2 difference −0.39 to −0.29.

**Run time** (`timing_us_per_case.json`). About 0.5–0.6 ms per case for all three methods, nearly all of it spent reading cached JSON. Every method makes exactly one registry lookup per citation that has a DOI, so the extra string comparisons in B2/B3 cost effectively nothing here. I haven't drawn any efficiency conclusion beyond that, since the cached setting doesn't represent live API latency.

## Leakage and fairness audit

- *Source leakage.* Test, pilot and ext source sets are disjoint (enforced in code). Stress cases reuse ext sources on purpose and are scored separately.
- *Tuning on test.* No threshold was changed. The sensitivity sweep is descriptive and its file marks the frozen operating point. B3's rule was written down in `contribution_plan.md` before any held-out output existed.
- *Comparator fairness.* All three methods share the same lookup function, cache and input fields. B2 and B3 differ in one line (`author_rule`).
- *Circularity, still present.* The mutations are built from Crossref records, and the checkers consult Crossref. This favours B2/B3 on the error categories and is the main reason the recall numbers above should be read as "the code does what it says", not "metadata checking catches 100% of citation errors".

## Output files

`results/phase4/predictions.csv` (one row per case × method: 503 cases including the pilot × 3 methods = 1,509 rows), `metrics.json`, `results.csv`, `ablation.csv`, `sensitivity.csv`, `bootstrap.json`, `timing_us_per_case.json`, `pilot_*` development outputs, `evaluate.log`, `acquire_ext*.log`. Figures are generated by `scripts/make_figures.py` into `paper/figures/` from these files only.
