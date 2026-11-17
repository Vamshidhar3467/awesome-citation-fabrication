# AI Assistance Log — Lab 07

| # | Date | Tool / model | Task | Prompt | AI output | Human decision | Verification |
|---|---|---|---|---|---|---|---|
| 1 | 2026-10-21 | Claude Code, Claude Opus 5.5 | Prompt 01: workspace setup and review scope | Lab 07 sheet Prompt 01, with Benchmarking Citation Fabrication Rates Across Large Language Models and Agentic Search Tools = T21 title; review supplied = Lab 06 `main.tex` | Scope summary and first entry in `research_decisions.md` |Pretty much, yes. The sections, their order and the content all line up with the paper. The only slips are that Table 2 actually sits in Section 6.1 rather than Section 5, and the summary leaves out 4.3 and the Goddard/Emsley commentary. | Compare the summary against `main.tex` |
| 2 | 2026-10-21 | Claude Code, Claude Opus 5.5 | Prompt 02: gap extraction | Lab 07 sheet Prompt 02, applied to the same review | `gap_matrix.md`: 5 gaps, top-3 ranking, verification checklist | Student chose G2 (2026-10-22); see Entry 5 | I checked Russinovich et al., Bhattacharyya et al., Walters & Wilder, Rao et al. (Entries 3–4) |
| 3 | 2026-10-22 | Claude Code, Claude Opus 5.5 | Update gap matrix with the student's checks of original papers | Student's summaries of Russinovich et al., Bhattacharyya et al., Walters & Wilder, Rao et al. | Updated labels in `gap_matrix.md`; Entry 3 in `research_decisions.md` | I read the four original papers. AI did not verify them independently. | I found that the review's sec 6.3 misattributes prompt-wording sensitivity to Bhattacharyya et al. |
| 4 | 2026-10-22 | Claude Code, Claude Opus 5.5 | Record G2 novelty check | My own reading of Russinovich et al. (text only; Fig. 8 values not visible) | Updated G2 and Part 4 in `gap_matrix.md`; Entry 4 | I read the paper text personally; Fig. 8 values were not visible in the version read | VERIFIED by student (text); not verified by AI |
| 5 | 2026-10-22 | Claude Code, Claude Opus 5.5 | Record evaluation section and Fig. 8 of Russinovich et al. | Student pasted the evaluation text and a screenshot of Fig. 8 | Fig. 8 values read approximately from the chart; updated `gap_matrix.md` and Entry 6 | Student read the paper and figure personally | VERIFIED by student; AI read approximate values from the student's screenshot |

## Continuation — 2026-10-30 — Codex

Exact backend model version is not exposed; no model identifier is invented. Historical model labels above are preserved as supplied, not independently authenticated. User prompt: continue the Lab07 assignment from Prompt 02 through Phase III autonomously; user clarified no strict 60% allocation and supplied local paths. Numbered assignment prompts were adapted to local execution; no claim that the student manually submitted each prompt.

| # | Task / adapted prompt | AI output or code change | Human decision | Actual verification / outcome |
|---|---|---|---|---|
| 6 | Read assignment and prior files | Phase III scope = Prompts 08–11; map remaining 03–11 deliverables | Autonomous continuation explicitly requested | PDF extracted using pypdf; Lab06 review and bibliography read |
| 7 | Prompts 03–05: mapping, search, question | Literature map, novelty/feasibility record, brief; narrow general G2 novelty due to CiteCheck | Individual wording/design acceptance pending | Primary paper/repository pages consulted; no systematic novelty claim |
| 8 | Prompts 06–07: data/comparators/protocol | Fixed source list, source-group split, mutation labels, B1/B2 specification, frozen JSON config | Agent implementation choice under broad user instruction | Protocol saved before dataset acquisition/pilot measurement; hashes in manifest |
| 9 | Prompt 08: environment | Standard-library Python baseline; cached API probe | No GPU install needed | Actual Python 3.14.6/system/nvidia-smi and Crossref output saved |
| 10 | Prompt 09: module cycles | Data/cache, corruption, validation, DOI-only predictor, comparator scaffold, metrics, plots | Student code comprehension remains pending | Real acquisition of 12 records; 32-case pilot, CSV/JSON/SVG outputs |
| 11 | Prompt 10: audit baseline | Baseline validation with explicit adaptations and limitations | No instructor sign-off invented | Ten tests; true subprocess exit-code logs; identical offline rerun hashes |
| 12 | Prompt 11: real debugging/verification | Replaced unavailable pymupdf with pypdf for PDF reading; fixed misleading PowerShell test logging using Python capture; added schema/hash checks | Agent performed fixes; no student correction invented | Actual extraction succeeded; final tests exit 0; pilot regenerated and hashes checked |
| 13 | Phase III handoff | README, code explanations, notebook with real subprocess outputs and phase coverage map | Personal source/code checks still pending | scripts/make_walkthrough.py executed; no held-out evaluation or publication |

All code in src/scripts/tests was AI-generated in this continuation and checked by agent execution. Source facts were fetched from Crossref; mutations were deliberately generated and labelled, not passed off as natural LLM outputs. No claim of a particular human/AI percentage, student reading, approval or personal reflection is manufactured. Earlier real student decisions remain in Entries 1–6. Remaining risks: small synthetic convenience sample, same-registry circularity, incomplete independent ground truth and limited comparator testing.

## Continuation — 2026-11-17 — Claude Code (Claude Opus 5.5)

User prompt (paraphrased): continue the LabQ7 assignment from Phase III and complete it fully, and make the generated reports read naturally. Numbered prompts 12–18 were carried out by the agent in local execution cycles. The student has not typed each prompt or reviewed the outputs yet. The full narrative is in `ai_audit.md`.

| # | Task / adapted prompt | AI output or code change | Human decision | Actual verification / outcome |
|---|---|---|---|---|
| 14 | Prompt 12: contribution pathway | `contribution_plan.md`: Pathway B plus one isolated change (B3); amendment A1 (random extension set, legitimate-variant stress cases, ablation, sensitivity, clustered bootstrap), written before any held-out output | Covered by "complete the work"; content review pending | Frozen file hashes and the order of logs confirm nothing held-out existed when it was written |
| 15 | Library refactor + B3 | `build_variants`, `field_checks`, `build_stress_cases`, `METHODS`; B1/B2 behaviour unchanged | — | Rebuilt `cases.json` byte-identical to Phase III; the 10 old tests pass |
| 16 | Extension data | `scripts/acquire_ext.py`; 100 sampled, 91 eligible, 40 frozen; 320 + 87 cases | — | **Bug:** `eligible()` returned a string, giving a TypeError before anything was saved; fixed with `bool()`. Snapshot SHA-256 `7eb0b029…` |
| 17 | Tests | `tests/test_phase4.py`, 7 tests | — | **Wrong expectation in an AI-written test** (longest word); test fixed, code unchanged; 17/17 pass |
| 18 | Prompt 13: evaluation | `scripts/evaluate.py`; pilot-only development run, then one held-out run | — | First held-out attempt stopped (uncached test synthetic DOIs; nothing written); 8 real 404s cached, then a single full run. `verify.py` regenerates all outputs byte-identically |
| 19 | Figures | `scripts/make_figures.py` | — | Palette validated; PNGs inspected; label collisions fixed |
| 20 | Prompt 14: interpretation | `evaluation_report.md`, `results_discussion.md` | — | Numbers cross-checked against files; row-count error (1,413 → 1,509) and a vague ablation sentence corrected |
| 21 | Prompt 15: manuscript | `paper/main.tex`, `references.bib`, `main.pdf` (9 pp.) | — | All 9 references checked live against arXiv/Crossref; three overclaims found by checking against data and corrected |
| 22 | Prompt 16: peer review | `peer_review.md` (4 major, 6 minor) and revision log | — | Revisions applied and recompiled; no numbers changed; pre-review PDF kept |
| 23 | Prompt 17: repository docs | README with reproduction checklist, data/paper READMEs, requirements | — | Unrun commands marked [TEST REQUIRED] |
| 24 | Prompt 18: AI audit | `ai_audit.md`, `demo_walkthrough.md` | — | Lists only events that appear in logs or in this session |
| 25 | Repository publication and full recheck (user requests) | Pushed to the existing GitHub repo as a subfolder; corrected root README (missing file link, Lab 1 score 97.5% to 95.0%), replaced the outdated Lab 06 paper; added Phase IV code notes, an executed results notebook and `scripts/check_paper_numbers.py` | User asked for the push and for items 1-9 | **Error found by recomputation:** the paper said the sample's median year was 2012; it is 2010. Fixed; all 32 paper numbers now checked automatically in `verify.py` |

Pushes to GitHub were made at the user's request. Nothing was submitted or approved on the student's behalf. Pending student entry: personal review of Phase IV–VI outputs and decisions.
