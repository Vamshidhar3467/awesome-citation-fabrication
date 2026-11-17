# AI use and research-integrity report — Prompt 18

*Covers the whole project, with the most detail on Phases IV–VI (2026-11-17). Prompt-by-prompt entries are in [`ai_assistance_log.md`](ai_assistance_log.md). This report doesn't invent anything the logs don't show, and it doesn't count work as the student's when an AI did it.*

## Who did what

The work happened in three stretches, and they differ a lot in how much of it was the student and how much was AI.

**Phases I–II (2026-10-21 to 10-22), Claude Code.** AI drafted the workspace, the scope summary and the gap matrix. The student made the substantive decisions here. They checked the AI's summary of the review against `main.tex` and found two slips, read four original papers, caught that the review had misattributed prompt-wording sensitivity to Bhattacharyya et al., and chose gap G2. These are recorded in log entries 1–5 in the student's own words.

**Phase III (2026-10-30), recorded in the log as Codex.** On the student's instruction to continue autonomously, an AI agent wrote all of the code in `src/`, `scripts/` and `tests/` at that point, chose the Pathway B design and froze the protocol. The student had not yet reviewed each technical choice, and the log says so.

**Phases IV–VI (2026-11-17), Claude Code with Claude Opus 5.5.** The student's prompt was to continue from Phase III, "complete the work completely", and make the reports read naturally ("humanize"). The agent then wrote the amendment, the new code and tests, ran every experiment, wrote the evaluation and discussion documents, drafted and revised the paper, reviewed it, and wrote this report. No student decision about Phase IV content has been recorded yet. The things only the student can do are listed at the end.

On "humanize": the reports were written in plain, first-person prose, but that changes style, not disclosure. AI involvement is stated in the paper and here. Nothing was written to hide it.

## Significant AI-assisted activities, Phases IV–VI

| Task | Tool | What the AI proposed or did | Human decision | How it was checked | Outcome |
|---|---|---|---|---|---|
| Choose the contribution (Prompt 12) | Claude Code | Argued that B2 beating B1 would be near-tautological because labels and lookup share Crossref, and proposed a legitimate-variant stress set plus one rule change (B3), logged as amendment A1 *before* any held-out output | Covered by the student's "complete the work" instruction; content not yet reviewed | Order of events visible in file timestamps and logs; the amendment names its own risks | `contribution_plan.md` |
| Random extension set | Claude Code | One Crossref `sample` call, eligibility filter, 40 works frozen with hashes | As above | Snapshot hash in manifest; offline rebuild reproduces cases byte for byte | `data/ext_*` |
| Refactor library without changing frozen behaviour | Claude Code | Split case construction, added field-level checks, B3 and the stress builder | — | Rebuilt `cases.json` and compared it byte for byte with the Phase III file before going further; all 10 old tests still passed | Identical |
| New tests | Claude Code | 7 tests (B3, ablation, stress applicability, split check, macro recall) | — | Ran them; one failed, see below | 17/17 pass |
| Evaluation (Prompt 13) | Claude Code | `evaluate.py` with alignment checks, ablation, sensitivity, clustered bootstrap | — | Pilot-only development run first; then one held-out run; then `verify.py` regenerates every result file byte-identically | `results/phase4/` |
| Figures | Claude Code | matplotlib figures from result files only | — | Palette checked with a colour-vision validator; each PNG opened and inspected, and label collisions fixed twice | `paper/figures/` |
| Interpretation (Prompt 14) | Claude Code | Separated observation, mechanism and unsupported claims; ranked three follow-ups | — | Every number cross-checked against CSV/JSON | `results_discussion.md` |
| References | Claude Code | Built `references.bib` | — | Every entry queried live from arXiv or Crossref; author lists and titles compared | 9 entries, all matched |
| Paper (Prompt 15) | Claude Code | Full draft in LaTeX | — | Compiled, rendered and read page by page | `paper/main.pdf` |
| Peer review (Prompt 16) | Claude Code | Critical self-review (4 major, 6 minor), then revisions | — | Revisions applied and recompiled; numbers unchanged | `peer_review.md` |
| Repository docs (Prompt 17) | Claude Code | README, data and paper READMEs, requirements, reproduction checklist | — | Commands not run here are marked [TEST REQUIRED] | `README.md` |

## Real examples of AI mistakes and corrections

None of these was caught by the student. They were caught by running code, by looking at output, or by checking a claim against a file. That is worth stating plainly, because a fluent draft is easy to trust.

1. **A boolean that wasn't.** `eligible()` in `acquire_ext.py` was written as `a and b and c and venue`, which returns the venue *string*, not `True`. Summing it crashed with `TypeError: unsupported operand type(s) for +: 'int' and 'str'`. The crash happened before the snapshot was saved, so nothing was frozen with the bug. Fixed by wrapping the expression in `bool(...)`.
2. **A wrong test.** A new test expected "Spectroscopic" to be the word split by the hyphenation variant, but "characterisation" is longer. The code was right and the AI's expectation was wrong. Only the test was changed.
3. **A missing cache entry.** The first held-out run stopped with `FileNotFoundError` for an uncached synthetic test DOI. That came from a Phase III decision to cache only pilot lookups. The fix was to look up the 8 test DOIs, inside the request budget already set in the amendment. No output had been written.
4. **Overclaims caught while checking the draft against data.** The draft said B3 removed "a third" of the flags (it was 30/47 ≈ 64%). It said four legitimate variants match Russinovich et al.'s false-positive causes (only two do directly). It described Walters and Wilder's method in more detail than the verified notes support. The evaluation report gave a prediction row count of 1,413 (the file has 1,509, because the pilot is included). The review quoted 0–5 stress cases per work (it's 0–4). All were corrected, and each one was found by checking a file or count, not by rereading the prose.
5. **Design weakness found in review.** The self-review pointed out that B3's headline improvement was designed together with the test it passes. The paper now says this explicitly and no longer presents it as general validation of B3.
6. **Tooling slips.** A `sed` edit turned `\citep` into a tab character. A shell heredoc broke on quoting. Both were found by the compiler or the shell, and both were fixed.

## Which conclusions depend on human reasoning

- **Student reasoning (Phases I–II, recorded):** the choice of G2, the correction of the review's misreading of Bhattacharyya et al., the reading of Russinovich et al.'s evaluation section, including that they report no false-positive *rate*, and the recognition that drift is excluded from their definition. The whole Phase IV contribution rests on that last reading.
- **AI reasoning not yet checked by the student:** the decision that the B1-versus-B2 comparison is near-tautological, the choice of legitimate-variant types, the B3 rule, the interpretation of the ablation and sensitivity results, and the paper's framing. These are defensible and documented, but they need the student's own review before submission.

## What was learned about vibe coding here

Fast generation was never the bottleneck. Verification was: byte-comparing the refactor against frozen data, running the pilot before the held-out set, opening every figure, and querying every citation. Each of the real errors above would have shipped if the output had only been read, not run. The other lesson is that being honest about design weaknesses (circularity, a fix designed alongside its test, and so on) made the paper more defensible, not less.

## Remaining risks

- The student hasn't yet read or approved the Phase IV–VI content. A viva would expose that.
- Labels and lookups share one registry, and the legitimate variants are registry-derived.
- The extension sample can't be redrawn. Its validity depends on the saved snapshot.
- Nothing has been pushed to GitHub, no licence has been chosen and no instructor gate has been signed off.

## What only the student can do before submission

1. Read `contribution_plan.md`, `results_discussion.md` and the paper, and either accept the framing or change it. The paper is written in your voice, so it should say what you'd say.
2. Pick three cases from `results/phase4/predictions.csv` (one "et al.", one abbreviated venue, one Frankenstein) and trace each from case file to cache to prediction by hand.
3. Be ready to explain the viva points in `demo_walkthrough.md`, especially why the 100% recall isn't impressive and why B3's improvement is by construction.
4. Choose a licence, create the GitHub repository and push it. The agent didn't publish anything.
5. Add your own entry to `ai_assistance_log.md` recording what you checked and decided.
