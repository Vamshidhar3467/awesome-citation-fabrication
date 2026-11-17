# Research Decisions Log — Lab 07

**Student:** Bayyapu Vamshidhar Reddy (MRA2026010)
**Topic (T21):** Benchmarking Citation Fabrication Rates Across Large Language Models and Agentic Search Tools
**Evidence labels:** VERIFIED = checked against the original source or actual execution · INFERRED = plausible interpretation that still needs testing · UNKNOWN = evidence missing

---

## Entry 1 — 2026-10-21 — Workspace setup and review scope (Prompt 01)

**Decision:** The Lab 06 ACM CSUR review (`Lab06/BayyapuVamshidharReddy_MRA2026010/main.tex`, 13 pages, 26 references) is the evidence base for Lab 07.

**Reason:** It is the most complete and most recent version of the review. The Lab 04 review is shorter, cites fewer of the core benchmarking studies, and contains a known metadata error (wrong authors for Bhattacharyya et al.).

**Caution (VERIFIED):** Much of the Lab 06 text comes from the Lab 01 paper, which Claude generated. Claims in the review are therefore *not* evidence by themselves. Each claim used to justify a gap must be checked against the original publication.

### Scope of the review (VERIFIED — read from main.tex)
| Section | Content |
|---|---|
| 1 Introduction | Scale of the problem; three review questions (prevalence by system class; detection/mitigation; methodological gaps) |
| 2 Review Methodology | Inclusion criteria (2023 – Sep 2026); three analytical layers: existence, attribute accuracy, support accuracy; Fig. 1 workflow |
| 3 Background | Hallucination taxonomy (Ji, Huang, Agrawal); early medical audits (Bhattacharyya, Athaluri, Wagner, McGowan, Walters & Wilder, Chelli); generative search (Liu, Gao/ALCE); legal and agentic (Dahl, Magesh, Du, Rao); contamination of the scholarly record (Zhao, Russinovich, Sakai, Ansari, Naddaf) |
| 4 Taxonomy | Four failure types; Eq. 1 E[F] = Np (volume effect); Fig. 2 taxonomy; Table 1 rates by system class; domain sensitivity |
| 5 Mitigation | Self-verification; SelfCheckGPT, FActScore, ALCE; RefChecker, Reference Hallucination Score, multi-database pipelines; Wayback URL checks; RAG; Table 2 |
| 6 Challenges | Definitions; proprietary opacity; prompt sensitivity; moving target; volume/denominator; feedback loops |
| 7 Research Gaps | Eight directions |
| 8–9 | Synthesis; conclusion |

### What the review does NOT contain (VERIFIED)
- No experiments, code, or measured results of its own.
- No list of available datasets, code repositories, or licences for the cited studies.
- No search counts or screening numbers: Section 2 states inclusion criteria, but there is no record that a screening was actually carried out (UNKNOWN).

### Resources and constraints
| Item | Status |
|---|---|
| Hardware | VERIFIED (`nvidia-smi`, 2026-10-22): laptop with NVIDIA GeForce RTX 4050 Laptop GPU, 6 GB VRAM. No PyTorch or Ollama installed yet. |
| Local model capacity | INFERRED: 6 GB fits small open models (about 3–4B parameters) comfortably, and roughly 7–8B models only when 4-bit quantized. Must be tested. |
| Paid LLM API budget | None (stated by student) |
| Time available | About 3 weeks (stated by student) |
| Group policy | UNKNOWN — check Google Classroom |

**Next action:** Run Prompt 02 (gap extraction) → see Entry 2.

---

## Entry 2 — 2026-10-21 — Candidate research gaps (Prompt 02)

**Output:** `gap_matrix.md` (5 candidate gaps, top 3 ranked).

**AI ranking (INFERRED — assumes laptop only, no paid API budget):**
1. G2 — Accuracy of automated citation verification by error type
2. G1 — Effect of the definition of "fabrication" on the measured rate
3. G4 — Prompt and trial sensitivity of fabrication-rate estimates

**Re-ranking with confirmed resources (2026-10-22, INFERRED):** The GPU, no API budget and 3-week window do not change the order. G2 stays first: it needs no model and fits 3 weeks. The GPU makes one addition feasible: a small local open model can *generate* references, giving G2 a second test set of naturally occurring errors alongside the deliberately altered ones. G4 becomes feasible with a local model, but running it as well as G2 is too much for 3 weeks.

**Human decision:** G2 chosen — see Entry 5.

**Next actions (from Entry 2):**
- [x] Open the original paper behind each top-3 gap (done for 4 papers — see Entry 3) and confirm the cited limitation; change labels to VERIFIED or correct them.
- [x] Fill in hardware and budget above, then ask for the ranking to be redone if they differ from the assumptions (done 2026-10-22; ranking unchanged).
- [ ] Prompt 03: map the chosen gap to an executable baseline.

---

## Entry 3 — 2026-10-22 — Original papers checked by the student

**Checked:** Russinovich et al. (2026), Bhattacharyya et al. (2023), Walters & Wilder (2023), Rao et al. (2026). Details are in `gap_matrix.md`, Part 4.

**What changed:**
- **G2 strengthened.** Russinovich et al. state that their tool's flags need human verification because many are false positives. G2's motivation now rests on an original paper, not only on the review.
- **G1 strengthened.** Drift exclusion is confirmed in Russinovich et al. Walters & Wilder count fabrication and errors in real citations separately, which shows that definitions differ between studies.
- **G4 weakened.** Bhattacharyya et al. found variation by topic and field, not by prompt wording.
- **Review error found.** Lab 06 §6.3 misattributes prompt-wording sensitivity to Bhattacharyya et al. Do not carry this claim into the Lab 07 paper.
- **New resource.** Rao et al. release an open-source URL checker, **urlhealth** (repository and licence UNKNOWN).

**Open question that decides G2's novelty:** Do Russinovich et al. measure their false-positive rate, or break errors down by type? If they do, G2 must be framed as an extension of their work, not a new question.

**Human decision:** G2 chosen — see Entry 5.

---

## Entry 4 — 2026-10-22 — G2 novelty check against Russinovich et al.

**Finding (VERIFIED — student read the paper's text; Fig. 8 values not visible):** Russinovich et al. give no false-positive rate, precision or recall. They report only that most hand-checked flags were false positives, with qualitative causes: editor listed as coauthor, title fragment parsed as author, two real papers with the same title, PDF extraction errors, real works not yet indexed. Fig. 8 splits flagged references into unresolved / author-list mismatch / multi-field failure.

**Implication (INFERRED):** G2 fills a gap this paper leaves open: measuring a reference verifier's error rates per error type and per false-positive cause, on test data whose correct labels are known by construction. The five false-positive causes can serve directly as test categories.

**Still to do:** Prompt 04 novelty search — has any other study measured verifier precision/recall by error type?

**Human decision:** G2 chosen — see Entry 5.

---

## Entry 5 — 2026-10-22 — Decision: G2 selected

**Decision:** I will study **G2: how accurately automated citation verifiers detect each type of citation error**.

**Research direction (to be made precise with Prompt 05):** Build test sets of references whose correct label is known by construction, and measure the precision and recall of at least two verification approaches for each error type and each false-positive cause.

**Reasons:**
1. **Gap confirmed in an original paper.** Russinovich et al. (2026) report that most hand-checked flags from their tool were false positives, but they never measure a false-positive rate, precision or recall (Entry 4, VERIFIED). The accuracy of reference verifiers is therefore an open, measurable question.
2. **Testable with known ground truth.** Because I create the test cases — real references plus copies with deliberate errors — the correct label of every case is known before the experiment. Russinovich et al.'s five false-positive causes and my Lab 01 error categories (wrong metadata, Frankenstein, fabricated, identifier mismatch) give concrete test categories.
3. **Feasible with my resources.** The core study needs no paid API and no model training: free scholarly databases (Crossref, OpenAlex — terms still to check) and a laptop. The RTX 4050 (6 GB) allows an optional second test set of references generated by a small local model.
4. **Fits three weeks.** The baseline (DOI-only checking) is simple to build and validate early, leaving time for the comparison and a deeper analysis.
5. **Continuity with my earlier work.** It builds directly on the Lab 01 manual citation audit and the Lab 06 review's call for studying verifiers' false-positive/false-negative trade-offs (§7).

**Planned deeper analysis:** G1. Rescore the same results under different definitions of "fabrication" (strict any-error, identity-level only, drift-excluding) to show how the definition changes the measured rate.

**Not chosen:**
- G3: needs paid agentic tools.
- G4: weakened after Bhattacharyya et al. was checked (variation by topic, not prompt wording), and too much to run alongside G2 in three weeks.
- G5: needs repeated model querying and has lower significance.

**Risks:**
- Novelty against the wider literature is not yet confirmed (Prompt 04).
- Database API rate limits and terms are unverified.
- The tool by Russinovich et al. may not be publicly available as a comparator.
- Manual labelling of the optional model-generated set takes time, so keep it small.

---

## Entry 6 — 2026-10-22 — Russinovich et al. evaluation section and Fig. 8 checked

**Verified by student:**
- Corpus of 48,095 papers and 2,614,992 references.
- Strict definition: no matching work, or a substantial author mismatch; drift recorded but not counted.
- The authors call their rates a lower bound.
- Fig. 8: roughly 40–47 % multiple failures, ~38–39 % unverified, ~14–22 % author mismatch. These values are read approximately from the chart.

**Effect on the plan:**
- G2's gap is unchanged: the evaluation section reports no false-positive rate.
- The authors' own **denominator argument** (rare per reference, common per paper) strengthens the G1 deeper analysis. Report results per reference and per paper, under each definition.
- Fig. 8's three failure modes (unverified, author mismatch, multiple failures) can serve as **labels in the G2 test set**, so results can be compared with their categories.

---

## Entry 7 — 2026-10-30 — Autonomous continuation through Phase III

User requested continuation after Prompt 02 through Phase III, with minimal interruptions, and clarified that a strict 60% allocation was unnecessary. The LabQ7 PDF contains responsible-use/ownership requirements but no numeric 60% allocation. No percentage of human authorship is claimed.

VERIFIED by agent: read LabQ7.pdf and adjacent Lab06 main.tex/references.bib. Read primary-source material and checked Crossref access. Existing personal verification entries are historical student statements, not reassigned to the agent.

INFERRED design decision: select Pathway B, a small controlled comparison of simple DOI-registration and DOI-anchored metadata controls. It is NOT an end-to-end RefChecker reproduction. See literature_to_experiment.md, research_brief.md and experiment_protocol.md for Prompts 03–07. User has not separately endorsed each technical choice; they are agent proposals implemented under the user's autonomous-work instruction.

Novelty correction: CiteCheck (https://arxiv.org/html/2605.27700v1) already describes a controlled-corruption citation benchmark. The broad G2 idea therefore must not be described as previously unstudied. The defensible scope is an interpretable course-level error audit; systematic novelty verification remains incomplete.

## Entry 8 — 2026-10-30 — Real baseline execution and phase boundary

Protocol/config saved before acquisition/pilot measurements. Actual environment: Python 3.14.6 on Windows 11; standard-library runtime, no GPU required. Twelve Crossref records acquired, source-group split into four pilot and eight test works; eight variants per source. API metadata facts and timestamps cached without abstracts/full text.

VERIFIED: 32 pilot cases executed, 4 correct flags, 0 false flags, 16 missed positives, 4 valid missing-DOI abstentions. Ten tests pass. Offline rerun output hashes match. Exact evidence: results/*.log, pilot_predictions.csv, pilot_metrics.json and verification.json. See baseline_validation.md. Sixty-four held-out cases have not been evaluated. Comparisons, research-level deeper analysis and paper writing remain later phases.

Design corrections: wrong-year mutation is not real version drift; DOI-anchored metadata checking is not title-search retrieval; Crossref absence is not proof of fabrication; per-paper rates cannot be estimated from synthetic source groups. Five real-world false-positive mechanisms in the earlier matrix remain future work. Student ownership checks and instructor approval remain UNKNOWN/pending, not invented.

Next personal action: inspect research_brief.md and code_understanding.md. Next experimental action after Phase III: independently audit sample labels, validate/expand comparator coverage, log any dataset amendment before evaluating held-out results.

## Entry 9 — 2026-11-17 — Phase IV contribution and completion through Phase VI

**Decision (agent, under the user's instruction to complete the assignment):** keep the frozen B1-vs-B2 comparison, and treat it as near-tautological because labels and lookup share Crossref. Put the actual contribution in a measured false-flag rate on legitimate citation variants. Add one isolated rule change (B3). All of this was logged as amendment A1 before any held-out output existed (`contribution_plan.md`).

**Why:** it follows from the student-verified reading of Russinovich et al. (Entry 6). Their tool's flags are often false positives, and they describe the causes but don't measure them. Drift is excluded from their definition.

**Result (VERIFIED by execution, `results/phase4/`):** macro recall B1 0.20, B2/B3 1.00 on both held-out sets, with zero false flags on preregistered valid cases. On 87 legitimate variants the false-flag rate is B1 0.00, B2 0.54, B3 0.195. Each false flag traces to one field rule. Identity-only rescoring moves B2's precision from 1.00 to 0.60.

**Not claimed:** LLM fabrication rates; general superiority of B3 (its fix was designed alongside the et-al test); anything about RefChecker or CiteCheck.

**Pending (student):** review and own the framing; trace cases by hand; licence and GitHub; instructor gates G3/G4.
