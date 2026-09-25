# Citation Fabrication Datasets and Benchmarks

This document provides detailed information about datasets and benchmarks used for evaluating citation fabrication in LLMs and retrieval-augmented systems.

## Public Datasets and Benchmarks

### 1. ALCE: Annotated Long-Form Citation Evaluation

| Property | Details |
|----------|---------|
| **Full Name** | Annotated Long-Form Citation Evaluation |
| **Authors** | Liu, N. F., Zhang, T., & Liang, P., 2023 |
| **Venue** | EMNLP 2023 Findings |
| **DOI** | 10.48550/arXiv.2304.09848 |
| **Repository** | [github.com/haesungpyun/alce](https://github.com/haesungpyun/alce) |
| **Language** | Python |
| **License** | Apache 2.0 |

**Purpose:**  
Benchmark for evaluating citation-grounded generation. Measures whether generated text is fully supported by its associated citations and whether citations actually support the statements they accompany.

**Key Metrics:**
- Citation precision (% of sentences fully supported by citations)
- Citation recall (% of citations that support their statements)
- Verifiability (joint measure of precision and recall)

**Datasets Included:**
- ELIS (web-based open-ended questions)
- ELI5 (Explain Like I'm 5)
- ASQA (Aspect-based question answering)
- BiPAR (Biomedical papers and references)

**Use Case:**  
Evaluate whether generative search engines (Bing Chat, Perplexity, YouChat, NeevaAI) generate verifiable text with properly supported citations.

---

### 2. FActScore: Fine-Grained Atomic Fact Evaluation

| Property | Details |
|----------|---------|
| **Full Name** | FActScore: Fine-Grained Atomic Evaluation of Factual Precision in Long Form Text Generation |
| **Authors** | Min, S., Krishna, K., Lyu, X., et al., 2023 |
| **Venue** | EMNLP 2023 |
| **DOI** | 10.18653/v1/2023.emnlp-main.741 |
| **Repository** | [github.com/shmsw25/FActScore](https://github.com/shmsw25/FActScore) |
| **Language** | Python |
| **License** | MIT |

**Purpose:**  
Automatic evaluation metric for factual precision in long-form generation. Decomposes generated text into atomic facts and checks each against retrieval-based knowledge bases.

**Key Metrics:**
- Per-fact accuracy
- Citation coverage (whether facts have supporting citations)
- Hallucination detection and quantification

**Datasets Included:**
- OPENBIO (open-domain biographical QA)
- Annotated evaluation sets for GPT-3, GPT-3.5, Claude

**Use Case:**  
Evaluate long-form document generation (biography summaries, research overviews) where both factual accuracy and citation support matter.

---

### 3. DeepResearch Bench and DRBench

| Property | Details |
|----------|---------|
| **Full Name** | DeepResearch Bench: A Comprehensive Benchmark for Deep Research Agents |
| **Authors** | Du, M., Xu, B., Zhu, C., Wang, X., & Mao, Z., 2025 |
| **DOI** | 10.48550/arXiv.2506.11763 |
| **Repository** | [github.com/DRBench](https://github.com/DRBench) (check for availability) |
| **Language** | Python |

**Purpose:**  
Benchmark specifically designed for autonomous deep-research agents like OpenAI Deep Research, Google Gemini Deep Research, and Perplexity Deep Research. Evaluates both citation generation and URL validity.

**Evaluation Dimensions:**
- Citation existence (does the work exist?)
- Citation correctness (are metadata accurate?)
- URL validity (do cited URLs resolve?)
- Citation coverage per query (volume effect)

**Test Queries:**
- Multi-hop research questions across science, law, medicine
- News and current events research
- Longitudinal fact verification

**Use Case:**  
Evaluate agentic research systems that query multiple sources, synthesize information, and produce long-form reports with inline citations.

---

### 4. ExpertQA and Domain-Specific Benchmarks

| Property | Details |
|----------|---------|
| **Full Name** | ExpertQA: Expert-Curated Questions and Answers for Evaluating Domain-Specific Knowledge |
| **Authors** | Various domain experts; compiled in academic benchmarks |
| **Scope** | Biomedical, legal, scientific, professional domains |

**Purpose:**  
Expert-curated question-answer pairs for domain-specific evaluation. Includes reference lists that can be used to evaluate fabrication rates in domain-specialized LLMs and RAG systems.

**Domain Coverage:**
- **Medical/Biomedical:** PubMed-curated QA, USMLE exam questions
- **Legal:** Structured legal queries with case law ground truth (from Dahl et al., 2024)
- **Computer Science:** Programming, algorithms, system design

**Use Case:**  
Evaluate domain-specialized systems (medical chatbots, legal research assistants) against expert-verified ground truth.

---

### 5. ArXiv Citation Contamination Corpus (Zhao et al., 2026)

| Property | Details |
|----------|---------|
| **Full Name** | LLM Hallucinations in the Wild: Large-Scale Evidence from Non-Existent Citations |
| **Authors** | Zhao, Z., Wang, Y., Stuart, T., et al., 2026 |
| **DOI** | 10.48550/arXiv.2605.07723 |
| **Scale** | 111 million references across 2.5 million papers |
| **Coverage** | arXiv, bioRxiv, SSRN, PubMed Central |
| **Access** | Preprint with supplementary data |

**Purpose:**  
Large-scale audit of real-world citation contamination. Identifies non-existent citations in published papers by:
1. CrossRef / DOI resolution
2. Author-year-title matching against major databases
3. Temporal anomalies (sudden appearance of hallucinated citations around 2023)

**Key Findings:**
- 146,932 hallucinated citations in 2025 literature alone (conservative estimate)
- Rates by venue: NeurIPS, ACL, EMNLP, medical preprint servers show highest contamination
- Strong correlation with paper submission dates (post-GPT-3.5 adoption)

**Use Case:**  
Assess real-world impact of LLM adoption on scientific literature. Benchmark contamination rates across time, venues, and domains.

---

### 6. Legal Hallucination Corpus (Dahl et al., 2024)

| Property | Details |
|----------|---------|
| **Full Name** | Large Legal Fictions: Profiling Legal Hallucinations in Large Language Models |
| **Authors** | Dahl, M., Magesh, V., Suzgun, M., & Ho, D. E., 2024 |
| **DOI** | 10.1093/jla/laae003 |
| **Scope** | 100+ structured legal queries |
| **Advantage** | Unambiguous ground truth (cases are well-indexed and public) |

**Purpose:**  
Domain-specific evaluation of hallucination in legal research. Queries target:
- Constitutional law
- Contract law
- Tort law
- Procedural law

**Evaluation Method:**
- Submit query to GPT-3.5, GPT-4, Claude
- Check cited cases against Google Scholar, LexisNexis, Justia
- Verify case holding and relevance

**Key Metrics:**
- Case existence rate
- Holding accuracy (does the LLM describe the case correctly?)
- Relevance accuracy (does the case actually support the query?)
- Fabrication rate: **58%+ for GPT-4, higher for other models**

**Use Case:**  
Evaluate RAG-based legal research tools; compare against commercial platforms (Lexis+, Westlaw, CoCounsel).

---

### 7. HalluCitation (Sakai et al., 2026)

| Property | Details |
|----------|---------|
| **Full Name** | HalluCitation Matters: Revealing the Impact of Hallucinated References with 300 Hallucinated Papers in ACL Conferences |
| **Authors** | Sakai, Y., Kamigaito, H., & Watanabe, T., 2026 |
| **DOI** | 10.48550/arXiv.2601.18724 |
| **Dataset** | 300 papers with documented hallucinated citations from ACL, NAACL, EMNLP |

**Purpose:**  
Identify and catalog hallucinated citations that appeared in peer-reviewed NLP conference papers. Creates dataset of:
- Fabricated references (author/title/year combinations that don't exist)
- Misattributed references (real papers cited incorrectly)
- URL hallucinations (broken or wrong links)

**Analysis:**
- Timeline of hallucination detection
- Correlation with paper acceptance/rejection
- Author demographics and experience level
- Impact on conference proceedings and community trust

**Use Case:**  
Study peer-review vulnerability to hallucinated citations; train detection systems on real-world examples.

---

### 8. Medical Reference Hallucination Benchmarks

| Property | Details |
|----------|---------|
| **Primary Studies** | Bhattacharyya et al. (2023), Chelli et al. (2024), Wagner et al. (2024) |
| **Domain** | Biomedical and clinical medicine |
| **Verification Sources** | PubMed, JMIR, Google Scholar, Medline |
| **Total References Audited** | 500+ across studies |

**Coverage:**
- ChatGPT-3.5 vs. GPT-4 comparison
- Bard (Gemini) evaluation
- Specialty-specific: radiology, psychiatry, surgery, internal medicine
- Citation accuracy scoring rubric (complete, metadata errors, fabricated, URL-only)

**Typical Experimental Design:**
1. Prompt LLM for literature summaries in specialty area
2. Manually verify each reference against PubMed
3. Categorize: authentic + accurate / authentic + error / fabricated
4. Calculate fabrication rates and error types

**Key Finding:**  
Fabrication rates: **47–91%** depending on model and topic; only **6–7%** of generated citations are both authentic and accurate in early studies.

---

## Private/Restricted Datasets

### Commercial RAG Audit Data (Magesh et al., 2025)

| Property | Details |
|----------|---------|
| **Scope** | Proprietary audit of Lexis+ AI, Westlaw Ask Practical Law, CoCounsel |
| **Availability** | Published summary; raw audit data restricted |
| **Key Metric** | **17–33% error rate** despite "hallucination-free" marketing claims |

**Significance:**  
First systematic independent audit showing that commercially marketed "hallucination-free" RAG systems still produce substantial citation errors.

---

## How to Use These Datasets

### For Your Own Research

1. **Citation Verification Project**: Use ArXiv Contamination Corpus + Legal Corpus as ground truth
2. **Model Evaluation**: Use ALCE, FActScore, or DeepResearch Bench to test a new model
3. **Domain-Specific Work**: Select Medical or Legal benchmarks matching your domain
4. **Mitigation Method Development**: Use public datasets to train and evaluate detection systems

### For Reproduction

- Most public datasets include train/test splits and evaluation scripts
- ALCE, FActScore, and DRBench have official evaluation codes on GitHub
- Medical and legal datasets document annotation guidelines for consistency

### Data Privacy and Ethics

- All public datasets anonymize personal information where applicable
- Citation data is drawn from publicly available sources
- No copyrighted paper content is included; only metadata and evaluation scripts

---

## Recommended Reading Order

1. **Start here**: Zhao et al. (2026) — Real-world scale of the problem
2. **Methodological foundation**: Ji et al. (2023) — Hallucination taxonomy
3. **Benchmarking approaches**: Liu et al. (2023) ALCE; Min et al. (2023) FActScore
4. **Domain deep-dive**: Dahl et al. (2024) Legal; Bhattacharyya et al. (2023) Medical
5. **State-of-the-art**: Du et al. (2025) DeepResearch Bench for agentic systems

---

## Contributing Dataset Information

If you know of additional public benchmarks or datasets for citation fabrication:

1. **Verify the dataset is publicly available** (or open-access research upon request)
2. **Document the authors, DOI, and repository**
3. **Provide one-paragraph description** of purpose and use case
4. **Submit a pull request** with the information formatted like the entries above

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

---

**Last Updated:** 2026-09-30  
**Maintained by:** Bayyapu Vamshidhar Reddy
