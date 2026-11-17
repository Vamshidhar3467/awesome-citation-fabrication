"""Capture genuine subprocess logs and verify deterministic offline reproduction."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(name, args):
    result = subprocess.run([sys.executable, *args], cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace')
    (ROOT / 'results' / f'{name}.log').write_text('COMMAND: python ' + ' '.join(args) + '\nEXIT CODE: ' + str(result.returncode) + '\nSTDOUT:\n' + result.stdout + '\nSTDERR:\n' + result.stderr, encoding='utf-8')
    if result.returncode:
        raise RuntimeError(f'{name} failed; inspect results/{name}.log')
    print(f'{name}: PASS')


def digest(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def main():
    run('environment', ['scripts/run.py', 'environment', '--offline'])
    run('tests', ['-m', 'unittest', 'discover', '-s', 'tests', '-v'])
    run('acquisition_offline', ['scripts/run.py', 'acquire', '--offline'])
    run('pilot', ['scripts/run.py', 'pilot', '--offline'])
    files = ['data/cases.json', 'data/manifest.json', 'results/pilot_predictions.csv', 'results/pilot_metrics.json', 'results/pilot_recall.svg']
    before = {p: digest(p) for p in files}
    run('pilot_repeat', ['scripts/run.py', 'pilot', '--offline'])
    after = {p: digest(p) for p in files}
    if before != after:
        raise AssertionError('Offline rerun changed outputs')

    # Phase IV: regenerate every reported result offline and require byte-identical files.
    # Timing and figures are excluded (wall-clock values; matplotlib embeds creation dates).
    phase4 = ['data/ext_cases.json', 'data/ext_manifest.json'] + [f'results/phase4/{f}' for f in (
        'predictions.csv', 'metrics.json', 'results.csv', 'ablation.csv', 'sensitivity.csv', 'bootstrap.json')]
    reported = {p: digest(p) for p in phase4}
    run('phase4_rebuild_ext', ['scripts/acquire_ext.py', '--offline'])
    run('phase4_evaluate', ['scripts/evaluate.py'])
    run('phase4_figures', ['scripts/make_figures.py'])
    run('paper_numbers', ['scripts/check_paper_numbers.py'])
    regenerated = {p: digest(p) for p in phase4}
    if reported != regenerated:
        changed = [p for p in phase4 if reported[p] != regenerated[p]]
        raise AssertionError(f'Phase IV rerun differs from reported outputs: {changed}')
    output = {'status': 'PASS', 'offline_repeat_identical': True, 'sha256': after,
              'phase4_regenerated_identical': True, 'phase4_sha256': regenerated,
              'held_out_evaluated': True}
    (ROOT / 'results/verification.json').write_text(json.dumps(output, indent=2), encoding='utf-8')
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
