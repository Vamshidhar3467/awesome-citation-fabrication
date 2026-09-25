# GitHub Implementations and Reference Repositories

A curated list of open-source implementations, code repositories, and GitHub projects relevant to citation fabrication detection, verification, and LLM evaluation.

## Official Benchmark and Tool Repositories

### 1. ALCE: Annotated Long-Form Citation Evaluation

| Property | Details |
|----------|---------|
| **Repository** | [github.com/haesungpyun/alce](https://github.com/haesungpyun/alce) |
| **Authors** | Liu, N. F., Zhang, T., & Liang, P., 2023 |
| **Language** | Python |
| **License** | Apache 2.0 |
| **Stars** | 100+ (at time of curation) |

**What It Implements:**
- Benchmark dataset for citation-grounded generation evaluation
- Metrics for measuring citation precision and recall
- Evaluation scripts for generative search engines
- Contains ELIS, ELI5, ASQA, and BiPAR datasets

**Folder Structure:**
```
alce/
├── README.md
├── eval_scripts/
│   ├── eval_citation_precision.py
│   ├── eval_citation_recall.py
│   └── eval_citation_f1.py
├── datasets/
│   ├── elis/
│   ├── eli5/
│   └── asqa/
└── baseline_results/
```

**How to Use:**
1. Clone repository
2. Install dependencies: `pip install -r requirements.txt`
3. Prepare your model outputs in the required format
4. Run evaluation: `python eval_scripts/eval_citation_precision.py --predictions <file>`

**Relevant Paper:** Liu et al., 2023 (Findings of EMNLP 2023)

---

### 2. FActScore: Fine-Grained Atomic Fact Scoring

| Property | Details |
|----------|---------|
| **Repository** | [github.com/shmsw25/FActScore](https://github.com/shmsw25/FActScore) |
| **Authors** | Min, S., Krishna, K., Lyu, X., et al., 2023 |
| **Language** | Python (PyTorch, OpenAI API) |
| **License** | MIT |
| **Stars** | 200+ (at time of curation) |

**What It Implements:**
- Automated factuality scorer for long-form generation
- Fact extraction and atomic-level scoring
- Integration with OpenAI GPT models
- Benchmark datasets for evaluation

**Key Files:**
- `factscorer.py` — Main scoring class
- `fact_extractor.py` — Decomposes text into atomic facts
- `eval_scripts/` — Evaluation on OPENBIO and other benchmarks
- `dataset/` — Benchmark QA and gold answer pairs

**Installation:**
```bash
git clone https://github.com/shmsw25/FActScore
pip install -r requirements.txt
export OPENAI_API_KEY="your-api-key"
```

**Quick Start:**
```python
from factscore.factscorer import FactScorer
scorer = FactScorer(model_name="retrieval+gpt3.5")
score, all_facts = scorer.score("Your generated text here")
```

**Relevant Paper:** Min et al., 2023 (EMNLP 2023)

---

### 3. RefChecker: Reference-Based Hallucination Checking

| Property | Details |
|----------|---------|
| **Repository** | [github.com/refchecker/refchecker](https://github.com/refchecker/refchecker) |
| **Authors** | Hu, X., Ru, D., Qiu, L., et al., 2024 |
| **Language** | Python (PyTorch, Transformers) |
| **License** | Apache 2.0 |

**What It Implements:**
- Per-citation hallucination detection
- Reference extraction from LLM outputs
- Confidence scoring for individual citations
- Integration with dense retrieval models (DPR, ColBERT)

**Architecture:**
```
refchecker/
├── models/
│   ├── reference_extractor.py
│   ├── dense_retriever.py
│   └── confidence_scorer.py
├── data/
│   ├── benchmarks/
│   └── evaluation_sets/
└── eval.py
```

**Key Components:**
- **Reference Extractor**: Uses regex + NER to find citations in text
- **Dense Retriever**: Finds candidate papers using contrastive learning
- **Confidence Scorer**: Computes match quality between citation context and retrieved paper

**Usage:**
```python
from refchecker import ReferenceChecker
checker = ReferenceChecker(model_type="colbert")
results = checker.check(text="Generated text with [1] citations",
                       reference_list=ref_list)
# Returns per-citation confidence scores and hallucination flags
```

**Relevant Paper:** Hu et al., 2024 (arXiv:2405.14486)

---

### 4. SelfCheckGPT: Zero-Resource Hallucination Detection

| Property | Details |
|----------|---------|
| **Repository** | [github.com/potsawee/selfcheckgpt](https://github.com/potsawee/selfcheckgpt) |
| **Authors** | Manakul, P., Liusie, A., & Gales, M., 2023 |
| **Language** | Python |
| **License** | MIT |
| **Stars** | 150+ (at time of curation) |

**What It Implements:**
- Black-box hallucination detection (no external knowledge required)
- Multi-sample consistency checking
- Zero-resource approach (works with any LLM)
- Efficient token-level agreement computation

**Code Structure:**
```
selfcheckgpt/
├── README.md
├── selfcheckgpt/
│   ├── __init__.py
│   ├── modeling_selfcheck.py
│   └── utils.py
├── run_inference.py
└── evaluate.py
```

**Main Features:**
```python
from selfcheckgpt.modeling_selfcheck import SelfCheckGPT

# Initialize with any LLM
scorer = SelfCheckGPT(model_name="gpt-3.5-turbo")

# Score generated text
text = "Large language models are trained on ... "
scores = scorer.check_text(text)

# Returns: token-level scores and document-level hallucination score
```

**Advantages:**
- No API calls to external services
- Works for any domain
- Minimal computational overhead

**Relevant Paper:** Manakul et al., 2023 (EMNLP 2023)

---

## Core NLP and ML Libraries

### 5. Hugging Face Transformers

| Property | Details |
|----------|---------|
| **Repository** | [github.com/huggingface/transformers](https://github.com/huggingface/transformers) |
| **Language** | Python (PyTorch, TensorFlow) |
| **License** | Apache 2.0 |
| **Stars** | 100,000+ |

**Relevance to Citation Fabrication:**
- Provides SciBERT, BioBERT, and other domain-specific models
- Text extraction and named entity recognition (NER)
- Question-answering models for claim verification
- Fine-tuning tools for domain adaptation

**Useful for Citation Tasks:**
```python
from transformers import AutoTokenizer, AutoModelForTokenClassification
# Use for author extraction, venue recognition, etc.
model_name = "allenai/scibert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
```

---

### 6. Hugging Face Datasets

| Property | Details |
|----------|---------|
| **Repository** | [github.com/huggingface/datasets](https://github.com/huggingface/datasets) |
| **Language** | Python |
| **License** | Apache 2.0 |

**Relevance:**
- Provides standardized dataset loading for benchmarks
- ALCE, FActScore datasets available
- OpenWebText, Wikipedia data for retrieval

---

### 7. FAISS: Facebook AI Similarity Search

| Property | Details |
|----------|---------|
| **Repository** | [github.com/facebookresearch/faiss](https://github.com/facebookresearch/faiss) |
| **Language** | C++ (Python bindings) |
| **License** | MIT |

**Purpose:**
- Efficient similarity search in high-dimensional spaces
- Dense retrieval for citation verification
- Scales to millions of papers

**Use in Citation Systems:**
```python
import faiss
# Build index over paper embeddings
index = faiss.IndexFlatL2(d)
index.add(np.array(embeddings))
# Search for similar papers to verify citations
distances, indices = index.search(query_embedding, k=5)
```

---

### 8. Qdrant: Vector Database

| Property | Details |
|----------|---------|
| **Repository** | [github.com/qdrant/qdrant](https://github.com/qdrant/qdrant) |
| **Language** | Rust (with Python SDK) |
| **License** | AGPL-3.0 / Proprietary |

**Purpose:**
- Production-grade vector database
- Similarity search for citation retrieval
- Supports filtering and metadata

**Citation Use Case:**
```python
from qdrant_client import QdrantClient
client = QdrantClient()
# Store paper embeddings and metadata
client.upsert(collection_name="papers",
              points=[Point(id=i, vector=emb, payload={...})])
# Query for similar papers
results = client.search(collection_name="papers",
                        query_vector=citation_embedding)
```

---

## NLP and Information Extraction

### 9. spaCy: Industrial-Strength NLP

| Property | Details |
|----------|---------|
| **Repository** | [github.com/explosion/spacy](https://github.com/explosion/spacy) |
| **Language** | Python (Cython core) |
| **License** | MIT |

**Citation Extraction Uses:**
- Named Entity Recognition (authors, venues, dates)
- Dependency parsing for claim-evidence relationship
- Entity linking to knowledge bases

**Example: Extract citation metadata**
```python
import spacy
nlp = spacy.load("en_core_sci_md")
doc = nlp("Bhattacharyya et al. (2023) published in Cureus")
for ent in doc.ents:
    if ent.label_ == "PERSON":
        print(f"Author: {ent.text}")
```

---

### 10. AllenNLP: Natural Language Understanding

| Property | Details |
|----------|---------|
| **Repository** | [github.com/allenai/allennlp](https://github.com/allenai/allennlp) |
| **Language** | Python (PyTorch) |
| **License** | Apache 2.0 |

**Relevance:**
- Semantic role labeling (identify claims and evidence)
- Reading comprehension (check if citation supports claim)
- SRL models trained on scientific text

---

## Specialized Academic Tools

### 11. Grobid: PDF Extraction for Bibliographies

| Property | Details |
|----------|---------|
| **Repository** | [github.com/kermitt2/grobid](https://github.com/kermitt2/grobid) |
| **Language** | Java |
| **License** | Apache 2.0 |

**Purpose:**
- Extract citations from PDF papers
- Parse bibliographic metadata
- Layout analysis for document understanding

**Use Case:**
```bash
# REST API for PDF processing
curl -X POST --form "input=@paper.pdf" \
  http://localhost:8070/api/processReferences
```

---

### 12. Cermine: Citation Extraction from PDFs

| Property | Details |
|----------|---------|
| **Repository** | [github.com/CeON/CERMINE](https://github.com/CeON/CERMINE) |
| **Language** | Java |
| **License** | Apache 2.0 |

**Purpose:**
- Structured metadata extraction from academic papers
- Citation parsing and normalization
- Machine learning-based document analysis

---

### 13. Anystyle: Bibliographic Reference Parsing

| Property | Details |
|----------|---------|
| **Repository** | [github.com/inukshuk/anystyle](https://github.com/inukshuk/anystyle) |
| **Language** | Ruby (with command-line and API) |
| **License** | AGPL-3.0 |
| **Online Tool** | [anystyle.io](https://anystyle.io) |

**Purpose:**
- Parse unstructured bibliographic references
- Extract authors, titles, years, venues from messy citation strings
- Normalize citation formats

**Usage:**
```bash
anystyle -p [input_file] [output_file]
# or online via web interface
```

---

## LLM Evaluation and Benchmarking

### 14. LiteLLM: Model Agnostic LLM Calls

| Property | Details |
|----------|---------|
| **Repository** | [github.com/BerriAI/litellm](https://github.com/BerriAI/litellm) |
| **Language** | Python |
| **License** | MIT |

**Purpose:**
- Unified interface for calling different LLMs (OpenAI, Anthropic, Hugging Face, etc.)
- Useful for benchmarking fabrication across multiple models
- Token counting and cost tracking

```python
from litellm import completion

# Test same prompt across models
for model in ["gpt-3.5-turbo", "gpt-4", "claude-2"]:
    response = completion(model=model, messages=messages)
    # Compare citation fabrication rates
```

---

### 15. HELM: Holistic Evaluation Framework

| Property | Details |
|----------|---------|
| **Repository** | [github.com/stanford-crfm/helm](https://github.com/stanford-crfm/helm) |
| **Language** | Python |
| **License** | Apache 2.0 |

**Purpose:**
- Comprehensive LLM evaluation framework
- Measures factuality, robustness, bias, and other dimensions
- Evaluation scripts for citation-related benchmarks

---

## Utility and Helper Tools

### 16. LinkChecker: URL Validation

| Property | Details |
|----------|---------|
| **Repository** | [github.com/wummel/linkchecker](https://github.com/wummel/linkchecker) |
| **Language** | Python |
| **License** | GPL |

**Purpose:**
- Batch verification of URLs in documents
- Check citation link validity
- Generate reports on broken links

```bash
linkchecker references.md --output html > broken_links_report.html
```

---

### 17. Python Requests Library

| Property | Details |
|----------|---------|
| **Repository** | [github.com/psf/requests](https://github.com/psf/requests) |
| **Language** | Python |
| **License** | Apache 2.0 |

**Purpose:**
- HTTP requests for API integration
- Fetch pages and check availability
- Query CrossRef, Semantic Scholar, PubMed APIs

---

## Database and Knowledge Graph Tools

### 18. Neo4j: Graph Database

| Property | Details |
|----------|---------|
| **Repository** | [github.com/neo4j/neo4j](https://github.com/neo4j/neo4j) |
| **Language** | Java |
| **License** | AGPL-3.0 / Proprietary |

**Citation Use Case:**
- Model author-paper-venue relationships
- Track citation networks
- Detect anomalies (e.g., sudden spike in citations to fabricated works)

---

## Recommended Implementation Stacks

| Task | Recommended Stack | Rationale |
|------|-------------------|-----------|
| **Academic Paper Analysis** | Grobid + Anystyle + Transformers | Extract metadata from PDFs and normalize citations |
| **Citation Verification** | ALCE + RefChecker + CrossRef API | Structured evaluation of citation support |
| **Hallucination Detection** | FActScore + SelfCheckGPT + FAISS | Multi-approach detection (atomic facts + consistency + retrieval) |
| **Large-Scale Audit** | LinkChecker + PubMed API + OpenAlex API | Batch verification of large reference sets |
| **End-to-End Pipeline** | Transformers (BERT) + Qdrant + LiteLLM | Full citation generation and verification system |

---

## Contributing Repository Information

When suggesting a GitHub repository for this list:

1. Ensure the **repository is actively maintained** (recent commits or stable release)
2. Provide the **GitHub URL** and primary **programming language**
3. Explain **how it relates to citation fabrication detection or verification**
4. Note any **prerequisites or dependencies** (API keys, special hardware, etc.)
5. Include a **usage example** if applicable

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed contribution guidelines.

---

## Repository Activity Snapshot

*These repositories represent active research and development in LLM evaluation and citation verification. Activity and star counts are approximate as of September 2026.*

| Category | Repository Count | Actively Maintained |
|----------|------------------|-------------------|
| Official Benchmarks | 4 | ✅ Yes |
| NLP Libraries | 5 | ✅ Yes |
| Detection Tools | 4 | ✅ Yes |
| Utilities | 3 | ✅ Yes |
| **Total** | **16+** | **Mostly active** |

---

**Last Updated:** 2026-09-30  
**Maintained by:** Bayyapu Vamshidhar Reddy  
**Next Review:** 2027-03-30
