# Citation Fabrication Detection and Verification Tools

A curated list of tools, libraries, and APIs for detecting, preventing, and mitigating citation fabrication in LLM-generated content.

## Citation Verification APIs

### 1. CrossRef API

| Property | Details |
|----------|---------|
| **Service** | CrossRef — The Official DOI Registration Agency |
| **URL** | [crossref.org/services/retrieve-metadata](https://www.crossref.org/services/retrieve-metadata) |
| **Authentication** | Free (basic) and premium (high-volume) tiers |
| **Language** | REST API (JSON responses) |
| **Rate Limit** | 50 requests/second (free tier) |

**Purpose:**  
Retrieve bibliographic metadata for any DOI. Essential for verifying publication details (authors, title, venue, year).

**Common Use Cases:**
- Resolve DOI → full citation metadata
- Search for works by author-year-title combination
- Verify journal/conference affiliation
- Check publication date authenticity

**Example Query:**
```
https://api.crossref.org/works/10.1038/s41598-023-41032-5
```

**Limitations:**
- Requires DOI or exact metadata to search
- Does not verify URL destinations
- Coverage: primarily peer-reviewed publications

---

### 2. Semantic Scholar API

| Property | Details |
|----------|---------|
| **Service** | Semantic Scholar — AI-powered research paper search |
| **URL** | [semanticscholar.org/product/api](https://www.semanticscholar.org/product/api) |
| **Authentication** | Free API key (register on website) |
| **Language** | REST API (JSON) |
| **Rate Limit** | 100 requests/5 minutes (free tier) |

**Purpose:**  
Search for academic papers by title, author, or keyword. Provides: title, authors, venue, year, abstract, PDF availability, citation count.

**Advantages:**
- Fuzzy matching for titles (tolerant of minor variations)
- Integrates with arXiv, PubMed, Google Scholar
- Returns citation graph (papers citing this work, papers cited by this work)
- Identifies paper availability (open-access links)

**Example Use:**
```json
{
  "queryString": "citation fabrication",
  "year": 2023,
  "openAccessPdf": true
}
```

**Limitations:**
- Coverage gap for very recent papers
- Cannot verify specific URL destinations
- Some metadata may be incomplete for non-English papers

---

### 3. OpenAlex API

| Property | Details |
|----------|---------|
| **Service** | OpenAlex — Open-source Academic Graph |
| **URL** | [openalex.org](https://openalex.org) |
| **Authentication** | Free (no key required) |
| **Language** | REST API (JSON) |
| **Data Format** | Linked Open Data, RDF |

**Purpose:**  
Query comprehensive academic metadata: works, authors, venues, institutions, and their relationships.

**Coverage:**
- 250+ million works
- 50+ million authors
- 100,000+ venues/journals
- Institutional affiliations

**Example Use Cases:**
- Verify author-publication associations
- Check journal/conference scope and ranking
- Identify co-authorship networks
- Track publication venue migrations (e.g., conference moving venues)

**Data Quality:**
- Community-curated; contributions welcome
- Merges data from Crossref, PubMed, arXiv, MAG

---

### 4. PubMed E-utilities (NIH)

| Property | Details |
|----------|---------|
| **Service** | PubMed Central / MEDLINE — National Library of Medicine |
| **URL** | [ncbi.nlm.nih.gov/books/NBK25499/](https://www.ncbi.nlm.nih.gov/books/NBK25499/) |
| **Authentication** | Free (no API key required) |
| **Language** | REST API (XML/JSON) |
| **Rate Limit** | 3 requests/second (public) |

**Purpose:**  
Query MEDLINE and PubMed Central for biomedical/life science publications. Over 38 million records.

**Identifiers Supported:**
- PMID (PubMed ID)
- PMCID (PubMed Central ID)
- DOI
- Author-year-title search

**Example Endpoints:**
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=autism&retmax=10
```

**Domain-Specific Features:**
- Mesh subject headings (medical taxonomy)
- Citation relationships
- Full-text availability status
- Open access indicators

---

### 5. arXiv API

| Property | Details |
|----------|---------|
| **Service** | arXiv — Preprint Repository for Physics, Math, CS, etc. |
| **URL** | [info.arxiv.org/help/api](https://info.arxiv.org/help/api) |
| **Authentication** | Free (no API key required) |
| **Language** | XML query/response |
| **Rate Limit** | 3 requests/second (advertised; be respectful) |

**Purpose:**  
Retrieve metadata and full-text papers from arXiv (240,000+ new papers/year in CS, ML, math, physics).

**Search Capabilities:**
- Query by arXiv ID
- Full-text search (title, authors, abstract)
- Categorical search
- Submission date filtering

**Example Query:**
```
http://export.arxiv.org/api/query?search_query=cat:cs.CL%20AND%20submittedDate:[202301010000%20TO%20202312312359]
```

**Use in Citation Verification:**
- Check if preprint version exists (preprints often precede peer review)
- Verify author names and publication dates
- Detect arXiv-specific fabrications (fake arXiv IDs)

---

## Hallucination Detection Tools

### 1. RefChecker: Reference-Based Hallucination Checker

| Property | Details |
|----------|---------|
| **Authors** | Hu, X., Ru, D., Qiu, L., et al., 2024 |
| **GitHub** | [github.com/refchecker](https://github.com/refchecker) (check for availability) |
| **Language** | Python (PyTorch, Transformers) |
| **License** | Apache 2.0 |
| **Paper** | arXiv:2405.14486 |

**Purpose:**  
Automated checker that:
1. Extracts references from LLM-generated text
2. Retrieves candidate papers using retrieval engine
3. Computes similarity between citation context and retrieved papers
4. Flags low-confidence matches as potential hallucinations

**Input:**
- LLM output text with inline or end-note citations
- Reference list or DOI links

**Output:**
- Per-citation confidence score
- Hallucination risk flagging
- Alternative suggestions for mismatched citations

**Advantages:**
- Fine-grained (per-citation) detection
- Provides confidence scores
- Suggests corrections

**Limitations:**
- Requires retrieval corpus (cannot work for obscure papers)
- May have false positives for niche/specialized work

---

### 2. SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection

| Property | Details |
|----------|---------|
| **Authors** | Manakul, P., Liusie, A., & Gales, M., 2023 |
| **GitHub** | [github.com/potsawee/selfcheckgpt](https://github.com/potsawee/selfcheckgpt) |
| **Language** | Python |
| **License** | MIT |
| **Venue** | EMNLP 2023 |

**Purpose:**  
Detect hallucinations without external knowledge bases. Generates multiple completions for the same prompt and checks for consistency across generations.

**Method:**
1. Generate N samples from LLM with same prompt
2. Compute token-level agreement across samples
3. Low agreement → likely hallucination
4. High agreement → likely factual

**Advantages:**
- No external API calls needed (black-box compatible)
- Works for any LLM and domain
- Computationally efficient

**Limitations:**
- Cannot distinguish between common hallucinations (repeated false "knowledge")
- Requires multiple model calls (higher cost)
- May struggle with ambiguous claims

**Example:**
```python
from selfcheckgpt.modeling_selfcheck import SelfCheckGPT
checker = SelfCheckGPT(model_name="gpt-3.5-turbo")
scores = checker.check_text(generated_text)
```

---

### 3. FActScore: Factual Precision Evaluation

| Property | Details |
|----------|---------|
| **Authors** | Min, S., Krishna, K., Lyu, X., et al., 2023 |
| **GitHub** | [github.com/shmsw25/FActScore](https://github.com/shmsw25/FActScore) |
| **Language** | Python (with OpenAI API integration) |
| **License** | MIT |
| **Venue** | EMNLP 2023 |

**Purpose:**  
Fine-grained atomic evaluation of factual precision. Breaks down generated text into individual facts and verifies each independently.

**Method:**
1. Parse generated text → atomic facts
2. Retrieve supporting documents for each fact
3. Assign binary score (supported/unsupported)
4. Compute overall factuality score

**Advantages:**
- Granular (per-fact) analysis
- Clear interpretability
- Provides reasoning for each fact

**Limitations:**
- Requires high-quality retrieval corpus
- May overcount or undercount facts
- Sensitive to fact parsing quality

**Python Example:**
```python
from factscore.factscorer import FactScorer
scorer = FactScorer(model_name="retrieval+gpt3.5")
score, all_facts = scorer.score(generated_text)
```

---

## URL and Link Verification Tools

### 1. Wayback Machine API

| Property | Details |
|----------|---------|
| **Service** | Internet Archive Wayback Machine |
| **URL** | [archive.org/help/memento_api.php](https://archive.org/help/memento_api.php) |
| **Authentication** | Free (no API key required) |
| **Language** | REST API (JSON) |
| **Advantage** | Detects links that worked when cited but are now broken |

**Purpose:**  
Check historical availability of URLs. Determines if a URL was accessible at the time the citation was created.

**Use Case:**
```
https://archive.org/wayback/available?url=example.com/paper&timestamp=20230615
```

**Output:**
- Snapshot date closest to query date
- Status (archived, not archived)
- Web.archive.org link to snapshot

**Limitations:**
- Only covers archived snapshots
- May not archive paywall-protected content
- Doesn't verify content authenticity

---

### 2. LinkChecker

| Property | Details |
|----------|---------|
| **Tool** | LinkChecker — Link validation utility |
| **Language** | Python |
| **Repository** | [github.com/wummel/linkchecker](https://github.com/wummel/linkchecker) |
| **Installation** | `pip install linkchecker` |

**Purpose:**  
Batch verify HTTP(S) links in documents. Check if URLs are currently accessible and report status codes.

**Features:**
- Recursive link checking
- Supports robots.txt
- Generates reports (HTML, text, CSV)
- Configurable timeout and retry

**Example:**
```bash
linkchecker README.md --output html > link_report.html
```

---

## Machine Learning Models for Citation Analysis

### 1. SciBERT

| Property | Details |
|----------|---------|
| **Model** | Specialized BERT for Scientific Text |
| **Authors** | Beltagy, I., Lo, K., & Cohan, A., 2019 |
| **Hub** | [huggingface.co/allenai/scibert-base-uncased](https://huggingface.co/allenai/scibert-base-uncased) |
| **Language** | PyTorch / Hugging Face Transformers |
| **Use Case** | Named entity recognition (authors, venues), relation extraction |

**Purpose:**  
Pre-trained BERT model on scientific papers. Effective for:
- Extracting citations from text
- Identifying author and venue mentions
- Relation extraction (who published where when)

---

### 2. BioBERT

| Property | Details |
|----------|---------|
| **Model** | BERT fine-tuned on Biomedical Literature |
| **Authors** | Lee, J., et al., 2020 |
| **Hub** | [huggingface.co/dmis-lab/biobert-base-cased-v1.2](https://huggingface.co/dmis-lab/biobert-base-cased-v1.2) |
| **Use Case** | Medical NER, biomedical citation analysis |

**Purpose:**  
Domain-optimized for biomedicine. Useful for:
- Extracting drug names, gene mentions, diseases
- Verifying biomedical citations against domain knowledge
- Medical literature mining

---

## LLM Evaluation Frameworks

### 1. HELM: Holistic Evaluation of LM Performance

| Property | Details |
|----------|---------|
| **Project** | Stanford CRFM |
| **URL** | [crfm.stanford.edu/helm](https://crfm.stanford.edu/helm) |
| **Scope** | 50+ models, 16 scenarios (including factuality) |
| **Language** | Benchmark suite (model-agnostic) |

**Purpose:**  
Comprehensive benchmark suite evaluating LLMs on factuality, calibration, bias, and other dimensions. Includes citation-specific metrics.

**Coverage:**
- Factuality (closed-book QA, open-book QA)
- Toxicity and bias
- Robustness and uncertainty

---

### 2. LitReview & Citation Analysis Tools

| Tool | Purpose | Link |
|------|---------|------|
| **CoReference** | Coreference resolution in citations | [github.com/coreference-tools](https://github.com/coreference-tools) |
| **Anystyle** | Bibliographic reference parsing | [anystyle.io](https://anystyle.io) |
| **Grobid** | Machine learning for PDF extraction | [github.com/kermitt2/grobid](https://github.com/kermitt2/grobid) |
| **Cermine** | Citation and metadata extraction from PDFs | [github.com/CeON/CERMINE](https://github.com/CeON/CERMINE) |

---

## Integration Pipelines

### DIY Citation Verification Pipeline (Python)

A minimal example pipeline combining multiple tools:

```python
import requests
import json
from datetime import datetime

class CitationVerifier:
    def __init__(self):
        self.crossref_url = "https://api.crossref.org/works"
        self.semantic_scholar_url = "https://api.semanticscholar.org/graph/v1/paper/search"
    
    def verify_by_doi(self, doi):
        """Verify citation by DOI"""
        response = requests.get(f"{self.crossref_url}/{doi}")
        if response.status_code == 200:
            return response.json()
        return None
    
    def verify_by_metadata(self, title, authors, year):
        """Verify citation by title, authors, year"""
        query = f"{title} {' '.join(authors)}"
        params = {
            "query": query,
            "year": year,
            "limit": 1
        }
        response = requests.get(f"{self.semantic_scholar_url}", params=params)
        if response.status_code == 200:
            results = response.json().get('data', [])
            if results:
                return results[0]
        return None
    
    def check_url_availability(self, url):
        """Check if URL is currently accessible"""
        try:
            response = requests.head(url, timeout=5, allow_redirects=True)
            return response.status_code in [200, 301, 302, 303]
        except:
            return False

# Usage
verifier = CitationVerifier()
doi_result = verifier.verify_by_doi("10.1038/s41598-023-41032-5")
print(json.dumps(doi_result, indent=2))
```

---

## Recommended Tool Combinations

| Use Case | Recommended Tools | Rationale |
|----------|-------------------|-----------|
| **Quick verification** | CrossRef + Semantic Scholar | Fast, no local setup needed |
| **Medical citations** | PubMed + CrossRef | Authoritative for biomedical domain |
| **Legal citations** | Legal databases (LexisNexis, Google Scholar) | Specialized jurisdiction indexing |
| **Batch verification** | LinkChecker + CrossRef API + custom script | Automated verification of large reference lists |
| **Hallucination detection** | RefChecker + SelfCheckGPT | Complementary approaches (reference-based + consistency-based) |
| **Agentic system audit** | DeepResearch Bench dataset + Wayback Machine | Evaluate both URL and content availability |

---

## Contributing Tool Information

If you discover or develop a tool for citation fabrication detection:

1. Provide the **official repository/website**
2. Document **installation instructions**
3. Explain **purpose and use case**
4. Include **code examples** if applicable
5. Note any **dependencies or API key requirements**
6. Submit via pull request

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

---

**Last Updated:** 2026-09-30  
**Maintained by:** Bayyapu Vamshidhar Reddy
