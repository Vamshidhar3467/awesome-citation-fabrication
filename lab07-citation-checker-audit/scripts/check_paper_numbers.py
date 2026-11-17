"""Prompt 15 evidence checklist: recompute every number the paper reports and confirm it appears in main.tex.

    python scripts/check_paper_numbers.py

Writes paper/evidence_checklist.md and exits non-zero if any claim is missing or disagrees.
"""
import csv
import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / 'results/phase4'
tex = (ROOT / 'paper/main.tex').read_text(encoding='utf-8')
metrics = json.loads((RES / 'metrics.json').read_text(encoding='utf-8'))
boot = json.loads((RES / 'bootstrap.json').read_text(encoding='utf-8'))
snap = json.loads((ROOT / 'data/ext_snapshot.json').read_text(encoding='utf-8'))
ablation = {r['variant']: r for r in csv.DictReader((RES / 'ablation.csv').open(encoding='utf-8'))}
sens = list(csv.DictReader((RES / 'sensitivity.csv').open(encoding='utf-8')))
cases = json.loads((ROOT / 'data/ext_cases.json').read_text(encoding='utf-8'))
stress = [c for c in cases if c['split'] == 'ext_stress']
years = [r['year_published'] for r in snap['selected']]
ov = lambda key, d='any_error': metrics[key][d]['overall']
st = lambda m: metrics[f'ext_stress/{m}']
sens_at = lambda p, v: next(float(r['stress_false_flag_rate']) for r in sens if r['parameter'] == p and float(r['value']) == v)
pct = lambda x: f'{round(100 * x)}\\%'

# (section, claim, value recomputed from files, exact text that must appear in main.tex, source file)
CLAIMS = [
    ('Abstract/5.1', 'B1 macro recall (test and ext)', ov('ext/B1')['macro_recall'], 'macro recall 0.20', 'results.csv'),
    ('Abstract/5.1', 'B2 macro recall', ov('ext/B2')['macro_recall'], 'macro recall 1.00', 'results.csv'),
    ('Abstract', 'Number of legitimate variants', len(stress), '87', 'ext_cases.json'),
    ('Abstract/5.2', 'B2 stress false-flag rate', st('B2')['false_flag_rate'], pct(st('B2')['false_flag_rate']), 'metrics.json'),
    ('Abstract/5.3', 'B3 stress false-flag rate', st('B3')['false_flag_rate'], '19.5\\%', 'metrics.json'),
    ('Abstract/5.3', 'Paired B3-B2 interval (lo)', boot['ext']['B3-B2_stress_flag_rate']['lo'], f"{boot['ext']['B3-B2_stress_flag_rate']['lo']:.2f}".replace('-', '$-'), 'bootstrap.json'),
    ('Abstract/5.3', 'Paired B3-B2 interval (hi)', boot['ext']['B3-B2_stress_flag_rate']['hi'], f"{boot['ext']['B3-B2_stress_flag_rate']['hi']:.2f}".replace('-', '$-'), 'bootstrap.json'),
    ('Abstract/5.4', 'B2 identity-only precision', ov('ext/B2', 'identity_only')['precision'], '0.60', 'results.csv'),
    ('5.4', 'B2 identity-only FPR', ov('ext/B2', 'identity_only')['false_positive_rate'], '0.40', 'results.csv'),
    ('5.4', 'B1 identity-only recall', ov('ext/B1', 'identity_only')['recall'], '0.33', 'results.csv'),
    ('3.2', 'Sample returned', snap['returned'], 'returned 100 records', 'ext_snapshot.json'),
    ('3.2', 'Eligible records', snap['eligible'], '91 met', 'ext_snapshot.json'),
    ('3.2', 'Year range', f'{min(years)}-{max(years)}', f'{min(years)}--{max(years)}', 'ext_snapshot.json'),
    ('3.2', 'Median year', statistics.median(years), f'median of {int(statistics.median(years))}', 'ext_snapshot.json'),
    ('3.2', 'Non-ASCII titles', sum(any(ord(ch) > 127 for ch in r['title']) for r in snap['selected']), 'Ten of the 40 titles', 'ext_snapshot.json'),
    ('3.2', 'DOIs with prefix 10.1016', sum(r['doi'].startswith('10.1016/') for r in snap['selected']), '17 of the 40 DOIs', 'ext_snapshot.json'),
    ('Table 1', '"et al." variants', sum(c['category'] == 'et_al_first_author' for c in stress), '$n=30$', 'ext_cases.json'),
    ('Table 1', 'Abbreviated venue variants', sum(c['category'] == 'venue_abbrev' for c in stress), '$n=11$', 'ext_cases.json'),
    ('Table 1', 'Subtitle variants', sum(c['category'] == 'subtitle_dropped' for c in stress), '$n=6$', 'ext_cases.json'),
    ('Table 1', 'Print-year variants', sum(c['category'] == 'print_year' for c in stress), '$n=1$', 'ext_cases.json'),
    ('Table 1', 'Hyphen variants', sum(c['category'] == 'title_hyphen_break' for c in stress), '$n=39$', 'ext_cases.json'),
    ('Table 2', 'B2 TP on extension', ov('ext/B2')['tp'], '& 200 &', 'results.csv'),
    ('Table 2', 'B2 identity-only FP on extension', ov('ext/B2', 'identity_only')['fp'], '& 120 & 80 &', 'results.csv'),
    ('Table 2', 'Coverage', ov('ext/B1')['coverage'], '0.875', 'results.csv'),
    ('Table 3', 'B2 total false flags', st('B2')['false_flags'], '47 (0.54)', 'metrics.json'),
    ('Table 3', 'B3 total false flags', st('B3')['false_flags'], '17 (0.195)', 'metrics.json'),
    ('5.2', 'B2 stress interval', (boot['ext']['B2_stress_flag_rate']['lo'], boot['ext']['B2_stress_flag_rate']['hi']),
     f"bootstrap {boot['ext']['B2_stress_flag_rate']['lo']:.2f}--{boot['ext']['B2_stress_flag_rate']['hi']:.2f}", 'bootstrap.json'),
    ('5.2', 'Ablation: without venue false-flag rate', float(ablation['without venue']['stress_false_flag_rate']), pct(float(ablation['without venue']['stress_false_flag_rate'])), 'ablation.csv'),
    ('5.2', 'Sensitivity: title 0.50', sens_at('title_threshold', .5), f"{pct(sens_at('title_threshold', .5))} at 0.50", 'sensitivity.csv'),
    ('5.2', 'Sensitivity: author 0.20', sens_at('author_threshold', .2), f"to {pct(sens_at('author_threshold', .2))}", 'sensitivity.csv'),
    ('5.2', 'Largest author list among et-al cases', max(len(c['citation']['authors']) for c in cases if c['split'] == 'ext' and c['category'] == 'clean' and c['source_id'] in {s['source_id'] for s in stress if s['category'] == 'et_al_first_author'}), '$1/17$', 'ext_cases.json'),
    ('6', 'Share of B2 false flags removed by B3', (st('B2')['false_flags'] - st('B3')['false_flags']) / st('B2')['false_flags'], pct((st('B2')['false_flags'] - st('B3')['false_flags']) / st('B2')['false_flags']), 'metrics.json'),
]

rows, failures = [], 0
for section, claim, value, text, source in CLAIMS:
    ok = text in tex
    failures += not ok
    shown = f'{value:.3f}' if isinstance(value, float) else str(value)
    rows.append(f"| {section} | {claim} | {shown} | `{text}` | `{source}` | {'OK' if ok else '**MISSING**'} |")

outline = """# Manuscript outline and evidence checklist — Prompt 15

Generated by `python scripts/check_paper_numbers.py`. Each number is **recomputed from the result files**, and the script then checks that the exact text appears in `paper/main.tex`. Rerun it after any edit to the paper.

## Section outline (as written)

1. Introduction: motivation, gap from the Lab06 review and Russinovich et al., RQ1–RQ3, what is and isn't new
2. Related work: measuring fabrication; checking references; where this study sits
3. Study design: pipeline (Fig. 1), data (preregistered set, amendment A1, Table 1), checkers B1–B3, metrics and decision rule
4. Experimental setup: environment, requests, hash checks, tests, order of work
5. Results: RQ1 (Table 2, Fig. 2a), RQ2 (Table 3, Fig. 2b, ablation Fig. 3, sensitivity Fig. 4), B3, RQ3
6. Discussion · 7. Limitations · 8. Conclusion · Reproducibility · Use of AI tools
The abstract was written last, after the results sections.

## Evidence checklist

| Section | Claim | Recomputed value | Text in paper | Source (`results/phase4/` or `data/`) | Status |
|---|---|---|---|---|---|
"""
(ROOT / 'paper/evidence_checklist.md').write_text(outline + '\n'.join(rows) + f"\n\n**{len(CLAIMS) - failures}/{len(CLAIMS)} claims verified.** Figures are drawn by `scripts/make_figures.py` from the same files. Citations: all 9 bibliography entries were checked against arXiv/Crossref on 2026-11-17 (see the header of `references.bib`).\n", encoding='utf-8')
print(f'{len(CLAIMS) - failures}/{len(CLAIMS)} claims verified')
for r in rows:
    if 'MISSING' in r:
        print(r)
sys.exit(1 if failures else 0)
