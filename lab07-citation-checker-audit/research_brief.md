# G1 research brief — Prompt 05

**Student:** Bayyapu Vamshidhar Reddy, MRA2026010. **Review topic:** Benchmarking Citation Fabrication Rates Across Large Language Models and Agentic Search Tools. **Working study title:** Error-type audit of DOI-based citation verification.

**Evidence and gap:** Lab06 §§5.3, 6.1 and 7 motivate validation of bibliography checking and explicit definitions. Original sources: [Russinovich et al.](https://arxiv.org/abs/2607.00738), [Walters & Wilder](https://doi.org/10.1038/s41598-023-41032-5), [Agrawal et al.](https://aclanthology.org/2024.findings-eacl.62/). Newly checked [CiteCheck](https://arxiv.org/abs/2605.27700) already uses controlled corruption, so general novelty is NOT claimed. The narrower course-level problem is explaining the limitations of simple, inspectable, no-LLM verification controls.

**Pathway:** Controlled comparative study, with an optional isolated metadata-check extension. **Problem:** A registered DOI can coexist with incorrect bibliographic fields. Test which error categories a DOI-only control flags and which it misses, while treating missing identifiers and network errors explicitly.

| Question / expectation | Data, comparator and variables | Metric / decision rule | Contrary observation |
|---|---|---|---|
| RQ1: Does metadata checking detect more controlled errors than registration-only checking? H1: higher recall. | Same structured citations/cache; independent variable checker; dependent variable flag correctness | Primary macro recall over five error types; practical threshold +0.10 with FPR increase <=0.05 | Recall gain below threshold, or excessive FPR |
| RQ2: Which categories cause misses or manual-review burden? | Eight fixed mutation/control categories; same source works | Per-category confusion counts, recall, FPR and coverage; descriptive, no superiority threshold | DOI-only detects registered-DOI metadata errors, contradicting its specified behavior and requiring debugging |
| RQ3: How does the target definition change interpretation? | Same predictions rescored under any-error versus local identity-only labels | Compare precision/recall and list relabelled categories; no directional hypothesis | No change must be reported if it occurs |

**Data:** Twelve fixed Crossref records; source-group split before mutation, four pilot works and eight held-out works. Eight variants per work. Source-level grouping prevents variants or donor works crossing partitions. This small construction is a feasibility dataset, not a representative benchmark of LLM fabrication rates. Before stronger claims, expand and independently audit the source set under a recorded protocol amendment.

**Controls/resources:** Fixed seed 20261030, frozen thresholds, identical lookup cache, CPU, standard-library Python, no model budget. RTX 4050 is available but unnecessary. Output flags are audit signals, not proof of fabrication. Independent bibliographic truth, broader domain coverage, instructor approval and student code comprehension remain outside automated verification.

**First executable milestone:** Verify Python/system/API access, acquire fact metadata, run schema/split/metric checks, execute B1 on the pilot and save genuine predictions/metrics. Phase III ends with baseline validation; held-out comparison, research conclusions and final paper are later phases. Intended contribution is a transparent error audit; no contribution has been established by the plan itself.
