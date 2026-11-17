import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from citationlab import build_cases, doi_key, metrics, normalize, predict, validate_cases


class BaselineTests(unittest.TestCase):
    def setUp(self):
        self.record = {'found': True, 'doi': '10.1/a', 'title': 'A real title', 'authors': ['García'], 'year': 2023, 'venue': 'Journal'}
        self.citation = {k: v for k, v in self.record.items() if k != 'found'}

    def test_doi_normalization(self):
        self.assertEqual(doi_key('HTTPS://DOI.ORG/10.1/A'), '10.1/a')

    def test_clean_and_formatting(self):
        self.assertEqual(normalize('GARCÍA!'), 'garcia')
        self.assertEqual(predict(self.citation, lambda d: self.record)['decision'], 'pass')

    def test_registered_doi_does_not_validate_authors(self):
        citation = dict(self.citation, authors=['FalseAuthor'])
        self.assertEqual(predict(citation, lambda d: self.record)['decision'], 'pass')
        self.assertEqual(predict(citation, lambda d: self.record, 'metadata_check')['decision'], 'flag')

    def test_missing_doi_does_not_trigger_lookup(self):
        self.assertEqual(predict(dict(self.citation, doi=''), lambda d: self.fail('Lookup called'))['decision'], 'abstain')

    def test_no_crossref_record_is_a_flag(self):
        self.assertEqual(predict(self.citation, lambda d: {'found': False})['decision'], 'flag')

    def test_transport_failure_is_not_a_fabrication(self):
        def failed_lookup(doi):
            raise TimeoutError('offline')
        with self.assertRaises(TimeoutError):
            predict(self.citation, failed_lookup)

    def test_metric_denominators(self):
        rows = [{'truth': True, 'decision': 'flag'}, {'truth': False, 'decision': 'flag'}, {'truth': True, 'decision': 'abstain'}, {'truth': False, 'decision': 'pass'}]
        result = metrics(rows)
        self.assertEqual(result['precision'], .5)
        self.assertEqual(result['recall'], .5)
        self.assertEqual(result['false_positive_rate'], .5)
        self.assertEqual(result['coverage'], .75)

    def test_group_isolation_and_labels(self):
        records = [dict(copy.deepcopy(self.record), doi=f'10.1/{i}', title=f'Title {i}') for i in range(8)]
        cases = build_cases(records, {'seed': 42, 'pilot_sources': 4})
        validate_cases(cases)
        groups = {s: {c['source_id'] for c in cases if c['split'] == s} for s in ('pilot', 'test')}
        self.assertFalse(groups['pilot'] & groups['test'])
        self.assertEqual(len(cases), 64)
        for case in cases:
            if case['donor_id']:
                self.assertIn(case['donor_id'], groups[case['split']])
            if case['category'] == 'wrong_year':
                self.assertTrue(case['labels']['any_error'])
                self.assertFalse(case['labels']['identity_only'])

    def test_duplicate_and_source_leakage_rejected(self):
        records = [dict(copy.deepcopy(self.record), doi=f'10.1/{i}', title=f'Title {i}') for i in range(8)]
        cases = build_cases(records, {'seed': 42, 'pilot_sources': 4})
        with self.assertRaises(ValueError):
            validate_cases(cases + [cases[0]])
        cases[-1]['source_id'] = cases[0]['source_id']
        with self.assertRaises(ValueError):
            validate_cases(cases)

    def test_undefined_precision(self):
        result = metrics([{'truth': False, 'decision': 'abstain'}])
        self.assertIsNone(result['precision'])
        self.assertIsNone(result['recall'])
        self.assertEqual(result['coverage'], 0)


if __name__ == '__main__':
    unittest.main()
