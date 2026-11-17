# Literature-to-experiment bridge — Prompt 03

Read evidence: Lab 06 `main.tex` and `references.bib` in the adjacent Lab06 folder, the existing Lab07 decision/gap logs, and primary sources linked below. The prior review was actually available on this run; earlier student verification remains attributed to the student.

| Published method in review | Algorithm and data | Access and metrics | Limitations / computation | Local study option |
|---|---|---|---|---|
| Russinovich et al., Phantom References, §5.3 | Multi-source bibliography verification with escalation; proceedings references | [Paper](https://arxiv.org/html/2607.00738v1), [official MIT repository](https://github.com/markrussinovich/refchecker), repository availability VERIFIED; full installation/execution UNKNOWN. Reports flagged-reference and paper-level incidence. | Multiple services, parsing and search; unresolved records need review. Full execution burden not measured. | A: reproduce official checker on a tiny corpus, then controlled errors. Smallest baseline: one extracted bibliography passed to official tool; requires a separate environment/API audit. |
| Agrawal et al., §5.1 | Ask model author/content consistency questions about references; book/article examples | [Published EACL paper](https://aclanthology.org/2024.findings-eacl.62/), [official code](https://github.com/microsoft/hallucinated-references). Paper and repository link VERIFIED; local install, current model access and repository licence not independently audited. Detection/consistency scores against real/fabricated labels. | Needs multiple model calls; a small local model is an adaptation with unknown fidelity. | B alternative: compare self-consistency and DOI lookup on the same references; model confounds and manual labels add burden. |
| Rao et al., §5.4 | URL resolution and historical existence check; DRBench/ExpertQA cited URLs | [Original paper](https://arxiv.org/abs/2604.03173). Paper access VERIFIED; urlhealth installation/licence not checked here. Non-resolving and hallucinated URL rates. | Archive/network dependencies; URL existence is a different task from metadata accuracy. | C: isolate retry/archive component and evaluate link rot separately; changing bibliographic fields would not test this method. |

## Three pathways for selected G2

| Pathway | Smallest executable baseline | Question | Burden and required evidence |
|---|---|---|---|
| A reproduction + extension | Install and run official RefChecker on one bibliography | How does it behave on controlled metadata mutations? | Highest complexity; pinned upstream commit, exact flags, extraction checks and official configuration needed. Not selected as minimum milestone. |
| B controlled comparison (selected) | DOI-registration lookup on known structured references | Which errors are missed by registration-only verification, and does metadata checking improve detection? | CPU and free Crossref metadata; source-group partitions, mutation audit, identical cache, validated metrics. No exact replication claim. |
| C targeted modification | Preserve DOI-only checker, add metadata consistency thresholds | Does adding metadata detect errors while limiting false flags? | Low compute, but thresholds must be frozen; use B protocol to avoid calling a routine feature a new algorithm. |

Recommendation: B with a deliberately simple original control inspired by database lookup, followed by one isolated metadata comparator. Phase III validates B1 only; B2 is specified and unit checked for later evaluation. No GPU or paid model required, compatible with the recorded RTX 4050 / three-week resource budget.

Before relying on the study, the student should personally inspect the source citations, the nearby CiteCheck work, several clean/mutated records and the code explanations. Automated acquisition/testing is genuine execution but does not constitute the student's reading or endorsement. Instructor acceptance of a controlled comparative pathway remains UNKNOWN.
