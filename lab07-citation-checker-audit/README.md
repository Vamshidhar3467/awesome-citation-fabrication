# What a Resolving DOI Doesn't Tell You

**An error-type audit of simple citation checkers.** Lab 07, AI Tools for Research. Bayyapu Vamshidhar Reddy (MRA2026010), IIIT Allahabad.

Tools that check reference lists for hallucinated citations usually start by asking whether the DOI resolves. This project measures what that question catches and what it misses. It also measures what happens when a checker goes further and compares the title, authors, year and venue against Crossref, including how often that makes it wrong about citations that are perfectly fine.

| | |
|---|---|
| **Paper** | [`paper/main.pdf`](paper/main.pdf) (LaTeX source `paper/main.tex`, bibliography `paper/references.bib`) |
| **Research question** | Which citation errors does a DOI check catch, what does field matching add, and what does field matching cost in false flags on legitimate citations? |
| **Pathway** | B, controlled comparison, plus one isolated modification (C) |
| **Headline** | DOI-only catches only non-existent DOIs (macro recall 0.20). Field matching catches every constructed error but false-flags 54% of 87 legitimate variants. Changing just the author rule to set containment cuts that to 19.5% with no recall loss |

## The study in one paragraph

Citations were built from Crossref records: 12 preregistered works (4 pilot, 8 held-out) and 40 randomly sampled journal articles added under a logged amendment. Each work gets eight variants: clean, re-formatted, DOI missing, wrong year, wrong authors, a borrowed DOI, a spliced title, and a fake DOI. The 40 random works also get up to five *legitimate* variants: "et al." author lists, abbreviated journal names, dropped subtitles, print-year differences and PDF hyphenation breaks. Three checkers are compared: **B1** (DOI resolves), **B2** (B1 plus title/author/year/venue matching) and **B3** (B2 with a containment author rule). The checkers see only the citation. Labels go to the scorer only. See [`experiment_protocol.md`](experiment_protocol.md) and [`contribution_plan.md`](contribution_plan.md).

## Reproduce everything (offline, CPU, about one minute)

Tested on Windows 11 with Python 3.14.6. The checkers need only the standard library. Figures need matplotlib.

```powershell
cd BayyapuVamshidharReddy_MRA2026010
python -m venv .venv; .\.venv\Scripts\Activate.ps1      # optional  [TEST REQUIRED: not run here]
pip install -r requirements.txt                          # figures only  [TEST REQUIRED: matplotlib was already installed]
python scripts/verify.py
```

`verify.py` runs the unit tests and the Phase III pilot (twice, checking that the outputs match), then rebuilds the extension cases, reruns the full evaluation and redraws the figures. It **fails if any reported result file changes by a single byte**. It writes logs to `results/*.log` and a summary to `results/verification.json`. This command was run successfully on 2026-11-17.

Individual steps, all offline against the cached Crossref facts:

| Step | Command | Writes |
|---|---|---|
| Unit tests (17) | `python -m unittest discover -s tests -v` | — |
| Rebuild preregistered cases | `python scripts/run.py acquire --offline` | `data/cases.json`, `data/manifest.json` |
| Phase III pilot (B1 only) | `python scripts/run.py pilot --offline` | `results/pilot_*` |
| Rebuild extension cases | `python scripts/acquire_ext.py --offline` | `data/ext_cases.json`, `data/ext_manifest.json` |
| Development check on pilot | `python scripts/evaluate.py --pilot-only` | `results/phase4/pilot_*` |
| Held-out evaluation | `python scripts/evaluate.py` | `results/phase4/*.csv/json` |
| Figures | `python scripts/make_figures.py` | `paper/figures/*.pdf/png` |
| Results notebook | `python scripts/make_phase4_notebook.py` (needs `nbformat`, `nbclient`, `ipykernel`) | `notebooks/phase4_results.ipynb` |
| Paper | `cd paper; latexmk -pdf main.tex` | `paper/main.pdf` (built with MiKTeX `pdflatex`/`bibtex`) |

**Online steps (not needed to reproduce; already run once).** `python scripts/run.py acquire` and `python scripts/acquire_ext.py` without `--offline` query the Crossref REST API. Don't rerun `acquire_ext.py` online with the snapshot deleted: Crossref's `sample` endpoint is random, so a new run draws a *different* 40 works, and the frozen hashes, and every number in the paper, would no longer apply. **[TEST REQUIRED]** A fresh online acquisition on another machine hasn't been tried. Crossref records can change over time, and the cache records retrieval timestamps for that reason.

## Where to find things

| Path | What it is |
|---|---|
| `src/citationlab.py` | Lookup and cache, case construction, legitimate-variant builder, the three checkers, metrics |
| `scripts/` | `run.py` (Phase III), `acquire_ext.py` (amendment A1 data), `evaluate.py` (all Phase IV results), `make_figures.py`, `verify.py`, `make_walkthrough.py` and `make_phase4_notebook.py` (notebooks) |
| `tests/` | `test_baseline.py` (10 Phase III tests) and `test_phase4.py` (7 tests for B3, ablation, stress cases, macro recall) |
| `configs/protocol.json` | Frozen v1.0 settings (seed, thresholds, DOI list). Never edited after freezing |
| `data/` | Crossref fact cache (`cache/`, one file per DOI, including real 404s), sources, case files, the random-sample snapshot and hash manifests. See [`data/README.md`](data/README.md) |
| `results/` | Phase III logs, pilot outputs and the original console captures (`results_*_console.txt`). `results/phase4/` holds every Phase IV prediction, metric, ablation, sensitivity and bootstrap file plus run logs |
| `paper/` | Manuscript, bibliography, figures, and the pre-review draft PDF for comparison |
| `notebooks/phase3_baseline.ipynb` | Phase III baseline walkthrough (captured script output) |
| `notebooks/phase4_results.ipynb` | Phase IV results walkthrough, executed with a real kernel: every table, the field that fired for each false flag, one case end to end, and the figures |

**Research record, in the order it happened:** [`research_decisions.md`](research_decisions.md) and [`gap_matrix.md`](gap_matrix.md) (Phases I–II), [`literature_to_experiment.md`](literature_to_experiment.md), [`novelty_feasibility.md`](novelty_feasibility.md), [`research_brief.md`](research_brief.md) (G1 brief), [`dataset_baseline_validation.md`](dataset_baseline_validation.md), [`experiment_protocol.md`](experiment_protocol.md), [`baseline_validation.md`](baseline_validation.md) (G2), [`code_understanding.md`](code_understanding.md), [`contribution_plan.md`](contribution_plan.md) (Prompt 12 and amendment A1), [`evaluation_report.md`](evaluation_report.md) (13), [`results_discussion.md`](results_discussion.md) (14), [`peer_review.md`](peer_review.md) (16), [`ai_audit.md`](ai_audit.md) and [`ai_assistance_log.md`](ai_assistance_log.md) (18), and [`demo_walkthrough.md`](demo_walkthrough.md) (five-minute demo).

## Compute and data use

CPU only. No GPU, model, training or paid API. The evaluation takes seconds. Crossref was queried 106 times in total (serially, cached, with back-off), and only bibliographic facts are stored: no abstracts or full text. Metadata comes from the [Crossref REST API](https://www.crossref.org/documentation/retrieve-metadata/rest-api/), used under Crossref's [metadata terms](https://www.crossref.org/documentation/retrieve-metadata/). No API keys, credentials or personal data are in the repository.

## Limitations, briefly

The errors are constructed, not taken from real model output, so nothing here estimates how often LLMs fabricate citations. Labels and lookups share one registry, which makes recall on the constructed errors close to guaranteed. The legitimate variants are derived from registry fields. B3's fix was designed alongside the variant it fixes. Samples are small (print-year drift has n = 1). The full list is in Section 7 of the paper.

## Credits, licence and citation

All code here is original to this project. No upstream code (RefChecker, CiteCheck or others) is copied or reproduced. AI assistance is disclosed in [`ai_audit.md`](ai_audit.md). This folder is part of the [awesome-citation-fabrication](../README.md) repository and is covered by its [CC BY 4.0 licence](../LICENSE). Crossref metadata in `data/` remains subject to Crossref's own terms.

If you refer to this work: Bayyapu Vamshidhar Reddy (2026). *What a Resolving DOI Doesn't Tell You: An Error-Type Audit of Simple Citation Checkers.* Course project, AI Tools for Research, IIIT Allahabad.

## Reproduction checklist for a second student

- [ ] Python ≥ 3.10 available (`python --version`). Install matplotlib if you want figures.
- [ ] `python scripts/verify.py` prints `"status": "PASS"` and `"phase4_regenerated_identical": true`.
- [ ] `results/tests.log` shows `Ran 17 tests … OK`.
- [ ] `results/phase4/results.csv` matches Table 2 of the paper. Its `ext_stress` rows give 0, 47 and 17 false flags.
- [ ] `results/phase4/metrics.json` → `ext_stress/B2` → `per_category` matches Table 3.
- [ ] Open one case in `data/ext_cases.json`, find its DOI's file in `data/cache/` (the name is the SHA-256 of the lower-cased DOI), and check the row for that ID in `results/phase4/predictions.csv`. The `reason` column names the field that failed.
- [ ] `paper/figures/*.png` look like the figures in the PDF.
- [ ] Nothing was fetched from the network (all commands above use `--offline` or read only the cache).
