# Lab 07 through Phase III — handoff

> **Superseded for current status (2026-11-17):** Phases IV–VI are now complete. Start from `README.md`, the paper in `paper/main.pdf` and `ai_audit.md`. This file is kept as the Phase III record.

**Completed scope:** continue existing Prompt 02 work through Prompts 03–11. Your previous three Markdown files were retained; dated continuation entries explain the new work. There is no final paper requirement completed at this stage: the assignment places that in Phase V.

| Assignment prompt | Saved evidence |
|---|---|
| 01–02 existing work | `research_decisions.md`, `gap_matrix.md`, historical `ai_assistance_log.md` |
| 03 literature → executable study | `literature_to_experiment.md` |
| 04 novelty / access / go-no-go | `novelty_feasibility.md` |
| 05 one-page research brief / RQs | `research_brief.md` |
| 06 datasets / baselines | `dataset_baseline_validation.md`, `data/README.md` |
| 07 frozen blueprint | `experiment_protocol.md`, `configs/protocol.json` |
| 08 environment / actual output | `results/environment.json`, `results/environment.log` |
| 09 baseline / modules / tests | `src/`, `scripts/`, `tests/`, `code_understanding.md`, `notebooks/phase3_baseline.ipynb` |
| 10 baseline verification | `baseline_validation.md`, `results/verification.json`, pilot CSV/JSON/SVG |
| 11 genuine debugging | `code_understanding.md`, dated AI log continuation |

**Verified:** 12 real Crossref source records, 96 constructed cases, 32-case pilot executed, ten tests passing, deterministic offline rerun. **Deferred:** evaluation on the remaining 64 cases, full comparator validation/evaluation, deeper research analysis and final manuscript. Keeping test outputs unseen preserves the planned comparison.

The pilot detects 4 of 20 engineered errors, with 0 false flags and 4 missing-DOI abstentions. This validates the DOI-only baseline and shows its expected blind spots; it does not measure real LLM citation-fabrication prevalence. CiteCheck already studies controlled-corruption citation checking, so the brief claims a course-level transparent comparison, not a new general research idea.

To inspect: open `README.md`, run `python scripts/verify.py` from this directory, then read `baseline_validation.md` alongside `results/pilot_predictions.csv`. The notebook presents the same script-driven workflow. No GPU setup required.

**Only the personal checks remain:** read the brief and source claims, inspect a few mutation/label examples, and learn the explanations/viva questions in `code_understanding.md`. The agent has not marked these as your completed reading, approved your own decisions on your behalf, or claimed instructor gate approval. No files were submitted or published.
