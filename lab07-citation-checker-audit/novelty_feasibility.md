# Novelty and feasibility — Prompt 04 — 2026-10-30

Searches actually run through web search: `Russinovich citation hallucinations RefChecker 2026 references github`; `Crossref REST API metadata license public domain rate limits`; `Walters Wilder 2023 fabricated citations ChatGPT scientific reports`; `Agrawal 2023 Do Language Models Know When They’re Hallucinating References arxiv`; `Crossref metadata license facts copyright abstracts`. Search is targeted, not a systematic or exhaustive literature review.

Additional reproducible searches for a later broader audit: `"citation verification" "controlled corruption" precision recall`; `"bibliographic" verifier "false positive"`; `"CiteCheck" DOI metadata`; `"citation hallucination" benchmark error types`. These additional strings are proposed, not claimed executed.

| Neighbor | VERIFIED contribution / primary source | Limitation relevant here | Proposed difference | Missing evidence |
|---|---|---|---|---|
| [Phantom References](https://arxiv.org/html/2607.00738v1) | Bibliography verification; [open MIT tool](https://github.com/markrussinovich/refchecker) | Conference incidence does not by itself measure detection accuracy on known corruptions | Tiny transparent controls with separate mutation categories | Full official-tool reproduction and independent human adjudication |
| [CiteCheck](https://arxiv.org/html/2605.27700v1) | Retrieval plus LLM verification, three labels, controlled-corruption physics benchmark | Its full learned/prompted pipeline is beyond this CPU-only control | Evaluate simple DOI/metadata controls, expose identifier mismatch and missing-DOI handling | Dataset/code licence and download not checked; no priority claim allowed |
| [Detecting Hallucinated and Suspicious Citations](https://arxiv.org/abs/2607.22693) | Position paper evaluates existing reference-checking tools | Tool-level investigation is already neighboring work | Narrow transparent course-level comparison | Full methods/results not audited; paper located, not a systematic novelty exclusion |
| [Walters & Wilder](https://doi.org/10.1038/s41598-023-41032-5) | Distinguishes fabricated citations from errors in real citations | Generation audit is not the same as verifier validation | Score constructed error labels explicitly | Natural-generation representativeness remains untested |

**Decision: GO for a course-level controlled comparison; NO-GO for claiming the general idea of known-corruption citation-verifier evaluation is novel.** CiteCheck materially weakens the earlier assumption of an unstudied general gap. Narrow the problem to an interpretable, no-LLM control experiment with explicit identifier errors and abstention. Do not state that no other paper reports precision/recall by error type.

## Resource and access record

Crossref public REST API access is documented at [official API documentation](https://www.crossref.org/documentation/retrieve-metadata/rest-api/). Actual lookup is checked by `results/environment.json`; successful acquisition is separate evidence in `data/manifest.json`. [Official metadata terms](https://www.crossref.org/documentation/retrieve-metadata/) distinguish reusable bibliographic facts from copyrighted abstracts. Save only facts, provenance URL and timestamps; do not download article text. Requests are serial, cached and delayed, with retries; service errors do not become fabricated-citation labels. A Crossref 404 cannot establish worldwide nonexistence.

No weights, model training, GPU stack, OpenAlex key or paid API needed. OpenAlex is deferred to avoid making unverified access claims. RefChecker's current repository is public and MIT, but it is not installed or represented as reproduced. Other upstream licences remain UNKNOWN until needed; no upstream source is copied into this project.

Timeline: days 1–3 verify brief/protocol, days 4–7 acquire and validate pilot (current work), week 2 expand and evaluate frozen comparisons, week 3 analyze and write. This is a plan, not elapsed work. Main bottleneck is independent label validation, not GPU compute. If Crossref fails, rerun the saved cache offline; if a required source is unavailable, record an amendment before any evaluation. If cache is absent and networking fails, stop acquisition rather than invent records. The current small sample establishes pipeline behavior, not external validity.
