"""Create a notebook with genuine captured script execution, without a Jupyter dependency."""
import json
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
setup = "from pathlib import Path\nimport subprocess, sys\nROOT = Path.cwd()\nif ROOT.name == 'notebooks':\n    ROOT = ROOT.parent\nassert (ROOT / 'configs/protocol.json').exists(), 'Open notebook from project root or notebooks directory'\n"
cells = [{'cell_type': 'markdown', 'metadata': {}, 'source': ['# Phase III baseline walkthrough\n', 'Outputs below are genuine local Python subprocess executions captured by scripts/make_walkthrough.py. They are not fabricated Jupyter-kernel execution logs. Run cells from the project or notebooks directory. No held-out evaluation occurs.\n']}]
for i, args in enumerate([['scripts/run.py', 'environment', '--offline'], ['scripts/run.py', 'pilot', '--offline'], ['-m', 'unittest', 'discover', '-s', 'tests', '-v']], 1):
    code = (setup if i == 1 else '') + f"result = subprocess.run([sys.executable, *{args!r}], cwd=ROOT, capture_output=True, text=True)\nprint(result.stdout)\nprint(result.stderr)\nassert result.returncode == 0\n"
    completed = subprocess.run([sys.executable, *args], cwd=root, capture_output=True, text=True)
    if completed.returncode:
        raise RuntimeError(completed.stderr)
    cells.append({'cell_type': 'code', 'metadata': {'execution_source': 'captured local subprocess'}, 'source': code.splitlines(True), 'execution_count': i,
                  'outputs': [{'output_type': 'stream', 'name': 'stdout', 'text': (completed.stdout + completed.stderr).splitlines(True)}]})
cells.append({'cell_type': 'markdown', 'metadata': {}, 'source': ['Read ../baseline_validation.md for interpretation. A registered DOI does not establish that title, authors or year are correct. Missing DOI requires review. The held-out comparison belongs to Phase IV.']})
notebook = {'cells': cells, 'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}, 'language_info': {'name': 'python', 'version': sys.version.split()[0]}}, 'nbformat': 4, 'nbformat_minor': 5}
(root / 'notebooks').mkdir(exist_ok=True)
(root / 'notebooks/phase3_baseline.ipynb').write_text(json.dumps(notebook, indent=2), encoding='utf-8')
print('Saved notebooks/phase3_baseline.ipynb with genuine subprocess output')
