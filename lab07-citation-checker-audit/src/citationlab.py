"""Transparent teaching baselines; not implementations of RefChecker or CiteCheck."""
import copy
import hashlib
import json
import re
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path


def normalize(value):
    value = unicodedata.normalize('NFKD', value).casefold()
    return ' '.join(re.findall(r'[^\W_]+', ''.join(c for c in value if not unicodedata.combining(c))))


def doi_key(value):
    return re.sub(r'^(https?://(dx\.)?doi\.org/|doi:\s*)', '', value.strip(), flags=re.I).lower()


def fetch_record(doi, cache, offline=False):
    """404 = no Crossref record. Transport errors must never become negative labels."""
    doi = doi_key(doi)
    path = Path(cache) / (hashlib.sha256(doi.encode()).hexdigest() + '.json')
    if path.exists():
        return json.loads(path.read_text(encoding='utf-8'))
    if offline:
        raise FileNotFoundError(f'Cache missing for {doi}; run acquisition online first')
    url = 'https://api.crossref.org/works/' + urllib.parse.quote(doi, safe='')
    for attempt in range(4):
        try:
            request = urllib.request.Request(url, headers={'User-Agent': 'CitationLab07/1.0 (educational metadata pilot)'})
            with urllib.request.urlopen(request, timeout=45) as response:
                message = json.load(response)['message']
            # Retain bibliographic facts only: no abstracts or full text.
            years = message.get('published', message.get('issued', {})).get('date-parts', [[]])
            result = {'doi': doi_key(message['DOI']), 'found': True,
                      'title': message.get('title', [''])[0],
                      'authors': [a.get('family', a.get('name', '')) for a in message.get('author', [])],
                      'year': years[0][0] if years and years[0] else None,
                      'venue': message.get('container-title', [''])[0] if message.get('container-title') else '',
                      'url': url, 'retrieved_utc': datetime.now(timezone.utc).isoformat()}
            break
        except urllib.error.HTTPError as error:
            if error.code == 404:
                result = {'doi': doi, 'found': False, 'url': url,
                          'retrieved_utc': datetime.now(timezone.utc).isoformat()}
                break
            if error.code not in (429, 500, 502, 503, 504) or attempt == 3:
                raise
            time.sleep(max(float(error.headers.get('Retry-After', 0)), 2 ** (attempt + 1)))
        except (urllib.error.URLError, TimeoutError):
            if attempt == 3:
                raise
            time.sleep(2 ** (attempt + 1))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
    time.sleep(1.1)  # Serial, low-volume requests; cache every successful response.
    return result


ERROR_CATEGORIES = ('wrong_year', 'wrong_author', 'wrong_doi', 'frankenstein', 'synthetic_unmatched')
IDENTITY_CATEGORIES = ('wrong_author', 'frankenstein', 'synthetic_unmatched')
STRESS_CATEGORIES = ('et_al_first_author', 'subtitle_dropped', 'venue_abbrev', 'print_year', 'title_hyphen_break')


def build_variants(group, split):
    """Eight frozen variants per source. Donor = next work in the same group."""
    cases = []
    for i, record in enumerate(group):
        donor = group[(i + 1) % len(group)]
        citation = {k: record[k] for k in ('doi', 'title', 'authors', 'year', 'venue')}
        variants = {}
        variants['clean'] = copy.deepcopy(citation)
        variants['format_variant'] = dict(copy.deepcopy(citation), doi='https://doi.org/' + citation['doi'].upper(), title=citation['title'].upper())
        variants['missing_doi'] = dict(copy.deepcopy(citation), doi='')
        variants['wrong_year'] = dict(copy.deepcopy(citation), year=citation['year'] + 7)
        variants['wrong_author'] = dict(copy.deepcopy(citation), authors=['SyntheticWrongAuthor'])
        variants['wrong_doi'] = dict(copy.deepcopy(citation), doi=donor['doi'])
        variants['frankenstein'] = dict(copy.deepcopy(citation), title=donor['title'])
        variants['synthetic_unmatched'] = dict(copy.deepcopy(citation), doi='10.0000/lab07-' + hashlib.sha256(citation['doi'].encode()).hexdigest()[:16], title='Synthetic Lab07 nonexistent test item ' + str(i), authors=['SyntheticWrongAuthor'])
        for category, observed in variants.items():
            cases.append({'id': f'{split}-{i:03d}-{category}', 'source_id': citation['doi'],
                          'donor_id': donor['doi'] if category in ('wrong_doi', 'frankenstein') else '',
                          'split': split, 'category': category, 'citation': observed,
                          'labels': {'any_error': category in ERROR_CATEGORIES,
                                     'identity_only': category in IDENTITY_CATEGORIES}})
    return cases


def build_cases(records, config):
    """Assign source groups before corruption. Donors stay inside the same split."""
    import random
    records = copy.deepcopy(records)
    random.Random(config['seed']).shuffle(records)
    cases = []
    for split, group in [('pilot', records[:config['pilot_sources']]),
                         ('test', records[config['pilot_sources']:])]:
        if len(group) < 2:
            raise ValueError('Each split needs at least two source works')
        cases.extend(build_variants(group, split))
    return cases


def build_stress_cases(record, extras, index, split='ext'):
    """Amendment A1.3: legitimate citation variants, all labelled valid.

    `record` is the fetch_record view the checkers use; `extras` holds
    snapshot-only fields (short venue, print year). Inapplicable variants are skipped."""
    citation = {k: record[k] for k in ('doi', 'title', 'authors', 'year', 'venue')}
    variants = {}
    if len(citation['authors']) >= 2:
        variants['et_al_first_author'] = dict(citation, authors=citation['authors'][:1])
    if ':' in citation['title']:
        head = citation['title'].split(':', 1)[0].strip()
        if len(normalize(head).split()) >= 3:
            variants['subtitle_dropped'] = dict(citation, title=head)
    short = (extras.get('short_venue') or '').strip()
    if short and normalize(short) != normalize(citation['venue']):
        variants['venue_abbrev'] = dict(citation, venue=short)
    print_year = extras.get('print_year')
    if isinstance(print_year, int) and print_year != citation['year']:
        variants['print_year'] = dict(citation, year=print_year)
    words = re.findall(r'[A-Za-z]{8,}', citation['title'])
    if words:
        word = max(words, key=len)
        cut = len(word) // 2
        variants['title_hyphen_break'] = dict(citation, title=citation['title'].replace(word, word[:cut] + '- ' + word[cut:], 1))
    return [{'id': f'{split}stress-{index:03d}-{category}', 'source_id': citation['doi'], 'donor_id': '',
             'split': split + '_stress', 'category': category, 'citation': copy.deepcopy(observed),
             'labels': {'any_error': False, 'identity_only': False}}
            for category, observed in variants.items()]


def validate_cases(cases):
    ids = set()
    groups = {}
    for case in cases:
        if case['id'] in ids:
            raise ValueError('Duplicate case ID')
        ids.add(case['id'])
        groups.setdefault(case['split'], set()).add(case['source_id'])
        if set(case['citation']) != {'doi', 'title', 'authors', 'year', 'venue'}:
            raise ValueError('Unexpected citation fields')
        if not isinstance(case['citation']['year'], int) or not isinstance(case['citation']['authors'], list):
            raise ValueError('Bad citation types')
        if any(type(value) is not bool for value in case['labels'].values()):
            raise ValueError('Labels must be bool')
    # Splits sharing a prefix (ext / ext_stress) are views of the same source works.
    names = sorted(groups)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            if a.split('_')[0] != b.split('_')[0] and groups[a] & groups[b]:
                raise ValueError('Source leakage across partitions')
    for case in cases:
        if case['donor_id'] and case['donor_id'] not in groups.get(case['split'], set()):
            raise ValueError('Donor leakage across partitions')


METADATA_FIELDS = ('title', 'authors', 'year', 'venue')

METHODS = {
    'doi_only': {},                                          # B1, frozen v1.0
    'metadata_check': {'author_rule': 'jaccard'},            # B2, frozen v1.0
    'metadata_containment': {'author_rule': 'containment'},  # B3, amendment A1.4
}


def field_checks(citation, record, config):
    """Per-field agreement between observed citation and registry record (True = agrees)."""
    title = SequenceMatcher(None, normalize(citation['title']), normalize(record['title'])).ratio()
    a, b = set(map(normalize, citation['authors'])), set(map(normalize, record['authors']))
    if config.get('author_rule', 'jaccard') == 'containment':
        authors_ok = bool(a) and a <= b  # every cited surname must be a real author
    else:
        authors_ok = (len(a & b) / len(a | b) if a | b else 0) >= config['author_threshold']
    return {'title': title >= config['title_threshold'], 'authors': authors_ok,
            'year': citation['year'] == record['year'],
            'venue': normalize(citation['venue']) == normalize(record['venue'])}


def predict(citation, lookup, method='doi_only', config=None):
    """Only observed citation is supplied; ground-truth and source IDs are not inputs.

    `config` may restrict `fields` (ablation) or override thresholds (sensitivity)."""
    if not citation['doi']:
        return {'decision': 'abstain', 'reason': 'missing_doi'}
    record = lookup(doi_key(citation['doi']))
    if not record['found']:
        return {'decision': 'flag', 'reason': 'no_crossref_record'}
    if method == 'doi_only':
        return {'decision': 'pass', 'reason': 'doi_registered'}
    if method not in METHODS:
        raise ValueError(method)
    settings = {'title_threshold': .9, 'author_threshold': .8, 'fields': METADATA_FIELDS}
    settings.update(METHODS[method])
    settings.update(config or {})
    checks = field_checks(citation, record, settings)
    failed = [field for field in settings['fields'] if not checks[field]]
    if failed:
        return {'decision': 'flag', 'reason': 'metadata_mismatch:' + '+'.join(failed)}
    return {'decision': 'pass', 'reason': 'metadata_agrees'}


def metrics(rows):
    # Abstentions require manual review: not counted as confirmed detections.
    tp = sum(r['truth'] and r['decision'] == 'flag' for r in rows)
    fp = sum(not r['truth'] and r['decision'] == 'flag' for r in rows)
    positives = sum(r['truth'] for r in rows)
    negatives = len(rows) - positives
    return {'n': len(rows), 'tp': tp, 'fp': fp,
            'fn_including_abstain': positives - tp,
            'precision': tp / (tp + fp) if tp + fp else None,
            'recall': tp / positives if positives else None,
            'f1': 2 * tp / (positives + tp + fp) if positives + tp + fp else None,
            'false_positive_rate': fp / negatives if negatives else None,
            'coverage': sum(r['decision'] != 'abstain' for r in rows) / len(rows) if rows else None}
