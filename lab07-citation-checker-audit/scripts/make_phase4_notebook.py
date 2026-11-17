"""Build and genuinely execute notebooks/phase4_results.ipynb (needs nbformat, nbclient, ipykernel).

    python scripts/make_phase4_notebook.py

The notebook only reads results/phase4/ and data/; it does not rerun the evaluation.
"""
from pathlib import Path

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
md, code = nbformat.v4.new_markdown_cell, nbformat.v4.new_code_cell

cells = [
    md("# Phase IV results walkthrough\n\n"
       "This notebook reads the files written by `scripts/evaluate.py` and shows where every number in the paper comes from. "
       "It doesn't recompute anything: to regenerate the files, run `python scripts/verify.py`. "
       "The outputs below come from a real kernel execution by `scripts/make_phase4_notebook.py`."),
    code("import csv, json\nfrom pathlib import Path\n\n"
         "ROOT = Path.cwd().parent if Path.cwd().name == 'notebooks' else Path.cwd()\n"
         "RES = ROOT / 'results' / 'phase4'\n"
         "rows = list(csv.DictReader(open(RES / 'results.csv', encoding='utf-8')))\n"
         "metrics = json.load(open(RES / 'metrics.json', encoding='utf-8'))\n"
         "print(len(rows), 'rows in results.csv')"),
    md("## Table 2: held-out results\n\nAny-error labels for test (8 works) and extension (40 works), plus the identity-only rescoring (RQ3)."),
    code("def fmt(v):\n    return '-' if v in ('', None) else (f'{float(v):.3f}' if '.' in str(v) else v)\n\n"
         "print(f\"{'split':<11}{'method':<7}{'labels':<14}{'TP':>5}{'FP':>5}{'prec':>7}{'recall':>8}{'macro':>8}{'FPR':>7}\")\n"
         "for r in rows:\n"
         "    print(f\"{r['split']:<11}{r['method']:<7}{r['labels']:<14}{r['tp']:>5}{r['fp']:>5}{fmt(r['precision']):>7}{fmt(r['recall']):>8}{fmt(r['macro_recall']):>8}{fmt(r['fpr']):>7}\")"),
    md("## Table 3: false flags on legitimate variants\n\nEvery one of these 87 citations is valid, so every flag is a false flag."),
    code("for m in ('B1', 'B2', 'B3'):\n"
         "    per = metrics[f'ext_stress/{m}']['per_category']\n"
         "    total = metrics[f'ext_stress/{m}']\n"
         "    print(m, {c: f\"{v['false_flags']}/{v['n']}\" for c, v in per.items()}, '-> rate', round(total['false_flag_rate'], 3))"),
    md("## Which field fired?\n\nB2 records the failed field in `reason`, so each false flag can be traced to one rule."),
    code("from collections import Counter\n"
         "preds = list(csv.DictReader(open(RES / 'predictions.csv', encoding='utf-8')))\n"
         "fired = Counter((p['method'], p['category'], p['reason']) for p in preds if p['split'] == 'ext_stress' and p['decision'] == 'flag')\n"
         "for (m, cat, reason), n in sorted(fired.items()):\n"
         "    print(f'{m}  {cat:<20} {reason:<28} {n}')"),
    md("## One case end to end\n\nThe demo case: an \"et al.\" citation that B2 flags and B3 passes."),
    code("case_id = 'extstress-000-et_al_first_author'\n"
         "cases = {c['id']: c for c in json.load(open(ROOT / 'data' / 'ext_cases.json', encoding='utf-8'))}\n"
         "print('cited authors:', cases[case_id]['citation']['authors'])\n"
         "for p in preds:\n"
         "    if p['id'] == case_id:\n"
         "        print(p['method'], p['decision'], p['reason'])"),
    md("## Ablation and sensitivity\n\nDescriptive only. The frozen thresholds were never changed."),
    code("for r in csv.DictReader(open(RES / 'ablation.csv', encoding='utf-8')):\n"
         "    print(f\"{r['variant']:<17} macro recall {float(r['macro_recall']):.2f}   false-flag rate {float(r['stress_false_flag_rate']):.3f}\")\n"
         "boot = json.load(open(RES / 'bootstrap.json', encoding='utf-8'))\n"
         "print('\\nB3-B2 stress false-flag difference, 95% interval:', boot['ext']['B3-B2_stress_flag_rate'])"),
    md("## Figures\n\nThe same files used in the paper."),
    code("from IPython.display import Image, display\n"
         "for name in ('fig_detection_false_flags', 'fig_ablation', 'fig_sensitivity'):\n"
         "    display(Image(filename=str(ROOT / 'paper' / 'figures' / f'{name}.png'), width=700))"),
    md("For interpretation and limitations see `../results_discussion.md` and Section 7 of the paper."),
]

nb = nbformat.v4.new_notebook(cells=cells, metadata={'kernelspec': {'name': 'python3', 'display_name': 'Python 3', 'language': 'python'}})
NotebookClient(nb, timeout=120, kernel_name='python3', resources={'metadata': {'path': str(ROOT / 'notebooks')}}).execute()
out = ROOT / 'notebooks' / 'phase4_results.ipynb'
nbformat.write(nb, out)
print('executed and saved', out.relative_to(ROOT))
