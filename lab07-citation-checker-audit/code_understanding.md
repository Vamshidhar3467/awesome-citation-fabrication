# Code understanding and prompt-to-code record — Prompts 08–11, plus Phase IV

*Phase III (below) explains the baseline. The [Phase IV section](#phase-iv-additions--2026-11-17) at the end explains the extension data, B3, the evaluation script and the deeper analyses.*

The user authorized autonomous continuation from Prompt 02 through Phase III. These are adapted execution cycles, not a claim that the student typed every numbered prompt. The agent executes locally and records actual outputs in place of repeatedly asking the student to paste them.

| Cycle | Specification / assumptions | Code and I/O | Check and explanation |
|---|---|---|---|
| Environment | CPU-only, no model training, public bibliographic facts | `run.py environment`: JSON system/runtime plus a real API lookup | `environment.json` and `environment.log`; no dependency compatibility assumed from a suggested version |
| Acquisition | Fixed DOI sources, cache facts only; 404 distinguished from outages | `fetch_record`: DOI string -> fact dictionary; records -> sources JSON | API success and cached 404s are real; exceptions stop a run |
| Partition / mutation | Assign original works before constructing rows; keep donors inside split | `build_cases`: list of source dictionaries -> eight case dictionaries per source | Split/unit checks reject overlap, duplicate IDs and malformed label types |
| Preprocessing | Normalize DOI prefixes/case, Unicode case/accents and punctuation | `doi_key`, `normalize`: string -> string | Tests exercise URL/case and accented author names |
| Baseline | A registered DOI establishes a registry match only | `predict`: observed citation + lookup callable -> decision/reason | Wrong author intentionally passes B1; test establishes this limitation, not desired comprehensive checking |
| Evaluation / saving | Labels only enter scorer; abstention coverage explicitly reported | `metrics`: prediction rows -> counts/ratios; `run.py pilot` saves CSV/JSON/SVG | Hand-calculated confusion fixture checks denominators; source-group validation and frozen-file hashes precede execution |
| Comparator scaffold | DOI-anchored field checks with frozen thresholds | `predict(..., method='metadata_check')` | Unit check only. No Phase IV comparison or held-out result claimed |

## Explain the data flow

A clean source is a dictionary of DOI, title, authors (surname strings), year (integer), venue, provenance and retrieval timestamp. A case adds `id`, `source_id`, `donor_id`, `split`, `category`, `citation` and labels. The predictor receives only `citation`, never `source_id` or labels. Cached metadata is a permitted external reference catalogue; the mutation ledger is hidden ground truth. The output contains one decision and reason per pilot case. Missing DOI returns abstain without making a request.

Precision = correct flags / all flags. Recall = detected positives / all positives. FPR = false flags / all valid cases. Coverage = non-abstentions / all cases. Undefined ratios become JSON null. F1 uses the same all-positive recall denominator. These are error-detection metrics, not citation-generation fabrication rates. No training step exists because neither baseline is learned.

## Authentic debugging record — Prompt 11

1. PDF extraction initially failed: `ModuleNotFoundError: No module named 'pymupdf'`. Small correction: install/use `pypdf` for assignment inspection. It is not a baseline dependency. Verification: all assignment text was extracted, including Phase III Prompts 08–11. No metrics were affected.
2. Initial test command emitted unittest progress on stderr; Windows PowerShell rendered this as `NativeCommandError` and reported an outer failure even though eight tests said OK. Correction: `scripts/verify.py` captures stdout/stderr with Python subprocess and records the actual child exit code. Inspect `results/tests.log`. This changes logging, not baseline predictions. Final tests were expanded to ten to cover schema/leakage and undefined metrics.
3. During code audit, a validation gap was found before final verification: the runner did not enforce case schema or frozen input hashes. Added `validate_cases` and protocol/case hash checks; tests cover duplicate IDs and crossing source groups. These checks protect execution against input drift. Pilot was rerun afterward; repeat-output hashes are recorded.

No algorithmic bug, performance gain or student intervention is invented. The metadata comparator has only a minimal sanity test; full validation is required before research claims about it.

## Student viva / ownership checks (still personal work)

Explain why wrong-author cases pass DOI-only; why missing DOI is not fabrication; why a 404 is inconclusive; how the source split prevents leakage between related variants; how false positives and recall denominators are computed; why a synthetic pilot cannot estimate real LLM fabrication rates. Read a case, its cached record, prediction and scorer output end to end. These questions are preparation, not a claim that you have already answered them.

## Phase IV additions — 2026-11-17

Same honesty rule as above: this code was written by the agent (Claude Code) and checked by execution. You still need to read it yourself. Each row says what goes in, what comes out, and how you'd know it works.

| Piece | Input → output | What it's for | How it was checked |
|---|---|---|---|
| `build_variants(group, split)` in `src/citationlab.py` | list of source records → 8 case dicts per record | The Phase III mutation code, pulled out so the extension set reuses it exactly | Rebuilt `data/cases.json` byte-identical to the Phase III file |
| `build_stress_cases(record, extras, i)` | one record + snapshot extras → 0–5 *valid* cases | Legitimate variants: "et al.", dropped subtitle, Crossref short venue, print year, hyphen break. Skips any variant the record can't support | `test_stress_cases_are_valid_and_applicability_respected` |
| `field_checks(citation, record, config)` | citation + registry record → `{title, authors, year, venue}` booleans | One place where every field rule lives; `author_rule` switches between Jaccard (B2) and containment (B3) | B2 outputs unchanged on pilot; `test_b3_accepts_et_al_but_rejects_foreign_author` |
| `predict(..., method, config)` | citation + lookup → decision + reason | Now names the failed field(s), e.g. `metadata_mismatch:authors`; `config['fields']` restricts which fields count (ablation) | `test_reason_lists_every_failed_field`, `test_field_ablation_ignores_unselected_fields` |
| `validate_cases` (changed) | all cases → error or nothing | Now accepts any split name; `ext` and `ext_stress` may share works (same prefix), every other pair must be disjoint | `test_ext_and_stress_share_sources_without_leakage_error` |
| `scripts/acquire_ext.py` | Crossref sample (online once) → snapshot, 320 + 87 cases, manifest | Draws and freezes the random 40 works; `--offline` rebuilds from the snapshot | Snapshot hash; offline rebuild matches; `verify.py` |
| `scripts/evaluate.py` | frozen cases + cache → `results/phase4/*` | Checks hashes, runs B1–B3, checks ID/label alignment, then scores, ablates, sweeps thresholds and bootstraps | Pilot-only run first; then one held-out run; `verify.py` regenerates identically |
| `score(rows, definition)` | prediction rows → overall + per-category metrics + macro recall | Same predictions under any-error or identity-only labels (RQ3) | `test_macro_recall_is_mean_of_category_recalls` |
| `bootstrap(...)` | predictions grouped by source work → 95% intervals | Resamples whole works, never rows, because one work's eight variants aren't independent | Seeded (20261117); intervals stable across reruns |
| `scripts/make_figures.py` | result files → three PDF/PNG figures | Paper figures; never reads raw cases, only results | Each PNG opened and inspected |

### Explain it in your own words (viva practice)

- **Why does "et al." always fail B2?** Citing 1 of *n* authors gives a Jaccard of 1/*n*. For *n* ≥ 2 that's at most 0.5, below the 0.8 threshold.
- **Why does B3 still catch wrong authors?** The fake author `SyntheticWrongAuthor` isn't in the registry list, so the cited set isn't contained in the real one.
- **Why is the stress set scored separately?** Every stress case is valid. Mixing them into the preregistered metrics would change the frozen comparison after the fact.
- **What would break if a label leaked into `predict`?** Nothing would crash. The scores would just become meaningless, which is why `predict` takes only the citation and a lookup function, and `check_alignment` only compares labels after prediction.
- **Why can't the extension set be regenerated online?** The Crossref `sample` endpoint is random. The snapshot file is the dataset.
