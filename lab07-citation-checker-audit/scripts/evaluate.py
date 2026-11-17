"""Phase IV evaluation (Prompt 13). Offline only; reads frozen cases and the lookup cache.

    python scripts/evaluate.py --pilot-only   # development check of code paths (A1.6)
    python scripts/evaluate.py                # all held-out evaluations, run once

Outputs go to results/phase4/. Every number in the paper comes from these files.
"""
import csv
import hashlib
import json
import random
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from citationlab import (ERROR_CATEGORIES, IDENTITY_CATEGORIES, METADATA_FIELDS, STRESS_CATEGORIES,
                         fetch_record, metrics, predict, validate_cases)

OUT = ROOT / 'results/phase4'
METHODS = {'B1': ('doi_only', {}), 'B2': ('metadata_check', {}), 'B3': ('metadata_containment', {})}
BOOT_SEED, BOOT_N = 20261117, 2000


def digest(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def load_cases(pilot_only):
    manifest = json.loads((ROOT / 'data/manifest.json').read_text())
    ext_manifest = json.loads((ROOT / 'data/ext_manifest.json').read_text())
    for expected, path in [(manifest['protocol_sha256'], 'configs/protocol.json'),
                           (manifest['cases_sha256'], 'data/cases.json'),
                           (ext_manifest['snapshot_sha256'], 'data/ext_snapshot.json'),
                           (ext_manifest['ext_cases_sha256'], 'data/ext_cases.json')]:
        if digest(path) != expected:
            raise ValueError(f'Frozen file changed: {path}')
    cases = json.loads((ROOT / 'data/cases.json').read_text(encoding='utf-8'))
    cases += json.loads((ROOT / 'data/ext_cases.json').read_text(encoding='utf-8'))
    validate_cases(cases)
    return [c for c in cases if c['split'] == 'pilot'] if pilot_only else cases


def run(cases, method, config=None):
    cache = ROOT / 'data/cache'
    lookup = lambda doi: fetch_record(doi, cache, offline=True)
    rows = []
    for case in cases:
        p = predict(case['citation'], lookup, method, config)
        rows.append({'split': case['split'], 'id': case['id'], 'source_id': case['source_id'],
                     'category': case['category'], 'truth_any': case['labels']['any_error'],
                     'truth_identity': case['labels']['identity_only'], **p})
    return rows


def check_alignment(rows, cases):
    """Prompt 13 audit: IDs, labels and decisions line up before any metric is computed."""
    by_id = {c['id']: c for c in cases}
    if len(rows) != len(cases) or len({r['id'] for r in rows}) != len(rows):
        raise AssertionError('Row/case count or duplicate-ID mismatch')
    for r in rows:
        c = by_id[r['id']]
        if r['truth_any'] != c['labels']['any_error'] or r['truth_identity'] != c['labels']['identity_only']:
            raise AssertionError(f"Label misalignment at {r['id']}")
        if r['decision'] not in ('pass', 'flag', 'abstain') or not r['reason']:
            raise AssertionError(f"Missing/invalid decision at {r['id']}")
        if r['split'].endswith('_stress') and (r['truth_any'] or r['category'] not in STRESS_CATEGORIES):
            raise AssertionError('Stress cases must be valid negatives')


def score(rows, definition='any'):
    key = 'truth_' + definition
    positives = ERROR_CATEGORIES if definition == 'any' else IDENTITY_CATEGORIES
    scored = [dict(r, truth=r[key]) for r in rows]
    overall = metrics(scored)
    per_cat = {c: metrics([r for r in scored if r['category'] == c]) for c in sorted({r['category'] for r in scored})}
    recalls = [per_cat[c]['recall'] for c in positives if c in per_cat and per_cat[c]['recall'] is not None]
    overall['macro_recall'] = sum(recalls) / len(recalls) if recalls else None
    return {'overall': overall, 'per_category': per_cat}


def flag_rate(rows):
    return sum(r['decision'] == 'flag' for r in rows) / len(rows) if rows else None


def bootstrap(rows_by_method, pairs, stress_by_method=None):
    """Source-clustered percentile bootstrap; whole source works are resampled together."""
    rng = random.Random(BOOT_SEED)
    sources = sorted({r['source_id'] for r in next(iter(rows_by_method.values()))})
    index = {m: {} for m in rows_by_method}
    for m, rows in rows_by_method.items():
        for r in rows:
            index[m].setdefault(r['source_id'], []).append(r)
    s_index = {m: {} for m in (stress_by_method or {})}
    for m, rows in (stress_by_method or {}).items():
        for r in rows:
            s_index[m].setdefault(r['source_id'], []).append(r)
    draws = {k: [] for k in [f'{m}_macro_recall' for m in rows_by_method] + [f'{m}_fpr' for m in rows_by_method]
             + [f'{a}-{b}_macro_recall' for a, b in pairs] + [f'{a}-{b}_fpr' for a, b in pairs]
             + [f'{m}_stress_flag_rate' for m in s_index] + [f'{a}-{b}_stress_flag_rate' for a, b in pairs if s_index]}
    for _ in range(BOOT_N):
        pick = [rng.choice(sources) for _ in sources]
        stats = {}
        for m in rows_by_method:
            sample = [r for s in pick for r in index[m][s]]
            res = score(sample)['overall']
            stats[m] = (res['macro_recall'], res['false_positive_rate'])
            draws[f'{m}_macro_recall'].append(res['macro_recall'])
            draws[f'{m}_fpr'].append(res['false_positive_rate'])
        for m in s_index:
            stats[m + 's'] = flag_rate([r for s in pick for r in s_index[m].get(s, [])])
            draws[f'{m}_stress_flag_rate'].append(stats[m + 's'])
        for a, b in pairs:
            draws[f'{a}-{b}_macro_recall'].append(stats[a][0] - stats[b][0])
            draws[f'{a}-{b}_fpr'].append(stats[a][1] - stats[b][1])
            if s_index:
                draws[f'{a}-{b}_stress_flag_rate'].append(stats[a + 's'] - stats[b + 's'])

    def interval(values):
        values = sorted(v for v in values if v is not None)
        return {'lo': values[int(.025 * len(values))], 'hi': values[int(.975 * len(values)) - 1], 'n_valid': len(values)} if values else None
    return {k: interval(v) for k, v in draws.items()}


def write_csv(path, rows):
    with path.open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    pilot_only = '--pilot-only' in sys.argv
    OUT.mkdir(parents=True, exist_ok=True)
    cases = load_cases(pilot_only)
    splits = ['pilot'] if pilot_only else ['test', 'ext', 'ext_stress']
    predictions, timing = {}, {}
    for name, (method, config) in METHODS.items():
        start = time.perf_counter()
        predictions[name] = run(cases, method, config)
        timing[name] = (time.perf_counter() - start) / len(cases) * 1e6
        check_alignment(predictions[name], cases)

    tag = 'pilot_' if pilot_only else ''
    write_csv(OUT / f'{tag}predictions.csv', [dict(r, method=m) for m, rows in predictions.items() for r in rows])
    summary = {}
    for split in splits:
        for m, rows in predictions.items():
            subset = [r for r in rows if r['split'] == split]
            if split.endswith('_stress'):
                summary[f'{split}/{m}'] = {'n': len(subset), 'false_flags': sum(r['decision'] == 'flag' for r in subset),
                                          'false_flag_rate': flag_rate(subset),
                                          'per_category': {c: {'n': sum(r['category'] == c for r in subset),
                                                               'false_flags': sum(r['category'] == c and r['decision'] == 'flag' for r in subset)}
                                                           for c in STRESS_CATEGORIES}}
            else:
                summary[f'{split}/{m}'] = {'any_error': score(subset, 'any'), 'identity_only': score(subset, 'identity')}
    (OUT / f'{tag}metrics.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')

    # Flat, traceable headline table (results.csv)
    table = []
    for key, value in summary.items():
        split, m = key.split('/')
        if 'any_error' in value:
            for definition in ('any_error', 'identity_only'):
                o = value[definition]['overall']
                table.append({'split': split, 'method': m, 'labels': definition, 'n': o['n'], 'tp': o['tp'], 'fp': o['fp'],
                              'fn_incl_abstain': o['fn_including_abstain'], 'precision': o['precision'], 'recall': o['recall'],
                              'macro_recall': o['macro_recall'], 'f1': o['f1'], 'fpr': o['false_positive_rate'], 'coverage': o['coverage']})
        else:
            table.append({'split': split, 'method': m, 'labels': 'valid_only', 'n': value['n'], 'tp': 0, 'fp': value['false_flags'],
                          'fn_incl_abstain': 0, 'precision': None, 'recall': None, 'macro_recall': None, 'f1': None,
                          'fpr': value['false_flag_rate'], 'coverage': None})
    write_csv(OUT / f'{tag}results.csv', table)
    (OUT / f'{tag}timing_us_per_case.json').write_text(json.dumps(timing, indent=2), encoding='utf-8')
    if pilot_only:
        print(json.dumps({k: v['any_error']['overall'] for k, v in summary.items()}, indent=2))
        return

    # A1.5(3) Field ablation on E (errors + stress), B2 thresholds
    E = [c for c in cases if c['split'] == 'ext']
    S = [c for c in cases if c['split'] == 'ext_stress']
    variants = {'B2 all fields': list(METADATA_FIELDS)}
    variants.update({f'{f} only': [f] for f in METADATA_FIELDS})
    variants.update({f'without {f}': [g for g in METADATA_FIELDS if g != f] for f in METADATA_FIELDS})
    ablation = []
    for label, fields in variants.items():
        er, sr = run(E, 'metadata_check', {'fields': fields}), run(S, 'metadata_check', {'fields': fields})
        sc = score(er)
        row = {'variant': label, 'macro_recall': sc['overall']['macro_recall'], 'clean_fpr': sc['overall']['false_positive_rate']}
        row.update({f'recall_{c}': sc['per_category'][c]['recall'] for c in ERROR_CATEGORIES})
        row['stress_false_flag_rate'] = flag_rate(sr)
        row.update({f'flags_{c}': sum(r['category'] == c and r['decision'] == 'flag' for r in sr) for c in STRESS_CATEGORIES})
        ablation.append(row)
    write_csv(OUT / 'ablation.csv', ablation)

    # A1.5(4) Threshold sensitivity (descriptive; frozen operating point is not changed)
    sensitivity = []
    for parameter, grid in [('title_threshold', [.5, .6, .7, .8, .85, .9, .95, 1.0]),
                            ('author_threshold', [.2, .3, .4, .5, .6, .7, .8, .9, 1.0])]:
        for value in grid:
            er, sr = run(E, 'metadata_check', {parameter: value}), run(S, 'metadata_check', {parameter: value})
            sc = score(er)['overall']
            sensitivity.append({'parameter': parameter, 'value': value, 'macro_recall': sc['macro_recall'],
                                'clean_fpr': sc['false_positive_rate'], 'stress_false_flag_rate': flag_rate(sr),
                                'frozen_operating_point': value == (.9 if parameter == 'title_threshold' else .8)})
    write_csv(OUT / 'sensitivity.csv', sensitivity)

    # A1.5(5) Source-clustered bootstrap
    pick = lambda split: {m: [r for r in rows if r['split'] == split] for m, rows in predictions.items()}
    boot = {'settings': {'seed': BOOT_SEED, 'resamples': BOOT_N, 'unit': 'source work', 'interval': '95% percentile'},
            'test': bootstrap(pick('test'), [('B2', 'B1'), ('B3', 'B2')]),
            'ext': bootstrap(pick('ext'), [('B2', 'B1'), ('B3', 'B2')], pick('ext_stress'))}
    (OUT / 'bootstrap.json').write_text(json.dumps(boot, indent=2), encoding='utf-8')
    print((OUT / 'results.csv').read_text())


if __name__ == '__main__':
    main()
