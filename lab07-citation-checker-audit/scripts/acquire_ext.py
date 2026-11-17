"""Amendment A1.2/A1.3: draw and freeze the random extension set E.

Run once, online, from the project root:   python scripts/acquire_ext.py
Rebuild from the frozen snapshot offline:  python scripts/acquire_ext.py --offline

The Crossref `sample` endpoint is random and cannot be replayed, so the saved
snapshot (data/ext_snapshot.json) is the frozen artifact. Only bibliographic
facts are kept; no abstracts or full text.
"""
import hashlib
import json
import random
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from citationlab import build_stress_cases, build_variants, doi_key, fetch_record, normalize, validate_cases

SAMPLE_URL = 'https://api.crossref.org/works?sample=100&filter=type:journal-article'
N_SOURCES = 40
SEED = 20261117


def year_of(message, key):
    parts = (message.get(key) or {}).get('date-parts') or [[]]
    return parts[0][0] if parts and parts[0] and parts[0][0] else None


def facts(message):
    """Minimal fact view of one sampled record (snapshot only)."""
    authors = [a.get('family', a.get('name', '')) for a in message.get('author', [])]
    return {'doi': doi_key(message['DOI']),
            'title': (message.get('title') or [''])[0],
            'authors': [a for a in authors if a],
            'year_published': year_of(message, 'published') or year_of(message, 'issued'),
            'print_year': year_of(message, 'published-print'),
            'online_year': year_of(message, 'published-online'),
            'venue': (message.get('container-title') or [''])[0],
            'short_venue': (message.get('short-container-title') or [''])[0]}


def eligible(record, excluded):
    return bool(record['doi'] not in excluded and len(normalize(record['title']).split()) >= 3
            and record['authors'] and record['year_published'] and record['venue'])


def main():
    offline = '--offline' in sys.argv
    cache = ROOT / 'data/cache'
    snapshot_path = ROOT / 'data/ext_snapshot.json'
    protocol = json.loads((ROOT / 'configs/protocol.json').read_text())
    excluded = {doi_key(d) for d in protocol['dois']}

    if snapshot_path.exists():
        snapshot = json.loads(snapshot_path.read_text(encoding='utf-8'))
    elif offline:
        raise FileNotFoundError('No frozen snapshot; run online once')
    else:
        request = urllib.request.Request(SAMPLE_URL, headers={'User-Agent': 'CitationLab07/1.0 (educational metadata pilot)'})
        with urllib.request.urlopen(request, timeout=90) as response:
            items = json.load(response)['message']['items']
        sampled = [facts(item) for item in items]
        chosen = sorted((r for r in sampled if eligible(r, excluded)), key=lambda r: r['doi'])[:N_SOURCES]
        snapshot = {'query': SAMPLE_URL, 'retrieved_utc': datetime.now(timezone.utc).isoformat(),
                    'returned': len(items), 'eligible': sum(eligible(r, excluded) for r in sampled),
                    'selected': chosen}
        snapshot_path.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False), encoding='utf-8')
    if len(snapshot['selected']) < N_SOURCES:
        raise ValueError(f"Only {len(snapshot['selected'])} eligible records; log an amendment instead of padding")

    # Checkers see the same per-DOI registry view as Phase III (fetch_record).
    records, extras = [], {}
    for item in snapshot['selected']:
        record = fetch_record(item['doi'], cache, offline)
        if not record['found'] or not all(record.get(k) for k in ('title', 'authors', 'year', 'venue')):
            raise ValueError(f"Incomplete lookup for sampled record {item['doi']}; log it, do not substitute")
        records.append(record)
        extras[record['doi']] = item

    group = sorted(records, key=lambda r: r['doi'])
    random.Random(SEED).shuffle(group)
    cases = build_variants(group, 'ext')
    stress = [c for i, r in enumerate(group) for c in build_stress_cases(r, extras[r['doi']], i)]
    validate_cases(json.loads((ROOT / 'data/cases.json').read_text(encoding='utf-8')) + cases + stress)
    # Cache every lookup evaluation will need (incl. synthetic-DOI 404s), so scoring runs offline.
    # Phase III cached pilot lookups only; the frozen test split is added here (A1.7).
    frozen_test = [c for c in json.loads((ROOT / 'data/cases.json').read_text(encoding='utf-8')) if c['split'] == 'test']
    for case in cases + frozen_test:
        if case['citation']['doi']:
            fetch_record(case['citation']['doi'], cache, offline)

    (ROOT / 'data/ext_cases.json').write_text(json.dumps(cases + stress, indent=2, ensure_ascii=False), encoding='utf-8')
    digest = lambda p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
    manifest = {'amendment': 'A1 (contribution_plan.md, 2026-11-17)',
                'snapshot_sha256': digest('data/ext_snapshot.json'),
                'ext_cases_sha256': digest('data/ext_cases.json'),
                'sources': len(group), 'error_cases': len(cases), 'stress_cases': len(stress),
                'stress_by_category': {c: sum(s['category'] == c for s in stress) for c in sorted({s['category'] for s in stress})}}
    (ROOT / 'data/ext_manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
