"""Run from project root: python scripts/run.py environment|acquire|pilot [--offline]."""
import csv
import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from citationlab import build_cases, fetch_record, metrics, predict, validate_cases


def save(path, value):
    path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding='utf-8')


def main():
    config = json.loads((ROOT / 'configs/protocol.json').read_text())
    action = sys.argv[1]
    offline = '--offline' in sys.argv
    cache = ROOT / 'data/cache'
    if action == 'environment':
        gpu = subprocess.run(['nvidia-smi'], capture_output=True, text=True) if __import__('shutil').which('nvidia-smi') else None
        output = {'python': sys.version, 'platform': platform.platform(), 'executable': sys.executable,
                  'dependencies': 'standard library only', 'gpu_required': False,
                  'gpu_diagnostic': gpu.stdout if gpu else 'nvidia-smi unavailable',
                  'api_probe': fetch_record(config['dois'][0], cache, offline)}
        save('results/environment.json', output)
        print(json.dumps(output, indent=2))
    elif action == 'acquire':
        records = [fetch_record(doi, cache, offline) for doi in config['dois']]
        for record in records:
            if not record['found'] or not all(record.get(k) for k in ['title', 'authors', 'year', 'venue']):
                raise ValueError(f'Incomplete source record: {record}')
        cases = build_cases(records, config)
        validate_cases(cases)
        # Populate only pilot lookup cache; do not evaluate held-out cases.
        for case in cases:
            if case['split'] == 'pilot' and case['citation']['doi']:
                fetch_record(case['citation']['doi'], cache, offline)
        save('data/sources.json', records)
        save('data/cases.json', cases)
        save('data/manifest.json', {'protocol_sha256': hashlib.sha256((ROOT / 'configs/protocol.json').read_bytes()).hexdigest(),
                                  'cases_sha256': hashlib.sha256((ROOT / 'data/cases.json').read_bytes()).hexdigest(),
                                  'sources': len(records), 'pilot_cases': sum(c['split'] == 'pilot' for c in cases),
                                  'held_out_cases': sum(c['split'] == 'test' for c in cases)})
        print((ROOT / 'data/manifest.json').read_text())
    elif action == 'pilot':
        cases = json.loads((ROOT / 'data/cases.json').read_text(encoding='utf-8'))
        manifest = json.loads((ROOT / 'data/manifest.json').read_text())
        for key, path in [('protocol_sha256', 'configs/protocol.json'), ('cases_sha256', 'data/cases.json')]:
            if hashlib.sha256((ROOT / path).read_bytes()).hexdigest() != manifest[key]:
                raise ValueError(f'Frozen file changed: {path}; log amendment and reacquire')
        validate_cases(cases)
        rows = []
        for case in cases:
            if case['split'] != 'pilot':
                continue
            prediction = predict(case['citation'], lambda doi: fetch_record(doi, cache, offline))
            rows.append({'id': case['id'], 'category': case['category'], 'truth': case['labels']['any_error'], **prediction})
        if len({r['id'] for r in rows}) != len(rows):
            raise ValueError('Duplicate IDs')
        (ROOT / 'results').mkdir(exist_ok=True)
        with (ROOT / 'results/pilot_predictions.csv').open('w', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
        summaries = {'all': metrics(rows), **{category: metrics([r for r in rows if r['category'] == category]) for category in sorted({r['category'] for r in rows})}}
        save('results/pilot_metrics.json', summaries)
        bars = []
        for i, (category, result) in enumerate(list(summaries.items())[1:]):
            width = 380 * (result['recall'] or 0)
            bars.append(f'<text x="10" y="{50+i*35}">{category}</text><rect x="230" y="{34+i*35}" width="{width}" height="22" fill="#2874a6"/><text x="620" y="{50+i*35}">{result["recall"] if result["recall"] is not None else "N/A"}</text>')
        (ROOT / 'results/pilot_recall.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="730" height="360"><rect width="100%" height="100%" fill="white"/><text x="10" y="20">DOI-only pilot recall by error type (not held-out evidence)</text>' + ''.join(bars) + '</svg>')
        print(json.dumps(summaries, indent=2))
    else:
        raise ValueError('Use environment, acquire or pilot')


if __name__ == '__main__':
    main()
