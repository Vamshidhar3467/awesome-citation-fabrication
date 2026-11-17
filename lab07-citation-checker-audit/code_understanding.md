# Code understanding and prompt-to-code record — Prompts 08–11

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
