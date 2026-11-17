"""Phase IV checks: B3 rule, field ablation, stress-case construction, macro recall."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from citationlab import build_stress_cases, build_variants, predict, validate_cases
from evaluate import score


RECORD = {'found': True, 'doi': '10.1/a', 'title': 'Spectroscopic characterisation of thin films: a review',
          'authors': ['García', 'Okafor', 'Lee'], 'year': 2021, 'venue': 'Journal of Applied Things'}
CITATION = {k: v for k, v in RECORD.items() if k != 'found'}
lookup = lambda doi: RECORD


class PhaseFourTests(unittest.TestCase):
    def test_b2_unchanged_on_clean_and_wrong_author(self):
        self.assertEqual(predict(CITATION, lookup, 'metadata_check')['decision'], 'pass')
        self.assertEqual(predict(dict(CITATION, authors=['Nobody']), lookup, 'metadata_check')['reason'], 'metadata_mismatch:authors')

    def test_b3_accepts_et_al_but_rejects_foreign_author(self):
        et_al = dict(CITATION, authors=['Garcia'])
        self.assertEqual(predict(et_al, lookup, 'metadata_check')['decision'], 'flag')
        self.assertEqual(predict(et_al, lookup, 'metadata_containment')['decision'], 'pass')
        extra = dict(CITATION, authors=['Garcia', 'Nobody'])
        self.assertEqual(predict(extra, lookup, 'metadata_containment')['decision'], 'flag')
        self.assertEqual(predict(dict(CITATION, authors=[]), lookup, 'metadata_containment')['decision'], 'flag')

    def test_field_ablation_ignores_unselected_fields(self):
        wrong_year = dict(CITATION, year=2028)
        self.assertEqual(predict(wrong_year, lookup, 'metadata_check', {'fields': ['title']})['decision'], 'pass')
        self.assertEqual(predict(wrong_year, lookup, 'metadata_check', {'fields': ['year']})['decision'], 'flag')

    def test_reason_lists_every_failed_field(self):
        result = predict(dict(CITATION, year=1999, venue='Other'), lookup, 'metadata_check')
        self.assertEqual(result['reason'], 'metadata_mismatch:year+venue')

    def test_stress_cases_are_valid_and_applicability_respected(self):
        extras = {'short_venue': 'J. Appl. Things', 'print_year': 2022}
        cases = build_stress_cases(RECORD, extras, 0)
        categories = {c['category'] for c in cases}
        self.assertEqual(categories, {'et_al_first_author', 'subtitle_dropped', 'venue_abbrev', 'print_year', 'title_hyphen_break'})
        self.assertTrue(all(not c['labels']['any_error'] and c['split'] == 'ext_stress' for c in cases))
        hyphen = next(c for c in cases if c['category'] == 'title_hyphen_break')['citation']['title']
        self.assertIn('characte- risation', hyphen)  # longest word (16 letters) is split
        none = build_stress_cases(dict(RECORD, authors=['Solo'], title='Short title only'), {'short_venue': 'Journal of Applied Things', 'print_year': 2021}, 1)
        self.assertEqual(none, [])

    def test_ext_and_stress_share_sources_without_leakage_error(self):
        records = [dict(RECORD, doi=f'10.1/{i}', title=f'Title number {i} here') for i in range(3)]
        cases = build_variants(records, 'ext') + build_stress_cases(records[0], {}, 0)
        validate_cases(cases)
        leaked = build_variants(records[:2], 'pilot') + build_variants(records, 'ext')
        with self.assertRaises(ValueError):
            validate_cases(leaked)

    def test_macro_recall_is_mean_of_category_recalls(self):
        rows = [{'category': 'wrong_year', 'truth_any': True, 'truth_identity': False, 'decision': 'flag'},
                {'category': 'wrong_author', 'truth_any': True, 'truth_identity': True, 'decision': 'pass'},
                {'category': 'wrong_author', 'truth_any': True, 'truth_identity': True, 'decision': 'flag'},
                {'category': 'clean', 'truth_any': False, 'truth_identity': False, 'decision': 'pass'}]
        self.assertAlmostEqual(score(rows, 'any')['overall']['macro_recall'], (1 + .5) / 2)
        identity = score(rows, 'identity')['overall']
        self.assertEqual(identity['macro_recall'], .5)
        self.assertEqual(identity['fp'], 1)  # wrong_year flag counts against identity-only labels


if __name__ == '__main__':
    unittest.main()
