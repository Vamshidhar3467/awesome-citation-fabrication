# Gap Matrix — Lab 07 (Prompt 02 output)

**Source analysed:** Lab 06 review, `main.tex` (section numbers follow the compiled PDF).
**Produced:** 2026-10-21, Claude (Opus 5.5) in Claude Code, acting as research mentor. See `ai_assistance_log.md`.
**Labels:** VERIFIED (read in the review / checked) · INFERRED · UNKNOWN. "In the review" ≠ "true": claims about original papers stay unverified until you check the paper.

---

## Part 1 — What the review contains

### Central methods
| Method | Where in review | What it does |
|---|---|---|
| Manual database lookup | §3.2 (Bhattacharyya, Walters & Wilder, Chelli) | Humans check each generated reference in PubMed / Google Scholar |
| Self-questioning (Agrawal et al.) | §5.1 | Model is asked direct/indirect questions about its own reference |
| SelfCheckGPT | §5.2 | Consistency across multiple sampled outputs |
| FActScore | §5.2 | Split text into atomic facts, check each against a source |
| ALCE benchmark | §3.3, §5.2 | Automatic citation precision/recall for cited generation |
| RefChecker (Hu et al.) | §5.3 | Claim-triplet checking against a reference |
| Multi-database pipeline (Russinovich et al.) | §5.3 | Bibliography checked against arXiv, Semantic Scholar, OpenAlex, Crossref, DBLP, ACL Anthology, then LLM web search |
| Wayback Machine check (Rao et al.) | §5.4 | Separates never-existed URLs from link rot |

### Datasets / benchmarks named
ALCE / ELI5 (§3.3) · DeepResearch Bench, 100 PhD-level tasks (§3.4) · DRBench 53,090 URLs and ExpertQA 168,021 URLs (§3.4) · RefChecker 11,000-triplet benchmark (§5.3) · 111M references / 2.5M papers (§3.5).
**Availability and licences of all of these: UNKNOWN** — the review does not say.

### Measured findings (as reported in the review — all need checking against originals)
- Unaugmented chat LLMs: 18–91 % fabricated, depending on model/topic (Table 1).
- Commercial legal RAG tools: 17–33 % hallucinated or incomplete (Magesh et al.).
- Deep-research agents: 3–13 % hallucinated URLs, 5–18 % non-resolving (Rao et al.).
- ~1 in 20 NeurIPS/USENIX 2025 papers with ≥2 likely-hallucinated references (Russinovich et al.).

### Limitations the review attributes to original papers
| Limitation | Review § | Attributed to |
|---|---|---|
| Rates vary with prompt wording | §6.3 | Bhattacharyya et al. — **CORRECTED (student check, 2026-10-22):** rates varied by prompt *topic* (p = 0.007) and medical field (p = 0.03) within one template, not by prompt wording. The review misreads this. |
| Bibliographic "drift" (preprint vs. published version) should not count as hallucination | §4.1, §6.1 | Russinovich et al. — **VERIFIED (student check):** strict definition = fabricated works or substantially wrong authors, excluding venue/year drift |
| Automated flags need human verification; many are false positives | not in review | Russinovich et al. — **VERIFIED (student check)**; new finding not stated in the review |
| Closed systems can't be attributed to a pipeline stage | §6.2 | Magesh et al. |
| Rates differ by domain | §4.4 | Walters & Wilder; Rao et al.; Chelli et al. |

### Unresolved questions the review raises itself (§6, §7)
Shared definitions · continuously updated cross-vendor benchmarks · external ground truth for URLs · volume-aware metrics · cross-lingual coverage · contamination feedback loops · false-positive/false-negative trade-offs of automated verifiers · audit protocols for closed tools.

---

## Part 2 — Five computationally testable gaps

### G1 — Does the definition of "fabrication" change the measured rate?
- **Review passage:** §6.1 ("inconsistent operational definitions"); §7 bullet 1 (decomposed metrics: existence, attribute accuracy, support accuracy); §4.1 drift-exclusion argument.
- **Source of limitation:** Original paper (Russinovich et al. on drift) **+ review's own inference** that definition differences explain much of the 6–91 % spread. The "explains much of the spread" part is INFERRED.
- **Denominator (VERIFIED, Russinovich et al. evaluation section):** the authors show that the same failures look rare per reference (under 1 %) but common per paper. The planned G1 analysis should therefore report rates both per reference and per paper/report, as well as under each definition.
- **Verification (2026-10-22):** Drift exclusion VERIFIED: Russinovich et al. flag fewer than 1 % of references under their strict definition. Walters & Wilder report fabricated citations (55 % / 18 %) separately from substantive errors in real citations (43 % / 24 %), which VERIFIES that studies split categories differently.
- **Experimental question:** On one fixed set of citations, how much does the reported fabrication rate change between (a) strict "any error" counting, (b) identity-level only, and (c) drift-excluding definitions?
- **Evidence that would test it:** A labelled citation set where each item has an error type, scored under each definition; the size of the rate difference.

### G2 — How accurate are automated citation verifiers, by error type?
- **Review passage:** §7 bullet 7 (verifiers' "false-positive/false-negative trade-offs at scale" not yet studied); Table 2 ("edge cases include preprints, variants, and incomplete metadata"); §5.3.
- **Source of limitation:** **Now supported by an original paper (VERIFIED, student check 2026-10-22):** Russinovich et al. stress that their tool's flags need human verification because many are false positives. Table 2's edge-case wording remains the review's own inference.
- **Resolved (2026-10-22, from the text of the paper; Fig. 8 values not seen):** Russinovich et al. do **not** measure a false-positive rate. They give no precision, recall or share of wrong flags; they say only that most hand-checked flags were set aside as false positives. Fig. 8 splits *flagged* references into three types (unresolved, substantial author-list mismatch, multi-field failure). That describes the flags, not the checker's accuracy. False-positive causes are given only as qualitative examples: an editor listed as coauthor, a title fragment parsed as an author, two real papers sharing a title, PDF extraction errors, and real works not yet indexed.
- **Consequence for G2:** Measuring a verifier's precision and recall by error type, and its false-positive rate by cause, is **not reported** in this paper. Novelty against the wider literature is still UNKNOWN (Prompt 04 search).
- **Design input:** Each of the five false-positive causes above can become a controlled test category, alongside the true error types (fabricated work, wrong author, wrong year/venue, Frankenstein, wrong DOI).
- **Citation limit:** Russinovich et al. can be cited for the *kinds* of false positives, not for *how often* the tool errs.
- **Possible comparators (availability UNKNOWN):** Russinovich et al.'s RefChecker; Rao et al.'s open-source **urlhealth** (for URLs, not bibliographic records). Check whether code is public and licensed.
- **Name clash (VERIFIED):** "RefChecker" names two different tools: Russinovich et al.'s bibliography checker, and Hu et al.'s (2024) claim-triplet hallucination checker. The review's §7 bullet links RefChecker to Hu et al. in a peer-review context, where Russinovich et al.'s tool is the relevant one.
- **Experimental question:** Which kinds of citation error (fabricated work, wrong year/venue, swapped authors, mixed-up "Frankenstein" citation, wrong DOI) does a DOI-only check catch, compared with metadata fuzzy-matching against Crossref/OpenAlex?
- **Evidence that would test it:** Real references plus copies with controlled, known errors (so ground truth is known by construction); precision/recall per error type for each verifier.

### G3 — Does ranking systems by error *rate* differ from ranking by expected errors *per report*?
- **Review passage:** §4.1 Eq. 1 (E[F] = Np); §4.3; §6.5 ("Few studies report both the rate and the absolute count").
- **Source of limitation:** Volume effect attributed to Rao et al.; "few studies report both" is the **review's own claim** (INFERRED).
- **Experimental question:** For two or more system configurations, is the order by per-citation fabrication rate the same as the order by expected fabricated citations per report?
- **Evidence that would test it:** N citations per output and p per configuration, measured on a common prompt set.
- **Cost note:** Needs generation from several systems; agentic/deep-research tools are usually paid.

### G4 — How many prompts and trials are needed for a stable fabrication-rate estimate?
- **Review passage:** §6.3 ("argues for multi-prompt, multi-trial designs"); §6.4 (moving target).
- **Source of limitation:** **Weakened (student check 2026-10-22):** Bhattacharyya et al. found variation by *topic* and *field*, not by prompt wording, so they do not support wording sensitivity. Wording/trial sensitivity is now only the review's inference (INFERRED). A topic/field-sensitivity version of this gap would be supported by the original paper.
- **Experimental question:** For one model, how much does the measured fabrication rate vary across prompt wordings and repeated runs, and how many runs does it take for the estimate to stabilise?
- **Evidence that would test it:** k prompt variants × n repeats, each citation verified; variance and confidence intervals versus number of runs.
- **Cost note:** Needs one model. A small open model run locally could work — whether your hardware can run one is UNKNOWN.

### G5 — Can self-consistency checks replace external lookup?
- **Review passage:** §5.1 ("a partially effective, cheap first-pass filter"); Table 2 ("does not establish that a source exists externally").
- **Source of limitation:** Agrawal et al. (original method); the weakness in Table 2 is the **review's own inference**.
- **Experimental question:** How well does a model's self-consistency about a reference agree with the ground truth from database lookup?
- **Evidence that would test it:** Model-generated references, self-consistency scores, and existence labels from Crossref/OpenAlex; agreement metrics.
- **Cost note:** Needs model access for repeated querying.

---

## Part 3 — Top-3 ranking

**Resources (confirmed 2026-10-22):** laptop with RTX 4050 (6 GB VRAM), no paid API budget, about 3 weeks. Local models must be small (about 3–4B parameters) or 4-bit quantized (INFERRED, still to test).

| Rank | Gap | Significance | Resources | Feasibility | Why |
|---|---|---|---|---|---|
| 1 | **G2** | High: directly addresses the review's §7 call about verifier error trade-offs | Free scholarly APIs (Crossref/OpenAlex terms: INFERRED free — check), no GPU | High | Ground truth built by construction; reuses your Lab 01 A–E categories; no model needed |
| 2 | **G1** | Medium–high: speaks to the field's main comparability problem | Same labelled data as G2 | High | Can be the "deeper analysis" for G2 rather than a separate study |
| 3 | **G4** | Medium | One small local model on the RTX 4050 | Medium | Feasible on its own, but too much alongside G2 in 3 weeks |

**Optional extension to G2 (made possible by the GPU):** use a small local open model to generate references for a set of topics. These give a second test set with *natural* errors, alongside the deliberately altered set. Ground truth for this set needs manual labelling, so keep it small (about 50–100 references).

G3 and G5 are not ranked: G3 needs paid agentic tools; G5 depends on model access and is weaker on significance.

**Novelty:** Not claimed. Whether G2 or G1 has already been studied must be checked with a separate literature search (Prompt 04).

---

## Part 4 — Claims to verify against the original papers before you rely on them
Results of the student's checks on 2026-10-22 are marked below.

- [x] **Russinovich et al. (2026):** drift exclusion VERIFIED. "RefChecker" is their own tool (a different tool from Hu et al.'s, same name). About 48,000 accepted papers from ICLR, ICML, NeurIPS and USENIX Security (the review mentions only NeurIPS and USENIX). Fewer than 1 % of references flagged; about 1 in 20 NeurIPS and USENIX Security 2025 papers has at least two. Reviewer scores don't track it. Many flags are false positives.
  - [x] False-positive rate: **not quantified** (qualitative causes only). Fig. 8 breaks down flagged references by failure mode, not wrong flags. See G2.
  - [x] **Evaluation section and Fig. 8 read by student (2026-10-22), VERIFIED:**
    - Corpus: 48,095 accepted papers and 2,614,992 extracted references. ICLR 2021–2026; ICML, NeurIPS and USENIX Security 2021–2025.
    - "Likely hallucinated" = no matching work found, or the best match's author list diverges substantially. Year, venue and publication-status drift are recorded but not counted. The authors call their rates a **lower bound**.
    - **Denominator effect, stated by the authors:** under 1 % of *references* in almost every venue-year, but a large share of *papers*, because each paper has many references.
    - Fig. 8 composition of flagged references (values **read approximately from the chart**, ±2 points):

      | Venue | Multiple failures | Unverified (no work found) | Author mismatch |
      |---|---|---|---|
      | ICLR | ~41 % | ~38 % | ~21 % |
      | ICML | ~40 % | ~38 % | ~22 % |
      | NeurIPS | ~41 % | ~38 % | ~21 % |
      | USENIX Security | ~47 % | ~39 % | ~14 % |

    - Fig. 8 shows what flagged references look like, **not** whether flags were correct.
- [x] **Bhattacharyya et al. (2023):** 30 papers, 115 references; 47 % fabricated, 46 % authentic but inaccurate, 7 % accurate — VERIFIED. **Review §6.3 is wrong:** variation was by topic (p = 0.007) and field (p = 0.03), not prompt wording.
- [x] **Rao et al. (2026):** 3–13 % hallucinated and 5–18 % non-resolving VERIFIED; agents produce more citations and hallucinate at higher rates VERIFIED. Correction: 10 models/agents on DRBench but only 3 on ExpertQA. They release an open-source tool, **urlhealth**, which reduces non-resolving URLs to under 1 % in self-correction tests.
  - [ ] Still open: the 5.4 % (Business) vs 11.4 % (Theology) domain range; the 168,021 / 32-field ExpertQA figures.
- [x] **Walters & Wilder (2023):** 42 topics, 636 citations; 55 % / 18 % fabricated; 43 % / 24 % substantive errors among real citations — VERIFIED.
  - [ ] Still open: the geography-vs-medicine comparison; the 51 % aggregate across six studies.
- [ ] **Magesh et al. (2025):** the opacity statement in §6.2.
- [ ] **All 2026 arXiv papers** (Zhao, Rao, Russinovich, Sakai, Ansari): confirm each exists with the stated title, authors and arXiv ID.
- [ ] **Table 1:** every rate you quote in Lab 07 should be checked against its original paper.

---

## Continuation note — 2026-10-30 — Prompt 04 novelty update

Historical G2 wording above is preserved for provenance. A targeted primary-source search located [CiteCheck](https://arxiv.org/html/2605.27700v1), which already studies retrieval-grounded checking on controlled-corruption citations. Also located [Detecting Hallucinated and Suspicious Citations](https://arxiv.org/abs/2607.22693), neighboring tool evaluation work. Therefore the general controlled-corruption/verifier-accuracy idea is not claimed novel. The wider absence-of-prior-work claim is UNKNOWN; see novelty_feasibility.md.

The current executable study narrows G2 to simple no-LLM controls with explicit abstention and identifier mismatch, not full replication of either published pipeline. G1's identity-only rescoring is planned; a +7 year corruption does not establish real version drift. Existing five false-positive causes are not all implemented. Baseline pilot results and limitations are in baseline_validation.md; no held-out or real-report fabrication rates have been produced.
