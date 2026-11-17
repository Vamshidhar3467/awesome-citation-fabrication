# Data

Everything here is either a bibliographic fact from the Crossref REST API or a citation variant generated from those facts by code in `src/citationlab.py`. There are no abstracts, full text, personal data or keys.

| File | Contents | Made by |
|---|---|---|
| `cache/<sha256>.json` | One registry lookup per DOI (title, author surnames, year, venue, request URL, retrieval time) or a real `found: false` 404 record. The filename is the SHA-256 of the normalized, lower-cased DOI | `fetch_record` (online once, offline afterwards) |
| `sources.json` | The 12 preregistered works | `scripts/run.py acquire` |
| `cases.json` | 96 preregistered cases: 4 pilot and 8 test works × 8 variants, with labels | `scripts/run.py acquire` |
| `manifest.json` | Hashes of the frozen protocol and `cases.json` | `scripts/run.py acquire` |
| `ext_snapshot.json` | The one random Crossref `sample` draw (100 returned, 91 eligible, 40 selected), with extra fields used only for legitimate variants (`short_venue`, `print_year`, `online_year`). **This is the frozen artifact. The sample can't be redrawn** | `scripts/acquire_ext.py` (online once) |
| `ext_cases.json` | 320 extension cases (40 works × 8 variants) and 87 legitimate-variant ("stress") cases | `scripts/acquire_ext.py --offline` |
| `ext_manifest.json` | Hashes of the snapshot and `ext_cases.json`, plus counts per stress category | same |

**Splits.** Pilot, test and extension use disjoint source works, and donors for wrong-DOI and Frankenstein cases come from the same split. `validate_cases` enforces both. Stress cases reuse the extension works on purpose and are scored separately.

**Labels** are a mutation ledger, not an independent expert judgement. They're visible in these files for auditing but never passed to a checker. Evaluation scripts check every hash before scoring.

**Known registry quirks** (kept as supplied, discussed in the paper): some titles contain U+FFFD replacement characters, one venue is stored with an un-decoded `&amp;`, and some records carry online dates decades after print (later digitisation).
